# Actions Taken — Metode Peningkatan Deteksi Deepfake

**Date:** 2026-03-05
**Scope:** All edits applied to the skripsi document and supporting files across two analysis sessions
**Document:** `deepfake_hybrid/documents/Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi.md`

---

## Session 1: BAB II Analysis & Content Generation

Source: `analyze/BAB2_Analysis_Metode_Peningkatan_Deteksi_Deepfake_2026-03-05_1200.md`

### Priority Item 1: XceptionNet Section (SANGAT TINGGI) — DONE
- Filled `## XceptionNet` with full architecture description (Entry Flow, Middle Flow, Exit Flow)
- Filled `### Arsitektur XceptionNet` with detailed layer breakdown (36 convolutional layers)
- Filled `### Keunggulan XceptionNet dalam Deteksi Deepfake` with deepfake-specific advantages
- Added transfer learning context (ImageNet pretraining)

### Priority Item 2: Celeb-DF Dataset (SANGAT TINGGI) — DONE
- Added `## Celeb-DF` section with dataset composition, manipulation techniques, and cross-dataset relevance

### Priority Item 3: AUC / ROC Curve (TINGGI) — DONE
- Added `### AUC (Area Under the ROC Curve)` subsection to Metrik Evaluasi
- Included ROC curve concept, AUC interpretation, and relevance for deepfake detection

### Priority Item 4: Pendekatan Hybrid (SANGAT TINGGI) — DONE
- Filled `### Pendekatan Hybrid Domain Spasial-Frekuensi` with:
  - Early fusion concept (4-channel RGB+FFT)
  - Late fusion / two-branch concept (XceptionNet + FreqCNN → concat)
  - Related works (SpecXNet, F3-Net)

### Priority Item 5: FreqCNN (TINGGI) — DONE
- Added FreqCNN description as frequency branch in HybridTwoBranch architecture within the hybrid section

### Priority Item 6: Adam Optimizer (TINGGI) — DONE
- Renamed SGD section to "Optimasi Model"
- Added Adam optimizer explanation (adaptive learning rate, momentum estimates)
- Kept SGD as historical context, shortened significantly

### Priority Item 7: Transfer Learning (SEDANG) — DONE
- Covered within XceptionNet section — ImageNet pretraining and fine-tuning for deepfake detection

### Priority Item 8: Binary Cross-Entropy (SEDANG) — DONE
- Added BCE loss function explanation in training methodology context

### Priority Item 9: Perbandingan Domain Spasial vs Frekuensi (SEDANG) — DONE
- Filled `### Perbandingan Domain Spasial dengan Domain Frekuensi` with comparative analysis and Table 2.9

### Priority Item 10: Artefak Generatif (SEDANG) — DONE
- Filled `### Artefak yang Dihasilkan Proses Generatif Deepfake` with artifact typology consolidation

### Revision Item 1: SGD Section — DONE
- Renamed to "Optimasi Model", refocused on Adam, shortened SGD content

### Revision Item 2: Analisis Video Temporal — NOT ACTIONED
- LSTM/GRU/Transformer content still present; user may address separately

### Revision Item 3: Energy Forecasting Reference — DONE
- Removed `(Akinrogunde, Adelakun, Theophilus, & Thomas, 2025)` from Daftar Pustaka (citation analysis session)
- Temporal CNN paragraph in the CNN section was not directly edited

### Revision Item 4: Spectral Dropoff Consolidation — DONE
- Moved Spectral Dropoff as subsection `### Spectral Dropoff` under Spectral Distortions (renumbered to 2.5.6)

### Revision Item 5: Repetitive Narration — NOT ACTIONED
- Consolidation of repeated GAN upsampling narration not performed; requires manual review

---

## Session 2: Formatting, Citations & Corrections

### A. Formatting (skripsi-format-guide.md applied)

1. **Typo fix:** Line 31 — "DEEFAKE" → "DEEPFAKE" on English cover page
2. **Section numbering:** ~90 headings numbered across entire document:
   - BAB I: 1.1–1.5
   - BAB II: 2.1–2.21 (with all sub-sections 2.x.y)
   - BAB III: 3.1–3.6 (with sub-sections)
   - BAB IV: 4.1–4.2
3. **Table of Contents updated:** Complete rewrite to match new numbering:
   - Spectral Dropoff renumbered from standalone to 2.5.6
   - All subsequent sections shifted
   - Added missing entries: Celeb-DF (2.13), XceptionNet subsections (2.11.1–2.11.3), AUC (2.18.6), BAB III subsections (3.1.x)
   - SGD → Optimasi Model
   - Removed stale page numbers

### B. Table Borderline Markers

Added 9 `> **[INSERT TABLE HERE → ...]**` markers after table captions:
- Tabel 2.1 (komponen domain frekuensi)
- Tabel 2.2 (GAN fingerprints)
- Tabel 2.3 (distorsi spektral)
- Tabel 2.4 (3x3 depthwise separable)
- Tabel 2.5 (confusion matrix)
- Tabel 2.6 (metrik evaluasi)
- Tabel 2.7 (perbandingan model CNN)
- Tabel 2.8 (spasial vs frekuensi)
- Tabel 2.9 (dasar pemilihan metode)

### C. Citation Fixes (from Citation Analysis)

Source: `analyze/Citation_Analysis_Metode_Peningkatan_Deteksi_Deepfake_2026-03-05_1600.md`

#### Fix 3.1 — SpecXNet Early Fusion Misattribution — DONE
- **Location:** Section 2.3.4 (Pendekatan Hybrid), early fusion paragraph
- **Action:** Removed `(Alam, Tanvir, & Woo, 2025)` citation
- **Reason:** SpecXNet uses DDFC with adaptive attention, not classical early fusion (4th channel)

