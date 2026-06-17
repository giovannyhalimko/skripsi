# BAB IV HASIL DAN PEMBAHASAN

Bab ini menyajikan hasil eksperimen dari ketiga arsitektur model yang dirancang pada BAB III, yaitu model spasial (*XceptionNet*), model frekuensi (*FreqCNN*), dan model *hybrid* (*HybridTwoBranch*), beserta pembahasannya. Hasil dipaparkan secara objektif pada subbab 4.1 dalam bentuk tabel dan gambar, kemudian dianalisis pada subbab 4.2 untuk menjawab setiap rumusan masalah yang diajukan pada BAB I. Seluruh angka yang dilaporkan merupakan rata-rata dari tiga *seed* (0, 1, 2) beserta simpangan bakunya, dihitung pada level *frame* dari set pengujian yang dipisahkan pada level video. Penelitian ini bersifat komparatif: ketiga model diperlakukan sebagai studi *ablation* terkontrol untuk mengukur kontribusi masing-masing domain analisis, bukan untuk membuktikan keunggulan satu arsitektur secara apriori.

## 4.1 Hasil

Subbab ini memaparkan hasil pengujian model pada dua skenario evaluasi utama, yaitu evaluasi *in-dataset* (dilatih dan diuji pada dataset yang sama) dan evaluasi *cross-dataset* (diuji pada dataset yang berbeda dari data pelatihan), serta analisis pendukung berupa *generalization drop*, pengaruh ukuran sampel, kurva ROC, dan *confusion matrix*. Sebelum hasil pengujian dipaparkan, terlebih dahulu diuraikan lingkungan dan konfigurasi eksperimen yang menjadi dasar seluruh pengukuran, serta purwarupa sistem yang dibangun dari model terlatih.

### 4.1.1 Lingkungan dan Konfigurasi Eksperimen

Seluruh eksperimen dijalankan pada lingkungan komputasi berbasis GPU dengan kerangka kerja *PyTorch* dan pustaka *timm* untuk *backbone* XceptionNet, sebagaimana spesifikasi perangkat keras dan perangkat lunak telah dirinci pada BAB III (Tabel 3.15 dan Tabel 3.16). Konfigurasi hyperparameter yang digunakan konsisten untuk seluruh model dan telah dirangkum pada Tabel 3.10, mencakup optimizer *AdamW* (*learning rate* dasar 2 × 10⁻⁴), *gradient accumulation* dua langkah (*batch* efektif 32), *early stopping* berdasarkan AUC validasi dengan *patience* 12, serta pembekuan *backbone* selama tiga *epoch* pertama. Pemilihan model terbaik didasarkan pada AUC validasi tertinggi.

Untuk memperoleh perbandingan yang menyeluruh, eksperimen dirancang sebagai matriks penuh atas tiga faktor, yaitu jenis model, dataset pelatihan, dan ukuran sampel, dengan masing-masing kombinasi diulang pada tiga *seed* untuk mengukur stabilitas hasil. Rincian matriks eksperimen ditunjukkan pada Tabel 4.1.

**Tabel 4.1 Matriks Eksperimen**

| Faktor | Nilai | Jumlah |
|---|---|---|
| Model | spatial, freq, hybrid | 3 |
| Dataset pelatihan | FaceForensics++ (FFPP), Celeb-DF v2 (CDF) | 2 |
| Ukuran sampel (video) | 100, 250, 500, 750 | 4 |
| Skenario evaluasi | *in-dataset*, *cross-dataset* | 2 |
| *Seed* | 0, 1, 2 | 3 |

Evaluasi dilakukan pada dua arah, yaitu evaluasi *in-dataset* (FFPP→FFPP dan CDF→CDF) dan evaluasi *cross-dataset* (FFPP→CDF dan CDF→FFPP). Metrik yang dihitung meliputi akurasi, presisi, *recall*, *F1-score*, dan AUC. Khusus pada tier ukuran sampel terkecil (n = 100), set pengujian hanya terdiri atas sekitar 15 video sehingga hasilnya rentan terhadap *noise* pencuplikan; oleh karena itu analisis utama pada bab ini bertumpu pada tier yang lebih andal, yaitu n = 250, n = 500, dan n = 750, dengan tier n = 750 dipakai sebagai representasi utama.

