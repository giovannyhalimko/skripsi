# REVISI BAB II & III — Penambahan Deployment (Gradio) + Konsolidasi Rumus FFT

> **Cara pakai:** tiap blok = **satu sub-bab / satu bagian utuh** siap-tempel. Bagian **baru** ditandai **「TAMBAHAN」 … 「/TAMBAHAN」**; bagian yang **dihapus** ditandai **「DIHAPUS」**. Ganti sub-bab lama di Word dengan versi ini.
>
> **Sitasi:** pada bagian yang direproduksi dari dokumen lama, sitasi dibiarkan apa adanya (semua berupa CITATION field). Penyeragaman gaya ke (Nama, Tahun) ditangani terpisah (lihat handoff §4).
>
> **Penomoran:** ikuti instruksi renumber pada bagian BAB II; setelah semua diterapkan, nomori ulang berurutan / Update Fields.

---

## ✅ STATUS PENERAPAN (cek docx 2026-06-17 11:50)

| Bagian | Status |
|---|---|
| BAB II · Konsolidasi rumus FFT (hapus 2.17/2.18/2.20, renumber) | ✅ **SUDAH** — preprocessing kini 2.16–2.19; total BAB II = 2.40 |
| BAB III · Tabel 3.16 (Gradio + opencv-python-headless) | ✅ **SUDAH** masuk |
| BAB III · Sub-bab "Skema Inferensi dan Purwarupa Sistem" | ⚠️ **SUDAH ada, tetapi perlu 1 koreksi** (lihat ⚠️ di TAMBAHAN B) |
| BAB IV · 4.1.2 dirampingkan jadi hasil-saja | ✅ **SUDAH** (merujuk BAB III, benar) |

> **⚠️ KOREKSI TERSISA (penting):** sub-bab BAB III "Skema Inferensi dan Purwarupa Sistem" yang ter-paste **masih memuat kalimat terakhir "Rincian antarmuka dan tangkapan layar purwarupa disajikan pada BAB IV."** → **HARUS DIHAPUS** (BAB III tidak boleh merujuk BAB IV). Selain itu ada artefak penulisan `di-*deploy*` (tanda bintang markdown ikut ter-paste) → perbaiki jadi *deploy* (miring, tanpa bintang). Versi final paragraf ada di TAMBAHAN B di bawah.

---

## 🟥 BAB III — TAMBAHAN A · Tabel 3.16 "Kebutuhan Perangkat Lunak" (2 baris baru) — ✅ SUDAH

**Aksi:** ✅ **sudah diterapkan di docx.** (Arsip) tambahkan dua pustaka terkait purwarupa/deployment ke Tabel 3.16. Tabel HTML lengkap (siap Copy→Paste) sudah disediakan di `documents/table/tabel_3_16_kebutuhan_perangkat_lunak.html`. Dua baris yang ditambahkan:

**「TAMBAHAN」**

| Pustaka / Alat | Peran dalam penelitian | Justifikasi pemilihan |
|---|---|---|
| `opencv-python-headless` | Pembacaan dan pencuplikan *frame* video pada lingkungan *deployment* (Hugging Face Spaces) yang tidak memiliki antarmuka grafis (GUI) | Varian OpenCV tanpa dependensi GUI, sesuai untuk lingkungan server/CPU |
| *Gradio* | Membangun antarmuka purwarupa interaktif untuk perbandingan tiga model dan *deployment* ke Hugging Face Spaces (subbab 4.1.2) | SDK antarmuka ringan dengan dukungan *native* pada platform Hugging Face Spaces |

> Letak: `opencv-python-headless` disisipkan tepat setelah baris OpenCV; *Gradio* di akhir tabel (setelah matplotlib).

**「/TAMBAHAN」**

---

## 🟥 BAB III — TAMBAHAN B · Sub-bab "Skema Inferensi dan Purwarupa Sistem" (sudah ada — PERLU KOREKSI)

