# Revisi BAB I–III Berdasarkan Hasil Tinjauan Pra Ujian Akhir

**Tanggal:** 2026-05-18
**Sumber feedback:** Pembanding 1 (nilai 70), Pembanding 2 (nilai 78)
**Sumber teks lama:** `documents/Metode Peningkatan ... _v2.md` (commit d90dbcc) — saat ini hanya ada di git history
**Sumber referensi:** `thesis_reference/INDEX.md` + Daftar Pustaka v2 (`[1]–[32]`)

---

## A. Perbandingan dua rencana revisi

`plan/lecturer-review-fixes-2026-04-19.md` dan `documentation/thesis_improvements_2026-04-25.md` pada dasarnya menangani **isu yang sama**, tetapi berbeda dalam tingkat keputusan editorial:

| Aspek | `lecturer-review-fixes` (19 Apr) | `thesis_improvements` (25 Apr) | Catatan |
|---|---|---|---|
| Rumusan masalah usulan | RM 1 = penurunan domain spasial; RM 2 = integrasi FFT; RM 3 = kontribusi tiap fitur | RM 1 = mendeteksi manipulasi yang artefak spasialnya halus; RM 2 = keterbatasan generalisasi; RM 3 = penambahan FFT untuk *robustness* | Versi 25 Apr **lebih sesuai** dengan permintaan P2 (paragraf turunan di latar belakang) dan lebih dekat dengan kerangka eksperimen ablation yang sudah ada. **Pakai versi 25 Apr.** |
| Manfaat poin 4 (kecepatan) | Diganti jadi "model sebagai dasar pengembangan forensik lanjut" | **Dihapus total** | 25 Apr lebih bersih — sejalan dengan rumusan masalah baru. |
| Manfaat poin 5 (alat andal) | Tidak dibahas eksplisit | Dilunakkan jadi "referensi metodologis" + manfaat dialamatkan ke pihak penerima | 25 Apr lebih lengkap. |
| Sitasi Celeb-DF | Belum ditentukan format | Eksplisit pakai `[35]` (Li et al. 2020) | **Masalah:** `[35]` tidak ada di Daftar Pustaka v2 (terakhir `[32]`). Wajib tambah entri baru. |
| Konsistensi BAB I ↔ BAB III ("1 arsitektur vs 3 arsitektur") | Tidak disebut | Reframe: 1 hybrid + 2 baseline untuk ablation | 25 Apr menyelesaikan kontradiksi yang dilaporkan P2. |
| BAB II — sub-bab dipangkas | Tidak ada | Eksplisit: 2.7 ringkas, 2.8 dipertimbangkan dipangkas, 2.17.1 (SGD) dipangkas, 2.5.4 ringkas | 25 Apr menanggapi catatan P2 ("cukup tuliskan yang akan diteliti"). |
| Subbab "Analisis Sistem" BAB III | Disebut | Disebut + lebih konkret (tools, hardware, orkestrasi) | Setara. |
| Augmentasi visual | Sama | Sama | Setara. |

**Kesimpulan:** Tidak ada perbedaan strategis. `thesis_improvements_2026-04-25.md` adalah **versi yang harus dipakai** — lebih lengkap, lebih sinkron dengan dua reviewer sekaligus, dan menyelesaikan kontradiksi struktur. `lecturer-review-fixes` cukup disimpan sebagai histori awal.

Satu hal yang **dua-duanya lupa eksplisit**: keduanya menyebut nomor sitasi seperti `[35]` atau `[ref]` tanpa memverifikasi bahwa nomor tersebut sudah ada di daftar pustaka v2 yang final. Lihat bagian **F** di bawah untuk verifikasi.

---

## B. BAB I — Rewrite per paragraf

> Format: **Lama** (kalimat persis dari `thesis_v2.md` baris 537–601) → **Baru** (usulan revisi) → *Catatan*.

### B.1 Latar Belakang — Paragraf 1+2 digabung (menjawab P2-LB-1)

**Lama (paragraf 1, baris 537):**
> Perkembangan teknologi kecerdasan buatan, khususnya pada bidang *Generative Adversarial Networks* (GAN), telah menghasilkan kemampuan menciptakan citra dan video sintetis yang sangat realistis. Salah satu hasil penerapannya adalah teknologi yang dikenal dengan nama *deepfake*. Teknologi ini mampu memanipulasi video atau audio untuk menampilkan adegan atau ucapan seolah-olah berasal dari orang yang sebenarnya. Meskipun tujuan awal dikembangkannya teknologi ini adalah untuk hiburan, atau penelitian, penyalahgunaan *deepfake* telah menimbulkan ancaman serius, seperti penyebaran informasi palsu (*fake news*), pelanggaran privasi, hingga memicu kerugian di tingkat individu, sosial, hingga geopolitik [1].

