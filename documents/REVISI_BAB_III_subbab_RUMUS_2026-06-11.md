# REVISI BAB III — Sub-bab yang Perlu Diubah (Penghapusan RUMUS, Hanya Perhitungan)

> **Cara pakai:** tiap blok = **satu sub-bab utuh** hasil revisi sesuai komentar dosen ("BAB III tanpa rumus, hanya perhitungan"). Definisi rumus telah **dihapus** dan diganti rujukan ke BAB II; **contoh perhitungan angka tetap dipertahankan**. Ganti seluruh sub-bab lama di Word dengan versi ini.
>
> **Penomoran persamaan:** karena banyak rumus dihapus, nomor (3.x) akan bergeser. Persamaan **perhitungan** yang dipertahankan saya beri label sementara `(3-hitung-…)`. Setelah semua sub-bab final, **nomori ulang berurutan**. Bagian `「DIHAPUS」` menandai rumus yang dipindah ke BAB II — jangan ditulis lagi di BAB III.
>
> Notasi rumus ditulis linear; tuliskan ulang di Word Equation Editor.

---

## 🟥 BAB III · Sub-bab "Konversi Domain Frekuensi (FFT)"
**Hapus rumus:** 3.1 (grayscale), 3.2 (DFT), 3.3 (magnitude), 3.4 (high-pass), 3.5 (log), 3.10 (z-score). **Pertahankan:** contoh perhitungan FFT 2D (eks-3.6 s/d 3.9), Tabel 3.4 & 3.5.

---

Konversi domain frekuensi merupakan inti kontribusi penelitian ini. Proses ini mengubah setiap frame citra RGB menjadi representasi peta magnitude frekuensi menggunakan Fast Fourier Transform (FFT) 2 dimensi. Representasi frekuensi ini menangkap artefak spektral yang dihasilkan oleh proses sintesis deepfake, seperti checkerboard artifacts dari operasi upsampling pada GAN (Odena et al., 2016), distorsi distribusi spektral (Durall et al., 2020), dan ketidakkontinyuan pada batas blending (Zhang et al., 2019). Seluruh dasar matematis transformasi ini — konversi grayscale, DFT 2D, magnitude spectrum, Gaussian high-pass filter, log scaling, dan normalisasi z-score — telah diuraikan pada BAB II sub-bab Fast Fourier Transform (FFT); pada bagian ini transformasi tersebut diterapkan secara berurutan pada data penelitian.

**a. Konversi RGB ke Grayscale.** Setiap frame hasil cropping (berukuran 224×224) terlebih dahulu dikonversi menjadi satu kanal grayscale menggunakan standar ITU-R BT.601 (lihat persamaan konversi grayscale pada BAB II). Konversi ke satu kanal cukup untuk analisis frekuensi karena informasi luminansi telah merepresentasikan distribusi intensitas spasial yang diperlukan untuk mendeteksi artefak spektral.

「DIHAPUS — rumus 3.1 dipindah ke BAB II」

**b. Transformasi Fourier 2D.** Citra grayscale ditransformasi ke domain frekuensi menggunakan Discrete Fourier Transform (DFT) 2 dimensi (lihat persamaan DFT 2D pada BAB II), dengan M = N = 224. Setelah transformasi, dilakukan operasi FFT shift yang memindahkan komponen frekuensi nol (DC component) dari sudut matriks ke posisi tengah, sehingga frekuensi rendah terletak di tengah peta dan frekuensi tinggi di tepi.

「DIHAPUS — rumus 3.2 dipindah ke BAB II」

