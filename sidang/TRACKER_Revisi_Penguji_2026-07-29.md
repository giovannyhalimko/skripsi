# 📋 TRACKER — Revisi Penguji Sidang (Notulen Ujian Akhir)

**Update terakhir:** 2026-07-29
**Sumber:** `Notulen [IF]-[…Samuel/Giovanny/Naomi].xlsx` — 8 item revisi, penguji **Irpan** & **Mustika**, notulis Gunawan.
**Prioritas = warna** di kolom notulen.

## 🎨 Legenda prioritas (warna sel notulen)
| Warna | Kode | Arti (asumsi — mohon konfirmasi) |
|---|---|---|
| 🟥 Merah tua | `C00000` | **P1 — kritis** (item 1, 3, 7) |
| 🟧 Merah | `FF0000` | **P2 — tinggi** (item 2, 5) |
| 🟩 Hijau | `92D050` | **P3 — rendah / "pertimbangkan/kaji"** (item 4, 8) |
| ⬜ Tanpa warna | — | belum ditandai (item 6) |

> ✅ Urutan dikonfirmasi user (2026-07-29): **merah tua > merah > hijau**.

---

## 📊 Master — 8 item

| No | Item | BAB / Hal | Penguji | Prioritas | Status |
|---|---|---|---|---|---|
| 1 | Latar Belakang — sifat studi komparatif belum tampak | BAB I | Irpan | 🟥 P1 | ✅ **SELESAI** (terpasang di .docx) |
| 3 | BAB 2 & 3 — wording AI-like dinarasikan ulang | BAB II/III | Mustika | 🟥 P1 | ✅ **SELESAI 30/30** (terpasang di .docx) |
| 7 | Hipotesis → hapus, fokus Tujuan | BAB I / hal 4 | Irpan | 🟥 P1 | ✅ **SELESAI** (di .docx) · ⚠️ perlu F9 |
| 2 | Lengkapi referensi pendukung | — | Irpan | 🟧 P2 | 🟡 **Sebagian** — justifikasi rumus + FreqCNN ✅ SELESAI (6 sitasi dikonversi); sisa = audit sitasi lama |
| 5 | Probabilitas 5%, apa dasarnya? (= spectral band masking) | BAB III / hal 79 | Mustika | 🟧 P2 | ✅ **Dasar ditulis di laporan** (hal 79) |
| 6 | Dasar hyperparameter — inti: batch size (Tabel 3.11)? | BAB III / hal 95 | Mustika | ⬜ ? | ✅ **SELESAI** (landasan hal 95 + refs + config.yaml + sitasi) |
| 4 | Pertimbangkan kembali penerapan studi komparatif | — | Mustika | 🟩 P3 | ⏭️ **SKIP** (rencana user 2026-07-29) |
| 8 | Keadilan sampling + karakteristik dataset | Dataset/§3.2 | Irpan | 🟩 P3 | ✅ **SELESAI** (konten + 2 tabel dipaste; cek duplikat Komposisi) |

**➡️ SISA:** **item 2 bagian "audit sitasi lama"** saja (§2.3.4/2.9.4/2.11 sitasi hilang, gambar arsitektur XceptionNet §2.10.1, 48 sumber "Book"). *(Item 1, 3, 5, 6, 7, 8 SELESAI; item 2 bagian rumus/FreqCNN SELESAI; item 4 SKIP.)*
**Status Word (kamu):** ✅ semua sitasi [Nama]→[n] (termasuk 6 sitasi rumus item-2 baru), ✅ Ctrl+A→F9, ✅ 2 tabel dipaste + angka diupdate, ✅ highlight review, ✅ Szegedy 2016 ditambah ke Daftar Pustaka.
**Fix lanjutan 2026-07-29:** ✅ sisa "37.500" (rumus math di §3.2.4 "Batas 50…") → 100/61.000 konsisten. ✅ highlight semua KUNING.
**➕ EKSTRA (permintaan penguji, 2026-07-29):** ✅ **"tanda panah" (→) di prosa diganti kata** (33 panah, terpasang & stabil) — lihat section "TANDA PANAH → KATA" di bawah.
**♻️ Insiden clobber (22:27):** arrows + 6 sitasi item-2 sempat ditimpa Word AutoSave, **sudah dipasang ulang & dikonversi** (verifikasi 2026-07-29: arrows 19, 0 placeholder, CITATION 323). Detail di section "INSIDEN CLOBBER".

