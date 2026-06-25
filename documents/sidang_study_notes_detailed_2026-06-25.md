# Sidang study notes — deep dive for every step

**Companion to the "Sidang field guide."** The field guide is your one-page mental model; this is the long-form version you actually *read and study* from. Every number here was re-verified against the code, your thesis docs, and the submitted PDF on 2026-06-25.

> ### ⚠️ Corrections to the field-guide card — memorize these, the card is wrong on a few
> The original field guide had some stale figures. The **correct** ones (verified by reading the code and running param counts) are:
>
> | Field-guide card said | Reality (verified) | Where |
> |---|---|---|
> | Xception 22.8M params | **~20.8M** (timm `xception`, exact 20,809,001) | counted live |
> | FreqCNN 4.2M | ✅ 4.2M — correct (config depth=5, base=64 → 4,217,217) | counted live |
> | hybrid ~25.8M | ✅ 25.8M — correct (25,878,570) | counted live |
> | label smoothing 0.02 | **0.05** | `config.yaml:17`, `train.py:268` |
> | early-stop patience 5 | **12** | `config.yaml:15` |
> | warmup 2 epochs | **3 epochs** | `train.py:256` |
> | freq_depth 3 | **5** (base channels 64) | `config.yaml:22-23` |
> | optimizer Adam | **AdamW** | `train.py:200+`, ref [45] |
> | FFT stats mean 5.78 | file on disk = **5.84** (FFPP); CDF = 5.32 | `fft_stats.json` |
> | freeze 3 epochs / cosine→1e-6 | ✅ both correct | `train.py:26`, `train.py:262` |
>
> If a reviewer asks for a param count, **say ~20.8M / 4.2M / 25.8M** and offer to show `sum(p.numel() for p in model.parameters())`. Don't quote 22.8M.

> ### 📌 Canonical run = `deepfake_hybrid/vast_run.sh`
> The reported results come from **`vast_run.sh`** (the GPU reproduction of `colab_run.ipynb`), which builds `vast_config.yaml` = `config.yaml` + overrides. Use *this* as the source of truth for run parameters.
> - **What it overrides:** `max_frames_per_video` → **100** (config default is 50, `vast_run.sh:21,51`); `batch_size` / `num_workers` / `compile_model` → **GPU-auto-tuned** by VRAM (batch **128** on A100/H100, **64** on 4090/3090/V100/T4-class, else 32; `vast_run.sh:36-44`); `fusion_mode` → `two_branch`.
> - **What it does NOT override** (so these keep the `config.yaml` values you memorized): `freq_depth` 5, `freq_base_channels` 64, `early_stop_patience` 12, `label_smoothing` 0.05, `fft_noise_sigma` 0.05, `accum_steps` 2, `lr` 2e-4, `epochs` 30, `n_seeds` 3, `frame_sampling_fps` 5, `image_size` 224. The script fail-fast **asserts** the first five exist in `config.yaml` (`vast_run.sh:62-63`) so they can't silently fall back to a `train.py` default.
> - Tiers = **100 / 250 / 500 / 750**, face margin **0.3**, `--face-crop --pretrained --force-fft` (`vast_run.sh:20,88-97`).

---

## The one sentence everything hangs on

**This thesis is a negative result.** The proposed XceptionNet+FFT hybrid does **not** beat plain XceptionNet, and the frequency branch is essentially a coin flip (AUC ~0.56). Your defense is *not* "look how well it works" — it is "here is *why* frequency fusion fails under these conditions, measured cleanly, and that is legitimate science." Almost every hard question routes back to this. The thesis itself states this explicitly: the frequency branch "cenderung menjadi sumber noise yang menyeret turun performa fusi" (tends to become a source of noise that drags down fusion performance), and **H0 cannot be rejected** (BAB IV §4.2.1, §5.1).

The three authors: Giovanny Halimko, Samuel Onasis, Naomi Prisella — Universitas Mikroskil Medan, defending 2026-06-23. Your declared specialty is the **demo** (Step 08).

---

# Step 00 — The framing (30 min) · CORE

**Goal:** lock in exactly what the thesis *claims* so you never over-promise. If you internalize only one step, make it this one.

### The three research questions (Rumusan Masalah), verbatim from the PDF (p.21–22)

- **RM1 —** "Sejauh mana detektor deepfake berbasis domain spasial murni (XceptionNet) mengalami penurunan performa ketika diuji pada video sintetis dari dataset yang berbeda dengan data pelatihannya?"
  *(How much does a pure spatial detector degrade when tested cross-dataset?)*
  → **Honest answer:** It degrades **substantially**, with a *recall collapse* — worst in the CDF→FFPP direction (recall ≈ 0.07).

- **RM2 —** "Sejauh mana penambahan analisis domain frekuensi (FFT) ... dapat memperkecil penurunan tersebut?"
  *(Does adding FFT reduce that drop?)*
  → **Honest answer:** Only **partially and direction-dependently**, and *even then at the cost of in-dataset performance*. Not a consistent solution.

- **RM3 —** "Seberapa besar kontribusi masing-masing komponen (fitur spasial vs fitur frekuensi) ...?"
  *(Which domain contributes more?)*
  → **Honest answer:** The **spatial domain is the main contributor**. The frequency branch is near random, so the hybrid does not beat pure spatial.

### Tujuan Penelitian (objectives) — note the word "ablation"
1. Implement the hybrid XceptionNet–FFT with late fusion + SE gating.
2. Run an **ablation study** (spatial-only vs freq-only vs hybrid) to isolate each domain's contribution.
3. Evaluate generalization in-dataset (FFPP→FFPP, CDF→CDF) and cross-dataset (FFPP→CDF, CDF→FFPP).

