from __future__ import annotations
import os
import random
from dataclasses import dataclass
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


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


@dataclass
class DatasetConfig:
    manifest_path: Path
    fft_cache_root: Optional[Path]
    image_size: int
    max_frames_per_video: int
    mode: str  # spatial, freq, hybrid, early_fusion
    seed: int = 42
    train: bool = True


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
        self.spatial_transform = T.get_spatial_transform(image_size=self.image_size, train=self.train)
        self.fft_transform = T.get_fft_transform(image_size=self.image_size, train=self.train)

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
            fft_tensor = torch.nn.functional.interpolate(
                fft_tensor.unsqueeze(0), size=(self.image_size, self.image_size), mode="bilinear", align_corners=False
            ).squeeze(0)
        else:
            fft_tensor = None

        if self.mode == "spatial":
            return img_tensor, torch.tensor(label, dtype=torch.float32)
        if self.mode == "freq":
            fft_tensor = self.fft_transform(img.convert("L")) if fft_tensor is None else fft_tensor
            return fft_tensor, torch.tensor(label, dtype=torch.float32)
        if self.mode == "early_fusion":
            fft_tensor = self.fft_transform(img.convert("L")) if fft_tensor is None else fft_tensor
            fused = T.stack_rgb_fft(img_tensor, fft_tensor)
            return fused, torch.tensor(label, dtype=torch.float32)
        if self.mode == "hybrid":
            fft_tensor = self.fft_transform(img.convert("L")) if fft_tensor is None else fft_tensor
            return {"image": img_tensor, "fft": fft_tensor}, torch.tensor(label, dtype=torch.float32)
        raise ValueError(f"Unknown mode {self.mode}")
