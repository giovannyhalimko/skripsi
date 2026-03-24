import argparse
import json
import sys
from pathlib import Path
import multiprocessing as mp
from functools import partial
import numpy as np
import pandas as pd
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, ensure_dir
from fft_utils import save_fft_cache


def worker(row, fft_root: Path, image_size: int, force: bool = False):
    frame_path = Path(row["frame_path"])
    video_id = row["video_id"]
    out_dir = fft_root / video_id
    out_path = out_dir / (frame_path.stem + ".npy")
    if out_path.exists() and not force:
        return
    try:
        save_fft_cache(frame_path, out_path, size=image_size)
    except Exception as e:
        print(f"[WARN] Failed on {frame_path}: {e}")


def compute_fft_stats(fft_root: Path, max_files: int = 5000):
    """Scan cached .npy files and compute global mean/std for normalization.

    Saves results to fft_root/fft_stats.json and returns (mean, std).
    """
    npy_files = list(Path(fft_root).rglob("*.npy"))
    if not npy_files:
        print(f"No .npy files found under {fft_root}")
        return None, None
    rng = np.random.default_rng(42)
    if len(npy_files) > max_files:
        indices = rng.choice(len(npy_files), size=max_files, replace=False)
        npy_files = [npy_files[i] for i in indices]
    print(f"Computing stats from {len(npy_files)} files...")
    running_sum = 0.0
    running_sq = 0.0
    total_pixels = 0
    for fp in tqdm(npy_files, desc="stats"):
        arr = np.load(fp).astype(np.float64)
        running_sum += arr.sum()
        running_sq += (arr ** 2).sum()
        total_pixels += arr.size
    mean = running_sum / total_pixels
    std = np.sqrt(running_sq / total_pixels - mean ** 2)
    print(f"\n_FFT_MEAN = {mean:.4f}")
    print(f"_FFT_STD  = {std:.4f}")
    stats_path = Path(fft_root) / "fft_stats.json"
    with open(stats_path, "w") as f:
        json.dump({"mean": float(mean), "std": float(std)}, f)
    print(f"Saved FFT stats to {stats_path}")
    return mean, std


def main():
    parser = argparse.ArgumentParser(description="Precompute FFT log-magnitude cache")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Dataset name")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--force", action="store_true", help="Recompute even if cache exists")
    parser.add_argument("--stats", action="store_true", help="Compute mean/std from existing cache")
    args = parser.parse_args()

    cfg = load_config(args.config)

    if args.stats:
        fft_root = Path(cfg["output_root"]) / "fft_cache" / args.dataset
        compute_fft_stats(fft_root)
        return

    manifest_path = Path(cfg["output_root"]) / "manifests" / args.dataset / "manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    df = pd.read_csv(manifest_path)

    # Expand to frame-level rows
    rows = []
    for _, row in df.iterrows():
        frames_dir = Path(row["frames_dir"])
        for fp in frames_dir.iterdir():
            if fp.suffix.lower() not in {".jpg", ".jpeg", ".png", ".bmp"}:
                continue
            rows.append({"video_id": row["video_id"], "frame_path": str(fp)})

    fft_root = Path(cfg["output_root"]) / "fft_cache" / args.dataset
    ensure_dir(fft_root)

    with mp.Pool(processes=args.num_workers) as pool:
        list(tqdm(pool.imap_unordered(partial(worker, fft_root=fft_root, image_size=cfg.get("image_size", 224), force=args.force), rows), total=len(rows)))

    print(f"FFT cache saved under {fft_root}")

    # Auto-compute and save normalization stats after cache generation
    print("Auto-computing FFT normalization stats...")
    compute_fft_stats(fft_root)


if __name__ == "__main__":
    main()
