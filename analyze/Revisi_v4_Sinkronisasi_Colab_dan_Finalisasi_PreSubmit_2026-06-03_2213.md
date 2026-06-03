# Revisi v4 — Sinkronisasi Colab↔Tesis & Finalisasi Pra-Submit (BAB I–III)

**Tanggal:** 2026-06-03 22:13
**Dokumen sasaran:** `.docx` OneDrive — *Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi*
**Sumber kebenaran:** kode `deepfake_hybrid/` (`config.yaml`, `src/`, `scripts/`) **dan** `deepfake_hybrid/colab_run.ipynb` (notebook yang benar-benar menghasilkan BAB IV)
**Dasar analisis:** `analyze/Deep_Analysis_PDF_vs_Code_PreSubmit_2026-06-03.md` + `analyze/Deep_Analysis_BAB1-3_ColabCrossCheck_2026-06-03.md`
**Cara pakai:** dokumen ini berisi instruksi *manual edit*. Setiap tindakan memuat **(a) lokasi persis** (teks-jangkar untuk dicari di Word), **(b) apa yang diubah/ditambah/dihapus**, dan **(c) teks final / nilai final** yang bisa langsung dipakai.

> **Konteks status:** Submission = **PROPOSAL (BAB I–III)**. BAB IV/V kosong = wajar, **bukan** blocker. Abstrak tetap perlu ditulis. Metodologi (BAB III) sudah sangat selaras dengan `config.yaml` — yang tersisa adalah **pekerjaan finishing**: menyelaraskan empat knob runtime yang di-*override* notebook, memperbaiki kontradiksi internal, dan polishing. **Tidak ada yang butuh sains baru.**

---

## ⚙️ KEPUTUSAN ARAH (dari penulis, 2026-06-03) — BACA DULU

Notebook `colab_run.ipynb` memuat `config.yaml` sebagai basis lalu **meng-*override* 4 knob runtime**. Setiap tempat tesis mengutip nilai config, ia kini bertentangan dengan run yang akan mengisi BAB IV. Arah penyelesaian sudah diputuskan:

| # | Knob | Tesis/`config.yaml` | Colab jalankan | **Keputusan** |
|---|---|---|---|---|
| 1 | **Seeds** | 3 seed (0,1,2); "72 run"; mean±std | `N_SEEDS = 1` | ⏸️ **Biarkan `1` untuk sekarang** (run final BAB IV → naikkan ke 3). Tesis tetap "3 seed" (rencana). (lihat **N1**) |
| 2 | **Frame/video** | maks **50** | `MAX_FRAMES = 100` | ✏️ **Edit TESIS** → **100** frame; pertahankan run 100. (lihat **A3**) |
| 3 | **Tier sampel FFPP** | [100,300,600,1000] | [100,250,500,750] | ✏️ **Edit TESIS** → `[100,250,500,750]`. (lihat **A1**) |
| 4 | **Batch size** | 16 (efektif 32) | 64 (efektif 128, T4) | ✏️ **Edit TESIS** → 64/efektif 128. (lihat **A2**) |

> **Alasan:** ini proposal — "3 seed" adalah *rencana* dan BAB IV masih kosong, jadi tidak ada yang bertentangan; mempertahankannya jauh lebih kuat secara metodologi (re-run final akan memakai 3 seed). **Frame/video: penulis memilih mengunci hasil run yang sudah ada (100 frame) → tesis diubah ke "100"** (lihat A3). Tier FFPP & batch size juga lebih murah diedit di tesis.
>
> **⚠️ Catatan run:** untuk **proposal sekarang**, `N_SEEDS` **dibiarkan `1`** dan `MAX_FRAMES` **dibiarkan `100`** → **tidak ada edit notebook yang wajib sekarang** (komentar kosmetik N2 sudah dikerjakan). Klaim "3 seed" tetap di tesis sebagai rencana. Kenaikan ke `N_SEEDS=3` ditunda sampai run **final** BAB IV (lihat **N1**); frame/video sepenuhnya jadi edit tesis (**A3**).
>
> **Face crop:** review pertama SALAH menyebut face-crop "opsional/off". Colab pakai `FACE_CROP = True`, jadi **§3.3.2 sudah benar** — yang salah hanya *flowchart* Gambar 3.1 (lihat **B4**).

---

## Daftar Tindakan (ringkasan)

