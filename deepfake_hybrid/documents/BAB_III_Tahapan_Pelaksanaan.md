# BAB III TAHAPAN PELAKSANAAN

## 3.1 Kerangka Tahapan Pelaksanaan

Penelitian ini menggunakan pendekatan kuantitatif eksperimental untuk merancang, mengimplementasikan, dan mengevaluasi model deteksi deepfake berbasis pembelajaran mendalam. Pendekatan tersebut dipilih karena penelitian berfokus pada perbandingan sistematis antara beberapa arsitektur model dalam kondisi yang terkontrol, sehingga setiap perbedaan performa dapat ditelusuri berdasarkan faktor eksperimen yang diuji. Adapun tahapan pelaksanaan penelitian adalah sebagai berikut:

1. Pengumpulan Data

   Tahap awal penelitian adalah pengumpulan dataset video deepfake dari dua sumber benchmark, yaitu FaceForensics++ (FFPP) dan Celeb-DF (CDF). Kedua dataset dipilih karena merupakan standar evaluasi yang umum digunakan dalam penelitian deteksi deepfake dan memiliki karakteristik manipulasi yang berbeda satu sama lain.

2. Analisis Proses

   Pada tahap ini, analisis dilakukan dengan menyusun alur pemrosesan data (*pipeline*) yang menggambarkan langkah-langkah utama mulai dari data mentah hingga hasil evaluasi. Analisis proses mencakup identifikasi label video, ekstraksi frame, pembangkitan representasi domain frekuensi, serta penyusunan format data masukan untuk setiap arsitektur model.

3. Prapemrosesan Data

   Tahap prapemrosesan meliputi ekstraksi frame dari video, *resize* citra ke ukuran 224 x 224 piksel, konversi domain frekuensi menggunakan FFT, pembentukan *split* data train/validation/test pada level video, dan penyimpanan cache FFT untuk efisiensi komputasi.

4. Implementasi Model

   Tahap implementasi dilakukan dengan membangun tiga arsitektur model utama menggunakan PyTorch, yaitu model *spatial* berbasis XceptionNet, model *frequency* berbasis FreqCNN, dan model *hybrid* dua cabang yang menggabungkan keduanya melalui *late fusion*. Seluruh model dilatih menggunakan konfigurasi yang seragam agar hasil perbandingan bersifat adil.

5. Pengujian dan Evaluasi

   Tahap pengujian dilakukan pada dua skenario evaluasi, yaitu *in-dataset* (latih dan uji pada dataset yang sama) dan *cross-dataset* (latih pada satu dataset, uji pada dataset lain). Evaluasi menggunakan metrik *accuracy*, *precision*, *recall*, F1-*score*, dan AUC untuk mengukur kemampuan deteksi dan generalisasi model.

Alur keseluruhan tahapan pelaksanaan penelitian dapat dirangkum sebagai berikut:

**Dataset Video** → **Sampling Video** → **Ekstraksi Frame** → **Pembagian Data (Train/Val/Test)** → **Prapemrosesan (Spasial + FFT)** → **Pelatihan Model (Spatial, Freq, Hybrid)** → **Evaluasi (In-Dataset + Cross-Dataset)** → **Tabel Hasil**

*Catatan: Diagram alir penelitian secara lengkap disajikan pada Lampiran Gambar.*

## 3.2 Dataset dan Sumber Data

### 3.2.1 Dataset FaceForensics++

Dataset pertama yang digunakan adalah FaceForensics++ (FFPP) yang diperkenalkan oleh Rossler dkk. [1]. Dataset ini merupakan salah satu benchmark standar dalam penelitian deteksi deepfake dan tersedia secara publik melalui repositori resmi. Data FFPP ditempatkan pada direktori `dataset/face_forensics` dan mencakup video asli maupun video hasil manipulasi.

Kategori manipulasi yang digunakan pada penelitian ini meliputi:

1. *Deepfakes* — penggantian wajah menggunakan *autoencoder*.
2. *Face2Face* — transfer ekspresi wajah secara *real-time*.
3. *FaceSwap* — pertukaran wajah berbasis *landmark*.
4. *NeuralTextures* — manipulasi tekstur wajah menggunakan jaringan saraf.

Video asli berasal dari koleksi `original_sequences` yang mencakup aktor dan video YouTube. FaceForensics++ dipilih karena menyediakan variasi teknik manipulasi yang beragam, sehingga model dapat diuji terhadap berbagai jenis artefak deepfake.

### 3.2.2 Dataset Celeb-DF

Dataset kedua yang digunakan adalah Celeb-DF versi 2 (CDF) yang ditempatkan pada direktori `dataset/celeb_df`. Dataset ini memuat tiga kategori:

1. `Celeb-real` — video wajah asli selebritas.
2. `YouTube-real` — video wajah asli dari YouTube.
3. `Celeb-synthesis` — video wajah hasil sintesis deepfake.

Celeb-DF dipilih untuk melengkapi pengujian dengan dataset yang memiliki karakteristik manipulasi dan distribusi visual yang berbeda dari FaceForensics++. Penggunaan dua dataset memungkinkan evaluasi yang lebih kuat terhadap kemampuan generalisasi model melalui skenario *cross-dataset*.

### 3.2.3 Unit Analisis dan Pembagian Data

Unit analisis pada penelitian ini dibedakan menjadi dua tingkat:

1. **Tingkat video** digunakan untuk pembentukan *split* data train, validation, dan test. Dengan demikian, seluruh frame dari satu video hanya berada pada satu subset data sehingga kebocoran data (*data leakage*) antarsubset dapat dihindari.
2. **Tingkat frame** digunakan sebagai unit input model selama pelatihan dan pengujian. Setiap video yang lolos seleksi diekstraksi menjadi sejumlah frame, yang kemudian diperlakukan sebagai sampel citra individual.

Pembagian data dilakukan secara *stratified* berdasarkan label (real/fake) dengan rasio sebagai berikut:

Tabel 3.1 Rasio Pembagian Data

| Subset | Proporsi |
| --- | --- |
| Train | 70% |
| Validation | 15% |
| Test | 15% |

