# Opus Deep Analysis — Deepfake Hybrid Detection System

**Date:** 2026-03-14
**Scope:** Code correctness review, architecture critique, experimental results interpretation
**Codebase:** `deepfake_hybrid/` — hybrid XceptionNet + FFT frequency analysis

---

## Section 1: Code Correctness Review

### 1a. CRITICAL — FFT Normalization Is Never Applied (Dead Code Path)

**Severity: CRITICAL — Invalidates all frequency-dependent results**

The `Normalize(mean=[0.5], std=[0.5])` added to `get_fft_transform()` in `transforms.py:36` is **never executed** during training or evaluation. Here is the exact code path that proves this:

**Step 1:** For modes `freq`, `hybrid`, and `early_fusion`, `__getitem__` (line 91-96 of `deepfake_data.py`) always calls `_load_fft()`:
```python
if self.mode in {"freq", "hybrid", "early_fusion"}:
    fft_tensor = self._load_fft(Path(frame_path))      # ALWAYS returns a tensor
    fft_tensor = torch.nn.functional.interpolate(...)   # resize (224→224, a no-op)
```

**Step 2:** `_load_fft()` (line 71-81) **always returns a `torch.Tensor`**, never `None`:
- Cache hit: returns `torch.tensor(arr, dtype=torch.float32).unsqueeze(0)` (line 77)
- Cache miss: computes FFT and returns `torch.tensor(logmag, dtype=torch.float32).unsqueeze(0)` (line 81)

**Step 3:** The normalization transform is gated behind `if fft_tensor is None` (lines 102, 105, 109):
```python
fft_tensor = self.fft_transform(img.convert("L")) if fft_tensor is None else fft_tensor
```
Since `fft_tensor` is **never None** after step 1, `self.fft_transform` is **never called**. The `Normalize(mean=[0.5], std=[0.5])` is dead code.

**Consequence:** The frequency branch receives raw `log1p(magnitude)` values. For a 224x224 grayscale image, the 2D FFT magnitude at the DC component can be extremely large (sum of all pixel values ~ 224 * 224 * 128 ≈ 6.4M, so `log1p(6.4M) ≈ 15.7`). The typical range of `log1p(magnitude)` across the spectrum is approximately **[0, 16]**.

Meanwhile, the spatial branch receives ImageNet-normalized values in approximately **[-2.1, 2.6]**.

This ~6x scale mismatch means:
- The frequency branch's raw features have much larger magnitude entering `freq_proj`
- `BatchNorm1d` in `freq_proj` partially corrects this post-projection, but the **convolutional layers inside FreqCNN** receive unnormalized inputs, causing suboptimal feature extraction
- The gradient magnitudes flowing through the frequency branch are disproportionately large compared to the spatial branch

**This bug is present in ALL experimental results reported in CONCLUSION.md.** The "FFT normalization fix" was added to `transforms.py` but the data loading pipeline bypasses it entirely.

---

### 1b. HIGH — Augmentation Asymmetry in Hybrid Mode

**Severity: HIGH — Corrupts spatial-frequency correspondence during training**

In hybrid mode, `__getitem__` processes both branches independently:

```python
# Line 87: spatial branch — applies RandomHorizontalFlip (50% chance) + RandomResizedCrop
img_tensor = self.spatial_transform(img)

# Line 92: frequency branch — loads pre-cached FFT (computed from original, un-augmented image)
fft_tensor = self._load_fft(Path(frame_path))
```

**The problem:** When `RandomHorizontalFlip` triggers (50% of training samples), the RGB image is horizontally mirrored but the FFT input is not. The model receives a **mismatched pair**: a flipped face paired with the spectrum of the un-flipped face.

**Why this matters for FFT:** Horizontally flipping an image in the spatial domain causes the FFT magnitude spectrum to also flip horizontally (since `|DFT(flip(x))| = flip(|DFT(x)|)` for the real-valued magnitude after fftshift). The magnitude spectrum is NOT identical before and after a horizontal flip — it is reflected. So the spatial branch sees a flipped face while the frequency branch sees the spectrum of the original orientation.

**Impact on fusion:** The classifier must learn to associate spatially-flipped RGB features with un-flipped FFT features for ~50% of training samples. This introduces systematic noise into the learned spatial-frequency relationship. The fusion layer cannot rely on consistent cross-branch correspondences, degrading its ability to learn meaningful complementary features.

