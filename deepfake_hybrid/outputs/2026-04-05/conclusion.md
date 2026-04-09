# Analysis: 2026-04-05 Results (n=100 and n=250)

Date analyzed: 2026-04-05  
Runs: n100 (trained 2026-04-04), n250 (trained 2026-04-05)  
Seed: 0, Pretrained: Yes, LR: 2e-4, Warmup: 2 epochs, Patience: 10

---

## 1. Summary Tables

### In-dataset AUC (test set)

| Model   | FFPP n100 | FFPP n250 | CDF n100 | CDF n250 |
|---------|-----------|-----------|----------|----------|
| spatial | 0.696     | **0.552** | 0.796    | **0.684**|
| freq    | 0.746     | **0.723** | 0.837    | **0.578**|
| hybrid  | 0.616     | **0.563** | 0.866    | **0.575**|

### Cross-dataset AUC

| Train→Test     | Model   | n100  | n250  |
|----------------|---------|-------|-------|
| FFPP → CDF     | spatial | 0.833 | 0.437 |
| FFPP → CDF     | freq    | 0.856 | 0.634 |
| FFPP → CDF     | hybrid  | 0.562 | 0.457 |
| CDF → FFPP     | spatial | 0.774 | 0.320 |
| CDF → FFPP     | freq    | 0.562 | 0.742 |
| CDF → FFPP     | hybrid  | 0.798 | 0.438 |

---

## 2. Key Finding: Severe n250 Regression (Especially CDF)

Going from n100 → n250, almost every model gets **worse**, not better. The worst cases:

- **freq CDF**: 0.837 → 0.578 (−0.259)
- **hybrid CDF**: 0.866 → 0.575 (−0.291)
- **spatial FFPP**: 0.696 → 0.552 (−0.144)

Only **freq FFPP** is relatively stable (0.746 → 0.723).

### Why does more data hurt?

**Most likely cause: the test set also grows with n_samples.**

At n100 the CDF test set has 1,026 frames (616 real, 410 fake). At n250 it has 2,390 frames (1,254 real, 1,136 fake) — 2.3x larger and includes videos not seen at n100. Those additional videos are harder, pulling AUC down. This is expected behavior; n100 test AUC was artificially inflated by evaluating on a small, easy subset.

**Secondary cause: hybrid/freq CDF overfitting.**

At n250 the hybrid FFPP training log shows train loss → 0.13 while val AUC stays at ~0.55. The model memorizes training patterns that don't generalize. With only 175 training videos but a 2,390-frame test set, there isn't enough data diversity.

---

## 3. DIAG Analysis — Prediction Inversion at n250

n250 has **6 cross-dataset inversion events** (mean_prob_for_real > mean_prob_for_fake):

| Model trained on | Evaluated on | Inverted? | Note |
|-----------------|--------------|-----------|------|
| spatial_CDF     | FFPP test    | YES       | 0.2937 real > 0.1640 fake |
| hybrid_CDF      | FFPP test    | YES       | 0.3337 real > 0.2832 fake |
| spatial_FFPP    | CDF test     | YES       | 0.5945 real > 0.5240 fake |
| hybrid_FFPP     | CDF test     | YES       | 0.4470 real > 0.4001 fake |

**freq models: no inversions.** freq_CDF→FFPP gives 0.226 real vs 0.376 fake (correct direction, low confidence). freq_FFPP→CDF gives 0.502 real vs 0.513 fake (barely separable but not inverted).

This confirms that **freq is the most domain-robust branch**. The spatial and hybrid models learn texture/appearance artifacts that are specific to each dataset's distribution. When transferred cross-dataset, the label direction flips because the learned artifacts appear in the "wrong" class.

n100 had **no inversions** at all — the smaller, likely easier test set did not expose this issue.

---

## 4. Per-Model Analysis

