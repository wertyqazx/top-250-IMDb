# IMDb Top‑250 • Data Pipeline & EDA

Проект по анализу списка IMDb Top‑250. Исследуем:

- какие жанры, страны и годы чаще представлены в топе;
- как связаны рейтинг, количество голосов, длительность;
- влияют ли возрастные ограничения и страна производства на популярность;
- какие закономерности можно выявить среди лучших фильмов.

---

## 📁 Структура проекта

```
.
├── data/
│   ├── raw/                      # результаты скрапинга (.csv)
│   └── clean/                    # очищенные версии датасетов
├── scripts/
│   ├── get_imdb_top250.py        # скрапинг с IMDb (basic или full)
│   ├── clean_imdb_top250.py      # очистка и типизация
│   └── analyze_imdb_top250.py    # сухой скрипт для EDA и гипотез
├── notebooks/
│   └── analysis.ipynb            # основной анализ и визуализация
├── dashboard/
│   └── streamlit_app.py          # интерактивный дэшборд (Streamlit)
├── requirements.txt              # зависимости проекта
└── README.md
```

---

## ⚙️ Установка

```bash
python -m venv venv
source venv/bin/activate     # Windows → .\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Как воспроизвести

### 1. Скрапинг данных

```bash
# базовая версия (быстро)
python scripts/get_imdb_top250.py

# расширенная версия (--deep, дольше, но с годами/странами/актёрами)
python scripts/get_imdb_top250.py --deep
```

> Результаты: `data/raw/imdb_top250_basic.csv` или `..._full.csv`

---

### 2. Очистка данных

```bash
python scripts/clean_imdb_top250.py
```

> Результат: `data/clean/imdb_top250_basic_clean.csv` и `..._full_clean.csv`

---

### 3. Анализ в ноутбуке

```bash
jupyter lab
```

> Открыть `notebooks/analysis.ipynb` и запустить все ячейки (или "Run All")

---

### 4. Дэшборд

```bash
streamlit run dashboard/streamlit_app.py
```

> Интерактивный фильтр по жанрам, графики по странам, рейтингам и голосам

---

## Авторы

_Data Pipeline:_ **Яковлев Олег 413120**  
_EDA & Visuals:_ **Яковлев Степан 468173**
