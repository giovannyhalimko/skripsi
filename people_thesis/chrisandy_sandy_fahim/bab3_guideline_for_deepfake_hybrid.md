# Guideline: Implementasi BAB III untuk Skripsi Deepfake Hybrid

> **Sumber referensi:** BAB III skripsi Chrisandy, Sandy, Fahim — "Implementasi BiLSTM dan Attention pada Aplikasi Semantic Textual Similarity Berbasis Web"
>
> **Target:** BAB III skripsi kita — "Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi"

---

## Ringkasan Struktur BAB III Chrisandy (Referensi)

| Section | Isi | Halaman |
|---|---|---|
| 3.1 Kerangka Tahapan Pelaksanaan | 5 tahap: Pengumpulan Data, Analisis, Perancangan, Implementasi, Pengujian & Evaluasi | p.31 |
| 3.2 Dataset | Deskripsi QQP, pembagian 80:20, statistik deskriptif (tabel), contoh data (gambar) | p.32-33 |
| 3.3 Analisis Proses | **Inti BAB III** — flowchart utama + 3 sub-flowchart, lalu perhitungan manual step-by-step untuk setiap tahap: Preprocessing, Tokenisasi+Embedding BERT, Layer Normalization, BiLSTM (Forward+Backward), Attention, Dense+Sigmoid | p.33-61 |
| 3.4 Analisis Kebutuhan | Fungsional (use case diagram + tabel use case) dan Non-Fungsional (PIECES) | p.62-67 |
| 3.5 Perancangan | Wireframe UI (sidebar, halaman text similarity, document similarity, login, admin dashboard) | p.68-73 |

### Pola Kunci yang Harus Diikuti

1. **Flowchart utama** yang merangkum seluruh pipeline (training + testing)
2. **Sub-flowchart** per tahap (preprocessing, embedding, normalisasi, dll)
3. **Contoh data illustratif** — ambil 1 sampel, sederhanakan dimensi, hitung manual dari awal sampai akhir
4. **Tabel-tabel hasil perhitungan** di setiap step
5. **Hyperparameter search** + tabel konfigurasi final
6. **Analisis kebutuhan** (use case + PIECES) — ini untuk komponen aplikasi/web jika ada

---

## Mapping ke Proyek Kita (Deepfake Hybrid)

### 3.1 Kerangka Umum Penelitian ✅ (sudah ada skeleton)

**Yang perlu ditulis:**
1. Jenis penelitian: eksperimental, bidang computer vision & deep learning
2. 5 tahapan pelaksanaan:
   - Pengumpulan Data (FaceForensics++, Celeb-DF)
   - Preprocessing (frame extraction, face crop, FFT conversion)
   - Perancangan Model (arsitektur hybrid)
   - Pelatihan & Optimasi
   - Pengujian & Evaluasi
3. Justifikasi pendekatan hybrid (sudah ada)
4. Alur sistem / pipeline diagram (sudah ada skeleton)

**Action:** Tulis narasi final, buat flowchart diagram utama.

---

### 3.2 Dataset dan Sumber Data ✅ (sudah ada skeleton)

**Yang perlu ditulis berdasarkan pola Chrisandy:**

| Komponen | Chrisandy (QQP) | Kita (FFPP + CDF) |
|---|---|---|
| Deskripsi dataset | Asal, ukuran, label | FaceForensics++ (4 metode manipulasi), Celeb-DF v2 |
| Contoh data | Gambar 3.1 (screenshot pasangan kalimat) | Screenshot frame real vs fake (RGB + FFT magnitude) |
| Statistik deskriptif | Tabel 3.1 (jumlah data, distribusi label, panjang token) | Tabel: jumlah video, jumlah frame per split, distribusi real/fake per dataset |
| Pembagian data | 80:20, justifikasi rasio | Train/Val/Test split dari FFPP, 30% sampling, seed deterministik |
| Alasan pemilihan | Benchmark standar, skala besar | Benchmark standar deepfake, multi-manipulation, tersedia publik |

