# Audit Mendalam Tesis — Kompatibilitas Kode, Kelengkapan Reviewer, dan Integritas Referensi

**Peran:** Dosen penguji melakukan *in-depth analysis*.
**Tanggal:** 2026-06-02
**Dokumen diaudit:** `.docx` OneDrive (tersimpan 2 Jun 2026, 20:25) — diekstrak ke `/tmp/dchk/plain.txt`
**Sumber kebenaran:** kode `deepfake_hybrid/`, `documents/reviewer_feedback/`, `thesis_reference/` (40 PDF).
**Metode:** ekstraksi penuh `word/document.xml`, pemetaan 39 *citation field* → 45 entri Daftar Pustaka, pembacaan PDF sumber, audit baris-demi-baris kode vs narasi.

---

## RINGKASAN EKSEKUTIF (verdict penguji)

Tiga temuan tingkat **kritis** harus diselesaikan sebelum sidang:

1. **🔴 Korupsi nomor sitasi sistemik.** Hampir semua penanda `[N]` di badan teks **tidak cocok** dengan Daftar Pustaka. Contoh: 17 sitasi Rössler ter-render **[19]** (= Chadha). Tag-nya benar, tetapi nomor tampilannya basi. **Wajib di-*refresh*** (Update Fields / Mendeley refresh) sebelum cetak.
2. **🔴 v4 (sinkronisasi kode) tidak pernah masuk ke `.docx`.** Enam+ parameter metodologi di `.docx` masih nilai lama (pra-v4) dan **bertentangan dengan kode** yang menghasilkan BAB IV.
3. **🔴 Satu angka fabrikatif + satu salah label metrik.** "XceptionNet 96,36% (Rössler)" tidak ada di paper Rössler (nilai asli 99,26/95,73/81,00) **dan** bertentangan dengan kalimat lain di tesis sendiri ("99,26% AUC" — yang juga salah label: itu *accuracy*, bukan AUC).

Selebihnya: mayoritas masukan reviewer **sudah** ditangani; beberapa item kecil masih terbuka (rename 2.20.1, dll.).

---

# POIN 1 — Kompatibilitas `.docx` ↔ Kode (DETIL)

## 1A. Temuan inti: v4-sync tidak ter-porting ke `.docx`

Commit `f8d16da` ("BAB III v4") mendokumentasikan 13 sinkronisasi narasi→kode **dalam file markdown** `documents/BAB_III_Tahapan_Pelaksanaan_v4.md`. **Namun `.docx` live tidak pernah menerima perubahan ini.** Diverifikasi langsung — `.docx` masih memuat nilai lama:

| # | Parameter | `.docx` (sekarang) | Kode (sumber kebenaran) | Severity |
|---|---|---|---|---|
| C1 | Hybrid classifier **dropout** | `Dropout(0,3)` ×2 (sec 3.4.3) | `nn.Dropout(0.5)` ×2 — `hybrid_fusion.py:49,53` | 🔴 Kritis |
| C2 | **Label smoothing** | "dinonaktifkan (α=0)" (sec 3.5.4) | `config.yaml:17 label_smoothing: 0.05` (AKTIF) | 🔴 Kritis — klaim berlawanan |
| C3 | **Early stopping patience** | "10 epoch" (sec 3.5.8, Tabel 3.10) | `config.yaml:15 early_stop_patience: 12` | 🔴 Kritis |
| C4 | **Linear warmup** | "2 epoch", `total_iters=2`, `T_max=max(epochs−2,1)` | `train.py:248` warmup **3**, `T_max=max(epochs−3,1)` | 🔴 Kritis — kurva LR & contoh salah |
| C5 | **FreqCNN base_channels** | "32, progresi [32,64,128,256,256]", feat_dim 256, ~700K (sec 3.4.2, Tabel 3.5/3.6/3.7/3.8) | `config.yaml:23 freq_base_channels: 64` → [64,128,256,512,512], feat_dim **512**, ~4,2 jt param | 🔴 Kritis — bila 64 dipakai untuk BAB IV, seluruh tabel FreqCNN & param hybrid salah |
| C6 | **High-pass filter FFT** | TIDAK ADA di sec 3.3.2 (eq 3.2–3.4 = `log1p(\|F\|)` polos) | `fft_utils.py:9-33` menerapkan *Gaussian high-pass mask* (`cutoff=0.15`) **sebelum** log1p; cache `.npy` = `log1p(\|F\|·mask)` | 🔴 Kritis — representasi FFT aktual ≠ semua persamaan/contoh di 3.3.2 |
| C7 | **Differential LR (hybrid)** | Tabel 3.9 = **2 grup** (backbone, head) | `train.py:209-213` = **3 grup** (backbone base/10, cabang freq base×0,25 = 5×10⁻⁵, head base) | 🟠 Sedang |
| C8 | FFT stats: "metode **Welford**" | klaim Welford | `compute_fft_cache.py:46-55` single-pass sum/sum-sq (BUKAN Welford) | 🟡 Minor (nama salah) |

