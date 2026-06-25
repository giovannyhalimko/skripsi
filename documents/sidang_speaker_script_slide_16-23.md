# Naskah Presentasi Sidang — Slide 16–23

> **Cara pakai:** ini naskah hampir kata-per-kata untuk dibaca/dihafal. Teks dalam *[kurung siku miring]* adalah arahan panggung (bukan untuk diucapkan). Estimasi total blok ini **±7–8 menit**. Angka memakai koma desimal agar sama dengan tampilan slide.
>
> Tiap slide berisi: **Cue** (catatan singkat yang sudah ada di deck) → **Naskah** (yang diucapkan). Kalau mau, isi `notes:` di source deck bisa diganti dengan ringkasan Cue, dan naskah ini dipegang terpisah.

---

## Slide 16 — In-Dataset *(Hasil 1 / 3)*

**Cue:** Temuan pertama sudah jelas: menambahkan frekuensi tidak menaikkan performa in-dataset.

**Naskah** *(±50 dtk)*

"Kita masuk ke hasil. Mulai dari skenario **in-dataset** — model dilatih dan diuji pada dataset yang sama. *[tunjuk grafik batang in-dataset]* Ada tiga temuan di sini.

Pertama, model **spasial konsisten paling unggul**. AUC-nya mencapai sekitar **nol koma sembilan tujuh** — pada Celeb-DF tepatnya nol koma sembilan tujuh satu, sementara pada FaceForensics lebih rendah, sekitar nol koma tujuh delapan. Artinya, dari piksel saja, XceptionNet sudah sangat baik membedakan asli dan palsu.

Kedua, dan ini penting — cabang **frekuensi nyaris setara tebakan acak**. AUC-nya hanya sekitar nol koma lima enam di kedua dataset; pada Celeb-DF tepatnya nol koma lima enam dua. Nol koma lima itu praktis seperti melempar koin.

Ketiga, karena frekuensi tidak membawa informasi diskriminatif, model **hybrid pun tidak mengungguli spasial** — di semua tier sampel yang andal, dan di kedua dataset.

Jadi temuan pertama sudah jelas: pada kondisi in-dataset, menambahkan frekuensi tidak menaikkan performa."

---

## Slide 17 — Cross-Dataset & Generalization Drop *(Hasil 2 / 3)*

**Cue:** Frekuensi hanya menahan penurunan pada satu arah, dan itu pun dengan mengorbankan performa in-dataset.

**Naskah** *(±60 dtk)*

"Sekarang skenario yang lebih menantang dan lebih realistis: **cross-dataset**. Model dilatih di satu dataset, lalu diuji di dataset yang berbeda — meniru kondisi nyata saat detektor bertemu deepfake dari sumber yang belum pernah dilihat. *[tunjuk grafik cross-dataset]*

Temuan pertama: **semua model menurun**. AUC jatuh ke kisaran **nol koma lima enam sampai nol koma enam delapan**. Ini tepat menjawab kekhawatiran utama kami soal generalisasi.

Yang paling mencolok adalah **recall collapse** — terutama pada arah **Celeb-DF ke FaceForensics**. Recall-nya hanya sekitar **nol koma nol tujuh**. Artinya model hampir gagal total menangkap sampel palsu di domain baru.

Soal frekuensi: di sini manfaatnya **mulai terlihat, tapi parsial dan bergantung arah**. Pada arah FaceForensics ke Celeb-DF, penurunan F1 model hybrid hanya **plus nol koma nol satu dua**, jauh lebih kecil dibanding spasial yang turun **plus nol koma nol sembilan satu** — jadi hybrid lebih tahan. Tetapi keunggulan ini **tidak konsisten** pada arah sebaliknya.

Kesimpulannya: frekuensi hanya menahan penurunan pada satu arah, dan itu pun dengan mengorbankan performa in-dataset tadi."

---

## Slide 18 — Ukuran Sampel & Dinamika Pelatihan *(Hasil 3 / 3)*

**Cue:** Cabang frekuensi bukan kurang optimal di akhir, ia memang tidak pernah belajar.

**Naskah** *(±55 dtk)*

"Temuan ketiga menjawab satu kemungkinan keberatan: apakah cabang frekuensi mungkin hanya **kekurangan data**? *[tunjuk kurva AUC vs ukuran sampel]*

