#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# vast_run.sh — reproduce colab_run.ipynb's training on a rented GPU box.
#
# Prereqs (already done if you followed the transfer steps):
#   - code at $PROJECT
#   - datasets at  $PROJECT/dataset/face_forensics  and  $PROJECT/dataset/celeb_df
#   - deps installed (see preflight in chat: timm, facenet-pytorch, opencv, ...)
#
# Run it detached so an SSH drop won't kill it:
#   tmux new -s train        # then inside tmux:
#   bash vast_run.sh 2>&1 | tee vast_train_$(date +%Y%m%d_%H%M%S).log
#   # detach with Ctrl-b d ; reattach later with: tmux attach -t train
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ===== KNOBS — the only lines you'd normally change ==========================
PROJECT="/workspace/skripsi/deepfake_hybrid"
N_SEEDS=3                       # matches config.yaml (statistical validity)
TIERS="100 250 500 750"         # sample-size tiers, both datasets — matches notebook
MAX_FRAMES=100                  # frames per video (notebook value; config.yaml default is 50)
EPOCHS=30
FACE_MARGIN=0.3                 # MTCNN face-crop margin (notebook: FACE_CROP=True, margin 0.3)
ROC_SEED=0                      # which seed's checkpoints to plot ROC/CM for (representative)
# =============================================================================

cd "$PROJECT"

# ── Build vast_config.yaml: base config.yaml + notebook overrides + GPU tune ──
# (mirrors notebook Step 2 GPU auto-tune and Step 4 config patching)
N_SEEDS="$N_SEEDS" MAX_FRAMES="$MAX_FRAMES" EPOCHS="$EPOCHS" python - <<'PY'
import os, yaml, torch
cfg = yaml.safe_load(open('config.yaml'))

# GPU auto-tune — same thresholds as the notebook (+ H100 / 24GB tiers)
if torch.cuda.is_available():
    name = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / 1e9
    if 'A100' in name or 'H100' in name or vram >= 35:
        batch, workers, compile_ = 128, 8, True
    elif vram >= 14:                       # 4090/3090/A5000/V100/T4 …
        batch, workers, compile_ = 64, 4, False
    else:
        batch, workers, compile_ = 32, 2, False
    print(f"GPU: {name} ({vram:.0f} GB) -> batch={batch} workers={workers} compile={compile_}")
else:
    raise SystemExit("ERROR: no CUDA GPU detected — aborting (would train on CPU).")

cfg['output_root']          = './outputs'
cfg['frame_sampling_fps']   = 5
cfg['max_frames_per_video'] = int(os.environ['MAX_FRAMES'])
cfg['image_size']           = 224
cfg['batch_size']           = batch
cfg['num_workers']          = workers
cfg['compile_model']        = compile_
cfg['epochs']               = int(os.environ['EPOCHS'])
cfg['n_seeds']              = int(os.environ['N_SEEDS'])
cfg['fusion_mode']          = 'two_branch'
# dataset roots + real/fake keywords are already correct in config.yaml

# Fail-fast: confirm the hyperparams train.py would otherwise silently default
for k in ['freq_depth','freq_base_channels','early_stop_patience','label_smoothing','fft_noise_sigma']:
    assert k in cfg, f"config.yaml missing '{k}' — would fall back to train.py default!"

yaml.dump(cfg, open('vast_config.yaml','w'), default_flow_style=False)
print(f"vast_config.yaml: seeds={cfg['n_seeds']} max_frames={cfg['max_frames_per_video']} "
      f"freq_depth={cfg['freq_depth']} base_ch={cfg['freq_base_channels']} "
      f"patience={cfg['early_stop_patience']} label_smoothing={cfg['label_smoothing']}")
PY

CFG="vast_config.yaml"
BATCH=$(python -c "import yaml;print(yaml.safe_load(open('vast_config.yaml'))['batch_size'])")
WORKERS=$(python -c "import yaml;print(yaml.safe_load(open('vast_config.yaml'))['num_workers'])")
echo "Using batch_size=$BATCH num_workers=$WORKERS n_seeds=$N_SEEDS tiers=[$TIERS]"

