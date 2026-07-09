"""Render a draw.io (.drawio) file to PNG via matplotlib (preview / faithful-enough).
Usage:  python scripts/render_flowchart_drawio.py <file.drawio> [<file2.drawio> ...]
Default: renders gambar_3_4 and gambar_3_8 in documents/media_v2/.
Shapes: parallelogram (data), terminator/stadium, rounded-rect (process), text label.
"""
import re, html, sys
import xml.etree.ElementTree as ET
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch, Ellipse

MEDIA = Path(__file__).resolve().parents[2] / "documents" / "media_v2"


def unesc(s):
    return html.unescape(html.unescape(s))


def label(v):
    s = unesc(v)
    m = re.search(r"<div[^>]*>(.*?)</div>", s, re.S)
    meta = re.sub("<[^>]+>", "", m.group(1)).strip() if m else ""
    title = re.sub(r"<div[^>]*>.*?</div>", "", s, flags=re.S)
    title = re.sub("<[^>]+>", "", title).strip()
    return title, meta


def render(path):
    path = Path(path)
    xml = path.read_text(encoding="utf-8")
    root = ET.fromstring(xml)
    verts, edges = {}, []
    for cell in root.iter("mxCell"):
        cid = cell.get("id", ""); style = cell.get("style") or ""; val = cell.get("value") or ""
        geo = cell.find("mxGeometry")
        if cell.get("vertex") == "1" and geo is not None:
            verts[cid] = dict(x=float(geo.get("x", 0)), y=float(geo.get("y", 0)),
                              w=float(geo.get("width", 0)), h=float(geo.get("height", 0)),
                              style=style, val=val)
        elif cell.get("edge") == "1":
            pts, sp, tp = [], None, None
            if geo is not None:
                arr = geo.find("Array")
                if arr is not None:
                    pts = [(float(p.get("x")), float(p.get("y"))) for p in arr.findall("mxPoint")]
                for p in geo.findall("mxPoint"):
                    if p.get("as") == "sourcePoint": sp = (float(p.get("x")), float(p.get("y")))
                    elif p.get("as") == "targetPoint": tp = (float(p.get("x")), float(p.get("y")))
            col = (re.search(r"strokeColor=(#[0-9A-Fa-f]{6})", style) or [None, "#1C1C1A"])[1]
            edges.append(dict(src=cell.get("source"), tgt=cell.get("target"), pts=pts, sp=sp, tp=tp, col=col))

    maxY = max(v["y"] + v["h"] for v in verts.values())
    minX = min(v["x"] for v in verts.values())

    def T(x, y):
        return x, maxY - y

    def center(v): return v["x"] + v["w"] / 2, v["y"] + v["h"] / 2

    def conn(v, toward):
        cx, cy = center(v)
        dx, dy = toward[0] - cx, toward[1] - cy
        if abs(dx) >= abs(dy):
            return (v["x"] + v["w"] if dx > 0 else v["x"], cy)
        return (cx, v["y"] + v["h"] if dy > 0 else v["y"])

    W = max(v["x"] + v["w"] for v in verts.values()) - minX
    Ht = maxY - min(v["y"] for v in verts.values())
    fig, ax = plt.subplots(figsize=(min(24, W / 90), max(3, Ht / 90 + 1)))

    for e in edges:
        seq = []
        if e["src"] in verts:
            nxt = e["pts"][0] if e["pts"] else (center(verts[e["tgt"]]) if e["tgt"] in verts else e["tp"])
            if nxt: seq.append(conn(verts[e["src"]], nxt))
        elif e["sp"]:
            seq.append(e["sp"])
        seq += e["pts"]
        if e["tgt"] in verts:
            prv = seq[-1] if seq else center(verts[e["tgt"]])
            seq.append(conn(verts[e["tgt"]], prv))
        elif e["tp"]:
            seq.append(e["tp"])
        seq = [T(*p) for p in seq]
        for i in range(len(seq) - 2):
            ax.plot([seq[i][0], seq[i+1][0]], [seq[i][1], seq[i+1][1]], color=e["col"], lw=1.4, zorder=1)
        if len(seq) >= 2:
            ax.add_patch(FancyArrowPatch(seq[-2], seq[-1], arrowstyle="-|>", mutation_scale=11,
                         color=e["col"], lw=1.4, zorder=1, shrinkA=0, shrinkB=0))

    for cid, v in verts.items():
        st = v["style"]
        fc = (re.search(r"fillColor=(#[0-9A-Fa-f]{6})", st) or [None, "#ffffff"])[1]
        ec = (re.search(r"strokeColor=(#[0-9A-Fa-f]{6})", st) or [None, "#1C1C1A"])[1]
        if "text;" in st:
            title, _ = label(v["val"])
            fcol = (re.search(r"fontColor=(#[0-9A-Fa-f]{6})", st) or [None, "#1C1C1A"])[1]
            fsz = float((re.search(r"fontSize=(\d+)", st) or [None, "11"])[1])
            algn = "center" if "align=center" in st else "left"
            tx = v["x"] + v["w"] / 2 if algn == "center" else v["x"]
            ax.text(*T(tx, v["y"] + v["h"] / 2), title, ha=algn, va="center",
                    color=fcol, fontsize=fsz * 0.72, fontweight="bold", zorder=3)
            continue
        x0, y0 = T(v["x"], v["y"] + v["h"])
        if "terminator" in st:
            ax.add_patch(FancyBboxPatch((x0, y0), v["w"], v["h"], boxstyle=f"round,pad=0,rounding_size={v['h']/2}",
                         facecolor=fc, edgecolor=ec, linewidth=2, zorder=2))
        elif "parallelogram" in st:
            s = 0.14 * v["w"]
            P = [(v["x"] + s, v["y"]), (v["x"] + v["w"], v["y"]),
                 (v["x"] + v["w"] - s, v["y"] + v["h"]), (v["x"], v["y"] + v["h"])]
            ax.add_patch(Polygon([T(*p) for p in P], closed=True, facecolor=fc, edgecolor=ec, linewidth=2, zorder=2))
        elif "ellipse" in st:
            ax.add_patch(Ellipse(T(*center(v)), v["w"], v["h"], facecolor=fc, edgecolor=ec, linewidth=2, zorder=2))
        else:
            ax.add_patch(FancyBboxPatch((x0, y0), v["w"], v["h"], boxstyle="round,pad=0,rounding_size=5",
                         facecolor=fc, edgecolor=ec, linewidth=2, zorder=2))
        title, meta = label(v["val"])
        cx, cy = T(*center(v))
        if meta:
            ax.text(cx, cy + v["h"] * 0.14, title, ha="center", va="center", fontsize=8.6, fontweight="bold", zorder=3, color="#1C1C1A")
            ax.text(cx, cy - v["h"] * 0.22, meta, ha="center", va="center", fontsize=6.6, zorder=3, color="#555")
        else:
            tfs = 16 if "ellipse" in st else 8.6
            ax.text(cx, cy, title, ha="center", va="center", fontsize=tfs, fontweight="bold", zorder=3, color="#1C1C1A")

    ax.set_xlim(minX - 20, max(v["x"] + v["w"] for v in verts.values()) + 20)
    ax.set_ylim(-10, maxY + 20)
    ax.set_aspect("equal"); ax.axis("off")
    out = path.with_suffix(".png")
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("rendered ->", out.name)


if __name__ == "__main__":
    files = sys.argv[1:] or [MEDIA / "gambar_3_4_flowchart_preprocessing.drawio",
                             MEDIA / "gambar_3_8_freqcnn_architecture.drawio"]
    for f in files:
        render(f)
