# Hasil Pelatihan **Sebelum** Face Crop (MTCNN) — Arsip & Bukti

> Dokumen ini mengumpulkan **semua hasil pelatihan yang dijalankan pada frame penuh (full frame), sebelum MTCNN face cropping diterapkan**, beserta lokasi bukti fisiknya dan perbandingan langsung sebelum-vs-sesudah crop.
>
> **Kenapa dokumen ini ada:** face crop adalah **satu-satunya perubahan yang paling menentukan** di seluruh proyek (spatial FFPP 0,696 → 0,901). Kalau penguji bertanya *"kenapa pakai face crop?"* atau *"apa buktinya crop itu perlu?"*, jawabannya ada di sini — bukan asumsi, tapi hasil eksperimen berpasangan.
>
> Dibuat 2026-07-25. Angka = **AUC in-dataset (test)** kecuali disebut lain. Model: **S**=spatial, **F**=freq, **H**=hybrid.
> Semua angka di dokumen ini **sudah diverifikasi ulang** langsung dari `Table1_in_dataset.csv` / `Table2_cross_dataset.csv` di tiap folder (bukan hanya menyalin `conclusion.md`).

---

## 1. TL;DR — 4 poin untuk dihafal

1. **Batas waktunya jelas:** MTCNN face crop masuk pada **2026-04-09** (commit `3e2f181`). Semua run bertanggal **sebelum** itu = full frame.
2. **Tanpa crop, FFPP gagal total di skala besar.** Di n=500/750, spatial & hybrid FFPP **di bawah 0,5** (lebih buruk dari tebak acak), dengan separasi prediksi hampir nol (gap 0,004–0,035).
3. **Crop menyelamatkan cabang spasial** (FFPP 0,696 → **0,901**, gap separasi 0,02 → **0,457**) tetapi **merusak cabang frekuensi** (FFPP 0,746 → **0,256**).
4. **Bukan karena FFPP multi-metode.** Ablasi per-metode tanpa crop (`separated_ffpp`) tetap near-random (0,43–0,65) → yang bikin gagal adalah **latar/konteks frame penuh**, bukan campuran 4 metode manipulasi. Crop-lah obatnya, bukan pemisahan metode.

---

## 2. Garis waktu — mana pre-crop, mana post-crop

| Commit | Tanggal | Isi |
|---|---|---|
| `3e2f181` | **2026-04-09** | **Add MTCNN face detection + cropping during frame extraction** ← garis batas |
| `f03643c` | 2026-04-10 | Add high-pass filter to FFT + increase freq model capacity |
| `7186a7d` | 2026-04-10 | face crop results |

> ⚠️ **Jebakan penamaan folder (penting!)**
> Run **pre-crop n500 & n750 tersimpan di dalam folder `2026-04-09/`**, yaitu di `2026-04-09/2026-04-05_continue/` — bersebelahan dengan `2026-04-09/face_crop/` yang justru **post-crop**. Satu tanggal, dua sisi perubahan.
> Pembeda pasti: `face_crop/n100/conclusion.md` menulis eksplisit **`face_crop=True, margin=0.3`** di header; folder pre-crop tidak.
> Urutan jam di log 2026-04-09: `separated_ffpp` 08:53–11:37 (pre-crop) → re-ekstraksi dengan MTCNN → `face_crop` 16:30–17:36 (post-crop).

---

## 3. Peta lokasi bukti (semua pre-crop)

Root: `deepfake_hybrid/outputs/`

| Folder | Tier | Isi | Catatan |
|---|---|---|---|
| **`2026-04-09/2026-04-05_continue/conclusion.md`** | **n100–750** | **Analisis gabungan 4 tier — dokumen pre-crop paling lengkap** | ⭐ mulai dari sini |
| `2026-04-05/` | n100, n250 | `conclusion.md`, runs, manifests, plots, tables | Train 5 |
| `2026-04-09/2026-04-05_continue/` | n500, n750 | runs, manifests, plots, tables | lanjutan Train 5 |
| `2026-04-09/separated_ffpp/n100/` | n100 per-metode | ablasi Deepfakes/Face2Face/FaceSwap/NeuralTextures | pre-crop (pagi) |
| `2026-04-03/` | n100 | Train 4 — sebelum perbaikan LR | konfigurasi berbeda |
| `2026-03-15/`, `2026-03-16/`, `2026-03-23/`, `2026-03-24/`, `2026-03-25/` | n50, n200, n400, dll. | Train 1–3 | arsitektur & config lebih lama, **tidak sebanding langsung** |

