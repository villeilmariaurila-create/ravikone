import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Simulaatiotyökalu – Numeromuotoiset Prosenttimuutokset",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Simulaattori – Puolueeton Datamalli & Numeromuutokset")
st.caption(
    "Färjestad – Peliprosenttien muutokset esitetään nyt selkeässä"
    " numeromuodossa (+/-)."
)

# ----------------- KOTIRADAN HEVOSLISTA (FÄRJESTAD) -----------------
kotirata_hevostiedot = [
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Goopin valmennettava kotiradalla, pieni paikallisetu.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Vahva paikallistuntemus Färjestadissa.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Tottunut Färjestadin lyhyeen loppusuoraan.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Kotiradan stayer-taituri.",
    },
]
df_kotirata = pd.DataFrame(kotirata_hevostiedot)

# ----------------- SIVUPALKIN ASETUKSET -----------------
st.sidebar.header("⚙️ Simulaation Asetukset")
panos_per_vihje = st.sidebar.number_input(
    "Panos per vihje (€)", min_value=1.0, value=10.0, step=1.0
)
osuma_raja_ev = st.sidebar.slider(
    "Suodata minimi EV-raja", 0.5, 2.0, 1.0, step=0.05
)
num_simulations = st.sidebar.selectbox(
    "Monte Carlo -simulaatiot", [1000, 5000, 10000, 50000], index=2
)

