# Revisi v3 — Perbaikan Nomor Sitasi, Sinkronisasi Kode, dan Koreksi Faktual

**Tanggal:** 2026-06-02 21:00
**Dokumen sasaran:** `.docx` OneDrive (tersimpan 2 Jun 20:31, **setelah F9**)
**Status verifikasi:** sudah saya extract ulang dan cek — **F9 BELUM menyelesaikan masalah nomor sitasi.**
**Cara pakai:** setiap tindakan = **(LOKASI: teks-jangkar untuk dicari)** + **UBAH DARI → MENJADI**.

---

## ⏱️ STATUS PROGRES (update 2026-06-02 21:28, setelah edit Anda)

| Item | Status | Catatan |
|---|---|---|
| **TEMUAN 0** Nomor sitasi | ✅ **BERES** | IEEE→APA→IEEE berhasil. Rössler=[7], Durall=[8], Zhang=[9], Alam=[13], Qian=[11], Hasanaath=[16], Li=[18], Rana=[14], Odena=[21] — semua benar |
| **A1** label smoothing | ⚠️ **SEBAGIAN** | Kalimat utama ✅ (α=0,05 aktif), tetapi **contoh perhitungan masih "α=0" & pakai α=0,02** → lihat A1-FIX di bawah |
| **A2** patience | ✅ **BERES** | 12 epoch (2 tempat + tabel) |
| **A3** warmup | ⚠️ **SEBAGIAN** | Teks utama ✅ (3 epoch, total_iters=3, T_max epochs−3), tetapi **narasi kurva per-epoch masih warmup=2** → lihat A3-FIX di bawah |
| **A4** dropout hybrid | ❌ **BELUM** | Masih `Dropout(0,3)` ×2 di Classifier Head — ubah ke `0,5` |
| **A5** FreqCNN base_channels | ❌ **BELUM** | Masih base_channels=32, [32,64,128,256,256], ~700K, judul Tabel 3.5 "32" |
| **A6** high-pass filter | ✅ **BERES** | Subbab "Magnitude Spectrum, High-Pass Filtering, Log Scaling" + β=0,15 sudah ada |
| **A7** grup LR ke-3 | ✅ **BERES** | "5×10⁻⁵ (base×0,25)" untuk cabang frekuensi sudah ada |
| **A8** Welford | ✅ **BERES** | Kata "Welford" sudah hilang |

**Sisa yang harus dikerjakan:** A1 (contoh — teks di A1-FIX), A3 (narasi di A3-FIX), **A4** (dropout 0,5), **A5** (paste tabel/teks base_channels 64).

### ⚠️ A5-SISA — Cek 21:58: FreqCNN (3.4.2) sudah, tapi DAMPAK ke Hybrid + tabel BELUM

Bagian 3.4.2 (paragraf + Tabel 3.5 + "~4,2 juta") **sudah ✅**. Tetapi nilai turunan di **subbab 3.4.3 dan tabel** masih nilai lama (base 32). Perbaiki 8 titik berikut:

**Subbab 3.4.3 (Cabang Frekuensi / Proyeksi):**
1. **CARI:** *"Output berupa vektor fitur **berdimensi 256** (pada konfigurasi..."* → **berdimensi 512** (base_channels=64).
2. **CARI:** *"...sedangkan cabang frekuensi hanya **256**, dengan rasio **8:1**..."* → **512**, rasio **4:1**.
3. **CARI (persamaan 3.24):** *"...dan **Wf∈R²⁵⁶ˣ²⁵⁶** adalah matriks bobot proyeksi..."* → **Wf∈R²⁵⁶ˣ⁵¹²**. (Ws∈R²⁵⁶ˣ²⁰⁴⁸ tetap.)

