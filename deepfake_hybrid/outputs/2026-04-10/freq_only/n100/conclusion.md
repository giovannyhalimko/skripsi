# Analysis: Freq Model with High-Pass FFT (n=100)

Date: 2026-04-10
Config: seed=42, LR=2e-4, warmup=2, patience=10, freq_depth=5, freq_base_channels=64
Change: Added Gaussian high-pass filter to FFT (cutoff=5%), increased freq model capacity (32→64 base channels, ~2.8M params)

---

## Training Results

| Metric        | Before (no high-pass, 32ch) | After (high-pass, 64ch) |
|---------------|----------------------------|-------------------------|
| Best val AUC  | 0.634 (but test=0.256, INVERTED) | **0.623** (stable)  |
| Training epochs | 7 (early stop)           | **27** (early stop)     |
| Loss trend    | 0.67 → 0.53 (unstable)    | 0.67 → 0.35 (clean)    |
| Val F1        | Collapsed to 0.0           | Oscillates 0.01–0.68   |

## Epoch-by-Epoch Val AUC

```
Epoch  1: 0.518    Epoch 10: 0.571    Epoch 19: 0.603
Epoch  2: 0.502    Epoch 11: 0.564    Epoch 20: 0.601
Epoch  3: 0.501    Epoch 12: 0.578    Epoch 21: 0.598
Epoch  4: 0.511    Epoch 13: 0.577    Epoch 22: 0.623 ← best
Epoch  5: 0.509    Epoch 14: 0.587    Epoch 23: 0.599
Epoch  6: 0.521    Epoch 15: 0.597    Epoch 24: 0.610
Epoch  7: 0.525    Epoch 16: 0.574    Epoch 25: 0.613
Epoch  8: 0.536    Epoch 17: 0.567    Epoch 26: 0.597
Epoch  9: 0.559    Epoch 18: 0.589    Epoch 27: 0.608
```

## Key Observations

1. **Training is stable now** — no inversion, no collapse. The high-pass filter fixed the catastrophic failure (0.256 test AUC → now learning properly).

2. **Val AUC climbs slowly but steadily** — 0.518 → 0.623 over 27 epochs. The model IS learning frequency-domain features from cropped faces.

3. **Still significantly below spatial** — spatial achieves 0.798 val AUC on the same data. The freq model at 0.623 is ~0.175 behind.

4. **Val F1 is unstable** — oscillates between 0.01 and 0.68 across epochs, suggesting the decision boundary is fragile. The model learns ranking (AUC) but struggles with a fixed threshold.

5. **Loss drops cleanly** — 0.67 → 0.35, showing the model fits training data well. The gap between train loss and val AUC suggests the model needs better generalization, not more capacity.

## What the high-pass filter fixed

- **Before**: FFT dominated by low frequencies (skin brightness, face shape) → model latched onto these → different val/test distributions caused inversion
- **After**: Low frequencies attenuated → model forced to use high-frequency patterns (manipulation artifacts, blending boundaries) → more stable learning

## What still needs improvement

Target: 0.75–0.80 val AUC to make freq a meaningful contributor to the hybrid model.

Potential directions:
- Training improvements (LR, augmentation, regularization)
- Architecture changes (attention, multi-scale)
- Input representation (multi-channel FFT, DCT instead of FFT)
- Better normalization of FFT features