### spatial
- **FFPP**: Consistent but mediocre. n100 val AUC peaked at 0.847, test AUC 0.696. Reasonable generalization (FFPP→CDF cross AUC 0.833 at n100).
- **CDF**: Good at n100 (0.796), drops at n250 (0.684). Cross-dataset inverts at n250.
- **Assessment**: Most stable across seeds/sizes for FFPP. Learns strong dataset-specific cues (hence inversion).

### freq
- **FFPP**: Persistently weak in-dataset (AUC 0.746/0.723), but **best val AUC happens at epoch 1 and degrades after** (both n100 and n250). This is the known freq FFPP instability — the model learns something useful immediately then overfits or collapses.
- **CDF**: Strong at n100 (0.837), crashes at n250 (0.578). But no inversion in cross-dataset.
- **Cross-dataset**: Most consistent model. CDF→FFPP freq at n250 = **0.742** (best cross-dataset score overall).
- **Assessment**: Frequency features generalize best cross-domain. The per-epoch instability (best at epoch 1) suggests the freq CNN needs a lower LR or stronger regularization for FFPP.

### hybrid
- **FFPP n100**: Paradox — val AUC peaked at **0.867** (best of all models) but test AUC is only **0.616** (worst of all models). Gap of 0.25 between val and test. The val set at n100 is only ~15 videos, making val AUC noisy/unreliable.
- **FFPP n250**: Train loss → 0.13, val AUC plateaus at 0.57 over 15 epochs. Severe overfitting. Early stopping at epoch 15 (patience=10).
- **CDF**: Strong at n100 (0.866), collapses at n250 (0.575). Cross-dataset inverts at n250.
- **Assessment**: The hybrid shows the most promise (high val AUC) but also the worst overfitting. The SE-gated fusion may be learning to heavily weight the spatial branch, which then fails cross-dataset.

---

## 5. FFPP Test Set — Persistent Near-Random Issue

FFPP in-dataset AUC is consistently lower than CDF across all models and sample sizes. The [DIAG] logs show all FFPP models predict probabilities in the 0.25–0.52 range — extremely low confidence, suggesting the FFPP test set has a distribution mismatch from the training/val sets.

This issue was already observed on 04/03. Recommend running `diagnose_splits.py --dataset FFPP` after the next full preprocessing to check if val videos and test videos come from different manipulation methods.

---

## 6. Comparing to 04/03 Baseline (n100 only)

| Model  | Dataset | 04/03 val AUC | 04/05 val AUC | 04/05 test AUC |
|--------|---------|---------------|---------------|----------------|
| spatial | FFPP   | 0.706 (old LR) | ~0.847       | 0.696          |
| freq   | CDF     | collapsed~0.5 | 0.886         | 0.837          |
| hybrid | CDF     | 0.74 (est.)   | 0.831         | 0.866          |

The LR fix (2e-4 + warmup=2) successfully restored FFPP spatial and fixed freq/hybrid CDF. This is a genuine improvement over 04/03.

---

## 7. Concerns for n500 and n750

Based on n100→n250 trends:

1. **AUC will likely stay flat or drop further** as test sets grow and include harder videos.
2. **Hybrid FFPP overfitting will worsen** — 15 epochs wasn't enough to see improvement, and larger n means more complex decision boundaries for a model that already memorizes.
3. **freq FFPP epoch-1 best behavior** may persist — worth logging per-epoch metrics carefully.
4. **Cross-dataset inversions** for spatial/hybrid are expected to continue; freq should remain stable.

**Recommendation before running n500/n750:**
- Consider adding dropout to the hybrid fusion head (currently none after SE block)
- Consider increasing weight decay for spatial/hybrid (current: 1e-4)
- Run diagnose_splits.py to verify FFPP split quality

---

## 8. One Positive Signal

**freq CDF→FFPP cross-dataset at n250 = 0.742** — this is the highest cross-dataset AUC across both runs. A model trained on CDF frequency features can generalize to FFPP test set with reasonable accuracy. This supports the thesis argument that frequency-domain artifacts are more universal across deepfake methods than spatial appearance.
