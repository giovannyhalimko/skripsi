# Skill: Create Word-Pasteable HTML Table

## When to Trigger
When the user asks to create a table, convert a markdown table to HTML, or needs a table for Word/Docs.

## Output Location
Save HTML files to: `deepfake_hybrid/documents/table/`
Naming convention: `tabel_{chapter}_{number}_{short_description}.html`
Example: `tabel_2_1_komponen_domain_frekuensi.html`

## HTML Template

Every table HTML file must follow this exact structure:

```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
table { border-collapse: collapse; width: 100%; font-family: 'Times New Roman', serif; font-size: 12pt; }
th, td { border: 1px solid black; padding: 6px 10px; text-align: left; vertical-align: top; }
th { font-weight: bold; text-align: center; }
caption { caption-side: bottom; text-align: left; font-size: 11pt; padding-top: 6px; }
</style></head><body>
<table>
  <thead>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
    </tr>
  </tbody>
  <caption>Tabel X.X Judul Tabel (Sumber referensi)</caption>
</table>
</body></html>
```

## Rules

1. **Font:** Always `Times New Roman`, 12pt for table content, 11pt for caption
2. **Borders:** Always `1px solid black`, collapsed
3. **Caption:** Always at the bottom (`caption-side: bottom`), left-aligned
4. **Italic terms:** Use `<i>` tags for English/technical terms (e.g., `<i>deepfake</i>`, `<i>XceptionNet</i>`)
5. **Special characters:** Use HTML entities (`&times;` for ×, `&ndash;` for --, `&amp;` for &, `&sup2;` for ², `&ouml;` for ö)
6. **Width:** `width: 100%` by default; use `width: auto; margin: 0 auto;` for small tables like Confusion Matrix
7. **Header row cells:** Use `<th>` with `text-align: center`
8. **Row header cells:** If the first column acts as a row header, use `<th>` in `<tbody>` too
9. **No inline styles on individual cells** unless absolutely necessary for special alignment
10. **Self-contained:** Each file is a complete HTML document that can be opened in a browser

## How to Use (for the user)
1. Open the .html file in a browser
2. Ctrl+A (Select All)
3. Ctrl+C (Copy)
4. Paste into Word — the table will retain formatting with borders and fonts
