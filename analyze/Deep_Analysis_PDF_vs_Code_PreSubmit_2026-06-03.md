# Deep Analysis — Thesis PDF/DOCX vs Code (Pre-Submission Review)

**Date:** 2026-06-03
**Reviewed:** `documents/Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi.pdf` (128 pages) cross-checked against `deepfake_hybrid/` code.
**Purpose:** Independent, comprehensive pre-reviewer audit — the good, the bad, what to improve.

Page numbers below use the **body numbering** (BAB I = page 1). Physical PDF page = body page + 17.

---

## 0. VERDICT (TL;DR)

This is a **proposal-stage review scoped to BAB I–III** (abstract, BAB IV/V, and other front/back matter are out of scope here). The methodology (BAB I–III) is genuinely strong and now matches the code very closely — the hard prior issues (FFT high-pass filter, AdamW, patience=12, label smoothing=0.05, FreqCNN base=64, 3-group differential LR, warmup=3) have all been correctly synced into the live document. **But there are several blocking issues that a reviewer comparing against the code or flipping between sections WILL catch:**

| # | Blocking issue | Severity |
|---|---|---|
| 1 | **Citation numbers in BAB II are stale/corrupted** — do NOT match the bibliography (BAB I/III are fine) | 🔴 High |
| 2 | **Two architecture diagrams are stale** — Gambar 3.8 (FreqCNN) shows old base=32; Gambar 3.10 (Hybrid) shows old dropout=0.3 — both contradict the tables/text/code | 🔴 High |
| 3 | **Tabel 3.10 says label smoothing = "0,0 (nonaktif)"** but body §3.5.4 + config say 0.05 (active) — internal contradiction | 🔴 High |
| 4 | **Flowchart Gambar 3.1 omits the face-detection/cropping box** — yet the actual runs (`colab_run.ipynb`, `FACE_CROP=True`) crop faces, so the flowchart contradicts §3.3.2 and the real pipeline | 🟠 Medium |

---

## A. DOCUMENT STATUS

- **3 authors:** Naomi Prisella (221111798), Giovanny Halimko (221110058), Samuel Onasis (221110680). Universitas Mikroskil.
- **Structure present (BAB I–III scope):** Cover (ID+EN), Pengesahan, 3× Pernyataan, Kata Pengantar, Daftar Isi/Gambar/Tabel, BAB I–III, Daftar Pustaka (45 refs).
- **Title page says "2025"; metadata/current date 2026** — update year on resubmission.

---

## B. THE GOOD (genuine strengths — keep / lean into these)

1. **BAB I is well-constructed.** Latar belakang is narrowed and properly cited; the problem is framed around *cross-dataset generalization drop* of pure-spatial detectors — a real, defensible gap. Rumusan masalah (3 RQs), Tujuan (3), Manfaat (4: akademik/teknologi/sosial/praktis), Ruang Lingkup are clear and internally consistent. This directly addresses Pembanding 1's "problem too broad" and Pembanding 2's "why is cross-dataset important" critiques.

2. **Methodology↔code fidelity is excellent in BAB III.** Verified line-by-line (see §C). The FFT pipeline, augmentation values, model dims, optimizer, LR schedule, freezing, early stopping all match the code. This is far above the typical skripsi standard and is the chapter's biggest asset.

3. **Experiment design (§3.6) is rigorous and explicit:** factorial 3 models × 2 datasets × 4 sample sizes × 3 seeds = 72 runs → 144 evaluations; clear in-dataset vs cross-dataset protocol; variabel penelitian table (independen/dependen/kontrol); generalization-drop metric Δ = F1_in − F1_cross. The ablation framing (1 hybrid contribution + 2 single-domain baselines) cleanly answers the reviewer's "3 architectures vs 1 contribution" confusion.

4. **Worked numerical examples are (mostly) correct** and pedagogically strong: FFT 4×4 DC/frequency computation, depthwise-separable parameter count (73,728 → 8,768 ≈ 88% reduction), BCE+label-smoothing loss (0.1415), confusion-matrix metrics (acc 0.87, P 0.894, R 0.84, F1 0.866), SE-gating walk-through. These show real understanding and will play well in defense.

