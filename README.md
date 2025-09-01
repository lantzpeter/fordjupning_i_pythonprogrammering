# ETL Exoplanets

## Description
This project implements a simple ETL pipeline that fetches exoplanet data from the NASA Exoplanet Archive, 
transforms selected numeric fields, and stores the results in a local SQLite database.  
The pipeline is automated via Windows Task Scheduler (WSL) and logs each run to a dedicated log file.

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
### Run the pipeline manually:
python -m etl.main

### Or schedule automatic runs using Windows Task Scheduler with WSL:
wsl bash -c "cd /path/to/etl_exoplanets && source .venv/bin/activate && python -m etl.main"

## Testing
### Run unit tests with pytest:
pytest -q

## Project structure
data/ – contains the SQLite database (created automatically)
logs/ – log files from each run
etl/ – ETL modules (extract, transform, logging, orchestration)
tests/ – pytest unit tests for extract/transform
requirements.txt – dependencies (pandas, pytest)
README.md – project description and instructions

## Directory tree
etl_exoplanets/
├── README.md                # Project description and instructions
├── requirements.txt         # Python dependencies (pandas, pytest)
├── data/                    # For database and optional sample files
│   └── exoplanets.db        # SQLite database (created automatically)
├── logs/                    # Log files (logs.log)
├── etl/                     # ETL package
│   ├── __init__.py
│   ├── config.py            # Configuration (API URL etc.)
│   ├── extract.py           # Extract: fetches data from NASA API
│   ├── transform.py         # Transform: converts and cleans data
│   ├── logging_conf.py      # Logger setup
│   └── main.py              # Orchestrates the full ETL pipeline
└── tests/                   # Pytest unit tests
    ├── conftest.py
    ├── test_extract.py
    ├── test_transform.py
    └── test_transform_columns.py

## Notes
- data/exoplanets.db is created the first time the pipeline runs.

- logs/logs.log is updated with each execution, including extraction, transformation, and loading steps.