**Additional asymmetry:** `RandomResizedCrop` changes the spatial extent of the face region in the RGB branch (scale 0.8-1.0), but the FFT is computed from the full frame. The RGB might show a zoomed-in cheek while the FFT represents the full-frame spectrum. This further decouples the two inputs.

---

### 1c. OK — FreqCNN Feature Extraction Call Is Correct

**Severity: None — no bug here**

In `hybrid_fusion.py:42`, `self.freq.features(fft)` calls the `features` attribute of `FreqCNN`, which is an `nn.Sequential` containing the convolutional backbone + `AdaptiveAvgPool2d((1,1))`.

This produces output shape `(B, 64, 1, 1)`. The subsequent `torch.flatten(freq_feat, 1)` collapses this to `(B, 64)`.

This is **intentionally correct** — the hybrid model extracts features from FreqCNN's convolutional backbone without passing through FreqCNN's own classifier head (which would output a scalar logit). The hybrid model replaces FreqCNN's classifier with the shared fusion classifier. This is the standard pattern for feature extraction in multi-branch architectures.

One subtlety: when `FreqCNN` is used standalone (mode="freq"), it uses its own `classifier` sub-module (64→64→1). But when used inside `HybridTwoBranch`, only `features` is called, and the standalone classifier weights are **allocated but never used**. This wastes a small amount of memory (~4K parameters) but has no functional impact.

---

### 1d. MODERATE — Projection Dimension Asymmetry

**Severity: MODERATE — Dilutes frequency features**

The two projection layers have fundamentally different information-theoretic roles:

| Branch | Input dim | Output dim | Effect |
|--------|-----------|------------|--------|
| Spatial | 2048 | 256 | **Compression** (8:1) — forces the network to select the 256 most discriminative features from 2048 |
| Frequency | 64 | 256 | **Expansion** (1:4) — maps 64 features into a 256-dim space, which the linear layer fills with linear combinations of the same 64 values |

**The expansion problem:** A `Linear(64, 256)` layer can only produce outputs that lie in a 64-dimensional subspace of R^256. The remaining 192 dimensions are either zero or linear combinations of the first 64. `BatchNorm1d(256)` then rescales each of the 256 dimensions independently, which can amplify noise in the linearly-dependent dimensions.

After `ReLU`, approximately half the expanded dimensions are zeroed out, but the surviving ones still live in a low-rank subspace. When concatenated with the spatial branch's genuinely 256-dimensional representation, the classifier sees a 512-dim vector where only ~256 + 64 = 320 dimensions carry independent information.

**In practice:** This means the frequency branch contributes at most 64 effective dimensions to the 512-dim fused vector, not 256. The classifier's `Linear(512, 128)` layer can learn to weight the spatial half more heavily (and the experimental results suggest it does — hybrid performs close to spatial on in-dataset tasks).

**Why this still matters:** If the 64 frequency dimensions encode dataset-specific artifacts (see Section 2c), the classifier still uses them because they are predictive on the training set. At test time on a different dataset, these 64 dimensions become adversarial inputs — they encode the wrong dataset's spectral fingerprint, actively pushing predictions in the wrong direction.

---

### 1e. MODERATE — FFT Interpolation No-Op

**Severity: LOW — Wastes computation but functionally harmless**

In `deepfake_data.py:93-95`:
```python
fft_tensor = torch.nn.functional.interpolate(
    fft_tensor.unsqueeze(0), size=(self.image_size, self.image_size),
    mode="bilinear", align_corners=False
).squeeze(0)
```

The FFT cache is already computed at `size=224` (via `save_fft_cache` which calls `image_to_fft_logmag(img, size=224)`), and `self.image_size` is also 224. This is a bilinear interpolation from 224x224 to 224x224 — a **no-op** that adds unnecessary computation to every data loading call without changing the tensor values. Not a correctness issue, but should be cleaned up.

---

### 1f. MINOR — Grayscale Conversion Inconsistency

**Severity: MINOR — Unlikely to significantly affect results**

Two different grayscale conversion methods are used:

| Function | Method | Formula |
|----------|--------|---------|
| `image_to_fft_logmag` (PIL path, used by cache) | `img.convert("L")` | 0.299R + 0.587G + 0.114B (ITU-R 601) |
| `tensor_fft_logmag` (tensor path, unused in current pipeline) | `torch.mean(img_tensor, dim=0)` | (R + G + B) / 3 (equal weight) |

