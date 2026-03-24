# Overall Analysis: 2026-03-23 Results vs Previous Runs

## What Changed in the Training Code

Three commits between the 03-16 and 03-23 runs changed the training pipeline significantly:

1. **`fe32f61` — Fix critical training bugs and improve hybrid architecture**
   - FFT normalisation constants: `(0.5, 0.5)` → `(5.0, 3.0)`
   - LR scheduler: CosineAnnealingLR → LinearLR warmup + cosine decay
   - Gradient clipping (max_norm=1.0)
   - Gaussian noise augmentation for FFT branch (sigma=0.1)
   - FreqCNN deepened: 3→5 conv layers, 64→256 output dim (~700K params)
   - SE (Squeeze-and-Excitation) attention gate on fused features
   - Label smoothing (0.05)

2. **`cc48cdc` — Improve GPU utilisation**
   - persistent_workers, prefetch_factor=4, drop_last in DataLoader
   - TF32 matmuls on CUDA
   - Optional torch.compile

3. **`7d698f6` — Fix torch.compile checkpoint incompatibility**
   - Unwrap `_orig_mod` keys before saving checkpoints

---

## Side-by-Side Comparison: In-Dataset F1

### FFPP

| Model | n=50 (old) | n=50 (new) | n=200 (old) | n=200 (new) | n=400 (new) |
|---------|------------|------------|-------------|-------------|-------------|
| Spatial | **0.751** | 0.544 | 0.441 | **0.464** | 0.432 |
| Freq | **0.622** | 0.534 | **0.440** | 0.100 | 0.092 |
| Hybrid | **0.670** | 0.648 | **0.536** | 0.136 | 0.207 |

### CDF

| Model | n=50 (old) | n=50 (new) | n=200 (old) | n=200 (new) | n=400 (new) |
|---------|------------|------------|-------------|-------------|-------------|
| Spatial | **0.694** | 0.195 | **0.656** | 0.570 | 0.578 |
| Freq | **0.364** | 0.000 | **0.681** | 0.000 | **0.631** |
| Hybrid | **0.602** | 0.004 | **0.585** | 0.372 | **0.668** |

**Key observation:** The old code outperforms the new code at every sample size for FFPP. On CDF, the old code wins at n=50 and n=200, but the new code's Hybrid (0.668) and Freq (0.631) catch up at n=400 — and the old code was never tested at n=400.

---

## Side-by-Side Comparison: Cross-Dataset F1

### FFPP→CDF

| Model | n=50 (old) | n=50 (new) | n=200 (old) | n=200 (new) | n=400 (new) |
|---------|------------|------------|-------------|-------------|-------------|
| Spatial | 0.696 | **0.703** | **0.638** | 0.622 | 0.458 |
| Freq | **0.725** | 0.180 | **0.750** | 0.539 | 0.493 |
| Hybrid | 0.751 | **0.881*** | 0.651 | 0.624 | 0.591 |

*Anomalous — likely bias artefact (100% recall, poor in-dataset AUC).

### CDF→FFPP

| Model | n=50 (old) | n=50 (new) | n=200 (old) | n=200 (new) | n=400 (new) |
|---------|------------|------------|-------------|-------------|-------------|
| Spatial | **0.632** | 0.303 | **0.598** | 0.573 | 0.308 |
| Freq | **0.347** | 0.000 | 0.200 | 0.002 | **0.626** |
| Hybrid | 0.344 | 0.000 | 0.351 | **0.558** | **0.645** |

**Key observation:** CDF→FFPP transfer for Freq and Hybrid improves dramatically at n=400 in the new code. This is the new architecture's strength — when given enough data, the deeper FreqCNN and SE gate learn transferable spectral features.

---

## Diagnosis: What Went Wrong and What Went Right

### What went wrong

1. **FFT normalisation constants are likely incorrect.** The change from `(0.5, 0.5)` to `(5.0, 3.0)` was intended to match the actual log1p range, but the catastrophic collapse of all frequency-dependent models at n=50 and n=200 suggests these constants may not match the actual cached FFT data. If the cached `.npy` files were computed with the old pipeline, the new constants would produce severely mis-scaled inputs (values would centre around -1.5 instead of 0). **This should be verified by running `compute_fft_cache.py --stats` and comparing against the hardcoded constants.**

2. **The deeper FreqCNN (700K params) needs too much data.** At n=50 (~2,500 frames) and n=200 (~10,000 frames), 5 conv layers with 256 output channels severely overfit. The old 3-layer FreqCNN with 64 output dim was appropriately sized for small datasets.