### 4.1.2 Implementasi dan Purwarupa Sistem

Selain dievaluasi secara kuantitatif, model terlatih juga diwujudkan menjadi sebuah purwarupa sistem deteksi yang dapat dioperasikan secara langsung. Purwarupa ini dibangun menggunakan kerangka *Gradio* dan di-*deploy* ke layanan Hugging Face Spaces, sehingga dapat diakses melalui peramban tanpa instalasi. Berbeda dari aplikasi deteksi pada umumnya yang hanya menampilkan satu keputusan, purwarupa ini sengaja dirancang sebagai alat **perbandingan tiga model**: untuk satu video yang diunggah, sistem menjalankan model spasial, *hybrid*, dan frekuensi secara berdampingan dan menampilkan verdict ketiganya, sejalan dengan sifat komparatif penelitian ini.

Alur inferensi pada purwarupa mengikuti pipeline pelatihan secara konsisten. Video yang diunggah dicuplik pada 5 *frame per second* (maksimum 16 *frame*), setiap *frame* dideteksi dan dipotong wajahnya menggunakan MTCNN dengan margin 0,3, lalu dipreproses identik dengan tahap pelatihan (RGB menjadi 224×224 dengan normalisasi ImageNet; peta FFT *log-magnitude* dengan normalisasi statistik dataset). Probabilitas-*fake* per-*frame* kemudian diagregasi menjadi satu keputusan level-video dengan merata-ratakan seluruh *frame*, dan video dinyatakan *fake* apabila rata-rata tersebut mencapai ambang keputusan masing-masing model. Tampilan antarmuka purwarupa beserta kartu verdict ketiga model ditunjukkan pada Gambar 4.1.

*Gambar 4.1 Antarmuka purwarupa perbandingan tiga model pada Hugging Face Spaces*

Selain kartu verdict, purwarupa menyediakan panel "*what the models see*" yang menampilkan potongan wajah hasil *cropping* (masukan cabang spasial) berdampingan dengan spektrum FFT-nya (masukan cabang frekuensi). Panel ini memberikan gambaran kualitatif mengenai informasi yang sebenarnya diproses oleh masing-masing cabang, sebagaimana ditunjukkan pada Gambar 4.2, dan akan dirujuk kembali pada pembahasan akar penyebab lemahnya cabang frekuensi (subbab 4.2.4).

*Gambar 4.2 Panel "what the models see": potongan wajah (masukan spasial) dan spektrum FFT (masukan frekuensi)*

### 4.1.3 Hasil Evaluasi In-Dataset

Evaluasi *in-dataset* mengukur kemampuan dasar setiap model ketika dilatih dan diuji pada distribusi data yang sama. Hasil pada tier n = 750 untuk kedua dataset disajikan pada Tabel 4.2, sedangkan perbandingan visualnya ditunjukkan pada Gambar 4.3.

**Tabel 4.2 Hasil Evaluasi In-Dataset (n = 750, rata-rata ± simpangan baku atas 3 seed)**

| Dataset | Model | Akurasi | Presisi | Recall | F1-Score | AUC |
|---|---|---|---|---|---|---|
| FFPP | spatial | 0,700 ± 0,002 | 0,662 ± 0,005 | 0,766 ± 0,009 | 0,710 ± 0,001 | **0,780 ± 0,002** |
| FFPP | hybrid | 0,610 ± 0,007 | 0,588 ± 0,007 | 0,618 ± 0,012 | 0,603 ± 0,008 | 0,650 ± 0,008 |
| FFPP | freq | 0,531 ± 0,024 | 0,512 ± 0,028 | 0,560 ± 0,131 | 0,529 ± 0,055 | 0,546 ± 0,037 |
| CDF | spatial | 0,915 ± 0,003 | 0,906 ± 0,010 | 0,912 ± 0,007 | 0,909 ± 0,003 | **0,969 ± 0,001** |
| CDF | hybrid | 0,858 ± 0,014 | 0,851 ± 0,034 | 0,843 ± 0,023 | 0,847 ± 0,013 | 0,924 ± 0,005 |
| CDF | freq | 0,563 ± 0,016 | 0,529 ± 0,018 | 0,495 ± 0,039 | 0,511 ± 0,028 | 0,586 ± 0,028 |

