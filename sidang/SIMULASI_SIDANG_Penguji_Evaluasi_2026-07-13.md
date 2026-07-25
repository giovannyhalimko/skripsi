# Simulasi Sidang Skripsi — Rekam Evaluasi Penguji

**Tanggal:** 2026-07-13
**Mahasiswa yang diuji:** Samuel Onasis (221110680)
**Kontribusi:** Penyusunan dokumen BAB I–V, evaluasi hasil pelatihan model, studi komparatif
**Judul:** Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal
**Penguji (simulasi):** Dosen Penguji Senior — Teknik Informatika

> Berkas ini merekam setiap pertanyaan, jawaban ringkas mahasiswa, dan evaluasi penguji
> (Ketepatan / Kedalaman / Kekurangan / Skor 1–10) untuk kepentingan refleksi mahasiswa.

---

## Perkenalan

Mahasiswa memperkenalkan judul, kontribusi, latar belakang singkat (video generatif sebagai
ancaman forensik digital), dan ringkasan metode (XceptionNet = spasial, FFT+FreqCNN = frekuensi,
hibrida = konkatenasi dua cabang + SE gating).

**Catatan penguji:** Istilah "SE gating = noise filtering" ditandai untuk digali lebih dalam.
Karakterisasi ini kurang tepat secara teknis (SE = channel recalibration/attention, bukan noise filtering).

---

## Pertanyaan #1 — Research Gap / Alasan Penelitian Perlu Ada

**Pertanyaan:** Mengapa penelitian ini perlu ada? XceptionNet sudah kuat dan banyak dipakai.
Apa research gap-nya?

**Jawaban ringkas mahasiswa:** GAN makin berkembang, artefak spasial makin sulit dideteksi.
Penelitian Durall & Alam menyarankan menambah domain frekuensi, tetapi via joint learning.
Teknik yang dipakai tim ini adalah *late fusion* antara domain frekuensi murni (FreqCNN) dengan
XceptionNet, yang belum ditemukan di literatur. Karena itu tertarik mengomparasi apakah penambahan
domain frekuensi murni ke XceptionNet meningkatkan kinerja.

**Evaluasi**
- **Ketepatan:** Cukup baik. Berhasil menyebut motivasi (degradasi artefak spasial seiring
  kemajuan GAN) dan membedakan late fusion vs joint/early fusion. Menyebut referensi konkret.
