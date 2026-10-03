"""Shared DB connection + helpers for the multi-page dashboard."""
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]

def get_con():
    return duckdb.connect(str(ROOT / "data" / "olist.duckdb"), read_only=True)
