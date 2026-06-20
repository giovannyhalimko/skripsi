# ACTION PLAN — 4 Commit Baru (ROC/CM + Freq Benchmark) vs WORD docx

**Tanggal:** 2026-06-20
**Disusun setelah:** cek 4 commit baru di atas `730cc04`, + `f11a8fd` (judul/Kata Pengantar), vs file WORD live.
**File WORD yang dianalisis:** `OneDrive/.../STUDI KOMPARATIF KINERJA DETEKSI DEEPFAKE BERBASIS ARSITEKTUR HYBRID XCEPTIONNET-FFT TERHADAP MODEL DOMAIN TUNGGAL.docx`
**Dokumen induk (jangan diabaikan):** `documents/HANDOFF_Finalisasi_BAB_II-IV_2026-06-17.md` — action plan ini adalah **lanjutan** dari §2A/§2C/§3/§7 handoff itu, sekarang aset ROC/CM-nya **sudah ada**.
**Aturan tim yang berlaku:** *"JANGAN ganti angka hasil tanpa kesepakatan tim. Hasil yang di-settle = `d28efae` → `results_vast_20260609/` (3 seed)."*

---

## 0. RINGKASAN EKSEKUTIF (baca ini dulu)

1. **4 commit baru = mayoritas aset gambar yang selama ini kurang.** Commit `a5cb3ba` menambah **ROC + confusion matrix untuk SEMUA eksperimen** (161 file). Ini melunasi tugas §2A handoff (Gambar 4.4, 4.6, 4.9). Tiga commit lain (`ecfbc4d`, `3ea7984`, `ad6d41d`) menambah **benchmark FreqCNN vs ResNet18** — konten **opsional baru** untuk pertahanan sidang, bukan perbaikan docx.
2. **⚠️ MASALAH UTAMA — model di-retrain.** ROC/CM di `a5cb3ba` berasal dari **run pelatihan BARU (2026-06-20, seed 0 saja)**, BUKAN dari run 2026-06-09 yang jadi dasar semua **tabel** di skripsi. AUC-nya **beda tipis** (lihat §2). Kalau gambar baru ini langsung ditempel, **angka AUC di legenda ROC tidak akan sama persis dengan Tabel 4.2/4.3**, dan pada satu kasus (FFPP→CDF) **urutan model di grafik berbeda dari tabel**. Ini titik keputusan paling penting.
3. **Semua tabel hasil docx SUDAH BENAR** terhadap run resmi 2026-06-09 (diverifikasi sel per sel, §3). **Semua nilai training (Tabel 3.10) SUDAH BENAR** terhadap `config.yaml` + `train.py` (§4).
4. **Masih ada lubang teks**: beberapa angka inline di prosa BAB IV **kosong** (mis. "AUC berada pada kisaran ()"). Bukan bug field Word — memang belum diisi (§6).
5. **Gambar 4.10 (kurva pelatihan)** tidak ada di 4 commit baru, tetapi **sudah tersedia** dari run 2026-06-09 (`results_vast_20260609/plots/`, label Inggris) (§5).

---

## 1. ISI 4 COMMIT BARU (di atas `730cc04`)

| Commit | Tanggal | Isi | Dampak ke docx |
|---|---|---|---|
| `ecfbc4d` | 06-19 | Tambah `freq_resnet18.py` (timm ResNet18, in_chans=1) + wiring train/eval/make_roc_cm + `freq_benchmark.sh`. Koreksi komentar `config.yaml` FreqCNN depth=5/base=64 → **~4,2 jt param** (dari teks lama ~2,8 jt). | **Konten opsional** (§7). Koreksi 4,2 jt **konsisten** dgn Tabel 3.6/3.7 docx (sudah ~4,2 jt). |
| `3ea7984` | 06-19 | `FREQ_BENCHMARK_RESULTS.md` — hasil n=750 seed0: AUC FreqCNN vs ResNet18 (pretrained & scratch). | Konten opsional (§7). |
| `ad6d41d` | 06-19 | Doc: link benchmark dari CODE_WALKTHROUGH, rapikan intro. | Tidak ada. |
| `a5cb3ba` | 06-20 | **ROC + CM + preds CSV + metrics JSON** untuk spatial/freq/hybrid × FFPP/CDF (in & cross) × n=100/250/500/750, **+** freqbench. Di `deepfake_hybrid/outputs/roc_cm/`. | **BESAR** — aset Gambar 4.4/4.6/4.9 (§2,§5). |

