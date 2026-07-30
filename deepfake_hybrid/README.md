# Deepfake Hybrid Detection — Experimental Pipeline

End-to-end, reproducible pipeline for the thesis **"Studi Komparatif Kinerja Deteksi Deepfake
Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal."**

It trains and compares four detector types on two benchmarks (FaceForensics++ / **FFPP** and
Celeb-DF v2 / **CDF**), and evaluates both **in-dataset** and **cross-dataset** generalization:

| Model key       | What it is                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `spatial`       | XceptionNet on RGB pixels (ImageNet-pretrained) — spatial-domain baseline   |
| `freq`          | FreqCNN — a lightweight residual CNN on the FFT log-magnitude map           |
| `hybrid`        | **The proposed model** — two-branch late fusion (XceptionNet + FreqCNN) with SE gating |
| `early_fusion`  | XceptionNet on a 4-channel input (RGB + FFT)                                |
| `freq_resnet18` | ResNet18 on the FFT map — ablation baseline used only by `freq_benchmark.sh`|

The pipeline: **videos → face-cropped frames → FFT cache → video-level splits → train → evaluate → tables/plots.**

---

## 1. Repository layout (everything in this folder)

```
deepfake_hybrid/
├── README.md                  ← you are here
├── requirements.txt           ← curated top-level Python dependencies
├── requirements-freeze.txt    ← full pinned environment (pip freeze) for exact reproduction
├── config.yaml                ← MAIN config (paths, hyperparameters, dataset roots) — edit this
├── config.dryrun.yaml         ← tiny config for a fast smoke test (2 epochs, 10 frames)
├── .pipeline_config.yaml      ← auto-generated temp config written by run_pipeline.py (do not edit)
├── command.txt                ← copy-paste quick-start cheat sheet
├── vast_run.sh                ← ⭐ reproduce the full thesis results on a CUDA GPU (see §6)
├── freq_benchmark.sh          ← FreqCNN-vs-ResNet18 ablation, run AFTER vast_run.sh (see §7)
├── colab_run.ipynb            ← ⭐ canonical Colab notebook that produced the reported results
├── colab_train.ipynb          ← older/experimental Colab training notebook
├── colab_ipynb.md             ← notes about the notebooks
├── COLAB_GUIDE.md             ← how to prepare datasets & run on Google Colab
├── CONCLUSION.md              ← summary of experimental conclusions
│
├── src/                       ← library code (imported by every script via sys.path)
│   ├── deepfake_data.py       ← Dataset/DataLoader (loads frames + FFT cache per mode)
│   ├── fft_utils.py           ← FFT log-magnitude computation & normalization
│   ├── transforms.py          ← spatial/frequency augmentations
│   └── models/                ← spatial_xception.py, freq_cnn.py, hybrid_fusion.py, …
│
├── scripts/                   ← runnable entry points (run all of these from THIS folder)
│   ├── run_pipeline.py        ← ⭐ one-command end-to-end pipeline (preprocess → train → eval)
│   ├── download_datasets.py   ← FaceForensics++ downloader (official server)
│   ├── extract_frames.py      ← videos → frames (+ optional MTCNN face crop)
│   ├── build_splits.py        ← stratified train/val/test split BY VIDEO (prevents leakage)
│   ├── compute_fft_cache.py   ← precompute FFT log-magnitude .npy cache (+ dataset stats)
│   ├── train.py               ← train one model on one dataset/sample-size/seed
│   ├── eval.py                ← evaluate a checkpoint (in- or cross-dataset)
│   ├── run_all.py             ← full experiment matrix → result tables
│   ├── plot_results.py        ← plots for the results chapter
│   ├── make_roc_cm.py         ← ROC curves + confusion matrices
│   ├── sample_dataset.py      ← subsample manifests to N videos/dataset
│   ├── diagnose_splits.py     ← sanity-check class balance of the splits
│   ├── build_experiment_excel.py ← collate results into an Excel workbook
│   └── make_*.py              ← figure generators for the thesis (architecture, augmentation, …)
│
├── dataset/                   ← where datasets live + download helpers
│   ├── download_datasets.py (in scripts/) / celeb_df_download.py / face_forensics_dataset_download.py
│   ├── celeb_df_manifest.json
│   ├── sample_videos/         ← 4 tiny real/fake clips for a smoke test
│   ├── dryrun_ffpp/ , dryrun_cdf/ ← drop a couple of clips here for config.dryrun.yaml
│   ├── face_forensics/        ← (you create) FFPP videos, path set in config.yaml
│   └── celeb_df/              ← (you create) Celeb-DF v2 videos, path set in config.yaml
│
├── demo/                      ← interactive Gradio demo (Hugging Face Space) — see §11
├── documentation/            ← logs of model fixes/changes
└── outputs/                   ← ALL generated artifacts (git-ignored; see §10)
```

