# Ringkasan Parameter, Nilai & Pengujian — Proyek Deepfake Hybrid XceptionNet–FFT

> Rangkuman **semua nilai, parameter, dan skenario pengujian** yang dipakai di proyek, diambil langsung dari kode & config (bukan dari draft skripsi). Setiap nilai diberi rujukan `file:line` agar dapat diverifikasi.
> Sumber utama: `deepfake_hybrid/config.yaml`, `src/`, `scripts/`. Dibuat 2026-07-07.

---

## 1. Ikhtisar

| Aspek | Nilai |
|---|---|
| Model dievaluasi | **spatial** (XceptionNet), **freq** (FreqCNN), **hybrid** (HybridTwoBranch, late fusion) — `run_all.py:23` `MODELS_CORE` |
| Model opsional (tidak dievaluasi) | **early_fusion** (XceptionNet 4-kanal RGB+FFT) |
| Dataset | **FFPP** (FaceForensics++, c23) & **CDF** (Celeb-DF v2) — `config.yaml` `datasets` |
| Skenario | in-dataset (FFPP→FFPP, CDF→CDF) + cross-dataset (FFPP→CDF, CDF→FFPP) |
| Level klasifikasi | frame-level, biner (real=0, fake=1), split per-video |

---

## 2. Data & Preprocessing

### 2.1 Ekstraksi Frame — `scripts/extract_frames.py`, `config.yaml`
| Parameter | Nilai | Sumber |
|---|---|---|
| `frame_sampling_fps` | **5** FPS | `config.yaml` |
| `max_frames_per_video` | **50** | `config.yaml` |
| `image_size` | **224** | `config.yaml` |
| Face crop | **MTCNN**, `face_margin` = **0,3** | `extract_frames.py:32,49` |
| Sampling interval | `max(round(native_fps / 5), 1)` (mis. 30 FPS → tiap frame ke-6) | `extract_frames.py:81` |
| Skip frame rusak/hitam | `mean(first_frame) < 3` → lewati video | `extract_frames.py:74` |
| Fallback wajah tak terdeteksi | pakai frame penuh | `extract_frames.py:93-96` |
| Penamaan berkas | `frame_{saved:06d}.jpg` (JPEG) | `extract_frames.py:98` |
| Manifes | CSV kolom `video_id, label, frames_dir` | `extract_frames.py:254` |
| Dispatch | **paralel** (multiprocessing pool) tanpa face-crop; **sekuensial** dgn face-crop (MTCNN tak bisa di-pickle) | `extract_frames.py:222-230` |
| Inferensi label | dari nama direktori via `real_keywords`/`fake_keywords` | `config.yaml`, `extract_frames.py:20,149` |

### 2.2 Pembagian Data — `scripts/build_splits.py`
| Parameter | Nilai |
|---|---|
| Train / Val / Test | **70% / 15% / 15%** (`--val-size 0.15`, `--test-size 0.15`) |
| Stratifikasi | per-video berdasarkan label (cegah kebocoran frame) |
| Min sampel per kelas | 4 (`min_per_class`) |
| Rasio kelas (sampling) | real : fake = **50 : 50** |

### 2.3 Transformasi FFT — `src/fft_utils.py`
| Langkah | Nilai/Detail |
|---|---|
| Grayscale | `Image.convert("L")` → Y = **0,299R + 0,587G + 0,114B** (ITU-R BT.601) — `fft_utils.py:24` |
| Resize | **224×224** — `fft_utils.py:25` |
| Transform | `np.fft.fft2` → `np.fft.fftshift` → `np.abs` (magnitude) — `fft_utils.py:27-29` |
| High-pass filter | Gaussian, `cutoff` (β) = **0,15** (fraksi ukuran; σ = 0,15 × size) — `fft_utils.py:9,17` |
| Log scaling | `log(1 + |F(u,v)|)` |
| Cache | `.npy` per frame |
| Normalisasi | **z-score** `(fft − μ) / σ`, μ,σ per-dataset dari `fft_stats.json` (auto-computed) — `deepfake_data.py:91,129` |