`f11a8fd` (sebelum 730cc04, dirujuk user): menetapkan **judul final** + Kata Pengantar.
→ Pastikan judul **"Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal"** dipakai konsisten di **sampul, lembar pengesahan, lembar pernyataan, header berjalan, abstrak**. Nama file docx sudah memakai judul ini → cek isi front-matter ikut diganti. Tempel Kata Pengantar dari `documents/Kata_Pengantar_2026-06-18.md`.

---

## 2. ⚠️ MASALAH UTAMA — RETRAIN: GAMBAR (run baru) vs TABEL (run lama)

### 2.1 Bukti bahwa ini run berbeda (bukan sekadar seed)
AUC bersifat **threshold-independent**. Kalau AUC berbeda, **bobot model berbeda** (= retrain). Contoh seed-0:

| Kondisi n750 seed0 | AUC run 2026-06-09 (dasar tabel) | AUC `a5cb3ba` (2026-06-20) | threshold lama → baru |
|---|---|---|---|
| spatial FFPP in | 0.7779 | **0.7671** | 0.1265 → 0.1630 |
| hybrid CDF in | 0.9181 | **0.9075** | 0.2522 → 0.6666 |
| spatial CDF in | 0.9684 | **0.9697** | 0.5636 → 0.4505 |

→ AUC & threshold sama-sama berubah ⇒ **`a5cb3ba` = run pelatihan ulang yang baru**, bukan inferensi atas checkpoint 2026-06-09. (Run lama tidak pernah meng-generate ROC/CM — itu sebabnya §2A handoff ada.)

### 2.2 Selisih nilai yang akan tampil di legenda ROC vs Tabel skripsi
Tabel skripsi = **rata-rata 3 seed (2026-06-09)**. Gambar `a5cb3ba` = **seed 0 (2026-06-20)**.

**In-dataset (n=750):**
| Model | Gambar baru (legenda ROC) | Tabel 4.2 | Δ |
|---|---|---|---|
| FFPP spatial | 0.767 | 0.780 | −0.013 |
| FFPP hybrid | 0.634 | 0.650 | −0.016 |
| FFPP freq | 0.569 | 0.546 | +0.023 |
| CDF spatial | 0.970 | 0.969 | +0.001 |
| CDF hybrid | 0.907 | 0.924 | −0.017 |
| CDF freq | 0.578 | 0.586 | −0.008 |

**Cross-dataset (n=750):**
| Arah | Model | Gambar baru | Tabel 4.3 | Δ |
|---|---|---|---|---|
| FFPP→CDF | spatial | 0.683 | 0.648 | **+0.035** |
| FFPP→CDF | hybrid | 0.680 | 0.648 | **+0.032** |
| FFPP→CDF | freq | 0.614 | 0.655 | **−0.041** |
| CDF→FFPP | spatial | 0.630 | 0.629 | +0.001 |
| CDF→FFPP | hybrid | 0.585 | 0.563 | +0.022 |
| CDF→FFPP | freq | 0.586 | 0.591 | −0.005 |

### 2.3 Satu konsekuensi naratif yang berbahaya
Pada **FFPP→CDF**, urutan AUC **berbeda**:
- **Tabel 4.3:** freq **tertinggi** (0.655) > spatial = hybrid (0.648).
- **Gambar baru:** spatial (0.683) > hybrid (0.680) > freq **terendah** (0.614).

