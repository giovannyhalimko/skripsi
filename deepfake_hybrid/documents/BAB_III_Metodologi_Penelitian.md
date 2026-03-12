# BAB III METODOLOGI PENELITIAN

## 3.1 Desain Penelitian

Penelitian ini menggunakan metode penelitian eksperimental dengan pendekatan kuantitatif. Pendekatan tersebut dipilih karena penelitian berfokus pada perancangan, implementasi, dan pengujian model deteksi deepfake berbasis pembelajaran mendalam dalam kondisi yang terkontrol. Melalui desain ini, setiap model dapat dibandingkan secara objektif karena menggunakan sumber data, tahapan prapemrosesan, konfigurasi pelatihan, dan metrik evaluasi yang seragam.

Secara konseptual, penelitian ini tidak hanya menilai kinerja model pada data yang berasal dari distribusi yang sama dengan data pelatihan, tetapi juga menilai kemampuan generalisasi model ketika diterapkan pada dataset yang berbeda. Dengan demikian, dua aspek utama yang dievaluasi adalah performa in-dataset dan performa cross-dataset.

Pemilihan desain tersebut didasarkan pada kenyataan bahwa permasalahan utama dalam deteksi deepfake bukan sekadar memperoleh akurasi tinggi pada satu dataset tertentu, melainkan mempertahankan kinerja ketika pola manipulasi, distribusi visual, dan artefak digital berubah pada dataset lain. Oleh karena itu, desain penelitian diarahkan pada pembandingan sistematis terhadap tiga model utama, dua sumber dataset, dan beberapa ukuran sampel pelatihan.

## 3.2 Tujuan Metodologis Penelitian

Secara metodologis, penelitian ini dirancang untuk mencapai tujuan-tujuan berikut.

1. Menyusun pipeline deteksi deepfake yang terstruktur mulai dari ekstraksi frame, pembentukan split data, pembangkitan representasi domain frekuensi, pelatihan model, hingga evaluasi hasil.
2. Membandingkan kinerja tiga arsitektur, yaitu model spasial berbasis Xception, model frekuensi berbasis CNN satu kanal, dan model hybrid dua cabang yang menggabungkan fitur spasial dan frekuensi.
3. Menguji pengaruh sumber data dan ukuran sampel pelatihan terhadap performa deteksi serta kemampuan generalisasi antardataset.

## 3.3 Lingkungan Implementasi

Implementasi penelitian dikembangkan dalam bahasa pemrograman Python dengan pustaka utama PyTorch sebagai kerangka pembelajaran mendalam. Beberapa pustaka pendukung yang digunakan dalam repositori ini meliputi torchvision untuk transformasi citra, timm untuk backbone Xception, NumPy untuk komputasi numerik, pandas untuk pengolahan tabular, scikit-learn untuk pembagian data dan evaluasi, OpenCV untuk ekstraksi frame video, Pillow untuk manipulasi citra, tqdm untuk progress monitoring, serta PyYAML untuk membaca konfigurasi eksperimen.

Repositori ini dijalankan pada lingkungan sistem operasi Windows dan menyediakan pipeline end-to-end melalui skrip otomatis, sehingga proses eksperimen dapat direplikasi secara konsisten. Seluruh konfigurasi inti, seperti ukuran citra, laju pembelajaran, jumlah epoch, dan lokasi dataset, didefinisikan melalui file konfigurasi YAML dan dapat dioverride melalui argumen command line ketika eksperimen dijalankan.

## 3.4 Data Penelitian dan Sumber Dataset

### 3.4.1 Dataset FaceForensics++

Dataset pertama yang digunakan adalah FaceForensics++ (FFPP). Pada struktur repositori ini, data FFPP ditempatkan pada direktori dataset/face_forensics dan mencakup video asli maupun video hasil manipulasi. Kategori manipulasi yang teridentifikasi pada repositori meliputi Deepfakes, Face2Face, FaceSwap, NeuralTextures, FaceShifter, dan DeepFakeDetection, sedangkan video asli berada pada kelompok original_sequences seperti actors dan youtube.

FaceForensics++ dipilih karena merupakan benchmark yang umum digunakan pada penelitian deteksi deepfake dan memiliki variasi teknik manipulasi yang cukup beragam. Keanekaragaman tersebut penting untuk menguji apakah model mampu mempelajari pola manipulasi yang lebih luas, bukan sekadar menghafal satu jenis artefak tertentu.

### 3.4.2 Dataset Celeb-DF