**c. Magnitude Spectrum, High-Pass Filtering, dan Log Scaling.** Dari hasil DFT yang berupa bilangan kompleks dihitung magnitude spectrum (lihat persamaan magnitude pada BAB II). Sebelum transformasi logaritmik, magnitude dilewatkan melalui Gaussian high-pass filter (lihat persamaan high-pass pada BAB II) untuk menekan dominasi komponen frekuensi rendah, dengan cutoff fraction β = 0,15 sehingga radius penekanan σ = β·N ≈ 33,6 piksel. Magnitude terfilter F'(u,v) = F(u,v)·H(u,v) kemudian dikompresi rentang dinamisnya melalui transformasi logaritmik log(1 + |F'(u,v)|) (lihat persamaan log scaling pada BAB II). Fungsi log1p dipilih karena menghindari log(0) dan mengompresi rentang dinamis sehingga detail frekuensi tinggi tidak tertutupi dominasi komponen DC. Hasil akhir berupa matriks float32 berukuran 224×224 dengan nilai tipikal pada rentang [0, ~16] yang disimpan sebagai berkas .npy dalam cache FFT.

「DIHAPUS — rumus 3.3, 3.4, 3.5 dipindah ke BAB II」

**d. Contoh Perhitungan FFT 2D.** Sebagai ilustrasi, berikut perhitungan FFT 2D pada matriks grayscale berukuran 4×4. Misalkan matriks piksel f(x,y) adalah:

*Tabel 3.4 Contoh Matriks Grayscale 4×4* — (tetap seperti versi lama)

| | y=0 | y=1 | y=2 | y=3 |
|---|---|---|---|---|
| x=0 | 100 | 120 | 100 | 120 |
| x=1 | 80 | 100 | 80 | 100 |
| x=2 | 100 | 120 | 100 | 120 |
| x=3 | 80 | 100 | 80 | 100 |

**Menghitung F(0,0)** (komponen DC):

>   F(0,0) = Σ_{x=0}^{3} Σ_{y=0}^{3} f(x,y) · e^{-j·2π·0}     (3-hitung-1)
>   F(0,0) = (100+120+100+120) + (80+100+80+100) + (100+120+100+120) + (80+100+80+100)
>   F(0,0) = 440 + 360 + 440 + 360 = 1600

Komponen DC merepresentasikan rata-rata intensitas keseluruhan citra, yaitu 1600/16 = 100.

**Menghitung F(0,1)** (frekuensi horizontal pertama):

>   F(0,1) = Σ_{x=0}^{3} Σ_{y=0}^{3} f(x,y) · e^{-j·2π·y/4}     (3-hitung-2)

Karena e^{-j·2π·y/4} menghasilkan faktor {1, −j, −1, j} untuk y = 0,1,2,3:
- Baris x=0: 100(1) + 120(−j) + 100(−1) + 120(j) = 0 + (−120j) + 120j = 0
- Baris x=1: 80(1) + 100(−j) + 80(−1) + 100(j) = 0 + (−100j) + 100j = 0
- Baris x=2: → 0
- Baris x=3: → 0

Sehingga F(0,1) = 0. Hal ini menunjukkan pola frekuensi horizontal pada matriks ini simetris.

**Menghitung F(1,0)** (frekuensi vertikal pertama):

>   F(1,0) = Σ_{x=0}^{3} Σ_{y=0}^{3} f(x,y) · e^{-j·2π·x/4}     (3-hitung-3)

Faktor e^{-j·2π·x/4} menghasilkan {1, −j, −1, j} untuk x = 0,1,2,3:
- x=0: (100+120+100+120)·1 = 440
- x=1: (80+100+80+100)·(−j) = −360j
- x=2: (100+120+100+120)·(−1) = −440
- x=3: (80+100+80+100)·(j) = 360j

F(1,0) = 440 − 360j − 440 + 360j = 0

**Menghitung F(1,1):**

>   F(1,1) = Σ_{x=0}^{3} Σ_{y=0}^{3} f(x,y) · e^{-j·2π·(x+y)/4}     (3-hitung-4)

*(Tabel faktor gabungan e^{-j·2π·(x+y)/4} per (x,y) — tetap seperti versi lama.)*
- Penjumlahan bagian real: 100−100−100+100−100+100−100+100 = 0
- Penjumlahan bagian imajiner: −120−80+80+120+120−120+80−80 = 0

F(1,1) = 0 + 0j = 0

