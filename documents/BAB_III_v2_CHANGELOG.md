# CHANGE LOG — Revisi BAB III Tahapan Pelaksanaan v2
**Tanggal:** 4 April 2026
**File:** `BAB_III_Tahapan_Pelaksanaan_v2.md`
**Revisi dari:** 847 baris → 904 baris (+57 baris)

---

## Perubahan Global

### Referensi: IEEE [N] → (Author, Year)
Seluruh referensi IEEE diganti format author-year:

| Lama | Baru |
|------|------|
| [1] | (Odena et al., 2016) |
| [2] | (Durall et al., 2020) |
| [3] | (Chollet, 2017) |
| [4] | (Rössler et al., 2019) |
| [5] | (Li et al., 2020) |
| [6] | (Zhang et al., 2019) |
| [7] | (Chollet, 2017; Rössler et al., 2019) |
| [8] | (Hu et al., 2018) — **perlu ditambahkan ke daftar pustaka** |
| [9] | (Kingma & Ba, 2015) + tambah (Loshchilov & Hutter, 2019) untuk AdamW |

### Penomoran Ulang
- **Persamaan:** Renomor 3.1–3.37 (dari 3.1–3.39) karena penambahan persamaan baru dan penghapusan metrik duplikat
- **Gambar:** Renomor 3.1–3.11 (dari 3.1–3.8) karena penambahan 3 gambar baru
- **Tabel:** Renomor 3.1–3.16 (dari 3.1–3.14) karena penambahan 3 tabel hasil + penghapusan tabel metrik duplikat

---

## Perubahan per Bagian

### [3.3.3.1] Augmentasi Domain Spasial — TAMBAH
- **Langkah 3 (baru):** ColorJitter (brightness=±0.2, contrast=±0.2, saturation=±0.1, hue=±0.05)
- **Langkah 7 (baru):** RandomErasing (p=0.1, scale=2%–15%) — beroperasi pada tensor setelah normalisasi
- Pipeline augmentasi sekarang 7 langkah (sebelumnya 5)

### [3.3.3.2] Augmentasi Domain Frekuensi — TAMBAH
- **Spectral band masking** (p=0.15): Pita frekuensi horizontal/vertikal acak diisi nol
- 2 persamaan baru (3.11, 3.12)
- **Gambar baru:** Gambar 3.3 — Contoh spectral band masking
  - Search keyword: "spectral band masking frequency domain augmentation"

### [3.4.2.1] Arsitektur FreqCNN — REWRITE
- **Lama:** Plain conv blocks (Conv2d + BN + ReLU + MaxPool), depth=3, ~130K params
- **Baru:** FreqBlock dengan koneksi residual (Conv2d + BN + ReLU + Shortcut 1×1 + MaxPool), depth=5, ~700K params
- Channel progression: [32, 64, 128, 256, 256]
- Persamaan baru (3.18) untuk FreqBlock residual
- Referensi baru: (He et al., 2016) untuk residual learning
- **Gambar baru:** Gambar 3.6 — Arsitektur FreqBlock
  - Search keyword: "residual block diagram CNN skip connection 1x1 convolution"

### [Tabel 3.5] — REWRITE LENGKAP
- **Lama:** 3 blok conv + classifier, ~130K params
- **Baru:** 5 FreqBlock residual + Dropout2d + GAP + classifier, ~700K params

### [3.4.3.2] Cabang Frekuensi Hybrid — UPDATE
- Dimensi output: 128 → **256** (depth=3 → depth=5)

### [3.4.3.3] Projection Layers — UPDATE
- Rasio dimensi: "16:1" → **"8:1"**
- Matriks bobot: $W_f \in \mathbb{R}^{256 \times 128}$ → **$\mathbb{R}^{256 \times 256}$**

### [3.4.3.5] Classifier Head — UPDATE
- Dropout pertama: **0,5 → 0,3**

### [Tabel 3.6] Perbandingan Arsitektur — UPDATE
- FreqCNN dimensi fitur: 128 → **256**
- FreqCNN total parameter: ~130K → **~700K**
- Hybrid total parameter: ~23,2M → **~23,8M**

### [Tabel 3.7] Dimensi Fitur Hybrid — UPDATE
- FreqCNN backbone output: 128 → **256**
- Proyeksi frekuensi input: 128 → **256**

### [Diagram HybridTwoBranch] — UPDATE
- FreqCNN output: (128) → **(256)**
- FreqBlock description: "3 conv blocks" → **"5 FreqBlocks residual"**
- Proyeksi: (128→256) → **(256→256)**

### [3.5.1] Backbone Freezing — UPDATE
- **Lama:** "Pada model hybrid dan early fusion..."
- **Baru:** "Pada seluruh model yang menggunakan backbone XceptionNet pretrained (spatial, hybrid, dan early fusion)..."