**Status:** sub-bab ini **sudah ada di docx**, tetapi versi yang ter-paste adalah versi lama yang **masih merujuk BAB IV** dan memuat artefak `di-*deploy*`.

**Aksi (pilih salah satu):**
- **(a) Termudah:** pada sub-bab yang ada, **HAPUS kalimat terakhir** "Rincian antarmuka dan tangkapan layar purwarupa disajikan pada BAB IV." dan perbaiki `di-*deploy*` → *deploy*. Selesai.
- **(b) Lebih rapi:** ganti **seluruh isi** sub-bab dengan versi final di bawah (paragraf ke-2 sedikit diperluas dengan deskripsi kartu verdict & panel; **tanpa rujukan BAB IV**).

Letak tetap di bagian **Analisis Sistem** (antara "Konfigurasi dan Orkestrasi Pipeline" dan "Keluaran Sistem"). Sub-bab ini **tidak boleh merujuk BAB IV**.

---

**「TAMBAHAN」**

**Skema Inferensi dan Purwarupa Sistem**

Selain digunakan dalam evaluasi eksperimental pada level *frame*, model terlatih diterapkan pada skenario inferensi *end-to-end* terhadap satu video utuh. Tahapannya identik dengan pipeline pelatihan: video disampel pada 5 FPS (hingga 16 *frame*), setiap *frame* dideteksi dan dipotong wajahnya menggunakan MTCNN (margin 0,3), lalu dipreproses sama persis (RGB → 224×224 → normalisasi ImageNet; FFT → *log-magnitude* → normalisasi statistik dataset). Probabilitas-*fake* per-*frame* kemudian diagregasi menjadi satu keputusan level-video dengan merata-ratakan probabilitas seluruh *frame*, dan video diklasifikasikan sebagai *fake* apabila rata-rata tersebut mencapai ambang keputusan yang disetel pada set validasi. Metrik evaluasi penelitian tetap dihitung pada level *frame* untuk mengisolasi kualitas detektor, sedangkan agregasi level-video ini diterapkan pada tahap penggunaan; keduanya tidak saling bertentangan.

Untuk menunjukkan kelaikan penerapan sekaligus mendukung sifat komparatif penelitian, ketiga model (spatial, hybrid, dan frequency) dikemas dalam sebuah purwarupa interaktif berbasis Gradio yang di-*deploy* ke layanan Hugging Face Spaces. Pengguna mengunggah sebuah video wajah, kemudian purwarupa menjalankan ketiga model secara berdampingan dan menampilkan verdict masing-masing dalam bentuk kartu (badge REAL/FAKE beserta bar probabilitas-*fake* dengan ambang keputusan ditandai). Purwarupa juga menyediakan panel "*what the models see*" yang menampilkan potongan wajah hasil *cropping* (masukan cabang spasial) berdampingan dengan spektrum FFT-nya (masukan cabang frekuensi), sehingga informasi yang diproses oleh masing-masing cabang dapat dibandingkan secara langsung. Seluruh praproses pada purwarupa menggunakan kembali modul yang sama dengan pipeline pelatihan untuk menjamin konsistensi antara skenario pelatihan dan penerapan.

**「/TAMBAHAN」**

---

## 🟩 BAB IV — PENYESUAIAN · Hindari duplikasi dengan BAB III (subbab 4.1.2) — ✅ SUDAH

**Status:** ✅ **sudah diterapkan di docx** — 4.1.2 kini hanya memuat hasil (paragraf "keluaran praktis" + Gambar 4.1 & 4.2 + rujukan ke 4.2.4), tanpa deskripsi metode. Blok di bawah dipertahankan sebagai arsip/acuan.

**Konteks:** naskah BAB IV sebelumnya memiliki subbab **4.1.2 "Implementasi dan Purwarupa Sistem"** yang **mendeskripsikan metode inferensi & purwarupa** — kini metode tersebut menjadi milik BAB III (TAMBAHAN B). Agar tidak duplikasi, subbab 4.1.2 **dirampingkan menjadi penyajian hasil saja** (sistem yang berhasil di-*deploy* + keluaran visualnya), tanpa mengulang alur metode.

