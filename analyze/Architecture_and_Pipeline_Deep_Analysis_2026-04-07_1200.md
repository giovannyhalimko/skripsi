# Architecture & Pipeline Deep Analysis — Deepfake Hybrid Detection

**Date:** 2026-04-07
**Scope:** Exhaustive technical analysis of every module, function, and data flow in the deepfake hybrid detection system. Covers how the code works from raw video input through training to deepfake detection.

---

## 1. Project Overview & Module Map

### What This Project Does

This system detects deepfake videos by combining two complementary analysis domains:
- **Spatial domain** — Analyzes RGB pixel patterns (textures, structures, face features) using XceptionNet, a CNN pretrained on ImageNet.
- **Frequency domain** — Analyzes FFT magnitude spectra (spectral artifacts, unnatural frequency distributions) using FreqCNN, a purpose-built lightweight CNN.

Three model variants allow controlled comparison:
- **Spatial-only:** XceptionNet on RGB images
- **Frequency-only:** FreqCNN on FFT magnitude maps
- **Hybrid:** Both branches fused via learned SE gating

### Directory Structure

```
deepfake_hybrid/
├── config.yaml                    # All hyperparameters and dataset paths
├── src/                           # Core library code
│   ├── __init__.py
│   ├── utils.py                   # Seeding, logging, config loading, device selection
│   ├── fft_utils.py               # FFT computation and caching
│   ├── transforms.py              # Spatial augmentation pipelines
│   ├── metrics.py                 # Evaluation metrics (accuracy, F1, AUC, etc.)
│   ├── deepfake_data.py           # PyTorch Dataset class (all 4 modes)
│   └── models/
│       ├── __init__.py
│       ├── spatial_xception.py    # XceptionNet via timm
│       ├── freq_cnn.py            # FreqBlock (residual) + FreqCNN
│       └── hybrid_fusion.py       # SEGate + HybridTwoBranch + EarlyFusionXception
├── scripts/                       # Pipeline scripts
│   ├── run_pipeline.py            # Master orchestrator
│   ├── extract_frames.py          # Video → JPEG frames
│   ├── build_splits.py            # Stratified train/val/test split
│   ├── compute_fft_cache.py       # FFT precomputation + stats
│   ├── train.py                   # Model training (full loop)
│   ├── eval.py                    # Checkpoint evaluation
│   ├── run_all.py                 # Full experiment matrix
│   ├── plot_results.py            # Publication-quality plots
│   ├── diagnose_splits.py         # Data quality diagnostics
│   ├── download_datasets.py       # FaceForensics++ downloader
│   └── sample_dataset.py          # Quick subset sampling
└── outputs/                       # All generated artifacts
    ├── frames/{DATASET}/          # Extracted JPEG frames
    ├── manifests/{DATASET}/       # CSV manifests and splits
    ├── fft_cache/{DATASET}/       # .npy FFT cache + fft_stats.json
    ├── runs/{model}_{ds}_seed{s}/ # Checkpoints + training logs
    ├── tables/                    # Result CSV tables
    └── plots/                     # Visualization PNGs
```

### Module Dependency Graph

```
config.yaml
    ↓ (loaded by utils.load_config)
    ↓
scripts/train.py ──────────────────────────────────────────────────┐
    ├── imports src/utils.py (seed, device, logging, config)       │
    ├── imports src/deepfake_data.py (Dataset, DatasetConfig)      │
    │       ├── imports src/fft_utils.py (FFT computation)         │
    │       └── imports src/transforms.py (augmentation pipelines) │
    ├── imports src/models/spatial_xception.py (XceptionNet)       │
    ├── imports src/models/freq_cnn.py (FreqCNN)                   │
    ├── imports src/models/hybrid_fusion.py (HybridTwoBranch)      │
    │       ├── imports spatial_xception (feature extractor)       │
    │       └── imports freq_cnn (FreqCNN class)                   │
    └── imports src/metrics.py (compute_metrics, etc.)             │
                                                                    │
scripts/run_all.py ─── calls train.py via subprocess ──────────────┘
scripts/run_pipeline.py ─── calls extract_frames → build_splits → compute_fft_cache → run_all
```

---

## 2. Configuration System

**File:** `config.yaml`

Every configurable parameter in the system flows from this single YAML file. Scripts load it via `utils.load_config(path)` which calls `yaml.safe_load()`.

### Frame Extraction Parameters
| Parameter | Value | Purpose |
|---|---|---|
| `frame_sampling_fps` | `5` | Extract 5 frames per second from video |
| `max_frames_per_video` | `50` | Cap at 50 frames per video (prevents large videos from dominating) |
| `image_size` | `224` | All images resized to 224×224 (XceptionNet input standard) |

### Training Hyperparameters
| Parameter | Value | Purpose |
|---|---|---|
| `batch_size` | `16` | Mini-batch size per optimizer step |
| `num_workers` | `2` | DataLoader worker processes |
| `lr` | `2.0e-4` | Base learning rate for AdamW optimizer |
| `weight_decay` | `1.0e-4` | L2 regularization (decoupled in AdamW) |
| `epochs` | `30` | Maximum training epochs |
| `early_stop_patience` | `10` | Stop after 10 epochs without AUC improvement |
| `accum_steps` | `2` | Gradient accumulation steps (effective batch = 32) |
| `label_smoothing` | `0.0` | Disabled — hard labels used (0 or 1) |
| `fusion_mode` | `two_branch` | Late fusion strategy for hybrid model |
| `n_seeds` | `3` | Number of random seeds for multi-run experiments |