### [Tabel 3.8] Learning Rate — UPDATE
- Backbone LR: 1×10⁻⁵ → **2×10⁻⁵**
- Head LR: 1×10⁻⁴ → **2×10⁻⁴**

### [3.5.3] Penjadwalan LR — UPDATE
- Epoch 1: 1×10⁻⁵ → **2×10⁻⁵**
- Epoch 2: 1×10⁻⁴ → **2×10⁻⁴**
- Cosine decay: dari 1×10⁻⁴ → dari **2×10⁻⁴**

### [3.5.4] Fungsi Loss — RESTRUCTURE
- **Judul:** "BCEWithLogitsLoss dengan Label Smoothing" → **"BCEWithLogitsLoss dengan Pos Weight"**
- **Tambah subsection 3.5.4.1:** Penyeimbangan Kelas (Pos Weight) — $w_p = n_{neg}/n_{pos}$
- **Tambah subsection 3.5.4.2:** Label Smoothing — penjelasan tetap, tapi dicatat dinonaktifkan (α=0)
- **Renomor subsection 3.5.4.3:** Contoh perhitungan (sebelumnya 3.5.4.1)
- Formula BCE (3.29) sekarang termasuk $w_p$

### [3.5.5] Optimizer — REWRITE
- **Judul:** "Adam dengan Gradient Accumulation" → **"AdamW dengan Gradient Accumulation"**
- **Lama:** Adam, lr=1×10⁻⁴, regularisasi L2
- **Baru:** AdamW (Loshchilov & Hutter, 2019), lr=2×10⁻⁴, decoupled weight decay
- Penjelasan perbedaan decoupled weight decay vs L2

### [3.5.6] Gradient Clipping — UPDATE
- max_norm: 1,0 → **5,0**
- Rationale ditambahkan: mengakomodasi LR lebih tinggi

### [3.5.8] Early Stopping — UPDATE
- Patience: 5 → **10**
- Paragraf baru: rationale peningkatan patience (recovery setelah unfreezing)

### [Tabel 3.9] Ringkasan Hyperparameter — REWRITE LENGKAP
Semua nilai diperbarui. Baris baru: pos_weight, FreqCNN depth.

### [Tabel 3.11] Variabel Penelitian — UPDATE
- Seed: 42, 43, 44 → **0, 1, 2**

### [3.7] Metode Evaluasi — TRIM
- **Dihapus:** Section 3.7.1–3.7.6 (Confusion Matrix, Accuracy, Precision, Recall, F1, AUC-ROC) — sudah ada di BAB II
- **Ditambah:** Paragraf referensi ke BAB II
- **Dipertahankan:** Generalization Drop (renomor ke 3.7.1) dan Contoh Perhitungan (renomor ke 3.7.2)
- **Tabel dihapus:** Tabel Struktur Confusion Matrix (duplikat BAB II)
- **Tabel dipertahankan:** Tabel 3.12 (Contoh Confusion Matrix), Tabel 3.13 (Perhitungan Metrik)

### [3.8] Hasil Eksperimen Awal — DIPINDAHKAN KE BAB IV
- Konten hasil (Tabel, Gambar) dipindahkan ke BAB IV sesuai pedoman skripsi
- Draft tersimpan di `documents/BAB_IV_draft_hasil_awal.md`
- HTML tables (`tabel_3_14_hasil_in_dataset.html`, `tabel_3_15_hasil_cross_dataset.html`, `tabel_3_16_generalization_drop.html`) tetap tersedia, perlu di-renumber ke Tabel 4.X saat menyusun BAB IV
  - Search keyword: "grouped bar chart model comparison AUC F1 in-dataset cross-dataset"
  - Plots tersedia di `outputs/2026-04-03/plots/`

---

## Gambar yang Perlu Ditambahkan

| No. | Keterangan | Search Keyword |
|-----|-----------|----------------|
| Gambar 3.3 | Contoh spectral band masking pada peta FFT (asli vs masked) | "spectral band masking frequency domain augmentation" |
| Gambar 3.6 | Arsitektur FreqBlock dengan koneksi residual | "residual block diagram CNN skip connection 1x1 convolution" |
| Gambar 3.11 | Perbandingan AUC dan F1 ketiga model (n=100, in-dataset + cross-dataset) | "grouped bar chart model comparison AUC F1" |

## Gambar yang Di-renomor

| Lama | Baru |
|------|------|
| Gambar 3.3 (Flowchart Preprocessing) | Gambar 3.4 |
| Gambar 3.4 (Perbandingan FFT) | Gambar 3.5 |
| Gambar 3.5 (Arsitektur XceptionNet) | Gambar 3.7 |
| Gambar 3.6 (Arsitektur FreqCNN) | Gambar 3.8 |
| Gambar 3.7 (Arsitektur HybridTwoBranch) | Gambar 3.9 |
| Gambar 3.8 (Kurva LR Schedule) | Gambar 3.10 |
