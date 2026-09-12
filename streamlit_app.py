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
    "Vihjeanalyysin ja Unibet-kertoimien pohjalta kootut alle 10 % pelatut ideavaljakot."
)

# Datapisteet vihjenostojen pohjalta
data = [
    # V85-1
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Henessi Kiev",
        "Ohjastaja": "Oskar J Andersson",
        "Peliprosentti": "4.0%",
        "Unibet": 14.50,
        "Coolbet": 15.00,
        "Perustelu": "Viimeksi jäi voimissaan pussiin johtavan taakse. Hieno 4-vuotias, joka vältessään johtavan rinnalla juoksemisen on todella varhainen varmistusmerkki.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Geisha Road Grif",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "5.5%",
        "Unibet": 11.00,
        "Coolbet": 10.50,
        "Perustelu": "Lähdön todennäköisin keulahevonen. Jorma Kontio ladannee keulaan, ja jos vauhti saa dämpätä toisella puolikkaalla, voi vetää loppuun asti.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#8 Herkules A'lir",
        "Ohjastaja": "Rikard N Skoglund",
        "Peliprosentti": "6.0%",
        "Unibet": 13.00,
        "Coolbet": 13.50,
        "Perustelu": "Kohtaa pykälää helpomman porukan kuin viimeksi Pronssidivisioonassa. Paikka on hankala, mutta juoksun onnistuessa riittää pitkälle.",
    },
    # V85-2
    {
        "Kohde": "V85-2",
        "Hevonen": "#4 Silke Sjarmör",
        "Ohjastaja": "Carl Johan Jepson",
        "Peliprosentti": "7.0%",
        "Unibet": 6.50,
        "Coolbet": 7.00,
        "Perustelu": "Keulafavoriitti ensimmäiseen kaarteeseen. Hoitojen jälkeen parempi ja viihtyy Hagmyrenillä (2 starttia, 2 voittoa). Johtaa pitkään.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#10 Re Alkapital",
        "Ohjastaja": "Joakim Eskilsson",
        "Peliprosentti": "3.0%",
        "Unibet": 21.00,
        "Coolbet": 22.00,
        "Perustelu": "Treeniraportit erittäin positiivisia. Ravaessaan pystyy yllättämään suosikit, vaikka ohjastajakokemus V85-tasolta on vähäinen.",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#15 Guli Em",
        "Ohjastaja": "Rikard N Skoglund",
        "Peliprosentti": "4.5%",
        "Unibet": 16.00,
        "Coolbet": 15.00,
        "Perustelu": "Taka-alalta kova tehtävä, mutta nopea jaloistaan ja toimi loistavasti uudessa kärrytasapainossa viimeksi. Vaarallinen yllättäjä.",
    },
    # V85-3
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Jerka Sting",
        "Ohjastaja": "Claes Sjöström",
        "Peliprosentti": "8.5%",
        "Unibet": 7.50,
        "Coolbet": 8.00,
        "Perustelu": "Vihjekirjoittajan A-hevonen! Jos megaratsut Mizai ja Before Takeoff kiihdyttävät rajusti keulasta, Jerka Sting kuittaa lopussa tulisen loppuvetonsa ansiosta.",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#4 Mizai",
        "Ohjastaja": "Mats E Djuse",
        "Peliprosentti": "7.5%",
        "Unibet": 8.50,
        "Coolbet": 9.00,
        "Perustelu": "Mats E Djuse tuntee vastustajat ja uskoo vahvasti keulapaikan ottoon. Viimeksi pirteä selästä, nopealla radalla jättiyllätysvalmis keulasta.",
    },
    # V85-4
    {
        "Kohde": "V85-4",
        "Hevonen": "#11 Bear Victor",
        "Ohjastaja": "Ulf Ohlsson",
        "Peliprosentti": "2.3%",
        "Unibet": 35.00,
        "Coolbet": 33.00,
        "Perustelu": "Täydellinen jättisensaatio hakuun. Pitkä matka sopii ja Ulf Ohlsson säästää voimia taka-alalta ratkaisukiriin.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Ytowns Ulrik",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "4.5%",
        "Unibet": 15.00,
        "Coolbet": 16.00,
        "Perustelu": "Näytti avaussuorituskykyä ja voimaa viime keulavoitossaan. Vankka jyrä pitkälle 2640m matkalle.",
    },
    # V85-5
    {
        "Kohde": "V85-5",
        "Hevonen": "#3 Tekno Tana",
        "Ohjastaja": "Tomas Pettersson",
        "Peliprosentti": "5.0%",
        "Unibet": 12.00,
        "Coolbet": 11.00,
        "Perustelu": "Viimeksi häikäisevä loppuveto voittomatsissa. Erittäin nopeasti avaava tamma, joka voi heittää jättisuosikki Majblomsterille todellisen haasteen.",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#2 Prinsesse Ness Tjo",
        "Ohjastaja": "Örjan Kihlström",
        "Peliprosentti": "6.5%",
        "Unibet": 9.50,
        "Coolbet": 10.00,
        "Perustelu": "Huippukuntoinen tamma, joka saa Örjan Kihlströmin kyytiin. Jos 1 ja 3 tappelevat keulasta, Örjan rankaisee lopussa.",
    },
    # V85-6
    {
        "Kohde": "V85-6",
        "Hevonen": "#3 Pure Jouline",
        "Ohjastaja": "Linus Lönn",
        "Peliprosentti": "4.0%",
        "Unibet": 19.00,
        "Coolbet": 18.00,
        "Perustelu": "Ainoa kerta keulasta toi voiton kovia vastaan. Kunto parempi kuin rivi näyttää ja keulaan päästessään voi kantaa koko matkan.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#9 Melina Havelock",
        "Ohjastaja": "Fredrik Wallin",
        "Peliprosentti": "3.5%",
        "Unibet": 23.00,
        "Coolbet": 25.00,
        "Perustelu": "Kohdannut ikäluokkalähdöissä kovia tammoja. Saanut kovista kisoista rutiinia ja kohtaa nyt selvästi helpomman vastuksen.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#5 Bohemian Maid",
        "Ohjastaja": "Magnus A Djuse",
        "Peliprosentti": "3.0%",
        "Unibet": 27.00,
        "Coolbet": 26.00,
        "Perustelu": "Mielenkiintoiset muutokset: kengittä, norjalaiset pääkkärit ja Magnus A Djuse ohjasiin. Yllätysvalmis smyygejuoksulla.",
    },
    # V85-7
    {
        "Kohde": "V85-7",
        "Hevonen": "#3 Graces Bird",
        "Ohjastaja": "Fredrik Plassen",
        "Peliprosentti": "3.5%",
        "Unibet": 21.00,
        "Coolbet": 19.00,
        "Perustelu": "Vihjeen kirjoittajan OMA hevonen. Paljastaa, että tällä AJETAAN KEULASTA. Hagmyrenin 170m loppusuoralla jätti-idea 3-4% pelattuna!",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#2 Pineapple",
        "Ohjastaja": "Carl Johan Jepson",
        "Peliprosentti": "4.5%",
        "Unibet": 15.00,
        "Coolbet": 14.00,
        "Perustelu": "Ensimmäistä kertaa ilman kenkiä (barfota runt om) + CJ Jepson rattailla. Vastasi rajusti ryöstäjiin viimereissulla, yllättää ylivauhdilla.",
    },
    # V85-8
    {
        "Kohde": "V85-8",
        "Hevonen": "#7 Brilliant Kid",
        "Ohjastaja": "Peter G Norman",
        "Peliprosentti": "5.5%",
        "Unibet": 12.00,
        "Coolbet": 12.50,
        "Perustelu": "Lähdön todennäköisin keulahevonen (spetsfavorit). Jos saa rauhoittaa matkavauhtia, suosikkien on vaikea tavoittaa lyhyellä loppusuoralla.",
    },
]