| # | Tindakan | Lokasi | Jenis | Prioritas |
|---|---|---|---|---|
| **N1** | Biarkan `N_SEEDS = 1` **untuk sekarang** (→ 3 hanya di run final BAB IV) | `colab_run.ipynb` (code-01) | NOTEBOOK | ⏸️ ditunda |
| **N2** | Komentar basi `patience=10` **dihapus** | `colab_run.ipynb` (code-01) | NOTEBOOK | ✅ selesai |
| **A1** | Tier sampel FFPP → **[100,250,500,750]** | Tabel 3.3 / 3.11 / 3.12, (soften 1.1/3.1, §3.3.1) | DOCX | 🔴 P1 |
| **A2** | Batch size → **64 (efektif 128)** | §3.5.5, Tabel 3.10, §3.8.3 | DOCX | 🟠 P1 |
| **A3** | Frame/video **50 → 100** + total frame ~50.000→**~100.000** / ~37.500→**~75.000** | Gambar 3.1 & 3.3, §3.2.4, §3.3.1, Tabel 3.1 (+ config.yaml) | DOCX | 🔴 P1 |
| **B1** | Tabel 3.10 label smoothing **0,0 → 0,05 (aktif)** + benahi §3.5.4 | Tabel 3.10, §3.5.4 | DOCX | 🔴 P1 |
| **B2** | Regenerasi **Gambar 3.8** (FreqCNN base=64) | Gambar 3.8 | GAMBAR | 🔴 P1 |
| **B3** | Regenerasi **Gambar 3.10** (Hybrid: 512-d, Proj 512→256, Dropout 0,5, "RGB") | Gambar 3.10 | GAMBAR | 🔴 P1 |
| **B4** | **Gambar 3.1**: tambah kotak deteksi+crop wajah; band-mask **0,15 → 0,05** | Gambar 3.1 | GAMBAR | 🟠 P1 |
| **B5** | **Refresh nomor sitasi BAB II** (esp. hlm. 12) | BAB II | DOCX | 🔴 P1 |
| **C1** | Hapus/lunakkan klaim early-fusion **"dievaluasi"** | BAB II §2.3.4 | DOCX | 🟠 P2 |
| **C2** | Lunakkan klaim empiris forward-reference | §3.3.2, §3.4.1, Tabel 2.9 | DOCX | 🟠 P2 |
| **C3** | Perbaiki rujukan tabel salah-satu | §3.4.4, §3.6.4 | DOCX | 🟠 P2 |
| **D1** | Eq (3.9): label F(1,0)→**F(1,1)**; header /2 → **/4** | §3.3.2.4 (contoh FFT) | DOCX | 🟠 P2 |
| **D2** | Eq (3.17): "3×10" → **"3×0"** | §contoh depthwise-separable | DOCX | 🟠 P2 |
| **D3** | "Alam **el at.**" → **"Alam et al."** | BAB I hlm. 2 | DOCX | 🟢 P2 |
| **E1** | Tambah sitasi sumber **Gambar 2.1** (Lena) | BAB II hlm. 16 | DOCX | 🟠 P2 |
| **E2** | Tambah sitasi **Tabel 2.1** + perbaiki typo | BAB II hlm. 13 | DOCX | 🟠 P2 |
| **E3** | Tambah sitasi **Goodfellow et al. 2014** (GAN) | §2.2 + Daftar Pustaka | DOCX | 🟠 P2 |
| **E4** | *Pass* format IEEE Daftar Pustaka | Daftar Pustaka | DOCX | 🟠 P2 |
| **F1** | Tahun sampul **2025 → 2026** | Halaman sampul | DOCX | 🟢 P3 |
| **F2** | Tulis **Abstrak** (ID + EN) | Abstrak | DOCX | 🔴 P1 |
| **F3** | Update `CLAUDE.md` (AdamW / 0,05 / patience 12 / FreqCNN base 64) | repo | KODE | 🟢 P3 |
| **F4** | Catatan kaki **Gambar 3.7** (299→224) | Gambar 3.7 | DOCX | 🟢 P3 |

---

# 🟢 BAGIAN N — Edit NOTEBOOK (`colab_run.ipynb`), BUKAN docx

> **Tidak ada edit notebook yang wajib sekarang.** N2 (komentar kosmetik) **sudah dikerjakan**; **`N_SEEDS` dibiarkan `1`** (lihat N1, ditunda) dan **`MAX_FRAMES` dibiarkan `100`** (frame/video dikunci ke run yang sudah ada; tesis yang menyesuaikan — lihat A3).

### N1 — Seeds: biarkan `N_SEEDS = 1` UNTUK SEKARANG (naikkan ke 3 saat run final) ⏸️

**Keputusan penulis (2026-06-03):** **biarkan `N_SEEDS = 1`** di `colab_run.ipynb` untuk sekarang — **tidak ada edit notebook sekarang.** Klaim "3 seed" di tesis tetap dipertahankan sebagai **rencana** (proposal; BAB IV kosong, jadi belum ada yang bertentangan).

> `N_SEEDS       = 1      # increase to 3 for statistical validity   ← biarkan 1 untuk sekarang`

**Yang HARUS diingat — kapan harus jadi 3:** saat menjalankan run **final** yang mengisi BAB IV, set `N_SEEDS = 3`. Alasannya: tesis menyatakan "tiga seed (0,1,2)", "72 run", "rata-rata dan simpangan baku" (§3.6.1, Tabel 3.10/3.11/3.12, §3.8.3). Kode `run_all.py`: `seeds = range(n_seeds)` → dengan `n_seeds=1` hanya seed [0], dan tabel *summary* mean±std (`Table1_in_dataset_summary.csv`, `Table2_cross_dataset_summary.csv`) **hanya dibuat jika `len(seeds) > 1`** → tak ada error bar.

