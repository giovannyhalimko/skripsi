# Hybrid Model Cross-Dataset Collapse: Root Cause Analysis & Proposed Fixes

**Date:** 2026-03-14
**Scope:** Full code audit of HybridTwoBranch model, training pipeline, data pipeline, and experimental results

---

## 1. Problem Statement

The HybridTwoBranch model achieves the **best in-dataset F1** (0.720 on FFPP at n=400) but suffers **catastrophic cross-dataset collapse**:

| Direction | TP | FP | FN | TN | F1 | AUC |
|-----------|-----|-----|------|------|-------|-------|
| Hybrid CDF→FFPP | **52** | 43 | **2606** | 2591 | **0.038** | 0.506 |

Out of 2658 actual fake videos, the model only detected **52**. It predicts "real" for almost everything — the sigmoid outputs are nearly all below 0.5.

---

## 2. Files Audited

| File | Lines | Role |
|------|-------|------|
| `src/models/hybrid_fusion.py` | 41 | HybridTwoBranch + EarlyFusion models |
| `src/models/freq_cnn.py` | 37 | Frequency branch (FreqCNN) |
| `src/models/spatial_xception.py` | 41 | Spatial branch (XceptionNet via timm) |
| `src/deepfake_data.py` | 112 | Dataset class, frame loading, FFT loading |
| `src/transforms.py` | 47 | Spatial + FFT augmentations |
| `src/fft_utils.py` | 54 | FFT computation + normalization |
| `src/metrics.py` | 33 | Metric computation (fixed threshold=0.5) |
| `scripts/train.py` | 163 | Training loop, optimizer, no scheduler |
| `scripts/eval.py` | 103 | Evaluation pipeline |
| `scripts/run_all.py` | 167 | Full experiment matrix |

---

## 3. Current Architecture Summary

### HybridTwoBranch Forward Pass

```
RGB Image (3, 224, 224)
    ↓
XceptionNet (pretrained, global_pool="avg", num_classes=0)
    ↓
spatial_feat: (batch, 2048)
                                            FFT Magnitude (1, 224, 224)
                                                ↓
                                            FreqCNN.features (3 conv layers)
                                                ↓
                                            freq_feat: (batch, 64)
    ↓                                           ↓
    └──────── torch.cat ────────────────────────┘
                    ↓
            fused: (batch, 2112)
                    ↓
        Linear(2112, 256) → ReLU → Dropout(0.3) → Linear(256, 1)
                    ↓
              logit: (batch, 1)
```

### Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | Adam (lr=1e-4, weight_decay=1e-4) |
| Loss | BCEWithLogitsLoss |
| Scheduler | **None** |
| Epochs | 10 |
| Batch size | 16 |
| Gradient accumulation | 2 steps (hybrid) |
| Model selection | Best validation AUC |
| Early stopping | **None** |
| Differential LR | **None** (all params share 1e-4) |
| Backbone freezing | **None** (all params trainable from epoch 1) |

---

## 4. Root Causes (Ordered by Severity)

### RC-1: Feature Dimension Imbalance — 2048:64 (32:1 ratio)

**Location:** `hybrid_fusion.py:27` — `fused = torch.cat([spatial_feat, freq_feat], dim=1)`

The fusion vector is 2112-dim where **96.97% is spatial** and **3.03% is frequency**. The classifier `Linear(2112, 256)` will learn to rely almost entirely on spatial features. The gradient signal flowing back to FreqCNN through 64 out of 2112 weight columns is negligible.

**Evidence:** The hybrid model's cross-dataset behavior closely mirrors the spatial-only model (both predict mostly "real" on CDF→FFPP), suggesting the frequency branch contributes almost nothing.

**Severity:** CRITICAL — this makes the "hybrid" effectively a spatial-only model with extra parameters to overfit.

---

### RC-2: Per-Image FFT Normalization Destroys Discriminative Signal

**Location:** `fft_utils.py:19`

```python
logmag = (logmag - logmag.min()) / (logmag.max() - logmag.min() + 1e-8)
```

Every FFT magnitude map is independently min-max normalized to [0, 1]. This **discards absolute magnitude information** — a key forgery cue. A real image with low spectral energy and a deepfake with high spectral energy both get mapped to [0, 1].

**Severity:** HIGH — the frequency branch receives degraded input that lacks the most discriminative spectral feature.

---

### RC-3: No Learning Rate Scheduling or Differential LR

**Location:** `train.py:141`

```python
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
```

All parameters (pretrained XceptionNet backbone + random FreqCNN + random classifier) share the same lr=1e-4 with no decay. This causes:

