# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a thesis (skripsi) project for deepfake detection using a hybrid architecture combining XceptionNet (spatial domain) and frequency-domain analysis (FFT + CNN). The main code lives in `deepfake_hybrid/`.

## Pipeline Commands

All scripts run from inside `deepfake_hybrid/`. Config is `config.yaml`.

```bash
# Full end-to-end pipeline (recommended entry point)
python scripts/run_pipeline.py --n-samples 500 --pretrained

# Quick smoke test
python scripts/run_pipeline.py --n-samples 50 --max-frames 10 --epochs 1 --pretrained

# Skip preprocessing if frames/splits/FFT already exist
python scripts/run_pipeline.py --skip-preprocess --pretrained
```

### Individual pipeline steps

```bash
# 1. Extract frames from videos
python scripts/extract_frames.py --config config.yaml --dataset FFPP --fps 5 --max-frames 100

# 2. Build train/val/test splits (stratified by video)
python scripts/build_splits.py --config config.yaml --dataset FFPP

# 3. Precompute FFT log-magnitude cache
python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --num-workers 4

# 4. Train a single model
python scripts/train.py --config config.yaml --dataset FFPP --model hybrid --pretrained

# 5. Evaluate a checkpoint
python scripts/eval.py --config config.yaml --dataset CDF --model hybrid --checkpoint outputs/runs/hybrid_FFPP_seed0/best.pt

# 6. Full experiment matrix (all models x datasets x seeds, generates result tables)
python scripts/run_all.py --config config.yaml --pretrained

# 7. Generate plots for results chapter
python scripts/plot_results.py --config config.yaml --n-samples 50,200,400
```

### Compute FFT normalization stats

After building the FFT cache, compute mean/std and update `_FFT_MEAN`/`_FFT_STD` in `src/deepfake_data.py`:

```bash
python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --stats
```

## Architecture

### Three model types

- **spatial** (`src/models/spatial_xception.py`): XceptionNet via `timm`, ImageNet-pretrained, binary classification
- **freq** (`src/models/freq_cnn.py`): 5-layer CNN on single-channel FFT log-magnitude maps
- **hybrid** (`src/models/hybrid_fusion.py`): Two-branch fusion — XceptionNet spatial features + FreqCNN features, projected to 256-d each, concatenated, passed through SE (Squeeze-and-Excitation) gating, then classified. Also supports `early_fusion` mode (4-channel input: RGB + FFT fed into XceptionNet)

### Data flow

1. Videos → frames extracted at configurable FPS (`scripts/extract_frames.py`)
2. Frames → FFT log-magnitude `.npy` cache (`scripts/compute_fft_cache.py`)
3. Manifests + splits by video ID to prevent frame leakage (`scripts/build_splits.py`)
4. `DeepfakeDataset` (`src/deepfake_data.py`) loads frames + FFT cache, applies transforms per mode (spatial/freq/hybrid/early_fusion)
5. For hybrid mode, horizontal flip augmentation is applied consistently to both RGB and FFT branches

### Training details

- Loss: BCEWithLogitsLoss with label smoothing (default 0.05)
- Optimizer: Adam with differential learning rates (backbone 10x lower than head for hybrid/early_fusion)
- Backbone freezing: spatial backbone frozen for first 3 epochs, then unfrozen
- LR schedule: linear warmup (2 epochs) → cosine decay
- Mixed precision (AMP) on CUDA, TF32 enabled for Ampere+ GPUs
- Gradient accumulation (default 2 steps for hybrid/early_fusion)
- Best checkpoint selected by validation AUC

### Key conventions

- Dataset names in CLI args: `FFPP` (FaceForensics++) or `CDF` (Celeb-DF)
- Video labels inferred from directory names via keyword matching in `config.yaml` (`real_keywords`/`fake_keywords`)
- All scripts use `sys.path.insert(0, str(SRC))` to import from `src/`
- Outputs go to `outputs/` (runs, tables, manifests, frames, fft_cache)
- `run_pipeline.py` creates a temporary `.pipeline_config.yaml` with overrides applied

## Environment

- Python 3.9 with venv at `deepfake_hybrid/.venv`
- Key dependencies: torch, torchvision, timm (for XceptionNet), opencv-python, scikit-learn, pandas, matplotlib
- Designed to run locally or on Google Colab. `colab_run.ipynb` is the primary notebook for training and evaluation on Colab — it handles Drive mounting, dataset setup, config patching, multi-sample-size training loops, and saving results back to Drive. See also `COLAB_GUIDE.md` for dataset preparation details.

## Repository structure beyond code

- `documents/` — thesis chapters in markdown (BAB III methodology, etc.)
- `analyze/` — analysis documents cross-checking code vs thesis
- `skills/` — Claude prompt templates for thesis writing tasks
- `documentation/` — logs of model fixes and changes
