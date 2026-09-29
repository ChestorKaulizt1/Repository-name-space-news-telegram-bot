import feedparser

from app.config import RSS_FEEDS, MAX_ARTICLES_PER_SOURCE
from app.database import article_exists, save_article


def collect_news():
    new_articles = []

    for source, feed_url in RSS_FEEDS.items():

        print()
        print(f"Проверяем: {source}")
        print(f"RSS: {feed_url}")

        try:
            feed = feedparser.parse(feed_url)

            if feed.bozo:
                print("⚠ RSS вернул предупреждение")

            entries = feed.entries[:MAX_ARTICLES_PER_SOURCE]

            for entry in entries:

                title = entry.get(
                    "title",
                    "Без названия"
                ).strip()

                url = entry.get(
                    "link",
                    ""
                ).strip()

                published = entry.get(
                    "published",
                    entry.get("updated", "")
                )

                if not url:
                    continue

                if article_exists(url):
                    print(f"  Уже есть: {title}")
                    continue

                save_article(
                    source=source,
                    title=title,
                    url=url,
                    published=published
                )

                article = {
                    "source": source,
                    "title": title,
                    "url": url,
                    "published": published,
                }

                new_articles.append(article)

                print(f"  + НОВАЯ: {title}")

        except Exception as error:
            print(f"  ОШИБКА {source}: {error}")

    return new_articles
