# REVISI BAB II — Sub-bab yang Perlu Diubah (Penambahan RUMUS dari BAB III)

> **Cara pakai:** tiap blok di bawah adalah **satu sub-bab utuh** yang sudah direvisi. Bagian yang **baru ditambahkan** (rumus pindahan dari BAB III) ditandai dengan **「TAMBAHAN」 … 「/TAMBAHAN」** supaya mudah dilihat saat review; sisanya = teks lama yang dipertahankan. Saat menempel ke Word, ganti seluruh sub-bab lama dengan versi ini.
>
> **Catatan penomoran:** rumus baru saya beri label sementara seperti `(2-baru-a)`. Setelah semua disisipkan, **nomori ulang berurutan** mengikuti posisi di dokumen (atau gunakan auto-caption Word). Di BAB III, rujukan ke rumus ini cukup ditulis dengan nama (mis. "persamaan konversi grayscale pada BAB II") agar tidak rapuh terhadap penggeseran nomor.
>
> **Notasi rumus:** ditulis linear agar jelas; tuliskan ulang di Word Equation Editor sesuai format thesis.

---

## 🟦 BAB II · Sub-bab "Fast Fourier Transform (FFT)" (di bawah Preprocessing)
**Aksi:** sub-bab ini sudah memuat Persamaan DFT (2.13), magnitude (2.14), log (2.15), fftshift (2.16). Tambahkan **tiga rumus pindahan** dari BAB III: konversi grayscale (eks-3.1), Gaussian high-pass filter (eks-3.4), dan normalisasi z-score (eks-3.10). Berikut sub-bab utuh hasil revisi.

---

Fast Fourier Transform (FFT) merupakan algoritma efisien untuk menghitung Discrete Fourier Transform (DFT), yaitu proses yang mengubah citra dari domain spasial menjadi domain frekuensi. Transformasi ini memungkinkan analisis distribusi energi frekuensi pada citra sehingga pola-pola artefak halus yang tidak terlihat pada domain spasial dapat teridentifikasi. Pada penelitian deteksi deepfake, FFT menjadi komponen penting karena manipulasi berbasis GAN cenderung menimbulkan ketidakwajaran sinyal frekuensi, terutama pada rentang high-frequency akibat proses upsampling, konvolusi, dan operasi blending (Durall et al., 2020; Qian et al., 2020; Hasanaath et al., 2023).

Dalam konteks deteksi, informasi frekuensi menjadi sangat berharga karena generator GAN secara matematis tidak mampu mempertahankan natural image statistics sehingga meninggalkan spectral fingerprint yang khas dan konsisten.

**「TAMBAHAN」**
Sebelum transformasi Fourier diterapkan, citra RGB terlebih dahulu dikonversi menjadi citra satu kanal (grayscale), karena analisis frekuensi cukup dilakukan pada informasi luminansi yang merepresentasikan distribusi intensitas spasial. Konversi menggunakan standar ITU-R BT.601:

>   Y = 0,299·R + 0,587·G + 0,114·B     (2-baru-a)

di mana Y adalah nilai luminansi, sedangkan R, G, dan B adalah nilai kanal warna merah, hijau, dan biru. Bobot yang berbeda pada setiap kanal mencerminkan sensitivitas mata manusia terhadap masing-masing warna.
**「/TAMBAHAN」**

Secara matematis, DFT dua dimensi untuk citra berukuran M×N didefinisikan sebagai:

>   F(u,v) = Σ_{x=0}^{M-1} Σ_{y=0}^{N-1} f(x,y) · e^{-j·2π( u·x/M + v·y/N )}     (2.13)

dengan:
- f(x,y) adalah intensitas piksel pada koordinat (x,y),
- F(u,v) adalah representasi frekuensi pada koordinat (u,v),
- j = √(-1) adalah bilangan imajiner.

Besarnya energi frekuensi (magnitude spectrum) dihitung melalui:

>   |F(u,v)| = √( Re[F(u,v)]² + Im[F(u,v)]² )     (2.14)

**「TAMBAHAN」**
Pada citra wajah, energi frekuensi sangat terkonsentrasi pada komponen DC dan frekuensi rendah yang merepresentasikan struktur global wajah (bentuk, pencahayaan) dan kurang informatif untuk deteksi deepfake. Sebaliknya, artefak sintesis seperti checkerboard pattern dan spectral rolloff yang anomal terutama muncul pada frekuensi menengah dan tinggi. Oleh karena itu magnitude spectrum dapat dilewatkan melalui Gaussian high-pass filter untuk menekan dominasi komponen frekuensi rendah:

