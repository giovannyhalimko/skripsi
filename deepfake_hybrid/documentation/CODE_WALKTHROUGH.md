# Code Walkthrough — Deepfake Hybrid Detection

Detailed rundown of the whole codebase, following the exact flow the **canonical run**
triggers. The models were most recently (re)trained on a rented GPU box via
`vast_run.sh`; the equivalent Colab notebook `colab_run.ipynb` runs the same pipeline.
Both are thin orchestrators that shell out to the `scripts/*.py` files, so every default
and override here reflects "what was actually run", not just the library defaults.

> **What changed in the vast run vs. the earlier Colab run:** `vast_run.sh` uses
> **`N_SEEDS=3`** (statistical validity) instead of the notebook's 1, and adds a
> **ROC + confusion-matrix step** (`make_roc_cm.py`). A separate `freq_benchmark.sh`
> adds a fourth model (`freq_resnet18`) as a frequency-branch ablation. These are the
> three substantive additions since the previous walkthrough.

---

## 0. Big picture

The project asks one question: **does fusing a spatial CNN (XceptionNet, RGB) with a
frequency-domain CNN (FFT log-magnitude) beat XceptionNet alone at deepfake detection?**

To answer it, three models are trained and compared on two datasets:

| Model     | Input                         | Backbone                          |
|-----------|-------------------------------|-----------------------------------|
| `spatial` | RGB face crop (3×224×224)     | XceptionNet (ImageNet-pretrained) |
| `freq`    | FFT log-magnitude (1×224×224) | small FreqCNN (from scratch)      |
| `hybrid`  | both                          | Xception + FreqCNN, fused         |

A fourth model, **`freq_resnet18`** (ImageNet ResNet18 on the FFT map), exists as an
*ablation* of the frequency branch — it is **not** part of the main matrix; only
`freq_benchmark.sh` trains it (see §11).

Datasets: **FFPP** (FaceForensics++) and **CDF** (Celeb-DF v2). Each model is trained
on each dataset at several sample-size tiers, then evaluated **in-dataset** (test split
of the same dataset) and **cross-dataset** (test split of the *other* dataset) to measure
generalization.

> **Headline result (2026-06-09 Colab run, seed 0):** spatial > hybrid > freq at every
> reliable tier. The proposed hybrid *loses* to the plain XceptionNet baseline — a negative
> result for the thesis hypothesis. The vast run re-runs this with **3 seeds** for
> statistical validity; read the final numbers from the `*_summary.csv` tables (mean/std
> over seeds), not a single seed. (Small n=100 tiers are sampling noise; trust tiers ≥250.)

### One-line data flow

```
Read it top to bottom — each step's output is the next step's input.

STEP 1 ─ extract_frames.py
   videos (.mp4)
        └─▶ frames/<video>/frame_000.jpg, frame_001.jpg, ...   (the actual images)
        └─▶ manifest.csv                                       (1 row per video: id, label, frames_dir)

STEP 2 ─ build_splits.py
   manifest.csv
        └─▶ train.csv + val.csv + test.csv                     (split BY VIDEO, 70/15/15)

STEP 3 ─ compute_fft_cache.py
   frames/*.jpg
        └─▶ fft_cache/*.npy                                    (1 FFT map per frame)
        └─▶ fft_stats.json                                     (mean/std for normalization)

STEP 4 ─ train.py        reads: train.csv + val.csv  ⨁  frames/*.jpg  ⨁  fft_cache/*.npy
   DeepfakeDataset ─▶ batches ─▶ model ─▶ best.pt               (checkpoint with best val-AUC)

STEP 5 ─ run_all.py      reads: best.pt  ⨁  test.csv
   evaluate ─▶ Table1_in_dataset.csv                           (test on SAME dataset)
            ─▶ Table2_cross_dataset.csv                        (test on OTHER dataset)
            ─▶ Table3_generalization_drop.csv                  (F1_in − F1_cross)
            ─▶ *_summary.csv                                   (mean/std over seeds; n_seeds>1)

STEP 6 ─ make_roc_cm.py  reads: best.pt  ⨁  test.csv  ⨁  threshold.json   (inference only)
   ─▶ roc_cm/*_roc.png      (one overlaid ROC per test set)
   ─▶ roc_cm/*_cm_<model>.png + *_metrics.json + *_preds_*.csv

STEP 7 ─ plot_results.py
   Table1/2/3.csv + metrics.json ─▶ plots/*.png
```

