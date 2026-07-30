# REVISI BAB I — Latar Belakang: Uraian Studi Komparatif

**Tanggal:** 2026-07-28 (diperbarui 2026-07-29 — catatan lanjutan penguji)
**Sumber catatan:** Penguji sidang (Irpan) — Catatan 1: *"Tidak tampak uraian mengenai studi komparatif, hal-hal yang dilakukan perlu diuraikan di latar belakang."*
**Catatan lanjutan penguji (2026-07-29):** *"Masa dari awal tidak dijelaskan apa itu."* → Studi komparatif harus dijelaskan **sejak awal** Latar Belakang, bukan hanya di paragraf penutup. Maka solusi = tambah paragraf orientasi **di awal (setelah para 378)**, DAN tetap uraikan detail di para 385.
**Lokasi di dokumen live (.docx):** paragraf orientasi baru **setelah para 378** (awal), + ganti paragraf penutup **para 385** ("Penelitian ini mengisi celah tersebut…").

---

## Masalah

Judul skripsi sudah berupa **studi komparatif** ("Studi Komparatif Kinerja Deteksi Deepfake … terhadap Model Domain Tunggal"), dan desain tiga model (spasial-murni, frekuensi-murni, hybrid) sudah muncul di **BAB III §3.4** serta **BAB V**. Namun **Latar Belakang tidak pernah menyatakan** bahwa penelitian ini bersifat komparatif, dan bahkan setelah diperbaiki di paragraf penutup, penguji menilai penjelasannya **terlalu di bawah** (baru muncul di akhir). Masalahnya:

1. Sifat komparatif tidak tampak (bertentangan dengan judul dan BAB III/V).
2. "Apa itu" studi komparatif tidak dijelaskan **sejak awal** — pembaca baru tahu di paragraf penutup.
3. "Hal-hal yang dilakukan" belum diuraikan konkret (model apa saja yang dibandingkan, dataset, skenario evaluasi, metrik).

---

## Teks BARU #1 — Paragraf ORIENTASI di awal (SISIPKAN setelah para 378)

Sisipkan paragraf ringkas ini **tepat setelah paragraf pembuka (378)**, sebelum pembahasan metode domain spasial (para 379). Tujuannya menjawab "apa itu" sejak awal:

> Penelitian ini merupakan sebuah studi komparatif yang membandingkan tiga pendekatan deteksi deepfake, yaitu pendekatan berbasis domain spasial, pendekatan berbasis domain frekuensi, dan pendekatan hybrid yang menggabungkan keduanya. Tujuannya adalah mengukur secara langsung dan terkontrol seberapa besar kontribusi analisis domain frekuensi dalam meningkatkan kemampuan deteksi, terutama ketahanan model ketika diuji lintas dataset. Uraian selanjutnya memaparkan perkembangan pendekatan deteksi deepfake beserta celah penelitian yang mendasari pemilihan rancangan komparatif tersebut.

*Catatan: kalimat terakhir berfungsi sebagai jembatan ke paragraf 379–384 (kajian) sehingga alur tetap mengalir. Menyisipkan paragraf baru adalah edit Word paling aman (tidak menyentuh run/sitasi/format paragraf lain).*

---

## Teks LAMA (para 385 — akan diganti)

> Penelitian ini mengisi celah tersebut dengan membangun arsitektur hybrid XceptionNet dan FFT dengan late fusion dan Squeeze-and-Excitation (SE) gating yang dirancang untuk mengevaluasi kontribusi domain frekuensi terhadap generalisasi lintas dataset. Berbeda dari pekerjaan sebelumnya yang berfokus pada in-dataset accuracy, penelitian ini secara eksplisit mengevaluasi skenario FFPP ke Celebrity DeepFake (Celeb-DF atau CDF) dan CDF ke FFPP untuk mengukur seberapa besar fitur frekuensi mampu menahan performance drop yang lazim terjadi pada detektor spasial murni.

---

## Teks BARU #2 — detail di penutup (ganti para 385 dengan DUA paragraf berikut)

**Paragraf 385a — kerangka komparatif:**

