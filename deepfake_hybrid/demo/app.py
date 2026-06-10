"""Gradio demo: deepfake detection — spatial vs. hybrid vs. frequency.

Reviewers upload a short video; we sample frames, MTCNN-crop faces, and show one
verdict per model side-by-side. The comparison is the point: it makes the thesis's
core finding visible — the proposed hybrid does NOT beat the spatial baseline.

Run locally:   python demo/app.py
On HF Spaces:  this file is the entrypoint (sdk: gradio); the platform sets the port.
"""
from pathlib import Path

import gradio as gr

import inference as inf

HERE = Path(__file__).resolve().parent
CKPT_DIR = HERE / "checkpoints"

# Load the three models once at startup (CPU).
LM = inf.load_models(CKPT_DIR)
DETECTOR, DETECTOR_ERR = inf.get_detector()

INTRO = """
# Deepfake Detection — Model Comparison Demo

Upload a short face video. Each model samples up to **{maxf} frames** (at {fps} fps),
MTCNN-crops the face, and averages its per-frame fake-probability into one verdict.

| Model | What it sees |
|---|---|
| **Spatial — XceptionNet** | RGB pixels only (the baseline) |
| **Hybrid — proposed** | RGB + FFT frequency map, fused |
| **Frequency-only** | FFT log-magnitude map only |

A clip is judged **FAKE** when its mean fake-probability is at or above that model's
decision threshold (tuned on the FaceForensics++ test set). The raw probability is
shown so you can read the model's confidence directly.
""".format(maxf=inf.MAX_FRAMES, fps=inf.TARGET_FPS)

CAVEAT = (
    "These models were trained on **FaceForensics++** face crops (n=750/class tier, seed 0). "
    "Clips from other sources are out-of-distribution and may be predicted unreliably. "
    "This is a research demo accompanying a thesis, not a production detector."
)


def _startup_warnings() -> str:
    msgs = []
    if DETECTOR is None:
        msgs.append(
            f"⚠️ **Face cropping is OFF** (MTCNN unavailable: {DETECTOR_ERR}). "
            "Predictions use full frames and will not match the trained distribution. "
            "Install `facenet-pytorch` to enable cropping."
        )
    if not LM.fft_stats_from_file:
        msgs.append("⚠️ " + LM.notes[-1] if LM.notes else "⚠️ FFT stats fallback in use.")
    return "\n\n".join(msgs)


def analyze(video_path):
    if not video_path:
        return [], "Please upload a video first."
    out = inf.predict_video(video_path, LM, DETECTOR)
    if not out["ok"]:
        return [], f"❌ {out['error']}"
    crop_note = (
        f"{out['faces_found']}/{out['frames']} frames had a detected face (cropped); "
        "the rest used the full frame."
        if out["cropping"]
        else f"{out['frames']} frames analyzed (face cropping OFF — full frames)."
    )
    info = f"**Analyzed {out['frames']} frames.** {crop_note}"
    return out["rows"], info


with gr.Blocks(title="Deepfake Detection Demo") as demo:
    gr.Markdown(INTRO)
    warn = _startup_warnings()
    if warn:
        gr.Markdown(warn)

    with gr.Row():
        with gr.Column(scale=1):
            video_in = gr.Video(label="Upload a face video", sources=["upload"])
            run_btn = gr.Button("Analyze", variant="primary")
        with gr.Column(scale=2):
            results = gr.Dataframe(
                headers=["Model", "Verdict", "Fake probability", "Decision threshold"],
                datatype=["str", "str", "str", "str"],
                label="Per-model verdicts",
                wrap=True,
                interactive=False,
            )
            info_md = gr.Markdown()

    gr.Markdown("---\n" + CAVEAT)

    run_btn.click(analyze, inputs=video_in, outputs=[results, info_md])
    video_in.upload(analyze, inputs=video_in, outputs=[results, info_md])


if __name__ == "__main__":
    demo.launch()
