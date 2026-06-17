# Konten Presentasi Sidang — Slide demi Slide

> Cara pakai: tiap blok antara `---` = **satu slide**. **Poin** = teks yang ditaruh di slide (ringkas). **🎤 Skrip** = yang diucapkan (jangan ditaruh di slide). Target ~20 menit, ~24 slide. Gaya: tanpa tanda pisah panjang dan titik-koma. Ganti judul lama jika sudah disetujui pembimbing.

---

## Slide 1 — Sampul

**Judul:**
Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet–FFT terhadap Model Domain Tunggal

Naomi Prisella (221111798) · Giovanny Halimko (221110058) · Samuel Onasis (221110680)
Dosen Pembimbing: [nama]
Program Studi [..], Universitas Mikroskil, Medan — 2026

🎤 *"Selamat [pagi/siang], kami akan mempresentasikan studi komparatif kinerja deteksi deepfake antara arsitektur hybrid XceptionNet–FFT dan model domain tunggal."*

---

## Slide 2 — Outline

- Latar Belakang & Masalah
- Tujuan & Hipotesis
- Landasan Teori
- Metodologi
- Hasil & Pembahasan
- Kesimpulan & Saran

🎤 Sebutkan alurnya dalam satu kalimat, lalu lanjut.

---

## Slide 3 — Latar Belakang

- Deepfake makin realistis dan menjadi ancaman forensik digital (misinformasi, penipuan).
- Detektor **domain spasial** (mis. XceptionNet) kuat di dataset yang sama, tetapi **lemah saat diuji lintas dataset**.
- Literatur mengklaim **domain frekuensi** (artefak GAN) lebih tahan dan lebih *generalizable*.

🎤 *"Masalah utama bukan akurasi di satu dataset, melainkan generalisasi: model sering jatuh saat menghadapi deepfake dari sumber berbeda. Banyak penelitian mengusulkan domain frekuensi sebagai solusi."*

---

## Slide 4 — Celah Penelitian & Motivasi

- Klaim "frekuensi lebih baik" sering diuji pada **kondisi ideal** (kompresi rendah, *cross-manipulation* dalam satu dataset).
- Belum banyak yang **menguji secara terkontrol** kontribusi frekuensi pada **generalisasi cross-dataset** yang lebih berat.
- **Posisi kami:** studi **komparatif** untuk mengukur kontribusi frekuensi, bukan menjanjikan peningkatan.

🎤 *"Di sinilah celahnya. Kami tidak berasumsi frekuensi pasti membantu. Kami mengujinya secara adil dan komparatif."*

---

## Slide 5 — Rumusan Masalah

1. Sejauh mana detektor spasial murni (XceptionNet) **menurun performanya** saat diuji lintas dataset?
2. Sejauh mana penambahan analisis frekuensi (FFT) dapat **memperkecil penurunan** tersebut?
3. Seberapa besar **kontribusi masing-masing komponen** (spasial vs frekuensi) terhadap performa?

🎤 Bacakan ketiganya singkat. Tekankan ketiganya bersifat **mengukur/membandingkan**.

---

## Slide 6 — Tujuan & Hipotesis

**Tujuan:** mengimplementasikan model hybrid, melakukan *ablation* (spasial vs frekuensi vs hybrid), dan mengevaluasi generalisasi in-dataset & cross-dataset.

**Hipotesis:**
- **H1:** Hybrid memiliki generalisasi cross-dataset lebih baik daripada model spasial.
- **H0:** Tidak terdapat peningkatan generalisasi yang berarti dari penambahan frekuensi.

🎤 *"Hipotesis ini kami uji secara empiris dan kami laporkan apa adanya, termasuk bila H0 tidak dapat ditolak."*

---

## Slide 7 — Batasan Penelitian

