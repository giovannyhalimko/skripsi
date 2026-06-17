# HANDOFF — Finalisasi BAB II, III, IV (Skripsi Deepfake Hybrid)

**Tanggal:** 2026-06-17
**Tujuan:** daftar tugas lengkap + recap perubahan untuk menuntaskan BAB II–IV pada dokumen WORD.
**Dokumen final:** OneDrive `REVISI V1 - Metode Peningkatan Deteksi Deepfake ... .docx`
**Hasil yang di-settle:** commit `d28efae` → `deepfake_hybrid/results_vast_20260609/` (3 model × 2 dataset × tier n100/250/500/750 × 3 seed). **JANGAN ganti angka hasil** tanpa kesepakatan tim.
**Arah judul (komparatif):** "Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet–FFT terhadap Model Domain Tunggal".

> Dokumen rujukan terkait (sudah ada di repo):
> - Rencana BAB IV: `documents/BAB_IV_STRUCTURE_PLAN_2026-06-15.md`
> - Naskah BAB IV: `documents/BAB_IV_Hasil_dan_Pembahasan_2026-06-17.md`
> - Status revisi & item value: `analyze/REVISI_V1_Status_dan_TODO_2026-06-17.md`
> - Analisis value lengkap: `analyze/REVISI_V1_Full_Analysis_and_RUMUS_Relokasi_2026-06-11_1600.md`

---

## 0. Status saat ini (hasil cek docx 2026-06-17 10:49)

**Sudah beres di docx:**
- BAB II: relokasi RUMUS dari BAB III selesai (Persamaan 2.1–2.43).
- BAB III: penomoran persamaan 3.1–3.17 (tanpa duplikat); sitasi SE gating sudah benar (Hu et al.).
- BAB IV: **naskah lengkap masuk** (4.1.1–4.2.6); **6 tabel tersisip** (4.1–4.6); **4 gambar tersisip** (4.3, 4.5, 4.7, 4.8); **9 sitasi sebagai CITATION field**; konten purwarupa/demo ada di 4.1.2.

**Masih kurang (inti pekerjaan handoff ini):** 6 gambar (4.1, 4.2, 4.4, 4.6, 4.9, 4.10), 1 sitasi hilang (Odena), penyeragaman gaya sitasi, beberapa item value, dan pembaruan front matter.

---

## 0b. ⚠️ AUDIT FINAL MENYELURUH (cek docx 2026-06-17 11:56) — PENOMORAN / SITASI / VALUE

> Banyak revisi sebelumnya **sudah diterapkan** (relokasi RUMUS, konsolidasi FFT → BAB II 2.1–2.40, BAB III 3.1–3.17, Gradio Tabel 3.16, BAB IV 4.1.2 dirampingkan). Audit final ini menyisakan **temuan berikut yang WAJIB ditangani sebelum dianggap final.**

### 🔴 A. Penomoran GAMBAR BAB IV TIDAK SINKRON (kritis)
Caption gambar BAB IV sudah dikonsolidasi menjadi **6 gambar (4.1–4.6)** — ROC, confusion matrix, dan kurva pelatihan **dihapus**. Namun **narasi masih merujuk skema lama (4.4 ROC, 4.5, 4.6 ROC, 4.7, 4.8, 4.9, 4.10)**. Gambar yang benar sekarang:
`4.1` antarmuka demo · `4.2` what-the-models-see · `4.3` bar in-dataset · `4.4` bar cross-dataset · `4.5` generalization drop · `4.6` scaling AUC.