1. **Pretrained features destroyed early** — XceptionNet's ImageNet weights provide domain-agnostic features. At lr=1e-4, these are overwritten within the first few epochs with dataset-specific patterns.
2. **No fine-grained convergence** — without decay, the model cannot transition from exploration to exploitation. Later epochs continue making large updates even when near convergence.

**Severity:** HIGH — directly causes loss of transferable features (main driver of cross-dataset collapse).

---

### RC-4: No Backbone Freezing

**Location:** `train.py:141` — `model.parameters()` passes everything to optimizer.

The XceptionNet backbone (22.8M params) is trainable from epoch 1. With only ~14,000 training frames at n=400, the pretrained features are quickly overwritten with dataset-specific patterns. The fusion classifier and FreqCNN (random init) need several epochs to learn meaningful representations, but by that time the backbone has already drifted from its transferable features.

**Severity:** HIGH — the backbone overfits before the fusion layers can leverage its pretrained features.

---

### RC-5: Augmentation Misalignment Between Branches

**Location:** `deepfake_data.py:87-95`

- RGB input: `self.spatial_transform(img)` applies RandomResizedCrop + RandomHorizontalFlip
- FFT input: loaded from **precomputed cache** (original, un-augmented frame)

The spatial and frequency branches see **different views** of the same frame during training. The spatial branch sees augmented data; the frequency branch sees the original. This teaches the fusion layer that the two signals are somewhat independent, reducing the benefit of fusion.

**Severity:** MEDIUM — degrades fusion quality but doesn't directly cause collapse.

---

### RC-6: Fixed Classification Threshold (0.5)

**Location:** `metrics.py:7` — `y_pred = (y_prob >= 0.5).astype(int)`

When the model's probability distribution shifts across datasets, the 0.5 threshold can cause near-total misclassification. The hybrid CDF→FFPP model outputs sigmoids mostly below 0.5, resulting in F1=0.038.

However, AUC (threshold-independent) is only 0.506 — barely above random. So this is a **contributing factor** but not the root cause.

**Severity:** MEDIUM — fixing this alone won't solve the problem, but it's easy to fix and will improve reported metrics.

---

### RC-7: FreqCNN Too Shallow (3 conv layers, 64-dim output)

**Location:** `freq_cnn.py:8-19`

```
Conv(1→16) → Conv(16→32) → Conv(32→64) → AdaptiveAvgPool → 64-dim
```

Compare: XceptionNet has 36 layers producing 2048-dim features. The frequency branch lacks capacity to learn complex spectral patterns from 224x224 FFT magnitude maps.

**Severity:** MEDIUM — low capacity limits what the frequency branch can contribute even if other issues are fixed.

---

### RC-8: No Normalization at Fusion Point

**Location:** `hybrid_fusion.py:25-27`

Neither branch output is normalized before concatenation. The spatial branch outputs features in an arbitrary range (determined by XceptionNet internals), while the frequency branch outputs features in a different range (after AdaptiveAvgPool2d). No L2-norm, BatchNorm1d, or LayerNorm is applied.

**Severity:** MEDIUM — exacerbates the dimension imbalance by adding scale imbalance.

---

### RC-9: Overparameterization Without Sufficient Regularization

- ~23.3M total parameters
- ~14,000 training frames at n=400
- Regularization: only weight_decay=1e-4 and Dropout(0.3)
- No label smoothing, no mixup, no stochastic depth, no gradient clipping

**Severity:** LOW-MEDIUM — standard for transfer learning, but insufficient given the severity of the distribution shift between FFPP and CDF.

---

## 5. Proposed Fixes

### Fix Priority Matrix

| Fix | Target RC | Code Change | Impact | Risk |
|-----|-----------|-------------|--------|------|
| A. Feature projection | RC-1 | `hybrid_fusion.py` | HIGH | LOW |
| B. Differential LR | RC-3 | `train.py` | HIGH | LOW |
| C. Backbone freezing | RC-4 | `train.py` | HIGH | LOW |
| D. LR scheduler | RC-3 | `train.py` | MEDIUM | LOW |
| E. FFT normalization | RC-2 | `fft_utils.py` + recompute cache | HIGH | MEDIUM |
| F. Fusion normalization | RC-8 | `hybrid_fusion.py` | MEDIUM | LOW |
| G. Increase dropout | RC-9 | `hybrid_fusion.py` | LOW | LOW |
| H. Optimal threshold | RC-6 | `metrics.py` / `eval.py` | LOW | LOW |

---

### Fix A: Feature Dimension Balancing (RC-1)

**File:** `hybrid_fusion.py`

**Current:**
```python
fused = torch.cat([spatial_feat, freq_feat], dim=1)  # (batch, 2112)
self.classifier = nn.Sequential(
    nn.Linear(2048 + 64, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 1)
)
```

