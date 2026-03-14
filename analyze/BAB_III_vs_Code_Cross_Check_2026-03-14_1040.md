# BAB III vs Code Implementation: Cross-Check Analysis

**Date:** 2026-03-14
**Scope:** BAB_III_Metodologi_Penelitian.md vs all source code, scripts, config.yaml, and CONCLUSION.md

---

## 1. ACCURACY CHECK: Factual Discrepancies

### 1.1 DISCREPANCY: Default epochs in config.yaml vs BAB III

- **BAB III (line 385):** States "konfigurasi default repositori, jumlah epoch adalah 5" and "eksperimen utama ... menggunakan 10 epoch"
- **config.yaml (line 14):** `epochs: 5`
- **CONCLUSION.md (line 8):** "10 epochs"
- **Verdict:** BAB III is **correct** in acknowledging both values. The config default is 5, and the pipeline overrides to 10 via `--epochs 10`. No discrepancy.

### 1.2 DISCREPANCY: max_frames_per_video default

- **BAB III (line 258):** States "skenario yang didokumentasikan pada command.txt menggunakan maksimum 100 frame per video"
- **config.yaml (line 6):** `max_frames_per_video: 50`
- **run_pipeline.py (line 69):** `--max-frames` default is `50`, not 100
- **BAB III pipeline commands (lines 486-488):** Show `--max-frames 100`
- **Verdict:** **Minor inconsistency.** The config default is 50, and run_pipeline.py default is also 50. BAB III says the documented experiments use 100 (via command line override), which is consistent with the explicit commands shown. However, the config default (50) is not mentioned anywhere in BAB III. This is acceptable as long as the experiment commands override it.

### 1.3 DISCREPANCY: Gradient accumulation steps

- **BAB III (line 393):** "model hybrid dan early_fusion, repositori ini menggunakan gradient accumulation sebanyak 2 langkah secara default. Sementara itu, model spatial dan freq menggunakan 1 langkah."
- **Code (train.py line 144):** `accum_steps = cfg.get("accum_steps", 2 if args.model in {"hybrid", "early_fusion"} else 1)`
- **Verdict:** **Accurate.** BAB III correctly describes the code behavior.

### 1.4 DISCREPANCY: Resize in spatial training transforms

- **BAB III (line 287):** "Resize ke ukuran 256 x 256, yaitu image_size + 32 dari ukuran target 224 x 224"
- **Code (transforms.py line 13):** `transforms.Resize((image_size + 32, image_size + 32))` which is 256x256
- **Verdict:** **Accurate.**

### 1.5 DISCREPANCY: FFT transform uses CenterCrop, not RandomResizedCrop

- **BAB III (section 3.8.6):** Describes the FFT preprocessing procedure (grayscale, resize, FFT, fftshift, log1p, normalize) but does NOT describe the FFT transform applied by the DataLoader during training.
- **Code (transforms.py lines 28-41):** The `get_fft_transform` for training uses `Resize(256x256) + CenterCrop(224)`, while for eval it uses `Resize(224x224)`.
- **Verdict:** **Gap.** BAB III describes how the FFT cache is computed (Section 3.8.6) but omits the runtime FFT transform (CenterCrop for training). This is a minor gap since the cache is the primary representation, but the difference in augmentation strategy between spatial (RandomResizedCrop) and FFT (CenterCrop) is methodologically relevant and should be mentioned.

### 1.6 DISCREPANCY: FFT tensor is bilinearly interpolated at runtime

- **Code (deepfake_data.py lines 93-95):** After loading the FFT cache, the tensor is bilinearly interpolated to `image_size x image_size`: `torch.nn.functional.interpolate(fft_tensor.unsqueeze(0), size=(self.image_size, self.image_size), mode="bilinear", align_corners=False)`
- **BAB III:** Does not mention this interpolation step.
- **Verdict:** **Gap.** This bilinear interpolation of the FFT tensor at runtime is an implementation detail not covered in BAB III. While the FFT is already computed at 224x224, this interpolation acts as a safeguard; it should be mentioned for completeness.

