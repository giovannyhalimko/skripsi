# Simulasi Sidang Skripsi — Rekam Evaluasi Penguji (Sesi 2026-07-27)

**Mahasiswa yang diuji:** Samuel Onasis (221110680)
**Kontribusi:** Penyusunan dokumen BAB I–V, evaluasi kinerja model, pengujian purwarupa
**Judul:** Studi Komparatif Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal
**Penguji (simulasi):** Dosen Penguji Senior — Teknik Informatika

> Aturan sesi: satu pertanyaan, satu jawaban. Setiap butir direkam dengan evaluasi
> (Ketepatan / Kedalaman / Kekurangan / Skor 1–10).
> Sesi sebelumnya (rata-rata 6,3/10) terekam di `SIMULASI_SIDANG_Penguji_Evaluasi_2026-07-13.md`.

---
## Pertanyaan #1 — Kenapa XceptionNet (bukan ResNet/VGG/EfficientNet)?

**Jawaban ringkas mahasiswa:** Menurut Rossler, XceptionNet baseline unggul untuk deteksi deepfake.

**Evaluasi**
- **Ketepatan:** Benar tapi minimal. Rossler (FF++) memang menetapkan Xception sbg baseline kuat.
  Namun jawaban murni *appeal to authority*, tanpa alasan arsitektural.
- **Kedalaman:** Dangkal. Belum menyebut: depthwise separable convolution (memfaktorkan korelasi
  spasial vs kanal → efisien & menangkap fitur lokal halus); artefak deepfake = inkonsistensi tekstur
  lokal halus (blending/warping) yg cocok ditangkap Xception; pretrained ImageNet (transfer learning).
- **Kekurangan:** Tidak menjelaskan KENAPA secara arsitektur ia mengungguli CNN lain.
- **Skor:** 5/10

### Pertanyaan #1a (follow-up) — Operasi khas Xception & kenapa cocok utk artefak deepfake

**Jawaban ringkas mahasiswa:** Depthwise Separable Convolution, berbasis Inception, memakai korelasi
cross-channel & spasial, "fokusnya ke masing-masing image".

**Evaluasi**
- **Ketepatan:** Nama operasi BENAR (depthwise separable conv) & kosakata benar (pisah korelasi
  cross-channel vs spasial). Tapi mekanisme kabur: depthwise = filter spasial per-KANAL (bukan "per
  image"); pointwise 1x1 = gabung antar-kanal. Xception = "extreme Inception" (spasial & kanal dipetakan
  terpisah penuh).
- **Kedalaman:** Sedang. Belum menghubungkan ke deepfake: efisiensi parameter (kurang overfit) +
  penangkapan pola lokal halus per-kanal cocok utk artefak blending/warping yg subtil & lokal.
- **Kekurangan:** "fokus ke masing-masing image" keliru (harusnya per-kanal); link ke artefak lemah.
- **Skor:** 6/10

## Pertanyaan #2 — Isi & beda mendasar FF++ vs Celeb-DF; kenapa lintas-dataset bermakna

**Jawaban ringkas mahasiswa:** FF++ = 4 metode (FaceSwap, Face2Face, DeepFakes, NeuralTextures);
Celeb-DF = 1 metode (face-swap). Dua dataset beda → komparasi lintas bermakna; kalau dua-duanya FF++
tak bermakna krn metode & model generatif dari dataset sama. FF++ sering dipakai (Alam); Celeb-DF
kualitas lebih tinggi & lebih sulit (Li: XceptionNet turun).

**Evaluasi**
- **Ketepatan:** KUAT & terverifikasi. 4 metode FF++ disebut lengkap (perbaikan besar dari sesi lalu).
  Celeb-DF = face-swap kualitas tinggi (Li menunjukkan AUC detektor turun). Rasional cross-dataset benar
  (uji generalisasi ke manipulasi tak dikenal; sama-dataset tak menguji generalisasi).
- **Kedalaman:** Baik. Sitasi Alam & Li relevan.
- **Kekurangan:** Minor — belum sebut skala (Celeb-DF v2 ~590 real/5639 fake) & bahwa cross-dataset
  menguji apakah model belajar isyarat forgery yg generalizable vs artefak spesifik-dataset.
- **Skor:** 8/10

### Pertanyaan #2a (follow-up) — Arah lintas-dataset mana lebih sulit & kenapa?