Tiap folder run berisi `metrics.json` (riwayat per-epoch) + `train.log`; tier n500/n750 juga punya `manifests/`, `plots/`, `tables/`. Checkpoint (`best.pt`) hanya tersimpan di run lama (2026-03-15/16) — tier n500/n750 tidak menyimpan bobot.

**Konfigurasi pre-crop (Train 5):** seed 0 · lr 2e-4 · warmup 2 epoch · patience 10 · pretrained ImageNet · tanpa face crop.

---

## 4. Hasil pre-crop — AUC in-dataset (test)

| Model | FFPP n100 | n250 | n500 | n750 | CDF n100 | n250 | n500 | n750 |
|---|---|---|---|---|---|---|---|---|
| spatial | 0,696 | 0,552 | **0,469** | **0,492** | 0,796 | 0,684 | 0,693 | **0,739** |
| freq | 0,746 | 0,723 | 0,511 | 0,544 | 0,837 | 0,578 | 0,585 | 0,653 |
| hybrid | 0,616 | 0,563 | 0,573 | **0,469** | **0,866** | 0,575 | 0,594 | 0,697 |

**Bacaan:**
- **FFPP makin banyak data makin hancur.** Di n500/n750 spatial & hybrid tembus ke bawah 0,5. Ini terjadi pada **ketiga arsitektur** → bukan bug hyperparameter satu model.
- **CDF berperilaku normal**: turun di n250 (test set membesar 2,3× dan memuat video lebih sulit) lalu **pulih** ke 0,739 (S) / 0,697 (H) di n750.
- Angka tertinggi (hybrid CDF n100 = 0,866) justru di tier terkecil → **wajib diberi catatan noise**, lihat §8.

## 5. Hasil pre-crop — AUC cross-dataset

| Arah | Model | n100 | n250 | n500 | n750 |
|---|---|---|---|---|---|
| FFPP→CDF | spatial | **0,833** | 0,437 | 0,546 | 0,520 |
| FFPP→CDF | freq | **0,856** | 0,634 | 0,374 | 0,409 |
| FFPP→CDF | hybrid | 0,562 | 0,457 | 0,563 | **0,634** |
| CDF→FFPP | spatial | 0,774 | 0,320 | 0,510 | 0,582 |
| CDF→FFPP | freq | 0,562 | **0,742** | **0,589** | 0,561 |
| CDF→FFPP | hybrid | **0,798** | 0,438 | 0,510 | 0,530 |

Tidak ada pemenang konsisten; fluktuasi besar antar tier. Nilai n100 yang tampak bagus (0,833 / 0,856 / 0,798) **kemungkinan besar inflasi test set kecil**. Hasil cross-dataset pre-crop paling bisa dipercaya: **hybrid FFPP→CDF n750 = 0,634**.

## 6. F1 pre-crop — bukti cabang frekuensi tidak stabil

| Model | FFPP n100 | n250 | n500 | n750 | CDF n100 | n250 | n500 | n750 |
|---|---|---|---|---|---|---|---|---|
| spatial | 0,667 | 0,588 | 0,363 | 0,505 | 0,565 | 0,648 | 0,676 | 0,670 |
| freq | 0,495 | 0,591 | **0,018** | 0,166 | 0,758 | 0,553 | **0,008** | 0,647 |
| hybrid | 0,652 | 0,565 | 0,592 | 0,463 | 0,603 | 0,540 | 0,620 | 0,635 |

F1 = **0,018** (freq FFPP n500) dan **0,008** (freq CDF n500) artinya model memprediksi hampir semua sampel ke satu kelas. Log DIAG mengonfirmasi: `freq_CDF` n500 mengeluarkan probabilitas 0,02–0,05 untuk semuanya (recall 0,004 dengan hanya 10 TP dari 2.431 fake). Jadi **ketidakstabilan cabang frekuensi sudah muncul sejak sebelum crop** — bukan efek samping cropping.

## 7. Separasi prediksi (DIAG) — akar masalah pre-crop

Rata-rata probabilitas untuk kelas real vs fake di test set sendiri, tier n750:

| Model | mean_prob real | mean_prob fake | Gap | Status |
|---|---|---|---|---|
| spatial_FFPP | 0,428 | 0,463 | **0,035** | sangat lemah |
| freq_FFPP | 0,468 | 0,472 | **0,004** | praktis acak |
| hybrid_FFPP | 0,392 | 0,419 | **0,027** | sangat lemah |
| spatial_CDF | 0,278 | 0,618 | 0,340 | kuat |
| freq_CDF | 0,518 | 0,572 | 0,054 | lemah |
| hybrid_CDF | 0,308 | 0,585 | 0,277 | baik |

