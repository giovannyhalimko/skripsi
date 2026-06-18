# HANDOFF — Finalisasi BAB II, III, IV (Skripsi Deepfake Hybrid)

**Tanggal:** 2026-06-17
**Tujuan:** daftar tugas lengkap + recap perubahan untuk menuntaskan BAB II–IV pada dokumen WORD.
**Dokumen final:** OneDrive `REVISI V1 - Metode Peningkatan Deteksi Deepfake ... .docx`
**Hasil yang di-settle:** commit `d28efae` → `deepfake_hybrid/results_vast_20260609/` (3 model × 2 dataset × tier n100/250/500/750 × 3 seed). **JANGAN ganti angka hasil** tanpa kesepakatan tim.
**Arah judul (komparatif):** "Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet–FFT terhadap Model Domain Tunggal".

> Dokumen rujukan terkait (sudah ada di repo):
>
> - Rencana BAB IV: `documents/BAB_IV_STRUCTURE_PLAN_2026-06-15.md`
> - Naskah BAB IV: `documents/BAB_IV_Hasil_dan_Pembahasan_2026-06-17.md`
> - Status revisi & item value: `analyze/REVISI_V1_Status_dan_TODO_2026-06-17.md`
> - Analisis value lengkap: `analyze/REVISI_V1_Full_Analysis_and_RUMUS_Relokasi_2026-06-11_1600.md`
> - **Handoff presentasi (deck sidang) — repo terpisah:** `../skripsi-presentation/HANDOFF.md` → lihat **§11** (berbagi data; update bersama-sama)

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

**KEPUTUSAN (2026-06-17): subbab 4.1.7 + Confusion Matrix + Kurva Pelatihan DIPERTAHANKAN** (gambar di-generate menyusul, lihat §2A & §2C). Jadi bukan dihapus — yang diperlukan hanya **menutup gap penomoran**:

- 4.1.3 (In-Dataset): pertahankan **Gambar 4.3** (bar). _(Bila ROC in-dataset jadi dimasukkan, ia menyisip sebagai gambar tersendiri — lihat catatan ROC.)_
- 4.1.4 (Cross-Dataset): **Gambar 4.4** (bar cross). ✅ sudah benar.
- 4.1.5 (Drop): **Gambar 4.5**. ✅
- 4.1.6 (Scaling): **Gambar 4.6**. ✅
- 4.1.7 (Confusion Matrix & Dinamika Pelatihan): **renumber Gambar 4.9 → 4.7 (confusion matrix)** dan **Gambar 4.10 → 4.8 (kurva pelatihan)** agar tidak ada lompatan setelah 4.6. Generate kedua gambar via §2A/§2C lalu sisipkan.
- 4.2.4: rujukan "kurva pelatihan (Gambar 4.10)" → ubah ke **Gambar 4.8**; pertahankan rujukan **Gambar 4.2**.

> **Catatan ROC (perlu keputusan):** teks 4.1.3/4.1.4 masih menyinggung "kurva ROC". Bila ROC **ikut dipertahankan** (in-dataset + cross-dataset), tambahkan 2 gambar ROC dan geser penomoran (mis. ROC in = 4.4, bar cross = 4.5, ROC cross = 4.6, drop = 4.7, scaling = 4.8, CM = 4.9, pelatihan = 4.10 → kembali ke skema 10 gambar). Bila ROC **tidak** dipakai, hapus kalimat ROC di 4.1.3/4.1.4 dan pakai skema 8 gambar (4.1–4.8) di atas.

### 🟠 B. Sitasi

- **Odena (Ode16) masih HILANG** di 4.2.4 — kalimat sidik jari upsampling GAN seharusnya memuat dua sitasi: Durall **[8]** dan **Odena [21]**. Tambahkan field Odena.
- **Gaya sitasi = IEEE `[N]` — JANGAN diubah ke (Nama, Tahun).** Pedoman 4.5.5 **mewajibkan IEEE** (`[1]`, `[1,3]`, `[1-5]`). Dokumen sudah render `[N]` → **sudah benar, tidak perlu diubah.** _(Koreksi: rekomendasi sebelumnya untuk pindah ke author-year DIBATALKAN karena melanggar pedoman.)_

### 🟠 C. Value (audit menyeluruh vs `config.yaml` + `d28efae`, 2026-06-17)

**Hanya `n` (ukuran sampel) & `α` (label smoothing) yang perlu diperbaiki. Semua nilai lain SUDAH BENAR** (Tabel 3.10 hyperparameter ✓ cocok config.yaml; Tabel 3.6 FreqCNN ~4,2 jt ✓ terverifikasi jumlah layer; Tabel 4.2–4.5 hasil ✓ cocok d28efae).

