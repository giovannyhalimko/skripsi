# Hybrid Model Collapse Fixes & Pipeline Improvements

**Date:** 2026-03-14
**Scope:** Fix cross-dataset collapse in HybridTwoBranch model + pipeline improvements

---

## Summary

Applied 8 fixes to address catastrophic cross-dataset collapse in the HybridTwoBranch model (F1=0.038 on CDF→FFPP). Also improved the training pipeline with multi-sample-size support, FFT cache recomputation, and result visualization.

---

## Model Architecture Changes

### Fix A: Feature Dimension Balancing
**File:** `deepfake_hybrid/src/models/hybrid_fusion.py`

**Problem:** Spatial branch (2048-dim) dominated frequency branch (64-dim) at 32:1 ratio, making hybrid effectively spatial-only.

**Change:** Added projection layers (`PROJ_DIM = 256`) for both branches:
- `spatial_proj`: Linear(2048, 256) → BatchNorm1d → ReLU
- `freq_proj`: Linear(64, 256) → BatchNorm1d → ReLU
- Fusion is now 50:50 balanced (512-dim total)

### Fix F: Fusion Normalization
**File:** `deepfake_hybrid/src/models/hybrid_fusion.py`

Addressed by Fix A — BatchNorm1d in projection layers normalizes feature scales before concatenation.

### Fix G: Increased Dropout
**File:** `deepfake_hybrid/src/models/hybrid_fusion.py`

**Change:** Classifier updated to:
- Dropout(0.5) → Linear(512, 128) → ReLU → Dropout(0.3) → Linear(128, 1)
- Previously: Linear(2112, 256) → ReLU → Dropout(0.3) → Linear(256, 1)

Also removed unused `self.freq_head = nn.Identity()`.

---

## Training Strategy Changes

### Fix B: Differential Learning Rates
**File:** `deepfake_hybrid/scripts/train.py`

**Problem:** All parameters shared lr=1e-4, destroying pretrained XceptionNet features.

**Change:** For hybrid model:
- Backbone (`model.spatial`): lr = base_lr / 10 (1e-5)
- New layers (`model.freq`, `model.spatial_proj`, `model.freq_proj`, `model.classifier`): lr = base_lr (1e-4)

For early_fusion: backbone at lr/10. For spatial/freq: unchanged single LR.

### Fix C: Backbone Freezing
**File:** `deepfake_hybrid/scripts/train.py`

**Problem:** XceptionNet backbone (22.8M params) overfits before fusion layers learn.

**Change:** Freeze spatial backbone for first 3 epochs (`FREEZE_EPOCHS = 3`), then unfreeze. Applied to hybrid and early_fusion models.

### Fix D: Cosine Annealing LR Scheduler
**File:** `deepfake_hybrid/scripts/train.py`

**Problem:** No LR decay caused large weight updates even near convergence.

**Change:** Added `CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)` with `scheduler.step()` at end of each epoch. Applied to all model types.

---

## Data Pipeline Changes

### Fix E: FFT Normalization
**File:** `deepfake_hybrid/src/fft_utils.py`

**Problem:** Per-image min-max normalization to [0,1] destroyed absolute magnitude — a key forgery signal.

**Change:** Removed per-image normalization in both `image_to_fft_logmag()` and `tensor_fft_logmag()`. Now returns raw `log1p(magnitude)`. FreqCNN's BatchNorm2d handles normalization during training.

**Impact:** Requires FFT cache recomputation (old `.npy` files are normalized to [0,1]).

### FFT Cache Recomputation Support
**Files:**
- `deepfake_hybrid/scripts/compute_fft_cache.py` — added `--force` flag
- `deepfake_hybrid/scripts/run_pipeline.py` — added `--force-fft` flag (passes `--force` to compute_fft_cache)

---

## Evaluation Changes

### Fix H: Optimal Threshold Selection
**Files:**
- `deepfake_hybrid/src/metrics.py` — added `find_optimal_threshold()` using Youden's J statistic (maximizes TPR - FPR)
- `deepfake_hybrid/scripts/eval.py` — now reports metrics at both threshold=0.5 and optimal threshold; added `--threshold` CLI arg; saves both to JSON output

---

## Pipeline & Notebook Changes

### Multi-Sample-Size Training
**File:** `deepfake_hybrid/colab_run.ipynb`

- `N_SAMPLES` replaced with `N_SAMPLES_LIST = [50, 200, 400]` (matches BAB III methodology: 3 variasi ukuran dataset)
- Step 4 loops through each N, running the full pipeline per value
- Intermediate results saved to Google Drive between each N run
- Plotting script runs after all sessions complete

### Configuration Additions
- `RECOMPUTE_FFT = True` — controls `--force-fft` flag (set to False after first successful run)
- `N_SAMPLES_LIST` — list of sample sizes to train sequentially

### Result Visualization
**File:** `deepfake_hybrid/scripts/plot_results.py` (NEW)

Generates BAB IV visualizations:
1. **Training curves** — loss, AUC, F1 per epoch for each model/dataset/N
2. **Model comparison** — grouped bar charts for in-dataset and cross-dataset metrics
3. **Generalization drop** — side-by-side F1 comparison (in vs cross)
4. **Sample size scaling** — line charts showing how F1/AUC scale with N

Output: `outputs/plots/` (PNG, 300 DPI)

---

## Files Modified

| File | Type |
|------|------|
| `src/models/hybrid_fusion.py` | Modified |
| `scripts/train.py` | Modified |
| `src/fft_utils.py` | Modified |
| `src/metrics.py` | Modified |
| `scripts/eval.py` | Modified |
| `scripts/compute_fft_cache.py` | Modified |
| `scripts/run_pipeline.py` | Modified |
| `scripts/plot_results.py` | **New** |
| `colab_run.ipynb` | Modified |

---

## Experimental Configuration (Final)

| Parameter | Value | Source |
|-----------|-------|--------|
| N_SAMPLES_LIST | [50, 200, 400] | BAB III |
| EPOCHS | 10 | BAB III |
| Models | spatial, freq, hybrid | BAB III |
| Datasets | FFPP, CDF | BAB III |
| Optimizer | Adam (lr=1e-4, wd=1e-4) | BAB III |
| Backbone LR | 1e-5 (10x lower) | Fix B |
| Freeze epochs | 3 | Fix C |
| LR scheduler | CosineAnnealing (eta_min=1e-6) | Fix D |
| Total experiment runs | 3 models × 2 datasets × 3 N-sizes × 2 eval = 36 | BAB III |
