# CHANGESET — Adopsi Run Pelatihan Terbaru (2026-06-20) sebagai Baseline

**Keputusan tim:** pakai hasil training **terbaru** (run 2026-06-20) sebagai sumber kebenaran, menggantikan run 2026-06-09.
**Status data (update setelah pull `26f5dae`):** ✅ **SEMUA aset run baru sudah ada di repo** — tabel **3-seed** (`outputs/tables/`), ROC/CM (`outputs/roc_cm/`), plot bar/scaling/drop + kurva pelatihan (`outputs/plots/`). Tidak perlu lagi tarik data dari box.
**Dokumen terkait:** `ACTION_4_Commits_ROC_CM_vs_WORD_2026-06-20.md`, `HANDOFF_Finalisasi_BAB_II-IV_2026-06-17.md`.

---

## 0. STATUS DATA — LENGKAP (blocker lama sudah teratasi)

Commit `26f5dae` ("Add GPU-trained result tables and plots; unignore tables/ and plots/") menambah seluruh hasil run baru:

| Aset run baru | Lokasi | Catatan |
|---|---|---|
| **Tabel 3-seed** (Table1/2/3 + *_summary) | `deepfake_hybrid/outputs/tables/n{100,250,500,750}/` | seed 0,1,2 → ada `auc_mean` **dan** `auc_std` |
| ROC + Confusion Matrix | `deepfake_hybrid/outputs/roc_cm/` | seed 0 (dari `a5cb3ba`) |
| Bar / scaling / drop / kurva pelatihan | `deepfake_hybrid/outputs/plots/` | label **Inggris** (output `plot_results.py`) |

**Verifikasi konsistensi:** seed-0 di tabel = `0,7671…` (FFPP spatial in n750) **cocok persis** dgn `outputs/roc_cm/FFPP_in_n750_metrics.json`. → tabel & gambar dari **run yang sama**. 🎯
**Kabar baik:** karena tabel run baru = **3-seed mean**, perubahan angka vs docx **kecil** (mayoritas AUC bergeser ≤0,03). Klaim "rata-rata ± simpangan baku atas 3 seed" **tetap dipertahankan** — tidak ada penurunan rigor.

> ⚠️ Catatan file untracked setelah pull: muncul `outputs/plots/*_n50/n200/n400` dan `outputs/tables/n50,n200,n400`. Itu **sisa eksperimen lokal lama** (ukuran sampel non-tesis) yang dulu disembunyikan `.gitignore`, kini terlihat karena folder di-untrack-ignore. **Aman dihapus** (bukan hasil kanonik). Bukan bagian commit baru.

---

## 1. PETA PERUBAHAN

| Aset | Lokasi | Aksi |
|---|---|---|
| Tabel 4.2 in-dataset | `documents/table/tabel_4_2_hasil_in_dataset.html` | Ganti nilai → §2.1 |
| Tabel 4.3 cross-dataset | `tabel_4_3_hasil_cross_dataset.html` | Ganti nilai → §2.2 |
| Tabel 4.4 generalization drop | `tabel_4_4_generalization_drop.html` | Ganti nilai → §2.3 |
| Tabel 4.5 AUC per tier | `tabel_4_5_auc_ukuran_sampel.html` | Ganti nilai → §2.4 |
| Tabel 4.6 ringkasan RM | `tabel_4_6_ringkasan_rumusan_masalah.html` | Ganti angka narasi → §2.5 |
| Gambar 4.3/4.5/4.7/4.8 (bar/drop/scaling) | `media_v2/` | **Regen** dari tabel baru → §4B |
| Gambar 4.4/4.6/4.9 (ROC/CM) | `media_v2/` | **TAMBAH** dari `outputs/roc_cm/` → §4A |
| Gambar 4.10 (kurva pelatihan) | `media_v2/` | **TAMBAH** dari `outputs/plots/` (run baru) → §4C |
| Prosa inline BAB IV | docx | Isi/ganti angka → §3 |

---

## 2. NILAI BARU PER TABEL (3-seed mean ± std; format `lama → baru`)