Untuk menguji pengaruh ukuran sampel pelatihan, eksperimen dijalankan dengan tiga variasi jumlah video per dataset:

Tabel 3.2 Variasi Ukuran Sampel Eksperimen

| Kode | Jumlah Video per Dataset | Tujuan |
| --- | --- | --- |
| n=50 | 50 video | Skenario data kecil |
| n=200 | 200 video | Skenario data menengah |
| n=400 | 400 video | Skenario data besar |

Sampling dilakukan secara *balanced* antara kelas real dan fake menggunakan *seed* deterministik (seed = 42) agar proses dapat direplikasi.

### 3.2.4 Identifikasi Label Video

Label video tidak dibaca dari anotasi eksternal, melainkan diinferensi secara otomatis dari nama folder dan nama file menggunakan daftar kata kunci (*keywords*) yang didefinisikan pada file konfigurasi.

Tabel 3.3 Kata Kunci Identifikasi Label

| Dataset | Label Real | Label Fake |
| --- | --- | --- |
| FFPP | original, real, pristine, actors, youtube | fake, manipulated, deepfakes, faceswap, neuraltextures, faceshifter, face2face |
| CDF | real, authentic, youtube | fake, synthesis, deepfake |

Pendekatan ini sesuai dengan struktur folder pada kedua dataset dan memungkinkan proses penandaan label dilakukan secara otomatis tanpa intervensi manual.

## 3.3 Analisis Proses

Bagian ini menjelaskan tahapan pemrosesan data secara berurutan, mulai dari data video mentah hingga tensor masukan yang siap diproses oleh model. Setiap tahap disertai penjelasan prosedur dan contoh perhitungan manual untuk memperjelas mekanisme kerja algoritma.

### 3.3.1 Ekstraksi Frame dari Video

Setiap video dibaca menggunakan OpenCV dan diambil frame pada laju 5 frame per detik (fps). Jumlah frame maksimum per video ditetapkan sebesar 100 frame untuk eksperimen utama. Jika jumlah frame yang tersedia melebihi batas, frame dipilih secara acak dengan *seed* tetap.

Setiap frame disimpan dalam format JPG dengan pola nama `frame_000000.jpg`, `frame_000001.jpg`, dan seterusnya. Seluruh frame dari satu video dikelompokkan ke dalam satu folder dengan nama `video_id`. Hasil ekstraksi dicatat pada sebuah *manifest* awal yang berisi tiga kolom: `video_id`, `label`, dan `frames_dir`.

### 3.3.2 Prapemrosesan Domain Spasial

Frame RGB yang digunakan oleh model *spatial* dan cabang spasial pada model *hybrid* diproses menggunakan transformasi citra sebagai berikut.

**Pada fase pelatihan:**

1. *Resize* ke ukuran 256 x 256 piksel (yaitu 224 + 32).
2. *RandomResizedCrop* ke ukuran 224 x 224 piksel dengan rentang skala 0,8 sampai 1,0.
3. *RandomHorizontalFlip* dengan probabilitas 0,5.
4. Konversi ke tensor float [0, 1].
5. Normalisasi menggunakan rata-rata dan deviasi standar ImageNet.

**Pada fase validasi dan pengujian:**

1. *Resize* langsung ke ukuran 224 x 224 piksel.
2. Konversi ke tensor float [0, 1].
3. Normalisasi menggunakan parameter ImageNet.

Parameter normalisasi ImageNet yang digunakan:

$$
\mu = [0{,}485;\; 0{,}456;\; 0{,}406] \quad \sigma = [0{,}229;\; 0{,}224;\; 0{,}225]
$$ ............(3.1)

Normalisasi diterapkan per kanal dengan formula:

$$
\hat{x}_c = \frac{x_c - \mu_c}{\sigma_c}
$$ ............(3.2)

Dimana:
- $x_c$ = nilai piksel pada kanal $c$ setelah konversi ke [0, 1]
- $\mu_c$ = rata-rata ImageNet untuk kanal $c$
- $\sigma_c$ = deviasi standar ImageNet untuk kanal $c$

**Contoh perhitungan normalisasi:**

Misalkan suatu piksel memiliki nilai RGB = (120, 200, 80). Setelah konversi ke [0, 1]:

$$
x_R = \frac{120}{255} = 0{,}471 \quad x_G = \frac{200}{255} = 0{,}784 \quad x_B = \frac{80}{255} = 0{,}314
$$

Normalisasi per kanal:

$$
\hat{x}_R = \frac{0{,}471 - 0{,}485}{0{,}229} = \frac{-0{,}014}{0{,}229} = -0{,}061
$$

$$
\hat{x}_G = \frac{0{,}784 - 0{,}456}{0{,}224} = \frac{0{,}328}{0{,}224} = 1{,}464
$$

$$
\hat{x}_B = \frac{0{,}314 - 0{,}406}{0{,}225} = \frac{-0{,}092}{0{,}225} = -0{,}409
$$

Hasil normalisasi: $(\hat{x}_R, \hat{x}_G, \hat{x}_B) = (-0{,}061;\; 1{,}464;\; -0{,}409)$.

### 3.3.3 Prapemrosesan Domain Frekuensi dengan FFT

Representasi domain frekuensi dibangkitkan dari setiap frame melalui prosedur berikut:

1. Konversi citra RGB ke *grayscale*.
2. *Resize* citra *grayscale* ke ukuran 224 x 224 piksel.
3. Hitung transformasi Fourier dua dimensi (*FFT2D*).
4. Pindahkan komponen frekuensi rendah ke pusat spektrum (*fftshift*).
5. Hitung *magnitude spectrum* dengan operasi nilai absolut.
6. Kompres *dynamic range* menggunakan logaritma $\log(1 + x)$.
7. Normalisasi nilai ke rentang [0, 1].

Secara matematis, representasi frekuensi *log-magnitude* dituliskan sebagai berikut:

$$
F(u,v) = \log\left(1 + \left|\text{fftshift}\left(\text{FFT2D}(I_g)\right)\right|\right)
$$ ............(3.3)