Matriks ini memiliki pola repetitif sempurna sehingga energi terkonsentrasi pada komponen DC. Pada citra wajah sesungguhnya, distribusi energi lebih tersebar dan perbedaan antara citra real dan fake terlihat dari pola distribusi frekuensi tinggi yang anomal.

**e. Magnitude dan Log Scaling.**

*Tabel 3.5 Contoh Perhitungan Magnitude dan Log Scaling* — (tetap)

| Komponen | F(u,v) | \|F(u,v)\| | log(1+\|F(u,v)\|) |
|---|---|---|---|
| F(0,0) | 1600 | 1600 | 7,378 |
| F(0,1) | 0 | 0 | 0 |
| F(1,0) | 0 | 0 | 0 |
| F(1,1) | 0 | 0 | 0 |

Pada citra deepfake sesungguhnya, komponen frekuensi tinggi menunjukkan pola anomali yang khas, seperti spectral rolloff yang tidak wajar (Durall et al., 2020) atau puncak periodik akibat checkerboard artifacts dari operasi transposed convolution pada GAN (Odena et al., 2016).

**f. Normalisasi FFT.** Setelah seluruh frame dikonversi ke peta magnitude dan disimpan dalam cache, dihitung statistik normalisasi per dataset menggunakan z-score (lihat persamaan normalisasi z-score pada BAB II). Nilai μ dan σ adalah rata-rata dan simpangan baku global dari seluruh piksel cache FFT dataset tersebut, dihitung pada sampel acak hingga 5.000 berkas menggunakan akumulasi satu lintasan (sum & sum-of-squares). Hasil disimpan dalam berkas fft_stats.json yang dimuat otomatis saat pelatihan. Normalisasi per dataset penting karena setiap dataset memiliki karakteristik spektral berbeda akibat perbedaan kamera, resolusi, dan kompresi.

「DIHAPUS — rumus 3.10 dipindah ke BAB II」

---

## 🟥 BAB III · Sub-bab "Augmentasi Data"
**Hapus rumus:** 3.11 (noise Gaussian), 3.12/3.13 (band masking). **Pertahankan:** seluruh deskripsi pipeline augmentasi spasial & frekuensi sebagai konfigurasi yang diterapkan (nilai parameter tetap ditulis sebagai perhitungan/konfigurasi).

---

Augmentasi data merupakan teknik regularisasi yang diterapkan selama pelatihan untuk meningkatkan keberagaman data tanpa menambah jumlah sampel asli. Konsep dan rumus augmentasi domain frekuensi (injeksi noise Gaussian dan spectral band masking) telah diuraikan pada BAB II sub-bab Augmentasi Data. Pada penelitian ini, strategi augmentasi dirancang terpisah untuk domain spasial dan frekuensi karena karakteristik kedua representasi berbeda secara fundamental, dan pada mode hybrid konsistensi augmentasi antar kedua cabang dijaga untuk mempertahankan korespondensi spasial–frekuensi.

**a. Augmentasi Domain Spasial.** Augmentasi pada citra RGB selama pelatihan terdiri dari:
- **Resize** ke 256×256 piksel (lebih besar dari ukuran input final).
- **RandomResizedCrop** ke 224×224 dengan skala 80%–100%, mensimulasikan variasi zoom dan posisi wajah.
- **ColorJitter**: kecerahan (±0,2), kontras (±0,2), saturasi (±0,1), hue (±0,05), mensimulasikan variasi pencahayaan dan karakteristik sensor.
- **RandomHorizontalFlip** dengan probabilitas 50%, memanfaatkan simetri bilateral wajah.
- **ToTensor**: konversi ke tensor dengan rentang [0, 1].
- **Normalize** menggunakan statistik ImageNet: mean = [0,485; 0,456; 0,406], std = [0,229; 0,224; 0,225].
- **RandomErasing** (probabilitas 10%, skala 2%–15% dari luas citra), mendorong model tidak bergantung pada satu wilayah wajah.

Pada validasi dan pengujian, augmentasi acak tidak diterapkan; citra hanya di-resize ke 224×224, dikonversi ke tensor, dan dinormalisasi.

