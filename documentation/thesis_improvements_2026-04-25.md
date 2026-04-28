# Thesis Improvements — Revisi Pasca Pra Ujian Akhir

**Tanggal:** 2026-04-25
**Sumber feedback:** `documents/reviewer_feedback/Hasil Tinjauan Pra Ujian Akhir - Pembanding 1.pdf` (Nilai 70) dan `Pembanding 2.pdf` (Nilai 78)
**Dokumen target revisi:** `documents/Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi.pdf` (source DOCX/GDoc — perlu dikonfirmasi)

---

## Ringkasan Tema Feedback

Dua pembanding sepakat pada tiga isu besar:

1. **Fokus masalah belum tajam** — latar belakang luas, rumusan masalah lebih ke solusi, tidak ada benang merah eksplisit menuju "apa yang diselesaikan".
2. **Konsistensi antar bagian lemah** — rumusan masalah ↔ tujuan terkesan duplikasi; manfaat operasional kontradiktif dengan ruang lingkup; BAB III menyebut 3 arsitektur padahal BAB I usulan 1 arsitektur hybrid.
3. **Detail teknis & sitasi kurang** — banyak gambar/tabel BAB II tanpa sitasi; alur algoritma BAB III kurang detail (sekadar "pakai library"); tidak ada analisis sistem; total dataset tidak disebut.

Plus catatan struktural P2: paragraf < 5 kalimat, anak subbab 1 paragraf, format rumus.

---

## BAB I — PENDAHULUAN

### 1.1 Latar Belakang

| # | Feedback | Aksi |
|---|----------|------|
| LB-1 | (P2) Paragraf 1 & 2 dapat digabung; ideal 5–7 kalimat | Gabung paragraf 1+2 jadi satu paragraf 5–7 kalimat: GAN → deepfake realistis → ancaman (fake news, privasi, deepfake porn). Sitasi [1], [2]. |
| LB-2 | (P1) Masalah terlalu luas; (P1) Apakah tujuan meningkatkan kinerja XceptionNet? | Tambahkan kalimat eksplisit yang menyempitkan masalah: **"Penelitian ini menargetkan penurunan kemampuan generalisasi cross-dataset/cross-GAN pada detektor berbasis domain spasial murni (XceptionNet) yang cenderung overfit terhadap artefak visual spesifik dataset training."** Bukti pendukung di bawah. |
| LB-3 | (P2) Paragraf 5 hanya 1 sitasi & 2 kalimat ("sejumlah penelitian...") | Perpanjang ke 5–7 kalimat dengan minimal 3 sitasi: [7] Durall, [8] Zhang, [13] Qian, [22] Tan — masing-masing disebutkan kontribusi metodenya secara singkat. |
| LB-4 | (P2) Paragraf 7–8 kontradiktif | Reframe: paragraf 7 = "studi awal menunjukkan **potensi** gabungan dua domain"; paragraf 8 = gap spesifik = **belum ada hybrid yang dioptimalkan untuk generalisasi cross-dataset dengan mekanisme fusi adaptif (mis. SE gating)**. Bukan "belum ada hybrid sama sekali". |
| LB-5 | (P2) Urgensi generalisasi cross-dataset belum muncul | Tambahkan 1–2 kalimat: penyerang menggunakan generator baru, deployment dunia nyata berbeda dari training data — sehingga generalisasi adalah syarat utama, bukan sekedar akurasi in-domain. |

#### Bukti pendukung untuk LB-2 (klaim XceptionNet drop pada cross-dataset)

Klaim ini sudah didukung literatur dan sebagian sudah disitasi tesis:

- **Li et al., "Celeb-DF: A Large-scale Challenging Dataset for DeepFake Forensics," CVPR 2020** — XceptionNet dari FF++ ke Celeb-DF turun ke ~84% AUC dari 96–99% in-domain. Sitasi primer paling kuat untuk klaim drop. Tambahkan ke daftar pustaka jika belum ada (saat ini disitasi sebagai [35] di BAB III, pastikan format konsisten).
- **Citation [5]** (sudah ada) — ResNet performa menurun cross-dataset.
- **Citation [10]** (sudah ada — Rana et al.) — spatial detectors mengandalkan "artefak permukaan spesifik terhadap proses pembuatan tertentu".
- **Tabel 2.1** (sudah ada) — spatial generalisasi: "Terbatas, cenderung overfit pada tekstur spesifik dataset."
- Sumber sekunder (web search): CNN-based detectors > 15% performa drop cross-dataset; "detectors overfit to generator-specific artifacts — checkerboard patterns in StyleGAN, periodic noise residues from diffusion decoders".

