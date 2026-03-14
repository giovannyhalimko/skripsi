import argparse
import sys
from pathlib import Path
import logging

from typing import Optional

import torch
from torch.utils.data import DataLoader
from torch import nn, optim
from tqdm import tqdm
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, seed_everything, setup_logging, ensure_dir, get_device, worker_init_fn, save_json
from deepfake_data import DeepfakeDataset, DatasetConfig
from models.spatial_xception import build_xception
from models.freq_cnn import FreqCNN
from models.hybrid_fusion import HybridTwoBranch, EarlyFusionXception
import metrics as metrics_mod

FREEZE_EPOCHS = 3  # number of initial epochs to freeze spatial backbone


def make_dataloader(manifest_path: Path, cfg: dict, mode: str, train: bool, fft_cache_root: Optional[Path], seed: int):
    ds_cfg = DatasetConfig(
        manifest_path=manifest_path,
        fft_cache_root=fft_cache_root,
        image_size=cfg.get("image_size", 224),
        max_frames_per_video=cfg.get("max_frames_per_video", 100),
        mode=mode,
        seed=seed,
        train=train,
    )
    dataset = DeepfakeDataset(ds_cfg)
    loader = DataLoader(
        dataset,
        batch_size=cfg.get("batch_size", 16),
        shuffle=train,
        num_workers=cfg.get("num_workers", 4),
        pin_memory=True,
        worker_init_fn=worker_init_fn,
    )
    return loader


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
    if model_type == "spatial":
        x, y = batch
        logits = model(x.to(device)).view(-1)
    elif model_type == "freq":
        x, y = batch
        logits = model(x.to(device)).view(-1)
    elif model_type == "early_fusion":
        x, y = batch
        logits = model(x.to(device)).view(-1)
    elif model_type == "hybrid":
        feats, y = batch
        logits = model(feats["image"].to(device), feats["fft"].to(device)).view(-1)
    else:
        raise ValueError
    return logits, y.to(device)


def evaluate(model, loader, model_type, device):
    model.eval()
    all_probs, all_targets = [], []
    with torch.no_grad():
        for batch in loader:
            logits, targets = forward_model(model_type, model, batch, device)
            probs = torch.sigmoid(logits)
            all_probs.append(probs.cpu())
            all_targets.append(targets.cpu())
    y_prob = torch.cat(all_probs).numpy()
    y_true = torch.cat(all_targets).numpy()
    return metrics_mod.compute_metrics(y_true, y_prob)


def train_one_epoch(model, loader, model_type, device, optimizer, scaler, loss_fn, accum_steps=1):
    model.train()
    running_loss = 0.0
    optimizer.zero_grad()
    for i, batch in enumerate(tqdm(loader, desc="train", leave=False)):
        with torch.cuda.amp.autocast(enabled=device.type == "cuda"):
            logits, targets = forward_model(model_type, model, batch, device)
            loss = loss_fn(logits, targets) / accum_steps
        scaler.scale(loss).backward()
        if (i + 1) % accum_steps == 0 or (i + 1) == len(loader):
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()
        running_loss += loss.item() * accum_steps * targets.size(0)
    return running_loss / len(loader.dataset)