Dataset kedua yang digunakan adalah Celeb-DF (CDF) yang ditempatkan pada direktori dataset/celeb_df. Struktur data pada repositori ini memuat kategori Celeb-real, Celeb-synthesis, dan YouTube-real. Celeb-DF digunakan untuk melengkapi pengujian dengan dataset yang memiliki karakteristik manipulasi dan distribusi visual yang berbeda dari FaceForensics++.

Penggunaan dua dataset ini memungkinkan evaluasi yang lebih kuat terhadap kemampuan generalisasi model. Jika model hanya baik pada satu dataset, maka model tersebut belum tentu cukup andal untuk diterapkan pada kondisi nyata yang lebih bervariasi.

### 3.4.3 Unit Analisis Data

Unit analisis pada penelitian ini perlu dibedakan menjadi dua tingkat.

1. Tingkat video digunakan untuk pembentukan split data train, validation, dan test. Dengan demikian, satu video hanya dapat berada pada satu subset data sehingga kebocoran data antarsubset dapat dihindari.
2. Tingkat frame digunakan sebagai unit input model selama pelatihan dan pengujian. Setiap video yang lolos seleksi akan diekstraksi menjadi sejumlah frame, kemudian frame-frame tersebut diperlakukan sebagai sampel citra individual pada proses pembelajaran.

Pemilihan strategi ini penting karena split pada tingkat frame berpotensi menimbulkan data leakage. Jika frame-frame dari video yang sama tersebar ke train dan test, model dapat terlihat sangat baik padahal sebenarnya hanya mengenali pola spesifik video tersebut.

## 3.5 Variabel Penelitian

Desain eksperimen pada penelitian ini menggunakan tiga kelompok variabel, yaitu variabel bebas, variabel terikat, dan variabel terkendali.

### 3.5.1 Variabel Bebas

Variabel bebas dalam penelitian ini adalah sebagai berikut.

1. Arsitektur model, yang terdiri atas model spatial, model freq, dan model hybrid.
2. Dataset pelatihan, yaitu FFPP dan CDF.
3. Ukuran sampel video pelatihan per dataset, yaitu n = 50, n = 200, dan n = 400.
4. Skenario evaluasi, yaitu in-dataset dan cross-dataset.

### 3.5.2 Variabel Terikat

Variabel terikat pada penelitian ini adalah nilai performa model yang diukur menggunakan metrik berikut.

1. Accuracy.
2. Precision.
3. Recall.
4. F1-score.
5. Area Under Curve (AUC).

### 3.5.3 Variabel Terkendali

Untuk menjaga keadilan pembandingan, beberapa parameter dijaga tetap sama pada seluruh eksperimen utama.

1. Ukuran citra input: 224 x 224 piksel.
2. Frame sampling rate: 5 frame per detik.
3. Rasio split data: 70 persen train, 15 persen validation, dan 15 persen test.
4. Optimizer: Adam.
5. Learning rate: 0,0001.
6. Weight decay: 0,0001.
7. Batch size: 16.
8. Fungsi loss: Binary Cross Entropy with Logits.
9. Ambang klasifikasi probabilitas: 0,5.

Pada repositori ini, nilai konfigurasi dasar disimpan pada file config.yaml, sedangkan pada eksperimen utama beberapa parameter, seperti ukuran sampel, jumlah epoch, dan jumlah frame maksimum per video, dapat disesuaikan melalui skrip eksekusi pipeline. Pengaturan ini memungkinkan penelitian tetap konsisten secara metodologis, namun fleksibel untuk menjalankan beberapa skenario percobaan.

## 3.6 Rancangan Eksperimen

Rancangan eksperimen pada penelitian ini disusun untuk menjawab pertanyaan penelitian secara sistematis, terukur, dan dapat direplikasi. Secara umum, eksperimen dirancang untuk membandingkan tiga arsitektur model, yaitu model spatial, model freq, dan model hybrid, pada dua dataset yang berbeda, yaitu FFPP dan CDF, dengan tiga variasi ukuran sampel, yaitu n = 50, n = 200, dan n = 400 video per dataset. Setiap model kemudian diuji menggunakan dua skenario evaluasi, yaitu in-dataset dan cross-dataset.

Dengan struktur tersebut, rancangan eksperimen dalam penelitian ini tidak hanya menilai kemampuan klasifikasi model, tetapi juga menganalisis kestabilan performa ketika model dihadapkan pada distribusi data yang berbeda. Oleh sebab itu, bagian ini merupakan inti dari pengujian metodologis penelitian karena menjadi dasar pembandingan seluruh hasil pada bab berikutnya.

### 3.6.1 Tujuan Design Eksperimentasi

Design eksperimentasi pada penelitian ini disusun untuk memenuhi empat tujuan analitis.

