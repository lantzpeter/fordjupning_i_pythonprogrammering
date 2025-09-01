import pandas as pd
import logging
from etl.config import NASA_API_URL

logger = logging.getLogger(__name__)

def extract_data():
    """ Extracts exoplanet data from the NASA API.

    Returns:
        pd.DataFrame: DataFrame with result.

    Raises:
        Exception: If the extraction or parsing fails.
    """
    logger.info('Starting data extraction from NASA API: %s', NASA_API_URL)

    try:
        data = pd.read_csv(NASA_API_URL) # Saving the extracted data for later use.
        logger.info('Successfully extracted %d rows and %d cols', len(data), len(data.columns))

        if len(data) == 0:
            logger.warning("No rows returned")

        return data
    
    except Exception as e:
        logger.exception('Data extraction failed')
        raise