### 1.7 ACCURACY: Video label inference

- **BAB III (section 3.8.1):** Lists the keywords for FFPP and CDF.
- **config.yaml (lines 22-27):** Matches exactly.
- **extract_frames.py (lines 18-26):** `infer_label` checks both parent directory parts and filename.
- **Verdict:** **Accurate.** BAB III says "diinferensi dari nama folder dan nama file" which matches the code.

### 1.8 ACCURACY: Split ratios

- **BAB III (lines 272-276):** 15% test, 15% val, 70% train.
- **build_splits.py (lines 19-20):** `val-size=0.15`, `test-size=0.15`, and the second split correctly computes `val_size / (1 - test_size) = 0.15 / 0.85 ~ 0.1765` to get 15% of total.
- **Verdict:** **Accurate.**

### 1.9 ACCURACY: BCEWithLogitsLoss formula

- **BAB III (lines 379-383):** Shows the standard BCE formula with sigmoid.
- **Code (train.py line 140):** `nn.BCEWithLogitsLoss()`
- **Verdict:** **Accurate.**

### 1.10 ACCURACY: Model architectures

- **FreqCNN (BAB III section 3.9.2):** Conv2D 1->16, BN, ReLU, MaxPool; Conv2D 16->32, BN, ReLU, MaxPool; Conv2D 32->64, BN, ReLU, AdaptiveAvgPool; Flatten, Linear 64->64, ReLU, Dropout(0.2), Linear 64->1.
- **Code (freq_cnn.py):** Matches exactly.
- **Hybrid classifier (BAB III section 3.9.3):** Linear(dim_gabungan, 256), ReLU, Dropout(0.3), Linear(256, 1).
- **Code (hybrid_fusion.py lines 16-20):** Matches exactly.
- **Verdict:** **Accurate.**

### 1.11 ACCURACY: Checkpoint selection criterion

- **BAB III (line 397):** "Nilai validation AUC menjadi dasar pemilihan checkpoint terbaik."
- **Code (train.py lines 153-155):** `if val_metrics["auc"] > best_auc: ... torch.save(...)`
- **Verdict:** **Accurate.**

### 1.12 ACCURACY: Metrics computation

- **BAB III (sections 3.11.1-3.11.5):** Lists accuracy, precision, recall, F1, AUC.
- **Code (metrics.py):** Computes all five plus confusion matrix components (tp, tn, fp, fn). Uses `roc_auc_score` from sklearn.
- **Verdict:** **Accurate.**

### 1.13 DISCREPANCY: Seed value

- **BAB III (line 116):** "1 seed pada hasil yang tersedia di repositori"
- **config.yaml (line 16):** `n_seeds: 1`
- **Code (train.py line 112, build_splits.py line 21, extract_frames.py line 106):** All default to seed=42.
- **BAB III:** Does not explicitly state the seed value (42), only that 1 seed is used.
- **Verdict:** **Minor gap.** For full reproducibility, BAB III should state the seed value is 42.

### 1.14 DISCREPANCY: Kernel size for FreqCNN convolutions

- **BAB III (section 3.9.2):** Says "Conv2D 1 ke 16" but does not specify kernel_size or padding.
- **Code (freq_cnn.py):** Uses `kernel_size=3, padding=1` for all three conv layers.
- **Verdict:** **Minor gap.** Kernel size and padding are standard architectural details that should be mentioned.

---

## 2. COMPLETENESS CHECK

### 2.1 Code features NOT covered in BAB III

