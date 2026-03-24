# BAB III Complete Rewrite Plan — Tahapan Pelaksanaan

**Date:** 2026-03-24
**Purpose:** Comprehensive plan for rewriting BAB III from scratch, informed by:
- Past analysis (`BAB_III_vs_Code_Cross_Check_2026-03-14`)
- All documentation fixes (`documentation/` — 4 files, 40+ fixes)
- Deep code analysis (all `src/` and `scripts/` modules)
- Reference thesis structure (Chrisandy et al. — BiLSTM+Attention STS)
- BAB III guideline mapping (`people_thesis/chrisandy_sandy_fahim/bab3_guideline_for_deepfake_hybrid.md`)
- Current BAB III content (lines 1855–2203 of main document)

---

## PART A: WHY A REWRITE IS NEEDED

### Problems with Current BAB III

The existing BAB III (lines 1855–2203, ~350 lines / ~15 pages) has these fundamental issues:

1. **Outdated architecture description:** Describes early_fusion as the primary model (4-channel RGB+FFT → Conv1×1 adapter → XceptionNet). The actual codebase now has 3 model types (spatial, freq, hybrid) as the core experiment matrix, with hybrid (late fusion with SE gating) as the main contribution.

2. **Missing critical components:**
   - No mention of FreqCNN architecture at all
   - No mention of HybridTwoBranch late fusion
   - No SE (Squeeze-and-Excitation) gating
   - No projection layers or dimension balancing
   - No differential learning rates
   - No backbone freezing strategy
   - No LR schedule (warmup + cosine)
   - No gradient accumulation or clipping
   - No FFT normalization (per-dataset stats)
   - No label smoothing
   - No early stopping on AUC
   - No cross-dataset evaluation methodology
   - No Celeb-DF dataset description
   - No multi-sample-size experiment design
   - No AUC metric (only mentions accuracy and loss)

3. **Incorrect details:**
   - Says image_size is 256×256 (actual: 224×224)
   - Says batch_size is 32 (actual: 16, effective 32 via accumulation)
   - Says epochs is 100 (actual: 30 with early stopping)
   - Describes Conv1×1 channel adapter that doesn't exist in current code
   - Describes early stopping based on accuracy > 95% (actual: AUC patience=5)
   - Only describes FaceForensics++ (missing Celeb-DF)

4. **Missing manual calculations:** Reference thesis (Chrisandy) dedicates ~28 pages to step-by-step calculations. Current BAB III has zero.

5. **Missing visual elements:** No flowcharts, no architecture diagrams, no dataset examples, no comparison tables.

**Verdict:** BAB III needs a complete rewrite to match the actual implemented system.

---

## PART B: PROPOSED STRUCTURE

### Estimated Length: 40–50 pages

Following Chrisandy's pattern and Mikroskil thesis conventions:

```
BAB III TAHAPAN PELAKSANAAN

3.1 Kerangka Tahapan Pelaksanaan .......................... (~3 pages)
    3.1.1 Jenis dan Pendekatan Penelitian
    3.1.2 Tahapan Pelaksanaan Penelitian
    [Gambar 3.1: Flowchart Utama Pipeline]

3.2 Dataset dan Sumber Data ............................... (~5 pages)
    3.2.1 FaceForensics++ (FFPP)
    3.2.2 Celeb-DF v2 (CDF)
    3.2.3 Pembagian Dataset (Train/Val/Test Split)
    3.2.4 Variasi Ukuran Sampel
    [Tabel 3.1: Statistik Dataset]
    [Tabel 3.2: Pembagian Data per Split]
    [Gambar 3.2: Contoh Frame Real vs Fake (RGB)]

3.3 Tahapan Preprocessing Data ............................ (~8 pages)
    3.3.1 Ekstraksi Frame dari Video
    3.3.2 Konversi Domain Frekuensi (FFT)
        3.3.2.1 Konversi RGB ke Grayscale
        3.3.2.2 Transformasi Fourier 2D
        3.3.2.3 Magnitude Spectrum dan Log Scaling
        3.3.2.4 Normalisasi FFT
    3.3.3 Augmentasi Data
        3.3.3.1 Augmentasi Domain Spasial
        3.3.3.2 Augmentasi Domain Frekuensi
        3.3.3.3 Konsistensi Augmentasi pada Mode Hybrid
    [Gambar 3.3: Flowchart Preprocessing]
    [Gambar 3.4: Perbandingan FFT Real vs Fake]
    [Tabel 3.3: Contoh Perhitungan FFT 4×4]

3.4 Arsitektur Model yang Diusulkan ........................ (~12 pages)
    3.4.1 Model Spasial — XceptionNet
        3.4.1.1 Depthwise Separable Convolution
        3.4.1.2 Transfer Learning dari ImageNet
    3.4.2 Model Frekuensi — FreqCNN
        3.4.2.1 Arsitektur Konvolusional
        3.4.2.2 Contoh Perhitungan Forward Pass
    3.4.3 Model Hybrid — HybridTwoBranch (Late Fusion)
        3.4.3.1 Cabang Spasial (XceptionNet Backbone)
        3.4.3.2 Cabang Frekuensi (FreqCNN Backbone)
        3.4.3.3 Projection Layers dan Penyeimbangan Dimensi
        3.4.3.4 Squeeze-and-Excitation (SE) Gating
        3.4.3.5 Classifier Head
        3.4.3.6 Contoh Perhitungan Late Fusion
    3.4.4 Perbandingan Arsitektur Model
    [Gambar 3.5: Diagram Arsitektur XceptionNet]
    [Gambar 3.6: Diagram Arsitektur FreqCNN]
    [Gambar 3.7: Diagram Arsitektur HybridTwoBranch]
    [Tabel 3.4: Layer-by-Layer FreqCNN]
    [Tabel 3.5: Perbandingan 3 Arsitektur]
    [Tabel 3.6: Dimensi Fitur per Komponen Hybrid]

3.5 Strategi Pelatihan Model ............................... (~8 pages)
    3.5.1 Transfer Learning dan Backbone Freezing
    3.5.2 Differential Learning Rate
    3.5.3 Penjadwalan Learning Rate (Warmup + Cosine Decay)
    3.5.4 Fungsi Loss — BCEWithLogitsLoss dengan Label Smoothing
        3.5.4.1 Contoh Perhitungan BCEWithLogitsLoss
    3.5.5 Optimisasi — Adam dengan Gradient Accumulation
    3.5.6 Gradient Clipping
    3.5.7 Mixed Precision Training (AMP)
    3.5.8 Early Stopping
    3.5.9 Seleksi Model Terbaik (Checkpoint)
    [Tabel 3.7: Hyperparameter Pelatihan]
    [Tabel 3.8: Learning Rate per Parameter Group]
    [Gambar 3.8: Kurva Learning Rate Schedule]

3.6 Desain Eksperimen ..................................... (~4 pages)
    3.6.1 Matriks Eksperimen
    3.6.2 Evaluasi In-Dataset
    3.6.3 Evaluasi Cross-Dataset
    3.6.4 Variabel Penelitian
    [Tabel 3.9: Matriks Eksperimen Lengkap]
    [Tabel 3.10: Variabel Independen, Dependen, dan Kontrol]

3.7 Metode Evaluasi Model ................................. (~4 pages)
    3.7.1 Confusion Matrix
    3.7.2 Accuracy
    3.7.3 Precision
    3.7.4 Recall
    3.7.5 F1-Score
    3.7.6 AUC-ROC
    3.7.7 Generalization Drop
    3.7.8 Contoh Perhitungan Metrik dari Confusion Matrix
    [Tabel 3.11: Confusion Matrix Template]
    [Tabel 3.12: Contoh Perhitungan Metrik]
```

