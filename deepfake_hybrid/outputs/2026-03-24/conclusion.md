# Experiment Conclusion — 2026-03-24

## Overview

Three model architectures were evaluated: **spatial** (XceptionNet), **freq** (FFT-CNN), and **hybrid** (SE-gated fusion). Experiments ran across two datasets — **FFPP** (FaceForensics++) and **CDF** (Celeb-DF) — at sample sizes n = 100, 250, 300, 600, and 1000. Metrics reported are F1 and AUC on the held-out test split.

---

## 1. In-Dataset Performance (Table 1)

### FFPP — All models struggle

| n    | Best Model | F1    | AUC   |
|------|------------|-------|-------|
| 100  | hybrid     | 0.597 | 0.614 |
| 250  | spatial    | 0.550 | 0.660 |
| 300  | hybrid     | 0.559 | 0.432 |
| 600  | spatial    | 0.492 | 0.553 |
| 1000 | freq       | 0.557 | 0.435 |

### CDF — Spatial dominates at larger scales

| n    | Best Model | F1    | AUC   |
|------|------------|-------|-------|
| 100  | hybrid     | 0.710 | 0.781 |
| 250  | spatial    | 0.602 | 0.630 |
| 300  | spatial    | 0.636 | 0.776 |
| 600  | spatial    | 0.731 | 0.776 |
| 1000 | spatial    | 0.669 | 0.664 |

**Key findings:**

- **Spatial (XceptionNet) dominates on CDF** across most sample sizes, with the strongest validation AUC of 0.931 at n=100 (epoch 3).
- **All models struggle severely on FFPP** — most test AUCs hover at 0.40–0.55, near random. This suggests a systematic issue with the FFPP test split or distribution mismatch.
- **Hybrid shows its best advantage at small sample sizes (n=100)** on CDF: F1=0.710, AUC=0.781 — clearly outperforming both spatial (0.766) and freq (0.685).
- **Freq model consistently underperforms** — AUC=0.185 on FFPP at n=100 (worse than random), and F1=0.229 on CDF at n=250. The frequency branch alone lacks discriminative power.
- **Scaling up data does not consistently help.** Performance at n=1000 is often *worse* than at n=100 or n=300 (e.g., spatial FFPP AUC: 0.537 at n=100 → 0.466 at n=1000), indicating training instability at larger scales.

---

## 2. Cross-Dataset Generalization (Table 2)

### FFPP-trained, tested on CDF

| n    | Best Model | F1    | AUC   |
|------|------------|-------|-------|
| 100  | freq       | 0.662 | 0.676 |
| 250  | hybrid     | 0.618 | 0.551 |
| 300  | hybrid     | 0.621 | 0.561 |
| 600  | spatial    | 0.579 | 0.649 |
| 1000 | hybrid     | 0.647 | 0.654 |

### CDF-trained, tested on FFPP

| n    | Best Model | F1    | AUC   |
|------|------------|-------|-------|
| 100  | freq       | 0.602 | 0.524 |
| 250  | spatial    | 0.460 | 0.668 |
| 300  | spatial    | 0.326 | 0.691 |
| 600  | spatial    | 0.215 | 0.574 |
| 1000 | freq       | 0.468 | 0.443 |

**Key findings:**

- **FFPP→CDF generalizes surprisingly well** — often better than in-dataset FFPP performance itself. This is anomalous and reinforces the suspicion that FFPP in-dataset test performance is artificially low.
- **CDF→FFPP generalizes poorly** across all models, especially at n=1000 where spatial drops to F1=0.205, freq to F1=0.290, and hybrid to F1=0.183.
- **Hybrid and freq generalize better than spatial** in the FFPP→CDF direction, suggesting frequency features capture more transferable forgery artifacts.
- **Freq achieves its only competitive results cross-dataset** (F1=0.662 at n=100 FFPP→CDF), hinting that frequency features, while weak alone, encode generalizable manipulation signatures.

---

## 3. Generalization Drop (Table 3)

### Average F1 drop (in-dataset → cross-dataset)

| Model  | FFPP-trained drop     | CDF-trained drop     |
|--------|-----------------------|----------------------|
| spatial | negative (improves!) | +0.25 (large)        |
| freq   | negative (improves!) | +0.17                |
| hybrid | negative (improves!) | +0.17                |

**Key findings:**

