![1784907502119](image/Citation_Audit_AllRefs_vs_Sources_2026-07-24_1812/1784907502119.png)

# Audit Sitasi Menyeluruh — Kalimat Skripsi vs Isi Paper Sumber

**Tanggal:** 2026-07-24 18:12
**Dokumen:** `live-thesis-document.docx` (STUDI KOMPARATIF ... DOMAIN TUNGGAL)
**Cakupan:** 49 entri Daftar Pustaka; 40 referensi ber-PDF diverifikasi kalimat-per-kalimat terhadap teks sumber aslinya (~250 kalimat pengutip). [2] & [3] sudah dibahas terpisah sebelumnya; [23]/[49] sumber web.
**Metode:** ekstraksi peta sitasi `[N] → kalimat` dari document.xml, konversi seluruh PDF referensi ke teks, verifikasi paralel 8 agen terhadap teks sumber. Verdikt: **SESUAI** (didukung) / **LEMAH** (tangensial, tangan-kedua, terlalu disederhanakan) / **TIDAK SESUAI** (tidak ada di sumber, bertentangan, atau salah atribusi).

---

## 1. Ringkasan Eksekutif

- **Mayoritas sitasi SESUAI.** Fakta dataset, definisi arsitektur, klaim optimizer (Adam/AdamW/MTCNN/Dropout/ResNet), dan teori spektral inti (Rahaman, Wang, Oppenheim, Ben-David) terverifikasi benar.
- **~28 kalimat TIDAK SESUAI** (salah atribusi / bertentangan / salah paper) dan **~25 kalimat LEMAH**. Terpusat pada bab landasan teori domain frekuensi.
- **6 referensi "yatim"** (terdaftar tapi tidak pernah disitasi di badan teks).

### Pola berulang (akar masalah)

1. **Label "FFT" ditempel ke paper non-FFT.** F3-Net [11] pakai **DCT**; FSBI [16] pakai **DWT/wavelet**; Zhang [9] **membuang fase** (hanya log-magnitude). Skripsi menyebut "FFT" untuk ketiganya.
2. **Klaim "band frekuensi menengah"** ditempel ke paper yang sebenarnya melaporkan sinyal **frekuensi tinggi/periodik** (SpecXNet [13], FSBI [16]).
3. **"Ketahanan terhadap kompresi" ↔ "generalisasi lintas-dataset" tertukar** antara F3-Net [11] (kompresi, 1 dataset) dan FreqNet [12]/FSBI [16] (lintas-sumber).
4. **Klaim teknis frekuensi disandarkan ke paper yang bukan tentang frekuensi** — Xception [6], PGGAN [27], Dropout [48], MesoNet [4], Rana [14], Sabir [40].
5. **Klaim latar/umum disandarkan ke paper spesifik** (definisi Fourier, efisiensi FFT, AUC, imbalance kelas → Durall [8]/Rana [14]).

---

## 2. Temuan Struktural — Referensi "Yatim" (terdaftar, tak pernah disitasi)

Gaya IEEE mensyaratkan tiap entri Daftar Pustaka dikutip minimal sekali. Enam entri ini hanya muncul di daftar:

| Ref  | Judul                                                 | Tindakan                                                  |
| ---- | ----------------------------------------------------- | --------------------------------------------------------- |
| [20] | Aduwala — Deepfake Detection using GAN Discriminators | sitasi di teks atau hapus                                 |
| [22] | Dai — Learning Affinity-Aware Upsampling              | sitasi di teks atau hapus                                 |
| [33] | Nguyen — Learning Spatio-temporal features            | sitasi di teks atau hapus                                 |
| [34] | Güera — Deepfake Video Detection Using RNN            | sitasi di teks atau hapus                                 |
| [42] | Bottou — Stochastic Gradient Descent Tricks           | sitasi di teks atau hapus                                 |
| [49] | Wikimedia — 2D Fourier Transform image                | pastikan dipakai sebagai kredit gambar; jika tidak, hapus |

> Catatan: [33] Nguyen & [34] Güera adalah paper temporal/video klasik. Jika bab "analisis video" membahasnya secara konsep, kemungkinan sitasinya hilang saat editing (kandidat kuat untuk dikutip, bukan dihapus).

---

## 3. TIDAK SESUAI — Perlu Diperbaiki (prioritas tinggi)

### 3a. Salah paper / salah nomor sitasi (yang paling mengkhawatirkan)

