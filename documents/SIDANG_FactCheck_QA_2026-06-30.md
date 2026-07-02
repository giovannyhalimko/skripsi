# Sidang — Fact-Check & Q&A (Living Document)

> Dokumen ini dipakai untuk memverifikasi fakta/pernyataan thesis terhadap **kode aktual** dan **data hasil run**, sekaligus menyiapkan jawaban sidang.
> Setiap kali ada pertanyaan/pernyataan/fakta baru, dokumen ini **di-update** (tambah item baru di bawah).
>
> Legenda verdict: ✅ BENAR · 🟡 BENAR TAPI PERLU DIPERTEGAS · 🔴 KELIRU/OVERSTATED
>
> Konvensi referensi kode: `path:baris` relatif terhadap `deepfake_hybrid/`.
> Live .docx dapat dibaca via symlink repo-root `live-thesis-document.docx` (unzip `word/document.xml`).
> Terakhir diperbarui: 2026-06-30.

## Daftar Item

1. [Rasio sampling 50:50 real vs fake](#item-1)
2. [Kenapa pembagian 70/15/15? (bukan 50/25/25 atau 80/10/10)](#item-2)
3. [FFT untuk &#34;ekstraksi fitur spektral&#34; — benar, atau seharusnya &#34;melihat high frequency&#34;?](#item-3)
4. [High frequency dipakai, low frequency &#34;tidak digunakan&#34; — benar?](#item-4)
5. [Sudah tahu fase &gt; magnitudo di BAB II, kenapa tetap pakai magnitudo saja? (handicap / rescope?)](#item-5)
6. [Deskripsi late fusion BAB II: &#34;concat → classifier&#34; — padahal ada proyeksi + SE gating di antaranya?](#item-6)
7. [🔴 &#34;Kedua strategi fusion (early + late) diimplementasikan DAN dievaluasi&#34; — padahal hanya late fusion yang dievaluasi](#item-7)
8. [Referensi: apa itu &#34;power spectrum&#34; (Durall et al. 2020) dan hubungannya ke representasi FFT kita](#item-8)
9. [&#34;Local&#34; vs &#34;global&#34; (SpecXNet) — kalian global atau lokal untuk spasial &amp; frekuensi?](#item-9)
10. [🔴 &#34;XceptionNet unggul pada FF++, DFDC, dan Celeb-DF [13, 7]&#34; — referensi hanya mendukung FF++](#item-10)
11. [🔴 &#34;Dalam penelitian ini FFT jadi kanal keempat input XceptionNet + DSC cocok&#34; — itu early fusion, bukan flow kita](#item-11)
12. [🔴 &#34;korelasi spasial (cross-channel) dan korelasi antarkanal (cross-spatial)&#34; — label Inggris tertukar](#item-12)
13. [🟡 Repetisi: pembuka seksi DSC &amp; §2.7 XceptionNet mengulang hal sama (+ dua daftar keunggulan tumpang-tindih)](#item-13)
14. [✅ &#34;SE block &gt; konkatenasi sederhana&#34; padahal kita pakai konkatenasi — kontradiksi? TIDAK](#item-14)
15. [🟡 Tingkat kompresi FFPP: HQ &amp; LQ tak diberi label c23/c40 (benar HQ=c23, LQ=c40)](#item-15)
16. [🔴 Daftar &#34;Artefak Spasial&#34;: butir (d) &#34;ekspresi antar-frame&#34; itu TEMPORAL, bentrok dgn frame-level](#item-16)
17. [🟡 Struktur membingungkan: dikotomi artefak spasial/frekuensi diulang 3x dengan 3 format berbeda](#item-17)
18. [🟡 &#34;Alasan Pemilihan FFPP&#34;: 3 klaim faktual tanpa sitasi (+ &#34;GAN dan non-GAN&#34; kurang tepat)](#item-18)

---

<a name="item-1"></a>

## Item 1 — "Pengambilan sampel dilakukan dengan rasio 50:50 antara kelas asli dan kelas manipulasi"

**Verdict: 🟡 BENAR, tapi tegaskan cakupannya = level VIDEO (bukan level frame).**

### Bukti kode

Diterapkan di pipeline kanonik `scripts/extract_frames.py:180-194` (bukan `sample_dataset.py`, itu skrip smoke-test lama):

```python
half = args.n_samples // 2
real_take = min(len(real_all), half)
fake_take = min(len(fake_all), args.n_samples - real_take)
selected = real_all[:real_take] + fake_all[:fake_take]
```

Lalu `scripts/build_splits.py:52-53` memakai `train_test_split(..., stratify=df["label"])`, sehingga rasio 50:50 **dipertahankan** di tiap subset train/val/test.

### Bukti data hasil run (manifest aktual)

| Run                     | Video           | Real           | Fake           |
| ----------------------- | --------------- | -------------- | -------------- |
| FFPP n100 / n250 / n500 | 100 / 250 / 500 | 50 / 125 / 250 | 50 / 125 / 250 |
| CDF n100 / n250 / n500  | 100 / 250 / 500 | 50 / 125 / 250 | 50 / 125 / 250 |

Semua **persis 50:50** di level video. Konsisten dengan BAB III v4 baris 104 ("pengambilan **video** dilakukan secara seimbang ... rasio 50:50").

### Catatan untuk sidang

- **50:50 itu di level VIDEO, bukan frame.** Model dilatih per-frame; `src/deepfake_data.py:79-81` ambil hingga `max_frames` per video, jadi jumlah frame per kelas bisa sedikit timpang. Karena itu `scripts/train.py:182-184` menghitung `pos_weight = n_neg / n_pos` (pengaman residual imbalance level frame; bernilai ~1.0 kalau benar seimbang).
- **50:50 di kode itu _best-effort_.** Kalau satu kelas kurang, kode menambal dari kelas mayoritas (`extract_frames.py:185-189`). Untuk FFPP (~1000 real) & CDF (~590-890 real), real selalu cukup untuk setengah sampel terbesar (butuh max 500 real di FFPP n1000, 375 di CDF n750), jadi 50:50 terealisasi.
- **Seed sampling di-hardcode = 42** (`extract_frames.py:174`), terpisah dari 3 seed training (0/1/2). Set video 50:50 yang sama dipakai di ketiga seed; yang berbeda hanya stokastisitas pelatihan.

**Frasa thesis paling akurat:** "pengambilan video secara seimbang (50:50 pada level video)".

---

<a name="item-2"></a>

## Item 2 — "Kenapa 70/15/15? Kenapa tidak 50/25/25 atau 80/10/10?"

**Verdict: ✅ Pilihan 70/15/15 dapat dipertahankan dengan baik.**

Referensi kode: `scripts/build_splits.py:18-19` (`--val-size 0.15`, `--test-size 0.15`), split bertingkat `train_test_split` dua tahap (baris 52-53), stratified by label, level video.

### Jawaban inti (3 argumen)

**1. Mengikuti konvensi benchmark FaceForensics++.**
Split resmi FF++ adalah **720 train / 140 val / 140 test video** dari 1000 video = **72% / 14% / 14%**. Jadi 70/15/15 pada dasarnya **mereplikasi rasio split kanonik FF++**, bukan angka yang dibuat sembarangan. Ini membuat hasil sebanding dengan literatur deteksi deepfake di dataset yang sama.

**2. Keseimbangan: cukup data latih untuk backbone besar, sekaligus set evaluasi yang stabil.**

- XceptionNet ≈ 22,8 juta parameter butuh data latih memadai. 70% memberi proporsi latih terbesar yang masuk akal **tanpa mengorbankan keandalan evaluasi**.
- 15% validasi penting karena **seleksi model & early stopping memakai AUC validasi** (`train.py`, kriteria best checkpoint by val AUC). Val terlalu kecil → sinyal AUC bising → checkpoint salah pilih / early stopping prematur.
- 15% test cukup besar untuk estimasi metrik yang relatif stabil.

**3. Kendala mengikat ada di tier sampel kecil (n=100), pada level video.**

- Split di level video, bukan frame (cegah kebocoran). Pada n=100: 15% = **15 video** untuk val dan 15 untuk test.
- Dengan **80/10/10**: val/test tinggal **10 video** → AUC sangat bising, terutama untuk model selection. Tidak layak pada tier kecil.
- Dengan **50/25/25**: latih turun ke **50 video** → XceptionNet kekurangan data, underfit, variansi antar-seed melonjak; sekaligus boros (25% test jauh lebih besar dari yang diperlukan untuk estimasi metrik).
- **70/15/15** = titik tengah: 70 video latih (cukup untuk fine-tuning + freeze/unfreeze backbone), 15 val (sinyal early stopping memadai), 15 test. Tiap video → hingga 50 frame, jadi metrik level frame tetap dihitung atas ~750 frame/subset, tetapi **diversitas video val/test** adalah batasan yang menentukan, dan 15 lebih aman daripada 10.

### Ringkas satu kalimat (untuk dilempar ke penguji)

> "70/15/15 mengikuti rasio split resmi FaceForensics++ (720/140/140 ≈ 72/14/14), memberi data latih cukup untuk backbone Xception sekaligus set validasi yang besarnya memadai untuk early stopping berbasis AUC; 80/10/10 membuat val/test hanya 10 video pada tier n=100 (AUC tidak stabil), sedangkan 50/25/25 menyusutkan data latih hingga model underfit."

---

<a name="item-3"></a>

## Item 3 — "Analisis frekuensi dilakukan menggunakan metode FFT untuk mengekstraksi fitur spektral yang merepresentasikan artefak sintesis"

**Verdict: 🟡 BENAR, tapi tidak lengkap — ada langkah _high-pass filtering_ yang menyaring spektrum ke arah frekuensi tinggi.**

### "Ekstraksi fitur spektral" — benar?

Ya. Pipeline FFT (`src/fft_utils.py:22-33`):

1. Grayscale → resize 224×224
2. `np.fft.fft2` → `fftshift` → `np.abs` (magnitude spectrum)
3. **High-pass mask** (lihat Item 4)
4. `log1p` → peta **FFT log-magnitude** 1-kanal

Peta log-magnitude inilah **representasi spektral**-nya, dan `FreqCNN` (`src/models/freq_cnn.py`) mempelajari fitur diskriminatif dari peta tersebut. Jadi "FFT untuk mengekstraksi fitur spektral" **akurat** sebagai deskripsi representasi input.

### "Bukan melihat high frequency?" — keduanya, tidak saling bertentangan

Dua framing ini **komplementer**, bukan kontradiktif:

- **Representasi** = peta spektral penuh (FFT log-magnitude 2D). ← inilah "fitur spektral"
- **Penekanan** = high-pass filter membobot peta itu ke arah frekuensi menengah-tinggi, tempat artefak sintesis (checkerboard dari up-convolution GAN, spectral roll-off anomal) terkonsentrasi.

Artinya: FFT memang menghasilkan fitur spektral (benar), dan dari fitur spektral itu **komponen frekuensi tinggi yang ditonjolkan** (juga benar). Pernyataan thesis tidak salah, hanya **menghilangkan** bagian high-pass-nya.

### Dukungan

- Thesis v4 sudah benar mendokumentasikan ini di **§3.3.2.3** (`BAB_III_Tahapan_Pelaksanaan_v4.md:156-170`): "_Magnitude Spectrum_, _High-Pass Filtering_, dan _Log Scaling_".
- Referensi: Durall et al. 2020 (spectral distribution), Odena et al. 2016 (checkerboard artifacts), Mejri et al. (Leveraging High-Frequency Components) — semua ada di `thesis_reference/`.

**Saran:** kalau ada ruang, perlengkap kalimat menjadi: "...menggunakan FFT untuk menghasilkan representasi spektral (log-magnitude) yang **kemudian ditekankan pada komponen frekuensi tinggi via _high-pass filter_** guna menonjolkan artefak sintesis."

---

<a name="item-4"></a>

## Item 4 — "High frequency dipakai untuk mendeteksi artefak, sedangkan low frequency tidak digunakan"

**Verdict: 🔴 OVERSTATED / kurang tepat. Yang benar: low frequency DITEKAN (di-atenuasi), bukan "tidak digunakan".**

### Bukti kode — high-pass-nya _soft_, bukan _hard cut_

`src/fft_utils.py:9-19`:

```python
def _highpass_mask(size, cutoff=0.15):
    ...
    sigma = cutoff * size                 # 0.15 * 224 ≈ 33.6 px
    mask = 1.0 - np.exp(-(dist**2) / (2*sigma**2))
    return mask
```

Diterapkan sebagai perkalian: `magnitude = magnitude * mask` (`fft_utils.py:30-31`), aktif secara default (`highpass=True`) baik di cache (`save_fft_cache` → `image_to_fft_logmag`) maupun di fallback live. Jadi input training **memang** sudah high-pass.

Sifat mask Gaussian `H = 1 − exp(−d²/2σ²)`:

| Posisi (jarak dari pusat) | Nilai mask | Efek                                           |
| ------------------------- | ---------- | ---------------------------------------------- |
| Pusat / DC (d=0)          | **0,00**   | DC dihilangkan                                 |
| d = σ (≈34 px)            | ~0,39      | low-freq**ditekan kuat**, tetap lewat sebagian |
| d = 2σ (≈67 px)           | ~0,86      | mid-freq sebagian besar lewat                  |
| Tepi (high freq)          | →1,00      | high-freq dipertahankan penuh                  |

### Kenapa pernyataan itu keliru

1. **Roll-off mulus, bukan biner.** Hanya DC murni yang dikali ~0. Komponen low/mid-freq **tetap masuk** ke FreqCNN dengan bobot tereduksi. Jadi "low frequency tidak digunakan" terlalu kuat.
2. **Thesis sendiri memakai kata yang benar:** `BAB_III...v4.md:164` menulis "**menekan dominasi** komponen frekuensi rendah" (suppress), bukan "membuang". Pernyataan user lebih ekstrem dari yang sebenarnya diimplementasikan.
3. **FreqCNN tetap menerima peta 224×224 utuh** (low+high, hanya dibobot). Doc depth=5 (`...v2.md:488`) bahkan menyebut model mengekstraksi "dari artefak frekuensi rendah (distribusi energi global) hingga anomali frekuensi tinggi" — jadi info low-freq tidak hilang.

### Frasa yang benar (untuk sidang & thesis)

> "Komponen frekuensi **tinggi diperkuat** dan komponen frekuensi **rendah ditekan (di-atenuasi)** melalui _Gaussian high-pass filter_ (cutoff β=0,15), karena artefak sintesis deepfake terkonsentrasi pada frekuensi menengah-tinggi sedangkan frekuensi rendah sebagian besar merepresentasikan struktur global wajah yang kurang diskriminatif. Frekuensi rendah **tidak dibuang sepenuhnya**, hanya dikurangi dominasinya."

### Jika penguji menekan: "kenapa tidak buang total low-freq?"

Karena (a) transisi mulus menjaga sebagian konteks struktural & mencegah artefak ringing dari pemotongan tajam, dan (b) sebagian sinyal diskriminatif (mis. distorsi distribusi spektral / spectral roll-off, Durall et al. 2020) berada di pita menengah, bukan hanya tepi — sehingga atenuasi bertahap lebih aman daripada hard cut.

---

<a name="item-5"></a>

## Item 5 — "Di BAB II kalian sudah tahu fase membawa lebih banyak info daripada magnitudo. Kenapa tetap _kekeh_ meng-_handicap_ cabang frekuensi dengan magnitudo saja? Bukankah lebih baik penelitian di-_scope_ ulang?"

**Verdict: ✅ Bisa dipertahankan kuat — ini keterbatasan desain yang DISENGAJA, terdokumentasi konsisten, dan justru memperkuat narasi komparatif. JANGAN di-rescope.**

### Lokasi di .docx (live)

- **BAB II §2.4.3 "Spektrum Magnitudo dan Fase"** (paragraf yang ditanyakan) — memperkenalkan magnitudo vs fase, mengakui keterbatasan magnitudo-saja, mengutip Oppenheim & Lim [25] dan Liu et al. SPSL [26].
- **Metodologi** (≈hal. representasi frekuensi): "Spektrum ... dikonversi menjadi satu kanal ... menonjolkan pola energi frekuensi tinggi."
- **BAB V Keterbatasan #3**: "cabang frekuensi ... hanya menggunakan spektrum magnitudo ... dan membuang spektrum fase ... representasi spektral yang tidak lengkap sejak awal."
- **BAB V Saran/Future Work**: merekomendasikan menyertakan fase (SPSL) sebagai penelitian lanjutan.

Jadi ini **bukan kelalaian yang ketahuan**, melainkan batas desain yang sengaja dinyatakan dan konsisten di tiga bab. Itu sendiri adalah aset pertahanan.

### Kunci pertahanan (4 argumen, urut kekuatan)

**1. Ini STUDI KOMPARATIF, bukan studi optimasi representasi frekuensi.**
Judulnya "Studi Komparatif Kinerja ... Arsitektur Hybrid ... terhadap Model Domain Tunggal." Variabel yang diteliti adalah **arsitektur** (hybrid vs single-domain), dengan **representasi frekuensi dijaga tetap (fixed)** pada pilihan kanonik. Supaya perbandingan terkontrol dan sebanding dengan literatur, representasinya dipatok ke yang **paling baku** di domain ini: log-magnitude spectrum (Durall et al. 2020, Frank et al. 2020, Wang et al. 2020). Mengganti ke fase/SPSL akan **mengubah variabel bebas** dan menjadikannya penelitian yang berbeda (perbandingan representasi: magnitudo vs fase vs gabungan) — itu skripsi lain, bukan milik kami.

**2. Oppenheim & Lim itu tentang STRUKTUR PERSEPTUAL, bukan deteksi ARTEFAK — dua klaim itu tidak bertentangan.** ← _senjata utama_
Hasil Oppenheim & Lim (1981) menunjukkan fase mendominasi **struktur perseptual citra natural** (tepi, bentuk, keterbacaan rekonstruksi). Tetapi **deteksi deepfake bukan rekonstruksi struktur** — ia menargetkan **anomali statistik spektral / artefak** (puncak spektral up-sampling GAN, spectral roll-off, replika checkerboard), dan artefak ini justru **termanifestasi kuat pada spektrum magnitudo** (Durall, Frank, Wang). Jadi:

> "Fase membawa lebih banyak info **struktur**" dan "magnitudo adalah kanal **artefak** yang sah" **keduanya benar dan tidak saling meniadakan.**

SPSL (Liu et al. [26]) menunjukkan fase **menambah** sinyal artefak yang **komplementer** (artefak up-sampling kumulatif) — _bukan_ membuktikan magnitudo tak berguna. Maka framing "fase lebih penting → magnitudo = handicap" adalah **kesimpulan yang melompat**: yang benar, fase itu **komplementer dan menjadi arah lanjutan**, bukan pengganti yang membuat magnitudo sia-sia.

**3. Keterbatasan ini MENJELASKAN temuan empiris — itu sains yang baik, bukan lubang.**
Hasil kami: cabang frekuensi adalah model **terlemah**, dan hybrid didominasi cabang spasial (ranking spatial ≥ hybrid > freq, konsisten lintas seed & tier 250/500/750). Paragraf BAB II ini memberi **penjelasan mekanistik** atas hasil negatif itu: representasi magnitudo-saja (ditambah hilangnya sidik jari spektral akibat face-crop & kompresi) → cabang frekuensi lemah. Tanpa paragraf ini, hasil lemah itu **tak terjelaskan**; dengan paragraf ini, hasil jadi **interpretable dan jujur**. Penguji menghargai limitation yang **memprediksi & menjelaskan** hasil, bukan menyembunyikannya.

**4. Justifikasi praktis: magnitudo-saja itu baku, reproducible, dan bersih secara arsitektur.**
Single-channel → cocok dengan FreqCNN 1-kanal, bisa di-_cache_ sebagai `.npy`. Fase **tidak** drop-in: ada _phase wrapping_, sensitif noise, tidak translation-invariant; SPSL butuh pemrosesan _shallow_ khusus. Menyertakan fase secara benar = arsitektur + eksperimen baru = **scope creep** di luar studi komparatif.

### Jawaban siap-ucap (30 detik)

> "Penelitian kami adalah **studi komparatif arsitektur**, jadi representasi frekuensi sengaja kami patok pada bentuk **paling baku** di literatur, yaitu log-magnitude spectrum, agar perbandingan hybrid vs domain-tunggal terkontrol dan sebanding. Soal Oppenheim & Lim: hasil itu menyatakan fase dominan untuk **struktur perseptual citra**, sedangkan deteksi deepfake menargetkan **artefak spektral** yang justru kuat di magnitudo, jadi keduanya tidak bertentangan — fase bersifat **komplementer**. Kami **tidak mengklaim** cabang frekuensi kami yang terkuat; kami melaporkan apa adanya bahwa ia terlemah, dan paragraf BAB II itulah yang **menjelaskan kenapa**. Penggunaan fase (mis. SPSL) sudah kami nyatakan eksplisit sebagai **keterbatasan dan saran penelitian lanjutan** di BAB V. Mengganti ke fase sejak awal berarti menjawab **pertanyaan riset yang berbeda** (perbandingan representasi), bukan pertanyaan kami (perbandingan arsitektur)."

### Rebuttal lanjutan kalau ditekan lebih jauh

- **"Fase kan tinggal ditambah, murah?"** → Tidak murah/bersih: butuh unwrapping, noise-sensitive, bukan flag konfigurasi; SPSL metode khusus. Implementasi yang benar = arsitektur + matriks eksperimen baru.
- **"Cabang frekuensi lemah, bukankah hybrid jadi tak valid?"** → Tidak. Hybrid tetap memetik manfaat dari cabang spasial; perbandingan kami justru **mengukur seberapa besar (atau kecil) kontribusi frekuensi** — dan jawabannya (kontribusi terbatas pada kondisi ini) adalah temuan ilmiah yang sah dan jujur.
- **"Harusnya pakai fase dari awal?"** → Itu menjawab pertanyaan "representasi frekuensi terbaik", bukan "perbandingan arsitektur". Dua skripsi berbeda; kami memilih dan **membatasi** milik kami secara eksplisit.

### Opsional — pelunakan teks BAB II (kalau mau menutup celah di paragrafnya sendiri)

Kerentanan satu-satunya: kalimat "rekonstruksi hanya dari magnitudo justru kehilangan struktur" bisa dibaca seakan magnitudo inferior **secara menyeluruh**. Bila ingin pre-empt di teks (bukan wajib), sisipkan satu klausa setelah kalimat Oppenheim:

> "Perlu ditekankan bahwa hasil tersebut berlaku untuk **rekonstruksi struktur perseptual citra natural**; dalam konteks deteksi, spektrum **magnitudo** tetap menjadi kanal yang mapan untuk menangkap **artefak distribusi spektral** akibat sintesis generatif (Durall et al., 2020), sehingga fase bersifat **komplementer** terhadap magnitudo, bukan substitusi."

Ini mengubah paragraf dari "mengakui kelemahan" menjadi "mengakui kelemahan **sambil membingkai fase sebagai pelengkap**", sehingga lebih sulit dijadikan jebakan. (Edit dilakukan dari Drive — teks di atas tinggal di-_paste_.)

---

<a name="item-6"></a>

## Item 6 — Deskripsi late fusion di BAB II ("...digabungkan _concatenated_ dan diteruskan ke lapisan klasifikasi bersama") vs implementasi aktual (ada proyeksi + SE gating)

**Verdict: 🟡 BENAR sebagai deskripsi UMUM (landasan teori), tapi merupakan PENYEDERHANAAN. Pengamatanmu tepat — model aktual menyisipkan proyeksi-256 lalu SE gating di antara concat dan classifier. Bukan kontradiksi: kedua langkah itu sudah didokumentasikan di tempat lain (BAB II §SE-Net + BAB III §HybridTwoBranch).**

### Alur AKTUAL model (verifikasi kode `src/models/hybrid_fusion.py`)

```
RGB → Xception → spatial_feat (2048)  → Linear(2048→256)+BN+ReLU ┐   (spatial_proj, L35-39)
                                                                 ├ cat → 512 (L64)
FFT → FreqCNN.features → flatten (512) → Linear(512→256)+BN+ReLU ┘   (freq_proj, L40-44)
                                                                 │
   → SE gate(512): Lin(512→128)→ReLU→Lin(128→512)→Sigmoid, lalu x*gate(x)   (L11-24, dipanggil L65)
   → classifier: Dropout(0.5)→Lin(512→128)→ReLU→Dropout(0.5)→Lin(128→1)     (L48-54, dipanggil L66)
```

Jadi urutan sebenarnya: **proyeksi → concat → SE gating → classifier (yang diawali Dropout).** Persis seperti dugaanmu: setelah concat ada **SE gating** dulu, baru **classifier yang dimulai dengan dropout**.

### Apa yang BENAR di paragraf BAB II (line 418 docx)

- ✅ Dua cabang independen mengekstraksi fitur terpisah — cocok (`self.spatial(rgb)`, `self.freq.features(fft)`).
- ✅ Cabang spasial CNN (misalnya XceptionNet) — cocok.
- ✅ Cabang frekuensi CNN lebih ringan — cocok (FreqCNN ~0,7 jt vs Xception ~22,8 jt param).
- ✅ Digabungkan (_concatenated_) → akhirnya menuju lapisan klasifikasi — cocok.
- ✅ Fleksibilitas pilih arsitektur per domain — properti umum late fusion yang sah.

### Apa yang DIHILANGKAN (dua langkah, keduanya nyata di model)

1. **Proyeksi per-cabang ke 256-d (Linear+BN+ReLU)** sebelum concat — penyetara dimensi 2048 vs 512 supaya spasial tidak mendominasi.
2. **SE gating** pada vektor fusi 512-d — _channel attention_ adaptif sebelum classifier.

### Kenapa ini BUKAN error / bukan inkonsistensi

Paragraf line 418 ada di **§2.7 (landasan teori "Pendekatan Hybrid")** sebagai **definisi UMUM** late fusion — ditandai kata "**misalnya** XceptionNet" dan sitasi ke karya **lain** [11, 13], bukan klaim langkah-demi-langkah model kami. Proyeksi & SE gating bukan ciri pendefinisi late fusion secara umum, melainkan **enhancement** kami, dan keduanya didokumentasikan pada altitude yang tepat:

- **§2.8 "Squeeze-and-Excitation Networks"** (docx line 633-651): konsep SE, channel attention, squeeze/excitation/scale, plus peran SE sebagai "**mekanisme fusi adaptif**" saat fitur spasial+frekuensi dikonkatenasi.
- **§2.x Persamaan proyeksi** (docx line 652-653): proyeksi ke dimensi seragam (Linear+BN+ReLU) "**sebelum diproses mekanisme channel attention seperti SE gating**".
- **BAB III §HybridTwoBranch** (docx line 1344-1353): instansiasi spesifik — proyeksi 256 → konkatenasi 512 → "**diterapkan SE gating [38]**" → classifier.
- **Judul/Abstrak**: arsitektur disebut eksplisit "late fusion **dan Squeeze-and-Excitation gating**".

Jadi strukturnya benar: §2.7 konsep umum → §2.8 SE sebagai penyempurnaan → BAB III menggabungkannya. Tidak ada yang disembunyikan; hanya **beda altitude** (konsep umum vs instansiasi spesifik).

### Catatan kecil: "tanpa saling mengganggu"

Klaim "setiap branch mengekstraksi fitur secara spesifik **tanpa saling mengganggu**" benar **pada tahap ekstraksi** (kedua cabang forward-pass independen). Tapi pada tahap **fusi**, SE gating justru membuat kedua cabang **berinteraksi** (bobot gerbang dihitung dari vektor gabungan 512-d, jadi fitur frekuensi ikut memengaruhi penskalaan fitur spasial dan sebaliknya). Karena kalimat itu menyangkut **ekstraksi**, ia tetap akurat — tapi jangan sampai diparafrase jadi "kedua domain tidak pernah berinteraksi", karena SE gating dirancang justru untuk fusi adaptif lintas-domain.

### Jawaban siap-ucap kalau penguji menyorot

> "Paragraf di BAB II itu adalah **definisi umum** late fusion sebagai landasan teori, makanya pakai 'misalnya XceptionNet' dan mengutip karya lain. Arsitektur spesifik kami menambahkan dua langkah di jalur fusi: **proyeksi kedua cabang ke 256 dimensi** untuk menyetarakan magnitudo, lalu **SE gating** sebagai atensi kanal adaptif sebelum classifier. Keduanya kami bahas di sub-bab tersendiri (Squeeze-and-Excitation Networks) dan dirinci pada BAB III sub-bab HybridTwoBranch, serta disebut eksplisit di judul dan abstrak. Jadi alur penuhnya: proyeksi → konkatenasi → SE gating → classifier; deskripsi BAB II hanya pada tingkat konsep umum."

### Opsional — tutup celah (kalau mau)

Bila ingin paragraf §2.7 tidak terbaca sebagai spesifikasi penuh model, tambahkan satu klausa penutup pengarah ke §2.8:

> "Pada penelitian ini, sebelum diteruskan ke lapisan klasifikasi, vektor hasil konkatenasi terlebih dahulu disetarakan dimensinya melalui proyeksi dan dibobot secara adaptif menggunakan _Squeeze-and-Excitation gating_ (dibahas pada sub-bab 2.8)."

Tidak wajib — struktur §2.7→§2.8 sudah logis. (Edit dari Drive bila diperlukan.)

---

<a name="item-7"></a>

## Item 7 — "Dalam penelitian ini, kedua strategi fusion diimplementasikan dan **dievaluasi** ... **Perbandingan kedua strategi** ini bertujuan mengidentifikasi pendekatan paling efektif"

**Verdict: 🔴 KELIRU / OVERCLAIM — HARUS DIPERBAIKI sebelum sidang. _Early fusion_ memang ADA di kode (`diimplementasikan` benar), tetapi TIDAK pernah masuk eksperimen, TIDAK ada di tabel hasil, TIDAK di BAB IV, dan TIDAK di abstrak. Yang dievaluasi dan diperbandingkan hanya 3 model: spatial, freq, hybrid (late fusion). Intuisimu benar.**

### Ini temuan paling rawan sejauh ini — penguji bisa mematahkannya dengan satu pertanyaan: _"Tunjukkan hasil early fusion-nya / mana perbandingan early vs late?"_

### Bukti

**1. Matriks eksperimen tidak menyertakan early fusion** (`scripts/run_all.py`):

```python
MODELS_CORE = ["spatial", "freq", "hybrid"]          # L23
...
models_to_run = MODELS_CORE.copy()                    # L139
if cfg.get("fusion_mode", "two_branch") == "early_fusion":   # L140
    models_to_run.append("early_fusion")              # L141  ← hanya jika fusion_mode == early_fusion
```

Config kanonik `config.yaml` → `fusion_mode: two_branch`. Jadi cabang `if` **tidak pernah aktif** → early fusion **tidak pernah dilatih/dievaluasi** pada konfigurasi penelitian.

**2. Tidak ada di tabel hasil.** Kolom `model` di semua `Table1_in_dataset.csv` / `Table2_cross_dataset.csv` hanya berisi: **`['freq', 'hybrid', 'spatial']`**. Tidak ada `early_fusion`.

**3. Tidak ada di BAB IV / hasil.** Pencarian "early fusion" di docx hanya muncul di: §2.7 konsep (line 415-416), **klaim bermasalah ini** (line 420), dan satu kalimat BAB III soal _freezing_ (line 1458). Nol baris hasil.

**4. Abstrak membantah klaim ini sendiri:** "**Tiga model** (spasial, frekuensi, dan hybrid) dievaluasi ...". Tiga, bukan empat. Tidak ada early fusion.

### Status sebenarnya per kata

- "**diimplementasikan**" → ✅ BENAR. `EarlyFusionXception` ada (`hybrid_fusion.py:70-78`), `train.py` mendukung `--model early_fusion` (L129, L67-68), dataset mendukung mode 4-kanal (`deepfake_data.py:149`). Bisa dijalankan.
- "**dievaluasi**" → 🔴 SALAH. Tidak ada dalam eksperimen/hasil yang dilaporkan.
- "**Perbandingan kedua strategi ... pendekatan paling efektif**" → 🔴 SALAH. Tidak ada perbandingan early-vs-late di mana pun.

### Inkonsistensi terkait yang ikut harus dirapikan

**BAB III line 1458** menyebut "...model spatial, hybrid, **dan early fusion**, backbone dibekukan..." — ini juga **menyiratkan early fusion adalah model yang dilatih**. Karena tidak dievaluasi, frasa "dan early fusion" sebaiknya dibuang dari kalimat metodologi itu (atau kalimatnya diubah ke "kode mendukung, namun tidak digunakan").

### Rekomendasi perbaikan (WAJIB) — opsi termurah & jujur

Pertahankan **deskripsi konsep** early fusion di §2.7 (line 415-416) sebagai landasan teori (boleh — itu teori). Tapi **ganti klaim evaluatif** di line 420. Contoh teks pengganti:

> "Penelitian ini berfokus pada strategi **late fusion**, yang diimplementasikan melalui arsitektur _two-branch_ yang menggabungkan XceptionNet untuk fitur spasial dan CNN ringan untuk fitur frekuensi, dilengkapi _Squeeze-and-Excitation gating_. Strategi _early fusion_ (XceptionNet 4-kanal RGB+FFT) disajikan sebagai **alternatif konseptual** dan didukung oleh implementasi kode, namun **tidak menjadi fokus evaluasi eksperimental** pada penelitian ini; pemilihan late fusion didasari fleksibilitas pemodelan arsitektur yang berbeda untuk tiap domain."

Lalu di line 1458 ganti "...model spatial, hybrid, dan early fusion..." → "...model spatial dan hybrid...".

### Kalau penguji terlanjur bertanya "katanya dievaluasi keduanya?"

> "Mohon koreksi pada kalimat tersebut, Pak/Bu — yang dievaluasi secara eksperimental dalam penelitian ini adalah **late fusion** (model hybrid _two-branch_ + SE gating), sebagaimana konsisten dengan judul, abstrak (tiga model), dan seluruh BAB IV. _Early fusion_ kami implementasikan sebagai opsi arsitektur dan kami bahas secara konseptual, tetapi tidak kami masukkan ke matriks evaluasi. Kalimat di BAB II akan kami perbaiki agar tidak menyiratkan adanya perbandingan empiris early-vs-late."

> ⚠️ **Prioritas tinggi:** ini bukan soal interpretasi seperti Item 5/6 — ini klaim faktual yang tidak didukung data. Perbaiki teks BAB II (line 420) dan BAB III (line 1458) di .docx sebelum sidang.

---

<a name="item-8"></a>

## Item 8 — Referensi: "power spectrum" (Durall et al. 2020, "Watch your Up-Convolution", CVPR) dan hubungannya ke kita

**Bukan verdict — ini referensi konsep** untuk memperkuat Item 3/4/5 dan menjelaskan **kenapa cabang frekuensi kita lemah**. Paper: `thesis_reference/Durall et al - Watch your Up-Convolution...pdf`.

### Definisi bertingkat (jangan tertukar)

| Istilah                        | Rumus                         | Arti                                                                                                                                                                          |
| ------------------------------ | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Magnitude spectrum             | `\|F(u,v)\|`                  | amplitudo tiap frekuensi 2D                                                                                                                                                   |
| **Power spectrum**             | `\|F(u,v)\|²`                 | **energi/daya** tiap frekuensi 2D (Durall Eq. 1, Fig 2 kiri)                                                                                                                  |
| **1D Power Spectrum**          | azimuthal integration (Eq. 2) | peta 2D diringkas jadi**satu kurva** dengan mengintegrasikan daya di lingkaran 360° untuk tiap radius `ω_k` → kurva _Power Spectrum vs Spatial Frequency_ (Fig 1, 2-kanan, 5) |
| Log-magnitude (**punya kita**) | `log(1+\|F(u,v)\|)`           | yang dipakai`fft_utils.py`; fungsi dari `\|F\|` yang sama, beda skala (log mengompres rentang dinamis)                                                                        |

### Temuan inti Durall

Up-sampling generator GAN (transposed-conv "bed of nails" → replika frekuensi tinggi; interpolasi → defisit frekuensi tinggi) **gagal mereproduksi distribusi spektral citra asli**. Kurva power spectrum citra GAN menyimpang dari real **terutama di ekor frekuensi tinggi**. Penyimpangan sistematis ini → deteksi deepfake **~100% akurasi** dengan classifier sederhana atas fitur 1D power spectrum.

### Hubungan ke penelitian ini (5 poin)

1. **Fondasi teoretis** keberadaan cabang frekuensi — sitasi untuk "distorsi distribusi spektral".
2. **Power spectrum (`\|F\|²`) vs log-magnitude kita (`log(1+\|F\|)`)** — sinyal sama, skala beda. Kita **tidak** pakai azimuthal integration.
3. **Pendekatan beda:** Durall = ringkasan **1D** (buang info arah) + classifier sederhana; kita = peta **2D penuh** + FreqCNN. Kita lebih kaya tapi lebih berisik/berdimensi tinggi.
4. **Justifikasi high-pass kita** (lihat [Item 4](#item-4)): Durall menunjukkan diskriminasi ada di **frekuensi tinggi**, low-freq (DC) hampir sama → maka kita tekan low-freq, tonjolkan high-freq.
5. **KUNCI — menjelaskan freq branch kita lemah (AUC 0,56-0,61) vs Durall ~100%:** Durall pakai **output GAN mentah tanpa kompresi**; kita pakai frame **face-crop + terkompresi c23**. Kompresi + resize = **low-pass filter yang menghancurkan sidik jari frekuensi tinggi** andalan Durall. Sudah diakui di BAB V ("hilangnya sidik jari spektral akibat face-cropping dan kompresi"). Jadi Durall = sekaligus **pembenar** mencoba frekuensi **dan kontras** yang menjelaskan hasil lemah kita.

### Kalau penguji tanya "kenudian kenapa hasilmu tidak ~100% seperti paper frekuensi?"

> "Karena kondisinya berbeda. Durall et al. menguji **output GAN mentah tanpa kompresi**, di mana sidik jari spektral up-sampling masih utuh. Penelitian kami memakai frame **wajah yang di-crop dan terkompresi (c23)** dari benchmark FaceForensics++/Celeb-DF; kompresi dan resize bertindak sebagai low-pass yang **menghapus jejak frekuensi tinggi** yang menjadi andalan deteksi spektral. Itulah mengapa cabang frekuensi kami berperforma rendah, dan ini konsisten dengan keterbatasan yang kami nyatakan di BAB V serta menjadi motivasi penelitian lanjutan (FFT pada citra penuh / multi-skala / menyertakan fasa)."

---

<a name="item-9"></a>

## Item 9 — "Local" vs "global" (SpecXNet, Alam et al. 2025) dan: _"Jadi kalian ini global atau lokal untuk spasial dan frekuensinya?"_

**Verdict: ✅ Bisa dijawab tegas. Jawaban singkat: spasial = LOKAL, frekuensi = GLOBAL. Tapi WAJIB perjelas dua hal: (a) kita TIDAK memecah local/global eksplisit seperti SpecXNet — kita pisah per-DOMAIN dengan late fusion sederhana; (b) ada dua makna "local/global" yang bisa dijebak penguji (sumbu domain vs sumbu pita-spektrum).**

### Apa arti "local" & "global" di SpecXNet (paper, §3.1 DDFC)

SpecXNet (Alam et al.) memecah feature map tiap blok jadi dua jalur via _Dual-Domain Feature Coupler (DDFC)_:

- **Local Spatial Branch** (`X_l`): **konvolusi standar** → menangkap **detail LOKAL** (tekstur halus, tepi, batas blending). "Local" karena konvolusi punya **receptive field terbatas**.
- **Global Spectral Branch** (`X_g`): **2D FFT** → domain frekuensi → menangkap **struktur GLOBAL / korelasi jarak-jauh & pola periodik**. "Global" karena **setiap koefisien Fourier bergantung pada SELURUH piksel citra**.
- Lalu difusikan dengan _Dual Fourier Attention (DFA)_ — atensi lintas-domain yang berulang di tiap blok.

Jadi di SpecXNet: **spasial ≡ lokal (konvolusi), frekuensi ≡ global (FFT)** — ini dualitas mendasar (konvolusi = lokal; transformasi Fourier = global).

### Pemetaan ke arsitektur kita (HybridTwoBranch)

|           | Cabang kita                                 | Sifat (istilah SpecXNet)                                                                          | Nuansa                                                                                                                     |
| --------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Spasial   | XceptionNet atas RGB                        | **LOKAL** — konvolusi menangkap tekstur/tepi/blending                                             | backbone dalam → effective receptive field membesar → fitur GAP akhir = deskriptor holistik wajah                          |
| Frekuensi | FFT seluruh citra → log-magnitude → FreqCNN | **GLOBAL** — FFT whole-image, menyandikan struktur periodik global, **kehilangan lokasi spasial** | tapi peta FFT itu lalu diproses**konvolusi lokal** oleh FreqCNN, dan ditekankan ke pita **frekuensi tinggi** via high-pass |

### Perbedaan penting dari SpecXNet (jangan diklaim setara)

- **SpecXNet:** pecah local/global **DI DALAM tiap blok** (channel split) + fusi **Dual Fourier Attention berulang** + inverse-FFT kembali ke spasial. Arsitektur terpadu, multi-skala.
- **Kita:** pisah per-**DOMAIN** (satu cabang spasial penuh, satu cabang frekuensi penuh), fusi **SEKALI** di level fitur via concat + **SE gating**. **Tidak ada** DDFC per-blok maupun Fourier cross-attention.
  → SpecXNet [13] kita kutip sebagai **inspirasi/related work**, bukan reimplementasi. (Senada dengan scoping di [Item 5](#item-5)/[Item 7](#item-7).)

### ⚠️ Jebakan dua-sumbu (penguji bisa pakai BAB II kalian sendiri)

Ada **dua** makna "local/global" di skripsi — jangan tertukar:

1. **Sumbu DOMAIN** (cara SpecXNet): spasial=lokal, frekuensi=global. ← ini yang dipakai untuk menjawab pertanyaan penguji.
2. **Sumbu PITA dalam spektrum** (BAB II kalian, docx line 446/454): frekuensi **rendah** = "bentuk global & pencahayaan", frekuensi **tinggi** = "tepi, tekstur, detail halus" (lokal).

Penguji bisa menjebak: _"High-pass kalian menonjolkan frekuensi tinggi, yang menurut BAB II kalian sendiri = detail LOKAL. Jadi cabang frekuensi kalian itu lokal atau global?"_

**Jawaban yang benar (tidak kontradiktif):**

> "Dua-duanya benar pada sumbu yang berbeda. **Transformasi**-nya global: FFT dihitung atas seluruh citra dan tidak menyimpan lokasi spasial artefak. **Konten** yang ditekankan adalah pita frekuensi tinggi, yang berkorelasi dengan detail halus. Jadi cabang frekuensi kami adalah **representasi global atas statistik detail berfrekuensi-tinggi** — ia mencirikan sidik jari frekuensi tinggi di seantero wajah, bukan menunjukkan DI MANA artefaknya. Tidak ada kontradiksi: 'global' merujuk pada cakupan transformasi, 'frekuensi tinggi/detail' merujuk pada pita yang ditonjolkan."

### Jawaban siap-ucap untuk "kalian global atau lokal?"

> "Cabang **spasial** kami bersifat **lokal** — XceptionNet menangkap detail lokal seperti tekstur kulit, tepi, dan batas blending lewat konvolusi; karena backbone-nya dalam, fitur akhirnya menjadi deskriptor holistik wajah. Cabang **frekuensi** kami bersifat **global** — FFT adalah transformasi seluruh citra yang menangkap struktur dan pola periodik global, meski kehilangan informasi lokasi spasial. Keduanya komplementer: yang satu tahu _bentuk artefak lokal_, yang lain tahu _tanda statistik global_. Berbeda dari SpecXNet yang memadukan local-global di tiap blok dengan atensi Fourier, arsitektur kami melakukan late fusion sederhana dua cabang domain via SE gating."

### Konsistensi dengan teks skripsi (sudah selaras)

- docx line 410: "spasial unggul menangkap anomali visual **lokal** (tekstur/tepi) ... frekuensi ... **kehilangan informasi lokasi spasial**" → mendukung pemetaan spasial=lokal, frekuensi=global. ✅
- docx line 446/454: low-freq=global, high-freq=detail → sumbu pita (jebakan #2). ✅ konsisten asalkan dijelaskan sebagai sumbu berbeda.
- Tidak perlu revisi; cukup siap membedakan dua sumbu saat ditanya.

---

<a name="item-10"></a>

## Item 10 — "Banyak penelitian menunjukkan XceptionNet unggul pada dataset FF++, DFDC, dan Celeb-DF [13, 7]" (docx line 595)

**Verdict: 🔴 OVERCLAIM + sitasi tidak mendukung. Hanya FF++ yang benar & terdukung. DFDC dan Celeb-DF TIDAK diuji oleh kedua referensi, dan klaim "unggul" pada keduanya justru BERTENTANGAN dengan literatur dan hasil kalian sendiri.**

### Referensi (per klarifikasi penulis)

- **[7] = Rössler et al., FaceForensics++ (ICCV 2019).**
- **[13] = Alam et al., SpecXNet (ACM MM 2025).**

> ⚠️ Catatan numbering: di Daftar Pustaka fisik, Rössler = entri **8** dan Alam/SpecXNet = entri **14**, tetapi dikutip in-text sebagai [7] dan [13]. In-text number **desync** dengan urutan Daftar Pustaka (isu yang sudah tercatat). Verifikasi penomoran sebelum sidang.

### Apa yang benar-benar dicakup tiap referensi

**Rössler [7] — FaceForensics++:**

- Menguji XceptionNet pada **FF++ saja** (Deepfakes, Face2Face, FaceSwap, NeuralTextures). Xception memang detektor **terbaik pada FF++** di paper itu. ✅ untuk FF++.
- **TIDAK memuat DFDC** (DFDC rilis akhir 2019/2020, setelah/di luar paper) dan **TIDAK memuat Celeb-DF** (dataset terpisah, Li et al. 2020). 🔴

**SpecXNet [13] — dari Tabel 1-5 paper (sudah dibaca):**

- Benchmark deepfake wajahnya **hanya FF++** (Tabel 3: "we adopt the FaceForensics++ (FF++) dataset, ... Deepfakes and FaceSwap"). Selebihnya GenImage + generator GAN/diffusion (ProGAN, StyleGAN, BigGAN, GLIDE, SD, DALL-E, Midjourney, dll.).
- **TIDAK ada Celeb-DF di tabel mana pun. TIDAK ada DFDC di tabel mana pun.** 🔴
- Lagipula SpecXNet melaporkan XceptionNet sebagai **backbone/baseline yang justru DIKALAHKAN** modul mereka (vanilla Xception ~81,3% rata-rata → +DDFC+DFA 96,4%, Tabel 4) — jadi paper ini **bukan** bukti "XceptionNet unggul", melainkan "SpecXNet > XceptionNet".

### Kesimpulan cakupan

| Dataset      | Didukung [7] Rössler?    | Didukung [13] SpecXNet? | Klaim "unggul" valid? |
| ------------ | ------------------------ | ----------------------- | --------------------- |
| **FF++**     | ✅ ya (Xception terbaik) | ✅ ya (diuji)           | ✅                    |
| **DFDC**     | 🔴 tidak diuji           | 🔴 tidak diuji          | 🔴 tidak terdukung    |
| **Celeb-DF** | 🔴 tidak diuji           | 🔴 tidak diuji          | 🔴 tidak terdukung    |

### Masalah SUBSTANSI (lebih dalam dari sekadar sitasi)

Klaim "XceptionNet **unggul** pada Celeb-DF dan DFDC" **bertentangan** dengan:

1. **Literatur:** XceptionNet terkenal **generalisasi buruk** ke Celeb-DF/DFDC. Paper Celeb-DF (Li et al. 2020) menunjukkan detektor termasuk Xception **anjlok mendekati tebakan acak** pada Celeb-DF.
2. **Hasil kalian sendiri:** model spasial (XceptionNet) **runtuh cross-dataset** (AUC turun, recall collapse) — justru itu MOTIVASI penelitian kalian. Mengklaim Xception "unggul" pada CDF malah **menggerus narasi** kalian sendiri.
3. **DFDC bahkan tidak dipakai** di penelitian ini (kalian pakai FF++ & Celeb-DF). Menyebutnya sebagai keunggulan itu janggal dan tak terpakai.

### Rekomendasi perbaikan (WAJIB)

Batasi klaim ke FF++ dan buang DFDC/Celeb-DF dari klaim "unggul". Contoh:

> "XceptionNet dilaporkan sebagai detektor domain spasial terbaik pada FaceForensics++ [7] dan menjadi backbone populer pada berbagai metode deteksi lanjutan termasuk pendekatan hybrid [13]. Namun, performa tinggi ini umumnya bersifat in-dataset; generalisasi ke dataset lain seperti Celeb-DF dan DFDC diketahui menurun, yang menjadi salah satu motivasi penelitian ini."

Reframe ini justru **menguatkan** motivasi kalian (masalah generalisasi), bukan melemahkannya.

### Kalau penguji bertanya

> "Kalimat itu perlu kami koreksi, Pak/Bu. Yang terdukung referensi adalah keunggulan XceptionNet pada **FaceForensics++**. Untuk Celeb-DF dan DFDC, justru sebaliknya: XceptionNet cenderung menurun secara lintas-dataset, sebagaimana juga kami temukan pada hasil model spasial kami. Referensi [7] (FaceForensics++) dan [13] (SpecXNet) tidak menguji Celeb-DF maupun DFDC, sehingga klaim tersebut akan kami persempit ke FF++."

---

<a name="item-11"></a>

## Item 11 — "Dalam penelitian ini, fitur FFT ditambahkan sebagai **kanal keempat** input XceptionNet; DSC cocok untuk multi-kanal ... sebagaimana SpecXNet [13] dan FSBI [16]" (docx §2.7.3, line ~597-602 & 630)

**Verdict: 🔴 TIDAK sejalan dengan flow kalian. Ini mendeskripsikan EARLY FUSION (input 4-kanal ke XceptionNet), padahal model yang dievaluasi adalah LATE FUSION (dua cabang terpisah). Ini instans lain dari overclaim early fusion — kembar dengan [Item 7](#item-7).**

### Jawaban langsung atas "is this lined up with our flow?": **TIDAK.**

- **Flow aktual (evaluated, `hybrid_fusion.py` HybridTwoBranch):** XceptionNet memproses RGB **3-kanal** SECARA TERPISAH; peta FFT diproses **cabang FreqCNN terpisah**; fiturnya baru digabung di **late fusion** (proyeksi → concat → SE gate → classifier). **FFT TIDAK pernah menjadi kanal ke-4 XceptionNet.**
- **Yang dideskripsikan kalimat itu:** RGB+FFT ditumpuk jadi **tensor 4-kanal** lalu masuk **satu** XceptionNet = **EarlyFusionXception** (`hybrid_fusion.py:70`). Ada di kode, **tetapi tidak dievaluasi** (lihat Item 7: `run_all.py` MODELS_CORE=[spatial,freq,hybrid], config `two_branch`).

Frasa "**Dalam penelitian ini**, fitur FFT ditambahkan sebagai kanal keempat" = **klaim faktual yang salah** untuk pipeline yang benar-benar dijalankan.

### Masalah tambahan pada paragraf ini

1. **Rasional DSC longgar untuk kasus 4-kanal.** Entry flow XceptionNet diawali **dua konvolusi BIASA** (bukan depthwise) — kalian sendiri menulisnya di §2.7.1. Jadi input 4-kanal langsung **dicampur oleh conv standar** di lapisan pertama; narasi "tiap kanal ditangani independen via depthwise" tidak berlaku untuk pencampuran awal kanal RGB vs FFT. (Deskripsi depthwise/pointwise-nya sendiri benar sebagai konsep, hanya salah tempat.)
2. **Perbandingan SpecXNet/FSBI keliru.** "sebagaimana juga dilakukan pada SpecXNet [13] dan FSBI [16]" — **keduanya TIDAK menambah FFT sebagai kanal ke-4**:
   - **SpecXNet** = DDFC (channel split → cabang spasial-lokal + cabang spektral-global via FFT di dalam blok) + Dual Fourier Attention. Bukan input 4-kanal.
   - **FSBI** = _Frequency-enhanced Self-Blended Images_ (sintesis citra latih yang ditingkatkan frekuensi). Bukan input 4-kanal.
     → "sebagaimana juga dilakukan" menyesatkan; metode mereka berbeda dari append 4-kanal.
3. **Numbering desync (lagi):** in-text FSBI [16] secara fisik = entri Daftar Pustaka **17** (Hasanaath). SpecXNet [13] = entri **14**. Cek penomoran (lihat catatan [Item 10](#item-10)).

### Rekomendasi perbaikan (WAJIB, sejalan Item 7)

Dua sub-poin di §2.7.3 — "**Integrasi dengan FFT sebagai Channel Tambahan**" dan "**Kompatibilitas dengan Analisis Frekuensi**" — mendeskripsikan early fusion. Karena model yang dievaluasi adalah late fusion, pilih salah satu:

- **(A, disarankan) Tulis ulang ke late fusion:** "XceptionNet dipilih sebagai backbone **cabang spasial** yang memproses citra RGB; efisiensi depthwise separable convolution membuatnya kuat menangkap tekstur lokal. Representasi FFT diproses **cabang frekuensi terpisah (FreqCNN)** dan digabung pada tahap **late fusion**, bukan sebagai kanal tambahan pada XceptionNet."
- **(B) Bingkai sebagai varian tak-dievaluasi:** nyatakan bahwa integrasi 4-kanal (early fusion) diimplementasikan sebagai alternatif namun **tidak menjadi model evaluasi** (konsisten dengan revisi Item 7).

Dan perbaiki klaim SpecXNet/FSBI: mereka memadukan domain lewat **modul/atensi atau sintesis input**, **bukan** penambahan kanal ke-4.

### Kalau penguji bertanya "jadi FFT itu kanal ke-4 atau cabang terpisah?"

> "Pada model yang kami evaluasi (hybrid two-branch), FFT diproses **cabang terpisah (FreqCNN)** dan digabung via late fusion + SE gating — **bukan** kanal ke-4. Varian early fusion 4-kanal memang kami implementasikan, tetapi tidak masuk evaluasi. Kalimat di BAB II yang menyebут 'kanal keempat' akan kami luruskan agar sesuai dengan arsitektur late fusion yang benar-benar digunakan."

### 📋 Perbaikan menyeluruh di Word (cakupan lengkap — hasil audit live .docx)

Framing early-fusion ("FFT jadi kanal ke-4 / channel fusion") bocor ke **7 tempat**. Model yang dievaluasi = **late fusion** (XceptionNet makan RGB 3-kanal + FreqCNN makan FFT 1-kanal, digabung di **level fitur**: proyeksi → concat → SE gating). Semua di bawah ini diedit dari Drive.

**✅ Yang sudah beres (jangan diutak-atik):**

- Konsep umum early fusion di §2.7 landasan teori (paragraf "Early Fusion (Fusi Awal)") — **biarkan**, itu teori.
- Paragraf "Penelitian ini berfokus pada strategi late fusion..." — **sudah benar** (fix Item 7). ⚠️ hanya buang **typo "ohwe"** di ujung kalimatnya.
- Tabel matriks yang menulis "RGB + FFT **(terpisah)**" — **sudah benar** (terpisah = late fusion).

**🔴 Yang masih harus diperbaiki:**

| #   | Lokasi (docx)                                                              | Teks sekarang (masalah)                                                                                                                                          | Ganti jadi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | §2.7 list "Kompatibel dengan analisis frekuensi"                           | "**Kombinasi kanal RGB dan kanal frekuensi (hasil FFT)** ... XceptionNet cocok untuk skenario hybrid ini."                                                       | "Dalam arsitektur hybrid, XceptionNet berperan sebagai**cabang spasial** yang memproses citra RGB, sedangkan representasi FFT ditangani **cabang terpisah**. Efisiensi XceptionNet membuatnya cocok sebagai backbone cabang spasial."                                                                                                                                                                                                                                                                                                                                                                   |
| 2   | §2.7.3 sub-judul + isi "**Integrasi dengan FFT sebagai Channel Tambahan**" | "Dalam penelitian ini, fitur FFT**ditambahkan sebagai kanal keempat pada input XceptionNet** ... sebagaimana SpecXNet [13] dan FSBI [16]."                       | Ganti judul → "**Peran XceptionNet sebagai Cabang Spasial dalam Arsitektur Hybrid**". Isi → "Dalam penelitian ini, XceptionNet memproses citra RGB sebagai cabang spasial, sedangkan FFT diproses **cabang frekuensi terpisah (FreqCNN)**. Fitur kedua cabang digabung pada tahap **late fusion** (proyeksi, konkatenasi, SE gating), **bukan** sebagai kanal tambahan. SpecXNet [13] dan FSBI [16] juga memadukan spasial-frekuensi, **melalui mekanisme berbeda** (SpecXNet: pemisahan kanal spasial-spektral + atensi Fourier di dalam blok; FSBI: citra self-blended yang ditingkatkan frekuensi)." |
| 3   | §2.7.3 sub-judul "**Kompatibilitas dengan Analisis Frekuensi**"            | "Struktur DSC ... memproses**input multi-kanal yang mencakup kanal RGB dan kanal frekuensi (FFT)** ... [13]."                                                    | **Hapus** sub-poin ini (sudah ditutup #2), **atau** ganti → "Efisiensi depthwise separable convolution membuat XceptionNet cukup ringan untuk dijadikan **salah satu cabang** arsitektur hybrid dua-cabang, sehingga penambahan cabang frekuensi terpisah tetap layak secara komputasi."                                                                                                                                                                                                                                                                                                                |
| 4   | §2.9 Peran FaceForensics++                                                 | "Kedua fitur ini kemudian digabungkan sebagai**channel fusion** ..."                                                                                             | "Fitur spasial dan frekuensi ini kemudian digabungkan pada tahap**late fusion di tingkat fitur** ..."                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 5   | **Tabel 2.4 Tahapan Preprocessing** — baris 7 + caption                    | Baris 7: "**Channel fusion** \| Menggabungkan RGB dan kanal frekuensi \| **Tensor 4-channel**". Caption: "tahapan 6-7 ... **fitur tambahan** pada model hybrid". | **Hapus baris 7** (fusi bukan langkah preprocessing, dan bukan 4-kanal). Caption → "Tahapan 1–5 menghasilkan citra RGB (preprocessing spasial); tahapan 6 menghasilkan peta FFT log-magnitude **1 kanal**. Kedua representasi **disimpan terpisah** dan digabungkan **di dalam model** pada tahap late fusion, bukan pada preprocessing."                                                                                                                                                                                                                                                               |
| 6   | **BAB III §Preprocessing FFT** (metodologi!)                               | "Representasi frekuensi kemudian digabungkan sebagai**frequency channel tambahan bersama citra RGB**."                                                           | "Representasi frekuensi**1-kanal** ini disimpan sebagai cache dan menjadi masukan **cabang frekuensi (FreqCNN)**, terpisah dari citra RGB yang menjadi masukan **cabang spasial (XceptionNet)**. Fitur kedua cabang digabung pada tahap **late fusion**."                                                                                                                                                                                                                                                                                                                                               |
| 7   | **BAB III §Pelatihan** (freezing)                                          | "...model spatial, hybrid,**dan early fusion**, backbone dibekukan ... pada model **early fusion**, seluruh parameter backbone dibekukan."                       | Buang klausa early fusion → "...model spatial**dan** hybrid, backbone dibekukan ... pada model hybrid: FreqCNN, proyeksi, SE gate, dan classifier."                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 8   | **BAB III §Preprocessing FFT** (line 793, dekat sitasi Sabir/Wang)         | "...penelitian ini menambahkan informasi Frekuensi ke dalam informasi citra sebagai**channel 4** yang akan membawa informasi mengenai penyebaran frekuensi."     | "...penelitian ini memproses informasi frekuensi pada**cabang terpisah (FreqCNN)** dan menggabungkannya dengan fitur spasial pada tahap **late fusion**, bukan sebagai kanal ke-4."                                                                                                                                                                                                                                                                                                                                                                                                                     |

**Opsional (rendah):** §2.10-related-work "SpecXNet, FSBI ... memasukkan **kanal-kanal frekuensi tambahan** atau modul khusus" — masih agak menyiratkan channel-append; boleh dipertegas jadi "melalui **modul khusus atau sintesis input** yang menonjolkan komponen frekuensi" agar tidak rancu dengan #2.

**Prinsip global untuk konsistensi:** di mana pun kata **"channel fusion" / "kanal keempat" / "4-channel" / "kanal frekuensi tambahan"** muncul sebagai deskripsi metode penelitian → ganti ke **"late fusion di tingkat fitur"** dengan dua cabang terpisah. Sisakan istilah 4-kanal HANYA di (a) paragraf konsep early fusion, dan (b) catatan "alternatif tak-dievaluasi".

---

<a name="item-12"></a>

## Item 12 — "korelasi spasial **(cross-channel)** dan korelasi antarkanal **(cross-spatial)**" (docx line 604)

**Verdict: 🔴 KELIRU — label Inggris di dalam kurung TERTUKAR, dan "cross-spatial" bukan istilah baku. Instingmu benar. Perbaikannya satu kalimat.**

### Yang benar (hipotesis Chollet, Xception 2017)

Chollet: _"cross-channel correlations and spatial correlations are sufficiently decoupled..."_. Depthwise separable convolution memisahkan dua jenis korelasi:

| Istilah Indonesia      | Label Inggris yang BENAR       | Ditangani oleh                                |
| ---------------------- | ------------------------------ | --------------------------------------------- |
| korelasi**spasial**    | **spatial correlations**       | **depthwise** conv (per-kanal, di bidang H×W) |
| korelasi**antarkanal** | **cross-channel correlations** | **pointwise** 1×1 conv (campur antar-kanal)   |

### Apa yang salah di kalimatmu (line 604)

- "korelasi spasial **(cross-channel)**" → salah. _cross-channel_ = label untuk **antarkanal**, bukan spasial.
- "korelasi antarkanal **(cross-spatial)**" → salah ganda: (a) mestinya **cross-channel**, (b) **"cross-spatial" tidak ada** dalam terminologi Chollet.

Jadi kedua label Inggris **saling tertukar**, plus satu istilah dikarang.

### Bukti bahwa ini memang typo (skripsimu contradict dirinya sendiri)

- **docx line 572** (BENAR): "_pointwise convolution_ ... menangkap **korelasi antarkanal**" → pointwise = cross-channel = antarkanal. ✅
- **docx line 562** (BENAR): "korelasi spasial dan korelasi kanal dapat dipisahkan" (tanpa label Inggris, urutan benar). ✅
- **docx line 604** (SALAH): satu-satunya tempat yang menempel label Inggris, dan tertukar. → jelas kesalahan penulisan lokal, bukan kesalahan pemahaman menyeluruh.

### Perbaikan (WAJIB, mudah)

> "Arsitektur ini dibangun berdasarkan hipotesis bahwa **korelasi spasial (spatial correlations)** dan **korelasi antarkanal (cross-channel correlations)** dapat dipisahkan (_decoupled_) secara penuh melalui _depthwise separable convolution_, sehingga operasi konvolusi menjadi lebih efisien tanpa mengorbankan kapasitas representasi fitur [6]."

(Atau cukup hapus kedua label Inggris — line 562 sudah membuktikan kalimat tanpa label pun jelas dan benar.)

### Kalau penguji menyorot

> "Betul, itu salah ketik pada label bahasa Inggris — tertukar. Yang benar: korelasi spasial = _spatial correlations_ (ditangani depthwise), korelasi antarkanal = _cross-channel correlations_ (ditangani pointwise 1×1). Ini juga sudah kami nyatakan dengan benar di bagian penjelasan pointwise convolution."

---

<a name="item-13"></a>

## Item 13 — Repetisi: pembuka seksi "DSC" dan pembuka §2.7 "XceptionNet" mengulang hal yang sama

**Verdict: 🟡 REPETITIF (editorial, bukan kesalahan fakta). Dua pembuka seksi menyampaikan proposisi identik. Instingmu benar. + ada redundansi kedua: dua daftar keunggulan tumpang-tindih.**

### Dua paragraf yang diulang

Keduanya menyatakan hal sama: (1) XceptionNet = CNN oleh Chollet (2017), pengembangan Inception Module; (2) hipotesis korelasi spasial & antarkanal dapat dipisahkan via DSC; (3) hasilnya konvolusi lebih efisien tanpa mengorbankan representasi.

- **Paragraf B** = pembuka sub-bab **"Depthwise Separable Convolution (DSC)"** (muncul lebih dulu): "Arsitektur XceptionNet merupakan salah satu model CNN modern ... memanfaatkan DSC. Pendekatan ini diperkenalkan oleh Chollet [6] ... korelasi spasial dan korelasi kanal dapat dipisahkan ..."
- **Paragraf A** = pembuka **§2.7 "Extreme Inception Network (XceptionNet)"**: "XceptionNet merupakan arsitektur CNN yang diperkenalkan oleh Chollet pada 2017 ... korelasi spasial dan korelasi antar-kanal (cross-channel) dapat dipisahkan secara penuh melalui DSC ..."

**Akar masalah:** seksi DSC ikut _memperkenalkan XceptionNet_, padahal seharusnya membahas **teknik DSC**; §2.7 yang memperkenalkan **arsitekturnya**.

### Perbaikan

Pertahankan **Paragraf A (§2.7)** sebagai pengantar kanonik XceptionNet. **Tulis ulang Paragraf B** → soal DSC-sebagai-teknik + forward-ref §2.7:

> "Depthwise Separable Convolution (DSC) merupakan teknik konvolusi yang memisahkan operasi spasial dan operasi antarkanal menjadi dua tahap terpisah (_depthwise_ dan _pointwise_). Pemisahan ini menekan jumlah parameter dan biaya komputasi secara signifikan tanpa mengurangi kapasitas representasi fitur, dan menjadi inti efisiensi arsitektur XceptionNet yang dibahas pada sub-bab 2.7."

### Redundansi KEDUA (di seksi yang sama) — dua daftar keunggulan tumpang-tindih

- **"Relevansi DSC pada Deteksi Deepfake"** (seksi DSC): sensitif tekstur lokal · stabil pada variasi kompresi · kompatibel analisis frekuensi · performa tinggi FFPP · representasi spasial kuat.
- **"Keunggulan XceptionNet dalam Deteksi Deepfake"** (§2.7.3): sensitivitas tekstur lokal · efisiensi parameter · performa tertinggi FFPP · stabilitas variasi kompresi · kompatibilitas analisis frekuensi · standar penelitian.

**4 poin identik** muncul di kedua daftar (tekstur lokal, FFPP, kompresi, frekuensi). **Rekomendasi:** gabung jadi **satu daftar** di §2.7.3; seksi DSC cukup fokus ke mekanisme + kompleksitas DSC (tanpa daftar keunggulan). Ini sekaligus menutup poin early-fusion di [Item 11](#item-11) (#1, #2, #3) yang kebetulan berada di kedua daftar tersebut.

---

<a name="item-14"></a>

## Item 14 — "SE block ... yang tidak dapat ditangkap oleh konkatenasi sederhana ... Dibandingkan fusi sederhana seperti konkatenasi atau penjumlahan, SE block ... meningkatkan performa" (§2.8.3, docx line 649-650) — padahal kita PAKAI konkatenasi

**Verdict: ✅ BUKAN masalah, TIDAK kontradiksi. Konkatenasi dan SE gating dipakai BERSAMAAN (bukan alternatif). Konkatenasi menggabungkan dua cabang; SE gating membobotinya secara adaptif SETELAHNYA. Thesis kalian sudah konsisten.**

### Kenapa bukan kontradiksi

Kesalahpahaman: membaca "konkatenasi" sebagai lawan dari "SE block". Padahal di model kita, urutannya:

```
proyeksi(256) → KONKATENASI (512) → SE GATE (bobot adaptif) → classifier
```

(kode `hybrid_fusion.py:64-66`). Jadi:

- **Konkatenasi** = operasi yang MENYATUKAN fitur spasial (256) + frekuensi (256) jadi satu vektor 512-d. **Wajib** — kedua cabang harus digabung dulu.
- **SE gating** = bekerja **di atas** hasil konkatenasi, mempelajari bobot kepentingan per-dimensi lalu menskala ulang (`x * gate(x)`).

"**Konkatenasi sederhana**" (kata "sederhana" penting) = konkatenasi **tanpa** pembobotan adaptif, yaitu vektor gabungan langsung masuk classifier. Model kita **tidak** begitu — kita konkatenasi **lalu** SE gating. Jadi kita ada di sisi "lebih baik" dari perbandingan itu. **Paragraf itu justru membenarkan desain kita**, bukan menyerangnya.

Analogi: "tembok polos itu lemah, jadi kami perkuat dengan baja." Temboknya tetap ada — hanya ditambah penguat. Bukan tembok-vs-baja, tapi tembok+baja. Konkatenasi = tembok, SE = baja.

### Thesis kalian sudah konsisten (tidak perlu revisi)

- §2.8.3 line 645: "...digabungkan melalui **konkatenasi**, vektor fusi..." lalu SE memprosesnya. ✅
- §2.8.3 line 652: "...digabungkan (konkatenasi) ... **sebelum diproses** oleh channel attention seperti SE gating." ✅
- BAB III line 1349-1351: "Setelah **konkatenasi**, diterapkan **SE gating**..." ✅
- Tabel arsitektur menulis fusi hybrid = "**Konkatenasi + SE Gating**". ✅

### Satu nuansa jujur (kalau penguji menekan teknis)

SE gating itu **channel attention** (squeeze-excite): membobot ulang tiap dimensi secara global, di mana bobot dihitung dari **seluruh vektor 512-d** (kedua domain). Jadi pembobotan dimensi spasial **dikondisikan** oleh nilai fitur frekuensi dan sebaliknya — itulah "interaksi lintas domain"-nya. Tapi SE **bukan** modul korelasi berpasangan penuh (bukan cross-attention/bilinear). Jadi frasa "mempelajari korelasi antara fitur spasial dan frekuensi" sebaiknya dipahami sebagai "**pembobotan kanal adaptif yang dikondisikan kedua domain**", bukan pemodelan korelasi eksplisit. Aman diucapkan, jangan overclaim jadi "SE memodelkan korelasi penuh".

### Opsional (kejelasan)

Kalau mau mencegah penguji salah baca seperti tadi, tambahkan satu klausa di §2.8.3:

> "Perlu ditegaskan bahwa SE block **tidak menggantikan** konkatenasi, melainkan bekerja **di atasnya**: konkatenasi menyatukan kedua cabang menjadi satu vektor, lalu SE gating membobotinya secara adaptif. Istilah 'konkatenasi sederhana' merujuk pada konkatenasi tanpa pembobotan adaptif."

### Jawaban siap-ucap

> "Tidak bertentangan, Pak/Bu. Kami memang memakai konkatenasi — sebagai langkah **menyatukan** fitur kedua cabang — tetapi tidak berhenti di situ; hasil konkatenasi lalu dibobot secara adaptif oleh **SE gating**. Jadi fusi kami adalah **konkatenasi + SE gating**. Yang dibandingkan pada paragraf itu adalah konkatenasi **tanpa** gating (konkatenasi sederhana) versus konkatenasi **dengan** SE gating, dan arsitektur kami menggunakan yang kedua."

---

<a name="item-15"></a>

## Item 15 — Tingkat kompresi FFPP: HQ/LQ tidak diberi label c23/c40 (§2.9, docx line 663-666)

**Verdict: 🟡 BENAR — instingmu tepat. Standar FaceForensics++: RAW = c0, HQ = c23, LQ = c40. Paragrafmu benar arah tapi VAGUE (tak menyebut c23/c40) dan tidak konsisten dengan bagian lain dokumen yang sudah pakai c23/c40.**

### Peta baku FaceForensics++ (Rössler et al.)

| Level             | Label   | Kompresi                  | Keterangan                                       |
| ----------------- | ------- | ------------------------- | ------------------------------------------------ |
| RAW               | **c0**  | lossless / tanpa kompresi | tekstur paling utuh                              |
| HQ (high quality) | **c23** | H.264,**CRF 23**          | kualitas tinggi, kompresi ringan                 |
| LQ (low quality)  | **c40** | H.264,**CRF 40**          | kualitas rendah, kompresi berat (≈ media sosial) |

c23/c40 = nilai _Constant Rate Factor_ (CRF) H.264; CRF lebih tinggi → kompresi lebih berat. Jadi **HQ = c23, LQ = c40** — persis dugaanmu.

### Masalah pada paragraf (line 663-666)

- RAW (lossless) ✅ benar.
- HQ = "kompresi ringan (misalnya CRF rendah)" → arah benar (CRF 23 < 40), tapi **harus sebut c23 (CRF 23)** eksplisit.
- LQ = "kompresi berat" → benar, tapi **harus sebut c40 (CRF 40)**.

### Inkonsistensi internal (dokumenmu sendiri sudah pakai label itu)

- **line 318 & 330 (BAB III):** "kompresi **high-quality (c23)**", "FaceForensics++ (n=750, **c23**)" → **penelitian ini memakai c23 = HQ**.
- **line 625 (§2.7.3):** "akurasi turun ke 81,00% pada kompresi berat (**c40**)".

Jadi c23/c40 muncul di tempat lain, tetapi seksi dataset (§2.9) tidak menautkan HQ↔c23 dan LQ↔c40. Pembaca bisa mengira HQ dan c23 hal berbeda.

### Perbaikan

Ganti tiga butir jadi:

> 1. **RAW (c0, lossless):** tanpa kompresi, tekstur paling utuh.
> 2. **HQ (c23):** kompresi H.264 dengan CRF 23 (kualitas tinggi, kompresi ringan).
> 3. **LQ (c40):** kompresi H.264 dengan CRF 40 (kualitas rendah, kompresi berat, meniru unggahan media sosial).

Dan tambahkan satu kalimat penutup: "**Penelitian ini menggunakan versi HQ (c23)**, sesuai standar benchmark FaceForensics++." (Ini juga menyiapkan jawaban kalau penguji tanya "kalian pakai kompresi yang mana?" → c23, dan varied-compression = future work.)

### ⚠️ Bonus (temuan baru untuk [Item 11](#item-11)): "channel 4" lagi di BAB III

docx **line 793** (paragraf preprocessing FFT, dekat sitasi Sabir/Wang): _"...penelitian ini menambahkan informasi Frekuensi ke dalam informasi citra sebagai **channel 4** yang akan membawa informasi mengenai penyebaran frekuensi."_ → Ini **instans early-fusion ke-8** (di luar 7 yang sudah dicatat di Item 11). Sudah ditambahkan ke tabel perbaikan Item 11.

---

<a name="item-16"></a>

## Item 16 — Daftar "Artefak Spasial" (§2.9, docx line 670-675): butir (d) sebenarnya artefak TEMPORAL

**Verdict: 🔴 Butir (d) salah kategori DAN bentrok dengan pendekatan frame-level. + prosa bisa dirapikan. Instingmu ("gak enak") menangkap masalah nyata.**

### Masalah substansi (lebih penting dari gaya)

Daftar di bawah judul "**Artefak Spasial**" (artefak yang muncul pada **satu frame**):

- (a) Ketidaksesuaian warna kulit — spasial ✅
- (b) Tepi wajah tidak rapi akibat _blending_ — spasial ✅
- (c) Distorsi geometri mata/mulut — spasial ✅
- (d) **"Ketidakkonsistenan ekspresi saat frame berubah cepat"** — **TEMPORAL ❌** (antar-frame, bukan dalam satu frame)
- (e) _Blurring_ lokal — spasial ✅

Dua masalah pada (d):

1. **Salah kategori:** "ekspresi berubah saat frame berubah cepat" adalah anomali **antar-frame** (temporal), bukan artefak spasial satu-frame.
2. **Bentrok dengan metode kalian:** docx line 724 menegaskan penelitian ini **frame-level**, "diproses secara terpisah ... **tanpa memerlukan informasi sekuensial antar-frame**". Model kalian **tidak bisa** menangkap inkonsistensi temporal. Jadi mencantumkannya sebagai artefak yang relevan itu kontradiktif. (Aspek temporal memang ada di §2.x "Distorsi Spektral Temporal", tetapi itu **bukan** yang diimplementasikan.)

### Perbaikan (pilih satu)

- **(A, disarankan) Ganti (d)** dengan artefak spasial asli, ambil dari versi yang sudah benar di docx line 367: "**Inkonsistensi pencahayaan dan bayangan akibat _face warping_**." (tetap 5 butir, semuanya spasial).
- **(B)** Hapus (d) (jadi 4 butir).

### Sekalian rapikan prosa

- "Hal ini membuat **dataset ini**..." → dobel "ini" + "sangat berguna" agak hiperbolik. Ganti: "Keberagaman artefak ini menjadikan FaceForensics++ **relevan** untuk penelitian _hybrid_ XceptionNet–FFT."
- Judul butir "Artefak Spasial, artefak utama yang sering muncul meliputi:" → "**Artefak spasial**, yaitu anomali yang muncul pada **setiap frame**, di antaranya:".
- Konsisten: istilah asing dimiringkan (_blending_, _frame_, _blurring_, _face warping_, _patch_).

**Versi rapi (butir d diganti):**

> Setiap teknik manipulasi pada FaceForensics++ menghasilkan pola artefak yang berbeda, baik pada domain spasial maupun frekuensi. Keberagaman ini menjadikan _dataset_ tersebut relevan untuk penelitian _hybrid_ seperti XceptionNet–FFT.
>
> 1. **Artefak spasial**, yaitu anomali yang muncul pada setiap _frame_, di antaranya:
>    a. ketidaksesuaian warna kulit antara wajah sintetis dan latar;
>    b. tepi wajah tidak rapi akibat _blending_ yang buruk;
>    c. distorsi geometri pada area mata dan mulut;
>    d. inkonsistensi pencahayaan dan bayangan akibat _face warping_;
>    e. _blurring_ lokal pada area rekonstruksi.
>
> Penelitian sebelumnya menunjukkan artefak ini paling jelas pada area transisi wajah, sehingga deteksi difokuskan pada _patch_ wajah, bukan keseluruhan citra [4, 7]. (Butir penutup ini juga menjustifikasi _face cropping_ yang dipakai penelitian ini.)

_(Catatan: bila memilih titik-koma di daftar terasa banyak, ganti ke titik seperti format aslimu — sesuaikan dengan gaya no-`;`.)_

---

<a name="item-17"></a>

## Item 17 — Struktur membingungkan: dikotomi "artefak spasial/frekuensi" diulang 3× dengan 3 format berbeda

**Verdict: 🟡 Redundansi struktural. Bukan salah fakta, tapi bikin bingung (persis yang kamu rasakan). Dikotomi spasial/frekuensi muncul di 3 tempat dengan format berlainan, dan versi FFPP mengulang isi konseptual.**

### Kenapa terasa membingungkan — 3 kemunculan

| #   | Lokasi                                                                | Format                                                                        | Isi                                                          |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------ |
| A   | §"Artefak yang Dihasilkan Proses Generatif" (docx ~366-370)           | **sub-judul + prosa**: "Artefak Domain Spasial", "Artefak Domain Frekuensi"   | taksonomi UMUM artefak GAN (benar, bersih)                   |
| B   | §"Perbandingan Domain Spasial dengan Frekuensi" (Tabel 2.1)           | **tabel**                                                                     | perbandingan aspek (jenis info, artefak, generalisasi, dll.) |
| C   | §2.9 FFPP "Karakteristik Artefak pada FaceForensics++" (docx 667-687) | **daftar bernomor**: "1. Artefak Spasial (a-e)", "2. Artefak Frekuensi (...)" | **mengulang** taksonomi A, dibungkus "dalam FFPP"            |

Jadi pembaca ketemu "spasial vs frekuensi" tiga kali: sebagai **sub-bab prosa** (A), lalu **tabel** (B), lalu **daftar bernomor bersarang** (C). Peralihan format inilah yang terasa "tiba-tiba poin", dan C sebagian besar **mengulang** A.

### Rekomendasi — beri tiap tempat peran berbeda, jangan mengulang

- **A** = rumah taksonomi UMUM artefak spasial/frekuensi. **Pertahankan.**
- **B** = tabel perbandingan. **Pertahankan** (fungsinya beda).
- **C (FFPP)** = seharusnya **khusus FaceForensics++**, bukan mengulang taksonomi umum. Yang benar-benar khas FFPP adalah **artefak per-teknik** (Deepfakes/Face2Face/FaceSwap/NeuralTextures) — itu yang menarik dan tidak ada di A/B. Buang daftar generik "1. Artefak Spasial (a-e) / 2. Artefak Frekuensi", rujuk balik ke A, dan sisakan pemetaan per-teknik.

### Usulan penulisan ulang untuk §C ("Karakteristik Artefak pada FaceForensics++")

> Karena mencakup empat teknik manipulasi, FaceForensics++ menghadirkan artefak spasial maupun frekuensi sebagaimana dibahas pada sub-bab Artefak yang Dihasilkan Proses Generatif. Yang khas pada dataset ini adalah pola artefak yang berbeda-beda menurut tekniknya:
>
> - **Deepfakes** menyisakan batas _blending_ dan ketidaksesuaian warna pada wajah hasil _face-swap_.
> - **Face2Face** meninggalkan _warping_ berfrekuensi rendah dari _reenactment_ ekspresi.
> - **NeuralTextures** memunculkan tekstur berfrekuensi tinggi yang berulang dari _neural rendering_.
> - **FaceSwap** menunjukkan _spectral drop-off_ yang tidak konsisten pada tepi wajah.
>
> Keberagaman artefak lintas-teknik ini menjadikan FaceForensics++ ideal untuk model _hybrid_ yang memadukan domain spasial dan frekuensi, sebagaimana dilakukan pada penelitian ini.

### Efek samping positif

- Penulisan ulang §C ini **otomatis menyelesaikan [Item 16](#item-16)** (daftar generik "1. Artefak Spasial (a-e)" — termasuk butir temporal (d) — dibuang).
- **Simpan** kalimat justifikasi _face crop_ ("...artefak paling jelas pada area transisi wajah, deteksi fokus pada _patch_ wajah [4,7]") — pindahkan ke sub-bab _preprocessing/face cropping_ agar tidak hilang, karena itu argumen berharga.

### Tentang "bersarang poin di dalam poin"

Di §FFPP, sub-bagian berturut-turut semuanya daftar (4 teknik → 3 tingkat kompresi → 1./2. artefak → 5 alasan pemilihan). Kepadatan daftar beruntun ini menambah kesan berat. Setelah §C diringkas jadi pemetaan per-teknik di atas, bebannya berkurang. Untuk "Alasan Pemilihan FaceForensics++" (5 poin) boleh tetap daftar — itu wajar.

---

<a name="item-18"></a>

## Item 18 — "Alasan Pemilihan FaceForensics++" (§2.9, docx ~682-695): klaim faktual tanpa sitasi

**Verdict: 🟡 BENAR — instingmu tepat. Tiga klaim faktual berdiri tanpa sitasi. Plus satu klaim ("GAN dan non-GAN") kurang tepat secara teknis.**

### Klaim yang butuh sitasi

| Klaim (docx)                                                                                               | Masalah                                                                           | Sitasi yang tepat                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "FFPP mencakup metode manipulasi**GAN dan non-GAN**..." (Alasan 1)                                         | faktual soal komposisi FFPP,**tanpa sitasi** + istilah kurang tepat (lihat bawah) | **Rössler et al. [7]** (paper FF++)                                                                                                                                                                                                                                          |
| "...agar model memiliki**kemampuan generalisasi yang baik**" (Alasan 1)                                    | klaim argumentatif keragaman-teknik → generalisasi, tanpa dukungan                | tinjauan generalisasi (Rana et al. / Rao & Uehara) —**dan scope-kan**: keragaman metode membantu antar-_method_ di FFPP, tetapi generalisasi lintas-_dataset_ tetap tantangan (temuan kalian sendiri, [Item 10](#item-10))                                                   |
| "Penelitian deteksi deepfake**sering gagal pada video berkualitas rendah**" (Alasan 2)                     | faktual, tanpa sitasi                                                             | **Rössler et al. [7]** (Xception turun ~99%→81% pada c40 — sudah kalian kutip di docx line 625 sebagai [3,7]); dapat diperkuat Tan et al. [12] / FSBI [16] soal ketahanan frekuensi pada citra terkompresi                                                                   |
| "FFPP ... digunakan oleh**lebih dari ratusan publikasi sejak 2019**" (Alasan 4, "Benchmark Internasional") | klaim kuantitatif spesifik ("ratusan"), tanpa sitasi                              | **Rössler et al. [7]** (untuk "sejak 2019" + status benchmark) + **tinjauan sistematis** (Rana et al. / Rao & Uehara) yang mendokumentasikan pemakaian luas. Kalau angka "ratusan" sulit disumberkan, **perlunak** jadi "salah satu benchmark yang paling banyak digunakan". |

### ⚠️ Bonus akurasi: "GAN dan non-GAN" kurang tepat

Empat metode FFPP bukan pas dikotomi GAN/non-GAN:

- **Face2Face** & **FaceSwap** = berbasis **grafika komputer** (reenactment / 3D + _blending_), non-GAN.
- **Deepfakes** = berbasis **autoencoder** (encoder-decoder), bukan GAN murni.
- **NeuralTextures** = _neural rendering_ dengan komponen **adversarial** — ini yang paling dekat "GAN".

Jadi hanya NeuralTextures yang benar-benar adversarial; Deepfakes autoencoder; dua lainnya grafika. **Frasa lebih tepat:** "mencakup metode berbasis **grafika komputer** (_Face2Face_, _FaceSwap_) dan berbasis **pembelajaran** (_Deepfakes_, _NeuralTextures_)" — ini justru dikotomi yang dipakai paper FF++ [7], dan tetap mendukung poin "beragam teknik".

### Ringkas untuk dieksekusi

Tambahkan **[7]** di akhir kalimat Alasan 1 dan Alasan 2 (dan awal Alasan 4), tambah tinjauan (Rana/Rao) untuk klaim "ratusan publikasi" & "generalisasi", ganti "GAN dan non-GAN" → "grafika komputer dan pembelajaran". Perhatikan **desync penomoran** in-text vs Daftar Pustaka (lihat catatan [Item 10](#item-10)) saat menaruh nomor.