The unit of training is a **single frame**, not a video. Splits are done **by video ID**
so that frames from one video never leak across train/val/test.

---

## 1. The orchestrators (`vast_run.sh` / `colab_run.ipynb`)

Both are glue + config; they shell out to the `scripts/*.py` files. `vast_run.sh` is the
script actually used for the most recent run; `colab_run.ipynb` is the Colab-equivalent.

### `vast_run.sh` — the canonical training script

Top-of-file **knobs** (the only lines normally edited):
- `N_SEEDS=3` — matches `config.yaml` (statistical validity). **This is the key difference
  from the notebook's `N_SEEDS=1`.**
- `TIERS="100 250 500 750"` — sample-size tiers, same list for both datasets
- `MAX_FRAMES=100`, `EPOCHS=30`, `FACE_MARGIN=0.3`
- `ROC_SEED=0` — which seed's checkpoints to plot ROC/CM for (representative)

**Config build.** An inline Python block loads `config.yaml`, **auto-tunes** batch/workers
from the detected GPU, applies the notebook-style overrides, and writes `vast_config.yaml`:
- `A100`/`H100`/`vram≥35 GB` → batch 128, workers 8, `compile=True`
- `vram≥14 GB` (4090/3090/A5000/V100/T4…) → batch 64, workers 4, `compile=False`
- otherwise → batch 32, workers 2, `compile=False`
- aborts hard if **no CUDA GPU** is present (refuses to train on CPU).
- Same **fail-fast `assert`** as the notebook for the science-critical keys
  (`freq_depth`, `freq_base_channels`, `early_stop_patience`, `label_smoothing`,
  `fft_noise_sigma`) so `train.py` can't silently fall back to its own defaults.

**Per-tier loop** (`for n in $TIERS`):
- **[A]** `run_pipeline.py --dataset FFPP --n-samples <n> --force-fft --face-crop
  --face-margin 0.3 --pretrained` → extract→split→FFT→train+eval FFPP.
- **[B]** same for CDF.
- **[C]** `run_all.py --dataset both --n-samples <n>` → re-uses the just-trained
  checkpoints (skips training) and fills the **cross-dataset** cells, writing the complete
  `Table1/2/3` (+ `*_summary.csv`, since `n_seeds=3`) for this tier.
- **[D]** `make_roc_cm.py` ×4 (in-dataset FFPP, in-dataset CDF, FFPP→CDF, CDF→FFPP) for
  `seed=ROC_SEED`, inference only (see §10). Each call is wrapped in `|| echo … continuing`
  so a plotting hiccup can't abort the rest of the run.

> ⚠️ **Why [D] runs *inside* the loop:** `manifests/FFPP/test.csv` and `…/CDF/test.csv`
> are **not** tier-tagged — the next tier's preprocessing overwrites them. So the
> correct-tier test split only exists on disk *now*. (Checkpoints and tables *are*
> tier-tagged with `_n<N>`; the manifests are not.)

After all tiers, `plot_results.py` runs over the full tier list. Steps 5/6 of the notebook
(save to Drive) have no analogue — vast outputs stay under `outputs/`.

### `colab_run.ipynb` — the Colab equivalent

Same pipeline, with these differences from `vast_run.sh`:
- `N_SEEDS=1` (seed 0 only) — the earlier canonical results came from here.
- GPU auto-tune covers only T4 (batch 64, workers 2) and A100 (batch 128, workers 8,
  `torch.compile` on); no H100/24 GB/small tiers.
- Writes `colab_config.yaml` instead of `vast_config.yaml`; its assert list also includes
  `accum_steps`.
- No ROC/CM step ([D]); it `cp`s tables/runs to `/content/drive/MyDrive/skripsi_outputs/`
  after each step and zips results at the end.

> ⚠️ **Config drift caveat (see memory):** both orchestrators override `config.yaml`.
> When reproducing, trust the orchestrator's effective config (`vast_config.yaml` /
> `colab_config.yaml`), not the committed `config.yaml`.

---

## 2. Config system & how it propagates

`config.yaml` is the single source of truth, but it gets cloned/patched on the way to a run:

```
config.yaml  ──(orchestrator: base + GPU-tune + overrides)──▶  vast_config.yaml / colab_config.yaml  ← run uses this
run_pipeline.py ──(patch_config: copies + applies CLI overrides)──▶ .pipeline_config.yaml
```

