import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Yllättäjät - Färjestad",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Yllättäjäanalyysi & Simulaatio (Lähdöittäin)")
st.caption(
    "Färjestad – Kaikki alipelatut yllättäjät (< 10 %) ryhmiteltynä"
    " lähdöittäin (valmentajakommentit, varusteet & lähtöpaikat)."
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

# ----------------- KAIKKI HEVOSET & YLLÄTTÄJÄT LÄHDÖTTÄIN -----------------
vihjeet_data = [
    # --- V85-1 (L5) ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Arvio %": 55.0,
        "Unibet": 1.65,
        "Coolbet": 1.60,
        "Perustelu": "Selvä suosikki, Goopin luokkahevonen (3/3 voittoa).",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#1 Licorice Sisu",
        "Peliprosentti": 15.0,
        "Arvio %": 18.0,
        "Unibet": 5.50,
        "Coolbet": 5.25,
        "Perustelu": "Kihlström kyydissä, varmin keulahevonen mailille.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Arvio %": 10.0,
        "Unibet": 10.00,
        "Coolbet": 9.50,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Mielenkiintoinen haastaja, ensi kertaa ilman"
            " kenkiä (barfota r/o)!"
        ),
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Glaziers Wondergirl",
        "Peliprosentti": 5.0,
        "Arvio %": 8.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Varustemuutos (amerikkalaiset kärryt +"
            " korvapallot), nopea avaaja."
        ),
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Peliprosentti": 2.0,
        "Arvio %": 6.0,
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Daniel Berglundin nosto – vahvin norjalainen"
            " vieras, näyttänyt erittäin terävältä."
        ),
    },
    # --- V85-2 (L6) ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#4 Nilla Lane",
        "Peliprosentti": 35.0,
        "Arvio %": 34.0,
        "Unibet": 2.85,
        "Coolbet": 2.90,
        "Perustelu": "U-tallin huipputamma, hakee suosikkipaikkaa keulasta.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Skylight",
        "Peliprosentti": 22.0,
        "Arvio %": 24.0,
        "Unibet": 3.75,
        "Coolbet": 3.80,
        "Perustelu": "Spurtade hyvin Sto-EM:ssä, kova haastaja.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#1 Rya Håleryd",
        "Peliprosentti": 8.0,
        "Arvio %": 14.0,
        "Unibet": 9.00,
        "Coolbet": 8.50,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Viimeksi laukkasi voimissaan. Sisärata tarjoaa"
            " täydellisen reissun sisärataa pitkin."
        ),
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Kinky Boots",
        "Peliprosentti": 3.0,
        "Arvio %": 7.0,
        "Unibet": 30.00,
        "Coolbet": 28.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Varustemuutos (Can't see back -bländare),"
            " valmentajan mukaan kyttää sopivaa selkäjuoksua."
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
        "Perustelu": "Kärkipään tamma tähän vaativaan tammalähtöön.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#2 Stens Rubin",
        "Peliprosentti": 6.0,
        "Arvio %": 12.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Todella nopea avaaja paalulta, varusteena"
            " murphybländare vasemmalle."
        ),
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Peliprosentti": 2.0,
        "Arvio %": 9.0,
        "Unibet": 25.00,
        "Coolbet": 22.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Kunto on aivan tapissaan, valmentajakommenttien"
            " mukaan kestävä tekemään itse töitä."
        ),
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#8 Ginevra Ek",
        "Peliprosentti": 6.0,
        "Arvio %": 11.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Gocciadoron tamma, testataan Finntack Yankee"
            " -kärryillä voltista!"
        ),
    },
    # --- V85-4 (L8) ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Arvio %": 35.0,
        "Unibet": 2.75,
        "Coolbet": 2.70,
        "Perustelu": "Tjomslandin huippuhevonen, kovan luokan suosikki.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#1 Jaguar Ima",
        "Peliprosentti": 4.0,
        "Arvio %": 11.0,
        "Unibet": 16.00,
        "Coolbet": 15.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Berglundin passas – spurtasi viimeksi 1.11 viimeiset"
            " 1100m häiriöstä huolimatta. Hirmuiskussa!"
        ),
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#10 Voje Lotta",
        "Peliprosentti": 3.0,
        "Arvio %": 9.0,
        "Unibet": 22.00,
        "Coolbet": 20.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Mielenkiintoinen balanssimuutos – ensimmäistä kertaa"
            " barfota runt om (kokonaan kengättä)!"
        ),
    },
    # --- V85-5 (L9) ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Arvio %": 45.0,
        "Unibet": 2.05,
        "Coolbet": 2.00,
        "Perustelu": (
            "Jättisuosikki, mutta Berglund varoittaa vaikeasta sisäradasta"
            " Färjestadissa."
        ),
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#3 Soot Blaze",
        "Peliprosentti": 5.0,
        "Arvio %": 10.0,
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Mats E Djuse ohjastaa, tulinen loppuveto jos saa"
            " oikeat selät eteensä."
        ),
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Miguel",
        "Peliprosentti": 5.0,
        "Arvio %": 9.0,
        "Unibet": 14.00,
        "Coolbet": 13.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Örjan Kihlström rattaille, Redénin laadukas ori"
            " nousee ryminällä."
        ),
    },
    # --- V85-6 (L10) ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Arvio %": 55.0,
        "Unibet": 1.75,
        "Coolbet": 1.70,
        "Perustelu": "Selvä suosikki, sopiva 2640 metrin matka.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#1 Kaxig In",
        "Peliprosentti": 9.0,
        "Arvio %": 12.0,
        "Unibet": 9.50,
        "Coolbet": 9.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Sisärata ja tsempparihenki. Vaikka Färjestadin ykkönen"
            " on vaativa, voimat ovat tallella."
        ),
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Peliprosentti": 6.0,
        "Arvio %": 10.0,
        "Unibet": 8.50,
        "Coolbet": 8.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Nopea avaaja, voi yllättää keulajuoksulla tai"
            " sujuvalla matkalla."
        ),
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "Peliprosentti": 2.0,
        "Arvio %": 8.0,
        "Unibet": 16.00,
        "Coolbet": 15.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Daniel Berglundin erikoissuosikki tähän lähtöön,"
            " aliarvostettu kapasiteetti."
        ),
    },
    # --- V85-7 (L11) ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 36.0,
        "Arvio %": 38.0,
        "Unibet": 2.50,
        "Coolbet": 2.45,
        "Perustelu": (
            "Gulddivisionen-suosikki, hyötyy Färjestadin tehokkaasta spår 5"
            " -paikasta."
        ),
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#7 Lucky Silver",
        "Peliprosentti": 9.0,
        "Arvio %": 13.0,
        "Unibet": 9.00,
        "Coolbet": 8.50,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Berglundin nosto – huonoista lähtöpaikoista huolimatta"
            " hirmuisia loppuvetoja."
        ),
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Slivovitz Lover",
        "Peliprosentti": 9.0,
        "Arvio %": 11.0,
        "Unibet": 9.50,
        "Coolbet": 9.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Kunto on kohdillaan, pystyy poimimaan väsyvät"
            " lopussa hyvillä kertoimilla."
        ),
    },
    # --- V85-8 (L12) ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Arvio %": 35.0,
        "Unibet": 2.60,
        "Coolbet": 2.55,
        "Perustelu": (
            "Stayerloppetin suosikki, mutta kysymysmerkkinä mahdolliset kengät"
            " jalassa."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#9 Golden Sunrise",
        "Peliprosentti": 2.0,
        "Arvio %": 8.0,
        "Unibet": 18.00,
        "Coolbet": 17.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Sjödénin tilastohuomio – 3140 metrin stayerlähdöissä"
            " nähdään usein jättiyllättäjiä takamatkoilta."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#10 Bourbon Brodde",
        "Peliprosentti": 1.0,
        "Arvio %": 7.0,
        "Unibet": 25.00,
        "Coolbet": 22.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Valmentajakommenttien mukaan stayer-matka on"
            " ehdoton plussa, Höitomt ohjissa."
        ),
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#14 Southbeach Volo",
        "Peliprosentti": 2.0,
        "Arvio %": 8.0,
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Ruotsin mediatietojen mukaan erinomainen"
            " loppuvetäjä, jos saa hyvän selkäjuoksun."
        ),
    },
]