### 🎯 Item 2 — scope diperluas (permintaan user 2026-07-29):
Bukan sekadar lengkapi sitasi. **Audit justifikasi:** cek SEMUA rumus/persamaan apakah benar ada di referensi (bukan mengada-ngada). **FreqCNN (model bikinan sendiri) WAJIB dijustifikasi referensi** juga. Kurang referensi → tambahkan. Perlu paragraf → tambah/adjust.
**⚠️ WAJIB di Word:** buka `.docx` → **Ctrl+A → F9** untuk (a) hapus "1.4 Hipotesis Penelitian" dari Daftar Isi, (b) renumber Manfaat 1.5→1.4, (c) refresh sitasi.

---

# DETAIL PER ITEM (urut prioritas)

## ✅ Item 1 — Latar Belakang studi komparatif · 🟥 P1 · SELESAI
Terpasang di `.docx` (2026-07-29). Catatan penguji "masa dari awal tidak dijelaskan" sudah dijawab: komparatif dijelaskan **sejak awal** + detail di penutup.
**Cek di Word (Ctrl+F):**
- ☐ `Penelitian ini merupakan sebuah studi komparatif yang membandingkan tiga pendekatan` — paragraf orientasi baru (setelah paragraf pembuka)
- ☐ `Alih-alih hanya membangun satu detektor` — paragraf 385a (kerangka komparatif)
- ☐ `Ketiga model dilatih dan diuji pada dua dataset benchmark` — paragraf 385b (uraian yang dilakukan)

## ✅ Item 3 — BAB 2 & 3 wording AI-like · 🟥 P1 · SELESAI 30/30
Semua 30 edit terpasang di `.docx`. 25 edit awal = text-only (formatting utuh). **5 paragraf terakhir** (p476, p571, p802, p1038, p1058) **dibangun ulang** karena formatting sumbernya rusak — sekalian dirapikan (buang italic satu-frasa yang keliru & spasi non-breaking nyasar), sitasi tetap utuh. Detail: `documents/REVISI_BAB_II_III_Narasi_AI_Wording_2026-07-28.md`.
**Cek di Word — 5 paragraf yang dibangun ulang (Ctrl+F):**
- ☐ `Berbagai studi tersebut mengindikasikan bahwa informasi domain frekuensi dapat melengkapi` (p476)
- ☐ `Anomali frekuensi pada video deepfake tidak hanya terjadi antarpiksel` (p571) — cek sitasi [33] & [34, 35]
- ☐ `FFPP menjadi dataset utama untuk mengevaluasi performa sistem hybrid` (p802)
- ☐ `Kombinasi metrik evaluasi tersebut memberikan gambaran menyeluruh` (p1038) — cek sitasi [11, 16, 17, 28]
- ☐ `Model generatif kini semakin mampu menghasilkan video dan citra deepfake` (p1058)

## ✅ Item 7 — Hipotesis dihapus, fokus Tujuan · 🟥 P1 · SELESAI
**Keputusan user (2026-07-29):** hapus semua mention "hipotesis" → fokus ke Tujuan (hipotesa level S2). Terpasang di `.docx`:
- ✅ **Dihapus:** subbab 1.4 "Hipotesis Penelitian" (heading + H1 + H0 + intro + penutup) di BAB I
- ✅ **BAB IV** (kesimpulan): "hipotesis nol (H0) tidak dapat ditolak, karena…" → dibuang, langsung ke temuan
- ✅ **BAB V** (kesimpulan): "Mengacu pada hipotesis penelitian…H0…H1…" → "Mengacu pada **tujuan penelitian**…"
- ✅ **BAB II** (XceptionNet): "berdasarkan **hipotesis** bahwa…" → "berdasarkan **premis** bahwa…"
- **Tujuan (1.3) tidak diubah** — sudah memuat ablation study + evaluasi cross-dataset (jadi fokus).
- **Cek di Word (setelah F9):**
  - ☐ Daftar Isi: pastikan "Hipotesis Penelitian" hilang & Manfaat jadi 1.4
  - ☐ `Ctrl+F "hipotes"` = 0 hasil
  - ☐ Kesimpulan BAB IV & V mengalir tanpa H0/H1

## 🟡 Item 2 — Lengkapi referensi + JUSTIFIKASI RUMUS · 🟧 P2 · Irpan

