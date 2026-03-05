# Skill: Analyze BAB (Chapter) Content

## When to Trigger
When the user asks to analyze a BAB (chapter) of the skripsi document — checking coverage, gaps, unnecessary content, or code-document alignment.

## Steps

1. **Read the target BAB** using line offsets from memory (or grep for `# BAB` headings)
2. **Read the reference BAB** (e.g., BAB I for requirements, BAB III for methodology)
3. **Read related code files** in `deepfake_hybrid/src/` and `deepfake_hybrid/scripts/`
4. **Cross-check** across three dimensions:
   - What the reference BAB requires vs what the target BAB covers
   - What the code implements vs what the target BAB discusses
   - What is in the target BAB but not needed (unnecessary content)
5. **Output analysis** to `/analyze/` directory

## Output Format

Save as: `analyze/{chapter}_Analysis_{document_short_title}_{YYYY-MM-DD}_{HHMM}.md`

Example: `analyze/BAB2_Analysis_Metode_Peningkatan_Deteksi_Deepfake_2026-03-05_1200.md`

## Analysis Structure

The output `.md` file must contain these sections:

```markdown
# {Chapter} Analysis — {Document Title}

## 1. Reference Baseline
Summary of what the reference BAB (e.g., BAB I) requires to be covered.

## 2. Coverage Check
Table or checklist: each requirement from the reference → covered / not covered / partially covered.

## 3. Missing Content
List of topics that SHOULD be in the target BAB but are missing or empty.

## 4. Code-Document Gaps
Misalignments between what the code does and what the document says.
(e.g., document says SGD but code uses Adam)

## 5. Unnecessary Content
Content in the target BAB that is not relevant to the research scope.

## 6. Priority Actions
Ordered list of recommended changes, from most critical to least.

## 7. Code Notes
Specific code files/lines referenced during analysis.
```

## Rules

1. Every claim in the analysis must reference a specific line number or code file
2. Be specific — say "Section 2.3.1 is empty [perlu isi]" not "some sections are incomplete"
3. Check for formula correctness (e.g., Recall = TP/(TP+FN), not TP/(TP+FP))
4. Check terminology consistency between document and code (optimizer names, loss functions, metric names)
5. Flag any content that contradicts the code implementation