Kalau ROC FFPP→CDF baru ditempel, **kurva freq jadi paling bawah** padahal tabel bilang freq AUC tertinggi di arah itu. Penguji yang membandingkan legenda ROC dgn Tabel 4.3 bisa menanyakannya.
*(Catatan: narasi inti — keruntuhan **recall** freq FFPP→CDF — TETAP benar di kedua run: recall 0.069 lama vs 0.056 baru. Yang flip hanya AUC.)*

### 2.4 KEPUTUSAN — pilih satu (butuh kesepakatan tim)

> **Rekomendasi: Path 1.** Selaras dgn aturan tim "jangan ubah angka hasil 2026-06-09".

- **Path 1 — Regenerasi ROC/CM dari checkpoint 2026-06-09 (PALING BERSIH, disarankan).**
  Jalankan ulang `make_roc_cm.py` (inferensi saja, cepat) pada **checkpoint seed-0 run 2026-06-09**. Hasil AUC akan = baris per-seed tabel (mis. spatial FFPP in = 0.778) → konsisten dgn Tabel 4.2/4.3 dan dgn kurva pelatihan 2026-06-09. **Buang** gambar `a5cb3ba`.
  *Prasyarat:* checkpoint 2026-06-09 masih ada (cek box vast / Google Drive / Colab / Space demo). **Aksi pertama: pastikan checkpoint lama masih tersimpan.**
- **Path 2 — Pakai gambar `a5cb3ba` apa adanya + catatan kaki.** Tambahkan di caption: *"Kurva ROC menampilkan satu run replikasi (seed 0); nilai AUC dapat berbeda tipis dari rata-rata tiga seed pada Tabel 4.2/4.3."* **Risiko:** flip urutan FFPP→CDF (§2.3) tetap terlihat. Hanya pilih bila checkpoint lama hilang & tak mau retrain.
- **Path 3 — Adopsi penuh run baru.** Latih 3 seed di setup baru, regenerasi **semua** Tabel 4.2–4.5 + bar chart + kurva + ROC/CM dari run baru. Paling banyak komputasi, dan **mengubah angka yang sudah di-settle** (melanggar aturan tim). Tidak disarankan kecuali tim sepakat ganti baseline.

---

## 3. VERIFIKASI SETIAP TABEL (vs `results_vast_20260609` / `config.yaml` / `train.py`)

Semua tabel hasil **cocok sel-per-sel** dengan run resmi 2026-06-09. Tidak ada yang perlu diubah (selama tetap Path 1/2).

| Tabel docx | Isi | Status vs sumber |
|---|---|---|
| **4.2** In-dataset n=750 (acc/prec/rec/f1/AUC ± std) | 6 baris | ✅ COCOK `n750/Table1_in_dataset_summary.csv` |
| **4.3** Cross-dataset n=750 | 6 baris | ✅ COCOK `n750/Table2_cross_dataset_summary.csv` |
| **4.4** Generalization drop F1 (n=750) | 6 baris | ✅ COCOK `n750/Table3_generalization_drop.csv` (spatial CDF +0.756, hybrid FFPP +0.027, freq CDF −0.058, dst) |
| **4.5** AUC in-dataset per tier (n=250/500/750) | 6 baris | ✅ COCOK auc_mean tiap tier (mis. FFPP spatial 0.746/0.693/0.780; CDF hybrid 0.812/0.892/0.924) |
| **4.6 (RM)** Temuan per rumusan masalah | naratif | ✅ Angka rujukan (AUC s.d. 0.969; freq 0.55–0.59; recall 0.083) konsisten. *Catat:* freq cross FFPP→CDF tabel = 0.655, sedikit di luar "0,55–0,59" — kosmetik, boleh dibiarkan. |

**Tabel non-hasil yang relevan dgn commit baru:**
- **Tabel 3.6 (arsitektur FreqCNN) & 3.7 (dimensi fitur hybrid):** total **~4,2 juta** param → ✅ konsisten dgn koreksi `config.yaml` di `ecfbc4d` (komentar lama ~2,8 jt sudah diperbaiki). Tidak ada aksi.

