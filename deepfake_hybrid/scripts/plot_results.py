#!/usr/bin/env python3
"""Generate publication-quality plots for BAB IV (Results & Discussion).

Usage
-----
    python scripts/plot_results.py --config config.yaml --n-samples 50,200,400
    python scripts/plot_results.py --config colab_config.yaml --n-samples 50,200,400 --output-dir outputs/plots
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — safe for headless servers / Colab
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODELS = ["spatial", "freq", "hybrid"]
MODEL_LABELS = {"spatial": "Spatial (XceptionNet)", "freq": "Frequency (FreqCNN)", "hybrid": "Hybrid"}
MODEL_COLORS = {"spatial": "#1f77b4", "freq": "#ff7f0e", "hybrid": "#2ca02c"}
DATASETS = ["FFPP", "CDF"]
DATASET_LABELS = {"FFPP": "FaceForensics++", "CDF": "Celeb-DF"}

STYLE = "seaborn-v0_8-whitegrid"  # clean, thesis-friendly

FIG_W, FIG_H = 8, 6
DPI = 300

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def _apply_style():
    """Apply a clean matplotlib style; fall back gracefully."""
    try:
        plt.style.use(STYLE)
    except OSError:
        try:
            plt.style.use("seaborn-whitegrid")
        except OSError:
            pass  # stick with default


def _save(fig: plt.Figure, outdir: Path, name: str):
    outdir.mkdir(parents=True, exist_ok=True)
    dest = outdir / name
    fig.savefig(dest, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    log.info("Saved %s", dest)


def _read_csv_safe(path: Path) -> Optional[pd.DataFrame]:
    if not path.exists():
        log.warning("File not found, skipping: %s", path)
        return None
    df = pd.read_csv(path)
    if df.empty:
        log.warning("Empty CSV, skipping: %s", path)
        return None
    return df


def _read_metrics_json(path: Path) -> Optional[List[dict]]:
    if not path.exists():
        return None
    with open(path) as f:
        data = json.load(f)
    history = data.get("history")
    if not history:
        return None
    return history


# ---------------------------------------------------------------------------
# Plot 1 — Training Curves
# ---------------------------------------------------------------------------

def plot_training_curves(output_root: Path, outdir: Path, n_values: List[int]):
    """One figure per (model, dataset, N) with train_loss, val_auc, val_f1."""
    for n in n_values:
        for ds in DATASETS:
            for model in MODELS:
                # Collect all seeds
                seed = 0
                while True:
                    run_dir = output_root / "runs" / f"{model}_{ds}_n{n}_seed{seed}"
                    history = _read_metrics_json(run_dir / "metrics.json")
                    if history is None:
                        break
                    # Only plot seed 0 (main run); extend later if multi-seed
                    if seed == 0:
                        epochs = [e["epoch"] for e in history]
                        train_loss = [e["train_loss"] for e in history]
                        val_auc = [e.get("auc", np.nan) for e in history]
                        val_f1 = [e.get("f1", np.nan) for e in history]

                        fig, ax1 = plt.subplots(figsize=(FIG_W, FIG_H))
                        color_loss = "#d62728"
                        color_auc = "#1f77b4"
                        color_f1 = "#2ca02c"

                        ax1.set_xlabel("Epoch", fontsize=12)
                        ax1.set_ylabel("Loss", color=color_loss, fontsize=12)
                        ln1 = ax1.plot(epochs, train_loss, color=color_loss, linewidth=2,
                                       marker="o", markersize=4, label="Train Loss")
                        ax1.tick_params(axis="y", labelcolor=color_loss)
                        ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

                        ax2 = ax1.twinx()
                        ax2.set_ylabel("Metric Value", fontsize=12)
                        ln2 = ax2.plot(epochs, val_auc, color=color_auc, linewidth=2,
                                       marker="s", markersize=4, label="Val AUC")
                        ln3 = ax2.plot(epochs, val_f1, color=color_f1, linewidth=2,
                                       marker="^", markersize=4, label="Val F1")
                        ax2.set_ylim(0, 1.05)

                        # Combined legend
                        lns = ln1 + ln2 + ln3
                        labs = [l.get_label() for l in lns]
                        ax1.legend(lns, labs, loc="center right", fontsize=10)

                        title = f"{MODEL_LABELS[model]} — {DATASET_LABELS[ds]} (N={n})"
                        fig.suptitle(title, fontsize=13, fontweight="bold")
                        fig.tight_layout(rect=[0, 0, 1, 0.95])

                        _save(fig, outdir, f"training_curves_{model}_{ds}_n{n}.png")
                    seed += 1
                    if seed > 10:
                        break  # safety cap


# ---------------------------------------------------------------------------
# Plot 2 — Model Comparison Bar Charts (F1 & AUC)
# ---------------------------------------------------------------------------

def plot_comparison_bars(output_root: Path, outdir: Path, n_values: List[int]):
    """Grouped bar chart: models on x, grouped by train_dataset, bars for F1 & AUC."""
    for n in n_values:
        for table_key, label_suffix in [("Table1_in_dataset", "in_dataset"),
                                         ("Table2_cross_dataset", "cross_dataset")]:
            csv_path = output_root / "tables" / f"n{n}" / f"{table_key}.csv"
            df = _read_csv_safe(csv_path)
            if df is None:
                continue

            # Average over seeds
            agg = df.groupby(["train_dataset", "model"])[["f1", "auc"]].mean().reset_index()

            fig, axes = plt.subplots(1, 2, figsize=(FIG_W * 1.3, FIG_H), sharey=True)
            bar_width = 0.25
            metrics = ["f1", "auc"]
            metric_labels = ["F1-Score", "AUC"]

            for ax, metric, mlabel in zip(axes, metrics, metric_labels):
                x_pos = np.arange(len(DATASETS))
                for i, model in enumerate(MODELS):
                    vals = []
                    for ds in DATASETS:
                        row = agg[(agg.train_dataset == ds) & (agg.model == model)]
                        vals.append(row[metric].values[0] if len(row) else 0)
                    offset = (i - 1) * bar_width
                    bars = ax.bar(x_pos + offset, vals, bar_width,
                                  label=MODEL_LABELS[model], color=MODEL_COLORS[model],
                                  edgecolor="black", linewidth=0.5)
                    # Value labels on bars
                    for bar, v in zip(bars, vals):
                        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                                f"{v:.3f}", ha="center", va="bottom", fontsize=8)

                ax.set_xticks(x_pos)
                ax.set_xticklabels([DATASET_LABELS[d] for d in DATASETS], fontsize=10)
                ax.set_ylabel(mlabel, fontsize=11)
                ax.set_ylim(0, 1.15)
                ax.set_title(mlabel, fontsize=12, fontweight="bold")
                ax.legend(fontsize=8, loc="upper right")

            scenario = "In-Dataset" if "in" in label_suffix else "Cross-Dataset"
            fig.suptitle(f"Model Comparison — {scenario} (N={n})", fontsize=13, fontweight="bold")
            fig.tight_layout(rect=[0, 0, 1, 0.93])
            _save(fig, outdir, f"comparison_{label_suffix}_n{n}.png")


# ---------------------------------------------------------------------------
# Plot 4 — Generalization Drop
# ---------------------------------------------------------------------------

def plot_generalization_drop(output_root: Path, outdir: Path, n_values: List[int]):
    """Side-by-side bars: F1 in-dataset vs F1 cross-dataset for each model, grouped by train_dataset."""
    for n in n_values:
        csv_path = output_root / "tables" / f"n{n}" / "Table3_generalization_drop.csv"
        df = _read_csv_safe(csv_path)
        if df is None:
            continue

        fig, axes = plt.subplots(1, len(DATASETS), figsize=(FIG_W * 1.2, FIG_H), sharey=True)
        if len(DATASETS) == 1:
            axes = [axes]

        bar_width = 0.3

        for ax, ds in zip(axes, DATASETS):
            sub = df[df.train_dataset == ds]
            if sub.empty:
                continue
            x_pos = np.arange(len(MODELS))
            f1_in_vals = []
            f1_cross_vals = []
            for model in MODELS:
                row = sub[sub.model == model]
                f1_in_vals.append(row["f1_in"].values[0] if len(row) else 0)
                f1_cross_vals.append(row["f1_cross"].values[0] if len(row) else 0)

            bars_in = ax.bar(x_pos - bar_width / 2, f1_in_vals, bar_width,
                             label="In-Dataset F1", color="#4c72b0", edgecolor="black", linewidth=0.5)
            bars_cross = ax.bar(x_pos + bar_width / 2, f1_cross_vals, bar_width,
                                label="Cross-Dataset F1", color="#dd8452", edgecolor="black", linewidth=0.5)

            # Value labels
            for bar, v in zip(bars_in, f1_in_vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=8)
            for bar, v in zip(bars_cross, f1_cross_vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                        f"{v:.3f}", ha="center", va="bottom", fontsize=8)

            ax.set_xticks(x_pos)
            ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS], fontsize=9, rotation=15, ha="right")
            ax.set_ylabel("F1-Score", fontsize=11)
            ax.set_ylim(0, 1.15)
            ax.set_title(f"Train: {DATASET_LABELS[ds]}", fontsize=12, fontweight="bold")
            ax.legend(fontsize=9, loc="upper right")

        fig.suptitle(f"Generalization Drop (N={n})", fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        _save(fig, outdir, f"generalization_drop_n{n}.png")


# ---------------------------------------------------------------------------
# Plot 5 — Sample-Size Scaling
# ---------------------------------------------------------------------------

def plot_scaling(output_root: Path, outdir: Path, n_values: List[int]):
    """Line chart: N on x-axis, metric on y-axis, one line per model."""
    if len(n_values) < 2:
        log.info("Fewer than 2 N values — skipping scaling plots.")
        return

    for metric, ylabel in [("f1", "F1-Score"), ("auc", "AUC")]:
        fig, axes = plt.subplots(1, len(DATASETS), figsize=(FIG_W * 1.2, FIG_H), sharey=True)
        if len(DATASETS) == 1:
            axes = [axes]

        any_data = False

        for ax, ds in zip(axes, DATASETS):
            for model in MODELS:
                vals = []
                ns_available = []
                for n in sorted(n_values):
                    csv_path = output_root / "tables" / f"n{n}" / "Table1_in_dataset.csv"
                    df = _read_csv_safe(csv_path)
                    if df is None:
                        continue
                    row = df[(df.model == model) & (df.train_dataset == ds)]
                    if row.empty:
                        continue
                    vals.append(row[metric].mean())
                    ns_available.append(n)

                if vals:
                    any_data = True
                    ax.plot(ns_available, vals, marker="o", markersize=6,
                            linewidth=2, label=MODEL_LABELS[model],
                            color=MODEL_COLORS[model])

            ax.set_xlabel("N (samples per class)", fontsize=11)
            ax.set_ylabel(ylabel, fontsize=11)
            ax.set_title(f"Train: {DATASET_LABELS[ds]}", fontsize=12, fontweight="bold")
            ax.set_xticks(sorted(n_values))
            ax.set_xticklabels([str(n) for n in sorted(n_values)])
            ax.set_ylim(0, 1.05)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)

        if not any_data:
            plt.close(fig)
            log.warning("No data found for scaling_%s plot.", metric)
            continue

        fig.suptitle(f"Sample-Size Scaling — {ylabel}", fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        _save(fig, outdir, f"scaling_{metric}.png")

    # Also create cross-dataset scaling plots
    for metric, ylabel in [("f1", "F1-Score"), ("auc", "AUC")]:
        fig, axes = plt.subplots(1, len(DATASETS), figsize=(FIG_W * 1.2, FIG_H), sharey=True)
        if len(DATASETS) == 1:
            axes = [axes]

        any_data = False

        for ax, ds in zip(axes, DATASETS):
            for model in MODELS:
                vals = []
                ns_available = []
                for n in sorted(n_values):
                    csv_path = output_root / "tables" / f"n{n}" / "Table2_cross_dataset.csv"
                    df = _read_csv_safe(csv_path)
                    if df is None:
                        continue
                    row = df[(df.model == model) & (df.train_dataset == ds)]
                    if row.empty:
                        continue
                    vals.append(row[metric].mean())
                    ns_available.append(n)

                if vals:
                    any_data = True
                    ax.plot(ns_available, vals, marker="o", markersize=6,
                            linewidth=2, label=MODEL_LABELS[model],
                            color=MODEL_COLORS[model])

            ax.set_xlabel("N (samples per class)", fontsize=11)
            ax.set_ylabel(ylabel, fontsize=11)
            ax.set_title(f"Train: {DATASET_LABELS[ds]}", fontsize=12, fontweight="bold")
            ax.set_xticks(sorted(n_values))
            ax.set_xticklabels([str(n) for n in sorted(n_values)])
            ax.set_ylim(0, 1.05)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)

        if not any_data:
            plt.close(fig)
            log.warning("No data found for scaling_%s_cross plot.", metric)
            continue

        fig.suptitle(f"Sample-Size Scaling (Cross-Dataset) — {ylabel}", fontsize=13, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.93])
        _save(fig, outdir, f"scaling_{metric}_cross.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate BAB IV plots for deepfake detection thesis."
    )
    parser.add_argument("--config", required=True,
                        help="Path to YAML config (needs output_root)")
    parser.add_argument("--n-samples", required=True,
                        help="Comma-separated list of N values, e.g. '50,200,400'")
    parser.add_argument("--output-dir", default=None,
                        help="Directory to save plots (default: <output_root>/plots)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    cfg = _load_config(args.config)
    output_root = Path(cfg["output_root"])

    n_values = [int(x.strip()) for x in args.n_samples.split(",")]

    if args.output_dir:
        outdir = Path(args.output_dir)
    else:
        outdir = output_root / "plots"

    _apply_style()

    log.info("Output root : %s", output_root)
    log.info("N values    : %s", n_values)
    log.info("Plot dir    : %s", outdir)

    # --- Generate all plots ---
    log.info("=== Plot 1: Training Curves ===")
    plot_training_curves(output_root, outdir, n_values)

    log.info("=== Plot 2: Model Comparison Bar Charts ===")
    plot_comparison_bars(output_root, outdir, n_values)

    log.info("=== Plot 4: Generalization Drop ===")
    plot_generalization_drop(output_root, outdir, n_values)

    log.info("=== Plot 5: Sample-Size Scaling ===")
    plot_scaling(output_root, outdir, n_values)

    log.info("All plots saved to %s", outdir)


if __name__ == "__main__":
    main()