>   H(u,v) = 1 − exp( − [ (u−u_c)² + (v−v_c)² ] / [ 2·(β·N)² ] )     (2-baru-b)

di mana (u_c, v_c) adalah koordinat pusat peta frekuensi setelah fftshift, N adalah dimensi peta, dan β adalah cutoff fraction yang mengontrol radius penekanan (σ = β·N). Magnitude terfilter diperoleh dari F'(u,v) = F(u,v) · H(u,v).
**「/TAMBAHAN」**

Untuk memudahkan analisis, spektrum frekuensi biasanya dilakukan log compression:

>   S(u,v) = log( 1 + |F(u,v)| )     (2.15)

dengan penambahan konstanta 1 untuk menghindari log(0). Selain itu, digunakan pula frequency shifting (fftshift) sehingga komponen frekuensi rendah berada di pusat tampilan spektrum:

>   F_shift(u,v) = F( (u + M/2) mod M , (v + N/2) mod N )     (2.16)

**「TAMBAHAN」**
Karena setiap dataset memiliki karakteristik spektral yang berbeda akibat perbedaan kamera, resolusi, dan metode kompresi, peta magnitude perlu dinormalisasi sebelum digunakan oleh model. Normalisasi dilakukan dengan z-score:

>   x̂ = (x − μ) / σ     (2-baru-c)

di mana μ dan σ adalah rata-rata dan simpangan baku global yang dihitung dari seluruh piksel peta magnitude pada satu dataset. Tanpa normalisasi yang tepat, fitur frekuensi antar dataset akan memiliki skala yang tidak sebanding.
**「/TAMBAHAN」**

Transformasi ini menghasilkan representasi frekuensi yang lebih mudah ditafsirkan dan lebih stabil untuk diproses oleh model deteksi.

Deepfake berbasis GAN menghasilkan pola-pola artefak yang tidak alami pada frekuensi tinggi akibat:
- operasi upsampling (nearest-neighbor, transposed convolution),
- ketidakstabilan filter pada generator,
- proses blending antara wajah asli dan hasil sintesis,
- kompresi video berulang kali.

Pola-pola ini sulit terdeteksi pada domain spasial namun sangat jelas pada domain frekuensi. Penelitian Durall et al. (2020) menunjukkan bahwa citra sintetis memiliki distribusi frekuensi global yang berbeda secara konsisten dibanding citra asli. Temuan tersebut diperkuat Qian et al. (2020) yang menunjukkan bahwa generator deepfake tidak mampu mereplikasi natural image statistics pada frekuensi tinggi.

*(paragraf-paragraf lanjutan sub-bab ini — mulai "Hasil transformasi FFT berupa spektrum magnitudo…" hingga "…dikombinasikan dengan model CNN berbasis spasial." — tetap seperti versi lama, tidak diubah.)*

---

## 🟦 BAB II · Sub-bab BARU "Augmentasi Data"
**Aksi:** BAB II belum punya sub-bab augmentasi. Buat **sub-bab/Heading2 baru** berjudul **"Augmentasi Data"**, letakkan **setelah** sub-bab "Preprocessing" dan **sebelum** "Optimasi Model". Memuat rumus pindahan eks-3.11 (noise Gaussian) dan eks-3.12/3.13 (spectral band masking). Berikut isi lengkapnya.

---

Augmentasi data merupakan teknik regularisasi yang memperbanyak variasi data pelatihan tanpa menambah jumlah sampel asli, sehingga membantu model menghindari overfitting dan meningkatkan generalisasi (Afchar et al., 2018; Rössler et al., 2019). Pada deteksi deepfake yang sering dilatih dengan data terbatas, augmentasi menjadi penting untuk mencegah model menghafal karakteristik spesifik video pelatihan.

Augmentasi pada **domain spasial** umumnya diterapkan langsung pada citra RGB melalui operasi geometris dan fotometrik, seperti pemotongan acak (random crop), pembalikan horizontal (horizontal flip), perubahan kecerahan/kontras/saturasi (color jitter), serta penghapusan acak sebagian area (random erasing). Operasi-operasi ini memanfaatkan invariansi alami citra wajah terhadap transformasi tersebut.

