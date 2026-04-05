# BAB III TAHAPAN PELAKSANAAN

## 3.1 Kerangka Tahapan Pelaksanaan

### 3.1.1 Jenis dan Pendekatan Penelitian

Penelitian ini merupakan penelitian eksperimental di bidang _computer vision_ dan _deep learning_. Fokus utama penelitian adalah merancang, mengimplementasikan, dan mengevaluasi model deteksi _deepfake_ yang menggabungkan analisis domain spasial dan domain frekuensi secara bersamaan. Pendekatan eksperimental dipilih karena tujuan penelitian adalah mengevaluasi keampuhan metode baru dalam kondisi terkontrol, di mana variabel seperti dataset, arsitektur model, dan parameter pelatihan dapat dimanipulasi dan direplikasi secara konsisten.

Metode deteksi _deepfake_ konvensional umumnya hanya memanfaatkan fitur spasial (tekstur, struktur wajah) atau bergantung pada model tunggal. Namun, pada kasus manipulasi yang canggih, artefak spasial dapat sangat halus sehingga sulit dideteksi oleh satu jenis fitur saja. Di sisi lain, citra hasil sintesis generatif (_GAN_) memiliki ketidaksempurnaan pada distribusi spektral yang tidak terlihat secara kasat mata namun terdeteksi melalui analisis frekuensi (Odena et al., 2016; Durall et al., 2020). Oleh karena itu, penelitian ini mengusulkan pendekatan hibrida yang memadukan dua domain analisis:

1. **Analisis domain spasial** melalui jaringan konvolusional XceptionNet (Chollet, 2017) yang telah terbukti efektif dalam mengekstraksi fitur visual tingkat tinggi dari citra wajah.
2. **Analisis domain frekuensi** melalui transformasi Fourier cepat (_Fast Fourier Transform_ / FFT) yang diproses oleh jaringan konvolusional khusus (_FreqCNN_) untuk menangkap artefak spektral yang dihasilkan oleh proses sintesis _deepfake_.

Sebagai bagian dari desain eksperimental, penelitian ini membangun tiga varian model sebagai perbandingan terkontrol:

- **Model spasial** (_spatial_): hanya menggunakan fitur domain spasial (XceptionNet).
- **Model frekuensi** (_freq_): hanya menggunakan fitur domain frekuensi (FreqCNN pada peta FFT).
- **Model hibrida** (_hybrid_): menggabungkan kedua domain melalui arsitektur _late fusion_ dengan mekanisme _Squeeze-and-Excitation_ (SE) _gating_.

Desain tiga varian ini memungkinkan pengukuran kontribusi individual masing-masing domain serta evaluasi apakah penggabungan keduanya menghasilkan peningkatan performa deteksi dan generalisasi lintas dataset.

### 3.1.2 Tahapan Pelaksanaan Penelitian

Pelaksanaan penelitian ini terdiri dari lima tahapan utama:

1. **Pengumpulan Data** — Menggunakan dua dataset _benchmark_ standar untuk deteksi _deepfake_, yaitu FaceForensics++ (FFPP) dan Celeb-DF v2 (CDF).
2. **Preprocessing** — Meliputi ekstraksi _frame_ dari video, konversi domain frekuensi melalui FFT, normalisasi, serta augmentasi data.
3. **Perancangan Model** — Merancang tiga arsitektur model: _spatial_ (XceptionNet), _frequency_ (FreqCNN), dan _hybrid_ (HybridTwoBranch) dengan mekanisme _late fusion_ dan SE _gating_.
4. **Pelatihan dan Optimasi** — Melatih setiap model menggunakan strategi _transfer learning_, _differential learning rate_, penjadwalan _learning rate_ (_warmup_ + _cosine decay_), dan _early stopping_ berdasarkan AUC.
5. **Pengujian dan Evaluasi** — Mengevaluasi setiap model secara _in-dataset_ dan _cross-dataset_ pada berbagai ukuran sampel, menggunakan metrik akurasi, presisi, _recall_, F1-_score_, dan AUC-ROC.

Alur pelaksanaan penelitian secara keseluruhan diilustrasikan pada Gambar 3.1.

<!-- Gambar 3.1: Flowchart Utama Pipeline Penelitian -->

<!--
Dataset Video (FFPP, CDF)
        ↓
Ekstraksi Frame (5 FPS, maks 50 frame/video)
        ↓
Konversi FFT (Grayscale → FFT 2D → fftshift → |F| → log1p)
        ↓
Pembagian Dataset (Train 70% / Val 15% / Test 15%, stratified by video)
        ↓
Pelatihan Model (Spatial / Freq / Hybrid) → Validasi → Checkpoint Terbaik (AUC)
        ↓
Evaluasi (In-dataset + Cross-dataset) → Tabel Hasil → Analisis
-->

> Gambar 3.1 Flowchart Utama _Pipeline_ Penelitian

---

## 3.2 Dataset dan Sumber Data

Pemilihan dataset merupakan langkah krusial dalam penelitian deteksi *deepfake*. Dataset yang digunakan harus merepresentasikan keberagaman metode manipulasi dan tingkat kualitas visual yang berbeda agar model yang dikembangkan dapat dievaluasi secara komprehensif. Penelitian ini menggunakan dua dataset *benchmark* yang diakui secara luas dalam komunitas riset deteksi *deepfake*, yaitu FaceForensics++ dan Celeb-DF v2, yang masing-masing memiliki karakteristik dan tantangan yang berbeda. Selain itu, diuraikan pula strategi pembagian dataset dan variasi ukuran sampel yang dirancang untuk menganalisis ketahanan model pada berbagai kondisi ketersediaan data.

### 3.2.1 FaceForensics++ (FFPP)

Dataset pertama yang digunakan dalam penelitian ini adalah FaceForensics++ yang diperkenalkan oleh Rössler _et al._ (Rössler et al., 2019). FaceForensics++ merupakan salah satu _benchmark_ standar yang paling banyak digunakan dalam penelitian deteksi _deepfake_. Dataset ini terdiri dari video wajah asli yang bersumber dari YouTube serta video hasil manipulasi menggunakan empat metode yang berbeda:

1. **Deepfakes** — Pertukaran wajah berbasis _autoencoder_.
2. **Face2Face** — Transfer ekspresi wajah secara _real-time_.
3. **FaceSwap** — Pertukaran wajah berbasis grafik komputer.
4. **NeuralTextures** — Manipulasi berbasis _neural rendering_.

Keberagaman metode manipulasi ini menjadikan FaceForensics++ sangat cocok untuk menguji ketahanan (_robustness_) model terhadap berbagai jenis artefak _deepfake_. Video dalam dataset tersedia dalam tiga tingkat kompresi: _raw_ (tanpa kompresi), c23 (kompresi ringan), dan c40 (kompresi berat). Pada penelitian ini digunakan tingkat kompresi c23 yang merepresentasikan skenario distribusi video secara _online_ yang realistis.

Pelabelan data dilakukan secara otomatis berdasarkan pencocokan kata kunci pada nama direktori. Video yang berada dalam direktori mengandung kata kunci "original", "real", atau "pristine" dilabeli sebagai _real_ (label 0), sedangkan video dalam direktori mengandung kata kunci "fake", "manipulated", "deepfakes", "faceswap", "neuraltextures", atau "face2face" dilabeli sebagai _fake_ (label 1).

### 3.2.2 Celeb-DF v2 (CDF)

Dataset kedua yang digunakan adalah Celeb-DF v2 (Celeb-_DeepFake_) yang diperkenalkan oleh Li _et al._ (Li et al., 2020). Celeb-DF berisi video wajah selebriti asli dan versi _deepfake_-nya yang dihasilkan menggunakan teknik _face swapping_ tunggal. Dibandingkan FaceForensics++, _deepfake_ dalam Celeb-DF memiliki kualitas visual yang lebih tinggi dengan artefak yang lebih halus dan sulit dideteksi secara kasat mata.

Celeb-DF digunakan secara khusus dalam penelitian ini untuk menguji kemampuan generalisasi lintas dataset (_cross-dataset generalization_). Karena Celeb-DF hanya menggunakan satu metode sintesis yang berbeda dari keempat metode dalam FaceForensics++, evaluasi silang antara kedua dataset ini mengukur sejauh mana model mampu mendeteksi _deepfake_ dari metode yang belum pernah dilihat selama pelatihan.

### 3.2.3 Pembagian Dataset

Pembagian dataset dilakukan pada level video, bukan pada level _frame_, untuk mencegah kebocoran data (_data leakage_). Apabila pembagian dilakukan pada level _frame_, terdapat risiko _frame-frame_ dari video yang sama tersebar ke dalam set pelatihan dan pengujian, sehingga model secara tidak sengaja menghafal karakteristik video tertentu alih-alih mempelajari pola _deepfake_ secara umum.

Pembagian dilakukan secara terstratifikasi (_stratified split_) berdasarkan label untuk mempertahankan rasio kelas _real_/_fake_ yang seimbang pada setiap subset. Proporsi pembagian yang digunakan adalah sebagai berikut:

Tabel 3.1 Pembagian Dataset

| Subset       | Proporsi | Stratifikasi      | Level Pembagian |
| ------------ | -------- | ----------------- | --------------- |
| _Training_   | 70%      | Berdasarkan label | Video           |
| _Validation_ | 15%      | Berdasarkan label | Video           |
| _Testing_    | 15%      | Berdasarkan label | Video           |

Pembagian dilakukan menggunakan fungsi `train_test_split` dari pustaka _scikit-learn_ dengan parameter `stratify` berdasarkan label dan _seed_ = 42 untuk menjamin reproduktibilitas. Validasi tambahan dilakukan untuk memastikan tidak terdapat duplikasi `video_id` dan setiap kelas memiliki minimum 4 sampel yang diperlukan untuk pembagian terstratifikasi tiga arah.

### 3.2.4 Variasi Ukuran Sampel

Untuk menganalisis pengaruh jumlah data pelatihan terhadap performa model, eksperimen dilakukan pada beberapa variasi ukuran sampel. Jumlah sampel yang digunakan berbeda untuk setiap dataset, disesuaikan dengan ketersediaan data:

Tabel 3.2 Variasi Ukuran Sampel per Dataset

