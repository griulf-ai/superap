import logging
import os
import threading

from flask import Flask, jsonify, render_template

from src.db import get_all_stocks, get_last_update_time, get_stock, get_stock_count, init_db
from src.scheduler import init_scheduler
from src.scraper import refresh_all_stocks, refresh_status

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = Flask(__name__)


@app.route("/")
def index():
    stocks = get_all_stocks(sort_by="rec_mean", order="ASC")
    last_update = get_last_update_time()
    stock_count = get_stock_count()
    return render_template(
        "index.html",
        stocks=stocks,
        last_update=last_update,
        stock_count=stock_count,
    )


@app.route("/stock/<ticker>")
def stock_detail(ticker):
    stock = get_stock(ticker.upper())
    if not stock:
        return render_template("stock.html", stock=None, ticker=ticker.upper()), 404
    return render_template("stock.html", stock=stock, ticker=ticker.upper())


@app.route("/api/refresh", methods=["POST"])
def manual_refresh():
    """Trigger a manual data refresh in a background thread."""
    if refresh_status["in_progress"]:
        return jsonify({"status": "refresh already in progress"})
    thread = threading.Thread(target=refresh_all_stocks, daemon=True)
    thread.start()
    return jsonify({"status": "refresh started"})


@app.route("/api/refresh/status")
def get_refresh_status():
    """Return the current refresh progress."""
    return jsonify(refresh_status)


@app.route("/api/stocks")
def api_stocks():
    """Return all stocks as JSON for live table updates."""
    stocks = get_all_stocks(sort_by="rec_mean", order="ASC")
    return jsonify({
        "stocks": stocks,
        "stock_count": get_stock_count(),
        "last_update": get_last_update_time(),
    })


def create_app():
    init_db()
    # Avoid duplicate scheduler when Flask reloader forks the process
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        init_scheduler()
    return app


if __name__ == "__main__":
    create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
