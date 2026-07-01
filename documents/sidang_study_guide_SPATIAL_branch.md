# Spatial Branch — Study Guide (XceptionNet)

> **Your role:** you own the **spatial branch** — XceptionNet, ImageNet transfer learning, and the RM1 story (how a pure-spatial detector degrades cross-dataset). This is a *companion* to `sidang_study_notes_detailed_2026-06-25.md` and `PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md`; read those for the full picture. This doc goes **deep only where the spatial branch is concerned**.
>
> **Why your branch is the important one to defend:** the spatial model is the **best model in the whole thesis** (it *beats* the proposed hybrid), and it is the subject of **RM1** (the cross-dataset degradation question). So two of the biggest reviewer targets — "why is your baseline better than your proposal?" and "why does it collapse cross-dataset?" — land on you.

---

## 0. The one-liner you defend

> "The spatial branch (XceptionNet, ImageNet-pretrained) is our **strongest detector** — in-dataset AUC up to **0.97**. But it does **not generalize**: cross-dataset it suffers a **recall collapse** (as low as **0.07**). That collapse is **domain shift**, and it's the *motivation* for adding frequency — which, as we show, doesn't reliably fix it."

Keep coming back to: **spatial = strong but brittle. Brittle = the problem the thesis probes.**

---

## 1. What to study — ordered curriculum

Each item: *what · why you need it · what to read.* Tick them off.

### ① Depthwise-separable convolution — the heart of Xception `[6]` (Chollet) · **~1.5 hr · CORE**
This is the single most likely "explain the architecture" question. You must be able to draw it.

- **Standard conv** mixes **space and channels at once**: one `k×k×C_in` kernel per output channel → cost ≈ `H·W·C_in·C_out·k²`.
- **Depthwise-separable conv factorizes this into two steps:**
  1. **Depthwise:** one `k×k` filter *per input channel*, applied independently — captures **spatial** structure, no channel mixing.
  2. **Pointwise (1×1):** a `1×1×C_in` conv that mixes **channels** — recombines across channels.
- **Cost** ≈ `H·W·C_in·k²` + `H·W·C_in·C_out` → roughly **`1/C_out + 1/k²`** of a standard conv (≈ 8–9× cheaper for `k=3`). Same expressive power, far fewer params/FLOPs.
- **Xception = "Extreme Inception":** Inception hypothesized that cross-channel and spatial correlations can be mapped **separately**; Xception takes that to the limit — *fully* separate them. That's literally what the name means (Extreme Inception).
- **Structure:** Entry flow → Middle flow (8 repeated modules) → Exit flow, with **residual connections** (`[5]` He/ResNet) around most blocks. Ends in global average pooling → 2048-d feature vector.

> **One-sentence answer:** "Xception replaces normal convolution with depthwise-separable convolution — a per-channel spatial filter followed by a 1×1 channel-mixing filter — which decouples spatial and cross-channel learning, cutting cost ~8× while keeping accuracy. It's 'Inception taken to the extreme.'"

**Read:** Chollet 2017 paper abstract + Figure 4 (the module); skim the entry/middle/exit diagram.

### ② Why Xception (and not ResNet / EfficientNet / ViT)? · **30 min · CORE**
- It's the **de-facto baseline for deepfake detection** — the FaceForensics++ paper `[7]` itself benchmarks XceptionNet and it's the reference detector in the field. Choosing it makes your baseline **comparable to the literature**.
- **Efficient** (depthwise-separable) and **ImageNet-pretrained weights are readily available in `timm`** → strong transfer learning on limited data.
- **Honest framing if pushed on ViT/EfficientNet:** "Those may perform comparably or better, but our goal was a **standard, well-established spatial baseline** to isolate the *frequency* contribution — not to win an architecture race. Swapping the backbone is orthogonal to our research question and is named future work."

### ③ Transfer learning & ImageNet pretraining · **45 min**
- **Pretrained = the backbone already learned generic visual features** (edges, textures, shapes) from 1.2M ImageNet images. We **fine-tune** them for real-vs-fake instead of learning from scratch.
- **Why it matters here:** our datasets are *small* (100–750 videos/tier). Training a 20.8M-param net from scratch on that would badly overfit. Transfer learning is what makes small-data training viable.
- **What `pretrained=False` would do:** random init → needs far more data → the demo checkpoints use `pretrained=False` *only* because the saved weights overwrite everything anyway (offline-safe), **not** because training used random init.