- **Kedalaman:** Sedang. Ada pembedaan metodologis yang jelas, tetapi klaim kebaruan ("belum ada
  late fusion freq murni + Xception") terlalu kuat dan rapuh — Alam (SpecXNet) justru arsitektur
  *dual-domain two-branch* yang sangat dekat; Luo, Qian (F3-Net) juga fusi spasial-frekuensi.
- **Kekurangan:**
  1. Karakterisasi Durall kurang tepat — Durall bukan mengusulkan joint learning dengan Xception,
     melainkan menunjukkan GAN gagal mereproduksi distribusi spektral (dasar teori, bukan arsitektur fusi).
  2. Kebaruan diletakkan pada *kombinasi arsitektur*, bukan pada *mengapa late fusion seharusnya
     lebih baik*. Novelty ≠ kontribusi ilmiah.
  3. Belum menjelaskan mekanisme: mengapa domain frekuensi menangkap yang tidak tertangkap spasial.
- **Skor:** 7/10

### Pertanyaan #1a (follow-up) — Beda dari SpecXNet

**Pertanyaan:** SpecXNet sudah dual-domain two-branch fusion. Apa bedanya penelitian ini, dan
kenapa beda itu = kontribusi, bukan pengulangan?

**Jawaban ringkas mahasiswa:** Bedanya pakai SE gating untuk filter noise, dan domain frekuensi
dibangun sendiri memanfaatkan log-magnitudo yang memuat artefak frekuensi / GAN fingerprints yang
diharapkan meningkatkan akurasi.

**Evaluasi**
- **Ketepatan:** Kurang. Dua komponen yang disebut (SE gating & log-magnitudo FFT) keduanya
  komponen *off-the-shelf/standar* — SE = Hu et al (Squeeze-Excitation), log-magnitudo FFT adalah
  representasi baku di literatur frekuensi (Durall, Zhang). Keduanya tidak memisahkan penelitian ini
  dari SpecXNet yang notabene juga jaringan dual-domain spektral.
- **Kedalaman:** Dangkal. Menyebut ulang komponen, bukan mengartikulasikan kontribusi.
- **Kekurangan:**
  1. Kontribusi paling defensible tidak disebut: ini **studi komparatif** (spasial vs frekuensi vs
     hibrida, termasuk lintas-dataset FFPP↔CDF) dengan cabang frekuensi yang **terpisah penuh**
     sehingga kontribusi tiap domain bisa diisolasi (ablation bersih) — bukan klaim arsitektur baru.
  2. Mengulang mischaracterization "SE gating = noise filtering" (kedua kalinya).
  3. Klaim "log-magnitudo diharapkan meningkatkan akurasi" bertentangan dengan temuan sendiri:
     cabang frekuensi justru *underperform* (lihat SIDANG_QA_freq_negative.md).
- **Skor:** 5/10

---

---

> ⚠️ **SESI DI ATAS DIBATALKAN.** Atas permintaan mahasiswa, simulasi diulang dari awal
> dengan aturan ketat: satu pertanyaan, satu jawaban. Rekaman sesi baru dimulai di bawah.

---

# === SIMULASI ULANG — Satu Pertanyaan Per Waktu ===

## Pertanyaan #1 — Definisi & urgensi deepfake

**Pertanyaan:** Apa itu deepfake dan mengapa ia jadi masalah? (dengan bahasa sendiri)

**Jawaban ringkas mahasiswa:** Deepfake = citra yang dimanipulasi dengan model GAN; dianggap masalah
karena sering dipakai menyebarkan misinformasi.

**Evaluasi**
- **Ketepatan:** Lemah untuk pertanyaan dasar. Dua imprecision penting:
  (a) Deepfake tidak terbatas GAN — face-swap deepfake orisinal berbasis *autoencoder*; kini juga
  diffusion. Lebih krusial: dataset penelitian ini sendiri (FaceForensics++) memuat Face2Face &
  FaceSwap yang **bukan GAN** (grafika komputer/autoencoder). Jadi "dimanipulasi dengan GAN"
  bertentangan dengan data yang dipakai.
  (b) Deepfake pada konteks skripsi ini adalah **video**, bukan sekadar citra tunggal (FF++, Celeb-DF
  adalah dataset video).
- **Kedalaman:** Dangkal. Hanya menyebut satu bahaya (misinformasi). Belum menyinggung penipuan
  finansial/CEO-voice-scam, konten eksplisit non-konsensual, pencurian identitas, dan yang paling
  relevan dengan tema: **erosi kepercayaan pada bukti forensik digital**.
- **Kekurangan:** Definisi terlalu sempit dan salah kaitan dengan dataset sendiri; urgensi kurang.
- **Skor:** 4/10

### Pertanyaan #1a (follow-up) — Face2Face & FaceSwap = GAN?

**Jawaban ringkas mahasiswa:** Minta maaf, deepfake bisa dari model generatif lain juga, bukan hanya
GAN. Face2Face & FaceSwap memakai "blending, bounding box".

**Evaluasi**
- **Ketepatan:** Koreksi definisi diterima (bagus, mau mengakui). Tapi penjelasan Face2Face/FaceSwap
  masih dangkal & sebagian keliru. Faktanya: Face2Face = *facial reenactment berbasis grafika
  komputer / model 3D morphable* (transfer ekspresi, bukan deep learning, bukan GAN). FaceSwap =
  *face swap berbasis model 3D + blending* (juga bukan GAN). Kategori "Deepfakes" di FF++ =
  autoencoder; NeuralTextures = neural rendering dgn adversarial loss. "Bounding box" bukan metode
  manipulasi.
- **Kedalaman:** Tipis. Mahasiswa yang melatih/menguji di FF++ idealnya tahu 4 metode manipulasinya.
- **Kekurangan:** Belum menguasai isi dataset sendiri secara teknis.
- **Skor:** 5/10

## Pertanyaan #2 — Rumusan masalah

**Pertanyaan:** Sebutkan rumusan masalah penelitian Saudara.

**Jawaban ringkas mahasiswa:** (1) Penurunan performa XceptionNet saat lintas dataset;
(2) seberapa MENINGKAT performa cabang spasial ketika ditambah cabang frekuensi FFT;
(3) kontribusi masing-masing cabang (spasial vs frekuensi) pada akurasi, presisi, recall, AUC.

**Naskah asli (Slide 5 / dokumen):** RM1 = sejauh mana detektor spasial menurun lintas dataset;
RM2 = sejauh mana penambahan FFT **memperkecil penurunan** tsb; RM3 = seberapa besar kontribusi
masing-masing komponen.

**Evaluasi**
- **Ketepatan:** RM1 & RM3 tepat. **RM2 salah bingkai** — diucapkan "seberapa MENINGKAT performa",
  padahal naskah = "memperkecil PENURUNAN lintas-dataset". Arah maknanya berbeda.
- **Kedalaman:** Cukup; paham ketiganya bersifat mengukur/membandingkan.
- **Kekurangan:** Salah bingkai RM2 berisiko merusak konsistensi RM ↔ kesimpulan (temuan negatif).
- **Skor:** 6/10

### Pertanyaan #2a (follow-up) — Kenapa bingkai RM2 penting?

**Jawaban ringkas mahasiswa:** Mengakui "meningkat" bukan kata yang tepat & meleset dari hasil
(baseline spasial tidak meningkat).

**Evaluasi**
- **Ketepatan:** Jujur mengakui (baik), tapi hanya menjawab setengah — belum menjelaskan alasan
  metodologisnya.
- **Kedalaman:** Dangkal.
- **Kekurangan:** Poin inti belum tersampaikan: bingkai "meningkatkan" mengubah RM jadi hipotesis
  kinerja yang harus dibuktikan → skripsi tampak gagal menjawab RM sendiri. Bingkai "mengukur sejauh
  mana memperkecil penurunan" membuat temuan negatif tetap sah = melindungi validitas skripsi.
- **Skor:** 5/10

## Pertanyaan #3 — Teori: apa yang dilihat domain frekuensi

**Pertanyaan:** Secara teori apa yang bisa dilihat FFT pada deepfake yang sulit ditangkap CNN
spasial? Jelaskan mekanismenya.

**Jawaban ringkas mahasiswa:** Artefak frekuensi (Odena, Durall) — deepfake mengandung pola tertentu
"dibasiskan terang gelapnya cahaya", disebut GAN fingerprints, berpola periodik seperti checkerboard.

**Evaluasi**
- **Ketepatan:** Recall istilah & referensi benar (Odena=checkerboard, Durall=distribusi spektral,
  GAN fingerprints, pola periodik). TAPI mekanisme keliru: "terang gelapnya cahaya" bukan sumbernya.
  Checkerboard lahir dari operasi **upsampling / transposed convolution (deconvolution)** di
  generator; Durall = GAN gagal mereproduksi distribusi spektral yang benar (defisit/kelainan
  frekuensi tinggi).
- **Kedalaman:** Sedang-dangkal. Belum menjawab inti pertanyaan: KENAPA lebih mudah di domain
  frekuensi daripada spasial. (Pola periodik/global terlokalisasi jadi puncak diskrit di FFT; CNN
  spasial berbias tekstur & belajar low-freq dulu — spectral bias Rahaman/Wang.)
- **Kekurangan:** Mekanisme fisik salah label; keunggulan frekuensi-vs-spasial tak dijelaskan.
- **Skor:** 6/10

### Pertanyaan #3a (follow-up) — Asal checkerboard & pola periodik di FFT

**Jawaban ringkas mahasiswa:** (1) Dari konvolusi/transposed/upsampling; GAN generate low-res→hi-res
lewat konvolusi → muncul pola periodik. (2) Pola periodik masuk spektrum "dalam bentuk overlapping";
per Durall, GAN fokus perbaiki visual tapi menyebabkan distorsi frekuensi tinggi.

**Evaluasi**
- **Ketepatan:** Bagian 1 tepat (transposed conv/upsampling, low→hi res). Bagian 2 meleset —
  "overlapping" bukan konsep yang benar.
- **Kedalaman:** Bagian 2 setengah; poin Durall benar tapi bukan jawaban "apa yang terjadi ke pola
  periodik di FFT".
- **Kekurangan:** Inti hilang: pola periodik spasial → **puncak/spikes tajam terlokalisasi** di
  frekuensi tertentu + harmonik (energi memusat). Itu yang bikin mudah dideteksi.
- **Skor:** 6/10

## Pertanyaan #4 — Tahapan preprocessing video → siap model

**Pertanyaan:** Jelaskan runtut preprocessing dari video mentah sampai siap masuk model.

**Jawaban ringkas mahasiswa:** Input → ekstrak frame 5 FPS → MTCNN crop → split dataset →
spasial: resize 224, normalisasi ImageNet, augmentasi; frekuensi: grayscale, resize 224, FFT shift,
magnitude + high-pass filter → log scaling → z-score → augmentasi.

**Evaluasi**
- **Ketepatan:** TINGGI. Dicocokkan ke `fft_utils.image_to_fft_logmag`: grayscale→resize→fft2→
  fftshift→abs(magnitude)→highpass mask (Gaussian cutoff 0.15)→log1p; z-score via fft_stats.json saat
  load. Urutan & langkah benar. Menyebut high-pass filter yang memang ADA di kode = poin plus (jarang
  disebut/sering diarang mahasiswa).
- **Kedalaman:** Baik, runtut, sesuai implementasi.
- **Kekurangan:** (1) "Pembagian dataset" tanpa menekankan split **by video_id** (anti frame-leakage).
  (2) Belum jelaskan KENAPA ada high-pass filter.
- **Skor:** 8/10

### Pertanyaan #4a (follow-up) — Kenapa high-pass (tekan tengah spektrum)?

**Jawaban ringkas mahasiswa:** High-pass menekan low frequency; per Durall distorsi kebanyakan di
high frequency, jadi tekan low-freq agar model fokus ke anomali high-freq.

**Evaluasi**
- **Ketepatan:** Benar (high-pass tekan low-freq; Durall high-freq distortion).
- **Kedalaman:** Sedang, agak berputar. Belum sebut: (1) pusat spektrum = DC/energi terbesar yang
  mendominasi peta magnitudo & normalisasi → artefak halus tenggelam; (2) low-freq hampir identik
  real vs fake = non-diskriminatif.
- **Kekurangan:** Dua poin inti di atas.
- **Skor:** 7/10

## Pertanyaan #5 — Kalau teori benar, kenapa cabang frekuensi gagal? (kritis)

**Pertanyaan:** Teori mendukung (Odena/Durall + high-pass), tapi cabang frekuensi ~acak
(AUC 0,56–0,61). Kenapa gagal?

**Jawaban ringkas mahasiswa:** Sesuai BAB V: (1) hilangnya sidik jari spektral akibat face-cropping
& kompresi dataset; (2) pakai log-magnitudo, mengabaikan fase.

**Evaluasi**
- **Ketepatan:** Baik & jujur. Cocok dgn BAB V saran #1 (verifikasi grep: face-cropping+kompresi,
  usulan citra penuh/fasa/multi-skala). Konsisten dgn naskah.