**Action items:**
- [ ] Buat **Tabel 3.1**: Statistik deskriptif dataset (jumlah video, frame, distribusi label per split)
- [ ] Buat **Gambar**: Contoh frame real vs fake (RGB) + FFT magnitude-nya
- [ ] Tulis narasi pembagian dataset + justifikasi penggunaan 30% subset

---

### 3.3 Tahapan Preprocessing Data ✅ (sudah ada skeleton)

**Pola Chrisandy:** Dia buat sub-flowchart per tahap, lalu hitung manual setiap langkah.

**Yang perlu kita tulis dengan detail:**

#### 3.3.1 Ekstraksi Frame dari Video
- Proses frame sampling (berapa frame per video)
- Resize ke 256x256
- Labelling berdasarkan metadata

#### 3.3.2 Konversi Domain Frekuensi (FFT) — **INTI SKRIPSI**
**Ikuti pola Chrisandy: buat contoh perhitungan manual!**

Langkah-langkah yang perlu dihitung manual (dengan contoh piksel kecil, misal 4x4):
1. Ambil 1 frame contoh
2. Konversi RGB ke grayscale — tunjukkan formula Y = 0.299R + 0.587G + 0.114B
3. Terapkan FFT 2D — tunjukkan DFT formula, hitung untuk matriks kecil
4. Hitung magnitude spectrum: |F(u,v)| = sqrt(Re^2 + Im^2)
5. FFT shift (pindah DC component ke tengah)
6. Log scaling: log(1 + |F(u,v)|)
7. Normalisasi ke [0,1]

**Action items:**
- [ ] Buat **Gambar flowchart** tahap FFT preprocessing
- [ ] Buat **contoh perhitungan manual** FFT dengan matriks 4x4 (seperti Chrisandy yang hitung manual BiLSTM step-by-step)
- [ ] Buat **Tabel**: Contoh hasil FFT pada piksel tertentu
- [ ] Tampilkan **gambar perbandingan**: frame asli RGB vs FFT magnitude (real vs fake)

#### 3.3.3 Integrasi FFT sebagai Channel Tambahan
- Tensor input: (256 x 256 x 4) = R, G, B, F
- Channel adapter Conv 1x1 (4 -> 3)
- Jelaskan + hitung contoh linear projection sederhana

---

### 3.4 Arsitektur Model yang Diusulkan

**Pola Chrisandy:** Dia punya Gambar 3.6 (arsitektur training) + Tabel 3.4-3.6 (hyperparameter).

**Yang perlu kita tulis:**

#### 3.4.1 Arsitektur XceptionNet
- Depthwise separable convolution (brief, sudah di BAB II)
- Transfer learning dari ImageNet (frozen backbone)

#### 3.4.2 Channel Adapter Layer
- Conv2D 1x1: 4 channel -> 3 channel
- **Contoh perhitungan manual**: ambil 1 piksel (4 nilai RGBF), kalikan dengan kernel 1x1 (4x3), hasilkan 3 nilai output
- Tunjukkan ini adalah linear projection

#### 3.4.3 Arsitektur Lengkap (4 Model Variants)
Buat **tabel perbandingan** 4 arsitektur:

| Model | Input | Backbone | Fusion | Classifier |
|---|---|---|---|---|
| spatial | RGB 256x256x3 | XceptionNet (pretrained) | - | FC + Sigmoid |
| freq | FFT 1-ch | FreqCNN (3 conv layers) | - | FC + Sigmoid |
| hybrid (late fusion) | RGB + FFT terpisah | XceptionNet + FreqCNN | Concat features | FC + Sigmoid |
| early_fusion | RGB+FFT 256x256x4 | XceptionNet (modified 1st conv) | 4-ch input | FC + Sigmoid |

Buat **diagram arsitektur** untuk setiap model (terutama hybrid dan early_fusion).

#### 3.4.4 FreqCNN Architecture
- 3 conv layers + AdaptiveAvgPool
- Buat tabel layer-by-layer (input shape -> output shape per layer)

---

### 3.5 Strategi Pelatihan Model

