# 📁 Folder Sidang — Pusat Materi & Panduan

> Semua yang berhubungan dengan **sidang skripsi** ada di folder ini: referensi, bukti eksperimen, Q&A, study guide per cabang, naskah presentasi, script demo, dan daftar revisi pra-sidang. Mulai dari dokumen ini.
>
> **Judul skripsi:** *Studi Komparatif Kinerja Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet-FFT terhadap Model Domain Tunggal.*
> **Penulis:** Naomi Prisella · Giovanny Halimko · Samuel Onasis — Universitas Mikroskil.

---

## 🎯 Mulai dari mana?

| Kebutuhan | Buka |
|---|---|
| Lihat **semua angka & hasil sekilas** (1 halaman, siap cetak) | **[referensi_sidang.pdf](referensi_sidang.pdf)** / [.html](referensi_sidang.html) |
| Ditanya **"pernah dicoba / berapa hasilnya?"** | **[Rekap_Eksperimen_Deepfake_2026-07-07.xlsx](Rekap_Eksperimen_Deepfake_2026-07-07.xlsx)** |
| **Latihan jawab pertanyaan penguji** (siap-ucap) | **[playbook_qna_sidang.pdf](playbook_qna_sidang.pdf)** |
| Belajar **memahami alur & alasan** (untuk menjawab dengan kata sendiri) | [PANDUAN_SIDANG_QnA_Teknis](PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md) |
| Latihan **presentasi** (naskah per slide) | [Naskah slide 10-15](sidang_speaker_script_slide_10-15.md) · [16-23](sidang_speaker_script_slide_16-23.md) |
| Siapkan **materi bagian saya** (per cabang) | Study guide di §C |
| **Revisi apa yang masih perlu** sebelum maju | §E |

---

## 🗂️ Peta Dokumen

### A. Referensi & Bukti (yang paling sering dibuka saat sidang)
| Berkas | Isi |
|---|---|
| [referensi_sidang.pdf](referensi_sidang.pdf) · [.html](referensi_sidang.html) | **Ringkasan 1 halaman**: verdict, hasil final n=750, parameter, jurnal Train 1→9, strategi fusi, Q&A. Warna per domain (spasial biru / frekuensi merah / hybrid ungu). |
| [playbook_qna_sidang.pdf](playbook_qna_sidang.pdf) · [.html](playbook_qna_sidang.html) | **Defense Playbook** — rangkuman 41 item fact-check jadi *"kalau ditanya X → jawab Y"*: 7 pertanyaan kunci + jawaban siap-ucap, fakta terverifikasi, jebakan yang sudah ditutup. |
| [Rekap_Eksperimen_Deepfake_2026-07-07.xlsx](Rekap_Eksperimen_Deepfake_2026-07-07.xlsx) | **Excel 6 sheet** — jurnal train + kolom *"kenapa train ini tidak dipakai"*, hasil detail per train, hasil final, early fusion, freqbench, parameter. |
| [RINGKASAN_PARAMETER_NILAI_PROYEK.md](RINGKASAN_PARAMETER_NILAI_PROYEK.md) | Semua parameter & nilai config (dengan rujukan `file:line`). |
| [INVENTARIS_SEMUA_EKSPERIMEN_2026-07-07.md](INVENTARIS_SEMUA_EKSPERIMEN_2026-07-07.md) | Jurnal kronologis Train 1→9 + section fusi (late/early/freqbench) + bukti path. |

### B. Q&A & Fact-Check
| Berkas | Isi |
|---|---|
| [PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md](PANDUAN_SIDANG_QnA_Teknis_2026-06-17.md) | Pemahaman alur + tanya-jawab teknis (memahami, bukan menghafal). |
| [SIDANG_FactCheck_QA_2026-06-30.md](SIDANG_FactCheck_QA_2026-06-30.md) | **Living document** — 41+ item fakta thesis diverifikasi vs kode & data, dengan jawaban siap-ucap. Lempar fakta baru → di-append. |
| [SIDANG_QA_freq_negative.md](SIDANG_QA_freq_negative.md) | Q&A khusus **temuan negatif frekuensi** — cara membela hasil freq near-random. |

### C. Study Guide per Cabang (pembagian peran presenter)
> Tiap presenter menguasai **satu cabang**. Baca [study_notes_detailed](sidang_study_notes_detailed_2026-06-25.md) dulu (gambaran penuh), lalu guide cabang masing-masing.

