"""
Single-command pipeline for deepfake hybrid detection experiments.

Runs the full experiment: extract frames → build splits → FFT cache → train → eval → tables.
Supports --n-samples to limit dataset size for faster runs on limited hardware.

Examples:
    # Full experiment with 500 samples per dataset:
    python scripts/run_pipeline.py --n-samples 500 --pretrained

    # Quick smoke test:
    python scripts/run_pipeline.py --n-samples 50 --max-frames 10 --epochs 1 --pretrained

    # More samples, custom settings:
    python scripts/run_pipeline.py --n-samples 1000 --max-frames 80 --epochs 10 --pretrained

    # Skip preprocessing (if already extracted):
    python scripts/run_pipeline.py --skip-preprocess --pretrained
"""

import argparse
import sys
import subprocess
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def step(cmd, description):
    """Run a pipeline step with timing."""
    print(f"\n{'=' * 60}")
    print(f"  {description}")
    print(f"{'=' * 60}")
    print(f"  > {' '.join(str(c) for c in cmd)}\n")
    t0 = time.time()
    result = subprocess.run(cmd)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"\n  FAILED after {elapsed:.1f}s (exit code {result.returncode})")
        sys.exit(1)
    print(f"\n  Done in {elapsed:.1f}s")


def patch_config(config_path, overrides):
    """Create a temporary config with overrides applied."""
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    for key, value in overrides.items():
        cfg[key] = value
    tmp_path = ROOT / ".pipeline_config.yaml"
    with open(tmp_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    return str(tmp_path)


def main():
    parser = argparse.ArgumentParser(
        description="Run the full deepfake detection pipeline end-to-end",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--config", default="config.yaml",
                        help="Path to config YAML (default: config.yaml)")
    parser.add_argument("--dataset", choices=["FFPP", "CDF", "both"], default="both",
                        help="Which dataset to train on (default: both)")
    parser.add_argument("--n-samples", type=int, default=500,
                        help="Videos per dataset (default: 500, 0 = all)")
    parser.add_argument("--max-frames", type=int, default=50,
                        help="Max frames per video (default: 50)")
    parser.add_argument("--fps", type=int, default=5,
                        help="Frame extraction FPS (default: 5)")
    parser.add_argument("--epochs", type=int, default=None,
                        help="Override training epochs (default: from config)")
    parser.add_argument("--batch-size", type=int, default=None,
                        help="Override batch size (default: from config)")
    parser.add_argument("--num-workers", type=int, default=4,
                        help="Workers for data loading / FFT (default: 4, safe on Windows)")
    parser.add_argument("--pretrained", action="store_true",
                        help="Use pretrained Xception backbone")
    parser.add_argument("--skip-preprocess", action="store_true",
                        help="Skip frame extraction, splits, and FFT cache")
    parser.add_argument("--force-fft", action="store_true",
                        help="Recompute FFT cache even if files already exist")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    total_start = time.time()

    # Resolve config path
    base_config = str(ROOT / args.config)

    # Apply overrides to config if needed
    overrides = {"num_workers": args.num_workers, "max_frames_per_video": args.max_frames}
    if args.epochs is not None:
        overrides["epochs"] = args.epochs
    if args.batch_size is not None:
        overrides["batch_size"] = args.batch_size
    config_path = patch_config(base_config, overrides)

    datasets = ["FFPP", "CDF"] if args.dataset == "both" else [args.dataset]

    print(f"\n{'#' * 60}")
    print(f"  Deepfake Hybrid Detection Pipeline")
    print(f"  Datasets:    {', '.join(datasets)}")
    print(f"  Models:      spatial, freq, hybrid")
    print(f"  Samples:     {args.n_samples if args.n_samples > 0 else 'ALL'} per dataset")
    print(f"  Max frames:  {args.max_frames} per video")
    print(f"  Pretrained:  {args.pretrained}")
    if args.epochs:
        print(f"  Epochs:      {args.epochs}")
    print(f"{'#' * 60}")

    # ── PHASE 1: Preprocessing ──────────────────────────────
    if not args.skip_preprocess:
        for ds in datasets:
            # Extract frames
            cmd = [PY, str(ROOT / "scripts" / "extract_frames.py"),
                   "--config", config_path, "--dataset", ds,
                   "--fps", str(args.fps),
                   "--max-frames", str(args.max_frames),
                   "--num-workers", str(args.num_workers)]
            if args.n_samples > 0:
                cmd += ["--n-samples", str(args.n_samples)]
            step(cmd, f"[1/3] Extract frames — {ds}")

            # Build train/val/test splits
            step([PY, str(ROOT / "scripts" / "build_splits.py"),
                  "--config", config_path, "--dataset", ds],
                 f"[2/3] Build splits — {ds}")

            # Compute FFT cache
            fft_cmd = [PY, str(ROOT / "scripts" / "compute_fft_cache.py"),
                       "--config", config_path, "--dataset", ds,
                       "--num-workers", str(args.num_workers)]
            if args.force_fft:
                fft_cmd.append("--force")
            step(fft_cmd, f"[3/3] FFT cache — {ds}")

    # ── PHASE 2: Train + Eval + Tables (via run_all.py) ─────
    cmd = [PY, str(ROOT / "scripts" / "run_all.py"), "--config", config_path,
           "--dataset", args.dataset]
    if args.n_samples > 0:
        cmd += ["--n-samples", str(args.n_samples)]
    if args.pretrained:
        cmd.append("--pretrained")
    step(cmd, "Train all models + Evaluate + Generate tables")

    # ── Done ────────────────────────────────────────────────
    total_elapsed = time.time() - total_start
    m, s = divmod(int(total_elapsed), 60)
    print(f"\n{'#' * 60}")
    print(f"  PIPELINE COMPLETE  ({m}m {s}s)")
    print(f"")
    n_label = f"n{args.n_samples}" if args.n_samples > 0 else "default"
    print(f"  Result tables:  outputs/tables/{n_label}/")
    print(f"    - Table1_in_dataset.csv")
    print(f"    - Table2_cross_dataset.csv")
    print(f"    - Table3_generalization_drop.csv")
    print(f"  Checkpoints:    outputs/runs/  (suffix _n{args.n_samples if args.n_samples > 0 else 'ALL'})")
    print(f"  Logs:           outputs/runs/*/train.log")
    print(f"{'#' * 60}\n")

    # Cleanup temp config
    tmp_cfg = ROOT / ".pipeline_config.yaml"
    if tmp_cfg.exists():
        tmp_cfg.unlink()


if __name__ == "__main__":
    main()
