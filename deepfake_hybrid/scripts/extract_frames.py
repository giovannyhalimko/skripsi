import argparse
import os
import sys
from pathlib import Path
from functools import partial
import multiprocessing as mp
import cv2
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, ensure_dir, effective_name


VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv"}


def infer_label(path: Path, real_keywords, fake_keywords):
    name_parts = [p.lower() for p in path.parts]
    for kw in fake_keywords:
        if kw.lower() in name_parts or kw.lower() in path.name.lower():
            return 1
    for kw in real_keywords:
        if kw.lower() in name_parts or kw.lower() in path.name.lower():
            return 0
    return None


def _extract_worker(item, out_root: Path, root: Path, fps: int, max_frames: int):
    """Top-level worker function so it's picklable for multiprocessing."""
    v, label = item
    try:
        rel = v.relative_to(root)
        vid = str(rel.with_suffix("")).replace("/", "_").replace("\\", "_")
    except ValueError:
        vid = v.stem
    out_dir = out_root / vid
    saved = extract_video_frames(v, out_dir, fps=fps, max_frames=max_frames)
    if saved == 0:
        return None
    return {"video_id": vid, "label": label, "frames_dir": str(out_dir)}


def extract_video_frames(video_path: Path, out_dir: Path, fps: int, max_frames: int):
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"[WARN] Could not open {video_path}")
        return 0
    vfps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(int(round(vfps / fps)) if vfps > 0 else 1, 1)
    count = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frame_name = f"frame_{saved:06d}.jpg"
            cv2.imwrite(str(out_dir / frame_name), frame)
            saved += 1
            if max_frames > 0 and saved >= max_frames:
                break
        count += 1
    cap.release()
    return saved


