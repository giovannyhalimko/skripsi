# Full Document Analysis — Skripsi v2 (docx → md)

**Date:** 2026-03-17
**Source file:** `documents/Metode Peningkatan Deteksi Deepfake ... (2).docx`
**Converted to:** `documents/Metode Peningkatan Deteksi Deepfake ..._v2.md`
**Scope:** Full document check against reviewer feedback, formatting rules, [perlu isi] markers, and previous analyses
**Previous analyses referenced:**
- `BAB2_Analysis_..._2026-03-05_1200.md`
- `BAB_III_vs_Code_Cross_Check_2026-03-14_1040.md`
- `Actions_Taken_..._2026-03-05.md`
- `Citation_Analysis_..._2026-03-05_1600.md`

---

## SECTION A: [PERLU ISI] — Content Gaps

### A.1 `[perlu isi]` at line 665 — Pendekatan Deteksi Deepfake intro
**Location:** `## Pendekatan Deteksi Deepfake` (line 663)
**Issue:** The section immediately shows `[perlu isi]` then jumps to `### Deteksi Berbasis Domain Spasial`.
**Action:** Write 1–2 introductory sentences providing context: "Bagian ini membahas tiga pendekatan utama deteksi deepfake: berbasis domain spasial, berbasis domain frekuensi, dan pendekatan hybrid yang menggabungkan keduanya."

### A.2 `[perlu isi]` at line 735 — Frequency Domain Analysis intro
**Location:** `## Frequency Domain Analysis` (line 733)
**Issue:** The section immediately shows `[perlu isi]` then jumps to `### Konsep Domain Frekuensi`.
**Action:** Write 1–2 introductory sentences: "Bagian ini membahas konsep analisis domain frekuensi, transformasi Fourier, serta peran artefak frekuensi dalam mendeteksi citra deepfake."

---

## SECTION B: RECALL FORMULA BUG — CRITICAL

### B.1 Recall definition formula is WRONG (line 1551)
**Current:** `$$Recall = \frac{TP}{TP + FP}$$`
**Correct:** `$$Recall = \frac{TP}{TP + FN}$$`
**Note:** The calculation example at line 1641 uses the CORRECT formula (TP/(TP+FN)). Only the definition formula is wrong.
**Priority:** CRITICAL — this was flagged in the previous analysis (2026-03-05) as fixed, but it persists in this docx version.

---

## SECTION C: BAB III IS A SKELETON — CRITICAL

BAB III (starting line 1855) is largely an **outline/instruction template**, NOT actual content. It contains ~16 instances of instruction markers like "Tuliskan:", "Jelaskan:", "Isi yang ditulis:", etc.

**Lines with instruction text (NOT actual prose):**
| Line | Instruction |
|------|-------------|
| 1917 | "Isi yang ditulis:" |
| 1929 | "Yang bisa dijelaskan:" |
| 1966 | "Jelaskan Alasan pemilihan dataset:" |
| 1978 | "Tuliskan:" |
| 1992 | "Tegaskan: ..." |
| 1996 | "Isi yang ditulis:" |
| 2010 | "Tambahkan kalimat kuat:" |
| 2046 | "Ini **inti skripsi**, tulis DETAIL." |
| 2062 | "Tekankan:" |
| 2070 | "Ini bagian **nilai jual skripsi**." |
| 2072 | "Tuliskan:" |
| 2084 | "Jelaskan kenapa:" |
| 2094 | "Isi ringkas:" |
| 2104 | "Jelaskan:" |
| 2136 | "Tuliskan:" |
| 2148 | "Dari notebook:" |
| 2162 | "Jelaskan:" |
| 2180 | "Tuliskan metrik yang dipakai:" |
| 2188 | "Jelaskan:" |

**Sections affected (all have skeleton/bullet-point structure, NOT proper prose):**
- 3.1 Kerangka Umum Penelitian — **partial content + instructions** (lines 1857–1938)
- 3.2 Dataset dan Sumber Data — **mostly bullet instructions** (lines 1940–2026)
- 3.3 Tahapan Preprocessing Data — **instruction markers** (lines 2028–2088)
- 3.4 Arsitektur Model yang Diusulkan — **instruction markers** (lines 2090–2130)
- 3.5 Strategi Pelatihan Model — **instruction markers** (lines 2132–2174)
- 3.6 Metode Evaluasi Model — **1 line of content + instructions** (lines 2176–2202)

