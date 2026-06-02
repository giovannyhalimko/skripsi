# Revisi v2 — BAB II & BAB III: Sistem, Teknologi, dan Konsistensi Kode

**Tanggal:** 2026-05-28 15:00
**Dokumen sasaran:** `.docx` OneDrive — *Metode Peningkatan Deteksi Deepfake...* (tersimpan 28 Mei 13:54)
**Sumber kebenaran:** kode `deepfake_hybrid/` (`config.yaml`, `src/`, `scripts/`)
**Cara pakai:** dokumen ini berisi instruksi *manual edit*. Setiap tindakan memuat **(a) lokasi persis** (teks-jangkar untuk dicari di Word), **(b) apa yang diubah/dihapus/ditambah**, dan **(c) teks final** yang bisa langsung di-*paste*.

> **Konteks status:** revisi lama (C.2, C.4 sitasi, D.2 pseudocode, D.5 augmentasi) **sudah diterapkan** ke `.docx`. Dokumen v2 ini mencakup **4 tindakan yang TERSISA** + 1 perbaikan referensi.

---

## Daftar Tindakan (ringkasan)

| # | Tindakan | BAB | Jenis |
|---|---|---|---|
| **T1** | Tambah subbab **3.3.2 Deteksi Wajah dan Cropping** (MTCNN) | III | TAMBAH |
| **T2** | Hapus klaim **"Face Alignment"** (sub-paragraf + baris Tabel 2.4) | II | HAPUS |
| **T3** | Tambah subbab **3.8 Analisis Sistem** (lengkap) | III | TAMBAH |
| **T4** | Tambah sitasi **(Zhang et al., 2016)** untuk MTCNN ke Daftar Pustaka | — | TAMBAH |
| **T5** | Perbaiki entri Daftar Pustaka **(Hu et al., 2018)** — 5 penulis → 3 penulis | — | UBAH |

---

## T1 — Subbab BARU 3.3.2 "Deteksi Wajah dan Cropping" (BAB III)

### Mengapa
Pipeline memotong wajah dengan **MTCNN** (`facenet-pytorch`, `src/face_utils.py`), dipanggil saat ekstraksi *frame* (`extract_frames.py --face-crop`). **Semua hasil BAB IV** diproduksi dengan `face_crop=True`:
- `config.yaml:23` → `freq_base_channels: 64` berkomentar *"64 for face crops, 32 for full scenes"*.
- `colab_run.ipynb` → `FACE_CROP = True`, `FACE_MARGIN = 0.3`.
- Eksperimen internal (`outputs/2026-04-09/face_crop/n100/conclusion.md`): *face crop* menaikkan AUC spatial FFPP **0,696 → 0,901**.

Namun di BAB III **metodologi**, subbab 3.3.1 "Ekstraksi Frame dari Video" langsung lompat ke "Konversi Domain Frekuensi (FFT)" — **langkah cropping hilang**. Tanpa langkah ini, hasil BAB IV tidak dapat direproduksi dari narasi.

### Lokasi PERSIS (cari teks ini di Word)
- **Setelah** akhir subbab 3.3.1 — yaitu paragraf yang berbunyi:
  > "*Proses ekstraksi dilakukan secara paralel menggunakan multiprocessing pool untuk mempercepat pemrosesan ... Hasil ekstraksi disimpan dalam berkas manifes CSV yang berisi kolom `video_id`, `label`, dan `frames_dir` sebagai referensi untuk tahap selanjutnya.*"
  dan **setelah** "Gambar 3.3 Pseudocode ekstraksi frame dari video".
- **Sebelum** heading "**Konversi Domain Frekuensi (FFT)**".

### Akibat penomoran
- Heading "Konversi Domain Frekuensi (FFT)" yang sekarang 3.3.2 → **menjadi 3.3.3**; seluruh sub-subbab 3.3.2.x → **3.3.3.x**.
- Subbab Augmentasi yang sekarang 3.3.3 → **menjadi 3.3.4** (beserta 3.3.3.x → 3.3.4.x).
- Jika menambahkan ilustrasi cropping, nomor Gambar 3.4/3.5 dst. bergeser +1.