# ── Training loop — mirrors notebook Step 4 ─────────────────────────────────
#   A) FFPP: preprocess (frames+splits+FFT) + train spatial/freq/hybrid
#   B) CDF : preprocess + train
#   C) run_all both: SKIPS training (checkpoints exist) → only cross-dataset
#      eval, producing the complete Table1/Table2/Table3 for this tier.
for n in $TIERS; do
  echo ""
  echo "############################################################"
  echo "#  TIER n=$n   ($(date '+%Y-%m-%d %H:%M:%S'))"
  echo "############################################################"

  echo "--- [A] FFPP n=$n: preprocess + train ---"
  python scripts/run_pipeline.py --config "$CFG" --dataset FFPP \
      --n-samples "$n" --max-frames "$MAX_FRAMES" --epochs "$EPOCHS" \
      --num-workers "$WORKERS" --batch-size "$BATCH" \
      --force-fft --face-crop --face-margin "$FACE_MARGIN" --pretrained

  echo "--- [B] CDF n=$n: preprocess + train ---"
  python scripts/run_pipeline.py --config "$CFG" --dataset CDF \
      --n-samples "$n" --max-frames "$MAX_FRAMES" --epochs "$EPOCHS" \
      --num-workers "$WORKERS" --batch-size "$BATCH" \
      --force-fft --face-crop --face-margin "$FACE_MARGIN" --pretrained

  echo "--- [C] Cross-dataset eval + tables n=$n ---"
  python scripts/run_all.py --config "$CFG" --dataset both \
      --n-samples "$n" --pretrained

  # ── [D] ROC curves + confusion matrices (inference only, seed $ROC_SEED) ────
  #   Must run HERE (inside the loop): manifests/FFPP|CDF/test.csv are NOT
  #   tier-tagged and get overwritten next tier, so the correct-tier test split
  #   is only on disk now. CM thresholds are auto-loaded from each run's
  #   threshold.json (written by [C]); cross-dataset uses the train-set threshold.
  #   Non-fatal: a plotting hiccup must not abort training of later tiers.
  echo "--- [D] ROC + confusion matrices n=$n (seed $ROC_SEED, inference only) ---"
  FFPP_CKPTS="spatial:outputs/runs/spatial_FFPP_n${n}_seed${ROC_SEED}/best.pt \
              hybrid:outputs/runs/hybrid_FFPP_n${n}_seed${ROC_SEED}/best.pt \
              freq:outputs/runs/freq_FFPP_n${n}_seed${ROC_SEED}/best.pt"
  CDF_CKPTS="spatial:outputs/runs/spatial_CDF_n${n}_seed${ROC_SEED}/best.pt \
             hybrid:outputs/runs/hybrid_CDF_n${n}_seed${ROC_SEED}/best.pt \
             freq:outputs/runs/freq_CDF_n${n}_seed${ROC_SEED}/best.pt"

  # In-dataset: FFPP-trained -> FFPP test, CDF-trained -> CDF test
  python scripts/make_roc_cm.py --models $FFPP_CKPTS \
      --test-manifest outputs/manifests/FFPP/test.csv \
      --fft-cache-root outputs/fft_cache/FFPP \
      --batch-size "$BATCH" --num-workers "$WORKERS" \
      --tag "FFPP_in_n${n}" --title "In-Dataset FFPP (n=${n})" \
      || echo "  !! [D] FFPP_in_n${n} failed — continuing"

  python scripts/make_roc_cm.py --models $CDF_CKPTS \
      --test-manifest outputs/manifests/CDF/test.csv \
      --fft-cache-root outputs/fft_cache/CDF \
      --batch-size "$BATCH" --num-workers "$WORKERS" \
      --tag "CDF_in_n${n}" --title "In-Dataset CDF (n=${n})" \
      || echo "  !! [D] CDF_in_n${n} failed — continuing"

  # Cross-dataset: FFPP-trained -> CDF test, CDF-trained -> FFPP test
  python scripts/make_roc_cm.py --models $FFPP_CKPTS \
      --test-manifest outputs/manifests/CDF/test.csv \
      --fft-cache-root outputs/fft_cache/CDF \
      --batch-size "$BATCH" --num-workers "$WORKERS" \
      --tag "FFPP2CDF_n${n}" --title "Cross-Dataset FFPP->CDF (n=${n})" \
      || echo "  !! [D] FFPP2CDF_n${n} failed — continuing"

  python scripts/make_roc_cm.py --models $CDF_CKPTS \
      --test-manifest outputs/manifests/FFPP/test.csv \
      --fft-cache-root outputs/fft_cache/FFPP \
      --batch-size "$BATCH" --num-workers "$WORKERS" \
      --tag "CDF2FFPP_n${n}" --title "Cross-Dataset CDF->FFPP (n=${n})" \
      || echo "  !! [D] CDF2FFPP_n${n} failed — continuing"
done

# ── Plots for the results chapter ───────────────────────────────────────────
NS=$(echo $TIERS | tr ' ' ',')
python scripts/plot_results.py --config "$CFG" --n-samples "$NS"

echo ""
echo "############################################################"
echo "#  ALL DONE — seeds=$N_SEEDS tiers=[$TIERS]"
echo "#  Tables:      outputs/tables/n*/{Table1,Table2,Table3}*.csv"
echo "#  Checkpoints: outputs/runs/<model>_<dataset>_n<N>_seed<S>/best.pt"
echo "#  Plots:       outputs/plots/"
echo "#  ROC/CM:      outputs/roc_cm/{FFPP_in,CDF_in,FFPP2CDF,CDF2FFPP}_n<N>_*.png (seed $ROC_SEED)"
echo "############################################################"
