import os
import sqlite3
from datetime import datetime, timezone

from config import DATABASE_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS recommendations (
    ticker          TEXT PRIMARY KEY,
    company_name    TEXT,
    sector          TEXT,
    market_cap      REAL,
    current_price   REAL,
    target_mean     REAL,
    target_median   REAL,
    target_low      REAL,
    target_high     REAL,
    upside_pct      REAL,
    rec_key         TEXT,
    rec_mean        REAL,
    num_analysts    INTEGER,
    strong_buy      INTEGER DEFAULT 0,
    buy             INTEGER DEFAULT 0,
    hold            INTEGER DEFAULT 0,
    sell            INTEGER DEFAULT 0,
    strong_sell     INTEGER DEFAULT 0,
    updated_at      TEXT
);
"""


def get_connection():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def upsert_stock(data: dict):
    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO recommendations (
                ticker, company_name, sector, market_cap,
                current_price, target_mean, target_median, target_low, target_high,
                upside_pct, rec_key, rec_mean, num_analysts,
                strong_buy, buy, hold, sell, strong_sell, updated_at
            ) VALUES (
                :ticker, :company_name, :sector, :market_cap,
                :current_price, :target_mean, :target_median, :target_low, :target_high,
                :upside_pct, :rec_key, :rec_mean, :num_analysts,
                :strong_buy, :buy, :hold, :sell, :strong_sell, :updated_at
            )
            """,
            {
                "ticker": data.get("ticker"),
                "company_name": data.get("company_name"),
                "sector": data.get("sector"),
                "market_cap": data.get("market_cap"),
                "current_price": data.get("current_price"),
                "target_mean": data.get("target_mean"),
                "target_median": data.get("target_median"),
                "target_low": data.get("target_low"),
                "target_high": data.get("target_high"),
                "upside_pct": data.get("upside_pct"),
                "rec_key": data.get("rec_key"),
                "rec_mean": data.get("rec_mean"),
                "num_analysts": data.get("num_analysts"),
                "strong_buy": data.get("strong_buy", 0),
                "buy": data.get("buy", 0),
                "hold": data.get("hold", 0),
                "sell": data.get("sell", 0),
                "strong_sell": data.get("strong_sell", 0),
                "updated_at": now,
            },
        )


def get_all_stocks(sort_by="rec_mean", order="ASC"):
    allowed_columns = {
        "rec_mean", "upside_pct", "ticker", "company_name", "sector",
        "market_cap", "current_price", "target_mean", "num_analysts",
    }
    if sort_by not in allowed_columns:
        sort_by = "rec_mean"
    if order.upper() not in ("ASC", "DESC"):
        order = "ASC"

    with get_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT * FROM recommendations
            WHERE rec_mean IS NOT NULL
            ORDER BY {sort_by} {order}
            """
        ).fetchall()
    return [dict(r) for r in rows]


def get_stock(ticker: str):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM recommendations WHERE ticker = ?", (ticker,)
        ).fetchone()
    return dict(row) if row else None


def get_last_update_time():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT MAX(updated_at) as last_update FROM recommendations"
        ).fetchone()
    return row["last_update"] if row else None


def get_stock_count():
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM recommendations WHERE rec_mean IS NOT NULL"
        ).fetchone()
    return row["cnt"] if row else 0
