The notebook is at `deepfake_hybrid/colab_train.ipynb`. Here's what to do:

### How to use it

1. **Upload to Colab** — go to [colab.research.google.com](https://colab.research.google.com) → File → Upload notebook → pick `colab_train.ipynb`
2. **Switch runtime to GPU** — Runtime → Change runtime type → T4 GPU
3. **Run cells top to bottom** — each step is clearly labeled

### Two things you need to edit before running

| Cell | Variable | What to set |
|------|----------|-------------|
| Step 1 | `CODE_IN_DRIVE` | Path to your skripsi folder in Drive |
| Step 3 | `FFPP_IN_DRIVE` | Path to the FFPP dataset shortcut in Drive |

### Getting the dataset into Drive
1. Open the shared folder link
2. Click the dropdown arrow next to the folder name → **"Add shortcut to Drive"**
3. Place it in `My Drive` and note the exact folder name — use that as `FFPP_IN_DRIVE`

### One important thing
The notebook sets `epochs: 20` — that's the minimum for meaningful results. If you want statistically valid numbers for the thesis, change `n_seeds` to `3` in Step 4 (means 3 training runs per model, takes ~3x longer).