> **⚠️ Konsekuensi jika tetap 1 seed sampai sidang akhir:** BAB IV tidak akan punya mean±std / 72 run. Untuk **proposal sekarang** ini tidak masalah (BAB IV kosong, "3 seed" = rencana). Tetapi sebelum tesis **final**, salah satu harus terjadi: **(a)** run final dengan `N_SEEDS=3`, **atau (b)** turunkan klaim tesis ke 1 seed (hapus "72 run / simpangan baku / 3 seed" dari §3.6.1, Tabel 3.10/3.11/3.12, §3.8.3). Untuk proposal, biarkan apa adanya.

### N2 — Komentar basi `patience=10` ✅ SUDAH DIKERJAKAN

Komentar `# max epochs — early stopping (patience=10) ...` pada baris `EPOCHS` di cell `code-01` **sudah dihapus** (2026-06-03) — kini barisnya hanya `EPOCHS        = 30`. Komentar ini hanya teks (nilai aktual `patience` tetap 12 dari config), jadi penghapusannya tidak memengaruhi training. **Tidak perlu tindakan tim.**

---

# 🔴 BAGIAN A — Sinkronisasi nilai run ke docx (Colab → Tesis)

### A1 — Tier sampel FFPP → [100, 250, 500, 750] 🔴

**Mengapa:** Notebook menjalankan `FFPP_SAMPLES_LIST = [100, 250, 500, 750]`, bukan `[100,300,600,1000]`. Baris/plot FFPP di BAB IV akan di 100/250/500/750. Pilih tier = sama dengan CDF (simetris & bersih). "Total 72 run" **tetap** (3×2×4×3=72) karena jumlah tier tetap 4.

**Edit bedah (4 titik):**

1. **Tabel 3.3 (hlm. 71):** baris FFPP
   > `FaceForensics++ (FFPP) | 100, 300, 600, 1000`
   ➡️ **UBAH** → `FaceForensics++ (FFPP) | 100, 250, 500, 750`

2. **Tabel 3.11 (hlm. 100):** baris ukuran sampel FFPP
   > `Ukuran sampel FFPP | 100, 300, 600, 1000 | 4`
   ➡️ **UBAH** → `Ukuran sampel FFPP | 100, 250, 500, 750 | 4`

3. **Tabel 3.12 (hlm. 101):** baris ukuran sampel (variabel kontrol)
   > `Ukuran sampel | 100–1000 (bervariasi per dataset)`
   ➡️ **UBAH** → `Ukuran sampel | 100–750`

4. **Tabel 1.1 (hlm. 5) / Tabel 3.1 (hlm. 70):** **PERTAHANKAN** *pool* FFPP n=1000 (500 real + 500 fake) — *pool*-nya memang 1000; eksperimen hanya men-*sample* subset s/d 750.
   - *(Opsional, disarankan)* tambah keterangan singkat: *"eksperimen menggunakan subset hingga 750 video"*.
   - **§3.3.1 total frame:** kalimat aritmetika *"Batas 50 frame/video … ~50.000"* **diubah di A3** (frame/video kini 100 → total ~100.000). Lihat **A3**.

### A2 — Batch size → 64 (efektif 128) 🟠

**Mengapa:** Notebook (cell `code-02`) auto-tune per GPU: **T4/V100 → `BATCH_SIZE = 64`** (A100 → 128, GPU kecil → 32), ditulis ke `colab_config.yaml`. Dengan `accum_steps=2`, **batch efektif = 128** (bukan 32). Tabel HW (Tabel 3.15) menyebut Tesla T4 → kanonkan ke nilai T4.

**Edit bedah (3 titik):**

1. **§3.5.5 (hlm. 97):**
   > *"...ukuran batch per langkah sebesar **16**, ukuran batch efektif menjadi 16 × 2 = **32**..."*
   ➡️ **UBAH MENJADI:**
   > *"...ukuran batch per langkah disesuaikan dengan kapasitas VRAM GPU (Tesla T4: **64**), dengan gradient accumulation 2 langkah sehingga ukuran batch efektif menjadi 64 × 2 = **128**."*

2. **Tabel 3.10 (hlm. 99):**
   > `Batch size | 16 | Per langkah; efektif 32` ➡️ `Batch size | 64 (T4) | Per langkah; efektif 128`
   > `Gradient accumulation | 2 langkah | ...batch efektif 32` ➡️ `...batch efektif 128`

3. **§3.8.3 (hlm. 104):**
   > *"...batch size **16** dengan gradient accumulation 2 langkah (batch efektif **32**)..."*
   ➡️ **UBAH MENJADI:**
   > *"...batch size **64** (disesuaikan VRAM Tesla T4) dengan gradient accumulation 2 langkah (batch efektif **128**)..."*

