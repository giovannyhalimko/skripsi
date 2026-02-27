# Skripsi Format & Style Guide

> Source: Pedoman Skripsi 2025 & Template Skripsi 2025 — Fakultas Informatika, Universitas Mikroskil

This skill defines the exact formatting rules, document structure, and content guidelines for the skripsi markdown file. Any agent editing the skripsi `.md` file MUST follow these rules.

---

## 1. Document Structure (Exact Order)

The skripsi document MUST contain these sections in this exact order:

```
1.  Sampul Bahasa Indonesia        (cover page, Indonesian)
2.  Sampul Bahasa Inggris          (cover page, English)
3.  Lembaran Pengesahan            (approval page)
4.  Halaman Pernyataan             (one per student — 3 pages for group of 3)
5.  Abstrak / Abstract             (Indonesian + English, on same page if possible)
6.  Kata Pengantar                 (acknowledgements)
7.  Daftar Isi                     (table of contents)
8.  Daftar Gambar                  (list of figures)
9.  Daftar Tabel                   (list of tables)
10. Daftar Lampiran                (list of appendices)
11. BAB I   — PENDAHULUAN
12. BAB II  — KAJIAN LITERATUR
13. BAB III — TAHAPAN PELAKSANAAN
14. BAB IV  — HASIL DAN PEMBAHASAN
15. BAB V   — PENUTUP
16. DAFTAR PUSTAKA
17. Lampiran Gambar
18. Lampiran Tabel
19. Lampiran Bukti Pelaksanaan dengan Mitra (if applicable)
20. Daftar Riwayat Hidup           (one per student)
```

---

## 2. Heading Hierarchy in Markdown

### Bab (Chapter) Titles
- Use `#` (H1) for bab titles
- Format: `# BAB I PENDAHULUAN`, `# BAB II KAJIAN LITERATUR`, etc.
- Also use `#` for non-chapter top-level sections: `# DAFTAR PUSTAKA`, `# DAFTAR GAMBAR`, etc.
- Bab numbering uses uppercase Roman numerals: I, II, III, IV, V

### Subbab (Section) Titles
- Use `##` (H2) for first-level subbab: `## 1.1 Latar Belakang`
- Use `###` (H3) for second-level subbab: `### 1.1.1 Sub-Section Title`
- Use `####` (H4) for third-level subbab: `#### 1.1.1.1 Sub-Sub-Section Title`
- Maximum 3 levels of subbab depth
- Subbab numbering uses Arabic numerals with dot notation (e.g., 2.1, 2.1.1, 2.1.1.1)
- Subbab titles use Title Case (capitalize each word)
- If a subbab has sub-levels, there must be at least 2 sub-items (e.g., if 2.3.1 exists, 2.3.2 must also exist)

---

## 3. Page Numbering Convention (for reference in ToC)

- **Front matter** (Abstrak through Daftar Lampiran): lowercase Roman numerals (i, ii, iii, iv, ...)
- **Body + back matter** (BAB I through Daftar Riwayat Hidup): Arabic numerals (1, 2, 3, ...)
- Sampul pages have no page numbers

---

## 4. Figures and Tables

### Figures (Gambar)
- Caption goes BELOW the figure
- Numbering format: `Gambar [bab].[urut]` (e.g., `Gambar 2.1` = first figure in Bab II)
- Caption uses Title Case
- Center-aligned in the document
- If figure is too large, place on its own page in landscape; font inside must be >= 10pt
- If a figure is continued, use: `Gambar X.X (sambungan)`

### Tables (Tabel)
- Caption goes ABOVE the table
- Numbering format: `Tabel [bab].[urut]` (e.g., `Tabel 3.4` = fourth table in Bab III)
- Caption uses Title Case
- If a table is continued, use: `Tabel X.X (sambungan)`

### Placement
- Figures/tables are placed after the text that discusses them, with no extra blank lines
- Text continues after figure/table without extra spacing

---

## 5. Mathematical Equations

- Use LaTeX notation in markdown: `$...$` for inline, `$$...$$` for display
- Equations are numbered on the right side: `(bab.urut)` e.g., `(2.1)`
- Include "Dimana:" section after equations to define variables

---

## 6. Numbering (Lists)

Maximum 3 levels:
- Level 1: `1. 2. 3. 4. ...`
- Level 2: `a. b. c. d. ...`
- Level 3: `i. ii. iii. iv. ...`

---

## 7. Citations (Sitasi) — IEEE Style

- Format: `[number]` in order of first appearance, e.g., `[1]`, `[1,3]`, `[1-5]`
- Every citation MUST appear in Daftar Pustaka; every Daftar Pustaka entry MUST be cited
- Ordering: by order of first citation appearance (NOT alphabetical by author)
- Must use peer-reviewed sources (journals, books, conference proceedings)
- NO preprints, drafts, working papers, or unpublished manuscripts
- Recommended: >= 70% of references should be from the last 5 years
- Use "dkk." (et al.) when there are more than 3 authors

### Daftar Pustaka Format (IEEE)

**Book:**
```
[N] First Initial. Middle Initial. Last Name, "Book Title (italic)," edition, Publisher, City, Year.
```

**Translated Book:**
```
[N] First Initial. Middle Initial. Last Name, "Translated Book Title (italic)," Vol. X, Ed. X, Publisher, City, Year (diterjemahkan oleh Translator Name).
```

**Journal Article:**
```
[N] First Initial. Middle Initial. Last Name, "Article Title," Journal Name (italic), vol. X, no. X, pp. XX–XX, Month Year.
```

**Conference Proceedings:**
```
[N] First Initial. Middle Initial. Last Name, "Paper Title," Conference Name (italic), Location, Year, pp. XX–XX.
```

