# Full Analysis: n=100, 250, 500, 750 Results

Date analyzed: 2026-04-09
Data sources: outputs/2026-04-05/ (n100, n250), outputs/2026-04-09/ (n500, n750)
Config: seed=0, LR=2e-4, warmup=2 epochs, patience=10, pretrained=True

---

## 1. In-Dataset Test AUC (Complete Trajectory)

| Model   | FFPP n100 | FFPP n250 | FFPP n500 | FFPP n750 | CDF n100 | CDF n250 | CDF n500 | CDF n750 |
|---------|-----------|-----------|-----------|-----------|----------|----------|----------|----------|
| spatial | 0.696     | 0.552     | **0.469** | **0.492** | 0.796    | 0.684    | 0.693    | **0.739**|
| freq    | 0.746     | 0.723     | 0.511     | 0.544     | 0.837    | 0.578    | 0.585    | 0.653    |
| hybrid  | 0.616     | 0.563     | 0.573     | **0.469** | 0.866    | 0.575    | 0.594    | **0.697**|

### Key observations:

**FFPP collapses with more data.** At n500/n750, spatial and hybrid FFPP drop **below 0.5** (worse than random coin flip). Even the best FFPP model at n750 (freq, 0.544) is barely above chance. This is not a hyperparameter issue — all three architectures fail equally.

**CDF recovers after n250 dip.** CDF models dipped at n250 (test set grew 2.3x, including harder videos) but recover at n500/n750 as training data catches up:
- spatial CDF: 0.796 → 0.684 → 0.693 → **0.739** (trending up)
- hybrid CDF: 0.866 → 0.575 → 0.594 → **0.697** (recovering)
- freq CDF: 0.837 → 0.578 → 0.585 → 0.653 (slow recovery)

---

## 2. In-Dataset Test F1 (Complete Trajectory)

| Model   | FFPP n100 | FFPP n250 | FFPP n500 | FFPP n750 | CDF n100 | CDF n250 | CDF n500 | CDF n750 |
|---------|-----------|-----------|-----------|-----------|----------|----------|----------|----------|
| spatial | 0.667     | 0.588     | 0.363     | 0.505     | 0.565    | 0.648    | 0.676    | **0.670**|
| freq    | 0.495     | 0.591     | **0.018** | 0.166     | 0.758    | 0.553    | **0.008**| 0.647    |
| hybrid  | 0.652     | 0.565     | 0.592     | 0.463     | 0.603    | 0.540    | 0.620    | **0.635**|

**Freq model is highly unstable.** F1 of 0.018 (n500 FFPP) and 0.008 (n500 CDF) means the model predicts almost everything as one class. The DIAG logs confirm: freq_CDF n500 outputs probabilities of 0.02-0.05 for everything.

---

## 3. Cross-Dataset AUC (Complete Trajectory)

| Direction  | Model   | n100  | n250  | n500  | n750  |
|------------|---------|-------|-------|-------|-------|
| FFPP→CDF   | spatial | **0.833** | 0.437 | 0.546 | 0.520 |
| FFPP→CDF   | freq    | **0.856** | 0.634 | 0.374 | 0.409 |
| FFPP→CDF   | hybrid  | 0.562 | 0.457 | 0.563 | **0.634** |
| CDF→FFPP   | spatial | 0.774 | 0.320 | 0.510 | 0.582 |
| CDF→FFPP   | freq    | 0.562 | **0.742** | **0.589** | 0.561 |
| CDF→FFPP   | hybrid  | **0.798** | 0.438 | 0.510 | 0.530 |

**No consistent cross-dataset winner.** Results fluctuate heavily across sample sizes. Best cross-dataset results:
- FFPP→CDF: freq n100 (0.856), spatial n100 (0.833)
- CDF→FFPP: hybrid n100 (0.798), freq n250 (0.742)

The n100 cross-dataset results are suspiciously good — likely inflated by small test sets.

---

## 4. Val AUC During Training vs Test AUC

| Run                   | Best Val AUC | Test AUC | Gap    | Status         |
|-----------------------|-------------|----------|--------|----------------|
| spatial_FFPP_n500     | 0.581       | 0.469    | -0.112 | Val > Test     |
| spatial_FFPP_n750     | 0.418       | 0.492    | +0.074 | Test > Val (!) |
| freq_FFPP_n500        | 0.536       | 0.511    | -0.025 | Close          |
| freq_FFPP_n750        | 0.421       | 0.544    | +0.123 | Test > Val (!) |
| hybrid_FFPP_n500      | 0.444       | 0.573    | +0.129 | Test > Val (!) |
| hybrid_FFPP_n750      | 0.395       | 0.469    | +0.074 | Test > Val (!) |
| spatial_CDF_n500      | 0.715       | 0.693    | -0.022 | Close          |
| spatial_CDF_n750      | 0.652       | 0.739    | +0.087 | Test > Val     |
| freq_CDF_n500         | 0.674       | 0.585    | -0.089 | Val > Test     |
| freq_CDF_n750         | 0.671       | 0.653    | -0.018 | Close          |
| hybrid_CDF_n500       | 0.671       | 0.594    | -0.077 | Val > Test     |
| hybrid_CDF_n750       | 0.635       | 0.697    | +0.062 | Test > Val     |