**KEPUTUSAN value (2026-06-17): Opsi A — komposisi FFPP tetap 1000** (FFPP = dataset utama 4-metode yang lebih besar; tier asli dulu sampai 1000 ⇒ data 1000/50.000 frame memang disiapkan; eksperimen lalu di-cap ≤750). Jadi Tabel 1.1/3.1 **tidak diubah**. *(Bila ternyata hanya ≤750 FFPP yang diekstrak, beralih ke Opsi B: 375+375=750, 37.500 frame.)*

Status per item (docx live 13:19) + HTML siap-tempel sudah diperbaiki:

- ✅ **Label smoothing (Tabel 3.10)** → `0,05`. SELESAI (oleh user).
- ✅ **Tabel 3.3 (Variasi Ukuran Sampel)** → di docx sudah `100,250,500,750` keduanya. HTML `tabel_3_2_variasi_ukuran_sampel.html` ikut diperbaiki (caption → 3.3).
- ⚠️ **Tabel 3.11 (Matriks Eksperimen) — baris FFPP masih `100, 300, 600, 1000`** di docx → ganti dgn HTML baru `tabel_3_10_matriks_eksperimen.html` (FFPP+CDF digabung jadi satu baris `Ukuran sampel (video) = 100,250,500,750`).
- ⚠️ **Tabel 3.12 (Variabel Penelitian) — "Ukuran sampel `100–1000`"** di docx → ganti dgn HTML baru `tabel_3_11_variabel_penelitian.html` (`100, 250, 500, 750`).
- ✅ **Tabel 1.1 / 3.1** → tetap (Opsi A); HTML `tabel_1_1_*` & `tabel_3_1_*` sudah sesuai.
- ⚠️ **Prosa BAB III** "membatasi total frame FFPP n=1000 ~ 50.000" → tetap konsisten dgn Opsi A (1000); tidak perlu diubah.

### 🟢 Sudah benar (terverifikasi)

- Persamaan BAB II 2.1–2.40 & BAB III 3.1–3.17 urut tanpa duplikat; semua rujukan "persamaan 2.x" BAB III benar pasca-renumber.
- Tabel 4.1–4.6 & captionnya urut; konsolidasi FFT benar.

_(Minor: "Tabel 4.2Hasil…" tambahkan spasi setelah "4.2".)_

---

## 1. ASET YANG SUDAH SIAP DIPAKAI

| Aset                                            | Lokasi                                                   | Status                            |
| ----------------------------------------------- | -------------------------------------------------------- | --------------------------------- |
| Tabel HTML BAB IV (4.1–4.6)                     | `documents/table/tabel_4_*.html`                         | ✅ siap (sudah tersisip ke docx)  |
| Gambar BAB IV 4.3/4.5/4.7/4.8 (label Indonesia) | `documents/media_v2/gambar_4_{3,5,7,8}_*.png`            | ✅ siap (sudah tersisip)          |
| Skrip ROC + Confusion Matrix                    | `deepfake_hybrid/scripts/make_roc_cm.py`                 | ✅ teruji (perlu checkpoint n750) |
| Skrip generate gambar bar/scaling/drop          | `deepfake_hybrid/scripts/make_bab4_figures.py`           | ✅ teruji                         |
| Plot mentah hasil                               | `deepfake_hybrid/results_vast_20260609/plots/` (Inggris) | referensi/Lampiran                |

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

1. **Gaya sitasi = IEEE `[N]` (Pedoman 4.5.5) — PERTAHANKAN, jangan diubah.** Seluruh sitasi sudah CITATION field yang render `[N]` → sesuai pedoman. **Tidak perlu** mengubah style ke author-year (rekomendasi lama dibatalkan). Cukup pastikan setiap sitasi tercantum di Daftar Pustaka dan urut kemunculan ([1] pertama muncul, dst — Pedoman 4.5.5.e).
2. ~~Verifikasi sitasi Augmentasi (BAB II).~~ ✅ **SELESAI (cek 2026-06-17):** paragraf "Augmentasi Data" kini memuat satu sitasi (Afchar et al.). Klaim "augmentasi sebagai teknik regularisasi" bersifat umum, sehingga satu sitasi pendukung sudah memadai — tidak perlu menambah Rössler.
3. Sebelum final, **Update Fields (Ctrl+A → F9)** seluruh dokumen untuk merefresh nomor sitasi `[N]`, bibliografi, penomoran tabel/gambar (SEQ), dan daftar isi.

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

