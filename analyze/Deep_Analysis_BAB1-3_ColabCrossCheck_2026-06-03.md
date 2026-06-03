# Deep Analysis v2 — BAB I–III vs Code **and the Colab run that actually trains**

**Date:** 2026-06-03
**Scope:** BAB I–III only (per request).
**Reviewed:** the PDF/DOCX cross-checked against `deepfake_hybrid/` code **and `deepfake_hybrid/colab_run.ipynb`** (the notebook that produces all results that will go into BAB IV).
**Builds on:** `analyze/Deep_Analysis_PDF_vs_Code_PreSubmit_2026-06-03.md` (the first review). This document re-verifies that one independently and adds the **Colab execution lens** it was missing.

Body page numbering (BAB I = p.1). Physical PDF page = body page + 17.

---

## 0. THE ONE BIG IDEA

The methodology was synced to **`config.yaml`** — and against `config.yaml` it is genuinely excellent (verified line-by-line; see §3). **But the experiments are not run from `config.yaml`.** They run from `colab_run.ipynb`, which loads `config.yaml` as a base and then **overrides four runtime knobs**. So every place the thesis quotes the config value, it now contradicts the run that will fill BAB IV.

| Parameter | Thesis / `config.yaml` says | **Colab actually ran** | Severity |
|---|---|---|---|
| **Seeds** | 3 seeds (0,1,2); "72 run"; mean±std | **`N_SEEDS = 1`** (one seed) | 🔴 Fatal for the stats claim |
| **FFPP sample tiers** | `[100, 300, 600, 1000]` | **`[100, 250, 500, 750]`** | 🔴 High |
| **Frames/video** | "maks **50** frame/video" (everywhere) | **`MAX_FRAMES = 100`** | 🟠 Medium-High |
| **Batch size** | 16 (effective 32) | **`BATCH_SIZE = 64`** → effective 128 | 🟠 Medium |
| Face crop | (config default OFF) | **`FACE_CROP = True`** | 🟢 *This vindicates the thesis text — see §1.5* |

Everything in the first review still holds (label-smoothing table cell, two stale diagrams, BAB II citation numbers, etc.) and is re-confirmed below. **None of the fixes require new science — but #1 and #2 may require a re-run** depending on which side you reconcile to.

---

## 1. COLAB-vs-THESIS EXECUTION GAPS (the new findings)

These are the headline issues. They were invisible to a code-only review because the code *can* do the thesis's version — the **notebook** is what diverges.

### 1.1 🔴 Seeds: thesis claims 3, Colab ran 1 — and 1 seed cannot produce the headline statistics

**Thesis says (consistently):**
- §3.6.1: "Setiap kombinasi dijalankan dengan **tiga seed berbeda** untuk memperoleh estimasi **rata-rata dan simpangan baku** yang reliabel."
- Tabel 3.11: Seed = "0, 1, 2" (count 3); **"Total pelatihan: 3 × 2 × 4 × 3 = 72 run"**, "144 evaluasi".
- Tabel 3.10: "Seed | 0, 1, 2 | Reproduktibilitas (3 seed)".
- Tabel 3.12 (control variable): "Seed | 0, 1, 2".
- §3.8.3: "…dan **3 seed untuk validitas statistik**."

