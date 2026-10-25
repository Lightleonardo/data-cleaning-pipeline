# Reproducibility Checklist

Each item was verified before being checked off; the verification method is noted
underneath each one.

- [x] **Raw data (`data/raw/orders_raw.csv`) is never modified after generation**
  The raw file is produced once by `generate_raw_data.py` and is only ever read
  (`pd.read_csv`) by the notebook; no notebook cell writes to `data/raw/`. All cleaning
  happens on an in-memory copy and is written to `data/cleaned/`.

- [x] **`generate_raw_data.py` uses a fixed random seed, so raw data is identical on every run**
  The script sets `random.seed(42)`. Verified by regenerating and comparing SHA-256
  hashes of `orders_raw.csv` before and after: both
  `066DF18B1D12C9269BA208A95234C6BE9C12A86C6A7D09BD9023BB2518C9A814` (identical).

- [x] **All package versions are pinned in `requirements.txt`**
  Every one of the 105 lines in `requirements.txt` uses an exact `==` pin (e.g.
  `pandas==3.1.0`, `numpy==2.5.4`).

- [x] **The notebook runs top-to-bottom with no errors via "Restart Kernel and Run All"**
  Verified by executing the notebook end-to-end in a fresh kernel with
  `jupyter nbconvert --to notebook --execute` (equivalent to Restart Kernel and Run
  All). It completed with exit code 0 and no cell errored (no `output_type: "error"` in
  the saved notebook).

- [x] **All file paths are relative to the project root, not hardcoded absolute paths**
  The notebook uses relative paths (`../data/raw/orders_raw.csv`,
  `../data/cleaned/orders_cleaned.csv`, `../data/cleaned/orders_cleaned.json`), and
  `generate_raw_data.py` uses `data/raw/orders_raw.csv`. A search for absolute
  Windows paths (`C:\` / `C:/`) in the notebook returns no matches.

- [x] **Cleaned data is only ever produced by running the notebook against the raw data, never edited by hand**
  `data/cleaned/orders_cleaned.csv` and `orders_cleaned.json` are written only by the
  export cell (`df.to_csv` / `df.to_json`) from the cleaned frame. No manual edits are
  made to the cleaned outputs.

- [x] **Every cleaning decision in the notebook has a Markdown cell explaining the reasoning**
  Section 2 contains one Markdown rationale cell immediately above each of the 9 code
  cells (2.1-2.9), and sections 1, 3, and 4 each have an introductory Markdown cell.

## Environment

| Item | Value |
|---|---|
| Python | 3.13 |
| pandas | 3.1.0 |
| numpy | 2.5.4 |
| Kernel | Python 3 (`ipykernel`) |
| Entry points | `generate_raw_data.py` → `notebooks/data_cleaning.ipynb` |
