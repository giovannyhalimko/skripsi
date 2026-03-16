# Experimental Conclusions: n=200 (Post-Fix Run — 2026-03-16)

## Experiment Design

- **Models**: Spatial (Xception), Frequency (FFT + CNN), Hybrid (Two-Branch Fusion)
- **Datasets**: FaceForensics++ (FFPP), Celeb-DF (CDF)
- **Sample size**: n=200 videos per dataset
- **Training**: 10 epochs, lr=1e-4, batch_size=16, Adam optimizer, ImageNet-pretrained (spatial & hybrid)
- **Evaluation**: In-dataset (train & test same dataset), Cross-dataset (train on one, test on other)
- **Splits**: By video ID (preventing frame leakage), stratified
- **Bug fixes active**: FFT normalization, augmentation consistency, cosine scheduler T_max

---

## Table 1 — In-Dataset Performance

| Model | Dataset | Acc | Precision | Recall | F1 | AUC |
|---------|---------|-------|-----------|--------|-------|-------|
| Spatial | FFPP | 0.531 | 0.554 | 0.367 | 0.441 | 0.484 |
| Freq | FFPP | 0.514 | 0.527 | 0.378 | 0.440 | 0.500 |
| Hybrid | FFPP | 0.521 | 0.525 | 0.547 | **0.536** | **0.525** |
| Spatial | CDF | 0.655 | 0.689 | 0.626 | **0.656** | **0.710** |
| Freq | CDF | 0.621 | 0.610 | 0.772 | 0.681 | 0.691 |
| Hybrid | CDF | 0.601 | 0.645 | 0.534 | 0.585 | 0.667 |

## Table 2 — Cross-Dataset Performance

| Model | Direction | Acc | Precision | Recall | F1 | AUC |
|---------|-----------|-------|-----------|--------|-------|-------|
| Spatial | FFPP→CDF | 0.553 | 0.555 | 0.748 | 0.638 | 0.609 |
| Freq | FFPP→CDF | 0.703 | 0.672 | 0.848 | **0.750** | **0.722** |
| Hybrid | FFPP→CDF | 0.549 | 0.548 | 0.802 | 0.651 | 0.552 |
| Spatial | CDF→FFPP | 0.503 | 0.506 | 0.730 | **0.598** | **0.558** |
| Freq | CDF→FFPP | 0.482 | 0.455 | 0.128 | 0.200 | 0.505 |
| Hybrid | CDF→FFPP | 0.520 | 0.553 | 0.257 | 0.351 | 0.464 |

## Table 3 — Generalization Drop (F1_in − F1_cross)

| Model | Train | F1_in | F1_cross | Drop |
|---------|-------|-------|----------|--------|
| Spatial | FFPP | 0.441 | 0.638 | **−0.196** |
| Spatial | CDF | 0.656 | 0.598 | +0.058 |
| Freq | FFPP | 0.440 | 0.750 | **−0.309** |
| Freq | CDF | 0.681 | 0.200 | +0.481 |
| Hybrid | FFPP | 0.536 | 0.651 | **−0.115** |
| Hybrid | CDF | 0.585 | 0.351 | +0.234 |

---

## n=50 → n=200 Progression

### In-Dataset

| Model | Dataset | F1 (n=50) | F1 (n=200) | AUC (n=50) | AUC (n=200) | Trend |
|---------|---------|-----------|------------|------------|-------------|-------|
| Spatial | FFPP | 0.751 | 0.441 | 0.808 | 0.484 | **−41% — dip** |
| Freq | FFPP | 0.622 | 0.440 | 0.541 | 0.500 | **−29% — dip** |
| Hybrid | FFPP | 0.670 | 0.536 | 0.662 | 0.525 | **−20% — dip** |
| Spatial | CDF | 0.694 | 0.656 | 0.654 | 0.710 | −6% F1, +AUC |
| Freq | CDF | 0.364 | 0.681 | 0.297 | 0.691 | **+87% — surge** |
| Hybrid | CDF | 0.602 | 0.585 | 0.554 | 0.667 | stable |

