import urllib.request
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Aatoksen ja Villen Forssa-Peli", page_icon="🚜", layout="wide"
)

st.title("🚜 Aatoksen ja Villen Forssa-Peli: Raviradan Kunnossapito 🚛")
st.caption(
    "Aatoksen ja Villen tekemä peli: Ohjaa punaisella vesiautolla Forssan raviradalla, kastele rata ja väistä 3 punaista traktoria!"
)

# Hae HTML-pelikoodi ulkoisesta osoitteesta (vältetään heittomerkki- ja syntaksivirheet)
url = "https://gist.githubusercontent.com/raw/d8b8a536fb1907cbcf61665e7ce00a0e/raw/forssa_game.html"


@st.cache_data
def load_game():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8")
    except Exception:
        return """
