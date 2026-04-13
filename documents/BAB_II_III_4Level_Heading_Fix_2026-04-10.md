# BAB II & BAB III — Perbaikan Sub-Heading 4 Tingkat → Numbering

**Tanggal:** 10 April 2026
**Tujuan:** Mengubah sub-heading 4 tingkat (misal `2.9.4.1`, `3.3.2.1`) menjadi daftar bernomor di dalam induk 3 tingkatnya agar patuh pada **Pedoman Skripsi/Tesis 2025**:

- **§4.5.1.c** (halaman 23) — *"Tingkatan subbab maksimum 3 tingkat."*
- **§4.5.4** (halaman 25) — Penulisan *numbering* maksimum 3 tingkat dengan format: Tingkat 1 `1. 2. 3.`, Tingkat 2 `a. b. c.`, Tingkat 3 `i. ii. iii.`.

**Cakupan:** hanya sub-bab yang mengandung heading 4 tingkat. Semua sub-bab lain di BAB II dan BAB III sudah patuh dan **tidak diubah**.

**Cara pakai:** untuk setiap sub-bab di bawah, ganti seluruh isi sub-bab pada dokumen sumber (Word) dengan versi yang diberikan. Penomoran persamaan (`(2.5)`, `(3.17)`, dan seterusnya), tabel, gambar, serta sitasi dipertahankan sama persis dengan versi PDF.

**Ringkasan sub-bab yang diubah:**

| BAB | Sub-bab induk | Jumlah heading 4 tingkat yang di-flatten |
|---|---|---|
| II  | 2.9.4  Convolution Neural Network (CNN)                             | 6 |
| III | 3.3.2  Konversi Domain Frekuensi (FFT)                              | 5 |
| III | 3.3.3  Augmentasi Data                                              | 3 |
| III | 3.4.1  Model Spasial XceptionNet                                    | 2 |
| III | 3.4.2  Model Frekuensi FreqCNN                                      | 2 |
| III | 3.4.3  Model *Hybrid* HybridTwoBranch (*Late Fusion*)               | 6 |
| III | 3.5.4  Fungsi *Loss*, BCEWithLogitsLoss dengan *Label Smoothing*    | 3 |

---

## BAB II — Kajian Literatur

### 2.9.4  Convolution Neural Network (CNN)

*Convolutional Neural Network* (CNN) merupakan salah satu arsitektur utama dalam *deep learning* yang dirancang khusus untuk mengolah data berbentuk *grid*, seperti citra dua dimensi. CNN memanfaatkan operasi konvolusi untuk mengekstraksi fitur lokal secara hierarkis, sehingga mampu mengenali pola sederhana (tepi, tekstur) pada lapisan awal dan pola yang semakin kompleks (bagian wajah, objek) pada lapisan lebih dalam. Pendekatan ini berbeda dengan *multilayer perceptron* biasa karena CNN mengeksploitasi struktur spasial citra melalui *local receptive field* dan *weight sharing* sehingga jumlah parameter menjadi jauh lebih sedikit dan proses pelatihan lebih efisien [28, 32].

Secara umum, arsitektur CNN tersusun atas beberapa jenis lapisan utama, yaitu *convolutional layer*, *non-linear activation* (misalnya ReLU), *pooling layer*, dan *fully connected layer* di bagian akhir untuk melakukan klasifikasi. *Convolutional layer* melakukan operasi *filter* menggunakan *kernel* yang digeser secara spasial pada citra untuk menghasilkan *feature map*. *Weight sharing* membuat satu filter yang sama digunakan di seluruh posisi citra sehingga CNN bersifat *translationally equivariant* terhadap pola tertentu. *Pooling layer* (seperti *max-pooling*) kemudian mereduksi resolusi spasial *feature map* sambil mempertahankan informasi penting sehingga model menjadi lebih tahan terhadap variasi kecil posisi dan *noise*. Seluruh parameter jaringan dipelajari secara *end-to-end* menggunakan algoritma *backpropagation* dan optimisasi gradien turun [28, 32].

Dalam bidang visi komputer, CNN telah menjadi *backbone* utama untuk berbagai tugas pengenalan citra dan wajah. Arsitektur-arsitektur seperti *ResNet* memanfaatkan *residual connection* untuk mengatasi degradasi performa pada jaringan sangat dalam dan berhasil mencapai performa *state-of-the-art* pada berbagai *benchmark* klasifikasi citra [5]. Sementara itu, *XceptionNet* mengusulkan *depthwise separable convolution* untuk mengurangi kompleksitas komputasi tanpa mengorbankan akurasi, dan banyak diadopsi dalam berbagai studi deteksi *deepfake* sebagai *feature extractor* utama pada domain spasial [3, 6, 19]. Model ringan seperti *MesoNet* juga dirancang sebagai CNN berukuran kompak khusus untuk deteksi pemalsuan wajah pada video, dengan fokus pada artefak *meso-level* di area wajah [4].

Pada konteks deteksi *deepfake*, CNN digunakan untuk mempelajari artefak manipulasi yang sulit ditangkap oleh pengamatan manusia, seperti tekstur kulit yang tidak konsisten, *edge* yang tidak alami, atau pola *noise* yang ditinggalkan oleh proses generatif. Studi literatur menunjukkan bahwa sebagian besar detektor *deepfake* modern menggunakan CNN sebagai komponen utama, baik pada citra statis maupun *frame* video, dengan performa yang sangat kompetitif pada berbagai *dataset* seperti FaceForensics++ [10, 11, 15, 19]. Dalam skenario ini, CNN biasanya menerima *input* berupa *patch* wajah yang telah dipotong dan disejajarkan (*aligned*), kemudian mengeluarkan probabilitas apakah wajah tersebut asli atau hasil manipulasi.

Perkembangan terbaru menunjukkan bahwa CNN tidak hanya efektif di domain spasial, tetapi juga dapat digabungkan dengan analisis frekuensi untuk meningkatkan kemampuan generalisasi. Pendekatan seperti *Thinking in Frequency* memanfaatkan CNN yang dioptimalkan untuk memanfaatkan petunjuk pada domain frekuensi (misalnya melalui representasi FFT), sehingga jaringan lebih peka terhadap distorsi tinggi frekuensi yang dihasilkan oleh proses generatif [13]. Model lain seperti *SpecXNet*, FSBI, serta serangkaian metode *frequency-aware deepfake detection* memodifikasi arsitektur CNN atau *input*-nya dengan memasukkan kanal-kanal frekuensi tambahan atau modul khusus untuk menonjolkan komponen frekuensi tinggi, sehingga artefak yang tidak terlihat di domain spasial dapat dimanfaatkan secara lebih efektif untuk deteksi [9, 18, 20, 21, 32].

Selain memodelkan informasi spasial, CNN juga sering dikombinasikan dengan pemodelan temporal untuk video. Salah satu pendekatan umum adalah menggunakan CNN untuk mengekstraksi fitur per-*frame*, kemudian meneruskannya ke model sekuensial seperti LSTM atau GRU untuk menangkap dinamika temporal antar-*frame*, misalnya gerakan wajah dan sinkronisasi bibir. Pendekatan ini digunakan dalam berbagai karya deteksi *deepfake* berbasis *spatio-temporal*, termasuk yang mempelajari fitur pergerakan wajah dan artefak *temporal* pada video *deepfake* [26, 27]. Pendekatan *spatio-temporal* serupa juga diadopsi oleh *Haliassos et al.* yang memanfaatkan representasi CNN pada area mulut dan jaringan temporal untuk mendeteksi ketidakwajaran pola gerak bibir pada video sintetis [33]. Di luar domain forensik media, CNN juga digunakan secara luas bersama model sekuensial untuk tugas-tugas lain seperti peramalan beban dan konsumsi energi, menunjukkan bahwa arsitektur ini bersifat serbaguna dan dapat menangani data spasial maupun *spatio-temporal* di berbagai domain aplikasi [34].

