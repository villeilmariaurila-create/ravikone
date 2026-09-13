import random
import streamlit as st

st.set_page_config(
    page_title="Aatoksen ja Villen Forssa-Peli", page_icon="🚜", layout="centered"
)

st.title("🚜 Aatoksen ja Villen Forssa-Peli 🚛")
st.subheader("Raviradan kunnossapito")

# Alustetaan pelin tila
if "player_x" not in st.session_state:
    st.session_state.player_x = 2
    st.session_state.player_y = 4
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.game_over = False
    # Luodaan kastelupisteet radalle
    st.session_state.water_dots = [
        (1, 0),
        (2, 0),
        (3, 0),
        (0, 1),
        (4, 1),
        (0, 2),
        (4, 2),
        (0, 3),
        (4, 3),
        (1, 4),
        (3, 4),
    ]
    st.session_state.tractors = [(1, 1), (3, 2), (2, 0)]


def move_player(dx, dy):
    if st.session_state.game_over:
        return

    # Uusi sijainti
    new_x = max(0, min(4, st.session_state.player_x + dx))
    new_y = max(0, min(4, st.session_state.player_y + dy))
    st.session_state.player_x = new_x
    st.session_state.player_y = new_y

    # Siirretään traktoreita satunnaisesti
    new_tractors = []
    for tx, ty in st.session_state.tractors:
        tdx = random.choice([-1, 0, 1])
        tdy = random.choice([-1, 0, 1])
        nx = max(0, min(4, tx + tdx))
        ny = max(0, min(4, ty + tdy))
        new_tractors.append((nx, ny))
    st.session_state.tractors = new_tractors

    # Tarkistetaan törmäys traktoriin
    if (new_x, new_y) in st.session_state.tractors:
        st.session_state.lives -= 1
        st.toast("⚠️ Törmäsit traktoriin! Menetit elämän.", icon="💥")
        st.session_state.player_x = 2
        st.session_state.player_y = 4
        if st.session_state.lives <= 0:
            st.session_state.game_over = True
            return

    # Tarkistetaan veden keräys
    if (new_x, new_y) in st.session_state.water_dots:
        st.session_state.water_dots.remove((new_x, new_y))
        st.session_state.score += 10
        st.toast("💧 Kastelupiste kerätty! +10 pistettä", icon="🎉")

    # Jos kaikki vedet kerätty, täytetään rata uudelleen
    if len(st.session_state.water_dots) == 0:
        st.session_state.water_dots = [
            (1, 0),
            (2, 0),
            (3, 0),
            (0, 1),
            (4, 1),
            (0, 2),
            (4, 2),
            (0, 3),
            (4, 3),
            (1, 4),
            (3, 4),
        ]


def restart_game():
    st.session_state.player_x = 2
    st.session_state.player_y = 4
    st.session_state.score = 0
    st.session_state.lives = 3
    st.session_state.game_over = False
    st.session_state.water_dots = [
        (1, 0),
        (2, 0),
        (3, 0),
        (0, 1),
        (4, 1),
        (0, 2),
        (4, 2),
        (0, 3),
        (4, 3),
        (1, 4),
        (3, 4),
    ]
    st.session_state.tractors = [(1, 1), (3, 2), (2, 0)]


# Tilastot
col1, col2 = st.columns(2)
with col1:
    st.metric("💧 Kastelupisteet", st.session_state.score)
with col2:
    st.metric("❤️ Elämät", st.session_state.lives)

st.markdown("---")

if st.session_state.game_over:
    st.error(
        f"💥 PELI PÄÄTTYI! Aatoseksi ja Villeksi saavutitte {st.session_state.score} pistettä!"
    )
    st.button("🔄 Pelaa uudelleen", on_click=restart_game, type="primary")
else:
    # Piirretään pelikenttä (5x5 ruudukko)
    grid_html = "
