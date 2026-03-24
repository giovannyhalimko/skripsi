# Thesis Reference Index

> Quick-reference index for all papers in `/thesis_reference/`. Organized by topic with keywords for fast lookup.
> Total: **40 references** (39 PDFs + 1 HTML)

---

## Quick Keyword Lookup

| Keyword | References |
|---|---|
| **deepfake detection** | Aduwala, Afchar (MesoNet), Alam (SpecXNet), Guera, Haliassos, Haq, Hasanaath (FSBI), Kim, Korshunov, Luo, Ma, Mejri, Nguyen, Qian, Rossler (FF++), Sabir, Tan |
| **frequency domain / FFT / DCT** | Alam (SpecXNet), Durall, Giudice (DCT), Kim, Luo, Mejri, Qian, Tan, Zhang |
| **XceptionNet / Xception** | Chollet, Haq, Rossler (FF++) |
| **depthwise separable convolution** | Chollet (Xception), Howard (MobileNet), Sifre |
| **GAN / generative** | Aduwala, Karras (ProGAN), Zhang |
| **spectral artifacts / checkerboard** | Durall, Odena, Zhang |
| **FaceForensics++ dataset** | Rossler, Sabir, Guera |
| **Celeb-DF dataset** | (not directly — use Rossler for cross-dataset context) |
| **transfer learning** | Chollet, He (ResNet), Rossler |
| **CNN architecture** | Chollet (Xception), He (ResNet), Howard (MobileNet), Lecun |
| **RNN / temporal** | Guera, Nguyen, Sabir |
| **image processing fundamentals** | Easton, Gonzalez & Woods |
| **signal processing / Fourier** | Oppenheim, Easton, Gonzalez & Woods |
| **optimizer / gradient descent** | Ruder, Bottou, Robbins |
| **hybrid / multi-domain** | Alam (SpecXNet), Luo, Qian, Tan |
| **generalization / cross-dataset** | Ma, Tan, Luo, Haliassos |
| **upsampling artifacts** | Dai, Durall, Odena |
| **face manipulation methods** | Chadha (overview), Rana (survey), Rao (survey) |
| **survey / review** | Akinrogunde, Chadha, Rana, Rao |
| **legal / societal** | Andira |
| **binary cross-entropy / loss** | Goodfellow (ML basics) |
| **label smoothing** | (general DL — Goodfellow, Lecun) |
| **attention / SE mechanism** | (not directly — Qian uses frequency attention) |
| **self-blended images** | Hasanaath (FSBI) |
| **face forgery / face swap** | Chadha, Korshunov, Rossler |

---

## A. Deepfake Detection — Spatial Domain

### Rossler et al — FaceForensics++
- **File:** `Rossler et al - FaceForensics++_ Learning to Detect Manipulated Facial Images.pdf`
- **Full title:** FaceForensics++: Learning to Detect Manipulated Facial Images
- **Keywords:** FaceForensics++, benchmark dataset, face manipulation, XceptionNet, Face2Face, FaceSwap, Deepfakes, NeuralTextures, binary classification, compression levels (raw/c23/c40)
- **Relevance:** Primary dataset paper. Introduces FF++ dataset used in this thesis. Also benchmarks XceptionNet as strong baseline detector.
- **Use in thesis:** BAB II (dataset description, prior work), BAB III (dataset source, experimental setup)

### Afchar et al — MesoNet
- **File:** `Afchar et al - MesoNet_ a Compact Facial Video Forgery Detection Network.pdf`
- **Full title:** MesoNet: a Compact Facial Video Forgery Detection Network
- **Keywords:** MesoNet, Meso-4, MesoInception, compact CNN, mesoscopic features, face forgery, video forensics, lightweight detection
- **Relevance:** Early compact deepfake detector focusing on mesoscopic (mid-level) features rather than pixel-level or semantic-level.
- **Use in thesis:** BAB II (prior work comparison, lightweight detection approaches)

