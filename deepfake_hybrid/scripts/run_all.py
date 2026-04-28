import argparse
import sys
import subprocess
from pathlib import Path
import logging
import pandas as pd
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, ensure_dir, setup_logging, get_device, worker_init_fn, effective_name, save_json
from deepfake_data import DeepfakeDataset, DatasetConfig
from models.spatial_xception import build_xception
from models.freq_cnn import FreqCNN
from models.hybrid_fusion import HybridTwoBranch, EarlyFusionXception
import metrics as metrics_mod


MODELS_CORE = ["spatial", "freq", "hybrid"]


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
    raise ValueError(model_type)


def _run_inference(cfg, manifest_path, dataset_name, model_type, model, device, seed):
    """Run inference on a manifest split and return (y_true, y_prob)."""
    fft_cache_root = (Path(cfg["output_root"]) / "fft_cache" / dataset_name) if model_type in {"freq", "hybrid", "early_fusion"} else None
    ds_cfg = DatasetConfig(
        manifest_path=manifest_path,
        fft_cache_root=fft_cache_root,
        image_size=cfg.get("image_size", 224),
        max_frames_per_video=cfg.get("max_frames_per_video", 100),
        mode=model_type if model_type != "hybrid" else "hybrid",
        seed=seed,
        train=False,
    )
    dataset = DeepfakeDataset(ds_cfg)
    loader = DataLoader(dataset, batch_size=cfg.get("batch_size", 16), shuffle=False, num_workers=cfg.get("num_workers", 4), pin_memory=True, worker_init_fn=worker_init_fn)
    all_probs, all_targets = [], []
    with torch.no_grad():
        for batch in loader:
            if model_type == "hybrid":
                feats, y = batch
                logits = model(feats["image"].to(device), feats["fft"].to(device)).view(-1)
            else:
                x, y = batch
                logits = model(x.to(device)).view(-1)
            probs = torch.sigmoid(logits)
            all_probs.append(probs.cpu())
            all_targets.append(y.cpu())
    return torch.cat(all_targets).numpy(), torch.cat(all_probs).numpy()


def _load_model(cfg, model_type, checkpoint_path, device):
    model = select_model(model_type, pretrained=False, cfg=cfg)
    checkpoint = torch.load(checkpoint_path, map_location=device)
    state_dict = checkpoint["state_dict"] if isinstance(checkpoint, dict) and "state_dict" in checkpoint else checkpoint
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def compute_val_threshold(cfg, train_dataset_name, model_type, checkpoint_path, run_dir, seed):
    """Pick optimal decision threshold from the val split and save to run_dir/threshold.json."""
    threshold_file = run_dir / "threshold.json"
    if threshold_file.exists():
        import json
        return json.loads(threshold_file.read_text())["threshold"]
    device = get_device()
    val_manifest = Path(cfg["output_root"]) / "manifests" / train_dataset_name / "val.csv"
    if not val_manifest.exists():
        logging.warning(f"Val manifest missing at {val_manifest}; falling back to threshold=0.5")
        return 0.5
    model = _load_model(cfg, model_type, checkpoint_path, device)
    y_true, y_prob = _run_inference(cfg, val_manifest, train_dataset_name, model_type, model, device, seed)
    threshold = metrics_mod.find_optimal_threshold(y_true, y_prob)
    save_json({"threshold": threshold}, threshold_file)
    logging.info(f"  [THRESHOLD] {model_type} trained on {train_dataset_name}: val-optimal threshold={threshold:.4f}")
    return threshold


def eval_checkpoint(cfg, dataset_name, model_type, checkpoint_path, seed, threshold=0.5):
    device = get_device()
    test_manifest = Path(cfg["output_root"]) / "manifests" / dataset_name / "test.csv"
    model = _load_model(cfg, model_type, checkpoint_path, device)
    y_true, y_prob = _run_inference(cfg, test_manifest, dataset_name, model_type, model, device, seed)
    n0, n1 = int((y_true == 0).sum()), int((y_true == 1).sum())
    mean0 = float(y_prob[y_true == 0].mean()) if n0 > 0 else float("nan")
    mean1 = float(y_prob[y_true == 1].mean()) if n1 > 0 else float("nan")
    inverted = " ← INVERTED?" if mean1 < mean0 else ""
    logging.info(
        f"  [DIAG] {dataset_name} test: n={len(y_true)}, "
        f"label_0={n0}, label_1={n1}, "
        f"mean_prob_for_real={mean0:.4f}, mean_prob_for_fake={mean1:.4f}{inverted}"
    )
    metrics = metrics_mod.compute_metrics(y_true, y_prob, threshold=threshold)
    metrics["threshold"] = threshold
    return metrics


def _n_tag(n_samples: int) -> str:
    """Return the n-samples tag used in run / table folder names."""
    return f"_n{n_samples}" if n_samples > 0 else ""