- **FFPP-trained models show negative generalization drop** — they perform *better* on CDF than on FFPP itself. This strongly suggests the FFPP test set evaluation is broken or the test distribution is anomalous.
- **CDF-trained models suffer large drops** when tested on FFPP, especially spatial at n=600 (drop of 0.464) and n=1000 (drop of 0.464). These models appear to overfit CDF-specific patterns.
- **The asymmetry** (FFPP→CDF transfers fine; CDF→FFPP does not) suggests FFPP introduces patterns general enough to transfer, while CDF-trained models memorize dataset-specific artifacts.

---

## 4. Training Dynamics

- **Early stopping triggered frequently**: most runs stopped at 6–12 epochs (max was 30). Many models peaked at epoch 1–3 before degrading.
- **FFPP freq models peak at epoch 1** across all sample sizes — validation AUC never improves beyond the initial epoch, suggesting FFT features from FFPP provide no learnable signal.
- **Spatial on CDF is the most stable learner**: spatial_CDF_n100 reached val AUC=0.931 at epoch 3 — the best validation performance in the entire experiment.
- **Hybrid models show unstable training on FFPP**: val AUC oscillates without clear improvement (e.g., hybrid_FFPP_n300 peaks at 0.598 at epoch 1, then degrades).
- **Larger sample sizes do not lead to more training**: hybrid_CDF_n1000 stopped at 7 epochs with val AUC=0.599, while hybrid_CDF_n100 ran 12 epochs reaching val AUC=0.708. More data did not stabilize or extend useful training.

---

## 5. Critical Issues

1. **FFPP in-dataset test performance is anomalously poor.** All models score near or below chance on the FFPP test set despite reasonable validation AUCs in some runs. The most likely cause is a train/test distribution mismatch in the FFPP split, a class imbalance issue in the test fold, or a data quality problem specific to that split.

2. **The freq (FFT-CNN) branch is fundamentally weak as a standalone model.** Single-channel FFT log-magnitude with a 3-layer CNN (~130K params) does not learn reliably. It requires either richer spectral features (phase + magnitude, multi-scale), a deeper architecture, or strong regularization.

3. **Hybrid fusion does not consistently outperform spatial.** The SE-gated fusion only shows a clear advantage at n=100 on CDF. At larger scales, noise from the freq branch degrades the hybrid model below spatial-only performance. The fusion design may need revisiting.

4. **No consistent benefit from increasing data.** The current training recipe (learning rates, backbone freezing schedule, cosine decay) appears tuned for small datasets and becomes unstable at n=600+.

---

## 6. Recommendations

1. **Investigate the FFPP data pipeline.** Check test split class balance, label assignment, and whether frames from the same video are leaking across splits. The near-random test AUC despite learning in validation is a red flag.

2. **Strengthen the freq branch.** Explore multi-channel spectral inputs (phase spectrum, DCT, radial frequency profiles), deeper architectures, or spectral attention before using the freq branch in the hybrid model.

3. **Tune training hyperparameters for larger datasets.** Consider separate LR schedules or longer warmup for n>=600, and stronger regularization (higher label smoothing, dropout) to combat overfitting.

4. **Frame hybrid conclusions carefully in the thesis.** The results support the hybrid advantage only at small scale (n=100) on CDF. This is a valid finding — deepfake detection under data-scarce conditions — but scaling limitations and FFPP failure must be addressed transparently.

5. **Rerun FFPP experiments with a verified split** before drawing final conclusions about model rankings on that dataset.

---

## Summary Table — Best Results Per Setting

| Setting              | Best Model | F1    | AUC   | Notes                          |
|----------------------|------------|-------|-------|--------------------------------|
| FFPP in-dataset      | hybrid n=100 | 0.597 | 0.614 | Near random; likely split issue |
| CDF in-dataset       | spatial n=600 | 0.731 | 0.776 | Strong spatial performance     |
| CDF in-dataset (small) | hybrid n=100 | 0.710 | 0.781 | Hybrid advantage at small n   |
| FFPP→CDF cross       | freq n=100 | 0.662 | 0.676 | Freq transfers well            |
| CDF→FFPP cross       | freq n=100 | 0.602 | 0.524 | Poor overall; freq best        |
| Best val AUC overall | spatial CDF n=100 | — | 0.931 | Epoch 3                        |