Dimana:
- $I_g$ = citra *grayscale* berukuran $N \times N$ dari frame masukan
- $\text{FFT2D}$ = transformasi Fourier diskret dua dimensi
- $\text{fftshift}$ = operasi pemindahan kuadran untuk menempatkan frekuensi rendah di pusat
- $|\cdot|$ = operasi *magnitude* (nilai absolut bilangan kompleks)

Normalisasi akhir ke rentang [0, 1]:

$$
\hat{F}(u,v) = \frac{F(u,v) - F_{\min}}{F_{\max} - F_{\min} + \epsilon}
$$ ............(3.4)

Dimana $\epsilon = 10^{-8}$ digunakan untuk menghindari pembagian dengan nol.

Hasil FFT setiap frame disimpan ke dalam file `.npy` pada folder `outputs/fft_cache/` agar representasi frekuensi tidak perlu dihitung ulang setiap kali pelatihan dijalankan.

#### 3.3.3.1 Contoh Perhitungan Manual FFT 2D

Untuk mengilustrasikan proses konversi domain frekuensi, berikut disajikan contoh perhitungan manual menggunakan matriks *grayscale* berukuran 4 x 4 piksel.

**Langkah 1 — Konversi RGB ke Grayscale**

Konversi menggunakan formula luminansi standar:

$$
Y = 0{,}299 \cdot R + 0{,}587 \cdot G + 0{,}114 \cdot B
$$ ............(3.5)

Misalkan empat piksel pada baris pertama memiliki nilai RGB sebagai berikut:

Tabel 3.4 Contoh Konversi RGB ke Grayscale

| Piksel | R | G | B | Y (grayscale) |
| --- | --- | --- | --- | --- |
| (0,0) | 180 | 160 | 140 | $0{,}299(180) + 0{,}587(160) + 0{,}114(140) = 163{,}7$ |
| (0,1) | 50 | 60 | 70 | $0{,}299(50) + 0{,}587(60) + 0{,}114(70) = 58{,}15$ |
| (0,2) | 200 | 190 | 180 | $0{,}299(200) + 0{,}587(190) + 0{,}114(180) = 192{,}05$ |
| (0,3) | 30 | 40 | 50 | $0{,}299(30) + 0{,}587(40) + 0{,}114(50) = 38{,}15$ |

Setelah konversi seluruh piksel, diperoleh matriks *grayscale* $I_g$ berukuran 4 x 4 (dibulatkan):

$$
I_g = \begin{bmatrix} 164 & 58 & 192 & 38 \\ 100 & 130 & 80 & 170 \\ 210 & 45 & 155 & 90 \\ 70 & 185 & 60 & 140 \end{bmatrix}
$$

**Langkah 2 — Transformasi Fourier Diskret 2D**

DFT 2D didefinisikan sebagai:

$$
X(u,v) = \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} x(m,n) \cdot e^{-j2\pi\left(\frac{um}{M} + \frac{vn}{N}\right)}
$$ ............(3.6)

Dimana:
- $x(m,n)$ = nilai piksel pada posisi $(m,n)$
- $M, N$ = dimensi matriks (dalam contoh ini $M = N = 4$)
- $u, v$ = koordinat frekuensi
- $j$ = unit imajiner ($j^2 = -1$)

Perhitungan komponen DC (frekuensi nol), $X(0,0)$:

$$
X(0,0) = \sum_{m=0}^{3} \sum_{n=0}^{3} x(m,n) \cdot e^{0} = \sum_{m=0}^{3} \sum_{n=0}^{3} x(m,n)
$$

$$
X(0,0) = (164 + 58 + 192 + 38) + (100 + 130 + 80 + 170)
$$

$$
\quad\quad\quad + (210 + 45 + 155 + 90) + (70 + 185 + 60 + 140)
$$

$$
X(0,0) = 452 + 480 + 500 + 455 = 1887
$$

Komponen DC merepresentasikan jumlah total intensitas piksel. Untuk komponen frekuensi lain, misalnya $X(1,0)$, faktor eksponensial $e^{-j2\pi \frac{m}{4}}$ menghasilkan rotasi pada bidang kompleks dengan nilai $\{1, -j, -1, j\}$ untuk $m = \{0, 1, 2, 3\}$:

$$
X(1,0) = \sum_{n=0}^{3} \left[ x(0,n) \cdot 1 + x(1,n) \cdot (-j) + x(2,n) \cdot (-1) + x(3,n) \cdot j \right]
$$

$$
= (452) \cdot 1 + (480) \cdot (-j) + (500) \cdot (-1) + (455) \cdot j
$$

$$
= 452 - 500 + j(-480 + 455) = -48 - 25j
$$

**Langkah 3 — FFT Shift**

Setelah FFT2D, komponen frekuensi rendah berada pada sudut matriks. Operasi *fftshift* menukar kuadran sehingga komponen DC ($X(0,0)$) berpindah ke pusat matriks. Pada matriks 4 x 4, ini dilakukan dengan menukar kuadran secara diagonal:

$$
\text{Sebelum: } \begin{bmatrix} Q_1 & Q_2 \\ Q_3 & Q_4 \end{bmatrix} \quad \rightarrow \quad \text{Sesudah: } \begin{bmatrix} Q_4 & Q_3 \\ Q_2 & Q_1 \end{bmatrix}
$$

**Langkah 4 — Magnitude Spectrum**

Untuk setiap elemen kompleks $X(u,v) = a + bj$, *magnitude* dihitung sebagai:

$$
|X(u,v)| = \sqrt{a^2 + b^2}
$$ ............(3.7)

Dari contoh $X(1,0) = -48 - 25j$:

$$
|X(1,0)| = \sqrt{(-48)^2 + (-25)^2} = \sqrt{2304 + 625} = \sqrt{2929} \approx 54{,}12
$$

**Langkah 5 — Log Scaling**

Kompresi *dynamic range* menggunakan $\log(1+x)$:

$$
F(1,0) = \log(1 + 54{,}12) = \log(55{,}12) \approx 4{,}01
$$ ............(3.8)

Untuk komponen DC:

$$
F(0,0) = \log(1 + 1887) = \log(1888) \approx 7{,}54
$$

**Langkah 6 — Normalisasi ke [0, 1]**