- Analisis **level frame** (tanpa pemodelan temporal antar-frame).
- Dua dataset benchmark: **FaceForensics++** dan **Celeb-DF v2**.
- Domain frekuensi memakai **magnitudo FFT** (tanpa fase).
- Ukuran sampel 100–750 video, 3 *seed*.

🎤 Sebutkan singkat, ini sekaligus menyiapkan jawaban untuk pertanyaan keterbatasan.

---

## Slide 8 — Landasan Teori (1): Spasial vs Frekuensi

- **Domain spasial:** nilai piksel langsung (tekstur, blending, warna).
- **Domain frekuensi (FFT):** pola periodik halus/kasar. Frekuensi tinggi memuat detail & artefak.
- **Artefak GAN:** proses *up-sampling* gagal mereplikasi statistik frekuensi alami → "sidik jari GAN" di frekuensi menengah-tinggi (Odena, Durall, Zhang).

🎤 Pakai analogi: spasial melihat *apa* yang tampak, frekuensi melihat *pola* yang tak kasat mata.

> Sisipkan **Gambar 2.1 / 2.2** (low vs high frequency / representasi domain frekuensi).

---

## Slide 9 — Landasan Teori (2): Komponen Model

- **XceptionNet:** backbone spasial, *depthwise separable convolution*, pretrained ImageNet.
- **FFT:** mengubah frame menjadi peta magnitudo frekuensi.
- **SE gating:** membobot kepentingan tiap kanal fitur saat fusi.
- **Hybrid (late fusion):** gabungkan fitur spasial + frekuensi di tahap akhir.

🎤 *"Empat komponen inilah yang kami rakit menjadi model hybrid."*

---

## Slide 10 — Metodologi: Alur Penelitian

```
Video → frame @5 FPS → MTCNN crop (224×224)
      → 2 representasi: RGB  +  peta FFT log-magnitude
      → split per-VIDEO (70/15/15)
      → latih 3 model (spatial / freq / hybrid)
      → evaluasi in-dataset & cross-dataset (3 seed)
```

🎤 Jelaskan perjalanan satu video dari awal sampai jadi keputusan. Tekankan **split per-video** untuk mencegah kebocoran.

> Sisipkan **Gambar 3.1** (flowchart pipeline).

---

## Slide 11 — Dataset

| Dataset | Metode manipulasi | Catatan |
|---|---|---|
| FaceForensics++ (FFPP) | 4 metode | kompresi c23 |
| Celeb-DF v2 (CDF) | 1 metode | 590 real / 5.639 fake, kualitas tinggi |

- Evaluasi **cross-dataset**: latih di satu, uji di yang lain (FFPP→CDF dan CDF→FFPP).

🎤 *"Dua dataset ini memungkinkan kami menguji generalisasi pada generator dan kondisi rekaman yang berbeda."*

---

## Slide 12 — Preprocessing

- **Ekstraksi frame** 5 FPS, maks 50 frame/video.
- **Deteksi & crop wajah** dengan MTCNN (margin 0,3) → 224×224.
- **Peta FFT:** grayscale → FFT 2D → fftshift → magnitudo → high-pass → log → normalisasi z-score.
- **Penting:** hanya **magnitudo**, fase tidak dipakai.

🎤 Tekankan baris terakhir, ini relevan ke pembahasan kegagalan frekuensi.

> Sisipkan **Gambar 3.6** (peta FFT real vs fake).

---

## Slide 13 — Arsitektur Tiga Model

- **Spatial:** RGB → XceptionNet (~22 jt param) → logit.
- **Freq:** peta FFT → FreqCNN (5 blok residual, ~4 jt param) → logit.
- **Hybrid:** (RGB→Xception→256-d) + (FFT→FreqCNN→256-d) → concat 512-d → **SE gate** → klasifikasi.

🎤 *"Ketiga model berbagi komponen yang sama supaya perbandingannya adil dan kami bisa mengisolasi kontribusi tiap domain."*

> Sisipkan **Gambar 3.10** (diagram HybridTwoBranch).