*Gambar 3.4 Tahapan augmentasi visual pada cabang spasial (RGB)* — (tetap)

**b. Augmentasi Domain Frekuensi.** Operasi spasial seperti random crop atau rotasi tidak sesuai untuk peta magnitude FFT karena merusak lokalisasi frekuensi. Oleh karena itu diterapkan dua mekanisme augmentasi frekuensi sesuai rumus pada BAB II:
- **Injeksi noise Gaussian** dengan σ = 0,05 (parameter fft_noise_sigma), diterapkan setelah normalisasi z-score dan hanya selama pelatihan. Tujuannya menyimulasikan variasi noise sensor/kompresi dan mencegah penghafalan peta FFT yang dimuat dari cache statis.
- **Spectral band masking** dengan probabilitas 5%: sebuah pita horizontal atau vertikal selebar acak 1 hingga ⌊H/16⌋ piksel diisi nilai nol, dengan orientasi dipilih 50:50. Teknik ini mencegah model bergantung pada satu pita frekuensi spesifik.

「DIHAPUS — rumus 3.11, 3.12, 3.13 dipindah ke BAB II」

*Gambar 3.5 Contoh Penerapan Spectral Band Masking pada Peta Magnitude FFT* — (tetap)

**c. Konsistensi Augmentasi pada Mode Hybrid.** Pada mode hybrid, pembalikan horizontal pada citra RGB tanpa pembalikan yang sama pada peta FFT akan merusak korespondensi spasial–frekuensi (karena DFT(flip(x)) = flip(DFT(x)), sebagaimana dibahas pada BAB II). Oleh karena itu pembalikan horizontal diterapkan secara manual setelah kedua input dimuat, dengan keputusan acak identik (probabilitas 50%) pada tensor RGB dan FFT; opsi RandomHorizontalFlip pada pipeline spasial dinonaktifkan (include_hflip=False) agar pembalikan terkontrol terpadu.

*Gambar 3.6 Perbandingan Peta Magnitude FFT: Frame Real vs Fake* — (tetap)

---

## 🟥 BAB III · Sub-bab "Model Frekuensi FreqCNN"
**Hapus rumus:** 3.19 (residual block), 3.22 (BatchNorm). **Pertahankan:** Tabel 3.6 arsitektur, dan contoh perhitungan forward pass (eks-3.20, 3.21).

---

Model frekuensi dirancang untuk mengekstraksi dan menganalisis artefak pada domain frekuensi yang tidak terdeteksi oleh model spasial. Berbeda dengan XceptionNet yang memproses citra RGB, FreqCNN memproses peta magnitude FFT yang merepresentasikan distribusi energi frekuensi. Arsitektur ini dibangun ringan namun mampu menangkap pola spektral khas citra deepfake.

**a. Arsitektur Konvolusional.** FreqCNN adalah jaringan konvolusional ringan untuk peta magnitude FFT satu kanal, terdiri dari blok-blok konvolusional residual bertingkat (FreqBlock). Setiap FreqBlock mengimplementasikan koneksi residual yang terinspirasi dari ResNet (He et al., 2015) dengan dua jalur paralel:
- **Jalur utama:** Conv2d(3×3, padding=1) → BatchNorm2d → ReLU.
- **Jalur pintasan (shortcut):** konvolusi 1×1 untuk menyesuaikan dimensi kanal, atau operasi identitas bila dimensi sudah sama.

Kedua jalur dijumlahkan secara elemen (residual addition) sebelum max pooling stride 2, mengikuti rumus blok residual dan batch normalization yang telah didefinisikan pada BAB II sub-bab CNN. Koneksi residual mencegah degradasi gradien pada jaringan yang lebih dalam dan memungkinkan setiap blok mempelajari representasi tambahan di atas representasi yang sudah ada.

「DIHAPUS — rumus 3.19 (residual block) dan 3.22 (BatchNorm) dipindah ke BAB II」

*Gambar 3.9 Arsitektur FreqBlock dengan Koneksi Residual* — (tetap)