### ④ What the spatial branch actually *detects* in a fake face · **45 min · CORE**
Reviewers love "what is your model looking at?" You should have a concrete, physical answer:
- **Blending / boundary seams** — where a swapped face is composited onto the target head (edge of jaw, hairline).
- **Texture inconsistencies** — skin that's too smooth, waxy, or inconsistent pore/wrinkle detail.
- **Warping & geometric artifacts** — subtle distortions around eyes, nose, mouth from face alignment.
- **Color / lighting mismatch** — the face's white balance or shading not matching the scene.
- **Semantic tells** — asymmetric or malformed eyes, teeth, ear/earring inconsistencies.
- **Key point:** these are all **spatial-domain, pixel-level** cues — exactly what a CNN with ImageNet priors is good at. This is *why* spatial beats frequency: the discriminative signal for c23-compressed cropped faces lives in the spatial domain, not the (compression-damaged) high-frequency spectrum.

### ⑤ The spatial code — read it line by line · **30 min**
- `src/models/spatial_xception.py`: three thin wrappers over `timm.create_model("xception", ...)`.
  - `build_xception` → full model, `num_classes=1` (one logit, binary via `BCEWithLogitsLoss`).
  - `build_feature_extractor` → `num_classes=0` returns the **2048-d feature vector** (this is what the *hybrid* consumes).
  - `global_pool="avg"` → global average pooling collapses the final `H×W` feature map to one 2048-vector per image.
  - `in_chans=3` (RGB) for spatial; `in_chans=4` is the early-fusion variant (RGB+FFT).
- **Params: ~20.8M** (exact 20,809,001). *Do not say 22.8M* — the old card was wrong. Offer to run `sum(p.numel() for p in m.parameters())`.
- **Feature dim: 2048.** Input **224×224**, ImageNet normalization (mean `[0.485,0.456,0.406]`, std `[0.229,0.224,0.225]`).

### ⑥ Spatial training mechanics — the choices *you* made · **1 hr · CORE**
These protect the pretrained backbone. All verified in `scripts/train.py`.

| Choice | Value | Why (rehearse) |
|---|---|---|
| **Backbone freeze** | first **3 epochs** frozen, unfreeze at **epoch 4** (`train.py:26,274`) | Let the random classifier head stabilize first. If the head is random and you immediately backprop into the pretrained backbone, the large early gradients **corrupt** the valuable ImageNet features. Freeze → head settles → then gently fine-tune. |
| **Differential LR** | backbone **2e-5** (`base/10`), head **2e-4** (`base`) (`train.py:191,203-204`) | The backbone is pretrained and precious → nudge it *gently*. The head is random → let it learn *fast*. A single high LR would let the random head's gradients overwrite the backbone (a documented cause of the original hybrid collapse). |
| **Optimizer** | **AdamW** `[45]` | Decoupled weight decay → cleaner regularization than Adam-with-L2. |
| **LR schedule** | linear **warmup 3 ep** → **cosine decay to 1e-6** (`train.py:256-262`) | Warmup avoids destabilizing the backbone on step 1; cosine anneal for smooth convergence. |
| **Loss** | `BCEWithLogitsLoss` + **`pos_weight`** + **label smoothing 0.05** | pos_weight handles class imbalance; smoothing prevents over-confident logits on small data. |
| **Regularization** | dropout, RandomResizedCrop / ColorJitter / flip / RandomErasing (train only) | Small datasets overfit fast; augmentation + dropout fight that. Off at inference. |
| **Selection** | best checkpoint by **validation AUC**, patience **12**, max **30** epochs | AUC is threshold-independent → robust model selection. |

> **If asked "why not just train everything at one LR from scratch?"** → "Two reasons: the backbone is *pretrained* (worth preserving) and the head is *random* (needs to move fast). Freeze-then-unfreeze + a 10× lower backbone LR keeps the ImageNet features intact while the head catches up. Training everything hot from step one is exactly what caused our earlier model to collapse."

### ⑦ Spatial results — memorize your own numbers · **45 min · CORE**
**In-dataset AUC, n=750** (mean over seeds 0/1/2):

| Dataset | **Spatial** | Hybrid | Freq |
|---|---|---|---|
| FaceForensics++ | **0.778** | 0.644 | 0.562 |
| Celeb-DF | **0.971** | 0.919 | 0.562 |

Spatial is **#1 on both**, at **every reliable tier (250/500/750)**. The hybrid *loses to your baseline* — that IS the thesis.