1. Mengetahui perbedaan performa antara model berbasis domain spasial, domain frekuensi, dan model hybrid.
2. Mengetahui pengaruh sumber dataset pelatihan terhadap kualitas model yang dihasilkan.
3. Mengetahui pengaruh ukuran sampel pelatihan terhadap performa deteksi.
4. Mengetahui kemampuan generalisasi model ketika diterapkan pada dataset yang berbeda dari data latih.

Dengan empat tujuan tersebut, desain eksperimen tidak hanya berfungsi sebagai proses pengujian teknis, tetapi juga sebagai kerangka analisis untuk menilai apakah kombinasi domain spasial dan frekuensi benar-benar memberikan keunggulan yang konsisten.

### 3.6.2 Matriks Eksperimen Utama

Eksperimen utama pada repositori ini dapat diringkas sebagaimana Tabel 3.1.

| Komponen | Variasi |
| --- | --- |
| Model | Spatial, Freq, Hybrid |
| Dataset latih | FFPP, CDF |
| Ukuran sampel | n = 50, n = 200, n = 400 |
| Jenis evaluasi | In-dataset, Cross-dataset |
| Jumlah seed utama | 1 seed pada hasil yang tersedia di repositori |

Berdasarkan kombinasi tersebut, jumlah skenario evaluasi utama adalah 3 model x 2 dataset latih x 3 ukuran sampel x 2 jenis evaluasi = 36 skenario evaluasi.

### 3.6.3 Struktur Perbandingan Eksperimen

Agar rancangan eksperimen mudah dipahami, struktur pembandingannya dapat dijelaskan sebagai berikut.

1. Perbandingan antarmodel dilakukan dengan melatih model spatial, freq, dan hybrid pada dataset dan ukuran sampel yang sama.
2. Perbandingan antardataset dilakukan dengan melatih model pada FFPP dan CDF secara terpisah.
3. Perbandingan ukuran sampel dilakukan dengan menjalankan eksperimen pada n = 50, n = 200, dan n = 400.
4. Perbandingan generalisasi dilakukan dengan membandingkan hasil in-dataset terhadap hasil cross-dataset.

Melalui struktur tersebut, setiap perubahan nilai performa dapat ditelusuri berdasarkan faktor penyebabnya, apakah berasal dari arsitektur model, sumber data, atau jumlah sampel pelatihan.

### 3.6.4 Skenario In-Dataset

Pada skenario in-dataset, model dilatih dan diuji pada dataset yang sama. Contohnya, model dilatih menggunakan FFPP dan diuji pada subset test FFPP, atau dilatih menggunakan CDF dan diuji pada subset test CDF. Tujuan skenario ini adalah mengukur kemampuan model mempelajari pola manipulasi pada distribusi data yang sejenis.

Secara metodologis, skenario ini digunakan untuk menjawab pertanyaan apakah model mampu mengenali pola deepfake dengan baik ketika distribusi data uji masih konsisten dengan distribusi data pelatihan. Nilai performa pada skenario ini merepresentasikan kemampuan deteksi internal model.

### 3.6.5 Skenario Cross-Dataset

Pada skenario cross-dataset, model dilatih pada satu dataset dan diuji pada dataset lain. Contohnya, model dilatih pada FFPP lalu diuji pada CDF, atau dilatih pada CDF lalu diuji pada FFPP. Skenario ini sangat penting karena merepresentasikan kondisi yang lebih realistis, yaitu ketika model harus menghadapi data dari distribusi yang tidak identik dengan data pelatihan.

Secara metodologis, skenario ini digunakan untuk mengukur robustness dan kemampuan transfer representasi yang dipelajari model. Apabila terjadi penurunan performa yang signifikan, maka hal tersebut menunjukkan bahwa model cenderung mempelajari karakteristik spesifik dataset, bukan ciri umum manipulasi deepfake.

### 3.6.6 Pengukuran Generalization Drop

Selain metrik evaluasi standar, repositori ini juga menghitung penurunan generalisasi menggunakan selisih nilai F1 pada pengujian in-dataset dan cross-dataset. Secara matematis, penurunan generalisasi dihitung sebagai berikut.

$$
Drop = F1_{in} - F1_{cross}
$$

Semakin besar nilai drop, semakin besar penurunan performa model ketika berpindah dari pengujian pada dataset sejenis ke pengujian pada dataset yang berbeda. Nilai ini digunakan untuk melihat apakah model benar-benar mempelajari ciri deepfake yang umum atau hanya menyesuaikan diri terhadap karakteristik dataset tertentu.

### 3.6.7 Prosedur Pelaksanaan Eksperimen

