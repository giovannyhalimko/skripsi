# PERBAIKAN — Angka Inline SELURUH DOKUMEN (run baru 2026-06-20)

**Cek menyeluruh WORD pada 2026-06-20.** Tabel embedded (4.2–4.6) **sudah** diisi nilai run baru. Yang **masih kosong/perlu diganti** = paragraf interpretasi ("konten"), pengantar, caption, **Abstrak (ID+EN)**, dan **BAB V Kesimpulan**.
**Cara baca:** teks siap-tempel (blockquote). Isi yang harus diketik dibungkus `[PERBAIKAN]…[/PERBAIKAN]` (tag jangan ikut diketik).
**Sumber:** `deepfake_hybrid/outputs/tables/n*/Table*_summary.csv` (3-seed run baru). Konsisten dgn Tabel 4.2–4.6 HTML.

> 🔢 **Referensi nilai cepat (3-seed):**
> In-AUC — FFPP: spatial **0,778** / hybrid **0,644** / freq **0,562**; CDF: spatial **0,971** / hybrid **0,919** / freq **0,562**.
> Cross-AUC — FFPP→CDF: **0,678 / 0,665 / 0,606**; CDF→FFPP: **0,607 / 0,555 / 0,575**.
> Drop F1 — spatial FFPP **+0,091**, CDF **+0,769**; hybrid FFPP **+0,012**, CDF **+0,597**; freq FFPP **+0,435**, CDF **−0,015**.
> Cross recall/F1 — spatial CDF→FFPP rec **0,074** F1 **0,137**; hybrid CDF→FFPP rec **0,142** F1 **0,238**; freq FFPP→CDF rec **0,064** F1 **0,115**; spatial FFPP→CDF rec **0,637** F1 **0,614**; hybrid FFPP→CDF rec **0,599** F1 **0,594**.

---

# BAGIAN 1 — BAB IV

## 4.1.3 In-Dataset

**(a) Pengantar** — masih ada satu blank:
> …Hasil pada tier [PERBAIKAN]n = 750[/PERBAIKAN] untuk kedua dataset disajikan pada Tabel 4.2, sedangkan perbandingan visualnya ditunjukkan pada Gambar 4.3.

**(b) KONTEN interpretasi** ← INTI yang kamu maksud (banyak blank):
> Pada kedua dataset, model spasial memperoleh nilai tertinggi pada seluruh metrik, diikuti model hybrid, dan model frekuensi pada posisi terendah. Pada FFPP, AUC model spasial mencapai [PERBAIKAN]0,778[/PERBAIKAN], sedangkan model hybrid dan frekuensi masing-masing [PERBAIKAN]0,644[/PERBAIKAN] dan [PERBAIKAN]0,562[/PERBAIKAN]. Pola yang sama terjadi pada CDF dengan selisih yang lebih lebar, yaitu AUC [PERBAIKAN]0,971[/PERBAIKAN] untuk model spasial, [PERBAIKAN]0,919[/PERBAIKAN] untuk hybrid, dan [PERBAIKAN]0,562[/PERBAIKAN] untuk frekuensi. Dataset CDF secara konsisten lebih mudah dideteksi dibanding FFPP bagi seluruh model. Nilai AUC model frekuensi yang berada pada kisaran [PERBAIKAN]0,56[/PERBAIKAN] menunjukkan kemampuan diskriminasi yang hanya sedikit di atas tebakan acak ([PERBAIKAN]0,5[/PERBAIKAN]). Urutan peringkat ini stabil, terlihat dari simpangan baku antar-seed yang kecil terutama pada model spasial.

**(c) Paragraf ROC**:
> …Urutan luas area di bawah kurva (AUC) konsisten dengan Tabel 4.2 Hasil Evaluasi In-Dataset ([PERBAIKAN]n = 750[/PERBAIKAN], rata-rata ± simpangan baku atas 3 seed), …

## 4.1.4 Cross-Dataset

**(a) Pengantar**:
> …Hasil untuk kedua arah pengujian pada tier [PERBAIKAN]n = 750[/PERBAIKAN] disajikan pada Tabel 4.3, dan perbandingan visualnya pada Gambar [PERBAIKAN]4.5[/PERBAIKAN] Perbandingan performa cross-dataset ketiga model pada kedua arah pengujian ([PERBAIKAN]n = 750[/PERBAIKAN]).

*(Catatan: teks menulis "Gambar 4.4" → seharusnya **4.5** karena bar cross-dataset bernomor 4.5; lihat §FLAGS.)*

