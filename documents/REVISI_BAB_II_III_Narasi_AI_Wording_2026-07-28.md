# REVISI BAB II & III — Re-narasi Wording "AI-like"

**Tanggal:** 2026-07-28 (diterapkan ke .docx 2026-07-29)
**Sumber catatan:** Penguji (Mustika) — "Bab 2, 3: Bagian-bagian AI perlu dinarasikan kembali."

> **STATUS PENERAPAN (2026-07-29):** 25 dari 30 edit sudah diterapkan langsung ke Word live (`.docx` OneDrive) secara text-only. Backup: `..._BACKUP_2026-07-29.docx`. **5 edit BELUM diterapkan** karena formatting sumbernya berantakan (italic satu frasa penuh / spasi non-breaking nyasar) atau menghapus kata yang ter-italic, sehingga auto-edit akan menyentuh formatting: **p476, p571, p802, p1038, p1058** — terapkan manual dari before/after di bawah. Catatan: p383 & p582 sedikit diubah dari draf awal agar urutan istilah ter-italic tetap (versi terpasang di bawah).
**Interpretasi (dikonfirmasi user):** banyak kalimat masih terbaca seperti tulisan hasil AI (translation-ese, kalimat perekat motivasional, kata sifat berlebihan). Contoh seed dari user: *"Di luar laboratorium…"* (ada di BAB I para 383).

---

## Pola "AI-like" yang disasar

1. **Pembuka klise / stock opener:** "Di luar laboratorium…", "Di era media generatif", "Seiring berkembangnya/meningkatnya…", "Dewasa ini".
2. **Kalimat perekat & wrap-up:** "Secara keseluruhan,", "Dengan demikian,", "Temuan ini menunjukkan/sejalan", "memperkuat pentingnya", "Konvergensi … menunjukkan".
3. **Kata sifat hype/kabur:** "sangat krusial", "ciri esensial", "presisi, tangguh, dan responsif", "menyoroti … dengan baik".
4. **Triad kosong / paralelisme paksa:** rangkaian tiga kata sifat yang tidak menambah informasi.

## Catatan penting — JANGAN sapu semua

Scan penanda otomatis menandai 67 paragraf di BAB II dan 6 di BAB III, tetapi banyak yang **false positive**. Kata seperti **"konvergensi"** dalam konteks pelatihan model (optimizer, learning rate) adalah istilah teknis yang benar dan **tidak boleh diubah**. Yang diperbaiki hanya paragraf naratif/motivasional yang benar-benar terbaca AI. Contoh yang **DIBIARKAN** (bukan AI-like, teknis benar): p693, p918, p974, p1407, p1443.

---

## Rewrite (before → after)

### BAB I — para 383 (seed "Di luar laboratorium")

**LAMA:**
> Di luar laboratorium, detektor deepfake harus menghadapi distribusi data yang sangat berbeda dari data pelatihan, seperti generator baru yang bermunculan setiap tahun, kompresi platform sosial bervariasi, dan teknik pasca-pemrosesan adversarial dipakai untuk menyamarkan jejak. Studi sistematis melaporkan penurunan Area Under the Curve (AUC) 10 hingga 20 poin ketika detektor berbasis CNN spasial dipindahkan dari satu dataset ke dataset lain [14, 15]. Karena itu, kemampuan generalisasi lintas dataset, bukan akurasi in-dataset, adalah metrik yang paling relevan untuk menilai kelayakan deteksi deepfake di dunia nyata, dan menjadi fokus utama penelitian ini.

**BARU (versi terpasang di .docx):**
> Pada penerapan nyata, detektor deepfake menghadapi distribusi data yang berbeda dari data pelatihan, seperti generator baru yang bermunculan setiap tahun, tingkat kompresi platform sosial yang bervariasi, dan teknik pasca-pemrosesan adversarial yang dipakai untuk menyamarkan jejak. Studi sistematis melaporkan penurunan Area Under the Curve (AUC) sebesar 10 hingga 20 poin ketika detektor berbasis CNN spasial dipindahkan dari satu dataset ke dataset lain [14, 15]. Karena itu, kemampuan generalisasi lintas dataset, bukan akurasi in-dataset, menjadi metrik yang paling relevan untuk menilai kelayakan deteksi deepfake pada kondisi nyata, sekaligus menjadi fokus utama penelitian ini.