1. **DAFTAR TABEL & DAFTAR GAMBAR:** perbarui agar memuat seluruh tabel (4.1–4.6) & gambar (4.1–4.10) BAB IV. Lakukan via _Update Field_ pada kedua daftar.
2. **Lampiran:** masukkan gambar tier non-n750 & training curve sisanya sesuai PLAN §5 (audit cakupan) bila diperlukan.
3. Pastikan penomoran otomatis (SEQ Tabel/Gambar) konsisten setelah penyisipan.

---

## 8. RECAP PERUBAHAN

**Sudah dilakukan (perlu dipertahankan):**

- Relokasi RUMUS BAB III → BAB II (Persamaan 2.1–2.43); BAB III tinggal perhitungan (3.1–3.17).
- Perbaikan duplikat persamaan 3.4 & sitasi SE gating (He → Hu).
- BAB IV ditulis penuh + 6 tabel + 4 gambar + 9 sitasi field; purwarupa di 4.1.2.

**Masih harus dilakukan (ringkas):**

| #   | Tugas                                                              | Penanggung jawab tipikal | Bagian |
| --- | ------------------------------------------------------------------ | ------------------------ | ------ |
| 1   | Generate ROC (4.4, 4.6) + Confusion Matrix (4.9) di vast           | IT/ML                    | §2A    |
| 2   | Tangkapan layar demo (4.1, 4.2)                                    | Tim                      | §2B    |
| 3   | Kurva pelatihan (4.10)                                             | IT/ML                    | §2C    |
| 4   | Tambah placeholder 4.4 + sisip 6 gambar                            | Tim dok                  | §3     |
| 5   | Tambah sitasi Odena yang hilang (4.2.4)                            | Tim dok                  | §3     |
| 6   | Ganti gaya sitasi → (Nama, Tahun) + Update Fields                  | Tim dok                  | §4     |
| 7   | Perbaiki item value (Tabel 3.3, 1.1/3.1, label smoothing, framing) | Tim dok                  | §5     |
| 8   | (Opsional) Gradio+opencv ke Tabel 3.16                             | Tim dok                  | §6     |
| 9   | Update DAFTAR TABEL/GAMBAR + Lampiran                              | Tim dok                  | §7     |

---

## 9. CHECKLIST FINAL PER BAB

**BAB II**

- [x] ~~Verifikasi sitasi Rössler di "Augmentasi Data"~~ — selesai (cukup satu sitasi Afchar)
- [ ] (Opsional) konsolidasi rumus FFT yang dobel — lihat panduan §10

---

## 10. PANDUAN KONSOLIDASI RUMUS FFT (BAB II) — opsional, cosmetik

**Masalah:** rumus inti transformasi muncul dua kali di BAB II:

- Subbab _Transformasi Fourier (FFT)_ (teori): **2.1** DFT, **2.2** inverse DFT, **2.3** magnitude, **2.4** log.
- Subbab _Fast Fourier Transform (FFT)_ (preprocessing): **2.16** grayscale, **2.17** DFT (= 2.1), **2.18** magnitude (= 2.3), **2.19** high-pass, **2.20** log (= 2.4), **2.21** fftshift, **2.22** z-score.

**Keputusan yang disarankan:** jadikan subbab **teori** sebagai rumah kanonik rumus inti; subbab **preprocessing** hanya merujuknya dan memuat rumus khas pipeline (grayscale, high-pass, fftshift, z-score). Ini pilihan dengan penggeseran paling sedikit.

**Langkah:**

1. **HAPUS** dari subbab preprocessing: Persamaan **2.17** (DFT), **2.18** (magnitude), **2.20** (log).
2. Pada prosa preprocessing, ganti rujukan ketiganya menjadi: "…menggunakan DFT 2D (Persamaan **2.1**)", "…magnitude (Persamaan **2.3**)", "…log scaling (Persamaan **2.4**)".
3. **Nomori ulang** persamaan setelah penghapusan (geser −3 mulai dari high-pass):
   | Lama | Baru | Isi |
   | ---- | -------------- | ------------------- |
   | 2.19 | **2.17** | High-pass H(u,v) |
   | 2.21 | **2.18** | fftshift |
   | 2.22 | **2.19** | z-score |
   | 2.23 | **2.20** | Noise augmentasi |
   | … | (−3) | … |
   | 2.43 | **2.40** | Generalization drop |