> **Catatan penting:** semua C1–C6 **sudah** dijelaskan benar di `BAB_III_Tahapan_Pelaksanaan_v4.md` + `BAB_III_v4_CHANGELOG.md`. Tindakannya bukan menulis ulang dari nol — cukup **porting v4 ke `.docx`** (lihat Poin 3).

## 1B. Yang SUDAH cocok (kode ↔ docx) — tidak perlu diubah

Diverifikasi MATCH: fps=5, max 50 frame, formula interval, MTCNN (`min_face_size=60`, `thresholds=[0.6,0.7,0.7]`, margin 0.3, pilih wajah terbesar, fallback full-frame), grayscale BT.601, DFT+fftshift, magnitude, z-score norm, σ noise 0.05, band masking p=5% lebar 1–⌊H/16⌋, augmentasi RGB (Resize 256, RRC 224 scale 0.8–1.0, ColorJitter b/c=0.2 s=0.1 h=0.05, RandomErasing p=0.1 scale 0.02–0.15, ImageNet norm), hflip konsisten hybrid, XceptionNet via timm + feat 2048, PROJ_DIM 256, concat 512, SE reduction=4 (512→128→512), AdamW, lr 2e-4, backbone lr 2e-5, wd 1e-4, batch 16, accum 2 (efektif 32), pos_weight, grad clip 5.0, freeze 3 epoch, eta_min 1e-6, max 30 epoch, AMP+TF32, seleksi val-AUC, split 70/15/15 seed 42 stratified, min 4/kelas.

---

# POIN 2 — Kelengkapan terhadap Reviewer Feedback (DETIL)

Kedua reviewer (Pembanding 1: nilai 70; Pembanding 2: nilai 78). Pemetaan setiap butir → status di `.docx` sekarang:

## Pembanding 1
| Butir | Status |
|---|---|
| 1. LB terlalu luas, pertajam masalah; apakah meningkatkan kinerja XceptionNet? | ✅ Ditangani (rewrite B.1–B.5) |
| 2. RM kurang jelas (solusi vs masalah) | ✅ Ditangani (B.6) |
| 3. Tujuan duplikasi RM | ✅ Ditangani (B.7) |
| 4. Manfaat tanpa implementasi | ✅ Ditangani (B.8) |
| 5. Ruang lingkup: kriteria dataset, citra/video | ✅ Ditangani (B.9, D.1) |
| 6a. **Tiap gambar & tabel BAB 2 harus ada sitasi** | ⚠️ **PERLU CEK MANUAL** — verifikasi tiap caption gambar/tabel BAB II punya sitasi (banyak figur baru) |
| 6b. Arsitektur algoritma kurang jelas, terlalu naratif | ✅ Sebagian (gambar arsitektur ditambah) |
| 6c. **Rumus sesuai pedoman TA** | ⚠️ **PERLU CEK** format penomoran/penyajian rumus vs Pedoman 2025 |
| 7a. Flowchart & detail algoritma (bukan sekadar "pakai library") | ✅ Ditangani (pseudocode D.2; tapi lihat C6 — high-pass tak terdokumentasi) |
| 7b. **"Kenapa tidak ada analisis sistem?"** | ✅ Ditangani (subbab 3.8 Analisis Sistem) |