Berikut komponen-komponen kunci *depthwise separable convolution* yang menjadi inti efisiensi XceptionNet, salah satu CNN paling banyak digunakan dalam deteksi *deepfake*:

1. **Depthwise Separable Convolution**

   Arsitektur XceptionNet merupakan salah satu model *Convolutional Neural Network* (CNN) modern yang dirancang untuk meningkatkan efisiensi ekstraksi fitur pada citra dengan memanfaatkan *depthwise separable convolution*. Pendekatan ini diperkenalkan oleh *Chollet* [6] sebagai pengembangan dari konsep *Inception Module*, dengan asumsi bahwa korelasi spasial dan korelasi kanal dapat dipisahkan sehingga proses konvolusi dapat dilakukan secara lebih optimal.

   Pada penelitian deteksi *deepfake*, XceptionNet banyak digunakan karena kemampuannya dalam mengekstraksi pola tekstur halus yang sering muncul sebagai artefak manipulasi wajah [4, 19]. Berbeda dengan konvolusi standar yang melakukan operasi terhadap seluruh kanal masukan secara bersamaan, *depthwise separable convolution* memecah operasi tersebut menjadi dua tahap, yaitu *depthwise convolution* dan *pointwise convolution*. Pemisahan ini secara signifikan mengurangi jumlah parameter dan kompleksitas komputasi tanpa mengurangi kapasitas representasi fitur, sehingga model menjadi lebih efisien dan stabil saat digunakan pada citra wajah beresolusi tinggi.

2. **Depthwise Convolution**

   Tahap pertama adalah *depthwise convolution*, yaitu proses konvolusi yang dilakukan secara independen pada setiap kanal masukan. Jika suatu citra masukan memiliki $M$ kanal dan kernel konvolusi berukuran $K \times K$, maka operasi *depthwise* akan menerapkan satu kernel per kanal secara terpisah. Secara matematis, *depthwise convolution* dapat dituliskan sebagai:

   $$D_m(x, y) = \sum_{i=0}^{K-1} \sum_{j=0}^{K-1} I_m(x + i, y + j) \cdot W_m(i, j) \tag{2.5}$$

   dengan:

   a. $I_m$ adalah kanal ke-$m$ dari citra masukan,
   b. $W_m$ adalah kernel konvolusi untuk kanal ke-$m$,
   c. $D_m$ adalah hasil *depthwise convolution* pada kanal ke-$m$.

   Pendekatan ini memungkinkan model mengekstraksi pola tekstur lokal secara lebih rinci, terutama pada bagian wajah yang sering mengandung artefak seperti *blending* dan *warping* pada *deepfake* [4].

3. **Pointwise Convolution**

   Tahap kedua adalah *pointwise convolution*, yaitu penerapan kernel berukuran $1 \times 1$ untuk menggabungkan kembali seluruh kanal hasil *depthwise* menjadi satu set fitur baru. Tahap ini bertujuan menangkap korelasi antarkanal yang tidak diproses pada tahap sebelumnya. Secara matematis, *pointwise convolution* dapat dituliskan sebagai:

   $$P(x, y) = \sum_{m=1}^{M} D_m(x, y) \cdot W_m^{pw} \tag{2.6}$$

   dengan:

   a. $D_m$ adalah keluaran *depthwise*,
   b. $W_m^{pw}$ adalah bobot kernel $1 \times 1$ pada kanal ke-$m$.

   Tahap ini membentuk representasi fitur yang lebih kaya karena menggabungkan informasi dari seluruh kanal, sekaligus tetap menjaga efisiensi komputasi.

4. **Kompleksitas Depthwise Separable Convolution**

   Perbedaan signifikan antara konvolusi biasa dan *depthwise separable convolution* terletak pada kompleksitas komputasi.

   a. *Konvolusi Standar.* Total operasi konvolusi standar:

   $$C_{standard} = K^2 \times M \times N \tag{2.7}$$

   dengan $N$ adalah jumlah kanal keluaran.

   b. *Depthwise Separable Convolution.* Operasi *depthwise* + *pointwise*:

   $$C_{DSC} = K^2 \times M + (M \times N) \tag{2.8}$$

   Sehingga efisiensi diperoleh karena:

   $$C_{DSC} \ll C_{standard} \tag{2.9}$$

   Efisiensi ini sangat relevan untuk penelitian deteksi *deepfake* yang menggunakan data dalam jumlah besar dan memerlukan proses pelatihan berulang-ulang.

5. **Relevansi Depthwise Separable Convolution pada Deteksi Deepfake**

   XceptionNet terbukti efektif untuk pendeteksian manipulasi wajah karena:

   a. *Sensitif terhadap pola tekstur lokal.* Artefak *deepfake* biasanya muncul pada area transisi wajah, seperti sekitar mata, hidung, dan garis rahang. *Depthwise convolution* menyoroti detail lokal ini dengan baik.

   b. *Stabil pada variasi kualitas video.* Variasi kompresi (contoh dari *dataset* FaceForensics++) tidak mengganggu performa secara signifikan karena struktur konvolusi XceptionNet lebih tahan terhadap *compression noise* [19].

   c. *Kompatibel dengan analisis frekuensi.* Kombinasi kanal RGB dan kanal frekuensi (hasil FFT) membutuhkan model yang ringan namun mampu menangkap interaksi tingkat tinggi. XceptionNet cocok untuk skenario *hybrid* ini.

   d. *Performa tinggi di berbagai dataset deepfake.* Banyak penelitian menunjukkan XceptionNet unggul pada *dataset* FF++, DFDC, dan Celeb-DF [9, 19].

   e. *Kemampuan representasi spasial yang kuat.* *Depthwise separable convolution* menghasilkan fitur berlapis-lapis yang mampu memisahkan pola alami dan pola palsu pada wajah sintetis.

6. **Integrasi dengan FFT sebagai Channel Tambahan**

   Dalam penelitian ini, fitur frekuensi hasil transformasi FFT ditambahkan sebagai kanal keempat pada *input* XceptionNet. *Depthwise separable convolution* sangat cocok untuk pemrosesan data multi-kanal seperti ini, karena:

   a. setiap kanal ditangani secara independen (melalui *depthwise*),
   b. setiap kanal digabungkan dalam tahap *pointwise*.

   Hal ini memungkinkan arsitektur memahami hubungan antara pola spasial (RGB) dan pola frekuensi (FFT), sebagaimana juga dilakukan pada pendekatan *SpecXNet* [9] dan FSBI [18].

---

## BAB III — Tahapan Pelaksanaan

### 3.3.2  Konversi Domain Frekuensi (FFT)

Konversi domain frekuensi merupakan inti kontribusi penelitian ini. Proses ini mengubah setiap *frame* citra RGB menjadi representasi peta *magnitude* frekuensi menggunakan *Fast Fourier Transform* (FFT) 2 dimensi. Representasi frekuensi ini menangkap artefak spektral yang dihasilkan oleh proses sintesis *deepfake*, seperti *checkerboard artifacts* dari operasi *upsampling* pada GAN [16], distorsi distribusi spektral [7], dan ketidakkontinyuan pada batas *blending* [8].