**Lama (paragraf 2, baris 539):**
> Di tingkat individu, *Deepfake* memiliki potensi besar untuk merusak citra, dan reputasi seseorang, terutama melalui pembuatan konten palsu yang merusak, seperti kasus *deepfake porn*. Secara global, studi menunjukkan mayoritas video *deepfake* adalah pornografi yang menargetkan perempuan, menciptakan konsekuensi serius terhadap privasi dan persepsi masyarakat [2].

**Baru (satu paragraf 5–7 kalimat):**
> Perkembangan *Generative Adversarial Networks* (GAN) telah memungkinkan terciptanya citra dan video sintetis yang sulit dibedakan dari rekaman asli, dan teknologi inilah yang melahirkan istilah *deepfake* — konten visual atau audio yang dimanipulasi sedemikian rupa sehingga menampilkan adegan atau ucapan yang tidak pernah terjadi. Meskipun awalnya dikembangkan untuk hiburan dan riset sintesis media, *deepfake* kini menjadi ancaman serius pada beberapa tingkatan: ditingkat geopolitik, ia dipakai sebagai instrumen disinformasi dan propaganda [1]; ditingkat individual, 96% video *deepfake* yang beredar global berbentuk pornografi non-konsensual yang sebagian besar menargetkan perempuan, menimbulkan kerugian reputasi, psikologis, dan hukum yang nyata [2]. Skala dan kecepatan distribusi konten ini menjadikan deteksi otomatis *deepfake* bukan sekadar tantangan riset, melainkan kebutuhan forensik digital yang mendesak.

*Catatan referensi:* [1] = Korshunov 2019 ✓, [2] = Andira & Susila 2024 ✓. Klaim 96% **wajib di-source ke [2]** (sudah konsisten). Jika klaim ingin diperkuat, tambahkan sitasi sekunder ke Sensity AI 2019 report (tidak wajib).

---

### B.2 Latar Belakang — Paragraf 3 (XceptionNet baseline) — perketat dan tambahkan klaim cross-dataset

**Lama (baris 541):** … "*XceptionNet* … menonjol karena efisiensinya dalam mengekstraksi fitur spasial tingkat tinggi menggunakan *depthwise separable convolution* [6]."

**Baru (tambahkan satu kalimat penutup; sisanya tetap):**
> *MesoNet* dirancang untuk mendeteksi artefak lokal seperti batas *blending* dan perbedaan warna pada wajah hasil manipulasi, namun memiliki keterbatasan pada citra resolusi tinggi [4]. *ResNet-50* memperkenalkan *residual learning* untuk merepresentasikan fitur spasial yang lebih dalam, dan dilaporkan mencapai akurasi >90% pada FaceForensics++ namun turun signifikan ketika diuji lintas dataset [3, 5]. *XceptionNet* (*Extreme Inception Net*) menjadi *baseline* domain spasial yang paling banyak dipakai karena *depthwise separable convolution* memberikan efisiensi komputasi tanpa mengorbankan akurasi, dan dilaporkan mencapai 99,26% AUC pada FaceForensics++ tanpa kompresi [6, 19]. **Namun, akurasi tinggi ini tidak konsisten pada pengujian lintas dataset, yang mengindikasikan ketergantungan model terhadap artefak visual khas dataset pelatihan.**

*Catatan referensi:* [3] Haq 2021 ✓, [4] Afchar (MesoNet) ✓, [5] He (ResNet) ✓, [6] Chollet (Xception) ✓, [19] Rossler (FF++) ✓. **Kalimat tambahan bold di atas menjawab P1 (kinerja XceptionNet) sekaligus P2-LB-2 (urgensi cross-dataset).**

---

### B.3 Latar Belakang — Paragraf 5 (sejumlah penelitian) — perpanjang dengan 3 sitasi (P2-LB-3)

**Lama (baris 545):**
> Untuk mengatasi keterbatasan tersebut, sejumlah penelitian telah mengusulkan pendekatan berbasis *frequency*, seperti *Frequency Domain Analysis (FDA)*, dengan metode *Fast Fourier Transform* (FFT), *Discrete Cosine Transform* (DCT), atau *Wavelet Transform*. Pendekatan ini berupaya mengekstraksi pola artefak frekuensi yang muncul akibat proses *upsampling*, *interpolation*, dan *compression* pada citra hasil sintesis [7].

**Baru (5–6 kalimat, 4 sitasi):**
> Untuk mengatasi keterbatasan tersebut, riset deteksi *deepfake* bergeser ke domain frekuensi. Pendekatan berbasis *Fast Fourier Transform* (FFT) memanfaatkan asimetri spektral pada citra GAN dan terbukti dapat membedakan citra sintetis dari citra natural meski manipulasi visualnya tidak terlihat di domain spasial [7]. Pendekatan berbasis *Discrete Cosine Transform* (DCT) bekerja pada koefisien blok dan menyingkapkan anomali pada band frekuensi menengah yang konsisten antar-arsitektur GAN [25]. Sementara itu, pembelajaran adaptif pada representasi frekuensi seperti *Frequency-aware Clues* [13] dan *Frequency-Aware Deepfake Detection* berbasis spektrum [22] meningkatkan kemampuan generalisasi terhadap teknik sintesis baru dan citra terkompresi. Konvergensi ketiga pendekatan ini menunjukkan bahwa jejak generatif paling stabil bukan pada piksel, melainkan pada distribusi spektralnya.