---

## PART C: DETAILED CONTENT PLAN PER SECTION

### 3.1 Kerangka Tahapan Pelaksanaan (~3 pages)

#### 3.1.1 Jenis dan Pendekatan Penelitian
**Content:**
- Penelitian eksperimental di bidang computer vision dan deep learning
- Fokus: perancangan, implementasi, evaluasi model deteksi deepfake
- Pendekatan hybrid yang menggabungkan analisis spasial (XceptionNet) dan analisis frekuensi (FFT + FreqCNN)

**Key sentences:**
- Justify why experimental approach (controlled variables, replicable)
- Justify why hybrid approach (complementary information, spatial catches texture/structure, frequency catches spectral artifacts invisible to human eye)
- State 3 model variants as deliberate experimental design (spatial-only, freq-only, hybrid) to measure individual and combined contribution

#### 3.1.2 Tahapan Pelaksanaan Penelitian
**Content — 5 stages:**
1. Pengumpulan Data — FaceForensics++ dan Celeb-DF
2. Preprocessing — Frame extraction, FFT conversion, normalization
3. Perancangan Model — 3 architectures (spatial, freq, hybrid)
4. Pelatihan dan Optimasi — Transfer learning, differential LR, early stopping
5. Pengujian dan Evaluasi — In-dataset, cross-dataset, multi-sample-size

**Visual:** Gambar 3.1 — Master flowchart showing entire pipeline from data collection through evaluation. Should show:
```
Dataset Videos → Frame Extraction → FFT Computation → Dataset Split
     ↓
Model Training (Spatial / Freq / Hybrid) → Validation → Best Checkpoint
     ↓
Evaluation (In-dataset + Cross-dataset) → Result Tables → Analysis
```

---

### 3.2 Dataset dan Sumber Data (~5 pages)

#### 3.2.1 FaceForensics++ (FFPP)
**Content from code:**
- Introduced by Rössler et al., benchmark standard for deepfake detection
- Contains original YouTube videos + manipulated versions
- 4 manipulation methods: Deepfakes, Face2Face, FaceSwap, NeuralTextures
- Videos labeled via directory name keyword matching (code uses `real_keywords` and `fake_keywords` from config)
- Compression level used: c23 (light compression, realistic scenario)

#### 3.2.2 Celeb-DF v2 (CDF)
**Content from code:**
- Introduced by Li et al., celebrity-based deepfake dataset
- Higher quality deepfakes than FFPP (less visible artifacts)
- Single synthesis method (face swapping)
- Used for cross-dataset generalization testing
- Keywords: real/authentic vs fake/synthesis/deepfake

#### 3.2.3 Pembagian Dataset
**Content from code (`build_splits.py`):**
- Split by **video_id** (not frame) — prevents data leakage
- Stratified split maintaining class balance (real/fake ratio preserved)
- Ratios: Train 70% / Validation 15% / Test 15%
- Uses `sklearn.model_selection.train_test_split` with `stratify=label`
- Seed = 42 for reproducibility
- Validation: minimum 4 samples per class required

**Tabel 3.1: Statistik Dataset**
| | FFPP | CDF |
|---|---|---|
| Total video (varies by n_samples) | ... | ... |
| Metode manipulasi | 4 (Deepfakes, Face2Face, FaceSwap, NeuralTextures) | 1 (face swapping) |
| Resolusi asli | Varies | Varies |
| Kompresi | c23 | Original |
| Label | real/fake (binary) | real/fake (binary) |

