import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Odotusarvo- ja Simulaatiotyökalu (Prosenttivertailu)",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Simulaatiotyökalu – Pe vs. La Prosenttivertailu")
st.caption(
    "Färjestad – Mukana suora vertailusarake peliprosenttien muutoksille"
    " perjantaista lauantaihin."
)

# ----------------- KOTIRADAN HEVOSLISTA (FÄRJESTAD) -----------------
kotirata_hevostiedot = [
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Goopin valmennettava kilpailee kotiradallaan, iso etu.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Vahva paikallistuntemus ja sopiva profiili Färjestadiin.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Tottunut Färjestadin kurveihin ja olosuhteisiin.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Kotiradan stayer-taituri, hyötyy radan profiilista.",
    },
]
df_kotirata = pd.DataFrame(kotirata_hevostiedot)

# ----------------- SELITYSLAATIKKO -----------------
with st.expander("ℹ️ Tietoa vertailusarakkeesta", expanded=False):
    st.markdown(
        """
    **Laskentalogiikka:**
    * **Pe %**: Perjantain alustava peliprosentti.
    * **La %**: Lauantain tuore peliprosentti (L5-L12 tuoreesta datasta).
    * **Muutos Pe-La**: Näyttää suoraan erotuksen (La % - Pe %). Plussalla olevat kertovat pelaajien heränneestä kiinnostuksesta.
    * **Odotusarvo (EV)**: `(Lopullinen Arvio % / 100) * Paras Kerroin`.
    """
    )

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

# ----------------- V85 LÄHDÖT & PE/LA PROSENTIT -----------------
vihjeet_data = [
    # --- V85-1 ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Pe %": 62.0,
        "La %": 61.0,
        "Data_Arvio %": 55.0,
        "Vihje_Paino": 1.02,
        "Unibet": 2.65,
        "Perustelu": "Pysyy vakaana jättisuosikkina (61%)[cite: 4, 9].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Global Grand Slam",
        "Pe %": 6.0,
        "La %": 9.0,
        "Data_Arvio %": 9.0,
        "Vihje_Paino": 1.05,
        "Unibet": 5.00,
        "Perustelu": "Pelattu hieman enemmän (+3%-yks)[cite: 9].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Pe %": 1.0,
        "La %": 3.0,
        "Data_Arvio %": 7.0,
        "Vihje_Paino": 1.02,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Pieni nousu, mutta edelleen alipelattu[cite: 4, 9].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Hola Que Tal",
        "Pe %": 4.0,
        "La %": 5.0,
        "Data_Arvio %": 6.0,
        "Vihje_Paino": 1.00,
        "Unibet": 7.00,
        "Perustelu": "Vakaa peliosuus (5%)[cite: 4, 9].",
    },
    # --- V85-2 ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "Pe %": 35.0,
        "La %": 50.0,
        "Data_Arvio %": 45.0,
        "Vihje_Paino": 1.05,
        "Unibet": 2.75,
        "Perustelu": "Vahvassa nosteessa (+15%-yks), selvä suosikki[cite: 5, 9].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Skylight",
        "Pe %": 15.0,
        "La %": 26.0,
        "Data_Arvio %": 25.0,
        "Vihje_Paino": 1.02,
        "Unibet": 2.75,
        "Perustelu": "Pelattu selvästi enemmän (+11%-yks)[cite: 5, 9].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#10 Monkey Wine",
        "Pe %": 5.0,
        "La %": 6.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.02,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Vakaa pikkupeli (6%)[cite: 3, 5, 9].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Panthere d’Inverne",
        "Pe %": 4.0,
        "La %": 4.0,
        "Data_Arvio %": 10.0,
        "Vihje_Paino": 1.00,
        "Unibet": 9.75,
        "Perustelu": "💥 Yllättäjä: Ei muutosta (4%)[cite: 3, 5, 9].",
    },
    # --- V85-3 ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "Pe %": 10.0,
        "La %": 23.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 1.05,
        "Unibet": 6.75,
        "Perustelu": "Saanut paljon luottoa markkinassa (+13%-yks)[cite: 6, 9].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Pe %": 8.0,
        "La %": 18.0,
        "Data_Arvio %": 24.0,
        "Vihje_Paino": 1.02,
        "Unibet": 8.50,
        "Perustelu": "Noussut reilusti (+10%-yks)[cite: 6, 9].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#10 Popup Pellini",
        "Pe %": 3.0,
        "La %": 6.0,
        "Data_Arvio %": 20.0,
        "Vihje_Paino": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Pientä nousua (6%)[cite: 3, 6, 9].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "Pe %": 12.0,
        "La %": 24.0,
        "Data_Arvio %": 20.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.00,
        "Perustelu": "Noussut suosikkikastiin (+12%-yks)[cite: 6, 9].",
    },
    # --- V85-4 ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Pe %": 33.0,
        "La %": 38.0,
        "Data_Arvio %": 42.0,
        "Vihje_Paino": 1.05,
        "Unibet": 2.20,
        "Perustelu": "Pieni nousu (+5%-yks), vahva suosikki[cite: 7, 9].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Pe %": 33.0,
        "La %": 29.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 0.98,
        "Unibet": 4.25,
        "Perustelu": "Laskenut hieman (-4%-yks)[cite: 7, 9].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "Pe %": 10.0,
        "La %": 17.0,
        "Data_Arvio %": 18.0,
        "Vihje_Paino": 1.02,
        "Unibet": 6.25,
        "Perustelu": "Selvä nousu (+7%-yks)[cite: 7, 9].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#6 Baias",
        "Pe %": 5.0,
        "La %": 4.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.00,
        "Unibet": 10.50,
        "Perustelu": "💥 Yllättäjä: Pysyy alhaisella osuudella (4%)[cite: 3, 7, 9].",
    },
    # --- V85-5 ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Pe %": 57.0,
        "La %": 50.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 0.95,
        "Unibet": 2.35,
        "Perustelu": "Laskenut hieman (-7%-yks), mutta yhä jättisuosikki[cite: 7, 9].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "Pe %": 15.0,
        "La %": 25.0,
        "Data_Arvio %": 38.0,
        "Vihje_Paino": 1.08,
        "Unibet": 3.35,
        "Perustelu": "Vahvassa nosteessa (+10%-yks)[cite: 7, 9].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Paw Patrol V.S.",
        "Pe %": 8.0,
        "La %": 6.0,
        "Data_Arvio %": 18.0,
        "Vihje_Paino": 1.00,
        "Unibet": 7.00,
        "Perustelu": "💥 Yllättäjä: Pientä laskua (6%)[cite: 3, 7, 9].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#10 Miguel",
        "Pe %": 5.0,
        "La %": 6.0,
        "Data_Arvio %": 14.0,
        "Vihje_Paino": 1.00,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä: Vakaa pikkupeli (6%)[cite: 3, 7, 9].",
    },
    # --- V85-6 ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Pe %": 59.0,
        "La %": 64.0,
        "Data_Arvio %": 45.0,
        "Vihje_Paino": 0.98,
        "Unibet": 2.20,
        "Perustelu": "Vahvistunut entisestään (+5%-yks, 64%)[cite: 8, 9].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "Pe %": 1.0,
        "La %": 3.0,
        "Data_Arvio %": 25.0,
        "Vihje_Paino": 1.05,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä: Pieni nosto, yhä huippu-EV (3%)[cite: 3, 8, 9].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Pe %": 10.0,
        "La %": 7.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.02,
        "Unibet": 7.00,
        "Perustelu": "Laskenut hieman (7%)[cite: 8, 9].",
    },
    # --- V85-7 ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Pe %": 36.0,
        "La %": 25.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.00,
        "Unibet": 5.75,
        "Perustelu": "Laskenut selvästi (-11%-yks)[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Get A Wish",
        "Pe %": 20.0,
        "La %": 20.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.50,
        "Perustelu": "Täysin vakaa (20%)[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Loxahatchee",
        "Pe %": 8.0,
        "La %": 19.0,
        "Data_Arvio %": 25.0,
        "Vihje_Paino": 1.02,
        "Unibet": 6.25,
        "Perustelu": "Rju nousu (+11%-yks, 19%)[cite: 3, 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#3 Barack Face",
        "Pe %": 15.0,
        "La %": 6.0,
        "Data_Arvio %": 15.0,
        "Vihje_Paino": 1.02,
        "Unibet": 5.75,
        "Perustelu": "💥 Yllättäjä: Peli laskenut (6%), hyvä EV[cite: 3, 9].",
    },
    # --- V85-8 ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Pe %": 38.0,
        "La %": 36.0,
        "Data_Arvio %": 40.0,
        "Vihje_Paino": 1.05,
        "Unibet": 3.00,
        "Perustelu": "Pysyy vakaana suosikkina (36%)[cite: 9].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "Pe %": 20.0,
        "La %": 23.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.25,
        "Perustelu": "Noussut hieman (+3%-yks)[cite: 9].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#2 Mr Carnation",
        "Pe %": 15.0,
        "La %": 18.0,
        "Data_Arvio %": 20.0,
        "Vihje_Paino": 1.00,
        "Unibet": 5.75,
        "Perustelu": "Pelattu hieman enemmän (+3%-yks)[cite: 9].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#12 King Okay",
        "Pe %": 3.0,
        "La %": 1.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Jättiyllättäjä: Laskenut 1 prosenttiin[cite: 3, 9].",
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)