| Ref                   | Kalimat (ringkas)                                                                 | Masalah                                                             | Perbaikan                                                                |
| --------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **[48] Dropout**      | Gambar 2.2 "Representasi Domain Frekuensi [48]" (muncul 3x)                       | Paper Dropout tak ada hubungan dgn domain frekuensi/FFT             | Ganti ke**[24]** Gonzalez & Woods atau **[23]**                          |
| **[6] Xception** (4)  | "frequency-aware features ... distribusi energi frekuensi ciri khas deepfake [6]" | Chollet murni klasifikasi citra; tak menyinggung frekuensi/deepfake | Ganti ke**[8]** / **[11]**                                               |
| **[6] Xception** (19) | "Chollet [6] ... XceptionNet baseline efektif deteksi manipulasi wajah"           | Chollet tak menguji deteksi manipulasi wajah                        | Sandarkan ke**[7]** FFPP                                                 |
| **[6] Xception** (14) | "XceptionNet sensitif terhadap variasi struktur lokal [6]"                        | Pernyataan tak ada di paper                                         | Hapus tag / cari sumber lain                                             |
| **[27] Karras** (2)   | "pendekatan spasial identifikasi blending/warping/blur [27]"                      | PGGAN paper GENERASI GAN, bukan deteksi                             | Ganti ke**[4]/[9]/[14]**                                                 |
| **[40] Sabir** (3)    | "[40] menemukan sinyal frekuensi tinggi lebih efektif utk deepfake terkompresi"   | Sabir NOL konten frekuensi (paper RNN/temporal murni; grep bersih)  | Ganti ke**[31]/[11]/[12]** — kemungkinan nomor tertukar                  |
| **[28] Geirhos** (2)  | "bias terhadap tekstur**dan komponen frekuensi rendah** [28]"                     | Geirhos hanya tekstur-vs-bentuk; low-freq-first milik [29]          | "...tekstur**[28]** dan komponen frekuensi rendah lebih dahulu **[29]**" |
| **[14] Rana**         | "spectral distortions ... keterbatasan struktural model generatif [14]"           | Rana tak pernah bahas distorsi spektral                             | Ganti ke**[8]** Durall                                                   |
| **[9] Zhang** (12)    | "ketidakkontinyuan pada batas blending [9]"                                       | Zhang soal replikasi spektral upsampling, bukan blending            | Ganti ke**[16]** FSBI                                                    |
| **[8] Durall** (7)    | "citra = kombinasi gelombang sinusoidal [8]"                                      | Definisi Fourier dasar; tak diartikulasikan Durall                  | Ganti ke**[24]**                                                         |
| **[8] Durall** (14)   | "domain shift = kualitas video/kompresi/device/lighting [8]"                      | Durall tak bahas domain shift                                       | Ganti ke**[46]/[14]**                                                    |
| **[8] Durall** (17)   | "FFT kompleksitas rendah, efisien utk hi-res [8]"                                 | Durall tak klaim biaya komputasi FFT                                | Ganti ke sumber DSP/**[24]**                                             |
| **[7] FFPP** (15)     | "Adam konvergensi cepat & stabil [7]"                                             | FFPP hanya MEMAKAI Adam, tak klaim itu                              | Ganti ke**[44]/[41]**                                                    |

### 3b. Bertentangan dengan isi sumber (paling serius — sumber berkata sebaliknya)

| Ref                  | Kalimat (ringkas)                                                                 | Yang sumber sebenarnya katakan                                                                                                           |
| -------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **[7] FFPP** (5)     | "variasi kompresi tidak mengganggu performa, XceptionNet tahan compression noise" | FFPP: Xception**kesulitan** pada kompresi; akurasi LQ turun ke **81%** (full-image 70%). Balik total.                                    |
| **[9] Zhang** (7)    | "[9] freq info meningkatkan robustness thd variasi kualitas video"                | Zhang: JPEG/resize**menghancurkan** artefak upsampling; tentang citra, bukan video. Menunjukkan generalisasi, bukan ketahanan degradasi. |
| **[9] Zhang** (10)   | "FFT menangkap amplitudo**dan fase** di semua frekuensi [9]"                      | Zhang eksplisit:**"phase information is discarded"** — hanya log-magnitude. Pindahkan klaim fase ke **[25]/[26]**.                       |
| **[4] MesoNet** (2)  | taksonomi artefak termasuk "inkonsistensi pencahayaan" [4]                        | MesoNet: deepfake justru "same illumination and expression". Taksonomi tak ada di paper. →**[14]**                                       |
| **[4] MesoNet** (10) | trailing "[4]" pada "XceptionNet melampaui ResNet & MesoNet"                      | Di paper [4], Xception fine-tune mereka**96,1/93,5%**, di BAWAH MesoNet 98,4%. Hapus tag [4].                                            |

### 3c. Klaim domain frekuensi tertukar/salah label (inti argumen frekuensi skripsi)

| Ref                        | Kalimat (ringkas)                                                                                                       | Masalah                                                                                                                                | Perbaikan                                                 |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| **[11] Qian/F3-Net** (3)   | "meningkatkan generalisasi pada**berbagai dataset** [11]"                                                               | F3-Net hanya diuji di FF++ (lintas kompresi), tak pernah lintas-dataset                                                                | "...pada**berbagai tingkat kompresi** di FaceForensics++" |
| **[11] Qian** (4)          | "belajar interaksi spasial-frekuensi**dari layer konvolusi pertama**, butuh input multi-channel" (framing early-fusion) | F3-Net**bukan** early fusion; dua stream frekuensi difusi belakangan; malah memperingatkan FFT/DCT mentah "infeasible" utk CNN vanilla | Ganti contoh / hapus framing early-fusion                 |
| **[11] Qian** (7)          | "CNN utk freq clues (mis. melalui representasi**FFT**) [11]"                                                            | F3-Net pakai**DCT**                                                                                                                    | Hapus "FFT" / ganti "DCT"                                 |
| **[11] Qian** (10)         | "high-freq clues lebih stabil thd variasi domain → deteksi**unseen datasets** lebih baik [11]"                          | Robustness F3-Net thd**kompresi**, bukan domain shift; tak ada uji unseen-dataset                                                      | Ubah ke "kompresi"                                        |
| **[12] Tan/FreqNet** (4)   | "detektor frekuensi lebih baik pada**citra terkompresi** [12]"                                                          | FreqNet tak punya eksperimen kompresi (fokus generalisasi lintas-GAN)                                                                  | Pindahkan ke**[11]**                                      |
| **[13] Alam/SpecXNet** (4) | "deepfake beda signifikan pada**band frekuensi menengah** [16][13]"                                                     | SpecXNet lapor sinyal**frekuensi tinggi/periodik** (radial lines, symmetry), bukan mid-band                                            | Hapus "menengah"                                          |
| **[16] FSBI** (6)          | "FSBI lapor deepfake beda di**band frekuensi menengah**"                                                                | FSBI pakai DWT (detail frekuensi tinggi), tanpa klaim mid-band                                                                         | Hapus "menengah"                                          |
| **[16] FSBI** (11)         | "metode frekuensi seperti**FFT** lebih tahan lintas dataset [16]"                                                       | FSBI pakai**DWT/wavelet**, bukan FFT                                                                                                   | Ganti label ke "DWT"                                      |

### 3d. Lain-lain

| Ref               | Kalimat (ringkas)                                                     | Masalah                                                                                                                               | Perbaikan                                                                |
| ----------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **[1] Korshunov** | "tingkat geopolitik: instrumen disinformasi & propaganda [1]"         | Paper soal kerentanan face recognition + database VidTIMIT; kata propaganda/disinformasi tak ada (hanya sebut fake-news tangan-kedua) | Ganti ke**[14]** Rana (abstraknya sebut "misinformation and propaganda") |
| **[19] Chadha**   | "...hiburan, film, lip-sync translation, dan**virtual reality** [19]" | "virtual reality" tak ada di Chadha (paper sebut*video games*)                                                                        | Hapus "virtual reality" / ganti "video game"                             |

---

## 4. LEMAH — Sebaiknya Diperhalus atau Diberi Sumber Tambahan (prioritas sedang)

- **[41] Goodfellow** (1): sitasi importance-of-optimizer OK, tapi klausa alasan spesifik-deepfake bukan dari buku.
- **[5] ResNet** (5): "degradasi **gradien**" salah kaprah — ResNet eksplisit menyatakan degradasi **bukan** dari vanishing gradient. Ubah ke "degradasi akurasi/optimasi".
- **[6] Xception** (7): rumus kompleksitas DSC dari MobileNets/Howard, bukan Chollet. (10): max-pooling **bukan** "setiap blok" (hanya entry/exit flow). (13): Xception ≈ jumlah parameter InceptionV3 (bukan "parameter lebih sedikit utk kapasitas setara"); ganti "penggunaan parameter lebih efisien".
- **[38] SE-Net** (2): "terinspirasi sistem visual manusia" tak ada di paper. (6): "SE > concatenation/addition utk fusi multi-domain" adalah ekstrapolasi (SE = rekalibrasi kanal single-stream ImageNet).
- **[8] Durall** (1): "penyebab utama kegagalan generalisasi" bukan framing Durall. (6): "kehilangan informasi lokasi spasial" inferensi penulis. (8): istilah "spectral fall-off" & "rasio band tinggi/rendah" bukan mekanisme paper (Durall pakai profil azimuthal penuh → SVM).
- **[9] Zhang** (4): alasan deteksi lintas-arsitektur terbalik — generalisasi Zhang dari artefak upsampling **bersama**, bukan "fingerprint unik" tiap GAN.
- **[10] Giudice** (1): "anomali konsisten **antar-arsitektur** GAN" keliru — GSF justru fingerprint **per-arsitektur** (dipakai membedakan arsitektur). Ubah "architecture-specific".
- **[31] Mejri** (1): "tekstur kulit terlalu halus" tak ada di Mejri (paper: fake justru punya **ekstra** noise frekuensi tinggi). (2): "kompresi merusak petunjuk frekuensi tinggi" tak dinyatakan Mejri (hanya sebut kompresi sbg tantangan).
- **[16] FSBI** (5): "pola frekuensi stabil meski terkompresi" — FSBI justru bilang kompresi lebih menantang. (8)(9)(10): robustness kompresi/noise tak ditunjukkan; FSBI = DWT-preproc + 1 CNN, bukan dua cabang spasial+frekuensi; tak ada perbandingan single-vs-hybrid.
- **[14] Rana**: (a) daftar artefak "pencahayaan/bayangan/distorsi geometrik" tak ada di Rana (cocok [4]); (b) "AUC threshold-independent" tak dijelaskan Rana; (c) "imbalance kelas/distribusi" tak dibahas Rana.
- **[4] MesoNet** (1): "keterbatasan pada citra resolusi tinggi" — justru MesoNet dirancang utk video terkompresi/low-res. (5)(6)(8)(9): fokus mesoscopic/blur, bukan blending-warping eksplisit.
- **[7] FFPP** (18)(20): "melampaui ResNet" — FFPP tak menguji ResNet-50 (menguji MesoNet). (4)(7)(11)(16)(3): pernyataan latar/spektral/kritik-diri disandarkan ke paper dataset.
- **[23] StackOverflow**: sumber lemah utk skripsi (Gambar 2.1 low/high-freq); lebih kokoh pakai [24].

---

## 5. Terverifikasi SESUAI (tidak perlu diubah — untuk ketenangan)

- **Optimizer & training:** [44] Adam (moment, β 0.9/0.999, ε), [45] AdamW (tanpa konflasi dgn Kingma), [43] Ruder, [47] MTCNN (P/R/O-Net), [48] Dropout 0.5, [35] LeCun, [41] Goodfellow (gradient clipping L2).
- **Teori spektral:** [25] Oppenheim (fase bawa struktur), [26] Liu SPSL (fase & upsampling), [29] Rahaman (low-freq first), [30] Wang (high-freq & generalisasi), [21] Odena (checkerboard), [24] Gonzalez & Woods (fase/magnitudo, f(x,y), f(x,y,t)).
- **Dataset:** [18] Celeb-DF (5639 video, 59 selebriti, kualitas ditingkatkan) — semua benar.
- **Deteksi frekuensi (inti benar):** [8] Durall (kegagalan distribusi spektral, azimuthal, replika high-freq), [17] Luo/FMSI (dual-stream spasial+frekuensi) — semua SESUAI, [11]/[12]/[13]/[16] core-nya benar (hanya sub-klaim label yang salah).
- **Temporal/domain:** [32] Kim (temporal-freq inconsistency), [36] Haliassos (gerak bibir + temporal), [46] Ben-David (galat target ≤ galat sumber + divergensi), [40] Sabir (frame-level + jittering/flickering — kecuali klaim frekuensi), [39] Ma, [15] Rao.

---

## 6. Rekomendasi Prioritas

1. **Perbaiki dulu yang bertentangan (§3b)** — ini paling berbahaya jika ditanya penguji: [7] kompresi, [9] fase & kualitas video, [4] pencahayaan & "Xception>MesoNet".
2. **Betulkan salah-label frekuensi (§3a, §3c)** — "FFT" pada paper DCT/DWT ([11],[16]), "band menengah" pada paper high-freq ([13],[16]), dan tukar kompresi↔lintas-dataset ([11]↔[12]). Ini pola sistemik; sekali paham polanya, cepat dibereskan.
3. **Relokasi klaim salah-paper (§3a)** — Gambar 2.2 [48]→[24]; [6] frekuensi→[8]/[11]; [27] deteksi→[4]/[9]; [40] frekuensi→[31]; [1] propaganda→[14]; [14] spektral→[8].
4. **Tangani 6 referensi yatim (§2)** — sitasi atau hapus.
5. **Perhalus LEMAH (§4)** bila sempat — tidak mengubah substansi, tapi memperkuat pertanggungjawaban.

> Semua verdikt di atas berbasis pembacaan teks penuh tiap PDF sumber. Jika ingin, saya bisa lanjut menyiapkan kalimat pengganti siap-tempel untuk butir §3, atau menyisir langsung ke `.docx` untuk mengecek apakah tiap `[N]` berupa teks biasa vs field cross-reference sebelum diedit.
