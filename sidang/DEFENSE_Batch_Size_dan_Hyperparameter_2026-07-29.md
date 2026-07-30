# 🛡️ Defense — Batch Size & Landasan Hyperparameter (Item 5 & 6)

**Tanggal:** 2026-07-29
**Pertanyaan penguji (Mustika):** (Item 6) "Dasar penyusunan hyperparameter ada landasannya?" (Tabel 3.11, hal 95) · **inti: batch size, dan kenapa efektif.** (Item 5) "Probabilitas 5%, dasarnya?" (hal 79).
**Sumber angka (terverifikasi):** `deepfake_hybrid/config.yaml`, `vast_run.sh` (auto-tune VRAM), Tabel 3.10 & 3.11 di `.docx`, cheatsheet `documents/CHEATSHEET_Hyperparameter_Sidang_2026-07-27.md`.

---

## 0. Ground truth — angka kanonik (yang harus dipertahankan)

| Parameter | Nilai (laporan / run kanonik) | config.yaml (default lokal) |
|---|---|---|
| Batch size (per langkah) | **64** | ⚠️ **16** |
| Gradient accumulation | 2 → **batch efektif 128** | 2 |
| Learning rate (base) | **2 × 10⁻⁴** | 2.0e-4 ✅ cocok |
| LR backbone | 2 × 10⁻⁵ (base/10) | (dihitung di train.py) |
| LR cabang freq | 5 × 10⁻⁵ (base×0,25) | (train.py) |
| Weight decay | 1 × 10⁻⁴ (decoupled) | 1.0e-4 ✅ |
| max_frames/video | **100** | ⚠️ **50** |
| Label smoothing | 0,05 | 0.05 ✅ |

**Dari mana 64?** `vast_run.sh` memilih batch otomatis menurut VRAM GPU: A100/H100 (≥35 GB) → 128, GPU 14–24 GB (T4/V100/3090/4090) → **64**, sisanya → 32. Colab Pro memberi **T4/V100 (16 GB)** → tier 64. Nilai final disimpan permanen di setiap `best.pt`. Jadi 64 bukan angka karangan, melainkan hasil kapasitas GPU yang dipakai.

---

## ⚠️ 1. VULNERABILITY yang HARUS diberesin dulu

`config.yaml` masih tertulis **`batch_size: 16`** dan **`max_frames_per_video: 50`**, padahal laporan (Tabel 3.11 + narasi §3.5.5) menyebut **64** dan **100**. Narasi laporan bahkan berbunyi *"Seluruh hyperparameter dipusatkan pada config.yaml… batch size 64…"* — ini **kontradiktif**: kalau penguji buka `config.yaml`, tertulis 16, bukan 64.

**Pilihan perbaikan (pilih satu, saya bisa bantu terapkan):**
- **(A, rekomendasi)** Ubah `config.yaml`: `batch_size: 64`, `max_frames_per_video: 100` → semua konsisten dengan laporan. Aman karena run kanonik memang pakai nilai ini.
- **(B)** Biarkan `config.yaml` (default lokal untuk smoke-test), tapi **ubah narasi** §3.5.5 menjadi: *"nilai default pada config.yaml (16) dinaikkan otomatis oleh skrip peluncuran (`vast_run.sh`) sesuai kapasitas VRAM GPU menjadi 64 pada GPU kelas 16 GB."* Jangan klaim config.yaml "memusatkan" batch 64.

> Catatan: checkpoint lama di `outputs/runs/` (batch 16, **lr 1e-4**) adalah **run eksplorasi lama, BUKAN hasil skripsi**. Hasil BAB IV = run `gpu_pull_2026-06-19` (batch 64, lr 2e-4). Kalau penguji menemukan checkpoint 16/1e-4, jawab: itu run uji-coba awal, bukan yang dilaporkan.

---

## 2. 🎯 BATCH SIZE — jawaban inti: "kenapa 64 (efektif 128) dan kenapa efektif?"

