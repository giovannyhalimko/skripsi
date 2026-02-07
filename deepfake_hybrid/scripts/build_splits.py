import argparse
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from utils import load_config, ensure_dir


def main():
    parser = argparse.ArgumentParser(description="Build train/val/test splits by video")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Dataset name")
    parser.add_argument("--val-size", type=float, default=0.15)
    parser.add_argument("--test-size", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    cfg = load_config(args.config)
    manifest_path = Path(cfg["output_root"]) / "manifests" / args.dataset / "manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}. Run extract_frames.py first.")

    df = pd.read_csv(manifest_path)
    train_val, test = train_test_split(df, test_size=args.test_size, stratify=df["label"], random_state=args.seed)
    train, val = train_test_split(train_val, test_size=args.val_size / (1 - args.test_size), stratify=train_val["label"], random_state=args.seed)

    out_dir = Path(cfg["output_root"]) / "manifests" / args.dataset
    ensure_dir(out_dir)
    train.to_csv(out_dir / "train.csv", index=False)
    val.to_csv(out_dir / "val.csv", index=False)
    test.to_csv(out_dir / "test.csv", index=False)
    print(f"Saved splits to {out_dir}")


if __name__ == "__main__":
    main()
