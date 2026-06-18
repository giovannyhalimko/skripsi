# Demo App — Technical Documentation

A reviewer-facing web demo for the thesis's deepfake-detection models. A user uploads a
short face video; the app runs all **three** thesis models on it and shows their verdicts
side-by-side. The comparison is the point: it makes the thesis's headline finding visible —
the proposed **hybrid** model does *not* beat the simple **spatial** (XceptionNet) baseline.

> This document explains *how the demo works internally* — the tech stack, the end-to-end
> code process, the file layout, and how to run/deploy it. For the short user-facing blurb
> and the HuggingFace Space front-matter, see [`README.md`](README.md).

---

## 1. What the demo does (at a glance)

```
┌────────────┐   upload    ┌──────────────────────────────────────────────┐
│  Reviewer  │ ──────────► │  Gradio UI (app.py)                            │
└────────────┘   .mp4      │  • verdict cards (REAL/FAKE + confidence bar)  │
       ▲                   │  • "what the models see" galleries             │
       │   3 verdicts      └───────────────────┬────────────────────────────┘
       │   + visuals                           │ video path
       └───────────────────────────────────────┤
                                               ▼
                              ┌──────────────────────────────────┐
                              │  inference.predict_video()        │
                              │  decode → sample → crop →         │
                              │  preprocess → 3 models → aggregate │
                              └──────────────────────────────────┘
```

Three models are compared on the **same** sampled frames:

| Model | Input | Role |
|---|---|---|
| **Spatial — XceptionNet** | RGB pixels (224²) | the baseline |
| **Hybrid — proposed** | RGB + FFT log-magnitude, fused | the thesis's proposal |
| **Frequency-only** | FFT log-magnitude map (224²) | ablation / reference |

Each model produces a per-frame fake-probability; these are **averaged** into one
video-level probability, then compared against that model's tuned **decision threshold** to
produce a REAL/FAKE verdict.

---

## 2. Tech stack

### Runtime & framework
- **Python 3.10** (the HF Space runtime; pinned in `README.md` front-matter). The repo's
  own `.venv` is 3.9 and is fine for the *non-Gradio* inference core, but Gradio 5.x needs 3.10+.
- **Gradio 5.49.1** — the web UI framework and the HF Spaces SDK. `app.py` is the entrypoint.
- **CPU-only** — everything runs on the free CPU tier; `DEVICE = "cpu"` is hard-coded in
  `inference.py`. No GPU is required or used.

### ML / numerics
- **PyTorch 2.2.2 (+cpu)** + **torchvision 0.17.2 (+cpu)** — model definitions, inference,
  image transforms. The `+cpu` wheels keep the Space build small (no multi-GB CUDA download).
- **timm ≥ 1.0** — provides the `xception` backbone (ImageNet architecture; weights come
  from our checkpoints, not from timm at load time).
- **facenet-pytorch** — MTCNN face detector for cropping. Imported lazily and degrades
  gracefully to "no crop" if unavailable.
- **OpenCV (opencv-python-headless)** — video decoding and colormap rendering.
- **Pillow** — image handling for the transform pipeline.
- **NumPy < 2** — FFT math and array ops (pinned below 2.0 for wheel compatibility).

### System packages (`packages.txt`, installed by the Space via apt)
- `ffmpeg` — video codec support for OpenCV's `VideoCapture`.
- `libgl1`, `libglib2.0-0` — shared libs OpenCV needs at runtime on the headless Space image.

### Why these pins?
The pins in `requirements.txt` exist to make the free CPU Space build reproducibly and
small: CPU torch wheels via the PyTorch CPU index, `numpy<2` to avoid ABI breaks with the
pinned torch, and `opencv-python-headless` (no GUI deps) for a server environment.

---

## 3. End-to-end code process

The whole pipeline lives in `inference.py`; `app.py` is a thin Gradio wrapper and `cards.py`
only renders HTML. Here is the flow from upload to verdict.