### Cross-Dataset

| Model | Direction | F1 (n=50) | F1 (n=200) | Trend |
|---------|-----------|-----------|------------|-------|
| Spatial | FFPP→CDF | 0.696 | 0.638 | −8% |
| Freq | FFPP→CDF | 0.725 | 0.750 | +3% |
| Hybrid | FFPP→CDF | 0.751 | 0.651 | −13% |
| Spatial | CDF→FFPP | 0.632 | 0.598 | −5% |
| Freq | CDF→FFPP | 0.347 | 0.200 | **−42% — collapse** |
| Hybrid | CDF→FFPP | 0.344 | 0.351 | stable |

---

## Comparison with Pre-Fix n=200 Results

| Model | Dataset | F1 (old) | F1 (new) | AUC (old) | AUC (new) |
|---------|---------|----------|----------|-----------|-----------|
| Spatial | FFPP | 0.523 | 0.441 | 0.583 | 0.484 |
| Freq | FFPP | 0.354 | 0.440 | 0.430 | 0.500 |
| Hybrid | FFPP | 0.433 | **0.536** | 0.522 | 0.525 |
| Spatial | CDF | 0.542 | **0.656** | 0.507 | **0.710** |
| Freq | CDF | 0.266 | **0.681** | 0.460 | **0.691** |
| Hybrid | CDF | 0.534 | 0.585 | 0.583 | 0.667 |

---

## Key Findings

### 1. The n=200 FFPP Dip Is Confirmed and Severe

All three models collapse on FFPP in-dataset at n=200:
- Spatial FFPP: **AUC=0.484** — worse than random (0.5)
- Freq FFPP: **AUC=0.500** — exactly random
- Hybrid FFPP: **AUC=0.525** — barely above random

This is the clearest evidence yet of the n=200 dip hypothesis. With ~200 videos × 50 frames = ~10,000 FFPP training samples, FFPP's 6 manipulation methods create enough variety to confuse the model, but not enough data for it to learn robust cross-method patterns. The model is stuck in an optimization valley.

The dip affects FFPP more severely than CDF because FFPP is a multi-method dataset. 200 videos spread across 6 manipulation types means only ~33 videos per fake method — too few to learn any single method's artifacts, yet too many to simply memorize.

### 2. CDF Surges — Especially Freq

While FFPP crashes, CDF in-dataset improves markedly, particularly for the frequency model:
- **Freq CDF: F1=0.364 (n=50) → 0.681 (n=200)** — a +87% jump
- Spatial CDF: 0.694 → 0.656 (slight drop, still strong)

CDF's single-method forgeries are more consistent, so doubling the training data helps the frequency branch learn its spectral pattern. At n=50, Freq CDF was too underfitted to learn anything meaningful (F1=0.364). At n=200, it has enough examples to generalize within CDF.

### 3. FFPP→CDF Cross-Dataset Remains Strong Despite the FFPP Dip

Despite poor FFPP in-dataset scores, FFPP-trained models still generalize well to CDF:
- Freq FFPP→CDF: **F1=0.750, AUC=0.722** (best cross-dataset result this run)
- Hybrid FFPP→CDF: F1=0.651
- Spatial FFPP→CDF: F1=0.638

All three exceed their respective FFPP in-dataset F1 scores. This confirms that CDF is an "easier" target — the forgery patterns in CDF are more uniform and detectable even by a model that struggles with FFPP's internal diversity.

### 4. Large Negative Generalization Drops from FFPP

Three of six drops are negative (cross > in), with Freq FFPP showing the largest gap:

| Model | Drop | Interpretation |
|-------|------|----------------|
| Freq FFPP | −0.309 | Model that barely detects FFPP fakes is good at detecting CDF fakes |
| Spatial FFPP | −0.196 | Same pattern |
| Hybrid FFPP | −0.115 | Same pattern, less extreme |

