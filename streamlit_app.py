import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Aatoksen ja Villen Forssa-Peli", page_icon="🚜", layout="wide"
)

st.title("🚜 Aatoksen ja Villen Forssa-Peli: Raviradan Kunnossapito 🚛")
st.caption(
    "Aatoksen ja Villen tekemä peli: Ohjaa punaisella vesiautolla Forssan raviradalla, kastele rata ja väistä 3 punaista traktoria!"
)

# HTML5 & JavaScript Canvas -pelikoodi
game_html = """