1. **Konversi RGB ke Grayscale**

   Langkah pertama adalah mengonversi citra RGB menjadi *grayscale* (satu kanal). Konversi dilakukan menggunakan standar ITU-R BT.601 dengan formula:

   $$Y = 0{,}299R + 0{,}587G + 0{,}114B \tag{3.1}$$

   di mana $Y$ adalah nilai luminansi, dan $R, G, B$ adalah nilai kanal warna merah, hijau, dan biru. Bobot yang berbeda pada setiap kanal mencerminkan sensitivitas mata manusia terhadap masing-masing warna. Konversi ke satu kanal cukup untuk analisis frekuensi karena informasi luminansi merepresentasikan distribusi intensitas spasial yang diperlukan untuk mendeteksi artefak spektral.

2. **Transformasi Fourier 2D**

   Citra *grayscale* kemudian diubah ukurannya menjadi $224 \times 224$ dan ditransformasi ke domain frekuensi menggunakan *Discrete Fourier Transform* (DFT) 2 dimensi. DFT 2D didefinisikan sebagai:

   $$F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) \cdot e^{-j \cdot 2\pi \left(\frac{u \cdot x}{M} + \frac{v \cdot y}{N}\right)} \tag{3.2}$$

   di mana $f(x, y)$ adalah nilai piksel pada posisi $(x, y)$, $F(u, v)$ adalah koefisien frekuensi pada koordinat frekuensi $(u, v)$, $M$ dan $N$ adalah dimensi citra (keduanya 224), dan $j = \sqrt{-1}$ adalah unit imajiner.

   Setelah transformasi, dilakukan operasi *FFT shift* yang memindahkan komponen frekuensi nol (*DC component*) dari sudut matriks ke posisi tengah. Hal ini menyebabkan frekuensi rendah terletak di bagian tengah peta frekuensi dan frekuensi tinggi di bagian tepi, sehingga memudahkan interpretasi visual dan analisis.

3. **Magnitude Spectrum dan Log Scaling**

   Dari hasil DFT yang berupa bilangan kompleks, dihitung *magnitude spectrum*:

   $$|F(u, v)| = \sqrt{Re(F(u, v))^2 + Im(F(u, v))^2} \tag{3.3}$$

   Karena rentang dinamis *magnitude spectrum* sangat lebar, komponen DC (*direct current*) dapat bernilai ribuan kali lipat lebih besar dari komponen frekuensi tinggi, maka dilakukan transformasi logaritmik:

   $$M_{log}(u, v) = \log(1 + |F(u, v)|) \tag{3.4}$$

   Fungsi $\log(1 + x)$ (dikenal sebagai *log1p*) dipilih karena dua alasan: pertama, menghindari permasalahan $\log(0)$ karena $\log(1 + 0) = 0$; dan kedua, mengompresi rentang dinamis sehingga detail pada frekuensi tinggi tidak tertutupi oleh dominasi komponen DC. Hasil akhir berupa matriks *float32* berukuran $224 \times 224$ dengan nilai tipikal pada rentang $[0, \sim 16]$ yang disimpan sebagai berkas `.npy` (*NumPy array*) dalam *cache* FFT.

4. **Contoh Perhitungan FFT 2D**

   Sebagai ilustrasi, berikut ditunjukkan perhitungan FFT 2D pada matriks *grayscale* berukuran $4 \times 4$. Misalkan matriks piksel $f(x, y)$ adalah:

   *Tabel 3.3 Contoh Matriks Grayscale 4x4*

   |        | $y = 0$ | $y = 1$ | $y = 2$ | $y = 3$ |
   |--------|---------|---------|---------|---------|
   | $x = 0$ | 100 | 120 | 100 | 120 |
   | $x = 1$ | 80  | 100 | 80  | 100 |
   | $x = 2$ | 100 | 120 | 100 | 120 |
   | $x = 3$ | 80  | 100 | 80  | 100 |

   a. *Menghitung $F(0,0)$, yaitu komponen DC*

   $$F(0, 0) = \sum_{x=0}^{3} \sum_{y=0}^{3} f(x, y) \cdot e^{-j \cdot 2\pi(0)} \tag{3.5}$$

   $$F(0, 0) = (100 + 120 + 100 + 120) + (80 + 100 + 80 + 100) + (100 + 120 + 100 + 120) + (80 + 100 + 80 + 100)$$

   $$F(0, 0) = 440 + 360 + 440 + 360 = 1600$$

   Komponen DC merepresentasikan rata-rata intensitas keseluruhan citra, yaitu $\frac{1600}{16} = 100$.

   b. *Menghitung $F(0,1)$, yaitu frekuensi horizontal pertama*

   $$F(0, 1) = \sum_{x=0}^{3} \sum_{y=0}^{3} f(x, y) \cdot e^{-j \cdot 2\pi \left(\frac{y}{4}\right)} \tag{3.6}$$

   Karena $e^{-j \cdot 2\pi (y/4)}$ menghasilkan faktor $\{1, -j, -1, j\}$ untuk $y = 0, 1, 2, 3$:

   i. Baris $x = 0$: $100(1) + 120(-j) + 100(-1) + 120(j) = 0 + (-120j + 120j) = 0$.
   ii. Baris $x = 1$: $80(1) + 100(-j) + 80(-1) + 100(j) = 0 + (-100j + 100j) = 0$.
   iii. Baris $x = 2$: pola sama dengan baris $x = 0$, menghasilkan 0.
   iv. Baris $x = 3$: pola sama dengan baris $x = 1$, menghasilkan 0.

   Sehingga $F(0, 1) = 0$. Hal ini menunjukkan bahwa pola frekuensi horizontal pada matriks ini simetris.

   c. *Menghitung $F(1,0)$, yaitu frekuensi vertikal pertama*

   $$F(1, 0) = \sum_{x=0}^{3} \sum_{y=0}^{3} f(x, y) \cdot e^{-j \cdot 2\pi \left(\frac{x}{4}\right)} \tag{3.7}$$

   Faktor $e^{-j \cdot 2\pi (x/4)}$ menghasilkan $\{1, -j, -1, j\}$ untuk $x = 0, 1, 2, 3$:

   i. $x = 0$: $(100 + 120 + 100 + 120)(1) = 440$.
   ii. $x = 1$: $(80 + 100 + 80 + 100)(-j) = -360j$.
   iii. $x = 2$: $(100 + 120 + 100 + 120)(-1) = -440$.
   iv. $x = 3$: $(80 + 100 + 80 + 100)(j) = 360j$.

   Sehingga $F(1, 0) = 440 - 360j - 440 + 360j = 0$.

   d. *Menghitung $F(1,1)$*

   $$F(1, 1) = \sum_{x=0}^{3} \sum_{y=0}^{3} f(x, y) \cdot e^{-j \cdot 2\pi \left(\frac{x + y}{4}\right)} \tag{3.8}$$

   Faktor gabungan $e^{-j \cdot 2\pi \left(\frac{x+y}{4}\right)}$ untuk setiap $(x, y)$ ditunjukkan pada tabel berikut:

   | $(x, y)$ | $f(x, y)$ | $e^{-j \cdot 2\pi \left(\frac{x+y}{4}\right)}$ | Hasil |
   |----------|-----------|------------------------------------------------|-------|
   | (0, 0) | 100 | $1$    | $100$   |
   | (0, 1) | 120 | $-j$   | $-120j$ |
   | (0, 2) | 100 | $-1$   | $-100$  |
   | (0, 3) | 120 | $j$    | $120j$  |
   | (1, 0) | 80  | $-j$   | $-80j$  |
   | (1, 1) | 100 | $-1$   | $-100$  |
   | (1, 2) | 80  | $j$    | $80j$   |
   | (1, 3) | 100 | $1$    | $100$   |
   | (2, 0) | 100 | $-1$   | $-100$  |
   | (2, 1) | 120 | $j$    | $120j$  |
   | (2, 2) | 100 | $1$    | $100$   |
   | (2, 3) | 120 | $-j$   | $-120j$ |
   | (3, 0) | 80  | $j$    | $80j$   |
   | (3, 1) | 100 | $1$    | $100$   |
   | (3, 2) | 80  | $-j$   | $-80j$  |
   | (3, 3) | 100 | $-1$   | $-100$  |

   i. Penjumlahan bagian real: $100 - 100 - 100 + 100 - 100 + 100 + 100 - 100 = 0$.
   ii. Penjumlahan bagian imajiner: $-120 - 80 + 120 + 120 + 120 - 120 + 80 - 80 = 0$.

   Sehingga $F(1, 1) = 0 + 0j = 0$. Matriks ini memiliki pola repetitif sempurna sehingga energi terkonsentrasi pada komponen DC. Pada citra wajah sesungguhnya, distribusi energi lebih tersebar dan perbedaan antara citra *real* dan *fake* terlihat dari pola distribusi frekuensi tinggi yang anomal.

   e. *Magnitude dan Log Scaling*

   *Tabel 3.4 Contoh Perhitungan Magnitude dan Log Scaling*

   | Komponen | $F(u, v)$ | $\lvert F(u, v) \rvert$ | $\log(1 + \lvert F(u, v) \rvert)$ |
   |----------|-----------|-------------------------|-----------------------------------|
   | $F(0, 0)$ | 1600 | 1600 | 7,378 |
   | $F(0, 1)$ | 0    | 0    | 0     |
   | $F(1, 0)$ | 0    | 0    | 0     |
   | $F(1, 1)$ | 0    | 0    | 0     |

   Pada citra *deepfake* sesungguhnya, komponen frekuensi tinggi menunjukkan pola anomali yang khas, seperti *spectral rolloff* yang tidak wajar [7] atau puncak periodik akibat *checkerboard artifacts* dari operasi *transposed convolution* pada GAN [16].