### 2.4 Augmentasi
**Cabang spasial (RGB), pelatihan** — `src/transforms.py`
| Augmentasi | Nilai |
|---|---|
| Resize | `image_size + 32` = **256** |
| RandomResizedCrop | 224, `scale=(0.8, 1.0)` |
| ColorJitter | brightness 0,2 · contrast 0,2 · saturation 0,1 · hue 0,05 |
| RandomHorizontalFlip | p = 0,5 |
| Normalize (ImageNet) | mean **[0,485, 0,456, 0,406]**, std **[0,229, 0,224, 0,225]** |
| RandomErasing | p = **0,1**, scale=(0,02–0,15) |

*(Eval: hanya Resize 224 + Normalize ImageNet.)*

**Cabang frekuensi (FFT), pelatihan** — `src/deepfake_data.py`
| Augmentasi | Nilai |
|---|---|
| Gaussian noise | σ (`fft_noise_sigma`) = **0,05** — `config.yaml`, `deepfake_data.py:57,132` |
| Spectral band masking | p = **0,05**; lebar band `random(1, max(h//16, 2))`; arah baris/kolom acak — `deepfake_data.py:134-141` |

**Hybrid:** horizontal flip **konsisten** pada kedua cabang (p = 0,5) — `deepfake_data.py:154`.

---

## 3. Arsitektur Model

### 3.1 Spatial — XceptionNet — `src/models/spatial_xception.py`
| Parameter | Nilai |
|---|---|
| Backbone | `timm.create_model("xception")`, pretrained **ImageNet** |
| `in_chans` | 3 (RGB) · `num_classes` = 1 (logit biner) |
| Dimensi fitur (setelah GAP) | **2048** |
| Jumlah parameter | ~22 juta |

### 3.2 Frequency — FreqCNN — `src/models/freq_cnn.py`
| Parameter | Nilai |
|---|---|
| Input | 1-kanal FFT log-magnitude (1, 224, 224) |
| `freq_depth` | **5** — `config.yaml` |
| `freq_base_channels` | **64** — `config.yaml` |
| Channels per blok | **[64, 128, 256, 512, 512]** → `feature_dim` = **512** |
| FreqBlock | Conv2d(3×3, pad 1) → BatchNorm → ReLU **+ shortcut** (1×1 bila C berubah, else Identity) → **MaxPool(2)** |
| Setelah 5 blok | Dropout2d(**0,2**) → AdaptiveAvgPool2d(1×1) |
| Classifier (freq standalone) | Linear(512→256) → ReLU → Dropout(**0,3**) → Linear(256→1) |
| Jumlah parameter | ~4,2 juta |

### 3.3 Hybrid — HybridTwoBranch (late fusion) — `src/models/hybrid_fusion.py`
| Komponen | Nilai |
|---|---|
| `PROJ_DIM` | **256** — `hybrid_fusion.py:8` |
| Proyeksi spasial | Linear(2048→256) → BatchNorm1d → ReLU |
| Proyeksi frekuensi | Linear(512→256) → BatchNorm1d → ReLU |
| Fusi | concat → `fused_dim` = **512** |
| SE Gate | `SEGate(512, reduction=4)`: Linear(512→128) → ReLU → Linear(128→512) → sigmoid gating |
| Classifier | Dropout(**0,5**) → Linear(512→128) → ReLU → Dropout(**0,5**) → Linear(128→1) |

---

## 4. Pelatihan — `scripts/train.py`, `config.yaml`

### 4.1 Optimizer & Differential Learning Rate
| Parameter | Nilai |
|---|---|
| Optimizer | **AdamW** (Loshchilov & Hutter, 2019) |
| `lr` (base) | **2×10⁻⁴** |
| `weight_decay` | **1×10⁻⁴** |
| LR backbone (XceptionNet) | base / 10 = **2×10⁻⁵** — `train.py:191` |
| LR cabang freq (dalam hybrid) | base × 0,25 = **5×10⁻⁵** — `train.py:219` |
| LR head (proj/SE/classifier) | base = **2×10⁻⁴** — `train.py:220` |

### 4.2 Backbone Freezing
| Parameter | Nilai |
|---|---|
| `FREEZE_EPOCHS` | **3** (epoch 1–3 beku) — `train.py:26` |
| Unfreeze | epoch **4** (`requires_grad_ = True`) — `train.py:274` |

### 4.3 Penjadwalan LR
| Fase | Nilai |
|---|---|
| Warmup | LinearLR `start_factor=0.1 → 1.0`, `total_iters` = **3 epoch** — `train.py:257` |
| Decay | CosineAnnealingLR `T_max = max(epochs−3, 1)`, `eta_min` = **1×10⁻⁶** — `train.py:260` |
| Gabungan | SequentialLR (milestone di epoch 3) |

