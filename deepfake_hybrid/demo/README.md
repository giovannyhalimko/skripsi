---
title: Deepfake Detection Demo
emoji: 🕵️
colorFrom: indigo
colorTo: purple
sdk: gradio
app_file: app.py
pinned: false
---

# Deepfake Detection — Model Comparison Demo

A thesis demo that runs three deepfake-detection models on an uploaded face video and
shows their verdicts side-by-side:

- **Spatial** — XceptionNet on RGB pixels (the baseline)
- **Hybrid** — the proposed two-branch model (RGB + FFT frequency map, fused)
- **Frequency-only** — a small CNN on the FFT log-magnitude map

The comparison is deliberate: it lets reviewers see the thesis's headline result —
the proposed hybrid does **not** beat the simple spatial baseline (FFPP n=750 tier:
spatial AUC ≈ 0.78, hybrid ≈ 0.65, freq ≈ 0.57).

## How it works

Each upload is sampled at 5 fps (up to 16 frames), every frame is MTCNN face-cropped
(margin 0.3) exactly as in training, then preprocessed identically to the training
pipeline (RGB → 224² → ImageNet norm; FFT → log-magnitude → dataset-stat normalization).
Per-frame fake-probabilities are averaged into one video-level verdict per model, using
each model's FFPP-tuned decision threshold.

All preprocessing is reused verbatim from the repo's `src/` (`face_utils`,
`transforms`, `fft_utils`, `models/`); see `inference.py`.

## Files

```
app.py            Gradio UI (entrypoint)
inference.py      model loading + video pipeline (no gradio dependency)
requirements.txt  pip deps   |   packages.txt  apt deps (ffmpeg, libgl1)
src/              copied from ../src at deploy time (models/, transforms, fft_utils, face_utils, utils)
checkpoints/      spatial.pt hybrid.pt freq.pt + *_threshold.json + fft_stats.json
```

## Run locally

> The repo's `.venv` is **Python 3.9**, which caps Gradio at 4.44 — incompatible with the
> installed `huggingface_hub` 1.x. For a local UI preview use a **Python ≥3.10** venv:

```bash
python3.10 -m venv .venv-demo && source .venv-demo/bin/activate
pip install gradio torch torchvision timm facenet-pytorch opencv-python-headless Pillow "numpy<2"
python demo/app.py                          # opens http://127.0.0.1:7860
```

`app.py` finds `src/` either bundled (`demo/src`) or in the repo (`../src`), so it runs
without copying. The core pipeline (`inference.py`) needs no Gradio and was validated on
the repo's 3.9 venv. If you don't want a local preview, just deploy to the Space (below).

## Deploy to HuggingFace Spaces (free CPU)

1. Create a **New Space** → SDK **Gradio**, hardware **CPU basic (free)**.
2. `src/` and `checkpoints/` are **gitignored deploy artifacts** (kept out of the main repo
   to stay DRY). In a fresh clone, reconstruct them: `cp -r ../src ./src` and copy the
   checkpoints per the table below. The only artifact you must fetch separately is
   `checkpoints/fft_stats.json` (see note). The **contents of `demo/` become the Space repo
   root** — `app.py` must sit at the top.
3. `git lfs install && git lfs track "*.pt"` (already in `.gitattributes`), then commit and
   push the contents of `demo/` to the Space repo.
4. Watch the build log; once green, share the Space URL with reviewers.

> These `.pt` checkpoints (~195 MB) are staged in the working tree for the Space push — you
> do **not** need to commit them to the main thesis repo.

### Checkpoints (FFPP, n750, seed 0 — same tier/seed for a fair comparison)

From the repo `outputs/runs/`:

| copy from | to |
|---|---|
| `spatial_FFPP_n750_seed0/best.pt` | `checkpoints/spatial.pt` |
| `hybrid_FFPP_n750_seed0/best.pt`  | `checkpoints/hybrid.pt` |
| `freq_FFPP_n750_seed0/best.pt`    | `checkpoints/freq.pt` |
| each run's `threshold.json`       | `checkpoints/{spatial,hybrid,freq}_threshold.json` |

### FFT stats note

`fft_stats.json` (the FFPP FFT mean/std used at train time) is **not** in the local repo —
it lives in `outputs/fft_cache/FFPP/` on the training machine (vast.ai / Colab Drive). Fetch
it and place it in `checkpoints/`. Without it the app falls back to mean=5.0/std=3.0 and the
**freq/hybrid** branches may be miscalibrated. **Spatial is unaffected** (RGB-only).

## Caveat

Trained on FaceForensics++ face crops only. Other-source clips are out-of-distribution and
may be predicted unreliably. Research demo, not a production detector.
