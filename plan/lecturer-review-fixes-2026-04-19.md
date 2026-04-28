# Plan: Address Lecturer Review Feedback — BAB I, II, III

## Context

This plan addresses feedback from the thesis lecturer review on the skripsi "Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi." The primary document is the PDF at `documents/BAB III - Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi.pdf`. The working source for edits will be `documents/BAB_III_Tahapan_Pelaksanaan_v3.md` (BAB III) and the main thesis markdown file for BAB I.

---

## PART A — BAB I FIXES

### A1. Paragraph 2 Merger (Structure)
**Why it's a problem:** Paragraph 2 is only 2–3 sentences discussing deepfake porn as an individual threat. It's too short to stand alone (rule: 4–6 sentences per paragraph) and is thematically connected to paragraph 1's introduction of threats.
**Fix:** Merge paragraph 2 into paragraph 1 by appending the deepfake porn threat as the 4th–5th sentence of paragraph 1. Expand paragraph 1 to 5–6 sentences covering: (a) GAN capability, (b) deepfake definition, (c) original intent vs. misuse, (d) individual-level harm including deepfake porn [2], (e) societal/geopolitical harm [1].

### A2. Paragraph 5: "Sejumlah Penelitian" with Only 1 Citation (Credibility)
**Why it's a problem:** The phrase "sejumlah penelitian" (several studies) implies multiple references, but paragraph 5 only has [7] (Durall et al.). Paragraph is also only 2 sentences — below the 4-sentence minimum. This weakens the claim and fails to show the breadth of frequency-based research.
**Fix:** Expand paragraph 5 to 4–5 sentences covering three distinct frequency-based approaches: FFT (Durall et al. [7]), DCT (Giudice et al. [25]), and Wavelet (reference to be added or use existing [22] Tan et al.). Add 2–3 more citations so "sejumlah penelitian" is substantiated.

### A3. Contradiction Between Paragraphs 7 & 8 (Logical Consistency)
**Why it's a problem:**
- Paragraph 7 states: "several studies show combining two domains CAN improve generalization" with citations [10,11,12]
- Paragraph 8 states: "there is no approach that integrates both domains" as the research gap
These directly contradict each other. If studies [10,11,12] already combine the domains, the gap claim in paragraph 8 is false.
**Fix:** Rewrite paragraph 7 to say "several studies have explored combining domains, but these approaches are **not optimized specifically** for cross-dataset generalization, and most focus on in-distribution performance." Paragraph 8 then becomes: the gap is not absence of hybrid approaches, but lack of a **systematically evaluated hybrid architecture optimized for cross-dataset robustness** using FFT + XceptionNet as the specific combination.

### A4. Cross-Dataset Generalization Importance Not Explained (Motivation Gap)
**Why it's a problem:** The reviewer notes the motivation for why cross-dataset generalization matters is absent. Without this, the research rationale is incomplete — the reader doesn't understand why it's a problem if a model fails on a different dataset.
**Fix:** Add 2–3 sentences in the latar belakang (best placed at the transition between paragraph 6 and 7) explaining: In real-world forensics, deepfake detectors will encounter videos from unknown generation methods. A model that only works on the dataset it was trained on has no practical value. Cross-dataset failure has been documented [ref] and is the primary barrier to deployment.

### A5. Problem Statement Is Vague / Rumusan Masalah Are Solutions (Framing)
**Why it's a problem:** The current Rumusan Masalah read as solution statements ("Bagaimana mengembangkan...") rather than problem statements. The reviewer explicitly states the problem being solved is not visible. Additionally, RM point 2 ("Bagaimana XceptionNet dapat dimodifikasi...") has no supporting discussion in the latar belakang.
**Fix (new Rumusan Masalah — MY TAKE):**
1. Apakah model deteksi deepfake berbasis domain spasial tunggal (XceptionNet) mengalami penurunan performa yang signifikan saat diuji pada dataset yang berbeda dari data pelatihannya (cross-dataset)?
2. Apakah integrasi fitur domain frekuensi (FFT) ke dalam arsitektur XceptionNet melalui pendekatan hybrid dapat meningkatkan kemampuan generalisasi lintas dataset dibandingkan model berbasis domain spasial saja?
3. Seberapa besar kontribusi fitur frekuensi terhadap peningkatan metrik evaluasi (akurasi, presisi, recall, AUC) pada pengujian in-dataset dan cross-dataset?

