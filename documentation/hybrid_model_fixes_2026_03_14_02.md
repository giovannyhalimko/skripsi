# Deep Analysis Report — Deepfake Hybrid Detection

**Date:** 2026-03-14
**Scope:** Full code review, ML methodology, experiment design, thesis alignment

---

## 1. Code Correctness & Bugs

### 1.1 FFT Normalization Mismatch (HIGH IMPACT)

**Problem:** `src/transforms.py` applies no normalization to FFT inputs — only `ToTensor()`. The spatial branch receives ImageNet-normalized RGB inputs (mean-subtracted, std-divided), while the frequency branch receives raw `log1p(magnitude)` values. This creates a scale imbalance in the hybrid model's fusion layer, where the projected features from each branch have different magnitude ranges.

**Location:** `src/transforms.py:28-41` (`get_fft_transform`)

**Before:**
```python
def get_fft_transform(image_size=224, train=True):
    if train:
        t = transforms.Compose([
            transforms.Resize((image_size + 32, image_size + 32)),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
        ])
    ...
```

**Fix:** Add `Normalize(mean=[0.5], std=[0.5])` to standardize FFT log-magnitude to roughly [-1, 1] range:
```python
transforms.ToTensor(),
transforms.Normalize(mean=[0.5], std=[0.5]),
```

**Impact:** Should improve FreqCNN and hybrid model convergence and feature balance.

---

### 1.2 Corrupted Videos Silently Skipped (LOW IMPACT)

**Problem:** `scripts/extract_frames.py` skips videos that OpenCV can't open (`saved == 0`) with a bare `continue`. No summary of how many were skipped is reported.

**Location:** `scripts/extract_frames.py:129`

**Fix:** Track skipped count and print summary at the end.

---

### 1.3 No Minimum Class Guard in Splits (MEDIUM IMPACT)

**Problem:** `scripts/build_splits.py` performs stratified split without checking if each class has enough samples. With very small n (like n=50 with imbalanced data), the split could fail or produce degenerate 0-1 sample classes.

**Location:** `scripts/build_splits.py:36`

**Fix:** Add pre-split validation that each class has at least 4 samples (enough for 70/15/15 split to have >=1 per class).

---

### 1.4 Python 3.9 Type Hint Incompatibility (MEDIUM IMPACT)

**Problem:** Several files use `X | Y` union type syntax which requires Python 3.10+. This breaks on Python 3.9 (e.g., local Mac).

**Locations:**
- `src/utils.py` — already fixed in prior commit
- `scripts/download_datasets.py` — already fixed in prior commit
- `scripts/train.py:26` — `Path | None` still present

**Fix:** Replace with `Optional[Path]` from `typing`.

---

## 2. ML Methodology

### 2.1 FreqCNN is Severely Underpowered

**Observation:** FreqCNN has 3 conv layers (max 64 channels, 64-dim output) vs XceptionNet's 36-layer deep network with 2048-dim output. Even after projection to 256-dim each, the information density is vastly different. The frequency branch contributes limited discriminative power to the fusion.

**Recommendation:** Document this as a known limitation. Consider using a deeper frequency backbone (e.g., ResNet-18 on FFT) in future work.

### 2.2 Gradient Accumulation — Already Correct

**Verified:** `train.py:99` already divides loss by `accum_steps`:
```python
loss = loss_fn(logits, targets) / accum_steps
```
The running_loss correctly compensates at line 105. No fix needed.

### 2.3 Cosine Annealing Schedule

**Observation:** With 10 epochs and 3 frozen epochs, the effective training with meaningful LR is only ~4 epochs (epochs 4-7 before LR decays near eta_min=1e-6). This is tight but acceptable for fine-tuning pretrained models.

### 2.4 BCEWithLogitsLoss Without Class Weights

**Observation:** No class weighting is applied. Since balanced sampling targets 50/50, this is acceptable. No fix needed.

---

## 3. Experiment Design

### 3.1 Sample Sizes: n=50, 200, 400

**Decision:** Use three experimental tiers (n=50, 200, 400) instead of previous five (n=10, 50, 200, 400, 800).

**Rationale:**
- n=10 is too small for meaningful results
- n=800 and n=1600 require significantly more data and compute without adding proportional insight
- n=50/200/400 covers small/medium/large regimes and reveals the overfitting-generalization tradeoff

### 3.2 Single Seed — No Statistical Validity

**Problem:** All results use seed=42 only. Any metric could be a lucky/unlucky split.

**Fix:** Set `n_seeds: 3` in config.yaml. With 3 seeds, results can report mean +/- std.

### 3.3 Cross-Dataset Evaluation Design

**Verified:** The cross-dataset setup (train on FFPP, test on CDF and vice versa) is correctly implemented in `run_all.py`. Test splits are from the target dataset, which is the standard protocol.

**Caveat:** FFPP has 4+ manipulation methods while CDF has 1. This fundamental distribution mismatch means CDF->FFPP transfer is inherently harder. This should be discussed in the thesis.

### 3.4 FFPP Multi-Method Confounding

**Observation:** With n=400 on FFPP, the model sees 400 real + ~100 each from 4 fake methods. The model might learn method-specific artifacts rather than universal fake indicators. This is a dataset characteristic, not a bug — but should be acknowledged.

---

## 4. Thesis Alignment

### 4.1 Hybrid Model Framing

**Issue:** The thesis methodology frames the hybrid as the "proposed improvement." However, results show it achieves best in-dataset F1 but worst cross-dataset generalization. This is actually a valuable finding — the thesis should frame it as: "We investigate whether hybrid fusion improves detection and find that while it improves in-dataset performance, it worsens generalization."

### 4.2 Missing Ablation Studies

The thesis would benefit from:
- Fusion strategy comparison (concatenation vs attention)
- Projection dimension sensitivity
- Backbone freezing duration effect

These are noted as future work, not blocking issues.

---

## 5. Changes Applied

| # | File | Change | Impact |
|---|------|--------|--------|
| 1 | `src/transforms.py` | Add FFT normalization | High |
| 2 | `scripts/extract_frames.py` | Track & report skipped videos | Low |
| 3 | `scripts/build_splits.py` | Minimum class guard before split | Medium |
| 4 | `scripts/train.py` | Fix Python 3.9 type hint | Medium |
| 5 | `config.yaml` | Set n_seeds: 3 | Medium |
| 6 | `command.txt` | Update to n=50, 200, 400 only | Low |
| 7 | `colab_run.ipynb` | Update N_SAMPLES default | Low |
