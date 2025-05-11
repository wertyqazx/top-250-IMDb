"""
Очистка сырых CSV из папки data/raw/ и сохранение чистых версий в data/clean/.

Запускать после парсинга фильмов:
    python scripts/clean_imdb_top250.py
"""

import os
import pandas as pd

# ───────────────────────────────────────────────
# Пути к папкам
RAW_DIR = os.path.join("..", "data", "raw")
CLEAN_DIR = os.path.join("..", "data", "clean")

# Названия входных и выходных файлов
FILES = {
    "imdb_top250_basic.csv": "imdb_top250_basic_clean.csv",
    "imdb_top250_full.csv":  "imdb_top250_full_clean.csv",
}

# ───────────────────────────────────────────────
# Очистка одного датафрейма
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Приводим типы, убираем дубликаты и пропуски, genres и actors → список."""

    # Приведение типов: числовые
    for col in ["rank", "rating", "votes", "duration_min"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Приведение года к int (без .0)
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    # genres: строка → список
    if "genres" in df.columns:
        df["genres"] = df["genres"].fillna("").apply(
            lambda x: [g.strip() for g in x.split(",")] if x else []
        )

    # actors: строка → список
    if "actors" in df.columns:
        df["actors"] = df["actors"].fillna("").apply(
            lambda x: [a.strip() for a in x.split(",")] if x else []
        )

    # Удаляем дубликаты по url
    if "url" in df.columns:
        df = df.drop_duplicates(subset="url")

    # Удаляем строки без названия или рейтинга
    df = df.dropna(subset=["title", "rating"])

    return df.reset_index(drop=True)

# ───────────────────────────────────────────────
# Основной процесс
def main():
    os.makedirs(CLEAN_DIR, exist_ok=True)

    for raw_name, clean_name in FILES.items():
        raw_path = os.path.join(RAW_DIR, raw_name)
        clean_path = os.path.join(CLEAN_DIR, clean_name)

        if not os.path.isfile(raw_path):
            print(f"[!] Файл не найден: {raw_path} — пропускаем.")
            continue

        print(f"→ Обрабатываем: {raw_name}")
        df_raw = pd.read_csv(raw_path)
        df_clean = clean_dataframe(df_raw)
        df_clean.to_csv(clean_path, index=False, encoding="utf-8")
        print(f"✓ Сохранено: {clean_name} ({len(df_clean)} строк)\n")

# ───────────────────────────────────────────────
if __name__ == "__main__":
    main()
