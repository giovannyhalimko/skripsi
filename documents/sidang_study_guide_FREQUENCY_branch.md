# Frequency Branch — Study Guide (FreqCNN + FFT)

> **Your role:** you own the **frequency branch** — the FFT log-magnitude representation, the `FreqCNN`, and the **central negative result** of the thesis (frequency is near-random and does not help fusion). This is a _companion_ to `sidang_study_guide_SPATIAL_branch.md`, `sidang_study_notes_detailed_2026-06-25.md` (Steps 03, 04, 07), and `PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md`. This doc goes **deep only where the frequency branch is concerned**, and includes a **demo section** (§7) for the freq-specific things a reviewer can point at live.
>
> **Why your branch is the one that decides the thesis:** the whole title is "_Studi Komparatif ... terhadap Model Domain Tunggal_". The variable being measured is **the contribution of the frequency domain**, and your branch is that variable. The freq branch being **weakest** (AUC ~0.56) is _the result_, not a bug. Two of the hardest reviewer targets land on you: "why is frequency near-random?" (RM3) and "if freq is useless, why does hybrid exist / why isn't this under-powered?"

---

## 0. The one-liner you defend

> "The frequency branch (FreqCNN on an FFT log-magnitude map) is our **weakest detector** — in-dataset AUC only **~0.56** on both datasets, and its **validation AUC is flat from epoch 1**: it never learned. That is **not** a training failure. We ruled out under-powering three ways — more data, a bigger backbone, verified preprocessing — and near-chance survives all three. So the bottleneck is the **information content of the compressed, face-cropped FFT input**, not the model. This is a **controlled falsification** of the common assumption that spectral artifacts are a strong, general cue."

Keep coming back to: **freq is near-random _by measurement, cleanly, for a reason we can name_ — that is the finding.**

---

## 1. What to study — ordered curriculum

Each item: _what · why you need it · what to read._ Tick them off.

### ① The FFT transform, exactly — `image_to_fft_logmag` (`src/fft_utils.py:22-33`) · **~1.5 hr · CORE**

This is the "explain your frequency representation" question. You must be able to walk it step by step.

