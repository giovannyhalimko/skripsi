import torch
import torch.nn as nn

from .spatial_xception import build_feature_extractor, get_feature_dim
from .freq_cnn import FreqCNN


PROJ_DIM = 256


class SEGate(nn.Module):
    """Squeeze-and-Excitation gating on the fused feature vector."""

    def __init__(self, in_dim: int, reduction: int = 4):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Linear(in_dim, in_dim // reduction),
            nn.ReLU(inplace=True),
            nn.Linear(in_dim // reduction, in_dim),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return x * self.gate(x)


class HybridTwoBranch(nn.Module):
    def __init__(self, pretrained: bool = True, freq_depth: int = 3, freq_base_channels: int = 32):
        super().__init__()
        self.spatial = build_feature_extractor(pretrained=pretrained)
        self.freq = FreqCNN(num_classes=1, depth=freq_depth, base_channels=freq_base_channels)
        spatial_dim = get_feature_dim()
        freq_dim = self.freq.feature_dim()

        self.spatial_proj = nn.Sequential(
            nn.Linear(spatial_dim, PROJ_DIM),
            nn.BatchNorm1d(PROJ_DIM),
            nn.ReLU(inplace=True),
        )
        self.freq_proj = nn.Sequential(
            nn.Linear(freq_dim, PROJ_DIM),
            nn.BatchNorm1d(PROJ_DIM),
            nn.ReLU(inplace=True),
        )

        fused_dim = PROJ_DIM * 2
        self.se_gate = SEGate(fused_dim)
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(fused_dim, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
        )

    def forward(self, rgb, fft):
        spatial_feat = self.spatial(rgb)
        freq_feat = self.freq.features(fft)
        freq_feat = torch.flatten(freq_feat, 1)

        spatial_feat = self.spatial_proj(spatial_feat)
        freq_feat = self.freq_proj(freq_feat)

        fused = torch.cat([spatial_feat, freq_feat], dim=1)
        fused = self.se_gate(fused)
        logits = self.classifier(fused)
        return logits.squeeze(-1)


class EarlyFusionXception(nn.Module):
    def __init__(self, pretrained: bool = True):
        super().__init__()
        from .spatial_xception import build_xception

        self.model = build_xception(num_classes=1, in_chans=4, pretrained=pretrained)

    def forward(self, x):
        return self.model(x).squeeze(-1)
