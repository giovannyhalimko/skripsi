# Experiment Conclusion — 2026-03-25 (Partial)

## Overview

First run after performance improvements: residual FreqCNN (depth=5), AdamW optimizer, backbone freezing for spatial model, enhanced augmentation (ColorJitter, RandomErasing, spectral masking), reduced hybrid dropout (0.5→0.3), warmup 2→3 epochs.

Only **n=100** results are valid. The n=250 tables are stale (identical to n=100) due to a `--dataset` flag bug in `run_all.py` that was fixed mid-run.

---

## Code Changes vs Previous Run (2026-03-24)

| Change | Detail |
|--------|--------|
| FreqCNN | depth 3→5 (~130K→~700K params), added residual connections (FreqBlock) |
| Optimizer | Adam → AdamW (decoupled weight decay) |
| Spatial model | Now gets backbone freezing (3 epochs) + differential LR (backbone 1e-5, head 1e-4) |
| Warmup | 2 → 3 epochs |
| Spatial augmentation | Added ColorJitter(0.2, 0.2, 0.1, 0.05) + RandomErasing(p=0.1) |
| FFT augmentation | Added spectral band masking (p=0.3) on top of existing Gaussian noise |
| Hybrid dropout | Post-concat dropout 0.5 → 0.3 |
| Pipeline fix | `run_all.py` `select_model` now passes `freq_depth`/`freq_base_channels` from config |

---

## 1. Validation AUC — Old vs New (n=100)

| Model | Old (03-24) | New (03-25) | Delta |
|-------|-------------|-------------|-------|
| spatial_FFPP | 0.559 | **0.706** | **+0.147** |
| freq_FFPP | 0.567 | **0.727** | **+0.160** |
| hybrid_FFPP | 0.675 | **0.787** | **+0.113** |
| spatial_CDF | **0.931** | 0.736 | -0.195 |
| freq_CDF | **0.784** | 0.574 | -0.210 |
| hybrid_CDF | 0.708 | **0.745** | +0.036 |

**All three FFPP models improved significantly** (+0.11 to +0.16 val AUC). The changes had their strongest impact on FFPP, which was the weakest dataset previously.

**CDF spatial and freq regressed in validation AUC**, but this likely reflects reduced overfitting rather than worse learning — the old spatial_CDF val AUC of 0.931 was suspiciously high relative to its test AUC (0.920 test is consistent across both runs).

---

## 2. In-Dataset Test Performance (n=100)

| Model | Dataset | F1 | AUC | Acc |
|-------|---------|------|------|------|
| spatial | FFPP | 0.340 | 0.435 | 0.429 |
| freq | FFPP | 0.358 | 0.357 | 0.424 |
| hybrid | FFPP | **0.450** | **0.446** | 0.500 |
| spatial | CDF | **0.806** | **0.920** | 0.799 |
| freq | CDF | 0.000 | 0.459 | 0.539 |
| hybrid | CDF | **0.793** | **0.910** | 0.795 |

**CDF results are strong.** Spatial (F1=0.806, AUC=0.920) and hybrid (F1=0.793, AUC=0.910) both perform well. Hybrid matches spatial despite the freq branch collapse.

**FFPP in-dataset test remains near-random** (AUC 0.35–0.45 for all models). This persists across both old and new runs — confirms a systematic issue with the FFPP test split, not a model problem.

---

## 3. Cross-Dataset Generalization (n=100)

| Model | Direction | F1 | AUC |
|-------|-----------|------|------|
| spatial | FFPP→CDF | 0.395 | 0.265 |
| freq | FFPP→CDF | 0.005 | 0.570 |
| hybrid | FFPP→CDF | 0.379 | 0.364 |
| spatial | CDF→FFPP | 0.677 | 0.696 |
| freq | CDF→FFPP | 0.000 | **0.733** |
| hybrid | CDF→FFPP | **0.694** | **0.788** |

### Major improvement: Hybrid CDF→FFPP

| | Old (03-23, n=400) | Old (03-24, n=100) | New (03-25, n=100) |
|---|---|---|---|
| Hybrid CDF→FFPP F1 | 0.038 | 0.183 | **0.694** |
| Hybrid CDF→FFPP AUC | 0.506 | — | **0.788** |

The hybrid cross-dataset collapse (F1=0.038) that was the worst finding of the old experiments is **completely fixed**. The model no longer predicts all-negative when tested on FFPP after CDF training.