**Priority:** CRITICAL — BAB III needs to be fully rewritten as proper prose. The previous analysis (2026-03-14) checked a *different* BAB III version (`BAB_III_Metodologi_Penelitian.md`) which was rated ~90% complete. This docx version appears to be an older draft that was never updated.

**Reference:** The fully-written BAB III exists at `deepfake_hybrid/documents/BAB_III_Metodologi_Penelitian.md` — content from that file should be ported into this document.

---

## SECTION D: BAB IV & BAB V ARE TEMPLATE PLACEHOLDERS

- **BAB IV (lines 2204–2212):** Contains only the template instruction text from Pedoman Skripsi, no actual results.
- **BAB V (lines 2214–2220):** Contains only the template instruction text, no actual conclusions.
- **Priority:** Expected — these haven't been written yet. But the template text should eventually be replaced.

---

## SECTION E: FORMATTING ISSUES (Reviewer Checklist)

### E.1 Bullet points used instead of numbered lists
**Rule:** "Jangan menggunakan simbol bullet → ganti jadi 1, 2, 3, dst."
**Violations found:**
- Lines 1885–1889: BAB III section "FFT sebagai Saluran Tambahan" uses `- **...**:` dash bullets.
**Action:** Convert to numbered list (1., 2., 3.).

### E.2 English/foreign terms NOT italicized in section headings
**Rule:** "Bahasa inggris/asing dibuat cetak miring (termasuk pada judul subbab, nama gambar, maupun nama tabel)"
**Violations (headings with unitalicized English terms):**

| Line | Current Heading | Should Be |
|------|----------------|-----------|
| 667 | `### Deteksi Berbasis Domain Spasial` | `### Deteksi Berbasis Domain *Spasial*` |
| 677 | `### Deteksi Berbasis Domain Frekuensi` | `### Deteksi Berbasis *Domain* Frekuensi` |
| 687 | `### Perbandingan Domain Spasial dengan Domain Frekuensi` | needs italics on Domain Spasial/Frekuensi |
| 715 | `### Pendekatan Hybrid Domain Spasial-Frekuensi` | `### Pendekatan *Hybrid* Domain Spasial-Frekuensi` |
| 733 | `## Frequency Domain Analysis` | `## *Frequency Domain Analysis*` |
| 737 | `### Konsep Domain Frekuensi` | OK (frekuensi is Indonesian loan word) |
| 811 | `### Peran Frequency Domain Analysis dalam Deteksi Deepfake` | italicize *Frequency Domain Analysis* and *Deepfake* |
| 831 | `## Spectral Distortions dalam Deteksi Deepfake` | `## *Spectral Distortions* dalam Deteksi *Deepfake*` |
| 909 | `## Spectral Dropoff` | `## *Spectral Dropoff*` |
| 929 | `## Periodic Noise dalam Domain Frekuensi` | `## *Periodic Noise* dalam Domain Frekuensi` |
| 933 | `### Definisi dan Karakteristik Periodic Noise` | `### Definisi dan Karakteristik *Periodic Noise*` |
| 983 | `## Warping dalam Domain Frekuensi` | `## *Warping* dalam Domain Frekuensi` |
| 1003 | `## Deep Learning` | `## *Deep Learning*` |
| 1011 | `### Arsitektur Dasar Deep Learning` | `### Arsitektur Dasar *Deep Learning*` |
| 1017 | `### Peran Deep Learning dalam Pembuatan Deepfake` | italicize both |
| 1023 | `### Peran Deep Learning dalam Deteksi *Deepfake*` | *Deep Learning* also needs italics |
| 1029 | `### Convolution Neural Network (CNN)` | `### *Convolution Neural Network* (CNN)` |
| 1063 | `### Depthwise Separable Convolution` | `### *Depthwise Separable Convolution*` |
| 1079 | `### Depthwise Convolution` | `### *Depthwise Convolution*` |
| 1087 | `### Pointwise Convolution` | `### *Pointwise Convolution*` |
| 1095 | `### Kompleksitas Depthwise Separable Convolution` | italicize English term |
| 1105 | `### Relevansi Depthwise Separable Convolution pada Deteksi Deepfake` | italicize |
| 1121 | `### Integrasi dengan FFT sebagai Channel Tambahan` | `### Integrasi dengan FFT sebagai *Channel* Tambahan` |
| 1149 | `## XceptionNet` | `## *XceptionNet*` |
| 1153 | `### Arsitektur XceptionNet` | `### Arsitektur *XceptionNet*` |
| 1171 | `### Transfer Learning pada XceptionNet` | `### *Transfer Learning* pada *XceptionNet*` |
| 1179 | `### Keunggulan XceptionNet dalam Deteksi Deepfake` | italicize both |
| 1207 | `## FaceForensics` | `## *FaceForensics*` |
| 1313 | `## Celeb-DF` | `## *Celeb-DF*` |
| 1335 | `## Analisis Citra` | OK |
| 1343 | `## Analisis Video` | OK |
| 1351 | `## Preprocessing` | `## *Preprocessing*` |
| 1453 | `## Optimasi Model` | OK |
| 1501 | `## Metrik Evaluasi Model` | OK |
| 1507 | `### Confusion Matrix` | `### *Confusion Matrix*` |
| 1531 | `### Accuracy` | `### *Accuracy*` |
| 1539 | `### Precision` | `### *Precision*` |
| 1547 | `### Recall` | `### *Recall*` |
| 1555 | `### F1-Score` | `### *F1-Score*` |
| 1563 | `### AUC (Area Under the ROC Curve)` | `### AUC (*Area Under the ROC Curve*)` |
| 1701 | `## Cross Dataset Generalization` | `## *Cross Dataset Generalization*` |
| 1715 | `## Cross-GAN pada Deteksi Deepfake` | `## *Cross-GAN* pada Deteksi *Deepfake*` |

