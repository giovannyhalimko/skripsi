"""Core inference for the deepfake-detection demo.

Loads the three thesis models (spatial / hybrid / freq), decodes an uploaded
video into MTCNN-cropped frames, and aggregates per-frame fake-probabilities
into one verdict per model. Preprocessing mirrors training exactly:

  - frames sampled at TARGET_FPS, MTCNN-cropped (margin 0.3), full-frame fallback
  - RGB: Resize 224 -> ToTensor -> ImageNet norm  (src/transforms.get_spatial_transform)
  - FFT: image_to_fft_logmag(highpass) -> (x - mean) / std  (src/fft_utils + fft_stats.json)

This module only needs torch/timm/numpy/PIL/cv2 + the bundled src/, so it can be
imported and exercised without gradio. facenet-pytorch (MTCNN) is imported lazily
and degrades to no-crop if unavailable. Heavy work (model loading) happens once via
load_models().
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
import torch
from PIL import Image

# --- make the bundled (Space) or repo (local dev) src/ importable -------------
HERE = Path(__file__).resolve().parent
for _cand in (HERE / "src", HERE.parent / "src"):
    if (_cand / "models").exists():
        sys.path.insert(0, str(_cand))
        break

from face_utils import create_face_detector, detect_face_bbox, crop_face  # noqa: E402
from fft_utils import image_to_fft_logmag  # noqa: E402
from transforms import get_spatial_transform  # noqa: E402
from models.spatial_xception import build_xception  # noqa: E402
from models.freq_cnn import FreqCNN  # noqa: E402
from models.hybrid_fusion import HybridTwoBranch  # noqa: E402

DEVICE = "cpu"
TARGET_FPS = 5          # match training (config.yaml fps)
MAX_FRAMES = 16         # cap to keep latency sane on a free CPU Space
FACE_MARGIN = 0.3       # match colab_run.ipynb FACE_CROP
DEFAULT_FFT_MEAN = 5.0  # src/deepfake_data fallback when fft_stats.json is absent
DEFAULT_FFT_STD = 3.0

# (model_key, human label) shown top-to-bottom in the results table.
MODELS_SPEC: List[Tuple[str, str]] = [
    ("spatial", "Spatial — XceptionNet (baseline)"),
    ("hybrid", "Hybrid — spatial + frequency (proposed)"),
    ("freq", "Frequency-only — FFT + CNN"),
]


def _build_model(model_type: str, cfg: dict) -> torch.nn.Module:
    """Mirror of scripts/eval.py:select_model, with pretrained=False.

    The checkpoint overwrites every weight, so we skip the timm ImageNet
    download (offline-safe, faster startup). freq params come from the
    checkpoint's embedded config, not the drifted config.yaml.
    """
    fd = int(cfg.get("freq_depth", 5))
    fb = int(cfg.get("freq_base_channels", 64))
    if model_type == "spatial":
        return build_xception(num_classes=1, in_chans=3, pretrained=False)
    if model_type == "freq":
        return FreqCNN(num_classes=1, depth=fd, base_channels=fb)
    if model_type == "hybrid":
        return HybridTwoBranch(pretrained=False, freq_depth=fd, freq_base_channels=fb)
    raise ValueError(f"Unknown model_type {model_type}")


@dataclass
class LoadedModels:
    models: Dict[str, torch.nn.Module]
    thresholds: Dict[str, float]
    image_size: int = 224
    fft_mean: float = DEFAULT_FFT_MEAN
    fft_std: float = DEFAULT_FFT_STD
    fft_stats_from_file: bool = False
    spatial_tf: object = field(default=None)
    notes: List[str] = field(default_factory=list)


def load_models(ckpt_dir: Path) -> LoadedModels:
    """Load spatial/hybrid/freq checkpoints from ckpt_dir once, on CPU.

    Expects: {key}.pt for each key in MODELS_SPEC, optional {key}_threshold.json
    (falls back to 0.5), and optional fft_stats.json (falls back to 5.0/3.0).
    """
    ckpt_dir = Path(ckpt_dir)
    models: Dict[str, torch.nn.Module] = {}
    thresholds: Dict[str, float] = {}
    notes: List[str] = []
    image_size = 224

    for key, _ in MODELS_SPEC:
        ckpt_path = ckpt_dir / f"{key}.pt"
        if not ckpt_path.exists():
            raise FileNotFoundError(f"Missing checkpoint: {ckpt_path}")
        # weights_only=False: these are our own trusted checkpoints and carry a
        # plain-dict 'config'. Avoids torch>=2.6 weights_only surprises.
        ckpt = torch.load(ckpt_path, map_location=DEVICE, weights_only=False)
        cfg = ckpt.get("config", {}) if isinstance(ckpt, dict) else {}
        image_size = int(cfg.get("image_size", image_size))
        model = _build_model(key, cfg)
        state = ckpt["state_dict"] if isinstance(ckpt, dict) and "state_dict" in ckpt else ckpt
        model.load_state_dict(state)
        model.to(DEVICE).eval()
        models[key] = model

        thr_path = ckpt_dir / f"{key}_threshold.json"
        if thr_path.exists():
            thresholds[key] = float(json.loads(thr_path.read_text())["threshold"])
        else:
            thresholds[key] = 0.5
            notes.append(f"{key}: no threshold file, using 0.5")

    # FFT normalization stats (needed by hybrid + freq).
    fft_mean, fft_std, from_file = DEFAULT_FFT_MEAN, DEFAULT_FFT_STD, False
    stats_path = ckpt_dir / "fft_stats.json"
    if stats_path.exists():
        s = json.loads(stats_path.read_text())
        fft_mean, fft_std, from_file = float(s["mean"]), float(s["std"]), True
    else:
        notes.append(
            "fft_stats.json missing — using fallback mean=5.0/std=3.0; the FREQ and "
            "HYBRID branches may be miscalibrated. Copy outputs/fft_cache/FFPP/fft_stats.json "
            "from the training machine into checkpoints/ to fix. (Spatial is unaffected.)"
        )

    return LoadedModels(
        models=models,
        thresholds=thresholds,
        image_size=image_size,
        fft_mean=fft_mean,
        fft_std=fft_std,
        fft_stats_from_file=from_file,
        spatial_tf=get_spatial_transform(image_size=image_size, train=False),
        notes=notes,
    )


def get_detector():
    """Create the MTCNN detector, or return (None, reason) if unavailable."""
    try:
        return create_face_detector(DEVICE), None
    except Exception as e:  # facenet-pytorch missing or failed to init
        return None, f"{type(e).__name__}: {e}"


def extract_frames(
    video_path: str,
    detector,
    max_frames: int = MAX_FRAMES,
    target_fps: int = TARGET_FPS,
) -> Tuple[List[np.ndarray], int, int]:
    """Sample frames at target_fps, MTCNN-crop each (margin 0.3, full-frame fallback).

    Returns (cropped_bgr_frames, faces_found, frames_sampled).
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return [], 0, 0
    vfps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    interval = max(int(round(vfps / target_fps)), 1) if vfps > 0 else 1

    frames: List[np.ndarray] = []
    faces_found = 0
    idx = 0
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            if detector is not None:
                bbox = detect_face_bbox(frame, detector, margin=FACE_MARGIN)
                if bbox is not None:
                    frame = crop_face(frame, bbox)
                    faces_found += 1
            frames.append(frame)
        idx += 1
    cap.release()
    return frames, faces_found, len(frames)


