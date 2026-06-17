# PLAN — Revisi Sesuai Catatan Penguji (BAB II ramping · Hipotesis · Paragraf Evaluasi · Sitasi tak terpakai)

**Tanggal:** 2026-06-17 · **docx acuan:** OneDrive `REVISI V1 …docx` (mod 13:50)
**Cakupan:** (1) rapikan paragraf "Metode Evaluasi Model"; (2) pangkas BAB II ~15–25% (buang teori tak dipakai); (3) bersihkan sitasi tak terpakai; (4) tambah hipotesis eksplisit.
**Prinsip:** **tidak ada yang dihapus tanpa bukti**. Setiap pemangkasan sudah diaudit terhadap **seluruh dokumen (BAB I–V) + kode (`src/`, `scripts/`)**.

---

## 0. METODE AUDIT (bukti agar bisa direview)

Audit dijalankan atas `word/document.xml` (semua paragraf, semua CITATION field) + grep kode:

1. **Peta konsep per-BAB** — menghitung kemunculan tiap konsep di BAB I/II/III/IV.
2. **Peta sitasi → lokasi** — tiap CITATION tag dipetakan ke semua subbab tempat ia dipakai (semua BAB).
3. **Peta kode** — grep konsep di `deepfake_hybrid/src` & `scripts`.
4. **Bibliografi** = Word **BIBLIOGRAPHY field**; **39 tag tersitasi** vs **45 entri Daftar Pustaka**.

**Hasil kunci (jadi dasar keputusan):**

| Konsep | BAB I | BAB II | BAB III | BAB IV | Kode | Verdict |
|---|---|---|---|---|---|---|
| Spectral Dropoff | 0 | 22 | 0 | 0 | 0 | hanya background → **pangkas** |
| Periodic Noise | 0 | 44 | 0 | 0 | 0 | hanya background → **pangkas** |
| Warping | 0 | 42 | 0 | 0 | 0 | hanya background → **pangkas** |
| Cross-GAN | 0 | 42 | 0 | 0 | 0 | hanya background → **gabung/pangkas** |

→ Keempatnya **tidak pernah dirujuk di luar BAB II** dan **tidak pernah diukur/dihitung di kode**. Aman dipangkas tanpa merusak rujukan silang.

---

## 1. PERBAIKAN PARAGRAF "METODE EVALUASI MODEL" (BAB III) — kecil, cepat

**Masalah:** (a) kalimat rumpang; (b) kalimat penutup menggantung & menyesatkan (menjanjikan "metrik tambahan cross-dataset" padahal subbab berikutnya hanya "Contoh Perhitungan Metrik" — Δ sudah dipindah ke *Desain Eksperimen → Evaluasi Cross-Dataset*).

**Ganti seluruh paragraf dengan:**

> Evaluasi model dilakukan pada frame-frame dari set pengujian (*test set*) yang telah dipisahkan pada level video untuk mencegah kebocoran data. Metrik evaluasi yang digunakan, **yaitu** *accuracy*, *precision*, *recall*, *F1-score*, dan AUC-ROC beserta *confusion matrix*, telah didefinisikan secara detail pada BAB II. AUC digunakan sebagai metrik utama untuk seleksi model dan *early stopping* karena sifatnya yang independen terhadap *threshold*. Selain evaluasi pada *threshold* tetap (θ = 0,5), penelitian ini juga menghitung *threshold* optimal menggunakan statistik J Youden (J = TPR − FPR) yang memberikan keseimbangan optimal antara sensitivitas dan spesifisitas. **Sebagai ilustrasi penerapan metrik-metrik tersebut, berikut disajikan contoh perhitungannya dari sebuah confusion matrix.**

*(Hapus kalimat lama "Pada bagian ini dibahas metrik tambahan yang spesifik untuk desain eksperimen silang dataset.")*

---

## 2. PEMANGKASAN BAB II (~15–25%)

Target: buang teori yang **tidak pernah dioperasionalkan**, pertahankan yang menopang metode. Estimasi penghematan: ~4–5 halaman dari BAB II (≈15–18%).