This is the magic word: it's an **ablation / comparative study**, not an improvement study. You isolate contributions; a clean negative result *is* the contribution.

### Hypothesis — you must be able to state this
- **H1 (alternative):** adding FFT yields better cross-dataset generalization than pure XceptionNet.
- **H0 (null):** no meaningful generalization gain from FFT; hybrid does not exceed spatial.
- **Verdict in the thesis: H0 cannot be rejected; H1 is not supported by consistent evidence.** (PDF §5.1)
- Stance on statistics (Slide 20): differences are discussed **descriptively** over 3 seeds; you do **not** claim statistical significance you did not test.

### The 30-second pitch (rehearse word-for-word)
> "Kami melakukan **studi komparatif**: membandingkan tiga model — spasial (XceptionNet), frekuensi (FreqCNN), dan hybrid. Tujuannya **mengukur kontribusi domain frekuensi**, terutama untuk generalisasi lintas dataset. Hasilnya: model spasial paling kuat, cabang frekuensi nyaris setara tebakan acak, dan hybrid tidak mengungguli spasial. Temuan utama kami adalah **hasil negatif yang terjelaskan secara ilmiah** — pada konfigurasi yang diuji, FFT tidak membantu, bahkan bisa jadi sumber noise."

**Four keywords that must surface in every answer:** *komparatif · kontribusi · generalisasi lintas dataset · hasil negatif yang dianalisis.*

**Read:** `documents/sidang_speaker_script_slide_16-23.md`, `documents/PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md`, PDF abstract (p.7) + Bab I (p.21–23).

---

# Step 01 — The problem domain (1 hr)

**Goal:** explain, in plain language, what a deepfake is, why detection generalizes poorly, and the in-dataset vs cross-dataset distinction. Then know your two datasets cold — their asymmetry explains most of your results.

### Plain-language framing
- A **deepfake** = a face image/video synthesized or manipulated by a generative model (GAN / autoencoder / diffusion). Detection = binary classification (real vs fake) at the **frame** level here.
- **Why detection generalizes poorly:** a detector learns the *artifact signature of the specific generators it trained on* (a particular up-sampling pattern, blending seam, compression interaction). A new dataset uses different generators and capture conditions, so those learned artifacts don't transfer. This is **domain shift** (theory: Ben-David et al., ref [46]).
- **In-dataset** = train and test on the same dataset (FFPP→FFPP). **Cross-dataset** = train on one, test on the other (FFPP→CDF). Cross-dataset is the honest test of generalization and is where everything collapses.

### Your two datasets — the asymmetry is the whole story
| | **FaceForensics++ (FFPP)** ref [7], Rössler et al. 2019 | **Celeb-DF v2 (CDF)** ref [18], Li et al. CVPR 2020 |
|---|---|---|
| Manipulation methods | **4** (Deepfakes, Face2Face, FaceSwap, NeuralTextures) | **1** high-quality celebrity face-swap |
| Diversity | **Heterogeneous** — 4 artifact types | **Homogeneous** — one polished method |
| Compression | **c23** (the standard high-quality benchmark) | high quality |
| Sampling here | 50/50 real/fake, video-level splits | 50/50 real/fake, video-level splits |

**Why this matters (say this when asked about the cross-dataset asymmetry):**
- Train on **CDF** (one homogeneous method) → the model learns a *narrow* artifact pattern → it fails badly on FFPP's four different methods → **CDF→FFPP collapses hardest** (spatial recall 0.074).
- Train on **FFPP** (four methods) → the model sees more varied artifacts → it transfers *somewhat* better to CDF.
- So the direction of degradation is not random; it's a direct consequence of source diversity. This is in-dataset success (CDF AUC 0.971!) masking a brittle, narrow representation.

**Citations:** FaceForensics++ [7]; Celeb-DF [18]; domain-shift theory Ben-David [46]. (Note: the Celeb-DF paper PDF is in your `thesis_reference/` folder, just added.)

---

# Step 02 — The data pipeline (2 hr) · FOUNDATIONAL

**Goal:** trace one video → one training batch, and nail the single most-asked question: **why split by video, not by frame?**

### The end-to-end flow
1. **Video → frames** (`scripts/extract_frames.py`)
2. **Frames → face crops** (`src/face_utils.py`, MTCNN, margin 0.3) — done during extraction when `--face-crop` is set
3. **Frames → FFT `.npy` cache** (`scripts/compute_fft_cache.py` → `src/fft_utils.py`)
4. **Manifest → train/val/test split by video** (`scripts/build_splits.py`)
5. **`DeepfakeDataset` loads frame + FFT + applies per-mode transforms** (`src/deepfake_data.py`)

### 1. Frame extraction — `scripts/extract_frames.py`
- Decoded with OpenCV `cv2.VideoCapture`. Default target **5 FPS** (`--fps`, line 115).
- **Sampling interval** (`extract_frames.py:81`): `frame_interval = max(round(native_fps / target_fps), 1)`. A 30-fps source at 5 FPS → keep every 6th frame.
- **Max frames cap** default 100 (`--max-frames`, line 116); `0` = unlimited. **The canonical run (`vast_run.sh`) uses `max_frames_per_video = 100`**, overriding the `config.yaml` default of 50.
- Saved as JPEG `frame_{n:06d}.jpg` at native (or cropped) resolution — **no resize at extraction**; resize happens later in the transform.
- Sanity gates: rejects unopenable / 0×0 / 0-frame / black videos (`np.mean(first_frame) < 3`, line 74).
- `video_id` = dataset-relative path with separators replaced by `_` (line 36-37). Labels via keyword match (`real_keywords`/`fake_keywords` in `config.yaml`).