*Catatan referensi:* [7] Durall ✓, [13] Qian ✓, [22] Tan ✓, [25] Giudice ✓. Semua sudah ada di daftar pustaka v2.

---

### B.4 Latar Belakang — Sisipkan paragraf baru: urgensi generalisasi cross-dataset (P2-LB-4 + P1)

**Tambahkan setelah paragraf 5 baru (sebelum paragraf 7 lama):**

> Di luar laboratorium, detektor *deepfake* harus menghadapi distribusi data yang sangat berbeda dari data pelatihan: generator baru bermunculan setiap tahun, kompresi platform sosial bervariasi, dan teknik pasca-pemrosesan adversarial dipakai untuk menyamarkan jejak. Studi sistematis melaporkan penurunan AUC 10–20 poin ketika detektor berbasis CNN spasial dipindahkan dari satu dataset ke dataset lain [10, 11]. Karena itu, kemampuan **generalisasi lintas dataset** — bukan akurasi *in-domain* — adalah metrik yang paling relevan untuk menilai kelayakan deteksi *deepfake* di dunia nyata, dan menjadi fokus utama penelitian ini.

*Catatan referensi:* [10] Rana et al. 2022 (systematic review, eksplisit melaporkan drop cross-dataset) ✓, [11] Rao & Uehara 2025 (chronological review) ✓. **Klaim "10–20 poin AUC drop" perlu dicocokkan dengan angka di paper [10] atau [11]; jika tidak presisi, ganti jadi "penurunan AUC yang signifikan" tanpa angka.**

---

### B.5 Latar Belakang — Paragraf 7 & 8 (kontradiksi) — reframe (P2-LB-LB-4)

**Lama paragraf 7 (baris 549):**
> Beberapa penelitian menunjukkan bahwa gabungan antara dua domain ini, dapat meningkatkan kemampuan generalisasi model terhadap *deepfake* lawas maupun baru, sekaligus menekan *overfitting* terhadap dataset tertentu [10, 11, 12]. …

**Lama paragraf 8 (baris 551):**
> Berdasarkan uraian tersebut, terdapat *research gap* dalam penelitian deteksi *deepfake*, yaitu belum adanya pendekatan yang secara terpadu mengombinasikan analisis domain spasial dan domain frekuensi dalam satu arsitektur yang dioptimalkan untuk meningkatkan kemampuan generalisasi lintas *dataset*. …

**Baru paragraf 7 (reframe potensi, bukan absen):**
> Studi awal hibridisasi domain spasial dan frekuensi telah menunjukkan **potensi** peningkatan generalisasi. *SpecXNet* menggabungkan cabang spasial *XceptionNet* dengan cabang frekuensi untuk meningkatkan ketahanan deteksi terhadap berbagai manipulasi [9]; *FSBI* memanfaatkan *self-blended image* yang ditingkatkan frekuensi untuk memperkuat generalisasi lintas dataset [18]; *Frequency-Domain Masking* mengintegrasikan informasi spasial dan frekuensi melalui mekanisme adaptif [20]. Studi-studi ini berhasil membuktikan bahwa fusi dua domain bermanfaat, tetapi sebagian besar masih dioptimalkan untuk performa *in-domain* pada FaceForensics++, dan belum mengevaluasi secara sistematis fusi *late* + *gating* sebagai mekanisme spesifik untuk meningkatkan robustness lintas dataset.

**Baru paragraf 8 (gap spesifik, bukan absen):**
> Penelitian ini mengisi celah tersebut dengan mengusulkan **arsitektur hybrid XceptionNet–FFT dengan *late fusion* dan *Squeeze-and-Excitation gating*** yang dioptimalkan untuk generalisasi lintas dataset. Berbeda dari pekerjaan sebelumnya yang berfokus pada *in-domain accuracy*, penelitian ini secara eksplisit mengevaluasi skenario FFPP→CDF dan CDF→FFPP untuk mengukur seberapa besar fitur frekuensi mampu menahan *performance drop* yang lazim terjadi pada detektor spasial murni.

*Catatan referensi:* [9] Alam SpecXNet ✓, [18] Hasanaath FSBI ✓, [20] Luo ✓. **Menghapus klaim "belum ada hybrid" yang kontradiktif.**

---

### B.6 Rumusan Masalah — Rewrite (P1-RM, P2-RM-1, P2-RM-2, P2-RM-3)