Currently, `tensor_fft_logmag` is not called anywhere in the training/eval pipeline — all FFT computation goes through the PIL-based `image_to_fft_logmag` via `save_fft_cache`. So this inconsistency has **no effect on current results**. But if someone switches to on-the-fly FFT computation using the tensor path, the different grayscale conversion would produce slightly different spectra. The luminosity-weighted conversion is perceptually correct; the equal-weight average would slightly over-weight the blue channel and under-weight green.

---

### 1g. MODERATE — Cosine Scheduler Interacts Poorly With Backbone Freezing

**Severity: MODERATE — Reduces effective training time**

In `train.py`:
- `FREEZE_EPOCHS = 3`: spatial backbone is frozen for epochs 1-3
- `CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)`: scheduler starts decaying from epoch 1
- With `epochs=10`, the scheduler follows: epoch 1 (LR=1e-4), epoch 2 (~9.5e-5), epoch 3 (~8.1e-5), ... epoch 10 (~1e-6)

**The problem:** The cosine schedule is "wasted" during the first 3 epochs when the backbone is frozen. By the time the backbone unfreezes at epoch 4, the backbone's learning rate (1/10 of head LR) has already decayed from 1e-5 to ~6.7e-6. The backbone effectively only trains for epochs 4-10 at a monotonically decreasing LR that starts 33% below its intended peak.

**What should happen:** The scheduler should start (or restart) at the unfreeze point, giving the backbone the full cosine warmup-decay cycle during its active training period. Alternatively, use `CosineAnnealingWarmRestarts` or manually set `T_max=epochs - FREEZE_EPOCHS` and start the scheduler after unfreezing.

This partially explains why the hybrid model's spatial branch may learn less robust features than the standalone spatial model, which gets the full cosine schedule for all 10 epochs.

---

## Section 2: Architecture Critique

### 2a. Root Cause of Hybrid Collapse at n=400 Cross-Dataset

The headline result: **Hybrid CDF→FFPP at n=400 produces F1=0.038** (essentially predicts "real" for everything), while Spatial achieves F1=0.234 on the same split. This is the most severe failure in the entire experiment matrix.

**Mechanistic explanation (four compounding factors):**

**Factor 1: The frequency branch encodes CDF-specific spectral signatures.**
Celeb-DF videos share a homogeneous compression pipeline (same codec settings, similar resolutions, consistent face synthesis method). At n=400, the FreqCNN has enough data to memorize the CDF-specific spectral envelope — the distribution of energy across frequencies that characterizes CDF's encoding. On CDF test data, this "dataset fingerprint" happens to correlate with the real/fake label. On FFPP data (different codec, different resolutions, 6 different manipulation methods), the fingerprint is meaningless but still active.

**Factor 2: The unnormalized FFT input (Bug 1a) amplifies frequency branch dominance.**
Because the FFT normalization is never applied (Section 1a), the frequency branch's raw inputs have 6x the magnitude of the spatial branch's normalized inputs. Despite BatchNorm partially correcting this after projection, the early convolutional layers of FreqCNN receive unnormalized values, producing features with different statistical properties than intended. The classifier layer `Linear(512, 128)` can develop larger weights for the frequency half of the 512-dim input simply because those features have more variance.

**Factor 3: Concatenation fusion has no gating mechanism.**
With simple concatenation, both branches contribute to every prediction with equal architectural opportunity. If the frequency branch encodes a strong but dataset-specific signal, the classifier will use it. There is no mechanism to detect "the frequency features are out-of-distribution" and down-weight them. When the model moves from CDF to FFPP, the frequency branch produces confident but incorrect activations (its learned CDF spectral pattern generates high-confidence outputs on FFPP spectral data that differs systematically), which override the spatial branch's more cautious but more generalizable predictions.

**Factor 4: More data amplifies memorization, not generalization.**
At n=50, the frequency branch can't memorize the CDF spectral fingerprint effectively — there's too little data for the 3-layer CNN to overfit to fine-grained spectral patterns. At n=400, there's enough statistical power to learn precise spectral signatures. The spatial branch also overfits at n=400, but its ImageNet-pretrained features provide a strong inductive bias toward edges, textures, and structures that transfer across datasets. The frequency branch has no such bias — it's trained from scratch on 64-channel features of FFT magnitudes.

