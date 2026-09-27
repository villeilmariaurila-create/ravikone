import pandas as pd
import streamlit as st

# --- STREAMLIT-SIVUN ASETUKSET ---
st.set_page_config(page_title="Solvalla V85 Analysaattori", layout="wide")

st.title("🏇 Solvalla V85 - Päivitetyt Peliprosentit & Simulaatio")

# --- SOLVALLA V85 - KOKO AINEISTO PÄIVITETYILLÄ PROSENTEILLA (L5–L12) ---
data = [
    # ==================== V85-1 / L5 (2140a) ====================
    {"Kohde": "V85-1 (L5)", "Hevonen": "#1 Catch and Go", "Veikkaus_%": 6.0, "Bonus": 1.15, "Perustelu": "💥 MAXIMOITU VIRITYS! Ekaa kertaa jenkit, kokolaput & vetolaput. Keulasuosikki."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#2 Pure Games", "Veikkaus_%": 43.0, "Bonus": 1.00, "Perustelu": "Suosikki ilman erityisiä varustemuutoksia."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#3 Com Best", "Veikkaus_%": 1.0, "Bonus": 1.05, "Perustelu": "Kuntopiikki, taistelee yllätyssijoituksista."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#4 Long Night Out", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Yllättäjätaustalla."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#5 Vulcan Tile", "Veikkaus_%": 24.0, "Bonus": 1.00, "Perustelu": "Tasaisen vahva haastaja."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#6 Steady Spender", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "💥 VAHVA PÄÄHAASTAJA! Barfota runt om -balanssilla vaarallinen."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#7 Nanda Devi Cut", "Veikkaus_%": 3.0, "Bonus": 1.04, "Perustelu": "Kiri hyvin viimeksi."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#8 Dalton Russell", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Ulkoradan lähtöpaikka rasittaa."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#9 Revanche Boko", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä vaikeaa."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#10 Tennessee H.C.", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Tarvitsee ylivauhtia."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#11 City Slicker", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Takarivin paikka."},
    {"Kohde": "V85-1 (L5)", "Hevonen": "#12 Ideal Kronos", "Veikkaus_%": 13.0, "Bonus": 1.00, "Perustelu": "Haastava paikka 12."},

    # ==================== V85-2 / L6 (2140a) ====================
    {"Kohde": "V85-2 (L6)", "Hevonen": "#1 Screen Time Limit", "Veikkaus_%": 1.0, "Bonus": 1.05, "Perustelu": "Sisäradan turvin ajoissa huomioitava."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#2 S.G.Empress", "Veikkaus_%": 25.0, "Bonus": 1.12, "Perustelu": "💥 KÄRKIPÄÄN SUOSIKKI! Mahtava kapasiteetti ja huippupaikka."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#3 Melba Westwood", "Veikkaus_%": 4.0, "Bonus": 1.02, "Perustelu": "Nappipaikalta smyygaa rahoille."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#4 First Class U.S.", "Veikkaus_%": 2.0, "Bonus": 1.04, "Perustelu": "Hyvä kakkosketjun haastaja."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#5 Ballerina", "Veikkaus_%": 0.0, "Bonus": 1.06, "Perustelu": "Ekaa kertaa barfota runt om."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#6 S.G.Dacota", "Veikkaus_%": 11.0, "Bonus": 1.00, "Perustelu": "Tasainen haastaja."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#7 Fly The Coup", "Veikkaus_%": 11.0, "Bonus": 1.00, "Perustelu": "Hankala lähtöpaikka."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#8 Matchmadeinheaven", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Rata 8 syö chanseja."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#9 Blast Off", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä tarkkailuasetelmat."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#10 Great Pride", "Veikkaus_%": 44.0, "Bonus": 1.00, "Perustelu": "💥 LÄHDÖN PELATUIN SUOSIKKI!"},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#11 Good Habit", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivin paikka."},
    {"Kohde": "V85-2 (L6)", "Hevonen": "#12 Cantilena", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Iskukylmä paikka 12."},

    # ==================== V85-3 / L7 (2140a) ====================
    {"Kohde": "V85-3 (L7)", "Hevonen": "#1 Oriana Boko", "Veikkaus_%": 47.0, "Bonus": 1.04, "Perustelu": "💥 SELKEÄ LÄHDÖN SUOSIKKI! Sisäradalta vahva juoksu luvassa."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#2 Lavender", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Smyygaa sisällä."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#3 Charma", "Veikkaus_%": 19.0, "Bonus": 1.08, "Perustelu": "💥 HUIPPUUUTINEN: Barfota runt om ekaa kertaa! Kihlström puikoissa."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#4 Osken", "Veikkaus_%": 6.0, "Bonus": 1.10, "Perustelu": "Vahva esitys alla, hyvä varustebonus."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#5 Clean Community", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Perussuorittaja."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#6 Valnes Penny", "Veikkaus_%": 3.0, "Bonus": 1.06, "Perustelu": "Goop ratissa, barfota fram."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#7 Unicum", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Ulkopuolelta tarkkailuun."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#8 Nightingale", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Rata 8 rasittaa."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#9 Egerie", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Takarivin merkki."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#10 Quina", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#11 Lilium Sisu", "Veikkaus_%": 12.0, "Bonus": 1.00, "Perustelu": "Hyvin pelattu yllättäjä takarivistä."},
    {"Kohde": "V85-3 (L7)", "Hevonen": "#12 S.G.Eye Candy", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Synkkä paikka."},

    # ==================== V85-4 / L8 (2140a) ====================
    {"Kohde": "V85-4 (L8)", "Hevonen": "#1 Unrestricted", "Veikkaus_%": 11.0, "Bonus": 1.02, "Perustelu": "Sisäradalta hyvä asema."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#2 Backwood Gisella", "Veikkaus_%": 29.0, "Bonus": 1.10, "Perustelu": "💥 LÄHDÖN SUOSIKKI OCH KEULABUD! Todella vahva esitys alla."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#3 La Nova", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Odotellaan parannusta."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#4 Free Time Trot", "Veikkaus_%": 3.0, "Bonus": 1.05, "Perustelu": "Ajoissa lapulle."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#5 Lavender", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Keskiradalta mukaan."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#6 Scarfo Pellini", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Lupauksia herättävä."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#7 Screen Time Limit", "Veikkaus_%": 21.0, "Bonus": 1.00, "Perustelu": "Päähaastajia ulkoreunalta."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#8 S.G.Empress", "Veikkaus_%": 19.0, "Bonus": 1.00, "Perustelu": "Vaarallinen luokkahäst."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#9 Egerie", "Veikkaus_%": 13.0, "Bonus": 1.00, "Perustelu": "Hyvin pelattu takarivistä."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#10 Hawthorne Effect", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "Hyvä varustebonus haastajaluokassa."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#11 Great Pride", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Iskukykyinen takarivistä."},
    {"Kohde": "V85-4 (L8)", "Hevonen": "#12 S.G.Dacota", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Paha paikka 12."},

    # ==================== V85-5 / L9 (2140a) ====================
    {"Kohde": "V85-5 (L9)", "Hevonen": "#1 Fatal Attraction", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Smyygaa innerspårilta."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#2 Procope", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Outsider."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#3 Jula Donatella", "Veikkaus_%": 2.0, "Bonus": 1.05, "Perustelu": "Ekaa kertaa barfota fram."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#4 Fatal Attraction", "Veikkaus_%": 21.0, "Bonus": 1.08, "Perustelu": "💥 Kaksi keulavoittoa putkeen! Kärkipaikalle tähdätään."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#5 Illicit Hooch", "Veikkaus_%": 1.0, "Bonus": 1.04, "Perustelu": "Ekaa kertaa barfota runt om & blinkers."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#6 N.Y.Easy On Me", "Veikkaus_%": 5.0, "Bonus": 1.02, "Perustelu": "Mukaan haastajajoukkoon."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#7 I See Tail Lights", "Veikkaus_%": 37.0, "Bonus": 1.10, "Perustelu": "💥 LÄHDÖN SUOSIKKI! Hirmuisessa iskussa (1.10,9a edellisen voiton aika)."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#8 Cruiser", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Huippusuku, mutta rata 8 rasittaa."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#9 Zeebreeze", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Vaikea tehtävä."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#10 Navy Cut", "Veikkaus_%": 3.0, "Bonus": 1.02, "Perustelu": "Hyvä kiri alla."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#11 Mellby Orkide", "Veikkaus_%": 24.0, "Bonus": 1.10, "Perustelu": "💥 JÄTTI-VARUSTEMUUTOS! Redén ottaa kengät pois ekaa kertaa (barfota runt om). Kihlström kyydissä."},
    {"Kohde": "V85-5 (L9)", "Hevonen": "#12 Klara Godiva", "Veikkaus_%": 0.0, "Bonus": 1.05, "Perustelu": "TAULUAAN PAREMPI! Laukkasi varman voiton viime metreillä."},

    # ==================== V85-6 / L10 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V85-6 (L10)", "Hevonen": "#1 In Fine Fettle", "Veikkaus_%": 4.0, "Bonus": 1.02, "Perustelu": "Kengättä edestä & jenkit."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#2 Thor Tooma", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Smyygaa sisällä."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#3 Bourbon Phantasy", "Veikkaus_%": 4.0, "Bonus": 1.08, "Perustelu": "🔥 Wäjerstenin oma valinta hyvältä paikalta."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#4 Kodiak Zet", "Veikkaus_%": 76.0, "Bonus": 1.15, "Perustelu": "💥 LÄHDÖN PÄÄVARMA OCH GIGA-SUOSIKKI! Ekaa kertaa barfota bak & jenkit. Kihlström puikoissa."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#5 Baby Love", "Veikkaus_%": 1.0, "Bonus": 1.10, "Perustelu": "Barfota runt om & jenkit ekaa kertaa."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#6 Neutron Star", "Veikkaus_%": 11.0, "Bonus": 1.05, "Perustelu": "💥 PÄÄHAASTAJA! Ilman etukenkiä sitkeä kuolemanpaikkajyrä."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#7 Crew Lane", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Haastava paikka."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#8 Bys Arigato", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Kaukana kärjestä."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#9 Prince of Euro", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "Luokkaa löytyy, ekaa kertaa barfota runt om."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#10 Pivot Caigoo", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#11 First Festive Vir", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-6 (L10)", "Hevonen": "#12 Xanthis Lewis", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Kunto piikissä, paha paikka."},

    # ==================== V85-7 / L11 (2640a) ====================
    {"Kohde": "V85-7 (L11)", "Hevonen": "#1 Coloneltomparker", "Veikkaus_%": 52.0, "Bonus": 1.12, "Perustelu": "💥 SPETSFAVORIT OCH FÖRSTA BARFOTA RUNT OM! Extremt stark och gynnad av 2640m."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#2 Bravo Desoto", "Veikkaus_%": 2.0, "Bonus": 1.05, "Perustelu": "Första barfota fram, får fint smyglopp."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#3 Ulix Turner", "Veikkaus_%": 2.0, "Bonus": 1.08, "Perustelu": "SKRÄLLBUD! Segstark häst med Jepson i sulkyn och första barfota runt om."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#4 Reagan Boko", "Veikkaus_%": 6.0, "Bonus": 1.02, "Perustelu": "Gjort det bra men möter hårt motstånd."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#5 Zarajevo Games", "Veikkaus_%": 28.0, "Bonus": 1.10, "Perustelu": "💥 KLASSIG HÄST! Vunnit 5/8, enorm styrka."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#6 Yardbird", "Veikkaus_%": 5.0, "Bonus": 1.00, "Perustelu": "Håller fin form."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#7 Banzai Brodde", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Ulkona kärkitaistosta."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#8 Vancouver Tile", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Barfota runt om på nytt."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#9 John McClane", "Veikkaus_%": 0.0, "Bonus": 1.06, "Perustelu": "Första barfota runt om och rycktussar."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#10 Po Tay Toes", "Veikkaus_%": 3.0, "Bonus": 1.08, "Perustelu": "SPÄNNANDE UTMANARE! Vunnit 3/4 och får barfota fram för första gången."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#11 Courage d'Inverne", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-7 (L11)", "Hevonen": "#12 Wingait Stefan", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Vunnit 4/5 men spår 12 i Kriteriekval är iskallt."},

    # ==================== V85-8 / L12 (2640a) ====================
    {"Kohde": "V85-8 (L12)", "Hevonen": "#1 Pure Games", "Veikkaus_%": 3.0, "Bonus": 1.08, "Perustelu": "🔥 SPETSBUD! Dante Kolgjini laddar från spår 1."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#2 Nanda Devi Cut", "Veikkaus_%": 5.0, "Bonus": 1.10, "Perustelu": "🔥 HUIPPUIDEANOSTO! Ekaa kertaa rycktussar, 3/4 voittanut keulasta."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#3 Mahzarin W.", "Veikkaus_%": 25.0, "Bonus": 1.02, "Perustelu": "💥 LÄHDÖN PELATUIMPIA SUOSIKKEJA! Spurtade vasst senast."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#4 Long Night Out", "Veikkaus_%": 1.0, "Bonus": 1.05, "Perustelu": "Carl Johan Jepson kyytiin."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#5 Vulcan Tile", "Veikkaus_%": 2.0, "Bonus": 1.06, "Perustelu": "Första barfota runt om."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#6 Ready for Boarding", "Veikkaus_%": 2.0, "Bonus": 1.05, "Perustelu": "KAPACITET FINNS! E3-voittaja elokuulta."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#7 Ideal Kronos", "Veikkaus_%": 9.0, "Bonus": 1.08, "Perustelu": "🔥 MAXADE ÄNDRINGAR! Första rycktussar och amerikansk vagn."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#8 Turner Ale", "Veikkaus_%": 3.0, "Bonus": 1.02, "Perustelu": "Första barfota bak."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#9 Campitj", "Veikkaus_%": 12.0, "Bonus": 1.00, "Perustelu": "Haastava paikka takarivissä."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#10 Pepper Creation", "Veikkaus_%": 4.0, "Bonus": 1.08, "Perustelu": "STARK OCH FORMSTOPPAD! Vunnit 2/3 barfota runt om."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#11 Evert Palema", "Veikkaus_%": 35.0, "Bonus": 1.05, "Perustelu": "💥 LÄHDÖN SUOSIKKI! Växlar upp till barfota runt om."},
    {"Kohde": "V85-8 (L12)", "Hevonen": "#12 Intro", "Veikkaus_%": 0.0, "Bonus": 1.10, "Perustelu": "Klassig favorit, mutta jäänyt ilman peliä spår 12 takia."}
]

# --- LASKENNALLINEN SIMULAATIO & VARUSTEBONUKSET ---
df = pd.DataFrame(data)

# 1. Painotetun arviotodennaeikoesyyden laskeminen
df['Painotettu_Peliosuus'] = df['Veikkaus_%'] * df['Bonus']
df['Arvioitu_Prob_%'] = df.groupby('Kohde')['Painotettu_Peliosuus'].transform(lambda x: (x / x.sum()) * 100)

# 2. Pelillisen eron (Ero) laskeminen (Arvio % - Veikkaus %)
df['Ero_%'] = df['Arvioitu_Prob_%'] - df['Veikkaus_%']

# --- STREAMLIT-KÄYTTÖLIITTYMÄN TULOSTUS ---

# Isoimmat varustemuutoksista hyötyvät alipelatut peli-ideat
st.header("🎯 Simulaation Parhaat Arvolöydöt (Arvio % > Pelattu %)")
top_ideas = df[df['Ero_%'] >= 1.5].sort_values(by='Ero_%', ascending=False)

if not top_ideas.empty:
    for _, r in top_ideas.iterrows():
        st.success(f"**[{r['Kohde']}] {r['Hevonen']}** | Pelattu: **{r['Veikkaus_%']:.1f}%** ➔ Arvio: **{r['Arvioitu_Prob_%']:.1f}%** (+{r['Ero_%']:.1f}%)\n\n_{r['Perustelu']}_")
else:
    st.info("Pelimarkkina on hyvin linjassa varustebonusten kanssa.")

st.divider()

# Kohdekohtainen tarkastelu
st.header("📊 Kohdekohtainen Analyysi (V85-1 – V85-8)")

kohteet = df['Kohde'].unique()
selected_kohde = st.selectbox("Valitse kohde tarkasteluun:", kohteet)

kohde_df = df[df['Kohde'] == selected_kohde].sort_values(by='Arvioitu_Prob_%', ascending=False)

st.subheader(f"Kohteen {selected_kohde} ranking & simulaatioarviot:")

# Muotoillaan taulukko siististi
display_df = kohde_df[['Hevonen', 'Veikkaus_%', 'Bonus', 'Arvioitu_Prob_%', 'Ero_%', 'Perustelu']].copy()
display_df.columns = ['Hevonen', 'Veikkaus %', 'Varustebonus', 'Simulaatio Arvio %', 'Ero %', 'Perustelu']

st.dataframe(display_df, use_container_width=True)

# Yhteenvetotekstit valitusta kohteesta
st.markdown("### Hevosten perustelut:")
for _, r in kohde_df.iterrows():
    st.write(f"• **{r['Hevonen']}** (Pelattu {r['Veikkaus_%']:.1f}% ➔ Arvio {r['Arvioitu_Prob_%']:.1f}%): {r['Perustelu']}")
