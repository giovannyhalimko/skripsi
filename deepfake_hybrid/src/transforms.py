from typing import Tuple
import torch
from torchvision import transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# Empirical stats for [0,1]-normalized FFT log-magnitude
FFT_MEAN = [0.5]
FFT_STD = [0.25]


def get_spatial_transform(image_size: int = 224, train: bool = True):
    if train:
        t = transforms.Compose([
            transforms.Resize((image_size + 32, image_size + 32)),
            transforms.RandomResizedCrop(image_size, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.05),
            transforms.RandomRotation(10),
            transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    else:
        t = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    return t


def get_fft_transform(image_size: int = 224, train: bool = True):
    # For FFT magnitude inputs (1 channel)
    if train:
        t = transforms.Compose([
            transforms.Resize((image_size + 32, image_size + 32)),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(FFT_MEAN, FFT_STD),
        ])
    else:
        t = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(FFT_MEAN, FFT_STD),
        ])
    return t


def normalize_fft_tensor(fft_tensor: torch.Tensor) -> torch.Tensor:
    """Normalize a raw FFT tensor (already [0,1]) with FFT mean/std.
    Used for cached FFT that bypasses get_fft_transform."""
    mean = torch.tensor(FFT_MEAN).view(-1, 1, 1)
    std = torch.tensor(FFT_STD).view(-1, 1, 1)
    return (fft_tensor - mean) / std


def stack_rgb_fft(rgb: torch.Tensor, fft: torch.Tensor) -> torch.Tensor:
    # rgb: (3,H,W), fft: (1,H,W)
    return torch.cat([rgb, fft], dim=0)
