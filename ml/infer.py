# ml/infer.py
import pandas as pd
import joblib
from ml.features import add_features

def load_model(path='models/exo_lr.pkl'):
    """Loads the trained sklearn pipeline and its feature list from a pickle file."""
    obj = joblib.load(path)
    return obj['model'], obj['features']

def score_all(df: pd.DataFrame, model, feat_columns):
    """Computes p_hab for all rows using the model (after feature engineering) 
    and returns df sorted by p_hab desc.
    """
    D = add_features(df)
    X = D[feat_columns].to_numpy(dtype=float)
    proba = model.predict_proba(X)
    pos_idx = list(model.named_steps["clf"].classes_).index(1)
    p = proba[:, pos_idx]
    out = df.copy()
    out["p_hab"] = p
    return out.sort_values("p_hab", ascending=False)