**Tabel 3.2: Pembagian Data per Split**
| Split | Proporsi | Stratifikasi | Level |
|---|---|---|---|
| Training | 70% | By label | Video-level |
| Validation | 15% | By label | Video-level |
| Testing | 15% | By label | Video-level |

#### 3.2.4 Variasi Ukuran Sampel
**Content from code:**
- FFPP: [100, 300, 600, 1000] video samples
- CDF: [100, 250, 500, 750] video samples
- Purpose: measure model robustness at different data scales
- Balanced sampling: 50/50 real/fake per sample size
- Frame extraction: up to 50 frames per video at 5 FPS

**Gambar 3.2:** Side-by-side comparison of real vs fake frames (RGB images) from both FFPP and CDF datasets.

---

### 3.3 Tahapan Preprocessing Data (~8 pages)

#### 3.3.1 Ekstraksi Frame dari Video
**Content from code (`extract_frames.py`):**
- Videos → frames at configurable FPS (default: 5 FPS)
- Max 50 frames per video (`max_frames_per_video`)
- Frame interval = `max(int(video_fps / target_fps), 1)`
- Frames saved as JPEG: `frame_000000.jpg`, `frame_000001.jpg`, ...
- Label inferred from directory name via keyword matching
- Parallel extraction using multiprocessing pool
- Output: manifest CSV with columns (video_id, label, frames_dir)

**Gambar 3.3:** Flowchart of preprocessing pipeline:
```
Video → OpenCV → Frame sampling (5 FPS) → Resize → JPEG save
                                                  ↓
                                        Manifest CSV generation
                                                  ↓
                         RGB frame → Grayscale → FFT 2D → fftshift → |F| → log1p → .npy cache
```

#### 3.3.2 Konversi Domain Frekuensi (FFT)

**THIS IS THE CORE CONTRIBUTION — WRITE IN MAXIMUM DETAIL**

**Content from code (`fft_utils.py`):**

##### 3.3.2.1 Konversi RGB ke Grayscale
- Formula: `Y = 0.299R + 0.587G + 0.114B` (ITU-R 601 standard)
- Implemented via `PIL.Image.convert("L")`
- Single channel preserves luminance information sufficient for spectral analysis

##### 3.3.2.2 Transformasi Fourier 2D
- Resize grayscale image to 224×224
- Apply 2D DFT: `F(u,v) = Σ_{x=0}^{M-1} Σ_{y=0}^{N-1} f(x,y) · e^{-j2π(ux/M + vy/N)}`
- Implemented via `np.fft.fft2(arr)`
- Shift zero frequency to center: `np.fft.fftshift(fft)` — low frequencies at center, high at edges
- Purpose: deepfake artifacts often appear as anomalous patterns in frequency domain (spectral distortions, checkerboard artifacts from upsampling, blending boundary artifacts)

##### 3.3.2.3 Magnitude Spectrum dan Log Scaling
- Magnitude: `|F(u,v)| = √(Re(F)² + Im(F)²)`
- Log scaling: `log(1 + |F(u,v)|)` — compresses dynamic range (DC component can be orders of magnitude larger)
- `log1p` prevents log(0) issues
- Output range: approximately [0, 16] for typical face images
- Saved as `.npy` float32 cache files

##### 3.3.2.4 Normalisasi FFT
- Per-dataset z-score normalization: `(x - μ) / σ`
- Statistics computed from up to 5000 random cache files per dataset
- Saved to `fft_stats.json`: `{"mean": float, "std": float}`
- Applied at training time in `DeepfakeDataset.__getitem__`
- Fallback values: mean=5.0, std=3.0 (if stats file missing)

**MANUAL CALCULATION (following Chrisandy's pattern):**

**Tabel 3.3: Contoh Perhitungan FFT pada Matriks 4×4**

Take a simplified 4×4 grayscale pixel matrix, show:
1. Original pixel values
2. DFT formula application (show at least 2-3 frequency components calculated by hand)
3. Magnitude computation
4. fftshift result
5. log1p result
6. Final normalized values

This should be ~3-4 pages of step-by-step calculation with intermediate tables.

**Gambar 3.4:** Visual comparison showing:
- Real face frame (RGB) → its FFT magnitude (smooth, natural spectral decay)
- Fake face frame (RGB) → its FFT magnitude (artifacts visible as anomalous peaks/patterns)

#### 3.3.3 Augmentasi Data

##### 3.3.3.1 Augmentasi Domain Spasial
**Content from code (`transforms.py`):**
- Training: `Resize(256) → RandomResizedCrop(224, scale=0.8-1.0) → RandomHorizontalFlip → ToTensor → Normalize(ImageNet)`
- Validation/Test: `Resize(224) → ToTensor → Normalize(ImageNet)`
- ImageNet normalization: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]

##### 3.3.3.2 Augmentasi Domain Frekuensi
**Content from code (`deepfake_data.py`):**
- Gaussian noise injection: `fft + randn * σ` where σ=0.05 (configurable via `fft_noise_sigma`)
- Applied after z-score normalization during training only
- Rationale: simulates sensor noise and compression variations; prevents exact memorization of cached FFT maps
- No spatial augmentation (random crop/rotation) for FFT — would destroy frequency localization

##### 3.3.3.3 Konsistensi Augmentasi pada Mode Hybrid
**Content from code (`deepfake_data.py` hybrid mode):**
- Horizontal flip: 50% probability, applied identically to both RGB and FFT tensors
- Critical: flipping RGB without flipping FFT would break spatial-frequency correspondence
- `get_spatial_transform(include_hflip=False)` for hybrid mode — flip applied manually after both branches loaded