5. **Citation substance is good.** References are recent and on-topic (Durall, Zhang, Qian, Tan, Hasanaath/FSBI, Luo&Wang, Alam/SpecXNet, Odena, Rössler, Li/Celeb-DF, MTCNN). The previously-fabricated "96.36% AUC" is fixed → now "akurasi deteksi 99,26%" with correct accuracy (not AUC) label. Durall "five GANs" → corrected to "empat". Subsection 2.20.1 renamed to "Faktor Penyebab Kesulitan Generalisasi Cross-GAN" (reviewer item resolved).

6. **System analysis (§3.8) added** (Tabel 3.15 hardware, Tabel 3.16 software with justifications, pipeline orchestration, system outputs) — directly answers Pembanding 1's "kenapa tidak ada analisis sistem?"

---

## C. CODE ↔ THESIS CROSS-CHECK (verified)

### ✅ Confirmed MATCHES (thesis claim = actual code)

| Thesis claim | Code | Verdict |
|---|---|---|
| Grayscale ITU-R BT.601 Y=0.299R+0.587G+0.114B (Eq 3.1) | PIL `.convert("L")` (=BT.601) | ✅ |
| FFT2 → fftshift → magnitude → **Gaussian high-pass (β=0.15)** → log1p → float32 (Eq 3.2–3.5) | `src/fft_utils.py` (fft2, fftshift, abs, high-pass cutoff 0.15, log1p) | ✅ |
| Z-score norm from `fft_stats.json`, single-pass sum/sum-sq over ≤5000 files | `compute_fft_cache.py` / `deepfake_data.py` | ✅ (correctly *not* called "Welford" anymore) |
| Spatial aug: Resize256→RRC224(0.8–1.0)→ColorJitter(.2/.2/.1/.05)→HFlip(.5)→Norm(ImageNet)→RandomErasing(p.1,.02–.15) | `src/transforms.py` | ✅ exact |
| FFT aug: Gaussian noise σ=0.05; spectral band masking p=5%, width 1..H/16 (Eq 3.11–3.13) | `deepfake_data.py` | ✅ |
| Hybrid: synchronized HFlip, `include_hflip=False` on spatial pipeline | `deepfake_data.py` | ✅ |
| Split 70/15/15, video-level, stratified by label, seed=42, min 4/class | `build_splits.py` | ✅ |
| Spatial: timm `xception` pretrained, num_classes→1 logit, feat 2048 | `spatial_xception.py` | ✅ |
| FreqCNN depth=5, base=64, channels [64,128,256,512,512], Dropout2d 0.2, FC 512→256→1, Dropout 0.3, ~4.2M params | `freq_cnn.py` + `config.yaml` | ✅ (Tabel 3.6 + body text) |
| Hybrid: proj 256 each, concat 512, SE reduction 4 (512→128→512), classifier **Dropout 0.5**→512→128→ReLU→Dropout 0.5→128→1 | `hybrid_fusion.py` | ✅ (body §3.4.3 text) |
| Optimizer **AdamW**, lr 2e-4, wd 1e-4 | `train.py` | ✅ |
| Differential LR (3 groups): backbone 2e-5, freq branch 5e-5, head 2e-4 (Tabel 3.9) | `train.py` | ✅ |
| Freeze backbone 3 epochs, unfreeze epoch 4 | `train.py` FREEZE_EPOCHS=3 | ✅ |
| Warmup 3 epochs (LinearLR 0.1→1.0) → cosine to 1e-6 (Gambar 3.11) | `train.py` | ✅ |
| BCEWithLogitsLoss + pos_weight + label smoothing 0.05; grad accum 2 (eff. 32); grad clip 5.0; AMP; early stop patience 12 on val AUC; best ckpt by AUC | `train.py` + `config.yaml` | ✅ |
| Eval: acc/precision/recall/F1/AUC + Youden's J optimal threshold + θ=0.5 | `eval.py`, `metrics.py` | ✅ |
| MTCNN params: min_face 60px, thresholds 0.6/0.7/0.7, largest face, margin 0.3, full-frame fallback (§3.3.2) | `src/face_utils.py` | ✅ exact |

