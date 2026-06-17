# REVISI BAB II · IV · V — Penambahan Teori (Phase FFT · Frequency/Texture Bias CNN · Domain Adaptation)

> **Cara pakai:** tiap blok = teks **siap-tempel**. Bagian **baru** ditandai **「TAMBAHAN」 … 「/TAMBAHAN」**; penyisipan ke paragraf yang sudah ada ditandai **「SISIPKAN setelah: '…' 」**; penggantian ditandai **「GANTI」**. Anchor dikutip **persis** dari docx (cek 2026-06-17 14:43).
>
> **Sitasi:** **(Nama, Tahun)** untuk memudahkan input (di Word → CITATION field render `[N]`).
>
> **Basis:** `PLAN_BAB_II_Teori_Tambahan_2026-06-17.md`. Aturan emas dipatuhi: **tiap teori baru di BAB II mendarat di BAB IV/V** (matriks anti-orphan di §0).

---

## 0. MATRIKS ANTI-ORPHAN (bukti tiap teori & referensi terpakai lintas-BAB)

| Teori (BAB II) | Mendarat di BAB IV | Mendarat di BAB V | Status |
|---|---|---|---|
| **Phase FFT** (2.4.x baru) | 4.2.4 *root-cause* faktor **Ketiga** | Saran "Memperkuat cabang frekuensi" | ✅ tidak orphan |
| **Freq/Texture Bias CNN** (2.4.x baru) | 4.2.4 *root-cause* faktor **Keempat** | Saran "Memperkuat cabang frekuensi" | ✅ tidak orphan |
| **Domain Adaptation/Generalization** (Cross Dataset Gen.) | 4.2.2 "Penurunan Performa Spasial" (1 kalimat) | Saran baru "Adaptasi domain eksplisit" | ✅ tidak orphan |

| Referensi baru | Dipakai di | ✓ ≥2× |
|---|---|---|
| Oppenheim & Lim, 1981 | BAB II Phase · BAB IV Ketiga | ✅ |
| Liu et al., 2021 (SPSL) | BAB II Phase · BAB IV Ketiga · BAB V Saran | ✅ |
| Geirhos et al., 2019 | BAB II Freq-bias · BAB IV Keempat · BAB V Saran | ✅ |
| Wang et al., 2020 | BAB II Freq-bias · BAB IV Keempat | ✅ |
| Rahaman et al., 2019 | BAB II Freq-bias · BAB IV Keempat | ✅ |
| Ben-David et al., 2010 | BAB II Domain · BAB IV 4.2.2 · BAB V Saran | ✅ |

---

## A. BAB II — TAMBAHAN 1 · Sub-bab baru "Spektrum Magnitudo dan Fase"

**Letak:** subbab **"Frequency Domain Analysis" (2.4)**, **sisipkan sebagai Heading3 baru** TEPAT **di antara**:
- sesudah → Heading3 **"Transformasi Fourier (FFT)"** (yang berakhir pada paragraf log-scaling spektrum magnitudo)
- sebelum → Heading3 **"Artefak Frekuensi pada Citra Deepfake"**

**「TAMBAHAN」**

### Spektrum Magnitudo dan Fase

Hasil Transformasi Fourier sebuah citra berupa bilangan kompleks yang dapat diuraikan menjadi dua komponen: *spektrum magnitudo* (|F(u,v)|) dan *spektrum fase* (∠F(u,v)). Spektrum magnitudo menyatakan seberapa besar energi yang terkandung pada setiap frekuensi, sedangkan spektrum fase menyatakan posisi serta penyelarasan setiap komponen frekuensi yang menentukan susunan struktur spasial citra (Gonzalez & Woods, 2018). Sebagian besar pendekatan deteksi *deepfake* berbasis frekuensi — termasuk representasi yang digunakan pada penelitian ini — hanya memanfaatkan spektrum magnitudo, sementara informasi fase umumnya diabaikan.

Padahal, sejumlah studi menunjukkan bahwa fase membawa porsi informasi struktural yang besar. Oppenheim & Lim (1981) memperlihatkan bahwa citra yang direkonstruksi hanya dari spektrum fase masih mempertahankan struktur penting seperti tepi dan bentuk objek, sedangkan rekonstruksi hanya dari spektrum magnitudo justru kehilangan struktur tersebut. Dalam konteks deteksi pemalsuan wajah, Liu et al. (2021) melalui metode *Spatial-Phase Shallow Learning* (SPSL) menunjukkan bahwa spektrum fase efektif menonjolkan artefak akumulatif dari proses *up-sampling* generatif yang tidak tampak pada domain spasial maupun pada spektrum magnitudo. Dengan demikian, representasi frekuensi yang hanya berbasis magnitudo memberikan gambaran spektral yang tidak lengkap, sebuah keterbatasan desain yang relevan dalam menafsirkan kinerja cabang frekuensi berbasis-magnitudo.

