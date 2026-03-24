"""Diagnose dataset splits for class balance, leakage, and label consistency.

Usage:
    python scripts/diagnose_splits.py --config config.yaml --dataset FFPP
    python scripts/diagnose_splits.py --config config.yaml --dataset CDF
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config


def infer_label(frames_dir: str, real_keywords: list, fake_keywords: list) -> int | None:
    path_lower = frames_dir.lower().replace("\\", "/")
    for kw in fake_keywords:
        if kw.lower() in path_lower:
            return 1
    for kw in real_keywords:
        if kw.lower() in path_lower:
            return 0
    return None


def diagnose(cfg: dict, dataset_name: str):
    manifest_root = Path(cfg["output_root"]) / "manifests" / dataset_name
    ds_cfg = cfg["datasets"].get(dataset_name.lower())
    if ds_cfg is None:
        # Try alternate case
        for k in cfg["datasets"]:
            if k.lower() == dataset_name.lower():
                ds_cfg = cfg["datasets"][k]
                break

    real_keywords = ds_cfg["real_keywords"] if ds_cfg else []
    fake_keywords = ds_cfg["fake_keywords"] if ds_cfg else []

    splits = {}
    for split_name in ["train", "val", "test"]:
        path = manifest_root / f"{split_name}.csv"
        if not path.exists():
            print(f"  [MISSING] {path}")
            continue
        splits[split_name] = pd.read_csv(path)

    if not splits:
        print(f"No split files found under {manifest_root}")
        return

    print(f"\n{'='*60}")
    print(f"Dataset: {dataset_name}")
    print(f"{'='*60}")

    # 1. Class balance per split
    print("\n[1] Class Balance")
    all_video_ids = {}
    for split_name, df in splits.items():
        counts = df["label"].value_counts().sort_index()
        total = len(df)
        real = counts.get(0, 0)
        fake = counts.get(1, 0)
        ratio = fake / total if total > 0 else 0
        print(f"  {split_name:5s}: {total:5d} videos | real={real:4d} ({real/total:.1%}) | fake={fake:4d} ({fake/total:.1%})")
        for vid in df["video_id"]:
            all_video_ids.setdefault(vid, []).append(split_name)

    # 2. Video ID overlap
    print("\n[2] Video ID Overlap Between Splits")
    split_names = list(splits.keys())
    found_overlap = False
    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):
            s1, s2 = split_names[i], split_names[j]
            ids1 = set(splits[s1]["video_id"])
            ids2 = set(splits[s2]["video_id"])
            overlap = ids1 & ids2
            if overlap:
                print(f"  [FAIL] {s1} / {s2} share {len(overlap)} video IDs: {list(overlap)[:5]}...")
                found_overlap = True
            else:
                print(f"  [OK]   {s1} / {s2}: no overlap")

    # 3. Label consistency — re-derive labels from path
    if real_keywords or fake_keywords:
        print("\n[3] Label Consistency (keyword vs manifest)")
        mismatches = []
        unknown = []
        for split_name, df in splits.items():
            for _, row in df.iterrows():
                inferred = infer_label(str(row["frames_dir"]), real_keywords, fake_keywords)
                if inferred is None:
                    unknown.append((split_name, row["video_id"], row["frames_dir"]))
                elif inferred != int(row["label"]):
                    mismatches.append((split_name, row["video_id"], int(row["label"]), inferred, row["frames_dir"]))
        if mismatches:
            print(f"  [FAIL] {len(mismatches)} label mismatches:")
            for split_name, vid, manifest_lbl, inferred_lbl, fdir in mismatches[:10]:
                print(f"    {split_name} | {vid} | manifest={manifest_lbl} inferred={inferred_lbl} | {fdir}")
        else:
            print(f"  [OK]   No label mismatches detected")
        if unknown:
            print(f"  [WARN] {len(unknown)} videos with unrecognized path (no keyword match):")
            for split_name, vid, fdir in unknown[:5]:
                print(f"    {split_name} | {vid} | {fdir}")
    else:
        print("\n[3] Label Consistency: skipped (no keywords in config)")

    # 4. Frames directory existence
    print("\n[4] Frames Directory Existence")
    missing_dirs = []
    empty_dirs = []
    for split_name, df in splits.items():
        for _, row in df.iterrows():
            fdir = Path(row["frames_dir"])
            if not fdir.exists():
                missing_dirs.append((split_name, str(fdir)))
            elif not any(fdir.iterdir()):
                empty_dirs.append((split_name, str(fdir)))
    if missing_dirs:
        print(f"  [FAIL] {len(missing_dirs)} missing frame directories:")
        for split_name, fdir in missing_dirs[:5]:
            print(f"    {split_name}: {fdir}")
    elif empty_dirs:
        print(f"  [WARN] {len(empty_dirs)} empty frame directories:")
        for split_name, fdir in empty_dirs[:5]:
            print(f"    {split_name}: {fdir}")
    else:
        print(f"  [OK]   All frame directories exist and are non-empty")

    # 5. Summary
    print("\n[5] Summary")
    total_videos = sum(len(df) for df in splits.values())
    total_frames = 0
    for df in splits.values():
        for _, row in df.iterrows():
            fdir = Path(row["frames_dir"])
            if fdir.exists():
                total_frames += sum(1 for f in fdir.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"})
    print(f"  Total videos across splits: {total_videos}")
    print(f"  Total frames on disk:       {total_frames}")
    if found_overlap:
        print("  [FAIL] Split leakage detected — video IDs appear in multiple splits")
    else:
        print("  [OK]   No split leakage")


def main():
    parser = argparse.ArgumentParser(description="Diagnose dataset splits")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF", "all"], default="all")
    args = parser.parse_args()

    cfg = load_config(args.config)
    datasets = ["FFPP", "CDF"] if args.dataset == "all" else [args.dataset]
    for ds in datasets:
        diagnose(cfg, ds)


if __name__ == "__main__":
    main()