### ⚠️ Code-vs-thesis DISCREPANCIES

1. **MTCNN face-crop — §3.3.2 is accurate to the real runs; only the flowchart disagrees.**
   - §3.3.2 (p.73): "*setiap frame hasil ekstraksi terlebih dahulu melewati tahap deteksi dan pemotongan wajah sebelum dianalisis*" and "*Secara empiris, penerapan face cropping meningkatkan performa model spasial secara substansial*."
   - **The canonical results pipeline DOES crop faces.** `colab_run.ipynb` sets `FACE_CROP = True` (margin 0.3) and Step 4 passes `--face-crop --face-margin 0.3` into every `run_pipeline.py` call, which forwards them to `extract_frames.py` (MTCNN crop at `extract_frames.py:210`). The cross-eval `run_all.py` doesn't re-extract — it reuses the already-cropped frames. So §3.3.2's "mandatory" framing matches what the experiments actually do. ✅
   - Minor caveat: the CLI flag is `action="store_true"`, **default OFF** (`extract_frames.py:124`, `run_pipeline.py:91/126`), and CLAUDE.md's *example* commands don't pass it — so anyone running those examples (rather than the Colab notebook) wouldn't get cropping. Cheap fix: add `--face-crop` to CLAUDE.md's example commands.
   - **Real remaining gap:** Flowchart **Gambar 3.1 has no face-detection/cropping box** — it goes Ekstraksi Frame → Konversi Grayscale directly, contradicting both §3.3.2 and the actual pipeline.
   - **Action:** Add a face-detection/cropping box to **Gambar 3.1** so the flowchart matches §3.3.2 and the runs. (The empirical "meningkatkan performa" claim is still a forward reference — see §F — since BAB I–III reports no results yet.)
   - **Corrected Gambar 3.1 (paste this into the Word flowchart — new box marked `← TAMBAH`):**

     ```
     Dataset Video (FFPP, CDF)
             ↓
     Ekstraksi Frame (5 FPS, maks 50 frame/video)
             ↓
     Deteksi & Crop Wajah (MTCNN, margin 30%)        ← TAMBAH
             ↓
     Konversi FFT (Grayscale → FFT 2D → fftshift → |F| → log1p)
             ↓
     Pembagian Dataset (Train 70% / Val 15% / Test 15%, stratified by video)
             ↓
     Pelatihan Model (Spatial / Freq / Hybrid) → Validasi → Checkpoint Terbaik (AUC)
             ↓
     Evaluasi (In-dataset + Cross-dataset) → Tabel Hasil → Analisis
     ```

     The only change is the **new "Deteksi & Crop Wajah (MTCNN, margin 30%)" box inserted between "Ekstraksi Frame" and "Konversi FFT/Grayscale"** — every other box stays as-is. (Box labels reproduced from the markdown source `documents/BAB_III_Tahapan_Pelaksanaan_v4.md`; if the live `.docx` flowchart wording differs, keep its wording and just insert the new box in the same position.)

2. **Early fusion: claimed "evaluated" in BAB II but excluded from BAB III experiment matrix.**
   - BAB II §2.3.4 (p.15): "*kedua strategi fusion diimplementasikan dan dievaluasi: early fusion melalui XceptionNet 4-kanal, serta late fusion…*"
   - BAB III §3.4 + Tabel 3.11: only **spatial, freq, hybrid** (late fusion). `EarlyFusionXception` exists in code but is not in `run_all.py`'s matrix.
   - **Action:** Either drop "early fusion dievaluasi" from BAB II, or add it as a documented baseline. (Recommend dropping the claim to keep scope tight.)