| Dataset                | Ukuran Sampel (jumlah video) |
| ---------------------- | ---------------------------- |
| FaceForensics++ (FFPP) | 100, 300, 600, 1000          |
| Celeb-DF v2 (CDF)      | 100, 250, 500, 750           |

Pada setiap ukuran sampel, pengambilan video dilakukan secara seimbang antara kelas _real_ dan _fake_ (rasio 50:50). Dari setiap video yang terpilih, diekstraksi maksimum 50 _frame_ pada laju 5 _frame per second_ (FPS). Variasi ukuran sampel ini memungkinkan analisis terhadap ketahanan masing-masing arsitektur model pada kondisi data terbatas maupun melimpah.

<!-- Gambar 3.2: Contoh Frame Real vs Fake -->

<!-- Tampilkan 4 gambar: Real FFPP, Fake FFPP, Real CDF, Fake CDF -->

> Gambar 3.2 Contoh _Frame_ Real dan _Fake_ dari Dataset FaceForensics++ dan Celeb-DF

---

## 3.3 Tahapan _Preprocessing_ Data

Tahapan *preprocessing* bertujuan untuk mengonversi data video mentah menjadi representasi yang dapat diproses oleh model *deep learning*. *Pipeline preprocessing* terdiri dari tiga tahapan utama: (1) ekstraksi *frame* dari video, (2) konversi domain frekuensi melalui FFT untuk menghasilkan peta *magnitude*, dan (3) augmentasi data untuk meningkatkan keberagaman set pelatihan. Setiap tahapan dirancang untuk mempertahankan informasi yang relevan sambil menstandarkan format data agar konsisten antar dataset.

### 3.3.1 Ekstraksi _Frame_ dari Video

Tahap pertama _preprocessing_ adalah mengekstraksi _frame_ citra dari setiap video dalam dataset. Proses ini dilakukan menggunakan pustaka OpenCV dengan langkah-langkah sebagai berikut:

1. Setiap video dibuka dan dibaca laju _frame_ aslinya (_native FPS_).
2. Interval pengambilan _frame_ dihitung berdasarkan target FPS: $\text{interval} = \max\left(\left\lfloor \frac{\text{FPS}_{\text{asli}}}{\text{FPS}_{\text{target}}} \right\rfloor, 1\right)$ dengan FPS target = 5.
3. _Frame_ diambil pada setiap interval yang telah dihitung, hingga maksimum 50 _frame_ per video.
4. Setiap _frame_ disimpan sebagai berkas JPEG dengan penamaan berurutan: `frame_000000.jpg`, `frame_000001.jpg`, dan seterusnya.
5. Label setiap video diinferensi secara otomatis dari nama direktori berdasarkan pencocokan kata kunci yang telah dikonfigurasi.

Proses ekstraksi dilakukan secara paralel menggunakan _multiprocessing pool_ untuk mempercepat pemrosesan pada dataset berskala besar. Hasil ekstraksi disimpan dalam berkas manifes CSV yang berisi kolom `video_id`, `label`, dan `frames_dir` sebagai referensi untuk tahap selanjutnya.

### 3.3.2 Konversi Domain Frekuensi (FFT)

Konversi domain frekuensi merupakan inti kontribusi penelitian ini. Proses ini mengubah setiap _frame_ citra RGB menjadi representasi peta _magnitude_ frekuensi menggunakan _Fast Fourier Transform_ (FFT) 2 dimensi. Representasi frekuensi ini menangkap artefak spektral yang dihasilkan oleh proses sintesis _deepfake_, seperti _checkerboard artifacts_ dari operasi _upsampling_ pada GAN (Odena et al., 2016), distorsi distribusi spektral (Durall et al., 2020), dan ketidakkontinyuan pada batas _blending_ (Zhang et al., 2019).

#### 3.3.2.1 Konversi RGB ke _Grayscale_

Langkah pertama adalah mengonversi citra RGB menjadi _grayscale_ (satu kanal). Konversi dilakukan menggunakan standar ITU-R BT.601 dengan formula:

$$
Y = 0{,}299R + 0{,}587G + 0{,}114B \tag{3.1}
$$

di mana $Y$ adalah nilai luminansi, dan $R$, $G$, $B$ adalah nilai kanal warna merah, hijau, dan biru. Bobot yang berbeda pada setiap kanal mencerminkan sensitivitas mata manusia terhadap masing-masing warna. Konversi ke satu kanal cukup untuk analisis frekuensi karena informasi luminansi merepresentasikan distribusi intensitas spasial yang diperlukan untuk mendeteksi artefak spektral.

#### 3.3.2.2 Transformasi Fourier 2D

Citra _grayscale_ kemudian diubah ukurannya menjadi $224 \times 224$ piksel dan ditransformasi ke domain frekuensi menggunakan _Discrete Fourier Transform_ (DFT) 2 dimensi. DFT 2D didefinisikan sebagai:

$$
F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) \cdot e^{-j2\pi\left(\frac{ux}{M} + \frac{vy}{N}\right)} \tag{3.2}
$$

di mana $f(x, y)$ adalah nilai piksel pada posisi $(x, y)$, $F(u, v)$ adalah koefisien frekuensi pada koordinat frekuensi $(u, v)$, $M$ dan $N$ adalah dimensi citra (keduanya 224), dan $j = \sqrt{-1}$ adalah unit imajiner.

Setelah transformasi, dilakukan operasi _FFT shift_ yang memindahkan komponen frekuensi nol (_DC component_) dari sudut matriks ke posisi tengah. Hal ini menyebabkan frekuensi rendah terletak di bagian tengah peta frekuensi dan frekuensi tinggi di bagian tepi, sehingga memudahkan interpretasi visual dan analisis.

#### 3.3.2.3 _Magnitude Spectrum_ dan _Log Scaling_

Dari hasil DFT yang berupa bilangan kompleks, dihitung _magnitude spectrum_:

$$
|F(u, v)| = \sqrt{\text{Re}(F(u,v))^2 + \text{Im}(F(u,v))^2} \tag{3.3}
$$

Karena rentang dinamis _magnitude spectrum_ sangat lebar — komponen DC (_direct current_) dapat bernilai ribuan kali lipat lebih besar dari komponen frekuensi tinggi — maka dilakukan transformasi logaritmik:

$$
M_{\log}(u, v) = \log(1 + |F(u, v)|) \tag{3.4}
$$

Fungsi $\log(1 + x)$ (dikenal sebagai `log1p`) dipilih karena dua alasan: (1) menghindari permasalahan $\log(0)$ karena $\log(1+0) = 0$, dan (2) mengompresi rentang dinamis sehingga detail pada frekuensi tinggi tidak tertutupi oleh dominasi komponen DC. Hasil akhir berupa matriks _float32_ berukuran $224 \times 224$ dengan nilai tipikal pada rentang $[0, \sim16]$ yang disimpan sebagai berkas `.npy` (_NumPy array_) dalam _cache_ FFT.

#### 3.3.2.4 Contoh Perhitungan FFT 2D

Sebagai ilustrasi, berikut ditunjukkan perhitungan FFT 2D pada matriks _grayscale_ berukuran $4 \times 4$. Misalkan matriks piksel $f(x, y)$ adalah:

Tabel 3.3 Contoh Matriks _Grayscale_ 4×4

|       | $y=0$ | $y=1$ | $y=2$ | $y=3$ |
| ----- | ----- | ----- | ----- | ----- |
| $x=0$ | 100   | 120   | 100   | 120   |
| $x=1$ | 80    | 100   | 80    | 100   |
| $x=2$ | 100   | 120   | 100   | 120   |
| $x=3$ | 80    | 100   | 80    | 100   |

**Langkah 1: Hitung $F(0,0)$ — Komponen DC**

$$
F(0,0) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi(0)} = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \tag{3.5}
$$

$$
F(0,0) = (100+120+100+120) + (80+100+80+100) + (100+120+100+120) + (80+100+80+100)
$$

$$
F(0,0) = 440 + 360 + 440 + 360 = 1600
$$

Komponen DC merepresentasikan rata-rata intensitas keseluruhan citra, yaitu $1600 / 16 = 100$.

**Langkah 2: Hitung $F(0,1)$ — Frekuensi horizontal pertama**

$$
F(0,1) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi \cdot y/4} \tag{3.6}
$$

Karena $e^{-j2\pi y/4}$ menghasilkan faktor $\{1, -j, -1, j\}$ untuk $y = 0, 1, 2, 3$:

- Baris $x=0$: $100(1) + 120(-j) + 100(-1) + 120(j) = 0 + (-120j + 120j) = 0$
- Baris $x=1$: $80(1) + 100(-j) + 80(-1) + 100(j) = 0 + (-100j + 100j) = 0$
- Baris $x=2$: sama dengan $x=0 \Rightarrow 0$
- Baris $x=3$: sama dengan $x=1 \Rightarrow 0$

$$
F(0,1) = 0
$$

Hal ini menunjukkan bahwa pola frekuensi horizontal pada matriks ini simetris.

**Langkah 3: Hitung $F(1,0)$ — Frekuensi vertikal pertama**

$$
F(1,0) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi x/4} \tag{3.7}
$$

Faktor $e^{-j2\pi x/4}$ menghasilkan $\{1, -j, -1, j\}$ untuk $x = 0, 1, 2, 3$:

- $x=0$: $(100+120+100+120)(1) = 440$
- $x=1$: $(80+100+80+100)(-j) = -360j$
- $x=2$: $(100+120+100+120)(-1) = -440$
- $x=3$: $(80+100+80+100)(j) = 360j$

$$
F(1,0) = 440 - 360j - 440 + 360j = 0
$$

**Langkah 4: Hitung $F(1,1)$**

$$
F(1,1) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi(x+y)/4} \tag{3.8}
$$

Faktor gabungan $e^{-j2\pi(x+y)/4}$ untuk setiap $(x, y)$:

| $(x,y)$ | $f(x,y)$ | $e^{-j\pi(x+y)/2}$ | Hasil   |
| ------- | -------- | ------------------ | ------- |
| (0,0)   | 100      | 1                  | 100     |
| (0,1)   | 120      | $-j$               | $-120j$ |
| (0,2)   | 100      | $-1$               | $-100$  |
| (0,3)   | 120      | $j$                | $120j$  |
| (1,0)   | 80       | $-j$               | $-80j$  |
| (1,1)   | 100      | $-1$               | $-100$  |
| (1,2)   | 80       | $j$                | $80j$   |
| (1,3)   | 100      | $1$                | $100$   |
| (2,0)   | 100      | $-1$               | $-100$  |
| (2,1)   | 120      | $j$                | $120j$  |
| (2,2)   | 100      | $1$                | $100$   |
| (2,3)   | 120      | $-j$               | $-120j$ |
| (3,0)   | 80       | $j$                | $80j$   |
| (3,1)   | 100      | $1$                | $100$   |
| (3,2)   | 80       | $-j$               | $-80j$  |
| (3,3)   | 100      | $-1$               | $-100$  |

Penjumlahan bagian real: $100 - 100 - 100 + 100 - 100 + 100 - 100 + 100 = 0$

Penjumlahan bagian imajiner: $-120 - 80 + 80 + 120 + 120 - 120 + 80 - 80 = 0$

$$
F(1,1) = 0 + 0j = 0
$$

Matriks ini memiliki pola repetitif sempurna sehingga energi terkonsentrasi pada komponen DC. Pada citra wajah sesungguhnya, distribusi energi lebih tersebar dan perbedaan antara citra _real_ dan _fake_ terlihat dari pola distribusi frekuensi tinggi yang anomal.

**Langkah 5: _Magnitude_ dan _Log Scaling_**

Tabel 3.4 Contoh Perhitungan _Magnitude_ dan _Log Scaling_

| Komponen | $F(u,v)$ | $\|F(u,v)\|$ | $\log(1 + \|F(u,v)\|)$ |
| -------- | -------- | ------------ | ---------------------- |
| $F(0,0)$ | $1600$   | $1600$       | $7{,}378$              |
| $F(0,1)$ | $0$      | $0$          | $0$                    |
| $F(1,0)$ | $0$      | $0$          | $0$                    |
| $F(1,1)$ | $0$      | $0$          | $0$                    |

Pada citra _deepfake_ sesungguhnya, komponen frekuensi tinggi menunjukkan pola anomali yang khas, seperti _spectral rolloff_ yang tidak wajar (Durall et al., 2020) atau puncak periodik akibat _checkerboard artifacts_ dari operasi _transposed convolution_ pada GAN (Odena et al., 2016).

#### 3.3.2.5 Normalisasi FFT

Setelah seluruh _frame_ dikonversi ke peta _magnitude_ FFT dan disimpan dalam _cache_, dilakukan perhitungan statistik normalisasi per dataset. Normalisasi menggunakan _z-score_:

$$
\hat{x} = \frac{x - \mu}{\sigma} \tag{3.9}
$$

di mana $\mu$ dan $\sigma$ adalah rata-rata dan simpangan baku global yang dihitung dari seluruh piksel dalam _cache_ FFT dataset tersebut. Perhitungan dilakukan pada sampel acak hingga 5.000 berkas _cache_ menggunakan akumulasi _online_ (metode Welford) untuk efisiensi memori. Hasil disimpan dalam berkas `fft_stats.json` yang dimuat secara otomatis saat pelatihan.

Normalisasi per dataset ini penting karena setiap dataset memiliki karakteristik spektral yang berbeda akibat perbedaan kamera, resolusi, dan metode kompresi. Tanpa normalisasi yang tepat, fitur frekuensi dari dataset yang berbeda akan memiliki skala yang tidak sebanding.

### 3.3.3 Augmentasi Data

Augmentasi data merupakan teknik regularisasi yang diterapkan selama pelatihan untuk meningkatkan keberagaman data tanpa menambah jumlah sampel asli. Pada penelitian ini, strategi augmentasi dirancang secara terpisah untuk domain spasial dan domain frekuensi, karena karakteristik kedua representasi data yang berbeda secara fundamental. Selain itu, pada mode *hybrid*, konsistensi augmentasi antara kedua cabang dijaga untuk mempertahankan korespondensi spasial-frekuensi.

#### 3.3.3.1 Augmentasi Domain Spasial

Augmentasi pada domain spasial diterapkan pada citra RGB selama pelatihan untuk meningkatkan keberagaman data dan mencegah _overfitting_. _Pipeline_ augmentasi terdiri dari:

1. **Resize** — Citra diubah ukurannya menjadi $256 \times 256$ piksel (lebih besar dari ukuran input final).
2. **RandomResizedCrop** — Pemotongan acak ke ukuran $224 \times 224$ dengan skala antara 80%–100% dari citra asli. Augmentasi ini mensimulasikan variasi _zoom_ dan posisi wajah.
3. **ColorJitter** — Perubahan acak pada kecerahan ($\pm 0{,}2$), kontras ($\pm 0{,}2$), saturasi ($\pm 0{,}1$), dan _hue_ ($\pm 0{,}05$). Augmentasi ini mensimulasikan variasi kondisi pencahayaan, pengaturan kamera, dan karakteristik sensor yang berbeda antar video sumber.
4. **RandomHorizontalFlip** — Pembalikan horizontal dengan probabilitas 50%. Augmentasi ini memanfaatkan simetri bilateral wajah manusia.
5. **ToTensor** — Konversi ke tensor PyTorch dengan rentang nilai $[0, 1]$.
6. **Normalize** — Normalisasi menggunakan statistik ImageNet: $\text{mean} = [0{,}485;\ 0{,}456;\ 0{,}406]$, $\text{std} = [0{,}229;\ 0{,}224;\ 0{,}225]$.
7. **RandomErasing** — Penghapusan acak sebuah area persegi panjang pada tensor (probabilitas 10%, skala 2%–15% dari luas citra) yang diisi dengan nilai acak. Teknik ini diterapkan setelah normalisasi (beroperasi pada tensor, bukan citra PIL) dan mendorong model untuk tidak bergantung pada satu wilayah spesifik dari citra wajah, meningkatkan ketahanan terhadap oklusi parsial.

Pada tahap validasi dan pengujian, augmentasi acak tidak diterapkan. Citra hanya diubah ukurannya secara langsung ke $224 \times 224$, dikonversi ke tensor, dan dinormalisasi.

#### 3.3.3.2 Augmentasi Domain Frekuensi

Augmentasi pada domain frekuensi memerlukan pendekatan yang berbeda dari domain spasial. Operasi spasial seperti pemotongan acak (_random crop_) atau rotasi tidak sesuai untuk peta _magnitude_ FFT karena akan merusak lokalisasi frekuensi — setiap posisi piksel pada peta FFT merepresentasikan komponen frekuensi spesifik yang bergantung pada posisi absolutnya.

Oleh karena itu, augmentasi pada domain frekuensi dilakukan melalui injeksi _noise_ Gaussian:

$$
\hat{x}_{\text{fft}} = x_{\text{fft}} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2) \tag{3.10}
$$

dengan $\sigma = 0{,}05$ (dikonfigurasi melalui parameter `fft_noise_sigma`). _Noise_ diterapkan setelah normalisasi _z-score_ dan hanya selama pelatihan. Rasional dari pendekatan ini adalah: (1) mensimulasikan variasi _noise_ sensor dan artefak kompresi yang memengaruhi spektrum frekuensi, dan (2) mencegah penghafalan (_memorization_) peta FFT yang identik di setiap _epoch_ karena data FFT dimuat dari _cache_ statis.

Selain injeksi _noise_, diterapkan pula **_spectral band masking_** dengan probabilitas 15%. Pada setiap _frame_ yang terpilih secara acak, sebuah pita frekuensi — baik horizontal maupun vertikal — dengan lebar acak antara 2 hingga $\lfloor H/8 \rfloor$ piksel diisi dengan nilai nol:

$$
\hat{x}_{\text{fft}}[r_1 : r_1 + w, :] = 0 \quad \text{(pita horizontal)} \tag{3.11}
$$

$$
\hat{x}_{\text{fft}}[:, c_1 : c_1 + w] = 0 \quad \text{(pita vertikal)} \tag{3.12}
$$

di mana $w$ adalah lebar pita acak dan $r_1$ atau $c_1$ adalah posisi awal acak. Pemilihan orientasi horizontal atau vertikal dilakukan dengan probabilitas 50:50. Teknik ini mencegah model bergantung pada satu pita frekuensi spesifik dan mendorong representasi frekuensi yang lebih merata dan _robust_.

<!-- Gambar 3.X: Contoh Spectral Band Masking pada Peta FFT -->

<!-- Search keyword: "spectral band masking frequency domain augmentation" -->

<!-- Tampilkan: peta FFT asli (kiri) dan peta FFT setelah pita horizontal di-mask/diisi nol (kanan) -->

> Gambar 3.3 Contoh Penerapan _Spectral Band Masking_ pada Peta _Magnitude_ FFT

#### 3.3.3.3 Konsistensi Augmentasi pada Mode _Hybrid_

Pada mode _hybrid_, di mana model menerima input RGB dan FFT secara bersamaan, konsistensi augmentasi antara kedua cabang sangat penting. Pembalikan horizontal (_horizontal flip_) pada citra RGB tanpa pembalikan yang sama pada peta FFT akan merusak korespondensi spasial-frekuensi, karena $|\text{DFT}(\text{flip}(x))| = \text{flip}(|\text{DFT}(x)|)$.

Untuk mengatasi hal ini, pembalikan horizontal pada mode _hybrid_ diterapkan secara manual setelah kedua input dimuat, dengan keputusan acak yang sama (probabilitas 50%) diterapkan secara identik pada tensor RGB dan tensor FFT. Pada _pipeline_ augmentasi spasial untuk mode _hybrid_, opsi `RandomHorizontalFlip` dinonaktifkan (`include_hflip=False`) agar pembalikan dapat dikontrol secara terpadu.

<!-- Gambar 3.3: Flowchart Preprocessing Pipeline -->

> Gambar 3.4 Flowchart _Pipeline Preprocessing_ Data

<!-- Gambar 3.4: Perbandingan FFT Real vs Fake -->

<!-- Tampilkan: Frame real (RGB) + FFT-nya, Frame fake (RGB) + FFT-nya -->

> Gambar 3.5 Perbandingan Peta _Magnitude_ FFT antara _Frame_ Real dan _Fake_

---

## 3.4 Arsitektur Model yang Diusulkan