Untuk setiap kombinasi model, dataset, dan ukuran sampel, eksperimen dijalankan melalui prosedur yang sama agar hasil yang diperoleh tetap adil dan dapat dibandingkan secara langsung. Prosedur tersebut adalah sebagai berikut.

1. Menentukan dataset dan ukuran sampel yang akan digunakan.
2. Melakukan ekstraksi frame dari video yang terpilih.
3. Membentuk train, validation, dan test split pada level video.
4. Menghasilkan cache FFT untuk seluruh frame yang diperlukan.
5. Melatih model sampai jumlah epoch yang ditentukan.
6. Memilih checkpoint terbaik berdasarkan validation AUC.
7. Mengevaluasi checkpoint terbaik pada test set in-dataset.
8. Mengevaluasi checkpoint yang sama pada dataset lain untuk memperoleh hasil cross-dataset.
9. Menyimpan seluruh hasil ke dalam tabel ringkasan eksperimen.

Keseragaman prosedur tersebut memastikan bahwa perbedaan hasil antarpercobaan terutama disebabkan oleh faktor eksperimen yang memang diuji, bukan oleh perbedaan proses pelaksanaan.

## 3.7 Alur Umum Pipeline Penelitian

Alur eksperimen pada repositori ini berjalan secara berurutan mulai dari data mentah hingga tabel hasil evaluasi. Secara konseptual, alur penelitian dapat diringkas sebagai berikut.

1. Menentukan dataset yang digunakan, yaitu FFPP dan CDF.
2. Memindai folder dataset untuk mengidentifikasi video asli dan video manipulasi berdasarkan keyword label.
3. Melakukan balanced sampling video sesuai jumlah sampel eksperimen yang ditetapkan.
4. Mengekstraksi frame dari setiap video yang terpilih.
5. Menyusun manifest video yang berisi video_id, label, dan lokasi folder frame.
6. Membagi data menjadi train, validation, dan test pada tingkat video secara stratified.
7. Menghitung representasi FFT log-magnitude untuk setiap frame dan menyimpannya sebagai cache.
8. Melatih model spatial, freq, dan hybrid menggunakan subset train.
9. Memilih checkpoint terbaik berdasarkan nilai validation AUC.
10. Mengevaluasi model pada subset test yang sejenis dan pada dataset lain.
11. Menghasilkan tabel ringkasan performa in-dataset, cross-dataset, dan generalization drop.

Alur tersebut tersedia secara otomatis melalui skrip run_pipeline.py dan run_all.py sehingga keseluruhan eksperimen dapat direplikasi dengan langkah yang konsisten. Jika diperlukan dalam naskah skripsi, urutan ini dapat divisualisasikan kembali dalam bentuk diagram alir penelitian dengan susunan Dataset -> Sampling -> Ekstraksi Frame -> Split Data -> FFT Cache -> Training -> Evaluasi -> Tabel Hasil.

## 3.8 Tahap Prapemrosesan Data

### 3.8.1 Identifikasi Label Video

Sebelum ekstraksi frame dilakukan, sistem terlebih dahulu memindai seluruh file video pada direktori dataset. Ekstensi video yang dikenali meliputi .mp4, .avi, .mov, dan .mkv. Label video tidak dibaca dari anotasi eksternal, melainkan diinferensi dari nama folder dan nama file menggunakan daftar keyword real_keywords dan fake_keywords yang didefinisikan pada file config.yaml.

Untuk FFPP, video asli dikenali dari keyword seperti original, real, pristine, actors, dan youtube, sedangkan video palsu dikenali dari keyword seperti fake, manipulated, deepfakes, faceswap, neuraltextures, deepfakedetection, faceshifter, dan face2face. Untuk CDF, video asli dikenali dari keyword real dan authentic, sedangkan video palsu dikenali dari keyword fake, synthesis, dan deepfake.

Pendekatan ini sesuai dengan struktur folder pada dataset yang tersedia di repositori dan memungkinkan proses penandaan label dilakukan secara otomatis.

### 3.8.2 Sampling Video untuk Skenario Eksperimen

Repositori ini mendukung eksperimen dengan jumlah video terbatas melalui parameter n-samples. Ketika parameter ini diaktifkan, sistem memilih video secara balanced antara kelas real dan fake. Secara operasional, prosedur sampling dilakukan sebagai berikut.

1. Seluruh video yang berhasil diberi label dikumpulkan.
2. Video dipisahkan menjadi dua kelompok, yaitu real dan fake.
3. Sistem mengambil jumlah video yang seimbang dari kedua kelompok sejauh data tersedia.
4. Jika distribusi kelas tidak sepenuhnya seimbang, sisa kuota diisi dari kelas yang masih memiliki video tersisa.
5. Daftar video terpilih diacak kembali sebelum diproses lebih lanjut.