`run_pipeline.py` makes its *own* temp copy `.pipeline_config.yaml` with `--num-workers`,
`--max-frames`, and optional `--epochs`/`--batch-size` applied, hands that path to every
sub-script, and deletes it at the end. So the effective config a training run sees is:
`config.yaml` → `vast_config.yaml` → `.pipeline_config.yaml`.

Canonical config values that matter for the science (from `config.yaml`, carried through):
- `freq_depth: 5`, `freq_base_channels: 64` → the "big" FreqCNN (**~4.2M params**,
  feature_dim **512**), not the tiny committed default. (The inline comment in
  `config.yaml` that says "~2.8M" is stale — see §7 for the actual count.)
- `early_stop_patience: 12`, `label_smoothing: 0.05`, `accum_steps: 2`, `fft_noise_sigma: 0.05`
- `n_seeds: 3` → matches the vast run; `run_all.py` now emits `*_summary.csv`
- `image_size: 224`, `lr: 2e-4`, `weight_decay: 1e-4`, `epochs: 30`

`src/utils.py` provides the shared plumbing: `load_config`, `seed_everything`
(seeds python/numpy/torch + cudnn deterministic), `get_device`, `setup_logging`,
`effective_name` (`"FFPP"` + method `"Deepfakes"` → `"FFPP_Deepfakes"`, used everywhere
to namespace output folders), and `worker_init_fn` (per-worker RNG seeding for dataloaders).

---

## 3. Phase 1 — Frame extraction (`scripts/extract_frames.py`)

**Goal:** turn videos into a flat set of JPEG frames + a video-level `manifest.csv`.

**Video discovery & labeling.** Recursively globs each video extension under the dataset
root. Labels are inferred by keyword matching (`infer_label`):
- checks the **parent directory** parts first, then the filename;
- **fake keywords are checked before real** (e.g. `deepfakes`, `synthesis`, `faceswap`);
- returns `1` (fake), `0` (real), or `None` (unlabeled → skipped).

Keywords come from config per dataset. `--method` (FFPP only) further restricts fakes to a
single manipulation family by substring-matching the path.

**Balanced sampling.** With `--n-samples N` (>0):
- splits candidates into real/fake, shuffles each with a **fixed `Random(42)`** (reproducible),
- takes `N/2` from each class (tops up from the other class if one is short),
- keeps the leftovers as a **reserve pool** to replace videos that fail to decode.
- An **early-stop** during globbing stops scanning once `~3×N` of each class is found, so it
  doesn't walk the entire dataset.

**Per-video extraction (`extract_video_frames`).** For each video:
- opens with OpenCV, **rejects** 0×0 resolution, 0-frame, unreadable, or black first-frame
  (`mean(frame) < 3`) videos — corruption guards;
- samples every `round(video_fps / target_fps)`-th frame (target 5 fps), capped at `max_frames`;
- if `--face-crop`: runs MTCNN per frame, picks the **largest** detected face, expands the
  box by `margin` (0.3), crops; falls back to the full frame when no face is found (and warns);
- writes `frame_000000.jpg`, `frame_000001.jpg`, … into `frames/<eff_name>/<video_id>/`.

`video_id` is the path relative to the dataset root with separators replaced by `_`.

**Parallelism.** Without face crop, uses an `mp.Pool` of N workers. **With face crop it runs
sequentially** because the MTCNN object can't be pickled for multiprocessing (this is why
the canonical `--face-crop` run is the slow part).

**Failure replacement.** Any video that yielded 0 frames is retried with a reserve candidate
of the same label, so the final count stays balanced.

**Output:** `manifests/<eff_name>/manifest.csv` with columns `video_id,label,frames_dir`
(one row per *video*).

> ⚠️ **Manifest portability (see memory):** `frames_dir` stores raw paths with the host
> OS separator. A manifest built on Windows breaks on Linux/Colab. Never copy `outputs/`
> between machines — re-extract.

---

## 4. Phase 2 — Build splits (`scripts/build_splits.py`)

**Goal:** stratified **70/15/15** train/val/test split **by video** (anti-leakage).

- Reads the video-level `manifest.csv`.
- Guards: errors on duplicate `video_id`s; requires ≥4 samples per class (so a stratified
  3-way split is possible).
