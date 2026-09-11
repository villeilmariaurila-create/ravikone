import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI, KIINTEÄT KERTOIMET & GOOGLE SHEETS -SEURANTALINKKI
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Peliarvotyökalu", layout="wide")

# CSS-tyyli taulukon solujen sisällön rivittämiseen
st.markdown(
    """
    
    """,
    unsafe_allow_html=True
)

st.title("🎯 V85 Alle 10% Pelatut Yllättäjät & Google Sheets -seuranta")
st.caption("Työkalu hakee V85-kohteista (lähdöt 5–12) parhaat alle 10% pelatut yllättäjät. Taulukon tiedot ja seurantalinkit on keskitetty omaan Google Sheets -tiedostoon.")

# Linkki erilliseen Google Sheet -seurantatiedostoon
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"

st.markdown(
    f"""
