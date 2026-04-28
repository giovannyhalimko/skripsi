# Hybrid Training Fixes — Code Changes Documentation

**Date:** 2026-04-25
**Scope:** Hybrid LR rebalance, patience/unfreeze fix, classifier regularization, val-threshold tuning
**Motivated by:** Analysis of 2026-04-15 n=500 run — hybrid FFPP peaked at epoch 1 (AUC 0.62) and never improved; early-stopped at epoch 6 with train_loss 0.15 vs val_auc 0.55 (textbook overfit)

---

## Summary of All Changes

| Change | Files Modified | Impact |
|--------|---------------|--------|
| Hybrid optimizer: 2 → 3 param groups | `scripts/train.py` | Prevents freq branch from overpowering gradients early |
| Reset patience counter at unfreeze | `scripts/train.py` | Gives fine-tuning a fresh window after backbone unfreezing |
| Bump patience 10 → 12 | `config.yaml` | Buffer around the 3-epoch unfreeze boundary |
| Label smoothing 0.0 → 0.05 | `config.yaml` | Reduces overconfidence on 350-sample training set |
| Classifier dropout 0.3 → 0.5 | `src/models/hybrid_fusion.py` | Stronger regularization on the fusion head |
| Val-threshold tuning in run_all | `scripts/run_all.py` | Tables now report F1 at val-optimal threshold instead of hardcoded 0.5 |

---

## 1. Hybrid Optimizer: 3 Param Groups

**Problem:** The hybrid model previously used 2 optimizer param groups:
- Group 1: `model.spatial.*` at backbone_lr (2e-5 effective)
- Group 2: `model.freq.*` + `model.spatial_proj` + `model.freq_proj` + `model.se_gate` + `model.classifier` at head_lr (2e-4)

The freq branch is randomly initialized but was grouped with the fusion head and got the full 2e-4 LR. During the frozen-backbone phase (epochs 1–3), the freq branch could overfit fast and establish a dominant gradient direction before the spatial branch contributed anything. When the backbone unfroze at epoch 4, the fusion had already converged to a freq-only representation.

**Fix (`scripts/train.py:198–215`):** Split hybrid into 3 groups:

```python
optimizer = optim.AdamW([
    {"params": backbone_params, "lr": backbone_lr},          # 2e-5 — spatial backbone
    {"params": freq_branch_params, "lr": base_lr * 0.25},    # 5e-5 — freq branch (new)
    {"params": fusion_head_params, "lr": base_lr},           # 2e-4 — projection/SE/classifier
], weight_decay=wd)
```

- `freq_branch_params` = `model.freq.*`
- `fusion_head_params` = `model.spatial_proj.*` + `model.freq_proj.*` + `model.se_gate.*` + `model.classifier.*`

Train log will now show 3 LR values, e.g. `lr=['2.00e-06', '5.00e-07', '2.00e-06']` during warmup.

---

## 2. Patience Counter Reset at Unfreeze

**Problem:** In the 2026-04-15 run, hybrid FFPP early-stopped at epoch 6 — only 2 epochs after the backbone unfroze at epoch 4. The patience counter was already at 3 from the frozen phase (epochs 2–3 didn't improve over epoch 1's AUC 0.62). Two more non-improving post-unfreeze epochs triggered early stop before fine-tuning could converge.

**Fix (`scripts/train.py:280`):** Reset `no_improve_count = 0` inside the unfreeze block:

```python
if epoch == FREEZE_EPOCHS + 1:
    # ... unfreeze params ...
    # Reset patience counter so fine-tuning gets a full window to converge
    no_improve_count = 0
```

This applies to all three model types (spatial, hybrid, early_fusion) since all share the same unfreeze block.

---

## 3. Patience + Label Smoothing (config.yaml)

**`early_stop_patience`: 10 → 12**

Adds 2 extra epochs of buffer. Primary motivation: the reset-at-unfreeze fix means fine-tuning now gets a full patience window, so 12 gives 12 epochs post-unfreeze before stopping. Previously logs showed "5 consecutive epochs" despite config having 10 — root cause was the Kaggle-side config missing the key (train.py default is 5). Bump to 12 makes the intent explicit.

