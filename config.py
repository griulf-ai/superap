import os

DATABASE_PATH = os.environ.get("SUPERAP_DB", "data/superap.db")
REFRESH_HOUR = int(os.environ.get("SUPERAP_REFRESH_HOUR", "6"))
REFRESH_MINUTE = int(os.environ.get("SUPERAP_REFRESH_MINUTE", "0"))
SCRAPE_DELAY_MIN = 1.0
SCRAPE_DELAY_MAX = 3.0
BATCH_SIZE = 50
BATCH_PAUSE_SECONDS = 30
SP500_WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
