import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Monte Carlo - Färjestad (Koko kenttä)",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Ravianalyysi & Monte Carlo Simulaatio (Koko Kierros)")
st.caption(
    "Färjestad – Analyysi kattaa kaikki 8 kohdetta ja noin 85 hevosta."
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

# ----------------- KAIKKI HEVOSET (KAIKKI 8 KOHDETTA) -----------------
vihjeet_data = [
    # --- V85-1 (L5) ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#1 Licorice Sisu",
        "Peliprosentti": 15.0,
        "Arvio %": 18.0,
        "Unibet": 5.50,
        "Coolbet": 5.25,
        "Perustelu": "Kihlström kyydissä, sisärata.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Arvio %": 55.0,
        "Unibet": 1.65,
        "Coolbet": 1.60,
        "Perustelu": "Selvä suosikki, Goopin luokkahevonen.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Arvio %": 9.0,
        "Unibet": 10.00,
        "Coolbet": 9.50,
        "Perustelu": "💥 YLLÄTTÄJÄ: Mielenkiintoinen haastaja taustalla.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Glaziers Wondergirl",
        "Peliprosentti": 5.0,
        "Arvio %": 7.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Nopea avaaja.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#5 Hulte Inez",
        "Peliprosentti": 2.0,
        "Arvio %": 3.0,
        "Unibet": 25.00,
        "Coolbet": 24.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Vaatii nappijuoksun.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Peliprosentti": 2.0,
        "Arvio %": 5.0,
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Berglundin nosto, norjalainen vieras.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#7 Mellby Knekt",
        "Peliprosentti": 3.0,
        "Arvio %": 2.0,
        "Unibet": 30.00,
        "Coolbet": 28.00,
        "Perustelu": "Taustalla isoilla kertoimilla.",
    },
    # --- V85-2 (L6) ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#1 Rya Håleryd",
        "Peliprosentti": 8.0,
        "Arvio %": 10.0,
        "Unibet": 9.00,
        "Coolbet": 8.50,
        "Perustelu": "💥 YLLÄTTÄJÄ: Hyvä sisärata.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#2 Global Depdendable",
        "Peliprosentti": 3.0,
        "Arvio %": 4.0,
        "Unibet": 20.00,
        "Coolbet": 18.00,
        "Perustelu": "Hakee yllätystä sisäratajuoksulla.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#3 Global Evolution",
        "Peliprosentti": 1.0,
        "Arvio %": 2.0,
        "Unibet": 40.00,
        "Coolbet": 35.00,
        "Perustelu": "Teilee isoilla kertoimilla.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#4 Nilla Lane",
        "Peliprosentti": 35.0,
        "Arvio %": 34.0,
        "Unibet": 2.85,
        "Coolbet": 2.90,
        "Perustelu": "Vahva tamma, hakee keulapaikkaa.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Skylight",
        "Peliprosentti": 22.0,
        "Arvio %": 24.0,
        "Unibet": 3.75,
        "Coolbet": 3.80,
        "Perustelu": "Kovassa kunnossa.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Great Old Dance (L6)",
        "Peliprosentti": 25.0,
        "Arvio %": 23.0,
        "Unibet": 4.00,
        "Coolbet": 3.80,
        "Perustelu": "Päähaastaja.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#7 Extra Special",
        "Peliprosentti": 3.0,
        "Arvio %": 2.0,
        "Unibet": 35.00,
        "Coolbet": 30.00,
        "Perustelu": "Vaikea tehtävä.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#8 Global Famous",
        "Peliprosentti": 1.0,
        "Arvio %": 1.0,
        "Unibet": 50.00,
        "Coolbet": 45.00,
        "Perustelu": "Ulkorata haastaa.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Kinky Boots",
        "Peliprosentti": 3.0,
        "Arvio %": 2.0,
        "Unibet": 30.00,
        "Coolbet": 28.00,
        "Perustelu": "Haastaa lopussa.",
    },
    # --- V85-3 (L7) ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#1 Dorito Pellini",
        "Peliprosentti": 25.0,
        "Arvio %": 24.0,
        "Unibet": 3.80,
        "Coolbet": 3.75,
        "Perustelu": "Paalun suosikki.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#2 Stens Rubin",
        "Peliprosentti": 6.0,
        "Arvio %": 8.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Nopea avaaja.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "Peliprosentti": 24.0,
        "Arvio %": 26.0,
        "Unibet": 3.80,
        "Coolbet": 3.75,
        "Perustelu": "Vahva tamma.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#4 Get A Wish",
        "Peliprosentti": 4.0,
        "Arvio %": 5.0,
        "Unibet": 18.00,
        "Coolbet": 16.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Iskuvalmiudessa.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#5 Bright Star",
        "Peliprosentti": 7.0,
        "Arvio %": 6.0,
        "Unibet": 14.00,
        "Coolbet": 13.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Kunto nousemassa.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Peliprosentti": 2.0,
        "Arvio %": 4.0,
        "Unibet": 25.00,
        "Coolbet": 22.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Tekee itse työt.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "Peliprosentti": 26.0,
        "Arvio %": 28.0,
        "Unibet": 3.50,
        "Coolbet": 3.40,
        "Perustelu": "Peliaineiston kärkipään tamma.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#8 Ginevra Ek",
        "Peliprosentti": 6.0,
        "Arvio %": 8.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Gocciadoron tamma.",
    },
    # --- V85-4 (L8) ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#1 Jaguar Ima",
        "Peliprosentti": 4.0,
        "Arvio %": 8.0,
        "Unibet": 16.00,
        "Coolbet": 15.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Berglundin passas, hurja loppuveto.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#2 B.W.Rune",
        "Peliprosentti": 1.0,
        "Arvio %": 2.0,
        "Unibet": 50.00,
        "Coolbet": 45.00,
        "Perustelu": "Taustalla isoilla kertoimilla.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Peliprosentti": 32.0,
        "Arvio %": 33.0,
        "Unibet": 2.85,
        "Coolbet": 2.80,
        "Perustelu": "Pääsuosikkeja.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "Peliprosentti": 16.0,
        "Arvio %": 15.0,
        "Unibet": 6.00,
        "Coolbet": 5.75,
        "Perustelu": "Vahva avaaja.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#5 Brenne Banker",
        "Peliprosentti": 1.0,
        "Arvio %": 2.0,
        "Unibet": 45.00,
        "Coolbet": 40.00,
        "Perustelu": "Haastaa laajemmilla lapuilla.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#6 Re Alm",
        "Peliprosentti": 4.0,
        "Arvio %": 5.0,
        "Unibet": 18.00,
        "Coolbet": 17.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Norjalainen vieras.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Arvio %": 35.0,
        "Unibet": 2.75,
        "Coolbet": 2.70,
        "Perustelu": "Kovan luokan suosikki.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#8 Grisle Odin G.L.",
        "Peliprosentti": 1.0,
        "Arvio %": 1.0,
        "Unibet": 60.00,
        "Coolbet": 50.00,
        "Perustelu": "Vaikea tehtävä.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#9 Stumne Fyr",
        "Peliprosentti": 2.0,
        "Arvio %": 3.0,
        "Unibet": 30.00,
        "Coolbet": 28.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Yllättäjäpotentiaalia.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#10 Voje Lotta",
        "Peliprosentti": 3.0,
        "Arvio %": 4.0,
        "Unibet": 22.00,
        "Coolbet": 20.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Kengättömänä.",
    },
    # --- V85-5 (L9) ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Arvio %": 45.0,
        "Unibet": 2.05,
        "Coolbet": 2.00,
        "Perustelu": "Ylivoimainen pelisuosikki, isot muutokset.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#3 Soot Blaze",
        "Peliprosentti": 5.0,
        "Arvio %": 8.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Mats E Djuse puikoissa.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "Peliprosentti": 17.0,
        "Arvio %": 24.0,
        "Unibet": 4.50,
        "Coolbet": 4.40,
        "Perustelu": "Spår 5 -etu (Färjestad ROI).",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Miguel",
        "Peliprosentti": 5.0,
        "Arvio %": 7.0,
        "Unibet": 14.00,
        "Coolbet": 13.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Kihlström rattaille.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#9 Eolo Jet",
        "Peliprosentti": 7.0,
        "Arvio %": 6.0,
        "Unibet": 11.00,
        "Coolbet": 10.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Tasaista suorittamista.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#10 Kinky Boots",
        "Peliprosentti": 5.0,
        "Arvio %": 5.0,
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Haastaa lopussa.",
    },
    # --- V85-6 (L10) ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#1 Kaxig In",
        "Peliprosentti": 9.0,
        "Arvio %": 10.0,
        "Unibet": 9.50,
        "Coolbet": 9.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Sisärata, hyvät krahter.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Peliprosentti": 6.0,
        "Arvio %": 11.0,
        "Unibet": 8.50,
        "Coolbet": 8.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Nopea avaaja.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Arvio %": 55.0,
        "Unibet": 1.75,
        "Coolbet": 1.70,
        "Perustelu": "Selvä suosikki.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 7.0,
        "Arvio %": 8.0,
        "Unibet": 11.00,
        "Coolbet": 10.50,
        "Perustelu": "💥 YLLÄTTÄJÄ: Redénin valmennettava.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "Peliprosentti": 2.0,
        "Arvio %": 6.0,
        "Unibet": 16.00,
        "Coolbet": 15.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Berglundin suosikki.",
    },
    # --- V85-7 (L11) ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#2 Stens Rubin",
        "Peliprosentti": 17.0,
        "Arvio %": 20.0,
        "Unibet": 4.80,
        "Coolbet": 4.60,
        "Perustelu": "Spetsläge, vahva haastaja.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Barack Face",
        "Peliprosentti": 14.0,
        "Arvio %": 16.0,
        "Unibet": 6.00,
        "Coolbet": 5.75,
        "Perustelu": "Finntack yankee -vagn.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 36.0,
        "Arvio %": 38.0,
        "Unibet": 2.50,
        "Coolbet": 2.45,
        "Perustelu": "Suosikki, spår 5 etu.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#7 Lucky Silver",
        "Peliprosentti": 9.0,
        "Arvio %": 11.0,
        "Unibet": 9.00,
        "Coolbet": 8.50,
        "Perustelu": "💥 YLLÄTTÄJÄ: Berglundin nosto, vahva loppuveto.",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Slivovitz Lover",
        "Peliprosentti": 9.0,
        "Arvio %": 10.0,
        "Unibet": 9.50,
        "Coolbet": 9.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Hyvä vire taustalla.",
    },
    # --- V85-8 (L12) ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#2 Mr Carnation",
        "Peliprosentti": 18.0,
        "Arvio %": 16.0,
        "Unibet": 5.00,
        "Coolbet": 4.80,
        "Perustelu": "Vahva pelihevonen paalulta.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Arvio %": 35.0,
        "Unibet": 2.60,
        "Coolbet": 2.55,
        "Perustelu": "Pääsuosikki.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#9 Golden Sunrise",
        "Peliprosentti": 2.0,
        "Arvio %": 5.0,
        "Unibet": 18.00,
        "Coolbet": 17.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Stayer-matkan yllättäjä.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#10 Bourbon Brodde",
        "Peliprosentti": 1.0,
        "Arvio %": 4.0,
        "Unibet": 25.00,
        "Coolbet": 22.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Sjödénin tilastohaku.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#14 Southbeach Volo",
        "Peliprosentti": 2.0,
        "Arvio %": 6.0,
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": "💥 YLLÄTTÄJÄ: Ruotsin mediavinkki.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "Peliprosentti": 20.0,
        "Arvio %": 24.0,
        "Unibet": 4.20,
        "Coolbet": 4.00,
        "Perustelu": "Luokkansa ykkönen takamatkalta.",
    },
]

