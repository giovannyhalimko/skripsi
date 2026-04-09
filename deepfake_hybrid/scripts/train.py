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

from utils import load_config, seed_everything, setup_logging, ensure_dir, get_device, worker_init_fn, save_json, effective_name
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
        fft_noise_sigma=cfg.get("fft_noise_sigma", 0.05),
    )
    dataset = DeepfakeDataset(ds_cfg)
    n_workers = cfg.get("num_workers", 4)
    loader = DataLoader(
        dataset,
        batch_size=cfg.get("batch_size", 16),
        shuffle=train,
        num_workers=n_workers,
        pin_memory=True,
        drop_last=train,
        persistent_workers=n_workers > 0,
        prefetch_factor=4 if n_workers > 0 else None,
        worker_init_fn=worker_init_fn,
    )
    return loader


def select_model(model_type: str, pretrained: bool, cfg: dict):
    freq_depth = cfg.get("freq_depth", 3)
    freq_base_channels = cfg.get("freq_base_channels", 32)
    if model_type == "spatial":
        return build_xception(num_classes=1, in_chans=3, pretrained=pretrained)
    if model_type == "freq":
        return FreqCNN(num_classes=1, depth=freq_depth, base_channels=freq_base_channels)
    if model_type == "hybrid":
        return HybridTwoBranch(pretrained=pretrained, freq_depth=freq_depth, freq_base_channels=freq_base_channels)
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


