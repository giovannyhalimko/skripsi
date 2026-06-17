# PLAN — Teori yang Sebaiknya Ditambahkan ke BAB II

**Tanggal:** 2026-06-17 · **Pemicu:** catatan pembimbing (3 teori belum cukup kuat)
**Sitasi draft:** **(Nama, Tahun)** untuk memudahkan input ke Word (final → CITATION field render `[N]`).

---

## 0. Prinsip — kenapa ini BUKAN melanggar "pangkas teori"

Penguji minta dua hal yang **searah**, bukan bertentangan:
- **Pangkas** Spectral Dropoff / Periodic Noise / Warping → karena **0× payoff** (tak pernah dipakai menjelaskan hasil).
- **Tambah** Domain Adaptation / Frequency Bias / Phase → karena **menjelaskan temuan inti** (kenapa cabang FFT gagal).

> **ATURAN EMAS (wajib dipatuhi tiap penambahan):** setiap paragraf teori baru di BAB II **harus mendarat** (dioperasionalkan) di BAB IV *Pembahasan* dan/atau BAB V *Saran*. Tidak ada teori yang berhenti sebagai background. Kolom "Payoff" di tiap bagian bawah ini = syarat lulus.

**Dampak panjang (jawaban untuk penguji):** pangkasan (~4–5 hlm: Dropoff+Periodic+Warping+Cross-GAN) **jauh lebih besar** dari tambahan (~1,5–2 hlm untuk 3 subbab padat). Jadi BAB II **tetap menyusut neto**, tetapi setiap bagian kini *load-bearing*. Narasi sidang: *"saya tidak hanya memotong — saya mengganti teori mati dengan teori yang menjelaskan hasil saya."*

---

## 1. PHASE INFORMATION FFT  ⭐ prioritas tertinggi (paling tajam & faktual)

**Kenapa terkuat:** ini **fakta desain yang terverifikasi**, bukan spekulasi. Cache FFT penelitian ini **hanya magnitudo** (`compute_fft_cache.py` → *log-magnitude*; FreqCNN menerima 1 kanal magnitudo). Komponen **fase dibuang total**. Fase justru membawa sebagian besar informasi struktural citra — jadi membuangnya adalah kandidat-penjelasan langsung kenapa cabang frekuensi nyaris acak.

### Penempatan di BAB II
**Subbab "Frequency Domain Analysis" (2.4)** → tambah **Heading3 baru** tepat setelah *"Transformasi Fourier (FFT)"*, judul:
> **2.4.x Spektrum Magnitudo dan Fase**

### Isi (≈140–170 kata, 2 paragraf)
1. **Dekomposisi:** Transformasi Fourier sebuah citra menghasilkan bilangan kompleks yang terurai jadi **spektrum magnitudo** (|F|, kekuatan tiap frekuensi) dan **spektrum fase** (∠F, posisi/penyelarasan tiap komponen). Magnitudo menyimpan *berapa banyak* energi tiap frekuensi; fase menyimpan *di mana* struktur berada (Gonzalez & Woods, 2018).
2. **Pentingnya fase:** Studi klasik menunjukkan rekonstruksi citra dari **fase saja** mempertahankan struktur (tepi, bentuk) yang dikenali, sedangkan dari **magnitudo saja** kehilangan struktur — artinya fase membawa sebagian besar informasi struktural (Oppenheim & Lim, 1981). Dalam deteksi *deepfake*, pendekatan yang mengeksploitasi spektrum fase (mis. SPSL) terbukti menangkap artefak *blending up-sampling* yang tidak tampak pada magnitudo (Liu et al., 2021). Konsekuensinya, representasi berbasis-magnitudo memberi gambaran spektral yang **tidak lengkap** — sebuah pertimbangan desain yang relevan dievaluasi pada BAB IV.

### Payoff (WAJIB) → BAB IV `Analisis Akar Penyebab Lemahnya Cabang Frekuensi`
Tambah 1 faktor:
> *"Ketiga, cabang frekuensi pada penelitian ini hanya menggunakan **spektrum magnitudo** dan membuang **spektrum fase**. Padahal fase membawa sebagian besar informasi struktural citra (Oppenheim & Lim, 1981), dan pendekatan yang memanfaatkan fase seperti SPSL menunjukkan fase informatif untuk deteksi (Liu et al., 2021). Dengan demikian, peta FFT log-magnitudo yang dipakai memberi representasi spektral tak lengkap, dan hilangnya petunjuk fase menjadi kandidat penyebab cabang frekuensi sulit mempelajari pola diskriminatif."*

→ juga 1 kalimat di **BAB V Saran**: *"mengikutkan spektrum fase (mis. SPSL) sebagai masukan cabang frekuensi."*