**Tabel 3.6 (Perbandingan Arsitektur):**
4. Baris **"Dimensi fitur"**: kolom Frequency (FreqCNN) **256** → **512**. (Kolom Hybrid "256 + 256 = 512 (terproyeksi)" tetap — itu setelah proyeksi.)
5. Baris **"Total parameter"**: Frequency **~700 ribu** → **~4,2 juta**; Hybrid **~23,8 juta** → **~27,7 juta**. (Spatial ~22,8 juta tetap.)

**Tabel 3.7 (Dimensi Fitur per Komponen):**
6. Baris **"FreqCNN backbone"**: Dimensi Output **256** → **512**.
7. Baris **"Proyeksi frekuensi"**: Dimensi Input **256** → **512** (jadi "512 → 256").

**Tabel 3.10 / ringkasan hyperparameter:**
8. **CARI:** *"FreqCNN depth 5 ... **~700K parameter**"* → **~4,2 juta parameter**.

> Catatan: Daftar Isi & PAGEREF masih menampilkan "base_channels = 32" untuk judul Tabel 3.5 — itu hanya cache TOC, akan benar setelah **Ctrl+A → F9** (caption asli di body sudah "base_channels = 64").

**Artefak yang sudah saya generate (siap pakai):**
- **Tabel 3.5 (base_channels=64):** `documents/table/tabel_3_5_arsitektur_freqcnn.html` — sudah diperbarui (FreqBlock 1–5 dimensi & param baru, FC1 512→256, total ~4,2 juta). Buka di browser → Copy Table → paste ke Word menggantikan Tabel 3.5 lama.
- **Kurva LR (A3):** `documents/media_v2/gambar_3_10_lr_schedule.png` — di-regenerate untuk **warmup 3 epoch** (skrip `deepfake_hybrid/scripts/make_lr_schedule_figure.py` mereplikasi persis `SequentialLR` dari `train.py`). Nilai per-epoch terkonfirmasi: 1→2e-5, 2→8e-5, 3→1,4e-4, 4→2e-4 (puncak), lalu cosine → 1e-6. Ganti gambar kurva LR lama di docx dengan file ini.

---

### A1-FIX — Contoh perhitungan label smoothing (VERIFIED dengan kode)

Kode `train.py:109`: `targets = targets*(1−α) + α*0.5`. Contoh saat ini memakai α=0,02 dan menyebut "α=0" (keduanya salah karena config final = 0,05). **Ganti seluruh blok contoh** agar konsisten α=0,05:

**CARI:** *"...contoh perhitungan BCEWithLogitsLoss dengan label smoothing **α=0,02 (walaupun pada konfigurasi akhir α=0**, contoh ini menunjukkan mekanisme...)"* dan persamaan (3.33)–(3.35) di bawahnya.

**UBAH MENJADI (verified):**
> Sebagai ilustrasi, berikut contoh perhitungan BCEWithLogitsLoss dengan *label smoothing* α=0,05 (nilai yang digunakan pada konfigurasi akhir), untuk satu sampel dengan label target *y*=1 (fake) dan logit *z*=2,5.
>
> **Label smoothing** (3.33): y' = y·(1−α) + α·0,5 = 1·(1−0,05) + 0,05·0,5 = 0,95 + 0,025 = **0,975**
>
> **Sigmoid** (3.34): σ(2,5) = 1 / (1 + e⁻²·⁵) = 1 / 1,0821 = **0,924**
>
> **Loss** (3.35): L = −[ y'·ln(σ) + (1−y')·ln(1−σ) ]
> = −[ 0,975·ln(0,924) + 0,025·ln(0,076) ]
> = −[ 0,975·(−0,0790) + 0,025·(−2,577) ]
> = −[ −0,0770 + (−0,0644) ]
> = −(−0,1415) = **0,1415**
>
> Nilai *loss* yang rendah (0,1415) menunjukkan prediksi model (probabilitas 0,924 untuk *fake*) sudah mendekati label target ter-*smooth* (0,975).

> Verifikasi angka: y'=0,975; σ(2,5)=0,924; ln(0,924)=−0,0790; ln(0,076)=−2,577; L≈0,1415. (Semua sudah saya hitung ulang.)