Augmentasi pada **domain frekuensi** memerlukan pendekatan yang berbeda. Operasi spasial seperti random crop atau rotasi tidak sesuai untuk peta magnitude FFT, karena setiap posisi piksel pada peta frekuensi merepresentasikan komponen frekuensi spesifik yang bergantung pada posisi absolutnya; transformasi geometris akan merusak lokalisasi frekuensi. Oleh karena itu augmentasi frekuensi dilakukan melalui dua mekanisme.

Pertama, **injeksi noise Gaussian** pada peta magnitude untuk menyimulasikan variasi noise sensor dan artefak kompresi, sekaligus mencegah penghafalan peta FFT yang identik antar-epoch:

>   x̂_fft = x_fft + ε ,    ε ~ N(0, σ²)     (2-baru-d)

di mana σ adalah intensitas noise. Noise hanya diterapkan selama pelatihan, setelah normalisasi.

Kedua, **spectral band masking**, yaitu menutup sebuah pita frekuensi (horizontal atau vertikal) selebar w piksel dengan nilai nol:

>   x̂_fft[ r₁ : r₁+w , : ] = 0     (pita horizontal)     (2-baru-e)
>   x̂_fft[ : , c₁ : c₁+w ] = 0     (pita vertikal)        (2-baru-f)

di mana w adalah lebar pita acak, sedangkan r₁ atau c₁ adalah posisi awal acak. Teknik ini mencegah model bergantung pada satu pita frekuensi spesifik dan mendorong representasi frekuensi yang lebih merata dan robust.

Pada arsitektur hybrid yang menerima input RGB dan FFT secara bersamaan, konsistensi augmentasi antar kedua cabang perlu dijaga: pembalikan horizontal pada citra RGB harus diikuti pembalikan yang sama pada peta FFT agar korespondensi spasial–frekuensi tidak rusak, karena DFT(flip(x)) = flip(DFT(x)).

---

## 🟦 BAB II · Sub-bab "Convolution Neural Network (CNN)" — tambahan Batch Normalization & Koneksi Residual
**Aksi:** sub-bab CNN sudah menyebut "residual connection" (ResNet) dan "batch normalization" tetapi tanpa rumus. Tambahkan **dua rumus generik** pindahan dari BAB III: Batch Normalization (eks-3.22) dan koneksi residual / residual block (eks-3.19). Sisipkan sebagai paragraf baru di bagian yang membahas komponen CNN (sebelum sub-Heading "Depthwise Separable Convolution"), atau buat dua paragraf pendek berikut. (Hanya cuplikan tambahan yang ditampilkan; tempel ke dalam sub-bab CNN yang sudah ada.)

---

**「TAMBAHAN — Batch Normalization」**
Untuk menstabilkan dan mempercepat pelatihan, lapisan konvolusional pada CNN modern umumnya diikuti oleh batch normalization, yang menormalisasi aktivasi setiap mini-batch lalu menskalakannya kembali melalui parameter yang dipelajari:

>   ẑᵢ = ( zᵢ − μ_B ) / √( σ_B² + ε ) · γ + β     (2-baru-g)

di mana μ_B dan σ_B² adalah rata-rata dan varians mini-batch, γ dan β adalah parameter skala dan geser yang dipelajari (learnable), dan ε adalah konstanta kecil untuk mencegah pembagian dengan nol. Batch normalization mengurangi internal covariate shift sehingga jaringan dapat dilatih dengan learning rate lebih tinggi dan lebih tahan terhadap inisialisasi bobot.
**「/TAMBAHAN」**

**「TAMBAHAN — Koneksi Residual」**
Pada jaringan yang sangat dalam, koneksi residual (residual connection) yang diperkenalkan pada ResNet (He et al., 2015) digunakan untuk mengatasi degradasi gradien. Sebuah blok residual menjumlahkan keluaran transformasi konvolusional dengan jalur pintasan (shortcut) dari input sebelum operasi berikutnya:

>   y = MaxPool₂ₓ₂( Conv₃ₓ₃(x) + Shortcut(x) )     (2-baru-h)

di mana Shortcut(x) berupa konvolusi 1×1 ketika jumlah kanal berubah, atau operasi identitas ketika dimensi sudah sesuai. Penjumlahan residual memungkinkan setiap blok mempelajari representasi tambahan di atas representasi yang sudah ada, sehingga pelatihan tetap stabil meskipun kedalaman jaringan bertambah.
**「/TAMBAHAN」**

---