### Frequency Branch Parameters
| Parameter | Value | Purpose |
|---|---|---|
| `freq_depth` | `5` | Number of FreqBlock residual conv blocks (~700K params) |
| `freq_base_channels` | `32` | Initial channel count (doubles per block up to 256) |
| `fft_noise_sigma` | `0.05` | Gaussian noise σ for FFT augmentation during training |

### Dataset Configuration
| Dataset | Root Path | Real Keywords | Fake Keywords |
|---|---|---|---|
| FFPP | `./dataset/face_forensics` | original, real, pristine, actors, youtube | fake, manipulated, deepfakes, faceswap, neuraltextures, deepfakedetection, faceshifter, face2face |
| CDF | `./dataset/celeb_df` | real, authentic | fake, synthesis, deepfake |

---

## 3. Data Pipeline (End-to-End)

### 3a. Video → Frames (`extract_frames.py`)

**Input:** Raw video files (`.mp4`, `.avi`, `.mov`, `.mkv`) from dataset root directories.

**Process:**

1. **Video discovery:** Recursively scans dataset root for video files. For each video, infers label by checking parent directory name and filename against keyword lists from config.

2. **Label inference (`infer_label`):** Converts path parts to lowercase, checks fake keywords first (returns 1), then real keywords (returns 0). Returns None if no match — video is skipped.

3. **Balanced sampling (if `--n-samples` > 0):** Separates videos into real/fake lists, shuffles each with seed=42, takes approximately n/2 from each class. Creates a reserve pool for replacing failed extractions.

4. **Parallel frame extraction:** Uses `multiprocessing.Pool` to extract frames in parallel. For each video:
   - Opens with `cv2.VideoCapture`
   - Calculates frame interval: `max(int(round(native_fps / target_fps)), 1)`
   - Saves every interval-th frame as `frame_XXXXXX.jpg` until max_frames reached
   - Returns metadata dict `{video_id, label, frames_dir}` or None if failed

5. **Retry mechanism:** Failed videos are replaced from reserve pool (if available).

6. **Manifest output:** All successful extractions saved to `outputs/manifests/{DATASET}/manifest.csv` with columns: `video_id`, `label`, `frames_dir`.

