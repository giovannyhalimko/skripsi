# Demo Video Presentation Script

**Target length:** ~10 minutes (including intro & outro)
**Format:** screen recording of the Gradio demo + voiceover.
**Pacing note:** the narration below is ~1,400 words ≈ 10 min at a calm 140 wpm. `[SCREEN: …]` cues tell you what to show; the plain text is what you say. Time markers are cumulative targets, not hard cuts.

---

## 0 · Intro — who, what, why (0:00 – 1:00)

> `[SCREEN: title slide or the demo's landing page, before uploading anything.]`

Hi, my name is **[name]**, and this is a walkthrough of the interactive demo built for my thesis on **deepfake detection**.

The thesis asks one question: if you take a strong image-based detector and *add* a frequency-domain branch to it, does the combined "hybrid" model actually detect deepfakes better? This demo is how I make that question — and its answer — something you can *see* rather than just read in a results table.

The way it works is simple: you upload a short face video, and the app runs **three different models** on the exact same frames, then shows their verdicts side by side. Over the next few minutes I'll upload a clip, walk through what happens to it internally, and explain what every part of the screen is telling us.

---

## 1 · The three models being compared (1:00 – 2:00)

> `[SCREEN: scroll to the small table at the top of the page — Spatial / Hybrid / Frequency.]`

Before I upload anything, here are the three models, because the whole demo is a comparison between them.

The first is the **Spatial model — XceptionNet**. It looks at the raw RGB pixels of the face, nothing else. This is my **baseline**: a well-established convolutional network for deepfake detection.

The second is the **Hybrid model — this is my thesis's proposal**. It takes the same RGB image *and* a frequency-domain map of that image, and fuses the two together. The idea is that deepfake generators leave subtle, periodic artifacts that are easier to spot in the frequency domain than in the pixels.

The third is the **Frequency-only model**. It sees *only* the frequency map — no pixels at all. It's there as a reference point, so we can tell how much each branch contributes on its own.

The key thing: all three are trained on the **same dataset** — FaceForensics++, the same sample size, the same random seed. So any difference in their verdicts comes from the *architecture*, not from one model getting a luckier training run.

---

## 2 · Uploading a clip & the processing pipeline (2:00 – 4:00)

> `[SCREEN: click the upload box, select a short face video, then click "Analyze".]`

Let me upload a short video clip of a face. I'll click **Analyze**.

While it processes, let me explain what's happening under the hood, because this part matters for a fair comparison. The app doesn't just feed the raw video to the models — it reproduces the **exact same preprocessing the models saw during training**.

> `[SCREEN: while it runs, you can show the DOCUMENTATION.md pipeline diagram, or just keep the demo on screen.]`

There are four steps. **First**, it samples frames from the video at **5 frames per second**, up to a maximum of **16 frames** — that cap keeps it responsive, since this is all running on a free CPU, no GPU.

**Second**, on every sampled frame it runs a **face detector (MTCNN)** and crops tightly to the face, with a small margin. This matters: the models were trained on cropped faces, so if we fed them the whole frame — background, hair, shoulders — they'd be looking at something they never learned on.

**Third**, each cropped face is turned into the **two inputs** the models need: the normalized RGB image for the spatial branch, and a **frequency map** — that's a Fourier transform of the face, with a high-pass filter that suppresses the broad, low-frequency content and keeps the fine detail where deepfake artifacts tend to live.

**Fourth**, each model produces a *fake-probability for every frame*, and the app **averages** those into a single video-level score. So the verdict you're about to see is a consensus across all the sampled frames, not a single lucky frame.

---

## 3 · Reading the verdict cards (4:00 – 6:00)

> `[SCREEN: the three result cards are now visible. Point at one card.]`

Here are the results — one card per model. Let me decode a single card first, then we'll compare them.

Each card has three parts. At the top, a **badge**: green for REAL, red for FAKE. Below it, a **confidence bar** — the colored fill is the model's averaged fake-probability, from 0 on the left to 100% on the right. And there's a small **vertical tick mark** on that bar — that's the model's **decision threshold**.

