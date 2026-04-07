# Code Architecture Reference — Deepfake Hybrid Detection

> **When to use:** When writing BAB III (methodology), BAB IV (results), or any thesis section that needs accurate technical details about the implementation. Use this as the single source of truth for code behavior, parameters, architecture, and data flow.

---

## 1. Configuration (`config.yaml`)

### Path & Frame Extraction
| Parameter | Value | Purpose |
|---|---|---|
| `output_root` | `"./outputs"` | Base directory for all outputs |
| `frame_sampling_fps` | `5` | Frames per second extracted from video |
| `max_frames_per_video` | `50` | Cap on frames per video |
| `image_size` | `224` | Standardized input resolution (224×224) |

### Training Hyperparameters
| Parameter | Value | Purpose |
|---|---|---|
| `batch_size` | `16` | Training batch size |
| `lr` | `2e-4` | AdamW learning rate |
| `weight_decay` | `1e-4` | Decoupled weight decay (AdamW) |
| `epochs` | `30` | Maximum training epochs |
| `early_stop_patience` | `10` | Epochs without AUC improvement before stopping |
| `accum_steps` | `2` | Gradient accumulation (effective batch = 32) |
| `label_smoothing` | `0.0` | Disabled (hard labels) |
| `n_seeds` | `3` | Number of random seeds for multi-run experiments |

### Frequency Branch Config
| Parameter | Value | Purpose |
|---|---|---|
| `freq_depth` | `5` | FreqCNN residual blocks (~700K params) |
| `freq_base_channels` | `32` | Initial channels (doubled per block, capped at 256) |
| `fft_noise_sigma` | `0.05` | Gaussian noise σ for FFT augmentation during training |

### Dataset Config
| Dataset | Root | Real Keywords | Fake Keywords |
|---|---|---|---|
| FFPP | `./dataset/face_forensics` | original, real, pristine, actors, youtube | fake, manipulated, deepfakes, faceswap, neuraltextures, etc. |
| CDF | `./dataset/celeb_df` | real, authentic | fake, synthesis, deepfake |

### Sample Sizes per Dataset
- **FFPP:** [100, 300, 600, 1000]
- **CDF:** [100, 250, 500, 750]

---

## 2. Source Code Modules

### 2.1 `src/utils.py` — Utility Functions

| Function | Signature | Purpose |
|---|---|---|
| `seed_everything` | `(seed=42, deterministic=True)` | Seeds Python, NumPy, PyTorch (including CUDA). Disables cudnn.benchmark if deterministic. |
| `get_device` | `() → torch.device` | Returns `cuda` if available, else `cpu` |
| `setup_logging` | `(log_path, level)` | Console + optional file logging, format: `[timestamp] LEVEL: message` |
| `load_config` | `(path) → dict` | `yaml.safe_load()` wrapper |
| `save_json` | `(obj, path)` | JSON with 2-space indent, auto-creates parent dirs |
| `ensure_dir` | `(path) → Path` | `mkdir(parents=True, exist_ok=True)` |
| `make_video_id` | `(video_path, root) → str` | Format: `{stem}_{md5(relative_path)[:8]}` — unique ID per video |
| `worker_init_fn` | `(worker_id)` | Seeds NumPy/random per DataLoader worker for reproducibility |
| `get_num_workers` | `(cfg) → int` | Config value, or `os.cpu_count()`, or 4 fallback |
| `env_info` | `() → dict` | Returns hostname, cuda availability, GPU count, torch version |

### 2.2 `src/fft_utils.py` — FFT Processing

| Function | Signature | Purpose |
|---|---|---|
| `image_to_fft_logmag` | `(img: PIL.Image, size=224) → np.ndarray` | **Core FFT pipeline:** RGB→grayscale→resize→FFT2D→fftshift→abs→log1p. Returns float32 (224×224). |
| `tensor_fft_logmag` | `(img_tensor: Tensor) → Tensor` | GPU-compatible FFT via `torch.fft.fft2`. Grayscale = channel average (not ITU-R 601). |
| `save_fft_cache` | `(img_path, out_path, size=224)` | Load image → compute FFT logmag → save as `.npy` |
| `load_fft_cache` | `(path) → np.ndarray` | `np.load()` wrapper |
| `pad_to_size` | `(tensor, size) → Tensor` | Reflection padding to target size |

