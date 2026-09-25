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
    "Data päivitetty Veikkauksen pelijakaumalla, Gävlen lähtölistoilla sekä valmentajahaastatteluilla."
)

# ----------------- KOTIRADAN HEVOSLISTA (GÄVLE) -----------------
kotirata_hevostiedot = [
    {
        "Kohde": "GS75-1",
        "Hevonen": "#3 Kattelbo Elon",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Gävlen kotiradan valmennettava, etu tutusta radasta ja lyhyestä kuljetuksesta.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#1 Oppgårdens Brunte",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Oskar Kylin Blom kotiradallaan, tutut olosuhteet.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#3 Xanthis Kimberly",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Gävlen kotiradan tamma, hyötyy kotikentän rutiinista spets-ajossa.",
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

# ----------------- GS75 / V85 LÄHDÖT & TIEDOT PAINOTUKSILLA (VEIKKAUS PROSENTIT) -----------------
vihjeet_data = [
    # --- GS75-1 (Lähtö 4) ---
    {
        "Kohde": "GS75-1",
        "Hevonen": "#1 Norheim Tor",
        "Veikkaus %": 9.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 6.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Derby-rahoittaja. 40m etumatka Ängsraskiin nähden antaa pienen taktisen edun.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#2 Komnes Fina",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasaisen varma puurtaja ilman terävintä huippua. Vaikea riittää aivan kärkeen.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#3 Kattelbo Elon",
        "Veikkaus %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "🏠 Kotiratanosto (+3%). Derby-karsintavoittaja, ratahiitti alla sairastelun jälkeen.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#4 Py Viking",
        "Veikkaus %": 15.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 16.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva suorittaja, treenaa hyvin sairastelun jälkeen. Pystyy kamppailemaan kärjessä.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#5 Grisle Balder G.L.",
        "Veikkaus %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Voitti viimeksi, mutta enemmän vahva kuin nopea. Lyhyt matka verottaa mahdollisuuksia.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#6 Andre Walter J.M.",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tarvitsee lisää terävyyttä ja nopeutta näin kovassa seurassa.",
    },
    {
        "Kohde": "GS75-1",
        "Hevonen": "#7 Ängsrask",
        "Veikkaus %": 67.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 50.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Ruotsin Derby-voittaja ja ikäluokkatähti. Takamatkasta huolimatta luokka on omaa luokkaansa.",
    },
    # --- GS75-2 (Lähtö 5) ---
    {
        "Kohde": "GS75-2",
        "Hevonen": "#1 Don Fanucci Zet",
        "Veikkaus %": 86.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 78.0,
        "Kengitys_Bonus": 1.05,  # Barfota r/o
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Maailmanluokan tähti. Kenkätön balanssi (barfota r/o +5%) takaa ylivoimaisen vauhdin.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#2 Santos de Castella",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Nopea avaaja, mutta parhaan terän kadottanut iän myötä. Totosijatoiveet.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#3 Dark Roadster",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Sairasteli talvella, valmentaja ilmoittaa kiltin selkäjuoksun. Ei asiaa voittotaistoon.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#4 Sourire Frö",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyödyllinen veteraani, mutta ahdas nelosrata voltissa tuottaa pienen laukkariskin.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#5 Steady Roc",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasainen suorittaja koviin lähtöihin, hakee puhdasta rahasijaa.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#6 Parveny",
        "Veikkaus %": 8.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 10.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tulossa loistavassa iskussa. Tulinen avaaja juoksuradalta ja ottanee keulat aluksi.",
    },
    {
        "Kohde": "GS75-2",
        "Hevonen": "#7 Nephtys Boko",
        "Veikkaus %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Rehti tamma, mutta kovan orieliitin kohtaaminen tekee voittamisesta haastavaa.",
    },
    # --- GS75-3 (Lähtö 6) ---
    {
        "Kohde": "GS75-3",
        "Hevonen": "#1 Oppgårdens Brunte",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "🏠 Kotiratabonus (+3%). Vahva ja hidas kiihtymään, 3140m matka suosii voimakkaita ominaisuuksia.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#2 Marodin",
        "Veikkaus %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 10.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Mennnyt tasaisen varmasti. Erinomainen fysiikka ja pitkä matka sopivat täydellisesti.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#3 Burman",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasainen puurtaja ilman terävintä voittokärkeä. Elokuussa vastaava matka oli liikaa.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#4 Trö Hav",
        "Veikkaus %": 17.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 8.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tjomslandin uusi orlov-tulokas Norjasta. Elää täysin voimillaan, 3140m leipälaji.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#5 Mötje Meir",
        "Veikkaus %": 0.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vauhtia löytyy taustalta, mutta kärsii suurista laukkariskeistä.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#6 Höstbo Elina",
        "Veikkaus %": 0.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Joutui hiittiradoille toistuvien laukkojen vuoksi. Vain pieni rahasijatoive.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#7 Ingen",
        "Veikkaus %": 5.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Voittanut aiemmin täydellä 3140m matkalla Gävlessä. Ravilla potentiaalinen yllättäjä.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#8 Guli Kasper",
        "Veikkaus %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 11.0,
        "Kengitys_Bonus": 1.02,  # Kengitysmuutos
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Uusi valmennus (Pihlström) ja muutos takakengitykseen (+2%). Pitkä matka suosii.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#9 Pyseidon",
        "Veikkaus %": 35.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 40.0,
        "Kengitys_Bonus": 1.05,  # Barfota fram
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Kenkätön etubalanssi (+5%) tehnyt ihmeitä. Voitti elokuussa vastaavan 3160m matkan leikitellen.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#10 Tore E.",
        "Veikkaus %": 5.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Palaa tauolta. Mats E Djuse vahvistaa ohjastusta selvästi.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#11 Hulte Jannina",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Halpa voitto aiemmin, matka ja voltin paikka tekevät tehtävästä raskaan.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#12 Trönö Borken",
        "Veikkaus %": 26.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 18.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva karhu 3000 metrille. Sairastelun jälkeen hoidettu ja treenaa lujaa. Ykköshaastaja.",
    },
    {
        "Kohde": "GS75-3",
        "Hevonen": "#13 Orrgårns Tycko",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Rehti suorittaja, mutta 60 metrin taka-matka on liikaa näin tiiviissä lähdössä.",
    },
    # --- GS75-4 (Lähtö 7) ---
    {
        "Kohde": "GS75-4",
        "Hevonen": "#1 Inkallad",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Voitti maanantaina keulasta kevyesti. Loistopaikka sisäradalla antaa etulyöntiaseman.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#2 Kjölstad Gutten",
        "Veikkaus %": 11.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 5.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hieno voitto viimeksi, mutta kohde on nyt huomattavasti kovempi.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#3 L.Q.Laban",
        "Veikkaus %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 0.98,  # Normaali balanssi (-2%)
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Palataan normaaliin kengitykseen epäonnistuneen kevennyksen jälkeen. Tasaisuus valttia.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#4 Tekno Ture",
        "Veikkaus %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Enemmän vahva kuin nopea, lyhyt matka ei paras valtti sprintissä.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#5 Sauron",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahvat tulokset helpoissa lähdöissä, vaatii merkittävää ennätysparannusta.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#6 Lomeglimt",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.02,  # Bootsit pois (+2%)
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Humörbetonad hevonen. Bootsien riisunta (+2%) tuo toivottua keveyttä kinttuihin.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#7 Bäcklös Borken",
        "Veikkaus %": 35.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 35.0,
        "Kengitys_Bonus": 1.02,  # Rautakengät (+2%)
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Ikäluokkatähti, treenaa kovaa. Paluu rautakenkiin (+2%) tuo kaivattua ravivarmuutta. Spetsfavorit.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#8 Alf",
        "Veikkaus %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hieno uran alku, norjan Derby-finaalikävijä. Sopivammassa seurassa vaarallinen.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#9 Järvsö Jan",
        "Veikkaus %": 27.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Aloitti 4 rapsakalla voitolla, Kriterium-kisoissa kunto notkahti.",
    },
    {
        "Kohde": "GS75-4",
        "Hevonen": "#10 Troll Knut",
        "Veikkaus %": 17.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 23.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kriterium-finaalisti molemmin puolin koti- ja norjankisoissa. Päähaastaja takamatkasta huolimatta.",
    },
    # --- GS75-5 (Lähtö 8) ---
    {
        "Kohde": "GS75-5",
        "Hevonen": "#1 Mary Wadd",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Hyvä lähtöpaikka sisällä, tavoitteena puhdas rahasija.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#2 Global Deadline",
        "Veikkaus %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Viron menestyjä, hyvä paikka eturivissä yllättää totokamppailuun.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#3 Xanthis Kimberly",
        "Veikkaus %": 27.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Kotiratabonus (+4%). Ikäluokkaeliittiä, tulinen avaaja ja Kylin Blom ajaa piikkipaikalta.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#4 Noa Transs R.",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Monté/sulky -suorittaja, kärki menee tässä lähdössä liian lujaa.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#5 Elin Avant",
        "Veikkaus %": 6.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kapabel tamma, hoidettu viime kisan jälkeen ja treenaa lujaa. Vahva haastaja.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#6 Ecuador Broline",
        "Veikkaus %": 26.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 20.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Gårdiksen Derbystoet-karsija. Sopivampi tammalähtö ja kamppailee voitoista.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#7 Bilbao Ace",
        "Veikkaus %": 5.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Keulavoitto Östersundissa, ulkoradan lähtöpaikka tekee reissusta haastavan.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#8 Evita Jacase",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Kasiradalta mahdoton ehtiä kärkitaisteluun kovassa seurassa.",
    },
    {
        "Kohde": "GS75-5",
        "Hevonen": "#9 Pralines",
        "Veikkaus %": 30.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 18.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Örjan Kihlström selässä takarivistä, erittäin iskukykyinen valjakko.",
    },
    # --- GS75-6 (Lähtö 9) ---
    {
        "Kohde": "GS75-6",
        "Hevonen": "#1 Belse Tösen",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.5,
        "Kengitys_Bonus": 0.97,  # Kengät jalkaan (-3%)
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Laukannut kahdesti. Juoksee kengät jalassa (-3%), hakee sisäratareissua.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#2 Sol Flamma",
        "Veikkaus %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vauhtia löytää ajoittain, mutta suoritusvarmuus ailahtelee.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#3 Gangsi",
        "Veikkaus %": 0.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Pieni tamma, joka tyytyy pikkurahoihin kovempien rinnalla.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#4 Hög Decibel",
        "Veikkaus %": 5.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 5.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Varma suorittaja, SM-lähtö oli liian kova karkelo.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#5 Klack Tea",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 1.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Juoksee usein omissa sarjoissaan, mutta kärki menee liian lujaa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#6 Lille Rose G.L.",
        "Veikkaus %": 14.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 9.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Uusi hieno aika viimeksi, kunto selvästi nousussa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#7 Eldida",
        "Veikkaus %": 3.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Mats E Djuse vahvistuksena kärryillä, mielenkiintoinen yllättäjä.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#8 Lysjö Isa",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 7.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Örjan Kihlström ohjastajana tuo aina irtopisteitä.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#9 Lokatt",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Tasoituksen keskellä pussitusvaara, hakee rahasijaa.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#10 Myllkärr Christina",
        "Veikkaus %": 0.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 3.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Vahva tamma, voittaa valitettavan harvoin.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#11 Guli Stina",
        "Veikkaus %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 14.0,
        "Kengitys_Bonus": 0.97,  # Kengät takaisin (-3%)
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Nuoruuden tähti, kengät jalkaan SM:n jälkeen (-3%). Platschans.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#12 Hulte Annika",
        "Veikkaus %": 40.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 32.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "💥 Vahva SM-kolmonen, laskee sopivampaan tammalähtöön. Ykkössuosikki.",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#13 Tekno Tana",
        "Veikkaus %": 26.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 16.0,
        "Kengitys_Bonus": 1.02,  # Etukengättömyys (+2%)
        "Karryt_Bonus": 1.02,  # Hybridikärryt (+2%)
        "Unibet": None,
        "Perustelu": "Erittäin vahva. Mahdolliset etukengättömyys ja hybridikärryt tuovat lisäpotkua (+4%).",
    },
    {
        "Kohde": "GS75-6",
        "Hevonen": "#14 Ethel",
        "Veikkaus %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 2.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "60 metrin taka-matkalta tehtävä on äärimmäisen raskas.",
    },
    # --- GS75-7 (Lähtö 10) ---
    {
        "Kohde": "GS75-7",
        "Hevonen": "#1 Guli Hektor",
        "Veikkaus %": 2.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 11.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Upea kiri viimestä, ykkösradalla pieni pussituksen riski.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#2 Guldhagens Pirat",
        "Veikkaus %": 3.0,
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
        "Veikkaus %": 7.0,
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
        "Veikkaus %": 0.0,
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
        "Veikkaus %": 53.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 22.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.04,  # Amerikansk vagn (+4%)
        "Unibet": None,
        "Perustelu": "💥 Hienossa iskussa, voitti Färjestadissa. Jenkkikärryt perään autolähtöön (+4%)!",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#6 Eld Prinsen",
        "Veikkaus %": 2.0,
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
        "Veikkaus %": 24.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 24.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.04,  # Amerikansk vagn (+4%)
        "Unibet": None,
        "Perustelu": "💥 Pihlström luottaa voittoon! Hyötyy autolähdöstä ja jenkkikärryistä (+4%).",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#8 Hibovalle",
        "Veikkaus %": 1.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.00,
        "Unibet": None,
        "Perustelu": "Saanut huonon paikan spårtrappassa, vaatii tuuria pussiin jäämättä.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#9 Guldhagens Oscar",
        "Veikkaus %": 2.0,
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
        "Veikkaus %": 4.0,
        "Prosentti_Muutos": 0,
        "Oma_Simulaatio_Arvio %": 4.0,
        "Kengitys_Bonus": 1.00,
        "Karryt_Bonus": 1.03,  # Amerikansk vagn (+3%)
        "Unibet": None,
        "Perustelu": "Ravi parantunut, autolähtö ja jenkkikärryt (+3%) takarivistä sopivat.",
    },
    {
        "Kohde": "GS75-7",
        "Hevonen": "#11 Blomsterprinsen",
        "Veikkaus %": 2.0,
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
        "Veikkaus %": 1.0,
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

# LASKETAAN LOPULLINEN ARVIO KAIKILLA PAINOTUKSILLA TAUSTALLA:
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

# JÄRJESTETÄÄN TAULUKKO LÄHDÖITTÄIN (GS75-1 -> GS75-7) JA SITTEN ARVIO % MUKAAN:
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

# ----------------- PARHAAT ALLE 10% IDEAT - LAATIKKO -----------------
df_vihjeet["Erotus %"] = df_vihjeet["Arvio %"] - df_vihjeet["Veikkaus %"]
alipelatut_alle_10 = df_vihjeet[
    (df_vihjeet["Veikkaus %"] < 10.0) & (df_vihjeet["Erotus %"] > 3.0)
].sort_values(by="Erotus %", ascending=False)

st.success("💡 **Parhaat Alipelatut Ideat (< 10% Pelijakauma)**")
for _, row in alipelatut_alle_10.head(4).iterrows():
    st.write(
        f"• **{row['Kohde']}**: **{row['Hevonen']}** (Arvio: **{row['Arvio %']:.1f}%** vs Veikkaus: **{row['Veikkaus %']:.0f}%** -> Erotus: **+{row['Erotus %']:.1f}%**)"
    )
    st.caption(f"_{row['Perustelu']}_")

st.divider()

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
            "Veikkaus %",
            "Prosentti_Muutos",
            "Arvio %",
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
df_surprises = df_vihjeet[df_vihjeet["Veikkaus %"] < 10.0]

st.dataframe(
    df_surprises[
        [
            "Kohde",
            "Hevonen",
            "Veikkaus %",
            "Prosentti_Muutos",
            "Arvio %",
            "Paras Kerroin",
            "EV",
            "Perustelu",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)