These three questions (a) establish the problem clearly, (b) propose the intervention, and (c) measure outcomes — matching the tujuan without duplicating them.

### A6. Tujuan Duplicates Rumusan Masalah (Redundancy)
**Why it's a problem:** Tujuan should state what will be *produced/demonstrated*, not restate the questions.
**Fix:** Rewrite tujuan as outcome-oriented:
1. Merancang dan mengimplementasikan model hybrid XceptionNet-FFT untuk deteksi deepfake pada frame video.
2. Mengevaluasi performa model hybrid dibandingkan model berbasis domain spasial murni pada pengujian in-dataset dan cross-dataset.
3. Menganalisis kontribusi masing-masing komponen (fitur spasial vs. fitur frekuensi) terhadap kemampuan generalisasi model.

### A7. Manfaat Operasional Contradicts Ruang Lingkup (Consistency)
**Why it's a problem:** Manfaat point 4 mentions "kecepatan serta ketepatan inferensi dari FFT" (speed of inference), but Ruang Lingkup point 4 explicitly states "Penelitian tidak terfokus pada optimasi waktu inferensi secara mendalam." These directly contradict.
**Fix:** Remove speed/inference claims from Manfaat point 4. Replace with: "Menghasilkan model yang dapat dievaluasi secara sistematis sebagai dasar pengembangan sistem forensik digital lebih lanjut."

### A8. Dataset Citation with Link and Total Count (Completeness)
**Why it's a problem:** The reviewer requires citations with links to dataset sources and total dataset counts used. This is absent in latar belakang.
**Fix:** In Ruang Lingkup or Latar Belakang paragraph 1/3, add: FaceForensics++ (Rössler et al. [19], available at [link]) contains X real and X×4 fake videos across 4 manipulation methods. Celeb-DF v2 (Li et al., [ref]) contains X real and X fake videos. Add the dataset citations with URL if the citation style allows (IEEE typically uses DOI).

---

## PART B — BAB II FIXES

### B1. Dataset Criteria Not Defined (Clarity)
**Why it's a problem:** The reviewer asks: what are the criteria for selecting videos from FaceForensics++ and Celeb-DF? Just saying "taken from" is insufficient — which compression level, which manipulation methods, what resolution, what facial content criteria?
**Fix:** In BAB III section 3.2 (Dataset), add explicit criteria table:
- FaceForensics++: compression level c23 (light compression), all 4 manipulation methods (Deepfakes, Face2Face, FaceSwap, NeuralTextures), videos with detectable faces, excluding heavily occluded frames.
- Celeb-DF v2: all available videos, celebrity face swaps only.
- Add total video counts per category and total frame counts.

### B2. Missing Citations on Figures and Tables (Academic Standard)
**Why it's a problem:** Every figure and table in academic work must have a source citation if not original. Without citations, the work is academically incomplete.
**Fix:** Audit all figures and tables in BAB II:
- Table 2.1 (Perbandingan Domain): Add citations [7,8,10] in caption
- Table 2.2 (Komponen Frekuensi): Already has [7,8] — verify
- Figure 2.1 (Low/High Frequency distribution): Add proper citation
- Figure 2.2 (Frequency domain representation): Already has [21] — verify others
- All figures that are reproduced from papers need "[Source: Author, Year]" in caption

### B3. Section 2.2.3 — Add Example Artifact Frames (Visual Evidence)
**Why it's a problem:** Theory without visual examples is harder to understand. The reviewer specifically asks for example frames showing spatial and frequency domain artifacts.
**Fix:** Add after the two-category description in 2.2.3:
- Include a figure showing: (a) original face frame, (b) deepfake frame with visible spatial artifacts highlighted (blending boundary), (c) FFT magnitude spectrum of original, (d) FFT magnitude spectrum of deepfake showing checkerboard/periodic noise.
- Use example from FaceForensics++ dataset if possible (original + manipulated pair).
- Caption: "Gambar 2.X Contoh artefak domain spasial dan frekuensi pada citra deepfake [7]"