Penelitian ini merancang dan mengevaluasi tiga arsitektur model yang masing-masing merepresentasikan pendekatan berbeda dalam deteksi _deepfake_: model berbasis domain spasial saja, model berbasis domain frekuensi saja, dan model hibrida yang menggabungkan keduanya.

### 3.4.1 Model Spasial — XceptionNet

Model spasial merupakan *baseline* utama dalam penelitian ini yang menganalisis fitur visual langsung dari citra RGB. Arsitektur XceptionNet dipilih karena telah terbukti sebagai salah satu model paling efektif untuk deteksi *deepfake* pada domain spasial, sebagaimana ditunjukkan oleh Rössler et al. (2019) yang melaporkan akurasi 96–99% pada dataset FaceForensics++. Bagian berikut menjelaskan komponen utama arsitektur XceptionNet yang digunakan dalam penelitian ini.

#### 3.4.1.1 _Depthwise Separable Convolution_

XceptionNet (Chollet, 2017) merupakan arsitektur _convolutional neural network_ (CNN) yang dibangun sepenuhnya dari _depthwise separable convolution_. Berbeda dengan konvolusi standar yang menerapkan filter secara simultan pada dimensi spasial dan kanal, _depthwise separable convolution_ memfaktorisasi operasi menjadi dua tahap terpisah:

1. **Konvolusi _depthwise_** — Menerapkan satu filter konvolusi per kanal input secara independen. Untuk input dengan $C$ kanal dan filter berukuran $K \times K$, jumlah parameter adalah $C \times K \times K$.
2. **Konvolusi _pointwise_** — Menerapkan konvolusi $1 \times 1$ untuk menggabungkan informasi lintas kanal. Untuk menghasilkan $C'$ kanal output, jumlah parameter adalah $C \times C'$.

**Contoh Perhitungan Perbandingan Parameter:**

Untuk input berukuran $H \times W$ dengan $C_{\text{in}} = 64$ kanal, filter $3 \times 3$, dan $C_{\text{out}} = 128$ kanal output:

- **Konvolusi standar:** $C_{\text{in}} \times K^2 \times C_{\text{out}} = 64 \times 9 \times 128 = 73.728$ parameter.
- **Konvolusi _depthwise separable_:**
  - _Depthwise_: $C_{\text{in}} \times K^2 = 64 \times 9 = 576$ parameter.
  - _Pointwise_: $C_{\text{in}} \times C_{\text{out}} = 64 \times 128 = 8.192$ parameter.
  - Total: $576 + 8.192 = 8.768$ parameter.
- **Rasio pengurangan:** $8.768 / 73.728 \approx 11{,}9\%$ — pengurangan parameter sebesar $\sim 88\%$.

Efisiensi parameter ini memungkinkan XceptionNet memiliki kedalaman yang besar (36 _layer_ konvolusional) dengan total $\sim 22{,}8$ juta parameter, sambil tetap mempertahankan kapasitas representasi yang tinggi.

**Contoh Perhitungan _Depthwise Separable Convolution_:**

Misalkan input berukuran $3 \times 3$ dengan 2 kanal:

$$
\mathbf{X}_1 = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 1 & 2 \\ 0 & 1 & 3 \end{bmatrix}, \quad \mathbf{X}_2 = \begin{bmatrix} 2 & 0 & 1 \\ 1 & 3 & 0 \\ 2 & 1 & 1 \end{bmatrix} \tag{3.13}
$$

**Tahap 1 — _Depthwise_:** Filter $2 \times 2$ terpisah per kanal (tanpa _padding_, _stride_ = 1):

$$
\mathbf{W}_1 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}, \quad \mathbf{W}_2 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} \tag{3.14}
$$

Konvolusi kanal 1 ($\mathbf{X}_1 * \mathbf{W}_1$), posisi $(0,0)$:

$$
1 \times 1 + 2 \times 0 + 3 \times 0 + 1 \times 1 = 2 \tag{3.15}
$$

Hasil lengkap kanal 1:

$$
\mathbf{Y}_1 = \begin{bmatrix} 2 & 3 \\ 4 & 4 \end{bmatrix}
$$

Konvolusi kanal 2 ($\mathbf{X}_2 * \mathbf{W}_2$), posisi $(0,0)$:

$$
2 \times 0 + 0 \times 1 + 1 \times 1 + 3 \times 0 = 1 \tag{3.16}
$$

Hasil lengkap kanal 2:

$$
\mathbf{Y}_2 = \begin{bmatrix} 1 & 4 \\ 2 & 1 \end{bmatrix}
$$

**Tahap 2 — _Pointwise_:** Filter $1 \times 1$ berukuran $(2, 1)$ misalnya $[0{,}5;\ 0{,}5]$:

$$
\mathbf{Z}(i,j) = 0{,}5 \times \mathbf{Y}_1(i,j) + 0{,}5 \times \mathbf{Y}_2(i,j) \tag{3.17}
$$

$$
\mathbf{Z} = \begin{bmatrix} 1{,}5 & 3{,}5 \\ 3{,}0 & 2{,}5 \end{bmatrix}
$$

Hasil akhir merupakan gabungan informasi lintas kanal yang diperoleh secara efisien melalui dua tahap terpisah.

#### 3.4.1.2 _Transfer Learning_ dari ImageNet

XceptionNet yang digunakan dalam penelitian ini diinisialisasi dengan bobot yang telah dilatih pada dataset ImageNet (Chollet, 2017; Rössler et al., 2019), yang terdiri dari 1,4 juta citra dalam 1.000 kelas. _Transfer learning_ dari ImageNet memberikan fondasi representasi visual yang kuat — fitur-fitur tingkat rendah (tepi, tekstur) dan tingkat menengah (pola, bentuk) yang telah dipelajari dari ImageNet relevan dan dapat ditransfer ke tugas deteksi _deepfake_.

Model diimplementasikan menggunakan pustaka `timm` (_PyTorch Image Models_) melalui pemanggilan `timm.create_model("xception", pretrained=True)`. Lapisan klasifikasi asli ImageNet (1.000 kelas) diganti dengan lapisan _fully connected_ tunggal yang menghasilkan satu nilai _logit_ untuk klasifikasi biner (_real_ vs _fake_). Dimensi fitur yang dihasilkan oleh _backbone_ XceptionNet setelah _global average pooling_ adalah 2.048.

### 3.4.2 Model Frekuensi — FreqCNN

Model frekuensi dirancang untuk mengekstraksi dan menganalisis artefak pada domain frekuensi yang tidak terdeteksi oleh model spasial. Berbeda dengan XceptionNet yang memproses citra RGB secara langsung, FreqCNN memproses peta *magnitude* FFT yang merepresentasikan distribusi energi frekuensi dalam citra. Arsitektur ini dibangun khusus untuk tugas ini dengan desain yang lebih ringan namun mampu menangkap pola spektral yang khas dari citra *deepfake*.

#### 3.4.2.1 Arsitektur Konvolusional

FreqCNN adalah jaringan konvolusional ringan yang dirancang khusus untuk memproses peta _magnitude_ FFT berdimensi satu kanal. Arsitektur ini terdiri dari blok-blok konvolusional residual bertingkat (_FreqBlock_) yang secara progresif mengekstraksi fitur frekuensi dari resolusi rendah hingga tinggi.

Setiap _FreqBlock_ mengimplementasikan koneksi residual yang terinspirasi dari ResNet (He et al., 2016) dan terdiri dari dua jalur paralel:

1. **Jalur utama** — Conv2d($3 \times 3$, _padding_ = 1) → BatchNorm2d → ReLU.
2. **Jalur pintasan (_shortcut_)** — Konvolusi $1 \times 1$ untuk menyesuaikan dimensi kanal ketika jumlah kanal input berbeda dari output. Apabila dimensi sudah sama, jalur pintasan berupa operasi identitas (_identity_).

Kedua jalur dijumlahkan secara elemen (_residual addition_) sebelum _max pooling_ dengan _stride_ 2:

$$
\mathbf{y} = \text{MaxPool}_{2\times2}\left(\text{Conv}_{3\times3}(\mathbf{x}) + \text{Shortcut}(\mathbf{x})\right) \tag{3.18}
$$

Koneksi residual ini mencegah degradasi gradien pada jaringan yang lebih dalam dan memungkinkan setiap blok mempelajari representasi fitur tambahan (_residual_) di atas representasi yang sudah ada.

<!-- Gambar 3.X: Arsitektur FreqBlock dengan Koneksi Residual -->

<!-- Search keyword: "residual block diagram CNN skip connection 1x1 convolution" -->

<!-- Tampilkan: diagram blok dengan jalur utama (Conv→BN→ReLU) dan jalur shortcut (1x1 Conv), dijumlahkan sebelum MaxPool -->

> Gambar 3.6 Arsitektur FreqBlock dengan Koneksi Residual

Konfigurasi yang digunakan dalam penelitian ini adalah _depth_ = 5 dengan _base_channels_ = 32, menghasilkan progresi kanal $[32, 64, 128, 256, 256]$. Dua blok terakhir menggunakan jumlah kanal yang sama (256), di mana jalur pintasan pada blok kelima berupa operasi identitas karena dimensi input dan output sudah sesuai.

Tabel 3.5 Arsitektur _Layer-by-Layer_ FreqCNN (_depth_ = 5, _base_channels_ = 32)

| _Layer_         | Tipe                                              | Dimensi Input    | Dimensi Output   | Parameter       |
| --------------- | ------------------------------------------------- | ---------------- | ---------------- | --------------- |
| FreqBlock 1     | Conv(1→32, 3×3) + BN + Shortcut(1×1) + MaxPool    | $(1, 224, 224)$  | $(32, 112, 112)$ | $\sim 384$      |
| FreqBlock 2     | Conv(32→64, 3×3) + BN + Shortcut(1×1) + MaxPool   | $(32, 112, 112)$ | $(64, 56, 56)$   | $\sim 20.700$   |
| FreqBlock 3     | Conv(64→128, 3×3) + BN + Shortcut(1×1) + MaxPool  | $(64, 56, 56)$   | $(128, 28, 28)$  | $\sim 82.300$   |
| FreqBlock 4     | Conv(128→256, 3×3) + BN + Shortcut(1×1) + MaxPool | $(128, 28, 28)$  | $(256, 14, 14)$  | $\sim 328.000$  |
| FreqBlock 5     | Conv(256→256, 3×3) + BN + Identity + MaxPool      | $(256, 14, 14)$  | $(256, 7, 7)$    | $\sim 590.000$  |
| Dropout2d(0,2)  | _Spatial dropout_                                 | $(256, 7, 7)$    | $(256, 7, 7)$    | 0               |
| AdaptiveAvgPool | _Global average pooling_                          | $(256, 7, 7)$    | $(256, 1, 1)$    | 0               |
| FC 1            | Linear(256→128) + ReLU                            | $(256)$          | $(128)$          | $\sim 33.000$   |
| Dropout(0,3)    | _Dropout_                                         | $(128)$          | $(128)$          | 0               |
| FC 2            | Linear(128→1)                                     | $(128)$          | $(1)$            | $\sim 129$      |
| **Total**       |                                                   |                  |                  | **$\sim$ 700K** |

