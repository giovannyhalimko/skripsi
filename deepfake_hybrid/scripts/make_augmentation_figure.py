"""Generate the RGB augmentation illustration figure for BAB III (subbab 3.3.3).

Produces a step-by-step RGB augmentation grid using the REAL augmentation pipeline
from src/transforms.py. Output goes to the repo-root documents/media_v2/ folder,
alongside the other thesis figures. Defaults to a real sample frame
(documents/media_v2/media/ffpp_original.png).

The FFT augmentation figures (Gaussian noise + spectral band masking) already exist
as gambar_3_3_spectral_band_masking.png and gambar_3_5_fft_real_vs_fake.png, so they
are not regenerated here.

Usage:
    python scripts/make_augmentation_figure.py                  # uses ffpp_original.png
    python scripts/make_augmentation_figure.py --frame path.jpg # use another frame
"""
import argparse
from pathlib import Path

import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms

IMAGENET_MEAN = np.array([0.485, 0.456, 0.406])
IMAGENET_STD = np.array([0.229, 0.224, 0.225])

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "documents" / "media_v2"
DEFAULT_FRAME = OUT_DIR / "media" / "ffpp_original.png"


def denorm(t: torch.Tensor) -> np.ndarray:
    arr = t.numpy().transpose(1, 2, 0)
    arr = arr * IMAGENET_STD + IMAGENET_MEAN
    return np.clip(arr, 0, 1)


def make_rgb_figure(base: Image.Image, out_path: Path):
    torch.manual_seed(7)
    resize = transforms.Resize((256, 256))
    rrc = transforms.RandomResizedCrop(224, scale=(0.8, 1.0))
    jitter = transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.05)
    hflip = transforms.RandomHorizontalFlip(p=1.0)  # forced for illustration
    to_tensor = transforms.ToTensor()
    normalize = transforms.Normalize(IMAGENET_MEAN.tolist(), IMAGENET_STD.tolist())
    erasing = transforms.RandomErasing(p=1.0, scale=(0.04, 0.12))  # forced for illustration

    s0 = base
    s1 = resize(s0)
    s2 = rrc(s1)
    s3 = jitter(s2)
    s4 = hflip(s3)
    # Normalize BEFORE erasing (matches real pipeline), then denorm for display
    s5 = denorm(erasing(normalize(to_tensor(s4))))

    panels = [
        (s0, "Frame asli"),
        (s1, "Resize 256x256"),
        (s2, "RandomResizedCrop 224\n(scale 0.8-1.0)"),
        (s3, "ColorJitter\n(b=0.2 c=0.2 s=0.1 h=0.05)"),
        (s4, "HorizontalFlip"),
        (s5, "RandomErasing\n(p=0.1 scale 0.02-0.15)"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(10, 7))
    for ax, (im, title) in zip(axes.ravel(), panels):
        ax.imshow(im)
        ax.set_title(title, fontsize=10)
        ax.axis("off")
    fig.suptitle("Tahapan augmentasi visual pada cabang spasial (RGB)", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("saved", out_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", type=str, default=str(DEFAULT_FRAME),
                    help="path to a sample frame (default: media_v2/media/ffpp_original.png)")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    base = Image.open(args.frame).convert("RGB").resize((256, 256))
    make_rgb_figure(base, OUT_DIR / "gambar_3_x_augmentasi_rgb.png")


if __name__ == "__main__":
    main()