Susun jawaban 3 lapis: **(a) kenapa nilainya begitu → (b) kenapa efektif secara teknis → (c) framing metodologis.**

### (a) Kenapa 64 / efektif 128
> "Batch 64 per langkah adalah kapasitas maksimum yang muat di VRAM GPU Colab Pro (16 GB) yang kami pakai. Untuk memperbesar batch secara statistik tanpa menambah kebutuhan memori, digunakan **gradient accumulation 2 langkah**, sehingga gradien dari 2 mini-batch dijumlahkan sebelum satu pembaruan bobot — **batch efektif menjadi 64 × 2 = 128**."

### (b) Kenapa efektif (landasan teknis — ini yang ditanya)
1. **Stabilitas BatchNorm (alasan terkuat).** Seluruh XceptionNet dan FreqCNN memakai **BatchNorm** di tiap blok. BatchNorm menormalisasi aktivasi memakai rata-rata & varians **per mini-batch**. Pada batch sangat kecil, statistik ini berisik dan akurasi BN anjlok (Ioffe & Szegedy, 2015; Wu & He, 2018 menunjukkan error BN naik tajam di bawah ~16–32). **Batch 64 memberi statistik BN yang stabil** → pelatihan stabil. Ini justifikasi paling langsung untuk arsitektur yang BN-heavy seperti Xception.
2. **Varians estimasi gradien lebih rendah.** Gradien mini-batch adalah estimasi berisik dari gradien sebenarnya; batch lebih besar → estimasi lebih halus → penurunan loss lebih stabil. Penting di sini karena banyak **frame dari video yang sama sangat berkorelasi**; batch 128 mencampur lebih banyak video per pembaruan sehingga sinyal gradien lebih representatif.
3. **Efektif 128 tanpa biaya VRAM.** Gradient accumulation **memisahkan ukuran batch statistik dari batas memori** — kita dapat manfaat kestabilan batch 128 di GPU yang hanya muat 64 (Goyal et al., 2017).
4. **Selaras dengan learning rate.** Batch efektif lebih besar mendukung LR stabil yang sedikit lebih tinggi (aturan penskalaan linear, Goyal et al., 2017; Smith et al., 2018). Base LR 2×10⁻⁴ yang dipakai konsisten dengan batch efektif 128.
5. **Tidak terlalu besar (jaga generalisasi).** Batch sangat besar diketahui memperburuk generalisasi ("generalization gap", Keskar et al., 2017). **128 itu moderat** — cukup besar untuk stabil, cukup kecil untuk tetap ada noise yang meregularisasi. Jadi ini titik seimbang, bukan sekadar "makin besar makin bagus".

### (c) Framing metodologis (tutup dengan ini)
> "Yang terpenting, batch size adalah **variabel kontrol**, disamakan pada ketiga arsitektur (spatial/freq/hybrid), dua dataset, empat ukuran sampel, dan tiga seed. Nilainya ditentukan kapasitas GPU, bukan di-tuning per model — supaya perbedaan performa murni berasal dari arsitektur, bukan dari usaha tuning yang berbeda."

**Referensi pendukung (untuk dikutip di §3.5.5 — lihat Item 2):**
- Ioffe & Szegedy (2015), *Batch Normalization* — BN butuh batch memadai. *(kemungkinan sudah ada di BAB II — cek)*
- Wu & He (2018), *Group Normalization* — BN memburuk pada batch kecil.
- Keskar et al. (2017), *On Large-Batch Training for Deep Learning* — generalization gap.
- Goyal et al. (2017), *Accurate, Large Minibatch SGD* — batch efektif & penskalaan LR.

---

## 3. Learning Rate — jawaban soal "LR uncited / tidak ada di cheatsheet"