> Verifikasi numerik penuh: lihat lampiran perhitungan di bawah (§8).

---

## 4. VERIFIKASI NILAI TRAINING (Tabel 3.10) vs KODE — SEMUA BENAR

Diperiksa terhadap `config.yaml` + `scripts/train.py`:

| Item Tabel 3.10 | Nilai docx | Kode | OK? |
|---|---|---|---|
| Optimizer | **AdamW** | `optim.AdamW(...)` (train.py:200–229) | ✅ |
| LR base | 2×10⁻⁴ | `lr: 2.0e-4` | ✅ |
| LR backbone | 2×10⁻⁵ (base/10) | `backbone_lr = base_lr/10` (train.py:191) | ✅ |
| Weight decay | 1×10⁻⁴ | `weight_decay: 1.0e-4` | ✅ |
| Batch size / accum | 16 / 2 (efektif 32) | `batch_size: 16`, `accum_steps: 2` | ✅ |
| Epoch maks | 30 | `epochs: 30` | ✅ |
| Early stop patience | 12 | `early_stop_patience: 12` | ✅ |
| Label smoothing | 0,05 | `label_smoothing: 0.05` | ✅ |
| Pos weight | n_neg/n_pos | `pos_weight = n_neg/max(n_pos,1)` (train.py:184) | ✅ |
| Gradient clip | max_norm=5,0 | `clip_grad_norm_(..., max_norm=5.0)` (train.py:117) | ✅ |
| LR warmup | 3 epoch (10%→100%) | `LinearLR(start_factor=0.1, total_iters=3)` (train.py:256) | ✅ |
| LR schedule | cosine → 1×10⁻⁶ | `CosineAnnealingLR(eta_min=1e-6)` (train.py:260) | ✅ |
| Backbone freeze | 3 epoch | `FREEZE_EPOCHS = 3` (train.py:26) | ✅ |
| FreqCNN depth | 5 (~4,2 jt) | `freq_depth: 5`, `freq_base_channels: 64` | ✅ |
| Seed | 0,1,2 | `n_seeds: 3` | ✅ |

> **Catatan internal:** memory/CLAUDE.md masih menyebut "Optimizer: Adam". Kode **memakai AdamW** (Loshchilov & Hutter). **Docx sudah benar (AdamW)** — jangan diubah. Yang perlu diperbarui justru CLAUDE.md/memory, bukan skripsi.

---

## 5. RENCANA PENYISIPAN GAMBAR (4 placeholder tersisa)

Placeholder yang masih ada di docx **persis 4**: `[MASUKAN GAMBAR 4.4]`, `[MASUKKAN GAMBAR 4.6]`, `[MASUKKAN GAMBAR 4.9]`, `[MASUKKAN GAMBAR 4.10]`.
(Gambar 4.1 & 4.2 demo **sudah tersisip** — bukan placeholder lagi.)

### 5.1 Pemetaan file → gambar
File ROC = **overlay 3 model dalam 1 grafik** (legenda berisi AUC tiap model). File CM = **1 model per file**.