### BAB II — para 438

**LAMA:**
> Seiring berkembangnya teknologi generatif seperti GAN, deepfake semakin sulit dibedakan dari konten asli. Kualitas manipulasi yang semakin sempurna membuat konten palsu nyaris tidak dapat dideteksi baik oleh pengamat manusia, maupun oleh sistem pendeteksi konvensional yang berbasis fitur spasial [14]. Oleh karena itu, kemampuan untuk mendeteksi dan memverifikasi keaslian konten digital menjadi sangat krusial dalam menjaga integritas informasi serta melindungi keamanan dan kepercayaan publik di era media generatif.

**BARU:**
> Perkembangan teknologi generatif seperti GAN membuat deepfake semakin sulit dibedakan dari konten asli. Peningkatan kualitas manipulasi menyebabkan konten palsu sulit dikenali, baik oleh pengamat manusia maupun oleh sistem pendeteksi konvensional yang hanya mengandalkan fitur spasial [14]. Kondisi ini menjadikan kemampuan mendeteksi dan memverifikasi keaslian konten digital sebagai kebutuhan penting untuk menjaga keandalan informasi.

### BAB II — para 476

**LAMA:**
> Secara keseluruhan, berbagai studi tersebut mengindikasikan bahwa informasi dalam domain frekuensi dapat berfungsi sebagai pelengkap penting bagi pendekatan berbasis spasial, karena mampu menangkap karakteristik yang tidak terlihat secara langsung dalam ruang gambar. Kehadiran artefak spektral yang konsisten di berbagai jenis konten deepfake menjadikan pendekatan berbasis FDA lebih andal dalam menghadapi variasi model generatif maupun perbedaan distribusi data (baik lintas model GAN maupun antar dataset). Oleh karena itu, semakin banyak penelitian terkini yang menggabungkan analisis spasial dan frekuensi dalam satu kerangka kerja deep learning, untuk membangun sistem pendeteksi deepfake yang lebih presisi, tangguh, dan responsif terhadap teknik manipulasi yang terus berkembang.

**BARU:**
> Berbagai studi tersebut mengindikasikan bahwa informasi domain frekuensi dapat melengkapi pendekatan berbasis spasial karena mampu menangkap karakteristik yang tidak tampak langsung pada ruang gambar. Artefak spektral yang konsisten pada beragam jenis deepfake membuat pendekatan Frequency Domain Analysis (FDA) lebih andal terhadap variasi model generatif maupun perbedaan distribusi antardataset. Hal ini mendorong berkembangnya penelitian yang menggabungkan analisis spasial dan frekuensi dalam satu kerangka deep learning untuk menghasilkan detektor yang lebih akurat dan tahan terhadap teknik manipulasi baru.

### BAB II — para 571

**LAMA:**
> Deepfake video tidak hanya mengandung anomali frekuensi antar piksel, tetapi juga antar frame. Kim et al. [33] menemukan bahwa manipulasi wajah menyebabkan inconsistency temporal frequency. Temuan ini sejalan dengan penelitian sebelumnya oleh Nguyen et al. dan Güera dan Delp., yang menjelaskan bahwa video deepfake cenderung memiliki pola frekuensi temporal yang tidak stabil selama pergerakan wajah [34, 35].

**BARU:**
> Anomali frekuensi pada video deepfake tidak hanya terjadi antarpiksel dalam satu frame, tetapi juga antarframe. Kim et al. [33] menemukan bahwa manipulasi wajah menimbulkan inkonsistensi frekuensi temporal. Hasil ini sejalan dengan Nguyen et al. serta Güera dan Delp yang melaporkan bahwa video deepfake cenderung memiliki pola frekuensi temporal yang tidak stabil selama pergerakan wajah [34, 35].

