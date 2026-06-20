# CHANGESET — Adopsi Run Pelatihan Terbaru (2026-06-20) sebagai Baseline

**Keputusan tim:** pakai hasil training **terbaru** (run `a5cb3ba`, 2026-06-20) sebagai sumber kebenaran, menggantikan run 2026-06-09.
**Konsekuensi:** seluruh Tabel 4.2–4.6, 4 gambar bar/scaling/drop, dan angka inline prosa BAB IV harus diselaraskan ke run baru.
**Dokumen terkait:** `ACTION_4_Commits_ROC_CM_vs_WORD_2026-06-20.md` (latar), `HANDOFF_Finalisasi_BAB_II-IV_2026-06-17.md`.

---

## 0. ⚠️ BLOCKER DATA — baca dulu sebelum mengedit tabel

Run baru yang **ter-commit di repo hanya seed 0** (file `outputs/roc_cm/*_metrics.json`, hasil inferensi untuk ROC/CM). **Tidak ada tabel 3-seed** untuk run baru (yang ada hanya `results_vast_20260609/` = run lama).

Akibatnya ada **dua cara** menjalankan keputusan ini:

- **Cara A — Ambil data 3-seed run baru (DISARANKAN).** Salin dari mesin GPU tempat run 2026-06-20 dijalankan:
  `results_vast_<tgl_baru>/tables/n{100,250,500,750}/Table{1,2,3}*_summary.csv`
  ke repo. Lalu semua tabel tetap **"rata-rata ± simpangan baku atas 3 seed"** (klaim robust dipertahankan), dan bar/scaling/drop chart bisa di-regen otomatis. **Jika data ini masih ada di box, ambil dulu — paling rapi.**
- **Cara B — Pakai seed-0 saja (fallback bila data 3-seed sudah hilang).** Semua tabel jadi **single-seed (seed 0)**: hapus `± std`, ubah caption jadi "seed 0", dan tambahkan keterbatasan "hasil satu seed" di BAB IV/V. Angka seed-0 sudah dihitung lengkap di §2 di bawah (siap pakai sekarang).

> **Rekomendasi:** kejar Cara A. Kalau dalam beberapa jam tidak dapat data 3-seed, jatuh ke Cara B dgn angka §2.

**Catatan kualitas berita baik:** run baru justru **lebih konsisten** secara naratif — di arah FFPP→CDF, freq sekarang **terendah** (0,614) dan spatial **tertinggi** (0,683), menghilangkan keanehan run lama (freq malah AUC tertinggi 0,655). Semua klaim kualitatif RM1/RM2/RM3 **tetap berlaku** (lihat §5).

---

## 1. PETA PERUBAHAN (ringkas)

| Aset | Lokasi | Aksi |
|---|---|---|
| Tabel 4.2 in-dataset | `documents/table/tabel_4_2_hasil_in_dataset.html` | **Ganti nilai** (§2.1) |
| Tabel 4.3 cross-dataset | `tabel_4_3_hasil_cross_dataset.html` | **Ganti nilai** (§2.2) |
| Tabel 4.4 generalization drop | `tabel_4_4_generalization_drop.html` | **Ganti nilai** (§2.3) |
| Tabel 4.5 AUC per tier | `tabel_4_5_auc_ukuran_sampel.html` | **Ganti nilai** (§2.4) |
| Tabel 4.6 ringkasan RM | `tabel_4_6_ringkasan_rumusan_masalah.html` | **Ganti angka di narasi** (§2.5) |
| Gambar 4.3 bar in-dataset | `media_v2/gambar_4_3_perbandingan_in_dataset.png` | **Regen** (Cara A) / rebuild seed-0 |
| Gambar 4.5 bar cross | `media_v2/gambar_4_5_perbandingan_cross_dataset.png` | **Regen** |
| Gambar 4.7 gen drop | `media_v2/gambar_4_7_generalization_drop.png` | **Regen** |
| Gambar 4.8 scaling AUC | `media_v2/gambar_4_8_scaling_auc.png` | **Regen** |
| Gambar 4.4 ROC in | `media_v2/gambar_4_4_roc_in_dataset.png` | **TAMBAH** (dari run baru, sudah ada PNG) |
| Gambar 4.6 ROC cross | `media_v2/gambar_4_6_roc_cross_dataset.png` | **TAMBAH** |
| Gambar 4.9 confusion matrix | `media_v2/gambar_4_9_confusion_matrix.png` | **TAMBAH** |
| Gambar 4.10 kurva pelatihan | `media_v2/gambar_4_10_kurva_pelatihan.png` | **TAMBAH — butuh regen di box** (lihat §4) |
| Prosa inline BAB IV | docx | **Isi/ganti angka** (§3) |

