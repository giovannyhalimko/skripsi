# Cheat Sheet Sidang — Pertahanan Pemilihan _Hyperparameter_

**Tanggal:** 27 Juli 2026
**Sumber angka:** `deepfake_hybrid/outputs/gpu_pull_2026-06-19/` — konfigurasi dibaca langsung dari `best.pt` (setiap _checkpoint_ menyimpan `config` yang benar-benar dipakai saat pelatihan), bukan dari `config.yaml`.

---

## 1. Jawaban Induk — pakai ini dulu untuk semua pertanyaan "kenapa nilai ini?"

> "Nilai-nilai ini adalah **variabel kontrol**, bukan hasil penelitian. Penelitian ini membandingkan tiga arsitektur — _spatial_, _freq_, dan _hybrid_. Apabila setiap model diberi _hyperparameter_ yang di-_tuning_ sendiri-sendiri, perbedaan performa tidak dapat diatribusikan ke arsitektur karena bisa saja berasal dari perbedaan usaha _tuning_. Karena itu satu konfigurasi identik diterapkan ke ketiga model, empat ukuran sampel, dua dataset, dan tiga _seed_ — sebagaimana dirangkum pada Tabel 3.9."

Lalu **langsung tambahkan bagian jujurnya** (jangan tunggu ditanya):

> "Nilai-nilai tersebut berasal dari praktik standar _transfer learning_ pada data terbatas dan dari kendala arsitektural, bukan dari _grid search_. Pencarian _hyperparameter_ menyeluruh atas 24 sel eksperimen × 3 _seed_ tidak memungkinkan dengan anggaran komputasi GPU sewa yang tersedia. Hal ini telah dicatat sebagai keterbatasan penelitian pada BAB V."

**Kenapa dua bagian?** Bagian pertama menutup pertanyaan secara metodologis. Bagian kedua mencegah penguji merasa menemukan kelemahan yang Anda sembunyikan — mengakui duluan jauh lebih kuat daripada ketahuan.

---

## 2. Konfigurasi yang Benar-Benar Dipakai (terverifikasi dari `best.pt`)

```
lr                    2e-4        weight_decay          1e-4
batch_size            64          accum_steps           2      → batch efektif 128
epochs (maks)         30          early_stop_patience   12
label_smoothing       0.05        fusion_mode           two_branch
freq_depth            5           freq_base_channels    64
fft_noise_sigma       0.05        image_size            224
frame_sampling_fps    5           max_frames_per_video  100
num_workers           4           n_seeds               3
```

**Pembagian data (FFPP n=750):** 524 / 113 / 113 video = 70 / 15 / 15 % — dipisah **per video**, bukan per _frame_.

---

## 3. Jawaban Cepat per Parameter