### 2.1 Tabel 4.2 — In-Dataset (n=750)
| Dataset | Model | Akurasi | Presisi | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| FFPP | spatial | 0,700±0,002 → **0,700±0,010** | 0,662±0,005 → **0,666±0,015** | 0,766±0,009 → **0,750±0,023** | 0,710±0,001 → **0,705±0,008** | 0,780±0,002 → **0,778±0,010** |
| FFPP | hybrid | 0,610±0,007 → **0,600±0,020** | 0,588±0,007 → **0,576±0,028** | 0,618±0,012 → **0,644±0,068** | 0,603±0,008 → **0,606±0,014** | 0,650±0,008 → **0,644±0,009** |
| FFPP | freq | 0,531±0,024 → **0,544±0,015** | 0,512±0,028 → **0,525±0,021** | 0,560±0,131 → **0,590±0,122** | 0,529±0,055 → **0,550±0,043** | 0,546±0,037 → **0,562±0,007** |
| CDF | spatial | 0,915±0,003 → **0,913±0,001** | 0,906±0,010 → **0,908±0,013** | 0,912±0,007 → **0,904±0,015** | 0,909±0,003 → **0,906±0,002** | 0,969±0,001 → **0,971±0,002** |
| CDF | hybrid | 0,858±0,014 → **0,847±0,014** | 0,851±0,034 → **0,845±0,026** | 0,843±0,023 → **0,824±0,032** | 0,847±0,013 → **0,834±0,016** | 0,924±0,005 → **0,919±0,010** |
| CDF | freq | 0,563±0,016 → **0,552±0,019** | 0,529±0,018 → **0,521±0,021** | 0,495±0,039 → **0,503±0,062** | 0,511±0,028 → **0,510±0,034** | 0,586±0,028 → **0,562±0,014** |

### 2.2 Tabel 4.3 — Cross-Dataset (n=750)
| Arah | Model | Akurasi | Presisi | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| FFPP→CDF | spatial | 0,608±0,006 → **0,627±0,005** | 0,571±0,007 → **0,594±0,012** | 0,618±0,012 → **0,637±0,040** | 0,594±0,008 → **0,614±0,013** | 0,648±0,013 → **0,678±0,008** |
| FFPP→CDF | hybrid | 0,611±0,025 → **0,624±0,012** | 0,584±0,036 → **0,599±0,024** | 0,570±0,016 → **0,599±0,119** | 0,576±0,009 → **0,594±0,048** | 0,648±0,031 → **0,665±0,016** |
| FFPP→CDF | freq | 0,550±0,005 → **0,541±0,004** | 0,621±0,027 → **0,566±0,018** | 0,069±0,017 → **0,064±0,017** | 0,124±0,027 → **0,115±0,028** | 0,655±0,007 → **0,606±0,009** |
| CDF→FFPP | spatial | 0,558±0,003 → **0,554±0,003** | 0,932±0,026 → **0,923±0,020** | 0,083±0,009 → **0,074±0,005** | 0,153±0,015 → **0,137±0,009** | 0,629±0,001 → **0,607±0,020** |
| CDF→FFPP | hybrid | 0,569±0,012 → **0,564±0,006** | 0,789±0,082 → **0,736±0,079** | 0,143±0,056 → **0,142±0,011** | 0,237±0,073 → **0,238±0,011** | 0,563±0,011 → **0,555±0,031** |
| CDF→FFPP | freq | 0,571±0,007 → **0,558±0,002** | 0,549±0,012 → **0,543±0,018** | 0,596±0,072 → **0,531±0,162** | 0,570±0,026 → **0,526±0,085** | 0,591±0,002 → **0,575±0,012** |

*Perbaikan naratif:* freq FFPP→CDF AUC 0,655→**0,606** (kini terendah; spatial 0,678 tertinggi) — lebih koheren dgn klaim "freq lemah".

### 2.3 Tabel 4.4 — Generalization Drop F1 (n=750)
| Model | Train | F1 In | F1 Cross | Δ |
|---|---|---|---|---|
| spatial | FFPP | 0,710 → **0,705** | 0,594 → **0,614** | +0,116 → **+0,091** |
| spatial | CDF | 0,909 → **0,906** | 0,153 → **0,137** | +0,756 → **+0,769** |
| hybrid | FFPP | 0,603 → **0,606** | 0,576 → **0,594** | +0,027 → **+0,012** |
| hybrid | CDF | 0,847 → **0,834** | 0,237 → **0,238** | +0,609 → **+0,597** |
| freq | FFPP | 0,529 → **0,550** | 0,124 → **0,115** | +0,406 → **+0,435** |
| freq | CDF | 0,511 → **0,510** | 0,570 → **0,526** | −0,058 → **−0,015** |

### 2.4 Tabel 4.5 — AUC In-Dataset per tier
| Dataset | Model | n=250 | n=500 | n=750 |
|---|---|---|---|---|
| FFPP | spatial | 0,746 → **0,743** | 0,693 → **0,693** | 0,780 → **0,778** |
| FFPP | hybrid | 0,542 → **0,540** | 0,582 → **0,616** | 0,650 → **0,644** |
| FFPP | freq | 0,480 → **0,469** | 0,570 → **0,545** | 0,546 → **0,562** |
| CDF | spatial | 0,942 → **0,914** | 0,967 → **0,945** | 0,969 → **0,971** |
| CDF | hybrid | 0,812 → **0,787** | 0,892 → **0,839** | 0,924 → **0,919** |
| CDF | freq | 0,569 → **0,500** | 0,615 → **0,549** | 0,586 → **0,562** |

