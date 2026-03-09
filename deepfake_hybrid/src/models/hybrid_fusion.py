import torch
import torch.nn as nn

from .spatial_xception import build_feature_extractor, get_feature_dim
from .freq_cnn import FreqCNN


class HybridTwoBranch(nn.Module):
    def __init__(self, pretrained: bool = True):
        super().__init__()
        self.spatial = build_feature_extractor(pretrained=pretrained)
        self.freq = FreqCNN(num_classes=1)
        spatial_dim = get_feature_dim()
        freq_dim = self.freq.feature_dim()

        # Normalize each branch before fusion to fix feature scale imbalance
        self.spatial_bn = nn.BatchNorm1d(spatial_dim)
        self.freq_bn = nn.BatchNorm1d(freq_dim)

        self.classifier = nn.Sequential(
            nn.Linear(spatial_dim + freq_dim, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, 1),
        )

    def forward(self, rgb, fft):
        spatial_feat = self.spatial(rgb)
        spatial_feat = self.spatial_bn(spatial_feat)

        freq_feat = self.freq.features(fft)
        freq_feat = torch.flatten(freq_feat, 1)
        freq_feat = self.freq_bn(freq_feat)

        fused = torch.cat([spatial_feat, freq_feat], dim=1)
        logits = self.classifier(fused)
        return logits.squeeze(-1)


class EarlyFusionXception(nn.Module):
    def __init__(self, pretrained: bool = True):
        super().__init__()
        from .spatial_xception import build_xception

        self.model = build_xception(num_classes=1, in_chans=4, pretrained=pretrained)

    def forward(self, x):
        return self.model(x).squeeze(-1)