Seluruh nilai $F(u,v)$ dinormalisasi dengan Persamaan (3.4). Jika $F_{\min} = 0{,}0$ dan $F_{\max} = 7{,}54$, maka:

$$
\hat{F}(1,0) = \frac{4{,}01 - 0{,}0}{7{,}54 - 0{,}0} \approx 0{,}532
$$

$$
\hat{F}(0,0) = \frac{7{,}54 - 0{,}0}{7{,}54 - 0{,}0} = 1{,}000
$$

Hasil akhir berupa matriks satu kanal dengan nilai dalam rentang [0, 1] yang siap digunakan sebagai input model frekuensi.

### 3.3.4 Prapemrosesan FFT untuk Data Loader

Saat data dimuat ke dalam *data loader*, representasi FFT yang telah dicache mengalami interpolasi bilinear ke ukuran 224 x 224 piksel untuk menjamin konsistensi dimensi. Pada fase pelatihan, transformasi tambahan yang diterapkan pada data FFT adalah:

1. *Resize* ke 256 x 256 piksel.
2. *CenterCrop* ke 224 x 224 piksel.

Berbeda dengan prapemrosesan spasial yang menggunakan *RandomResizedCrop*, prapemrosesan FFT menggunakan *CenterCrop* karena representasi frekuensi bersifat simetris terhadap pusat dan pemotongan acak dapat menghilangkan informasi frekuensi rendah yang terletak di tengah spektrum.

### 3.3.5 Penyusunan Data untuk Model

Format data yang diberikan ke model bergantung pada mode eksperimen:

Tabel 3.5 Format Data Masukan per Mode Model

| Mode | Input ke Model | Dimensi |
| --- | --- | --- |
| *spatial* | Tensor RGB 3 kanal | $(3, 224, 224)$ |
| *freq* | Tensor FFT *magnitude* 1 kanal | $(1, 224, 224)$ |
| *hybrid* | Dua tensor terpisah: RGB + FFT | $(3, 224, 224)$ dan $(1, 224, 224)$ |
| *early_fusion* | Tensor gabungan RGB + FFT 4 kanal | $(4, 224, 224)$ |

Eksperimen utama berfokus pada tiga model inti: *spatial*, *freq*, dan *hybrid*.

## 3.4 Arsitektur Model

### 3.4.1 Model Spatial Berbasis XceptionNet

Model *spatial* menggunakan *backbone* XceptionNet yang diakses melalui pustaka `timm`. XceptionNet dibangun di atas konsep *depthwise separable convolution* yang memisahkan konvolusi spasial dan konvolusi lintas kanal, sehingga lebih efisien secara parameter dibandingkan konvolusi standar.

Model ini dikonfigurasi dengan satu neuron output untuk klasifikasi biner, menerima input tiga kanal RGB, dan menggunakan *global average pooling* untuk merangkum representasi fitur sebelum klasifikasi. Bobot awal menggunakan *pretrained* ImageNet.

Dimensi vektor fitur yang dihasilkan XceptionNet sebelum lapisan klasifikasi adalah **2048**.

#### 3.4.1.1 Contoh Perhitungan Depthwise Separable Convolution

*Depthwise separable convolution* terdiri atas dua tahap: *depthwise convolution* dan *pointwise convolution*.

**Tahap 1 — Depthwise Convolution**

Pada *depthwise convolution*, setiap kanal input dikonvolusi secara terpisah dengan *kernel* tersendiri. Misalkan terdapat input 3 kanal berukuran 3 x 3:

$$
X_1 = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 1 & 2 \\ 0 & 1 & 3 \end{bmatrix} \quad
X_2 = \begin{bmatrix} 2 & 0 & 1 \\ 1 & 3 & 0 \\ 2 & 1 & 1 \end{bmatrix} \quad
X_3 = \begin{bmatrix} 0 & 1 & 2 \\ 2 & 0 & 3 \\ 1 & 2 & 0 \end{bmatrix}
$$

Dengan *kernel* 2 x 2 per kanal:

$$
K_1 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \quad
K_2 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} \quad
K_3 = \begin{bmatrix} 1 & 1 \\ 0 & 0 \end{bmatrix}
$$

Konvolusi pada posisi (0,0) untuk kanal 1:

$$
Y_1(0,0) = 1 \cdot 1 + 2 \cdot 0 + 3 \cdot 0 + 1 \cdot 1 = 2
$$

Masing-masing kanal menghasilkan satu *feature map* berukuran 2 x 2 (3 *kernel* untuk 3 kanal = **3 parameter set**).

**Tahap 2 — Pointwise Convolution**

Setelah *depthwise convolution* menghasilkan 3 *feature map*, *pointwise convolution* (Conv 1x1) menggabungkannya menjadi jumlah kanal output yang diinginkan. Jika output yang diinginkan adalah 2 kanal, maka terdapat 2 *kernel* berukuran 1 x 1 x 3:

$$
W_1 = [w_{11}, w_{12}, w_{13}] = [0{,}5;\; 0{,}3;\; 0{,}2]
$$

Untuk posisi (0,0):

$$
Z_1(0,0) = 0{,}5 \cdot Y_1(0,0) + 0{,}3 \cdot Y_2(0,0) + 0{,}2 \cdot Y_3(0,0)
$$

**Perbandingan parameter:**

Tabel 3.6 Perbandingan Jumlah Parameter Konvolusi

| Jenis Konvolusi | Formula | Contoh (3 input, 2 output, kernel 2x2) | Jumlah |
| --- | --- | --- | --- |
| Konvolusi standar | $C_{in} \times C_{out} \times K^2$ | $3 \times 2 \times 4$ | 24 |
| *Depthwise separable* | $C_{in} \times K^2 + C_{in} \times C_{out}$ | $3 \times 4 + 3 \times 2$ | 18 |

Penghematan parameter ini menjadi signifikan pada jaringan dalam seperti XceptionNet yang memiliki puluhan lapisan konvolusi.

### 3.4.2 Model Frequency CNN (FreqCNN)

Model *freq* dirancang sebagai CNN ringan satu kanal yang menerima peta FFT *log-magnitude*. Arsitektur utamanya terdiri atas tiga blok ekstraksi fitur konvolusional dan satu blok *classifier*.