**Jawaban ringkas mahasiswa:** CDF→FFPP lebih sulit; CDF hanya 1 metode → recall turun drastis; kualitas
FFPP lebih rendah → deteksi sedikit kurang akurat.

**Evaluasi**
- **Ketepatan:** Inti BENAR & cocok dgn temuan (recall collapse ≈0,07 CDF→FFPP). Latih di dataset
  SEMPIT (1 metode) → aturan sempit → gagal pd FFPP 4 metode. Latih di FF++ DIVERS → generalisasi lebih
  baik ke CDF. Poin "kualitas FFPP rendah" agak kabur (domain shift kompresi ada, tapi bukan faktor
  dominan).
- **Kedalaman:** Baik — mengaitkan komposisi (asimetri diversitas) ke hasil empiris.
- **Kekurangan:** Belum eksplisit "latih-divers > latih-sempit"; poin kualitas kurang tajam.
- **Skor:** 7/10

## Pertanyaan #3 — Kenapa AUC metrik utama, bukan akurasi?

**Jawaban ringkas mahasiswa:** AUC lebih baik krn threshold-independent. Juga AUC "bergantung ke semua
statistik (Accuracy, Precision, Recall, F1)". Kalau hanya akurasi, cuma dapat akurasi deteksi palsu/asli.

**Evaluasi**
- **Ketepatan:** Poin UTAMA benar (threshold-independent). TAPI klaim "AUC bergantung ke akurasi/
  presisi/recall/F1" = MISKONSEPSI. AUC = luas di bawah kurva ROC (TPR vs FPR lintas threshold);
  terkait recall & FPR, BUKAN agregat akurasi/presisi/F1. AUC = P(positif acak di-rank > negatif acak).
- **Kedalaman:** Lewat alasan terkuat & paling relevan: KETIDAKSEIMBANGAN KELAS. Data mereka timpang
  (Celeb-DF ~590 real vs 5639 fake). Akurasi @threshold tetap menyesatkan saat imbalance (tebak kelas
  mayoritas bisa "akurat" tapi gagal minoritas / recall runtuh). AUC tahan imbalance & ukur kemampuan
  MEMERINGKAT.
- **Kekurangan:** Miskonsepsi "AUC = gabungan semua metrik"; tak sebut imbalance.
- **Skor:** 6/10

### Pertanyaan #3a (follow-up) — Model malas 90% fake; akurasi vs AUC

**Jawaban ringkas mahasiswa:** Sampel penelitian kami sudah diseimbangkan. Untuk kasus: akurasi 90%
(model tebak 90% sbg palsu). AUC dipakai krn "menghitung memakai hasil statistik lain" → model tak bisa
membohongi.

**Evaluasi**
- **Ketepatan:** Angka 90% BENAR. Tapi (a) belum jelaskan KENAPA menyesatkan: model degeneratif, deteksi
  video ASLI = 0 (recall_real=0), tak belajar apa pun; (b) MENGULANG miskonsepsi yg baru dikoreksi —
  AUC bukan "gabungan statistik lain". Alasan benar AUC menangkap model malas: prediktor konstan tak
  bisa MEMERINGKAT → kurva ROC = diagonal → AUC = 0,5 (setara acak).
- **Kedalaman:** Kurang; dua bagian "kenapa" lemah/salah.
- **Kekurangan:** Ulang miskonsepsi AUC. Klaim "data kami seimbang" perlu diverifikasi (Celeb-DF penuh
  timpang; cek logika sampling).
- **Skor:** 5/10

## Pertanyaan #4 — Bahaya split acak per-frame & cara menghindari

**Jawaban ringkas mahasiswa:** Bahaya: frame dari video yg sama bisa terambil di split berbeda. Solusi:
frame diberi video_id → tidak mengambil dari video yg sama (split by video).

**Evaluasi**
- **Ketepatan:** BENAR. Masalah = data/frame leakage; solusi = split by video_id (semua frame satu
  video → satu split). Sesuai build_splits.py (stratified by video).
- **Kedalaman:** Baik, tapi belum eja "kenapa serius": leakage → model menghafal ciri video (orang,
  latar, lighting, kompresi) bukan belajar isyarat forgery umum → metrik uji MENGGELEMBUNG / tidak jujur.
- **Kekurangan:** Tak menamai "data leakage" & tak jelaskan efek metrik menggelembung.
- **Skor:** 7/10