> **Kesimpulan:** klaim aman diassert. Cukup tambah 1 sitasi primer (Li et al. Celeb-DF) di kalimat masalah agar pembanding melihat angka konkret.

### 1.2 Rumusan Masalah

| # | Feedback | Aksi |
|---|----------|------|
| RM-1 | (P1) Lebih ke solusi; (P1) tidak terlihat di latar belakang | Reformulasi dari bentuk solusi → bentuk masalah. Setiap point harus ada paragraf turunan di latar belakang. |
| RM-2 | (P2) Point 1 cukup "video sintetis", tidak perlu "citra atau video" | Hapus frase "citra atau video", ganti jadi "video sintetis (deepfake)". |
| RM-3 | (P2) Point 2 tidak punya turunan di latar belakang | Hapus point 2 (terlalu teknis-solusi, redundan), atau reformulasi jadi masalah turunan. |

**Usulan rumusan masalah baru:**

1. Bagaimana mendeteksi manipulasi video sintetis yang artefak spasialnya semakin halus pada model generatif modern?
2. Sejauh mana keterbatasan generalisasi detektor berbasis domain spasial murni pada skenario cross-dataset?
3. Sejauh mana penambahan analisis domain frekuensi (FFT) ke detektor spasial dapat meningkatkan robustness pada skenario cross-dataset?

### 1.3 Tujuan

| # | Feedback | Aksi |
|---|----------|------|
| TJ-1 | (P1) Terkesan duplikasi rumusan masalah | Ubah dari paraphrase rumusan masalah jadi **deliverable konkret**. |

**Usulan tujuan baru:**

1. Mengimplementasikan arsitektur hybrid XceptionNet–FFT dengan late fusion + SE gating.
2. Melakukan ablation study (spasial-only vs frekuensi-only vs hybrid) untuk mengukur kontribusi tiap domain.
3. Mengevaluasi generalisasi cross-dataset pada skenario FFPP→CDF dan CDF→FFPP.

### 1.4 Manfaat

| # | Feedback | Aksi |
|---|----------|------|
| MF-1 | (P2) Manfaat 4 (kecepatan inferensi) kontradiktif dengan ruang lingkup | **Hapus manfaat 4.** Ruang lingkup eksplisit menyatakan tidak fokus optimasi inferensi. |
| MF-2 | (P2) Manfaat 5 (alat forensik andal/akurat) butuh pengujian dengan teknologi saat ini | Hapus klaim "lebih andal dan akurat". Reformulasi jadi: "Memberikan referensi metodologis bagi pengembang sistem deteksi deepfake yang ingin mengevaluasi kontribusi domain frekuensi dalam arsitektur hybrid." |
| MF-3 | (P1) Tanpa implementasi, manfaat hanya ke yang menerima | Reframe manfaat akademik/sosial/teknologi sebagai manfaat untuk **pihak penerima** (akademisi, peneliti, lembaga forensik untuk pertimbangan pengembangan lanjutan), bukan klaim langsung tentang capability sistem. |

### 1.5 Ruang Lingkup

| # | Feedback | Aksi |
|---|----------|------|
| RL-1 | (P1) Tipe data tidak jelas (citra/video) | Tambah eksplisit: "Sumber data adalah **video**, kemudian diekstraksi menjadi **frame citra** untuk diproses model." |
| RL-2 | (P2) Tambahkan sitasi link dataset + total dataset | Tambah link repo + total. FFPP: github.com/ondyari/FaceForensics ([19]). CDF: github.com/yuezunli/celeb-deepfakeforensics ([35]). |
| RL-3 | (P1) Kriteria seleksi tidak jelas | Tambah: pengambilan acak rasio 50:50 real/fake, stratified split level video. |