---

### 3.4 Arsitektur Model yang Diusulkan (~12 pages)

**THIS IS THE HEAVIEST SECTION — MOST DETAIL NEEDED**

#### 3.4.1 Model Spasial — XceptionNet

##### 3.4.1.1 Depthwise Separable Convolution
- Explain concept: depthwise conv (per-channel) + pointwise conv (1×1 cross-channel)
- Parameter efficiency vs standard convolution
- Formula comparison showing parameter reduction

**MANUAL CALCULATION:**
- Take a small 3×3×3 feature map
- Show standard convolution parameter count vs depthwise separable
- Calculate step-by-step depthwise then pointwise
- ~2-3 pages

##### 3.4.1.2 Transfer Learning dari ImageNet
- Pretrained on ImageNet (1.4M images, 1000 classes)
- `timm.create_model("xception", pretrained=True)`
- Output feature dimension: 2048 (via global average pooling)
- ~22.8M parameters total

#### 3.4.2 Model Frekuensi — FreqCNN

##### 3.4.2.1 Arsitektur Konvolusional
**Content from code (`freq_cnn.py`):**

**Tabel 3.4: Layer-by-Layer FreqCNN (depth=3, base_channels=32)**
| Layer | Type | Input Shape | Output Shape | Parameters |
|---|---|---|---|---|
| Conv Block 1 | Conv2d(1→32, 3×3) + BN + ReLU + MaxPool | (1, 224, 224) | (32, 112, 112) | ~320 |
| Conv Block 2 | Conv2d(32→64, 3×3) + BN + ReLU + MaxPool | (32, 112, 112) | (64, 56, 56) | ~18.5K |
| Conv Block 3 | Conv2d(64→128, 3×3) + BN + ReLU + MaxPool | (64, 56, 56) | (128, 28, 28) | ~73.9K |
| Dropout2d(0.2) | Spatial dropout | (128, 28, 28) | (128, 28, 28) | 0 |
| AdaptiveAvgPool | Global average pool | (128, 28, 28) | (128, 1, 1) | 0 |
| FC 1 | Linear(128→64) + ReLU | (128,) | (64,) | ~8.3K |
| Dropout(0.3) | Dropout | (64,) | (64,) | 0 |
| FC 2 | Linear(64→1) | (64,) | (1,) | ~65 |
| **Total** | | | | **~130K** |

Each conv block: `Conv2d(in, out, kernel_size=3, padding=1) → BatchNorm2d(out) → ReLU → MaxPool2d(2)`

##### 3.4.2.2 Contoh Perhitungan Forward Pass
- Take a small 4×4 single-channel input (simplified FFT)
- Show convolution with 3×3 kernel, padding=1
- Show BatchNorm computation
- Show ReLU activation
- Show MaxPool2d(2) result
- ~2 pages

#### 3.4.3 Model Hybrid — HybridTwoBranch (Late Fusion)

**THIS IS THE MAIN CONTRIBUTION OF THE THESIS**

##### 3.4.3.1 Cabang Spasial
- `build_feature_extractor(pretrained=True)` — XceptionNet with `num_classes=0`
- Input: RGB (3, 224, 224) with ImageNet normalization
- Output: feature vector (batch, 2048)

##### 3.4.3.2 Cabang Frekuensi
- `FreqCNN.features` — convolutional backbone only (no classifier head)
- Input: FFT (1, 224, 224) with z-score normalization
- Output: feature maps → flatten → (batch, freq_dim)
- freq_dim = 128 (depth=3) or 256 (depth=5)

##### 3.4.3.3 Projection Layers dan Penyeimbangan Dimensi
**Content from code (`hybrid_fusion.py`):**
- Problem: spatial (2048-dim) would dominate frequency (128-dim) at 16:1 ratio
- Solution: both projected to `PROJ_DIM = 256`
- Each projection: `Linear(input → 256) → BatchNorm1d(256) → ReLU`
- Spatial: 2048→256 (compression, selects most discriminative features)
- Frequency: 128→256 (learned transformation)

##### 3.4.3.4 Squeeze-and-Excitation (SE) Gating
**Content from code (`hybrid_fusion.py` SEGate class):**
- Based on Hu et al. (2018) — Squeeze-and-Excitation Networks
- Architecture:
  ```
  Input (512) → Linear(512→128) → ReLU → Linear(128→512) → Sigmoid → gate
  Output = input * gate  (element-wise)
  ```
- Squeeze: compress 512-dim to 128 (learn global feature importance)
- Excitation: expand back to 512 with sigmoid (gate weights ∈ [0,1])
- Effect: suppresses noisy/irrelevant features, enhances discriminative ones
- ~131K parameters (negligible overhead)

##### 3.4.3.5 Classifier Head
```
Dropout(0.5) → Linear(512→128) → ReLU → Dropout(0.3) → Linear(128→1)
```
- Heavy initial dropout (0.5) prevents overfitting on fused representation
- Progressive dimension reduction: 512 → 128 → 1
- Output: single logit (passed to BCEWithLogitsLoss)