#### Fix 3.2 — FSBI Late Fusion Misattribution — DONE
- **Location:** Section 2.3.4 (Pendekatan Hybrid), late fusion paragraph
- **Action:** Removed `(Hasanaath, Luqman, Katib, & Anwar, 2023)` citation
- **Reason:** FSBI uses single-pipeline with DWT, not a two-branch architecture

#### Fix 3.3 — FSBI XceptionNet Backbone Claim — DONE
- **Location:** Section 2.11.3 (Keunggulan XceptionNet dalam Deteksi Deepfake)
- **Action:** Removed `dan FSBI (Hasanaath, Luqman, Katib, & Anwar, 2023)` from XceptionNet backbone list
- **Reason:** FSBI uses EfficientNet-B5, not XceptionNet

#### Fix 3.4 — XceptionNet Accuracy Range Incomplete — DONE
- **Location:** Section 2.11.3 and Table 2.7
- **Action in text:** Changed `96--99%` → detailed `99,26% (raw), 95,73% (HQ), ~81% (LQ/c40)` with caveat about compression impact
- **Action in Table 2.7 HTML:** Changed `96&ndash;99%` → `95,73&ndash;99,26% (HQ&ndash;Raw)`

#### Fix 3.5 — EfficientNet in Rössler Citation — DONE
- **Location:** Section 2.11.3
- **Action:** Removed "EfficientNet" from the list of models compared in Rössler et al. (2019)
- **Reason:** EfficientNet was not tested in the FaceForensics++ paper

#### Fix 3.6 — Rana et al. Taxonomy — NOT ACTIONED
- **Status:** Minor issue. Rana et al. citation is not wrong, just slightly overstated. Left as-is.

#### Fix 3.7 — FSBI Uses DWT Not FFT — PARTIALLY DONE
- **Action taken:** Removed FSBI from FFT-specific contexts (Section 2.10.5 and 2.11.3)
- **Action NOT taken:** Did not add explicit "FSBI uses DWT" clarification text anywhere. FSBI is no longer cited in FFT-specific claims, so the misrepresentation is resolved by removal.

#### Fix 3.8 — F3-Net Uses DCT Not FFT — NOT ACTIONED
- **Status:** Minor. Qian et al. is accurately cited as two-branch architecture. No explicit FFT claim was made for F3-Net. Left as-is.

### D. Section 2.21.2 Fix — DONE
- **Location:** Section 2.21.2 (Dasar Pemilihan Metode), comparison text
- **Action:** Changed `*EfficientNet*` → `*MesoNet*` in a comparison paragraph
- **Reason:** The comparison context was about lightweight models; MesoNet is the correct comparator

### E. Table 2.7 HTML Update — DONE
- **File:** `deepfake_hybrid/documents/table/tabel_2_7_perbandingan_model_cnn.html`
- XceptionNet accuracy: `96&ndash;99%` → `95,73&ndash;99,26% (HQ&ndash;Raw)`
- Caption: added `Chollet, 2017` to source list

### F. Daftar Pustaka Removals — DONE

Three entries removed for violating format rule "every Daftar Pustaka entry MUST be cited in body":

1. **Akinrogunde, O., Adelakun, A., Theophilus, A., & Thomas, O. V. (2025)** — "Harnessing CNN for Enhanced Load and Energy Consumption Prediction" — irrelevant to deepfake detection, never cited
2. **Haliassos, A., Vougioukas, K., Petridis, S., & Pantic, M. (2021)** — "Lips Don't Lie" — never cited in document body
3. **Robbins, H., & Monro, S. (1951)** — "A Stochastic Approximation Method" — never cited in document body

---

## Items NOT Actioned (User Action Required)

| # | Item | Reason |
|---|------|--------|
| 1 | Download missing PDFs: Kingma & Ba (2015), Li et al. (2020) | User will handle |
| 2 | Remove/cite Howard 2017.pdf and Sifre 2014.pdf from thesis_reference/ | User decision needed |
| 3 | Analisis Video temporal content trim (LSTM/GRU/Transformer) | Not requested in this session |
| 4 | Consolidate repeated GAN upsampling narration | Requires significant manual review |
| 5 | F3-Net/DCT clarification | Minor, no explicit FFT claim exists for F3-Net |
| 6 | Rana et al. taxonomy nuance | Minor, citation is not wrong |

---

## Removed Citations Summary (for Word document mirroring)

The following citations/references were **removed** from the markdown and should be removed from the Word document:

### From Document Body:
1. `(Alam, Tanvir, & Woo, 2025)` — removed from Section 2.3.4 early fusion paragraph
2. `(Hasanaath, Luqman, Katib, & Anwar, 2023)` — removed from Section 2.3.4 late fusion paragraph
3. `dan FSBI (Hasanaath, Luqman, Katib, & Anwar, 2023)` — removed from Section 2.11.3 XceptionNet backbone list
4. `EfficientNet` — removed from Rössler et al. comparison in Section 2.11.3
5. `*EfficientNet*` → changed to `*MesoNet*` in Section 2.21.2

### From Daftar Pustaka:
1. Akinrogunde et al. (2025) — full entry removed
2. Haliassos et al. (2021) — full entry removed
3. Robbins & Monro (1951) — full entry removed

**Note:** The citations for Alam, Tanvir, & Woo (2025) and Hasanaath et al. (2023) were only removed from *specific incorrect contexts*. They are still cited correctly elsewhere in the document and should remain in Daftar Pustaka.