### Teks final (paste sebagai subbab 3.3.2)

> **3.3.2 Deteksi Wajah dan Cropping**
>
> Bagian wajah merupakan target utama manipulasi *deepfake*, sementara latar belakang umumnya tidak mengandung informasi diskriminatif dan justru berperan sebagai *noise* (Afchar et al., 2018; Rössler et al., 2019). Oleh karena itu, setiap *frame* hasil ekstraksi terlebih dahulu melewati tahap deteksi dan pemotongan wajah sebelum dianalisis.
>
> Deteksi wajah dilakukan menggunakan **MTCNN** (*Multi-task Cascaded Convolutional Networks*) (Zhang et al., 2016) dari pustaka `facenet-pytorch`. MTCNN bekerja melalui tiga jaringan konvolusional bertingkat (*cascade*):
> 1. **P-Net** (*Proposal Network*) — secara cepat menghasilkan banyak kandidat *bounding box* wajah beserta skor kepercayaannya.
> 2. **R-Net** (*Refine Network*) — menyaring dan membuang kandidat palsu dari P-Net, serta memperhalus koordinat kotak.
> 3. **O-Net** (*Output Network*) — memfinalisasi posisi *bounding box* wajah (dan titik *landmark*) dengan presisi tertinggi.
>
> Detektor dikonfigurasi dengan ukuran wajah minimum 60 piksel dan ambang kepercayaan bertahap sebesar 0,6, 0,7, dan 0,7 untuk masing-masing tahap. Apabila pada satu *frame* terdeteksi lebih dari satu wajah, dipilih wajah dengan luas *bounding box* terbesar. Kotak terpilih kemudian diperluas dengan margin sebesar 30% pada setiap sisi untuk memastikan seluruh area wajah beserta konteks tepi (rahang, dahi) ikut terpotong, lalu *frame* dipotong sesuai kotak tersebut. Apabila tidak ada wajah yang terdeteksi pada suatu *frame*, *frame* penuh digunakan sebagai *fallback* agar tidak ada data yang hilang.
>
> Pembatasan analisis hanya pada region wajah meminimalkan jumlah fitur tidak relevan, sehingga model memiliki kapasitas lebih besar untuk mempelajari pola-pola manipulasi. Secara empiris, penerapan *face cropping* meningkatkan performa model spasial secara substansial pada dataset FaceForensics++. *Frame* hasil *crop* selanjutnya diubah ukurannya menjadi 224×224 piksel sebelum memasuki tahap konversi domain frekuensi.

> **Catatan implementasi (boleh dimasukkan sebagai catatan kaki / kalimat tambahan):** karena objek MTCNN tidak dapat di-*pickle* untuk *multiprocessing*, ekstraksi *frame* dengan *face cropping* dijalankan secara sekuensial, sedangkan tanpa *cropping* dijalankan paralel.

---

## T2 — Hapus klaim "Face Alignment" (BAB II)

### Mengapa
Kode **tidak melakukan** *face alignment*. `src/face_utils.py` hanya: deteksi *bounding box* (`detect_face_bbox`) → ekspansi margin 30% → *crop* (`crop_face`). Tidak ada penyelarasan berbasis *landmark*. Klaim *alignment* sebagai langkah preprocessing kita = langkah yang tidak pernah dijalankan → harus dihapus agar metodologi jujur dan konsisten.

### Hasil sweep menyeluruh seluruh dokumen
Pencarian "align/alignment/penyelarasan/orientasi wajah" di seluruh `.docx` menemukan **5 kemunculan**. Tiga harus **DIHAPUS/DIPERBAIKI** (menyebut alignment sebagai langkah preprocessing kita), dua harus **DIPERTAHANKAN** (konteks berbeda — bukan pipeline kita):