Pada eksperimen utama yang tersedia di folder outputs, ukuran sampel yang digunakan adalah n = 50, n = 200, dan n = 400 video per dataset.

### 3.8.3 Ekstraksi Frame dari Video

Tahap berikutnya adalah ekstraksi frame menggunakan OpenCV. Setiap video dibaca dan diambil frame pada laju 5 frame per detik. Pada implementasi umum repositori, jumlah frame maksimum per video didefinisikan melalui parameter max_frames_per_video pada config.yaml. Untuk eksperimen utama, pipeline menyediakan override agar jumlah frame maksimum per video dapat ditetapkan melalui command line, dan skenario yang didokumentasikan pada command.txt menggunakan maksimum 100 frame per video.

Setiap frame disimpan dalam format JPG dengan pola nama frame_000000.jpg, frame_000001.jpg, dan seterusnya. Seluruh frame dari satu video dikelompokkan ke dalam satu folder khusus dengan nama video_id. Hasil ekstraksi disimpan pada struktur folder outputs/frames/[nama_dataset]/[video_id]/.

Tahap ini menghasilkan sebuah manifest awal pada level video yang berisi tiga kolom utama.

1. video_id.
2. label.
3. frames_dir.

Manifest tersebut disimpan pada outputs/manifests/[nama_dataset]/manifest.csv dan menjadi referensi utama untuk seluruh tahapan berikutnya.

### 3.8.4 Pembentukan Train, Validation, dan Test Split

Pembagian data dilakukan oleh skrip build_splits.py menggunakan metode train_test_split dari scikit-learn dengan stratifikasi berdasarkan label. Rasio split yang diterapkan adalah sebagai berikut.

1. Test set sebesar 15 persen dari total video.
2. Validation set sebesar 15 persen dari total video.
3. Train set sebesar 70 persen dari total video.

Karena split dilakukan pada level video_id, seluruh frame dari video yang sama akan tetap berada pada subset yang sama. Strategi ini dipilih untuk mencegah data leakage dan menjaga validitas evaluasi.

### 3.8.5 Prapemrosesan Domain Spasial

Frame RGB yang digunakan oleh model spatial dan cabang spasial pada model hybrid diproses menggunakan transformasi citra sebagai berikut.

Pada fase pelatihan:

1. Resize ke ukuran 256 x 256, yaitu image_size + 32 dari ukuran target 224 x 224.
2. RandomResizedCrop ke ukuran 224 x 224 dengan rentang skala 0,8 sampai 1,0.
3. RandomHorizontalFlip.
4. Konversi ke tensor.
5. Normalisasi menggunakan rata-rata dan deviasi standar ImageNet.

Pada fase validasi dan pengujian:

1. Resize langsung ke ukuran 224 x 224.
2. Konversi ke tensor.
3. Normalisasi menggunakan parameter ImageNet.

Strategi ini digunakan agar backbone Xception yang berasal dari ekosistem pretrained ImageNet tetap menerima distribusi input yang sesuai.

### 3.8.6 Prapemrosesan Domain Frekuensi dengan FFT

Representasi domain frekuensi dibangkitkan dari setiap frame melalui fungsi image_to_fft_logmag pada modul fft_utils.py. Prosedurnya adalah sebagai berikut.

1. Citra RGB dikonversi menjadi grayscale.
2. Citra grayscale diubah ukurannya menjadi 224 x 224 piksel.
3. Dihitung transformasi Fourier dua dimensi dengan FFT.
4. Spektrum dipindahkan ke pusat menggunakan fftshift.
5. Dihitung magnitude spectrum dengan operasi nilai absolut.
6. Magnitude dikompresi menggunakan logaritma log1p.
7. Nilai hasil transformasi dinormalisasi ke rentang 0 sampai 1.

Secara matematis, representasi frekuensi log-magnitude dapat dituliskan sebagai berikut.

$$
F(u,v) = \log\left(1 + \left|\operatorname{fftshift}(\operatorname{FFT2}(I_g))\right|\right)
$$

dengan $I_g$ menyatakan citra grayscale dari frame masukan.

Hasil FFT setiap frame disimpan terlebih dahulu ke dalam file .npy pada folder outputs/fft_cache/[nama_dataset]/[video_id]/. Penyimpanan cache ini dilakukan agar representasi frekuensi tidak perlu dihitung ulang setiap kali training dijalankan, sehingga eksperimen menjadi lebih efisien.

### 3.8.7 Penyusunan Data untuk Loader

