# Deepfake Hybrid Pipeline

End-to-end experimental pipeline for deepfake detection with spatial (Xception), frequency (FFT + CNN), and hybrid (two-branch or early-fusion) models on FaceForensics++ (FF++) and Celeb-DF (CDF).

## Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate  # on Windows
pip install -r requirements.txt
```

## Configure
Edit `config.yaml`:
- Set `datasets.ffpp.root` and `datasets.cdf.root` to your data.
- Adjust `output_root`, `image_size`, `batch_size`, `epochs`, `max_frames_per_video`, `fusion_mode` (`two_branch` or `early_fusion`), and `n_seeds`.

## Pipeline
0) **Download datasets (optional helper)**
```bash
python scripts/download_datasets.py --config config.yaml --datasets original Deepfakes Face2Face FaceSwap NeuralTextures FaceShifter --compression c23 --type videos --server EU2
# For masks/models adjust --type; for partial download use --num-videos N
# Celeb-DF must be placed manually under datasets.cdf.root (license)
```

1) **Extract frames** (video → frames, per video dir) and manifest:
```bash
python scripts/extract_frames.py --config config.yaml --dataset FFPP --fps 5 --max-frames 100
python scripts/extract_frames.py --config config.yaml --dataset CDF  --fps 5 --max-frames 100
```
2) **Build splits** (by video ID, stratified):
```bash
python scripts/build_splits.py --config config.yaml --dataset FFPP
python scripts/build_splits.py --config config.yaml --dataset CDF
```
3) **Compute FFT cache** (log magnitude per frame):
```bash
python scripts/compute_fft_cache.py --config config.yaml --dataset FFPP --num-workers 4
python scripts/compute_fft_cache.py --config config.yaml --dataset CDF  --num-workers 4
```
4) **Train** (examples):
```bash
python scripts/train.py --config config.yaml --dataset FFPP --model spatial --pretrained
python scripts/train.py --config config.yaml --dataset FFPP --model freq
python scripts/train.py --config config.yaml --dataset FFPP --model hybrid --pretrained
```
5) **Eval** (example):
```bash
python scripts/eval.py --config config.yaml --dataset CDF --model hybrid --checkpoint outputs/runs/hybrid_FFPP_seed0/best.pt
```
6) **Full matrix** (train on FF++ & CDF; in- and cross-dataset eval; tables generated):
```bash
python scripts/run_all.py --config config.yaml --pretrained
```
Tables saved to `outputs/tables/`:
- `Table1_in_dataset.csv`
- `Table2_cross_dataset.csv`
- `Table3_generalization_drop.csv`
(+ summaries if `n_seeds>1`).

## Notes
- Splits are by **video**, preventing frame leakage.
- FFT uses log magnitude of grayscale FFT; cache stored under `outputs/fft_cache/<dataset>/<video_id>/`.
- Checkpoints saved to `outputs/runs/<model>_<dataset>_seedX/best.pt`, selected by best val AUC.
- Models use GPU if available; otherwise CPU.
- If your dataset folder names differ, edit `real_keywords`/`fake_keywords` in `config.yaml` or extend `extract_frames.py` to match your structure (TODO markers inside).

## Quick dry-run (sanity)
You can point `datasets.ffpp.root` to a tiny folder with a couple of short videos (real/fake) and run steps 1–4 with `--max-frames 5` to validate the pipeline wiring before full training.