Tabel 3.7 Arsitektur FreqCNN Layer-by-Layer

| No | Layer | Parameter | Output |
| --- | --- | --- | --- |
| 1 | Conv2d(1, 16, kernel=3, padding=1) | $1 \times 16 \times 3 \times 3 = 144$ | $(16, 224, 224)$ |
| 2 | BatchNorm2d(16) + ReLU | 32 | $(16, 224, 224)$ |
| 3 | MaxPool2d(2) | — | $(16, 112, 112)$ |
| 4 | Conv2d(16, 32, kernel=3, padding=1) | $16 \times 32 \times 3 \times 3 = 4.608$ | $(32, 112, 112)$ |
| 5 | BatchNorm2d(32) + ReLU | 64 | $(32, 112, 112)$ |
| 6 | MaxPool2d(2) | — | $(32, 56, 56)$ |
| 7 | Conv2d(32, 64, kernel=3, padding=1) | $32 \times 64 \times 3 \times 3 = 18.432$ | $(64, 56, 56)$ |
| 8 | BatchNorm2d(64) + ReLU | 128 | $(64, 56, 56)$ |
| 9 | AdaptiveAvgPool2d(1,1) | — | $(64, 1, 1)$ |
| 10 | Flatten | — | $(64)$ |
| 11 | Linear(64, 64) + ReLU | 4.160 | $(64)$ |
| 12 | Dropout(0,2) | — | $(64)$ |
| 13 | Linear(64, 1) | 65 | $(1)$ |

Dimensi vektor fitur yang dihasilkan FreqCNN (setelah layer 9) adalah **64**.

#### 3.4.2.1 Contoh Perhitungan Forward Pass FreqCNN

Misalkan input FFT berukuran 4 x 4 (disederhanakan dari 224 x 224) dengan 1 kanal:

$$
X = \begin{bmatrix} 0{,}9 & 0{,}3 & 0{,}7 & 0{,}1 \\ 0{,}4 & 0{,}8 & 0{,}2 & 0{,}6 \\ 0{,}5 & 0{,}1 & 0{,}9 & 0{,}3 \\ 0{,}2 & 0{,}7 & 0{,}4 & 0{,}8 \end{bmatrix}
$$

**Conv2d(1, 2, kernel=3, padding=1)** — dua filter 3x3 diterapkan pada input. Dengan *padding*=1, output tetap berukuran 4 x 4 namun memiliki 2 kanal.

Misalkan filter pertama $K_1$:

$$
K_1 = \begin{bmatrix} 0{,}1 & -0{,}2 & 0{,}1 \\ 0{,}3 & 0{,}5 & -0{,}1 \\ -0{,}1 & 0{,}2 & 0{,}3 \end{bmatrix}
$$

Konvolusi pada posisi (1,1) (tanpa *padding*):

$$
Y_1(1,1) = 0{,}1(0{,}9) + (-0{,}2)(0{,}3) + 0{,}1(0{,}7)
$$

$$
\quad + 0{,}3(0{,}4) + 0{,}5(0{,}8) + (-0{,}1)(0{,}2)
$$

$$
\quad + (-0{,}1)(0{,}5) + 0{,}2(0{,}1) + 0{,}3(0{,}9)
$$

$$
= 0{,}09 - 0{,}06 + 0{,}07 + 0{,}12 + 0{,}40 - 0{,}02 - 0{,}05 + 0{,}02 + 0{,}27 = 0{,}84
$$

**BatchNorm + ReLU:** Nilai 0,84 > 0 sehingga ReLU tidak mengubahnya.

**MaxPool2d(2):** Mengambil nilai maksimum dari setiap region 2x2, menghasilkan ukuran output yang tereduksi setengah.

**AdaptiveAvgPool2d(1,1):** Menghitung rata-rata seluruh *feature map* per kanal, menghasilkan vektor fitur berdimensi sama dengan jumlah kanal terakhir (64).

### 3.4.3 Model Hybrid Dua Cabang (HybridTwoBranch)

Model *hybrid* merupakan arsitektur utama yang diusulkan dalam penelitian ini. Model ini menggunakan dua cabang yang berjalan paralel:

1. **Cabang spasial** menggunakan XceptionNet sebagai *feature extractor* (tanpa lapisan klasifikasi akhir), menghasilkan vektor fitur spasial berdimensi **2048**.
2. **Cabang frekuensi** menggunakan bagian *feature extractor* dari FreqCNN (layer 1–9), menghasilkan vektor fitur frekuensi berdimensi **64**.

Kedua vektor fitur digabungkan melalui operasi *concatenation* menjadi vektor berdimensi **2112** (= 2048 + 64), kemudian diteruskan ke *classifier* akhir:

1. Linear(2112, 256) + ReLU.
2. Dropout(0,3).
3. Linear(256, 1).

Tabel 3.8 Arsitektur Classifier Hybrid

| No | Layer | Dimensi Input | Dimensi Output |
| --- | --- | --- | --- |
| 1 | Concatenation | (2048) + (64) | (2112) |
| 2 | Linear + ReLU | (2112) | (256) |
| 3 | Dropout(0,3) | (256) | (256) |
| 4 | Linear | (256) | (1) |

#### 3.4.3.1 Contoh Perhitungan Late Fusion

Untuk mengilustrasikan proses *late fusion*, berikut contoh perhitungan dengan dimensi yang disederhanakan.

Misalkan output cabang spasial $\mathbf{f}_s = [0{,}8;\; 0{,}3;\; -0{,}5;\; 1{,}2]$ (4 dimensi) dan output cabang frekuensi $\mathbf{f}_f = [0{,}6;\; -0{,}2]$ (2 dimensi).

**Langkah 1 — Concatenation:**

$$
\mathbf{f}_{fused} = [\mathbf{f}_s \| \mathbf{f}_f] = [0{,}8;\; 0{,}3;\; -0{,}5;\; 1{,}2;\; 0{,}6;\; -0{,}2]
$$ ............(3.9)

Vektor gabungan berdimensi 6 (= 4 + 2).

**Langkah 2 — Linear Layer:**

