# REVISI BAB II — Sub-bab 2.13 "Preprocessing" (ready copy-paste)

> **Cara pakai:** blok di bawah adalah **sub-bab 2.13 utuh** (termasuk 2.13.1) hasil revisi. Ganti seluruh sub-bab lama di Word dengan versi ini. Sitasi ditulis format **(Nama, Tahun)** agar mudah disisipkan berdasarkan nama — abaikan nomor IEEE lama.
>
> **Perbaikan yang sudah dimasukkan** (lihat `SIDANG_FactCheck_QA_2026-06-30.md`):
> - **Item 20** — kalimat "alur preprocessing" ditulis ulang jadi **bercabang** (RGB vs FFT) dengan urutan benar; "konversi skala warna" → "konversi ke skala keabuan (grayscale)".
> - **Item 21-1** 🔴 — klaim **temporal** (flickering / inkonsistensi ekspresi) di Ekstraksi Frame **dihapus** (bentrok dengan frame-level).
> - **Item 21-2** 🟡 — Resize: ditambah **"224×224 piksel"**; klaim "sesuai input Xception (299)" diluruskan jadi pilihan sadar 224.
> - **Item 21-3** 🟡 — **Tabel 2.4** dirombak: baris "Channel fusion → 4-channel" **dibuang**; cabang FFT (grayscale, high-pass, log, z-score) ditampilkan utuh; caption jadi **late fusion**.
>
> **Sitasi yang dipakai di sub-bab ini:** (Haq, 2021), (Afchar et al., 2018), (Chollet, 2017), (Rössler et al., 2019), (Durall et al., 2020), (Zhang et al., 2019), (Qian et al., 2020), (Hasanaath et al., 2023).

---

## 2.13  Preprocessing

Preprocessing merupakan tahap fundamental dalam sistem deteksi deepfake karena kualitas data masukan sangat memengaruhi kemampuan model dalam mengekstraksi fitur, baik pada domain spasial melalui XceptionNet maupun pada domain frekuensi melalui _Fast Fourier Transform_ (FFT). Pada penelitian deteksi deepfake modern, preprocessing tidak hanya berfungsi sebagai proses penyiapan data, tetapi juga sebagai cara untuk menghilangkan _noise_ visual, menjaga konsistensi bentuk wajah, serta menstabilkan distribusi frekuensi sebelum dilakukan transformasi (Haq, 2021; Afchar et al., 2018; Rössler et al., 2019; Durall et al., 2020; Qian et al., 2020).

Tahap preprocessing yang baik sangat diperlukan karena deepfake sering menampilkan variasi kualitas video, tingkat kompresi yang berbeda, posisi wajah yang tidak seragam, serta pola artefak yang tidak konsisten antar-_frame_. Penelitian terdahulu menunjukkan bahwa ketidakseragaman ini berdampak langsung pada performa model deteksi, terutama yang memanfaatkan sinyal frekuensi tinggi yang sensitif terhadap rotasi, translasi, dan perubahan intensitas (Durall et al., 2020; Zhang et al., 2019; Hasanaath et al., 2023).

Oleh karena itu, preprocessing pada penelitian ini dirancang untuk memastikan data masukan memiliki format yang seragam, representasi wajah yang stabil, dan struktur frekuensi yang tidak terdistorsi. Alur preprocessing terdiri atas **tahap bersama** yang kemudian **bercabang** menjadi dua representasi. Tahap bersama meliputi ekstraksi _frame_, deteksi wajah, dan _cropping_ area wajah. Setelah itu, setiap _frame_ diolah menjadi dua representasi paralel: (1) **cabang spasial** berupa citra RGB yang di-_resize_ ke 224×224 piksel lalu dinormalisasi dengan statistik ImageNet, dan (2) **cabang frekuensi** berupa citra yang dikonversi ke skala keabuan (_grayscale_), di-_resize_, ditransformasikan dengan FFT (disertai _high-pass filtering_ dan _log-magnitude_), lalu dinormalisasi dengan _z-score_. Kedua representasi diproses oleh cabang jaringan yang terpisah dan baru digabungkan di dalam model pada tahap _late fusion_, bukan sebagai kanal tambahan pada masukan XceptionNet.

### 2.13.1  Tahapan dan Alur Preprocessing

**Ekstraksi _Frame_ Video.** Video deepfake direpresentasikan sebagai rangkaian _frame_, dan setiap _frame_ berpotensi mengandung tingkat manipulasi yang berbeda. Pendekatan _frame-level_ digunakan karena artefak manipulasi tidak selalu muncul konsisten sepanjang video (Haq, 2021). Haq (2021) menunjukkan bahwa sebagian _frame_ menampilkan distorsi tekstur yang lebih jelas, sehingga pemrosesan per-_frame_ membantu model menangkap sinyal manipulasi yang penting. Pemrosesan per-_frame_ memungkinkan model mengevaluasi variasi artefak **spasial dan spektral** yang berbeda pada tiap _frame_ secara independen, tanpa bergantung pada urutan temporal antar-_frame_, sesuai dengan pendekatan _frame-level_ yang diterapkan pada penelitian ini.