### Haq — XceptionNet + ResNet-50 Classification
- **File:** `Haq - KLASIFIKASI CEPAT MODEL XCEPTIONNET DAN RESNET-50 PADA VIDEO DEEPFAKE MENGGUNAKAN LOCAL BINARY PATTERN.pdf`
- **Full title:** Klasifikasi Cepat Model XceptionNet dan ResNet-50 pada Video Deepfake Menggunakan Local Binary Pattern
- **Keywords:** XceptionNet, ResNet-50, LBP (Local Binary Pattern), deepfake classification, Indonesian thesis, video deepfake, fast classification
- **Relevance:** Indonesian-language thesis using XceptionNet for deepfake detection — directly comparable methodology.
- **Use in thesis:** BAB II (prior work, XceptionNet application in deepfake context)

### Haliassos et al — Lips Don't Lie
- **File:** `Haliassos et al - Lips Don_t Lie_ A Generalisable and Robust Approach to Face Forgery Detection.pdf`
- **Full title:** Lips Don't Lie: A Generalisable and Robust Approach to Face Forgery Detection
- **Keywords:** lip-based detection, generalization, robustness, face forgery, cross-dataset, mouth region, temporal consistency
- **Relevance:** Focuses on generalization across datasets — relevant to cross-dataset evaluation methodology.
- **Use in thesis:** BAB II (generalization challenge, alternative detection cues)

### Korshunov — DeepFakes: A New Threat
- **File:** `Korshunov - DeepFakes_ a New Threat to Face Recognition_ Assessment and Detection.pdf`
- **Full title:** DeepFakes: a New Threat to Face Recognition? Assessment and Detection
- **Keywords:** face recognition, deepfake threat, assessment, detection baseline, biometric security
- **Relevance:** Establishes deepfake as threat to face recognition systems. Motivation for detection research.
- **Use in thesis:** BAB I (latar belakang, threat motivation), BAB II (prior work)

### Aduwala — Deepfake Detection using GAN Discriminators
- **File:** `Aduwala - Deepfake Detection using GAN Discriminators.pdf`
- **Full title:** Deepfake Detection using GAN Discriminators
- **Keywords:** GAN discriminator, deepfake detection, discriminator reuse, adversarial training, fake detection
- **Relevance:** Repurposes GAN discriminator as detector — alternative approach to CNN-based detection.
- **Use in thesis:** BAB II (alternative detection methods)

### Ma et al — From Specificity to Generality
- **File:** `Ma et al - From Specificity to Generality Revisiting Generalizable Artifacts in Detecting Face Deepfakes.pdf`
- **Full title:** From Specificity to Generality: Revisiting Generalizable Artifacts in Detecting Face Deepfakes
- **Keywords:** generalization, generalizable artifacts, cross-manipulation, universal deepfake features, domain adaptation
- **Relevance:** Directly addresses generalization challenge — why detectors fail on unseen manipulation methods.
- **Use in thesis:** BAB II (generalization problem), BAB IV (interpreting cross-dataset results)

---

## B. Deepfake Detection — Frequency Domain

### Qian et al — Thinking in Frequency
- **File:** `Qian et al - Thinking in Frequency_ Face Forgery Detection by Mining Frequency-aware Clues.pdf`
- **Full title:** Thinking in Frequency: Face Forgery Detection by Mining Frequency-aware Clues
- **Keywords:** frequency-aware, face forgery, frequency clues, DCT, frequency attention, multi-scale frequency, F3-Net
- **Relevance:** **Core reference** — uses frequency analysis for deepfake detection. Demonstrates frequency-domain features complement spatial features.
- **Use in thesis:** BAB I (justification for frequency approach), BAB II (frequency-based detection methods), BAB III (methodology comparison)

### Tan et al — Frequency-Aware Deepfake Detection
- **File:** `Tan et al - Frequency-Aware Deepfake Detection_ Improving Generalizability through Frequency Space Domain Learning.pdf`
- **Full title:** Frequency-Aware Deepfake Detection: Improving Generalizability through Frequency Space Domain Learning
- **Keywords:** frequency-aware, generalizability, frequency space learning, cross-dataset, domain learning, spectral features
- **Relevance:** **Core reference** — frequency domain for improved generalization. Directly relates to thesis hypothesis about hybrid frequency+spatial improving generalization.
- **Use in thesis:** BAB I, BAB II (frequency for generalization), BAB IV (comparing generalization results)