# TOTEUTUNEET TULOKSET (Esimerkkitulokset testausta varten)
tulokset_data = [
    {"Kohde": "V85-1", "Voittaja": "#2 Mohawk", "Kerroin_Toteutunut": 1.65},
    {"Kohde": "V85-2", "Voittaja": "#4 Nilla Lane", "Kerroin_Toteutunut": 2.85},
    {"Kohde": "V85-3", "Voittaja": "#7 Lotusorchide", "Kerroin_Toteutunut": 3.50},
    {"Kohde": "V85-4", "Voittaja": "#7 Tangen Bork", "Kerroin_Toteutunut": 2.75},
    {"Kohde": "V85-5", "Voittaja": "#1 Fedorov", "Kerroin_Toteutunut": 2.05},
    {"Kohde": "V85-6", "Voittaja": "#4 Cold Blaze", "Kerroin_Toteutunut": 1.75},
    {
        "Kohde": "V85-7",
        "Voittaja": "#5 Bright Star U.S.",
        "Kerroin_Toteutunut": 2.50,
    },
    {
        "Kohde": "V85-8",
        "Voittaja": "#6 Great Old Dance",
        "Kerroin_Toteutunut": 2.60,
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)
df_tulokset = pd.DataFrame(tulokset_data)

# ----------------- ANALYYSI & LASKENTA -----------------
df_vihjeet["Paras Kerroin"] = df_vihjeet[["Unibet", "Coolbet"]].max(axis=1)
df_vihjeet["EV"] = (df_vihjeet["Arvio %"] / 100.0) * df_vihjeet["Paras Kerroin"]

df_vihjeet["Voitti"] = df_vihjeet.apply(
    lambda row: any(
        (row["Kohde"] == t["Kohde"])
        and (row["Hevonen"].split()[0] in t["Voittaja"])
        for _, t in df_tulokset.iterrows()
    ),
    axis=1,
)

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

kokonaispanos = len(df_vihjeet) * panos_per_vihje
voittaneet = df_vihjeet[df_vihjeet["Voitti"]]
palautus = (voittaneet["Paras Kerroin"] * panos_per_vihje).sum()
netto = palautus - kokonaispanos
roi = (palautus / kokonaispanos * 100) if kokonaispanos > 0 else 0

# ----------------- TULOSTEN NÄYTTÖ -----------------
st.subheader("📊 V85 Kierroksen Yhteenveto & ROI")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Käsiteltyjä Hevosia", f"{len(df_vihjeet)} kpl")
m2.metric("Osuneet Vihjeet", f"{len(voittaneet)} kpl")
m3.metric("Nettotulos", f"{palautus:.2f} €", delta=f"{netto:.2f} €")
m4.metric("ROI", f"{roi:.1f} %")

st.divider()

# 🔥 KAIKKI ALLE 10 % YLLÄTTÄJÄT
st.subheader("🔥 Kaikki Alipelatut Yllättäjät (< 10 % Peliprosentti)")
df_surprises = df_vihjeet[df_vihjeet["Peliprosentti"] < 10.0]
st.dataframe(
    df_surprises[
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

st.subheader("🎯 Kaikki Kohteet ja EV-analyysi")
df_filtered = df_vihjeet[df_vihjeet["EV"] >= osuma_raja_ev]
st.dataframe(
    df_filtered[
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
