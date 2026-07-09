# REVISI BAB III (+ Tabel 4.1) — Fix Sisa Audit (ready copy-paste)

> **Konteks:** re-check menyeluruh BAB I–III 2026-07-07 (lihat `SIDANG_FactCheck_QA_2026-06-30.md` blok "🔁 STATUS RE-CHECK MENYELURUH BAB I-III"). **Mayoritas Item 1–41 sudah kamu terapkan** ✅ (metrik+AUC, EfficientNet dihapus, framing RM, ekstraksi sekuensial, face-crop sitasi, requires_grad_(True), §3.6.1, Δ para, dst). File ini memuat **sisa** yang belum: **3 fix wajib + 4 typo + 3 opsional/verify + 1 refresh field**.
> **Cara pakai:** tiap blok = **cari** teks lama di Word, **ganti** dengan teks baru.

---

## 🔴 FIX 1 (WAJIB) — §3.5.4 Label smoothing masih mengulang BAB II 2.32 (Item 37, docx line 1837)

**CARI (teks lama):**
> Dengan α = 0,02, transformasi label mengubah 0 → 0,01 dan 1 → 0,99 sehingga model tidak perlu mendorong logit ke nilai ekstrem. Pada konfigurasi akhir eksperimen, label smoothing diaktifkan dengan α = 0,05 sebagai regularisasi ringan untuk mencegah overconfidence pada dataset berukuran kecil (mulai n = 100).

**GANTI (teks baru):**
> _Label smoothing_ diaktifkan dengan **α = 0,05** (persamaan 2.32) sebagai regularisasi ringan untuk mencegah _overconfidence_ pada dataset berukuran kecil (mulai n = 100).

**Kenapa:** kalimat "α = 0,02 → 0,01/0,99" menurunkan ulang mekanisme yang sudah dijelaskan di BAB II (persamaan 2.32) — duplikasi. Angka 0,02 juga bukan nilai final (config = 0,05). Cukup nyatakan nilai yang dipakai + rujuk rumus. (Bagian pos_weight di atasnya **sudah** kamu perbaiki jadi "pos_weight ≈ 1" ✅.)

---

## 🔴 FIX 2 (WAJIB) — §3.5.5 AdamW menurunkan ulang penjelasan BAB II 2.15.2/2.15.3 (docx line 1852)

**CARI (teks lama):**
> Optimizer yang digunakan adalah AdamW [45], varian dari Adam [44] dengan decoupled weight decay, dengan konfigurasi lr = 2 × 10⁻⁴ dan weight_decay = 1 × 10⁻⁴. Berbeda dengan Adam standar yang menambahkan regularisasi L2 ke gradien sebelum penskalaan adaptif, AdamW menerapkan weight decay secara langsung pada bobot setelah langkah pembaruan Adam. Perbedaan ini penting karena pada Adam standar, efektif regularisasi bervariasi antar parameter bergantung pada learning rate adaptifnya, sedangkan pada AdamW, regularisasi konsisten untuk semua parameter. Konsistensi ini sangat bermanfaat dalam skenario transfer learning di mana parameter pretrained dan parameter baru memiliki skala gradien yang sangat berbeda.

**GANTI (teks baru):**
> _Optimizer_ yang digunakan adalah **AdamW** (Loshchilov & Hutter, 2019) dengan konfigurasi lr = 2×10⁻⁴ dan _weight_decay_ = 1×10⁻⁴. Alasan pemilihan AdamW dibanding Adam standar (_decoupled weight decay_) telah diuraikan pada §2.15.2–2.15.3; konsistensi regularisasi antar-parameter tersebut penting pada skenario _transfer learning_ di mana parameter _pretrained_ dan parameter baru memiliki skala gradien yang berbeda.

**Kenapa:** penjelasan "Berbeda dengan Adam standar… menerapkan weight decay langsung…" adalah isi §2.15.2 (AdamW: Decoupled Weight Decay) dan §2.15.3 (Keunggulan AdamW). BAB III cukup menyebut nilai + rujuk balik. Pola sama seperti FIX 1.