**Total dataset yang dipakai (verifikasi dari `outputs/manifests/`):**

| Dataset | Real videos | Fake videos | Total frames (~) |
|---------|-------------|-------------|------------------|
| FFPP (n=1000, c23) | 500 | 500 | ~50.000 |
| CDF v2 (n=750) | 375 | 375 | ~37.500 |

(Asumsi 50 frame/video × 1000 video = 50K. Verifikasi sebelum final.)

---

## BAB II — KAJIAN LITERATUR

### 2.A Sitasi gambar dan tabel (P1)

Audit semua, tambah sitasi yang masih kurang:

| Item | Status | Aksi |
|------|--------|------|
| Gambar 2.1 (Distribusi Low/High-Frequency) | tidak ada sitasi | **Tambah sitasi** sumber gambar (kemungkinan Durall et al. [7] atau buku Gonzales & Woods) |
| Gambar 2.2 (Representasi Domain Frekuensi) | [21] ✓ | OK |
| Tabel 2.1, 2.2, 2.3, 2.7, 2.8, 2.9 | sitasi lengkap ✓ | OK |
| Tabel 2.4 (Tahapan Preprocessing) | cek | Tambah sitasi jika belum |
| Tabel 2.5 (Confusion Matrix) | tidak ada | Tambah sitasi (Goodfellow / textbook ML) |
| Tabel 2.6 (Hasil Perhitungan Metrik) | tidak ada | Tambah sitasi |

### 2.B Subbab tanpa sitasi (P2)

| Subbab | Issue | Aksi |
|--------|-------|------|
| 2.3.4 | Penjelasan Early/Late Fusion tidak ada sitasi | Tambah sitasi [9] SpecXNet, [18] FSBI, paper hybrid lain yang sudah ada di pustaka |
| 2.9.4 | Depthwise separable convolution tidak ada referensi | Tambah sitasi Chollet [6] di paragraf yang menjelaskan konsep |
| 2.11.1, 2.11.2 (SE Networks) | Tidak ada referensi | **Tambah Hu et al. (2018) "Squeeze-and-Excitation Networks" CVPR ke daftar pustaka.** Sitasi di kedua subbab. |
| 2.20.1 ("Mengapa Cross-GAN Sulit") | Nama informal | Ganti jadi "Faktor Penyebab Kesulitan Cross-GAN" atau "Tantangan Cross-GAN" |

### 2.C Tambahan konten yang diminta (P2)

- **2.2.3 Artefak Generatif** — tambah figur perbandingan artefak spasial vs frekuensi (crop wajah deepfake dengan blending boundary + magnitude FFT yang menampilkan checkerboard/spectral peak). Bisa pakai Gambar 3.4 yang sudah ada atau buat figur composite baru.
- **2.10.1 Arsitektur XceptionNet** — duplikat/pindahkan Gambar 3.6 (entry/middle/exit flow) ke sini, dengan sitasi Chollet [6].

### 2.D Format & struktur (P1, P2)

- **Audit paragraf < 5 kalimat** — gabung dengan paragraf adjacent atau perluas. Banyak paragraf di 2.5–2.8 yang pendek.
- **Anak subbab 1 paragraf → konversi ke bullet point a/b/c.** Kandidat: 2.6.1, 2.6.2, 2.7.4.
- **Format rumus** — sesuaikan pedoman TA Mikroskil (rata tengah, nomor di kanan dalam kurung, italic untuk variabel). Audit semua persamaan BAB II (DFT, magnitude, log scaling, dst).
- **Pangkas teori yang tidak dipakai metode** (kesimpulan P2: "BAB 2 dan 3 cukup tuliskan yang akan diteliti"):
  - 2.7 Periodic Noise — ringkas
  - 2.8 Warping dalam Domain Frekuensi — pertimbangkan dipangkas (tidak dipakai eksplisit)
  - 2.17.1 SGD — boleh dipangkas (dipakai AdamW)
  - 2.5.4 Pendekatan Modern — overlap dengan 2.4.4, ringkas

### 2.E Arsitektur sistem yang akan dikembangkan (P1)

