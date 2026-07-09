"""Render the corrected frame-extraction pseudocode (docx Gambar 3.3) as a
dark 'code window' PNG. Uses a column grid (1 data unit = 1 monospace char) so
text can never overflow the window. -> media_v2/."""
import re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parents[2] / "documents" / "media_v2" / "gambar_3_3_pseudocode_ekstraksi_frame.png"

BG, WIN, INK = "#e9e9ec", "#282c34", "#abb2bf"
GUTC, CMT, KW, FUN, STR, STEP = "#5c6370", "#7f848e", "#c678dd", "#61afef", "#98c379", "#61afef"

LINES = [
    ("input  : path_video, target_fps=5, max_frame=50, margin=0.3", "cmt"),
    ("output : frame wajah tersimpan sebagai .jpg", "cmt"),
    ("", ""),
    ("1.  buka video dengan OpenCV, ambil native_fps", "code"),
    ("2.  baca frame pertama; jika gagal / hitam (mean<3) -> lewati", "code"),
    ("3.  interval <- max(round(native_fps / target_fps), 1)", "code"),
    ("4.  frame_idx <- 0 , saved <- 0", "code"),
    ("5.  selama saved < max_frame:", "code"),
    ("6.      baca frame ke-frame_idx ; jika gagal -> break", "code"),
    ("7.      jika frame_idx mod interval == 0:", "code"),
    ("8.          bbox <- deteksi_wajah_MTCNN(frame, margin)", "code"),
    ("9.          jika bbox ada -> frame <- crop(frame, bbox)", "code"),
    ("10.         else          -> pakai frame penuh (fallback)", "code"),
    ("11.         tulis frame -> \"frame_{saved:06d}.jpg\"", "code"),
    ("12.         saved <- saved + 1", "code"),
    ("13.     frame_idx <- frame_idx + 1", "code"),
    ("14. tutup video", "code"),
]
KEYWORDS = ["selama", "jika", "else", "break", "mod", "tutup", "buka", "baca",
            "tulis", "pakai", "lewati", "ambil"]
FUNCS = ["deteksi_wajah_MTCNN", "crop", "round", "max", "OpenCV"]

FS = 14
CW = 0.602 * FS / 72.0       # inch per column so 1 data-x-unit == 1 char advance
RH = 0.34                    # inch per row

GUT_R, CODE = 4.4, 6.0       # gutter-number right edge col, code start col
maxlen = max(len(t) for t, _ in LINES)
NCOLS = CODE + maxlen + 3
NROWS = len(LINES) + 4.0

fig = plt.figure(figsize=(NCOLS * CW, NROWS * RH))
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, NCOLS); ax.set_ylim(0, NROWS); ax.axis("off")

ax.add_patch(FancyBboxPatch((0.7, 0.7), NCOLS - 1.4, NROWS - 1.4,
             boxstyle="round,pad=0.1,rounding_size=0.6", facecolor=WIN,
             edgecolor="#3a3f4b", linewidth=1.2, zorder=1))
hy = NROWS - 1.5
ax.scatter([2.0, 2.9, 3.8], [hy, hy, hy], s=100,
           c=["#ff5f56", "#ffbd2e", "#27c93f"], edgecolors="none", zorder=5)
ax.text(NCOLS / 2, hy, "Algoritma  —  Ekstraksi Frame dari Video", ha="center", va="center",
        color="#9aa0aa", fontsize=FS - 2, family="monospace", zorder=5)


def put(col, y, s, color, z=3, size=FS):
    ax.text(col, y, s, ha="left", va="center", color=color, fontsize=size, family="monospace", zorder=z)


y0 = NROWS - 3.0
for i, (txt, kind) in enumerate(LINES):
    y = y0 - i
    ax.text(GUT_R, y, str(i + 1), ha="right", va="center", color=GUTC, fontsize=FS - 3, family="monospace", zorder=3)
    if kind == "":
        continue
    put(CODE, y, txt, CMT if kind == "cmt" else INK)
    if kind != "code":
        continue
    m = re.match(r"\d+\.", txt)
    if m:
        put(CODE, y, m.group(0), STEP, z=4)
    for words, col in ((KEYWORDS, KW), (FUNCS, FUN)):
        for w in words:
            for mm in re.finditer(r"(?<![A-Za-z_])" + re.escape(w) + r"(?![A-Za-z_])", txt):
                put(CODE + mm.start(), y, w, col, z=4)
    for mm in re.finditer(r"\"[^\"]*\"", txt):
        put(CODE + mm.start(), y, mm.group(0), STR, z=4)

fig.savefig(OUT, dpi=200, facecolor=BG)
plt.close(fig)
print("saved ->", OUT.name, "| cols:", round(NCOLS), "rows:", NROWS)