---

## 🔴 FIX 3 (WAJIB) — Tabel 4.1 (BAB IV) duplikat Tabel 3.12 (Item 41, docx line 2131)

**Masalah:** Tabel 4.1 "Matriks Eksperimen" isinya identik dengan Tabel 3.12 (BAB III). BAB IV sudah **merujuk** Tabel 3.11/3.16/3.17 tanpa menyalinnya — matriks harus diperlakukan sama. Tabel 3.12 juga lebih benar (memisahkan 72 pelatihan vs 144 evaluasi; Tabel 4.1 keliru menaruh "skenario evaluasi" sebagai faktor matriks).

**AKSI:** **hapus Tabel 4.1** dan ganti seluruh §4.1.1 dengan versi berikut:

> **4.1.1 Lingkungan dan Konfigurasi Eksperimen**
>
> Seluruh eksperimen dijalankan pada lingkungan komputasi berbasis GPU dengan kerangka kerja PyTorch dan pustaka _timm_ untuk _backbone_ XceptionNet; spesifikasi perangkat keras dan lunak dirinci pada Tabel 3.16 dan Tabel 3.17. Konfigurasi _hyperparameter_ konsisten untuk seluruh model (dirangkum pada Tabel 3.11): _optimizer_ AdamW (_learning rate_ dasar 2×10⁻⁴), _gradient accumulation_ dua langkah (_batch_ efektif 32), _early stopping_ berdasarkan AUC validasi dengan _patience_ 12, serta pembekuan _backbone_ selama tiga _epoch_ pertama. Pemilihan model terbaik didasarkan pada AUC validasi tertinggi.
>
> Evaluasi mengikuti **matriks eksperimen penuh yang telah dirancang pada §3.6.1 (Tabel 3.12)**, yaitu kombinasi tiga model (spasial, frekuensi, _hybrid_) × dua dataset (FFPP, CDF) × empat ukuran sampel (100, 250, 500, 750) × tiga _seed_, menghasilkan **72 pelatihan dan 144 evaluasi**. Pengujian dilakukan pada dua arah, yaitu _in-dataset_ (FFPP→FFPP, CDF→CDF) dan _cross-dataset_ (FFPP→CDF, CDF→FFPP), dengan metrik _accuracy_, _precision_, _recall_, F1-_score_, dan AUC. Khusus pada tier ukuran sampel terkecil (n = 100), set pengujian hanya terdiri atas sekitar 15 video sehingga rentan terhadap _noise_ pencuplikan; oleh karena itu analisis utama bab ini bertumpu pada tier yang lebih andal, yaitu n = 250, n = 500, dan n = 750, dengan n = 750 sebagai representasi utama.

**⚠️ Konsekuensi:** menghapus Tabel 4.1 menggeser nomor tabel BAB IV (4.2→4.1, 4.3→4.2, dst). Lakukan **Ctrl+A → F9** dan cek rujukan silang (lihat FIX 10).

---

## 🟡 FIX 4 — Typo caption Gambar 3.10 (docx line 322 / caption)

**CARI:** "Diagram **Aristektur** HybridTwoBranch (Late Fusion)"
**GANTI:** "Diagram **Arsitektur** HybridTwoBranch (Late Fusion)"
*(Perbaiki di caption gambarnya; Daftar Gambar akan auto-update saat F9.)*

## 🟡 FIX 5 — Grammar "adalah" (docx line 1721)

**CARI:** "…terletak pada domain informasi yang dieksploitasi **adalah** model spasial mengandalkan fitur visual…"
**GANTI:** "…terletak pada domain informasi yang dieksploitasi**:** model spasial mengandalkan fitur visual…"

## 🟡 FIX 6 — Typo method AMP (docx line 1856)

**CARI:** "…**scaler.unscale()** dipanggil sebelum clipping…"
**GANTI:** "…**scaler.unscale_()** dipanggil sebelum clipping…" *(ada underscore; itu nama method PyTorch yang benar)*

## 🟡 FIX 7 — Spasi hilang (docx line 1336)