# TOTEUTUNEET TULOKSET
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

# ----------------- LASKENTA -----------------
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

# ----------------- SIMULAATIO -----------------
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

# ----------------- NÄYTTÖ -----------------
st.subheader("📊 V85 Kierroksen Yhteenveto & ROI")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Analysoituja Hevosia", f"{len(df_vihjeet)} kpl")
m2.metric("Osuneet Vihjeet", f"{len(voittaneet)} kpl")
m3.metric("Nettotulos", f"{palautus:.2f} €", delta=f"{netto:.2f} €")
m4.metric("ROI", f"{roi:.1f} %")

st.divider()

# 🔥 YLLÄTTÄJÄT LÄHDÖTTÄIN RYHMITTELTYNÄ (< 10 %)
st.subheader(
    "🔥 Alipelatut Yllättäjät Lähdöittäin (< 10 % Peliprosentti)"
)
st.markdown(
    "Seuraavat hevoset on poimittu tarkasti lähdöittäin valmentajakommenttien,"
    " varustemuutoksien ja asiantuntijavinkkien perusteella:"
)

df_surprises = df_vihjeet[df_vihjeet["Peliprosentti"] < 10.0]

# Käydään läpi kohde kerrallaan
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

st.divider()

st.subheader("🎯 Kaikki Kohteet ja EV-suodatus")
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
