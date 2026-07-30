# Item 2 — Audit Justifikasi Rumus & Model FreqCNN vs Referensi

**Tanggal:** 2026-07-29
**Permintaan penguji/user:** pastikan SEMUA rumus benar-benar ada di referensi (bukan mengada-ngada); model FreqCNN (bikinan sendiri) WAJIB dijustifikasi referensi; kurang referensi → tambahkan; perlu paragraf → tambah/adjust.
**Metode:** audit tingkat subbab — untuk setiap subbab ber-rumus, dicek sitasi yang ada di dalamnya (422 objek math, 238 paragraf ber-math).

---

## VERDICT UMUM: **sebagian besar SUDAH terjustifikasi.** Ada **2 gap nyata** + beberapa minor.

Angka "198 rumus tak bersitasi" pada scan awal **menyesatkan** — mayoritas adalah **contoh perhitungan (worked examples)** dan **hasil BAB IV**, yang memang TIDAK perlu sitasi (itu demonstrasi/temuan sendiri, bukan klaim teori).

---

## A. Subbab ber-rumus yang SUDAH terjustifikasi (✅)

| Rumus / Subbab | Sitasi ada | Layak? |
|---|---|---|
| Transformasi Fourier / DFT, magnitude, log | Durall, Gonzalez & Woods, Oppenheim | ✅ (Gonzalez untuk DFT) |
| CNN (conv, ReLU, pooling) | banyak (Chollet, He, dll.) | ✅ |
| SE Block (squeeze/excitation) | Hu (SE-Net) | ✅ tepat |
| Residual block (pers. 2.6) | He (ResNet) | ✅ tepat |
| Depthwise/pointwise/DSC (2.7–2.9) | Chollet, Howard, Sifre (di subbab CNN) | ✅ |
| SGD (pers. 2.23–…) | Bottou, Ruder | ✅ tepat |
| Adam/AdamW (momen, koreksi bias) | Kingma, Loshchilov | ✅ tepat |
| BCEWithLogitsLoss (2.30) | Goodfellow | ✅ |
| Gaussian high-pass (2.17) | Durall, Odena, Zhang (subbab Konversi FFT) | ✅ |
| Augmentasi (noise 2.20, band mask 2.21) — BAB III | Goodfellow, Srivastava, Zhong | ✅ (baru) |
| Metrik: Accuracy/Precision/Recall/F1/AUC/TPR/FPR | Rana, Durall, Hasanaath | ✅ |
| Generalization drop Δ (2.40) | — (metrik turunan penulis) | ✅ tak perlu (didefinisikan sendiri) |

**Contoh perhitungan** (FFT 2D, DSC, forward pass FreqCNN, loss, metrik) & **hasil BAB IV**: benar TANPA sitasi.

---

## B. GAP NYATA (wajib diperbaiki)

### B.1 Label smoothing (persamaan 2.32) — ❌ TIDAK ADA sitasi
- Lokasi: BAB II §2.15.5 (area idx937) **dan** BAB III §3.5.4 — keduanya tanpa sitasi label smoothing.
- Sumber asli label smoothing = **Szegedy et al. 2016, "Rethinking the Inception Architecture for Computer Vision" (§7)**. ✅ **Sudah didownload** ke `thesis_reference/`.
- **AKSI:** tambah ke bibliografi + sisipkan sitasi [Szegedy] di:
  - BAB II tempat rumus 2.32 diperkenalkan ("…melunakkan label target: [Szegedy]")
  - BAB III §3.5.4 ("Label smoothing diaktifkan dengan α = 0,05 … [Szegedy]")

### B.2 Batch Normalization (persamaan 2.5) — sitasi SALAH
- Sitasi di sekitar rumus 2.5 = Akinrogunde, Haliassos, Nguyen (paper deepfake — **tidak relevan**, bukan sumber BatchNorm).
- Sumber asli = **Ioffe & Szegedy 2015** — ✅ **sudah ada di bibliografi** (ditambah untuk landasan batch size).
- **AKSI:** sisipkan sitasi [Ioffe & Szegedy] tepat pada rumus BatchNorm 2.5.

---

## C. Model FreqCNN (§3.4.2) — dinilai: **CUKUP terjustifikasi, bisa diperkuat**

FreqCNN memang custom, TAPI sudah dijustifikasi komponen-per-komponen (bukan mengada-ngada):
- Blok residual (FreqBlock) → **He et al. (ResNet) [HeK15]** ✅ sudah dikutip.
- Merujuk rumus residual (2.6) & BatchNorm (2.5).
- Progresi kanal [64,128,256,512,512], depth 5, base_channels 64 → argumen desain penulis.

**Penguatan yang disarankan (opsional tapi bagus):**
1. Sisipkan [Ioffe & Szegedy] pada penyebutan BatchNorm di FreqBlock (konsisten dgn B.2).
2. Di paragraf pembuka FreqCNN, tambah 1 kalimat + sitasi precedent bahwa **CNN pada peta FFT/magnitude adalah pendekatan yang sudah divalidasi** (Durall, Qian, Tan sudah di bibliografi) — supaya "kenapa CNN pada domain frekuensi" punya landasan, bukan asumsi.
   - Draf: *"Pendekatan menerapkan CNN langsung pada representasi frekuensi telah divalidasi pada deteksi citra sintetis [Durall], [Qian], sehingga FreqCNN mengadaptasi prinsip tersebut pada peta log-magnitude FFT."*

---

## D. MINOR (opsional)
| Rumus/Subbab | Status | Saran |
|---|---|---|
| Gradient Clipping — BAB III §3.5.6 | tak bersitasi | reuse Goodfellow, atau Pascanu 2013 (asal gradient clipping) |
| Mixed Precision (AMP) §3.5.7 | tak bersitasi | Micikevicius et al. 2018 (kalau mau; detail implementasi) |
| Augmentasi Data — BAB II | hanya Afchar | tambah Shorten & Khoshgoftaar 2019 (survei augmentasi) opsional |

---

## RINGKAS AKSI
1. ✅ Download **Szegedy 2016** (label smoothing) — DONE, indexed.
2. ☐ Bibliografi Word: tambah sumber **Szegedy 2016**.
3. ☐ Sisip sitasi: **[Szegedy]** di rumus 2.32 (BAB II + §3.5.4); **[Ioffe & Szegedy]** di rumus 2.5 (BatchNorm) + FreqBlock.
4. ☐ (opsional) 1 kalimat precedent [Durall]/[Qian] di pembuka FreqCNN.
5. ☐ (opsional minor) clipping & AMP citations.