| Berkas | Cabang / Topik |
|---|---|
| [sidang_study_notes_detailed_2026-06-25.md](sidang_study_notes_detailed_2026-06-25.md) | **Deep-dive semua langkah** (dokumen belajar utama). |
| [sidang_study_guide_SPATIAL_branch.md](sidang_study_guide_SPATIAL_branch.md) | **Spasial** — XceptionNet, transfer learning, RM1 (penurunan lintas dataset). |
| [sidang_study_guide_FREQUENCY_branch.md](sidang_study_guide_FREQUENCY_branch.md) · [.designed.html](sidang_study_guide_FREQUENCY_branch.designed.html) | **Frekuensi** — FFT, FreqCNN, temuan negatif (freq near-random). |
| [sidang_study_guide_HYBRID_branch.md](sidang_study_guide_HYBRID_branch.md) · [.designed.html](sidang_study_guide_HYBRID_branch.designed.html) | **Hybrid** — late fusion, SE gating, klaim komparatif utama. |
| [sidang_study_guide_DEMO_debug.md](sidang_study_guide_DEMO_debug.md) | **Demo** — cara jalankan, alur kode, cara "debug di tempat". |

### D. Presentasi & Naskah
| Berkas | Isi |
|---|---|
| [PRESENTASI_Sidang_2026-06-17.md](PRESENTASI_Sidang_2026-06-17.md) | Konten slide demi slide (~24 slide, ~20 menit). |
| [sidang_speaker_script_slide_10-15.md](sidang_speaker_script_slide_10-15.md) | Naskah kata-per-kata Metodologi (±6 menit). |
| [sidang_speaker_script_slide_16-23.md](sidang_speaker_script_slide_16-23.md) | Naskah kata-per-kata Hasil & Penutup (±7-8 menit). |
| [demo_video_script_ID.md](demo_video_script_ID.md) · [demo_video_script.md](demo_video_script.md) | Naskah narasi video demo Gradio (~10 menit). |

### E. Feedback Pembanding & Panduan Review (apa yang penguji soroti)
| Berkas | Isi |
|---|---|
| [reviewer_feedback/](reviewer_feedback/) | **Hasil Tinjauan Pra Ujian Akhir — Pembanding 1 & 2** (komentar penguji atas draf). Baca ini untuk tahu titik yang akan ditanya. |
| [panduan_sidang_review.pdf](panduan_sidang_review.pdf) | Panduan review sidang. |

> **Catatan:** dokumen **revisi naskah** (`REVISI_BAB_*_FIX_*.md`) **tidak** di sini — itu instruksi edit dokumen Word (thesis-writing), bukan materi sidang. Ada di `../documents/`.

---

## 🧠 Fakta inti (hafalkan angkanya)

| | Nilai |
|---|---|
| **Spasial (XceptionNet)** AUC in-dataset | hingga **0,97** (CDF) / 0,78 (FFPP) — **paling unggul** |
| **Frekuensi (FreqCNN)** AUC | **0,56–0,61** → **≈ tebakan acak (0,5)** |
| **Hybrid** | **tidak mengungguli** baseline spasial |
| **Hipotesis** | **H₀ tidak ditolak** — manfaat frekuensi parsial & bergantung arah |
| Cross-dataset (semua model) | AUC **0,55–0,68** + **keruntuhan recall** (hingga 0,07) |
| Skala eksperimen | **72 pelatihan · 144 evaluasi** · 3 model × 2 dataset × 4 ukuran × 3 seed |
| Tier headline | **n = 750** (3 seed, mean ± std) |

---

## ❓ Kalau ditanya… → buka

| Pertanyaan penguji | Jawaban ada di |
|---|---|
| *"Sudah pernah test? Hasilnya?"* | Excel Sheet 2 (Hasil Detail per Train) |
| *"Kenapa pakai hasil ini, bukan train sebelumnya?"* | Excel Sheet 1, kolom **Alasan tidak dipakai** |
| *"Pernah coba early fusion?"* | Excel Sheet 4 · referensi §Fusi → **Ya, val-AUC 0,68, tidak lebih baik** |
| *"Mungkin FreqCNN kurang kuat?"* | Excel Sheet 5 (freqbench) → **sudah coba ResNet18, tetap near-random** |
| *"Kenapa AUC metrik utama?"* | PANDUAN + referensi → independen threshold + tahan imbalance |
| *"Kok hybrid tidak lebih baik?"* | HYBRID study guide → freq lemah membatasi fusi; temuan negatif yang sah |

---

## ✅ Checklist sebelum sidang
- [ ] Baca **feedback pembanding** (§E) — pastikan tiap titik yang mereka soroti sudah terjawab di naskah/jawaban.
- [ ] Terapkan sisa **revisi naskah** (`../documents/REVISI_BAB_*`) + isi tahun lahir, Ctrl+A→F9.
- [ ] Latihan naskah §D sampai lancar (target ~20 menit).
- [ ] Buka `referensi_sidang.pdf` & Excel di laptop — pastikan bisa dibuka **offline**.
- [ ] Tiap presenter kuasai study guide cabangnya (§C) + bisa demo (DEMO guide).
- [ ] Hafalkan **fakta inti** di atas.
- [ ] Siapkan jawaban temuan negatif: *"hybrid tidak mengungguli spasial"* = **kontribusi ilmiah yang sah** (studi komparatif, bukan kegagalan).

*Folder ini dirapikan 2026-07-07. Draf bab & dokumen revisi historis tetap di `documents/`.*
