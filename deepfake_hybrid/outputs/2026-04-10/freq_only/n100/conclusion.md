# Analysis: Freq Model Tuning Results (n=100)

Date: 2026-04-10
Dataset: FFPP, face-cropped, n=100

---

## Comparison: Two Tuning Attempts

| Run    | High-pass cutoff | Spectral mask | Warmup | Best val AUC | Epochs |
|--------|-----------------|---------------|--------|-------------|--------|
| n100-1 | 0.05 (tight)    | 15%, h/8      | 2      | **0.623**   | 27     |
| n100-2 | 0.15 (wide)     | 5%, h/16      | 3      | 0.610       | 24     |

## Key Findings

1. **Widening the high-pass cutoff did not help** — 0.15 performed marginally worse than 0.05 (0.610 vs 0.623). The tighter cutoff that suppresses more low-frequency content may actually be better, forcing the model to focus purely on high-frequency artifacts.

2. **Reducing spectral masking did not help** — less augmentation didn't improve learning. The model isn't overfitting (train loss drops cleanly while val AUC plateaus), so reducing regularization had no effect.

3. **Longer warmup did not help** — 3-epoch warmup vs 2-epoch made no meaningful difference.

4. **The freq model has a ceiling at ~0.62 val AUC** with the current approach (single-channel FFT log-magnitude + custom CNN). This appears to be a fundamental limitation of the representation, not a tuning issue.

## Why Freq Plateaus at 0.62

The single-channel FFT log-magnitude of a face crop contains limited discriminative information for deepfake detection:
- Manipulation artifacts in the frequency domain are subtle (small spectral peaks, localized distortions)
- The log1p transform compresses the dynamic range, potentially hiding small high-frequency differences
- A CNN training from scratch on ~3,500 frames has insufficient data to learn these subtle patterns
- The spatial model (XceptionNet, pretrained on ImageNet) starts with 22M params of learned texture/edge features — the freq CNN starts with nothing

## Recommendation

**Accept freq at ~0.62 and proceed with the full pipeline.** The freq branch doesn't need to match spatial performance on its own. In the hybrid model, it just needs to contribute complementary information that spatial alone doesn't capture. A freq val AUC of 0.62 still indicates the model is learning *something* from the frequency domain — this signal, combined with spatial's 0.80, may produce a stronger hybrid.

Focus remaining compute on running spatial + freq + hybrid across all sample sizes (n=100, 250, 500, 750) with face cropping to get the complete thesis results.