**Cross-dataset, n=750** (this is *your* RM1 evidence):

| Direction | AUC | **Recall** | Precision |
|---|---|---|---|
| FFPP→CDF | 0.678 | 0.637 | — |
| **CDF→FFPP** | 0.607 | **0.074** | **0.923** |

- **The recall collapse is your headline finding.** Trained on CDF, tested on FFPP, spatial predicts almost everything **"real"** — recall 0.074 means it *misses ~93% of fakes*. But precision is 0.923: when it *does* say "fake," it's almost always right. **Operational read:** the model became **ultra-conservative** — it only fires "fake" on artifacts identical to CDF's one synthesis method, and FFPP's four different methods don't match, so nearly all fakes slip through as "real."

### ⑧ Domain shift — the theory behind RM1 · **30 min · CORE**
- **Why cross-dataset collapses:** the detector learns the **artifact signature of the specific generators it trained on** (a particular up-sampling pattern, blending seam, compression interaction). A new dataset uses **different generators + capture conditions**, so those learned cues don't transfer. Formal name: **domain shift** (Ben-David et al. `[46]`).
- **The asymmetry explains the direction** (this is the elegant part):
  - Train on **CDF** = *one* homogeneous synthesis method → narrow representation → **fails hard** on FFPP's four methods → **CDF→FFPP is the worst collapse**.
  - Train on **FFPP** = *four* methods → sees varied artifacts → transfers *somewhat* better to CDF.
- So the collapse **direction is a consequence of source-dataset diversity, not randomness.** High in-dataset CDF AUC (0.971) *masks* a brittle, narrow model.

---

## 2. Reviewer questions most likely aimed at the SPATIAL owner

Ranked by likelihood. Answer honestly, frame negatives as findings.

**SQ1. "Explain XceptionNet. What makes it different from a normal CNN?"** *(almost certain)*
> "Its core is the **depthwise-separable convolution**: instead of one kernel mixing space and channels together, it does a per-channel spatial filter (depthwise) then a 1×1 channel-mixing filter (pointwise). This decouples spatial and cross-channel correlations — the 'Extreme Inception' idea — and cuts compute ~8× for 3×3 kernels with no accuracy loss. It's the standard deepfake-detection baseline, used in FaceForensics++ itself. Pretrained on ImageNet, ~20.8M params, outputs a 2048-d feature then one logit."

**SQ2. "Your spatial baseline beats your proposed hybrid. Then what's the point of the thesis?"** *(certain — the hardest one)*
> "That's exactly our finding, and it's why this is a **comparative / ablation study**, not an improvement study. We measured the contribution of the frequency domain and found it's near-random, so adding it doesn't help — it injects noise. A cleanly-measured, well-explained **negative result** is legitimate science: it challenges the common 'adding FFT must help' assumption with quantitative evidence and stops others from repeating the dead end. The spatial branch being strongest is a *result*, not a failure of the design."

**SQ3. "Why does the spatial model collapse cross-dataset — recall 0.074?"** *(certain — this is RM1, yours)*
> "**Domain shift.** The model learns the artifact signature of the generators it trained on. Trained on Celeb-DF — a *single* homogeneous synthesis method — it learns a narrow pattern, then fails on FaceForensics++'s four *different* methods. It becomes ultra-conservative: precision stays 0.923 (when it says fake, it's right) but recall crashes to 0.074 (it misses 93% of fakes it's never seen). This is a fundamental, unsolved problem affecting *all* deepfake detectors — and it's the motivation for asking whether frequency could fix it (RM2)."

**SQ4. "Precision 0.923 but recall 0.074 — what does that actually mean?"**
> "The model almost never *false-alarms* but almost always *misses*. It only labels 'fake' when it sees an artifact matching its training distribution; FFPP's artifacts don't match, so it defaults to 'real.' In a real deployment that's dangerous — a detector that misses 93% of fakes is useless even if its rare 'fake' calls are accurate. It's the quantitative face of domain shift."

**SQ5. "Why freeze the backbone for 3 epochs, then differential learning rates?"**
> "The backbone is ImageNet-pretrained and valuable; the classifier head starts random. If I backprop into the backbone on epoch 1, the head's large random gradients corrupt the pretrained features. So I **freeze** the backbone for 3 epochs to let the head stabilize, then unfreeze and fine-tune with a **10× lower LR on the backbone** (2e-5 vs 2e-4 head) so I nudge it gently instead of overwriting it. Skipping this was a documented cause of our earlier collapse."