**Lama:**
1. Bagaimana mengembangkan metode deteksi *deepfake* yang lebih akurat, dan *robust* dengan menggabungkan arsitektur *XceptionNet* berbasis domain spasial, dan analisis frekuensi FFT untuk mendeteksi manipulasi **citra atau video sintetis**?
2. Bagaimana arsitektur *XceptionNet* dapat dimodifikasi dan diperluas melalui integrasi modul FDA untuk secara efektif mengekstrak dan menggabungkan fitur spasial *fine-grained* pada artefak *high-band frequency*?
3. Seberapa besar peningkatan kinerja, khususnya dalam hal *cross-dataset generalization capability* …

**Baru (3 pertanyaan berbentuk masalah, bukan solusi):**
1. Sejauh mana detektor *deepfake* berbasis domain spasial murni (*XceptionNet*) mengalami penurunan performa ketika diuji pada **video sintetis** dari dataset yang berbeda dengan data pelatihannya?
2. Sejauh mana penambahan analisis domain frekuensi (FFT) ke dalam arsitektur *XceptionNet* dapat memperkecil penurunan tersebut?
3. Seberapa besar kontribusi masing-masing komponen (fitur spasial vs fitur frekuensi) terhadap akurasi, presisi, *recall*, dan AUC pada pengujian *in-dataset* maupun *cross-dataset*?

*Catatan:* setiap RM mempunyai paragraf turunan di latar belakang baru: RM1 ↔ B.2 + B.4; RM2 ↔ B.5; RM3 ↔ B.5 (kalimat penutup tentang ablation).

---

### B.7 Tujuan — Rewrite (P1-TJ)

**Lama:** "Merancang dan mengimplementasi model *hybrid* … / Memperluas dan memodifikasi … / Menganalisis dan membandingkan kinerja …" — terkesan paraphrase RM.

**Baru (deliverable konkret, bukan paraphrase RM):**
1. Mengimplementasikan arsitektur hybrid *XceptionNet*–FFT dengan *late fusion* dan *SE gating* untuk deteksi *deepfake* tingkat *frame* video.
2. Melakukan *ablation study* (spasial-saja vs frekuensi-saja vs hybrid) untuk memisahkan kontribusi masing-masing domain.
3. Mengevaluasi generalisasi model pada skenario *in-dataset* (FFPP→FFPP, CDF→CDF) dan *cross-dataset* (FFPP→CDF, CDF→FFPP) menggunakan akurasi, presisi, *recall*, dan AUC.

---

### B.8 Manfaat — Hapus poin 4, lunakkan poin 5 (P2-MF-1, P2-MF-2)

**Lama poin 4:** "Manfaat Operasional: Menghasilkan model yang efisien dengan *XceptionNet*, dan **kecepatan serta ketepatan inferensi dari FFT**." → **HAPUS** (kontradiksi dengan Ruang Lingkup 4).

**Lama poin 5:** "Manfaat Praktis: Menyediakan **alat forensik digital yang lebih andal dan akurat**. Penegak hukum dan badan pengawas media dapat menggunakan model ini …"

**Baru (turunkan jadi 4 poin, dilunakkan):**
1. Manfaat Akademik: Memberikan kontribusi ilmiah berupa evaluasi sistematis terhadap kontribusi fitur frekuensi dalam arsitektur hybrid deteksi *deepfake*.
2. Manfaat Teknologi: Menyediakan rancangan arsitektur dan pipeline reproduktif yang dapat dijadikan acuan oleh peneliti lain yang mengembangkan detektor hibrida domain spasial–frekuensi.
3. Manfaat Sosial: Mendukung upaya mitigasi penyalahgunaan *deepfake* (misinformasi, *deepfake porn*, propaganda politik) dengan menyediakan dasar metodologis yang dapat dievaluasi oleh lembaga forensik digital.
4. Manfaat Praktis: Memberikan baseline cross-dataset yang dapat dipakai pengembang sistem verifikasi konten sebagai pembanding untuk arsitektur deteksi lain.

---

### B.9 Ruang Lingkup — Tambahkan kriteria dataset + sitasi link (P1-RL, P2-RL)

**Tambahkan ke Ruang Lingkup poin 1:**

> 1. Cakupan Data: Penelitian menggunakan **video** dari dua dataset publik yang kemudian diekstraksi menjadi **frame citra** untuk diproses model:
>    a. **FaceForensics++** [19] (repositori: `https://github.com/ondyari/FaceForensics`), kompresi *high-quality* (c23), dengan empat metode manipulasi (*Deepfakes, Face2Face, FaceSwap, NeuralTextures*).
>    b. **Celeb-DF v2** [33] (repositori: `https://github.com/yuezunli/celeb-deepfakeforensics`), kategori *celebrity face-swap*.
>    Pengambilan sampel dilakukan dengan rasio 50:50 antara kelas asli dan kelas manipulasi, dan pemisahan *train/val/test* dilakukan pada level video untuk menghindari kebocoran *frame*. Penelitian tidak mencakup deteksi manipulasi audio atau *text-based deepfake*.