P1 minta arsitektur sistem jelas di BAB II. Tambah subbab penutup BAB II (mis. 2.22 atau perluas 2.21):

- Rangkum bagaimana komponen teori (FFT, XceptionNet, SE, Late Fusion) **dirangkai** menjadi pendekatan penelitian
- Diagram blok ringkas: Frame video → [Spasial: XceptionNet] + [Frekuensi: FFT → FreqCNN] → Concat + SE Gating → Klasifikasi
- Sebut tools: Python 3.9, PyTorch, timm, OpenCV, NumPy, scikit-learn

---

## BAB III — TAHAPAN PELAKSANAAN

### 3.A Total dataset eksplisit (P2)

Tambah di subbab 3.2 (sebelum/sesudah Tabel 3.1) tabel total dataset yang dipakai (lihat tabel di bagian RL-3 di atas).

### 3.B Konsistensi BAB I ↔ BAB III (P2)

Subbab 3.4 sekarang: "Penelitian merancang dan evaluasi 3 arsitektur model" → kontradiktif dengan BAB I yang usulan 1 arsitektur hybrid.

**Reframe:**
> "Penelitian ini mengusulkan **arsitektur hybrid HybridTwoBranch** (subbab 3.4.3) sebagai kontribusi utama. Sebagai pembanding (baseline) dalam ablation study, dirancang juga model spasial-only (XceptionNet) dan frekuensi-only (FreqCNN) untuk mengukur kontribusi setiap domain terhadap performa akhir."

### 3.C Posisi Gambar 3.8 (P2)

Pindahkan Gambar 3.8 (HybridTwoBranch) dari posisi sekarang (akhir 3.4.4 setelah Tabel 3.7) ke awal subbab 3.4.3 (Model Hybrid HybridTwoBranch), tepat setelah pembukaan paragraf, sebelum 3.4.3.1 Cabang Spasial.

### 3.D Detail alur algoritma (P1)

P1: "Detail proses untuk semua algoritma tidak jelas mulai dari awal hingga akhir, apakah dipahami cara kerja algoritmanya?"

| Subbab | Sudah ada | Tambahan |
|--------|-----------|----------|
| 3.3.1 Ekstraksi Frame | Hanya narasi "pakai OpenCV" | Tambah pseudocode: open video → read FPS → compute interval = native_fps/target_fps → loop frame → save tiap interval-th frame → stop di max_frames. Jelaskan **kenapa 5 FPS dan 50 frame max**. Tambah diagram alir. |
| 3.3.2 FFT | Sudah ada DFT formula + contoh 4×4 ✓ | Tambah flowchart ringkas: Grayscale → Resize 224 → FFT2D → fftshift → magnitude → log → cache .npy |
| 3.4.1 XceptionNet | Sudah ada Gambar 3.6 ✓ | Tambah pseudocode forward pass: input (3,224,224) → entry → middle (8× block) → exit → GAP → FC |
| 3.4.2 FreqCNN | Sudah ada Gambar 3.5, 3.7 ✓ | Tambah pseudocode forward pass tabel layer-by-layer sudah ada di Tabel 3.5 ✓ |
| 3.4.3 HybridTwoBranch | Persamaan SE ada | Tambah narasi step-by-step alur SE gating (squeeze → excitation → scale) untuk pembaca non-expert |

### 3.E Analisis Sistem / Implementasi (P1)

P1: "Kenapa tidak ada analisis sistemnya? ini akan diimplementasikan pakai apa?"

Tambah subbab baru (mis. **3.8 Analisis Sistem**) berisi:

- **Bahasa**: Python 3.9
- **Framework deep learning**: PyTorch, timm (XceptionNet pretrained ImageNet)
- **Library pendukung**: OpenCV (video I/O), NumPy (FFT), scikit-learn (split), pandas (manifest)
- **Hardware**: GPU NVIDIA (CUDA, AMP/TF32 untuk Ampere+); fallback CPU untuk eksperimen kecil
- **Environment**: lihat `requirements.txt`
- **Orkestrasi pipeline**: skrip `run_pipeline.py`, `train.py`, `eval.py`, `compute_fft_cache.py`
- **Output**: checkpoint terbaik (`best.pt`) berdasarkan AUC validasi; tabel hasil (`Table1_in_dataset.csv`, `Table2_cross_dataset.csv`, `Table3_generalization_drop.csv`)

