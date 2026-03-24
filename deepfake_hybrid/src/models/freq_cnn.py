import torch
import torch.nn as nn


class FreqCNN(nn.Module):
    """CNN for single-channel FFT log-magnitude maps with configurable depth.

    Args:
        num_classes: Number of output classes (1 for binary).
        depth: Number of conv blocks (3 or 5). Default 3 (~130K params).
               depth=3: 1→32→64→128, feature_dim=128.
               depth=5: 1→32→64→128→256→256, feature_dim=256 (~700K params).
        base_channels: Number of channels in first conv block (default 32).
    """

    def __init__(self, num_classes: int = 1, depth: int = 3, base_channels: int = 32):
        super().__init__()
        if depth < 1:
            raise ValueError(f"depth must be >= 1, got {depth}")

        # Build channel progression: [base, base*2, base*4, ...] capped at base*8
        channels = [min(base_channels * (2 ** i), base_channels * 8) for i in range(depth)]
        # Last two blocks at depth=5 reuse the same channel count (256)
        if depth == 5:
            channels[3] = base_channels * 8
            channels[4] = base_channels * 8

        layers = []
        in_ch = 1
        for i, out_ch in enumerate(channels):
            layers += [
                nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(2),
            ]
            in_ch = out_ch

        # Spatial dropout for regularization before pooling
        layers.append(nn.Dropout2d(0.2))
        layers.append(nn.AdaptiveAvgPool2d((1, 1)))
        self.features = nn.Sequential(*layers)
        self._feature_dim = channels[-1]

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(self._feature_dim, max(self._feature_dim // 2, 32)),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(max(self._feature_dim // 2, 32), num_classes),
        )

    def forward(self, x):
        feats = self.features(x)
        logits = self.classifier(feats)
        return logits.squeeze(-1)

    def feature_dim(self) -> int:
        return self._feature_dim