**FFT Pipeline Detail (for BAB III manual calculation):**
1. Convert RGB to grayscale: `Y = 0.299R + 0.587G + 0.114B` (ITU-R 601)
2. Resize to 224×224
3. 2D FFT: `F(u,v) = Σ_x Σ_y f(x,y) · e^{-j2π(ux/M + vy/N)}`
4. Center shift: `fftshift()` moves DC component (0,0) to center
5. Magnitude: `|F(u,v)| = √(Re² + Im²)`
6. Log scaling: `log(1 + |F(u,v)|)` — compresses dynamic range, prevents log(0)
7. Output: float32 array, values typically range [0, ~16]

### 2.3 `src/transforms.py` — Data Augmentation

**Constants:**
- `IMAGENET_MEAN = [0.485, 0.456, 0.406]`
- `IMAGENET_STD = [0.229, 0.224, 0.225]`

**`get_spatial_transform(image_size=224, train=True, include_hflip=True)`**

| Mode | Pipeline |
|---|---|
| **Training** | Resize(256×256) → RandomResizedCrop(224, scale=0.8–1.0) → [RandomHorizontalFlip] → ToTensor → Normalize(ImageNet) |
| **Validation/Test** | Resize(224×224) → ToTensor → Normalize(ImageNet) |

- `include_hflip=False` for hybrid mode (flip applied manually to both branches)

**`stack_rgb_fft(rgb, fft) → Tensor`**
- Concatenates RGB (3,H,W) + FFT (1,H,W) → (4,H,W) for early fusion

### 2.4 `src/metrics.py` — Evaluation Metrics

| Function | Returns | Notes |
|---|---|---|
| `compute_metrics(y_true, y_prob, threshold=0.5)` | `{tp, tn, fp, fn, acc, precision, recall, f1, auc}` | Uses sklearn. AUC = NaN if single class. zero_division=0. |
| `roc_points(y_true, y_prob)` | `(fpr, tpr, thresholds)` | For ROC curve plotting |
| `find_optimal_threshold(y_true, y_prob)` | `float` | Youden's J = max(TPR − FPR). Balances sensitivity/specificity. |

**Primary model selection metric:** AUC (used for early stopping + best checkpoint)

### 2.5 `src/deepfake_data.py` — Dataset Class

**Constants:**
- `IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}`
- `_FFT_MEAN_FALLBACK = 5.0`, `_FFT_STD_FALLBACK = 3.0`

**`load_fft_stats(fft_cache_root) → (mean, std)`**
- Reads `fft_stats.json` from cache directory
- Falls back to 5.0/3.0 with warning if missing

**`DatasetConfig` (dataclass)**
| Field | Type | Purpose |
|---|---|---|
| `manifest_path` | Path | CSV: video_id, label, frames_dir |
| `fft_cache_root` | Optional[Path] | FFT cache directory |
| `image_size` | int | Target resolution (224) |
| `max_frames_per_video` | int | 0 = use all |
| `mode` | str | "spatial" / "freq" / "hybrid" / "early_fusion" |
| `seed` | int | Reproducible frame sampling (default 42) |
| `train` | bool | Enable augmentation |
| `fft_noise_sigma` | float | Gaussian noise for FFT (default 0.05) |

**`DeepfakeDataset(Dataset)` — Core Data Loading**

**`__init__`:**
1. Load manifest CSV → list of (video_id, label, frames_dir)
2. For each video: list image files, sample up to max_frames (seeded RNG)
3. Build items list: `[(frame_path, label, video_id), ...]`
4. Load FFT normalization stats from `fft_stats.json`
5. Create spatial transform (hybrid: `include_hflip=False`)

**`__getitem__(idx)` — Return format by mode:**