> **Catatan:** karena auto-tune bergantung GPU, sebaiknya nyatakan GPU kanonik (T4). Boleh tambah 1 kalimat: *"ukuran batch disesuaikan VRAM (T4: 64; A100: 128)."* `config.yaml` boleh dibiarkan `batch_size: 16` (notebook tetap meng-*override*).

### A3 — Frame per video: 50 → 100 🔴

**Keputusan penulis (2026-06-03):** kunci hasil run yang sudah ada (`MAX_FRAMES=100`) → **tesis diubah ke "100 frame/video"** (notebook **tidak** diturunkan ke 50). Re-run final untuk 3 seed tetap memakai `MAX_FRAMES=100`.

**Mengapa:** Notebook menulis `MAX_FRAMES=100` ke `colab_config.yaml` **dan** mengoper `--max-frames 100` ke setiap `run_pipeline.py`. Tesis menulis "maks 50" di banyak tempat → harus diselaraskan ke 100 agar deskripsi metodologi sesuai run yang menghasilkan BAB IV.

**Edit bedah (6 titik) — ganti setiap "50" → "100":**

1. **Gambar 3.1 (flowchart):** kotak ekstraksi frame *"maks **50** frame/video"* ➡️ *"maks **100** frame/video"*. *(Catatan: kotak ini juga disentuh B4 — tambah kotak crop wajah; lakukan sekaligus.)*

2. **Gambar 3.3 (pseudocode ekstraksi frame):** baris `max_frame = 50` ➡️ `max_frame = 100`.

3. **§3.2.4:** *"...diekstraksi maksimum **50** frame..."* ➡️ *"...maksimum **100** frame..."*

4. **§3.3.1 (2 tempat):**
   - *"...hingga maksimum **50** frame per video..."* ➡️ *"...maksimum **100** frame per video..."*
   - aritmetika total frame: *"Batas **50** frame/video membatasi total frame FFPP n=1000 ~ **50.000**"* ➡️ *"Batas **100** frame/video membatasi total frame FFPP n=1000 hingga ~**100.000**"*

5. **Tabel 3.1 (hlm. 70):** sel *"5 fps, max **50** frame/video"* ➡️ *"5 fps, max **100** frame/video"*; **dan** kolom total frame: FFPP *~**50.000*** ➡️ *~**100.000***, CDF *~**37.500*** ➡️ *~**75.000***.

6. **Tabel 1.1 (hlm. 5):** jika memuat total frame, samakan: FFPP *~**50.000*** ➡️ *~**100.000***, CDF *~**37.500*** ➡️ *~**75.000***.

> **⚠️ Angka total frame adalah BATAS ATAS, bukan pasti.** "~100.000" = 1000 video × cap 100. Tetapi pada 5 fps, video pendek (≲20 dtk) menghasilkan <100 frame, jadi cap 100 tidak selalu terpenuhi → total aktual bisa **< 2×** dari versi 50-frame. **Paling akurat:** ambil jumlah frame **aktual** dari manifes run (`outputs/manifests/*.csv` atau hitung baris frame) dan tulis angka riil itu. Bila ingin tetap memakai estimasi, frasa "**hingga** ~100.000" (batas atas) lebih aman daripada menyatakannya sebagai jumlah pasti.

> **Konsistensi kode (disarankan):** ubah juga `config.yaml: max_frames_per_video: 50` → **100** agar `config.yaml` ↔ tesis tidak menimbulkan drift baru. (Tidak memengaruhi run — notebook tetap meng-*override* — tetapi reviewer yang membuka `config.yaml` akan melihat angka yang konsisten.) Sertakan ini saat update **CLAUDE.md** (F3).

---

# 🔴 BAGIAN B — Kontradiksi internal (WAJIB — paling mudah ketahuan reviewer)

### B1 — Tabel 3.10: label smoothing "0,0 (nonaktif)" → "0,05 (aktif)" + benahi §3.5.4 🔴

**Masalah:** Tabel 3.10 (hlm. 99) berisi:
> `Label smoothing | 0,0 (nonaktif) | Dinonaktifkan untuk dataset kecil`

Ini bertentangan dengan §3.5.4 ("α=0,05 *diaktifkan*"), §3.8.3 ("label smoothing 0,05"), contoh perhitungan (Eq 3.33 pakai 0,05), `config.yaml` (0.05), **dan** run Colab (0.05).

**Edit 1 — sel Tabel 3.10:**
> ➡️ **UBAH** → `Label smoothing | 0,05 (aktif) | Regularisasi ringan; mencegah overconfidence pada dataset kecil`

**Edit 2 — §3.5.4 kalimat yang saling bertentangan:** paragraf mengaktifkan smoothing 0,05 "untuk mencegah overconfidence pada dataset kecil", lalu kalimat berikutnya berbunyi:
> *"Pada dataset berukuran kecil, sinyal positif yang terbatas menjadi semakin lemah apabila label di-smooth, sehingga model kesulitan membedakan kelas."*

