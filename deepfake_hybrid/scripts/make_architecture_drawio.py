"""
Emit editable draw.io (.drawio / mxGraph XML) versions of the BAB III diagrams,
matching the corrected PNGs. Open in app.diagrams.net or draw.io desktop.

Outputs to documents/media_v2/:
  gambar_3_4_flowchart_preprocessing.drawio
  gambar_3_8_freqcnn_architecture.drawio
  gambar_3_9_hybrid_twobranch.drawio
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[2] / "documents" / "media_v2"
OUT.mkdir(parents=True, exist_ok=True)

NAVY, BLUE, RED, PURPLE, GREEN, ORANGE = "#33475B", "#2980B9", "#E24A38", "#8E44AD", "#27AE60", "#F0932B"
TSP, TFR, TERM, INK = "#EAF1F8", "#FCECEA", "#EAE7DF", "#1C1C1A"

_ids = iter(range(1000, 100000))


def _label(title, meta=None, tc="#ffffff"):
    h = "<b>%s</b>" % escape(title)
    if meta:
        mc = "#5a5a54" if tc == "#1C1C1A" else "#e9eef4"
        h += "<br><span style=\"font-size:10px;color:%s\">%s</span>" % (mc, escape(meta))
    return escape(h, {'"': "&quot;"})


def node(cells, x, y, w, h, title, meta=None, fill=NAVY, tc="#ffffff", rounded=1, term=False):
    nid = "n%d" % next(_ids)
    if term:
        style = ("rounded=1;arcSize=50;whiteSpace=wrap;html=1;fillColor=%s;fontColor=%s;"
                 "strokeColor=%s;fontStyle=1;fontSize=15;" % (fill, tc, INK))
    else:
        style = ("rounded=%d;whiteSpace=wrap;html=1;fillColor=%s;fontColor=%s;strokeColor=%s;"
                 "fontSize=12;verticalAlign=middle;" % (rounded, fill, tc, INK))
    cells.append('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
                 '<mxGeometry x="%g" y="%g" width="%g" height="%g" as="geometry"/></mxCell>'
                 % (nid, _label(title, meta, tc), style, x, y, w, h))
    return nid


def edge(cells, src, dst, color=INK, ortho=True):
    eid = "e%d" % next(_ids)
    es = "edgeStyle=%s;rounded=0;" % ("orthogonalEdgeStyle" if ortho else "none")
    style = ("%shtml=1;strokeColor=%s;strokeWidth=2;endArrow=block;endFill=1;" % (es, color))
    cells.append('<mxCell id="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
                 '<mxGeometry relative="1" as="geometry"/></mxCell>' % (eid, style, src, dst))


def text(cells, x, y, w, s, color=INK, fs=12, bold=True):
    style = ("text;html=1;align=center;verticalAlign=middle;strokeColor=none;fillColor=none;"
             "fontColor=%s;fontSize=%d;%s" % (color, fs, "fontStyle=1;" if bold else ""))
    cells.append('<mxCell id="t%d" value="%s" style="%s" vertex="1" parent="1">'
                 '<mxGeometry x="%g" y="%g" width="%g" height="26" as="geometry"/></mxCell>'
                 % (next(_ids), escape(s), style, x, y, w))


def write(name, cells, w=1400, h=900):
    body = "\n        ".join(cells)
    xml = ('<mxfile host="app.diagrams.net">\n'
           '  <diagram name="%s" id="%s">\n'
           '    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" '
           'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
           'pageWidth="%d" pageHeight="%d" math="0" shadow="0">\n'
           '      <root>\n'
           '        <mxCell id="0"/>\n'
           '        <mxCell id="1" parent="0"/>\n'
           '        %s\n'
           '      </root>\n'
           '    </mxGraphModel>\n'
           '  </diagram>\n'
           '</mxfile>\n' % (name, name, w, h, body))
    (OUT / (name + ".drawio")).write_text(xml, encoding="utf-8")
    print("saved", name + ".drawio")


# ------------------------------------------------------------------ 3.8 FreqCNN
def freqcnn():
    c = []
    text(c, 300, 30, 1400, "Arsitektur FreqCNN (depth = 5, base_channels = 64, ~4,2 juta parameter)", fs=17)
    steps = [
        ("FFT Input", "(1, 224, 224)", NAVY), ("FreqBlock 1", "1→64 · 112×112", NAVY),
        ("FreqBlock 2", "64→128 · 56×56", NAVY), ("FreqBlock 3", "128→256 · 28×28", NAVY),
        ("FreqBlock 4", "256→512 · 14×14", NAVY), ("FreqBlock 5", "512→512 · 7×7", NAVY),
        ("Dropout2d", "(0,2)", ORANGE), ("GAP", "512→1", PURPLE),
        ("FC", "512→256 +ReLU", BLUE), ("Drop", "(0,3)", ORANGE),
        ("FC", "256→1", BLUE), ("Logit", None, GREEN),
    ]
    ids = []
    for i, (t, m, f) in enumerate(steps):
        ids.append(node(c, 40 + i * 168, 150, 150, 90, t, m, f))
    for a, b in zip(ids, ids[1:]):
        edge(c, a, b)
    write("gambar_3_8_freqcnn_architecture", c, w=2060, h=340)


# ------------------------------------------------------------------- 3.9 Hybrid
def hybrid():
    c = []
    text(c, 300, 20, 1200, "Arsitektur HybridTwoBranch (Late Fusion)", fs=18)
    text(c, 40, 90, 260, "Cabang Spasial", color=BLUE, fs=14)
    text(c, 40, 640, 300, "Cabang Frekuensi", color=RED, fs=14)
    bx = [40, 250, 470, 640, 850]
    bw = [150, 170, 120, 160, 90]
    sp = [("RGB Input", "(3, 224, 224)", NAVY), ("XceptionNet Backbone", "frozen 3 epoch", BLUE),
          ("2048-d", None, BLUE), ("Proj Linear+BN+ReLU", "2048→256", PURPLE), ("256", None, PURPLE)]
    fr = [("FFT Input", "(1, 224, 224)", NAVY), ("FreqCNN Backbone", "5 FreqBlocks", RED),
          ("512-d", None, RED), ("Proj Linear+BN+ReLU", "512→256", PURPLE), ("256", None, PURPLE)]
    sids, fids = [], []
    for x, w, (t, m, f) in zip(bx, bw, sp):
        sids.append(node(c, x, 140, w, 95, t, m, f))
    for x, w, (t, m, f) in zip(bx, bw, fr):
        fids.append(node(c, x, 540, w, 95, t, m, f))
    for a, b in zip(sids, sids[1:]):
        edge(c, a, b, BLUE)
    for a, b in zip(fids, fids[1:]):
        edge(c, a, b, RED)
    concat = node(c, 1000, 340, 120, 95, "Concat", "512-d", GREEN)
    se = node(c, 1160, 340, 120, 95, "SE Gate", "512→512", ORANGE)
    cls = node(c, 1320, 330, 160, 115, "Classifier", "Drop(0,5) · FC 512→128 · FC 128→1", NAVY)
    edge(c, sids[-1], concat)
    edge(c, fids[-1], concat)
    edge(c, concat, se)
    edge(c, se, cls)
    write("gambar_3_9_hybrid_twobranch", c, w=1520, h=680)


# --------------------------------------------------------------- 3.4 flowchart
def flowchart():
    c = []
    cx, W, H = 360, 320, 62
    x = cx - W / 2
    start = node(c, cx - 90, 20, 180, 56, "START", None, TERM, tc=INK, term=True)
    shared = [("Dataset Video", "FaceForensics++ (c23) & Celeb-DF v2"),
              ("Ekstraksi Frame", "5 FPS · maks. 50 frame / video"),
              ("Deteksi Wajah & Cropping", "MTCNN · margin 0,3 · fallback frame penuh"),
              ("Pembagian Dataset", "Train 70% / Val 15% / Test 15% · stratified per-video")]
    prev = start; y = 110
    sh_ids = []
    for t, m in shared:
        nid = node(c, x, y, W, H, t, m, "#ffffff", tc=INK)
        edge(c, prev, nid); prev = nid; sh_ids.append(nid); y += 92
    split = prev
    text(c, x - 40, y - 6, W + 80, "Setiap frame → dua representasi paralel", color="#5a5a54", fs=11, bold=False)

    # lanes
    lx, rx, LW = 60, 620, 300
    text(c, lx, y + 24, LW, "CABANG SPASIAL · RGB", color=BLUE, fs=11)
    text(c, rx, y + 24, LW, "CABANG FREKUENSI · FFT", color=RED, fs=11)
    ytop = y + 56

    def lane(lxx, steps, tint, ac):
        yy = ytop; ids = []
        for t, m in steps:
            ids.append(node(c, lxx, yy, LW, 60, t, m, tint, tc=INK))
            yy += 88
        for a, b in zip(ids, ids[1:]):
            edge(c, a, b, ac)
        return ids

    sp = lane(lx, [("Resize 224×224", None), ("Normalisasi ImageNet", "tetap 3-kanal warna"),
                   ("Augmentasi (pelatihan)", "ColorJitter · RRC · HFlip · RandErasing")], TSP, BLUE)
    fr = lane(rx, [("Konversi Grayscale", "Y=0,299R+0,587G+0,114B"), ("Resize 224×224", None),
                   ("FFT 2D + FFTShift", "np.fft.fft2 → fftshift"),
                   ("Magnitude & High-Pass", "|F(u,v)| × Gaussian HPF (β=0,15)"),
                   ("Log Scaling", "log(1 + |F(u,v)|)"), ("Cache .npy + Z-Score", "μ,σ per-dataset"),
                   ("Augmentasi (pelatihan)", "Noise σ=0,05 · Spectral band mask")], TFR, RED)
    edge(c, split, sp[0], BLUE)
    edge(c, split, fr[0], RED)

    ymerge = ytop + 7 * 88 + 20
    train = node(c, x, ymerge, W, H, "Pelatihan Model",
                 "Spatial / Freq / Hybrid · Hybrid = late fusion (proyeksi→concat→SE gating→classifier)",
                 "#ffffff", tc=INK)
    edge(c, sp[-1], train, BLUE)
    edge(c, fr[-1], train, RED)
    prev = train; y = ymerge + 92
    for t, m in [("Validasi → Checkpoint Terbaik", "seleksi & early stopping by AUC validasi"),
                 ("Evaluasi (In-dataset & Cross-dataset)", "accuracy, precision, recall, F1, AUC"),
                 ("Tabel Hasil → Analisis", None)]:
        nid = node(c, x, y, W, H, t, m, "#ffffff", tc=INK)
        edge(c, prev, nid); prev = nid; y += 92
    stop = node(c, cx - 90, y, 180, 56, "STOP", None, TERM, tc=INK, term=True)
    edge(c, prev, stop)
    write("gambar_3_4_flowchart_preprocessing", c, w=1000, h=int(y + 120))


if __name__ == "__main__":
    freqcnn(); hybrid(); flowchart()
    print("-> written to", OUT)
