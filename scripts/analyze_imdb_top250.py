"""
Анализ IMDb Top‑250: числовые распределения, жанры, страны, актёры и гипотезы.

Запускается после подготовки данных:
    python scripts/clean_imdb_top250.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, ttest_ind, kruskal

sns.set_theme(font_scale=1.1)
plt.style.use("default")

# Загрузка данных
df = pd.read_csv("../data/clean/imdb_top250_full_clean.csv")

# ───────────────────────────────────────────────────────
# Первичный EDA
# ───────────────────────────────────────────────────────

# info, describe, пропуски
print(df.info())
print(df.describe())
print(df.isna().sum())

# Гистограммы распределений
df[["rating", "votes", "duration_min", "year"]].hist(
    bins=30, figsize=(12, 8), layout=(2, 2)
)
plt.tight_layout()
plt.show()

# ───────────────────────────────────────────────────────
# Частотный анализ жанров и стран
# ───────────────────────────────────────────────────────

# Частоты жанров (explode → value_counts)
df["genres"] = df["genres"].apply(lambda x: eval(x) if isinstance(x, str) else [])
genres_exploded = df.explode("genres")
print(genres_exploded["genres"].value_counts().head(10))

# Частоты стран
print(df["country"].value_counts().head(10))

# ───────────────────────────────────────────────────────
# Гипотеза 1: Больше голосов → выше рейтинг
# ───────────────────────────────────────────────────────
r, p = pearsonr(df["votes"], df["rating"])
print(f"[Гипотеза 1] Корреляция rating и votes: r = {r:.2f}, p = {p:.2e}")

# ───────────────────────────────────────────────────────
# Гипотеза 2: Голоса у фильмов из США выше
# ───────────────────────────────────────────────────────
df["is_USA"] = np.where(df["country"] == "United States", "USA", "Other")
usa_votes = df[df["is_USA"] == "USA"]["votes"]
other_votes = df[df["is_USA"] == "Other"]["votes"]
t_stat, p_val = ttest_ind(usa_votes, other_votes, equal_var=False)
print(f"[Гипотеза 2] Средние: USA = {usa_votes.mean():,.0f}, Other = {other_votes.mean():,.0f}")
print(f"[Гипотеза 2] t = {t_stat:.2f}, p = {p_val:.2e}")

# ───────────────────────────────────────────────────────
# Гипотеза 3: Старые фильмы оцениваются выше
# ───────────────────────────────────────────────────────
year_rating = df.dropna(subset=["year"])[["year", "rating"]]
r_year, p_year = pearsonr(year_rating["year"], year_rating["rating"])
print(f"[Гипотеза 3] Корреляция года и рейтинга: r = {r_year:.2f}, p = {p_year:.2e}")

# ───────────────────────────────────────────────────────
# Гипотеза 4: Content Rating влияет на оценку
# ───────────────────────────────────────────────────────
rating_map = {
    "G": "child", "PG": "child", "0+": "child", "6+": "child",
    "PG-13": "teen", "12+": "teen", "14+": "teen",
    "R": "adult", "NC-17": "adult", "16+": "adult", "18+": "adult",
}
df["age_group"] = df["content_rating"].map(rating_map).fillna("other")
df_age = df[df["age_group"].isin(["child", "teen", "adult"])]

groups = [df_age[df_age["age_group"] == g]["rating"] for g in ["child", "teen", "adult"]]
stat, pval = kruskal(*groups)
means = df_age.groupby("age_group")["rating"].mean()
print("[Гипотеза 4] Средние рейтинги по группам:")
print(means)
print(f"[Гипотеза 4] Kruskal-Wallis: H = {stat:.2f}, p = {pval:.4f}")
