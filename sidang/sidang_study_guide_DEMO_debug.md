# Demo — Debug-On-The-Spot Study Guide

> **Scenario this doc prepares you for:** a reviewer says *"run it,"* *"why did it just do that?"*, or *"change X and show me."* This is the **operational** guide — how to launch it, how the code flows, and every way it breaks with the fix. Pair it with Step 08 of `sidang_study_notes_detailed_2026-06-25.md` (the conceptual version). All line numbers are from `deepfake_hybrid/demo/`.
>
> **Golden rule when something breaks live:** narrate what you *expect*, read the error out loud, and map it to a cause below. Reviewers score you higher for *diagnosing calmly* than for a demo that never hiccups. You wrote this — act like you own it.

---

## 0. 20-second mental model

```
app.py  (Gradio UI)           ← the only file with a gradio dependency
  ├─ inference.py             ← all the ML: load models, decode video, predict  (no gradio → unit-testable)
  │    └─ src/  (face_utils, fft_utils, transforms, models/)   ← SHARED with training, verbatim
  └─ cards.py                 ← pure-stdlib HTML renderer (no torch/gradio)
checkpoints/  spatial.pt hybrid.pt freq.pt + *_threshold.json + fft_stats.json
```

Flow of one click: **video → `extract_frames` (5 fps, ≤16, MTCNN crop) → `_preprocess` (RGB tensor + FFT tensor per frame) → 3 models run batched → sigmoid→mean→threshold → cards + galleries.**

Three things that make it defensible: (1) preprocessing is the **same `src/` modules as training** (no drift), (2) it runs **all three models side-by-side** so the negative result is visible, (3) it **degrades gracefully** (missing MTCNN / stats → warnings, not crashes).

---

## 1. How to actually run it — the #1 thing to get right

⚠️ **There are two venvs. Use the right one.**

- `deepfake_hybrid/.venv` = **Python 3.9** → caps Gradio at 4.44 → **incompatible** with the installed `huggingface_hub` 1.x. **Do not launch the UI from here.**
- `deepfake_hybrid/demo/.venv-demo` = **Python 3.10** → this is the one that runs the Gradio app.

**Launch locally (memorize this):**
```bash
cd deepfake_hybrid/demo
source .venv-demo/bin/activate
python app.py                 # opens http://127.0.0.1:7860
```
- `app.py`'s `if __name__ == "__main__": demo.launch()` (app.py:119-120) — no port arg, so it defaults to **7860**.
- It finds `src/` either bundled (`demo/src`) or one level up (`../src`) via the loop in `inference.py:31-34`, so you don't need to copy anything.

**Sanity-check the ML core WITHOUT gradio** (works even on the 3.9 venv — great for a quick "is the model logic alive?" check):
```python
python -c "import inference as inf; lm=inf.load_models('checkpoints'); d,_=inf.get_detector(); print(inf.predict_video('SOME.mp4', lm, d))"
```
If that prints a dict with `ok: True`, the whole ML pipeline is fine and any problem is UI/gradio-only.

> **If asked "how do I run this?" and you're not sure the laptop is set up:** say *"the UI needs the Python 3.10 `.venv-demo`; the ML core also runs headless on the 3.9 repo venv. Let me activate the demo venv."* Then run the two commands above.

---

## 2. Pipeline walkthrough at debugging depth

Know **what each function returns** and **where it can fail** — that's what lets you diagnose live.

### Startup (`app.py:22-24`, runs once at boot)
- `LM = inf.load_models(CKPT_DIR)` — loads all 3 checkpoints on **CPU**. **This is the line that crashes at boot if a `.pt` is missing** (`FileNotFoundError`, inference.py:103).
- `DETECTOR, DETECTOR_ERR = inf.get_detector()` — creates MTCNN, or returns `(None, reason)` if `facenet-pytorch` is missing/broken. **Never crashes** — it degrades (inference.py:147-152).
- `_startup_warnings()` (app.py:50-60) prints yellow banners if cropping is OFF or FFT stats fell back.

### `load_models` (inference.py:88-144)
- For each of `spatial/hybrid/freq`: load `{key}.pt`, read its **embedded `config`** for `freq_depth`/`freq_base_channels` (so arch matches the checkpoint, **not** the drifted `config.yaml`), build the model with `pretrained=False`, `load_state_dict`, `.eval()`.
- `weights_only=False` is **deliberate** (inference.py:104-106) — our own trusted checkpoints carry a plain-dict `config`; avoids the torch≥2.6 `weights_only=True` default rejecting them.
- Thresholds: `{key}_threshold.json` → else **0.5** + a note. FFT stats: `fft_stats.json` → else **5.0/3.0** + a note.

### `extract_frames` (inference.py:155-187)
- `cv2.VideoCapture`; if `not cap.isOpened()` → returns `([],0,0)` → later becomes the **"Could not read any frames"** error.
- `interval = max(round(vfps/5),1)` → samples ~5 fps. Loops until **16 frames** collected.
- Per kept frame: `detect_face_bbox` → if a face, `crop_face` (margin 0.3) and `faces_found += 1`; **if no face, the full frame is kept** (fallback). If `detector is None`, every frame is full-frame.