**Note:** This is extensive. Many headings need English terms to be wrapped in `*...*` for italics. The body text already italicizes these terms correctly in most places — it's the headings that are inconsistent.

### E.3 Sections that jump directly to subsections without intro paragraph
**Rule:** "setelah judul Bab atau Subbab, harus ada setidaknya satu atau dua kalimat pengantar sebelum langsung melompat ke anak subbab"
**Violations found:**

| Line | Section | Issue |
|------|---------|-------|
| 663 | `## Pendekatan Deteksi Deepfake` | → `[perlu isi]` → immediately jumps to `### Deteksi Berbasis Domain Spasial` |
| 733 | `## Frequency Domain Analysis` | → `[perlu isi]` → immediately jumps to `### Konsep Domain Frekuensi` |
| 831 | `## Spectral Distortions dalam Deteksi Deepfake` | Has intro ✅ |
| 929 | `## Periodic Noise dalam Domain Frekuensi` | Has intro ✅ (line 931) |
| 983 | `## Warping dalam Domain Frekuensi` | Has intro ✅ |
| 1003 | `## Deep Learning` | Has intro ✅ |
| 1029 | `### Convolution Neural Network (CNN)` | Has intro ✅ |
| 1149 | `## XceptionNet` | Has intro ✅ |
| 1207 | `## FaceForensics` | Has intro ✅ |
| 1313 | `## Celeb-DF` | Has intro ✅ |
| 1351 | `## Preprocessing` | Has intro ✅ |
| 1453 | `## Optimasi Model` | Has intro ✅ |
| 1501 | `## Metrik Evaluasi Model` | Has intro ✅ |
| 1701 | `## Cross Dataset Generalization` | Has intro ✅ |
| 1715 | `## Cross-GAN pada Deteksi Deepfake` | Has intro ✅ |
| 1773 | `## Dasar Pemilihan Metode` | Has intro ✅ |
| 1857 | `## Kerangka Umum Penelitian` (BAB III) | Has intro ✅ (but skeleton) |

**Only 2 violations** — both are the `[perlu isi]` sections. Most sections already comply.

### E.4 Math equations without numbering
**Rule:** "Setiap persamaan matematika perlu diberikan nomor persamaan di posisi kanan → lihat penulisan di Panduan TA"
**Equations found without numbers:**

| Line | Equation |
|------|----------|
| 1535 | Accuracy formula |
| 1543 | Precision formula |
| 1551 | Recall formula |
| 1559 | F1-Score formula |
| 1569 | TPR formula |
| 1573 | FPR formula |
| 1611–1617 | Accuracy calculation steps |
| 1625–1631 | Precision calculation steps |
| 1641–1647 | Recall calculation steps |
| 1655–1663 | F1-Score calculation steps |

**Action:** Each definition formula should get a number, e.g., (2.1), (2.2), (2.3), etc. Calculation steps can optionally share the parent number. This is best done in the Word document directly since markdown equation numbering doesn't translate well.

