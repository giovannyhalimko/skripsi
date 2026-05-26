# CHANGE LOG — Revisi BAB III Tahapan Pelaksanaan v4
**Tanggal:** 26 Mei 2026
**File:** `BAB_III_Tahapan_Pelaksanaan_v4.md`
**Revisi dari:** v3 (956 baris)
**Motivasi:** Sinkronisasi narasi tesis dengan kode aktual di `deepfake_hybrid/` (config + scripts) yang telah dioptimasi setelah penulisan v3. Hasil BAB IV (`BAB_IV_draft_hasil_awal.md`) dihasilkan dari konfigurasi yang dideskripsikan v4 ini.

---

## Ringkasan Perubahan

Semua perubahan adalah **sinkronisasi narasi → kode**, bukan perubahan kode. Tidak ada perubahan terhadap referensi pustaka, struktur bab, atau urutan penomoran tabel/gambar dari v3.

| # | Item | v3 (Lama) | v4 (Baru) | Sumber Kebenaran (Kode) |
|---|------|-----------|-----------|--------------------------|
| 1 | FFT _High-Pass Filter_ | (tidak ada) | **Subbab + persamaan (3.4) ditambahkan** | `src/fft_utils.py:9-33` (`_highpass_mask`, `image_to_fft_logmag(highpass=True)`) |
| 2 | FreqCNN `base_channels` | 32, kanal $[32, 64, 128, 256, 256]$, feature_dim = 256, ~700K param | **64, kanal $[64, 128, 256, 512, 512]$, feature_dim = 512, ~4,2 juta param** | `config.yaml: freq_base_channels: 64` |
| 3 | Hybrid: dimensi cabang frekuensi & rasio | 256, rasio 8:1, $W_f \in \mathbb{R}^{256 \times 256}$ | **512, rasio 4:1, $W_f \in \mathbb{R}^{256 \times 512}$** | konsekuensi #2 |
| 4 | Hybrid _classifier dropout_ | 0,3 (dua kali) | **0,5 (dua kali)** | `src/models/hybrid_fusion.py:49,52` |
| 5 | _Spectral band masking_ probabilitas | $p = 0{,}15$ | **$p = 0{,}05$** | `src/deepfake_data.py:134` |
| 6 | _Spectral band masking_ lebar pita | $2$ hingga $\lfloor H/8 \rfloor$ | **$1$ hingga $\max(\lfloor H/16 \rfloor, 2)$** | `src/deepfake_data.py:136` |
| 7 | _Linear warmup_ | 2 _epoch_, `total_iters=2` | **3 _epoch_, `total_iters=3`** (sinkron dengan _backbone freeze_) | `scripts/train.py:248` |
| 8 | _Early stopping patience_ | 10 _epoch_ | **12 _epoch_** | `config.yaml: early_stop_patience: 12` |
| 9 | _Label smoothing_ | $\alpha = 0$ (nonaktif) | **$\alpha = 0{,}05$ (aktif)** | `config.yaml: label_smoothing: 0.05` |
| 10 | _Differential learning rate_ — model _hybrid_ | 2 kelompok (_backbone_ / _head_) | **3 kelompok: _backbone_ ($2 \times 10^{-5}$) / cabang frekuensi ($5 \times 10^{-5}$) / _head_ ($2 \times 10^{-4}$)** | `scripts/train.py:209-213` |
| 11 | _Cosine annealing_ — `T_max` | `max(epochs - 2, 1)` | **`max(epochs - 3, 1)`** (konsekuensi #7) | `scripts/train.py:253` |
| 12 | Hybrid total parameter | ~23,8 juta | **~27,7 juta** | konsekuensi #2 (4,2M FreqCNN, bukan 700K) |
| 13 | Penomoran persamaan | 3.1–3.37 (37 persamaan) | **3.1–3.38 (38 persamaan)** — bertambah 1 karena persamaan _high-pass mask_ (#1) | — |

---

## Perubahan per Bagian

### [3.3.2.3] _Magnitude Spectrum_, _High-Pass Filtering_, dan _Log Scaling_ — REWRITE
- **Judul subbab:** "Magnitude Spectrum dan Log Scaling" → **"Magnitude Spectrum, High-Pass Filtering, dan Log Scaling"**
- **Persamaan baru (3.4):** _Gaussian high-pass mask_ $H(u, v) = 1 - \exp(-((u-u_c)^2 + (v-v_c)^2) / (2(\beta N)^2))$ dengan $\beta = 0{,}15$
- **Paragraf baru:** Rasional _high-pass filtering_ — menekan dominasi komponen frekuensi rendah yang sebagian besar merepresentasikan struktur global wajah, sementara artefak _deepfake_ (_checkerboard_, _spectral rolloff_) terkonsentrasi di frekuensi menengah–tinggi
- **Persamaan log _scaling_ (sekarang 3.5):** Input ke `log1p` adalah $|F'(u,v)| = |F(u,v)| \cdot H(u,v)$, bukan $|F(u,v)|$ langsung

### [3.3.2.4 dst.] — RENUMBER
- Subbab "Contoh Perhitungan FFT 2D" tetap di posisi yang sama, hanya persamaan-persamaan di dalamnya bergeser dari 3.5–3.8 menjadi **3.6–3.9**
- Semua persamaan setelah 3.4 lama bergeser +1 (3.5 → 3.6, 3.6 → 3.7, ..., 3.37 → 3.38)

### [3.3.3.2] Augmentasi Domain Frekuensi — UPDATE
- _Spectral band masking_ probabilitas: 15% → **5%**
- Lebar pita: $2$ hingga $\lfloor H/8 \rfloor$ → **$1$ hingga $\max(\lfloor H/16 \rfloor, 2)$**

### [3.4.2.1] Arsitektur FreqCNN — UPDATE
- _base_channels_: 32 → **64**
- Progresi kanal: $[32, 64, 128, 256, 256]$ → **$[64, 128, 256, 512, 512]$**
- Batas maksimum kanal: 256 → **512** ($8 \times \text{base\_channels}$)
- **Paragraf baru:** Rasional pemilihan _base_channels_ = 64 — kapasitas representasi yang lebih besar pada tahap awal untuk menangkap variasi artefak frekuensi yang halus pada _crop_ wajah

### [Tabel 3.5] Arsitektur _Layer-by-Layer_ FreqCNN — REWRITE LENGKAP
- Subjudul: "_depth_ = 5, _base_channels_ = 32" → **"_depth_ = 5, _base_channels_ = 64"**
- Seluruh baris dimensi output diperbarui: $32 \rightarrow 64$, $64 \rightarrow 128$, $128 \rightarrow 256$, $256 \rightarrow 512$
- Parameter per blok diperbarui (perhitungan baru):
  - FreqBlock 1: 384 → **~900**
  - FreqBlock 2: 20.700 → **~82.400**
  - FreqBlock 3: 82.300 → **~329.000**
  - FreqBlock 4: 328.000 → **~1.313.000**
  - FreqBlock 5: 590.000 → **~2.361.000**
- _Classifier head_ standalone: FC1 Linear(256→128) → **Linear(512→256)**, FC2 Linear(128→1) → **Linear(256→1)**
- Total parameter: ~700K → **~4,2 juta**

### [3.4.3.2] Cabang Frekuensi Hybrid — UPDATE
- Dimensi output FreqCNN _backbone_: 256 → **512**
- Catatan konfigurasi: "(pada konfigurasi _depth_ = 5)" → **"(pada konfigurasi _depth_ = 5 dengan _base_channels_ = 64)"**

### [3.4.3.3] _Projection Layers_ — UPDATE
- Rasio dimensi cabang: "8:1" → **"4:1"**
- Matriks bobot: $\mathbf{W}_f \in \mathbb{R}^{256 \times 256}$ → **$\mathbf{W}_f \in \mathbb{R}^{256 \times 512}$**

### [3.4.3.5] _Classifier Head_ — UPDATE
- _Dropout_ pertama: 0,3 → **0,5**
- _Dropout_ kedua: 0,3 → **0,5**
- Penjelasan disesuaikan: dari "_dropout_ yang moderat agar tidak menghilangkan terlalu banyak sinyal" → **"tingkat _dropout_ yang relatif tinggi dipilih karena kepala klasifikasi merupakan satu-satunya komponen yang langsung memetakan fitur fusi menjadi keputusan _real_/_fake_"**

### [Tabel 3.6] Perbandingan Tiga Arsitektur Model — UPDATE
- FreqCNN dimensi fitur: 256 → **512**
- FreqCNN total parameter: ~700 ribu → **~4,2 juta**
- Hybrid total parameter: ~23,8 juta → **~27,7 juta**

### [Tabel 3.7] Dimensi Fitur per Komponen Model Hybrid — UPDATE
- FreqCNN _backbone_ output: 256 → **512**
- Proyeksi frekuensi input: 256 → **512**

### [Diagram HybridTwoBranch] (HTML comment, Gambar 3.9) — UPDATE
- FreqCNN output: (256) → **(512)**
- Proyeksi: (256→256) → **(512→256)**

### [Tabel 3.8] _Learning Rate_ per Kelompok Parameter — REWRITE
- **Lama:** 2 baris (_Backbone_ $2 \times 10^{-5}$, _Head_ $2 \times 10^{-4}$)
- **Baru:** 3 baris dengan tambahan kelompok cabang frekuensi untuk model _hybrid_:
  - _Backbone_ ($2 \times 10^{-5}$, base/10) — Parameter XceptionNet
  - **Cabang frekuensi _hybrid_ ($5 \times 10^{-5}$, base × 0,25) — Parameter FreqCNN dalam model _hybrid_**
  - _Head_ ($2 \times 10^{-4}$, base) — Proyeksi, SE _gate_, _classifier_; juga FreqCNN _standalone_
- **Paragraf baru:** Rasional pemberian _learning rate_ menengah pada cabang FreqCNN _hybrid_ — mencegah gradien dari cabang frekuensi yang diinisialisasi acak mendominasi pembaruan bobot pada awal pelatihan

### [3.5.3] Penjadwalan _Learning Rate_ — UPDATE
- _Linear warmup_: 2 _epoch_ → **3 _epoch_**, `total_iters=2` → **`total_iters=3`**
- _Cosine annealing_: dimulai _epoch_ ke-3 → **_epoch_ ke-4**; `T_max=max(epochs-2, 1)` → **`T_max=max(epochs-3, 1)`**
- **Penjelasan baru:** Durasi _warmup_ sengaja disinkronkan dengan periode _backbone freezing_ (3 _epoch_) — pada _epoch_ ke-4 saat _backbone_ dilepaskan, _learning rate_ sudah pada nilai _base_ penuh siap untuk _fine-tuning_
- Kurva LR untuk 30 _epoch_:
  - _Epoch_ 1: $\approx 2 \times 10^{-5}$ (tidak berubah)
  - _Epoch_ 2: $1 \times 10^{-4} \rightarrow$ **$\approx 1{,}1 \times 10^{-4}$** (titik tengah _warmup_ 3 _epoch_)
  - **_Epoch_ 3:** $2 \times 10^{-4}$ — akhir _warmup_ (baru ditambahkan ke daftar)
  - _Epoch_ 3–30 _cosine decay_ → **_Epoch_ 4–30 _cosine decay_**

### [3.5.4.2] _Label Smoothing_ — REWRITE
- **Lama:** $\alpha = 0$ (nonaktif), dengan alasan "memaksimalkan sinyal pelatihan pada dataset ukuran kecil"
- **Baru:** **$\alpha = 0{,}05$ (aktif)** dengan alasan "memberikan efek regularisasi yang mencegah model _overconfident_ pada label _hard_ — terutama relevan ketika _backbone_ XceptionNet _pretrained_ digabungkan dengan _head_ yang dilatih dari awal, karena kombinasi ini cenderung menghasilkan _logit_ ekstrem pada awal pelatihan"
- Contoh transformasi label: $0 \rightarrow 0{,}01$, $1 \rightarrow 0{,}99$ → **$0 \rightarrow 0{,}025$, $1 \rightarrow 0{,}975$**

### [3.5.4.3] Contoh Perhitungan BCEWithLogitsLoss — UPDATE
- Ilustrasi menggunakan $\alpha = 0{,}02$ (sebelumnya, untuk menunjukkan mekanisme) → **$\alpha = 0{,}05$ (sesuai konfigurasi aktif)**
- Label _smoothed_: $y' = 0{,}99$ → **$y' = 0{,}975$**
- Nilai _loss_ akhir: 0,1041 → **0,1415** (dihitung ulang dengan $\alpha = 0{,}05$)

### [3.5.8] _Early Stopping_ — UPDATE
- _Patience_: 10 _epoch_ → **12 _epoch_**
- Paragraf rasional ditulis ulang: dari "Peningkatan _patience_ dari 5 ke 10" → **"Nilai _patience_ sebesar 12 _epoch_ ... _counter patience_ direset pada _epoch_ ke-4 saat _unfreezing_"** (catatan teknis baru: _patience counter_ reset pada saat _backbone unfreeze_, sesuai `scripts/train.py:280`)

### [Tabel 3.9] Ringkasan _Hyperparameter_ Pelatihan — REWRITE LENGKAP
Perubahan baris:
- _Learning rate_ (_base_): tetap, catatan diperjelas → "Lapisan baru (proyeksi, SE _gate_, _classifier_)"
- **Baris baru:** _Learning rate_ (cabang freq, _hybrid_) = $5 \times 10^{-5}$
- _Early stopping patience_: 10 → **12**
- _Label smoothing_: 0,0 (nonaktif) → **0,05**
- _LR warmup_: 2 _epoch_ → **3 _epoch_**, catatan "sinkron dengan _freeze_"
- FreqCNN _depth_: "5" → **"5 / 64"** (depth / base_channels), dengan parameter ~700K → **~4,2 juta** dan progresi kanal eksplisit
- **Baris baru:** FFT _high-pass cutoff_ ($\beta$) = 0,15
- **Baris baru:** FFT _noise sigma_ = 0,05
- **Baris baru:** _Spectral band masking_ ($p = 0{,}05$, lebar $1$–$H/16$)

---

## Konsistensi yang Tetap Dipertahankan dari v3

Item-item berikut **sudah cocok antara v3 dan kode**, sehingga tidak diubah:

- Dataset (FFPP, CDF), _stratified split_ 70/15/15 per video, _seed_ = 42
- Ekstraksi _frame_: 5 FPS, maks 50 _frame_/video, OpenCV + multiprocessing
- FFT _z-score normalization_ per dataset via `fft_stats.json`
- Augmentasi spasial: Resize 256, RandomResizedCrop(224, 0.8-1.0), ColorJitter, RandomHorizontalFlip, ToTensor, Normalize ImageNet, RandomErasing(p=0.1, scale=0.02-0.15)
- _Consistent hflip_ pada mode _hybrid_ (`include_hflip=False` di transforms, manual `TF.hflip` + `torch.flip(FFT)` dengan $p = 0{,}5$)
- Injeksi _noise_ Gaussian pada FFT dengan $\sigma = 0{,}05$
- Optimizer AdamW, _weight decay_ $1 \times 10^{-4}$
- _Pos weight_ = $n_{\text{neg}} / n_{\text{pos}}$
- _Gradient accumulation_ (`accum_steps = 2`), _gradient clipping_ (`max_norm = 5,0`), AMP + TF32
- _Backbone freezing_ 3 _epoch_, _unfreeze_ _epoch_ ke-4 untuk _spatial_, _hybrid_, _early fusion_
- _Differential learning rate_ untuk model _spatial_ (2 kelompok) — tidak berubah, hanya kelompok _hybrid_ yang menjadi 3
- AUC validasi sebagai metrik _early stopping_ dan seleksi _checkpoint_
- _Checkpoint_ format `{"state_dict", "epoch", "config"}`
- 3 _seed_ (0, 1, 2), evaluasi _in-dataset_ dan _cross-dataset_, _generalization drop_ $\Delta = \text{F1}_{\text{in}} - \text{F1}_{\text{cross}}$
- Variasi ukuran sampel: FFPP [100, 300, 600, 1000], CDF [100, 250, 500, 750]

---

## Catatan untuk Penyalinan ke `.docx`

1. **Persamaan 3.4 baru** (Gaussian high-pass mask) perlu disisipkan di §3.3.2.3 — pastikan editor `.docx` menambahkan persamaan baru di tempat yang tepat dan menggeser nomor persamaan setelahnya (+1 untuk semua persamaan dari 3.5 hingga akhir).
2. **Tabel 3.5 (FreqCNN layer-by-layer)** memerlukan perubahan dimensi pada SEMUA baris — pastikan tidak hanya angka kanal tetapi juga parameter count diperbarui.
3. **Tabel 3.8 (Differential LR)** bertambah satu baris — pastikan _layout_ tabel di `.docx` mengakomodasi 3 baris (bukan 2).
4. **Tabel 3.9 (Ringkasan Hyperparameter)** bertambah 4 baris baru — pertahankan urutan dan kelompokan logis.
5. **Tidak ada gambar baru** yang ditambahkan di v4. Semua gambar v3 (Gambar 3.1–3.11) tetap berlaku.
6. **Tidak ada perubahan referensi pustaka** — daftar pustaka tetap sama seperti v3.
