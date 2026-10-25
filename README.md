# Data Cleaning Pipeline

A reproducible pandas/Jupyter workflow that transforms a messy orders dataset (CSV,
with an embedded JSON address column and a free-text notes column) into a documented,
analysis-ready dataset.

Raw: 203 rows × 10 columns. Cleaned: 200 rows × 13 columns, exported as both CSV and
JSON.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
```

## Running

1. (Optional) Regenerate the raw dataset: `python generate_raw_data.py`
   (uses a fixed seed, so the output is identical every run)
2. Launch Jupyter: `jupyter notebook`
3. Open `notebooks/data_cleaning.ipynb` and run all cells top to bottom
   (Kernel → Restart Kernel and Run All)

Running the notebook writes `data/cleaned/orders_cleaned.csv` and
`data/cleaned/orders_cleaned.json`.

## Project structure

| Path | Contents |
|---|---|
| `data/raw/orders_raw.csv` | Original, unmodified dataset (generated once) |
| `data/cleaned/` | Cleaned dataset, exported as CSV and JSON |
| `notebooks/data_cleaning.ipynb` | The full cleaning workflow |
| `generate_raw_data.py` | Generates the raw dataset with a fixed seed |
| `docs/data_dictionary.md` | Column-by-column reference for the cleaned data |
| `docs/profile_before_after.md` | What the data looked like before and after cleaning |
| `docs/transformation_log.md` | Every cleaning decision, and why it was made |
| `docs/reproducibility_checklist.md` | Confirms the pipeline is reproducible |

## What the pipeline does

- Removes exact duplicate rows and a row with a missing `order_id`.
- Standardizes casing/whitespace in `customer_name`, `product`, and `status`.
- Parses three mixed `order_date` formats into a real datetime.
- Cleans `unit_price` from `$`-prefixed/plain/missing strings into a numeric column.
- Flags (does not drop) invalid quantities via a `quantity_invalid` column.
- Expands the JSON `shipping_address` into `city`, `state`, and `zip`.
- Cleans the free-text `notes` column.

See `docs/transformation_log.md` for the full reasoning behind each step.