def main():
    parser = argparse.ArgumentParser(description="Run full experiment matrix")
    parser.add_argument("--config", required=True)
    parser.add_argument("--pretrained", action="store_true")
    parser.add_argument("--n-samples", type=int, default=0,
                        help="Number of samples used (only affects output folder naming)")
    parser.add_argument("--dataset", choices=["FFPP", "CDF", "both"], default="both",
                        help="Which training dataset to run (default: both)")
    parser.add_argument("--method", type=str, default=None,
                        choices=["Deepfakes", "Face2Face", "FaceSwap", "NeuralTextures"],
                        help="FFPP only: train/eval on a single manipulation method")
    args = parser.parse_args()

    n_tag = _n_tag(args.n_samples)

    cfg = load_config(args.config)
    setup_logging(Path(cfg["output_root"]) / "runs" / f"run_all{n_tag}.log")
    models_to_run = MODELS_CORE.copy()
    if cfg.get("fusion_mode", "two_branch") == "early_fusion":
        models_to_run.append("early_fusion")

    seeds = list(range(cfg.get("n_seeds", 1)))
    train_datasets = ["FFPP", "CDF"] if args.dataset == "both" else [args.dataset]

    results_in = []
    results_cross = []

    for seed in seeds:
        for train_ds in train_datasets:
            # Apply method only to FFPP
            method_for_ds = args.method if train_ds == "FFPP" else None
            eff_train = effective_name(train_ds, method_for_ds)

            for model_type in models_to_run:
                run_name = f"{model_type}_{eff_train}{n_tag}_seed{seed}"
                run_dir = Path(cfg["output_root"]) / "runs" / run_name
                ckpt = run_dir / "best.pt"
                if not ckpt.exists():
                    # Skip if manifest is missing (e.g. cross-eval pass before dataset is preprocessed)
                    train_manifest = Path(cfg["output_root"]) / "manifests" / eff_train / "train.csv"
                    if not train_manifest.exists():
                        logging.warning(f"Skipping {run_name}: manifest not found at {train_manifest}")
                        continue
                    # train
                    cmd = [sys.executable, str(ROOT / "scripts" / "train.py"), "--config", args.config, "--dataset", train_ds, "--model", model_type, "--seed", str(seed)]
                    if method_for_ds:
                        cmd += ["--method", method_for_ds]
                    if args.n_samples > 0:
                        cmd += ["--n-samples", str(args.n_samples)]
                    if args.pretrained:
                        cmd.append("--pretrained")
                    subprocess.run(cmd, check=True)
                # pick val-optimal threshold once per (model, train_dataset) pair
                threshold = compute_val_threshold(cfg, eff_train, model_type, ckpt, run_dir, seed)
                # eval in-dataset
                metrics_in = eval_checkpoint(cfg, eff_train, model_type, ckpt, seed, threshold=threshold)
                metrics_in["train_dataset"] = eff_train
                metrics_in["test_dataset"] = eff_train
                metrics_in["model"] = model_type
                metrics_in["seed"] = seed
                results_in.append(metrics_in)
                # eval cross (only if the other dataset's manifest exists)
                other_ds = "CDF" if train_ds == "FFPP" else "FFPP"
                other_method = args.method if other_ds == "FFPP" else None
                eff_other = effective_name(other_ds, other_method)
                other_manifest = Path(cfg["output_root"]) / "manifests" / eff_other / "test.csv"
                if other_manifest.exists():
                    metrics_cross = eval_checkpoint(cfg, eff_other, model_type, ckpt, seed, threshold=threshold)
                    metrics_cross["train_dataset"] = eff_train
                    metrics_cross["test_dataset"] = eff_other
                    metrics_cross["model"] = model_type
                    metrics_cross["seed"] = seed
                    results_cross.append(metrics_cross)
                else:
                    logging.warning(f"Skipping cross-dataset eval ({eff_train}→{eff_other}): manifest not found at {other_manifest}")

    method_suffix = f"_{args.method}" if args.method else ""
    tables_dir = Path(cfg["output_root"]) / "tables" / (f"n{args.n_samples}{method_suffix}" if args.n_samples > 0 else f"default{method_suffix}")
    ensure_dir(tables_dir)
    df_in = pd.DataFrame(results_in)
    df_cross = pd.DataFrame(results_cross)
    df_in.to_csv(tables_dir / "Table1_in_dataset.csv", index=False)
    df_cross.to_csv(tables_dir / "Table2_cross_dataset.csv", index=False)

    # generalization drop (only when cross-dataset results exist)
    rows = []
    if not df_cross.empty:
        for model_type in models_to_run:
            for train_ds in train_datasets:
                method_for_ds = args.method if train_ds == "FFPP" else None
                eff_ds = effective_name(train_ds, method_for_ds)
                f1_in = df_in[(df_in.model == model_type) & (df_in.train_dataset == eff_ds)]["f1"].mean()
                f1_cross = df_cross[(df_cross.model == model_type) & (df_cross.train_dataset == eff_ds)]["f1"].mean()
                rows.append({"model": model_type, "train_dataset": eff_ds, "f1_in": f1_in, "f1_cross": f1_cross, "drop": f1_in - f1_cross})
    pd.DataFrame(rows).to_csv(tables_dir / "Table3_generalization_drop.csv", index=False)

    # summary (mean/std over seeds)
    if len(seeds) > 1:
        def summarize(df):
            summary = df.groupby(["model", "train_dataset", "test_dataset"]).agg({
                "acc": ["mean", "std"],
                "precision": ["mean", "std"],
                "recall": ["mean", "std"],
                "f1": ["mean", "std"],
                "auc": ["mean", "std"],
            })
            summary.columns = ["_".join(col).strip("_") for col in summary.columns.values]
            return summary.reset_index()
        summarize(df_in).to_csv(tables_dir / "Table1_in_dataset_summary.csv", index=False)
        summarize(df_cross).to_csv(tables_dir / "Table2_cross_dataset_summary.csv", index=False)
        pd.DataFrame(rows).to_csv(tables_dir / "Table3_drop_summary.csv", index=False)


if __name__ == "__main__":
    main()
