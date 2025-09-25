# ml/report.py
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from urllib.parse import quote

def _safe_name(name: str) -> str:
    """ 
    Return a filesystem-safe version of a planet name:
    keep alphanumerics, space, '-' and '_'; replace others with '_'.
    """
    return ''.join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in name).strip()

def export_planet_pdf(row: pd.Series, population: pd.DataFrame, out_path: str):
    """
    Export a one-page PDF report for a planet: header + key fields table,
    population p_hab histogram (with marker), and radius–mass scatter.
    
    Parameters:
    row : pd.Series
        Single planet row with fields (e.g., pl_name, p_hab, pl_rade, ...).
    population : pd.DataFrame
        Scored dataset used for context plots (must include 'p_hab').
    out_path : str
        Destination file path for the PDF.
    """
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    # Initialize
    with PdfPages(out_path) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        # Creating header for the pdf.
        ax = fig.add_axes([0.08, 0.75, 0.84, 0.2]); ax.axis('off')
        ax.text(0, 0.8, f"Planet: {row['pl_name']}", fontsize=16, weight='bold',
                 transform=ax.transAxes, ha='left', va='center')
        p = float(np.clip(row['p_hab'], 1e-3, 1-1e-3))
        ax.text(0, 0.5, f'Predicted habitability prob: {p:.3f}', fontsize=12,
                 transform=ax.transAxes, ha='left', va='center')

        # Creating a table to print values in a nice order.
        cols = ['pl_rade', 'pl_bmasse', 'pl_orbper', 'pl_orbsmax', 'pl_insol', 'st_teff', 'st_rad', 'disc_year']
        vals = [row.get(c, np.nan) for c in cols]
        ax2 = fig.add_axes([0.08, 0.58, 0.84, 0.12]); ax2.axis('off')
        table = ax2.table(cellText=[[c, f'{v}'] for c, v in zip(cols, vals)],
                          colLabels=['Field', 'Value'], loc='center')
        table.scale(1, 1.2)

        # Distribution of p_hab
        ax3 = fig.add_axes([0.08, 0.35, 0.84, 0.18])
        vals = population['p_hab'].dropna().to_numpy()
        ax3.hist(vals, bins=40, range=(0, 1), alpha=0.7)
        ax3.axvline(float(np.clip(row['p_hab'], 0, 1)), linestyle='--')
        ax3.set_xlabel('Predicted habitability probability'); ax3.set_ylabel('Count')
        ax3.set_xlim(0, 1)

        # Scatter plot: radius vs mass
        ax4 = fig.add_axes([0.08, 0.08, 0.84, 0.22])
        m = population[['pl_rade','pl_bmasse']].dropna()
        ax4.scatter(m['pl_rade'], m['pl_bmasse'], s=10, alpha=0.3)
        if np.isfinite(row.get('pl_rade')) and np.isfinite(row.get('pl_bmasse')):
            ax4.scatter([row['pl_rade']],[row['pl_bmasse']], marker='x', s=60, zorder=3)
        ax4.set_xlabel('Radius (R⊕)'); ax4.set_ylabel('Mass (M⊕)')
        ax4.scatter([1],[1], marker='+', s=80)  # Earth

        
        overview = f"https://exoplanetarchive.ipac.caltech.edu/overview/{quote(str(row['pl_name']))}"
        ax.text(0, 0.15, 'More info (Exoplanet Archive)', fontsize=10,
        url=overview, transform=ax.transAxes)  # Clickable link in PDF


        pdf.savefig(fig); plt.close(fig)

def export_topk_pdfs(scored: pd.DataFrame, k=10, outdir='artifacts/reports'):
    """Exports one-page PDF reports for the top-k planets by p_hab into outdir."""
    Path(outdir).mkdir(parents=True, exist_ok=True)
    topk = scored.head(k)
    for _, r in topk.iterrows():
        name = _safe_name(str(r['pl_name']))
        export_planet_pdf(r, scored, f'{outdir}/{name}.pdf')