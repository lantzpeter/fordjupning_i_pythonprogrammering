# ml/predict.py
import argparse
import logging
import pandas as pd
from ml.data import load_exoplanets
from ml.infer import load_model, score_all
from ml.report import export_planet_pdf, export_topk_pdfs
from etl.logging_conf import setup_logger

logger = logging.getLogger('ml.predict' if __name__ == '__main__' else __name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    logger.addHandler(setup_logger())

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--planet', type=str, help='Exact planet name for one PDF.')
    p.add_argument('--top', type=int, default=0, help='Export top-k PDFs by probability.')
    p.add_argument('--model', type=str, default='models/exo_lr.pkl')
    args = p.parse_args()

    df = load_exoplanets()
    model, feats = load_model(args.model)
    scored = score_all(df, model, feats)

    if args.planet:
        row = scored.loc[scored['pl_name'] == args.planet]
        if row.empty:
            logger.error('Planet not found: %s', args.planet); return
        export_planet_pdf(row.iloc[0], scored, f"artifacts/reports/{args.planet}.pdf")
        logger.info("Saved artifacts/reports/%s.pdf", args.planet)
    elif args.top and args.top > 0:
        export_topk_pdfs(scored, k=args.top, outdir='artifacts/reports')
        logger.info("Saved %d PDFs under artifacts/reports/", args.top)
    else:
        scored[["pl_name","p_hab"]].to_csv("artifacts/all_predictions.csv", index=False)
        logger.info("Saved artifacts/all_predictions.csv")
    
if __name__ == '__main__':
    main()