---

### A3-FIX — Narasi kurva LR (regenerated untuk warmup=3, VERIFIED dengan kode)

Kode `train.py:247-258`: `SequentialLR([LinearLR(start=0.1, end=1.0, total_iters=3), CosineAnnealingLR(T_max=epochs−3, eta_min=1e-6)], milestones=[3])`. Jadi warmup epoch 1–3, cosine mulai epoch 4. Per-epoch saat ini masih versi lama (Epoch 2 = 1,0×base; Epoch 3–30 cosine). **Ganti:**

**CARI (2 tempat):**
1. *"Cosine annealing (**epoch ke-3 hingga selesai**), ... CosineAnnealingLR(T_max=max(epochs-3, 1)..."*
2. Blok "Kurva learning rate untuk pelatihan 30 epoch:" dengan rincian Epoch 1 / Epoch 2 / Epoch 3-30.

**UBAH MENJADI (verified):**
> *Cosine annealing* (**epoch ke-4 hingga selesai**), *learning rate* diturunkan secara halus mengikuti kurva kosinus dari nilai *base* menuju 1×10⁻⁶. `CosineAnnealingLR(T_max=max(epochs−3, 1), eta_min=1e-6)`.
>
> Kurva *learning rate* untuk pelatihan 30 *epoch* (warmup 3 *epoch* selaras dengan *backbone freeze*):
> - **Epoch 1:** LR = 0,1 × base = 2 × 10⁻⁵
> - **Epoch 2:** LR = 0,4 × base = 8 × 10⁻⁵
> - **Epoch 3:** LR = 0,7 × base = 1,4 × 10⁻⁴
> - **Epoch 4:** LR = 1,0 × base = 2 × 10⁻⁴ (puncak; *cosine decay* dimulai)
> - **Epoch 4–30:** *Cosine decay* dari 2 × 10⁻⁴ menuju 1 × 10⁻⁶

> Catatan: LinearLR(total_iters=3) menaikkan faktor secara linear 0,1 → 0,4 → 0,7 pada epoch 1–3, lalu SequentialLR beralih ke cosine pada epoch 4 yang dimulai dari nilai *base* (2×10⁻⁴). (Diverifikasi terhadap perilaku `SequentialLR` + `LinearLR` di kode.)

---

## 🔴 TEMUAN 0 (PALING PENTING) — Nomor sitasi in-text masih salah setelah F9

### Diagnosis (terverifikasi)
Saya bandingkan `.docx` Anda **setelah F9** vs sebelumnya: **nomor `[N]` in-text tidak berubah sama sekali (byte-identik).** Diagnosis teknis:

- Sitasi Anda adalah **fitur Citation native Word** (`CITATION <Tag>`), dengan Daftar Pustaka berupa **field BIBLIOGRAPHY** (sumber tersimpan di `customXml/item1.xml`). Bukan Mendeley/Zotero.
- **Daftar Pustaka [1]–[45] SUDAH benar** (F9 memperbaruinya): [7]=Rössler, [8]=Durall, [9]=Zhang, [13]=Alam, [14]=Rana, [16]=Hasanaath, [17]=Luo, [18]=Li/Celeb-DF, [19]=Chadha, [21]=Odena.
- **TAPI field sitasi in-text menyimpan nomor lama (basi).** Tag-nya benar, hanya angka tampilannya yang ketinggalan. Contoh terverifikasi (tag → angka yang TAMPIL → seharusnya):