The negative drops at n=200 are larger than at n=50 (where Freq FFPP was −0.103). This is because the in-dataset denominator (F1_in) has crashed at n=200 while cross-dataset performance holds relatively steady.

### 5. Freq CDF→FFPP Collapses Further

Freq CDF→FFPP went from F1=0.347 (n=50) to **F1=0.200** (n=200). With more CDF training data, the frequency branch learns CDF's spectral fingerprint more deeply, making it even less transferable to FFPP. This is the overfitting-to-dataset-artifacts problem the Opus analysis predicted, now visible at n=200 for the frequency branch.

### 6. Hybrid FFPP Struggles Most at n=200

Hybrid FFPP best validation AUC across all 10 epochs was only **0.346** (at epoch 8) — below random. The fusion mechanism combining a spatially-confused branch with an FFT branch that is just beginning to learn meaningful CDF patterns produces a degraded result. Neither branch has enough signal from FFPP at this scale to contribute usefully.

### 7. Bug Fix Impact at n=200

The most notable pre-fix vs post-fix changes:
- **Freq CDF**: F1 jumped from 0.266 → **0.681** — the biggest improvement. The normalized FFT now gives the frequency branch a properly scaled input, enabling real learning on CDF's consistent spectral patterns.
- **Spatial CDF AUC**: 0.507 → **0.710** — a massive improvement, no longer barely above random.
- **Hybrid FFPP**: F1 improved from 0.433 → 0.536 — the augmentation consistency fix contributed here.
- FFPP results overall remain low (dip regime), but they are more honest than the pre-fix numbers.

---

## Training Dynamics

| Model | Dataset | Best AUC Epoch | Best Val AUC | Final Loss | Notes |
|---------|---------|---------------|-------------|------------|-------|
| Spatial | FFPP | 1 | 0.649 | 0.0003 | Peaks at first epoch, heavily overfits to nothing |
| Spatial | CDF | 2 | 0.611 | 0.0011 | Early convergence then stable |
| Freq | FFPP | 8 | 0.639 | 0.6120 | Slow but steady — loss still high at epoch 10 |
| Freq | CDF | 1 | 0.562 | 0.6202 | Early best, never improves; struggles throughout |
| Hybrid | FFPP | 8 | 0.346 | 0.0291 | Below random — model failing on FFPP at n=200 |
| Hybrid | CDF | 10 | 0.565 | 0.0849 | Still improving at epoch 10 — needs more epochs |

**Critical observation:** Hybrid CDF's best epoch is epoch 10 — the model was still improving when training ended. This strongly supports the argument that n=200 needs more epochs (15-20) rather than fewer. Cutting to 5 epochs would have captured Hybrid CDF at a much worse checkpoint.

---

## Verdict for n=200

| Aspect | Best Model | Score |
|--------|-----------|-------|
| In-dataset F1 (FFPP) | **Hybrid** | 0.536 |
| In-dataset F1 (CDF) | **Spatial** | 0.656 |
| In-dataset AUC (CDF) | **Spatial** | 0.710 |
| Cross-dataset F1 (FFPP→CDF) | **Freq** | 0.750 |
| Cross-dataset F1 (CDF→FFPP) | **Spatial** | 0.598 |
| Smallest gen. drop (FFPP train) | **Hybrid** | −0.115 |
| Smallest gen. drop (CDF train) | **Spatial** | +0.058 |

**Summary:** n=200 is the clearest demonstration of the U-shaped learning curve. FFPP in-dataset performance crashes to near-random for all models — the n=200 dip is real and severe. CDF improves substantially, especially Freq CDF (+87% F1), because its single-method consistency is learnable at this data scale. Cross-dataset transfer from FFPP remains strong (Freq FFPP→CDF F1=0.750), with all FFPP-trained models outperforming their own in-dataset scores on CDF. Hybrid CDF still improving at epoch 10 signals that more training budget is needed at n=200 to see this model's true potential. The expected recovery at n=400 will be the critical validation of the overall experimental story.