➡️ **HAPUS / GANTI** kalimat kontradiktif itu. Pilih **satu sikap** (aktif di 0,05). Saran teks pengganti:
> *"Label smoothing diterapkan dengan α=0,05 sebagai regularisasi ringan. Nilai kecil ini menggeser target dari {0, 1} menjadi {0,025, 0,975}, cukup untuk meredam overconfidence pada dataset berukuran kecil tanpa mengaburkan batas antar-kelas."*

### B2 — Regenerasi Gambar 3.8 (FreqCNN) — diagram BASI base=32 🔴

**Masalah (hlm. 86):** diagram menampilkan arsitektur **lama base=32**:
- Kanal: `1 → 32 → 64 → 128 → 256 → 256`
- FC: `256 → 128 → 1`
- Kotak "GAP 256→1" (salah label).

Padahal **Tabel 3.6 (halaman berikutnya) + teks body + kode** memakai **base=64**.

**Spesifikasi diagram BARU (base=64) — untuk tim yang regenerasi gambar:**
- Input: `1 kanal (FFT log-magnitude 224×224)`
- FreqBlock progresif: `1 → 64 → 128 → 256 → 512 → 512` (5 blok, depth=5)
- Tiap FreqBlock: Conv 3×3 → BatchNorm → ReLU → MaxPool (+ Dropout2d 0,2)
- Setelah blok terakhir: **Global Average Pooling → vektor 512-d** (bukan "256→1")
- FC head: `Linear(512 → 256) → ReLU → Dropout(0,3) → Linear(256 → 1)`
- Total parameter ≈ **4,2 juta**

> Pastikan label kotak GAP berbunyi **"GAP → 512-d"**, bukan "256→1".

### B3 — Regenerasi Gambar 3.10 (Hybrid) — diagram BASI (4 kesalahan) 🔴

**Masalah (hlm. 89):** diagram menampilkan nilai lama:
1. Cabang FreqCNN dilabel **"256-d"** → seharusnya **"512-d"** (base=64; §3.4.3 butir 2 "vektor fitur berdimensi 512").
2. Kotak proyeksi **"Proj 256→256"** → seharusnya **"Proj 512→256"**.
3. **"ClassifierDrop(0.3)"** → seharusnya **Dropout(0,5)** ×2 (§3.4.3 + `hybrid_fusion.py`).
4. Typo **"RG Input"** → **"RGB Input"**.

**Spesifikasi diagram BARU — untuk tim yang regenerasi gambar:**
- Cabang spasial: `RGB Input (224×224×3) → XceptionNet → fitur 2048-d → Proj 2048→256`
- Cabang frekuensi: `FFT Input (224×224×1) → FreqCNN → fitur 512-d → Proj 512→256`
- Fusi: `concat → 512-d → SE-gating (reduction 4: 512→128→512)`
- Classifier head: `Dropout(0,5) → Linear(512→128) → ReLU → Dropout(0,5) → Linear(128→1)`

### B4 — Gambar 3.1 (flowchart): tambah kotak deteksi+crop wajah; band-mask 0,15 → 0,05 🟠

**Masalah:** Flowchart langsung *Ekstraksi Frame → Konversi Grayscale/FFT* — **tanpa** kotak deteksi/crop wajah, padahal run nyata pakai `FACE_CROP=True` (MTCNN, margin 0,3) dan §3.3.2 mendeskripsikannya sebagai wajib. Selain itu kotak augmentasi berbunyi "Bn. Mask **p=0,15**" — seharusnya **0,05** (band-mask 5%; nilai 0,15 kemungkinan tercampur dengan high-pass β=0,15 / RandomErasing 0,15).

**Edit 1 — sisipkan kotak baru** antara "Ekstraksi Frame" dan "Konversi FFT/Grayscale". Flowchart final:

```
Dataset Video (FFPP, CDF)
        ↓
Ekstraksi Frame (5 FPS, maks 100 frame/video)   ← angka 50→100 per A3
        ↓
Deteksi & Crop Wajah (MTCNN, margin 30%)        ← TAMBAH
        ↓
Konversi FFT (Grayscale → FFT 2D → fftshift → |F| → high-pass → log1p)
        ↓
Pembagian Dataset (Train 70% / Val 15% / Test 15%, stratified by video)
        ↓
Pelatihan Model (Spatial / Freq / Hybrid) → Validasi → Checkpoint Terbaik (AUC)
        ↓
Evaluasi (In-dataset + Cross-dataset) → Tabel Hasil → Analisis
```

> Dua perubahan pada Gambar 3.1: **(1)** tambah kotak **"Deteksi & Crop Wajah (MTCNN, margin 30%)"** (B4); **(2)** angka frame **50 → 100** (A3). Jika redaksi kotak di `.docx` berbeda, pertahankan redaksi aslinya — hanya sisipkan kotak crop & ganti angka frame.