**Pilih satu jalur penyelesaian:**
- **(B-1, disarankan) Tanpa ROC/CM/kurva pelatihan** (sesuai kondisi sekarang). Perbaiki narasi:
  - 4.1.3: **hapus** paragraf/kalimat "kurva ROC … Gambar 4.4". Sisakan rujukan **Gambar 4.3** (bar).
  - 4.1.4: ganti **Gambar 4.5 → 4.4**; **hapus** kalimat "kurva ROC … Gambar 4.6".
  - 4.1.5 (Drop): ganti **Gambar 4.7 → 4.5**.
  - 4.1.6 (Scaling): ganti **Gambar 4.8 → 4.6**.
  - **Hapus subbab 4.1.7 "Confusion Matrix dan Dinamika Pelatihan"** (gambar 4.9 & 4.10 sudah tidak ada).
  - 4.2.4: **hapus** kalimat "Stagnasi kurva pelatihan … (Gambar 4.10) …"; pertahankan rujukan **Gambar 4.2**.
- **(B-2) Tetap ingin ROC/CM/kurva pelatihan:** generate via `make_roc_cm.py` di vast (lihat §2A), sisipkan, lalu **kembalikan penomoran ke 10 gambar** dan sesuaikan caption. Lebih berat.

### 🟠 B. Sitasi
- **Odena (Ode16) masih HILANG** di 4.2.4 — kalimat sidik jari upsampling GAN seharusnya "(Durall et al., 2020; **Odena et al., 2016**)". Tambahkan field-nya.
- Seluruh **319 sitasi masih render IEEE `[N]`** — bila target (Nama, Tahun): ganti citation style di reference manager → Update All Fields.

### 🟠 C. Value
- **Tabel 3.3:** FFPP masih `100, 300, 600, 1000` → ubah `100, 250, 500, 750`.
- **Tabel 1.1 / 3.1:** klaim FFPP `n = 1000` / `1.000 video` → perjelas tier maks 750.
- **Label smoothing (Tabel 3.10):** tertulis `0,0 (nonaktif)` tetapi prosa + contoh + commit `f8d16da` = **α = 0,05 (aktif)** → perbaiki sel Tabel 3.10 menjadi **`0,05`**.

### 🟢 Sudah benar (terverifikasi)
- Persamaan BAB II 2.1–2.40 & BAB III 3.1–3.17 urut tanpa duplikat; semua rujukan "persamaan 2.x" BAB III benar pasca-renumber.
- Tabel 4.1–4.6 & captionnya urut; konsolidasi FFT benar.

*(Minor: "Tabel 4.2Hasil…" tambahkan spasi setelah "4.2".)*

---

## 1. ASET YANG SUDAH SIAP DIPAKAI

| Aset | Lokasi | Status |
|---|---|---|
| Tabel HTML BAB IV (4.1–4.6) | `documents/table/tabel_4_*.html` | ✅ siap (sudah tersisip ke docx) |
| Gambar BAB IV 4.3/4.5/4.7/4.8 (label Indonesia) | `documents/media_v2/gambar_4_{3,5,7,8}_*.png` | ✅ siap (sudah tersisip) |
| Skrip ROC + Confusion Matrix | `deepfake_hybrid/scripts/make_roc_cm.py` | ✅ teruji (perlu checkpoint n750) |
| Skrip generate gambar bar/scaling/drop | `deepfake_hybrid/scripts/make_bab4_figures.py` | ✅ teruji |
| Plot mentah hasil | `deepfake_hybrid/results_vast_20260609/plots/` (Inggris) | referensi/Lampiran |

---

## 2. TUGAS — GAMBAR YANG MASIH KURANG (BAB IV)

Penomoran gambar mengikuti naskah BAB IV. Yang sudah tersisip: **4.3, 4.5, 4.7, 4.8**. Yang masih perlu:

### 2A. ROC & Confusion Matrix (Gambar 4.4, 4.6, 4.9) — butuh mesin vast/Colab
**Hanya inferensi, TANPA training.** Prasyarat di mesin yang punya data + checkpoint:
1. Checkpoint **n750 seed0** untuk 6 kombinasi, ditaruh di `outputs/runs/{model}_{dataset}_n750_seed0/best.pt` (+ `threshold.json` bila ada): `spatial/hybrid/freq` × `FFPP/CDF`. (Ada di mesin pelatihan vast/Colab dan/atau di Space demo; lihat `deepfake_hybrid/demo/README.md`.)
2. `outputs/fft_cache/{FFPP,CDF}/fft_stats.json` tersedia (untuk normalisasi freq/hybrid).
3. `outputs/manifests/{FFPP,CDF}/test.csv` + frame test tersedia.