def main():
    parser = argparse.ArgumentParser(description="Train deepfake models")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Training dataset")
    parser.add_argument("--model", choices=["spatial", "freq", "hybrid", "early_fusion"], help="Model type")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pretrained", action="store_true", help="Use pretrained backbones where applicable")
    parser.add_argument("--n-samples", type=int, default=0,
                        help="Number of samples (only affects output folder naming)")
    args = parser.parse_args()

    cfg = load_config(args.config)
    seed_everything(args.seed)
    device = get_device()

    n_tag = f"_n{args.n_samples}" if args.n_samples > 0 else ""
    run_dir = Path(cfg["output_root"]) / "runs" / f"{args.model}_{args.dataset}{n_tag}_seed{args.seed}"
    ensure_dir(run_dir)
    setup_logging(run_dir / "train.log")
    logging.info(f"Starting training: model={args.model}, dataset={args.dataset}, seed={args.seed}, device={device}")

    manifest_root = Path(cfg["output_root"]) / "manifests" / args.dataset
    train_manifest = manifest_root / "train.csv"
    val_manifest = manifest_root / "val.csv"
    if not train_manifest.exists():
        raise FileNotFoundError(f"Train manifest missing at {train_manifest}. Run build_splits.py")

    fft_cache_root = (Path(cfg["output_root"]) / "fft_cache" / args.dataset) if args.model in {"freq", "hybrid", "early_fusion"} else None

    train_loader = make_dataloader(train_manifest, cfg, mode=args.model if args.model != "hybrid" else "hybrid", train=True, fft_cache_root=fft_cache_root, seed=args.seed)
    val_loader = make_dataloader(val_manifest, cfg, mode=args.model if args.model != "hybrid" else "hybrid", train=False, fft_cache_root=fft_cache_root, seed=args.seed)

    model = select_model(args.model, pretrained=args.pretrained).to(device)
    loss_fn = nn.BCEWithLogitsLoss()

    # --- Fix B: Differential Learning Rates ---
    base_lr = cfg.get("lr", 1e-4)
    wd = cfg.get("weight_decay", 1e-4)
    backbone_lr = base_lr / 10  # 10x lower LR for pretrained backbone

    if args.model == "hybrid":
        backbone_params = list(model.spatial.parameters())
        head_params = (
            list(model.freq.parameters())
            + list(model.spatial_proj.parameters())
            + list(model.freq_proj.parameters())
            + list(model.classifier.parameters())
        )
        optimizer = optim.Adam([
            {"params": backbone_params, "lr": backbone_lr},
            {"params": head_params, "lr": base_lr},
        ], weight_decay=wd)
    elif args.model == "early_fusion":
        backbone_params = list(model.model.parameters())
        # early_fusion only has model.model; all params are backbone
        optimizer = optim.Adam([
            {"params": backbone_params, "lr": backbone_lr},
        ], weight_decay=wd)
    else:
        optimizer = optim.Adam(model.parameters(), lr=base_lr, weight_decay=wd)

    scaler = torch.amp.GradScaler(device=device.type, enabled=device.type == "cuda")

    # --- Fix C: Backbone Freezing for first FREEZE_EPOCHS epochs ---
    if args.model == "hybrid":
        for p in model.spatial.parameters():
            p.requires_grad = False
        logging.info(f"Froze spatial backbone for first {FREEZE_EPOCHS} epochs")
    elif args.model == "early_fusion":
        for p in model.model.parameters():
            p.requires_grad = False
        logging.info(f"Froze backbone for first {FREEZE_EPOCHS} epochs")

    accum_steps = cfg.get("accum_steps", 2 if args.model in {"hybrid", "early_fusion"} else 1)
    best_auc = -1.0
    history = []
    epochs = cfg.get("epochs", 3)

    # --- Fix D: Cosine Annealing LR Scheduler ---
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    for epoch in range(1, epochs + 1):
        # --- Fix C: Unfreeze backbone after FREEZE_EPOCHS ---
        if epoch == FREEZE_EPOCHS + 1:
            if args.model == "hybrid":
                for p in model.spatial.parameters():
                    p.requires_grad = True
                logging.info(f"Epoch {epoch}: unfreezing spatial backbone")
            elif args.model == "early_fusion":
                for p in model.model.parameters():
                    p.requires_grad = True
                logging.info(f"Epoch {epoch}: unfreezing backbone")

        train_loss = train_one_epoch(model, train_loader, args.model, device, optimizer, scaler, loss_fn, accum_steps=accum_steps)
        val_metrics = evaluate(model, val_loader, args.model, device)
        history.append({"epoch": epoch, "train_loss": train_loss, **val_metrics})
        logging.info(f"Epoch {epoch}: loss={train_loss:.4f}, val_auc={val_metrics['auc']:.4f}, val_f1={val_metrics['f1']:.4f}")
        scheduler.step()
        if val_metrics["auc"] > best_auc:
            best_auc = val_metrics["auc"]
            torch.save({"state_dict": model.state_dict(), "epoch": epoch, "config": cfg}, run_dir / "best.pt")

    save_json({"history": history}, run_dir / "metrics.json")
    logging.info(f"Training complete. Best AUC={best_auc:.4f}. Checkpoint at {run_dir/'best.pt'}")


if __name__ == "__main__":
    main()
