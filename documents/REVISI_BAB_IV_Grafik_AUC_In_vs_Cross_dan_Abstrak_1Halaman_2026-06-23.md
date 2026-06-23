# REVISI — Grafik AUC In-vs-Cross (BAB IV) + Abstrak Jadi 1 Halaman (2026-06-23)

**Dokumen target (live):** `STUDI KOMPARATIF KINERJA DETEKSI DEEPFAKE BERBASIS ARSITEKTUR HYBRID XCEPTIONNET-FFT TERHADAP MODEL DOMAIN TUNGGAL.docx` (OneDrive, folder Thesis).
**Backup pra-revisi:** `STUDI KOMPARATIF...DOMAIN TUNGGAL_BACKUP_pre-revisi_2026-06-23.docx` (sesama folder) + salinan di scratchpad sesi.
**Status:** Sudah diterapkan langsung ke `.docx`. **PDF belum diregenerasi** (lihat §AKSI WAJIB DI WORD).

Dua butir masukan penguji dikerjakan:
1. **BAB IV** — tambah grafik khusus (Spasial, Hybrid, Frekuensi) yang menampilkan perubahan AUC in-dataset → cross-dataset agar besarnya penurunan performa langsung terbaca, serta menonjolkan asimetri arah (FFPP→CDF vs CDF→FFPP).
2. **Abstrak** — dipadatkan menjadi 1 halaman.

---

## 1. BAB IV — Gambar baru "Perubahan AUC In-Dataset → Cross-Dataset"

**Letak:** subbab **4.1.5 Analisis Generalization Drop**, tepat setelah pembahasan Gambar 4.7 (drop F1) dan sebelum subbab 4.1.6 Pengaruh Ukuran Sampel.

**Penomoran (otomatis via field SEQ):**
- Grafik baru = **Gambar 4.8**.
- Gambar lama bergeser: 4.8 Tren AUC → **4.9**; 4.9 Confusion matrix → **4.10**; 4.10 Kurva pelatihan → **4.11**.
- Caption pakai field `STYLEREF 1 \s` + `SEQ Gambar`, rujukan dalam teks pakai field `REF`. Daftar Gambar = field TOC. Semua menomori ulang sendiri saat **Update Field**. Nilai cache sudah ikut dinaikkan agar nomor caption sudah benar walau belum di-refresh.

**File gambar sumber:** `documents/media_v2/gambar_4_x_auc_in_vs_cross.png` (sudah tertanam di `.docx`).
**Generator:** fungsi `fig_auc_in_vs_cross()` baru di `deepfake_hybrid/scripts/make_bab4_figures.py`. Regenerasi: `python scripts/make_bab4_figures.py outputs/tables auc_in_vs_cross`.

**Desain grafik:** slope chart 2 panel (satu per arah). Tiap model satu garis menghubungkan AUC in-dataset → AUC cross-dataset; makin curam turun, makin besar penurunannya. Label Δ = AUC in-dataset − cross-dataset (positif = turun, **konsisten dengan Tabel 4.4**). Garis acuan 0,5 (tebakan acak).

**Angka (n = 750, rata-rata 3 seed; sumber `outputs/tables/n750/Table{1,2}_*_summary.csv`):**

| Arah | Model | AUC In | AUC Cross | Δ (In−Cross) |
|---|---|---|---|---|
| FFPP→CDF | Spasial | 0,778 | 0,678 | **+0,101** (turun kecil) |
| FFPP→CDF | Hybrid | 0,644 | 0,665 | **−0,021** (naik tipis) |
| FFPP→CDF | Frekuensi | 0,562 | 0,606 | **−0,044** (naik tipis) |
| CDF→FFPP | Spasial | 0,971 | 0,607 | **+0,364** (turun besar) |
| CDF→FFPP | Hybrid | 0,919 | 0,555 | **+0,364** (turun besar) |
| CDF→FFPP | Frekuensi | 0,562 | 0,575 | **−0,013** (datar) |

**Pesan grafik:** pada FFPP→CDF garis hybrid nyaris datar bahkan sedikit naik (Δ=−0,021) → hybrid menahan generalization drop. Pada CDF→FFPP garis hybrid jatuh sama dalam dengan spasial (Δ=+0,364) → manfaat FFT tidak konsisten dan bergantung arah. Ini visualisasi langsung dari temuan penguji.

