# REVISI BAB II — Padatan (Spectral Distortions · Cross-GAN · Analisis Citra/Video)

> Lanjutan plan `PLAN_Revisi_Penguji_…`. Draft **siap-tempel**, sitasi **(Nama, Tahun)** untuk memudahkan input (di Word jadi CITATION field → render `[N]`). Ganti seluruh subbab lama dengan versi padat ini.

---

## ✅ Verifikasi penghapusan (Spectral Dropoff / Periodic Noise / Warping)

| Cek | Hasil |
|---|---|
| Heading subbab masih ada? | ❌ Tidak — ketiganya sudah terhapus |
| Dirujuk di BAB III / IV / V? | **0×** (semua) — aman |
| Dipakai di kode/perhitungan? | **0×** di `src/` & `scripts/` |
| Sitasi yatim akibatnya | **Opp89 (Oppenheim, [29]) kini 0× tersitasi** → hapus dari Daftar Pustaka |

**Catatan (bukan masalah):**
- **Daftar Isi** masih menampilkan entri lama (Spectral Dropoff/Periodic Noise/Warping) sebagai `PAGEREF` basi → hilang otomatis setelah **Update Field** (Ctrl+A → F9) pada Daftar Isi.
- Konsep masih disebut **sambil lalu** di subbab lain yang dipertahankan (warping 8×, periodic noise 4×, spectral dropoff 1× — mis. "akibat *face warping*", "mendeteksi *periodic noise*"). Ini **bukan rujukan menggantung** (tidak ada "lihat subbab …"), jadi aman dibiarkan; opsional dirapikan bila ingin nol-sebutan.

---

## 1. Spectral Distortions → PADATKAN (≈800 → ≈230 kata, buang 5 sub-subbab)

**「GANTI seluruh subbab + 5 sub-subbab dengan ini」**

### Spectral Distortions dalam Deteksi Deepfake

Pendekatan deteksi berbasis domain frekuensi memanfaatkan *spectral distortions*, yaitu penyimpangan distribusi spektral yang muncul secara sistematis pada citra hasil manipulasi. Distorsi ini berakar pada keterbatasan model generatif berbasis CNN: operasi *up-convolution* (misalnya *transposed convolution*) dengan kernel yang tumpang-tindih tidak merata menghasilkan pola periodik dan *checkerboard artifacts* (Odena et al., 2016), sementara generator GAN gagal mereplikasi statistik frekuensi alami sehingga meninggalkan anomali pada komponen frekuensi menengah–tinggi yang dikenal sebagai *GAN fingerprints* (Durall et al., 2020; Zhang et al., 2019).

Anomali tersebut terutama termanifestasi sebagai ketidakseimbangan energi pada frekuensi tinggi (Qian et al., 2020; Mejri et al., 2021) serta perbedaan pada band frekuensi menengah yang berhubungan dengan tekstur wajah (Hasanaath et al., 2023; Alam et al., 2025). Karena bersifat algoritmik dan tidak bergantung pada pola piksel spesifik dataset, *spectral distortions* dilaporkan lebih *generalizable* lintas dataset dan lebih tahan terhadap kompresi dibanding fitur spasial murni (Tan et al., 2024).

Relevansi terhadap penelitian ini: integrasi FFT ke dalam arsitektur *hybrid* XceptionNet memberi akses langsung pada pola spektral tersebut, sehingga model dapat memanfaatkan petunjuk frekuensi sebagai pelengkap fitur spasial — landasan utama desain *hybrid* yang diuji, sekaligus menjustifikasi penggunaan *high-pass filter* yang menonjolkan komponen frekuensi menengah–tinggi pada tahap praproses (BAB III).

**「/GANTI」**

---

## 2. Cross-GAN → HAPUS subbab + sisipkan **1 KALIMAT** ke "Cross Dataset Generalization"

> **Koreksi pendekatan (telusur 2026-06-17):** rencana awal "tempel 2 paragraf di akhir" **dibatalkan**. Setelah menelusuri isi subbab "Cross Dataset Generalization" (9 paragraf), ternyata **~100% isi Cross-GAN sudah tercakup** di sana (domain shift metode-beda di P5, drop Δ di P2–P4, frekuensi/hybrid di P6/P8, relevansi di P1/P9). Menempel 2 paragraf = **redundan**, dan menaruhnya setelah paragraf penutup (P9) = **memecah alur**.

**「AKSI」**
1. **HAPUS** subbab Heading2 "Cross-GAN pada Deteksi Deepfake" + 4 sub-subbabnya (Faktor Penyebab, Indikator Evaluasi, Pendekatan untuk Meningkatkan, Relevansi).
2. **SISIPKAN 1 kalimat** di subbab "Cross Dataset Generalization", pada paragraf *domain shift* (paragraf yang diakhiri sitasi Zhang et al.), tepat setelah "…mudah terjebak pada *dataset-specific artifacts* (Zhang et al., 2019).":

