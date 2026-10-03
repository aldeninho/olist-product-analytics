"""Run every SQL file and print/save results."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "olist.duckdb"))
out = ROOT / "results"
out.mkdir(exist_ok=True)

for path in sorted((ROOT / "sql").glob("*.sql")):
    print("\n" + "=" * 70)
    print(path.name)
    print("=" * 70)
    sql = "\n".join(l for l in path.read_text().splitlines() if not l.strip().startswith("--"))
    for i, stmt in enumerate(s for s in sql.split(";") if s.strip()):
        try:
            df = con.execute(stmt).fetchdf()
            print(df.head(15).to_string(index=False))
            df.to_csv(out / f"{path.stem}_{i}.csv", index=False)
        except Exception as e:
            print("[no result set executed]", e)
