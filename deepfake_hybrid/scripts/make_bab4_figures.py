"""Generate BAB IV figures (Indonesian labels) from the result tables.

Reads the 3-seed summary CSVs (default: outputs/tables/n*/ — the adopted 2026-06-20
run) and produces thesis-ready PNGs into documents/media_v2/ with the gambar_4_x_*
naming convention. No model inference needed — purely re-plots the aggregated metrics.

Usage:
  python scripts/make_bab4_figures.py                 # default: outputs/tables (run baru)
  python scripts/make_bab4_figures.py results_vast_20260609/tables   # override (run lama)

Produces:
  gambar_4_3_perbandingan_in_dataset.png     (bar F1 + AUC, in-dataset n=750)
  gambar_4_5_perbandingan_cross_dataset.png  (bar F1 + AUC, cross-dataset n=750)
  gambar_4_7_generalization_drop.png         (bar Delta F1 per model/dataset, n=750)
  gambar_4_8_scaling_auc.png                 (line AUC vs ukuran sampel, in & cross)
"""
import sys
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TABLES = (Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "tables")
if not TABLES.is_absolute():
    TABLES = ROOT / TABLES
OUT = ROOT.parent / "documents" / "media_v2"
OUT.mkdir(parents=True, exist_ok=True)

# konsisten dgn plot lama: spasial biru, hybrid hijau, frekuensi oranye
COLOR = {"spatial": "#1f77b4", "hybrid": "#2ca02c", "freq": "#ff7f0e"}
LABEL = {"spatial": "Spasial (XceptionNet)", "hybrid": "Hybrid", "freq": "Frekuensi (FreqCNN)"}
ORDER = ["spatial", "hybrid", "freq"]
DS_LABEL = {"FFPP": "FaceForensics++", "CDF": "Celeb-DF"}

plt.rcParams.update({"font.size": 12, "axes.titlesize": 14, "figure.dpi": 200})