### ✅ Audit justifikasi rumus + FreqCNN (2026-07-29) — `analyze/Item2_Audit_Justifikasi_Rumus_dan_FreqCNN_2026-07-29.md`
Verdict: sebagian besar rumus SUDAH terjustifikasi. 2 gap nyata diperbaiki → **5 placeholder sitasi DIAPPLY ke .docx (highlight kuning):**
| Placeholder | Lokasi (subbab / hal) | Konteks |
|---|---|---|
| `[Szegedy]` | §2.15.5 BCE / **hal 52** | "…teknik regularisasi **[Szegedy]** untuk mencegah…" (label smoothing pers. 2.32) |
| `[Szegedy]` | §3.5.4 / **hal 94** | "…(persamaan 2.32) **[Szegedy]** sebagai regularisasi ringan…" |
| `[Ioffe]` | §2.6.4 CNN / **hal ~28** | "…batch normalization (BatchNorm) **[Ioffe]**, yang menormalisasi…" (pers. 2.5) |
| `[Ioffe]` | §3.4.2 FreqBlock / **hal 87** | "…BatchNorm (persamaan 2.5) **[Ioffe]**." |
| `[Durall], [Qian]` | §3.4.2 FreqCNN opener / **hal 86** | kalimat baru precedent: "Penerapan CNN langsung pada representasi frekuensi telah divalidasi… [Durall], [Qian]…" |
- **Sumber:** Durall [8], Qian, Ioffe&Szegedy 2015 → SUDAH ada. Szegedy 2016 (label smoothing) ditambah.
- ✅ **DI WORD — SUDAH DIKERJAKAN (2026-07-29 malam):** Szegedy 2016 ("Rethinking the Inception Architecture") sudah masuk Daftar Pustaka; semua placeholder dikonversi jadi nomor → **BatchNorm [39]** (Ioffe, §2.6.4 + FreqBlock §3.4.2), **label smoothing [47]** (Szegedy, §2.15.5 + §3.5.4), precedent FreqCNN (Durall/Qian) bernomor. 0 placeholder tersisa; CITATION fields 318→**323**. *(Tidak perlu to-do lagi.)*
- Backup: `…_BACKUP_2026-07-29_pre-item2cites.docx`.

### Sisa item 2 — REKONSILIASI vs dokumen sekarang (cek 2026-07-29 malam):
Checklist lama sebagian **SUDAH SELESAI / OBSOLETE** setelah dicek ke .docx terbaru:
- ✅ **Sitasi Gambar 2.1/2.2** sudah dibetulkan: Gambar 2.1 = [24], Gambar 2.2 = [25] (persis rekomendasi audit v2). SELESAI.
- ✅ **Gambar arsitektur XceptionNet SUDAH ADA** = **Gambar 2.3 "Arsitektur XceptionNet"** (§2.7). Checklist lama "§2.10.1" salah nomor. SELESAI.
- ✅ **Tidak ada referensi yatim** (audit v2 §2: ke-57 sumber tersitasi). Jadi "sitasi hilang §2.3.4/2.9.4/2.11" = tidak berlaku.
- ☐ **NYATA tersisa: 55 dari 57 sumber ber-tipe "Book"** di Word citation manager (hanya 2 InternetSite). Banyak yang sebenarnya JournalArticle/ConferenceProceedings → bibliografi IEEE bisa kurang tepat (vol./pp.). Perbaiki via **Manage Sources → Edit → Type** per sumber. (Besar & fiddly; opsional untuk kualitas.)
- ☐ **(Opsional) koreksi ketepatan sitasi** audit v2 §3 (klaim ↔ paper yang benar): [7] kompresi, [9] fase/kualitas video, label "FFT" pada paper DCT/DWT, dll. Bukan diminta penguji eksplisit, tapi memperkuat.
- Audit: `analyze/Citation_Audit_v2_CORRECTED_2026-07-24_1840.md`

## ✅ Item 5 — "Probabilitas 5%" = Spectral Band Masking · 🟧 P2 · BAB III hal 79
**Dasar sudah DITULIS di laporan (hal 79)**, ditambahkan ke paragraf spectral band masking:
- Peluang 5% sengaja rendah karena artefak spektral = sinyal utama; masking terlalu sering merusak jejak generatif.
- Lebih rendah dari RandomErasing spasial (10%) karena info frekuensi lebih sensitif terhadap penghapusan.
- Prinsip masking = *dropout* → sitasi **[Srivastava]** ✅ SUDAH dipasang user (`[49]`).
- **Koreksi:** "1 hingga __ piksel" & σ TERNYATA tidak kosong — itu equation (`H/16` dan `σ=0,05`), cuma tak terbaca extractor. Tidak ada yang perlu diisi.