**Proposed:**
```python
PROJ_DIM = 256  # both branches project to same dimension

self.spatial_proj = nn.Sequential(
    nn.Linear(spatial_dim, PROJ_DIM),
    nn.BatchNorm1d(PROJ_DIM),
    nn.ReLU(inplace=True),
)
self.freq_proj = nn.Sequential(
    nn.Linear(freq_dim, PROJ_DIM),
    nn.BatchNorm1d(PROJ_DIM),
    nn.ReLU(inplace=True),
)
self.classifier = nn.Sequential(
    nn.Dropout(0.5),
    nn.Linear(PROJ_DIM * 2, 128),
    nn.ReLU(inplace=True),
    nn.Dropout(0.3),
    nn.Linear(128, 1),
)

# In forward:
spatial_feat = self.spatial_proj(self.spatial(rgb))
freq_feat = self.freq_proj(torch.flatten(self.freq.features(fft), 1))
fused = torch.cat([spatial_feat, freq_feat], dim=1)  # (batch, 512) — balanced 50:50
```

**Why:** Both branches contribute equally to the fusion. BatchNorm1d normalizes the feature scales. The projection layers give each branch a learnable mapping to a common representation space.

---

### Fix B: Differential Learning Rates (RC-3)

**File:** `train.py`

**Current:**
```python
optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
```

**Proposed:**
```python
if args.model in ("hybrid", "early_fusion"):
    param_groups = [
        {"params": model.spatial.parameters(), "lr": cfg.get("lr", 1e-4) * 0.1},   # 1e-5
        {"params": model.freq.parameters(), "lr": cfg.get("lr", 1e-4)},             # 1e-4
        {"params": model.spatial_proj.parameters(), "lr": cfg.get("lr", 1e-4)},     # 1e-4
        {"params": model.freq_proj.parameters(), "lr": cfg.get("lr", 1e-4)},        # 1e-4
        {"params": model.classifier.parameters(), "lr": cfg.get("lr", 1e-4)},       # 1e-4
    ]
    optimizer = optim.Adam(param_groups, weight_decay=cfg.get("weight_decay", 1e-4))
else:
    optimizer = optim.Adam(model.parameters(), lr=cfg.get("lr", 1e-4), weight_decay=cfg.get("weight_decay", 1e-4))
```

**Why:** The pretrained XceptionNet backbone learns at 10x slower rate, preserving its transferable features while allowing the new layers to learn quickly.

---

### Fix C: Backbone Freezing for Initial Epochs (RC-4)

**File:** `train.py`

**Proposed:** Add inside the training loop:

```python
FREEZE_EPOCHS = 3  # freeze backbone for first 3 epochs

for epoch in range(1, epochs + 1):
    # Unfreeze backbone after FREEZE_EPOCHS
    if epoch == FREEZE_EPOCHS + 1 and args.model in ("hybrid", "early_fusion"):
        for param in model.spatial.parameters():
            param.requires_grad = True
        print(f"Epoch {epoch}: Unfroze spatial backbone")

    # At start, freeze backbone
    if epoch == 1 and args.model in ("hybrid", "early_fusion"):
        for param in model.spatial.parameters():
            param.requires_grad = False
        print("Freezing spatial backbone for first {} epochs".format(FREEZE_EPOCHS))
```

**Why:** The fusion classifier and frequency branch learn meaningful representations first, then the backbone is fine-tuned gently. This prevents the backbone from overfitting to dataset-specific patterns before the fusion layers are ready.

**Note:** When using both Fix B and Fix C together, unfreeze the backbone with the lower LR from Fix B.

---

### Fix D: Cosine Annealing LR Scheduler (RC-3)

**File:** `train.py`

**Proposed:**
```python
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

# At end of each epoch:
scheduler.step()
```

**Why:** Learning rate decays smoothly from initial value to near-zero, preventing large weight updates in later epochs that cause overfitting.

---

### Fix E: Global FFT Normalization (RC-2)

**File:** `fft_utils.py`

**Current:**
```python
logmag = (logmag - logmag.min()) / (logmag.max() - logmag.min() + 1e-8)  # per-image
```

**Proposed (Option 1 — remove normalization, let BatchNorm handle it):**
```python
# Just return logmag without min-max normalization
return logmag.astype(np.float32)
```

**Proposed (Option 2 — use global statistics):**
```python
# Precompute these from the training set
GLOBAL_MEAN = 4.5   # approximate — compute from training data
GLOBAL_STD = 1.2    # approximate — compute from training data
logmag = (logmag - GLOBAL_MEAN) / GLOBAL_STD
```

**Why:** Per-image min-max normalization discards absolute magnitude — a key forgery signal. The FreqCNN has BatchNorm layers that can normalize features, so raw log-magnitude is fine.