Kami memvariasikan ukuran sampel. Tren AUC model **spasial naik stabil** seiring bertambahnya data — perilaku belajar yang sehat. Sebaliknya, cabang **frekuensi tetap datar** di sekitar level acak di **seluruh tier** — dari sampel kecil sampai besar.

Lebih dari itu, **kurva pelatihannya stagnan sejak awal**. Ini bukan kasus overfitting atau kurang epoch — modelnya memang tidak pernah menemukan pola diskriminatif untuk dipelajari.

Dan **confusion matrix** pada skenario cross-dataset **menegaskan keruntuhan recall** yang tadi kita lihat.

Jadi intinya: cabang frekuensi bukan kurang optimal di tahap akhir — **ia memang tidak pernah belajar**. Ini yang mengantar kita ke pembahasan berikutnya: mengapa?"

---

## Slide 19 — Mengapa Cabang Frekuensi Gagal *(Pembahasan 1 / 2)* — **SLIDE INTI PERTAHANAN**

**Cue:** Ini slide inti pertahanan. Kuasai keempatnya.

**Naskah** *(±75 dtk — pelan, percaya diri)*

"Ini bagian terpenting dari pembahasan kami. Kami **tidak berhenti pada 'frekuensi gagal'** — kami menjelaskan **mengapa**, dan kami menemukan empat penyebab yang saling menguatkan.

**Pertama, artefak frekuensinya rusak oleh praproses.** Crop wajah dengan MTCNN dan kompresi video c23 sama-sama menekan komponen frekuensi tinggi — padahal justru di situlah artefak deepfake biasanya berada. Ini sejalan dengan temuan **Mejri**.

**Kedua, kami membuang informasi fase.** Kami hanya memakai magnitudo FFT, padahal **fase** justru membawa informasi struktur citra. **Oppenheim dan Lim** menunjukkan ini, dan metode seperti **SPSL** dari Liu memanfaatkan fase secara eksplisit.

**Ketiga, ada bias arsitektur.** CNN cenderung belajar tekstur dan frekuensi rendah lebih dulu — ini didokumentasikan oleh **Geirhos, Rahaman, dan Wang**. Jadi sinyal frekuensi tinggi yang lemah memang sulit ditangkap.

**Keempat, representasi kami terlalu sederhana** — satu peta FFT mentah dimasukkan ke CNN yang dangkal. Tidak cukup ekspresif untuk mengekstraksi pola yang halus.

Empat hal inilah yang menjelaskan kegagalan tersebut secara menyeluruh — dan masing-masing nanti menjadi dasar saran perbaikan kami."

---

## Slide 20 — Posisi terhadap Literatur & Hipotesis *(Pembahasan 2 / 2)*

**Cue:** Kami melengkapi literatur dengan menandai kapan frekuensi gagal membantu.

**Naskah** *(±55 dtk)*

"Lalu, bagaimana posisi temuan kami terhadap literatur yang justru memuji domain frekuensi?

Kami menegaskan: ini **bukan kontradiksi, melainkan kondisi batas** — *boundary condition*. Artefak frekuensi memang **tetap ada**, sebagaimana ditunjukkan **Durall dan Zhang**. Yang kami tunjukkan adalah bahwa **mengeksploitasinya bersifat kondisional** — tergantung representasi, skema fusi, dan tingkat kesulitan pengujian.

Penelitian-penelitian yang berhasil umumnya memakai **representasi dan fusi frekuensi yang jauh lebih canggih**, dan menguji pada *cross-manipulation* yang lebih ringan — bukan *cross-dataset* yang seketat pengujian kami.

Soal hipotesis: berdasarkan bukti kami, **H0 tidak dapat ditolak**. Selisih antar-model kami bahas secara **deskriptif** menggunakan tiga seed, tanpa mengklaim signifikansi statistik yang tidak kami uji.

Jadi kami tidak menyangkal literatur — kami **melengkapinya**, dengan menandai secara tepat kapan frekuensi gagal membantu."

---

## Slide 21 — Purwarupa *(Demo)*

**Cue:** Tunjukkan Gambar 4.1 & 4.2 (atau demo live bila diizinkan).