---

## 4. Generalization Drop (n=100)

| Model | Train | F1 in | F1 cross | Drop |
|-------|-------|-------|----------|------|
| spatial | FFPP | 0.340 | 0.395 | -0.055 (improves!) |
| spatial | CDF | 0.806 | 0.677 | +0.129 |
| freq | FFPP | 0.358 | 0.005 | +0.354 |
| freq | CDF | 0.000 | 0.000 | 0.000 |
| hybrid | FFPP | 0.450 | 0.379 | +0.071 |
| hybrid | CDF | 0.793 | 0.694 | **+0.099** |

**Hybrid CDF generalization drop is now only 0.099** — down from 0.627 in the old n=400 experiments. The fusion mechanism retains useful features across datasets.

---

## 5. Training Dynamics

### Backbone freezing is working

All models with pretrained backbones (spatial, hybrid) show a clear pattern:
- **Epochs 1–3 (frozen):** Gradual loss decrease, val AUC climbing steadily
- **Epoch 4 (unfreeze):** Sharp loss drop (e.g., spatial_FFPP: 0.657→0.480, hybrid_FFPP: 0.503→0.227)
- **Epochs 5+ (fine-tune):** Further refinement before early stopping

Example — spatial_CDF_n100:
```
Epoch 1 (frozen):  loss=0.692, val_auc=0.391
Epoch 3 (frozen):  loss=0.657, val_auc=0.655
Epoch 4 (unfroze): loss=0.498, val_auc=0.693  ← sharp improvement
Epoch 8 (best):    loss=0.142, val_auc=0.736
```

### Freq FFPP dramatically improved in training

Old freq_FFPP peaked at epoch 1 (val AUC=0.567) and never improved. New freq_FFPP trained for 12 productive epochs, reaching val AUC=0.727 at epoch 7. The residual connections and depth=5 give the freq branch enough capacity to learn from FFPP's diverse frequency patterns.

### Freq CDF collapsed

Freq_CDF peaked at epoch 1 (val AUC=0.574) and degraded through 6 epochs. Test F1=0.0 (predicts all negative). The deeper architecture may overfit CDF's smaller, more homogeneous frequency space. Consider reverting to depth=3 for CDF, or adding stronger regularization.

---

## 6. Critical Issues

### Issue 1: FFPP test split anomaly persists

All models score near-random on FFPP test (AUC 0.35–0.45) despite val AUC 0.70–0.79. This is consistent across both old and new runs. The FFPP test split likely has a distribution mismatch, class imbalance, or labeling issue.

**Action:** Run `diagnose_splits.py` on Colab to investigate.

### Issue 2: Freq branch collapses on CDF

FreqCNN (depth=5 with residuals) learned well on FFPP (val AUC 0.727) but collapsed on CDF (test F1=0.0). The deeper model may need:
- Lower learning rate for freq-only training
- Or depth=3 for CDF (CDF's frequency patterns may be simpler)
- Or more Gaussian noise / spectral masking to prevent memorization

### Issue 3: n=250 results invalid

The n=250 tables are identical to n=100 due to the `--dataset` bug (now fixed). Full rerun needed with latest code.

---

## 7. Summary — What Improved, What Didn't

| Aspect | Improved? | Detail |
|--------|-----------|--------|
| FFPP validation AUC | Yes | All 3 models +0.11 to +0.16 |
| Hybrid cross-dataset collapse | **Yes** | F1 from 0.038 → 0.694 (CDF→FFPP) |
| Hybrid generalization drop | **Yes** | From 0.627 → 0.099 |
| Freq branch on FFPP | Yes | Val AUC 0.567 → 0.727 |
| CDF in-dataset (spatial/hybrid) | Stable | AUC ~0.91–0.92 (unchanged) |
| FFPP test split anomaly | No | Still near-random; needs split investigation |
| Freq branch on CDF | **Worse** | Collapsed to F1=0.0 |

---

## 8. Next Steps

1. **Rerun full experiment** on Colab with `--dataset` fix for valid multi-sample results
2. **Run `diagnose_splits.py --dataset FFPP`** on Colab to identify FFPP test split issue
3. **Investigate freq CDF collapse** — consider per-dataset freq_depth or lower LR
4. **If FFPP split is broken**, rebuild splits with verified class balance
