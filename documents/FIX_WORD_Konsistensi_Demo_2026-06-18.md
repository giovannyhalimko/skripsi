# FIX WORD — Konsistensi dengan Dokumentasi Teknis Demo

> Hasil verifikasi docx (judul baru, mod 2026-06-18) terhadap `deepfake_hybrid/demo/DOCUMENTATION.md` (commit `85b43ff`). **Kesimpulan: WORD sudah sesuai** dengan implementasi demo (5 FPS, 16 frame, MTCNN margin 0,3, rata-rata probabilitas, ambang dari set validasi, Gradio + HF Spaces, stack pustaka cocok). Tersisa perbaikan kecil di bawah. Gaya tanpa tanda pisah panjang dan titik-koma.

---

## 1. Rujukan nomor tabel basi di BAB III (WAJIB)
Caption tabel dan rujukan di BAB IV sudah benar (**Tabel 3.15** = Perangkat Keras, **Tabel 3.16** = Perangkat Lunak). Yang salah hanya angka yang diketik manual di paragraf pembuka kedua subbab.

**a. Kebutuhan Perangkat Keras** (paragraf pembuka)
- SEBELUM: "…Spesifikasi perangkat keras dirangkum pada **Tabel 3.17**."
- SESUDAH: "…Spesifikasi perangkat keras dirangkum pada **Tabel 3.15**."

**b. Kebutuhan Perangkat Lunak** (paragraf pembuka)
- SEBELUM: "Implementasi menggunakan bahasa Python 3.9 … yang dirangkum pada **Tabel 3.18**."
- SESUDAH: "Implementasi menggunakan bahasa Python 3.9 … yang dirangkum pada **Tabel 3.16**."

> Catatan: jika angka itu ternyata berupa *cross-reference field* (bukan teks ketik), Update Fields tidak memperbaikinya karena menunjuk target salah. Lebih aman: hapus angka lama, sisipkan ulang **Insert → Cross-reference → ke caption tabel yang benar**, lalu Update Fields.

## 2. Versi Python demo (OPSIONAL, klarifikasi)
WORD menyebut "Python 3.9" untuk implementasi penelitian, sedangkan purwarupa Gradio di Hugging Face Spaces sebenarnya berjalan pada **Python 3.10** (Gradio 5.x memerlukan 3.10+). Bukan kontradiksi (training 3.9 vs deploy demo 3.10), tapi bisa diperjelas. Tambahkan satu klausa pada paragraf *Skema Inferensi dan Purwarupa Sistem* (kalimat purwarupa Gradio):

- SESUDAH: "…dikemas dalam sebuah purwarupa interaktif berbasis Gradio yang di-*deploy* ke Hugging Face Spaces dan dijalankan pada Python 3.10 sesuai kebutuhan Gradio versi 5, menampilkan verdict ketiga model secara berdampingan untuk satu video unggahan."

## 3. Titik-koma pada paragraf Skema Inferensi (OPSIONAL, gaya)
Paragraf kedua *Skema Inferensi dan Purwarupa Sistem* memuat "…dapat dipakai pengguna**;** keduanya tidak saling bertentangan." Sesuai preferensi gaya, ganti titik-koma menjadi titik:
- SESUDAH: "…sebagai bentuk keluaran yang dapat dipakai pengguna. Keduanya tidak saling bertentangan."

---

## Catatan terpisah (BUKAN perbaikan WORD)
`demo/DOCUMENTATION.md` §4 dan §5 menulis threshold *"Tuned on the FFPP test set"*, padahal kode (`run_all.py` `compute_val_threshold`, baca `val.csv`) menyetelnya pada **validation split**. Di sini **WORD sudah benar**. Yang perlu diperbaiki adalah file DOCUMENTATION.md (ganti "test set" → "validation split"), bukan WORD.

## Verifikasi cocok (tidak perlu diubah)
5 FPS · maks 16 frame · MTCNN margin 0,3 · RGB→224²→ImageNet · FFT→log-magnitude→norm dataset · agregasi rata-rata per-frame · ambang dari set validasi · 3 model berdampingan · Gradio + HF Spaces · Tabel 3.16 memuat PyTorch, torchvision, timm, facenet-pytorch, opencv-python-headless, Gradio, NumPy, Pillow · panel "what the models see".
</content>
