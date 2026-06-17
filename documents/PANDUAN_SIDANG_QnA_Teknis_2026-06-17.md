# Panduan Sidang — Pemahaman Teknis & Tanya-Jawab

> Tujuan: memahami **alur dan alasan** (bukan menghafal), supaya bisa menjawab dengan kata-kata sendiri. Semua angka di sini sesuai kode & hasil final (d28efae).

---

## 0. Pitch 30 detik (kalau diminta "jelaskan singkat penelitian Anda")

"Kami melakukan **studi komparatif**: membandingkan tiga model deteksi deepfake — hanya spasial (XceptionNet), hanya frekuensi (FreqCNN), dan gabungan keduanya (hybrid). Tujuannya **mengukur seberapa besar kontribusi domain frekuensi**, terutama untuk generalisasi lintas dataset. Hasilnya: model spasial paling kuat, cabang frekuensi nyaris setara tebakan acak, dan hybrid tidak mengungguli spasial. Jadi temuan utama kami adalah **hasil negatif yang terjelaskan secara ilmiah**: pada konfigurasi yang diuji, FFT tidak membantu, bahkan bisa jadi sumber noise."

Kata kunci yang harus selalu muncul: **komparatif, kontribusi, generalisasi lintas dataset, hasil negatif yang dianalisis.**

---

## 1. FLOW TEKNIS END-TO-END (wajib dikuasai 1 orang minimal)

Bayangkan satu video masuk, lalu ikuti perjalanannya:

```
VIDEO
 └─(1) Ekstraksi frame @5 FPS, maks 50 frame/video
     └─(2) Deteksi & crop wajah (MTCNN, margin 0,3) → 224×224
         ├─ Representasi A: RGB 224×224 (untuk cabang SPASIAL)
         └─ Representasi B: peta FFT log-magnitude 1-kanal (untuk cabang FREKUENSI)
             └─(3) Split per-VIDEO (70/15/15) → cegah kebocoran
                 └─(4) Tiga model dilatih terpisah:
                       • SPATIAL : RGB → XceptionNet → logit
                       • FREQ    : FFT-map → FreqCNN → logit
                       • HYBRID  : (RGB→Xception) + (FFT→FreqCNN) → fusi → logit
                     └─(5) Latih: AdamW + AUC sebagai metrik seleksi
                         └─(6) Evaluasi: in-dataset & cross-dataset, 3 seed
```

**Cara membuat peta FFT (langkah 2, representasi B):**
RGB → grayscale (luminansi, ITU-R BT.601) → FFT 2D → `fftshift` (frekuensi rendah ke tengah) → ambil **magnitude** → **high-pass** (menekan frekuensi rendah/DC) → **log** (`log1p`, kompres rentang dinamis) → **normalisasi z-score** (per dataset).
**Poin penting:** kami hanya menyimpan **magnitudo**, **fase dibuang**. (Ini salah satu alasan kegagalan — lihat Q11.)

**Alur internal tiap model:**

| Model | Alur | Output |
|---|---|---|
| **Spatial** | RGB 224×224 → XceptionNet (depthwise separable conv, pretrained ImageNet, ~22 jt param) → fitur ~2048-d → FC → 1 logit | prob fake |
| **Freq** | FFT-map 1-kanal → FreqCNN (5 blok konv residual, base 64 kanal, ~4 jt param) → fitur 512-d → FC → 1 logit | prob fake |
| **Hybrid** | RGB→Xception→**256-d** ; FFT→FreqCNN→**256-d** ; concat→**512-d** ; **SE gate** (512→128→512, sigmoid, membobot tiap kanal) ; → FC 512→128→1 | prob fake |

logit → `sigmoid` → probabilitas fake → bandingkan dengan ambang (θ=0,5, plus ambang optimal **Youden J = TPR − FPR**).