| Lokasi | Kalimat | Tindakan |
|---|---|---|
| **(a)** subbab 2.16, paragraf intro "Alur preprocessing" | "...Alur preprocessing mencakup: ekstraksi frame, deteksi wajah, **face alignment**, cropping, resize..." | ✂️ **HAPUS** "face alignment" |
| **(b)** subbab 2.16, sub-paragraf "Face Alignment" | "**Face Alignment** — Penyelarasan orientasi wajah berdasarkan landmark..." | ✂️ **HAPUS** seluruh sub-paragraf |
| **(c)** Tabel 2.4, baris tahap 3 | "Face alignment \| Menyelaraskan orientasi wajah \| Wajah ter-align" | ✂️ **HAPUS** baris + renumber |
| (d) subbab "Warping" (BAB II) | "...warping sering muncul sebagai konsekuensi dari proses **face alignment**, resizing... antara wajah sumber dan wajah target." | ✅ **PERTAHANKAN** — ini menjelaskan proses *pembuatan* deepfake (GAN), bukan preprocessing kita |
| (e) deskripsi FaceSwap (BAB II) | "FaceSwap, menggantikan wajah target menggunakan metode **penyelarasan geometris** dan blending manual." | ✅ **PERTAHANKAN** — ini menjelaskan teknik manipulasi FaceSwap, bukan preprocessing kita |

### Detail tindakan yang DIHAPUS/DIUBAH

**(a) Paragraf intro subbab 2.16 "Preprocessing"** — kalimat terakhir berbunyi:
> "*Alur preprocessing mencakup: ekstraksi frame, deteksi wajah, **face alignment**, cropping, resize, normalisasi, konversi skala warna, dan transformasi FFT.*"

➡️ **UBAH** menjadi (hapus "face alignment", urutan kini selaras dengan Tabel 2.4):
> "*Alur preprocessing mencakup: ekstraksi frame, deteksi wajah, cropping, resize, normalisasi, konversi skala warna (grayscale), dan transformasi FFT.*"

**(b) Sub-paragraf "Face Alignment"** — terletak di antara sub-paragraf "Deteksi wajah dan cropping" dan "Resize". Berbunyi:
> "**Face Alignment** — Penyelarasan orientasi wajah berdasarkan landmark (posisi mata/hidung) agar rotasi dan kemiringan antar-frame lebih konsisten. Face alignment juga mengurangi kesalahan prediksi yang dapat muncul akibat variasi sudut pandang..."

➡️ **HAPUS seluruh sub-paragraf ini (judul + isi).**

**(c) Tabel 2.4 "Tahapan Preprocessing"** — saat ini 8 baris. Baris ke-3:
> | 3 | Face alignment | Menyelaraskan orientasi wajah | Wajah ter-align |

➡️ **HAPUS baris ini**, lalu **nomori ulang** baris berikutnya (4→3, 5→4, 6→5, 7→6, 8→7). Hasil akhir Tabel 2.4 menjadi **7 tahap**.

> **Versi HTML siap-paste (SUDAH diperbarui):** [`documents/table/tabel_2_3_tahapan_preprocessing.html`](../documents/table/tabel_2_3_tahapan_preprocessing.html) — baris *Face alignment* sudah dihapus (kini 7 baris) dan caption diselaraskan ke "Tabel 2.4". *(Catatan: nama file masih `tabel_2_3_...` karena penomoran file lama; caption di dalamnya sudah "Tabel 2.4" sesuai docx.)*

| Tahap | Operasi | Tujuan Utama | Output |
|---|---|---|---|
| 1 | Ekstraksi frame | Mengubah video menjadi deretan frame | Citra per-frame |
| 2 | Deteksi wajah | Menemukan lokasi (bounding box) wajah | Koordinat wajah |
| 3 | Cropping | Memotong area wajah dari background | Patch wajah |
| 4 | Resize 224×224 | Menyeragamkan resolusi | Citra 224×224 |
| 5 | Normalisasi pixel | Menstabilkan intensitas dan kontras | Citra ternormalisasi |
| 6 | Transformasi FFT | Mengubah ke domain frekuensi | Spektrum frekuensi |
| 7 | Channel fusion | Menggabungkan RGB dan kanal frekuensi | Tensor 4-channel |