That threshold is important, and it's not just 0.5. For each model I tuned the threshold on a **separate validation split** — data the model never trained on — to find the cutoff that best separates real from fake. So spatial's threshold sits around 0.13, hybrid's around 0.23, frequency's around 0.45. The rule is simple: **if the bar fills past the tick mark, the verdict is FAKE.** Showing the raw probability *and* the threshold lets you read not just the decision, but how *confident* and how *close to the line* each model is.

> `[SCREEN: now gesture across all three cards together.]`

Now the comparison. Look at all three cards together for the same clip. You'll often see them **disagree** — and that disagreement is the whole point of the demo. The spatial baseline tends to be the most confident and correct; the hybrid and frequency models are more hesitant, and sometimes wrong.

---

## 4 · "What the models see" (6:00 – 7:30)

> `[SCREEN: scroll down to the two galleries — "Face crops" and "FFT spectra".]`

This panel makes the abstract inputs concrete. These are the actual frames the models analyzed.

On the **left** are the **face crops** — the RGB images. This is literally what the *spatial* model sees: just the face, resized.

On the **right** are the **frequency spectra** — the Fourier maps, color-coded so they're visible to the human eye. This is what the *frequency* and *hybrid* models see. The bright center is the coarse structure of the face; the patterns spreading out toward the edges are the fine, high-frequency detail. In theory, deepfake generators leave faint, regular patterns out here — grid-like or periodic textures — that a clean camera image wouldn't have.

> `[SCREEN: linger on a spectrum image.]`

And this is where the honest finding starts to show. When you look at these spectra by eye — and the frequency model's verdicts confirm it — those artifacts are **subtle and inconsistent**. The frequency signal just isn't as reliable as the pixel signal for this dataset.

---

## 5 · The headline finding (7:30 – 9:00)

> `[SCREEN: back to the three verdict cards, all visible.]`

So here's the conclusion this demo is built to deliver — and it's a **negative result**, which I think is the honest and interesting kind.

Adding the frequency branch did **not** improve detection. Across my full experiments, the simple **spatial baseline performed best** — roughly 0.78 on the area-under-curve metric. The **hybrid**, my proposed model, came in clearly **lower**, around 0.65. And the **frequency-only** model was weakest, near 0.57 — barely above guessing.

In other words: the extra complexity of fusing a frequency branch onto a strong image model didn't pay off — it actually *hurt*. The frequency artifacts that the literature suggests should help just aren't strong or consistent enough in this data to add value, and the extra branch mostly added noise.

This demo lets a reviewer **verify that finding for themselves** — upload a clip, and watch the "advanced" hybrid lose to the plain baseline, again and again. That's far more convincing than asking someone to trust a number in a table.

> `[SCREEN: briefly show the caveat text at the bottom of the page.]`

One fair caveat, shown right on the page: these models were trained only on FaceForensics++ faces. A clip from a totally different source is out-of-distribution and may be predicted unreliably. This is a **research demo accompanying a thesis — not a production detector.**

---

## 6 · Outro (9:00 – 10:00)

> `[SCREEN: return to the full demo page, or a closing slide.]`

To wrap up: this demo runs three deepfake detectors — a spatial baseline, my proposed hybrid, and a frequency-only model — on the same uploaded video, mirroring the exact training pipeline, and shows their verdicts side by side along with the inputs they each see.

And what it demonstrates is the thesis's core finding, made visible and reproducible: **the proposed hybrid does not beat the simple spatial baseline.** Sometimes the most valuable result in research is the one that says "this idea, tested carefully, didn't work" — and now anyone can see exactly why.

Thank you for watching.

---

### Recording tips
- **Pre-load a clip.** CPU inference on 16 frames × 3 models takes a few seconds — have your test video ready and consider trimming the "Analyze" wait in the edit, or talk over it (the script already does this in §2).
- **Prepare two clips if possible** — ideally one where the baseline is right and the hybrid disagrees, to make §5's point land on screen.
- **Zoom your browser** to ~125% so the cards and the threshold tick are readable on video.
- If you run out of time, §1 and §4 are the most compressible; §3 (reading a card) and §5 (the finding) are the parts you must keep.
