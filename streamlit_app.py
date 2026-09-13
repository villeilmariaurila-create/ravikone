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


@st.cache_data
def get_game_code():
    url = "https://gist.githubusercontent.com/raw/d8b8a536fb1907cbcf61665e7ce00a0e/raw/forssa_game.html"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")


html_code = get_game_code()
components.html(html_code, height=630)