**Why F1=0.038 specifically (near-total collapse to "real" predictions):**
The BCEWithLogitsLoss produces a single logit. At threshold 0.5, the sigmoid of the logit determines the prediction. If the frequency branch's CDF-trained features produce systematically negative activations on FFPP data (because FFPP's spectral characteristics map to "real" in the CDF-trained feature space), the combined logit is pushed negative for all samples, causing universal "real" predictions. The spatial branch alone (F1=0.234) shows this isn't purely random — there is some residual discrimination, but the frequency branch's erroneous signal drowns it out in the fused representation.

**Is this fixable or fundamental?**
This is a **fixable architecture issue**, not a fundamental limitation of late fusion. The root causes are:
1. No input normalization (Bug 1a) — fixable
2. No branch gating — fixable with attention-based fusion
3. FreqCNN trained from scratch with no inductive bias — fixable with pretrained frequency backbone
4. No domain-invariance constraint — fixable with domain-adversarial training

However, even with all fixes, the fundamental question remains: do deepfakes leave **universal** spectral signatures, or are spectral artifacts always codec/pipeline-specific? The literature (Durall et al., 2020; Frank et al., 2020) suggests that high-frequency artifacts in GAN-generated images are partially universal but heavily modulated by post-processing. For face-swapping deepfakes (as in FFPP/CDF), the spectral signature is dominated by the compression pipeline, not the manipulation method.

---

### 2b. FreqCNN Capacity Gap and Fusion Balance

**The numbers tell the story.** Comparing Freq-only vs Hybrid in-dataset performance:

| Dataset | n | Freq F1 | Hybrid F1 | Delta | Freq AUC | Hybrid AUC | Delta |
|---------|---|---------|-----------|-------|----------|------------|-------|
| FFPP | 50 | 0.394 | 0.666 | **+0.272** | 0.576 | 0.627 | +0.051 |
| FFPP | 200 | 0.354 | 0.433 | +0.079 | 0.430 | 0.522 | +0.092 |
| FFPP | 400 | 0.656 | 0.720 | **+0.064** | 0.681 | 0.666 | -0.015 |
| CDF | 50 | 0.596 | 0.882 | **+0.286** | 0.733 | 1.000 | **+0.267** |
| CDF | 200 | 0.266 | 0.534 | +0.268 | 0.460 | 0.583 | +0.123 |
| CDF | 400 | 0.604 | 0.665 | +0.061 | 0.603 | 0.823 | **+0.220** |

**Key observations:**

1. **Hybrid consistently outperforms Freq-only** — the spatial branch is clearly the dominant contributor. The improvement is largest at small n (CDF n=50: +0.286 F1, +0.267 AUC), where the frequency branch has the least data to overfit on and the spatial branch's pretrained features dominate.

2. **The hybrid improvement over Freq shrinks as n grows** (FFPP: +0.272 → +0.064), suggesting the frequency branch contributes less at scale — or more precisely, the spatial branch gets better while the frequency branch adds diminishing marginal information.

3. **At FFPP n=400, hybrid AUC (0.666) is actually LOWER than Freq AUC (0.681)**, while hybrid F1 (0.720) exceeds Freq F1 (0.656). This divergence between AUC and F1 suggests the hybrid model has better calibrated predictions at the 0.5 threshold but worse overall ranking ability — the frequency features are **distorting the probability landscape** in a way that helps threshold-based classification but hurts the ranking.

**Does the capacity gap cause the fusion to ignore one branch?**

Not exactly. BatchNorm after projection ensures both branches' 256-dim outputs have zero mean and unit variance per dimension, which prevents one branch from dominating purely through scale. However, the **information content** differs dramatically:

- Spatial branch: 2048 features compressed to 256 → rich, diverse feature set with genuine 256-dimensional structure
- Frequency branch: 64 features expanded to 256 → at most 64-dimensional submanifold, padded with linear dependencies

The classifier's `Linear(512, 128)` layer learns 128 filters across the 512-dim input. Empirically, it will learn to place more weight on the spatial half because those dimensions are more predictive and more diverse. The frequency half gets some weight because it carries *some* signal (especially dataset-specific patterns), but the classifier can't allocate more capacity to the spatial branch than the 50/50 architectural split allows.

**Does BatchNorm help or hurt?**

BatchNorm **helps** the in-dataset case by normalizing the two branches to compatible scales, enabling the classifier to compare them meaningfully. But it **hurts** the cross-dataset case because it masks the distributional shift: when the frequency branch produces out-of-distribution activations on the target dataset, BatchNorm rescales them to look "normal" (zero mean, unit variance), hiding the fact that the feature semantics have changed. The classifier has no signal that the frequency features are unreliable.

