import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import REFRESH_HOUR, REFRESH_MINUTE
from src.scraper import refresh_all_stocks

logger = logging.getLogger(__name__)


def init_scheduler():
    """Start the background scheduler for daily data refresh."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=refresh_all_stocks,
        trigger=CronTrigger(hour=REFRESH_HOUR, minute=REFRESH_MINUTE),
        id="daily_refresh",
        name="Refresh S&P 500 analyst data",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        f"Scheduler started: daily refresh at {REFRESH_HOUR:02d}:{REFRESH_MINUTE:02d} UTC"
    )
    return scheduler