| Sumber (tag) | Tampil sekarang | Seharusnya | Yang tampil itu sebenarnya |
|---|---|---|---|
| Rössler (`Rös19`) | **[19]** (17×) | **[7]** | [19] = Chadha |
| Durall (`Dur`) | **[7]** (15×) | **[8]** | [7] = Rössler |
| Zhang-GAN (`Zha19`) | **[8]** (11×) | **[9]** | [8] = Durall |
| Alam (`Ala`) | **[9]** (10×) | **[13]** | [9] = Zhang |
| Qian (`Qia20`) | **[13]** (8×) | **[11]** | [13] = Alam |
| Rana (`Ran22`) | **[10]** (11×) | **[14]** | [10] = Giudice |
| Hasanaath (`Has23`) | **[18]** (10×) | **[16]** | [18] = Li/Celeb-DF |
| Odena (`Ode16`) | **[16]** (4×) | **[21]** | [16] = Hasanaath |
| Li/Celeb-DF (`LiY20`) | **[35]** (3×) | **[18]** | [35] = Akinrogunde |

(Yang sudah benar: Afchar→[4], Chollet→[6], Hu→[36], Zhang-MTCNN→[44].)

### Kenapa F9 gagal & CARA MEMPERBAIKI (lakukan di Word)
Plain **Ctrl+A → F9 tidak me-regenerasi nomor Citation native Word** (ia hanya memperbarui field bibliografi/TOC, bukan angka sitasi in-text). Yang memaksa regenerasi total:

**Metode 1 — Ganti style bolak-balik (PALING ANDAL):**
1. Tab **References** → grup **Citations & Bibliography** → dropdown **Style**.
2. Ganti ke style lain (mis. **APA**), tunggu sebentar.
3. Ganti **kembali ke IEEE**. → Word me-renumber **semua** sitasi in-text + Daftar Pustaka secara konsisten.
4. Lalu **Ctrl+A → F9** untuk Daftar Isi, nomor gambar/tabel/persamaan.

**Metode 2 — bila Metode 1 tidak mempan:** klik pada area Daftar Pustaka → muncul tombol **"Update Citations and Bibliography"** → klik.

**Metode 3 — bila masih ada yang bandel:** klik field sitasi yang salah → panah dropdown → **Update Field** per-citation (untuk sisa yang tidak ikut ter-regenerasi).

### CARA VERIFIKASI sesudahnya
Klik satu sitasi Rössler di teks → harus menunjukkan **[7]**, bukan [19]. Cek juga Durall → [8], Alam → [13]. Jika sudah, beri tahu saya — saya bisa cek ulang `.docx` untuk memastikan semua 307 field konsisten.

> **JIKA masih gagal setelah ketiga metode:** kemungkinan sebagian field "rusak"/ter-*unlink*. Simpan temuan ini; kirim `.docx` terbaru, saya akan petakan field mana saja yang masih salah satu per satu.

---

## 🔴 BAGIAN A — Sinkronisasi Kode (v4 belum masuk ke `.docx`)

Nilai di `.docx` masih versi lama dan **bertentangan dengan kode** yang menghasilkan BAB IV. Teks koreksi lengkap **sudah tersedia** di `documents/BAB_III_Tahapan_Pelaksanaan_v4.md` — di bawah saya beri lokasi + ubahan persis.

### A1 — Label smoothing (subbab 3.5.4)
**CARI:** *"Pada konfigurasi akhir yang digunakan dalam eksperimen ini, label smoothing **dinonaktifkan (α = 0)** untuk memaksimalkan sinyal pelatihan..."*
**UBAH MENJADI:** *"Pada konfigurasi akhir yang digunakan dalam eksperimen ini, label smoothing **diaktifkan dengan α = 0,05** sebagai regularisasi ringan untuk mencegah model menjadi terlalu percaya diri pada dataset berukuran kecil."*
> Kode: `config.yaml:17 label_smoothing: 0.05`. **Juga periksa** contoh perhitungan yang memakai α=0,02 — sesuaikan ke 0,05 atau beri keterangan bahwa nilai final adalah 0,05.

### A2 — Early stopping patience (subbab 3.5.8 + Tabel 3.10)
**CARI (2 tempat):** *"Kesabaran (patience): **10 epoch**..."* dan *"Penggunaan patience **10 epoch** memberikan waktu..."* serta baris Tabel 3.10 "Early stopping patience = **10**".
**UBAH:** semua **10** → **12**.
> Kode: `config.yaml:15 early_stop_patience: 12`.