> Kasus khusus dari *domain shift* ini dikenal sebagai *cross-GAN* (*cross-generator*), yaitu ketika model dilatih pada deepfake dari satu metode/arsitektur generatif lalu diuji pada metode lain yang belum pernah dilihat; karena perbedaan generator umumnya beriringan dengan perbedaan dataset, evaluasi *cross-GAN* dalam praktiknya menyatu dengan evaluasi *cross-dataset* (Rana et al., 2022; Rao & Uehara, 2025).

**「/AKSI」**

**Hasil akhir alur subbab:** P1 definisi → P2–P4 metrik Δ → **P5 domain shift + (1 kalimat) cross-GAN** → P6 frekuensi → P7 spasial → P8 hybrid → P9 penutup. Mulus, tanpa redundansi.

**Dampak sitasi:** Rana et al. (2022) & Rao & Uehara (2025) tertampung di kalimat ini (tidak yatim). Sitasi Cross-GAN lain (Alam et al., Durall et al., Rössler et al., Haq, Karras et al., Luo et al.) **semua sudah dipakai** di paragraf lain "Cross Dataset Generalization" atau subbab lain → aman. *(Kim et al. tetap kandidat yatim hanya jika padatan Spectral Distortions juga membuangnya — lihat §5.)*

---

## 3. Analisis Citra → PADATKAN (≈227 → ≈110 kata)

**「GANTI」**

### Analisis Citra

Analisis citra adalah proses mengekstraksi informasi penting (bentuk, tekstur, tepi, *noise*) dari citra digital melalui operasi matematis dan transformasi domain (Gonzalez & Woods, 2018). Pada deteksi deepfake, pendekatan domain spasial menyoroti anomali visual seperti ketidaksesuaian *blending* dan tekstur kulit, tetapi menjadi kurang efektif ketika kualitas manipulasi meningkat. Oleh karena itu analisis diperluas ke domain frekuensi yang mampu mengungkap *high-frequency artifacts* yang konsisten lintas arsitektur GAN dan tidak terlihat di domain spasial (Durall et al., 2020; Zhang et al., 2019). Kombinasi kedua domain inilah yang mendasari pendekatan *hybrid* pada penelitian ini.

**「/GANTI」**

---

## 4. Analisis Video → PADATKAN (≈213 → ≈95 kata)

**「GANTI」**

### Analisis Video

Analisis video memperluas analisis citra dengan mempertimbangkan hubungan temporal antar-*frame*. Namun, manipulasi deepfake umumnya dilakukan per-*frame*, sehingga artefaknya dapat dideteksi pada tingkat *frame* individual (Sabir et al., 2019). Penelitian ini menggunakan pendekatan *frame-level*: setiap *frame* diekstraksi dan diproses terpisah menggunakan CNN untuk fitur spasial dan FFT untuk fitur frekuensi, tanpa pemodelan temporal. Pendekatan ini memadai untuk menangkap artefak manipulasi sekaligus menjaga kompleksitas komputasi tetap rendah (Haq, 2021).

**「/GANTI」**

---

## 5. DAMPAK SITASI dari padatan (audit ulang `\m`-aware — DIKOREKSI)

> Koreksi: audit awal melewatkan sitasi gabungan `\m`. Setelah dibetulkan (cek `customXml/item1.xml`), beberapa sitasi yang dikira yatim ternyata aman.

Sitasi yang **dipertahankan** (terbukti masih dipakai di tempat lain): Odena, Durall, Zhang, Qian, Mejri, Hasanaath, Alam, Tan, Rana, Rao & Uehara, Rössler, Gonzalez, Sabir, Haq, **dan Karras [23]**.

| Ref | Lokasi (\m-aware) | Status pasca-padatan |
|---|---|---|
| **[23] Karras** | Analisis Citra, Cross-GAN, Spectral Distortions, **+ Deep Learning** | ✅ **AMAN** — masih dipakai di "Deep Learning" (tidak dipangkas) |
| **[25] Kim** (temporal frequency) | Cross-GAN, Spectral Distortions | ⚠️ **yatim** bila padatan membuang konten temporal (studi ini *frame-level*) → kandidat hapus |

**Daftar referensi yang dihapus — DEFINITIF:**
- **Pasti (4):** [29] Oppenheim, [31] Stack Overflow, [32] Easton, [45] Robbins.
- **Kondisional (1):** [25] Kim — hanya jika setuju membuang konten temporal saat padatan.
- ✅ **JANGAN hapus:** Aduwala [20], Dai [22], Güera [27], Karras [23] — keempatnya terbukti disitasi.

→ Setelah hapus: **Update Field** seluruh dokumen (renumber `[N]` + Daftar Pustaka + Daftar Isi).