##### 3.4.3.6 Contoh Perhitungan Late Fusion
**MANUAL CALCULATION (following Chrisandy's pattern):**
1. Take simplified spatial features (e.g., 4-dim vector)
2. Take simplified frequency features (e.g., 4-dim vector)
3. Show projection through Linear + BN + ReLU (both branches)
4. Show concatenation
5. Show SE gating computation (squeeze → excitation → element-wise multiply)
6. Show classifier forward pass → logit → sigmoid → probability
7. ~3-4 pages

#### 3.4.4 Perbandingan Arsitektur Model

**Tabel 3.5: Perbandingan 3 Arsitektur Model**
| Aspek | Spatial (XceptionNet) | Frequency (FreqCNN) | Hybrid (HybridTwoBranch) |
|---|---|---|---|
| Input | RGB (3, 224, 224) | FFT (1, 224, 224) | RGB + FFT (terpisah) |
| Backbone | XceptionNet (pretrained) | FreqCNN (from scratch) | XceptionNet + FreqCNN |
| Feature dim | 2048 | 128 | 256+256 = 512 (projected) |
| Fusion | — | — | Concatenation + SE Gating |
| Parameters | ~22.8M | ~130K | ~23.2M |
| Pretrained | Yes (ImageNet) | No | Partial (spatial only) |
| Domain | Spatial | Frequency | Both |

**Tabel 3.6: Dimensi Fitur per Komponen Hybrid**
| Komponen | Input Dim | Output Dim | Operasi |
|---|---|---|---|
| XceptionNet backbone | (3, 224, 224) | 2048 | Feature extraction + GAP |
| FreqCNN backbone | (1, 224, 224) | 128 | Conv blocks + GAP |
| Spatial projection | 2048 | 256 | Linear + BN + ReLU |
| Frequency projection | 128 | 256 | Linear + BN + ReLU |
| Concatenation | 256 + 256 | 512 | torch.cat |
| SE Gate | 512 | 512 | Squeeze-Excitation |
| Classifier | 512 | 1 | FC layers + Dropout |

**Gambar 3.7: Diagram Arsitektur HybridTwoBranch**
```
RGB (3,224,224) ──→ [XceptionNet Backbone] ──→ (2048) ──→ [Projection: Linear→BN→ReLU] ──→ (256) ─┐
                     (frozen 3 epochs)                      (2048→256)                               │
                                                                                                      ├─→ [Concat] → (512) → [SE Gate] → (512) → [Classifier] → logit
FFT (1,224,224) ──→ [FreqCNN Backbone] ──→ (128) ──→ [Projection: Linear→BN→ReLU] ──→ (256) ────────┘
                     (3 conv blocks)                  (128→256)
```

---

### 3.5 Strategi Pelatihan Model (~8 pages)

#### 3.5.1 Transfer Learning dan Backbone Freezing
**Content from code (`train.py`):**
- XceptionNet pretrained on ImageNet (1.4M images)
- FREEZE_EPOCHS = 3: spatial backbone frozen for first 3 epochs
- Only hybrid and early_fusion models freeze backbone
- Purpose: allow randomly-initialized head layers (projections, SE gate, classifier) to learn meaningful representations before fine-tuning the pretrained backbone
- At epoch 4: `requires_grad_(True)` to unfreeze all backbone parameters

#### 3.5.2 Differential Learning Rate
**Content from code (`train.py`):**

**Tabel 3.8: Learning Rate per Parameter Group**
| Parameter Group | Learning Rate | Applies To |
|---|---|---|
| Backbone (pretrained) | 1e-5 (base/10) | XceptionNet spatial backbone |
| Head (new layers) | 1e-4 (base) | FreqCNN, projections, SE gate, classifier |

- Rationale: pretrained weights are already near-optimal; large LR would destroy learned features (catastrophic forgetting)
- New layers need faster learning to catch up

#### 3.5.3 Penjadwalan Learning Rate
**Content from code (`train.py` SequentialLR):**

```
Epoch 1: LR = 0.1 × base (warmup start)
Epoch 2: LR = 1.0 × base (warmup end)
Epochs 3-30: Cosine decay from base → 1e-6
```

- **Warmup (LinearLR, 2 epochs):** `start_factor=0.1, end_factor=1.0`
  - Prevents large initial weight updates on pretrained features
  - Ramps from 10% to 100% of base LR
- **Cosine Annealing:** `T_max=max(epochs-2, 1), eta_min=1e-6`
  - Smooth, monotonic decay
  - No sharp LR drops that could destabilize training

**Gambar 3.8:** Plot showing LR curve over 30 epochs (warmup phase → cosine decay phase)

#### 3.5.4 Fungsi Loss — BCEWithLogitsLoss dengan Label Smoothing
**Content from code:**
- `nn.BCEWithLogitsLoss()` — combines sigmoid + binary cross-entropy in one step
- More numerically stable than separate sigmoid + BCELoss
- Formula: `L = -[y·log(σ(z)) + (1-y)·log(1-σ(z))]` where σ(z) = sigmoid(z)

**Label smoothing (0.02):**
- `targets = targets × (1 - 0.02) + 0.02 × 0.5`
- Transforms: 0 → 0.01, 1 → 0.99
- Prevents model from becoming overconfident
- Particularly important at small sample sizes

##### 3.5.4.1 Contoh Perhitungan BCEWithLogitsLoss
**MANUAL CALCULATION:**
1. Take a logit value z (e.g., z = 2.5)
2. Compute sigmoid: σ(2.5) = 1/(1+e^{-2.5}) = 0.924
3. Apply label smoothing to target: y = 1 → y' = 0.99
4. Compute loss: L = -[0.99·log(0.924) + 0.01·log(0.076)] = ...
5. ~1-2 pages

#### 3.5.5 Optimisasi — Adam dengan Gradient Accumulation
**Content from code:**
- Optimizer: Adam (lr=1e-4, weight_decay=1e-4)
- Adam combines momentum + adaptive learning rate per parameter
- Gradient accumulation: `accum_steps = 2`
  - Effective batch size: 16 × 2 = 32
  - Loss divided by accum_steps before backward
  - Optimizer step every 2 batches
  - Purpose: achieve larger effective batch without increased memory

#### 3.5.6 Gradient Clipping
- `clip_grad_norm_(model.parameters(), max_norm=1.0)`
- Applied after `scaler.unscale_()` (before optimizer step)
- Prevents gradient explosion, especially at epoch 4 (backbone unfreeze boundary)
- L2 norm clipping: if ‖g‖ > 1.0, scale g to ‖g‖ = 1.0

#### 3.5.7 Mixed Precision Training (AMP)
- `torch.cuda.amp.autocast()` + `GradScaler`
- Float16 for forward/backward pass, float32 for optimizer step
- TF32 enabled for Ampere+ GPUs
- ~2× speedup with minimal accuracy loss

#### 3.5.8 Early Stopping
- Monitor: validation AUC (primary metric)
- Patience: 5 epochs without improvement
- Maximum: 30 epochs
- Action: stop training, use best checkpoint

#### 3.5.9 Seleksi Model Terbaik
- Save checkpoint when val_auc improves: `{"state_dict": ..., "epoch": ..., "config": ...}`
- Best model selected by highest validation AUC
- AUC preferred over accuracy because it's threshold-independent

**Tabel 3.7: Hyperparameter Pelatihan**
| Parameter | Nilai | Keterangan |
|---|---|---|
| Optimizer | Adam | Adaptive learning rate |
| Learning rate (base) | 1×10⁻⁴ | Head/new layers |
| Learning rate (backbone) | 1×10⁻⁵ | Pretrained XceptionNet |
| Weight decay | 1×10⁻⁴ | L2 regularization |
| Batch size | 16 | Per-step; effective 32 via accumulation |
| Gradient accumulation | 2 steps | Effective batch = 32 |
| Epochs (maks) | 30 | Limited by early stopping |
| Early stopping patience | 5 | Consecutive epochs tanpa perbaikan AUC |
| Label smoothing | 0.02 | Target: 0→0.01, 1→0.99 |
| Gradient clipping | max_norm=1.0 | L2 norm clipping |
| LR warmup | 2 epochs | 10%→100% linear ramp |
| LR schedule | Cosine annealing | Decay to 1×10⁻⁶ |
| Backbone freeze | 3 epochs | Hybrid/early_fusion only |
| Mixed precision | AMP (float16) | CUDA only |
| Seed | 42 | Reproducibility |
| Framework | PyTorch + timm | XceptionNet via timm |

---

### 3.6 Desain Eksperimen (~4 pages)

#### 3.6.1 Matriks Eksperimen

**Tabel 3.9: Matriks Eksperimen**
| Dimensi | Nilai | Jumlah |
|---|---|---|
| Model | spatial, freq, hybrid | 3 |
| Dataset pelatihan | FFPP, CDF | 2 |
| Ukuran sampel FFPP | 100, 300, 600, 1000 | 4 |
| Ukuran sampel CDF | 100, 250, 500, 750 | 4 |
| Seed | 0, 1, 2 | 3 |
| Evaluasi | In-dataset, Cross-dataset | 2 |

Total training runs: 3 models × 2 datasets × 4 sample sizes × 3 seeds = **72 runs**
Total evaluations: 72 × 2 (in-dataset + cross-dataset) = **144 evaluations**

#### 3.6.2 Evaluasi In-Dataset
- Train on FFPP → Test on FFPP test set
- Train on CDF → Test on CDF test set
- Measures: how well model learns from its training distribution

#### 3.6.3 Evaluasi Cross-Dataset
- Train on FFPP → Test on CDF test set
- Train on CDF → Test on FFPP test set
- Measures: generalization to unseen deepfake methods and data sources
- **Generalization drop:** `Δ = F1_in-dataset - F1_cross-dataset`

#### 3.6.4 Variabel Penelitian

**Tabel 3.10: Variabel Penelitian**
| Jenis | Variabel | Nilai |
|---|---|---|
| **Independen** | Arsitektur model | spatial, freq, hybrid |
| | Dataset pelatihan | FFPP, CDF |
| | Ukuran sampel | 100-1000 (varies by dataset) |
| **Dependen** | Accuracy, Precision, Recall, F1, AUC | Continuous [0,1] |
| | Generalization drop | F1_in - F1_cross |
| **Kontrol** | Hyperparameter pelatihan | Fixed per Tabel 3.7 |
| | Seed | 42, 43, 44 |
| | Pembagian data | 70/15/15 stratified |
| | Image size | 224×224 |

---

### 3.7 Metode Evaluasi Model (~4 pages)

#### 3.7.1–3.7.6 Individual Metrics
For each metric, provide:
1. Definition in words
2. Mathematical formula
3. What it measures
4. Why it matters for deepfake detection

**Content from code (`metrics.py`):**

| Metric | Formula | Purpose in Deepfake Detection |
|---|---|---|
| Accuracy | (TP+TN)/(TP+TN+FP+FN) | Overall classification correctness |
| Precision | TP/(TP+FP) | How many "fake" predictions are truly fake |
| Recall | TP/(TP+FN) | How many actual fakes are detected |
| F1-Score | 2·P·R/(P+R) | Balance between precision and recall |
| AUC-ROC | Area under ROC curve | Threshold-independent ranking quality |

**AUC as primary metric:**
- Threshold-independent: evaluates model at all possible thresholds
- More robust than accuracy for binary classification
- Used for: model selection (best checkpoint), early stopping

#### 3.7.7 Generalization Drop
- Formula: `Δ = F1_in-dataset - F1_cross-dataset`
- Measures how much performance degrades on unseen data
- Higher Δ = worse generalization
- Key research question: does hybrid fusion improve or hurt generalization?

#### 3.7.8 Contoh Perhitungan Metrik
**MANUAL CALCULATION:**
1. Present a small confusion matrix (e.g., TP=8, FP=2, FN=3, TN=7)
2. Calculate all 5 metrics step by step
3. Show ROC curve concept (plot TPR vs FPR at different thresholds)
4. Calculate Youden's J for optimal threshold selection
5. ~2 pages

**Tabel 3.11: Template Confusion Matrix**
| | Prediksi Fake | Prediksi Real |
|---|---|---|
| **Aktual Fake** | TP | FN |
| **Aktual Real** | FP | TN |

**Tabel 3.12: Contoh Perhitungan**
| Metrik | Perhitungan | Hasil |
|---|---|---|
| Accuracy | (8+7)/(8+2+3+7) = 15/20 | 0.750 |
| Precision | 8/(8+2) = 8/10 | 0.800 |
| Recall | 8/(8+3) = 8/11 | 0.727 |
| F1-Score | 2×0.800×0.727/(0.800+0.727) | 0.762 |
| AUC | (computed from ROC curve) | ... |

---

## PART D: VISUAL ELEMENTS CHECKLIST

### Figures (Gambar) — Required

| ID | Description | Source/How to Create |
|---|---|---|
| Gambar 3.1 | Flowchart utama pipeline (data → preprocessing → training → evaluation) | Draw.io / Lucidchart |
| Gambar 3.2 | Contoh frame real vs fake (RGB) dari FFPP dan CDF | Screenshot from actual dataset |
| Gambar 3.3 | Flowchart preprocessing (frame extraction + FFT conversion) | Draw.io |
| Gambar 3.4 | Perbandingan FFT magnitude: real vs fake | Generated from actual FFT cache |
| Gambar 3.5 | Diagram arsitektur XceptionNet (simplified) | Draw.io or reference paper |
| Gambar 3.6 | Diagram arsitektur FreqCNN (layer-by-layer) | Draw.io |
| Gambar 3.7 | Diagram arsitektur HybridTwoBranch (complete with projections + SE gate) | Draw.io |
| Gambar 3.8 | Kurva learning rate schedule (warmup + cosine decay) | matplotlib plot |

### Tables (Tabel) — Required

| ID | Description | Data Source |
|---|---|---|
| Tabel 3.1 | Statistik dataset (FFPP + CDF) | Dataset files + config |
| Tabel 3.2 | Pembagian data per split | build_splits.py output |
| Tabel 3.3 | Contoh perhitungan FFT 4×4 | Manual calculation |
| Tabel 3.4 | Layer-by-layer FreqCNN | freq_cnn.py |
| Tabel 3.5 | Perbandingan 3 arsitektur model | Architecture comparison |
| Tabel 3.6 | Dimensi fitur per komponen hybrid | hybrid_fusion.py |
| Tabel 3.7 | Hyperparameter pelatihan | config.yaml + train.py |
| Tabel 3.8 | Learning rate per parameter group | train.py |
| Tabel 3.9 | Matriks eksperimen | run_all.py |
| Tabel 3.10 | Variabel penelitian | Experiment design |
| Tabel 3.11 | Template confusion matrix | Standard ML |
| Tabel 3.12 | Contoh perhitungan metrik evaluasi | Manual calculation |

### Manual Calculations — Required

| Calculation | Estimated Pages | Location |
|---|---|---|
| FFT 2D pada matriks 4×4 | 3-4 pages | Section 3.3.2 |
| Depthwise separable convolution | 2-3 pages | Section 3.4.1.1 |
| FreqCNN forward pass | 2 pages | Section 3.4.2.2 |
| Late fusion (projection + SE + classifier) | 3-4 pages | Section 3.4.3.6 |
| BCEWithLogitsLoss | 1-2 pages | Section 3.5.4.1 |
| Metrik evaluasi dari confusion matrix | 2 pages | Section 3.7.8 |
| **Total** | **~15-17 pages** | |

---

## PART E: CROSS-REFERENCE WITH CODE

### Every claim in BAB III must match actual code. Key verification points:

| BAB III Claim | Code Location | Verified Value |
|---|---|---|
| image_size = 224 | config.yaml: `image_size: 224` | ✓ |
| batch_size = 16 | config.yaml: `batch_size: 16` | ✓ |
| epochs = 30 | config.yaml: `epochs: 30` | ✓ |
| lr = 1e-4 | config.yaml: `lr: 1.0e-4` | ✓ |
| weight_decay = 1e-4 | config.yaml: `weight_decay: 1.0e-4` | ✓ |
| early_stop_patience = 5 | config.yaml: `early_stop_patience: 5` | ✓ |
| accum_steps = 2 | config.yaml: `accum_steps: 2` | ✓ |
| label_smoothing = 0.02 | config.yaml: `label_smoothing: 0.02` | ✓ |
| freq_depth = 3 | config.yaml: `freq_depth: 3` | ✓ |
| freq_base_channels = 32 | config.yaml: `freq_base_channels: 32` | ✓ |
| fft_noise_sigma = 0.05 | config.yaml: `fft_noise_sigma: 0.05` | ✓ |
| n_seeds = 3 | config.yaml: `n_seeds: 3` | ✓ |
| PROJ_DIM = 256 | hybrid_fusion.py:7 | ✓ |
| FREEZE_EPOCHS = 3 | train.py constant | ✓ |
| SE reduction = 4 | hybrid_fusion.py SEGate(reduction=4) | ✓ |
| Optimizer = Adam | train.py: `optim.Adam(...)` | ✓ |
| LR warmup = 2 epochs | train.py: LinearLR total_iters=2 | ✓ |
| Cosine eta_min = 1e-6 | train.py: CosineAnnealingLR eta_min=1e-6 | ✓ |
| Backbone LR = base/10 | train.py: `backbone_lr = lr / 10` | ✓ |
| Gradient clip max_norm = 1.0 | train.py: clip_grad_norm_ max_norm=1.0 | ✓ |
| Grayscale = ITU-R 601 | fft_utils.py: PIL "L" mode | ✓ |
| FFT = np.fft.fft2 + fftshift | fft_utils.py:13-16 | ✓ |
| Log scaling = log1p | fft_utils.py:17 | ✓ |
| Split ratios = 70/15/15 | build_splits.py defaults | ✓ |
| FPS = 5 | config.yaml: `frame_sampling_fps: 5` | ✓ |
| Max frames = 50 | config.yaml: `max_frames_per_video: 50` | ✓ |
| FFPP samples = [100,300,600,1000] | CLAUDE.md + run_pipeline | ✓ |
| CDF samples = [100,250,500,750] | CLAUDE.md + run_pipeline | ✓ |

---

## PART F: WHAT NOT TO INCLUDE IN BAB III

1. **Conv1×1 channel adapter** — this was the old early_fusion approach. Current code does NOT use a Conv1×1 adapter. Remove all references.
2. **Early stopping based on accuracy > 95%** — incorrect. Early stopping is patience=5 on AUC.
3. **Image size 256×256** — incorrect. Actual is 224×224 (resize to 256 is only an intermediate step before RandomResizedCrop).
4. **Batch size 32** — misleading. Actual batch_size=16 with accum_steps=2 for effective 32.
5. **100 epochs** — incorrect. Max epochs=30 with early stopping.
6. **Early fusion as primary model** — early_fusion exists but is not the main contribution. The main contribution is HybridTwoBranch (late fusion with SE gating).
7. **Web application components** — this is a pure ML thesis, no web app. Skip Analisis Kebutuhan Fungsional/Non-Fungsional sections.
8. **SGD optimizer** — already removed from BAB II. Confirm Adam throughout.
9. **LSTM/GRU/Transformer** — not used. This is frame-level detection, not temporal.

---

## PART G: WRITING PRIORITY ORDER

| Priority | Section | Effort | Dependencies |
|---|---|---|---|
| 1 | 3.4 Arsitektur Model (~12 pages) | HIGH | Need architecture diagrams |
| 2 | 3.3 Preprocessing + FFT (~8 pages) | HIGH | Need FFT manual calculation, visual examples |
| 3 | 3.5 Strategi Pelatihan (~8 pages) | MEDIUM | Need LR curve plot |
| 4 | 3.7 Metode Evaluasi (~4 pages) | MEDIUM | Need confusion matrix example |
| 5 | 3.6 Desain Eksperimen (~4 pages) | MEDIUM | Straightforward from code |
| 6 | 3.2 Dataset (~5 pages) | LOW | Need dataset statistics, example images |
| 7 | 3.1 Kerangka Umum (~3 pages) | LOW | Write last (overview of everything) |

**Total estimated: ~44 pages** (aligns with Chrisandy's 43 pages)

---

## PART H: DIFFERENCES FROM PREVIOUS BAB III ANALYSIS

The previous analysis (2026-03-14) rated BAB III at "90% complete". This was overly optimistic because:

1. **It evaluated against the code at that time** — since then, 40+ fixes were applied (SE gating, deeper FreqCNN, warmup scheduler, label smoothing, gradient clipping, etc.)
2. **It didn't account for manual calculations** — Chrisandy's thesis (the reference standard at Mikroskil) devotes ~28 pages to step-by-step calculations
3. **It didn't flag the fundamental architecture mismatch** — BAB III describes early_fusion with Conv1×1 adapter as the main model, but the actual main contribution is HybridTwoBranch with late fusion + SE gating

**Updated assessment: BAB III needs a complete rewrite (~85% new content)**

Only salvageable content from current BAB III:
- General justification for hybrid approach (3.1, partially)
- FFPP dataset description (3.2.1, partially — needs CDF addition)
- FFT conversion concept (3.3.2, partially — needs detail expansion and manual calculation)
- Evaluation metric formulas (3.7, partially — needs AUC and generalization drop)

---

## PART I: SUMMARY

### What BAB III Must Achieve

1. **Accurately describe what was built** — 3 models (spatial, freq, hybrid), not just early_fusion
2. **Show the "how" with manual calculations** — FFT, depthwise conv, fusion, loss, metrics (~15 pages)
3. **Present complete experiment design** — multi-model × multi-dataset × multi-sample-size × multi-seed
4. **Include all training innovations** — differential LR, backbone freezing, warmup, cosine decay, SE gating, gradient clipping, label smoothing
5. **Provide visual aids** — 8 figures (flowcharts, architecture diagrams, examples) + 12 tables
6. **Cross-reference with code** — every number, formula, and parameter must match actual implementation
7. **Target ~44 pages** — matching reference thesis scope

### What Makes This BAB III Strong

- **Three-model comparative design:** Spatial-only, Freq-only, Hybrid allows measuring individual and combined contribution of each domain
- **Cross-dataset evaluation:** Goes beyond standard in-dataset testing to measure real-world generalization
- **Multi-sample-size analysis:** Shows how data quantity affects each model type differently
- **SE gating as innovation:** Learned attention mechanism for branch weighting is a meaningful architectural contribution
- **Manual calculations:** Following Mikroskil convention, readers can verify algorithmic correctness by hand