**Deteksi Wajah dan _Cropping_.** Bagian wajah merupakan target utama manipulasi deepfake. Penelitian MesoNet menunjukkan bahwa kesalahan _blending_ dan _warping_ sering muncul pada tepi wajah serta area mata, hidung, dan mulut (Afchar et al., 2018). Rössler et al. (2019) melalui FaceForensics++ menegaskan bahwa latar belakang justru menjadi _noise_ apabila tidak dipotong. Dengan membatasi analisis hanya pada area wajah, jumlah fitur yang tidak relevan dapat diminimalkan sehingga model memiliki kapasitas lebih besar untuk mempelajari pola-pola manipulasi. Deteksi wajah pada penelitian ini menggunakan MTCNN dengan margin 0,3 di sekitar _bounding box_.

**_Resize_.** Citra wajah hasil _cropping_ kemudian di-_resize_ menjadi **224×224 piksel**. Penyeragaman ukuran penting untuk menjaga konsistensi pola tekstur, karena XceptionNet sensitif terhadap variasi struktur lokal (Chollet, 2017). Meskipun arsitektur XceptionNet asli dirancang untuk masukan 299×299 piksel, penelitian ini menggunakan ukuran **224×224** sebagai pilihan sadar karena merupakan ukuran standar _feature extractor_ pada banyak arsitektur visi komputer dan kompatibel dengan bobot _pretrained_ (ImageNet) yang digunakan pada tahap _transfer learning_.

**Normalisasi.** Normalisasi penting karena model CNN sangat sensitif terhadap variasi intensitas cahaya (Afchar et al., 2018). Pada cabang spasial, citra RGB dinormalisasi menggunakan statistik ImageNet (_mean_ = [0,485, 0,456, 0,406]; _std_ = [0,229, 0,224, 0,225]) agar konsisten dengan distribusi data _pretraining_. Pada cabang frekuensi, peta FFT _log-magnitude_ dinormalisasi menggunakan _z-score_ berdasarkan statistik per-dataset. Normalisasi tidak hanya meningkatkan stabilitas pelatihan, tetapi juga mempercepat konvergensi model dan mengurangi risiko _gradient explosion_ maupun _gradient vanishing_.

**Konversi _Grayscale_ dan Transformasi FFT (cabang frekuensi).** Untuk cabang frekuensi, citra wajah lebih dahulu dikonversi ke skala keabuan (_grayscale_) karena analisis frekuensi cukup dilakukan pada informasi luminansi, lalu di-_resize_ ke 224×224 piksel dan ditransformasikan ke domain frekuensi menggunakan FFT dua dimensi. Peta magnitude yang dihasilkan dilewatkan melalui _Gaussian high-pass filter_ untuk menekan dominasi komponen frekuensi rendah, kemudian dikompresi rentang dinamisnya dengan _log-magnitude_. Rincian matematis transformasi ini diuraikan pada sub-bab 2.13.2.

Tabel 2.4 merangkum keseluruhan tahapan preprocessing beserta pemisahan cabang spasial dan frekuensi.

**Tabel 2.4  Tahapan Preprocessing**

| Tahap | Operasi | Cabang | Tujuan Utama | Output |
| ----- | ------- | ------ | ------------ | ------ |
| 1 | Ekstraksi _frame_ | Bersama | Mengubah video menjadi deretan _frame_ | Citra per-_frame_ |
| 2 | Deteksi wajah (MTCNN) | Bersama | Menemukan lokasi (_bounding box_) wajah | Koordinat wajah |
| 3 | _Cropping_ (margin 0,3) | Bersama | Memotong area wajah dari latar | _Patch_ wajah |
| 4 | _Resize_ 224×224 | Spasial (RGB) | Menyeragamkan resolusi | Citra RGB 224×224 |
| 5 | Normalisasi ImageNet | Spasial (RGB) | Menstabilkan intensitas dan kontras | Citra RGB ternormalisasi |
| 6 | Konversi _grayscale_ | Frekuensi | Mengambil informasi luminansi | Citra 1-kanal |
| 7 | _Resize_ 224×224 | Frekuensi | Menyeragamkan resolusi | Citra 1-kanal 224×224 |
| 8 | Transformasi FFT (_high-pass_, _log_) | Frekuensi | Mengubah ke domain frekuensi | Peta _log-magnitude_ |
| 9 | Normalisasi _z-score_ | Frekuensi | Menyeragamkan skala spektral | Peta FFT ternormalisasi |

Tahap 1–3 bersifat bersama untuk kedua cabang. Tahap 4–5 menghasilkan representasi spasial (RGB) yang menjadi masukan XceptionNet, sedangkan tahap 6–9 menghasilkan representasi frekuensi (peta FFT _log-magnitude_) yang menjadi masukan FreqCNN. Kedua representasi diproses oleh cabang yang terpisah dan digabungkan di dalam model pada tahap _late fusion_, bukan pada tahap preprocessing dan bukan sebagai kanal tambahan.