| Feature | Code Location | Impact |
|---------|---------------|--------|
| **`seed_everything` function** sets deterministic CUDNN | utils.py lines 15-22 | Reproducibility detail; should be mentioned |
| **`worker_init_fn`** for DataLoader worker seeding | utils.py lines 74-77 | Minor but relevant for reproducibility |
| **`env_info`** logging (hostname, CUDA, torch version) | utils.py lines 84-90 | Minor |
| **Fallback FFT computation** when cache is missing | deepfake_data.py lines 79-81 | Safety mechanism; minor |
| **Early stopping in video scanning** (`early_stop = n_samples * 3`) | extract_frames.py lines 77, 96-100 | Optimization detail; minor |
| **`make_video_id`** uses MD5 hash of path | utils.py lines 62-71 | Relevant for understanding manifest structure |
| **Duplicate video_id check** in build_splits.py | build_splits.py lines 29-35 | Data integrity check; minor |
| **Patched config mechanism** in run_pipeline.py | run_pipeline.py lines 48-57 | Implementation detail of how overrides work |
| **`tensor_fft_logmag` function** (unused tensor-based FFT) | fft_utils.py lines 23-32 | Not used in main pipeline; no impact |
| **`pad_to_size` function** (unused padding utility) | fft_utils.py lines 46-53 | Not used in main pipeline; no impact |

### 2.2 BAB III claims NOT implemented in code

| BAB III Claim | Status |
|---------------|--------|
| All claims verified | No "phantom" features found. Everything BAB III describes exists in the code. |

### 2.3 Missing methodological details that SHOULD be in BAB III

1. **No learning rate scheduler.** BAB III does not discuss this, and the code confirms there is no scheduler (constant learning rate throughout training). This should be explicitly stated as a controlled variable design choice.

2. **No early stopping mechanism.** Training runs for the full number of epochs with no early stopping. The checkpoint is saved based on best validation AUC, but training itself does not stop early. This should be noted.

3. **No data augmentation for frequency branch.** BAB III describes spatial augmentation (RandomResizedCrop, RandomHorizontalFlip) but does not discuss that the FFT branch uses CenterCrop instead of random augmentation. The asymmetry is methodologically significant.

4. **video_id generation mechanism.** BAB III says manifest contains video_id but doesn't explain how video_id is generated (stem + MD5 hash). This matters for understanding that the same video processed twice gets the same ID.

5. **Number of workers.** config.yaml sets `num_workers: 0` but run_pipeline defaults to 4, and BAB III doesn't discuss this parameter.

---

## 3. CONSISTENCY WITH CONCLUSION.md RESULTS

### 3.1 Experiment design match

| Parameter | BAB III | CONCLUSION.md | Match? |
|-----------|---------|---------------|--------|
| Models | spatial, freq, hybrid | Spatial, Frequency, Hybrid | Yes |
| Datasets | FFPP, CDF | FFPP, CDF | Yes |
| Sample sizes | n=50, n=200, n=400 | n=50, n=200, n=400 | Yes |
| Epochs | 10 (for main experiments) | 10 | Yes |
| lr | 1e-4 | 1e-4 | Yes |
| batch_size | 16 | 16 | Yes |
| Optimizer | Adam | Adam | Yes |
| Pretrained | Yes (Xception) | Yes (spatial & hybrid) | Yes |
| Splits | By video ID, stratified | By video ID, stratified | Yes |
| Evaluation types | In-dataset, cross-dataset | In-dataset, cross-dataset | Yes |

### 3.2 Output tables match

- BAB III mentions Table1_in_dataset.csv, Table2_cross_dataset.csv, Table3_generalization_drop.csv
- CONCLUSION.md presents Table 1, Table 2, Table 3 with matching structures
- **Match: Yes**

### 3.3 Generalization drop formula

- BAB III: `Drop = F1_in - F1_cross`
- CONCLUSION.md Table 3 header: "F1_in - F1_cross"
- run_all.py (line 145): `"drop": f1_in - f1_cross`
- **Match: Yes**

### 3.4 CONCLUSION findings consistency with BAB III hypotheses

| BAB III Hypothesis | CONCLUSION Finding | Consistent? |
|--------------------|-------------------|-------------|
| H1: Hybrid has best in-dataset | Hybrid best at n=400 FFPP (F1=0.720) | Yes |
| H2: FFPP training generalizes better | FFPP->CDF generally better than CDF->FFPP | Yes |
| H3: More samples improve in-dataset but not necessarily cross | In-dataset improves n=400, cross degrades | Yes |
| H4: Drop shows dataset sensitivity | Drops increase with n, especially at n=400 | Yes |