5. **Normalisasi FFT**

   Setelah seluruh *frame* dikonversi ke peta *magnitude* FFT dan disimpan dalam *cache*, dilakukan perhitungan statistik normalisasi per *dataset*. Normalisasi menggunakan *z-score*:

   $$\hat{x} = \frac{x - \mu}{\sigma} \tag{3.9}$$

   di mana $\mu$ dan $\sigma$ adalah rata-rata dan simpangan baku global yang dihitung dari seluruh piksel dalam *cache* FFT *dataset* tersebut. Perhitungan dilakukan pada sampel acak hingga 5.000 berkas *cache* menggunakan akumulasi *online* (metode Welford) untuk efisiensi memori. Hasil disimpan dalam berkas `fft_stats.json` yang dimuat secara otomatis saat pelatihan.

   Normalisasi per *dataset* ini penting karena setiap *dataset* memiliki karakteristik spektral yang berbeda akibat perbedaan kamera, resolusi, dan metode kompresi. Tanpa normalisasi yang tepat, fitur frekuensi dari *dataset* yang berbeda akan memiliki skala yang tidak sebanding.

---

### 3.3.3  Augmentasi Data

Augmentasi data merupakan teknik regularisasi yang diterapkan selama pelatihan untuk meningkatkan keberagaman data tanpa menambah jumlah sampel asli. Pada penelitian ini, strategi augmentasi dirancang secara terpisah untuk domain spasial dan domain frekuensi, karena karakteristik kedua representasi data yang berbeda secara fundamental. Selain itu, pada mode *hybrid*, konsistensi augmentasi antara kedua cabang dijaga untuk mempertahankan korespondensi spasial-frekuensi.

1. **Augmentasi Domain Spasial**

   Augmentasi pada domain spasial diterapkan pada citra RGB selama pelatihan untuk meningkatkan keberagaman data dan mencegah *overfitting*. *Pipeline* augmentasi terdiri dari:

   a. *Resize*, citra diubah ukurannya menjadi $256 \times 256$ piksel (lebih besar dari ukuran *input* final).

   b. *RandomResizedCrop*, pemotongan acak ke ukuran $224 \times 224$ dengan skala antara 80%–100% dari citra asli. Augmentasi ini mensimulasikan variasi *zoom* dan posisi wajah.

   c. *ColorJitter*, yaitu perubahan acak pada kecerahan ($\pm 0{,}2$), kontras ($\pm 0{,}2$), saturasi ($\pm 0{,}1$), dan *hue* ($\pm 0{,}05$). Augmentasi ini mensimulasikan variasi kondisi pencahayaan, pengaturan kamera, dan karakteristik sensor yang berbeda antar video sumber.

   d. *RandomHorizontalFlip*, pembalikan horizontal dengan probabilitas 50%. Augmentasi ini memanfaatkan simetri bilateral wajah manusia.

   e. *ToTensor*, konversi ke tensor PyTorch dengan rentang nilai $[0, 1]$.

   f. *Normalize*, normalisasi menggunakan statistik ImageNet:

   $$\text{mean} = [0{,}485;\ 0{,}456;\ 0{,}406]$$
   $$\text{std}\;\; = [0{,}229;\ 0{,}224;\ 0{,}225]$$

   g. *RandomErasing*, penghapusan acak sebuah area persegi panjang pada tensor (probabilitas 10%, skala 2%–15% dari luas citra) yang diisi dengan nilai acak. Teknik ini diterapkan setelah normalisasi (beroperasi pada tensor, bukan citra PIL) dan mendorong model untuk tidak bergantung pada satu wilayah spesifik dari citra wajah, meningkatkan ketahanan terhadap oklusi parsial.

   Pada tahap validasi dan pengujian, augmentasi acak tidak diterapkan. Citra hanya diubah ukurannya secara langsung ke $224 \times 224$, dikonversi ke tensor, dan dinormalisasi.

2. **Augmentasi Domain Frekuensi**

   Augmentasi pada domain frekuensi memerlukan pendekatan yang berbeda dari domain spasial. Operasi spasial seperti pemotongan acak (*random crop*) atau rotasi tidak sesuai untuk peta *magnitude* FFT karena akan merusak lokalisasi frekuensi; setiap posisi piksel pada peta FFT merepresentasikan komponen frekuensi spesifik yang bergantung pada posisi absolutnya.

   Oleh karena itu, augmentasi pada domain frekuensi dilakukan melalui injeksi *noise* Gaussian:

   $$\hat{x}_{fft} = x_{fft} + \epsilon_1,\quad \epsilon \sim \mathcal{N}(0, \sigma^2) \tag{3.10}$$

   dengan $\sigma = 0{,}05$ (dikonfigurasi melalui parameter `fft_noise_sigma`). *Noise* diterapkan setelah normalisasi *z-score* dan hanya selama pelatihan. Rasional dari pendekatan ini adalah:

   a. menyimulasikan variasi *noise* sensor dan artefak kompresi yang memengaruhi spektrum frekuensi;
   b. mencegah penghafalan (*memorization*) peta FFT yang identik di setiap *epoch* karena data FFT dimuat dari *cache* statis.

   Selain injeksi *noise*, diterapkan pula **spectral band masking** dengan probabilitas 15%. Pada setiap *frame* yang terpilih secara acak, sebuah pita frekuensi, baik horizontal maupun vertikal dengan lebar acak antara 2 hingga $\lfloor H/8 \rfloor$ piksel diisi dengan nilai nol:

   $$\hat{x}_{fft}[r_1 : r_1 + w, :] = 0 \quad (\text{pita horizontal}) \tag{3.11}$$
   $$\hat{x}_{fft}[:, c_1 : c_1 + w] = 0 \quad (\text{pita vertikal}) \tag{3.12}$$

   di mana $w$ adalah lebar pita acak dan $r_1$ atau $c_1$ adalah posisi awal acak. Pemilihan orientasi horizontal atau vertikal dilakukan dengan probabilitas 50:50. Teknik ini mencegah model bergantung pada satu pita frekuensi spesifik dan mendorong representasi frekuensi yang lebih merata dan *robust*.

   *Gambar 3.3 Contoh Penerapan Spectral Band Masking pada Peta Magnitude FFT*