- Two `train_test_split` calls (sklearn, `random_state=42`, `stratify=label`):
  first peel off 15% test, then peel 15% val out of the remaining 85%.
- Writes `train.csv`, `val.csv`, `test.csv` next to the manifest.

Because the split happens at the **video** level and each row still carries `frames_dir`,
all frames of a given video stay together in one split — no frame from a training video
ever appears in val/test.

> Note: these split CSVs are **overwritten** each time a dataset is preprocessed and are
> **not** tier-tagged. That's why `vast_run.sh` step [D] must plot ROC/CM before the next
> tier overwrites `test.csv` (§1).

---

## 5. Phase 3 — FFT cache (`scripts/compute_fft_cache.py` + `src/fft_utils.py`)

**Goal:** precompute the frequency-domain representation once, so training doesn't redo FFTs.

**Expansion.** The manifest is video-level; this script walks each `frames_dir` and expands
to one row per *frame*, then computes an FFT map per frame in an `mp.Pool`.

**The FFT transform (`image_to_fft_logmag`):**
1. grayscale → resize to 224×224;
2. `fft2` → `fftshift` (DC/low frequencies to center);
3. magnitude `|F|`;
4. **Gaussian high-pass mask** (`_highpass_mask`, cutoff 0.15) multiplies the magnitude to
   *attenuate the low-frequency center*. Rationale: deepfake artifacts (blending seams,
   upsampling grids, GAN fingerprints) live in mid/high frequencies; suppressing the
   dominant low-frequency energy makes those artifacts more salient;
5. `log1p` compresses the huge dynamic range → stored as `.npy` (float32, 224×224).

Output: `fft_cache/<eff_name>/<video_id>/frame_XXXXXX.npy`.

**Normalization stats.** After caching, `compute_fft_stats` samples up to 5000 `.npy` files
and computes the global mean/std, saving `fft_cache/<eff_name>/fft_stats.json`. The dataset
loads this at train time to standardize FFT maps. If the file is missing, the dataset falls
back to hardcoded `mean=5.0, std=3.0` with a warning. **Stats are per-dataset** — FFPP and
CDF each get their own. (Recomputed locally 2026-06-13: mean≈5.78, std≈1.28 — the fallback
std of 3.0 was ~2.3× too large.)

