# ml/train.py
import numpy as np
from pathlib import Path
import json, logging, joblib
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score, average_precision_score

from etl.logging_conf import setup_logger
from ml.data import load_exoplanets
from ml.features import make_label, add_features, FEATURES
from ml.plots import save_pr_roc

logger = logging.getLogger( __name__)

def main():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not root.handlers:
        root.addHandler(setup_logger())

    data = load_exoplanets() #Raw data
    logger.info('Raw data %d×%d', *data.shape)
    D = add_features(data)
    y_all = make_label(D).to_numpy()

    # Splitting by index so i can connect with planet names later.
    idx = np.arange(len(data))
    train_idx, test_idx = train_test_split(idx, test_size=0.2, stratify=y_all, random_state=42)

    X_train = D.loc[train_idx, FEATURES].to_numpy(dtype=float); y_train = y_all[train_idx]
    X_test = D.loc[test_idx,  FEATURES].to_numpy(dtype=float); y_test = y_all[test_idx]

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    pipe = Pipeline([
        ('imp', SimpleImputer(strategy='median')),
        ('sc', StandardScaler()),
        ('clf', LogisticRegressionCV(
            Cs=10,
            cv=cv,
            scoring='roc_auc',
            class_weight="balanced",
            max_iter=1000,
            n_jobs=-1,
            solver='liblinear',
            refit=True
        ))
    ])

    pipe.fit(X_train, y_train)
    prob_test = pipe.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, prob_test)
    ap = average_precision_score(y_test, prob_test)
    logger.info('Test AUC=%.3f | AP=%.3f | pos=%d/%d', auc, ap, int(y_test.sum()), len(y_test))
    save_pr_roc(y_test, prob_test, outdir='artifacts')

    Path('models').mkdir(exist_ok=True)
    joblib.dump({'model': pipe, 'features': FEATURES}, 'models/exo_lr.pkl') # Saving model and features for later use.

    Path('artifacts').mkdir(exist_ok=True)
    with open('artifacts/metrics.json', 'w') as f:
        json.dump({'auc': float(auc), 'average_precision': float(ap)}, f)

if __name__ == '__main__':
    main()