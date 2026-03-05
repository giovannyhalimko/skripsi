# Analisis BAB II - Kajian Literatur
**Dokumen:** Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi
**Tanggal Analisis:** 2026-03-05
**Scope:** Cek kelengkapan BAB II terhadap BAB I, identifikasi konten tidak diperlukan, dan gap antara implementasi kode dengan literatur

---

## 1. Ringkasan Isi BAB I (Requirement Baseline)

BAB I mendefinisikan scope penelitian sebagai berikut:

| Aspek | Detail |
|---|---|
| Topik utama | Hybrid XceptionNet + FFT untuk deteksi deepfake |
| Pendekatan | Gabungan domain spasial (XceptionNet) + domain frekuensi (FFT) |
| Dataset | **FaceForensics++** dan **Celeb-DF** |
| Metode frekuensi | FFT |
| Metode spasial | XceptionNet |
| Metrik evaluasi | Accuracy, Precision, Recall, **AUC** |
| Tujuan kunci | Cross-dataset generalization, cross-GAN robustness |
| Research gap | Tidak ada pendekatan terpadu spatial + frequency yang optimal |

Rumusan masalah secara eksplisit menyebut: modifikasi XceptionNet dengan modul FDA, integrasi fitur spasial fine-grained dan high-band frequency artifacts, serta peningkatan cross-dataset generalization.

---

## 2. Pemetaan BAB I → BAB II (Coverage Check)

### 2.1 Yang Sudah Tercakup dengan Baik

| Topik BAB I | Seksi BAB II | Status |
|---|---|---|
| Deepfake technology & GAN | Deepfake, GAN, Upsampling | LENGKAP |
| Spatial domain (XceptionNet background) | CNN, Depthwise Separable Convolution | LENGKAP |
| Frequency domain (FFT) | Frequency Domain Analysis, FFT, Spectral Distortions | LENGKAP |
| GAN fingerprints / artefak | Periodic Noise, Spectral Dropoff, Warping | LENGKAP |
| FaceForensics++ dataset | FaceForensics (seksi tersendiri) | LENGKAP |
| Preprocessing pipeline | Preprocessing (tahapan lengkap) | LENGKAP |
| Cross-dataset generalization | Cross Dataset Generalization | LENGKAP |
| Cross-GAN | Cross-GAN pada Deteksi Deepfake | LENGKAP |
| Metrik (Accuracy, Precision, Recall, F1) | Metrik Evaluasi Model | SEBAGIAN |
| Pemilihan metode | Dasar Pemilihan Metode | LENGKAP |
| Deep Learning & CNN | Deep Learning, CNN | LENGKAP |
| Pendekatan deteksi deepfake | Pendekatan Deteksi Deepfake | SEBAGIAN |

---

## 3. Apa yang HILANG dari BAB II (Kritis)

### 3.1 [KRITIS] XceptionNet - Seksi Utama Kosong
**Lokasi:** `## XceptionNet` dan `### Keunggulan XceptionNet dalam Deteksi Deepfake`
**Status:** `[perlu isi]` — KOSONG

XceptionNet adalah komponen UTAMA penelitian. Seksi ini wajib berisi:
- Arsitektur XceptionNet secara keseluruhan (entry blocks, middle flow, exit flow)
- Alasan pemilihan vs ResNet, EfficientNet, MesoNet (sudah dibahas di Dasar Pemilihan tapi perlu dikonsolidasi di seksi utama)
- Karakteristik depthwise separable convolution dalam konteks XceptionNet spesifik (sudah ada di seksi Depthwise tapi XceptionNet-nya sendiri perlu dijelaskan sebagai satu entitas)
- Transfer learning / pretrained weights (ImageNet) — ini penting karena kode menggunakan `pretrained=True` via timm

### 3.2 [KRITIS] Celeb-DF Dataset Tidak Ada
**Status:** HILANG SEPENUHNYA

BAB I Ruang Lingkup secara eksplisit menyebut **FaceForensics++** dan **Celeb-DF** sebagai kedua dataset. Kode pun memiliki `celeb_df_download.py` dan `--dataset CDF` di training script. Namun BAB II hanya membahas FaceForensics++. Perlu ditambahkan seksi Celeb-DF yang mencakup:
- Komposisi dataset (video selebriti, manipulasi face-swapping)
- Teknik manipulasi yang digunakan
- Mengapa digunakan untuk cross-dataset testing
- Perbedaan karakteristik artefak vs FF++

### 3.3 [KRITIS] AUC / ROC Curve Tidak Dibahas
**Status:** HILANG dari seksi Metrik Evaluasi