## Pertanyaan #5 — (Skenario) satu perubahan besar utk perbaiki cabang frekuensi

**Jawaban ringkas mahasiswa:** Memanfaatkan FASE (sesuai saran). Karena fase mencakup informasi posisi &
letak struktur.

**Evaluasi**
- **Ketepatan:** Pilihan sah & terdasar (Liu SPSL: fase memuat artefak upsampling kumulatif; cabang
  mereka magnitude-only membuang fase). "Fase = info posisi/struktur" benar (Oppenheim & Lim: fase bawa
  info struktural citra).
- **Kedalaman:** Tipis. Belum kaitkan ke mekanisme kegagalan deepfake (upsampling meninggalkan artefak
  di fase yg magnitude buang). Belum PERTAHANKAN kenapa fase DULU dibanding opsi lain — padahal saya
  minta itu.
- **Kekurangan:** Justifikasi prioritas lemah; potensi TAK KONSISTEN dgn akar utama BAB V sendiri
  (dugaan utama = crop+kompresi, bukan fase).
- **Skor:** 6/10

### Pertanyaan #5a (follow-up, konsistensi) — Kenapa fase dulu, bukan hapus crop?

**Jawaban ringkas mahasiswa:** Di cabang spasial, crop membantu; karena studi komparatif, crop dibuat
adil (sama semua). Maka utamakan fase utk bantu cabang frekuensi.

**Evaluasi**
- **Ketepatan:** Argumen fairness/komparasi terkontrol SAH & menunjukkan pemahaman: hapus crop merusak
  komparasi terkendali, sedangkan tambah fase memperbaiki freq tanpa merusak keadilan.
- **Kedalaman:** Ada slip logika halus: kendala "fairness" itu milik studi SAAT INI; pada FUTURE WORK
  perbaikan freq, kendala itu bisa dilonggarkan. BAB V mereka SENDIRI mengusulkan "FFT citra penuh tanpa
  crop" → jadi argumen "harus tetap crop" justru bertentangan dgn saran sendiri. Ideal: future-work bebas
  jalankan ablation full-image FFT.
- **Kekurangan:** Mencampur kendala studi-sekarang dgn kebebasan future-work; tak akui saran full-image
  di BAB V.
- **Skor:** 6/10

## Pertanyaan #6 — Beda early vs late fusion; kenapa late fusion?

**Jawaban ringkas mahasiswa:** Early = 4 kanal (RGB+frekuensi digabung di awal). Late = konkatenasi
fitur dari masing-masing cabang. Pilih late fusion untuk melihat dominasi tiap cabang, & bisa langsung
memakai fitur tiap cabang.

**Evaluasi**
- **Ketepatan:** Distinksi BENAR (early=input 4-kanal; late=fitur-level concat; cocok EarlyFusionXception
  vs HybridTwoBranch). Alasan "melihat dominasi tiap cabang" = JUSTRU alasan terbaik utk studi mereka
  (isolasi kontribusi = RM3). Bagus & selaras tesis.
- **Kedalaman:** Alasan #2 kabur. Poin lebih dalam yg terlewat: late fusion memungkinkan tiap cabang
  punya ARSITEKTUR sendiri sesuai modalitas (Xception utk RGB, FreqCNN utk FFT yg statistiknya beda),
  & pretraining ImageNet (mustahil utk input 4-kanal early fusion).
- **Kekurangan:** Tak sebut arsitektur per-modalitas & kendala pretraining.
- **Skor:** 7/10

## Pertanyaan #7 — Kenapa FreqCNN ringan buatan sendiri, bukan arsitektur besar?

**Jawaban ringkas mahasiswa:** Per Qian, backbone frekuensi mereka bukan frekuensi murni (ada campur
spasial); kami mau studi komparatif MURNI cabang frekuensi → CNN buatan sendiri. Jujur: keputusan itu
mungkin salah satu penyumbang kegagalan.

**Evaluasi**
- **Ketepatan:** Rasional SAH & selaras tesis (isolasi cabang frekuensi murni utk ukur kontribusi
  domain; Qian/F3-Net memang mencampur freq+spasial). Kejujuran mengakui shallow CNN mungkin menyumbang
  kegagalan = bagus & memperkuat scoping (hasil spesifik-implementasi).
