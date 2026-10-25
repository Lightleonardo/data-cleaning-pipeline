# Data Dictionary

One row per column in the cleaned dataset
(`data/cleaned/orders_cleaned.csv` / `orders_cleaned.json`).

| Column | Type | Description | Example | Notes |
|---|---|---|---|---|
| `order_id` | int | Unique order identifier | `42` | Rows with a missing ID were dropped (1 row); cast from float to int |
| `customer_name` | string | Customer's full name | `Ada Obi` | Stripped and title-cased (`ada obi`, `BELLO MUSA` → `Ada Obi`, `Bello Musa`) |
| `email` | string | Customer email address | `ada@example.com` | May be missing; not validated during cleaning |
| `order_date` | datetime | Date the order was placed | `2026-03-14` | Parsed from 3 mixed source formats (ISO, `MM/DD/YYYY`, `DD-Mon-YYYY`) |
| `product` | string | Product name | `Laptop` | Stripped and title-cased; 7 raw spellings collapsed to 5 products |
| `quantity` | float | Number of units ordered | `2` | Kept as-is, including missing/zero/negative values (see `quantity_invalid`) |
| `unit_price` | float | Unit price of the product | `49.99` | `$` stripped and coerced to numeric; unknown prices left as missing (`NaN`/`null`) |
| `notes` | string | Free-text order note | `Please deliver after 5pm.` | Whitespace/newlines collapsed; empty strings converted to missing |
| `status` | string | Order status | `Delivered` | Stripped and title-cased; 6 raw spellings collapsed to 3 statuses |
| `quantity_invalid` | bool | Flags rows where quantity ≤ 0 or missing | `True` | Added during cleaning, not in raw data; flagged rather than dropped |
| `city` | string | Shipping city | `Lagos` | Parsed from the raw JSON `shipping_address` column |
| `state` | string | Shipping state | `FCT` | Parsed from the raw JSON `shipping_address` column |
| `zip` | string | Shipping postal code | `900009` | Parsed from the raw JSON `shipping_address`; kept as string to preserve leading zeros |

## Type notes

- `order_date` is exported as `datetime64` in the notebook; the CSV writes it as
  `YYYY-MM-DD` and the JSON as an ISO 8601 timestamp (`2026-03-14T00:00:00.000`).
- `quantity` and `unit_price` are floats because both contain missing values; a
  missing `unit_price` means the price was absent or unparseable in the source.
- `quantity_invalid` is the only column not present in the raw data — it is a
  cleaning artifact for downstream analysis to filter on.