**Aksi:** ganti **seluruh isi prosa** subbab 4.1.2 (dua paragraf metode + paragraf panel) dengan versi ringkas berikut. **Gambar 4.1 dan Gambar 4.2 tetap di posisi yang sama** (tidak ada penomoran ulang). Catatan: BAB IV **boleh** merujuk ke BAB III.

**「GANTI ISI 4.1.2 DENGAN」**

Sebagai keluaran praktis penelitian, purwarupa perbandingan tiga model yang dirancang pada sub-bab Skema Inferensi dan Purwarupa Sistem (BAB III) berhasil di-*deploy* dan beroperasi pada layanan Hugging Face Spaces. Gambar 4.1 menampilkan antarmuka purwarupa beserta kartu verdict ketiga model untuk satu video uji, memperlihatkan bahwa sistem mampu menyajikan keputusan spatial, hybrid, dan frequency secara berdampingan sebagaimana dirancang.

Gambar 4.2 menampilkan panel "*what the models see*", yaitu potongan wajah (masukan cabang spasial) berdampingan dengan spektrum FFT-nya (masukan cabang frekuensi). Pada panel ini terlihat bahwa spektrum FFT wajah *real* dan *fake* nyaris tidak dapat dibedakan secara visual — pengamatan kualitatif yang menjadi dasar pembahasan akar penyebab lemahnya cabang frekuensi pada sub-bab 4.2.4.

*Gambar 4.1 Antarmuka purwarupa perbandingan tiga model pada Hugging Face Spaces*
*Gambar 4.2 Panel "what the models see": potongan wajah (masukan spasial) dan spektrum FFT (masukan frekuensi)*

**「/GANTI」**

> **Alasan tetap di-keep (bukan dihapus):** subbab 4.1.2 ringkas ini memuat **hasil khusus yang dibahas** — yaitu purwarupa yang beroperasi (keluaran praktis) dan, terutama, panel spektrum FFT (Gambar 4.2) yang menjadi **bukti kualitatif** dan dianalisis pada 4.2.4. Yang dihapus hanya **deskripsi metode** (alur 5 FPS, MTCNN, agregasi, ambang) karena sudah pindah ke BAB III.
>
> *(Opsional, lebih ketat: bila dosen menilai Gambar 4.1 (antarmuka) bukan "hasil yang dibahas", paragraf pertama 4.1.2 boleh dihapus dan Gambar 4.1 dipindah ke sub-bab BAB III. Namun ini memicu penomoran ulang gambar BAB IV — tidak disarankan kecuali diminta.)*

---

## 🟦 BAB II — UBAH · Sub-bab "Fast Fourier Transform (FFT)" (konsolidasi rumus dobel) — ✅ SUDAH

**Status:** ✅ **sudah diterapkan di docx** — preprocessing kini hanya 2.16 (grayscale), 2.17 (high-pass), 2.18 (fftshift), 2.19 (z-score); duplikat DFT/magnitude/log dihapus; total persamaan BAB II = **2.40**. Pastikan rujukan "persamaan 2.x" di BAB III sudah ikut diperbarui (tabel di bawah). Blok berikut dipertahankan sebagai arsip/acuan.

**Aksi:** rumus inti DFT, magnitude, dan log scaling sudah didefinisikan di sub-bab teori *Transformasi Fourier (FFT)* (Persamaan 2.1, 2.3, 2.4). Pada sub-bab ini, **hapus tiga rumus duplikat** (DFT, magnitude, log) dan ganti dengan rujukan; pertahankan rumus khas pipeline (grayscale, high-pass, fftshift, z-score). **Renumber** persamaan setelah penghapusan (lihat tabel di bawah). Berikut sub-bab utuh hasil revisi.

---