---

## 2. NILAI BARU PER TABEL (seed 0; format `lama → baru`)

> Jika Cara A (3-seed), angka tengah akan sedikit berbeda + ada `± std`. Pola perubahan tetap mirip (selisih lama↔baru seed-0 kecil).

### 2.1 Tabel 4.2 — In-Dataset (n=750)
| Dataset | Model | Akurasi | Presisi | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| FFPP | spatial | 0,700 → **0,689** | 0,662 → **0,652** | 0,766 → **0,750** | 0,710 → **0,698** | 0,780 → **0,767** |
| FFPP | hybrid | 0,610 → **0,608** | 0,588 → **0,590** | 0,618 → **0,597** | 0,603 → **0,594** | 0,650 → **0,634** |
| FFPP | freq | 0,531 → **0,532** | 0,512 → **0,508** | 0,560 → **0,716** | 0,529 → **0,595** | 0,546 → **0,569** |
| CDF | spatial | 0,915 → **0,913** | 0,906 → **0,923** | 0,912 → **0,887** | 0,909 → **0,905** | 0,969 → **0,970** |
| CDF | hybrid | 0,858 → **0,832** | 0,851 → **0,838** | 0,843 → **0,795** | 0,847 → **0,816** | 0,924 → **0,907** |
| CDF | freq | 0,563 → **0,570** | 0,529 → **0,539** | 0,495 → **0,540** | 0,511 → **0,540** | 0,586 → **0,578** |

*Perubahan menonjol:* FFPP-freq recall 0,560→**0,716** & F1 0,529→**0,595** (threshold seed-0 baru lebih agresif).

### 2.2 Tabel 4.3 — Cross-Dataset (n=750)
| Arah | Model | Akurasi | Presisi | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| FFPP→CDF | spatial | 0,608 → **0,626** | 0,571 → **0,586** | 0,618 → **0,679** | 0,594 → **0,629** | 0,648 → **0,683** |
| FFPP→CDF | hybrid | 0,611 → **0,632** | 0,584 → **0,626** | 0,570 → **0,525** | 0,576 → **0,571** | 0,648 → **0,680** |
| FFPP→CDF | freq | 0,550 → **0,538** | 0,621 → **0,549** | 0,069 → **0,056** | 0,124 → **0,101** | 0,655 → **0,614** |
| CDF→FFPP | spatial | 0,558 → **0,551** | 0,932 → **0,911** | 0,083 → **0,070** | 0,153 → **0,130** | 0,629 → **0,630** |
| CDF→FFPP | hybrid | 0,569 → **0,558** | 0,789 → **0,680** | 0,143 → **0,147** | 0,237 → **0,242** | 0,563 → **0,585** |
| CDF→FFPP | freq | 0,571 → **0,559** | 0,549 → **0,532** | 0,596 → **0,647** | 0,570 → **0,584** | 0,591 → **0,586** |

*Perbaikan naratif:* freq FFPP→CDF AUC 0,655→**0,614** (kini terendah; sebelumnya janggal jadi tertinggi).

### 2.3 Tabel 4.4 — Generalization Drop F1 (n=750)
| Model | Train | F1 In | F1 Cross | Δ |
|---|---|---|---|---|
| spatial | FFPP | 0,710 → **0,698** | 0,594 → **0,629** | +0,116 → **+0,069** |
| spatial | CDF | 0,909 → **0,905** | 0,153 → **0,130** | +0,756 → **+0,775** |
| hybrid | FFPP | 0,603 → **0,594** | 0,576 → **0,571** | +0,027 → **+0,023** |
| hybrid | CDF | 0,847 → **0,816** | 0,237 → **0,242** | +0,609 → **+0,573** |
| freq | FFPP | 0,529 → **0,595** | 0,124 → **0,101** | +0,406 → **+0,494** |
| freq | CDF | 0,511 → **0,540** | 0,570 → **0,584** | −0,058 → **−0,044** |

