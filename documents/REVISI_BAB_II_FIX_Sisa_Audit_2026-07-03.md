# REVISI BAB II — Fix Sisa Audit (ready copy-paste)

> **Konteks:** hasil audit menyeluruh BAB II (lihat `SIDANG_FactCheck_QA_2026-06-30.md` blok "🔬 AUDIT BAB II"). Mayoritas item **sudah** diperbaiki. File ini memuat **sisa** yang belum: **3 fix wajib + 2 typo + 1 refresh field**.
> **Cara pakai:** tiap blok = **cari** teks lama di Word, **ganti** dengan teks baru. Sitasi format (Nama, Tahun) — sesuaikan nomor bila kamu pakai IEEE.

---

## 🔴 FIX 1 (WAJIB) — Daftar metrik evaluasi kehilangan AUC (Item 23, docx line 856)

**CARI (teks lama):**
> Pada penelitian ini, metrik evaluasi yang digunakan meliputi Confusion Matrix, Accuracy, Precision, Recall, dan F1-Score. Seluruh metrik dihitung berdasarkan hubungan antara hasil prediksi model dan kelas sebenarnya pada data uji.

**GANTI (teks baru):**
> Pada penelitian ini, metrik evaluasi yang digunakan meliputi _Confusion Matrix_, _Accuracy_, _Precision_, _Recall_, _F1-Score_, dan _Area Under the ROC Curve_ (AUC). Metrik _Accuracy_, _Precision_, _Recall_, dan _F1-Score_ dihitung dari hasil prediksi model pada ambang tertentu (θ = 0,5) terhadap kelas sebenarnya, sedangkan AUC dihitung dari skor probabilitas model sehingga bersifat independen terhadap ambang. AUC digunakan sebagai **metrik utama** untuk seleksi model dan _early stopping_ karena tahan terhadap ketidakseimbangan kelas dan tidak bergantung pada pemilihan ambang.

**Kenapa:** AUC adalah metrik utama (seleksi model + _early stopping_ di kode `train.py`), disebut di abstrak, BAB I, §2.16.6, dan seluruh BAB IV — tetapi hilang dari daftar ini. Menyamaratakan "seluruh metrik dari hasil prediksi" juga keliru untuk AUC (AUC dari skor probabilitas).

---

## 🔴 FIX 2 (WAJIB) — "channel 4" (early fusion) di prosa preprocessing (Item 11, docx line 812)

**CARI (teks lama):**
> Maka dari itu, penelitian ini menambahkan informasi Frekuensi ke dalam informasi citra sebagai channel 4 yang akan membawa informasi mengenai penyebaran frekuensi.

**GANTI (teks baru):**
> Maka dari itu, penelitian ini memproses informasi frekuensi pada **cabang terpisah (FreqCNN)** dan menggabungkannya dengan fitur spasial pada tahap **_late fusion_**, bukan sebagai kanal tambahan pada masukan XceptionNet.

**Kenapa:** model yang dievaluasi adalah **late fusion** (dua cabang terpisah), bukan _early fusion_ 4-kanal. Frasa "channel 4" bertentangan dengan arsitektur sebenarnya.

---

## 🔴 FIX 3 (WAJIB) — Tabel 2.8: parameter MesoNet salah + caption over-cite (Item 28)

**Masalah:** parameter MesoNet ditulis **"4M"** — MesoNet/MesoInception-4 sebenarnya hanya **~28 ribu parameter (~0,03M)**, memang sengaja dibuat "mesoscopic" (kecil). Caption "[3, 4, 13, 7]": angka FF++ hanya bersumber dari **Afchar (2018)** dan **Rössler et al. (2019)**; Haq [3] memakai Celeb-DF dan SpecXNet [13] tidak menguji model-model ini.

**Tabel 2.8 versi benar:**

| Model | Akurasi (FaceForensics++) | Jumlah Parameter | Kelebihan |
| ----- | ------------------------- | ---------------- | --------- |
| _MesoNet_ | 83,10% (HQ/c23) | ~0,03 juta (~28 ribu) | Ringan, cepat |
| _XceptionNet_ | 96–99% | 22 juta | Akurasi tertinggi, efisien |

**Caption:** "Tabel 2.8 Perbandingan performa model CNN pada FaceForensics++ (Afchar et al., 2018; Rössler et al., 2019)."

> Versi HTML siap-tempel (tanpa baris parameter yang meragukan) juga tersedia: `documents/table/tabel_2_8_perbandingan_model_cnn.html`. Kalau ingin **mempertahankan** kolom parameter, cukup ganti "4M" → "~0,03 juta" seperti tabel di atas.

---

## 🟡 FIX 4 — Typo (docx line 597)

