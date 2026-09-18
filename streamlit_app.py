import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Keulapainotettu Simulaatio",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Simulaatio & Odotusarvotyökalu (Keulapaikka Painotettu)")
st.caption(
    "Färjestad – Malli huomioi nyt keulapaikan edun ja Unibetin viralliset"
    " kertoimet."
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

# ----------------- KAIKKI 8 LÄHTÖÄ & KEULAPAINOTUS -----------------
vihjeet_data = [
    # --- V85-1 ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Perus_Arvio %": 50.0,
        "Keula_Bonus": 1.05,  # Vahva luokkahevonen, voi saada keulat tai voittaa ulkoa
        "Unibet": 2.65,
        "Perustelu": "Selvä suosikki, Goopin luokkahevonen[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Perus_Arvio %": 9.0,
        "Keula_Bonus": 1.10,  # Nopea avaaja, barfota r/o
        "Unibet": 5.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Ensimmäistä kertaa ilman kenkiä (barfota r/o)."
        ),
    },
    # --- V85-2 ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "Peliprosentti": 35.0,
        "Perus_Arvio %": 32.0,
        "Keula_Bonus": 1.20,  # Erittäin vahva keulaehdokas, Berglundin nosto
        "Unibet": 2.75,
        "Perustelu": "Suosikki, hakee aktiivisesti keulapaikkaa[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "Urbina Southwind",
        "Peliprosentti": 2.0,
        "Perus_Arvio %": 5.0,
        "Keula_Bonus": 1.00,
        "Unibet": 25.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Pieni peliosuus (2%), potentiaalinen yllättäjä"
            " vauhdikkaan juoksun jälkeen[cite: 3, 5]."
        ),
    },
    # --- V85-3 ---
    {
        "Kohde": "V85-3",
        "Hevonen": "Miss Magdalena",
        "Peliprosentti": 4.0,
        "Perus_Arvio %": 9.0,
        "Keula_Bonus": 1.05,
        "Unibet": 14.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ ('Super'): Erittäin mielenkiintoinen ja aliarvostettu"
            " tammalähdön haastaja[cite: 3, 6]."
        ),
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#11 Ginevra Ek",
        "Peliprosentti": 6.0,
        "Perus_Arvio %": 11.0,
        "Keula_Bonus": 1.00,
        "Unibet": 33.00,
        "Perustelu": (
            "Gocciadoron tamma, testataan Finntack Yankee -kärryillä[cite: 6]."
        ),
    },
    # --- V85-4 ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#1 Jaguar Ima",
        "Peliprosentti": 4.0,
        "Perus_Arvio %": 10.0,
        "Keula_Bonus": 1.00,
        "Unibet": 9.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Berglundin passas – spurtasi viimeksi 1.11 viimeiset"
            " 1100m."
        ),
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Perus_Arvio %": 33.0,
        "Keula_Bonus": 1.15,  # Hyvin nopea voltista/autosta kylmäveriseksi
        "Unibet": 4.25,
        "Perustelu": (
            "Tjomslandin huippuhevonen, kovan luokan suosikki[cite: 7]."
        ),
    },
    # --- V85-5 ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Perus_Arvio %": 44.0,
        "Keula_Bonus": 0.90,  # Miinuskeula Färjestadin hankalasta innerspår-lähdöstä
        "Unibet": 2.35,
        "Perustelu": (
            "Jättisuosikki, mutta sisärata on riski Färjestadissa[cite: 7]."
        ),
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "Miguel",
        "Peliprosentti": 5.0,
        "Perus_Arvio %": 10.0,
        "Keula_Bonus": 1.10,
        "Unibet": 15.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Nousee kovan luokan taustalta, Kihlström rattaille"
            "[cite: 3, 7]."
        ),
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "King Kong D.K.",
        "Peliprosentti": 2.0,
        "Perus_Arvio %": 5.0,
        "Keula_Bonus": 1.05,
        "Unibet": 18.50,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Unohdettu pikkoprosenteilla, varteenotettava"
            " yllätyshaku[cite: 3, 7]."
        ),
    },
    # --- V85-6 ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Perus_Arvio %": 53.0,
        "Keula_Bonus": 1.10,
        "Unibet": 2.20,
        "Perustelu": "Selvä suosikki, sopiva matka[cite: 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "Obiwan Keeper",
        "Peliprosentti": 1.0,
        "Perus_Arvio %": 4.0,
        "Keula_Bonus": 1.00,
        "Unibet": 55.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Todellinen jättiyllättäjä (1%), sopii isommille"
            " lapuille[cite: 3, 8]."
        ),
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "Maximus Vici",
        "Peliprosentti": 1.0,
        "Perus_Arvio %": 4.0,
        "Keula_Bonus": 1.00,
        "Unibet": 25.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Pienellä prosentilla mukaan tukkoon, jos suosikit"
            " epäonnistuvat[cite: 3, 8]."
        ),
    },
    # --- V85-7 ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 36.0,
        "Perus_Arvio %": 35.0,
        "Keula_Bonus": 1.15,  # Spår 5 -etu Färjestadissa (loistava keula-/asemapaikkariski)
        "Unibet": 5.75,
        "Perustelu": "Gulddivisionen-suosikki, spår 5 etu[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "Follow Him",
        "Peliprosentti": 8.0,
        "Perus_Arvio %": 12.0,
        "Keula_Bonus": 1.05,
        "Unibet": 6.25,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Barfota-muutos ja hyvät iskumahdollisuudet"
            " Gulddivisionissa[cite: 3, 9]."
        ),
    },
    # --- V85-8 ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Perus_Arvio %": 35.0,
        "Keula_Bonus": 1.05,
        "Unibet": 3.00,
        "Perustelu": "Stayerloppetin suosikki[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "King Okay",
        "Peliprosentti": 3.0,
        "Perus_Arvio %": 7.0,
        "Keula_Bonus": 1.00,
        "Unibet": 11.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Stayer-matkan tuoma venyvyys tekee tästä hyvän"
            " haastajan[cite: 3, 10]."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "Southbeach Volo",
        "Peliprosentti": 2.0,
        "Perus_Arvio %": 8.0,
        "Keula_Bonus": 1.00,
        "Unibet": 17.50,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Vahva loppuvetäjä, erinomainen valinta pitkälle"
            " matkalle[cite: 3, 10]."
        ),
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)