Konfigurasi yang digunakan adalah depth = 5 dengan base_channels = 64, menghasilkan progresi kanal [64, 128, 256, 512, 512]. Dua blok terakhir menggunakan jumlah kanal sama (512), dengan jalur pintasan pada blok kelima berupa identitas. Pemilihan base_channels = 64 (bukan default 32) dilatarbelakangi karakteristik input crop wajah dengan distribusi spektral relatif kaya.

*Tabel 3.6 Arsitektur Layer-by-Layer FreqCNN (depth=5, base_channels=64)* — (tetap, lihat versi lama)

Meskipun jumlah parameter FreqCNN (~4,2 juta) lebih besar dari konfigurasi default depth=3, base_channels=32 (~130.000), model ini tetap jauh lebih kecil dari XceptionNet (~22,8 juta). Kedalaman 5 blok dipilih untuk mengekstraksi fitur frekuensi yang lebih kaya, dan koneksi residual memastikan pelatihan tetap stabil. Kedalaman dapat dikonfigurasi melalui parameter freq_depth dan freq_base_channels; jumlah kanal berlipat dua tiap blok hingga batas 8×base_channels = 512.

**b. Contoh Perhitungan Forward Pass.** Berikut contoh forward pass pada satu blok konvolusional dengan input sederhana 4×4 satu kanal.

Input (peta magnitude FFT tersederhanakan):

>   X₁ = [[2,1  3,5  1,2  4,0],
>         [0,8  2,3  3,1  1,5],
>         [4,2  1,0  2,7  3,3],
>         [1,6  3,8  0,5  2,9]]     (3-hitung-5)

Konvolusi dengan kernel 3×3 (misalkan bobot W, bias b=0), padding=1. Posisi (0,0) dengan zero padding:

>   z(0,0) = 0·w00 + 0·w01 + 0·w02
>          + 0·w10 + 2,1·w11 + 3,5·w12
>          + 0·w20 + 0,8·w21 + 2,3·w22     (3-hitung-6)

Setelah seluruh posisi dihitung, batch normalization menormalisasi output (sesuai rumus BatchNorm pada BAB II), dengan ϵ = 10⁻⁵. Selanjutnya ReLU(z) = max(0, z) mengubah nilai negatif menjadi nol, dan MaxPool2d(2) mengambil nilai maksimum pada tiap grid 2×2 sehingga output 4×4 menjadi peta fitur 2×2.

---

## 🟥 BAB III · Sub-bab "Model Hybrid HybridTwoBranch (Late Fusion)"
**Hapus rumus:** 3.23/3.24 (proyeksi), 3.25/3.26 (SE gating). **Pertahankan:** Tabel 3.7/3.8 dan contoh perhitungan late fusion (eks-3.27, 3.28, 3.29 + langkah klasifikasi).

---

Model hybrid merupakan kontribusi utama penelitian ini. Arsitektur HybridTwoBranch menggabungkan fitur domain spasial dan frekuensi melalui mekanisme late fusion: kedua cabang mengekstraksi fitur secara independen, lalu fitur digabungkan dan diproses bersama untuk klasifikasi akhir.

**a. Cabang Spasial (XceptionNet Backbone).** Menggunakan XceptionNet (num_classes=0) sebagai feature extractor tanpa lapisan klasifikasi. Input citra RGB (3, 224, 224) ternormalisasi ImageNet menghasilkan vektor fitur berdimensi 2.048.

**b. Cabang Frekuensi (FreqCNN Backbone).** Menggunakan backbone FreqCNN (blok konvolusional + global average pooling) tanpa lapisan klasifikasi. Input peta magnitude FFT (1, 224, 224) ternormalisasi z-score menghasilkan vektor fitur berdimensi 512.

