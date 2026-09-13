import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Aatoksen ja Villen Forssa-Peli", page_icon="🚜", layout="wide"
)

st.title("🚜 Aatoksen ja Villen Forssa-Peli: Raviradan Kunnossapito 🚛")
st.caption(
    "Ohjaa vesiautoa nuolinäppäimillä tai WASD:lla. Kastele rata ja väistä traktoreita!"
)

game_html = """