### 2.4 Tabel 4.5 — AUC In-Dataset per tier
| Dataset | Model | n=250 | n=500 | n=750 |
|---|---|---|---|---|
| FFPP | spatial | 0,746 → **0,730** | 0,693 → **0,690** | 0,780 → **0,767** |
| FFPP | hybrid | 0,542 → **0,602** | 0,582 → **0,619** | 0,650 → **0,634** |
| FFPP | freq | 0,480 → **0,422** | 0,570 → **0,503** | 0,546 → **0,569** |
| CDF | spatial | 0,942 → **0,915** | 0,967 → **0,942** | 0,969 → **0,970** |
| CDF | hybrid | 0,812 → **0,791** | 0,892 → **0,848** | 0,924 → **0,907** |
| CDF | freq | 0,569 → **0,537** | 0,615 → **0,541** | 0,586 → **0,578** |

*Catatan:* FFPP-freq kini **monoton naik** 0,422→0,503→0,569 (run lama non-monoton 0,480→0,570→0,546) → lebih enak dijelaskan. CDF-freq sedikit turun di n500.

### 2.5 Tabel 4.6 — Ringkasan Rumusan Masalah (ganti angka di narasi)
| Sel | Lama | Baru |
|---|---|---|
| RM1 temuan | "AUC turun ke **0,629–0,648** dan recall runtuh hingga **0,083**" | "AUC turun ke **0,630–0,683** dan recall runtuh hingga **0,070**" |
| RM2 temuan | "Δ hybrid **+0,027** vs spatial **+0,116**" | "Δ hybrid **+0,023** vs spatial **+0,069**" |
| RM3 temuan | "AUC s.d. **0,969**); freq nyaris acak (**0,55–0,59**)" | "AUC s.d. **0,970**); freq nyaris acak (**0,57–0,61**)" |

> RM1 "AUC turun ke 0,630–0,683": ini rentang AUC cross spatial (CDF→FFPP 0,630; FFPP→CDF 0,683). Bila ingin tegas "spatial", tulis begitu; bila rentang semua model cross gunakan **0,585–0,683**.

---

## 3. ANGKA INLINE PROSA BAB IV (isi/ganti — pakai nilai run baru)

Banyak kurung di prosa **masih kosong** (bukan field Word). Isi dgn nilai run baru:

| Lokasi | Teks | Isi (run baru) |
|---|---|---|
| §4.1.3 & caption | "tier ( )", "( , rata-rata…)" | **n = 750** |
| §4.1.4 | "AUC berada pada kisaran ( )." | **0,58–0,68** |
| §4.1.4 | spatial "presisi sangat tinggi ( ) namun recall runtuh menjadi ( )" | presisi **0,911**, recall **0,070** |
| §4.1.4 | hybrid "(presisi , recall )" | **0,680**, **0,147** |
| §4.1.4 | freq "keruntuhan recall ( )" (FFPP→CDF) | **0,056** |
| §4.1.4 | "spasial dan hybrid mempertahankan recall yang lebih wajar ( dan )" | **0,679** dan **0,525** |
| §4.1.6 | "tiga tier …, yaitu , , dan ." | **250, 500, 750** |
| Caption 4.3/4.5(bar)/4.7 | "( )" | **(n = 750)** |

---

## 4. GAMBAR — APA YANG DITAMBAH & DIREGEN (`documents/media_v2/`)

### 4A. TAMBAH (file baru) — sumber sudah ada di `deepfake_hybrid/outputs/roc_cm/` (run baru)
| Gambar | Komposisi dari | Simpan sebagai |
|---|---|---|
| **4.4** ROC in-dataset | `FFPP_in_n750_roc.png` + `CDF_in_n750_roc.png` (2 panel) | `gambar_4_4_roc_in_dataset.png` |
| **4.6** ROC cross-dataset | `FFPP2CDF_n750_roc.png` + `CDF2FFPP_n750_roc.png` | `gambar_4_6_roc_cross_dataset.png` |
| **4.9** Confusion matrix | contoh: `CDF_in_n750_cm_spatial.png` (in, baik) + `CDF2FFPP_n750_cm_spatial.png` (cross, recall runtuh TP=308/FN=4108) | `gambar_4_9_confusion_matrix.png` |

ROC PNG = overlay 3 model (legenda berisi AUC seed-0 baru, otomatis cocok dgn tabel baru). ✅ inilah inti keuntungan adopsi run baru.

