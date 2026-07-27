# Sidang — Fact-Check & Q&A (Living Document)

> Dokumen ini dipakai untuk memverifikasi fakta/pernyataan thesis terhadap **kode aktual** dan **data hasil run**, sekaligus menyiapkan jawaban sidang.
> Setiap kali ada pertanyaan/pernyataan/fakta baru, dokumen ini **di-update** (tambah item baru di bawah).
>
> Legenda verdict: ✅ BENAR · 🟡 BENAR TAPI PERLU DIPERTEGAS · 🔴 KELIRU/OVERSTATED
>
> Konvensi referensi kode: `path:baris` relatif terhadap `deepfake_hybrid/`.
> Live .docx dapat dibaca via symlink repo-root `live-thesis-document.docx` (unzip `word/document.xml`).
> Terakhir diperbarui: 2026-06-30.

## Daftar Item

1. [Rasio sampling 50:50 real vs fake](#item-1)
2. [Kenapa pembagian 70/15/15? (bukan 50/25/25 atau 80/10/10)](#item-2)
3. [FFT untuk &#34;ekstraksi fitur spektral&#34; — benar, atau seharusnya &#34;melihat high frequency&#34;?](#item-3)
4. [High frequency dipakai, low frequency &#34;tidak digunakan&#34; — benar?](#item-4)
5. [Sudah tahu fase &gt; magnitudo di BAB II, kenapa tetap pakai magnitudo saja? (handicap / rescope?)](#item-5)
6. [Deskripsi late fusion BAB II: &#34;concat → classifier&#34; — padahal ada proyeksi + SE gating di antaranya?](#item-6)
7. [🔴 &#34;Kedua strategi fusion (early + late) diimplementasikan DAN dievaluasi&#34; — padahal hanya late fusion yang dievaluasi](#item-7)
8. [Referensi: apa itu &#34;power spectrum&#34; (Durall et al. 2020) dan hubungannya ke representasi FFT kita](#item-8)
9. [&#34;Local&#34; vs &#34;global&#34; (SpecXNet) — kalian global atau lokal untuk spasial &amp; frekuensi?](#item-9)
10. [🔴 &#34;XceptionNet unggul pada FF++, DFDC, dan Celeb-DF [13, 7]&#34; — referensi hanya mendukung FF++](#item-10)
11. [🔴 &#34;Dalam penelitian ini FFT jadi kanal keempat input XceptionNet + DSC cocok&#34; — itu early fusion, bukan flow kita](#item-11)
12. [🔴 &#34;korelasi spasial (cross-channel) dan korelasi antarkanal (cross-spatial)&#34; — label Inggris tertukar](#item-12)
13. [🟡 Repetisi: pembuka seksi DSC &amp; §2.7 XceptionNet mengulang hal sama (+ dua daftar keunggulan tumpang-tindih)](#item-13)
14. [✅ &#34;SE block &gt; konkatenasi sederhana&#34; padahal kita pakai konkatenasi — kontradiksi? TIDAK](#item-14)
15. [🟡 Tingkat kompresi FFPP: HQ &amp; LQ tak diberi label c23/c40 (benar HQ=c23, LQ=c40)](#item-15)
16. [🔴 Daftar &#34;Artefak Spasial&#34;: butir (d) &#34;ekspresi antar-frame&#34; itu TEMPORAL, bentrok dgn frame-level](#item-16)
17. [🟡 Struktur membingungkan: dikotomi artefak spasial/frekuensi diulang 3x dengan 3 format berbeda](#item-17)
18. [🟡 &#34;Alasan Pemilihan FFPP&#34;: 3 klaim faktual tanpa sitasi (+ &#34;GAN dan non-GAN&#34; kurang tepat)](#item-18)
19. [🟡 Paragraf Celeb-DF: angka BENAR, tapi sitasi [18] salah tunjuk (harusnya Li et al.) + daftar tanpa penutup](#item-19)
20. [🟡 Alur preprocessing: 7 langkah semua ADA, tapi urutan salah + menyembunyikan percabangan RGB/FFT](#item-20)
21. [🔴 Review §2.13/§2.13.1 Preprocessing: kontradiksi temporal + resize tanpa angka + 299 vs 224 + tabel under-describe FFT](#item-21)
22. [✅ Gradient Clipping (norma L2, rumus 2.29) — COCOK dgn kode (max_norm=5,0); tapi sitasi KOSONG](#item-22)
23. [🔴 Daftar metrik evaluasi HILANG AUC — padahal AUC metrik UTAMA (seleksi model + early stopping)](#item-23)
24. [❓ &#34;Kenapa komparatif? Ada paper yang menyarankan?&#34; — jawaban + sitasi](#item-24)
25. [❓ &#34;Kenapa nilai learning rate sekian? Ada paper? Kenapa tidak HP-tuning?&#34; — jawaban](#item-25)
26. [❓ &#34;SE gate malah menyeret turun hybrid — bagaimana kalau SE gate dihapus?&#34; — koreksi premis + data + ablation](#item-26)
27. [🔴 &#34;Dua metode utama ... terbukti unggul&#34; + &#34;sebagian besar penelitian memisahkan&#34; — tanpa sitasi &amp; kontradiktif](#item-27)
28. [🔴 EfficientNet dibandingkan 5× (+ angka Tabel 2.8) tapi TANPA sitasi &amp; tak ada di Daftar Pustaka; klaim perbandingan tak terdukung](#item-28)
29. [🔴 Kalimat penutup &#34;kombinasi FFT+Xception menghasilkan sistem lebih tangguh...&#34; terasa GARANSI — padahal studi komparatif dgn hasil negatif](#item-29)
30. [🟡 §2.18.3 ~75% RECAP dari §2.18.1 + §2.18.2 (FFT &amp; spatial diulang) — rewrite jadi seksi perbandingan yang lean](#item-30)
31. [🔴 Diagram BAB III (media_v2): gambar 3.4 flowchart salah (recreated), 3.8 FreqCNN &amp; 3.9 Hybrid pakai config lama (base=32/256-d)](#item-31)
32. [🔴/✅ §3.3.1 Ekstraksi Frame: naming/label/manifest BENAR; &#34;paralel&#34; &amp; &#34;FFPP n=1000 ~50.000&#34; SALAH (sekuensial di face-crop; n max=750)](#item-32)
33. [✅ Face cropping menaikkan performa spasial di FFPP — ADA referensi: Rössler et al. (2019), Tabel 1 (74,78%→95,73% c23)](#item-33)
34. [✅ Classifier head hybrid (Dropout 0,5 → Linear 512→128 → ReLU → Dropout 0,5 → Linear 128→1) — COCOK kode; catatan &#34;moderat&#34; untuk p=0,5 debatable](#item-34)
35. [🔴 &#34;Desain 3 varian menjawab RM1/2 yaitu membangun detektor lebih akurat...&#34; (docx 1397) — MISLEADING: salah nyatakan RM (sisa judul lama &#34;Peningkatan&#34;) + bertabrakan dgn temuan negatif](#item-35)
36. [✅ Transfer learning + backbone freezing 3 epoch → unfreeze epoch 4 — COCOK kode; minor: &#34;requires_grad(True)&#34; itu set atribut bukan pemanggilan, &#34;catastrophic forgetting&#34; longgar](#item-36)
37. [🟡 Loss (BCE + pos_weight + label smoothing): konten BENAR &amp; pos_weight betul dipakai, TAPI BAB III mengulang verbatim BAB II 2.31/2.32 + kontradiksi &#34;telah diuraikan&#34;](#item-37)
38. [✅ §3.5.2-3.5.8 (diff LR, LR schedule, AdamW, accum, clip, AMP, early stop) — SEMUA BENAR cocok kode](#item-38)
39. [🔴 §3.6 vs §3.6.1 repetitif (paragraf faktorial identik) + Tabel 3.12: &#34;Ukuran sampel CDF&#34; salah (berlaku kedua dataset) + total run/eval kosong (72/144)](#item-39)
40. [🟡 Paragraf Δ generalization drop (docx 1616) repetitif dgn BAB I/II — motivasi cross-dataset &amp; interpretasi Δ diulang; pola berulang BAB III re-motivasi+re-derive](#item-40)

---

## Status re-check terhadap WORD terbaru (2026-07-03)

**Sudah diperbaiki di .docx ✅:**

- [Item 10](#item-10) — klaim "XceptionNet unggul di FF++, DFDC, Celeb-DF" → "DFDC" sudah hilang.
- [Item 12](#item-12) — "cross-spatial" → sudah jadi "cross-channel" (line 599).
- [Item 16](#item-16) — butir temporal "ketidakkonsistenan ekspresi saat frame" → sudah hilang.
- [Item 11](#item-11) #2 (§2.7.3) — sudah ditulis ulang jadi late fusion (line 597). _(minor: typo "ynag"→"yang" 2×.)_
- [Item 7](#item-7) (line 420) — sudah "fokus late fusion; early fusion tidak dievaluasi".
- [Item 21](#item-21)-1 — kalimat temporal (flickering) di §2.13.1 → sudah hilang.

**Masih terbuka 🔴 (belum diperbaiki di .docx):**

- [Item 11](#item-11) #7 / [Item 7](#item-7) — **line 1476**: masih "...model spatial, hybrid, **dan early fusion**, backbone dibekukan...".
- [Item 11](#item-11) #8 — **line 812**: masih "...menambahkan informasi Frekuensi ... sebagai **channel 4**...".
- [Item 21](#item-21)-3 / [Item 11](#item-11) #5 — **Tabel 2.4** di .docx belum diganti dgn versi baru (`table/tabel_2_4_tahapan_preprocessing.html`).
- [Item 19](#item-19) — sitasi Celeb-DF **line 703** masih "[18]" (harusnya Li et al.).

---

## 🔬 AUDIT BAB II MENYELURUH terhadap WORD terbaru (2026-07-03) — 2213 paragraf

Cek per-item ke `.docx` saat ini. Ringkas: **mayoritas item BAB II SUDAH kamu perbaiki** (rewrite §2.9/§2.13/§2.15/§2.17/§2.18 sudah ditempel; EfficientNet dihapus total). Sisa yang perlu diubah relatif sedikit.

### ✅ Sudah memadai (terverifikasi di .docx sekarang)

| Item                          | Bukti fix                                                                                                  |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 10 (Xception unggul DFDC/CDF) | "DFDC" hilang total (0 hit)                                                                                |
| 12 (cross-spatial)            | jadi "cross-channel"                                                                                       |
| 13 (pembuka DSC repetitif)    | pembuka lama hilang                                                                                        |
| 15 (kompresi c23/c40)         | line 658-661: RAW/HQ(c23,CRF23)/LQ(c40,CRF40) + "pakai HQ (c23)" ✅                                        |
| 16 (butir temporal artefak)   | hilang                                                                                                     |
| 17 (artefak spasial/freq 3×)  | line 675: jadi pemetaan**per-teknik** (Deepfakes/Face2Face/...) ✅                                         |
| 18 (GAN dan non-GAN)          | frasa hilang                                                                                               |
| 20+21 (preprocessing)         | line 725-740:**bercabang** RGB/FFT, grayscale, high-pass, z-score ✅                                       |
| 27 (dua metode + gap)         | line 956: gap direframe + sebut SpecXNet/FSBI/FDM ✅                                                       |
| 28 (EfficientNet)             | **dihapus total** dari prosa & Tabel 2.8; MesoNet dikoreksi ke **83,10%**; ResNet-50 dibuang dari tabel ✅ |
| 29 (kalimat garansi)          | line 985+: direframe jadi "berpotensi/dilaporkan/menguji" ✅                                               |
| 30 (§2.18.3 recap)            | direwrite jadi**lean** (rujuk 2.18.1/2.18.2 + Tabel 2.9) ✅                                                |

### 🔴 Masih perlu diubah

1. **[Item 23](#item-23) — BELUM.** line 856 masih: "metrik ... meliputi _Confusion Matrix, Accuracy, Precision, Recall, dan F1-Score_. **Seluruh metrik dihitung berdasarkan hasil prediksi ...**" → **AUC masih hilang dari daftar** (padahal §2.16 nanti + BAB III/IV menyebut AUC metrik utama, line 894). Tambahkan AUC + kaveat "AUC dari skor probabilitas". **Ini yang paling penting tersisa di BAB II.**
2. **[Item 11](#item-11) #8 — BELUM.** line 812 masih "...menambahkan informasi Frekuensi ... sebagai **channel 4**..." (early fusion di prosa BAB II). Ganti ke cabang FreqCNN terpisah + late fusion.
3. **Tabel 2.8 — parameter MesoNet "4M" salah** → MesoNet/MesoInception-4 ~**28 ribu** parameter (~0,03M), bukan 4M. Juga caption "[3, 4, 13, 7]": angka FF++ sebenarnya dari **[4] Afchar & [7] Rössler** saja ([3] Haq = Celeb-DF, [13] SpecXNet tak menguji ini) → rapikan jadi [4, 7].

### 🟡 Typo pada rewrite yang sudah ditempel (kecil)

- line 597: "mekanisme **ynag** berbeda" → "**yang**".
- line 956: "**sebagai besar** dioptimalkan" → "**sebagian besar**".

### 🟢 Boleh dibiarkan / opsional

- [Item 5](#item-5) (framing fase Oppenheim) — pelunakan bersifat opsional; boleh tetap.
- [Item 6](#item-6) (§2.7 line 418 "digabungkan (concatenated) ... tanpa saling mengganggu") — deskripsi **konsep umum** late fusion di landasan teori; dapat diterima. Instansiasi spesifik sudah benar di line 597.
- [Item 19](#item-19) (Celeb-DF [18]) — di Daftar Pustaka sekarang FDM (Luo&Wang) lalu Li (Celeb-DF) berurutan; in-text FDM=[17], Celeb-DF=[18] → **tampak konsisten**. Tetap **refresh field (Ctrl+A→F9)** lalu spot-check bahwa [18] me-resolve ke Li et al.

### Kesimpulan

BAB II **sudah cukup memadai** — tinggal **3 perubahan wajib** (AUC di daftar metrik [Item 23]; "channel 4" line 812; parameter MesoNet 4M→~28K di Tabel 2.8) + **2 typo** (line 597, 956), lalu **refresh field sitasi** sekali untuk mengunci penomoran.

> ✅ **Ready copy-paste untuk semua sisa fix di atas:** **`documents/REVISI_BAB_II_FIX_Sisa_Audit_2026-07-03.md`** (find/replace per lokasi + checklist).

---

## 🔬🔬 CEK ULANG THOROUGH — ROUND 2 (2026-07-03, 2213 paragraf)

**6 fix audit: SEMUA sudah diterapkan ✅** (AUC masuk daftar metrik line 856; "channel 4" hilang; MesoNet param "~0,03 juta"; typo "ynag"/"sebagai besar" hilang).

**Diverifikasi BENAR (tidak perlu diubah):**

- **Rumus metrik §2.16** — contoh TP=180/FP=20/TN=160/FN=40 → Accuracy 85%, **Precision 90% = TP/(TP+FP)**, **Recall 81,8% = TP/(TP+FN)**, F1 85,7%. Semua **konsisten & benar** (rumus recall sudah benar). ✅
- **Rumus SE §2.8** — squeeze 512→128, excitation 128→512 sigmoid, scale, classifier Dropout(0,5)→Linear(512→128)→ReLU → **cocok dengan kode**. ✅

### 🔴 Temuan BARU yang masih perlu diubah

1. **Line 286 (intro §2.1) — "ResNet-50 ... akurasi di atas 90% pada FaceForensics++ [3, 5]" TAK TERDUKUNG.** Ini kembaran temuan [Item 28](#item-28) tapi di **intro** (belum tersentuh saat fix Tabel 2.8). Haq [3] = **Celeb-DF (79%)**, He [5] = ImageNet. Tak ada sumber ResNet-50 >90% di FF++.
   **Ganti:** "ResNet-50 memperkenalkan _residual learning_ untuk merepresentasikan fitur spasial yang lebih dalam (He et al., 2015), namun performanya pada deteksi deepfake dilaporkan lebih rendah dibanding XceptionNet dan menurun pada pengujian lintas dataset (Haq, 2021)."
   - Bonus di kalimat sama: "99,26% ... [6, 7]" — [6] Chollet = ImageNet (tak melaporkan angka FF++); cukup **(Rössler et al., 2019)**.

### 🟡 Temuan BARU kecil

2. **Line 462 — typo "Lao et al." → "Luo dan Wang"** (Frequency-Domain Masking, [17]). Di tempat lain (line 381/419/524) sudah benar "Luo dan Wang".
3. **Line 462 — sitasi menggantung setelah titik**: "...citra sintetis. **[11]**" dan "...antar-dataset. **[16]**" → pindahkan [11] & [16] ke **sebelum** titik (tempat lain, mis. line 380/381/496, sudah benar). Juga verba "membuktikan" → "menunjukkan" (lebih hati-hati).
4. **Statistik "96% ... pornografi non-konsensual [2]" muncul 2×** (line 285 intro bab & line 348 §2.1.1) — redundansi kecil; pertimbangkan sebut sekali (mis. hanya di §2.1.1) agar tidak berulang.

### Kesimpulan Round 2

BAB II **solid**. Rumus & angka metrik benar, SE benar, 6 fix terpasang. Sisa **1 wajib** (line 286 ResNet) + **3 kecil** (Lao→Luo, sitasi menggantung line 462, redundansi 96%). Setelah ini + refresh field, BAB II tuntas.

### ✅ VERIFIKASI FINAL (2026-07-03) — semua fix Round 2 SUDAH diterapkan

- **FIX 7** (line 286 ResNet >90% FFPP) → ✅ diganti: "...residual learning ... [5], namun performanya pada deteksi deepfake dilaporkan lebih rendah dibanding XceptionNet dan menurun lintas dataset [3]".
- **FIX 8** ("Lao et al." → "Luo dan Wang") → ✅.
- **FIX 9** (sitasi [11]/[16] dipindah ke sebelum titik) → ✅.
- **FIX 10** (statistik "96%" dari 2× → 1×) → ✅.
- 6 fix Round 1 tetap terpasang (AUC di metrik ✅, "channel 4" hilang ✅, EfficientNet hilang ✅).

**Sisa ultra-minor (opsional, tidak menghalangi):** line 286 "99,26% ... [6, 7]" — [6] Chollet = ImageNet, boleh di-drop jadi [7] saja; "membuktikan" → "menunjukkan" (line 462). Plus satu langkah mekanis: **Ctrl+A→F9** refresh field + spot-check sitasi Celeb-DF.

**STATUS BAB II: TUNTAS.** Semua temuan Item 1-30 + audit Round 1 & 2 sudah terselesaikan (atau opsional/dapat-diterima).

---

<a name="item-1"></a>

## Item 1 — "Pengambilan sampel dilakukan dengan rasio 50:50 antara kelas asli dan kelas manipulasi"

**Verdict: 🟡 BENAR, tapi tegaskan cakupannya = level VIDEO (bukan level frame).**

### Bukti kode

Diterapkan di pipeline kanonik `scripts/extract_frames.py:180-194` (bukan `sample_dataset.py`, itu skrip smoke-test lama):

```python
half = args.n_samples // 2
real_take = min(len(real_all), half)
fake_take = min(len(fake_all), args.n_samples - real_take)
selected = real_all[:real_take] + fake_all[:fake_take]
```

Lalu `scripts/build_splits.py:52-53` memakai `train_test_split(..., stratify=df["label"])`, sehingga rasio 50:50 **dipertahankan** di tiap subset train/val/test.

### Bukti data hasil run (manifest aktual)

| Run                     | Video           | Real           | Fake           |
| ----------------------- | --------------- | -------------- | -------------- |
| FFPP n100 / n250 / n500 | 100 / 250 / 500 | 50 / 125 / 250 | 50 / 125 / 250 |
| CDF n100 / n250 / n500  | 100 / 250 / 500 | 50 / 125 / 250 | 50 / 125 / 250 |

Semua **persis 50:50** di level video. Konsisten dengan BAB III v4 baris 104 ("pengambilan **video** dilakukan secara seimbang ... rasio 50:50").

### Catatan untuk sidang

- **50:50 itu di level VIDEO, bukan frame.** Model dilatih per-frame; `src/deepfake_data.py:79-81` ambil hingga `max_frames` per video, jadi jumlah frame per kelas bisa sedikit timpang. Karena itu `scripts/train.py:182-184` menghitung `pos_weight = n_neg / n_pos` (pengaman residual imbalance level frame; bernilai ~1.0 kalau benar seimbang).
- **50:50 di kode itu _best-effort_.** Kalau satu kelas kurang, kode menambal dari kelas mayoritas (`extract_frames.py:185-189`). Untuk FFPP (~1000 real) & CDF (~590-890 real), real selalu cukup untuk setengah sampel terbesar (butuh max 500 real di FFPP n1000, 375 di CDF n750), jadi 50:50 terealisasi.
- **Seed sampling di-hardcode = 42** (`extract_frames.py:174`), terpisah dari 3 seed training (0/1/2). Set video 50:50 yang sama dipakai di ketiga seed; yang berbeda hanya stokastisitas pelatihan.

**Frasa thesis paling akurat:** "pengambilan video secara seimbang (50:50 pada level video)".

---

<a name="item-2"></a>

## Item 2 — "Kenapa 70/15/15? Kenapa tidak 50/25/25 atau 80/10/10?"

**Verdict: ✅ Pilihan 70/15/15 dapat dipertahankan dengan baik.**

Referensi kode: `scripts/build_splits.py:18-19` (`--val-size 0.15`, `--test-size 0.15`), split bertingkat `train_test_split` dua tahap (baris 52-53), stratified by label, level video.

### Jawaban inti (3 argumen)

**1. Mengikuti konvensi benchmark FaceForensics++.**
Split resmi FF++ adalah **720 train / 140 val / 140 test video** dari 1000 video = **72% / 14% / 14%**. Jadi 70/15/15 pada dasarnya **mereplikasi rasio split kanonik FF++**, bukan angka yang dibuat sembarangan. Ini membuat hasil sebanding dengan literatur deteksi deepfake di dataset yang sama.

**2. Keseimbangan: cukup data latih untuk backbone besar, sekaligus set evaluasi yang stabil.**

- XceptionNet ≈ 22,8 juta parameter butuh data latih memadai. 70% memberi proporsi latih terbesar yang masuk akal **tanpa mengorbankan keandalan evaluasi**.
- 15% validasi penting karena **seleksi model & early stopping memakai AUC validasi** (`train.py`, kriteria best checkpoint by val AUC). Val terlalu kecil → sinyal AUC bising → checkpoint salah pilih / early stopping prematur.
- 15% test cukup besar untuk estimasi metrik yang relatif stabil.

**3. Kendala mengikat ada di tier sampel kecil (n=100), pada level video.**

- Split di level video, bukan frame (cegah kebocoran). Pada n=100: 15% = **15 video** untuk val dan 15 untuk test.
- Dengan **80/10/10**: val/test tinggal **10 video** → AUC sangat bising, terutama untuk model selection. Tidak layak pada tier kecil.
- Dengan **50/25/25**: latih turun ke **50 video** → XceptionNet kekurangan data, underfit, variansi antar-seed melonjak; sekaligus boros (25% test jauh lebih besar dari yang diperlukan untuk estimasi metrik).
- **70/15/15** = titik tengah: 70 video latih (cukup untuk fine-tuning + freeze/unfreeze backbone), 15 val (sinyal early stopping memadai), 15 test. Tiap video → hingga 50 frame, jadi metrik level frame tetap dihitung atas ~750 frame/subset, tetapi **diversitas video val/test** adalah batasan yang menentukan, dan 15 lebih aman daripada 10.

### Ringkas satu kalimat (untuk dilempar ke penguji)

> "70/15/15 mengikuti rasio split resmi FaceForensics++ (720/140/140 ≈ 72/14/14), memberi data latih cukup untuk backbone Xception sekaligus set validasi yang besarnya memadai untuk early stopping berbasis AUC; 80/10/10 membuat val/test hanya 10 video pada tier n=100 (AUC tidak stabil), sedangkan 50/25/25 menyusutkan data latih hingga model underfit."

---

<a name="item-3"></a>

## Item 3 — "Analisis frekuensi dilakukan menggunakan metode FFT untuk mengekstraksi fitur spektral yang merepresentasikan artefak sintesis"

**Verdict: 🟡 BENAR, tapi tidak lengkap — ada langkah _high-pass filtering_ yang menyaring spektrum ke arah frekuensi tinggi.**

### "Ekstraksi fitur spektral" — benar?

Ya. Pipeline FFT (`src/fft_utils.py:22-33`):

1. Grayscale → resize 224×224
2. `np.fft.fft2` → `fftshift` → `np.abs` (magnitude spectrum)
3. **High-pass mask** (lihat Item 4)
4. `log1p` → peta **FFT log-magnitude** 1-kanal

Peta log-magnitude inilah **representasi spektral**-nya, dan `FreqCNN` (`src/models/freq_cnn.py`) mempelajari fitur diskriminatif dari peta tersebut. Jadi "FFT untuk mengekstraksi fitur spektral" **akurat** sebagai deskripsi representasi input.

### "Bukan melihat high frequency?" — keduanya, tidak saling bertentangan

Dua framing ini **komplementer**, bukan kontradiktif:

- **Representasi** = peta spektral penuh (FFT log-magnitude 2D). ← inilah "fitur spektral"
- **Penekanan** = high-pass filter membobot peta itu ke arah frekuensi menengah-tinggi, tempat artefak sintesis (checkerboard dari up-convolution GAN, spectral roll-off anomal) terkonsentrasi.

Artinya: FFT memang menghasilkan fitur spektral (benar), dan dari fitur spektral itu **komponen frekuensi tinggi yang ditonjolkan** (juga benar). Pernyataan thesis tidak salah, hanya **menghilangkan** bagian high-pass-nya.

### Dukungan

- Thesis v4 sudah benar mendokumentasikan ini di **§3.3.2.3** (`BAB_III_Tahapan_Pelaksanaan_v4.md:156-170`): "_Magnitude Spectrum_, _High-Pass Filtering_, dan _Log Scaling_".
- Referensi: Durall et al. 2020 (spectral distribution), Odena et al. 2016 (checkerboard artifacts), Mejri et al. (Leveraging High-Frequency Components) — semua ada di `thesis_reference/`.

**Saran:** kalau ada ruang, perlengkap kalimat menjadi: "...menggunakan FFT untuk menghasilkan representasi spektral (log-magnitude) yang **kemudian ditekankan pada komponen frekuensi tinggi via _high-pass filter_** guna menonjolkan artefak sintesis."

---

<a name="item-4"></a>

## Item 4 — "High frequency dipakai untuk mendeteksi artefak, sedangkan low frequency tidak digunakan"

**Verdict: 🔴 OVERSTATED / kurang tepat. Yang benar: low frequency DITEKAN (di-atenuasi), bukan "tidak digunakan".**

### Bukti kode — high-pass-nya _soft_, bukan _hard cut_

`src/fft_utils.py:9-19`:

```python
def _highpass_mask(size, cutoff=0.15):
    ...
    sigma = cutoff * size                 # 0.15 * 224 ≈ 33.6 px
    mask = 1.0 - np.exp(-(dist**2) / (2*sigma**2))
    return mask
```

Diterapkan sebagai perkalian: `magnitude = magnitude * mask` (`fft_utils.py:30-31`), aktif secara default (`highpass=True`) baik di cache (`save_fft_cache` → `image_to_fft_logmag`) maupun di fallback live. Jadi input training **memang** sudah high-pass.

Sifat mask Gaussian `H = 1 − exp(−d²/2σ²)`:

| Posisi (jarak dari pusat) | Nilai mask | Efek                                           |
| ------------------------- | ---------- | ---------------------------------------------- |
| Pusat / DC (d=0)          | **0,00**   | DC dihilangkan                                 |
| d = σ (≈34 px)            | ~0,39      | low-freq**ditekan kuat**, tetap lewat sebagian |
| d = 2σ (≈67 px)           | ~0,86      | mid-freq sebagian besar lewat                  |
| Tepi (high freq)          | →1,00      | high-freq dipertahankan penuh                  |

### Kenapa pernyataan itu keliru

1. **Roll-off mulus, bukan biner.** Hanya DC murni yang dikali ~0. Komponen low/mid-freq **tetap masuk** ke FreqCNN dengan bobot tereduksi. Jadi "low frequency tidak digunakan" terlalu kuat.
2. **Thesis sendiri memakai kata yang benar:** `BAB_III...v4.md:164` menulis "**menekan dominasi** komponen frekuensi rendah" (suppress), bukan "membuang". Pernyataan user lebih ekstrem dari yang sebenarnya diimplementasikan.
3. **FreqCNN tetap menerima peta 224×224 utuh** (low+high, hanya dibobot). Doc depth=5 (`...v2.md:488`) bahkan menyebut model mengekstraksi "dari artefak frekuensi rendah (distribusi energi global) hingga anomali frekuensi tinggi" — jadi info low-freq tidak hilang.

### Frasa yang benar (untuk sidang & thesis)

> "Komponen frekuensi **tinggi diperkuat** dan komponen frekuensi **rendah ditekan (di-atenuasi)** melalui _Gaussian high-pass filter_ (cutoff β=0,15), karena artefak sintesis deepfake terkonsentrasi pada frekuensi menengah-tinggi sedangkan frekuensi rendah sebagian besar merepresentasikan struktur global wajah yang kurang diskriminatif. Frekuensi rendah **tidak dibuang sepenuhnya**, hanya dikurangi dominasinya."

### Jika penguji menekan: "kenapa tidak buang total low-freq?"

Karena (a) transisi mulus menjaga sebagian konteks struktural & mencegah artefak ringing dari pemotongan tajam, dan (b) sebagian sinyal diskriminatif (mis. distorsi distribusi spektral / spectral roll-off, Durall et al. 2020) berada di pita menengah, bukan hanya tepi — sehingga atenuasi bertahap lebih aman daripada hard cut.

---

<a name="item-5"></a>

## Item 5 — "Di BAB II kalian sudah tahu fase membawa lebih banyak info daripada magnitudo. Kenapa tetap _kekeh_ meng-_handicap_ cabang frekuensi dengan magnitudo saja? Bukankah lebih baik penelitian di-_scope_ ulang?"

**Verdict: ✅ Bisa dipertahankan kuat — ini keterbatasan desain yang DISENGAJA, terdokumentasi konsisten, dan justru memperkuat narasi komparatif. JANGAN di-rescope.**

### Lokasi di .docx (live)

- **BAB II §2.4.3 "Spektrum Magnitudo dan Fase"** (paragraf yang ditanyakan) — memperkenalkan magnitudo vs fase, mengakui keterbatasan magnitudo-saja, mengutip Oppenheim & Lim [25] dan Liu et al. SPSL [26].
- **Metodologi** (≈hal. representasi frekuensi): "Spektrum ... dikonversi menjadi satu kanal ... menonjolkan pola energi frekuensi tinggi."
- **BAB V Keterbatasan #3**: "cabang frekuensi ... hanya menggunakan spektrum magnitudo ... dan membuang spektrum fase ... representasi spektral yang tidak lengkap sejak awal."
- **BAB V Saran/Future Work**: merekomendasikan menyertakan fase (SPSL) sebagai penelitian lanjutan.

Jadi ini **bukan kelalaian yang ketahuan**, melainkan batas desain yang sengaja dinyatakan dan konsisten di tiga bab. Itu sendiri adalah aset pertahanan.

### Kunci pertahanan (4 argumen, urut kekuatan)

**1. Ini STUDI KOMPARATIF, bukan studi optimasi representasi frekuensi.**
Judulnya "Studi Komparatif Kinerja ... Arsitektur Hybrid ... terhadap Model Domain Tunggal." Variabel yang diteliti adalah **arsitektur** (hybrid vs single-domain), dengan **representasi frekuensi dijaga tetap (fixed)** pada pilihan kanonik. Supaya perbandingan terkontrol dan sebanding dengan literatur, representasinya dipatok ke yang **paling baku** di domain ini: log-magnitude spectrum (Durall et al. 2020, Frank et al. 2020, Wang et al. 2020). Mengganti ke fase/SPSL akan **mengubah variabel bebas** dan menjadikannya penelitian yang berbeda (perbandingan representasi: magnitudo vs fase vs gabungan) — itu skripsi lain, bukan milik kami.

**2. Oppenheim & Lim itu tentang STRUKTUR PERSEPTUAL, bukan deteksi ARTEFAK — dua klaim itu tidak bertentangan.** ← _senjata utama_
Hasil Oppenheim & Lim (1981) menunjukkan fase mendominasi **struktur perseptual citra natural** (tepi, bentuk, keterbacaan rekonstruksi). Tetapi **deteksi deepfake bukan rekonstruksi struktur** — ia menargetkan **anomali statistik spektral / artefak** (puncak spektral up-sampling GAN, spectral roll-off, replika checkerboard), dan artefak ini justru **termanifestasi kuat pada spektrum magnitudo** (Durall, Frank, Wang). Jadi:

> "Fase membawa lebih banyak info **struktur**" dan "magnitudo adalah kanal **artefak** yang sah" **keduanya benar dan tidak saling meniadakan.**

SPSL (Liu et al. [26]) menunjukkan fase **menambah** sinyal artefak yang **komplementer** (artefak up-sampling kumulatif) — _bukan_ membuktikan magnitudo tak berguna. Maka framing "fase lebih penting → magnitudo = handicap" adalah **kesimpulan yang melompat**: yang benar, fase itu **komplementer dan menjadi arah lanjutan**, bukan pengganti yang membuat magnitudo sia-sia.

**3. Keterbatasan ini MENJELASKAN temuan empiris — itu sains yang baik, bukan lubang.**
Hasil kami: cabang frekuensi adalah model **terlemah**, dan hybrid didominasi cabang spasial (ranking spatial ≥ hybrid > freq, konsisten lintas seed & tier 250/500/750). Paragraf BAB II ini memberi **penjelasan mekanistik** atas hasil negatif itu: representasi magnitudo-saja (ditambah hilangnya sidik jari spektral akibat face-crop & kompresi) → cabang frekuensi lemah. Tanpa paragraf ini, hasil lemah itu **tak terjelaskan**; dengan paragraf ini, hasil jadi **interpretable dan jujur**. Penguji menghargai limitation yang **memprediksi & menjelaskan** hasil, bukan menyembunyikannya.

**4. Justifikasi praktis: magnitudo-saja itu baku, reproducible, dan bersih secara arsitektur.**
Single-channel → cocok dengan FreqCNN 1-kanal, bisa di-_cache_ sebagai `.npy`. Fase **tidak** drop-in: ada _phase wrapping_, sensitif noise, tidak translation-invariant; SPSL butuh pemrosesan _shallow_ khusus. Menyertakan fase secara benar = arsitektur + eksperimen baru = **scope creep** di luar studi komparatif.

### Jawaban siap-ucap (30 detik)

> "Penelitian kami adalah **studi komparatif arsitektur**, jadi representasi frekuensi sengaja kami patok pada bentuk **paling baku** di literatur, yaitu log-magnitude spectrum, agar perbandingan hybrid vs domain-tunggal terkontrol dan sebanding. Soal Oppenheim & Lim: hasil itu menyatakan fase dominan untuk **struktur perseptual citra**, sedangkan deteksi deepfake menargetkan **artefak spektral** yang justru kuat di magnitudo, jadi keduanya tidak bertentangan — fase bersifat **komplementer**. Kami **tidak mengklaim** cabang frekuensi kami yang terkuat; kami melaporkan apa adanya bahwa ia terlemah, dan paragraf BAB II itulah yang **menjelaskan kenapa**. Penggunaan fase (mis. SPSL) sudah kami nyatakan eksplisit sebagai **keterbatasan dan saran penelitian lanjutan** di BAB V. Mengganti ke fase sejak awal berarti menjawab **pertanyaan riset yang berbeda** (perbandingan representasi), bukan pertanyaan kami (perbandingan arsitektur)."

### Rebuttal lanjutan kalau ditekan lebih jauh

- **"Fase kan tinggal ditambah, murah?"** → Tidak murah/bersih: butuh unwrapping, noise-sensitive, bukan flag konfigurasi; SPSL metode khusus. Implementasi yang benar = arsitektur + matriks eksperimen baru.
- **"Cabang frekuensi lemah, bukankah hybrid jadi tak valid?"** → Tidak. Hybrid tetap memetik manfaat dari cabang spasial; perbandingan kami justru **mengukur seberapa besar (atau kecil) kontribusi frekuensi** — dan jawabannya (kontribusi terbatas pada kondisi ini) adalah temuan ilmiah yang sah dan jujur.
- **"Harusnya pakai fase dari awal?"** → Itu menjawab pertanyaan "representasi frekuensi terbaik", bukan "perbandingan arsitektur". Dua skripsi berbeda; kami memilih dan **membatasi** milik kami secara eksplisit.

### Opsional — pelunakan teks BAB II (kalau mau menutup celah di paragrafnya sendiri)

Kerentanan satu-satunya: kalimat "rekonstruksi hanya dari magnitudo justru kehilangan struktur" bisa dibaca seakan magnitudo inferior **secara menyeluruh**. Bila ingin pre-empt di teks (bukan wajib), sisipkan satu klausa setelah kalimat Oppenheim:

> "Perlu ditekankan bahwa hasil tersebut berlaku untuk **rekonstruksi struktur perseptual citra natural**; dalam konteks deteksi, spektrum **magnitudo** tetap menjadi kanal yang mapan untuk menangkap **artefak distribusi spektral** akibat sintesis generatif (Durall et al., 2020), sehingga fase bersifat **komplementer** terhadap magnitudo, bukan substitusi."

Ini mengubah paragraf dari "mengakui kelemahan" menjadi "mengakui kelemahan **sambil membingkai fase sebagai pelengkap**", sehingga lebih sulit dijadikan jebakan. (Edit dilakukan dari Drive — teks di atas tinggal di-_paste_.)

---

<a name="item-6"></a>

## Item 6 — Deskripsi late fusion di BAB II ("...digabungkan _concatenated_ dan diteruskan ke lapisan klasifikasi bersama") vs implementasi aktual (ada proyeksi + SE gating)

**Verdict: 🟡 BENAR sebagai deskripsi UMUM (landasan teori), tapi merupakan PENYEDERHANAAN. Pengamatanmu tepat — model aktual menyisipkan proyeksi-256 lalu SE gating di antara concat dan classifier. Bukan kontradiksi: kedua langkah itu sudah didokumentasikan di tempat lain (BAB II §SE-Net + BAB III §HybridTwoBranch).**

### Alur AKTUAL model (verifikasi kode `src/models/hybrid_fusion.py`)

```
RGB → Xception → spatial_feat (2048)  → Linear(2048→256)+BN+ReLU ┐   (spatial_proj, L35-39)
                                                                 ├ cat → 512 (L64)
FFT → FreqCNN.features → flatten (512) → Linear(512→256)+BN+ReLU ┘   (freq_proj, L40-44)
                                                                 │
   → SE gate(512): Lin(512→128)→ReLU→Lin(128→512)→Sigmoid, lalu x*gate(x)   (L11-24, dipanggil L65)
   → classifier: Dropout(0.5)→Lin(512→128)→ReLU→Dropout(0.5)→Lin(128→1)     (L48-54, dipanggil L66)
```

Jadi urutan sebenarnya: **proyeksi → concat → SE gating → classifier (yang diawali Dropout).** Persis seperti dugaanmu: setelah concat ada **SE gating** dulu, baru **classifier yang dimulai dengan dropout**.

### Apa yang BENAR di paragraf BAB II (line 418 docx)

- ✅ Dua cabang independen mengekstraksi fitur terpisah — cocok (`self.spatial(rgb)`, `self.freq.features(fft)`).
- ✅ Cabang spasial CNN (misalnya XceptionNet) — cocok.
- ✅ Cabang frekuensi CNN lebih ringan — cocok (FreqCNN ~0,7 jt vs Xception ~22,8 jt param).
- ✅ Digabungkan (_concatenated_) → akhirnya menuju lapisan klasifikasi — cocok.
- ✅ Fleksibilitas pilih arsitektur per domain — properti umum late fusion yang sah.

### Apa yang DIHILANGKAN (dua langkah, keduanya nyata di model)

1. **Proyeksi per-cabang ke 256-d (Linear+BN+ReLU)** sebelum concat — penyetara dimensi 2048 vs 512 supaya spasial tidak mendominasi.
2. **SE gating** pada vektor fusi 512-d — _channel attention_ adaptif sebelum classifier.

### Kenapa ini BUKAN error / bukan inkonsistensi

Paragraf line 418 ada di **§2.7 (landasan teori "Pendekatan Hybrid")** sebagai **definisi UMUM** late fusion — ditandai kata "**misalnya** XceptionNet" dan sitasi ke karya **lain** [11, 13], bukan klaim langkah-demi-langkah model kami. Proyeksi & SE gating bukan ciri pendefinisi late fusion secara umum, melainkan **enhancement** kami, dan keduanya didokumentasikan pada altitude yang tepat:

- **§2.8 "Squeeze-and-Excitation Networks"** (docx line 633-651): konsep SE, channel attention, squeeze/excitation/scale, plus peran SE sebagai "**mekanisme fusi adaptif**" saat fitur spasial+frekuensi dikonkatenasi.
- **§2.x Persamaan proyeksi** (docx line 652-653): proyeksi ke dimensi seragam (Linear+BN+ReLU) "**sebelum diproses mekanisme channel attention seperti SE gating**".
- **BAB III §HybridTwoBranch** (docx line 1344-1353): instansiasi spesifik — proyeksi 256 → konkatenasi 512 → "**diterapkan SE gating [38]**" → classifier.
- **Judul/Abstrak**: arsitektur disebut eksplisit "late fusion **dan Squeeze-and-Excitation gating**".

Jadi strukturnya benar: §2.7 konsep umum → §2.8 SE sebagai penyempurnaan → BAB III menggabungkannya. Tidak ada yang disembunyikan; hanya **beda altitude** (konsep umum vs instansiasi spesifik).

### Catatan kecil: "tanpa saling mengganggu"

Klaim "setiap branch mengekstraksi fitur secara spesifik **tanpa saling mengganggu**" benar **pada tahap ekstraksi** (kedua cabang forward-pass independen). Tapi pada tahap **fusi**, SE gating justru membuat kedua cabang **berinteraksi** (bobot gerbang dihitung dari vektor gabungan 512-d, jadi fitur frekuensi ikut memengaruhi penskalaan fitur spasial dan sebaliknya). Karena kalimat itu menyangkut **ekstraksi**, ia tetap akurat — tapi jangan sampai diparafrase jadi "kedua domain tidak pernah berinteraksi", karena SE gating dirancang justru untuk fusi adaptif lintas-domain.

### Jawaban siap-ucap kalau penguji menyorot

> "Paragraf di BAB II itu adalah **definisi umum** late fusion sebagai landasan teori, makanya pakai 'misalnya XceptionNet' dan mengutip karya lain. Arsitektur spesifik kami menambahkan dua langkah di jalur fusi: **proyeksi kedua cabang ke 256 dimensi** untuk menyetarakan magnitudo, lalu **SE gating** sebagai atensi kanal adaptif sebelum classifier. Keduanya kami bahas di sub-bab tersendiri (Squeeze-and-Excitation Networks) dan dirinci pada BAB III sub-bab HybridTwoBranch, serta disebut eksplisit di judul dan abstrak. Jadi alur penuhnya: proyeksi → konkatenasi → SE gating → classifier; deskripsi BAB II hanya pada tingkat konsep umum."

### Opsional — tutup celah (kalau mau)

Bila ingin paragraf §2.7 tidak terbaca sebagai spesifikasi penuh model, tambahkan satu klausa penutup pengarah ke §2.8:

> "Pada penelitian ini, sebelum diteruskan ke lapisan klasifikasi, vektor hasil konkatenasi terlebih dahulu disetarakan dimensinya melalui proyeksi dan dibobot secara adaptif menggunakan _Squeeze-and-Excitation gating_ (dibahas pada sub-bab 2.8)."

Tidak wajib — struktur §2.7→§2.8 sudah logis. (Edit dari Drive bila diperlukan.)

---

<a name="item-7"></a>

## Item 7 — "Dalam penelitian ini, kedua strategi fusion diimplementasikan dan **dievaluasi** ... **Perbandingan kedua strategi** ini bertujuan mengidentifikasi pendekatan paling efektif"

**Verdict: 🔴 KELIRU / OVERCLAIM — HARUS DIPERBAIKI sebelum sidang. _Early fusion_ memang ADA di kode (`diimplementasikan` benar), tetapi TIDAK pernah masuk eksperimen, TIDAK ada di tabel hasil, TIDAK di BAB IV, dan TIDAK di abstrak. Yang dievaluasi dan diperbandingkan hanya 3 model: spatial, freq, hybrid (late fusion). Intuisimu benar.**

### Ini temuan paling rawan sejauh ini — penguji bisa mematahkannya dengan satu pertanyaan: _"Tunjukkan hasil early fusion-nya / mana perbandingan early vs late?"_

### Bukti

**1. Matriks eksperimen tidak menyertakan early fusion** (`scripts/run_all.py`):

```python
MODELS_CORE = ["spatial", "freq", "hybrid"]          # L23
...
models_to_run = MODELS_CORE.copy()                    # L139
if cfg.get("fusion_mode", "two_branch") == "early_fusion":   # L140
    models_to_run.append("early_fusion")              # L141  ← hanya jika fusion_mode == early_fusion
```

Config kanonik `config.yaml` → `fusion_mode: two_branch`. Jadi cabang `if` **tidak pernah aktif** → early fusion **tidak pernah dilatih/dievaluasi** pada konfigurasi penelitian.

**2. Tidak ada di tabel hasil.** Kolom `model` di semua `Table1_in_dataset.csv` / `Table2_cross_dataset.csv` hanya berisi: **`['freq', 'hybrid', 'spatial']`**. Tidak ada `early_fusion`.

**3. Tidak ada di BAB IV / hasil.** Pencarian "early fusion" di docx hanya muncul di: §2.7 konsep (line 415-416), **klaim bermasalah ini** (line 420), dan satu kalimat BAB III soal _freezing_ (line 1458). Nol baris hasil.

**4. Abstrak membantah klaim ini sendiri:** "**Tiga model** (spasial, frekuensi, dan hybrid) dievaluasi ...". Tiga, bukan empat. Tidak ada early fusion.

### Status sebenarnya per kata

- "**diimplementasikan**" → ✅ BENAR. `EarlyFusionXception` ada (`hybrid_fusion.py:70-78`), `train.py` mendukung `--model early_fusion` (L129, L67-68), dataset mendukung mode 4-kanal (`deepfake_data.py:149`). Bisa dijalankan.
- "**dievaluasi**" → 🔴 SALAH. Tidak ada dalam eksperimen/hasil yang dilaporkan.
- "**Perbandingan kedua strategi ... pendekatan paling efektif**" → 🔴 SALAH. Tidak ada perbandingan early-vs-late di mana pun.

### Inkonsistensi terkait yang ikut harus dirapikan

**BAB III line 1458** menyebut "...model spatial, hybrid, **dan early fusion**, backbone dibekukan..." — ini juga **menyiratkan early fusion adalah model yang dilatih**. Karena tidak dievaluasi, frasa "dan early fusion" sebaiknya dibuang dari kalimat metodologi itu (atau kalimatnya diubah ke "kode mendukung, namun tidak digunakan").

### Rekomendasi perbaikan (WAJIB) — opsi termurah & jujur

Pertahankan **deskripsi konsep** early fusion di §2.7 (line 415-416) sebagai landasan teori (boleh — itu teori). Tapi **ganti klaim evaluatif** di line 420. Contoh teks pengganti:

> "Penelitian ini berfokus pada strategi **late fusion**, yang diimplementasikan melalui arsitektur _two-branch_ yang menggabungkan XceptionNet untuk fitur spasial dan CNN ringan untuk fitur frekuensi, dilengkapi _Squeeze-and-Excitation gating_. Strategi _early fusion_ (XceptionNet 4-kanal RGB+FFT) disajikan sebagai **alternatif konseptual** dan didukung oleh implementasi kode, namun **tidak menjadi fokus evaluasi eksperimental** pada penelitian ini; pemilihan late fusion didasari fleksibilitas pemodelan arsitektur yang berbeda untuk tiap domain."

Lalu di line 1458 ganti "...model spatial, hybrid, dan early fusion..." → "...model spatial dan hybrid...".

### Kalau penguji terlanjur bertanya "katanya dievaluasi keduanya?"

> "Mohon koreksi pada kalimat tersebut, Pak/Bu — yang dievaluasi secara eksperimental dalam penelitian ini adalah **late fusion** (model hybrid _two-branch_ + SE gating), sebagaimana konsisten dengan judul, abstrak (tiga model), dan seluruh BAB IV. _Early fusion_ kami implementasikan sebagai opsi arsitektur dan kami bahas secara konseptual, tetapi tidak kami masukkan ke matriks evaluasi. Kalimat di BAB II akan kami perbaiki agar tidak menyiratkan adanya perbandingan empiris early-vs-late."

> ⚠️ **Prioritas tinggi:** ini bukan soal interpretasi seperti Item 5/6 — ini klaim faktual yang tidak didukung data. Perbaiki teks BAB II (line 420) dan BAB III (line 1458) di .docx sebelum sidang.

---

<a name="item-8"></a>

## Item 8 — Referensi: "power spectrum" (Durall et al. 2020, "Watch your Up-Convolution", CVPR) dan hubungannya ke kita

**Bukan verdict — ini referensi konsep** untuk memperkuat Item 3/4/5 dan menjelaskan **kenapa cabang frekuensi kita lemah**. Paper: `thesis_reference/Durall et al - Watch your Up-Convolution...pdf`.

### Definisi bertingkat (jangan tertukar)

| Istilah                        | Rumus                         | Arti                                                                                                                                                                          |
| ------------------------------ | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Magnitude spectrum             | `\|F(u,v)\|`                  | amplitudo tiap frekuensi 2D                                                                                                                                                   |
| **Power spectrum**             | `\|F(u,v)\|²`                 | **energi/daya** tiap frekuensi 2D (Durall Eq. 1, Fig 2 kiri)                                                                                                                  |
| **1D Power Spectrum**          | azimuthal integration (Eq. 2) | peta 2D diringkas jadi**satu kurva** dengan mengintegrasikan daya di lingkaran 360° untuk tiap radius `ω_k` → kurva _Power Spectrum vs Spatial Frequency_ (Fig 1, 2-kanan, 5) |
| Log-magnitude (**punya kita**) | `log(1+\|F(u,v)\|)`           | yang dipakai`fft_utils.py`; fungsi dari `\|F\|` yang sama, beda skala (log mengompres rentang dinamis)                                                                        |

### Temuan inti Durall

Up-sampling generator GAN (transposed-conv "bed of nails" → replika frekuensi tinggi; interpolasi → defisit frekuensi tinggi) **gagal mereproduksi distribusi spektral citra asli**. Kurva power spectrum citra GAN menyimpang dari real **terutama di ekor frekuensi tinggi**. Penyimpangan sistematis ini → deteksi deepfake **~100% akurasi** dengan classifier sederhana atas fitur 1D power spectrum.

### Hubungan ke penelitian ini (5 poin)

1. **Fondasi teoretis** keberadaan cabang frekuensi — sitasi untuk "distorsi distribusi spektral".
2. **Power spectrum (`\|F\|²`) vs log-magnitude kita (`log(1+\|F\|)`)** — sinyal sama, skala beda. Kita **tidak** pakai azimuthal integration.
3. **Pendekatan beda:** Durall = ringkasan **1D** (buang info arah) + classifier sederhana; kita = peta **2D penuh** + FreqCNN. Kita lebih kaya tapi lebih berisik/berdimensi tinggi.
4. **Justifikasi high-pass kita** (lihat [Item 4](#item-4)): Durall menunjukkan diskriminasi ada di **frekuensi tinggi**, low-freq (DC) hampir sama → maka kita tekan low-freq, tonjolkan high-freq.
5. **KUNCI — menjelaskan freq branch kita lemah (AUC 0,56-0,61) vs Durall ~100%:** Durall pakai **output GAN mentah tanpa kompresi**; kita pakai frame **face-crop + terkompresi c23**. Kompresi + resize = **low-pass filter yang menghancurkan sidik jari frekuensi tinggi** andalan Durall. Sudah diakui di BAB V ("hilangnya sidik jari spektral akibat face-cropping dan kompresi"). Jadi Durall = sekaligus **pembenar** mencoba frekuensi **dan kontras** yang menjelaskan hasil lemah kita.

### Kalau penguji tanya "kenudian kenapa hasilmu tidak ~100% seperti paper frekuensi?"

> "Karena kondisinya berbeda. Durall et al. menguji **output GAN mentah tanpa kompresi**, di mana sidik jari spektral up-sampling masih utuh. Penelitian kami memakai frame **wajah yang di-crop dan terkompresi (c23)** dari benchmark FaceForensics++/Celeb-DF; kompresi dan resize bertindak sebagai low-pass yang **menghapus jejak frekuensi tinggi** yang menjadi andalan deteksi spektral. Itulah mengapa cabang frekuensi kami berperforma rendah, dan ini konsisten dengan keterbatasan yang kami nyatakan di BAB V serta menjadi motivasi penelitian lanjutan (FFT pada citra penuh / multi-skala / menyertakan fasa)."

---

<a name="item-9"></a>

## Item 9 — "Local" vs "global" (SpecXNet, Alam et al. 2025) dan: _"Jadi kalian ini global atau lokal untuk spasial dan frekuensinya?"_

**Verdict: ✅ Bisa dijawab tegas. Jawaban singkat: spasial = LOKAL, frekuensi = GLOBAL. Tapi WAJIB perjelas dua hal: (a) kita TIDAK memecah local/global eksplisit seperti SpecXNet — kita pisah per-DOMAIN dengan late fusion sederhana; (b) ada dua makna "local/global" yang bisa dijebak penguji (sumbu domain vs sumbu pita-spektrum).**

### Apa arti "local" & "global" di SpecXNet (paper, §3.1 DDFC)

SpecXNet (Alam et al.) memecah feature map tiap blok jadi dua jalur via _Dual-Domain Feature Coupler (DDFC)_:

- **Local Spatial Branch** (`X_l`): **konvolusi standar** → menangkap **detail LOKAL** (tekstur halus, tepi, batas blending). "Local" karena konvolusi punya **receptive field terbatas**.
- **Global Spectral Branch** (`X_g`): **2D FFT** → domain frekuensi → menangkap **struktur GLOBAL / korelasi jarak-jauh & pola periodik**. "Global" karena **setiap koefisien Fourier bergantung pada SELURUH piksel citra**.
- Lalu difusikan dengan _Dual Fourier Attention (DFA)_ — atensi lintas-domain yang berulang di tiap blok.

Jadi di SpecXNet: **spasial ≡ lokal (konvolusi), frekuensi ≡ global (FFT)** — ini dualitas mendasar (konvolusi = lokal; transformasi Fourier = global).

### Pemetaan ke arsitektur kita (HybridTwoBranch)

|           | Cabang kita                                 | Sifat (istilah SpecXNet)                                                                          | Nuansa                                                                                                                     |
| --------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Spasial   | XceptionNet atas RGB                        | **LOKAL** — konvolusi menangkap tekstur/tepi/blending                                             | backbone dalam → effective receptive field membesar → fitur GAP akhir = deskriptor holistik wajah                          |
| Frekuensi | FFT seluruh citra → log-magnitude → FreqCNN | **GLOBAL** — FFT whole-image, menyandikan struktur periodik global, **kehilangan lokasi spasial** | tapi peta FFT itu lalu diproses**konvolusi lokal** oleh FreqCNN, dan ditekankan ke pita **frekuensi tinggi** via high-pass |

### Perbedaan penting dari SpecXNet (jangan diklaim setara)

- **SpecXNet:** pecah local/global **DI DALAM tiap blok** (channel split) + fusi **Dual Fourier Attention berulang** + inverse-FFT kembali ke spasial. Arsitektur terpadu, multi-skala.
- **Kita:** pisah per-**DOMAIN** (satu cabang spasial penuh, satu cabang frekuensi penuh), fusi **SEKALI** di level fitur via concat + **SE gating**. **Tidak ada** DDFC per-blok maupun Fourier cross-attention.
  → SpecXNet [13] kita kutip sebagai **inspirasi/related work**, bukan reimplementasi. (Senada dengan scoping di [Item 5](#item-5)/[Item 7](#item-7).)

### ⚠️ Jebakan dua-sumbu (penguji bisa pakai BAB II kalian sendiri)

Ada **dua** makna "local/global" di skripsi — jangan tertukar:

1. **Sumbu DOMAIN** (cara SpecXNet): spasial=lokal, frekuensi=global. ← ini yang dipakai untuk menjawab pertanyaan penguji.
2. **Sumbu PITA dalam spektrum** (BAB II kalian, docx line 446/454): frekuensi **rendah** = "bentuk global & pencahayaan", frekuensi **tinggi** = "tepi, tekstur, detail halus" (lokal).

Penguji bisa menjebak: _"High-pass kalian menonjolkan frekuensi tinggi, yang menurut BAB II kalian sendiri = detail LOKAL. Jadi cabang frekuensi kalian itu lokal atau global?"_

**Jawaban yang benar (tidak kontradiktif):**

> "Dua-duanya benar pada sumbu yang berbeda. **Transformasi**-nya global: FFT dihitung atas seluruh citra dan tidak menyimpan lokasi spasial artefak. **Konten** yang ditekankan adalah pita frekuensi tinggi, yang berkorelasi dengan detail halus. Jadi cabang frekuensi kami adalah **representasi global atas statistik detail berfrekuensi-tinggi** — ia mencirikan sidik jari frekuensi tinggi di seantero wajah, bukan menunjukkan DI MANA artefaknya. Tidak ada kontradiksi: 'global' merujuk pada cakupan transformasi, 'frekuensi tinggi/detail' merujuk pada pita yang ditonjolkan."

### Jawaban siap-ucap untuk "kalian global atau lokal?"

> "Cabang **spasial** kami bersifat **lokal** — XceptionNet menangkap detail lokal seperti tekstur kulit, tepi, dan batas blending lewat konvolusi; karena backbone-nya dalam, fitur akhirnya menjadi deskriptor holistik wajah. Cabang **frekuensi** kami bersifat **global** — FFT adalah transformasi seluruh citra yang menangkap struktur dan pola periodik global, meski kehilangan informasi lokasi spasial. Keduanya komplementer: yang satu tahu _bentuk artefak lokal_, yang lain tahu _tanda statistik global_. Berbeda dari SpecXNet yang memadukan local-global di tiap blok dengan atensi Fourier, arsitektur kami melakukan late fusion sederhana dua cabang domain via SE gating."

### Konsistensi dengan teks skripsi (sudah selaras)

- docx line 410: "spasial unggul menangkap anomali visual **lokal** (tekstur/tepi) ... frekuensi ... **kehilangan informasi lokasi spasial**" → mendukung pemetaan spasial=lokal, frekuensi=global. ✅
- docx line 446/454: low-freq=global, high-freq=detail → sumbu pita (jebakan #2). ✅ konsisten asalkan dijelaskan sebagai sumbu berbeda.
- Tidak perlu revisi; cukup siap membedakan dua sumbu saat ditanya.

---

<a name="item-10"></a>

## Item 10 — "Banyak penelitian menunjukkan XceptionNet unggul pada dataset FF++, DFDC, dan Celeb-DF [13, 7]" (docx line 595)

**Verdict: 🔴 OVERCLAIM + sitasi tidak mendukung. Hanya FF++ yang benar & terdukung. DFDC dan Celeb-DF TIDAK diuji oleh kedua referensi, dan klaim "unggul" pada keduanya justru BERTENTANGAN dengan literatur dan hasil kalian sendiri.**

### Referensi (per klarifikasi penulis)

- **[7] = Rössler et al., FaceForensics++ (ICCV 2019).**
- **[13] = Alam et al., SpecXNet (ACM MM 2025).**

> ⚠️ Catatan numbering: di Daftar Pustaka fisik, Rössler = entri **8** dan Alam/SpecXNet = entri **14**, tetapi dikutip in-text sebagai [7] dan [13]. In-text number **desync** dengan urutan Daftar Pustaka (isu yang sudah tercatat). Verifikasi penomoran sebelum sidang.

### Apa yang benar-benar dicakup tiap referensi

**Rössler [7] — FaceForensics++:**

- Menguji XceptionNet pada **FF++ saja** (Deepfakes, Face2Face, FaceSwap, NeuralTextures). Xception memang detektor **terbaik pada FF++** di paper itu. ✅ untuk FF++.
- **TIDAK memuat DFDC** (DFDC rilis akhir 2019/2020, setelah/di luar paper) dan **TIDAK memuat Celeb-DF** (dataset terpisah, Li et al. 2020). 🔴

**SpecXNet [13] — dari Tabel 1-5 paper (sudah dibaca):**

- Benchmark deepfake wajahnya **hanya FF++** (Tabel 3: "we adopt the FaceForensics++ (FF++) dataset, ... Deepfakes and FaceSwap"). Selebihnya GenImage + generator GAN/diffusion (ProGAN, StyleGAN, BigGAN, GLIDE, SD, DALL-E, Midjourney, dll.).
- **TIDAK ada Celeb-DF di tabel mana pun. TIDAK ada DFDC di tabel mana pun.** 🔴
- Lagipula SpecXNet melaporkan XceptionNet sebagai **backbone/baseline yang justru DIKALAHKAN** modul mereka (vanilla Xception ~81,3% rata-rata → +DDFC+DFA 96,4%, Tabel 4) — jadi paper ini **bukan** bukti "XceptionNet unggul", melainkan "SpecXNet > XceptionNet".

### Kesimpulan cakupan

| Dataset      | Didukung [7] Rössler?    | Didukung [13] SpecXNet? | Klaim "unggul" valid? |
| ------------ | ------------------------ | ----------------------- | --------------------- |
| **FF++**     | ✅ ya (Xception terbaik) | ✅ ya (diuji)           | ✅                    |
| **DFDC**     | 🔴 tidak diuji           | 🔴 tidak diuji          | 🔴 tidak terdukung    |
| **Celeb-DF** | 🔴 tidak diuji           | 🔴 tidak diuji          | 🔴 tidak terdukung    |

### Masalah SUBSTANSI (lebih dalam dari sekadar sitasi)

Klaim "XceptionNet **unggul** pada Celeb-DF dan DFDC" **bertentangan** dengan:

1. **Literatur:** XceptionNet terkenal **generalisasi buruk** ke Celeb-DF/DFDC. Paper Celeb-DF (Li et al. 2020) menunjukkan detektor termasuk Xception **anjlok mendekati tebakan acak** pada Celeb-DF.
2. **Hasil kalian sendiri:** model spasial (XceptionNet) **runtuh cross-dataset** (AUC turun, recall collapse) — justru itu MOTIVASI penelitian kalian. Mengklaim Xception "unggul" pada CDF malah **menggerus narasi** kalian sendiri.
3. **DFDC bahkan tidak dipakai** di penelitian ini (kalian pakai FF++ & Celeb-DF). Menyebutnya sebagai keunggulan itu janggal dan tak terpakai.

### Rekomendasi perbaikan (WAJIB)

Batasi klaim ke FF++ dan buang DFDC/Celeb-DF dari klaim "unggul". Contoh:

> "XceptionNet dilaporkan sebagai detektor domain spasial terbaik pada FaceForensics++ [7] dan menjadi backbone populer pada berbagai metode deteksi lanjutan termasuk pendekatan hybrid [13]. Namun, performa tinggi ini umumnya bersifat in-dataset; generalisasi ke dataset lain seperti Celeb-DF dan DFDC diketahui menurun, yang menjadi salah satu motivasi penelitian ini."

Reframe ini justru **menguatkan** motivasi kalian (masalah generalisasi), bukan melemahkannya.

### Kalau penguji bertanya

> "Kalimat itu perlu kami koreksi, Pak/Bu. Yang terdukung referensi adalah keunggulan XceptionNet pada **FaceForensics++**. Untuk Celeb-DF dan DFDC, justru sebaliknya: XceptionNet cenderung menurun secara lintas-dataset, sebagaimana juga kami temukan pada hasil model spasial kami. Referensi [7] (FaceForensics++) dan [13] (SpecXNet) tidak menguji Celeb-DF maupun DFDC, sehingga klaim tersebut akan kami persempit ke FF++."

---

<a name="item-11"></a>

## Item 11 — "Dalam penelitian ini, fitur FFT ditambahkan sebagai **kanal keempat** input XceptionNet; DSC cocok untuk multi-kanal ... sebagaimana SpecXNet [13] dan FSBI [16]" (docx §2.7.3, line ~597-602 & 630)

**Verdict: 🔴 TIDAK sejalan dengan flow kalian. Ini mendeskripsikan EARLY FUSION (input 4-kanal ke XceptionNet), padahal model yang dievaluasi adalah LATE FUSION (dua cabang terpisah). Ini instans lain dari overclaim early fusion — kembar dengan [Item 7](#item-7).**

### Jawaban langsung atas "is this lined up with our flow?": **TIDAK.**

- **Flow aktual (evaluated, `hybrid_fusion.py` HybridTwoBranch):** XceptionNet memproses RGB **3-kanal** SECARA TERPISAH; peta FFT diproses **cabang FreqCNN terpisah**; fiturnya baru digabung di **late fusion** (proyeksi → concat → SE gate → classifier). **FFT TIDAK pernah menjadi kanal ke-4 XceptionNet.**
- **Yang dideskripsikan kalimat itu:** RGB+FFT ditumpuk jadi **tensor 4-kanal** lalu masuk **satu** XceptionNet = **EarlyFusionXception** (`hybrid_fusion.py:70`). Ada di kode, **tetapi tidak dievaluasi** (lihat Item 7: `run_all.py` MODELS_CORE=[spatial,freq,hybrid], config `two_branch`).

Frasa "**Dalam penelitian ini**, fitur FFT ditambahkan sebagai kanal keempat" = **klaim faktual yang salah** untuk pipeline yang benar-benar dijalankan.

### Masalah tambahan pada paragraf ini

1. **Rasional DSC longgar untuk kasus 4-kanal.** Entry flow XceptionNet diawali **dua konvolusi BIASA** (bukan depthwise) — kalian sendiri menulisnya di §2.7.1. Jadi input 4-kanal langsung **dicampur oleh conv standar** di lapisan pertama; narasi "tiap kanal ditangani independen via depthwise" tidak berlaku untuk pencampuran awal kanal RGB vs FFT. (Deskripsi depthwise/pointwise-nya sendiri benar sebagai konsep, hanya salah tempat.)
2. **Perbandingan SpecXNet/FSBI keliru.** "sebagaimana juga dilakukan pada SpecXNet [13] dan FSBI [16]" — **keduanya TIDAK menambah FFT sebagai kanal ke-4**:
   - **SpecXNet** = DDFC (channel split → cabang spasial-lokal + cabang spektral-global via FFT di dalam blok) + Dual Fourier Attention. Bukan input 4-kanal.
   - **FSBI** = _Frequency-enhanced Self-Blended Images_ (sintesis citra latih yang ditingkatkan frekuensi). Bukan input 4-kanal.
     → "sebagaimana juga dilakukan" menyesatkan; metode mereka berbeda dari append 4-kanal.
3. **Numbering desync (lagi):** in-text FSBI [16] secara fisik = entri Daftar Pustaka **17** (Hasanaath). SpecXNet [13] = entri **14**. Cek penomoran (lihat catatan [Item 10](#item-10)).

### Rekomendasi perbaikan (WAJIB, sejalan Item 7)

Dua sub-poin di §2.7.3 — "**Integrasi dengan FFT sebagai Channel Tambahan**" dan "**Kompatibilitas dengan Analisis Frekuensi**" — mendeskripsikan early fusion. Karena model yang dievaluasi adalah late fusion, pilih salah satu:

- **(A, disarankan) Tulis ulang ke late fusion:** "XceptionNet dipilih sebagai backbone **cabang spasial** yang memproses citra RGB; efisiensi depthwise separable convolution membuatnya kuat menangkap tekstur lokal. Representasi FFT diproses **cabang frekuensi terpisah (FreqCNN)** dan digabung pada tahap **late fusion**, bukan sebagai kanal tambahan pada XceptionNet."
- **(B) Bingkai sebagai varian tak-dievaluasi:** nyatakan bahwa integrasi 4-kanal (early fusion) diimplementasikan sebagai alternatif namun **tidak menjadi model evaluasi** (konsisten dengan revisi Item 7).

Dan perbaiki klaim SpecXNet/FSBI: mereka memadukan domain lewat **modul/atensi atau sintesis input**, **bukan** penambahan kanal ke-4.

### Kalau penguji bertanya "jadi FFT itu kanal ke-4 atau cabang terpisah?"

> "Pada model yang kami evaluasi (hybrid two-branch), FFT diproses **cabang terpisah (FreqCNN)** dan digabung via late fusion + SE gating — **bukan** kanal ke-4. Varian early fusion 4-kanal memang kami implementasikan, tetapi tidak masuk evaluasi. Kalimat di BAB II yang menyebут 'kanal keempat' akan kami luruskan agar sesuai dengan arsitektur late fusion yang benar-benar digunakan."

### 📋 Perbaikan menyeluruh di Word (cakupan lengkap — hasil audit live .docx)

Framing early-fusion ("FFT jadi kanal ke-4 / channel fusion") bocor ke **7 tempat**. Model yang dievaluasi = **late fusion** (XceptionNet makan RGB 3-kanal + FreqCNN makan FFT 1-kanal, digabung di **level fitur**: proyeksi → concat → SE gating). Semua di bawah ini diedit dari Drive.

**✅ Yang sudah beres (jangan diutak-atik):**

- Konsep umum early fusion di §2.7 landasan teori (paragraf "Early Fusion (Fusi Awal)") — **biarkan**, itu teori.
- Paragraf "Penelitian ini berfokus pada strategi late fusion..." — **sudah benar** (fix Item 7). ⚠️ hanya buang **typo "ohwe"** di ujung kalimatnya.
- Tabel matriks yang menulis "RGB + FFT **(terpisah)**" — **sudah benar** (terpisah = late fusion).

**🔴 Yang masih harus diperbaiki:**

| #   | Lokasi (docx)                                                              | Teks sekarang (masalah)                                                                                                                                          | Ganti jadi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | §2.7 list "Kompatibel dengan analisis frekuensi"                           | "**Kombinasi kanal RGB dan kanal frekuensi (hasil FFT)** ... XceptionNet cocok untuk skenario hybrid ini."                                                       | "Dalam arsitektur hybrid, XceptionNet berperan sebagai**cabang spasial** yang memproses citra RGB, sedangkan representasi FFT ditangani **cabang terpisah**. Efisiensi XceptionNet membuatnya cocok sebagai backbone cabang spasial."                                                                                                                                                                                                                                                                                                                                                                   |
| 2   | §2.7.3 sub-judul + isi "**Integrasi dengan FFT sebagai Channel Tambahan**" | "Dalam penelitian ini, fitur FFT**ditambahkan sebagai kanal keempat pada input XceptionNet** ... sebagaimana SpecXNet [13] dan FSBI [16]."                       | Ganti judul → "**Peran XceptionNet sebagai Cabang Spasial dalam Arsitektur Hybrid**". Isi → "Dalam penelitian ini, XceptionNet memproses citra RGB sebagai cabang spasial, sedangkan FFT diproses **cabang frekuensi terpisah (FreqCNN)**. Fitur kedua cabang digabung pada tahap **late fusion** (proyeksi, konkatenasi, SE gating), **bukan** sebagai kanal tambahan. SpecXNet [13] dan FSBI [16] juga memadukan spasial-frekuensi, **melalui mekanisme berbeda** (SpecXNet: pemisahan kanal spasial-spektral + atensi Fourier di dalam blok; FSBI: citra self-blended yang ditingkatkan frekuensi)." |
| 3   | §2.7.3 sub-judul "**Kompatibilitas dengan Analisis Frekuensi**"            | "Struktur DSC ... memproses**input multi-kanal yang mencakup kanal RGB dan kanal frekuensi (FFT)** ... [13]."                                                    | **Hapus** sub-poin ini (sudah ditutup #2), **atau** ganti → "Efisiensi depthwise separable convolution membuat XceptionNet cukup ringan untuk dijadikan **salah satu cabang** arsitektur hybrid dua-cabang, sehingga penambahan cabang frekuensi terpisah tetap layak secara komputasi."                                                                                                                                                                                                                                                                                                                |
| 4   | §2.9 Peran FaceForensics++                                                 | "Kedua fitur ini kemudian digabungkan sebagai**channel fusion** ..."                                                                                             | "Fitur spasial dan frekuensi ini kemudian digabungkan pada tahap**late fusion di tingkat fitur** ..."                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 5   | **Tabel 2.4 Tahapan Preprocessing** — baris 7 + caption                    | Baris 7: "**Channel fusion** \| Menggabungkan RGB dan kanal frekuensi \| **Tensor 4-channel**". Caption: "tahapan 6-7 ... **fitur tambahan** pada model hybrid". | **Hapus baris 7** (fusi bukan langkah preprocessing, dan bukan 4-kanal). Caption → "Tahapan 1–5 menghasilkan citra RGB (preprocessing spasial); tahapan 6 menghasilkan peta FFT log-magnitude **1 kanal**. Kedua representasi **disimpan terpisah** dan digabungkan **di dalam model** pada tahap late fusion, bukan pada preprocessing."                                                                                                                                                                                                                                                               |
| 6   | **BAB III §Preprocessing FFT** (metodologi!)                               | "Representasi frekuensi kemudian digabungkan sebagai**frequency channel tambahan bersama citra RGB**."                                                           | "Representasi frekuensi**1-kanal** ini disimpan sebagai cache dan menjadi masukan **cabang frekuensi (FreqCNN)**, terpisah dari citra RGB yang menjadi masukan **cabang spasial (XceptionNet)**. Fitur kedua cabang digabung pada tahap **late fusion**."                                                                                                                                                                                                                                                                                                                                               |
| 7   | **BAB III §Pelatihan** (freezing)                                          | "...model spatial, hybrid,**dan early fusion**, backbone dibekukan ... pada model **early fusion**, seluruh parameter backbone dibekukan."                       | Buang klausa early fusion → "...model spatial**dan** hybrid, backbone dibekukan ... pada model hybrid: FreqCNN, proyeksi, SE gate, dan classifier."                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 8   | **BAB III §Preprocessing FFT** (line 793, dekat sitasi Sabir/Wang)         | "...penelitian ini menambahkan informasi Frekuensi ke dalam informasi citra sebagai**channel 4** yang akan membawa informasi mengenai penyebaran frekuensi."     | "...penelitian ini memproses informasi frekuensi pada**cabang terpisah (FreqCNN)** dan menggabungkannya dengan fitur spasial pada tahap **late fusion**, bukan sebagai kanal ke-4."                                                                                                                                                                                                                                                                                                                                                                                                                     |

**Opsional (rendah):** §2.10-related-work "SpecXNet, FSBI ... memasukkan **kanal-kanal frekuensi tambahan** atau modul khusus" — masih agak menyiratkan channel-append; boleh dipertegas jadi "melalui **modul khusus atau sintesis input** yang menonjolkan komponen frekuensi" agar tidak rancu dengan #2.

**Prinsip global untuk konsistensi:** di mana pun kata **"channel fusion" / "kanal keempat" / "4-channel" / "kanal frekuensi tambahan"** muncul sebagai deskripsi metode penelitian → ganti ke **"late fusion di tingkat fitur"** dengan dua cabang terpisah. Sisakan istilah 4-kanal HANYA di (a) paragraf konsep early fusion, dan (b) catatan "alternatif tak-dievaluasi".

---

<a name="item-12"></a>

## Item 12 — "korelasi spasial **(cross-channel)** dan korelasi antarkanal **(cross-spatial)**" (docx line 604)

**Verdict: 🔴 KELIRU — label Inggris di dalam kurung TERTUKAR, dan "cross-spatial" bukan istilah baku. Instingmu benar. Perbaikannya satu kalimat.**

### Yang benar (hipotesis Chollet, Xception 2017)

Chollet: _"cross-channel correlations and spatial correlations are sufficiently decoupled..."_. Depthwise separable convolution memisahkan dua jenis korelasi:

| Istilah Indonesia      | Label Inggris yang BENAR       | Ditangani oleh                                |
| ---------------------- | ------------------------------ | --------------------------------------------- |
| korelasi**spasial**    | **spatial correlations**       | **depthwise** conv (per-kanal, di bidang H×W) |
| korelasi**antarkanal** | **cross-channel correlations** | **pointwise** 1×1 conv (campur antar-kanal)   |

### Apa yang salah di kalimatmu (line 604)

- "korelasi spasial **(cross-channel)**" → salah. _cross-channel_ = label untuk **antarkanal**, bukan spasial.
- "korelasi antarkanal **(cross-spatial)**" → salah ganda: (a) mestinya **cross-channel**, (b) **"cross-spatial" tidak ada** dalam terminologi Chollet.

Jadi kedua label Inggris **saling tertukar**, plus satu istilah dikarang.

### Bukti bahwa ini memang typo (skripsimu contradict dirinya sendiri)

- **docx line 572** (BENAR): "_pointwise convolution_ ... menangkap **korelasi antarkanal**" → pointwise = cross-channel = antarkanal. ✅
- **docx line 562** (BENAR): "korelasi spasial dan korelasi kanal dapat dipisahkan" (tanpa label Inggris, urutan benar). ✅
- **docx line 604** (SALAH): satu-satunya tempat yang menempel label Inggris, dan tertukar. → jelas kesalahan penulisan lokal, bukan kesalahan pemahaman menyeluruh.

### Perbaikan (WAJIB, mudah)

> "Arsitektur ini dibangun berdasarkan hipotesis bahwa **korelasi spasial (spatial correlations)** dan **korelasi antarkanal (cross-channel correlations)** dapat dipisahkan (_decoupled_) secara penuh melalui _depthwise separable convolution_, sehingga operasi konvolusi menjadi lebih efisien tanpa mengorbankan kapasitas representasi fitur [6]."

(Atau cukup hapus kedua label Inggris — line 562 sudah membuktikan kalimat tanpa label pun jelas dan benar.)

### Kalau penguji menyorot

> "Betul, itu salah ketik pada label bahasa Inggris — tertukar. Yang benar: korelasi spasial = _spatial correlations_ (ditangani depthwise), korelasi antarkanal = _cross-channel correlations_ (ditangani pointwise 1×1). Ini juga sudah kami nyatakan dengan benar di bagian penjelasan pointwise convolution."

---

<a name="item-13"></a>

## Item 13 — Repetisi: pembuka seksi "DSC" dan pembuka §2.7 "XceptionNet" mengulang hal yang sama

**Verdict: 🟡 REPETITIF (editorial, bukan kesalahan fakta). Dua pembuka seksi menyampaikan proposisi identik. Instingmu benar. + ada redundansi kedua: dua daftar keunggulan tumpang-tindih.**

### Dua paragraf yang diulang

Keduanya menyatakan hal sama: (1) XceptionNet = CNN oleh Chollet (2017), pengembangan Inception Module; (2) hipotesis korelasi spasial & antarkanal dapat dipisahkan via DSC; (3) hasilnya konvolusi lebih efisien tanpa mengorbankan representasi.

- **Paragraf B** = pembuka sub-bab **"Depthwise Separable Convolution (DSC)"** (muncul lebih dulu): "Arsitektur XceptionNet merupakan salah satu model CNN modern ... memanfaatkan DSC. Pendekatan ini diperkenalkan oleh Chollet [6] ... korelasi spasial dan korelasi kanal dapat dipisahkan ..."
- **Paragraf A** = pembuka **§2.7 "Extreme Inception Network (XceptionNet)"**: "XceptionNet merupakan arsitektur CNN yang diperkenalkan oleh Chollet pada 2017 ... korelasi spasial dan korelasi antar-kanal (cross-channel) dapat dipisahkan secara penuh melalui DSC ..."

**Akar masalah:** seksi DSC ikut _memperkenalkan XceptionNet_, padahal seharusnya membahas **teknik DSC**; §2.7 yang memperkenalkan **arsitekturnya**.

### Perbaikan

Pertahankan **Paragraf A (§2.7)** sebagai pengantar kanonik XceptionNet. **Tulis ulang Paragraf B** → soal DSC-sebagai-teknik + forward-ref §2.7:

> "Depthwise Separable Convolution (DSC) merupakan teknik konvolusi yang memisahkan operasi spasial dan operasi antarkanal menjadi dua tahap terpisah (_depthwise_ dan _pointwise_). Pemisahan ini menekan jumlah parameter dan biaya komputasi secara signifikan tanpa mengurangi kapasitas representasi fitur, dan menjadi inti efisiensi arsitektur XceptionNet yang dibahas pada sub-bab 2.7."

### Redundansi KEDUA (di seksi yang sama) — dua daftar keunggulan tumpang-tindih

- **"Relevansi DSC pada Deteksi Deepfake"** (seksi DSC): sensitif tekstur lokal · stabil pada variasi kompresi · kompatibel analisis frekuensi · performa tinggi FFPP · representasi spasial kuat.
- **"Keunggulan XceptionNet dalam Deteksi Deepfake"** (§2.7.3): sensitivitas tekstur lokal · efisiensi parameter · performa tertinggi FFPP · stabilitas variasi kompresi · kompatibilitas analisis frekuensi · standar penelitian.

**4 poin identik** muncul di kedua daftar (tekstur lokal, FFPP, kompresi, frekuensi). **Rekomendasi:** gabung jadi **satu daftar** di §2.7.3; seksi DSC cukup fokus ke mekanisme + kompleksitas DSC (tanpa daftar keunggulan). Ini sekaligus menutup poin early-fusion di [Item 11](#item-11) (#1, #2, #3) yang kebetulan berada di kedua daftar tersebut.

---

<a name="item-14"></a>

## Item 14 — "SE block ... yang tidak dapat ditangkap oleh konkatenasi sederhana ... Dibandingkan fusi sederhana seperti konkatenasi atau penjumlahan, SE block ... meningkatkan performa" (§2.8.3, docx line 649-650) — padahal kita PAKAI konkatenasi

**Verdict: ✅ BUKAN masalah, TIDAK kontradiksi. Konkatenasi dan SE gating dipakai BERSAMAAN (bukan alternatif). Konkatenasi menggabungkan dua cabang; SE gating membobotinya secara adaptif SETELAHNYA. Thesis kalian sudah konsisten.**

### Kenapa bukan kontradiksi

Kesalahpahaman: membaca "konkatenasi" sebagai lawan dari "SE block". Padahal di model kita, urutannya:

```
proyeksi(256) → KONKATENASI (512) → SE GATE (bobot adaptif) → classifier
```

(kode `hybrid_fusion.py:64-66`). Jadi:

- **Konkatenasi** = operasi yang MENYATUKAN fitur spasial (256) + frekuensi (256) jadi satu vektor 512-d. **Wajib** — kedua cabang harus digabung dulu.
- **SE gating** = bekerja **di atas** hasil konkatenasi, mempelajari bobot kepentingan per-dimensi lalu menskala ulang (`x * gate(x)`).

"**Konkatenasi sederhana**" (kata "sederhana" penting) = konkatenasi **tanpa** pembobotan adaptif, yaitu vektor gabungan langsung masuk classifier. Model kita **tidak** begitu — kita konkatenasi **lalu** SE gating. Jadi kita ada di sisi "lebih baik" dari perbandingan itu. **Paragraf itu justru membenarkan desain kita**, bukan menyerangnya.

Analogi: "tembok polos itu lemah, jadi kami perkuat dengan baja." Temboknya tetap ada — hanya ditambah penguat. Bukan tembok-vs-baja, tapi tembok+baja. Konkatenasi = tembok, SE = baja.

### Thesis kalian sudah konsisten (tidak perlu revisi)

- §2.8.3 line 645: "...digabungkan melalui **konkatenasi**, vektor fusi..." lalu SE memprosesnya. ✅
- §2.8.3 line 652: "...digabungkan (konkatenasi) ... **sebelum diproses** oleh channel attention seperti SE gating." ✅
- BAB III line 1349-1351: "Setelah **konkatenasi**, diterapkan **SE gating**..." ✅
- Tabel arsitektur menulis fusi hybrid = "**Konkatenasi + SE Gating**". ✅

### Satu nuansa jujur (kalau penguji menekan teknis)

SE gating itu **channel attention** (squeeze-excite): membobot ulang tiap dimensi secara global, di mana bobot dihitung dari **seluruh vektor 512-d** (kedua domain). Jadi pembobotan dimensi spasial **dikondisikan** oleh nilai fitur frekuensi dan sebaliknya — itulah "interaksi lintas domain"-nya. Tapi SE **bukan** modul korelasi berpasangan penuh (bukan cross-attention/bilinear). Jadi frasa "mempelajari korelasi antara fitur spasial dan frekuensi" sebaiknya dipahami sebagai "**pembobotan kanal adaptif yang dikondisikan kedua domain**", bukan pemodelan korelasi eksplisit. Aman diucapkan, jangan overclaim jadi "SE memodelkan korelasi penuh".

### Opsional (kejelasan)

Kalau mau mencegah penguji salah baca seperti tadi, tambahkan satu klausa di §2.8.3:

> "Perlu ditegaskan bahwa SE block **tidak menggantikan** konkatenasi, melainkan bekerja **di atasnya**: konkatenasi menyatukan kedua cabang menjadi satu vektor, lalu SE gating membobotinya secara adaptif. Istilah 'konkatenasi sederhana' merujuk pada konkatenasi tanpa pembobotan adaptif."

### Jawaban siap-ucap

> "Tidak bertentangan, Pak/Bu. Kami memang memakai konkatenasi — sebagai langkah **menyatukan** fitur kedua cabang — tetapi tidak berhenti di situ; hasil konkatenasi lalu dibobot secara adaptif oleh **SE gating**. Jadi fusi kami adalah **konkatenasi + SE gating**. Yang dibandingkan pada paragraf itu adalah konkatenasi **tanpa** gating (konkatenasi sederhana) versus konkatenasi **dengan** SE gating, dan arsitektur kami menggunakan yang kedua."

---

<a name="item-15"></a>

## Item 15 — Tingkat kompresi FFPP: HQ/LQ tidak diberi label c23/c40 (§2.9, docx line 663-666)

**Verdict: 🟡 BENAR — instingmu tepat. Standar FaceForensics++: RAW = c0, HQ = c23, LQ = c40. Paragrafmu benar arah tapi VAGUE (tak menyebut c23/c40) dan tidak konsisten dengan bagian lain dokumen yang sudah pakai c23/c40.**

### Peta baku FaceForensics++ (Rössler et al.)

| Level             | Label   | Kompresi                  | Keterangan                                       |
| ----------------- | ------- | ------------------------- | ------------------------------------------------ |
| RAW               | **c0**  | lossless / tanpa kompresi | tekstur paling utuh                              |
| HQ (high quality) | **c23** | H.264,**CRF 23**          | kualitas tinggi, kompresi ringan                 |
| LQ (low quality)  | **c40** | H.264,**CRF 40**          | kualitas rendah, kompresi berat (≈ media sosial) |

c23/c40 = nilai _Constant Rate Factor_ (CRF) H.264; CRF lebih tinggi → kompresi lebih berat. Jadi **HQ = c23, LQ = c40** — persis dugaanmu.

### Masalah pada paragraf (line 663-666)

- RAW (lossless) ✅ benar.
- HQ = "kompresi ringan (misalnya CRF rendah)" → arah benar (CRF 23 < 40), tapi **harus sebut c23 (CRF 23)** eksplisit.
- LQ = "kompresi berat" → benar, tapi **harus sebut c40 (CRF 40)**.

### Inkonsistensi internal (dokumenmu sendiri sudah pakai label itu)

- **line 318 & 330 (BAB III):** "kompresi **high-quality (c23)**", "FaceForensics++ (n=750, **c23**)" → **penelitian ini memakai c23 = HQ**.
- **line 625 (§2.7.3):** "akurasi turun ke 81,00% pada kompresi berat (**c40**)".

Jadi c23/c40 muncul di tempat lain, tetapi seksi dataset (§2.9) tidak menautkan HQ↔c23 dan LQ↔c40. Pembaca bisa mengira HQ dan c23 hal berbeda.

### Perbaikan

Ganti tiga butir jadi:

> 1. **RAW (c0, lossless):** tanpa kompresi, tekstur paling utuh.
> 2. **HQ (c23):** kompresi H.264 dengan CRF 23 (kualitas tinggi, kompresi ringan).
> 3. **LQ (c40):** kompresi H.264 dengan CRF 40 (kualitas rendah, kompresi berat, meniru unggahan media sosial).

Dan tambahkan satu kalimat penutup: "**Penelitian ini menggunakan versi HQ (c23)**, sesuai standar benchmark FaceForensics++." (Ini juga menyiapkan jawaban kalau penguji tanya "kalian pakai kompresi yang mana?" → c23, dan varied-compression = future work.)

### ⚠️ Bonus (temuan baru untuk [Item 11](#item-11)): "channel 4" lagi di BAB III

docx **line 793** (paragraf preprocessing FFT, dekat sitasi Sabir/Wang): _"...penelitian ini menambahkan informasi Frekuensi ke dalam informasi citra sebagai **channel 4** yang akan membawa informasi mengenai penyebaran frekuensi."_ → Ini **instans early-fusion ke-8** (di luar 7 yang sudah dicatat di Item 11). Sudah ditambahkan ke tabel perbaikan Item 11.

---

<a name="item-16"></a>

## Item 16 — Daftar "Artefak Spasial" (§2.9, docx line 670-675): butir (d) sebenarnya artefak TEMPORAL

**Verdict: 🔴 Butir (d) salah kategori DAN bentrok dengan pendekatan frame-level. + prosa bisa dirapikan. Instingmu ("gak enak") menangkap masalah nyata.**

### Masalah substansi (lebih penting dari gaya)

Daftar di bawah judul "**Artefak Spasial**" (artefak yang muncul pada **satu frame**):

- (a) Ketidaksesuaian warna kulit — spasial ✅
- (b) Tepi wajah tidak rapi akibat _blending_ — spasial ✅
- (c) Distorsi geometri mata/mulut — spasial ✅
- (d) **"Ketidakkonsistenan ekspresi saat frame berubah cepat"** — **TEMPORAL ❌** (antar-frame, bukan dalam satu frame)
- (e) _Blurring_ lokal — spasial ✅

Dua masalah pada (d):

1. **Salah kategori:** "ekspresi berubah saat frame berubah cepat" adalah anomali **antar-frame** (temporal), bukan artefak spasial satu-frame.
2. **Bentrok dengan metode kalian:** docx line 724 menegaskan penelitian ini **frame-level**, "diproses secara terpisah ... **tanpa memerlukan informasi sekuensial antar-frame**". Model kalian **tidak bisa** menangkap inkonsistensi temporal. Jadi mencantumkannya sebagai artefak yang relevan itu kontradiktif. (Aspek temporal memang ada di §2.x "Distorsi Spektral Temporal", tetapi itu **bukan** yang diimplementasikan.)

### Perbaikan (pilih satu)

- **(A, disarankan) Ganti (d)** dengan artefak spasial asli, ambil dari versi yang sudah benar di docx line 367: "**Inkonsistensi pencahayaan dan bayangan akibat _face warping_**." (tetap 5 butir, semuanya spasial).
- **(B)** Hapus (d) (jadi 4 butir).

### Sekalian rapikan prosa

- "Hal ini membuat **dataset ini**..." → dobel "ini" + "sangat berguna" agak hiperbolik. Ganti: "Keberagaman artefak ini menjadikan FaceForensics++ **relevan** untuk penelitian _hybrid_ XceptionNet–FFT."
- Judul butir "Artefak Spasial, artefak utama yang sering muncul meliputi:" → "**Artefak spasial**, yaitu anomali yang muncul pada **setiap frame**, di antaranya:".
- Konsisten: istilah asing dimiringkan (_blending_, _frame_, _blurring_, _face warping_, _patch_).

**Versi rapi (butir d diganti):**

> Setiap teknik manipulasi pada FaceForensics++ menghasilkan pola artefak yang berbeda, baik pada domain spasial maupun frekuensi. Keberagaman ini menjadikan _dataset_ tersebut relevan untuk penelitian _hybrid_ seperti XceptionNet–FFT.
>
> 1. **Artefak spasial**, yaitu anomali yang muncul pada setiap _frame_, di antaranya:
>    a. ketidaksesuaian warna kulit antara wajah sintetis dan latar;
>    b. tepi wajah tidak rapi akibat _blending_ yang buruk;
>    c. distorsi geometri pada area mata dan mulut;
>    d. inkonsistensi pencahayaan dan bayangan akibat _face warping_;
>    e. _blurring_ lokal pada area rekonstruksi.
>
> Penelitian sebelumnya menunjukkan artefak ini paling jelas pada area transisi wajah, sehingga deteksi difokuskan pada _patch_ wajah, bukan keseluruhan citra [4, 7]. (Butir penutup ini juga menjustifikasi _face cropping_ yang dipakai penelitian ini.)

_(Catatan: bila memilih titik-koma di daftar terasa banyak, ganti ke titik seperti format aslimu — sesuaikan dengan gaya no-`;`.)_

---

<a name="item-17"></a>

## Item 17 — Struktur membingungkan: dikotomi "artefak spasial/frekuensi" diulang 3× dengan 3 format berbeda

**Verdict: 🟡 Redundansi struktural. Bukan salah fakta, tapi bikin bingung (persis yang kamu rasakan). Dikotomi spasial/frekuensi muncul di 3 tempat dengan format berlainan, dan versi FFPP mengulang isi konseptual.**

### Kenapa terasa membingungkan — 3 kemunculan

| #   | Lokasi                                                                | Format                                                                        | Isi                                                          |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------ |
| A   | §"Artefak yang Dihasilkan Proses Generatif" (docx ~366-370)           | **sub-judul + prosa**: "Artefak Domain Spasial", "Artefak Domain Frekuensi"   | taksonomi UMUM artefak GAN (benar, bersih)                   |
| B   | §"Perbandingan Domain Spasial dengan Frekuensi" (Tabel 2.1)           | **tabel**                                                                     | perbandingan aspek (jenis info, artefak, generalisasi, dll.) |
| C   | §2.9 FFPP "Karakteristik Artefak pada FaceForensics++" (docx 667-687) | **daftar bernomor**: "1. Artefak Spasial (a-e)", "2. Artefak Frekuensi (...)" | **mengulang** taksonomi A, dibungkus "dalam FFPP"            |

Jadi pembaca ketemu "spasial vs frekuensi" tiga kali: sebagai **sub-bab prosa** (A), lalu **tabel** (B), lalu **daftar bernomor bersarang** (C). Peralihan format inilah yang terasa "tiba-tiba poin", dan C sebagian besar **mengulang** A.

### Rekomendasi — beri tiap tempat peran berbeda, jangan mengulang

- **A** = rumah taksonomi UMUM artefak spasial/frekuensi. **Pertahankan.**
- **B** = tabel perbandingan. **Pertahankan** (fungsinya beda).
- **C (FFPP)** = seharusnya **khusus FaceForensics++**, bukan mengulang taksonomi umum. Yang benar-benar khas FFPP adalah **artefak per-teknik** (Deepfakes/Face2Face/FaceSwap/NeuralTextures) — itu yang menarik dan tidak ada di A/B. Buang daftar generik "1. Artefak Spasial (a-e) / 2. Artefak Frekuensi", rujuk balik ke A, dan sisakan pemetaan per-teknik.

### Usulan penulisan ulang untuk §C ("Karakteristik Artefak pada FaceForensics++")

> Karena mencakup empat teknik manipulasi, FaceForensics++ menghadirkan artefak spasial maupun frekuensi sebagaimana dibahas pada sub-bab Artefak yang Dihasilkan Proses Generatif. Yang khas pada dataset ini adalah pola artefak yang berbeda-beda menurut tekniknya:
>
> - **Deepfakes** menyisakan batas _blending_ dan ketidaksesuaian warna pada wajah hasil _face-swap_.
> - **Face2Face** meninggalkan _warping_ berfrekuensi rendah dari _reenactment_ ekspresi.
> - **NeuralTextures** memunculkan tekstur berfrekuensi tinggi yang berulang dari _neural rendering_.
> - **FaceSwap** menunjukkan _spectral drop-off_ yang tidak konsisten pada tepi wajah.
>
> Keberagaman artefak lintas-teknik ini menjadikan FaceForensics++ ideal untuk model _hybrid_ yang memadukan domain spasial dan frekuensi, sebagaimana dilakukan pada penelitian ini.

### Efek samping positif

- Penulisan ulang §C ini **otomatis menyelesaikan [Item 16](#item-16)** (daftar generik "1. Artefak Spasial (a-e)" — termasuk butir temporal (d) — dibuang).
- **Simpan** kalimat justifikasi _face crop_ ("...artefak paling jelas pada area transisi wajah, deteksi fokus pada _patch_ wajah [4,7]") — pindahkan ke sub-bab _preprocessing/face cropping_ agar tidak hilang, karena itu argumen berharga.

### Tentang "bersarang poin di dalam poin"

Di §FFPP, sub-bagian berturut-turut semuanya daftar (4 teknik → 3 tingkat kompresi → 1./2. artefak → 5 alasan pemilihan). Kepadatan daftar beruntun ini menambah kesan berat. Setelah §C diringkas jadi pemetaan per-teknik di atas, bebannya berkurang. Untuk "Alasan Pemilihan FaceForensics++" (5 poin) boleh tetap daftar — itu wajar.

---

<a name="item-18"></a>

## Item 18 — "Alasan Pemilihan FaceForensics++" (§2.9, docx ~682-695): klaim faktual tanpa sitasi

**Verdict: 🟡 BENAR — instingmu tepat. Tiga klaim faktual berdiri tanpa sitasi. Plus satu klaim ("GAN dan non-GAN") kurang tepat secara teknis.**

### Klaim yang butuh sitasi

| Klaim (docx)                                                                                               | Masalah                                                                           | Sitasi yang tepat                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "FFPP mencakup metode manipulasi**GAN dan non-GAN**..." (Alasan 1)                                         | faktual soal komposisi FFPP,**tanpa sitasi** + istilah kurang tepat (lihat bawah) | **Rössler et al. [7]** (paper FF++)                                                                                                                                                                                                                                          |
| "...agar model memiliki**kemampuan generalisasi yang baik**" (Alasan 1)                                    | klaim argumentatif keragaman-teknik → generalisasi, tanpa dukungan                | tinjauan generalisasi (Rana et al. / Rao & Uehara) —**dan scope-kan**: keragaman metode membantu antar-_method_ di FFPP, tetapi generalisasi lintas-_dataset_ tetap tantangan (temuan kalian sendiri, [Item 10](#item-10))                                                   |
| "Penelitian deteksi deepfake**sering gagal pada video berkualitas rendah**" (Alasan 2)                     | faktual, tanpa sitasi                                                             | **Rössler et al. [7]** (Xception turun ~99%→81% pada c40 — sudah kalian kutip di docx line 625 sebagai [3,7]); dapat diperkuat Tan et al. [12] / FSBI [16] soal ketahanan frekuensi pada citra terkompresi                                                                   |
| "FFPP ... digunakan oleh**lebih dari ratusan publikasi sejak 2019**" (Alasan 4, "Benchmark Internasional") | klaim kuantitatif spesifik ("ratusan"), tanpa sitasi                              | **Rössler et al. [7]** (untuk "sejak 2019" + status benchmark) + **tinjauan sistematis** (Rana et al. / Rao & Uehara) yang mendokumentasikan pemakaian luas. Kalau angka "ratusan" sulit disumberkan, **perlunak** jadi "salah satu benchmark yang paling banyak digunakan". |

### ⚠️ Bonus akurasi: "GAN dan non-GAN" kurang tepat

Empat metode FFPP bukan pas dikotomi GAN/non-GAN:

- **Face2Face** & **FaceSwap** = berbasis **grafika komputer** (reenactment / 3D + _blending_), non-GAN.
- **Deepfakes** = berbasis **autoencoder** (encoder-decoder), bukan GAN murni.
- **NeuralTextures** = _neural rendering_ dengan komponen **adversarial** — ini yang paling dekat "GAN".

Jadi hanya NeuralTextures yang benar-benar adversarial; Deepfakes autoencoder; dua lainnya grafika. **Frasa lebih tepat:** "mencakup metode berbasis **grafika komputer** (_Face2Face_, _FaceSwap_) dan berbasis **pembelajaran** (_Deepfakes_, _NeuralTextures_)" — ini justru dikotomi yang dipakai paper FF++ [7], dan tetap mendukung poin "beragam teknik".

### Ringkas untuk dieksekusi

Tambahkan **[7]** di akhir kalimat Alasan 1 dan Alasan 2 (dan awal Alasan 4), tambah tinjauan (Rana/Rao) untuk klaim "ratusan publikasi" & "generalisasi", ganti "GAN dan non-GAN" → "grafika komputer dan pembelajaran". Perhatikan **desync penomoran** in-text vs Daftar Pustaka (lihat catatan [Item 10](#item-10)) saat menaruh nomor.

---

<a name="item-19"></a>

## Item 19 — Paragraf komposisi Celeb-DF (§2.10, docx line 709-713): angka benar, tapi sitasi [18] salah tunjuk + daftar tanpa penutup

**Verdict: 🟡 ISI ANGKA BENAR. Tapi (a) sitasi [18] kemungkinan menunjuk referensi SALAH (bukan paper Celeb-DF), dan (b) daftar 3 poin ditutup mendadak tanpa kalimat penutup (instingmu benar).**

### Cek fakta angka — semua BENAR ✅

| Klaim                                                   | Status                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Celeb-DF punya v1 dan v2, v2 lebih luas dipakai         | ✅ benar                                                                                        |
| Celeb-DF v2:**590 video asli**                          | ✅ benar (angka baku "Celeb-real" v2)                                                           |
| Celeb-DF v2:**5.639 video deepfake**                    | ✅ benar                                                                                        |
| "encoder-decoder yang disempurnakan"                    | ✅ benar (metode sintesis autoencoder yang ditingkatkan: resolusi 256×256, koreksi warna, dll.) |
| variasi tinggi (pencahayaan, resolusi, latar, ekspresi) | ✅ sesuai deskripsi paper                                                                       |

_(Opsional: v2 juga menambah 300 video "YouTube-real" untuk test set, tetapi 590/5.639 adalah angka baku yang dikutip mayoritas paper. Tak perlu diubah.)_

### 🔴 Masalah sitasi [18]

Paragraf ditutup dengan **[18]** untuk mendukung deskripsi Celeb-DF. Padahal di Daftar Pustaka (ekstraksi live .docx):

- **[18] = X. Luo dan Y. Wang, "Frequency-Domain Masking and Spatial Interaction..."** (2025) — **bukan** Celeb-DF.
- **[19] = Y. Li, X. Yang, P. Sun, H. Qi, S. Lyu, "Celeb-DF: A Large-scale Challenging Dataset for DeepFake Forensics"** (2020) — **INI** paper Celeb-DF.

Jadi seperti tertulis, [18] menyeret pembaca ke paper Frequency-Domain Masking, bukan Celeb-DF. Sitasi ini **seharusnya Li et al. (entri [19])**. Instans lain dari **desync penomoran** ([Item 10](#item-10)). **Aksi:** ganti [18]→[19] di sini (lebih baik: _refresh_ seluruh field Ctrl+A→F9 lalu verifikasi sitasi Celeb-DF me-resolve ke Li et al.). Cek juga [18] di paragraf lain (mis. line 715/716) apakah maksudnya Celeb-DF atau Frequency-Domain Masking.

### 🟡 Daftar 3 poin ditutup mendadak

Setelah butir 3, sub-bab langsung lompat ke "Peran Celeb-DF dalam Evaluasi Cross-Dataset" tanpa penutup. Tambahkan jembatan:

> "Perbedaan-perbedaan ini menjadikan Celeb-DF sebagai dataset uji yang lebih menantang dibanding FaceForensics++, sekaligus tolok ukur penting untuk menilai generalisasi model, sebagaimana diuraikan pada bagian berikut."

Menutup daftar sekaligus menyambung ke §2.10.2. (Pola "daftar tanpa penutup" ini sama dengan yang kamu rasakan di [Item 17](#item-17) — layak dicek juga di daftar lain.)

---

<a name="item-20"></a>

## Item 20 — "Alur preprocessing mencakup ekstraksi frame, deteksi wajah, cropping, resize, normalisasi, konversi skala warna, dan transformasi FFT" (§3-preprocessing, docx line ~730)

**Verdict: 🟡 Ketujuh langkah SEMUA nyata di kode ✅, tetapi (a) URUTANNYA tidak akurat, (b) daftar linear MENYEMBUNYIKAN percabangan RGB vs FFT, dan (c) "konversi skala warna" hanya untuk cabang FFT + istilah kurang tepat.**

### Cek keberadaan tiap langkah — semua ADA ✅

| Langkah diklaim      | Ada di kode? | Lokasi                                                                    |
| -------------------- | ------------ | ------------------------------------------------------------------------- |
| ekstraksi frame      | ✅           | `extract_frames.py`                                                       |
| deteksi wajah        | ✅           | MTCNN`detect_face_bbox` (jika `--face-crop`)                              |
| cropping             | ✅           | `crop_face` (margin 0.3)                                                  |
| resize               | ✅           | ke 224 — di FFT (`image_to_fft_logmag`) & di `spatial_transform`          |
| normalisasi          | ✅           | RGB: ImageNet mean/std; FFT: z-score (`deepfake_data.py:129`)             |
| konversi skala warna | ✅           | grayscale`img.convert("L")` — **hanya di cabang FFT** (`fft_utils.py:24`) |
| transformasi FFT     | ✅           | `np.fft.fft2` + high-pass + log1p                                         |

### 🟡 Masalah URUTAN

Klaim: ...resize → **normalisasi** → **konversi skala warna** → **transformasi FFT**. Yang benar di kode:

1. **Grayscale ("konversi skala warna") terjadi SEBELUM resize+FFT**, bukan setelah normalisasi. Alur FFT sebenarnya: `convert("L")` → `resize(224)` → `fft2` (`fft_utils.py:24-27`).
2. **Normalisasi FFT justru SETELAH transformasi FFT** (z-score pada log-magnitude, `deepfake_data.py:129`), padahal klaim menaruh "normalisasi" sebelum "transformasi FFT".
3. Jadi daftar linear itu menempatkan langkah pada urutan yang keliru untuk cabang frekuensi.

### 🟡 Menyembunyikan percabangan (ini inti masalahnya)

Pipeline sebenarnya **bercabang setelah cropping** menjadi dua representasi paralel:

```
ekstraksi frame → deteksi wajah → cropping
        ├─ cabang SPASIAL (RGB): resize 224 → normalisasi ImageNet        (tetap berwarna)
        └─ cabang FREKUENSI: grayscale → resize 224 → FFT (high-pass, log) → normalisasi z-score
```

Daftar linear tunggal menyiratkan satu rantai berurutan, padahal ada **front bersama + dua ekor paralel**. Penting juga: **grayscale hanya untuk cabang FFT** — citra RGB yang masuk XceptionNet tetap 3-kanal berwarna. Menyebut "konversi skala warna" sebagai langkah umum bisa disalahartikan seakan RGB pun di-grayscale-kan.

### Catatan istilah

"Konversi skala warna" ambigu (bisa dibaca konversi ruang warna, mis. RGB→YCbCr). Yang dilakukan kode = **RGB → skala keabuan (grayscale/luminance)**. Pakai "**konversi ke skala keabuan (grayscale)**".

### Konsistensi internal (prosa vs Tabel 2.4)

- **Prosa** (kalimat ini): 7 langkah, berakhir di "transformasi FFT", **memuat** "konversi skala warna".
- **Tabel 2.4**: 7 langkah (Ekstraksi, Deteksi wajah, Cropping, Resize, Normalisasi pixel, Transformasi FFT, **Channel fusion→4-channel**), **tanpa** grayscale.
  → Prosa dan tabel **tak sinkron** (prosa punya grayscale tanpa channel-fusion; tabel punya channel-fusion tanpa grayscale). Tabel-nya juga masih memuat "Channel fusion → 4-channel" yang keliru ([Item 11](#item-11) #5).

### Perbaikan (disarankan) — ganti daftar linear jadi deskripsi bercabang

> Alur preprocessing terdiri atas tahap bersama lalu bercabang. Tahap bersama meliputi ekstraksi _frame_, deteksi wajah, dan _cropping_ wajah. Selanjutnya setiap _frame_ diolah menjadi dua representasi: (1) cabang spasial (RGB) yang di-_resize_ ke 224×224 lalu dinormalisasi dengan statistik ImageNet, dan (2) cabang frekuensi yang dikonversi ke skala keabuan, di-_resize_, ditransformasikan dengan FFT (_high-pass_ dan _log-magnitude_), lalu dinormalisasi dengan _z-score_. Dengan demikian data masukan memiliki format seragam, representasi wajah yang stabil, dan struktur frekuensi yang tidak terdistorsi.

**Alternatif minimal** (tetap satu kalimat, hanya benahi urutan): "...ekstraksi frame, deteksi wajah, cropping, resize, konversi ke skala keabuan (khusus cabang frekuensi), transformasi FFT, dan normalisasi."

---

<a name="item-21"></a>

## Item 21 — Review menyeluruh §2.13 "Preprocessing" & §2.13.1 "Tahapan dan Alur Preprocessing"

**Verdict: 🔴 Seksi ini mengumpulkan banyak masalah — 2 sudah tercatat + 3 baru. Prioritas: kontradiksi temporal & Tabel 2.4.**

### Sudah tercatat (ada di seksi ini)

- **[Item 20](#item-20):** kalimat intro "Alur preprocessing mencakup ..." — urutan salah + sembunyikan percabangan + "konversi skala warna".
- **[Item 11](#item-11) #5:** **Tabel 2.4** baris 7 "Channel fusion → **Tensor 4-channel**" + caption "...digunakan sebagai **fitur tambahan** pada model hybrid" = framing early-fusion (padahal model late fusion).

### 🔴 BARU-1 — Kontradiksi temporal di "Ekstraksi Frame Video"

> "...pemrosesan per-frame memungkinkan **analisis lebih mendetail terhadap variasi temporal, seperti flickering dan inkonsistensi ekspresi**..."

Ini **bertentangan** dengan metode kalian. _Flickering_ dan "inkonsistensi ekspresi antar-frame" adalah fenomena **temporal** — butuh membandingkan/mengurutkan frame. Tapi §Analisis Video (kalimat tepat di atasnya) menegaskan penelitian ini **frame-level**, "diproses secara terpisah ... **tanpa informasi sekuensial antar-frame**". Pemrosesan per-frame independen **justru TIDAK bisa** menangkap flickering. Sama tema dengan [Item 16](#item-16). **Fix:** hapus/ubah kalimat ini, mis. → "pemrosesan per-frame memungkinkan model menangkap variasi artefak **spasial dan spektral** yang berbeda antar-frame **tanpa bergantung pada urutan temporal**."

### 🟡 BARU-2 — "Resize" kehilangan angka + inkonsistensi 299 vs 224

- Kalimat: "Citra kemudian **di-resize menjadi pixel** agar sesuai dengan input XceptionNet." → **angka "224×224" hilang** (kemungkinan teks/field terputus). Kalimat berikutnya baru menyebut "Ukuran 224×224". **Fix:** "di-resize menjadi **224×224 piksel**".
- Inkonsistensi: §Arsitektur XceptionNet menyatakan "citra masukan berukuran **299×299**" (spec asli Chollet), tetapi preprocessing me-_resize_ ke **224×224** (sesuai kode `image_size=224`). Frasa "agar sesuai dengan input XceptionNet" jadi rancu (input asli Xception 299). **Fix:** samakan cerita — implementasi kalian **memang 224×224**; sebutkan itu pilihan sadar (kompatibel _pretrained_ 224), dan jangan mengklaim 224 = "sesuai input asli Xception". (Sekalian "struktur local" → "struktur **lokal**".)

### 🟡 BARU-3 — Tabel 2.4 & langkah under-describe cabang FFT

Langkah bernomor dan Tabel 2.4 hanya menyebut "Transformasi FFT → Spektrum frekuensi". **Tidak ada**: konversi grayscale, _high-pass filtering_, maupun normalisasi z-score FFT. Padahal intro §2.13 menyebut "konversi skala warna". Jadi **intro (ada grayscale) vs Tabel 2.4 (tanpa grayscale, malah ada channel-fusion)** tak sinkron, dan cabang FFT tampil kurang utuh. **Fix:** buat langkah/tabel mencerminkan cabang FFT sebenarnya: grayscale → resize → FFT (high-pass, log) → normalisasi z-score; dan buang baris "channel fusion 4-channel".

### 🟡 BARU-4 — Duplikasi BAB II vs BAB III

Preprocessing juga dibahas ulang di **BAB III §3.3 "Tahapan Preprocessing Data"** (docx ~line 1100). Pastikan tidak saling bertentangan (mis. 224 vs 299, urutan langkah, ada/tidaknya channel-fusion). Idealnya BAB II = konsep, BAB III = implementasi spesifik penelitian (senada pola [Item 17](#item-17)).

### Ringkas prioritas fix di seksi ini

1. 🔴 Hapus klaim temporal (flickering/inkonsistensi ekspresi) di Ekstraksi Frame.
2. 🔴 Tabel 2.4: buang baris "Channel fusion → 4-channel", perbaiki caption ([Item 11](#item-11)).
3. 🟡 "di-resize menjadi **224×224 piksel**" + selaraskan 299/224.
4. 🟡 Lengkapi langkah cabang FFT (grayscale/high-pass/z-score), sinkronkan intro↔tabel.
5. 🟡 Cek konsistensi dengan BAB III §3.3.

> ✅ **Sudah dibuatkan versi ready copy-paste** (Item 20 + 21 terintegrasi, sitasi (Nama, Tahun)): **`documents/REVISI_BAB_II_2.13_Preprocessing_2026-07-03.md`**. Item 20 juga tercakup di file itu. Tabel 2.4 terkoreksi: **`documents/table/tabel_2_4_tahapan_preprocessing.html`**.

---

<a name="item-22"></a>

## Item 22 — "Gradient Clipping" (BAB II §2.15.4 rumus 2.29 + BAB III §3.5.6)

**Verdict: ✅ ISI & RUMUS BENAR, COCOK PERSIS dengan kode. Satu-satunya kekurangan: paragraf BAB II TANPA SITASI.**

### Cek fakta — semua BENAR ✅

| Klaim                                                | Kode                                                            | Status                                                              |
| ---------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------- |
| "gradient clipping berdasarkan norma L2"             | `clip_grad_norm_(...)` (default norm_type=2 = L2)               | ✅                                                                  |
| Rumus g←g bila ‖g‖₂≤c; g←g·(c/‖g‖₂) bila ‖g‖₂>c      | perilaku persis`clip_grad_norm_`                                | ✅                                                                  |
| "menjaga arah gradien, membatasi besarnya"           | penskalaan menjaga arah                                         | ✅                                                                  |
| ambang c =**max_norm**                               | `max_norm=5.0` (`train.py:117`)                                 | ✅ (BAB III Tabel hyperparameter tulis**max_norm = 5,0**, Norma L2) |
| "saat backbone pretrained dilepaskan (unfreezing)"   | backbone di-unfreeze epoch 4                                    | ✅                                                                  |
| "AMP:`scaler.unscale_()` sebelum clipping" (BAB III) | `scaler.unscale_()` lalu `clip_grad_norm_` (`train.py:116-117`) | ✅ persis                                                           |

Tidak ada kesalahan faktual. Nilai c = 5,0 konsisten antara kode, BAB III §3.5.6, dan Tabel hyperparameter.

### 🟡 Satu-satunya masalah: SITASI KOSONG

Paragraf §2.15.4 (line 845-846) **tidak memuat sitasi**, padahal teknik ini punya sumber jelas.

- **Termudah:** **(Goodfellow et al., 2016)** — buku _Deep Learning_ (MIT Press) membahas _gradient clipping_ (§10.11.1) dan **sudah ada di Daftar Pustaka** (line 2135). Tinggal tempel nama, tanpa menambah referensi baru.
- **Sumber primer (opsional):** **(Pascanu et al., 2013)** — _"On the difficulty of training recurrent neural networks"_ (ICML 2013), pengenalan _gradient norm clipping_. Belum ada di Daftar Pustaka; perlu ditambah bila dipakai.

**Aksi:** tambahkan **(Goodfellow et al., 2016)** di akhir kalimat pertama:

> "...diterapkan _gradient clipping_ berdasarkan norma L2 (Goodfellow et al., 2016)."

---

<a name="item-23"></a>

## Item 23 — "metrik evaluasi yang digunakan meliputi Confusion Matrix, Accuracy, Precision, Recall, dan F1-Score" (intro §2.16 Metrik Evaluasi)

**Verdict: 🔴 DAFTAR TIDAK LENGKAP — HILANG "AUC (Area Under the ROC Curve)", padahal AUC adalah metrik UTAMA penelitian. Ini kontradiksi dengan seluruh bagian dokumen lain.**

### Bukti bahwa AUC memang dipakai (dan justru paling utama)

- **Kode `src/metrics.py`** menghitung: `confusion_matrix`, `accuracy_score`, `precision_recall_fscore_support`, **`roc_auc_score`**, dan **`roc_curve`**. Jadi AUC + kurva ROC memang dihitung.
- **Kode `train.py`**: seleksi checkpoint terbaik pakai **val AUC** (`if val_metrics["auc"] > best_auc`, `:296`) dan **early stopping pada AUC** (`:305` "val AUC did not improve"). Jadi AUC = **metrik seleksi model & early stopping** — bukan sekadar pelengkap.
- **Abstrak** (line 52): "...menggunakan metrik akurasi, presisi, recall, F1-score, **dan AUC**...".
- **BAB I** (line 297, 302, 322): tujuan & cakupan menyebut "akurasi, presisi, recall, **dan AUC**".
- **BAB II** punya sub-bab tersendiri **§2.16.6 "Area Under the ROC Curve"** (TOC line 153).
- **BAB IV**: Kurva ROC (Gambar 4.4, 4.6), **Tabel 4.5 AUC In-Dataset**, perbandingan AUC (Gambar 4.8, 4.9). Hasil headline semuanya AUC.

Jadi **semua tempat lain menampilkan AUC**, hanya kalimat pengantar §2.16 ini yang melewatkannya. Padahal AUC justru **metrik yang paling menentukan** di skripsi ini. Penguji hampir pasti menyorot ini.

### Masalah kedua — "Seluruh metrik dihitung berdasarkan hasil prediksi ... kelas sebenarnya"

Setelah AUC dimasukkan, kalimat ini jadi **tidak akurat untuk AUC**. Accuracy/Precision/Recall/F1/Confusion Matrix dihitung dari **label prediksi** (pada ambang θ = 0,5), tetapi **AUC dihitung dari skor probabilitas** model (`y_prob`) dan **independen terhadap ambang** — justru itulah alasan AUC dipakai sebagai metrik utama. Jadi jangan menyamaratakan "seluruh metrik dari hasil prediksi (label)".

### Perbaikan (disarankan)

> "Pada penelitian ini, metrik evaluasi yang digunakan meliputi _Confusion Matrix_, _Accuracy_, _Precision_, _Recall_, _F1-Score_, dan _Area Under the ROC Curve_ (AUC). Metrik _Accuracy_, _Precision_, _Recall_, dan _F1-Score_ dihitung dari hasil prediksi model pada ambang tertentu (θ = 0,5) terhadap kelas sebenarnya, sedangkan AUC dihitung dari skor probabilitas model sehingga bersifat independen terhadap ambang. AUC digunakan sebagai **metrik utama** untuk seleksi model dan _early stopping_ karena sifatnya yang tahan terhadap ketidakseimbangan kelas dan tidak bergantung pada pemilihan ambang."

Menambahkan AUC di sini sekaligus **menyelaraskan** intro §2.16 dengan §2.16.6, abstrak, BAB I, dan BAB IV.

---

<a name="item-24"></a>

## Item 24 — Pertanyaan penguji: "Kenapa (studi) komparatif? Apakah ada paper ilmiah yang menyarankan?"

**Verdict: ❓ Pertanyaan antisipatif. Jawaban kuat + ada dasar paper. Ringkas: pertanyaan riset kami memang komparatif secara inheren, mengisi celah literatur, dan protokol evaluasi komparatif lintas-dataset memang direkomendasikan/ditetapkan oleh paper benchmark & survei.**

### Kenapa komparatif (3 alasan)

1. **Pertanyaan risetnya memang komparatif.** Tujuan kami mengukur **kontribusi domain frekuensi**. Satu-satunya cara ilmiah mengisolasi kontribusi itu adalah **membandingkan** model domain-tunggal (spasial, frekuensi) vs hybrid **di bawah kondisi identik** (dataset, backbone, training, split, seed sama). Ini pada dasarnya **ablation terkontrol** — variabel bebasnya arsitektur, sisanya dijaga tetap. Tanpa baseline domain-tunggal, kontribusi frekuensi tidak bisa diatribusikan.
2. **Mengisi celah literatur.** Metode hybrid (SpecXNet, FSBI, frequency-aware) **mengklaim** fusi frekuensi meningkatkan generalisasi, tetapi sebagian besar dioptimalkan untuk **in-dataset FF++** dan **belum menguji kontribusi itu secara sistematis lintas-dataset**. Kalian sudah menyatakan ini eksplisit di BAB II ("...belum mengevaluasi secara sistematis kontribusi fusi late dan gating terhadap robustness lintas dataset. Penelitian ini mengisi celah tersebut"). Studi komparatif = **verifikasi terkontrol** atas klaim yang belum terbukti.
3. **Jujur terhadap temuan.** Ternyata kontribusi frekuensi **terbatas** (freq ≈ tebakan acak, hybrid tidak mengungguli spasial). Framing **komparatif** (mengukur kontribusi) adalah wadah yang tepat untuk menyampaikan temuan itu — lebih jujur daripada mengklaim arsitektur baru yang superior. Hasil negatif/terbatas yang terverifikasi adalah **kontribusi ilmiah yang sah** (mengoreksi asumsi over-optimistik di literatur).

### "Ada paper yang menyarankan?" — YA, ada dasarnya

- **(Li et al., 2020 — Celeb-DF)** **menetapkan protokol evaluasi komparatif lintas-dataset** (latih FaceForensics++ → uji Celeb-DF) sebagai tolok ukur yang menantang. Protokol inilah yang kami ikuti; jadi desain komparatif cross-dataset kami mengikuti benchmark yang sudah baku.
- **(Rana et al., 2022 — Systematic Literature Review)** dan **(Rao & Uehara, 2025 — Chronological Review)**: survei sistematis menegaskan bahwa **generalisasi lintas-dataset, bukan akurasi in-dataset, adalah metrik paling relevan**, dan banyak metode **overfit** ke dataset pelatihan (penurunan AUC 10–20 poin lintas-dataset). Ini **secara langsung merekomendasikan** pendekatan evaluasi komparatif yang kami pakai. (Sudah kalian kutip di BAB II.)
- **Metodologi ablation/perbandingan terkontrol adalah standar** di bidang ini — bahkan paper yang kami bandingkan memakainya: **SpecXNet** melakukan ablation modul (DDFC/DFA, backbone ResNet vs Xception); **(Durall et al., 2020)** membandingkan spektrum citra real vs GAN. Jadi membandingkan untuk mengatribusikan kontribusi = norma keilmuan, bukan pilihan yang perlu dibela.

### Jawaban siap-ucap (± 30 detik)

> "Karena pertanyaan riset kami memang komparatif: kami ingin mengukur **seberapa besar kontribusi domain frekuensi**, dan itu hanya bisa dijawab dengan **membandingkan** model spasial, frekuensi, dan hybrid pada kondisi yang identik — sebuah ablation terkontrol. Ini mengisi celah nyata: metode hybrid di literatur mengklaim manfaat frekuensi untuk generalisasi, tetapi jarang mengujinya secara sistematis lintas-dataset. Soal dasar ilmiah: protokol komparatif lintas-dataset (latih FF++, uji Celeb-DF) justru **ditetapkan oleh Li et al. (2020)** pada paper Celeb-DF, dan survei seperti **Rana et al. (2022)** serta **Rao & Uehara (2025)** menegaskan bahwa generalisasi lintas-dataset adalah metrik yang paling relevan. Jadi desain komparatif kami mengikuti rekomendasi dan benchmark yang sudah baku di bidang ini."

### Kalau ditekan "berarti tidak ada kontribusi baru?"

> "Kontribusi kami adalah **verifikasi terkontrol** atas klaim yang belum terbukti, plus temuan bahwa kontribusi frekuensi **terbatas** pada kondisi terkompresi/face-crop — temuan yang justru mengoreksi optimisme literatur dan mengarahkan penelitian lanjutan (fasa/SPSL, FFT citra penuh). Studi komparatif yang jujur dan terkontrol adalah bentuk kontribusi ilmiah yang sah."

---

<a name="item-25"></a>

## Item 25 — Pertanyaan penguji: "Kenapa nilai learning rate sekian-sekian? Ada paper? Kenapa tidak hyperparameter fine-tuning kalau resource terbatas?"

**Verdict: ❓ Antisipatif. Nilai LR = resep transfer-learning yang PRINSIPIL (bukan asal), metodenya punya sitasi, dan TIDAK men-tuning HP justru pilihan tepat untuk studi komparatif + realistis untuk resource.**

### Nilai LR aktual (kode `train.py:189-221`, `config.yaml`)

| Kelompok parameter                  | LR                                               | Rasio     | Alasan                                                    |
| ----------------------------------- | ------------------------------------------------ | --------- | --------------------------------------------------------- |
| _Head_ / fusion (lapisan baru)      | **2e-4**                                         | 1× (base) | dilatih dari nol → perlu belajar cepat                    |
| _Backbone_ XceptionNet (pretrained) | **2e-5**                                         | **÷10**   | _fine-tuning_ lembut agar fitur ImageNet tak rusak        |
| Cabang FreqCNN (hybrid)             | **5e-5**                                         | **×0,25** | init acak tapi dibatasi agar tak mendominasi gradien awal |
| Optimizer                           | **AdamW**, wd **1e-4**                           | —         | cocok utk skala gradien berbeda antar cabang              |
| Jadwal                              | _warmup_ 3 epoch → _cosine decay_ (eta_min 1e-6) | —         | cegah instabilitas awal (mis. saat unfreeze epoch 4)      |

### Q1 — Kenapa nilai itu? (prinsipil, bukan asal)

Ini **discriminative / differential learning rate** untuk transfer learning: lapisan baru cepat, backbone pretrained pelan (÷10), cabang frekuensi menengah (×0,25). Semua **diturunkan dari peran tiap komponen**, bukan angka ajaib. Nilai _base_ **2e-4** dengan AdamW adalah **default yang lazim & teruji** untuk _fine-tuning_ CNN; _warmup→cosine_ adalah jadwal standar modern.

### Q2 — Ada paper? YA untuk metodenya

- **Optimizer:** **(Kingma & Ba, 2015)** Adam — sudah dikutip [44]; **(Loshchilov & Hutter, 2019)** AdamW _decoupled weight decay_ — sudah dikutip [45]. ✅ ada di Daftar Pustaka.
- **Differential/discriminative LR** (backbone LR lebih rendah): prinsip dari **(Howard & Ruder, 2018)** ULMFiT — _discriminative fine-tuning_. **Belum** di Daftar Pustaka; bisa ditambah bila mau sitasi eksplisit di §3.5.2.
- **_Warmup_ + _cosine annealing_:** _cosine_ dari **(Loshchilov & Hutter, 2017)** SGDR; _warmup_ dari **(Goyal et al., 2017)**. **Belum** di Daftar Pustaka; opsional ditambah di §3.5.3.
- **Nilai spesifik 2e-4** = _default_ konvensional, bukan dari satu paper. Jujur saja: konvensi tidak wajib disitasi angka-per-angka; yang disitasi adalah **metode**-nya (Adam/AdamW, differential LR, cosine).

### Q3 — Kenapa tidak HP-tuning? (INI kuncinya — 2 argumen saling menguatkan)

**(a) Metodologis (paling kuat):** Ini **studi komparatif** ([Item 24](#item-24)). Tujuannya membandingkan arsitektur pada **kondisi identik**. Kalau tiap model di-tuning terpisah, muncul **confound** — perbedaan bisa jadi karena **usaha tuning**, bukan arsitektur. Memakai **hyperparameter baku yang sama** untuk ketiga model menjaga perbandingan **adil & terkontrol**. Jadi HP tetap = **pilihan desain untuk validitas internal**, bukan sekadar alasan resource.

**(b) Praktis (resource):** Matriks eksperimen sudah besar: **3 model × 2 dataset × 4 ukuran sampel × 3 seed = 72 run**. Grid search sederhana (mis. 3 LR × 3 WD = 9 konfig) akan mengalikannya ~9× → ratusan run, **tidak feasible di Colab**.

**(c) Mitigasi (mengurangi kebutuhan tuning):** kami pakai default prinsipil + **early stopping pada val AUC** (adaptif, kurangi sensitivitas terhadap LR/epoch) + _warmup_ + differential LR. HP-tuning per-model dinyatakan sebagai **future work**.

### Jawaban siap-ucap

> "Nilai learning rate kami bukan asal: ini resep _transfer learning_ berjenjang — lapisan baru 2×10⁻⁴, backbone pretrained sepuluh kali lebih rendah agar fitur ImageNet tidak rusak, dan cabang frekuensi di antaranya. Metodenya berdasar paper: Adam (Kingma & Ba, 2015) dan AdamW (Loshchilov & Hutter, 2019) yang sudah kami kutip, plus prinsip _discriminative fine-tuning_ (Howard & Ruder, 2018) dan _cosine schedule_ (Loshchilov & Hutter, 2017). Soal kenapa tidak _hyperparameter tuning_: karena ini **studi komparatif**, justru kami sengaja memakai hyperparameter baku **yang sama** untuk ketiga model supaya perbandingannya **adil** — kalau tiap model di-tuning terpisah, perbedaan hasilnya bisa disebabkan usaha tuning, bukan arsitektur. Selain itu matriks 72 run kami sudah di batas resource Colab. Kami mitigasi dengan _early stopping_ berbasis AUC, dan _tuning_ per-model kami catat sebagai penelitian lanjutan."

### Antisipasi lanjutan: "Mungkin cabang frekuensi lemah karena LR-nya tak di-tuning?"

> "Cabang frekuensi sudah kami beri LR khusus (5×10⁻⁵) agar tidak tertekan. Lemahnya lebih dijelaskan oleh **representasi magnitudo-saja** dan **hilangnya sidik jari spektral akibat kompresi/face-crop** ([Item 5](#item-5), [Item 8](#item-8)), bukan LR. Tuning khusus cabang frekuensi memang arah future work."

---

<a name="item-26"></a>

## Item 26 — "SE gate seharusnya membantu, tapi malah menyeret turun hybrid — bagaimana kalau SE gate dihapus?"

**Verdict: ❓ Premis perlu DIKOREKSI (SE gate ≠ membuang low-freq). Data MEMBENARKAN bahwa hybrid < spatial (fusi menyeret turun). Tapi "hapus SE gate" BELUM tentu memperbaiki, dan kita BELUM punya ablasinya — ini eksperimen yang layak dijalankan.**

### 1. Koreksi premis: SE gate TIDAK "membuang low frequency"

Dua hal berbeda (jangan tertukar):

- **Membuang/menekan low frequency** = tugas **_high-pass filter_** di preprocessing FFT ([Item 4](#item-4)) — langkah tetap, di ranah frekuensi.
- **SE gate** = _channel attention_ **pada vektor fitur gabungan 512-d** (256 spasial + 256 frekuensi). Ia membobot ulang **dimensi fitur hasil belajar**, bukan pita frekuensi. Tujuannya: adaptif menonjolkan modalitas yang lebih berguna per-input. Jadi SE gate **tidak** beroperasi pada "low frequency".

### 2. Data membenarkan "hybrid diseret turun" (in-dataset AUC, tier terpercaya)

| Dataset   | spatial | hybrid | freq  | drag (hybrid−spatial) |
| --------- | ------- | ------ | ----- | --------------------- |
| CDF n250  | 0,914   | 0,787  | 0,500 | **−0,127**            |
| CDF n500  | 0,945   | 0,839  | 0,549 | **−0,106**            |
| FFPP n250 | 0,743   | 0,540  | 0,469 | **−0,203**            |
| FFPP n500 | 0,693   | 0,616  | 0,545 | **−0,077**            |

Konsisten **spatial > hybrid > freq**. Hybrid tertarik **ke bawah, ke arah cabang freq yang lemah** → fusi + SE gate **gagal melindungi** performa spasial.

### 3. Kenapa SE gate gagal melindungi?

- **SE gate itu SOFT** (`Sigmoid`, `x * gate(x)` — `hybrid_fusion.py:20,24`): bobot ∈ (0,1), **tak pernah 0**. Jadi ia bisa **meredam** tapi **tak bisa mematikan** dimensi freq → noise selalu bocor.
- **Fitur freq selalu ter-konkatenasi** ke classifier (512-d), apa pun bobot gate-nya. Classifier dilatih di atas vektor gabungan → dimensi freq yang berisik menambah variansi dan bisa memicu **overfitting ke pola spektral semu**.
- Jadi drag berasal dari **fakta bahwa cabang lemah ikut difusikan**, bukan khusus dari SE gate.

### 4. "Kalau SE gate dihapus?" — jujur: BELUM diukur, dan kemungkinan TIDAK menyelesaikan

- Matriks eksperimen kita = spatial / freq / hybrid. **Tidak ada** varian "hybrid tanpa SE gate", jadi **tidak ada angka** untuk dijawab pasti.
- Penalaran: hapus SE gate → concat polos → classifier. Fitur freq **tetap** masuk classifier, jadi **drag kemungkinan tetap ada**. SE gate justru dirancang untuk **membantu** (meredam adaptif); menghapusnya tak otomatis memperbaiki. Efeknya bisa sedikit membaik (parameter lebih sedikit) atau memburuk (kehilangan peredaman) — **genuinely uncertain tanpa eksperimen**.
- Yang benar-benar mengangkat hybrid ke level spasial bukan "hapus SE gate", melainkan **membuang/keras-gerbang cabang freq** atau memperkuat penekanannya.

### 5. Ablation yang tepat untuk menjawabnya (layak dijalankan)

- **(A) Hybrid TANPA SE gate** (concat → classifier langsung) → mengisolasi kontribusi SE gate. Jika hybrid-tanpa-SE ≈ hybrid → SE gate bukan biang; jika ≈ spatial → SE gate bagian masalah.
- **(B) Hybrid dengan cabang freq di-nol-kan** → cek waras: seharusnya ≈ spatial (memastikan mesin fusi tak rusak).
- **(C) Hard-gate / bobot cabang skalar yang dipelajari** → uji apakah penekanan lebih kuat memulihkan performa spasial.

Hasil apa pun berguna: (A) membela desain SE **atau** menjadi temuan ("channel-attention lunak tak cukup menetralkan modalitas lemah pada late fusion").

### Jawaban siap-ucap

> "Perlu diluruskan dulu: SE gate tidak membuang frekuensi rendah — itu tugas _high-pass filter_ di preprocessing. SE gate adalah atensi kanal pada vektor fitur gabungan yang mestinya meredam modalitas yang kurang berguna. Data kami memang menunjukkan hybrid di bawah spasial, artinya SE gate **tidak berhasil sepenuhnya** meredam cabang frekuensi yang lemah — wajar, karena SE gate bersifat _soft_ (sigmoid, tak pernah nol) dan fitur frekuensi tetap terkonkatenasi. Menghapus SE gate belum tentu memperbaiki, karena akar masalahnya adalah **memfusikan cabang yang lemah**, bukan gerbangnya. Kami belum menjalankan ablasi tanpa-SE, dan itu justru **eksperimen ablation yang tepat** untuk memastikannya — kami catat sebagai kelanjutan."

> 💡 **Ini eksperimen kecil & runnable.** Ablasi (A) hanya perlu satu flag untuk melewati `se_gate` di `HybridTwoBranch.forward`, lalu latih ulang hybrid. Bisa dibuatkan bila mau bukti empiris untuk sidang.

---

<a name="item-27"></a>

## Item 27 — Dua paragraf "Pemilihan Metode" (§ sebelum "Pemilihan Transformasi FFT", docx line 953 & 955): klaim empiris & research-gap TANPA sitasi + kontradiktif

**Verdict: 🔴 Instingmu benar dua-duanya. Paragraf 1: klaim "terbukti unggul secara empiris" tanpa sitasi DAN salah atribusi (cross-dataset ke XceptionNet). Paragraf 2: klaim "sebagian besar penelitian memisahkan" tanpa menyebut penelitian mana DAN bertentangan dengan BAB II sendiri.**

### Paragraf 1 (line 953) — "dua metode utama ... telah terbukti unggul secara empiris ... akurasi, efisiensi, cross-dataset robustness"

**Masalah:**

1. **Tanpa sitasi** sama sekali, padahal klaimnya kuat ("terbukti unggul secara empiris dalam berbagai penelitian").
2. **Salah atribusi cross-dataset ke XceptionNet.** XceptionNet unggul untuk **akurasi in-dataset + efisiensi**, tetapi **generalisasi lintas-dataset-nya JUSTRU LEMAH** — itu premis & temuan kalian sendiri (dan [Item 10](#item-10)). Menyebut XceptionNet "terbukti unggul dalam cross-dataset robustness" **menggerus tesis kalian sendiri**.
3. **Cross-dataset FFT sebagai "sudah terbukti".** Ketahanan lintas-dataset domain frekuensi adalah **klaim/harapan** literatur — dan hasil kalian **justru membantahnya** (freq ≈ tebakan acak). Menyatakannya "telah terbukti unggul" bertentangan dengan hasil, sekaligus **melemahkan alasan penelitian** (kalau sudah terbukti, kenapa diteliti? → [Item 24](#item-24)).

**Rewrite (dengan sitasi (Nama, Tahun), klaim didisentangle):**

> "Dalam penelitian ini digunakan dua metode utama, yaitu FFT sebagai representasi domain frekuensi dan XceptionNet sebagai model ekstraksi fitur spasial. XceptionNet dipilih karena efisiensi _depthwise separable convolution_ (Chollet, 2017) dan performanya sebagai detektor domain spasial terbaik pada FaceForensics++ (Rössler et al., 2019), meskipun keunggulan ini umumnya bersifat _in-dataset_. FFT dipilih karena analisis domain frekuensi **dilaporkan** mampu menangkap artefak sintesis yang bersifat algoritmik dan lebih stabil lintas dataset (Durall et al., 2020; Zhang et al., 2019; Tan et al., 2024; Hasanaath et al., 2023). Perlu ditekankan bahwa klaim ketahanan lintas-dataset domain frekuensi inilah yang **justru diuji secara empiris** pada penelitian ini, bukan diasumsikan sebagai fakta yang sudah pasti."

### Paragraf 2 (line 955) — "sebagian besar penelitian terdahulu masih MEMISAHKAN pendekatan spasial dan frekuensi ..."

**Masalah:**

1. **"Penelitian mana?"** — tak ada satu pun sitasi. Klaim research-gap wajib menyebut karya yang dimaksud.
2. **Kontradiksi internal.** BAB II kalian sendiri (line 291) justru membahas metode **hybrid yang MENGGABUNGKAN** spasial+frekuensi: SpecXNet, FSBI, Frequency-Domain Masking. Jadi "sebagian besar masih memisahkan" **bertentangan** dengan related-work kalian. Gap yang benar (dan sudah kalian tulis di line 291): hybrid **sudah ada**, tetapi dioptimalkan untuk **in-dataset FFPP** dan **belum mengukur kontribusi domain frekuensi terhadap robustness lintas-dataset secara sistematis**.

**Rewrite (gap yang akurat + sitasi):**

> "Sejumlah penelitian terkini telah menggabungkan domain spasial dan frekuensi, misalnya SpecXNet (Alam et al., 2025), FSBI (Hasanaath et al., 2023), dan _Frequency-Domain Masking_ (Luo & Wang, 2025). Namun, pendekatan hybrid tersebut sebagian besar **dioptimalkan untuk performa in-dataset** pada FaceForensics++ dan **belum mengevaluasi secara sistematis seberapa besar kontribusi domain frekuensi terhadap ketahanan lintas-dataset** (Rana et al., 2022; Rao & Uehara, 2025). Penelitian ini mengisi celah tersebut dengan merancang model hybrid FFT–XceptionNet, sekaligus **mengukur kontribusi domain frekuensi melalui perbandingan terkontrol** antar model."

### Sitasi yang dipakai (Nama, Tahun)

(Chollet, 2017), (Rössler et al., 2019), (Durall et al., 2020), (Zhang et al., 2019), (Tan et al., 2024), (Hasanaath et al., 2023), (Alam et al., 2025), (Luo & Wang, 2025), (Rana et al., 2022), (Rao & Uehara, 2025) — semuanya sudah ada di Daftar Pustaka.

### Kalau penguji menyorot

> "Betul, dua paragraf ini akan kami lengkapi sitasinya dan luruskan. Keunggulan XceptionNet yang terbukti adalah **in-dataset dan efisiensi**, bukan generalisasi lintas-dataset; sedangkan ketahanan lintas-dataset domain frekuensi adalah **klaim literatur yang justru kami uji**. Untuk klaim research-gap, kami akan menyebut karya spesifik (SpecXNet, FSBI, Frequency-Domain Masking) dan memperbaiki gap-nya menjadi 'hybrid sudah ada tetapi belum mengukur kontribusi frekuensi lintas-dataset', konsisten dengan related-work di BAB II."

---

<a name="item-28"></a>

## Item 28 — EfficientNet dibandingkan berulang kali tanpa sitasi & tanpa entri Daftar Pustaka (§2.18 "Pemilihan Arsitektur XceptionNet")

**Verdict: 🔴 Instingmu benar. EfficientNet dipakai sebagai pembanding **5×** (termasuk sub-judul & baris Tabel 2.8 dengan angka spesifik), tetapi **tidak ada satu pun sitasi** dan **tidak ada di Daftar Pustaka**. Lebih jauh: **tidak ada studi yang dikutip yang benar-benar membandingkan XceptionNet vs EfficientNet** pada deteksi deepfake — jadi klaim perbandingannya tak terdukung.**

### Di mana EfficientNet muncul (semua tanpa referensi EfficientNet)

| Lokasi                | Kutipan                                                                     | Sitasi tertera     | Masalah                                                                   |
| --------------------- | --------------------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------- |
| line 977              | "lebih efisien ... dibandingkan ResNet dan**EfficientNet**"                 | [3, 4]             | [3]=Haq, [4]=Afchar — bukan sumber EfficientNet                           |
| line 979              | "Dibandingkan**EfficientNet** ... XceptionNet lebih peka tekstur ... [13]"  | [13]=SpecXNet      | SpecXNet tak menguji EfficientNet                                         |
| line 981              | "Terbukti akurasi lebih tinggi dibanding ResNet dan**EfficientNet**"        | —                  | tak ada sumber yang membandingkan                                         |
| line 1000 (Tabel 2.8) | "**EfficientNet** \| 94–96% \| 18M \| kurang sensitif tekstur"              | caption [3,4,13,7] | **angka spesifik tanpa sumber**                                           |
| line 1007             | "SpecXNet [13] ... XceptionNet lebih tangguh dibanding ...**EfficientNet**" | [13]=SpecXNet      | **misatribusi** — SpecXNet ablasi ResNet/Xception, **bukan** EfficientNet |

### Tiga masalah

1. **Arsitektur EfficientNet (Tan & Le, 2019) tidak dikutip di mana pun** dan **tidak ada di Daftar Pustaka**. ⚠️ Hati-hati: ada "C. Tan" di Daftar Pustaka, tapi itu **Chuangchuang Tan** (Frequency-Aware Deepfake, AAAI-24, in-text [13]) — **BUKAN** Mingxing Tan (EfficientNet). Jangan dikira sudah tersitasi.
2. **Angka Tabel 2.8 untuk EfficientNet (94–96%, 18M, "kurang sensitif tekstur") tanpa sumber.** Tidak ada di [3,4,13,7]. Ini **risiko data fabrikatif** — dari mana angka itu?
3. **Klaim "XceptionNet lebih akurat / lebih peka tekstur daripada EfficientNet" tak terdukung.** Rössler [7] membandingkan Xception vs ResNet vs MesoNet (bukan EfficientNet); SpecXNet [13] membandingkan Xception vs ResNet (bukan EfficientNet). Jadi **tidak ada studi terkutip** yang menguji Xception vs EfficientNet. Menyematkan [13]/[7] untuk klaim ini = **misatribusi**. (Catatan teknis: EfficientNet juga memakai _depthwise separable conv_ + SE via MBConv, jadi "kurang peka tekstur" pun lemah secara argumentatif.)

### Dua jalan perbaikan

**Jalan 1 (kalau EfficientNet dipertahankan):**

- Tambahkan **(Tan & Le, 2019)** — "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" (ICML 2019) — ke Daftar Pustaka, sitir saat EfficientNet diperkenalkan.
- **Sumberkan angka Tabel 2.8** (94–96%/18M). Bila tak ada studi deepfake yang menguji EfficientNet di FF++, **hapus angka akurasinya** (biarkan jumlah parameter saja, itu dari Tan & Le) dan jangan mengklaim "terbukti lebih tinggi".
- Lunakkan klaim: bukan "terbukti akurasi lebih tinggi", tetapi "EfficientNet belum lazim dipakai/divalidasi sebagai baseline deepfake pada FF++, sedangkan XceptionNet sudah menjadi standar".

**Jalan 2 (disarankan — lebih bersih): buang perbandingan EfficientNet.**

- Justifikasi terkuat XceptionNet: **standar de-facto** deteksi deepfake (dipakai FF++, dibangun-atas oleh SpecXNet) → memungkinkan **komparabilitas** dengan literatur. Argumen ini **tidak butuh** EfficientNet.
- Karena tak ada sumber yang membandingkan Xception vs EfficientNet, membuang tangent ini menghilangkan klaim tak-terdukung + angka tak-bersumber sekaligus. Pertahankan perbandingan ResNet/MesoNet (itu **memang** terkutip via Rössler [7]).

### Kalau penguji menyorot ("EfficientNet dari mana?")

> "Perbandingan EfficientNet akan kami perbaiki. Tidak ada studi yang kami kutip yang benar-benar menguji EfficientNet pada deteksi deepfake, sehingga klaim akurasi dan angka pada Tabel 2.8 tidak kami dasari sumber yang tepat. Kami akan memilih salah satu: menambahkan referensi asli EfficientNet (Tan & Le, 2019) dengan klaim yang dilunakkan dan angka yang disumberkan, atau membuang perbandingan EfficientNet dan bersandar pada argumen bahwa XceptionNet adalah **baseline standar** deteksi deepfake demi komparabilitas. Pemilihan backbone alternatif kami catat sebagai penelitian lanjutan."

### 🔧 PERBAIKAN (refined, per catatan penulis 2026-07-03): Tan & Le TIDAK menguji EfficientNet pada FaceForensics

Poin penting: **(Tan & Le, 2019) hanya menguji EfficientNet pada ImageNet** (klasifikasi umum), **bukan** pada FaceForensics++/deteksi deepfake. Jadi menambahkan (Tan & Le, 2019) **hanya bisa menyumberkan** klaim efisiensi parameter/arsitektur umum — **TIDAK** bisa menyumberkan angka "94–96% pada FaceForensics++" maupun klaim "Xception lebih akurat dari EfficientNet pada deepfake". Angka FF++ EfficientNet **tetap tak bersumber** apa pun yang terjadi → **wajib dibuang**.

**Keputusan fix (disarankan): pertahankan penyebutan EfficientNet secara jujur & singkat (sitir Tan & Le hanya untuk efisiensi parameter), tetapi BUANG semua angka FF++ dan klaim superioritas deepfake, dan HAPUS baris EfficientNet dari Tabel 2.8.**

**Ready copy-paste — §2.18.2 (sitasi (Nama, Tahun)):**

> Arsitektur XceptionNet (_Extreme Inception Network_) dipilih untuk mengekstraksi fitur spasial secara efisien melalui _depthwise separable convolution_, yang memisahkan konvolusi per kanal (_depthwise_) dari penggabungan antarkanal (_pointwise_). Desain ini membuat XceptionNet efisien secara parameter dibandingkan arsitektur konvensional seperti ResNet, sekaligus mempertahankan sensitivitas tinggi terhadap tekstur, tepi, dan pola detail pada citra wajah hasil manipulasi (Chollet, 2017; Afchar et al., 2018).
>
> Penelitian Afchar et al. (2018) dengan MesoNet menunjukkan arsitektur CNN dangkal dapat mendeteksi wajah palsu secara efektif, meskipun akurasinya menurun pada dataset yang lebih kompleks. Rössler et al. (2019) melaporkan XceptionNet mencapai akurasi hingga 99,26% pada FaceForensics++, melampaui ResNet dan MesoNet. Haq (2021), yang membandingkan XceptionNet dan ResNet-50 dengan _Gaussian filter_ dan _Local Binary Pattern_ (LBP), menemukan XceptionNet tidak hanya lebih akurat tetapi juga lebih cepat.
>
> Arsitektur lain seperti EfficientNet (Tan & Le, 2019) menawarkan efisiensi jumlah parameter yang baik pada tugas klasifikasi umum, tetapi **belum divalidasi secara luas sebagai _baseline_ deteksi deepfake pada FaceForensics++**, sehingga perbandingan empiris langsung pada tugas ini belum tersedia. XceptionNet sendiri telah menjadi _baseline_ kuat dan banyak dipakai pada FaceForensics++ (Rössler et al., 2019) serta sebagai _backbone_ pada SpecXNet (Alam et al., 2025). Oleh karena itu, XceptionNet dipilih karena:
>
> - Efisien secara parameter namun tetap mampu mengekstraksi fitur spasial yang kompleks.
> - Terbukti mencapai akurasi tertinggi dibanding ResNet dan MesoNet pada FaceForensics++ (Rössler et al., 2019).
> - Telah menjadi _baseline_ standar dalam berbagai studi deteksi deepfake, sehingga memudahkan komparabilitas dengan penelitian sebelumnya.

**Juga perbaiki §2.18.3 (line 1007):** "...XceptionNet lebih tangguh ... dibandingkan dengan ResNet ~~maupun EfficientNet~~ (Alam et al., 2025)." → SpecXNet mengablasi ResNet & Xception, **bukan** EfficientNet, jadi buang "maupun EfficientNet".

**Tabel 2.8:** baris EfficientNet dihapus. Versi terkoreksi: **`documents/table/tabel_2_8_perbandingan_model_cnn.html`** (MesoNet, ResNet-50, XceptionNet saja).

_(Alternatif kalau mau lebih tegas: buang total penyebutan EfficientNet — tetapi menyebutnya singkat & jujur seperti di atas lebih baik karena menunjukkan kalian sudah mempertimbangkannya.)_

### 🔎 Verifikasi angka MesoNet & ResNet-50 di Tabel 2.8 (dicek ke PDF sumber, 2026-07-03)

Sumber PDF ada lokal: MesoNet (Afchar), FaceForensics++ (Rössler), Haq. Hasil cek:

**MesoNet — angka "85–90%" IMPRECISE.** Rössler et al. (2019) Tabel 1 (dilatih 4 metode) melaporkan MesoNet: **Raw 95,23% · HQ/c23 83,10% · LQ/c40 70,47%**. Jadi "85–90%" **bukan angka riil** mana pun. Yang benar (untuk c23 yang dipakai penelitian ini) = **83,10%**, atau rentang **83,10–95,23% (HQ–Raw)**. → sudah dikoreksi di tabel.

**ResNet-50 — angka "92–94% pada FaceForensics++" FABRIKATIF / salah sumber. 🔴**

1. **ResNet TIDAK ADA** di benchmark FF++ Rössler (Tabel 1 hanya: Steg.Features, Cozzolino, Bayar&Stamm, Rahmouni, MesoNet, XceptionNet). Jadi tak ada angka FF++ untuk ResNet dari Rössler.
2. **Haq (2021)** — sumber [3] yang dikutip — ternyata **memakai dataset Celeb-DF (V2), BUKAN FaceForensics++**, dengan preprocessing Gaussian+LBP, dan melaporkan **ResNet-50: AUC 0,87; akurasi 0,79 (79%)** (XceptionNet lebih baik dari itu). Jadi angka riilnya **79% di Celeb-DF**, bukan "92–94% di FF++".
3. Konsekuensi: klaim di **line 286** ("ResNet-50 ... di atas 90% pada FaceForensics++ [3, 5]") juga **tidak terdukung** — Haq = 79% di Celeb-DF, dan He et al. [5] = ImageNet.

**Aksi pada tabel:** baris **ResNet-50 dihapus** dari Tabel 2.8 (tak ada sumber FF++). Perbandingan XceptionNet vs ResNet-50 tetap sah **di prosa** dengan sumber yang benar: Haq (2021) menemukan XceptionNet > ResNet-50 pada **Celeb-DF** (ResNet-50 akurasi 79%). Tabel 2.8 kini hanya memuat **MesoNet & XceptionNet** (dua-duanya dari benchmark FF++ Rössler). File: `documents/table/tabel_2_8_perbandingan_model_cnn.html`.

**Bonus temuan:** parameter MesoNet "4M" pada tabel lama juga meragukan — MesoNet/MesoInception-4 hanya **~28 ribu parameter** (~0,03M), sengaja dibuat "mesoscopic". Kolom parameter sebaiknya dicek/di-drop; di tabel baru kolom parameter saya hilangkan agar tidak memuat angka tak-bersumber.

---

<a name="item-29"></a>

## Item 29 — Kalimat penutup "kombinasi FFT+XceptionNet ... menghasilkan sistem yang lebih akurat, efisien, dan lebih tangguh ..." (§2.18.3, docx line ~1008): terasa GARANSI

**Verdict: 🔴 BENAR, instingmu tepat. Kalimat ini berbunyi seperti JAMINAN keberhasilan, padahal (a) ini studi komparatif yang justru MENGUJI klaim itu, dan (b) hasil kalian sebagian besar NEGATIF (hybrid tak mengungguli spasial, freq ≈ tebakan acak). Kalimat ini BERTENTANGAN dengan BAB IV/V kalian sendiri.**

### Kenapa terasa "garansi"

Kalimat: "Integrasi keduanya **menghasilkan sistem deteksi deepfake yang tidak hanya lebih akurat dan efisien, tetapi juga lebih tangguh terhadap variasi data, tingkat kompresi, serta teknik manipulasi baru**, sebagaimana ditunjukkan pada penelitian-penelitian terkini [13, 16, 7, 17]."

- Bentuknya **deklaratif-pasti** ("menghasilkan sistem yang lebih tangguh ...") — bukan hipotesis. Pembaca menangkapnya sebagai **hasil yang dijamin**.
- Frasa "lebih tangguh terhadap variasi data, kompresi, teknik baru" persis **klaim yang kalian UJI** — dan hasilnya: hybrid **tidak** mengungguli spasial (AUC hybrid < spatial), cabang frekuensi **nyaris tebakan acak** (0,56–0,61), generalisasi lintas-dataset **tetap runtuh**. Jadi kalimat ini **dibantah oleh hasil kalian sendiri** (BAB IV/V + abstrak).
- "[13, 16, 7, 17]" = SpecXNet, FSBI, Rössler, Frequency-Domain Masking — itu **hasil positif paper LAIN**, dipinjam untuk menjamin pendekatan **kalian**. Sama polanya dengan [Item 10](#item-10)/[Item 27](#item-27).
- Ironi genre: kalau sudah "ditunjukkan menghasilkan sistem lebih tangguh", **kenapa diteliti?** Garansi di BAB II merusak justifikasi studi komparatif ([Item 24](#item-24)) dan menyiapkan **kontradiksi** dengan BAB IV/V.

### Perbaikan — ubah dari GARANSI jadi HIPOTESIS/RASIONAL (ready copy-paste, (Nama, Tahun))

> "Secara teoretis, kombinasi FFT dan XceptionNet bersifat saling melengkapi: FFT **berpotensi** mengekstraksi pola artefak yang tersembunyi di domain frekuensi seperti _spectral distortion_ dan _GAN fingerprints_, sedangkan XceptionNet kuat dalam mendeteksi anomali spasial pada struktur wajah dan tekstur visual. Sejumlah penelitian terkini **melaporkan** bahwa integrasi kedua domain **dapat** meningkatkan akurasi dan ketahanan deteksi (Alam et al., 2025; Hasanaath et al., 2023; Rössler et al., 2019; Luo & Wang, 2025), meskipun besarnya manfaat **bergantung pada representasi frekuensi, strategi fusi, dan karakteristik dataset**. Penelitian ini bertujuan **menguji secara empiris** sejauh mana kombinasi tersebut memberikan peningkatan, khususnya pada skenario lintas dataset — dan bukan mengasumsikannya sebagai hasil yang pasti."

Kunci perubahan: "menghasilkan" → "berpotensi/dapat"; "sebagaimana ditunjukkan" → "melaporkan"; tambah kaveat "bergantung pada ..."; tutup dengan "penelitian ini menguji ...".

### Cek pola serupa

Kalimat "garansi" di BAB II ini satu keluarga dengan [Item 10](#item-10), [Item 27](#item-27) (klaim over-optimistik yang bertabrakan dengan hasil negatif). Sebaiknya seluruh BAB II disisir untuk verba pasti ("menghasilkan", "membuktikan", "terbukti unggul") pada hal-hal yang justru **diuji** — ubah ke modal hipotesis ("berpotensi", "dilaporkan", "diharapkan").

### Jawaban siap-ucap kalau penguji menyorot

> "Betul, kalimat itu terlalu menjanjikan untuk sebuah studi komparatif. Yang tepat adalah membingkainya sebagai **hipotesis**: secara teoretis kedua domain saling melengkapi dan penelitian lain melaporkan potensinya, tetapi justru **itulah yang kami uji**. Temuan kami menunjukkan kontribusi domain frekuensi **terbatas** pada konfigurasi ini, sehingga kalimat di BAB II akan kami lunakkan agar konsisten dengan hasil di BAB IV dan V."

---

<a name="item-30"></a>

## Item 30 — §2.18.3 "Perbandingan Akurasi dan Ketahanan Metode FFT dan XceptionNet" ~75% RECAP dari §2.18.1 + §2.18.2

**Verdict: 🟡 Repetitif, instingmu tepat. §2.18.3 menulis ulang justifikasi FFT (sudah di §2.18.1) DAN justifikasi XceptionNet (sudah di §2.18.2), lalu menutup. Yang benar-benar baru hanya framing "saling melengkapi" + Tabel 2.9.**

### Peta duplikasi (dicek di .docx)

| §2.18.3 (isi)                                                   | Duplikat dari                       | Sumber & klaim yang diulang                                                                                                            |
| --------------------------------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Para "Pada domain frekuensi ..."                                | **§2.18.1** (Pemilihan FFT)         | Durall & Zhang [8,9] (artefak upsampling universal), FSBI [16] (robust lintas-dataset) —**sama persis**; hanya tambah Qian/Tan [11,12] |
| Para "Sementara itu, pada domain spasial ..." (yang kamu kutip) | **§2.18.2** (Pemilihan XceptionNet) | Afchar [4]/MesoNet, Rössler [7]/XceptionNet 96–99% > ResNet & MesoNet, Haq [3] —**sama persis**; hanya tambah Alam/SpecXNet [13]       |
| Para "Dengan demikian, kombinasi ..."                           | — (baru)                            | tapi ini kalimat**GARANSI** → lihat [Item 29](#item-29)                                                                                |
| Tabel 2.9 Ringkasan FFT vs XceptionNet                          | — (baru,**value asli**)             | perbandingan aspek-per-aspek                                                                                                           |

Jadi 2 dari 3 paragraf isi = **recap**. §2.18.1 membenarkan FFT, §2.18.2 membenarkan XceptionNet, lalu §2.18.3 **membenarkan keduanya lagi**.

### Apa yang seharusnya dilakukan §2.18.3

Judulnya "**Perbandingan** ... FFT dan XceptionNet" → tugasnya **membandingkan & menunjukkan komplementaritas**, bukan menurunkan ulang keunggulan masing-masing. Cukup: satu paragraf jembatan (rujuk balik §2.18.1/§2.18.2) + Tabel 2.9 + paragraf motivasi (versi hipotesis, bukan garansi).

### Rewrite lean (ready copy-paste, (Nama, Tahun); sudah gabung fix [Item 29](#item-29))

> Berdasarkan pembahasan pada sub-bab 2.18.1 dan 2.18.2, FFT dan XceptionNet unggul pada dimensi yang berbeda sehingga **berpotensi saling melengkapi**. XceptionNet unggul pada akurasi _in-dataset_ dan efisiensi parameter, tetapi cenderung bergantung pada artefak visual yang spesifik terhadap dataset pelatihan. Sebaliknya, representasi FFT menonjolkan artefak spektral yang bersifat algoritmik dan **dilaporkan** lebih stabil pada skenario lintas-dataset serta variasi kompresi, meskipun kehilangan informasi lokasi spasial. Ringkasan perbandingan kedua pendekatan disajikan pada Tabel 2.9.
>
> Secara teoretis, kombinasi keduanya **dapat** menghasilkan representasi yang lebih lengkap: FFT menangkap _spectral distortion_ dan _GAN fingerprints_ di domain frekuensi, sedangkan XceptionNet menangkap anomali spasial pada struktur wajah dan tekstur. Sejumlah penelitian terkini **melaporkan** potensi peningkatan akurasi dan ketahanan dari integrasi dua domain (Alam et al., 2025; Hasanaath et al., 2023; Luo & Wang, 2025), meskipun besarnya manfaat bergantung pada representasi frekuensi, strategi fusi, dan karakteristik dataset. **Penelitian ini bertujuan menguji secara empiris** sejauh mana kombinasi tersebut memberikan peningkatan, khususnya pada skenario lintas-dataset.

Hasil: buang ~2 paragraf recap, pertahankan Tabel 2.9, dan paragraf terakhir sudah dalam mode **hipotesis** (bukan garansi).

### Catatan lanjutan

- Klaim baru di Para spasial "SpecXNet [13] ... XceptionNet lebih tangguh terhadap variasi dataset ... dibandingkan ResNet" perlu hati-hati: itu **cross-dataset robustness untuk XceptionNet** — bertabrakan dengan temuan kalian (spasial justru **runtuh** lintas-dataset). Kalau paragraf ini dibuang (rewrite di atas), masalahnya ikut hilang.
- Pola "seksi perbandingan yang malah mengulang seksi sebelumnya" ini sekeluarga dengan [Item 13](#item-13) & [Item 17](#item-17). Saat menyisir BAB II, cek juga apakah §2.18.1/§2.18.2/§2.18.3 sebaiknya digabung/diringkas jadi struktur yang lebih rapi (FFT → XceptionNet → perbandingan-singkat).

---

<a name="item-31"></a>

## Item 31 — Audit DIAGRAM BAB III (`documents/media_v2/`)

**Verdict: 🔴 3 dari 5 diagram arsitektur perlu perbaikan. Yang paling penting: gambar 3.8 (FreqCNN) & 3.9 (Hybrid) memakai konfigurasi LAMA (base_channels=32 → 256-d), padahal teks/Tabel 3.7/config = base_channels=64 → 512-d.**

### Hasil cek per diagram (dibandingkan ke kode + config)

| Gambar                          | Status                     | Temuan                                                                                                                                                                                        |
| ------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **3.4** Flowchart preprocessing | 🔴→✅**sudah di-recreate** | Salah: grayscale jadi langkah utama, tanpa face-crop, tanpa high-pass/resize, rantai tunggal (bukan bercabang). Versi baru: artifact + Mermaid.                                               |
| **3.6** FreqBlock residual      | ✅**BENAR**                | Conv3×3→BN→ReLU + shortcut(1×1) → MaxPool, cocok kode.                                                                                                                                        |
| **3.3** Spectral band masking   | ✅**BENAR** (minor)        | Menunjukkan pita horizontal di-nol. (Minor: pita digambar agak lebar; hanya kasus horizontal, kode juga bisa vertikal.)                                                                       |
| **3.8** Arsitektur FreqCNN      | 🔴**SALAH**                | Pakai**base_channels=32 → 256-d, ~700K params**. Seharusnya **base_channels=64 → 512-d, ~4,2 juta** (sesuai `config.yaml`, Tabel 3.7, dan teks docx line 1358 "vektor fitur berdimensi 512"). |
| **3.9** Arsitektur Hybrid       | 🔴**SALAH**                | (a) cabang freq "256-d" & "Proj 256→256" →**512-d** & **512→256**; (b) Classifier "**Drop(0,3)**" → **Drop(0,5)** (kode hybrid pakai dropout 0,5, dua kali).                                  |

_(Gambar 3.2 frame real/fake, 3.5 FFT viz, 3.10 LR schedule, dan semua 4.x = plot/foto ter-generate dari data — bukan diagram konseptual, tidak bermasalah.)_

### Koreksi persis untuk 3.8 (FreqCNN)

Judul: "depth=5, **base_channels=64, ~4,2 juta params**". Blok:
`FreqBlock 1: 1→64` · `2: 64→128` · `3: 128→256` · `4: 256→512` · `5: 512→512` (dimensi spasial 112→56→28→14→7 sudah benar) · `GAP 512→1` · `FC 512→256 +ReLU` · `Drop(0,3)` · `FC 256→1` · Logit.

### Koreksi persis untuk 3.9 (Hybrid)

Cabang frekuensi: `FreqCNN → 512-d → Proj Linear+BN+ReLU 512→256 → 256`. Classifier: `Drop(0,5) · FC 512→128 · FC 128→1`. (Cabang spasial, Concat 512, SE Gate 512→512 sudah benar.)

### Kenapa ini penting

Kedua diagram itu **bertentangan dengan teks BAB III & Tabel 3.7 sendiri** (yang benar 512-d/base=64). Penguji yang membandingkan gambar vs tabel akan langsung melihat inkonsistensi 256 vs 512. Ini konsisten dengan dugaanmu ("masalah di grafik 3+").

> 🔧 Tidak ada skrip generator untuk diagram ini (hand-made). Bisa diperbaiki di tool asalnya (draw.io) dengan mengganti angka di atas, **atau** minta aku recreate 3.8 & 3.9 sebagai artifact (seperti flowchart 3.4).
>
> ✅ **Sudah dibuatkan** PNG terkoreksi + **.drawio editable** di `documents/media_v2/` (3.4 versi compact untuk Word, 3.8, 3.9). Generator: `scripts/make_architecture_figures.py` (PNG) & `scripts/make_architecture_drawio.py` (.drawio).

---

<a name="item-32"></a>

## Item 32 — §3.3.1 "Ekstraksi Frame" butir 4-6 + justifikasi 5 FPS / 50 frame

**Verdict: naming/label/manifest ✅ BENAR; tapi 2 klaim SALAH — "ekstraksi paralel" (sebenarnya SEKUENSIAL di mode face-crop) dan "FFPP n=1000 ~50.000" (n maksimum sebenarnya 750 → ~37.500).**

### Cek per butir (vs `scripts/extract_frames.py`)

| Klaim                                                                                   | Status                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Butir 4: nama berkas "frame_000000.jpg", "frame_000001.jpg" (JPEG)                      | ✅ BENAR —`f"frame_{saved:06d}.jpg"` (L98) + `cv2.imwrite`                                                                                                                                                                                                                            |
| Butir 5: label diinferensi dari nama direktori via pencocokan kata kunci terkonfigurasi | ✅ BENAR —`infer_label(p.parent, real_kw, fake_kw)` (L149), keyword dari `config.yaml`                                                                                                                                                                                                |
| Butir 6: manifes CSV kolom**video_id, label, frames_dir**                               | ✅ BENAR —`pd.DataFrame(rows, columns=["video_id","label","frames_dir"])` (L254)                                                                                                                                                                                                      |
| Butir 6:**"ekstraksi dilakukan secara paralel (multiprocessing pool)"**                 | 🔴**HANYA saat face-crop OFF.** Pada mode **face-crop (MTCNN)** — yang dipakai penelitian ini — ekstraksi **SEKUENSIAL**: L222-223 "MTCNN can't be pickled for multiprocessing" / "Extracting frames sequentially (face crop mode)". Jadi untuk run kalian, klaim paralel **keliru**. |

**Fix butir 6:** "Proses ekstraksi memanfaatkan _multiprocessing pool_ untuk paralelisasi pada mode tanpa _face-crop_; namun pada mode _face-crop_ dengan MTCNN yang digunakan pada penelitian ini, ekstraksi dilakukan secara **sekuensial** karena detektor MTCNN tidak dapat di-_pickle_."

### Gambar 3.3 "Pseudocode ekstraksi frame" — nomor OK, tapi ISI kurang face-crop

- ✅ **Penomoran benar**: di docx, Gambar 3.3 = Pseudocode (bukan band masking; nama file `gambar_3_3_spectral_band_masking.png` di media_v2 yang melenceng — itu Gambar 3.5 docx). Tak perlu renumber.
- ✅ Pseudocode **tidak** mengklaim paralel/multiprocessing → isu "paralel" murni di prosa, bukan di sini.
- 🔴 **Pseudocode kehilangan langkah face-crop MTCNN (margin 0,3) + fallback frame penuh** (kode `extract_frames.py` L86-96). Menggambarkan pipeline full-frame, padahal hasil BAB IV pakai frame ter-crop. Instance lain dari [[facecrop-mtcnn-doc-gap]].
- 🟡 Juga hilang: skip frame pertama hitam/gagal (`mean<3`), dan guard `max(round(...),1)`.
- **Pseudocode benar** (drop-in): tambahkan setelah cek `frame_idx mod interval == 0` → `bbox ← MTCNN(frame, margin 0,3); jika ada → crop; else → frame penuh`; plus skip hitam di awal dan penamaan `frame_{saved:06d}.jpg`.

### Justifikasi "5 FPS / 50 frame" (docx line 1129)

| Klaim                                           | Status                                                                                                                                                                                                                                                                                                  |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "5 FPS = satu sampel setiap 200ms"              | ✅ BENAR (1/5 s = 200 ms)                                                                                                                                                                                                                                                                               |
| "Pada 30 native FPS" (ambil tiap frame ke-6)    | ✅ konteks benar                                                                                                                                                                                                                                                                                        |
| **"membatasi total frame FFPP n=1000 ~50.000"** | 🔴**SALAH.** Tabel 3.3 kalian sendiri menyatakan FFPP = **100, 250, 500, 750** (bukan ...1000). Semua BAB IV headline **n=750**, dan **tidak ada tabel hasil n1000** (maks di disk = n750). Jadi n=1000 adalah sisa skema tier LAMA (100/300/600/1000). Yang benar: **n=750 → 750×50 = ~37.500 frame**. |

**Fix:** "Batas 50 frame/video membatasi total frame FaceForensics++ pada ukuran sampel terbesar (**n=750**) menjadi sekitar **37.500** frame, ukuran yang dapat dilatih pada satu sesi Colab Pro tanpa mengorbankan keberagaman video."

> ⚠️ Angka "n=1000" ini menandakan ada **sisa dari skema tier lama** yang mungkin masih muncul di tempat lain. Saat menyisir BAB III, cek konsistensi: semua rujukan tier FFPP harus **100/250/500/750**, bukan 300/600/1000.

---

<a name="item-33"></a>

## Item 33 — "Face cropping meningkatkan performa spasial secara substansial pada FaceForensics++" — apakah ada referensi?

**Verdict: ✅ ADA — Rössler et al. (2019), paper FaceForensics++ itu sendiri.**

Tabel 1 Rössler et al. membandingkan XceptionNet (model spasial) dengan vs tanpa face-crop:

| XceptionNet             | Raw    | HQ (c23)   | LQ (c40) |
| ----------------------- | ------ | ---------- | -------- |
| Full Image (tanpa crop) | 82,01% | **74,78%** | 70,52%   |
| Face-cropped            | 99,26% | **95,73%** | 81,00%   |

Pada c23 (kompresi yang dipakai): **74,78% → 95,73%**, lompatan **~21 poin** → persis klaim "substansial". Rössler et al. menulis face extraction _"improves the overall performance of a forgery detector in comparison to a naïve approach that uses the whole image."_ Sitasi = **(Rössler et al., 2019)** [7].

⚠️ Kata **"Secara empiris"** menyiratkan temuan sendiri, padahal matriks eksperimen kalian **tidak memuat ablasi crop-vs-no-crop**. Rekomendasi: atribusikan ke literatur — _"Sebagaimana ditunjukkan Rössler et al. (2019), face cropping meningkatkan performa model spasial secara substansial pada FaceForensics++ (74,78% → 95,73% pada c23)."_ Jangan biarkan "Secara empiris" berdiri tanpa sitasi/ablasi.

---

<a name="item-34"></a>

## Item 34 — Classifier head hybrid (pasca SE gating, ĥ_fused ∈ ℝ⁵¹²)

**Verdict: ✅ BENAR — struktur cocok persis kode `src/models/hybrid_fusion.py`.**

```python
fused_dim = PROJ_DIM * 2            # = 512  (L46)
self.se_gate = SEGate(fused_dim)   # 512 → 512, reduction 4  (L47)
self.classifier = nn.Sequential(   # (L48-54)
    nn.Dropout(0.5),               # ✅
    nn.Linear(fused_dim, 128),     # ✅ 512 → 128
    nn.ReLU(inplace=True),         # ✅
    nn.Dropout(0.5),               # ✅
    nn.Linear(128, 1),             # ✅ 128 → 1 (logit)
)
# forward: fused = cat([spatial(256), freq(256)]) → se_gate → classifier   (L64-66)
```

| Klaim                               | Status                                           |
| ----------------------------------- | ------------------------------------------------ |
| ĥ_fused ∈ ℝ⁵¹² pasca SE gating      | ✅`fused_dim = 256×2 = 512`; SEGate keluar 512-d |
| Dropout(0,5)                        | ✅                                               |
| Linear(512 → 128) "reduksi dimensi" | ✅                                               |
| ReLU                                | ✅                                               |
| Dropout(0,5)                        | ✅                                               |
| Linear(128 → 1) "logit biner"       | ✅                                               |

🟡 **Satu catatan bahasa (bukan salah kode):** kalimat menyebut dropout 0,5 sebagai **"moderat ... agar tidak menghilangkan terlalu banyak sinyal"**. Secara teknis p=0,5 me-nol-kan **50%** aktivasi — itu dropout **kuat/standar** (nilai default klasik Srivastava et al., 2014), bukan "moderat". Penguji bisa mengait: _"0,5 kok disebut moderat, padahal buang setengah sinyal?"_ Saran aman: _"Dropout(0,5), nilai standar untuk regularisasi kuat pada kepala klasifikasi (Srivastava et al., 2014)"_ — atau hapus frasa "moderat / tidak menghilangkan terlalu banyak sinyal".

---

<a name="item-35"></a>

## Item 35 — "Desain tiga varian ... menjawab RM pertama & kedua, yaitu bagaimana membangun detektor lebih akurat ..." (docx line 1397)

**Verdict: 🔴 MISLEADING — menyalahnyatakan rumusan masalah + bertabrakan dengan temuan negatif. (Deskripsi model di kalimat pertama BENAR; hanya kalimat kedua yang bermasalah.)**

### RM asli (BAB I, docx 293-296) — semuanya analitis/komparatif

|     | Rumusan masalah asli                                                              |
| --- | --------------------------------------------------------------------------------- |
| RM1 | Sejauh mana detektor spasial murni**mengalami penurunan** performa cross-dataset? |
| RM2 | Sejauh mana**FFT memperkecil penurunan** tersebut?                                |
| RM3 | Seberapa besar**kontribusi** komponen (spasial vs frekuensi)?                     |

**Tidak ada RM "membangun detektor yang lebih akurat".**

### Tiga cacat kalimat

1. 🔴 **RM1 salah dinyatakan** sebagai "bagaimana membangun detektor lebih akurat". Itu **sisa framing judul lama** ("Metode **Peningkatan** Deteksi Deepfake" → sudah retitle "**Studi Komparatif**"). Grep: framing "lebih akurat" HANYA muncul di line 1397 — yatim & bertentangan dgn seluruh narasi.
2. 🔴 **Salah nomor:** "kontribusi masing-masing jenis fitur" = **RM3**, bukan RM2 (RM2 = FFT memperkecil penurunan).
3. 🔴 **Bertabrakan dgn hasil sendiri:** kesimpulan = _hybrid TIDAK mengungguli baseline spasial; H0 tidak ditolak_. Klaim "menjawab bagaimana membangun detektor lebih akurat" → penguji menodong _"terjawab tidak? kan tidak lebih akurat."_ Temuan negatif itu SAH untuk studi komparatif; framing "lebih akurat" yang membuatnya tampak gagal.

### Fix (kalimat kedua saja) — TANPA menyebut hasil (ini BAB III; hasil ranah BAB IV)

> "Desain tiga varian ini menjadi basis _ablation study_ yang menjawab ketiga rumusan masalah: model spasial-saja mengukur penurunan performa domain spasial lintas dataset (RM1), perbandingan hybrid terhadap spasial menguji apakah penambahan domain frekuensi memperkecil penurunan tersebut (RM2), dan kontras spasial vs frekuensi vs hybrid mengisolasi kontribusi masing-masing domain (RM3). Sesuai sifat komparatifnya, penelitian ini diarahkan untuk **mengukur kontribusi** domain frekuensi terhadap generalisasi, bukan semata membangun detektor dengan akurasi tertinggi."

> ⚠️ **Koreksi atas saran awal (2026-07-07):** versi fix pertamaku sempat menambahkan klausa _"...sehingga temuan bahwa hybrid tidak mengungguli baseline spasial tetap sah"_ — itu **KELIRU** karena menyeret HASIL (BAB IV) ke BAB III. Passage line 1397 ada di **bab metodologi**, jadi fix harus berhenti pada framing tujuan/sifat komparatif; **jangan menyebut outcome** ("hybrid tidak mengungguli"). Statemen sifat-studi (komparatif, mengukur kontribusi) = sah di BAB III; statemen hasil = tidak.

⚠️ **Pola berulang:** cek seluruh BAB I & III untuk sisa framing "peningkatan / lebih akurat / lebih unggul" dari judul lama — harus konsisten dengan judul komparatif. (Konsistensi dengan temuan negatif = urusan BAB IV/V, bukan di sini.)

---

<a name="item-36"></a>

## Item 36 — Transfer learning & backbone freezing (spasial + hybrid)

**Verdict: ✅ BENAR — cocok persis `scripts/train.py`.** Salah satu paragraf paling akurat.

| Klaim                                                        | Kode                                                    | Status |
| ------------------------------------------------------------ | ------------------------------------------------------- | ------ |
| Freeze backbone 3 epoch pertama                              | `FREEZE_EPOCHS = 3` (L26); epoch 1-3                    | ✅     |
| Spasial: hanya head diperbarui                               | freeze semua kecuali`head.fc`/`fc` (L236-239)           | ✅     |
| Hybrid: FreqCNN + proyeksi + SE gate + classifier diperbarui | freeze**hanya** `model.spatial` (L242-243)              | ✅     |
| Unfreeze pada**epoch ke-4**                                  | `if epoch == FREEZE_EPOCHS + 1` (L274), epoch 1-indexed | ✅     |
| Fine-tuning menyeluruh                                       | `p.requires_grad = True` (L277/281)                     | ✅     |

🟡 **Catatan halus (bukan salah kode):**

1. **"pemanggilan `requires_grad(True)`"** → kode meng-**set atribut** `p.requires_grad = True`, bukan memanggil fungsi. `requires_grad(True)` sbg pemanggilan tidak ada di PyTorch. Rapikan: _"menyetel `requires_grad = True`"_ / method `requires_grad_(True)`.
2. **"catastrophic forgetting"** → istilah ketatnya = lupa tugas lama (continual learning); di sini lebih tepat "gradien head acak merusak bobot pretrained". Longgar tapi umum; penguji ML bisa koreksi.
3. **"proyeksi"** = **dua** lapisan (spatial_proj 2048→256 + freq_proj 512→256), keduanya trainable saat freeze. `spatial_proj` belajar memproyeksikan fitur backbone yang beku — konsisten.

---

<a name="item-37"></a>

## Item 37 — Loss BCEWithLogitsLoss + pos_weight + label smoothing (BAB II teori vs BAB III metode)

**Verdict: 🟡 Konten BENAR SEMUA, tapi BAB III REPETITIF (mengulang verbatim BAB II) + satu kontradiksi.**

### Konten ✅ (cocok kode)

| Klaim                                        | Kode                                                 | Status          |
| -------------------------------------------- | ---------------------------------------------------- | --------------- |
| `pos_weight = n_neg/n_pos` **betul dipakai** | train.py L184-185`BCEWithLogitsLoss(pos_weight=...)` | ✅              |
| Label smoothing`y'=y(1-α)+α·0,5`             | L112`targets*(1-ls)+ls*0.5`                          | ✅ cocok persis |
| α = 0,05 konfigurasi akhir                   | config.yaml L17                                      | ✅              |
| Seimbang → pos_weight = 1                    | benar                                                | ✅              |

### Repetisi 🟡

1. 🔴 BAB III **"Penyeimbangan Kelas (pos_weight)"** ≈ **verbatim** BAB II rumus 2.31 ("dikalikan pada sampel positif... seimbang → pos_weight=1 → BCE standar").
2. 🟡 BAB III **"Label Smoothing"** kalimat pertama (α=0,02 → 0,01/0,99) = **duplikat** BAB II 2.32; hanya "α=0,05 akhir" yang baru.
3. ⚠️ **Kontradiksi**: BAB III menulis "kedua rumus **telah diuraikan** pada 2.31 & 2.32" lalu **menguraikannya lagi**.

### Unik & pertahankan

"Contoh Perhitungan BCEWithLogitsLoss" (z=2,5, y=1, α=0,05, wp=1) — nilai tambah BAB III, tidak ada di BAB II.

### Fix (konkret — ganti seluruh subbab loss di BAB III)

Prinsip: BAB II = teori+rumus; BAB III = **nilai dipakai + apakah aktif + contoh**, jangan derive ulang.

> **Fungsi Loss dan Penyesuaiannya**
> Fungsi loss yang digunakan adalah _BCEWithLogitsLoss_ (persamaan 2.30), dengan dua penyesuaian dari teori pada Subbab 2.x sesuai konfigurasi eksperimen:
>
> 1. **Penyeimbangan kelas (pos_weight).** Bobot `pos_weight = n_neg/n_pos` (persamaan 2.31) dihitung otomatis dari komposisi data latih. Karena pengambilan sampel dirancang **seimbang 50:50**, nilai `pos_weight ≈ 1` sehingga loss efektif setara BCEWithLogitsLoss standar; mekanisme tetap disiapkan agar robust bila komposisi kelas bergeser.
> 2. **Label smoothing.** Diaktifkan dengan **α = 0,05** (persamaan 2.32) sebagai regularisasi ringan untuk mencegah _overconfidence_ pada dataset kecil (mulai n = 100).
>
> **Contoh perhitungan.** Untuk satu sampel: z = 2,5, y = 1 (_fake_), `pos_weight` = 1, α = 0,05:
>
> - y' = 1·(1 − 0,05) + 0,05·0,5 = **0,975**
> - σ(2,5) = 1/(1 + e^(−2,5)) ≈ **0,9241**
> - L = −[0,975·ln(0,9241) + 0,025·ln(0,0759)] ≈ **0,141**

**Yang dihapus/diubah:** (a) hapus subbab yang menurunkan ulang pos_weight & label smoothing (verbatim BAB II) + kalimat kontradiktif "telah diuraikan pada 2.31/2.32"; (b) tambah **pos_weight ≈ 1** (karena 50:50); (c) hapus contoh "α=0,02 → 0,01/0,99" (duplikat 2.32 + nilai lama); (d) pertahankan & lengkapi **Contoh Perhitungan** (satu-satunya bagian milik BAB III).

**Bonus BAB II:** contoh label smoothing masih pakai α=0,02 (sisa nilai lama) — selaraskan ke **α=0,05** (0→0,025, 1→0,975) agar konsisten dgn config & BAB III.

---

<a name="item-38"></a>

## Item 38 — §3.5.2–3.5.8 (optimizer/LR/gradient/AMP/early stop)

**Verdict: ✅ SEMUA BENAR — cocok `train.py` + `config.yaml`.** Salah satu bagian paling akurat.

| Klaim                                                                                               | Kode                                     | Status    |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------- | --------- |
| Backbone LR 10× lebih rendah                                                                        | `backbone_lr = base_lr/10` = 2e-5 (L191) | ✅        |
| FreqCNN (hybrid) LR 25% base                                                                        | `base_lr*0.25` = 5e-5 (L~218)            | ✅        |
| Head LR = base 2e-4                                                                                 | (L219)                                   | ✅        |
| Warmup LinearLR(0.1→1.0, 3ep) + CosineAnnealingLR(T_max=max(ep−3,1), eta_min=1e-6) via SequentialLR | L257-266                                 | ✅ persis |
| AdamW, base_lr=2e-4, wd=1e-4                                                                        | config L12-13                            | ✅        |
| accum_steps=2, batch 16 → efektif 32                                                                | config L10,16 (semua model)              | ✅        |
| Gradient clip max*norm=5.0, unscale*() sebelum clip                                                 | L116-117                                 | ✅        |
| AMP + TF32 Ampere+                                                                                  | ✅                                       | ✅        |
| Early stopping AUC, patience 12, max 30                                                             | config L14-15                            | ✅        |

Tidak ada kesalahan faktual. (Angka rumus kosong di extraction karena objek equation, tapi logika cocok.)

---

<a name="item-39"></a>

## Item 39 — §3.6 vs §3.6.1 repetitif + Tabel 3.12 error

**Verdict: 🔴 Paragraf redundan + 2 kesalahan di Tabel 3.12.**

- §3.6 & §3.6.1 **paragraf pertama nyaris identik** ("eksperimen faktorial, tiga faktor: model/dataset/ukuran sampel, seed, reliabel"). Fix: §3.6 = tujuan singkat; §3.6.1 **langsung Tabel 3.12** tanpa mengulang framing faktorial.
- | **Tabel 3.12 errors** (vs `run_all.py`, `MODELS_CORE=[spatial,freq,hybrid]`): | Masalah                                                                                               | Betul |
  | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----- |
  | 🔴 "Ukuran sampel**CDF**"                                                     | berlaku**kedua** dataset (Tabel 3.3: FFPP & CDF sama 100/250/500/750) → "Ukuran sampel (per dataset)" |
  | 🔴 "Total pelatihan: [kosong]" / "Total evaluasi: [kosong]"                   | **72 run** (3×2×4×3); **144 evaluasi** (72 × in+cross)                                                |

---

<a name="item-40"></a>

## Item 40 — Paragraf Δ (generalization drop) repetitif dgn BAB I/II

**Verdict: 🟡 Mildly repetitif.** BAB II (docx 940) sudah mendefinisikan Δ = selisih F1 in-dataset vs cross-dataset (rumus 2.40). BAB III (docx 1616):

- 🟡 Kalimat 1 (motivasi "cross-dataset penting krn skenario nyata / metode belum dilihat") = ulang **BAB I latar belakang** (docx 290) + BAB II.
- 🟡 Kalimat 3 ("Δ besar → generalisasi buruk") = interpretasi berdempet dgn BAB II 940 (dan ranah BAB IV).
- ✅ Kalimat 2 ("rumus di 2.40") sudah benar.

**Fix:** _"Selain in-dataset, setiap model dievaluasi cross-dataset (FFPP↔CDF); selisih performa dikuantifikasi dengan generalization drop (Δ, persamaan 2.40)."_ Buang motivasi + interpretasi.

> 🔁 **Pola berulang (Item 37, 39, 40):** BAB III sering **re-motivasi + re-derive** konsep BAB I/II lalu tetap bilang "sudah dijelaskan di [rumus]". Aturan bersih: BAB III = **nilai/konfigurasi + apa yang dilakukan + rujuk balik**; tanpa re-motivasi/re-derive.

---

# 🔁 STATUS RE-CHECK MENYELURUH BAB I-III (2026-07-07)

Re-extract docx terkini (`CUR.txt`, 2613 paragraf), cek Item 1-40.

## ✅ SUDAH DITERAPKAN di docx

Item **23** (AUC di daftar metrik, L1009) · **27** (Pemilihan Metode "diuji empiris" + sitasi, L1145) · **28** (EfficientNet dihapus) · **29** (garansi dilunakkan "diharapkan…robust", L460) · **32** (ekstraksi sekuensial caveat MTCNN L1336; n=1000/50.000 hilang) · **33** (sitasi Rös19 face-crop L1348) · **34** ("moderat" dihapus) · **35** (RM → "basis ablation study", L1721, tanpa "lebih akurat"/tanpa hasil) · **36** (`requires_grad_(True)` L1798) · **39** (§3.6.1 dup dihapus; "Ukuran sampel (per dataset)"; total 72/144, L1945-56) · **40** (Δ para trim, L1967) · HQ/LQ=c23/c40 (L789-791) · Contoh loss L=0,1415 **arithmetic BENAR** (#3.15-3.17).

## ⏳ MASIH PERLU

- **Item 37 (parsial):** pos_weight sudah OK ("≈1"), tapi **bullet Label smoothing masih ulang α=0,02→0,01/0,99** (L1837) → hapus, sisakan α=0,05. BAB II L1006 masih "mis. 0,02" (opsional).
- **BARU §3.5.5 AdamW:** L1852 mengulang penjelasan decoupled weight decay dari §2.15.2/2.15.3 → ringkas + rujuk balik.
- **Item 30:** §2.18.3 masih ada (L1191) — verifikasi sudah dipangkas dari recap 2.18.1+2.18.2.

## 🟡 TYPO BARU

- L322 "Aristektur" → **Arsitektur** (caption Gambar 3.10). · L1721 "dieksploitasi **adalah** model" → ":"/"yaitu". · L1856 "scaler.unscale()" → **unscale\_()**. · L1336 "denganMTCNN" → "dengan MTCNN".

## 🎯 early_fusion

Masih ada (L508-513, 715) tapi **tidak lagi misleading** — diframing "alternatif konseptual, tidak dievaluasi" (L513) + L715 kontras "bukan kanal tambahan". Klaim lama "hybrid=kanal keempat" HILANG. Boleh tetap (literatur) atau dihapus utk ketat.

## 📁 Nomor gambar (bukan error docx)

Nama file media_v2 ≠ nomor docx: `gambar_3_6_freqblock`=**Gambar 3.9**; `gambar_3_9_hybrid`=**Gambar 3.10**; `gambar_3_4_flowchart`=**Gambar 3.1** (Flowchart Utama). `gambar_3_8_freqcnn`=3.8 ✅. `gambar_3_3_pseudocode`=3.3 ✅.

---

# 🔬 AUDIT BAB IV–V + TYPO SWEEP (2026-07-07, 3 auditor paralel)

Detail + fix CARI/GANTI: **`REVISI_BAB_IV_V_FIX_Audit_2026-07-07.md`**.

- **BAB IV (angka):** ✅ BERSIH — Tabel 4.1–4.5 cocok persis CSV `outputs/`; semua Δ/AUC aritmetik benar.
- **Konsistensi antar-bab:** ✅ Abstract↔IV↔V↔RM/H0 konsisten; H0 tidak ditolak; tak ada over-claim di hasil/kesimpulan.
- **🔴 WAJIB:** (A) Tabel 3.11 label smoothing "Dinonaktifkan untuk dataset kecil" **SALAH** (config=0,05, prosa 1836 = diaktifkan) → "Diaktifkan α=0,05". (B) "AUC 0,56–0,68" → batas bawah **0,55** (min 0,555); di BAB IV L2253 + Abstrak.
- **Typo jelas:** spasi heading (BAB IVHASIL/BAB VPENUTUP), titik ganda (2361/1832/1231/1226), berdukungan/PyTroch/dibahasa/Alam el at/ke-mmm/resiko, dibawah-diatas (5×), judul Daftar Pustaka (Assesment/Deteciton/Enchanced/Detectionin/Explainthe/in-CML).
- **Soft:** klaim hybrid-F1 unggul n=250/500 (L2364) BENAR tapi tak ditabelkan → cek Gambar 4.9; scope Tabel 4.4 vs Gambar 4.9; dimana→di mana; fasa→fase; nama DP (Cozzolino/Giudice/Loshchilov/Zhao); BAB II L1167 klaim FFT datar; tahun lahir Samuel L2581 hilang.

---

<a name="item-41"></a>

## Item 41 — Tabel 4.1 (BAB IV) = Tabel 3.12 (BAB III) duplikat

**Verdict: 🔴 Redundan — matriks eksperimen yang sama muncul dua kali.** Isi identik (Model 3 · Dataset 2 · Ukuran sampel 4 · Seed 3 · Evaluasi 2); beda hanya kosmetik (header "Dimensi"/"Faktor", urutan baris).

**Fix:** hapus **Tabel 4.1**, ganti rujukan ke Tabel 3.12. Alasan: (1) matriks = desain → rumah di BAB III; (2) BAB IV sudah **merujuk** Tabel 3.11/3.16/3.17 tanpa menyalin — matriks harus diperlakukan sama; (3) risiko drift bila dua tabel terpisah; (4) **3.12 lebih benar** — 4.1 menaruh "Skenario evaluasi=2" sbg faktor matriks (menyesatkan; arah eval bukan faktor pelatihan), sedangkan 3.12 memisahkan 72 run vs 144 eval. **Pertahankan 3.12**, buang 4.1.

### §4.1.1 versi bersih (drop-in, Tabel 4.1 dihapus)

> **4.1.1 Lingkungan dan Konfigurasi Eksperimen**
> Seluruh eksperimen dijalankan pada lingkungan komputasi berbasis GPU dengan PyTorch dan _timm_ untuk backbone XceptionNet; spesifikasi perangkat dirinci pada Tabel 3.16 dan 3.17. Konfigurasi hyperparameter konsisten untuk seluruh model (Tabel 3.11): optimizer AdamW (lr dasar 2×10⁻⁴), gradient accumulation dua langkah (batch efektif 32), early stopping AUC validasi patience 12, dan pembekuan backbone tiga epoch pertama. Pemilihan model terbaik berdasarkan AUC validasi tertinggi.
> Evaluasi mengikuti **matriks eksperimen penuh pada §3.6.1 (Tabel 3.12)**, yaitu 3 model (spasial, frekuensi, hybrid) × 2 dataset (FFPP, CDF) × 4 ukuran sampel (100, 250, 500, 750) × 3 seed, menghasilkan **72 pelatihan dan 144 evaluasi**. Pengujian dua arah: in-dataset (FFPP→FFPP, CDF→CDF) dan cross-dataset (FFPP→CDF, CDF→FFPP), dengan metrik accuracy, precision, recall, F1-score, dan AUC. Khusus n=100 (~15 video, rentan noise pencuplikan), analisis utama bertumpu pada n=250, n=500, n=750, dengan n=750 representasi utama.

**Berubah:** ❌ hapus Tabel 4.1 + kalimat "Rincian…Tabel 4.1" · 🔄 ganti jadi 1 kalimat rujuk Tabel 3.12 (72/144 inline) · ✅ tetap: lingkungan/hyperparameter (rujuk 3.11/3.16/3.17), 2-arah eval, caveat n=100.

⚠️ **Konsekuensi renumber:** hapus Tabel 4.1 → Tabel 4.2→4.1, 4.3→4.2, dst. **Ctrl+A→F9** untuk refresh field (SEQ/REF); cek nomor tabel yang diketik manual (tidak auto-update).