| Placeholder | Konten | File sumber (jika Path 1: regen dari ckpt lama; jika Path 2: pakai `a5cb3ba` apa adanya) |
|---|---|---|
| **Gambar 4.4** ROC in-dataset | 2 panel: FFPP & CDF | `outputs/roc_cm/FFPP_in_n750_roc.png` + `CDF_in_n750_roc.png` → `media_v2/gambar_4_4_roc_in_dataset.png` |
| **Gambar 4.6** ROC cross-dataset | 2 panel: FFPP→CDF & CDF→FFPP | `outputs/roc_cm/FFPP2CDF_n750_roc.png` + `CDF2FFPP_n750_roc.png` → `media_v2/gambar_4_6_roc_cross_dataset.png` |
| **Gambar 4.9** Confusion matrix | contoh in + cross (sorot keruntuhan recall) | mis. `FFPP_in_n750_cm_spatial.png` + `CDF2FFPP_n750_cm_spatial.png` (CM cross spatial paling menonjolkan recall jatuh: TP 308 / FN 4108) → `media_v2/gambar_4_9_confusion_matrix.png` |
| **Gambar 4.10** Kurva pelatihan | freq vs spatial, FFPP | `results_vast_20260609/plots/training_curves_freq_FFPP_n750.png` + `training_curves_spatial_FFPP_n750.png` → `media_v2/gambar_4_10_kurva_pelatihan.png` |

**Catatan penting Gambar 4.10:**
- TIDAK ada di 4 commit baru. **Sudah ada** dari run 2026-06-09 (`results_vast_20260609/plots/`), tetapi **label sumbu Bahasa Inggris**.
  - Cepat: salin apa adanya (stopgap).
  - Rapi: regen versi Indonesia (butuh histori per-epoch di mesin pelatihan — `history.json` tidak ter-commit).
- Karena 4.10 berasal dari run 2026-06-09, **inilah alasan tambahan memilih Path 1** agar ROC/CM (4.4/4.6/4.9) juga dari run 2026-06-09 → semua gambar BAB IV satu run.

### 5.2 🔴 RENUMBER GAMBAR BAB IV (wajib — penomoran sekarang tabrakan)
Docx sekarang **setengah jalan** antara dua skema:
- **Caption** pakai skema 6-gambar: cross-bar=**4.4**, drop=**4.5**, scaling=**4.6**.
- **Narasi + placeholder** pakai skema 10-gambar: ROC-in=4.4, ROC-cross=4.6, CM=4.9, pelatihan=4.10.
- **File media_v2** pakai skema 10-gambar: `gambar_4_3` (bar in), `gambar_4_5` (bar cross), `gambar_4_7` (drop), `gambar_4_8` (scaling).

**Keputusan handoff 2026-06-17 (§0b.A): pakai skema 10-gambar.** Target akhir:

| No final | Gambar | Status aset |
|---|---|---|
| 4.1 | Antarmuka demo | ✅ tersisip |
| 4.2 | "What the models see" | ✅ tersisip |
| 4.3 | Bar in-dataset | ✅ `gambar_4_3_perbandingan_in_dataset.png` |
| **4.4** | **ROC in-dataset** | 🆕 dari `a5cb3ba`/regen |
| 4.5 | Bar cross-dataset | ✅ `gambar_4_5_perbandingan_cross_dataset.png` *(caption docx skrg salah nomor 4.4)* |
| **4.6** | **ROC cross-dataset** | 🆕 dari `a5cb3ba`/regen |
| 4.7 | Generalization drop | ✅ `gambar_4_7_generalization_drop.png` *(caption docx skrg salah nomor 4.5)* |
| 4.8 | Scaling AUC | ✅ `gambar_4_8_scaling_auc.png` *(caption docx skrg salah nomor 4.6)* |
| **4.9** | **Confusion matrix** | 🆕 dari `a5cb3ba`/regen |
| **4.10** | **Kurva pelatihan** | ✅ dari 2026-06-09 (label Inggris) |

**Aksi renumber di docx:**
1. Caption bar-cross saat ini "Gambar 4.4 Perbandingan performa cross-dataset" → **jadikan 4.5**.
2. Caption "Gambar 4.5 Generalization drop" → **jadikan 4.7**.
3. Caption "Gambar 4.6 Tren AUC" → **jadikan 4.8**.
4. Sisipkan 4 gambar baru pada placeholder masing-masing (caption di bawah, rata tengah, sesuai Pedoman).
5. Perbaiki typo placeholder `[MASUKAN GAMBAR 4.4]` (kurang satu K) — hapus saat menyisipkan gambar.
6. **Update DAFTAR GAMBAR** (Update Field) → harus memuat 4.1–4.10 (sekarang hanya 4.1–4.6).
7. Pastikan rujukan narasi: "Gambar 4.4" (ROC in) ✓, "Gambar 4.6" (ROC cross) ✓, "Gambar 4.9" (CM) ✓, "Gambar 4.10" (pelatihan) ✓ — semua sudah pakai nomor skema-10, jadi setelah caption diselaraskan, narasi otomatis benar. **Tapi** cek rujukan "Gambar 4.3" (bar in) & yang menyebut drop/scaling agar memakai 4.7/4.8.

