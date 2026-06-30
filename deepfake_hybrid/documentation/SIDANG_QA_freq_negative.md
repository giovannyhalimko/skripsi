# Sidang Q&A — Hasil Negatif Frekuensi & Hybrid

**Pertanyaan penguji (antisipasi):**
> Jika hybrid tak pernah menang dan frekuensi nyaris acak, apa kontribusi ilmiah riil
> selain "hasil negatif," dan bagaimana memastikan ini bukan sekadar studi yang
> *under-powered* pada sisi frekuensi?

**Sumber angka:** `outputs/gpu_pull_2026-06-19/` (3-seed mean), tier andal n=500/750.

---

## Jawaban lisan 60 detik (hafalkan ini)

> "Hasil negatif saya bukan kegagalan, melainkan falsifikasi terkontrol atas asumsi
> umum di literatur bahwa artefak domain-frekuensi adalah cue yang kuat dan general.
> Pada rezim realistis — frame video terkompresi, face-cropped, data terbatas,
> lintas-dataset — cue itu nyaris hilang dan fusi justru mengencerkan sinyal spatial
> yang kuat. Kontribusinya tiga: (1) panduan desain konkret untuk deteksi deepfake
> low-resource — backbone spatial pretrained sendirian paling kuat sekaligus paling
> hemat parameter; (2) temuan diagnostik soal kalibrasi threshold pada transfer
> lintas-dataset; (3) bukti bahwa bottleneck-nya kandungan informasi input FFT, bukan
> model. Dan saya tidak menyimpulkan dari satu eksperimen: saya menyingkirkan tiga
> sumber under-power — data, kapasitas model, dan preprocessing — dan kesimpulan
> near-chance bertahan di ketiganya. Itulah yang mengubah 'gagal' jadi 'temuan'."

---

## Apa yang sebenarnya diuji penguji

Dua mata pisau:
1. "Negative result bukan kontribusi" → apakah kamu paham nilai ilmiah hasil yang mematahkan asumsi.
2. "Mungkin frekuensinya cuma kurang data/tuning" → **rigor metodologis**: apakah confound sudah disingkirkan sebelum menyimpulkan "frekuensi lemah."

Bagian (2) lebih penting — kalau terbukti *bukan* under-powered, hasil negatif naik kelas jadi temuan.

---

## Bagian A — Kontribusi ilmiah riil

**1. Falsifikasi terkontrol atas asumsi literatur.** Literatur luas mengklaim artefak
spektral (spectral fingerprint GAN, checkerboard upsampling) adalah cue kuat & general.
Studi ini menunjukkan pada frame video terkompresi + face-crop + data terbatas +
lintas-dataset, cue itu nyaris hilang dan fusi tidak menolong. Mematahkan asumsi yang
diterima luas, dengan protokol terkontrol, adalah kontribusi ilmiah klasik.

**2. Diagnostik, bukan cuma "angka jelek."**
- Cabang frekuensi near-chance: AUC in-dataset hanya **0.56** (n750, FFPP & CDF) vs
  spatial **0.78 / 0.97**.
- Gerbang SE pada hybrid mengencerkan sinyal spatial kuat dengan freq near-chance →
  menjelaskan kenapa fusi *menurunkan* performa (hybrid FFPP n750 AUC 0.64 < spatial 0.78).
- Analisis recall-collapse / kalibrasi threshold (CDF→FFPP): recall ambruk ke 0.07
  ternyata artefak threshold, bukan hilangnya kemampuan ranking (AUC 0.61, precision 0.92).
  Lihat `RECALL_COLLAPSE_ANALYSIS.md`.

**3. Kontribusi praktis actionable.** Untuk deteksi deepfake low-resource (data kecil,
berbasis frame): backbone spatial ImageNet-pretrained sendirian = pilihan terkuat *dan*
paling hemat parameter. Menambah cabang FFT menambah parameter sambil menurunkan akurasi.

**4. Terikat-kondisi & punya mekanisme.** Kompresi video (H.264/JPEG) + resize face-crop
menghancurkan komponen frekuensi-tinggi tempat artefak sintesis berada. Hasil negatif
terhubung ke mekanisme yang bisa dipertanggungjawabkan, bukan kebetulan.

---

## Bagian B — Bukti ini BUKAN under-powered (inti pertahanan)

Setiap penjelasan "kurang power" disingkirkan satu per satu:

**1. Sweep ukuran sampel = analisis power langsung.** Kalau freq kelaparan data, AUC naik
terus dengan n. Faktanya plateau ~0.56:

| freq AUC (in-dataset) | n250 | n500 | n750 |
|---|---|---|---|
| FFPP | 0.47 | 0.54 | 0.56 |
| CDF  | 0.50 | 0.55 | 0.56 |

Naik 3× data (250→750) hanya menggeser ~0.06 lalu mentok → lemah secara substansi.
*(Tier n100 noisy — andalkan tren 250→750.)*

**2. Kontrol arsitektur (FreqCNN vs ResNet18).** FreqCNN custom diganti ResNet18 standar —
scratch **dan** ImageNet-pretrained — dengan **2.6× lebih banyak parameter** (11.2M vs 4.2M).
Semua arm tetap di **AUC 0.51–0.63**. Backbone lebih besar/pretrained pun tak mengangkat
input FFT keluar near-chance → bottleneck = kandungan informasi input FFT, bukan kapasitas
model. Mematahkan "jaringan frekuensimu cuma terlalu kecil/jelek." Lihat `FREQ_BENCHMARK_RESULTS.md`.
> Catatan jujur: arm pretrained sebenarnya 2-2 split (ResNet18 menang di CDF-in & FFPP→CDF).
> Klaim aman = arm **scratch** (FreqCNN menang 4/4 pada kondisi terkontrol). Jangan klaim
> pretrained sebagai kemenangan FreqCNN.

**3. Multi-seed (3 seed) + std dilaporkan.** Di tier andal, std AUC freq kecil (~0.007–0.015).
Near-chance itu stabil, bukan run sial.

**4. Anggaran latih identik & no-leakage.** Freq dilatih dengan optimizer/schedule/epoch/
early-stopping (val AUC) sama persis dengan spatial; split by-video-ID cegah kebocoran.
Apples-to-apples.

**5. Preprocessing diverifikasi.** Statistik normalisasi FFT dihitung ulang (mean≈5.78,
std≈1.28); fallback lama std=3.0 ~2.3× terlalu besar. Input freq tidak lumpuh karena salah
normalisasi — sudah dicek & diperbaiki.

---

## Yang harus DIAKUI (mendisarm penguji)

- Klaim dibatasi pada satu keluarga desain fusi (SE late-fusion + early-fusion 4-channel)
  dan satu input frekuensi (FFT log-magnitude global). Tidak mengklaim *tidak ada* metode
  frekuensi yang bisa membantu — klaim: cabang & fusi *ini* tidak, di rezim *ini*.
- Frekuensi mungkin berguna pada citra full-frame/tak-terkompresi atau manipulasi spesifik;
  scope = frame video terkompresi yang sudah di-crop wajah.
- n dibatasi anggaran komputasi; dimitigasi dengan sweep ukuran sampel, bukan satu n tunggal.
