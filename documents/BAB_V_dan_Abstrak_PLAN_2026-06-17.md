# PLAN — BAB V (Kesimpulan dan Saran) + Abstrak

**Tanggal:** 2026-06-17
**Dasar:** hasil settle `d28efae`; BAB IV sudah lengkap (4.2 menjawab RM1–RM3).
**Framing wajib:** studi **komparatif** + **temuan negatif yang jujur** (hybrid TIDAK mengungguli baseline spasial). Jangan mengklaim hybrid unggul. Selaras judul: "Studi Komparatif … terhadap Model Domain Tunggal".

---

## BAGIAN 1 — BAB V KESIMPULAN DAN SARAN

Struktur pedoman: **5.1 Kesimpulan** (menjawab tiap Rumusan Masalah, ringkas, tanpa data mentah baru) + **5.2 Saran** (tindak lanjut). Tiap heading diawali paragraf pembuka (konsisten gaya BAB I–IV).

### 5.1 Kesimpulan
**Paragraf pembuka:** nyatakan ulang tujuan secara ringkas — penelitian membandingkan kontribusi domain spasial, frekuensi, dan gabungannya (hybrid) untuk deteksi deepfake pada skenario in-dataset & cross-dataset. Lalu sajikan kesimpulan per rumusan masalah (boleh sebagai paragraf atau poin):

- **Jawaban RM1 (penurunan spasial cross-dataset):** detektor spasial murni (XceptionNet) mengalami penurunan performa substansial saat lintas dataset — AUC turun dari 0,78–0,97 (in-dataset) menjadi ~0,63–0,65, disertai keruntuhan *recall* (terparah arah CDF→FFPP, *recall* ≈ 0,08; *generalization drop* F1 hingga +0,76).
- **Jawaban RM2 (pengaruh FFT):** penambahan analisis frekuensi **memperkecil** *generalization drop* hanya pada arah FFPP→CDF (Δ hybrid +0,03 vs spasial +0,12) dan **tidak konsisten** pada arah sebaliknya; tanpa peningkatan AUC yang menyeluruh, serta **mengorbankan** performa in-dataset. Jadi manfaatnya **parsial dan bergantung arah**.
- **Jawaban RM3 (kontribusi komponen):** domain **spasial** adalah penyumbang utama (AUC hingga 0,969); cabang **frekuensi** nyaris setara tebakan acak (AUC 0,55–0,59); akibatnya model **hybrid tidak mengungguli** baseline spasial murni pada seluruh tier in-dataset yang andal.
- **Kesimpulan menyeluruh:** dalam konfigurasi yang diuji, arsitektur hybrid XceptionNet–FFT **belum** memberikan keunggulan dibanding baseline spasial; kontribusi domain frekuensi terbatas dan generalisasi lintas dataset tetap menjadi tantangan terbuka. Temuan negatif ini sahih secara ilmiah dan menjadi dasar saran perbaikan.

> Hindari: klaim "hybrid meningkatkan deteksi", "fusi terbukti unggul". Boleh: "ablation menunjukkan…", "temuan menunjukkan kontribusi frekuensi terbatas…".

### 5.2 Saran
**Paragraf pembuka:** arahkan saran pada (a) perbaikan metode dan (b) penelitian lanjutan, berbasis akar penyebab di 4.2.4. Poin:

- **Memperkuat cabang frekuensi:** gunakan representasi frekuensi yang lebih tahan terhadap *face-cropping* + kompresi (mis. tanpa crop / multi-skala / fitur fasa), atau praproses FFT pada citra penuh agar sidik jari *upsampling* tidak hilang.
- **Memperbaiki mekanisme fusi:** regularisasi/penyetelan SE-gating agar mampu menekan cabang lemah; pertimbangkan *pretraining*/pembekuan cabang frekuensi sebelum fusi; atau mekanisme atensi dua-domain yang lebih canggih (rujuk Qian et al., 2020; Alam et al., 2025).
- **Eksplorasi domain alternatif:** DCT/wavelet, atau gabungan spektral lain yang dilaporkan lebih stabil lintas-GAN.
- **Skala & temporal:** dataset lebih besar, variasi kompresi, dan pemodelan temporal antar-*frame* (saat ini frame-level).
- **Praktis:** untuk penerapan saat ini, baseline spasial (XceptionNet) tetap menjadi pilihan paling andal; generalisasi lintas dataset perlu riset lanjutan.

**Sumber angka:** Tabel 4.2 (in-dataset), 4.3 (cross), 4.4 (drop), 4.6 (RM). Tidak perlu gambar/tabel baru di BAB V.

---

## BAGIAN 2 — ABSTRAK (Indonesia) + ABSTRACT (Inggris) + Kata Kunci

**Format pedoman:** 100–200 kata, **satu paragraf**, *cetak miring*, Times New Roman 12 pt. Sediakan **Abstrak (Bahasa Indonesia)** dan **Abstract (English)** + **Kata kunci/Keywords** (3–5).

### Alur isi (satu paragraf, urutan ini)
1. **Latar/masalah (1 kalimat):** deteksi deepfake penting; detektor spasial murni lemah pada generalisasi lintas dataset; domain frekuensi diklaim membantu.
2. **Tujuan (1 kalimat):** studi komparatif kontribusi domain frekuensi melalui arsitektur hybrid XceptionNet–FFT (late fusion + SE gating) dibanding model domain tunggal.
3. **Metode (1–2 kalimat):** tiga model (spasial, frekuensi, hybrid) × dua dataset (FaceForensics++, Celeb-DF) × evaluasi in-dataset & cross-dataset × beberapa ukuran sampel × 3 *seed*; metrik akurasi, presisi, *recall*, F1, AUC (frame-level, split per-video).
4. **Hasil utama (2 kalimat, dengan angka kunci):** spasial terbaik (AUC in-dataset s.d. 0,97); cabang frekuensi nyaris acak (≈0,55–0,59); hybrid **tidak** mengungguli spasial; cross-dataset menurun untuk semua model (AUC ≈0,63–0,65, *recall* runtuh), dengan FFT hanya menekan *generalization drop* secara parsial.
5. **Kesimpulan (1 kalimat):** kontribusi domain frekuensi terbatas pada konfigurasi ini; temuan komparatif/negatif + arah perbaikan.

### Kata kunci (usulan, pilih 3–5)
deteksi deepfake; XceptionNet; domain frekuensi (FFT); arsitektur hybrid; generalisasi lintas dataset.
*(Keywords: deepfake detection; XceptionNet; frequency domain (FFT); hybrid architecture; cross-dataset generalization.)*

### Patokan & rambu
- Konsisten dengan Abstrak ID ↔ Abstract EN (terjemahan setara, bukan menambah klaim).
- **Jangan** sebut angka yang masih bermasalah (mis. ukuran sampel "1000" — pakai pernyataan kualitatif "beberapa ukuran sampel" atau rentang 100–750 yang benar).
- **Jangan** mengklaim keunggulan hybrid; gunakan bahasa investigatif.
- Hitung kata: jaga 100–200 kata per versi (ID & EN terpisah).

---

## Kesiapan & catatan
- **Bisa ditulis sekarang** — bahan settle, BAB IV lengkap. Isu BAB IV yang tertunda (penomoran gambar, value, sitasi) **tidak menghambat** BAB V/Abstrak karena keduanya merangkum temuan tingkat tinggi.
- Setelah plan disetujui, langkah berikut: tulis draft penuh BAB V lalu Abstrak ID + EN siap-tempel.