3. **CLAUDE.md is slightly stale vs both code and thesis** (says optimizer "Adam", label smoothing default 0.02, patience 5, FreqCNN default 3-layer/130K). Not a thesis problem, but fix CLAUDE.md so future cross-checks don't get confused — code & thesis both use AdamW / 0.05 / patience 12 / FreqCNN depth 5 base 64.

---

## D. INTERNAL CONTRADICTIONS (thesis disagrees with itself — high reviewer-catch risk)

1. **🔴 Citation numbers in BAB II are stale — do not match the bibliography.**
   BAB I and BAB III cite correctly; BAB II §2.3.2 (p.12) is corrupted. Confirmed mismatches on a single page:
   | In-text (BAB II p.12) | Renders as | Should be | What that number actually is |
   |---|---|---|---|
   | Durall et al. | [7] | **[8]** | [7] = Rössler |
   | Zhang et al. | [8] | **[9]** | [8] = Durall |
   | Qian "Thinking in Frequency" | [14] | **[11]** | [14] = Rana |
   | Hasanaath FSBI | [17] | **[16]** | [17] = Luo & Wang |
   | Tan FSDL | [18] | **[12]** | [18] = Li (Celeb-DF) |
   | Luo & Wang | [19] | **[17]** | [19] = Chadha |

   Note it's *inconsistent even within BAB II*: Durall renders as [8] on p.9 (correct) but [7] on p.12 (wrong). This is the same field-sync issue flagged in the June-2 audit — it was fixed in BAB I/III but **BAB II was not fully refreshed.**
   **Fix:** In Word, select all (Ctrl+A) → F9 to update all citation fields; if numbers still don't move, toggle the bibliography style (IEEE→APA→IEEE) to force renumber, then re-verify BAB II in-text numbers against the Daftar Pustaka one by one (especially the frequency-domain block on p.12).

2. **🔴 Gambar 3.8 (FreqCNN diagram, p.86) is stale — shows the OLD base=32 architecture.**
   Diagram shows FreqBlock channels 1→32→64→128→256→256 and FC 256→128→1. But **Tabel 3.6 + body text + code** use base=64: channels 1→64→128→256→512→512, FC 512→256→1. The diagram directly contradicts the table on the very next page. **Regenerate Gambar 3.8 for base=64.** (The "GAP 256→1" box in the diagram is also mislabeled — GAP outputs a 512-d vector, not 1.)

3. **🔴 Gambar 3.10 (Hybrid diagram, p.89) is stale — shows dropout 0.3.**
   Diagram label "ClassifierDrop(0.3)". Body §3.4.3 (p.90–91) + code say **Dropout(0.5)** ×2. **Regenerate diagram with 0.5.**

4. **🔴 Tabel 3.10 (Hyperparameter summary, p.99) says "Label smoothing | 0,0 (nonaktif) | Dinonaktifkan untuk dataset kecil".**
   Contradicts §3.5.4 ("*label smoothing diaktifkan dengan α=0,05*"), §3.8.3 ("label smoothing 0,05"), the worked example (α=0.05), and `config.yaml` (0.05). **Fix the table to 0.05 (aktif).** Also clean up the muddled sentence in §3.5.4 that argues label smoothing *hurts* small datasets while the same paragraph says it's enabled — pick one stance (it's enabled at 0.05).

5. **🟠 Flowchart Gambar 3.1 augmentation box says "Bn. Mask p=0,15".**
   Body §3.3.4 + code say spectral band masking probability **0.05** (5%). The 0.15 looks like a leftover (possibly confused with high-pass β=0.15 or RandomErasing scale 0.15). Fix to 0.05.

---

## E. CITATIONS & REFERENCES (polish)