### 2. Face cropping — `src/face_utils.py` (MTCNN, ref [47])
- Detector: **MTCNN** from `facenet-pytorch` with `keep_all=True`, **`min_face_size=60`** px, cascade thresholds `[0.6, 0.7, 0.7]`, `post_process=False` (lines 8-17).
- Converts BGR→RGB *before* detection (line 27) — OpenCV is BGR, MTCNN wants RGB.
- **Largest face by area** is selected (lines 35-37).
- **Margin 0.3**: each side expanded by 30% of the box dimension, clamped to frame bounds (lines 40-44). Net crop ≈ 1.6× the raw box. *Why margin?* to keep blending/boundary context where seam artifacts live — but note (Step 07) this still discards background frequency context.
- **No-face fallback:** keep the **full uncropped frame** and increment `no_face_count` (no second pass). The crop is variable-size; the fixed 224×224 resize happens in the transform.

### 3. Splits — `scripts/build_splits.py` — ⭐ THE must-answer question
- Ratio **70 / 15 / 15**, two-stage `train_test_split`, `stratify=df["label"]`, seed 42 (lines 52-53).
- **Critical: the split operates on the manifest, where each row is ONE VIDEO.** So you partition *videos*, never individual frames. All frames of a given video stay in exactly one split.

> **Why split by video, not by frame? (rehearse this — it's the #1 pipeline question)**
> Consecutive frames from one video are near-identical (same identity, lighting, background, same manipulation). If you split at the *frame* level, frames from the same source video land in **both** train and test. The model then **memorizes the video's appearance** and "recognizes" it at test time — giving ~99% test accuracy that is pure leakage and ~50% (chance) in the real world. Splitting **by `video_id`** guarantees test videos are genuinely unseen, so the metric measures generalization, not memorization.

- Integrity guards: duplicate-`video_id` check raises (protects the guarantee); min 4 videos per class required for a stratified 70/15/15 split.

### 4. Dataset & transforms — `src/deepfake_data.py`
- **One item per frame**, expanded from each video row. Per-video frame cap with a seeded random subsample (`max_frames_per_video`; **canonical run = 100**, `config.yaml` default 50).
- **FFT cache load** (`_load_fft`): reads `{video_id}/{frame}.npy`, returns `(1, H, W)` single-channel tensor; computes on the fly if cache miss.
- **FFT z-score normalization** is applied **here**, not in `fft_utils.py`: `(fft - mean) / std` with per-dataset stats from `fft_stats.json` (line 129). Fallback constants 5.0 / 3.0 if the file is missing (the old std=3.0 was ~2.3× too large — fixed).
- **ImageNet normalization** (mean `[0.485,0.456,0.406]`, std `[0.229,0.224,0.225]`) and **resize to 224×224** live in `src/transforms.py` (`get_spatial_transform`).
- **Per-mode return:** `spatial`→`(rgb, label)`; `freq`→`(fft, label)`; `early_fusion`→4-channel stacked tensor; `hybrid`→`{"image":rgb,"fft":fft}` + label.
- **Augmentation (train-only):** RGB RandomResizedCrop / ColorJitter / flip / RandomErasing; FFT Gaussian noise (σ=0.05) and 5%-probability spectral-band masking. For **hybrid**, horizontal flip is applied **consistently to both branches** (one random decision flips RGB via `TF.hflip` *and* FFT via `torch.flip(dims=[-1])`) so the two views stay spatially aligned — independent flips would desync them (lines 152-156). At inference all augmentations are off (correct).

**Read in order:** `scripts/extract_frames.py` → `src/face_utils.py` → `scripts/build_splits.py` → `src/deepfake_data.py`.

---

# Step 03 — The FFT / frequency domain (2 hr) · CORE

**Goal:** read `src/fft_utils.py` line by line. This is the artifact at the heart of the thesis. Be fluent on every step and why it's there.

### The exact transform (`image_to_fft_logmag`, lines 22-33)
```
grayscale ("L")  →  resize 224×224  →  np.fft.fft2  →  np.fft.fftshift
  →  np.abs  (magnitude ONLY — phase discarded, line 29)
  →  × Gaussian high-pass mask (cutoff 0.15)
  →  np.log1p
  →  float32
```
Output is **224×224, single channel**. (A torch twin `tensor_fft_logmag` exists for on-the-fly compute; algorithmically identical.)

| Step | Why it's there |
|---|---|
| **Grayscale** | Spectral forgery artifacts are luminance-structural, not color; one channel keeps it simple. |
| **fft2 + fftshift** | 2-D Fourier transform; `fftshift` moves the DC (zero-frequency) term to the image center so low freq = center, high freq = edges. |
| **Magnitude only** (`np.abs`) | Keeps spectral *energy* per frequency. **Phase is thrown away** — remember this, it's failure cause #2. |
| **Gaussian high-pass, cutoff 0.15** | Suppresses the dominant low-frequency energy so the CNN can focus on the high-frequency band where GAN up-sampling fingerprints live. |
| **log1p** | Compresses the huge dynamic range of FFT magnitude (DC dwarfs everything) into a learnable scale. `log1p` = `log(1+x)`, safe at 0. |
| **z-score (later, in dataset)** | Standardizes the cache to ~zero-mean/unit-var per dataset so the CNN sees consistent input scale. |

### The high-pass mask (`_highpass_mask`, lines 9-19) — be ready for "how is it built?"
- `sigma = cutoff * size = 0.15 × 224 = 33.6 px`.
- `mask = 1.0 - exp(-dist² / (2·sigma²))` where `dist` is distance from center.
- It's **1 − (Gaussian low-pass)**: value **0 at the DC center** (fully suppress low freq), rising smoothly to ~1 at the edges (pass high freq). So it attenuates the low-frequency dominance and lets the high-frequency artifact band through.

### Why FFT *should* expose deepfakes (the literature you're testing)
- GANs use **transposed-conv / up-sampling**, which leaves periodic **high-frequency spectral fingerprints** — checkerboard-like grid artifacts (Odena ref [21]; Durall et al. ref [8]: "CNN-based generators fail to reproduce spectral distributions"; Zhang et al. ref [9]).
- Frequency-aware detectors exploit this: F³-Net / "Thinking in Frequency" (Qian, ref [11]), DCT-based methods (Giudice ref [10]), FreqNet (Tan ref [12]). Your study asks: *does a simple FFT branch capture this and help fusion?* Answer: not under these conditions.

### ⚠️ The deliberate handicap: phase is discarded
- Line 29 keeps `np.abs(...)` only. The complex **phase is never used.**
- **Oppenheim & Lim (ref [25], "The Importance of Phase in Signals", Proc. IEEE 1981)** showed phase carries *most* of an image's structural information — you can reconstruct a recognizable image from phase alone but not from magnitude alone.
- **SPSL (Liu et al., ref [26], CVPR 2021)** is a deepfake method that explicitly *uses* phase to catch up-sampling artifacts invisible in magnitude.
- You **own this deliberately** as failure cause #2 and an explicit future-work recommendation (Step 07). It's foreshadowed in your own methodology (Slide 12): "Informasi fase tidak kami pakai. Keputusan desain ini kelak menjadi salah satu penjelasan mengapa cabang frekuensi gagal."

### FFT normalization stats (exact, on disk)
| Dataset | mean | std |
|---|---|---|
| FFPP | **5.84** (5.8410) | **1.28** (1.2767) |
| CDF | **5.32** (5.3173) | **1.21** (1.2123) |

(The demo's docs say 5.78 from an earlier recompute; the file on disk says 5.84. Quote **5.84** for FFPP, and if challenged, note it's read live from `fft_stats.json` so the model always uses whatever the file holds.)

**Read:** `src/fft_utils.py` (line by line), `outputs/.../fft_stats.json`.
**Citations:** Durall [8], Zhang [9], Odena [21], Qian/F³-Net [11], Giudice [10], Tan/FreqNet [12]; phase: Oppenheim & Lim [25], SPSL/Liu [26].

---

# Step 04 — The three models (2 hr)

**Goal:** know the hybrid flow cold, and the *why* behind each design choice. All param counts verified live.

### Spatial — `src/models/spatial_xception.py` (ref [6], Chollet)
- Backbone: **timm `xception`**, ImageNet-pretrained. Depthwise-separable convolutions (that's Xception's whole idea — factorize spatial and channel convolution).
- Feature dim **2048** (global-avg-pooled); classifier head outputs **1 logit** (binary, BCEWithLogits).
- **~20.8M params** (exact 20,809,001). *Not 22.8M — correct the card if needed.*

### Frequency — `src/models/freq_cnn.py`
- Input: **single-channel** FFT log-magnitude (224×224).
- Building block `FreqBlock`: `Conv3×3 → BN → ReLU` + **residual** 1×1 shortcut, then `MaxPool2d(2)`.
- **Configurable depth/channels** via `freq_depth` / `freq_base_channels`. The **results run uses depth=5, base=64** (`config.yaml:22-23`) → channel progression `1→64→128→256→512→512`, **feature dim 512**, **~4.2M params** (4,217,217).
- (The constructor *default* is depth=3/base=32 → 128-dim, ~112K — the docstring's "~130K". But that's not what the experiments use. Cite **512-dim, 4.2M.**)
- Standalone it has its own classifier head; **inside the hybrid only `.features` is used** (the classifier is bypassed).

### Hybrid — `src/models/hybrid_fusion.py` (the one to know cold)
```
RGB (3×224×224) → Xception features → 2048 → spatial_proj: Linear(2048→256)+BN+ReLU → 256
FFT (1×224×224) → FreqCNN.features → 512  → freq_proj:    Linear(512→256)+BN+ReLU  → 256
concat([256, 256]) → 512 → SE gate (channel reweighting) → classifier:
    Dropout(0.5) → Linear(512→128) → ReLU → Dropout(0.5) → Linear(128→1) → 1 logit
```
- **~25.8M params** (25,878,570) = spatial extractor 20.8M + FreqCNN features 4.2M + projections/SE/head (~0.85M).

**Q: Why project both branches to 256? (symmetric bottleneck)**
> Raw dims are wildly asymmetric — spatial 2048 vs freq 512. Concatenating them directly lets the 2048-dim spatial branch *dominate* the fusion (and the gradient flowing back to the freq branch becomes negligible — this is exactly what caused the original collapse, see Step 07). Projecting **both to 256** equalizes their contribution (256+256), adds BatchNorm for scale normalization, and gives the SE gate a balanced 512-dim vector to weight. It's what makes late fusion *fair* between modalities.

**Q: What does the SE gate do? (ref [38], Hu et al., Squeeze-and-Excitation)**
> It's channel attention on the 512-dim fused vector. **Squeeze:** `Linear(512→128)` (reduction=4) summarizes cross-channel interactions. **Excitation:** `Linear(128→512) → Sigmoid` produces a per-channel gate weight in (0,1). **Reweight:** multiply the fused vector by those gates (`x * gate(x)`). The intent is to let the network *down-weight* the useless frequency channels and *up-weight* the good spatial ones per input — adaptive branch weighting.
> **The honest punchline (say this):** in our results the SE gate **fails to fully suppress** the near-random frequency branch, so the hybrid still underperforms pure spatial. Adding a gate was the right idea; it wasn't enough.

**Q: What's `early_fusion`?**
> An alternative: a single Xception with **`in_chans=4`** (RGB + FFT stacked at the input). It exists in code (`EarlyFusionXception`) but was **not the focus** — input-level fusion can't *isolate* each domain's contribution, which is the whole point (RM3 ablation). The late-fusion two-branch design lets you ablate spatial-only vs freq-only vs hybrid.

**Read:** `src/models/spatial_xception.py`, `freq_cnn.py`, `hybrid_fusion.py`.
**Citations:** Xception/Chollet [6]; SE-Net/Hu [38]; ResNet/He [5] (for the residual idea in FreqBlock).

---

# Step 05 — Training details (1.5 hr)

**Goal:** justify every hyperparameter. The theme: *random-init branches must not blow up the pretrained backbone.* All values are the **actual `config.yaml`/`train.py` values** (the CLAUDE.md summary is stale on several).

### Loss
- **`BCEWithLogitsLoss` with `pos_weight`** (`train.py:185`), `pos_weight = n_neg / n_pos` computed from the train manifest (auto-handles class imbalance).
- **Label smoothing 0.05** (`config.yaml:17`), applied manually: `targets = targets*(1-0.05) + 0.05*0.5` (`train.py:111`). Prevents over-confident logits / improves calibration. *(Card said 0.02 — wrong.)*

### Optimizer + differential learning rates — **AdamW** (ref [45], Loshchilov & Hutter)
| Param group | LR | Why |
|---|---|---|
| Spatial backbone | **2e-5** (`base/10`) | pretrained ImageNet features — nudge gently, don't destroy them |
| Freq branch | **5e-5** (`base×0.25`) | random init — needs to move, but not dominate gradients |
| Fusion head (proj+SE+classifier) | **2e-4** (`base`) | random init, top of the net — learn fastest |

> **Why differential LRs? (rehearse)** The backbone is pretrained and valuable; the freq branch and fusion head are random. A single high LR would let the random branches' large early gradients *overwrite* the pretrained backbone (this was a documented cause of the original collapse). Lower LR on the backbone preserves transferable ImageNet features.

### Backbone freezing
- **`FREEZE_EPOCHS = 3`** (`train.py:26`): spatial backbone frozen for the first 3 epochs (head/freq/fusion train), then **unfrozen at epoch 4**. On unfreeze, the early-stop counter resets so fine-tuning gets a full window. Lets the fusion head stabilize before the backbone starts moving.

### LR schedule
- **Linear warmup 3 epochs** (start factor 0.1 → 1.0) → **cosine decay** to **eta_min = 1e-6** via `SequentialLR` (`train.py:255-262`). *(Card said warmup 2 — it's 3.)*

### Numerics & batching
- **AMP** (mixed precision) on CUDA; **TF32** enabled for Ampere+ (A100).
- **Gradient accumulation = 2** (`config.yaml`, not overridden by the canonical run).
- **Batch size is GPU-auto-tuned in the canonical run** (`vast_run.sh:36-44`): **128** on A100/H100 (VRAM ≥35 GB), **64** on a 4090/3090/V100/T4-class (VRAM ≥14 GB), else 32. With accum ×2 → **effective batch 256 / 128 / 64**, *not* 32. The `config.yaml` default 16 (→ effective 32) only applies if you run *without* the GPU auto-tune.
  - ⚠️ **BAB IV §4.1.1 says "batch efektif 32"** — that matches the un-tuned config default, not the GPU run. **Reconcile this before the defense:** confirm which GPU the canonical results ran on, then either correct BAB IV to the real effective batch or be ready to explain that 32 describes the config baseline. If asked live, the safe answer is *"effective batch was GPU-dependent via auto-tuning; the config baseline is 32."*
- **Gradient clipping max-norm 5.0** (`train.py:117`).

### Early stopping & checkpointing
- Metric: **validation AUC**; best checkpoint = highest val AUC → `best.pt` (`train.py:296`).
- **Patience 12**, **max 30 epochs** (`config.yaml:14-15`). *(Card said patience 5 — it's 12.)*

### Experiment matrix
- **3 seeds: 0, 1, 2.** Tiers **100 / 250 / 500 / 750** for both datasets. Main analysis trusts **250/500/750** (n=100 is noise — see Step 06). **n=750 is the headline tier.**

**Read:** `scripts/train.py`, `config.yaml`.
**Citations:** Adam [44], AdamW [45], BCE/optimization basics Goodfellow [41].

---

# Step 06 — Results (1.5 hr) — memorize the headline numbers

**Goal:** have the n=750 table and three killer facts on instant recall. All numbers are mean over seeds 0/1/2, frame-level, matching BAB IV exactly.

### In-dataset AUC, n=750 (the table to memorize)
| Dataset | Spatial | Hybrid | Freq |
|---|---|---|---|
| **FaceForensics++** | **0.778** | 0.644 | 0.562 |
| **Celeb-DF** | **0.971** | 0.919 | 0.562 |

**Ranking: Spatial > Hybrid > Freq — on both datasets, at every reliable tier.** The hybrid *loses to its own baseline.* That's the thesis.

### The ranking holds across tiers (AUC)
| | n=250 | n=500 | n=750 |
|---|---|---|---|
| FFPP spatial | 0.743 | 0.693 | 0.778 |
| FFPP hybrid | 0.540 | 0.616 | 0.644 |
| FFPP freq | 0.469 | 0.545 | 0.562 |
| CDF spatial | 0.914 | 0.945 | 0.971 |
| CDF hybrid | 0.787 | 0.839 | 0.919 |
| CDF freq | 0.500 | 0.549 | 0.562 |

### Cross-dataset, n=750 — where everything collapses (AUC / **recall**)
| Direction | Model | AUC | **Recall** |
|---|---|---|---|
| FFPP→CDF | spatial | 0.678 | 0.637 |
| FFPP→CDF | hybrid | 0.665 | 0.599 |
| FFPP→CDF | freq | 0.606 | **0.064** (freq collapses here) |
| CDF→FFPP | spatial | 0.607 | **0.074** (precision 0.923!) |
| CDF→FFPP | hybrid | 0.555 | 0.142 |
| CDF→FFPP | freq | 0.575 | 0.531 |

All cross-dataset AUCs compress to **0.56–0.68**. The **recall collapse** is the dramatic finding: spatial CDF→FFPP predicts almost everything "real" (recall 0.074, precision 0.923) → it only fires "fake" when extremely sure, missing 93% of fakes.

### Generalization drop (ΔF1, n=750) — the one place hybrid "helps"
| Model | Train | F1 in | F1 cross | Δ |
|---|---|---|---|---|
| spatial | FFPP | 0.705 | 0.614 | +0.091 |
| **hybrid** | **FFPP** | 0.606 | 0.594 | **+0.012** (smallest drop) |
| spatial | CDF | 0.906 | 0.137 | +0.769 (worst) |
| hybrid | CDF | 0.834 | 0.238 | +0.597 |

> **The honest nuance (RM2):** FFT *does* reduce the generalization drop — but **only FFPP→CDF** (ΔF1 +0.012 vs spatial +0.091), and it's bought by a much lower in-dataset score (0.606 vs 0.705). It does **not** hold the other direction. So FFT helps *inconsistently and at a cost* — exactly what RM2's honest answer says.

### The three killer facts
1. **Spatial > Hybrid > Freq** at every reliable tier, both datasets.
2. **Freq is stuck at ~0.56** regardless of data size, and its **validation AUC curve is flat from epoch 1** (BAB IV §4.1.7, Gambar 4.10) → it never learned, it wasn't undertrained.
3. **n=100 is noise** (next step).

### Don't get trapped: n=100 is statistical noise
The n=100 test split is ~15 videos. Sub-0.5 "inverted" AUCs there (e.g. FFPP freq 0.469 at n=250) are **sampling artifacts**, not label bugs. Trust **n≥250**. If a reviewer points at a weird small-tier number, this is your answer — and the thesis already states it as a limitation (n=100 excluded from main analysis).

**Read:** `outputs/tables/n750/` (Table1/2/3 + `*_summary.csv`), `documents/BAB_IV_Hasil_dan_Pembahasan_2026-06-17.md`.

---

# Step 07 — Why frequency fails — the core defense (1 hr) · CORE

**Goal:** the four reinforcing causes, each with its citation, plus the framing that wins. This is Slide 19 ("SLIDE INTI PERTAHANAN") and Q11.

### The framing that wins: **boundary condition, not contradiction**
> "Ini **bukan kontradiksi, melainkan kondisi batas** — a boundary condition. Frequency artifacts are real (Durall [8], Zhang [9]). What we show is that *exploiting* them is **conditional** — on representation, fusion design, and test difficulty. We don't deny the literature, we **complement it** by marking exactly when frequency fails to help." A clean, explained negative result stops others repeating the dead end.

### The four causes (memorize all four, in order of strength)

**① Preprocessing destroys the artifacts** — *Mejri [31]*
MTCNN face-cropping removes edge/background context that carries spectral traces, **and** c23 compression suppresses exactly the high-frequency band where GAN fingerprints live. Mejri et al. ([31]) document that compression destroys high-frequency cues. **Qualitative proof:** in your own demo, real vs fake FFT spectra are **visually indistinguishable** (BAB IV §4.2.4).

**② Phase is discarded** — *Oppenheim & Lim [25]; SPSL/Liu [26]*
You use magnitude only. Phase carries most structural information (Oppenheim & Lim [25]); SPSL (Liu [26]) proves phase catches up-sampling artifacts invisible in magnitude. You handicapped the branch — deliberately, and you flag it. → future work.

**③ CNN spectral / texture bias** — *Geirhos [28]; Rahaman [29]; Wang [30]*
CNNs learn **texture and low frequencies first** (Geirhos [28] = texture bias; Rahaman [29] = spectral bias / "F-principle"; Wang [30] = high-freq helps generalization). A weak high-frequency signal is intrinsically hard for a shallow CNN to capture without architectural help.

**④ Over-simplified representation** — *vs DCT/wavelet SOTA*
A single **raw FFT magnitude map** fed to a **shallow CNN** is not expressive enough. SOTA uses richer frequency-aware decompositions — DCT (Giudice [10], Qian [11]), learned frequency spaces (Tan/FreqNet [12]). → future work.

### The mechanism: why this drags the *hybrid* down
freq ≈ random, so concatenating it **injects noise** into the fused features. The SE gate was meant to suppress it but **can't fully** → fusion ≤ spatial. The thesis says it plainly (§4.2.1): the frequency branch "cenderung menjadi sumber noise yang menyeret turun performa fusi."

### Context: the collapse analysis doc is OLDER than the final model
`analyze/Hybrid_Model_Collapse_Analysis_2026-03-14_1600.md` describes the **original (pre-fix)** architecture — plain 2048:64 concat (96.97% spatial!), per-image FFT min-max norm, no scheduler, no freezing, no differential LR — which **catastrophically collapsed** (hybrid CDF→FFPP F1 = 0.038, AUC 0.506). You then **fixed** it: symmetric 256-d projections + SE gate, differential LRs, freeze-then-unfreeze, cosine schedule, **global FFT z-score** (the stats fix), Youden's-J thresholds. The fixes **stopped the catastrophic collapse but did not make frequency informative** — which is precisely the final negative result.

> **If asked "did your fixes accomplish anything?"** → "Yes — they stopped the catastrophic cross-dataset collapse (F1 0.038 → competitive). But they did **not** make frequency discriminative. That tells us the limitation is in the *domain/representation*, not the training code — which strengthens, not weakens, our conclusion."

**Read:** `analyze/Hybrid_Model_Collapse_Analysis_2026-03-14_1600.md`, BAB IV §4.2.4.

---

# Step 08 — The demo (1.5 hr) · CORE · YOUR SPECIALTY

**Goal:** total fluency. You can be asked anything here. The headline: the demo runs all three models side-by-side so the negative result is *visible*, and its preprocessing matches training **verbatim**.

### What it is
- **Gradio** app (`demo/app.py`) for **HuggingFace Spaces** (free CPU tier; `DEVICE = "cpu"` in `inference.py:43`).
- User **uploads a face video** → gets back: (1) three **verdict cards** side-by-side, (2) a **face-crop gallery** (what spatial sees), (3) an **FFT-spectrum gallery** (what freq/hybrid see), (4) frame/face-count info.
- **The point** (`app.py:5-7`): showing all three side-by-side makes the negative result self-evident — hybrid doesn't beat spatial, and the FFT panel shows real vs fake spectra look the same.

### Checkpoints
- `spatial.pt`, `hybrid.pt`, `freq.pt` in `demo/checkpoints/` — all **FFPP, n=750/class, seed 0** (`outputs/runs/{model}_FFPP_n750_seed0/best.pt`).
- Built with `pretrained=False` (the checkpoint overwrites all weights → no timm download → offline-safe). FreqCNN/hybrid depth+base read from the **checkpoint's embedded config**, not the drifted `config.yaml`.

### Thresholds — per-model, **Youden's J on the validation split** (not 0.5)
- Loaded from `{model}_threshold.json` (falls back to 0.5 if missing):
  - **spatial 0.127** · **hybrid 0.229** · **freq 0.451**
- Derivation (`scripts/run_all.py:79-94` → `src/metrics.py:35-39`): run inference on the FFPP **val** manifest, compute ROC, take `argmax(tpr − fpr)` = **Youden's J**, save to `threshold.json`, copy into the demo.

> **Why not 0.5?** The models aren't calibrated to a 0.5 boundary; the optimal operating point (max TPR−FPR) differs per model. Spatial's 0.127 means it needs only weak evidence to call "fake"; freq's 0.451 is near 0.5 — consistent with freq being near-random (no confident operating point exists). Tuned on **validation**, never test — no leakage.

### Inference flow (`inference.predict_video`, `@torch.no_grad()`)
1. **Sample frames:** `interval = max(round(vfps/5), 1)` → **5 FPS**, capped at **16 frames** (CPU latency).
2. **MTCNN crop, margin 0.3** (full-frame fallback if no face) — same `src/face_utils.py` as training.
3. **Per frame build two tensors:** RGB via `get_spatial_transform(train=False)` (Resize 224 → ToTensor → ImageNet norm); FFT via `image_to_fft_logmag(size=224, highpass=True)` then z-score with `fft_stats.json`.
4. **Batched inference:** spatial(rgb), freq(fft), hybrid(rgb, fft).
5. **Aggregate:** `prob = sigmoid(logits).mean()` over frames → one video-level prob per model; `is_fake = prob >= threshold`.

### ⭐ "Does the demo match training?" → **Yes, verbatim**
Same 5 FPS · margin 0.3 · resize 224 · ImageNet norm · FFT high-pass cutoff 0.15 + per-dataset z-score — all through the **shared `src/` modules**, so there's no drift by construction. The **only** differences are **train-only augmentations being off** (RandomResizedCrop, ColorJitter, flip, RandomErasing, FFT noise, band-masking) — which is **correct for inference**.
- Two honest, immaterial nuances if pressed: (a) training computes FFT from the saved JPEG crop, the demo from the in-memory crop → differ by one JPEG re-encode; (b) the docs quote FFT mean 5.78 but the file on disk is **5.84** (the code reads the file, so it always uses the live value).

### The "what the models see" panel — your visual proof
- Up to 4 evenly-spaced frames. **Face-crop gallery** = exactly the RGB the spatial model ingests. **FFT-spectrum gallery** = `image_to_fft_logmag` min-max scaled + MAGMA colormap.
- **This is the negative result made visible:** reviewers can see for themselves that **real and fake FFT spectra are essentially indistinguishable** under crop+c23 — the human-visible reason the freq branch (and thus the hybrid) carries little signal.

### cards.py
- Pure stdlib (no torch/gradio → unit-testable). Each card: model label, 🔴 FAKE / 🟢 REAL badge, a confidence bar with a tick at the decision threshold, and raw `fake-prob` / `thr` to 3 decimals. Shows "⚠︎ FFT calibration estimated" on freq/hybrid cards if `fft_stats.json` fell back to defaults.

**Read:** `demo/app.py`, `demo/inference.py`, `demo/cards.py`.

---

# Step 09 — Drill the hardest questions (daily)

**Goal:** make the five decisive answers reflexive. Loop this every day until sidang. The guiding principle: **jujur > defensif** (honest beats defensive) — if it's a negative result, frame it as a *finding*, and always return to *"we compared, we didn't promise an improvement."*

### Q1. "Your hybrid is worse than the baseline. How is that a contribution?"
> "It's a **comparative / ablation study**, not an improvement study. A rigorously explained negative result is valid science: it maps **when** FFT fusion helps and when it doesn't, challenges the common assumption that 'adding FFT must help' with quantitative evidence, and stops others walking into the same dead end. In science, knowing what *doesn't* work — and *why* — is as valuable as a positive result." *(Q18/Q19)*

### Q2. "How do you know frequency truly failed, not just a bad implementation?"
> "Three proofs: (1) freq AUC is flat at **~0.56 across every data size** — more data doesn't help; (2) its **validation AUC is flat from epoch 1** — it never learned, it wasn't undertrained; (3) the demo's spectra panel shows real vs fake FFT maps are **visually indistinguishable** under crop+c23. And on 'bad implementation' specifically — **that under-engineering *is* our finding**: a naive magnitude-only FFT into a shallow CNN is insufficient, and we name exactly what's needed (phase, attention fusion, richer decompositions). We acknowledge the limitation *and* show it's part of the contribution." *(Q20)*

### Q3. "You discarded phase — didn't you handicap yourself?"
> "Yes, deliberately, and we flag it openly. Magnitude-only is one of our **four documented failure causes** (Oppenheim & Lim show phase carries most structural information; SPSL proves it's exploitable for deepfakes). It's an explicit **future-work recommendation** — SPSL-style phase use. We don't hide it; we foreshadow it in the methodology." *(Q11 cause 2)*

### Q4. "Spatial also collapses on CDF→FFPP (recall 0.074) — so the problem is deeper than frequency?"
> "Correct — and that's exactly **RM1**. The spatial collapse is **domain shift**: CDF is one homogeneous synthesis method, so a model trained on it learns a narrow artifact pattern and fails on FFPP's four methods. This is a **fundamental, unsolved problem in deepfake detection** that affects *all* models — it's not specific to frequency. In fact it's the **motivation** for the whole study: we asked whether FFT could fix it (RM2), and the honest answer is it only helps partially, in one direction, at a cost. The spatial collapse doesn't undercut the thesis — it *is* the problem the thesis set out to probe." *(RM1 + Q14)*

### Q5. "Only 3 seeds, n=750, c23 compression — is that enough?"
> "We acknowledge the limits openly: we report **mean ± std over 3 seeds** and do **not** claim statistical significance we didn't test (that's named future work — Wilcoxon/paired t-test). But the **ranking spatial > hybrid > freq is consistent across every seed and every tier (250/500/750)** — so the *direction* isn't luck. c23 is the standard FaceForensics++ benchmark; varied compression is recommended future work." *(Q20a + Slide 20)*

### Bonus mechanism question — "Why exactly is the hybrid not better?"
> "hybrid = spatial (good) + frequency (≈ random). Concatenating a near-random branch **injects noise** into the fused features. The SE gate was designed to down-weight useless channels, but in our results it **can't fully suppress** the bad branch — so fusion ends up ≤ spatial. Adding something random to something good doesn't add information; it can subtract." *(Q12 + Q5 SE-not-enough)*

---

## Numbers to keep on a card (corrected)
| | |
|---|---|
| **FFT transform** | gray → resize 224 → fft2 → fftshift → \|mag\| → highpass(0.15) → log1p → z-score |
| **High-pass** | Gaussian, cutoff 0.15 → σ = 33.6 px; mask = 1 − Gaussian (0 at DC, 1 at edges) |
| **FFT stats** | FFPP mean **5.84** / std **1.28** · CDF mean **5.32** / std **1.21** |
| **Splits** | 70/15/15, stratified by **video** (seed 42) |
| **Frame sampling** | 5 FPS · MTCNN margin 0.3 · min face 60 px · resize 224 · max **100** frames/video (canonical; config default 50) |
| **Demo** | ≤16 frames @ 5 FPS · thresholds (Youden J): spatial **0.127** / hybrid **0.229** / freq **0.451** |
| **Params** | Xception **~20.8M** · FreqCNN **~4.2M** (depth5/base64) · hybrid **~25.8M** |
| **Hybrid dims** | RGB 2048→256, FFT 512→256, concat 512 → SE gate → 512→128→1 |
| **Loss** | BCEWithLogits + pos_weight + label smoothing **0.05** |
| **Optimizer** | **AdamW**, LR backbone 2e-5 / freq 5e-5 / head 2e-4 |
| **Schedule** | warmup **3** ep → cosine to 1e-6; freeze backbone 3 ep then unfreeze |
| **Batch** | GPU-auto-tuned (`vast_run.sh`): 128 (A100/H100) / 64 (4090-class) / 32 (small) · accum ×2 → eff. 256/128/64 · (config default 16 → eff. 32; BAB IV says 32) |
| **Stopping** | best by val AUC · patience **12** · max 30 epochs · clip 5.0 |
| **Headline AUC (n=750)** | FFPP 0.778/0.644/0.562 · CDF 0.971/0.919/0.562 (spatial/hybrid/freq) |
| **Worst collapse** | spatial CDF→FFPP recall **0.074** (precision 0.923) |

## Thesis citation quick-map (so you cite the right reference number)
Xception **[6]** Chollet · FaceForensics++ **[7]** Rössler · GAN spectral **[8]** Durall, **[9]** Zhang · DCT anomalies **[10]** Giudice · F³-Net "Thinking in Frequency" **[11]** Qian · FreqNet **[12]** Tan · Celeb-DF **[18]** Li · checkerboard artifacts **[21]** Odena · phase **[25]** Oppenheim & Lim · SPSL **[26]** Liu · texture bias **[28]** Geirhos · spectral bias **[29]** Rahaman · high-freq generalization **[30]** Wang · high-freq for deepfakes **[31]** Mejri · SE-Net **[38]** Hu · Adam **[44]** / AdamW **[45]** · domain-shift theory **[46]** Ben-David · MTCNN **[47]** Zhang K.

> **Note:** there is **no "Frank et al."** in your bibliography — the GAN-spectral claim rests on **Durall [8]**. And the Daftar Pustaka has several name typos (Cozzolino→"Cozzoliono", Zhao→"Zaho", Giudice→"Guidice", Honggang Qi→"Q. Honggang", Papadopoulos→"Papadopoulus", Loshchilov→"Loschilov"). Cite the **correct** names out loud even though the document misspells them.