df = pd.DataFrame(data)

# Sivupalkin suodatin helppoon selaukseen
st.sidebar.header("Suodata kohteita")
selected_kohde = st.sidebar.selectbox(
    "Valitse kohde:", ["Kaikki kohteet"] + list(df["Kohde"].unique())
)

if selected_kohde != "Kaikki kohteet":
    filtered_df = df[df["Kohde"] == selected_kohde]
else:
    filtered_df = df

# Päänäkymä: Korttirakenne helppoon luettavuuteen
st.subheader("💡 Nostot & Perustelut (Helppolukuinen näkymä)")

for idx, row in filtered_df.iterrows():
    with st.expander(
        f"{row['Kohde']}: {row['Hevonen']} ({row['Ohjastaja']}) — Pelattu: {row['Peliprosentti']} | Unibet: {row['Unibet']:.2f}"
    ):
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            st.metric("Peliosuus", row["Peliprosentti"])
        with col2:
            st.metric("Unibet Kerroin", f"{row['Unibet']:.2f}")
        with col3:
            st.write(f"**Ohjastaja:** {row['Ohjastaja']}")
            st.write(f"**Coolbet:** {row['Coolbet']:.2f}")

        st.markdown(f"**💡 Perustelu:** {row['Perustelu']}")

st.divider()

# Yhteenvetotaulukko sivun alalaidassa
st.subheader("📊 Kaikki ideat taulukossa")
st.dataframe(
    filtered_df[
        [
            "Kohde",
            "Hevonen",
            "Ohjastaja",
            "Peliprosentti",
            "Unibet",
            "Coolbet",
            "Perustelu",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