*Gambar 4.3 Perbandingan performa in-dataset ketiga model pada FFPP dan CDF (n = 750)*

Pada kedua dataset, model spasial memperoleh nilai tertinggi pada seluruh metrik, diikuti model *hybrid*, dan model frekuensi pada posisi terendah. Pada FFPP, AUC model spasial mencapai 0,780, sedangkan model *hybrid* dan frekuensi masing-masing 0,650 dan 0,546. Pola yang sama terjadi pada CDF dengan selisih yang lebih lebar, yaitu AUC 0,969 untuk model spasial, 0,924 untuk *hybrid*, dan 0,586 untuk frekuensi. Dataset CDF secara konsisten lebih mudah dideteksi dibanding FFPP bagi seluruh model. Nilai AUC model frekuensi yang berada pada kisaran 0,55–0,59 menunjukkan kemampuan diskriminasi yang hanya sedikit di atas tebakan acak (0,5). Urutan peringkat ini stabil, terlihat dari simpangan baku antar-*seed* yang kecil terutama pada model spasial.

Selain perbandingan nilai metrik, kemampuan diskriminasi model pada seluruh rentang ambang ditunjukkan melalui kurva ROC pada Gambar 4.4. Urutan luas area di bawah kurva (AUC) konsisten dengan Tabel 4.2, dengan kurva model spasial berada paling jauh dari garis diagonal acak dan kurva model frekuensi paling mendekatinya.

*Gambar 4.4 Kurva ROC evaluasi in-dataset ketiga model (FFPP dan CDF, n = 750)*

### 4.1.4 Hasil Evaluasi Cross-Dataset

Evaluasi *cross-dataset* mengukur kemampuan generalisasi model terhadap dataset yang tidak pernah dilihat saat pelatihan, yang merepresentasikan skenario dunia nyata ketika metode manipulasi baru terus bermunculan. Hasil untuk kedua arah pengujian pada tier n = 750 disajikan pada Tabel 4.3, dan perbandingan visualnya pada Gambar 4.5.

**Tabel 4.3 Hasil Evaluasi Cross-Dataset (n = 750, rata-rata ± simpangan baku atas 3 seed)**

| Arah | Model | Akurasi | Presisi | Recall | F1-Score | AUC |
|---|---|---|---|---|---|---|
| FFPP→CDF | spatial | 0,608 ± 0,006 | 0,571 ± 0,007 | 0,618 ± 0,012 | 0,594 ± 0,008 | 0,648 ± 0,013 |
| FFPP→CDF | hybrid | 0,611 ± 0,025 | 0,584 ± 0,036 | 0,570 ± 0,016 | 0,576 ± 0,009 | 0,648 ± 0,031 |
| FFPP→CDF | freq | 0,550 ± 0,005 | 0,621 ± 0,027 | 0,069 ± 0,017 | 0,124 ± 0,027 | 0,655 ± 0,007 |
| CDF→FFPP | spatial | 0,558 ± 0,003 | 0,932 ± 0,026 | 0,083 ± 0,009 | 0,153 ± 0,015 | 0,629 ± 0,001 |
| CDF→FFPP | hybrid | 0,569 ± 0,012 | 0,789 ± 0,082 | 0,143 ± 0,056 | 0,237 ± 0,073 | 0,563 ± 0,011 |
| CDF→FFPP | freq | 0,571 ± 0,007 | 0,549 ± 0,012 | 0,596 ± 0,072 | 0,570 ± 0,026 | 0,591 ± 0,002 |

*Gambar 4.5 Perbandingan performa cross-dataset ketiga model pada kedua arah pengujian (n = 750)*

Dibandingkan evaluasi *in-dataset*, performa seluruh model menurun tajam pada skenario *cross-dataset*, dengan AUC berada pada kisaran 0,56–0,66. Penurunan paling mencolok tampak pada metrik *recall* di beberapa konfigurasi. Pada arah CDF→FFPP, model spasial mencatat presisi sangat tinggi (0,932) namun *recall* runtuh menjadi 0,083, yang berarti model nyaris tidak mengenali sampel *fake* dari dataset yang berbeda; pola serupa terjadi pada model *hybrid* (presisi 0,789, *recall* 0,143). Sebaliknya, pada arah FFPP→CDF, model frekuensi mengalami keruntuhan *recall* (0,069) sementara model spasial dan *hybrid* mempertahankan *recall* yang lebih wajar (0,618 dan 0,570). Kurva ROC untuk skenario *cross-dataset* ditunjukkan pada Gambar 4.6, memperlihatkan seluruh kurva yang jauh lebih dekat ke garis diagonal dibanding kurva *in-dataset*.

