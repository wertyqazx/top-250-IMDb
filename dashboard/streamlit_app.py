import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="IMDb Top-250 Dashboard", layout="wide")

# Загрузка данных
df = pd.read_csv("../data/clean/imdb_top250_full_clean.csv")

# Преобразуем жанры из строки в список
df["genres"] = df["genres"].apply(lambda x: eval(x) if isinstance(x, str) else [])

# Заголовок
st.title("🎬 IMDb Top‑250 Dashboard")
st.markdown("Интерактивный обзор ключевых характеристик топ‑250 фильмов IMDb.")

# Фильтрация по жанрам
all_genres = sorted({g for sublist in df["genres"] for g in sublist})
selected_genre = st.sidebar.selectbox("Выберите жанр", ["Все"] + all_genres)

if selected_genre != "Все":
    df = df[df["genres"].apply(lambda gs: selected_genre in gs)]

# Колонки: топ стран и средний рейтинг по годам
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 Топ-10 стран по числу фильмов")
    top_countries = df["country"].value_counts().head(10)
    st.bar_chart(top_countries)

with col2:
    st.subheader("📅 Средний рейтинг по годам")
    df_year = df.dropna(subset=["year"]).groupby("year")["rating"].mean()
    st.line_chart(df_year)

# Scatterplot: votes vs rating
st.subheader("📊 Зависимость рейтинга от числа голосов")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="votes", y="rating", ax=ax)
ax.set_xscale("log")
ax.set_xlabel("Число голосов (log)")
ax.set_ylabel("Рейтинг")
st.pyplot(fig)