**「/TAMBAHAN」**

> Referensi baru: **Oppenheim & Lim, 1981**; **Liu et al., 2021**. Referensi lama dipakai ulang: Gonzalez & Woods, 2018.

---

## B. BAB II — TAMBAHAN 2 · Sub-bab baru "Bias Frekuensi dan Tekstur pada CNN"

**Letak:** subbab **"Frequency Domain Analysis" (2.4)**, **sisipkan sebagai Heading3 baru** TEPAT **sesudah** Heading3 **"Artefak Frekuensi pada Citra Deepfake"** (yang berakhir pada *Tabel 2.3 Karakteristik Artefak Frekuensi*) dan **sebelum** Heading3 **"Peran Frequency Domain Analysis dalam Deteksi Deepfake"**.

**「TAMBAHAN」**

### Bias Frekuensi dan Tekstur pada CNN

Efektivitas sebuah arsitektur dalam memanfaatkan petunjuk frekuensi tidak hanya ditentukan oleh ketersediaan sinyal, tetapi juga oleh kecenderungan induktif (*inductive bias*) jaringan itu sendiri. Geirhos et al. (2019) menunjukkan bahwa CNN yang dilatih pada citra natural cenderung mengambil keputusan berdasarkan *tekstur* lokal alih-alih bentuk global. Kecenderungan ini menjelaskan mengapa *backbone* spasial seperti XceptionNet efektif menangkap anomali tekstur kulit dan ketidaksesuaian *blending* pada wajah *deepfake*, karena ranah kerjanya selaras dengan bias bawaan CNN.

Di sisi lain, jaringan saraf memiliki *spectral bias*, yaitu kecenderungan mempelajari komponen frekuensi rendah terlebih dahulu, kemudian komponen frekuensi tinggi apabila memungkinkan (Rahaman et al., 2019). Wang et al. (2020) lebih jauh menunjukkan bahwa kemampuan generalisasi CNN berkaitan erat dengan cara jaringan memanfaatkan komponen frekuensi tinggi citra. Implikasinya bagi penelitian ini, sebuah CNN frekuensi yang relatif dangkal dan menerima peta magnitudo FFT mentah harus mempelajari selektivitas frekuensi yang diskriminatif tanpa dukungan bias arsitektural yang memadai. Ketika sinyal artefak lemah atau terdistorsi, jaringan semacam ini rentan gagal menemukan pola yang berguna. Pemahaman ini menjadi landasan teoretis dalam membahas kinerja cabang frekuensi pada arsitektur *hybrid*.

**「/TAMBAHAN」**

> Referensi baru: **Geirhos et al., 2019**; **Rahaman et al., 2019**; **Wang et al., 2020**.
> *(Alternatif penempatan: di subbab "Deep Learning → CNN". Rekomendasi tetap di 2.4 agar berdampingan dengan justifikasi/limitasi pendekatan frekuensi.)*

---

## C. BAB II — TAMBAHAN 3 · Paragraf Domain Adaptation/Generalization

**Letak:** subbab **"Cross Dataset Generalization"** (Heading2). Sisipkan **2 paragraf** TEPAT **di antara**:
- sesudah → paragraf *domain shift* (paragraf yang berakhir pada kalimat sisipan *cross-GAN*: "…evaluasi *cross-GAN* dalam praktiknya menyatu dengan evaluasi *cross-dataset* (Rana et al., 2022; Rao & Uehara, 2025).")
- sebelum → paragraf berikutnya yang dimulai "Penelitian-penelitian modern menunjukkan bahwa pendekatan berbasis domain frekuensi…"

**「SISIPKAN setelah paragraf domain shift (yang berakhir '…menyatu dengan evaluasi cross-dataset.')」**

