# BAB V (Penutup) + Abstrak — Draft Siap-Tempel

> Framing: studi komparatif + temuan negatif jujur (hybrid TIDAK mengungguli baseline spasial). Istilah asing di-*italic*. Angka dari hasil run terbaru 2026-06-20 (`outputs/tables/`, 3 seed) — konsisten dengan Tabel 4.2–4.6. Judul bab "BAB V PENUTUP" sesuai Pedoman 5.16.
>
> **Sitasi (penting):** ditulis **(Nama, Tahun)** di draft ini **hanya untuk memudahkan input ke Word** — agar jelas sumber mana yang harus disisipkan. Saat ditempel, sisipkan sebagai **CITATION field** dengan style IEEE → otomatis **render `[N]`** sesuai Pedoman 4.5.5. Jadi (Nama, Tahun) di draft = penunjuk, **bukan** gaya final. Padanan: Qian et al. (2020) → [11]; Alam et al. (2025) → [13].

---

# BAB V PENUTUP

Bab ini menutup penelitian dengan menyarikan temuan utama menjadi kesimpulan yang menjawab setiap rumusan masalah, serta menyampaikan saran bagi pengembangan dan penelitian lanjutan. Kesimpulan disusun berdasarkan hasil eksperimen yang telah dipaparkan dan dianalisis pada BAB IV, sedangkan saran diarahkan pada perbaikan keterbatasan yang ditemukan selama penelitian.

## 5.1 Kesimpulan

Penelitian ini merupakan studi komparatif yang mengukur kontribusi domain spasial, domain frekuensi, dan gabungan keduanya melalui arsitektur *hybrid* XceptionNet–FFT terhadap performa deteksi *deepfake*, baik pada skenario *in-dataset* maupun *cross-dataset*. Berdasarkan hasil dan pembahasan pada BAB IV, diperoleh kesimpulan sebagai berikut.

Pertama, sehubungan dengan penurunan performa detektor spasial murni pada pengujian lintas dataset, model spasial (XceptionNet) terbukti mengalami degradasi yang substansial. Nilai AUC yang tinggi pada evaluasi *in-dataset* (0,78 pada FaceForensics++ dan 0,97 pada Celeb-DF) turun menjadi sekitar 0,61–0,68 pada evaluasi *cross-dataset*, disertai keruntuhan *recall* yang paling parah pada arah CDF→FFPP (*recall* ≈ 0,07), dengan *generalization drop* F1 mencapai +0,77. Hal ini menegaskan bahwa detektor spasial murni sangat bergantung pada karakteristik dataset pelatihan dan lemah dalam menggeneralisasi ke metode manipulasi yang belum pernah dilihat.

Kedua, sehubungan dengan pengaruh penambahan analisis domain frekuensi terhadap penurunan tersebut, manfaat yang diberikan bersifat parsial dan bergantung arah. Pada arah FFPP→CDF, model *hybrid* berhasil menahan degradasi dengan *generalization drop* yang jauh lebih kecil (Δ ≈ +0,01) dibanding model spasial (Δ ≈ +0,09); namun keuntungan ini tidak konsisten pada arah CDF→FFPP, tidak disertai peningkatan AUC yang menyeluruh, dan diperoleh dengan mengorbankan performa *in-dataset* yang lebih rendah. Dengan demikian, penambahan FFT belum mampu menghasilkan peningkatan generalisasi yang konsisten dan menyeluruh.

Ketiga, sehubungan dengan kontribusi masing-masing komponen, domain spasial merupakan penyumbang performa utama, sedangkan cabang frekuensi berperforma nyaris setara tebakan acak (AUC 0,56–0,61) sehingga cenderung menjadi sumber *noise* dalam fusi. Akibatnya, model *hybrid* tidak mengungguli baseline spasial murni pada seluruh tier ukuran sampel yang andal dan pada kedua dataset.

Secara keseluruhan, dapat disimpulkan bahwa dalam konfigurasi yang diuji, arsitektur *hybrid* XceptionNet–FFT **belum** memberikan keunggulan dibanding baseline spasial, kontribusi domain frekuensi masih terbatas, dan generalisasi lintas dataset tetap menjadi tantangan terbuka. Temuan negatif ini, beserta analisis akar penyebabnya, merupakan kontribusi ilmiah yang sahih dan menjadi dasar bagi saran perbaikan pada subbab berikut.

## 5.2 Saran

Berdasarkan keterbatasan dan akar penyebab yang teridentifikasi pada penelitian ini, diajukan beberapa saran yang diarahkan pada perbaikan metode maupun penelitian lanjutan.