### A3 — Linear warmup (subbab 3.5.3 + Tabel 3.10)
**CARI:** *"**Linear warmup (2 epoch)**, learning rate dinaikkan... **LinearLR(start_factor=0.1, end_factor=1.0, total_iters=2)**..."* dan narasi "Epoch 1... Epoch 2... Epoch 3–30 cosine", serta `T_max = max(epochs − 2, 1)`.
**UBAH:**
- "2 epoch" → **"3 epoch"**; `total_iters=2` → **`total_iters=3`**
- `T_max = max(epochs − 2, 1)` → **`T_max = max(epochs − 3, 1)`**
- Narasi kurva: warmup epoch 1–3, cosine epoch 4–30 (selaras dengan *backbone freeze* 3 epoch).
- Tabel 3.10 "LR warmup = 2 epoch" → **3 epoch**.
> Kode: `train.py:248` warmup 3, `:253` T_max epochs−3.

### A4 — Hybrid classifier dropout (subbab 3.4.3 "Classifier Head" + Tabel 3.8)
**CARI:** *"**Dropout(0,3)**, regularisasi pada representasi fusi..."* dan *"**Dropout(0,3)**, regularisasi tambahan."* (dua kemunculan di Classifier Head hybrid).
**UBAH:** kedua **Dropout(0,3)** → **Dropout(0,5)**.
> Kode: `hybrid_fusion.py:49,53` `nn.Dropout(0.5)`. ⚠️ JANGAN ubah Dropout(0,3) milik FreqCNN FC head (itu memang 0,3) maupun Dropout2d(0,2).

### A5 — FreqCNN base_channels (subbab 3.4.2.1 + Tabel 3.5 + Tabel 3.6/3.7/3.10)
**CARI:** *"Konfigurasi yang digunakan dalam penelitian ini adalah depth = 5 dengan **base_channels = 32**, menghasilkan progresi kanal **[32, 64, 128, 256, 256]**..."* dan judul "Tabel 3.5 ... **base_channels = 32**", dan "freq_base_channels (jumlah kanal awal, **default 32**)".
**UBAH:** ganti seluruh paragraf + tabel dengan versi **base_channels = 64** yang **sudah ditulis lengkap** di `BAB_III_Tahapan_Pelaksanaan_v4.md` baris 488–508. Ringkas perubahan nilai:
- base_channels 32 → **64**; progresi [32,64,128,256,256] → **[64,128,256,512,512]**
- feature_dim 256 → **512**; param FreqCNN ~700K → **~4,2 juta**
- **Tabel 3.5** (layer-by-layer): seluruh dimensi output & param diganti (lihat v4 baris 490–504): FreqBlock4 ~1.313.000; FreqBlock5 ~2.361.000; FC1 Linear(512→256).
- **Akibat ke Hybrid (3.4.3):** cabang freq 256 → **512**; rasio dimensi 8:1 → **4:1**; matriks proyeksi $W_f \in \mathbb{R}^{256\times256}$ → **$\mathbb{R}^{256\times512}$**; total param hybrid ~23,8 jt → **~27,7 jt**.
> Kode: `config.yaml:23 freq_base_channels: 64`. **Penting:** konfirmasi BAB IV memang dijalankan dengan 64 (komentar config "64 for face crops" + colab mengindikasikan ya).

