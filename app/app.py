import streamlit as st
import pandas as pd
from ml.data import load_exoplanets
from ml.infer import load_model, score_all
from ml.report import export_planet_pdf
import tempfile
from pathlib import Path
from urllib.parse import quote

# --Cache--
@st.cache_resource
def get_model():
    return load_model() # Returns model and features

@st.cache_data
def get_data():
    return load_exoplanets() # Loads and cach data.
    
@st.cache_data
def get_scored(df: pd.DataFrame, feature_names: tuple) -> pd.DataFrame:
    return score_all(df, model, list(feature_names)) # Returns df with 'p_hab'

# --Load--
model, features = get_model()
data = get_data()
scored = get_scored(data, tuple(features))

# --Sidebar--
st.sidebar.header('Filters')
top_k = st.sidebar.number_input('Top-K', min_value=1, max_value=10, value=10, step=1)
min_prob = st.sidebar.slider('Min p_hab', 0.0, 1.0, 0.5, 0.001)

planet_opts = ['(none)'] + sorted(scored['pl_name'].astype(str).unique().tolist())
planet_name = st.sidebar.selectbox('Planet', options=planet_opts)

# filtering views to use in columns
scored_filtered = scored[scored['p_hab'] >= min_prob]
top_view = scored_filtered.nlargest(top_k, 'p_hab')

# setting up KPI's
c1, c2, c3 = st.columns(3)
c1.metric('Planets (filtered)', len(scored_filtered))
c2.metric('Top-k shown', len(top_view))
c3.metric('Average p_hab (filtered)', f"{scored_filtered['p_hab'].mean():.3f}" if len(scored_filtered) else '-')

# Table
st.subheader('Top candidates')
cols_to_show = ['pl_name', 'p_hab','pl_rade','pl_bmasse','pl_orbper','st_teff','disc_year']
exist_columns = [c for c in cols_to_show if c in top_view.columns]
st.dataframe(top_view[exist_columns].style.format({"p_hab": "{:.6f}"})
    if len(top_view) else pd.DataFrame()
)

# --Details--

if planet_name != '(none)':
    sel = scored.loc[scored['pl_name'].astype(str) == planet_name]
    if len(sel):
        row = sel.iloc[0]
        st.markdown('---')
        st.subheader(f"{row['pl_name']} — p_hab = {row['p_hab']:.6f} ({row['p_hab']:.2%})")

        # NASA link
        nasa_url = f"https://exoplanetarchive.ipac.caltech.edu/overview/{quote(str(row['pl_name']), safe='')}"
        st.markdown(f"[Open in NASA Exoplanet Archive]({nasa_url})")

        # Quick facts
        facts_cols = [c for c in ['pl_rade', 'pl_bmasse', 'pl_insol', 'pl_eqt', 'pl_orbper', 'st_teff', 'st_rad', 'disc_year'] if c in sel.columns]
        st.table(sel[facts_cols].round(3) if facts_cols else pd.DataFrame({'info':['no fields found']}))

        # PDF download (one planet)
        with tempfile.TemporaryDirectory() as td:
            outpath = Path(td) / 'report.pdf'
            export_planet_pdf(row, scored, str(outpath))
            pdf_bytes = outpath.read_bytes()
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{row['pl_name']}.pdf",
                mime="application/pdf",
            )
    else:
        st.warning('Selected planet not in current filtered set.')
elif len(scored_filtered) == 0:
    st.info('No rows match the current p_hab threshold. Lower it to see candidates.')