### Step 0 — Startup (once, at app boot)
`app.py` calls:
- `inf.load_models(CKPT_DIR)` → builds all three models on CPU, loads their `.pt`
  checkpoints, reads each model's decision threshold (`{key}_threshold.json`), and loads the
  FFT normalization stats (`fft_stats.json`). Returns a `LoadedModels` dataclass.
- `inf.get_detector()` → constructs the MTCNN detector, or returns `(None, reason)` if
  `facenet-pytorch` is missing — the app keeps working, just without cropping.

Startup warnings (`_startup_warnings`) surface two degraded states to the reviewer:
face-cropping OFF, and FFT-stats fallback in use.

### Step 1 — Frame extraction (`extract_frames`)
1. Open the video with `cv2.VideoCapture`.
2. Compute a sampling interval so frames are taken at **`TARGET_FPS = 5`** (matching
   training's `config.yaml` fps), regardless of the source video's fps.
3. For each sampled frame, if the detector is available, run MTCNN
   (`detect_face_bbox`, margin **0.3**) and crop to the largest face (`crop_face`). If no
   face is found, **fall back to the full frame**.
4. Stop at **`MAX_FRAMES = 16`** to keep latency reasonable on a free CPU.

Returns `(frames, faces_found, frames_sampled)`.

### Step 2 — Preprocessing (`_preprocess`, per frame)
Each BGR frame is turned into the two tensors the models expect, **mirroring training exactly**:

- **RGB branch** (spatial + hybrid): `BGR→RGB` → `get_spatial_transform(train=False)`:
  `Resize(224²)` → `ToTensor` → ImageNet `Normalize` → tensor `(3,224,224)`.
- **FFT branch** (freq + hybrid): `image_to_fft_logmag(highpass=True)`:
  grayscale → `Resize(224²)` → `fft2` → `fftshift` → magnitude → Gaussian **high-pass mask**
  (cutoff 0.15, suppresses the low-frequency center) → `log1p` → then per-dataset
  normalization `(x − mean) / std` using `fft_stats.json` → tensor `(1,224,224)`.

### Step 3 — Inference (`predict_video`, batched, `@torch.no_grad`)
1. Stack all frames into an RGB batch `(N,3,224,224)` and an FFT batch `(N,1,224,224)`.
2. For each model:
   - `spatial`: `model(rgb_batch)`
   - `freq`: `model(fft_batch)`
   - `hybrid`: `model(rgb_batch, fft_batch)`
3. `sigmoid(logits)` → per-frame fake-probabilities → **mean** over frames = video-level prob.
4. Verdict: `is_fake = prob >= threshold` (each model has its own threshold).

### Step 4 — Visuals (`_build_visuals`)
Picks up to **4 evenly-spaced** frames and produces two galleries:
- **Face crops** — the resized RGB crop (what *spatial* sees).
- **FFT spectra** — the raw FFT log-magnitude (pre per-dataset normalization),
  min-max scaled per image and **MAGMA**-colormapped so the spectrum is human-visible
  (`_spectrum_to_rgb`). This is what *freq/hybrid* see.

### Step 5 — Rendering (`cards.render_cards`)
The structured results become an HTML block of per-model cards: a colored REAL/FAKE badge, a
fake-probability bar with the decision threshold marked as a vertical tick, and the raw
numbers. If the FFT stats fell back to defaults, the freq/hybrid cards show a
"calibration estimated" flag. `cards.py` is **pure stdlib** (no Gradio/torch) so it stays
unit-testable on the 3.9 venv.

---

## 4. File-by-file reference

```
demo/
├── app.py             Gradio UI + entrypoint. Loads models once, wires the
│                       Analyze button to inference, lays out cards + galleries.
├── inference.py       The engine. Model loading, video decode, MTCNN crop,
│                       preprocessing, batched inference, aggregation, visuals.
│                       No Gradio dependency — importable/testable standalone.
├── cards.py           Verdict-card HTML/CSS renderer. Pure stdlib.
├── requirements.txt   pip deps for the Space (CPU torch, timm, facenet, cv2…).
├── packages.txt       apt deps for the Space (ffmpeg, libgl1, libglib2.0-0).
├── README.md          User blurb + HF Space front-matter (sdk, python_version…).
├── .gitattributes     git-lfs tracking for *.pt (large checkpoints).
├── .gitignore         src/ and checkpoints/ — deploy artifacts, not committed to main repo.
├── checkpoints/       Deploy artifact (gitignored). Model weights + config:
│   ├── spatial.pt  hybrid.pt  freq.pt          trained weights (FFPP n750 seed0)
│   ├── {key}_threshold.json                    per-model decision thresholds
│   └── fft_stats.json                          FFT mean/std for normalization
└── src/               Deploy artifact (gitignored). `cp -r ../src ./src` copies it
    │                    whole; the files the demo actually imports are:
    ├── face_utils.py    MTCNN detector + bbox + crop
    ├── transforms.py    get_spatial_transform (RGB resize/ToTensor/ImageNet norm)
    ├── fft_utils.py     image_to_fft_logmag (FFT log-magnitude + high-pass)
    └── models/
        ├── spatial_xception.py   build_xception / feature extractor (timm)
        ├── freq_cnn.py           FreqCNN (configurable-depth CNN on FFT maps)
        └── hybrid_fusion.py      HybridTwoBranch (spatial + freq + SE-gated fusion)
```

> **`src/` and `checkpoints/` are deploy artifacts, not source.** They are gitignored in the
> main thesis repo to stay DRY (`src/` is the canonical `../src`; checkpoints come from
> `../outputs/runs`). They are reconstructed only when assembling the Space — see §6.

---

## 5. Models & artifacts

### Architectures (defined in `src/models/`)
- **Spatial** — `timm` `xception`, ImageNet architecture, single-logit binary head
  (`build_xception(num_classes=1, in_chans=3)`).
- **Frequency** — `FreqCNN`: stacked residual conv blocks (`Conv→BN→ReLU` + 1×1 shortcut +
  MaxPool) on the single-channel FFT map, adaptive-avg-pooled into an FC classifier. Depth
  and base channels come from the **checkpoint's embedded config**, not the (drifted)
  `config.yaml`.
- **Hybrid** — `HybridTwoBranch`: Xception features and FreqCNN features each projected to
  256-d, concatenated (512-d), passed through a **Squeeze-and-Excitation gate**, then a
  two-layer MLP head (`Dropout→Linear(512,128)→ReLU→Dropout→Linear(128,1)`).

At load time models are built with `pretrained=False` — the checkpoint overwrites every
weight anyway, so this skips the timm ImageNet download (offline-safe, faster boot).
Checkpoints are loaded with `weights_only=False` because they are our own trusted files
carrying a plain-dict `config` (avoids the torch ≥2.6 `weights_only` default change).

### Checkpoints (`checkpoints/*.pt`)
All three come from the **same** training tier for a fair comparison:
**FaceForensics++, n=750/class, seed 0** (from `../outputs/runs/{model}_FFPP_n750_seed0/best.pt`).
Approximate sizes: spatial ~80 MB, hybrid ~99 MB, freq ~16 MB.

### Decision thresholds (`checkpoints/{key}_threshold.json`)
Tuned on the FFPP **validation split** via Youden's J (`run_all.py:compute_val_threshold`),
not on the test set and not fixed at 0.5. Current values:

| Model | Threshold |
|---|---|
| spatial | 0.127 |
| hybrid | 0.229 |
| freq | 0.451 |

A clip is FAKE when its mean fake-probability ≥ this value. If a threshold file is missing,
the app falls back to 0.5 and logs a note.

### FFT normalization stats (`checkpoints/fft_stats.json`)
`{"mean": 5.778, "std": 1.277}` — the FFPP FFT log-magnitude statistics used at train time,
applied as `(x − mean) / std` to the freq/hybrid input. Recomputed locally from the FFPP
videos with the exact training preprocessing. **Only freq/hybrid depend on this**; spatial is
RGB-only and unaffected. If the file is missing, the app falls back to `mean=5.0 / std=3.0`
and flags the freq/hybrid cards as "calibration estimated."

---

## 6. Running & deploying

### Run locally (preview the UI)
The repo's `.venv` is Python 3.9, which caps Gradio at 4.44 (incompatible with the installed
`huggingface_hub` 1.x). For a UI preview, use a **Python ≥ 3.10** venv:

