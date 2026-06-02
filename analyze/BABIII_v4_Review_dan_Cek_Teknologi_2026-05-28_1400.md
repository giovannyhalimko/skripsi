# Review Revisi Terakhir (BAB III v4) + Cek Kelengkapan Teknologi

**Tanggal:** 2026-05-28
**Sumber:** commit `f8d16da` (`documents/BAB_III_Tahapan_Pelaksanaan_v4.md`, `BAB_III_v4_CHANGELOG.md`), `.docx` OneDrive (25 Mei), kode `deepfake_hybrid/`.

---

## 1. Apakah revisi terakhir (v4) sudah OK?

**Sebagian besar OK.** v4 adalah sinkronisasi narasi→kode atas 13 ketidakcocokan. Spot-check terhadap `config.yaml`/kode cocok:

| Klaim v4 | Verifikasi kode | Status |
|---|---|---|
| `label_smoothing = 0,05` | `config.yaml:17 label_smoothing: 0.05` | ✅ |
| `early_stop_patience = 12` | `config.yaml:15` | ✅ |
| `lr = 2e-4`, `weight_decay = 1e-4` | `config.yaml:12-13` | ✅ |
| FreqCNN `base_channels = 64` | `config.yaml:23` | ✅ |
| High-pass mask (pers. 3.4) β=0,15 | `fft_utils.py:9` `cutoff=0.15` | ✅ |
| Spectral band masking p=0,05; lebar 1–⌊H/16⌋ | `deepfake_data.py:134-136` | ✅ |
| 3 grup differential LR (hybrid) | `train.py:209-213` | ✅ |

### ❗ Masalah utama v4: langkah *face detection & cropping* HILANG (regresi)

- `.docx` (25 Mei) **punya** subbab "**Deteksi wajah dan cropping**" (+ "Face Alignment", "Resize"). **v4 markdown menghapusnya** — subbab 3.3.1 hanya menyebut ekstraksi frame via OpenCV, tanpa cropping wajah sama sekali.
- Padahal *face cropping* adalah langkah inti pipeline:
  - `scripts/extract_frames.py:124` & `run_pipeline.py:91`: opsi `--face-crop` (MTCNN).
  - `src/face_utils.py:10`: `from facenet_pytorch import MTCNN`.
  - `config.yaml:23`: komentar "*64 for face crops, 32 for full scenes*" → default 64 = pipeline memang pakai *face crop*.
  - `colab_run.ipynb`: `FACE_CROP = True` (recommended), `FACE_MARGIN = 0.3`.
  - Hasil eksperimen (`outputs/2026-04-09/face_crop/n100/conclusion.md`): *face crop* menaikkan AUC spatial FFPP **0,696 → 0,901**. **Semua hasil BAB IV diproduksi dengan `face_crop=True`.**
- v4 bahkan diam-diam mengasumsikan *face crop* (rasional FreqCNN menyebut "*crop wajah*") tetapi tidak pernah mendokumentasikan langkahnya. **Inkonsisten.**

➡️ **Tindakan:** kembalikan subbab "Deteksi Wajah dan Cropping" ke 3.3 (idealnya **3.3.2**, antara Ekstraksi Frame dan Konversi FFT), dan tulis sesuai kode (lihat bagian 3 di bawah).

---

## 2. Apakah "Analisis Sistem" memang sependek itu?

**Tidak ada "Analisis Sistem" di dokumen mana pun** — baik `.docx` maupun v4 markdown (grep "Analisis Sistem" = 0 hit). Yang ada hanyalah **stub D.6** di `Revisi_Reviewer_BAB_I_II_III_2026-05-18.md` (4 poin bullet). Jadi "pendek" karena memang baru kerangka.

Untuk jadi subbab yang layak (mis. **3.8 Analisis Sistem / Kebutuhan Sistem**), perlu diperluas mencakup:
- **Perangkat keras**: GPU NVIDIA (CUDA), spesifikasi Colab Pro (T4 15 GB / V100), RAM, fallback CPU.
- **Perangkat lunak & versi**: Python 3.9, dan **setiap** dependensi di `requirements.txt` dengan peran + rasional (lihat tabel bagian 3).
- **Justifikasi pemilihan** tiap pustaka (kenapa `timm`, kenapa MTCNN dari `facenet-pytorch`, dll.).
- **Orkestrasi pipeline** (`run_pipeline.py` → extract → split → FFT cache → train → eval).

---

## 3. Cek kelengkapan teknologi + penjabaran sub-dependensi