`vast_run.sh` passes `--force-fft` (= the notebook's `RECOMPUTE_FFT=True`), regenerating the
cache every tier (needed whenever `fft_utils.py` changes, e.g. the high-pass cutoff).

---

## 6. The Dataset (`src/deepfake_data.py`)

`DeepfakeDataset` is the heart of data loading. Configured by `DatasetConfig`
(`mode` ∈ {spatial, freq, hybrid, early_fusion}).

**Construction.** Reads a split manifest, and for each video expands to frame-level
`items = (frame_path, label, video_id)`. If a video has more than `max_frames_per_video`
frames, it **subsamples** them with `Random(seed)` (deterministic). Loads `fft_stats.json`
for the FFT-using modes.

**`__getitem__` per mode:**
- **spatial:** load RGB → `spatial_transform` → `(img, label)`.
- **freq:** load the cached FFT `.npy` (1×H×W), standardize `(x-mean)/std`, apply FFT
  augmentation (below) → `(fft, label)`. *(The `freq_resnet18` model reuses this exact mode
  — see §11.)*
- **hybrid:** both branches; returns `({"image": img, "fft": fft}, label)`.
- **early_fusion:** stacks RGB+FFT into a 4-channel tensor (only used if
  `fusion_mode=early_fusion`; the canonical run uses `two_branch`, so this is dormant).

**Spatial transforms (`src/transforms.py`):**
- *train:* resize→`RandomResizedCrop(scale 0.8–1.0)`→`ColorJitter`→(hflip)→`ToTensor`→
  ImageNet-normalize→`RandomErasing(p=0.1)`.
- *eval:* resize→`ToTensor`→normalize only.

**FFT augmentation (train only):**
- additive Gaussian noise, `sigma = fft_noise_sigma` (0.05);
- **spectral masking** with 5% probability: zeroes a random horizontal or vertical frequency
  band, so the model can't over-rely on one band.

**Consistent flip in hybrid.** Critical detail: in hybrid-train mode the spatial transform's
hflip is **disabled** (`include_hflip=False`), and instead `__getitem__` applies the same
random horizontal flip to *both* the RGB tensor (`TF.hflip`) and the FFT tensor
(`torch.flip` on the width axis). This keeps the two branches spatially aligned — flipping
one but not the other would teach the fusion layer a bogus correspondence.

**FFT loading fallback.** `_load_fft` prefers the cached `.npy`; if missing, it recomputes
the FFT on the fly from the image. So training still works (slower) without a prebuilt cache.

---

## 7. The models (`src/models/`)

### `spatial_xception.py`
Thin wrapper over `timm.create_model("xception", ...)`. Three builders:
- `build_xception` — full classifier head, `num_classes=1` (binary, single logit);
- `build_feature_extractor` — `num_classes=0`, returns the 2048-d pooled feature vector
  (used by the hybrid spatial branch);
- `get_feature_dim` — returns 2048.

### `freq_cnn.py`
A small from-scratch CNN over the 1-channel FFT map.
- `FreqBlock` = `Conv3×3 → BN → ReLU`, plus a **residual** 1×1 shortcut (to match channels),
  then `MaxPool(2)` downsampling.
- `FreqCNN` stacks `depth` blocks with channel progression `[base, base·2, base·4, …]`
  capped at **`base·8`**. At the canonical **depth=5, base=64** the cap is `64·8 = 512`, so
  the channels are **`[64,128,256,512,512]`**, feature_dim **512**, **~4.2M params**
  (verified: 4,217,217). *(The class docstring's "depth=5 → 256 / ~700K" example assumes
  `base=32`, not the canonical 64 — don't read it as the run's size.)* The committed default
  (depth=3, base=32) is the tiny ~130K-param version — *not* what the thesis ran.
- Ends with `Dropout2d → AdaptiveAvgPool(1×1)` → a 2-layer MLP classifier.
- `.features` exposes the conv stack (the hybrid branch calls this and flattens, bypassing
  the standalone classifier).

### `freq_resnet18.py` *(new — ablation backbone, see §11)*
`build_freq_resnet18` = `timm.create_model("resnet18", in_chans=1, num_classes=1,
pretrained=True, global_pool="avg")`. With `in_chans=1`, timm adapts the ImageNet `conv1`
weights by averaging across the RGB channels. **~11.2M params** (≈2.7× the FreqCNN). It
consumes the same single-channel FFT input (`mode="freq"`) as `freq`, so it's a drop-in
replacement for the frequency branch. **Not in the main matrix** — only `freq_benchmark.sh`
trains it.

### `hybrid_fusion.py` — `HybridTwoBranch` (the proposed model)
```
RGB  ─▶ Xception feat-extractor (2048) ─▶ Linear→256 ─▶ BN ─▶ ReLU ┐
                                                                    ├─ concat (512)
FFT  ─▶ FreqCNN.features (512) ─▶ flatten ─▶ Linear→256 ─▶ BN ─▶ ReLU ┘
                                                                    │
                                                       SE gate (512→128→512, sigmoid)
                                                                    │
                                           Dropout .5 → Linear 512→128 → ReLU → Dropout .5 → Linear→1
```
- Both branches are **projected to 256-d** (`PROJ_DIM`) so neither dominates by sheer
  dimensionality — note the freq branch's raw feature_dim is 512 at the canonical base=64.
- **SE (Squeeze-and-Excitation) gate** (`reduction=4`, i.e. 512→128→512) learns a per-channel
  multiplicative attention over the fused 512-d vector — the "smart fusion" the thesis
  proposes (vs. naive concat).
- Heavy dropout (0.5) in the head to fight overfitting on small training sets.

`EarlyFusionXception` is the alternative: a 4-channel-input Xception (RGB+FFT stacked).
Dormant in the canonical run.

---

## 8. Phase 4 — Training (`scripts/train.py`)

One process trains one `(model, dataset, seed)`. Models supported: `spatial`, `freq`,
`hybrid`, `early_fusion`, **`freq_resnet18`**. The `freq_resnet18` mode maps to the `freq`
data pipeline and the generic single-input forward path. Key mechanics:

**Loss.** `BCEWithLogitsLoss` with `pos_weight = n_neg/n_pos` (handles class imbalance) and
**label smoothing** applied manually to targets (`y·(1−s)+0.5·s`, s=0.05) to curb
overconfidence on small sets.

**Differential learning rates (AdamW).** Pretrained backbones get a 10× lower LR than freshly
initialized heads:
- *spatial:* backbone @ `lr/10`, FC head @ `lr`.
- *hybrid:* **three groups** — spatial backbone @ `lr/10` (lowest), freq branch @ `lr·0.25`
  (mid), fusion head @ `lr` (highest). This stops the randomly-initialized freq branch from
  swamping the gradients early and destabilizing the pretrained Xception.
- *freq / freq_resnet18 / (early_fusion):* fall into the **`else` branch** — a single flat
  `lr` over all params, **no differential rates**. Note `freq_resnet18` is ImageNet-pretrained
  yet is optimized like a from-scratch model (flat LR, no freeze — see below).

**Backbone freezing.** For the first `FREEZE_EPOCHS = 3`, the (pretrained) spatial backbone
is frozen so the new head/fusion layers warm up first; unfrozen at epoch 4, and the
early-stopping patience counter is reset at that boundary. **Only `spatial`/`hybrid`/
`early_fusion` get freezing** — `freq` and `freq_resnet18` are never frozen.

**LR schedule.** `SequentialLR`: linear warmup over 3 epochs (start factor 0.1) → cosine
decay to `eta_min=1e-6` for the rest.

**Throughput tricks.** mixed precision (`autocast` + `GradScaler`) on CUDA; TF32 enabled for
Ampere+; gradient accumulation (`accum_steps=2`); grad-norm clipping at 5.0; optional
`torch.compile` (large-GPU tier only).

**Selection & stopping.** After each epoch, evaluate on val and track **AUC**. Save
`best.pt` whenever val-AUC improves (unwrapping any `torch.compile` wrapper so the checkpoint
loads on a plain model). The checkpoint embeds its `config` (incl. `freq_depth`/
`freq_base_channels`/`image_size`) so downstream tools rebuild the exact architecture.
**Early stop** after `early_stop_patience=12` epochs without improvement (max 30 epochs).
Writes `train.log` and `metrics.json` (full per-epoch history).

Output: `runs/<model>_<eff_name>_n<N>_seed<S>/{best.pt, train.log, metrics.json}`.

---

## 9. Phase 5/6 — Matrix run, eval & tables (`scripts/run_all.py`)

`run_pipeline.py`'s phase 2 calls this; it's where evaluation and the result tables happen.
The model set is `MODELS_CORE = ["spatial", "freq", "hybrid"]` (+`early_fusion` only if
`fusion_mode=early_fusion`). **`freq_resnet18` is not here** — it never enters the matrix.

For every `seed × train_dataset × model` (seeds = `range(n_seeds)` = **0,1,2** for the vast run):
1. **Train if needed.** If `best.pt` doesn't exist (and the train manifest does), shell out
   to `train.py`. If the checkpoint already exists, **reuse it** — this is why notebook/script
   step [C] can re-run `run_all` cheaply just to fill cross-dataset cells.
2. **Pick a decision threshold** once per (model, train-dataset): run inference on that
   dataset's **val** split and choose the threshold maximizing **Youden's J** (`tpr−fpr`),
   cached in `runs/.../threshold.json`.
3. **In-dataset eval:** run the checkpoint on its own test split with that threshold.
4. **Cross-dataset eval:** run the *same* checkpoint (and *same* val-chosen threshold) on the
   **other** dataset's test split — but only if that dataset's manifest already exists.

> Methodological note: the threshold is chosen on the *training* dataset's val split and then
> applied to the cross-dataset test set. That's a deliberate "no peeking at the target domain"
> choice; it also means cross-dataset accuracy/F1 can look worse than AUC suggests if the
> score distribution shifts.

**Diagnostics.** `eval_checkpoint` logs `mean_prob_for_real` vs `mean_prob_for_fake` and flags
`← INVERTED?` when fakes score lower than reals. On tiny tiers this is **sampling noise**
(n=100 test ≈ 15 videos), not a label bug — see the memory note; trust tiers ≥250.

**Metrics (`src/metrics.py`).** `compute_metrics` returns tp/tn/fp/fn, acc, precision, recall,
F1, and AUC (AUC is threshold-independent; the rest use the chosen threshold). `roc_points`
and `find_optimal_threshold` (Youden) are also defined here and reused by `make_roc_cm.py`.

**Tables written** to `tables/n<N>/`:
- `Table1_in_dataset.csv` — per (model, dataset, seed) in-dataset metrics.
- `Table2_cross_dataset.csv` — train-on-A, test-on-B metrics.
- `Table3_generalization_drop.csv` — `f1_in − f1_cross` per (model, train-dataset): the core
  "how much does each model degrade out-of-domain" number.
- **`*_summary.csv`** — because `n_seeds=3 (>1)`, `run_all.py` now also writes
  `Table1_in_dataset_summary.csv`, `Table2_cross_dataset_summary.csv`, and
  `Table3_drop_summary.csv` with **mean/std over seeds**. (The earlier 1-seed Colab run had
  none of these — this is new in the vast run, and these summaries are the numbers to cite.)

`scripts/eval.py` is a **standalone** single-checkpoint evaluator (reports metrics at both
0.5 and Youden-optimal thresholds; also supports `freq_resnet18`). It is *not* on the
orchestrator path — `run_all.py` does its own eval — but is handy for ad-hoc checks.

---

## 10. Phase D — ROC curves & confusion matrices (`scripts/make_roc_cm.py`)

**New in the vast run.** Pure **inference** over trained checkpoints — no training. Step [D]
of `vast_run.sh` calls it four times per tier (in-dataset FFPP, in-dataset CDF, FFPP→CDF,
CDF→FFPP) for `seed=ROC_SEED=0` only.

**What it does.** Takes one or more `modeltype:checkpoint.pt` specs plus a `--test-manifest`
and `--fft-cache-root`, then for each model:
1. **Rebuilds the architecture from the checkpoint's embedded `config`** (`freq_depth`,
   `freq_base_channels`, `image_size`) — so freq/hybrid match the trained sizes — and loads
   the weights.