---

## 2. Requirements

- **Python 3.10–3.13** (developed on 3.13; Colab/HF Space use 3.10).
- **GPU with CUDA** for real training (`vast_run.sh` refuses to run on CPU). A CPU is fine only for
  the tiny smoke test and the demo.
- Core libraries (`requirements.txt`): `torch`, `torchvision`, `timm` (XceptionNet), `opencv-python`,
  `facenet-pytorch` (MTCNN face crop), `scikit-learn`, `pandas`, `numpy`, `Pillow`, `pyyaml`, `tqdm`.
  For an exact environment use `requirements-freeze.txt`.

---

## 3. Setup (initialization)

```bash
cd deepfake_hybrid

# 1. create + activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .\.venv\Scripts\activate         # Windows (PowerShell)

# 2. install dependencies
pip install --upgrade pip
pip install -r requirements.txt    # or: pip install -r requirements-freeze.txt  (exact versions)
```

> **GPU torch:** `pip install torch` gives the default build for your platform. On a CUDA box,
> install the matching CUDA wheel from https://pytorch.org if `torch.cuda.is_available()` is `False`.

Verify the install:
```bash
python -c "import torch, timm, cv2, facenet_pytorch; print('torch', torch.__version__, 'cuda', torch.cuda.is_available())"
```

---

## 4. Data

Datasets are **not** shipped (size + license). Point `config.yaml` at your copies:

```yaml
datasets:
  ffpp: { root: "./dataset/face_forensics" }   # FaceForensics++ videos
  cdf:  { root: "./dataset/celeb_df" }          # Celeb-DF v2 videos
```

Real vs. fake is inferred from folder names via `real_keywords` / `fake_keywords` in `config.yaml`
— adjust these if your folder structure differs.

- **FaceForensics++** — use the official downloader (needs the signed access form / server key):
  ```bash
  python scripts/download_datasets.py --config config.yaml \
      --datasets original Deepfakes Face2Face FaceSwap NeuralTextures FaceShifter \
      --compression c23 --type videos --server EU2
  ```
- **Celeb-DF v2** — request access, then place videos under `datasets.cdf.root`
  (`dataset/celeb_df_download.py` documents the layout).
- **No dataset yet?** Use the bundled clips in `dataset/sample_videos/` (or drop a few clips into
  `dataset/dryrun_ffpp/` and `dataset/dryrun_cdf/`) and run the smoke test in §5.2.

---

## 5. Quick start

### 5.1 One command, end-to-end (`run_pipeline.py`)
Runs preprocessing (frames → FFT cache → splits) then trains + evaluates. This is the easiest way
to train a single configuration:

```bash
# Canonical settings (MTCNN face crop, 100 frames/video) — matches the reported results:
python scripts/run_pipeline.py --n-samples 300 --pretrained --face-crop --face-margin 0.3 --max-frames 100

# If frames/splits/FFT already exist, skip preprocessing:
python scripts/run_pipeline.py --skip-preprocess --pretrained
```
Key flags: `--dataset {FFPP,CDF,both}` (default `both`), `--n-samples N`, `--max-frames`, `--fps`,
`--epochs`, `--batch-size`, `--num-workers`, `--pretrained`, `--face-crop --face-margin 0.3`,
`--skip-preprocess`, `--force-fft`, `--seed`.
> ⚠️ `--face-crop` defaults **off** and `--max-frames` defaults to 50; the reported results use
> `--face-crop` with `--max-frames 100`. Pass them explicitly to reproduce.

