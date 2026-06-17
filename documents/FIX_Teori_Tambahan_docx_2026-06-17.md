# FIX — Perbaikan Kalimat Teori Tambahan di docx (pasca-tempel)

> **Konteks:** §A–§G `REVISI_BAB_II_IV_V_Teori_Tambahan_2026-06-17.md` sudah masuk docx (cek 15:45). Pengecekan mendalam: penempatan & sitasi **100% benar** ([24]–[30], [39], [46] semua tepat; 48 entri), simbol math §A benar. Tersisa **4 perbaikan kalimat kecil** akibat edit manual.
>
> **Gaya:** hindari tanda pisah `—` dan titik-koma `;`. Sambung dengan kalimat terpisah atau konjungsi.
> **Status draft:** REVISI sudah dirapikan ke gaya ini, jadi alternatifnya cukup **re-paste** subbab terkait dari draft.
>
> **Cakupan tambahan:** dokumen ini juga memuat **penambahan HIPOTESIS** (kritik penguji #3, lihat bagian 🧪 di bawah) yang belum ada di docx.

---

## ✅ Daftar perbaikan (4)

### 1. §C — kalimat rusak (subjek "evaluasi" tidak bisa "melatih model")
**Lokasi:** BAB II, subbab *Cross Dataset Generalization*, paragraf setelah daftar Domain Adaptation/Generalization.

**SEBELUM:**
> Dalam kerangka ini, evaluasi *cross-dataset* pada penelitian ini **melatih model pada satu dataset dan diuji** pada dataset lain tanpa menyertakan data uji saat pelatihan, termasuk skenario *domain generalization*, bukan *domain adaptation*.

**SESUDAH:**
> Dalam kerangka ini, evaluasi *cross-dataset* pada penelitian ini termasuk skenario *domain generalization*, bukan *domain adaptation*, karena model dilatih pada satu dataset lalu diuji pada dataset lain tanpa menyertakan data uji selama pelatihan.

---

### 2. §E — koma sambung / run-on
**Lokasi:** BAB IV, subbab *Penurunan Performa Model Spasial pada Cross-Dataset* (4.2.2), kalimat ber-sitasi [46].

**SEBELUM:**
> …sesuai batas galat pada domain target [46]**,** karena penelitian ini tidak menyertakan data dataset target saat pelatihan**,** skenario yang diuji termasuk *domain generalization* dan bukan *domain adaptation*.

**SESUDAH:**
> …sesuai batas galat pada domain target [46]**.** Penelitian ini tidak menyertakan data dataset target saat pelatihan sehingga skenario yang diuji termasuk *domain generalization*, bukan *domain adaptation*.

---

### 3. §A — "Oppenheim et al." → "Oppenheim dan Lim" (paper 2 penulis)
**Lokasi:** BAB II, subbab *Spektrum Magnitudo dan Fase*, paragraf ke-2.

**SEBELUM:** "**Oppenheim et al.** [25] memperlihatkan bahwa citra yang direkonstruksi…"
**SESUDAH:** "**Oppenheim dan Lim** [25] memperlihatkan bahwa citra yang direkonstruksi…"

> Alasan: referensi [25] hanya 2 penulis (Oppenheim & Lim), jadi "et al." kurang tepat.

---

### 4. §B (bonus) — titik-koma → titik
**Lokasi:** BAB II, subbab *Bias Frekuensi dan Tekstur pada CNN*, paragraf ke-2.

**SEBELUM:**
> …harus mempelajari selektivitas frekuensi yang diskriminatif tanpa dukungan bias arsitektural yang memadai**;** ketika sinyal artefak lemah atau terdistorsi, jaringan semacam ini rentan gagal menemukan pola yang berguna.

**SESUDAH:**
> …harus mempelajari selektivitas frekuensi yang diskriminatif tanpa dukungan bias arsitektural yang memadai**. Ketika** sinyal artefak lemah atau terdistorsi, jaringan semacam ini rentan gagal menemukan pola yang berguna.

---

## 🔸 Opsional (boleh dilewati) — dijabarkan

### Opsional 1 — §C: HAPUS 1 kalimat redundan
**Lokasi:** BAB II, subbab *Cross Dataset Generalization*, paragraf yang dimulai "Dalam kerangka ini, evaluasi *cross-dataset*…".

**Yang dihapus** (kalimat ke-2 paragraf tersebut):
> ~~Penambahan cabang frekuensi diharapkan menghasilkan representasi yang lebih invarian terhadap domain, sejalan dengan laporan bahwa fitur frekuensi cenderung lebih *generalizable* lintas dataset [12] dan upaya menemukan artefak yang lebih umum [39].~~

**Kenapa:** kalimat ini mengulang isi paragraf **tepat sesudahnya** (P7: "Penelitian-penelitian modern menunjukkan bahwa pendekatan berbasis domain frekuensi cenderung memiliki kemampuan generalisasi lebih baik… Durall… Qian… Hasanaath…").
**Aman:** [12] dipakai **13×** dan [39] **4×** di tempat lain, jadi **tidak ada sitasi yang yatim**. Tidak perlu Update Fields.

**Hasil §C setelah Fix 1 + hapus ini (2 kalimat, padat):**
> Dalam kerangka ini, evaluasi *cross-dataset* pada penelitian ini termasuk skenario *domain generalization*, bukan *domain adaptation*, karena model dilatih pada satu dataset lalu diuji pada dataset lain tanpa menyertakan data uji selama pelatihan. Teknik adaptasi domain eksplisit berada di luar lingkup penelitian ini dan menjadi salah satu arah pengembangan.

### Opsional 2 — §G: PINDAH butir (bukan hapus)
**Lokasi:** BAB V, subbab *Saran*. **Tidak ada yang dihapus**, hanya urutan dipindah.

Urutan sekarang → setelah dipindah:
| # | Sekarang | Setelah dipindah |
|---|---|---|
| 1 | Memperkuat cabang frekuensi | Memperkuat cabang frekuensi |
| 2 | Memperbaiki mekanisme fusi | Memperbaiki mekanisme fusi |
| 3 | Mengeksplorasi domain transformasi alternatif | Mengeksplorasi domain transformasi alternatif |
| 4 | Memperluas skala dan dimensi temporal | Memperluas skala dan dimensi temporal |
| 5 | Implikasi praktis | **Menerapkan adaptasi domain eksplisit** |
| 6 | **Menerapkan adaptasi domain eksplisit** | Implikasi praktis *(penutup)* |

**Aksi:** potong blok **"Menerapkan adaptasi domain eksplisit"** (judul + 1 paragraf) dari posisi terakhir, tempel **sebelum** "Implikasi praktis" agar implikasi praktis tetap jadi butir penutup.

---

---

## 🎯 COMPARING bukan IMPROVING — perbaikan framing BAB I & II (kritik penguji #2 & #3)

> **Inti:** narasi penelitian = **studi komparatif kontribusi domain frekuensi**, BUKAN "metode peningkatan". Beberapa kalimat di BAB I (latar belakang) dan BAB II masih berbunyi seolah hybrid **pasti lebih baik** atau studi ini **dioptimalkan untuk meningkatkan** — ini **kontradiktif** dengan hasil negatif.
> **Sudah benar (JANGAN diubah):** Abstrak, Rumusan Masalah, Tujuan, dan seluruh kesimpulan BAB IV/V sudah komparatif/jujur.
> Gaya: tanpa `—` dan `;`.

### C-1. BAB I (Latar Belakang) — "dioptimalkan untuk generalisasi"
**SEBELUM:**
> Penelitian ini mengisi celah tersebut dengan **mengusulkan** arsitektur hybrid XceptionNet dan FFT dengan late fusion dan Squeeze-and-Excitation gating **yang dioptimalkan untuk generalisasi lintas dataset**.

**SESUDAH:**
> Penelitian ini mengisi celah tersebut dengan **membangun** arsitektur hybrid XceptionNet dan FFT dengan late fusion dan Squeeze-and-Excitation gating **yang dirancang untuk mengevaluasi kontribusi domain frekuensi terhadap generalisasi lintas dataset**.

### C-2. BAB I (Ruang Lingkup) — "validasi efektivitas … untuk meningkatkan"
**SEBELUM:**
> Dengan batasan ini, penelitian diarahkan untuk menjaga fokus pada **validasi efektivitas** integrasi antara FDA ke dalam arsitektur XceptionNet **untuk meningkatkan** kemampuan generalisasi serta ketahanan, dan akurasi dalam mendeteksi deepfake.

**SESUDAH:**
> Dengan batasan ini, penelitian diarahkan untuk menjaga fokus pada **evaluasi kontribusi** integrasi FDA ke dalam arsitektur XceptionNet **terhadap** kemampuan generalisasi, ketahanan, dan akurasi dalam mendeteksi deepfake.

### C-3. BAB II — "hybrid secara konsisten menghasilkan performa lebih baik" (kontradiksi utama)
**SEBELUM** (kalimat pertama dan terakhir paragraf SpecXNet/FSBI/Luo):
> **Beberapa penelitian terkini yang mengadopsi pendekatan hybrid menunjukkan peningkatan performa yang signifikan.** … **Penelitian-penelitian ini menunjukkan bahwa pendekatan hybrid secara konsisten menghasilkan performa yang lebih baik dibanding model berbasis domain tunggal, terutama dalam skenario cross-dataset.**

**SESUDAH** (ubah kalimat pertama + terakhir, tengahnya tetap):
> **Beberapa penelitian terkini yang mengadopsi pendekatan hybrid melaporkan peningkatan performa.** … **Namun, peningkatan tersebut tidak selalu konsisten karena efektivitas pendekatan hybrid masih bergantung pada representasi frekuensi, strategi fusi, dan karakteristik dataset.**

### C-4. BAB II (Cross Dataset Generalization) — "memiliki performa generalisasi lebih baik dibanding domain tunggal"
**SEBELUM:**
> Penelitian seperti SpecXNet [13] dan FSBI [16] **menunjukkan** bahwa model hybrid yang menggabungkan domain spasial dan domain frekuensi **memiliki performa generalisasi lebih baik dibanding model berbasis domain tunggal**.

**SESUDAH:**
> Penelitian seperti SpecXNet [13] dan FSBI [16] **melaporkan** bahwa model hybrid yang menggabungkan domain spasial dan domain frekuensi **dapat memiliki performa generalisasi lebih baik dibanding model berbasis domain tunggal, meskipun manfaat tersebut bergantung pada representasi frekuensi dan strategi fusi yang digunakan**.

### C-5 (opsional) BAB I — "berhasil membuktikan … untuk meningkatkan robustness"
**SEBELUM:**
> Studi-studi ini **berhasil membuktikan** bahwa fusi dua domain bermanfaat, tetapi sebagian besar masih dioptimalkan untuk performa in-domain pada FaceForensics++, dan belum mengevaluasi secara sistematis fusi late dan gating **sebagai mekanisme spesifik untuk meningkatkan robustness** lintas dataset.

**SESUDAH:**
> Studi-studi ini **melaporkan** bahwa fusi dua domain bermanfaat, tetapi sebagian besar masih dioptimalkan untuk performa in-domain pada FaceForensics++, dan belum mengevaluasi secara sistematis **kontribusi** fusi late dan gating **terhadap robustness** lintas dataset.

### C-6 (opsional) BAB II — "untuk meningkatkan kemampuan generalisasi"
**SEBELUM:** "…dapat digabungkan dengan analisis frekuensi **untuk meningkatkan** kemampuan generalisasi."
**SESUDAH:** "…dapat digabungkan dengan analisis frekuensi **dengan tujuan meningkatkan** kemampuan generalisasi."

> **Catatan:** C-1 sampai C-4 wajib (kontradiktif). C-5/C-6 opsional (penghalusan). Tidak perlu Update Fields (tanpa perubahan sitasi/penomoran).

---

## 📚 REKONSILIASI DENGAN LITERATUR — jawaban "kenapa hasil berbeda dari penelitian terdahulu"

> **Pertanyaan penguji:** BAB II berkali-kali menyebut domain frekuensi lebih baik untuk generalisasi, tapi hasil kalian menunjukkan domain frekuensi nyaris tidak membantu. Mengapa bertentangan dengan penelitian terdahulu?
>
> **Strategi jawaban (inti):** Ini **bukan kontradiksi, melainkan kondisi batas**. Literatur membuktikan artefak frekuensi **ada** (Durall, Zhang); penelitian ini tidak menyangkalnya. Yang ditunjukkan adalah **kemampuan mengeksploitasi** artefak itu **kondisional** terhadap praproses, representasi, fusi, dan jenis pergeseran domain. Bingkai hasil sebagai **pelengkap** literatur (menandai batas kondisi), bukan pembantah. Ini menaikkan nilai karena hasil negatif yang terjelaskan lebih bernilai daripada klaim sukses tanpa syarat.

**Letak (docx):** BAB IV → Pembahasan → **tambah Heading3 baru** setelah *"Analisis Akar Penyebab Lemahnya Cabang Frekuensi"* dan sebelum *"Keterbatasan Penelitian"*. Tanpa referensi baru (pakai sitasi yang sudah ada). Gaya tanpa `—`/`;`.

**「TAMBAH (Heading3 + isi)」**

**Posisi Temuan terhadap Penelitian Terdahulu**

Hasil bahwa domain frekuensi nyaris tidak membantu sekilas tampak bertentangan dengan banyak penelitian terdahulu yang melaporkan manfaat fitur frekuensi untuk deteksi deepfake. Namun, pertentangan ini bersifat semu. Durall et al. [8] dan Zhang et al. [9] menegaskan bahwa artefak spektral memang muncul pada citra sintetis, dan temuan penelitian ini tidak menyangkal keberadaannya. Yang ditunjukkan penelitian ini adalah bahwa kemampuan sebuah model untuk mengeksploitasi artefak tersebut bersifat kondisional, bergantung pada bagaimana sinyal frekuensi dipertahankan, direpresentasikan, dan difusikan.

Terdapat sejumlah perbedaan metodologis yang menjelaskan perbedaan hasil. Pertama, dari sisi praproses, cropping wajah dengan MTCNN dan kompresi c23 pada penelitian ini menekan konteks tepi dan komponen frekuensi tinggi tempat artefak generatif termanifestasi, suatu kerentanan yang juga dicatat oleh Mejri et al. [31]. Kedua, dari sisi representasi, metode seperti Thinking in Frequency [11] dan SpecXNet [13] menggunakan representasi frekuensi yang lebih kaya, misalnya dekomposisi frequency-aware atau filter yang dapat dilatih, sedangkan penelitian ini hanya memakai satu peta magnitudo FFT tanpa informasi fase. Ketiga, dari sisi fusi, penelitian terdahulu kerap memakai mekanisme atensi dua-domain yang khusus, sedangkan penelitian ini memakai konkatenasi dengan SE gating yang lebih sederhana. Keempat, dari sisi skenario, penelitian ini menguji generalisasi cross-dataset antara FaceForensics++ dan Celeb-DF yang melibatkan perbedaan generator sekaligus kondisi perekaman, yaitu pergeseran domain yang umumnya lebih berat dibanding evaluasi cross-manipulation dalam satu dataset. Dengan demikian, temuan penelitian ini melengkapi literatur dengan menandai batas kondisi ketika kontribusi domain frekuensi menjadi terbatas.

**「/TAMBAH」**

> **Sitasi:** semua sudah ada (Durall [8], Zhang [9], Qian [11], Alam/SpecXNet [13], Mejri [31]). Tidak ada referensi baru. **Update Fields** hanya untuk Daftar Isi (karena ada Heading3 baru).

### Sinkron dengan bagian lain (penting)
- Subbab ini = **payoff** dari penghalusan BAB II (C-3/C-4). Setelah BAB II diubah jadi "frekuensi **dapat** membantu, bergantung representasi/fusi/dataset", subbab ini menutup lingkaran: "pada konfigurasi kami, syarat itu tidak terpenuhi".
- Ia juga memperkuat 4.2.4 (akar penyebab internal: fase dibuang, bias CNN) dengan **sudut eksternal** (perbedaan dari penelitian terdahulu).

### Untuk sidang (jawaban lisan ringkas)
> "Kami tidak membantah bahwa artefak frekuensi ada. Kami menunjukkan bahwa memanfaatkannya bersifat kondisional. Penelitian yang sukses umumnya memakai representasi frekuensi yang lebih kaya, fusi beratensi, dan praproses yang mempertahankan frekuensi tinggi, serta menguji cross-manipulation. Konfigurasi kami sengaja lebih sederhana dan reproducible, dengan cropping dan kompresi c23 yang menekan artefak, magnitudo saja tanpa fase, dan pengujian cross-dataset yang lebih berat. Jadi hasil kami menandai batas kondisi, bukan membantah prinsipnya."

---

## 🧪 HIPOTESIS — penambahan (kritik penguji #3: "tidak ada hipotesis eksplisit")

> **Status:** belum ada di docx (dikonfirmasi: tidak ada heading "Hipotesis"). Asal: `PLAN_Revisi_Penguji_BAB_II_Hipotesis_Evaluasi_2026-06-17.md` §4. Bersinggungan langsung dengan §C/§E (framing *domain generalization*), jadi sebaiknya dipasang bersamaan.
> **Framing:** hipotesis dirumuskan sebagai yang **diuji**, lalu dilaporkan **jujur** (hasil negatif → H₀ tidak ditolak). Karena hanya 3 *seed*, perbandingan dibahas **deskriptif**, tanpa klaim "signifikan secara statistik".

### H-1. BAB I — TAMBAH subbab baru "Hipotesis Penelitian"
**Lokasi:** BAB I, **setelah subbab *Tujuan*** (sebelum *Manfaat*). Buat Heading2 baru.

**「TAMBAH (Heading2 + isi)」**

**Hipotesis Penelitian**

Berdasarkan rumusan masalah dan tujuan penelitian, dirumuskan hipotesis yang diuji secara empiris sebagai berikut.

- **H₁ (hipotesis alternatif):** Penambahan analisis domain frekuensi melalui arsitektur *hybrid* XceptionNet–FFT menghasilkan kemampuan generalisasi *cross-dataset* yang lebih baik dibandingkan model domain spasial murni (XceptionNet).
- **H₀ (hipotesis nol):** Tidak terdapat peningkatan generalisasi *cross-dataset* yang berarti dari penambahan analisis domain frekuensi, sehingga performa *hybrid* tidak melampaui model spasial.

Hipotesis ini diuji melalui perbandingan *generalization drop* dan metrik *cross-dataset* antara model *hybrid* dan model spasial yang disajikan pada BAB IV.

**「/TAMBAH」**

> Catatan: ini membuat hipotesis **tidak yatim** karena langsung dijawab di BAB IV (H-2) dan BAB V (H-3).

### H-2. BAB IV — payoff di "Ringkasan Jawaban atas Rumusan Masalah" (subbab terakhir)
**Lokasi:** paragraf penutup yang berbunyi "Secara keseluruhan, penelitian ini menyimpulkan bahwa… hanya bersifat parsial serta bergantung arah. Temuan negatif ini…".

**「SISIPKAN setelah '…hanya bersifat parsial serta bergantung arah.' dan sebelum 'Temuan negatif ini…'」**

Dengan demikian, hipotesis nol (H₀) tidak dapat ditolak, karena penambahan analisis domain frekuensi belum terbukti meningkatkan generalisasi *cross-dataset* secara konsisten. Selisih antar-model relatif kecil dan dibahas secara deskriptif tanpa uji signifikansi formal mengingat jumlah *seed* yang terbatas.

**「/SISIPKAN」**

### H-3. BAB V — payoff di Kesimpulan
**Lokasi:** paragraf penutup Kesimpulan yang berbunyi "Secara keseluruhan, dapat disimpulkan bahwa… generalisasi lintas dataset tetap menjadi tantangan terbuka. Temuan negatif ini…".

**「SISIPKAN setelah '…tetap menjadi tantangan terbuka.' dan sebelum 'Temuan negatif ini…'」**

Mengacu pada hipotesis penelitian, hasil ini berarti hipotesis nol (H₀) tidak dapat ditolak dan hipotesis alternatif (H₁) belum didukung bukti yang konsisten.

**「/SISIPKAN」**

> **Perlu Update Fields?** Tidak untuk H-2/H-3 (tanpa sitasi/penomoran baru). Untuk H-1, subbab baru menggeser penomoran subbab BAB I, jadi **Update Fields** (Ctrl+A → F9) agar Daftar Isi ikut menyesuaikan.

---

## Catatan
- Tidak ada masalah sitasi/penempatan/simbol pada teori tambahan. Hanya 4 perbaikan kalimat di atas.
- Setelah memperbaiki 4 kalimat, **tidak perlu Update Fields** kecuali Anda memindah butir §G atau menambah subbab Hipotesis (H-1).
- **Caveat akademik (penting):** karena hanya 3 *seed* (rata-rata ± simpangan baku), jangan klaim "signifikan secara statistik" tanpa uji formal. Pembahasan H₀/H₁ bersifat deskriptif.
</content>