Fast Fourier Transform (FFT) merupakan algoritma efisien untuk menghitung Discrete Fourier Transform (DFT), yaitu proses yang mengubah citra dari domain spasial menjadi domain frekuensi. Transformasi ini memungkinkan analisis distribusi energi frekuensi pada citra sehingga pola-pola artefak halus yang tidak terlihat pada domain spasial dapat teridentifikasi. Pada penelitian deteksi deepfake, FFT menjadi komponen penting karena manipulasi berbasis GAN cenderung menimbulkan ketidakwajaran sinyal frekuensi, terutama pada rentang *high-frequency* akibat proses *upsampling*, konvolusi, dan operasi *blending* [8, 11, 16].

Dalam konteks deteksi, informasi frekuensi menjadi sangat berharga karena generator GAN secara matematis tidak mampu mempertahankan *natural image statistics* sehingga meninggalkan *spectral fingerprint* yang khas dan konsisten. Sebelum transformasi Fourier diterapkan, citra RGB terlebih dahulu dikonversi menjadi citra satu kanal (*grayscale*), karena analisis frekuensi cukup dilakukan pada informasi luminansi yang merepresentasikan distribusi intensitas spasial. Konversi menggunakan standar ITU-R BT.601:

>   Y = 0,299·R + 0,587·G + 0,114·B     (2.16)

di mana Y adalah nilai luminansi, sedangkan R, G, dan B adalah nilai kanal warna merah, hijau, dan biru. Bobot yang berbeda pada setiap kanal mencerminkan sensitivitas mata manusia terhadap masing-masing warna.

Citra *grayscale* tersebut kemudian ditransformasi ke domain frekuensi menggunakan **DFT dua dimensi sebagaimana telah didefinisikan pada Persamaan 2.1**, dengan f(x,y) sebagai intensitas piksel dan F(u,v) sebagai representasi frekuensinya.

「DIHAPUS — Persamaan 2.17 (DFT) dihapus; sudah ada di Persamaan 2.1」

Besarnya energi frekuensi (*magnitude spectrum*) dihitung **menggunakan Persamaan 2.3**.

「DIHAPUS — Persamaan 2.18 (magnitude) dihapus; sudah ada di Persamaan 2.3」

Pada citra wajah, energi frekuensi sangat terkonsentrasi pada komponen DC dan frekuensi rendah yang merepresentasikan struktur global wajah (bentuk, pencahayaan) dan kurang informatif untuk deteksi deepfake. Sebaliknya, artefak sintesis seperti *checkerboard pattern* dan *spectral rolloff* yang anomal terutama muncul pada frekuensi menengah dan tinggi. Oleh karena itu *magnitude spectrum* dapat dilewatkan melalui *Gaussian high-pass filter* untuk menekan dominasi komponen frekuensi rendah:

>   H(u,v) = 1 − exp( − [ (u−u_c)² + (v−v_c)² ] / [ 2·(β·N)² ] )     (2.17)   ← sebelumnya 2.19

di mana (u_c, v_c) adalah koordinat pusat peta frekuensi setelah *fftshift*, N adalah dimensi peta, dan β adalah *cutoff fraction* yang mengontrol radius penekanan (σ = β·N). Magnitude terfilter diperoleh dari F'(u,v) = F(u,v) · H(u,v).

Untuk memudahkan analisis, spektrum frekuensi dikompresi rentang dinamisnya **menggunakan log scaling pada Persamaan 2.4**.

「DIHAPUS — Persamaan 2.20 (log) dihapus; sudah ada di Persamaan 2.4」

Selain itu, digunakan pula *frequency shifting* (*fftshift*) sehingga komponen frekuensi rendah berada di pusat tampilan spektrum:

>   F_shift(u,v) = F( (u + M/2) mod M , (v + N/2) mod N )     (2.18)   ← sebelumnya 2.21