3. **Konsistensi Augmentasi pada Mode Hybrid**

   Pada mode *hybrid*, di mana model menerima *input* RGB dan FFT secara bersamaan, konsistensi augmentasi antara kedua cabang sangat penting. Pembalikan horizontal (*horizontal flip*) pada citra RGB tanpa pembalikan yang sama pada peta FFT akan merusak korespondensi spasial-frekuensi, karena $|DFT(\text{flip}(x))| = \text{flip}(|DFT(x)|)$.

   Untuk mengatasi hal ini, pembalikan horizontal pada mode *hybrid* diterapkan secara manual setelah kedua *input* dimuat, dengan keputusan acak yang sama (probabilitas 50%) diterapkan secara identik pada tensor RGB dan tensor FFT. Pada *pipeline* augmentasi spasial untuk mode *hybrid*, opsi `RandomHorizontalFlip` dinonaktifkan (`include_hflip=False`) agar pembalikan dapat dikontrol secara terpadu.

---

### 3.4.1  Model Spasial XceptionNet

Model spasial merupakan *baseline* utama dalam penelitian ini yang menganalisis fitur visual langsung dari citra RGB. Arsitektur XceptionNet dipilih karena telah terbukti sebagai salah satu model paling efektif untuk deteksi *deepfake* pada domain spasial, sebagaimana ditunjukkan oleh *Rössler et al.* [19] yang melaporkan akurasi 96–99% pada *dataset* FaceForensics++. Bagian berikut menjelaskan komponen utama arsitektur XceptionNet yang digunakan dalam penelitian ini.

1. **Depthwise Separable Convolution**

   XceptionNet [6] merupakan arsitektur *convolutional neural network* (CNN) yang dibangun sepenuhnya dari *depthwise separable convolution*. Berbeda dengan konvolusi standar yang menerapkan filter secara simultan pada dimensi spasial dan kanal, *depthwise separable convolution* memfaktorisasi operasi menjadi dua tahap terpisah:

   a. *Konvolusi depthwise*, menerapkan satu filter konvolusi per kanal *input* secara independen. Untuk *input* dengan $C$ kanal dan filter berukuran $K \times K$, jumlah parameter adalah $C \times K \times K$.

   b. *Konvolusi pointwise*, menerapkan konvolusi $1 \times 1$ untuk menggabungkan informasi lintas kanal. Untuk menghasilkan $C'$ kanal *output*, jumlah parameter adalah $C \times C'$.

   **Contoh perhitungan perbandingan parameter**, untuk *input* berukuran $H \times W$ dengan $C_{in} = 64$ kanal, filter $3 \times 3$, dan $C_{out} = 128$ kanal *output*:

   a. Konvolusi standar:

   $$C_{in} \times K^2 \times C_{out} = 64 \times 9 \times 128 = 73.728 \text{ parameter}$$

   b. Konvolusi *depthwise separable*:

   i. *Depthwise*: $C_{in} \times K^2 = 64 \times 9 = 576$ parameter.
   ii. *Pointwise*: $C_{in} \times C_{out} = 64 \times 128 = 8.192$ parameter.
   iii. Total: $576 + 8.192 = 8.768$ parameter.

   c. Rasio pengurangan: $\frac{8.768}{73.728} \approx 11{,}9\%$, yaitu pengurangan parameter sebesar $\sim 88\%$.

   Efisiensi parameter ini memungkinkan XceptionNet memiliki kedalaman yang besar (36 *layer* konvolusional) dengan total $\sim 22{,}8$ juta parameter, sambil tetap mempertahankan kapasitas representasi yang tinggi.

   **Contoh perhitungan Depthwise Separable Convolution**, misalkan *input* berukuran $3 \times 3$ dengan 2 kanal:

   $$X_1 = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 1 & 2 \\ 0 & 1 & 3 \end{bmatrix},\quad X_2 = \begin{bmatrix} 2 & 0 & 1 \\ 1 & 3 & 0 \\ 2 & 1 & 1 \end{bmatrix} \tag{3.13}$$

   a. *Depthwise*, filter $2 \times 2$ terpisah per kanal (tanpa *padding*, *stride* = 1):

   $$W_1 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix},\quad W_2 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} \tag{3.14}$$

   Konvolusi kanal 1 ($X_1 * W_1$) posisi $(0, 0)$:

   $$1 \times 1 + 2 \times 0 + 3 \times 0 + 1 \times 1 = 2 \tag{3.15}$$

   Hasil lengkap kanal 1:

   $$Y_1 = \begin{bmatrix} 2 & 3 \\ 4 & 4 \end{bmatrix}$$

   Konvolusi kanal 2 ($X_2 * W_2$) posisi $(0, 0)$:

   $$2 \times 0 + 0 \times 1 + 1 \times 1 + 3 \times 10 = 1 \tag{3.16}$$

   Hasil lengkap kanal 2:

   $$Y_2 = \begin{bmatrix} 1 & 4 \\ 2 & 1 \end{bmatrix}$$

   b. *Pointwise*, filter $1 \times 1$ berukuran $(2, 1)$ misalnya $[0{,}5;\ 0{,}5]$:

   $$Z(i, j) = 0{,}5 \times Y_1(i, j) + 0{,}5 \times Y_2(i, j) \tag{3.17}$$
   $$Z = \begin{bmatrix} 1{,}5 & 3{,}5 \\ 3{,}0 & 2{,}5 \end{bmatrix}$$

   Hasil akhir merupakan gabungan informasi lintas kanal yang diperoleh secara efisien melalui dua tahap terpisah.

2. **Transfer Learning dari ImageNet**

   XceptionNet yang digunakan dalam penelitian ini diinisialisasi dengan bobot yang telah dilatih pada *dataset* ImageNet [6, 19], yang terdiri dari 1,4 juta citra dalam 1.000 kelas. *Transfer learning* dari ImageNet memberikan fondasi representasi visual yang kuat, fitur-fitur tingkat rendah (tepi, tekstur) dan tingkat menengah (pola, bentuk) yang telah dipelajari dari ImageNet relevan dan dapat ditransfer ke tugas deteksi *deepfake*.

   Model diimplementasikan menggunakan pustaka *timm* (*PyTorch Image Models*) melalui pemanggilan `timm.create_model("xception", pretrained=True)`. Lapisan klasifikasi asli ImageNet (1.000 kelas) diganti dengan lapisan *fully connected* tunggal yang menghasilkan satu nilai *logit* untuk klasifikasi biner (*real* vs *fake*). Dimensi fitur yang dihasilkan oleh *backbone* XceptionNet setelah *global average pooling* adalah 2.048.

---

### 3.4.2  Model Frekuensi FreqCNN

Model frekuensi dirancang untuk mengekstraksi dan menganalisis artefak pada domain frekuensi yang tidak terdeteksi oleh model spasial. Berbeda dengan XceptionNet yang memproses citra RGB secara langsung, FreqCNN memproses peta *magnitude* FFT yang merepresentasikan distribusi energi frekuensi dalam citra. Arsitektur ini dibangun khusus untuk tugas ini dengan desain yang lebih ringan namun mampu menangkap pola spektral yang khas dari citra *deepfake*.