**SQ6. "Why Xception and not a newer model — EfficientNet, a ViT?"**
> "Because Xception is the *established* spatial baseline for deepfake detection — used in FaceForensics++ — so our results are comparable to the literature. Our research question is about the **frequency** contribution, not the backbone. A better backbone is orthogonal and named future work; swapping it wouldn't change what we're measuring."

**SQ7. "What visual cues does the spatial model rely on?"**
> "Pixel-level forgery tells: blending seams at the face boundary, texture inconsistencies (over-smooth/waxy skin), warping around eyes/nose/mouth, color and lighting mismatch, and malformed eyes/teeth. These are spatial-domain cues — which is precisely why the spatial branch outperforms the frequency branch on our compressed, cropped faces."

**SQ8. "How do you get one prediction per video from frame-level predictions?"**
> "I run the model per sampled frame, apply sigmoid to each logit, then **average the probabilities across frames** to get one video-level probability, and threshold that. Splits are **by video** (70/15/15), so no video's frames appear in two splits — the metric measures generalization, not memorization."

**SQ9. "With ImageNet pretraining and only hundreds of videos, aren't you overfitting?"**
> "That's the real risk, and it's why we lean on transfer learning (the backbone's features are already learned, we only adapt them), heavy augmentation, dropout, label smoothing, and **early stopping on validation AUC**. We also report across 3 seeds and 4 sample-size tiers — the ranking is stable, so we're not chasing one lucky fit. In-dataset AUC up to 0.97 with clean video-level splits indicates it's learning real cues, and the honest counter-evidence is that it *fails* cross-dataset — which is a generalization result, not an overfitting artifact."

**SQ10. "Why 224×224 and global average pooling?"**
> "224×224 is Xception's ImageNet input size — matching it lets us use the pretrained weights directly. Global average pooling collapses the final feature map to a fixed 2048-vector regardless of spatial layout, which is what the classifier (and the hybrid's fusion) consumes. It also adds mild regularization vs a giant flattened FC."

**SQ11. "Is the spatial collapse evidence that frequency is even more necessary?"** *(a trap — stay honest)*
> "It shows domain shift is a *real, hard* problem — which is our motivation. But our data shows frequency does **not** reliably solve it: freq alone is near-random (~0.56), and the hybrid only reduces the drop in **one** direction (FFPP→CDF) and at the cost of in-dataset accuracy. So the collapse motivates the question, but our answer to 'does FFT fix it' is a qualified no."

---

## 3. Spatial-branch numbers card (keep on your phone)

| | |
|---|---|
| **Backbone** | timm `xception`, ImageNet-pretrained, depthwise-separable conv |
| **Params** | **~20.8M** (20,809,001) — *not* 22.8M |
| **Feature dim** | **2048** (global avg pool) → 1 logit |
| **Input** | 224×224 RGB, ImageNet norm |
| **In-dataset AUC (n=750)** | FFPP **0.778** · CDF **0.971** (best model both) |
| **Cross-dataset** | FFPP→CDF AUC 0.678 (recall 0.637) · **CDF→FFPP AUC 0.607, recall 0.074, precision 0.923** |
| **Freeze** | backbone frozen 3 ep → unfreeze epoch 4 |
| **LR** | backbone **2e-5** (base/10) · head **2e-4** · AdamW · warmup 3 → cosine to 1e-6 |
| **Loss** | BCEWithLogits + pos_weight + label smoothing 0.05 |
| **Selection** | best val AUC · patience 12 · max 30 ep |
| **Key citations** | Xception **[6]** Chollet · FaceForensics++ **[7]** Rössler · ResNet **[5]** He · domain shift **[46]** Ben-David · AdamW **[45]** |

---

## 4. If you only have one evening

1. **Draw depthwise-separable conv** and say why it's ~8× cheaper (SQ1).
2. **Memorize the spatial AUC + the CDF→FFPP recall 0.074 / precision 0.923** and explain domain shift (SQ2, SQ3, SQ4).
3. **Rehearse freeze + differential LR** (SQ5).
4. Re-read `sidang_study_notes_detailed_2026-06-25.md` Steps 04, 05, 07 once for context.

**Guiding principle (same as the team doc):** *jujur > defensif.* Spatial is your strong result; its cross-dataset failure is a *finding*, not an embarrassment. Always land on: **"spatial is strong but brittle — and that brittleness is the problem we set out to study."**