def main():
    import random
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Dataset name")
    parser.add_argument("--fps", type=int, default=5)
    parser.add_argument("--max-frames", type=int, default=100)
    parser.add_argument("--n-samples", type=int, default=0,
                        help="Limit to N randomly sampled videos (balanced real/fake). 0 = all.")
    parser.add_argument("--num-workers", type=int, default=4,
                        help="Parallel video workers (default: 4)")
    parser.add_argument("--method", type=str, default=None,
                        choices=["Deepfakes", "Face2Face", "FaceSwap", "NeuralTextures"],
                        help="FFPP only: restrict to a single manipulation method")
    args = parser.parse_args()

    cfg = load_config(args.config)
    ds_cfg = cfg["datasets"][args.dataset.lower()]
    root = Path(ds_cfg["root"])
    eff_name = effective_name(args.dataset, args.method)
    out_root = Path(cfg["output_root"]) / "frames" / eff_name
    manifest_path = Path(cfg["output_root"]) / "manifests" / eff_name / "manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    real_kw = ds_cfg.get("real_keywords", ["real", "original", "pristine", "actors"])
    fake_kw = ds_cfg.get("fake_keywords", ["fake", "manipulated", "synthesis", "deepfake"])

    # Collect and label videos — only search for video extensions (not all files)
    all_videos = []
    early_stop = args.n_samples * 3 if args.n_samples > 0 else 0
    real_count = 0
    fake_count = 0
    print(f"  Scanning for videos in {root} ...")
    for ext in VIDEO_EXTS:
        for p in root.rglob(f"*{ext}"):
            label = infer_label(p.parent, real_kw, fake_kw)
            if label is None:
                label = infer_label(p, real_kw, fake_kw)
            if label is None:
                continue
            all_videos.append((p, label))
            if label == 0:
                real_count += 1
            else:
                fake_count += 1
            if len(all_videos) % 200 == 0:
                print(f"    ...{len(all_videos)} videos found ({real_count} real, {fake_count} fake)")
            # Early stop when we have enough for both classes
            if early_stop > 0 and real_count >= early_stop and fake_count >= early_stop:
                break
        if early_stop > 0 and real_count >= early_stop and fake_count >= early_stop:
            print(f"  Early stop: enough candidates ({len(all_videos)} videos)")
            break

    print(f"Found {len(all_videos)} labeled videos ({real_count} real, {fake_count} fake)")

    # Filter to a single manipulation method (FFPP only)
    if args.method:
        before = len(all_videos)
        all_videos = [(v, l) for v, l in all_videos
                      if l == 0 or args.method.lower() in str(v).lower()]
        real_count = sum(1 for _, l in all_videos if l == 0)
        fake_count = sum(1 for _, l in all_videos if l == 1)
        print(f"Filtered to method '{args.method}': {before} → {len(all_videos)} "
              f"({real_count} real, {fake_count} fake)")

    # Apply n-samples limit with balanced sampling; keep reserve for replacements
    rng = random.Random(42)
    real_all = [(v, l) for v, l in all_videos if l == 0]
    fake_all = [(v, l) for v, l in all_videos if l == 1]
    rng.shuffle(real_all)
    rng.shuffle(fake_all)

    if args.n_samples > 0 and len(all_videos) > args.n_samples:
        half = args.n_samples // 2
        real_take = min(len(real_all), half)
        fake_take = min(len(fake_all), args.n_samples - real_take)
        remaining = args.n_samples - real_take - fake_take
        if remaining > 0:
            if len(real_all) > real_take:
                real_take = min(len(real_all), real_take + remaining)
            elif len(fake_all) > fake_take:
                fake_take = min(len(fake_all), fake_take + remaining)
        selected = real_all[:real_take] + fake_all[:fake_take]
        # Reserve = candidates not selected, used to replace broken videos
        reserve = {0: list(real_all[real_take:]), 1: list(fake_all[fake_take:])}
        rng.shuffle(selected)
        all_videos = selected
        print(f"Sampled {len(all_videos)} videos ({real_take} real, {fake_take} fake) "
              f"| reserve: {len(reserve[0])} real, {len(reserve[1])} fake")
    else:
        reserve = {0: [], 1: []}

    if len(all_videos) == 0:
        print(f"[ERROR] No labeled videos found in {root}")
        print(f"  Check dataset path and keywords in config:")
        print(f"  real_keywords: {real_kw}")
        print(f"  fake_keywords: {fake_kw}")
        print(f"  Contents of root dir: {[str(p.name) for p in root.iterdir()] if root.exists() else 'PATH DOES NOT EXIST'}")
        sys.exit(1)

    worker_fn = partial(_extract_worker, out_root=out_root, root=root,
                        fps=args.fps, max_frames=args.max_frames)
    num_workers = min(args.num_workers, len(all_videos))
    print(f"Extracting frames with {num_workers} parallel workers...")
    with mp.Pool(num_workers) as pool:
        results = list(tqdm(
            pool.imap(worker_fn, all_videos),
            total=len(all_videos), desc="Extracting frames"
        ))

    # Replace failed videos by retrying from reserve pool
    failed = [(i, all_videos[i]) for i, r in enumerate(results) if r is None]
    if failed:
        print(f"[WARN] {len(failed)} videos failed — retrying with reserve candidates...")
        for i, (orig_path, label) in failed:
            replaced = False
            while reserve[label]:
                replacement = reserve[label].pop(0)
                result = worker_fn(replacement)
                if result is not None:
                    results[i] = result
                    print(f"  Replaced {orig_path.name} → {replacement[0].name}")
                    replaced = True
                    break
            if not replaced:
                print(f"  [WARN] No reserve left for label={label}, skipping {orig_path.name}")

    import pandas as pd

    rows = [r for r in results if r is not None]
    df = pd.DataFrame(rows, columns=["video_id", "label", "frames_dir"])
    df.to_csv(manifest_path, index=False)
    print(f"Saved manifest to {manifest_path} with {len(rows)} videos")


if __name__ == "__main__":
    main()