### Justifikasi nilai augmentasi lain (ditambah 2026-07-29, hal 79 & BAB II)
- ✅ **σ = 0,05** (noise Gaussian, hal 79): ditambah rasional "5% dari 1 std setelah z-score" + sitasi prinsip noise-injection **[Goodfellow]** (sumber sudah ada di bibliografi).
- ✅ **β = 0,15** (high-pass, BAB II def): nilai + rasional ditulis (sebelumnya nilai TIDAK ada di prosa, cuma di gambar).
- ✅ **RandomErasing 10%**: rasional + sitasi teknik **[Zhong]** (Random Erasing, PDF baru didownload).
- **Referensi per parameter:** teknik → bisa disitasi (Goodfellow/Srivastava/Durall-Zhang-Qian/Gonzalez&Woods/Zhong); NILAI spesifik (0,05·0,15·0,1·5%) → design choice, tidak ada sitasi langsung (wajar).
- ✅ **DI WORD — SUDAH DIKERJAKAN:** `[Goodfellow]` & `[Zhong]` sudah dikonversi (0 placeholder tersisa di .docx). *(Tidak perlu to-do lagi.)*

## 🟡 Item 6 — Dasar hyperparameter, INTI: batch size · BAB III hal 95 · Mustika
**Defense lengkap:** `sidang/DEFENSE_Batch_Size_dan_Hyperparameter_2026-07-29.md` (batch size 3-lapis, LR, config.yaml fix).
- ✅ **config.yaml diselaraskan (2026-07-29):** `batch_size: 16 → 64` (cocok Tabel 3.11). Koreksi: laporan ternyata bilang **max_frames = 50** (bukan 100), jadi config (50) = laporan (50) SUDAH cocok. Semua nilai config lain sudah cocok dengan laporan.
- ⚠️ Caveat terpisah: cheatsheet klaim run asli mungkin pakai ~100 frame/video (bukti: split FFPP n750 = 8.904 frame/113 video ≈ 79/video). Laporan & config sama-sama tulis 50, jadi konsisten satu sama lain, tapi mungkin understate run asli. Cek log run bila mau akurat.
- ☐ Batch 64 (efektif 128) — landasan: stabilitas BatchNorm (Xception BN-heavy), varians gradien, batch efektif tanpa biaya VRAM, generalisasi. Ref: Ioffe&Szegedy, Keskar, Goyal, Wu&He.
- ☐ LR 2e-4 (base) / 2e-5 (backbone) — discriminative fine-tuning (Howard & Ruder 2018). Checkpoint lama 1e-4 = run lama, bukan hasil skripsi.
- ✅ **Referensi didownload & di-rename** (tanpa prefix [Uncited]) di `thesis_reference/`: Ioffe & Szegedy, Wu & He, Keskar (baru); Goyal & Howard & Ruder (sudah ada). INDEX.md §H + total 50 diperbarui.
- ✅ **4 paragraf landasan SUDAH DISISIPKAN ke .docx** tepat setelah Tabel 3.11 (sebelum "Desain Eksperimen"). Penanda sitasi = teks placeholder **[Goyal] [Ioffe] [Wu] [Keskar] [Howard]**.
- ✅ **DI WORD — SUDAH DIKERJAKAN:** 5 placeholder ([Goyal] [Ioffe] [Wu] [Keskar] [Howard]) sudah dikonversi (0 tersisa di .docx). *(Tidak perlu to-do lagi.)*

## ⚪ Item 4 — Pertimbangkan penerapan studi komparatif · 🟩 P3 · Mustika
- ☐ Tinjau apakah penerapan framing "studi komparatif" sudah tepat/terjustifikasi di seluruh TA (terkait item 1). Sifatnya "pertimbangkan", bukan wajib ubah.

## ⚪ Item 8 — Karakteristik dataset + KEADILAN SAMPLING · 🟩 P3 · Irpan
**Statement penguji (diperjelas user 2026-07-29):** *"Kalian mengambil 50:50, gimana kalau ada video yang pelatihannya tidak mengambil hingga max frame, atau misalnya pada video pendek, jadinya kan gak adil?"*
→ Konteks: di sidang jawaban "kami bagi 50:50 di level video, frame harusnya tetap adil" **DITOLAK** (klaim tanpa bukti).

### 📊 BUKTI EMPIRIS (dari `outputs/roc_cm/*_preds_*.csv`, per-frame test split)
| Split | Frame | Real | Fake | Frame/video |
|---|---|---|---|---|
| FFPP n750 | 9.220 | 52,1% | 47,9% | 82 |
| CDF n750 | 7.419 | 53,4% | 46,6% | 66 |
| FFPP n500 | 5.741 | 50,1% | 49,9% | 77 |
| CDF n500 | 4.938 | 52,4% | 47,6% | 66 |

