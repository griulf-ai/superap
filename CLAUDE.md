# CLAUDE.md

This file provides guidance for AI assistants working with the **superap** repository.

## Repository Overview

- **Repository**: `griulf-ai/superap`
- **Description**: A web dashboard that displays S&P 500 analyst recommendations from Yahoo Finance, refreshed daily.
- **Tech stack**: Python 3, Flask, yfinance, SQLite, APScheduler, DataTables.js
- **Entry point**: `app.py`

## Project Structure

```
superap/
├── CLAUDE.md              # AI assistant guidance (this file)
├── requirements.txt       # Python dependencies
├── config.py              # App configuration (DB path, scheduler timing, rate limits)
├── app.py                 # Flask app entry point, routes, scheduler init
├── src/
│   ├── __init__.py
│   ├── db.py              # SQLite schema, connection helper, CRUD operations
│   ├── scraper.py         # S&P 500 ticker list from Wikipedia + yfinance data fetcher
│   └── scheduler.py       # APScheduler daily job configuration
├── templates/
│   ├── base.html          # Base layout (nav, footer, CDN includes)
│   ├── index.html         # Main dashboard: sortable table of all stocks
│   └── stock.html         # Detail view for a single stock
├── static/
│   ├── css/
│   │   └── style.css      # Dark-theme custom styles
│   └── js/
│       └── dashboard.js   # DataTables init + refresh button handler
├── data/
│   └── superap.db         # SQLite database (gitignored, created at runtime)
└── tests/
    └── __init__.py
```

## Development Setup

**Requirements**: Python 3.10+

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app starts at `http://localhost:5000`. The SQLite database is created automatically in `data/superap.db` on first run.

### Environment Variables (all optional)

| Variable | Default | Description |
|---|---|---|
| `SUPERAP_DB` | `data/superap.db` | Path to SQLite database file |
| `SUPERAP_REFRESH_HOUR` | `6` | Hour (UTC) for daily data refresh |
| `SUPERAP_REFRESH_MINUTE` | `0` | Minute for daily data refresh |

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run tests
python -m pytest tests/
```

## Architecture

### Data Flow

1. **Scraper** (`src/scraper.py`): Fetches S&P 500 ticker list from Wikipedia, then calls yfinance for each ticker to get analyst recommendations, price targets, and fundamentals.
2. **Database** (`src/db.py`): Stores all stock data in a single `recommendations` SQLite table. Uses `INSERT OR REPLACE` for upserts.
3. **Scheduler** (`src/scheduler.py`): APScheduler `BackgroundScheduler` triggers `refresh_all_stocks()` daily at the configured time (default 06:00 UTC).
4. **Web app** (`app.py`): Flask serves the dashboard at `/`, stock detail pages at `/stock/<ticker>`, and a manual refresh endpoint at `POST /api/refresh`.

### Database Schema

Single table `recommendations` with columns: `ticker` (PK), `company_name`, `sector`, `market_cap`, `current_price`, `target_mean`, `target_median`, `target_low`, `target_high`, `upside_pct`, `rec_key`, `rec_mean`, `num_analysts`, `strong_buy`, `buy`, `hold`, `sell`, `strong_sell`, `updated_at`.

### Routes

| Method | Path | Description |
|---|---|---|
| GET | `/` | Main dashboard with sortable stock table |
| GET | `/stock/<ticker>` | Detail page for a single stock |
| POST | `/api/refresh` | Trigger manual data refresh (runs in background thread) |

### Rate Limiting

The scraper uses random delays (1-3s between requests) and 30-second pauses every 50 tickers to avoid Yahoo Finance rate limiting. A full 500-ticker refresh runs for approximately 25-30 minutes.

## Code Conventions

- **Language**: Python 3.10+
- **Web framework**: Flask with Jinja2 server-side templates
- **Frontend**: Vanilla HTML/CSS/JS with DataTables.js (no build step, no React/Vue)
- **Database**: Raw `sqlite3` — no ORM
- **Config**: Plain Python module (`config.py`) with `os.environ.get()` defaults
- **Error handling**: Use `.get()` with defaults for yfinance data (fields may be missing). Log warnings, don't crash.
- **Naming**: snake_case for Python files, functions, variables. Lowercase kebab-case not used.

## Guidelines for AI Assistants

1. **Read before writing** — always read existing files before proposing changes.
2. **Minimal changes** — only make changes that are directly requested or clearly necessary.
3. **No over-engineering** — avoid adding features, abstractions, or configurability beyond what is asked.
4. **Security awareness** — do not introduce command injection, XSS, SQL injection, or other OWASP top-10 vulnerabilities. The `sort_by` parameter in `db.py` is validated against an allowlist.
5. **yfinance resilience** — always use `info.get()` with fallbacks when accessing yfinance data. Fields can disappear without notice.
6. **Keep this file current** — update CLAUDE.md whenever significant project structure, tooling, or conventions change.