### Mejri et al — Leveraging High-Frequency Components
- **File:** `Mejri et al - Leveraging High-Frequency Components for Deepfake Detection.pdf`
- **Full title:** Leveraging High-Frequency Components for Deepfake Detection
- **Keywords:** high-frequency components, spectral analysis, frequency filtering, deepfake detection, high-pass filtering
- **Relevance:** Shows high-frequency spectral components carry deepfake signatures. Supports FFT magnitude map approach.
- **Use in thesis:** BAB II (frequency artifacts in deepfakes, high-frequency analysis)

### Alam et al — SpecXNet
- **File:** `Alam et al - SpecXNet_ A Dual-Domain Convolutional Network for Robust Deepfake Detection.pdf`
- **Full title:** SpecXNet: A Dual-Domain Convolutional Network for Robust Deepfake Detection
- **Keywords:** dual-domain, spatial+spectral, SpecXNet, robust detection, two-branch, fusion, XceptionNet variant
- **Relevance:** **Most directly comparable** — dual-domain (spatial+spectral) CNN for deepfake detection. Similar hybrid concept to this thesis.
- **Use in thesis:** BAB II (closely related work), BAB III (architecture comparison), BAB IV (result comparison)

### Luo et al — Frequency-Domain Masking
- **File:** `Luo et al - Frequency-Domain Masking and Spatial Interaction for Generalizable Deepfake Detection.pdf`
- **Full title:** Frequency-Domain Masking and Spatial Interaction for Generalizable Deepfake Detection
- **Keywords:** frequency masking, spatial interaction, generalizable detection, cross-domain, frequency-spatial fusion
- **Relevance:** Combines frequency masking with spatial interaction for generalization. Another hybrid frequency+spatial approach.
- **Use in thesis:** BAB II (hybrid approaches, generalization)

### Giudice et al — GAN DCT Anomalies
- **File:** `Giudice et al - Fighting Deepfakes by Detecting GAN DCT Anomalies.pdf`
- **Full title:** Fighting Deepfakes by Detecting GAN DCT Anomalies
- **Keywords:** DCT (Discrete Cosine Transform), GAN anomalies, frequency artifacts, DCT coefficients, spectral forensics
- **Relevance:** Uses DCT (related to FFT) to detect GAN-generated images. Demonstrates frequency-domain anomalies in GAN outputs.
- **Use in thesis:** BAB II (DCT vs FFT comparison, frequency artifact types)

### Kim et al — Beyond Spatial Frequency
- **File:** `Kim et al - Beyond Spatial Frequency_ Pixel-wise Temporal Frequency-based Deepfake Video Detection.pdf`
- **Full title:** Beyond Spatial Frequency: Pixel-wise Temporal Frequency-based Deepfake Video Detection
- **Keywords:** temporal frequency, pixel-wise, video detection, beyond spatial, temporal inconsistency, video-level
- **Relevance:** Extends frequency analysis to temporal domain (frame-to-frame). Contrasts with our frame-level spatial frequency approach.
- **Use in thesis:** BAB II (temporal vs spatial frequency analysis)

### Hasanaath — FSBI
- **File:** `Hasanaath - FSBI_ Deepfakes Detection with Frequency Enhanced Self-Blended Images.pdf`
- **Full title:** FSBI: Deepfakes Detection with Frequency Enhanced Self-Blended Images
- **Keywords:** self-blended images, frequency enhancement, data augmentation, SBI, training strategy, blending artifacts
- **Relevance:** Uses frequency-enhanced training data to improve detection. Novel augmentation approach.
- **Use in thesis:** BAB II (frequency-enhanced training strategies)

---

## C. Deepfake Detection — Temporal / Video-Level

### Guera et al — Deepfake Video Detection Using RNN
- **File:** `Guera et al - Deepfake Video Detection Using Recurrent Neural Networks.pdf`
- **Full title:** Deepfake Video Detection Using Recurrent Neural Networks
- **Keywords:** RNN, recurrent neural network, video-level detection, temporal features, frame sequence, CNN+RNN pipeline
- **Relevance:** CNN extracts per-frame features → RNN models temporal inconsistencies. Contrasts with our frame-level approach.
- **Use in thesis:** BAB II (temporal detection methods, justification for frame-level approach)