## Pembanding 2
| Butir | Status |
|---|---|
| 1.1 Paragraf 2 LB gabung ke 1 (5–7 kalimat/paragraf) | ✅ (B.1) |
| 1.2 Paragraf 5 "sejumlah penelitian" hanya 1 sitasi | ✅ (B.3) |
| 1.3 Kontradiksi paragraf 7 vs 8 | ✅ (B.5) |
| 1.4 Urgensi generalisasi lintas-dataset di LB | ✅ (B.4) |
| 2.1 RM turunan dari LB; 2.2 hapus "citra atau video" | ✅ (B.6) |
| 3. Tujuan — oke | ✅ |
| 4. Manfaat "andal & akurat"; kontradiksi kecepatan | ✅ (B.8) |
| 5. Sitasi link dataset + total dataset | ✅ (B.9, D.1) |
| 6a. **Banyak paragraf < 5 kalimat** | ⚠️ **PERLU CEK MENYELURUH** — masih banyak paragraf pendek? |
| 6b. **2.2.3 contoh frame artefak spasial & frekuensi** | 🟠 **Sebagian** — contoh frame ada di BAB III (Gambar 3.2 real/fake, 3.4 FFT real vs fake) tapi reviewer minta di **2.2.3 (BAB II)**. Pertimbangkan menautkan/menyalin contoh ke 2.2.3 |
| 6c. 2.3.4 sitasi "2 strategi utama" | ✅ (C.1) |
| 6d. 2.9.4 sitasi DSC | ✅ (C.2) |
| 6e. 2.10.1 gambar arsitektur XceptionNet | ✅ Ada (Gambar 2.3 Arsitektur Xception) |
| 6f. 2.11.1/2.11.2 sitasi SE | ✅ (C.4) |
| 6g. **Rename 2.20.1** | ❌ **BELUM** — masih "Mengapa Cross-GAN Sulit" (C.5 belum diterapkan) |
| 6h. Subbab 1-paragraf → jadikan poin a,b,1,2 | ⚠️ **PERLU CEK** struktural |
| 7.1 Total tiap dataset | ✅ (D.1) |
| 7.2 "3 arsitektur" vs 1 arsitektur usulan | ✅ (D.3 reframe) |
| 7.3 Arsitektur 3.4.3 + posisi Gambar 3.8 | ✅ (D.4 dipindah ke awal 3.4.3) |
| 7.4 Contoh citra tiap step augmentasi | ✅ (Gambar augmentasi RGB ditambah) |

**Item reviewer yang MASIH terbuka:** rename 2.20.1 (❌); sitasi tiap gambar/tabel BAB II (⚠️ cek); rumus sesuai pedoman (⚠️ cek); paragraf <5 kalimat (⚠️ cek); contoh artefak di 2.2.3 (🟠); subbab 1-paragraf → poin (⚠️).

---

# POIN 4 — Integritas Referensi (DETIL)

## 4A. 🔴 Korupsi nomor sitasi (TEMUAN UTAMA)

*Citation field* Word menyimpan **tag** (benar), tapi nomor `[N]` yang ditampilkan **basi/tidak sinkron** dengan Daftar Pustaka. Tag yang sama bahkan render beda-beda:

| Tag (maksud penulis) | Render `[N]` (frekuensi) | Seharusnya | `[N]` yang muncul itu sebenarnya = |
|---|---|---|---|
| `Rös19` Rössler | **[19] ×17**, [7] ×3 | [7] | **[19] = Chadha** |
| `Dur` Durall | **[7] ×15**, [8] ×5, [7,8] ×8 | [8] | **[7] = Rössler** |
| `Ala` Alam/SpecXNet | **[9] ×10** | [13] | **[9] = Zhang** |
| `Qia20` Qian | **[13] ×8**, [11] ×2 | [11] | **[13] = Alam** |
| `Has23` Hasanaath | **[18] ×10**, [16] ×1 | [16] | **[18] = Li/Celeb-DF** |
| `LiY20` Celeb-DF | [35] ×3, [18] ×3 | [18] | **[35] = Akinrogunde** |
| `Ran22` Rana | **[10] ×11** | [14] | **[10] = Giudice** |
| `Ode16` Odena | [16] ×4 | [21] | **[16] = Hasanaath** |

**Akibat:** pembaca yang mengeklik `[19]` mengharapkan Rössler tetapi mendapat Chadha. Hampir seluruh badan teks terdampak.
**Penyebab:** Daftar Pustaka diurutkan ulang/diedit manual tanpa me-*refresh* field sitasi (cache Mendeley/Zotero rusak).
**Perbaikan:** buka di Word → *Update All Fields* (Ctrl+A → F9), atau via *reference manager* "Refresh". **Verifikasi** library reference manager masih utuh; jika tidak, nomor harus diperbaiki manual. **Ini prioritas #1.**

## 4B. 🔴 Kesalahan faktual

1. **"XceptionNet 96,36% (Rössler [19])"** — angka **96,36% TIDAK ADA** di paper FF++ (nilai asli: 99,26 raw / 95,73 HQ / 81,00 LQ). Selain itu **bertentangan** dengan kalimat lain di tesis: "XceptionNet mencapai **99,26% AUC**". → Perbaiki ke 99,26% dan hapus 96,36%.
2. **"99,26% AUC"** — 99,26 di Rössler adalah **accuracy**, bukan AUC. → Ganti label "AUC" → "akurasi". (Kalimat ini berasal dari rewrite C.3 sebelumnya — salah label dari saya, mohon dikoreksi.)
3. **Durall "lima arsitektur GAN"** — paper Durall menguji **empat** varian GAN (DCGAN, DRAGAN, LSGAN, WGAN-GP). → Ganti "lima" → "empat" (klaim konsistensi lintas-GAN tetap valid).
4. **`Lao25` → [20] Aduwala** untuk klaim *frequency-domain/dual-domain* — paper Aduwala (*GAN Discriminators*) **tidak punya konten domain frekuensi sama sekali**. Klaim itu milik **Luo & Wang [17]**. Ini gabungan dari korupsi nomor (4A) — setelah *refresh* field, pastikan tag `Lao25` memang menunjuk Luo.