---

## Slide 14 — Strategi Pelatihan

- Loss: **BCEWithLogitsLoss** + label smoothing 0,05.
- Optimizer: **AdamW** (lr 2e-4) dengan *differential learning rate*.
- Backbone dibekukan 3 epoch awal, lalu di-unfreeze. Warmup 2 epoch + cosine decay.
- Mixed precision, gradient accumulation, gradient clipping.
- **Seleksi model terbaik berdasarkan val AUC**, early stopping, 3 seed.

🎤 Lewati cepat, ini bukti rigor. Siapkan detail jika ditanya.

---

## Slide 15 — Desain Eksperimen

| Dimensi | Nilai | Jumlah |
|---|---|---|
| Model | spatial, freq, hybrid | 3 |
| Dataset | FFPP, CDF | 2 |
| Ukuran sampel | 100, 250, 500, 750 | 4 |
| Seed | 0, 1, 2 | 3 |
| Evaluasi | in-dataset, cross-dataset | 2 |

Metrik: accuracy, precision, recall, F1, **AUC (utama)**. Ambang θ=0,5 dan ambang optimal Youden J.

🎤 *"Total kombinasi ini membuat perbandingan kami terkontrol dan dapat direproduksi."*

---

## Slide 16 — Hasil (1): In-Dataset

- **Spatial konsisten terbaik**, AUC in-dataset hingga **~0,97**.
- **Freq nyaris setara tebakan acak**, AUC **0,55–0,59**.
- **Hybrid tidak mengungguli spatial** pada semua tier yang andal dan kedua dataset.

🎤 *"Temuan pertama sudah jelas: menambahkan frekuensi tidak menaikkan performa in-dataset."*

> Sisipkan **Gambar 4.3** (bar in-dataset) + **Tabel 4.2**.

---

## Slide 17 — Hasil (2): Cross-Dataset & Generalization Drop

- Semua model **menurun** saat lintas dataset, AUC ke **~0,63–0,65**.
- **Recall collapse**, terparah arah **CDF→FFPP (recall ≈ 0,08)**.
- Manfaat frekuensi **parsial dan bergantung arah**: pada FFPP→CDF drop F1 hybrid **+0,027** vs spatial **+0,116**, tetapi tidak konsisten pada arah sebaliknya.

🎤 *"Frekuensi hanya menahan penurunan pada satu arah, dan itu pun dengan mengorbankan performa in-dataset."*

> Sisipkan **Gambar 4.4** (cross-dataset) + **Gambar 4.5** (gen drop) + **Tabel 4.3/4.4**.

---

## Slide 18 — Hasil (3): Ukuran Sampel & Dinamika Pelatihan

- Tren AUC terhadap ukuran sampel: spatial naik stabil, **freq tetap datar di sekitar acak**.
- Kurva pelatihan model frekuensi **stagnan sejak awal** (gagal belajar pola diskriminatif).
- Confusion matrix cross-dataset menegaskan keruntuhan recall.

🎤 *"Cabang frekuensi bukan kurang optimal di akhir, ia memang tidak pernah belajar."*

> Sisipkan **Gambar 4.6** (tren AUC) + **Gambar 4.7/4.8** (confusion matrix & kurva pelatihan).

---

## Slide 19 — Pembahasan (1): Mengapa Cabang Frekuensi Gagal

1. **Artefak rusak praproses:** crop MTCNN + kompresi c23 menekan frekuensi tinggi (Mejri).
2. **Fase dibuang:** hanya magnitudo, padahal fase membawa struktur (Oppenheim & Lim, Liu/SPSL).
3. **Bias CNN:** cenderung tekstur & frekuensi rendah dulu (Geirhos, Rahaman, Wang).
4. **Representasi terlalu sederhana:** satu peta FFT mentah ke CNN dangkal.

🎤 Ini slide inti pertahanan. Kuasai keempatnya.