2. Runs a forward pass over the test split, collecting per-frame `(y_true, y_prob)`; saves
   them to `<tag>_preds_<model>.csv`.
3. **Resolves the CM threshold** with this precedence: explicit `--threshold` override >
   sibling `threshold.json` / `<model>_threshold.json` next to the checkpoint > Youden's J on
   *this* eval set. In the vast pipeline, [C] has already written each run's `threshold.json`
   (the train-dataset val-optimal threshold), so both in-dataset and cross-dataset CMs use the
   **train-set** threshold — consistent with `run_all.py`'s "no peeking" policy.
4. Computes metrics and emits plots.

**Outputs** (to `outputs/roc_cm/`):
- one **overlaid ROC** per test set (`<tag>_roc.png`) — all models on one axis, AUC in the legend;
- one **confusion matrix** per model (`<tag>_cm_<model>.png`), annotated with the threshold + its source;
- a `<tag>_metrics.json` (AUC, threshold, source, full metrics, preds-CSV path) and the per-model preds CSVs.

**Robustness.** A bad/mismatched checkpoint is **skipped** (caught, logged, recorded in the
metrics JSON) rather than killing the batch; if every model fails, the ROC figure is skipped.
Tags follow `FFPP_in_n<N>`, `CDF_in_n<N>`, `FFPP2CDF_n<N>`, `CDF2FFPP_n<N>`.