*Gambar 4.6 Kurva ROC evaluasi cross-dataset ketiga model (kedua arah, n = 750)*

### 4.1.5 Analisis Generalization Drop

*Generalization drop* (Δ) mengukur besarnya degradasi performa antara evaluasi *in-dataset* dan *cross-dataset*, dihitung sebagai selisih *F1-score* keduanya sebagaimana didefinisikan pada BAB II. Nilai Δ yang kecil menandakan generalisasi yang baik, sedangkan nilai yang besar menandakan ketergantungan model pada pola spesifik dataset pelatihan. Hasil perhitungan untuk tier n = 750 disajikan pada Tabel 4.4 dan divisualisasikan pada Gambar 4.7.

**Tabel 4.4 Generalization Drop F1-Score (n = 750)**

| Model | Dataset latih | F1 in-dataset | F1 cross-dataset | Δ |
|---|---|---|---|---|
| spatial | FFPP | 0,710 | 0,594 | +0,116 |
| spatial | CDF | 0,909 | 0,153 | +0,756 |
| hybrid | FFPP | 0,603 | 0,576 | **+0,027** |
| hybrid | CDF | 0,847 | 0,237 | +0,609 |
| freq | FFPP | 0,529 | 0,124 | +0,406 |
| freq | CDF | 0,511 | 0,570 | −0,058 |

*Gambar 4.7 Generalization drop F1-Score per model dan arah pelatihan (n = 750)*

Besarnya *generalization drop* sangat bergantung pada arah pelatihan. Pada model yang dilatih CDF, degradasi sangat besar, yaitu Δ = +0,756 untuk spasial dan Δ = +0,609 untuk *hybrid*. Sebaliknya, pada model yang dilatih FFPP, degradasi jauh lebih kecil, bahkan model *hybrid* mencatat Δ = +0,027 yang merupakan nilai terkecil di antara seluruh konfigurasi. Adapun model frekuensi menunjukkan Δ yang kecil hingga negatif (−0,058 pada pelatihan CDF); namun nilai ini perlu ditafsirkan dengan hati-hati karena performa *in-dataset* model frekuensi memang sudah rendah, sehingga praktis tidak ada performa yang dapat turun. Interpretasi atas pola ini diuraikan lebih lanjut pada subbab 4.2.

### 4.1.6 Pengaruh Ukuran Sampel terhadap Performa

Untuk mengamati pengaruh jumlah data pelatihan, performa diukur pada tiga tier ukuran sampel yang andal, yaitu n = 250, n = 500, dan n = 750. Nilai AUC *in-dataset* untuk setiap tier disajikan pada Tabel 4.5, dan trennya divisualisasikan pada Gambar 4.8.

**Tabel 4.5 AUC In-Dataset pada Berbagai Ukuran Sampel**

| Dataset | Model | n = 250 | n = 500 | n = 750 |
|---|---|---|---|---|
| FFPP | spatial | 0,746 | 0,693 | 0,780 |
| FFPP | hybrid | 0,542 | 0,582 | 0,650 |
| FFPP | freq | 0,480 | 0,570 | 0,546 |
| CDF | spatial | 0,942 | 0,967 | 0,969 |
| CDF | hybrid | 0,812 | 0,892 | 0,924 |
| CDF | freq | 0,569 | 0,615 | 0,586 |

*Gambar 4.8 Tren AUC terhadap ukuran sampel pelatihan (in-dataset dan cross-dataset)*

Secara umum, performa meningkat seiring bertambahnya ukuran sampel, paling jelas terlihat pada model spasial dan *hybrid* di dataset CDF yang naik konsisten dari n = 250 hingga n = 750. Peningkatan pada dataset FFPP berlangsung lebih fluktuatif; sebagai contoh, AUC model spasial pada FFPP sempat menurun di n = 500 sebelum kembali naik pada n = 750, yang mencerminkan tingkat kesulitan FFPP yang lebih tinggi dan variasi antar-*seed* yang lebih besar. Adapun model frekuensi tetap berada pada kisaran rendah (AUC ≈ 0,48–0,62) di seluruh tier, menandakan bahwa penambahan data tidak secara berarti memperbaiki kemampuan cabang frekuensi. Urutan peringkat antar model (spasial > *hybrid* > frekuensi) tidak berubah pada seluruh ukuran sampel.

