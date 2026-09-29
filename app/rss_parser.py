import feedparser

from app.config import RSS_FEEDS, MAX_ARTICLES_PER_SOURCE
from app.database import article_exists, save_article


# Сильные космические ключевые слова.
# Если заголовок содержит одно из них — материал получает высокий приоритет.
STRONG_SPACE_KEYWORDS = [
    # Планеты и спутники
    "mars",
    "moon",
    "lunar",
    "venus",
    "jupiter",
    "saturn",
    "mercury",
    "uranus",
    "neptune",
    "pluto",

    # Космос и астрономия
    "space",
    "cosmos",
    "astronomy",
    "astronomical",
    "astrophysics",
    "astrophysical",
    "universe",
    "cosmic",

    # Звёзды и компактные объекты
    "star",
    "stars",
    "stellar",
    "neutron star",
    "pulsar",
    "magnetar",
    "supernova",
    "supernovae",

    # Чёрные дыры
    "black hole",
    "black holes",
    "supermassive black hole",
    "event horizon",

    # Галактики
    "galaxy",
    "galaxies",
    "galactic",

    # Экзопланеты
    "exoplanet",
    "exoplanets",
    "habitable planet",
    "habitable world",

    # Космические объекты
    "asteroid",
    "asteroids",
    "comet",
    "comets",
    "meteor",
    "meteors",
    "meteorite",
    "interstellar object",

    # Телескопы
    "jwst",
    "james webb",
    "webb telescope",
    "hubble",
    "space telescope",

    # Космические миссии и аппараты
    "spacecraft",
    "spacecrafts",
    "spaceship",
    "space station",
    "iss",
    "starliner",
    "artemis",
    "apollo mission",
    "rover",
    "probe",
    "orbiter",

    # Запуски и ракеты
    "rocket",
    "rockets",
    "launch",
    "launches",
    "liftoff",
    "spacex",
    "starship",

    # Космические явления
    "solar flare",
    "solar storm",
    "solar wind",
    "sunspot",
    "coronal mass ejection",
    "gamma ray burst",
    "gamma-ray burst",
    "gravitational wave",
    "dark matter",
    "dark energy",
    "wormhole",
    "quasar",
    "nebula",

    # Космонавты
    "astronaut",
    "astronauts",
    "cosmonaut",
    "cosmonauts",

    # Ночное небо
    "night sky",
    "stargazing",
    "skywatching",
]


# Общие космические слова.
# Они дают небольшой дополнительный балл.
GENERAL_SPACE_KEYWORDS = [
    "orbit",
    "orbital",
    "satellite",
    "mission",
    "missions",
    "spaceflight",
    "spaceflight",
    "nasa",
    "esa",
    "esa mission",
    "rocket",
    "telescope",
    "astronaut",
    "planet",
    "planets",
]


# Темы, которые нам не нужны для Telegram-канала
# "КРАЙ РЕАЛЬНОСТИ".
EXCLUDE_KEYWORDS = [
    # Медицина
    "cancer",
    "infection",
    "infections",
    "disease",
    "medicine",
    "medical",
    "health",
    "brain health",
    "menopause",
    "drug",
    "drugs",

    # Психология
    "anger",
    "anxiety",
    "depression",
    "psychology",
    "mental health",

    # Питание
    "nutrition",
    "diet",
    "food",
    "calories",

    # Политика и общественные темы
    "politics",
    "political",
    "election",
    "government",

    # Земные темы, не связанные с космосом
    "ocean",
    "oceans",
    "climate",
    "earthquake",
    "volcano",
    "weather",

    # Компьютеры и технологии, не связанные напрямую с космосом
    "quantum computer",
    "quantum computing",
    "artificial intelligence",
    "ai model",
    "smartphone",
]


def calculate_relevance_score(title: str, source: str = "") -> int:
    """
    Оценивает насколько новость подходит для космического канала.

    Чем выше балл — тем больше вероятность,
    что материал относится к космосу.
    """

    text = f"{title} {source}".lower()

    score = 0

    # Сильные космические слова
    for keyword in STRONG_SPACE_KEYWORDS:
        if keyword in text:
            score += 3

    # Общие космические слова
    for keyword in GENERAL_SPACE_KEYWORDS:
        if keyword in text:
            score += 1

    # Штраф за явно неподходящие темы
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in text:
            score -= 5

    return score


def is_space_article(title: str, source: str = "") -> bool:
    """
    Проверяет, подходит ли статья для космического канала.
    """

    score = calculate_relevance_score(
        title=title,
        source=source
    )

    # Минимальный балл для публикации.
    return score >= 3


def collect_news():
    """
    Собирает новые космические новости из RSS-источников.
    """

    new_articles = []

    for source, feed_url in RSS_FEEDS.items():

        print()
        print("=" * 60)
        print(f"Проверяем: {source}")
        print(f"RSS: {feed_url}")

        try:

            feed = feedparser.parse(feed_url)

            if feed.bozo:
                print("⚠ RSS вернул предупреждение")

            entries = feed.entries[:MAX_ARTICLES_PER_SOURCE]

            if not entries:
                print("  Новостей не найдено.")

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

                # -------------------------------------------------
                # ФИЛЬТР КОСМИЧЕСКИХ НОВОСТЕЙ
                # -------------------------------------------------

                score = calculate_relevance_score(
                    title=title,
                    source=source
                )

                if not is_space_article(
                    title=title,
                    source=source
                ):
                    print(
                        f"  ✕ Пропущено "
                        f"(не космос, score={score}): "
                        f"{title}"
                    )
                    continue

                print(
                    f"  ✓ Космос "
                    f"(score={score}): "
                    f"{title}"
                )

                # -------------------------------------------------
                # ПРОВЕРКА НА ДУБЛИКАТ
                # -------------------------------------------------

                if article_exists(url):

                    print(
                        f"  ↳ Уже есть в базе: "
                        f"{title}"
                    )

                    continue

                # -------------------------------------------------
                # СОХРАНЕНИЕ
                # -------------------------------------------------

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
                    "score": score,
                }

                new_articles.append(article)

                print(
                    f"  + НОВАЯ КОСМИЧЕСКАЯ НОВОСТЬ: "
                    f"{title}"
                )

        except Exception as error:

            print(
                f"  ОШИБКА {source}: "
                f"{error}"
            )

    return new_articles
