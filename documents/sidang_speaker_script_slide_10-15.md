# Naskah Presentasi Sidang — Slide 10–15 *(Metodologi)*

> **Cara pakai:** naskah hampir kata-per-kata untuk dibaca/dihafal. Teks dalam *[kurung siku miring]* adalah arahan panggung (bukan untuk diucapkan). Estimasi total blok ini **±6 menit**. Angka memakai koma desimal agar sama dengan tampilan slide.
>
> Tiap slide berisi: **Cue** (catatan singkat yang sudah ada di deck) → **Naskah** (yang diucapkan).

---

## Slide 10 — Alur Penelitian *(Metodologi)*

**Cue:** Jelaskan perjalanan satu video dari awal sampai jadi keputusan. Tekankan split per-video untuk mencegah kebocoran.

**Naskah** *(±55 dtk)*

"Sekarang kita masuk ke **metodologi**. Slide ini menunjukkan alur penelitian secara utuh — perjalanan satu video dari awal hingga menjadi sebuah keputusan. *[tunjuk diagram alur]*

Kita mulai dari **video**. Dari tiap video kita **cuplik frame pada lima FPS**. Setiap frame lalu dideteksi wajahnya dan **di-crop dengan MTCNN** ke ukuran **224 kali 224** piksel.

Dari frame wajah ini kita bentuk **dua representasi**: citra **RGB** untuk cabang spasial, dan **peta FFT** untuk cabang frekuensi.

Lalu data dibagi train, validation, dan test dengan rasio **70 / 15 / 15**. Dan ini penting — pembagiannya **per-video, bukan per-frame**. Artinya frame dari satu video tidak boleh tersebar di train dan test sekaligus. Ini **mencegah kebocoran data** yang bisa membuat hasil terlihat lebih bagus dari yang sebenarnya.

Dari sini kita latih **tiga model** — spasial, frekuensi, dan hybrid — dan kita evaluasi pada **dua skenario**, in-dataset dan cross-dataset, masing-masing dengan **tiga seed**."

---

## Slide 11 — Dataset *(Metodologi)*

**Cue:** Dua dataset ini memungkinkan kami menguji generalisasi pada generator dan kondisi rekaman berbeda (kedua dataset memakai subset seimbang 375/375 = 750 video, sesuai Tabel 3.1).

**Naskah** *(±55 dtk)*

"Kami memakai **dua dataset benchmark**. *[tunjuk tabel]*

Yang pertama, **FaceForensics++** — kami singkat FFPP. Kami pakai **subset seimbang 750 video**, 375 asli dan 375 palsu, dengan **empat metode manipulasi**, pada tingkat kompresi c23.

Yang kedua, **Celeb-DF versi dua** — CDF. Berisi **750 video**, 375 asli dan 375 palsu, dengan satu metode manipulasi tetapi **kualitas yang tinggi**.

Dua catatan penting. Pertama, kedua dataset kami pakai sebagai **subset seimbang 375 / 375** (750 video), dibagi **per video** 70/15/15 tanpa kebocoran. *[Bila ditanya: benchmark FFPP penuh jauh lebih besar — 1.000 video asli plus empat metode manipulasi — dan Celeb-DF v2 publik tidak seimbang (590 real / 5.639 fake), tetapi kami sengaja mengambil subset seimbang 375 / 375 untuk tiap dataset, sesuai Tabel 3.1, supaya perbandingannya adil dan tidak berat sebelah.]*

Kedua, kami melakukan **evaluasi cross-dataset**: model dilatih di satu dataset lalu diuji di dataset lain — **kedua arah**, FFPP ke CDF dan CDF ke FFPP. Inilah inti pengujian generalisasi kami."

---

## Slide 12 — Preprocessing *(Metodologi)*

**Cue:** Tekankan baris terakhir (hanya magnitudo, fase tidak dipakai) — ini relevan ke pembahasan kegagalan frekuensi di Slide 19.

**Naskah** *(±55 dtk)*

"Slide ini merinci tahap **preprocessing**. *[tunjuk gambar spektrum FFT real vs fake]*

Pertama, **ekstraksi frame** pada lima FPS, maksimal lima puluh frame per video.

Kedua, **deteksi dan crop wajah** dengan MTCNN, margin nol koma tiga, lalu di-resize ke 224 kali 224.

