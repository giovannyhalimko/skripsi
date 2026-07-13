# Jurnal Eksperimen (Kronologis) + Perbandingan Fusi — Bukti Pengujian

> Semua percobaan yang pernah dijalankan, disusun **per-train (kronologis)**: konfigurasi → hasil → catatan, lalu **section per strategi fusi** (late/early fusion) dan **benchmark backbone frekuensi**. Bukti fisik di `deepfake_hybrid/outputs/` (train.log, metrics.json, conclusion.md tiap folder bertanggal). Dibuat 2026-07-07.
>
> **Konvensi:** angka = **AUC in-dataset** (test) kecuali disebut lain. Model: **S**=spatial, **F**=freq, **H**=hybrid.

---

# BAGIAN A — Jurnal Kronologis (train demi train)

### Train 1 — 2026-03-12 s/d 03-16 · n=50, n=200 (+ EARLY FUSION n=400)
**Konfigurasi:** 10 epoch · lr **1e-4** · **Adam** · ImageNet-pretrained (S & H) · FreqCNN **depth 3** · FFT-norm `(x−0,5)/0,5` · flip konsisten dua cabang · freeze belum ada.
**Hasil (AUC in-dataset):**
| | FFPP | CDF |
|---|---|---|
| n=50 | S **0,808** · F 0,541 · H 0,662 | S 0,654 · F 0,297 · H 0,554 |
| n=200 | S 0,484 · F 0,500 · H 0,525 | S **0,710** · F 0,691 · H 0,667 |
| **Early fusion (n=400 FFPP)** | val-AUC puncak **0,685** (epoch 6) | — |
**Catatan:** spatial umumnya terbaik; **early fusion diuji di sini** dan **tidak lebih baik** → tidak dikejar. Folder: `2026-03-15/`, `2026-03-16/`, `runs/early_fusion_FFPP_n400_seed0/`.

### Train 2 — 2026-03-23/24 · n=100/250/300/600/1000
**Perubahan besar (vs Train 1):** FFT-norm `(0,5;0,5)→(5,0;3,0)` · LR scheduler cosine → **warmup+cosine** · **gradient clipping** ditambah · **noise FFT** ditambah · **FreqCNN 3→5 blok** · **SE gate** ditambah · **label smoothing 0,05** ditambah.
**Hasil (in-dataset terbaik):** FFPP n100 → H F1 0,597/AUC 0,614; n1000 → F F1 0,557. CDF → spatial dominan di skala besar.
**Catatan:** hasil masih fluktuatif, hybrid sempat collapse di beberapa tier. Folder: `2026-03-23/CONCLUSION_OVERALL.md`, `2026-03-24/`.

### Train 3 — 2026-03-25 · n=100
**Perubahan:** **residual FreqCNN depth 5** (~700K, FreqBlock) · **Adam → AdamW** · **backbone freezing** spatial (3 epoch) + diff-LR (backbone 1e-5/head 1e-4) · warmup 2→3 · **ColorJitter + RandomErasing** · spectral mask p=0,3 · hybrid dropout 0,5→0,3.
**Hasil (FFPP, AUC):** S **0,706** (+0,147) · F **0,727** · H **0,787**.
**Catatan:** **lompatan besar** — AdamW + FreqCNN residual + freeze sangat membantu. Folder: `2026-03-25/`.

### Train 4 — 2026-04-03 · n=100
**Perubahan:** lr 1e-4→**5e-4** · patience 5→10 · label smoothing 0,02→**0,0** · warmup 3→1 · grad clip 1,0→**5,0** · **pos_weight** di loss · spectral mask 0,30→**0,15** · tier disatukan → **100/250/500/750**.
**Hasil (CDF, AUC):** S **0,951** · F 0,799 · H **0,895**. FFPP masih lemah (S 0,542).
**Catatan:** CDF sangat baik, FFPP tetap sulit. Folder: `2026-04-03/`.