**CARI:** "…pada mode face-crop **denganMTCNN** yang digunakan…"
**GANTI:** "…pada mode face-crop **dengan MTCNN** yang digunakan…"

---

## 🟢 FIX 8 (opsional) — Selaraskan contoh α di BAB II (docx line 1006)

**CARI:** "Dengan α kecil (mis. 0,02), label biner 0 dan 1 berubah menjadi 0,01 dan 0,99, sehingga model tidak perlu mendorong logit ke nilai ekstrem (±∞)."
**GANTI:** "Dengan α kecil (mis. **0,05** yang dipakai pada penelitian ini), label biner 0 dan 1 dilunakkan menjadi **0,025 dan 0,975**, sehingga model tidak perlu mendorong logit ke nilai ekstrem (±∞)."
**Kenapa:** BAB II pakai 0,02 (sisa nilai lama) sedangkan config = 0,05; menyamakan menutup celah "kok angkanya beda".

## 🟢 FIX 9 (verify) — §2.18.3 recap (Item 30, docx line 1191)

§2.18.3 "Perbandingan Akurasi dan Ketahanan Metode FFT dan XceptionNet" masih ada. **Pastikan** sudah dipangkas dari ~75% recap §2.18.1+§2.18.2 (mengulang poin XceptionNet unggul in-dataset & FFT lebih tahan lintas-dataset). Kalau masih mengulang, jadikan **sintesis/tabel perbandingan singkat**, bukan paragraf naratif ulang. *(Kirim isi terkini kalau mau kucek.)*

## 🟢 FIX 10 (opsional) — early_fusion (docx line 508-513)

Subbab "Early Fusion" + klausa "alternatif konseptual, tidak dievaluasi" **tidak salah/tidak misleading** (sudah diframing benar). Boleh **tetap** (memosisikan pilihan late fusion) atau **dihapus** untuk ketat. Jika dihapus: buang subbab Early Fusion (508-509) + klausa "alternatif konseptual" (513), **pertahankan** kalimat kontras "…bukan sebagai kanal tambahan (early fusion)" (715).

---

## 🟢 FIX 11 — Refresh field + cek penomoran tabel BAB IV

Setelah semua edit (khususnya FIX 3), tekan **Ctrl+A → F9**. Lalu **spot-check**:
- Nomor tabel BAB IV bergeser (Tabel 4.2→4.1, dst) — rujukan silang "Tabel 4.3"/"Tabel 4.4"/"Tabel 4.5" di prosa **harus ikut ter-update** (kalau field). Cek kalau ada yang **diketik manual**.
- Daftar Gambar/Tabel & penomoran persamaan (3.15–3.17 contoh loss) konsisten.

---

## Checklist eksekusi — VERIFIED 2026-07-07
- [x] FIX 1 — label smoothing dup α=0,02 ✅ *(α=0,02 hilang, tinggal 0,05)*
- [x] FIX 2 — AdamW re-derive BAB II ✅ *(rujuk §2.15.2–2.15.3)*
- [x] FIX 3 — hapus Tabel 4.1, rewrite §4.1.1 ✅ *(matriks jadi rujukan Tabel 3.12)*
- [x] FIX 4 — typo "Aristektur" ✅ *(0 kemunculan)*
- [x] FIX 5 — grammar "adalah" → ":" ✅
- [x] FIX 6 — "scaler.unscale_()" ✅
- [x] FIX 7 — "dengan MTCNN" ✅
- [x] FIX 8 — BAB II α=0,05 ✅
- [x] FIX 9 — §2.18.3 kini sintesis + Tabel 2.9 (bukan recap) ✅
- [ ] FIX 10 — early_fusion tetap/hapus *(opsional — keputusanmu)*
- [x] FIX 11 — Daftar Tabel refresh ✅ *(verified 2026-07-07: Daftar Tabel = 4.1–4.5, cocok body)*

**Status: SEMUA fix wajib/typo/verify TUNTAS.** Hanya tersisa FIX 10 (early_fusion) yang memang opsional/keputusanmu.