**Temuan:** (1) Frame-level = **~52:48** (bukan 50:50) — penguji BENAR, tapi simpangan KECIL (2–4 pp). Video-level 50:50 terverifikasi (375 real + 375 fake untuk n750). (2) **max_frames sebenarnya = 100, BUKAN 50** — 66–82 frame/video mustahil kalau cap 50. Laporan & config salah tulis 50.

**Jawaban revisi (akui → ukur → pertahankan):** akui frame-level ~52:48; jelaskan kecil karena mayoritas video capai cap 100 + fake diturunkan dari real (durasi berpasangan); tidak material + AUC tahan imbalance ringan; penyempurnaan = samakan frame/video atau agregasi level-video.

### 🗂️ Karakteristik dataset (tambahan Pak Irpan, 2026-07-29): bukan cuma 50:50, tapi detail dataset
Pak Irpan mau: sumber origin, FPS asli, resolusi, skala — dijelaskan. **Audit §3.2:** ADA = sumber(sitasi), metode, kompresi, jumlah dipakai. **HILANG = resolusi, FPS native, detail origin, skala penuh.**
**Fakta dari paper (terverifikasi):** FFPP [7] = 1.000 video YouTube, 509.914 frame (~510/video), 4 metode, kompresi raw/c23/c40, FPS bervariasi. CDF [18] = 590 asli + 5.639 fake, YouTube selebriti, **30 FPS ~13 detik**, >2 juta frame. Resolusi keduanya bervariasi → crop 224×224.
- ✅ **HTML tabel dibuat:** `documents/table/tabel_3_1_karakteristik_dataset.html` (letak: setelah §3.2.2, sebelum §3.2.3 → jadi Tabel 3.1, sisanya geser +1)
- "Bervariasi" (FFPP FPS) OK — dinetralkan karena ekstraksi diseragamkan 5 FPS untuk kedua dataset.

### Edit `.docx` item 8 — SUDAH DIAPPLY 2026-07-29 (semua di-highlight kuning):
- ✅ **A** — paragraf keadilan sampling (~52:48) di §3.2.4
- ✅ **B** — max_frames 50→100 (3 narasi §3.2 + config.yaml)
- ✅ **C** — BAB I ruang lingkup: 50:50 "diterapkan pada level video"
- ✅ **D** — kalimat pengantar Tabel 3.1 di §3.2
- ✅ **RETROACTIVE HIGHLIGHT** — semua ~40 revisi sebelumnya di-highlight kuning (303 run total)
- ✅ **DI WORD (kamu) — SUDAH DIKERJAKAN:** 2 tabel HTML sudah di-paste (terverifikasi di .docx: 36 tabel, kata kunci "Karakteristik", "Komposisi", "509", "590" ada). *(Tidak perlu dianggap to-do lagi.)*

## 🟨 CATATAN HIGHLIGHT (KUNING)
Semua revisi Claude di `.docx` **di-highlight KUNING** (~280 run; diubah dari merah 2026-07-29 biar lebih readable) → gampang dicek. Setelah review & setuju, hapus highlight: **Select All → Text Highlight Color → No Color**.

## ➡️ TANDA PANAH → KATA (permintaan penguji, 2026-07-29)
**Komentar penguji:** *"iya, soalnya pakai tanda panah, jadi membingungkan."*
**Scope (dipilih user):** ganti panah **cross-dataset** + **prosa-definisi** jadi kata; **notasi arsitektur/dimensi tetap** (jelas & standar).
**SUDAH DIAPPLY ke .docx (2026-07-29):** 33 panah diganti (dari 52 → sisa 19). Integritas terverifikasi identik backup (2751 paragraf, 36 tabel, 318 sitasi, 288 highlight — cuma panah yang berubah).
- ✅ **Cross-dataset (22):** `FFPP→CDF` → **"FFPP ke CDF"**, `CDF→FFPP` → "CDF ke FFPP", `FFPP→FFPP`/`CDF→CDF` → "…ke…", `FFPP↔CDF` → **"FFPP dan CDF"**. (BAB I Tujuan, §hasil BAB IV, caption Gambar 4.10, sel tabel.)
- ✅ **Prosa-definisi (4):** confusion matrix `TP = 180 → deepfake…` → **"TP = 180, yaitu deepfake…"** (TP/FP/TN/FN).
- ✅ **Prediksi (1):** `p>0,5 ⇒ fake` → "…**berarti** fake".
- ⏸️ **TETAP panah (19 — sengaja, notasi standar):** `Conv(1→64)`, `Linear(512→256)`, `Squeeze 512→128`, `Excitation 128→512`, dll.
- ⚠️ **3 borderline yang AKU BIARKAN** (notasi tapi ada di prosa — bilang kalau mau diubah juga):
  1. warmup LR `10% → 100% linear`
  2. konversi warna `BGR→RGB`
  3. pipeline preproses `RGB → 224×224 → normalisasi ImageNet; FFT → log-magnitude → …`