BAB I Ruang Lingkup menyebut: *"metrik accuracy, precision, recall, dan **AUC** (Area Under Curve)"*
Kode (`metrics.py`) menghitung `roc_auc_score` dan `roc_curve`, dan `train.py` memilih model terbaik berdasarkan `best_auc`. Namun BAB II hanya membahas Accuracy, Precision, Recall, F1-Score — **AUC tidak ada**.
Perlu ditambahkan:
- Konsep ROC Curve (FPR vs TPR)
- Definisi AUC dan interpretasinya
- Mengapa AUC relevan untuk deteksi deepfake (terutama threshold-independent evaluation)

### 3.4 [KRITIS] Pendekatan Hybrid Domain Spasial-Frekuensi - Kosong
**Lokasi:** `### Pendekatan Hybrid Domain Spasial-Frekuensi`
**Status:** `[perlu isi]` — KOSONG

Ini adalah inti kontribusi penelitian. Perlu membahas:
- Konsep arsitektur dual-domain / late fusion vs early fusion
- Related works: SpecXNet (Alam et al.), FSBI (Hasanaath et al.), Thinking in Frequency (Qian et al.)
- Dua strategi fusion yang diimplementasikan dalam kode: **early fusion** (4-channel input ke XceptionNet) dan **late fusion** / two-branch (HybridTwoBranch — XceptionNet spatial + FreqCNN frequency, concatenated)

### 3.5 [KRITIS] Perbandingan Domain Spasial vs Domain Frekuensi - Kosong
**Lokasi:** `### Perbandingan Domain Spasial dengan Domain Frekuensi`
**Status:** `[perlu isi]` — KOSONG

Konten sudah tersebar di beberapa seksi (Dasar Pemilihan Metode Tabel 2.8 sudah ada ringkasannya), tapi seksi formal ini perlu diisi atau dikembangkan sebagai tabel komparatif yang komprehensif.

### 3.6 [PERLU ISI] Artefak yang Dihasilkan Proses Generatif Deepfake - Kosong
**Lokasi:** `### Artefak yang Dihasilkan Proses Generatif Deepfake`
**Status:** `[perlu isi]` — KOSONG

Konten terkait sudah tersebar di seksi lain (Spectral Distortions, Periodic Noise, Warping). Seksi ini bisa diisi dengan konsolidasi atau ringkasan tipologi artefak dari proses generatif deepfake.

---

## 4. Gap Antara Kode dan BAB II

### 4.1 Dua Arsitektur Fusion - Hanya Satu yang Dibahas
**Kode mengimplementasikan:**
```
HybridTwoBranch   — late fusion: XceptionNet (spatial) + FreqCNN (frequency) → concat → classifier
EarlyFusionXception — early fusion: 4-channel (RGB + FFT magnitude) → XceptionNet
```
**BAB II hanya membahas** early fusion (4-channel) di seksi Depthwise Separable Convolution (integrasi FFT sebagai channel tambahan). `HybridTwoBranch` sebagai strategi late fusion **tidak dibahas sama sekali**.

**Rekomendasi:** Seksi "Pendekatan Hybrid Domain Spasial-Frekuensi" (yang masih kosong) harus menjelaskan kedua strategi ini dan perbedaannya.

### 4.2 FreqCNN - Branch Frekuensi Tidak Dibahas
**Kode:** `freq_cnn.py` — custom lightweight CNN (3 conv layers + BatchNorm + AdaptiveAvgPool) khusus memproses FFT magnitude 1-channel.
**BAB II:** Tidak ada pembahasan. Hanya membahas XceptionNet sebagai model utama.
**Rekomendasi:** Tambahkan penjelasan arsitektur FreqCNN di seksi XceptionNet atau Pendekatan Hybrid, sebagai branch frequency dalam HybridTwoBranch.

### 4.3 Optimizer: Adam vs SGD
**Kode (train.py line 136):**
```python
optimizer = optim.Adam(model.parameters(), lr=cfg.get("lr", 1e-4), weight_decay=cfg.get("weight_decay", 1e-4))
```
**BAB II:** Memiliki seksi panjang tentang **SGD** (Stochastic Gradient Descent) tapi kode menggunakan **Adam**. Adam adalah varian dari SGD dengan adaptive learning rate, tapi penjelasan teoritis di BAB II tidak relevan langsung dengan pilihan implementasi.
**Rekomendasi:** Seksi optimasi seharusnya fokus pada **Adam** (Adaptive Moment Estimation), bukan SGD. SGD bisa disebutkan sebagai konteks historis saja.