*(Perbaikan sekaligus: istilah campur "inconsistency temporal frequency" → "inkonsistensi frekuensi temporal"; titik nyasar "Delp." → "Delp".)*

### BAB II — para 582

**LAMA:**
> Seiring meningkatnya video deepfake, distorsi spektral temporal menjadi ciri esensial yang sulit dihilangkan oleh model generatif. Pendekatan oleh Kim et al. dan Guera et al. memperkuat pentingnya analisis frekuensi dalam dimensi waktu [33, 35].

**BARU (versi terpasang di .docx):**
> Pada video deepfake, distorsi spektral temporal merupakan ciri yang sulit dihilangkan oleh model generatif. Penelitian Kim et al. dan Guera et al. menunjukkan bahwa analisis frekuensi pada dimensi waktu efektif untuk mengungkap ciri tersebut [33, 35].

### BAB II — para 668

**LAMA:**
> Artefak deepfake biasanya muncul pada area transisi wajah, seperti sekitar mata, hidung, dan garis rahang. Depthwise convolution menyoroti detail lokal ini dengan baik.

**BARU:**
> Artefak deepfake umumnya muncul pada area transisi wajah seperti sekitar mata, hidung, dan garis rahang. Depthwise convolution memproses setiap kanal secara terpisah sehingga sesuai untuk menangkap detail lokal pada area tersebut.

*(Ganti "menyoroti … dengan baik" yang kabur dengan alasan teknis yang benar.)*

---

### BAB II — para 802

**LAMA:**
> Fitur spasial dan frekuensi kemudian digabungkan pada tahap late fusion di tingkat fitur sehingga model mampu mendeteksi manipulasi baik visual maupun statistik spektral. Dengan demikian, FFPP menjadi backbone penting dalam evaluasi performa sistem hybrid pada penelitian ini.

**BARU:**
> Fitur spasial dan frekuensi kemudian digabungkan pada tahap late fusion di tingkat fitur sehingga model mampu mendeteksi manipulasi baik secara visual maupun secara statistik spektral. FFPP menjadi dataset utama untuk mengevaluasi performa sistem hybrid pada penelitian ini.

*(Buang metafora "backbone penting" untuk sebuah dataset dan wrap-up "Dengan demikian".)*

### BAB II — para 817

**LAMA:**
> …Oleh karena itu, kemampuan model untuk memanfaatkan informasi domain frekuensi menjadi sangat krusial ketika diuji pada dataset ini, karena artefak frekuensi yang bersifat algoritmik cenderung lebih stabil meskipun kualitas visual manipulasi meningkat [8].

**BARU:**
> …Karena itu, kemampuan model memanfaatkan informasi domain frekuensi menjadi sangat menentukan ketika diuji pada dataset ini, sebab artefak frekuensi yang bersifat algoritmik cenderung lebih stabil meskipun kualitas visual manipulasi meningkat [8].

### BAB II — para 822

**LAMA:**
> …Distribusi frekuensi yang berbeda secara signifikan dari citra asli menjadi dasar metode deteksi domain frekuensi [9]. Dengan demikian, kombinasi analisis spasial dan frekuensi memberikan pendekatan yang lebih komprehensif dalam mendeteksi manipulasi visual pada citra deepfake.

**BARU:**
> …Distribusi frekuensi yang jauh berbeda dari citra asli menjadi dasar metode deteksi domain frekuensi [9]. Oleh sebab itu, kombinasi analisis spasial dan frekuensi memberikan pendekatan yang lebih menyeluruh dalam mendeteksi manipulasi pada citra deepfake.

### BAB II — para 940

**LAMA:**
> Evaluasi kinerja model merupakan tahap krusial dalam pengembangan sistem deteksi deepfake. Melalui proses evaluasi, peneliti dapat menilai sejauh mana model mampu membedakan citra asli dan citra hasil manipulasi, serta mengidentifikasi kelemahan model ketika dihadapkan pada variasi distribusi data atau skenario cross-dataset. Hal ini penting karena model generatif modern seperti GAN dan variannya terus menghasilkan konten dengan kualitas semakin realistis sehingga semakin sulit dibedakan secara visual [8, 9, 14].