### `_preprocess` (inference.py:190-197)
- BGR→RGB→PIL. RGB tensor via `spatial_tf` (Resize 224 → ToTensor → ImageNet norm). FFT via `image_to_fft_logmag(size=224, highpass=True)` then **z-score `(x - mean)/std`** using the loaded stats.

### `predict_video` (inference.py:233-270, `@torch.no_grad()`)
- Stacks all frames into `rgb_batch` and `fft_batch`, runs each model: spatial(rgb) / freq(fft) / hybrid(rgb,fft).
- `prob = sigmoid(logits).mean()` over frames → one video-level prob. `is_fake = prob >= threshold`.
- Returns `results` (for cards), `visuals` (galleries), `frames`, `faces_found`, `cropping`, `fft_calibrated`.

### `cards.render_cards` (cards.py:42-81)
- Pure string/HTML. Bar fill = `prob×100%`, tick mark = `threshold×100%`. Shows **"⚠︎ FFT calibration estimated"** on freq/hybrid cards only when `fft_calibrated=False`.

---

## 3. Failure-mode table — symptom → cause → fix (THE core of this doc)

| # | Symptom you'd see | Root cause | Fix / what to say |
|---|---|---|---|
| **F1** | App won't even start; `FileNotFoundError: Missing checkpoint: .../spatial.pt` | A `.pt` is missing from `checkpoints/` | Copy from `outputs/runs/{model}_FFPP_n750_seed0/best.pt` → `checkpoints/{model}.pt`. All three required. |
| **F2** | Yellow banner **"Face cropping is OFF (MTCNN unavailable)"** at top | `facenet-pytorch` not installed / failed to import (`get_detector` returned None) | `pip install facenet-pytorch`. *Say:* "cropping degraded gracefully to full-frame; results are off-distribution until MTCNN is back." **Spatial still runs.** |
| **F3** | freq/hybrid cards show **"⚠︎ FFT calibration estimated"** | `fft_stats.json` missing → fallback mean 5.0/std 3.0 | Copy `outputs/fft_cache/FFPP/fft_stats.json` → `checkpoints/`. **Spatial is unaffected** (RGB-only). Old fallback std 3.0 was ~2.3× too big. |
| **F4** | Result panel: **"❌ Could not read any frames from the video."** | Video codec unreadable by OpenCV (`cap.isOpened()` false) — usually missing **ffmpeg** or an exotic container | Install ffmpeg (in `packages.txt` for the Space; locally `brew install ffmpeg`). Or re-encode: `ffmpeg -i in.mov -c:v libx264 out.mp4`. Try a known-good `.mp4`. |
| **F5** | UI won't launch from the repo venv; gradio / `huggingface_hub` import error | Ran from the **Python 3.9 `.venv`** (caps gradio 4.44, clashes with hf_hub 1.x) | Use `.venv-demo` (Python 3.10). This is the single most common "it won't run" cause. |
| **F6** | `RuntimeError: Error(s) in loading state_dict ... size mismatch` | Checkpoint arch ≠ built model (wrong `freq_depth`/`base_channels`, or wrong `.pt` in the slot) | The code reads depth/base from the checkpoint's embedded `config` (inference.py:65-66). If the ckpt lacks config it defaults to **5/64**. Ensure you copied the *right* run's `best.pt`. |
| **F7** | `numpy`-related import crash (e.g. `_ARRAY_API not found`) | numpy 2.x installed; cv2/torch built against numpy 1.x | `pip install "numpy<2"` (it's pinned in `requirements.txt`). |
| **F8** | `OSError: port 7860 already in use` | Another gradio/process holds the port | `python -c "import app; app.demo.launch(server_port=7861)"` or kill the other process. |
| **F9** | Very slow / seems hung on a long clip | CPU-only + big video | It's capped at **16 frames** (`MAX_FRAMES`) so it's bounded; just wait. *Say:* "free-tier CPU, capped at 16 frames for latency." |
| **F10** | "It says REAL but I know it's fake" (or all three disagree) | Out-of-distribution clip (not FFPP face crop), or the genuine negative result | This is **expected** and defensible: models trained on FFPP crops; other sources are OOD (the caveat banner). And **hybrid disagreeing with / losing to spatial is the thesis finding**, not a bug. |
| **F11** | freq card sits near its threshold / flips on tiny changes | freq is **near-random** (AUC ~0.56), threshold 0.451 ≈ 0.5 | Expected — a near-random model has no confident operating point. This is *evidence*, not a defect. |

---

## 4. Live-debugging playbook (what to physically do)

1. **Read the exact error text.** Startup crash → §3 F1/F5/F6/F7. In-panel "❌ …" → F4. Yellow banner → F2/F3.
2. **Isolate UI vs ML:** run the headless one-liner in §1. If it returns `ok:True`, the model logic is fine → the problem is gradio/venv (F5/F8).
3. **Check the artifacts exist:** `ls checkpoints/` — expect `spatial.pt hybrid.pt freq.pt`, three `*_threshold.json`, `fft_stats.json`.
4. **Confirm the environment:** `python --version` (want 3.10 for the UI), `python -c "import gradio, torch, facenet_pytorch, cv2"` — whichever import throws is your missing dep.
5. **Fall back to the headless check** if the UI is truly dead: `predict_video(...)` prints the same verdicts as text — you can still *show the result* without the GUI.

> **Have this line ready:** *"The demo is designed to degrade, not crash — missing MTCNN or FFT stats show a warning and spatial keeps working. So let me read what the banner/error is telling us."*

---

## 5. "Change X and show me" — the tweaks a reviewer might request

Know these edit points so you can make a change on the spot without breaking it.

| Request | Where | Edit |
|---|---|---|
| "Sample more/fewer frames" | `inference.py:45` | `MAX_FRAMES = 16` → change; higher = slower on CPU. |
| "Change the sampling rate" | `inference.py:44` | `TARGET_FPS = 5` (matches training — say so before changing). |
| "Use 0.5 threshold instead of the tuned one" | delete/rename the `*_threshold.json` | falls back to 0.5 (inference.py:118-119). Show how spatial's calls change — good teaching moment on Youden's J. |
| "Turn off face cropping" | pass `detector=None` to `predict_video`, or uninstall MTCNN | full-frame path; shows why cropping matters (OOD without it). |
| "Run just one model" | `inference.py:51-55` `MODELS_SPEC` | comment out rows; the loop (predict_video:245) iterates this list. |
| "Change the FFT high-pass cutoff" | it's in `src/fft_utils.py` (`_highpass_mask`, cutoff 0.15) | ⚠️ this diverges from training — flag that any change here breaks the "matches training" guarantee. |

> **Safe stance:** for anything that touches preprocessing (fps, crop, FFT), say *"I can change it, but note it will no longer match the training distribution, so the numbers stop being comparable to the thesis."* That shows you understand *why* the values are what they are.

---

## 6. Known quirks to OWN before they're pointed out

- **FFT-stats number mismatch:** README/DOCUMENTATION say **mean 5.78**, but `checkpoints/fft_stats.json` on disk is **5.8410 / std 1.2767**. The code reads the **file live** (inference.py:127), so it always uses 5.84 — the doc text is just a stale earlier recompute. Quote **5.84**.
- **Two FFT re-encodes differ by one JPEG hop:** training computes FFT from the saved JPEG crop; the demo from the in-memory crop. Immaterial (one re-encode), but be honest if asked.
- **`pretrained=False` in the demo** (inference.py:68,72) is **not** "trained from scratch" — the checkpoint overwrites every weight; `False` just skips the timm ImageNet download so the Space is offline-safe and boots faster.
- **Thresholds are Youden's J on the FFPP *validation* split**, never test: spatial **0.127** / hybrid **0.229** / freq **0.451** (the actual files). Not 0.5 because the models aren't calibrated to a 0.5 boundary; the optimal TPR−FPR point differs per model.
- **The galleries are literal proof, not decoration:** the "Face crops" gallery = *exactly* what spatial ingests; the "FFT spectra" gallery = *exactly* the freq/hybrid input (MAGMA-colored). Point at them: **real vs fake spectra look indistinguishable** — that's the visible reason freq (and thus hybrid) carries little signal.

---

## 7. Command cheat-sheet (keep open in a terminal tab)

```bash
# launch the UI
cd deepfake_hybrid/demo && source .venv-demo/bin/activate && python app.py

# headless smoke test (works on the 3.9 repo venv too)
python -c "import inference as inf; lm=inf.load_models('checkpoints'); d,_=inf.get_detector(); \
print(inf.predict_video('PATH.mp4', lm, d))"

# verify artifacts present
ls checkpoints/                       # spatial.pt hybrid.pt freq.pt + *_threshold.json + fft_stats.json

# verify env / deps
python --version                       # want 3.10 for the UI
python -c "import gradio, torch, timm, facenet_pytorch, cv2, numpy; print('deps ok')"
python -c "import numpy; print(numpy.__version__)"   # must be <2

# re-encode a stubborn video so OpenCV can read it
ffmpeg -i input.mov -c:v libx264 -pix_fmt yuv420p output.mp4

# launch on a different port if 7860 is taken
python -c "import app; app.demo.launch(server_port=7861)"
```

---

## 8. If you only have 30 minutes

1. **Run it once yourself** with a known-good `.mp4` — feel the latency, see the cards + galleries.
2. **Memorize the launch command** and the **two-venv gotcha** (§1, F5) — that's the most likely live failure.
3. **Read the §3 table twice** — F2 (MTCNN off), F3 (FFT stats), F4 (can't read video) are the realistic three.
4. **Rehearse one sentence:** *"It degrades gracefully — let me read what the warning is telling us."*
5. Know that **hybrid ≤ spatial is the finding, not a bug** (F10/F11).