**Tabel total dataset (sisipkan setelah daftar Ruang Lingkup):**

| Dataset | Real videos | Fake videos | Total frame (~) | Sumber |
|---|---|---|---|---|
| FaceForensics++ (n=1000, c23) | 500 | 500 | ~50.000 | [19] |
| Celeb-DF v2 (n=750) | 375 | 375 | ~37.500 | [33] (baru) |

*Catatan referensi:* **[33] Li et al. 2020 "Celeb-DF: A Large-scale Challenging Dataset for DeepFake Forensics" CVPR — BELUM ADA di Daftar Pustaka v2** (terakhir [32]). Wajib ditambahkan. Atau jika nomor lain dipakai, sesuaikan.

---

## C. BAB II — Rewrite paragraf bermasalah (sentence-level)

### C.1 Subbab 2.3.4 — Pendekatan Hybrid: tambah sitasi pada "dua strategi utama" (P2-2.3.4)

Tambahkan sitasi `[9, 18, 30]` segera setelah frasa "dua strategi utama" dan tulis ulang paragraf pembuka strategi:

> Integrasi domain spasial dan domain frekuensi pada satu arsitektur deteksi *deepfake* umumnya mengikuti dua strategi utama, yaitu *early fusion* dan *late fusion* [9, 18, 30]. Pada *early fusion*, representasi frekuensi (misalnya peta magnitude FFT) digabungkan dengan citra RGB sebagai kanal tambahan sebelum masuk ke *backbone* sehingga jaringan mempelajari fitur dari kedua domain secara bersamaan; pendekatan ini dianut antara lain oleh *Frequency-aware Clues* yang menyisipkan jalur frekuensi langsung pada tahap *input* [30]. Pada *late fusion*, masing-masing domain memiliki *backbone* sendiri yang fitur outputnya digabungkan pada tahap klasifikasi; pendekatan ini diadopsi oleh *SpecXNet* [9] dan *FSBI* [18], dan memberikan fleksibilitas dalam menambah modul fusi adaptif seperti *channel attention* atau *gating*.

*Catatan referensi:* [9] Alam ✓, [18] Hasanaath ✓, [30] Stack Overflow — **salah!** sebaiknya pakai [13] Qian "Thinking in Frequency" ✓ untuk strategi *early-style*.

---

### C.2 Subbab 2.9.4 — Depthwise Separable Convolution (P2-2.9.4)

Pastikan sitasi `[6]` (Chollet) muncul tepat pada **definisi** *depthwise separable convolution* dan pada persamaan (2.5)/(2.6):

> *Depthwise separable convolution* adalah dekomposisi konvolusi standar menjadi dua tahap berurutan — *depthwise convolution* yang mengoperasikan kernel terpisah pada tiap kanal *input*, dan *pointwise convolution* (1×1) yang menggabungkan kanal — yang diformulasikan oleh Chollet [6] sebagai dasar arsitektur *Xception*. Dekomposisi ini secara signifikan menurunkan kompleksitas komputasi dari `K² × M × N` (standar) menjadi `K² × M + M × N` (DSC), seperti yang dijelaskan pada persamaan (2.5)–(2.9).

Sitasi [6] sudah benar — Chollet 2017.

---

### C.3 Subbab 2.10.1 — XceptionNet (P2-2.10.1)

**Tindakan:** sisipkan gambar arsitektur XceptionNet (Entry flow → Middle flow × 8 → Exit flow) dari Chollet [6]. Caption: "Gambar 2.X Arsitektur XceptionNet [6]".

**Rewrite paragraf pembuka 2.10.1** (lebih faktual, bukan kutipan):

**Lama (baris 1193 lingkungan):** "Penelitian oleh *Rössler et al.* menunjukkan bahwa *XceptionNet* mencapai akurasi deteksi hingga 99,26% pada data mentah …"

**Baru (faktual, bukan "menurut"):**
> Pada *benchmark* FaceForensics++ tanpa kompresi, *XceptionNet* mencapai 99,26% AUC dan melampaui *ResNet-50* maupun *MesoNet*; namun akurasi turun ke 81,00% pada kompresi berat (c40), menunjukkan ketergantungan model pada artefak visual berfrekuensi tinggi yang rusak oleh kompresi [19, 3].

---

### C.4 Subbab 2.11.1 & 2.11.2 — Squeeze-and-Excitation (P2-2.11)

**Tambahkan referensi baru** ke daftar pustaka: **Hu, J., Shen, L., & Sun, G. (2018). Squeeze-and-Excitation Networks. CVPR.** — diusulkan sebagai **[34]**.

Sisipkan sitasi `[34]` pada definisi *channel attention*, rumus *squeeze* + *excitation*, dan deskripsi blok SE.

---

### C.5 Subbab 2.20.1 — rename (P2-2.20.1)