### Nguyen et al — Spatio-temporal Features
- **File:** `Nguyen et al - Learning Spatio-temporal features to detect manipulated facial videos.pdf`
- **Full title:** Learning Spatio-temporal features to detect manipulated facial videos
- **Keywords:** spatio-temporal, manipulated video, temporal learning, video forensics, sequence modeling
- **Relevance:** Combines spatial and temporal features. Relates to our spatial+frequency hybrid but in temporal dimension.
- **Use in thesis:** BAB II (spatio-temporal approaches, comparison with our spatial+frequency)

### Sabir 2019 — Recurrent Convolutional Strategies
- **File:** `Sabir 2019.pdf`
- **Full title:** Recurrent Convolutional Strategies for Face Manipulation Detection in Videos
- **Authors:** Ekraam Sabir, Jiaxin Cheng, Ayush Jaiswal, Wael AbdAlmageed, Iacopo Masi, Prem Natarajan (USC)
- **Keywords:** recurrent convolutional, face manipulation, video detection, FaceForensics++, temporal, RNN+CNN, face preprocessing
- **Relevance:** CNN+RNN on FaceForensics++. State-of-the-art video-level detection using temporal modeling.
- **Use in thesis:** BAB II (video-level approaches, FF++ benchmark results)

---

## D. Deepfake Surveys & Overviews

### Chadha et al — Deepfake: An Overview
- **File:** `Chadha et al - Deepfake_ An Overview (page 559).pdf`
- **Full title:** Deepfake: An Overview
- **Keywords:** deepfake overview, survey, face swap, face reenactment, generation methods, detection methods, GAN, autoencoder, taxonomy
- **Relevance:** Comprehensive overview of deepfake generation and detection landscape. Good for BAB I/II context.
- **Use in thesis:** BAB I (latar belakang), BAB II (taxonomy of deepfake methods)

### Rana et al — Deepfake Detection: Systematic Review
- **File:** `Rana et al - Deepfake Detection_ A Systematic Literature Review.pdf`
- **Full title:** Deepfake Detection: A Systematic Literature Review
- **Keywords:** systematic review, detection taxonomy, literature survey, detection challenges, benchmark comparison, evaluation methods
- **Relevance:** Systematic literature review of detection methods. Useful for positioning our work in the field.
- **Use in thesis:** BAB I, BAB II (prior work landscape)

### Rao et al — Chronological Review
- **File:** `Rao et al - A Chronological Review of Deepfake Detection_ Techniques and Evolutions.pdf`
- **Full title:** A Chronological Review of Deepfake Detection: Techniques and Evolutions
- **Keywords:** chronological review, evolution of detection, technique progression, detection timeline, historical development
- **Relevance:** Traces evolution of detection techniques over time. Contextualizes our approach in the timeline.
- **Use in thesis:** BAB I, BAB II (historical context)

### Andira et al — Deepfake Crimes in Indonesia
- **File:** `Andira et al - Overcoming Deepfake Porn Crimes In Indonesia.pdf`
- **Full title:** Overcoming Deepfake Porn Crimes In Indonesia
- **Keywords:** Indonesia, deepfake crime, pornography, legal, regulation, societal impact, law enforcement
- **Relevance:** Indonesian legal context for deepfake threats. Motivation for detection research in local context.
- **Use in thesis:** BAB I (latar belakang — Indonesian context, societal motivation)

---

## E. GAN & Generative Artifacts

### Karras et al — Progressive Growing of GANs
- **File:** `Karras et al - Progressive Growing of GANs for Imrpoved Quality, Stability, and Variation.pdf`
- **Full title:** Progressive Growing of GANs for Improved Quality, Stability, and Variation
- **Keywords:** ProGAN, progressive training, GAN, high-resolution face generation, face synthesis, image quality
- **Relevance:** Key GAN architecture for face generation. Understanding how fakes are created helps design detectors.
- **Use in thesis:** BAB II (GAN-based face generation methods)

