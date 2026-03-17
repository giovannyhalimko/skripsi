# Code Improvements — Deepfake Hybrid Detection System

**Date:** 2026-03-17
**Scope:** Bug fixes, training stability, architecture improvements, optional enhancements
**Motivation:** Post-fix training runs (n=50 on 2026-03-15, n=200 on 2026-03-16) revealed catastrophic FFPP collapse, FreqCNN learning failures, and hybrid underperformance. This document details all code changes made.

---

## Summary of Changes

| Tier | Fix | Files Modified | Impact |
|------|-----|----------------|--------|
| 1A | FFT normalization constants | `src/deepfake_data.py`, `scripts/compute_fft_cache.py` | Critical — Freq AUC +0.05-0.10 |
| 1B | Cosine scheduler wraparound | `scripts/train.py` | Critical — prevents LR increase in late epochs |
| 2A | Gradient clipping | `scripts/train.py` | Stability at backbone unfreeze boundary |
| 2B | LR warmup | `scripts/train.py` | Reduces initial weight shock |
| 2C | FFT augmentation | `src/deepfake_data.py` | Prevents freq branch memorization |
| 2D | Per-epoch LR logging | `scripts/train.py` | Observability |
| 3A | Deeper FreqCNN (5 layers) | `src/models/freq_cnn.py` | Freq AUC +0.05-0.08 |
| 3B | Remove dead FFT transform | `src/transforms.py`, `src/deepfake_data.py` | Code cleanup |
| 4A | SE attention on fusion | `src/models/hybrid_fusion.py`, `scripts/train.py` | Learned branch weighting |
| 4B | Label smoothing | `scripts/train.py` | Reduces overconfident predictions |

---

## Tier 1: Critical Bugs

### 1A. FFT Normalization Constants Are Wrong

**File:** `src/deepfake_data.py:22-25`

**Problem:**
The previous constants `_FFT_MEAN=0.5, _FFT_STD=0.5` were applied to FFT log-magnitude data ranging approximately [0, 16]. The normalization formula `(x - 0.5) / 0.5` mapped this to [-1, 31] instead of the intended [-1, 1]. The DC component (center pixel) reaches log1p values of ~15-16, which after normalization became ~30 — an extreme positive outlier that distorted the network's input distribution.

**Root cause:** The constants were originally written for `get_fft_transform()` in `transforms.py`, which applied `Normalize(mean=[0.5], std=[0.5])` to PIL images (range [0, 1]). But the actual data pipeline loads raw `.npy` cache files containing `log1p(magnitude)` values in [0, ~16], bypassing the transform entirely.

**Fix (two parts):**

1. Updated `_FFT_MEAN` and `_FFT_STD` to estimated values matching the actual data distribution:

```python
# Before:
_FFT_MEAN = 0.5
_FFT_STD = 0.5

# After:
_FFT_MEAN = 5.0
_FFT_STD = 3.0
```

These are estimated values. The exact values should be computed by running:
```bash
python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --stats
python scripts/compute_fft_cache.py --config config.yaml --dataset CDF --stats
```

2. Added `compute_fft_stats()` function to `scripts/compute_fft_cache.py` that scans up to 5000 random `.npy` cache files and computes the global mean and standard deviation using Welford-style online accumulation:

```python
def compute_fft_stats(fft_root: Path, max_files: int = 5000):
    npy_files = list(Path(fft_root).rglob("*.npy"))
    # ... samples up to max_files, computes running sum and sum-of-squares
    mean = running_sum / total_pixels
    std = np.sqrt(running_sq / total_pixels - mean ** 2)
    print(f"_FFT_MEAN = {mean:.4f}")
    print(f"_FFT_STD  = {std:.4f}")
```

Invoked via new `--stats` CLI flag. No FFT cache recomputation needed — existing caches store raw log-magnitude.

**Expected impact:** +0.05-0.10 AUC for Freq models. Properly scaled inputs allow BatchNorm and conv layers to operate in their intended range.