**Trade-off:** Requires recomputing the FFT cache. Option 1 is simpler and sufficient since FreqCNN's BatchNorm2d will handle normalization.

---

### Fix F: Fusion Normalization (RC-8)

Already addressed by Fix A — the `nn.BatchNorm1d(PROJ_DIM)` in each projection layer normalizes both branches to comparable scales.

---

### Fix G: Increase Fusion Dropout (RC-9)

Already addressed by Fix A — dropout increased to 0.5 before the first fusion layer and 0.3 before the output.

---

### Fix H: Optimal Threshold Selection (RC-6)

**File:** `eval.py` or `metrics.py`

**Proposed:** After computing AUC, find optimal threshold on validation set:
```python
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_true_val, y_prob_val)
optimal_idx = (tpr - fpr).argmax()
optimal_threshold = thresholds[optimal_idx]

# Use this threshold for test evaluation
y_pred = (y_prob_test >= optimal_threshold).astype(int)
```

**Why:** The fixed 0.5 threshold fails when probability distributions shift between datasets. Threshold optimization on validation set is standard practice.

**Note:** This only improves reported F1/accuracy/precision/recall. AUC is unaffected. Since AUC is also poor (0.506), this fix alone won't save the model — but it's easy and correct.

---

## 6. Implementation Plan

### Phase 1: High-Impact, Low-Risk (do first)

| Fix | Files Changed | Requires Retraining | Requires Cache Recompute |
|-----|--------------|--------------------|-----------------------|
| A. Feature projection | `hybrid_fusion.py` | Yes | No |
| B. Differential LR | `train.py` | Yes | No |
| C. Backbone freezing | `train.py` | Yes | No |
| D. LR scheduler | `train.py` | Yes | No |

These 4 fixes change only 2 files and don't require recomputing the FFT cache. They address the 3 most critical root causes (RC-1, RC-3, RC-4).

### Phase 2: Medium-Impact (if Phase 1 is insufficient)

| Fix | Files Changed | Requires Cache Recompute |
|-----|--------------|-------------------------|
| E. FFT normalization | `fft_utils.py` | **Yes** (all FFT .npy files) |
| H. Optimal threshold | `metrics.py` or `eval.py` | No |

### Phase 3: Architecture Expansion (optional, for future work)

- Increase FreqCNN capacity (RC-7)
- Attention-based fusion instead of concatenation
- Augmentation alignment (RC-5) — compute FFT on-the-fly from augmented images

---

## 7. Expected Outcomes

| Metric | Current (n=400) | Expected After Phase 1 |
|--------|-----------------|----------------------|
| Hybrid in-dataset F1 (FFPP) | 0.720 | ~0.70-0.75 (maintained or improved) |
| Hybrid in-dataset F1 (CDF) | 0.665 | ~0.65-0.70 (maintained) |
| Hybrid cross-dataset F1 (CDF→FFPP) | **0.038** | ~0.25-0.40 (major improvement) |
| Hybrid cross-dataset F1 (FFPP→CDF) | 0.368 | ~0.40-0.50 (moderate improvement) |
| Hybrid generalization drop (CDF) | 0.627 | ~0.25-0.35 (halved) |

**Key expectation:** The hybrid should no longer collapse cross-dataset. It may not beat spatial in cross-dataset metrics (spatial has inherent advantages from ImageNet pretraining), but it should remain competitive rather than catastrophically failing.

---

## 8. Impact on BAB III Methodology

Fixes A-D are **training strategy changes**, not architecture changes:
- Feature projection (Fix A) is a standard practice in multi-modal fusion — BAB III already describes the model as "late fusion with classifier"
- Differential LR, backbone freezing, and LR scheduling are standard transfer learning practices
- These don't change the fundamental approach (XceptionNet + FreqCNN + concatenation fusion)

**Recommendation:** BAB III can describe these as "training optimization strategies for the hybrid model" without needing to redefine the architecture. Add a paragraph about transfer learning best practices (differential LR, backbone freezing, scheduling) to the training configuration section.

---

## 9. What About Epochs?

**Current:** 10 epochs (per BAB III).

**Analysis:**
- With the current code (no scheduler, no freezing), more epochs = more overfitting = worse cross-dataset
- With Phase 1 fixes (scheduler + freezing + differential LR), the model converges more reliably
- 10 epochs is reasonable with cosine scheduling
- 20 epochs could be tried but is unlikely to help significantly — the improvements come from the fixes above, not from training longer

**Recommendation:** Keep 10 epochs. If Phase 1 results are promising, try 15 epochs with the scheduler to see if the model benefits from longer training under the regularized regime.