### 5.2 Smoke test (no real dataset, ~1 minute on CPU)
Put 1–2 short clips into `dataset/dryrun_ffpp/` and `dataset/dryrun_cdf/` (or reuse
`dataset/sample_videos/`), then:
```bash
python scripts/run_pipeline.py --config config.dryrun.yaml --n-samples 4 --max-frames 5 --epochs 2 --pretrained
```
`config.dryrun.yaml` uses tiny values (batch 2, 2 epochs, 10 frames) and writes to `outputs/dryrun/`.

---

## 6. Reproduce the full thesis results — `vast_run.sh` ⭐

`vast_run.sh` mirrors `colab_run.ipynb` and produces every reported number. **Requires a CUDA GPU.**

**What it does:**
1. Builds `vast_config.yaml` = `config.yaml` + notebook overrides + **GPU auto-tune** (batch/workers by
   VRAM: ≥35 GB → 128, ≥14 GB → 64, else 32).
2. Trains the full matrix: `spatial`, `freq`, `hybrid` × `FFPP`, `CDF` × sample tiers `100 250 500 750`
   × `3 seeds`, with **MTCNN face crop (margin 0.3)** and 100 frames/video.
3. Evaluates in-dataset and cross-dataset, then renders ROC curves + confusion matrices.

**How to run** (edit the KNOBS block at the top first — mainly `PROJECT`):
```bash
# run detached so an SSH drop won't kill it
tmux new -s train
bash vast_run.sh 2>&1 | tee vast_train_$(date +%Y%m%d_%H%M%S).log
# detach: Ctrl-b then d   |   reattach: tmux attach -t train
```
Outputs land in `outputs/` (checkpoints, tables, plots). This is a long run (hours).

---

## 7. Frequency-branch ablation — `freq_benchmark.sh`

A controlled comparison that trains **ResNet18 on the same single-channel FFT input** as FreqCNN, in
two arms (`pretrained` and `scratch`), then overlays ROC/CM against the FreqCNN checkpoints. It shows
FreqCNN wins at ~2.65× fewer parameters.

**Prerequisite:** run `vast_run.sh` first — it needs `vast_config.yaml` plus the `n=750, seed=0`
manifests, FFT cache, and `freq_*_n750_seed0` checkpoints to exist.
```bash
bash freq_benchmark.sh 2>&1 | tee freq_benchmark.log
```

---

## 8. Manual pipeline steps (fine-grained control)

Run these from `deepfake_hybrid/` if you want each stage separately (add `--face-crop --face-margin 0.3`
to steps 1 to match the canonical runs):

```bash
# 1. Extract frames (per video), build a manifest
python scripts/extract_frames.py --config config.yaml --dataset FFPP --fps 5 --max-frames 100 --face-crop --face-margin 0.3
python scripts/extract_frames.py --config config.yaml --dataset CDF  --fps 5 --max-frames 100 --face-crop --face-margin 0.3

# 2. Split by video ID (stratified) — prevents frame leakage across splits
python scripts/build_splits.py --config config.yaml --dataset FFPP
python scripts/build_splits.py --config config.yaml --dataset CDF

# 3. Precompute the FFT log-magnitude cache (+ auto-saves normalization stats)
python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --num-workers 4
python scripts/compute_fft_cache.py --config config.yaml --dataset CDF  --num-workers 4

# 4. Train one model (repeat per model/dataset/seed as needed)
python scripts/train.py --config config.yaml --dataset FFPP --model hybrid --pretrained --n-samples 300 --seed 0

# 5. Evaluate a checkpoint (cross-dataset shown: trained on FFPP, tested on CDF)
python scripts/eval.py --config config.yaml --dataset CDF --model hybrid \
    --checkpoint outputs/runs/hybrid_FFPP_n300_seed0/best.pt

# 6. Full experiment matrix → result tables
python scripts/run_all.py --config config.yaml --pretrained --n-samples 750

# 7. Figures for the results chapter
python scripts/plot_results.py --config config.yaml --n-samples 100,300,600,1000
python scripts/make_roc_cm.py  --config config.yaml
```

