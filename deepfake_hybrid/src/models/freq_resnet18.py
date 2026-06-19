import torch.nn as nn

try:
    import timm
except ImportError as e:
    raise ImportError("timm is required. Install via pip install timm") from e


def build_freq_resnet18(num_classes: int = 1, pretrained: bool = True) -> nn.Module:
    # in_chans=1: timm adapts ImageNet conv1 weights (average across RGB channels)
    # for the single-channel FFT log-magnitude input. ~11.2M params vs FreqCNN ~4.2M.
    return timm.create_model(
        "resnet18",
        pretrained=pretrained,
        num_classes=num_classes,
        in_chans=1,
        global_pool="avg",
    )