**Edit 2 — kotak augmentasi:** `Bn. Mask p=0,15` ➡️ `Bn. Mask p=0,05`.

### B5 — Refresh nomor sitasi BAB II (esp. hlm. 12) 🔴

**Masalah:** BAB I & BAB III menyitasi **benar**; **BAB II bergeser** (field sitasi native Word menyimpan nomor lama/basi). Penomoran kanonik (dari BAB I/III ↔ Daftar Pustaka):
`[8]`Durall, `[9]`Zhang, `[10]`Giudice, `[11]`Qian, `[12]`Tan, `[13]`Alam/SpecXNet, `[14]`Rana, `[15]`Rao&Uehara, `[16]`Hasanaath/FSBI, `[17]`Luo&Wang, `[18]`Li/Celeb-DF.

**Ketidakcocokan terkonfirmasi di §2.3.2 (hlm. 12):**

| In-text (BAB II hlm. 12) | Tampil | Seharusnya |
|---|---|---|
| Durall et al. | [7] | **[8]** |
| Zhang et al. | [8] | **[9]** |
| Qian "Thinking in Frequency" | [14] | **[11]** |
| Hasanaath FSBI | [17] | **[16]** |
| Tan FSDL | [18] | **[12]** |
| Luo & Wang | [19] | **[17]** |

Juga **§2.4.3 (hlm. 18)** tidak konsisten ("Tan et al. … [17, 23]").

**Cara perbaiki (di Word) — sama seperti TEMUAN 0 di Revisi v3:**
1. **Ctrl+A → F9** (refresh semua field). Jika nomor in-text **tidak bergerak**:
2. **References → Citations & Bibliography → Style:** ganti ke **APA**, tunggu, ganti **kembali ke IEEE** → memaksa Word me-*renumber* semua sitasi in-text.
3. **Verifikasi satu per satu** blok domain-frekuensi di hlm. 12 terhadap Daftar Pustaka: klik sitasi Durall → harus **[8]**, Zhang → **[9]**, Qian → **[11]**.

> Jika sebagian field bandel/ter-*unlink*: klik field salah → dropdown → **Update Field** per-citation. Bila masih gagal total, kirim `.docx` terbaru untuk dipetakan field demi field.

---

# 🟠 BAGIAN C — Klaim & ruang lingkup

### C1 — Hapus/lunakkan klaim early-fusion "dievaluasi" (BAB II §2.3.4, hlm. 15) 🟠

**CARI:**
> *"...kedua strategi fusion diimplementasikan dan **dievaluasi**: early fusion melalui XceptionNet 4-kanal, serta late fusion..."*

**Masalah:** BAB III §3.4 + Tabel 3.11 hanya membangun **spatial / freq / hybrid (late fusion)**. `EarlyFusionXception` ada di kode tetapi **tidak** masuk matriks `run_all.py` maupun matriks Colab.

**UBAH MENJADI** (salah satu):
> *"...early fusion (XceptionNet 4-kanal) **diimplementasikan namun tidak menjadi fokus evaluasi**; penelitian ini berfokus pada late fusion dua cabang."*

### C2 — Lunakkan klaim empiris forward-reference (sebelum BAB IV ada) 🟠

Beberapa klaim empiris dinyatakan sebagai fakta padahal BAB IV (hasil) belum ada:

1. **§3.3.2** — *"Secara empiris, penerapan face cropping meningkatkan performa model spasial secara **substansial** pada FaceForensics++."*
   - Colab hanya run dengan crop **ON** (tidak ada baseline OFF) → tak ada A/B untuk "substansial".
   - ➡️ **UBAH** → sandarkan ke rasional literatur: *"Latar belakang umumnya tidak mengandung informasi diskriminatif dan berperan sebagai noise (Afchar et al., 2018; Rössler et al., 2019), sehingga pembatasan analisis pada region wajah **diharapkan** meningkatkan fokus model."*

2. **§3.4.1** — klaim *"akurasi 96–99%"* → ➡️ reword sebagai target/ekspektasi atau atribusikan ke literatur (Rössler).

3. **Tabel 2.9** — menyajikan hybrid *"98–99% / generalisasi sangat baik"* sebagai fakta. Ini sedikit melemahkan *gap* yang justru ingin diisi tesis. ➡️ **Lunakkan** menjadi rentang dari literatur/ekspektasi, bukan klaim hasil sendiri.

### C3 — Perbaiki rujukan tabel salah-satu 🟠

1. **§3.4.4:** *"Tabel **3.6** merangkum perbedaan ... antara ketiga arsitektur ... Tabel **3.7** merinci dimensi fitur."*
   - Tabel 3.6 = tabel layer FreqCNN. Perbandingan 3-arsitektur = **Tabel 3.7**; dimensi per-komponen = **Tabel 3.8**.
   - ➡️ **UBAH** → *"Tabel **3.7** ... Tabel **3.8** ..."*