Dataset loader pada repositori ini membaca manifest level video, lalu memperluasnya menjadi item level frame. Untuk setiap video, sistem membaca seluruh file frame yang tersedia pada folder frames_dir dan memilih paling banyak sejumlah max_frames_per_video. Jika jumlah frame melebihi batas, frame dipilih secara acak dengan seed yang tetap agar proses dapat direplikasi.

Format data yang diberikan ke model bergantung pada mode eksperimen.

1. Mode spatial mengembalikan tensor RGB tiga kanal.
2. Mode freq mengembalikan tensor FFT satu kanal.
3. Mode hybrid mengembalikan dua tensor terpisah, yaitu tensor RGB dan tensor FFT.
4. Mode early_fusion yang tersedia sebagai variasi tambahan menggabungkan RGB dan FFT menjadi tensor empat kanal.

Perlu ditekankan bahwa eksperimen utama yang dilaporkan pada tabel hasil repositori berfokus pada tiga model inti, yaitu spatial, freq, dan hybrid.

## 3.9 Arsitektur Model

### 3.9.1 Model Spatial Berbasis Xception

Model spatial menggunakan backbone Xception yang diakses melalui pustaka timm. Model dibangun dengan satu neuron output untuk klasifikasi biner dan menerima input tiga kanal RGB. Global average pooling digunakan pada akhir backbone untuk merangkum representasi fitur sebelum klasifikasi.

Model ini berfungsi sebagai baseline spasial, yaitu model yang hanya bergantung pada informasi visual di domain piksel. Jika model ini memiliki performa tinggi, maka dapat disimpulkan bahwa tekstur, bentuk, dan pola spasial pada frame sudah cukup informatif untuk mendeteksi manipulasi.

### 3.9.2 Model Frequency CNN

Model freq dirancang sebagai CNN sederhana satu kanal yang menerima peta FFT log-magnitude. Arsitektur utamanya terdiri atas tiga blok ekstraksi fitur konvolusional, yaitu:

1. Conv2D 1 ke 16, BatchNorm, ReLU, dan MaxPooling.
2. Conv2D 16 ke 32, BatchNorm, ReLU, dan MaxPooling.
3. Conv2D 32 ke 64, BatchNorm, ReLU, dan Adaptive Average Pooling.

Setelah fitur frekuensi diperoleh, classifier terdiri atas lapisan Flatten, Linear 64 ke 64, ReLU, Dropout 0,2, dan Linear 64 ke 1. Model ini digunakan untuk mengevaluasi seberapa jauh artefak pada domain frekuensi dapat dimanfaatkan tanpa bantuan fitur spasial.

### 3.9.3 Model Hybrid Dua Cabang

Model hybrid merupakan model utama yang diusulkan dalam implementasi repositori ini. Arsitektur ini menggunakan dua cabang yang berjalan paralel.

1. Cabang spasial menggunakan feature extractor Xception tanpa layer klasifikasi akhir, sehingga menghasilkan vektor fitur spasial.
2. Cabang frekuensi menggunakan bagian feature extractor dari FreqCNN untuk menghasilkan vektor fitur frekuensi.

Kedua vektor fitur tersebut kemudian digabungkan menggunakan operasi concatenation dan diteruskan ke classifier akhir yang terdiri atas:

1. Linear dari dimensi gabungan ke 256 unit.
2. ReLU.
3. Dropout 0,3.
4. Linear 256 ke 1.

Dengan desain ini, model hybrid tidak mencampurkan domain RGB dan FFT sejak awal, melainkan membiarkan masing-masing cabang mengekstraksi representasi spesifik terlebih dahulu. Pendekatan ini lebih sesuai dengan sifat kedua domain yang berbeda dan memberi peluang lebih besar bagi model untuk mempelajari fitur yang saling melengkapi.

### 3.9.4 Variasi Early Fusion

Repositori ini juga menyediakan variasi early_fusion, yaitu model Xception empat kanal yang menerima tumpukan RGB dan FFT secara langsung. Meskipun variasi ini tersedia pada kode sumber, tabel hasil utama pada repositori berfokus pada tiga model inti, yaitu spatial, freq, dan hybrid. Oleh karena itu, pembahasan utama pada penelitian ini menitikberatkan pada model hybrid dua cabang sebagai pendekatan yang diusulkan.

## 3.10 Strategi Pelatihan Model

### 3.10.1 Konfigurasi Pelatihan

Pelatihan model dilakukan menggunakan optimizer Adam dengan learning rate 0,0001 dan weight decay 0,0001. Fungsi loss yang digunakan adalah BCEWithLogitsLoss karena tugas yang dihadapi merupakan klasifikasi biner. Untuk sebuah logit $z$ dan label target $y$, fungsi loss secara konseptual dapat dituliskan sebagai berikut.