- **Kedalaman:** Alasan tambahan terlewat: (a) peta FFT 1-kanal beda statistik → pretrained ImageNet tak
  transfer; (b) data terbatas → model besar overfit; (c) kapasitas dangkal vs spectral bias (Rahaman/
  Wang) → sulit belajar selektivitas high-freq.
- **Kekurangan:** Tak sebut pretraining-tak-transfer, overfitting, kapasitas/spectral-bias.
- **Skor:** 7/10

## Pertanyaan #8 — (Re-test) Ideal SE gating thd fitur noise & mekanismenya

**Jawaban ringkas mahasiswa:** SE gating membobot, menekan fitur tak penting spt "background noise".
3 tahap: Squeeze (kecilkan ke 128 + global average pooling pilih bobot berguna), Excitation
(kembalikan dimensi), Scale. "Kerjanya seperti filter".

**Evaluasi**
- **Ketepatan:** Perbaikan: 3 tahap Squeeze-Excitation-Scale disebut BENAR; TIDAK mengulang error
  "sigmoid=loss". TAPI inaccuracy baru: "global average pooling" itu SE-Net tekstual utk feature-MAP;
  SEGate MEREKA bekerja pd VEKTOR 512-d gabungan → TIDAK ada GAP, squeeze = Linear(512→128) saja.
  Mereka membaca paper, bukan kode sendiri.
- **Kedalaman:** Belum jawab "lewat mekanisme apa MEMUTUSKAN menekan": lewat PELATIHAN — backprop
  menurunkan bobot gate utk fitur yg tak membantu loss; Sigmoid → bobot [0,1]; Scale = kali. Sigmoid
  tak disebut. Metafora "filter/background noise" longgar.
- **Kekurangan:** GAP salah-terap; mekanisme belajar & sigmoid absen.
- **Skor:** 6/10

### Pertanyaan #8a (follow-up) — Dari mana SE gate "belajar" menekan fitur noise?

**Jawaban ringkas mahasiswa:** Melalui backpropagation, bobot fitur tak berguna diturunkan saat training.
(Mahasiswa mengakui belum paham SE gate & minta penjelasan lebih lengkap di MD.)

**Evaluasi**
- **Ketepatan:** BENAR. Backprop/gradient descent menyetel jaringan gate agar fitur yg tak menurunkan
  loss diberi bobot kecil. Inti mekanisme tepat.
- **Kedalaman:** Ringkas tapi kena. Kejujuran mengakui belum paham = sikap baik.
- **Kekurangan:** Perlu memantapkan detail (lihat Catatan Penjelasan di bawah).
- **Skor:** 7/10

---

## CATATAN PENJELASAN LENGKAP: SE GATING (sesuai kode `src/models/hybrid_fusion.py`)

**PENTING — versi kode kalian ≠ versi buku teks SE-Net (Hu et al.).**
SE-Net asli bekerja pada *feature map* konvolusi (H×W×C) dan tahap *squeeze*-nya memakai **global
average pooling** untuk meringkas tiap kanal jadi satu angka. **SE gate kalian TIDAK begitu**, karena
inputnya sudah berupa **vektor fitur 512-d** (256 spasial + 256 frekuensi hasil concat), bukan peta
spasial. Jadi **tidak ada global average pooling** di implementasi kalian. Jangan sebut GAP saat sidang.

**Kode sebenarnya:**
```
gate = Linear(512→128) → ReLU → Linear(128→512) → Sigmoid    # menghasilkan bobot g ∈ [0,1]^512
output = x * g                                                # dikalikan elemen-wise ke fitur
```

**Tiga tahap, dipetakan ke kode kalian:**
1. **Squeeze:** `Linear(512→128)` — meringkas 512 fitur ke bottleneck 128 dimensi (memaksa jaringan
   merangkum pola antar-fitur, bukan menghafal tiap fitur). *(Bukan pooling — hanya proyeksi linier.)*
2. **Excitation:** `Linear(128→512) → Sigmoid` — mengembalikan ke 512 dan menghasilkan **satu bobot
   g_i ∈ [0,1] untuk tiap fitur**.
3. **Scale:** `x * g` — tiap fitur dikalikan bobotnya. g_i≈0 = ditekan (dibuang); g_i≈1 = dipertahankan.