| Ditanya soal | Jawaban singkat |
| --- | --- |
| **AdamW, lr 2e-4, wd 1e-4** | _Decoupled weight decay_ (Loshchilov & Hutter, 2019). Pada Adam standar, efek regularisasi bervariasi antar parameter mengikuti LR adaptifnya; pada AdamW konsisten. Penting di sini karena parameter _pretrained_ dan parameter baru punya skala gradien yang sangat berbeda. |
| **LR _backbone_ = base/10 (2e-5)** | Melindungi bobot ImageNet dari gradien besar yang berasal dari _head_ yang masih acak. Praktik standar _fine-tuning_. |
| **LR cabang freq = base × 0,25 (5e-5)** | FreqCNN diinisialisasi acak. Tanpa peredaman, gradiennya mendominasi pembaruan bobot di awal pelatihan dan cabang spasial praktis tidak terlatih. Nilai menengah menjaga keseimbangan kontribusi kedua cabang. |
| **_Freeze_ 3 _epoch_ + _warmup_ 3 _epoch_** | **Sengaja disinkronkan.** Saat _backbone_ dilepas di _epoch_ 4, LR sudah tepat mencapai 100% nilai _base_ — siap untuk _fine-tuning_ penuh. Ini argumen desain, bukan kebetulan. |
| **_Patience_ 12 (bukan 5)** | _Unfreezing_ di _epoch_ 4 memicu pergeseran distribusi fitur internal dan penurunan AUC sementara. _Patience_ 12 + reset _counter_ saat _unfreeze_ memberi jendela pemulihan penuh. **Ada bukti empirisnya — lihat §5.** |
| **_Epoch_ maksimum 30** | Batas atas anggaran komputasi. Durasi nyata ditentukan _early stopping_ (aktif di 59 dari 76 _run_). |
| **_Label smoothing_ 0,05** | Cukup untuk meredam _overconfidence_ (kombinasi _backbone pretrained_ + _head_ baru cenderung menghasilkan _logit_ ekstrem di awal), namun cukup kecil agar sinyal positif tidak melemah pada tier n = 100. |
| **_pos_weight_ = n_neg/n_pos** | Nilainya **1,000** karena _sampling_ sudah 50:50 secara desain — jadi praktis non-aktif. Tetap dipasang agar kode tetap benar bila rasio kelas bergeser. |
| **_Gradient clipping_ 5,0** | Mengakomodasi LR 2×10⁻⁴, terutama lonjakan norma gradien pada _epoch_ 4 ketika seluruh jaringan mulai menerima aliran gradien. |
| **_Gradient accumulation_ 2** | Memperbesar _batch_ efektif tanpa menambah kebutuhan VRAM. _Loss_ dibagi `accum_steps` agar skala gradien konsisten. |
| **Seleksi model = AUC validasi** | AUC bersifat _threshold-independent_; akurasi dan F1 bergantung pada ambang 0,5 yang belum tentu optimal. Ambang operasional dipilih terpisah dan disimpan di `threshold.json` (mis. 0,195 pada _hybrid_ FFPP n750). |
| **3 _seed_** | Semua angka dilaporkan _mean_ ± _std_. Contoh: _spatial_ FFPP n750 AUC = 0,778 ± 0,010 — simpangan antar-_seed_ ~0,01, jauh lebih kecil dari selisih antar-model. |
| **Split 70/15/15 _by video_** | **Poin metodologis terkuat.** Pemisahan dilakukan pada level video, bukan _frame_, sehingga _frame_ dari video yang sama tidak pernah muncul di dua _split_ berbeda (_frame leakage_). Tanpa ini, AUC akan melambung palsu. |
| **FreqCNN _depth_ 5 / _base_ch_ 64** | Argumen desain: blok bertingkat menangkap pola spektral dari abstraksi rendah hingga tinggi; koneksi residual menjaga stabilitas pelatihan. ⚠️ **Jangan klaim sudah diuji vs _depth_ 3** — ablasinya tidak ada. |
| **FFT _high-pass_ β = 0,15** | Menekan energi frekuensi rendah yang didominasi konten wajah, agar model fokus pada artefak frekuensi tinggi hasil _upsampling_ GAN. |
| **FFT _noise_ σ = 0,05** | Peta FFT dimuat dari _cache_ statis dan identik setiap _epoch_; _noise_ mencegah penghafalan sekaligus mensimulasikan variasi _noise_ sensor/kompresi. |
| **5 FPS** | Mengurangi redundansi antar-_frame_ berdekatan yang hampir identik, sehingga variasi data lebih tinggi per satuan biaya komputasi. |
| **224 × 224** | Resolusi input standar XceptionNet _pretrained_ ImageNet; mengubahnya akan membuang manfaat bobot _pretrained_. |

---

## 4. ⚠️ DUA ANGKA YANG HARUS DIPERBAIKI SEBELUM SIDANG

Keduanya mudah diverifikasi penguji dari _log_ atau _checkpoint_.

### 4.1 _Batch size_ — naskah salah

| | Naskah (Tabel 3.9 / 3.11 + BAB IV §4.1) | Run sebenarnya |
| --- | --- | --- |
| _Batch_ per langkah | 16 | **64** |
| _Batch_ efektif | 32 | **128** |

`config.yaml` memang berisi `batch_size: 16`, tetapi `vast_run.sh` menimpanya dengan _auto-tune_ berbasis VRAM. Nilai 64 tersimpan permanen di dalam setiap `best.pt`.