1. **Arsitektur Konvolusional**

   FreqCNN adalah jaringan konvolusional ringan yang dirancang khusus untuk memproses peta *magnitude* FFT berdimensi satu kanal. Arsitektur ini terdiri dari blok-blok konvolusional residual bertingkat (*FreqBlock*) yang secara progresif mengekstraksi fitur frekuensi dari resolusi rendah hingga tinggi.

   Setiap *FreqBlock* mengimplementasikan koneksi residual yang terinspirasi dari *ResNet* (He et al., 2016) dan terdiri dari dua jalur paralel:

   a. *Jalur utama*: Conv2d($3 \times 3$, padding = 1) → BatchNorm2d → ReLU.
   b. *Jalur pintasan* (*shortcut*), konvolusi $1 \times 1$ untuk menyesuaikan dimensi kanal ketika jumlah kanal *input* berbeda dari *output*. Apabila dimensi sudah sama, jalur pintasan berupa operasi identitas (*identity*).

   Kedua jalur dijumlahkan secara elemen (*residual addition*) sebelum *max pooling* dengan *stride* 2:

   $$\mathbf{y} = \text{MaxPool}_{2 \times 2}\left(\text{Conv}_{3 \times 3}(\mathbf{x}) + \text{Shortcut}(\mathbf{x})\right) \tag{3.18}$$

   Koneksi residual ini mencegah degradasi gradien pada jaringan yang lebih dalam dan memungkinkan setiap blok mempelajari representasi fitur tambahan (*residual*) di atas representasi yang sudah ada.

   *Gambar 3.5 Arsitektur FreqBlock dengan Koneksi Residual*

   Konfigurasi yang digunakan dalam penelitian ini adalah *depth* = 5 dengan *base_channels* = 32, menghasilkan progresi kanal $[32, 64, 128, 256, 256]$. Dua blok terakhir menggunakan jumlah kanal yang sama (256), di mana jalur pintasan pada blok kelima berupa operasi identitas karena dimensi *input* dan *output* sudah sesuai.

   *Tabel 3.5 Arsitektur Layer-by-Layer FreqCNN (depth = 5, base_channels = 32)*

   | Layer | Tipe | Dimensi Input | Dimensi Output | Parameter |
   |-------|------|---------------|----------------|-----------|
   | FreqBlock 1 | Conv(1→32, 3×3) + BN + Shortcut(1×1) + MaxPool | (1, 224, 224)  | (32, 112, 112)  | $\sim 384$     |
   | FreqBlock 2 | Conv(32→64, 3×3) + BN + Shortcut(1×1) + MaxPool | (32, 112, 112) | (64, 56, 56)    | $\sim 20.700$  |
   | FreqBlock 3 | Conv(64→128, 3×3) + BN + Shortcut(1×1) + MaxPool | (64, 56, 56)  | (128, 28, 28)   | $\sim 82.300$  |
   | FreqBlock 4 | Conv(128→256, 3×3) + BN + Shortcut(1×1) + MaxPool | (128, 28, 28) | (256, 14, 14)   | $\sim 328.000$ |
   | FreqBlock 5 | Conv(256→256, 3×3) + BN + Identity + MaxPool | (256, 14, 14)  | (256, 7, 7)     | $\sim 590.000$ |
   | Dropout2d(0,2) | *Spatial dropout*   | (256, 7, 7) | (256, 7, 7) | 0 |
   | AdaptiveAvgPool | *Global average pooling* | (256, 7, 7) | (256, 1, 1) | 0 |
   | FC 1 | Linear(256→128) + ReLU | (256) | (128) | $\sim 33.000$ |
   | Dropout(0,3) | *Dropout* | (128) | (128) | 0 |
   | FC 2 | Linear(128→1) | (128) | (1) | $\sim 129$ |
   | | **Total** | | | **$\sim 700K$** |

   Meskipun jumlah parameter FreqCNN ($\sim 700.000$) lebih besar dibandingkan konfigurasi *depth* = 3 ($\sim 130.000$), model ini tetap jauh lebih kecil dari XceptionNet ($\sim 22{,}8$ juta parameter). Kedalaman 5 blok dipilih untuk mengekstraksi fitur frekuensi yang lebih kaya, dengan blok-blok tambahan memungkinkan model menangkap pola spektral pada berbagai tingkat abstraksi, dari artefak frekuensi rendah (seperti distribusi energi global) hingga anomali frekuensi tinggi (seperti *spectral rolloff* dan *checkerboard patterns*). Koneksi residual memastikan bahwa pelatihan tetap stabil meskipun kedalaman jaringan bertambah.

   Kedalaman FreqCNN dapat dikonfigurasi melalui parameter `freq_depth` dan `freq_base_channels` (jumlah kanal awal, *default* 32). Jumlah kanal berlipat dua pada setiap blok hingga batas maksimum $8 \times \text{base\_channels} = 256$.

