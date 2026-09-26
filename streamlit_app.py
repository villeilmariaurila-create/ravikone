import numpy as np
import pandas as pd
import streamlit as st

# Streamlit-sivun määritykset
st.set_page_config(
    page_title="V85 Åby - Monte Carlo Simulaattori", page_icon="🏇", layout="wide"
)

st.title("🏇 V85 Åby - Monte Carlo Simulaattori & Peli-ideat")
st.markdown(
    "Tämä ammattimainen simulaattori ajaa 100 000 Monte Carlo -kierrosta jokaiselle kohteelle. "
    "Malli huomioi ratsastus- ja varustebonukset, Åbyn Open Stretch -edun, Veikkauksen pelijakauman sekä Unibetin kertoimet."
)

np.random.seed(42)
NUM_SIMULATIONS = 100000

# Kaikkien kohteiden V85-1 - V85-8 tiedot
races_data = [
    # --- V85-1 ---
    [
        {
            "Kohde": "V85-1",
            "Hevonen": "#1 Staro Raili",
            "Veikkaus %": 12.0,
            "Unibet": 8.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-1",
            "Hevonen": "#2 Naomi Bros",
            "Veikkaus %": 15.0,
            "Unibet": 6.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-1",
            "Hevonen": "#3 Daim Brodda",
            "Veikkaus %": 35.0,
            "Unibet": 2.20,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-1",
            "Hevonen": "#4 Eivissa",
            "Veikkaus %": 10.0,
            "Unibet": 12.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-1",
            "Hevonen": "#5 Xia Lloyd",
            "Veikkaus %": 18.0,
            "Unibet": 4.50,
            "Bonus": 1.02,
        },
        {
            "Kohde": "V85-1",
            "Hevonen": "#6 Ninetta Boko",
            "Veikkaus %": 10.0,
            "Unibet": 15.00,
            "Bonus": 1.00,
        },
    ],
    # --- V85-2 ---
    [
        {
            "Kohde": "V85-2",
            "Hevonen": "#1 Phantom Express",
            "Veikkaus %": 40.0,
            "Unibet": 1.85,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-2",
            "Hevonen": "#2 Bullet The BlueSky",
            "Veikkaus %": 25.0,
            "Unibet": 3.50,
            "Bonus": 1.02,
        },
        {
            "Kohde": "V85-2",
            "Hevonen": "#3 Screen Time Limit",
            "Veikkaus %": 15.0,
            "Unibet": 7.50,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-2",
            "Hevonen": "#4 Magic In",
            "Veikkaus %": 10.0,
            "Unibet": 12.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-2",
            "Hevonen": "#5 Dream Mine",
            "Veikkaus %": 10.0,
            "Unibet": 15.00,
            "Bonus": 1.00,
        },
    ],
    # --- V85-3 ---
    [
        {
            "Kohde": "V85-3",
            "Hevonen": "#1 Isaac Wynn",
            "Veikkaus %": 14.0,
            "Unibet": 4.65,
            "Bonus": 1.10,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#2 Wilma Express",
            "Veikkaus %": 1.0,
            "Unibet": 30.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#3 King Light",
            "Veikkaus %": 1.0,
            "Unibet": 22.00,
            "Bonus": 1.07,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#4 Hans Palema",
            "Veikkaus %": 7.0,
            "Unibet": 8.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#5 Sky Brigadoon",
            "Veikkaus %": 1.0,
            "Unibet": 35.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#6 Kung Fu Dot Com",
            "Veikkaus %": 50.0,
            "Unibet": 4.50,
            "Bonus": 1.06,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#7 Paul Mccartney",
            "Veikkaus %": 1.0,
            "Unibet": 17.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#8 Packedwithsasstrot",
            "Veikkaus %": 1.0,
            "Unibet": 30.00,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#9 Occam's Razor",
            "Veikkaus %": 19.0,
            "Unibet": 3.75,
            "Bonus": 1.04,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#10 Jaguar Ima",
            "Veikkaus %": 2.0,
            "Unibet": 17.50,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#11 Pernod Boko",
            "Veikkaus %": 2.0,
            "Unibet": 22.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-3",
            "Hevonen": "#12 Emon Face",
            "Veikkaus %": 2.0,
            "Unibet": 18.50,
            "Bonus": 1.00,
        },
    ],
    # --- V85-4 ---
    [
        {
            "Kohde": "V85-4",
            "Hevonen": "#1 Pace Marke",
            "Veikkaus %": 3.0,
            "Unibet": 43.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#2 Luther King",
            "Veikkaus %": 7.0,
            "Unibet": 7.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#3 Assar Wibb",
            "Veikkaus %": 5.0,
            "Unibet": 17.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#4 Wiener Sängerknabe",
            "Veikkaus %": 5.0,
            "Unibet": 45.00,
            "Bonus": 1.02,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#5 Parameter",
            "Veikkaus %": 5.0,
            "Unibet": 27.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#6 True Lies",
            "Veikkaus %": 9.0,
            "Unibet": 16.00,
            "Bonus": 1.06,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#7 Jayden De Joudes",
            "Veikkaus %": 18.0,
            "Unibet": 4.25,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#8 Digital Brodde",
            "Veikkaus %": 25.0,
            "Unibet": 4.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#9 Made By Love",
            "Veikkaus %": 3.0,
            "Unibet": 30.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#10 Sir Hans",
            "Veikkaus %": 7.0,
            "Unibet": 10.50,
            "Bonus": 1.04,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#11 Keepthesugarcoming",
            "Veikkaus %": 1.0,
            "Unibet": 65.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#12 Dencos T.D.",
            "Veikkaus %": 3.0,
            "Unibet": 27.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#13 Assar Rapid",
            "Veikkaus %": 6.0,
            "Unibet": 7.25,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#14 Omari Boko",
            "Veikkaus %": 2.0,
            "Unibet": 55.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-4",
            "Hevonen": "#15 Everglow",
            "Veikkaus %": 1.0,
            "Unibet": 65.00,
            "Bonus": 1.00,
        },
    ],
    # --- V85-5 ---
    [
        {
            "Kohde": "V85-5",
            "Hevonen": "#1 No Moore Z.A.R.",
            "Veikkaus %": 10.0,
            "Unibet": 6.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#2 Global Federation",
            "Veikkaus %": 17.0,
            "Unibet": 4.50,
            "Bonus": 1.02,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#3 My D.X.One",
            "Veikkaus %": 3.0,
            "Unibet": 14.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#4 Global Good Luck",
            "Veikkaus %": 26.0,
            "Unibet": 4.15,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#5 Tvingens Calippo",
            "Veikkaus %": 26.0,
            "Unibet": 2.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#6 Lugnets Ametrin",
            "Veikkaus %": 3.0,
            "Unibet": 17.50,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#7 Humble Malt",
            "Veikkaus %": 3.0,
            "Unibet": 50.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#8 Wing Profile",
            "Veikkaus %": 6.0,
            "Unibet": 25.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#9 Boba Fett",
            "Veikkaus %": 1.0,
            "Unibet": 27.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#11 Grasshopper R.L.",
            "Veikkaus %": 3.0,
            "Unibet": 14.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-5",
            "Hevonen": "#12 Al's Demonic Doll",
            "Veikkaus %": 2.0,
            "Unibet": 65.00,
            "Bonus": 1.09,
        },
    ],
    # --- V85-6 ---
    [
        {
            "Kohde": "V85-6",
            "Hevonen": "#1 Blixt Lane",
            "Veikkaus %": 7.0,
            "Unibet": 6.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#2 Mellby Mowgli",
            "Veikkaus %": 16.0,
            "Unibet": 4.65,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#3 J.C.",
            "Veikkaus %": 3.0,
            "Unibet": 16.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#4 I.D.Got A Colt",
            "Veikkaus %": 14.0,
            "Unibet": 5.50,
            "Bonus": 1.02,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#5 Simon Palema",
            "Veikkaus %": 18.0,
            "Unibet": 6.00,
            "Bonus": 1.04,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#6 Joker Ima",
            "Veikkaus %": 3.0,
            "Unibet": 18.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#7 Ebbot Rice",
            "Veikkaus %": 17.0,
            "Unibet": 12.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#8 Drag Racing",
            "Veikkaus %": 5.0,
            "Unibet": 30.00,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#9 Fly Express",
            "Veikkaus %": 8.0,
            "Unibet": 12.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#10 Mansa Musa Mearas",
            "Veikkaus %": 5.0,
            "Unibet": 15.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#11 L'Amiral S.J.S.",
            "Veikkaus %": 2.0,
            "Unibet": 28.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-6",
            "Hevonen": "#12 Epicure D.E.",
            "Veikkaus %": 2.0,
            "Unibet": 30.00,
            "Bonus": 1.05,
        },
    ],
    # --- V85-7 ---
    [
        {
            "Kohde": "V85-7",
            "Hevonen": "#1 R.K.Augusta",
            "Veikkaus %": 2.0,
            "Unibet": 45.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#2 Monnier Mearas",
            "Veikkaus %": 14.0,
            "Unibet": 5.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#3 Miss Magdalena",
            "Veikkaus %": 11.0,
            "Unibet": 5.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#4 Pelshin Boko",
            "Veikkaus %": 10.0,
            "Unibet": 5.50,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#5 Cornelia Palema",
            "Veikkaus %": 1.0,
            "Unibet": 30.00,
            "Bonus": 1.02,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#6 Run Rhapsody Run",
            "Veikkaus %": 6.0,
            "Unibet": 14.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#7 C'est Ma Course",
            "Veikkaus %": 1.0,
            "Unibet": 75.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#8 Janica Zet",
            "Veikkaus %": 1.0,
            "Unibet": 115.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#9 Sainz Zon",
            "Veikkaus %": 2.0,
            "Unibet": 115.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#10 Piccadilly Pellini",
            "Veikkaus %": 8.0,
            "Unibet": 17.50,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#11 Grace Vendil",
            "Veikkaus %": 7.0,
            "Unibet": 30.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#12 Just For Show",
            "Veikkaus %": 17.0,
            "Unibet": 4.75,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#13 Merlene Boko",
            "Veikkaus %": 9.0,
            "Unibet": 25.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#14 Can't Be Ruled",
            "Veikkaus %": 1.0,
            "Unibet": 125.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-7",
            "Hevonen": "#15 Halina S.H.",
            "Veikkaus %": 10.0,
            "Unibet": 11.50,
            "Bonus": 1.00,
        },
    ],
    # --- V85-8 ---
    [
        {
            "Kohde": "V85-8",
            "Hevonen": "#1 Boscha Diablo",
            "Veikkaus %": 6.0,
            "Unibet": 3.65,
            "Bonus": 1.10,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#2 Kentucky River",
            "Veikkaus %": 27.0,
            "Unibet": 3.20,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#3 Call Me Gleipner",
            "Veikkaus %": 2.0,
            "Unibet": 17.50,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#4 Ready Star",
            "Veikkaus %": 16.0,
            "Unibet": 9.00,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#5 Orosei Boko",
            "Veikkaus %": 1.0,
            "Unibet": 65.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#7 High On Pepper",
            "Veikkaus %": 10.0,
            "Unibet": 7.00,
            "Bonus": 1.00,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#8 Barack Face",
            "Veikkaus %": 10.0,
            "Unibet": 18.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#9 H.C.'s Crazy Horse",
            "Veikkaus %": 2.0,
            "Unibet": 25.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#10 A Fair Day",
            "Veikkaus %": 17.0,
            "Unibet": 8.50,
            "Bonus": 1.09,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#11 Macahan",
            "Veikkaus %": 6.0,
            "Unibet": 27.00,
            "Bonus": 1.05,
        },
        {
            "Kohde": "V85-8",
            "Hevonen": "#12 Fighter Kronos",
            "Veikkaus %": 3.0,
            "Unibet": 75.00,
            "Bonus": 1.09,
        },
    ],
]

