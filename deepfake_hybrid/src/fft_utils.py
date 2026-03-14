from pathlib import Path
from typing import Tuple
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F


def image_to_fft_logmag(img: Image.Image, size: int = 224) -> np.ndarray:
    # Convert to grayscale
    img = img.convert("L")
    img = img.resize((size, size))
    arr = np.asarray(img).astype(np.float32)
    fft = np.fft.fft2(arr)
    fft_shift = np.fft.fftshift(fft)
    magnitude = np.abs(fft_shift)
    logmag = np.log1p(magnitude)
    return logmag.astype(np.float32)


def tensor_fft_logmag(img_tensor: torch.Tensor) -> torch.Tensor:
    # img_tensor: (C,H,W) in [0,1]
    gray = torch.mean(img_tensor, dim=0, keepdim=True)  # (1,H,W)
    fft = torch.fft.fft2(gray)
    fft_shift = torch.fft.fftshift(fft)
    magnitude = torch.abs(fft_shift)
    logmag = torch.log1p(magnitude)
    return logmag


def save_fft_cache(img_path: Path, out_path: Path, size: int = 224) -> None:
    img = Image.open(img_path).convert("RGB")
    logmag = image_to_fft_logmag(img, size=size)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(out_path, logmag)


def load_fft_cache(path: Path) -> np.ndarray:
    return np.load(path)


def pad_to_size(tensor: torch.Tensor, size: int) -> torch.Tensor:
    _, h, w = tensor.shape
    dh = max(0, size - h)
    dw = max(0, size - w)
    pad = (dw // 2, dw - dw // 2, dh // 2, dh - dh // 2)
    if dh > 0 or dw > 0:
        tensor = F.pad(tensor, pad, mode="reflect")
    return tensor