- **Kedalaman:** Cukup, belum tuntas. Sebab fundamental tak disebut: **mismatch arsitektural** —
  CNN mengandalkan lokalitas spasial/translation-invariance, tak bermakna pada peta spektrum FFT;
  plus spectral bias (Rahaman/Wang) → sulit belajar selektivitas high-freq.
- **Kekurangan:** Sisi arsitektur/inductive-bias belum disinggung.
- **Skor:** 8/10

### Pertanyaan #5a (follow-up, jebakan) — Kalau crop merusak freq, kenapa tetap crop?

**Jawaban ringkas mahasiswa:** (1) Empiris: face-crop menaikkan akurasi spasial signifikan; tanpa
crop background = noise. (2) Crop diterapkan ke freq juga demi perbandingan ADIL (perlakuan sama).
(3) Referensi Li et al memakai face crop untuk training CNN.

**Evaluasi**
- **Ketepatan:** Kuat. 3 argumen sah (empiris, fairness/kontrol, literatur). Li et al terverifikasi
  ada (face warping artifacts / Celeb-DF). Mematahkan jebakan.
- **Kedalaman:** Baik — paham menyamakan praproses menjaga validitas komparasi.
- **Kekurangan:** Klaim "crop merusak sidik jari spektral" masih DUGAAN (belum diuji ablation
  dgn/tanpa crop pd cabang freq). Kesimpulan harus dibatasi ruang lingkup ("dalam konfigurasi diuji").
