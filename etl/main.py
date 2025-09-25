# etl/main.py
import logging
import sqlite3
from etl.extract import extract_data
from .logging_conf import setup_logger
from .transform import transform

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    logger.addHandler(setup_logger())


def main():
    # Extract
    data = extract_data()
   
    # Transform
    data = transform(data)
    logger.info("Transformation complete, shape: %s", data.shape)

    # Load - Save to SQlite3 table.
    con = sqlite3.connect('data/exoplanets.db')
    data.to_sql('exo_planets', con, if_exists='replace', index=False )
    logger.info("Saved %d rows into SQLite table 'exo_planets'", len(data))
    con.close()

if __name__ == "__main__":
    main()