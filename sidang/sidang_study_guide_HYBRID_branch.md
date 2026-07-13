# Hybrid Branch — Study Guide (Late Fusion + SE Gating)

> **Your role:** you own the **hybrid model** — `HybridTwoBranch`, the **fusion design** (projection → concatenation → SE gating → classifier), and the thesis's **headline comparative claim** (the proposed hybrid does **not** beat the spatial baseline). This is a *companion* to `sidang_study_guide_SPATIAL_branch.md`, `sidang_study_guide_FREQUENCY_branch.md`, and `sidang_study_notes_detailed_2026-06-25.md` (Steps 04, 05, 07). It goes **deep only on the fusion**, and includes a **demo section** (§7) for the hybrid-specific things a reviewer can point at live.
>
> **Why your branch carries the thesis:** the hybrid is the *proposed contribution* — and its job at the defense is to lose honestly. "Your proposal is worse than your baseline, so what's the point?" is the single hardest question in the whole sidang, and it's aimed straight at you. You defend it as a **rigorous comparative / ablation result**, not a failed improvement. The title says it: *studi komparatif ... terhadap model domain tunggal.*

---

## 0. The one-liner you defend

> "The hybrid (XceptionNet spatial branch + FreqCNN frequency branch, fused by projection + concatenation + **SE gating**) is our **proposed** model. Its architecture is sound — we balance the two branches to 256-d each and add an SE gate to adaptively weight them. But because the frequency branch is near-random, fusion **injects noise**: the hybrid lands **below** pure spatial in-dataset on both datasets. The one place FFT helps is **reducing the generalization drop FFPP→CDF** — but only in that direction, and at the cost of in-dataset accuracy. So our answer to 'does adding FFT help?' is a **quantified, qualified no** — which is a legitimate comparative finding."

Keep coming back to: **the fusion is well-engineered; the *input* it fuses is weak — so hybrid ≤ spatial, and that IS the measured contribution.**

---

## 1. What to study — ordered curriculum

Each item: *what · why you need it · what to read.* Tick them off.

### ① The full hybrid forward pass — `HybridTwoBranch.forward` (`src/models/hybrid_fusion.py:56-67`) · **1.5 hr · CORE**
You must be able to draw this from memory, with dimensions:

```
RGB (3×224×224) → Xception features → 2048 → spatial_proj: Linear(2048→256)+BN+ReLU → 256 ┐
                                                                                          ├ concat → 512
FFT (1×224×224) → FreqCNN.features → 512  → freq_proj:    Linear(512→256)+BN+ReLU  → 256 ┘
concat(512) → SE gate (channel reweighting) → classifier:
     Dropout(0.5) → Linear(512→128) → ReLU → Dropout(0.5) → Linear(128→1) → 1 logit
```

- Two **independent** branches extract features (`self.spatial(rgb)`, `self.freq.features(fft)`), then fuse **once at the feature level** — that's **late fusion**.
- The spatial branch is Xception's **2048-d** global-avg-pooled feature (num_classes=0 extractor); the freq branch is FreqCNN's **512-d** `.features` output (its classifier head bypassed).
- **~25.9M params** (25,878,570) = spatial extractor 20.8M + FreqCNN 4.2M + projections/SE/head (~0.85M).
- Thesis refs: **§3.4.3 "Model Hybrid HybridTwoBranch"**, **Gambar 3.10** (architecture diagram).

### ② Why project both branches to 256 — the symmetric bottleneck · **45 min · CORE**
This is the "why not just concatenate?" question.
- Raw dims are **wildly asymmetric: spatial 2048 vs freq 512 (a 4:1 ratio).** Concatenating raw would let the 2048-d spatial branch **dominate**, and the gradient reaching the freq branch would shrink to near-nothing.
- **`spatial_proj` / `freq_proj`** each = `Linear(→256) + BatchNorm1d + ReLU`. Projecting **both to 256** (256+256) equalizes their contribution; **BatchNorm** normalizes their scales; the result is a **balanced 512-d vector** the SE gate can weight fairly.
- **This is exactly the fix** for the original collapse (see ⑥): the pre-fix model concatenated 2048:64 directly and the spatial branch swamped everything (~97% spatial). Symmetric projection is *what makes late fusion fair between modalities.* (Thesis: projection eq. 2.15, §2.8.)

