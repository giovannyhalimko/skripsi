from __future__ import annotations
import json
import logging
import os
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import numpy as np
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset

# Use absolute imports so the module works when src is added to sys.path
import fft_utils
import transforms as T
import torchvision.transforms.functional as TF


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

# Fallback FFT normalization constants used when fft_stats.json is missing.
# Run compute_fft_cache.py to generate the correct per-dataset stats file.
_FFT_MEAN_FALLBACK = 5.0
_FFT_STD_FALLBACK = 3.0


def load_fft_stats(fft_cache_root: Path) -> Tuple[float, float]:
    """Load FFT normalization stats from fft_stats.json in the cache root.

    Falls back to hardcoded defaults with a warning if the file is missing.
    """
    stats_path = fft_cache_root / "fft_stats.json"
    if stats_path.exists():
        with open(stats_path) as f:
            stats = json.load(f)
        return float(stats["mean"]), float(stats["std"])
    logging.warning(
        f"fft_stats.json not found at {stats_path}. "
        f"Using fallback mean={_FFT_MEAN_FALLBACK}, std={_FFT_STD_FALLBACK}. "
        "Run compute_fft_cache.py to generate correct stats."
    )
    return _FFT_MEAN_FALLBACK, _FFT_STD_FALLBACK


@dataclass
class DatasetConfig:
    manifest_path: Path
    fft_cache_root: Optional[Path]
    image_size: int
    max_frames_per_video: int
    mode: str  # spatial, freq, hybrid, early_fusion
    seed: int = 42
    train: bool = True
    fft_noise_sigma: float = 0.05


class DeepfakeDataset(Dataset):
    def __init__(self, cfg: DatasetConfig):
        self.cfg = cfg
        self.manifest = pd.read_csv(cfg.manifest_path)
        required_cols = {"video_id", "label", "frames_dir"}
        if not required_cols.issubset(set(self.manifest.columns)):
            raise ValueError(f"Manifest must contain columns {required_cols}")

        self.items: List[Tuple[str, int, str]] = []  # (frame_path, label, video_id)
        rng = random.Random(cfg.seed)
        for _, row in self.manifest.iterrows():
            video_id = str(row["video_id"])
            label = int(row["label"])
            frames_dir = Path(row["frames_dir"])
            if not frames_dir.exists():
                raise FileNotFoundError(f"Frames dir not found: {frames_dir}")
            frame_files = [p for p in sorted(frames_dir.iterdir()) if p.suffix.lower() in IMAGE_EXTS]
            if len(frame_files) == 0:
                continue
            max_frames = cfg.max_frames_per_video if cfg.max_frames_per_video > 0 else len(frame_files)
            if len(frame_files) > max_frames:
                frame_files = rng.sample(frame_files, k=max_frames)
            for fp in frame_files:
                self.items.append((str(fp), label, video_id))

        self.train = cfg.train
        self.mode = cfg.mode
        self.image_size = cfg.image_size
        self.fft_cache_root = Path(cfg.fft_cache_root) if cfg.fft_cache_root else None
        # Load per-dataset FFT normalization stats from cache
        if self.fft_cache_root is not None and cfg.mode in {"freq", "hybrid", "early_fusion"}:
            self.fft_mean, self.fft_std = load_fft_stats(self.fft_cache_root)
        else:
            self.fft_mean, self.fft_std = _FFT_MEAN_FALLBACK, _FFT_STD_FALLBACK
        # Hybrid mode: disable hflip here and apply it manually to both branches together
        include_hflip = not (cfg.mode == "hybrid" and cfg.train)
        self.spatial_transform = T.get_spatial_transform(
            image_size=self.image_size, train=self.train, include_hflip=include_hflip
        )

    def __len__(self):
        return len(self.items)

    def _load_image(self, path: str) -> Image.Image:
        return Image.open(path).convert("RGB")

    def _load_fft(self, frame_path: Path) -> torch.Tensor:
        if self.fft_cache_root is not None:
            rel = frame_path.parent.name  # video_id
            fft_path = self.fft_cache_root / rel / (frame_path.stem + ".npy")
            if fft_path.exists():
                arr = np.load(fft_path)
                return torch.tensor(arr, dtype=torch.float32).unsqueeze(0)
        # fallback compute
        img = self._load_image(str(frame_path))
        logmag = fft_utils.image_to_fft_logmag(img, size=self.image_size)
        return torch.tensor(logmag, dtype=torch.float32).unsqueeze(0)

    def __getitem__(self, idx: int):
        frame_path, label, video_id = self.items[idx]
        img = self._load_image(frame_path)
        if self.mode in {"spatial", "hybrid", "early_fusion"}:
            img_tensor = self.spatial_transform(img)
        else:
            img_tensor = None

        if self.mode in {"freq", "hybrid", "early_fusion"}:
            fft_tensor = self._load_fft(Path(frame_path))
            # Normalize log-magnitude using dataset-level statistics
            fft_tensor = (fft_tensor - self.fft_mean) / self.fft_std
            # FFT augmentation: add Gaussian noise during training to prevent memorization
            if self.train and self.cfg.fft_noise_sigma > 0:
                fft_tensor = fft_tensor + torch.randn_like(fft_tensor) * self.cfg.fft_noise_sigma
            # Spectral masking: randomly zero a frequency band to prevent reliance on any single band
            if self.train and random.random() < 0.05:
                _, h, w = fft_tensor.shape
                band_width = random.randint(1, max(h // 16, 2))
                start = random.randint(0, h - band_width)
                if random.random() < 0.5:
                    fft_tensor[:, start:start + band_width, :] = 0.0
                else:
                    fft_tensor[:, :, start:start + band_width] = 0.0
        else:
            fft_tensor = None

        if self.mode == "spatial":
            return img_tensor, torch.tensor(label, dtype=torch.float32)
        if self.mode == "freq":
            return fft_tensor, torch.tensor(label, dtype=torch.float32)
        if self.mode == "early_fusion":
            fused = T.stack_rgb_fft(img_tensor, fft_tensor)
            return fused, torch.tensor(label, dtype=torch.float32)
        if self.mode == "hybrid":
            # Apply consistent random horizontal flip to both branches
            if self.train and random.random() < 0.5:
                img_tensor = TF.hflip(img_tensor)
                fft_tensor = torch.flip(fft_tensor, dims=[-1])
            return {"image": img_tensor, "fft": fft_tensor}, torch.tensor(label, dtype=torch.float32)
        raise ValueError(f"Unknown mode {self.mode}")