# ----------------- V85 LÄHDÖT & NUMEROMUOTOISET MUUTOKSET -----------------
vihjeet_data = [
    # --- V85-1 ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "La %": 61.0,
        "Prosentti_Muutos": -1,
        "Oma_Simulaatio_Arvio %": 52.0,
        "Unibet": 2.65,
        "Perustelu": "Goopin tykki, tekee ison työn ulkoa, mutta simulaatio pitää selvänä suosikkina[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Global Grand Slam",
        "La %": 9.0,
        "Prosentti_Muutos": +3,
        "Oma_Simulaatio_Arvio %": 12.0,
        "Unibet": 5.00,
        "Perustelu": "Nopea avaaja, barfota r/o. Simulaatio näkee tässä hyvän EV:n.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "La %": 3.0,
        "Prosentti_Muutos": +2,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Loistava kerroin suhteessa simulaation voittotodennäköisyyteen[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Hola Que Tal",
        "La %": 5.0,
        "Prosentti_Muutos": +1,
        "Oma_Simulaatio_Arvio %": 22.0,
        "Unibet": 7.00,
        "Perustelu": "Hyvä lähtöpaikka ja Kontio. Simulaatio nostaa arvoa selvästi[cite: 4].",
    },
    # --- V85-2 ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "La %": 50.0,
        "Prosentti_Muutos": +15,
        "Oma_Simulaatio_Arvio %": 40.0,
        "Unibet": 2.75,
        "Perustelu": "Pelattu paljon, mutta simulaatio antaa hyvät saumat keulasta[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Skylight",
        "La %": 26.0,
        "Prosentti_Muutos": +11,
        "Oma_Simulaatio_Arvio %": 28.0,
        "Unibet": 2.75,
        "Perustelu": "Norjalainen kovuus, vastaa hyvin simulaation arviota[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#10 Monkey Wine",
        "La %": 6.0,
        "Prosentti_Muutos": +1,
        "Oma_Simulaatio_Arvio %": 18.0,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Wäjerstenin tykki kirii vahvasti, erinomainen EV[cite: 3, 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Panthere d’Inverne",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Unibet": 9.75,
        "Perustelu": "💥 Yllättäjä: Alipelattu tamma, simulaatio löytää yllätyspotentiaalia[cite: 3, 5].",
    },
    # --- V85-3 ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "La %": 23.0,
        "Prosentti_Muutos": +13,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Unibet": 6.75,
        "Perustelu": "Saanut paljon luottoa, loistava kerroin suhteessa simulaatioon[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "La %": 18.0,
        "Prosentti_Muutos": +10,
        "Oma_Simulaatio_Arvio %": 28.0,
        "Unibet": 8.50,
        "Perustelu": "Viihtyy Färjestadissa, simulaatio arvostaa korkealle[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#10 Popup Pellini",
        "La %": 6.0,
        "Prosentti_Muutos": +3,
        "Oma_Simulaatio_Arvio %": 22.0,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Ikäluokkakarsintojen kovuus kantaa hedelmää[cite: 3, 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "La %": 24.0,
        "Prosentti_Muutos": +12,
        "Oma_Simulaatio_Arvio %": 18.0,
        "Unibet": 4.00,
        "Perustelu": "Tasainen suorittaja, markkina ehkä hieman ylipelannut[cite: 6].",
    },
    # --- V85-4 ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "La %": 38.0,
        "Prosentti_Muutos": +5,
        "Oma_Simulaatio_Arvio %": 45.0,
        "Unibet": 2.20,
        "Perustelu": "Simulaation selvä ykkönen kylmäverisiin.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "La %": 29.0,
        "Prosentti_Muutos": -4,
        "Oma_Simulaatio_Arvio %": 30.0,
        "Unibet": 4.25,
        "Perustelu": "Kova haastaja, simulaatio luottaa tasaisesti.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "La %": 17.0,
        "Prosentti_Muutos": +7,
        "Oma_Simulaatio_Arvio %": 15.0,
        "Unibet": 6.25,
        "Perustelu": "Keulapotentiaali huomioitu simulaatiossa.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#6 Baias",
        "La %": 4.0,
        "Prosentti_Muutos": -1,
        "Oma_Simulaatio_Arvio %": 10.0,
        "Unibet": 10.50,
        "Perustelu": "💥 Yllättäjä: Aliarvostettu eliittihevonen, mahtava EV[cite: 3].",
    },
    # --- V85-5 ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "La %": 50.0,
        "Prosentti_Muutos": -7,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Unibet": 2.35,
        "Perustelu": "Ylipelattu suosikki sisäratoriskin vuoksi.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "La %": 25.0,
        "Prosentti_Muutos": +10,
        "Oma_Simulaatio_Arvio %": 42.0,
        "Unibet": 3.35,
        "Perustelu": "Simulaation superlöytö! Loistava EV ja keulasauma.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Paw Patrol V.S.",
        "La %": 6.0,
        "Prosentti_Muutos": -2,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Unibet": 7.00,
        "Perustelu": "💥 Yllättäjä: Nousuvireinen haastaja hyvällä kertoimella[cite: 3].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#10 Miguel",
        "La %": 6.0,
        "Prosentti_Muutos": +1,
        "Oma_Simulaatio_Arvio %": 12.0,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä: Kihlström rattaille, kova kerroin[cite: 3].",
    },
    # --- V85-6 ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "La %": 64.0,
        "Prosentti_Muutos": +5,
        "Oma_Simulaatio_Arvio %": 40.0,
        "Unibet": 2.20,
        "Perustelu": "Markkinoiden ylipelaama suosikki, simulaatio varoittaa.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "La %": 3.0,
        "Prosentti_Muutos": +2,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Unibet": 15.00,
        "Perustelu": "💥 Jättiyllättäjä (3%): Kierroksen paras EV! Barfota r/o ja pitkä matka[cite: 3].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "La %": 7.0,
        "Prosentti_Muutos": -3,
        "Oma_Simulaatio_Arvio %": 28.0,
        "Unibet": 7.00,
        "Perustelu": "Vahva keulakandidaatti, loistava peliarvo.",
    },
    # --- V85-7 ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "La %": 25.0,
        "Prosentti_Muutos": -11,
        "Oma_Simulaatio_Arvio %": 25.0,
        "Unibet": 5.75,
        "Perustelu": "Markkina rauhoittunut, simulaatio pitää tasaisena.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Get A Wish",
        "La %": 20.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 30.0,
        "Unibet": 4.50,
        "Perustelu": "Rautainen kovuus, simulaatio nostaa arvoa.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Loxahatchee",
        "La %": 19.0,
        "Prosentti_Muutos": +11,
        "Oma_Simulaatio_Arvio %": 30.0,
        "Unibet": 6.25,
        "Perustelu": "Guld-debytantti Mats E Djusella, kova luotto simulaatiossa[cite: 3].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#3 Barack Face",
        "La %": 6.0,
        "Prosentti_Muutos": -9,
        "Oma_Simulaatio_Arvio %": 15.0,
        "Unibet": 5.75,
        "Perustelu": "💥 Yllättäjä (6%): Aliarvostettu tähän lähtöön, erinomainen EV[cite: 3].",
    },
    # --- V85-8 ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "La %": 36.0,
        "Prosentti_Muutos": -2,
        "Oma_Simulaatio_Arvio %": 45.0,
        "Unibet": 3.00,
        "Perustelu": "Stayerloppetin simulaatioykkönen.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "La %": 23.0,
        "Prosentti_Muutos": +3,
        "Oma_Simulaatio_Arvio %": 28.0,
        "Unibet": 4.25,
        "Perustelu": "Vahva fuxi pitkälle matkalle.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#2 Mr Carnation",
        "La %": 18.0,
        "Prosentti_Muutos": +3,
        "Oma_Simulaatio_Arvio %": 15.0,
        "Unibet": 5.75,
        "Perustelu": "Hyötyy stayer-matkasta.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#12 King Okay",
        "La %": 1.0,
        "Prosentti_Muutos": -2,
        "Oma_Simulaatio_Arvio %": 12.0,
        "Unibet": 11.00,
        "Perustelu": "💥 Jättiyllättäjä (1%): Loistava loppuvetäjä, mahtava yllätyspotentiaali[cite: 3].",
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)