**Kenapa Sigmoid (bukan ReLU/tanh/softmax)?**
Karena gate butuh nilai **[0,1] independen per fitur** → "seberapa banyak fitur ini dipertahankan".
ReLU tak berbatas atas; tanh bisa negatif (membalik tanda fitur); softmax memaksa total = 1 (fitur saling
berebut). Sigmoid ini **TIDAK ADA hubungannya** dengan sigmoid di BCEWithLogitsLoss — itu dua hal beda.

**Bagaimana ia "memutuskan" menekan fitur frekuensi yang noise? (jawaban Samuel yang benar, diperjelas)**
Tidak ada aturan tulis-tangan. Jaringan gate dilatih **end-to-end bersama seluruh model**. Saat
**backpropagation**, jika suatu fitur (mis. dari cabang frekuensi) tidak berkorelasi dengan label,
menaikkan bobotnya tidak menurunkan loss, sehingga gradient mendorong `Linear` gate menghasilkan bobot
kecil untuk fitur itu. Bobotnya **turun dengan sendirinya** karena itulah yang meminimalkan loss.
Gate ini juga **adaptif per-sampel** (bobot dihitung dari vektor fitur tiap input), bukan bobot tetap.

**Kaitan ke hasil kalian (siap-siap ditanya penguji):**
Secara teori SE gate *seharusnya* menekan cabang frekuensi yang ≈noise. Tapi hasil kalian menunjukkan
hybrid TETAP tidak mengungguli spasial murni. Artinya SE gate **tidak sepenuhnya menetralkan** noise
frekuensi. Alasan yang bisa kalian sampaikan: (a) gate [0,1] itu "lunak", tidak bisa memaksa bobot
persis 0; (b) dengan data terbatas gate sendiri belum tentu belajar sempurna; (c) fitur noise tetap
menambah variansi/gradien yang mengganggu; (d) proyeksi & BatchNorm sebelum gate sudah mencampur sinyal.
Jujurnya: SE gate mengurangi dampak noise, tetapi tidak menghapusnya, sehingga cabang frekuensi tetap
menyeret performa hybrid ke bawah baseline spasial.

## Pertanyaan #9 — (Jebakan) In-dataset AUC CDF (0,97) > FFPP (0,78) padahal CDF "lebih sulit"?

**Jawaban ringkas mahasiswa:** AUC in-dataset CDF lebih tinggi karena dilatih di dataset itu sendiri, &
CDF hanya 1 metode generatif. Kualitas citra CDF lebih tinggi (tanpa kompresi).

**Evaluasi**
- **Ketepatan:** Inti BENAR (1 metode konsisten → mudah dipisah in-dataset → AUC 0,97; FFPP 4 metode
  termasuk NeuralTextures subtil → 0,78). Tapi belum eja RESOLUSI kontradiksi: "sulit/berkualitas tinggi"
  itu utk CROSS-dataset (detektor asing gagal di CDF), BUKAN in-dataset.
- **Kedalaman:** Poin "kualitas tinggi/tanpa kompresi" justru agak KONTRADIKTIF — kualitas tinggi =
  artefak subtil = harusnya lebih SULIT, bukan lebih mudah. Alasan dominan = konsistensi 1 metode.
- **Kekurangan:** Distinksi in-dataset vs cross-dataset tak eksplisit; poin kualitas goyah.
- **Skor:** 6/10

## Pertanyaan #10 — (Jebakan) Apakah judul "Hybrid" menyesatkan krn hybrid bukan pemenang?

**Jawaban ringkas mahasiswa:** Sesuai tujuan BAB 1 (lihat apakah frekuensi menahan penurunan performa),
yg ditonjolkan "hybrid"; studi ini KOMPARATIF, bukan klaim "peningkatan" deteksi via hybrid.

**Evaluasi**
- **Ketepatan:** Pertahanan BENAR & konsisten. Judul = "Studi KOMPARATIF ... Hybrid ... TERHADAP Model
  Domain Tunggal" → hybrid = OBJEK studi, bukan klaim pemenang. Kata "komparatif" = pengaman.
- **Kedalaman:** Baik. Penguat yg terlewat: (1) tunjuk eksplisit kata "Komparatif"/"terhadap Model
  Domain Tunggal" sbg disclaimer; (2) SEBUT bahwa judul SENGAJA DIUBAH dari "Metode PENINGKATAN Deteksi
  Deepfake..." (lama, overclaim) menjadi "Studi Komparatif..." — bukti kejujuran ilmiah. Pakai ini!