Jalankan 4 perintah berikut:
```bash
cd deepfake_hybrid
# ROC In-Dataset (Gambar 4.4): FFPP & CDF
python scripts/make_roc_cm.py --models spatial:outputs/runs/spatial_FFPP_n750_seed0/best.pt \
  hybrid:outputs/runs/hybrid_FFPP_n750_seed0/best.pt freq:outputs/runs/freq_FFPP_n750_seed0/best.pt \
  --test-manifest outputs/manifests/FFPP/test.csv --fft-cache-root outputs/fft_cache/FFPP \
  --tag FFPP_in_n750 --title "Kurva ROC In-Dataset FFPP (n = 750)"
python scripts/make_roc_cm.py --models spatial:outputs/runs/spatial_CDF_n750_seed0/best.pt \
  hybrid:outputs/runs/hybrid_CDF_n750_seed0/best.pt freq:outputs/runs/freq_CDF_n750_seed0/best.pt \
  --test-manifest outputs/manifests/CDF/test.csv --fft-cache-root outputs/fft_cache/CDF \
  --tag CDF_in_n750 --title "Kurva ROC In-Dataset CDF (n = 750)"
# ROC Cross-Dataset (Gambar 4.6): dua arah
python scripts/make_roc_cm.py --models spatial:outputs/runs/spatial_FFPP_n750_seed0/best.pt \
  hybrid:outputs/runs/hybrid_FFPP_n750_seed0/best.pt freq:outputs/runs/freq_FFPP_n750_seed0/best.pt \
  --test-manifest outputs/manifests/CDF/test.csv --fft-cache-root outputs/fft_cache/CDF \
  --tag FFPP2CDF_n750 --title "Kurva ROC Cross-Dataset FFPP->CDF (n = 750)"
python scripts/make_roc_cm.py --models spatial:outputs/runs/spatial_CDF_n750_seed0/best.pt \
  hybrid:outputs/runs/hybrid_CDF_n750_seed0/best.pt freq:outputs/runs/freq_CDF_n750_seed0/best.pt \
  --test-manifest outputs/manifests/FFPP/test.csv --fft-cache-root outputs/fft_cache/FFPP \
  --tag CDF2FFPP_n750 --title "Kurva ROC Cross-Dataset CDF->FFPP (n = 750)"
```
Keluaran di `outputs/roc_cm/`: `*_roc.png` (overlay 3 model) + `*_cm_{model}.png` + CSV prediksi + metrics JSON.
Pemetaan ke gambar tesis (salin & ganti nama ke `documents/media_v2/`):
- **Gambar 4.4** ← `FFPP_in_n750_roc.png` (+ `CDF_in_n750_roc.png`) → `gambar_4_4_roc_in_dataset.png`
- **Gambar 4.6** ← `FFPP2CDF_n750_roc.png` (+ `CDF2FFPP_n750_roc.png`) → `gambar_4_6_roc_cross_dataset.png`
- **Gambar 4.9** ← pilih CM representatif (mis. `FFPP_in_n750_cm_spatial.png` + `CDF2FFPP_n750_cm_hybrid.png` untuk menonjolkan keruntuhan recall) → `gambar_4_9_confusion_matrix.png`

### 2B. Tangkapan layar demo (Gambar 4.1 & 4.2) — dari HF Spaces
Buka Space `https://huggingface.co/spaces/thesissufferer/deepfake-detection-demo`, unggah satu video uji, lalu:
- **Gambar 4.1** = tangkapan antarmuka + kartu verdict 3 model → `documents/media_v2/gambar_4_1_antarmuka_demo.png`
- **Gambar 4.2** = panel "what the models see" (potongan wajah + spektrum FFT) → `documents/media_v2/gambar_4_2_what_models_see.png`