### 4.1.7 Confusion Matrix dan Dinamika Pelatihan

Untuk melengkapi gambaran kualitatif perilaku model, disajikan pula *confusion matrix* dan kurva dinamika pelatihan. *Confusion matrix* memperjelas pola kesalahan klasifikasi pada ambang keputusan optimal, khususnya fenomena keruntuhan *recall* pada skenario *cross-dataset* yang telah teramati pada Tabel 4.3. Contoh *confusion matrix* model pada evaluasi *in-dataset* dan *cross-dataset* ditunjukkan pada Gambar 4.9.

*Gambar 4.9 Confusion matrix model pada evaluasi in-dataset dan cross-dataset (n = 750)*

Sementara itu, kurva dinamika pelatihan memperlihatkan perbedaan karakter konvergensi antar model. Kurva untuk cabang frekuensi dan cabang spasial pada dataset FFPP ditunjukkan pada Gambar 4.10. Kurva pelatihan model frekuensi memperlihatkan AUC validasi yang stagnan pada kisaran rendah sejak awal pelatihan, menandakan bahwa model kesulitan mempelajari pola diskriminatif, sedangkan kurva model spasial menunjukkan peningkatan AUC validasi yang jelas hingga mencapai konvergensi. Temuan ini memperkuat hasil kuantitatif pada Tabel 4.2 dan menjadi dasar pembahasan pada subbab 4.2.4.

*Gambar 4.10 Kurva dinamika pelatihan model frekuensi dan model spasial (FFPP, n = 750)*

## 4.2 Pembahasan

Subbab ini menganalisis hasil yang telah dipaparkan pada subbab 4.1 dan mengaitkannya secara langsung dengan ketiga rumusan masalah penelitian. Pembahasan diawali dengan kontribusi masing-masing domain, dilanjutkan dengan analisis penurunan performa lintas dataset dan pengaruh penambahan domain frekuensi, kemudian analisis akar penyebab lemahnya cabang frekuensi, keterbatasan penelitian, dan diakhiri dengan ringkasan jawaban atas seluruh rumusan masalah.

### 4.2.1 Kontribusi Domain Spasial dan Domain Frekuensi

Pembahasan ini menjawab rumusan masalah ketiga (RM3) mengenai besarnya kontribusi masing-masing komponen terhadap performa deteksi. Berdasarkan rancangan *ablation* tiga model, kontribusi setiap domain dapat dibaca langsung dari Tabel 4.2. Model spasial yang hanya memanfaatkan fitur visual XceptionNet justru menjadi penyumbang performa terbesar, dengan AUC *in-dataset* mencapai 0,969 pada CDF dan 0,780 pada FFPP. Hal ini selaras dengan temuan Rössler et al. (2019) dan Chollet (2017) yang menunjukkan XceptionNet sebagai *baseline* spasial yang sangat efektif untuk deteksi manipulasi wajah.

Sebaliknya, model frekuensi yang hanya memanfaatkan peta FFT memberikan kontribusi yang sangat terbatas, dengan AUC yang hanya sedikit di atas tebakan acak (0,546–0,586). Konsekuensinya, penggabungan kedua domain pada model *hybrid* tidak menghasilkan peningkatan, melainkan justru menurunkan performa dibanding model spasial murni pada seluruh tier *in-dataset* yang andal dan pada kedua dataset. Dengan kata lain, dalam konfigurasi penelitian ini, fitur frekuensi tidak berperan sebagai informasi pelengkap yang memperkuat fitur spasial, tetapi cenderung menjadi sumber *noise* yang menyeret turun performa fusi. Temuan ini merupakan hasil negatif yang penting dan menjadi inti dari sifat komparatif penelitian.

### 4.2.2 Penurunan Performa Model Spasial pada Cross-Dataset

