import numpy as np
import pandas as pd
import streamlit as st

# --- STREAMLIT-SIVUN ASETUKSET ---
st.set_page_config(page_title="Solvalla V85 Voittokone", layout="wide")

st.title("🏇 Solvalla V85 - Optimoitu Voittosimulaattori & Analyysi")
st.caption("Päivitetyt peliprosentit, H2H-kohtaamiset ja varustemuutokset hiottuna maksimipitoiseen muotoon.")

# --- KOKO V85-AINEISTO ---
data = [
    # ==================== V85-1 / L5 (2140a) ====================
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#1 Catch and Go", "Veikkaus_%": 6.0, "Bonus": 1.25, "Perustelu": "💥 MAKSIMOIDUT VARUSTEET & H2H-ETU! Ekaa kertaa jenkit + kokolaput + vetolaput. Keulasuosikki."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#2 Pure Games", "Veikkaus_%": 43.0, "Bonus": 1.00, "Perustelu": "Suosikki ilman uusia varusteviilauksia, keskinäisissä ottanut tappioita vauhtijuoksuissa."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#3 Com Best", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "Voitti viimeksi selvästi kovan nipun. Kuntopiikki!"},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#4 Long Night Out", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Aiemmissa keskinäisissä jäänyt hieman puristukseen."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#5 Vulcan Tile", "Veikkaus_%": 24.0, "Bonus": 1.02, "Perustelu": "Tasainen suorittaja, kohdannut suosikkeja aiemmin sitkeästi."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#6 Steady Spender", "Veikkaus_%": 1.0, "Bonus": 1.15, "Perustelu": "💥 JÄTTI-VARUSTEBONUS! Kengättä ympärinsä."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#7 Nanda Devi Cut", "Veikkaus_%": 3.0, "Bonus": 1.06, "Perustelu": "Huippukiri Com Bestin takana viimeksi (12,3a)."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#8 Dalton Russell", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Ulkorata rasittaa keskinäisissä kamppailuissa."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#9 Revanche Boko", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä vaikea ehtiä terävään kärkeen."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#10 Tennessee H.C.", "Veikkaus_%": 4.0, "Bonus": 1.02, "Perustelu": "Tarvitsee kovaa ylivauhtia."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#11 City Slicker", "Veikkaus_%": 4.0, "Bonus": 1.02, "Perustelu": "Voittanut aiemmin vastaavia gängejä, paikka 11 painaa."},
    {"Kohde": "V85-1", "Lähtö": "L5", "Hevonen": "#12 Ideal Kronos", "Veikkaus_%": 13.0, "Bonus": 1.00, "Perustelu": "Paha paikka 12 vaatii tuuria."},

    # ==================== V85-2 / L6 (2140a) ====================
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#1 Screen Time Limit", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "Sisäradan turvin saa tarkan reissun kärkiporukassa."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#2 S.G.Empress", "Veikkaus_%": 25.0, "Bonus": 1.18, "Perustelu": "💥 H2H-DOMINAATTORI! Lyönyt luokkansa tammat toistuvasti aiemmin."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#3 Melba Westwood", "Veikkaus_%": 4.0, "Bonus": 1.04, "Perustelu": "Nappipaikalta smyygaa asemiin."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#4 First Class U.S.", "Veikkaus_%": 2.0, "Bonus": 1.05, "Perustelu": "Mukaan kakkosketjun haastajiin."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#5 Ballerina", "Veikkaus_%": 0.0, "Bonus": 1.12, "Perustelu": "🔥 TÄYDELLINEN HIRMUMERKKI! Ekaa kertaa ilman kaikkia kenkiä."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#6 S.G.Dacota", "Veikkaus_%": 11.0, "Bonus": 1.02, "Perustelu": "Tasainen suorittaja karsinnoissa."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#7 Fly The Coup", "Veikkaus_%": 11.0, "Bonus": 1.00, "Perustelu": "Rata 7 verottaa alussa."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#8 Matchmadeinheaven", "Veikkaus_%": 0.0, "Bonus": 1.04, "Perustelu": "Kapasiteettia on, rata 8 erittäin haastava."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#9 Blast Off", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä passiivinen taktiikka."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#10 Great Pride", "Veikkaus_%": 44.0, "Bonus": 1.05, "Perustelu": "Suosikki, mutta kärsinyt keskinäisissä aiemmin pussituksista."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#11 Good Habit", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Kaukana kärjestä."},
    {"Kohde": "V85-2", "Lähtö": "L6", "Hevonen": "#12 Cantilena", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Lähtöpaikka 12 vaatii ihmeitä."},

    # ==================== V85-3 / L7 (2140a) ====================
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#1 Oriana Boko", "Veikkaus_%": 47.0, "Bonus": 1.08, "Perustelu": "💥 Vahva suosikki sisäradalta, hallinnut aiemmin vastaavia karsintoja."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#2 Lavender", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Sisäradalta asemiin."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#3 Charma", "Veikkaus_%": 19.0, "Bonus": 1.15, "Perustelu": "💥 HUIPPUUUTINEN & H2H-YLLÄTTÄJÄ! Barfota runt om ekaa kertaa + Kihlström."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#4 Osken", "Veikkaus_%": 6.0, "Bonus": 1.12, "Perustelu": "🔥 ALIPELATTU SUOSIKKI! Vahvat näyttö- ja keulajuoksut alla."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#5 Clean Community", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Perussuorittaja."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#6 Valnes Penny", "Veikkaus_%": 3.0, "Bonus": 1.08, "Perustelu": "Björn Goop ratissa ja barfota fram -etu."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#7 Unicum", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Ulkopuolelta haastavaa."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#8 Nightingale", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Rata 8 rasittaa."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#9 Egerie", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Takarivin merkki."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#10 Quina", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#11 Lilium Sisu", "Veikkaus_%": 12.0, "Bonus": 1.00, "Perustelu": "Pelattu suosikkien takana."},
    {"Kohde": "V85-3", "Lähtö": "L7", "Hevonen": "#12 S.G.Eye Candy", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Synkkä paikka."},

    # ==================== V85-4 / L8 (2140a) ====================
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#1 Unrestricted", "Veikkaus_%": 11.0, "Bonus": 1.04, "Perustelu": "Hyvä paikka sisällä, keskinäisissä kamppailut tasan."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#2 Backwood Gisella", "Veikkaus_%": 29.0, "Bonus": 1.15, "Perustelu": "💥 LÄHDÖN PÄÄKEULAHÄST! Vahvat H2H-tulokset ja huippupaikka."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#3 La Nova", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Odotellaan parannusta."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#4 Free Time Trot", "Veikkaus_%": 3.0, "Bonus": 1.06, "Perustelu": "Tasaisen varma keskinäisissä vauhdeissa."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#5 Lavender", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Keskiradalta mukaan."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#6 Scarfo Pellini", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Lupauksia herättävä."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#7 Screen Time Limit", "Veikkaus_%": 21.0, "Bonus": 1.00, "Perustelu": "Haastaja ulkoreunalta."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#8 S.G.Empress", "Veikkaus_%": 19.0, "Bonus": 1.02, "Perustelu": "Luokkaa löytyy, mutta rata 8 vaikeuttaa peliä."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#9 Egerie", "Veikkaus_%": 13.0, "Bonus": 1.00, "Perustelu": "Hyvin pelattu takarivistä."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#10 Hawthorne Effect", "Veikkaus_%": 1.0, "Bonus": 1.14, "Perustelu": "🔥 H2H-SUPERLÖYTÖ OCH YLLÄTTÄJÄ! Voittanut keskinäiset aiemmin selvästi."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#11 Great Pride", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Iskukykyinen takarivistä."},
    {"Kohde": "V85-4", "Lähtö": "L8", "Hevonen": "#12 S.G.Dacota", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Paha paikka 12."},

    # ==================== V85-5 / L9 (2140a) ====================
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#1 Fatal Attraction", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Smyygaa innerspårilta."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#2 Procope", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Outsider."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#3 Jula Donatella", "Veikkaus_%": 2.0, "Bonus": 1.06, "Perustelu": "Ekaa kertaa ilman etukenkiä (barfota fram)."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#4 Fatal Attraction", "Veikkaus_%": 21.0, "Bonus": 1.10, "Perustelu": "💥 2 keulavoittoa putkeen ja H2H-edut puolellaan."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#5 Illicit Hooch", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "Barfota runt om & blinkers -tuplaviritys."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#6 N.Y.Easy On Me", "Veikkaus_%": 5.0, "Bonus": 1.02, "Perustelu": "Mukaan haastajajoukkoon."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#7 I See Tail Lights", "Veikkaus_%": 37.0, "Bonus": 1.12, "Perustelu": "💥 Hirmuisessa iskussa (1.10,9a edellisen voiton aika). Hallinnut aiemminkin."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#8 Cruiser", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Huippusuku, rata 8 rasittaa."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#9 Zeebreeze", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Vaikea tehtävä."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#10 Navy Cut", "Veikkaus_%": 3.0, "Bonus": 1.02, "Perustelu": "Hyvä kiri alla keskinäisissä vauhdeissa."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#11 Mellby Orkide", "Veikkaus_%": 24.0, "Bonus": 1.18, "Perustelu": "💥 JÄTTI-VARUSTEBONUS! Redén riisuu kengät ekaa kertaa (barfota runt om) + Kihlström."},
    {"Kohde": "V85-5", "Lähtö": "L9", "Hevonen": "#12 Klara Godiva", "Veikkaus_%": 0.0, "Bonus": 1.08, "Perustelu": "🔥 TAULUAAN PAREMPI! Laukkasi varman voiton viime metreillä."},

    # ==================== V85-6 / L10 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#1 In Fine Fettle", "Veikkaus_%": 4.0, "Bonus": 1.04, "Perustelu": "Kengättä edestä & jenkit."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#2 Thor Tooma", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Smyygaa sisällä."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#3 Bourbon Phantasy", "Veikkaus_%": 4.0, "Bonus": 1.10, "Perustelu": "🔥 Wäjerstenin oma valinta hyvältä paikalta, hienot H2H-esiintymiset."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#4 Kodiak Zet", "Veikkaus_%": 76.0, "Bonus": 1.20, "Perustelu": "💥 KOKO ILLAN PÄÄVARMA & H2H-DOMINAATTORI! Ekaa kertaa ilman takakenkiä & jenkkikärryt."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#5 Baby Love", "Veikkaus_%": 1.0, "Bonus": 1.12, "Perustelu": "Barfota runt om & jenkit ekaa kertaa."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#6 Neutron Star", "Veikkaus_%": 11.0, "Bonus": 1.06, "Perustelu": "💥 PÄÄHAASTAJA! Ilman etukenkiä sitkeä kuolemanpaikkajyrä."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#7 Crew Lane", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Haastava paikka."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#8 Bys Arigato", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Kaukana kärjestä."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#9 Prince of Euro", "Veikkaus_%": 1.0, "Bonus": 1.10, "Perustelu": "🔥 Voittanut aiemmin kovia lähtöjä (mm. Pure Gamesin), ekaa kertaa barfota runt om."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#10 Pivot Caigoo", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#11 First Festive Vir", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V85-6", "Lähtö": "L10", "Hevonen": "#12 Xanthis Lewis", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Kunto piikissä, paha paikka."},

    # ==================== V85-7 / L11 (2640a) ====================
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#1 Coloneltomparker", "Veikkaus_%": 52.0, "Bonus": 1.15, "Perustelu": "💥 KEULASUOSIKKI & FÖRSTA BARFOTA RUNT OM! Voittanut aiemmat keskinäiset voimalla."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#2 Bravo Desoto", "Veikkaus_%": 2.0, "Bonus": 1.06, "Perustelu": "Första barfota fram, saa tarkan juoksun suosikin takana."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#3 Ulix Turner", "Veikkaus_%": 2.0, "Bonus": 1.10, "Perustelu": "🔥 H2H-SKRÄLLBUD! Jepson ratissa ja ensimmäistä kertaa ilman kaikkia kenkiä."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#4 Reagan Boko", "Veikkaus_%": 6.0, "Bonus": 1.02, "Perustelu": "Tehnyt hyviä juoksuja aiemmissa karsinnoissa."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#5 Zarajevo Games", "Veikkaus_%": 28.0, "Bonus": 1.12, "Perustelu": "💥 KLASSIKKO-ORHI! Voittanut 5/8 ja peitonnut monet näistä aiemmin."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#6 Yardbird", "Veikkaus_%": 5.0, "Bonus": 1.00, "Perustelu": "Hyvässä kunnossa."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#7 Banzai Brodde", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Ei riitä kärkeen."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#8 Vancouver Tile", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Barfota runt om."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#9 John McClane", "Veikkaus_%": 0.0, "Bonus": 1.08, "Perustelu": "Ekaa kertaa barfota runt om ja rycktussar."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#10 Po Tay Toes", "Veikkaus_%": 3.0, "Bonus": 1.10, "Perustelu": "🔥 SPÄNNANDE UTMANARE! Voittanut 3/4 ja ekaa kertaa barfota fram."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#11 Courage d'Inverne", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takaa mahdotonta."},
    {"Kohde": "V85-7", "Lähtö": "L11", "Hevonen": "#12 Wingait Stefan", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Voittanut 4/5, mutta spår 12 tähän karsintaan syö mahkut."},

    # ==================== V85-8 / L12 (2640a) ====================
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#1 Pure Games", "Veikkaus_%": 3.0, "Bonus": 1.10, "Perustelu": "🔥 SPETSBUD! Dante Kolgjini lataa ykkösestä keulaan."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#2 Nanda Devi Cut", "Veikkaus_%": 5.0, "Bonus": 1.15, "Perustelu": "💥 HUIPPUIDEANOSTO! Ekaa kertaa rycktussar, 3/4 voittanut keulasta ja vahva keskinäisissä."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#3 Mahzarin W.", "Veikkaus_%": 25.0, "Bonus": 1.02, "Perustelu": "Suosikkeja, tehnyt teräviä kirejä aiemmin."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#4 Long Night Out", "Veikkaus_%": 1.0, "Bonus": 1.06, "Perustelu": "Carl Johan Jepson vahvisteena."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#5 Vulcan Tile", "Veikkaus_%": 2.0, "Bonus": 1.08, "Perustelu": "Ensimmäistä kertaa barfota runt om."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#6 Ready for Boarding", "Veikkaus_%": 2.0, "Bonus": 1.08, "Perustelu": "💥 E3-VOITTAJA ELOKUULTA! Luokka ja keskinäiset näytöt riittävät yllätykseen."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#7 Ideal Kronos", "Veikkaus_%": 9.0, "Bonus": 1.12, "Perustelu": "🔥 MAXADE ÄNDRINGAR! Ekaa kertaa rycktussar + amerikansk vagn."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#8 Turner Ale", "Veikkaus_%": 3.0, "Bonus": 1.04, "Perustelu": "Första barfota bak."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#9 Campitj", "Veikkaus_%": 12.0, "Bonus": 1.00, "Perustelu": "Haastava paikka takarivissä."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#10 Pepper Creation", "Veikkaus_%": 4.0, "Bonus": 1.10, "Perustelu": "STARK OCH FORMSTOPPAD! Voittanut 2/3 barfota runt om -balanssilla."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#11 Evert Palema", "Veikkaus_%": 35.0, "Bonus": 1.06, "Perustelu": "Suosikki takarivistä, barfota runt om -vaihde silmään."},
    {"Kohde": "V85-8", "Lähtö": "L12", "Hevonen": "#12 Intro", "Veikkaus_%": 0.0, "Bonus": 1.10, "Perustelu": "Klassinen suosikki, spår 12 takia jäänyt täysin ilman peliä."}
]

df = pd.DataFrame(data)

# 1. Suhteellisen todennäköisyyden peruslaskenta
df['Painotettu_Osuus'] = df['Veikkaus_%'] * df['Bonus']
df['Arvioitu_Prob_%'] = df.groupby('Kohde')['Painotettu_Osuus'].transform(lambda x: (x / x.sum()) * 100 if x.sum() > 0 else 0)
df['Ero_%'] = df['Arvioitu_Prob_%'] - df['Veikkaus_%']

# --- INTERAKTIIVINEN MONTE CARLO -SIMULAATTORI ---
st.sidebar.header("⚙️ Simulaattorin Asetukset")
n_simulations = st.sidebar.slider("Simulaatiotoistojen määrä", min_value=1000, max_value=50000, value=10000, step=1000)
run_sim = st.sidebar.button("🎲 Suorita Lopullinen Simulaatio", type="primary")

if run_sim or 'sim_done' not in st.session_state:
    st.session_state['sim_done'] = True
    # Monte Carlo -simulaatio jokaiselle lähdölle
    sim_results = {}
    for kohde, group in df.groupby('Kohde'):
        probs = group['Arvioitu_Prob_%'].values / 100.0
        probs = probs / probs.sum()  # Varmistetaan summaksi 1
        winners = np.random.choice(group['Hevonen'].values, size=n_simulations, p=probs)
        unique, counts = np.unique(winners, return_counts=True)
        counts_dict = dict(zip(unique, counts))
        sim_results[kohde] = {h: (counts_dict.get(h, 0) / n_simulations) * 100 for h in group['Hevonen'].values}
    
    # Liitetään simulaation voittotodennäköisyydet
    df['Simuloitu_Voitto_%'] = df.apply(lambda r: sim_results[r['Kohde']][r['Hevonen']], axis=1)

# --- SIVUN PÄÄVALIKKO: YHTEENVETO VS KOHTEET ---
st.markdown("---")

# Yhteenvetonostot
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("💥 Simulaation 3 Varminta Pankkia (Bankerit)")
    top_bankers = df.sort_values(by='Simuloitu_Voitto_%', ascending=False).groupby('Kohde').first().reset_index()
    top_bankers = top_bankers.sort_values(by='Simuloitu_Voitto_%', ascending=False).head(3)
    for _, r in top_bankers.iterrows():
        st.success(f"**[{r['Kohde']}] {r['Hevonen']}** | Simuloitu voittomahdollisuus: **{r['Simuloitu_Voitto_%']:.1f}%** (Veikkaus: {r['Veikkaus_%']}%)")

with col_b:
    st.subheader("💣 3 Kuuminta Alipelattua Jätti-Ideaa (EV+)")
    top_underdogs = df[df['Veikkaus_%'] < 10.0].sort_values(by='Ero_%', ascending=False).head(3)
    for _, r in top_underdogs.iterrows():
        st.warning(f"🔥 **[{r['Kohde']}] {r['Hevonen']}** | Pelattu: **{r['Veikkaus_%']:.1f}%** ➔ Simulaatio: **{r['Simuloitu_Voitto_%']:.1f}%** (+{r['Ero_%']:.1f}%)\n\n_{r['Perustelu']}_")

st.markdown("---")
st.header("📊 V85-Kohteet (Järjestyksessä V85-1 – V85-8)")

# KÄYTTÖLIITTYMÄN VÄLILEHDET NUMEROJÄRJESTYKSESSÄ
tabs = st.tabs(["V85-1 (L5)", "V85-2 (L6)", "V85-3 (L7)", "V85-4 (L8)", "V85-5 (L9)", "V85-6 (L10)", "V85-7 (L11)", "V85-8 (L12)"])

kohteet_list = ["V85-1", "V85-2", "V85-3", "V85-4", "V85-5", "V85-6", "V85-7", "V85-8"]

for tab, kohde_code in zip(tabs, kohteet_list):
    with tab:
        k_df = df[df['Kohde'] == kohde_code].sort_values(by='Simuloitu_Voitto_%', ascending=False)
        
        lahto_nimi = k_df['Lähtö'].iloc[0]
        st.subheader(f"Lähtö {lahto_nimi} ({kohde_code}) - Lopulliset Simulaatiotulokset")
        
        # Luodaan nätti taulukko
        disp_df = k_df[['Hevonen', 'Veikkaus_%', 'Bonus', 'Simuloitu_Voitto_%', 'Ero_%']].copy()
        disp_df.columns = ['Hevonen', 'Veikkaus %', 'Varuste/H2H Kerroin', 'Simulaatio Voitto %', 'Peliarvo (Ero %)']
        
        st.dataframe(
            disp_df.style.format({
                'Veikkaus %': '{:.1f}%',
                'Varuste/H2H Kerroin': '{:.2f}',
                'Simulaatio Voitto %': '{:.1f}%',
                'Peliarvo (Ero %)': '{:+.1f}%'
            }).background_gradient(subset=['Simulaatio Voitto %'], cmap='Blues'),
            use_container_width=True
        )
        
        st.markdown("### 📝 Analysaattorin kommentit hevosittain:")
        for _, r in k_df.iterrows():
            badge = "🟢 **SUOSIKKI**" if r['Simuloitu_Voitto_%'] > 25 else ("🟡 **HAASTAJA**" if r['Simuloitu_Voitto_%'] > 8 else "⚪ **YLLÄTTÄJÄ**")
            st.markdown(f"{badge} **{r['Hevonen']}** (Simulaatio: **{r['Simuloitu_Voitto_%']:.1f}%** | Pelattu: {r['Veikkaus_%']:.1f}%): {r['Perustelu']}")