### 2C. Kurva pelatihan (Gambar 4.10)
PNG sudah ada tetapi **berbahasa Inggris**: `results_vast_20260609/plots/training_curves_{freq,spatial}_FFPP_n750.png`.
- Cepat: salin ke `documents/media_v2/gambar_4_10_kurva_pelatihan.png` (stopgap, label Inggris), ATAU
- Rapi: regenerasi versi Indonesia dari histori per-epoch (ada di mesin pelatihan).

---

## 3. TUGAS — PERBAIKAN DI DOCX (BAB IV)

1. **Tambah placeholder Gambar 4.4 yang hilang.** Saat ini docx punya penanda `[MASUKKAN GAMBAR 4.1/4.2/4.6/4.9/4.10]` tetapi **tidak ada untuk 4.4** (padahal naskah merujuk "Gambar 4.4" di subbab 4.1.3). Tambahkan caption "Gambar 4.4 Kurva ROC evaluasi in-dataset ..." pada posisi yang sesuai, lalu sisipkan gambarnya.
2. **Sisipkan 6 gambar** (4.1, 4.2, 4.4, 4.6, 4.9, 4.10) menggantikan penanda `[MASUKKAN GAMBAR …]`. Caption **di bawah** gambar, format `Gambar 4.x` (rata tengah), sesuai Pedoman.
3. **Sitasi Odena hilang.** Naskah 4.2.4 menyebut "(Durall et al., 2020; Odena et al., 2016)" tetapi pada docx hanya Durall yang tersisip sebagai field. **Tambahkan CITATION field Odena (Ode16)** pada kalimat tersebut.

---

## 4. TUGAS — SITASI (SELURUH DOKUMEN)

1. **Seragamkan gaya ke (Nama, Tahun).** Seluruh sitasi sudah berupa CITATION field tetapi masih **render IEEE [N]**. Ubah *citation style* di reference manager (Mendeley/Zotero/Word) ke gaya *author-year* (mis. APA/Harvard) → **Update All Fields**. Satu langkah, bukan edit manual.
2. ~~Verifikasi sitasi Augmentasi (BAB II).~~ ✅ **SELESAI (cek 2026-06-17):** paragraf "Augmentasi Data" kini memuat satu sitasi (Afchar et al.). Klaim "augmentasi sebagai teknik regularisasi" bersifat umum, sehingga satu sitasi pendukung sudah memadai — tidak perlu menambah Rössler.
3. Setelah ganti style, **Update Fields (Ctrl+A → F9)** seluruh dokumen untuk merefresh nomor/teks sitasi & bibliografi.

---

## 5. TUGAS — ITEM VALUE (BAB I & III) — rujuk analisis, jangan ubah angka hasil

Detail di `analyze/REVISI_V1_Full_Analysis_…_2026-06-11_1600.md` & PLAN. Yang masih ada di docx:
1. **Tabel 3.3 / variasi ukuran sampel:** FFPP masih tertulis `100, 300, 600, 1000` → seharusnya `100, 250, 500, 750` (sesuai hasil final). (`100, 300, 600, 1000` muncul 2× di docx.)
2. **Tabel 1.1 / Tabel 3.1:** klaim FFPP `n = 1000` / ~50.000 frame → perjelas bahwa tier maksimum yang dijalankan = 750.
3. **Label smoothing tidak konsisten:** Tabel 3.10 menulis `0,0 (nonaktif)`, sedangkan contoh perhitungan Fungsi Loss (BAB III) memakai `α = 0,05`. Samakan keduanya.
4. **Framing BAB I:** lunakkan klaim "fusi bermanfaat/meningkatkan" pada Latar Belakang & paragraf penutup agar selaras dengan judul komparatif & temuan negatif (lihat PLAN §1–2).

---

## 6. TUGAS — DEPLOYMENT: INFERENSI & PURWARUPA (BAB III) + PENYESUAIAN BAB IV