### A6 — High-pass filter FFT (subbab 3.3.2.3) — TAMBAH, saat ini HILANG
`.docx` subbab 3.3.2 langsung dari magnitude → log1p, **tanpa** langkah high-pass. Kode (`fft_utils.py:9-33`) menerapkan *Gaussian high-pass mask* (β/cutoff = 0,15) **sebelum** log1p; jadi cache FFT = `log1p(|F|·H)`, bukan `log1p(|F|)`.
**TINDAKAN:** ganti subbab "Magnitude Spectrum dan Log Scaling" dengan versi **"Magnitude Spectrum, High-Pass Filtering, dan Log Scaling"** yang **sudah ditulis lengkap** di `BAB_III_Tahapan_Pelaksanaan_v4.md` baris 156–178. Intinya:
- Tambah **persamaan (3.4)**: $H(u,v) = 1 - \exp\!\left(-\frac{(u-u_c)^2+(v-v_c)^2}{2(\beta N)^2}\right)$, β=0,15, N=224.
- Magnitude terfilter: $|F'| = |F|\cdot H$.
- Log scaling jadi **(3.5)**: $M_{\log} = \log(1+|F'|)$.
- **Akibat:** semua persamaan setelah 3.4 lama **bergeser +1** (3.4→3.5, dst. hingga 3.37→3.38). Perbarui rujukan nomor & contoh perhitungan FFT (3.3.2.4) agar memakai $|F'|$.

### A7 — Differential LR: grup ke-3 (subbab 3.5.2 + Tabel 3.9)
**CARI:** Tabel 3.9 yang hanya mendaftar **2 grup** (backbone, head).
**UBAH:** tambahkan **grup ke-3 untuk model hybrid** = cabang frekuensi dengan LR = base × 0,25 = **5×10⁻⁵**. Jadi: backbone (2×10⁻⁵) / cabang freq (5×10⁻⁵) / head (2×10⁻⁴).
> Kode: `train.py:209-213`.

### A8 — Klaim "Welford" (subbab Normalisasi FFT)
**CARI:** *"...akumulasi online (metode **Welford**)..."*
**UBAH MENJADI:** *"...akumulasi satu-lintasan (penjumlahan nilai dan kuadrat / sum & sum-of-squares)..."*
> Kode: `compute_fft_cache.py:46-55` memakai sum/sum-sq sederhana, bukan Welford.

---

## 🔴 BAGIAN B — Koreksi Faktual (vs paper asli)

### B1 — Angka XceptionNet fabrikatif (subbab BAB II, paragraf perbandingan domain spasial)
**CARI:** *"...Rössler et al. ... melaporkan bahwa XceptionNet mencapai akurasi deteksi hingga **96,36%** pada dataset FaceForensics++, melampaui performa ResNet dan MesoNet..."*
**MASALAH:** angka **96,36% tidak ada** di paper Rössler (nilai asli: **99,26%** raw / 95,73% HQ / 81,00% LQ). Juga bertentangan dengan kalimat lain di tesis ("99,26%").
**UBAH:** "96,36%" → **"99,26% (pada FaceForensics++ tanpa kompresi / raw)"**.

### B2 — Salah label metrik AUC vs akurasi (subbab BAB II / latar belakang)
**CARI:** *"Pada benchmark FaceForensics++ tanpa kompresi, XceptionNet mencapai **99,26% AUC** dan melampaui ResNet-50 maupun MesoNet."*
**MASALAH:** 99,26% di Rössler adalah **accuracy/detection accuracy**, bukan AUC.
**UBAH:** "99,26% AUC" → **"akurasi deteksi 99,26%"**.

> **⚠️ Cek 22:07 — ada DUA kemunculan "99,26% AUC":**
> - (a) BAB II (subbab perbandingan domain) → **SUDAH diperbaiki** jadi "akurasi deteksi 99,26%". ✅
> - (b) **BAB I PENDAHULUAN** masih salah: *"...depthwise separable convolution memberikan efisiensi komputasi tanpa mengorbankan akurasi, dan dilaporkan mencapai **99,26% AUC** pada FaceForensics++ tanpa kompresi (Chollet; Rössler)"* → **UBAH "99,26% AUC" → "akurasi deteksi 99,26%"**. ❌ BELUM

### B3 — Durall "lima GAN" (subbab artefak frekuensi / Durall)
**CARI:** kalimat yang menyebut artefak konsisten pada *"**lima** arsitektur GAN"* (tag `Dur`).
**MASALAH:** Durall menguji **empat** varian GAN (DCGAN, DRAGAN, LSGAN, WGAN-GP).
**UBAH:** "lima" → **"empat"** (klaim konsistensi lintas-GAN tetap valid).

### B4 — Referensi Zhang MTCNN ada typo (Daftar Pustaka [44])
**CARI:** *"K. Zhang, Z. Zhang, Z. Li dan Y. Qiao, Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks **Kaipeng**, IEEE Signal Processing Letters, 2016."*
**UBAH MENJADI:** *"K. Zhang, Z. Zhang, Z. Li dan Y. Qiao, Joint Face Detection and Alignment using Multitask Cascaded Convolutional Networks, IEEE Signal Processing Letters, vol. 23, no. 10, hlm. 1499–1503, 2016."*
> Hapus kata **"Kaipeng"** (nama depan penulis yang nyasar ke judul). Edit di **Manage Sources** (References → Manage Sources → edit entri Zha16 → field Title), bukan di teks bibliografi (karena itu field).

---

## 🟠 BAGIAN C — Item Reviewer yang Masih Terbuka

### C1 — Rename subbab 2.20.1 (Pembanding 2, butir 6g)
**CARI:** heading **"2.20.1 Mengapa Cross-GAN Sulit"**
**UBAH MENJADI:** **"2.20.1 Faktor Penyebab Kesulitan Generalisasi Cross-GAN"**

### C2 — Sitasi pada setiap gambar & tabel BAB II (Pembanding 1, butir 6a)
**TINDAKAN:** telusuri setiap caption Gambar/Tabel di BAB II; pastikan ada sitasi sumber (mis. "(Rössler et al., 2019)"). Gambar arsitektur/teori yang diambil/diadaptasi dari paper **wajib** bersitasi. (Perlu cek manual per-caption.)

### C3 — Paragraf < 5 kalimat & subbab 1-paragraf (Pembanding 2, butir 6a & 6h)
**TINDAKAN:** (a) gabungkan/lengkapi paragraf yang < 5 kalimat; (b) subbab yang hanya 1 paragraf → ubah jadi poin (a, b / 1, 2). Perlu telaah manual menyeluruh BAB II–III.

### C4 — Contoh frame artefak di subbab 2.2.3 (Pembanding 2, butir 6b)
**TINDAKAN:** reviewer minta contoh frame artefak **spasial & frekuensi** di **2.2.3 (BAB II)**. Saat ini contoh ada di BAB III (Gambar 3.2 real/fake, Gambar 3.4 FFT). Pertimbangkan menautkan/menyalin contoh ringkas ke 2.2.3.

---

## URUTAN PENGERJAAN YANG DISARANKAN
1. **TEMUAN 0** dulu (ganti style IEEE→APA→IEEE) — perbaiki semua nomor sitasi. Verifikasi Rössler=[7].
2. **Bagian A** (A1–A8) — porting nilai v4 (sumber: `BAB_III_Tahapan_Pelaksanaan_v4.md`).
3. **Bagian B** (B1–B4) — koreksi faktual.
4. **Bagian C** — item reviewer tersisa.
5. Terakhir: **Ctrl+A → F9** (TOC, nomor gambar/tabel/persamaan) + simpan.
6. Kabari saya — saya cek ulang `.docx` untuk konfirmasi semua beres.

---

*Catatan: nilai kode diverifikasi langsung dari `config.yaml`, `src/`, `scripts/train.py`. Teks koreksi A5/A6 tersedia siap-salin di `documents/BAB_III_Tahapan_Pelaksanaan_v4.md` (baris dirujuk di atas). Diagnosis sitasi berdasarkan `customXml/item1.xml` (45 sumber, tanpa tag duplikat) + penyelarasan field `CITATION` ↔ teks tampil.*