2. **Contoh Perhitungan Forward Pass**

   Berikut ditunjukkan contoh perhitungan *forward pass* pada satu blok konvolusional FreqCNN dengan *input* sederhana berukuran $4 \times 4$, satu kanal.

   *Input* (peta *magnitude* FFT tersederhanakan):

   $$X_1 = \begin{bmatrix} 2{,}1 & 3{,}5 & 1{,}2 & 4{,}0 \\ 0{,}8 & 2{,}3 & 3{,}1 & 1{,}5 \\ 4{,}2 & 1{,}0 & 2{,}7 & 3{,}3 \\ 1{,}6 & 3{,}8 & 0{,}5 & 2{,}9 \end{bmatrix} \tag{3.19}$$

   **Konvolusi** dengan *kernel* $3 \times 3$ (misalkan bobot $\mathbf{W}$ dan bias $b = 0$), *padding* = 1. Posisi $(0, 0)$ dengan *zero padding*:

   $$z_{0,0} = 0 \cdot w_{00} + 0 \cdot w_{01} + 0 \cdot w_{02}$$
   $$+ 0 \cdot w_{10} + 2{,}1 \cdot w_{11} + 3{,}5 \cdot w_{12}$$
   $$+ 0 \cdot w_{20} + 0{,}8 \cdot w_{21} + 2{,}3 \cdot w_{22} \tag{3.20}$$

   **BatchNorm**, setelah seluruh posisi dihitung, *batch normalization* menormalisasi *output*:

   $$\hat{z}_i = \frac{z_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \cdot \gamma + \beta \tag{3.21}$$

   Di mana $\mu_B$ dan $\sigma_B^2$ adalah rata-rata dan varians *mini-batch*, $\gamma$ dan $\beta$ adalah parameter *learnable*, dan $\epsilon = 10^{-5}$ mencegah pembagian dengan nol.

   **ReLU**, $\text{ReLU}(\hat{z}) = \max(0, \hat{z})$. Nilai negatif diubah menjadi nol.

   **MaxPool2d(2)**, pada *grid* $2 \times 2$, diambil nilai maksimum. Dari *output* $4 \times 4$, dihasilkan peta fitur berukuran $2 \times 2$.

---

### 3.4.3  Model *Hybrid* HybridTwoBranch (*Late Fusion*)

Model *hybrid* merupakan kontribusi utama penelitian ini. Arsitektur HybridTwoBranch menggabungkan fitur dari domain spasial dan domain frekuensi melalui mekanisme *late fusion*: kedua cabang mengekstraksi fitur secara independen, kemudian fitur digabungkan dan diproses bersama untuk klasifikasi akhir.

1. **Cabang Spasial (XceptionNet Backbone)**

   Cabang spasial menggunakan XceptionNet sebagai *feature extractor* dengan konfigurasi `num_classes=0`, yang berarti lapisan klasifikasi dihilangkan dan model hanya menghasilkan vektor fitur. *Input* berupa citra RGB berukuran $(3, 224, 224)$ yang telah dinormalisasi menggunakan statistik ImageNet. *Output* berupa vektor fitur berdimensi 2.048 yang merepresentasikan fitur spasial tingkat tinggi dari citra wajah.

2. **Cabang Frekuensi (FreqCNN Backbone)**

   Cabang frekuensi menggunakan bagian *backbone* dari FreqCNN (blok konvolusional + *global average pooling*) tanpa lapisan klasifikasi. *Input* berupa peta *magnitude* FFT berukuran $(1, 224, 224)$ yang telah dinormalisasi menggunakan *z-score* per *dataset*. *Output* berupa vektor fitur berdimensi 256 (pada konfigurasi *depth* = 5) yang merepresentasikan pola frekuensi dalam citra.

3. **Projection Layers dan Penyeimbangan Dimensi**

   Tantangan utama dalam *late fusion* adalah ketidakseimbangan dimensi antara kedua cabang. Cabang spasial menghasilkan vektor berdimensi 2.048, sedangkan cabang frekuensi hanya 256, dengan rasio 8:1. Apabila kedua vektor langsung digabungkan (*concatenation*), fitur spasial akan mendominasi proses klasifikasi karena magnitudonya yang jauh lebih besar.

   Untuk mengatasi hal ini, kedua cabang diproyeksikan ke dimensi yang sama (`PROJ_DIM = 256`) melalui lapisan proyeksi:

   $$\mathbf{h}_{spatial} = \text{ReLU}\left(\text{BN}\left(\mathbf{W}_s \cdot \mathbf{f}_{spatial} + \mathbf{b}_s\right)\right) \tag{3.22}$$
   $$\mathbf{h}_{freq} = \text{ReLU}\left(\text{BN}\left(\mathbf{W}_f \cdot \mathbf{f}_{freq} + \mathbf{b}_f\right)\right) \tag{3.23}$$

   di mana $\mathbf{W}_s \in \mathbb{R}^{256 \times 2048}$ dan $\mathbf{W}_f \in \mathbb{R}^{256 \times 256}$ adalah matriks bobot proyeksi, BN adalah *batch normalization* 1D, dan ReLU adalah fungsi aktivasi. Setelah proyeksi, kedua cabang memiliki representasi berdimensi sama (256) yang dapat digabungkan secara seimbang.

4. **Squeeze-and-Excitation (SE) Gating**

   Setelah kedua vektor fitur terproyeksi digabungkan melalui konkatenasi ($\mathbf{h}_{fused} = [\mathbf{h}_{spatial}; \mathbf{h}_{freq}] \in \mathbb{R}^{512}$, diterapkan mekanisme *Squeeze-and-Excitation* (SE) *gating* [42] yang memungkinkan model mempelajari bobot kepentingan per dimensi fitur secara adaptif. Arsitektur SE *gate* terdiri dari:

   a. *Squeeze*, kompresi vektor fusi dari 512 dimensi ke 128 dimensi melalui transformasi linier, diikuti aktivasi ReLU.
   b. *Excitation*, ekspansi kembali ke 512 dimensi melalui transformasi linier, diikuti fungsi *sigmoid* yang menghasilkan bobot gerbang (*gate weights*) pada rentang $[0, 1]$.
   c. *Pengalian elemen*, vektor fusi asli dikalikan secara elemen-per-elemen (*element-wise*) dengan bobot gerbang.

   Secara matematis:

   $$\mathbf{g} = \sigma\left(\mathbf{W}_2 \cdot \text{ReLU}\left(\mathbf{W}_1 \cdot \mathbf{h}_{fused} + \mathbf{b}_1\right) + \mathbf{b}_2\right) \tag{3.24}$$
   $$\hat{\mathbf{h}}_{fused} = \mathbf{h}_{fused} \odot \mathbf{g} \tag{3.25}$$

   di mana $\mathbf{W}_1 \in \mathbb{R}^{128 \times 512}$, $\mathbf{W}_2 \in \mathbb{R}^{512 \times 128}$, $\sigma$ adalah fungsi *sigmoid*, dan $\odot$ adalah perkalian elemen. Mekanisme ini memungkinkan model untuk menekan (*suppress*) fitur yang tidak informatif dan memperkuat (*enhance*) fitur yang diskriminatif, baik dari cabang spasial maupun frekuensi, secara adaptif berdasarkan *input*.

5. **Classifier Head**

   Vektor fitur yang telah melalui SE *gating* ($\hat{\mathbf{h}}_{fused} \in \mathbb{R}^{512}$) diteruskan ke kepala klasifikasi (*classifier head*) yang terdiri dari:

   a. *Dropout(0,3)*, regularisasi pada representasi fusi untuk mencegah *overfitting*, dengan tingkat *dropout* yang moderat agar tidak menghilangkan terlalu banyak sinyal pada *dataset* berukuran kecil.
   b. *Linear(512 → 128)*, reduksi dimensi.
   c. *ReLU*, fungsi aktivasi.
   d. *Dropout(0,3)*, regularisasi tambahan.
   e. *Linear(128 → 1)*, menghasilkan satu nilai *logit* untuk klasifikasi biner.

   *Output logit* diproses oleh fungsi *loss* BCEWithLogitsLoss yang secara internal menerapkan fungsi *sigmoid* sebelum menghitung *binary cross-entropy*.

6. **Contoh Perhitungan Late Fusion**

   Berikut ditunjukkan contoh perhitungan *late fusion* yang disederhanakan dengan dimensi kecil untuk ilustrasi.

   a. *Fitur input* (disederhanakan ke 4 dimensi per cabang):

   $$\mathbf{f}_{spatial} = [0{,}2;\ 1{,}2;\ -0{,}3;\ 0{,}5],\quad \mathbf{f}_{freq} = [0{,}4;\ -0{,}1;\ 0{,}7;\ 0{,}2] \tag{3.26}$$

   b. *Proyeksi* ($4 \rightarrow 4$, disederhanakan tanpa BN). Misalkan $\mathbf{W}_s$ dan $\mathbf{W}_f$ adalah matriks identitas, maka:

   $$\mathbf{h}_{spatial} = \text{ReLU}(\mathbf{f}_{spatial}) = [0{,}8;\ 1{,}2;\ 0;\ 0{,}5]$$
   $$\mathbf{h}_{freq} = \text{ReLU}(\mathbf{f}_{freq}) = [0{,}4;\ 0;\ 0{,}7;\ 0{,}2]$$

   c. *Konkatenasi*:

   $$\mathbf{h}_{fused} = [0{,}8;\ 1{,}2;\ 0;\ 0{,}5;\ 0{,}4;\ 0;\ 0{,}7;\ 0{,}2] \in \mathbb{R}^8 \tag{3.27}$$

   d. *SE Gating* ($8 \rightarrow 2 \rightarrow 8$, *reduction* = 4):

   i. *Squeeze*: $\mathbf{s} = \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_{fused})$. Misalkan hasilnya $\mathbf{s} = [1{,}5;\ 0{,}8]$.
   ii. *Excitation*: $\mathbf{g} = \sigma(\mathbf{W}_2 \cdot \mathbf{s})$. Misalkan hasilnya $\mathbf{g} = [0{,}9;\ 0{,}7;\ 0{,}3;\ 0{,}8;\ 0{,}6;\ 0{,}2;\ 0{,}9;\ 0{,}5]$.
   iii. *Gating*:

   $$\hat{\mathbf{h}}_{fused} = \mathbf{h}_{fused} \odot \mathbf{g} = [0{,}72;\ 0{,}84;\ 0;\ 0{,}40;\ 0{,}24;\ 0;\ 0{,}63;\ 0{,}10] \tag{3.28}$$

   Terlihat bahwa SE *gate* menekan dimensi ke-3 dan ke-6 (nilai *gate* rendah: 0,3 dan 0,2) sambil mempertahankan dimensi ke-1 dan ke-7 (nilai *gate* tinggi: 0,9 dan 0,9). Mekanisme ini memungkinkan model untuk secara adaptif memilih fitur yang paling diskriminatif dari kedua cabang.

   e. *Klasifikasi*:

   *Logit*: $z = \mathbf{w}^T \hat{\mathbf{h}}_{fused} + b$. Misalkan $z = 2{,}1$.

   Probabilitas: $p = \sigma(2{,}1) = \frac{1}{1 + e^{-2{,}1}} = 0{,}891$.

   Prediksi: $p > 0{,}5 \Rightarrow \text{fake}$ (label 1).

---

### 3.5.4  Fungsi *Loss*, BCEWithLogitsLoss dengan *Label Smoothing*

Fungsi *loss* yang digunakan adalah *Binary Cross-Entropy with Logits* (BCEWithLogitsLoss), sebagaimana telah dibahas pada BAB II, yang menggabungkan fungsi *sigmoid* dan *binary cross-entropy* dalam satu operasi yang stabil secara numerik:

$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \left[w_p \cdot y_i \cdot \log(\sigma(z_i)) + (1 - y_i) \cdot \log(1 - \sigma(z_i))\right] \tag{3.29}$$

di mana $z_i$ adalah *logit* (*output* model sebelum *sigmoid*), $\sigma(z) = \frac{1}{1 + e^{-z}}$ adalah fungsi *sigmoid*, $y_i$ adalah label target, dan $w_p$ adalah `pos_weight` untuk penyeimbangan kelas.

1. **Penyeimbangan Kelas (pos_weight)**

   Untuk menangani ketidakseimbangan kelas yang dapat terjadi pada pembagian *dataset*, diterapkan *positive class weighting*:

   $$w_p = \frac{n_{neg}}{n_{pos}} \tag{3.30}$$

   di mana $n_{neg}$ dan $n_{pos}$ adalah jumlah sampel kelas negatif (*real*) dan positif (*fake*) dalam set pelatihan. Bobot ini dikalikan pada komponen *loss* untuk sampel positif, sehingga kelas minoritas mendapat pengaruh lebih besar pada pembaruan gradien. Apabila *dataset* seimbang ($n_{neg} = n_{pos}$), maka $w_p = 1$ dan fungsi *loss* menjadi BCEWithLogitsLoss standar.

2. **Label Smoothing**

   *Label smoothing* merupakan teknik regularisasi yang dapat diterapkan untuk mencegah model menjadi terlalu percaya diri (*overconfident*):

   $$y_i' = y_i \times (1 - \alpha) + \alpha \times 0{,}5 \tag{3.31}$$

   Sebagai ilustrasi, dengan $\alpha = 0{,}02$, transformasi ini mengubah label biner menjadi: $0 \rightarrow 0{,}01$ dan $1 \rightarrow 0{,}99$, sehingga model tidak perlu mendorong *logit* ke nilai ekstrem ($\pm \infty$).

   Pada konfigurasi akhir yang digunakan dalam eksperimen ini, *label smoothing* dinonaktifkan ($\alpha = 0$) untuk memaksimalkan sinyal pelatihan pada *dataset* dengan ukuran sampel kecil (mulai dari $n = 100$). Pada *dataset* berukuran kecil, sinyal positif yang terbatas menjadi semakin lemah apabila label di-*smooth*, sehingga model kesulitan membedakan kelas *real* dan *fake*.

3. **Contoh Perhitungan BCEWithLogitsLoss**

   Sebagai ilustrasi, berikut ditunjukkan contoh perhitungan BCEWithLogitsLoss dengan *label smoothing* $\alpha = 0{,}02$ (walaupun pada konfigurasi akhir $\alpha = 0$, contoh ini menunjukkan mekanisme penuh). Misalkan *logit output* model $z = 2{,}5$, label asli $y = 1$ (*fake*), dan $w_p = 1$ (*dataset* seimbang).

   a. *Label Smoothing*:

   $$y_i' = 1 \times (1 - 0{,}02) + 0{,}02 \times 0{,}5 = 0{,}98 + 0{,}01 = 0{,}99 \tag{3.32}$$

   b. *Sigmoid*:

   $$\sigma(2{,}5) = \frac{1}{1 + e^{-2{,}5}} = \frac{1}{1 + 0{,}0821} = \frac{1}{1{,}0821} = 0{,}924 \tag{3.33}$$

   c. *Loss*:

   $$\mathcal{L} = -\left[0{,}99 \cdot \log(0{,}924) + 0{,}01 \cdot \log(1 - 0{,}924)\right] \tag{3.34}$$
   $$= -\left[0{,}99 \times (-0{,}0791) + 0{,}01 \times (-2{,}577)\right]$$
   $$= -\left[-0{,}0783 + (-0{,}0258)\right]$$
   $$= -(-0{,}1041)$$
   $$= 0{,}1041$$

   Nilai *loss* yang rendah (0,1041) menunjukkan bahwa prediksi model (probabilitas 0,924 untuk *fake*) sudah mendekati label target. Pada awal pelatihan, nilai *loss* umumnya jauh lebih tinggi dan menurun seiring konvergensi model.

---

## Catatan Verifikasi

1. **Tidak ada label heading 4 tingkat yang tersisa.** Seluruh sub-heading lama (`2.9.4.1`–`2.9.4.6`, `3.3.2.1`–`3.3.2.5`, `3.3.3.1`–`3.3.3.3`, `3.4.1.1`–`3.4.1.2`, `3.4.2.1`–`3.4.2.2`, `3.4.3.1`–`3.4.3.6`, `3.5.4.1`–`3.5.4.3`) telah diubah menjadi *numbering* `N. **Judul**` di dalam induk 3 tingkatnya.

2. **Kedalaman *numbering* maksimum 3 tingkat.** Struktur terdalam yang muncul adalah `1. → a. → i.` pada sub-bab 3.3.2 (`4. Contoh Perhitungan FFT 2D` → `b. Menghitung F(0,1)` → `i.–iv. Baris x=...`) dan 3.4.1 (`1. Depthwise Separable Convolution` → `b. Konvolusi depthwise separable` → `i.–iii. Depthwise/Pointwise/Total`). Tidak ada daftar yang melebihi tingkat 3.

3. **Semua nomor persamaan dipertahankan** persis seperti PDF: `(2.5)`–`(2.9)` untuk BAB II, dan `(3.1)`–`(3.17)`, `(3.18)`–`(3.21)`, `(3.22)`–`(3.28)`, `(3.29)`–`(3.34)` untuk BAB III. Referensi tabel (`Tabel 3.3`, `Tabel 3.4`, `Tabel 3.5`) dan gambar (`Gambar 3.3`, `Gambar 3.5`) juga dipertahankan.

4. **Sub-bab lain di BAB II/III tidak diubah.** Sub-bab seperti `2.1–2.8`, `2.10–2.21`, `3.1`, `3.2`, `3.3.1`, `3.5.1–3.5.3`, `3.5.5–3.5.9`, `3.6.*`, `3.7.*` tidak perlu diperbaiki karena sudah 3 tingkat dan *numbering*-nya sudah patuh.

5. **Daftar Isi.** TOC saat ini hanya menampilkan sampai 3 tingkat sehingga tidak ada entri `X.Y.Z.N` yang perlu dihapus. Pastikan pengacakan nomor halaman tetap konsisten setelah penggantian isi.