*Catatan:* CDF-freq n250 = **0,500** (tepat acak); freq kedua dataset kini **monoton naik** terhadap n (lebih mudah dijelaskan).

### 2.5 Tabel 4.6 — Ringkasan Rumusan Masalah (ganti angka narasi)
| Sel | Lama | Baru |
|---|---|---|
| RM1 | "AUC turun ke **0,629–0,648** dan recall runtuh hingga **0,083**" | "AUC turun ke **0,607–0,678** dan recall runtuh hingga **0,074**" |
| RM2 | "Δ hybrid **+0,027** vs spatial **+0,116**" | "Δ hybrid **+0,012** vs spatial **+0,091**" |
| RM3 | "AUC s.d. **0,969**); freq nyaris acak (**0,55–0,59**)" | "AUC s.d. **0,971**); freq nyaris acak (**0,56–0,61**)" |

---

## 3. ANGKA INLINE PROSA BAB IV (isi/ganti — 3-seed run baru)

| Lokasi | Teks | Isi |
|---|---|---|
| §4.1.3 & caption | "tier ( )", "( , rata-rata…)" | **n = 750** |
| §4.1.4 | "AUC berada pada kisaran ( )." | **0,56–0,68** |
| §4.1.4 | spatial "presisi sangat tinggi ( ) … recall runtuh menjadi ( )" | **0,923** ; **0,074** |
| §4.1.4 | hybrid "(presisi , recall )" | **0,736** ; **0,142** |
| §4.1.4 | freq "keruntuhan recall ( )" (FFPP→CDF) | **0,064** |
| §4.1.4 | "spasial dan hybrid … recall lebih wajar ( dan )" | **0,637** dan **0,599** |
| §4.1.6 | "tiga tier …, yaitu , , dan ." | **250, 500, 750** |
| Caption 4.3/4.5/4.7 | "( )" | **(n = 750)** |

---

## 4. GAMBAR — ✅ SUDAH DIBUAT SEMUA di `documents/media_v2/`

Kedelapan gambar BAB IV (4.3–4.10) sudah ada di `media_v2/` dengan penamaan `gambar_4_#`, semuanya dari run baru 2026-06-20:
- **Bar/scaling/drop** (4.3, 4.5, 4.7, 4.8): regen dari tabel 3-seed baru via `scripts/make_bab4_figures.py` (skrip kini default baca `outputs/tables/`; bisa override arg ke run lama). Label **Indonesia**, angka **cocok Tabel 4.2–4.5**.
- **ROC** (4.4, 4.6) & **CM** (4.9) & **kurva pelatihan** (4.10): komposit dari `outputs/roc_cm/` dan `outputs/plots/`. Label internal **Inggris**, dan menampilkan **seed 0**.

> ⚠️ **Catatan seed-0 (penting untuk caption):** ROC/CM/kurva pelatihan (4.4, 4.6, 4.9, 4.10) menampilkan **satu seed (seed 0)** — sebuah kurva ROC tidak bisa jadi rata-rata 3 seed. Maka AUC di legenda ROC sedikit berbeda dari rata-rata Tabel 4.2/4.3 (mis. FFPP spatial ROC 0,767 vs tabel 0,778). Bar/scaling/drop (4.3/4.5/4.7/4.8) **3-seed**, persis cocok tabel. Sertakan keterangan "seed 0" pada caption 4.4/4.6/4.9/4.10 (sudah ditulis di §4D).

### 4D. LABEL / CAPTION GAMBAR BAB IV (skema final 10 gambar — siap tempel)
Caption diletakkan **di bawah** gambar, rata tengah, format "Gambar 4.x …" (Pedoman). `→` = tanda panah.