- **Grayscale → resize 224×224** (`img.convert("L")`, `resize`). Color is dropped; the branch sees luminance structure only.
- **`np.fft.fft2` → `np.fft.fftshift`** — 2-D Fourier transform, then shift the **DC (zero-frequency)** term to the image center. So after shift: **center = low freq, edges = high freq.**
- **Magnitude only** (`np.abs`) — keeps spectral **energy** per frequency. **Phase is thrown away.** _(Memorize this — it's failure cause #2.)_
- **Gaussian high-pass mask** (`_highpass_mask`, cutoff 0.15) — multiplied in, attenuates the dominant low-frequency center so the CNN can focus on the high-frequency band where GAN up-sampling fingerprints live.
- **`log1p`** = `log(1+|F|)` — log scaling compresses the huge dynamic range of the spectrum into a trainable map.
- Output: a **single-channel 224×224** FFT log-magnitude map, cached as `.npy`.

> **One-sentence answer:** "We take each frame to grayscale, compute its 2-D FFT, keep the magnitude spectrum, apply a Gaussian high-pass to emphasize high frequencies, and log-scale it — producing a single-channel FFT log-magnitude map. The FreqCNN learns discriminative features from that map."

### ② The high-pass mask is _soft_, not a hard cut — `_highpass_mask` (`fft_utils.py:9-19`) · **30 min · CORE**

A likely trap: "you said low frequency is unused." **Wrong — it's attenuated, not removed.**

- Formula: `H = 1 − exp(−d²/2σ²)`, with `σ = cutoff·size = 0.15·224 ≈ 33.6 px`. `d` = distance from center.
- **Only the pure DC term (d=0) is multiplied by ~0.** At `d=σ` the mask ≈ 0.39 (low freq strongly attenuated but still passes), at `d=2σ` ≈ 0.86, edges → 1.0.
- **Why soft, not hard:** (a) a smooth roll-off avoids **ringing** artifacts a sharp cut would introduce, and (b) some discriminative signal (spectral roll-off, Durall `[8]`) lives in the **mid** band, not only the edge — gradual attenuation is safer than a hard cut.
- **Correct phrasing:** "high frequencies are **amplified**, low frequencies are **suppressed (attenuated)** — not discarded." (The thesis itself says "menekan dominasi", suppress, not remove.)

### ③ Why FFT _should_ expose deepfakes — the literature you are testing · **45 min · CORE**

Reviewers want to know the theory you built on (and are now qualifying):

- GANs up-sample with **transposed convolution / interpolation**, which inserts zeros → **replicates the spectrum into the high-frequency band** → periodic **checkerboard** grid artifacts (Odena `[21]`).
- CNN-based generators **fail to reproduce the natural spectral distribution** — their power spectrum deviates from real images, **mostly in the high-frequency tail** (Durall et al. `[8]`; Zhang et al. `[9]`).
- Frequency-aware detectors exploit this: F³-Net / "Thinking in Frequency" (Qian `[11]`), DCT anomalies (Giudice `[10]`), FreqNet (Tan `[12]`).
- **Your study asks:** does a _simple raw-FFT branch_ capture this and help fusion? **Answer, under our conditions: no.** That's the whole point — you're testing the claim, not assuming it.

### ④ The FreqCNN architecture — read it line by line (`src/models/freq_cnn.py`) · **1 hr · CORE**

This is your "explain your model" question. Know it cold.

- **`FreqBlock`** (the building block): `Conv3×3(pad 1) → BatchNorm → ReLU`, plus a **residual shortcut** (a `1×1` conv when channel count changes, else identity), added **before** a `MaxPool2d(2)`. So one block = `pool(conv(x) + shortcut(x))`. Residual idea is from ResNet (He `[5]`); it keeps training stable as depth grows.
- **Configurable depth/channels** via `freq_depth` / `freq_base_channels`. ⚠️ **The results run uses `depth=5, base_channels=64`** (`config.yaml:22-23`), NOT the constructor defaults (3/32). Cite the _results_ config:
  - Channel progression **1 → 64 → 128 → 256 → 512 → 512**, **feature dim 512**, **~4.2M params (4,217,217)**.
  - _(The docstring's "depth=5 → 256-d, ~700K" describes base=32; that is **not** what the experiments use. Say **512-dim, 4.2M**.)_
- **`.features`** = the conv blocks + `Dropout2d(0.2)` + `AdaptiveAvgPool2d(1)` → a 512-vector. **`.classifier`** = `Flatten → Linear(512→256) → ReLU → Dropout(0.3) → Linear(256→1)`.
- **Key fact for the hybrid:** inside the hybrid, only `FreqCNN.features` is used — **the classifier head is bypassed** (`hybrid_fusion.py:58`). Standalone `freq` uses the full net.
- Input **224×224, single channel**. Layer-by-layer is in the thesis (**Tabel 3.7**, and **Gambar 3.8/3.9** for the FreqCNN / FreqBlock diagrams).

### ⑤ FFT normalization + augmentation — the preprocessing you must defend · **45 min**

- **Per-dataset z-score:** `(x − mean) / std` using stats from `fft_stats.json` (`deepfake_data.py:129`). Stats are **auto-computed** after `compute_fft_cache.py`. FFPP stats: **mean ≈ 5.84 / std ≈ 1.28** (the file on disk; docs sometimes quote 5.78 — the code reads the **live file**, so 5.84 is what runs). The old fallback `std=3.0` was **~2.3× too big** — a real bug that was found and fixed. This matters because _bad normalization_ is one thing a reviewer will suspect; you can say it was verified and corrected.
- **Train-only FFT augmentation** (`deepfake_data.py:131-141`): Gaussian noise `σ=0.05` added to the map, plus **5%-probability spectral-band masking** (zero a random horizontal/vertical frequency band) to stop the net memorizing any single band. Off at inference.

### ⑥ Freq results — memorize your own numbers · **45 min · CORE**

**In-dataset AUC (mean over seeds 0/1/2):**

|                               | n=250 | n=500 | n=750     |
| ----------------------------- | ----- | ----- | --------- |
| **FFPP freq**                 | 0.469 | 0.545 | **0.562** |
| **CDF freq**                  | 0.500 | 0.549 | **0.562** |
| _(for contrast)_ FFPP spatial | 0.743 | 0.693 | 0.778     |
| _(for contrast)_ CDF spatial  | 0.914 | 0.945 | 0.971     |

Freq is **last on both datasets at every reliable tier.** More data barely moves it: 3× the data (250→750) shifts AUC ~0.06 then **plateaus at ~0.56**. And its **validation-AUC curve is flat from epoch 1** (BAB IV §4.1.7, **Gambar 4.10/4.11**) → it did not "undertrain," it **never found signal.**

**Cross-dataset, n=750** (AUC / **recall**):

| Direction     | AUC   | **Recall**                      |
| ------------- | ----- | ------------------------------- |
| FFPP→CDF freq | 0.606 | **0.064** (freq's own collapse) |
| CDF→FFPP freq | 0.575 | 0.531                           |

- Note the mirror to spatial: **freq collapses FFPP→CDF** (recall 0.064) while spatial collapses CDF→FFPP. Same mechanism (score distribution sinks past the fixed 0.5 cutoff), different direction — it's a **threshold-calibration artifact under domain shift**, not a total loss of ranking (see `RECALL_COLLAPSE_ANALYSIS.md`).

### ⑦ Why frequency fails — the four causes, each with a citation · **1 hr · CORE**

This is your core defense (thesis Slide 19, BAB IV §4.2.4). Memorize all four, in order of strength:

1. **Preprocessing destroys the artifacts (strongest).** MTCNN face-crop removes edge/background context that carries spectral traces, **and** **c23 compression is a low-pass filter that kills exactly the high-frequency band** where GAN fingerprints live (Mejri `[31]`). _Durall got ~100% because he used **raw, uncompressed** GAN output; we use cropped, c23-compressed frames — the fingerprint is largely gone._ **Visible proof:** in your demo, real vs fake FFT spectra look **indistinguishable** (BAB IV §4.2.4, Gambar 4.2).
2. **Phase is discarded.** Magnitude only. Phase carries most structural info (Oppenheim & Lim `[25]`); SPSL (Liu `[26]`) shows phase catches up-sampling artifacts invisible in magnitude. A **deliberate, flagged** handicap → future work.
3. **CNN spectral / texture bias.** CNNs learn texture and **low** frequencies first (Geirhos `[28]` texture bias; Rahaman `[29]` "F-principle" / spectral bias; Wang `[30]` high-freq ↔ generalization). A weak high-frequency signal is intrinsically hard for a shallow CNN without architectural help.
4. **Over-simplified representation.** A single **raw FFT magnitude map** into a **shallow CNN** is less expressive than SOTA's learned/decomposed frequency spaces — DCT (Giudice `[10]`, Qian `[11]`), FreqNet (Tan `[12]`). → future work.

> **The framing that wins:** "This is **not a contradiction of the literature, it's a boundary condition.** Spectral artifacts are real; _exploiting_ them is **conditional** on representation, fusion design, and test difficulty. We mark exactly _when_ frequency stops helping."

### ⑧ Proving it's NOT under-powered — the rigor that upgrades "failure" to "finding" · **45 min · CORE**

A reviewer's sharpest attack is "your freq net is just too small / under-trained / mis-normalized." You dismantle each:

- **Sample-size sweep = a direct power analysis.** If freq were data-starved, AUC would keep rising with n. It **plateaus at ~0.56** (table above). _(n=100 is noisy — argue the 250→750 trend.)_
- **Architecture control (FreqCNN vs ResNet18).** Swapped in a standard **ResNet18** (11.2M params, **2.6× bigger**) both scratch and ImageNet-pretrained. Every arm still sits at **AUC 0.51–0.63** (`FREQ_BENCHMARK_RESULTS.md`). A bigger/pretrained backbone **can't lift FFT input out of near-chance** → bottleneck = **input information**, not model capacity.
  - ⚠️ **Honest caveat:** cite the **scratch** arm as the clean win (FreqCNN wins 4/4 under matched training). The **pretrained** ResNet18 arm is a **2–2 split** — do **not** claim it as a FreqCNN victory.
- **Multi-seed (3 seeds), std reported.** At reliable tiers freq std is small (~0.007–0.015) → near-chance is **stable**, not a bad run.
- **Identical training budget, no leakage.** Same optimizer/schedule/epochs/early-stopping (val AUC) as spatial; splits **by video ID**. Apples-to-apples.
- **Preprocessing verified.** FFT stats recomputed (fixed the std=3.0 bug). Not a normalization cripple.

---

## 2. Reviewer questions most likely aimed at the FREQUENCY owner

Ranked by likelihood. Answer honestly; frame negatives as findings.

**FQ1. "Explain your frequency representation — walk me through the FFT step."** _(almost certain)_

> "Per frame: grayscale, resize 224, 2-D FFT, `fftshift` so DC is centered, take the **magnitude** spectrum, apply a **Gaussian high-pass** (cutoff 0.15) to emphasize high frequencies, then `log(1+|F|)` to compress the range. That single-channel log-magnitude map is the FreqCNN's input. Phase is not used — a deliberate, documented limitation."

**FQ2. "Your frequency branch is near-random (AUC 0.56). Isn't that just a failed model?"** _(certain — the hard one)_

> "It's a **measured negative result**, and we made sure it's not an artifact of under-powering. Three checks: a **data sweep** (AUC plateaus at ~0.56, so not data-starved), an **architecture swap** to a 2.6×-bigger ResNet18 (still 0.51–0.63, so not capacity), and **verified FFT normalization**. Near-chance survives all three, across 3 seeds. So the limit is the **information content of the compressed, cropped FFT input**, not the network. That's a finding about the domain, not a bug in our code."

**FQ3. "Why does frequency work near-perfectly in papers like Durall but not for you?"** _(certain)_

> "Conditions differ. Durall et al. `[8]` tested **raw, uncompressed GAN output**, where the up-sampling spectral fingerprint is intact. We use **face-cropped, c23-compressed** frames from FaceForensics++/Celeb-DF. Cropping and JPEG/H.264 compression act as a **low-pass filter that erases the high-frequency traces** those methods rely on (Mejri `[31]`). It's the same reason our demo's real-vs-fake spectra look identical."

**FQ4. "Why magnitude only? You cite Oppenheim that phase carries more information."** _(likely — the phase trap)_

> "Two things that don't conflict. Oppenheim & Lim `[25]` is about **perceptual structure** of natural images — phase dominates edges/shapes. Deepfake detection targets **spectral artifacts**, which show up strongly in the **magnitude** (Durall, Frank, Wang). So magnitude is a legitimate artifact channel; phase is **complementary**, not a replacement. We fixed the frequency representation to the **canonical** log-magnitude to keep the _architecture_ comparison controlled, and we flag phase (e.g. SPSL, Liu `[26]`) explicitly as future work. Adding phase would change the research question from 'compare architectures' to 'compare representations.'"

**FQ5. "Walk me through FreqCNN. Why this design and not just a big CNN?"**

> "It's a lightweight stack of **residual conv blocks** — each is Conv3×3→BN→ReLU with a 1×1 shortcut, then MaxPool. Depth 5, base 64 → channels 1→64→128→256→512→512, a 512-d feature vector, ~4.2M params — an order of magnitude smaller than Xception. We kept it light on purpose: the FFT input carries little signal, so a heavier net just overfits. And we **tested** that — a 2.6×-bigger ResNet18 didn't beat it under matched training."

**FQ6. "Frequency looks inverted at n=250 (AUC 0.469 < 0.5). Is your labeling broken?"** _(a trap)_

> "No — that's **small-sample noise**. The n=100/250 test splits are ~15–37 videos, so a near-random model produces sub-0.5 AUCs by chance. We base the analysis on **n≥250** and headline **n=750**, and we state n=100 exclusion as a limitation. The stable read is 'freq ≈ chance,' and the trend from 250→750 confirms it plateaus, not inverts."

**FQ7. "Recall for freq FFPP→CDF is 0.064 — total collapse?"**

> "Same mechanism as the spatial CDF→FFPP collapse: under domain shift the whole score distribution sinks below the fixed 0.5 cutoff, so almost everything is called 'real.' AUC stays ~0.61, meaning the **ranking partly survives** — it's a **threshold-calibration artifact**, not a loss of all ability. A target-calibrated threshold recovers recall. But the near-chance AUC still says transfer is genuinely weak — I won't oversell it."

**FQ8. "What does the high-pass filter actually remove?"**

> "It **suppresses**, not removes. It's `1 − Gaussian`, so only the pure DC term is zeroed; low frequencies pass with reduced weight, high frequencies pass fully. The roll-off is smooth to avoid ringing. We suppress low freq because it mostly encodes global face shape and lighting — less discriminative than the high-frequency band where synthesis artifacts concentrate (Durall `[8]`)."

**FQ9. "If frequency is useless, why include it at all / why isn't this a wasted branch?"**

> "Because measuring 'useless, and why' is the contribution. This is an **ablation**: spatial-only vs freq-only vs hybrid isolates each domain's contribution and answers RM3. A clean negative on the freq branch is exactly what tells the field 'a naive FFT branch doesn't rescue cross-dataset generalization under compression' — and it points to the right future work (phase, DCT/wavelet, full-frame FFT)."

**FQ10. "Why single-channel / grayscale? Don't you lose the color artifacts?"**

> "The FFT branch targets **structural/periodic** spectral artifacts, which are luminance-dominated; a single-channel log-magnitude map is the standard, cacheable representation (Durall, Frank, Wang) and matches FreqCNN's 1-channel input. Color-domain artifacts are the **spatial** branch's job — that's the division of labor in the two-branch design."

---

## 3. Frequency-branch numbers card (keep on your phone)

|                            |                                                                                                                                                                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Representation**         | grayscale → FFT2 → fftshift → \|magnitude\| → Gaussian high-pass (cutoff 0.15) → log1p → **1×224×224** map                                                                                                                                               |
| **Phase**                  | **discarded** (magnitude only) — deliberate, flagged limitation                                                                                                                                                                                          |
| **Model**                  | FreqCNN — residual `FreqBlock` (Conv3×3→BN→ReLU + 1×1 shortcut → MaxPool)                                                                                                                                                                                |
| **Config (results run)**   | `freq_depth=5`, `freq_base_channels=64` → channels **1→64→128→256→512→512**, feature dim **512**                                                                                                                                                         |
| **Params**                 | **~4.2M** (4,217,217) — vs Xception 20.8M                                                                                                                                                                                                                |
| **Normalization**          | per-dataset z-score, FFPP **mean ≈ 5.84 / std ≈ 1.28** (file); old fallback std 3.0 was ~2.3× too big                                                                                                                                                    |
| **Aug (train only)**       | FFT Gaussian noise σ=0.05 · 5%-prob spectral-band masking                                                                                                                                                                                                |
| **In-dataset AUC (n=750)** | FFPP **0.562** · CDF **0.562** (weakest model, both)                                                                                                                                                                                                     |
| **Cross-dataset (n=750)**  | FFPP→CDF AUC 0.606 (recall **0.064**) · CDF→FFPP AUC 0.575 (recall 0.531)                                                                                                                                                                                |
| **Threshold (demo)**       | **0.451** (Youden's J on FFPP val — near 0.5, consistent with near-random)                                                                                                                                                                               |
| **Power checks**           | data sweep plateaus ~0.56 · ResNet18 (2.6× params) still 0.51–0.63 · 3 seeds, small std                                                                                                                                                                  |
| **Key citations**          | Durall **[8]** · Zhang **[9]** · Odena **[21]** · Qian/F³-Net **[11]** · Giudice **[10]** · Tan/FreqNet **[12]** · Oppenheim&Lim **[25]** · SPSL/Liu **[26]** · Geirhos **[28]** · Rahaman **[29]** · Wang **[30]** · Mejri **[31]** · ResNet/He **[5]** |

---

## 4. If you only have one evening

1. **Walk the FFT transform** end to end (FQ1) and know the high-pass is **soft** (FQ8).
2. **Memorize freq AUC ~0.56 + the flat validation curve** and the **four failure causes with citations** (FQ2, FQ3).
3. **Rehearse the "not under-powered" trio** — data sweep, ResNet18 control, verified normalization (FQ2, §1⑧).
4. **Own the phase handicap** as deliberate future work, not an oversight (FQ4).
5. Re-read `sidang_study_notes_detailed_2026-06-25.md` Steps 03 & 07 and `FREQ_BENCHMARK_RESULTS.md` once.

---

## 5. Literature notes worth keeping (for BAB II/V and the Q&A)

These are the references that directly back the freq-branch story. In-text numbers below follow the docx; ⚠️ **verify the [N] against Daftar Pustaka** before sidang — the fact-check flagged in-text/bibliography desync.

- **Durall et al. `[8]` — "Watch your Up-Convolution"** (`thesis_reference/`). GAN up-sampling fails to reproduce the spectral distribution; deviation is in the **high-freq tail** → ~100% detection on **raw** output. Your **justification** for trying FFT _and_ the **contrast** that explains your weak result (they used uncompressed; you use c23 crops).
- **Odena `[21]` / Zhang `[9]`** — checkerboard & spectral artifacts from transposed conv. The mechanism your branch was designed to catch.
- **Mejri `[31]` — "Leveraging High-Frequency Components"** — compression/filtering destroys high-frequency deepfake cues. **The single best citation for failure cause #1.**
- **Oppenheim & Lim `[25]`** (phase carries structure) + **Liu/SPSL `[26]`** (phase surfaces up-sampling artifacts) — back the phase-as-future-work argument. Note: Oppenheim is about **perceptual structure**, not artifact detection — don't let it be turned into "magnitude is worthless."
- **Geirhos `[28]` (texture bias) · Rahaman `[29]` (F-principle / spectral bias) · Wang `[30]` (high-freq ↔ generalization)** — the CNN-bias reason a shallow FreqCNN struggles on a weak high-freq signal (failure cause #3). These 3 are the "teori tambahan BAB II" added 2026-06-17.
- **Qian/F³-Net `[11]` · Giudice/DCT `[10]` · Tan/FreqNet `[12]`** — richer frequency-aware SOTA; frame your raw-FFT-magnitude as the **simple baseline** and these as the future-work direction.
- **He/ResNet `[5]`** — the residual idea inside `FreqBlock`.
- **SpecXNet (Alam `[13]`) · FSBI (Hasanaath `[16]`)** — dual-domain / freq-enhanced related work; cite as **inspiration**, and be precise that they do **not** append FFT as a 4th channel (that's early fusion, which you did not evaluate).

---

## 6. Known quirks to OWN before they're pointed out

- **Docstring vs results config.** `freq_cnn.py`'s docstring says depth=5 → 256-d ~700K; that's for **base=32**. Your run is **base=64 → 512-d, 4.2M**. Quote the config values, not the docstring.
- **`.features` only in hybrid.** The FreqCNN's own classifier head is **bypassed** inside the hybrid; only the 512-d feature vector is used. Standalone `freq` uses the full head.
- **FFT-stats number:** file on disk is **5.84 / 1.28**; some docs say 5.78. Code reads the file live → 5.84 runs. Quote 5.84.
- **Two FFT re-encodes differ by one JPEG hop:** training computes FFT from the saved JPEG crop, the demo from the in-memory crop — immaterial, but be honest if asked.
- **Freq threshold 0.451 ≈ 0.5** — that near-0.5 operating point is itself _evidence_ of near-randomness (no confident cutoff exists), not a tuning mistake.

---

## 7. The demo — the freq-branch things a reviewer can point at live

> Pair this with `sidang_study_guide_DEMO_debug.md` (the full operational guide). This section is **only** the frequency-specific angles. The demo runs all three models side-by-side so the negative result is _visible_ — your branch is the one that's supposed to look weak, and it does.

### What is _yours_ on screen

- The **"FFT spectra" gallery** (`inference._build_visuals` → `_spectrum_to_rgb`, MAGMA colormap) is **exactly the freq/hybrid input** (raw `image_to_fft_logmag`, pre per-dataset z-score). **This is your headline visual proof:** point at it and say _"real and fake spectra are essentially indistinguishable under crop + c23 — that's the human-visible reason the freq branch carries little signal."_ (This panel is **Gambar 4.2** in the thesis.)
- The **freq verdict card** shows the fake-probability bar with a tick at the **0.451** threshold.

### Freq-specific failure modes (map symptom → cause → what to say)

| Symptom                                                  | Cause                                                                         | What to say                                                                                                                                  |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Freq card **near its threshold / flips on tiny changes** | freq is near-random (AUC ~0.56), threshold **0.451 ≈ 0.5**                    | _"Expected — a near-random model has no confident operating point. This is evidence, not a defect."_                                         |
| Freq/hybrid cards show **"⚠︎ FFT calibration estimated"** | `fft_stats.json` missing → fallback mean 5.0/std 3.0 (`inference.py:123-133`) | Copy `outputs/fft_cache/FFPP/fft_stats.json` → `checkpoints/`. **Spatial is unaffected** (RGB-only). Old fallback std 3.0 was ~2.3× too big. |
| Freq says the **opposite** of spatial on an OOD clip     | freq ≈ coin flip; clip is off-distribution                                    | _"Freq alone is near chance, so disagreement is uninformative — that's the finding, and it's why we don't ship freq alone."_                 |
| Freq is **fast but weak**                                | 1-channel FFT input, tiny 4.2M net                                            | latency isn't the point; the point is the flat spectra above it                                                                              |

### Reviewer: "change X and show me" (freq edit points)

- **"Turn off the high-pass"** → `image_to_fft_logmag(..., highpass=False)` in `inference._preprocess`. ⚠️ Say first: _"this diverges from training, so the numbers stop matching the thesis."_
- **"Change the FFT high-pass cutoff"** → `_highpass_mask(cutoff=…)` in `src/fft_utils.py`. Same caveat — it breaks the "matches training" guarantee.
- **"Run just the frequency model"** → in `inference.py` `MODELS_SPEC`, keep only the `("freq", …)` row; the loop in `predict_video` iterates that list.

### The one sentence for the demo

> "The FFT-spectra panel _is_ my defense: you can see for yourself that fake spectra look like real ones after cropping and compression — so the frequency branch has almost nothing to grab, and that's exactly what its ~0.56 AUC reports."