Misalkan bobot $\mathbf{W} \in \mathbb{R}^{3 \times 6}$ dan bias $\mathbf{b} \in \mathbb{R}^{3}$:

$$
\mathbf{z} = \mathbf{W} \cdot \mathbf{f}_{fused} + \mathbf{b}
$$ ............(3.10)

Untuk neuron pertama dengan $\mathbf{w}_1 = [0{,}2;\; -0{,}1;\; 0{,}3;\; 0{,}4;\; -0{,}2;\; 0{,}1]$ dan $b_1 = 0{,}05$:

$$
z_1 = 0{,}2(0{,}8) + (-0{,}1)(0{,}3) + 0{,}3(-0{,}5) + 0{,}4(1{,}2) + (-0{,}2)(0{,}6) + 0{,}1(-0{,}2) + 0{,}05
$$

$$
= 0{,}16 - 0{,}03 - 0{,}15 + 0{,}48 - 0{,}12 - 0{,}02 + 0{,}05 = 0{,}37
$$

**Langkah 3 — ReLU:** $\text{ReLU}(0{,}37) = \max(0, 0{,}37) = 0{,}37$

**Langkah 4 — Linear(3, 1)** menghasilkan satu *logit* $z$ yang kemudian dikonversi ke probabilitas menggunakan sigmoid:

$$
p = \sigma(z) = \frac{1}{1 + e^{-z}}
$$ ............(3.11)

Jika $z = 0{,}82$:

$$
p = \frac{1}{1 + e^{-0{,}82}} = \frac{1}{1 + 0{,}440} = \frac{1}{1{,}440} = 0{,}694
$$

Prediksi: $p = 0{,}694 > 0{,}5$ → **fake** (label 1).

### 3.4.4 Variasi Early Fusion

Sebagai variasi tambahan, repositori juga menyediakan model *early_fusion* yang menggunakan XceptionNet dengan 4 kanal input (RGB + FFT). Arsitektur ini menggabungkan informasi spasial dan frekuensi sejak lapisan pertama, berbeda dengan model *hybrid* yang menggabungkan fitur di lapisan akhir. Meskipun variasi ini tersedia, tabel hasil utama pada penelitian ini berfokus pada tiga model inti: *spatial*, *freq*, dan *hybrid*.

Tabel 3.9 Perbandingan Arsitektur Model

| Model | Input | Backbone | Strategi Fusi | Dimensi Fitur |
| --- | --- | --- | --- | --- |
| *spatial* | RGB $(3, 224, 224)$ | XceptionNet (*pretrained*) | — | 2048 |
| *freq* | FFT $(1, 224, 224)$ | FreqCNN (3 conv) | — | 64 |
| *hybrid* | RGB + FFT terpisah | XceptionNet + FreqCNN | *Late fusion* (concat) | 2048 + 64 = 2112 |
| *early_fusion* | RGB+FFT $(4, 224, 224)$ | XceptionNet 4-ch | *Early fusion* (channel stack) | 2048 |

## 3.5 Strategi Pelatihan Model

### 3.5.1 Transfer Learning

Model *spatial* dan cabang spasial pada model *hybrid* menggunakan bobot awal (*pretrained*) dari ImageNet. Seluruh parameter *backbone* XceptionNet **tidak dibekukan** dan ikut diperbarui selama pelatihan (*fine-tuning*). Strategi ini dipilih agar model dapat menyesuaikan representasi fitur yang telah dipelajari dari ImageNet terhadap karakteristik spesifik citra deepfake.

### 3.5.2 Konfigurasi Pelatihan

Tabel 3.10 Parameter Pelatihan

| Parameter | Nilai |
| --- | --- |
| *Optimizer* | Adam |
| *Learning rate* | $1 \times 10^{-4}$ |
| *Weight decay* | $1 \times 10^{-4}$ |
| Fungsi *loss* | BCEWithLogitsLoss |
| *Batch size* | 16 |
| Jumlah *epoch* | 10 |
| *Gradient accumulation* | 2 langkah (hybrid, early_fusion); 1 langkah (spatial, freq) |
| *Mixed precision* | Aktif pada perangkat CUDA |
| *Seed* deterministik | 42 |
| *Framework* | PyTorch |
| *Backbone library* | timm |

Pelatihan dijalankan tanpa *learning rate scheduler* dan tanpa *early stopping*. Model dilatih selama jumlah *epoch* penuh yang ditetapkan, dan *checkpoint* terbaik dipilih berdasarkan kriteria yang dijelaskan pada Subbab 3.5.3.

### 3.5.3 Pemilihan Checkpoint Terbaik

Pada akhir setiap *epoch*, model dievaluasi menggunakan *validation set*. Nilai *validation* AUC menjadi dasar pemilihan *checkpoint* terbaik. Jika AUC pada *epoch* saat ini lebih tinggi daripada AUC terbaik sebelumnya, bobot model disimpan sebagai `best.pt`.

Pemilihan *checkpoint* berdasarkan AUC lebih tepat dibandingkan akurasi karena AUC mempertimbangkan kualitas pemisahan kelas secara menyeluruh dan lebih tahan terhadap perubahan *threshold* klasifikasi.

### 3.5.4 Fungsi Loss — BCEWithLogitsLoss

Fungsi *loss* yang digunakan adalah *Binary Cross-Entropy with Logits*, yang menggabungkan lapisan sigmoid dan *binary cross-entropy* dalam satu operasi yang stabil secara numerik.

Untuk sebuah *logit* $z$ dan label target $y \in \{0, 1\}$:

$$
\mathcal{L}(z, y) = -\left[y \cdot \log(\sigma(z)) + (1 - y) \cdot \log(1 - \sigma(z))\right]
$$ ............(3.12)

Dimana $\sigma(z) = \frac{1}{1 + e^{-z}}$ adalah fungsi sigmoid.

#### 3.5.4.1 Contoh Perhitungan Loss

Misalkan model menghasilkan *logit* $z = 1{,}5$ untuk sebuah frame deepfake (*fake*, $y = 1$):

$$
\sigma(1{,}5) = \frac{1}{1 + e^{-1{,}5}} = \frac{1}{1 + 0{,}223} = 0{,}818
$$

