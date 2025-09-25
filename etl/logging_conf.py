# etl/logging_conf.py
import logging

def setup_logger():
    """Set up a logger.
    Create a FileHandler, add a Formatter and return the FileHandler. 
    """
    fh = logging.FileHandler("logs/logs.log")
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s][%(message)s]')

    fh.setFormatter(formatter)
    return fh