### Odena et al — Deconvolution and Checkerboard Artifacts
- **File:** `Odena et al - Deconvolution and Checkerboard Artifacts.pdf`
- **Full title:** Deconvolution and Checkerboard Artifacts
- **Keywords:** checkerboard artifacts, deconvolution, transposed convolution, upsampling, artifact patterns, spectral artifacts
- **Relevance:** **Key reference** — explains why GANs produce checkerboard artifacts detectable in frequency domain. Directly motivates FFT-based detection.
- **Use in thesis:** BAB II (why frequency analysis works — GAN upsampling creates spectral artifacts)

### Durall et al — Watch your Up-Convolution
- **File:** `Durall et al - Watch your Up-Convolution_ CNN Based Generative Deep Neural Networks are Failing to Reproduce Spectral Distributions.pdf`
- **Full title:** Watch your Up-Convolution: CNN Based Generative Deep Neural Networks are Failing to Reproduce Spectral Distributions
- **Keywords:** spectral distribution, up-convolution, generative CNN, frequency failure, spectral rolloff, high-frequency deficit, spectral analysis
- **Relevance:** **Key reference** — demonstrates that GANs fail to reproduce correct spectral distributions. High-frequency components are systematically wrong in generated images. Core justification for FFT approach.
- **Use in thesis:** BAB II (spectral distortion in deepfakes, frequency artifact theory)

### Zhang et al — Detecting and Simulating GAN Artifacts
- **File:** `Zhang et al - Detecting and Simulating Artifacts in GAN Fake Images (Extended Version).pdf`
- **Full title:** Detecting and Simulating Artifacts in GAN Fake Images (Extended Version)
- **Keywords:** GAN artifacts, artifact simulation, frequency artifacts, spectral analysis, fake image detection, artifact patterns
- **Relevance:** Analyzes and simulates GAN-specific artifacts. Shows artifacts are detectable in frequency domain.
- **Use in thesis:** BAB II (GAN artifact types, frequency-domain evidence)

### Dai et al — Affinity-Aware Upsampling
- **File:** `Dai et al - Learning Affinity-Aware Upsampling for Deep Image Matting.pdf`
- **Full title:** Learning Affinity-Aware Upsampling for Deep Image Matting
- **Authors:** Yutong Dai, Hao Lu, Chunhua Shen (University of Adelaide / Huazhong University)
- **Keywords:** upsampling, affinity-aware, bilinear upsampling, image matting, feature map upsampling, A2U
- **Relevance:** Upsampling technique in deep networks. Related to understanding upsampling artifacts in GAN-generated images.
- **Use in thesis:** BAB II (upsampling methods and their artifacts)

---

## F. CNN Architectures

### Chollet — Xception
- **File:** `Chollet - Xception_ Deep Learning with Depthwise Separable Convolutions.pdf`
- **Full title:** Xception: Deep Learning with Depthwise Separable Convolutions
- **Keywords:** Xception, XceptionNet, depthwise separable convolution, Inception, channel-wise convolution, ImageNet, efficient architecture
- **Relevance:** **Core architecture paper** — XceptionNet is the spatial backbone in all thesis models. Must be cited for architecture description.
- **Use in thesis:** BAB II (XceptionNet architecture), BAB III (model architecture section)

### He et al — ResNet
- **File:** `He et al - Deep Residual Learning for Image Recognition.pdf`
- **Full title:** Deep Residual Learning for Image Recognition
- **Keywords:** ResNet, residual learning, skip connections, deep networks, ImageNet, vanishing gradient, identity mapping
- **Relevance:** Foundational deep learning architecture. Referenced for comparison and as alternative backbone.
- **Use in thesis:** BAB II (CNN architectures, residual connections)

### Howard et al 2017 — MobileNets
- **File:** `Howard 2017.pdf`
- **Full title:** MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications
- **Authors:** Andrew G. Howard, Menglong Zhu, Bo Chen, Dmitry Kalenichenko et al. (Google)
- **Keywords:** MobileNet, depthwise separable convolution, mobile CNN, efficient inference, width multiplier, resolution multiplier, lightweight
- **Relevance:** Popularized depthwise separable convolutions (used in XceptionNet). Reference for efficient CNN design.
- **Use in thesis:** BAB II (depthwise separable convolution explanation, efficient architectures)

