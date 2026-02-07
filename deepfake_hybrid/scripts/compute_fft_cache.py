import argparse
import sys
from pathlib import Path
import multiprocessing as mp
from functools import partial
import pandas as pd
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from utils import load_config, ensure_dir
from fft_utils import save_fft_cache


def worker(row, fft_root: Path, image_size: int):
    frame_path = Path(row["frame_path"])
    video_id = row["video_id"]
    out_dir = fft_root / video_id
    out_path = out_dir / (frame_path.stem + ".npy")
    if out_path.exists():
        return
    try:
        save_fft_cache(frame_path, out_path, size=image_size)
    except Exception as e:
        print(f"[WARN] Failed on {frame_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Precompute FFT log-magnitude cache")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Dataset name")
    parser.add_argument("--num-workers", type=int, default=4)
    args = parser.parse_args()

    cfg = load_config(args.config)
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
        list(tqdm(pool.imap_unordered(partial(worker, fft_root=fft_root, image_size=cfg.get("image_size", 224)), rows), total=len(rows)))

    print(f"FFT cache saved under {fft_root}")


if __name__ == "__main__":
    main()