Meskipun jumlah parameter FreqCNN ($\sim 700.000$) lebih besar dibandingkan konfigurasi _depth_ = 3 ($\sim 130.000$), model ini tetap jauh lebih kecil dari XceptionNet ($\sim 22{,}8$ juta parameter). Kedalaman 5 blok dipilih untuk mengekstraksi fitur frekuensi yang lebih kaya — blok-blok tambahan memungkinkan model menangkap pola spektral pada berbagai tingkat abstraksi, dari artefak frekuensi rendah (seperti distribusi energi global) hingga anomali frekuensi tinggi (seperti _spectral rolloff_ dan _checkerboard patterns_). Koneksi residual memastikan bahwa pelatihan tetap stabil meskipun kedalaman jaringan bertambah.

Kedalaman FreqCNN dapat dikonfigurasi melalui parameter `freq_depth` dan `freq_base_channels` (jumlah kanal awal, _default_ 32). Jumlah kanal berlipat dua pada setiap blok hingga batas maksimum $8 \times \text{base\_channels} = 256$.

#### 3.4.2.2 Contoh Perhitungan _Forward Pass_

Berikut ditunjukkan contoh perhitungan _forward pass_ pada satu blok konvolusional FreqCNN dengan input sederhana berukuran $4 \times 4$, satu kanal.

**Input** (peta _magnitude_ FFT tersederhanakan):

$$
\mathbf{X} = \begin{bmatrix} 2{,}1 & 3{,}5 & 1{,}2 & 4{,}0 \\ 0{,}8 & 2{,}3 & 3{,}1 & 1{,}5 \\ 4{,}2 & 1{,}0 & 2{,}7 & 3{,}3 \\ 1{,}6 & 3{,}8 & 0{,}5 & 2{,}9 \end{bmatrix} \tag{3.19}
$$

**Konvolusi** dengan _kernel_ $3 \times 3$ (misalkan bobot $\mathbf{W}$ dan bias $b = 0$), _padding_ = 1:

Posisi $(0, 0)$ dengan _zero padding_:

$$
z_{0,0} = 0 \cdot w_{00} + 0 \cdot w_{01} + 0 \cdot w_{02} + 0 \cdot w_{10} + 2{,}1 \cdot w_{11} + 3{,}5 \cdot w_{12} + 0 \cdot w_{20} + 0{,}8 \cdot w_{21} + 2{,}3 \cdot w_{22} \tag{3.20}
$$

**BatchNorm:** Setelah seluruh posisi dihitung, _batch normalization_ menormalisasi output:

$$
\hat{z}_i = \frac{z_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \cdot \gamma + \beta \tag{3.21}
$$

di mana $\mu_B$ dan $\sigma_B^2$ adalah rata-rata dan varians _mini-batch_, $\gamma$ dan $\beta$ adalah parameter _learnable_, dan $\epsilon = 10^{-5}$ mencegah pembagian dengan nol.

**ReLU:** $\text{ReLU}(\hat{z}) = \max(0, \hat{z})$. Nilai negatif diubah menjadi nol.

**MaxPool2d(2):** Pada grid $2 \times 2$, diambil nilai maksimum. Dari output $4 \times 4$, dihasilkan peta fitur berukuran $2 \times 2$.

### 3.4.3 Model _Hybrid_ — HybridTwoBranch (_Late Fusion_)

Model _hybrid_ merupakan kontribusi utama penelitian ini. Arsitektur HybridTwoBranch menggabungkan fitur dari domain spasial dan domain frekuensi melalui mekanisme _late fusion_ — kedua cabang mengekstraksi fitur secara independen, kemudian fitur digabungkan dan diproses bersama untuk klasifikasi akhir.

#### 3.4.3.1 Cabang Spasial (XceptionNet _Backbone_)

Cabang spasial menggunakan XceptionNet sebagai _feature extractor_ dengan konfigurasi `num_classes=0`, yang berarti lapisan klasifikasi dihilangkan dan model hanya menghasilkan vektor fitur. Input berupa citra RGB berukuran $(3, 224, 224)$ yang telah dinormalisasi menggunakan statistik ImageNet. Output berupa vektor fitur berdimensi 2.048 yang merepresentasikan fitur spasial tingkat tinggi dari citra wajah.

#### 3.4.3.2 Cabang Frekuensi (FreqCNN _Backbone_)

Cabang frekuensi menggunakan bagian _backbone_ dari FreqCNN (blok konvolusional + _global average pooling_) tanpa lapisan klasifikasi. Input berupa peta _magnitude_ FFT berukuran $(1, 224, 224)$ yang telah dinormalisasi menggunakan _z-score_ per dataset. Output berupa vektor fitur berdimensi 256 (pada konfigurasi _depth_ = 5) yang merepresentasikan pola frekuensi dalam citra.

#### 3.4.3.3 _Projection Layers_ dan Penyeimbangan Dimensi

Tantangan utama dalam _late fusion_ adalah ketidakseimbangan dimensi antara kedua cabang. Cabang spasial menghasilkan vektor berdimensi 2.048, sedangkan cabang frekuensi 256 — rasio 8:1. Apabila kedua vektor langsung digabungkan (_concatenation_), fitur spasial akan mendominasi proses klasifikasi karena magnitudonya yang jauh lebih besar.

Untuk mengatasi hal ini, kedua cabang diproyeksikan ke dimensi yang sama ($\text{PROJ\_DIM} = 256$) melalui lapisan proyeksi:

$$
\mathbf{h}_{\text{spatial}} = \text{ReLU}(\text{BN}(\mathbf{W}_s \cdot \mathbf{f}_{\text{spatial}} + \mathbf{b}_s)) \tag{3.22}
$$

$$
\mathbf{h}_{\text{freq}} = \text{ReLU}(\text{BN}(\mathbf{W}_f \cdot \mathbf{f}_{\text{freq}} + \mathbf{b}_f)) \tag{3.23}
$$

di mana $\mathbf{W}_s \in \mathbb{R}^{256 \times 2048}$ dan $\mathbf{W}_f \in \mathbb{R}^{256 \times 256}$ adalah matriks bobot proyeksi, BN adalah _batch normalization_ 1D, dan ReLU adalah fungsi aktivasi. Setelah proyeksi, kedua cabang memiliki representasi berdimensi sama (256) yang dapat digabungkan secara seimbang.

#### 3.4.3.4 _Squeeze-and-Excitation_ (SE) _Gating_

Setelah kedua vektor fitur terproyeksi digabungkan melalui konkatenasi ($\mathbf{h}_{\text{fused}} = [\mathbf{h}_{\text{spatial}}; \mathbf{h}_{\text{freq}}] \in \mathbb{R}^{512}$), diterapkan mekanisme _Squeeze-and-Excitation_ (SE) _gating_ (Hu et al., 2018) yang memungkinkan model mempelajari bobot kepentingan per dimensi fitur secara adaptif.

Arsitektur SE _gate_ terdiri dari:

1. **_Squeeze_** — Kompresi vektor fusi dari 512 dimensi ke 128 dimensi melalui transformasi linier, diikuti aktivasi ReLU.
2. **_Excitation_** — Ekspansi kembali ke 512 dimensi melalui transformasi linier, diikuti fungsi _sigmoid_ yang menghasilkan bobot gerbang (_gate weights_) pada rentang $[0, 1]$.
3. **Pengalian elemen** — Vektor fusi asli dikalikan secara elemen-per-elemen (_element-wise_) dengan bobot gerbang.

Secara matematis:

$$
\mathbf{g} = \sigma(\mathbf{W}_2 \cdot \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_{\text{fused}} + \mathbf{b}_1) + \mathbf{b}_2) \tag{3.24}
$$

$$
\hat{\mathbf{h}}_{\text{fused}} = \mathbf{h}_{\text{fused}} \odot \mathbf{g} \tag{3.25}
$$

di mana $\mathbf{W}_1 \in \mathbb{R}^{128 \times 512}$, $\mathbf{W}_2 \in \mathbb{R}^{512 \times 128}$, $\sigma$ adalah fungsi _sigmoid_, dan $\odot$ adalah perkalian elemen. Mekanisme ini memungkinkan model untuk menekan (_suppress_) fitur yang tidak informatif dan memperkuat (_enhance_) fitur yang diskriminatif, baik dari cabang spasial maupun frekuensi, secara adaptif berdasarkan input.

#### 3.4.3.5 _Classifier Head_

Vektor fitur yang telah melalui SE _gating_ ($\hat{\mathbf{h}}_{\text{fused}} \in \mathbb{R}^{512}$) diteruskan ke kepala klasifikasi (_classifier head_) yang terdiri dari:

1. **Dropout(0,3)** — Regularisasi pada representasi fusi untuk mencegah _overfitting_, dengan tingkat _dropout_ yang moderat agar tidak menghilangkan terlalu banyak sinyal pada dataset berukuran kecil.
2. **Linear(512 → 128)** — Reduksi dimensi.
3. **ReLU** — Fungsi aktivasi.
4. **Dropout(0,3)** — Regularisasi tambahan.
5. **Linear(128 → 1)** — Menghasilkan satu nilai _logit_ untuk klasifikasi biner.

Output _logit_ diproses oleh fungsi _loss_ BCEWithLogitsLoss yang secara internal menerapkan fungsi _sigmoid_ sebelum menghitung _binary cross-entropy_.

#### 3.4.3.6 Contoh Perhitungan _Late Fusion_

Berikut ditunjukkan contoh perhitungan _late fusion_ yang disederhanakan dengan dimensi kecil untuk ilustrasi.