> Plot labels are in **Indonesian** (`Acak`, `Prediksi`, `Aktual`, `Kurva ROC`) — these
> figures go straight into the thesis results chapter.

---

## 11. The frequency-branch benchmark (`freq_benchmark.sh` + `freq_resnet18`)

A standalone ablation answering: *would a bigger, ImageNet-pretrained backbone on the FFT map
beat the small from-scratch FreqCNN?* Run **after** `vast_run.sh` (it reuses the n=750
manifests + FFT cache + `vast_config.yaml` already on disk).

Steps:
1. **Train `freq_resnet18`** on FFPP n=750 seed 0 and CDF n=750 seed 0 (`train.py --model
   freq_resnet18 --pretrained`). Same single-channel FFT input as `freq`.
2. **Head-to-head ROC + CM** via `make_roc_cm.py` overlaying `freq` vs `freq_resnet18`,
   in-dataset and cross-dataset, tagged `freqbench_*_n750`.
3. **Parameter-count comparison** printed inline: FreqCNN (~4.2M at depth=5/base=64) vs
   ResNet18-1ch (~11.2M), with the ratio.

Outputs: `runs/freq_resnet18_{FFPP,CDF}_n750_seed0/best.pt` and
`roc_cm/freqbench_*_n750_*.{png,json}`. Because `freq_resnet18` is absent from
`MODELS_CORE`, it never appears in `Table1/2/3` — this benchmark is the only place its numbers
live.