| Mode | Returns | Details |
|---|---|---|
| `spatial` | `(img_tensor, label)` | RGB (3,224,224) ImageNet-normalized |
| `freq` | `(fft_tensor, label)` | FFT (1,224,224) z-score normalized + noise |
| `early_fusion` | `(fused_tensor, label)` | 4-channel (4,224,224) via `stack_rgb_fft` |
| `hybrid` | `({"image": img, "fft": fft}, label)` | Both tensors + consistent random hflip |

**FFT normalization pipeline (in `__getitem__`):**
1. Load from `.npy` cache → tensor (1,224,224)
2. Z-score normalize: `(fft - mean) / std` (per-dataset stats)
3. If training & sigma > 0: add Gaussian noise `fft + randn * sigma`

**Hybrid mode augmentation consistency:**
- Random horizontal flip with 50% probability
- Same flip applied to BOTH RGB tensor and FFT tensor
- Ensures spatial-frequency correspondence is maintained

---

## 3. Model Architectures

### 3.1 Spatial Model — `src/models/spatial_xception.py`

**`build_xception(num_classes=1, in_chans=3, pretrained=True)`**
- Uses `timm.create_model("xception", ...)` with ImageNet pretrained weights
- Global average pooling → single logit output
- For early fusion: `in_chans=4` (RGB + FFT)

**`build_feature_extractor(in_chans=3, pretrained=True)`**
- XceptionNet with `num_classes=0` — returns feature vector only
- Output dimension: ~2048 (queried via `get_feature_dim()`)
- Used by HybridTwoBranch as spatial branch

**XceptionNet Architecture Highlights:**
- Depthwise separable convolutions (efficient parameter usage)
- ~22.8M parameters (full model)
- Proven effective on FaceForensics++ benchmark
- ImageNet pretraining provides strong visual feature foundation

### 3.2 Frequency Model — `src/models/freq_cnn.py`

**`FreqCNN(num_classes=1, depth=3, base_channels=32)`**

**Channel progression:** `[base_channels × 2^i]` capped at `base_channels × 8`

| Config | Channels | Feature Dim | Params | Spatial Progression (224→) |
|---|---|---|---|---|
| depth=3, base=32 | [32, 64, 128] | 128 | ~130K | 224→112→56→28→1 (pool) |
| depth=5, base=32 | [32, 64, 128, 256, 256] | 256 | ~700K | 224→112→56→28→14→7→1 (pool) |

**Each convolutional block:**
```
Conv2d(in_ch, out_ch, kernel_size=3, padding=1) → BatchNorm2d → ReLU → MaxPool2d(2)
```

**Regularization:** Dropout2d(0.2) on feature maps, Dropout(0.3) in classifier

**Classifier head:**
```
Flatten → Linear(feat_dim, feat_dim//2) → ReLU → Dropout(0.3) → Linear(→1)
```

**`feature_dim()`** — returns `_feature_dim` (128 or 256) for hybrid projection sizing

### 3.3 Hybrid Fusion — `src/models/hybrid_fusion.py`

**Constant:** `PROJ_DIM = 256` (projection dimension for both branches)

#### SEGate (Squeeze-and-Excitation Gating)
```
Linear(512→128) → ReLU → Linear(128→512) → Sigmoid
Forward: x * gate(x)  # element-wise learned weighting
```
- Learns per-dimension importance of fused features
- ~131K parameters (negligible vs XceptionNet)
- Based on Hu et al., 2018

#### HybridTwoBranch (Late Fusion)

**Architecture:**
```
RGB (3,224,224) ──→ XceptionNet backbone ──→ (B, 2048) ──→ spatial_proj ──→ (B, 256) ─┐
                                                                                        ├──→ concat (B, 512) → SEGate → Classifier → logit
FFT (1,224,224) ──→ FreqCNN.features ──→ (B, freq_dim) ──→ freq_proj ──→ (B, 256) ────┘
```

**Projection layers (both branches):**
```
Linear(input_dim → 256) → BatchNorm1d(256) → ReLU
```
- Spatial: 2048→256 (compression)
- Frequency: 128/256→256 (transform/identity)

