import pandas as pd
import streamlit as st

# Sivun asetukset
st.set_page_config(
    page_title="V85 Hagmyren - Yllättäjät & Ideat",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Hagmyren: KAIKKI Alle 10 % Yllättäjät Perusteluineen")
st.caption(
    "Päivitetty Veikkauksen tuoreimmilla peliprosenteilla ja vihjeanalyysillä."
)

# Datapisteet tuoreilla Veikkauksen peliprosenteilla
data = [
    # V85-1 (L5)
    {
        "Kohde": "V85-1 (L5)",
        "Hevonen": "#5 Macho Cabrio B.B.",
        "Ohjastaja": "Peter G Norman",
        "Peliprosentti": "12.0%",
        "Huomio": "YLI 10 % (Rajatapaus)",
        "Unibet": 9.50,
        "Coolbet": 10.00,
        "Perustelu": "Luokkoriittävä hevonen eturivin paikalta. Kestää kovan matkavauhdin ja pystyy ratkaisemaan peli-ideana.",
    },
    {
        "Kohde": "V85-1 (L5)",
        "Hevonen": "#4 Geisha Road Grif",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "10.0%",
        "Huomio": "Rajalla (10 %)",
        "Unibet": 11.00,
        "Coolbet": 10.50,
        "Perustelu": "Lähdön todennäköisin keulahevonen. Kontio ladannee keulaan, ja jos vauhti saa dämpätä, voi vetää loppuun asti.",
    },
    {
        "Kohde": "V85-1 (L5)",
        "Hevonen": "#8 Herkules A'lir",
        "Ohjastaja": "Rikard N Skoglund",
        "Peliprosentti": "9.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 13.00,
        "Coolbet": 13.50,
        "Perustelu": "Kohtaa pykälää helpomman porukan kuin viimeksi Pronssidivisioonassa. Paikka on hankala, mutta juoksun onnistuessa riittää pitkälle.",
    },
    {
        "Kohde": "V85-1 (L5)",
        "Hevonen": "#6 Henessi Kiev",
        "Ohjastaja": "Oskar J Andersson",
        "Peliprosentti": "5.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 14.50,
        "Coolbet": 15.00,
        "Perustelu": "Viimeksi jäi voimissaan pussiin johtavan taakse. Hieno 4-vuotias, joka on todella varhainen varmistusmerkki.",
    },

    # V85-2 (L6)
    {
        "Kohde": "V85-2 (L6)",
        "Hevonen": "#2 Hip To Be Square / Paalu",
        "Ohjastaja": "Per Lennartsson / Tytti",
        "Peliprosentti": "8.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 11.00,
        "Coolbet": 10.00,
        "Perustelu": "Kylmäveristen nousukas, joka viihtyy hyvin keulassa/kärkijoukossa.",
    },
    {
        "Kohde": "V85-2 (L6)",
        "Hevonen": "#15 Guli Em",
        "Ohjastaja": "Rikard N Skoglund",
        "Peliprosentti": "4.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 16.00,
        "Coolbet": 15.00,
        "Perustelu": "Taka-alalta kova tehtävä, mutta nopea jaloistaan ja toimi loistavasti uudessa kärrytasapainossa viimeksi. Vaarallinen yllättäjä.",
    },
    {
        "Kohde": "V85-2 (L6)",
        "Hevonen": "#10 Re Alkapital",
        "Ohjastaja": "Joakim Eskilsson",
        "Peliprosentti": "3.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 21.00,
        "Coolbet": 22.00,
        "Perustelu": "Treeniraportit erittäin positiivisia. Ravaessaan pystyy yllättämään suosikit.",
    },

    # V85-3 (L7)
    {
        "Kohde": "V85-3 (L7)",
        "Hevonen": "#4 Mizai",
        "Ohjastaja": "Mats E Djuse",
        "Peliprosentti": "9.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 8.50,
        "Coolbet": 9.00,
        "Perustelu": "Mats E Djuse tuntee vastustajat ja uskoo vahvasti keulapaikan ottoon. Nopealla radalla jättiyllätysvalmis keulasta.",
    },

    # V85-4 (L8)
    {
        "Kohde": "V85-4 (L8)",
        "Hevonen": "#12 Lion Sisu / Muut",
        "Ohjastaja": "Eri ohjastajia",
        "Peliprosentti": "9.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 14.00,
        "Coolbet": 15.00,
        "Perustelu": "Tasaiseen spårtrappaan yllätysvalmis venyjä.",
    },
    {
        "Kohde": "V85-4 (L8)",
        "Hevonen": "#3 Ytowns Ulrik",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "0.0%",  # Taulukossa 0% / todella alipelattu
        "Huomio": "JÄTTI-IDEA (< 1 %)",
        "Unibet": 15.00,
        "Coolbet": 16.00,
        "Perustelu": "Näytti avaussuorituskykyä ja voimaa viime keulavoitossaan. Vankka jyrä pitkälle 2640m matkalle.",
    },
    {
        "Kohde": "V85-4 (L8)",
        "Hevonen": "#11 Bear Victor",
        "Ohjastaja": "Ulf Ohlsson",
        "Peliprosentti": "2.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 35.00,
        "Coolbet": 33.00,
        "Perustelu": "Täydellinen jättisensaatio hakuun. Pitkä matka sopii ja Ulf Ohlsson säästää voimia taka-alalta ratkaisukiriin.",
    },

    # V85-5 (L9)
    {
        "Kohde": "V85-5 (L9)",
        "Hevonen": "#2 Prinsesse Ness Tjo",
        "Ohjastaja": "Örjan Kihlström",
        "Peliprosentti": "12.0%",
        "Huomio": "YLI 10 % (Rajatapaus)",
        "Unibet": 9.50,
        "Coolbet": 10.00,
        "Perustelu": "Huippukuntoinen tamma, joka saa Örjan Kihlströmin kyytiin. Jos keulassa kiihdytetään liikaa, Örjan kuittaa lopussa.",
    },
    {
        "Kohde": "V85-5 (L9)",
        "Hevonen": "#3 Tekno Tana",
        "Ohjastaja": "Tomas Pettersson",
        "Peliprosentti": "8.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": "Viimeksi häikäisevä loppuveto voittomatsissa. Erittäin nopeasti avaava tamma, joka voi haastaa suosikin.",
    },

    # V85-6 (L10)
    {
        "Kohde": "V85-6 (L10)",
        "Hevonen": "#3 Pure Jouline",
        "Ohjastaja": "Linus Lönn",
        "Peliprosentti": "6.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 19.00,
        "Coolbet": 18.00,
        "Perustelu": "Ainoa kerta keulasta toi voiton kovia vastaan. Kunto parempi kuin rivi näyttää ja keulaan päästessään voi kantaa koko matkan.",
    },
    {
        "Kohde": "V85-6 (L10)",
        "Hevonen": "#9 Melina Havelock",
        "Ohjastaja": "Fredrik Wallin",
        "Peliprosentti": "7.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 23.00,
        "Coolbet": 25.00,
        "Perustelu": "Saanut kovista ikäluokkakisoista rutiinia ja kohtaa nyt selvästi helpomman vastuksen.",
    },
    {
        "Kohde": "V85-6 (L10)",
        "Hevonen": "#5 Bohemian Maid",
        "Ohjastaja": "Magnus A Djuse",
        "Peliprosentti": "4.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 27.00,
        "Coolbet": 26.00,
        "Perustelu": "Mielenkiintoiset muutokset: kengittä, norjalaiset pääkkärit ja Magnus A Djuse ohjasiin.",
    },

    # V85-7 (L11)
    {
        "Kohde": "V85-7 (L11)",
        "Hevonen": "#3 Graces Bird",
        "Ohjastaja": "Fredrik Plassen",
        "Peliprosentti": "7.0%",
        "Huomio": "JÄTTI-IDEA (< 10 %)",
        "Unibet": 21.00,
        "Coolbet": 19.00,
        "Perustelu": "Vihjeen kirjoittajan OMA hevonen. Paljastaa, että tällä AJETAAN KEULASTA. Hagmyrenin lyhyellä loppusuoralla huipputärppi!",
    },
    {
        "Kohde": "V85-7 (L11)",
        "Hevonen": "#6 Jaguar Godiva",
        "Ohjastaja": "Matsu E Djuse / Pihlström",
        "Peliprosentti": "6.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 18.00,
        "Coolbet": 17.00,
        "Perustelu": "Kestää kovan matkavauhdin ja pystyy tarvittaessa ratkaisemaan kauempaakin.",
    },

    # V85-8 (L12)
    {
        "Kohde": "V85-8 (L12)",
        "Hevonen": "#7 Brilliant Kid",
        "Ohjastaja": "Peter G Norman",
        "Peliprosentti": "6.0%",
        "Huomio": "< 10 % Yllättäjä",
        "Unibet": 12.00,
        "Coolbet": 12.50,
        "Perustelu": "Lähdön todennäköisin keulahevonen (spetsfavorit). Jos saa rauhoittaa matkavauhtia, suosikkien on vaikea tavoittaa.",
    },
]

df = pd.DataFrame(data)

# Sivupalkin suodattimet
st.sidebar.header("Suodata kohteita")
selected_kohde = st.sidebar.selectbox(
    "Valitse kohde:", ["Kaikki kohteet"] + list(df["Kohde"].unique())
)

only_under_10 = st.sidebar.checkbox("Näytä VAIN alle 10 % pelatut", value=True)

# Suodatuksen logiikka
filtered_df = df.copy()

if selected_kohde != "Kaikki kohteet":
    filtered_df = filtered_df[filtered_df["Kohde"] == selected_kohde]

if only_under_10:
    filtered_df = filtered_df[filtered_df["Huomio"].str.contains("< 10 %|JÄTTI-IDEA|Rajalla")]

# Korttirakenne helppoon luettavuuteen
st.subheader("💡 Nostot & Perustelut (Veikkaus-Päivitetty)")

for idx, row in filtered_df.iterrows():
    with st.expander(
        f"{row['Kohde']}: {row['Hevonen']} ({row['Ohjastaja']}) — Veikkaus %: {row['Peliprosentti']} | Unibet: {row['Unibet']:.2f}"
    ):
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            st.metric("Veikkaus Peliosuus", row["Peliprosentti"])
        with col2:
            st.metric("Unibet Kerroin", f"{row['Unibet']:.2f}")
        with col3:
            st.write(f"**Tila:** {row['Huomio']}")
            st.write(f"**Coolbet Kerroin:** {row['Coolbet']:.2f}")

        st.markdown(f"**💡 Perustelu:** {row['Perustelu']}")

st.divider()

# Yhteenvetotaulukko
st.subheader("📊 Kaikki ideat taulukossa")
st.dataframe(
    filtered_df[
        [
            "Kohde",
            "Hevonen",
            "Ohjastaja",
            "Peliprosentti",
            "Huomio",
            "Unibet",
            "Coolbet",
            "Perustelu",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