Pembahasan ini menjawab rumusan masalah pertama (RM1) mengenai sejauh mana detektor spasial murni menurun performanya saat diuji lintas dataset. Berdasarkan Tabel 4.3 dan Tabel 4.4, model spasial mengalami degradasi yang nyata, dengan AUC turun dari 0,780–0,969 pada *in-dataset* menjadi 0,629–0,648 pada *cross-dataset*. Degradasi paling parah terjadi pada arah CDF→FFPP, dengan *generalization drop* F1 mencapai +0,756 dan *recall* runtuh menjadi 0,083.

Penurunan ini bersifat asimetris terhadap arah pengujian. Model yang dilatih pada CDF mengalami keruntuhan lebih besar ketika diuji pada FFPP dibanding sebaliknya. Hal ini dapat dipahami dari karakteristik kedua dataset: CDF dihasilkan oleh satu metode sintesis yang relatif homogen, sehingga model yang dilatih padanya mempelajari pola artefak yang sempit dan gagal mengeneralisasi ke FFPP yang memuat empat metode manipulasi berbeda. Pola domain shift seperti ini konsisten dengan temuan Rössler et al. (2019) dan Ma et al. (2025) yang menunjukkan bahwa detektor berbasis fitur spasial mudah terjebak pada artefak spesifik dataset pelatihan. Dengan demikian, RM1 terjawab: detektor spasial murni memang mengalami penurunan performa yang substansial pada skenario lintas dataset, terutama dalam bentuk keruntuhan *recall*.

### 4.2.3 Pengaruh Penambahan FFT terhadap Penurunan Performa

Pembahasan ini menjawab rumusan masalah kedua (RM2) mengenai sejauh mana penambahan analisis domain frekuensi dapat memperkecil penurunan performa lintas dataset. Jawabannya bersifat parsial dan bergantung pada arah pengujian. Di satu sisi, pada arah FFPP→CDF, penambahan domain frekuensi tampak menahan degradasi: model *hybrid* mencatat *generalization drop* F1 sebesar +0,027, jauh lebih kecil dibanding model spasial (+0,116), bahkan F1 *cross-dataset* *hybrid* (0,576) sedikit di bawah spasial (0,594) namun dengan kestabilan yang lebih baik. Pada tier n = 250 dan n = 500 yang dilaporkan pada analisis pendukung, F1 *cross-dataset* model *hybrid* bahkan melampaui model spasial pada arah ini.

Di sisi lain, keuntungan tersebut tidak konsisten. Pada arah CDF→FFPP, model *hybrid* tetap mengalami keruntuhan (*recall* 0,143, Δ = +0,609), dan dari sisi AUC *cross-dataset*, model *hybrid* tidak secara meyakinkan mengungguli model spasial (misalnya pada arah FFPP→CDF keduanya setara di 0,648, sedangkan pada CDF→FFPP spasial 0,629 lebih tinggi dari *hybrid* 0,563). Yang terpenting, keuntungan generalisasi parsial ini diperoleh dengan mengorbankan performa *in-dataset* yang jauh lebih rendah. Oleh karena itu, RM2 terjawab dengan kesimpulan yang jujur: penambahan analisis FFT dapat memperkecil *generalization drop* pada arah tertentu, tetapi tidak menghasilkan peningkatan generalisasi yang konsisten dan menyeluruh, sebagian karena cabang frekuensi yang lemah membatasi manfaat fusi. Kesulitan generalisasi lintas dataset yang dialami seluruh model juga sejalan dengan karakteristik masalah yang memang sulit sebagaimana dilaporkan Tan et al. (2024).

### 4.2.4 Analisis Akar Penyebab Lemahnya Cabang Frekuensi

Temuan bahwa cabang frekuensi berperforma nyaris acak merupakan inti yang perlu dijelaskan, karena pada literatur fitur frekuensi sering dilaporkan informatif untuk deteksi *deepfake*. Beberapa faktor dapat menjelaskan hal ini. Pertama, sidik jari spektral dari proses *upsampling* GAN yang menjadi dasar deteksi frekuensi (Durall et al., 2020; Odena et al., 2016) sangat rentan rusak oleh dua tahap praproses pada penelitian ini, yaitu *cropping* wajah dengan MTCNN dan kompresi video c23. *Cropping* menghilangkan konteks tepi dan latar yang turut membawa jejak frekuensi, sedangkan kompresi menekan komponen frekuensi tinggi tempat artefak tersebut termanifestasi; hal ini konsisten dengan temuan Mejri et al. (2021) bahwa kompresi merusak petunjuk frekuensi tinggi. Bukti kualitatif untuk dugaan ini tampak pada panel "*what the models see*" (Gambar 4.2), di mana spektrum FFT wajah *real* dan *fake* nyaris tidak dapat dibedakan secara visual.

