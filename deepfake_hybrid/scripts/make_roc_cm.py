"""Generate ROC curves + confusion matrices from TRAINED checkpoints (inference only).

No training. For one test set, loads one or more checkpoints, runs a forward pass over
the test split, saves per-frame predictions (y_true, y_prob), then plots:
  - one overlaid ROC figure for all models
  - one confusion matrix PNG per model
  - a metrics JSON for all models

Each model is rebuilt from its checkpoint's *embedded config* (freq_depth /
freq_base_channels / image_size) so freq/hybrid match the trained architecture.

Examples
--------
In-dataset FFPP (3 models overlaid), Youden-optimal threshold for the CM:
  python scripts/make_roc_cm.py \
      --models spatial:outputs/runs/spatial_FFPP_n750_seed0/best.pt \
               hybrid:outputs/runs/hybrid_FFPP_n750_seed0/best.pt \
               freq:outputs/runs/freq_FFPP_n750_seed0/best.pt \
      --test-manifest outputs/manifests/FFPP/test.csv \
      --fft-cache-root outputs/fft_cache/FFPP \
      --tag FFPP_in_n750 --title "In-Dataset FFPP (n=750)"

Cross-dataset (train FFPP -> test CDF): point checkpoints at FFPP-trained runs,
test-manifest/fft-cache at CDF:
  python scripts/make_roc_cm.py --models spatial:.../spatial_FFPP_n750_seed0/best.pt ... \
      --test-manifest outputs/manifests/CDF/test.csv --fft-cache-root outputs/fft_cache/CDF \
      --tag FFPP2CDF_n750 --title "Cross-Dataset FFPP->CDF (n=750)"
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from deepfake_data import DeepfakeDataset, DatasetConfig  # noqa: E402
from models.spatial_xception import build_xception  # noqa: E402
from models.freq_cnn import FreqCNN  # noqa: E402
from models.hybrid_fusion import HybridTwoBranch, EarlyFusionXception  # noqa: E402
import metrics as metrics_mod  # noqa: E402

CLASS_NAMES = ["Real", "Fake"]


def build_model(model_type, ckpt_cfg, pretrained=False):
    """Rebuild the architecture using params embedded in the checkpoint config."""
    depth = int(ckpt_cfg.get("freq_depth", 3))
    base = int(ckpt_cfg.get("freq_base_channels", 32))
    if model_type == "spatial":
        return build_xception(num_classes=1, in_chans=3, pretrained=pretrained)
    if model_type == "freq":
        return FreqCNN(num_classes=1, depth=depth, base_channels=base)
    if model_type == "hybrid":
        return HybridTwoBranch(pretrained=pretrained, freq_depth=depth, freq_base_channels=base)
    if model_type == "early_fusion":
        return EarlyFusionXception(pretrained=pretrained)
    raise ValueError(f"Unknown model_type {model_type}")


def forward(model_type, model, batch, device):
    if model_type == "hybrid":
        feats, y = batch
        logits = model(feats["image"].to(device), feats["fft"].to(device)).view(-1)
    else:
        x, y = batch
        logits = model(x.to(device)).view(-1)
    return logits, y.to(device)


@torch.no_grad()
def infer(model_type, ckpt_path, test_manifest, fft_cache_root, device, batch_size, num_workers):
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    ckpt_cfg = ckpt.get("config", {}) if isinstance(ckpt, dict) else {}
    image_size = int(ckpt_cfg.get("image_size", 224))
    max_frames = int(ckpt_cfg.get("max_frames_per_video", 100))

    needs_fft = model_type in {"freq", "hybrid", "early_fusion"}
    ds_cfg = DatasetConfig(
        manifest_path=Path(test_manifest),
        fft_cache_root=Path(fft_cache_root) if (needs_fft and fft_cache_root) else None,
        image_size=image_size,
        max_frames_per_video=max_frames,
        mode=model_type,
        seed=0,
        train=False,
    )
    dataset = DeepfakeDataset(ds_cfg)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False,
                        num_workers=num_workers, pin_memory=False)

    model = build_model(model_type, ckpt_cfg, pretrained=False)
    state = ckpt["state_dict"] if isinstance(ckpt, dict) and "state_dict" in ckpt else ckpt
    model.load_state_dict(state)
    model.to(device).eval()

    probs, targets = [], []
    for batch in loader:
        logits, y = forward(model_type, model, batch, device)
        probs.append(torch.sigmoid(logits).cpu())
        targets.append(y.cpu())
    return torch.cat(targets).numpy().astype(int), torch.cat(probs).numpy()


def resolve_threshold(model_type, ckpt_path, y_true, y_prob, override):
    """Pick CM threshold: explicit override > sibling *_threshold.json > Youden's J on this set."""
    if override is not None:
        return float(override), "manual"
    ck = Path(ckpt_path)
    for cand in (ck.parent / "threshold.json", ck.parent / f"{model_type}_threshold.json"):
        if cand.exists():
            try:
                data = json.loads(cand.read_text())
                thr = data.get("threshold", data.get("optimal_threshold"))
                if thr is not None:
                    return float(thr), f"file:{cand.name}"
            except Exception:
                pass
    return float(metrics_mod.find_optimal_threshold(y_true, y_prob)), "youden"