**c. Projection Layers dan Penyeimbangan Dimensi.** Tantangan utama late fusion adalah ketidakseimbangan dimensi: cabang spasial 2.048 vs frekuensi 512 (rasio 4:1). Bila langsung dikonkatenasi, fitur spasial akan mendominasi. Untuk mengatasinya, kedua cabang diproyeksikan ke dimensi sama (PROJ_DIM = 256) melalui lapisan proyeksi (linear + BatchNorm + ReLU, sesuai rumus proyeksi fitur pada BAB II), dengan matriks bobot W_s ∈ ℝ^{256×2048} dan W_f ∈ ℝ^{256×512}. Setelah proyeksi, kedua cabang berdimensi sama (256) dan dapat digabungkan secara seimbang.

「DIHAPUS — rumus 3.23, 3.24 dipindah ke BAB II」

**d. Squeeze-and-Excitation (SE) Gating.** Setelah konkatenasi (h_fused = [h_spatial ; h_freq] ∈ ℝ^{512}), diterapkan SE gating (Hu et al., 2018) yang mempelajari bobot kepentingan per dimensi fitur secara adaptif, mengikuti rumus SE gating dan penskalaan yang telah didefinisikan pada BAB II sub-bab Squeeze-and-Excitation Networks. SE gate terdiri dari: **Squeeze** (kompresi 512→128 via linear + ReLU), **Excitation** (ekspansi 128→512 via linear + sigmoid menghasilkan gate pada [0,1]), dan **pengalian elemen** antara vektor fusi dengan bobot gerbang (W₁ ∈ ℝ^{128×512}, W₂ ∈ ℝ^{512×128}). Mekanisme ini menekan fitur tidak informatif dan memperkuat fitur diskriminatif dari kedua cabang.

「DIHAPUS — rumus 3.25, 3.26 dipindah/diduplikasi dari BAB II (Persamaan SE 2.11 & 2.12)」

**e. Classifier Head.** Vektor h_fused ∈ ℝ^{512} diteruskan ke kepala klasifikasi: Dropout(0,5) → Linear(512→128) → ReLU → Dropout(0,5) → Linear(128→1). Output logit diproses BCEWithLogitsLoss yang menerapkan sigmoid secara internal.

**f. Contoh Perhitungan Late Fusion.** Contoh disederhanakan dengan dimensi kecil.

Fitur input (4 dimensi per cabang):

>   f_spatial = [0,2 ; 1,2 ; −0,3 ; 0,5] ,  f_freq = [0,4 ; −0,1 ; 0,7 ; 0,2]     (3-hitung-7)

Proyeksi (4→4, disederhanakan, W_s & W_f = identitas, tanpa BN):
- h_spatial = ReLU(f_spatial) = [0,8 ; 1,2 ; 0 ; 0,5]
- h_freq = ReLU(f_freq) = [0,4 ; 0 ; 0,7 ; 0,2]

Konkatenasi:

>   h_fused = [0,8 ; 1,2 ; 0 ; 0,5 ; 0,4 ; 0 ; 0,7 ; 0,2] ∈ ℝ^{8}     (3-hitung-8)

SE Gating (8→2→8, reduction=4):
- Squeeze: s = ReLU(W₁·h_fused), misalkan s = [1,5 ; 0,8]
- Excitation: g = σ(W₂·s), misalkan g = [0,9 ; 0,7 ; 0,3 ; 0,8 ; 0,6 ; 0,2 ; 0,9 ; 0,5]
- Gating:

>   h_fused = h_fused ⊙ g = [0,72 ; 0,84 ; 0 ; 0,40 ; 0,24 ; 0 ; 0,63 ; 0,10]     (3-hitung-9)

Terlihat SE gate menekan dimensi ke-3 dan ke-6 (gate rendah: 0,3 dan 0,2) sambil mempertahankan dimensi ke-1 dan ke-7 (gate tinggi: 0,9). Mekanisme ini secara adaptif memilih fitur paling diskriminatif dari kedua cabang.

Klasifikasi: logit z = wᵀ·h_fused + b, misalkan z = 2,1, sehingga probabilitas p = σ(2,1) = 1/(1+e^{−2,1}) = 0,891. Karena p > 0,5 ⇒ prediksi fake (label 1).

