from app.rss_parser import collect_news


def main():
    print("=" * 60)
    print("КРАЙ РЕАЛЬНОСТИ — СБОРЩИК НОВОСТЕЙ")
    print("=" * 60)

    articles = collect_news()

    print()
    print("=" * 60)
    print(f"Новых материалов: {len(articles)}")
    print("=" * 60)

    if not articles:
        print("Новых материалов нет.")
        return

    for number, article in enumerate(
        articles,
        start=1
    ):
        print()
        print(f"[{number}] {article['source']}")
        print(article["title"])
        print(article["url"])


if __name__ == "__main__":
    main()