## 4C. Realitas referensi (45 entri)

- **39/45 punya PDF lokal** terverifikasi nyata.
- **Nyata tapi tanpa PDF lokal (bukan fabrikasi):** [18] Celeb-DF (Li 2020), [36] SE-Net (Hu 2018), [42] Adam (Kingma 2015), [43] AdamW (Loshchilov 2019). [30] Wikimedia & [31] Stack Overflow = sumber web.
- **Orphan/hilang:** Howard (MobileNet) & Sifre — dibahas konseptual (DSC) & ada PDF, tetapi **tidak masuk Daftar Pustaka**. Pertimbangkan menambah bila DSC mengutipnya, atau hapus klaim.
- **MTCNN [44]** kini disitasi di badan (subbab 3.3.2 baru) — bagus.

## 4D. INDEX.md — SUDAH DIPERBARUI
- ✅ Ditambah entri **Zhang MTCNN** (ada di folder, tadinya tak terindeks) + kategori "K. Face Detection".
- ✅ Ditambah seksi **"Cited but NOT in folder"** (Celeb-DF, SE-Net, Adam, AdamW, web) agar tidak dikira fabrikasi.
- ✅ Total diperbarui 41 → 42; keyword MTCNN & optimizer ditambah.

---

# POIN 3 — Apa yang Perlu Ditambah / Dikurangi ke `.docx`

## DITAMBAH
1. **Porting seluruh v4-sync** (C1–C7) dari `BAB_III_Tahapan_Pelaksanaan_v4.md` → `.docx`: dropout 0,5; label smoothing 0,05 (aktif); patience 12; warmup 3 + T_max=epochs−3; FreqCNN base 64 + tabel FreqCNN/param hybrid dihitung ulang; subbab high-pass filter (eq 3.4) + perbaiki eq/contoh 3.3.2; grup LR ke-3 (cabang freq) di Tabel 3.9. **(Sudah ada draftnya di v4 — tinggal salin.)**
2. **Sitasi yang hilang** pada tiap gambar/tabel BAB II (butir reviewer 1.6a).
3. (Opsional) contoh frame artefak di **2.2.3** (reviewer 2.6b).

## DIKURANGI / DIPERBAIKI
1. **Angka "96,36%"** → hapus, ganti 99,26%; label "AUC"→"akurasi"; "lima GAN"→"empat".
2. **Klaim "Welford"** → ganti "akumulasi satu-lintasan (sum & sum-of-squares)".
3. **Rename 2.20.1** "Mengapa Cross-GAN Sulit" → "Faktor Penyebab Kesulitan Generalisasi Cross-GAN".
4. **Subbab 1-paragraf** → ubah jadi poin (reviewer 2.6h).

## TINDAKAN MEKANIS (paling penting, bukan tulis-menulis)
- **Refresh seluruh field sitasi** agar `[N]` cocok Daftar Pustaka (4A) — **PRIORITAS #1**.
- **Update All Fields (F9)** untuk penomoran tabel/gambar/persamaan & Daftar Isi setelah semua edit.

---

## DAFTAR PRIORITAS (untuk kandidat)

| Prioritas | Aksi | Rujukan |
|---|---|---|
| 🔴 P1 | Refresh field sitasi — perbaiki korupsi nomor `[N]` | 4A |
| 🔴 P2 | Porting v4-sync ke `.docx` (dropout/smoothing/patience/warmup/freq-channels/high-pass) | 1A, `v4_CHANGELOG` |
| 🔴 P3 | Perbaiki 96,36% / label AUC / "lima GAN" | 4B |
| 🟠 P4 | Rename 2.20.1; cek sitasi gambar/tabel BAB II; rumus per pedoman | Poin 2 |
| 🟡 P5 | "Welford"; subbab 1-paragraf→poin; contoh artefak 2.2.3; Howard/Sifre di Daftar Pustaka | 1A-C8, 2, 4C |

---

*Catatan metodologi: angka render `[N]` diambil dengan menyelaraskan `<w:instrText>` (tag CITATION) dengan teks tampil setelah `fldChar separate` di `word/document.xml`. Klaim faktual diverifikasi terhadap PDF asli di `thesis_reference/`. Audit kode menelusuri `config.yaml`, `src/`, dan `scripts/train.py` baris-demi-baris.*
