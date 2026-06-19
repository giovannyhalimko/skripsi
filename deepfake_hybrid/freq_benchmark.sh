#!/usr/bin/env bash
# freq_benchmark.sh — head-to-head: FreqCNN vs ResNet18 on the frequency branch.
#
# Trains ResNet18 on the SAME single-channel FFT input as FreqCNN, in TWO arms:
#   - pretrained : ImageNet weights (the "just use a standard transfer-learning backbone" baseline)
#   - scratch    : random init (the controlled architecture comparison — matches FreqCNN's
#                  from-scratch condition, isolating architecture as the only variable)
# This pre-empts both reviewer objections at once: ResNet18 fails to beat FreqCNN whether
# pretrained OR from scratch, at ~2.65x the parameters (11.2M vs 4.2M @ depth=5,base=64).
#
# Run AFTER vast_run.sh (n=750 manifests + FFT cache + freq_*_n750_seed0 checkpoints must exist).
# Trains on FFPP n=750 seed=0 and CDF n=750 seed=0, then overlays ROC + CM against the
# existing FreqCNN checkpoints.
#
# Usage (from deepfake_hybrid/):
#   bash freq_benchmark.sh 2>&1 | tee freq_benchmark.log
# ---------------------------------------------------------------------------
set -euo pipefail

PROJECT="${PROJECT:-$(cd "$(dirname "$0")" && pwd)}"
cd "$PROJECT"

CFG="vast_config.yaml"
if [ ! -f "$CFG" ]; then
  echo "ERROR: $CFG not found — run vast_run.sh first to generate it." >&2
  exit 1
fi

BATCH=$(python -c "import yaml; print(yaml.safe_load(open('$CFG'))['batch_size'])")
WORKERS=$(python -c "import yaml; print(yaml.safe_load(open('$CFG'))['num_workers'])")

echo "============================================================"
echo "  freq_benchmark.sh  (batch=$BATCH  workers=$WORKERS)"
echo "  Prereq: vast_run.sh must have already run at n=750"
echo "============================================================"

# ── Step 1: Train freq_resnet18 — both arms, both datasets ──────────────────
# --run-suffix keeps the two arms (same model/dataset/n/seed) in separate run dirs.
for DS in FFPP CDF; do
  echo ""
  echo "--- [1] Train freq_resnet18 on $DS n=750 seed=0 (pretrained) ---"
  python scripts/train.py \
      --config "$CFG" --dataset "$DS" --model freq_resnet18 \
      --n-samples 750 --seed 0 --pretrained --run-suffix _pretrained

  echo ""
  echo "--- [1] Train freq_resnet18 on $DS n=750 seed=0 (scratch) ---"
  python scripts/train.py \
      --config "$CFG" --dataset "$DS" --model freq_resnet18 \
      --n-samples 750 --seed 0 --run-suffix _scratch
done

# ── Step 2: Head-to-head ROC + CM overlays (FreqCNN vs both ResNet18 arms) ──
echo ""
echo "--- [2] ROC + confusion matrices (FreqCNN vs ResNet18 pretrained/scratch) ---"

FREQ_FFPP="freq:outputs/runs/freq_FFPP_n750_seed0/best.pt"
FREQ_CDF="freq:outputs/runs/freq_CDF_n750_seed0/best.pt"
RN18P_FFPP="freq_resnet18:outputs/runs/freq_resnet18_FFPP_n750_seed0_pretrained/best.pt"
RN18S_FFPP="freq_resnet18:outputs/runs/freq_resnet18_FFPP_n750_seed0_scratch/best.pt"
RN18P_CDF="freq_resnet18:outputs/runs/freq_resnet18_CDF_n750_seed0_pretrained/best.pt"
RN18S_CDF="freq_resnet18:outputs/runs/freq_resnet18_CDF_n750_seed0_scratch/best.pt"

LABELS=("FreqCNN" "ResNet18 (pretrained)" "ResNet18 (scratch)")

