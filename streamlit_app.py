import random
import streamlit as st

st.set_page_config(
    page_title="Aatoksen ja Villen Forssa-Peli", page_icon="🚜", layout="centered"
)

st.title("🚜 Aatoksen ja Villen Forssa-Peli 🚛")
st.caption("Ohjaa vesiautoa (🚛), kastele rata (💧) ja väistä traktoreita (🚜)!")

# Alustetaan pelin tila
if "player_x" not in st.session_state:
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


def move_player(dx, dy):
    if st.session_state.game_over:
        return

    # Liikutetaan pelaajaa
    new_x = max(0, min(4, st.session_state.player_x + dx))
    new_y = max(0, min(4, st.session_state.player_y + dy))
    st.session_state.player_x = new_x
    st.session_state.player_y = new_y

    # Liikutetaan traktoreita
    new_tractors = []
    for tx, ty in st.session_state.tractors:
        nx = max(0, min(4, tx + random.choice([-1, 0, 1])))
        ny = max(0, min(4, ty + random.choice([-1, 0, 1])))
        new_tractors.append((nx, ny))
    st.session_state.tractors = new_tractors

    # Törmäys traktoriin
    if (new_x, new_y) in st.session_state.tractors:
        st.session_state.lives -= 1
        st.toast("⚠️ Törmäsit traktoriin! Menetit elämän.", icon="💥")
        st.session_state.player_x = 2
        st.session_state.player_y = 4
        if st.session_state.lives <= 0:
            st.session_state.game_over = True
            return

    # Veden keräys
    if (new_x, new_y) in st.session_state.water_dots:
        st.session_state.water_dots.remove((new_x, new_y))
        st.session_state.score += 10
        st.toast("💧 Kastelupiste kerätty! +10 pistettä", icon="🎉")

    # Jos vesi loppuu, täytetään uudet pisarat
    if not st.session_state.water_dots:
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
col1.metric("💧 Kastelupisteet", st.session_state.score)
col2.metric("❤️ Elämät", st.session_state.lives)

st.markdown("---")

if st.session_state.game_over:
    st.error(
        f"💥 PELI PÄÄTTYI! Aatoksen ja Villen radalle keräämät pisteet: {st.session_state.score}"
    )
    st.button("🔄 Pelaa uudelleen", on_click=restart_game, type="primary")
else:
    # Piirretään pelikenttä Streamlit-sarakkeilla ilman HTML-koodia
    for y in range(5):
        cols = st.columns(5)
        for x in range(5):
            icon = "🟫"
            if (x, y) == (
                st.session_state.player_x,
                st.session_state.player_y,
            ):
                icon = "🚛"
            elif (x, y) in st.session_state.tractors:
                icon = "🚜"
            elif (x, y) in st.session_state.water_dots:
                icon = "💧"
            cols[x].markdown(f"### {icon}")

    st.markdown("---")

    # Ohjauspainikkeet
    c1, c2, c3 = st.columns([1, 1, 1])
    c2.button(
        "⬆️ Ylös",
        on_click=move_player,
        args=(0, -1),
        use_container_width=True,
    )

    c4, c5, c6 = st.columns([1, 1, 1])
    c4.button(
        "⬅️ Vasen",
        on_click=move_player,
        args=(-1, 0),
        use_container_width=True,
    )
    c5.button(
        "⬇️ Alas",
        on_click=move_player,
        args=(0, 1),
        use_container_width=True,
    )
    c6.button(
        "➡️ Oikea",
        on_click=move_player,
        args=(1, 0),
        use_container_width=True,
    )
