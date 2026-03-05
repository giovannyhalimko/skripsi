# BAB II Citation Gaps & Reference Recency Analysis

**Date:** 2026-03-05
**Document:** `deepfake_hybrid/documents/Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi.md`

---

## 1. Reference Recency Check

**Requirement (Pedoman Skripsi 2025):** >= 70% of references from the last 5 years (2021–2026)

### Current Status: DOES NOT MEET THRESHOLD

| Metric | Count |
|--------|-------|
| Total references | 37 |
| Dated references | 34 |
| Undated ("t.thn.") | 3 |
| From 2021–2026 | **16 (47.1%)** |
| From before 2021 | **18 (52.9%)** |
| Gap to 70% | **~10 more recent refs needed** |

### References from 2021–2026 (16)

| Author | Year |
|--------|------|
| Aduwala et al. | 2021 |
| Alam, Tanvir, & Woo | 2025 |
| Andira & Susila | 2024 |
| Chadha et al. | 2021 |
| Dai et al. | 2021 |
| Haq | 2021 |
| Hasanaath et al. | 2023 |
| Kim et al. | 2025 |
| Luo & Wang | 2025 |
| Ma et al. | 2025 |
| Mejri et al. | 2021 |
| Nguyen et al. | 2021 |
| Rana et al. | 2022 |
| Rao & Uehara | 2025 |
| Tan et al. | 2024 |
| (need 1 more to count — only 15 unique above) | — |

### References from before 2021 (18)

| Author | Year | Replaceable? |
|--------|------|-------------|
| Afchar et al. (MesoNet) | 2018 | No — seminal work |
| Bottou (SGD) | 2012 | Yes — could use a 2021+ optimization survey |
| Chollet (XceptionNet) | 2017 | No — seminal work |
| Commons (Wikimedia) | 2018 | Yes — replace with academic source |
| Durall et al. | 2020 | No — key frequency domain paper |
| Easton Jr. | 2010 | Yes — could use newer textbook |
| Gonzalez & Woods | 2018 | Borderline — standard textbook |
| Goodfellow et al. (DL textbook) | 2016 | Borderline — foundational |
| Guera & Delp | 2018 | Yes — could use more recent temporal detection paper |
| Giudice et al. | t.thn. | Needs year clarification |
| He et al. (ResNet) | 2015 | No — seminal work |
| Karras et al. (ProGAN) | 2018 | No — seminal work |
| LeCun et al. | t.thn. | Needs year clarification |
| Odena et al. (checkerboard) | 2016 | No — seminal work |
| Oppenheim et al. (DSP) | 1989 | Yes — could use newer DSP textbook |
| P. & S. (Korshunov) | 2019 | Yes — could use more recent survey |
| Qian et al. (F3-Net) | 2020 | No — key related work |
| Rossler et al. (FF++) | 2019 | No — key dataset paper |
| Ruder (optimization) | 2017 | Yes — could use 2021+ reference |
| Sabir et al. | 2019 | Yes — could use more recent temporal paper |
| Stack Overflow | t.thn. | Must replace — not academic |
| Zhang et al. | 2019 | No — key frequency fingerprint paper |

### Strategy to Reach 70%

To reach 70% of ~37 refs = need 26 recent refs. Currently have 16. Options:

**A. Add ~10 new recent (2021–2026) references** — the uncited paragraphs below provide natural insertion points

**B. Replace older references where possible:**
- Bottou (2012) → recent optimization survey
- Easton Jr. (2010) → newer image processing textbook
- Oppenheim et al. (1989) → newer DSP reference
- Guera & Delp (2018) → recent temporal detection paper
- Sabir et al. (2019) → recent temporal detection paper
- Korshunov (2019) → recent deepfake threat survey
- Commons (2018) / Stack Overflow → academic sources

**C. Combination** — most practical: add ~6-7 new recent refs via uncited paragraphs + replace ~3-4 old refs

---

## 2. Uncited Claims in BAB II (Citation Opportunities)

36 issues found. Each is a potential insertion point for a new (preferably recent) citation.

### CRITICAL — Must Fix