- **Catatan:** perubahan panah **TIDAK di-highlight** (33 sisipan kata "ke"/"yaitu" kecil-kecil → kalau di-highlight malah berantakan). Kalau mau di-highlight juga, bilang.
- Backup: `…_BACKUP_2026-07-29_pre-arrows.docx`.

## 🗂️ RENAME ASET /table & /media_v2 → sesuai nomor laporan (2026-07-29)
Nama file lama pakai nomor draft lama (tidak sinkron). Semua di-`git mv` agar nomor cocok laporan (ground truth diambil dari caption .docx). Reversible (git).
- **/table:** 32 file kini 1:1 dengan Tabel 1.1–4.5 (hanya Tabel 3.6 tak ada file = tabel sederhana diketik langsung). Contoh koreksi besar: `tabel_2_9_perbandingan_spasial_frekuensi` → **Tabel 2.1**; semua Tabel 2.x & 3.x/4.x digeser ke nomor benar. **11 file duplikat/stale → `documents/table/_archive/`** (dipilih yang mtime terbaru sebagai kanonik).
- **/media_v2:** 24 file (png+drawio) kini cocok Gambar 3.2–4.11. Contoh: `gambar_4_x_auc_in_vs_cross`→**4.8**, `gambar_4_8_scaling_auc`→**4.9**, `gambar_4_9_confusion`→**4.10**, `gambar_4_10_kurva`→**4.11**.
- ✅ **`gambar_3_4_flowchart_preprocessing` ternyata = Gambar 3.1** (flowchart utama pipeline START→END, dicek visual) → di-rename jadi `gambar_3_1_flowchart_pipeline.png/.drawio`. Sisa `Untitled Diagram.drawio` = scratch, dibiarkan.
- Raw frame dataset ada di `media_v2/media/`: `ffpp_original.png`, `ffpp_deepfaked.png`, `cdf_deepfaked.png` (+ montage `gambar_3_2_frame_real_fake.png`).

## ✅ PERMINTAAN PENGUJI BARU (2026-07-29) — sampel gambar dataset di BAB 2 — SELESAI (2026-07-30)
Penguji minta **sampel gambar dataset ditaruh juga di BAB 2** (sebelumnya cuma di BAB 3 = Gambar 3.2). **SUDAH DISISIPKAN ke .docx:**
- **Gambar 2.4** "Contoh Frame Real dan Palsu dari Dataset FaceForensics++" di **§2.9** (setelah paragraf "FFPP terdiri dari dua komponen utama…").
- **Gambar 2.5** "Contoh Frame Real dan Palsu dari Dataset Celeb-DF v2" di **§2.10** (setelah paragraf "Celeb-DF terdiri dari dua versi…").
- 2 figur dirakit sendiri (panel "Asli | Palsu (deepfake)") dari raw frame → disimpan ke `media_v2/gambar_2_4_sampel_ffpp.png` & `gambar_2_5_sampel_celebdf.png`.
- Caption pakai style Caption + field SEQ (auto-number) yang disalin dari Gambar 2.3, jadi nomor & Daftar Gambar ikut ter-update **saat Ctrl+A→F9**. Embedding gambar mengikuti struktur Word (rId63/64 → image90/91.png); integritas terverifikasi (parses, zip ok, rel resolve, +4 paragraf, sitasi/tabel utuh).
- Backup: `…_BACKUP_2026-07-30_pre-figs.docx`.
- ☐ **DI WORD (kamu):** buka dokumen → **Ctrl+A → F9** supaya nomor Gambar 2.4/2.5 fix + Daftar Gambar nambah 2 entri. Cek ukuran/posisi gambar (lebar ±13 cm, bisa di-resize di Word kalau perlu).

