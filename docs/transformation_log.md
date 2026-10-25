# Transformation Log

Chronological record of every cleaning decision applied to the raw orders dataset, in
the order the notebook runs them. Each entry states what was done, why, and what
changed (row/value counts). The corresponding cells live in
`notebooks/data_cleaning.ipynb`, section 2.

Starting point: `data/raw/orders_raw.csv` — **203 rows × 10 columns**.

## 1. Removed exact duplicate rows

Found 2 exact duplicate rows via `df.duplicated().sum()`. Exact duplicates add no
information and would double-count orders in any aggregate, so they were dropped with
`drop_duplicates()`.

**Rows:** 203 → 201.

## 2. Dropped rows with a missing `order_id`

1 row had a blank `order_id`, making it untrackable and impossible to deduplicate
reliably later. Rather than invent a synthetic ID (which would fabricate data), the row
was dropped. With the missing value gone, `order_id` was cast from `float64` to `int`.

**Rows:** 201 → 200. **`order_id` dtype:** `float64` → `int64`.

## 3. Standardized `customer_name` casing and whitespace

The same person appeared as `Ada Obi`, `ada obi`, `BELLO MUSA`, and `  Efe Okafor  `.
Names were stripped of surrounding whitespace and title-cased so they are comparable
across rows and in joins.

**Values:** `ada obi` → `Ada Obi`, `BELLO MUSA` → `Bello Musa`, `  Efe Okafor  ` →
`Efe Okafor`.

## 4. Standardized `product` and `status` categories

Mixed casing split single real categories into several spellings. Both columns were
stripped and title-cased so each category collapses to one value.

**`product`:** 7 unique → 5 unique (`laptop `, `LAPTOP`, `Laptop` → `Laptop`).
**`status`:** 6 unique → 3 unique (`delivered`, `Delivered`, `DELIVERED` → `Delivered`;
`cancelled`, `Cancelled` → `Cancelled`; `Pending` unchanged).

## 5. Parsed the mixed `order_date` formats

`order_date` mixed three layouts in one column: ISO (`2026-01-03`), US (`01/24/2026`),
and day-month name (`15-Feb-2026`). It was parsed with
`pd.to_datetime(df["order_date"], format="mixed")`, which infers the format per value.

**`order_date` dtype:** `str` → `datetime64[us]`. No values were lost (0 missing before
and after).

## 6. Cleaned `unit_price` into a numeric column

Prices mixed plain numbers (`199.99`), currency-prefixed strings (`$49.99`), and
missing markers (`N/A`, empty). The markers were normalized, `$` was stripped, and the
column was coerced to numeric with `errors="coerce"`. Where a price is unknown the
order's value is unknowable, so it was left as a real missing value rather than guessed.

**`unit_price` dtype:** `str` → `float64`. **Missing prices:** 83 of 200 rows.

## 7. Flagged invalid quantities (did not drop)

Negative or zero quantities are logically invalid for an order, and a missing quantity
is unknown. Per the chosen policy these rows were **flagged, not dropped**, because the
rest of the row (customer, address, notes) may still be useful. A new boolean column
`quantity_invalid` was added; the original `quantity` values were kept unchanged.

**New column:** `quantity_invalid` (`bool`). **Flagged rows:** 101 of 200 are `True`.

## 8. Parsed the embedded JSON `shipping_address`

`shipping_address` held a JSON object per row (e.g. `{"city": "Lagos", "state": "FCT",
"zip": "900001"}`). Each string was parsed with `json.loads` and expanded into real
`city`, `state`, and `zip` columns; the original JSON string column was dropped.

**Columns:** `shipping_address` (1) → `city`, `state`, `zip` (3). **Rows affected:**
200 (all parsed successfully). `zip` is kept as a string to preserve leading zeros.

## 9. Cleaned the free-text `notes` column

Notes contained embedded newlines and runs of spaces (e.g. `"Urgent\n\ndelivery
needed"`) plus invisible empty strings. Runs of whitespace were collapsed to a single
space, ends were stripped, and empty strings were converted to a real missing value so
blanks are not mistaken for content.

**Values:** `"Urgent\n\ndelivery needed"` → `"Urgent delivery needed"`;
`"  Please deliver after 5pm.  "` → `"Please deliver after 5pm."`.
**Missing `notes`:** 39 of 200 rows.

## 10. Exported the cleaned dataset

The cleaned frame was written to two formats from the same in-memory data so the copies
cannot drift apart: `data/cleaned/orders_cleaned.csv` (`index=False`) and
`data/cleaned/orders_cleaned.json` (`orient="records"`, `indent=2`,
`date_format="iso"`).

**Output:** 200 rows × 13 columns in both formats.

## Summary

| Stage | Rows | Columns |
|---|---|---|
| Raw | 203 | 10 |
| After duplicate removal | 201 | 10 |
| After dropping missing `order_id` | 200 | 10 |
| Final (after normalization + expansion) | 200 | 13 |

Net row reduction: 3 (2 duplicates + 1 missing key). Net column change: +3
(`shipping_address` replaced by `city`/`state`/`zip`, plus `quantity_invalid`).
