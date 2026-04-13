# Training Improvements Branch — Code Changes Documentation

**Date:** 2026-04-09 to 2026-04-10
**Branch:** `naomi/training-improvements`
**Scope:** Face detection, video validation, per-method FFPP training, FFT high-pass filter, freq model tuning

---

## Summary of All Changes

| Change | Files Modified | Impact |
|--------|---------------|--------|
| Per-method FFPP training (`--method` flag) | 9 files (all pipeline scripts + utils + notebook) | Enables training on single manipulation method |
| Fix method filter (inside scan loop) | `extract_frames.py` | Fixed early_stop skipping matching videos |
| Use Drive directly (no SSD copy) | `colab_run.ipynb` | Fixed 0-byte files from broken cp -r |
| Video validation checks | `extract_frames.py` | Skip 0x0, 0-frame, black-frame videos |
| MTCNN face detection + cropping | `extract_frames.py`, `face_utils.py` (new), `run_pipeline.py`, `requirements.txt` | **FFPP spatial AUC 0.696 → 0.901** |
| FFT high-pass filter | `fft_utils.py` | Attenuate low frequencies, focus on manipulation artifacts |
| Freq model capacity increase | `config.yaml` | freq_base_channels 32→64 (~2.8M params) |
| Spectral masking reduction | `deepfake_data.py` | 15%→5% probability, narrower bands |
| Warmup increase | `train.py` | 2→3 epochs for more gradual LR ramp |

---

## 1. MTCNN Face Detection + Cropping

**Problem:** FFPP videos contain full scenes where faces are at varying positions, scales, and distances. Models were learning to classify backgrounds, not faces.

**Solution:** Added `--face-crop` flag to `extract_frames.py`. Uses MTCNN (via `facenet-pytorch`) to detect the largest face per frame, crops with 30% margin. Falls back to full frame when no face detected.

**Files:**
- `src/face_utils.py` (NEW): `create_face_detector()`, `detect_face_bbox()`, `crop_face()`
- `scripts/extract_frames.py`: `--face-crop`, `--face-margin` args, sequential mode when face crop enabled (MTCNN not picklable)
- `scripts/run_pipeline.py`: passthrough `--face-crop`, `--face-margin`
- `requirements.txt`: added `facenet-pytorch`

**Result:** FFPP spatial test AUC: 0.696 → **0.901** (+0.205)

---

## 2. Video Validation Checks

**Problem:** 0-byte files from Drive copy, corrupt videos, black frames caused models to train on garbage data.

**Solution:** Added 5-level validation in `extract_video_frames()`:
1. Can't open → skip
2. 0x0 resolution → skip
3. 0 frames / no duration → skip
4. Can't read first frame → skip
5. First frame is black (mean < 3) → skip

All trigger reserve pool replacement.

---

## 3. Per-Method FFPP Training

**Problem:** Hypothesis that mixing 4 manipulation methods caused FFPP failure.

**Solution:** Added `--method` flag across all pipeline scripts. Uses `effective_name()` helper in `src/utils.py` to construct output paths like `FFPP_Deepfakes`.

**Result:** Per-method separation did NOT fix FFPP (real issue was 0-byte files). The `--method` flag remains available but notebook reverted to combined training.

---

## 4. FFT High-Pass Filter

**Problem:** Face crop FFT dominated by low frequencies (smooth skin), drowning out manipulation artifacts in high frequencies.

**Solution:** Gaussian high-pass mask applied to FFT magnitude before log transform. Cutoff tested at 0.05 and 0.15 (0.15 = wider, keeps more mid-frequencies).

**Result:** Fixed freq model inversion (was 0.256 test AUC / INVERTED → now 0.62 val AUC, stable). Freq model still plateaus at ~0.62 — believed to be a fundamental limitation of single-channel FFT log-magnitude with a small CNN.

---

## 5. Drive Direct Access (No SSD Copy)

**Problem:** `cp -r` from Google Drive FUSE mount to Colab SSD created 0-byte empty files. This was the **root cause** of all FFPP training failures since April 2026.

**Solution:** Reverted notebook to use Drive mount path directly (`FFPP_LOCAL = FFPP_IN_DRIVE`). Same for CDF.

---

## Key Findings

1. **FFPP was broken by 0-byte files**, not by architecture/hyperparameters/method mixing
2. **Face cropping is essential** for deepfake detection on FFPP — transforms spatial AUC from 0.70 to 0.90
3. **Freq model on face crops peaks at ~0.62** — the single-channel FFT representation has limited discriminative power on cropped faces
4. **Spatial model is the strongest** single branch (0.90 FFPP, 0.82 CDF with face crop)
5. **Hybrid performance is limited by freq branch** — if freq contributes noise, hybrid is dragged below spatial