2. **§3.6.4:** *"Tabel **3.11** merangkum seluruh variabel..."*
   - Tabel variabel = **Tabel 3.12** (3.11 = matriks eksperimen).
   - ➡️ **UBAH** → *"Tabel **3.12** ..."*

---

# 🟠 BAGIAN D — Math & typo pada contoh perhitungan

### D1 — Eq (3.9): label F(1,0) → F(1,1); header eksponen /2 → /4 🟠

**Lokasi:** contoh perhitungan FFT 4×4 (§3.3.2.4, sekitar hlm. 77).
- Persamaan dilabeli **"F(1,0)"** padahal heading & hasil untuk **F(1,1)** (heading "Menghitung F(1,1)", pakai (x+y)/4, hasil 0).
- Header kolom tabel tertulis `e^{−j·2π((x+y)/2)}` padahal nilai memakai **/4**.

➡️ **UBAH:** label `F(1,0)` → **`F(1,1)`**; header `/2` → **`/4`**. (Angka-angkanya sudah benar: F(1,1)=0.)

### D2 — Eq (3.17): "3×10" → "3×0" 🟠

**Lokasi:** contoh depthwise-separable (sekitar hlm. 85).
**CARI:**
> *"2×0 + 0×1 + 1×1 + **3×10** = 1"*

➡️ **UBAH** "3×10" → **"3×0"** (agar jumlah = 1, sesuai Y₂; "3×10" membuat total 31). Kemungkinan typo/OCR.

### D3 — "Alam el at." → "Alam et al." (BAB I hlm. 2) 🟢

**CARI:** *"Alam **el at.**"* ➡️ **UBAH** → *"Alam **et al.**"*

---

# 🟠 BAGIAN E — Sitasi & referensi (polish — sesuai permintaan Pembanding 1)

### E1 — Gambar 2.1 (Lena, hlm. 16) tanpa sitasi 🟠
Gambar komponen frekuensi (panel (a)/(b)/(c)/(d)) jelas bersumber. Gambar 2.2 `[30]` & 2.3 `[6]` sudah bersitasi. ➡️ **Tambah sumber** pada caption Gambar 2.1.

### E2 — Tabel 2.1 (hlm. 13) tanpa sitasi + typo 🟠
- Typo: *"**e**latif stabil"* → *"**R**elatif stabil"*; ada **"R"** nyasar di *"kompresi tinggi **R**"*.
- ➡️ Tambah sitasi sumber, atau *"(disusun penulis)"* bila sintesis sendiri.
- *(Tabel 2.4 & 2.5 juga uncited — beri "(disusun penulis)" bila milik sendiri.)*

### E3 — Tambah sitasi seminal GAN — Goodfellow et al. 2014 🟠
**CARI:** §2.2 *"GAN ... diperkenalkan pada tahun 2014"* — saat ini menyitasi review `[15, 20]`, bukan paper asli.
➡️ **Tambah** entri Daftar Pustaka + sitasi in-text:
> I. J. Goodfellow et al., "Generative Adversarial Nets," in *Advances in Neural Information Processing Systems (NeurIPS)*, 2014, hlm. 2672–2680.

### E4 — Pass format IEEE Daftar Pustaka 🟠
Format tidak seragam. Contoh masalah: `[1]` nama penulis kacau ("K. P. dan M. S."), `[10]` Giudice, `[13]` SpecXNet, `[33]` LeCun kekurangan tahun/venue; beberapa entri tanpa publisher/halaman.
➡️ **Pass format** menyeluruh sesuai pedoman TA. **Verifikasi** ke-45 referensi benar-benar disitasi in-text (sweep), tidak ada entri yatim/duplikat setelah refresh field.

---

# 🟢 BAGIAN F — Housekeeping

### F1 — Tahun sampul 2025 → 2026 🟢
Halaman sampul masih "2025"; tanggal kini 2026. ➡️ **Update** saat resubmit.

### F2 — Tulis Abstrak (ID + EN) 🔴
Abstrak masih placeholder template (ID + EN). ➡️ **Tulis** 100–200 kata, 3–5 kata kunci. Wajib untuk proposal sekalipun BAB IV/V kosong.

### F3 — Update `CLAUDE.md` + `config.yaml` 🟢
`CLAUDE.md` masih menulis optimizer "Adam", label smoothing default 0,02, patience 5, FreqCNN default 3-layer/130K, dan FFPP `[100,300,600,1000]`.
➡️ **Update** ke: **AdamW**, **label smoothing 0,05**, **patience 12**, **FreqCNN depth 5 / base 64 / ~4,2 juta**, FFPP `[100,250,500,750]`, dan **maks 100 frame/video**.
➡️ **`config.yaml`:** `max_frames_per_video: 50` → **100** (lihat A3) agar config ↔ tesis konsisten. *(Bukan masalah tesis, tapi cegah kebingungan saat cross-check berikutnya.)*

