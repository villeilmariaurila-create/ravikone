import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Odotusarvot - Färjestad",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Odotusarvo- ja Simulaatiotyökalu (Kaikki 8 lähtöä)")
st.caption(
    "Färjestad – Päivitä Unibetin ja Coolbetin kertoimet taulukkoon klo 18 jälkeen."
)

# ----------------- SIVUPALKIN ASETUKSET -----------------
st.sidebar.header("⚙️ Pelin Asetukset")
panos_per_vihje = st.sidebar.number_input(
    "Panos per vihje (€)", min_value=1.0, value=10.0, step=1.0
)
osuma_raja_ev = st.sidebar.slider(
    "Suodata minimi EV-raja", 0.5, 2.0, 1.0, step=0.05
)
num_simulations = st.sidebar.selectbox(
    "Monte Carlo -simulaatiot", [1000, 5000, 10000, 50000], index=2
)

# ----------------- KAIKKI 8 LÄHTÖÄ & HEVOSET -----------------
vihjeet_data = [
    # --- V85-1 ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Arvio %": 55.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Selvä suosikki, Goopin luokkahevonen.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Arvio %": 10.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "💥 YLLÄTTÄJÄ: Ensimmäistä kertaa ilman kenkiä (barfota r/o).",
    },
    # --- V85-2 ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#4 Nilla Lane",
        "Peliprosentti": 35.0,
        "Arvio %": 34.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Suosikki, hakee keulapaikkaa.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "Urbina Southwind",
        "Peliprosentti": 2.0,
        "Arvio %": 5.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Pieni peliosuus (2%), potentiaalinen yllättäjä"
            " vauhdikkaan juoksun jälkeen[cite: 3]."
        ),
    },
    # --- V85-3 ---
    {
        "Kohde": "V85-3",
        "Hevonen": "Miss Magdalena",
        "Peliprosentti": 4.0,
        "Arvio %": 9.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ ('Super'): Erittäin mielenkiintoinen ja aliarvostettu"
            " tammalähdön haastaja[cite: 3]."
        ),
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#8 Ginevra Ek",
        "Peliprosentti": 6.0,
        "Arvio %": 11.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Gocciadoron tamma, testataan Finntack Yankee -kärryillä.",
    },
    # --- V85-4 ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#1 Jaguar Ima",
        "Peliprosentti": 4.0,
        "Arvio %": 11.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Berglundin passas – spurtasi viimeksi 1.11 viimeiset"
            " 1100m."
        ),
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Arvio %": 35.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Tjomslandin huippuhevonen, kovan luokan suosikki.",
    },
    # --- V85-5 ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Arvio %": 45.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Jättisuosikki, mutta sisärata on riski.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "Miguel",
        "Peliprosentti": 5.0,
        "Arvio %": 10.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Nousee kovan luokan taustalta, Kihlström rattaille"
            "[cite: 3]."
        ),
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "King Kong DK",
        "Peliprosentti": 2.0,
        "Arvio %": 5.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Unohdettu pikkoprosenteilla, varteenotettava"
            " yllätyshaku[cite: 3]."
        ),
    },
    # --- V85-6 ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Arvio %": 55.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Selvä suosikki, sopiva matka.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "Obi Wan Keeper",
        "Peliprosentti": 1.0,
        "Arvio %": 4.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Todellinen jättiyllättäjä (1%), sopii isommille"
            " lapuille[cite: 3]."
        ),
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "Maximus Vici",
        "Peliprosentti": 1.0,
        "Arvio %": 4.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Pienellä prosentilla mukaan tukkoon, jos suosikit"
            " epäonnistuvat[cite: 3]."
        ),
    },
    # --- V85-7 ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 36.0,
        "Arvio %": 38.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Gulddivisionen-suosikki, spår 5 etu.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "Follow Him",
        "Peliprosentti": 8.0,
        "Arvio %": 12.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Barfota-muutos ja hyvät iskumahdollisuudet"
            " Gulddivisionissa[cite: 3]."
        ),
    },
    # --- V85-8 ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Arvio %": 35.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Stayerloppetin suosikki.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "King Okay",
        "Peliprosentti": 3.0,
        "Arvio %": 7.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Stayer-matkan tuoma venyvyys tekee tästä hyvän"
            " haastajan[cite: 3]."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "Southbeach Volo",
        "Peliprosentti": 2.0,
        "Arvio %": 8.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Vahva loppuvetäjä, erinomainen valinta pitkälle"
            " matkalle[cite: 3]."
        ),
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)

st.subheader("📝 Kertoimien syöttö (Päivitä illalla klo 18 jälkeen)")
edited_df = st.data_editor(df_vihjeet, use_container_width=True, num_rows="fixed")

# ----------------- LASKENTA -----------------
edited_df["Paras Kerroin"] = edited_df[["Unibet", "Coolbet"]].max(axis=1)
edited_df["EV"] = (edited_df["Arvio %"] / 100.0) * edited_df["Paras Kerroin"]

st.divider()

# 🔥 YLLÄTTÄJÄT LÄHDÖTTÄIN RYHMITTELTYNÄ (< 10 %)
st.subheader(
    "🔥 Alipelatut Yllättäjät Lähdöittäin (< 10 % Peliprosentti)"
)

df_surprises = edited_df[edited_df["Peliprosentti"] < 10.0]

for kohde in sorted(df_surprises["Kohde"].unique()):
    st.markdown(f"### 📌 {kohde}")
    sub_df = df_surprises[df_surprises["Kohde"] == kohde]
    st.dataframe(
        sub_df[
            [
                "Hevonen",
                "Peliprosentti",
                "Arvio %",
                "Unibet",
                "Coolbet",
                "Paras Kerroin",
                "EV",
                "Perustelu",
            ]
        ].sort_values(by="EV", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