# Lasketaan lopullinen keulapainotettu arvio-% (normalisoidaan kohdekohtaisesti)
df_vihjeet["Lopullinen Arvio %"] = (
    df_vihjeet["Perus_Arvio %"] * df_vihjeet["Keula_Bonus"]
)
# Normalisoidaan niin että jokaisen kohteen prosentit summan 100%
df_vihjeet["Arvio %"] = df_vihjeet.groupby("Kohde").apply(
    lambda x: x["Lopullinen Arvio %"]
    / x["Lopullinen Arvio %"].sum()
    * 100
).reset_index(level=0, drop=True)

df_vihjeet["Paras Kerroin"] = df_vihjeet["Unibet"]
df_vihjeet["EV"] = (df_vihjeet["Arvio %"] / 100.0) * df_vihjeet[
    "Paras Kerroin"
]

# ----------------- MONTE CARLO SIMULAATIO KEULAPAINOTUKSELLA -----------------
st.sidebar.subheader("🎲 Simulaatio (Keulapainotettu)")
if st.sidebar.button("Aja Keulapainotettu Simulaatio"):
    sim_results = []
    kohde_groups = df_vihjeet.groupby("Kohde")
    for _ in range(num_simulations):
        row_win = []
        for kohde, group in kohde_groups:
            probs = group["Arvio %"].values / group["Arvio %"].sum()
            winner_idx = np.random.choice(len(group), p=probs)
            row_win.append(group.iloc[winner_idx]["EV"] >= osuma_raja_ev)
        sim_results.append(all(row_win))
    hit_rate = np.mean(sim_results) * 100
    st.sidebar.success(
        f"Keulapainotettu osumatodennäköisyys: {hit_rate:.2f} %"
    )

st.subheader("📊 Keulapainotetut Odotusarvot (EV)")
st.dataframe(
    df_vihjeet[
        [
            "Kohde",
            "Hevonen",
            "Peliprosentti",
            "Arvio %",
            "Paras Kerroin",
            "EV",
            "Perustelu",
        ]
    ].sort_values(by="EV", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# 🔥 YLLÄTTÄJÄT LÄHDÖTTÄIN
st.subheader(
    "🔥 Keulahuomioidut Yllättäjät Lähdöittäin (< 10 % Peliprosentti)"
)
df_surprises = df_vihjeet[df_vihjeet["Peliprosentti"] < 10.0]

for kohde in sorted(df_surprises["Kohde"].unique()):
    st.markdown(f"### 📌 {kohde}")
    sub_df = df_surprises[df_surprises["Kohde"] == kohde]
    st.dataframe(
        sub_df[
            [
                "Hevonen",
                "Peliprosentti",
                "Arvio %",
                "Paras Kerroin",
                "EV",
                "Perustelu",
            ]
        ].sort_values(by="EV", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
