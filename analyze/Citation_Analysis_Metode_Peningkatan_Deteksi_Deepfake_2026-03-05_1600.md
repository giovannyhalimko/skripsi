# Citation Analysis — Metode Peningkatan Deteksi Deepfake

**Date:** 2026-03-05
**Scope:** Full document (BAB I–III), with focus on generated/added sections
**Reference directory:** `/thesis_reference/`

---

## 1. Missing Reference PDFs

These citations appear in the document but have **no corresponding PDF** in `thesis_reference/`:

| Citation | Uses | Severity | Notes |
|----------|------|----------|-------|
| **(Li, Yang, Sun, & Lyu, 2020)** | 3 | **HIGH** | Celeb-DF dataset paper. Cited in section 2.13. Must be obtained. |
| **(Kingma & Ba, 2015)** | 2 | **HIGH** | Adam optimizer paper. Cited in section 2.17. Must be obtained. |
| **(Commons, 2018)** | 2 | LOW | Wikimedia Commons — web resource, no PDF expected |
| **(Stack Overflow, n.d.)** | 1 | LOW | Web resource, no PDF expected |

**Action required:** Download and add to `thesis_reference/`:
- Li, Y., Yang, X., Sun, P., & Lyu, S. (2020). Celeb-DF: A Large-scale Challenging Dataset for DeepFake Forensics.
- Kingma, D. P., & Ba, J. (2015). Adam: A Method for Stochastic Optimization.

---

## 2. Uncited PDFs in `thesis_reference/`

These PDFs exist but are **never cited** in the document body (BAB I–III):

| PDF | In Daftar Pustaka? | Action |
|-----|---------------------|--------|
| Akinrogunde et al - ...load and energy consumption prediction... | Yes | Remove from Daftar Pustaka (irrelevant to deepfake detection) |
| Haliassos et al - Lips Don't Lie... | Yes | Either cite in BAB II or remove from Daftar Pustaka |
| Howard 2017.pdf (MobileNets) | No | Remove PDF or cite if needed for depthwise separable convolution discussion |
| Sifre 2014.pdf | No | Remove PDF or cite if needed for depthwise separable convolution history |
| robbins et al - a stochastic approximation method.pdf | Yes | Remove from Daftar Pustaka (not cited in body) |

**Format guide rule:** "Every citation MUST appear in Daftar Pustaka; every Daftar Pustaka entry MUST be cited"

---

## 3. Misattributions & Inaccurate Claims (Generated Sections)

### 3.1 MEDIUM — Alam et al. (SpecXNet) cited for "Early Fusion"

**Location:** Section 2.3.4 Pendekatan Hybrid, ~line 701
**Claim:** Early fusion described as "FFT added as 4th channel" and attributed to (Alam, Tanvir, & Woo, 2025)
**Reality:** SpecXNet uses a Dual-Domain Feature Coupler (DDFC) with adaptive attention-based fusion (DFA), not classical early fusion with a 4th input channel.
**Fix:** Remove `(Alam, Tanvir, & Woo, 2025)` from the early fusion paragraph. The early fusion concept is a general technique — cite a general deep learning source or describe it without attribution to SpecXNet.

### 3.2 MEDIUM — Hasanaath (FSBI) cited for "Late Fusion / Two-Branch"

**Location:** Section 2.3.4, ~line 705
**Claim:** Late fusion / two-branch architecture attributed to (Hasanaath, Luqman, Katib, & Anwar, 2023)
**Reality:** FSBI uses a single-pipeline with DWT-enhanced self-blended images fed into EfficientNet-B5, not a two-branch architecture.
**Fix:** Remove `(Hasanaath, Luqman, Katib, & Anwar, 2023)` from the late fusion paragraph. Keep `(Qian, Yin, Sheng, Chen, & Shao, 2020)` which is accurate for two-branch (F3-Net).

### 3.3 MEDIUM — FSBI claimed to use XceptionNet backbone

**Location:** Check around line ~1189 in BAB II
**Claim:** FSBI implied to use XceptionNet as backbone
**Reality:** FSBI uses EfficientNet-B5, not XceptionNet.
**Fix:** Correct any mention of FSBI + XceptionNet. FSBI uses EfficientNet-B5.

### 3.4 MEDIUM — XceptionNet accuracy "96–99%" is incomplete

**Location:** Table 2.7 and various sections
**Claim:** XceptionNet achieves 96–99% on FaceForensics++
**Reality:** Per Rössler et al. (2019): Raw=99.26%, HQ=95.73%, **LQ=81.00%**. The "96–99%" range only covers Raw/HQ and omits the significant LQ drop.
**Fix:** Either specify "96–99% (HQ–Raw)" or note that performance drops to ~81% under heavy compression (LQ/c40).

### 3.5 LOW — EfficientNet comparison citing Rössler et al.

**Location:** Table 2.7
**Claim:** EfficientNet compared alongside other CNNs citing (Rössler, et al., 2019)
**Reality:** EfficientNet is NOT tested in the FaceForensics++ paper. The citation does not support this comparison.
**Fix:** Remove (Rössler, et al., 2019) from EfficientNet row, or add a more appropriate source.

### 3.6 LOW — Rana et al. spatial vs frequency taxonomy overstated

**Location:** Sections 2.3.1, 2.3.3, Table 2.9
**Claim:** Rana et al. (2022) cited as primary source for spatial vs frequency domain comparison
**Reality:** Rana et al.'s systematic review organizes by method type (DL, ML, statistical, blockchain), not by spatial vs frequency domain. It mentions frequency domain analysis in only 7 of 112 studies.
**Fix:** Minor — the citation is not wrong, but the document may overstate Rana et al.'s emphasis on this dichotomy. Consider adding a note or citing additional sources.

