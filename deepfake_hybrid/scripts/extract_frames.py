import argparse
import os
import sys
from pathlib import Path
import cv2
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, ensure_dir


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
    args = parser.parse_args()

    cfg = load_config(args.config)
    ds_cfg = cfg["datasets"][args.dataset.lower()]
    root = Path(ds_cfg["root"])
    out_root = Path(cfg["output_root"]) / "frames" / args.dataset
    manifest_path = Path(cfg["output_root"]) / "manifests" / args.dataset / "manifest.csv"
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

    # Apply n-samples limit with balanced sampling
    if args.n_samples > 0 and len(all_videos) > args.n_samples:
        rng = random.Random(42)
        real = [(v, l) for v, l in all_videos if l == 0]
        fake = [(v, l) for v, l in all_videos if l == 1]
        rng.shuffle(real)
        rng.shuffle(fake)
        half = args.n_samples // 2
        real_take = min(len(real), half)
        fake_take = min(len(fake), args.n_samples - real_take)
        remaining = args.n_samples - real_take - fake_take
        if remaining > 0:
            if len(real) > real_take:
                real_take = min(len(real), real_take + remaining)
            elif len(fake) > fake_take:
                fake_take = min(len(fake), fake_take + remaining)
        all_videos = real[:real_take] + fake[:fake_take]
        rng.shuffle(all_videos)
        print(f"Sampled {len(all_videos)} videos ({real_take} real, {fake_take} fake)")

    rows = []
    skipped = 0
    for v, label in tqdm(all_videos, desc="Extracting frames"):
        try:
            rel = v.relative_to(root)
            vid = str(rel.with_suffix("")).replace("/", "_").replace("\\", "_")
        except ValueError:
            vid = v.stem
        out_dir = out_root / vid
        saved = extract_video_frames(v, out_dir, fps=args.fps, max_frames=args.max_frames)
        if saved == 0:
            skipped += 1
            continue
        rows.append({"video_id": vid, "label": label, "frames_dir": str(out_dir)})

    if skipped > 0:
        print(f"[WARN] {skipped} videos could not be opened and were skipped")

    import pandas as pd

    df = pd.DataFrame(rows, columns=["video_id", "label", "frames_dir"])
    df.to_csv(manifest_path, index=False)
    print(f"Saved manifest to {manifest_path} with {len(rows)} videos")


if __name__ == "__main__":
    main()