*(Tabel 3.7 Perbandingan Tiga Arsitektur Model dan Tabel 3.8 Dimensi Fitur per Komponen — tetap seperti versi lama.)*

---

## 🟥 BAB III · Sub-bab "Fungsi Loss, BCEWithLogitsLoss dengan Label Smoothing"
**Hapus rumus:** 3.30 (BCE), 3.31 (pos_weight), 3.32 (label smoothing). **Pertahankan:** contoh perhitungan BCEWithLogitsLoss (eks-3.33, 3.34, 3.35).

---

Fungsi loss yang digunakan adalah Binary Cross-Entropy with Logits (BCEWithLogitsLoss), yang menggabungkan fungsi sigmoid dan binary cross-entropy dalam satu operasi yang stabil secara numerik (rumus BCEWithLogitsLoss telah didefinisikan pada BAB II). Untuk menangani ketidakseimbangan kelas diterapkan penyeimbangan kelas (pos_weight), dan untuk regularisasi diterapkan label smoothing; kedua rumus tersebut juga telah diuraikan pada BAB II sub-bab Binary Cross-Entropy sebagai Fungsi Loss.

「DIHAPUS — rumus 3.30, 3.31, 3.32 dipindah ke BAB II」

**a. Penyeimbangan Kelas (pos_weight).** Bobot pos_weight = n_neg/n_pos dikalikan pada komponen loss untuk sampel positif sehingga kelas minoritas mendapat pengaruh lebih besar. Apabila dataset seimbang (n_neg = n_pos), maka pos_weight = 1 dan loss menjadi BCEWithLogitsLoss standar.

**b. Label Smoothing.** Dengan α = 0,02, transformasi label mengubah 0 → 0,01 dan 1 → 0,99 sehingga model tidak perlu mendorong logit ke nilai ekstrem. Pada konfigurasi akhir eksperimen, label smoothing diaktifkan dengan α = 0,05 sebagai regularisasi ringan untuk mencegah overconfidence pada dataset berukuran kecil (mulai n = 100).

**c. Contoh Perhitungan BCEWithLogitsLoss.** Contoh dengan label smoothing α = 0,05 (nilai pada konfigurasi akhir), untuk satu sampel dengan logit z = 2,5, label asli y = 1 (fake), dan pos_weight = 1.

Label smoothing:

>   y' = 1·(1 − α) + α·0,5 = 1·(1 − 0,05) + 0,05·0,5 = 0,975     (3-hitung-10)

Sigmoid:

>   σ(2,5) = 1 / (1 + e^{−2,5}) = 1 / (1 + 0,0821) = 1 / 1,0821 = 0,924     (3-hitung-11)

Loss (menggunakan bentuk per-sampel dari BCE pada BAB II):

>   L = −[ y'·ln σ + (1 − y')·ln(1 − σ) ]     (3-hitung-12)
>     = −[ 0,975·(−0,0790) + 0,025·(−2,577) ]
>     = −[ (−0,0770) + (−0,0644) ]
>     = −(−0,1415) = 0,1415

Nilai loss yang rendah (0,1415) menunjukkan prediksi model (probabilitas 0,924 untuk fake) sudah mendekati label target ter-smooth (0,975). Pada awal pelatihan, nilai loss umumnya jauh lebih tinggi dan menurun seiring konvergensi.

> *Catatan: bila dosen menghendaki BAB III benar-benar tanpa bentuk simbolik, baris (3-hitung-12) boleh dihapus dan langsung ditulis substitusi angkanya saja.*

---

## 🟥 BAB III · Sub-bab "Gradient Clipping"
**Hapus rumus:** 3.36. **Pertahankan:** penjelasan nilai ambang sebagai konfigurasi.

---

