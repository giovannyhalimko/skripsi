from pathlib import Path
from typing import Tuple
import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F


def _highpass_mask(size: int, cutoff: float = 0.05) -> np.ndarray:
    """Gaussian high-pass mask to attenuate low-frequency center of FFT.

    cutoff is fraction of image size (0.05 = 5% radius suppressed).
    """
    cy, cx = size // 2, size // 2
    Y, X = np.ogrid[:size, :size]
    dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    sigma = cutoff * size
    mask = 1.0 - np.exp(-(dist ** 2) / (2 * sigma ** 2))
    return mask.astype(np.float32)


def image_to_fft_logmag(img: Image.Image, size: int = 224, highpass: bool = True) -> np.ndarray:
    # Convert to grayscale
    img = img.convert("L")
    img = img.resize((size, size))
    arr = np.asarray(img).astype(np.float32)
    fft = np.fft.fft2(arr)
    fft_shift = np.fft.fftshift(fft)
    magnitude = np.abs(fft_shift)
    if highpass:
        magnitude = magnitude * _highpass_mask(size)
    logmag = np.log1p(magnitude)
    return logmag.astype(np.float32)


def _highpass_mask_torch(size: int, cutoff: float = 0.05, device=None) -> torch.Tensor:
    """Torch version of Gaussian high-pass mask."""
    cy, cx = size // 2, size // 2
    y = torch.arange(size, device=device).float()
    x = torch.arange(size, device=device).float()
    Y, X = torch.meshgrid(y, x, indexing="ij")
    dist = torch.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    sigma = cutoff * size
    mask = 1.0 - torch.exp(-(dist ** 2) / (2 * sigma ** 2))
    return mask.unsqueeze(0)  # (1, H, W)


def tensor_fft_logmag(img_tensor: torch.Tensor, highpass: bool = True) -> torch.Tensor:
    # img_tensor: (C,H,W) in [0,1]
    gray = torch.mean(img_tensor, dim=0, keepdim=True)  # (1,H,W)
    fft = torch.fft.fft2(gray)
    fft_shift = torch.fft.fftshift(fft)
    magnitude = torch.abs(fft_shift)
    if highpass:
        magnitude = magnitude * _highpass_mask_torch(gray.shape[-1], device=gray.device)
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
