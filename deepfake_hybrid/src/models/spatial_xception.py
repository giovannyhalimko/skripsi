import torch
import torch.nn as nn

try:
    import timm
except ImportError as e:
    raise ImportError("timm is required for Xception. Install via pip install timm") from e


def build_xception(num_classes: int = 1, in_chans: int = 3, pretrained: bool = True) -> nn.Module:
    model = timm.create_model(
        "xception",
        pretrained=pretrained,
        num_classes=num_classes,
        in_chans=in_chans,
        global_pool="avg",
    )
    return model


def build_feature_extractor(in_chans: int = 3, pretrained: bool = True) -> nn.Module:
    model = timm.create_model(
        "xception",
        pretrained=pretrained,
        num_classes=0,  # return features
        in_chans=in_chans,
        global_pool="avg",
    )
    return model


def get_feature_dim(in_chans: int = 3) -> int:
    model = timm.create_model(
        "xception",
        pretrained=False,
        num_classes=0,
        in_chans=in_chans,
        global_pool="avg",
    )
    return model.num_features