## ✅ SAPU BERSIH TITIK-KOMA (;) DI PROSA (2026-07-30) — [[gaya-tulisan-skripsi-no-dash-semicolon]]
User: jangan pakai ";". Diperiksa SEMUA. Dari 30 ";" di prosa, **21 diperbaiki** (jadi koma / titik+kapital / ", sedangkan" / " dan" / restrukturisasi): termasuk legendaku (3), mean/std, keadilan sampling, hflip, freqdepth, SE gate, warmup, loss, batch cells, pipeline preproses, fluktuatif, generalization drop, dll. Integritas verified (2759 paragraf, 36 tabel, 323 sitasi — hanya teks berubah). Backup: `…_BACKUP_2026-07-30_pre-semicolon.docx`.
- ⏸️ **3 sengaja DIPERTAHANKAN:** (a) baris **"Kata kunci"** & (b) **"Keywords"** — ";" itu pemisah kata-kunci standar di abstrak; (c) referensi **Geirhos** — ";" ada di JUDUL ASLI paper ("...biased towards texture; increasing shape bias...") → mengubahnya = memalsukan sitasi.
- ℹ️ ";" di dalam PERSAMAAN (pemisah baris matriks 4×4 di contoh perhitungan) = notasi matematika sah, tidak disentuh.
- ☐ (opsional) mau baris Kata kunci/Keywords diganti pemisah koma juga? Bilang saja.

## ✅ LEGENDA RUMUS DFT — pertanyaan dosen "J itu apa?" (2026-07-30)
Dosen menanyakan formula `e^{−j·2π((x+y)/4)}` ("J itu apa, rumus untuk apa?"). Temuan: formula umum SUDAH ada = **Persamaan 2.1 (BAB II)** `F(u,v)=ΣΣ f(x,y)·e^{−j·2π(ux/M+vy/N)}` (gambar dosen = **Persamaan 3.4** contoh perhitungan F(1,1) matriks 4×4). TAPI **tidak ada legenda "di mana…"** → `j` tak pernah didefinisikan. **SUDAH DIPERBAIKI:** disisipkan paragraf legenda (highlight kuning) tepat setelah Persamaan 2.1, mendefinisikan f(x,y), F(u,v), M, N, dan **j = satuan imajiner (√−1)** + rumus Euler `e^{−jθ}=cos θ − j sin θ`. Integritas terverifikasi (+1 paragraf, sitasi 323 utuh). Backup: `…_BACKUP_2026-07-30_pre-legend.docx`.
- ☐ (opsional) tambah penyebutan singkat `j` di contoh BAB III (persamaan 3.1–3.4) kalau mau konsisten — belum dilakukan.

## ♻️ INSIDEN CLOBBER (2026-07-29, malam) — arrows + item-2 cites ditimpa lalu dipasang ulang
Word (yang masih terbuka di background) AutoSave jam 22:27 menimpa 2 tulisan terakhirku → arrows balik ke 52, placeholder [Szegedy]/[Ioffe]/[Durall]/[Qian] hilang, highlight balik 288. **Sudah dipasang ulang** saat dokumen benar-benar tertutup (arrows 19, placeholder lengkap, hl 293, terverifikasi di disk).
**⚠️ PENCEGAHAN:** waktu buka Word buat konversi 4 nama item-2, kerjakan dalam **satu sesi** lalu **Cmd+Q total** (bukan cuma tutup window — di Mac window ditutup ≠ app keluar). Selama itu Claude tidak menulis file lagi, jadi tidak akan bentrok.

## 🛠️ INSIDEN & PERBAIKAN FORM FIELD (2026-07-29)
Seluruh dokumen (2754 paragraf) ternyata terbungkus **satu FORMTEXT form field raksasa** (`Text1`, artefak template lama) → itu sebabnya muncul: background abu-abu, double-click di mana saja = form field, protection "Filling in forms" auto-nyala. **SUDAH DIPERBAIKI TOTAL:** form field dihapus (begin+separate+end), documentProtection dihapus, fldChar balanced (711/711/711), 0 ffData/FORMTEXT, konten & sitasi utuh.

---

## ✅ SUDAH TERPASANG di .docx — daftar CEK di Word (Item 3, 25 edit)
Ctrl+F frasa → pastikan kalimat enak dibaca & sitasi/italic utuh.

