# Analisis REVISI V1 + Rencana Relokasi RUMUS (BAB III → BAB II)

**Tanggal:** 2026-06-11
**Dokumen:** `REVISI V1 - Metode Peningkatan Deteksi Deepfake ... .docx` (OneDrive)
**Hasil acuan (settle):** commit `d28efae` — `deepfake_hybrid/results_vast_20260609/` (vast.ai full matrix, n100/250/500/750, 3 seed)
**Revisi sebelumnya yg belum semua masuk Word:** `710887f`

---

## 0. Ruang lingkup dokumen saat ini
REVISI V1 hanya memuat **BAB I, BAB II, BAB III + Daftar Pustaka**. **Belum ada BAB IV (Hasil) maupun BAB V.** Jadi analisis ini fokus pada (a) konsistensi narasi & parameter BAB I–III terhadap hasil final, dan (b) komentar dosen soal RUMUS di BAB III.

---

## PART A — Yang perlu diperbaiki/diubah (konten)

### A1. ⚠️ ISU TERBESAR — framing vs hasil negatif
Hasil final (tier andal n250/n500/n750, in-dataset AUC rata-rata 3 seed):

| Tier | Dataset | spatial (baseline) | **hybrid (usulan)** | freq |
|------|---------|------:|------:|-----:|
| n750 | CDF | **0,969** | 0,924 | 0,586 |
| n750 | FFPP | **0,780** | 0,650 | 0,546 |
| n500 | CDF | **0,967** | 0,892 | 0,615 |
| n500 | FFPP | **0,693** | 0,582 | 0,570 |
| n250 | CDF | **0,942** | 0,812 | 0,569 |
| n250 | FFPP | **0,746** | 0,542 | 0,480 |

- **Hybrid (usulan) KALAH dari XceptionNet baseline di SEMUA tier in-dataset, kedua dataset, AUC & F1.**
- Cabang **freq nyaris chance** (AUC in-dataset 0,55–0,59) → menyeret hybrid turun, bukan membantu.
- Klaim headline “fusi frekuensi **meningkatkan** deteksi” **tidak didukung data** in-dataset. Ini hal pertama yang akan disorot penguji.

**Nuansa cross-dataset (penting untuk framing):** pada arah **FFPP→CDF**, hybrid justru menahan F1 lebih baik (drop F1 hybrid ≈ 0,03/−0,01/−0,01 vs spatial 0,12/0,07/0,16 di n750/500/250), bahkan F1 cross-dataset hybrid > spatial di n250 & n500. Namun arah **CDF→FFPP** hybrid kolaps (recall jatuh; mis. n250 CDF→FFPP precision 0,94 / recall 0,08 / F1 0,15). Jadi hasilnya **campuran & bergantung arah**, bukan kemenangan bersih.

**Rekomendasi framing (Path A — aman, bisa hari ini):**
Ubah narasi dari “mengusulkan hybrid yang **meningkatkan** deteksi” → **“studi komparatif/ablation: apakah fusi domain frekuensi membantu XceptionNet, dengan temuan negatif yang jujur + analisis akar penyebab.”** Negative result itu sah secara ilmiah selama *mengapa*-nya dianalisis (cabang freq kehilangan sidik jari upsampling akibat FFT pada wajah ter-crop & ter-kompresi; cabang near-chance menyuntik noise; SE-gating gagal menekan cabang buruk).

Kabar baik: **Rumusan Masalah & Tujuan di BAB I sudah berbentuk pertanyaan/ablation** (“sejauh mana…”, “ablation study spasial vs frekuensi vs hybrid”) — ini sudah defensible. Yang perlu **dilunakkan** hanya kalimat asertif di **Latar Belakang & paragraf penutup BAB I**:
- “fusi dua domain **bermanfaat**” / “…dioptimalkan untuk generalisasi” → ubah ke bentuk hipotesis/pertanyaan yang akan diuji, bukan klaim hasil.

> Catatan: jika tim mau mengejar **Path B** (perbaiki cabang freq — cek loading `fft_stats.json`, trainability standalone, pretrain/freeze freq branch) sebelum settle, hybrid berpotensi membalik. Tapi user menyatakan ingin **settle dengan hasil d28efae**, jadi default = Path A (reframe).

### A2. ⚠️ Ukuran sampel — Tabel 3.3 TIDAK cocok dengan hasil final
- **Tabel 3.3 (BAB III)** menulis FFPP = `100, 300, 600, 1000`. **Hasil final memakai FFPP = `100, 250, 500, 750`** (lihat `results_vast_20260609/tables/n250/Table1_in_dataset_summary.csv` ada baris `freq,FFPP,FFPP` dst). CDF sudah `100, 250, 500, 750` (cocok).
- **Aksi:** ubah Tabel 3.3 baris FFPP → `100, 250, 500, 750` (samakan kedua dataset), dan sesuaikan semua kalimat yang menyebut “1000 video FFPP”.