### B4. Section 2.3.4 — Two Strategies Missing Citation (Credibility)
**Why it's a problem:** The subsection introduces "dua strategi utama" (early fusion and late fusion) as facts without citing who proposed or classified these strategies.
**Fix:** Add citation after "dua strategi utama": reference Alam et al. [9] (SpecXNet, late fusion), Qian et al. [13] (frequency-aware, early fusion-like), and/or a survey paper that formalizes the taxonomy. Add at minimum [9, 18] after "dua strategi utama dalam mengintegrasikan domain spasial dan frekuensi."

### B5. Section 2.9.4 — Depthwise Separable Convolution Key Explanation Missing Ref (Credibility)
**Why it's a problem:** The explanation of depthwise separable convolution is presented as fact without citing the source where this definition comes from.
**Fix:** Ensure Chollet [6] is cited at the definition of depthwise separable convolution and at the mathematical formulation. Also add Howard et al. (MobileNets) if used — but Chollet [6] is the primary reference.

### B6. Section 2.10.1 — XceptionNet Architecture Figure Missing (Visual Clarity)
**Why it's a problem:** For a chapter that uses XceptionNet as a core component, not showing its architecture diagram means readers must imagine it. The reviewer explicitly asks for this.
**Fix:** Add figure of XceptionNet architecture (Entry flow → Middle flow → Exit flow with depthwise separable convolution blocks), cited from Chollet [6]. Caption: "Gambar 2.X Arsitektur XceptionNet [6]"

### B7. Sections 2.11.1 & 2.11.2 — No References for SE Networks (Credibility)
**Why it's a problem:** Channel Attention and SE Block architecture explanations have no citations. These are specific concepts from a published paper.
**Fix:** Add Hu et al. (2018) "Squeeze-and-Excitation Networks" citation throughout 2.11.1 and 2.11.2. Citation should appear at: definition of channel attention, SE block formula, and SE block architecture description.

### B8. Section 2.20.1 — Subsection Name Review
**Why it's a problem:** The reviewer flags this subsection name. "Mengapa Cross-GAN Sulit" may be too informal or question-form for a subsection title.
**Fix:** Rename to "Tantangan dalam Generalisasi Cross-GAN" or "Faktor Penghambat Generalisasi Cross-GAN" — descriptive noun phrase rather than question form.

### B9. Single-Paragraph Subsections → Convert to Numbered/Bulleted Points
**Why it's a problem:** Subsections with only 1 paragraph don't justify their own header level — they fragment the text unnecessarily.
**Fix:** For any 4th-level subsection with ≤1 paragraph, integrate as lettered or numbered point within the parent section. Specifically review: any sub-subsections in 2.5, 2.6, 2.7, 2.8 that have very short content.

---

## PART C — BAB III FIXES

### C1. Process Flow Not Detailed — Algorithm Explanation Missing (Depth)
**Why it's a problem:** The reviewer says the process stages lack detail. "Capture using library" is not an explanation of HOW the algorithm works. Each stage must describe the algorithmic process, not just the tool used.
**Fix (per stage):**
- **Frame extraction**: Explain WHY 5 FPS was chosen (balancing temporal coverage vs. dataset size), HOW OpenCV decodes video (frame decoding from H.264 stream), what happens when a frame is skipped (stride-based sampling logic)
- **FFT Conversion**: Already has good mathematical detail in v3 — verify it's in the final document. If not, copy from v3.
- **Face detection/alignment**: Explain Haar cascade or MTCNN detection process if used, or clarify that no face detection is applied (frame-level analysis)
- **Data splitting**: Explain stratified split at VIDEO level (not frame level) and WHY (preventing data leakage where frames from same video appear in both train and test)