---

## 12. Phase 7 — Plots (`scripts/plot_results.py`)

Headless matplotlib (`Agg`), reads the tables/metrics and emits 300-DPI PNGs into `plots/`:
1. **Training curves** — per (model, dataset, n), train-loss + val-AUC + val-F1 vs epoch,
   **seed 0 only**, from each run's `metrics.json`.
2. **Comparison bars** — grouped F1 & AUC per model, for in-dataset and cross-dataset
   (**averaged over available seeds**).
3. **Generalization drop** — in- vs cross-dataset F1 side by side per model.
4. **Sample-size scaling** — metric vs N line per model (in- and cross-dataset); skipped if
   only one tier.

All readers are defensive (`_read_csv_safe`): missing/empty CSVs are skipped with a warning
rather than crashing, so partial runs still plot what exists.

---

## 13. Output layout (under `output_root`, i.e. `./outputs` on the vast box)

```
outputs/
├── frames/<eff_name>/<video_id>/frame_XXXXXX.jpg
├── fft_cache/<eff_name>/<video_id>/frame_XXXXXX.npy   + fft_stats.json
├── manifests/<eff_name>/{manifest,train,val,test}.csv          (NOT tier-tagged — overwritten per tier)
├── runs/<model>_<eff_name>_n<N>_seed<S>/{best.pt, train.log, metrics.json, threshold.json}
├── tables/n<N>/{Table1_in_dataset, Table2_cross_dataset, Table3_generalization_drop}.csv
│                 + *_summary.csv   (mean/std over seeds; n_seeds>1)
├── roc_cm/{FFPP_in,CDF_in,FFPP2CDF,CDF2FFPP}_n<N>_{roc.png, cm_<model>.png, metrics.json, preds_<model>.csv}
│          + freqbench_*_n750_*   (from freq_benchmark.sh)
└── plots/*.png
```
`<eff_name>` is `FFPP`, `CDF`, or `FFPP_<Method>`.

---

## 14. Conventions, subtleties & gotchas

- **Frame-level samples, video-level splits.** Training operates on frames; the split is on
  videos to prevent leakage. A "sample tier" N counts *videos* (balanced real/fake), not frames.
- **Seeds.** Extraction & splitting always use a fixed `Random(42)` / `random_state=42`.
  The *training* seed comes from the matrix loop (`n_seeds`); **vast run = seeds 0,1,2**, so
  cite the `*_summary.csv` (mean±std). The earlier Colab run was seed 0 only.
- **ROC/CM is seed 0 only.** `make_roc_cm.py` plots `ROC_SEED=0` as the representative seed,
  even though the tables average 3 seeds.
- **Manifests/test splits aren't tier-tagged.** They're overwritten every tier — which is why
  ROC/CM ([D]) runs inside the per-tier loop, before the next tier clobbers `test.csv`.
- **`freq_depth`/`base_channels` must reach the config**, or `train.py` silently builds the
  tiny default FreqCNN. Both orchestrators `assert` they're present — keep that guard. At the
  canonical depth=5/base=64 the FreqCNN is **~4.2M params, feature_dim 512** (not the
  config-comment's stale "~2.8M").
- **Per-dataset FFT stats.** Standardization mean/std differ per dataset; the `fft_stats.json`
  is auto-written after caching and auto-loaded at train time. Don't hand-edit.
- **High-pass FFT is a modeling choice**, not just preprocessing — it biases the freq branch
  toward the mid/high-frequency artifact bands. Changing the cutoff requires `--force-fft`.
- **Manifests aren't portable across OS** (raw separators in `frames_dir`); never copy
  `outputs/` between machines.
- **Tiny tiers are noise.** n=100 test ≈ 15 videos; sub-0.5 AUC / "INVERTED?" there is
  sampling variance. Trust 250/500/750.
- **Face-crop mode is sequential** (MTCNN unpicklable) → the slowest phase of the canonical run.
- **`freq_resnet18` is off the matrix path** — it's an ablation trained only by
  `freq_benchmark.sh`; it appears in `roc_cm/freqbench_*` but never in `Table1/2/3`.
- **The result is negative.** Across reliable tiers spatial > hybrid > freq; the proposed
  hybrid does not beat the XceptionNet baseline. The frequency branch + SE-gated fusion add
  parameters and complexity without a generalization win on these datasets.
```