**CARI:** "...memadukan spasial-frekuensi, melalui mekanisme **ynag** berbeda..."
**GANTI:** "...melalui mekanisme **yang** berbeda..."

## 🟡 FIX 5 — Typo (docx line 956)

**CARI:** "...pendekatan hybrid tersebut **sebagai besar** dioptimalkan untuk performa in-dataset..."
**GANTI:** "...pendekatan hybrid tersebut **sebagian besar** dioptimalkan untuk performa in-dataset..."

---

## 🟢 FIX 6 — Refresh field sitasi (verifikasi penomoran)

Setelah semua edit, tekan **Ctrl+A → F9** ("Update entire table") untuk me-refresh nomor sitasi & daftar. Lalu **spot-check** khususnya:
- Sitasi **Celeb-DF** ([Item 19](#)) — pastikan me-resolve ke **Li et al., 2020** (bukan Luo & Wang / Frequency-Domain Masking). Di Daftar Pustaka sekarang urutannya sudah FDM lalu Celeb-DF, jadi in-text FDM=[17] & Celeb-DF=[18] tampak konsisten — tetap dikonfirmasi setelah refresh.

---

---

# TAMBAHAN dari Cek Ulang Thorough Round 2 (2026-07-03)

> FIX 1–5 sudah kamu terapkan ✅. Berikut sisa dari pass kedua.

## 🔴 FIX 7 (WAJIB) — ResNet-50 ">90% pada FaceForensics++" tak terdukung (intro §2.1, docx line 286)

**CARI:**
> ResNet-50 memperkenalkan residual learning untuk merepresentasikan fitur spasial yang lebih dalam, dan dilaporkan mencapai akurasi di atas 90% pada FaceForensics++ (FFPP) namun turun signifikan ketika diuji lintas dataset [3, 5].

**GANTI:**
> ResNet-50 memperkenalkan _residual learning_ untuk merepresentasikan fitur spasial yang lebih dalam (He et al., 2015), namun performanya pada deteksi deepfake dilaporkan lebih rendah dibanding XceptionNet dan menurun pada pengujian lintas dataset (Haq, 2021).

**Kenapa:** Haq [3] memakai **Celeb-DF** (akurasi ResNet-50 = 79%, XceptionNet lebih baik), He [5] = ImageNet. Tidak ada sumber ResNet-50 >90% di FaceForensics++.

**Sekalian** di kalimat berikutnya: "...99,26% pada FaceForensics++ tanpa kompresi **[6, 7]**" → cukup **(Rössler et al., 2019)** ([6] Chollet = ImageNet, tak melaporkan angka FF++).

## 🟡 FIX 8 — Typo "Lao et al." (docx line 462)

**CARI:** "...Tan et al. dan **Lao et al.** juga menunjukkan..."
**GANTI:** "...Tan et al. dan **Luo dan Wang** juga menunjukkan..." (Frequency-Domain Masking).

## 🟡 FIX 9 — Sitasi menggantung setelah titik (docx line 462)

**CARI:** "...dalam mendeteksi citra sintetis. **[11]** Hasanaath et al. ... generalisasi antar-dataset. **[16]** Tan et al. ..."
**GANTI:** pindahkan sitasi ke **sebelum** titik: "...dalam mendeteksi citra sintetis **[11]**. Hasanaath et al. ... generalisasi antar-dataset **[16]**. Tan et al. ..." (dan "membuktikan" → "menunjukkan").

## 🟡 FIX 10 — Statistik "96%" berulang (line 285 & 348)

Statistik "96% video deepfake ... pornografi non-konsensual [2]" muncul dua kali. Pertahankan **sekali** (disarankan di §2.1.1 line 348), dan di intro bab (line 285) cukup rujuk tanpa mengulang angka.

---

## Checklist eksekusi
- [ ] FIX 1 — AUC masuk daftar metrik (line 856) ✅ *(sudah)*
- [ ] FIX 2 — "channel 4" → late fusion (line 812) ✅ *(sudah)*
- [ ] FIX 3 — Tabel 2.8: MesoNet param ✅ *(sudah)*
- [ ] FIX 4 — typo "ynag" ✅ *(sudah)*
- [ ] FIX 5 — typo "sebagai besar" ✅ *(sudah)*
- [ ] FIX 7 — ResNet-50 >90% FFPP (line 286) **← wajib**
- [ ] FIX 8 — "Lao et al." → "Luo dan Wang" (line 462)
- [ ] FIX 9 — sitasi menggantung [11]/[16] (line 462)
- [ ] FIX 10 — statistik "96%" berulang (line 285/348)
- [ ] FIX 6 — Ctrl+A → F9, verifikasi sitasi Celeb-DF

Setelah ini, BAB II tuntas sesuai audit.