- **Skor:** 8/10

## Pertanyaan #6 — Interpretasi recall 0,07 (CDF→FFPP)

**Pertanyaan:** Apa arti recall 0,07 secara praktis? (dari 100 video palsu?)

**Jawaban ringkas mahasiswa:** Dari 100 video palsu, hanya ~7 yang benar dikategorikan palsu.

**Evaluasi**
- **Ketepatan:** Tepat (recall = TP/(TP+FN); 7/100 terdeteksi).
- **Kedalaman:** Cukup; berhenti di definisi. Belum tarik konsekuensi: 93/100 palsu LOLOS dianggap
  asli → praktis gagal total lintas-dataset.
- **Kekurangan:** Implikasi praktis & keparahan belum disampaikan.
- **Skor:** 8/10

### Pertanyaan #6a (follow-up) — Kenapa RECALL yang runtuh? (mekanisme)

**Jawaban ringkas mahasiswa:** Model dilatih CDF hanya kenal artefak 1 metode generatif; FFPP punya
4 metode → generalisasi model CDF kurang.

**Evaluasi**
- **Ketepatan:** Akar benar (CDF ragam manipulasi sempit vs FFPP 4 metode).
- **Kedalaman:** Belum jawab "kenapa recall spesifik". Mekanisme: model belajar "palsu = artefak khas
  CDF"; palsu FFPP tak memicu sinyal → divonis asli → false negative menumpuk → recall jatuh. Wajah
  ASLI mirip antar-dataset, artefak PALSU spesifik-metode → model pertahankan "asli", hilang "palsu".
