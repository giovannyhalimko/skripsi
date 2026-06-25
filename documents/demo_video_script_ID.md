# Naskah Presentasi Video Demo

**Target durasi:** ~10 menit (sudah termasuk pembuka & penutup)
**Format:** rekaman layar (screen recording) aplikasi demo Gradio + suara narasi (voiceover).
**Catatan tempo:** narasi di bawah ini ~1.400 kata ≈ 10 menit pada kecepatan santai 140 kata/menit. Tanda `[LAYAR: …]` menunjukkan apa yang ditampilkan; teks biasa adalah yang diucapkan. Penanda waktu bersifat target kumulatif, bukan potongan kaku.

---

## 0 · Pembuka — siapa, apa, mengapa (0:00 – 1:00)

> `[LAYAR: slide judul atau halaman awal demo, sebelum mengunggah apa pun.]`

Halo, kami **[nama anggota kelompok]**, dan ini adalah penjelasan singkat (walkthrough) dari aplikasi demo interaktif yang kami bangun untuk skripsi kami tentang **deteksi deepfake**.

Skripsi ini mengajukan satu pertanyaan: jika kita mengambil sebuah detektor berbasis citra yang sudah kuat, lalu *menambahkan* cabang domain frekuensi ke dalamnya, apakah model gabungan atau "hybrid" tersebut benar-benar mendeteksi deepfake dengan lebih baik? Demo ini adalah cara kami membuat pertanyaan itu — beserta jawabannya — menjadi sesuatu yang bisa *dilihat*, bukan sekadar dibaca dalam tabel hasil.

Cara kerjanya sederhana: Anda mengunggah sebuah video wajah singkat, lalu aplikasi menjalankan **tiga model berbeda** pada frame yang sama persis, kemudian menampilkan keputusan masing-masing secara berdampingan. Dalam beberapa menit ke depan, kami akan mengunggah satu klip, menjelaskan apa yang terjadi di balik layar, dan menerangkan arti dari setiap bagian di layar.

---

## 1 · Tiga model yang dibandingkan (1:00 – 2:00)

> `[LAYAR: gulir ke tabel kecil di bagian atas halaman — Spatial / Hybrid / Frequency.]`

Sebelum mengunggah apa pun, mari kami kenalkan ketiga modelnya, karena keseluruhan demo ini adalah perbandingan di antara ketiganya.

Yang pertama adalah **model Spatial — XceptionNet**. Model ini melihat piksel RGB mentah dari wajah, tidak lebih. Ini adalah **baseline** atau acuan kami: sebuah jaringan konvolusi yang sudah mapan untuk deteksi deepfake.

Yang kedua adalah **model Hybrid — inilah usulan dari skripsi kami**. Model ini mengambil citra RGB yang sama *dan* sebuah peta domain frekuensi dari citra tersebut, lalu menggabungkan keduanya. Idenya adalah bahwa generator deepfake meninggalkan jejak artefak yang halus dan berulang, yang lebih mudah dikenali di domain frekuensi dibandingkan di pikselnya.

Yang ketiga adalah **model Frequency-only** atau hanya-frekuensi. Model ini *hanya* melihat peta frekuensi — sama sekali tanpa piksel. Model ini hadir sebagai pembanding, agar kita bisa tahu seberapa besar kontribusi masing-masing cabang secara terpisah.

Hal yang penting: ketiganya dilatih pada **dataset yang sama** — FaceForensics++, dengan jumlah sampel yang sama, dan seed acak yang sama. Jadi, perbedaan keputusan apa pun di antara ketiga model murni berasal dari *arsitekturnya*, bukan karena salah satu model kebetulan mendapat sesi pelatihan yang lebih beruntung.

---

## 2 · Mengunggah klip & alur pemrosesan (2:00 – 4:00)

> `[LAYAR: klik kotak unggah, pilih video wajah singkat, lalu klik "Analyze".]`

Kami akan mengunggah sebuah klip video wajah singkat. Kami klik **Analyze**.

Selagi diproses, izinkan kami menjelaskan apa yang sedang terjadi di balik layar, karena bagian ini penting demi perbandingan yang adil. Aplikasi tidak langsung menyuapkan video mentah ke model — melainkan menjalankan **prapemrosesan yang sama persis seperti saat model dilatih**.

> `[LAYAR: selagi berjalan, Anda bisa menampilkan diagram pipeline dari DOCUMENTATION.md, atau cukup biarkan demo di layar.]`