### Referensi
- **Sudah ada:** Gonzalez & Woods, 2018 (Gon18).
- **TAMBAH BARU (2):** Oppenheim & Lim, 1981 — *The Importance of Phase in Signals*, Proc. IEEE 69(5). · Liu et al., 2021 — *Spatial-Phase Shallow Learning (SPSL)*, CVPR 2021.
  > Catatan: Oppenheim & Lim 1981 ≠ Oppenheim (Opp89) yang baru dihapus. Ini paper berbeda dan **benar-benar dipakai**.

---

## 2. FREQUENCY / TEXTURE BIAS PADA CNN  ⭐ prioritas kedua (kuat)

**Kenapa kuat:** menjelaskan *mekanisme* kenapa CNN dangkal di atas peta FFT sulit belajar, dan kenapa XceptionNet spasial sudah cukup menangkap petunjuk. Memperkuat pembahasan hasil negatif.

### Penempatan di BAB II
**Subbab "Frequency Domain Analysis" (2.4)** → **Heading3 baru** setelah *"Artefak Frekuensi pada Citra Deepfake"*, judul:
> **2.4.x Bias Frekuensi dan Tekstur pada CNN**

*(Alternatif: taruh di "Deep Learning → CNN". Rekomendasi: di 2.4 agar berdampingan dengan justifikasi/limitasi pendekatan frekuensi.)*

