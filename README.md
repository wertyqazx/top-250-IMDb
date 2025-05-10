# IMDb Top‑250 Analysis

This repository contains code and data for the project:

**Goal**  
Analyse the IMDb Top‑250 list to understand which genres, years and countries are most represented, how ratings and vote counts are distributed, and what patterns characterise films that make it into the top.

## Structure
```
.
├── scripts/               # scraping & utility scripts
├── data/
│   ├── raw/               # raw scraped CSV
│   └── clean/             # cleaned dataset
├── notebooks/             # Jupyter notebooks with EDA and analysis
├── dashboard/             # (optional) Streamlit/Dash app
├── requirements.txt       # python dependencies
└── README.md              # this file
```

## Setup

```bash
python -m venv venv
source venv/bin/activate   # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

```bash
python scripts/get_imdb_top250.py --output data/raw/imdb_top250_raw.csv --deep
```

After scraping, open `notebooks/analysis.ipynb` and run all cells to reproduce the figures.

## Author
*Yakovlev Oleg 413120, Yakovlev Stepan 468173*