**Langkah 1: Fitur input** (disederhanakan ke 4 dimensi per cabang):

$$
\mathbf{f}_{\text{spatial}} = [0{,}8;\ 1{,}2;\ -0{,}3;\ 0{,}5], \quad \mathbf{f}_{\text{freq}} = [0{,}4;\ -0{,}1;\ 0{,}7;\ 0{,}2] \tag{3.26}
$$

**Langkah 2: Proyeksi** ($4 \rightarrow 4$, disederhanakan tanpa BN):

Misalkan $\mathbf{W}_s$ dan $\mathbf{W}_f$ adalah matriks identitas, maka $\mathbf{h}_{\text{spatial}} = \text{ReLU}(\mathbf{f}_{\text{spatial}}) = [0{,}8;\ 1{,}2;\ 0;\ 0{,}5]$ dan $\mathbf{h}_{\text{freq}} = \text{ReLU}(\mathbf{f}_{\text{freq}}) = [0{,}4;\ 0;\ 0{,}7;\ 0{,}2]$.

**Langkah 3: Konkatenasi:**

$$
\mathbf{h}_{\text{fused}} = [0{,}8;\ 1{,}2;\ 0;\ 0{,}5;\ 0{,}4;\ 0;\ 0{,}7;\ 0{,}2] \in \mathbb{R}^8 \tag{3.27}
$$

**Langkah 4: SE _Gating_** ($8 \rightarrow 2 \rightarrow 8$, _reduction_ = 4):

_Squeeze_: $\mathbf{s} = \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_{\text{fused}})$. Misalkan hasilnya $\mathbf{s} = [1{,}5;\ 0{,}8]$.

_Excitation_: $\mathbf{g} = \sigma(\mathbf{W}_2 \cdot \mathbf{s})$. Misalkan hasilnya $\mathbf{g} = [0{,}9;\ 0{,}7;\ 0{,}3;\ 0{,}8;\ 0{,}6;\ 0{,}2;\ 0{,}9;\ 0{,}5]$.

_Gating_:

$$
\hat{\mathbf{h}}_{\text{fused}} = \mathbf{h}_{\text{fused}} \odot \mathbf{g} = [0{,}72;\ 0{,}84;\ 0;\ 0{,}40;\ 0{,}24;\ 0;\ 0{,}63;\ 0{,}10] \tag{3.28}
$$

Terlihat bahwa SE _gate_ menekan dimensi ke-3 dan ke-6 (nilai _gate_ rendah: 0,3 dan 0,2) sambil mempertahankan dimensi ke-1 dan ke-7 (nilai _gate_ tinggi: 0,9 dan 0,9). Mekanisme ini memungkinkan model untuk secara adaptif memilih fitur yang paling diskriminatif dari kedua cabang.

**Langkah 5: Klasifikasi:**

_Logit_: $z = \mathbf{w}^T \hat{\mathbf{h}}_{\text{fused}} + b$. Misalkan $z = 2{,}1$.

Probabilitas: $p = \sigma(2{,}1) = \frac{1}{1 + e^{-2{,}1}} = 0{,}891$.

Prediksi: $p > 0{,}5 \Rightarrow$ _fake_ (label 1).

### 3.4.4 Perbandingan Arsitektur Model

Tabel 3.6 Perbandingan Tiga Arsitektur Model

| Aspek           | _Spatial_ (XceptionNet)    | _Frequency_ (FreqCNN)    | _Hybrid_ (HybridTwoBranch)      |
| --------------- | -------------------------- | ------------------------ | ------------------------------- |
| Input           | RGB$(3, 224, 224)$         | FFT$(1, 224, 224)$       | RGB + FFT (terpisah)            |
| _Backbone_      | XceptionNet (_pretrained_) | FreqCNN (_from scratch_) | XceptionNet + FreqCNN           |
| Dimensi fitur   | 2.048                      | 256                      | $256 + 256 = 512$ (terproyeksi) |
| Mekanisme fusi  | —                          | —                        | Konkatenasi + SE*Gating*        |
| Total parameter | $\sim 22{,}8$ juta         | $\sim 700$ ribu          | $\sim 23{,}8$ juta              |
| _Pretrained_    | Ya (ImageNet)              | Tidak                    | Parsial (cabang spasial)        |
| Domain          | Spasial                    | Frekuensi                | Keduanya                        |

Tabel 3.7 Dimensi Fitur per Komponen Model _Hybrid_

| Komponen              | Dimensi Input   | Dimensi Output | Operasi                    |
| --------------------- | --------------- | -------------- | -------------------------- |
| XceptionNet*backbone* | $(3, 224, 224)$ | 2.048          | Ekstraksi fitur + GAP      |
| FreqCNN*backbone*     | $(1, 224, 224)$ | 256            | 5 FreqBlock residual + GAP |
| Proyeksi spasial      | 2.048           | 256            | Linear + BN + ReLU         |
| Proyeksi frekuensi    | 256             | 256            | Linear + BN + ReLU         |
| Konkatenasi           | $256 + 256$     | 512            | `torch.cat`                |
| SE*Gate*              | 512             | 512            | _Squeeze-Excitation_       |
| _Classifier_          | 512             | 1              | FC + Dropout               |

<!-- Gambar 3.5: Diagram Arsitektur XceptionNet (simplified) -->

> Gambar 3.7 Diagram Arsitektur XceptionNet

<!-- Gambar 3.6: Diagram Arsitektur FreqCNN -->

> Gambar 3.8 Diagram Arsitektur FreqCNN

<!-- Gambar 3.7: Diagram Arsitektur HybridTwoBranch -->

<!--
RGB (3,224,224) → [XceptionNet Backbone] → (2048) → [Proj: Linear→BN→ReLU] → (256) ─┐
                   (frozen 3 epochs)                  (2048→256)                        │
                                                                                        ├→ [Concat] → (512) → [SE Gate] → (512) → [Classifier] → logit
FFT (1,224,224) → [FreqCNN Backbone] → (256) → [Proj: Linear→BN→ReLU] → (256) ────────┘
                   (5 FreqBlocks residual)       (256→256)
-->

> Gambar 3.9 Diagram Arsitektur HybridTwoBranch (_Late Fusion_)

---

## 3.5 Strategi Pelatihan Model

Strategi pelatihan yang tepat sangat menentukan performa akhir model, terutama pada arsitektur *hybrid* yang menggabungkan komponen *pretrained* (XceptionNet) dengan komponen yang dilatih dari awal (FreqCNN). Beberapa teknik optimasi diterapkan untuk mengatasi tantangan ini, termasuk *transfer learning* dengan *backbone freezing*, *differential learning rate*, penjadwalan *learning rate* adaptif, serta mekanisme *early stopping* untuk mencegah *overfitting*. Bagian berikut menjelaskan setiap strategi secara detail.

### 3.5.1 _Transfer Learning_ dan _Backbone Freezing_

Strategi _transfer learning_ diterapkan pada model _spatial_ dan _hybrid_ yang menggunakan _backbone_ XceptionNet. Bobot yang telah dilatih pada ImageNet memberikan inisialisasi yang kuat, sehingga model tidak perlu mempelajari fitur visual dasar dari awal.

Pada seluruh model yang menggunakan _backbone_ XceptionNet _pretrained_ — yaitu model _spatial_, _hybrid_, dan _early fusion_ — _backbone_ dibekukan (_frozen_) selama 3 _epoch_ pertama pelatihan. Selama periode ini, hanya parameter lapisan baru yang diperbarui: pada model _spatial_, lapisan klasifikasi akhir (_head_); pada model _hybrid_, FreqCNN, proyeksi, SE _gate_, dan _classifier_; pada model _early fusion_, seluruh parameter _backbone_ dibekukan. Pembekuan ini bertujuan agar lapisan-lapisan baru yang diinisialisasi secara acak dapat mempelajari representasi yang bermakna terlebih dahulu sebelum gradien mengalir ke _backbone_ yang telah _pretrained_. Tanpa pembekuan, gradien acak dari lapisan baru yang belum terlatih dapat merusak bobot _pretrained_ yang sudah optimal (_catastrophic forgetting_).

Pada _epoch_ ke-4, seluruh parameter _backbone_ dilepaskan (_unfreezing_) dengan pemanggilan `requires_grad_(True)`, memungkinkan _fine-tuning_ menyeluruh untuk mengadaptasi fitur ImageNet ke domain deteksi _deepfake_.

### 3.5.2 _Differential Learning Rate_

Untuk melindungi bobot _pretrained_ yang sudah berkualitas sambil memungkinkan lapisan baru belajar dengan cepat, digunakan _differential learning rate_ — laju pembelajaran yang berbeda untuk kelompok parameter yang berbeda:

Tabel 3.8 _Learning Rate_ per Kelompok Parameter

| Kelompok Parameter        | _Learning Rate_                | Diterapkan Pada                           |
| ------------------------- | ------------------------------ | ----------------------------------------- |
| _Backbone_ (_pretrained_) | $2 \times 10^{-5}$ (base / 10) | Parameter XceptionNet                     |
| _Head_ (lapisan baru)     | $2 \times 10^{-4}$ (base)      | FreqCNN, proyeksi, SE*gate*, _classifier_ |

_Learning rate_ _backbone_ yang 10 kali lebih rendah memastikan bahwa _fine-tuning_ dilakukan secara halus tanpa menghancurkan representasi visual yang telah dipelajari dari ImageNet, sementara lapisan baru mendapat _learning rate_ yang lebih tinggi untuk konvergensi yang lebih cepat.

### 3.5.3 Penjadwalan _Learning Rate_

Penjadwalan _learning rate_ menggabungkan dua fase menggunakan `SequentialLR`:

1. **_Linear warmup_** (2 _epoch_) — _Learning rate_ dinaikkan secara linier dari 10% ke 100% dari nilai _base_. `LinearLR(start_factor=0.1, end_factor=1.0, total_iters=2)`. Fase ini mencegah pembaruan bobot yang terlalu besar pada iterasi awal, terutama penting pada _backbone pretrained_.
2. **_Cosine annealing_** (_epoch_ ke-3 hingga selesai) — _Learning rate_ diturunkan secara halus mengikuti kurva kosinus dari nilai _base_ menuju $1 \times 10^{-6}$. `CosineAnnealingLR(T_max=max(epochs-2, 1), eta_min=1e-6)`. Penurunan yang mulus ini menghindari _shock_ akibat penurunan LR yang tiba-tiba.