- **Reference formatting is uneven (IEEE).** Examples: [1] authors mangled as "K. P. dan M. S."; [10] Guidice and [13] SpecXNet and [33] LeCun missing year/venue; several entries lack publisher/venue/pages. Pembanding 1 explicitly cared about citation/format compliance with the TA pedoman — do a formatting pass.
- **Gambar 2.1 (p.16) has no citation** (Lena image with frequency components — clearly sourced). Pembanding 1 wanted every BAB II figure/table cited. Gambar 2.2 [30] and 2.3 [6] are cited; add a source for 2.1.
- **Tabel 2.1 (p.13) has no citation** and contains typos: "elatif stabil" → "Relatif stabil"; stray "R" in "kompresi tinggi R". A few other tables (2.4, 2.5) are uncited — fine if they're your own synthesis, but Pembanding 1 asked for citations on all; add "(disusun penulis)" or a source where appropriate.
- **Seminal GAN paper missing.** §2.2 says GAN "diperkenalkan pada tahun 2014" but cites reviews [15,20], not Goodfellow et al. 2014. Add the original GAN citation.
- Confirm every one of the 45 references is actually cited in-text (do a sweep), and that there are no orphan/duplicate entries after the field refresh.

---

## F. SMALLER ISSUES / TYPOS

- **FFT worked example (p.77):** Eq (3.9) is labelled "F(1,0)" but the heading and result are for **F(1,1)** — fix the label. The table's exponent column header shows `e^{-j2π((x+y)/2)}` but the values (and correct math) use `/4` — fix header to `/4`. (The numbers themselves are correct: F(1,1)=0.)
- **Depthwise-separable example (p.85), Eq (3.17):** "2×0 + 0×1 + 1×1 + 3×10 = 1" — the "3×10" should be "3×0" (otherwise it sums to 31, not 1). Likely an OCR/typo; verify in the DOCX.
- **Paragraph/sentence quality (Pembanding 2):** BAB II still has some run-on/comma-splice sentences and a few sub-1-paragraph subsections. Pervasive but minor; a light editing pass would help. Pembanding 2 also asked single-paragraph subsections be converted to point lists (a/b or 1/2).
- **Empirical claims stated in BAB III with no results to back them:** §3.3.2's "face cropping meningkatkan performa secara substansial" and §3.4.1's "akurasi 96–99%" are forward references; reword them as expectations/targets since BAB I–III contains no results to substantiate them.

---

## G. PRIORITIZED CHECKLIST (in order)

**P1 — must fix before any submission**
- [ ] **Refresh all citation fields** and fix the **BAB II numbering** (esp. p.12). Verify in-text [N] ↔ Daftar Pustaka one by one.
- [ ] **Regenerate Gambar 3.8** (FreqCNN base=64) and **Gambar 3.10** (dropout 0.5).
- [ ] **Fix Tabel 3.10** label smoothing → 0.05 (aktif); clean up §3.5.4 contradictory sentence.

**P2 — should fix (reviewer-catchable)**
- [ ] Add the **face-detection/cropping box to Gambar 3.1** (the runs already crop via `colab_run.ipynb` `FACE_CROP=True`; only the flowchart is out of sync). Optionally add `--face-crop` to CLAUDE.md examples.
- [ ] Remove/soften the **early-fusion "dievaluasi"** claim in BAB II to match BAB III scope.
- [ ] Fix flowchart **band-mask p=0.15 → 0.05**.
- [ ] Reference formatting pass (IEEE); add citation to **Gambar 2.1** + **Tabel 2.1**; add Goodfellow 2014.
- [ ] Fix Eq (3.9) label + table header (/2→/4); fix Eq (3.17) "3×10→3×0"; Tabel 2.1 typos.

**P3 — housekeeping**
- [ ] Update title-page year (2025→2026).
- [ ] Update `CLAUDE.md` so it reflects AdamW / label smoothing 0.05 / patience 12 / FreqCNN depth 5 base 64.

---

## H. BOTTOM LINE

The science and the methodology↔code alignment are strong and defensible — that's the hard part and it's done well. What's standing between BAB I–III and a clean reviewer pass is **finishing/cleanup work**, not rethinking: fix the BAB II citation numbers, regenerate two stale diagrams (Gambar 3.8, 3.10), and fix the label-smoothing table cell (Tabel 3.10). None of these require new experiments.