### E.5 Table and figure numbering issues
- **Duplicate Gambar 2.1** in DAFTAR GAMBAR (lines 507–508): Two entries both labeled "Gambar 2.1 Distribusi Komponen Low-Frequency dan High-Frequency".
- **Tabel numbering inconsistency:** The Tabel anchors in the body (e.g., `Tabel 2.5 Struktur Confusion Matrix` at line 1519) don't match the DAFTAR TABEL listing (line 521: `Tabel 2.4 Struktur Confusion Matrix`). Several tables appear to have shifted numbers between the TOC and the body.

### E.6 Bold formatting artifacts (line 1775)
**Location:** `## Dasar Pemilihan Metode` opening paragraph
**Issue:** Stray bold markers: `video dan citra** ***deepfake*** **yang hampir ... model** **GAN.`
**Action:** Remove stray `**` bold markers. Should be normal text with *deepfake* and GAN italicized where appropriate.

---

## SECTION F: TEXT ERRORS & INCONSISTENCIES

### F.1 "tesis" instead of "skripsi" (line 227)
**Current:** "saya dapat menyelesaikan **tesis** yang berjudul"
**Correct:** "saya dapat menyelesaikan **skripsi** yang berjudul"
**Location:** KATA PENGANTAR

### F.2 Daftar Pustaka still contains previously-removed entries
The previous analysis (2026-03-05) removed 3 uncited entries from the markdown version. However, this docx version (which appears to be a separate/parallel edit) still contains them:
- **[33] Haliassos et al. (2021)** — "Lips Don't Lie" — never cited in body
- **[34] Akinrogunde et al. (2025)** — energy consumption prediction — irrelevant
- **[42] Robbins & Monro (1951)** — never cited in body

**Action:** Remove these 3 entries from Daftar Pustaka. Verify all remaining entries are cited in the body.

### F.3 Recall description text inconsistency (line 1553)
**Current:** "Nilai *recall* yang tinggi berarti model jarang meloloskan *deepfake*."
But the formula above shows TP/(TP+FP) which would measure precision, not recall. This text is correct for the intended recall meaning but contradicts the wrong formula. Fix the formula (see B.1).

### F.4 Table caption numbering mismatch
In the body text, tables are labeled:
- Line 1519: "Tabel 2.5 Struktur Confusion Matrix" (anchor says Tabel 2.5)
- Line 1679: "Tabel 2.6 Ringkasan Hasil Perhitungan Metrik" (anchor says Tabel 2.6)

But DAFTAR TABEL (lines 513–528) lists:
- "Tabel 2.4 Struktur Confusion Matrix"
- "Tabel 2.5 Ringkasan Hasil Perhitungan Metrik"

These are off by 1. Need to reconcile.

---

## SECTION G: CROSS-REFERENCE WITH PREVIOUS ANALYSES

### G.1 Items from BAB2 Analysis (2026-03-05) — status in this v2 docx

| # | Item | Previous Status | v2 Status |
|---|------|----------------|-----------|
| 1 | XceptionNet section filled | DONE | ✅ Present (lines 1149–1204) |
| 2 | Celeb-DF dataset added | DONE | ✅ Present (lines 1313–1332) |
| 3 | AUC/ROC Curve section | DONE | ✅ Present (lines 1563–1585) |
| 4 | Pendekatan Hybrid filled | DONE | ✅ Present (lines 715–730) |
| 5 | Perbandingan Domain Spasial vs Frekuensi | DONE | ✅ Present (lines 687–714) |
| 6 | Artefak Generatif filled | DONE | ✅ Present (lines 659–662) |
| 7 | Adam optimizer (SGD replaced) | DONE | ✅ "Optimasi Model" (lines 1453–1498) |
| 8 | Transfer Learning for XceptionNet | DONE | ✅ Present (lines 1171–1178) |
| 9 | BCEWithLogitsLoss explained | DONE | ✅ Present (lines 1493–1498) |
| 10 | Recall formula fixed | DONE previously | ❌ **STILL BROKEN** at line 1551 — TP/(TP+FP) instead of TP/(TP+FN) |
| 11 | Spectral Dropoff consolidated | DONE | ✅ Appears as subsection (line 909) |
| 12 | Analisis Video temporal trim | NOT ACTIONED | ❌ Still contains LSTM/GRU/Transformer content |
| 13 | Repetitive GAN upsampling narration | NOT ACTIONED | ❌ Still repetitive |

### G.2 Items from BAB III Cross-Check (2026-03-14) — status in this v2 docx

