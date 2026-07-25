# Audit Sitasi — KOREKSI atas Dokumen ter-Refresh (F9)

**Tanggal:** 2026-07-24 18:40
**Menggantikan:** `Citation_Audit_AllRefs_vs_Sources_2026-07-24_1812.md` (nomor sitasinya berbasis versi lama/pra-F9).
**Alasan revisi:** setelah Ctrl+A→F9, penomoran Daftar Pustaka berubah. Sebuah **referensi baru [23] (Y. Li & S. Lyu, *Exposing DeepFake Videos By Detecting Face Warping Artifacts*)** disisipkan, sehingga **semua nomor lama ≥ 23 naik +1**. Isi (verdikt konten) audit sebelumnya sebagian besar tetap benar; yang salah hanyalah **label nomornya**. Laporan ini memakai nomor v2 yang benar dan mencatat apa yang sudah kamu perbaiki.

**Aturan konversi nomor:** v1 ≤ 22 → sama; v1 ≥ 23 → v2 = v1 + 1; plus [23] baru.

---

## 0. Sudah Kamu Perbaiki (terverifikasi di v2) ✅

- **[2] Andira** — klaim teknis "model dilatih untuk mempelajari pola, ekspresi, pergerakan wajah" **sudah dihapus** dari Andira. Andira kini hanya menyandang dua klaim yang memang didukung (pornografi non-konsensual menargetkan perempuan; 96%). **Baik.** (Sisa catatan kecil: "Studi global ... 96%" tetap kutipan tangan-kedua, prioritas rendah.)
- **[4] MesoNet** — ditulis ulang menyeluruh. Taksonomi artefak palsu, klaim "inkonsistensi pencahayaan" (yang bertentangan), dan tag "[4]" pada "Xception > MesoNet" **semuanya hilang**. Diganti klaim yang akurat untuk MesoNet (wajah deepfake buram, kehilangan detail halus akibat keterbatasan encoding space autoencoder). **Baik.**
- **Kalimat "XceptionNet 99,26% ... melampaui ResNet dan MesoNet"** — tag ganda "[4]" **sudah dilepas**, kini murni **[7]** FFPP.
- **Klaim "beberapa frame menampilkan distorsi tekstur lebih jelas"** — sudah dipindah dari **Haq** ke **Afchar/MesoNet [4]** (lihat catatan §3, masih agak lemah di sana).

---

## 1. BARU MUNCUL AKIBAT RENUMBER — Sitasi Gambar (angka statis, tidak ikut F9)

Nomor sitasi di caption gambar tampaknya **teks statis**, bukan *field*, sehingga tidak ikut ter-update saat F9. Setelah renumber, keduanya kini menunjuk paper yang salah:

| Gambar | Menyandang nomor | Sekarang menunjuk ke | Seharusnya |
|--------|------------------|----------------------|------------|
| **Gambar 2.2 "Representasi Domain Frekuensi"** | **[48]** | **MTCNN** (Zhang, Joint Face Detection) — tak berkaitan dgn frekuensi | **[25]** Gonzalez & Woods (atau **[24]** Stack Overflow) |
| **Gambar 2.1 "Distribusi Low/High-Frequency"** | caption body **[24]**, tapi Daftar Gambar masih **[23]** | body → Stack Overflow (oke-lemah); Daftar Gambar → **Li & Lyu** (salah, basi) | selaraskan ke **[24]**/**[25]**; **refresh Daftar Gambar** |

**Tindakan:**
1. **Gambar 2.2:** ganti `[48]` → `[25]` (Gonzalez & Woods) atau `[24]` (Stack Overflow). MTCNN salah total di sini.
2. **Gambar 2.1:** caption body sudah `[24]` (Stack Overflow, dapat diterima walau lemah; `[25]` Gonzalez lebih kokoh). **Refresh Daftar Gambar** (klik tabel → F9 → Update entire table) supaya `[23]` basi hilang.
3. **Cek semua caption gambar lain** apakah nomornya statis — kalau ya, semuanya perlu diverifikasi ulang setelah renumber.

> **Konsekuensi penting:** referensi baru **[23] Li & Lyu** saat ini **hanya muncul di Daftar Gambar yang basi**, tidak di prosa/caption manapun. Setelah Daftar Gambar di-refresh, **[23] berpotensi jadi referensi yatim** (tidak tersitasi). Pastikan Li & Lyu memang ingin dipakai — kalau ya, sitasikan di teks; kalau tidak, hapus dari daftar.

---

## 2. Referensi "Yatim" — DIRALAT: TIDAK ADA yang yatim ✅

**Koreksi penting.** Klaim "referensi yatim" pada laporan sebelumnya **SALAH**. Setelah dicek langsung terhadap **penyimpan sumber Word** (`customXml/item1.xml`) dan **seluruh field `CITATION`** di `document.xml`, hasilnya: **ke-50 sumber tersitasi. Tidak ada satu pun yang yatim.**

Kesalahan sebelumnya berasal dari pemindaian teks `[N]` yang terlihat, yang gagal menangkap:
1. **Sitasi gabungan/merged** (Word `\m` — beberapa sumber dalam satu tanda kurung), dan
2. **Sitasi gambar**, serta
3. field `CITATION` yang dipecah Word ke beberapa run XML.

Bukti lokasi sitasi (via field code):

| Ref v2 | Tag Word | Tersitasi di | 
|--------|----------|--------------|
| [20] Aduwala | `Adu21` | 1× dalam sitasi gabungan `[14],[15],[20],[7]` (Rana+Rao+Aduwala+Rössler) |
| [22] Dai | `Dai21` | 1× (dalam grup) |
| [23] Li & Lyu | `LiY19` | 1× (caption Gambar 2.1) |
| [34] Nguyen | `Ngu` | 2× bergrup dengan `[35]` Güera |
| [35] Güera | `Güe18` | 4× bergrup (Nguyen/Li/Kim) |
| [43] Bottou | `Bot12` | 1× bergrup `[42],[43]` dengan Goodfellow |
| [50] Wikimedia | `Wik18` | 2× (sitasi gambar) |

**Konsekuensi untuk penghapusan:** tombol `[−]` di panel Citations Word **disabled karena sumbernya memang masih dipakai** — Word melindungi sumber yang tersitasi. Ini perilaku benar, bukan bug. Kalau memang ingin membuang salah satunya, hapus dulu sitasinya di teks (untuk sitasi gabungan: klik grup → *Edit Citation* → buang sumber itu saja), baru `[−]` aktif.

---

## 3. TIDAK SESUAI — Masih Perlu Diperbaiki (nomor v2)

### 3a. Bertentangan dengan sumber (paling serius)

| Ref v2 | Kalimat | Faktanya di paper |
|--------|---------|-------------------|
| **[7] FFPP** (5) | "variasi kompresi tidak mengganggu, Xception tahan compression noise" | FFPP: Xception **kesulitan** pada kompresi; akurasi LQ turun ke **81%** |
| **[9] Zhang** (7) | "[9] freq meningkatkan robustness thd variasi kualitas video" | Zhang: JPEG/resize **menghancurkan** artefak; ini soal citra bukan video |
| **[9] Zhang** (10) | "FFT menangkap amplitudo **dan fase**" | Zhang eksplisit **membuang fase** (hanya log-magnitude). Pindah klaim fase ke **[26]/[27]** |

### 3b. Salah paper / relabel

| Ref v2 | Kalimat | Perbaikan |
|--------|---------|-----------|
| **Gambar 2.2** [48]=MTCNN | figur domain frekuensi | → **[25]** / **[24]** (lihat §1) |
| **[6] Xception** (4) | "frequency-aware features / energi frekuensi [6]" | Chollet tak menyinggung frekuensi → **[8]/[11]** |
| **[6] Xception** (19) | "baseline efektif deteksi manipulasi wajah [6]" | Chollet tak menguji ini → **[7]** |
| **[6] Xception** (14) | "sensitif variasi struktur lokal [6]" | tak ada di paper → hapus |
| **[9] Zhang** (12) | "ketidakkontinyuan batas blending [9]" | di luar cakupan Zhang → **[16]** |
| **[28] Karras** (2) *(v1 27)* | "identifikasi blending/warping/blur [28]" | PGGAN paper **generasi** GAN → **[4]/[9]/[14]** |
| **[41] Sabir** (3) *(v1 40)* | "sinyal frekuensi tinggi lebih efektif utk deepfake terkompresi [41]" | Sabir **nol** konten frekuensi (RNN/temporal) → **[32] Mejri / [11] / [12]** |
| **[14] Rana** | "spectral distortions dari keterbatasan struktural generatif [14]" | Rana tak bahas spektral → **[8]** |
| **[1] Korshunov** (1) | "disinformasi & propaganda geopolitik [1]" | Korshunov soal kerentanan face-recognition; propaganda/disinformasi tak ada (fake-news hanya tangan-kedua via Allcott&Gentzkow) → **[14]** |
| **[1] Korshunov** (2) | "model dilatih mempelajari pola/ekspresi/pergerakan wajah [1]" *(pindahan dari Andira)* | **LEMAH** — Korshunov sebut GAN/autoencoder face-swap & meniru gerak mulut, tapi tak menjelaskan proses pelatihan fitur. Lebih tepat **[19] Chadha** (overview) atau **[42] Goodfellow** |
| **[19] Chadha** | "...lip-sync translation, dan **virtual reality** [19]" | "virtual reality" tak ada (paper sebut *video game*) → hapus |

### 3c. Salah-label domain frekuensi (inti argumen skripsi)

| Ref v2 | Kalimat | Masalah → perbaikan |
|--------|---------|---------------------|
| **[11] Qian/F3-Net** (3) | "generalisasi pada **berbagai dataset**" | Hanya diuji FF++ lintas kompresi → "berbagai **tingkat kompresi**" |
| **[11]** (4) | framing early-fusion "dari layer konvolusi pertama" | F3-Net **bukan** early fusion (dua stream freq, fusi belakangan) |
| **[11]** (7) | "representasi **FFT**" | F3-Net pakai **DCT** → hapus/ganti "DCT" |
| **[11]** (10) | "deteksi **unseen datasets** lebih baik" | Robust thd **kompresi**, bukan domain shift |
| **[12] Tan/FreqNet** (4) | "lebih baik pada **citra terkompresi**" | FreqNet tak ada eksperimen kompresi → **[11]** |
| **[13] Alam/SpecXNet** (4) | "band frekuensi **menengah** [16][13]" | SpecXNet = frekuensi **tinggi/periodik** → hapus "menengah" |
| **[16] FSBI** (6) | "band frekuensi **menengah**" | FSBI = DWT (high-freq detail), tanpa mid-band |
| **[16] FSBI** (11) | "metode **FFT** lebih tahan lintas dataset" | FSBI pakai **DWT/wavelet** → ganti label "DWT" |

---

## 4. LEMAH — Perhalus bila sempat (nomor v2)

- **[3] Haq** (1): "menurun pada pengujian **lintas dataset** [3]" — Haq hanya pakai 1 dataset (Celeb-DF V2), tak menguji lintas-dataset. (3): "artefak manipulasi tidak selalu muncul konsisten sepanjang video [3]" — **masih** tak didukung Haq (alasannya efisiensi + variasi ekspresi). (2),(4) SESUAI.
- **[4] MesoNet** (v2, sisa): (5) "blending & warping" bukan fokus eksplisit MesoNet; (6) "Afchar menunjukkan beberapa frame distorsi tekstur lebih jelas" — MesoNet tak menganalisis variasi antar-frame (klaim ex-Haq ini masih lemah, kini di Afchar); (8) "augmentasi=regularisasi" framing umum; (9) "akurasi menurun pada dataset lebih kompleks" tak ditunjukkan.
- **[5] ResNet** (5): "degradasi **gradien**" keliru — ResNet eksplisit menyatakan bukan vanishing gradient → "degradasi akurasi/optimasi".
- **[6] Xception**: (7) rumus kompleksitas DSC = MobileNets/Howard, bukan Chollet; (10) max-pooling bukan "setiap blok" (hanya entry/exit flow); (13) Xception ≈ jumlah parameter InceptionV3 → "penggunaan parameter lebih efisien".
- **[8] Durall**: (7) "citra = kombinasi gelombang sinusoidal" (definisi Fourier) → **[25]**; (14) taksonomi domain-shift → **[47]/[14]**; (17) "FFT efisien hi-res" → sumber DSP/**[25]**; (1)(6)(8) inferensi penulis (kegagalan generalisasi / kehilangan lokasi spasial / "spectral fall-off & band ratio").
- **[9] Zhang** (4): alasan lintas-arsitektur terbalik (generalisasi dari artefak upsampling **bersama**, bukan "fingerprint unik").
- **[10] Giudice** (1): "konsisten **antar-arsitektur** GAN" keliru — GSF fingerprint **per-arsitektur** → "architecture-specific".
- **[14] Rana**: daftar artefak "pencahayaan/bayangan/distorsi geometrik" (cocok [4]); "AUC threshold-independent"; "imbalance kelas/distribusi" — ketiganya tak dinyatakan Rana.
- **[29] Geirhos** *(v1 28)* + **[30] Rahaman** *(v1 29)*: kalimat gabungan kini "[29, 30]" (tekstur + low-freq) — **dapat diterima** sebagai sitasi terbagi. Pastikan tak ada versi berdiri sendiri "[29]" yang mengklaim low-freq (itu milik [30]).
- **[32] Mejri** *(v1 31)*: (1) "tekstur kulit terlalu halus" tak ada di Mejri (fake justru **ekstra** noise freq tinggi); (2) "kompresi merusak petunjuk freq tinggi" tak dinyatakan.
- **[16] FSBI**: (5) "pola freq stabil meski terkompresi" — FSBI bilang sebaliknya; (8)(9)(10) robustness kompresi/noise tak ditunjukkan, FSBI = DWT-preproc + 1 CNN (bukan dua cabang).
- **[39] SE-Net** *(v1 38)*: (2) "inspirasi sistem visual manusia" tak ada; (6) "SE > concat/add utk fusi multi-domain" ekstrapolasi.
- **[7] FFPP**: (18)(20) "melampaui ResNet" — FFPP tak menguji ResNet-50; (4)(7)(11)(16)(3) pernyataan latar/spektral/kritik-diri disandarkan ke paper dataset.
- **[42] Goodfellow** *(v1 41)* (1): klausa alasan spesifik-deepfake bukan dari buku.
- **[24] Stack Overflow** *(v1 23)*: sumber lemah utk skripsi (Gambar 2.1); **[25]** lebih kokoh.

---

## 5. SESUAI — tidak perlu diubah (ringkas, nomor v2)

Optimizer/training: **[45] Adam, [46] AdamW, [44] Ruder, [48] MTCNN (klaim deteksi wajah, bukan figur frekuensi), [49] Dropout 0.5, [36] LeCun, [42] Goodfellow (gradient clipping)**. Teori spektral: **[26] Oppenheim, [27] Liu SPSL, [30] Rahaman, [31] Wang, [21] Odena, [25] Gonzalez & Woods**. Dataset: **[18] Celeb-DF**. Deteksi frekuensi (inti benar): **[8] Durall, [17] Luo/FMSI** (semua), core **[11]/[12]/[13]/[16]** benar. Temporal/domain: **[33] Kim, [37] Haliassos, [47] Ben-David, [41] Sabir** (kecuali klaim frekuensi), **[40] Ma, [15] Rao, [38] Akinrogunde**.

---

## 6. Prioritas Eksekusi

1. **Perbaiki sitasi Gambar (§1)** — dua-duanya kini salah paper akibat renumber; ini yang membuat audit lama terasa "meleset". Ganti Gambar 2.2 `[48]`→`[25]`, selaraskan Gambar 2.1 ke `[24]/[25]`, lalu refresh Daftar Gambar.
2. **Perbaiki yang bertentangan (§3a)** — [7] kompresi, [9] fase & kualitas video.
3. **Betulkan salah-label frekuensi (§3b, §3c)** — "FFT" pada paper DCT/DWT, "band menengah" pada paper high-freq, tukar kompresi↔lintas-dataset, [41] Sabir & [28] Karras salah paper.
4. **Tangani referensi yatim (§2)** — termasuk verifikasi [23] Li & Lyu.
5. **Perhalus LEMAH (§4)** bila sempat.

> Verdikt didasarkan pembacaan teks penuh tiap PDF sumber; 34 dari 40 paper isinya identik dgn versi sebelumnya (hanya renumber), sisanya sudah diverifikasi ulang pada v2. Siap membuat kalimat pengganti siap-tempel atau menyisir langsung `.docx` untuk cek field vs teks statis bila diinginkan.
