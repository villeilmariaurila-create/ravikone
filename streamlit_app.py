import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Aatoksen ja Villen Forssa-Peli", page_icon="🚜", layout="wide"
)

st.title("🚜 Aatoksen ja Villen Forssa-Peli: Raviradan Kunnossapito 🚛")
st.caption(
    "Ohjaa pientä punaista vesiautoa nuolinäppäimillä tai WASD:lla. Kastele hiekkarata sinisistä kastelupisteistä ja väistä traktoreita!"
)

# Luodaan peli HTML5 Canvas -muodossa
game_code = """
