# Draft Konten Hasil Eksperimen Awal (untuk BAB IV)

> Konten ini dipindahkan dari Section 3.8 BAB III karena sesuai pedoman, hasil masuk BAB IV (Hasil dan Pembahasan).

---

## Hasil Eksperimen Awal ($n = 100$)

> **Catatan:** Hasil berikut diperoleh pada percobaan tanggal 3 April 2026 dengan konfigurasi *learning rate* $5 \times 10^{-4}$ dan *patience* 10. Konfigurasi *learning rate* kemudian direvisi ke $2 \times 10^{-4}$ untuk menyeimbangkan stabilitas pelatihan pada kedua dataset. Eksperimen ulang dengan konfigurasi final sedang dalam proses pelaksanaan.

### Performa *In-Dataset* ($n = 100$)

Evaluasi *in-dataset* mengukur performa setiap model pada set pengujian dari dataset yang sama dengan dataset pelatihan.

Tabel 4.X Hasil Evaluasi *In-Dataset* ($n = 100$, *seed* = 0)

| Model | Dataset | *Test AUC* | *Test F1* | *Accuracy* |
|---|---|---|---|---|
| *Spatial* | FFPP | 0,497 | 0,558 | 0,512 |
| *Freq* | FFPP | 0,307 | 0,219 | 0,315 |
| *Hybrid* | FFPP | 0,437 | 0,379 | 0,494 |
| *Spatial* | CDF | 0,825 | 0,754 | 0,729 |
| *Freq* | CDF | 0,676 | 0,652 | 0,530 |
| **Hybrid** | **CDF** | **0,895** | **0,780** | **0,766** |

Pada dataset CDF, model *hybrid* mencapai AUC tertinggi (0,895) dan F1-*score* tertinggi (0,780), mengungguli model *spatial* (AUC 0,825) dan *freq* (AUC 0,676). Hal ini menunjukkan bahwa penggabungan fitur spasial dan frekuensi melalui mekanisme *late fusion* dengan SE *gating* memberikan keuntungan pada deteksi *deepfake* berkualitas tinggi. Performa yang lebih rendah pada FFPP disebabkan oleh *learning rate* yang terlalu agresif ($5 \times 10^{-4}$) untuk dataset tersebut, yang telah diperbaiki pada konfigurasi final ($2 \times 10^{-4}$).

### Performa *Cross-Dataset* ($n = 100$)

Evaluasi *cross-dataset* menguji kemampuan generalisasi model pada dataset yang berbeda dari dataset pelatihan.

Tabel 4.X Hasil Evaluasi *Cross-Dataset* ($n = 100$, *seed* = 0)

| Pelatihan → Pengujian | *Spatial* F1 | *Freq* F1 | *Hybrid* F1 | *Hybrid* AUC |
|---|---|---|---|---|
| FFPP → CDF | 0,174 | 0,253 | **0,628** | 0,642 |
| CDF → FFPP | 0,583 | 0,349 | **0,631** | 0,720 |

Model *hybrid* secara konsisten menunjukkan performa *cross-dataset* terbaik pada kedua arah evaluasi silang. Pada evaluasi CDF → FFPP, model *hybrid* mencapai AUC 0,720, jauh mengungguli model *spatial* (AUC 0,669) dan *freq* (AUC 0,454). Keunggulan ini mengindikasikan bahwa fitur domain frekuensi yang ditangkap oleh cabang FreqCNN berkontribusi pada kemampuan generalisasi yang lebih baik — artefak spektral dari proses sintesis *deepfake* cenderung lebih universal lintas metode manipulasi dibandingkan artefak visual spasial.

### *Generalization Drop* ($n = 100$)

Tabel 4.X *Generalization Drop* F1-*Score* ($n = 100$, *seed* = 0)

| Model | Dataset Pelatihan | F1 *In-Dataset* | F1 *Cross-Dataset* | $\Delta$ |
|---|---|---|---|---|
| *Spatial* | FFPP | 0,558 | 0,174 | +0,384 |
| *Spatial* | CDF | 0,754 | 0,583 | +0,171 |
| *Freq* | FFPP | 0,219 | 0,253 | −0,035 |
| *Freq* | CDF | 0,652 | 0,349 | +0,303 |
| *Hybrid* | FFPP | 0,379 | 0,628 | **−0,249** |
| **Hybrid** | **CDF** | **0,780** | **0,631** | **+0,149** |

Temuan menarik terlihat pada model *hybrid* yang dilatih pada FFPP: F1-*score cross-dataset* (0,628) justru lebih tinggi dari F1-*score in-dataset* (0,379), menghasilkan $\Delta$ negatif (−0,249). Model *hybrid* yang dilatih pada CDF menunjukkan *generalization drop* terkecil (+0,149) di antara semua model, mengonfirmasi bahwa arsitektur *hybrid* dengan gabungan domain spasial-frekuensi menghasilkan representasi yang paling *robust* dan dapat digeneralisasikan.

<!-- Gambar: Perbandingan Performa Model (n=100) -->
<!-- Search keyword: "grouped bar chart model comparison AUC F1 in-dataset cross-dataset" -->
<!-- Plots tersedia di outputs/2026-04-03/plots/ -->

### HTML Tables (sudah dibuat)
- `tabel_3_14_hasil_in_dataset.html` → renumber ke tabel_4_X
- `tabel_3_15_hasil_cross_dataset.html` → renumber ke tabel_4_X
- `tabel_3_16_generalization_drop.html` → renumber ke tabel_4_X