### Sifre & Mallat 2014 — Rigid-Motion Scattering
- **File:** `Sifre 2014.pdf`
- **Full title:** Rigid-Motion Scattering for Texture Classification
- **Authors:** Laurent Sifre, Stephane Mallat (Ecole Polytechnique / ENS)
- **Keywords:** depthwise separable convolution (origin), scattering transform, wavelet, texture classification, rigid-motion invariant, factorized convolution
- **Relevance:** **Origin paper** for depthwise separable convolutions — foundational reference for XceptionNet's core operation.
- **Use in thesis:** BAB II (depthwise separable convolution origin/citation)

---

## G. Deep Learning Fundamentals

### LeCun et al — Deep Learning
- **File:** `Lecun et al - Deep learning.pdf`
- **Full title:** Deep Learning (Nature review)
- **Keywords:** deep learning, neural networks, backpropagation, convolutional networks, representation learning, supervised learning, overview
- **Relevance:** Seminal deep learning overview. General reference for CNN concepts, backpropagation, representation learning.
- **Use in thesis:** BAB II (deep learning fundamentals, CNN theory)

### Goodfellow et al — Machine Learning Basics
- **File:** `goodfellow et al - machine learning basics.html`
- **Full title:** Machine Learning Basics (from Deep Learning textbook)
- **Keywords:** machine learning, supervised learning, loss functions, cross-entropy, regularization, overfitting, underfitting, bias-variance, optimization basics
- **Relevance:** Textbook reference for ML fundamentals — loss functions (BCE), regularization, training methodology.
- **Use in thesis:** BAB II (loss function theory, regularization, training fundamentals)

---

## H. Optimization

### Ruder et al — Gradient Descent Optimization Overview
- **File:** `Ruder et al - An overview of gradient descent optimization.pdf`
- **Full title:** An Overview of Gradient Descent Optimization Algorithms
- **Keywords:** gradient descent, SGD, Adam, AdaGrad, RMSProp, momentum, adaptive learning rate, optimizer comparison, convergence
- **Relevance:** Comprehensive optimizer survey. Reference for Adam optimizer choice and comparison with alternatives.
- **Use in thesis:** BAB II (optimizer section — Adam explanation and justification)

### Bottou et al — SGD Tricks
- **File:** `bottou et al - stochastic gradient descent tricks.pdf`
- **Full title:** Stochastic Gradient Descent Tricks
- **Keywords:** SGD, stochastic gradient descent, learning rate schedule, mini-batch, convergence tricks, practical tips
- **Relevance:** Practical SGD guidance. Reference for learning rate scheduling concepts.
- **Use in thesis:** BAB II (optimization theory, learning rate scheduling)

### Robbins et al — Stochastic Approximation
- **File:** `robbins et al - a stochastic approximation method.pdf`
- **Full title:** A Stochastic Approximation Method
- **Keywords:** stochastic approximation, Robbins-Monro, convergence theory, iterative optimization, foundational statistics
- **Relevance:** Foundational paper for stochastic optimization. Historical citation for SGD theory.
- **Use in thesis:** BAB II (historical reference for optimization theory)

---

## I. Image & Signal Processing

### Gonzalez & Woods — Digital Image Processing (4th Ed.)
- **File:** `Gonzalez,Woods-Digital.Image.Processing.4th.Edition.pdf`
- **Full title:** Digital Image Processing, 4th Edition
- **Keywords:** image processing, Fourier transform, DFT, 2D FFT, frequency domain, spatial filtering, image enhancement, convolution, morphology, segmentation
- **Relevance:** **Key textbook** — reference for FFT theory, 2D Fourier transform, frequency domain concepts, magnitude spectrum, log scaling.
- **Use in thesis:** BAB II (Fourier transform theory, frequency domain fundamentals), BAB III (FFT computation methodology)

### Easton Jr — Fundamentals of Image Processing
- **File:** `Easton Jr - Fundamentals of Image Processing.pdf`
- **Full title:** Fundamentals of Image Processing
- **Keywords:** image processing fundamentals, spatial domain, frequency domain, filtering, transforms, image analysis basics
- **Relevance:** Supplementary image processing reference. Covers spatial and frequency domain basics.
- **Use in thesis:** BAB II (image processing fundamentals)