1. **Memperkuat cabang frekuensi.** Lemahnya cabang frekuensi diduga kuat disebabkan oleh hilangnya sidik jari spektral akibat *face-cropping* dan kompresi. Penelitian lanjutan dapat menggunakan representasi frekuensi yang lebih tahan terhadap kedua proses tersebut, misalnya menghitung FFT pada citra penuh (tanpa *crop*), memanfaatkan informasi fasa, atau menerapkan analisis frekuensi multi-skala.
2. **Memperbaiki mekanisme fusi.** Mekanisme *Squeeze-and-Excitation gating* perlu diregularisasi atau disetel agar mampu menekan cabang yang lemah secara efektif; alternatif lain adalah melakukan *pretraining* atau pembekuan cabang frekuensi sebelum fusi, atau mengadopsi mekanisme atensi dua-domain yang lebih canggih sebagaimana ditunjukkan oleh Qian et al. (2020) dan Alam et al. (2025).
3. **Mengeksplorasi domain transformasi alternatif.** Selain FFT, transformasi seperti DCT atau *wavelet* dapat diteliti karena dilaporkan menghasilkan artefak yang lebih stabil antar-arsitektur GAN.
4. **Memperluas skala dan dimensi temporal.** Penelitian dapat memakai jumlah data pelatihan yang lebih besar, variasi tingkat kompresi yang lebih beragam, serta pemodelan temporal antar-*frame*, mengingat penelitian ini terbatas pada analisis level *frame*.
5. **Implikasi praktis.** Untuk kebutuhan penerapan saat ini, baseline spasial (XceptionNet) tetap menjadi pilihan paling andal, sementara peningkatan generalisasi lintas dataset memerlukan penelitian lebih lanjut.

---

# ABSTRAK (Bahasa Indonesia)

> Satu paragraf, *cetak miring*, Times New Roman 12 pt, 100–200 kata.

*Deteksi deepfake yang andal merupakan kebutuhan forensik digital yang mendesak, namun detektor berbasis domain spasial murni umumnya lemah dalam generalisasi lintas dataset, sementara domain frekuensi diklaim mampu menutupi keterbatasan tersebut. Penelitian ini melakukan studi komparatif untuk mengukur kontribusi domain frekuensi melalui arsitektur hybrid XceptionNet–FFT dengan late fusion dan Squeeze-and-Excitation gating, dibandingkan model domain tunggal. Tiga model (spasial, frekuensi, dan hybrid) dievaluasi pada dua dataset benchmark, yaitu FaceForensics++ dan Celeb-DF, dalam skenario in-dataset dan cross-dataset pada beberapa ukuran sampel dengan tiga seed, menggunakan metrik akurasi, presisi, recall, F1-score, dan AUC pada level frame dengan pembagian per-video. Hasil menunjukkan model spasial konsisten paling unggul (AUC in-dataset hingga 0,97), sedangkan cabang frekuensi berperforma nyaris setara tebakan acak (AUC 0,56–0,61) sehingga model hybrid tidak mengungguli baseline spasial. Pada pengujian cross-dataset, performa seluruh model menurun (AUC sekitar 0,56–0,68) disertai keruntuhan recall, dan penambahan analisis frekuensi hanya menekan penurunan generalisasi secara parsial dan bergantung arah. Penelitian menyimpulkan bahwa kontribusi domain frekuensi terbatas pada konfigurasi ini dan generalisasi lintas dataset tetap menjadi tantangan terbuka.*

**Kata kunci:** *deteksi deepfake; XceptionNet; domain frekuensi; arsitektur hybrid; generalisasi lintas dataset*

---

# ABSTRACT (English)

> One paragraph, *italics*, Times New Roman 12 pt, 100–200 words.

*Reliable deepfake detection is an urgent digital-forensics need, yet purely spatial-domain detectors generally generalize poorly across datasets, while the frequency domain is claimed to mitigate this limitation. This study conducts a comparative investigation to measure the contribution of the frequency domain through a hybrid XceptionNet–FFT architecture with late fusion and Squeeze-and-Excitation gating, compared against single-domain models. Three models (spatial, frequency, and hybrid) are evaluated on two benchmark datasets, FaceForensics++ and Celeb-DF, under in-dataset and cross-dataset scenarios across several training-set sizes with three seeds, using accuracy, precision, recall, F1-score, and AUC at the frame level with video-level splits. The results show that the spatial model is consistently the best (in-dataset AUC up to 0.97), whereas the frequency branch performs near chance (AUC 0.56–0.61), so the hybrid model does not outperform the spatial baseline. Under cross-dataset testing, all models degrade (AUC around 0.56–0.68) with a collapse in recall, and adding frequency analysis only partially and directionally reduces the generalization drop. The study concludes that the contribution of the frequency domain is limited in this configuration and that cross-dataset generalization remains an open challenge.*

**Keywords:** *deepfake detection; XceptionNet; frequency domain; hybrid architecture; cross-dataset generalization*