> Penelitian ini mengisi celah tersebut melalui sebuah studi komparatif yang mengukur secara terkontrol seberapa besar kontribusi domain frekuensi terhadap kemampuan generalisasi lintas dataset. Alih-alih hanya membangun satu detektor, penelitian ini merancang, melatih, dan mengevaluasi tiga konfigurasi model pada kondisi eksperimen yang identik, yaitu (1) model domain spasial murni berbasis XceptionNet sebagai baseline, (2) model domain frekuensi murni berbasis FreqCNN yang bekerja pada peta log-magnitude Fast Fourier Transform (FFT), dan (3) model hybrid yang menggabungkan kedua cabang melalui late fusion dengan Squeeze-and-Excitation (SE) gating. Dengan menyetarakan data, protokol pelatihan, dan metrik pada ketiga model, perbedaan kinerja yang teramati dapat diatribusikan langsung pada domain fitur yang digunakan, sehingga kontribusi domain frekuensi dapat diisolasi dan diukur, bukan sekadar diasumsikan.

**Paragraf 385b — uraian konkret yang dilakukan:**

> Ketiga model dilatih dan diuji pada dua dataset benchmark, yaitu FaceForensics++ (FFPP) dan Celeb-DF (CDF), pada beberapa ukuran sampel untuk mengamati pengaruh volume data terhadap kinerja. Evaluasi dilakukan dalam dua skenario, yaitu in-dataset ketika model dilatih dan diuji pada dataset yang sama, serta cross-dataset ketika model dilatih pada FFPP lalu diuji pada CDF dan sebaliknya CDF ke FFPP. Area Under the Curve (AUC) digunakan sebagai metrik utama karena paling relevan untuk menilai kelayakan deteksi di dunia nyata. Melalui perbandingan langsung ketiga konfigurasi tersebut, penelitian ini menilai apakah penambahan fitur frekuensi mampu menahan penurunan kinerja lintas dataset yang lazim dialami detektor domain spasial murni, sekaligus menetapkan apakah dan seberapa besar pendekatan hybrid memberikan keunggulan dibandingkan model domain tunggal.

> **Catatan refinement (2026-07-28):** frasa penutup diubah dari *"menetapkan sejauh mana pendekatan hybrid lebih unggul"* menjadi *"menetapkan apakah dan seberapa besar pendekatan hybrid memberikan keunggulan"* agar tidak mengasumsikan hasil (netral secara ilmiah, aman saat dipertanyakan penguji mengingat ada kasus kontribusi cabang frekuensi yang negatif).

---

## Opsional — sinyal komparatif di akhir para 384 (kini tidak wajib)

> Karena paragraf orientasi awal (Teks BARU #1) sudah menegaskan sifat komparatif sejak awal, penambahan kalimat di para 384 ini menjadi **opsional** (boleh dilewati agar tidak berlebihan). Disimpan sebagai cadangan bila ingin memperkuat transisi.

Agar peralihan ke tiga model di para 385 tidak terasa mendadak, tambahkan **satu kalimat penutup** di akhir paragraf 384 (paragraf yang membahas SpecXNet, FSBI, Frequency-Domain Masking). Paragraf 384 saat ini berakhir dengan:

> …tetapi sebagian besar masih dioptimalkan untuk performa in-dataset pada FFPP, dan belum mengevaluasi secara sistematis kontribusi fusi late dan gating terhadap robustness lintas dataset.

Tambahkan setelahnya:

> Belum tersedianya perbandingan terkendali antara model domain spasial murni, model domain frekuensi murni, dan model gabungannya pada protokol yang setara membuat besar kontribusi masing-masing domain terhadap generalisasi lintas dataset masih sulit dipastikan.

Kalimat ini memunculkan "gap komparatif" tepat sebelum para 385, sehingga keputusan membandingkan tiga model terasa termotivasi. (Opsional — para 384 sudah bersitasi; penambahan ini tidak memerlukan sitasi baru karena berupa perumusan gap oleh penulis.)

---

## Catatan penerapan

- Ganti satu paragraf 385 lama dengan dua paragraf baru di atas. Isi lama yang penting (late fusion + SE gating, skenario FFPP↔CDF, kontras terhadap fokus in-dataset) sudah dipertahankan dan dilebur ke dalam versi baru.
- Konsisten dengan **BAB III §3.4** (tiga varian model, "perbandingan terkontrol") dan **BAB V** ("studi komparatif yang mengukur kontribusi domain spasial, domain frekuensi, dan gabungan keduanya"). Tidak ada klaim baru yang perlu sitasi tambahan pada dua paragraf ini (merupakan kontribusi/desain penulis).
- Gaya: tanpa em-dash dan titik-koma, sesuai konvensi penulisan skripsi.
- Ukuran sampel sengaja ditulis "beberapa ukuran sampel" (bukan angka spesifik) agar tidak duplikatif dengan BAB III/IV. Angka pastinya: FFPP [100, 300, 600, 1000], CDF [100, 250, 500, 750].