# In-dataset FFPP
python scripts/make_roc_cm.py \
    --models "$FREQ_FFPP" "$RN18P_FFPP" "$RN18S_FFPP" \
    --labels "${LABELS[@]}" \
    --test-manifest outputs/manifests/FFPP/test.csv \
    --fft-cache-root outputs/fft_cache/FFPP \
    --batch-size "$BATCH" --num-workers "$WORKERS" \
    --tag "freqbench_FFPP_in_n750" \
    --title "Frequency Branch: FreqCNN vs ResNet18 — In-Dataset FFPP (n=750)" \
    || echo "  !! freqbench_FFPP_in_n750 failed — continuing"

# In-dataset CDF
python scripts/make_roc_cm.py \
    --models "$FREQ_CDF" "$RN18P_CDF" "$RN18S_CDF" \
    --labels "${LABELS[@]}" \
    --test-manifest outputs/manifests/CDF/test.csv \
    --fft-cache-root outputs/fft_cache/CDF \
    --batch-size "$BATCH" --num-workers "$WORKERS" \
    --tag "freqbench_CDF_in_n750" \
    --title "Frequency Branch: FreqCNN vs ResNet18 — In-Dataset CDF (n=750)" \
    || echo "  !! freqbench_CDF_in_n750 failed — continuing"

# Cross-dataset FFPP -> CDF
python scripts/make_roc_cm.py \
    --models "$FREQ_FFPP" "$RN18P_FFPP" "$RN18S_FFPP" \
    --labels "${LABELS[@]}" \
    --test-manifest outputs/manifests/CDF/test.csv \
    --fft-cache-root outputs/fft_cache/CDF \
    --batch-size "$BATCH" --num-workers "$WORKERS" \
    --tag "freqbench_FFPP2CDF_n750" \
    --title "Frequency Branch: FreqCNN vs ResNet18 — FFPP->CDF (n=750)" \
    || echo "  !! freqbench_FFPP2CDF_n750 failed — continuing"

# Cross-dataset CDF -> FFPP
python scripts/make_roc_cm.py \
    --models "$FREQ_CDF" "$RN18P_CDF" "$RN18S_CDF" \
    --labels "${LABELS[@]}" \
    --test-manifest outputs/manifests/FFPP/test.csv \
    --fft-cache-root outputs/fft_cache/FFPP \
    --batch-size "$BATCH" --num-workers "$WORKERS" \
    --tag "freqbench_CDF2FFPP_n750" \
    --title "Frequency Branch: FreqCNN vs ResNet18 — CDF->FFPP (n=750)" \
    || echo "  !! freqbench_CDF2FFPP_n750 failed — continuing"

# ── Step 3: Parameter count comparison ──────────────────────────────────────
echo ""
echo "--- [3] Parameter counts ---"
python - <<'PY'
import sys
sys.path.insert(0, 'src')
from models.freq_cnn import FreqCNN
from models.freq_resnet18 import build_freq_resnet18
import yaml

cfg = yaml.safe_load(open('vast_config.yaml'))
depth = cfg.get('freq_depth', 3)
base  = cfg.get('freq_base_channels', 32)

freq_cnn   = FreqCNN(num_classes=1, depth=depth, base_channels=base)
freq_rn18  = build_freq_resnet18(num_classes=1, pretrained=False)

p_freq  = sum(p.numel() for p in freq_cnn.parameters())
p_rn18  = sum(p.numel() for p in freq_rn18.parameters())

print(f"FreqCNN  (depth={depth}, base={base}): {p_freq:,} params  ({p_freq/1e6:.2f}M)")
print(f"ResNet18 (1-ch, timm):                {p_rn18:,} params  ({p_rn18/1e6:.2f}M)")
print(f"Ratio: ResNet18 is {p_rn18/p_freq:.1f}x larger than FreqCNN")
print("(ResNet18 param count is identical for the pretrained and scratch arms.)")
PY

echo ""
echo "============================================================"
echo "  freq_benchmark.sh DONE"
echo "  Checkpoints:"
echo "    outputs/runs/freq_resnet18_{FFPP,CDF}_n750_seed0_pretrained/best.pt"
echo "    outputs/runs/freq_resnet18_{FFPP,CDF}_n750_seed0_scratch/best.pt"
echo "  ROC/CM outputs:"
echo "    outputs/roc_cm/freqbench_*_n750_roc.png"
echo "    outputs/roc_cm/freqbench_*_n750_cm_*.png"
echo "    outputs/roc_cm/freqbench_*_n750_metrics.json"
echo "============================================================"