### ③ The SE gate — squeeze, excitation, scale (`SEGate`, `hybrid_fusion.py:11-24`) · **1 hr · CORE**
The most likely "explain your fusion mechanism" question. SE-Net is Hu et al. `[38]`.
- It's **channel attention** on the **512-d fused vector** (here each "channel" is a fused feature dimension).
- **Squeeze:** `Linear(512→128)` (reduction=4) summarizes cross-channel interactions into a compact descriptor.
- **Excitation:** `Linear(128→512) → Sigmoid` produces a per-dimension **gate weight in (0,1)**.
- **Scale (reweight):** multiply the fused vector by those gates — `x * gate(x)` (`forward`, line 24).
- **Intent:** let the network **down-weight** the useless frequency dimensions and **up-weight** the good spatial ones, *adaptively per input* — a learned, input-dependent branch weighting. The gate weights are computed from the **whole 512-d vector**, so both domains condition the reweighting (cross-domain interaction).
- **The honest punchline (say it):** in our results the SE gate **fails to fully suppress** the near-random frequency branch, so the hybrid still underperforms pure spatial. *Adding a gate was the right idea; it wasn't enough.* (Thesis worked example: **Gambar/§3.4.3** shows the gate suppressing low-value dims, e.g. gate 0.2–0.3, and keeping high-value dims at ~0.9.)

### ④ Concatenation + SE are *both* used, not alternatives · **30 min · CORE**
A classic reviewer trap: "BAB II says SE beats simple concatenation — but you use concatenation. Contradiction?" **No.**
- Order is **projection → CONCATENATION (512) → SE GATE → classifier**. Concatenation **unites** the two branches into one vector; SE gating **reweights** that vector afterward. They stack.
- "**Simple** concatenation" (the thing BAB II says is weaker) = concat with **no** adaptive weighting, straight into the classifier. Your model is on the **better** side of that comparison: concat **plus** SE gate.
- Analogy: "a plain wall is weak, so we reinforce it with steel." The wall (concat) stays; the steel (SE) is added. Not wall-vs-steel — wall+steel.

### ⑤ Hybrid training mechanics — the 3-group LR and freeze (`scripts/train.py`) · **1 hr · CORE**
The hybrid is the trickiest to train because it mixes a **pretrained** backbone with a **randomly-initialized** freq branch and fusion head. Every choice protects the backbone.

| Choice | Value | Why (rehearse) |
|---|---|---|
| **Backbone freeze** | spatial backbone frozen first **3 epochs**, unfreeze at **epoch 4** (`train.py:26,241-244,279-282`) | Let FreqCNN + projections + SE + classifier stabilize before the pretrained backbone starts moving. If the random parts backprop into the backbone on epoch 1, they corrupt the ImageNet features. |
| **3-group differential LR** | backbone **2e-5** (`base/10`) · **freq branch 5e-5** (`base×0.25`) · fusion head **2e-4** (`base`) (`train.py:206-221`) | Backbone is precious → nudge gently. Freq branch is random → must move, but **not dominate** early gradients. Fusion head is random + on top → learns fastest. A single high LR let the random branches overwrite the backbone — a **documented cause of the original collapse.** |
| **Optimizer** | **AdamW** `[45]` | decoupled weight decay → cleaner regularization. |
| **LR schedule** | linear **warmup 3 ep** → **cosine decay to 1e-6** (`train.py:256-262`) | warmup avoids destabilizing the backbone on step 1; cosine anneals smoothly. |
| **Loss** | `BCEWithLogitsLoss` + **`pos_weight`** + **label smoothing 0.05** | pos_weight handles frame-level class imbalance; smoothing curbs overconfidence on small data. |
| **Consistent hflip on both branches** | one random flip → `TF.hflip(rgb)` **and** `torch.flip(fft, dims=[-1])` (`deepfake_data.py:152-156`) | independent flips would **desync** the RGB and FFT views of the same frame; hybrid disables the transform's own hflip and applies it jointly. |
| **Grad accumulation** | 2 steps · grad clip max-norm 5.0 | stability on small effective batches. |
| **Selection** | best checkpoint by **validation AUC**, patience **12**, max **30** epochs | AUC = threshold-independent, robust selection. |

> **If asked "why three learning rates?"** → "Three parameter groups with three roles: a pretrained backbone I must preserve (lowest LR), a randomly-initialized frequency branch that must learn but not overpower the backbone (mid LR), and a randomly-initialized fusion head that should converge fast (highest LR). One flat LR let the random branches' early gradients wreck the ImageNet features — that was a real failure we fixed."

