import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Odotusarvot - Färjestad",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Odotusarvo- ja Simulaatiotyökalu (Ilta-asetus)")
st.caption(
    "Färjestad – Syötä illalla klo 18 jälkeen viralliset kertoimet"
    " päivittyviin kenttiin."
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

# ----------------- KAIKKI HEVOSET (Kertoimet aluksi tyhjinä / None) -----------------
vihjeet_data = [
    # --- V85-1 (L5) ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Arvio %": 55.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Selvä suosikki, Goopin luokkahevonen (3/3 voittoa).",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#1 Licorice Sisu",
        "Peliprosentti": 15.0,
        "Arvio %": 18.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Kihlström kyydissä, varmin keulahevonen mailille.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Arvio %": 10.0,
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "U-tallin huipputamma, hakee suosikkipaikkaa keulasta.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Skylight",
        "Peliprosentti": 22.0,
        "Arvio %": 24.0,
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Spurtade hyvin Sto-EM:ssä, kova haastaja.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#1 Rya Håleryd",
        "Peliprosentti": 8.0,
        "Arvio %": 14.0,
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Kärkipään tamma tähän vaativaan tammalähtöön.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#2 Stens Rubin",
        "Peliprosentti": 6.0,
        "Arvio %": 12.0,
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Tjomslandin huippuhevonen, kovan luokan suosikki.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#1 Jaguar Ima",
        "Peliprosentti": 4.0,
        "Arvio %": 11.0,
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": "Selvä suosikki, sopiva 2640 metrin matka.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#1 Kaxig In",
        "Peliprosentti": 9.0,
        "Arvio %": 12.0,
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
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
        "Unibet": None,
        "Coolbet": None,
        "Perustelu": (
            "💥 YLLÄTTÄJÄ: Ruotsin mediatietojen mukaan erinomainen"
            " loppuvetäjä, jos saa hyvän selkäjuoksun."
        ),
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)

st.subheader("📝 Kertoimien syöttö (Päivitä illalla klo 18 jälkeen)")
st.info(
    "Voit syöttää Unibetin ja Coolbetin kertoimet suoraan tähän taulukkoon,"
    " kun ne julkaistaan!"
)

# Streamlit antaa muokata taulukkoa suoraan selaimessa
edited_df = st.data_editor(df_vihjeet, use_container_width=True, num_rows="fixed")

# ----------------- LASKENTA (Käytetään muokatun taulukon kertoimia) -----------------
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

st.divider()

st.subheader("🎯 Kaikki Kohteet ja EV-suodatus")
df_filtered = edited_df[
    (edited_df["EV"].notna()) & (edited_df["EV"] >= osuma_raja_ev)
]
if not df_filtered.empty:
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
else:
    st.warning(
        "Ei vielä osumia EV-suodatuksella. Syötä kertoimet yllä olevaan"
        " taulukkoon!"
    )