Secara teoretis, kesulitan lintas dataset ini merupakan persoalan yang dipelajari dalam bidang *domain adaptation* dan *domain generalization*. Ben-David et al. (2010) menunjukkan bahwa galat sebuah model pada domain target dibatasi oleh galatnya pada domain sumber ditambah suatu ukuran jarak (divergensi) antara distribusi kedua domain; semakin jauh distribusi domain uji dari domain latih, semakin besar potensi penurunan performa. Perbedaan kedua pendekatan terletak pada ketersediaan data target: *domain adaptation* memanfaatkan sebagian data domain target (berlabel maupun tidak) selama pelatihan untuk menyelaraskan distribusi, sedangkan *domain generalization* berupaya melatih model agar tahan terhadap pergeseran tanpa pernah melihat domain target.

Dalam kerangka ini, evaluasi *cross-dataset* pada penelitian ini termasuk skenario *domain generalization*, bukan *domain adaptation*, karena model dilatih pada satu dataset lalu diuji pada dataset lain tanpa menyertakan data uji selama pelatihan. Penambahan cabang frekuensi diharapkan menghasilkan representasi yang lebih invarian terhadap domain, sejalan dengan laporan bahwa fitur frekuensi cenderung lebih *generalizable* lintas dataset (Tan et al., 2024) dan upaya menemukan artefak yang lebih umum (Ma et al., 2024). Teknik adaptasi domain eksplisit berada di luar lingkup penelitian ini dan menjadi salah satu arah pengembangan.

**「/SISIPKAN」**

> Referensi baru: **Ben-David et al., 2010**. Referensi lama dipakai ulang: Tan et al., 2024 (Tan24); Ma et al. (Ma — entri Daftar Pustaka [34]; gunakan tahun sesuai entri sumber yang sudah ada).
> **⚠️ Framing wajib:** ini *domain generalization*, **bukan** klaim melakukan *domain adaptation*. Jangan ubah jadi seolah-olah penelitian menerapkan DA.

---

## D. BAB IV — SISIPKAN · 4.2.4 "Analisis Akar Penyebab Lemahnya Cabang Frekuensi" (faktor 3 & 4)

**Letak:** subbab **"Analisis Akar Penyebab Lemahnya Cabang Frekuensi"**. Saat ini berisi 2 paragraf ("Pertama…" kerusakan artefak; "Kedua…" fusi lemah + SE gating). **Tambahkan 2 paragraf baru** TEPAT **sesudah** paragraf kedua (yang berakhir: "…**bukan sekadar kurang optimal pada tahap akhir.**") dan **sebelum** Heading3 berikutnya **"Keterbatasan Penelitian"**.

**「SISIPKAN setelah paragraf 'Kedua…' (berakhir '…bukan sekadar kurang optimal pada tahap akhir.')」**

Ketiga, dari sisi representasi masukan, cabang frekuensi pada penelitian ini hanya menggunakan spektrum magnitudo FFT (dalam skala logaritmik) dan membuang spektrum fase. Padahal fase membawa sebagian besar informasi struktural citra (Oppenheim & Lim, 1981), dan pendekatan yang secara eksplisit memanfaatkan fase seperti SPSL terbukti menangkap artefak *up-sampling* generatif yang tidak tampak pada magnitudo (Liu et al., 2021). Dengan demikian, peta magnitudo yang menjadi satu-satunya masukan cabang frekuensi sudah merupakan representasi spektral yang tidak lengkap sejak awal, sehingga sebagian petunjuk diskriminatif berpotensi hilang sebelum proses pembelajaran dimulai.

Keempat, dari sisi kapasitas pembelajaran, sifat bias bawaan CNN turut membatasi cabang frekuensi. Jaringan konvolusi cenderung mengandalkan tekstur dan mempelajari komponen frekuensi rendah lebih dahulu (Geirhos et al., 2019; Rahaman et al., 2019), sedangkan kemampuan generalisasinya bergantung pada pemanfaatan komponen frekuensi tinggi yang tepat (Wang et al., 2020). FreqCNN yang relatif dangkal harus menemukan selektivitas frekuensi diskriminatif pada peta magnitudo yang sudah terdistorsi oleh *cropping* dan kompresi tanpa dukungan bias arsitektural yang memadai, kontras dengan XceptionNet spasial yang bekerja pada ranah tekstur yang selaras dengan bias bawaannya. Kombinasi representasi masukan yang tidak lengkap (faktor ketiga) dan keterbatasan kapasitas belajar ini memberikan penjelasan teoretis yang melengkapi penyebab empiris (kerusakan artefak dan fusi yang lemah) yang dibahas sebelumnya.