> **Prinsip:** inferensi & purwarupa **dijelaskan (metode) di BAB III**; BAB IV **hanya menyajikan hasilnya**, tanpa mengulang metode. **BAB III tidak boleh merujuk BAB IV.** Semua teks siap-tempel ada di `documents/REVISI_BAB_II_III_Deployment_FFT_2026-06-17.md`.

1. **Tabel 3.16 (Perangkat Lunak):** tambah baris **Gradio** + **opencv-python-headless**. ✅ **HTML siap:** `documents/table/tabel_3_16_kebutuhan_perangkat_lunak.html` → Copy Table → ganti tabel lama.
2. **BAB III — sub-bab baru "Skema Inferensi dan Purwarupa Sistem" (WAJIB).** Sisipkan di bagian Analisis Sistem (antara Konfigurasi Pipeline dan Keluaran Sistem). Teks siap-tempel di file revisi. Tidak boleh merujuk BAB IV.
3. **BAB IV — rampingkan sub-bab 4.1.2.** Ganti deskripsi metode (alur 5 FPS, MTCNN, agregasi, ambang) dengan versi **hasil-saja** (purwarupa beroperasi + panel FFT yang dianalisis di 4.2.4). Gambar 4.1 & 4.2 **tetap** (tanpa penomoran ulang). Teks pengganti siap-tempel di file revisi.

---

## 7. TUGAS — FRONT MATTER & FINALISASI

1. **DAFTAR TABEL & DAFTAR GAMBAR:** perbarui agar memuat seluruh tabel (4.1–4.6) & gambar (4.1–4.10) BAB IV. Lakukan via *Update Field* pada kedua daftar.
2. **Lampiran:** masukkan gambar tier non-n750 & training curve sisanya sesuai PLAN §5 (audit cakupan) bila diperlukan.
3. Pastikan penomoran otomatis (SEQ Tabel/Gambar) konsisten setelah penyisipan.

---

## 8. RECAP PERUBAHAN

**Sudah dilakukan (perlu dipertahankan):**
- Relokasi RUMUS BAB III → BAB II (Persamaan 2.1–2.43); BAB III tinggal perhitungan (3.1–3.17).
- Perbaikan duplikat persamaan 3.4 & sitasi SE gating (He → Hu).
- BAB IV ditulis penuh + 6 tabel + 4 gambar + 9 sitasi field; purwarupa di 4.1.2.

**Masih harus dilakukan (ringkas):**
| # | Tugas | Penanggung jawab tipikal | Bagian |
|---|---|---|---|
| 1 | Generate ROC (4.4, 4.6) + Confusion Matrix (4.9) di vast | IT/ML | §2A |
| 2 | Tangkapan layar demo (4.1, 4.2) | Tim | §2B |
| 3 | Kurva pelatihan (4.10) | IT/ML | §2C |
| 4 | Tambah placeholder 4.4 + sisip 6 gambar | Tim dok | §3 |
| 5 | Tambah sitasi Odena yang hilang (4.2.4) | Tim dok | §3 |
| 6 | Ganti gaya sitasi → (Nama, Tahun) + Update Fields | Tim dok | §4 |
| 7 | Perbaiki item value (Tabel 3.3, 1.1/3.1, label smoothing, framing) | Tim dok | §5 |
| 8 | (Opsional) Gradio+opencv ke Tabel 3.16 | Tim dok | §6 |
| 9 | Update DAFTAR TABEL/GAMBAR + Lampiran | Tim dok | §7 |

---

## 9. CHECKLIST FINAL PER BAB

**BAB II**
- [x] ~~Verifikasi sitasi Rössler di "Augmentasi Data"~~ — selesai (cukup satu sitasi Afchar)
- [ ] (Opsional) konsolidasi rumus FFT yang dobel — lihat panduan §10

---

## 10. PANDUAN KONSOLIDASI RUMUS FFT (BAB II) — opsional, cosmetik