| Subbab BAB II | Aksi | Alasan (berbukti) |
|---|---|---|
| **Spectral Dropoff** (+sub-subbab) | **HAPUS** | 0× di BAB I/III/IV & kode; tidak pernah dihitung |
| **Periodic Noise dalam Domain Frekuensi** (+sub) | **HAPUS** | idem; tidak pernah diukur |
| **Warping dalam Domain Frekuensi** (Low/High-Freq) | **HAPUS** | idem; tidak pernah diukur |
| **Cross-GAN pada Deteksi Deepfake** (+sub) | **GABUNG** → 1–2 paragraf di "Cross Dataset Generalization" | studi ini *cross-dataset*, bukan cross-GAN; konsep 0× di luar BAB II |
| **Spectral Distortions dalam Deteksi Deepfake** (5 sub-subbab) | **PADATKAN** → 1 subbab ringkas (pertahankan inti: artefak GAN di frekuensi menengah–tinggi yang menjustifikasi *high-pass filter*) | sebagian background; inti tetap perlu utk menjustifikasi high-pass di BAB III |
| Frequency Domain Analysis, FFT, XceptionNet, CNN/Depthwise, SE, Optimasi, Metrik, Dataset, Cross Dataset Generalization, GAN/upsampling (Durall, Odena) | **PERTAHANKAN** | dipakai langsung dalam metode/eksperimen |
| *(opsional)* Analisis Citra / Analisis Video | **boleh dipadatkan** | agak tipis; menjustifikasi pendekatan frame-level (boleh diringkas, bukan dihapus) |

> **Penting:** saat menghapus, **jaga justifikasi *high-pass filter*** (BAB III memakai Gaussian high-pass). Inti "artefak deepfake termanifestasi di frekuensi menengah–tinggi" dipertahankan di "Spectral Distortions" yang dipadatkan — tidak perlu Dropoff/Periodic Noise/Warping yang rinci.

---

## 3. PEMBERSIHAN SITASI (Pedoman 4.5.5.d: setiap entri Daftar Pustaka wajib disitasi)

### 3a. Referensi TAK PERNAH disitasi → **HAPUS dari sumber/Daftar Pustaka**
**KOREKSI (audit ulang \m-aware dari `customXml/item1.xml`):** 45 sumber, **41 tersitasi** → hanya **4 entri orphan**. *(Catatan: audit awal keliru menandai Aduwala/Dai/Güera sebagai orphan — ternyata KETIGANYA DISITASI lewat sitasi gabungan `\m`, mis. `CITATION Ran22 \m Adu21`. JANGAN hapus ketiganya.)*

| Daftar Pustaka | Tag | Status |
|---|---|---|
| [31] Stack Overflow, *What Does the Fourier Transform of an Image Show?* | Wha | ❌ tak disitasi → hapus |
| [32] Easton, *Fundamentals of Digital Image Processing* | Eas10 | ❌ tak disitasi → hapus |
| [45] Robbins & Monro, *A Stochastic Approximation Method* | Rob51 | ❌ tak disitasi → hapus |

✅ **TETAP (terbukti disitasi via `\m`):** [20] Aduwala (Adu21), [22] Dai (Dai21), [27] Güera (Güe18).

### 3b. Referensi yang jadi yatim AKIBAT pemangkasan BAB II
- **[29] Oppenheim et al., *Discrete-Time Signal Processing* (tag Opp89)** — **HANYA** disitasi di "Periodic Noise". Bila Periodic Noise dihapus → jadi orphan → **hapus juga**.
- **Semua sitasi lain** di subbab yang dipangkas **TETAP DIPERTAHANKAN** karena dipakai di tempat lain. Bukti:
  - Spectral Dropoff: Dur, Gon18, Rao25, Zha19 → semua dipakai di subbab lain.
  - Warping: Afc, Dur, Has23, Ode16, Ran22, Rös19 → semua dipakai di subbab lain.
  - Cross-GAN: Ala, Dur, Haq, Kar18, Kim25, Lao25, Ran22, Rös19 → semua dipakai di subbab lain (mis. Kar18 di Spectral Distortions/Analisis Citra; Kim25 di Spectral Distortions; Lao25 di Frequency Domain Analysis/Pendekatan Deteksi).
  - Periodic Noise: selain Opp89, semuanya (Ala, Cha21, Dur, Gon18, Has23, Lao25, Mej, Ode16, Qia20, Tan24, Wik18, Zha19) dipakai di tempat lain.