### A3. Tabel 1.1 & Tabel 3.1 — komposisi FFPP n=1000
- Tabel 1.1 menyebut `FaceForensics++ (n=1000, c23)` & ~50.000 frame; Tabel 3.1 juga 1.000 video / 50.000 frame. Tier maksimum yang **benar-benar dijalankan** untuk FFPP pada hasil final = **750**, bukan 1000.
- **Aksi:** putuskan satu cerita. Opsi termudah & konsisten: nyatakan komposisi **populasi** dataset (boleh tetap 1000/750 sebagai ukuran sumber) TAPI perjelas bahwa **eksperimen mengambil subset 100–750**. Hilangkan kesan “dilatih pada 1000 video FFPP”.

### A4. Typo / kesalahan kecil BAB I (sekalian diperbaiki)
- “**Sebagai besar** generator deepfake…” → “**Sebagian besar**”.
- “**Alam el at.** menunjukkan…” → “**Alam et al.**”.
- Ruang Lingkup: URL Celeb-DF terpotong jadi dua baris “…celeb-deepfakeforens / ics” → rapikan jadi satu: `https://github.com/yuezunli/celeb-deepfakeforensics`.
- Cek konsistensi sitasi [13] dipakai untuk dua hal berbeda (Alam et al. & SpecXNet) di Latar Belakang — pastikan nomor referensi benar (isu sinkronisasi [N] vs Daftar Pustaka sudah pernah dicatat).

### A5. Redundansi rumus DALAM BAB II (cleanup)
BAB II memuat rumus FFT **dua kali**: bagian *Transformasi Fourier (FFT)* (2.1 DFT, 2.3 magnitude, 2.4 log) dan bagian *Fast Fourier Transform (FFT)* di Preprocessing (2.13 DFT, 2.14 magnitude, 2.15 log, 2.16 fftshift). Sebaiknya **konsolidasi** agar tidak dobel — penting karena rumus dari BAB III akan dipindah ke sini juga (lihat Part B).

---

## PART B — Komentar dosen: hilangkan RUMUS dari BAB III

**Aturan dosen:** BAB III hanya boleh berisi **perhitungan** (contoh angka yang disubstitusi), **bukan definisi rumus**. Semua definisi rumus dipindah ke **BAB II**.

BAB III saat ini memuat **38 persamaan bernomor (3.1–3.38)**. Klasifikasi:
- **RUMUS (definisi simbolik)** → HAPUS dari BAB III. Jika belum ada di BAB II → TAMBAHKAN; jika sudah ada (duplikat) → cukup hapus.
- **PERHITUNGAN (contoh angka)** → **TETAP** di BAB III (ganti referensi ke “Persamaan 2.x”).

### B1. Tabel keputusan per persamaan BAB III