## 🟦 BAB II · Sub-bab "Squeeze-and-Excitation Networks" — tambahan rumus Proyeksi Fitur
**Aksi:** SE gating sudah ada (Persamaan 2.10–2.12). Tambahkan **satu rumus proyeksi linear** (eks-3.23/3.24) yang dipakai untuk menyeimbangkan dimensi fitur sebelum fusi. Sisipkan sebagai paragraf baru di akhir sub-bab SE (atau di awal pembahasan fusi). (Cuplikan tambahan; tempel ke sub-bab SE yang sudah ada.)

---

**「TAMBAHAN — Proyeksi Fitur untuk Fusi」**
Dalam arsitektur fusi multi-domain, fitur dari cabang yang berbeda kerap memiliki dimensi yang tidak seimbang sehingga salah satu cabang dapat mendominasi. Untuk menyeimbangkannya, setiap vektor fitur diproyeksikan ke dimensi yang sama melalui lapisan linear yang diikuti batch normalization dan aktivasi ReLU:

>   h = ReLU( BN( W·f + b ) )     (2-baru-i)

di mana f adalah vektor fitur masukan, W dan b adalah bobot dan bias proyeksi, dan h adalah vektor terproyeksi berdimensi seragam. Setelah proyeksi, fitur dari kedua cabang dapat digabungkan (concatenation) secara seimbang sebelum diproses oleh mekanisme channel attention seperti SE gating.
**「/TAMBAHAN」**

---

## 🟦 BAB II · Sub-bab "Binary Cross-Entropy sebagai Fungsi Loss" — tambahan pos_weight & Label Smoothing
**Aksi:** sub-bab ini sudah memuat BCE (Persamaan 2.23). Tambahkan **dua rumus** pindahan dari BAB III: penyeimbangan kelas pos_weight (eks-3.31) dan label smoothing (eks-3.32). Berikut sub-bab utuh hasil revisi.

---

Dalam deteksi deepfake, tugas klasifikasi bersifat biner, yaitu membedakan citra asli (real) dan citra hasil manipulasi (fake). Fungsi loss yang digunakan adalah Binary Cross-Entropy with Logits (BCEWithLogitsLoss), yang menggabungkan fungsi sigmoid dan binary cross-entropy dalam satu operasi yang stabil secara numerik:

>   L = −(1/N) Σ_{i=1}^{N} [ yᵢ·log σ(zᵢ) + (1−yᵢ)·log(1−σ(zᵢ)) ]     (2.23)

di mana zᵢ adalah logit keluaran model, σ(z) adalah fungsi sigmoid, dan yᵢ ∈ {0,1} adalah label kelas (0 untuk asli, 1 untuk palsu). Fungsi loss ini memastikan bahwa model dioptimalkan untuk menghasilkan probabilitas yang akurat dalam membedakan konten asli dan palsu (Goodfellow et al., 2016).

**「TAMBAHAN — Penyeimbangan Kelas (pos_weight)」**
Apabila distribusi kelas tidak seimbang, BCEWithLogitsLoss dapat dilengkapi dengan bobot kelas positif (pos_weight) yang menambah pengaruh kelas minoritas pada pembaruan gradien:

>   w_p = n_neg / n_pos     (2-baru-j)

di mana n_neg dan n_pos adalah jumlah sampel kelas negatif (real) dan positif (fake). Bobot ini dikalikan pada komponen loss untuk sampel positif. Apabila dataset seimbang (n_neg = n_pos) maka w_p = 1 dan loss kembali menjadi BCEWithLogitsLoss standar.
**「/TAMBAHAN」**

**「TAMBAHAN — Label Smoothing」**
Label smoothing merupakan teknik regularisasi untuk mencegah model menjadi terlalu percaya diri (overconfident) dengan melunakkan label target:

>   y'ᵢ = yᵢ·(1 − α) + α·0,5     (2-baru-k)

di mana α adalah faktor smoothing. Dengan α kecil (mis. 0,02), label biner 0 dan 1 berubah menjadi 0,01 dan 0,99, sehingga model tidak perlu mendorong logit ke nilai ekstrem (±∞).
**「/TAMBAHAN」**

---

## 🟦 BAB II · Sub-bab "Optimasi Model" — tambahan Gradient Clipping
**Aksi:** tambahkan **satu rumus** gradient clipping (eks-3.36) sebagai paragraf/Heading3 baru di akhir sub-bab "Optimasi Model" (setelah pembahasan AdamW). (Cuplikan tambahan.)

