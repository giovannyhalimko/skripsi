# REVISI BAB IV–V + Typo Sweep Menyeluruh — Fix Audit (ready copy-paste)

> **Konteks:** audit 3-auditor paralel (2026-07-07) atas BAB IV, BAB V, dan typo seluruh dokumen (docx terkini `CUR3.txt`, 2597 paragraf).
> **Kabar bagus:** **BAB IV bersih secara numerik** (semua Tabel 4.1–4.5 cocok persis dengan data CSV di `outputs/`; semua Δ/AUC aritmetik benar) dan **konsisten antar-bab** (Abstract ↔ BAB IV ↔ BAB V ↔ RM/H0 semua cocok; tidak ada over-claim tersisa di bab hasil/kesimpulan). Sisa = **1 kontradiksi faktual + 1 angka batas + typo + tidy-up.**
> **Cara pakai:** tiap blok = **cari** teks lama, **ganti** dengan teks baru.

---

## 🔴 FIX A (WAJIB, faktual) — Tabel 3.11: label smoothing "Dinonaktifkan" (docx line ~1901)

**Masalah:** keterangan baris _Label smoothing_ di Tabel 3.11 tertulis **"Dinonaktifkan untuk dataset kecil"** — **bertentangan** dengan config (`label_smoothing: 0.05`) dan prosa §3.5.4 (line 1836: "label smoothing **diaktifkan** dengan α = 0,05 … pada dataset berukuran kecil, mulai n = 100").

**CARI:** (baris Tabel 3.11) "Label smoothing … **Dinonaktifkan untuk dataset kecil**"
**GANTI:** kolom Nilai = **"α = 0,05"**, kolom Keterangan = **"Diaktifkan; regularisasi ringan untuk mencegah _overconfidence_ pada dataset kecil"**

---

## 🔴 FIX B (WAJIB, angka) — Batas bawah AUC cross-dataset 0,56 → 0,55 (line 2253 + Abstract)

**Masalah:** disebut "AUC berada pada kisaran **0,56**–0,68", tapi AUC cross-dataset **terendah** di Tabel 4.2 = **0,555** (hybrid CDF→FFPP). Batas bawah harus 0,55.

**CARI (BAB IV line 2253):** "…AUC berada pada kisaran **0,56–0,68**…"
**GANTI:** "…AUC berada pada kisaran **0,55–0,68**…"

**Juga di Abstrak** (Indo + English): "AUC sekitar **0,56–0,68**" → **0,55–0,68** (agar konsisten dengan tabel). *(Catatan: "0,56–0,61" untuk cabang frekuensi tetap benar, jangan diubah.)*

---

## 🔴 FIX C — Spasi hilang di heading bab (body)

- **line 2123:** "**BAB IVHASIL DAN PEMBAHASAN**" → "**BAB IV HASIL DAN PEMBAHASAN**"
- **line 2393:** "**BAB VPENUTUP**" → "**BAB V PENUTUP**"

## 🔴 FIX D — Titik ganda / titik nyasar

- **line 2361:** "…bukan _domain adaptation_**..** Dengan demikian…" → satu titik: "…_domain adaptation_**.** Dengan demikian…"
- **line 1832:** "…BCEWithLogitsLoss (persamaan 2.30)**.** dengan dua penyesuaian…" → "…(persamaan 2.30) dengan dua penyesuaian…"
- **line 1231:** "Model frekuensi**.** hanya menggunakan…" → "Model frekuensi**,** hanya menggunakan…" *(samakan dgn butir lain di list 1230/1232 yang pakai koma)*
- **line 1226:** "…XceptionNet [6]**.** yang telah terbukti…" → "…XceptionNet [6] yang telah terbukti…"

## 🔴 FIX E — Misspelling

- **line 2054** (Tabel 3.16): "NVIDIA **berdukungan** CUDA" → "NVIDIA **dengan dukungan** CUDA"
- **line 1587:** "pustaka **PyTroch** Image Models" → "**PyTorch**"
- **line 804:** "sebagaimana **dibahasa** pada subbab" → "**dibahas**"
- **line 376:** "**Alam el at.** menunjukkan" → "**Alam et al.**"
- **line 676:** "…kanal ke-**mmm** dari citra…" → "ke-**m**"
- **line 1081:** "semakin kecil **resiko** false accusation" → "**risiko**" *(dokumen konsisten pakai "risiko" di tempat lain)*