| Eq | Bagian (Heading) | Isi singkat | Jenis | Status di BAB II | **AKSI** |
|----|------------------|-------------|-------|------------------|----------|
| 3.1 | Konversi Domain Frekuensi | Grayscale `Y=0,299R+0,587G+0,114B` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.2 | Konversi Domain Frekuensi | DFT 2D `F(u,v)=ΣΣ…` | RUMUS | **duplikat 2.1 / 2.13** | Hapus dari III |
| 3.3 | Konversi Domain Frekuensi | Magnitude `\|F\|=√(Re²+Im²)` | RUMUS | **duplikat 2.3 / 2.14** | Hapus dari III |
| 3.4 | Konversi Domain Frekuensi | Gaussian high-pass `H(u,v)=1−exp(…)` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.5 | Konversi Domain Frekuensi | Log scaling `M_log=log(1+\|F'\|)` | RUMUS | **duplikat 2.4 / 2.15** | Hapus dari III |
| 3.6 | Konversi Domain Frekuensi | Contoh `F(0,0)=…` | PERHITUNGAN | — | **TETAP** (ref ke 2.x) |
| 3.7 | Konversi Domain Frekuensi | Contoh `F(0,1)=…` | PERHITUNGAN | — | **TETAP** |
| 3.8 | Konversi Domain Frekuensi | Contoh `F(1,0)=…` | PERHITUNGAN | — | **TETAP** |
| 3.9 | Konversi Domain Frekuensi | Contoh `F(1,1)=…` | PERHITUNGAN | — | **TETAP** |
| 3.10 | Konversi Domain Frekuensi | Z-score `x'=(x−μ)/σ` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.11 | Augmentasi Data | Gaussian noise `x_fft+=ε` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.12 | Augmentasi Data | Band masking horizontal | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.13 | Augmentasi Data | Band masking vertikal | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.14 | Model Spasial XceptionNet | Matriks contoh `X1, X2` | PERHITUNGAN | — | **TETAP** |
| 3.15 | Model Spasial XceptionNet | Kernel contoh `W1, W2` | PERHITUNGAN | — | **TETAP** |
| 3.16 | Model Spasial XceptionNet | `1×1+2×0+…=2` | PERHITUNGAN | — | **TETAP** |
| 3.17 | Model Spasial XceptionNet | hasil depthwise (angka) | PERHITUNGAN | — | **TETAP** |
| 3.18 | Model Spasial XceptionNet | `Z=0,5·Y1+0,5·Y2` (pointwise, angka) | PERHITUNGAN | — | **TETAP** |
| 3.19 | Model Frekuensi FreqCNN | Residual block `y=MaxPool(Conv(x))+Shortcut(x)` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.20 | Model Frekuensi FreqCNN | Matriks input 4×4 (angka) | PERHITUNGAN | — | **TETAP** |
| 3.21 | Model Frekuensi FreqCNN | `0·w20+0,8·w21+…` | PERHITUNGAN | — | **TETAP** |
| 3.22 | Model Frekuensi FreqCNN | BatchNorm `z=(z−μ)/√(σ²+ε)·γ+β` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.23 | Model Hybrid | Proyeksi `h_sp=ReLU(BN(Ws·f+bs))` | RUMUS | **belum ada** | **Pindah → BAB II** (lihat catatan B3), hapus dari III |
| 3.24 | Model Hybrid | Proyeksi `h_fr=ReLU(BN(Wf·f+bf))` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.25 | Model Hybrid | SE-gating `g=σ(W2·ReLU(W1·…))` | RUMUS | **duplikat 2.11** | Hapus dari III |
| 3.26 | Model Hybrid | Scaling `h=h⊙g` | RUMUS | **duplikat 2.12** | Hapus dari III |
| 3.27 | Model Hybrid | `f_sp=…, f_fr=…` (angka) | PERHITUNGAN | — | **TETAP** |
| 3.28 | Model Hybrid | `h_fused=[…]∈R⁸` (angka) | PERHITUNGAN | — | **TETAP** |
| 3.29 | Model Hybrid | `h⊙g=[…]` (angka) | PERHITUNGAN | — | **TETAP** |
| 3.30 | Fungsi Loss | BCE `L=−1/N Σ[…]` | RUMUS | **duplikat 2.23** | Hapus dari III |
| 3.31 | Fungsi Loss | pos_weight `w_p=n_neg/n_pos` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.32 | Fungsi Loss | Label smoothing `y'=y(1−α)+α·0,5` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.33 | Fungsi Loss | `y'=1·(1−α)+α·0,5` (angka) | PERHITUNGAN | — | **TETAP** |
| 3.34 | Fungsi Loss | `σ(2,5)=…=0,924` | PERHITUNGAN | — | **TETAP** |
| 3.35 | Fungsi Loss | `L=−y'·lnσ+…` (substitusi contoh) | PERHITUNGAN* | — | **TETAP** (ref ke 2.23; lihat catatan) |
| 3.36 | Gradient Clipping | `g←g·5/‖g‖ jika ‖g‖>5` | RUMUS | **belum ada** | **Pindah → BAB II**, hapus dari III |
| 3.37 | Evaluasi Cross-Dataset | `Δ=F1_in−F1_cross` | RUMUS | **belum ada** | **Pindah → BAB II** (satu saja), hapus dari III |
| 3.38 | Generalization Drop | `Δ=F1_in−F1_cross` (dup 3.37) | RUMUS | duplikat 3.37 | Hapus dari III |

\* 3.35 secara teknis adalah penulisan ulang rumus loss per-sampel di tengah contoh; boleh tetap sebagai langkah substitusi, cukup tambahkan “(berdasarkan Persamaan 2.23)”. Kalau dosen ketat, ubah jadi langsung angka tanpa bentuk simbolik.

**Ringkas:**
- **HAPUS dari BAB III (20 rumus):** 3.1, 3.2, 3.3, 3.4, 3.5, 3.10, 3.11, 3.12, 3.13, 3.19, 3.22, 3.23, 3.24, 3.25, 3.26, 3.30, 3.31, 3.32, 3.36, 3.37, 3.38.
- **TETAP di BAB III (perhitungan):** 3.6–3.9, 3.14–3.18, 3.20, 3.21, 3.27–3.29, 3.33–3.35, + Tabel 3.13/3.14 (perhitungan metrik — sudah benar bentuknya).

### B2. Yang perlu DITAMBAHKAN ke BAB II (rumus yang belum ada di sana)

Hanya rumus berikut yang **belum** ada di BAB II dan harus ditambah (sisanya sudah duplikat → cukup dihapus dari III):