**(b) KONTEN temuan**:
> Dibandingkan evaluasi in-dataset, performa seluruh model menurun tajam pada skenario cross-dataset, dengan AUC berada pada kisaran [PERBAIKAN]0,56–0,68[/PERBAIKAN]. Penurunan paling mencolok tampak pada metrik recall di beberapa konfigurasi. Pada arah CDF→FFPP, model spasial mencatat presisi sangat tinggi ([PERBAIKAN]0,923[/PERBAIKAN]) namun recall runtuh menjadi [PERBAIKAN]0,074[/PERBAIKAN], yang berarti model nyaris tidak mengenali sampel fake dari dataset yang berbeda; pola serupa terjadi pada model hybrid (presisi [PERBAIKAN]0,736[/PERBAIKAN], recall [PERBAIKAN]0,142[/PERBAIKAN]). Sebaliknya, pada arah FFPP→CDF, model frekuensi mengalami keruntuhan recall ([PERBAIKAN]0,064[/PERBAIKAN]) sementara model spasial dan hybrid mempertahankan recall yang lebih wajar ([PERBAIKAN]0,637[/PERBAIKAN] dan [PERBAIKAN]0,599[/PERBAIKAN]). …

## 4.1.5 Generalization Drop

**(a) Pengantar** (blank = simbol Δ + n):
> Generalization drop ([PERBAIKAN]Δ[/PERBAIKAN]) mengukur besarnya degradasi performa antara evaluasi in-dataset dan cross-dataset… Nilai [PERBAIKAN]Δ[/PERBAIKAN] yang kecil menandakan generalisasi yang baik… Hasil perhitungan untuk [PERBAIKAN]n = 750[/PERBAIKAN] disajikan pada Tabel 4.4 dan divisualisasikan pada Gambar [PERBAIKAN]4.7[/PERBAIKAN].

*(Catatan: teks menulis "Gambar 4.5" → seharusnya **4.7**; lihat §FLAGS.)*

**(b) KONTEN interpretasi**:
> Besarnya generalization drop sangat bergantung pada arah pelatihan. Pada model yang dilatih CDF, degradasi sangat besar, yaitu [PERBAIKAN]+0,769[/PERBAIKAN] untuk spasial dan [PERBAIKAN]+0,597[/PERBAIKAN] untuk hybrid. Sebaliknya, pada model yang dilatih FFPP, degradasi jauh lebih kecil, bahkan model hybrid mencatat [PERBAIKAN]+0,012[/PERBAIKAN] yang merupakan nilai terkecil di antara seluruh konfigurasi. Adapun model frekuensi menunjukkan [PERBAIKAN]Δ[/PERBAIKAN] yang bervariasi, dari [PERBAIKAN]+0,435[/PERBAIKAN] (pelatihan FFPP) hingga negatif [PERBAIKAN]−0,015[/PERBAIKAN] (pelatihan CDF); namun nilai ini perlu ditafsirkan dengan hati-hati karena performa in-dataset model frekuensi memang sudah rendah, sehingga praktis tidak ada performa yang dapat turun. …

> ⚠️ **Perubahan kata, bukan hanya angka:** kalimat lama "model frekuensi menunjukkan Δ yang **kecil hingga negatif**" **tidak lagi akurat** — freq FFPP drop = **+0,435 (besar)**. Saya reword jadi "bervariasi, dari +0,435 (FFPP) hingga negatif −0,015 (CDF)". Pakai versi ini.

## 4.1.6 Pengaruh Ukuran Sampel

**(a) Pengantar**:
> Untuk mengamati pengaruh jumlah data pelatihan, performa diukur pada tiga tier ukuran sampel yang andal, yaitu [PERBAIKAN]250[/PERBAIKAN], [PERBAIKAN]500[/PERBAIKAN], dan [PERBAIKAN]750[/PERBAIKAN]. Nilai AUC in-dataset untuk setiap tier disajikan pada Tabel 4.5, dan trennya divisualisasikan pada Gambar [PERBAIKAN]4.8[/PERBAIKAN].

*(Catatan: teks menulis "Gambar 4.6" → seharusnya **4.8**; lihat §FLAGS.)*