**Naskah** *(±55 dtk)*

"Untuk membuat temuan ini konkret, kami membangun sebuah **purwarupa**. *[tunjuk Gambar 4.1 — antarmuka demo]*

Ini aplikasi **Gradio** yang kami hosting di **Hugging Face Spaces**. Pengguna mengunggah gambar, dan ketiga model — spasial, frekuensi, dan hybrid — memberikan **verdict berdampingan**, sehingga perbedaannya langsung terlihat.

Yang menarik adalah panel **'what the models see'**. *[tunjuk Gambar 4.2]* Di sebelah kiri, **wajah** yang dilihat cabang spasial. Di sebelah kanan, **spektrum FFT** yang dilihat cabang frekuensi.

Dan di sinilah bukti kualitatifnya: **spektrum FFT untuk wajah asli dan palsu nyaris tidak terbedakan** oleh mata. Ini secara visual menjelaskan mengapa cabang frekuensi kesulitan — sinyalnya memang nyaris tidak ada pada kondisi pengujian kami.

*[Opsional, jika diizinkan penguji: "Bila berkenan, saya bisa menjalankan demo-nya secara langsung sebentar."]*"

---

## Slide 22 — Kesimpulan

**Cue:** Secara keseluruhan, pada konfigurasi yang diuji, kontribusi domain frekuensi terbatas dan generalisasi lintas dataset tetap menjadi tantangan terbuka.

**Naskah** *(±60 dtk)*

"Mari kita rangkum, menjawab langsung ketiga rumusan masalah.

**Rumusan Masalah 1** — sejauh mana detektor spasial menurun lintas dataset? Jawabannya: **menurun secara substansial**. Terjadi *recall collapse*, paling parah pada arah Celeb-DF ke FaceForensics.

**Rumusan Masalah 2** — apakah penambahan FFT membantu? Penambahan FFT **hanya menekan penurunan secara parsial dan bergantung arah** — dan itu pun dengan mengorbankan performa in-dataset. Jadi bukan solusi yang konsisten.

**Rumusan Masalah 3** — domain mana yang berkontribusi? **Domain spasial adalah penyumbang utama.** Cabang frekuensi mendekati acak, sehingga **model hybrid tidak mengungguli model spasial murni**.

Secara keseluruhan, pada konfigurasi yang kami uji, kontribusi domain frekuensi **terbatas**, dan generalisasi lintas dataset **tetap menjadi tantangan terbuka**."

---

## Slide 23 — Saran

**Cue:** Sambungkan tiap saran ke akar penyebab di Slide 19.

**Naskah** *(±60 dtk)*

"Dari empat akar penyebab di slide pembahasan tadi, kami menurunkan saran yang **konkret** — bukan sekadar daftar umum.

**Pertama, perkuat cabang frekuensi:** sertakan informasi **fase** — misalnya pendekatan SPSL; hitung **FFT pada frame penuh**, bukan hanya crop wajah; dan lakukan **analisis multi-skala**. Ini langsung menjawab penyebab pertama dan kedua.

**Kedua, fusi yang lebih baik:** gunakan **regularisasi atau atensi dua-domain**, dan lakukan **pretraining** pada cabang frekuensi. Ini menjawab bias arsitektur.

**Ketiga, eksplorasi domain transformasi alternatif** seperti **DCT atau wavelet**, yang representasinya bisa lebih kaya daripada FFT mentah.

**Keempat, untuk memperkuat validitas dan cakupan:** adaptasi domain secara eksplisit untuk masalah generalisasi, **uji signifikansi statistik** untuk klaim yang lebih kuat, **pemodelan temporal** antar-frame, serta **memperbanyak data pelatihan dan variasi tingkat kompresi** — yang berada di luar batasan penelitian ini.

Dan satu catatan praktis: untuk kebutuhan penerapan saat ini, **baseline spasial XceptionNet tetap menjadi pilihan paling andal** — peningkatan generalisasi lintas dataset masih memerlukan penelitian lanjutan.

Jadi setiap saran tersambung langsung ke akar penyebab yang sudah kami identifikasi."

---

*[Transisi ke Slide 24 — Penutup: "Demikian, dan sebagai penutup…"]*