def _preprocess(frame_bgr: np.ndarray, lm: LoadedModels) -> Tuple[torch.Tensor, torch.Tensor]:
    """One BGR frame -> (rgb_tensor (3,H,W), fft_tensor (1,H,W)), computed once."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    rgb_t = lm.spatial_tf(pil)
    logmag = image_to_fft_logmag(pil, size=lm.image_size, highpass=True)
    fft_t = (torch.from_numpy(logmag).unsqueeze(0) - lm.fft_mean) / lm.fft_std
    return rgb_t, fft_t.float()


@torch.no_grad()
def predict_video(video_path: str, lm: LoadedModels, detector) -> dict:
    """Run all three models on a video. Returns rows + diagnostic info."""
    frames, faces_found, sampled = extract_frames(video_path, detector)
    if sampled == 0:
        return {"ok": False, "error": "Could not read any frames from the video.", "rows": []}

    rgb_list, fft_list = zip(*(_preprocess(f, lm) for f in frames))
    rgb_batch = torch.stack(rgb_list).to(DEVICE)
    fft_batch = torch.stack(fft_list).to(DEVICE)

    rows = []
    for key, label in MODELS_SPEC:
        model = lm.models[key]
        if key == "spatial":
            logits = model(rgb_batch).view(-1)
        elif key == "freq":
            logits = model(fft_batch).view(-1)
        else:  # hybrid
            logits = model(rgb_batch, fft_batch).view(-1)
        prob = float(torch.sigmoid(logits).mean().cpu())
        thr = lm.thresholds[key]
        verdict = "🔴 FAKE" if prob >= thr else "🟢 REAL"
        rows.append([label, verdict, f"{prob:.3f}", f"{thr:.3f}"])

    return {
        "ok": True,
        "rows": rows,
        "frames": sampled,
        "faces_found": faces_found,
        "cropping": detector is not None,
    }