# --- KOTIRATABONUS LOGIIKKA ---
def get_kotirata_bonus(kohde, hevonen):
    match = df_kotirata[
        (df_kotirata["Kohde"] == kohde) & (df_kotirata["Hevonen"] == hevonen)
    ]
    if not match.empty:
        return match.iloc[0]["Kotirata_Bonus"]
    return 1.00


df_vihjeet["Kotirata_Bonus"] = df_vihjeet.apply(
    lambda row: get_kotirata_bonus(row["Kohde"], row["Hevonen"]), axis=1
)

df_vihjeet["Lopullinen Arvio %"] = (
    df_vihjeet["Oma_Simulaatio_Arvio %"] * df_vihjeet["Kotirata_Bonus"]
)
df_vihjeet["Arvio %"] = df_vihjeet.groupby("Kohde").apply(
    lambda x: x["Lopullinen Arvio %"]
    / x["Lopullinen Arvio %"].sum()
    * 100
).reset_index(level=0, drop=True)

df_vihjeet["Paras Kerroin"] = df_vihjeet["Unibet"]
df_vihjeet["EV"] = (df_vihjeet["Arvio %"] / 100.0) * df_vihjeet[
    "Paras Kerroin"
]

# ----------------- MONTE CARLO SIMULAATIO -----------------
st.sidebar.subheader("🎲 Monte Carlo Ajo")
if st.sidebar.button("Aja Simulaatio"):
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
    st.sidebar.success(f"Oma simulaatio osumatodennäköisyys: {hit_rate:.2f} %")

# ----------------- NÄYTÖT -----------------
st.subheader("🏠 Färjestadin Kotiradan Hevoset")
st.dataframe(df_kotirata, use_container_width=True, hide_index=True)

st.divider()

st.subheader("📊 Simulaation Mukaiset Odotusarvot (EV)")
st.dataframe(
    df_vihjeet[
        [
            "Kohde",
            "Hevonen",
            "La %",
            "Prosentti_Muutos",
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

st.subheader("🔥 Potentiaaliset Yllätysvoittajat (< 10 % Peliprosentti)")
df_surprises = df_vihjeet[df_vihjeet["La %"] < 10.0]

for kohde in sorted(df_surprises["Kohde"].unique()):
    st.markdown(f"### 📌 {kohde}")
    sub_df = df_surprises[df_surprises["Kohde"] == kohde]
    st.dataframe(
        sub_df[
            [
                "Hevonen",
                "La %",
                "Prosentti_Muutos",
                "Arvio %",
                "Paras Kerroin",
                "EV",
                "Perustelu",
            ]
        ].sort_values(by="EV", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