### 3.7 LOW — FSBI uses DWT, not FFT

**Location:** Various sections where Hasanaath et al. is cited alongside FFT-based methods
**Claim:** FSBI grouped with FFT-based frequency domain approaches
**Reality:** FSBI uses Discrete Wavelet Transform (DWT), not FFT.
**Fix:** When discussing FSBI alongside FFT-based approaches, clarify it uses DWT. Or simply cite it as a "frequency-domain" approach without implying it uses FFT.

### 3.8 LOW — F3-Net (Qian et al.) uses DCT, not FFT

**Location:** Section 2.3.4 late fusion paragraph
**Claim:** Qian et al. cited for two-branch frequency approach
**Reality:** F3-Net uses DCT (Discrete Cosine Transform), not FFT.
**Fix:** Accurate as a "two-branch" citation, but note it uses DCT, not FFT, if specifying the transform.

---

## 4. Verified Claims (Accurate)

These citations in generated sections were **verified against the actual PDFs**:

| Citation | Claim | Verdict |
|----------|-------|---------|
| Chollet (2017) | 36 conv layers, Entry/Middle/Exit flow, ImageNet | ✅ Fully accurate |
| Chollet (2017) | Depthwise separable convolution hypothesis | ✅ Fully accurate |
| Rössler et al. (2019) | Transfer learning from ImageNet for deepfake detection | ✅ Accurate |
| Rössler et al. (2019) | XceptionNet outperforms other tested models on FF++ | ✅ Accurate |
| Haq (2021) | Compares XceptionNet vs ResNet-50 with LBP on Celeb-DF | ✅ Accurate |
| Luo & Wang (2025) | Frequency-domain masking + spatial interaction, dual stream | ✅ Accurate |
| Tan et al. (2024) | FreqNet for generalizable frequency-aware detection | ✅ Accurate |
| Qian et al. (2020) | Two-branch architecture with cross-attention fusion | ✅ Accurate (uses DCT) |
| Durall et al. (2020) | GANs fail to reproduce spectral distributions | ✅ Accurate |
| Zhang et al. (2019) | Frequency-domain fingerprints for GAN detection | ✅ Accurate |
| Bottou (2012) | SGD mini-batch gradient updates | ✅ Accurate |
| Odena et al. (2016) | Checkerboard artifacts from transposed convolution | ✅ Accurate |

---

## 5. Complete Citation Statistics

| Metric | Count |
|--------|-------|
| Unique citations in document body | 39 |
| Citations with matching PDFs | 35 |
| Missing academic PDFs | **2** (Kingma & Ba, Li et al.) |
| Web resources (no PDF expected) | 2 |
| Uncited PDFs in thesis_reference/ | **5** |
| Issues found (medium severity) | **5** |
| Issues found (low severity) | **3** |

### Top 10 Most-Cited References

| # | Citation | Count |
|---|----------|-------|
| 1 | Durall, Keuper, & Keuper (2020) | 53 |
| 2 | Rana, Nobi, Murali, & Sung (2022) | 34 |
| 3 | Zhang, Karaman, & Chang (2019) | 34 |
| 4 | Hasanaath, Luqman, Katib, & Anwar (2023) | 32 |
| 5 | Rössler, et al. (2019) | 30 |
| 6 | Qian, Yin, Sheng, Chen, & Shao (2020) | 28 |
| 7 | Alam, Tanvir, & Woo (2025) | 27 |
| 8 | Afchar, Nozick, & Yamagishi (2018) | 21 |
| 9 | Tan, et al. (2024) | 19 |
| 10 | Chollet (2017) | 18 |

---

## 6. Priority Actions

### Critical (must fix)
1. **Add missing PDFs** to `thesis_reference/`: Kingma & Ba (2015), Li et al. (2020) — **USER ACTION REQUIRED**
2. **Fix FSBI backbone claim** — change XceptionNet → EfficientNet-B5 where FSBI is described — **DONE** (removed FSBI from XceptionNet backbone list in 2.11.3)
3. **Fix early fusion attribution** — remove SpecXNet citation from early fusion paragraph — **DONE** (removed from 2.3.4)

### Important (should fix)
4. **Fix late fusion attribution** — remove FSBI citation from two-branch/late fusion description — **DONE** (removed from 2.3.4)
5. **Clarify XceptionNet accuracy** — note that 81% on LQ compression is omitted from "96–99%" range — **DONE** (updated text to 99.26%/95.73%/~81% and Table 2.7 HTML)
6. **Remove uncited Daftar Pustaka entries** (Akinrogunde, Haliassos, Robbins) per format guide rules — **DONE** (all 3 removed)

### Minor (nice to have)
7. Clarify FSBI uses DWT, not FFT — **PARTIALLY DONE** (removed FSBI from FFT-specific contexts in 2.10.5 and 2.11.3; no explicit "FSBI uses DWT" text added since FSBI is no longer cited in FFT claims)
8. Clarify F3-Net uses DCT, not FFT — **NOT ACTIONED** (no explicit FFT claim exists for F3-Net in the document; Qian et al. is cited as "two-branch" which is accurate)
9. Add Rana et al. taxonomy nuance — **NOT ACTIONED** (minor; citation is not wrong, just slightly overstated)
10. Remove or cite Howard 2017 and Sifre 2014 PDFs — **USER ACTION REQUIRED** (PDFs still in thesis_reference/ uncited)