$$
\mathcal{L}(z, y) = -\left[y \log(\sigma(z)) + (1-y)\log(1-\sigma(z))\right]
$$

dengan $\sigma(z)$ adalah fungsi sigmoid.

Batch size yang digunakan adalah 16. Pada konfigurasi default repositori, jumlah epoch adalah 5. Namun, eksperimen utama yang didokumentasikan pada command.txt dan tercermin pada riwayat training di folder outputs/runs/n50, n200, dan n400 menggunakan 10 epoch. Dengan demikian, untuk penulisan laporan penelitian, parameter pelatihan utama yang lebih representatif terhadap eksperimen aktual adalah 10 epoch.

### 3.10.2 Pemanfaatan GPU dan Mixed Precision

Repositori ini secara otomatis menggunakan GPU apabila tersedia, dan kembali ke CPU apabila GPU tidak tersedia. Pada perangkat CUDA, pelatihan memanfaatkan automatic mixed precision melalui autocast dan GradScaler. Strategi ini bertujuan untuk mempercepat pelatihan dan mengurangi penggunaan memori tanpa mengubah desain metodologis eksperimen.

### 3.10.3 Gradient Accumulation

Untuk model hybrid dan early_fusion, repositori ini menggunakan gradient accumulation sebanyak 2 langkah secara default. Sementara itu, model spatial dan freq menggunakan 1 langkah. Pengaturan ini dilakukan untuk membantu kestabilan pelatihan model yang lebih berat tanpa harus menaikkan kebutuhan memori secara drastis.

### 3.10.4 Pemilihan Checkpoint Terbaik

Pada akhir setiap epoch, model dievaluasi menggunakan validation set. Nilai validation AUC menjadi dasar pemilihan checkpoint terbaik. Jika AUC pada epoch saat ini lebih tinggi daripada AUC terbaik sebelumnya, bobot model disimpan sebagai best.pt pada direktori outputs/runs/[model]_[dataset]_[tag]/.

Pemilihan checkpoint berdasarkan AUC lebih tepat dibandingkan akurasi semata karena AUC mempertimbangkan kualitas pemisahan kelas secara lebih menyeluruh dan lebih tahan terhadap perubahan threshold klasifikasi.

## 3.11 Metode Evaluasi

Setelah pelatihan selesai, checkpoint terbaik dievaluasi pada test set. Probabilitas prediksi diperoleh dengan menerapkan fungsi sigmoid pada logit keluaran model. Kelas prediksi kemudian ditentukan dengan threshold 0,5. Berdasarkan prediksi tersebut, repositori menghitung confusion matrix dan menurunkan beberapa metrik evaluasi.

### 3.11.1 Accuracy

Accuracy mengukur proporsi prediksi yang benar terhadap seluruh data uji.

$$
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
$$

### 3.11.2 Precision

Precision mengukur proporsi prediksi positif yang benar-benar positif.

$$
Precision = \frac{TP}{TP + FP}
$$

### 3.11.3 Recall

Recall mengukur proporsi data positif yang berhasil dikenali sebagai positif.

$$
Recall = \frac{TP}{TP + FN}
$$

### 3.11.4 F1-Score

F1-score merupakan harmonic mean dari precision dan recall.

$$
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
$$

### 3.11.5 AUC

AUC digunakan untuk mengukur kemampuan model dalam membedakan kelas real dan fake secara threshold-independent. Dalam repositori ini, AUC dihitung menggunakan roc_auc_score dari scikit-learn.

### 3.11.6 Tabel Evaluasi Otomatis

Repositori menghasilkan tiga tabel utama setelah eksperimen selesai.

1. Table1_in_dataset.csv untuk performa pada skenario in-dataset.
2. Table2_cross_dataset.csv untuk performa pada skenario cross-dataset.
3. Table3_generalization_drop.csv untuk selisih F1 antara pengujian in-dataset dan cross-dataset.

Tabel-tabel tersebut disimpan pada folder outputs/tables/[n]/ dan menjadi dasar analisis pada bab hasil dan pembahasan.

## 3.12 Langkah Implementasi Eksperimen

Bagian ini menjelaskan prosedur operasional yang dapat digunakan untuk mereplikasi eksperimen pada repositori secara langsung. Penyajian langkah implementasi ini penting untuk menegaskan bahwa penelitian tidak berhenti pada tingkat konseptual, melainkan benar-benar dijalankan melalui tahapan komputasional yang terstruktur.

### 3.12.1 Persiapan Lingkungan