Ada empat langkah. **Pertama**, aplikasi mengambil cuplikan frame dari video sebanyak **5 frame per detik**, dengan batas maksimum **16 frame** — batas ini menjaga agar aplikasi tetap responsif, sebab semuanya berjalan di CPU gratis, tanpa GPU.

**Kedua**, pada setiap frame yang diambil, aplikasi menjalankan **detektor wajah (MTCNN)** dan memotong (crop) tepat pada area wajah dengan sedikit margin. Ini penting: model dilatih pada wajah yang sudah dipotong, jadi jika kita menyuapkan seluruh frame — latar belakang, rambut, bahu — model akan melihat sesuatu yang tidak pernah dipelajarinya.

**Ketiga**, setiap wajah hasil potong diubah menjadi **dua jenis masukan** yang dibutuhkan model: citra RGB ternormalisasi untuk cabang spatial, dan sebuah **peta frekuensi** — yaitu transformasi Fourier dari wajah tersebut, dengan filter high-pass yang menekan konten frekuensi rendah yang dominan dan mempertahankan detail halus tempat artefak deepfake biasanya berada.

**Keempat**, setiap model menghasilkan *probabilitas-palsu untuk setiap frame*, lalu aplikasi **merata-ratakan** nilai-nilai itu menjadi satu skor tingkat-video. Jadi, keputusan yang akan Anda lihat adalah konsensus dari seluruh frame yang diambil, bukan dari satu frame yang kebetulan beruntung.

---

## 3 · Membaca kartu keputusan (4:00 – 6:00)

> `[LAYAR: tiga kartu hasil kini terlihat. Tunjuk salah satu kartu.]`

Inilah hasilnya — satu kartu untuk setiap model. Mari kami jelaskan satu kartu dulu, baru kita bandingkan.

Setiap kartu punya tiga bagian. Di bagian atas, ada **lencana (badge)**: hijau untuk ASLI (REAL), merah untuk PALSU (FAKE). Di bawahnya, ada **batang keyakinan (confidence bar)** — bagian berwarna yang terisi adalah probabilitas-palsu rata-rata dari model, dari 0 di sisi kiri hingga 100% di sisi kanan. Lalu ada **garis penanda vertikal kecil** pada batang itu — itulah **ambang keputusan (decision threshold)** model tersebut.

Ambang itu penting, dan nilainya bukan sekadar 0,5. Untuk setiap model, kami menyetel ambang ini pada **data validasi terpisah** — data yang tidak pernah dilatihkan ke model — untuk menemukan titik potong yang paling baik memisahkan asli dan palsu. Jadi ambang spatial berada di sekitar 0,13, hybrid di sekitar 0,23, dan frequency di sekitar 0,45. Aturannya sederhana: **jika batang terisi melewati garis penanda, keputusannya adalah PALSU.** Menampilkan probabilitas mentah *sekaligus* ambangnya membuat kita bisa membaca bukan hanya keputusannya, tetapi juga seberapa *yakin* dan seberapa *dekat ke garis batas* setiap model.

> `[LAYAR: kini arahkan ke ketiga kartu sekaligus.]`

Sekarang, perbandingannya. Lihat ketiga kartu bersamaan untuk klip yang sama. Anda akan sering melihatnya **berbeda pendapat** — dan ketidaksepakatan itulah inti dari demo ini. Baseline spatial cenderung paling yakin dan paling tepat; sementara model hybrid dan frequency lebih ragu-ragu, dan kadang keliru.

---

## 4 · "Apa yang dilihat oleh model" (6:00 – 7:30)

> `[LAYAR: gulir ke bawah ke dua galeri — "Face crops" dan "FFT spectra".]`

Panel ini membuat masukan yang abstrak menjadi konkret. Inilah frame-frame yang sebenarnya dianalisis oleh model.

Di **sebelah kiri** ada **potongan wajah (face crops)** — citra RGB. Inilah yang secara harfiah dilihat oleh model *spatial*: hanya wajah, yang sudah diubah ukurannya.

Di **sebelah kanan** ada **spektrum frekuensi** — peta Fourier, yang diberi warna agar terlihat oleh mata manusia. Inilah yang dilihat oleh model *frequency* dan *hybrid*. Bagian terang di tengah adalah struktur kasar dari wajah; pola-pola yang menyebar ke arah tepi adalah detail frekuensi tinggi yang halus. Secara teori, generator deepfake meninggalkan pola-pola samar dan teratur di area tepi ini — seperti kisi atau pola berulang — yang tidak akan ada pada citra kamera asli.