def _bars(ax, groups, get_val, title, ylabel, ylim=(0, 1.05)):
    """groups: list of (group_label, key_prefix). get_val(model, group_key) -> float."""
    n_models = len(ORDER)
    width = 0.8 / n_models
    xs = range(len(groups))
    for i, m in enumerate(ORDER):
        vals = [get_val(m, g[1]) for g in groups]
        pos = [x - 0.4 + width / 2 + i * width for x in xs]
        bars = ax.bar(pos, vals, width, label=LABEL[m], color=COLOR[m], edgecolor="black", linewidth=0.4)
        for p, v in zip(pos, vals):
            ax.text(p, v + 0.012, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(list(xs)); ax.set_xticklabels([g[0] for g in groups])
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel(ylabel); ax.set_ylim(*ylim)
    ax.grid(axis="y", alpha=0.3)


def fig_in_dataset():
    df = pd.read_csv(TABLES / "n750" / "Table1_in_dataset_summary.csv")
    def val(metric):
        return lambda m, ds: float(df[(df.model == m) & (df.train_dataset == ds)][metric + "_mean"].iloc[0])
    groups = [(DS_LABEL["FFPP"], "FFPP"), (DS_LABEL["CDF"], "CDF")]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6))
    _bars(a1, groups, val("f1"), "F1-Score", "F1-Score")
    _bars(a2, groups, val("auc"), "AUC", "AUC")
    a1.legend(loc="upper left", fontsize=9)
    fig.suptitle("Perbandingan Performa In-Dataset (n = 750)", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p = OUT / "gambar_4_3_perbandingan_in_dataset.png"
    fig.savefig(p); plt.close(fig); return p


def fig_cross_dataset():
    df = pd.read_csv(TABLES / "n750" / "Table2_cross_dataset_summary.csv")
    # group key = train dataset; direction label
    dirs = [("FFPP→CDF", "FFPP"), ("CDF→FFPP", "CDF")]
    def val(metric):
        return lambda m, tr: float(df[(df.model == m) & (df.train_dataset == tr)][metric + "_mean"].iloc[0])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6))
    _bars(a1, dirs, val("f1"), "F1-Score", "F1-Score")
    _bars(a2, dirs, val("auc"), "AUC", "AUC")
    a1.legend(loc="upper right", fontsize=9)
    fig.suptitle("Perbandingan Performa Cross-Dataset (n = 750)", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p = OUT / "gambar_4_5_perbandingan_cross_dataset.png"
    fig.savefig(p); plt.close(fig); return p


def fig_drop():
    df = pd.read_csv(TABLES / "n750" / "Table3_drop_summary.csv")
    fig, ax = plt.subplots(figsize=(9, 6))
    width = 0.38
    xs = range(len(ORDER))
    for j, ds in enumerate(["FFPP", "CDF"]):
        vals = [float(df[(df.model == m) & (df.train_dataset == ds)]["drop"].iloc[0]) for m in ORDER]
        pos = [x - width / 2 + j * width for x in xs]
        color = "#4c72b0" if ds == "FFPP" else "#dd8452"
        ax.bar(pos, vals, width, label=f"Dilatih {DS_LABEL[ds]}", color=color, edgecolor="black", linewidth=0.4)
        for p_, v in zip(pos, vals):
            ax.text(p_, v + (0.012 if v >= 0 else -0.03), f"{v:+.3f}", ha="center",
                    va="bottom" if v >= 0 else "top", fontsize=9)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(list(xs)); ax.set_xticklabels([LABEL[m] for m in ORDER])
    ax.set_ylabel("Generalization Drop (Δ F1-Score)")
    ax.set_title("Generalization Drop per Model dan Dataset Pelatihan (n = 750)", fontweight="bold")
    ax.legend(fontsize=10); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    p = OUT / "gambar_4_7_generalization_drop.png"
    fig.savefig(p); plt.close(fig); return p


def fig_scaling():
    tiers = [250, 500, 750]
    ind = {n: pd.read_csv(TABLES / f"n{n}" / "Table1_in_dataset_summary.csv") for n in tiers}
    cro = {n: pd.read_csv(TABLES / f"n{n}" / "Table2_cross_dataset_summary.csv") for n in tiers}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 6))
    style = {"FFPP": "-", "CDF": "--"}
    # in-dataset
    for m in ORDER:
        for ds in ["FFPP", "CDF"]:
            ys = [float(ind[n][(ind[n].model == m) & (ind[n].train_dataset == ds)]["auc_mean"].iloc[0]) for n in tiers]
            a1.plot(tiers, ys, style[ds], marker="o", color=COLOR[m], label=f"{LABEL[m].split(' ')[0]} {DS_LABEL[ds]}")
    a1.set_title("In-Dataset", fontweight="bold")
    # cross-dataset
    for m in ORDER:
        for tr, lab in [("FFPP", "FFPP→CDF"), ("CDF", "CDF→FFPP")]:
            ys = [float(cro[n][(cro[n].model == m) & (cro[n].train_dataset == tr)]["auc_mean"].iloc[0]) for n in tiers]
            a2.plot(tiers, ys, style[tr], marker="s", color=COLOR[m], label=f"{LABEL[m].split(' ')[0]} {lab}")
    a2.set_title("Cross-Dataset", fontweight="bold")
    for ax in (a1, a2):
        ax.set_xlabel("Ukuran sampel (jumlah video)"); ax.set_ylabel("AUC")
        ax.set_xticks(tiers); ax.set_ylim(0.45, 1.0); ax.grid(alpha=0.3)
        ax.axhline(0.5, color="grey", ls=":", lw=1, alpha=0.7)
        ax.legend(fontsize=8, ncol=1)
    fig.suptitle("Pengaruh Ukuran Sampel terhadap AUC", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p = OUT / "gambar_4_8_scaling_auc.png"
    fig.savefig(p); plt.close(fig); return p


if __name__ == "__main__":
    for fn in (fig_in_dataset, fig_cross_dataset, fig_drop, fig_scaling):
        print("saved", fn().relative_to(ROOT.parent))
