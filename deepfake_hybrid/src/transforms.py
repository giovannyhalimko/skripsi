from typing import Tuple
import torch
from torchvision import transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_spatial_transform(image_size: int = 224, train: bool = True):
    if train:
        t = transforms.Compose([
            transforms.Resize((image_size + 32, image_size + 32)),
            transforms.RandomResizedCrop(image_size, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
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
        ])
    else:
        t = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
        ])
    return t


def stack_rgb_fft(rgb: torch.Tensor, fft: torch.Tensor) -> torch.Tensor:
    # rgb: (3,H,W), fft: (1,H,W)
    return torch.cat([rgb, fft], dim=0)
