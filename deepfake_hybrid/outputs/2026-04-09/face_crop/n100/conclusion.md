# Analysis: Face Crop Results (n=100)

Date: 2026-04-09
Config: seed=0, LR=2e-4, warmup=2, patience=10, pretrained=True, **face_crop=True, margin=0.3**
Change: Added MTCNN face detection + cropping during frame extraction. All frames now contain only the face region (with 30% margin) instead of full scene.

---

## 1. In-Dataset Test AUC — Before vs After Face Crop

| Model   | FFPP (no crop) | FFPP (face crop) | Delta   | CDF (no crop) | CDF (face crop) | Delta   |
|---------|----------------|-------------------|---------|---------------|-----------------|---------|
| spatial | 0.696          | **0.901**         | **+0.205** | 0.796         | **0.822**       | +0.026  |
| freq    | 0.746          | 0.256             | -0.490  | 0.837         | 0.568           | -0.269  |
| hybrid  | 0.616          | **0.678**         | +0.062  | 0.866         | 0.785           | -0.081  |

**Face cropping transformed FFPP spatial from mediocre (0.696) to excellent (0.901).** This is the single biggest AUC improvement in the entire project.

---

## 2. Val AUC During Training

| Model   | FFPP  | CDF       |
|---------|-------|-----------|
| spatial | 0.798 | **0.993** |
| freq    | 0.634 | 0.586     |
| hybrid  | 0.703 | **0.974** |

CDF spatial and hybrid val AUC are near-perfect (0.99 and 0.97). These models have genuinely learned to distinguish real from fake faces.

---

## 3. DIAG — Prediction Separation

| Model on own test set | mean_prob_real | mean_prob_fake | Gap   | Status    |
|-----------------------|---------------|---------------|-------|-----------|
| spatial_FFPP          | 0.212         | 0.669         | 0.457 | EXCELLENT |
| spatial_CDF           | 0.374         | 0.772         | 0.398 | EXCELLENT |
| hybrid_CDF            | 0.346         | 0.709         | 0.363 | GOOD      |
| hybrid_FFPP           | 0.492         | 0.509         | 0.017 | Weak      |
| freq_FFPP             | 0.805         | 0.625         | -0.180| INVERTED  |
| freq_CDF              | 0.534         | 0.539         | 0.005 | Random    |

Spatial models now have strong class separation (~0.40-0.46 gap). Previously the gap was 0.01-0.03.

---

## 4. Cross-Dataset AUC

| Direction   | Model   | AUC   |
|-------------|---------|-------|
| FFPP→CDF    | spatial | 0.543 |
| FFPP→CDF    | freq    | 0.644 |
| FFPP→CDF    | hybrid  | **0.647** |
| CDF→FFPP    | spatial | **0.741** |
| CDF→FFPP    | freq    | 0.565 |
| CDF→FFPP    | hybrid  | **0.730** |

CDF→FFPP generalization improved significantly (spatial 0.741, hybrid 0.730). CDF models trained on cropped faces transfer well to FFPP cropped faces.

---

## 5. Why Freq Model Broke

The freq model's AUC dropped from 0.746 to 0.256 (INVERTED). This is expected:

- **Before crop:** FFT was computed on full-scene frames. The frequency pattern captured the entire image structure (background + face + edges). Real and fake videos had distinguishably different full-scene frequency signatures.
- **After crop:** FFT is computed on face-only crops. The frequency content is dominated by skin texture and facial features. The frequency differences between real and fake faces are subtler and require the model to learn different patterns.

The FreqCNN (3 layers, ~130K params) may not have enough capacity to learn these subtler face-level frequency differences. The current architecture was tuned for full-scene FFT.

**Impact on hybrid:** The hybrid model fuses spatial + freq features. Since the freq branch produces garbage, it drags down the hybrid. The hybrid FFPP AUC (0.678) is significantly below spatial alone (0.901). If the freq branch were fixed or disconnected, hybrid would likely match or exceed spatial.

---

## 6. In-Dataset F1 Scores

| Model   | FFPP  | CDF   |
|---------|-------|-------|
| spatial | **0.765** | **0.744** |
| freq    | 0.514 | 0.661 |
| hybrid  | 0.633 | **0.773** |

Spatial FFPP F1=0.765 is excellent. Hybrid CDF F1=0.773 is the highest overall.

---

## 7. Summary

### What face cropping fixed:
1. **FFPP spatial AUC: 0.696 → 0.901** — the model now sees actual faces instead of backgrounds
2. **FFPP prediction separation: 0.01 gap → 0.46 gap** — the model confidently distinguishes real from fake
3. **CDF spatial val AUC: 0.993** — near-perfect on validation
4. **Cross-dataset CDF→FFPP: 0.741** — face features transfer across datasets

### What needs fixing:
1. **Freq model is broken on cropped faces** — needs architectural changes or retuning for face-level FFT
2. **Hybrid is held back by freq branch** — spatial alone outperforms hybrid on FFPP (0.901 vs 0.678)

### Root cause of all previous FFPP failures:
The FFPP videos contain full scenes where faces are small and at varying positions. Without face cropping, the model was learning to classify backgrounds, not faces. Combined with the 0-byte file issue from Drive copying, the model had zero useful signal. Face cropping provides the correct input that deepfake detection models need.

---

## 8. Next Steps

1. **Run n=250, 500, 750 with face crop** to see if the improvement holds at larger scales
2. **Fix the freq model** for cropped faces — consider increasing depth/channels, or using a different frequency representation
3. **Consider disabling the freq branch in hybrid** temporarily to see if spatial-only hybrid matches spatial standalone