# Monte Carlo -laskenta
results_list = []

for race_idx, race in enumerate(races_data, 1):
    base_probs = np.array([h["Veikkaus %"] for h in race], dtype=float)
    bonuses = np.array([h["Bonus"] for h in race], dtype=float)
    unibet_odds = [h["Unibet"] for h in race]

    adj_weights = base_probs * bonuses
    adj_probs = adj_weights / np.sum(adj_weights)

    wins = np.random.choice(len(race), size=NUM_SIMULATIONS, p=adj_probs)
    win_counts = np.bincount(wins, minlength=len(race))
    sim_probs = (win_counts / NUM_SIMULATIONS) * 100.0

    for i, h in enumerate(race):
        s_prob = sim_probs[i]
        odds = unibet_odds[i]
        ev = (s_prob / 100.0) * odds if odds is not None else 0.0

        is_under_10 = h["Veikkaus %"] < 10.0
        is_value = ev >= 1.0

        results_list.append(
            {
                "Kohde": f"V85-{race_idx}",
                "Hevonen": h["Hevonen"],
                "Veikkaus %": h["Veikkaus %"],
                "Simu Voitto %": round(s_prob, 2),
                "Unibet Kerroin": odds if odds is not None else "-",
                "EV (Odotusarvo)": round(ev, 2),
                "Status": "🔥 YLIKERROIN (<10%)"
                if (is_under_10 and is_value)
                else ("💥 Hyvä EV" if is_value else "-"),
            }
        )

df_results = pd.DataFrame(results_list)

# --- Käyttöliittymä ---
st.subheader("🔥 Parhaat alle 10 % pelatut peli-ideat (EV >= 1.0)")
gems = df_results[df_results["Status"] == "🔥 YLIKERROIN (<10%)"]
st.dataframe(gems, use_container_width=True)

st.subheader("📋 Kaikkien kohteiden simulaatiotulokset")
selected_race = st.selectbox(
    "Valitse kohde tarkasteltavaksi:", df_results["Kohde"].unique(), index=0
)
st.dataframe(
    df_results[df_results["Kohde"] == selected_race], use_container_width=True
)