`Mengapa Cross-GAN Sulit` → `Faktor Penyebab Kesulitan Generalisasi Cross-GAN`.

---

### C.6 Ubah pola "Menurut / X et al. menunjukkan" → kalimat faktual (permintaan utama Anda)

Identifikasi terdapat **17+ kalimat** dengan pola `*X et al*. menunjukkan/menemukan/mengusulkan …`. Pola ini terbaca seperti rangkuman kutipan, bukan pembuktian. Rumus penggantinya:

> **Lama:** *X et al.* menunjukkan bahwa *Y* [N].
> **Baru:** *Y* — secara teknis disebabkan oleh *mekanisme M*, dengan bukti pada *dataset/benchmark Z* [N].

Contoh konkret yang harus diubah:

| Lokasi (baris) | Lama | Baru |
|---|---|---|
| 547 | "*Durall et al*. menunjukkan bahwa sebagian besar *deepfake* generator gagal dalam mereplikasi spektrum frekuensi alami citra manusia …" | "Sebagian besar generator *deepfake* gagal mereplikasi distribusi spektral citra natural pada frekuensi tinggi: pengukuran *azimuthal frequency profile* memperlihatkan kelebihan energi konsisten pada *frame* sintetis di lima arsitektur GAN yang diuji [7]." |
| 793 | "Penelitian *Durall et al.* menemukan bahwa jaringan GAN gagal mereproduksi distribusi spektral …" | "Jaringan GAN dengan operasi *upsampling* transposed-convolution secara sistematis menghasilkan distribusi spektral yang lebih landai (*spectral fall-off*) dibanding citra natural, sehingga rasio energi *high-band* terhadap *low-band* dapat dijadikan ciri pembeda [7]." |
| 837 | "*Durall et al*. menunjukkan bahwa operasi *up-convolution* sering menghasilkan pola spektral …" | "Operasi *up-convolution* dengan *stride* > 1 menghasilkan pola periodik di domain frekuensi karena *kernel overlap* yang tidak seragam — fenomena yang dikenal sebagai *checkerboard artifact* [7, 16]." |
| 1007 | "Menurut *Chadha et al*, istilah *deepfake* berasal dari …" | "Istilah *deepfake* terbentuk dari gabungan *deep learning* dan *fake*, merujuk pada konten visual atau audio yang dimodifikasi dengan jaringan saraf dalam hingga menyerupai rekaman asli [14]." |
| 1193 | "Penelitian oleh *Rössler et al.* menunjukkan bahwa *XceptionNet* mencapai akurasi …" | "Pada FaceForensics++ *raw*, XceptionNet mencapai 99,26% AUC; pada c40 turun ke 81,00%, menunjukkan dependensi pada artefak *high-frequency* yang rusak oleh kompresi [19, 3]." |
| 1255 | "*Durall et al.* menunjukkan bahwa citra GAN menghasilkan pola energi frekuensi tinggi yang berlebihan …" | "Pengukuran energi spektral azimuth pada citra GAN menunjukkan kelebihan energi pada band frekuensi tinggi dibanding citra natural, beserta penguatan harmonik akibat *upsampling* yang tidak ideal [7]." |
| 1341 | "Studi oleh Durall et al. menunjukkan bahwa model GAN meninggalkan pola *high-frequency artifacts* …" | "Model GAN meninggalkan pola *high-frequency artifacts* yang konsisten lintas arsitektur, terutama akibat operasi *upsampling* dan ketidakseimbangan kernel konvolusi [7], dan distribusi frekuensi yang berbeda secara signifikan dari citra asli menjadi dasar metode deteksi domain frekuensi [8]." |
| 1347 | "Studi oleh Sabir et al. menunjukkan bahwa *deepfake* sering menampilkan pola-pola tidak stabil …" | "Manipulasi *frame-by-frame* tanpa konsistensi temporal menghasilkan *jittering* dan *flickering* yang dapat dideteksi dengan analisis spasial-frekuensi per-*frame* [35]." (sitasi Sabir perlu diverifikasi — di v2.md disitasi `[37]` namun daftar pustaka v2 berhenti di [32]; **wajib cek**) |
| 1443 | "Penelitian *Durall et al*. menunjukkan bahwa citra sintetis memiliki distribusi frekuensi global yang berbeda secara konsisten …" → diperkuat *Qian et al.* … | "Distribusi frekuensi global citra sintetis berbeda secara konsisten dari citra natural [7], dan generator *deepfake* gagal mereplikasi *natural image statistics* pada frekuensi tinggi karena bias *upsampling* [13]." |

**Pola umum:**
- Hapus subjek "*X et al*. menunjukkan/menemukan" — pindahkan klaim faktual menjadi kalimat utama.
- Tambahkan mekanisme teknis (mengapa fenomena itu terjadi) di antara klaim dan sitasi.
- Pertahankan sitasi `[N]` di akhir kalimat untuk attribution.

