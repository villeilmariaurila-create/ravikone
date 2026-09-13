import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Forssa-Peli", layout="wide")

with open("game.html", "r", encoding="utf-8") as f:
    html_data = f.read()

components.html(html_data, height=600)