**Colab ran:** `N_SEEDS = 1` (cell `code-01`, with the author's own comment *"increase to 3 for statistical validity"*). This is written through to `colab_config.yaml` as `n_seeds: 1`.

**Code consequence (verified in `run_all.py`):** seeds = `range(n_seeds)` → `[0]`. The mean/std **summary** tables (`Table1_in_dataset_summary.csv`, `Table2_cross_dataset_summary.csv`) are generated **only if `len(seeds) > 1`**. With one seed they are **not produced at all** — and a std over one sample is 0/undefined anyway.

**Why it matters:** the thesis's reliability argument (mean ± std over 3 seeds, 72 runs) is structural to the experimental design section. A 1-seed run gives **no variance estimate and no 72-run matrix** — exactly what a methods-aware reviewer probes ("where are your error bars / how many runs?").

**Fix — pick one:**
- **(A, recommended)** Re-run with `N_SEEDS = 3`. It's the only way to honor the thesis as written and to report mean±std. (Cost: 3× training time. With the small sample tiers and early stopping this is feasible on Colab Pro.)
- **(B)** If a re-run is impossible before submission, change the thesis to single-seed honestly: drop "72 run", "simpangan baku", "3 seed" from §3.6.1, Tabel 3.10/3.11/3.12, §3.8.3; report single-seed numbers and state the seed (0). This is weaker and reviewers may object.

### 1.2 🔴 FFPP sample tiers: thesis `[100,300,600,1000]`, Colab `[100,250,500,750]`

**Thesis says:** Tabel 3.3 and Tabel 3.11 → FFPP = **100, 300, 600, 1000**; CDF = 100, 250, 500, 750. Tabel 1.1 & Tabel 3.1 describe FFPP as **n = 1000** (500 real + 500 fake). §3.3.1 even computes "Batas 50 frame/video membatasi total frame FFPP **n = 1000 ~ 50.000**".

**Colab ran:** `FFPP_SAMPLES_LIST = [100, 250, 500, 750]` and `CDF_SAMPLES_LIST = [100, 250, 500, 750]` (cell `code-01`). FFPP tops out at **750, not 1000**, and the middle tiers are **250/500, not 300/600**.

**Why it matters:** BAB IV's FFPP rows/plots will be at 100/250/500/750. They will not match Tabel 3.3/3.11, and the "n=1000" framing in Tabel 1.1/3.1/§3.3.1 will have no corresponding experiment.

**Fix — pick one:**
- **(A, easiest)** Set FFPP tiers in the thesis to **[100, 250, 500, 750]** (identical to CDF — clean and symmetric). Update Tabel 3.3, Tabel 3.11, and soften Tabel 1.1/3.1 "n=1000" to "pool tersedia s/d 1000; eksperimen s/d 750", and fix the §3.3.1 frame arithmetic.
- **(B)** Re-run FFPP at [100,300,600,1000] to match the thesis.
- (Note: `CDF [100,250,500,750]` already matches — only FFPP is off.)

### 1.3 🟠 Frames per video: thesis "maks 50", Colab ran 100

**Thesis says (everywhere):** Gambar 3.1 ("maks 50 frame/video"), the Gambar 3.3 pseudocode (`max_frame = 50`), §3.2.4 ("diekstraksi maksimum 50 frame"), §3.3.1 ("hingga maksimum 50 frame per video"; "Batas 50 frame/video … ~ 50.000"), Tabel 3.1 ("5 fps, max 50 frame/video"). `config.yaml`: `max_frames_per_video: 50`.

**Colab ran:** `MAX_FRAMES = 100`, written to `colab_config.yaml` (`max_frames_per_video: 100`) **and** passed as `--max-frames 100` to every `run_pipeline.py` call.

**Why it matters:** actual frames per video — and therefore the total-frame counts (~50,000 FFPP, ~37,500 CDF in Tabel 1.1/3.1) — are about **2×** what the thesis states. The per-frame dataset size that all results rest on is different.

**Fix:** set `MAX_FRAMES = 50` in the notebook (cheapest, matches the whole thesis) **or** change every "50" above to 100 and recompute the ~frame totals. The first is far less error-prone.

### 1.4 🟠 Batch size: thesis 16 (effective 32), Colab ran 64 (effective 128)

**Thesis says:** §3.5.5 ("ukuran batch per langkah sebesar 16, ukuran batch efektif menjadi 16 × 2 = 32"), Tabel 3.10 ("Batch size | 16 | …efektif 32"), §3.8.3 ("batch size 16 … batch efektif 32"). `config.yaml`: `batch_size: 16`.

**Colab ran:** cell `code-02` auto-tunes by GPU → **`BATCH_SIZE = 64`** on a T4 (128 on A100, 32 on a small GPU), written to `colab_config.yaml`. With `accum_steps = 2`, **effective batch = 128** (or 256 on A100), not 32.

**Why it matters:** effective batch size is a real optimization hyperparameter (interacts with LR, warmup, BN). A reviewer comparing config ↔ thesis ↔ notebook sees three different numbers. Also the value is GPU-dependent, so "the" batch size depends on which GPU the final run used.

**Fix:** decide the canonical run GPU (T4 ⇒ 64/eff 128), then state that in §3.5.5 / Tabel 3.10 / §3.8.3; **or** pin `BATCH_SIZE = 16` in the notebook to match the thesis. If you keep auto-tune, add a sentence: "batch size disesuaikan dengan VRAM GPU (T4: 64, A100: 128)".

### 1.5 🟢 Face crop: the FIRST REVIEW WAS BACKWARDS — Colab uses it, so §3.3.2 is correct; fix the flowchart instead

The first review flagged MTCNN face-crop as "opt-in/off-by-default" and recommended **softening §3.3.2**. The Colab run shows the opposite: **`FACE_CROP = True`, `FACE_MARGIN = 0.3`** (cell `code-01`), passed as `--face-crop --face-margin 0.3` to every pipeline call. Face cropping **is** part of the real pipeline. This is reinforced by Tabel 3.16 (lists `facenet-pytorch` "untuk deteksi dan cropping wajah") and §3.8.3 ("ekstraksi frame **dan cropping wajah** (`extract_frames.py`)").

So **§3.3.2's "setiap frame … melewati tahap deteksi dan pemotongan wajah" is accurate.** The genuine inconsistency is:
- 🟠 **Gambar 3.1 (flowchart) has no face-detection/crop box.** It goes *Ekstraksi Frame → Konversi Grayscale* directly. Add a **"Deteksi & Crop Wajah (MTCNN, margin 30%)"** box between them so the flowchart matches §3.3.2 + the code + the run.
- 🟠 **The empirical claim** in §3.3.2 — "*Secara empiris, penerapan face cropping meningkatkan performa model spasial secara substansial pada FaceForensics++*" — is a forward reference. The Colab only ran with crop **ON** (no OFF baseline), so there is no A/B result to back "substansial". Either soften to the literature-backed rationale (background = noise [4,7]) or run a crop-on/off ablation if you want to keep the empirical claim.

### 1.6 Note on what the Colab *preserves* (these are fine)

The notebook's "load config.yaml as base, override only runtime keys" pattern (cell `code-04`) **correctly carries through** the hyperparameters the thesis cares about: `freq_depth=5`, `freq_base_channels=64`, `early_stop_patience=12`, `label_smoothing=0.05`, `fft_noise_sigma=0.05`, `accum_steps=2`, `lr=2e-4`, `weight_decay=1e-4`, `image_size=224`, `fusion_mode=two_branch`. There's even a fail-fast assertion guarding these. So those thesis claims **do** match the run. (The Colab comment "patience=10" in `code-01` is stale text only — the actual value loaded is 12 from config. Harmless, but tidy it up.)

---

## 2. THE GOOD (genuine strengths — keep)

Independently confirmed, not just inherited from the first review:

1. **BAB I is strong and tight.** Latar belakang narrows cleanly to the *cross-dataset generalization drop* of pure-spatial detectors (AUC drop 10–20 pts cross-dataset [14,15]) — a real, defensible gap. 3 RQs / 3 tujuan / 4 manfaat / ruang lingkup are internally consistent. The ablation framing (1 hybrid contribution + 2 single-domain baselines) directly answers the "3 architectures vs 1 contribution" reviewer worry.
2. **BAB III ↔ `config.yaml` fidelity is excellent** (verified line-by-line via the code): FFT pipeline (BT.601 grayscale Eq 3.1, DFT Eq 3.2, Gaussian high-pass β=0.15/σ≈33.6px Eq 3.4, log1p Eq 3.5), spatial aug (Resize256→RRC224(0.8–1.0)→ColorJitter(.2/.2/.1/.05)→HFlip(.5)→ImageNet norm→RandomErasing(p.1,.02–.15)), FFT aug (noise σ=0.05, band-mask 5%, width 1..H/16), hybrid dims (2048→256, 512→256, concat 512, SE reduction 4, classifier Dropout 0.5×2 → 512→128→1), AdamW lr 2e-4/wd 1e-4, 3-group differential LR (2e-5 / 5e-5 / 2e-4), freeze 3 epochs, warmup 3 → cosine to 1e-6, grad accum 2, grad clip 5.0, AMP, early stop patience 12 on val AUC, Youden's J + θ=0.5 eval. **FreqCNN Tabel 3.6 (base=64, depth=5, ~4.2M) matches the code exactly.** This is well above the typical skripsi bar.
3. **Worked examples are pedagogically strong and (mostly) numerically correct:** FFT 4×4 DC=1600, depthwise-separable param count (73,728→8,768 ≈ 88% reduction), BCE+label-smoothing loss = 0.1415, confusion-matrix metrics (acc 0.870 / P 0.894 / R 0.840 / F1 0.866), SE-gating walk-through. They demonstrate real understanding and will defend well.
4. **Experiment design (§3.6) is rigorous:** factorial, explicit in- vs cross-dataset protocol, variabel penelitian table, generalization-drop metric Δ = F1_in − F1_cross.
5. **System analysis (§3.8) is a good add** and — nice touch — **the hardware table (Tesla T4) matches the actual Colab environment**, so that part is internally consistent with the run.
6. **Citation substance is good** (Durall, Zhang, Qian, Tan/FSDL, Hasanaath/FSBI, Luo&Wang, Odena, Rössler, Li/Celeb-DF, MTCNN). The headline number is now correctly stated: XceptionNet **99,26% akurasi** on uncompressed FFPP, attributed to Rössler [7] (§2.21.2, Tabel 2.8) — defensible.

---

## 3. CONFIRMED FROM FIRST REVIEW (still unresolved — re-verified here)

### 3.1 🔴 Internal contradictions
- **Tabel 3.10 label smoothing = "0,0 (nonaktif) — Dinonaktifkan untuk dataset kecil".** Contradicts §3.5.4 (α=0.05 *diaktifkan*), the worked example (Eq 3.33 uses 0.05), §3.8.3 ("label smoothing 0,05"), `config.yaml` (0.05), and the Colab run (0.05). **→ Change the cell to "0,05 (aktif)".** Still present.
- **§3.5.4 muddled sentence.** It enables smoothing at 0.05 "untuk mencegah overconfidence pada dataset kecil," then says "Pada dataset berukuran kecil, sinyal positif yang terbatas menjadi semakin lemah apabila label di-smooth, sehingga model kesulitan membedakan kelas." Those two claims fight each other. **→ Pick one stance (it's enabled at 0.05).**
- **Gambar 3.8 (FreqCNN) is STALE — base=32.** Diagram shows `1→32→64→128→256→256`, `FC 256→128→1`. Tabel 3.6 (next page), body, and code use **base=64**: `1→64→128→256→512→512`, `FC 512→256→1`. The "GAP 256→1" box is also mislabeled (GAP outputs a 512-d vector). **→ Regenerate for base=64.**
- **Gambar 3.10 (Hybrid) is STALE — multiple errors:**
  - "ClassifierDrop(0.3)" → should be **Dropout(0.5) ×2** (body §3.4.3 + code). *(first review caught this)*
  - **NEW:** FreqCNN branch labeled **"256-d"** and **"Proj 256→256"** → should be **"512-d"** and **"Proj 512→256"** (base=64; body §3.4.3 item 2 says "vektor fitur berdimensi 512"). The diagram still reflects the old base=32 freq branch.
  - **NEW:** "RG Input" typo → "RGB Input".
  - **→ Regenerate.**

### 3.2 🔴 BAB II citation numbering still stale
BAB I and BAB III cite correctly; **BAB II is shifted.** Canonical numbering (from BAB I/III ↔ Daftar Pustaka): `[8]`Durall, `[9]`Zhang, `[10]`Giudice, `[11]`Qian, `[12]`Tan, `[13]`Alam/SpecXNet, `[14]`Rana, `[15]`Rao&Uehara, `[16]`Hasanaath/FSBI, `[17]`Luo&Wang, `[18]`Li/Celeb-DF.

Confirmed mismatches on **§2.3.2 (p.12)**: Durall `[7]`→**[8]**, Zhang `[8]`→**[9]**, Qian `[14]`→**[11]**, Hasanaath/FSBI `[17]`→**[16]**, Tan `[18]`→**[12]**, Luo&Wang `[19]`→**[17]**. §2.4.3 (p.18) is also inconsistent ("Tan et al. … [17, 23]"). **→ Ctrl+A → F9 to refresh fields; if numbers don't move, toggle the bibliography style to force renumber; then verify the frequency-domain block on p.12 one-by-one against the Daftar Pustaka.**

### 3.3 🟠 Scope / claim issues
- **Early-fusion "dievaluasi" claim (BAB II §2.3.4, p.15):** "*kedua strategi fusion diimplementasikan dan **dievaluasi**: early fusion … 4-kanal, serta late fusion …*". But BAB III §3.4 builds only spatial/freq/hybrid(late), Tabel 3.11 excludes early fusion, and the Colab matrix does **not** enable `early_fusion`. **→ Drop "dievaluasi" (or "diimplementasikan namun tidak menjadi fokus evaluasi").**
- **Forward-referenced empirical claims before BAB IV exists:** §3.3.2 face-crop "substansial", §3.4.1 "akurasi 96–99%", Tabel 2.9 hybrid "98–99% / generalisasi sangat baik". Stated as established. **→ Ensure BAB IV substantiates, or reword as expectation / clearly attribute to literature.** (Tabel 2.9 presenting hybrid "98–99%, sangat baik" as fact slightly undercuts the very gap the thesis claims to fill — soften.)

### 3.4 🟠 Math/typo in worked examples
- **Eq (3.9) is labeled "F(1,0)" but computes F(1,1)** (heading says "Menghitung F(1,1)", uses (x+y)/4, result 0). Also the table column header reads `e^{-j·2π((x+y)/2)}` while the values use **/4**. **→ Fix label F(1,0)→F(1,1) and header /2→/4.** (Numbers are correct.)
- **Eq (3.17): "2×0 + 0×1 + 1×1 + 3×10 = 1"** — the "3×10" should be **"3×0"** (sum = 1, matches Y₂). **→ Fix typo.**

### 3.5 🟠 Citations / figures
- **Gambar 2.1 (Lena, p.16) uncited** (clearly sourced; (a)/(b)/(c)/(d) panel layout). Gambar 2.2 `[30]` and 2.3 `[6]` are cited — **add a source for 2.1.**
- **Tabel 2.1 (p.13) uncited + typos:** "elatif stabil" → "**R**elatif stabil"; stray "R" in "kompresi tinggi **R**".
- **§2.2 GAN "diperkenalkan pada tahun 2014"** cites reviews `[15, 20]`, not **Goodfellow et al. 2014** — add the seminal GAN citation.
- IEEE reference formatting uneven (per first review) — do a formatting pass against the TA pedoman.

---

## 4. NEW SMALL ITEMS (this review)
- 🟠 **§3.4.4 mis-references tables by one:** "*Tabel 3.6 merangkum perbedaan … antara ketiga arsitektur … Tabel 3.7 merinci dimensi fitur*." But Tabel 3.6 = FreqCNN layer table; the 3-architecture comparison is **Tabel 3.7**, and the per-component dimensions is **Tabel 3.8**. **→ Should read "Tabel 3.7 … Tabel 3.8".**
- 🟠 **§3.6.4 mis-reference:** "*Tabel 3.11 merangkum seluruh variabel*" → the variable table is **Tabel 3.12** (3.11 is the experiment matrix).
- 🟢 **BAB I p.2 typo:** "*Alam **el at.***" → "Alam et al."
- 🟢 **Gambar 3.1 augmentation box** still says "Bn. Mask **p=0,15**" → should be **0,05** (matches §3.3.4 + code). *(first review item, still present)*
- 🟢 Gambar 3.7 shows a **299×299×3** input (the canonical Xception figure) while the pipeline uses 224×224 — acceptable as a reference diagram, but a one-line caption note ("input disesuaikan ke 224×224") would pre-empt the question.

---

## 5. DOCUMENT STATUS (unchanged from first review)
- **Abstrak** still template placeholder (ID + EN). **Daftar Lampiran** empty. **BAB IV/BAB V** empty stubs. **Title year "2025".** → If this is a **proposal/sidang proposal** submission, empty BAB IV/V is expected; the abstract should still be written. **Confirm proposal vs final** — it changes whether BAB IV/V are blockers.

---

## 6. PRIORITIZED CHECKLIST

**P0 — confirm context**
- [ ] Proposal (BAB I–III) or final thesis? Decides whether empty BAB IV/V are blockers.
- [ ] **Decide the reconciliation direction for §1.1–§1.4:** re-run Colab to match the thesis, or edit the thesis to match the Colab run? (This is the single most important decision.)

**P1 — must fix (reviewer-catchable, no new science except possibly seeds)**
- [ ] **Seeds (🔴):** re-run with `N_SEEDS=3` *(recommended)*, **or** strip all "3 seed / 72 run / simpangan baku" claims (§3.6.1, Tabel 3.10/3.11/3.12, §3.8.3).
- [ ] **FFPP tiers (🔴):** make Tabel 3.3/3.11 = `[100,250,500,750]` and reconcile Tabel 1.1/3.1/§3.3.1 *(recommended)*, **or** re-run FFPP at `[100,300,600,1000]`.
- [ ] **Frames/video (🟠):** set Colab `MAX_FRAMES=50` *(recommended)* **or** change every "50 frame/video" + frame totals to 100.
- [ ] **Batch size (🟠):** state the actual run value (T4 ⇒ 64/eff 128) in §3.5.5 / Tabel 3.10 / §3.8.3, **or** pin Colab `BATCH_SIZE=16`.
- [ ] **Tabel 3.10 label smoothing → "0,05 (aktif)"**; fix the contradictory §3.5.4 sentence.
- [ ] **Regenerate Gambar 3.8** (base=64) and **Gambar 3.10** (freq 512-d, Proj 512→256, Dropout 0.5×2, "RGB Input").
- [ ] **Add the face-crop box to Gambar 3.1** (and fix band-mask `p=0,15`→`0,05`); keep §3.3.2 but soften the "substansial" empirical claim.
- [ ] **Refresh citation fields; fix BAB II numbering** (esp. p.12), verify in-text [N] ↔ Daftar Pustaka.
- [ ] Write the **Abstrak** (ID+EN, 100–200 words, 3–5 keywords).

**P2 — should fix**
- [ ] Drop the early-fusion "dievaluasi" claim (BAB II §2.3.4).
- [ ] Fix §3.4.4 ("Tabel 3.6/3.7" → "3.7/3.8") and §3.6.4 ("Tabel 3.11" → "3.12") cross-references.
- [ ] Fix Eq (3.9) label + table header (/2→/4); fix Eq (3.17) "3×10"→"3×0".
- [ ] Add citation to Gambar 2.1 + Tabel 2.1 (and Tabel 2.1 typos); add Goodfellow 2014; IEEE formatting pass.
- [ ] "Alam el at." → "Alam et al." (BAB I p.2).

**P3 — housekeeping**
- [ ] Title year 2025 → 2026.
- [ ] Update `CLAUDE.md` (it still says FFPP `[100,300,600,1000]` — note the Colab actually ran `[100,250,500,750]`; also Adam→AdamW, patience 5→12, label smoothing 0.02→0.05, FreqCNN 3-layer/130K→depth-5/base-64/4.2M).
- [ ] Tidy the stale "patience=10" comment in `colab_run.ipynb` cell `code-01`.

---

## 7. BOTTOM LINE

The science, the gap, and the methodology↔`config.yaml` alignment are strong — that's the hard part and it's done. The blocker now is that **the notebook that generates the results overrides `config.yaml` on seeds, FFPP sample sizes, frames/video, and batch size.** Until those four are reconciled (re-run *or* re-document), BAB IV will not match BAB III, and a reviewer who opens `colab_run.ipynb` (or just counts "72 runs" against a single-seed result) will catch it immediately. Fix the seeds question first — it's the only one that might force a re-run, and it's load-bearing for the whole "reliable mean±std" story. Everything else (label-smoothing cell, two diagrams, BAB II citations, flowchart face-crop box, worked-example typos) is finishing work.

---

## 8. ACTION DECISIONS (from author, 2026-06-03)

**Submission = PROPOSAL (BAB I–III).** Empty BAB IV/V are expected and not blockers. Abstract still needed.
**Direction = edit thesis to match the Colab run** — with two flagged exceptions where editing the *notebook* is cheaper/stronger (see below).

### 8.1 The 4 runtime mismatches — exact resolution

| # | Item | Resolution | Why |
|---|---|---|---|
| 1 | **Seeds** | ⚠️ **EXCEPTION — fix the notebook, not the thesis.** Set `N_SEEDS = 3` in `colab_run.ipynb` (cell `code-01`). Keep "3 seed / 72 run / mean±std" in the thesis. | It's a proposal; "3 seeds" is the *plan* and BAB IV is empty, so nothing contradicts it. Editing down to 1 seed throws away the strongest stats claim for no gain. One-line notebook change. |
| 2 | **Frames/video** | ⚠️ **EXCEPTION — fix the notebook.** Set `MAX_FRAMES = 50` in `colab_run.ipynb`. Thesis stays "50 frame/video, ~50.000/~37.500". | Editing the thesis touches 2 figures + ~6 text spots + frame totals; the notebook is one line and the "50" story is cleaner. |
| 3 | **FFPP sample tiers** | **Edit thesis** → `[100, 250, 500, 750]`. | Two table cells; matches CDF; symmetric and clean. |
| 4 | **Batch size** | **Edit thesis** → document actual (T4: 64, effective 128; auto-tuned by VRAM). | Notebook auto-tunes by GPU; pinning to 16 wastes T4 VRAM. |

### 8.2 Surgical edit list — FFPP tiers (#3)
- **Tabel 3.3 (p.71):** "FaceForensics++ (FFPP) | **100, 300, 600, 1000**" → "**100, 250, 500, 750**".
- **Tabel 3.11 (p.100):** "Ukuran sampel FFPP | **100, 300, 600, 1000** | 4" → "**100, 250, 500, 750** | 4".
- **Tabel 3.12 (p.101):** "Ukuran sampel | **100–1000** (bervariasi per dataset)" → "**100–750**".
- **Tabel 1.1 (p.5) / Tabel 3.1 (p.70):** keep FFPP pool n=1000 (500 real + 500 fake) — the pool is fine; tiers sample subsets up to 750. Optional: note "eksperimen menggunakan s/d 750 video".
- "**Total pelatihan: 3 × 2 × 4 × 3 = 72 run**" (Tabel 3.11 caption): still 72 with 4 FFPP tiers — no change.

### 8.3 Surgical edit list — batch size (#4)
- **§3.5.5 (p.97):** "ukuran batch per langkah sebesar 16, ukuran batch efektif menjadi 16 × 2 = 32" → e.g. "ukuran batch disesuaikan dengan VRAM GPU (Tesla T4: 64), dengan gradient accumulation 2 langkah sehingga batch efektif = 128".
- **Tabel 3.10 (p.99):** "Batch size | **16** | Per langkah; efektif 32" → "**64** (T4) | Per langkah; efektif 128"; "Gradient accumulation | 2 langkah | …batch efektif **32**" → "…efektif **128**".
- **§3.8.3 (p.104):** "batch size **16** dengan gradient accumulation 2 langkah (batch efektif **32**)" → "batch size **64** … (batch efektif **128**)".
- *(Optional)* update `config.yaml` `batch_size: 16` → 64, or leave it and note the notebook auto-tunes.

### 8.4 Notebook edits (#1, #2)
- `colab_run.ipynb` cell `code-01`: `N_SEEDS = 1` → `3`; `MAX_FRAMES = 100` → `50`; fix stale comment "early stopping (patience=10)" → "(patience=12)".

### 8.5 Everything else still applies (P1/P2 in §6)
Label-smoothing cell (Tabel 3.10 → 0,05 aktif), §3.5.4 sentence, regenerate Gambar 3.8 & 3.10, add face-crop box to Gambar 3.1 + band-mask 0,15→0,05, BAB II citation refresh, early-fusion "dievaluasi" claim, table cross-refs (§3.4.4, §3.6.4), Eq 3.9/3.17, Gambar 2.1/Tabel 2.1 citations, Goodfellow 2014, "Alam el at." typo, **and write the Abstrak**.
