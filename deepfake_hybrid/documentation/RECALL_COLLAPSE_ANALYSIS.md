# Recall Collapse Analysis — Spatial CDF→FFPP Cross-Dataset Transfer

**Date:** 2026-06-29
**Source data:** `outputs/gpu_pull_2026-06-19/` (latest run with the recall collapse)
**Model:** spatial (XceptionNet), trained on CDF, evaluated on FFPP, n750

## The puzzle

The cross-dataset summary (`tables/n750/Table2_cross_dataset_summary.csv`, 3-seed mean) shows:

| metric | value |
|---|---|
| recall | **0.074** |
| precision | **0.923** |
| AUC | **0.607** |
| accuracy | 0.554 |

Recall looks catastrophic, yet precision and AUC say the model still works. How can all three be true at once?

## Answer: a threshold-calibration artifact under domain shift — not a collapse of discriminative ability

AUC is **threshold-independent** — it measures only whether the model *ranks* fakes above reals. Recall and precision are measured at a **fixed 0.5 threshold** (`src/metrics.py:6`, `scripts/eval.py:109`). The three numbers are consistent because:

- **The ranking survives** (AUC 0.61, precision 0.92): the highest-scoring samples really are fakes.
- **The whole score distribution sinks below 0.5** under transfer, so the 0.5 cutoff calls almost everything "real" → recall collapses.

### Where the scores actually land (seed0)

| domain | fake-class mean prob | real-class mean prob |
|---|---|---|
| CDF (source, in-domain) | 0.839 | 0.101 |
| FFPP (target, transfer) | **0.108** | 0.044 |

In-domain, the model is confident and spread around 0.5. Under transfer, the entire distribution sinks to the floor (fake mean 0.839 → 0.108). Fakes still sit above reals (ranking intact), but everything is far below 0.5.

> Intuition: a thermometer reading 10° too cold still ranks hot days above cold days, but the "fever = 38°" rule reports everyone healthy. The instrument works; the cutoff is wrong for this instrument.

## Threshold experiment (seed0 preds, `roc_cm/CDF2FFPP_n750_preds_spatial.csv`)

FFPP AUC (seed0) = 0.630.

| threshold | value | recall | precision |
|---|---|---|---|
| Default 0.5 | 0.500 | 0.064 | 0.916 |
| Youden's J on FFPP test (oracle, **A**) | 0.042 | 0.468 | 0.606 |
| Youden's J on CDF, applied to FFPP (honest, **B**) | 0.286 | 0.095 | 0.888 |

(Single-seed recall 0.064 ≈ the 3-seed mean 0.074 — same story.)

### Reading the table

1. **The source threshold is much higher than the target's ideal.** CDF's own optimal cutoff is 0.286; FFPP's is 0.042. Transferring the source threshold honestly (B) barely moves recall (0.064 → 0.095) — the honest cross-dataset protocol does **not** fix the collapse.
2. **Only an oracle threshold tuned on the target (A) rescues recall** — and it must drop all the way to 0.042 to lift recall to 0.47. This *proves* the ranking is intact and the cutoff was the problem.
3. **The model is still genuinely weak.** Even at the oracle threshold, recall is only 0.47 and precision falls to 0.61, because AUC is only 0.63. The threshold explains why 0.074 looks *catastrophic*; it does not make transfer good.

### Two distinct conclusions (do not conflate)

- **The recall *collapse* (0.074)** = threshold artifact, fixable, misleadingly bad.
- **The *limited* transfer (AUC 0.63)** = genuine domain-shift weakness, real, not fixable by thresholding.

> ⚠️ "It was just the threshold" must not become "transfer is actually fine." Transfer is **weak but real**; the default threshold merely exaggerates how bad it looks.

## Caveats

- **Oracle threshold (A) is not a deployable result** — it peeks at FFPP test labels to set the cutoff. Cite it only as evidence that ranking is preserved, never as real-world performance.
- **Practical honest fix:** calibrate the threshold on a *small labeled sample from the target domain* (target-domain calibration). This is the standard real-world remedy for exactly this shift.

## Suggested thesis sentence

> Under CDF→FFPP transfer the spatial model's score distribution shifts sharply downward (fake-class mean 0.839 → 0.108), so the default 0.5 threshold collapses recall to 0.07 despite preserved ranking (AUC 0.61, precision 0.92). The collapse is a calibration artifact: the source-domain threshold (0.29) sits far above the target's optimal point (0.04), and transferring it honestly leaves recall at 0.10. An oracle target threshold restores recall to 0.47, confirming the ranking is intact — but the near-chance AUC shows cross-dataset transfer itself remains weak.

## Reproduce

```python
# from outputs/gpu_pull_2026-06-19/roc_cm/
# CDF2FFPP_n750_preds_spatial.csv  (target = FFPP)
# CDF_in_n750_preds_spatial.csv    (source = CDF)
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np, csv
def load(f):
    rows=list(csv.DictReader(open(f)))
    return (np.array([int(r['y_true']) for r in rows]),
            np.array([float(r['y_prob']) for r in rows]))
def youden(y,p):
    fpr,tpr,th=roc_curve(y,p); return th[(tpr-fpr).argmax()]
```
