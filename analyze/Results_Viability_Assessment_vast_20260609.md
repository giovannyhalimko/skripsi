# Results Viability Assessment — `results_vast_20260609`

**Date:** 2026-06-09
**Question:** Are these results good enough for an undergraduate (S1) thesis?
**Source:** `deepfake_hybrid/results_vast_20260609/tables/{n100,n250,n500,n750}/`
**Setup:** 3 models (spatial = XceptionNet baseline, freq = FFT-CNN, hybrid = proposed) × 2 datasets (FFPP, CDF) × in-dataset + cross-dataset × 4 sample-size tiers × 3 seeds (0,1,2).

> **Reliability note:** n100 test splits are ~15 videos, so their AUC/F1 are sampling noise. This assessment is based on the reliable tiers **n250 / n500 / n750**.

---

## Headline: in-dataset AUC (mean over 3 seeds)

| Tier | Dataset | spatial (baseline) | **hybrid (proposed)** | freq |
|------|---------|--------:|--------:|-----:|
| n750 | CDF  | **0.969** | 0.924 | 0.586 |
| n750 | FFPP | **0.780** | 0.650 | 0.546 |
| n500 | CDF  | **0.967** | 0.892 | 0.615 |
| n500 | FFPP | **0.693** | 0.582 | 0.570 |
| n250 | CDF  | **0.942** | 0.812 | 0.569 |
| n250 | FFPP | **0.746** | 0.542 | 0.480 |

In-dataset F1 follows the same ordering (e.g. n750 FFPP: spatial 0.710 > hybrid 0.603 > freq 0.529; n750 CDF: spatial 0.909 > hybrid 0.847 > freq 0.511).

---

## Verdict (two parts)

### 1. The experimental work is more than rigorous enough for an S1 thesis
- 3 models × 2 datasets × in-dataset + cross-dataset × 4 sample-size tiers × 3 seeds.
- Video-level splits (no frame leakage), std reported, full AUC / F1 / precision / recall.
- Includes a scaling study and a generalization-drop analysis.
- This design is **stronger than most undergraduate theses**. Mechanically, the effort is publishable-quality.

### 2. But the scientific result is negative
**The proposed hybrid loses to the plain XceptionNet baseline at every reliable tier, on both datasets, on both AUC and F1.**
- The frequency branch is essentially at chance (in-dataset AUC 0.55–0.59) and is **dragging the hybrid down** rather than helping.
- So the headline contribution — *"fusing frequency information improves detection"* — is **not supported by the data**.
- This is the single thing an examiner will zero in on.

---

## Is the negative result disqualifying? No — but framing decides everything

- ❌ **Framed as "we propose a hybrid that *improves* detection"** → results contradict the claim. An examiner will catch it; this framing fails.
- ✅ **Framed as "a comparative investigation into whether frequency-domain fusion helps XceptionNet, with an honest negative finding and root-cause analysis"** → completely legitimate, defensible undergraduate work. Negative results are valid science **if** the *why* is analyzed.

### Context on the absolute numbers (these are fine)
- FFPP is genuinely hard; a baseline AUC ~0.78 at n=750 videos is reasonable for a small-data regime.
- CDF baseline at ~0.97 is strong.
- Cross-dataset generalization is weak across **all** models (AUC ~0.55–0.70, with recall collapse in the CDF→FFPP direction, e.g. hybrid n250 CDF→FFPP: precision 0.94 / recall 0.08 / F1 0.15). This is a **known-hard** problem in the deepfake literature, not a flaw in the work.

---

## Recommended paths

### Path A — Reframe (low effort, safe, defensible today)
Keep the results; change the thesis narrative to a **comparative study + honest analysis of why the freq branch fails**. Candidate explanations to develop:
- FFT computed on **face-cropped, re-compressed** frames loses the GAN upsampling fingerprint.
- A near-chance branch **injects noise** into the fusion.
- The **SE (squeeze-excitation) gating never learns to suppress** the bad branch.

### Path B — Diagnose & try to fix (more effort, higher upside)
The freq branch sitting at chance is **suspicious** — it may be a training/normalization bug rather than a fundamental limitation. Worth checking before conceding the negative result:
- FFT normalization stats (`fft_stats.json`) loading correctly.
- Freq branch learning at all (loss curve / standalone trainability).
- Fusion strategy (e.g. freezing/pretraining the freq branch, gating regularization).

If fixable, the hybrid could flip to beating the baseline and restore the original "improvement" framing.

---

## Bottom line
The **methodology and execution clear the S1 bar comfortably.** The **finding is negative** (proposed > baseline does **not** hold). The thesis is viable either way — but the claims must be reframed around the negative result (Path A) unless the freq branch can be fixed (Path B).

---

### Related
- Memory: `hybrid-underperforms-spatial`, `small-tier-test-auc-is-noise`, `thesis-stage-and-colab-drift`
- Prior analysis: `analyze/Hybrid_Model_Collapse_Analysis_2026-03-14_1600.md`
- Fix logs: `documentation/hybrid_model_fixes_*.md`, `documentation/hybrid_training_fixes_2026-04-25.md`