# --- LASKETAAN PROSENTTIMUUTOS (La % - Pe %) ---
df_vihjeet["Muutos Pe-La"] = df_vihjeet["La %"] - df_vihjeet["Pe %"]


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
    df_vihjeet["Data_Arvio %"]
    * df_vihjeet["Vihje_Paino"]
    * df_vihjeet["Kotirata_Bonus"]
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
    st.sidebar.success(f"Simulaation osumatodennäköisyys: {hit_rate:.2f} %")

# ----------------- NÄYTÖT -----------------
st.subheader("🏠 Färjestadin Kotiradan Hevoset & Paikallisetu")
st.dataframe(df_kotirata, use_container_width=True, hide_index=True)

st.divider()

st.subheader("📊 Odotusarvot & Pe-La Prosenttivertailu")
st.dataframe(
    df_vihjeet[
        [
            "Kohde",
            "Hevonen",
            "Pe %",
            "La %",
            "Muutos Pe-La",
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

st.subheader("🔥 Alipelatut Yllättäjät (< 10 % Peliprosentti)")
df_surprises = df_vihjeet[df_vihjeet["La %"] < 10.0]

for kohde in sorted(df_surprises["Kohde"].unique()):
    st.markdown(f"### 📌 {kohde}")
    sub_df = df_surprises[df_surprises["Kohde"] == kohde]
    st.dataframe(
        sub_df[
            [
                "Hevonen",
                "Pe %",
                "La %",
                "Muutos Pe-La",
                "Arvio %",
                "Paras Kerroin",
                "EV",
                "Perustelu",
            ]
        ].sort_values(by="EV", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
