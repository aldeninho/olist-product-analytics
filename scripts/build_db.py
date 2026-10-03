"""Load the Olist CSVs into a DuckDB database (data/olist.duckdb)."""
import duckdb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB = DATA / "olist.duckdb"

TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

con = duckdb.connect(str(DB))
for name, csv in TABLES.items():
    con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{DATA / csv}', header=true)")
    n = con.execute(f"SELECT count(*) FROM {name}").fetchone()[0]
    print(f"{name:20s} {n:>10,} rows")

# Useful parsed date columns
con.execute("""
ALTER TABLE orders ADD COLUMN purchase_ts TIMESTAMP;
""") if False else None

print("DB written to", DB)