### 4.4 Loss
| Parameter | Nilai |
|---|---|
| Fungsi loss | **BCEWithLogitsLoss** dengan `pos_weight = n_neg/n_pos` — `train.py:184-185` |
| Label smoothing (α) | **0,05**: `y' = y(1−α) + α·0,5` — `config.yaml`, `train.py:112` |

### 4.5 Stabilitas & Efisiensi
| Parameter | Nilai |
|---|---|
| Gradient clipping | `clip_grad_norm_`, `max_norm` = **5,0** — `train.py:117` |
| Gradient accumulation | `accum_steps` = **2** (batch 16 → efektif **32**) — `config.yaml`, `train.py:113` |
| Mixed precision (AMP) | `autocast` + `GradScaler` (CUDA); **TF32** untuk Ampere+ |

### 4.6 Batch, Epoch, Seed, Seleksi
| Parameter | Nilai |
|---|---|
| `batch_size` | **16** |
| `num_workers` | 2 |
| `epochs` (maks) | **30** |
| Early stopping | `patience` = **12**, metrik = **AUC validasi** |
| `n_seeds` | **3** (seed 0, 1, 2) |
| Seleksi model | checkpoint dengan **AUC validasi tertinggi** |

---

## 5. Matriks Eksperimen (pengujian) — `scripts/run_all.py`, Tabel 3.12

| Dimensi | Nilai | Jumlah |
|---|---|---|
| Model | spatial, freq, hybrid | 3 |
| Dataset pelatihan | FFPP, CDF | 2 |
| Ukuran sampel (video, per dataset) | **100, 250, 500, 750** | 4 |
| Seed | 0, 1, 2 | 3 |
| Skenario evaluasi | in-dataset, cross-dataset | 2 |

- **Total pelatihan:** 3 × 2 × 4 × 3 = **72 run**
- **Total evaluasi:** 72 × 2 = **144 evaluasi**
- Tier andal untuk analisis utama: **n = 250, 500, 750** (n=100 ~15 video uji, rentan noise); **n = 750** = representasi utama.
- *(Ukuran sampel di-drive lewat CLI `--n-samples`; loop dijalankan di `colab_run.ipynb`. Tier eksplorasi lain di disk: n50/n200/n400.)*

---

## 6. Evaluasi — `scripts/eval.py`

| Aspek | Nilai |
|---|---|
| Metrik | accuracy, precision, recall, F1-score, **AUC-ROC**, confusion matrix |
| Threshold default | θ = **0,5** — `eval.py:109` |
| Threshold optimal | **Youden's J** (J = TPR − FPR) — `eval.py:115` |
| Metrik utama | **AUC** (seleksi model + early stopping; independen threshold) |

---

## 7. Pengujian Kode (unit test)

- **Tidak ada** unit test / `pytest` (`tests/` tidak ada; tidak ada `test_*.py`). "Pengujian" pada proyek ini = **evaluasi eksperimental** (in-dataset & cross-dataset, Bagian 5–6).
- **Smoke test** manual (CLAUDE.md): `python scripts/run_pipeline.py --n-samples 100 --max-frames 10 --epochs 3 --pretrained --face-crop`.

---

## 8. Environment

| Aspek | Nilai |
|---|---|
| Python | 3.9 (venv `deepfake_hybrid/.venv`) |
| Dependensi kunci | torch, torchvision, **timm** (xception), opencv-python, scikit-learn, pandas, matplotlib, facenet-pytorch (MTCNN) |
| Hardware | GPU CUDA (Tesla T4 15 GB / V100), Google Colab Pro |
| Config aktif | `deepfake_hybrid/config.yaml` (`run_pipeline.py` membuat `.pipeline_config.yaml` dengan override) |

---

### Catatan konsistensi
- `HybridTwoBranch.__init__` punya **default** `freq_depth=3, base_channels=32` (`feature_dim` 256/128), tetapi **nilai efektif** dari `config.yaml` = **depth 5, base 64** → `feature_dim` **512**. Selalu rujuk `config.yaml` sebagai sumber kebenaran.
- Semua nilai di atas dikonfirmasi terhadap kode pada 2026-07-07; bila config diubah, perbarui dokumen ini.