### Train 5 — 2026-04-05 · n=100, n=250
**Konfigurasi:** seed 0 · lr **2e-4** · warmup 2 · patience 10 · pretrained.
**Hasil (AUC in-dataset):** FFPP n250 → S 0,552 · F 0,723 · H 0,563; CDF n250 → S 0,684 · F 0,578 · H 0,575.
**Catatan:** **regresi di n250** (turun dari n100) — masalah yang diperbaiki di Train 8. Folder: `2026-04-05/`.

### Train 6 — 2026-04-09/10 · Ablasi (n=100)
**Yang diuji:** **face crop** (dengan vs tanpa MTCNN) · **separated_ffpp** · **freq-only** (seed 42).
**Catatan:** memfinalkan keputusan face crop + isolasi cabang. Folder: `2026-04-09/face_crop`, `separated_ffpp`, `2026-04-10/freq_only`.

### Train 7 — 2026-04-15 · n=500 (Kaggle, full matrix)
**Hasil (AUC in-dataset):** FFPP → S **0,749** · F 0,531 · H 0,555 (**collapse**, early-stop epoch 6); CDF → S **0,923** · F 0,625 · H 0,808.
**Catatan:** **hybrid-FFPP collapse** (early stopping terlalu dini). Folder: `2026-04-15/`.

### Train 8 — 2026-06-04 · n=100, n=250 (Kaggle)
**Perubahan:** **config-drift fix** (commit 1985a7a, FreqCNN/patience terbawa ke run) · **LR rebalance hybrid** → 3 grup: backbone 2e-5 / **freq-branch 5e-5** / head 2e-4 · **patience 10→12** · warmup → LR penuh epoch 4.
**Hasil (AUC in-dataset n=250):** FFPP → S **0,877** · F 0,670 · H 0,668; CDF → S 0,884 · F 0,622 · H 0,803.
**Catatan:** **hybrid collapse teratasi**; regresi n250 dibalik. **Ini konfigurasi final.** Folder: `2026-06-04/`.

### Train 9 (FINAL) — n=750 · 3 seed (dipakai di skripsi)
**Konfigurasi:** config final (lihat `RINGKASAN_PARAMETER_NILAI_PROYEK.md`) · **3 seed (0,1,2)** · mean ± std.
**Hasil (AUC in-dataset, mean):**
| | FFPP | CDF |
|---|---|---|
| Spatial | **0,778** | **0,971** |
| Freq | 0,562 | 0,562 |
| Hybrid | 0,644 | 0,919 |

**Hasil (AUC cross-dataset, mean):**
| | FFPP→CDF | CDF→FFPP |
|---|---|---|
| Spatial | **0,678** | **0,607** |
| Freq | 0,606 | 0,575 |
| Hybrid | 0,665 | 0,555 |

**Catatan:** hasil **final** skripsi. Spatial terbaik; **freq near-random (0,56–0,61)**; **hybrid tidak mengungguli spatial**; recall runtuh lintas dataset. Folder: `tables/n750/`, `roc_cm/*_n750_*`.

---

# BAGIAN B — Per Strategi Fusi

### B.1 Late Fusion — Hybrid (HybridTwoBranch) — **jalur utama**
Dua cabang terpisah (XceptionNet spasial + FreqCNN frekuensi) → proyeksi 256 masing-masing → concat 512 → **SE gate** → classifier. Diuji & dituning di **seluruh Train 1–9**. Kesimpulan final: **tidak mengungguli baseline spasial** (in-dataset), manfaat lintas dataset **parsial & bergantung arah** (Train 9).

### B.2 Early Fusion (XceptionNet 4-kanal RGB+FFT) — **diuji, tidak dikejar**
- **Diuji sekali:** 2026-03-12, n=400, FFPP, seed 0 (`runs/early_fusion_FFPP_n400_seed0/train.log`).
- **Hasil:** val-AUC puncak **≈ 0,685** (epoch 6), val-F1 ≈ 0,62 — **setara/di bawah hybrid**.
- **Keputusan:** tidak dilanjutkan; di skripsi menjadi **"alternatif konseptual"** (BAB II), bukan model evaluasi.
- **Jawaban sidang:** *"kenapa tidak early fusion?"* → **sudah dicoba, hasilnya tidak lebih baik.**