4. **Perbarui rujukan di BAB III** (yang menunjuk subbab preprocessing):
   | Rujukan BAB III lama | Jadi |
   | -------------------------- | -------------- |
   | persamaan 2.17 (DFT) | **2.1** |
   | persamaan 2.18 (magnitude) | **2.3** |
   | persamaan 2.20 (log) | **2.4** |
   | persamaan 2.19 (high-pass) | **2.17** |
   | persamaan 2.22 (z-score) | **2.19** |
   | persamaan 2.16 (grayscale) | 2.16 (tetap) |
   | persamaan 2.15 (proyeksi) | 2.15 (tetap) |
5. Update _Daftar Persamaan_ (bila ada) dan cek semua nomor (2.x) berurutan 2.1–2.40.

> **Alternatif ringan (bila waktu mepet):** biarkan kedua rumus, cukup tambahkan catatan "(identik dengan Persamaan 2.1)" pada rumus preprocessing. Tidak benar-benar menghapus duplikasi, tetapi mengakui keterkaitannya tanpa penomoran ulang. Duplikasi rumus teori vs terapan **bukan kesalahan** dan jarang dipermasalahkan dosen — prioritas rendah.

**BAB III**

- [x] Tabel 3.3 ukuran sampel FFPP → 100/250/500/750
- [x] Tabel 1.1/3.1 klaim n=1000 → perjelas tier maks 750
- [x] Label smoothing Tabel 3.10 vs contoh loss → konsisten
- [x] Tambah sub-bab "Skema Inferensi dan Purwarupa Sistem" (metode inferensi+purwarupa)
- [x] Gradio + opencv-python-headless ke Tabel 3.16

**BAB IV**

- [ ] Generate & sisip Gambar 4.4, 4.6 (ROC), 4.9 (CM)
- [ ] Sisip Gambar 4.1, 4.2 (demo), 4.10 (kurva pelatihan)
- [ ] Tambah caption/placeholder Gambar 4.4 yang hilang
- [x] Tambah sitasi Odena (4.2.4)
- [x] Rampingkan sub-bab 4.1.2 → hasil saja (metode pindah ke BAB III), gambar 4.1/4.2 tetap
- [ ] Verifikasi 6 tabel & 4 gambar tersisip sudah benar caption/nomornya

**Lintas-bab**

- [x] Gaya sitasi → (Nama, Tahun), Update All Fields
- [x] Update DAFTAR TABEL & DAFTAR GAMBAR
- [x] Framing BAB I selaras judul komparatif

---

## 11. Handoff Presentasi (deck sidang) — repo terpisah `skripsi-presentation`

> Deck presentasi sidang dibuat di repo terpisah **`../skripsi-presentation`**. Handoff lengkapnya: **`../skripsi-presentation/HANDOFF.md`**. Deck **mengambil data dari repo thesis ini** (skrip, Tabel 4.x, gambar `media_v2`), jadi **kedua handoff harus diperbarui bersamaan** saat data berubah.

**Yang sudah selesai di deck (bisa dipakai balik untuk thesis):**

- **Screenshot demo Gambar 4.1 & 4.2 SUDAH TERSEDIA** (memenuhi §2B di atas). Ada di `../skripsi-presentation/public/figures/fig-demo-ui.png` (= **4.1** antarmuka demo) dan `fig-what-models-see.png` (= **4.2** what-the-models-see). Untuk thesis, salin & rename ke `documents/media_v2/gambar_4_1_antarmuka_demo.png` & `gambar_4_2_what_models_see.png`, lalu sisipkan menggantikan penanda `[MASUKKAN GAMBAR 4.1/4.2]` (§3).
- Komposisi Celeb-DF di deck memakai **375/375 (n=750)** sesuai Tabel 1.1/3.1 (Opsi A/B perlu dipastikan konsisten — lihat §0b.C).

**Titik sinkronisasi (bila salah satu berubah, update keduanya):**

| Berubah di thesis | Update di deck |
|---|---|
| Angka hasil (Tabel 4.2–4.6) | `src/data/results.ts` |
| **Penomoran gambar BAB IV final** (§0b.A — masih cair) | `src/data/figures.ts` (`figureNo`) — deck kini pakai 4.3/4.5/4.7/4.8; selaraskan ke skema final |
| Komposisi dataset (Tabel 1.1/3.1) | slide `dataset` di `src/data/slides.ts` |
| Gambar baru CM/ROC/kurva (§2A/§2C) | drop PNG ke `public/figures/` + un-placeholder di `figures.ts` |

**Catatan untuk deck (info, bukan tugas thesis):** deck sudah memakai nilai **v4** (label smoothing 0,05; FreqCNN ~4 jt) — konsisten dengan keputusan §0b.C. Tabel HTML `tabel_3_9`/`tabel_3_6` yang masih pra-v4 sebaiknya diregenerasi agar tidak bentrok dengan deck/docx.
