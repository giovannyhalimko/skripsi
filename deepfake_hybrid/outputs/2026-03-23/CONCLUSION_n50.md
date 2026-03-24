# Experimental Conclusions: n=50 (2026-03-23 — Updated Training Code)

## Experiment Design

- **Models**: Spatial (Xception), Frequency (FFT + CNN), Hybrid (Two-Branch Fusion with SE Gate)
- **Datasets**: FaceForensics++ (FFPP), Celeb-DF (CDF)
- **Sample size**: n=50 videos per dataset
- **Training**: 10 epochs, lr=1e-4, batch_size=16, Adam optimizer, ImageNet-pretrained (spatial & hybrid)
- **Evaluation**: In-dataset (train & test same dataset), Cross-dataset (train on one, test on other)
- **Splits**: By video ID (preventing frame leakage), stratified
- **Code changes since 2026-03-16 run** (commit fe32f61+):
  1. FFT normalization constants updated from `(0.5, 0.5)` to `(5.0, 3.0)` to match actual log1p range
  2. LR scheduler replaced: buggy CosineAnnealingLR → LinearLR warmup (2 epochs) + cosine decay
  3. Gradient clipping added (max_norm=1.0) with proper AMP unscaling
  4. Gaussian noise augmentation (sigma=0.1) added to FFT branch during training
  5. FreqCNN deepened from 3 to 5 conv layers (64→256 output dim, ~700K params)
  6. SE (Squeeze-and-Excitation) attention gate added on fused features
  7. Label smoothing (0.05) added
  8. torch.compile enabled, persistent DataLoader workers, TF32 matmuls

---

## Table 1 — In-Dataset Performance

| Model | Dataset | Acc | Precision | Recall | F1 | AUC |
|---------|---------|-------|-----------|--------|-------|-------|
| Spatial | FFPP | 0.513 | 0.567 | 0.522 | 0.544 | 0.490 |
| Freq | FFPP | 0.593 | 0.736 | 0.419 | 0.534 | 0.486 |
| Hybrid | FFPP | 0.490 | 0.526 | 0.844 | **0.648** | **0.518** |
| Spatial | CDF | 0.239 | 0.206 | 0.185 | 0.195 | 0.235 |
| Freq | CDF | 0.250 | 0.000 | 0.000 | 0.000 | 0.001 |
| Hybrid | CDF | 0.101 | 0.005 | 0.004 | 0.004 | 0.003 |

## Table 2 — Cross-Dataset Performance

| Model | Direction | Acc | Precision | Recall | F1 | AUC |
|---------|-----------|-------|-----------|--------|-------|-------|
| Spatial | FFPP→CDF | 0.726 | 0.765 | 0.649 | **0.703** | **0.797** |
| Freq | FFPP→CDF | 0.449 | 0.347 | 0.122 | 0.180 | 0.409 |
| Hybrid | FFPP→CDF | **0.866** | 0.788 | 1.000 | **0.881** | **0.991** |
| Spatial | CDF→FFPP | 0.238 | 0.308 | 0.298 | **0.303** | 0.163 |
| Freq | CDF→FFPP | 0.444 | 0.000 | 0.000 | 0.000 | 0.455 |
| Hybrid | CDF→FFPP | 0.344 | 0.000 | 0.000 | 0.000 | 0.462 |

## Table 3 — Generalization Drop (F1_in - F1_cross)

| Model | Train | F1_in | F1_cross | Drop |
|---------|-------|-------|----------|--------|
| Spatial | FFPP | 0.544 | 0.703 | **-0.159** |
| Spatial | CDF | 0.195 | 0.303 | -0.108 |
| Freq | FFPP | 0.534 | 0.180 | +0.354 |
| Freq | CDF | 0.000 | 0.000 | 0.000 |
| Hybrid | FFPP | 0.648 | 0.881 | **-0.233** |
| Hybrid | CDF | 0.004 | 0.000 | +0.004 |

---

## Comparison with Previous Run (2026-03-15)

### In-Dataset

| Model | Dataset | F1 (03-15) | F1 (03-23) | AUC (03-15) | AUC (03-23) | Change |
|---------|---------|------------|------------|-------------|-------------|--------|
| Spatial | FFPP | **0.751** | 0.544 | **0.808** | 0.490 | -28% F1, massive drop |
| Freq | FFPP | **0.622** | 0.534 | **0.541** | 0.486 | -14% F1 |
| Hybrid | FFPP | 0.670 | 0.648 | 0.662 | 0.518 | -3% F1, -22% AUC |
| Spatial | CDF | **0.694** | 0.195 | **0.654** | 0.235 | -72% F1, catastrophic |
| Freq | CDF | 0.364 | 0.000 | 0.297 | 0.001 | collapsed |
| Hybrid | CDF | **0.602** | 0.004 | **0.554** | 0.003 | collapsed |

### Cross-Dataset

| Model | Direction | F1 (03-15) | F1 (03-23) | Change |
|---------|-----------|------------|------------|--------|
| Spatial | FFPP→CDF | 0.696 | **0.703** | +1% (stable) |
| Freq | FFPP→CDF | **0.725** | 0.180 | -75% (collapsed) |
| Hybrid | FFPP→CDF | 0.751 | **0.881** | +17% (improved) |
| Spatial | CDF→FFPP | **0.632** | 0.303 | -52% |
| Freq | CDF→FFPP | **0.347** | 0.000 | collapsed |
| Hybrid | CDF→FFPP | **0.344** | 0.000 | collapsed |

---

## Key Findings

### 1. CDF In-Dataset Has Completely Collapsed

All three models on CDF in-dataset produce near-zero or zero F1 scores:
- **Freq CDF: F1=0.000** — model predicts a single class
- **Hybrid CDF: F1=0.004, AUC=0.003** — worse than random by a wide margin
- **Spatial CDF: F1=0.195, AUC=0.235** — severely below random

