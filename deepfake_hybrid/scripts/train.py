import argparse
import sys
from pathlib import Path
import logging

import torch
from torch.utils.data import DataLoader
from torch import nn, optim
from torch.optim.lr_scheduler import CosineAnnealingLR, LinearLR, SequentialLR
from tqdm import tqdm
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, seed_everything, setup_logging, ensure_dir, get_device, worker_init_fn, save_json
from datasets import DeepfakeDataset, DatasetConfig
from models.spatial_xception import build_xception
from models.freq_cnn import FreqCNN
from models.hybrid_fusion import HybridTwoBranch, EarlyFusionXception
import metrics as metrics_mod


def make_dataloader(manifest_path: Path, cfg: dict, mode: str, train: bool, fft_cache_root: Path | None, seed: int):
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
        logits = model(x.to(device)).squeeze(-1)
    elif model_type == "freq":
        x, y = batch
        logits = model(x.to(device)).squeeze(-1)
    elif model_type == "early_fusion":
        x, y = batch
        logits = model(x.to(device)).squeeze(-1)
    elif model_type == "hybrid":
        feats, y = batch
        logits = model(feats["image"].to(device), feats["fft"].to(device))
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


def train_one_epoch(model, loader, model_type, device, optimizer, scaler, loss_fn, max_grad_norm):
    model.train()
    running_loss = 0.0
    for batch in tqdm(loader, desc="train", leave=False):
        optimizer.zero_grad()
        with torch.cuda.amp.autocast(enabled=device.type == "cuda"):
            logits, targets = forward_model(model_type, model, batch, device)
            loss = loss_fn(logits, targets)
        scaler.scale(loss).backward()
        # Gradient clipping for training stability
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=max_grad_norm)
        scaler.step(optimizer)
        scaler.update()
        running_loss += loss.item() * targets.size(0)
    return running_loss / len(loader.dataset)


def build_optimizer(model, model_type, cfg):
    """Build optimizer with differential LR for hybrid model."""
    base_lr = cfg.get("lr", 1e-4)
    wd = cfg.get("weight_decay", 1e-4)

    if model_type == "hybrid":
        param_groups = [
            {"params": model.spatial.parameters(), "lr": base_lr * 0.1},
            {"params": model.freq.parameters(), "lr": base_lr},
            {"params": model.spatial_bn.parameters(), "lr": base_lr},
            {"params": model.freq_bn.parameters(), "lr": base_lr},
            {"params": model.classifier.parameters(), "lr": base_lr},
        ]
        return optim.Adam(param_groups, weight_decay=wd)

    if model_type == "spatial":
        return optim.Adam(model.parameters(), lr=base_lr * 0.1, weight_decay=wd)

    return optim.Adam(model.parameters(), lr=base_lr, weight_decay=wd)


def build_scheduler(optimizer, cfg, epochs):
    """Build cosine annealing scheduler with linear warmup."""
    scheduler_type = cfg.get("scheduler", "cosine")
    if scheduler_type != "cosine":
        return None

    warmup_epochs = cfg.get("warmup_epochs", 2)
    min_lr = cfg.get("min_lr", 1e-6)

    warmup_sched = LinearLR(optimizer, start_factor=0.1, total_iters=warmup_epochs)
    cosine_sched = CosineAnnealingLR(optimizer, T_max=max(1, epochs - warmup_epochs), eta_min=min_lr)
    return SequentialLR(optimizer, schedulers=[warmup_sched, cosine_sched], milestones=[warmup_epochs])


def compute_pos_weight(manifest_path, device):
    """Compute pos_weight for BCEWithLogitsLoss from label distribution."""
    df = pd.read_csv(manifest_path)
    n_real = (df["label"] == 0).sum()
    n_fake = (df["label"] == 1).sum()
    if n_real == 0 or n_fake == 0:
        return None
    ratio = n_real / n_fake
    if 0.8 <= ratio <= 1.2:
        return None  # balanced enough
    return torch.tensor([ratio], dtype=torch.float32).to(device)


def main():
    parser = argparse.ArgumentParser(description="Train deepfake models")
    parser.add_argument("--config", required=True)
    parser.add_argument("--dataset", choices=["FFPP", "CDF"], help="Training dataset")
    parser.add_argument("--model", choices=["spatial", "freq", "hybrid", "early_fusion"], help="Model type")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pretrained", action="store_true", help="Use pretrained backbones where applicable")
    args = parser.parse_args()

    cfg = load_config(args.config)
    seed_everything(args.seed)
    device = get_device()

    run_dir = Path(cfg["output_root"]) / "runs" / f"{args.model}_{args.dataset}_seed{args.seed}"
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
    epochs = cfg.get("epochs", 25)
    max_grad_norm = cfg.get("max_grad_norm", 1.0)
    patience = cfg.get("early_stopping_patience", 7)

    # Class weighting
    pos_weight = compute_pos_weight(train_manifest, device)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    if pos_weight is not None:
        logging.info(f"Using pos_weight={pos_weight.item():.3f} for class imbalance")

    # Optimizer with differential LR
    optimizer = build_optimizer(model, args.model, cfg)

    # LR scheduler
    scheduler = build_scheduler(optimizer, cfg, epochs)

    scaler = torch.cuda.amp.GradScaler(enabled=device.type == "cuda")

    best_auc = -1.0
    patience_counter = 0
    history = []
    for epoch in range(1, epochs + 1):
        train_loss = train_one_epoch(model, train_loader, args.model, device, optimizer, scaler, loss_fn, max_grad_norm)
        val_metrics = evaluate(model, val_loader, args.model, device)
        history.append({"epoch": epoch, "train_loss": train_loss, **val_metrics})

        current_lr = optimizer.param_groups[0]["lr"]
        logging.info(f"Epoch {epoch}: loss={train_loss:.4f}, val_auc={val_metrics['auc']:.4f}, val_f1={val_metrics['f1']:.4f}, lr={current_lr:.2e}")

        if val_metrics["auc"] > best_auc:
            best_auc = val_metrics["auc"]
            patience_counter = 0
            torch.save({"state_dict": model.state_dict(), "epoch": epoch, "config": cfg}, run_dir / "best.pt")
        else:
            patience_counter += 1

        if scheduler is not None:
            scheduler.step()

        if patience_counter >= patience:
            logging.info(f"Early stopping at epoch {epoch} (no improvement for {patience} epochs)")
            break

    save_json({"history": history}, run_dir / "metrics.json")
    logging.info(f"Training complete. Best AUC={best_auc:.4f}. Checkpoint at {run_dir/'best.pt'}")


if __name__ == "__main__":
    main()