1. **Grayscale ITU-R BT.601** (dari 3.1) → tambah di bagian *Fast Fourier Transform (FFT)* / Preprocessing BAB II, sebelum DFT.
2. **Gaussian high-pass mask `H(u,v)`** (dari 3.4) → tambah setelah magnitude spectrum di bagian FFT-Preprocessing BAB II.
3. **Normalisasi z-score `x'=(x−μ)/σ`** (dari 3.10) → tambah di bagian FFT/normalisasi BAB II.
4. **Augmentasi domain frekuensi** (dari 3.11–3.13: Gaussian noise injection + spectral band masking) → **buat subbab baru “Augmentasi Data” di BAB II** (BAB II belum punya). Muat ketiga rumus operasi ini.
5. **Residual block FreqCNN** `y=MaxPool₂ₓ₂(Conv₃ₓ₃(x))+Shortcut(x)` (dari 3.19) → tambah (lihat catatan B3).
6. **Batch Normalization** `ẑ=(z−μ_B)/√(σ_B²+ε)·γ+β` (dari 3.22) → tambah di subbab CNN/Deep Learning BAB II (rumus generik).
7. **Proyeksi fitur fusi** `h=ReLU(BN(W·f+b))` (dari 3.23/3.24) → tambah (lihat catatan B3).
8. **pos_weight** `w_p=n_neg/n_pos` (dari 3.31) → tambah di bagian *Binary Cross-Entropy* BAB II (dekat 2.23).
9. **Label smoothing** `y'=y(1−α)+α·0,5` (dari 3.32) → tambah di bagian *Binary Cross-Entropy / Optimasi* BAB II.
10. **Gradient clipping** `g←g·(c/‖g‖₂) bila ‖g‖₂>c` (dari 3.36) → tambah di bagian *Optimasi Model* BAB II.
11. **Generalization drop** `Δ=F1_in−F1_cross` (dari 3.37/3.38) → tambah di bagian *Cross Dataset Generalization* BAB II (sudah ada subbab-nya, tinggal sisipkan rumus).

Rumus yang **TIDAK perlu** ditambah (sudah ada di BAB II): DFT (2.1/2.13), magnitude (2.3/2.14), log (2.4/2.15), SE-gating (2.11), scaling SE (2.12), BCE (2.23).

### B3. Catatan keputusan — rumus milik arsitektur usulan (3.19, 3.22–3.26)
Rumus 3.19 (FreqCNN), 3.23/3.24 (proyeksi), 3.25/3.26 (SE fusi) adalah **definisi arsitektur yang diusulkan** — biasanya wajar berada di BAB III (perancangan). Tapi aturan dosen tegas “BAB III tanpa rumus”. Dua opsi:
- **(Strict, default rekomendasi)** Pindahkan bentuk **generik/konsep**-nya ke BAB II (residual block, BatchNorm, proyeksi linear+BN+ReLU, SE-gating sudah di 2.11). Di BAB III, jelaskan arsitektur dalam **prosa + diagram + contoh angka** (3.27–3.29 yang sudah ada).
- **(Lenient)** Konfirmasi ke dosen apakah rumus *arsitektur usulan* boleh tetap di BAB III sebagai bagian “perancangan”. Banyak skripsi mengizinkan ini.

→ **Saran:** konfirmasi poin ini ke dosen; sambil menunggu, terapkan strict (paling aman terhadap komentar yang sudah diberikan).

### B4. Konsekuensi teknis saat mengedit docx
1. **Penomoran ulang:** menghapus 20 persamaan akan menggeser nomor (3.x) sisanya dan nomor (2.x) baru. Jika penomoran manual, renumber; jika pakai field caption Word, update otomatis.
2. **Re-pointing prosa:** tiap contoh perhitungan yang tetap di BAB III harus mengganti “…didefinisikan sebagai (3.2)” menjadi “…sesuai **Persamaan 2.1**”.
3. **Daftar Persamaan / Daftar Gambar:** perbarui bila ada.
4. Konsolidasikan dulu duplikasi FFT di BAB II (A5) sebelum menambah rumus baru agar tidak makin dobel.

---

## Ringkasan prioritas
1. **(Konten, kritis)** Reframe klaim “meningkatkan” → studi komparatif + temuan negatif jujur (A1). Lunakkan Latar Belakang & penutup BAB I.
2. **(Konsistensi, kritis)** Perbaiki Tabel 3.3 ukuran sampel FFPP → 100/250/500/750; selaraskan Tabel 1.1/3.1 soal n=1000 (A2, A3).
3. **(Dosen)** Hapus 20 rumus dari BAB III; tambah 11 rumus ke BAB II (sisanya duplikat). Buat subbab “Augmentasi Data” di BAB II. Konfirmasi status rumus arsitektur usulan (B1–B3).
4. **(Minor)** Typo & URL BAB I (A4); konsolidasi duplikat FFT BAB II (A5).
