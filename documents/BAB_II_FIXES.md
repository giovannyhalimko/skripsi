# BAB II — Perbaikan yang Perlu Dilakukan di Word

Berikut daftar perbaikan BAB II berdasarkan cross-check dengan kode implementasi aktual.

---

## 1. Section 2.16.2 & 2.16.3 — Adam → AdamW (CRITICAL)

**Lokasi:** Halaman 45–46, Section 2.16.2 dan 2.16.3

**Masalah:** BAB II hanya menjelaskan Adam standar. Kode menggunakan **AdamW** (decoupled weight decay). Judul dan beberapa poin masih menyebut "Adam" alih-alih "AdamW".

**Perbaikan — ganti keseluruhan 2.16.2 dan 2.16.3 dengan teks berikut:**

---

### 2.16.2 AdamW (*Decoupled Weight Decay Regularization*)

Adam (*Adaptive Moment Estimation*) merupakan metode optimasi yang menggabungkan konsep *momentum* dan *adaptive learning rate* dari RMSprop. Adam menghitung estimasi momen pertama (rata-rata gradien) dan momen kedua (rata-rata kuadrat gradien) untuk setiap parameter, kemudian menggunakan estimasi tersebut untuk menyesuaikan langkah pembaruan secara individual [41].

Persamaan pembaruan Adam adalah:

Estimasi momen pertama:

$$m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t \tag{2.15}$$

Estimasi momen kedua:

$$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \tag{2.16}$$

Koreksi bias:

$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t} \tag{2.17}$$

$$\hat{v}_t = \frac{v_t}{1 - \beta_2^t} \tag{2.18}$$

Pembaruan parameter:

$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t \tag{2.19}$$

di mana $\beta_1$ dan $\beta_2$ adalah koefisien peluruhan momen (umumnya $\beta_1 = 0{,}9$, $\beta_2 = 0{,}999$), dan $\epsilon$ adalah konstanta stabilitas numerik [41].

AdamW merupakan varian dari Adam yang diperkenalkan oleh Loshchilov dan Hutter [42] dengan mekanisme *decoupled weight decay*. Berbeda dengan implementasi *weight decay* pada Adam standar yang menambahkan regularisasi L2 ke gradien sebelum penskalaan adaptif, AdamW menerapkan *weight decay* secara langsung pada bobot setelah langkah pembaruan Adam. Perbedaan ini memastikan bahwa efek regularisasi konsisten untuk semua parameter, tidak bergantung pada *learning rate* adaptif masing-masing parameter. Dalam skenario *transfer learning*, di mana parameter *pretrained* dan parameter baru memiliki skala gradien yang sangat berbeda, konsistensi ini sangat penting untuk menjaga stabilitas pelatihan.

### 2.16.3 Keunggulan AdamW untuk Deteksi Deepfake

AdamW dipilih dalam penelitian ini sebagai metode optimasi utama karena beberapa alasan:

1. *Adaptive learning rate* per parameter memungkinkan konvergensi yang lebih stabil pada arsitektur *hybrid* yang memiliki parameter dengan skala gradien yang berbeda antara *branch* spasial dan frekuensi.
2. Koreksi bias pada momen pertama dan kedua membuat AdamW efektif bahkan pada tahap awal pelatihan ketika estimasi momen masih tidak akurat.
3. AdamW mengimplementasikan *decoupled weight decay* secara *native*, sehingga regularisasi lebih konsisten dan efektif pada arsitektur *hybrid* dengan parameter *pretrained* dan baru.
4. Dalam praktik pelatihan model deteksi *deepfake*, AdamW telah terbukti menghasilkan konvergensi yang cepat dan stabil pada berbagai arsitektur CNN, termasuk XceptionNet [19].

---

**Referensi yang perlu ditambahkan ke Daftar Pustaka:**
- [42] I. Loshchilov dan F. Hutter, Decoupled Weight Decay Regularization, International Conference on Learning Representations (ICLR), 2019.

---

## 3. Section 2.16 — Intro Paragraph Missing (LOW)

**Lokasi:** Halaman 44, sebelum Section 2.16.1 "Stochastic Gradient Descent dan Perkembangannya"

**Tambahkan paragraf intro:**

> Optimasi model merupakan proses penyesuaian parameter jaringan saraf untuk meminimalkan fungsi *loss* selama pelatihan. Pemilihan metode optimasi yang tepat sangat memengaruhi kecepatan konvergensi, stabilitas pelatihan, dan kualitas model akhir. Pada penelitian deteksi *deepfake*, tantangan optimasi menjadi lebih kompleks ketika arsitektur *hybrid* menggabungkan komponen *pretrained* dengan komponen yang dilatih dari awal, karena skala gradien antar komponen dapat sangat berbeda. Bagian ini membahas perkembangan metode optimasi dari *Stochastic Gradient Descent* (SGD) hingga AdamW yang digunakan dalam penelitian ini, serta fungsi *loss* yang diterapkan untuk tugas klasifikasi biner.

