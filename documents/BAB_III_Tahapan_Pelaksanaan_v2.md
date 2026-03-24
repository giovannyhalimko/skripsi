# BAB III TAHAPAN PELAKSANAAN

## 3.1 Kerangka Tahapan Pelaksanaan

### 3.1.1 Jenis dan Pendekatan Penelitian

Penelitian ini merupakan penelitian eksperimental di bidang *computer vision* dan *deep learning*. Fokus utama penelitian adalah merancang, mengimplementasikan, dan mengevaluasi model deteksi *deepfake* yang menggabungkan analisis domain spasial dan domain frekuensi secara bersamaan. Pendekatan eksperimental dipilih karena tujuan penelitian adalah mengevaluasi keampuhan metode baru dalam kondisi terkontrol, di mana variabel seperti dataset, arsitektur model, dan parameter pelatihan dapat dimanipulasi dan direplikasi secara konsisten.

Metode deteksi *deepfake* konvensional umumnya hanya memanfaatkan fitur spasial (tekstur, struktur wajah) atau bergantung pada model tunggal. Namun, pada kasus manipulasi yang canggih, artefak spasial dapat sangat halus sehingga sulit dideteksi oleh satu jenis fitur saja. Di sisi lain, citra hasil sintesis generatif (*GAN*) memiliki ketidaksempurnaan pada distribusi spektral yang tidak terlihat secara kasat mata namun terdeteksi melalui analisis frekuensi [1][2]. Oleh karena itu, penelitian ini mengusulkan pendekatan hibrida yang memadukan dua domain analisis:

1. **Analisis domain spasial** melalui jaringan konvolusional XceptionNet [3] yang telah terbukti efektif dalam mengekstraksi fitur visual tingkat tinggi dari citra wajah.

2. **Analisis domain frekuensi** melalui transformasi Fourier cepat (*Fast Fourier Transform* / FFT) yang diproses oleh jaringan konvolusional khusus (*FreqCNN*) untuk menangkap artefak spektral yang dihasilkan oleh proses sintesis *deepfake*.

Sebagai bagian dari desain eksperimental, penelitian ini membangun tiga varian model sebagai perbandingan terkontrol:

- **Model spasial** (*spatial*): hanya menggunakan fitur domain spasial (XceptionNet).
- **Model frekuensi** (*freq*): hanya menggunakan fitur domain frekuensi (FreqCNN pada peta FFT).
- **Model hibrida** (*hybrid*): menggabungkan kedua domain melalui arsitektur *late fusion* dengan mekanisme *Squeeze-and-Excitation* (SE) *gating*.

Desain tiga varian ini memungkinkan pengukuran kontribusi individual masing-masing domain serta evaluasi apakah penggabungan keduanya menghasilkan peningkatan performa deteksi dan generalisasi lintas dataset.

### 3.1.2 Tahapan Pelaksanaan Penelitian

Pelaksanaan penelitian ini terdiri dari lima tahapan utama:

1. **Pengumpulan Data** — Menggunakan dua dataset *benchmark* standar untuk deteksi *deepfake*, yaitu FaceForensics++ (FFPP) dan Celeb-DF v2 (CDF).

2. **Preprocessing** — Meliputi ekstraksi *frame* dari video, konversi domain frekuensi melalui FFT, normalisasi, serta augmentasi data.

3. **Perancangan Model** — Merancang tiga arsitektur model: *spatial* (XceptionNet), *frequency* (FreqCNN), dan *hybrid* (HybridTwoBranch) dengan mekanisme *late fusion* dan SE *gating*.

4. **Pelatihan dan Optimasi** — Melatih setiap model menggunakan strategi *transfer learning*, *differential learning rate*, penjadwalan *learning rate* (*warmup* + *cosine decay*), dan *early stopping* berdasarkan AUC.

5. **Pengujian dan Evaluasi** — Mengevaluasi setiap model secara *in-dataset* dan *cross-dataset* pada berbagai ukuran sampel, menggunakan metrik akurasi, presisi, *recall*, F1-*score*, dan AUC-ROC.

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

> Gambar 3.1 Flowchart Utama *Pipeline* Penelitian

---

## 3.2 Dataset dan Sumber Data

### 3.2.1 FaceForensics++ (FFPP)

Dataset pertama yang digunakan dalam penelitian ini adalah FaceForensics++ yang diperkenalkan oleh Rössler *et al.* [4]. FaceForensics++ merupakan salah satu *benchmark* standar yang paling banyak digunakan dalam penelitian deteksi *deepfake*. Dataset ini terdiri dari video wajah asli yang bersumber dari YouTube serta video hasil manipulasi menggunakan empat metode yang berbeda:

1. **Deepfakes** — Pertukaran wajah berbasis *autoencoder*.
2. **Face2Face** — Transfer ekspresi wajah secara *real-time*.
3. **FaceSwap** — Pertukaran wajah berbasis grafik komputer.
4. **NeuralTextures** — Manipulasi berbasis *neural rendering*.

Keberagaman metode manipulasi ini menjadikan FaceForensics++ sangat cocok untuk menguji ketahanan (*robustness*) model terhadap berbagai jenis artefak *deepfake*. Video dalam dataset tersedia dalam tiga tingkat kompresi: *raw* (tanpa kompresi), c23 (kompresi ringan), dan c40 (kompresi berat). Pada penelitian ini digunakan tingkat kompresi c23 yang merepresentasikan skenario distribusi video secara *online* yang realistis.

Pelabelan data dilakukan secara otomatis berdasarkan pencocokan kata kunci pada nama direktori. Video yang berada dalam direktori mengandung kata kunci "original", "real", atau "pristine" dilabeli sebagai *real* (label 0), sedangkan video dalam direktori mengandung kata kunci "fake", "manipulated", "deepfakes", "faceswap", "neuraltextures", atau "face2face" dilabeli sebagai *fake* (label 1).

### 3.2.2 Celeb-DF v2 (CDF)

Dataset kedua yang digunakan adalah Celeb-DF v2 (Celeb-*DeepFake*) yang diperkenalkan oleh Li *et al.* [5]. Celeb-DF berisi video wajah selebriti asli dan versi *deepfake*-nya yang dihasilkan menggunakan teknik *face swapping* tunggal. Dibandingkan FaceForensics++, *deepfake* dalam Celeb-DF memiliki kualitas visual yang lebih tinggi dengan artefak yang lebih halus dan sulit dideteksi secara kasat mata.

Celeb-DF digunakan secara khusus dalam penelitian ini untuk menguji kemampuan generalisasi lintas dataset (*cross-dataset generalization*). Karena Celeb-DF hanya menggunakan satu metode sintesis yang berbeda dari keempat metode dalam FaceForensics++, evaluasi silang antara kedua dataset ini mengukur sejauh mana model mampu mendeteksi *deepfake* dari metode yang belum pernah dilihat selama pelatihan.

### 3.2.3 Pembagian Dataset

Pembagian dataset dilakukan pada level video, bukan pada level *frame*, untuk mencegah kebocoran data (*data leakage*). Apabila pembagian dilakukan pada level *frame*, terdapat risiko *frame-frame* dari video yang sama tersebar ke dalam set pelatihan dan pengujian, sehingga model secara tidak sengaja menghafal karakteristik video tertentu alih-alih mempelajari pola *deepfake* secara umum.