**Setelan latih (kalau ditanya detail):** AdamW (lr 2e-4, weight decay 1e-4, **differential LR**: backbone lebih kecil dari head), label smoothing 0,05, warmup 2 epoch lalu cosine decay, gradient accumulation 2, gradient clipping, mixed precision (AMP), backbone XceptionNet **dibekukan 3 epoch pertama** lalu di-unfreeze, early stopping (patience pada **val AUC**), maks 30 epoch, 3 seed (0,1,2).

---

## 2. Angka yang harus hafal (cukup ini)

| Hal | Nilai |
|---|---|
| Spatial AUC in-dataset | hingga **~0,97** (terbaik) |
| Freq AUC | **0,55–0,59** (≈ tebakan acak) |
| Hybrid vs Spatial | hybrid **tidak mengungguli** spatial |
| Cross-dataset AUC (semua model) | turun ke **~0,63–0,65** |
| Recall collapse terparah | arah **CDF→FFPP**, recall ≈ **0,08** |
| Gen drop F1 (FFPP→CDF) | hybrid **+0,027** vs spatial **+0,116** (hybrid drop lebih kecil di arah ini) |
| Dataset | FFPP (4 metode manipulasi, c23) & Celeb-DF v2 (1 metode) |
| Ukuran sampel | 100 / 250 / 500 / 750 video |

---

## 3. Q&A — DASAR TEORI

**Q1. Perbedaan domain spasial dan frekuensi?**
Spasial = nilai piksel langsung (tekstur, warna, bentuk, blending). Frekuensi = citra diubah dengan FFT menjadi "seberapa banyak pola berulang halus/kasar" yang ada. Frekuensi rendah = struktur global (bentuk wajah, pencahayaan); frekuensi tinggi = detail halus & artefak. Intuisi: spasial melihat *apa* yang tampak, frekuensi melihat *pola periodik* yang tak kasat mata.

**Q2. Mengapa artefak GAN muncul pada frekuensi tinggi?**
GAN membuat citra dengan operasi *up-sampling* (transposed convolution). Operasi ini tidak sempurna mereproduksi statistik frekuensi citra alami, sehingga meninggalkan pola periodik (*checkerboard*) dan kelebihan/kekurangan energi di frekuensi menengah-tinggi (Odena; Durall; Zhang). Inilah "sidik jari GAN".

**Q3. Fungsi FFT dalam penelitian ini?**
FFT mengubah frame menjadi peta magnitudo frekuensi, supaya cabang frekuensi bisa "melihat" sidik jari GAN yang tak terlihat di domain spasial. FFT adalah jembatan dari piksel ke representasi yang menonjolkan artefak spektral.

**Q4. Mengapa XceptionNet?**
Karena XceptionNet adalah *baseline* standar dan kuat untuk deteksi deepfake (dipakai sebagai backbone di FaceForensics++). Arsitekturnya pakai *depthwise separable convolution* yang efisien, dan tersedia *pretrained* ImageNet (transfer learning) sehingga belajar cepat dengan data terbatas.

**Q5. Fungsi SE-Gating?**
Setelah fitur spasial dan frekuensi digabung (512-d), SE block belajar **bobot kepentingan tiap kanal** (512→128→512→sigmoid, lalu dikalikan). Idenya: biar model bisa "mengecilkan" kanal yang tidak berguna dan "membesarkan" yang berguna. **Catatan jujur:** dalam hasil kami, SE **tidak cukup** menekan cabang frekuensi yang buruk sepenuhnya (lihat Q11).

---

## 4. Q&A — METODOLOGI

**Q6. Mengapa late fusion?**
Late fusion = tiap domain diekstraksi fiturnya **terpisah** lalu digabung di akhir. Dipilih karena: (a) bisa pakai backbone XceptionNet pretrained apa adanya, (b) memudahkan **ablation** (kami bisa uji spatial-saja & freq-saja dengan komponen yang sama), (c) modular dan reproducible. Karena fokus kami **membandingkan kontribusi**, late fusion paling cocok untuk mengisolasi peran tiap domain.