**(d) Kalimat penutup di bawah tabel** — saat ini: "*Tahapan 1–6 membentuk preprocessing spasial, sedangkan tahapan 7–8 menghubungkannya dengan representasi frekuensi...*"
➡️ **UBAH** menjadi: "*Tahapan 1–5 membentuk preprocessing spasial, sedangkan tahapan 6–7 menghubungkannya dengan representasi frekuensi yang digunakan sebagai fitur tambahan pada model hybrid.*"

> **Konsistensi:** jangan memunculkan kembali *alignment* sebagai langkah preprocessing kita di mana pun (termasuk subbab 3.3.2 baru pada T1). Kemunculan (d) "Warping" dan (e) "FaceSwap" **tetap** karena keduanya menjelaskan proses pembuatan/manipulasi deepfake, bukan pipeline preprocessing penelitian ini.

---

## T3 — Subbab BARU 3.8 "Analisis Sistem" (BAB III) — LENGKAP

### Mengapa & status
Subbab "Analisis Sistem" **belum ada sama sekali** di `.docx`. Diminta reviewer (P1-BAB3 sistem). Harus mencakup perangkat keras, perangkat lunak (seluruh pustaka + versi + peran + justifikasi), orkestrasi pipeline, dan keluaran sistem.

### Lokasi PERSIS (.docx, BAB III)
- Sisipkan sebagai **subbab paling akhir BAB III**.
- **Setelah** subbab 3.7 "Metode Evaluasi Model" selesai — yaitu setelah sub-subbab terakhir "**Contoh Perhitungan Metrik**".
- **Sebelum** heading "**BAB IV HASIL DAN PEMBAHASAN**".
- Heading level subbab sama dengan 3.7 (mis. Heading 2). Sub-subbab 3.8.1–3.8.4 satu level di bawahnya.

### Sumber kebenaran nilai (agar konsisten dengan kode)
Diverifikasi dari `config.yaml` / `requirements.txt` / `src/`:
`image_size=224`, `batch_size=16`, `accum_steps=2` (efektif 32), `lr=2e-4`, `weight_decay=1e-4`, `epochs=30`, `early_stop_patience=12`, `label_smoothing=0.05`, `n_seeds=3`, AMP via `torch.cuda.amp.autocast` (CUDA). Python 3.9.

### Teks final (paste sebagai subbab 3.8)

> **3.8 Analisis Sistem**
>
> Subbab ini menjabarkan kebutuhan perangkat keras dan perangkat lunak yang digunakan untuk mengimplementasikan dan menjalankan seluruh *pipeline* penelitian, mulai dari *preprocessing* hingga evaluasi, beserta justifikasi pemilihan setiap teknologi.
>
> **3.8.1 Kebutuhan Perangkat Keras**
>
> Pelatihan model *deep learning* membutuhkan akselerasi GPU. Penelitian ini dikembangkan dan dijalankan pada lingkungan Google Colab Pro. Spesifikasi perangkat keras dirangkum pada Tabel 3.17.

**Versi HTML siap-paste:** [`documents/table/tabel_3_17_kebutuhan_perangkat_keras.html`](../documents/table/tabel_3_17_kebutuhan_perangkat_keras.html)