Untuk mencegah ledakan gradien (gradient explosion), diterapkan gradient clipping berdasarkan norma L2 dengan batas max_norm = 5,0 (rumus gradient clipping telah didefinisikan pada BAB II sub-bab Optimasi Model). Ambang 5,0 dipilih untuk mengakomodasi learning rate yang lebih tinggi (2 × 10⁻⁴) sambil tetap mencegah ledakan gradien, terutama pada epoch ke-4 ketika backbone XceptionNet dilepaskan (unfreezing) dan aliran gradien dari seluruh jaringan secara tiba-tiba meningkatkan norma gradien. Pada implementasi mixed precision (AMP), scaler.unscale_() dipanggil sebelum clipping agar gradien berada pada skala aslinya.

「DIHAPUS — rumus 3.36 dipindah ke BAB II」

---

## 🟥 BAB III · Sub-bab "Evaluasi Cross-Dataset" (di bawah Desain Eksperimen)
**Hapus rumus:** 3.37. **Pertahankan:** deskripsi skenario evaluasi silang.

---

Evaluasi cross-dataset mengukur kemampuan generalisasi model pada dataset yang berbeda dari dataset pelatihan:
- Model dilatih pada FFPP, lalu dievaluasi pada set pengujian CDF.
- Model dilatih pada CDF, lalu dievaluasi pada set pengujian FFPP.

Evaluasi silang ini penting karena dalam skenario nyata detektor deepfake harus mengenali manipulasi dari metode yang belum pernah dilihat selama pelatihan. Perbedaan performa antara evaluasi in-dataset dan cross-dataset diukur melalui metrik generalization drop (Δ), yang rumusnya telah didefinisikan pada BAB II sub-bab Cross Dataset Generalization. Nilai Δ yang besar menunjukkan model terlalu bergantung pada pola spesifik dataset pelatihan dan generalisasinya buruk.

「DIHAPUS — rumus 3.37 dipindah ke BAB II」

---

## 🟥 BAB III · Sub-bab "Generalization Drop" (di bawah Metode Evaluasi Model)
**Hapus rumus:** 3.38 (duplikat 3.37). **Catatan:** sub-bab ini hampir seluruhnya merupakan pengulangan definisi 3.37. Pertimbangkan **menggabungkannya** dengan sub-bab "Evaluasi Cross-Dataset" agar tidak redundan. Versi minimal tanpa rumus:

---

Metrik generalization drop mengukur degradasi performa model ketika dievaluasi pada dataset yang berbeda dari dataset pelatihan, yaitu selisih F1-Score in-dataset terhadap cross-dataset (lihat rumus generalization drop pada BAB II). Nilai Δ yang mendekati nol menunjukkan generalisasi yang baik — model mampu mendeteksi deepfake dari metode yang belum pernah dilihat. Nilai Δ yang besar menunjukkan model menghafal pola spesifik dataset pelatihan. Contoh perhitungan Δ disajikan bersama contoh perhitungan metrik pada sub-bab berikut.

「DIHAPUS — rumus 3.38 dipindah ke BAB II」

---

### Ringkasan tindakan BAB III
| Sub-bab | Rumus dihapus | Perhitungan dipertahankan |
|---|---|---|
| Konversi Domain Frekuensi (FFT) | 3.1, 3.2, 3.3, 3.4, 3.5, 3.10 | 3.6–3.9 (FFT), Tabel 3.4/3.5 |
| Augmentasi Data | 3.11, 3.12, 3.13 | konfigurasi parameter |
| Model Frekuensi FreqCNN | 3.19, 3.22 | 3.20, 3.21 (forward pass) |
| Model Hybrid | 3.23, 3.24, 3.25, 3.26 | 3.27, 3.28, 3.29 + klasifikasi |
| Fungsi Loss | 3.30, 3.31, 3.32 | 3.33, 3.34, 3.35 |
| Gradient Clipping | 3.36 | — |
| Evaluasi Cross-Dataset | 3.37 | — |
| Generalization Drop | 3.38 | (gabungkan; contoh di Tabel 3.13/3.14) |

**Tidak diubah** (sudah berupa perhitungan): Model Spasial XceptionNet (3.14–3.18), Contoh Perhitungan Metrik (Tabel 3.13/3.14), Differential Learning Rate & Penjadwalan Learning Rate (hanya angka, bukan rumus).