### Isi (≈150–180 kata, 2 paragraf)
1. **Bias tekstur:** CNN terlatih cenderung mengklasifikasi berdasarkan **tekstur**, bukan bentuk global (Geirhos et al., 2019). Pada deteksi deepfake, ini menjelaskan kenapa backbone spasial seperti XceptionNet efektif menangkap anomali tekstur kulit/*blending*.
2. **Bias spektral / komponen frekuensi:** CNN mempelajari komponen **frekuensi rendah lebih dahulu** (*spectral bias* / *frequency principle*) (Rahaman et al., 2019), dan kemampuan generalisasinya terkait erat dengan cara ia memanfaatkan komponen frekuensi tinggi (Wang et al., 2020). Implikasinya untuk penelitian ini: sebuah **FreqCNN dangkal** yang menerima peta magnitudo FFT mentah harus mempelajari selektivitas frekuensi yang tepat tanpa bias arsitektural yang membantunya, sehingga rawan gagal bila sinyalnya lemah/terdistorsi — kontras dengan XceptionNet yang bias-tekstur-nya selaras dengan artefak spasial.

### Payoff (WAJIB) → BAB IV `Analisis Akar Penyebab Lemahnya Cabang Frekuensi`
Sisipkan ke faktor "arsitektur fusi lemah" (faktor kedua yang sudah ada):
> *"…Hal ini diperkuat oleh sifat **bias frekuensi-tekstur** CNN: jaringan konvolusi cenderung mengandalkan tekstur dan mempelajari komponen frekuensi rendah lebih dahulu (Geirhos et al., 2019; Rahaman et al., 2019), sehingga FreqCNN dangkal sulit menemukan selektivitas frekuensi diskriminatif pada peta magnitudo yang sudah terdistorsi crop+kompresi, sementara XceptionNet spasial bekerja pada ranah yang selaras dengan bias bawaannya."*

### Referensi
- **TAMBAH BARU (2–3):** Geirhos et al., 2019 — *ImageNet-trained CNNs are biased towards texture*, ICLR 2019. · Wang et al., 2020 — *High-Frequency Component Helps Explain the Generalization of CNN*, CVPR 2020. · *(opsional)* Rahaman et al., 2019 — *On the Spectral Bias of Neural Networks*, ICML 2019.
  > Minimal 2 (Geirhos + Wang); Rahaman opsional untuk kedalaman.

---

## 3. DOMAIN ADAPTATION / GENERALIZATION  ⭐ prioritas ketiga (bagus, hati-hati framing)

**Kenapa perlu hati-hati:** fokus skripsi = *cross-dataset generalization*, dan ini memang ranah domain adaptation/generalization. TAPI penelitian ini **tidak menggunakan data target saat latih** → secara teknis yang dilakukan adalah **Domain Generalization (DG)**, *bukan* Domain Adaptation (DA, yang memakai data target). **Jangan klaim melakukan DA.** Bingkai: latar teori untuk memahami *domain shift* + arah lanjutan.

### Penempatan di BAB II
**Subbab "Cross Dataset Generalization"** (Heading2, saat ini tanpa sub-subbab) → tambah **1–2 paragraf** (atau Heading3 *"Domain Shift, Adaptasi, dan Generalisasi Domain"*) **setelah** paragraf *domain shift* (paragraf yang kini memuat kalimat sisipan cross-GAN).

### Isi (≈130–160 kata)
- **Definisi & posisi:** *Domain shift* — pergeseran distribusi data antara domain sumber (latih) dan target (uji) — adalah akar kesulitan lintas dataset; secara teori, risiko model pada domain target dibatasi oleh risiko sumber **ditambah** jarak antar-distribusi kedua domain (Ben-David et al., 2010). Bidang yang menanganinya: **domain adaptation** (memakai sebagian data target saat pelatihan) dan **domain generalization** (melatih agar tahan tanpa melihat target).
- **Posisi penelitian ini (jujur):** Evaluasi *cross-dataset* (latih FFPP, uji CDF, tanpa data CDF saat latih) **termasuk skenario domain generalization**, bukan adaptation. Penambahan cabang frekuensi diharapkan menghasilkan representasi yang lebih invarian-domain, sejalan dengan laporan bahwa fitur frekuensi lebih *generalizable* (Tan et al., 2024) dan upaya mencari artefak yang lebih umum (Ma et al., 2024). Teknik adaptasi domain eksplisit berada di luar lingkup dan menjadi arah pengembangan.

### Payoff (WAJIB)
- **BAB IV** `Penurunan Performa Model Spasial pada Cross-Dataset`: 1 kalimat membingkai Δ sebagai manifestasi *domain shift* (Ben-David et al., 2010) dan menegaskan setup = domain generalization.
- **BAB V Saran:** *"menerapkan teknik adaptasi domain eksplisit (mis. penyelarasan distribusi fitur / adversarial domain adaptation) yang tidak dicakup penelitian ini."*

### Referensi
- **Sudah ada:** Tan et al., 2024 (Tan24); Ma et al. (Ma — INDEX menyebut keyword "domain adaptation"); Haliassos (generalization).
- **TAMBAH BARU (1):** Ben-David et al., 2010 — *A Theory of Learning from Different Domains*, Machine Learning 79. *(opsional: Wang & Deng, 2018 — Deep Visual Domain Adaptation: A Survey, jika ingin rujukan survei.)*
  > Bisa minimal **tanpa** referensi baru bila mau (andalkan Ma + Tan), tapi Ben-David memberi dasar teoretis (batas risiko) yang kuat dan murah.

---

## 4. RINGKASAN REFERENSI BARU YANG PERLU DITAMBAH (ke Mendeley/Manage Sources)

| # | Teori | Referensi baru | Wajib? |
|---|---|---|---|
| 1 | Phase | **Oppenheim & Lim, 1981** — The Importance of Phase in Signals (Proc. IEEE 69:5) | ✅ wajib |
| 2 | Phase | **Liu et al., 2021** — Spatial-Phase Shallow Learning / SPSL (CVPR 2021) | ✅ wajib |
| 3 | Freq bias | **Geirhos et al., 2019** — ImageNet-trained CNNs biased towards texture (ICLR 2019) | ✅ wajib |
| 4 | Freq bias | **Wang et al., 2020** — High-Frequency Component Helps Explain Generalization of CNN (CVPR 2020) | ✅ wajib |
| 5 | Freq bias | Rahaman et al., 2019 — On the Spectral Bias of Neural Networks (ICML 2019) | ◯ opsional |
| 6 | Domain | Ben-David et al., 2010 — A Theory of Learning from Different Domains (Mach. Learn. 79) | ◯ disarankan |
| 7 | Domain | Wang & Deng, 2018 — Deep Visual Domain Adaptation: A Survey (Neurocomputing) | ◯ opsional |

**Minimal set = 4 wajib + Ben-David (disarankan) = 5 referensi baru.** Semua paper nyata & terkenal (bukan fabrikasi). Tidak ada PDF lokal → tambah manual di *References → Manage Sources*.

> **Catatan keseimbangan sitasi:** menambah 5 entri sambil menghapus 3 orphan (Oppenheim Opp89, Easton, Robbins) → Daftar Pustaka neto **+2** (42 → ~44). Semua tambahan **tersitasi** (Pedoman 4.5.5.d aman).

---

## 5. URUTAN EKSEKUSI

1. **Phase** (Bagian 1) — paling berdampak & paling mudah dibela; pasang dulu. + payoff BAB IV & Saran.
2. **Freq/Texture Bias** (Bagian 2) — sisipkan subbab + payoff ke faktor fusi BAB IV.
3. **Domain Adaptation/Generalization** (Bagian 3) — paragraf di Cross Dataset Generalization + payoff BAB IV/Saran; **jaga framing DG bukan DA**.
4. Tambah 5 referensi baru di Manage Sources → **Update Fields** (renumber `[N]` + Daftar Pustaka + Daftar Isi).

## Checklist
- [ ] 2.4.x Spektrum Magnitudo dan Fase + payoff BAB IV faktor-3 + Saran
- [ ] 2.4.x Bias Frekuensi dan Tekstur pada CNN + payoff BAB IV faktor-fusi
- [ ] Paragraf Domain Shift/Adaptation/Generalization di Cross Dataset Generalization + payoff BAB IV/Saran (framing DG)
- [ ] Tambah 5 referensi baru (Oppenheim&Lim, Liu/SPSL, Geirhos, Wang, Ben-David) ke Manage Sources
- [ ] Update Fields seluruh dokumen + cek Daftar Isi/Pustaka
</content>
</invoke>