**Model FFPP pre-crop benar-benar tidak bisa membedakan real dari fake** (gap 0,004–0,035), sementara model CDF mencapai separasi nyata (0,28–0,34). Ini bukan soal kalibrasi threshold — informasinya memang tidak ada di representasi yang dipelajari.

Dinamika latihan menguatkan: semua model FFPP pre-crop menurunkan train loss ke 0,13–0,16 sementara val AUC diam di 0,35–0,58 → **menghafal tanpa belajar**. Contoh `hybrid_FFPP_n750`: epoch 1 train_loss 0,675 / val_auc 0,324 → epoch 20 train_loss 0,140 / val_auc 0,373.

## 8. Ablasi pendukung — FFPP per-metode, tetap tanpa crop

`2026-04-09/separated_ffpp/n100/` — FFPP dilatih **terpisah per metode manipulasi** (bukan 4 metode dicampur), masih full frame:

| Model | Deepfakes | Face2Face | FaceSwap | NeuralTextures |
|---|---|---|---|---|
| spatial | **0,615** | 0,538 | 0,550 | 0,433 |
| freq | 0,417 | 0,473 | 0,470 | 0,497 |
| hybrid | **0,646** | 0,519 | 0,541 | 0,541 |

**Ini eksperimen yang mematikan satu hipotesis.** Hipotesis awal di `conclusion.md` pre-crop adalah *"FFPP gagal karena mencampur 4 metode manipulasi"*. Ternyata **memisahkan metode tidak menolong** — tetap near-random. Yang menolong adalah **membuang latar dan fokus ke wajah**. Ini argumen kuat dan berbasis bukti untuk membela keputusan face crop.

---

## 9. Perbandingan langsung: sebelum vs sesudah crop (n=100, seed 0)

Sumber: `2026-04-09/face_crop/n100/conclusion.md` (sudah memuat tabel berpasangan ini).

### AUC in-dataset

| Model | FFPP tanpa crop | FFPP + crop | Δ | CDF tanpa crop | CDF + crop | Δ |
|---|---|---|---|---|---|---|
| spatial | 0,696 | **0,901** | **+0,205** | 0,796 | **0,822** | +0,026 |
| freq | 0,746 | **0,256** | **−0,490** | 0,837 | 0,568 | −0,269 |
| hybrid | 0,616 | 0,678 | +0,062 | 0,866 | 0,785 | −0,081 |

### Separasi prediksi (gap) — perubahan paling dramatis

| Model | Gap tanpa crop | Gap + crop |
|---|---|---|
| spatial_FFPP | 0,005–0,035 | **0,457** |
| spatial_CDF | 0,260–0,340 | **0,398** |
| hybrid_CDF | 0,152–0,277 | 0,363 |
| freq_FFPP | ~0,006 | −0,180 (**terbalik**) |

### Cross-dataset setelah crop

| Arah | S | F | H |
|---|---|---|---|
| FFPP→CDF | 0,543 | 0,644 | **0,647** |
| CDF→FFPP | **0,741** | 0,565 | **0,730** |

Arah CDF→FFPP jelas membaik (spatial 0,741, hybrid 0,730) — model yang dilatih pada wajah ter-crop pindah domain lebih baik.

---

## 10. Interpretasi — kenapa crop menolong spasial tapi merusak frekuensi

**Kenapa spasial melompat.** Pada frame penuh, wajah hanya sebagian kecil piksel; sisanya latar, tubuh, dan artefak kompresi YouTube. XceptionNet menghabiskan kapasitas pada konteks yang tidak berkorelasi dengan label, lalu menghafal latar per video (train loss turun, val AUC diam). Setelah crop, hampir semua piksel adalah wajah — tepat di tempat artefak manipulasi berada. Separasi naik dari 0,02 ke 0,46: perubahan kualitatif, bukan sekadar tuning.

**Kenapa frekuensi jatuh.** Ini penjelasan yang paling penting untuk cabang frekuensi, dan **kami punya bukti di disk, bukan spekulasi**: MTCNN menghasilkan crop kecil dengan ukuran bervariasi, lalu di-resize naik ke input model. Resampling itu sendiri **menulis ulang isi frekuensi tinggi** — justru komponen tempat artefak upsampling GAN berada. Jadi crop memindahkan sinyal ke tempat cabang spasial bisa memakainya, sekaligus **mencuci sinyal yang jadi andalan cabang FFT**. Ini menjelaskan kenapa freq tetap lemah (0,56) di hasil final skripsi.

