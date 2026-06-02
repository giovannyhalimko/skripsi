"""Regenerate the learning-rate schedule figure for BAB III (Gambar Kurva Penjadwalan LR).

Replicates the EXACT scheduler from scripts/train.py:
  SequentialLR([
      LinearLR(start_factor=0.1, end_factor=1.0, total_iters=3),   # warmup 3 epochs
      CosineAnnealingLR(T_max=epochs-3, eta_min=1e-6),
  ], milestones=[3])
with base_lr = 2e-4, epochs = 30.

Output: documents/media_v2/gambar_3_10_lr_schedule.png
"""
from pathlib import Path

import torch
import matplotlib.pyplot as plt

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "documents" / "media_v2" / "gambar_3_10_lr_schedule.png"

BASE_LR = 2e-4
EPOCHS = 30
WARMUP = 3

# A dummy parameter so we can attach a real optimizer/scheduler (exact replication)
p = torch.nn.Parameter(torch.zeros(1))
opt = torch.optim.AdamW([p], lr=BASE_LR)
warmup = torch.optim.lr_scheduler.LinearLR(opt, start_factor=0.1, end_factor=1.0, total_iters=WARMUP)
cosine = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(EPOCHS - WARMUP, 1), eta_min=1e-6)
sched = torch.optim.lr_scheduler.SequentialLR(opt, schedulers=[warmup, cosine], milestones=[WARMUP])

epochs, lrs = [], []
for e in range(1, EPOCHS + 1):
    epochs.append(e)
    lrs.append(opt.param_groups[0]["lr"])
    opt.step()
    sched.step()

print("Per-epoch LR (first 6):", [f"{e}:{lr:.2e}" for e, lr in zip(epochs[:6], lrs[:6])])

fig, ax = plt.subplots(figsize=(8, 4.5))
# warmup region shading
ax.axvspan(1, WARMUP, color="#ffe8c2", alpha=0.7, label="Warmup linear (epoch 1–3)")
ax.axvspan(WARMUP, EPOCHS, color="#d8ebff", alpha=0.5, label="Cosine decay (epoch 4–30)")
ax.plot(epochs, lrs, marker="o", markersize=4, color="#1f4e79", linewidth=1.8)

# annotate key points
for e in (1, 2, 3, 4):
    ax.annotate(f"{lrs[e-1]:.1e}", (e, lrs[e-1]), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=8)
ax.annotate(f"{lrs[-1]:.0e}", (EPOCHS, lrs[-1]), textcoords="offset points",
            xytext=(-2, 8), ha="center", fontsize=8)

ax.set_xlabel("Epoch")
ax.set_ylabel("Learning rate")
ax.set_title("Kurva Penjadwalan Learning Rate (Warmup 3 Epoch + Cosine Decay)")
ax.set_xticks([1, 3, 5, 10, 15, 20, 25, 30])
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=200, bbox_inches="tight")
print("saved", OUT)