### 4.4 Transfer Learning / Pretrained Weights Tidak Dibahas
**Kode:** `build_xception(pretrained=True)` via `timm` — menggunakan bobot ImageNet pretrained.
**BAB II:** Tidak ada pembahasan tentang transfer learning atau fine-tuning dalam konteks XceptionNet.
**Rekomendasi:** Tambahkan di seksi XceptionNet: konsep transfer learning (ImageNet pretraining → deepfake fine-tuning), alasan penggunaan pretrained weights untuk training efisien pada dataset yang relatif kecil.

### 4.5 AUC Sebagai Metrik Primer Pemilihan Model
**Kode (train.py line 139, 147):**
```python
best_auc = -1.0
...
if val_metrics["auc"] > best_auc:
    best_auc = val_metrics["auc"]
```
Model terbaik dipilih berdasarkan **AUC**, bukan accuracy atau F1. Namun AUC tidak ada di BAB II Metrik Evaluasi.

### 4.6 Loss Function: BCEWithLogitsLoss
**Kode:** `nn.BCEWithLogitsLoss()` — binary cross-entropy with numerically stable sigmoid.
**BAB II:** Tidak membahas fungsi loss yang digunakan dalam pelatihan.
**Rekomendasi:** Tambahkan penjelasan singkat binary cross-entropy sebagai loss function untuk klasifikasi biner (asli vs deepfake).

### 4.7 Data Augmentation Specifics
**Kode (transforms.py):**
- Spatial: `RandomResizedCrop`, `RandomHorizontalFlip`, ImageNet normalization (mean/std)
- FFT: `CenterCrop` (bukan RandomCrop untuk FFT agar distribusi frekuensi tidak terdistorsi)
**BAB II:** Menyebut augmentasi secara umum tapi tidak menjelaskan pilihan augmentasi spesifik atau alasan mengapa FFT menggunakan CenterCrop (bukan RandomCrop).

### 4.8 Celeb-DF untuk Cross-Dataset Testing
**Kode:** Training script mendukung `--dataset CDF`. Ini mengindikasikan Celeb-DF digunakan untuk cross-dataset evaluation.
**BAB II:** Tidak ada pembahasan tentang Celeb-DF sama sekali.

---

## 5. Konten yang Tidak Diperlukan / Berlebihan di BAB II

### 5.1 Seksi SGD — Terlalu Panjang dan Tidak Sesuai Implementasi
**Lokasi:** `## Stochastic Gradient Descent (SGD)`
**Masalah:** Seksi ini sangat panjang dengan derivasi matematis penuh (full-batch GD, mini-batch SGD, varian), namun kode tidak menggunakan SGD — menggunakan Adam. Selain itu, optimasi bukan bagian dari novelty penelitian ini.
**Rekomendasi:** Ganti dengan seksi singkat tentang **Adam optimizer** (3-4 paragraf maksimal), atau ubah judul menjadi "Optimasi Model" yang mencakup Adam sebagai metode yang dipilih dengan justifikasi singkat vs SGD.

### 5.2 Seksi Analisis Video — Konten Temporal Tidak Diimplementasikan
**Lokasi:** `## Analisis Video`
**Masalah:** Seksi ini membahas analisis temporal dengan LSTM, GRU, 3D-CNN, Transformer untuk video deepfake. Namun:
- Kode hanya mengimplementasikan frame-level analysis (tidak ada LSTM/GRU/temporal model)
- BAB I Ruang Lingkup menyatakan: *"Penelitian tidak mencakup deteksi manipulasi audio"* dan fokus pada "frame video" bukan video sequence
- `extract_frames.py` mengekstrak frame individual, bukan video sequences

**Rekomendasi:** Potong bagian tentang LSTM/GRU/3D-CNN/Transformer (karena tidak diimplementasikan). Pertahankan hanya justifikasi mengapa frame-level analysis dipilih (efisiensi, relevansi artefak per-frame).

### 5.3 Bagian CNN Temporal dalam Seksi CNN — Tidak Relevan
**Lokasi:** Paragraf terakhir `## Convolution Neural Network (CNN)` — membahas CNN + LSTM/GRU untuk video dan referensi ke energy forecasting (Akinrogunde et al., 2025)
**Masalah:** Referensi ke energy consumption forecasting (`Akinrogunde, Adelakun, Theophilus, & Thomas, 2025`) sama sekali tidak relevan dengan deteksi deepfake. Ini tampaknya keliru masuk.
**Rekomendasi:** Hapus referensi energy forecasting dan paragraf temporal CNN yang tidak diimplementasikan.