### ⑥ Hybrid results — memorize your own numbers · **45 min · CORE**
**In-dataset AUC (mean over seeds 0/1/2):**

| | n=250 | n=500 | n=750 |
|---|---|---|---|
| **FFPP hybrid** | 0.540 | 0.616 | **0.644** |
| **CDF hybrid** | 0.787 | 0.839 | **0.919** |
| *(baseline)* FFPP spatial | 0.743 | 0.693 | **0.778** |
| *(baseline)* CDF spatial | 0.914 | 0.945 | **0.971** |

**Ranking is Spatial > Hybrid > Freq on both datasets, at every reliable tier.** The hybrid **loses to its own baseline** — that IS the thesis.

**Cross-dataset, n=750** (AUC / **recall**):

| Direction | Model | AUC | Recall |
|---|---|---|---|
| FFPP→CDF | hybrid | 0.665 | 0.599 |
| FFPP→CDF | spatial | 0.678 | 0.637 |
| CDF→FFPP | hybrid | 0.555 | 0.142 |
| CDF→FFPP | spatial | 0.607 | 0.074 |

**Generalization drop (ΔF1, n=750) — the ONE place hybrid helps:**

| Model | Train | F1 in | F1 cross | Δ |
|---|---|---|---|---|
| spatial | FFPP | 0.705 | 0.614 | +0.091 |
| **hybrid** | **FFPP** | 0.606 | 0.594 | **+0.012 (smallest drop)** |
| spatial | CDF | 0.906 | 0.137 | +0.769 |
| hybrid | CDF | 0.834 | 0.238 | +0.597 |