### 4B. REGEN (timpa file lama) — **butuh data 3-seed run baru (Cara A)**
`make_bab4_figures.py` membaca `results_vast_20260609/tables/`. Untuk run baru:
1. Taruh tabel 3-seed run baru di `results_vast_<tgl_baru>/tables/`.
2. Ubah konstanta `TABLES` di `scripts/make_bab4_figures.py` ke folder baru (atau ganti isi `results_vast_20260609`).
3. Jalankan → regen `gambar_4_3`, `gambar_4_5`, `gambar_4_7`, `gambar_4_8`.

> Tanpa data 3-seed (Cara B): keempat chart ini harus dibangun ulang dari seed-0 (perlu modifikasi skrip kecil agar baca `outputs/roc_cm/*_metrics.json`). Bisa saya buatkan bila diminta.

### 4C. Gambar 4.10 (kurva pelatihan) — **BLOCKER kecil**
- Run baru **tidak meng-commit** histori per-epoch (`history.json`) maupun PNG kurva pelatihan.
- Pilihan: (a) **regen di box** dari histori run baru (paling benar, konsisten), atau (b) stopgap pakai kurva run lama `results_vast_20260609/plots/training_curves_{freq,spatial}_FFPP_n750.png` — **tapi ini run lama → tak konsisten** dgn keputusan adopsi run baru. **Disarankan (a).**
- Narasi §4.2 (freq stagnan, spatial naik jelas) **tetap valid** di run baru (in-dataset freq AUC 0,569 ≪ spatial 0,767).

---

## 5. CEK NARASI — semua klaim utama TETAP BERLAKU di run baru ✅

| Klaim | Run baru | Status |
|---|---|---|
| spatial > hybrid > freq (in-dataset) | FFPP 0,767>0,634>0,569; CDF 0,970>0,907>0,578 | ✅ |
| hybrid tidak mengungguli spatial (RM3) | hybrid < spatial di semua in-dataset | ✅ |
| freq nyaris acak | in 0,569/0,578 | ✅ (revisi pita ke 0,57–0,61) |
| spatial runtuh lintas-dataset, recall jatuh (RM1) | CDF→FFPP recall 0,070, AUC turun | ✅ |
| FFT perkecil drop FFPP→CDF (RM2) | hybrid Δ+0,023 < spatial Δ+0,069 | ✅ (gap mengecil tapi arah sama) |
| freq FFPP→CDF recall collapse | 0,056 | ✅ (lebih parah, perkuat klaim) |
| (BARU) freq cross tidak lagi AUC tertinggi | FFPP→CDF freq 0,614 < spatial 0,683 | ✅ lebih koheren |

**Tidak ada klaim yang patah.** Adopsi run baru aman secara naratif.

---

## 6. URUTAN KERJA

1. **[BLOCKER]** Coba ambil `results_vast_<tgl_baru>/tables/` 3-seed dari box (Cara A). Kabari hasilnya.
2. Update 5 tabel HTML (`documents/table/tabel_4_2..4_6`) → nilai §2. (Saya bisa kerjakan begitu A/B diputuskan.)
3. Tambah 3 komposit gambar ROC/CM ke `media_v2` (4.4/4.6/4.9) dari `outputs/roc_cm/`. (Bisa saya buatkan.)
4. Regen 4 chart bar/scaling/drop (4.3/4.5/4.7/4.8) — Cara A via skrip, atau Cara B dari seed-0.
5. Gambar 4.10: regen di box (disarankan) atau stopgap.
6. Isi angka inline prosa BAB IV (§3) + caption (n=750).
7. Renumber gambar BAB IV ke skema 4.1–4.10 (lihat ACTION doc §5.2) + Update DAFTAR GAMBAR.
8. (Opsional) catat di BAB V keterbatasan bila Cara B (single seed).
9. `Ctrl+A → F9` Update Fields.

---

## Lampiran — sumber angka
Semua nilai run baru dihitung dari `deepfake_hybrid/outputs/roc_cm/{FFPP_in,CDF_in,FFPP2CDF,CDF2FFPP}_n{250,500,750}_metrics.json` (seed 0). Nilai lama dari `results_vast_20260609/tables/`. n=100 sengaja tidak masuk tabel mana pun (tidak stabil: FFPP in-dataset AUC seed-0 di bawah 0,5).
