import streamlit as st
import streamlit.components.v1 as components
components.html(open("game.html", encoding="utf-8").read(), height=600)
