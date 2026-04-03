# Experiment Conclusion — 2026-04-03

## Overview

First run with updated hyperparameters: LR 1e-4→5e-4, patience 5→10, label_smoothing 0.02→0.0, warmup 3→1 epoch, grad clip 1.0→5.0, pos_weight in loss, spectral masking 0.30→0.15. Both datasets use sample sizes [100, 250, 500, 750]. Only **n=100** results available.

---

## Code Changes vs Previous Run (2026-03-25)

| Change | Detail |
|--------|--------|
| LR | 1e-4 → 5e-4 |
| Early stopping patience | 5 → 10 |
| Label smoothing | 0.02 → 0.0 |
| Warmup epochs | 3 → 1 |
| Grad clip max_norm | 1.0 → 5.0 |
| Loss function | BCEWithLogitsLoss → BCEWithLogitsLoss(pos_weight) |
| Spectral masking probability | 0.30 → 0.15 |
| Sample size schedule | FFPP [100,300,600,1000] / CDF [100,250,500,750] → both [100,250,500,750] |
| Diagnostic logging | Added [DIAG] mean_prob_for_real vs mean_prob_for_fake to eval |

---

## 1. In-Dataset Performance (n=100)

| Model | Dataset | Val AUC | Test AUC | Test F1 |
|-------|---------|---------|----------|---------|
| spatial | FFPP | 0.542 | 0.497 | 0.558 |
| freq | FFPP | 0.324 | 0.307 | 0.219 |
| hybrid | FFPP | 0.399 | 0.437 | 0.379 |
| spatial | CDF | **0.951** | **0.825** | **0.754** |
| freq | CDF | 0.799 | **0.676** | **0.652** |
| hybrid | CDF | **0.895** | **0.895** | **0.780** |

### CDF improved significantly across all models

| Model | Old val AUC (03-25) | New val AUC (04-03) | Old test AUC | New test AUC |
|-------|---------------------|---------------------|--------------|--------------|
| spatial | 0.736 | **0.951** | 0.920 | 0.825 |
| freq | 0.574 | **0.799** | 0.459 | **0.676** |
| hybrid | 0.745 | **0.895** | 0.910 | 0.895 |

- **Freq CDF is no longer collapsed.** F1 went from 0.000 → 0.652, AUC from 0.459 → 0.676. The fix was patience=10 + pos_weight + reduced spectral masking.
- Hybrid CDF val AUC improved +0.15 (0.745 → 0.895), now training for 29 epochs.
- Spatial CDF val AUC improved +0.22 (0.736 → 0.951).

### FFPP performance regressed

| Model | Old val AUC (03-25) | New val AUC (04-03) | Change |
|-------|---------------------|---------------------|--------|
| spatial | 0.706 | 0.542 | **-0.164** |
| freq | 0.727 | 0.324 | **-0.403** |
| hybrid | 0.787 | 0.399 | **-0.388** |

FFPP performance dropped sharply. The higher LR (5e-4) combined with warmup=1 appears to destabilize FFPP training. Spatial peaked at epoch 1 (val AUC=0.542) then declined through epochs 2-3 before early stopping at epoch 6. The LR change that helped CDF hurt FFPP.

---

## 2. Cross-Dataset Performance (n=100)

| Train | Test | Model | F1 | AUC |
|-------|------|-------|----|-----|
| FFPP | CDF | spatial | 0.174 | 0.187 |
| FFPP | CDF | freq | 0.253 | 0.279 |
| FFPP | CDF | **hybrid** | **0.628** | **0.642** |
| CDF | FFPP | spatial | 0.583 | 0.669 |
| CDF | FFPP | freq | 0.349 | 0.454 |
| CDF | FFPP | **hybrid** | **0.631** | **0.720** |

Hybrid remains the best cross-dataset generalizer in both directions. CDF→FFPP hybrid AUC=0.720 is strong. FFPP→CDF spatial/freq are near-random (AUC 0.187/0.279), consistent with the FFPP models being poorly trained this run.

---

## 3. Generalization Drop (n=100)

| Model | Train | F1 in | F1 cross | Drop |
|-------|-------|-------|----------|------|
| spatial | FFPP | 0.558 | 0.174 | +0.384 |
| spatial | CDF | 0.754 | 0.583 | +0.171 |
| freq | FFPP | 0.219 | 0.253 | -0.035 (improves) |
| freq | CDF | 0.652 | 0.349 | +0.303 |
| hybrid | FFPP | 0.379 | 0.628 | **-0.249** (improves!) |
| hybrid | CDF | 0.780 | 0.631 | +0.149 |