## 🔴 FIX F — "dibawah"/"diatas" → "di bawah"/"di atas" (baku, 5 tempat)
Lines **1059, 1074, 1081, 1088, 1096**. *(line 2040 sudah benar "di atas" — jadikan acuan.)*

## 🔴 FIX G — Typo judul di Daftar Pustaka
- [1] line 2419: "**Assesment**" → "**Assessment**"
- [16] line 2449: "**Deteciton**" → "**Detection**"; "**Enchanced**" → "**Enhanced**"
- [26] line 2469: "**Detectionin**" → "**Detection in**"
- [30] line 2477: "**Explainthe**" → "**Explain the**"
- [29] line 2475: "**in/CML**" → "**in ICML**"

---

## 🔴 FIX H (WAJIB — bukti) — Klaim hybrid-F1 unggul vs Gambar 4.9 (AUC) (line 2364)

**Terverifikasi dari CSV** (`outputs/tables/{n250,n500,n750}/Table2_cross_dataset_summary.csv`), arah **FFPP→CDF**:

| Tier | F1 hybrid | F1 spasial | AUC hybrid | AUC spasial |
|---|---|---|---|---|
| n=250 | **0,621** | 0,518 | 0,563 | 0,612 |
| n=500 | **0,552** | 0,490 | 0,620 | 0,659 |
| n=750 | 0,594 | **0,614** | 0,665 | 0,678 |

**Masalah:** klaim "hybrid melampaui spasial di n=250/500" **benar untuk F1**, TAPI **Gambar 4.9 memplot AUC** — dan di AUC **spasial unggul di SEMUA tier**. Jadi gambar tidak mendukung (tampak membantah) klaim itu. (Gambar 4.9 sudah memuat panel In-Dataset + Cross-Dataset, jadi caption benar; scope Tabel 4.4 "AUC In-Dataset" juga tidak salah — hanya lebih sempit dari gambar.)

**CARI (line 2364, kalimat terakhir paragraf RM2):**
> Pada tier n = 250 dan n = 500 yang dilaporkan pada analisis pendukung, F1 cross-dataset model hybrid bahkan melampaui model spasial pada arah ini.

**GANTI:**
> Pada tier n = 250 dan n = 500, F1-score cross-dataset model hybrid arah FFPP→CDF sedikit melampaui model spasial (n=250: **0,62 vs 0,52**; n=500: **0,55 vs 0,49**). Keunggulan ini hanya muncul pada **F1 di ambang 0,5** akibat keseimbangan recall yang lebih baik, dan **tidak tercermin pada AUC** yang tetap mengunggulkan model spasial di seluruh tier (Gambar 4.9); sehingga manfaat cabang frekuensi bersifat **parsial, bergantung arah, dan bergantung metrik**.

**Kenapa:** menjadikan angka F1 eksplisit (ada buktinya) + menjelaskan kontradiksi-semu dengan Gambar 4.9 (F1 vs AUC beda) → justru memperkuat kesimpulan "manfaat parsial", tidak bisa ditembak penguji.

## 🟡 FIX I — Perjelas scope angka & rapikan Δ
- **line 2301:** "model spasial hanya turun Δ = **+0,101**" — dari nilai tabel 0,778−0,678 = **0,100** (walau dari nilai tak-dibulatkan memang +0,101). Selaraskan (pakai +0,100 agar konsisten dengan angka yang ditampilkan, atau beri catatan "dari nilai tak-dibulatkan").
- **Abstract "0,56–0,68" (semua model)** vs **BAB V line 2396 "0,61–0,68" (spasial saja)** — keduanya benar untuk subset berbeda; **perjelas scope** di salah satu ("AUC spasial 0,61–0,68") agar tidak terbaca kontradiksi saat Q&A.

## 🟡 FIX J — Ejaan baku & nama (konsistensi)
- **CARI `dimana` → GANTI `di mana`** (relative pronoun, 2 kata). Find&Replace global (4×), atau per lokasi:
  - L443 "…dilatih secara bersamaan, **dimana** generator…"
  - L459 "…bersifat komplementer, **dimana** artefak spasial…"
  - L1192 "…representasi yang lebih lengkap, **dimana** FFT menangkap…"
  - L2361 "…RM1 terjawab, **dimana** detektor spasial…"
