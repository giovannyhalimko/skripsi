# Running the Deepfake Hybrid Detection Pipeline on Google Colab

## Prerequisites

### 1. Datasets in Google Drive

You need two datasets uploaded to your Google Drive before starting.

**FaceForensics++ (FFPP)**

Request access at [faceforensics.com](https://github.com/ondyari/FaceForensics), then download using:

```bash
python download_datasets.py . -d original Deepfakes Face2Face FaceSwap NeuralTextures -c c23 -t videos
```

Upload the resulting folder to Drive. Expected structure:

```
MyDrive/ffpp/
├── original_sequences/
│   └── youtube/c23/videos/*.mp4          ← real videos
└── manipulated_sequences/
    ├── Deepfakes/c23/videos/*.mp4        ← fake
    ├── Face2Face/c23/videos/*.mp4        ← fake
    ├── FaceSwap/c23/videos/*.mp4         ← fake
    └── NeuralTextures/c23/videos/*.mp4   ← fake
```

**Celeb-DF v2 (CDF)**

Download from the [authors' GitHub](https://github.com/yuezunli/celeb-deepfakeforensics). Upload the zip to Drive:

```
MyDrive/skripsi/deepfake_hybrid/dataset/celeb_df/Celeb-DF-v2.zip
```

After extraction, the expected layout:

```
Celeb-DF-v2/
├── Celeb-real/*.mp4        ← real celebrity videos
├── YouTube-real/*.mp4      ← real YouTube videos
└── Celeb-synthesis/*.mp4   ← fake synthesis videos
```

### 2. Project Code in Google Drive

Your project repo should be in Drive:

```
MyDrive/skripsi/
└── deepfake_hybrid/
    ├── config.yaml
    ├── scripts/
    ├── src/
    └── ...
```

---

## Quick Start (One Command Per Experiment)

If you just want to run everything, follow Steps 1–4 below, then use `run_pipeline.py`:

```python
# Smoke test (~5 min) — verify everything works
!python scripts/run_pipeline.py --n-samples 50 --max-frames 10 --epochs 1 --pretrained

# Thesis experiments
!python scripts/run_pipeline.py --n-samples 50  --max-frames 100 --epochs 10 --pretrained
!python scripts/run_pipeline.py --n-samples 200 --max-frames 100 --epochs 10 --pretrained
!python scripts/run_pipeline.py --n-samples 400 --max-frames 100 --epochs 10 --pretrained
```

Each command runs the full pipeline: extract frames → build splits → FFT cache → train all 3 models on both datasets → evaluate in-dataset + cross-dataset → generate result tables.

---

## Detailed Step-by-Step

### Step 1 — Open Colab and Set GPU

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. File → Upload notebook → select `colab_train.ipynb`, OR create a new notebook
3. **Runtime → Change runtime type → T4 GPU**

### Step 2 — Mount Drive and Copy Code

```python
from google.colab import drive
drive.mount('/content/drive')
```

```python
import os

# Copy project code from Drive to local SSD (faster I/O)
CODE_IN_DRIVE = "/content/drive/MyDrive/skripsi"   # <-- EDIT THIS
!cp -r "{CODE_IN_DRIVE}" /content/skripsi

os.chdir("/content/skripsi/deepfake_hybrid")
!pwd && ls
```

### Step 3 — Install Dependencies

```python
# timm and scikit-learn are not pre-installed on Colab
!pip install -q timm scikit-learn tqdm opencv-python-headless pyyaml

# ffmpeg is needed for OpenCV to decode H.264/H.265 .mp4 files
!apt-get install -qq ffmpeg libavcodec-extra

# Verify GPU
import torch
print("CUDA available:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")
```

Expected output:
```
CUDA available: True
Device: Tesla T4
```

### Step 4 — Copy Datasets to Local SSD

Reading directly from Drive during training is extremely slow. Always copy datasets to `/content/` first.

```python
import os

# ── FFPP: copy folder from Drive ──────────────────────────────────────
FFPP_IN_DRIVE = "/content/drive/MyDrive/ffpp"   # <-- EDIT THIS

print("Copying FFPP from Drive (may take 5-15 minutes)...")
!cp -r "{FFPP_IN_DRIVE}" /content/ffpp
print("Done.")

# Verify
for label, path in [
    ("real", "/content/ffpp/original_sequences/youtube/c23/videos"),
    ("fake (Deepfakes)", "/content/ffpp/manipulated_sequences/Deepfakes/c23/videos"),
    ("fake (Face2Face)", "/content/ffpp/manipulated_sequences/Face2Face/c23/videos"),
]:
    if os.path.isdir(path):
        count = len([f for f in os.listdir(path) if f.endswith(".mp4")])
        print(f"  OK  {label}: {count} .mp4 files")
    else:
        print(f"  MISSING  {label}: {path}")
```

```python
# ── CDF: unzip from Drive ─────────────────────────────────────────────
CDF_ZIP = "/content/drive/MyDrive/skripsi/deepfake_hybrid/dataset/celeb_df/Celeb-DF-v2.zip"  # <-- EDIT THIS

print("Unzipping Celeb-DF-v2 from Drive (may take 5-10 minutes)...")
os.makedirs("/content/celeb_df", exist_ok=True)
!unzip -q "{CDF_ZIP}" -d /content/celeb_df
print("Done.")

# Flatten if extracted into a wrapper subfolder
import shutil
from pathlib import Path

celeb_root = Path("/content/celeb_df")
subdirs = [d for d in celeb_root.iterdir() if d.is_dir()]
expected = {"Celeb-real", "YouTube-real", "Celeb-synthesis"}

if subdirs and not expected.intersection({d.name for d in subdirs}):
    wrapper = subdirs[0]
    print(f"Flattening wrapper folder '{wrapper.name}'...")
    for item in wrapper.iterdir():
        shutil.move(str(item), str(celeb_root / item.name))
    wrapper.rmdir()

# Verify
for subdir in ["Celeb-real", "YouTube-real", "Celeb-synthesis"]:
    p = celeb_root / subdir
    if p.exists():
        mp4s = list(p.glob("*.mp4"))
        print(f"  OK  {subdir}: {len(mp4s)} .mp4 files")
    else:
        print(f"  MISSING  {subdir}")
```

### Step 5 — Update config.yaml

```python
import yaml

CONFIG_PATH = "/content/skripsi/deepfake_hybrid/config.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

# Point to local SSD copies
cfg['datasets']['ffpp']['root'] = "/content/ffpp"
cfg['datasets']['cdf']['root'] = "/content/celeb_df"
cfg['output_root'] = "/content/outputs"

# Training settings
cfg['batch_size'] = 16       # reduce to 8 if you get CUDA OOM
cfg['num_workers'] = 2       # 2 works well on Colab
cfg['epochs'] = 10           # 10 for thesis experiments
cfg['lr'] = 1e-4
cfg['weight_decay'] = 1e-4
cfg['image_size'] = 224
cfg['n_seeds'] = 1

# Keywords for label inference
cfg['datasets']['ffpp']['real_keywords'] = [
    "original", "real", "pristine", "actors", "youtube"
]
cfg['datasets']['ffpp']['fake_keywords'] = [
    "fake", "manipulated", "deepfakes", "faceswap",
    "neuraltextures", "deepfakedetection", "faceshifter", "face2face"
]
cfg['datasets']['cdf']['real_keywords'] = ["real", "authentic", "youtube"]
cfg['datasets']['cdf']['fake_keywords'] = ["fake", "synthesis", "deepfake"]

with open(CONFIG_PATH, 'w') as f:
    yaml.dump(cfg, f, sort_keys=False)

print("Config updated. Key values:")
print(f"  FFPP root:    {cfg['datasets']['ffpp']['root']}")
print(f"  CDF root:     {cfg['datasets']['cdf']['root']}")
print(f"  Output root:  {cfg['output_root']}")
print(f"  Batch size:   {cfg['batch_size']}")
print(f"  Epochs:       {cfg['epochs']}")
print(f"  LR:           {cfg['lr']}")
```

### Step 6 — Run the Full Pipeline

**Option A: One command per experiment size (recommended)**

```python
os.chdir("/content/skripsi/deepfake_hybrid")

# ── Smoke test first (~5 min) ────────────────────────────────────────
!python scripts/run_pipeline.py \
    --n-samples 50 \
    --max-frames 10 \
    --epochs 1 \
    --pretrained
```

If the smoke test passes, run the real experiments:

```python
# ── n=50 (~15 min on T4) ─────────────────────────────────────────────
!python scripts/run_pipeline.py \
    --n-samples 50 \
    --max-frames 100 \
    --epochs 10 \
    --pretrained
```

```python
# ── n=200 (~50 min on T4) ────────────────────────────────────────────
!python scripts/run_pipeline.py \
    --n-samples 200 \
    --max-frames 100 \
    --epochs 10 \
    --pretrained
```

```python
# ── n=400 (~2 hours on T4) ───────────────────────────────────────────
!python scripts/run_pipeline.py \
    --n-samples 400 \
    --max-frames 100 \
    --epochs 10 \
    --pretrained
```

```python
# ── n=1000 (~5 hours on T4, optional for extended study) ─────────────
!python scripts/run_pipeline.py \
    --n-samples 1000 \
    --max-frames 100 \
    --epochs 10 \
    --pretrained
```

**What each run produces:**

For each `--n-samples N`, the pipeline creates:
- `outputs/runs/{model}_{dataset}_n{N}_seed0/best.pt` — best model checkpoint
- `outputs/runs/{model}_{dataset}_n{N}_seed0/metrics.json` — per-epoch validation metrics
- `outputs/runs/{model}_{dataset}_n{N}_seed0/train.log` — training log
- `outputs/tables/n{N}/Table1_in_dataset.csv` — in-dataset results
- `outputs/tables/n{N}/Table2_cross_dataset.csv` — cross-dataset results
- `outputs/tables/n{N}/Table3_generalization_drop.csv` — F1 generalization drop

**Option B: Run steps individually (for debugging or partial runs)**

```python
os.chdir("/content/skripsi/deepfake_hybrid")
N = 400  # change this for each experiment

# 1. Extract frames
!python scripts/extract_frames.py --config config.yaml --dataset FFPP --fps 5 --max-frames 100 --n-samples {N}
!python scripts/extract_frames.py --config config.yaml --dataset CDF  --fps 5 --max-frames 100 --n-samples {N}

# 2. Build splits
!python scripts/build_splits.py --config config.yaml --dataset FFPP
!python scripts/build_splits.py --config config.yaml --dataset CDF

# 3. Compute FFT cache
!python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --num-workers 2
!python scripts/compute_fft_cache.py --config config.yaml --dataset CDF  --num-workers 2

# 4. Train all models + eval + tables
!python scripts/run_all.py --config config.yaml --pretrained --n-samples {N}
```

### Step 7 — View Results

```python
import pandas as pd

for n in [50, 200, 400]:
    for table in ["Table1_in_dataset", "Table2_cross_dataset", "Table3_generalization_drop"]:
        path = f"/content/outputs/tables/n{n}/{table}.csv"
        try:
            df = pd.read_csv(path)
            print(f"\n{'='*60}")
            print(f"  {table} (n={n})")
            print(f"{'='*60}")
            pd.set_option('display.float_format', '{:.4f}'.format)
            print(df.to_string(index=False))
        except FileNotFoundError:
            pass
```

### Step 8 — Save Everything Back to Drive

**IMPORTANT: Always run this before closing the Colab session. Everything in `/content/` is deleted when the session ends.**

```python
import shutil
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
DRIVE_OUT = f"/content/drive/MyDrive/skripsi_outputs/{timestamp}"
os.makedirs(DRIVE_OUT, exist_ok=True)

LOCAL_OUT = "/content/outputs"

# Save checkpoints (largest, most important)
runs_src = Path(LOCAL_OUT) / "runs"
if runs_src.exists():
    shutil.copytree(runs_src, f"{DRIVE_OUT}/runs")
    print(f"  Checkpoints saved -> {DRIVE_OUT}/runs/")

# Save result tables
tables_src = Path(LOCAL_OUT) / "tables"
if tables_src.exists():
    shutil.copytree(tables_src, f"{DRIVE_OUT}/tables")
    print(f"  Tables saved      -> {DRIVE_OUT}/tables/")

# Save manifests/splits
manifests_src = Path(LOCAL_OUT) / "manifests"
if manifests_src.exists():
    shutil.copytree(manifests_src, f"{DRIVE_OUT}/manifests")
    print(f"  Manifests saved   -> {DRIVE_OUT}/manifests/")

# Save config used
shutil.copy2(
    "/content/skripsi/deepfake_hybrid/config.yaml",
    f"{DRIVE_OUT}/config.yaml"
)
print(f"  Config saved      -> {DRIVE_OUT}/config.yaml")

# Print summary
print(f"\nAll outputs saved to: {DRIVE_OUT}")
total_mb = sum(f.stat().st_size for f in Path(DRIVE_OUT).rglob("*") if f.is_file()) / 1_048_576
print(f"Total size: {total_mb:.1f} MB")
```

---

## Time Estimates

| Sample size | Frame extraction | FFT cache | Training (6 runs) | Total |
|-------------|-----------------|-----------|-------------------|-------|
| n=50 | ~3 min | ~2 min | ~10 min | **~15 min** |
| n=200 | ~10 min | ~8 min | ~30 min | **~50 min** |
| n=400 | ~20 min | ~15 min | ~90 min | **~2 hours** |
| n=1000 | ~45 min | ~30 min | ~4 hours | **~5 hours** |

Training = 3 models (spatial, freq, hybrid) x 2 datasets (FFPP, CDF) = 6 training runs per sample size.

Free Colab sessions disconnect after ~4-6 hours of idle time or ~12 hours total. For n=1000+, consider Colab Pro.

---

## Resuming After a Disconnection

If your session dies mid-run, reconnect and:

```python
from google.colab import drive
drive.mount('/content/drive')

# Re-copy code
!cp -r "/content/drive/MyDrive/skripsi" /content/skripsi

import os
os.chdir("/content/skripsi/deepfake_hybrid")

!pip install -q timm scikit-learn tqdm opencv-python-headless pyyaml
!apt-get install -qq ffmpeg libavcodec-extra

# Re-copy datasets to local SSD
!cp -r "/content/drive/MyDrive/ffpp" /content/ffpp
!unzip -q "/content/drive/MyDrive/skripsi/deepfake_hybrid/dataset/celeb_df/Celeb-DF-v2.zip" -d /content/celeb_df

# If you saved outputs from a previous run, restore them
PREVIOUS_RUN = "/content/drive/MyDrive/skripsi_outputs/YYYYMMDD_HHMMSS"  # <-- EDIT THIS
!cp -r "{PREVIOUS_RUN}/runs" /content/outputs/runs 2>/dev/null
!cp -r "{PREVIOUS_RUN}/manifests" /content/outputs/manifests 2>/dev/null

# Re-run config update (Step 5 above), then:
# --skip-preprocess skips frame extraction/splits/FFT if manifests already exist
!python scripts/run_pipeline.py --skip-preprocess --n-samples 400 --epochs 10 --pretrained
```

Note: `run_all.py` automatically skips models that already have a `best.pt` checkpoint, so partially completed runs will resume from where they left off.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `CUDA out of memory` | Batch too large for T4 (16GB) | Set `batch_size: 8` in Step 5 |
| Empty manifest (0 videos) | Folder names don't match label keywords | Run the debug cell below |
| `OpenCV can open: False` | Missing ffmpeg codecs | Re-run `apt-get install ffmpeg`, restart runtime |
| All videos labeled `unknown` | Real/fake keyword mismatch | Check exact folder names match `real_keywords`/`fake_keywords` in config |
| `FileNotFoundError: manifest` | Skipped frame extraction | Run `extract_frames.py` first |
| `duplicate video_id` in `build_splits.py` | Multiple videos with same stem name | Re-run `extract_frames.py` (the updated code generates unique IDs) |
| Slow copy from Drive | Normal Drive I/O | Wait. FFPP can take 10+ min. |
| Session disconnects mid-training | Colab timeout | See "Resuming After a Disconnection" above |
| SSL error downloading Xception weights | Certificate issue | Add: `import ssl; ssl._create_default_https_context = ssl._create_unverified_context` |
| `No module named 'deepfake_data'` | Old code version | Make sure you copied the latest code from Drive (after the master merge) |

### Debug Cell — Run If Frame Extraction Fails

```python
import cv2, glob

for ds, root in [("FFPP", "/content/ffpp"), ("CDF", "/content/celeb_df")]:
    print(f"\n=== {ds}: scanning {root} ===")
    mp4s = glob.glob(f"{root}/**/*.mp4", recursive=True)
    print(f"  Found {len(mp4s)} .mp4 files")
    if mp4s:
        for p in mp4s[:5]:
            print(f"    {p}")
        cap = cv2.VideoCapture(mp4s[0])
        print(f"  OpenCV can open first file: {cap.isOpened()}")
        cap.release()

        # Check folder names for label matching
        from collections import Counter
        parents = [Path(p).parent.name.lower() for p in mp4s]
        print(f"  Folder name distribution: {dict(Counter(parents))}")
    else:
        print(f"  No .mp4 files found. Check that Step 4 completed successfully.")
        print(f"  Contents of {root}:")
        !ls -la "{root}"
```

---

## What the Pipeline Produces

After running all three sample sizes (n=50, 200, 400), you will have:

```
/content/outputs/
├── manifests/
│   ├── FFPP/
│   │   ├── manifest.csv          ← all videos with labels
│   │   ├── train.csv             ← 70% of videos
│   │   ├── val.csv               ← 15% of videos
│   │   └── test.csv              ← 15% of videos
│   └── CDF/
│       └── (same structure)
├── frames/
│   ├── FFPP/{video_id}/*.jpg     ← extracted frames
│   └── CDF/{video_id}/*.jpg
├── fft_cache/
│   ├── FFPP/{video_id}/*.npy     ← precomputed FFT magnitude
│   └── CDF/{video_id}/*.npy
├── runs/
│   ├── spatial_FFPP_n50_seed0/
│   │   ├── best.pt               ← best model checkpoint (~80 MB)
│   │   ├── metrics.json          ← per-epoch val metrics
│   │   └── train.log
│   ├── freq_FFPP_n50_seed0/
│   ├── hybrid_FFPP_n50_seed0/
│   ├── spatial_CDF_n50_seed0/
│   ├── freq_CDF_n50_seed0/
│   ├── hybrid_CDF_n50_seed0/
│   └── (same for n200 and n400)
└── tables/
    ├── n50/
    │   ├── Table1_in_dataset.csv
    │   ├── Table2_cross_dataset.csv
    │   └── Table3_generalization_drop.csv
    ├── n200/
    │   └── (same 3 tables)
    └── n400/
        └── (same 3 tables)
```

### Understanding the Result Tables

**Table1_in_dataset.csv** — Train and test on the same dataset:

| Column | Meaning |
|--------|---------|
| model | spatial, freq, or hybrid |
| train_dataset / test_dataset | FFPP or CDF (same for in-dataset) |
| acc, precision, recall, f1, auc | Performance metrics |

**Table2_cross_dataset.csv** — Train on one dataset, test on the other:

Same columns, but `train_dataset != test_dataset`.

**Table3_generalization_drop.csv** — How much performance drops cross-dataset:

| Column | Meaning |
|--------|---------|
| f1_in | F1 on same dataset |
| f1_cross | F1 on other dataset |
| drop | f1_in - f1_cross (higher = worse generalization) |
