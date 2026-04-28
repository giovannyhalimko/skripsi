# Thesis vs Code — Updates Needed After Training Improvements Branch

**Date:** 2026-04-10
**Branch:** `naomi/training-improvements` (to be merged to master)
**Prior cross-check:** `PDF_Thesis_Cross_Check_2026-04-07_1400.md`

This document lists what changed in the code and what needs updating in the thesis PDF.

---

## 1. Values That Changed Since Last Cross-Check

| Item | Thesis PDF (04/07) | Code Now (04/10) | Thesis Section | Action |
|------|-------------------|-------------------|----------------|--------|
| freq_base_channels | 32 | **64** | BAB III 3.4.2 (FreqCNN architecture) | Update ~700K params → ~2.8M params, channel progression 32→64→128→256→256 → 64→128→256→512→512 |
| Spectral masking probability | 15% | **5%** | BAB III 3.3.3 (Augmentasi Data Frekuensi) | Update "probabilitas 15%" → "probabilitas 5%" |
| Spectral masking band width | h/8 | **h/16** | BAB III 3.3.3 | Update band width description |
| Warmup epochs | 2 | **3** | BAB III 3.5.2 (Learning Rate Schedule) | Update warmup description and Gambar 3.9 (LR curve) |
| FFPP sample sizes | [100,300,600,1000] | **[100,250,500,750]** | BAB III Tabel 3.2 | Update FFPP row to match CDF row |
| Face detection preprocessing | Not mentioned | **MTCNN face crop with 30% margin** | BAB III 3.3.1 (Preprocessing) | **ADD NEW SUBSECTION** (see below) |
| FFT high-pass filter | Not mentioned | **Gaussian high-pass, cutoff=0.15** | BAB III 3.3.2 (FFT computation) | **ADD** to FFT pipeline description |
| Batch size (Colab) | 16 (effective 32) | **64** (effective 128 with accum=2) | BAB III 3.5 | Update for Colab config |

---

## 2. New Content Needed in BAB II (Tinjauan Pustaka)

### 2.1 Face Detection for Deepfake Preprocessing (NEW subsection)

**Where:** After section 2.16 (Praproses Video) or as part of it.

**Content needed:**
- Explain why face detection is a standard preprocessing step in deepfake detection
- Describe MTCNN (Multi-task Cascaded Convolutional Networks) — the 3-stage cascade (P-Net, R-Net, O-Net)
- Cite the original MTCNN paper (Zhang et al., 2016)
- Explain why face cropping improves detection: removes irrelevant background, normalizes face scale/position, focuses model on manipulation region
- Reference that FaceForensics++ and most deepfake detection papers use face cropping

### 2.2 High-Pass Filtering in Frequency Domain (addition to existing section)

**Where:** Section 2.4 (Transformasi Fourier) or 2.5 (Distorsi Spektral)

**Content needed:**
- Explain high-pass filtering concept (attenuate low frequencies, emphasize high frequencies)
- Connect to deepfake detection: manipulation artifacts (blending boundaries, GAN fingerprints) are predominantly in high-frequency components
- Explain Gaussian high-pass mask: `1 - exp(-d²/2σ²)` where d is distance from center

---

## 3. Changes Needed in BAB III (Metodologi)

### 3.1 Section 3.3.1 — Preprocessing: ADD Face Detection Step

**Current flow in thesis:** Video → Frame extraction → (goes to FFT/training)

**New flow:** Video → Frame extraction → **Face detection (MTCNN) → Face cropping (30% margin)** → FFT/training

**Content to add:**
- MTCNN detects faces in each extracted frame
- Largest face selected (by bounding box area)
- Bounding box expanded by 30% margin in each direction
- Cropped to face region, saved as JPEG
- If no face detected, full frame used as fallback
- Sequential processing (MTCNN on GPU, ~50 FPS)
- Add a figure showing: original frame → detected face bbox → cropped face

### 3.2 Section 3.3.2 — FFT Computation: ADD High-Pass Filter

**Current description:** Grayscale → FFT2D → fftshift → log(1+|F|)

**New description:** Grayscale → FFT2D → fftshift → **× high-pass mask** → log(1+|F|)

**Content to add:**
- Gaussian high-pass mask with cutoff σ = 0.15 × image_size
- Purpose: attenuate dominant low-frequency content (overall brightness, face shape) which is similar between real and fake
- Focus model on high-frequency components where manipulation artifacts are more prominent
- Add equation: `H(u,v) = 1 - exp(-d(u,v)² / 2σ²)` where d is distance from frequency center
- Add figure: FFT before vs after high-pass filtering