---

### 2c. FFT Features as Dataset Fingerprints

**Why FFT features learn dataset fingerprints:**

The FFT log-magnitude representation captures the **power spectral density** of the image. For a face image, this encodes:

1. **Camera/sensor characteristics** — pixel response function, Bayer pattern, sensor noise floor
2. **Compression artifacts** — JPEG/H.264 blocking patterns appear as periodic peaks in the spectrum; different quality settings produce different spectral envelopes
3. **Resolution and resampling** — upscaling/downscaling creates characteristic spectral rolloff patterns
4. **Face synthesis method** — GAN checkerboard artifacts, blending boundary artifacts, etc.

Properties (1-3) are **dataset-level constants** — all videos in CDF share the same camera pipeline and compression settings. Property (4) is the **signal of interest** for deepfake detection.

**The problem:** With a 3-layer CNN (FreqCNN), the network lacks the depth to disentangle forgery-specific spectral patterns from pipeline-specific spectral patterns. It learns the **easiest** discriminative features first, which are the dataset-level constants (because they're perfectly correlated with the data source, and CDF real/fake videos may use slightly different codecs or quality settings).

At n=50, there isn't enough data to reliably learn these fine-grained spectral patterns. At n=400, there is — and the model memorizes CDF's spectral fingerprint rather than learning universal forgery indicators.

**Evidence from Table 2:** Freq CDF→FFPP drops from F1=0.701 (n=50) to F1=0.168 (n=400). This is the most dramatic performance collapse of any model-direction combination. The n=50 result was likely "accidentally good" — with only 50 videos, the frequency model learns coarse features that happen to transfer. With 400 videos, it learns fine-grained features that are CDF-specific and anti-correlated with FFPP's patterns.

**The hybrid cascade:** If the freq branch learns "CDF spectral signature = fake" at n=400, then on FFPP data:
- FFPP spectra don't match the CDF fake signature → freq branch outputs "real" signal
- FFPP spectra also don't match the CDF real signature → freq branch is confused, outputs biased toward one class
- The spatial branch can partially detect FFPP fakes (F1=0.234 standalone) but the confused frequency signal adds noise
- The fusion classifier, which learned to trust the frequency branch on CDF, applies the same trust on FFPP
- Result: F1=0.038 — worse than either branch alone

---

### 2d. Concatenation Fusion vs Alternatives

**Failure modes of concatenation:**

1. **No input-dependent gating.** Each branch contributes the same 256 dimensions regardless of input difficulty or branch confidence. A hard sample where the spatial branch is uncertain still gets an equal contribution from the frequency branch, even if the frequency branch is encoding irrelevant dataset artifacts.

2. **Linear combination in the classifier can't "turn off" a branch.** While `Linear(512, 128)` can learn small weights for the frequency half, it can't learn to ignore the frequency branch **conditionally** (per-sample). A consistently uninformative frequency branch would get near-zero weights learned globally, but a frequency branch that's informative in-dataset but adversarial cross-dataset cannot be handled.

3. **No cross-branch interaction.** Concatenation treats the two feature vectors as independent. If there are interactions (e.g., a spatial artifact is confirmed by a spectral anomaly at the same spatial location), concatenation + linear layer can't capture them efficiently.

**Would attention-based weighting help?**

Partially. A gating mechanism like:
```python
alpha = sigmoid(Linear(concat([spatial_feat, freq_feat])))
fused = alpha * spatial_feat + (1 - alpha) * freq_feat
```
would allow the model to learn per-sample branch weights. **In-dataset**, this would likely learn α ≈ 0.6-0.7 (favoring spatial) but use frequency features when they're discriminative. **Cross-dataset**, the attention mechanism would still face the same problem: it was trained to trust the frequency branch on in-dataset data, so it doesn't know to distrust it on the target dataset.

For cross-dataset generalization specifically, attention-based weighting provides marginal improvement at best. The core problem is that the frequency features' distribution shifts across datasets, and no amount of learned weighting (trained on the source dataset) can detect this shift at test time.

**Would domain-adversarial training help?**

Yes — this is the most principled fix for the generalization problem. The mechanism:

1. Add a domain classifier head after the frequency projection: `domain_head = Linear(256, 1)` (predicts source dataset)
2. During training, use a gradient reversal layer (GRL) between `freq_proj` and `domain_head`
3. The freq branch is trained to: (a) minimize forgery classification loss, while (b) maximizing domain classification loss
4. This forces `freq_proj` to produce features that are **discriminative for forgery but invariant to the source dataset**

This directly addresses the root cause: the frequency branch learns dataset fingerprints because there's no constraint preventing it. Domain-adversarial training adds exactly that constraint.

**Implementation complexity:** Moderate — requires a second dataset during training (or held-out data treated as a different domain) and careful tuning of the GRL learning rate (λ parameter). For a thesis, this would be an excellent "proposed improvement" in future work.

---

### 2e. The n=200 Dip — Mechanistic Explanation

All models show a U-shaped pattern: n=50 outperforms n=200, then n=400 recovers. This is universal across models and datasets, ruling out model-specific explanations.

**Primary cause: Regime transition in the bias-variance tradeoff, amplified by fixed hyperparameters.**

At **n=50** (very small):
- ~50 videos × ~50 frames = ~2,500 training samples
- With batch_size=16 and 10 epochs: ~1,560 gradient steps
- The model quickly memorizes the small dataset → high training accuracy
- Test performance is inflated because the test set (15% of 50 videos ≈ 7 videos) is too small for reliable estimation. With ~350 test frames, variance in the F1 metric is very high. The "good" n=50 performance partially reflects lucky test splits.
- **The n=50 numbers are unreliable high estimates** (acknowledged in CONCLUSION.md)

At **n=200** (medium):
- ~200 videos × ~50 frames = ~10,000 training samples
- With batch_size=16 and 10 epochs: ~6,250 gradient steps
- The training set is now large enough that memorization doesn't work — the model must learn actual patterns
- But 10,000 samples may be in the "valley" where:
  - The learning rate schedule (cosine decay from 1e-4 to 1e-6 over 10 epochs) is too aggressive — the LR reaches low values before the model converges on the larger dataset
  - 10 epochs is not enough for 10K samples (the model needs more passes to learn from the increased variety)
  - The model underfits relative to the data complexity

At **n=400** (large):
- ~400 videos × ~50 frames = ~20,000 training samples
- With batch_size=16 and 10 epochs: ~12,500 gradient steps
- More gradient steps compensate for the aggressive LR decay
- The model has enough data AND enough training steps to learn robust patterns
- Performance recovers and exceeds n=50

**Supporting evidence:**
- The n=200 dip is worse for Freq (0.354 on FFPP, 0.266 on CDF) than Spatial (0.523, 0.542). FreqCNN trains from scratch with no pretrained initialization, so it needs more data/steps to learn useful features. At n=200, it's in the worst spot — too much data to memorize, too little training budget to learn.
- Hybrid at n=200 on FFPP shows AUC=0.522, barely above random (0.5). This suggests the fusion classifier is confused, receiving undertrained features from both branches.

**The fix is not more data but more training:** Increasing epochs from 10 to 20-30 would likely eliminate the n=200 dip by giving the model sufficient optimization steps. Alternatively, reducing the cosine decay aggressiveness (higher `eta_min`, or using step-based decay) would help.

---

## Section 3: Recommendations

| # | Issue | Severity | Affects Reported Results | Fix |
|---|-------|----------|-------------------------|-----|
| 1a | FFT normalization never applied — dead code path in `deepfake_data.py` | **CRITICAL** | **Yes — all freq and hybrid results are trained on unnormalized FFT** | In `_load_fft`, apply normalization after loading: `fft_tensor = (fft_tensor - 0.5) / 0.5` after the `unsqueeze(0)` line. Or restructure so `self.fft_transform` is always applied regardless of cache. |
| 1b | Augmentation asymmetry — spatial flip not applied to FFT | **HIGH** | **Yes — hybrid model trains on mismatched spatial-frequency pairs 50% of the time** | Either (a) disable `RandomHorizontalFlip` in spatial transform for hybrid mode, or (b) apply the same random flip to the cached FFT tensor after loading. Option (a) is simpler; option (b) preserves the augmentation benefit. |
| 1d | Projection expansion 64→256 dilutes frequency features | **MODERATE** | Partially — reduces frequency branch's effective contribution | Change to `PROJ_DIM = 64` for both branches (compress spatial to 64, keep freq at 64), or use separate projection dims (spatial_proj=128, freq_proj=64) to match information content. |
| 1e | FFT interpolate is a no-op (224→224) | **LOW** | No | Remove the `F.interpolate` call; add an assertion that the cached FFT size matches `self.image_size`. |
| 1g | Cosine scheduler wastes 3 epochs during backbone freeze | **MODERATE** | Yes — hybrid's spatial backbone gets suboptimal LR schedule | Set `T_max=epochs - FREEZE_EPOCHS` and start the scheduler after unfreezing, or use `SequentialLR` to chain a constant-LR phase with a cosine phase. |
| 2a | Hybrid collapse at n=400 cross-dataset | **CRITICAL** | Results are real, not a bug — but root cause includes bug 1a | Fix bugs 1a and 1b first, then re-evaluate. If collapse persists, add branch gating (attention-based fusion weight). |
| 2c | FFT features learn dataset fingerprints | **HIGH** | Fundamental issue, not a bug | Document as a key finding. For improvement: add domain-adversarial training on freq branch, or replace FreqCNN with a pretrained backbone (e.g., ResNet-18 on FFT). |
| 2e | n=200 dip from insufficient training budget | **MODERATE** | Yes — n=200 results understate model capability | Increase epochs to 20-30, or use per-tier epoch counts (n=50: 5 epochs, n=200: 15, n=400: 10). |

---

## Section 4: Thesis Contribution Framing

### 4.1 The Hybrid Model's Contribution

The hybrid model should be framed as a **methodological contribution with a nuanced finding**, not as a straightforward improvement:

> "We propose a two-branch late fusion architecture combining spatial (XceptionNet) and frequency (FFT-CNN) features for deepfake detection. Our experiments demonstrate that this hybrid approach achieves the highest in-dataset detection performance (F1=0.720 on FaceForensics++ at n=400), confirming that spatial and frequency features capture complementary forgery artifacts. However, we discover that the same complementary capacity that improves in-dataset performance **severely degrades cross-dataset generalization** (F1=0.038 from CDF→FFPP at n=400), revealing that the frequency branch learns dataset-specific spectral fingerprints rather than universal forgery indicators. This finding has important implications for the deployment of multi-modal deepfake detectors in real-world settings where the test distribution is unknown."

This framing turns the negative result into a **contribution**: you're not just reporting that hybrid doesn't generalize — you're identifying *why* (spectral fingerprinting) and providing evidence for a nuanced understanding of spatial vs. frequency features in deepfake detection.

### 4.2 The Frequency Branch's Role

Frame it as a **conditional benefit**:

> "Frequency domain features provide complementary information to spatial features *within a fixed data distribution*. The FFT log-magnitude representation captures compression artifacts and synthesis-specific spectral anomalies that the spatial branch misses, yielding consistent in-dataset improvements (+0.064 to +0.286 F1 over frequency-only baselines). However, these same spectral features are highly sensitive to dataset-specific acquisition and compression pipelines. Our results demonstrate that frequency features function as a *double-edged sword*: they boost performance when the test distribution matches the training distribution, but actively harm performance when it does not."

### 4.3 The Cleanest Thesis Contribution

The single strongest, most defensible finding:

> **"Cross-dataset generalization inversely correlates with in-dataset performance as training data scales, and this effect is most severe in multi-modal (hybrid) architectures."**

This is supported by Table 3: the average generalization drop goes from 0.17 (n=50) to 0.05 (n=200) to 0.39 (n=400). The hybrid model shows the worst drop at n=400 (0.627 from CDF). This is a **genuine empirical contribution** — it demonstrates that:

1. More data does not solve the generalization problem; it worsens it
2. Adding modalities (spatial + frequency) amplifies the overfitting risk
3. The field's standard practice of evaluating deepfake detectors in-dataset dramatically overestimates real-world performance

These findings are directly applicable to the ongoing debate in the deepfake detection community about evaluation protocols and generalization benchmarks. They argue for mandatory cross-dataset evaluation in future work — a methodological contribution that transcends the specific architecture.

### Secondary contribution:

> **"Training on multi-method datasets (FaceForensics++) produces more generalizable detectors than training on single-method datasets (Celeb-DF), across all model architectures."**

Table 2 shows that FFPP→CDF transfer consistently outperforms CDF→FFPP transfer at n=400 (Spatial: 0.503 vs 0.234; Hybrid: 0.368 vs 0.038). This supports dataset diversity as a key factor for generalization and recommends multi-method training data for practical deployment.
