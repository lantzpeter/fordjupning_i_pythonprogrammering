import logging

logger = logging.getLogger(__name__)

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
    
def transform(df):
    """Apply the transformation to the whole DataFrame"""
    
    numeric_columns = ['pl_rade', 'pl_bmasse', 'disc_year']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(to_float)
            logger.info('Transformed column %s', col)
        else:
            logger.warning('Column %s not found in DataFrame', col)
    
    return df