---

**「TAMBAHAN — Gradient Clipping」**
Untuk mencegah ledakan gradien (gradient explosion) yang dapat membuat pelatihan tidak stabil, diterapkan gradient clipping berdasarkan norma L2. Apabila norma vektor gradien melebihi ambang c, gradien diskalakan kembali agar normanya tepat sama dengan c:

>   g ← g                  jika ‖g‖₂ ≤ c
>   g ← g · ( c / ‖g‖₂ )   jika ‖g‖₂ > c     (2-baru-l)

di mana g adalah vektor gradien dan c adalah ambang batas maksimum (max_norm). Teknik ini menjaga arah gradien tetap sama namun membatasi besarnya, sehingga pembaruan bobot tidak melonjak terutama pada tahap awal pelatihan atau saat backbone pretrained dilepaskan (unfreezing).
**「/TAMBAHAN」**

---

## 🟦 BAB II · Sub-bab "Cross Dataset Generalization" — REWRITE PENUH (integrasi rumus Generalization Drop)
**Aksi:** sub-bab lama hanya menyinggung "penurunan akurasi signifikan" tanpa menamai/mengukurnya, sehingga rumus Δ terasa menggantung bila sekadar disisipkan. Maka sub-bab ini **ditulis ulang utuh**: degradasi performa lintas dataset diberi nama eksplisit (generalization drop) lalu dikuantifikasi dengan Δ pada paragraf kedua, sehingga rumus pindahan eks-3.37/3.38 muncul secara natural. Ganti seluruh sub-bab lama dengan versi ini. (Rumus baru ditandai **「TAMBAHAN」**; sitasi memakai gaya (Nama, Tahun).)

---

Cross-dataset generalization merupakan konsep penting dalam penelitian deteksi deepfake yang menggambarkan kemampuan sebuah model untuk mempertahankan performa ketika diuji pada dataset yang berbeda dari dataset pelatihan. Konsep ini muncul sebagai respons terhadap fakta bahwa deepfake di lingkungan nyata sering kali memiliki karakteristik yang sangat berbeda dengan dataset benchmark yang umum digunakan dalam penelitian akademik. Rössler et al. (2019) menunjukkan bahwa dataset seperti FaceForensics++ hanya mencakup jenis manipulasi wajah tertentu dengan kondisi visual yang relatif seragam. Karena itu, model yang dilatih pada dataset tunggal cenderung mengalami **degradasi performa** secara signifikan ketika diuji pada dataset lain yang memiliki distribusi data berbeda.

**「TAMBAHAN — Generalization Drop」**
Degradasi performa lintas dataset tersebut dapat diukur secara kuantitatif melalui metrik **generalization drop (Δ)**, yaitu selisih antara F1-Score pada evaluasi in-dataset (dilatih dan diuji pada dataset yang sama) dengan F1-Score pada evaluasi cross-dataset (diuji pada dataset yang berbeda dari data pelatihan):

>   Δ = F1_in-dataset − F1_cross-dataset     (2-baru-m)

Nilai Δ yang mendekati nol menunjukkan generalisasi yang baik, yaitu model tetap mampu mendeteksi deepfake dari metode atau dataset yang belum pernah dilihat selama pelatihan. Sebaliknya, nilai Δ yang besar mengindikasikan bahwa model terlalu bergantung pada pola spesifik dataset pelatihan (dataset-specific artifacts) dan gagal menangkap karakteristik manipulasi yang bersifat umum. Dengan demikian, Δ menjadi indikator langsung sejauh mana sebuah arsitektur mampu menahan degradasi performa saat berpindah domain.
**「/TAMBAHAN」**

Dalam konteks deteksi deepfake, tantangan cross-dataset terutama disebabkan oleh fenomena domain shift. Domain shift terjadi ketika model menemukan pola visual atau statistik baru yang tidak muncul pada dataset pelatihan. Bentuk domain shift dapat berupa variasi kualitas video, tingkat kompresi, perangkat perekaman, kondisi pencahayaan, hingga teknik manipulasi generatif yang berbeda (Durall et al., 2020). Zhang et al. (2019) juga menegaskan bahwa setiap metode generatif berbasis GAN menghasilkan artefak sintesis yang memiliki pola distribusi berbeda, sehingga membuat model berbasis fitur spasial saja mudah terjebak pada dataset-specific artifacts.