Ketiga, pembentukan **peta FFT**. Urutannya: frame diubah ke grayscale, dilakukan FFT dua dimensi, lalu *fftshift* untuk memusatkan frekuensi rendah, diambil **magnitudo**-nya, diberi *high-pass*, di-*log*, dan terakhir dinormalisasi dengan *z-score*.

Dan satu hal yang ingin saya tekankan — ini akan relevan nanti di pembahasan: kami **hanya memakai magnitudo**. Informasi **fase tidak kami pakai**. Keputusan desain ini kelak menjadi salah satu penjelasan mengapa cabang frekuensi gagal."

---

## Slide 13 — Arsitektur Tiga Model *(Metodologi)*

**Cue:** Ketiga model berbagi komponen yang sama supaya perbandingannya adil dan kami bisa mengisolasi kontribusi tiap domain.

**Naskah** *(±65 dtk)*

"Ini **arsitektur** dari ketiga model yang kami bandingkan. *[tunjuk diagram dua cabang]*

Model pertama, **Spatial**. Murni cabang spasial: citra RGB masuk ke **XceptionNet**, langsung menghasilkan logit. Sekitar **22,8 juta** parameter.

Model kedua, **Freq**. Murni cabang frekuensi: peta FFT masuk ke **FreqCNN** — sebuah CNN dengan lima blok residual — menghasilkan logit. Jauh lebih ringan, sekitar **4,2 juta** parameter.

Model ketiga, **Hybrid**. Ini menggabungkan keduanya dengan **late fusion**. Fitur dari XceptionNet diproyeksikan ke 256 dimensi, fitur dari FreqCNN juga 256 dimensi; keduanya **digabung menjadi 512 dimensi**, melewati **SE gate** untuk pembobotan, lalu masuk ke klasifikasi.

Kuncinya: **ketiga model berbagi komponen yang sama**. Dengan begitu perbandingannya adil, dan kami bisa **mengisolasi kontribusi tiap domain** secara bersih.

*[Opsional, sebagai jembatan ke hasil: angka kecil di tiap kartu adalah pratinjau hasil — sudah terlihat di sini bahwa cabang frekuensi mendekati acak.]*"

---

## Slide 14 — Strategi Pelatihan *(Metodologi)*

**Cue:** Lewati cepat, ini bukti rigor. Siapkan detail jika ditanya.

**Naskah** *(±50 dtk — tempo cepat)*

"Strategi pelatihan saya **lewati cepat** — ini lebih ke bukti rigor, dan saya siap merinci bila Bapak/Ibu penguji ingin. *[tunjuk kurva learning rate]*

Singkatnya: loss **BCEWithLogitsLoss** dengan *label smoothing* nol koma nol lima. Optimizer **AdamW** dengan *learning rate* dua kali sepuluh pangkat minus empat, memakai *differential learning rate*. Backbone kami **bekukan tiga epoch pertama** lalu di-unfreeze, dengan *warmup* tiga epoch dilanjutkan *cosine decay*.

Kami juga pakai *mixed precision*, *gradient accumulation*, dan *gradient clipping* untuk stabilitas.

Dan yang penting untuk reproduktibilitas: **model terbaik dipilih berdasarkan AUC validasi**, dengan *early stopping*, dan semuanya diulang pada **tiga seed**."

---

## Slide 15 — Desain Eksperimen *(Metodologi)*

**Cue:** Total kombinasi ini membuat perbandingan kami terkontrol dan dapat direproduksi.

**Naskah** *(±55 dtk)*

"Terakhir di metodologi, **desain eksperimen** — bagaimana semua faktor ini dikombinasikan. *[tunjuk tabel]*

Ada lima dimensi: **tiga model** — spasial, frekuensi, hybrid; **dua dataset** — FFPP dan CDF; **empat ukuran sampel** — seratus, dua ratus lima puluh, lima ratus, dan tujuh ratus lima puluh; **tiga seed**; dan **dua skenario evaluasi** — in-dataset dan cross-dataset.

Untuk metrik, kami laporkan *accuracy*, *precision*, *recall*, dan F1, dengan **AUC sebagai metrik utama** — karena AUC tidak bergantung pada pemilihan ambang.

Soal ambang, kami evaluasi pada dua titik: ambang standar **nol koma lima**, dan ambang optimal lewat **Youden J**.

Total kombinasi inilah yang membuat perbandingan kami **terkontrol penuh dan dapat direproduksi**. Dengan fondasi metodologi ini, mari kita lihat hasilnya."

---

*[Transisi ke Slide 16 — Hasil 1 / 3: "Kita mulai dari skenario in-dataset…"]*