---

### 1B. Cosine Scheduler Wraparound + LR Warmup

**File:** `scripts/train.py:193-204`

**Problem:**
The previous scheduler used `T_max = epochs - FREEZE_EPOCHS` (= 7 for 10 epochs). Since `scheduler.step()` was called every epoch (including frozen ones), CosineAnnealingLR completed its full cycle at step 7 and **wrapped around** — causing the learning rate to **increase** during epochs 8-10 when it should be at its lowest.

Additionally, training jumped straight to full LR from step 1, causing large initial weight updates on pretrained features.

**Fix:**
Replaced the single CosineAnnealingLR with a `SequentialLR` combining:
- **Linear warmup** (2 epochs): ramps LR from 10% to 100% of base rate
- **Cosine annealing** (remaining epochs): decays to `eta_min=1e-6`

```python
# Before:
frozen_epochs = FREEZE_EPOCHS if args.model in {"hybrid", "early_fusion"} else 0
t_max = max(epochs - frozen_epochs, 1)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max, eta_min=1e-6)

# After:
warmup_epochs = 2
warmup_scheduler = optim.lr_scheduler.LinearLR(
    optimizer, start_factor=0.1, end_factor=1.0, total_iters=warmup_epochs
)
cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=max(epochs - warmup_epochs, 1), eta_min=1e-6
)
scheduler = optim.lr_scheduler.SequentialLR(
    optimizer, schedulers=[warmup_scheduler, cosine_scheduler],
    milestones=[warmup_epochs]
)
```

**LR curve for 10 epochs (base_lr=1e-4):**
- Epoch 1: 1e-5 (warmup start, 10% of base)
- Epoch 2: 1e-4 (warmup end, 100% of base)
- Epoch 3-10: cosine decay from 1e-4 → 1e-6

**Note on epoch count:** The plan also recommends `--epochs 15` for n=200 and `--epochs 20` for n=400 runs. This is a config/CLI change, not a code change. Hybrid CDF was still improving at epoch 10 (loss 0.0849, still decreasing).

**Expected impact:** +0.02-0.05 AUC; eliminates LR wraparound and reduces initial training instability.

---

## Tier 2: Training Stability

### 2A. Gradient Clipping

**File:** `scripts/train.py:105-110`

**Problem:**
No gradient clipping was applied. When the backbone unfreezes at epoch 4 (after `FREEZE_EPOCHS=3`), sudden gradient flow from the entire network can produce large gradient norms that destabilize the pretrained XceptionNet weights. This is especially problematic with mixed-precision training (AMP) where gradient magnitudes can vary more widely.

**Fix:**
Added `scaler.unscale_()` followed by `clip_grad_norm_()` before the optimizer step inside `train_one_epoch()`:

```python
# Before:
if (i + 1) % accum_steps == 0 or (i + 1) == len(loader):
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()

# After:
if (i + 1) % accum_steps == 0 or (i + 1) == len(loader):
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()
```

**Why `scaler.unscale_()` first:** With AMP, gradients are scaled by the GradScaler. We must unscale them before clipping, otherwise the clip threshold would need to account for the unknown scale factor. After unscaling, `max_norm=1.0` clips at the true gradient L2 norm.

**Expected impact:** Prevents gradient explosions at the unfreeze boundary (epoch 4). Particularly important for hybrid model where two branches contribute gradients.

---

### 2C. FFT Augmentation

**File:** `src/deepfake_data.py:105-107`

**Problem:**
The FFT branch received identical cached input every epoch. While the spatial branch benefits from `RandomResizedCrop` and `RandomHorizontalFlip`, the frequency branch had **zero augmentation** — the `CenterCrop` in `get_fft_transform()` was dead code (never called). This caused severe overfitting: the freq branch memorized exact training FFT maps.

**Fix:**
Added Gaussian noise injection to normalized FFT tensors during training:

```python
if self.train:
    fft_tensor = fft_tensor + torch.randn_like(fft_tensor) * 0.1
```

**Why Gaussian noise (not spatial augmentation):**
- FFT magnitude maps have different semantics than spatial images — random crops/rotations would destroy frequency localization
- Additive Gaussian noise (σ=0.1 in normalized space) simulates sensor noise and compression artifacts
- After normalization to ~N(0,1), σ=0.1 adds ~10% relative noise — enough to prevent exact memorization without destroying signal

**Expected impact:** +0.02-0.05 Freq AUC, especially on small datasets where memorization is the primary failure mode.

---

### 2D. Per-Epoch LR Logging

**File:** `scripts/train.py:223-224`

**Fix:**
Added learning rate values to the per-epoch log line for visibility:

```python
# Before:
logging.info(f"Epoch {epoch}: loss={train_loss:.4f}, val_auc={...}, val_f1={...}")

# After:
current_lrs = [f"{pg['lr']:.2e}" for pg in optimizer.param_groups]
logging.info(f"Epoch {epoch}: lr={current_lrs}, loss={train_loss:.4f}, val_auc={...}, val_f1={...}")
```

For hybrid models with differential LR (2 param groups), this logs both backbone LR and head LR, making it easy to verify the warmup → cosine decay pattern and detect scheduler bugs.

---

## Tier 3: Architecture Improvements

### 3A. Deeper FreqCNN (3 → 5 Conv Layers, 64 → 256 Output Dim)

**File:** `src/models/freq_cnn.py`

**Problem:**
The original FreqCNN had only 3 conv layers (1→16→32→64 channels) with 2 MaxPool operations. For 224x224 input, this produced 56x56 feature maps before `AdaptiveAvgPool2d` — losing critical mid-frequency spatial resolution. The 64-dim output was vastly inferior to XceptionNet's 2048-dim features; even after projection to 256 via `freq_proj`, the information bottleneck at 64 dims limited what the frequency branch could contribute to fusion.

**Fix:**
Deepened to 5 conv layers with progressive channel expansion:

```
Before: Conv(1→16) → Pool → Conv(16→32) → Pool → Conv(32→64) → AdaptiveAvgPool
         224        112       112          56       56            1
         Params: ~28K, Output dim: 64

After:  Conv(1→32) → Pool → Conv(32→64) → Pool → Conv(64→128) → Pool →
         224        112       112          56       56            28
        Conv(128→256) → Pool → Conv(256→256) → AdaptiveAvgPool
         28             14       14              1
         Params: ~700K, Output dim: 256
```

Key changes:
- **5 conv layers** (was 3): captures more hierarchical frequency patterns
- **4 MaxPool operations** (was 2): reduces 224→14 before global pooling, preserving more spatial-frequency resolution
- **256-dim output** (was 64): matches the projection dimension in `hybrid_fusion.py`, eliminating the information bottleneck
- **BatchNorm after every conv**: stabilizes training of the deeper network
- **Classifier**: 256→128→num_classes with Dropout(0.3) (was 64→64→num_classes with Dropout(0.2))

**Impact on HybridTwoBranch:**
The `freq_proj` layer in `hybrid_fusion.py` automatically adapts because it reads `freq_dim = self.freq.feature_dim()`. The projection changes from `Linear(64→256)` to `Linear(256→256)`, which now acts as a learned transform + BatchNorm regularization rather than an upscaling bottleneck.