### F4 — Catatan kaki Gambar 3.7 (299→224) 🟢
Gambar 3.7 menampilkan input **299×299×3** (figur kanonik Xception) sementara pipeline pakai **224×224**. ➡️ Tambah catatan caption: *"input disesuaikan ke 224×224 pada implementasi ini."*

---

## ✅ Verifikasi setelah edit (checklist)

**Notebook (sekarang):**
- [ ] **N1** — **tidak ada aksi sekarang**; biarkan `N_SEEDS = 1` dan `MAX_FRAMES = 100`. *(Catatan untuk run final BAB IV nanti: naikkan `N_SEEDS = 3` agar tabel summary mean±std/72 run terbentuk.)*
- [x] **N2** komentar `patience` dihapus dari cell `code-01` — **selesai**.

**Docx (P1 wajib):**
- [ ] **A1** Tabel 3.3 / 3.11 / 3.12 = `[100,250,500,750]`; "72 run" tetap benar.
- [ ] **A2** §3.5.5 / Tabel 3.10 / §3.8.3 = batch 64 / efektif 128.
- [ ] **A3** Frame/video = **100** di Gambar 3.1 & 3.3, §3.2.4, §3.3.1, Tabel 3.1/1.1; total frame ~100.000/~75.000 (atau angka aktual dari manifes); `config.yaml` = 100.
- [ ] **B1** Tabel 3.10 label smoothing = "0,05 (aktif)"; kalimat kontradiktif §3.5.4 sudah dibenahi.
- [ ] **B2** Gambar 3.8 base=64 (`1→64→128→256→512→512`, FC `512→256→1`, GAP→512-d).
- [ ] **B3** Gambar 3.10: freq **512-d**, Proj **512→256**, **Dropout(0,5)** ×2, "**RGB** Input".
- [ ] **B4** Gambar 3.1: kotak "Deteksi & Crop Wajah" muncul antara Ekstraksi Frame & FFT; band-mask **0,05**.
- [ ] **B5** Klik sitasi BAB II hlm. 12: Durall=[8], Zhang=[9], Qian=[11], Tan=[12], Hasanaath=[16], Luo&Wang=[17].
- [ ] **F2** Abstrak ID+EN ditulis.

**Docx (P2):**
- [ ] **C1** klaim early-fusion "dievaluasi" dilunakkan.
- [ ] **C2** klaim empiris (§3.3.2/§3.4.1/Tabel 2.9) dilunakkan ke ekspektasi/literatur.
- [ ] **C3** §3.4.4 → "Tabel 3.7/3.8"; §3.6.4 → "Tabel 3.12".
- [ ] **D1** Eq (3.9) label F(1,1) + header /4; **D2** Eq (3.17) "3×0"; **D3** "Alam et al."
- [ ] **E1–E4** sitasi Gambar 2.1 & Tabel 2.1 (+typo), Goodfellow 2014, pass format IEEE.

**Housekeeping (P3):**
- [ ] **F1** tahun 2026; **F3** `CLAUDE.md`; **F4** catatan Gambar 3.7.

**Terakhir:** **Ctrl+A → F9** (TOC, nomor gambar/tabel/persamaan/sitasi) → simpan → re-render PDF → cek tidak ada nomor rusak.

---

## Urutan pengerjaan yang disarankan
1. **Notebook:** sudah beres (N2 dihapus). **N1 ditunda** — `N_SEEDS` tetap `1` untuk sekarang, `MAX_FRAMES` tetap `100`. *(Ingat: naikkan `N_SEEDS=3` saat run final BAB IV.)*
2. **A1, A2, A3** — sinkronisasi nilai run (tier FFPP, batch, frame/video → 100).
3. **B1** (label smoothing) lalu **B5** (sitasi BAB II: F9 → toggle IEEE→APA→IEEE → verifikasi hlm. 12).
4. **B2, B3, B4** — regenerasi 2 diagram + tambah kotak flowchart (serahkan ke yang pegang sumber gambar).
5. **C–E** — klaim, rujukan tabel, math/typo, sitasi/referensi.
6. **F2 Abstrak** + housekeeping (F1/F3/F4).
7. **Ctrl+A → F9** + simpan + re-render PDF.
8. Kabari saya — saya cek ulang `.docx` final untuk konfirmasi semua beres.

---

*Catatan: seluruh nilai diverifikasi langsung dari `config.yaml` (`max_frames_per_video: 50`, `batch_size: 16`, `n_seeds: 3`, `label_smoothing: 0.05`, `freq_base_channels: 64`, `freq_depth: 5`, `early_stop_patience: 12`) dan `colab_run.ipynb` cell code-01/code-02 (`FFPP_SAMPLES_LIST=[100,250,500,750]`, `MAX_FRAMES=100`, `N_SEEDS=1`, `BATCH_SIZE` auto-tune T4=64/A100=128, `FACE_CROP=True`). Arah penyelesaian mengikuti keputusan penulis di §8 `Deep_Analysis_BAB1-3_ColabCrossCheck_2026-06-03.md`.*
