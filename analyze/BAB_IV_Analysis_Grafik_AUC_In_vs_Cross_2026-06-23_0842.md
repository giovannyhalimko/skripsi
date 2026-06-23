# BAB IV — Analisis Grafik AUC In-vs-Cross & Abstrak 1 Halaman

**Tanggal:** 2026-06-23 08:42
**Dokumen:** STUDI KOMPARATIF ... DOMAIN TUNGGAL.docx (live)
**Pemicu:** masukan penguji — (1) tambah grafik perubahan In-dataset AUC vs Cross-dataset AUC untuk Spasial/Hybrid/Frekuensi agar besarnya penurunan langsung terlihat; (2) abstrak jadi 1 halaman.
**Changelog terkait:** `documents/REVISI_BAB_IV_Grafik_AUC_In_vs_Cross_dan_Abstrak_1Halaman_2026-06-23.md`

---

## 1. Pemetaan masukan penguji → temuan data

Penguji mencatat: *"hybrid mampu mengurangi generalization drop pada arah FFPP→CDF, tetapi tidak konsisten pada arah sebaliknya."* Data AUC (n=750, 3-seed) memang menunjukkan asimetri arah yang tajam:

| Arah | Δ AUC Spasial | Δ AUC Hybrid | Δ AUC Frekuensi |
|---|---|---|---|
| FFPP→CDF | +0,101 | **−0,021** | −0,044 |
| CDF→FFPP | +0,364 | **+0,364** | −0,013 |

(Δ = AUC in-dataset − cross-dataset; positif = turun, konvensi sama dengan Tabel 4.4.)

- **FFPP→CDF:** hybrid praktis tidak turun (Δ=−0,021, sedikit naik) → mendukung klaim "hybrid menahan drop pada arah ini".
- **CDF→FFPP:** hybrid turun **sama dalam** dengan spasial (keduanya Δ=+0,364) → membuktikan "tidak konsisten pada arah sebaliknya".

Jadi grafik bukan sekadar dekorasi: ia adalah bukti visual langsung atas kalimat temuan penguji.

## 2. Mengapa AUC (bukan F1) dan mengapa slope chart

- Tabel/Gambar 4.4/4.7 yang sudah ada memakai **drop F1-score**. F1 menyembunyikan satu nuansa: pada FFPP→CDF, AUC hybrid/frekuensi malah **naik** (karena CDF lebih mudah), padahal F1 tetap turun akibat keruntuhan recall. Grafik AUC melengkapi gambaran: memisahkan "kemampuan pemeringkatan" (AUC) dari "kalibrasi ambang" (recall/F1).
- **Slope chart** dipilih karena permintaan eksplisit "menunjukkan perubahan ... sehingga dapat langsung melihat besarnya penurunan". Kemiringan garis = besarnya perubahan; dua panel arah = asimetri. Bentuk ini juga berbeda dari bar chart 4.3/4.5/4.7 sehingga menambah informasi, bukan mengulang.

## 3. Verifikasi numerik (sumber kebenaran)

Seluruh nilai dibaca ulang dari CSV ringkasan 3-seed run baru:
- `deepfake_hybrid/outputs/tables/n750/Table1_in_dataset_summary.csv` → `auc_mean`
  - FFPP: spatial 0,7781 / hybrid 0,6437 / freq 0,5623; CDF: spatial 0,9712 / hybrid 0,9185 / freq 0,5625
- `.../Table2_cross_dataset_summary.csv` → `auc_mean`
  - FFPP→CDF: spatial 0,6776 / hybrid 0,6649 / freq 0,6063; CDF→FFPP: spatial 0,6068 / hybrid 0,5548 / freq 0,5753

Cocok dengan Tabel 4.2 (in-dataset) dan Tabel 4.3 (cross-dataset) di dokumen, serta dengan ringkasan cepat di `documents/PERBAIKAN_Angka_Inline_BAB_IV_2026-06-20.md`. Tidak ada konflik.

Rentang freq di teks pembahasan ("0,56–0,61") = min–maks AUC frekuensi lintas keempat sel (0,562–0,606); konsisten dengan abstrak.

## 4. Dampak struktural pada dokumen

- Penomoran gambar memakai field (SEQ/STYLEREF/REF/TOC). Penyisipan Gambar 4.8 memicu pergeseran 4.8→4.9, 4.9→4.10, 4.10→4.11 yang **otomatis** saat Update Field. Nilai cache caption sudah dinaikkan agar benar tanpa refresh; rujukan REF dalam teks dan Daftar Gambar masih perlu refresh (`updateFields=true` menanganinya saat file dibuka di Word).
- Tidak ada tabel baru → "Tabel 4.4" yang dirujuk paragraf pembahasan baru tetap valid.

## 5. Abstrak 1 halaman — diagnosis

- Luapan ke halaman ii **bukan** karena kelebihan kata (ID 167, EN 181, keduanya ≤200 sesuai `skills/skripsi-format-guide.md`), melainkan spasi 1,5 (`docDefaults w:line="360"`).
- Perbaikan = spasi 1 pada 4 paragraf abstrak (`w:line="240"`, after=0). Hemat ±138 twips/baris × ±35 baris ≈ 4.830 twips. Total tinggi abstrak turun ke ±12.560 twips < area teks 14.004 twips (A4, margin atas/bawah 2,5 cm). Isi tidak diubah → tidak ada risiko makna/angka.
- **Caveat:** verifikasi 1-halaman bersifat geometris; LibreOffice/Word headless tidak tersedia di mesin ini, jadi konfirmasi visual final dilakukan saat user membuka di Word.

## 6. Risiko & mitigasi
- *Pre-refresh:* rujukan teks ke gambar lama (REF) sempat menampilkan nomor lama sampai F9 — dimitigasi `updateFields=true` + instruksi eksplisit di changelog.
- *PDF lama stale:* PDF belum diregenerasi; user harus ekspor ulang dari Word setelah refresh field.
- *Backup:* salinan pra-revisi disimpan di folder Thesis dan scratchpad sesi bila perlu rollback.

## 7. Tindak lanjut yang disarankan
- Pertimbangkan menyebut Gambar 4.8 di subbab Pembahasan 4.2.3 (Pengaruh FFT) sebagai rujukan silang, karena di situlah argumen "manfaat hybrid bergantung arah" dibahas naratif.