**(b) KONTEN interpretasi**:
> Secara umum, performa meningkat seiring bertambahnya ukuran sampel, paling jelas terlihat pada model spasial dan hybrid di dataset CDF yang naik konsisten dari [PERBAIKAN]0,79[/PERBAIKAN] hingga [PERBAIKAN]0,97[/PERBAIKAN]. Peningkatan pada dataset FFPP berlangsung lebih fluktuatif; sebagai contoh, AUC model spasial pada FFPP sempat menurun di [PERBAIKAN]n = 500[/PERBAIKAN] sebelum kembali naik pada [PERBAIKAN]n = 750[/PERBAIKAN], yang mencerminkan tingkat kesulitan FFPP yang lebih tinggi dan variasi antar-seed yang lebih besar. Adapun model frekuensi tetap berada pada kisaran rendah (AUC ≈ [PERBAIKAN]0,5[/PERBAIKAN]) di seluruh tier, menandakan bahwa penambahan data tidak secara berarti memperbaiki kemampuan cabang frekuensi. …

*(Nilai: CDF naik dari hybrid n250 0,787 → spasial n750 0,971 ⇒ "0,79 hingga 0,97". freq AUC seluruh tier 0,47–0,56 ⇒ "≈ 0,5".)*

## 4.2.1 Kontribusi Domain (RM3)
> …Model spasial yang hanya memanfaatkan fitur visual XceptionNet justru menjadi penyumbang performa terbesar, dengan AUC in-dataset mencapai [PERBAIKAN]0,971[/PERBAIKAN] pada CDF dan [PERBAIKAN]0,778[/PERBAIKAN] pada FFPP. …
> Sebaliknya, model frekuensi … dengan AUC yang hanya sedikit di atas tebakan acak ([PERBAIKAN]0,5[/PERBAIKAN]). …

## 4.2.2 Penurunan Spasial Cross-Dataset (RM1)
> …model spasial mengalami degradasi yang nyata, dengan AUC turun dari [PERBAIKAN]0,78–0,97[/PERBAIKAN] pada in-dataset menjadi [PERBAIKAN]0,61–0,68[/PERBAIKAN] pada cross-dataset. Degradasi paling parah terjadi pada arah CDF→FFPP, dengan generalization drop F1 mencapai [PERBAIKAN]0,769[/PERBAIKAN] dan recall runtuh menjadi [PERBAIKAN]0,074[/PERBAIKAN].

## 4.2.3 Pengaruh FFT (RM2)
> …pada arah FFPP→CDF … model hybrid mencatat generalization drop F1 sebesar [PERBAIKAN]+0,012[/PERBAIKAN], jauh lebih kecil dibanding model spasial ([PERBAIKAN]+0,091[/PERBAIKAN]), bahkan F1 cross-dataset hybrid ([PERBAIKAN]0,594[/PERBAIKAN]) sedikit di bawah spasial ([PERBAIKAN]0,614[/PERBAIKAN]) namun dengan kestabilan yang lebih baik. Pada tier [PERBAIKAN]250[/PERBAIKAN] dan [PERBAIKAN]500[/PERBAIKAN] yang dilaporkan pada analisis pendukung, F1 cross-dataset model hybrid bahkan melampaui model spasial pada arah ini.

> (verifikasi: n250 hybrid F1 0,621 > spasial 0,518; n500 hybrid 0,552 > spasial 0,490; n750 hybrid 0,594 < spasial 0,614 — jadi "250 dan 500" benar.)

> …Pada arah CDF→FFPP, model hybrid tetap mengalami keruntuhan (recall [PERBAIKAN]0,142[/PERBAIKAN], F1 [PERBAIKAN]0,238[/PERBAIKAN]), dan dari sisi AUC cross-dataset, model hybrid tidak secara meyakinkan mengungguli model spasial (misalnya pada arah FFPP→CDF keduanya berdekatan, [PERBAIKAN]spasial 0,678 dan hybrid 0,665[/PERBAIKAN], sedangkan pada CDF→FFPP spasial [PERBAIKAN]0,607[/PERBAIKAN] lebih tinggi dari hybrid [PERBAIKAN]0,555[/PERBAIKAN]).

> ⚠️ **Perubahan kata:** dulu "keduanya **setara di** [nilai]" (run lama 0,648 = 0,648). Sekarang **tidak persis sama** (0,678 vs 0,665) → saya ganti jadi "**berdekatan**, spasial 0,678 dan hybrid 0,665".

## 4.2.5 Keterbatasan
> …Ketiga, hasil pada tier [PERBAIKAN]n = 100[/PERBAIKAN] bersifat noisy akibat ukuran set pengujian yang sangat kecil…

---

# BAGIAN 2 — ABSTRAK (WAJIB diubah)

