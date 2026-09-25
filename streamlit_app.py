import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="GS75 / V85 Simulaattori – Gävle 25.9.",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 GS75 / V85 Simulaattori – Gävle (25.9.2026)")
st.caption(
    "Data päivitetty Gävlen lähtölistojen, varustemuutosten ja Travrondenin kommenttien pohjalta."
)

# ----------------- KOTIRADAN HEVOSLISTA (GÄVLE) -----------------
kotirata_hevostiedot = [
    {
        "Kohde": "GS75-1",
        "Hevonen": "#3 Kattelbo Elon",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Gävlen kotiradan valmennettava.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#1 Oppgårdens Brunte",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Kylin Blom kotiradallaan.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#3 Xanthis Kimberly",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Gävlen kotiradan tamma, hakee keulaan.",
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

# ----------------- GS75 / V85 LÄHDÖT & VARUSTETIEDOT (GÄVLE 25.9.) -----------------
vihjeet_data = [
    # --- GS75-1 (Lähtö 4) ---
    {
        "Kohde": "GS75-1",
        "Hevonen": "#1 Norheim Tor",
        "La %": 5.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 6.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tog pengar i Derbyt, 40m etumatka Ängsraskiin.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#2 Komnes Fina",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasainen suorittaja, vaikea riittää aivan kärkeen.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#3 Kattelbo Elon",
        "La %": 12.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Derby-karsintavoittaja, ratahiitti alla sairastelun jälkeen.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#4 Py Viking",
        "La %": 15.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 16.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva suorittaja, pystyy kamppailemaan kärkisijoista.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#5 Grisle Balder G.L.",
        "La %": 8.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Enemmän vahva kuin nopea, lyhyt matka ei paras etu.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#6 Andre Walter J.M.",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tarvitsee lisää terävyyttä kovassa seurassa.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#7 Ängsrask",
        "La %": 57.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 50.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Ikäluokkatähti ja Derby-voittaja, valtava voittosauma.",
    },
    # --- GS75-2 (Lähtö 5) ---
    {
        "Kohde": "GS75-2",
        "Hevonen": "#1 Don Fanucci Zet",
        "La %": 82.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 78.0,
        "Kengitys_Bonus": 1.05,  # Barfota r/o
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Maailmanluokan tähti, kengittä (barfota r/o). Voitti Kouvolassa leikitellen.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#2 Santos de Castella",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Nopea avaaja, mutta terävyys kadonnut iän myötä.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#3 Dark Roadster",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Sairasteli talvella, ajetaan kiltisti selässä.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#4 Sourire Frö",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyödyllinen suorittaja, ahdas juoksurata haittaa.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#5 Steady Roc",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasainen ja varma suorittaja koviin lähtöihin.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#6 Parveny",
        "La %": 10.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 10.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kova avaaja juoksuradalta, ottanee keulat aluksi.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#7 Nephtys Boko",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyödyllinen tamma, orien kohtaaminen tekee tiukkaa.",
    },
    # --- GS75-3 (Lähtö 6) ---
    {
        "Kohde": "GS75-3",
        "Hevonen": "#1 Oppgårdens Brunte",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva ja hidas kiihtymään, 3140m sopii matkana.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#2 Marodin",
        "La %": 8.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 10.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Mennyt tasaisen varmasti, matka sopii erinomaisesti.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#3 Burman",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Purottanut tasaisesti ilman terävintä kärkeä.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#4 Trö Hav",
        "La %": 7.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 8.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Uusi tulokas Tjomslandille, elää voimillaan.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#5 Mötje Meir",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vauhtia löytyy mutta erittäin laukkaherkkä.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#6 Höstbo Elina",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Joutui hiittiin toistuvien laukkojen vuoksi.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#7 Ingen",
        "La %": 6.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Voittanut aiemmin pitkällä matkalla (3140m).",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#8 Guli Kasper",
        "La %": 9.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 11.0,
        "Kengitys_Bonus": 1.02,  # Kengitysmuutos
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Uusi valmennus (Pihlström) ja kengitystä muutetaan taakse.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#9 Pyseidon",
        "La %": 42.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 40.0,
        "Kengitys_Bonus": 1.05,  # Barfota fram
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Hienossa kunnossa, kenkätön balanssi edessä toiminut loistavasti.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#10 Tore E.",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Palaa tauolta, Mats E Djuse vahvistaa rattailla.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#11 Hulte Jannina",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Halpa voitto aiemmin, vaikea paikka voltissa.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#12 Trönö Borken",
        "La %": 20.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 18.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Erittäin vahva karhu 3000 metrille, ykköshaastaja.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#13 Orrgårns Tycko",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Varma suorittaja, mutta 60m pakki on liikaa.",
    },
    # --- GS75-4 (Lähtö 7) ---
    {
        "Kohde": "GS75-4",
        "Hevonen": "#1 Inkallad",
        "La %": 12.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Voitti helposti spetsistä maanantaina, loistopaikka.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#2 Kjölstad Gutten",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 5.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyvä voitto viimeksi, mutta taso nousee kovasti.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#3 L.Q.Laban",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 0.98,  # Normaali balanssi takaisin
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Palataan normaaliin balanssiin helpotuksen jälkeen.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#4 Tekno Ture",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Enemmän vahva kuin nopea, totokandidaatti.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#5 Sauron",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Mött halpoja porukoita, pitää parantaa ennätystä.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#6 Lomeglimt",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.02,  # Bootseja kevennetty
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Humörbetonad, riisutaan bootseista tähän lähtöön.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#7 Bäcklös Borken",
        "La %": 38.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 35.0,
        "Kengitys_Bonus": 1.02,  # Järnskor ympäriinsä
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Kulltopp, treenaa kovaa. Paluu rautakenkiin toimii paremmin.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#8 Alf",
        "La %": 8.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyvä uran alku, norjan Derby-kävijä.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#9 Järvsö Jan",
        "La %": 6.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Aloitti 4 voitolla, vaikeampi karkelo nyt.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#10 Troll Knut",
        "La %": 24.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 23.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Molemmin puolin Kriterium-finaalisti, päähaastaja.",
    },
    # --- GS75-5 (Lähtö 8) ---
    {
        "Kohde": "GS75-5",
        "Hevonen": "#1 Mary Wadd",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyvä paikka, mutta riittävyys kärkitaistoon tiukalla.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#2 Global Deadline",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Viron menestyjä, hyvä paikka yllättää totosijalle.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#3 Xanthis Kimberly",
        "La %": 35.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Ikäluokkaeliittiä, nopea avaaja ja valmentaja ajaa keulasta.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#4 Noa Transs R.",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Monté/sulky -yhdistelijä, kova porukka vastassa.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#5 Elin Avant",
        "La %": 12.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kapabel tamma, hoidettu viime kisan jälkeen. Haastaja.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#6 Ecuador Broline",
        "La %": 22.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 20.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Mennnyt kovaa ikäluokkalähdöissä, passaava tehtävä.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#7 Bilbao Ace",
        "La %": 6.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Keulavoitto viimeksi Östersundissa, ulkorata haittaa.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#8 Evita Jacase",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Ulkopaikalta vaikea ehtiä terävimpään kärkeen.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#9 Pralines",
        "La %": 17.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 18.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Örjan Kihlström selässä taka-alalta, erittäin mielenkiintoinen.",
    },
    # --- GS75-6 (Lähtö 9) ---
    {
        "Kohde": "GS75-6",
        "Hevonen": "#1 Belse Tösen",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.5,
        "Kengitys_Bonus": 0.97,  # Kengät jalkaan
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Laukannut kahdesti, juoksee nyt kengät jalassa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#2 Sol Flamma",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Ajoittain hyvä vauhti, mutta kunto ailahtelee.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#3 Gangsi",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Pieni tamma, joka hakee lähinnä pikkurahoja.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#4 Hög Decibel",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 5.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Varma suorittaja, SM-kisa oli liian kova.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#5 Klack Tea",
        "La %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Juoksee usein, mutta kärki menee liian kovaa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#6 Lille Rose G.L.",
        "La %": 8.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyvä aika viimeksi, kunto nousussa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#7 Eldida",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Mats E Djuse vahvistuksena kärryillä, yllätysvalmis.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#8 Lysjö Isa",
        "La %": 6.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Örjan Kihlström rattaille, parantaa aina otteitaan.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#9 Lokatt",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasoituksen keskellä, hakee rahasijaa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#10 Myllkärr Christina",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva tamma, mutta voittaa harvoin.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#11 Guli Stina",
        "La %": 12.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 0.97,  # Kengät takaisin SM:n jälkeen
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Nuoruuden tähti, kengät jalassa jälleen SM-kisan jälkeen.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#12 Hulte Annika",
        "La %": 35.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Vahva SM-kolmonen, laskee sopivaan tehtävään. Ykkössuosikki.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#13 Tekno Tana",
        "La %": 18.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 16.0,
        "Kengitys_Bonus": 1.02,  # Mahdollinen etukengättömyys
        "Karryt_Bonus": 1.02,  # Hybridikärryt
        "Unibet": None,
        "Perustelu": "Erittäin vahva, mahdollisesti etukengittä ja hybridikärryillä.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#14 Ethel",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "60m pakki tekee tehtävästä lähes mahdottoman.",
    },
    # --- GS75-7 (Lähtö 10) ---
    {
        "Kohde": "GS75-7",
        "Hevonen": "#1 Guli Hektor",
        "La %": 10.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 11.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva loppukiri viimeksi, pussitusvaara ykkösradalla.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#2 Guldhagens Pirat",
        "La %": 8.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasaista laatua, unelmapaikka eturivissä.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#3 Klack Vidar",
        "La %": 12.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 13.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kehittynyt valtavasti kesän aikana, nopea avaaja.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#4 G.G.Qurre",
        "La %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva vääntäjä, nopeus ei tahdo riittää autolähdöissä.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#5 Guli Em",
        "La %": 20.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 22.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.04,  # Amerikansk vagn
        "Unibet": None,
        "Perustelu": "💥 Hienossa iskussa, voitti Färjestadissa. Jenkkikärryt perään!",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#6 Eld Prinsen",
        "La %": 5.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 5.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Luokkaa löytyy, mutta kunto hieman kysymysmerkki.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#7 Pyrotek",
        "La %": 25.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 24.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.04,  # Amerikansk vagn
        "Unibet": None,
        "Perustelu": "💥 Pihlström luottaa voittoon, hyötyy autolähdöstä ja jenkkikärryistä!",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#8 Hibovalle",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Saanut huonon paikan spårtrappassa, vaatii tuuria.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#9 Guldhagens Oscar",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tyytyväinen keulasta sijoitukseen, takarivistä haastavaa.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#10 Gör Som Jag Vill",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.03,  # Amerikansk vagn
        "Unibet": None,
        "Perustelu": "Ravi parantunut, autolähtö ja jenkkikärryt takarivistä sopivat.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#11 Blomsterprinsen",
        "La %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kehitys polkee paikallaan, vaikea paikka ehtiä kärkeen.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#12 Höstbo Wille",
        "La %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Aina yllätysvalmis, mutta lähtöpaikka on yön musta.",
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

# LASKETAAN LOPULLINEN ARVIO KAIKILLA PAINOTUKSILLA:
# (Oma arvio * Kotirata_Bonus * Kengitys_Bonus * Karryt_Bonus)
df_vihjeet["Lopullinen Arvio %"] = (
    df_vihjeet["Oma_Simulaatio_Arvio %"]
    * df_vihjeet["Kotirata_Bonus"]
    * df_vihjeet["Kengitys_Bonus"]
    * df_vihjeet["Karryt_Bonus"]
)

# Normalisoidaan arviot kohteittain tasan 100 prosenttiin
df_vihjeet["Arvio %"] = df_vihjeet.groupby("Kohde")["Lopullinen Arvio %"].transform(
    lambda x: (x / x.sum()) * 100 if x.sum() > 0 else x
)

# Jos kerroin puuttuu (None), asetetaan 0.0
df_vihjeet["Paras Kerroin"] = df_vihjeet["Unibet"].fillna(0.0)

# Lasketaan EV
df_vihjeet["EV"] = np.where(
    df_vihjeet["Paras Kerroin"] > 0,
    (df_vihjeet["Arvio %"] / 100.0) * df_vihjeet["Paras Kerroin"],
    0.0,
)

# Järjestetään taulukko kohteittain
if "Kohde" in df_vihjeet.columns and not df_vihjeet.empty:
    df_vihjeet["Kohde_Num"] = (
        df_vihjeet["Kohde"].str.extract(r"(\d+)").astype(float)
    )
    df_vihjeet = df_vihjeet.sort_values(
        by=["Kohde_Num", "Arvio %"], ascending=[True, False]
    ).drop(columns=["Kohde_Num"])

# ----------------- MONTE CARLO SIMULAATIO -----------------
st.sidebar.subheader("🎲 Monte Carlo Ajo")
if st.sidebar.button("Aja Simulaatio"):
    sim_results = []
    kohde_groups = df_vihjeet.groupby("Kohde", sort=False)
    for _ in range(num_simulations):
        row_win = []
        for kohde, group in kohde_groups:
            probs = group["Arvio %"].values / group["Arvio %"].sum()
            winner_idx = np.random.choice(len(group), p=probs)
            row_win.append(group.iloc[winner_idx]["Arvio %"] > 0)
        sim_results.append(all(row_win))
    st.sidebar.success("Simulaatio ajettu onnistuneesti!")

# ----------------- NÄYTÖT -----------------
st.subheader("🏠 Gävlen Kotiradan Hevoset")
st.dataframe(df_kotirata, use_container_width=True, hide_index=True)

st.divider()

st.subheader("📊 Lähtöjen Voittotodennäköisyydet ja Peliarvot (Gävle)")
st.dataframe(
    df_vihjeet[
        [
            "Kohde",
            "Hevonen",
            "La %",
            "Prosentti_Muutos",
            "Arvio %",
            "Kengitys_Bonus",
            "Karryt_Bonus",
            "Paras Kerroin",
            "EV",
            "Perustelu",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("🔥 Potentiaaliset Yllättäjät (< 10 % Peliprosentti)")
df_surprises = df_vihjeet[df_vihjeet["La %"] < 10.0]

st.dataframe(
    df_surprises[
        [
            "Kohde",
            "Hevonen",
            "La %",
            "Prosentti_Muutos",
            "Arvio %",
            "Kengitys_Bonus",
            "Karryt_Bonus",
            "Paras Kerroin",
            "EV",
            "Perustelu",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