**`label_smoothing`: 0.0 → 0.05**

The previous comment said "Disabled — maximise signal at small n". At n=500 with 350 training frames per class the hybrid FFPP was still collapsing (train_loss 0.15 = overconfident on training data). 0.05 smoothing targets `0.95`/`0.05` instead of `1.0`/`0.0`, preventing the model from driving logits to ±∞ on training examples. Applies to all model types via the existing implementation in `scripts/train.py:108–109`.

---

## 4. Classifier Dropout 0.3 → 0.5 (hybrid_fusion.py)

**`src/models/hybrid_fusion.py:49,52`**

```python
self.classifier = nn.Sequential(
    nn.Dropout(0.5),        # was 0.3
    nn.Linear(fused_dim, 128),
    nn.ReLU(inplace=True),
    nn.Dropout(0.5),        # was 0.3
    nn.Linear(128, 1),
)
```

The SE gate feeds a 512-d vector into the classifier. At 350 training samples, even 0.3 dropout is not enough to prevent the 512×128 weight matrix from memorizing training patterns. 0.5 forces the network to distribute information across the full feature space. Projection layers (spatial_proj, freq_proj) are unchanged — their BatchNorm1d already provides some regularization.

---

## 5. Val-Threshold Tuning in run_all.py

**Problem:** `run_all.py:83` called `compute_metrics(y_true, y_prob)` without a threshold argument, defaulting to 0.5. For the freq model on FFPP this caused F1 to oscillate between 0.0 and 0.69 across epochs — the model had signal (AUC 0.67) but the operating point at 0.5 was unstable. Table1/2/3 were reporting F1 at a misleading threshold.

**Fix (`scripts/run_all.py`):** Added two new functions and updated the eval loop.

`compute_val_threshold(cfg, train_dataset_name, model_type, checkpoint_path, run_dir, seed)`:
- Loads the val split for the training dataset
- Runs inference with the saved checkpoint
- Calls `metrics_mod.find_optimal_threshold()` (Youden's J, already in `src/metrics.py:35`)
- Saves result to `outputs/runs/<run_name>/threshold.json` (cached — won't re-run if file exists)
- Returns the threshold float

`_run_inference(cfg, manifest_path, dataset_name, model_type, model, device, seed)` / `_load_model(...)`:
- Extracted from the old monolithic `eval_checkpoint` to avoid loading the model twice (once for val threshold, once for test eval)

`eval_checkpoint(..., threshold=0.5)`:
- Now accepts an explicit threshold; adds `"threshold"` key to the returned metrics dict so the tables record what threshold was used

**Main loop:**
```python
threshold = compute_val_threshold(cfg, eff_train, model_type, ckpt, run_dir, seed)
metrics_in   = eval_checkpoint(cfg, eff_train,  model_type, ckpt, seed, threshold=threshold)
metrics_cross = eval_checkpoint(cfg, eff_other, model_type, ckpt, seed, threshold=threshold)
```

Cross-dataset eval uses the *training dataset's* val threshold — matches deployment reality (can only calibrate on data you have). Table1/2/3 now include a `threshold` column.

---

## Key Motivation (from 2026-04-15 run)

| Issue | Evidence | Fix |
|-------|----------|-----|
| Hybrid FFPP peaks epoch 1, never improves | train_loss 0.677→0.149, val_auc stuck 0.55–0.62 | 3-group LR + patience reset |
| Early stop fires 2 epochs after unfreeze | "did not improve for 5 consecutive epochs" at epoch 6 | patience reset at unfreeze |
| Freq FFPP F1 0.0021/0.66/0.0000 alternating | AUC stable 0.67 but F1 collapses | val-threshold tuning |
| Hybrid overfit on 350-sample training set | train_loss 0.15 vs val_auc 0.55 = 78% loss drop, no val gain | dropout 0.5 + label smoothing 0.05 |
| patience in Kaggle run was 5 not 10 | train.py default is 5; Kaggle config missing the key | explicit 12 in config + train.py default bump |
