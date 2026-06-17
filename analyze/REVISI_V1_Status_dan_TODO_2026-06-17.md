# REVISI V1 — Status & Daftar Revisi (cek ulang vs WORD terbaru)

**Tanggal:** 2026-06-17 · **docx diperiksa:** `REVISI V1 - …docx` (mod 2026-06-15 16:13)
**Menggantikan/menyambung:** `analyze/REVISI_V1_Full_Analysis_and_RUMUS_Relokasi_2026-06-11_1600.md` (rujukan item *value*).
**Pemicu:** rilis demo Gradio (commit `63a7896`, `a02ca82`) + `CODE_WALKTHROUGH.md` → menilai tambahan BAB II/III.

---

## A. Sudah SELESAI di docx (terverifikasi 2026-06-17)
- ✅ **Relokasi RUMUS BAB III → BAB II** diterapkan. BAB II 2.1–2.43 (rapi), BAB III hanya perhitungan.
- ✅ **Penomoran persamaan BAB III** kini **3.1–3.17, tanpa duplikat** (dulu eq 3.4 dobel — sudah diperbaiki).
- ✅ **Sitasi SE gating** kini **Hu et al. (HuJ18)** — benar (dulu salah He/HeK15).
- ✅ Cross-ref persamaan BAB III→BAB II benar sasaran (grayscale 2.16, DFT 2.17, magnitude 2.18, high-pass 2.19, log 2.20, z-score 2.22, proyeksi 2.15).

---

## B. PENILAIAN: apakah demo/deployment perlu masuk BAB II / BAB III?

### BAB II (Kajian Literatur) → **tidak perlu**
Deployment / Gradio / Hugging Face Spaces **bukan topik kajian literatur** (BAB II = teori: deepfake, GAN, FFT, CNN, XceptionNet, SE, dataset, metrik). Tidak ada teori baru dari demo yang wajib ditambah.
- *Opsional (boleh diabaikan):* 1–2 kalimat di subbab **Analisis Video** tentang **agregasi prediksi frame → keputusan level-video** (rata-rata probabilitas). Tidak wajib.

### BAB III (Tahapan Pelaksanaan) → **perlu 2 tambahan kecil**
Substansi deployment (tangkapan layar, UI 3 model) → **BAB IV 4.1.2**. Namun ada 2 titik metodologis yang saat ini **kosong** di BAB III (scan: Gradio 0×, deploy 0×, video-level 0×, agregasi 0×):

**B1. Tabel 3.16 (Kebutuhan Perangkat Lunak) — tambah baris.**
`facenet-pytorch` sudah ada; tambahkan:

| Pustaka / Alat | Peran dalam penelitian | Justifikasi |
|---|---|---|
| Gradio | Antarmuka purwarupa interaktif untuk perbandingan 3 model (deploy ke Hugging Face Spaces) | SDK UI ringan, native di HF Spaces |
| opencv-python-headless | Pembacaan video pada lingkungan deployment CPU tanpa GUI | Varian OpenCV untuk server/Spaces |

**B2. Subbab baru pendek "Skema Inferensi dan Purwarupa Sistem"** (letakkan di akhir *Analisis Sistem*, sebelum/sesudah *Keluaran Sistem*). Draft siap-tempel:

> **Skema Inferensi dan Purwarupa Sistem**
>
> Selain evaluasi eksperimental pada level frame, model terlatih diterapkan pada skenario inferensi end-to-end terhadap satu video utuh. Tahapannya identik dengan pipeline pelatihan: video disampel pada 5 FPS (hingga 16 frame), setiap frame dideteksi dan dipotong wajahnya menggunakan MTCNN (margin 0,3), lalu dipreproses sama persis (RGB → 224×224 → normalisasi ImageNet; FFT → log-magnitude → normalisasi statistik dataset). Probabilitas-fake per-frame kemudian **diagregasi menjadi satu keputusan level-video** dengan merata-ratakan probabilitas seluruh frame, dan video diklasifikasikan sebagai *fake* bila rata-rata tersebut mencapai ambang keputusan yang disetel pada set validasi.
>
> Perlu ditegaskan bahwa **metrik evaluasi penelitian dihitung pada level frame** (untuk mengisolasi kualitas detektor), sedangkan **agregasi level-video di atas hanya digunakan pada tahap penerapan (purwarupa)** sebagai bentuk keluaran yang dapat dipakai pengguna; keduanya tidak saling bertentangan.
>
> Sebagai bukti kelaikan penerapan, ketiga model (spatial, hybrid, frequency) dikemas dalam sebuah purwarupa interaktif berbasis Gradio yang di-deploy ke Hugging Face Spaces, menampilkan verdict ketiga model secara berdampingan untuk satu video unggahan. Rincian antarmuka dan tangkapan layar purwarupa disajikan pada BAB IV.

> Catatan: subbab ini menjembatani BAB III (metode) dan BAB IV (4.1.2 purwarupa). Jika dosen menghendaki deployment murni di BAB IV, B2 boleh diringkas jadi 1 paragraf "penerapan" dan sisanya dipindah ke 4.1.2.

---

## C. PENDING — item value (JANGAN diutak-atik sekarang; rujuk PLAN/analisis)
Per instruksi, fokus value ditunda. Daftar acuan (detail di `REVISI_V1_Full_Analysis_…_2026-06-11_1600.md` + `documents/BAB_IV_STRUCTURE_PLAN_2026-06-15.md`):
- ⏳ **Tabel 3.3 / Tabel variasi ukuran sampel:** FFPP masih `100, 300, 600, 1000` (hasil final pakai `100, 250, 500, 750`). Masih ada di docx.
- ⏳ **Tabel 1.1 / 3.1:** klaim FFPP n=1000 / ~50.000 frame (tier maks dijalankan = 750).
- ⏳ **Label smoothing:** Tabel 3.10 menulis **0,0 (nonaktif)**, sedangkan contoh perhitungan Fungsi Loss memakai **α=0,05** → tidak konsisten. (masuk bucket value)
- ⏳ **Framing hasil negatif** (BAB I Latar Belakang/penutup) → selaraskan dengan judul komparatif (lihat PLAN §1–2).

---

## D. PENDING — sitasi & minor
- ⏳ **Gaya sitasi:** seluruh dokumen masih render **IEEE [N]** (semuanya CITATION field). Target (Nama, Tahun) → **ubah citation style di reference manager → Update All Fields** (satu langkah, bukan edit manual).
- ⏳ **Augmentasi Data (BAB II):** paragraf pembuka tampak hanya memuat sitasi **Afchar**; cek apakah **Rössler** perlu ditambah (draft awal: Afchar + Rössler). *(perlu verifikasi)*
- ⏳ **(opsional)** BAB II memuat rumus FFT **dobel** (DFT 2.1 & 2.17, magnitude 2.3 & 2.18, log 2.4 & 2.20) — konsolidasi suatu saat.
- ⏳ **(opsional)** Typo BAB I: "Sebagian besar", "Alam et al.", URL Celeb-DF terpotong.

---

## Ringkasan tindakan berikutnya
| Prioritas | Item | Lokasi |
|---|---|---|
| Baru (bisa segera) | Tambah Gradio + opencv-headless ke Tabel 3.16 | BAB III B1 |
| Baru (bisa segera) | Subbab "Skema Inferensi dan Purwarupa Sistem" | BAB III B2 |
| — | BAB II: tidak ada tambahan deployment | — |
| Ditunda (value) | Tabel 3.3, 1.1/3.1, label smoothing, framing | rujuk PLAN |
| Ditunda (sitasi) | Ganti style → (Nama, Tahun); verifikasi Rössler | reference manager |