1. Membuat virtual environment Python.
2. Mengaktifkan virtual environment.
3. Menginstal seluruh dependensi dari requirements.txt.
4. Memastikan struktur dataset FFPP dan CDF sudah berada pada direktori yang sesuai.

Contoh perintah:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3.12.2 Konfigurasi Dataset

1. Menyesuaikan path dataset pada file config.yaml.
2. Memastikan output_root mengarah ke folder outputs.
3. Memastikan daftar real_keywords dan fake_keywords sesuai struktur folder dataset.

### 3.12.3 Menjalankan Pipeline Lengkap

Repositori menyediakan skrip run_pipeline.py untuk menjalankan seluruh tahapan eksperimen secara otomatis, meliputi ekstraksi frame, pembentukan split data, pembuatan FFT cache, pelatihan model, evaluasi, dan pembuatan tabel hasil.

Untuk eksperimen utama yang digunakan pada penelitian ini, variasi ukuran sampel dijalankan sebagai berikut.

```bash
python scripts\run_pipeline.py --n-samples 50 --max-frames 100 --epochs 10 --pretrained
python scripts\run_pipeline.py --n-samples 200 --max-frames 100 --epochs 10 --pretrained
python scripts\run_pipeline.py --n-samples 400 --max-frames 100 --epochs 10 --pretrained
```

Makna parameter utama adalah sebagai berikut.

1. n-samples menyatakan jumlah video per dataset pada skenario eksperimen.
2. max-frames menyatakan jumlah frame maksimum per video.
3. epochs menyatakan jumlah putaran pelatihan.
4. pretrained menyatakan bahwa backbone Xception menggunakan bobot awal pretrained.

### 3.12.4 Menjalankan Tahapan Secara Parsial

Jika diperlukan, setiap tahap juga dapat dijalankan secara terpisah sebagai berikut.

1. Ekstraksi frame:

```bash
python scripts\extract_frames.py --config config.yaml --dataset FFPP --fps 5 --max-frames 100 --n-samples 400
python scripts\extract_frames.py --config config.yaml --dataset CDF --fps 5 --max-frames 100 --n-samples 400
```

1. Pembentukan split data:

```bash
python scripts\build_splits.py --config config.yaml --dataset FFPP
python scripts\build_splits.py --config config.yaml --dataset CDF
```

1. Pembangkitan FFT cache:

```bash
python scripts\compute_fft_cache.py --config config.yaml --dataset FFPP --num-workers 4
python scripts\compute_fft_cache.py --config config.yaml --dataset CDF --num-workers 4
```

1. Pelatihan model individual:

```bash
python scripts\train.py --config config.yaml --dataset FFPP --model spatial --pretrained
python scripts\train.py --config config.yaml --dataset FFPP --model freq
python scripts\train.py --config config.yaml --dataset FFPP --model hybrid --pretrained
```

1. Evaluasi checkpoint individual:

```bash
python scripts\eval.py --config config.yaml --dataset CDF --model hybrid --checkpoint outputs\runs\hybrid_FFPP_n400_seed0\best.pt
```

### 3.12.5 Alur Output Eksperimen

Output yang dihasilkan pipeline tersusun sebagai berikut.

1. outputs/frames untuk frame hasil ekstraksi.
2. outputs/manifests untuk manifest video dan split train, validation, test.
3. outputs/fft_cache untuk cache FFT per frame.
4. outputs/runs untuk checkpoint model, log pelatihan, dan riwayat metrik validation.
5. outputs/tables untuk tabel hasil evaluasi.

Dengan struktur ini, setiap tahap eksperimen dapat ditelusuri kembali secara sistematis. Kejelasan struktur output juga penting dalam konteks penelitian akademik karena memudahkan proses audit hasil, penelusuran ulang eksperimen, dan penyusunan analisis pada bab pembahasan.

## 3.13 Ringkasan Metodologi

Berdasarkan implementasi repositori, metodologi penelitian ini dibangun di atas prinsip evaluasi yang terkontrol dan dapat direplikasi. Data diproses dari level video ke level frame, tetapi pembagian subset dilakukan pada level video untuk mencegah kebocoran data. Representasi deepfake dianalisis melalui dua domain, yaitu domain spasial dan domain frekuensi, kemudian dibandingkan melalui tiga arsitektur model utama: spatial, freq, dan hybrid.

Desain eksperimen yang menggunakan dua dataset, tiga ukuran sampel, serta dua skenario evaluasi memungkinkan penelitian ini tidak hanya menilai performa deteksi, tetapi juga menilai generalisasi model. Dengan demikian, BAB III ini memberikan fondasi metodologis yang kuat bagi analisis hasil pada bab berikutnya.