**Q7. Mengapa tidak early fusion?**
Early fusion (RGB+FFT jadi 4 kanal masuk ke satu XceptionNet) **kami sediakan di kode** (`EarlyFusionXception`) tapi bukan fokus. Masalahnya: early fusion mencampur dua domain sejak awal sehingga **sulit memisahkan kontribusi masing-masing** — bertentangan dengan tujuan komparatif kami. Late fusion lebih bersih untuk ablation. (Kalau ditanya "sudah coba?" jawab: arsitekturnya ada, tapi tidak dijadikan fokus karena tidak mendukung tujuan pemisahan kontribusi.)

**Q8. Mengapa FaceForensics++ dan Celeb-DF?**
Keduanya benchmark internasional standar. FFPP punya **4 metode manipulasi** (beragam), Celeb-DF v2 punya **1 metode** tapi kualitas tinggi & realistis. Kombinasi keduanya memungkinkan **evaluasi cross-dataset** (latih di satu, uji di lain) untuk menguji generalisasi — justru inti penelitian kami.

**Q9. Mengapa split per video?**
Karena satu video menghasilkan banyak frame yang sangat mirip. Kalau split per-frame, frame dari video yang sama bisa bocor ke train DAN test sekaligus. Kami split **per ID video** (70/15/15) supaya tidak ada video yang muncul di dua set.

**Q10. Apa itu data leakage?**
Kebocoran data = informasi dari test set "bocor" ke training, membuat hasil **palsu tinggi**. Dalam kasus kami, bahaya utamanya frame-leakage antar split video. Makanya split per-video (Q9). Ini bukti metodologi kami ketat.

---

## 5. Q&A — HASIL

**Q11. Mengapa model frekuensi gagal? (PERTANYAAN INTI)**
Empat alasan (urut dari kuat):
1. **Artefak rusak oleh praproses.** MTCNN crop membuang konteks tepi/latar, dan kompresi c23 menekan frekuensi tinggi — justru tempat sidik jari GAN berada (sesuai Mejri).
2. **Fase dibuang.** Kami hanya pakai spektrum magnitudo. Padahal fase membawa sebagian besar info struktural (Oppenheim & Lim), dan metode SPSL membuktikan fase informatif (Liu).
3. **Bias bawaan CNN.** CNN cenderung pakai tekstur & belajar frekuensi rendah dulu (Geirhos; Rahaman; Wang). FreqCNN dangkal sulit menemukan selektivitas frekuensi yang tepat tanpa bantuan arsitektur.
4. **Representasi terlalu sederhana.** Satu peta magnitudo FFT mentah ke CNN dangkal, bukan dekomposisi frequency-aware seperti metode SOTA.

**Q12. Mengapa hybrid tidak lebih baik dari spatial?**
Karena hybrid = spatial (bagus) + frekuensi (≈ acak). Cabang frekuensi yang buruk **menyuntikkan noise** ke fitur gabungan, dan SE gating tidak cukup menekannya. Jadi "menambahkan sesuatu yang acak ke sesuatu yang bagus" tidak menambah, malah bisa mengganggu.

**Q13. Apa arti AUC 0,55?**
AUC = peluang model memberi skor lebih tinggi ke sampel fake dibanding real, untuk pasangan acak. AUC 0,5 = **tebakan koin**. 0,55–0,59 = **nyaris acak**, hampir tidak ada kemampuan diskriminatif. (1,0 = sempurna.) Jadi cabang frekuensi praktis tidak belajar pola yang berguna.

**Q14. Mengapa recall collapse pada cross-dataset?**
Recall fake = persentase fake yang berhasil ditangkap. Saat diuji di dataset lain (distribusi baru), model jadi cenderung memprediksi semuanya "real", sehingga banyak fake lolos → recall jatuh (terparah CDF→FFPP, ≈0,08). Penyebabnya **domain shift**: model dilatih pada artefak satu dataset, gagal mengenali artefak generator/kondisi rekaman yang berbeda.

**Q15. Apakah hasil ini berarti FFT tidak berguna?**
**Tidak.** Yang kami tunjukkan: FFT tidak membantu **pada konfigurasi ini** (magnitudo saja, FreqCNN dangkal, crop+c23, fusi sederhana). Artefak frekuensi tetap ada (Durall, Zhang); kemampuan **mengeksploitasinya** yang kondisional. Ini **kondisi batas**, bukan vonis bahwa frekuensi mutlak tak berguna.