Kedua, karena cabang frekuensi berada di sekitar tebakan acak, ia praktis menyuntikkan *noise* ke dalam representasi fusi, dan mekanisme *Squeeze-and-Excitation gating* yang dirancang untuk membobot kepentingan fitur ternyata tidak cukup untuk menekan cabang yang buruk tersebut secara penuh. Hal ini sejalan dengan pengamatan pada literatur bahwa pemanfaatan domain frekuensi yang efektif memerlukan mekanisme yang lebih canggih daripada sekadar memasukkan peta FFT sebagai cabang tambahan, seperti dekomposisi *frequency-aware* dan pembelajaran kolaboratif pada Qian et al. (2020) atau fusi dua-domain dengan atensi khusus pada Alam et al. (2025). Stagnasi kurva pelatihan model frekuensi (Gambar 4.10) memperkuat bahwa cabang ini memang gagal mempelajari pola diskriminatif sejak awal, bukan sekadar kurang optimal pada tahap akhir.

### 4.2.5 Keterbatasan Penelitian

Beberapa keterbatasan perlu dicatat dalam menafsirkan hasil penelitian ini. Pertama, jumlah data pelatihan dibatasi hingga 750 video per dataset dan hanya menggunakan tingkat kompresi c23, sehingga hasil belum tentu berlaku pada rezim data yang jauh lebih besar atau pada tingkat kompresi lain. Kedua, evaluasi dilakukan pada level *frame* tanpa memanfaatkan informasi temporal antar-*frame*, sehingga pola manipulasi yang bersifat dinamis tidak ditangkap. Ketiga, hasil pada tier n = 100 bersifat *noisy* akibat ukuran set pengujian yang sangat kecil dan karenanya tidak dijadikan dasar analisis utama. Keempat, purwarupa sistem ditujukan sebagai bukti kelaikan penerapan dan belum dioptimasi dari sisi waktu inferensi maupun ketahanan terhadap video di luar distribusi pelatihan.

### 4.2.6 Ringkasan Jawaban atas Rumusan Masalah

Berdasarkan seluruh pembahasan di atas, ketiga rumusan masalah penelitian dapat dijawab secara ringkas. Pemetaan jawaban beserta bukti pendukungnya dirangkum pada Tabel 4.6.

**Tabel 4.6 Ringkasan Jawaban atas Rumusan Masalah**

| Rumusan Masalah | Temuan | Bukti |
|---|---|---|
| RM1 — penurunan performa spasial lintas dataset | Terjadi penurunan substansial; AUC turun ke 0,629–0,648 dan *recall* runtuh hingga 0,083 (terparah pada arah CDF→FFPP) | Tabel 4.3, Tabel 4.4 |
| RM2 — pengaruh FFT terhadap penurunan | Memperkecil *generalization drop* pada arah FFPP→CDF (Δ hybrid +0,027 vs spasial +0,116), tetapi tidak konsisten dan tanpa peningkatan AUC menyeluruh, serta mengorbankan performa in-dataset | Tabel 4.3, Tabel 4.4 |
| RM3 — kontribusi spasial vs frekuensi | Spasial penyumbang utama (AUC s.d. 0,969); frekuensi nyaris acak (0,55–0,59) sehingga fusi *hybrid* tidak mengungguli spasial murni | Tabel 4.2, Gambar 4.4 |

Secara keseluruhan, penelitian ini menyimpulkan bahwa dalam konfigurasi yang diuji, arsitektur *hybrid* XceptionNet–FFT tidak mengungguli *baseline* spasial murni pada evaluasi *in-dataset*, dan manfaat domain frekuensi terhadap generalisasi lintas dataset hanya bersifat parsial serta bergantung arah. Temuan negatif ini, beserta analisis akar penyebabnya, merupakan kontribusi ilmiah yang sah dan menjadi dasar bagi rekomendasi perbaikan yang diuraikan pada BAB V.
