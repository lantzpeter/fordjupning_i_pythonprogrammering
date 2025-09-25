# ml/data.py
import logging
import pandas as pd
from etl.db import get_engine

logger = logging.getLogger(__name__)

SELECT_SQL = """
SELECT
    pl_name,
    CAST(pl_rade AS REAL) AS pl_rade,
    CAST(pl_insol AS REAL) AS pl_insol,
    CAST(pl_bmasse AS REAL) AS pl_bmasse,
    CAST(pl_orbsmax AS REAL) AS pl_orbsmax,
    CAST(pl_orbper AS REAL) AS pl_orbper,
    CAST(pl_eqt AS REAL) AS pl_eqt,
    CAST(st_teff AS REAL) AS st_teff,
    CAST(st_rad AS REAL) AS st_rad,
    CAST(disc_year AS INTEGER) AS disc_year
    FROM exo_planets
"""

def load_exoplanets() -> pd.DataFrame:
    """
    Load the curated exoplanet snapshot from the local database.

    Returns:
    pd.DataFrame
        Columns: pl_name (str), pl_rade, pl_bmasse, pl_orbsmax, pl_orbper,
        pl_eqt, st_teff, st_rad (floats via SQL CAST), and disc_year (int/nullable).

    Notes:
    Uses etl.db.get_engine(); set the DB_URL env var to override the default SQLite path.
    This function only reads data and does not modify the database.

    Example:
    >>> df = load_exoplanets()
    >>> df.shape
    """
    df = pd.read_sql_query(SELECT_SQL, get_engine())
    logger.info('Loaded %d rows and %d columns', *df.shape)
    return df