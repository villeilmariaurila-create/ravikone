import pandas as pd
import streamlit as st

# --- STREAMLIT-SIVUN ASETUKSET ---
st.set_page_config(page_title="Solvalla V85 Analysaattori", layout="wide")

st.title("🏇 Solvalla V85 - Täydellinen Analyysi & Peli-ideat")

# --- SOLVALLA V85 - KOKO AINEISTO (V85-1 – V85-8) ---
data = [
    # ==================== V85-1 (Solvalla L5, 2140a) ====================
    {"Kohde": "V85-1", "Hevonen": "#1 Catch and Go", "Veikkaus_%": 41.0, "Unibet": None, "Bonus": 1.15, "Perustelu": "💥 MAXIMOITU VIRITYS! Ekaa kertaa jenkit, kokolaput & vetolaput. Keulasuosikki."},
    {"Kohde": "V85-1", "Hevonen": "#2 Pure Games", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Hyvä paikka, mutta riittääkö nopeus?"},
    {"Kohde": "V85-1", "Hevonen": "#3 Com Best", "Veikkaus_%": 15.0, "Unibet": None, "Bonus": 1.05, "Perustelu": "Kuntopiikki, taistelee kärkipään sijoituksista."},
    {"Kohde": "V85-1", "Hevonen": "#4 Long Night Out", "Veikkaus_%": 3.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Yllättäjätaustalla."},
    {"Kohde": "V85-1", "Hevonen": "#5 Vulcan Tile", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Tasainen suorittaja."},
    {"Kohde": "V85-1", "Hevonen": "#6 Steady Spender", "Veikkaus_%": 22.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "💥 VAHVA PÄÄHAASTAJA! Barfota runt om -balanssilla vaarallinen."},
    {"Kohde": "V85-1", "Hevonen": "#7 Nanda Devi Cut", "Veikkaus_%": 8.0, "Unibet": None, "Bonus": 1.04, "Perustelu": "Kiri hyvin viimeksi."},
    {"Kohde": "V85-1", "Hevonen": "#8 Dalton Russell", "Veikkaus_%": 4.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Ulkoradan lähtöpaikka rasittaa."},
    {"Kohde": "V85-1", "Hevonen": "#9 Revanche Boko", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Takarivistä vaikeaa."},
    {"Kohde": "V85-1", "Hevonen": "#10 Tennessee H.C.", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Tarvitsee ylivauhtia."},
    {"Kohde": "V85-1", "Hevonen": "#11 City Slicker", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Takarivin paikka."},
    {"Kohde": "V85-1", "Hevonen": "#12 Ideal Kronos", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Ulkona kärkitaistosta."},

    # ==================== V85-2 (Solvalla L6, 2140a) ====================
    {"Kohde": "V85-2", "Hevonen": "#1 Screen Time Limit", "Veikkaus_%": 12.0, "Unibet": None, "Bonus": 1.05, "Perustelu": "Sisäradan turvin ajoissa huomioitava."},
    {"Kohde": "V85-2", "Hevonen": "#2 S.G.Empress", "Veikkaus_%": 48.0, "Unibet": None, "Bonus": 1.12, "Perustelu": "💥 TAMMALÄHDÖN GIGA-FAVORIT! Mahtava kapasiteetti ja huippupaikka."},
    {"Kohde": "V85-2", "Hevonen": "#3 Melba Westwood", "Veikkaus_%": 3.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Nappipaikalta smyygaa rahoille."},
    {"Kohde": "V85-2", "Hevonen": "#4 First Class U.S.", "Veikkaus_%": 6.0, "Unibet": None, "Bonus": 1.04, "Perustelu": "Hyvä kakkosketjun haastaja."},
    {"Kohde": "V85-2", "Hevonen": "#5 Ballerina", "Veikkaus_%": 15.0, "Unibet": None, "Bonus": 1.06, "Perustelu": "💥 PÄÄHAASTAJA! Tulossa kova esitys ekaa kertaa barfota runt om."},
    {"Kohde": "V85-2", "Hevonen": "#6 S.G.Dacota", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Tasainen haastaja."},
    {"Kohde": "V85-2", "Hevonen": "#7 Fly The Coup", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Hankala lähtöpaikka."},
    {"Kohde": "V85-2", "Hevonen": "#8 Matchmadeinheaven", "Veikkaus_%": 8.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Luokkaa löytyy, mutta rata 8 syö chanseja."},
    {"Kohde": "V85-2", "Hevonen": "#9 Blast Off", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Takarivistä tarkkailuasetelmat."},
    {"Kohde": "V85-2", "Hevonen": "#10 Great Pride", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Vaatii tuuria kärkipäähän."},
    {"Kohde": "V85-2", "Hevonen": "#11 Good Habit", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Takarivin paikka."},
    {"Kohde": "V85-2", "Hevonen": "#12 Cantilena", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Iskukylmä paikka 12."},

    # ==================== V85-3 (Solvalla L7, 2140a) ====================
    {"Kohde": "V85-3", "Hevonen": "#1 Oriana Boko", "Veikkaus_%": 5.0, "Unibet": None, "Bonus": 1.04, "Perustelu": "Sisäradalta hyvä juoksu luvassa."},
    {"Kohde": "V85-3", "Hevonen": "#2 Lavender", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Smyygaa sisällä."},
    {"Kohde": "V85-3", "Hevonen": "#3 Charma", "Veikkaus_%": 18.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "💥 HUIPPUUUTINEN: Barfota runt om ekaa kertaa! Kihlström puikoissa."},
    {"Kohde": "V85-3", "Hevonen": "#4 Osken", "Veikkaus_%": 35.0, "Unibet": None, "Bonus": 1.10, "Perustelu": "💥 LÄHDÖN SUOSIKKI OCH KEULABUD! Todella vahva esitys alla."},
    {"Kohde": "V85-3", "Hevonen": "#5 Clean Community", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Perussuorittaja."},
    {"Kohde": "V85-3", "Hevonen": "#6 Valnes Penny", "Veikkaus_%": 22.0, "Unibet": None, "Bonus": 1.06, "Perustelu": "💥 PÄÄHAASTAJA! Goop ratissa, barfota fram."},
    {"Kohde": "V85-3", "Hevonen": "#7 Unicum", "Veikkaus_%": 4.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Ulkopuolelta tarkkailuun."},
    {"Kohde": "V85-3", "Hevonen": "#8 Nightingale", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Rata 8 rasittaa."},
    {"Kohde": "V85-3", "Hevonen": "#9 Egerie", "Veikkaus_%": 8.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Takarivin paras merkki."},
    {"Kohde": "V85-3", "Hevonen": "#10 Quina", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-3", "Hevonen": "#11 Lilium Sisu", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Tarvitsee ylivauhtia."},
    {"Kohde": "V85-3", "Hevonen": "#12 S.G.Eye Candy", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Synkkä paikka."},

    # ==================== V85-4 (Solvalla L8, 2140a) ====================
    {"Kohde": "V85-4", "Hevonen": "#1 Unrestricted", "Veikkaus_%": 4.0, "Unibet": 19.00, "Bonus": 1.02, "Perustelu": "Sisäradalta hyvä asema."},
    {"Kohde": "V85-4", "Hevonen": "#2 Backwood Gisella", "Veikkaus_%": 30.0, "Unibet": 85.00, "Bonus": 1.10, "Perustelu": "🔥 MEGA-EV OCH VIRHEPRISOINTI! Veikkauksen keulasuosikki (30%), Unibet tarjoaa 85.00!"},
    {"Kohde": "V85-4", "Hevonen": "#3 La Nova", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Odotellaan parannusta."},
    {"Kohde": "V85-4", "Hevonen": "#4 Free Time Trot", "Veikkaus_%": 12.0, "Unibet": 7.50, "Bonus": 1.05, "Perustelu": "Ajoissa lapulle."},
    {"Kohde": "V85-4", "Hevonen": "#5 Lavender", "Veikkaus_%": 2.0, "Unibet": 14.00, "Bonus": 1.00, "Perustelu": "Keskiradalta mukaan."},
    {"Kohde": "V85-4", "Hevonen": "#6 Scarfo Pellini", "Veikkaus_%": 5.0, "Unibet": 11.00, "Bonus": 1.02, "Perustelu": "Lupauksia herättävä."},
    {"Kohde": "V85-4", "Hevonen": "#7 Screen Time Limit", "Veikkaus_%": 1.0, "Unibet": 21.00, "Bonus": 1.00, "Perustelu": "Ulkoreunalta haastavaa."},
    {"Kohde": "V85-4", "Hevonen": "#8 S.G.Empress", "Veikkaus_%": 3.0, "Unibet": 2.10, "Bonus": 1.00, "Perustelu": "Unibetin suosikki, matala peliosuus Veikkauksessa."},
    {"Kohde": "V85-4", "Hevonen": "#9 Egerie", "Veikkaus_%": 2.0, "Unibet": 31.00, "Bonus": 1.00, "Perustelu": "Takarivistä."},
    {"Kohde": "V85-4", "Hevonen": "#10 Hawthorne Effect", "Veikkaus_%": 18.0, "Unibet": 4.00, "Bonus": 1.08, "Perustelu": "🔥 MAHTAVA H2H-PELIDEI! Selkeä suosikki La Novaa vastaan H2H:ssa."},
    {"Kohde": "V85-4", "Hevonen": "#11 Great Pride", "Veikkaus_%": 10.0, "Unibet": 12.00, "Bonus": 1.02, "Perustelu": "Iskukykyinen takarivistä."},
    {"Kohde": "V85-4", "Hevonen": "#12 S.G.Dacota", "Veikkaus_%": 12.0, "Unibet": 7.50, "Bonus": 1.00, "Perustelu": "Paha paikka 12."},

    # ==================== V85-5 (Solvalla L9, 2140a) ====================
    {"Kohde": "V85-5", "Hevonen": "#1 Fatal Attraction", "Veikkaus_%": 3.0, "Unibet": 16.00, "Bonus": 1.00, "Perustelu": "Smyygaa innerspårilta."},
    {"Kohde": "V85-5", "Hevonen": "#2 Procope", "Veikkaus_%": 1.0, "Unibet": 85.00, "Bonus": 1.00, "Perustelu": "Outsider."},
    {"Kohde": "V85-5", "Hevonen": "#3 Jula Donatella", "Veikkaus_%": 2.0, "Unibet": 37.00, "Bonus": 1.05, "Perustelu": "Ekaa kertaa barfota fram."},
    {"Kohde": "V85-5", "Hevonen": "#4 Fatal Attraction", "Veikkaus_%": 22.0, "Unibet": 2.35, "Bonus": 1.08, "Perustelu": "💥 Kaksi keulavoittoa putkeen! Kärkipaikalle tähdätään."},
    {"Kohde": "V85-5", "Hevonen": "#5 Illicit Hooch", "Veikkaus_%": 1.0, "Unibet": 16.00, "Bonus": 1.04, "Perustelu": "Ekaa kertaa barfota runt om & blinkers."},
    {"Kohde": "V85-5", "Hevonen": "#6 N.Y.Easy On Me", "Veikkaus_%": 4.0, "Unibet": 5.00, "Bonus": 1.02, "Perustelu": "Mukaan haastajajoukkoon."},
    {"Kohde": "V85-5", "Hevonen": "#7 I See Tail Lights", "Veikkaus_%": 37.0, "Unibet": 4.15, "Bonus": 1.10, "Perustelu": "💥 Hirmuisessa iskussa (1.10,9a edellisen voiton aika). Keulasuosikki."},
    {"Kohde": "V85-5", "Hevonen": "#8 Cruiser", "Veikkaus_%": 1.0, "Unibet": 9.50, "Bonus": 1.02, "Perustelu": "Huippusuku, mutta rata 8 rasittaa."},
    {"Kohde": "V85-5", "Hevonen": "#9 Zeebreeze", "Veikkaus_%": 0.0, "Unibet": 35.00, "Bonus": 1.00, "Perustelu": "Vaikea tehtävä."},
    {"Kohde": "V85-5", "Hevonen": "#10 Navy Cut", "Veikkaus_%": 3.0, "Unibet": 12.50, "Bonus": 1.02, "Perustelu": "Hyvä kiri alla."},
    {"Kohde": "V85-5", "Hevonen": "#11 Mellby Orkide", "Veikkaus_%": 23.0, "Unibet": 33.00, "Bonus": 1.10, "Perustelu": "💥 JÄTTI-VARUSTEMUUTOS! Redén ottaa kengät pois ekaa kertaa (barfota runt om). Kihlström kyydissä."},
    {"Kohde": "V85-5", "Hevonen": "#12 Klara Godiva", "Veikkaus_%": 0.0, "Unibet": 90.00, "Bonus": 1.05, "Perustelu": "🔥 TAULUAAN PAREMPI! Laukkasi varman voiton viime metreillä."},

    # ==================== V85-6 / SOLVALLA L10 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V85-6", "Hevonen": "#1 In Fine Fettle", "Veikkaus_%": 4.1, "Unibet": 15.89, "Bonus": 1.02, "Perustelu": "Kengättä edestä & jenkit."},
    {"Kohde": "V85-6", "Hevonen": "#2 Thor Tooma", "Veikkaus_%": 0.8, "Unibet": 27.74, "Bonus": 1.00, "Perustelu": "Smyygaa sisällä."},
    {"Kohde": "V85-6", "Hevonen": "#3 Bourbon Phantasy", "Veikkaus_%": 4.5, "Unibet": 14.81, "Bonus": 1.08, "Perustelu": "🔥 Wäjerstenin oma valinta hyvältä paikalta."},
    {"Kohde": "V85-6", "Hevonen": "#4 Kodiak Zet", "Veikkaus_%": 76.0, "Unibet": 1.61, "Bonus": 1.15, "Perustelu": "💥 LÄHDÖN PÄÄVARMA OCH GIGA-SUOSIKKI! Ekaa kertaa barfota bak & jenkit. Kihlström puikoissa."},
    {"Kohde": "V85-6", "Hevonen": "#5 Baby Love", "Veikkaus_%": 0.9, "Unibet": 11.72, "Bonus": 1.10, "Perustelu": "🔥 Barfota runt om & jenkit ekaa kertaa."},
    {"Kohde": "V85-6", "Hevonen": "#6 Neutron Star", "Veikkaus_%": 10.7, "Unibet": 8.16, "Bonus": 1.05, "Perustelu": "💥 PÄÄHAASTAJA! Ilman etukenkiä sitkeä kuolemanpaikkajyrä."},
    {"Kohde": "V85-6", "Hevonen": "#7 Crew Lane", "Veikkaus_%": 0.4, "Unibet": 47.26, "Bonus": 1.00, "Perustelu": "Haastava paikka."},
    {"Kohde": "V85-6", "Hevonen": "#8 Bys Arigato", "Veikkaus_%": 0.1, "Unibet": 69.06, "Bonus": 1.00, "Perustelu": "Kaukana kärjestä."},
    {"Kohde": "V85-6", "Hevonen": "#9 Prince of Euro", "Veikkaus_%": 1.4, "Unibet": 15.45, "Bonus": 1.08, "Perustelu": "🔥 Luokkaa löytyy, ekaa kertaa barfota runt om."},
    {"Kohde": "V85-6", "Hevonen": "#10 Pivot Caigoo", "Veikkaus_%": 0.2, "Unibet": 32.81, "Bonus": 1.00, "Perustelu": "Takarivistä."},
    {"Kohde": "V85-6", "Hevonen": "#11 First Festive Vir", "Veikkaus_%": 0.2, "Unibet": 83.50, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-6", "Hevonen": "#12 Xanthis Lewis", "Veikkaus_%": 0.7, "Unibet": 24.25, "Bonus": 1.00, "Perustelu": "Kunto piikissä, paha paikka."},

    # ==================== V85-7 (Solvalla L11, 2640a) ====================
    {"Kohde": "V85-7", "Hevonen": "#1 Coloneltomparker", "Veikkaus_%": 53.0, "Unibet": None, "Bonus": 1.12, "Perustelu": "💥 SPETSFAVORIT OCH FÖRSTA BARFOTA RUNT OM! Extremt stark och gynnad av 2640m."},
    {"Kohde": "V85-7", "Hevonen": "#2 Bravo Desoto", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.05, "Perustelu": "Första barfota fram, får fint smyglopp."},
    {"Kohde": "V85-7", "Hevonen": "#3 Ulix Turner", "Veikkaus_%": 3.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "🔥 SKRÄLLBUD! Segstark häst med Jepson i sulkyn och första barfota runt om."},
    {"Kohde": "V85-7", "Hevonen": "#4 Reagan Boko", "Veikkaus_%": 5.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Gjort det bra men möter hårt motstånd."},
    {"Kohde": "V85-7", "Hevonen": "#5 Zarajevo Games", "Veikkaus_%": 28.0, "Unibet": None, "Bonus": 1.10, "Perustelu": "💥 KLASSIG HÄST! Vunnit 5/8, enorm styrka."},
    {"Kohde": "V85-7", "Hevonen": "#6 Yardbird", "Veikkaus_%": 4.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Håller fin form."},
    {"Kohde": "V85-7", "Hevonen": "#7 Banzai Brodde", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Ulkona kärkitaistosta."},
    {"Kohde": "V85-7", "Hevonen": "#8 Vancouver Tile", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Barfota runt om på nytt."},
    {"Kohde": "V85-7", "Hevonen": "#9 John McClane", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.06, "Perustelu": "Första barfota runt om och rycktussar."},
    {"Kohde": "V85-7", "Hevonen": "#10 Po Tay Toes", "Veikkaus_%": 3.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "🔥 SPÄNNANDE UTMANARE! Vunnit 3/4 och får barfota fram för första gången."},
    {"Kohde": "V85-7", "Hevonen": "#11 Courage d'Inverne", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-7", "Hevonen": "#12 Wingait Stefan", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Vunnit 4/5 men spår 12 i Kriteriekval är iskallt."},

    # ==================== V85-8 (Solvalla L12, 2640a) ====================
    {"Kohde": "V85-8", "Hevonen": "#1 Pure Games", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "🔥 SPETSBUD! Dante Kolgjini laddar från spår 1."},
    {"Kohde": "V85-8", "Hevonen": "#2 Nanda Devi Cut", "Veikkaus_%": 28.0, "Unibet": None, "Bonus": 1.10, "Perustelu": "💥 SPETSFAVORIT OCH FÖRSTA RYCKTUSSAR! 3/4 vinnut keulasta."},
    {"Kohde": "V85-8", "Hevonen": "#3 Mahzarin W.", "Veikkaus_%": 1.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Spurtade vasst senast."},
    {"Kohde": "V85-8", "Hevonen": "#4 Long Night Out", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.05, "Perustelu": "Carl Johan Jepson kyytiin."},
    {"Kohde": "V85-8", "Hevonen": "#5 Vulcan Tile", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.06, "Perustelu": "Första barfota runt om."},
    {"Kohde": "V85-8", "Hevonen": "#6 Ready for Boarding", "Veikkaus_%": 6.0, "Unibet": None, "Bonus": 1.05, "Perustelu": "💥 KAPACITET FINNS! E3-voittaja elokuulta."},
    {"Kohde": "V85-8", "Hevonen": "#7 Ideal Kronos", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "🔥 MAXADE ÄNDRINGAR! Första rycktussar och amerikansk vagn."},
    {"Kohde": "V85-8", "Hevonen": "#8 Turner Ale", "Veikkaus_%": 2.0, "Unibet": None, "Bonus": 1.02, "Perustelu": "Första barfota bak."},
    {"Kohde": "V85-8", "Hevonen": "#9 Campitj", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.00, "Perustelu": "Haastava paikka."},
    {"Kohde": "V85-8", "Hevonen": "#10 Pepper Creation", "Veikkaus_%": 5.0, "Unibet": None, "Bonus": 1.08, "Perustelu": "🔥 STARK OCH FORMSTOPPAD! Vunnit 2/3 barfota runt om."},
    {"Kohde": "V85-8", "Hevonen": "#11 Evert Palema", "Veikkaus_%": 0.0, "Unibet": None, "Bonus": 1.05, "Perustelu": "Växlar upp till barfota runt om."},
    {"Kohde": "V85-8", "Hevonen": "#12 Intro", "Veikkaus_%": 41.0, "Unibet": None, "Bonus": 1.10, "Perustelu": "💥 KLASSIG FAVORIT! Nära seger senast, spår 12 rasittaa."}
]

# --- LASKENNALLISET VAHVISTUKSET ---
df = pd.DataFrame(data)

# 1. Painotetun suhteellisen todennäköisyyden laskeminen varustebonusten avulla
df['Painotettu_Peliosuus'] = df['Veikkaus_%'] * df['Bonus']
df['Arvioitu_Prob_%'] = df.groupby('Kohde')['Painotettu_Peliosuus'].transform(lambda x: (x / x.sum()) * 100)

# 2. Odotusarvon (EV) laskeminen Unibetin kertoimille
df['EV'] = df.apply(lambda row: (row['Arvioitu_Prob_%'] / 100) * row['Unibet'] if row['Unibet'] is not None else None, axis=1)

# --- STREAMLIT-KÄYTTÖLIITTYMÄN TULOSTUS ---

# Ylikertoimien nosto sivun alkuun
st.header("🎯 Parhaat Ylikertoimet & Peli-ideat (EV > 1.10)")
top_ev = df[df['EV'] > 1.10].sort_values(by='EV', ascending=False)

if not top_ev.empty:
    for _, r in top_ev.iterrows():
        st.success(f"**[{r['Kohde']}] {r['Hevonen']}** | Arvio: **{r['Arvioitu_Prob_%']:.1f}%** | Kerroin: **{r['Unibet']}** | EV: **{r['EV']:.2f}**\n\n_{r['Perustelu']}_")
else:
    st.info("Ei yksittäisiä Unibet-ylikertoimia saatavilla tässä aineistossa.")

st.divider()

# Kohdekohtainen tarkastelu
st.header("📊 Kohdekohtainen Analyysi (V85-1 – V85-8)")

kohteet = df['Kohde'].unique()
selected_kohde = st.selectbox("Valitse kohde tarkasteluun:", kohteet)

kohde_df = df[df['Kohde'] == selected_kohde].sort_values(by='Arvioitu_Prob_%', ascending=False)

st.subheader(f"Kohteen {selected_kohde} ranking & arviot:")

# Muotoillaan taulukko siististi
display_df = kohde_df[['Hevonen', 'Veikkaus_%', 'Arvioitu_Prob_%', 'Unibet', 'EV', 'Perustelu']].copy()
display_df.columns = ['Hevonen', 'Veikkaus %', 'Arvio %', 'Unibet Kerroin', 'EV', 'Perustelu']

st.dataframe(display_df, use_container_width=True)

# Yhteenvetotekstit valitusta kohteesta
st.markdown("### Hevosten perustelut:")
for _, r in kohde_df.iterrows():
    st.write(f"• **{r['Hevonen']}** (Arvio {r['Arvioitu_Prob_%']:.1f}%): {r['Perustelu']}")