Kurva _learning rate_ untuk pelatihan 30 _epoch_:

- _Epoch_ 1: $\text{LR} = 0{,}1 \times \text{base} = 2 \times 10^{-5}$
- _Epoch_ 2: $\text{LR} = 1{,}0 \times \text{base} = 2 \times 10^{-4}$
- _Epoch_ 3–30: _Cosine decay_ dari $2 \times 10^{-4}$ menuju $1 \times 10^{-6}$

<!-- Gambar 3.8: Kurva Learning Rate Schedule -->

> Gambar 3.10 Kurva Penjadwalan _Learning Rate_ (_Warmup_ + _Cosine Decay_)

### 3.5.4 Fungsi _Loss_ — BCEWithLogitsLoss dengan _Pos Weight_

Fungsi _loss_ yang digunakan adalah _Binary Cross-Entropy with Logits_ (BCEWithLogitsLoss), sebagaimana telah dibahas pada BAB II, yang menggabungkan fungsi _sigmoid_ dan _binary cross-entropy_ dalam satu operasi yang stabil secara numerik:

$$
\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\left[w_p \cdot y_i \cdot \log(\sigma(z_i)) + (1 - y_i) \cdot \log(1 - \sigma(z_i))\right] \tag{3.29}
$$

di mana $z_i$ adalah _logit_ (output model sebelum _sigmoid_), $\sigma(z) = \frac{1}{1 + e^{-z}}$ adalah fungsi _sigmoid_, $y_i$ adalah label target, dan $w_p$ adalah _pos_weight_ untuk penyeimbangan kelas.

#### 3.5.4.1 Penyeimbangan Kelas (_Pos Weight_)

Untuk menangani ketidakseimbangan kelas yang dapat terjadi pada pembagian dataset, diterapkan _positive class weighting_:

$$
w_p = \frac{n_{\text{neg}}}{n_{\text{pos}}} \tag{3.30}
$$

di mana $n_{\text{neg}}$ dan $n_{\text{pos}}$ adalah jumlah sampel kelas negatif (_real_) dan positif (_fake_) dalam set pelatihan. Bobot ini dikalikan pada komponen _loss_ untuk sampel positif, sehingga kelas minoritas mendapat pengaruh lebih besar pada pembaruan gradien. Apabila dataset seimbang ($n_{\text{neg}} = n_{\text{pos}}$), maka $w_p = 1$ dan fungsi _loss_ menjadi BCEWithLogitsLoss standar.

#### 3.5.4.2 _Label Smoothing_

_Label smoothing_ merupakan teknik regularisasi yang dapat diterapkan untuk mencegah model menjadi terlalu percaya diri (_overconfident_):

$$
y'_i = y_i \times (1 - \alpha) + \alpha \times 0{,}5 \tag{3.31}
$$

Sebagai ilustrasi, dengan $\alpha = 0{,}02$, transformasi ini mengubah label biner menjadi: $0 \rightarrow 0{,}01$ dan $1 \rightarrow 0{,}99$, sehingga model tidak perlu mendorong _logit_ ke nilai ekstrem ($\pm \infty$).

Pada konfigurasi akhir yang digunakan dalam eksperimen ini, _label smoothing_ dinonaktifkan ($\alpha = 0$) untuk memaksimalkan sinyal pelatihan pada dataset dengan ukuran sampel kecil (mulai dari $n = 100$). Pada dataset berukuran kecil, sinyal positif yang terbatas menjadi semakin lemah apabila label di-_smooth_, sehingga model kesulitan membedakan kelas _real_ dan _fake_.

#### 3.5.4.3 Contoh Perhitungan BCEWithLogitsLoss

Sebagai ilustrasi, berikut ditunjukkan contoh perhitungan BCEWithLogitsLoss dengan _label smoothing_ $\alpha = 0{,}02$ (walaupun pada konfigurasi akhir $\alpha = 0$, contoh ini menunjukkan mekanisme penuh). Misalkan _logit_ output model $z = 2{,}5$, label asli $y = 1$ (_fake_), dan $w_p = 1$ (dataset seimbang).

**Langkah 1: _Label smoothing_:**

$$
y' = 1 \times (1 - 0{,}02) + 0{,}02 \times 0{,}5 = 0{,}98 + 0{,}01 = 0{,}99 \tag{3.32}
$$

**Langkah 2: _Sigmoid_:**

$$
\sigma(2{,}5) = \frac{1}{1 + e^{-2{,}5}} = \frac{1}{1 + 0{,}0821} = \frac{1}{1{,}0821} = 0{,}924 \tag{3.33}
$$

**Langkah 3: _Loss_:**

$$
\mathcal{L} = -\left[w_p \cdot 0{,}99 \cdot \log(0{,}924) + 0{,}01 \cdot \log(1 - 0{,}924)\right] \tag{3.34}
$$

$$
= -\left[1 \times 0{,}99 \times (-0{,}0791) + 0{,}01 \times (-2{,}577)\right]
$$

$$
= -\left[-0{,}0783 + (-0{,}0258)\right] = -(-0{,}1041) = 0{,}1041
$$

Nilai _loss_ yang rendah (0,1041) menunjukkan bahwa prediksi model (probabilitas 0,924 untuk _fake_) sudah mendekati label target. Pada awal pelatihan, nilai _loss_ umumnya jauh lebih tinggi dan menurun seiring konvergensi model.

### 3.5.5 Optimisasi — AdamW dengan _Gradient Accumulation_

Optimizer yang digunakan adalah AdamW (Loshchilov & Hutter, 2019), varian dari Adam (Kingma & Ba, 2015) dengan _decoupled weight decay_, dengan konfigurasi $\text{lr} = 2 \times 10^{-4}$ dan $\text{weight\_decay} = 1 \times 10^{-4}$. Berbeda dengan Adam standar yang menambahkan regularisasi L2 ke gradien sebelum penskalaan adaptif, AdamW menerapkan _weight decay_ secara langsung pada bobot setelah langkah pembaruan Adam. Perbedaan ini penting karena pada Adam standar, efektif regularisasi bervariasi antar parameter bergantung pada _learning rate_ adaptifnya, sedangkan pada AdamW, regularisasi konsisten untuk semua parameter. Konsistensi ini sangat bermanfaat dalam skenario _transfer learning_ di mana parameter _pretrained_ dan parameter baru memiliki skala gradien yang sangat berbeda.

_Gradient accumulation_ diterapkan dengan `accum_steps = 2`, yang berarti gradien diakumulasikan selama 2 _batch_ sebelum pembaruan bobot dilakukan. Dengan ukuran _batch_ per langkah sebesar 16, ukuran _batch_ efektif menjadi $16 \times 2 = 32$. Teknik ini memungkinkan penggunaan _batch_ efektif yang lebih besar tanpa meningkatkan kebutuhan memori GPU. _Loss_ dibagi dengan `accum_steps` sebelum _backpropagation_ untuk menjaga skala gradien yang konsisten.

### 3.5.6 _Gradient Clipping_

_Gradient clipping_ berdasarkan norma L2 diterapkan dengan batas $\text{max\_norm} = 5{,}0$:

$$
\mathbf{g} \leftarrow \begin{cases} \mathbf{g} & \text{jika } \|\mathbf{g}\|_2 \leq 5{,}0 \\ \frac{5{,}0 \cdot \mathbf{g}}{\|\mathbf{g}\|_2} & \text{jika } \|\mathbf{g}\|_2 > 5{,}0 \end{cases} \tag{3.35}
$$

Ambang batas 5,0 dipilih untuk mengakomodasi _learning rate_ yang lebih tinggi ($2 \times 10^{-4}$) sambil tetap mencegah ledakan gradien (_gradient explosion_), terutama pada _epoch_ ke-4 ketika _backbone_ XceptionNet dilepaskan (_unfreezing_) dan aliran gradien dari seluruh jaringan secara tiba-tiba meningkatkan norma gradien. Pada implementasi dengan _mixed precision_ (AMP), `scaler.unscale_()` dipanggil sebelum _clipping_ untuk memastikan gradien berada pada skala aslinya.

### 3.5.7 _Mixed Precision Training_ (AMP)

Pelatihan dengan presisi campuran (_Automatic Mixed Precision_ / AMP) diterapkan pada GPU CUDA menggunakan `torch.cuda.amp.autocast()` dan `GradScaler`. Dalam mode ini, operasi _forward pass_ dan _backward pass_ dilakukan dalam format _float16_ (setengah presisi), sedangkan pembaruan bobot oleh _optimizer_ dilakukan dalam format _float32_ (presisi penuh). AMP memberikan percepatan pelatihan hingga $\sim 2\times$ dengan penurunan akurasi yang minimal. Optimisasi TF32 juga diaktifkan untuk GPU arsitektur Ampere ke atas.

### 3.5.8 _Early Stopping_

Mekanisme _early stopping_ digunakan untuk menghentikan pelatihan secara otomatis ketika model tidak lagi menunjukkan peningkatan performa pada set validasi. Konfigurasi yang digunakan:

- **Metrik pemantauan:** AUC validasi (metrik utama).
- **Kesabaran (_patience_):** 10 _epoch_ berturut-turut tanpa peningkatan AUC.
- **Jumlah _epoch_ maksimum:** 30.
- **Tindakan:** Pelatihan dihentikan dan _checkpoint_ terbaik digunakan untuk evaluasi.

Peningkatan _patience_ dari 5 ke 10 _epoch_ memberikan waktu yang cukup bagi model untuk pulih dari degradasi performa sementara yang sering terjadi setelah _unfreezing backbone_ pada _epoch_ ke-4. Tanpa _patience_ yang memadai, _early stopping_ dapat menghentikan pelatihan terlalu dini sebelum model beradaptasi dengan parameter _backbone_ yang baru dilepaskan.

AUC dipilih sebagai metrik pemantauan karena bersifat independen terhadap _threshold_ — mengevaluasi kemampuan model membedakan kelas positif dan negatif pada seluruh kemungkinan _threshold_, berbeda dengan akurasi yang bergantung pada satu nilai _threshold_ tertentu.

### 3.5.9 Seleksi Model Terbaik

