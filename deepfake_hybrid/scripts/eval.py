import argparse
import sys
from pathlib import Path
import logging
import torch
from torch.utils.data import DataLoader
import pandas as pd
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, setup_logging, ensure_dir, get_device, worker_init_fn, save_json
from deepfake_data import DeepfakeDataset, DatasetConfig
from models.spatial_xception import build_xception
from models.freq_cnn import FreqCNN
from models.hybrid_fusion import HybridTwoBranch, EarlyFusionXception
import metrics as metrics_mod


def select_model(model_type: str, pretrained: bool):
    if model_type == "spatial":
        return build_xception(num_classes=1, in_chans=3, pretrained=pretrained)
    if model_type == "freq":
        return FreqCNN(num_classes=1)
    if model_type == "hybrid":
        return HybridTwoBranch(pretrained=pretrained)
    if model_type == "early_fusion":
        return EarlyFusionXception(pretrained=pretrained)
    raise ValueError(f"Unknown model_type {model_type}")


def forward_model(model_type, model, batch, device):
    if model_type == "hybrid":
        feats, y = batch
        logits = model(feats["image"].to(device), feats["fft"].to(device)).view(-1)
    else:
        x, y = batch
        logits = model(x.to(device)).view(-1)
    return logits, y.to(device)


def main():
    parser = argparse.ArgumentParser(description="Evaluate checkpoint")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Test dataset")
    parser.add_argument("--model", choices=["spatial", "freq", "hybrid", "early_fusion"], help="Model type")
    parser.add_argument("--checkpoint", required=True, help="Path to checkpoint .pt")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pretrained", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)
    device = get_device()

    run_dir = Path(cfg["output_root"]) / "runs"
    setup_logging(run_dir / "eval.log")

    test_manifest = Path(cfg["output_root"]) / "manifests" / args.dataset / "test.csv"
    if not test_manifest.exists():
        raise FileNotFoundError(f"Test manifest missing at {test_manifest}. Run build_splits.py")

    fft_cache_root = (Path(cfg["output_root"]) / "fft_cache" / args.dataset) if args.model in {"freq", "hybrid", "early_fusion"} else None
    ds_cfg = DatasetConfig(
        manifest_path=test_manifest,
        fft_cache_root=fft_cache_root,
        image_size=cfg.get("image_size", 224),
        max_frames_per_video=cfg.get("max_frames_per_video", 100),
        mode=args.model if args.model != "hybrid" else "hybrid",
        seed=args.seed,
        train=False,
    )
    dataset = DeepfakeDataset(ds_cfg)
    loader = DataLoader(dataset, batch_size=cfg.get("batch_size", 16), shuffle=False, num_workers=cfg.get("num_workers", 4), pin_memory=True, worker_init_fn=worker_init_fn)

    model = select_model(args.model, pretrained=args.pretrained)
    checkpoint = torch.load(args.checkpoint, map_location=device)
    model.load_state_dict(checkpoint["state_dict"] if isinstance(checkpoint, dict) and "state_dict" in checkpoint else checkpoint)
    model.to(device)
    model.eval()

    all_probs, all_targets = [], []
    with torch.no_grad():
        for batch in tqdm(loader, desc="eval"):
            logits, targets = forward_model(args.model, model, batch, device)
            probs = torch.sigmoid(logits)
            all_probs.append(probs.cpu())
            all_targets.append(targets.cpu())
    y_prob = torch.cat(all_probs).numpy()
    y_true = torch.cat(all_targets).numpy()

    metrics = metrics_mod.compute_metrics(y_true, y_prob)
    print(metrics)

    results_dir = Path(cfg["output_root"]) / "tables"
    ensure_dir(results_dir)
    save_json(metrics, results_dir / f"eval_{args.model}_{args.dataset}.json")


if __name__ == "__main__":
    main()