**「/SISIPKAN」**

> Hasil akhir 4.2.4 = 4 faktor: (1) artefak rusak crop+kompresi · (2) fusi lemah/SE gating · **(3) fase dibuang** · **(4) bias frekuensi-tekstur CNN**. Faktor (1)&(3) tentang *masukan*; (2)&(4) tentang *pembelajaran/fusi* — terstruktur rapi.
> Referensi baru: Oppenheim & Lim 1981, Liu et al. 2021, Geirhos et al. 2019, Rahaman et al. 2019, Wang et al. 2020.

---

## E. BAB IV — SISIPKAN · 4.2.2 "Penurunan Performa Model Spasial pada Cross-Dataset" (1 kalimat domain shift)

**Letak:** subbab **"Penurunan Performa Model Spasial pada Cross-Dataset"**. Sisipkan **1 kalimat** TEPAT **sesudah** kalimat: "…menunjukkan bahwa detektor berbasis fitur spasial **mudah terjebak pada artefak spesifik dataset pelatihan.**" dan **sebelum** "Dengan demikian, RM1 terjawab…".

**「SISIPKAN setelah '…mudah terjebak pada artefak spesifik dataset pelatihan.'」**

Secara teoretis, degradasi ini merupakan manifestasi *domain shift*, yaitu pergeseran distribusi antara domain sumber (data latih) dan domain target (data uji) yang membatasi performa lintas-domain sesuai batas galat pada domain target (Ben-David et al., 2010). Penelitian ini tidak menyertakan data dataset target saat pelatihan sehingga skenario yang diuji termasuk *domain generalization*, bukan *domain adaptation*.

**「/SISIPKAN」**

> Referensi baru: Ben-David et al., 2010. Menautkan teori Domain (BAB II §C) ke hasil RM1.

---

## F. BAB V — GANTI · Saran "Memperkuat cabang frekuensi" (grounding fase + bias CNN)

**Letak:** subbab **"Saran"**, butir **"Memperkuat cabang frekuensi"**. Kalimat saat ini:

> ~~"Lemahnya cabang frekuensi diduga kuat disebabkan oleh hilangnya sidik jari spektral akibat *face-cropping* dan kompresi. Penelitian lanjutan dapat menggunakan representasi frekuensi yang lebih tahan terhadap kedua proses tersebut, misalnya menghitung FFT pada citra penuh (tanpa *crop*), memanfaatkan informasi fasa, atau menerapkan analisis frekuensi multi-skala."~~

**「GANTI butir tersebut DENGAN」**

Lemahnya cabang frekuensi diduga kuat disebabkan oleh hilangnya sidik jari spektral akibat *face-cropping* dan kompresi, serta oleh representasi masukan yang tidak lengkap. Penelitian lanjutan dapat menggunakan representasi frekuensi yang lebih tahan terhadap kedua proses tersebut, misalnya menghitung FFT pada citra penuh (tanpa *crop*) atau menerapkan analisis frekuensi multi-skala. Yang tidak kalah penting, cabang frekuensi sebaiknya menyertakan informasi fasa yang terbukti informatif untuk deteksi pemalsuan wajah (misalnya pendekatan SPSL oleh Liu et al., 2021), bukan hanya spektrum magnitudo. Selain itu, mengingat CNN dangkal memiliki bias terhadap tekstur dan komponen frekuensi rendah (Geirhos et al., 2019), arsitektur cabang frekuensi yang lebih dalam atau dilengkapi mekanisme atensi-frekuensi eksplisit perlu dipertimbangkan agar mampu mempelajari selektivitas frekuensi yang diskriminatif.

**「/GANTI」**

> Menautkan teori Phase (§A) dan Freq-bias (§B) ke Saran. Referensi: Liu et al. 2021, Geirhos et al. 2019.

---

## G. BAB V — TAMBAHAN · Saran baru "Menerapkan adaptasi domain eksplisit"

**Letak:** subbab **"Saran"**. Tambahkan **butir baru** (judul tebal + 1 paragraf), disarankan **sesudah** butir "Mengeksplorasi domain transformasi alternatif".

**「TAMBAHAN」**

**Menerapkan adaptasi domain eksplisit**