- **Kekurangan:** Tak memanfaatkan riwayat retitle & kata kunci judul sbg pembelaan.
- **Skor:** 7/10

## Pertanyaan #11 — (Skenario etis) Model dipakai utk bukti pengadilan, lalu runtuh

**Jawaban ringkas mahasiswa:** (1) Model bisa memfitnah orang jika gagal deteksi (tak 100% akurat).
(2) Penelitian kami menekankan pentingnya cross-dataset, karena real-life menerima input BARU, bukan
video dari datasetnya sendiri.

**Evaluasi**
- **Ketepatan:** Dua poin sah & relevan. Poin (2) KUAT — mengaitkan temuan cross-dataset collapse ke
  kehati-hatian dunia nyata (detektor hadapi input out-of-distribution). Peningkatan jelas dari sesi lalu
  (etika 5→7).
- **Kedalaman:** Belum sampaikan PESAN konkret yg saya minta: deteksi otomatis TAK BOLEH jadi bukti
  tunggal/penentu di keputusan berisiko tinggi; harus alat BANTU + tinjauan ahli manusia; ungkap
  keterbatasan & ketidakandalan OOD. Akuntabilitas: manusia/institusi tetap penanggung jawab, model
  hanya alat bantu; memakainya sbg "orakel" = tak etis.
- **Kekurangan:** Pesan-ke-pengguna & akuntabilitas belum eksplisit.
- **Skor:** 7/10

## Pertanyaan #12 — Optimizer & beda AdamW vs Adam

**Jawaban ringkas mahasiswa:** AdamW. Pada Adam standar efek regularisasi bervariasi bergantung learning
rate; AdamW tidak, sehingga lebih stabil.

**Evaluasi**
- **Ketepatan:** Nama BENAR (AdamW, sesuai train.py). Konsep BENAR: di Adam, weight decay tercampur/
  tergandeng dgn skala LR adaptif → efek regularisasi tak konsisten; AdamW men-DECOUPLE weight decay dari
  update gradien → regularisasi konsisten. Topik yg sering tertukar, dan dijawab tepat.
- **Kedalaman:** Baik tapi ringkas. Belum menamai "decoupled weight decay" & mekanismenya (Adam masukkan
  weight decay ke gradien; AdamW terapkan langsung ke bobot) → generalisasi lebih baik.
- **Kekurangan:** Istilah teknis & mekanisme eksplisit belum disebut.
- **Skor:** 7/10

## Pertanyaan #13 — Hasil bertentangan dgn SpecXNet (yg lapor dual-domain berhasil)

**Jawaban ringkas mahasiswa:** SpecXNet pakai joint learning; kami ablasi penuh (cabang terpisah + SE
gating) → bisa lihat kontribusi tiap cabang. Kami TIDAK bilang freq tak berguna SECARA UMUM, hanya di
ruang lingkup kami. Saran: tambah fase sbg komplementer.

**Evaluasi**
- **Ketepatan:** KUAT & ter-scope benar. Divergensi dijelaskan via beda metode (joint learning vs
  late-fusion cabang terpisah lightweight) → hasil bukan "salah" tapi setup berbeda. Scoping ke ruang
  lingkup = langkah ilmiah tepat (konsisten dgn kekuatan sesi lalu). Arahkan ke future work (fase).
- **Kedalaman:** Baik. Penguat: sebut beda konkret (skala data/kompute SpecXNet lebih besar; representasi
  mereka log-mag+highpass saja; FreqCNN dangkal). Intinya: MANFAAT freq bergantung CARA integrasi.
- **Kekurangan:** Frasa "ablasi dengan SE gating" agak keliru (ablasi = jalankan spatial/freq/hybrid
  terpisah; SE gating bagian fusi hybrid). Beda konkret implementasi belum dirinci.
- **Skor:** 8/10

## Pertanyaan #14 — Keterbatasan lain (selain cabang frekuensi), min. 2

**Jawaban ringkas mahasiswa:** (1) SE gate kurang kuat. (2) Hanya 3 seed → konsisten sbg temuan tapi
belum valid penuh secara statistik.

**Evaluasi**
- **Ketepatan:** Poin (2) SANGAT BAIK — internalisasi feedback sesi lalu soal rigor statistik, frasa
  tepat ("konsisten sbg temuan, belum valid statistik penuh"). Poin (1) lemah/redundan (sub-bagian
  kegagalan freq, bukan keterbatasan independen).
