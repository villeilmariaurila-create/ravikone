import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Hagmyren - Kaikki Yllättäjät", layout="wide"
)

st.title("🏇 V85 Hagmyren: KAIKKI Alle 10 % Yllättäjät Perusteluineen")
st.caption(
    "Simulaation ja kertoimien pohjalta poimittu jokainen alle 10 % pelattu ideavaljakko tarkan analyysin kera."
)

data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#5 Macho Cabrio B.B.",
        "Ohjastaja": "Peter G Norman",
        "Peliprosentti": "9.0%",
        "Unibet": 9.50,
        "Coolbet": 10.00,
        "Perustelu": "Luokkoriittävä hevonen, joka saa eturivin paikalta 5 hyvät asemat toisesta ulkoa tai johtavan rinnalta. Kestää kovan matkavauhdin ja pystyy Hagmyrenin lyhyellä loppusuoralla ratkaisemaan peli-ideana.",
    },
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#4 Geisha Road Grif",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "5.5%",
        "Unibet": 15.00,
        "Coolbet": 14.50,
        "Perustelu": "Italialaissukuinen tamma kokeneen Jorma Kontion ohjastamana. Viime kisan kakkossija osoitti kunnon olevan kohdallaan, ja nelosradalta tie on auki taloudelliseen juoksuun keularyhmän tuntumassa.",
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Hevonen": "#4 Silke Sjarmör",
        "Ohjastaja": "Carl Johan Jepson",
        "Peliprosentti": "7.0%",
        "Unibet": 12.00,
        "Coolbet": 12.50,
        "Perustelu": "Kapasiteetiltaan vahva norjalainen kylmäverinen. Ohjastajavahvistus Carl Johan Jepson tuo huomattavan lisäedun taktiikkaan, jolloin kiri kantaa pussituksen vältettäessä.",
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Hevonen": "#10 Re Alkapital",
        "Ohjastaja": "Joakim Eskilsson",
        "Peliprosentti": "3.0%",
        "Unibet": 26.00,
        "Coolbet": 25.00,
        "Perustelu": "Huono tulossarja hämää suuria massoja, minkä vuoksi peliprosentti on painunut pohjiin. Väläytellyt aiemmin luokkaa, jolla taistellaan kärkikohteissa laukan sattuessa muille.",
    },
    {
        "Kohde": "V85-3 (Lopp 7)",
        "Hevonen": "#4 Mizai",
        "Ohjastaja": "Per Lennartsson",
        "Peliprosentti": "7.5%",
        "Unibet": 11.00,
        "Coolbet": 11.50,
        "Perustelu": "Pikamatkalla (1640 m) erittäin nopea avaaja. Per Lennartsson saa tammalla sisäradalta heti paikan kärkiporukasta, mistä se pystyy yllättämään suosikit.",
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Hevonen": "#3 Ytowns Ulrik",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "4.5%",
        "Unibet": 17.00,
        "Coolbet": 18.00,
        "Perustelu": "Pitkälle matkalle (2640 m) vankka ja tasainen jyrä Jorma Kontiolla vahvistettuna. Jaksaa puskemaan raskaan matkavauhdin loppuun asti muiden hyytyessä.",
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Hevonen": "#11 Bear Victor",
        "Ohjastaja": "Ulf Ohlsson",
        "Peliprosentti": "2.3%",
        "Unibet": 10.91,
        "Coolbet": 11.00,
        "Perustelu": "Erittäin alipelattu suhteessa voittajakertoimeensa (10.91). Mestarikuski Ulf Ohlsson ohjastaa ja pystyy takarivistä ajamaan säästeliäästi pitkällä matkalla iskien lopussa.",
    },
    {
        "Kohde": "V85-5 (Lopp 9)",
        "Hevonen": "#4 Hulte Alva",
        "Ohjastaja": "Linda S Hedström",
        "Peliprosentti": "6.0%",
        "Unibet": 18.00,
        "Coolbet": 17.50,
        "Perustelu": "Suurmurskaajasuosikki Majblomsterin varjossa kulkeva tasaisen varma tamma, joka hyötyy erinomaisesta eturivin lähtöpaikasta ja tarkasta juoksusta.",
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Hevonen": "#3 Pure Jouline",
        "Ohjastaja": "Linus Lönn",
        "Peliprosentti": "4.0%",
        "Unibet": 21.00,
        "Coolbet": 20.00,
        "Perustelu": "Kierroksen pääskrälli volttilähdöstä. Saa nopean lähdön paalulta, kun suosikit joutuvat kiertämään takamatkalta runsaassa liikenneruuhkassa.",
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Hevonen": "#8 Brionne",
        "Ohjastaja": "Rikard N Skoglund",
        "Peliprosentti": "3.5%",
        "Unibet": 28.00,
        "Coolbet": 26.00,
        "Perustelu": "Pitkä 2640 metrin matka suosii hevosta. Saa hyvän peitteisen juoksun sisäradalla ja Rikard N Skoglundin ajamana kyseessä on merkittävä peli-idea.",
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Hevonen": "#3 Graces Bird",
        "Ohjastaja": "Fredrik Plassen",
        "Peliprosentti": "7.8%",
        "Unibet": 13.50,
        "Coolbet": 14.00,
        "Perustelu": "Tulinen avaaja ja lähdön todennäköisin keulakandidaatti. Hagmyrenin lyhyellä 170 metrin loppusuoralla keulasta ajava valjakko on tilastollisesti vahvoilla.",
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Hevonen": "#1 Bruce Braylon",
        "Ohjastaja": "Per Lennartsson",
        "Peliprosentti": "5.0%",
        "Unibet": 19.00,
        "Coolbet": 18.50,
        "Perustelu": "Ykkösradalta taattu taloudellinen sisäradan juoksu johtavan takana. Iskee terävästi tilan avautuessa loppusuoralla Per Lennartssonin kannustamana.",
    },
    {
        "Kohde": "V85-8 (Lopp 12)",
        "Hevonen": "#9 Summermusic'nightS",
        "Ohjastaja": "Marcus Lilius",
        "Peliprosentti": "3.5%",
        "Unibet": 31.00,
        "Coolbet": 33.00,
        "Perustelu": "Suorituskyky on huomattavasti tulostaulua parempi. Jos eturivin suosikit pitävät yllä liian kovaa matkavauhtia, tämä valjakko syöksyy kirillään mitalitaisteluun.",
    },
]

df = pd.DataFrame(data)

st.subheader(f"📊 Yhteenvetotaulukko ({len(data)} Hevosta)")
st.dataframe(
    df[
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

st.divider()
st.subheader("🔥 Kaikkien 13 yllättäjän yksityiskohtaiset analyysit")

for item in data:
    with st.container(border=True):
        st.subheader(f"{item['Kohde']}: {item['Hevonen']}")
        st.write(f"**Ohjastaja:** {item['Ohjastaja']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Peliprosentti",
                value=item["Peliprosentti"],
                delta="ALLE 10%",
                delta_color="normal",
            )
        with col2:
            st.metric(label="Unibet Kerroin", value=item["Unibet"])
        with col3:
            st.metric(label="Coolbet Kerroin", value=item["Coolbet"])

        st.info(f"💡 **Simulaation perustelu:** {item['Perustelu']}")
