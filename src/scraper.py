import logging
import random
import time

import pandas as pd
import yfinance as yf

from config import (
    BATCH_PAUSE_SECONDS,
    BATCH_SIZE,
    SCRAPE_DELAY_MAX,
    SCRAPE_DELAY_MIN,
    SP500_WIKIPEDIA_URL,
)
from src.db import upsert_stock

logger = logging.getLogger(__name__)

# Module-level refresh progress tracking
refresh_status = {
    "in_progress": False,
    "processed": 0,
    "total": 0,
    "success": 0,
    "failed": 0,
}


def get_sp500_tickers() -> list[dict]:
    """Fetch current S&P 500 constituents from Wikipedia."""
    tables = pd.read_html(SP500_WIKIPEDIA_URL)
    df = tables[0]
    # Wikipedia uses '.' but yfinance uses '-' (e.g., BRK.B -> BRK-B)
    df["Symbol"] = df["Symbol"].str.replace(".", "-", regex=False)
    return df[["Symbol", "Security", "GICS Sector"]].to_dict("records")


def fetch_stock_data(ticker: str) -> dict | None:
    """Fetch analyst recommendation data for a single ticker from yfinance."""
    try:
        t = yf.Ticker(ticker)
        info = t.info

        if not info or info.get("trailingPegRatio") is None and len(info) < 5:
            logger.warning(f"{ticker}: no meaningful data returned")
            return None

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        target_mean = info.get("targetMeanPrice")
        target_median = info.get("targetMedianPrice")
        target_low = info.get("targetLowPrice")
        target_high = info.get("targetHighPrice")

        upside_pct = None
        if current_price and target_mean:
            upside_pct = round((target_mean - current_price) / current_price * 100, 2)

        rec_key = info.get("recommendationKey")
        rec_mean = info.get("recommendationMean")
        num_analysts = info.get("numberOfAnalystOpinions")

        # Analyst breakdown from recommendations_summary
        strong_buy = 0
        buy = 0
        hold = 0
        sell = 0
        strong_sell = 0
        try:
            rec_summary = t.recommendations_summary
            if rec_summary is not None and not rec_summary.empty:
                # Use the most recent period (first row)
                latest = rec_summary.iloc[0]
                strong_buy = int(latest.get("strongBuy", 0))
                buy = int(latest.get("buy", 0))
                hold = int(latest.get("hold", 0))
                sell = int(latest.get("sell", 0))
                strong_sell = int(latest.get("strongSell", 0))
        except Exception:
            pass

        return {
            "ticker": ticker,
            "company_name": info.get("shortName") or info.get("longName"),
            "sector": info.get("sector"),
            "market_cap": info.get("marketCap"),
            "current_price": current_price,
            "target_mean": target_mean,
            "target_median": target_median,
            "target_low": target_low,
            "target_high": target_high,
            "upside_pct": upside_pct,
            "rec_key": rec_key,
            "rec_mean": rec_mean,
            "num_analysts": num_analysts,
            "strong_buy": strong_buy,
            "buy": buy,
            "hold": hold,
            "sell": sell,
            "strong_sell": strong_sell,
        }

    except Exception as e:
        logger.error(f"{ticker}: failed to fetch data: {e}")
        return None


def refresh_all_stocks():
    """Fetch data for all S&P 500 stocks and store in the database."""
    logger.info("Starting S&P 500 data refresh...")

    try:
        tickers = get_sp500_tickers()
    except Exception as e:
        logger.error(f"Failed to fetch S&P 500 ticker list: {e}")
        return

    total = len(tickers)
    success = 0
    failed = 0

    refresh_status["in_progress"] = True
    refresh_status["processed"] = 0
    refresh_status["total"] = total
    refresh_status["success"] = 0
    refresh_status["failed"] = 0

    for i, row in enumerate(tickers):
        symbol = row["Symbol"]
        try:
            data = fetch_stock_data(symbol)
            if data:
                # Use Wikipedia data as fallback for sector/name
                data.setdefault("company_name", row["Security"])
                data.setdefault("sector", row["GICS Sector"])
                upsert_stock(data)
                success += 1
            else:
                failed += 1
        except Exception as e:
            logger.warning(f"Failed to process {symbol}: {e}")
            failed += 1

        refresh_status["processed"] = i + 1
        refresh_status["success"] = success
        refresh_status["failed"] = failed

        # Rate limiting
        if i < total - 1:
            time.sleep(random.uniform(SCRAPE_DELAY_MIN, SCRAPE_DELAY_MAX))

        # Batch pause
        if (i + 1) % BATCH_SIZE == 0:
            logger.info(f"Processed {i + 1}/{total} tickers, pausing...")
            time.sleep(BATCH_PAUSE_SECONDS)

    refresh_status["in_progress"] = False

    logger.info(
        f"Refresh complete: {success} succeeded, {failed} failed out of {total} tickers"
    )