- **Kedalaman:** Melewatkan keterbatasan yg lebih besar & jelas: (a) LEVEL FRAME saja, TANPA pemodelan
  TEMPORAL antar-frame (padahal saran BAB V sebut ini); (b) skala data kecil (100–1000 video); (c)
  cakupan hanya 2 dataset/2 arah; deepfake diffusion terbaru tak tercakup → simpulan mungkin tak transfer;
  (d) magnitude-only tanpa fase; (e) confound crop/kompresi.
- **Kekurangan:** Poin ke-2 kuat, poin ke-1 lemah; keterbatasan besar (temporal, skala data, cakupan
  generator) terlewat.
- **Skor:** 6/10

## Pertanyaan #15 — Kenapa per-frame bukan temporal? Kelebihan & kekurangan

**Jawaban ringkas mahasiswa:** Karena yg diteliti domain frekuensi, jadi di ruang lingkup ini aspek
temporal diabaikan.

**Evaluasi**
- **Ketepatan:** Alasan scoping SAH tapi diucapkan CIRCULAR & tipis. Versi kuat: pertanyaan riset (apakah
  frekuensi membantu spasial) inheren per-CITRA (Xception & FFT sama-sama operasi per-gambar); menambah
  temporal = variabel ketiga yg mengaburkan komparasi spasial-vs-frekuensi. Frame-level = komparasi
  terkontrol + lebih murah + lebih banyak sampel + selaras baseline Rossler.
- **Kedalaman:** TAK menjawab yg diminta (kelebihan & kekurangan). Yg dikorbankan: isyarat TEMPORAL
  (flicker, gerak tak natural, diskontinuitas antar-frame, kedip tak wajar) — fake yg meyakinkan per-frame
  tapi tak konsisten antar-waktu jadi lolos.
- **Kekurangan:** Circular, tipis, tak sebut trade-off yg diminta.
- **Skor:** 5/10

## Pertanyaan #16 — Kenapa BCE (1 output) bukan CrossEntropy 2 kelas; guna label smoothing (dijawab ulang)

**Jawaban ringkas mahasiswa:** BCE karena output hanya dua (0 real, 1 fake). Label smoothing meredam
overconfidence model hybrid (backbone pretrained + cabang baru) yg bisa hasilkan logit ekstrem.

**Evaluasi**
- **Ketepatan:** Poin 2 BAGUS (label smoothing meredam overconfidence; konteks hybrid→logit ekstrem
  cerdas). Poin 1 TAK BERUBAH meski sudah diberi kesempatan ulang & di-nudge. "Karena kelasnya dua"
  bukan alasan pembeda (CrossEntropy pun 2 kelas).
- **Kedalaman:** Alasan benar poin 1: biner butuh 1 neuron/1 logit → sigmoid → P(fake); P(real)=1−P(fake)
  jadi 1 output cukup; CrossEntropy 2 kelas = 2 output redundan. BCEWithLogitsLoss = sigmoid+BCE stabil
  numerik.
- **Kekurangan:** Poin 1 gagal jawab "kenapa 1 output bukan 2" walau sudah retry.
- **Skor:** 6/10

## Pertanyaan #17 — Kenapa magnitudo FFT di-log (log1p)?

**Jawaban ringkas mahasiswa:** Magnitudo murni angka sangat besar; di-log jadi lebih kecil tapi tetap
"preserve range".

**Evaluasi**
- **Ketepatan:** Permukaan benar (magnitudo besar → log mengecilkan). TAPI "preserve range" KELIRU —
  log justru MENGOMPRES rentang dinamis (itu tujuannya). Magnitudo FFT punya rentang dinamis SANGAT lebar
  (DC/low-freq >> high-freq).
- **Kedalaman:** Lewat inti pertanyaan "kalau log dihapus": tanpa log, komponen DC/low-freq raksasa akan
  MENDOMINASI, artefak high-freq halus (yg justru dibutuhkan) jadi tak terlihat/negligible; nilai mentah
  besar juga buruk utk training NN (normalisasi/gradien).
- **Kekurangan:** "preserve range" terbalik (harusnya kompres); efek penghapusan log tak dijelaskan.
- **Skor:** 5/10

