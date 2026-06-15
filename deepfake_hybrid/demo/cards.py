"""Per-model verdict cards for the demo — pure stdlib (no gradio/torch).

`render_cards(results)` turns the structured output of `inference.predict_video`
into an HTML block of side-by-side cards: a REAL/FAKE badge, a fake-probability
confidence bar with the decision-threshold marked, and the raw numbers. Kept
gradio-free so it can be unit-tested on the repo's Python 3.9 venv.

`CARDS_CSS` is injected into the gradio Blocks; it also makes the cards wrap
to a single column on narrow (mobile) screens.
"""
from typing import List, Dict
from html import escape

CARDS_CSS = """
.df-cards { display:flex; flex-wrap:wrap; gap:14px; margin-top:4px; }
.df-card {
  flex:1 1 200px; min-width:180px; border-radius:14px; padding:16px 16px 14px;
  border:1px solid var(--border-color-primary, rgba(128,128,128,.25));
  background:var(--background-fill-secondary, rgba(128,128,128,.04));
}
.df-card-label { font-size:13px; font-weight:600; opacity:.85; margin-bottom:12px; min-height:34px; line-height:1.3; }
.df-badge { display:inline-block; font-size:17px; font-weight:800; letter-spacing:.02em;
  padding:5px 14px; border-radius:999px; margin-bottom:16px; }
.df-bar { position:relative; height:12px; border-radius:6px; background:rgba(128,128,128,.20); overflow:hidden; }
.df-bar-fill { position:absolute; left:0; top:0; bottom:0; }
.df-bar-thr { position:absolute; top:0; bottom:0; width:2px; background:var(--body-text-color, #111); opacity:.65; }
.df-nums { display:flex; justify-content:space-between; font-size:12px; margin-top:9px; opacity:.85; }
.df-nums b { font-variant-numeric:tabular-nums; }
.df-legend { font-size:11.5px; opacity:.6; margin-top:10px; }
.df-est { font-size:11px; color:#b45309; margin-top:6px; }
@media (max-width:640px){ .df-card{ flex:1 1 100%; } }
"""

_GREEN = "#16a34a"
_RED = "#dc2626"


def _clamp_pct(x: float) -> float:
    return max(0.0, min(100.0, x * 100.0))


def render_cards(results: List[Dict], fft_calibrated: bool = True) -> str:
    """results: list of {key,label,prob,threshold,is_fake}. Returns an HTML string."""
    if not results:
        return (
            '<div class="df-legend" style="opacity:.7;font-size:14px;">'
            "Upload a video and click <b>Analyze</b> to see each model’s verdict.</div>"
        )
    cards = []
    for r in results:
        fake = bool(r["is_fake"])
        accent = _RED if fake else _GREEN
        verdict = "FAKE" if fake else "REAL"
        emoji = "🔴" if fake else "🟢"
        fill = _clamp_pct(float(r["prob"]))
        thr = _clamp_pct(float(r["threshold"]))
        # freq/hybrid use the FFT branch; flag when running on estimated stats.
        est = (
            '<div class="df-est">⚠︎ FFT calibration estimated</div>'
            if (not fft_calibrated and r["key"] in ("freq", "hybrid"))
            else ""
        )
        cards.append(
            f'<div class="df-card">'
            f'<div class="df-card-label">{escape(str(r["label"]))}</div>'
            f'<div class="df-badge" style="color:{accent};background:{accent}1a;border:1px solid {accent}55;">'
            f'{emoji} {verdict}</div>'
            f'<div class="df-bar">'
            f'<div class="df-bar-fill" style="width:{fill:.1f}%;background:{accent};"></div>'
            f'<div class="df-bar-thr" style="left:{thr:.1f}%;" title="threshold {float(r["threshold"]):.3f}"></div>'
            f'</div>'
            f'<div class="df-nums"><span>fake-prob&nbsp;<b>{float(r["prob"]):.3f}</b></span>'
            f'<span>thr&nbsp;{float(r["threshold"]):.3f}</span></div>'
            f'{est}'
            f'</div>'
        )
    legend = (
        '<div class="df-legend">Bar = mean fake-probability across sampled frames; '
        "the vertical mark is each model’s decision threshold. Fill past the mark → FAKE.</div>"
    )
    return f'<div class="df-cards">{"".join(cards)}</div>{legend}'