---

## D. BAB III — Rewrite/tambahan paragraf

### D.1 Subbab 3.2 — Tambahkan tabel total dataset (P2-BAB3-1)

Sisipkan **sebelum** Tabel 3.1 (Variabel Penelitian) tabel berikut dengan caption "Tabel 3.X Komposisi total *dataset* yang digunakan":

| Dataset | Versi | Real videos | Fake videos | Total videos | Frame rate ekstraksi | Total frame (~) | Sumber |
|---|---|---|---|---|---|---|---|
| FaceForensics++ | c23 (HQ) | 500 | 500 (125 per metode × 4 metode) | 1.000 | 5 fps, max 50 *frame*/video | 50.000 | [19] |
| Celeb-DF | v2 | 375 | 375 | 750 | 5 fps, max 50 *frame*/video | 37.500 | [33] |

---

### D.2 Subbab 3.3.1 — Ekstraksi Frame (P1-BAB3 detail algoritma)

**Tambahkan pseudocode setelah paragraf narasi yang sudah ada:**

```
input  : path_video, target_fps = 5, max_frame = 50
output : frame yang tersimpan sebagai .jpg

1. buka video dengan OpenCV → ambil native_fps
2. interval ← round(native_fps / target_fps)
3. frame_idx ← 0, saved ← 0
4. selama saved < max_frame:
       baca frame ke-frame_idx
       jika gagal → break
       jika frame_idx mod interval == 0:
           tulis frame ke output_dir
           saved ← saved + 1
       frame_idx ← frame_idx + 1
5. tutup video
```

**Tambahkan justifikasi:**
> Pemilihan 5 fps dan maksimum 50 *frame*/video merupakan kompromi antara cakupan temporal dan ukuran *dataset*. Pada 30 fps native, 5 fps memberikan satu sampel setiap 200 ms — cukup untuk menangkap variasi ekspresi tanpa redundansi *frame*. Batas 50 *frame*/video membatasi total *frame* FFPP n=1000 ke ~50.000, ukuran yang dapat dilatih pada satu sesi Colab Pro tanpa mengorbankan keberagaman video.

---

### D.3 Subbab 3.4 — Reframe "3 arsitektur model" (P2-3.4)

**Lama:** "Penelitian merancang dan evaluasi 3 arsitektur model."

**Baru:**
> Penelitian ini mengusulkan **satu arsitektur utama**, yaitu *HybridTwoBranch* (subbab 3.4.3), sebagai kontribusi. Sebagai pembanding (*baseline*) dalam *ablation study*, dirancang juga dua model satu-domain: *XceptionNet* spasial-saja (subbab 3.4.1) dan *FreqCNN* frekuensi-saja (subbab 3.4.2). Tujuan *baseline* ini bukan kontribusi tersendiri, melainkan untuk memisahkan kontribusi masing-masing domain terhadap performa akhir model hybrid.

---

### D.4 Subbab 3.4.3 — Pindahkan Gambar 3.8 (P2-3.4.3)

Pindahkan Gambar 3.8 (diagram HybridTwoBranch) dari akhir 3.4.4 ke **awal** subbab 3.4.3, sebelum 3.4.3.1.

---

### D.5 Subbab 3.3.3 — Augmentasi visual (P2-augmentasi)

Tambahkan dua *figure*:

- **Gambar 3.X**: grid 5 kolom × 2 baris menunjukkan output dari masing-masing transformasi (Resize → RandomResizedCrop → ColorJitter → HorizontalFlip → RandomErasing).
- **Gambar 3.Y**: pasangan citra FFT — kiri tanpa augmentasi, kanan dengan Gaussian noise injection + spectral band masking.

---

### D.6 Subbab BARU 3.8 — Analisis Sistem (P1-BAB3 sistem)

Tambahkan subbab akhir BAB III:

> ### 3.8 Analisis Sistem
>
> Implementasi penelitian ini menggunakan perangkat lunak dan perangkat keras berikut:
>
> 1. **Bahasa & framework**: Python 3.9, PyTorch (≥2.0), `timm` untuk *XceptionNet* yang sudah *pretrained* pada *ImageNet*.
> 2. **Library pendukung**: OpenCV (I/O video), NumPy (perhitungan FFT), scikit-learn (*train/val/test split*), pandas (*manifest*), matplotlib (visualisasi).
> 3. **Hardware**: GPU NVIDIA dengan dukungan CUDA dan *Automatic Mixed Precision* (AMP)/TF32 untuk arsitektur Ampere ke atas; pengembangan dilakukan pada Google Colab Pro (T4/V100); *fallback* CPU disediakan untuk eksperimen kecil.
> 4. **Orkestrasi pipeline**: skrip terpadu `run_pipeline.py` yang menjalankan ekstraksi *frame* (`extract_frames.py`), pembangunan *split* (`build_splits.py`), *cache* FFT (`compute_fft_cache.py`), pelatihan (`train.py`), dan evaluasi (`eval.py`).
> 5. **Output**: *checkpoint* terbaik (`best.pt`) dipilih berdasarkan AUC validasi tertinggi; tabel hasil disimpan sebagai `Table1_in_dataset.csv`, `Table2_cross_dataset.csv`, `Table3_generalization_drop.csv` di direktori `outputs/tables/`.