The cross-check was done against a **fully-written BAB III** (`BAB_III_Metodologi_Penelitian.md`). This v2 docx has a **skeleton BAB III** that does not reflect that work. The fully-written BAB III content needs to be ported into the Word document.

### G.3 Items from Citation Analysis (2026-03-05) — status in this v2 docx

| # | Item | v2 Status |
|---|------|-----------|
| 1 | SpecXNet removed from early fusion | ✅ Not present in early fusion paragraph |
| 2 | FSBI removed from late fusion | ✅ Not present |
| 3 | FSBI removed from XceptionNet backbone | ✅ Not present |
| 4 | XceptionNet accuracy updated | ⚠️ Still says "96–99%" in Table 2.8 (line 1822) but text may have detail. Check. |
| 5 | Uncited Daftar Pustaka entries removed | ❌ [33], [34], [42] still present |

---

## SECTION H: PRIORITY ACTION ITEMS (SORTED)

### CRITICAL (Must Fix Before Submission)

| # | Item | Location | Effort |
|---|------|----------|--------|
| 1 | **Fix Recall formula:** TP/(TP+FP) → TP/(TP+FN) | Line 1551 | Trivial |
| 2 | **Port BAB III content** from `BAB_III_Metodologi_Penelitian.md` into the Word doc | Lines 1855–2202 | HIGH |
| 3 | **Fill [perlu isi]** — Pendekatan Deteksi Deepfake intro | Line 665 | Low |
| 4 | **Fill [perlu isi]** — Frequency Domain Analysis intro | Line 735 | Low |
| 5 | **Fix "tesis" → "skripsi"** in KATA PENGANTAR | Line 227 | Trivial |

### HIGH (Should Fix)

| # | Item | Location | Effort |
|---|------|----------|--------|
| 6 | **Italicize English terms in ALL headings** | ~40 headings (see E.2) | Medium |
| 7 | **Remove 3 uncited Daftar Pustaka entries** | [33], [34], [42] | Low |
| 8 | **Add equation numbers** to all math formulas | Section 2.17 (~10 equations) | Medium (in Word) |
| 9 | **Fix bold formatting artifacts** in Dasar Pemilihan Metode opening | Line 1775 | Trivial |
| 10 | **Replace bullet points with numbered lists** in BAB III | Line 1885–1889 | Trivial |
| 11 | **Fix duplicate Gambar 2.1** in DAFTAR GAMBAR | Lines 507–508 | Trivial |
| 12 | **Reconcile table numbering** between DAFTAR TABEL and body | Lines 513–528 vs body | Low |

### MEDIUM (Should Fix When Possible)

| # | Item | Location | Effort |
|---|------|----------|--------|
| 13 | Trim Analisis Video temporal content (LSTM/GRU/Transformer) | ~line 1343 | Low |
| 14 | Consolidate repetitive GAN upsampling narration | Multiple sections | Medium |
| 15 | Write actual BAB IV (Hasil dan Pembahasan) content | Lines 2204–2212 | HIGH |
| 16 | Write actual BAB V (Penutup) content | Lines 2214–2220 | Medium |

### LOW (Nice to Have)

| # | Item |
|---|------|
| 17 | Add Abstrak content (currently template) |
| 18 | Complete DAFTAR LAMPIRAN (currently empty) |
| 19 | Verify all 42 Daftar Pustaka entries are cited and correct |
| 20 | Ensure Gambar numbering is sequential and referenced in text |

---

## SECTION I: WHAT IS ALREADY GOOD (No Action Needed)

1. **BAB I (Pendahuluan):** Complete and well-structured — Latar Belakang, Rumusan Masalah, Tujuan, Manfaat, Ruang Lingkup all present with proper prose.
2. **BAB II (Kajian Literatur):** Substantially complete. All critical gaps from the 2026-03-05 analysis have been addressed (XceptionNet, Celeb-DF, AUC, Hybrid, Adam, etc.).
3. **Most subsections have intro paragraphs** before jumping to sub-subsections — only 2 violations found.
4. **Numbered lists (1, 2, 3)** are used consistently throughout BAB I and BAB II — only 1 bullet violation in BAB III.
5. **English terms in body text** are generally italicized correctly.
6. **Citations use IEEE numeric format** [1], [2], etc. consistently.
7. **Table captions** use "Tabel X.Y" format positioned at bottom (implied by anchors).
8. **Cross-dataset and Cross-GAN sections** are thorough and well-cited.