### Oppenheim et al — Discrete-Time Signal Processing
- **File:** `Oppenheim et al - Discrete-Time Signal Processing.pdf`
- **Full title:** Discrete-Time Signal Processing
- **Keywords:** DFT, FFT, discrete Fourier transform, signal processing, spectral analysis, windowing, sampling theorem, z-transform, filter design
- **Relevance:** **Key textbook** — authoritative reference for DFT/FFT algorithms, spectral analysis theory, discrete-time signal processing.
- **Use in thesis:** BAB II (FFT algorithm theory, DFT formula derivation)

---

## J. Other / Tangential

### Akinrogunde et al — ML for Energy Prediction
- **File:** `Akinrogunde et al - A systematic review of machine learning and deep_learning approaches for load and energy consumption_prediction in contemporary power systems.pdf`
- **Full title:** A Systematic Review of ML and DL Approaches for Load and Energy Consumption Prediction in Contemporary Power Systems
- **Authors:** Oluwadare Olatunde Akinrogunde et al. (Ogun State Institute of Technology, Nigeria)
- **Keywords:** systematic review, CNN, LSTM, Transformer, energy forecasting, power systems, ML comparison
- **Relevance:** Tangential — general ML/DL survey. May be cited for CNN/LSTM architecture overview in non-vision context.
- **Use in thesis:** BAB II (general DL method comparison, if needed)

---

## By Chapter Usage

### BAB I — Latar Belakang & Rumusan Masalah
| Purpose | References |
|---|---|
| Deepfake threat/motivation | Korshunov, Chadha (overview), Andira (Indonesia) |
| Why detection is needed | Rana (survey), Rao (chronological review) |
| Why frequency domain | Qian, Tan, Durall, Mejri |
| Why hybrid approach | Alam (SpecXNet), Luo |

### BAB II — Tinjauan Pustaka
| Topic | References |
|---|---|
| Deepfake generation (GAN) | Karras (ProGAN), Chadha (overview) |
| GAN artifacts & spectral distortions | Odena (checkerboard), Durall (spectral), Zhang (GAN artifacts), Dai (upsampling) |
| CNN fundamentals | LeCun (deep learning), He (ResNet) |
| XceptionNet architecture | Chollet (Xception) |
| Depthwise separable convolution | Chollet, Howard (MobileNet), Sifre (origin paper) |
| Fourier transform / FFT | Gonzalez & Woods, Oppenheim, Easton |
| Deepfake detection — spatial | Rossler (FF++), Afchar (MesoNet), Haq (XceptionNet+LBP) |
| Deepfake detection — frequency | Qian, Tan, Mejri, Giudice (DCT), Kim (temporal freq) |
| Deepfake detection — hybrid/dual | Alam (SpecXNet), Luo, Hasanaath (FSBI) |
| Deepfake detection — temporal | Guera (RNN), Nguyen, Sabir |
| Generalization / cross-dataset | Ma, Haliassos, Tan, Luo |
| Optimizer (Adam) | Ruder (overview), Bottou (SGD tricks), Robbins (stochastic approx) |
| Loss function (BCE) | Goodfellow (ML basics) |
| Prior surveys | Rana, Rao, Chadha, Akinrogunde |

### BAB III — Tahapan Pelaksanaan
| Topic | References |
|---|---|
| Dataset (FaceForensics++) | Rossler |
| FFT methodology | Gonzalez & Woods, Oppenheim |
| XceptionNet architecture | Chollet |
| Depthwise separable conv | Chollet, Howard, Sifre |
| Frequency artifacts justification | Durall, Odena, Zhang |
| Optimizer choice | Ruder |
| Evaluation metrics | Goodfellow |

### BAB IV — Hasil dan Pembahasan
| Topic | References |
|---|---|
| Result comparison | Rossler (FF++ baselines), Alam (SpecXNet), Qian, Tan |
| Generalization analysis | Ma, Haliassos, Tan, Durall |
| Frequency artifact discussion | Durall, Odena, Mejri, Zhang |

---

## Alphabetical File List