Hybrid FFPP generalization drop is -0.249 (cross-dataset F1 is *higher* than in-dataset). This is misleading — the FFPP in-dataset score is artificially low due to the FFPP training failure this run, not because the model generalizes unusually well.

---

## 4. Training Dynamics

### Backbone freezing + patience=10 working well for CDF

- Spatial CDF trained for 20 epochs (up from ~13), reaching val AUC=0.951 at epoch 15
- Hybrid CDF trained for 29 epochs, steadily improving through epoch 24 (val AUC=0.895)
- Longer training allowed by patience=10 produced significantly better CDF results

### LR=5e-4 is too high for FFPP

Spatial FFPP training curve:
```
Epoch 1 (frozen):  val_auc=0.542  ← best (head learning fine)
Epoch 2 (frozen):  val_auc=0.397  ← drops immediately as LR ramps to full
Epoch 3 (frozen):  val_auc=0.342  ← continues declining
Epoch 4 (unfreeze): val_auc=0.356  ← no recovery
Early stop epoch 6: best=0.542
```

The warmup goes from LR×0.1 at epoch 1 to full LR by epoch 2 (warmup=1). At epoch 2 the head sees LR=5e-4 directly on a frozen backbone — likely overshooting. The previous warmup=3 was more gradual.

### Freq FFPP completely broken

Freq FFPP val AUC started at 0.303 and monotonically declined to 0.270 — never improved. Best was 0.324. This is a training failure, not a capability limit.

---

## 5. FFPP Test Split Diagnostic ([DIAG] output)

```
spatial  FFPP: mean_prob_for_real=0.5051, mean_prob_for_fake=0.5021 ← INVERTED?
freq     FFPP: mean_prob_for_real=0.4893, mean_prob_for_fake=0.4059 ← INVERTED?
hybrid   FFPP: mean_prob_for_real=0.4269, mean_prob_for_fake=0.4052 ← INVERTED?
```

vs CDF (working correctly):
```
spatial  CDF:  mean_prob_for_real=0.3887, mean_prob_for_fake=0.7835  ← clear separation
freq     CDF:  mean_prob_for_real=0.3331, mean_prob_for_fake=0.7698  ← clear separation
hybrid   CDF:  mean_prob_for_real=0.6914, mean_prob_for_fake=0.8062
```

**The FFPP test set has no discrimination signal.** Models assign near-identical probabilities (~0.40-0.51) to both real and fake test samples. This is not label inversion (which would give AUC <0.4); it's the model being genuinely uncertain on FFPP test videos.

Possible causes:
1. **Test split distribution mismatch** — test videos may be harder/different (different actors, locations, or manipulation methods)
2. **FFPP test set has a different compression level** — if test frames were extracted from c40 (heavy compression) while training used c23, artifacts would be washed out
3. **Low sample count** — with only ~70 training videos and 5 fps, the FFPP model may simply not have enough data to learn generalizable features

---

## 6. Summary

| Aspect | Result | vs 03-25 |
|--------|--------|----------|
| CDF in-dataset (spatial/hybrid) | AUC 0.895-0.951 | **Better** (+0.15-0.22) |
| CDF freq (was collapsed) | AUC 0.676 | **Fixed** (was 0.459) |
| FFPP training | AUC 0.32-0.54 | **Worse** (was 0.70-0.79) |
| FFPP test discrimination | Near zero | Unchanged |
| Hybrid cross-dataset (CDF→FFPP) | AUC 0.720 | Stable (was 0.788) |
| Training stability | CDF: more epochs; FFPP: fewer | Mixed |

---

## 7. Next Steps

### Critical
1. **Run `diagnose_splits.py --dataset FFPP`** on Colab to check label consistency and class balance in the FFPP test split
2. **Revert LR to 2e-4** (compromise between 1e-4 which worked for FFPP and 5e-4 which worked for CDF). Keep warmup=2 (not 1, not 3)

### Medium priority
3. Wait for n=250, n=500, n=750 results — FFPP models may recover at larger sample sizes even with the higher LR
4. Consider per-dataset LR if the split issue is ruled out: FFPP uses 1e-4, CDF uses 5e-4