---

## 4. MISSING SECTIONS (Typical BAB III for Skripsi)

### 4.1 Sections present and adequate

- [x] Desain Penelitian (3.1)
- [x] Tujuan Metodologis (3.2)
- [x] Lingkungan Implementasi (3.3)
- [x] Data Penelitian dan Sumber Dataset (3.4)
- [x] Variabel Penelitian (3.5)
- [x] Rancangan Eksperimen (3.6) - Very thorough
- [x] Alur Pipeline (3.7)
- [x] Tahap Prapemrosesan Data (3.8)
- [x] Arsitektur Model (3.9)
- [x] Strategi Pelatihan (3.10)
- [x] Metode Evaluasi (3.11)
- [x] Langkah Implementasi (3.12)
- [x] Ringkasan Metodologi (3.13)

### 4.2 Potentially missing sections

1. **Diagram alir (flowchart/figure).** BAB III line 232 acknowledges this: "urutan ini dapat divisualisasikan kembali dalam bentuk diagram alir penelitian." The section suggests it but does not include it. Most skripsi require at least one flowchart in BAB III.

2. **Tabel ringkasan parameter/hyperparameter.** While Section 3.5.3 lists controlled variables, a consolidated table of all hyperparameters (lr, weight_decay, batch_size, epochs, image_size, max_frames, accum_steps, dropout rates, etc.) would strengthen the chapter.

3. **Spesifikasi perangkat keras.** BAB III mentions "lingkungan sistem operasi Windows" and GPU/mixed-precision but does not specify the exact hardware (GPU model, RAM, storage). Most skripsi include this.

4. **Versi pustaka.** BAB III lists libraries but not their versions. Reproducibility best practice would include version numbers (PyTorch version, timm version, etc.).

5. **Xception feature dimension.** BAB III says the Xception feature extractor produces a "vektor fitur spasial" but does not state its dimensionality. The code shows it is determined by `model.num_features` from timm (2048 for Xception). The hybrid classifier input dimension (spatial_dim + freq_dim = 2048 + 64 = 2112) should be stated.

6. **Kernel size for FreqCNN convolutions.** As noted in 1.14, kernel_size=3 and padding=1 are not specified.

---

## 5. OVERALL VERDICT

### Can BAB III be considered "concluded" (final/complete)?

**Near-complete, but not fully finalized.** Here is the assessment:

**Strengths:**
- BAB III is remarkably thorough and well-structured, covering 13 major sections.
- Model architectures are described with high fidelity to the code.
- The experimental design (matrix, hypotheses, procedures) is excellent and well-matched to the actual experiments.
- All major algorithms, formulas, and processes are accurately described.
- No "phantom" features -- everything described exists in the code.
- Consistency with CONCLUSION.md results is strong.

**Required fixes before finalization:**

| Priority | Item | Effort |
|----------|------|--------|
| HIGH | Add at least one flowchart/diagram (referenced but not included) | Medium |
| HIGH | Add hardware specs (GPU model, RAM) | Low |
| MEDIUM | State the seed value (42) explicitly | Trivial |
| MEDIUM | Add FreqCNN kernel_size=3 and padding=1 | Trivial |
| MEDIUM | State Xception feature dimension (2048) and hybrid concat dimension (2112) | Low |
| MEDIUM | Mention that no learning rate scheduler or early stopping is used | Low |
| MEDIUM | Document the FFT augmentation asymmetry (CenterCrop vs RandomResizedCrop) | Low |
| LOW | Add library version numbers | Low |
| LOW | Mention the bilinear interpolation step for FFT tensors | Trivial |
| LOW | Note config default values (max_frames=50, epochs=5) vs experiment overrides more clearly | Low |

**Bottom line:** BAB III is approximately **90% complete**. The textual methodology is accurate and thorough. The main gaps are presentational (missing diagram, missing hardware specs) and a few minor technical details (kernel sizes, feature dimensions, seed value). None of the gaps represent factual errors -- they are omissions. With the fixes above, BAB III would be ready for submission.