Penelitian-penelitian modern menunjukkan bahwa pendekatan berbasis domain frekuensi cenderung memiliki kemampuan generalisasi lebih baik dibanding fitur spasial murni. Durall et al. (2020) menemukan bahwa sebagian besar model GAN gagal mereplikasi natural spectral statistics, sehingga muncul pola spektral yang konsisten pada berbagai jenis deepfake, terlepas dari dataset asal. Qian et al. (2020) memperkuat temuan tersebut dengan menunjukkan bahwa petunjuk frekuensi tinggi biasanya bersifat lebih stabil terhadap variasi domain, sehingga model yang mengeksploitasi sinyal frekuensi mampu mendeteksi manipulasi pada dataset unseen lebih baik. Hasanaath et al. (2023) juga membuktikan bahwa penggunaan fitur frekuensi eksplisit meningkatkan robustness model terhadap kompresi dan noise yang bervariasi antar dataset, yang pada gilirannya menekan nilai Δ.

Sebaliknya, pendekatan berbasis CNN murni pada domain spasial umumnya sangat sensitif terhadap distribusi tekstur dataset pelatihan. Afchar et al. (2018) dan Chollet (2017) menunjukkan bahwa CNN secara alami mempelajari pola spasial lokal yang bergantung pada tekstur permukaan, sehingga performanya dapat menurun pada dataset yang memiliki karakteristik visual berbeda. Temuan ini menjelaskan mengapa model deteksi deepfake berbasis fitur spasial sering mengalami Δ yang besar ketika menghadapi variasi kualitas video atau teknik manipulasi baru.

Oleh karena itu, dalam kajian literatur terkini, kemampuan cross-dataset generalization, yang tercermin dari kecilnya nilai generalization drop, menjadi indikator utama kualitas model deteksi deepfake modern. Penelitian seperti SpecXNet (Alam et al., 2025) dan FSBI (Hasanaath et al., 2023) menunjukkan bahwa model hybrid yang menggabungkan domain spasial dan domain frekuensi memiliki performa generalisasi lebih baik dibanding model berbasis domain tunggal. Hal ini disebabkan oleh sifat pelengkap kedua domain: domain spasial menangkap anomali tekstur dan struktur wajah, sementara domain frekuensi menangkap artefak spektral yang lebih universal antar dataset.

Secara keseluruhan, konsep cross-dataset generalization menegaskan bahwa deteksi deepfake tidak dapat bergantung pada pola dataset tertentu, tetapi harus mampu mengidentifikasi karakteristik manipulasi yang bersifat umum dan stabil. Oleh karena itu, banyak penelitian terkini mengarah pada integrasi fitur spasial dan frekuensi untuk memperoleh representasi fitur yang lebih robust terhadap perbedaan distribusi data antar dataset (Durall et al., 2020; Qian et al., 2020; Alam et al., 2025).

---

### Ringkasan rumus yang ditambahkan ke BAB II
| Label sementara | Rumus | Asal di BAB III | Sub-bab tujuan BAB II |
|---|---|---|---|
| 2-baru-a | Grayscale BT.601 | 3.1 | Fast Fourier Transform (FFT) |
| 2-baru-b | Gaussian high-pass H(u,v) | 3.4 | Fast Fourier Transform (FFT) |
| 2-baru-c | Z-score x̂=(x−μ)/σ | 3.10 | Fast Fourier Transform (FFT) |
| 2-baru-d | Noise Gaussian | 3.11 | Augmentasi Data (baru) |
| 2-baru-e/f | Spectral band masking | 3.12/3.13 | Augmentasi Data (baru) |
| 2-baru-g | Batch Normalization | 3.22 | CNN |
| 2-baru-h | Residual block | 3.19 | CNN |
| 2-baru-i | Proyeksi fitur | 3.23/3.24 | SE Networks |
| 2-baru-j | pos_weight | 3.31 | Binary Cross-Entropy |
| 2-baru-k | Label smoothing | 3.32 | Binary Cross-Entropy |
| 2-baru-l | Gradient clipping | 3.36 | Optimasi Model |
| 2-baru-m | Generalization drop | 3.37/3.38 | Cross Dataset Generalization |

**Tidak perlu ditambah (sudah ada di BAB II, di BAB III cukup dihapus):** DFT 2D (3.2≈2.13), magnitude (3.3≈2.14), log scaling (3.5≈2.15), BCE (3.30≈2.23), SE gating (3.25≈2.11), SE scaling (3.26≈2.12).