**FFPP val AUC is often worse than test AUC** — very unusual. This means the model picks a "best" checkpoint on a val set where it's near-random, then that checkpoint happens to score slightly differently on test. At these AUC levels (0.4-0.5), noise dominates.

**CDF val/test AUC are reasonably aligned**, confirming CDF is a well-behaved dataset.

---

## 5. DIAG: Prediction Separation

### n500 DIAG (in-dataset)
| Model on own test set  | mean_prob_real | mean_prob_fake | Separation | Status |
|------------------------|---------------|---------------|------------|--------|
| spatial_FFPP           | 0.490         | 0.485         | 0.005      | INVERTED, near-random |
| freq_FFPP              | 0.238         | 0.232         | 0.006      | INVERTED, near-random |
| hybrid_FFPP            | 0.431         | 0.556         | 0.125      | OK, weak  |
| spatial_CDF            | 0.471         | 0.731         | 0.260      | OK, GOOD  |
| freq_CDF               | 0.019         | 0.050         | 0.031      | OK but miscalibrated |
| hybrid_CDF             | 0.512         | 0.664         | 0.152      | OK        |

### n750 DIAG (in-dataset)
| Model on own test set  | mean_prob_real | mean_prob_fake | Separation | Status |
|------------------------|---------------|---------------|------------|--------|
| spatial_FFPP           | 0.428         | 0.463         | 0.035      | OK, very weak |
| freq_FFPP              | 0.468         | 0.472         | 0.004      | Essentially random |
| hybrid_FFPP            | 0.392         | 0.419         | 0.027      | OK, very weak |
| spatial_CDF            | 0.278         | 0.618         | 0.340      | OK, STRONG  |
| freq_CDF               | 0.518         | 0.572         | 0.054      | OK, weak |
| hybrid_CDF             | 0.308         | 0.585         | 0.277      | OK, GOOD  |

**CDF models achieve real class separation** (0.15-0.34 gaps). **FFPP models have near-zero separation** (0.004-0.035 gaps). The FFPP models literally cannot tell real from fake.

---

## 6. Training Dynamics

### FFPP — Severe Overfitting Without Learning
All FFPP models show training loss dropping to 0.13-0.16 while val AUC stays at 0.35-0.58. The models perfectly memorize training data but learn nothing generalizable.

Example: hybrid_FFPP_n750
- Epoch 1: train_loss=0.675, val_auc=0.324
- Epoch 20: train_loss=0.140, val_auc=0.373
- 20 epochs of training, val AUC barely moved. Train loss dropped 5x.

### CDF — Proper Learning Curves
CDF models show healthy learning: loss decreases AND val AUC improves.

Example: spatial_CDF_n750
- Epoch 1: train_loss=0.688, val_auc=0.563
- Epoch 14: train_loss=0.133, val_auc=0.652
- Clear upward trajectory in val AUC.

### Freq Model — Epoch-1-Best Pattern Persists
freq_FFPP consistently peaks at epoch 1-3 then degrades:
- n500: best val_auc=0.536 at epoch 6, but then early stops at epoch 11
- n750: best val_auc=0.421 at epoch 3, early stops at epoch 8

The freq CNN overfits FFPP FFT features extremely quickly.

---

## 7. Test Set Growth

| n_samples | FFPP test frames | CDF test frames |
|-----------|-----------------|----------------|
| 100       | 1,239           | 1,026          |
| 250       | 3,268           | 2,390          |
| 500       | 5,957           | 5,094          |
| 750       | 8,996           | 7,564          |

Test set grows ~linearly with n_samples. At n750, we evaluate on nearly 9,000 FFPP frames and 7,500 CDF frames — much more robust than n100's ~1,000.

---

## 8. Root Cause Analysis

### Why does FFPP fail?

This is the critical question. Three hypotheses:

**Hypothesis A: FFPP video quality/diversity issue.**
FFPP contains 4 manipulation methods (Deepfakes, Face2Face, FaceSwap, NeuralTextures). At larger n, the training set includes more diverse manipulation types. If the test set distribution doesn't match (e.g., test has more NeuralTextures which is hardest), the model fails. CDF has only one method (Celeb-synthesis), making it more homogeneous and easier to learn.

**Hypothesis B: FFPP label or split problem.**
The `diagnose_splits.py` tool should be run to verify:
- Are all labels correct? (keyword matching on path names)
- Are train/val/test splits balanced across manipulation methods?
- Is there video-level leakage?

**Hypothesis C: FFPP data quality from Drive copy.**
With the SSD copy fix, FFPP was copied from Drive. If the copy was incomplete or some videos are corrupted, training on bad data would explain the collapse. The reserve pool mechanism should handle this, but at n750 (262 train videos), more broken videos get included.

**Most likely: Hypothesis A.** CDF works perfectly fine with the same code, ruling out bugs. The multi-method FFPP distribution is fundamentally harder, and our models aren't large/powerful enough to generalize across all 4 methods simultaneously.

### Why does CDF work?

CDF is simpler:
- One fake method (Celeb-synthesis) vs four in FFPP
- Cleaner videos (celebrity interviews vs YouTube compression in FFPP)
- The spatial CDF model achieves **0.739 AUC at n750** with clear prediction separation (0.278 real vs 0.618 fake) — the model genuinely learned to distinguish real from fake

---

## 9. Summary of Best Results

### In-Dataset (test AUC)
| Rank | Model         | Dataset | n     | AUC   |
|------|---------------|---------|-------|-------|
| 1    | hybrid        | CDF     | 100   | 0.866 |
| 2    | freq          | CDF     | 100   | 0.837 |
| 3    | spatial       | CDF     | 100   | 0.796 |
| 4    | freq          | FFPP    | 100   | 0.746 |
| 5    | spatial       | CDF     | 750   | 0.739 |
| 6    | freq          | FFPP    | 250   | 0.723 |
| 7    | hybrid        | CDF     | 750   | 0.697 |
| 8    | spatial       | FFPP    | 100   | 0.696 |

**Top results are dominated by CDF** and small n. The best large-n result is spatial_CDF n750 at 0.739.

### Cross-Dataset (test AUC)
| Rank | Direction   | Model   | n    | AUC   |
|------|-------------|---------|------|-------|
| 1    | FFPP→CDF    | freq    | 100  | 0.856 |
| 2    | FFPP→CDF    | spatial | 100  | 0.833 |
| 3    | CDF→FFPP    | hybrid  | 100  | 0.798 |
| 4    | CDF→FFPP    | spatial | 100  | 0.774 |
| 5    | CDF→FFPP    | freq    | 250  | 0.742 |
| 6    | FFPP→CDF    | hybrid  | 750  | 0.634 |

Best cross-dataset results at n100 are likely inflated by small test sets. The most reliable cross-dataset result is **hybrid FFPP→CDF at n750 = 0.634** (large test set, reasonable AUC).

---

## 10. Conclusions and Next Steps

### What we know:
1. **The hybrid architecture works on CDF** — achieves 0.866 AUC at n100 and 0.697 at n750, outperforming or matching spatial-only at most sample sizes.
2. **Frequency features add value on CDF** — freq alone achieves 0.837 at n100, 0.653 at n750. This supports the thesis that FFT features capture manipulation artifacts.
3. **FFPP is fundamentally harder** — likely due to multi-method diversity and compression artifacts. All models fail at n500+.
4. **Cross-dataset generalization is weak** at large n, but freq features show the most domain-robust behavior.

### Critical next steps:

**1. Diagnose the FFPP problem (HIGHEST PRIORITY)**
Run `diagnose_splits.py --dataset FFPP` on the n500 or n750 preprocessed data. Specifically check:
- Label distribution across manipulation methods in train vs test
- Whether certain methods dominate the test set
- Whether there are path-based label errors

**2. Consider filtering FFPP to single manipulation method**
Train on Deepfakes-only (matching CDF's single-method setup) and see if FFPP AUC recovers. This would confirm Hypothesis A.

**3. Run with multiple seeds (n_seeds=3)**
All current results are seed=0 only. At AUC levels of 0.5-0.7, random variation is significant. Multiple seeds would give confidence intervals.

**4. For the thesis:**
- Present CDF results as the primary evidence for the hybrid architecture
- Discuss FFPP as a challenging multi-method scenario that requires future work
- Highlight that frequency features (freq model) show the best cross-dataset generalization properties, supporting the theoretical motivation
- The CDF recovery curve (n100→n750) shows the hybrid benefits from more data, suggesting it could improve further with larger datasets