---

## 6. LUBANG ANGKA INLINE DI PROSA BAB IV (isi manual — dari Tabel 2026-06-09)

Beberapa nilai dalam tanda kurung **benar-benar kosong** di docx (bukan field Word). Isi dari run 2026-06-09:

| Lokasi prosa | Teks | Isi yang benar |
|---|---|---|
| §4.1.3 pengantar | "Hasil pada tier ( ) … Tabel 4.2 ( , rata-rata ± simpangan baku atas 3 seed)" | **n = 750** (2 tempat) |
| §4.1.4 cross | "AUC berada pada kisaran ( )." | **0,56–0,66** (rentang AUC cross seluruh model) |
| §4.1.4 cross | "spasial … presisi sangat tinggi ( ) namun recall runtuh menjadi ( )" | presisi **0,932**, recall **0,083** (spatial CDF→FFPP) |
| §4.1.4 cross | "hybrid (presisi , recall )" | presisi **0,789**, recall **0,143** (hybrid CDF→FFPP) |
| §4.1.4 cross | "frekuensi … keruntuhan recall ( )" | recall **0,069** (freq FFPP→CDF) |
| §4.1.4 cross | "spasial dan hybrid mempertahankan recall yang lebih wajar ( dan )" | **0,618** dan **0,570** (FFPP→CDF) |
| §4.1.6 scaling | "tiga tier … yaitu , , dan ." | **250, 500, 750** |
| Caption 4.3/4.5(bar)/4.7 | "… ( )" | **(n = 750)** |

> Jika tim memilih **Path 2/3**, angka-angka ini harus mengikuti run yang dipilih, BUKAN tabel 2026-06-09. (Argumen lain untuk Path 1: prosa & gambar & tabel satu sumber.)

---

## 7. KONTEN OPSIONAL BARU — BENCHMARK FreqCNN vs ResNet18 (`3ea7984`)

Bukan perbaikan docx; **tambahan untuk antisipasi pertanyaan penguji** *"kenapa FreqCNN buatan sendiri, bukan arsitektur standar?"*

Hasil n=750 seed0 (`FREQ_BENCHMARK_RESULTS.md`):
- **Arm from-scratch (perbandingan arsitektur terkontrol): FreqCNN menang di 4/4 kondisi** dgn 2,6× lebih sedikit parameter (4,2 jt vs 11,2 jt). → jawaban kuat & jujur.
- **Arm pretrained: 2–2 split.** ResNet18-ImageNet **mengalahkan** FreqCNN di CDF-in (0.609 vs 0.578) & FFPP→CDF (0.628 vs 0.614). → **JANGAN klaim "ResNet18 kalah telak".**
- Semua AUC di pita 0.51–0.63 (near-chance), single seed → selisih <0.03 = imbang.

**Rekomendasi:** kalau mau dipakai, masukkan **hanya sebagai paragraf/lampiran pertahanan** dengan klaim defensif: *"pada kondisi pelatihan yang setara (from scratch), FreqCNN ringan tidak kalah dari ResNet18 yang 2,6× lebih besar; transfer learning ImageNet membuat ResNet18 setara, bukan unggul."* Sudah disiapkan di deck sidang. **Tidak wajib** untuk skripsi.

---

## 8. CHECKLIST AKSI (urut prioritas)

