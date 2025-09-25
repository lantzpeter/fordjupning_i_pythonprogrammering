# Exoplanets

## Description
This project builds a complete end-to-end workflow for working with exoplanet data from the NASA Exoplanet Archive.
It starts with an ETL pipeline that fetches the latest data, transforms selected numeric fields, and stores the results in a local SQLite database.

The cleaned data is then processed through a machine learning pipeline that trains a logistic regression model to predict whether an exoplanet could be potentially habitable. Model artifacts, metrics, and plots are stored for reproducibility and further analysis.

Finally, the trained model is integrated into a Streamlit app, where users can explore top-K candidate planets, filter by probability thresholds, and view details for individual planets. Each planet’s profile can be exported as a one-page PDF report, and direct links to the NASA Exoplanet Archive are provided for further information.

## Installation
1. Clone this repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/WSL
   .venv\Scripts\activate      # Windows

## Install dependencies
pip install -r requirements.txt

## Usage
### Run ETL (extract + transform + load):
python -m etl.main

### Train the model:
python -m ml.train

### Generate PDF reports:
python -m ml.predict --top 5
python -m ml.predict --planet "Kepler-186 f"

### Start the Streamlit app:
streamlit run app/app.py

### Or schedule automatic runs using Windows Task Scheduler with WSL:
wsl bash -c "cd /path/to/exoplanets && source .venv/bin/activate && python -m etl.main"

## Project structure
data/ – contains the SQLite database (created automatically)
logs/ – log files from each run
etl/ – ETL modules (extract, transform, logging, orchestration)
ml/ – ML modules (features, training, inference, reporting)
app/ – Streamlit app for exploration and PDF export
artifacts/ – metrics, plots, predictions, and generated reports
models/ – trained model files
eda/ – Jupyter notebooks for exploratory analysis
requirements.txt – dependencies (pandas, scikit-learn, streamlit, sqlalchemy, joblib, etc.)
README.md – project description and instructions

## Directory tree

```text

exoplanets/
├── README.md
├── requirements.txt                # or pyproject.toml if you use 'pip install -e .'
├── app/
│   └── app.py                      # Streamlit app
├── artifacts/                      # training artifacts and prediction files
│   ├── metrics.json
│   ├── pr.png
│   ├── roc.png
│   ├── all_predictions.csv
│   └── reports/                    # PDF reports (generated on export)
├── data/                           # SQLite database
│   └── exoplanets.db
├── eda/                            # Jupyter notebooks for exploratory analysis
│   └── EDA.ipynb
├── etl/                            # ETL package
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── extract.py
│   ├── logging_conf.py
│   ├── main.py
│   └── transform.py
├── logs/                           # log files (logs.log.)
├── ml/                             # Machine Learning package
│   ├── __init__.py
│   ├── config.py                   # thresholds / reference values for features/label
│   ├── data.py                     # read data from SQLite
│   ├── features.py                 # add_features(), make_label(), FEATURES
│   ├── infer.py                    # load_model(), score_all()
│   ├── plots.py                    # save_pr_roc()
│   ├── predict.py                  # CLI for PDF / Top-K predictions
│   ├── report.py                   # export_planet_pdf(), export_topk_pdfs()
│   └── train.py                    # training + save model/metrics/plots
├── models/                         # trained models (e.g. exo_lr.pkl)
└── .gitignore                      # exclude .venv, data/, artifacts/, logs/, etc.

```

## Flow:
- ETL: Extract from NASA API → Transform numerics → Load into SQLite (data/exoplanets.db)
- ML: Feature engineering → Train/test split → Logistic regression → Save model (models/exo_lr.pkl) → Save metrics + plots (artifacts/)
- Prediction & Reports: Predict probabilities, export one-page PDF reports (artifacts/reports/)
- App: Streamlit interface with filters, Top-K selection, planet details, NASA links, and PDF download.

## Notes
- data/exoplanets.db is created the first time the pipeline runs.
- Logs stored in logs/logs.log
- Metrics (metrics.json) and plots (pr.png, roc.png) stored in artifacts/
- Model retraining overwrites files in models/