| No | File `media_v2/` | Caption |
|---|---|---|
| 4.1 | *(screenshot demo)* | Gambar 4.1 Antarmuka purwarupa perbandingan tiga model pada Hugging Face Spaces |
| 4.2 | *(screenshot demo)* | Gambar 4.2 Panel "what the models see": potongan wajah (masukan spasial) dan spektrum FFT (masukan frekuensi) |
| 4.3 | `gambar_4_3_perbandingan_in_dataset.png` | Gambar 4.3 Perbandingan performa in-dataset ketiga model pada FaceForensics++ dan Celeb-DF (n = 750) |
| **4.4** | `gambar_4_4_roc_in_dataset.png` | Gambar 4.4 Kurva ROC evaluasi in-dataset ketiga model pada FaceForensics++ dan Celeb-DF (n = 750, seed 0) |
| 4.5 | `gambar_4_5_perbandingan_cross_dataset.png` | Gambar 4.5 Perbandingan performa cross-dataset ketiga model pada kedua arah pengujian (n = 750) |
| **4.6** | `gambar_4_6_roc_cross_dataset.png` | Gambar 4.6 Kurva ROC evaluasi cross-dataset ketiga model pada kedua arah pengujian (n = 750, seed 0) |
| 4.7 | `gambar_4_7_generalization_drop.png` | Gambar 4.7 Generalization drop F1-Score per model dan arah pelatihan (n = 750) |
| 4.8 | `gambar_4_8_scaling_auc.png` | Gambar 4.8 Tren AUC terhadap ukuran sampel pelatihan (in-dataset dan cross-dataset) |
| **4.9** | `gambar_4_9_confusion_matrix.png` | Gambar 4.9 Confusion matrix model spasial pada evaluasi in-dataset (Celeb-DF) dan cross-dataset (Celeb-DF→FaceForensics++) yang memperlihatkan keruntuhan recall lintas dataset (n = 750, seed 0) |
| **4.10** | `gambar_4_10_kurva_pelatihan.png` | Gambar 4.10 Kurva dinamika pelatihan cabang frekuensi (FreqCNN) dan cabang spasial (XceptionNet) pada FaceForensics++ (n = 750) |

> Opsional (rapi): label internal gambar 4.4/4.6/4.9/4.10 masih Inggris ("In-Dataset FFPP", "Confusion Matrix — Spatial", "Epoch/Loss"). Bisa diregen ke Indonesia dari checkpoint (tidak tersedia lokal) — readable apa adanya, jadi prioritas rendah.

---

## 5. CEK NARASI — semua klaim utama TETAP BERLAKU (3-seed run baru) ✅
| Klaim | Run baru | Status |
|---|---|---|
| spatial > hybrid > freq (in) | FFPP 0,778>0,644>0,562; CDF 0,971>0,919>0,562 | ✅ |
| hybrid tidak ungguli spatial (RM3) | hybrid < spatial semua in-dataset | ✅ |
| freq nyaris acak | in 0,562/0,562 | ✅ (pita 0,56–0,61) |
| spatial runtuh lintas-dataset (RM1) | CDF→FFPP recall 0,074 | ✅ |
| FFT perkecil drop FFPP→CDF (RM2) | hybrid Δ+0,012 < spatial Δ+0,091 | ✅ |
| freq FFPP→CDF recall collapse | 0,064 | ✅ |
| freq cross bukan lagi AUC tertinggi | FFPP→CDF freq 0,606 < spatial 0,678 | ✅ lebih koheren |

**Tidak ada klaim yang patah.**

---

## 6. URUTAN KERJA
1. ✅ ~~Ambil data 3-seed~~ — sudah ada di repo (`outputs/tables/`).
2. ✅ ~~Update 5 tabel HTML~~ (`documents/table/tabel_4_2..4_6`) — selesai, terverifikasi cocok sumber.
3. ✅ ~~Komposit ROC/CM (4.4/4.6/4.9)~~ — di `media_v2/`.
4. ✅ ~~Regen 4 chart bar/scaling/drop (4.3/4.5/4.7/4.8)~~ — `make_bab4_figures.py` (default kini `outputs/tables/`).
5. ✅ ~~Gambar 4.10 kurva pelatihan~~ — di `media_v2/gambar_4_10_kurva_pelatihan.png`.
6. ⏳ Tempel 5 tabel HTML + 8 gambar ke docx; isi angka inline prosa BAB IV (§3) + caption (§4D, n=750).
7. ⏳ Renumber gambar BAB IV → skema 4.1–4.10 (ACTION doc §5.2) + Update DAFTAR GAMBAR.
8. ⏳ `Ctrl+A → F9` Update Fields.
9. (Bersih-bersih) hapus untracked `outputs/{plots,tables}/n50,n200,n400` (sisa lokal lama).

---

## Lampiran — sumber
Run baru 3-seed: `deepfake_hybrid/outputs/tables/n{250,500,750}/Table*_summary.csv` (commit `26f5dae`). Run lama: `results_vast_20260609/`. Seed-0 cek silang: `outputs/roc_cm/*_metrics.json`. n=100 tidak masuk tabel (tak stabil).