**Why not ResNet-18:** A purpose-built frequency CNN aligns better with the thesis narrative ("hybrid architecture with specialized branches"). Using ResNet-18 would mean two pretrained backbones, weakening the "complementary branch" argument. The deeper FreqCNN remains lightweight (~700K params vs XceptionNet's 22.8M).

**Expected impact:** Freq AUC improvement from ~0.50-0.54 to ~0.58+; stronger frequency features make fusion more effective.

---

### 3B. Remove Dead FFT Transform Code

**Files:** `src/transforms.py:32-48` (removed), `src/deepfake_data.py:72` (updated)

**Problem:**
`get_fft_transform()` in `transforms.py` was constructed in `DeepfakeDataset.__init__()` but **never called** in `__getitem__()`. The function included `CenterCrop`, `ToTensor`, and `Normalize(mean=[0.5], std=[0.5])` — all dead code since FFT data is loaded from `.npy` caches as tensors and normalized inline using `_FFT_MEAN`/`_FFT_STD`.

**Fix:**
1. Removed `get_fft_transform()` entirely from `transforms.py`
2. Replaced `self.fft_transform = T.get_fft_transform(...)` with a comment explaining that FFT normalization is done inline in `__getitem__`

This eliminates confusion about where FFT normalization happens and prevents future bugs from assuming the transform is applied.

---

## Tier 4: Optional Enhancements

### 4A. SE (Squeeze-and-Excitation) Attention on Fusion

**File:** `src/models/hybrid_fusion.py:11-24`

**Problem:**
The previous fusion strategy was simple concatenation: `fused = cat([spatial_feat, freq_feat])`. This treats both branches equally regardless of input — a mislabeled frequency artifact would contribute as much as a clear spatial manipulation signal. The classifier had to learn branch-weighting implicitly through its fully-connected layers.

**Fix:**
Added `SEGate` module between concatenation and classifier:

```python
class SEGate(nn.Module):
    """Squeeze-and-Excitation gating on the fused feature vector."""
    def __init__(self, in_dim: int, reduction: int = 4):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Linear(in_dim, in_dim // reduction),  # 512 → 128
            nn.ReLU(inplace=True),
            nn.Linear(in_dim // reduction, in_dim),  # 128 → 512
            nn.Sigmoid(),
        )

    def forward(self, x):
        return x * self.gate(x)  # element-wise gating
```

The forward pass becomes:
```python
fused = torch.cat([spatial_feat, freq_feat], dim=1)  # [B, 512]
fused = self.se_gate(fused)  # learned per-dimension gating
logits = self.classifier(fused)
```

**How it works:**
1. The gate network compresses the 512-dim fused vector to 128 dims (squeeze)
2. Re-expands to 512 dims with sigmoid activation (excitation)
3. Element-wise multiplication scales each feature dimension by [0, 1]
4. The network learns to suppress noisy dimensions and amplify informative ones

**Parameter overhead:** ~131K parameters (512×128 + 128×512 + biases) — negligible compared to XceptionNet's 22.8M.

**Also updated `train.py`:** Added `model.se_gate.parameters()` to the `head_params` group for the hybrid optimizer, ensuring SE gate parameters receive the full (not reduced) learning rate.

---

### 4B. Label Smoothing

**File:** `scripts/train.py:94, 101-102, 206`

**Problem:**
With small datasets (n=50, n=200), the model can become overconfident on training samples, predicting probabilities very close to 0.0 or 1.0. This leads to sharp loss gradients and poor calibration — the model's confidence doesn't reflect its actual accuracy.

**Fix:**
Added configurable label smoothing that softens binary targets:

```python
# In train_one_epoch():
if label_smooth > 0:
    targets = targets * (1 - label_smooth) + label_smooth * 0.5
    # Maps: 0 → 0.025, 1 → 0.975 (with default smooth=0.05)
```

Default value: `label_smoothing: 0.05` (read from config, overridable).

**Why 0.05:** A 5% smoothing factor is conservative enough to preserve the learning signal while preventing the model from driving logits to extreme values. For BCEWithLogitsLoss, this means the model targets sigmoid(logits) ≈ 0.975 instead of 1.0, requiring logits ≈ 3.66 instead of +∞.

---

## Files Modified — Complete Diff Summary

### `src/deepfake_data.py`
- **Lines 22-25:** `_FFT_MEAN` changed from 0.5 to 5.0; `_FFT_STD` changed from 0.5 to 3.0
- **Line 73:** Replaced `self.fft_transform = T.get_fft_transform(...)` with explanatory comment
- **Lines 105-107:** Added Gaussian noise augmentation for FFT tensors during training

### `scripts/train.py`
- **Lines 94:** Added `label_smooth` parameter to `train_one_epoch()`
- **Lines 101-102:** Label smoothing applied to targets before loss computation
- **Lines 105-110:** Added `scaler.unscale_()` and `clip_grad_norm_(max_norm=1.0)` before optimizer step
- **Lines 157-162:** Added `model.se_gate.parameters()` to hybrid head param group
- **Lines 193-206:** Replaced CosineAnnealingLR with SequentialLR (LinearLR warmup + CosineAnnealingLR)
- **Line 206:** Added `label_smooth` config read (default 0.05)
- **Line 220:** Pass `label_smooth` to `train_one_epoch()`
- **Lines 223-224:** Added per-epoch LR logging with formatted learning rates

### `src/models/freq_cnn.py`
- Complete rewrite: 3 → 5 conv layers, channel progression 1→32→64→128→256→256
- 4 MaxPool layers (was 2), AdaptiveAvgPool at end
- Classifier: 256→128→num_classes with Dropout(0.3)
- `feature_dim()` returns 256 (was 64)

### `src/transforms.py`
- Removed `get_fft_transform()` function entirely (was lines 32-48, dead code)

### `src/models/hybrid_fusion.py`
- Added `SEGate` class (Squeeze-and-Excitation gating)
- Inserted `self.se_gate = SEGate(fused_dim)` in `HybridTwoBranch.__init__()`
- Added `fused = self.se_gate(fused)` in forward pass between concat and classifier

### `scripts/compute_fft_cache.py`
- Added `import numpy as np`
- Added `compute_fft_stats()` function for computing global FFT mean/std from cache
- Added `--stats` CLI flag to invoke stats computation instead of cache building
- Early return after stats computation when `--stats` is set

---

## Verification Plan

### Phase 1: After deploying these fixes
1. Run `compute_fft_stats` on existing cache → get actual mean/std → update `_FFT_MEAN`/`_FFT_STD` in `deepfake_data.py`
2. Train Freq-only on FFPP n=50 — expect AUC improvement from 0.541 to 0.60+
3. Train Hybrid on CDF n=200 with `--epochs 15` — expect AUC improvement past 0.565

### Phase 2: Stability checks
1. Train all 3 models on FFPP n=200 — check if catastrophic collapse (AUC ~0.50) is resolved
2. Inspect training logs for LR warmup → cosine decay pattern
3. Verify no gradient explosion at epoch 4 (unfreeze boundary) via loss curve

### Phase 3: Full validation
Run complete experiment matrix (n=50, n=200, n=400) with all fixes and compare against baseline tables from previous runs.

### Key metrics to watch
- **Freq standalone AUC** should exceed 0.55 (was 0.50-0.54)
- **Hybrid should outperform Spatial** (was underperforming due to weak freq branch + bad normalization)
- **FFPP n=200 should not collapse** to near-random (was AUC ~0.48-0.52)
- **Training logs** should show `lr=[...]` with monotonic warmup then decay

---

## Notes

- The FFPP n=200 U-shaped performance dip has a **data-level component** (200 videos / 6 methods = ~33 per method → insufficient per-method diversity). No code fix can fully resolve this; it is a legitimate finding for the thesis.
- The `_FFT_MEAN=5.0` and `_FFT_STD=3.0` are estimates based on the expected range of `log1p(FFT magnitude)`. **Run `--stats` to get exact values before the next training run.**
- Label smoothing default of 0.05 can be adjusted via `label_smoothing` key in the config YAML file. Set to 0.0 to disable.
- Epoch count is controlled via config (`epochs` key). Recommended: 15 for n=200, 20 for n=400.