> | Komponen | Spesifikasi | Peran |
> |---|---|---|
> | GPU | NVIDIA berdukungan CUDA (Tesla T4 15 GB / V100) | Pelatihan dan inferensi model; mendukung *mixed precision* (AMP) dan TF32 pada arsitektur Ampere ke atas |
> | RAM | ≥ 12 GB | Pemuatan *batch* citra dan *cache* FFT ke memori |
> | Penyimpanan | Beberapa GB | Menyimpan *frame* hasil ekstraksi, *cache* FFT (`.npy`), dan *checkpoint* model |
> | CPU | Multi-core | *Fallback* untuk eksperimen kecil; ekstraksi *frame* paralel via *multiprocessing* |
>
> **3.8.2 Kebutuhan Perangkat Lunak**
>
> Implementasi menggunakan bahasa **Python 3.9** dengan ekosistem pustaka *deep learning* dan pemrosesan citra yang dirangkum pada Tabel 3.18.

**Versi HTML siap-paste:** [`documents/table/tabel_3_18_kebutuhan_perangkat_lunak.html`](../documents/table/tabel_3_18_kebutuhan_perangkat_lunak.html)

> | Pustaka / Alat | Peran dalam penelitian | Justifikasi pemilihan |
> |---|---|---|
> | **PyTorch** (`torch`) | *Framework* utama: definisi model, *autograd*, *training loop*, *mixed precision* (AMP), optimisasi (AdamW), fungsi *loss* (`BCEWithLogitsLoss`), dan penjadwalan *learning rate* | Dukungan GPU penuh dan fleksibilitas tinggi untuk riset arsitektur kustom |
> | **torchvision** | Transformasi dan augmentasi citra pada cabang spasial | Terintegrasi erat dengan PyTorch |
> | **timm** (*PyTorch Image Models*) | Menyediakan arsitektur **XceptionNet** beserta bobot *pretrained* ImageNet melalui `create_model("xception", pretrained=True)` | Implementasi *backbone* yang teruji dan akses langsung ke bobot *transfer learning* |
> | **facenet-pytorch** | Menyediakan **MTCNN** untuk deteksi dan *cropping* wajah pada tahap *preprocessing* (lihat subbab 3.3.2) | Detektor wajah ringan, akurat, dan mudah diintegrasikan |
> | **OpenCV** (`opencv-python`) | Membaca video, mengekstraksi *frame*, dan konversi ruang warna (BGR→RGB, *grayscale*) | Pustaka standar untuk I/O video dan operasi citra |
> | **NumPy** | Komputasi Transformasi Fourier 2D (`fft2`, `fftshift`) dan operasi numerik berbasis *array* | Fondasi komputasi numerik Python |
> | **scikit-learn** | Pembagian *train/validation/test* terstratifikasi (`train_test_split`) dan perhitungan metrik (AUC) | Standar evaluasi dan pembagian data yang reproducible |
> | **pandas** | Pengelolaan berkas manifes CSV (`video_id`, `label`, `frames_dir`) dan tabel hasil | Manipulasi data tabular yang efisien |
> | **Pillow** (PIL) | Pemuatan dan manipulasi citra sebagai *backend* transformasi torchvision | Format citra standar di ekosistem Python |
> | **PyYAML** | Membaca berkas konfigurasi terpusat `config.yaml` | Konfigurasi eksperimen yang ringkas dan mudah dibaca |
> | **tqdm** | Menampilkan *progress bar* pada proses berdurasi panjang | Pemantauan eksekusi pipeline |
> | **matplotlib** | Visualisasi hasil (kurva ROC, *learning curve*) pada BAB IV | Pembuatan grafik publikasi |
>
> **3.8.3 Konfigurasi dan Orkestrasi Pipeline**
>
> Seluruh hyperparameter dipusatkan pada berkas `config.yaml`, antara lain: ukuran citra 224×224, *batch size* 16 dengan *gradient accumulation* 2 langkah (*batch* efektif 32), *learning rate* awal $2 \times 10^{-4}$, *weight decay* $1 \times 10^{-4}$, maksimum 30 *epoch* dengan *early stopping* (*patience* 12), *label smoothing* 0,05, dan 3 *seed* untuk validitas statistik.
>
> Seluruh tahap dijalankan melalui skrip terpadu `run_pipeline.py` yang memanggil secara berurutan: ekstraksi *frame* dan *cropping* wajah (`extract_frames.py`), pembangunan *split* dataset (`build_splits.py`), prakomputasi *cache* FFT (`compute_fft_cache.py`), pelatihan model (`train.py`), dan evaluasi (`eval.py`). *Mixed precision training* diaktifkan secara otomatis ketika perangkat CUDA tersedia.
>
> **3.8.4 Keluaran Sistem**
>
> Untuk setiap konfigurasi pelatihan, *checkpoint* dengan AUC validasi tertinggi disimpan sebagai `best.pt`. Hasil evaluasi akhir disimpan dalam bentuk tabel pada direktori `outputs/tables/`, yaitu `Table1_in_dataset.csv` (evaluasi *in-dataset*), `Table2_cross_dataset.csv` (evaluasi *cross-dataset*), dan `Table3_generalization_drop.csv` (penurunan generalisasi).