### 3.3 Section 3.4.2 — FreqCNN Architecture: UPDATE Parameters

**Current in thesis:** depth=5, base_channels=32, ~700K params
**New:** depth=5, base_channels=**64**, ~**2.8M** params

Update:
- Channel progression: 1→64→128→256→512→512 (was 1→32→64→128→256→256)
- Feature dimension: **512** (was 256)
- Update Tabel 3.6 (architecture comparison) parameter count
- Update Gambar 3.7 (FreqCNN diagram) channel numbers

### 3.4 Section 3.3.3 — Augmentasi Data Frekuensi: UPDATE Values

- Spectral masking probability: 15% → **5%**
- Band width: h/8 → **h/16**
- Reason: less aggressive masking preserves critical frequency information for face-level FFT

### 3.5 Section 3.5.2 — Learning Rate Schedule: UPDATE Warmup

- Warmup epochs: 2 → **3**
- Update LR schedule description and Gambar 3.9
- New schedule: epoch 1 at 0.033×LR, epoch 2 at 0.367×LR, epoch 3 at 0.7×LR, epoch 4 at full LR + backbone unfreeze

### 3.6 Tabel 3.2 — Sample Sizes: UPDATE FFPP

- FFPP samples: [100, 300, 600, 1000] → **[100, 250, 500, 750]**
- Now matches CDF: [100, 250, 500, 750]

### 3.7 Section 3.4.4 — Still needs [PERLU ISI] filled (from previous cross-check)

---

## 4. Changes Needed in BAB IV (Hasil dan Pembahasan)

BAB IV is currently empty. When writing it, include these findings from the training improvements:

### 4.1 Face Cropping Impact (key finding)

| Model | FFPP without crop | FFPP with crop | Improvement |
|-------|------------------|----------------|-------------|
| spatial | 0.696 | **0.901** | +0.205 |
| hybrid | 0.616 | **0.678** | +0.062 |
| freq | 0.746 | 0.256 (broken) | See 4.2 |

This should be discussed as a critical preprocessing step. Without face cropping, models learn background features instead of manipulation artifacts.

### 4.2 Frequency Model Limitations on Face Crops

- Freq model peaks at ~0.62 val AUC on face-cropped FFPP
- FFT of cropped faces has limited discriminative power with single-channel grayscale
- High-pass filter stabilized training (prevented inversion) but didn't significantly improve AUC
- This is a genuine limitation worth discussing in the thesis

### 4.3 Cross-Dataset Generalization with Face Crop

- CDF→FFPP spatial: 0.741 (improved from previous ~0.55)
- Face cropping normalizes input across datasets, improving transfer

---

## 5. Items from Previous Cross-Check Still Pending

| Priority | Item | Status |
|----------|------|--------|
| HIGH | Fill [PERLU ISI] in 3.4.4 | Still needed |
| HIGH | Write BAB IV | Still empty |
| HIGH | Write BAB V | Still empty |
| HIGH | Write Abstrak (ID + EN) | Still placeholder |
| MEDIUM | Fix Recall formula (eq 2.25, p.50) | Still wrong (TP/(TP+FP) should be TP/(TP+FN)) |
| MEDIUM | Fix duplicate equation 3.29 | Still duplicated |
| MEDIUM | Fix "tesis" → "skripsi" | Still says "tesis" |

---

## 6. New Files Added to Codebase

| File | Purpose |
|------|---------|
| `src/face_utils.py` | MTCNN face detection + cropping utilities |
| `src/utils.py` → `effective_name()` | Helper for per-method dataset naming |
| `requirements.txt` → `facenet-pytorch` | MTCNN dependency |

---

## 7. Summary: What to Update in Thesis Before Submission

**BAB II (3 additions):**
1. Add MTCNN / face detection subsection
2. Add high-pass filtering explanation to FFT section
3. Cite facenet-pytorch / MTCNN paper

**BAB III (7 updates):**
1. Add face detection preprocessing step (new subsection in 3.3.1)
2. Add high-pass filter to FFT pipeline (update 3.3.2)
3. Update FreqCNN params: base_channels=64, ~2.8M params (update 3.4.2)
4. Update spectral masking: 5%, h/16 (update 3.3.3)
5. Update warmup: 3 epochs (update 3.5.2)
6. Update FFPP sample sizes to [100,250,500,750] (update Tabel 3.2)
7. Fill [PERLU ISI] in 3.4.4

**BAB IV:** Write with new face-crop results as primary data

**BAB V:** Write conclusions based on BAB IV
