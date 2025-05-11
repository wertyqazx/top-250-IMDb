import json
import os
import re
import sys
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────
# Настройки
URL = "https://www.imdb.com/chart/top"
HEADERS = {"User-Agent": "Mozilla/5.0"}


# ─────────────────────────────────────────────────────────────
# Парсим длительность из формата "PT2H22M" → 142 (минуты)
def parse_duration(duration_str):
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", duration_str or "")
    if not match:
        return None
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    return hours * 60 + minutes


# ─────────────────────────────────────────────────────────────
# Получаем дополнительные данные из карточки фильма
def get_details_from_card(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # JSON‑LD блок с актёрами и датой выхода
        json_ld = soup.find("script", type="application/ld+json")
        data = json.loads(json_ld.string) if json_ld else {}

        # Год выхода
        year = int(data["datePublished"][:4]) if "datePublished" in data else None

        # Страна производства (берём первую)
        country_tag = soup.find("a", href=re.compile(r"/search/title/\?country_of_origin="))
        country = country_tag.text.strip() if country_tag else None

        # Ведущие актёры (до 5 имён)
        actors_data = data.get("actor", [])
        actors = [actor.get("name") for actor in actors_data[:5]]
        actors_str = ", ".join(actors) if actors else None

        return year, country, actors_str

    except Exception as e:
        print(f"[!] Ошибка при парсинге карточки {url}: {e}")
        return None, None, None


# ─────────────────────────────────────────────────────────────
# Основной парсинг IMDb Top‑250
def fetch_top250(deep=False, delay=0.05):
    print("Скачиваем список фильмов…")
    response = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    json_block = soup.find("script", type="application/ld+json")
    items = json.loads(json_block.string)["itemListElement"]

    movies = []
    total = len(items)

    for index, item in enumerate(items, start=1):
        movie_data = item["item"]
        movie_url = (
            "https://www.imdb.com" + movie_data["url"]
            if movie_data["url"].startswith("/")
            else movie_data["url"]
        )

        movie = {
            "rank": index,
            "title": movie_data.get("name"),
            "rating": float(movie_data["aggregateRating"]["ratingValue"]),
            "votes": int(movie_data["aggregateRating"]["ratingCount"]),
            "genres": (
                ", ".join(movie_data["genre"])
                if isinstance(movie_data.get("genre"), list)
                else movie_data.get("genre", "")
            ),
            "duration_min": parse_duration(movie_data.get("duration")),
            "content_rating": movie_data.get("contentRating"),
            "year": None,
            "country": None,
            "actors": None,
            "url": movie_url,
        }

        if deep:
            try:
                year, country, actors = get_details_from_card(movie_url)
                movie.update({"year": year, "country": country, "actors": actors})
                print(f"[{index:3}/{total}] {movie['title']} — ok")
            except Exception as e:
                print(f"[{index:3}/{total}] {movie['title']} — ошибка: {e}")
            time.sleep(delay)

        movies.append(movie)

    return pd.DataFrame(movies)


# ─────────────────────────────────────────────────────────────
# Сохраняем результат в CSV
def save_csv(df, deep):
    filename = "imdb_top250_full.csv" if deep else "imdb_top250_basic.csv"
    path = os.path.join("..", "data", "raw", filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")

    print(f"\nСохранено {len(df)} фильмов в → {path}")


# ─────────────────────────────────────────────────────────────
# Точка входа
def main():
    deep_mode = "--deep" in sys.argv
    df = fetch_top250(deep=deep_mode)
    save_csv(df, deep=deep_mode)


if __name__ == "__main__":
    main()