**Teks yang ditambahkan (siap-baca; sudah masuk ke `.docx`):**

> (a) Pengantar — sebelum gambar:
> Selain selisih F1-score, besarnya penurunan performa juga dapat diamati langsung dari perubahan nilai AUC antara evaluasi *in*-dataset dan *cross*-dataset. [REF→Gambar 4.8] menyajikan perubahan tersebut untuk ketiga model pada masing-masing arah pengujian, sehingga besarnya penurunan AUC dapat dibaca langsung dari kemiringan tiap garis.

> Caption:
> **Gambar 4.8** Perbandingan AUC *in*-dataset dan *cross*-dataset ketiga model pada kedua arah pengujian (n = 750)

> (b) Pembahasan — setelah gambar:
> Pola pada gambar tersebut mempertegas sifat asimetris generalisasi antar arah. Pada arah FFPP→CDF, penurunan AUC relatif kecil, model spasial hanya turun Δ = +0,101 sementara model hybrid dan frekuensi justru sedikit meningkat (Δ = −0,021 dan Δ = −0,044), sehingga penambahan cabang frekuensi efektif menahan penurunan generalisasi pada arah ini. Sebaliknya, pada arah CDF→FFPP penurunan AUC sangat besar dan model hybrid (Δ = +0,364) turun sama dalamnya dengan model spasial (Δ = +0,364), yang menunjukkan bahwa manfaat penambahan domain frekuensi tidak konsisten dan bergantung arah. Adapun model frekuensi tetap berada di sekitar 0,56–0,61 pada kedua arah karena performa *in*-dataset-nya memang sudah rendah, sehingga nilainya hampir tidak berubah saat diuji lintas dataset. Konsistensi temuan ini dengan Tabel 4.4 memperkuat bahwa kontribusi domain frekuensi dalam menekan generalization drop bersifat parsial dan tidak dapat digeneralisasi ke seluruh arah pengujian.

---

## 2. Abstrak — jadi 1 halaman

**Masalah:** abstrak (ID + EN) melimpah ke halaman ii. Penyebab = spasi 1,5 (default `w:line="360"`), **bukan** jumlah kata (ID 167 kata, EN 181 kata — keduanya sudah ≤ 200, sesuai Pedoman).

**Perbaikan (tanpa mengubah isi):** paragraf abstrak ID, kata kunci, abstract EN, dan keywords diset **spasi 1** (`w:line="240"`, `after=0`). Spasi 1 untuk abstrak memang lazim/standar dan menghemat ±4.800 twips, sehingga seluruh abstrak (±12.560 twips) muat dalam area teks 1 halaman (14.004 twips), sisa ±5 baris. Isi teks dan jumlah kata tidak diubah.

---

## §AKSI WAJIB DI WORD (setelah buka file)

1. Buka `.docx` di Microsoft Word. Sudah diset `updateFields=true`, jadi Word akan menawarkan update field saat dibuka → pilih **Yes/Update**. Jika tidak muncul: **Ctrl+A** lalu **F9** (Update Field); untuk Daftar Gambar pilih **"Update entire table"**.
   - Ini menuntaskan: penomoran Gambar 4.8–4.11, semua rujukan `REF` dalam teks, dan **Daftar Gambar** (entri + nomor halaman).
2. **Cek visual abstrak** muat 1 halaman (estimasi sudah pas, tetapi konfirmasi karena render LibreOffice tidak tersedia di mesin ini).
3. **Ekspor ulang PDF** dari Word (Save As PDF) menggantikan PDF lama — PDF saat ini masih versi pra-revisi.

## Verifikasi
- Angka grafik dihitung ulang dari `outputs/tables/n750/Table{1,2}_*_summary.csv` (3-seed run baru 2026-06-20), cocok dengan Tabel 4.2 (in-dataset) dan Tabel 4.3 (cross-dataset) di dokumen.
- `document.xml` well-formed; gambar tertanam valid (rId45 → image26.png, 2600×1200); media 25 → 26.
- Analisis pendukung: `analyze/BAB_IV_Analysis_Grafik_AUC_In_vs_Cross_2026-06-23_0842.md`.
