import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V64 Ravianalyysi & Monte Carlo Simulaatio",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V64 Ravianalyysi & Monte Carlo Simulaatio - Åby 17.9.")
st.caption(
    "Päivitetty tuoreilla ruotsalaistipseillä (TR Media, ATG), Unibetin"
    " kertoimilla ja Monte Carlo -ajoilla."
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

# ----------------- PÄIVITETTY VIHJEDATA (V64: L4-L9) -----------------
vihjeet_data = [
    # V64-1 (L4)
    {
        "Kohde": "V64-1 (L4)",
        "Hevonen": "#7 Zehir",
        "Peliprosentti": 62.0,
        "Arvio %": 65.0,
        "Unibet": 1.60,
        "Perustelu": "Kierroksen varmapilari (TR Media spik). Derbykval-tausta.",
    },
    {
        "Kohde": "V64-1 (L4)",
        "Hevonen": "#5 Fantasy Sensation",
        "Peliprosentti": 24.0,
        "Arvio %": 18.0,
        "Unibet": 4.25,
        "Perustelu": "Ykköshaastaja tauolta.",
    },
    {
        "Kohde": "V64-1 (L4)",
        "Hevonen": "#4 Figlia Di Ciclone",
        "Peliprosentti": 4.0,
        "Arvio %": 11.0,
        "Unibet": 7.25,
        "Perustelu": "💥 YLLÄTTÄJÄ (<10%): Anmäld barfota runt om!",
    },
    # V64-2 (L5)
    {
        "Kohde": "V64-2 (L5)",
        "Hevonen": "#6 Numina",
        "Peliprosentti": 40.0,
        "Arvio %": 28.0,
        "Unibet": 3.25,
        "Perustelu": "Suosikki, mutta pienenä kysymysmerkkinä.",
    },
    {
        "Kohde": "V64-2 (L5)",
        "Hevonen": "#7 Ytowns Master",
        "Peliprosentti": 26.0,
        "Arvio %": 27.0,
        "Unibet": 3.15,
        "Perustelu": "Keulavoittaja, vaarallinen jos keulaan.",
    },
    {
        "Kohde": "V64-2 (L5)",
        "Hevonen": "#2 Milton Jaam",
        "Peliprosentti": 4.0,
        "Arvio %": 12.5,
        "Unibet": 15.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ (<10%): A-ryhmän nosto tipsistä! Eka kertaa barfota!"
        ),
    },
    {
        "Kohde": "V64-2 (L5)",
        "Hevonen": "#1 Clog",
        "Peliprosentti": 12.0,
        "Arvio %": 15.0,
        "Unibet": 6.75,
        "Perustelu": "Sisäradan etu nopealla maililla.",
    },
    # V64-3 (L6)
    {
        "Kohde": "V64-3 (L6)",
        "Hevonen": "#4 Kålle",
        "Peliprosentti": 31.0,
        "Arvio %": 35.0,
        "Unibet": 3.15,
        "Perustelu": "David Perssonin regidebuutti, unelmapaikka & barfota r/o.",
    },
    {
        "Kohde": "V64-3 (L6)",
        "Hevonen": "#5 Ulix Turner",
        "Peliprosentti": 22.0,
        "Arvio %": 30.0,
        "Unibet": 2.65,
        "Perustelu": "Vahva vääntäjä johtohevosen rinnalta.",
    },
    {
        "Kohde": "V64-3 (L6)",
        "Hevonen": "#1 Cay",
        "Peliprosentti": 17.0,
        "Arvio %": 16.0,
        "Unibet": 6.00,
        "Perustelu": "Lövgrenin tulokas, Open Stretch hyödyttää.",
    },
    # V64-4 (L7)
    {
        "Kohde": "V64-4 (L7)",
        "Hevonen": "#4 Nightrain",
        "Peliprosentti": 34.0,
        "Arvio %": 40.0,
        "Unibet": 1.95,
        "Perustelu": "Halsoperoitu, hyvä treeneissä ja kova spetsinimi.",
    },
    {
        "Kohde": "V64-4 (L7)",
        "Hevonen": "#9 Fabulous N'Away",
        "Peliprosentti": 21.0,
        "Arvio %": 22.0,
        "Unibet": 5.50,
        "Perustelu": "A-ryhmän hevonen, ravatessaan todella vahva.",
    },
    {
        "Kohde": "V64-4 (L7)",
        "Hevonen": "#11 Global General",
        "Peliprosentti": 5.0,
        "Arvio %": 14.0,
        "Unibet": 6.00,
        "Perustelu": "💥 YLLÄTTÄJÄ (<10%): Alipelattu haastaja Unibetin kertoimella.",
    },
    # V64-5 (L8)
    {
        "Kohde": "V64-5 (L8)",
        "Hevonen": "#4 Carltex",
        "Peliprosentti": 51.0,
        "Arvio %": 36.0,
        "Unibet": 2.55,
        "Perustelu": "Spetsfavorit, mutta pelattu liian suureksi.",
    },
    {
        "Kohde": "V64-5 (L8)",
        "Hevonen": "#2 Lauser",
        "Peliprosentti": 4.0,
        "Arvio %": 16.5,
        "Unibet": 9.75,
        "Perustelu": (
            "🔥 DAGENS SKRÄLL! TR Median ykköskuvio. Täta starter sopii"
            " Berghille!"
        ),
    },
    {
        "Kohde": "V64-5 (L8)",
        "Hevonen": "#3 From Free D.L.",
        "Peliprosentti": 21.0,
        "Arvio %": 20.0,
        "Unibet": 4.35,
        "Perustelu": "Untersteinerin uusi ratsu.",
    },
    {
        "Kohde": "V64-5 (L8)",
        "Hevonen": "#6 Isaac Wynn",
        "Peliprosentti": 9.0,
        "Arvio %": 15.0,
        "Unibet": 4.35,
        "Perustelu": "💥 YLLÄTTÄJÄ (<10%): Barfota r/o muutos.",
    },
    # V64-6 (L9)
    {
        "Kohde": "V64-6 (L9)",
        "Hevonen": "#3 Ugalli",
        "Peliprosentti": 51.0,
        "Arvio %": 34.0,
        "Unibet": 2.65,
        "Perustelu": "Goopin suosikki, mutta haavoittuvainen.",
    },
    {
        "Kohde": "V64-6 (L9)",
        "Hevonen": "#2 Deadly Map",
        "Peliprosentti": 9.0,
        "Arvio %": 15.0,
        "Unibet": 6.50,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ (<10%): Korkea luokka (Elitloppshelgen-voittaja)."
        ),
    },
    {
        "Kohde": "V64-6 (L9)",
        "Hevonen": "#4 Arnie Silvio",
        "Peliprosentti": 17.0,
        "Arvio %": 16.0,
        "Unibet": 6.25,
        "Perustelu": "Varma puristaja eturivistä.",
    },
]

