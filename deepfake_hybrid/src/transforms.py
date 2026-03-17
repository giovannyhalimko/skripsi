from typing import Tuple
import torch
from torchvision import transforms


IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def get_spatial_transform(image_size: int = 224, train: bool = True, include_hflip: bool = True):
    if train:
        aug = [
            transforms.Resize((image_size + 32, image_size + 32)),
            transforms.RandomResizedCrop(image_size, scale=(0.8, 1.0)),
        ]
        if include_hflip:
            aug.append(transforms.RandomHorizontalFlip())
        aug += [
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ]
        t = transforms.Compose(aug)
    else:
        t = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
        ])
    return t


def stack_rgb_fft(rgb: torch.Tensor, fft: torch.Tensor) -> torch.Tensor:
    # rgb: (3,H,W), fft: (1,H,W)
    return torch.cat([rgb, fft], dim=0)
