# WORD Readiness Audit — BAB I–V + Abstrak (literal check)

**Docx:** REVISI V1 (live OneDrive, mod 2026-06-17 16:15) · **Metode:** ekstraksi `document.xml` + scan red-flag + cross-check plan & /analyze.

> **Verdict ringkas:** Substansi **matang** dan sebagian besar revisi penguji **sudah masuk** (hipotesis, 3 teori baru, padatan Cross-GAN, sitasi bersih, "Error! Bookmark" hilang, TOC page-number normal). Yang menahan status "final" adalah **placeholder gambar BAB IV** dan **judul yang belum diganti**. Selebihnya perbaikan kecil.

---

## ✅ Sudah beres (review GPT penguji rupanya pada versi lama)

| Item (dikhawatirkan penguji) | Status di docx 16:15 |
|---|---|
| "DAFTAR PUSTAKA … Error! Bookmark not defined" | **0 kemunculan** — sudah hilang ✓ |
| TOC angka aneh (1049/547/758) | Hilang; page number normal (1, 6, 64, 101, 115) ✓ |
| Hipotesis eksplisit | **Sudah ada** subbab "Hipotesis Penelitian" (H1/H0) + payoff "hipotesis nol" 3× ✓ |
| 3 teori tambahan (phase, freq-bias, domain) | Masuk, sitasi [25]–[30],[46] tepat ✓ |
| Sitasi orphan/dangling | **48 sumber, 48 tersitasi, 0 orphan, 0 dangling** ✓ |
| Heading BAB ("BAB I" + break + "PENDAHULUAN") | Benar (ada `<w:br/>`) ✓ |
| Abstrak | ID 167 kata, EN 181 kata (≤200 ✓), 1 paragraf, 5 kata kunci, framing jujur ✓ |
| 4 perbaikan kalimat (§A/§C/§E + §B) | Diterapkan ✓ |

---

## 🔴 BLOCKER (membuat dokumen terlihat "belum final")

### 1. Placeholder gambar BAB IV (paling fatal)
Masih ada teks mentah:
- **`[MASUKKAN GAMBAR 4.6]`** — **STALE**: Gambar 4.6 ("Tren AUC terhadap ukuran sampel") **sudah ada gambar + caption-nya** di tempat lain. Placeholder ini sisa lama → **HAPUS**.
- **`[MASUKKAN GAMBAR 4.9]`** dan **`[MASUKKAN GAMBAR 4.10]`** — **GENUINELY MISSING**: tidak ada caption 4.7/4.8/4.9/4.10, dan teks 4.2.4 merujuk "Gambar 4.10" (kurva pelatihan). Ini gambar **Confusion Matrix** + **dinamika/kurva pelatihan** (subbab "Confusion Matrix dan Dinamika Pelatihan"). Inilah blocker ROC/CM yang tertunda.

**Aksi:** generate CM + training-curve (mis. `make_roc_cm.py` / log training), sisipkan, beri caption, dan **renumber** agar berurutan (4.7, 4.8) sesuai handoff. Hapus placeholder stale 4.6.

> Catatan: Gambar 4.1–4.6 **semua sudah tertanam** (image-before caption = True). Jadi yang kurang hanya CM + kurva pelatihan.

### 2. Judul masih "Metode Peningkatan…" (narasi tak sinkron)
- Body memuat **"Metode Peningkatan…" 1×**, **"Studi Komparatif" 0×**.
- Rumusan Masalah sudah komparatif (RM1 penurunan spasial, RM2 FFT memperkecil penurunan, RM3 kontribusi tiap komponen) dan hasil = negatif. Judul lama ("Peningkatan") **bertentangan** dengan isi.
- **Keputusan tim + pembimbing** (ganti judul cover/halaman pengesahan/header). Usulan: *"Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet–FFT terhadap Model Domain Tunggal"*.

---

## 🟡 Perlu diperbaiki (kecil, cepat)

### 3. TOC: prefix auto-number "1. BAB I"
TOC menampilkan **"1.BAB I PENDAHULUAN", "2.BAB II …", "3.BAB III …"** dst. Angka "1./2./3." adalah **auto-number Heading1** yang menumpuk dengan teks "BAB I". Pedoman: judul bab cukup "BAB I" (tanpa "1."). **Aksi:** matikan penomoran otomatis pada style Heading1 (atau hapus numbering), lalu Update Fields.