- **The RM2 nuance (memorize the exact shape):** FFT *does* reduce the generalization drop — **but only FFPP→CDF** (ΔF1 +0.012 vs spatial's +0.091), and it's **bought with a lower in-dataset score** (0.606 vs 0.705). It does **not** hold CDF→FFPP. So FFT helps **inconsistently and at a cost** — the honest answer to RM2.

### ⑦ Why fusion drags the hybrid down — the mechanism · **45 min · CORE**
- The freq branch is **≈ random** (AUC ~0.56, flat val curve from epoch 1 — see the freq guide). Concatenating it **injects noise** into the fused 512-d vector.
- The **SE gate was meant to suppress** that noise but **can't fully** — so fusion ≤ spatial. The thesis says it plainly (§4.2.1, §4.2.3 "Pengaruh Penambahan FFT terhadap Penurunan Performa"): the frequency branch *"cenderung menjadi sumber noise yang menyeret turun performa fusi."*
- **H0 cannot be rejected:** no meaningful cross-dataset generalization gain from FFT (BAB IV §4.2.1, BAB V §5.1).
- **Context — the collapse doc is OLDER than the final model.** `analyze/Hybrid_Model_Collapse_Analysis_2026-03-14_1600.md` describes the **pre-fix** hybrid: raw 2048:64 concat (~97% spatial), per-image FFT min-max norm, no scheduler, no freeze, no differential LR → **catastrophic** cross-dataset collapse (CDF→FFPP F1 = 0.038, AUC 0.506). Your fixes — symmetric 256-d projections, SE gate, 3-group differential LR, freeze-then-unfreeze, cosine schedule, **global FFT z-score**, Youden's-J thresholds — **stopped the catastrophic collapse but did not make frequency informative.** That is precisely the final, honest negative result.

> **If asked "did your fixes accomplish anything?"** → "Yes — they turned a catastrophic collapse (F1 0.038) into a competitive-but-not-better model. They did **not** make frequency discriminative. That localizes the limit to the **domain/representation**, not the training code — which *strengthens* the conclusion."

---

## 2. Reviewer questions most likely aimed at the HYBRID owner

Ranked by likelihood. Answer honestly; frame the negative as a finding.

**HQ1. "Your proposed hybrid is worse than your own baseline. What's the contribution?"** *(certain — the hardest question in the room)*
> "It's a **comparative / ablation study**, not an improvement study. We set out to **measure** the frequency domain's contribution, and the measured answer is: under compressed, face-cropped, cross-dataset conditions, FFT fusion **doesn't help and can inject noise**. A rigorously explained negative result is legitimate science — it falsifies the common 'adding FFT must help' assumption with quantitative evidence, and it stops others walking into the same dead end. The hybrid losing to spatial is a **result**, not a failure of the design."

**HQ2. "Explain your fusion. Why projection + concatenation + SE gating?"** *(almost certain)*
> "Three steps. First **projection**: the branches are 2048-d spatial vs 512-d freq — a 4:1 imbalance that would let spatial dominate — so I project **both to 256-d** with Linear+BN+ReLU to balance scale and contribution. Then **concatenation** into a 512-d vector. Then an **SE gate** — channel attention that squeezes the 512-d vector to 128, excites back to 512 through a sigmoid, and multiplies — to adaptively down-weight useless frequency dimensions and up-weight good spatial ones per input. Finally a dropout-regularized 2-layer classifier."

**HQ3. "What does the SE gate actually do here, and did it work?"** *(certain)*
> "It's input-dependent channel reweighting on the fused vector — squeeze `Linear(512→128)`, excitation `Linear(128→512)→sigmoid`, then `x*gate(x)`. The intent was to let the model suppress the near-random frequency channels. It **partially** does that, but it **can't fully** suppress a branch that's essentially noise, so the hybrid still underperforms spatial. The gate was the right idea and necessary — it just isn't enough to rescue a weak input."

**HQ4. "BAB II says SE gating beats simple concatenation, but you use concatenation. Isn't that a contradiction?"** *(likely trap)*
> "No — we use **both, in sequence**: concatenation unites the two branches, then SE gating reweights the concatenated vector. 'Simple concatenation' means concat with **no** adaptive weighting; our model is the *improved* version, concat **plus** SE gate. So that paragraph endorses our design, it doesn't contradict it."

**HQ5. "Is FFT a 4th channel of XceptionNet?"** *(likely — the early-fusion confusion)*
> "No. In the model we evaluate — **late fusion, HybridTwoBranch** — XceptionNet processes RGB (3-channel) and FreqCNN processes the FFT map (1-channel) in **separate branches**, fused at the **feature level**. The 4-channel 'FFT-as-channel-4' design is **early fusion**; it exists in our code but was **not** part of the evaluation. We chose late fusion so we can pick a different architecture per domain and **isolate each domain's contribution** for the ablation."

**HQ6. "Why does hybrid help FFPP→CDF but not CDF→FFPP?"** *(likely)*
> "Source-dataset diversity. Trained on **FFPP** — four manipulation methods — the model sees varied artifacts and the frequency branch adds a little cross-dataset robustness, shrinking the F1 drop to +0.012 vs spatial's +0.091. Trained on **CDF** — one homogeneous synthesis method — there's less to generalize from, and FFT doesn't help. So the benefit is **real but directional**, and it costs in-dataset accuracy. That asymmetry is the honest RM2 answer, not a contradiction."

**HQ7. "How do you know the hybrid isn't just under-trained or badly fused?"**
> "Because we removed each confound. The freq branch's own power was checked three ways (data sweep plateaus, a 2.6×-bigger ResNet18 stays near chance, verified normalization). The fusion was **rebuilt** from a version that catastrophically collapsed — symmetric projections, SE gate, 3-group LR, freeze/unfreeze, global FFT z-score — and the collapse went away while the near-chance freq contribution **remained**. That tells us the limit is the frequency **input**, not the training or the fusion code."

**HQ8. "Why not weight the branches manually, or drop the freq branch when it's bad?"**
> "That's essentially what the SE gate learns to do — adaptive, per-input weighting — and it still can't lift a noise input. A hard manual down-weight to zero would just recover the spatial model, which is exactly our finding: under these conditions the spatial branch alone is best. We report that instead of hiding it."

**HQ9. "~25.9M parameters for a model that's worse than a 20.8M one — isn't that wasteful?"**
> "Precisely one of our practical conclusions: for **low-resource, frame-based** deepfake detection, the pretrained spatial backbone alone is both the **strongest** and the **most parameter-efficient** choice. Adding the FFT branch adds ~5M parameters and **lowers** accuracy. That's actionable design guidance, and it's only visible because we measured the hybrid honestly."

**HQ10. "Why late fusion and not early fusion?"**
> "Late fusion keeps the two domains **separable**, which is what lets us run the ablation — spatial-only vs freq-only vs hybrid — and attribute the contribution to each domain (RM3). Early fusion mixes RGB and FFT at the input, so you can't isolate the frequency contribution. It's also cleaner architecturally: each domain gets the backbone that suits it."

---

## 3. Hybrid numbers card (keep on your phone)

| | |
|---|---|
| **Architecture** | late fusion: Xception(2048) + FreqCNN(512) → project both to **256** → concat **512** → **SE gate** → classifier |
| **SE gate** | squeeze `Linear(512→128)` (reduction 4) → excite `Linear(128→512)→Sigmoid` → `x*gate(x)` |
| **Classifier** | `Dropout(0.5) → Linear(512,128) → ReLU → Dropout(0.5) → Linear(128,1)` |
| **Params** | **~25.9M** (25,878,570) = spatial 20.8M + freq 4.2M + fusion ~0.85M |
| **3-group LR** | backbone **2e-5** · freq branch **5e-5** (base×0.25) · fusion head **2e-4** · AdamW · warmup 3 → cosine to 1e-6 |
| **Freeze** | spatial backbone frozen 3 ep → unfreeze epoch 4 |
| **In-dataset AUC (n=750)** | FFPP **0.644** · CDF **0.919** — **below spatial (0.778 / 0.971) both** |
| **Cross-dataset (n=750)** | FFPP→CDF AUC 0.665 (recall 0.599) · CDF→FFPP AUC 0.555 (recall 0.142) |
| **Where FFT helps** | ΔF1 FFPP→CDF **+0.012** (smallest drop) vs spatial +0.091 — but only this direction, at lower in-dataset F1 |
| **Threshold (demo)** | **0.229** (Youden's J on FFPP val) |
| **Mechanism** | freq ≈ noise → concat injects noise → SE gate can't fully suppress → hybrid ≤ spatial; **H0 not rejected** |
| **Key citations** | SE-Net/Hu **[38]** · Xception/Chollet **[6]** · ResNet/He **[5]** · SpecXNet/Alam **[13]** · FSBI/Hasanaath **[16]** · AdamW **[45]** · domain shift/Ben-David **[46]** |

---

## 4. If you only have one evening

1. **Draw the full forward pass** with dims (2048 & 512 → 256 & 256 → 512 → SE → head) — HQ2.
2. **Explain the SE gate** (squeeze/excite/scale) *and* say it partially-but-not-fully suppresses the noise — HQ3.
3. **Memorize the n=750 table** (hybrid < spatial both) and the **ΔF1 +0.012 FFPP→CDF** nuance — HQ1, HQ6.
4. **Rehearse the 3-group LR + freeze** rationale — HQ7, and the "concat + SE are both used" rebuttal — HQ4.
5. **Own the negative:** the fusion is well-built; the freq *input* is weak; hybrid ≤ spatial is the measured result. Re-read `sidang_study_notes_detailed_2026-06-25.md` Steps 04, 05, 07.

---

## 5. Literature notes worth keeping (for BAB II/III/V and the Q&A)

In-text numbers below follow the docx; ⚠️ **verify the [N] against Daftar Pustaka** before sidang (fact-check flagged in-text/bibliography desync).

- **Hu et al. `[38]` — Squeeze-and-Excitation Networks.** The SE gate's source. In your BAB II §2.8 it's framed as an **adaptive multi-domain fusion mechanism** — channel attention that suppresses uninformative channels and enhances discriminative ones. Cite for the gate *and* for the "better than simple concatenation" claim (which endorses your concat+SE design).
- **Chollet `[6]` (Xception) · He `[5]` (ResNet).** The two backbones inside the hybrid — depthwise-separable spatial branch, residual `FreqBlock`.
- **SpecXNet (Alam `[13]`) · FSBI (Hasanaath `[16]`).** Dual-domain / freq-enhanced related work — cite as **inspiration**, and be precise: SpecXNet fuses spatial-spectral via **channel split + Fourier attention inside each block**; FSBI uses **frequency-enhanced self-blended images**. **Neither appends FFT as a 4th channel** — don't equate their approach with early fusion.
- **Ben-David et al. `[46]` — domain adaptation theory.** The formal name for the cross-dataset drop the hybrid is trying (and mostly failing) to reduce.
- **AdamW (Loshchilov & Hutter) `[45]`.** The optimizer for all three models.
- For **why the fused input is weak** (the mechanism behind hybrid ≤ spatial), lean on the frequency guide's citations: Durall `[8]`, Mejri `[31]`, Oppenheim&Lim `[25]` / SPSL `[26]`, Geirhos `[28]` / Rahaman `[29]` / Wang `[30]`.

---

## 6. Known quirks to OWN before they're pointed out

- **"early fusion" leftovers in the .docx.** The live Word doc still says "dan early fusion" in a couple of methodology spots (e.g. the freezing paragraph) and once frames FFT as a "4th channel." Those are **being revised** — the evaluated model is **late fusion only** (three models: spatial, freq, hybrid). If a reviewer quotes one, correct it: "that's the unevaluated early-fusion variant; our results are late fusion." (See the fact-check doc, Items 7 & 11.)
- **BatchNorm in the projections needs batch > 1.** `spatial_proj`/`freq_proj` use `BatchNorm1d`; at inference the demo batches all frames together, so it's fine — just know it's there.
- **Freq classifier bypassed.** Inside the hybrid, only `FreqCNN.features` (512-d) is used; the standalone freq classifier head is not part of the hybrid.
- **"SE learns correlations" — don't overclaim.** SE gating is **channel reweighting conditioned on both domains**, not a full pairwise cross-attention / bilinear correlation. Say "adaptive channel weighting conditioned on the fused vector," not "models the full spatial-frequency correlation."
- **Effective batch varies by GPU** in the canonical run (auto-tuned); BAB IV's "batch efektif 32" is the config baseline. If asked, "effective batch was GPU-dependent via auto-tuning; the config baseline is 32."

---

## 7. The demo — the hybrid-specific things a reviewer can point at live

> Pair this with `sidang_study_guide_DEMO_debug.md` (the full operational guide). This section is **only** the hybrid-specific angles. The demo runs all three models side-by-side so the comparison is self-evident — your model is the *proposal*, and it's supposed to sit at or below spatial.

### What is *yours* on screen
- The **hybrid verdict card** — fake-probability bar with a tick at threshold **0.229**. In `inference.predict_video` the hybrid path is `model(rgb_batch, fft_batch)` (it consumes **both** inputs), then `sigmoid(logits).mean()` over frames.
- The comparison itself is the point: **hybrid tracking close to but not above spatial is the thesis made visible** — not a bug.

### Hybrid-specific failure modes (map symptom → cause → what to say)

| Symptom | Cause | What to say |
|---|---|---|
| Hybrid **agrees-but-underperforms** or **loses to** spatial | the finding — freq input is near-noise, SE can't fully suppress it | *"Expected and central to the thesis: the proposed hybrid does not beat the spatial baseline. That's a measured comparative result."* |
| Hybrid card shows **"⚠︎ FFT calibration estimated"** | `fft_stats.json` missing → fallback mean 5.0/std 3.0 (`inference.py:123-133`) | Hybrid **depends on FFT stats** (it has a freq branch). Copy `outputs/fft_cache/FFPP/fft_stats.json` → `checkpoints/`. **Spatial is unaffected.** |
| `RuntimeError: size mismatch` loading `hybrid.pt` | built arch ≠ checkpoint (wrong `freq_depth`/`base_channels`) | The demo reads depth/base from the **checkpoint's embedded config** (`inference.py:65-66`, defaults 5/64). Ensure you copied the right run's `best.pt`. |
| Hybrid **disagrees with both** on an OOD clip | out-of-distribution + a noisy freq branch | *"Models are trained on FFPP crops; other sources are OOD (the caveat banner), and the freq branch adds noise — that's the fusion cost we report."* |

### Reviewer: "change X and show me" (hybrid edit points)
- **"Run just the hybrid"** → keep only the `("hybrid", …)` row in `inference.py` `MODELS_SPEC`; the loop iterates that list.
- **"Use 0.5 threshold instead of 0.229"** → delete/rename `hybrid_threshold.json`; it falls back to 0.5 (`inference.py:118-119`). Good moment to explain Youden's J.
- **Anything touching FFT preprocessing** (fps, crop, high-pass) affects the hybrid's freq branch → say: *"I can change it, but it will no longer match the training distribution, so the numbers stop being comparable to the thesis."*

### The one sentence for the demo
> "Watch the hybrid sit right at or just under the spatial card on every clip — that side-by-side *is* our result: a well-engineered fusion can't turn a near-random frequency input into an improvement, so the honest answer to 'does FFT help?' is no under these conditions."
