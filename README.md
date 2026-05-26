# CTR Prediction — Ads ML Project

Click-through rate (CTR) prediction model for ads. Trains and compares Logistic
Regression and XGBoost classifiers on synthetic ad click data.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

This executes the full pipeline in four steps:

| Step | Description |
|------|-------------|
| 1 | Generate 10,000 rows of synthetic ad click data |
| 2 | One-hot encode categorical features, save X/y to disk |
| 3 | Train Logistic Regression (StandardScaler + L2) |
| 4 | Train XGBoost (n_estimators=100, max_depth=4) |

## Model Results

| Model | AUC-ROC |
|-------|---------|
| Logistic Regression | 0.7138 |
| XGBoost | 0.7215 |

## Folder Structure

```
ml-project/
├── main.py                  # Pipeline orchestrator — run this
├── requirements.txt
├── data/
│   ├── raw/                 # Source data — never modify, never commit
│   └── processed/           # ctr_data.csv, X.csv, y.csv (generated)
├── models/
│   ├── ctr_model.pkl        # Logistic regression pipeline
│   └── ctr_xgboost.pkl      # XGBoost pipeline
├── src/
│   ├── data_generator.py    # Synthetic CTR data generation
│   ├── features.py          # OHE encoding, save X/y
│   ├── evaluate.py          # Shared evaluation utilities (AUC, confusion matrix, importances)
│   ├── train.py             # Logistic regression training
│   └── train_xgboost.py     # XGBoost training
├── notebooks/               # EDA and prototyping
└── experiments/             # Experiment configs and results
```

## Features

Input features after one-hot encoding (drop_first=True):

- `user_age` — integer, 18–64
- `user_gender_M`, `user_gender_Other`
- `ad_category_electronics`, `_fashion`, `_food`, `_sports`, `_travel`
- `time_of_day_evening`, `_morning`, `_night`
- `device_type_mobile`, `_tablet`
