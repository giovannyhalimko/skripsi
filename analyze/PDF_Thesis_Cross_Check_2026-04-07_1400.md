# PDF Thesis Cross-Check Analysis

**Date:** 2026-04-07
**Source:** PDF version of thesis (115 pages, 6.6MB)
**Cross-checked against:** `Architecture_and_Pipeline_Deep_Analysis_2026-04-07_1200.md` and actual code

---

## 1. [PERLU ISI] Markers Found

| Location | Section | What's Needed |
|---|---|---|
| **p.86** | **3.4.4 Perbandingan Arsitektur Model** | `[PERLU ISI]` appears before Tabel 3.6. Needs **narrative text** comparing the three architectures — explain why three models are tested, what each contributes, and how they relate to the research questions. Write 2-3 paragraphs discussing trade-offs between spatial-only, freq-only, and hybrid approaches. |

---

## 2. BAB IV and BAB V — Empty

| Section | Page | Status |
|---|---|---|
| **BAB IV HASIL DAN PEMBAHASAN** | p.100 | **Completely empty** — only section headers "4.1 Hasil" and "4.2 Pembahasan" exist with no content |
| **BAB V PENUTUP** | p.101 | **Completely empty** — only header exists |
| **DAFTAR PUSTAKA** | p.102+ | Exists with references listed |

**Action:** BAB IV needs all result tables, analysis, cross-dataset comparison, and discussion. BAB V needs conclusions and recommendations.

---

## 3. BAB III vs Code Accuracy Check

The PDF BAB III (p.64–99) is significantly **updated and accurate** compared to the older .md version. It correctly reflects the current code architecture. Specific verification:

### Correct (Matches Code)

| Claim in PDF | Actual Code Value | Status |
|---|---|---|
| Optimizer: AdamW | `torch.optim.AdamW` in train.py | Correct |
| LR base: 2×10⁻⁴ | config.yaml `lr: 2.0e-4` | Correct |
| LR backbone: 2×10⁻⁵ | `base_lr / 10` in train.py | Correct |
| Early stopping patience: 10 | config.yaml `early_stop_patience: 10` | Correct |
| Label smoothing: 0.0 (disabled) | config.yaml `label_smoothing: 0.0` | Correct |
| Gradient clipping max_norm: 5.0 | train.py `clip_grad_norm_ max_norm=5.0` | Correct |
| FreqCNN depth: 5, ~700K params | config.yaml `freq_depth: 5` | Correct |
| FreqBlock with residual connections | freq_cnn.py `FreqBlock` class | Correct |
| Batch size: 16, effective 32 | config.yaml `batch_size: 16`, `accum_steps: 2` | Correct |
| Image size: 224×224 | config.yaml `image_size: 224` | Correct |
| Split: 70/15/15 stratified by video | build_splits.py | Correct |
| FFPP samples: [100,300,600,1000] | Tabel 3.2 | Correct |
| CDF samples: [100,250,500,750] | Tabel 3.2 | Correct |
| 3 seeds (0,1,2) | config.yaml `n_seeds: 3` | Correct |
| SE Gate reduction=4 | hybrid_fusion.py `SEGate(reduction=4)` | Correct |
| PROJ_DIM = 256 | hybrid_fusion.py | Correct |
| pos_weight = n_neg/n_pos | train.py | Correct |
| Spectral band masking 15% | deepfake_data.py `random.random() < 0.15` | Correct |
| FFT noise σ=0.05 | config.yaml `fft_noise_sigma: 0.05` | Correct |
| ColorJitter + RandomErasing | transforms.py | Correct |
| Warmup 2 epochs + cosine decay | train.py `SequentialLR` | Correct |
| Backbone freeze 3 epochs (all pretrained) | train.py `FREEZE_EPOCHS=3` | Correct |
| Classifier: Dropout(0.3)→FC→Dropout(0.3)→FC | hybrid_fusion.py | Correct |
| FreqCNN feature_dim: 256 (depth=5) | freq_cnn.py | Correct |
| Grayscale ITU-R BT.601 | fft_utils.py PIL "L" mode | Correct |

**Assessment: BAB III is now fully aligned with current code. All hyperparameters, architecture details, and training strategies match.**

---

## 4. Issues Found in PDF

### 4.1 Missing Narrative — Section 3.4.4 (p.86)

**Problem:** `[PERLU ISI]` tag present. The section jumps directly from the late fusion calculation example to Tabel 3.6 without any connecting narrative.

