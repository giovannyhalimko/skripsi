import argparse
import random
import shutil
from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import pandas as pd
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

import sys
sys.path.append(str(SRC))

from utils import load_config, ensure_dir  # noqa: E402

VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv"}


def infer_label(path: Path, real_keywords: Sequence[str], fake_keywords: Sequence[str]) -> Optional[int]:
    """Return 0 for real, 1 for fake, or None if unknown."""
    parts = [p.lower() for p in path.parts]
    for kw in fake_keywords:
        kw_l = kw.lower()
        if kw_l in parts or kw_l in path.name.lower():
            return 1
    for kw in real_keywords:
        kw_l = kw.lower()
        if kw_l in parts or kw_l in path.name.lower():
            return 0
    return None


def collect_videos(root: Path, real_kw: Sequence[str], fake_kw: Sequence[str]) -> List[Tuple[Path, int]]:
    videos: List[Tuple[Path, int]] = []
    for p in root.rglob("*"):
        if p.suffix.lower() not in VIDEO_EXTS:
            continue
        label = infer_label(p.parent, real_kw, fake_kw)
        if label is None:
            label = infer_label(p, real_kw, fake_kw)
        if label is None:
            tqdm.write(f"[WARN] Skipping unlabeled video: {p}")
            continue
        videos.append((p, label))
    return videos


def balanced_sample(videos: List[Tuple[Path, int]], sample_size: int, seed: int, balance: bool) -> List[Tuple[Path, int]]:
    rng = random.Random(seed)
    rng.shuffle(videos)
    if not balance:
        return videos[:sample_size]

    real = [v for v in videos if v[1] == 0]
    fake = [v for v in videos if v[1] == 1]
    if not real or not fake:
        tqdm.write("[WARN] Balance requested but one class is missing; falling back to random sample.")
        return videos[:sample_size]

    half = sample_size // 2
    real_take = min(len(real), half)
    fake_take = min(len(fake), sample_size - real_take)
    # if still short, top up from the larger pool
    remaining = sample_size - (real_take + fake_take)
    if remaining > 0:
        if len(real) - real_take >= len(fake) - fake_take:
            real_take = min(len(real), real_take + remaining)
        else:
            fake_take = min(len(fake), fake_take + remaining)

    rng.shuffle(real)
    rng.shuffle(fake)
    selected = real[:real_take] + fake[:fake_take]
    rng.shuffle(selected)
    return selected


def copy_videos(videos: List[Tuple[Path, int]], src_root: Path, dst_root: Path) -> List[dict]:
    rows = []
    for src, label in tqdm(videos, desc="copy", unit="vid"):
        rel = src.relative_to(src_root)
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        rows.append({
            "video_id": src.stem,
            "label": label,
            "src": str(src),
            "dst": str(dst),
        })
    return rows


def maybe_write_sampled_config(cfg_path: Path, cfg: dict, dataset: str, new_root: Path, out_path: Optional[Path]) -> None:
    if out_path is None:
        return
    cfg_copy = deepcopy(cfg)
    cfg_copy["datasets"][dataset.lower()]["root"] = str(new_root)
    with open(out_path, "w", encoding="utf-8") as f:
        import yaml  # local import to avoid global dependency when unused
        yaml.safe_dump(cfg_copy, f, sort_keys=False)
    tqdm.write(f"Wrote sampled config to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample a subset of videos into a new folder for smoke tests.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], required=True)
    parser.add_argument("--sample-size", type=int, default=None, help="Number of videos to keep (overrides config.sampling.sample_size).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (overrides config.sampling.seed).")
    parser.add_argument("--no-balance", action="store_true", help="Do not balance real/fake; just take first N shuffled.")
    parser.add_argument("--write-config", type=str, default=None, help="Optional path to write a config with dataset root set to sampled folder.")
    args = parser.parse_args()

    cfg = load_config(args.config)
    sampling_cfg = cfg.get("sampling", {})
    sample_size = args.sample_size or int(sampling_cfg.get("sample_size", 1000))
    seed = args.seed if args.seed is not None else int(sampling_cfg.get("seed", 42))
    balance = not args.no_balance and bool(sampling_cfg.get("balance_real_fake", True))

    ds_cfg = cfg["datasets"][args.dataset.lower()]
    src_root = Path(ds_cfg["root"]).resolve()
    if not src_root.exists():
        raise FileNotFoundError(f"Dataset root not found: {src_root}")

    dst_root = Path(sampling_cfg.get("output_root", "./outputs/sampled")).resolve() / args.dataset
    ensure_dir(dst_root)

    real_kw = ds_cfg.get("real_keywords", [])
    fake_kw = ds_cfg.get("fake_keywords", [])

    all_videos = collect_videos(src_root, real_kw, fake_kw)
    if not all_videos:
        raise RuntimeError(f"No labeled videos found under {src_root}")

    if sample_size > len(all_videos):
        tqdm.write(f"[WARN] Requested {sample_size} but only {len(all_videos)} available; using all.")
        sample_size = len(all_videos)

    selected = balanced_sample(all_videos, sample_size, seed, balance)
    tqdm.write(f"Sampling {len(selected)} videos to {dst_root}")

    rows = copy_videos(selected, src_root, dst_root)

    manifest_path = Path(cfg.get("output_root", "./outputs")) / "manifests" / args.dataset / "sampled_manifest.csv"
    ensure_dir(manifest_path.parent)
    pd.DataFrame(rows).to_csv(manifest_path, index=False)
    tqdm.write(f"Saved sampled manifest: {manifest_path}")

    if args.write_config:
        maybe_write_sampled_config(Path(args.config), cfg, args.dataset, dst_root, Path(args.write_config))


if __name__ == "__main__":
    main()