def plot_roc(per_model, tag, title, out_dir):
    plt.figure(figsize=(5.6, 5.2))
    for m in per_model:
        fpr, tpr, _ = metrics_mod.roc_points(m["y_true"], m["y_prob"])
        plt.plot(fpr, tpr, lw=2, label=f"{m['label']} (AUC = {m['auc']:.3f})")
    plt.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.6, label="Acak (AUC = 0.500)")
    plt.xlim(0, 1); plt.ylim(0, 1.02)
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title(title or f"Kurva ROC — {tag}")
    plt.legend(loc="lower right", fontsize=9)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    path = Path(out_dir) / f"{tag}_roc.png"
    plt.savefig(path, dpi=200); plt.close()
    return path


def plot_cm(m, tag, out_dir):
    thr = m["threshold"]
    y_pred = (m["y_prob"] >= thr).astype(int)
    cm = np.zeros((2, 2), dtype=int)
    for t, p in zip(m["y_true"], y_pred):
        cm[t, p] += 1
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1], CLASS_NAMES); ax.set_yticks([0, 1], CLASS_NAMES)
    ax.set_xlabel("Prediksi"); ax.set_ylabel("Aktual")
    ax.set_title(f"Confusion Matrix — {m['label']}\n(threshold = {thr:.3f}, {m['thr_src']})")
    vmax = cm.max() if cm.max() > 0 else 1
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > vmax / 2 else "black", fontsize=14)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    path = Path(out_dir) / f"{tag}_cm_{m['model']}.png"
    fig.savefig(path, dpi=200); plt.close(fig)
    return path


def main():
    ap = argparse.ArgumentParser(description="ROC + confusion matrix from trained checkpoints (inference only)")
    ap.add_argument("--models", nargs="+", required=True,
                    help="One or more 'modeltype:checkpoint.pt' (e.g. spatial:.../best.pt)")
    ap.add_argument("--test-manifest", required=True)
    ap.add_argument("--fft-cache-root", default=None, help="Needed for freq/hybrid/early_fusion")
    ap.add_argument("--tag", required=True, help="Filename prefix, e.g. FFPP_in_n750")
    ap.add_argument("--title", default=None, help="ROC figure title")
    ap.add_argument("--out-dir", default=str(ROOT / "outputs" / "roc_cm"))
    ap.add_argument("--threshold", type=float, default=None, help="Force CM threshold for all models")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--num-workers", type=int, default=2)
    ap.add_argument("--device", default=None, help="cpu / cuda / mps (default: auto)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    if args.device:
        device = torch.device(args.device)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    per_model, metrics_out, failures = [], {}, []
    for spec in args.models:
        model_type, ckpt = spec.split(":", 1)
        print(f"[{model_type}] loading {ckpt} …", flush=True)
        try:
            y_true, y_prob = infer(model_type, ckpt, args.test_manifest, args.fft_cache_root,
                                   device, args.batch_size, args.num_workers)
        except Exception as e:  # one bad/mismatched checkpoint shouldn't kill the rest
            msg = f"{type(e).__name__}: {str(e).splitlines()[0]}"
            print(f"    !! SKIPPED ({msg})", flush=True)
            failures.append({"model": model_type, "checkpoint": ckpt, "error": msg})
            metrics_out[model_type] = {"checkpoint": ckpt, "error": msg}
            continue
        thr, thr_src = resolve_threshold(model_type, ckpt, y_true, y_prob, args.threshold)
        auc = metrics_mod.compute_metrics(y_true, y_prob, threshold=thr)["auc"]
        label = model_type.capitalize()
        # save predictions
        pred_path = out_dir / f"{args.tag}_preds_{model_type}.csv"
        np.savetxt(pred_path, np.column_stack([y_true, y_prob]),
                   delimiter=",", header="y_true,y_prob", comments="", fmt=["%d", "%.6f"])
        m = dict(model=model_type, label=label, y_true=y_true, y_prob=y_prob,
                 threshold=thr, thr_src=thr_src, auc=auc)
        per_model.append(m)
        metrics_out[model_type] = {
            "checkpoint": ckpt, "n_frames": int(len(y_true)),
            "auc": auc, "threshold": thr, "threshold_source": thr_src,
            **metrics_mod.compute_metrics(y_true, y_prob, threshold=thr),
            "predictions_csv": str(pred_path),
        }
        cm_path = plot_cm(m, args.tag, out_dir)
        print(f"    AUC={auc:.3f}  thr={thr:.3f} ({thr_src})  -> {cm_path.name}", flush=True)

    (out_dir / f"{args.tag}_metrics.json").write_text(json.dumps(metrics_out, indent=2))
    if per_model:
        roc_path = plot_roc(per_model, args.tag, args.title, out_dir)
        print(f"\nSaved ROC -> {roc_path}")
    else:
        print("\nNo model produced predictions; ROC figure skipped.")
    print(f"Saved metrics -> {out_dir / (args.tag + '_metrics.json')}")
    if failures:
        print(f"Skipped {len(failures)} model(s): " + ", ".join(f['model'] for f in failures))
    print(f"All outputs in: {out_dir}")


if __name__ == "__main__":
    main()