**Fix needed:** Add 2-3 paragraphs before Tabel 3.6 that:
1. Summarize why three architectures are tested (controlled comparison)
2. Highlight key differences (parameter count, domain, fusion mechanism)
3. Connect to research questions — which model addresses which question
4. Briefly explain what each table shows

**Suggested text (Indonesian):**

> Untuk memberikan evaluasi yang komprehensif, penelitian ini membandingkan ketiga arsitektur model secara sistematis. Perbandingan ini memungkinkan analisis kontribusi individual masing-masing domain (spasial dan frekuensi) serta evaluasi apakah penggabungan keduanya melalui model *hybrid* menghasilkan peningkatan performa yang signifikan.
>
> Tabel 3.6 merangkum perbedaan utama antara ketiga arsitektur, meliputi jenis input, *backbone* yang digunakan, mekanisme fusi, jumlah parameter, dan domain analisis. Sementara Tabel 3.7 merinci dimensi fitur pada setiap komponen model *hybrid*, menunjukkan aliran data dari input hingga keluaran *logit* klasifikasi.
>
> Perbedaan paling mendasar antara ketiga model terletak pada domain informasi yang dieksploitasi: model spasial mengandalkan fitur visual tingkat tinggi dari XceptionNet yang telah *pretrained*, model frekuensi mengekstraksi pola spektral menggunakan FreqCNN yang dilatih dari awal, dan model *hybrid* menggabungkan keduanya melalui proyeksi dimensi seimbang dan SE *gating* yang adaptif. Desain tiga varian ini secara langsung menjawab rumusan masalah pertama dan kedua penelitian, yaitu bagaimana membangun detektor *deepfake* yang lebih akurat dan bagaimana mengevaluasi kontribusi masing-masing jenis fitur.

### 4.2 Abstrak Not Written (p.1)

**Problem:** Both Indonesian and English abstracts are template placeholders:
- Indonesian: "Abstrak minimal 100 kata dan maksimal 200 kata berbahasa Indonesia..."
- English: "A minimum 100 words and maximum 200 words of abstract in English..."
- Keywords: "3 s/d 5 kata kunci dicetak miring" / "3 to 5 keywords in italics"

**Action:** Write both abstracts after BAB IV results are available. Should summarize: problem, method (hybrid XceptionNet + FFT + FreqCNN + SE gating), datasets (FFPP, CDF), key results, and conclusion.

### 4.3 Kata Pengantar — Says "tesis" (p.2)

**Problem:** The Kata Pengantar says "menyelesaikan **tesis**" — should be "**skripsi**".

**Fix:** Change "tesis" to "skripsi" in the Kata Pengantar.

### 4.4 Daftar Lampiran Empty (p.11)

**Problem:** The page exists but has no content listed.

**Action:** Populate after completing BAB IV with actual appendix items (code snippets, additional tables, training logs, etc.)

### 4.5 BAB II Recall Formula — Previously Fixed?

The Recall formula on p.50 shows:

$$Recall = \frac{TP}{TP + FP}$$

**This is WRONG.** The correct formula is:

$$Recall = \frac{TP}{TP + FN}$$

However, checking the calculation example on p.53, the example uses the **correct** formula (TP / (TP + FN) = 180/220 = 0.818). So the formula definition on p.50 is incorrect but the worked example is correct. **The formula text on p.50 needs to be fixed.**

### 4.6 Table Numbering — Tabel 3.12/3.13 vs PDF

