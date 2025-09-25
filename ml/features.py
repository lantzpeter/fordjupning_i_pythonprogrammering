# ml/features.py
import numpy as np
import pandas as pd
from ml.config import HZ_MIN, HZ_MAX, ROCKY_R_MAX, STAR_T_MIN, STAR_T_MAX

FEATURES = [
    'pl_rade', 'pl_bmasse', 'pl_orbper', 'pl_orbsmax',
    'st_teff', 'st_rad', 'pl_insol', 'rho_e', 'log_orbper', 'log_a'
]

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a few derived features (e.g., rho_e, log_orbper, log_a) without touching the input.
    Returns a copy with the extra columns.
    """
    d = df.copy()
    d['rho_e'] = d['pl_bmasse'] / (d['pl_rade']**3)  # density proxy (M/R^3)

    # safe log10: values <= 0 become NaN
    d['log_orbper'] = np.log10(d['pl_orbper'].where(d['pl_orbper'] > 0))
    d['log_a']      = np.log10(d['pl_orbsmax'].where(d['pl_orbsmax'] > 0))
    return d

def make_label(df: pd.DataFrame) -> pd.Series:
    """
    Create a simple 0/1 habitable proxy (pl_insol in [0.35,1.5], pl_rade ≤ 1.6, st_teff in [2600,7200]).
    Returns an index-aligned Series.
    """
    need    = df[['pl_rade', 'pl_insol', 'st_teff']].notna().all(axis=1)
    in_hz   = df['pl_insol'].between(HZ_MIN, HZ_MAX)
    rocky   = df['pl_rade'] <= ROCKY_R_MAX
    ok_star = df['st_teff'].between(STAR_T_MIN, STAR_T_MAX)
    return (in_hz & rocky & ok_star & need).astype(int)

def make_xy(df: pd.DataFrame):
    """
    Build X and y for modeling: add_features(df) → y via make_label(df) → select FEATURES into X (float).
    Returns (X, y).
    """
    d = add_features(df)
    y = make_label(d).to_numpy()
    X = d[FEATURES].to_numpy(dtype=float)
    return X, y