---

## 6. Q&A — KRITIS (penentu nilai)

**Q16. Jika penelitian diulang, apa yang diubah?**
Tiga hal konkret: (1) **sertakan fase** (mis. pendekatan SPSL), bukan magnitudo saja; (2) **kurangi kerusakan artefak** — FFT pada frame penuh/kompresi lebih rendah; (3) **fusi & cabang frekuensi lebih canggih** (atensi frekuensi, FreqCNN lebih dalam) daripada konkatenasi + SE sederhana.

**Q17. Jika diberi GPU tak terbatas, eksperimen berikutnya?**
(a) **Ablation SE-gating** (hybrid dengan vs tanpa SE) untuk mengukur peran SE; (b) representasi frekuensi alternatif (DCT, wavelet, magnitudo+fase); (c) **pemodelan temporal** antar-frame (artefak deepfake punya jejak temporal); (d) data & ukuran sampel lebih besar; (e) **uji signifikansi statistik** (Wilcoxon/paired t-test) atas lebih banyak seed.

**Q18. Mengapa tetap bernilai walau hipotesis tidak terbukti?**
Karena **hasil negatif yang terbukti dan terjelaskan** adalah kontribusi ilmiah yang sah. Kami menantang asumsi umum "tambah FFT pasti lebih baik" dengan bukti kuantitatif, dan menjelaskan *mengapa* gagal. Ini mencegah peneliti lain mengulangi jalan buntu yang sama. Dalam sains, mengetahui *apa yang tidak bekerja dan kenapa* sama berharganya.

**Q19. Kontribusi ilmiah utama?**
1. **Studi komparatif terkontrol** (3 model × 2 dataset × 3 seed) dengan **evaluasi cross-dataset** yang jarang dilakukan di level S1.
2. **Bukti kuantitatif** bahwa kontribusi domain frekuensi **terbatas dan kondisional** pada konfigurasi yang diuji.
3. **Analisis akar penyebab** kegagalan cabang frekuensi (fase hilang, bias CNN, kerusakan artefak, fusi sederhana) + **posisi temuan terhadap literatur** (kondisi batas, bukan kontradiksi).

**Q20. Jika reviewer paper menolak, kritik paling mungkin?**
Jujur akui dua hal: (a) **tidak ada uji signifikansi statistik** (baru mean±std atas 3 seed) — jawab: perbedaan dibahas deskriptif, dan arah temuan konsisten; (b) **cabang frekuensi mungkin under-engineered** (magnitudo saja, FreqCNN dangkal) sehingga kegagalan bisa karena implementasi, bukan domain frekuensi itu sendiri — jawab: **justru itu temuan kami** — kami menandai bahwa pendekatan frekuensi "naif" tidak cukup, dan menyebut secara eksplisit apa yang dibutuhkan (fase, fusi beratensi). Sikap: **akui keterbatasan, lalu tunjukkan itu bagian dari kontribusi.**

---

## 7. Tips pembagian peran (3 orang)

- **Orang A (alur & arsitektur):** kuasai Bagian 1 & Q1–Q7 (flow, FFT, XceptionNet, SE, fusi).
- **Orang B (data & metodologi):** kuasai Q8–Q10 (dataset, split per-video, leakage) + setelan latih.
- **Orang C (hasil & pertahanan):** kuasai Bagian 2 + Q11–Q20 (angka, kenapa gagal, nilai ilmiah, kritik).
- **Semua wajib bisa** Pitch 30 detik (Bagian 0) dan Q15/Q18/Q19 (kenapa tetap bernilai).

**Prinsip menjawab:** jujur > defensif. Kalau hasil negatif, **bingkai sebagai temuan**, bukan kegagalan. Selalu kembalikan ke: *"kami membandingkan, bukan menjanjikan peningkatan."*
</content>