Karena setiap dataset memiliki karakteristik spektral yang berbeda akibat perbedaan kamera, resolusi, dan metode kompresi, peta *magnitude* perlu dinormalisasi sebelum digunakan oleh model. Normalisasi dilakukan dengan *z-score*:

>   x̂ = (x − μ) / σ     (2.19)   ← sebelumnya 2.22

di mana μ dan σ adalah rata-rata dan simpangan baku global yang dihitung dari seluruh piksel peta *magnitude* pada satu dataset. Tanpa normalisasi yang tepat, fitur frekuensi antar dataset akan memiliki skala yang tidak sebanding. Transformasi ini menghasilkan representasi frekuensi yang lebih mudah ditafsirkan dan lebih stabil untuk diproses oleh model deteksi.

*(Paragraf-paragraf lanjutan — mulai "Deepfake berbasis GAN menghasilkan pola-pola artefak…" hingga akhir sub-bab "…dikombinasikan dengan model CNN berbasis spasial." — tetap seperti versi lama, tidak diubah.)*

---

### Konsekuensi penomoran (BAB II)

Setelah menghapus 2.17, 2.18, 2.20, persamaan berikutnya bergeser **−3**:

| Lama | Baru | Isi |
|---|---|---|
| 2.19 | **2.17** | High-pass H(u,v) |
| 2.21 | **2.18** | fftshift |
| 2.22 | **2.19** | z-score |
| 2.23 | **2.20** | Noise augmentasi |
| 2.24 | **2.21** | Band masking horizontal |
| … (geser −3) | … | … |
| 2.43 | **2.40** | Generalization drop |

### Pembaruan rujukan di BAB III

| Rujukan BAB III lama | Jadi |
|---|---|
| "persamaan 2.17" (DFT) | **2.1** |
| "persamaan 2.18" (magnitude) | **2.3** |
| "persamaan 2.20" (log) | **2.4** |
| "persamaan 2.19" (high-pass) | **2.17** |
| "persamaan 2.22" (z-score) | **2.19** |
| "persamaan 2.16" (grayscale) | 2.16 (tetap) |
| "persamaan 2.15" (proyeksi) | 2.15 (tetap) |

> **Alternatif ringan** (bila tak ingin renumber): biarkan ketiga rumus, cukup tambahkan catatan "(identik dengan Persamaan 2.1/2.3/2.4)". Duplikasi teori-vs-terapan bukan kesalahan — prioritas rendah.

---

## Ringkasan tindakan ronde ini

| Bagian | Aksi | Status (cek docx 11:50) |
|---|---|---|
| BAB III · Tabel 3.16 | Tambah baris Gradio + opencv-python-headless | ✅ SUDAH |
| BAB III · Sub-bab "Skema Inferensi…" | Rumah metodologi inferensi+purwarupa | ⚠️ ADA, **hapus kalimat ref BAB IV** + perbaiki `di-*deploy*` |
| BAB IV · 4.1.2 | Rampingkan jadi hasil saja; gambar 4.1/4.2 tetap; rujuk balik ke BAB III | ✅ SUDAH |
| BAB II · Sub-bab FFT | Hapus rumus dobel → renumber + rujukan BAB III diperbarui | ✅ SUDAH (semua rujukan 2.x BAB III terverifikasi benar) |

### 🔴 Satu-satunya yang tersisa
Di sub-bab BAB III **"Skema Inferensi dan Purwarupa Sistem"**, hapus kalimat terakhir:
> ~~"Rincian antarmuka dan tangkapan layar purwarupa disajikan pada BAB IV."~~

dan perbaiki `di-*deploy*` → *deploy*. Setelah itu, seluruh revisi ronde ini tuntas.

> **Prinsip pembagian:** inferensi & purwarupa **dijelaskan (metode) di BAB III**; BAB IV **hanya menyajikan hasilnya** (purwarupa beroperasi + panel FFT yang dianalisis di 4.2.4) — tanpa mengulang metode. BAB III tidak boleh merujuk BAB IV; BAB IV boleh merujuk BAB III.