**Classifier:**
```
Dropout(0.5) → Linear(512→128) → ReLU → Dropout(0.3) → Linear(128→1)
```

**`forward(rgb, fft)`:**
1. `spatial_feat = self.spatial(rgb)` → (B, 2048)
2. `freq_feat = self.freq.features(fft)` → (B, freq_dim, 1, 1) → flatten → (B, freq_dim)
3. Project both to 256-dim
4. Concatenate → (B, 512)
5. SE gating → (B, 512)
6. Classify → logit

#### EarlyFusionXception

**Architecture:**
```
Stacked [RGB + FFT] (4,224,224) → XceptionNet(in_chans=4) → logit
```
- Single backbone processes all 4 channels together
- Pretrained ImageNet weights; 4th channel initialized randomly by timm
- Simpler than late fusion; fewer parameters

---

## 4. Training Pipeline (`scripts/train.py`)

### Model Selection
| Mode | Model | Input |
|---|---|---|
| `spatial` | `build_xception(1, 3, pretrained)` | RGB (3,224,224) |
| `freq` | `FreqCNN(1, depth, base_channels)` | FFT (1,224,224) |
| `hybrid` | `HybridTwoBranch(pretrained, depth, base_ch)` | dict: {image, fft} |
| `early_fusion` | `EarlyFusionXception(pretrained)` | Stacked (4,224,224) |

### Differential Learning Rates
| Parameter Group | LR | Applies To |
|---|---|---|
| Backbone | `lr / 10 = 1e-5` | XceptionNet pretrained params (hybrid, early_fusion) |
| Head | `lr = 1e-4` | Projections, SE gate, classifier, FreqCNN |

### Backbone Freezing
- **FREEZE_EPOCHS = 3** (hybrid and early_fusion only)
- Epochs 1–3: spatial backbone parameters frozen (requires_grad=False)
- Epoch 4+: unfrozen, trained with backbone_lr (1e-5)
- Purpose: let head layers warm up before fine-tuning pretrained backbone

### Learning Rate Schedule
```
Epoch 1-2: Linear warmup (10% → 100% of base LR)
Epoch 3+:  Cosine annealing decay (base LR → 1e-6)
```
- Implemented via `SequentialLR([LinearLR, CosineAnnealingLR], milestones=[2])`

### Training Loop (per epoch)
1. For each batch:
   - Forward pass → logits
   - Label smoothing: `targets = targets * (1 - 0.02) + 0.02 * 0.5`
   - Loss: `BCEWithLogitsLoss(logits, smoothed_targets)`
   - Loss scaled by `1 / accum_steps`
   - AMP (mixed precision) on CUDA with `GradScaler`
2. Every `accum_steps` batches:
   - `scaler.unscale_(optimizer)`
   - `clip_grad_norm_(model.parameters(), max_norm=1.0)`
   - `scaler.step(optimizer)` + `scaler.update()`
3. End of epoch: `scheduler.step()`
4. Validate → compute metrics → check early stopping (patience=5 on AUC)
5. Save checkpoint if val_auc improves: `{"state_dict": ..., "epoch": ..., "config": ...}`

### Mixed Precision & Hardware Optimizations
- AMP (`autocast` + `GradScaler`) on CUDA
- TF32 enabled for Ampere+ GPUs: `torch.backends.cuda.matmul.allow_tf32 = True`
- `torch.backends.cudnn.allow_tf32 = True`

---

## 5. Scripts Pipeline

### 5.1 `extract_frames.py`
- **Input:** Video files from dataset root
- **Process:** OpenCV frame extraction at target FPS, label inference from directory keywords
- **Sampling:** If `--n-samples` > 0, balanced sampling (50/50 real/fake)
- **Output:** `outputs/frames/{DATASET}/{video_id}/frame_XXXXXX.jpg` + `outputs/manifests/{DATASET}/manifest.csv`

