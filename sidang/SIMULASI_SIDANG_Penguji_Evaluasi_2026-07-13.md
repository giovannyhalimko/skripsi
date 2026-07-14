# Simulasi Sidang Skripsi — Rekam Evaluasi Penguji

**Tanggal:** 2026-07-13
**Mahasiswa yang diuji:** Samuel Onasis (221110680)
**Kontribusi:** Penyusunan dokumen BAB I–V, evaluasi hasil pelatihan model, studi komparatif
**Judul:** Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal
**Penguji (simulasi):** Dosen Penguji Senior — Teknik Informatika

> Berkas ini merekam setiap pertanyaan, jawaban ringkas mahasiswa, dan evaluasi penguji
> (Ketepatan / Kedalaman / Kekurangan / Skor 1–10) untuk kepentingan refleksi mahasiswa.

---

## Perkenalan

Mahasiswa memperkenalkan judul, kontribusi, latar belakang singkat (video generatif sebagai
ancaman forensik digital), dan ringkasan metode (XceptionNet = spasial, FFT+FreqCNN = frekuensi,
hibrida = konkatenasi dua cabang + SE gating).

**Catatan penguji:** Istilah "SE gating = noise filtering" ditandai untuk digali lebih dalam.
Karakterisasi ini kurang tepat secara teknis (SE = channel recalibration/attention, bukan noise filtering).

---

## Pertanyaan #1 — Research Gap / Alasan Penelitian Perlu Ada

**Pertanyaan:** Mengapa penelitian ini perlu ada? XceptionNet sudah kuat dan banyak dipakai.
Apa research gap-nya?

**Jawaban ringkas mahasiswa:** GAN makin berkembang, artefak spasial makin sulit dideteksi.
Penelitian Durall & Alam menyarankan menambah domain frekuensi, tetapi via joint learning.
Teknik yang dipakai tim ini adalah *late fusion* antara domain frekuensi murni (FreqCNN) dengan
XceptionNet, yang belum ditemukan di literatur. Karena itu tertarik mengomparasi apakah penambahan
domain frekuensi murni ke XceptionNet meningkatkan kinerja.

**Evaluasi**
- **Ketepatan:** Cukup baik. Berhasil menyebut motivasi (degradasi artefak spasial seiring
  kemajuan GAN) dan membedakan late fusion vs joint/early fusion. Menyebut referensi konkret.
- **Kedalaman:** Sedang. Ada pembedaan metodologis yang jelas, tetapi klaim kebaruan ("belum ada
  late fusion freq murni + Xception") terlalu kuat dan rapuh — Alam (SpecXNet) justru arsitektur
  *dual-domain two-branch* yang sangat dekat; Luo, Qian (F3-Net) juga fusi spasial-frekuensi.
- **Kekurangan:**
  1. Karakterisasi Durall kurang tepat — Durall bukan mengusulkan joint learning dengan Xception,
     melainkan menunjukkan GAN gagal mereproduksi distribusi spektral (dasar teori, bukan arsitektur fusi).
  2. Kebaruan diletakkan pada *kombinasi arsitektur*, bukan pada *mengapa late fusion seharusnya
     lebih baik*. Novelty ≠ kontribusi ilmiah.
  3. Belum menjelaskan mekanisme: mengapa domain frekuensi menangkap yang tidak tertangkap spasial.
- **Skor:** 7/10

### Pertanyaan #1a (follow-up) — Beda dari SpecXNet

**Pertanyaan:** SpecXNet sudah dual-domain two-branch fusion. Apa bedanya penelitian ini, dan
kenapa beda itu = kontribusi, bukan pengulangan?

**Jawaban ringkas mahasiswa:** Bedanya pakai SE gating untuk filter noise, dan domain frekuensi
dibangun sendiri memanfaatkan log-magnitudo yang memuat artefak frekuensi / GAN fingerprints yang
diharapkan meningkatkan akurasi.

**Evaluasi**
- **Ketepatan:** Kurang. Dua komponen yang disebut (SE gating & log-magnitudo FFT) keduanya
  komponen *off-the-shelf/standar* — SE = Hu et al (Squeeze-Excitation), log-magnitudo FFT adalah
  representasi baku di literatur frekuensi (Durall, Zhang). Keduanya tidak memisahkan penelitian ini
  dari SpecXNet yang notabene juga jaringan dual-domain spektral.
- **Kedalaman:** Dangkal. Menyebut ulang komponen, bukan mengartikulasikan kontribusi.
- **Kekurangan:**
  1. Kontribusi paling defensible tidak disebut: ini **studi komparatif** (spasial vs frekuensi vs
     hibrida, termasuk lintas-dataset FFPP↔CDF) dengan cabang frekuensi yang **terpisah penuh**
     sehingga kontribusi tiap domain bisa diisolasi (ablation bersih) — bukan klaim arsitektur baru.
  2. Mengulang mischaracterization "SE gating = noise filtering" (kedua kalinya).
  3. Klaim "log-magnitudo diharapkan meningkatkan akurasi" bertentangan dengan temuan sendiri:
     cabang frekuensi justru *underperform* (lihat SIDANG_QA_freq_negative.md).
- **Skor:** 5/10

---