### 3c. Total yang dihapus dari Daftar Pustaka
**4 entri (pasti):** [29] Oppenheim, [31] Stack Overflow, [32] Easton, [45] Robbins.
**+1 kondisional:** [25] Kim et al. (temporal frequency) — **hanya jika** padatan Spectral Distortions/Cross-GAN membuang temporal (studi ini *frame-level*); lihat `REVISI_BAB_II_Padatan_…` §5.
Setelah dihapus, **Update Field** pada Daftar Pustaka + seluruh sitasi (Word auto-renumber `[N]`).

> ⚠️ Verifikasi akhir di Word: gunakan *References → Manage Sources* — sumber yang tak ada di "Current List" sitasinya akan terlihat; pastikan ketujuh entri ini memang tanpa sitasi sebelum dihapus dari master list.

---

## 4. HIPOTESIS EKSPLISIT (perkuat BAB IV/V)

**Letak:** BAB I, subbab baru **"1.x Hipotesis Penelitian"** setelah Tujuan (atau awal BAB III). **Framing:** dirumuskan sbg yang **diuji**, lalu dilaporkan jujur (hasil negatif → H₀ tak ditolak).

**Teks siap-tempel:**

> **Hipotesis Penelitian**
> Berdasarkan rumusan masalah, penelitian ini menguji hipotesis berikut:
> - **H₁:** Penambahan analisis domain frekuensi melalui arsitektur *hybrid* XceptionNet–FFT menghasilkan kemampuan generalisasi *cross-dataset* yang lebih baik dibandingkan model domain spasial murni (XceptionNet).
> - **H₀:** Tidak terdapat peningkatan generalisasi *cross-dataset* yang berarti dari penambahan analisis domain frekuensi (performa *hybrid* ≤ spasial).

**Tindak lanjut di BAB IV/V:** tambahkan 1–2 kalimat di Ringkasan Jawaban RM (4.2.6) & Kesimpulan (5.1): *"Berdasarkan hasil (in-dataset hybrid < spasial; cross-dataset manfaat hanya parsial dan bergantung arah), **H₀ tidak dapat ditolak** — fitur frekuensi belum terbukti meningkatkan generalisasi secara konsisten."*

> ⚠️ Karena hanya 3 *seed* (mean±std), bahas "berarti/signifikan" secara **deskriptif** (selisih kecil, std tumpang-tindih). Jangan klaim "signifikan secara statistik" tanpa uji formal.

---

## 5. URUTAN EKSEKUSI & DAMPAK

1. **Paragraf evaluasi (Bagian 1)** — kecil, langsung.
2. **Hipotesis (Bagian 4)** — tambah 1 subbab BAB I + 2 kalimat BAB IV/V.
3. **Pangkas BAB II (Bagian 2)** — hapus/gabung/padatkan 4–5 subbab.
4. **Bersihkan sitasi (Bagian 3)** — hapus 7 entri orphan dari *Manage Sources* → Update Fields seluruh dokumen.
5. **Update otomatis:** Ctrl+A → F9 (refresh nomor sitasi `[N]`, Daftar Pustaka, Daftar Isi/Gambar/Tabel, penomoran SEQ).

**Dampak penomoran:** sitasi `[N]` akan ter-renumber otomatis (BIBLIOGRAPHY field). Penomoran subbab BAB II ikut bergeser (hapus subbab) — Heading auto-number Word menangani; cek Daftar Isi.

**Yang TIDAK berubah:** hasil eksperimen (BAB IV), persamaan, value (sudah final), gaya sitasi (tetap IEEE `[N]` per Pedoman 4.5.5).

---

## Ringkasan checklist
- [ ] Ganti paragraf "Metode Evaluasi Model" (Bagian 1)
- [ ] Tambah subbab Hipotesis di BAB I + jawaban H₀ di BAB IV/V (Bagian 4)
- [ ] Hapus subbab BAB II: Spectral Dropoff, Periodic Noise, Warping; gabung Cross-GAN; padatkan Spectral Distortions (Bagian 2)
- [ ] Hapus 7 referensi orphan: [20],[22],[27],[29],[31],[32],[45] (Bagian 3)
- [ ] Update Fields seluruh dokumen + cek Daftar Isi/Pustaka