$$
\mathcal{L} = -\left[1 \cdot \log(0{,}818) + 0 \cdot \log(1 - 0{,}818)\right] = -\log(0{,}818) = 0{,}201
$$

Untuk frame asli (*real*, $y = 0$) dengan *logit* $z = -0{,}8$:

$$
\sigma(-0{,}8) = \frac{1}{1 + e^{0{,}8}} = \frac{1}{1 + 2{,}226} = 0{,}310
$$

$$
\mathcal{L} = -\left[0 \cdot \log(0{,}310) + 1 \cdot \log(1 - 0{,}310)\right] = -\log(0{,}690) = 0{,}371
$$

Rata-rata *loss* dari kedua sampel:

$$
\mathcal{L}_{\text{avg}} = \frac{0{,}201 + 0{,}371}{2} = 0{,}286
$$

## 3.6 Rancangan Eksperimen

### 3.6.1 Matriks Eksperimen

Eksperimen utama membandingkan tiga arsitektur model pada dua dataset dengan tiga ukuran sampel dan dua skenario evaluasi.

Tabel 3.11 Matriks Eksperimen Utama

| Komponen | Variasi |
| --- | --- |
| Model | *spatial*, *freq*, *hybrid* |
| Dataset latih | FFPP, CDF |
| Ukuran sampel | n = 50, n = 200, n = 400 |
| Jenis evaluasi | *In-dataset*, *cross-dataset* |

Jumlah total skenario evaluasi: 3 model x 2 dataset latih x 3 ukuran sampel x 2 jenis evaluasi = **36 skenario**.

### 3.6.2 Tabel Perlakuan Eksperimen

Tabel 3.12 Perlakuan Eksperimen

| Kode | Model | Dataset Latih | Dataset Uji | Ukuran Sampel | Tujuan |
| --- | --- | --- | --- | --- | --- |
| E1 | *spatial* | FFPP | FFPP | 50, 200, 400 | Performa *in-dataset* model spasial |
| E2 | *freq* | FFPP | FFPP | 50, 200, 400 | Performa *in-dataset* model frekuensi |
| E3 | *hybrid* | FFPP | FFPP | 50, 200, 400 | Performa *in-dataset* model hibrida |
| E4 | *spatial* | CDF | CDF | 50, 200, 400 | Performa *in-dataset* model spasial |
| E5 | *freq* | CDF | CDF | 50, 200, 400 | Performa *in-dataset* model frekuensi |
| E6 | *hybrid* | CDF | CDF | 50, 200, 400 | Performa *in-dataset* model hibrida |
| E7 | *spatial* | FFPP | CDF | 50, 200, 400 | Generalisasi FFPP → CDF |
| E8 | *freq* | FFPP | CDF | 50, 200, 400 | Generalisasi FFPP → CDF |
| E9 | *hybrid* | FFPP | CDF | 50, 200, 400 | Generalisasi FFPP → CDF |
| E10 | *spatial* | CDF | FFPP | 50, 200, 400 | Generalisasi CDF → FFPP |
| E11 | *freq* | CDF | FFPP | 50, 200, 400 | Generalisasi CDF → FFPP |
| E12 | *hybrid* | CDF | FFPP | 50, 200, 400 | Generalisasi CDF → FFPP |

### 3.6.3 Skenario In-Dataset

Pada skenario *in-dataset*, model dilatih dan diuji pada dataset yang sama (misalnya latih pada FFPP, uji pada subset test FFPP). Tujuan skenario ini adalah mengukur kemampuan model mempelajari pola manipulasi pada distribusi data yang sejenis.

### 3.6.4 Skenario Cross-Dataset

Pada skenario *cross-dataset*, model dilatih pada satu dataset dan diuji pada dataset lain (misalnya latih pada FFPP, uji pada CDF). Skenario ini merepresentasikan kondisi yang lebih realistis ketika model harus menghadapi data dari distribusi yang berbeda dengan data pelatihan.

### 3.6.5 Hipotesis Eksperimen

1. Model *hybrid* memiliki performa *in-dataset* yang lebih baik dibandingkan model *spatial* dan model *freq* karena memanfaatkan dua domain fitur secara simultan.
2. Model yang dilatih pada FFPP cenderung memiliki kemampuan generalisasi yang lebih baik dibandingkan model yang dilatih pada CDF karena FFPP memiliki variasi manipulasi yang lebih beragam.
3. Peningkatan jumlah sampel pelatihan meningkatkan performa *in-dataset*, tetapi belum tentu meningkatkan performa *cross-dataset* secara proporsional.
4. Selisih performa antara pengujian *in-dataset* dan *cross-dataset* menunjukkan adanya sensitivitas model terhadap karakteristik dataset.

## 3.7 Metode Evaluasi

### 3.7.1 Metrik Evaluasi

Setelah pelatihan selesai, *checkpoint* terbaik dievaluasi pada *test set*. Probabilitas prediksi diperoleh dengan menerapkan fungsi sigmoid pada *logit* keluaran model. Kelas prediksi ditentukan dengan *threshold* 0,5. Berdasarkan prediksi tersebut, dihitung *confusion matrix* yang memuat empat komponen:

1. *True Positive* (TP): jumlah observasi *fake* yang diklasifikasikan dengan benar sebagai *fake*.
2. *True Negative* (TN): jumlah observasi *real* yang diklasifikasikan dengan benar sebagai *real*.
3. *False Positive* (FP): jumlah observasi *real* yang salah diklasifikasikan sebagai *fake*.
4. *False Negative* (FN): jumlah observasi *fake* yang salah diklasifikasikan sebagai *real*.

Dari *confusion matrix*, diturunkan metrik evaluasi berikut:

**Accuracy:**

$$
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
$$ ............(3.13)

**Precision:**

$$
Precision = \frac{TP}{TP + FP}
$$ ............(3.14)

**Recall:**

$$
Recall = \frac{TP}{TP + FN}
$$ ............(3.15)

**F1-Score:**

$$
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
$$ ............(3.16)

**AUC (Area Under the ROC Curve):**