---

## 4. Section 2.3 — Intro Paragraph Missing (LOW)

**Lokasi:** Halaman 9, sebelum Section 2.3.1

**Tambahkan paragraf intro:**

> Pendekatan deteksi *deepfake* dapat diklasifikasikan berdasarkan domain analisis yang digunakan. Secara umum, terdapat dua pendekatan utama: deteksi berbasis domain spasial yang menganalisis fitur visual langsung dari citra, dan deteksi berbasis domain frekuensi yang menganalisis representasi spektral untuk mengidentifikasi artefak yang tidak terlihat secara kasat mata. Beberapa penelitian terkini juga mengeksplorasi pendekatan *hybrid* yang menggabungkan kedua domain untuk meningkatkan akurasi dan kemampuan generalisasi. Bagian berikut menguraikan masing-masing pendekatan beserta perbandingannya.

---

## 4. Section 2.4 — Intro Paragraph Missing (LOW)

**Lokasi:** Halaman 14, sebelum Section 2.4.1

**Tambahkan paragraf intro:**

> Analisis domain frekuensi (*Frequency Domain Analysis* / FDA) merupakan pendekatan yang mengubah representasi citra dari domain spasial ke domain frekuensi untuk mengungkap pola-pola yang tidak terdeteksi oleh analisis visual langsung. Dalam konteks deteksi *deepfake*, FDA sangat relevan karena proses sintesis generatif menghasilkan artefak spektral yang khas, seperti distorsi distribusi frekuensi dan puncak periodik pada komponen frekuensi tinggi. Bagian berikut menjelaskan konsep dasar domain frekuensi, transformasi Fourier, dan relevansinya terhadap deteksi *deepfake*.

---

## 5. Section 2.15 — Intro Paragraph Missing (LOW)

**Lokasi:** Halaman 40, sebelum Section 2.15.1 "Tahapan dan Alur Preprocessing"

**Tambahkan paragraf intro:**

> *Preprocessing* merupakan tahapan persiapan data yang dilakukan sebelum data digunakan untuk melatih model *deep learning*. Dalam konteks deteksi *deepfake*, *preprocessing* mencakup serangkaian transformasi yang mengonversi data video mentah menjadi representasi yang terstandar dan siap diproses oleh jaringan saraf. Tahapan ini meliputi ekstraksi *frame* dari video, normalisasi citra, konversi ke domain frekuensi melalui FFT, serta augmentasi data untuk meningkatkan keberagaman set pelatihan. Kualitas *preprocessing* sangat memengaruhi performa model akhir, karena representasi data yang tidak tepat dapat menyebabkan model mempelajari artefak *preprocessing* alih-alih pola manipulasi *deepfake* yang sesungguhnya.

---

## 6. NEW Section 2.11 — *Squeeze-and-Excitation Networks* (HIGH)

**Lokasi:** Setelah Section 2.10 (XceptionNet), sebelum 2.11 (FaceForensics) yang saat ini ada di Word.

**Dampak penomoran:** Section 2.11 FaceForensics → 2.12, Celeb-DF 2.12 → 2.13, dst. hingga 2.20 → 2.21. Semua cross-reference internal perlu disesuaikan.

**Tambahkan section baru berikut:**

---

### 2.11 *Squeeze-and-Excitation Networks*

Dalam arsitektur *deep learning* modern, tidak semua fitur yang diekstraksi oleh lapisan konvolusional memiliki tingkat kepentingan yang sama untuk tugas klasifikasi tertentu. Beberapa kanal fitur mungkin mengandung informasi yang sangat diskriminatif, sementara kanal lainnya mengandung *noise* atau informasi yang tidak relevan. *Squeeze-and-Excitation Networks* (SE-Net) yang diperkenalkan oleh Hu *et al.* [42] mengatasi permasalahan ini melalui mekanisme *channel attention* yang memungkinkan jaringan untuk secara adaptif mempelajari bobot kepentingan setiap kanal fitur.

#### 2.11.1 Konsep *Channel Attention*

*Channel attention* merupakan mekanisme yang memberikan bobot berbeda pada setiap kanal fitur berdasarkan konten input. Berbeda dengan konvolusi standar yang memperlakukan semua kanal secara seragam, *channel attention* memungkinkan jaringan untuk secara selektif menekan (*suppress*) kanal yang tidak informatif dan memperkuat (*enhance*) kanal yang diskriminatif. Pendekatan ini terinspirasi dari mekanisme atensi selektif pada sistem visual manusia yang secara alami memfokuskan perhatian pada informasi yang paling relevan.

#### 2.11.2 Arsitektur SE *Block*

SE *block* terdiri dari tiga operasi berurutan yang diterapkan pada peta fitur keluaran lapisan konvolusional:

1. ***Squeeze* (Kompresi Global)** — Informasi spasial dari setiap kanal fitur dikompresi menjadi satu nilai skalar melalui operasi *global average pooling*. Untuk peta fitur $\mathbf{U} \in \mathbb{R}^{C \times H \times W}$ dengan $C$ kanal, operasi *squeeze* menghasilkan vektor deskriptor $\mathbf{z} \in \mathbb{R}^C$:

$$z_c = \frac{1}{H \times W} \sum_{i=1}^{H} \sum_{j=1}^{W} u_c(i, j)$$

Setiap elemen $z_c$ merepresentasikan respons global dari kanal ke-$c$, sehingga menangkap distribusi informasi pada kanal tersebut secara keseluruhan.

2. ***Excitation* (Pemodelan Hubungan Antar Kanal)** — Vektor deskriptor $\mathbf{z}$ diproses melalui dua lapisan *fully connected* (FC) yang membentuk arsitektur *bottleneck* untuk mempelajari hubungan non-linear antar kanal:

$$\mathbf{s} = \sigma(\mathbf{W}_2 \cdot \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{z}))$$

di mana $\mathbf{W}_1 \in \mathbb{R}^{C/r \times C}$ adalah matriks bobot reduksi, $\mathbf{W}_2 \in \mathbb{R}^{C \times C/r}$ adalah matriks bobot ekspansi, $r$ adalah rasio reduksi (*reduction ratio*), dan $\sigma$ adalah fungsi *sigmoid* yang menghasilkan bobot gerbang pada rentang $[0, 1]$. Rasio reduksi $r$ mengendalikan kapasitas dan biaya komputasi — nilai $r$ yang lebih besar mengurangi jumlah parameter dalam *bottleneck*.

3. ***Scale* (Pengalian Elemen)** — Bobot gerbang $\mathbf{s}$ yang telah dipelajari dikalikan secara elemen-per-elemen (*element-wise*) dengan peta fitur asli:

$$\tilde{u}_c = s_c \cdot u_c$$

di mana $s_c$ adalah bobot skalar untuk kanal ke-$c$ dan $u_c$ adalah peta fitur kanal ke-$c$. Kanal dengan bobot $s_c$ mendekati 1 dipertahankan, sedangkan kanal dengan bobot mendekati 0 ditekan.

#### 2.11.3 Relevansi SE *Block* untuk Fusi *Multi-Domain*

Dalam konteks deteksi *deepfake* berbasis pendekatan *hybrid*, SE *block* memiliki peran penting sebagai mekanisme fusi adaptif. Ketika fitur dari domain spasial (XceptionNet) dan domain frekuensi (FreqCNN) digabungkan melalui konkatenasi, vektor fusi yang dihasilkan mengandung dimensi-dimensi fitur dari kedua domain yang mungkin memiliki tingkat relevansi berbeda tergantung pada jenis manipulasi yang dihadapi.

Mekanisme SE memungkinkan model untuk:

1. **Menyesuaikan kontribusi relatif** kedua domain secara adaptif berdasarkan input — misalnya, memberikan bobot lebih tinggi pada fitur frekuensi ketika artefak spasial sulit dideteksi, atau sebaliknya.
2. **Menekan fitur yang redundan** atau mengandung *noise* dari salah satu cabang, sehingga proses klasifikasi tidak terganggu oleh informasi yang tidak relevan.
3. **Mengoptimalkan interaksi lintas domain** — SE *block* dapat mempelajari korelasi antara fitur spasial dan frekuensi yang tidak dapat ditangkap oleh konkatenasi sederhana.

Dibandingkan dengan mekanisme fusi sederhana seperti konkatenasi atau penjumlahan (*addition*), penggunaan SE *block* sebagai gerbang adaptif telah terbukti meningkatkan performa pada arsitektur *multi-branch* karena memungkinkan model untuk secara dinamis menyesuaikan strategi fusi berdasarkan karakteristik input (Hu et al., 2018).

---

## 7. Typo di BAB III Word (p.79) — SE Gate W1 Dimension

**Lokasi:** Halaman 79, Section 3.4.3.4

**Masalah:** Tertulis $\mathbf{W}_1 \in \mathbb{R}^{238 \times 512}$ — seharusnya $\mathbb{R}^{128 \times 512}$

**Perbaikan:** Ganti "238" dengan "128"

---

## 8. Referensi yang Perlu Ditambahkan ke Daftar Pustaka

| # | Referensi | Status |
|---|-----------|--------|
| 1 | I. Loshchilov dan F. Hutter, Decoupled Weight Decay Regularization, ICLR, 2019 | **PERLU DITAMBAHKAN** |
| 2 | J. Hu, L. Shen dan G. Sun, Squeeze-and-Excitation Networks, CVPR, 2018 | Sudah ditambahkan sebagai [42] |