- **Kekurangan:** Tak menghubungkan generalisasi → mekanisme recall.
- **Skor:** 6/10

## Pertanyaan #7 — Validitas hasil dgn hanya 3 seed & selisih kecil

**Pertanyaan:** Dgn 3 seed & selisih kecil (std tumpang tindih), bagaimana yakin beda itu nyata bukan
kebetulan? Apa yg boleh & tidak boleh diklaim?

**Jawaban ringkas mahasiswa:** Hasil nyata: urutan spasial > hybrid > frekuensi, "MUTLAK" setelah
berbagai percobaan & sampel berbeda. Yang bisa diklaim: spasial tetap unggul pada metode implementasi
frekuensi ini; hybrid tak lebih baik karena freq setara peluang acak.

**Evaluasi**
- **Ketepatan:** Separuh. Benar: urutan konsisten & scoping "pada metode implementasi frekuensi ini"
  bagus. TAPI kata **"MUTLAK"** = overclaim serius — dgn 3 seed hanya boleh bicara DESKRIPTIF, tak
  boleh klaim signifikansi statistik tanpa uji formal.
- **Kedalaman:** Belum menangani inti pertanyaan: bedakan gap BESAR vs KECIL. Gap "kedua model >>
  frekuensi (≈acak)" itu ROBUST. Gap "spasial vs hybrid" itu KECIL & std tumpang tindih → TIDAK boleh
  diklaim beda nyata.
- **Kekurangan:** Overclaim "mutlak"; tak memisahkan klaim aman (gap besar) dari tak-aman (gap kecil).
- **Skor:** 6/10

### Pertanyaan #7a (follow-up) — Gap mana yg boleh diklaim nyata?

**Jawaban ringkas mahasiswa:** Kedua gap bisa diklaim nyata karena semua pengujian (cross & in-dataset)
memberi kesimpulan urutan yang sama. Koreksi: bukan "selalu" unggul, tapi unggul "dalam ruang lingkup
penelitian ini".

**Evaluasi**
- **Ketepatan:** Koreksi scoping "selalu"→"ruang lingkup ini" bagus. TAPI masih keliru & bertahan:
  gap spasial-vs-hybrid KECIL + std tumpang tindih + 3 seed tanpa uji formal → TIDAK boleh diklaim
  "perbedaan nyata". Konsistensi arah ≠ signifikansi.
- **Kedalaman:** Lewatkan poin kunci yg menguntungkan dia: yg dibutuhkan tesis bukan "spasial > hybrid"
  tapi "hybrid TIDAK lebih baik". Std tumpang tindih = JUSTRU bukti "tak ada peningkatan".
  Gap besar (kedua model >> frekuensi≈acak) = boleh diklaim nyata.
- **Kekurangan:** Overclaim gap kecil; belum pakai std-overlap sebagai pendukung kesimpulan.
- **Skor:** 5/10
- **Kalimat kunci yg harus dikuasai:** "Untuk perbandingan berselisih kecil & std tumpang tindih,
  dibahas DESKRIPTIF, tidak mengklaim signifikansi statistik (hanya 3 seed, tanpa uji formal)."

## Pertanyaan #8 — Fusi hybrid & fungsi SE gating

**Pertanyaan:** Bagaimana 2 cabang digabung, & apa fungsi SE gating pada fitur gabungan?

**Jawaban ringkas mahasiswa:** Digabung dgn concatenation; SE gate menekan fitur mubazir & noise tak
relevan.

**Evaluasi**
- **Ketepatan:** Concatenation benar (2×256-d → 512-d). SE gate: menangkap sisi "menekan fitur kurang
  berguna" tapi imprecise & lagi-lagi bersandar istilah "noise".
- **Kedalaman:** Belum sebut MEKANISME: gate = MLP bottleneck (Linear 512→128→ReLU→512→Sigmoid) →
  bobot per-fitur [0,1], lalu KALIKAN elemen-wise. Adaptif/input-dependent (dihitung DARI vektor
  gabungan), bukan filter tetap. Juga re-weighting (relatif menonjolkan yg berguna), bukan sekadar
  "buang noise".
