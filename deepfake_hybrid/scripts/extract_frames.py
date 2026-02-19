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
    parser = argparse.ArgumentParser(description="Extract frames from videos")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Dataset name")
    parser.add_argument("--fps", type=int, default=5)
    parser.add_argument("--max-frames", type=int, default=100)
    args = parser.parse_args()

    cfg = load_config(args.config)
    ds_cfg = cfg["datasets"][args.dataset.lower()]
    root = Path(ds_cfg["root"])
    out_root = Path(cfg["output_root"]) / "frames" / args.dataset
    manifest_path = Path(cfg["output_root"]) / "manifests" / args.dataset / "manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    real_kw = ds_cfg.get("real_keywords", ["real", "original", "pristine", "actors"])
    fake_kw = ds_cfg.get("fake_keywords", ["fake", "manipulated", "synthesis", "deepfake"])

    if not root.exists():
        raise FileNotFoundError(
            f"Dataset root not found: {root}\n"
            "Make sure Step 3 (copy from Drive) completed successfully."
        )

    videos = [p for p in root.rglob("*") if p.suffix.lower() in VIDEO_EXTS]

    if not videos:
        raise RuntimeError(
            f"No video files ({', '.join(VIDEO_EXTS)}) found under: {root}\n"
            "Possible causes:\n"
            "  1. Step 3 copy failed or is still running\n"
            "  2. Videos are in a different subfolder structure\n"
            "     Run: find <root> -name '*.mp4' | head -10\n"
            "  3. Files have a different extension (e.g. .avi, .mov)"
        )

    print(f"Found {len(videos)} video files under {root}")
    rows = []
    unknown_count = 0
    for v in tqdm(videos, desc="videos"):
        label = infer_label(v.parent, real_kw, fake_kw)
        if label is None:
            # try using name
            label = infer_label(v, real_kw, fake_kw)
        if label is None:
            print(f"[WARN] Skip (unknown label): {v}")
            unknown_count += 1
            continue
        vid = v.stem
        out_dir = out_root / vid
        saved = extract_video_frames(v, out_dir, fps=args.fps, max_frames=args.max_frames)
        if saved == 0:
            continue
        rows.append({"video_id": vid, "label": label, "frames_dir": str(out_dir)})

    import pandas as pd

    if unknown_count > 0:
        print(f"[WARN] {unknown_count} videos skipped (unknown label) — check real_keywords/fake_keywords in config")

    df = pd.DataFrame(rows, columns=["video_id", "label", "frames_dir"])
    df.to_csv(manifest_path, index=False)
    print(f"Saved manifest to {manifest_path} with {len(rows)} videos")

    if len(rows) == 0:
        raise RuntimeError(
            "No videos were written to the manifest.\n"
            f"  Total videos scanned: {len(videos)}\n"
            f"  Skipped (unknown label): {unknown_count}\n"
            f"  Skipped (0 frames extracted / OpenCV error): {len(videos) - unknown_count}\n"
            "Check [WARN] lines above for details."
        )


if __name__ == "__main__":
    main()
