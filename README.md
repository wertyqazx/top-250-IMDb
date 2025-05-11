# IMDb Top‑250 • Data Pipeline & EDA

Анализируем список IMDb Top‑250, чтобы понять:

* какие жанры, годы и страны чаще всего попадают в топ;
* как связаны рейтинг, число голосов, длительность;
* почему одни фильмы оказываются выше других.

---

## 📁 Структура репозитория
```
.
├── scripts/
│   ├── get_imdb_top250.py        # парсер (basic / full)
│   └── clean_imdb_top250.py      # очистка raw → clean
├── data/
│   ├── raw/                      # результаты скрапинга (.csv)
│   └── clean/                    # очищенные датасеты
├── notebooks/
│   └── analysis.ipynb            # EDA и визуализации
├── requirements.txt              # зависимости
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

1. **Скрапинг**

   ```bash
   # быстрый (без года/страны/актёров)
   python scripts/get_imdb_top250.py

   # полный (год, страна, актёры, ~5‑10 мин)
   python scripts/get_imdb_top250.py --deep
   ```

   *Файлы появятся в `data/raw/`
   — `imdb_top250_basic.csv` или `imdb_top250_full.csv`.*

2. **Очистка**

   ```bash
   python scripts/clean_imdb_top250.py
   ```

   Результат сохранится в `data/clean/`
   — `*_clean.csv` с приведёнными типами и списками.

3. **Анализ**

   Открыть Jupyter‑ноутбук:

   ```bash
   jupyter lab
   ```

   и запустить `notebooks/analysis.ipynb`
   (или просто «Run All»).

---

## ✍️ Автор(ы)

*Data Pipeline:* **Имя A**  
*EDA & Visuals:* **Имя B**
