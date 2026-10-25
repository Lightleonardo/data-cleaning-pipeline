# Profile: Before vs After

The raw orders dataset and the cleaned dataset, profiled with the same commands
(`df.shape`, `df.info()`, `df.isna().sum()`, `df.duplicated().sum()`) so the numbers
line up one-to-one. "Before" is the raw file as generated; "after" is the frame at the
end of `notebooks/data_cleaning.ipynb`.

## Shape

| | Before | After |
|---|---|---|
| Rows | 203 | 200 |
| Columns | 10 | 13 |

Rows fell by 3: 2 exact duplicates removed, and 1 row with a missing `order_id`
dropped. Columns rose from 10 to 13: the JSON `shipping_address` column was expanded
into `city`, `state`, `zip`, and a `quantity_invalid` flag column was added
(10 - 1 + 3 + 1 = 13).

## Columns

**Before (10):** `order_id, customer_name, email, order_date, product, quantity,
unit_price, shipping_address, notes, status`

**After (13):** `order_id, customer_name, email, order_date, product, quantity,
unit_price, notes, status, quantity_invalid, city, state, zip`

`shipping_address` is gone (replaced by `city`/`state`/`zip`); `quantity_invalid` is
new.

## Duplicates

| | Before | After |
|---|---|---|
| `df.duplicated().sum()` | 2 | 0 |

## Missing values per column

| Column | Before | After | Note |
|---|---|---|---|
| `order_id` | 1 | 0 | Row dropped (untrackable without a key) |
| `customer_name` | 0 | 0 | — |
| `email` | 41 | 40 | Two duplicates removed, one had a missing email |
| `order_date` | 0 | 0 | — |
| `product` | 0 | 0 | — |
| `quantity` | 33 | 33 | Kept as missing; flagged via `quantity_invalid` |
| `unit_price` | 84 | 83 | Unknown price left as a real missing value |
| `shipping_address` | 0 | — | Column replaced by `city`/`state`/`zip` |
| `notes` | 41 | 39 | Two duplicates removed; blanks converted to missing |
| `status` | 0 | 0 | — |
| `quantity_invalid` | — | 0 | New flag column, never missing |
| `city` | — | 0 | Parsed from JSON |
| `state` | — | 0 | Parsed from JSON |
| `zip` | — | 0 | Parsed from JSON |

## Data types

| Column | Before | After |
|---|---|---|
| `order_id` | `float64` | `int64` |
| `order_date` | `str` (3 mixed formats) | `datetime64[us]` |
| `unit_price` | `str` (mixed `$`/plain/`N/A`) | `float64` |
| `quantity` | `float64` | `float64` |
| `quantity_invalid` | — | `bool` |
| `customer_name, email, product, notes, status` | `str` | `str` |
| `city, state, zip` | — | `str` |

## Categorical consistency

| Column | Before (unique) | After (unique) |
|---|---|---|
| `product` | 7 (`laptop `, `LAPTOP`, `Laptop`, `Mouse`, `Monitor`, `Keyboard`, `Headphones`) | 5 (`Laptop`, `Mouse`, `Monitor`, `Keyboard`, `Headphones`) |
| `status` | 6 (`Cancelled`, `cancelled`, `delivered`, `Delivered`, `Pending`, `DELIVERED`) | 3 (`Cancelled`, `Delivered`, `Pending`) |

Casing and whitespace noise collapsed 7 product spellings into 5 real products and 6
status spellings into 3 real statuses.

## Text quality

`notes` contained embedded newlines and runs of spaces (e.g. `"Urgent\n\ndelivery
needed"`). After cleaning, whitespace is collapsed to single spaces and leading/trailing
space is stripped (`"Urgent delivery needed"`), with empty strings converted to real
missing values.

## Interpretation

The cleaned frame is analysis-ready for the questions this dataset invites: order
counts and value over time (`order_date` is now a real datetime), revenue by product
and status (categories are consolidated), and geographic breakdowns (`city`/`state`/
`zip` are first-class columns). Rows with an unknown or invalid `quantity` remain in
the dataset and are explicitly marked by `quantity_invalid`, so downstream analysis can
either exclude or account for them rather than silently losing the rest of the row.