Tech stack aktual (dari `requirements.txt` + import di `src/`+`scripts/`):
`torch, torchvision, timm, numpy, pandas, pyyaml, tqdm, scikit-learn, opencv-python, Pillow, facenet-pytorch, matplotlib`.

| Pustaka | Dipakai untuk | Dibahas di dok.? | Catatan / sub-dependensi yang perlu dijelaskan |
|---|---|---|---|
| **facenet-pytorch → MTCNN** | Deteksi & crop wajah (`face_utils.py`) | ❌ **TIDAK** (v4) | **GAP TERBESAR.** MTCNN = *Multi-task Cascaded CNN* (kaskade **P-Net → R-Net → O-Net**) — perlu dijelaskan cara kerjanya. Parameter aktual: `keep_all=True, min_face_size=60, thresholds=[0.6,0.7,0.7], margin=0.3`, pilih wajah terbesar by area. |
| **timm** | XceptionNet pretrained | ✅ (3.4.1.2) | `timm.create_model("xception", pretrained=True)` — bobot ImageNet. Baik. |
| **torch / torchvision** | Training, AMP, AdamW, BCEWithLogitsLoss, scheduler, transforms | ✅ (3.5) | Sub-fitur (AMP, gradient accumulation, cosine+warmup, clipping) dibahas. Baik. |
| **OpenCV (cv2)** | Baca video, ekstraksi frame, BGR→RGB, grayscale | ✅ (3.3.1, 3.3.2.1) | Baik. |
| **NumPy** | FFT (`np.fft.fft2`, `fftshift`), perhitungan | ✅ (3.3.2.2) | Baik. |
| **scikit-learn** | `train_test_split(stratify=...)` | ✅ singkat (3.2.3) | Cukup. |
| **Pillow (PIL)** | Load/transform citra | ⚠️ disebut sekilas | Sebut di Analisis Sistem. |
| **pandas** | Manifest CSV | ⚠️ implisit | Sebut di Analisis Sistem. |
| **pyyaml** | Baca `config.yaml` | ❌ | Sebut di Analisis Sistem. |
| **tqdm** | Progress bar | ❌ | Utilitas, sebut singkat. |
| **matplotlib** | Plot hasil (BAB IV) | ❌ (BAB III) | Sebut di Analisis Sistem / relevan BAB IV. |

### ❗ Over-claim yang harus dikoreksi: "Face Alignment"
`.docx` mendeskripsikan **"Face Alignment"** (penyelarasan berbasis *landmark* mata/hidung). **Kode TIDAK melakukan alignment** — `face_utils.py` hanya deteksi *bounding box* + ekspansi margin 30% + crop. **Hapus klaim Face Alignment** (atau implementasikan), agar narasi tidak mengklaim langkah yang tak ada.

### Draf subbab "Deteksi Wajah dan Cropping" (sesuai kode, untuk 3.3.2)
> Setelah frame diekstraksi, setiap frame melewati deteksi wajah menggunakan **MTCNN** (*Multi-task Cascaded Convolutional Networks*) dari pustaka `facenet-pytorch`. MTCNN bekerja melalui tiga jaringan bertingkat: **P-Net** (mengusulkan kandidat wajah), **R-Net** (menyaring kandidat), dan **O-Net** (memfinalisasi *bounding box*). Detektor dikonfigurasi dengan `min_face_size = 60` piksel dan ambang deteksi `[0,6; 0,7; 0,7]`. Bila terdapat lebih dari satu wajah, dipilih wajah dengan area terbesar. *Bounding box* diperluas dengan margin 30% lalu citra dipotong, sehingga analisis terfokus pada region wajah dan meminimalkan *noise* latar. Frame hasil *crop* di-resize ke 224×224 sebelum tahap berikutnya.

➡️ Sertakan **justifikasi empiris**: *face crop* menaikkan AUC spatial FFPP dari 0,696 → 0,901 (rujuk eksperimen internal).

---

## Ringkasan tindakan
1. **v4 3.3:** tambahkan kembali subbab "Deteksi Wajah dan Cropping" sesuai kode (MTCNN), tanpa klaim *Face Alignment*.
2. **Tulis subbab 3.8 Analisis Sistem** yang lengkap (HW + semua pustaka + justifikasi).
3. **Jelaskan sub-dependensi**: terutama kaskade MTCNN (P/R/O-Net); timm/torch sudah cukup.
4. Pastikan konsistensi: seluruh BAB IV memakai `face_crop=True` → metodologi wajib mencantumkannya.