AUC mengukur kemampuan model membedakan kelas *real* dan *fake* secara *threshold-independent*. Nilai AUC mendekati 1,0 menunjukkan daya pemisah yang sangat baik, sedangkan nilai mendekati 0,5 menunjukkan performa setara tebakan acak.

#### 3.7.1.1 Contoh Perhitungan Metrik dari Confusion Matrix

Misalkan pada evaluasi *test set* diperoleh hasil berikut:

Tabel 3.13 Contoh Confusion Matrix

| | Prediksi Fake | Prediksi Real |
| --- | --- | --- |
| **Aktual Fake** | TP = 85 | FN = 15 |
| **Aktual Real** | FP = 10 | TN = 90 |

$$
Accuracy = \frac{85 + 90}{85 + 90 + 10 + 15} = \frac{175}{200} = 0{,}875
$$

$$
Precision = \frac{85}{85 + 10} = \frac{85}{95} = 0{,}895
$$

$$
Recall = \frac{85}{85 + 15} = \frac{85}{100} = 0{,}850
$$

$$
F1 = 2 \times \frac{0{,}895 \times 0{,}850}{0{,}895 + 0{,}850} = 2 \times \frac{0{,}761}{1{,}745} = 0{,}872
$$

### 3.7.2 Pengukuran Generalization Drop

Selain metrik evaluasi standar, penelitian ini juga menghitung penurunan generalisasi menggunakan selisih nilai F1 antara pengujian *in-dataset* dan *cross-dataset*:

$$
Drop = F1_{\text{in}} - F1_{\text{cross}}
$$ ............(3.17)

Semakin besar nilai *drop*, semakin besar penurunan performa model ketika berpindah dari pengujian pada dataset sejenis ke dataset yang berbeda. Nilai ini digunakan untuk menganalisis apakah model mempelajari ciri deepfake yang universal atau hanya menyesuaikan diri terhadap karakteristik dataset tertentu.

### 3.7.3 Tabel Evaluasi Otomatis

Pipeline menghasilkan tiga tabel utama setelah eksperimen selesai:

1. `Table1_in_dataset.csv` — performa pada skenario *in-dataset*.
2. `Table2_cross_dataset.csv` — performa pada skenario *cross-dataset*.
3. `Table3_generalization_drop.csv` — selisih F1 antara *in-dataset* dan *cross-dataset*.

Tabel-tabel tersebut disimpan pada folder `outputs/tables/n{jumlah_sampel}/` dan menjadi dasar analisis pada BAB IV.

## 3.8 Langkah Implementasi Eksperimen

### 3.8.1 Lingkungan Implementasi

Implementasi dikembangkan dalam bahasa pemrograman Python dengan pustaka utama PyTorch. Pustaka pendukung meliputi:

Tabel 3.14 Pustaka yang Digunakan

| Pustaka | Fungsi |
| --- | --- |
| PyTorch | Kerangka pembelajaran mendalam |
| torchvision | Transformasi citra |
| timm | *Backbone* XceptionNet *pretrained* |
| NumPy | Komputasi numerik dan FFT |
| pandas | Pengolahan data tabular |
| scikit-learn | Pembagian data dan metrik evaluasi |
| OpenCV | Ekstraksi frame video |
| Pillow | Manipulasi citra |
| tqdm | *Progress monitoring* |
| PyYAML | Pembacaan konfigurasi |

Seluruh konfigurasi inti didefinisikan melalui file `config.yaml` dan dapat di-*override* melalui argumen *command line*.

### 3.8.2 Prosedur Pelaksanaan

Untuk setiap kombinasi model, dataset, dan ukuran sampel, eksperimen dijalankan melalui prosedur yang seragam:

1. Menentukan dataset dan ukuran sampel yang akan digunakan.
2. Memindai folder dataset untuk mengidentifikasi video asli dan manipulasi berdasarkan *keyword* label.
3. Melakukan *balanced sampling* video sesuai jumlah sampel eksperimen.
4. Mengekstraksi frame dari setiap video terpilih.
5. Menyusun *manifest* video dan membentuk *split* train/validation/test pada level video.
6. Menghitung dan menyimpan cache FFT *log-magnitude* untuk setiap frame.
7. Melatih model sampai jumlah *epoch* yang ditetapkan.
8. Memilih *checkpoint* terbaik berdasarkan *validation* AUC.
9. Mengevaluasi *checkpoint* terbaik pada *test set in-dataset*.
10. Mengevaluasi *checkpoint* yang sama pada dataset lain (*cross-dataset*).
11. Menyimpan seluruh hasil ke dalam tabel ringkasan eksperimen.

Prosedur ini tersedia secara otomatis melalui skrip `run_pipeline.py` sehingga keseluruhan eksperimen dapat direplikasi dengan satu perintah:

```
python scripts/run_pipeline.py --n-samples 400 --max-frames 100 --epochs 10 --pretrained
```

### 3.8.3 Struktur Output

Output yang dihasilkan *pipeline* tersusun sebagai berikut:

1. `outputs/frames/` — frame hasil ekstraksi per video.
2. `outputs/manifests/` — *manifest* video dan *split* train, validation, test.
3. `outputs/fft_cache/` — cache FFT per frame.
4. `outputs/runs/` — *checkpoint* model, log pelatihan, dan riwayat metrik validasi.
5. `outputs/tables/` — tabel hasil evaluasi.

## 3.9 Ringkasan Tahapan Pelaksanaan

Metodologi penelitian ini dibangun di atas prinsip evaluasi yang terkontrol dan dapat direplikasi. Data diproses dari level video ke level frame, namun pembagian subset dilakukan pada level video untuk mencegah kebocoran data. Representasi deepfake dianalisis melalui dua domain, yaitu domain spasial dan domain frekuensi, kemudian dibandingkan melalui tiga arsitektur model utama: *spatial*, *freq*, dan *hybrid*.

Desain eksperimen yang menggunakan dua dataset, tiga ukuran sampel, serta dua skenario evaluasi memungkinkan penelitian ini tidak hanya menilai performa deteksi, tetapi juga menilai kemampuan generalisasi model. Dengan demikian, BAB III ini memberikan fondasi metodologis yang kuat bagi analisis hasil pada bab berikutnya.