In the PDF on p.98, the confusion matrix example is "Tabel 3.12" and the metric calculation is "Tabel 3.13". But the HTML table files use "Tabel 3.13" for confusion matrix and "Tabel 3.14" for metrics. The PDF numbering (3.12, 3.13) is correct since there are 13 tables total in BAB III (the original Tabel 3.12 "Struktur Confusion Matrix" template from the .md was merged into BAB II's Tabel 2.5, so it was removed from BAB III).

**The HTML files tabel_3_13 and tabel_3_14 should be renumbered to match the PDF's 3.12 and 3.13.**

### 4.7 Equation Numbering

BAB III equations are properly numbered (3.1 through 3.36). However:
- Equation 3.29 appears twice on p.91 (both the loss formula and pos_weight formula use 3.29)
- **Fix:** Renumber pos_weight formula to 3.30 and shift subsequent equations

### 4.8 Recall Formula in BAB II (Equation 2.25, p.50)

The displayed formula shows $Recall = \frac{TP}{TP+FP}$ which is the Precision formula, not Recall.

**Fix:** Change to $Recall = \frac{TP}{TP+FN}$

---

## 5. BAB II Content Assessment

BAB II (p.5–63, ~58 pages) is **comprehensive and well-structured** with 21 major sections:
- 2.1–2.3: Deepfake fundamentals, GAN, detection approaches
- 2.4–2.8: Frequency domain (FFT, spectral distortions, spectral dropoff, periodic noise, warping)
- 2.9: Deep learning and CNN (with depthwise separable conv detail)
- 2.10: XceptionNet (architecture, transfer learning, advantages)
- 2.11: SE-Net (channel attention, SE block, multi-domain fusion relevance)
- 2.12–2.13: FaceForensics++ and Celeb-DF
- 2.14–2.16: Image analysis, video analysis, preprocessing
- 2.17: Optimization (SGD, AdamW, BCE loss)
- 2.18: Evaluation metrics (all 5 metrics + AUC + worked example)
- 2.19–2.20: Cross-dataset generalization, cross-GAN
- 2.21: Dasar pemilihan metode (FFT vs DCT vs wavelet comparison, XceptionNet vs ResNet vs MesoNet)

**Strengths:** Thorough frequency domain coverage, good SE-Net section connecting to hybrid fusion, comprehensive cross-dataset generalization discussion.

---

## 6. BAB III Content Assessment

BAB III (p.64–99, ~35 pages) covers:
- 3.1: Research framework with flowchart (Gambar 3.1) — **has diagram**
- 3.2: Datasets (FFPP + CDF) with sample images (Gambar 3.2) — **has images**
- 3.3: Preprocessing with FFT manual calculation, spectral masking visual (Gambar 3.3), FFT comparison (Gambar 3.4) — **has figures**
- 3.4: Model architectures with FreqBlock diagram (Gambar 3.5), XceptionNet diagram (Gambar 3.6), FreqCNN diagram (Gambar 3.7), HybridTwoBranch diagram (Gambar 3.8) — **has all 4 architecture diagrams**
- 3.5: Training strategy with LR schedule plot (Gambar 3.9) — **has LR curve**
- 3.6: Experiment design with full matrix
- 3.7: Evaluation methods with worked confusion matrix example

**Assessment:** BAB III is now **~95% complete**. Only missing items:
1. `[PERLU ISI]` narrative in 3.4.4 (minor — 2-3 paragraphs needed)
2. Duplicate equation numbering (3.29 appears twice)

---

## 7. Summary of Required Actions

| Priority | Item | Location | Effort |
|---|---|---|---|
| **HIGH** | Fill `[PERLU ISI]` in 3.4.4 | p.86 | Low (2-3 paragraphs) |
| **HIGH** | Write BAB IV (Hasil dan Pembahasan) | p.100 | High (needs results data) |
| **HIGH** | Write BAB V (Penutup) | p.101 | Medium |
| **HIGH** | Write Abstrak (ID + EN) | p.1 | Medium (after results) |
| **MEDIUM** | Fix Recall formula (2.25) | p.50 | Trivial — change FP to FN |
| **MEDIUM** | Fix duplicate equation 3.29 | p.91 | Trivial — renumber |
| **MEDIUM** | Fix "tesis" → "skripsi" in Kata Pengantar | p.2 | Trivial |
| **LOW** | Renumber HTML tables 3.13/3.14 → 3.12/3.13 | HTML files | Trivial |
| **LOW** | Fill Daftar Lampiran | p.11 | After completion |
| **LOW** | Fill Halaman Pernyataan details | p.4-6 | Tempat/alamat/no telp |

---

## 8. What's Already Good

- BAB I (p.1-4): Complete with 3 research questions, 3 objectives, 5 benefits, clear scope
- BAB II (p.5-63): Comprehensive literature review with proper citations, tables, figures
- BAB III (p.64-99): Architecture descriptions match code exactly, proper diagrams and manual calculations present, hyperparameters verified against config.yaml
- All figures present: 9 Gambar in BAB III (flowchart, sample images, spectral masking, FFT comparison, 4 architecture diagrams, LR curve)
- All tables present: 13 Tabel in BAB III
- Equation numbering consistent (except the 3.29 duplicate)
- Daftar Pustaka has references (42+ entries)