### 5.2 `build_splits.py`
- **Input:** `manifest.csv`
- **Process:** Stratified split by video_id (NOT frame) — prevents data leakage
- **Ratios:** Train 70% / Val 15% / Test 15%
- **Output:** `train.csv`, `val.csv`, `test.csv` in manifests directory
- **Validation:** Checks for duplicate video_ids, minimum 4 samples per class

### 5.3 `compute_fft_cache.py`
- **Input:** Frame images from manifest
- **Process:** Parallel FFT computation via multiprocessing → `.npy` cache files
- **Stats:** Auto-computes global mean/std from up to 5000 random cache files (Welford-style)
- **Output:** `outputs/fft_cache/{DATASET}/{video_id}/{frame}.npy` + `fft_stats.json`
- **Flags:** `--force` recomputes all, `--stats` only recomputes statistics

### 5.4 `train.py`
- **Input:** Train/val manifests, FFT cache, config
- **Process:** Full training loop with all features described in Section 4
- **Output:** `outputs/runs/{model}_{dataset}_n{n}_seed{seed}/best.pt` + `metrics.json` + `train.log`

### 5.5 `eval.py`
- **Input:** Checkpoint + test manifest
- **Process:** Inference → metrics at threshold=0.5 and optimal (Youden's J)
- **Output:** Metrics JSON + console report

### 5.6 `run_all.py`
- **Input:** Config
- **Process:** Full experiment matrix: all models × datasets × seeds
- **Evaluates:** In-dataset AND cross-dataset (train FFPP→test CDF, train CDF→test FFPP)
- **Output:** Three CSV tables:
  - `Table1_in_dataset.csv` — in-dataset metrics
  - `Table2_cross_dataset.csv` — cross-dataset metrics
  - `Table3_generalization_drop.csv` — F1 drop analysis

### 5.7 `plot_results.py`
- **Input:** metrics.json + result CSVs
- **Output:** PNG plots (300 DPI): training curves, model comparison bars, generalization drop, sample-size scaling

### 5.8 `run_pipeline.py` (Master Orchestrator)
- Runs entire pipeline end-to-end via subprocess calls
- Creates temporary `.pipeline_config.yaml` with CLI overrides
- Order: extract_frames → build_splits → compute_fft_cache → run_all

---

## 6. Data Flow Diagram

```
Videos (FFPP/CDF roots)
       │
       ▼
  extract_frames.py ─────────→ outputs/frames/{DS}/{video_id}/frame_*.jpg
       │                        outputs/manifests/{DS}/manifest.csv
       ▼
  build_splits.py ────────────→ train.csv, val.csv, test.csv
       │
       ▼
  compute_fft_cache.py ───────→ outputs/fft_cache/{DS}/{video_id}/*.npy
       │                        outputs/fft_cache/{DS}/fft_stats.json
       ▼
  DeepfakeDataset.__getitem__()
       │
       ├─ spatial: RGB → Resize+Crop+Normalize → (3,224,224)
       ├─ freq:    .npy → z-score normalize + noise → (1,224,224)
       ├─ hybrid:  both, consistent hflip → {"image": (3,H,W), "fft": (1,H,W)}
       └─ early:   stack → (4,224,224)
       │
       ▼
  train.py ───────────────────→ outputs/runs/{model}_{ds}_n{n}_seed{s}/
       │                        ├── best.pt (checkpoint)
       │                        ├── metrics.json (training history)
       │                        └── train.log
       ▼
  run_all.py / eval.py ──────→ outputs/tables/n{n}/
       │                        ├── Table1_in_dataset.csv
       │                        ├── Table2_cross_dataset.csv
       │                        └── Table3_generalization_drop.csv
       ▼
  plot_results.py ────────────→ outputs/plots/*.png
```

---

## 7. Key Design Patterns

### Pattern 1: Transfer Learning with Progressive Unfreezing
- XceptionNet pretrained on ImageNet
- Frozen for 3 epochs → unfrozen with 10× lower LR
- Prevents catastrophic forgetting of visual features

### Pattern 2: Modality-Specific Normalization
- RGB: ImageNet stats (mean/std from 1M images)
- FFT: Per-dataset stats computed from cache (z-score)
- Prevents scale mismatch at fusion

### Pattern 3: Consistent Cross-Modal Augmentation (Hybrid)
- Horizontal flip applied to BOTH RGB and FFT with same random decision
- Ensures spatial-frequency alignment during training

### Pattern 4: Dimension-Balanced Fusion
- Both branches projected to PROJ_DIM=256 before concatenation
- Prevents 2048-dim spatial from dominating 128-dim frequency
- SE gating learns per-feature importance

### Pattern 5: Multi-Level Regularization
- Label smoothing (0.02) — prevents overconfident predictions
- Gradient clipping (max_norm=1.0) — stability at unfreeze boundary
- Dropout cascade: 0.5 → 0.3 in classifier
- Dropout2d(0.2) in FreqCNN features
- Weight decay (1e-4)
- Early stopping (patience=5)

### Pattern 6: Video-Level Data Integrity
- Splits by video_id, not frame — prevents frame leakage
- All frames from same video share label and split
- Stratified splitting maintains class balance

### Pattern 7: Reproducibility Guarantees
- `seed_everything(42)` — Python, NumPy, PyTorch, CUDA
- `worker_init_fn` — per-worker DataLoader seeding
- Deterministic frame sampling via seeded RNG
- Deterministic splits via sklearn seed

---

## 8. Fixes & Improvements Applied (from documentation/)

### Critical Fixes
| Fix | Before | After | Impact |
|---|---|---|---|
| Feature dimension balancing | Spatial 2048 vs Freq 64 (32:1 ratio) | Both projected to 256 via learned layers + BatchNorm | Balanced fusion |
| FFT normalization | Per-image min-max or wrong constants (0.5/0.5) | Per-dataset stats from fft_stats.json | Correct input scaling |
| Cosine scheduler wraparound | T_max=epochs-freeze, wrapped around | SequentialLR: warmup(2) + cosine(remaining) | Monotonic LR decay |
| Augmentation asymmetry | RGB flipped, FFT not | Consistent flip applied to both | Preserved spatial-freq correspondence |

### Architecture Improvements
| Change | Before | After |
|---|---|---|
| FreqCNN depth | 3 layers, 64-dim output | Configurable 3 or 5 layers, 128/256-dim |
| Fusion gating | Simple concatenation | SE (Squeeze-and-Excitation) attention |
| Dropout in classifier | Single dropout | Cascade: Dropout(0.5) → FC → Dropout(0.3) → FC |

### Training Stability
| Change | Purpose |
|---|---|
| Gradient clipping (max_norm=1.0) | Prevents gradient explosion at unfreeze boundary |
| LR warmup (2 epochs, 10%→100%) | Reduces initial weight shock |
| FFT Gaussian noise (σ=0.05) | Prevents freq branch memorization |
| Label smoothing (0.02) | Reduces overconfident predictions |
| Per-epoch LR logging | Observability / debugging |

---

## 9. Experiment Design

### Experiment Matrix
- **Models:** spatial, freq, hybrid (3 models)
- **Datasets:** FFPP, CDF (2 datasets)
- **Sample sizes:** FFPP [100,300,600,1000], CDF [100,250,500,750]
- **Seeds:** 3 seeds (0, 1, 2) for mean±std
- **Evaluation:** In-dataset + cross-dataset (6 combinations per sample size)

### Cross-Dataset Protocol
- Train on FFPP → Test on CDF (and vice versa)
- Measures generalization beyond training distribution
- Generalization drop = F1_in - F1_cross

### Metrics Reported
| Metric | Formula | Role |
|---|---|---|
| Accuracy | (TP+TN) / (TP+TN+FP+FN) | Overall performance |
| Precision | TP / (TP+FP) | False positive control |
| Recall | TP / (TP+FN) | Detection coverage |
| F1-Score | 2·P·R / (P+R) | Harmonic mean |
| AUC | Area under ROC curve | **Primary** — threshold-independent ranking |