- **Kekurangan:** Mekanisme squeeze-excite + sigmoid tak dijelaskan; "noise" longgar.
- **Skor:** 6/10

### Pertanyaan #8a (follow-up) — Dari mana bobot SE & kenapa Sigmoid?

**Jawaban ringkas mahasiswa:** Squeeze tekan ke 128, Excitation naikkan lagi ke 512 dgn sigmoid.
Sigmoid dipakai KARENA loss BCEWithLogitsLoss memakai sigmoid.

**Evaluasi**
- **Ketepatan:** Struktur squeeze(→128)/excite(→512) BENAR. Tapi alasan sigmoid **SALAH** — sigmoid
  di SE gate TIDAK ada hubungan dgn loss. Sigmoid dipakai agar tiap bobot ∈ [0,1] → gate multiplikatif
  per-fitur (0=buang, 1=simpan). Sigmoid loss BCE = hal terpisah (logit→probabilitas).
- **Kedalaman:** Salah konsep pada inti pertanyaan. Kenapa bukan fungsi lain: ReLU tak berbatas atas;
  tanh [-1,1] (bobot negatif membalik tanda); softmax memaksa bersaing jumlah=1. Sigmoid = gate
  independen [0,1] per fitur.
- **Kekurangan:** Konflasi sigmoid-gate dgn sigmoid-loss (miskonsepsi nyata).
- **Skor:** 5/10

## Pertanyaan #9 — Apa kontribusi kalau hipotesis tak terbukti? (kritis, penentu)

**Pertanyaan:** Hybrid tak mengalahkan spasial, freq nyaris tak berguna. Apa kontribusi ilmiahnya?

**Jawaban ringkas mahasiswa:** Fokus studi ablasi & komparatif (single XceptionNet & FFT vs hybrid).
Hipotesis gagal dibuktikan tetap berkontribusi: memperingatkan peneliti lain agar tak mengulang, dan
jadi referensi pengembangan hybrid lanjutan mengikuti kesimpulan & saran.

**Evaluasi**
- **Ketepatan:** Baik — pijakan "studi komparatif/ablasi" tepat (memindah nilai dari "menang" ke
  "mengukur"; studi komparatif tak bisa "gagal"). Nilai hasil negatif benar.
- **Kedalaman:** Cukup; kontribusi masih umum. Lebih kuat bila konkret: (1) kuantifikasi generalization
  drop spasial; (2) bukti FFT log-mag+highpass ≈ acak pd video crop+kompresi; (3) late fusion cabang
  lemah tak membantu/mengganggu + analisis akar; (4) rekomendasi (fasa/citra penuh/multi-skala).
- **Kekurangan:** Hindari kata "gagal" → "hipotesis tidak didukung". Belum sebut prasyarat validitas.
- **Skor:** 8/10

### Pertanyaan #9a (follow-up, jebakan) — "Domain freq tak berguna" vs "implementasi kami kurang"

**Jawaban ringkas mahasiswa:** Menyimpulkan implementasi frekuensi kami yg belum baik (hasil acak),
karena keterbatasan ruang lingkup & sumber daya (hanya magnitudo). Fase diarahkan ke saran.

**Evaluasi**
- **Ketepatan:** Bagus & benar. Menahan pada klaim (b) implementasi-spesifik, TIDAK naik ke (a)
  menyapu. Kerendahan hati ilmiah tepat; dikaitkan ke keterbatasan & saran. Lolos jebakan.
- **Kedalaman:** Baik. Penguat: sebut literatur (Qian, Tan) yg menunjukkan freq BISA bekerja → bukti
  hasil negatif ini spesifik implementasi, bukan sifat domain.
- **Kekurangan:** Belum pakai literatur pembanding untuk pertegas scoping.
- **Skor:** 8/10

## Pertanyaan #10 — Pertimbangan etika

**Pertanyaan:** Risiko/pertimbangan etis penelitian ini (min. 2, dari beberapa sisi, termasuk data &
penggunaan hasil).

**Jawaban ringkas mahasiswa:** (1) Detektor bisa salah klasifikasi. (2) Risiko model generatif dilatih
memakai detektor hybrid → deepfake makin sulit dideteksi (adversarial/dual-use).

**Evaluasi**
- **Ketepatan:** Dua poin sah, termasuk satu yang cukup canggih (dual-use/adversarial spt discriminator
  memperbaiki generator).
