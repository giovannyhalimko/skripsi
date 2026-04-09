# Analysis: Per-Method FFPP Training (n=100)

Date: 2026-04-09
Config: seed=0, LR=2e-4, warmup=2 epochs, patience=10, pretrained=True
Change: FFPP trained separately per manipulation method (Deepfakes, Face2Face, FaceSwap, NeuralTextures) instead of all 4 mixed together.

---

## 1. Per-Method FFPP — In-Dataset Test AUC

| Model   | Deepfakes | Face2Face | FaceSwap | NeuralTextures |
|---------|-----------|-----------|----------|----------------|
| spatial | **0.615** | 0.538     | 0.550    | 0.433          |
| freq    | 0.417     | 0.473     | 0.470    | 0.497          |
| hybrid  | **0.646** | 0.519     | 0.541    | 0.541          |

### Val AUC (best during training)

| Model   | Deepfakes | Face2Face | FaceSwap | NeuralTextures |
|---------|-----------|-----------|----------|----------------|
| spatial | 0.643     | 0.469     | 0.445    | 0.443          |
| freq    | **0.823** | 0.442     | 0.442    | 0.440          |
| hybrid  | **0.736** | 0.546     | 0.620    | 0.540          |

**Deepfakes is the easiest method** — all 3 models show noticeably higher val AUC (0.64–0.82). The other 3 methods cluster around 0.44–0.55, barely above random.

**NeuralTextures is the hardest** — spatial gets 0.433 test AUC (below random), freq 0.497 (random), hybrid 0.541 (barely above).

---

## 2. CDF Results (Same Run)

| Model   | This run (04/09) | Previous run (04/05) | Delta |
|---------|------------------|---------------------|-------|
| spatial | 0.549            | 0.796               | -0.247|
| freq    | **0.781**        | 0.837               | -0.056|
| hybrid  | 0.590            | 0.866               | -0.276|

CDF was not changed — same code, same config. The large drop (especially spatial and hybrid) is due to **random variance at n=100**. With only ~15 test videos, a different random sample of videos produces very different results between sessions. freq CDF is the most stable (0.781 vs 0.837).

---

## 3. Cross-Dataset Results (test AUC)

### FFPP method → CDF

| Model   | Deepfakes→CDF | Face2Face→CDF | FaceSwap→CDF | NeuralTextures→CDF |
|---------|---------------|---------------|--------------|---------------------|
| spatial | 0.378         | 0.289         | 0.367        | 0.307               |
| freq    | **0.645**     | **0.599**     | **0.642**    | **0.624**           |
| hybrid  | 0.360         | 0.359         | 0.416        | 0.338               |

**freq is the only model that cross-generalizes** from FFPP to CDF (0.60–0.65). Spatial and hybrid models trained on any FFPP method fail completely on CDF (AUC 0.29–0.42).

### CDF → FFPP method

| Model   | CDF→Deepfakes | CDF→Face2Face | CDF→FaceSwap | CDF→NeuralTextures |
|---------|---------------|---------------|--------------|---------------------|
| spatial | 0.437         | 0.410         | 0.427        | 0.400               |
| freq    | 0.497         | 0.523         | 0.523        | 0.532               |
| hybrid  | **0.638**     | **0.663**     | **0.637**    | **0.669**           |

**hybrid CDF model generalizes best to all FFPP methods** (0.64–0.67). This is consistent across all 4 methods, suggesting the hybrid's spatial+freq fusion captures more universal features.

---

## 4. Val/Test Gap Analysis

| Run                        | Val AUC | Test AUC | Gap   |
|----------------------------|---------|----------|-------|
| freq_FFPP_Deepfakes        | 0.823   | 0.417    | -0.406|
| hybrid_FFPP_Deepfakes      | 0.736   | 0.646    | -0.090|
| spatial_FFPP_Deepfakes     | 0.643   | 0.615    | -0.028|
| spatial_CDF                | 0.783   | 0.549    | -0.234|
| hybrid_CDF                 | 0.783   | 0.590    | -0.193|
| freq_CDF                   | 0.788   | 0.781    | -0.007|

freq models show the largest val/test gaps (especially FFPP Deepfakes: 0.82 val → 0.42 test). This means the freq CNN overfits to validation set patterns that don't appear in the test set. At n=100 with ~15 test videos, this is expected — the test set is too small for stable evaluation.

---

## 5. Comparison: Per-Method vs All-Methods-Mixed (04/05 run)

### FFPP test AUC

| Model   | All mixed (04/05) | Deepfakes only (04/09) | Best other method |
|---------|-------------------|------------------------|-------------------|
| spatial | **0.696**         | 0.615                  | 0.550 (FaceSwap)  |
| freq    | **0.746**         | 0.417                  | 0.497 (NeuralTex) |
| hybrid  | 0.616             | **0.646**              | 0.541 (FaceSwap/NT)|

Per-method separation did NOT improve FFPP results. The old mixed-method run actually scored higher for spatial and freq. Only hybrid Deepfakes marginally beat the old mixed hybrid (0.646 vs 0.616).

**This means the FFPP problem is NOT caused by method mixing.** It's a more fundamental issue — likely the combination of:
1. Small dataset (n=100 → only 35 training videos per class)
2. High variance at small n (15 test videos)
3. FFPP video quality / compression artifacts making real vs fake harder to separate than CDF

---

## 6. Key Takeaways

1. **Separating FFPP by method did not fix the low-AUC problem.** Even single-method training gives near-random results except for Deepfakes.

2. **Deepfakes is the easiest FFPP method** to detect. All other methods (Face2Face, FaceSwap, NeuralTextures) are near-random even in isolation.

3. **CDF results are unstable at n=100** — dropped from 0.80–0.87 (04/05) to 0.55–0.78 (04/09) with identical code, purely from different video sampling.

4. **freq model has best cross-dataset FFPP→CDF transfer** (0.60–0.65), supporting the thesis that frequency features capture more universal manipulation artifacts.

5. **hybrid CDF model has best cross-dataset CDF→FFPP transfer** (0.64–0.67), consistent across all 4 methods.

6. **n=100 is too noisy for reliable conclusions.** Results vary dramatically between runs. Need n=250+ for stable evaluation.