`train.py` flags: `--config --dataset --model --n-samples --seed --pretrained --run-suffix --freq-depth --method`.
`eval.py` flags: `--config --dataset --model --checkpoint --pretrained --seed --threshold --method`.

---

## 9. Configuration reference (`config.yaml`)

| Key | Meaning |
|---|---|
| `output_root` | where all artifacts are written (`./outputs`) |
| `frame_sampling_fps` | frames sampled per second of video (5) |
| `max_frames_per_video` | cap on frames per video (**100** for the canonical runs) |
| `image_size` | input resolution (224) |
| `batch_size` / `accum_steps` | per-step batch (64) × accumulation (2) = effective 128 |
| `lr` / `weight_decay` | AdamW base LR (2e-4; backbone uses 10× lower) / 1e-4 |
| `epochs` / `early_stop_patience` | max epochs (30) / early-stop patience on val AUC (12) |
| `label_smoothing` | BCE label smoothing (0.05) |
| `fusion_mode` | `two_branch` (late fusion) or `early_fusion` |
| `n_seeds` | seeds per configuration (3) |
| `freq_depth` / `freq_base_channels` | FreqCNN depth (5) / first-block channels (64) |
| `fft_noise_sigma` | Gaussian-noise sigma for FFT augmentation (0.05; 0 disables) |
| `datasets.{ffpp,cdf}.root` | dataset video roots |
| `datasets.{ffpp,cdf}.{real,fake}_keywords` | folder-name keywords for label inference |

---

## 10. Outputs layout (`outputs/`, git-ignored)

```
outputs/
├── frames/<dataset>/<video_id>/*.jpg      ← extracted (optionally face-cropped) frames
├── fft_cache/<dataset>/…  + fft_stats.json ← FFT log-magnitude cache + normalization stats
├── manifests/<dataset>/{train,val,test}.csv ← video-level splits
├── runs/<model>_<dataset>_n<N>_seed<S>/best.pt ← best checkpoint (selected by val AUC)
├── tables/n<N>/Table1_in_dataset.csv, Table2_cross_dataset.csv, Table3_generalization_drop.csv
├── plots/  ,  roc_cm/                       ← result figures
```

---

## 11. Interactive demo (`demo/`)

A Gradio app that runs the three models on an uploaded face video and shows their verdicts
side-by-side (deployed as a Hugging Face Space). To run locally you need trained checkpoints:

```bash
cd demo
pip install -r requirements.txt
# copy trained weights from outputs/runs into demo/checkpoints/ named:
#   spatial.pt   hybrid.pt   freq.pt   (+ optional *_threshold.json, fft_stats.json)
python app.py
```
Without those `.pt` files the app raises a "Missing checkpoint" error — the weights are the ~80 MB
run artifacts, intentionally not shipped in the code package.

---

## 12. Notebooks / Colab

- **`colab_run.ipynb`** — the canonical notebook that produced the reported results (Drive mount,
  dataset setup, GPU auto-tune, multi-sample-size training loops, saving results back to Drive).
- `colab_train.ipynb` — older experimental training notebook.
- **`COLAB_GUIDE.md`** — step-by-step dataset preparation for Colab.

---

## Notes & reproducibility

- **Splits are by video**, never by frame — no frame from a video appears in more than one split.
- **Face cropping** (MTCNN, margin 0.3) is the canonical setting; the CLI flag defaults off, so pass
  `--face-crop` to reproduce. `run_all.py`/`vast_run.sh` reuse whatever frames are already on disk.
- **FFT normalization stats** are auto-computed after each `compute_fft_cache.py` run and loaded at
  train time from `outputs/fft_cache/<dataset>/fft_stats.json` — no manual step.
- Training uses AdamW, BCEWithLogitsLoss (+ label smoothing), differential LRs (backbone 10× lower),
  3-epoch backbone freeze, warmup→cosine LR, AMP + TF32 on CUDA, gradient accumulation, and
  early stopping on validation AUC. The best checkpoint is chosen by val AUC.