# TOTEUTUNEET TULOKSET (Seuranta)
tulokset_data = [
    {"Kohde": "V64-1 (L4)", "Voittaja": "#7", "Kerroin_Toteutunut": 1.60},
    {"Kohde": "V64-2 (L5)", "Voittaja": "#6", "Kerroin_Toteutunut": 3.25},
    {"Kohde": "V64-3 (L6)", "Voittaja": "#4", "Kerroin_Toteutunut": 3.15},
    {"Kohde": "V64-4 (L7)", "Voittaja": "#4", "Kerroin_Toteutunut": 1.95},
    {"Kohde": "V64-5 (L8)", "Voittaja": "#2", "Kerroin_Toteutunut": 9.75},
    {"Kohde": "V64-6 (L9)", "Voittaja": "#3", "Kerroin_Toteutunut": 2.65},
]

df_vihjeet = pd.DataFrame(vihjeet_data)
df_tulokset = pd.DataFrame(tulokset_data)

# ----------------- ANALYYSI & LASKENTA -----------------
df_vihjeet["Paras Kerroin"] = df_vihjeet["Unibet"]
df_vihjeet["EV"] = (df_vihjeet["Arvio %"] / 100.0) * df_vihjeet["Paras Kerroin"]

# Automaattinen osuman tarkistus
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
    st.sidebar.success(
        f"Simulaation (6 oikein) arvioitu osumatodennäköisyys: {hit_rate:.2f} %"
    )

kokonaispanos = len(df_vihjeet) * panos_per_vihje
voittaneet = df_vihjeet[df_vihjeet["Voitti"]]
palautus = (voittaneet["Paras Kerroin"] * panos_per_vihje).sum()
netto = palautus - kokonaispanos
roi = (palautus / kokonaispanos * 100) if kokonaispanos > 0 else 0

# ----------------- TULOSTEN NÄYTTÖ -----------------
st.subheader("📊 V64 Kierroksen Yhteenveto & ROI")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Vihjeiden Määrä", f"{len(df_vihjeet)} kpl")
m2.metric("Osuneet Vihjeet", f"{len(voittaneet)} / {len(df_vihjeet)}")
m3.metric(
    f"Nettotulos ({panos_per_vihje:.0f} € panokselle)",
    f"{palautus:.2f} €",
    delta=f"{netto:.2f} €",
)
m4.metric("Palautusprosentti (ROI)", f"{roi:.1f} %")

st.divider()

# 🔥 ALLE 10 % YLLÄTTÄJÄT
st.subheader("🔥 Asiantuntija-nostot: Alle 10 % Alipelatut Yllättäjät")
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

# EV-Suodatettu vihjetaulukko
st.subheader("🎯 V64 Kohdekohtainen Analyysi & EV")
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
            "Voitti",
            "Perustelu",
        ]
    ].sort_values(by="EV", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("🏁 Toteutuneet Voittajat vs Vihjeet")
taulukko_vertailu = df_tulokset.merge(
    df_vihjeet[["Kohde", "Hevonen", "Paras Kerroin", "Voitti", "EV"]],
    on="Kohde",
    how="left",
)
st.dataframe(taulukko_vertailu, use_container_width=True, hide_index=True)
