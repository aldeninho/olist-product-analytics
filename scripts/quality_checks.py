"""Data-quality checks: grain, null rates, key integrity on the Olist tables."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "olist.duckdb"), read_only=True)

checks = [
    ("orders PK unique", "SELECT COUNT(*) = COUNT(DISTINCT order_id) FROM orders"),
    ("customers PK unique", "SELECT COUNT(*) = COUNT(DISTINCT customer_id) FROM customers"),
    ("no null order status", "SELECT COUNT(*) = 0 FROM orders WHERE order_status IS NULL"),
    ("no null purchase ts", "SELECT COUNT(*) = 0 FROM orders WHERE order_purchase_timestamp IS NULL"),
    ("no negative prices", "SELECT COUNT(*) = 0 FROM order_items WHERE price < 0"),
    ("FK orders->customers ok", """SELECT NOT EXISTS (
        SELECT 1 FROM orders o LEFT JOIN customers c ON c.customer_id=o.customer_id
        WHERE c.customer_id IS NULL)"""),
    ("payment sums ~= item sums +/-5%", """SELECT abs(
        (SELECT SUM(payment_value) FROM payments) - (SELECT SUM(price+freight_value) FROM order_items)
    ) / (SELECT SUM(payment_value) FROM payments) < 0.05"""),
    ("reviews FK ok", """SELECT NOT EXISTS (
        SELECT 1 FROM reviews r LEFT JOIN orders o ON o.order_id=r.order_id
        WHERE o.order_id IS NULL)"""),
]
failed = 0
for name, sql in checks:
    ok = con.execute(sql).fetchone()[0]
    print(("PASS" if ok else "FAIL"), "-", name)
    failed += 0 if ok else 1
print(f"\n{len(checks) - failed}/{len(checks)} checks passed")
raise SystemExit(1 if failed else 0)