**Kalimat pengganti:**

> "...ukuran _batch_ per langkah disesuaikan dengan kapasitas VRAM GPU (64 pada GPU kelas 16–24 GB), dengan _gradient accumulation_ 2 langkah sehingga ukuran _batch_ efektif menjadi 64 × 2 = **128**."

Versi ini justru lebih baik: _gradient accumulation_ jadi punya alasan nyata.

**Lokasi yang harus diedit:** Tabel 3.9 (2 baris: _Batch size_ dan _Gradient accumulation_), narasi §3.5.5, dan paragraf pembuka BAB IV §4.1.

### 4.2 Jumlah _frame_ per video — naskah salah

| | Naskah (BAB III, bagan alur + §3.2) | Run sebenarnya |
| --- | --- | --- |
| Maks _frame_/video | 50 | **100** |

**Cara penguji bisa membuktikannya:** _split_ validasi FFPP n=750 berisi 113 video dan menghasilkan **8.904 _frame_** (≈ 79 _frame_/video) — mustahil terjadi bila batasnya 50.

**Perbaikan:** ganti "50" → "100" pada bagan alur tahapan dan pada narasi §3.2 ("...diekstraksi maksimum **100** _frame_ pada laju 5 FPS").

> 📌 Catatan: ketidaksesuaian ini sudah tercatat sejak `analyze/Deep_Analysis_BAB1-3_ColabCrossCheck_2026-06-03.md` dan masih belum diperbaiki pada revisi 7 Juli 2026.

### 4.3 Jumlah parameter XceptionNet — 22,8 juta vs 20,8 juta

BAB III §3.4 menyebut XceptionNet memiliki "~22,8 juta parameter". Diverifikasi langsung dari `timm`:

```
xception, num_classes=0    → 20,81 juta     ← yang dipakai penelitian ini
xception, head 1000 kelas  → 22,86 juta     ← angka yang dikutip di naskah
```

**Ini sebenarnya bukan kesalahan fatal — dan bisa dijadikan jawaban yang bagus** bila ditanya:

> "Angka 22,8 juta adalah jumlah parameter XceptionNet asli **beserta _classifier head_ 1000 kelas ImageNet** (20,81 juta + 2048 × 1000 ≈ 22,86 juta). Dalam penelitian ini _backbone_ digunakan sebagai _feature extractor_ dengan `num_classes=0`, sehingga _head_ tersebut dihilangkan dan jumlah parameter riilnya **20,8 juta**."

**Rekomendasi:** perjelas di naskah menjadi *"~22,8 juta parameter (termasuk _head_ ImageNet 1000 kelas); ~20,8 juta sebagai _feature extractor_ yang digunakan pada penelitian ini"*.

**Jumlah parameter terverifikasi (diukur langsung dari kode, bukan dijumlah manual):**

| Komponen | Parameter |
| --- | --- |
| XceptionNet _backbone_ (`num_classes=0`) | **20,81 juta** |
| FreqCNN (_depth_ 5, _base_ch_ 64) | **4,22 juta** |
| **Hybrid total** (termasuk proyeksi, SE _gate_, _classifier_) | **25,88 juta** |

Selisih 25,88 − (20,81 + 4,22) = 0,85 juta berasal dari dua lapisan proyeksi (2048→256 dan 512→256), SE _gate_, dan _classifier_ akhir. Periksa apakah angka total _hybrid_ muncul di naskah dan sesuaikan ke **~25,9 juta**.

---

## 5. Bukti Empiris untuk Membela _Patience_ = 12

Jika ditanya *"kenapa patience 12? Bukankah itu terlalu longgar dan boros komputasi?"*:

- **_Early stopping_ benar-benar aktif:** terpicu pada **59 dari 76 _run_** (78%). Jadi batas 30 _epoch_ jarang menjadi kendala pengikat — _early stopping_-lah yang menentukan durasi.
- **_Run_ tercepat berhenti di _epoch_ 15**, artinya AUC terbaiknya di _epoch_ 3 — konsisten dengan reset _counter_ saat _unfreeze_.
- **31 dari 76 _run_ mencapai AUC validasi terbaik pada _epoch_ ≥ 15.** Dengan _patience_ 5, sepertiga lebih eksperimen akan terpotong sebelum mencapai puncaknya.
- **Contoh konkret:** `hybrid_FFPP_n750_seed0` mencapai AUC terbaik **0,7006 pada _epoch_ 20** dari 30 _epoch_. Dengan _patience_ 5, pelatihan berhenti jauh sebelum itu dan hasilnya lebih buruk.

Tunjukkan `train.log`-nya bila diminta — barisnya jelas: `Epoch 4: unfreezing spatial backbone`, lalu AUC naik bertahap hingga _epoch_ 20.

---

## 6. Kalau Ditekan: "Kenapa tidak di-_tuning_ sama sekali?"

Jangan defensif. Belokkan ke temuan utama:

> "Selisih antara _spatial_ dan _hybrid_ pada n = 750 adalah **0,778 vs 0,644** AUC pada FFPP dan **0,971 vs 0,919** pada CDF — jarak sekitar 0,13 dan 0,05, sementara simpangan baku antar-_seed_ hanya ~0,01. Selisih sebesar itu tidak dapat ditutup dengan penyetelan _learning rate_. Kesimpulan bahwa fusi domain frekuensi tidak memberikan peningkatan pada rezim data terbatas tetap berdiri secara statistik."

Lalu tutup dengan: *"Penyetelan _hyperparameter_ spesifik per arsitektur merupakan keterbatasan penelitian ini dan telah dicantumkan sebagai saran penelitian lanjutan pada BAB V."*

✅ **Pastikan kalimat keterbatasan itu benar-benar ada di BAB V sebelum sidang.**

---

## 7. Angka yang Wajib Hafal

**Hasil _in-dataset_ n = 750 (AUC, _mean_ ± _std_ atas 3 _seed_):**

| Model | FFPP | CDF |
| --- | --- | --- |
| _spatial_ | **0,778 ± 0,010** | **0,971 ± 0,002** |
| _hybrid_ | 0,644 ± 0,009 | 0,919 ± 0,010 |
| _freq_ | 0,562 ± 0,007 | 0,562 ± 0,014 |

**Hasil lintas-dataset n = 750 (AUC):**

| Model | FFPP → CDF | CDF → FFPP |
| --- | --- | --- |
| _spatial_ | 0,678 ± 0,008 | 0,607 ± 0,020 |
| _hybrid_ | 0,665 ± 0,016 | 0,555 ± 0,031 |
| _freq_ | 0,606 ± 0,009 | 0,575 ± 0,012 |

**Konteks penting:** _hybrid_ **kalah** dari _baseline spatial_ di setiap tier yang andal. Ini temuan negatif dan harus disampaikan sebagai temuan, bukan disembunyikan — nilai ilmiahnya justru ada pada ketegasan pengukurannya (3 _seed_, 4 tier, 2 dataset, _hyperparameter_ dikontrol).

**Jangan pakai angka tier n = 100** sebagai bukti apa pun: _split_ ujinya hanya ~15 video, sehingga AUC di bawah 0,5 pada tier itu adalah derau _sampling_, bukan sinyal.

---

## 8. Checklist Pra-Sidang

- [ ] Perbaiki _batch size_ → 64 / efektif 128 (Tabel 3.9, §3.5.5, BAB IV §4.1)
- [ ] Perbaiki maks _frame_ → 100 (bagan alur BAB III, §3.2)
- [ ] Perjelas parameter XceptionNet → 20,8 juta tanpa _head_ (§3.4); _hybrid_ total → 25,9 juta
- [ ] Pastikan keterbatasan "tanpa _tuning_ per-arsitektur" tercantum di BAB V
- [ ] Siapkan `hybrid_FFPP_n750_seed0/train.log` agar bisa ditunjukkan (bukti _unfreeze_ + puncak _epoch_ 20)
- [ ] Hafal empat angka: 0,778 / 0,644 / 0,971 / 0,919
