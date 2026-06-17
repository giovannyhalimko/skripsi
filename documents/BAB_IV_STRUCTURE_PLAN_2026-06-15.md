# BAB IV — Struktur / Blueprint (Hasil dan Pembahasan)

**Tanggal:** 2026-06-15 · **diperbarui 2026-06-17** (setelah rilis demo Gradio ditarik)
**Hasil acuan (settle):** commit `d28efae` — `deepfake_hybrid/results_vast_20260609/` (3 model × 2 dataset × 4 tier n100/250/500/750 × 3 seed)
**Demo ter-deploy:** https://huggingface.co/spaces/thesissufferer/deepfake-detection-demo
**Arah judul baru (komparatif):** "Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal" / "Analisa Kontribusi Domain Frekuensi…"

> **Update 2026-06-17 — artefak rilis baru (commit `63a7896`, `a02ca82`):** demo Gradio + dokumentasi sudah masuk repo.
> - `deepfake_hybrid/demo/` — demo **perbandingan 3 model** (spatial/hybrid/freq) di HF Spaces. Bukan hybrid-saja. `app.py` (UI), `inference.py` (pipeline), `cards.py` (verdict card), `README.md` (deploy + checkpoint).
> - `deepfake_hybrid/documentation/CODE_WALKTHROUGH.md` (436 baris) — referensi implementasi/alur data (untuk 4.1.1).
> - Demo memakai checkpoint **FFPP, n750, seed 0** untuk ketiga model (tier yang sama dengan badan bab). `fft_stats.json` lokal = {mean 5,78; std 1,28}.
> - Implikasi: keputusan "demo = hybrid" **digantikan** → demo adalah **reviewer komparatif** (lihat 4.1.2 & §6 #3). Checkpoint n750 **tidak ada di repo lokal** (hanya tier lama n10/50/200/400) → relevan ke kendala ROC/CM (§6a).

---

## 0. Prinsip penyusunan (dari pedoman + konvensi paper deepfake)

1. **Pedoman Skripsi 2025:** BAB IV wajib dua bagian — **4.1 Hasil** (data objektif: tabel, gambar, angka) dan **4.2 Pembahasan** (analisis *mengapa*, **wajib menjawab tiap Rumusan Masalah**). Jangan campur data mentah dengan analisis.
2. **Tabel:** caption **di atas**, `Tabel 4.x`, Title Case. **Gambar:** caption **di bawah**, `Gambar 4.x`. Rujuk eksplisit di teks ("…ditunjukkan pada Tabel 4.1").
3. **Framing komparatif/ablation:** tiga model = ablation alami (spatial = tanpa frekuensi; freq = tanpa spasial; hybrid = keduanya). Ini menjawab RM3 secara langsung.
4. **Temuan negatif ditangani jujur** (konvensi paper: Durall, Odena, Mejri, Ma, Tan): sebut baseline apa adanya, tunjukkan ablation lengkap, jelaskan *mengapa* cabang frekuensi lemah, pisahkan rezim in-dataset vs cross-dataset.
5. **Metodologi pelaporan:** semua angka = **rata-rata ± std atas 3 seed**, frame-level, split per-video. Tier **n100 dilaporkan dengan peringatan** (test set ~15 video → noise); analisis utama bertumpu pada **n250/n500/n750**.

---

## 1. Rumusan Masalah yang harus dijawab (dari REVISI V1)

- **RM1:** Sejauh mana detektor spasial murni (XceptionNet) **menurun performanya** saat diuji lintas dataset?
- **RM2:** Sejauh mana **penambahan analisis frekuensi (FFT)** dapat **memperkecil penurunan** tersebut?
- **RM3:** Seberapa besar **kontribusi masing-masing komponen** (spasial vs frekuensi) terhadap accuracy, precision, recall, AUC pada in-dataset & cross-dataset?

> Catatan framing: dengan judul komparatif, narasi BAB IV adalah **investigasi** ("apakah & seberapa frekuensi membantu"), bukan klaim "hybrid lebih unggul". Temuan jujur: in-dataset hybrid < spatial; cross-dataset bermanfaat *parsial & bergantung arah*.

---

## 2. Ringkasan temuan kunci (data-driven, jadi tulang punggung narasi)

**A. In-dataset (RM3):** urutan konsisten **spatial > hybrid > freq** di semua tier andal & kedua dataset.
- n750: AUC CDF — spatial 0,969 / hybrid 0,924 / freq 0,586; FFPP — 0,780 / 0,650 / 0,546.
- CDF lebih mudah dari FFPP. Cabang **freq nyaris chance** (AUC 0,48–0,62).

**B. Degradasi cross-dataset model spasial (RM1):** sangat besar, **asimetris**.
- Arah **CDF→FFPP**: spatial kolaps (drop F1 +0,82 / +0,68 / +0,76 di n250/500/750).
- Arah **FFPP→CDF**: spatial turun moderat (drop F1 +0,16 / +0,07 / +0,12).
- AUC cross-dataset spatial jatuh ke 0,57–0,70.

**C. Apakah FFT memperkecil penurunan? (RM2): parsial & bergantung arah.**
- **FFPP→CDF**: drop F1 hybrid nyaris nol/negatif (−0,008 / −0,006 / +0,027) vs spatial (+0,16/+0,07/+0,12) → hybrid **menahan F1 jauh lebih baik**; F1 absolut cross kadang > spatial (n250, n500).
- **CDF→FFPP**: hybrid drop (+0,56/+0,49/+0,61) lebih kecil dari spatial (+0,82/+0,68/+0,76) tapi **tetap besar** (recall kolaps).
- **AUC cross**: hybrid ≈ spatial (n750 F→C dua-duanya 0,648; C→F spatial 0,629 > hybrid 0,563) → **bukan kemenangan bersih**.
- **Trade-off**: keuntungan generalisasi hybrid datang **dengan biaya** performa in-dataset yang lebih rendah.

**D. Caveat metrik drop:** freq punya "drop" kecil/negatif **secara trivial** karena AUC cross-nya (0,52–0,66) ≈ AUC in-dataset-nya (0,48–0,62) — ia tidak pernah benar-benar belajar fitur spesifik dataset, jadi "tidak ada yang bisa jatuh". Wajib disampaikan agar drop tidak salah tafsir.

---

## 3. STRUKTUR BAB IV (usulan — Opsi A, komparatif berbasis jenis evaluasi)

```
# BAB IV  HASIL DAN PEMBAHASAN

## 4.1 Hasil
### 4.1.1 Lingkungan dan Konfigurasi Eksperimen
### 4.1.2 Implementasi dan Purwarupa Sistem
### 4.1.3 Hasil Evaluasi In-Dataset
### 4.1.4 Hasil Evaluasi Cross-Dataset
### 4.1.5 Analisis Generalization Drop
### 4.1.6 Pengaruh Ukuran Sampel terhadap Performa (Scaling)
### 4.1.7 Dinamika Pelatihan dan Konvergensi Model

## 4.2 Pembahasan
### 4.2.1 Kontribusi Domain Spasial dan Domain Frekuensi (menjawab RM3)
### 4.2.2 Penurunan Performa Model Spasial pada Cross-Dataset (menjawab RM1)
### 4.2.3 Pengaruh Penambahan FFT terhadap Penurunan Performa (menjawab RM2)
### 4.2.4 Analisis Akar Penyebab Lemahnya Cabang Frekuensi
### 4.2.5 Keterbatasan Penelitian
### 4.2.6 Ringkasan Jawaban atas Rumusan Masalah
```

---

## 4. Rincian tiap subbab (isi · tabel/gambar · RM yang dijawab)

### 4.1 Hasil

**4.1.1 Lingkungan dan Konfigurasi Eksperimen**
- Isi: perangkat keras (GPU vast.ai/Colab), stack perangkat lunak (PyTorch/timm/dll), hyperparameter final yang **benar-benar dipakai** (AdamW lr 2e-4, wd 1e-4, label smoothing 0,05, base_channels 64, patience 12, accum 2, AMP, face-crop MTCNN margin 0,3), serta **matriks eksperimen**: 3 model × 2 dataset × 4 tier × 3 seed. Protokol evaluasi (frame-level, split per-video, mean±std, threshold 0,5 + Youden J).
- Tabel: **Tabel 4.1** Konfigurasi hyperparameter final; **Tabel 4.2** Matriks eksperimen (jumlah run).
- Catatan: ringkas — detail teknis sudah di BAB III; di sini cukup "apa yang dijalankan".
- Referensi penulisan: `documentation/CODE_WALKTHROUGH.md` (alur data end-to-end, output layout, konvensi) sebagai sumber deskripsi lingkungan/implementasi yang akurat.

**4.1.2 Implementasi dan Purwarupa Sistem** → mendukung framing komparatif & RM3
- Isi: prototipe **"Model Comparison Demo"** ter-deploy di Hugging Face Spaces (`deepfake_hybrid/demo/`, SDK Gradio). Pengguna mengunggah video wajah; sistem **menjalankan ketiga model (spatial, hybrid, freq) secara berdampingan** dan menampilkan:
  - **Verdict card per model** — badge REAL/FAKE + bar probabilitas-fake dengan ambang keputusan ditandai.
  - **Panel "what the models see"** — galeri face-crop (input RGB cabang spasial) + spektrum FFT berwarna MAGMA (input cabang freq/hybrid).
  - Alur: sampling 5 fps (≤16 frame) → MTCNN crop margin 0,3 → preprocessing identik pelatihan (RGB→224²→norm ImageNet; FFT→log-magnitude→normalisasi statistik dataset) → rata-rata probabilitas per-frame → verdict per model memakai ambang ter-tuning FFPP. Seluruh preprocessing **reuse `src/` verbatim**.
  - Checkpoint: **FFPP, n750, seed 0** untuk ketiga model (tier sama, perbandingan adil).
  - Tujuan desain: **menyurfacekan temuan utama secara interaktif** — hybrid tidak mengungguli spatial (mendukung narasi komparatif & dapat dirujuk di 4.2).
- Gambar: **Gambar 4.1** Antarmuka demo + verdict card 3 model; **Gambar 4.2** Panel "what the models see" (face-crop vs spektrum FFT).
- Catatan silang: panel spektrum FFT (Gambar 4.2) **dipakai ulang di 4.2.4** sebagai bukti kualitatif bahwa spektrum FFT wajah ter-crop nyaris tak berbeda real vs fake → menjelaskan lemahnya cabang frekuensi.
- Referensi penulisan: `deepfake_hybrid/demo/README.md`, `demo/app.py`, `documentation/CODE_WALKTHROUGH.md`.

**4.1.3 Hasil Evaluasi In-Dataset**  → **RM3**
- Isi: tabel acc/precision/recall/F1/AUC untuk **3 model × 2 dataset** pada tier representatif **n750** (mean±std). Tunjukkan urutan spatial > hybrid > freq. Sorot recall vs precision.
- Tabel: **Tabel 4.3** Performa in-dataset (n750). *(Tabel per tier n250/n500 → Lampiran.)*
- Gambar: **Gambar 4.3** `comparison_in_dataset_n750.png` (bar AUC/F1 per model–dataset).

**4.1.4 Hasil Evaluasi Cross-Dataset**  → **RM1 & RM2**
- Isi: tabel metrik untuk dua arah **FFPP→CDF** dan **CDF→FFPP**, 3 model, n750. Sorot **kolaps recall** (mis. hybrid n750 CDF→FFPP recall 0,143; spatial C→F recall rendah). Bandingkan AUC cross spatial vs hybrid vs freq.
- Tabel: **Tabel 4.4** Performa cross-dataset (n750).
- Gambar: **Gambar 4.4** `comparison_cross_dataset_n750.png`.

**4.1.5 Analisis Generalization Drop**  → **RM1 & RM2**
- Isi: tabel Δ = F1_in − F1_cross per model/arah/tier. Tunjukkan: spatial drop terbesar (terutama C→F), hybrid drop FFPP→CDF nyaris nol, freq drop trivial (caveat D).
- Tabel: **Tabel 4.5** Generalization drop (F1) seluruh model & arah, n250/500/750.
- Gambar: **Gambar 4.5** `generalization_drop_n750.png`.

**4.1.6 Pengaruh Ukuran Sampel terhadap Performa (Scaling)**  → mendukung RM3 (rezim data)
- Isi: tren AUC/F1 in-dataset & cross-dataset terhadap n (100→750). Spatial naik paling tajam; freq stagnan rendah. Beri peringatan n100 (noise).
- Gambar: **Gambar 4.6** `scaling_auc.png`, **Gambar 4.7** `scaling_auc_cross.png` (opsional + `scaling_f1*`).
- Tabel (opsional): **Tabel 4.6** ringkasan AUC per tier.

**4.1.7 Dinamika Pelatihan dan Konvergensi Model**  → mendukung 4.2.4
- Isi: kurva pelatihan menunjukkan cabang **freq tidak benar-benar belajar** (loss/AUC val stagnan) vs spatial/hybrid konvergen. Pilih beberapa kurva representatif.
- Gambar: **Gambar 4.8** `training_curves_freq_FFPP_n750.png` vs **Gambar 4.9** `training_curves_spatial_FFPP_n750.png` (atau hybrid).
- *(Opsional bila sempat dibuat: ROC curve & confusion matrix — perlu di-generate dari prediksi; lihat §6.)*

### 4.2 Pembahasan (wajib menjawab RM)

**4.2.1 Kontribusi Domain Spasial dan Domain Frekuensi (RM3)**
- Inti: spasial = penyumbang utama; frekuensi (standalone) nyaris chance → kontribusi marjinal/negatif in-dataset; hybrid mewarisi kekuatan spasial tetapi tertahan cabang frekuensi. Diskusi precision–recall.

**4.2.2 Penurunan Performa Model Spasial pada Cross-Dataset (RM1)**
- Inti: kuantifikasi degradasi (drop F1 hingga +0,76; AUC turun ke ~0,6). Jelaskan asimetri arah (CDF→FFPP jauh lebih parah karena CDF satu-metode, FFPP empat-metode). Kaitkan ke domain shift (Ma, Rössler).

**4.2.3 Pengaruh Penambahan FFT terhadap Penurunan Performa (RM2)**
- Inti: jawaban **parsial & bergantung arah** — FFT menekan drop F1 (terutama FFPP→CDF, drop ≈ 0) dan kadang menaikkan F1 absolut cross, **tetapi** tanpa keuntungan AUC konsisten dan **dengan biaya** performa in-dataset. Tegaskan caveat D (drop freq trivial).

**4.2.4 Analisis Akar Penyebab Lemahnya Cabang Frekuensi**
- Inti (root-cause, sitasi): (a) FFT pada wajah ter-crop + kompresi c23 **menghapus sidik jari upsampling GAN** (Durall, Odena, Mejri); (b) cabang near-chance **menyuntik noise** ke fusi; (c) **SE-gating gagal menekan** cabang buruk; (d) cross-dataset memang sulit (Ma, Tan). Kontras dengan SpecXNet/Qian yang butuh mekanisme frekuensi lebih canggih.
- **Bukti kualitatif:** rujuk **Gambar 4.2** (panel "what the models see" dari demo) — spektrum FFT face-crop real vs fake nyaris tak terbedakan secara visual, mendukung argumen bahwa sinyal frekuensi diskriminatif sudah hilang sebelum masuk FreqCNN.

**4.2.5 Keterbatasan Penelitian**
- Data terbatas (≤750 video/dataset), hanya c23, frame-level (tanpa temporal), dua dataset, prototipe belum dioptimasi inferensi, n100 noisy.

**4.2.6 Ringkasan Jawaban atas Rumusan Masalah**
- Tabel pemetaan **RM → temuan → bukti (tabel/gambar)** agar penguji mudah mengecek. (**Tabel 4.7**)

---

## 5. Daftar Tabel & Gambar (rancangan penomoran)

| ID | Judul | Sumber artefak |
|----|-------|----------------|
| Tabel 4.1 | Konfigurasi Hyperparameter Final | BAB III config |
| Tabel 4.2 | Matriks Eksperimen | — |
| Tabel 4.3 | Performa In-Dataset (n750) | Table1_in_dataset_summary |
| Tabel 4.4 | Performa Cross-Dataset (n750) | Table2_cross_dataset_summary |
| Tabel 4.5 | Generalization Drop F1 (n250/500/750) | Table3_drop_summary |
| Tabel 4.6 | Ringkasan AUC per Ukuran Sampel | semua tier |
| Tabel 4.7 | Ringkasan Jawaban Rumusan Masalah | — |
| Gambar 4.1 | Antarmuka Demo + Verdict Card 3 Model (HF Spaces) | screenshot `demo/app.py` |
| Gambar 4.2 | Panel "What the Models See": Face-Crop vs Spektrum FFT | screenshot demo (dipakai ulang di 4.2.4) |
| Gambar 4.3 | Perbandingan In-Dataset | comparison_in_dataset_n750.png |
| Gambar 4.4 | Perbandingan Cross-Dataset | comparison_cross_dataset_n750.png |
| Gambar 4.5 | Generalization Drop | generalization_drop_n750.png |
| Gambar 4.6 | Scaling AUC In-Dataset | scaling_auc.png |
| Gambar 4.7 | Scaling AUC Cross-Dataset | scaling_auc_cross.png |
| Gambar 4.8 | Kurva Pelatihan Cabang Frekuensi | training_curves_freq_FFPP_n750.png |
| Gambar 4.9 | Kurva Pelatihan Model Spasial | training_curves_spatial_FFPP_n750.png |
| Gambar 4.10 | Kurva ROC In-Dataset FFPP (3 model) | `make_roc_cm.py` → FFPP_in_n750_roc.png |
| Gambar 4.11 | Kurva ROC In-Dataset CDF (3 model) | CDF_in_n750_roc.png |
| Gambar 4.12 | Kurva ROC Cross-Dataset (FFPP↔CDF) | FFPP2CDF / CDF2FFPP _roc.png |
| Gambar 4.13 | Confusion Matrix per model (in-dataset n750) | `{tag}_cm_{model}.png` |
| (Lampiran) | Tabel in/cross/drop untuk n100, n250, n500 | per tier |
| (Lampiran) | Confusion matrix cross-dataset + ROC tier lain | make_roc_cm.py |

*(Tabel hasil dibuat sebagai HTML siap-paste mengikuti `skills/create-table-html.md`.)*

---

## 6. Keputusan — SUDAH DIKONFIRMASI (2026-06-15)

1. **Organisasi 4.1** → **Opsi A (per jenis evaluasi).** ✅
2. **Gaya sitasi BAB IV** → **(Nama, Tahun).** ✅ (catatan: seragamkan seluruh dokumen nanti)
3. **Model di demo (4.1.2)** → ~~Hybrid saja~~ **DIPERBARUI: demo = reviewer komparatif 3 model** (spatial/hybrid/freq berdampingan, checkpoint FFPP n750 seed0). Lebih selaras dengan judul komparatif. ✅
4. **ROC curve & confusion matrix** → **Dibuat & dimasukkan.** ✅ → lihat §6a (perlu langkah teknis).

Masih terbuka (rekomendasi default, tak menghambat): **n100** diringkas di scaling + Lampiran; **tabel utama** tampilkan n750 di badan, tier lain di Lampiran.

### 6a. ⚠️ Kendala teknis ROC/Confusion Matrix
- `scripts/run_all.py` menghitung `y_true, y_prob` **di memori** tetapi **tidak menyimpannya** (hanya menulis tabel ringkasan). Jadi **artefak prediksi untuk ROC/CM belum ada.**
- Checkpoint lokal di `outputs/runs/` berasal dari tier **berbeda** (n10/n50/n200/n400) — **bukan** matriks n100/250/500/750 hasil `d28efae`. Checkpoint vast.ai tampaknya tidak ter-commit (hanya tabel + plot).
- **Update 2026-06-17:** checkpoint n750 yang dibutuhkan **TIDAK ada di repo lokal** (cek `outputs/runs/` hanya tier lama n10/50/200/400 seed0). Namun checkpoint **FFPP n750 seed0** untuk ketiga model **pasti tersedia** di luar repo — demo HF Spaces yang berjalan memakainya (lihat `demo/README.md`, di-assemble dari mesin pelatihan vast/Colab; `*.pt` ~195 MB di-gitignore). Threshold per model (`threshold.json`) juga ada di sana.
- **Konsekuensi & jalur (terrevisi):** ROC/CM untuk hasil settle **tidak perlu re-training** asal checkpoint diambil kembali:
  - **(i, REKOMENDASI)** Ambil checkpoint **FFPP n750 seed0** (+ CDF n750 seed0 untuk arah lain) dari mesin pelatihan/HF Space → jalankan skrip inferensi atas **test split** yang **menyimpan `(y_true, y_prob)`** → generate ROC & confusion matrix. `demo/inference.py` dan `scripts/eval.py` sudah melakukan forward pass; tinggal tambah penyimpanan prediksi + plot. Biaya: hanya inferensi, bukan latih ulang.
  - **(ii)** Bila checkpoint sulit diambil: patch `run_all.py` simpan prediksi lalu re-run tier n750 saja (perlu latih ulang).
### 6b. ✅ Skrip ROC/CM sudah dibuat & diuji (`scripts/make_roc_cm.py`)
**Status:** skrip selesai dan **diuji end-to-end** (smoke test pada data dryrun + checkpoint nyata) → menghasilkan PNG ROC + confusion matrix yang valid (`outputs/roc_cm_smoke/`). **Inferensi saja, tanpa training.**

Cara kerja: muat checkpoint (arsitektur dibangun dari **config embedded** checkpoint, jadi freq/hybrid n750 base_channels=64/depth=5 cocok) → inferensi atas test split → simpan `y_true,y_prob` CSV → plot **ROC overlay multi-model** + **confusion matrix per model** + metrics JSON. Threshold CM otomatis pakai `threshold.json` di samping checkpoint (tuned di val set train — faithful ke tabel `d28efae`); fallback Youden.

> Catatan: checkpoint lama lokal (freq/hybrid n400) **gagal load** karena arsitektur FreqCNN usang (conv-stack lama vs FreqBlock residual sekarang). Checkpoint **n750** dilatih dengan kode sekarang → akan load normal. Pastikan `fft_stats.json` ada di `fft_cache/{FFPP,CDF}/` agar normalisasi freq/hybrid benar.

**Perintah final — jalankan di mesin vast/Colab (yang punya `outputs/runs/*_n750_seed0/best.pt` + `manifests/` + `fft_cache/`):**

```bash
# 1. In-dataset FFPP
python scripts/make_roc_cm.py \
  --models spatial:outputs/runs/spatial_FFPP_n750_seed0/best.pt \
           hybrid:outputs/runs/hybrid_FFPP_n750_seed0/best.pt \
           freq:outputs/runs/freq_FFPP_n750_seed0/best.pt \
  --test-manifest outputs/manifests/FFPP/test.csv --fft-cache-root outputs/fft_cache/FFPP \
  --tag FFPP_in_n750 --title "Kurva ROC In-Dataset FFPP (n=750)"

# 2. In-dataset CDF
python scripts/make_roc_cm.py \
  --models spatial:outputs/runs/spatial_CDF_n750_seed0/best.pt \
           hybrid:outputs/runs/hybrid_CDF_n750_seed0/best.pt \
           freq:outputs/runs/freq_CDF_n750_seed0/best.pt \
  --test-manifest outputs/manifests/CDF/test.csv --fft-cache-root outputs/fft_cache/CDF \
  --tag CDF_in_n750 --title "Kurva ROC In-Dataset CDF (n=750)"

# 3. Cross-dataset FFPP->CDF (model latih FFPP, uji CDF)
python scripts/make_roc_cm.py \
  --models spatial:outputs/runs/spatial_FFPP_n750_seed0/best.pt \
           hybrid:outputs/runs/hybrid_FFPP_n750_seed0/best.pt \
           freq:outputs/runs/freq_FFPP_n750_seed0/best.pt \
  --test-manifest outputs/manifests/CDF/test.csv --fft-cache-root outputs/fft_cache/CDF \
  --tag FFPP2CDF_n750 --title "Kurva ROC Cross-Dataset FFPP->CDF (n=750)"

# 4. Cross-dataset CDF->FFPP
python scripts/make_roc_cm.py \
  --models spatial:outputs/runs/spatial_CDF_n750_seed0/best.pt \
           hybrid:outputs/runs/hybrid_CDF_n750_seed0/best.pt \
           freq:outputs/runs/freq_CDF_n750_seed0/best.pt \
  --test-manifest outputs/manifests/FFPP/test.csv --fft-cache-root outputs/fft_cache/FFPP \
  --tag CDF2FFPP_n750 --title "Kurva ROC Cross-Dataset CDF->FFPP (n=750)"
```

**Output (per perintah):** `{tag}_roc.png` (overlay 3 model), `{tag}_cm_{model}.png` (×3), `{tag}_preds_{model}.csv`, `{tag}_metrics.json` di `outputs/roc_cm/`. → masuk **Gambar 4.x** di 4.1.3 (ROC in-dataset), 4.1.4 (ROC cross-dataset), dan confusion matrix di 4.1 yang relevan.

---

## 7. Konsekuensi ke bab lain (agar konsisten)
- **Judul, Rumusan Masalah, Tujuan** sudah komparatif/ablation → cocok dengan BAB IV ini. Pastikan Abstrak & BAB I/V mengikuti narasi temuan negatif jujur.
- **BAB V (Kesimpulan)** nanti: jawab RM secara ringkas + saran (perbaiki cabang frekuensi: representasi frekuensi yang tidak terhapus crop/kompresi, gating teregularisasi, pretrain cabang freq).