### BAB II — Kajian Literatur
| Cari frasa (Ctrl+F) | Perubahan | Dicek |
|---|---|---|
| `Perkembangan teknologi generatif seperti GAN membuat` | buang "sangat krusial…di era media generatif" | ☐ |
| `Dalam pembuatan deepfake, GAN dimanfaatkan` | ganti "Dalam konteks ini" | ☐ |
| `Artefak yang muncul akibat proses pembangkitan GAN inilah` | buang "Dengan demikian" | ☐ |
| `Dengan cara ini, seluruh informasi spasial dan frekuensi` | variasi konektor | ☐ |
| `Oppenheim dan Lim ` | hapus titik nyasar "Lim." | ☐ |
| `FDA berperan penting dalam` | ganti "memainkan peran penting" | ☐ |
| `deep learning juga digunakan untuk pendeteksiannya` | ganti "berperan penting" | ☐ |
| `Pada video deepfake, distorsi spektral temporal merupakan ciri` | buang "ciri esensial…memperkuat pentingnya" | ☐ |
| `Depthwise convolution memproses setiap kanal secara terpisah` | ganti "menyoroti…dengan baik" | ☐ |
| `menjadi dataset utama untuk mengevaluasi performa sistem hybrid` | buang metafora "backbone penting" | ☐ |
| `menjadi sangat menentukan ketika diuji pada dataset ini` | ganti "sangat krusial" | ☐ |
| `Oleh sebab itu, kombinasi analisis spasial dan frekuensi memberikan pendekatan yang lebih menyeluruh` | buang "secara signifikan/Dengan demikian/komprehensif" | ☐ |
| `Karena itu, analisis video melibatkan pemrosesan frame-level` | variasi "Dengan demikian" | ☐ |
| `Normalisasi meningkatkan stabilitas pelatihan dan mempercepat konvergensi model sekaligus` | rapikan "tidak hanya…tetapi juga" | ☐ |
| `Atas dasar itu, FFT menjadi pilihan yang efektif dan efisien` | variasi "Dengan demikian" | ☐ |
| `pemilihan metode optimasi yang tepat menjadi penting karena` | ganti "sangat penting" | ☐ |
| `Evaluasi kinerja model merupakan tahap penting` | ganti "tahap krusial" + "semakin…semakin" | ☐ |
| `Hal ini penting pada skenario forensik digital` | ganti "sangat penting" | ☐ |
| `Dengan hasil tersebut, model berada dalam kategori performa baik` | variasi "Dengan demikian" | ☐ |
| `Nilai recall sangat penting karena` | ganti "sangat krusial" | ☐ |
| `Analisis ini penting terutama pada skenario cross-dataset` | ganti "sangat penting" | ☐ |
| `Hal ini menjelaskan mengapa model deteksi` | ganti "Temuan ini" | ☐ |
| `Konsep cross-dataset generalization menegaskan bahwa` | buang "Secara keseluruhan" | ☐ |
| `Atas dasar itu, FFT dipilih karena mampu mendeteksi artefak tersembunyi` | buang triad "efisien, umum, dan…" | ☐ |

### BAB III — Tahapan Pelaksanaan
| Cari frasa (Ctrl+F) | Perubahan | Dicek |
|---|---|---|
| `Pemilihan dataset merupakan langkah penting` | ganti "langkah krusial" | ☐ |
| `Pada penerapan nyata, detektor deepfake menghadapi` | (BAB I) ganti "Di luar laboratorium…" | ☐ |

---

## 🔧 Catatan terpisah (formatting/field, bukan wording)
- ☐ Placeholder rumus kosong `()` di p1044 & p1443 — field persamaan tidak ter-render (Ctrl+A → F9, atau isi ulang simbol).

## 💾 Backup .docx (di folder OneDrive Thesis) — DIBERSIHKAN 2026-07-30
17 backup intermediate lama dihapus (313 MB dibebaskan). **Tersisa 4** (safety net memadai; dokumen sudah diverifikasi sehat):
- `…_BACKUP_2026-07-29.docx` — **PRISTINE, sebelum semua edit** (fallback utama)
- `…_BACKUP_2026-07-30_pre-figs.docx` — sebelum sisip Gambar 2.4/2.5 (snapshot awal sesi 30/7)
- `…_BACKUP_2026-07-30_pre-legend.docx` — sebelum legenda rumus DFT
- `…_BACKUP_2026-07-30_pre-semicolon.docx` — sebelum sapu-bersih titik-koma (paling baru)
> Backup yang dihapus masih bisa dipulihkan dari OneDrive Recycle Bin bila perlu.

## ✔️ Checklist verifikasi cepat
- ☐ Buka `.docx` di Word — pastikan tidak korup
- ☐ Ctrl+A → F9 (refresh field) — sitasi `[n]` & Daftar Pustaka tetap benar
- ☐ Spot-check paragraf Item 1 & beberapa dari daftar "cek di Word"
- ☐ Kurang sreg? edit langsung di Word (semua backup aman)