- **line 2404:** "informasi **fasa**" → "**fase**" (dokumen pakai "fase" di 558/560/2370).
- **line 1350:** kalimat run-on — beri titik setelah "…subbab 2.13.2**.** Pada bagian ini, transformasi…"
- **"Guera et al." → "Güera"** (lines 611, 622, 662; Daftar Pustaka [34] pakai umlaut; karya 2-penulis, "et al." dipertanyakan).
- **Nama Daftar Pustaka** (samakan dgn ejaan di prosa): [7] "Cozzoliono"→**Cozzolino**; [10] "Guidice"→**Giudice** (prosa 607 sudah "Giudice"); [45] "Loschilov"→**Loshchilov** (teks 985/1877 sudah "Loshchilov"); [12] "Zaho"→**Zhao**; [31] "Papadopoulus"→**Papadopoulos**.
- **magnitude vs magnitudo** dipakai bergantian — pilih satu, konsistenkan.

## 🟡 FIX K — Klaim FFT datar di BAB II (line 1167)
"FFT dipilih karena mampu mendeteksi artefak tersembunyi… dengan **kemampuan generalisasi yang lebih tinggi**." Dinyatakan sebagai fakta, padahal **hasil membantahnya**. Sudah dilunakkan di line 1144, tapi tidak di sini. **Saran:** ubah ke "…**dilaporkan** memiliki generalisasi lebih tinggi **(klaim yang diuji pada penelitian ini)**".

---

## 🟢 FIX L (verify — kemungkinan artefak ekstraksi, cek di Word)
- **line 2581:** Samuel — "Tempat/Tanggal Lahir: Binjai / 23 Juli **[tahun hilang?]**" — lengkapi tahun lahir.
- **lines 493–494:** kata "**Relatif**" tampak terpecah antar sel tabel ("…tinggi R" / "elatif stabil") — cek apakah benar terpecah di dokumen hidup.
- **Daftar Riwayat Hidup:** field tanpa spasi setelah titik dua ("NIM:221111798") — kemungkinan artefak sel tabel; cek layout asli.

## 🟢 FIX M — Refresh field
Setelah edit, **Ctrl+A → F9** (Update entire table) untuk Daftar Isi/Tabel/Gambar & penomoran.

---

## Checklist — VERIFIED 2026-07-07 (docx CUR4)
- [x] A — Tabel 3.11 "Diaktifkan, α=0,05" ✅
- [x] B — 0,55–0,68 (abstrak + L2253) ✅
- [~] C — ❌ **RETRACTED (false positive)**: "BAB IVHASIL"/"BAB VPENUTUP" itu heading dua-baris (line-break), semua BAB I–V begitu di extraction; di Word tampil normal. **Abaikan.**
- [x] D — titik ganda ✅
- [x] E — misspelling ✅
- [x] F — dibawah/diatas ✅
- [x] G — Daftar Pustaka judul ✅
- [x] H — klaim F1 + caveat AUC (L2364) ✅ *(verified 2026-07-07)*
- [x] I — Δ = +0,100 (L2301) ✅; sisa opsional: perjelas scope "0,56–0,68" (abstrak) vs "0,61–0,68" (BAB V, spasial)
- [x] J — `dimana`→`di mana` ✅ (count=0)
- [x] K — BAB II L1167 klaim FFT dilunakkan ✅
- [ ] L — **tahun lahir Samuel (L2581) masih kosong** ("Binjai / 23 Juli __") → isi tahun. *("Lahir:Medan" tanpa spasi = artefak sel tabel, abaikan; "Relatif" terpecah = artefak, abaikan.)*
- [ ] M — Ctrl+A → F9
- [ ] Opsional kosmetik: Güera, nama DP (Cozzolino/Giudice/Loshchilov/Zhao), magnitude/magnitudo, run-on L1350

**Ringkasan (2026-07-07): A–K SEMUA ✅, regresi 0.** Sisa hanya **L** (tahun lahir Samuel — personal) + **M** (F9) + opsional kosmetik. BAB IV/V praktis tuntas.