## Abstrak (Indonesia)
> …Hasil menunjukkan model spasial konsisten paling unggul (AUC in-dataset hingga [PERBAIKAN]0,97[/PERBAIKAN]), sedangkan cabang frekuensi berperforma nyaris setara tebakan acak (AUC [PERBAIKAN]0,56–0,61[/PERBAIKAN]) sehingga model hybrid tidak mengungguli baseline spasial. Pada pengujian cross-dataset, performa seluruh model menurun (AUC sekitar [PERBAIKAN]0,56–0,68[/PERBAIKAN]) disertai keruntuhan recall, dan penambahan analisis frekuensi hanya menekan penurunan generalisasi secara parsial dan bergantung arah. …

Perubahan: freq `0,55–0,59 → 0,56–0,61`; cross `0,63–0,65 → 0,56–0,68`. (`0,97` tetap.)

## Abstract (English)
> …The results show that the spatial model is consistently the best (in-dataset AUC up to [PERBAIKAN]0.97[/PERBAIKAN]), whereas the frequency branch performs near chance (AUC [PERBAIKAN]0.56–0.61[/PERBAIKAN]), so the hybrid model does not outperform the spatial baseline. Under cross-dataset testing, all models degrade (AUC around [PERBAIKAN]0.56–0.68[/PERBAIKAN]) with a collapse in recall, … 

Perubahan: `0.55–0.59 → 0.56–0.61`; `0.63–0.65 → 0.56–0.68`. (titik desimal, bukan koma.)

---

# BAGIAN 3 — BAB V KESIMPULAN (WAJIB diisi)

**Kesimpulan poin 1 (RM1):**
> …Nilai AUC yang tinggi pada evaluasi in-dataset ([PERBAIKAN]0,778[/PERBAIKAN] pada FaceForensics++ dan [PERBAIKAN]0,971[/PERBAIKAN] pada Celeb-DF) turun menjadi sekitar [PERBAIKAN]0,61–0,68[/PERBAIKAN] pada evaluasi cross-dataset, disertai keruntuhan recall yang paling parah pada arah CDF→FFPP ([PERBAIKAN]0,074[/PERBAIKAN]), dengan generalization drop F1 mencapai [PERBAIKAN]0,769[/PERBAIKAN]. …

**Kesimpulan poin 2 (RM2):**
> …Pada arah FFPP→CDF, model hybrid berhasil menahan degradasi dengan generalization drop yang jauh lebih kecil ([PERBAIKAN]+0,012[/PERBAIKAN]) dibanding model spasial ([PERBAIKAN]+0,091[/PERBAIKAN]); namun keuntungan ini tidak konsisten… 

**Kesimpulan poin 3 (RM3):**
> …cabang frekuensi berperforma nyaris setara tebakan acak (AUC [PERBAIKAN]0,56–0,61[/PERBAIKAN]) sehingga cenderung menjadi sumber noise dalam fusi. …

---

# §FLAGS — perlu perhatian (bukan sekadar isi angka)

1. **Rujukan nomor gambar di narasi tidak sinkron** (akibat skema final 10 gambar):
   - 4.1.4 pengantar: "Gambar **4.4** Perbandingan performa cross-dataset" → **4.5**.
   - 4.1.5 pengantar: "divisualisasikan pada Gambar **4.5**" → **4.7**.
   - 4.1.6 pengantar: "divisualisasikan pada Gambar **4.6**" → **4.8**.
   - (4.1.3 "Gambar 4.4" untuk ROC sudah benar; 4.1.4 "Gambar 4.6" ROC benar; 4.9/4.10 benar.)
2. **Caption masih ada `()` kosong** → isi `(n = 750)`: Gambar 4.3, Gambar 4.5 (cross bar), Gambar 4.7. (DAFTAR GAMBAR juga masih `()` — akan beres saat Update Field.)
3. **Reword (sudah disiapkan di atas):** 4.1.5(b) "kecil hingga negatif" → "bervariasi…"; 4.2.3 "setara di" → "berdekatan".
4. Setelah semua: **DAFTAR GAMBAR/TABEL** masih daftar 4.1–4.6 → harus jadi 4.1–4.10; lakukan **Ctrl+A → F9**.

---

## Verifikasi
Semua angka dihitung ulang dari `outputs/tables/n{250,500,750}/Table*_summary.csv` (3-seed run baru), dicocokkan dengan Tabel 4.2–4.6 HTML yang sudah diperbarui. Tidak ada konflik.
