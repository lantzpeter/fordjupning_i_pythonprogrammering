# etl/config.py
# URL for the NASA Exoplanet Archive TAP query (returns CSV).
NASA_API_URL = 'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,pl_rade,pl_insol,pl_bmasse,pl_orbper,pl_orbsmax,pl_eqt,st_teff,st_rad,disc_year+from+pscomppars&format=csv'