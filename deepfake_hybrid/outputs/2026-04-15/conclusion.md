# Experiment Conclusion — 2026-04-15

## Overview

Single sample-size run at **n=500** for the full 3-model × 2-dataset matrix (spatial, freq, hybrid × FFPP, CDF). Trained on Kaggle (`/kaggle/outputs/`). The previous comparable matrix was 2026-04-05 at n=250, so this is the doubled-data follow-up.

---

## 1. In-Dataset Performance (n=500)

| Model | Dataset | Test Acc | Test F1 | Test AUC | Best Val AUC | Epochs |
|-------|---------|----------|---------|----------|--------------|--------|
| spatial | FFPP | 0.694 | 0.671 | **0.749** | 0.726 | 21 (early-stop) |
| freq    | FFPP | 0.486 | 0.623 | 0.531 | 0.674 | 15 (early-stop) |
| hybrid  | FFPP | 0.551 | **0.497** | **0.555** | 0.622 | **6 (early-stop)** |
| spatial | CDF  | **0.861** | **0.861** | **0.923** | 0.948 | 13 (early-stop) |
| freq    | CDF  | 0.578 | 0.595 | 0.625 | 0.597 | 10 (early-stop) |
| hybrid  | CDF  | 0.756 | 0.740 | 0.808 | 0.865 | 14 (early-stop) |

### Comparison vs n=250 (2026-04-05)

| Model | Dataset | F1 (n=250) | F1 (n=500) | AUC (n=250) | AUC (n=500) | Δ AUC |
|-------|---------|-----------|------------|-------------|-------------|-------|
| spatial | FFPP | 0.588 | 0.671 | 0.552 | 0.749 | **+0.197** |
| freq    | FFPP | 0.591 | 0.623 | 0.723 | 0.531 | **−0.192** |
| hybrid  | FFPP | 0.565 | 0.497 | 0.563 | 0.555 | −0.008 |
| spatial | CDF  | 0.648 | 0.861 | 0.684 | 0.923 | **+0.239** |
| freq    | CDF  | 0.553 | 0.595 | 0.578 | 0.625 | +0.047 |
| hybrid  | CDF  | 0.540 | 0.740 | 0.575 | 0.808 | **+0.233** |

- **Spatial scaled cleanly with data** on both datasets — the largest gains in the run.
- **Hybrid scaled on CDF** (+0.23 AUC) but **stalled on FFPP**. This is the central anomaly.
- **Freq FFPP regressed in AUC** (0.72 → 0.53) despite F1 going up, indicating threshold/calibration drift, not skill loss alone.

---

## 2. Cross-Dataset Performance (n=500)

| Train | Test | Model | F1 | AUC |
|-------|------|-------|------|------|
| FFPP | CDF | spatial | 0.523 | 0.712 |
| FFPP | CDF | freq    | **0.633** | 0.582 |
| FFPP | CDF | hybrid  | 0.404 | 0.552 |
| CDF  | FFPP | spatial | **0.072** | 0.593 |
| CDF  | FFPP | freq    | **0.611** | 0.592 |
| CDF  | FFPP | hybrid  | 0.157 | 0.557 |

- **CDF → FFPP collapses for spatial**: 109 TP vs 2778 FN — the model predicts almost everything as "real". CDF spatial features overfit to identity/background, not manipulation cues.
- **Hybrid no longer wins cross-dataset** (it did at n=100 in 2026-04-03). The fusion does not propagate the freq branch's dataset-invariance.
- **Freq is the only model that holds up cross-dataset**, both directions, because it has no spatial bias to overfit to.

---

## 3. Generalization Drop (n=500)

| Model | Train | F1 in | F1 cross | Drop |
|-------|-------|-------|----------|------|
| spatial | FFPP | 0.671 | 0.523 | +0.148 |
| spatial | CDF  | 0.861 | 0.072 | **+0.789** |
| freq    | FFPP | 0.623 | 0.633 | −0.010 |
| freq    | CDF  | 0.595 | 0.611 | −0.015 |
| hybrid  | FFPP | 0.497 | 0.404 | +0.093 |
| hybrid  | CDF  | 0.740 | 0.157 | **+0.583** |

- Freq generalizes essentially without loss (negative drops mean cross-test was *better* than in-test).
- Spatial CDF→FFPP and hybrid CDF→FFPP both collapse — same root cause (CDF identity overfit propagates through hybrid fusion).

---

## 4. Diagnostic Findings

### 4.1 Hybrid FFPP plateaus immediately

`runs/hybrid_FFPP_n500_seed0/train.log`:

```
Epoch 1: loss=0.6770, val_auc=0.6218, val_f1=0.4827   ← peak
Epoch 2: loss=0.5013, val_auc=0.5233
Epoch 3: loss=0.3085, val_auc=0.5092
Epoch 4: loss=0.2150, val_auc=0.5128   ← unfreeze
Epoch 5: loss=0.1645, val_auc=0.5876
Epoch 6: loss=0.1495, val_auc=0.5941   ← early-stop
```

Train loss collapses 0.68 → 0.15 (**−78%**) while val AUC stays in the 0.5–0.6 band. This is textbook overfitting on a small training pool (350 frames, balanced 175/175). Best val AUC was epoch 1 — the model never improved on its near-random initialization. Patience=5 fired right after the unfreeze transition, killing training before fine-tuning could converge.

### 4.2 Freq FFPP val F1 is unstable

```
Epoch 7: val_auc=0.4482, val_f1=0.0021   ← collapses to one class
Epoch 8: val_auc=0.6396, val_f1=0.6628
Epoch 9: val_auc=0.6126, val_f1=0.0000   ← collapses again
Epoch 10: val_auc=0.6744, val_f1=0.6835
Epoch 11: val_auc=0.6693, val_f1=0.0867
```

AUC is reasonable but F1 oscillates between near-zero and 0.69 across consecutive epochs — the operating point at threshold=0.5 is not stable. The freq head's logit distribution is shifting epoch-to-epoch, so a fixed threshold is meaningless.

### 4.3 LR mismatch in hybrid

For hybrid, the spatial backbone trains at 2e-5 (post-unfreeze) while the freq branch + fusion head train at 2e-4 — a 10× gap. The freq branch is randomly initialized but gets the head's full LR. This likely lets the freq branch overfit fast and dominate fusion gradients before the spatial branch contributes, especially on FFPP where freq signal is weaker.

### 4.4 CDF → FFPP spatial bias

`run_all_n500.log` DIAG line: `mean_prob_for_real=0.0529, mean_prob_for_fake=0.0923`. CDF-trained spatial pushes essentially all FFPP samples toward 0 — it learned CDF identity statistics, not manipulation features. This propagates to hybrid (DIAG: `mean_prob_for_real=0.1239, mean_prob_for_fake=0.1558`), confirming the spatial branch dominates hybrid fusion at test time.

---

## 5. Key Takeaways

1. **Spatial is the best in-dataset model** at n=500, but worst-generalizing from CDF.
2. **Hybrid fusion is broken on FFPP.** Adding the freq branch hurts vs spatial-only (AUC 0.749 → 0.555). The fusion head is not gating signal correctly on FFPP and the unfreeze + patience schedule kills training too early.
3. **Freq is the only cross-dataset-stable model** (drop ≈ 0 both directions), but its absolute scores are weak and its threshold is unstable.
4. **CDF spatial features do not transfer.** Identity/background overfit dominates manipulation cues, and hybrid inherits this bias instead of correcting it via the freq branch.
5. **Doubling data (n=250 → n=500) helps spatial and helps hybrid on CDF**, but does not rescue hybrid FFPP — the issue is architectural/scheduling, not data volume.

---

## 6. Improvement Targets (for next iteration)

Ranked by likely impact:

1. **Hybrid LR rebalance** — drop freq-branch / fusion-head LR closer to backbone (e.g. 5e-5), not 2e-4. Stops the freq branch from overfitting first.
2. **Patience increase** — 5 → 8 or 10, especially across the unfreeze epoch boundary so hybrid doesn't early-stop right after backbone unfreezing.
3. **Threshold tuning on val** — pick the F1-optimal threshold per model and report metrics at that operating point. Will fix freq's F1 instability.
4. **Stronger regularization on hybrid head** — dropout in SE/fusion + higher label smoothing (0.02 → 0.05–0.1). Train loss → 0.15 with val ≈ 0.5 is overfit signal.
5. **Freq branch warm-start** — pretrain freq alone for 2–3 epochs before fusion training, so the fusion head starts with a non-random freq embedding.
6. **Augmentation for CDF spatial overfit** — color jitter, JPEG compression, random crops to break identity overfit on CDF. May rescue CDF → FFPP transfer.
7. **Re-verify FFT cache stats** — rerun `compute_fft_cache.py --stats` for both datasets; freq FFPP regression vs n=250 suggests possible cache/normalization drift.
8. **Scale to n=750 / n=1000** — only after fixing the hybrid schedule, otherwise we're scaling a broken trainer.