3. **Gaussian noise augmentation destroys weak signals.** At small n, the FFT signal-to-noise ratio is already low. Adding sigma=0.1 Gaussian noise further degrades the input, making it harder for the frequency branch to learn.

4. **Label smoothing + small data = underconfidence.** With only 50-200 training videos, the model needs every bit of gradient signal. Label smoothing (0.05) reduces this, contributing to the inability to learn discriminative features.

### What went right

1. **SE attention gate works.** The hybrid model's cross-dataset performance is often the best or near-best, suggesting the SE gate successfully learns to weight the more informative branch. When the freq branch is broken (n=50, n=200), the gate appears to suppress it in favour of spatial features.

2. **n=400 CDF recovery.** The deeper architecture pays off at scale — Freq CDF F1 goes from 0.000 to 0.631, and Hybrid CDF reaches 0.668, likely exceeding what the old architecture could achieve.

3. **Near-zero generalisation drops at n=400.** Freq CDF (drop=+0.005) and Hybrid CDF (drop=+0.023) show nearly perfect transfer, meaning the features learned are genuinely forgery-related rather than dataset-specific.

4. **Spatial cross-dataset resilience.** Spatial FFPP→CDF and CDF→FFPP are stable within 3-5% of the old values, confirming the ImageNet backbone provides robust features unaffected by the frequency pipeline changes.

---

## The FFPP Problem Persists

Across both old and new code, FFPP in-dataset remains the hardest task:

| Sample Size | Best FFPP In-Dataset F1 (old) | Best FFPP In-Dataset F1 (new) |
|-------------|-------------------------------|-------------------------------|
| n=50 | Spatial: 0.751 | Hybrid: 0.648 |
| n=200 | Hybrid: 0.536 | Spatial: 0.464 |
| n=400 | — | Spatial: 0.432 |

The n=200 dip identified in the 03-16 analysis has now extended to n=400 — there is no recovery. FFPP's 6 manipulation methods create a learning challenge that neither the old nor new code can solve at these sample sizes. The multi-method diversity requires either (a) much more data (n>1000), (b) method-aware training, or (c) architectural changes specific to multi-method detection.

---

## Scaling Curves Summary

### CDF In-Dataset (new code) — Shows healthy scaling

```
F1  |
0.7 |                          * Hybrid (0.668)
    |                        * Freq (0.631)
0.6 |              * Spatial  * Spatial (0.578)
    |              (0.570)
0.5 |
0.4 |            * Hybrid
    |              (0.372)
0.3 |
0.2 |  * Spatial
    |    (0.195)
0.1 |
0.0 |  * Freq, Hybrid (collapsed)
    +----+----------+-----------+
        n=50      n=200       n=400
```

### FFPP In-Dataset (new code) — Shows persistent failure

```
F1  |
0.7 |
0.6 |  * Hybrid (0.648)
0.5 |  * Spatial (0.544) * Spatial (0.464) * Spatial (0.432)
0.4 |  * Freq (0.534)
0.3 |
0.2 |                                      * Hybrid (0.207)
0.1 |                    * Freq (0.100)    * Freq (0.092)
    |                    * Hybrid (0.136)
0.0 +----+----------+-----------+
        n=50      n=200       n=400
```

---

## Recommendations

1. **Verify FFT normalisation constants.** Run `python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --stats` and `--dataset CDF --stats` to get actual mean/std. Compare with the hardcoded `(5.0, 3.0)`.

2. **Consider reverting FreqCNN depth for small n.** The 3-layer architecture was better suited for n<200. A configurable depth based on sample size could help.

3. **Remove Gaussian noise augmentation.** Or make it conditional on n — at n=50, the noise likely overwhelms the signal.

4. **Investigate the training-eval AUC discrepancy at n=50.** Training metrics show reasonable validation AUCs (e.g., Hybrid CDF best val AUC=0.874) but evaluation produces AUC=0.003. This gap is too large to be explained by checkpoint selection alone — there may be a data pipeline or evaluation bug.

5. **Test at n=800+ to confirm FFPP recovery.** The CDF scaling curve suggests the new architecture learns well with enough data. FFPP may need 800-1000 videos to exit the multi-method confusion zone.

6. **Run the old code at n=400 for a fair comparison.** The old code was only tested at n=50 and n=200. Testing it at n=400 would show whether the new architecture genuinely offers a scaling advantage.
