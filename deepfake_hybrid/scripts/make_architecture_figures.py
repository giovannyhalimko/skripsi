"""
Generate the BAB III architecture / pipeline figures, corrected to match the
actual code + config (freq base_channels=64 -> 512-d, hybrid dropout 0.5, etc.).

Outputs PNGs to documents/media_v2/:
  - gambar_3_4_flowchart_preprocessing.png   (branched pipeline)
  - gambar_3_8_freqcnn_architecture.png       (base=64, 512-d, ~4.2M)
  - gambar_3_9_hybrid_twobranch.png           (freq 512-d, proj 512->256, Drop 0.5)

Run:  deepfake_hybrid/.venv/bin/python scripts/make_architecture_figures.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[2] / "documents" / "media_v2"
OUT.mkdir(parents=True, exist_ok=True)

# palette matched to existing diagrams
NAVY   = "#33475B"
BLUE   = "#2980B9"
RED    = "#E24A38"
PURPLE = "#8E44AD"
GREEN  = "#27AE60"
ORANGE = "#F0932B"
INK    = "#1c1c1a"
TINT_SP = "#EAF1F8"
TINT_FR = "#FCECEA"


def box(ax, cx, cy, w, h, text, fc=NAVY, tc="white", fs=11, ec=INK, lw=1.4, weight="bold"):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                 boxstyle="round,pad=0.015,rounding_size=0.06",
                 facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", color=tc, fontsize=fs,
            fontweight=weight, zorder=3, linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, color=INK, lw=2.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=16, color=color, lw=lw, zorder=1,
                 shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- 3.8 FreqCNN
def make_freqcnn():
    fig, ax = plt.subplots(figsize=(20, 4.2))
    ax.set_xlim(0, 122); ax.set_ylim(0, 22); ax.axis("off")
    ax.set_title("Arsitektur FreqCNN (depth = 5, base_channels = 64, ~4,2 juta parameter)",
                 fontsize=16, fontweight="bold", pad=14)
    y = 11; w = 9.4; h = 8.2; gap = 10.4; x = 6
    steps = [
        ("FFT Input\n(1, 224, 224)", NAVY),
        ("FreqBlock 1\n1→64\n112×112", NAVY),
        ("FreqBlock 2\n64→128\n56×56", NAVY),
        ("FreqBlock 3\n128→256\n28×28", NAVY),
        ("FreqBlock 4\n256→512\n14×14", NAVY),
        ("FreqBlock 5\n512→512\n7×7", NAVY),
        ("Dropout2d\n(0,2)", ORANGE),
        ("GAP\n512→1", PURPLE),
        ("FC\n512→256\n+ReLU", BLUE),
        ("Drop\n(0,3)", ORANGE),
        ("FC\n256→1", BLUE),
        ("Logit", GREEN),
    ]
    xs = [x + i * gap for i in range(len(steps))]
    for xi, (txt, c) in zip(xs, steps):
        box(ax, xi, y, w, h, txt, fc=c, fs=10)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + w / 2, y, xs[i + 1] - w / 2, y)
    fig.tight_layout()
    fig.savefig(OUT / "gambar_3_8_freqcnn_architecture.png", dpi=210, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------- 3.9 Hybrid
def make_hybrid():
    fig, ax = plt.subplots(figsize=(21, 8.6))
    ax.set_xlim(0, 114); ax.set_ylim(0, 44); ax.axis("off")
    ax.set_title("Arsitektur HybridTwoBranch (Late Fusion)", fontsize=17,
                 fontweight="bold", pad=10)
    w = 12; h = 7; ytop = 34; ybot = 10
    xs = [8, 26, 43, 58, 71]
    ax.text(xs[0], ytop + 6.5, "Cabang Spasial", color=BLUE, fontsize=13, fontweight="bold", ha="center")
    ax.text(xs[0], ybot - 6.5, "Cabang Frekuensi", color=RED, fontsize=13, fontweight="bold", ha="center")
    # spatial row
    sp = [("RGB Input\n(3, 224, 224)", NAVY, 12),
          ("XceptionNet\nBackbone\n(frozen 3 epoch)", BLUE, 13),
          ("2048-d", BLUE, 8.5),
          ("Proj\nLinear+BN+ReLU\n2048→256", PURPLE, 12),
          ("256", PURPLE, 6.5)]
    for xi, (txt, c, ww) in zip(xs, sp):
        box(ax, xi, ytop, ww, h, txt, fc=c, fs=10)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + sp[i][2] / 2, ytop, xs[i + 1] - sp[i + 1][2] / 2, ytop, color=BLUE)
    # freq row
    fr = [("FFT Input\n(1, 224, 224)", NAVY, 12),
          ("FreqCNN\nBackbone\n(5 FreqBlocks)", RED, 13),
          ("512-d", RED, 8.5),
          ("Proj\nLinear+BN+ReLU\n512→256", PURPLE, 12),
          ("256", PURPLE, 6.5)]
    for xi, (txt, c, ww) in zip(xs, fr):
        box(ax, xi, ybot, ww, h, txt, fc=c, fs=10)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + fr[i][2] / 2, ybot, xs[i + 1] - fr[i + 1][2] / 2, ybot, color=RED)
    # merge into concat -> SE -> classifier
    ymid = (ytop + ybot) / 2
    concat_cx, se_cx, cls_cx = 82, 93, 105
    for yb in (ytop, ybot):
        arrow(ax, xs[-1] + 3.25, yb, concat_cx - 4.5, ymid, color=INK, lw=2.0)
    box(ax, concat_cx, ymid, 9, h, "Concat\n512-d", fc=GREEN, fs=10)
    box(ax, se_cx, ymid, 9, h, "SE Gate\n512→512", fc=ORANGE, fs=10)
    box(ax, cls_cx, ymid, 11, h + 1.6, "Classifier\nDrop(0,5)\nFC 512→128\nFC 128→1", fc=NAVY, fs=9.5)
    arrow(ax, concat_cx + 4.5, ymid, se_cx - 4.5, ymid)
    arrow(ax, se_cx + 4.5, ymid, cls_cx - 5.5, ymid)
    fig.tight_layout()
    fig.savefig(OUT / "gambar_3_9_hybrid_twobranch.png", dpi=210, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ------------------------------------------------------- 3.4 pipeline flowchart
def make_flowchart():
    fig, ax = plt.subplots(figsize=(12.5, 18.5))
    ax.set_xlim(0, 100); ax.set_ylim(-30, 168); ax.axis("off")
    W = 46; H = 8; xc = 50

    def term(cx, cy, t):
        ax.add_patch(FancyBboxPatch((cx - 14, cy - 3.6), 28, 7.2,
                     boxstyle="round,pad=0.02,rounding_size=3.6",
                     facecolor="#EAE7DF", edgecolor=INK, linewidth=1.6, zorder=2))
        ax.text(cx, cy, t, ha="center", va="center", color=INK, fontsize=12,
                fontweight="bold", zorder=3)

    def pnode(cx, cy, title, meta="", w=W, h=H, fc="white"):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                     boxstyle="round,pad=0.02,rounding_size=1.4",
                     facecolor=fc, edgecolor=INK, linewidth=1.5, zorder=2))
        if meta:
            ax.text(cx, cy + 1.2, title, ha="center", va="center", color=INK, fontsize=10.5, fontweight="bold", zorder=3)
            ax.text(cx, cy - 2.2, meta, ha="center", va="center", color="#5a5a54", fontsize=8.3, zorder=3)
        else:
            ax.text(cx, cy, title, ha="center", va="center", color=INK, fontsize=10.5, fontweight="bold", zorder=3)

    def vdown(cy_from, cy_to, cx=xc, color=INK):
        arrow(ax, cx, cy_from, cx, cy_to, color=color, lw=1.8)

    y = 162
    term(xc, y, "START"); y0 = y - 3.6
    y = 152; vdown(y0, y + H / 2); pnode(xc, y, "Dataset Video", "FaceForensics++ (c23) & Celeb-DF v2")
    y2 = 141; vdown(y - H / 2, y2 + H / 2); pnode(xc, y2, "Ekstraksi Frame", "5 FPS · maks. 50 frame / video"); y = y2
    y2 = 130; vdown(y - H / 2, y2 + H / 2); pnode(xc, y2, "Deteksi Wajah & Cropping", "MTCNN · margin 0,3 · fallback frame penuh"); y = y2
    y2 = 119; vdown(y - H / 2, y2 + H / 2); pnode(xc, y2, "Pembagian Dataset", "Train 70% / Val 15% / Test 15% · stratified per-video"); y = y2

    # split label
    ax.text(xc, 111.5, "Setiap frame → dua representasi paralel", ha="center", color="#5a5a54", fontsize=9)
    vdown(y - H / 2, 110)

    # branch lanes
    xL, xR = 27, 73
    bw = 40
    # fork arrows
    ax.add_patch(FancyArrowPatch((xc, 110), (xL, 105), arrowstyle="-|>", mutation_scale=13, color=BLUE, lw=1.7))
    ax.add_patch(FancyArrowPatch((xc, 110), (xR, 105), arrowstyle="-|>", mutation_scale=13, color=RED, lw=1.7))
    ax.text(xL, 108.5, "CABANG SPASIAL · RGB", ha="center", color=BLUE, fontsize=8.5, fontweight="bold")
    ax.text(xR, 108.5, "CABANG FREKUENSI · FFT", ha="center", color=RED, fontsize=8.5, fontweight="bold")

    def lane(cx, steps, tint, ac, top=101):
        yy = top; ys = []
        for (t, m) in steps:
            ax.add_patch(FancyBboxPatch((cx - bw / 2, yy - 4), bw, 8,
                         boxstyle="round,pad=0.02,rounding_size=1.2",
                         facecolor=tint, edgecolor=ac, linewidth=1.3, zorder=2))
            if m:
                ax.text(cx, yy + 1.1, t, ha="center", va="center", color=INK, fontsize=8.8, fontweight="bold", zorder=3)
                ax.text(cx, yy - 2.1, m, ha="center", va="center", color="#5a5a54", fontsize=7.2, zorder=3)
            else:
                ax.text(cx, yy, t, ha="center", va="center", color=INK, fontsize=8.8, fontweight="bold", zorder=3)
            ys.append(yy); yy -= 12
        for i in range(len(ys) - 1):
            arrow(ax, cx, ys[i] - 4, cx, ys[i + 1] + 4, color=ac, lw=1.4)
        return ys[-1] - 4

    sp_bot = lane(xL, [
        ("Resize 224×224", ""),
        ("Normalisasi ImageNet", "tetap 3-kanal warna"),
        ("Augmentasi (pelatihan)", "ColorJitter · RRC · HFlip · RandErasing"),
    ], TINT_SP, BLUE)
    fr_bot = lane(xR, [
        ("Konversi Grayscale", "Y=0,299R+0,587G+0,114B"),
        ("Resize 224×224", ""),
        ("FFT 2D + FFTShift", "np.fft.fft2 → fftshift"),
        ("Magnitude & High-Pass", "|F(u,v)| × Gaussian HPF (β=0,15)"),
        ("Log Scaling", "log(1 + |F(u,v)|)"),
        ("Cache .npy + Z-Score", "μ,σ per-dataset"),
        ("Augmentasi (pelatihan)", "Noise σ=0,05 · Spectral band mask"),
    ], TINT_FR, RED)

    merge_y = min(sp_bot, fr_bot) - 6
    ax.add_patch(FancyArrowPatch((xL, sp_bot), (xc, merge_y + 4), arrowstyle="-|>", mutation_scale=13, color=BLUE, lw=1.7))
    ax.add_patch(FancyArrowPatch((xR, fr_bot), (xc, merge_y + 4), arrowstyle="-|>", mutation_scale=13, color=RED, lw=1.7))

    y = merge_y
    pnode(xc, y, "Pelatihan Model", "Spatial / Freq / Hybrid  ·  Hybrid = late fusion (proyeksi→concat→SE gating→classifier)")
    y2 = y - 11; vdown(y - H / 2, y2 + H / 2); pnode(xc, y2, "Validasi → Checkpoint Terbaik", "seleksi & early stopping by AUC validasi"); y = y2
    y2 = y - 11; vdown(y - H / 2, y2 + H / 2); pnode(xc, y2, "Evaluasi (In-dataset & Cross-dataset)", "accuracy, precision, recall, F1, AUC"); y = y2
    y2 = y - 11; vdown(y - H / 2, y2 + H / 2); pnode(xc, y2, "Tabel Hasil → Analisis"); y = y2
    y2 = y - 10; vdown(y - H / 2, y2 + 3.6); term(xc, y2, "STOP")

    fig.savefig(OUT / "gambar_3_4_flowchart_preprocessing.png", dpi=200, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    make_freqcnn(); print("saved gambar_3_8_freqcnn_architecture.png")
    make_hybrid();  print("saved gambar_3_9_hybrid_twobranch.png")
    make_flowchart(); print("saved gambar_3_4_flowchart_preprocessing.png")
    print("-> written to", OUT)