### 4. Caption gambar dengan "()" kosong (2 tempat)
- **Gambar 4.3** "…pada FFPP dan CDF **()**" — kurung kosong (bukan math).
- **Gambar 4.5** "…per model dan arah pelatihan **()**" — kurung kosong.
Kemungkinan dimaksudkan "(n = 750)" atau keterangan lain. **Isi atau hapus kurung kosongnya.**
*(Catatan: "()" lain di BAB II/III — ColorJitter, FreqCNN, loss — semuanya berisi OMML math, render benar di Word, bukan masalah.)*

### 5. Typo
- **BAB I:** "**Sebagai besar** generator deepfake gagal mereplikasi…" → "**Sebagian besar**".
- **Daftar Pustaka [12] (Tan et al.):** nama "Y. **Zaho**" → "Y. **Zhao**" (perbaiki di Manage Sources lalu Update Fields).

### 6. (Opsional) 3 tanda "—" berdiri sendiri di BAB III
Kemungkinan sel tabel "tidak berlaku" (N/A). Verifikasi sekilas; bila itu N/A tabel, biarkan.

---

## 🟢 Status per bagian (literal)

- **Abstrak (ID+EN):** OK. *(Opsional: pemisah kata kunci pakai `;` — konvensional, boleh dibiarkan atau ganti koma.)*
- **BAB I:** Rumusan/Tujuan/Manfaat/Hipotesis lengkap & komparatif. Perlu: fix typo (#5), sinkron judul (#2).
- **BAB II:** Teori tambahan masuk, sitasi bersih. *Pertimbangan penguji:* Spectral Distortions (5 sub-subbab) + Analisis Citra/Video **belum dipadatkan** (sengaja dibiarkan). Penguji minta pangkas 15–25%; pemangkasan Dropoff/Periodic/Warping/Cross-GAN sudah memenuhi sebagian. Bila penguji menekan lagi, padatan sisa sudah siap di `REVISI_BAB_II_Padatan_2026-06-17.md`.
- **BAB III:** Bersih (math "()" semua benar). Cek "—" (#6).
- **BAB IV:** **Blocker gambar (#1)** + caption "()" (#4). Narasi & tabel hasil OK, payoff hipotesis (H-2) masuk.
- **BAB V:** Kesimpulan + payoff H0 (H-3) + Saran (termasuk adaptasi domain) lengkap.

---

## 🧭 Pertimbangan lebih dalam (yang penguji kemungkinan tanyakan — bukan soal WORD, tapi siapkan)

1. **Uji signifikansi statistik** — 3 seed (mean±std) belum diuji (paired t-test/Wilcoxon). Untuk S1 masih lolos, tapi penguji menyebutnya. Opsi: tambahkan uji deskriptif/non-parametrik, atau siapkan jawaban "dibahas deskriptif" (sudah konsisten dengan caveat hipotesis).
2. **Ablation SE-gating** — belum ada hybrid-tanpa-SE vs hybrid-dengan-SE. SE "dijual" sejak awal. Siapkan jawaban atau tambahkan baris ablation bila sempat.
3. **Frame-level only** — keterbatasan diakui (sudah di Saran). Siapkan jawaban "kenapa tak temporal".
4. **Frequency branch lemah (AUC 0,55–0,59)** — apakah domain freq buruk atau FreqCNN kurang kuat? **Sudah terjawab** lewat teori baru (fase dibuang, bias CNN) di 4.2.4. Kuat.

---

## Urutan tindakan disarankan
1. **Sisipkan gambar CM + kurva pelatihan** (4.9→4.7, 4.10→4.8), hapus placeholder stale [4.6]. *(blocker)*
2. **Ganti judul** ke versi komparatif (cover, pengesahan, header). *(keputusan pembimbing)*
3. Matikan auto-number "1." pada Heading1 (TOC). 
4. Isi/hapus "()" caption 4.3 & 4.5. 
5. Fix typo "Sebagai besar" + "Zaho".
6. **Update Fields** (Ctrl+A → F9) → TOC, Daftar Gambar, Daftar Pustaka.
</content>