> `[LAYAR: tahan tampilan pada salah satu gambar spektrum.]`

Dan di sinilah temuan yang jujur mulai terlihat. Ketika kita mengamati spektrum ini dengan mata — dan keputusan model frequency mengonfirmasinya — artefak-artefak itu ternyata **halus dan tidak konsisten**. Sinyal frekuensi memang tidak seandal sinyal piksel untuk dataset ini.

---

## 5 · Temuan utama (7:30 – 9:00)

> `[LAYAR: kembali ke tiga kartu keputusan, semuanya terlihat.]`

Jadi, inilah kesimpulan yang ingin disampaikan demo ini — dan ini adalah sebuah **hasil negatif**, yang menurut kami justru jenis hasil yang jujur dan menarik.

Menambahkan cabang frekuensi ternyata **tidak** meningkatkan deteksi. Dari keseluruhan eksperimen kami, **baseline spatial yang sederhana justru berkinerja paling baik** — sekitar 0,78 pada metrik AUC (area di bawah kurva). Model **hybrid**, yang merupakan usulan kami, justru berada **lebih rendah**, sekitar 0,65. Dan model **frequency-only** adalah yang paling lemah, sekitar 0,57 — nyaris setara menebak.

Dengan kata lain: tambahan kompleksitas dari menggabungkan cabang frekuensi ke model citra yang sudah kuat tidak memberi keuntungan — malah *merugikan*. Artefak frekuensi yang menurut literatur seharusnya membantu, ternyata tidak cukup kuat atau konsisten di data ini untuk menambah nilai, dan cabang tambahan itu justru lebih banyak menambahkan derau (noise).

Demo ini memungkinkan penguji untuk **membuktikan temuan tersebut sendiri** — unggah sebuah klip, lalu saksikan model hybrid yang "lebih canggih" justru kalah dari baseline yang sederhana, berulang kali. Ini jauh lebih meyakinkan daripada meminta seseorang mempercayai sebuah angka di dalam tabel.

> `[LAYAR: tampilkan sebentar teks peringatan (caveat) di bagian bawah halaman.]`

Satu catatan penting yang adil, dan ditampilkan langsung di halaman: model-model ini hanya dilatih pada wajah dari FaceForensics++. Klip dari sumber yang sama sekali berbeda berada di luar distribusi data (out-of-distribution) dan keputusannya bisa jadi tidak andal. Ini adalah **demo penelitian yang menyertai sebuah skripsi — bukan detektor untuk penggunaan produksi.**

---

## 6 · Penutup (9:00 – 10:00)

> `[LAYAR: kembali ke halaman demo lengkap, atau slide penutup.]`

Sebagai rangkuman: demo ini menjalankan tiga detektor deepfake — sebuah baseline spatial, model hybrid usulan kami, dan model hanya-frekuensi — pada video yang sama yang diunggah, dengan mencerminkan alur pelatihan yang sama persis, lalu menampilkan keputusan masing-masing secara berdampingan beserta masukan yang dilihat setiap model.

Dan apa yang ditunjukkannya adalah temuan inti skripsi ini, yang dibuat dapat dilihat dan dapat diuji ulang: **model hybrid yang diusulkan tidak mengungguli baseline spatial yang sederhana.** Kadang, hasil paling berharga dalam penelitian justru yang mengatakan "ide ini, setelah diuji dengan cermat, ternyata tidak berhasil" — dan kini siapa pun bisa melihat persis mengapa demikian.

Terima kasih telah menyaksikan.

---

### Tips perekaman
- **Siapkan klip lebih dahulu.** Inferensi di CPU untuk 16 frame × 3 model butuh beberapa detik — siapkan video uji Anda dan pertimbangkan untuk memotong jeda "Analyze" saat menyunting, atau bicara selama menunggu (naskah pada §2 sudah dirancang untuk ini).
- **Siapkan dua klip jika memungkinkan** — idealnya satu klip di mana baseline benar dan hybrid berbeda pendapat, agar poin pada §5 terlihat jelas di layar.
- **Perbesar tampilan browser** ke ~125% agar kartu dan garis penanda ambang terbaca jelas di video.
- Jika waktu mepet, §1 dan §4 paling bisa dipadatkan; §3 (membaca kartu) dan §5 (temuan) adalah bagian yang wajib dipertahankan.