### 5.4 Spectral Dropoff — Bisa Dikonsilidasikan
**Lokasi:** `## Spectral Dropoff`
**Masalah:** Konten sebagian besar overlap dengan `## Spectral Distortions dalam Deteksi Deepfake`. Spectral dropoff adalah subtipe dari spectral distortion dan bisa menjadi subseksi di dalamnya.
**Rekomendasi:** Pindahkan ke bawah Spectral Distortions sebagai `### Spectral Dropoff` untuk mengurangi redundansi.

### 5.5 Beberapa Konsep Diulang Berkali-kali
Konsep berikut dijelaskan berulang di beberapa seksi berbeda dengan narasi yang hampir sama:
- **Upsampling GAN menghasilkan artefak frekuensi** — muncul di: GAN, Spectral Distortions, Periodic Noise, Warping, FDA, FFT, Dasar Pemilihan
- **Durall et al. (2020) dan Zhang et al. (2019)** — dikutip berkali-kali dengan konteks yang hampir identik di hampir setiap seksi
- **SpecXNet dan FSBI** — direferensikan berulang tanpa tambahan insight baru

**Rekomendasi:** Konsolidasi narasi berulang, pastikan setiap penyebutan menambahkan nuansa baru. Gunakan cross-reference ke seksi yang sudah membahas daripada mengulang.

---

## 6. Ringkasan — Prioritas Tindakan

### Harus Ditambahkan (Kritis untuk Konsistensi)

| # | Item | Prioritas |
|---|---|---|
| # | Item | Prioritas | Status |
|---|---|---|---|
| 1 | Seksi XceptionNet (arsitektur, transfer learning) | SANGAT TINGGI | DONE — filled Entry/Middle/Exit Flow, 36 layers, transfer learning |
| 2 | Celeb-DF dataset | SANGAT TINGGI | DONE — added section 2.13 |
| 3 | AUC / ROC Curve di Metrik Evaluasi | TINGGI | DONE — added subsection 2.18.6 |
| 4 | Pendekatan Hybrid (early fusion + late fusion / two-branch) | SANGAT TINGGI | DONE — filled with both fusion strategies |
| 5 | FreqCNN sebagai frequency branch | TINGGI | DONE — described in hybrid section |
| 6 | Adam optimizer (ganti SGD) | TINGGI | DONE — renamed to "Optimasi Model", added Adam |
| 7 | Transfer learning / pretrained weights | SEDANG | DONE — covered in XceptionNet section |
| 8 | Binary Cross-Entropy loss function | SEDANG | DONE — added in training methodology |
| 9 | Perbandingan Domain Spasial vs Frekuensi (yang masih kosong) | SEDANG | DONE — filled with comparative analysis + Table 2.9 |
| 10 | Artefak Generatif (yang masih kosong) | SEDANG | DONE — filled with artifact typology |

### Harus Direvisi / Dikurangi

| # | Item | Rekomendasi | Status |
|---|---|---|---|
| 1 | Seksi SGD | Ganti dengan Adam, persingkat drastis | DONE — renamed to "Optimasi Model" |
| 2 | Analisis Video (bagian temporal CNN) | Potong LSTM/GRU/Transformer, pertahankan justifikasi frame-level | NOT ACTIONED |
| 3 | Referensi energy forecasting di CNN | Hapus sepenuhnya | DONE — Akinrogunde removed from Daftar Pustaka |
| 4 | Spectral Dropoff | Pindah jadi subseksi Spectral Distortions | DONE — renumbered to 2.5.6 |
| 5 | Pengulangan narasi GAN upsampling | Konsolidasi | NOT ACTIONED |

---

## 7. Catatan Teknis dari Kode

Beberapa detail implementasi yang perlu dicerminkan di BAB II / BAB III:

1. **Image size:** 224×224 (sudah tercakup di preprocessing)
2. **Normalization:** ImageNet mean `[0.485, 0.456, 0.406]` std `[0.229, 0.224, 0.225]` — implikasi transfer learning
3. **FFT preprocessing:** grayscale → FFT2D → fftshift → log magnitude → normalize [0,1] — sudah cukup tercakup di BAB II
4. **FFT augmentation:** CenterCrop (bukan RandomCrop) untuk menjaga integritas spektrum — perlu justifikasi di BAB II
5. **AUC sebagai model selection criterion** — perlu dibahas mengapa AUC dipilih vs F1 atau accuracy
6. **BCEWithLogitsLoss** — binary classification, output single logit per sample
7. **Model types tersedia:** `spatial` (XceptionNet saja), `freq` (FreqCNN saja), `hybrid` (HybridTwoBranch), `early_fusion` (EarlyFusionXception) — artinya ada 4 skenario eksperimen, perlu dijelaskan di BAB III
8. **Mixed precision training** (`torch.cuda.amp`) — detail implementasi