---

## Slide 20 — Pembahasan (2): Posisi terhadap Literatur & Hipotesis

- Bukan kontradiksi, melainkan **kondisi batas**. Artefak frekuensi tetap ada (Durall, Zhang), tetapi **mengeksploitasinya bersifat kondisional** (representasi, fusi, praproses, jenis pergeseran domain).
- Penelitian sukses umumnya memakai representasi & fusi frekuensi yang lebih canggih, serta menguji *cross-manipulation* yang lebih ringan.
- **Hipotesis:** H0 **tidak dapat ditolak**. Selisih dibahas deskriptif (3 seed).

🎤 *"Kami melengkapi literatur dengan menandai kapan frekuensi gagal membantu."*

---

## Slide 21 — Purwarupa (Demo)

- Tiga model dikemas dalam purwarupa interaktif **Gradio** di **Hugging Face Spaces**.
- Menampilkan verdict spatial/hybrid/freq berdampingan + panel "what the models see" (wajah vs spektrum FFT).
- Bukti kualitatif: spektrum FFT real vs fake **nyaris tak terbedakan**.

🎤 Tunjukkan **Gambar 4.1 & 4.2** (atau demo live bila diizinkan).

---

## Slide 22 — Kesimpulan

1. **RM1:** detektor spasial murni **menurun substansial** lintas dataset (recall collapse, terparah CDF→FFPP).
2. **RM2:** penambahan FFT **hanya menekan penurunan secara parsial dan bergantung arah**, dengan mengorbankan performa in-dataset.
3. **RM3:** **spasial penyumbang utama**, frekuensi ≈ acak sehingga **hybrid tidak mengungguli spasial**.

🎤 *"Secara keseluruhan, pada konfigurasi yang diuji, kontribusi domain frekuensi terbatas dan generalisasi lintas dataset tetap menjadi tantangan terbuka."*

---

## Slide 23 — Saran

- **Perkuat cabang frekuensi:** sertakan **fase** (mis. SPSL), FFT pada frame penuh, analisis multi-skala.
- **Fusi lebih baik:** regularisasi/atensi dua-domain, pretraining cabang frekuensi.
- **Domain transformasi alternatif:** DCT, wavelet.
- **Adaptasi domain eksplisit** + **uji signifikansi statistik** + **pemodelan temporal**.

🎤 Sambungkan tiap saran ke akar penyebab di Slide 19.

---

## Slide 24 — Kontribusi Ilmiah & Penutup

**Kontribusi:**
- Studi komparatif terkontrol (3 model × 2 dataset × 3 seed) dengan **evaluasi cross-dataset**.
- Bukti kuantitatif bahwa kontribusi frekuensi **terbatas & kondisional**.
- Analisis akar penyebab + posisi terhadap literatur.

**Nilai hasil negatif:** menantang asumsi "tambah FFT pasti lebih baik" dengan bukti, mencegah jalan buntu yang sama.

🎤 *"Terima kasih. Kami siap menerima pertanyaan dan masukan."*

---

## Lampiran (siapkan, jangan ditampilkan kecuali ditanya)

- Tabel hasil lengkap per tier & seed (Tabel 4.1–4.6).
- Detail hyperparameter (Tabel 3.9).
- Arsitektur FreqCNN & FreqBlock residual (Gambar 3.8/3.9).
- Rumus generalization drop Δ = F1_in − F1_cross.
- Jawaban siap pakai: uji statistik (deskriptif, 3 seed), ablation SE (rencana lanjutan), kenapa bukan early fusion (agar kontribusi terpisah).

---

### Catatan penyaji
- Konsisten dengan narasi **komparatif**, hindari kata "meningkatkan/membuktikan peningkatan".
- Slide inti yang wajib lancar: **16, 17, 19, 20, 22**.
- Bila ditanya di luar slide, rujuk `PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md`.
</content>