This is a catastrophic regression from the 03-15 run (Spatial CDF was F1=0.694). The updated FFT normalization constants `(5.0, 3.0)` — changed from `(0.5, 0.5)` — appear to have destabilized the frequency branch on CDF entirely. At n=50 with CDF's small sample count, the deeper FreqCNN (5 layers, 700K params) combined with Gaussian noise augmentation may be overwhelming the signal.

### 2. FFPP In-Dataset Is Near Random

All models hover around AUC=0.49-0.52 on FFPP — essentially random:
- Spatial FFPP: AUC=0.490
- Freq FFPP: AUC=0.486
- Hybrid FFPP: AUC=0.518

The 03-15 run had Spatial FFPP at AUC=0.808. The new LR scheduler (warmup + cosine decay), label smoothing, and architectural changes have not helped — they appear to have degraded the spatial branch's ability to learn from small FFPP datasets.

### 3. Hybrid FFPP→CDF Shows Anomalous Near-Perfect Transfer

The most striking result: **Hybrid FFPP→CDF achieves F1=0.881 and AUC=0.991** — near-perfect cross-dataset detection, despite the same model achieving only F1=0.648 and AUC=0.518 on its own training dataset (FFPP in-dataset).

This is suspicious and warrants investigation:
- The model predicts **100% recall** on CDF (all 271 positive samples detected) with 0 false negatives
- This pattern (poor in-dataset, perfect cross-dataset) suggests the model has learned a bias that happens to correlate with CDF's class distribution
- With only n=50 training videos, this could be a coincidental alignment between the model's prediction bias and CDF's test set characteristics

### 4. CDF-Trained Models Cannot Transfer at All

All CDF-trained models produce F1=0.000 on FFPP (freq, hybrid) or very low F1=0.303 (spatial). Combined with the collapsed CDF in-dataset results, this indicates the models trained on CDF at n=50 have learned essentially nothing useful — neither for CDF itself nor for transfer.

### 5. Training Dynamics Reveal Instability

| Model | Dataset | Best AUC | Best Epoch | Pattern |
|---------|---------|----------|------------|---------|
| Spatial | FFPP | 0.860 | 9 | Strong learning, stable plateau |
| Freq | FFPP | 0.792 | 10 | Late breakthrough after mode collapse (epochs 1-6) |
| Hybrid | FFPP | 0.560 | 7 | Mode collapse, never recovers well |
| Spatial | CDF | 0.790 | 2 | Strong early, severe degradation after |
| Freq | CDF | 0.818 | 3 | Strong early, severe late collapse |
| Hybrid | CDF | 0.874 | 8 | Excellent plateau, slight late decline |

**Critical discrepancy:** The training metrics show reasonable validation AUCs (e.g., Freq FFPP best val AUC=0.792, Hybrid CDF best val AUC=0.874), but the evaluation table shows much worse results (Freq FFPP eval AUC=0.486, Hybrid CDF eval AUC=0.003). This gap between training-time validation AUC and evaluation-time AUC suggests a **checkpoint loading or evaluation issue**, or that the best checkpoint is not being selected correctly.

### 6. The Architectural Changes Hurt More Than They Helped at n=50

The combined effect of all code changes is overwhelmingly negative at n=50:
- **Deeper FreqCNN** (3→5 layers, 700K params): Too many parameters for ~2,500 training frames at n=50
- **Gaussian noise augmentation**: May be destroying the weak signal in small datasets
- **New FFT normalization** (5.0, 3.0): If these constants don't match the actual data distribution, they could create out-of-range inputs
- **Label smoothing**: Reduces the gradient signal, which hurts when data is already scarce
- **SE gating**: Additional parameters that need sufficient data to learn

---

## Training Dynamics

| Model | Dataset | Best AUC Epoch | Best Val AUC | Final Loss | Notes |
|---------|---------|---------------|-------------|------------|-------|
| Spatial | FFPP | 9 | 0.860 | 0.117 | Strong learning, good convergence |
| Spatial | CDF | 2 | 0.790 | 0.119 | Peaks early, severe overfitting |
| Freq | FFPP | 10 | 0.792 | 0.384 | Still improving — needs more epochs |
| Freq | CDF | 3 | 0.818 | 0.364 | Early peak then collapses |
| Hybrid | FFPP | 7 | 0.560 | 0.168 | Mode collapse, poor convergence |
| Hybrid | CDF | 8 | 0.874 | 0.293 | Strong plateau, slight late decline |

---

## Verdict for n=50

| Aspect | Best Model | Score |
|--------|-----------|-------|
| In-dataset F1 (FFPP) | **Hybrid** | 0.648 |
| In-dataset F1 (CDF) | **Spatial** | 0.195 |
| In-dataset AUC (FFPP) | **Hybrid** | 0.518 |
| Cross-dataset F1 (FFPP→CDF) | **Hybrid** | 0.881* |
| Cross-dataset F1 (CDF→FFPP) | **Spatial** | 0.303 |

*Anomalous result — likely a bias artefact, not genuine generalisation.

**Summary:** The updated training code has severely degraded n=50 performance compared to the 2026-03-15 run. CDF in-dataset has completely collapsed for all models. FFPP in-dataset is near-random. The only bright spot — Hybrid FFPP→CDF F1=0.881 — is likely an artefact of prediction bias rather than genuine cross-dataset transfer. The architectural changes (deeper FreqCNN, SE gating, Gaussian noise, new FFT normalisation) are too heavy for the n=50 data regime. The discrepancy between training-time validation AUC (often reasonable) and evaluation-time AUC (near-random or collapsed) suggests a potential evaluation or checkpoint issue that should be investigated.