### C2. No System Analysis Section (Completeness)
**Why it's a problem:** The reviewer asks: "This will be implemented with what?" There's no section describing the hardware, software stack, and system constraints.
**Fix:** Add section **3.X Lingkungan Implementasi dan Spesifikasi Sistem** containing:
- Hardware: GPU (Google Colab T4/V100 or local GPU), RAM
- OS: Linux (Colab) / Windows (local)
- Python version: 3.9
- Key dependencies with versions: PyTorch, torchvision, timm, OpenCV, NumPy, pandas, scikit-learn, matplotlib
- Training environment: Google Colab Pro with GPU acceleration, Drive mounting for dataset storage
- Estimated training time per model configuration

### C3. Total Dataset Count Per Category Not Specified (Precision)
**Why it's a problem:** The reviewer cannot verify the scale of the experiment without knowing exact numbers.
**Fix:** Add a table in BAB III section 3.2 showing:
| Dataset | Category | Total Videos | Frames Extracted (est.) | Used Samples |
|---------|----------|-------------|------------------------|--------------|
| FaceForensics++ | Real | ~1,000 | ~50,000 | per split |
| FaceForensics++ | Fake (DF) | ~1,000 | | |
| FaceForensics++ | Fake (F2F) | ~1,000 | | |
| ... | | | | |
| Celeb-DF v2 | Real | 590 | | |
| Celeb-DF v2 | Fake | 5,639 | | |
Include exact numbers from the official dataset papers with citations.

### C4. Augmentation Lacks Visual Examples (Demonstrability)
**Why it's a problem:** The reviewer asks for visual examples showing each augmentation step's output. Without this, readers can't assess the impact of augmentation choices.
**Fix:** Add a figure in section 3.3.3 showing a grid of augmented frames:
- Row 1: Original frame
- Row 2: After RandomResizedCrop
- Row 3: After ColorJitter
- Row 4: After RandomHorizontalFlip
- Row 5: After RandomErasing
Also add a figure showing FFT magnitude before and after frequency-domain augmentation (Gaussian noise injection + spectral band masking).

---

## PART D — OVERALL STRUCTURAL FIXES

### D1. Cross-Reference Rumusan Masalah ↔ Latar Belakang
After rewriting RM, verify each RM point has supporting evidence in latar belakang:
- RM 1 (cross-dataset failure of spatial models) → supported by paragraphs about spatial limitations
- RM 2 (hybrid can improve generalization) → supported by paragraphs about FDA and hybrid approaches
- RM 3 (measuring improvement) → supported by mention of evaluation gap in existing research

### D2. Consistency Check: Manfaat vs. Ruang Lingkup
After fixing A7, do a full cross-check: each manfaat point should be achievable within the stated ruang lingkup.

---

## Files to Modify

| File | Changes |
|------|---------|
| Main thesis markdown (BAB I section) | A1–A8: paragraph mergers, RM rewrite, tujuan rewrite, manfaat fix, dataset count |
| `documents/BAB_III_Tahapan_Pelaksanaan_v3.md` | C1–C4: process detail, system analysis section, dataset counts table, augmentation figures |
| BAB II section in main thesis markdown | B1–B9: citations, figures, subsection names, conversion of single-para subsections |

> **Note:** Confirm which file is the "live" source for BAB I and BAB II content. The PDF suggests a Word export. The markdown source needs to be identified (likely the main thesis `.md` file referenced in MEMORY.md).

---

## Execution Order

1. **First:** Fix BAB I (A1–A8) — highest priority, foundational to the whole document
2. **Second:** Fix BAB II (B1–B9) — citation/reference fixes can be done systematically
3. **Third:** Fix BAB III (C1–C4) — requires generating example images for augmentation
4. **Finally:** Cross-check D1–D2

---

## Verification

- Re-read latar belakang paragraphs 1–8 sequentially to confirm no contradictions remain
- Verify each RM has ≥1 supporting sentence in latar belakang
- Verify tujuan does not restate RM verbatim
- Verify manfaat points are consistent with ruang lingkup
- Check all BAB II tables and figures have captions with citations
- Verify BAB III has explicit total dataset count in a table
- Confirm 2.3.4, 2.9.4, 2.11.1, 2.11.2 all have citations added
