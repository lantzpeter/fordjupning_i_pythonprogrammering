# ml/plots.py
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend (no display needed); enables saving figures in headless environments.
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay
import logging

log = logging.getLogger(__name__)

def save_pr_roc(y_true, y_score, outdir='artifacts'):
    """
    Save Precision–Recall and ROC curves as pr.png and roc.png in outdir.
    """
    Path(outdir).mkdir(exist_ok=True)

    # PR
    fig_pr, ax_pr = plt.subplots()
    PrecisionRecallDisplay.from_predictions(y_true, y_score, ax=ax_pr)
    pr_path = f'{outdir}/pr.png'
    fig_pr.savefig(pr_path, dpi=150, bbox_inches='tight')
    plt.close(fig_pr)

    # ROC
    fig_roc, ax_roc = plt.subplots()
    RocCurveDisplay.from_predictions(y_true, y_score, ax=ax_roc)
    roc_path = f'{outdir}/roc.png'
    fig_roc.savefig(roc_path, dpi=150, bbox_inches='tight')
    plt.close(fig_roc)

    log.info('Saved PR/ROC: %s , %s', pr_path, roc_path)