**Pola Chrisandy:** Hyperband tuning + tabel konfigurasi final.

**Yang perlu kita tulis:**

#### 3.5.1 Transfer Learning
- XceptionNet backbone: frozen vs unfrozen strategy
- Pretrained weights dari ImageNet

#### 3.5.2 Parameter Pelatihan
Buat **Tabel** (seperti Tabel 3.6 Chrisandy):

| Parameter | Value |
|---|---|
| Optimizer | Adam |
| Learning Rate | 1e-4 |
| Weight Decay | 1e-4 |
| Loss Function | BCEWithLogitsLoss |
| Batch Size | 32 |
| Epoch Maksimum | 100 |
| Metric Seleksi Model | AUC |
| Framework | PyTorch |

#### 3.5.3 Early Stopping
- Strategi custom early stopping
- Threshold akurasi + validation loss
- Patience

#### 3.5.4 Data Augmentation
- RandomCrop untuk spatial input
- CenterCrop untuk FFT input (justifikasi: FFT perlu konsistensi spasial)
- Normalisasi ImageNet (mean, std)

---

### 3.6 Analisis Proses — Perhitungan Manual (INTI!)

**Ini bagian terpenting yang mengikuti pola Chrisandy.**

Chrisandy menghabiskan ~30 halaman (p.33-61) untuk perhitungan manual step-by-step. Kita perlu melakukan hal serupa untuk pipeline kita:

#### Contoh Perhitungan Manual yang Perlu Dibuat:

**1. FFT Conversion (padanan preprocessing Chrisandy)**
- Ambil matriks grayscale 4x4
- Hitung DFT 2D manual (gunakan formula)
- Hitung magnitude, shift, log-scale
- ~3-4 halaman perhitungan

**2. Channel Adapter / Conv 1x1 (padanan tokenisasi Chrisandy)**
- Ambil 1 piksel 4-channel [R, G, B, F]
- Kalikan dengan kernel 1x1 (4 input -> 3 output)
- Tunjukkan hasilnya adalah 3-channel output
- ~1-2 halaman

**3. Depthwise Separable Convolution (padanan Layer Norm Chrisandy)**
- Ambil feature map kecil (misal 3x3, 3 channel)
- Hitung depthwise conv step-by-step
- Hitung pointwise conv step-by-step
- Bandingkan parameter count dengan standard conv
- ~3-4 halaman

**4. Late Fusion (concat + FC) (padanan Attention Chrisandy)**
- Ambil output spatial branch (misal vektor 4-dim)
- Ambil output freq branch (misal vektor 4-dim)
- Concat -> 8-dim
- FC layer: W (8x1) + bias
- Sigmoid -> probabilitas
- ~2-3 halaman

**5. BCEWithLogitsLoss (padanan Dense+Sigmoid Chrisandy)**
- Hitung logit dari FC output
- Terapkan sigmoid
- Hitung binary cross-entropy loss
- ~1-2 halaman

**6. Metrik Evaluasi**
- Contoh confusion matrix kecil
- Hitung Accuracy, Precision, Recall, F1, AUC dari contoh
- ~1-2 halaman

**Total estimasi: ~15-20 halaman perhitungan manual**

---

### 3.7 Metode Evaluasi Model

| Metrik | Formula | Fungsi |
|---|---|---|
| Accuracy | (TP+TN)/(TP+TN+FP+FN) | Performa keseluruhan |
| Precision | TP/(TP+FP) | Ketepatan prediksi positif |
| Recall | TP/(TP+FN) | Kemampuan mendeteksi positif |
| F1-Score | 2*(P*R)/(P+R) | Harmonic mean P dan R |
| AUC | Area under ROC curve | **Primary metric** untuk model selection |
| Loss | BCEWithLogitsLoss | Training objective |

Jelaskan:
- Evaluasi pada train, validation, test split
- Kurva yang dianalisis: Loss vs Epoch, Accuracy vs Epoch, AUC vs Epoch
- Cross-dataset evaluation (train FFPP, test CDF)

---