**Konsekuensi untuk klaim skripsi.** Face crop adalah trade-off yang **disengaja dan terdokumentasi**: kami menerima pelemahan cabang frekuensi demi baseline spasial yang layak. Tanpa crop, FFPP di bawah 0,5 dan tidak ada satu pun model yang bisa dipertahankan. Keputusan ini konsisten dengan praktik standar bidang ini (Rössler dkk., Li dkk. — deteksi deepfake bekerja pada region wajah).

---

## 11. Catatan kehati-hatian (sebutkan kalau ditanya, jangan disembunyikan)

- **Seed 0 saja.** Semua angka pre-crop di dokumen ini seed tunggal. Hasil final skripsi (Train 9, n=750) pakai 3 seed dengan mean ± std.
- **Tier kecil = noise.** Split test n100 hanya ~15 video (FFPP 1.239 frame, CDF 1.026 frame). Angka mencolok seperti hybrid CDF n100 = 0,866 dan cross-dataset 0,83–0,86 **tidak boleh diklaim sebagai hasil** — itu inflasi test set kecil. Pertumbuhan test set: n100 → 1.239/1.026 frame; n250 → 3.268/2.390; n500 → 5.957/5.094; n750 → 8.996/7.564.
- **Perbandingan sebelum/sesudah crop hanya di n=100.** Tier crop yang lebih besar dijalankan setelah perubahan lain (high-pass FFT, kapasitas freq) ikut masuk, jadi tidak ada perbandingan crop yang bersih di n500/n750. Yang berpasangan bersih hanya n100.
- **Bukan satu-satunya perubahan sesudahnya.** Antara pre-crop dan hasil final ada Train 7 (Kaggle n500), Train 8 (config-drift fix + LR rebalance), Train 9 (3 seed). Jangan sajikan delta crop sebagai satu-satunya penyebab perbaikan akhir.
- **Manifest tidak portabel.** Manifest di folder-folder ini menyimpan path frame dengan separator OS asli — jangan dipakai lintas mesin.

---

## 12. Kalau ditanya penguji → jawab

| Pertanyaan | Jawaban singkat |
|---|---|
| *"Kenapa pakai face crop / MTCNN?"* | Karena tanpa crop FFPP gagal total: AUC di bawah 0,5 di n500/n750 dengan separasi prediksi hampir nol. Setelah crop, spatial FFPP naik ke 0,901. Perbandingan berpasangannya ada di `outputs/2026-04-09/`. |
| *"Ada bukti tanpa crop?"* | Ada, lengkap 4 tier (n100–750): `outputs/2026-04-09/2026-04-05_continue/conclusion.md`, plus run, log, dan tabel per tier. |
| *"Mungkin FFPP gagal karena 4 metode manipulasi dicampur?"* | Sudah diuji: FFPP dilatih terpisah per metode (tetap tanpa crop) **tetap near-random** (0,43–0,65). Jadi penyebabnya frame penuh, bukan campuran metode. |
| *"Kenapa cabang frekuensi lemah?"* | Salah satu penyebab teridentifikasi: face crop + resize menulis ulang komponen frekuensi tinggi tempat artefak GAN berada. Buktinya freq FFPP turun 0,746 → 0,256 tepat saat crop diaktifkan, satu-satunya perubahan. Selain itu freq sudah tidak stabil sejak pre-crop (F1 0,008–0,018 di n500). |
| *"Apakah crop menaikkan semua model?"* | Tidak — dan itu kami laporkan apa adanya. Spatial naik tajam, hybrid sedikit naik di FFPP, frekuensi turun. Trade-off yang disengaja. |
| *"Kenapa hasil awal (0,866) tidak dipakai?"* | Itu n=100, test set ~15 video, seed tunggal — noise. Hasil skripsi pakai n=750 dengan 3 seed. |

---

## Rujukan silang

- [INVENTARIS_SEMUA_EKSPERIMEN_2026-07-07.md](INVENTARIS_SEMUA_EKSPERIMEN_2026-07-07.md) — jurnal kronologis Train 1→9; dokumen ini memperluas **Train 5 & Train 6**.
- [SIDANG_QA_freq_negative.md](SIDANG_QA_freq_negative.md) — Q&A temuan negatif frekuensi (§10 di sini memberi satu penyebab mekanistiknya).
- [sidang_study_guide_SPATIAL_branch.md](sidang_study_guide_SPATIAL_branch.md) — cabang spasial; crop adalah alasan utama baseline spasial jadi kuat.
- [RINGKASAN_PARAMETER_NILAI_PROYEK.md](RINGKASAN_PARAMETER_NILAI_PROYEK.md) — parameter final (`face_crop`, `face_margin`).
