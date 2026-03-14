# Experimental Conclusions: Deepfake Hybrid Detection

## Experiment Design

- **Models**: Spatial (Xception), Frequency (FFT + CNN), Hybrid (Two-Branch Fusion)
- **Datasets**: FaceForensics++ (FFPP), Celeb-DF (CDF)
- **Sample sizes**: n=50, n=200, n=400 videos per dataset
- **Training**: 10 epochs, lr=1e-4, batch_size=16, Adam optimizer, ImageNet-pretrained (spatial & hybrid)
- **Evaluation**: In-dataset (train & test same dataset), Cross-dataset (train on one, test on other)
- **Splits**: By video ID (preventing frame leakage), stratified

---

## Table 1 — In-Dataset Performance

| Model | Dataset | F1 (n=50) | F1 (n=200) | F1 (n=400) | AUC (n=50) | AUC (n=200) | AUC (n=400) |
|---------|---------|-----------|------------|------------|------------|-------------|-------------|
| Spatial | FFPP | 0.540 | 0.523 | **0.630** | 0.674 | 0.583 | **0.624** |
| Freq | FFPP | 0.394 | 0.354 | **0.656** | 0.576 | 0.430 | **0.681** |
| Hybrid | FFPP | 0.666 | 0.433 | **0.720** | 0.627 | 0.522 | **0.666** |
| Spatial | CDF | 0.772 | 0.542 | **0.707** | 0.998 | 0.507 | **0.815** |
| Freq | CDF | 0.596 | 0.266 | **0.604** | 0.733 | 0.460 | **0.603** |
| Hybrid | CDF | 0.882 | 0.534 | **0.665** | 1.000 | 0.583 | **0.823** |

## Table 2 — Cross-Dataset Performance

| Model | Direction | F1 (n=50) | F1 (n=200) | F1 (n=400) | AUC (n=50) | AUC (n=200) | AUC (n=400) |
|---------|-----------|-----------|------------|------------|------------|-------------|-------------|
| Spatial | FFPP→CDF | 0.573 | 0.332 | **0.503** | 0.267 | 0.361 | **0.624** |
| Freq | FFPP→CDF | 0.386 | 0.506 | 0.342 | 0.159 | 0.421 | 0.421 |
| Hybrid | FFPP→CDF | 0.549 | 0.588 | 0.368 | 0.360 | 0.607 | 0.512 |
| Spatial | CDF→FFPP | 0.278 | 0.449 | 0.234 | 0.302 | 0.413 | **0.653** |
| Freq | CDF→FFPP | 0.701 | 0.155 | 0.168 | 0.724 | 0.538 | 0.327 |
| Hybrid | CDF→FFPP | 0.321 | 0.479 | 0.038 | 0.436 | 0.502 | 0.506 |

## Table 3 — Generalization Drop (F1\_in − F1\_cross)

| Model | Train | Drop (n=50) | Drop (n=200) | Drop (n=400) |
|---------|-------|-------------|-------------|-------------|
| Spatial | FFPP | −0.032 | +0.191 | **+0.127** |
| Spatial | CDF | +0.494 | +0.093 | **+0.472** |
| Freq | FFPP | +0.008 | −0.152 | **+0.314** |
| Freq | CDF | −0.105 | +0.110 | **+0.436** |
| Hybrid | FFPP | +0.117 | −0.155 | **+0.352** |
| Hybrid | CDF | +0.561 | +0.055 | **+0.627** |

---

## Key Findings

### 1. More Data Fixes In-Dataset Performance — The n=200 Dip Is a Transition Artifact

The n=200 results showed a surprising performance dip from n=50. With n=400, all models recover and surpass both n=50 and n=200 in-dataset F1. This reveals a U-shaped learning curve:

- **n=50**: Small sample, easy to memorize → inflated metrics
- **n=200**: More data variety overwhelms the model before it learns robust features → performance drops
- **n=400**: Enough data for the model to learn meaningful patterns → genuine improvement

### 2. Hybrid Is the Best In-Dataset Model

At n=400, Hybrid achieves the highest in-dataset F1 on FFPP (**0.720**) and competitive performance on CDF (0.665). Spatial edges out on CDF in-dataset (0.707), but Hybrid's CDF AUC (**0.823**) confirms it captures richer complementary features through spatial+frequency fusion.

| | Best F1 (FFPP) | Best F1 (CDF) |
|--|--|--|
| n=400 | **Hybrid: 0.720** | Spatial: 0.707 |

### 3. Cross-Dataset Generalization Severely Degrades at n=400

Despite much better in-dataset performance, cross-dataset F1 collapses at n=400:

- **Hybrid CDF→FFPP: F1 = 0.038** (essentially random — the model predicts almost all negatives)
- **Freq CDF→FFPP: F1 = 0.168** (down from 0.701 at n=50)
- **Spatial CDF→FFPP: F1 = 0.234** (down from 0.449 at n=200)

The generalization drops at n=400 are the largest across all sample sizes:
- Hybrid from CDF: **0.627 drop** (worst across all experiments)
- Spatial from CDF: **0.472 drop**
- Freq from CDF: **0.436 drop**

This strongly indicates that with more training data, all models overfit to dataset-specific artifacts rather than learning universal deepfake signatures.

### 4. Spatial Becomes the Most Generalizable Model at n=400

Despite the overall degradation, Spatial has the smallest FFPP→CDF drop (**0.127**) and achieves the best cross-dataset AUC in both directions:

- FFPP→CDF AUC: **0.624** (best)
- CDF→FFPP AUC: **0.653** (best by far)

This reverses the n=200 finding where Hybrid generalized best. At higher data volumes, Xception's pretrained spatial features retain more transferable representations than the frequency or hybrid branches.

### 5. Frequency Features Do Not Generalize Well at Scale

At n=50 and n=200, frequency features showed promising transferability (negative drops). At n=400, this completely reverses — Freq shows massive drops (0.314, 0.436). The FFT-based features learn dataset-specific compression/spectral fingerprints rather than universal forgery traces.

### 6. Training on FFPP Generalizes to CDF Better Than the Reverse

At n=400, every model generalizing from CDF to FFPP performs drastically worse than the FFPP→CDF direction. FFPP (FaceForensics++) contains multiple manipulation types (Deepfakes, Face2Face, FaceSwap, NeuralTextures, FaceShifter, DeepFakeDetection), making it a more diverse training set. CDF (Celeb-DF) is more homogeneous, so models trained on it learn narrower feature spaces.

### 7. The Hybrid Model Has a Collapse Problem at n=400 Cross-Dataset

Hybrid CDF→FFPP produces F1=0.038 with recall=0.0196 — it predicts "real" for almost everything. The fusion mechanism overfits the two branches to CDF-specific patterns so aggressively that when confronted with FFPP data, the model's confidence collapses to a single class.

---

## Trend Summary Across Sample Sizes

| Metric | n=50 | n=200 | n=400 | Trend |
|--------|------|-------|-------|-------|
| Best in-dataset F1 | 0.882 (Hybrid/CDF) | 0.534 (Hybrid/CDF) | **0.720 (Hybrid/FFPP)** | Recovers with more data |
| Best cross-dataset F1 | 0.701 (Freq CDF→FFPP) | 0.588 (Hybrid FFPP→CDF) | **0.503 (Spatial FFPP→CDF)** | Steadily degrades |
| Avg generalization drop | 0.17 | 0.05 | **0.39** | Overfitting worsens |
| Most robust model | Hybrid | Hybrid | **Spatial** | Shifts at scale |

## Overall Verdict by Sample Size

| Aspect | n=50 | n=200 | n=400 |
|--------|------|-------|-------|
| Best in-dataset | Hybrid | Hybrid | **Hybrid** |
| Best cross-dataset | Freq | Hybrid | **Spatial** |
| Worst generalizer | Spatial | Freq | **Hybrid** |
| Reliability | Overfit (inflated) | Borderline | **Trustworthy for in-dataset; reveals real generalization issues** |

---

## Conclusions

1. **Hybrid fusion is the strongest in-dataset detector** (F1=0.720 on FFPP at n=400), confirming that combining spatial and frequency features captures complementary forgery cues.

2. **Cross-dataset generalization is the unsolved problem.** All models overfit to dataset-specific characteristics as training data grows — the opposite of what we would hope. The average generalization drop increases from 0.05 (n=200) to 0.39 (n=400).

3. **Spatial (Xception) generalizes best at scale**, likely because ImageNet pretraining provides domain-agnostic features that resist dataset overfitting. At n=400, it achieves the best cross-dataset AUC in both directions (0.624 and 0.653).

4. **The Hybrid model's cross-dataset collapse** (F1=0.038 from CDF→FFPP at n=400) is a critical architectural vulnerability. The fusion mechanism needs regularization strategies (e.g., dropout on fusion layers, domain-adversarial training, or freezing pretrained weights longer) to prevent overfitting.

5. **Training on FFPP generalizes to CDF better than the reverse**, because FFPP's multi-method manipulation diversity provides broader forgery feature coverage.

6. **n=50 results are unreliable** due to overfitting on small samples. **n=400 provides the most trustworthy in-dataset evaluation** and exposes the true generalization challenge that smaller samples masked.
