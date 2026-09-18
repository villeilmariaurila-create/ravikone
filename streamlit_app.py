import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Monte Carlo - Färjestad (Eksperttimalli)",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Ravianalyysi & Monte Carlo Simulaatio (Eksperttimalli)")
st.caption(
    "Färjestad – Unionskampen. Päivitetty malli sisältää Jens Sjödénin tilastot"
    " ja Daniel Berglundin tärpit (mm. Fedorovin varoitus & unohdetut"
    " kirijät)."
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

# ----------------- VIHJEDATA (KOKO V85: LÄHDÖT 1-8 / L5-L12) -----------------
vihjeet_data = [
    # --- V85-1 (L5) ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Arvio %": 60.0,
        "Unibet": 1.65,
        "Coolbet": 1.60,
        "Perustelu": (
            "Kuvan pelijakauman selvä suosikkipilari (62 %)[cite: 1]. B."
            " Goopin luokkahevonen."
        ),
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#1 Licorice Sisu",
        "Peliprosentti": 15.0,
        "Arvio %": 18.0,
        "Unibet": 5.50,
        "Coolbet": 5.25,
        "Perustelu": (
            "Kuvan toinen päämerkki (15 %)[cite: 1]. Kihlström kyydissä,"
            " sisärata."
        ),
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Peliprosentti": 2.0,
        "Arvio %": 8.0,
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": (
            "💥 BERGLUNDIN NOSTO: Vahvin norjalainen vieras, näyttänyt"
            " terävältä."
        ),
    },
    # --- V85-2 (L6) ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "Peliprosentti": 48.0,
        "Arvio %": 50.0,
        "Unibet": 2.10,
        "Coolbet": 2.05,
        "Perustelu": (
            "Kuvan ykkössuosikki (48 %)[cite: 1]. Berglund: Läge för"
            " favoritposition spets."
        ),
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Skylight",
        "Peliprosentti": 25.0,
        "Arvio %": 26.0,
        "Unibet": 3.75,
        "Coolbet": 3.80,
        "Perustelu": (
            "Kuvan kakkonen (25 %)[cite: 1]. Spurtade bra i Sto-EM, selvä"
            " lokaali motbud."
        ),
    },
    # --- V85-3 (L7) ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "Peliprosentti": 26.0,
        "Arvio %": 28.0,
        "Unibet": 3.50,
        "Coolbet": 3.40,
        "Perustelu": (
            "Kuvan pelatuin (26 %)[cite: 1]. Tässä avoimessa tammalähdössä"
            " vahva merkki."
        ),
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "Peliprosentti": 24.0,
        "Arvio %": 26.0,
        "Unibet": 3.80,
        "Coolbet": 3.75,
        "Perustelu": (
            "Kuvan kakkonen (24 %)[cite: 1]. Vahva esitys viimeksi, tiukka"
            " kamppailu."
        ),
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Peliprosentti": 18.0,
        "Arvio %": 20.0,
        "Unibet": 5.00,
        "Coolbet": 4.80,
        "Perustelu": "Kunto aivan på topp, tekee työtä itse tammalähdössä.",
    },
    # --- V85-4 (L8) ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Arvio %": 35.0,
        "Unibet": 2.75,
        "Coolbet": 2.70,
        "Perustelu": (
            "Kuvan kärki (33 %)[cite: 1]. Sjödénin tilasto: Autostart-kallblodit"
            " suosivat suosikkeja."
        ),
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Peliprosentti": 32.0,
        "Arvio %": 33.0,
        "Unibet": 2.85,
        "Coolbet": 2.80,
        "Perustelu": "Kuvan kakkonen (32 %)[cite: 1]. Vahva haastaja kärkipaikalle.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "Peliprosentti": 16.0,
        "Arvio %": 15.0,
        "Unibet": 6.00,
        "Coolbet": 5.75,
        "Perustelu": "Kuvan kolmas merkki (16 %)[cite: 1]. Nopea avaaja.",
    },
    # --- V85-5 (L9 - Fedorov varoitus) ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Arvio %": 45.0,
        "Unibet": 2.05,
        "Coolbet": 2.00,
        "Perustelu": (
            "Kuvan ylivoimainen suosikki (57 %)[cite: 1]. Isot varustemuutokset"
            " + Färjestads innerspår-haaste (Berglund varoittaa)."
        ),
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "Peliprosentti": 17.0,
        "Arvio %": 24.0,
        "Unibet": 4.50,
        "Coolbet": 4.40,
        "Perustelu": (
            "Kuvan kakkonen (17 %)[cite: 1]. Spår 5 -etu (Färjestadin vahva"
            " ROI-spår)."
        ),
    },
    # --- V85-6 (L10 - Cold Blaze / Oliver Transs R.) ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Arvio %": 55.0,
        "Unibet": 1.75,
        "Coolbet": 1.70,
        "Perustelu": (
            "Kuvan selvä suosikki (59 %)[cite: 1]. Berglundin mahdollinen"
            " 'spik'."
        ),
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Peliprosentti": 6.0,
        "Arvio %": 12.0,
        "Unibet": 8.00,
        "Coolbet": 7.50,
        "Perustelu": "Kuvan haastaja, nopea avaaja ja spets-ehdokas[cite: 1].",
    },
    # --- V85-7 (L11 - Gulddivisionen) ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 36.0,
        "Arvio %": 38.0,
        "Unibet": 2.50,
        "Coolbet": 2.45,
        "Perustelu": (
            "Kuvan suosikki (36 %)[cite: 1]. Tilastoetu: Starttaa suositulta"
            " spår 5:ltä (Färjestadin pluslottning)!"
        ),
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#2 Stens Rubin",
        "Peliprosentti": 17.0,
        "Arvio %": 20.0,
        "Unibet": 4.80,
        "Coolbet": 4.60,
        "Perustelu": (
            "Kuvan kakkonen (17 %)[cite: 1]. Spetsläge, växer en klass i"
            " ledningen."
        ),
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Barack Face",
        "Peliprosentti": 14.0,
        "Arvio %": 16.0,
        "Unibet": 6.00,
        "Coolbet": 5.75,
        "Perustelu": "Kuvan kolmas (14 %)[cite: 1]. Finntack yankee -vagn.",
    },
    # --- V85-8 (L12 - Sjödén / Skrällprofil) ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Arvio %": 35.0,
        "Unibet": 2.60,
        "Coolbet": 2.55,
        "Perustelu": (
            "Kuvan suosikki (38 %)[cite: 1]. Kapasiteetti riittää pitkälle."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "Peliprosentti": 20.0,
        "Arvio %": 24.0,
        "Unibet": 4.20,
        "Coolbet": 4.00,
        "Perustelu": (
            "Kuvan kakkonen (20 %)[cite: 1]. Luokkansa ykkönen takamatkalta."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#2 Mr Carnation",
        "Peliprosentti": 18.0,
        "Arvio %": 16.0,
        "Unibet": 5.00,
        "Coolbet": 4.80,
        "Perustelu": "Kuvan kolmas (18 %)[cite: 1]. Vahva pelihevonen paalulta.",
    },
]

# TOTEUTUNEET TULOKSET (Lähdöt 1–8)
tulokset_data = [
    {"Kohde": "V85-1", "Voittaja": "#2 Mohawk", "Kerroin_Toteutunut": 1.65},
    {"Kohde": "V85-2", "Voittaja": "#5 Nilla Lane", "Kerroin_Toteutunut": 2.10},
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
st.sidebar.subheader("🎲 Monte Carlo Ajo (Eksperttimalli)")
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
        f"Simulaation osumatodennäköisyys (Eksperttimalli): {hit_rate:.2f} %"
    )

kokonaispanos = len(df_vihjeet) * panos_per_vihje
voittaneet = df_vihjeet[df_vihjeet["Voitti"]]
palautus = (voittaneet["Paras Kerroin"] * panos_per_vihje).sum()
netto = palautus - kokonaispanos
roi = (palautus / kokonaispanos * 100) if kokonaispanos > 0 else 0

# ----------------- TULOSTEN NÄYTTÖ -----------------
st.subheader("📊 V85 Kierroksen Yhteenveto & ROI")

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
st.subheader("🔥 Nostot: Alipelatut Yllättäjät")
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
st.subheader("🎯 V85 Kohdekohtainen Analyysi & EV")
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