### B.3 Benchmark backbone frekuensi — **FreqCNN vs ResNet18** (freqbench)
Menguji apakah cabang frekuensi yang lemah = salah FreqCNN atau keterbatasan FFT. Backbone **ResNet18 (pretrained & scratch)** dilatih pada input FFT yang sama, n=750, 4 skenario (`roc_cm/freqbench_*`).
| Skenario | FreqCNN | ResNet18-pretrained | ResNet18-scratch |
|---|---|---|---|
| FFPP in | 0,569 | 0,561 | 0,507 |
| CDF in | 0,578 | 0,609 | 0,545 |
| FFPP→CDF | 0,614 | 0,628 | 0,544 |
| CDF→FFPP | 0,586 | 0,578 | 0,545 |
**Kesimpulan:** **semua** backbone frekuensi (termasuk ResNet18-pretrained) tetap **near-random (0,51–0,63)**. → Kelemahan frekuensi = **keterbatasan representasi FFT**, bukan salah FreqCNN. **Jawaban sidang:** *"mungkin FreqCNN kurang dalam?"* → **sudah dicoba ResNet18 pretrained & scratch, tetap near-random.**

---

# BAGIAN C — Sweep ukuran sampel (semua tier yang pernah dijalankan)

| Tier | Jumlah run | Skema |
|---|---|---|
| n=10 | 2 | smoke |
| n=50 | 18 | awal |
| n=100 | 88 | terbanyak |
| n=200 | 18 | |
| n=250 | 34 | **final** |
| n=300 | 7 | lama |
| n=400 | 13 | + early fusion |
| n=500 | 22 | **final** |
| n=600 | 7 | lama |
| n=750 | 12 | **final (headline)** |
| n=1000 | 7 | lama |

→ Tier **300/600/1000 memang pernah dijalankan** (skema lama), final memakai **100/250/500/750**. Seed: seed 0 (167 run) + seed 42 (4 run) + **final 3 seed (0/1/2)**.

---

# BAGIAN D — Ringkasan "pernah dicoba?" (untuk Q&A sidang)

| Pertanyaan | Jawaban singkat | Bukti |
|---|---|---|
| Pernah coba **early fusion**? | Ya, n400 FFPP, val-AUC ≈0,68, tidak lebih baik | `runs/early_fusion_FFPP_n400_seed0/` |
| **Late fusion** dituning? | Ya, Train 1–9 (SE gate, LR rebalance, dll) | folder bertanggal |
| Mungkin **FreqCNN kurang kuat**? | Sudah coba ResNet18 pre/scratch, tetap near-random | `roc_cm/freqbench_*` |
| Cuma beberapa ukuran sampel? | Tidak — n=10…1000 | `runs/`, `tables/` |
| **Face crop** berpengaruh? | Ada ablasinya | `2026-04-09/face_crop/` |
| Multi-seed? | Ya (0, 42, lalu 0/1/2) | nama dir `*_seed*` |

---

# BAGIAN E — Lokasi bukti
```
deepfake_hybrid/outputs/
├── runs/early_fusion_FFPP_n400_seed0/train.log   # bukti early fusion
├── roc_cm/freqbench_*_metrics.json               # bukti FreqCNN vs ResNet18
├── tables/n{100,250,500,750}/                     # hasil final (Train 9)
├── 2026-03-15 … 2026-06-04/conclusion.md          # jurnal per-train (Train 1–8)
│   ├── 2026-03-23/CONCLUSION_OVERALL.md           # perbandingan old-vs-new code
│   ├── 2026-04-09/face_crop, separated_ffpp       # ablasi
│   └── 2026-04-10/freq_only                       # ablasi
```

*(Nilai per-train dikutip dari `conclusion.md` masing-masing folder; hasil final dari `tables/n750/`. Konfigurasi parameter lengkap ada di `RINGKASAN_PARAMETER_NILAI_PROYEK.md`.)*