- **Kedalaman:** Poin misklasifikasi tak diurai jadi bahaya konkret (false positive = fitnah/menolak
  bukti asli; false negative = fake lolos; "liar's dividend").
- **Kekurangan:** LEWAT sisi DATA yg sudah di-hint: FF++/Celeb-DF berisi wajah orang nyata (selebriti/
  YouTube) → privasi & consent. Juga akuntabilitas penggunaan hasil (moderasi otomatis, over-trust).
- **Skor:** 6/10

### Pertanyaan #10a (follow-up) — Etika data wajah orang nyata

**Jawaban ringkas mahasiswa:** Dataset publik; FF++ ambil subjek dari YouTube (publik); Celeb-DF wajah
selebriti; keduanya "tidak merusak norma".

**Evaluasi**
- **Ketepatan:** Lemah — "publik = boleh" argumen yg paling mudah dipatahkan (publik ≠ consent).
  "Tidak merusak norma" kabur.
- **Kedalaman:** Kurang. Pembenaran benar: (1) dataset riset baku dgn LISENSI/EULA akademik yg
  dipatuhi; (2) tujuan DEFENSIF (lindungi korban); (3) tidak buat deepfake korban baru; (4) tak
  disebarluaskan. Jujur akui ada ketegangan sisa (subjek YT belum tentu consent).
- **Kekurangan:** Bersandar "publik=boleh"; lewat lisensi riset/tujuan defensif/no-new-victim.
- **Skor:** 5/10

## Pertanyaan #11 — Freeze backbone & differential learning rate

**Pertanyaan:** Kenapa backbone dibekukan di awal lalu diberi LR jauh lebih kecil dari head? Apa yg
ingin dihindari?

**Jawaban ringkas mahasiswa:** Epoch awal model masih belajar pola artefak; XceptionNet pretrained
ImageNet sudah mampu sehingga tak perlu LR tinggi agar parameternya tidak "jatuh".

**Evaluasi**
- **Ketepatan:** Menangkap inti LR-kecil (pretrained bagus → LR kecil agar tak rusak). Bagian FREEZE
  masih kabur.
- **Kedalaman:** Belum crisp: head yg random-init menghasilkan gradien awal besar/noisy; kalau backbone
  langsung dibuka, gradien itu MERUSAK fitur pretrained (catastrophic forgetting). Maka bekukan dulu
  sampai head stabil, baru unfreeze dgn LR kecil. Differential LR = jaga fitur umum, adaptasi head.
- **Kekurangan:** Tak menyebut mekanisme gradien-noisy-head / catastrophic forgetting.
- **Skor:** 6/10

## Pertanyaan #12 — Manfaat penelitian (jujur, temuan negatif)

**Pertanyaan:** Apa manfaat penelitian & untuk siapa? (jujur, tanpa membesar-besarkan; teoretis &
praktis, ke pihak konkret)

**Jawaban ringkas mahasiswa:** (1) Keamanan/forensik digital terbantu mendeteksi deepfake yg mengancam
keamanan & moral sosial. (2) Bagi penulis lain: tahu research gap, tingkatkan kualitas laporan.

**Evaluasi**
- **Ketepatan:** Poin akademik (research gap/panduan lanjutan) benar & paling jujur utk temuan negatif.
  TAPI poin praktis (forensik terbantu deteksi) OVERSTATED — persis yg saya minta dihindari, krn model
  hybrid gagal lintas-dataset (recall collapse).
- **Kedalaman:** Manfaat praktis yg JUJUR = peringatan/kehati-hatian: detektor ber-AUC tinggi in-dataset
  bisa runtuh (recall) pd manipulasi tak dikenal → jangan dipercaya penuh saat deployment. Bukan "tool
  kami menyelesaikan forensik".
- **Kekurangan:** Membesar-besarkan manfaat praktis; pihak masih generik.
- **Skor:** 6/10


---

# === PENILAIAN AKHIR MENYELURUH ===

**Mahasiswa:** Samuel Onasis (221110680) — kontribusi: dokumentasi BAB I–V, evaluasi model, uji purwarupa.

## Rekap Skor (sesi ulang, 22 butir)

