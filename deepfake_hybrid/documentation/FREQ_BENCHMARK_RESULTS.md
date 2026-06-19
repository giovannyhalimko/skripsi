# Frequency-Branch Benchmark — Results (FreqCNN vs ResNet18)

**Run date:** 2026-06-19 · **Box:** rented GPU (RTX 3090) · **Driver:** `freq_benchmark.sh`
(mechanics documented in `CODE_WALKTHROUGH.md` §11; this file records the *outcome*).

## What was run

Head-to-head on the **frequency branch only** — the single-channel FFT log-magnitude map —
at **n=750, seed 0**, two arms for the standard backbone:

- **FreqCNN** — the thesis's from-scratch CNN (depth=5, base=64, **4.22M** params).
- **ResNet18 (pretrained)** — ImageNet `resnet18.a1_in1k`, conv1 adapted 3→1 channel
  (the "just use a standard transfer-learning backbone" baseline).
- **ResNet18 (scratch)** — random init, identical training to FreqCNN
  (the **controlled** architecture comparison — isolates architecture as the only variable).

Both ResNet18 arms are **11.17M** params → **2.6× larger** than FreqCNN. Evaluated in- and
cross-dataset, giving four conditions.

## Results — AUC (primary metric, threshold-independent)

| Condition (n=750, seed 0) | FreqCNN (4.2M) | ResNet18-pretrained (11.2M) | ResNet18-scratch (11.2M) |
|---|---|---|---|
| In-dataset **FFPP**        | **0.569** | 0.561 | 0.507 |
| In-dataset **CDF**         | 0.578     | **0.609** | 0.545 |
| Cross **FFPP → CDF**       | 0.614     | **0.628** | 0.544 |
| Cross **CDF → FFPP**       | **0.586** | 0.578 | 0.545 |

Bold = best in row. Params: FreqCNN 4,217,217 vs ResNet18 11.17M (**2.6×**, identical for
both ResNet18 arms).

## Interpretation — the result only *partially* supports the benchmark's premise

`freq_benchmark.sh`'s header asserts "ResNet18 fails to beat FreqCNN whether pretrained OR
from scratch." The data says:

- ✅ **From-scratch (controlled comparison): FreqCNN wins all 4 conditions** despite 2.6×
  fewer parameters. This cleanly answers the reviewer objection *"your custom net is just a
  worse standard CNN."* Under matched training, the lightweight FreqCNN is **not** outclassed
  by a deeper standard CNN on the FFT input.
- ⚠️ **Pretrained: a 2–2 split.** ImageNet-ResNet18 *beats* FreqCNN on **CDF-in** (0.609 vs
  0.578) and **FFPP→CDF** (0.628 vs 0.614), and loses narrowly on the other two. The *"just
  use a pretrained backbone"* objection is **not refuted** — the transfer-learning baseline is
  competitive. **Do not cite the pretrained arm as a FreqCNN win.**

The defensible thesis claim is the **scratch** one: matched-condition architecture comparison
favors FreqCNN everywhere. The pretrained arm should be reported as "ImageNet transfer makes
ResNet18 roughly on par with FreqCNN on the frequency input, at 2.6× the parameters."

## Caveats (read before citing)

1. **Near-chance regime.** Every AUC sits in **0.51–0.63** — the frequency branch *alone* is
   close to chance (consistent with `freq` being the weakest model in the main matrix). Gaps
   of ~0.01–0.03 are fragile.
2. **Single seed.** Seed 0 only; no error bars / repeated-seed variance. Treat sub-0.03
   differences as ties.
3. **`acc`/`f1` in the JSON are not directly comparable.** FreqCNN uses a *saved* operating
   threshold (`threshold.json`); both ResNet18 arms use **Youden's-J fit on the test set**,
   which mildly flatters ResNet18's accuracy/F1. **Lead with AUC.** (For reference, accuracies
   land ~0.52–0.60 across the board and do not change the ranking story.)

## Operational notes / gotchas

- **Offline weights.** The box is air-gapped (no HF egress). `resnet18.a1_in1k` weights were
  pushed from a dev machine into the HF cache at `/workspace/.hf_home/hub/`. If the instance is
  **recycled**, that cache is wiped and the pretrained arm will fail to download again.
- **`set -e` ordering trap.** `freq_benchmark.sh` runs the **pretrained arm first** under
  `set -euo pipefail`. On an offline box with no cached ImageNet weights, this aborts the whole
  script *before* the scratch arm ever runs. Either pre-seed the HF cache, or run scratch first
  (the 2026-06-19 run used a scratch-first ordering for exactly this reason).

## Deliverables

- **Checkpoints:** `outputs/runs/freq_resnet18_{FFPP,CDF}_n750_seed0_{pretrained,scratch}/best.pt`
- **ROC overlays + CMs + metrics + per-frame preds:** `outputs/roc_cm/freqbench_{FFPP_in,CDF_in,FFPP2CDF,CDF2FFPP}_n750_*.{png,json,csv}`
- **Console log:** `freq_benchmark.log`
- Source AUCs above come from the four `freqbench_*_n750_metrics.json` files.