Karena evaluasi lintas dataset pada penelitian ini merupakan skenario *domain generalization* tanpa memanfaatkan data domain target, penelitian lanjutan dapat menerapkan teknik adaptasi domain (*domain adaptation*) secara eksplisit, misalnya penyelarasan distribusi fitur antar-domain atau *adversarial domain adaptation*, untuk menekan pengaruh *domain shift* (Ben-David et al., 2010) yang menjadi akar penurunan performa lintas dataset.

**「/TAMBAHAN」**

> Menautkan teori Domain (§C) ke Saran. Referensi: Ben-David et al., 2010.

---

## H. REFERENSI BARU — sudah diunduh ke `thesis_reference/` (tambahkan ke Manage Sources)

Semua PDF **sudah tersimpan** di `/Users/sam/Documents/GitHub/skripsi/thesis_reference/` (total entri 42 → 48). Tambahkan ke *References → Manage Sources* dengan data berikut:

| Tag saran | Sitasi lengkap |
|---|---|
| OppLim81 | A. V. Oppenheim dan J. S. Lim, "The Importance of Phase in Signals," *Proceedings of the IEEE*, vol. 69, no. 5, pp. 529–541, May 1981. |
| Liu21 | H. Liu, X. Li, W. Zhou, Y. Chen, Y. He, H. Xue, W. Zhang, dan N. Yu, "Spatial-Phase Shallow Learning: Rethinking Face Forgery Detection in Frequency Domain," in *CVPR*, 2021, pp. 772–781. |
| Gei19 | R. Geirhos, P. Rubisch, C. Michaelis, M. Bethge, F. A. Wichmann, dan W. Brendel, "ImageNet-trained CNNs are biased towards texture; increasing shape bias improves accuracy and robustness," in *ICLR*, 2019. |
| Wan20 | H. Wang, X. Wu, Z. Huang, dan E. P. Xing, "High-Frequency Component Helps Explain the Generalization of Convolutional Neural Networks," in *CVPR*, 2020, pp. 8684–8694. |
| Rah19 | N. Rahaman, A. Baratin, D. Arpit, F. Draxler, M. Lin, F. A. Hamprecht, Y. Bengio, dan A. Courville, "On the Spectral Bias of Neural Networks," in *ICML*, 2019, pp. 5301–5310. |
| BenD10 | S. Ben-David, J. Blitzer, K. Crammer, A. Kulesza, F. Pereira, dan J. W. Vaughan, "A theory of learning from different domains," *Machine Learning*, vol. 79, no. 1–2, pp. 151–175, 2010. |

**Dampak Daftar Pustaka:** +6 entri baru − 3 orphan terhapus (Oppenheim Opp89, Easton, Robbins) = **neto +3** (≈45 entri). Semua tambahan **tersitasi ≥2×** (Pedoman 4.5.5.d aman). *(Bila Rahaman dilewati: +5 baru, neto +2.)*

> Catatan: **Oppenheim & Lim 1981 ≠ Oppenheim Opp89** (Discrete-Time Signal Processing) yang dihapus. Paper berbeda dan benar-benar dipakai.

---

## I. URUTAN EKSEKUSI

1. Tambah 6 referensi ke *Manage Sources* (data di §H).
2. BAB II: sisipkan §A (Phase), §B (Freq-bias), §C (Domain).
3. BAB IV: sisipkan §D (root-cause faktor 3&4), §E (1 kalimat 4.2.2).
4. BAB V: ganti §F (Saran fase+bias), tambah §G (Saran adaptasi domain).
5. **Update Fields** seluruh dokumen (Ctrl+A → F9) → renumber `[N]`, Daftar Pustaka, Daftar Isi.
6. Cek Daftar Isi memuat 2 Heading3 baru (Spektrum Magnitudo dan Fase; Bias Frekuensi dan Tekstur pada CNN).

## Checklist
- [ ] 6 referensi ditambah ke Manage Sources
- [ ] §A Spektrum Magnitudo dan Fase (BAB II 2.4)
- [ ] §B Bias Frekuensi dan Tekstur pada CNN (BAB II 2.4)
- [ ] §C Paragraf Domain Adaptation/Generalization (BAB II Cross Dataset Gen.)
- [ ] §D Faktor 3&4 root-cause (BAB IV 4.2.4)
- [ ] §E Kalimat domain shift (BAB IV 4.2.2)
- [ ] §F Saran fase+bias diganti (BAB V)
- [ ] §G Saran adaptasi domain baru (BAB V)
- [ ] Update Fields + cek Daftar Isi/Pustaka
</content>
</invoke>