def train_one_epoch(model, loader, model_type, device, optimizer, scaler, loss_fn, accum_steps=1, label_smooth=0.0):
    model.train()
    running_loss = 0.0
    optimizer.zero_grad()
    for i, batch in enumerate(tqdm(loader, desc="train", leave=False)):
        with torch.cuda.amp.autocast(enabled=device.type == "cuda"):
            logits, targets = forward_model(model_type, model, batch, device)
            if label_smooth > 0:
                targets = targets * (1 - label_smooth) + label_smooth * 0.5
            loss = loss_fn(logits, targets) / accum_steps
        scaler.scale(loss).backward()
        if (i + 1) % accum_steps == 0 or (i + 1) == len(loader):
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
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
    parser.add_argument("--freq-depth", type=int, default=None,
                        help="Override config freq_depth for FreqCNN (e.g. --freq-depth 3 for CDF)")
    parser.add_argument("--method", type=str, default=None,
                        choices=["Deepfakes", "Face2Face", "FaceSwap", "NeuralTextures"],
                        help="FFPP only: use method-specific manifests and cache")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.freq_depth is not None:
        cfg["freq_depth"] = args.freq_depth
    seed_everything(args.seed)
    device = get_device()

    # A100 / Ampere+ optimizations
    if device.type == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True   # 3x faster matmuls on A100
        torch.backends.cudnn.allow_tf32 = True

    eff_name = effective_name(args.dataset, args.method)
    n_tag = f"_n{args.n_samples}" if args.n_samples > 0 else ""
    run_dir = Path(cfg["output_root"]) / "runs" / f"{args.model}_{eff_name}{n_tag}_seed{args.seed}"
    ensure_dir(run_dir)
    setup_logging(run_dir / "train.log")
    logging.info(f"Starting training: model={args.model}, dataset={eff_name}, seed={args.seed}, device={device}")
    if args.freq_depth is not None:
        logging.info(f"freq_depth overridden to {args.freq_depth} via CLI")

    manifest_root = Path(cfg["output_root"]) / "manifests" / eff_name
    train_manifest = manifest_root / "train.csv"
    val_manifest = manifest_root / "val.csv"
    if not train_manifest.exists():
        raise FileNotFoundError(f"Train manifest missing at {train_manifest}. Run build_splits.py")

    fft_cache_root = (Path(cfg["output_root"]) / "fft_cache" / eff_name) if args.model in {"freq", "hybrid", "early_fusion"} else None

    train_loader = make_dataloader(train_manifest, cfg, mode=args.model if args.model != "hybrid" else "hybrid", train=True, fft_cache_root=fft_cache_root, seed=args.seed)
    val_loader = make_dataloader(val_manifest, cfg, mode=args.model if args.model != "hybrid" else "hybrid", train=False, fft_cache_root=fft_cache_root, seed=args.seed)

    model = select_model(args.model, pretrained=args.pretrained, cfg=cfg).to(device)
    if cfg.get("compile_model", False) and hasattr(torch, "compile"):
        logging.info("Compiling model with torch.compile (first batch will be slow)...")
        model = torch.compile(model)
    train_df = pd.read_csv(train_manifest)
    n_pos = int((train_df["label"] == 1).sum())
    n_neg = int((train_df["label"] == 0).sum())
    pos_weight = torch.tensor([n_neg / max(n_pos, 1)], device=device)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    logging.info(f"Class balance: {n_neg} neg, {n_pos} pos, pos_weight={pos_weight.item():.3f}")

    # --- Fix B: Differential Learning Rates ---
    base_lr = cfg.get("lr", 1e-4)
    wd = cfg.get("weight_decay", 1e-4)
    backbone_lr = base_lr / 10  # 10x lower LR for pretrained backbone

    if args.model == "spatial":
        # Backbone = all params except the final FC head
        backbone_params = [p for n, p in model.named_parameters() if not n.startswith("head.fc") and not n.startswith("fc")]
        head_params = [p for n, p in model.named_parameters() if n.startswith("head.fc") or n.startswith("fc")]
        if not head_params:
            # timm xception uses 'head' attribute; fall back to all params as backbone
            backbone_params = list(model.parameters())
            optimizer = optim.AdamW(backbone_params, lr=backbone_lr, weight_decay=wd)
        else:
            optimizer = optim.AdamW([
                {"params": backbone_params, "lr": backbone_lr},
                {"params": head_params, "lr": base_lr},
            ], weight_decay=wd)
    elif args.model == "hybrid":
        backbone_params = list(model.spatial.parameters())
        head_params = (
            list(model.freq.parameters())
            + list(model.spatial_proj.parameters())
            + list(model.freq_proj.parameters())
            + list(model.se_gate.parameters())
            + list(model.classifier.parameters())
        )
        optimizer = optim.AdamW([
            {"params": backbone_params, "lr": backbone_lr},
            {"params": head_params, "lr": base_lr},
        ], weight_decay=wd)
    elif args.model == "early_fusion":
        backbone_params = list(model.model.parameters())
        # early_fusion only has model.model; all params are backbone
        optimizer = optim.AdamW([
            {"params": backbone_params, "lr": backbone_lr},
        ], weight_decay=wd)
    else:
        optimizer = optim.AdamW(model.parameters(), lr=base_lr, weight_decay=wd)

    scaler = torch.amp.GradScaler(device=device.type, enabled=device.type == "cuda")

    # --- Fix C: Backbone Freezing for first FREEZE_EPOCHS epochs ---
    if args.model == "spatial":
        # Freeze all backbone params (everything except the final classification head)
        head_param_ids = {id(p) for n, p in model.named_parameters() if n.startswith("head.fc") or n.startswith("fc")}
        for p in model.parameters():
            if id(p) not in head_param_ids:
                p.requires_grad = False
        logging.info(f"Froze spatial backbone for first {FREEZE_EPOCHS} epochs")
    elif args.model == "hybrid":
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

    # --- LR Schedule: linear warmup → cosine decay ---
    warmup_epochs = 3  # Gradual ramp over 3 epochs, unfreeze backbone at epoch 4
    warmup_scheduler = optim.lr_scheduler.LinearLR(
        optimizer, start_factor=0.1, end_factor=1.0, total_iters=warmup_epochs
    )
    cosine_scheduler = optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max(epochs - warmup_epochs, 1), eta_min=1e-6
    )
    scheduler = optim.lr_scheduler.SequentialLR(
        optimizer, schedulers=[warmup_scheduler, cosine_scheduler],
        milestones=[warmup_epochs]
    )

    label_smooth = cfg.get("label_smoothing", 0.05)
    patience = cfg.get("early_stop_patience", 5)
    no_improve_count = 0

    for epoch in range(1, epochs + 1):
        # --- Fix C: Unfreeze backbone after FREEZE_EPOCHS ---
        if epoch == FREEZE_EPOCHS + 1:
            if args.model == "spatial":
                for p in model.parameters():
                    p.requires_grad = True
                logging.info(f"Epoch {epoch}: unfreezing spatial backbone")
            elif args.model == "hybrid":
                for p in model.spatial.parameters():
                    p.requires_grad = True
                logging.info(f"Epoch {epoch}: unfreezing spatial backbone")
            elif args.model == "early_fusion":
                for p in model.model.parameters():
                    p.requires_grad = True
                logging.info(f"Epoch {epoch}: unfreezing backbone")

        train_loss = train_one_epoch(model, train_loader, args.model, device, optimizer, scaler, loss_fn, accum_steps=accum_steps, label_smooth=label_smooth)
        val_metrics = evaluate(model, val_loader, args.model, device)
        history.append({"epoch": epoch, "train_loss": train_loss, **val_metrics})
        current_lrs = [f"{pg['lr']:.2e}" for pg in optimizer.param_groups]
        logging.info(f"Epoch {epoch}: lr={current_lrs}, loss={train_loss:.4f}, val_auc={val_metrics['auc']:.4f}, val_f1={val_metrics['f1']:.4f}")
        scheduler.step()
        if val_metrics["auc"] > best_auc:
            best_auc = val_metrics["auc"]
            no_improve_count = 0
            # Unwrap torch.compile wrapper so checkpoints load on non-compiled models
            unwrapped = getattr(model, '_orig_mod', model)
            torch.save({"state_dict": unwrapped.state_dict(), "epoch": epoch, "config": cfg}, run_dir / "best.pt")
        else:
            no_improve_count += 1
            if no_improve_count >= patience:
                logging.info(f"Early stopping at epoch {epoch}: val AUC did not improve for {patience} consecutive epochs.")
                break

    save_json({"history": history}, run_dir / "metrics.json")
    logging.info(f"Training complete. Best AUC={best_auc:.4f}. Checkpoint at {run_dir/'best.pt'}")


if __name__ == "__main__":
    main()