| # | Filename | Short ID |
|---|---|---|
| 1 | `Aduwala - Deepfake Detection using GAN Discriminators.pdf` | Aduwala |
| 2 | `Afchar et al - MesoNet_ a Compact Facial Video Forgery Detection Network.pdf` | Afchar (MesoNet) |
| 3 | `Akinrogunde et al - A systematic review of machine learning and deep_learning approaches...pdf` | Akinrogunde |
| 4 | `Alam et al - SpecXNet_ A Dual-Domain Convolutional Network...pdf` | Alam (SpecXNet) |
| 5 | `Andira et al - Overcoming Deepfake Porn Crimes In Indonesia.pdf` | Andira |
| 6 | `Chadha et al - Deepfake_ An Overview (page 559).pdf` | Chadha |
| 7 | `Chollet - Xception_ Deep Learning with Depthwise Separable Convolutions.pdf` | Chollet (Xception) |
| 8 | `Dai et al - Learning Affinity-Aware Upsampling for Deep Image Matting.pdf` | Dai |
| 9 | `Durall et al - Watch your Up-Convolution...pdf` | Durall |
| 10 | `Easton Jr - Fundamentals of Image Processing.pdf` | Easton |
| 11 | `Giudice et al - Fighting Deepfakes by Detecting GAN DCT Anomalies.pdf` | Giudice |
| 12 | `Gonzalez,Woods-Digital.Image.Processing.4th.Edition.pdf` | Gonzalez & Woods |
| 13 | `Guera et al - Deepfake Video Detection Using Recurrent Neural Networks.pdf` | Guera |
| 14 | `Haliassos et al - Lips Don_t Lie...pdf` | Haliassos |
| 15 | `Haq - KLASIFIKASI CEPAT MODEL XCEPTIONNET...pdf` | Haq |
| 16 | `Hasanaath - FSBI_ Deepfakes Detection with Frequency Enhanced Self-Blended Images.pdf` | Hasanaath (FSBI) |
| 17 | `He et al - Deep Residual Learning for Image Recognition.pdf` | He (ResNet) |
| 18 | `Howard 2017.pdf` | Howard (MobileNet) |
| 19 | `Karras et al - Progressive Growing of GANs...pdf` | Karras (ProGAN) |
| 20 | `Kim et al - Beyond Spatial Frequency...pdf` | Kim |
| 21 | `Korshunov - DeepFakes_ a New Threat to Face Recognition...pdf` | Korshunov |
| 22 | `Lecun et al - Deep learning.pdf` | LeCun |
| 23 | `Luo et al - Frequency-Domain Masking and Spatial Interaction...pdf` | Luo |
| 24 | `Ma et al - From Specificity to Generality...pdf` | Ma |
| 25 | `Mejri et al - Leveraging High-Frequency Components for Deepfake Detection.pdf` | Mejri |
| 26 | `Nguyen et al - Learning Spatio-temporal features...pdf` | Nguyen |
| 27 | `Odena et al - Deconvolution and Checkerboard Artifacts.pdf` | Odena |
| 28 | `Oppenheim et al - Discrete-Time Signal Processing.pdf` | Oppenheim |
| 29 | `Qian et al - Thinking in Frequency...pdf` | Qian |
| 30 | `Rana et al - Deepfake Detection_ A Systematic Literature Review.pdf` | Rana |
| 31 | `Rao et al - A Chronological Review of Deepfake Detection...pdf` | Rao |
| 32 | `Rossler et al - FaceForensics++...pdf` | Rossler (FF++) |
| 33 | `Ruder et al - An overview of gradient descent optimization.pdf` | Ruder |
| 34 | `Sabir 2019.pdf` | Sabir |
| 35 | `Sifre 2014.pdf` | Sifre |
| 36 | `Tan et al - Frequency-Aware Deepfake Detection...pdf` | Tan |
| 37 | `Zhang et al - Detecting and Simulating Artifacts in GAN Fake Images...pdf` | Zhang |
| 38 | `bottou et al - stochastic gradient descent tricks.pdf` | Bottou |
| 39 | `goodfellow et al - machine learning basics.html` | Goodfellow |
| 40 | `robbins et al - a stochastic approximation method.pdf` | Robbins |