| # | Section | Line | Issue | Suggested Citation |
|---|---------|------|-------|--------------------|
| 1 | 2.1.2 | ~603 | "teknik deteksi konvensional yang hanya mengandalkan informasi spasial tidak lagi memadai" — entire paragraph uncited | (Rana et al., 2022) or recent survey |
| 2 | 2.2 | ~607 | GAN "diperkenalkan pada tahun 2014" — missing original GAN paper | **ADD: Goodfellow et al. (2014)** — but this is pre-2021 |
| 3 | 2.5.6 | ~895 | Dangling ` .` where citation was intended — spectral distribution pattern claim | (Gonzalez & Woods, 2018) or recent image stats paper |
| 4 | 2.8 | ~991 | "Menurut *Chadha et al*" but cites **(Guidice, Guarnera, & Battiato)** — citation MISMATCH | Fix: change to (Chadha et al., 2021) |
| 5 | 2.6.3 | ~957 | Stack Overflow cited as source — **not academic** | Replace with (Gonzalez & Woods, 2018) or academic source |
| 6 | 2.21 | ~1765-1769 | Opening paragraphs entirely uncited despite evaluative claims about prior research | (Rana et al., 2022; Durall et al., 2020) |

### FORMAT — Inconsistent Citation Style

| # | Section | Line | Issue |
|---|---------|------|-------|
| 7 | 2.3.2 | ~657 | Uses [7], [8], [14] instead of (Author, Year) |
| 8 | 2.3.2 | ~659 | Uses [17], [18], [19] instead of (Author, Year) |
| 9 | 2.18.8 | ~1687 | Uses [12, 20] instead of (Author, Year) |

### HIGH — Factual Claims Needing Citations

| # | Section | Line | Claim | Suggested Citation (prefer recent) |
|---|---------|------|-------|------------------------------------|
| 10 | 2.2.2 | ~621 | Interpolation definition and frequency characteristics | (Gonzalez & Woods, 2018) + (Durall et al., 2020) |
| 11 | 2.2.3 | ~629 | Artifact classification into 2 categories | (Rana et al., 2022) |
| 12 | 2.3.2 | ~661 | Concluding paragraph on FDA as complement to spatial methods | (Durall et al., 2020; Rana et al., 2022) |
| 13 | 2.3.4 | ~699 | Early fusion description (4-channel RGB+FFT) — no citation after SpecXNet was removed | **ADD: recent early fusion paper** |
| 14 | 2.4.2 | ~747-769 | FFT formulas (DFT, inverse DFT, magnitude) | (Gonzalez & Woods, 2018) or (Oppenheim et al., 1989) |
| 15 | 2.6 | ~915 | Periodic noise intro paragraph — frequency fingerprint claims | (Zhang et al., 2019) + (Durall et al., 2020) |
| 16 | 2.8.1 | ~997 | Deep learning fundamentals cited only as (Rossler et al., 2019) — wrong source | (Goodfellow, Bengio, & Courville, 2016) or (LeCun et al.) |
| 17 | 2.8.1 | ~999 | Feature hierarchy (edges → complex patterns) — no citation | (LeCun, Bengio, & Hinton) or recent DL textbook |
| 18 | 2.10.3 | ~1077 | Computational complexity formulas — no citation | (Chollet, 2017) |
| 19 | 2.10.4 | ~1101 | XceptionNet effectiveness claims (points 1, 3, 5) — no citations | (Chollet, 2017) + (Rossler et al., 2019) |
| 20 | 2.11.1 | ~1153 | ReLU and batch normalization in XceptionNet — no citation | (Chollet, 2017) |
| 21 | 2.11.2 | ~1161 | ImageNet normalization values (mean/std) — no citation | PyTorch docs or (He et al., 2015) |
| 22 | 2.12.1 | ~1211 | FF++ compression levels (RAW, HQ, LQ) — no citation | (Rossler et al., 2019) |
| 23 | 2.12.2 | ~1241 | Artifact characteristics per manipulation method — no citation | (Rossler et al., 2019) |
| 24 | 2.12.3 | ~1257 | FF++ selection reasons (points 1,2,4,5) — no citations | (Rossler et al., 2019) |
| 25 | 2.12.4 | ~1279 | FFT training claims (spectral instability, amplitude anomalies) — no citation | (Durall et al., 2020) |
| 26 | 2.16.1 | ~1353 | Face alignment paragraph — no citation | Recent face detection paper or (Rossler et al., 2019) |
| 27 | 2.16.1 | ~1357 | "224x224 is standard size" — no citation | (He et al., 2015) or (Chollet, 2017) |
| 28 | 2.16.2 | ~1391 | "GAN cannot maintain natural image statistics" — no citation | (Durall et al., 2020) |
| 29 | 2.16.2 | ~1413 | fftshift formula — no citation | (Gonzalez & Woods, 2018) |
| 30 | 2.16.2 | ~1419 | Artifact causes list (upsampling, filter instability, blending, compression) — no citation | (Durall et al., 2020; Odena et al., 2016) |
| 31 | 2.17.3 | ~1470 | Adam advantages for hybrid architectures — no citation | **ADD: Kingma & Ba (2015)** — missing PDF |
| 32 | 2.17.3 | ~1472 | Bias correction claim — no citation | **ADD: Kingma & Ba (2015)** — missing PDF |
| 33 | 2.18.1 | ~1509 | FN "paling berbahaya" claim — no citation | (Rana et al., 2022) or forensics reference |
| 34 | 2.18.6 | ~1563 | AUC stability on imbalanced datasets — no citation | ML textbook or recent evaluation methods paper |
| 35 | 2.19 | ~1695 | "domain shift" attributed only to Durall et al. — not accurate source for this concept | **ADD: recent domain adaptation paper** |