Bisa dibuat dalam bentuk diagram deployment sederhana atau use-case actor (peneliti) → sistem → output.

### 3.F Augmentasi dengan contoh visual (P2)

Subbab 3.3.3 — tambah grid figur contoh hasil augmentasi:

- **Gambar 3.x: Contoh Augmentasi Domain Spasial** — original → Resize → RandomResizedCrop → ColorJitter → HorizontalFlip → RandomErasing
- **Gambar 3.y: Contoh Augmentasi Domain Frekuensi** — original FFT → +Gaussian noise → +spectral band masking (Gambar 3.3 sudah ada untuk masking ✓)

---

## Daftar Pustaka

| # | Aksi |
|---|------|
| DP-1 | Tambah **Hu, J., Shen, L., & Sun, G. (2018). Squeeze-and-Excitation Networks. CVPR.** untuk subbab 2.11 |
| DP-2 | Pastikan **Chollet, F. (2017). Xception: Deep Learning with Depthwise Separable Convolutions. CVPR.** sudah ada (kemungkinan [6]) dan dipakai di 2.9.4 |
| DP-3 | Pastikan **Li, Y., et al. (2020). Celeb-DF.** ada (kemungkinan [35]) dan dipakai di latar belakang sebagai bukti drop cross-dataset XceptionNet |
| DP-4 | (Opsional) Goodfellow et al. textbook untuk konsep CNN/metrik dasar (2.18) |
| DP-5 | Cek format sitasi konsisten (IEEE atau APA) sesuai pedoman TA Mikroskil |

---

## Checklist Verifikasi (sebelum re-submit)

- [ ] Setiap point Rumusan Masalah punya paragraf turunan di Latar Belakang dan Tujuan padanan
- [ ] Setiap gambar/tabel BAB II ada sitasi (caption atau paragraf sekitar)
- [ ] Tidak ada paragraf < 5 kalimat di BAB II
- [ ] Anak subbab 1 paragraf sudah dikonversi ke bullet/numbering
- [ ] Format rumus konsisten dengan pedoman TA Mikroskil
- [ ] Arsitektur yang diusulkan konsisten antara BAB I dan BAB III (1 hybrid + 2 baseline ablation)
- [ ] Total dataset disebut eksplisit di BAB I (Ruang Lingkup) dan BAB III (3.2)
- [ ] Sitasi link dataset (FFPP, CDF) ada
- [ ] Subbab Analisis Sistem ada di BAB III
- [ ] Manfaat 4 (kecepatan inferensi) sudah dihapus
- [ ] Klaim "alat forensik andal/akurat" sudah dilunakkan
- [ ] Gambar 3.8 sudah pindah ke 3.4.3
- [ ] Hu et al. SE Networks sudah masuk daftar pustaka
- [ ] Re-render PDF dan baca ulang dengan checklist feedback
- [ ] Diskusi dengan dosen pembimbing sebelum submit final

---

## Prioritas Eksekusi

1. **BAB I** dulu — akar dari banyak feedback. Begitu BAB I selaras (latar belakang fokus → rumusan masalah turunan jelas → tujuan padanan), revisi BAB II/III akan mengikuti dengan lebih lurus.
2. **BAB III** kedua — konsistensi dengan BAB I (3.4 reframing), tambah analisis sistem, detail algoritma.
3. **BAB II** terakhir — tedious tapi mostly mekanis: audit sitasi, format paragraf, pangkas konten tidak relevan.

## Catatan untuk eksekusi

- **Lokasi file source dokumen tesis perlu dikonfirmasi** — PDF tidak bisa diedit langsung. Apakah source-nya DOCX, Google Docs, atau LaTeX?
- Pertimbangkan buat **dokumen response-to-reviewer** terpisah saat submit revisi — tabel: feedback → halaman lama → halaman baru → ringkasan perubahan. Memudahkan pembanding melihat di mana tiap point ditangani.
