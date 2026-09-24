# 🌿 India AQI Business Intelligence Dashboard

A lightweight, single-file Business Intelligence dashboard built with **Streamlit** and **Pandas** to explore Air Quality Index (AQI) data across Indian states and cities.

---

## 📊 Features

- **Data Loading & Cleaning** — Automatically handles missing values, coerces numeric columns, and normalises column names.
- **4 Key Metrics**
  - Most polluted state (by average pollutant level)
  - City with the highest absolute pollutant spike
  - Most prominent pollutant nationwide
  - Overall average pollutant level
- **2 Interactive Charts**
  - Bar chart — Top 5 most polluted states by average pollutant level
  - Pie chart — Distribution of pollutant types across all readings
- **Sidebar Filters** — Drill down by state and/or pollutant type in real time.
- **Raw Data Preview** — Expandable table showing the first 100 rows of the filtered dataset.

---

## 🗂️ Project Structure

```
project/
├── app.py              # Single-file Streamlit dashboard
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── Data Export.csv     # AQI dataset (place here before running)
```

---

## 📦 Dataset

Download the dataset from Kaggle and place it in the project root as **`Data Export.csv`**.

> 🔗 **Dataset:** https://www.kaggle.com/datasets/yashdogra/aqi-india

**Expected columns:**

| Column | Description |
|---|---|
| `country` | Country name |
| `state` | Indian state |
| `city` | City name |
| `station` | Monitoring station name |
| `last_update` | Timestamp of last reading |
| `latitude` | Station latitude |
| `longitude` | Station longitude |
| `pollutant_id` | Pollutant identifier (e.g. PM2.5, NO2) |
| `pollutant_min` | Minimum recorded value (µg/m³) |
| `pollutant_max` | Maximum recorded value (µg/m³) |
| `pollutant_avg` | Average recorded value (µg/m³) |

---

## ⚙️ Setup & Installation

### 1. Clone / download the project

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place `AQI data.csv` in the same directory as `app.py`.

### 5. Run the dashboard

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web frontend & interactivity |
| [Pandas](https://pandas.pydata.org) | Data loading, cleaning & aggregation |
| [Matplotlib](https://matplotlib.org) | Chart rendering |

---

## 📝 License

This project is open-source and free to use for educational and personal purposes.