**Key detail — video_id generation:** The video_id is derived from the relative path to the video file, with path separators (`/`, `\`) replaced by `_`. This creates a flat namespace in the frames directory while preserving traceability to the original video location.

---

### 3b. Frames → Splits (`build_splits.py`)

**Input:** `manifest.csv` from previous step.

**Process:**

1. **Validation:**
   - Checks for duplicate video_ids (raises ValueError — means extract_frames needs re-running)
   - Verifies minimum 4 samples per class (needed for 3-way stratified split)

2. **Two-stage stratified split:**
   - First: `train_test_split(df, test_size=0.15, stratify=label, random_state=42)` → separates test set
   - Second: `train_test_split(train_val, test_size=0.15/(1-0.15), stratify=label, random_state=42)` → separates val from train
   - Result: Train ≈ 70%, Val ≈ 15%, Test ≈ 15%

3. **Why video-level splitting matters:** If splitting were done at frame level, frames from the same video could appear in both training and test sets. The model would memorize video-specific features (background, lighting, face identity) instead of learning generalizable deepfake artifacts. Video-level splitting ensures all frames from a video stay in one subset.

**Output:** `train.csv`, `val.csv`, `test.csv` in `outputs/manifests/{DATASET}/`.

---

### 3c. Frames → FFT Cache (`compute_fft_cache.py` + `fft_utils.py`)

**Input:** Frame JPEG files referenced in manifest.csv.

**FFT Computation Pipeline (`fft_utils.image_to_fft_logmag`):**

```
RGB Image (PIL)
    ↓ Convert to grayscale ("L" mode)
    ↓   Uses ITU-R BT.601: Y = 0.299R + 0.587G + 0.114B
    ↓ Resize to 224×224
    ↓ Convert to float32 numpy array
    ↓ 2D FFT: np.fft.fft2(arr)
    ↓   Produces complex-valued frequency coefficients
    ↓ FFT Shift: np.fft.fftshift(fft)
    ↓   Moves DC component (0,0) from corner to center
    ↓   Low frequencies → center, high frequencies → edges
    ↓ Magnitude: np.abs(fft_shift)
    ↓   |F(u,v)| = sqrt(Re² + Im²)
    ↓ Log scaling: np.log1p(magnitude)
    ↓   Compresses dynamic range (DC can be 10000x larger than high-freq)
    ↓   log1p avoids log(0) = -inf
    ↓
float32 array (224×224), values typically [0, ~16]
    ↓ Save as .npy file
```

**Parallel execution:** Uses `multiprocessing.Pool` to compute FFT for all frames in parallel. Each worker loads one frame, computes FFT, saves `.npy` file. Skips existing cache files unless `--force` flag set.

**Statistics computation (`compute_fft_stats`):**
- After all FFT files are cached, scans up to 5000 random `.npy` files
- Computes global mean and std across all pixels using online accumulation:
  - `running_sum += arr.sum()`
  - `running_sq += (arr**2).sum()`
  - `mean = running_sum / total_pixels`
  - `std = sqrt(running_sq/total - mean²)`
- Saves to `fft_stats.json`: `{"mean": float, "std": float}`

**Why per-dataset stats matter:** FFPP and CDF have different camera types, compression codecs, and resolutions. Their FFT magnitude distributions are fundamentally different. Using global stats from one dataset to normalize another would introduce systematic bias.

**Output:** `.npy` files in `outputs/fft_cache/{DATASET}/{video_id}/` + `fft_stats.json`.

---

### 3d. Dataset Loading (`deepfake_data.py`)

**The `DeepfakeDataset` class bridges the cached data and the training loop.**

#### Initialization (`__init__`)

1. Loads manifest CSV (train.csv, val.csv, or test.csv)
2. For each video in manifest:
   - Lists all image files in `frames_dir` (extensions: `.jpg`, `.jpeg`, `.png`, `.bmp`)
   - Samples up to `max_frames_per_video` frames using a seeded RNG (`random.Random(seed)`)
   - Stores as list of `(frame_path, label, video_id)` tuples
3. Loads FFT normalization stats from `fft_stats.json` (falls back to mean=5.0, std=3.0 if missing)
4. Creates spatial transform pipeline:
   - For hybrid mode during training: `include_hflip=False` (flip applied manually to both branches)
   - For all other cases: `include_hflip=True`

#### Data Loading (`__getitem__`)

Returns different formats based on mode:

**Mode: "spatial"**
```
Load image → apply spatial transform → (img_tensor[3,224,224], label)
```

**Mode: "freq"**
```
Load FFT from .npy cache → normalize (z-score) → add noise → apply spectral masking → (fft_tensor[1,224,224], label)
```

**Mode: "hybrid"**
```
Load image → spatial transform (no hflip)
Load FFT → normalize → noise → spectral masking
Apply consistent random hflip to BOTH tensors (50% probability)
→ ({"image": img_tensor, "fft": fft_tensor}, label)
```

**Mode: "early_fusion"**
```
Load image → spatial transform
Load FFT → normalize → noise → spectral masking
Stack: torch.cat([rgb, fft], dim=0) → 4-channel tensor
→ (fused_tensor[4,224,224], label)
```

#### FFT Augmentation Details

**Gaussian noise (always during training if σ > 0):**
```python
fft_tensor = fft_tensor + torch.randn_like(fft_tensor) * cfg.fft_noise_sigma  # σ=0.05
```
Applied after z-score normalization. Simulates sensor noise and compression variations. Prevents exact memorization of cached FFT maps across epochs.

**Spectral band masking (15% probability during training):**
```python
if random.random() < 0.15:
    band_width = random.randint(2, max(h // 8, 3))
    start = random.randint(0, h - band_width)
    if random.random() < 0.5:
        fft_tensor[:, start:start+band_width, :] = 0  # horizontal band
    else:
        fft_tensor[:, :, start:start+band_width] = 0  # vertical band
```
Zeros out a random horizontal or vertical frequency band. Forces the model to not rely on any single frequency range, improving generalization.

#### Hybrid Augmentation Consistency

For hybrid mode, horizontal flip must be applied identically to both RGB and FFT:
```python
if self.train and random.random() < 0.5:
    img_tensor = TF.hflip(img_tensor)           # torchvision functional flip
    fft_tensor = torch.flip(fft_tensor, dims=[-1])  # flip last dimension
```
This is critical because `|DFT(flip(x))| = flip(|DFT(x)|)` — flipping the image flips its FFT magnitude. Without consistent flipping, the spatial and frequency branches would see mismatched representations 50% of the time.

---

## 4. Model Architectures

### 4a. Spatial Model — XceptionNet (`spatial_xception.py`)

**What it is:** XceptionNet is a deep CNN architecture built entirely from depthwise separable convolutions, introduced by Chollet (2017). It was originally designed for ImageNet classification and subsequently adopted as a strong baseline for deepfake detection by Rössler et al. (FaceForensics++).

**Three functions exposed:**

| Function | Returns | Used By |
|---|---|---|
| `build_xception(num_classes=1, in_chans=3, pretrained=True)` | Complete classifier model | Spatial model, EarlyFusion |
| `build_feature_extractor(in_chans=3, pretrained=True)` | Feature extractor (no classifier head) | HybridTwoBranch spatial branch |
| `get_feature_dim(in_chans=3)` | Integer feature dimension (2048) | HybridTwoBranch projection sizing |

All use `timm.create_model("xception", ...)` with `global_pool="avg"`. The key difference is `num_classes`: setting it to 0 removes the classification head and returns pooled features.

**Depthwise separable convolution — why it matters:**
- Standard convolution with $C_{in}$ input channels, $C_{out}$ output channels, kernel $K \times K$ requires $C_{in} \times K^2 \times C_{out}$ parameters.
- Depthwise separable factorizes this into: depthwise ($C_{in} \times K^2$) + pointwise ($C_{in} \times C_{out}$), total = $C_{in}(K^2 + C_{out})$.
- For typical values ($K=3$, $C_{in}=64$, $C_{out}=128$): standard = 73,728 params, separable = 8,768 params (~88% reduction).
- This allows XceptionNet to have 36 conv layers with only ~22.8M parameters.

**ImageNet pretraining:** The model is initialized with weights learned from 1.4M images across 1000 classes. Low-level features (edges, textures) and mid-level features (patterns, shapes) transfer well to deepfake detection. Only the final classification layer is replaced.

**Output:** 2048-dimensional feature vector after global average pooling.

---

### 4b. Frequency Model — FreqCNN (`freq_cnn.py`)

**What it is:** A purpose-built lightweight CNN for processing single-channel FFT log-magnitude maps. Designed to be small enough to avoid overfitting on small datasets while having enough capacity to learn meaningful frequency patterns.

**FreqBlock — Residual convolutional block:**
```
Input(in_ch) ──┬── Conv2d(in_ch→out_ch, 3×3, pad=1) → BatchNorm → ReLU ──┐
               │                                                            ├── Add → MaxPool2d(2)
               └── Shortcut(in_ch→out_ch, 1×1) if in_ch≠out_ch ───────────┘
                   Identity                  if in_ch==out_ch
```
The residual (shortcut) connection allows gradients to flow directly through the block, preventing vanishing gradients in deeper configurations. When channel dimensions change, a 1×1 convolution adapts the shortcut. MaxPool2d(2) halves spatial dimensions after each block.

**Architecture (depth=5, default):**

| Block | Channels | Input Size | Output Size | Parameters |
|---|---|---|---|---|
| FreqBlock 1 | 1 → 32 | (1, 224, 224) | (32, 112, 112) | ~384 |
| FreqBlock 2 | 32 → 64 | (32, 112, 112) | (64, 56, 56) | ~20,700 |
| FreqBlock 3 | 64 → 128 | (64, 56, 56) | (128, 28, 28) | ~82,300 |
| FreqBlock 4 | 128 → 256 | (128, 28, 28) | (256, 14, 14) | ~328,000 |
| FreqBlock 5 | 256 → 256 | (256, 14, 14) | (256, 7, 7) | ~590,000 |
| Dropout2d(0.2) | — | (256, 7, 7) | (256, 7, 7) | 0 |
| AdaptiveAvgPool | — | (256, 7, 7) | (256, 1, 1) | 0 |

**Classifier head:** `Flatten → Linear(256→128) → ReLU → Dropout(0.3) → Linear(128→1)`

**Channel progression:** `channels[i] = min(base_channels × 2^i, base_channels × 8)`. For depth=5 with base=32: [32, 64, 128, 256, 256]. The cap at 256 prevents excessive parameters in deeper blocks.

**`feature_dim()` method:** Returns `self._feature_dim` (256 for depth=5). Used by HybridTwoBranch to size the frequency projection layer.

**Why lightweight matters:** With only ~700K parameters (vs XceptionNet's 22.8M), FreqCNN is much less prone to overfitting on small datasets. It's forced to learn compact, generalizable frequency representations rather than memorizing training examples.

---

### 4c. Hybrid Model — HybridTwoBranch (`hybrid_fusion.py`)

**This is the main architectural contribution of the thesis.**

**Architecture overview:**
```
RGB (3,224,224) ──→ XceptionNet Backbone ──→ (batch, 2048)
                     │                           │
                     │                    spatial_proj: Linear(2048→256) + BN + ReLU
                     │                           │
                     │                           ↓ (batch, 256)
                     │                           │
                     │                     ┌─────┴─────┐
                     │                     │  Concat    │ ──→ (batch, 512)
                     │                     └─────┬─────┘
                     │                           │
                     │                      SE Gate ──→ (batch, 512)
                     │                           │
                     │                      Classifier ──→ logit
                     │
FFT (1,224,224) ──→ FreqCNN.features ──→ (batch, 256, 1, 1) → flatten → (batch, 256)
                                              │
                                       freq_proj: Linear(256→256) + BN + ReLU
                                              │
                                              ↓ (batch, 256) ──────────────────────────┘
```

**Projection layers — why dimension balancing matters:**

Without projection, concatenating XceptionNet's 2048-dim vector with FreqCNN's 256-dim vector creates a 2304-dim fused vector where 89% of dimensions come from the spatial branch. The classifier would learn to largely ignore frequency features because spatial features dominate by magnitude and dimensionality.

Both projection layers map to PROJ_DIM = 256:
- `spatial_proj`: Linear(2048 → 256) + BatchNorm1d(256) + ReLU — compresses, selects most discriminative spatial features
- `freq_proj`: Linear(256 → 256) + BatchNorm1d(256) + ReLU — learned transformation + normalization

After projection, both branches contribute equally to the 512-dim fused vector.

**SEGate — Squeeze-and-Excitation gating:**

```python
class SEGate(nn.Module):
    def __init__(self, in_dim, reduction=4):
        self.gate = nn.Sequential(
            nn.Linear(in_dim, in_dim // reduction),     # 512 → 128 (squeeze)
            nn.ReLU(inplace=True),
            nn.Linear(in_dim // reduction, in_dim),     # 128 → 512 (excitation)
            nn.Sigmoid()                                 # gate weights ∈ [0, 1]
        )
    
    def forward(self, x):
        return x * self.gate(x)  # element-wise gating
```

**How SE gating works:**
1. **Squeeze:** Compresses the 512-dim fused vector to 128 dimensions, forcing the network to identify the most important feature interactions.
2. **Excitation:** Expands back to 512 dimensions with sigmoid activation, producing per-dimension importance weights between 0 and 1.
3. **Gating:** Element-wise multiplication of original features with gate weights — suppresses irrelevant dimensions (gate ≈ 0), enhances informative ones (gate ≈ 1).

**Why SE gating over simple concatenation:** Simple concatenation treats all features equally. SE gating learns input-dependent weighting — for example, if the frequency branch produces noisy features for a particular input (e.g., highly compressed video), the gate can suppress those dimensions while amplifying spatial features that are more reliable for that sample.

**Classifier head:**
```
Dropout(0.3) → Linear(512 → 128) → ReLU → Dropout(0.3) → Linear(128 → 1)
```
Progressive dimension reduction with dropout regularization. Output is a single logit processed by BCEWithLogitsLoss.

---

### 4d. Early Fusion — EarlyFusionXception

**Architecture:** Takes the 4-channel stacked tensor `[RGB(3) + FFT(1)]` and feeds it directly into XceptionNet configured for 4 input channels.

```python
self.model = build_xception(num_classes=1, in_chans=4, pretrained=pretrained)
```

When `in_chans=4` with `pretrained=True`, timm handles the channel mismatch by adapting the first convolutional layer — typically replicating or zero-initializing weights for the 4th channel.

**Key difference from hybrid:** Early fusion forces the model to learn cross-modal (spatial-frequency) representations from the very first layer. The hybrid model allows each branch to learn modality-specific representations independently before combining them.

---

## 5. Training Pipeline (`train.py`)

### 5a. Model Selection & Initialization

```python
def select_model(model_type, pretrained, cfg):
    if model_type == "spatial":
        return build_xception(num_classes=1, in_chans=3, pretrained=pretrained)
    elif model_type == "freq":
        return FreqCNN(num_classes=1, depth=cfg.get("freq_depth", 3), base_channels=cfg.get("freq_base_channels", 32))
    elif model_type == "hybrid":
        return HybridTwoBranch(pretrained=pretrained, freq_depth=cfg.get("freq_depth", 3), freq_base_channels=cfg.get("freq_base_channels", 32))
    elif model_type == "early_fusion":
        return EarlyFusionXception(pretrained=pretrained)
```

After creation, model is moved to device (CUDA/CPU). If `compile_model` is set in config and PyTorch supports it, `torch.compile()` is applied for potential speedup.

**TF32 optimization:** On Ampere+ GPUs, TF32 is enabled for matmul and cuDNN operations for ~3× faster computation with minimal accuracy impact.

### 5b. Optimizer Setup — AdamW with Differential Learning Rates

**AdamW** (not Adam) is used — the key difference is *decoupled weight decay*. In standard Adam, weight decay is entangled with the adaptive learning rate, making it less effective. AdamW applies weight decay directly to weights, independent of the gradient moment estimates.

**Differential learning rates per model type:**

**Spatial model:**
- Scans all named parameters; those containing "head.fc" or "fc" are head params (base LR)
- All others are backbone params (base LR / 10)
- Handles case where no head params found (uses all as backbone)

**Hybrid model:**
- Backbone params: `model.spatial.parameters()` → LR = base / 10
- Head params: `model.freq`, `model.spatial_proj`, `model.freq_proj`, `model.se_gate`, `model.classifier` → LR = base

**Freq model:**
- All parameters at base LR (no pretrained weights to protect)

**Early fusion model:**
- All parameters at backbone LR (entire model is pretrained XceptionNet)

**Class imbalance handling:**
```python
train_df = pd.read_csv(train_manifest_path)
n_pos = int((train_df["label"] == 1).sum())
n_neg = int((train_df["label"] == 0).sum())
pos_weight = torch.tensor([n_neg / max(n_pos, 1)], device=device)
loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
```
If there are more real (0) than fake (1) samples, pos_weight > 1 increases the loss contribution of fake samples, preventing the model from defaulting to predicting "real" for everything.

### 5c. Backbone Freezing Strategy

**FREEZE_EPOCHS = 3** — For the first 3 epochs:

| Model | What's Frozen |
|---|---|
| spatial | All params except those containing "head.fc" or "fc" |
| hybrid | `model.spatial.parameters()` (XceptionNet backbone only) |
| early_fusion | `model.model.parameters()` (entire XceptionNet) |
| freq | Nothing frozen (no pretrained weights) |

**Why freeze:** New randomly-initialized layers (projections, classifier, SE gate) produce random gradients at the start of training. If these random gradients flow into the pretrained backbone immediately, they can destroy the carefully learned ImageNet representations (catastrophic forgetting). Freezing lets the new layers learn meaningful representations first.

**Unfreezing at epoch 4:**
```python
if epoch == FREEZE_EPOCHS + 1:  # epoch 4
    for p in backbone_params:
        p.requires_grad_(True)
```

### 5d. Learning Rate Schedule

**Two-phase schedule using `SequentialLR`:**

```python
warmup_scheduler = LinearLR(optimizer, start_factor=0.1, end_factor=1.0, total_iters=2)
cosine_scheduler = CosineAnnealingLR(optimizer, T_max=max(epochs - 2, 1), eta_min=1e-6)
scheduler = SequentialLR(optimizer, [warmup_scheduler, cosine_scheduler], milestones=[2])
```

**Phase 1 — Warmup (epochs 1-2):**
- LR ramps linearly from 10% to 100% of base
- Prevents large weight updates on pretrained features at the start
- Epoch 1: LR = 0.1 × 2e-4 = 2e-5, Epoch 2: LR = 2e-4

**Phase 2 — Cosine decay (epochs 3-30):**
- LR decreases smoothly following cosine curve from base to eta_min=1e-6
- No sharp drops that could destabilize training
- Monotonically decreasing — no wraparound issues

### 5e. Training Loop (`train_one_epoch`)

**For each batch in the training DataLoader:**

```
1. Forward pass (inside autocast for mixed precision):
   - Route batch through forward_model() based on model_type
   - Apply label smoothing if configured: targets = targets * (1 - α) + α * 0.5
   - Compute loss: BCEWithLogitsLoss(logits, targets) / accum_steps

2. Backward pass:
   - scaler.scale(loss).backward()

3. Optimizer step (every accum_steps batches):
   - scaler.unscale_(optimizer)                    # Unscale gradients to real magnitude
   - clip_grad_norm_(model.parameters(), max_norm=5.0)  # Prevent gradient explosion
   - scaler.step(optimizer)                        # Update weights
   - scaler.update()                               # Adjust loss scale for next iteration
   - optimizer.zero_grad()                         # Reset gradients
```

**Gradient accumulation:** Loss is divided by `accum_steps` before backward. Gradients accumulate over 2 batches before optimizer step. Effective batch size = 16 × 2 = 32 without requiring 32-sample GPU memory.

**Gradient clipping (max_norm=5.0):** After unscaling, if the L2 norm of all gradients exceeds 5.0, gradients are scaled down proportionally. This is especially important at epoch 4 when the backbone is unfrozen — the sudden gradient flow from 22.8M parameters can cause spikes.

**AMP (Automatic Mixed Precision):** `autocast` executes forward/backward in float16 on CUDA, `GradScaler` scales loss to prevent float16 underflow. Optimizer step uses float32 for numerical stability. Provides ~2× speedup with negligible accuracy impact.

### 5f. Validation & Early Stopping

**After each epoch:**

```python
val_metrics = evaluate(model, val_loader, model_type, device)
```

`evaluate()`:
1. Sets model to eval mode
2. Iterates through val_loader in `torch.no_grad()` context
3. Applies `torch.sigmoid(logits)` to get probabilities
4. Concatenates all predictions and targets
5. Calls `metrics_mod.compute_metrics(y_true, y_prob)` → returns dict with acc, precision, recall, f1, auc

**Checkpoint selection:**
```python
if val_metrics["auc"] > best_auc:
    best_auc = val_metrics["auc"]
    torch.save({"state_dict": model.state_dict(), "epoch": epoch, "config": cfg}, checkpoint_path)
    no_improve_count = 0
else:
    no_improve_count += 1
    if no_improve_count >= patience:  # patience=10
        break  # early stop
```

**Why AUC for model selection:** AUC evaluates the model's ranking ability across all possible thresholds, unlike accuracy which depends on a single threshold choice. A model with high AUC can be tuned to any desired precision-recall tradeoff at deployment time.

### 5g. Output Artifacts

Each training run produces:
- `best.pt` — Best checkpoint (highest val AUC)
- `metrics.json` — Full training history: `{"history": [{epoch, train_loss, acc, precision, recall, f1, auc, ...}, ...]}`
- `train.log` — Detailed training log with per-epoch LR values, loss, metrics

---

## 6. How Detection Works (`eval.py`)

**The detection pipeline answers one question: is this face frame real or fake?**

### Inference Flow

```
1. Load trained checkpoint (best.pt)
2. Load test manifest (test.csv)
3. Create DataLoader (no augmentation, no shuffle)
4. For each batch:
   a. Forward pass through model → raw logits
   b. Apply sigmoid: probability = σ(logit) = 1/(1+e^{-logit})
   c. Collect all probabilities and ground truth labels
5. Compute metrics at threshold=0.5
6. Find optimal threshold via Youden's J statistic
7. Compute metrics at optimal threshold
```

### How a Single Frame is Classified

**For the hybrid model:**

```
Frame image (JPEG)
    ├── Load as RGB → spatial transform (resize, normalize) → (3, 224, 224)
    └── Load FFT from .npy cache → z-score normalize → (1, 224, 224)
    ↓
    ├── XceptionNet backbone → 2048-dim features → project to 256-dim
    └── FreqCNN backbone → 256-dim features → project to 256-dim
    ↓
    Concatenate → 512-dim → SE Gate → 512-dim → Classifier → logit
    ↓
    sigmoid(logit) = probability
    ↓
    if probability > threshold: FAKE (label 1)
    else: REAL (label 0)
```

### Threshold Selection

**Default threshold (0.5):** Standard binary classification boundary. Any probability > 0.5 is classified as fake.

**Optimal threshold (Youden's J):**
```python
fpr, tpr, thresholds = roc_curve(y_true, y_prob)
j_scores = tpr - fpr
optimal_idx = np.argmax(j_scores)
optimal_threshold = thresholds[optimal_idx]
```
Youden's J = TPR - FPR finds the threshold that maximizes the difference between true positive rate and false positive rate — the point where the model best separates the two classes.

### Diagnostic Output

The evaluation script also computes mean predicted probabilities per class to detect potential issues:
```python
mean_prob_fake = y_prob[y_true == 1].mean()
mean_prob_real = y_prob[y_true == 0].mean()
```
If `mean_prob_fake < mean_prob_real`, the model's predictions are inverted — it thinks fakes are real and vice versa. This is logged as a warning.

---

## 7. Experiment Orchestration

### `run_pipeline.py` — Master Orchestrator

Runs the complete pipeline end-to-end via subprocess calls:

```
1. Patch config with CLI overrides → .pipeline_config.yaml
2. For each dataset (FFPP, CDF):
   a. extract_frames.py → frames + manifest
   b. build_splits.py → train/val/test CSVs
   c. compute_fft_cache.py → .npy cache + fft_stats.json
3. run_all.py → train all models, evaluate, generate tables
4. Cleanup temp config
```

### `run_all.py` — Experiment Matrix

Executes the full factorial experiment:

```
For each seed in [0, 1, 2]:
  For each train_dataset in [FFPP, CDF]:
    For each model in [spatial, freq, hybrid]:
      1. Check if checkpoint exists → train if not
      2. Evaluate in-dataset (train_ds == test_ds)
      3. Evaluate cross-dataset (train_ds ≠ test_ds)
```

**Outputs three tables:**
- `Table1_in_dataset.csv` — Metrics when test set matches training set
- `Table2_cross_dataset.csv` — Metrics when test set differs from training set
- `Table3_generalization_drop.csv` — F1 drop = F1_in - F1_cross per model

If `n_seeds > 1`: generates `_summary` tables with mean ± std over seeds.

---

## 8. Augmentation & Transforms (`transforms.py`)

### Spatial Training Pipeline

```python
transforms.Compose([
    Resize((image_size + 32, image_size + 32)),          # 256×256 (larger for crop margin)
    RandomResizedCrop(image_size, scale=(0.8, 1.0)),     # Random 224×224 crop at 80-100% scale
    ColorJitter(brightness=0.2, contrast=0.2,            # Color variation
                saturation=0.1, hue=0.05),
    RandomHorizontalFlip(),                               # 50% horizontal flip
    ToTensor(),                                           # [0, 255] int → [0, 1] float
    Normalize(IMAGENET_MEAN, IMAGENET_STD),              # ImageNet normalization
    RandomErasing(p=0.1, scale=(0.02, 0.15))             # 10% chance: erase small patch
])
```

**ColorJitter:** Simulates lighting variations. Important because deepfake artifacts can be lighting-dependent.

**RandomErasing:** Randomly occludes 2-15% of the image area 10% of the time. Forces the model to not rely on any single facial region.

### Spatial Validation/Test Pipeline

```python
transforms.Compose([
    Resize((image_size, image_size)),    # Direct 224×224 resize
    ToTensor(),
    Normalize(IMAGENET_MEAN, IMAGENET_STD)
])
```
No randomness — deterministic preprocessing for reproducible evaluation.

### FFT Augmentation (in deepfake_data.py)

Two augmentations applied after z-score normalization:
1. **Gaussian noise** (σ=0.05): always during training
2. **Spectral band masking** (15% probability): zeros random horizontal or vertical frequency band

No spatial augmentations (crop, rotate) on FFT — each pixel position represents a specific frequency component, so spatial transforms would destroy frequency semantics.

---

## 9. Metrics & Evaluation (`metrics.py`)

### `compute_metrics(y_true, y_prob, threshold=0.5)`

**Input:** Ground truth labels (0/1) and predicted probabilities [0,1].

**Process:**
1. Binarize predictions: `y_pred = (y_prob >= threshold).astype(int)`
2. Compute confusion matrix with explicit labels `[0, 1]` → extract TN, FP, FN, TP
3. Compute accuracy via `accuracy_score()`
4. Compute precision, recall, F1 via `precision_recall_fscore_support(average='binary')`
5. Compute AUC via `roc_auc_score()` with try-except for single-class edge case (→ NaN)

**Returns:** `{tp, tn, fp, fn, acc, precision, recall, f1, auc}`

### `find_optimal_threshold(y_true, y_prob)`

Computes ROC curve, calculates Youden's J = TPR - FPR at each threshold, returns threshold at maximum J. This finds the decision boundary that best separates real from fake.

### `roc_points(y_true, y_prob)`

Returns (fpr, tpr, thresholds) arrays for ROC curve plotting.

---

## 10. Visualization (`plot_results.py`)

Generates 4 types of publication-quality plots (300 DPI PNG):

### Training Curves
- One plot per (model, dataset, N) combination
- Dual-axis: training loss (left) and validation AUC + F1 (right)
- Shows convergence behavior and overfitting patterns

### Model Comparison Bars
- Grouped bar charts comparing spatial, freq, hybrid
- Separate plots for in-dataset and cross-dataset evaluation
- Bars show F1 and AUC side by side

### Generalization Drop
- Bar chart showing F1 in-dataset vs F1 cross-dataset
- Visualizes how much each model's performance degrades on unseen data

### Sample-Size Scaling
- Line plots showing metric vs N (sample size)
- Reveals how data quantity affects each model differently
- Key for thesis narrative: "more data helps spatial but may hurt frequency generalization"

---

## 11. Design Decisions & Rationale

### Why XceptionNet for spatial branch?
- Proven to achieve 95-99% accuracy on FaceForensics++ (highest among tested CNNs)
- Depthwise separable convolutions provide efficient parameter usage
- ImageNet pretraining transfers well to face analysis tasks
- Standard benchmark choice enables fair comparison with prior work

### Why FFT log-magnitude for frequency branch?
- GAN-based deepfakes systematically fail to reproduce correct spectral distributions (Durall et al.)
- Upsampling operations in generators create checkerboard artifacts visible in frequency domain (Odena et al.)
- Blending boundaries create discontinuities detectable as frequency anomalies
- Log scaling compresses the dynamic range (DC component can be 10000× larger than high-frequency)

### Why late fusion over early fusion?
- Late fusion allows each branch to learn modality-specific representations independently
- Spatial features (textures, structures) and frequency features (spectral patterns) have very different statistical properties
- Independent learning prevents one modality from dominating the other during training
- Empirically: late fusion with SE gating outperforms naive 4-channel early fusion

### Why SE gating instead of simple concatenation?
- Simple concatenation treats all features equally regardless of their quality
- SE gating learns input-dependent importance weights per feature dimension
- Can suppress noisy frequency features for compressed inputs while amplifying reliable spatial features
- Adds only ~131K parameters (negligible overhead on top of 23M+ total)

### Why video-level splits?
- Frames from the same video share background, lighting, face identity, and camera characteristics
- Frame-level splitting would let the model memorize video-specific features instead of learning deepfake artifacts
- Video-level splitting ensures generalization to unseen videos in the test set

### Why per-dataset FFT normalization?
- Different datasets use different cameras, compression codecs, and resolutions
- These factors create dataset-specific spectral signatures independent of deepfake artifacts
- Per-dataset normalization (z-score with dataset-specific mean/std) removes this confound
- Without it, the frequency branch would learn "dataset fingerprints" instead of forgery patterns

### Why differential learning rate?
- Pretrained XceptionNet weights are already near-optimal for visual feature extraction
- Applying the same high learning rate would destroy these learned representations (catastrophic forgetting)
- 10× lower LR for backbone allows gentle fine-tuning while new layers learn rapidly
- Backbone freezing during first 3 epochs provides additional protection during initial chaotic phase

### Why AdamW over Adam?
- Standard Adam applies weight decay inside the adaptive learning rate computation, making it less effective
- AdamW decouples weight decay from the gradient update, applying it directly to weights
- Results in more effective regularization, especially with differential learning rates

---

## 12. Known Issues & Historical Fixes

### Summary of 40+ fixes from documentation/ (chronological)

**2026-03-14 — Initial fixes (hybrid_model_fixes_2026-03-14.md):**
- Fix A: Feature dimension balancing — added projection layers (2048→256, 64→256) with BatchNorm
- Fix B: Differential learning rates — backbone LR = base/10
- Fix C: Backbone freezing — 3 epochs for hybrid/early_fusion
- Fix D: Cosine annealing LR scheduler
- Fix E: FFT normalization — removed per-image normalization, use raw log1p
- Fix F: Fusion normalization — BatchNorm in projections
- Fix G: Increased dropout (0.5→0.3 cascade in classifier)
- Fix H: Optimal threshold selection via Youden's J

**2026-03-14 — Deep analysis (hybrid_model_fixes_2026_03_14_03.md):**
- Critical: FFT normalization was dead code (never executed)
- High: Augmentation asymmetry (RGB flipped but FFT not)
- Analysis: Hybrid collapse root cause (4 compounding factors)
- Analysis: FreqCNN learns dataset fingerprints (spectral signatures of camera/codec)

**2026-03-17 — Final round (hybrid_model_fixes_2026_03_17.md):**
- FFT normalization constants updated (0.5/0.5 → per-dataset stats from fft_stats.json)
- SequentialLR replacing CosineAnnealingLR (fixed wraparound bug)
- Gradient clipping (max_norm for stability at unfreeze boundary)
- LR warmup (2 epochs, 10%→100%)
- FFT Gaussian noise augmentation
- Deeper FreqCNN (5 layers, 256-dim output, ~700K params)
- SE gating on fusion
- Label smoothing (configurable, currently 0.0)
- Per-epoch LR logging

**Current state vs older documentation:**
Some earlier documentation (skills/code-architecture-reference.md) has outdated values. Current actual values from config.yaml and code:
- Optimizer: **AdamW** (not Adam)
- Base LR: **2e-4** (not 1e-4)
- Gradient clipping: **max_norm=5.0** (not 1.0)
- Early stopping patience: **10** (not 5)
- Label smoothing: **0.0** (not 0.02)
- FreqCNN depth: **5** (not 3), with **residual connections** (FreqBlock)
- Spatial augmentation: includes **ColorJitter** and **RandomErasing**
- FFT augmentation: includes **spectral band masking** (15% probability)
- Loss: includes **pos_weight** for class imbalance
- Classifier dropout: **0.3/0.3** (not 0.5/0.3)
- Backbone freezing: applies to **spatial model too** (not just hybrid)