### 3.8 Analisis Kebutuhan (OPSIONAL — hanya jika ada komponen web/app)

Jika skripsi kita murni model ML tanpa web app, bagian ini **BISA DISKIP**.

Jika ada komponen aplikasi:
- Use case diagram
- Tabel use case per fitur
- Analisis non-fungsional (PIECES)

---

## Checklist Deliverables

### Gambar/Diagram yang Perlu Dibuat:
- [ ] Flowchart utama pipeline (Training + Testing)
- [ ] Sub-flowchart: Preprocessing (frame extraction + FFT)
- [ ] Sub-flowchart: Training pipeline per model variant
- [ ] Diagram arsitektur: EarlyFusionXception (4-ch input)
- [ ] Diagram arsitektur: HybridTwoBranch (late fusion)
- [ ] Diagram arsitektur: FreqCNN
- [ ] Contoh visual: Frame real vs fake (RGB + FFT magnitude)

### Tabel yang Perlu Dibuat:
- [ ] Statistik deskriptif dataset FFPP + CDF
- [ ] Pembagian dataset (train/val/test per split)
- [ ] Perbandingan 4 arsitektur model
- [ ] Layer-by-layer FreqCNN
- [ ] Hyperparameter final training
- [ ] Contoh perhitungan FFT (matriks kecil)
- [ ] Contoh perhitungan Conv 1x1
- [ ] Contoh perhitungan depthwise separable conv
- [ ] Contoh confusion matrix + metrik evaluasi

### Perhitungan Manual:
- [ ] FFT 2D pada matriks 4x4 grayscale
- [ ] Conv 1x1 adapter (4ch -> 3ch)
- [ ] Depthwise separable convolution
- [ ] Late fusion (concat + FC + sigmoid)
- [ ] BCEWithLogitsLoss
- [ ] Metrik evaluasi dari contoh confusion matrix

---

## Prioritas Implementasi

1. **HIGH** — 3.3 Analisis Proses + Perhitungan Manual FFT (ini "jualan" skripsi)
2. **HIGH** — 3.4 Arsitektur Model (diagram + tabel 4 variant)
3. **HIGH** — 3.5 Strategi Pelatihan (hyperparameter table)
4. **MEDIUM** — 3.2 Dataset (statistik + contoh visual)
5. **MEDIUM** — 3.6 Metrik Evaluasi
6. **LOW** — 3.1 Kerangka Umum (sudah ada skeleton)
7. **LOW** — 3.7 Analisis Kebutuhan (skip jika tidak ada web app)

---

## Perbedaan Kunci: Chrisandy vs Kita

| Aspek | Chrisandy (NLP/STS) | Kita (CV/Deepfake) |
|---|---|---|
| Domain | Text processing | Image/Video processing |
| Input | Pasangan kalimat teks | Frame video (RGB + FFT) |
| Preprocessing | Text cleaning, tokenisasi BERT | Frame extraction, resize, FFT conversion |
| Feature extraction | BERT (frozen) -> embedding 768-dim | XceptionNet (pretrained) -> spatial features |
| Core model | BiLSTM + Additive Attention | Hybrid: XceptionNet + FreqCNN (atau early fusion) |
| Perhitungan manual fokus | BiLSTM gates (forget, input, candidate, output) + Attention | FFT 2D + Depthwise Sep Conv + Late Fusion concat |
| Output | Similarity score (0-100%) | Binary classification (real/fake) |
| Loss | BCE | BCEWithLogitsLoss |
| Optimizer | AdamW | Adam |
| Hyperparameter tuning | Hyperband (Keras Tuner) | Manual / grid search |
| Web app | Ada (FastAPI + Streamlit) | Tidak ada (pure model) |

**Mapping perhitungan manual:**
- Chrisandy: BERT embedding -> LayerNorm -> BiLSTM -> Attention -> Dense -> Sigmoid
- Kita: **FFT conversion -> Conv1x1 adapter -> Depthwise Sep Conv (XceptionNet) -> Concat Fusion -> FC -> Sigmoid**