**BARU:**
> Evaluasi kinerja model merupakan tahap penting dalam pengembangan sistem deteksi deepfake. Melalui evaluasi, peneliti dapat menilai sejauh mana model mampu membedakan citra asli dari citra hasil manipulasi, sekaligus mengidentifikasi kelemahan model ketika dihadapkan pada variasi distribusi data atau skenario cross-dataset. Hal ini penting karena model generatif modern seperti GAN dan variannya menghasilkan konten yang makin realistis dan makin sulit dibedakan secara visual [8, 9, 14].

### BAB II — para 1038

**LAMA:**
> Secara keseluruhan, kombinasi metrik evaluasi tersebut memberikan pemahaman komprehensif mengenai performa pendekatan hybrid FFT + XceptionNet, termasuk kemampuan model untuk tetap robust, stabil, dan adaptif terhadap variasi jenis deepfake. Hal ini sejalan dengan berbagai penelitian…

**BARU:**
> Kombinasi metrik evaluasi tersebut memberikan gambaran menyeluruh mengenai performa pendekatan hybrid FFT + XceptionNet, termasuk kemampuan model mempertahankan kinerja terhadap variasi jenis deepfake. Hal ini sejalan dengan penelitian…

*(Buang pembuka "Secara keseluruhan" dan triad kosong "robust, stabil, dan adaptif".)*

### BAB II — para 1058

**LAMA:**
> Semakin canggihnya model generatif dalam menghasilkan video dan citra deepfake yang hampir tidak dapat dibedakan secara visual dari data asli, pemilihan metode deteksi yang tepat menjadi faktor krusial dalam penelitian ini. Pendekatan spasial umumnya berfokus pada analisis fitur visual langsung (seperti tekstur, warna, dan tepi wajah), sementara pendekatan frekuensi…

**BARU:**
> Model generatif kini semakin mampu menghasilkan video dan citra deepfake yang sulit dibedakan secara visual dari data asli, sehingga pemilihan metode deteksi yang tepat menjadi penting dalam penelitian ini. Pendekatan spasial berfokus pada analisis fitur visual langsung seperti tekstur, warna, dan tepi wajah, sedangkan pendekatan frekuensi…

*(Perbaiki juga kalimat pembuka yang menggantung secara gramatikal; "faktor krusial" → "penting".)*

### BAB II — para 1067 (kalimat penutup)

**LAMA:**
> …Dengan demikian, FFT dipilih karena mampu mendeteksi artefak tersembunyi hasil sintesis GAN secara efisien, umum, dan dilaporkan memiliki generalisasi lebih tinggi (klaim yang diuji pada penelitian ini).

**BARU:**
> …Atas dasar itu, FFT dipilih karena mampu mendeteksi artefak tersembunyi hasil sintesis GAN secara efisien dan bersifat umum, serta dilaporkan memiliki generalisasi yang lebih tinggi, klaim yang justru diuji pada penelitian ini.

### BAB III — para 1112

**LAMA:**
> Pemilihan dataset merupakan langkah krusial dalam penelitian deteksi deepfake. Dataset yang digunakan harus merepresentasikan keberagaman metode manipulasi dan tingkat kualitas visual yang berbeda agar model yang dikembangkan dapat dievaluasi secara komprehensif. … Selain itu, diuraikan pula strategi pembagian dataset…

**BARU:**
> Pemilihan dataset merupakan langkah penting dalam penelitian deteksi deepfake. Dataset yang digunakan harus merepresentasikan keberagaman metode manipulasi dan tingkat kualitas visual yang berbeda agar model dapat dievaluasi secara menyeluruh. … Bagian ini juga menguraikan strategi pembagian dataset…

---

## Ganti-frasa cepat (find → replace di Word — perubahan kecil)

Paragraf berikut hanya perlu ganti satu frasa (bukan seluruh paragraf), jadi cukup Find & Replace di Word:

| Para | Cari (LAMA) | Ganti (BARU) |
|------|-------------|--------------|
| p446 | `Dalam konteks ini, GAN dimanfaatkan` | `Dalam pembuatan deepfake, GAN dimanfaatkan` |
| p448 | `Dengan demikian, artefak yang muncul akibat proses pembangkitan GAN menjadi dasar dari metode deteksi deepfake berbasis analisis frekuensi` | `Artefak yang muncul akibat proses pembangkitan GAN inilah yang menjadi dasar metode deteksi deepfake berbasis analisis frekuensi` |
| p489 | `Dengan demikian, seluruh informasi spasial dan frekuensi diproses secara bersamaan` | `Dengan cara ini, seluruh informasi spasial dan frekuensi diproses bersamaan` |
| p531 | `Oppenheim dan Lim.` | `Oppenheim dan Lim` |
| p543 | `FDA memainkan peran penting dalam` | `FDA berperan penting dalam` |
| p611 | `deep learning juga berperan penting dalam pendeteksiannya` | `deep learning juga digunakan untuk pendeteksiannya` |
| p825 | `Dengan demikian, analisis video melibatkan pemrosesan frame-level` | `Karena itu, analisis video melibatkan pemrosesan frame-level` |
| p847 | `Normalisasi tidak hanya meningkatkan stabilitas pelatihan, tetapi juga mempercepat konvergensi model dan mengurangi risiko` | `Normalisasi meningkatkan stabilitas pelatihan dan mempercepat konvergensi model sekaligus mengurangi risiko` |
| p877 | `Dengan demikian, FFT menjadi pilihan yang efektif dan efisien` | `Atas dasar itu, FFT menjadi pilihan yang efektif dan efisien` |
| p893 | `pemilihan metode optimasi yang tepat sangat penting karena` | `pemilihan metode optimasi yang tepat menjadi penting karena` |
| p961 | `Hal ini sangat penting pada skenario forensik digital` | `Hal ini penting pada skenario forensik digital` |
| p1029 | `Dengan demikian, model berada dalam kategori performa baik` | `Dengan hasil tersebut, model berada dalam kategori performa baik` |
| p1035 | `Nilai recall sangat krusial karena` | `Nilai recall sangat penting karena` |
| p1037 | `Analisis ini sangat penting terutama pada skenario cross-dataset` | `Analisis ini penting terutama pada skenario cross-dataset` |
| p1044 | `Dengan demikian,  menjadi indikator langsung` | `Nilai ini menjadi indikator langsung` |
| p1051 | `Temuan ini menjelaskan mengapa` | `Hal ini menjelaskan mengapa` |
| p1055 | `Secara keseluruhan, konsep cross-dataset generalization menegaskan bahwa` | `Konsep cross-dataset generalization menegaskan bahwa` |

---

## Dibiarkan (false positive — bukan AI-like, teknis benar)

- **p539** — "tidak hanya … tetapi juga" di sini kontras nyata (ketersediaan sinyal vs inductive bias); prosa sudah baik.
- **p595** — "tidak hanya mempelajari tekstur … tetapi juga distribusi energi frekuensi" kontras substantif; biarkan.
- **p914** — deskripsi teknis AdamW (decoupled weight decay); "sangat penting" wajar, biarkan.
- **p1090** — pengantar pendekatan hybrid BAB III; "Di sisi lain / Oleh karena itu" penghubung wajar, biarkan.
- Semua paragraf dengan "konvergensi" dalam konteks optimizer/pelatihan (p693, p918, p1407, p1443) — istilah teknis benar.

---

## Catatan terpisah (bukan #3, untuk pass formatting/#2)

Beberapa paragraf punya **placeholder rumus kosong `()`** karena field persamaan tidak ter-render: **p1044** ("Nilai  yang mendekati nol"), **p1443** ("Nilai loss yang rendah ()"). Ini masalah field Word (Ctrl+A → F9 untuk refresh, atau isi ulang simbol), terpisah dari perbaikan wording. Dicatat agar tidak terlewat.