| # | Topik | Skor |
|---|-------|------|
| 1 | Definisi & urgensi deepfake | 4 |
| 1a | Face2Face/FaceSwap = GAN? | 5 |
| 2 | Rumusan masalah | 6 |
| 2a | Kenapa bingkai RM2 penting | 5 |
| 3 | Teori: apa yg dilihat domain frekuensi | 6 |
| 3a | Asal checkerboard & pola periodik di FFT | 6 |
| 4 | Tahapan preprocessing | 8 |
| 4a | Kenapa high-pass filter | 7 |
| 5 | Kenapa cabang frekuensi gagal | 8 |
| 5a | (Jebakan) kenapa tetap face-crop | 8 |
| 6 | Interpretasi recall 0,07 | 8 |
| 6a | Mekanisme kenapa recall runtuh | 6 |
| 7 | Validitas hasil (3 seed) | 6 |
| 7a | Gap mana boleh diklaim nyata | 5 |
| 8 | Fusi hybrid & fungsi SE gating | 6 |
| 8a | Mekanisme bobot SE & kenapa Sigmoid | 5 |
| 9 | Kontribusi saat hipotesis tak terbukti | 8 |
| 9a | (Jebakan) domain vs implementasi | 8 |
| 10 | Pertimbangan etika | 6 |
| 10a | Etika data wajah orang nyata | 5 |
| 11 | Freeze backbone & differential LR | 6 |
| 12 | Manfaat penelitian | 6 |

**Rata-rata: 6,3 / 10** → setara **LULUS DENGAN REVISI** (simulasi).

## Kekuatan
1. **Jujur & mudah dikoreksi (coachable).** Berkali-kali mengakui kesalahan dgn elegan, tidak defensif membabi buta.
2. **Sangat kuat mempertahankan temuan negatif** (kluster skor 8: Q5, Q5a, Q9, Q9a). Paham bahwa studi komparatif tak bisa "gagal", menyamakan praproses demi komparasi terkontrol, dan membatasi klaim ke "implementasi kami" bukan "domain frekuensi umum". Ini bagian tersulit & paling sering diserang penguji — dan di sinilah dia paling kokoh.
3. **Hafal detail pipeline praproses** termasuk langkah non-obvious (high-pass filter yg memang ada di kode).

## Kelemahan Berulang (akar masalah)
1. **Kecenderungan OVERCLAIM / bahasa tidak presisi.** "mutlak", "meningkat" (RM2), manfaat praktis dibesar-besarkan, "publik = boleh". Ironisnya paling kuat saat DIPAKSA rendah hati (temuan negatif), paling lemah saat bebas menyimpulkan.
2. **Tahu APA, goyah pada MENGAPA/mekanisme.** SE-gate sigmoid (dikira terkait loss), alasan freeze backbone, mekanisme recall collapse, pola periodik→spikes di FFT. Struktur hafal, mekanisme belum.
3. **Fundamental dataset sendiri lemah.** 4 metode manipulasi FF++, definisi deepfake (bukan GAN-only), lisensi/etika dataset.
4. **Bersandar metafora longgar** — "noise filtering" utk SE gate (berulang).

## Perbaikan Prioritas Sebelum Sidang Sungguhan
1. **Fundamental dataset:** kuasai 4 metode FF++ (Deepfakes=autoencoder, Face2Face=reenactment grafika/3D, FaceSwap=swap 3D+blending, NeuralTextures=neural rendering+adversarial); komposisi & lisensi Celeb-DF; definisi deepfake yg benar (bukan hanya GAN).
2. **Bahasa statistik:** JANGAN "mutlak/signifikan" dgn 3 seed. Pisahkan gap besar (freq≈acak, boleh diklaim) vs gap kecil std-overlap (spasial vs hybrid → deskriptif; std tumpang tindih = bukti "tak ada peningkatan"). Hafal kalimat kunci di Q7a.
3. **SE gating:** squeeze→excite (MLP bottleneck)+Sigmoid → bobot per-fitur [0,1], dikalikan, adaptif. Sigmoid gate ≠ sigmoid BCE loss. Kenapa sigmoid bukan ReLU/tanh/softmax. Stop istilah "noise filtering".
4. **Etika:** lisensi/EULA riset + tujuan defensif + tanpa korban baru + liar's dividend + akui ketegangan sisa. Buang argumen "publik = boleh".
5. **RM2:** hafalkan sebagai "sejauh mana FFT MEMPERKECIL PENURUNAN lintas-dataset" (mengukur), jangan "meningkatkan performa".
6. **Kefasihan mekanisme:** pola periodik→spikes di FFT; catastrophic forgetting utk freeze; recall collapse (fake asing tak memicu sinyal→divonis asli).
7. **Manfaat:** bingkai manfaat praktis sebagai PERINGATAN (detektor 1-dataset bisa runtuh lintas-dataset), bukan alat forensik yg sudah bekerja.