**A. Keputusan run (BLOCKER — sebelum sentuh gambar):**
- [ ] Cek apakah **checkpoint seed-0 run 2026-06-09** masih ada (vast / Drive / Colab / Space demo).
- [ ] Tim pilih **Path 1 / 2 / 3** (§2.4). *Rekomendasi: Path 1.*
- [ ] (Path 1) Jalankan `make_roc_cm.py` inferensi pada ckpt lama → ROC/CM yang AUC-nya = tabel.

**B. Penyisipan & penomoran gambar (§5):**
- [ ] Sisip Gambar **4.4** (ROC in), **4.6** (ROC cross), **4.9** (CM), **4.10** (kurva pelatihan).
- [ ] Renumber caption: cross-bar→**4.5**, drop→**4.7**, scaling→**4.8**.
- [ ] Perbaiki typo `[MASUKAN GAMBAR 4.4]` saat menyisip.
- [ ] (4.10) putuskan stopgap label Inggris vs regen label Indonesia.
- [ ] Update **DAFTAR GAMBAR** → 4.1–4.10.

**C. Isi lubang angka prosa BAB IV (§6):**
- [ ] Isi 8 grup nilai kosong (n=750, presisi/recall cross, tier 250/500/750, dst).

**D. Front matter (dari `f11a8fd`):**
- [ ] Judul final konsisten di sampul / pengesahan / pernyataan / header / abstrak.
- [ ] Tempel Kata Pengantar (`Kata_Pengantar_2026-06-18.md`).

**E. Verifikasi akhir:**
- [ ] Tabel 4.2–4.5 tetap = 2026-06-09 (jangan diubah bila Path 1/2). ✅ sudah cocok.
- [ ] Tabel 3.10 training = kode. ✅ sudah cocok (AdamW).
- [ ] `Ctrl+A → F9` (Update Fields) untuk SEQ tabel/gambar, sitasi [N], daftar isi/tabel/gambar.

**F. Opsional:**
- [ ] Pertimbangkan paragraf/lampiran benchmark ResNet18 (§7) — klaim defensif saja.
- [ ] Perbarui CLAUDE.md/memory: optimizer = **AdamW** (bukan Adam).

---

## LAMPIRAN — verifikasi numerik tabel (ringkas)

**Tabel 4.2 (in n750) vs `Table1_in_dataset_summary.csv`** — cocok:
FFPP spatial 0.700/0.662/0.766/0.710/0.780 · FFPP hybrid 0.610/0.588/0.618/0.603/0.650 · FFPP freq 0.531/0.512/0.560/0.529/0.546 · CDF spatial 0.915/0.906/0.912/0.909/0.969 · CDF hybrid 0.858/0.851/0.843/0.847/0.924 · CDF freq 0.563/0.529/0.495/0.511/0.586.

**Tabel 4.3 (cross n750) vs `Table2_cross_dataset_summary.csv`** — cocok:
FFPP→CDF spatial 0.608/0.571/0.618/0.594/0.648 · hybrid 0.611/0.584/0.570/0.576/0.648 · freq 0.550/0.621/0.069/0.124/0.655 · CDF→FFPP spatial 0.558/0.932/0.083/0.153/0.629 · hybrid 0.569/0.789/0.143/0.237/0.563 · freq 0.571/0.549/0.596/0.570/0.591.

**Tabel 4.4 (drop n750)** — cocok: spatial FFPP +0.116 / CDF +0.756 · hybrid FFPP +0.027 / CDF +0.609 · freq FFPP +0.406 / CDF −0.058.

**Tabel 4.5 (AUC in per tier 250/500/750)** — cocok: FFPP spatial 0.746/0.693/0.780 · FFPP hybrid 0.542/0.582/0.650 · FFPP freq 0.480/0.570/0.546 · CDF spatial 0.942/0.967/0.969 · CDF hybrid 0.812/0.892/0.924 · CDF freq 0.569/0.615/0.586.