```bash
python3.10 -m venv .venv-demo && source .venv-demo/bin/activate
pip install gradio torch torchvision timm facenet-pytorch opencv-python-headless Pillow "numpy<2"
python demo/app.py            # serves http://127.0.0.1:7860
```

`app.py`/`inference.py` locate `src/` either bundled (`demo/src`) or in the repo (`../src`),
so the demo runs without copying anything for local dev. The inference core
(`inference.py`) has no Gradio dependency and can be exercised on the 3.9 venv.

### Deploy to HuggingFace Spaces (free CPU)
1. Create a **New Space** → SDK **Gradio**, hardware **CPU basic (free)**.
2. Reconstruct the deploy artifacts (they're gitignored in the main repo):
   - `cp -r ../src ./src`
   - copy checkpoints from `../outputs/runs/{model}_FFPP_n750_seed0/best.pt` →
     `checkpoints/{spatial,hybrid,freq}.pt`, plus each run's `threshold.json` →
     `checkpoints/{key}_threshold.json`, plus `fft_stats.json`.
3. `git lfs install && git lfs track "*.pt"` (already in `.gitattributes`).
4. Push the **contents of `demo/`** to the Space repo (so `app.py` sits at the repo root).
5. The Space reads `README.md` front-matter for the SDK/version, installs `packages.txt`
   (apt) and `requirements.txt` (pip), then launches `app.py`. Watch the build log; once
   green, share the URL.

> The `.pt` files (~195 MB total) are staged in the working tree only for the Space push via
> git-lfs — they do **not** need to be committed to the main thesis repo.

---

## 7. Configuration knobs (`inference.py`)

| Constant | Default | Meaning |
|---|---|---|
| `DEVICE` | `"cpu"` | inference device (CPU-only by design) |
| `TARGET_FPS` | `5` | frame sampling rate (matches training `config.yaml`) |
| `MAX_FRAMES` | `16` | cap on sampled frames (latency control) |
| `FACE_MARGIN` | `0.3` | MTCNN crop margin (matches `colab_run.ipynb`) |
| `DEFAULT_FFT_MEAN/STD` | `5.0 / 3.0` | fallback FFT normalization when `fft_stats.json` is absent |
| `MODELS_SPEC` | spatial/hybrid/freq | which models to load and their display order |

---

## 8. Caveats & limitations

- **Distribution-bound.** Models were trained on FaceForensics++ face crops only. Clips from
  other sources (different compression, lighting, generators) are out-of-distribution and may
  be predicted unreliably. This is a research demo, **not** a production detector.
- **It's a comparison, not a "best" detector.** The demo deliberately runs all three models
  to show the negative result: the proposed hybrid does not beat the spatial baseline
  (FFPP n=750 tier: spatial AUC ≈ 0.78, hybrid ≈ 0.65, freq ≈ 0.57).
- **Cropping matters.** If MTCNN is unavailable, predictions run on full frames, which no
  longer match the trained (cropped) distribution — the app warns about this on startup.
- **FFT calibration matters for freq/hybrid.** Without the correct `fft_stats.json`, those
  two branches use fallback stats and are flagged as "calibration estimated"; spatial is
  unaffected.
- **CPU latency.** Up to 16 frames × 3 models on CPU; the `MAX_FRAMES` cap keeps a single
  upload responsive on the free tier.
```