Pembagian dilakukan secara terstratifikasi (*stratified split*) berdasarkan label untuk mempertahankan rasio kelas *real*/*fake* yang seimbang pada setiap subset. Proporsi pembagian yang digunakan adalah sebagai berikut:

Tabel 3.1 Pembagian Dataset

| Subset | Proporsi | Stratifikasi | Level Pembagian |
|---|---|---|---|
| *Training* | 70% | Berdasarkan label | Video |
| *Validation* | 15% | Berdasarkan label | Video |
| *Testing* | 15% | Berdasarkan label | Video |

Pembagian dilakukan menggunakan fungsi `train_test_split` dari pustaka *scikit-learn* dengan parameter `stratify` berdasarkan label dan *seed* = 42 untuk menjamin reproduktibilitas. Validasi tambahan dilakukan untuk memastikan tidak terdapat duplikasi `video_id` dan setiap kelas memiliki minimum 4 sampel yang diperlukan untuk pembagian terstratifikasi tiga arah.

### 3.2.4 Variasi Ukuran Sampel

Untuk menganalisis pengaruh jumlah data pelatihan terhadap performa model, eksperimen dilakukan pada beberapa variasi ukuran sampel. Jumlah sampel yang digunakan berbeda untuk setiap dataset, disesuaikan dengan ketersediaan data:

Tabel 3.2 Variasi Ukuran Sampel per Dataset

| Dataset | Ukuran Sampel (jumlah video) |
|---|---|
| FaceForensics++ (FFPP) | 100, 300, 600, 1000 |
| Celeb-DF v2 (CDF) | 100, 250, 500, 750 |

Pada setiap ukuran sampel, pengambilan video dilakukan secara seimbang antara kelas *real* dan *fake* (rasio 50:50). Dari setiap video yang terpilih, diekstraksi maksimum 50 *frame* pada laju 5 *frame per second* (FPS). Variasi ukuran sampel ini memungkinkan analisis terhadap ketahanan masing-masing arsitektur model pada kondisi data terbatas maupun melimpah.

<!-- Gambar 3.2: Contoh Frame Real vs Fake -->
<!-- Tampilkan 4 gambar: Real FFPP, Fake FFPP, Real CDF, Fake CDF -->

> Gambar 3.2 Contoh *Frame* Real dan *Fake* dari Dataset FaceForensics++ dan Celeb-DF

---

## 3.3 Tahapan *Preprocessing* Data

### 3.3.1 Ekstraksi *Frame* dari Video

Tahap pertama *preprocessing* adalah mengekstraksi *frame* citra dari setiap video dalam dataset. Proses ini dilakukan menggunakan pustaka OpenCV dengan langkah-langkah sebagai berikut:

1. Setiap video dibuka dan dibaca laju *frame* aslinya (*native FPS*).
2. Interval pengambilan *frame* dihitung berdasarkan target FPS: $\text{interval} = \max\left(\left\lfloor \frac{\text{FPS}_{\text{asli}}}{\text{FPS}_{\text{target}}} \right\rfloor, 1\right)$ dengan FPS target = 5.
3. *Frame* diambil pada setiap interval yang telah dihitung, hingga maksimum 50 *frame* per video.
4. Setiap *frame* disimpan sebagai berkas JPEG dengan penamaan berurutan: `frame_000000.jpg`, `frame_000001.jpg`, dan seterusnya.
5. Label setiap video diinferensi secara otomatis dari nama direktori berdasarkan pencocokan kata kunci yang telah dikonfigurasi.

Proses ekstraksi dilakukan secara paralel menggunakan *multiprocessing pool* untuk mempercepat pemrosesan pada dataset berskala besar. Hasil ekstraksi disimpan dalam berkas manifes CSV yang berisi kolom `video_id`, `label`, dan `frames_dir` sebagai referensi untuk tahap selanjutnya.

### 3.3.2 Konversi Domain Frekuensi (FFT)

Konversi domain frekuensi merupakan inti kontribusi penelitian ini. Proses ini mengubah setiap *frame* citra RGB menjadi representasi peta *magnitude* frekuensi menggunakan *Fast Fourier Transform* (FFT) 2 dimensi. Representasi frekuensi ini menangkap artefak spektral yang dihasilkan oleh proses sintesis *deepfake*, seperti *checkerboard artifacts* dari operasi *upsampling* pada GAN [1], distorsi distribusi spektral [2], dan ketidakkontinyuan pada batas *blending* [6].

#### 3.3.2.1 Konversi RGB ke *Grayscale*

Langkah pertama adalah mengonversi citra RGB menjadi *grayscale* (satu kanal). Konversi dilakukan menggunakan standar ITU-R BT.601 dengan formula:

$$Y = 0{,}299R + 0{,}587G + 0{,}114B \tag{3.1}$$

di mana $Y$ adalah nilai luminansi, dan $R$, $G$, $B$ adalah nilai kanal warna merah, hijau, dan biru. Bobot yang berbeda pada setiap kanal mencerminkan sensitivitas mata manusia terhadap masing-masing warna. Konversi ke satu kanal cukup untuk analisis frekuensi karena informasi luminansi merepresentasikan distribusi intensitas spasial yang diperlukan untuk mendeteksi artefak spektral.

#### 3.3.2.2 Transformasi Fourier 2D

Citra *grayscale* kemudian diubah ukurannya menjadi $224 \times 224$ piksel dan ditransformasi ke domain frekuensi menggunakan *Discrete Fourier Transform* (DFT) 2 dimensi. DFT 2D didefinisikan sebagai:

$$F(u, v) = \sum_{x=0}^{M-1} \sum_{y=0}^{N-1} f(x, y) \cdot e^{-j2\pi\left(\frac{ux}{M} + \frac{vy}{N}\right)} \tag{3.2}$$

di mana $f(x, y)$ adalah nilai piksel pada posisi $(x, y)$, $F(u, v)$ adalah koefisien frekuensi pada koordinat frekuensi $(u, v)$, $M$ dan $N$ adalah dimensi citra (keduanya 224), dan $j = \sqrt{-1}$ adalah unit imajiner.

Setelah transformasi, dilakukan operasi *FFT shift* yang memindahkan komponen frekuensi nol (*DC component*) dari sudut matriks ke posisi tengah. Hal ini menyebabkan frekuensi rendah terletak di bagian tengah peta frekuensi dan frekuensi tinggi di bagian tepi, sehingga memudahkan interpretasi visual dan analisis.

#### 3.3.2.3 *Magnitude Spectrum* dan *Log Scaling*

Dari hasil DFT yang berupa bilangan kompleks, dihitung *magnitude spectrum*:

$$|F(u, v)| = \sqrt{\text{Re}(F(u,v))^2 + \text{Im}(F(u,v))^2} \tag{3.3}$$

Karena rentang dinamis *magnitude spectrum* sangat lebar — komponen DC (*direct current*) dapat bernilai ribuan kali lipat lebih besar dari komponen frekuensi tinggi — maka dilakukan transformasi logaritmik:

$$M_{\log}(u, v) = \log(1 + |F(u, v)|) \tag{3.4}$$

Fungsi $\log(1 + x)$ (dikenal sebagai `log1p`) dipilih karena dua alasan: (1) menghindari permasalahan $\log(0)$ karena $\log(1+0) = 0$, dan (2) mengompresi rentang dinamis sehingga detail pada frekuensi tinggi tidak tertutupi oleh dominasi komponen DC. Hasil akhir berupa matriks *float32* berukuran $224 \times 224$ dengan nilai tipikal pada rentang $[0, \sim16]$ yang disimpan sebagai berkas `.npy` (*NumPy array*) dalam *cache* FFT.

#### 3.3.2.4 Contoh Perhitungan FFT 2D

Sebagai ilustrasi, berikut ditunjukkan perhitungan FFT 2D pada matriks *grayscale* berukuran $4 \times 4$. Misalkan matriks piksel $f(x, y)$ adalah:

Tabel 3.3 Contoh Matriks *Grayscale* 4×4

| | $y=0$ | $y=1$ | $y=2$ | $y=3$ |
|---|---|---|---|---|
| $x=0$ | 100 | 120 | 100 | 120 |
| $x=1$ | 80 | 100 | 80 | 100 |
| $x=2$ | 100 | 120 | 100 | 120 |
| $x=3$ | 80 | 100 | 80 | 100 |

**Langkah 1: Hitung $F(0,0)$ — Komponen DC**

$$F(0,0) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi(0)} = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \tag{3.5}$$

$$F(0,0) = (100+120+100+120) + (80+100+80+100) + (100+120+100+120) + (80+100+80+100)$$

$$F(0,0) = 440 + 360 + 440 + 360 = 1600$$

Komponen DC merepresentasikan rata-rata intensitas keseluruhan citra, yaitu $1600 / 16 = 100$.

**Langkah 2: Hitung $F(0,1)$ — Frekuensi horizontal pertama**

$$F(0,1) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi \cdot y/4} \tag{3.6}$$

Karena $e^{-j2\pi y/4}$ menghasilkan faktor $\{1, -j, -1, j\}$ untuk $y = 0, 1, 2, 3$:

- Baris $x=0$: $100(1) + 120(-j) + 100(-1) + 120(j) = 0 + (-120j + 120j) = 0$
- Baris $x=1$: $80(1) + 100(-j) + 80(-1) + 100(j) = 0 + (-100j + 100j) = 0$
- Baris $x=2$: sama dengan $x=0 \Rightarrow 0$
- Baris $x=3$: sama dengan $x=1 \Rightarrow 0$

$$F(0,1) = 0$$

Hal ini menunjukkan bahwa pola frekuensi horizontal pada matriks ini simetris.

**Langkah 3: Hitung $F(1,0)$ — Frekuensi vertikal pertama**

$$F(1,0) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi x/4} \tag{3.7}$$

Faktor $e^{-j2\pi x/4}$ menghasilkan $\{1, -j, -1, j\}$ untuk $x = 0, 1, 2, 3$:

- $x=0$: $(100+120+100+120)(1) = 440$
- $x=1$: $(80+100+80+100)(-j) = -360j$
- $x=2$: $(100+120+100+120)(-1) = -440$
- $x=3$: $(80+100+80+100)(j) = 360j$

$$F(1,0) = 440 - 360j - 440 + 360j = 0$$

**Langkah 4: Hitung $F(1,1)$**

$$F(1,1) = \sum_{x=0}^{3}\sum_{y=0}^{3} f(x,y) \cdot e^{-j2\pi(x+y)/4} \tag{3.8}$$

Faktor gabungan $e^{-j2\pi(x+y)/4}$ untuk setiap $(x, y)$:

| $(x,y)$ | $f(x,y)$ | $e^{-j\pi(x+y)/2}$ | Hasil |
|---|---|---|---|
| (0,0) | 100 | 1 | 100 |
| (0,1) | 120 | $-j$ | $-120j$ |
| (0,2) | 100 | $-1$ | $-100$ |
| (0,3) | 120 | $j$ | $120j$ |
| (1,0) | 80 | $-j$ | $-80j$ |
| (1,1) | 100 | $-1$ | $-100$ |
| (1,2) | 80 | $j$ | $80j$ |
| (1,3) | 100 | $1$ | $100$ |
| (2,0) | 100 | $-1$ | $-100$ |
| (2,1) | 120 | $j$ | $120j$ |
| (2,2) | 100 | $1$ | $100$ |
| (2,3) | 120 | $-j$ | $-120j$ |
| (3,0) | 80 | $j$ | $80j$ |
| (3,1) | 100 | $1$ | $100$ |
| (3,2) | 80 | $-j$ | $-80j$ |
| (3,3) | 100 | $-1$ | $-100$ |

Penjumlahan bagian real: $100 - 100 - 100 + 100 - 100 + 100 - 100 + 100 = 0$

Penjumlahan bagian imajiner: $-120 - 80 + 80 + 120 + 120 - 120 + 80 - 80 = 0$

$$F(1,1) = 0 + 0j = 0$$

Matriks ini memiliki pola repetitif sempurna sehingga energi terkonsentrasi pada komponen DC. Pada citra wajah sesungguhnya, distribusi energi lebih tersebar dan perbedaan antara citra *real* dan *fake* terlihat dari pola distribusi frekuensi tinggi yang anomal.

**Langkah 5: *Magnitude* dan *Log Scaling***

Tabel 3.4 Contoh Perhitungan *Magnitude* dan *Log Scaling*

| Komponen | $F(u,v)$ | $\|F(u,v)\|$ | $\log(1 + \|F(u,v)\|)$ |
|---|---|---|---|
| $F(0,0)$ | $1600$ | $1600$ | $7{,}378$ |
| $F(0,1)$ | $0$ | $0$ | $0$ |
| $F(1,0)$ | $0$ | $0$ | $0$ |
| $F(1,1)$ | $0$ | $0$ | $0$ |

Pada citra *deepfake* sesungguhnya, komponen frekuensi tinggi menunjukkan pola anomali yang khas, seperti *spectral rolloff* yang tidak wajar [2] atau puncak periodik akibat *checkerboard artifacts* dari operasi *transposed convolution* pada GAN [1].

#### 3.3.2.5 Normalisasi FFT

Setelah seluruh *frame* dikonversi ke peta *magnitude* FFT dan disimpan dalam *cache*, dilakukan perhitungan statistik normalisasi per dataset. Normalisasi menggunakan *z-score*:

$$\hat{x} = \frac{x - \mu}{\sigma} \tag{3.9}$$

di mana $\mu$ dan $\sigma$ adalah rata-rata dan simpangan baku global yang dihitung dari seluruh piksel dalam *cache* FFT dataset tersebut. Perhitungan dilakukan pada sampel acak hingga 5.000 berkas *cache* menggunakan akumulasi *online* (metode Welford) untuk efisiensi memori. Hasil disimpan dalam berkas `fft_stats.json` yang dimuat secara otomatis saat pelatihan.

Normalisasi per dataset ini penting karena setiap dataset memiliki karakteristik spektral yang berbeda akibat perbedaan kamera, resolusi, dan metode kompresi. Tanpa normalisasi yang tepat, fitur frekuensi dari dataset yang berbeda akan memiliki skala yang tidak sebanding.

### 3.3.3 Augmentasi Data

#### 3.3.3.1 Augmentasi Domain Spasial

Augmentasi pada domain spasial diterapkan pada citra RGB selama pelatihan untuk meningkatkan keberagaman data dan mencegah *overfitting*. *Pipeline* augmentasi terdiri dari:

1. **Resize** — Citra diubah ukurannya menjadi $256 \times 256$ piksel (lebih besar dari ukuran input final).
2. **RandomResizedCrop** — Pemotongan acak ke ukuran $224 \times 224$ dengan skala antara 80%–100% dari citra asli. Augmentasi ini mensimulasikan variasi *zoom* dan posisi wajah.
3. **RandomHorizontalFlip** — Pembalikan horizontal dengan probabilitas 50%. Augmentasi ini memanfaatkan simetri bilateral wajah manusia.
4. **ToTensor** — Konversi ke tensor PyTorch dengan rentang nilai $[0, 1]$.
5. **Normalize** — Normalisasi menggunakan statistik ImageNet: $\text{mean} = [0{,}485;\ 0{,}456;\ 0{,}406]$, $\text{std} = [0{,}229;\ 0{,}224;\ 0{,}225]$.

Pada tahap validasi dan pengujian, augmentasi acak tidak diterapkan. Citra hanya diubah ukurannya secara langsung ke $224 \times 224$, dikonversi ke tensor, dan dinormalisasi.

#### 3.3.3.2 Augmentasi Domain Frekuensi

Augmentasi pada domain frekuensi memerlukan pendekatan yang berbeda dari domain spasial. Operasi spasial seperti pemotongan acak (*random crop*) atau rotasi tidak sesuai untuk peta *magnitude* FFT karena akan merusak lokalisasi frekuensi — setiap posisi piksel pada peta FFT merepresentasikan komponen frekuensi spesifik yang bergantung pada posisi absolutnya.

Oleh karena itu, augmentasi pada domain frekuensi dilakukan melalui injeksi *noise* Gaussian:

$$\hat{x}_{\text{fft}} = x_{\text{fft}} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2) \tag{3.10}$$

dengan $\sigma = 0{,}05$ (dikonfigurasi melalui parameter `fft_noise_sigma`). *Noise* diterapkan setelah normalisasi *z-score* dan hanya selama pelatihan. Rasional dari pendekatan ini adalah: (1) mensimulasikan variasi *noise* sensor dan artefak kompresi yang memengaruhi spektrum frekuensi, dan (2) mencegah penghafalan (*memorization*) peta FFT yang identik di setiap *epoch* karena data FFT dimuat dari *cache* statis.

#### 3.3.3.3 Konsistensi Augmentasi pada Mode *Hybrid*

Pada mode *hybrid*, di mana model menerima input RGB dan FFT secara bersamaan, konsistensi augmentasi antara kedua cabang sangat penting. Pembalikan horizontal (*horizontal flip*) pada citra RGB tanpa pembalikan yang sama pada peta FFT akan merusak korespondensi spasial-frekuensi, karena $|\text{DFT}(\text{flip}(x))| = \text{flip}(|\text{DFT}(x)|)$.

Untuk mengatasi hal ini, pembalikan horizontal pada mode *hybrid* diterapkan secara manual setelah kedua input dimuat, dengan keputusan acak yang sama (probabilitas 50%) diterapkan secara identik pada tensor RGB dan tensor FFT. Pada *pipeline* augmentasi spasial untuk mode *hybrid*, opsi `RandomHorizontalFlip` dinonaktifkan (`include_hflip=False`) agar pembalikan dapat dikontrol secara terpadu.

<!-- Gambar 3.3: Flowchart Preprocessing Pipeline -->

> Gambar 3.3 Flowchart *Pipeline Preprocessing* Data

<!-- Gambar 3.4: Perbandingan FFT Real vs Fake -->
<!-- Tampilkan: Frame real (RGB) + FFT-nya, Frame fake (RGB) + FFT-nya -->

> Gambar 3.4 Perbandingan Peta *Magnitude* FFT antara *Frame* Real dan *Fake*

---

## 3.4 Arsitektur Model yang Diusulkan

Penelitian ini merancang dan mengevaluasi tiga arsitektur model yang masing-masing merepresentasikan pendekatan berbeda dalam deteksi *deepfake*: model berbasis domain spasial saja, model berbasis domain frekuensi saja, dan model hibrida yang menggabungkan keduanya.

### 3.4.1 Model Spasial — XceptionNet

#### 3.4.1.1 *Depthwise Separable Convolution*

XceptionNet [3] merupakan arsitektur *convolutional neural network* (CNN) yang dibangun sepenuhnya dari *depthwise separable convolution*. Berbeda dengan konvolusi standar yang menerapkan filter secara simultan pada dimensi spasial dan kanal, *depthwise separable convolution* memfaktorisasi operasi menjadi dua tahap terpisah:

1. **Konvolusi *depthwise*** — Menerapkan satu filter konvolusi per kanal input secara independen. Untuk input dengan $C$ kanal dan filter berukuran $K \times K$, jumlah parameter adalah $C \times K \times K$.

2. **Konvolusi *pointwise*** — Menerapkan konvolusi $1 \times 1$ untuk menggabungkan informasi lintas kanal. Untuk menghasilkan $C'$ kanal output, jumlah parameter adalah $C \times C'$.

**Contoh Perhitungan Perbandingan Parameter:**

Untuk input berukuran $H \times W$ dengan $C_{\text{in}} = 64$ kanal, filter $3 \times 3$, dan $C_{\text{out}} = 128$ kanal output:

- **Konvolusi standar:** $C_{\text{in}} \times K^2 \times C_{\text{out}} = 64 \times 9 \times 128 = 73.728$ parameter.
- **Konvolusi *depthwise separable*:**
  - *Depthwise*: $C_{\text{in}} \times K^2 = 64 \times 9 = 576$ parameter.
  - *Pointwise*: $C_{\text{in}} \times C_{\text{out}} = 64 \times 128 = 8.192$ parameter.
  - Total: $576 + 8.192 = 8.768$ parameter.
- **Rasio pengurangan:** $8.768 / 73.728 \approx 11{,}9\%$ — pengurangan parameter sebesar $\sim 88\%$.

Efisiensi parameter ini memungkinkan XceptionNet memiliki kedalaman yang besar (36 *layer* konvolusional) dengan total $\sim 22{,}8$ juta parameter, sambil tetap mempertahankan kapasitas representasi yang tinggi.

**Contoh Perhitungan *Depthwise Separable Convolution*:**

Misalkan input berukuran $3 \times 3$ dengan 2 kanal:

$$\mathbf{X}_1 = \begin{bmatrix} 1 & 2 & 0 \\ 3 & 1 & 2 \\ 0 & 1 & 3 \end{bmatrix}, \quad \mathbf{X}_2 = \begin{bmatrix} 2 & 0 & 1 \\ 1 & 3 & 0 \\ 2 & 1 & 1 \end{bmatrix} \tag{3.11}$$

**Tahap 1 — *Depthwise*:** Filter $2 \times 2$ terpisah per kanal (tanpa *padding*, *stride* = 1):

$$\mathbf{W}_1 = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}, \quad \mathbf{W}_2 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix} \tag{3.12}$$

Konvolusi kanal 1 ($\mathbf{X}_1 * \mathbf{W}_1$), posisi $(0,0)$:

$$1 \times 1 + 2 \times 0 + 3 \times 0 + 1 \times 1 = 2 \tag{3.13}$$

Hasil lengkap kanal 1:
$$\mathbf{Y}_1 = \begin{bmatrix} 2 & 3 \\ 4 & 4 \end{bmatrix}$$

Konvolusi kanal 2 ($\mathbf{X}_2 * \mathbf{W}_2$), posisi $(0,0)$:

$$2 \times 0 + 0 \times 1 + 1 \times 1 + 3 \times 0 = 1 \tag{3.14}$$

Hasil lengkap kanal 2:
$$\mathbf{Y}_2 = \begin{bmatrix} 1 & 4 \\ 2 & 1 \end{bmatrix}$$

**Tahap 2 — *Pointwise*:** Filter $1 \times 1$ berukuran $(2, 1)$ misalnya $[0{,}5;\ 0{,}5]$:

$$\mathbf{Z}(i,j) = 0{,}5 \times \mathbf{Y}_1(i,j) + 0{,}5 \times \mathbf{Y}_2(i,j) \tag{3.15}$$

$$\mathbf{Z} = \begin{bmatrix} 1{,}5 & 3{,}5 \\ 3{,}0 & 2{,}5 \end{bmatrix}$$

Hasil akhir merupakan gabungan informasi lintas kanal yang diperoleh secara efisien melalui dua tahap terpisah.

#### 3.4.1.2 *Transfer Learning* dari ImageNet

XceptionNet yang digunakan dalam penelitian ini diinisialisasi dengan bobot yang telah dilatih pada dataset ImageNet [7], yang terdiri dari 1,4 juta citra dalam 1.000 kelas. *Transfer learning* dari ImageNet memberikan fondasi representasi visual yang kuat — fitur-fitur tingkat rendah (tepi, tekstur) dan tingkat menengah (pola, bentuk) yang telah dipelajari dari ImageNet relevan dan dapat ditransfer ke tugas deteksi *deepfake*.

Model diimplementasikan menggunakan pustaka `timm` (*PyTorch Image Models*) melalui pemanggilan `timm.create_model("xception", pretrained=True)`. Lapisan klasifikasi asli ImageNet (1.000 kelas) diganti dengan lapisan *fully connected* tunggal yang menghasilkan satu nilai *logit* untuk klasifikasi biner (*real* vs *fake*). Dimensi fitur yang dihasilkan oleh *backbone* XceptionNet setelah *global average pooling* adalah 2.048.

### 3.4.2 Model Frekuensi — FreqCNN

#### 3.4.2.1 Arsitektur Konvolusional

FreqCNN adalah jaringan konvolusional ringan yang dirancang khusus untuk memproses peta *magnitude* FFT berdimensi satu kanal. Arsitektur ini terdiri dari blok-blok konvolusional bertingkat yang secara progresif mengekstraksi fitur frekuensi dari resolusi rendah hingga tinggi.

Setiap blok konvolusional terdiri dari empat operasi berurutan:

1. **Conv2d** — Konvolusi 2D dengan *kernel* $3 \times 3$ dan *padding* = 1 (mempertahankan dimensi spasial).
2. **BatchNorm2d** — Normalisasi batch untuk menstabilkan distribusi aktivasi.
3. **ReLU** — Fungsi aktivasi *Rectified Linear Unit*.
4. **MaxPool2d(2)** — *Max pooling* dengan *stride* 2 (mengurangi dimensi spasial menjadi setengah).

Tabel 3.5 Arsitektur *Layer-by-Layer* FreqCNN (*depth* = 3, *base\_channels* = 32)

| *Layer* | Tipe | Dimensi Input | Dimensi Output | Parameter |
|---|---|---|---|---|
| Blok Conv 1 | Conv2d(1→32, 3×3) + BN + ReLU + MaxPool | $(1, 224, 224)$ | $(32, 112, 112)$ | $\sim 320$ |
| Blok Conv 2 | Conv2d(32→64, 3×3) + BN + ReLU + MaxPool | $(32, 112, 112)$ | $(64, 56, 56)$ | $\sim 18.500$ |
| Blok Conv 3 | Conv2d(64→128, 3×3) + BN + ReLU + MaxPool | $(64, 56, 56)$ | $(128, 28, 28)$ | $\sim 73.900$ |
| Dropout2d(0,2) | *Spatial dropout* | $(128, 28, 28)$ | $(128, 28, 28)$ | 0 |
| AdaptiveAvgPool | *Global average pooling* | $(128, 28, 28)$ | $(128, 1, 1)$ | 0 |
| FC 1 | Linear(128→64) + ReLU | $(128)$ | $(64)$ | $\sim 8.300$ |
| Dropout(0,3) | *Dropout* | $(64)$ | $(64)$ | 0 |
| FC 2 | Linear(64→1) | $(64)$ | $(1)$ | $\sim 65$ |
| **Total** | | | | **$\sim$ 130K** |

Jumlah parameter FreqCNN yang relatif kecil ($\sim 130.000$) merupakan pilihan desain yang disengaja. Pada dataset berukuran kecil, model dengan kapasitas terlalu besar cenderung menghafal pola spesifik dataset alih-alih mempelajari artefak frekuensi yang universal. FreqCNN yang ringan mendorong model untuk mempelajari representasi frekuensi yang lebih generalisasi.

Kedalaman FreqCNN dapat dikonfigurasi melalui parameter `freq_depth` (3 atau 5 blok) dan `freq_base_channels` (jumlah kanal awal, *default* 32). Jumlah kanal berlipat dua pada setiap blok hingga batas maksimum 256.

#### 3.4.2.2 Contoh Perhitungan *Forward Pass*

Berikut ditunjukkan contoh perhitungan *forward pass* pada satu blok konvolusional FreqCNN dengan input sederhana berukuran $4 \times 4$, satu kanal.

**Input** (peta *magnitude* FFT tersederhanakan):

$$\mathbf{X} = \begin{bmatrix} 2{,}1 & 3{,}5 & 1{,}2 & 4{,}0 \\ 0{,}8 & 2{,}3 & 3{,}1 & 1{,}5 \\ 4{,}2 & 1{,}0 & 2{,}7 & 3{,}3 \\ 1{,}6 & 3{,}8 & 0{,}5 & 2{,}9 \end{bmatrix} \tag{3.16}$$

**Konvolusi** dengan *kernel* $3 \times 3$ (misalkan bobot $\mathbf{W}$ dan bias $b = 0$), *padding* = 1:

Posisi $(0, 0)$ dengan *zero padding*:

$$z_{0,0} = 0 \cdot w_{00} + 0 \cdot w_{01} + 0 \cdot w_{02} + 0 \cdot w_{10} + 2{,}1 \cdot w_{11} + 3{,}5 \cdot w_{12} + 0 \cdot w_{20} + 0{,}8 \cdot w_{21} + 2{,}3 \cdot w_{22} \tag{3.17}$$

**BatchNorm:** Setelah seluruh posisi dihitung, *batch normalization* menormalisasi output:

$$\hat{z}_i = \frac{z_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} \cdot \gamma + \beta \tag{3.18}$$

di mana $\mu_B$ dan $\sigma_B^2$ adalah rata-rata dan varians *mini-batch*, $\gamma$ dan $\beta$ adalah parameter *learnable*, dan $\epsilon = 10^{-5}$ mencegah pembagian dengan nol.

**ReLU:** $\text{ReLU}(\hat{z}) = \max(0, \hat{z})$. Nilai negatif diubah menjadi nol.

**MaxPool2d(2):** Pada grid $2 \times 2$, diambil nilai maksimum. Dari output $4 \times 4$, dihasilkan peta fitur berukuran $2 \times 2$.

### 3.4.3 Model *Hybrid* — HybridTwoBranch (*Late Fusion*)

Model *hybrid* merupakan kontribusi utama penelitian ini. Arsitektur HybridTwoBranch menggabungkan fitur dari domain spasial dan domain frekuensi melalui mekanisme *late fusion* — kedua cabang mengekstraksi fitur secara independen, kemudian fitur digabungkan dan diproses bersama untuk klasifikasi akhir.

#### 3.4.3.1 Cabang Spasial (XceptionNet *Backbone*)

Cabang spasial menggunakan XceptionNet sebagai *feature extractor* dengan konfigurasi `num_classes=0`, yang berarti lapisan klasifikasi dihilangkan dan model hanya menghasilkan vektor fitur. Input berupa citra RGB berukuran $(3, 224, 224)$ yang telah dinormalisasi menggunakan statistik ImageNet. Output berupa vektor fitur berdimensi 2.048 yang merepresentasikan fitur spasial tingkat tinggi dari citra wajah.

#### 3.4.3.2 Cabang Frekuensi (FreqCNN *Backbone*)

Cabang frekuensi menggunakan bagian *backbone* dari FreqCNN (blok konvolusional + *global average pooling*) tanpa lapisan klasifikasi. Input berupa peta *magnitude* FFT berukuran $(1, 224, 224)$ yang telah dinormalisasi menggunakan *z-score* per dataset. Output berupa vektor fitur berdimensi 128 (pada konfigurasi *depth* = 3) yang merepresentasikan pola frekuensi dalam citra.

#### 3.4.3.3 *Projection Layers* dan Penyeimbangan Dimensi

Tantangan utama dalam *late fusion* adalah ketidakseimbangan dimensi antara kedua cabang. Cabang spasial menghasilkan vektor berdimensi 2.048, sedangkan cabang frekuensi hanya 128 — rasio 16:1. Apabila kedua vektor langsung digabungkan (*concatenation*), fitur spasial akan mendominasi proses klasifikasi karena magnitudonya yang jauh lebih besar.

Untuk mengatasi hal ini, kedua cabang diproyeksikan ke dimensi yang sama ($\text{PROJ\_DIM} = 256$) melalui lapisan proyeksi:

$$\mathbf{h}_{\text{spatial}} = \text{ReLU}(\text{BN}(\mathbf{W}_s \cdot \mathbf{f}_{\text{spatial}} + \mathbf{b}_s)) \tag{3.19}$$

$$\mathbf{h}_{\text{freq}} = \text{ReLU}(\text{BN}(\mathbf{W}_f \cdot \mathbf{f}_{\text{freq}} + \mathbf{b}_f)) \tag{3.20}$$

di mana $\mathbf{W}_s \in \mathbb{R}^{256 \times 2048}$ dan $\mathbf{W}_f \in \mathbb{R}^{256 \times 128}$ adalah matriks bobot proyeksi, BN adalah *batch normalization* 1D, dan ReLU adalah fungsi aktivasi. Setelah proyeksi, kedua cabang memiliki representasi berdimensi sama (256) yang dapat digabungkan secara seimbang.

#### 3.4.3.4 *Squeeze-and-Excitation* (SE) *Gating*

Setelah kedua vektor fitur terproyeksi digabungkan melalui konkatenasi ($\mathbf{h}_{\text{fused}} = [\mathbf{h}_{\text{spatial}}; \mathbf{h}_{\text{freq}}] \in \mathbb{R}^{512}$), diterapkan mekanisme *Squeeze-and-Excitation* (SE) *gating* [8] yang memungkinkan model mempelajari bobot kepentingan per dimensi fitur secara adaptif.

Arsitektur SE *gate* terdiri dari:

1. ***Squeeze*** — Kompresi vektor fusi dari 512 dimensi ke 128 dimensi melalui transformasi linier, diikuti aktivasi ReLU.
2. ***Excitation*** — Ekspansi kembali ke 512 dimensi melalui transformasi linier, diikuti fungsi *sigmoid* yang menghasilkan bobot gerbang (*gate weights*) pada rentang $[0, 1]$.
3. **Pengalian elemen** — Vektor fusi asli dikalikan secara elemen-per-elemen (*element-wise*) dengan bobot gerbang.

Secara matematis:

$$\mathbf{g} = \sigma(\mathbf{W}_2 \cdot \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_{\text{fused}} + \mathbf{b}_1) + \mathbf{b}_2) \tag{3.21}$$

$$\hat{\mathbf{h}}_{\text{fused}} = \mathbf{h}_{\text{fused}} \odot \mathbf{g} \tag{3.22}$$

di mana $\mathbf{W}_1 \in \mathbb{R}^{128 \times 512}$, $\mathbf{W}_2 \in \mathbb{R}^{512 \times 128}$, $\sigma$ adalah fungsi *sigmoid*, dan $\odot$ adalah perkalian elemen. Mekanisme ini memungkinkan model untuk menekan (*suppress*) fitur yang tidak informatif dan memperkuat (*enhance*) fitur yang diskriminatif, baik dari cabang spasial maupun frekuensi, secara adaptif berdasarkan input.

#### 3.4.3.5 *Classifier Head*

Vektor fitur yang telah melalui SE *gating* ($\hat{\mathbf{h}}_{\text{fused}} \in \mathbb{R}^{512}$) diteruskan ke kepala klasifikasi (*classifier head*) yang terdiri dari:

1. **Dropout(0,5)** — Regularisasi berat pada representasi fusi untuk mencegah *overfitting*.
2. **Linear(512 → 128)** — Reduksi dimensi.
3. **ReLU** — Fungsi aktivasi.
4. **Dropout(0,3)** — Regularisasi tambahan.
5. **Linear(128 → 1)** — Menghasilkan satu nilai *logit* untuk klasifikasi biner.

Output *logit* diproses oleh fungsi *loss* BCEWithLogitsLoss yang secara internal menerapkan fungsi *sigmoid* sebelum menghitung *binary cross-entropy*.

#### 3.4.3.6 Contoh Perhitungan *Late Fusion*

Berikut ditunjukkan contoh perhitungan *late fusion* yang disederhanakan dengan dimensi kecil untuk ilustrasi.

**Langkah 1: Fitur input** (disederhanakan ke 4 dimensi per cabang):

$$\mathbf{f}_{\text{spatial}} = [0{,}8;\ 1{,}2;\ -0{,}3;\ 0{,}5], \quad \mathbf{f}_{\text{freq}} = [0{,}4;\ -0{,}1;\ 0{,}7;\ 0{,}2] \tag{3.23}$$

**Langkah 2: Proyeksi** ($4 \rightarrow 4$, disederhanakan tanpa BN):

Misalkan $\mathbf{W}_s$ dan $\mathbf{W}_f$ adalah matriks identitas, maka $\mathbf{h}_{\text{spatial}} = \text{ReLU}(\mathbf{f}_{\text{spatial}}) = [0{,}8;\ 1{,}2;\ 0;\ 0{,}5]$ dan $\mathbf{h}_{\text{freq}} = \text{ReLU}(\mathbf{f}_{\text{freq}}) = [0{,}4;\ 0;\ 0{,}7;\ 0{,}2]$.

**Langkah 3: Konkatenasi:**

$$\mathbf{h}_{\text{fused}} = [0{,}8;\ 1{,}2;\ 0;\ 0{,}5;\ 0{,}4;\ 0;\ 0{,}7;\ 0{,}2] \in \mathbb{R}^8 \tag{3.24}$$

**Langkah 4: SE *Gating*** ($8 \rightarrow 2 \rightarrow 8$, *reduction* = 4):

*Squeeze*: $\mathbf{s} = \text{ReLU}(\mathbf{W}_1 \cdot \mathbf{h}_{\text{fused}})$. Misalkan hasilnya $\mathbf{s} = [1{,}5;\ 0{,}8]$.

*Excitation*: $\mathbf{g} = \sigma(\mathbf{W}_2 \cdot \mathbf{s})$. Misalkan hasilnya $\mathbf{g} = [0{,}9;\ 0{,}7;\ 0{,}3;\ 0{,}8;\ 0{,}6;\ 0{,}2;\ 0{,}9;\ 0{,}5]$.

*Gating*:
$$\hat{\mathbf{h}}_{\text{fused}} = \mathbf{h}_{\text{fused}} \odot \mathbf{g} = [0{,}72;\ 0{,}84;\ 0;\ 0{,}40;\ 0{,}24;\ 0;\ 0{,}63;\ 0{,}10] \tag{3.25}$$

Terlihat bahwa SE *gate* menekan dimensi ke-3 dan ke-6 (nilai *gate* rendah: 0,3 dan 0,2) sambil mempertahankan dimensi ke-1 dan ke-7 (nilai *gate* tinggi: 0,9 dan 0,9). Mekanisme ini memungkinkan model untuk secara adaptif memilih fitur yang paling diskriminatif dari kedua cabang.

**Langkah 5: Klasifikasi:**

*Logit*: $z = \mathbf{w}^T \hat{\mathbf{h}}_{\text{fused}} + b$. Misalkan $z = 2{,}1$.

Probabilitas: $p = \sigma(2{,}1) = \frac{1}{1 + e^{-2{,}1}} = 0{,}891$.

Prediksi: $p > 0{,}5 \Rightarrow$ *fake* (label 1).

### 3.4.4 Perbandingan Arsitektur Model

Tabel 3.6 Perbandingan Tiga Arsitektur Model

| Aspek | *Spatial* (XceptionNet) | *Frequency* (FreqCNN) | *Hybrid* (HybridTwoBranch) |
|---|---|---|---|
| Input | RGB $(3, 224, 224)$ | FFT $(1, 224, 224)$ | RGB + FFT (terpisah) |
| *Backbone* | XceptionNet (*pretrained*) | FreqCNN (*from scratch*) | XceptionNet + FreqCNN |
| Dimensi fitur | 2.048 | 128 | $256 + 256 = 512$ (terproyeksi) |
| Mekanisme fusi | — | — | Konkatenasi + SE *Gating* |
| Total parameter | $\sim 22{,}8$ juta | $\sim 130$ ribu | $\sim 23{,}2$ juta |
| *Pretrained* | Ya (ImageNet) | Tidak | Parsial (cabang spasial) |
| Domain | Spasial | Frekuensi | Keduanya |

Tabel 3.7 Dimensi Fitur per Komponen Model *Hybrid*

| Komponen | Dimensi Input | Dimensi Output | Operasi |
|---|---|---|---|
| XceptionNet *backbone* | $(3, 224, 224)$ | 2.048 | Ekstraksi fitur + GAP |
| FreqCNN *backbone* | $(1, 224, 224)$ | 128 | Blok konvolusi + GAP |
| Proyeksi spasial | 2.048 | 256 | Linear + BN + ReLU |
| Proyeksi frekuensi | 128 | 256 | Linear + BN + ReLU |
| Konkatenasi | $256 + 256$ | 512 | `torch.cat` |
| SE *Gate* | 512 | 512 | *Squeeze-Excitation* |
| *Classifier* | 512 | 1 | FC + Dropout |

<!-- Gambar 3.5: Diagram Arsitektur XceptionNet (simplified) -->

> Gambar 3.5 Diagram Arsitektur XceptionNet

<!-- Gambar 3.6: Diagram Arsitektur FreqCNN -->

> Gambar 3.6 Diagram Arsitektur FreqCNN

<!-- Gambar 3.7: Diagram Arsitektur HybridTwoBranch -->
<!--
RGB (3,224,224) → [XceptionNet Backbone] → (2048) → [Proj: Linear→BN→ReLU] → (256) ─┐
                   (frozen 3 epochs)                  (2048→256)                        │
                                                                                        ├→ [Concat] → (512) → [SE Gate] → (512) → [Classifier] → logit
FFT (1,224,224) → [FreqCNN Backbone] → (128) → [Proj: Linear→BN→ReLU] → (256) ────────┘
                   (3 conv blocks)               (128→256)
-->

> Gambar 3.7 Diagram Arsitektur HybridTwoBranch (*Late Fusion*)

---

## 3.5 Strategi Pelatihan Model

### 3.5.1 *Transfer Learning* dan *Backbone Freezing*

Strategi *transfer learning* diterapkan pada model *spatial* dan *hybrid* yang menggunakan *backbone* XceptionNet. Bobot yang telah dilatih pada ImageNet memberikan inisialisasi yang kuat, sehingga model tidak perlu mempelajari fitur visual dasar dari awal.

Pada model *hybrid* dan *early fusion*, *backbone* XceptionNet dibekukan (*frozen*) selama 3 *epoch* pertama pelatihan. Selama periode ini, hanya parameter lapisan baru (proyeksi, SE *gate*, *classifier*, dan FreqCNN) yang diperbarui. Pembekuan ini bertujuan agar lapisan-lapisan baru yang diinisialisasi secara acak dapat mempelajari representasi yang bermakna terlebih dahulu sebelum gradien mengalir ke *backbone* yang telah *pretrained*. Tanpa pembekuan, gradien acak dari lapisan baru yang belum terlatih dapat merusak bobot *pretrained* yang sudah optimal (*catastrophic forgetting*).

Pada *epoch* ke-4, seluruh parameter *backbone* dilepaskan (*unfreezing*) dengan pemanggilan `requires_grad_(True)`, memungkinkan *fine-tuning* menyeluruh untuk mengadaptasi fitur ImageNet ke domain deteksi *deepfake*.

### 3.5.2 *Differential Learning Rate*

Untuk melindungi bobot *pretrained* yang sudah berkualitas sambil memungkinkan lapisan baru belajar dengan cepat, digunakan *differential learning rate* — laju pembelajaran yang berbeda untuk kelompok parameter yang berbeda:

Tabel 3.8 *Learning Rate* per Kelompok Parameter

| Kelompok Parameter | *Learning Rate* | Diterapkan Pada |
|---|---|---|
| *Backbone* (*pretrained*) | $1 \times 10^{-5}$ (base / 10) | Parameter XceptionNet |
| *Head* (lapisan baru) | $1 \times 10^{-4}$ (base) | FreqCNN, proyeksi, SE *gate*, *classifier* |

*Learning rate* *backbone* yang 10 kali lebih rendah memastikan bahwa *fine-tuning* dilakukan secara halus tanpa menghancurkan representasi visual yang telah dipelajari dari ImageNet, sementara lapisan baru mendapat *learning rate* yang lebih tinggi untuk konvergensi yang lebih cepat.

### 3.5.3 Penjadwalan *Learning Rate*

Penjadwalan *learning rate* menggabungkan dua fase menggunakan `SequentialLR`:

1. ***Linear warmup*** (2 *epoch*) — *Learning rate* dinaikkan secara linier dari 10% ke 100% dari nilai *base*. `LinearLR(start_factor=0.1, end_factor=1.0, total_iters=2)`. Fase ini mencegah pembaruan bobot yang terlalu besar pada iterasi awal, terutama penting pada *backbone pretrained*.

2. ***Cosine annealing*** (*epoch* ke-3 hingga selesai) — *Learning rate* diturunkan secara halus mengikuti kurva kosinus dari nilai *base* menuju $1 \times 10^{-6}$. `CosineAnnealingLR(T_max=max(epochs-2, 1), eta_min=1e-6)`. Penurunan yang mulus ini menghindari *shock* akibat penurunan LR yang tiba-tiba.

Kurva *learning rate* untuk pelatihan 30 *epoch*:

- *Epoch* 1: $\text{LR} = 0{,}1 \times \text{base} = 1 \times 10^{-5}$
- *Epoch* 2: $\text{LR} = 1{,}0 \times \text{base} = 1 \times 10^{-4}$
- *Epoch* 3–30: *Cosine decay* dari $1 \times 10^{-4}$ menuju $1 \times 10^{-6}$

<!-- Gambar 3.8: Kurva Learning Rate Schedule -->

> Gambar 3.8 Kurva Penjadwalan *Learning Rate* (*Warmup* + *Cosine Decay*)

### 3.5.4 Fungsi *Loss* — BCEWithLogitsLoss dengan *Label Smoothing*

Fungsi *loss* yang digunakan adalah *Binary Cross-Entropy with Logits* (BCEWithLogitsLoss), yang menggabungkan fungsi *sigmoid* dan *binary cross-entropy* dalam satu operasi yang stabil secara numerik:

$$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\left[y_i \cdot \log(\sigma(z_i)) + (1 - y_i) \cdot \log(1 - \sigma(z_i))\right] \tag{3.26}$$

di mana $z_i$ adalah *logit* (output model sebelum *sigmoid*), $\sigma(z) = \frac{1}{1 + e^{-z}}$ adalah fungsi *sigmoid*, dan $y_i$ adalah label target.

**Label smoothing** diterapkan dengan faktor $\alpha = 0{,}02$ untuk mencegah model menjadi terlalu percaya diri (*overconfident*) pada prediksinya:

$$y'_i = y_i \times (1 - \alpha) + \alpha \times 0{,}5 \tag{3.27}$$

Transformasi ini mengubah label biner menjadi: $0 \rightarrow 0{,}01$ dan $1 \rightarrow 0{,}99$. Model tidak perlu mendorong *logit* ke nilai ekstrem ($\pm \infty$), sehingga menghasilkan probabilitas yang lebih terkalibrasi.

#### 3.5.4.1 Contoh Perhitungan BCEWithLogitsLoss

Misalkan *logit* output model $z = 2{,}5$ dan label asli $y = 1$ (*fake*).

**Langkah 1: *Label smoothing*:**

$$y' = 1 \times (1 - 0{,}02) + 0{,}02 \times 0{,}5 = 0{,}98 + 0{,}01 = 0{,}99 \tag{3.28}$$

**Langkah 2: *Sigmoid*:**

$$\sigma(2{,}5) = \frac{1}{1 + e^{-2{,}5}} = \frac{1}{1 + 0{,}0821} = \frac{1}{1{,}0821} = 0{,}924 \tag{3.29}$$

**Langkah 3: *Loss*:**

$$\mathcal{L} = -\left[0{,}99 \cdot \log(0{,}924) + 0{,}01 \cdot \log(1 - 0{,}924)\right] \tag{3.30}$$

$$= -\left[0{,}99 \times (-0{,}0791) + 0{,}01 \times (-2{,}577)\right]$$

$$= -\left[-0{,}0783 + (-0{,}0258)\right] = -(-0{,}1041) = 0{,}1041$$

Nilai *loss* yang rendah (0,1041) menunjukkan bahwa prediksi model (probabilitas 0,924 untuk *fake*) sudah mendekati label target. Pada awal pelatihan, nilai *loss* umumnya jauh lebih tinggi dan menurun seiring konvergensi model.

### 3.5.5 Optimisasi — Adam dengan *Gradient Accumulation*

Optimizer yang digunakan adalah Adam [9] dengan konfigurasi $\text{lr} = 1 \times 10^{-4}$ dan $\text{weight\_decay} = 1 \times 10^{-4}$ (regularisasi L2). Adam menggabungkan keunggulan *momentum* (merata-ratakan gradien untuk stabilitas) dan *adaptive learning rate* (menyesuaikan laju pembelajaran per parameter berdasarkan estimasi momen pertama dan kedua gradien).

*Gradient accumulation* diterapkan dengan `accum_steps = 2`, yang berarti gradien diakumulasikan selama 2 *batch* sebelum pembaruan bobot dilakukan. Dengan ukuran *batch* per langkah sebesar 16, ukuran *batch* efektif menjadi $16 \times 2 = 32$. Teknik ini memungkinkan penggunaan *batch* efektif yang lebih besar tanpa meningkatkan kebutuhan memori GPU. *Loss* dibagi dengan `accum_steps` sebelum *backpropagation* untuk menjaga skala gradien yang konsisten.

### 3.5.6 *Gradient Clipping*

*Gradient clipping* berdasarkan norma L2 diterapkan dengan batas $\text{max\_norm} = 1{,}0$:

$$\mathbf{g} \leftarrow \begin{cases} \mathbf{g} & \text{jika } \|\mathbf{g}\|_2 \leq 1{,}0 \\ \frac{\mathbf{g}}{\|\mathbf{g}\|_2} & \text{jika } \|\mathbf{g}\|_2 > 1{,}0 \end{cases} \tag{3.31}$$

Teknik ini mencegah ledakan gradien (*gradient explosion*), terutama pada *epoch* ke-4 ketika *backbone* XceptionNet dilepaskan (*unfreezing*) dan aliran gradien dari seluruh jaringan secara tiba-tiba meningkatkan norma gradien. Pada implementasi dengan *mixed precision* (AMP), `scaler.unscale_()` dipanggil sebelum *clipping* untuk memastikan gradien berada pada skala aslinya.

### 3.5.7 *Mixed Precision Training* (AMP)

Pelatihan dengan presisi campuran (*Automatic Mixed Precision* / AMP) diterapkan pada GPU CUDA menggunakan `torch.cuda.amp.autocast()` dan `GradScaler`. Dalam mode ini, operasi *forward pass* dan *backward pass* dilakukan dalam format *float16* (setengah presisi), sedangkan pembaruan bobot oleh *optimizer* dilakukan dalam format *float32* (presisi penuh). AMP memberikan percepatan pelatihan hingga $\sim 2\times$ dengan penurunan akurasi yang minimal. Optimisasi TF32 juga diaktifkan untuk GPU arsitektur Ampere ke atas.

### 3.5.8 *Early Stopping*

Mekanisme *early stopping* digunakan untuk menghentikan pelatihan secara otomatis ketika model tidak lagi menunjukkan peningkatan performa pada set validasi. Konfigurasi yang digunakan:

- **Metrik pemantauan:** AUC validasi (metrik utama).
- **Kesabaran (*patience*):** 5 *epoch* berturut-turut tanpa peningkatan AUC.
- **Jumlah *epoch* maksimum:** 30.
- **Tindakan:** Pelatihan dihentikan dan *checkpoint* terbaik digunakan untuk evaluasi.

AUC dipilih sebagai metrik pemantauan karena bersifat independen terhadap *threshold* — mengevaluasi kemampuan model membedakan kelas positif dan negatif pada seluruh kemungkinan *threshold*, berbeda dengan akurasi yang bergantung pada satu nilai *threshold* tertentu.

### 3.5.9 Seleksi Model Terbaik

Pada setiap *epoch*, apabila AUC validasi meningkat dibandingkan nilai terbaik sebelumnya, *checkpoint* model disimpan dalam format `{"state_dict": ..., "epoch": ..., "config": ...}`. *Checkpoint* terbaik berdasarkan AUC validasi tertinggi digunakan untuk evaluasi akhir pada set pengujian.

Tabel 3.9 Ringkasan *Hyperparameter* Pelatihan

| Parameter | Nilai | Keterangan |
|---|---|---|
| *Optimizer* | Adam | *Adaptive learning rate* |
| *Learning rate* (*base*) | $1 \times 10^{-4}$ | Lapisan baru |
| *Learning rate* (*backbone*) | $1 \times 10^{-5}$ | XceptionNet *pretrained* |
| *Weight decay* | $1 \times 10^{-4}$ | Regularisasi L2 |
| *Batch size* | 16 | Per langkah; efektif 32 |
| *Gradient accumulation* | 2 langkah | *Batch* efektif = 32 |
| *Epoch* maksimum | 30 | Dibatasi *early stopping* |
| *Early stopping patience* | 5 | Tanpa peningkatan AUC |
| *Label smoothing* | 0,02 | Target: $0 \rightarrow 0{,}01$; $1 \rightarrow 0{,}99$ |
| *Gradient clipping* | max_norm = 1,0 | Norma L2 |
| *LR warmup* | 2 *epoch* | 10% → 100% linear |
| *LR schedule* | *Cosine annealing* | Decay ke $1 \times 10^{-6}$ |
| *Backbone freeze* | 3 *epoch* | *Hybrid* saja |
| *Mixed precision* | AMP (*float16*) | CUDA saja |
| *Seed* | 42 | Reproduktibilitas |
| *Framework* | PyTorch + timm | XceptionNet via timm |

---

## 3.6 Desain Eksperimen

### 3.6.1 Matriks Eksperimen

Penelitian ini dirancang sebagai eksperimen faktorial yang menguji kombinasi dari tiga faktor utama: arsitektur model, dataset pelatihan, dan ukuran sampel. Setiap kombinasi dijalankan dengan tiga *seed* berbeda untuk memperoleh estimasi rata-rata dan simpangan baku yang reliabel.

Tabel 3.10 Matriks Eksperimen

| Dimensi | Nilai | Jumlah |
|---|---|---|
| Model | *spatial*, *freq*, *hybrid* | 3 |
| Dataset pelatihan | FFPP, CDF | 2 |
| Ukuran sampel FFPP | 100, 300, 600, 1000 | 4 |
| Ukuran sampel CDF | 100, 250, 500, 750 | 4 |
| *Seed* | 0, 1, 2 | 3 |
| Evaluasi | *In-dataset*, *cross-dataset* | 2 |

Total pelatihan: $3 \times 2 \times 4 \times 3 = 72$ *run*.
Total evaluasi: $72 \times 2 = 144$ evaluasi (setiap model dievaluasi secara *in-dataset* dan *cross-dataset*).

### 3.6.2 Evaluasi *In-Dataset*

Evaluasi *in-dataset* mengukur performa model pada set pengujian dari dataset yang sama dengan dataset pelatihan:
- Model dilatih pada FFPP → dievaluasi pada set pengujian FFPP.
- Model dilatih pada CDF → dievaluasi pada set pengujian CDF.

Evaluasi ini mengukur seberapa baik model mempelajari pola *deepfake* dari distribusi data pelatihannya.

### 3.6.3 Evaluasi *Cross-Dataset*

Evaluasi *cross-dataset* mengukur kemampuan generalisasi model pada dataset yang berbeda dari dataset pelatihan:
- Model dilatih pada FFPP → dievaluasi pada set pengujian CDF.
- Model dilatih pada CDF → dievaluasi pada set pengujian FFPP.

Evaluasi silang ini sangat penting karena dalam skenario nyata, detektor *deepfake* harus mampu mengenali manipulasi dari metode yang belum pernah dilihat selama pelatihan. Perbedaan performa antara evaluasi *in-dataset* dan *cross-dataset* diukur melalui metrik **generalisasi *drop***:

$$\Delta = \text{F1}_{\text{in-dataset}} - \text{F1}_{\text{cross-dataset}} \tag{3.32}$$

Nilai $\Delta$ yang besar menunjukkan bahwa model terlalu bergantung pada pola spesifik dataset pelatihan dan tidak memiliki kemampuan generalisasi yang baik.

### 3.6.4 Variabel Penelitian

Tabel 3.11 Variabel Penelitian

| Jenis | Variabel | Nilai |
|---|---|---|
| **Independen** | Arsitektur model | *spatial*, *freq*, *hybrid* |
| | Dataset pelatihan | FFPP, CDF |
| | Ukuran sampel | 100–1000 (bervariasi per dataset) |
| **Dependen** | *Accuracy*, *Precision*, *Recall*, F1-*Score*, AUC | Kontinu $[0, 1]$ |
| | *Generalization drop* ($\Delta$) | $\text{F1}_{\text{in}} - \text{F1}_{\text{cross}}$ |
| **Kontrol** | *Hyperparameter* pelatihan | Tetap (Tabel 3.9) |
| | *Seed* | 42, 43, 44 |
| | Pembagian data | 70/15/15 terstratifikasi |
| | Ukuran citra | $224 \times 224$ |

---

## 3.7 Metode Evaluasi Model

Evaluasi model dilakukan pada *frame-frame* dari set pengujian (*test set*) yang telah dipisahkan pada level video untuk mencegah kebocoran data. Lima metrik evaluasi digunakan untuk mengukur performa model secara komprehensif.

### 3.7.1 *Confusion Matrix*

*Confusion matrix* merupakan fondasi dari seluruh metrik evaluasi klasifikasi biner. Matriks ini membandingkan prediksi model dengan label aktual:

Tabel 3.12 Struktur *Confusion Matrix*

| | **Prediksi *Fake*** | **Prediksi *Real*** |
|---|---|---|
| **Aktual *Fake*** | *True Positive* (TP) | *False Negative* (FN) |
| **Aktual *Real*** | *False Positive* (FP) | *True Negative* (TN) |

Dalam konteks deteksi *deepfake*:
- **TP**: *Frame fake* yang terdeteksi dengan benar sebagai *fake*.
- **TN**: *Frame real* yang terdeteksi dengan benar sebagai *real*.
- **FP**: *Frame real* yang salah terdeteksi sebagai *fake* (*false alarm*).
- **FN**: *Frame fake* yang lolos deteksi (*missed detection*).

### 3.7.2 *Accuracy*

*Accuracy* mengukur proporsi prediksi yang benar dari seluruh prediksi:

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} \tag{3.33}$$

### 3.7.3 *Precision*

*Precision* mengukur ketepatan prediksi positif — dari seluruh prediksi *fake*, berapa banyak yang benar-benar *fake*:

$$\text{Precision} = \frac{TP}{TP + FP} \tag{3.34}$$

### 3.7.4 *Recall*

*Recall* mengukur kelengkapan deteksi — dari seluruh *frame fake* yang sebenarnya, berapa banyak yang berhasil terdeteksi:

$$\text{Recall} = \frac{TP}{TP + FN} \tag{3.35}$$

### 3.7.5 F1-*Score*

F1-*Score* adalah rata-rata harmonik dari *precision* dan *recall*, memberikan keseimbangan antara kedua metrik:

$$\text{F1} = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \tag{3.36}$$

### 3.7.6 AUC-ROC

AUC (*Area Under the Receiver Operating Characteristic Curve*) mengukur kemampuan model membedakan kelas positif dan negatif secara independen dari *threshold*. Kurva ROC memplotkan *True Positive Rate* (TPR = *Recall*) terhadap *False Positive Rate* (FPR) pada berbagai nilai *threshold*:

$$\text{FPR} = \frac{FP}{FP + TN} \tag{3.37}$$

Nilai AUC berkisar antara 0 dan 1, di mana 0,5 menunjukkan prediksi acak dan 1,0 menunjukkan pemisahan sempurna. AUC digunakan sebagai metrik utama untuk seleksi model dan *early stopping* karena sifatnya yang independen terhadap *threshold*.

Selain evaluasi pada *threshold* tetap ($\theta = 0{,}5$), penelitian ini juga menghitung *threshold* optimal menggunakan statistik J Youden:

$$J = \text{TPR} - \text{FPR} \tag{3.38}$$

*Threshold* yang memaksimalkan $J$ memberikan keseimbangan optimal antara sensitivitas dan spesifisitas.

### 3.7.7 *Generalization Drop*

Metrik *generalization drop* mengukur degradasi performa model ketika dievaluasi pada dataset yang berbeda dari dataset pelatihan:

$$\Delta = \text{F1}_{\text{in-dataset}} - \text{F1}_{\text{cross-dataset}} \tag{3.39}$$

Nilai $\Delta$ yang mendekati nol menunjukkan generalisasi yang baik — model mampu mendeteksi *deepfake* dari metode yang belum pernah dilihat. Nilai $\Delta$ yang besar menunjukkan bahwa model menghafal pola spesifik dataset pelatihan.

### 3.7.8 Contoh Perhitungan Metrik

Sebagai ilustrasi, berikut ditunjukkan contoh perhitungan seluruh metrik dari suatu *confusion matrix*:

Tabel 3.13 Contoh *Confusion Matrix*

| | **Prediksi *Fake*** | **Prediksi *Real*** | **Total** |
|---|---|---|---|
| **Aktual *Fake*** | TP = 42 | FN = 8 | 50 |
| **Aktual *Real*** | FP = 5 | TN = 45 | 50 |
| **Total** | 47 | 53 | 100 |

Tabel 3.14 Perhitungan Metrik Evaluasi

| Metrik | Perhitungan | Hasil |
|---|---|---|
| *Accuracy* | $(42 + 45) / (42 + 45 + 5 + 8) = 87/100$ | $0{,}870$ |
| *Precision* | $42 / (42 + 5) = 42/47$ | $0{,}894$ |
| *Recall* | $42 / (42 + 8) = 42/50$ | $0{,}840$ |
| F1-*Score* | $2 \times 0{,}894 \times 0{,}840 / (0{,}894 + 0{,}840)$ | $0{,}866$ |
| AUC | (dihitung dari kurva ROC) | — |

Dari contoh di atas, model berhasil mendeteksi 42 dari 50 *frame fake* (*recall* = 84%) dengan tingkat *false alarm* yang rendah (5 dari 50 *frame real* salah diklasifikasi, FPR = 10%). F1-*Score* sebesar 0,866 menunjukkan keseimbangan yang baik antara *precision* dan *recall*.