### BORDERLINE — Author's Own Framing (Optional)

| # | Section | Line | Note |
|---|---------|------|------|
| 36 | 2.1 | ~591 | Research scope definition — could add (Rana et al., 2022) |
| 37 | 2.3.4 | ~709 | Research plan statement — author's own, acceptable without citation |

---

## 3. Recommended New References to Add

These would simultaneously fix uncited paragraphs AND improve the recency ratio. Priority on 2021–2026 sources:

| # | Reference | Year | Fixes Issues # | Topic |
|---|-----------|------|----------------|-------|
| 1 | **Kingma & Ba** — Adam optimizer | 2015 | 31, 32 | Already needed (missing PDF) — but pre-2021 |
| 2 | **Goodfellow et al.** — GAN original paper | 2014 | 2 | Needed but pre-2021 |
| 3 | **Recent domain adaptation survey (2022+)** | 2022+ | 35 | Domain shift concept |
| 4 | **Recent deepfake detection survey (2023+)** | 2023+ | 1, 6, 12, 33, 34 | General deepfake detection claims |
| 5 | **Recent early fusion paper (2022+)** | 2022+ | 13 | Multi-modal fusion for deepfake |
| 6 | **Recent AUC/evaluation methods paper** | 2022+ | 34 | Evaluation metrics |
| 7 | **Recent face detection/alignment paper** | 2022+ | 26 | Face preprocessing |
| 8 | **Recent GAN artifact analysis (2022+)** | 2022+ | 11, 15, 30 | GAN artifacts taxonomy |
| 9 | **Recent DL textbook/survey (2022+)** | 2022+ | 16, 17, 19 | Deep learning fundamentals |
| 10 | **Recent image processing textbook** | 2021+ | 5, 10, 14, 29 | Replace Easton Jr. (2010) / supplement Gonzalez |

Adding references 3–10 (8 new recent refs) + fixing replaceable old refs would bring the ratio to approximately:
- Current: 16 recent / 34 dated = 47%
- After: ~24 recent / ~42 dated = **57%** (still short)
- Need to be more aggressive with replacements to hit 70%

### To actually reach 70%:
With ~40 total refs, need 28 recent. Currently 16. Need **12 more recent refs** through a combination of:
- Adding ~8 new recent references (from uncited paragraphs)
- Replacing ~4 old references with recent equivalents

---

## 4. Actions Taken

None — this is a research/analysis document only. All fixes are pending user decision.
