import csv
import random

random.seed(42)  # fixed seed: same "messy" data every time this is run

products = ["Laptop", "laptop ", "LAPTOP", "Headphones", "Keyboard", "Monitor", "Mouse"]
statuses = ["Delivered", "delivered", "DELIVERED", "Pending", "Cancelled", "cancelled"]
cities = ["Lagos", "Abuja", "Kano", "Ibadan", "Enugu"]

date_formats = ["{y}-{m:02d}-{d:02d}", "{m:02d}/{d:02d}/{y}", "{d:02d}-{mon}-{y}"]
months_abbr = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

rows = []
for i in range(1, 201):
    order_id = i
    name = random.choice(["Ada Obi", "ada obi", "BELLO MUSA", "Chinwe Okonkwo", "David Adebayo", "  Efe Okafor  "])
    email = random.choice(["ada@example.com", "", "bello.musa@example", "chinwe@example.com"])
    y, m, d = 2026, random.randint(1, 6), random.randint(1, 28)
    fmt = random.choice(date_formats)
    date_str = fmt.format(y=y, m=m, d=d, mon=months_abbr[m - 1])
    product = random.choice(products)
    quantity = random.choice([1, 2, 3, -1, 0, None])
    price_raw = random.choice(["199.99", "$49.99", "89.50", "", "N/A"])
    city = random.choice(cities)
    address_json = f'{{"city": "{city}", "state": "FCT", "zip": "90000{random.randint(1,9)}"}}'
    notes = random.choice([
        "Customer requested gift wrap.",
        "  Please deliver after 5pm.  ",
        "Urgent\n\ndelivery needed",
        "",
        "Called twice, no response.   Follow up.",
    ])
    status = random.choice(statuses)
    rows.append([order_id, name, email, date_str, product, quantity, price_raw, address_json, notes, status])

# Inject exact duplicate rows
rows.append(rows[10])
rows.append(rows[50])

# Inject a row with a missing order_id
rows.append(["", "Grace Nwosu", "grace@example.com", "2026-03-01", "Monitor", 1, "150.00",
             '{"city": "Lagos", "state": "FCT", "zip": "900001"}', "", "Delivered"])

with open("data/raw/orders_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer_name", "email", "order_date", "product",
                      "quantity", "unit_price", "shipping_address", "notes", "status"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to data/raw/orders_raw.csv")