**Website:**
```
[N] Author/Org, "Page Title," Site Name (italic), [Online]. Tersedia: URL (akses pada: DD Month YYYY).
```

---

## 8. Content Guidelines per Chapter

### BAB I — PENDAHULUAN
Must contain exactly these subbabs:
- **1.1 Latar Belakang**: 3-5 paragraphs (S-1). Must include citations. Explain: problem background, existing solutions with pros/cons, proposed solution.
- **1.2 Rumusan Masalah**: 1 paragraph, specific formulation of the problem (question or statement form).
- **1.3 Tujuan**: What the research aims to achieve. Can use numbered list.
- **1.4 Manfaat**: Positive impact/contribution after objectives are met.
- **1.5 Ruang Lingkup**: Scope, limitations, assumptions. Keeps research focused.

### BAB II — KAJIAN LITERATUR
- For S-1: Explain theories, concepts, models, methods, algorithms used in the skripsi
- Order: general concepts first, then specific
- Every claim must have a citation from a reputable source
- Allowed: published books, accredited journals, conference proceedings, official organization websites
- NOT allowed: lecture slides/handouts, social media, wikis, blogs, WordPress

### BAB III — TAHAPAN PELAKSANAAN
- For S-1: Title is "TAHAPAN PELAKSANAAN" (not "Metodologi Penelitian")
- Describes systematic steps/strategy to solve the problem from BAB I
- Can reference research methodology, system development methodology, or other relevant approaches
- Can include flowcharts/diagrams

### BAB IV — HASIL DAN PEMBAHASAN
- **4.1 Hasil**: Implementation results, testing results per scope. Can have multiple sub-sections.
- **4.2 Pembahasan**: Analysis/discussion of results. Must answer the problems from BAB I.

### BAB V — PENUTUP
- For S-1: Can contain either Rangkuman OR Kesimpulan + Saran
- **Kesimpulan**: Summary of research findings. Must answer each rumusan masalah. One conclusion per hypothesis (if applicable).
- **Saran**: Recommendations for future work. Must stay within the research topic.

---

## 9. Front Matter Specifics

### Sampul (Cover)
- All text UPPERCASE and Bold
- No abbreviations in title (except proper nouns like PT, UD, CV)
- Title must not be a question
- No punctuation at end of title
- Includes: Title, "SKRIPSI", "Oleh:", Student names + NIMs, University logo, Program Studi, Fakultas, University, City, Year

### Abstrak
- Max 200 words per language version (Indonesian + English)
- Italic text
- Single paragraph each
- Both versions on same page if possible
- Must include: reason for topic, methodology, summary of results, brief conclusion
- End with "Kata kunci:" (Indonesian) / "Keywords:" (English) — 3 to 5 keywords in italic

### Kata Pengantar
- Thank-you order: internal university people first, then external, then family/friends
- Standard order of acknowledgements:
  1. Dosen Pembimbing I
  2. Dosen Pembimbing II
  3. Rektor Universitas Mikroskil Medan
  4. Dekan Fakultas Informatika
  5. Ketua Program Studi
  6. Company/Mitra (if applicable)
  7. Parents and family
  8. Others

### Daftar Isi
- Front matter pages use Roman numerals (i, ii, iii...)
- Body pages use Arabic numerals (1, 2, 3...)
- Includes all sections from ABSTRAK through DAFTAR RIWAYAT HIDUP

### Daftar Gambar / Daftar Tabel / Daftar Lampiran
- List all figures/tables/appendices with their page numbers

---

## 10. Back Matter

### Lampiran
- Lampiran Gambar: collection of figures/screenshots used or produced
- Lampiran Tabel: collection of tables used or produced
- Lampiran Bukti Pelaksanaan dengan Mitra (if applicable): includes Surat Keterangan Bersedia Menjadi Mitra, documentation log with dates/activities/photos, Surat Selesai dari Mitra

### Daftar Riwayat Hidup
- One per student
- Includes: photo, personal info (NIM, name, gender, DOB, religion, phone, email), formal education, non-formal education, organizational experience, work experience, certifications

---

## 11. Project-Specific Information

This skripsi is for:
- **Program**: S-1 Teknik Informatika
- **Fakultas**: Informatika
- **Universitas**: Mikroskil, Medan
- **Jalur**: Riset (Research track)
- **Pengerjaan**: Kelompok (3 students)

### Students:
1. Naomi Prisella — NIM 221111798
2. Giovanny Halimko — NIM 221110058
3. Samuel Onasis — NIM 221110680

### Dosen Pembimbing:
1. Gunawan S.Kom., M.T.I. (Pembimbing I)
2. Heru Kurniawan S.Kom., M.Kom. (Pembimbing II)

### Title:
- ID: Metode Peningkatan Deteksi Deepfake Berbasis Arsitektur Hybrid XceptionNet dan Analisis Artefak Domain Frekuensi
- EN: An Enhanced Deepfake Detection Method Based on Hybrid XceptionNet Architecture and Frequency-Domain Artifact Analysis

---

## 12. Markdown-Specific Conventions

Since the document is maintained as `.md`, follow these conventions:
- Use standard markdown syntax (headings, bold, italic, lists, tables, images, math)
- Images reference format: `![caption](./media/media/imageN.ext)`
- Bold text with `**text**`, italic with `*text*`
- Tables use markdown pipe tables
- LaTeX math uses `$...$` inline and `$$...$$` for display blocks
- Horizontal rules (`---`) may be used to separate major document sections (sampul, etc.) but are not required
- Keep each bab starting clearly (with its `#` heading)
- Foreign/English terms within Indonesian text should be *italicized*