**Masalah:** rumus inti transformasi muncul dua kali di BAB II:
- Subbab *Transformasi Fourier (FFT)* (teori): **2.1** DFT, **2.2** inverse DFT, **2.3** magnitude, **2.4** log.
- Subbab *Fast Fourier Transform (FFT)* (preprocessing): **2.16** grayscale, **2.17** DFT (= 2.1), **2.18** magnitude (= 2.3), **2.19** high-pass, **2.20** log (= 2.4), **2.21** fftshift, **2.22** z-score.

**Keputusan yang disarankan:** jadikan subbab **teori** sebagai rumah kanonik rumus inti; subbab **preprocessing** hanya merujuknya dan memuat rumus khas pipeline (grayscale, high-pass, fftshift, z-score). Ini pilihan dengan penggeseran paling sedikit.

**Langkah:**
1. **HAPUS** dari subbab preprocessing: Persamaan **2.17** (DFT), **2.18** (magnitude), **2.20** (log).
2. Pada prosa preprocessing, ganti rujukan ketiganya menjadi: "…menggunakan DFT 2D (Persamaan **2.1**)", "…magnitude (Persamaan **2.3**)", "…log scaling (Persamaan **2.4**)".
3. **Nomori ulang** persamaan setelah penghapusan (geser −3 mulai dari high-pass):

   | Lama | Baru | Isi |
   |---|---|---|
   | 2.19 | **2.17** | High-pass H(u,v) |
   | 2.21 | **2.18** | fftshift |
   | 2.22 | **2.19** | z-score |
   | 2.23 | **2.20** | Noise augmentasi |
   | … | (−3) | … |
   | 2.43 | **2.40** | Generalization drop |

4. **Perbarui rujukan di BAB III** (yang menunjuk subbab preprocessing):

   | Rujukan BAB III lama | Jadi |
   |---|---|
   | persamaan 2.17 (DFT) | **2.1** |
   | persamaan 2.18 (magnitude) | **2.3** |
   | persamaan 2.20 (log) | **2.4** |
   | persamaan 2.19 (high-pass) | **2.17** |
   | persamaan 2.22 (z-score) | **2.19** |
   | persamaan 2.16 (grayscale) | 2.16 (tetap) |
   | persamaan 2.15 (proyeksi) | 2.15 (tetap) |

5. Update *Daftar Persamaan* (bila ada) dan cek semua nomor (2.x) berurutan 2.1–2.40.

> **Alternatif ringan (bila waktu mepet):** biarkan kedua rumus, cukup tambahkan catatan "(identik dengan Persamaan 2.1)" pada rumus preprocessing. Tidak benar-benar menghapus duplikasi, tetapi mengakui keterkaitannya tanpa penomoran ulang. Duplikasi rumus teori vs terapan **bukan kesalahan** dan jarang dipermasalahkan dosen — prioritas rendah.

**BAB III**
- [ ] Tabel 3.3 ukuran sampel FFPP → 100/250/500/750
- [ ] Tabel 1.1/3.1 klaim n=1000 → perjelas tier maks 750
- [ ] Label smoothing Tabel 3.10 vs contoh loss → konsisten
- [ ] Tambah sub-bab "Skema Inferensi dan Purwarupa Sistem" (metode inferensi+purwarupa)
- [ ] Gradio + opencv-python-headless ke Tabel 3.16

**BAB IV**
- [ ] Generate & sisip Gambar 4.4, 4.6 (ROC), 4.9 (CM)
- [ ] Sisip Gambar 4.1, 4.2 (demo), 4.10 (kurva pelatihan)
- [ ] Tambah caption/placeholder Gambar 4.4 yang hilang
- [ ] Tambah sitasi Odena (4.2.4)
- [ ] Rampingkan sub-bab 4.1.2 → hasil saja (metode pindah ke BAB III), gambar 4.1/4.2 tetap
- [ ] Verifikasi 6 tabel & 4 gambar tersisip sudah benar caption/nomornya

**Lintas-bab**
- [ ] Gaya sitasi → (Nama, Tahun), Update All Fields
- [ ] Update DAFTAR TABEL & DAFTAR GAMBAR
- [ ] Framing BAB I selaras judul komparatif
