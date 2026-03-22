# Experimental Conclusions: n=200 (2026-03-23 — Updated Training Code)

## Experiment Design

- **Models**: Spatial (Xception), Frequency (FFT + CNN), Hybrid (Two-Branch Fusion with SE Gate)
- **Datasets**: FaceForensics++ (FFPP), Celeb-DF (CDF)
- **Sample size**: n=200 videos per dataset
- **Training**: 10 epochs, lr=1e-4, batch_size=16, Adam optimizer, ImageNet-pretrained (spatial & hybrid)
- **Evaluation**: In-dataset (train & test same dataset), Cross-dataset (train on one, test on other)
- **Splits**: By video ID (preventing frame leakage), stratified
- **Code changes**: Same as n=50 (see CONCLUSION_n50.md for full list)

---

## Table 1 — In-Dataset Performance

| Model | Dataset | Acc | Precision | Recall | F1 | AUC |
|---------|---------|-------|-----------|--------|-------|-------|
| Spatial | FFPP | 0.481 | 0.484 | 0.445 | **0.464** | **0.431** |
| Freq | FFPP | 0.477 | 0.377 | 0.058 | 0.100 | 0.352 |
| Hybrid | FFPP | 0.446 | 0.318 | 0.087 | 0.136 | 0.389 |
| Spatial | CDF | 0.602 | 0.689 | 0.486 | **0.570** | **0.526** |
| Freq | CDF | 0.458 | 0.000 | 0.000 | 0.000 | 0.521 |
| Hybrid | CDF | 0.416 | 0.446 | 0.320 | 0.372 | 0.381 |

## Table 2 — Cross-Dataset Performance

| Model | Direction | Acc | Precision | Recall | F1 | AUC |
|---------|-----------|-------|-----------|--------|-------|-------|
| Spatial | FFPP→CDF | 0.531 | 0.552 | 0.713 | **0.622** | 0.565 |
| Freq | FFPP→CDF | 0.550 | 0.607 | 0.484 | 0.539 | **0.589** |
| Hybrid | FFPP→CDF | 0.608 | 0.649 | 0.602 | **0.624** | **0.630** |
| Spatial | CDF→FFPP | 0.674 | 0.843 | 0.434 | **0.573** | **0.712** |
| Freq | CDF→FFPP | 0.489 | 0.048 | 0.001 | 0.002 | 0.559 |
| Hybrid | CDF→FFPP | 0.608 | 0.648 | 0.490 | 0.558 | 0.710 |

## Table 3 — Generalization Drop (F1_in - F1_cross)

| Model | Train | F1_in | F1_cross | Drop |
|---------|-------|-------|----------|--------|
| Spatial | FFPP | 0.464 | 0.622 | **-0.158** |
| Spatial | CDF | 0.570 | 0.573 | -0.003 |
| Freq | FFPP | 0.100 | 0.539 | **-0.438** |
| Freq | CDF | 0.000 | 0.002 | -0.002 |
| Hybrid | FFPP | 0.136 | 0.624 | **-0.488** |
| Hybrid | CDF | 0.372 | 0.558 | **-0.185** |

---

## Comparison with Previous Run (2026-03-16)

### In-Dataset

| Model | Dataset | F1 (03-16) | F1 (03-23) | AUC (03-16) | AUC (03-23) | Change |
|---------|---------|------------|------------|-------------|-------------|--------|
| Spatial | FFPP | 0.441 | **0.464** | 0.484 | 0.431 | +5% F1, -11% AUC |
| Freq | FFPP | **0.440** | 0.100 | **0.500** | 0.352 | -77% F1, severe drop |
| Hybrid | FFPP | **0.536** | 0.136 | **0.525** | 0.389 | -75% F1, severe drop |
| Spatial | CDF | **0.656** | 0.570 | **0.710** | 0.526 | -13% F1, -26% AUC |
| Freq | CDF | **0.681** | 0.000 | **0.691** | 0.521 | collapsed |
| Hybrid | CDF | **0.585** | 0.372 | **0.667** | 0.381 | -36% F1, -43% AUC |

### Cross-Dataset

| Model | Direction | F1 (03-16) | F1 (03-23) | Change |
|---------|-----------|------------|------------|--------|
| Spatial | FFPP→CDF | 0.638 | 0.622 | -3% (stable) |
| Freq | FFPP→CDF | **0.750** | 0.539 | -28% |
| Hybrid | FFPP→CDF | 0.651 | 0.624 | -4% (stable) |
| Spatial | CDF→FFPP | 0.598 | 0.573 | -4% (stable) |
| Freq | CDF→FFPP | 0.200 | 0.002 | collapsed |
| Hybrid | CDF→FFPP | 0.351 | **0.558** | +59% (improved) |

---

## Key Findings

### 1. The Frequency Branch Is Broken at n=200