---

## E. Verifikasi sitasi vs Daftar Pustaka v2

| Sitasi yang dirujuk plan/dokumen | Nomor di Daftar Pustaka v2 | Status |
|---|---|---|
| Korshunov 2019 | [1] | ✓ ada |
| Andira & Susila 2024 | [2] | ✓ ada |
| Haq 2021 (Xception+ResNet) | [3] | ✓ ada |
| Afchar (MesoNet) | [4] | ✓ ada |
| He (ResNet) | [5] | ✓ ada |
| Chollet (Xception) | [6] | ✓ ada |
| Durall (Watch your Up-Convolution) | [7] | ✓ ada |
| Zhang (GAN artifacts) | [8] | ✓ ada |
| Alam (SpecXNet) | [9] | ✓ ada |
| Rana (Systematic Review) | [10] | ✓ ada |
| Rao (Chronological Review) | [11] | ✓ ada |
| Kim (Beyond Spatial Frequency) | [12] | ✓ ada |
| Qian (Thinking in Frequency) | [13] | ✓ ada |
| Chadha (Overview) | [14] | ✓ ada |
| Aduwala | [15] | ✓ ada |
| Odena (Checkerboard) | [16] | ✓ ada |
| Dai (Affinity-aware upsampling) | [17] | ✓ ada |
| Hasanaath (FSBI) | [18] | ✓ ada |
| Rossler (FF++) | [19] | ✓ ada |
| Luo (Frequency-Domain Masking) | [20] | ✓ ada |
| Wikimedia (2D Fourier) | [21] | ✓ ada |
| Tan (Frequency-Aware) | [22] | ✓ ada |
| Karras (ProGAN) | [23] | ✓ ada |
| Mejri (High-Frequency) | [24] | ✓ ada |
| Giudice (DCT anomalies) | [25] | ✓ ada |
| Nguyen (Spatio-temporal) | [26] | ✓ ada |
| Guera (RNN) | [27] | ✓ ada |
| Gonzalez & Woods (DIP) | [28] | ✓ ada |
| Oppenheim (DSP) | [29] | ✓ ada |
| Stack Overflow (FFT image) | [30] | ✓ ada (tetapi sumber lemah — ganti dengan Gonzalez/Easton jika memungkinkan) |
| Easton (Fundamentals) | [31] | ✓ ada |
| LeCun (Deep Learning) | [32] | ✓ ada |
| **Li et al. 2020 (Celeb-DF)** | **Tidak ada** | **WAJIB TAMBAH** sebagai [33] |
| **Hu et al. 2018 (SE-Net)** | **Tidak ada** | **WAJIB TAMBAH** sebagai [34] |
| Sabir 2019 | Tidak ada (terkutip di baris 1347 sebagai [37]) | **WAJIB CEK** — nomor [37] tidak ada di daftar v2. Tambahkan atau hapus klaim. |

**Catatan tentang [33] Celeb-DF:**
> Y. Li, X. Yang, P. Sun, H. Qi, dan S. Lyu, "Celeb-DF: A Large-Scale Challenging Dataset for DeepFake Forensics," in *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2020, hlm. 3207–3216. doi: 10.1109/CVPR42600.2020.00327.

**Catatan tentang [34] SE-Net:**
> J. Hu, L. Shen, dan G. Sun, "Squeeze-and-Excitation Networks," in *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018, hlm. 7132–7141. doi: 10.1109/CVPR.2018.00745.

---

## F. Ringkasan eksekusi

1. **Mulai dari BAB I.** Apply rewrite B.1–B.9 di atas ke dokumen sumber (Google Docs / `.docx`).
2. **Tambah dua entri** Daftar Pustaka ([33] Celeb-DF, [34] SE-Net) sebelum memakai nomor itu di tubuh dokumen.
3. **BAB II:** apply C.1–C.6. Untuk C.6 (penghilangan pola "X et al. menunjukkan") — gunakan tabel di C.6 sebagai *find-and-replace* checklist.
4. **BAB III:** apply D.1–D.6.
5. **Setelah selesai**: re-render PDF dan cross-check checklist di `documentation/thesis_improvements_2026-04-25.md` baris 215–229.
6. **Catatan**: dokumen sumber BAB I/II ada di Google Docs / `.docx`, bukan di markdown. Markdown v2 terakhir di commit `d90dbcc`. Setelah revisi, pertimbangkan re-konversi ke markdown agar perubahan terlacak di git.

---

**Akhir dokumen.**