---

## T4 — Sitasi BARU (Zhang et al., 2016) untuk MTCNN

Tambahkan ke **Daftar Pustaka** (dipakai oleh T1):

> K. Zhang, Z. Zhang, Z. Li, dan Y. Qiao, "Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks," *IEEE Signal Processing Letters*, vol. 23, no. 10, hlm. 1499–1503, 2016. doi: 10.1109/LSP.2016.2603342.

- Format in-text (gaya dokumen): **(Zhang et al., 2016)** — sudah dipakai di teks T1.
- ⚠️ **Hati-hati:** sudah ada entri **(Zhang et al., 2019)** untuk *spectral artifacts* — pastikan ini entri **berbeda** (tahun 2016, judul MTCNN), jangan tertukar.

---

## T5 — Perbaiki entri Daftar Pustaka (Hu et al., 2018) SE-Net

### Masalah
Entri saat ini di `.docx` mencampur **5 penulis** (versi jurnal TPAMI 2020) dengan **venue CVPR 2018**:
> ~~"J. Hu, L. Shen, S. Albanie, G. Sun dan E. Wu, Squeeze-and-Excitation Networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2018."~~

Paper **CVPR 2018** hanya 3 penulis (Hu, Shen, Sun). Pilih satu bentuk konsisten — **disarankan tetap CVPR 2018, 3 penulis**:

> J. Hu, L. Shen, dan G. Sun, "Squeeze-and-Excitation Networks," dalam *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2018, hlm. 7132–7141. doi: 10.1109/CVPR.2018.00745.

➡️ Hapus "S. Albanie" dan "E. Wu". Sitasi in-text (sudah ter-render **[36]** dan konsisten) tidak perlu diubah.

---

## Verifikasi setelah edit (checklist)
- [ ] T1: subbab 3.3.2 muncul sebelum FFT; subbab FFT & Augmentasi sudah ter-*renumber* (3.3.3, 3.3.4); *Update All Fields* (Ctrl+A → F9) untuk memperbarui nomor & daftar isi.
- [ ] T2: ketiga lokasi (a) paragraf intro 2.16, (b) sub-paragraf "Face Alignment", (c) baris Tabel 2.4 sudah dihapus/diperbaiki; Tabel 2.4 = 7 baris; kalimat penutup "1–5 / 6–7" sudah benar. **Cek** sisa: cari "align" di Word — yang tersisa hanya 2 (Warping & FaceSwap) yang memang dipertahankan.
- [ ] T3: subbab 3.8 muncul setelah 3.7 dan sebelum BAB IV; masuk ke Daftar Isi setelah F9. Tabel 3.17 (perangkat keras) & 3.18 (perangkat lunak) di-*paste* dari HTML di `documents/table/`.
- [ ] T4 & T5: Daftar Pustaka memuat Zhang 2016 (MTCNN) dan entri Hu 2018 sudah 3 penulis.
- [ ] Re-render PDF; pastikan tidak ada nomor persamaan/gambar/tabel yang rusak.
