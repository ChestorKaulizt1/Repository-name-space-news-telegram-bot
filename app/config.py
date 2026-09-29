import os


RSS_FEEDS = {
    "NASA": "https://www.nasa.gov/feed/",
    "ESA": "https://www.esa.int/rssfeed",
    "Space.com": "https://www.space.com/feeds/all",
    "Universe Today": "https://universetoday.com/feed/",
    "ScienceAlert": "https://www.sciencealert.com/feed",
}


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/news.db"
)


MAX_ARTICLES_PER_SOURCE = int(
    os.getenv("MAX_ARTICLES_PER_SOURCE", "5")
)