Pada setiap _epoch_, apabila AUC validasi meningkat dibandingkan nilai terbaik sebelumnya, _checkpoint_ model disimpan dalam format `{"state_dict": ..., "epoch": ..., "config": ...}`. _Checkpoint_ terbaik berdasarkan AUC validasi tertinggi digunakan untuk evaluasi akhir pada set pengujian.

Tabel 3.9 Ringkasan _Hyperparameter_ Pelatihan

| Parameter                    | Nilai                             | Keterangan                                           |
| ---------------------------- | --------------------------------- | ---------------------------------------------------- |
| _Optimizer_                  | AdamW                             | _Decoupled weight decay_ (Loshchilov & Hutter, 2019) |
| _Learning rate_ (_base_)     | $2 \times 10^{-4}$                | Lapisan baru                                         |
| _Learning rate_ (_backbone_) | $2 \times 10^{-5}$                | XceptionNet*pretrained* (base/10)                    |
| _Weight decay_               | $1 \times 10^{-4}$                | _Decoupled weight decay_                             |
| _Batch size_                 | 16                                | Per langkah; efektif 32                              |
| _Gradient accumulation_      | 2 langkah                         | Semua model;_batch_ efektif = 32                     |
| _Epoch_ maksimum             | 30                                | Dibatasi*early stopping*                             |
| _Early stopping patience_    | 10                                | Tanpa peningkatan AUC                                |
| _Label smoothing_            | 0,0 (nonaktif)                    | Dinonaktifkan untuk dataset kecil                    |
| _Pos weight_                 | $n_{\text{neg}} / n_{\text{pos}}$ | Penyeimbangan kelas                                  |
| _Gradient clipping_          | max_norm = 5,0                    | Norma L2                                             |
| _LR warmup_                  | 2*epoch*                          | 10% → 100% linear                                    |
| _LR schedule_                | _Cosine annealing_                | Decay ke$1 \times 10^{-6}$                           |
| _Backbone freeze_            | 3*epoch*                          | Semua model*pretrained*                              |
| _Mixed precision_            | AMP (_float16_)                   | CUDA saja                                            |
| FreqCNN*depth*               | 5                                 | $\sim 700$K parameter                                |
| _Seed_                       | 0, 1, 2                           | Reproduktibilitas (3*seed*)                          |
| _Framework_                  | PyTorch + timm                    | XceptionNet via timm                                 |

---

## 3.6 Desain Eksperimen

Desain eksperimen dirancang untuk mengevaluasi secara sistematis kontribusi masing-masing domain analisis serta keunggulan pendekatan *hybrid* dalam deteksi *deepfake*. Evaluasi dilakukan melalui eksperimen faktorial yang mengkombinasikan tiga variabel utama: arsitektur model, dataset pelatihan, dan ukuran sampel. Setiap konfigurasi diuji secara *in-dataset* maupun *cross-dataset* untuk mengukur kemampuan generalisasi, dan setiap eksperimen diulang dengan beberapa *seed* berbeda untuk memperoleh estimasi performa yang reliabel.

### 3.6.1 Matriks Eksperimen

Penelitian ini dirancang sebagai eksperimen faktorial yang menguji kombinasi dari tiga faktor utama: arsitektur model, dataset pelatihan, dan ukuran sampel. Setiap kombinasi dijalankan dengan tiga _seed_ berbeda untuk memperoleh estimasi rata-rata dan simpangan baku yang reliabel.

Tabel 3.10 Matriks Eksperimen

| Dimensi            | Nilai                         | Jumlah |
| ------------------ | ----------------------------- | ------ |
| Model              | _spatial_, _freq_, _hybrid_   | 3      |
| Dataset pelatihan  | FFPP, CDF                     | 2      |
| Ukuran sampel FFPP | 100, 300, 600, 1000           | 4      |
| Ukuran sampel CDF  | 100, 250, 500, 750            | 4      |
| _Seed_             | 0, 1, 2                       | 3      |
| Evaluasi           | _In-dataset_, _cross-dataset_ | 2      |

Total pelatihan: $3 \times 2 \times 4 \times 3 = 72$ _run_.
Total evaluasi: $72 \times 2 = 144$ evaluasi (setiap model dievaluasi secara _in-dataset_ dan _cross-dataset_).

### 3.6.2 Evaluasi _In-Dataset_

Evaluasi _in-dataset_ mengukur performa model pada set pengujian dari dataset yang sama dengan dataset pelatihan:

- Model dilatih pada FFPP → dievaluasi pada set pengujian FFPP.
- Model dilatih pada CDF → dievaluasi pada set pengujian CDF.

Evaluasi ini mengukur seberapa baik model mempelajari pola _deepfake_ dari distribusi data pelatihannya.

### 3.6.3 Evaluasi _Cross-Dataset_

Evaluasi _cross-dataset_ mengukur kemampuan generalisasi model pada dataset yang berbeda dari dataset pelatihan:

- Model dilatih pada FFPP → dievaluasi pada set pengujian CDF.
- Model dilatih pada CDF → dievaluasi pada set pengujian FFPP.

Evaluasi silang ini sangat penting karena dalam skenario nyata, detektor _deepfake_ harus mampu mengenali manipulasi dari metode yang belum pernah dilihat selama pelatihan. Perbedaan performa antara evaluasi _in-dataset_ dan _cross-dataset_ diukur melalui metrik **generalisasi _drop_**:

$$
\Delta = \text{F1}_{\text{in-dataset}} - \text{F1}_{\text{cross-dataset}} \tag{3.36}
$$

Nilai $\Delta$ yang besar menunjukkan bahwa model terlalu bergantung pada pola spesifik dataset pelatihan dan tidak memiliki kemampuan generalisasi yang baik.

### 3.6.4 Variabel Penelitian

Variabel penelitian diklasifikasikan menjadi tiga jenis: variabel independen yang dimanipulasi secara sistematis, variabel dependen yang diukur sebagai indikator performa, dan variabel kontrol yang dijaga konstan untuk memastikan validitas perbandingan antar eksperimen. Tabel 3.11 merangkum seluruh variabel yang terlibat dalam penelitian ini.

Tabel 3.11 Variabel Penelitian

| Jenis          | Variabel                                           | Nilai                                              |
| -------------- | -------------------------------------------------- | -------------------------------------------------- |
| **Independen** | Arsitektur model                                   | _spatial_, _freq_, _hybrid_                        |
|                | Dataset pelatihan                                  | FFPP, CDF                                          |
|                | Ukuran sampel                                      | 100–1000 (bervariasi per dataset)                  |
| **Dependen**   | _Accuracy_, _Precision_, _Recall_, F1-_Score_, AUC | Kontinu$[0, 1]$                                    |
|                | _Generalization drop_ ($\Delta$)                   | $\text{F1}_{\text{in}} - \text{F1}_{\text{cross}}$ |
| **Kontrol**    | _Hyperparameter_ pelatihan                         | Tetap (Tabel 3.9)                                  |
|                | _Seed_                                             | 0, 1, 2                                            |
|                | Pembagian data                                     | 70/15/15 terstratifikasi                           |
|                | Ukuran citra                                       | $224 \times 224$                                   |

---

## 3.7 Metode Evaluasi Model

Evaluasi model dilakukan pada _frame-frame_ dari set pengujian (_test set_) yang telah dipisahkan pada level video untuk mencegah kebocoran data. Metrik evaluasi yang digunakan — _accuracy_, _precision_, _recall_, F1-_score_, dan AUC-ROC beserta _confusion matrix_ — telah didefinisikan secara detail pada BAB II. AUC digunakan sebagai metrik utama untuk seleksi model dan _early stopping_ karena sifatnya yang independen terhadap _threshold_. Selain evaluasi pada _threshold_ tetap ($\theta = 0{,}5$), penelitian ini juga menghitung _threshold_ optimal menggunakan statistik J Youden ($J = \text{TPR} - \text{FPR}$) yang memberikan keseimbangan optimal antara sensitivitas dan spesifisitas.

Pada bagian ini dibahas metrik tambahan yang spesifik untuk desain eksperimen silang dataset.

### 3.7.1 _Generalization Drop_

Metrik _generalization drop_ mengukur degradasi performa model ketika dievaluasi pada dataset yang berbeda dari dataset pelatihan:

$$
\Delta = \text{F1}_{\text{in-dataset}} - \text{F1}_{\text{cross-dataset}} \tag{3.37}
$$

Nilai $\Delta$ yang mendekati nol menunjukkan generalisasi yang baik — model mampu mendeteksi _deepfake_ dari metode yang belum pernah dilihat. Nilai $\Delta$ yang besar menunjukkan bahwa model menghafal pola spesifik dataset pelatihan.

### 3.7.2 Contoh Perhitungan Metrik

Sebagai ilustrasi, berikut ditunjukkan contoh perhitungan seluruh metrik dari suatu _confusion matrix_:

Tabel 3.12 Contoh _Confusion Matrix_

|                   | **Prediksi _Fake_** | **Prediksi _Real_** | **Total** |
| ----------------- | ------------------- | ------------------- | --------- |
| **Aktual _Fake_** | TP = 42             | FN = 8              | 50        |
| **Aktual _Real_** | FP = 5              | TN = 45             | 50        |
| **Total**         | 47                  | 53                  | 100       |

Tabel 3.13 Perhitungan Metrik Evaluasi

| Metrik      | Perhitungan                                             | Hasil     |
| ----------- | ------------------------------------------------------- | --------- |
| _Accuracy_  | $(42 + 45) / (42 + 45 + 5 + 8) = 87/100$                | $0{,}870$ |
| _Precision_ | $42 / (42 + 5) = 42/47$                                 | $0{,}894$ |
| _Recall_    | $42 / (42 + 8) = 42/50$                                 | $0{,}840$ |
| F1-_Score_  | $2 \times 0{,}894 \times 0{,}840 / (0{,}894 + 0{,}840)$ | $0{,}866$ |
| AUC         | (dihitung dari kurva ROC)                               | —         |

Dari contoh di atas, model berhasil mendeteksi 42 dari 50 _frame fake_ (_recall_ = 84%) dengan tingkat _false alarm_ yang rendah (5 dari 50 _frame real_ salah diklasifikasi, FPR = 10%). F1-_Score_ sebesar 0,866 menunjukkan keseimbangan yang baik antara _precision_ dan _recall_.
