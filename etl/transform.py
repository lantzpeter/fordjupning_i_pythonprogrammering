# etl/transform.py
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

#Creating a function to convert any numbers manually entered into float.
def to_float(number) -> float | None:
    """Converts data to float if sucessful, otherwise to None value
    """
    if number is None:
        logger.warning('Received None value for number')
        return None
    
    if isinstance(number, str):
        number = number.strip().replace(',', '.')
    
    try: 
        converted = float(number)
        logger.debug('Converted %s to %f', number, converted)
        return converted
    
    except (ValueError, TypeError) as e:
        logger.warning('Could not convert %s to float (%s)', number, e)
        return None

#Creating a function to catch all numbers in a DataFrame and ensure output is in float.    
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the transformation to the whole DataFrame"""
    
    df = df.copy() #creating a copy to use insted of the original one.
    exclude = {'pl_name', 'disc_year'}

    #If already numeric columns -> float64
    num = (df.select_dtypes(include=[np.number], exclude=['bool','boolean'])
             .columns.difference(exclude, sort=False))
    df[num] = df[num].astype('float64')
    logger.info('Cast to float64: %s', list(num))
    
    
    # If object/string → try convert to num
    obj = (df.select_dtypes(include=['object','string'])
             .columns.difference(exclude, sort=False))
    for c in obj:
        df[c] = pd.to_numeric(
            df[c].astype('string').str.strip().str.replace(",", ".", regex=False),
            errors='coerce'
        )
    if len(obj):
        logger.info('Parsed object → numeric: %s', list(obj))

    return df