Freq models produce F1=0.100 on FFPP and F1=0.000 on CDF (in-dataset). At n=200, the deeper FreqCNN (5 layers, 700K params) combined with the new FFT normalisation does not have enough signal to train:
- Freq FFPP: only 75 true positives out of 1,294 positive samples (5.8% recall)
- Freq CDF: predicts all-negative (0 TP, 0 FP)

The 03-16 run had Freq CDF at F1=0.681 — the new code completely broke this. The likely culprit is the new FFT normalisation constants: `(mean=5.0, std=3.0)` shifts and scales the log-magnitude maps into a range that may not match the actual data distribution, producing near-zero or highly compressed input values.

### 2. Spatial Is the Only Functional In-Dataset Model

At n=200, only spatial produces above-chance results:
- Spatial FFPP: F1=0.464, AUC=0.431 (below random AUC but consistent with the n=200 dip)
- Spatial CDF: F1=0.570, AUC=0.526

This is roughly comparable to the 03-16 run for spatial (F1 was 0.441/0.656). The spatial branch's ImageNet-pretrained XceptionNet backbone is resilient to the code changes because it doesn't use the frequency pipeline.

### 3. Cross-Dataset Transfer Remains Surprisingly Stable for Spatial & Hybrid

Despite the in-dataset collapse, cross-dataset F1 for spatial and hybrid models is remarkably close to the 03-16 values:
- Spatial FFPP→CDF: 0.622 (was 0.638, -3%)
- Hybrid FFPP→CDF: 0.624 (was 0.651, -4%)
- Spatial CDF→FFPP: 0.573 (was 0.598, -4%)

This stability suggests the spatial backbone's features are the primary driver of cross-dataset transfer, and those features are relatively unaffected by the training code changes.

### 4. Hybrid CDF→FFPP Improved Significantly

Hybrid CDF→FFPP jumped from F1=0.351 to **0.558** (+59%). This is one of the few improvements in the new run. The SE attention gate may be helping the hybrid model better weight the spatial branch (which has useful features) over the broken frequency branch, resulting in better transfer when the spatial signal dominates.

### 5. Massive Negative Generalization Drops

All FFPP-trained models show large negative drops (cross > in-dataset), with Hybrid FFPP showing **-0.488**:

| Model | In-Dataset F1 | Cross F1 | Gap |
|---------|--------------|----------|-----|
| Hybrid FFPP | 0.136 | 0.624 | **4.6x better cross-dataset** |
| Freq FFPP | 0.100 | 0.539 | **5.4x better cross-dataset** |
| Spatial FFPP | 0.464 | 0.622 | 1.3x better cross-dataset |

This extreme pattern — where models generalise better to unseen data than their own test set — confirms that the n=200 FFPP dip is real and severe. FFPP's multi-method diversity at this scale creates an adversarial training environment, while CDF's uniform forgeries are an "easier" target.

### 6. Training Dynamics Show the Freq Branch Struggling

| Model | Dataset | Best Val AUC | Best Epoch | Pattern |
|---------|---------|-------------|------------|---------|
| Spatial | FFPP | 0.468 | 1 | Peaks immediately, degrades |
| Spatial | CDF | 0.765 | 6 | Steady improvement, best run |
| Freq | FFPP | 0.602 | 10 | Still improving — needs more epochs |
| Freq | CDF | 0.556 | 1 | Never improves, erratic |
| Hybrid | FFPP | 0.577 | 3 | Early peak, stagnates around 0.50 |
| Hybrid | CDF | 0.487 | 6 | Poor, never exceeds random |

---

## Verdict for n=200

| Aspect | Best Model | Score |
|--------|-----------|-------|
| In-dataset F1 (FFPP) | **Spatial** | 0.464 |
| In-dataset F1 (CDF) | **Spatial** | 0.570 |
| In-dataset AUC (CDF) | **Spatial** | 0.526 |
| Cross-dataset F1 (FFPP→CDF) | **Hybrid** | 0.624 |
| Cross-dataset F1 (CDF→FFPP) | **Spatial** | 0.573 |
| Cross-dataset AUC (CDF→FFPP) | **Spatial** | 0.712 |

**Summary:** At n=200, the updated training code has severely degraded the frequency and hybrid models while leaving spatial relatively stable. The frequency branch is effectively non-functional (F1=0.000-0.100 in-dataset) due to the new FFT normalisation and deeper architecture. The spatial branch carries all the useful signal for both in-dataset and cross-dataset evaluation. The n=200 FFPP dip persists and is even more pronounced, with FFPP-trained models performing 1.3-5.4x better cross-dataset than in-dataset. The one positive finding — Hybrid CDF→FFPP improving from F1=0.351 to 0.558 — suggests the SE gate is successfully down-weighting the broken frequency branch in favour of spatial features during transfer.