**Klarifikasi:** LR di laporan = **base 2×10⁻⁴, backbone 2×10⁻⁵, cabang freq 5×10⁻⁵** (Tabel 3.10 & 3.11). Nilai ini **cocok** dengan `config.yaml` (2e-4) dan cheatsheet. Angka **1e-4** yang mungkin Anda temukan ada di checkpoint lama `outputs/runs/` — itu **run eksplorasi, bukan hasil skripsi**.

**Kenapa "uncited"?** Nilai 2×10⁻⁴ memang **tidak punya satu paper tunggal** yang mematoknya — ia default empiris standar untuk fine-tuning. Landasan yang bisa dipertahankan:
- **Besaran (orde 10⁻⁴):** rentang standar fine-tuning AdamW pada backbone pretrained (1e-4–3e-4); Adam default 1e-3 terlalu besar dan merusak bobot ImageNet.
- **Backbone = base/10 & cabang freq = base×0,25 (differential/discriminative LR):** melindungi bobot pretrained dari gradien besar head acak. Landasan: **Howard & Ruder (2018), ULMFiT — discriminative fine-tuning** (lapisan berbeda, LR berbeda). Cocok dikutip di §3.5.2.
- **AdamW-nya:** Loshchilov & Hutter (2019) — sudah dikutip (ref [46]).
- **Framing:** sama seperti batch — variabel kontrol, praktik standar, bukan hasil grid search (grid search 24 sel × 3 seed tak muat anggaran GPU; sudah dicatat sebagai keterbatasan di BAB V).

**Jawaban singkat kalau ditanya "dasar LR?":**
> "LR mengikuti praktik standar fine-tuning: base 2×10⁻⁴ (orde 10⁻⁴, aman untuk backbone ImageNet), dengan differential learning rate — backbone 10× lebih kecil untuk melindungi bobot pretrained, mengikuti prinsip discriminative fine-tuning (Howard & Ruder, 2018). Nilainya variabel kontrol yang identik di semua model, bukan hasil tuning per model."

---

## 4. Item 5 — "Probabilitas 5%" (hal 79) = Spectral Band Masking

Ditemukan di §3.x augmentasi: *"Spectral band masking dengan probabilitas 5%: sebuah pita horizontal/vertikal selebar acak 1–N piksel diisi nol, orientasi 50:50."* Jadi 5% = **peluang menerapkan augmentasi spectral band masking per sampel** (bukan signifikansi statistik).

**Dasar 5%:** augmentasi frekuensi harus **probabilitas rendah** — kalau terlalu sering, terlalu banyak informasi spektral dihapus dan sinyal artefak (yang justru jadi fitur deteksi) ikut rusak. 5% cukup untuk meregularisasi (mencegah model bergantung pada satu pita frekuensi) tanpa merusak sinyal. Bandingkan RandomErasing 10% (domain spasial, lebih toleran). **Framing:** design choice konservatif, variabel kontrol, bukan hasil tuning.

> Kalau ingin lebih kuat: bisa dikaitkan ke praktik spectral/frequency masking pada SpecAugment (Park et al., 2019) yang juga memakai masking pita frekuensi sebagai regularisasi.

---

## 5. Ringkas — yang perlu dilakukan

- ☐ **Beresin config.yaml vs laporan** (opsi A: set batch 64 & max_frames 100; atau opsi B: ubah narasi). **← paling penting, mudah ketahuan penguji.**
- ☐ (Item 2) Tambah 3–4 referensi batch/BN ke daftar pustaka + sitasi di §3.5.5 (Ioffe & Szegedy, Keskar, Goyal, Wu & He) dan Howard & Ruder di §3.5.2.
- ☐ Hafalkan jawaban 3-lapis batch size (§2) + jawaban singkat LR (§3) + 5% (§4).
- ☐ (opsional) Tulis 1 paragraf "landasan pemilihan hyperparameter" di bawah Tabel 3.11 yang menyebut: variabel kontrol + praktik standar transfer learning + keterbatasan grid search.
