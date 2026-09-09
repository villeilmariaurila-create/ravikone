import random
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. LIVE-PELIJAKAUMA & VAIHTO (PÄIVITETÄÄN TÄHÄN)
# ==============================================================================

LIVE_PELIJAKAUMA = {
    5: {1: 3, 2: 24, 3: 1, 4: 4, 5: 10, 6: 5, 7: 3, 8: 12, 9: 35, 10: 1, 11: 1, 12: 2},
    6: {1: 2, 2: 10, 3: 2, 4: 29, 5: 6, 6: 4, 7: 1, 8: 24, 9: 1, 10: 2, 11: 4, 12: 1, 13: 9, 14: 1, 15: 5},
    7: {1: 44, 2: 2, 3: 3, 4: 10, 5: 9, 6: 26, 7: 7},
    8: {1: 2, 2: 3, 3: 10, 4: 1, 5: 3, 6: 36, 7: 2, 8: 13, 9: 2, 10: 3, 11: 1, 12: 15, 13: 4, 14: 2, 15: 1},
    9: {1: 63, 2: 18, 3: 5, 4: 2, 5: 1, 6: 1, 7: 3, 8: 3, 9: 1, 10: 1, 11: 1, 12: 0},
    10: {1: 1, 2: 1, 3: 2, 4: 6, 5: 10, 6: 27, 7: 2, 8: 15, 9: 5, 10: 7, 11: 0, 12: 3, 13: 16, 14: 1, 15: 2},
    11: {1: 7, 2: 5, 3: 3, 4: 48, 5: 2, 6: 6, 7: 2, 8: 14, 9: 1, 10: 7, 11: 2, 12: 1}
}

LIVE_VAIHTOTIEDOT = {
    "vaihto": "46 319 €",
    "jakosumma": "1 350 933 €",
    "jackpot": "1 320 826 €"
}

# ==============================================================================
# 2. HAGMYREN DATA & JENS SJÖDÉN TILASTOT
# ==============================================================================

DATABANK = {
    5: {
        "nimi": "Lopp 5 - STL Klass I (V85-1, V5-2)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a",
        "vihje": "<b>Daniel Berglund:</b> 9 Night Hawk ja 2 Hip To Be Square vahvoilla.<br><b>Jens Sjödén - Tilastot:</b> Hagmyrenissä pelaajat ovat osuvat kahden suosituimman joukkoon 10/11 kertaa tässä luokassa. Radat 4-5 huippuradoja, 7-12 ottavat vain 28% voitoista.",
        "hevoset": [
            {"numero": 1, "nimi": "T.Wall's Notorius", "ohjastaja": "Jomar Blekkan", "peruspaino": 1.0},
            {"numero": 2, "nimi": "Hip To Be Square", "ohjastaja": "Per Lennartsson", "peruspaino": 1.4},
            {"numero": 3, "nimi": "Sign Of Times", "ohjastaja": "Tomas Pettersson", "peruspaino": 0.9},
            {"numero": 4, "nimi": "Geisha Road Grif", "ohjastaja": "Jorma Kontio", "peruspaino": 1.0},
            {"numero": 5, "nimi": "Macho Cabrio B.B.", "ohjastaja": "Peter G Norman", "peruspaino": 1.0},
            {"numero": 6, "nimi": "Henessi Kiev", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.8},
            {"numero": 7, "nimi": "Takter", "ohjastaja": "Hans G Eriksson", "peruspaino": 0.6},
            {"numero": 8, "nimi": "Herkules A'lir", "ohjastaja": "Rikard N Skoglund", "peruspaino": 1.2},
            {"numero": 9, "nimi": "Night Hawk", "ohjastaja": "Mats E Djuse", "peruspaino": 1.25},
            {"numero": 10, "nimi": "Huchuy Qosqo", "ohjastaja": "Anders Eriksson", "peruspaino": 0.5},
            {"numero": 11, "nimi": "De Är Hon", "ohjastaja": "Ulf Ohlsson", "peruspaino": 0.4},
            {"numero": 12, "nimi": "Sandsjöns Cantona", "ohjastaja": "Claes Sjöström", "peruspaino": 0.8},
        ]
    },
    6: {
        "nimi": "Lopp 6 - STL Kallblodsdivisionen (V85-2)",
        "matka": "2140m Voltstart",
        "tyyppi": "tasoitus",
        "vihje": "<b>Daniel Berglund:</b> Sekava lähtö. 8 Teknologen paras takaa, muuten paalun hevoset vahvoja.<br><b>Jens Sjödén - Tilastot:</b> Syysomgångilla takaa tullaan paremmin läpi (21% voitoista takariveiltä/kauempaa).",
        "hevoset": [
            {"numero": 1, "nimi": "Fosshaug Frasse", "ohjastaja": "Michaela B Fransson", "peruspaino": 0.6},
            {"numero": 2, "nimi": "Sangviks Lynet", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.1},
            {"numero": 3, "nimi": "Andarnas Patron", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.9},
            {"numero": 4, "nimi": "Silke Sjarmör", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.2},
            {"numero": 5, "nimi": "Ellbert", "ohjastaja": "Mats E Djuse", "peruspaino": 1.3},
            {"numero": 6, "nimi": "Guli Hektor", "ohjastaja": "Örjan Kihlström", "peruspaino": 0.8},
            {"numero": 7, "nimi": "Tåga Ryker", "ohjastaja": "Ingvar Nyberg", "peruspaino": 0.5},
            {"numero": 8, "nimi": "Teknologen", "ohjastaja": "Robert Skoglund", "peruspaino": 1.5},
            {"numero": 9, "nimi": "Ava Modde", "ohjastaja": "Henrik Svensson", "peruspaino": 0.6},
            {"numero": 10, "nimi": "Re Alkapital", "ohjastaja": "Joakim Eskilsson", "peruspaino": 0.6},
            {"numero": 11, "nimi": "Mira Kiro", "ohjastaja": "Jorma Kontio", "peruspaino": 0.7},
            {"numero": 12, "nimi": "Ersa Frej", "ohjastaja": "Nathalie Blom", "peruspaino": 0.3},
            {"numero": 13, "nimi": "Klack Vidar", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.4},
            {"numero": 14, "nimi": "Blixen", "ohjastaja": "Jan-Olof Johansson", "peruspaino": 0.4},
            {"numero": 15, "nimi": "Guli Em", "ohjastaja": "Marcus Lilius", "peruspaino": 0.4},
        ]
    },
    7: {
        "nimi": "Lopp 7 - STL Gulddivisionen EJ's Guldsko (V85-3)",
        "matka": "1640m Autostart",
        "tyyppi": "guld",
        "vihje": "<b>Daniel Berglund:</b> Vain 7 hevosta, taktinen taisto keulasta.<br><b>Jens Sjödén - Tilastot:</b> Vain 7 osallistujaa pudottaa jo entisestään erittäin matalan skrällitodennäköisyyden lähes nollaan. Vain 2 skrälliä sitten vuoden 1995.",
        "hevoset": [
            {"numero": 1, "nimi": "Before Takeoff", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.45},
            {"numero": 2, "nimi": "Santos De Castella", "ohjastaja": "Marcus Lilius", "peruspaino": 0.6},
            {"numero": 3, "nimi": "Romulus Tooma", "ohjastaja": "Peter G Norman", "peruspaino": 0.4},
            {"numero": 4, "nimi": "Mizai", "ohjastaja": "Per Lennartsson", "peruspaino": 1.0},
            {"numero": 5, "nimi": "Lando Mearas", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.25},
            {"numero": 6, "nimi": "Mellby Joker", "ohjastaja": "Mats E Djuse", "peruspaino": 1.15},
            {"numero": 7, "nimi": "Jerka Sting", "ohjastaja": "Claes Sjöström", "peruspaino": 0.85},
        ]
    },
    8: {
        "nimi": "Lopp 8 - STL Dubbelklasslopp (V85-4, V4-1, V5-1)",
        "matka": "2640m Autostart",
        "tyyppi": "dubbelklass",
        "vihje": "<b>Daniel Berglund:</b> Erittäin avoin lähtö, 8 Uno ja 11 Bear Victor mielenkiintoisia.<br><b>Jens Sjödén - Tilastot:</b> Paras paikka skrällille! Suosikit voittavat vain 20%, 2-suosikki 25% ja skrälli (rank 4+) toteutuu 4 kerta 10:stä.",
        "hevoset": [
            {"numero": 1, "nimi": "Napoleon Sisu", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.8},
            {"numero": 2, "nimi": "Ies Ingusmemory", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.95},
            {"numero": 3, "nimi": "Ytowns Ulrik", "ohjastaja": "Jorma Kontio", "peruspaino": 1.1},
            {"numero": 4, "nimi": "Classique Launcher", "ohjastaja": "Olle Alsén", "peruspaino": 0.5},
            {"numero": 5, "nimi": "Umpteen", "ohjastaja": "Nathalie Blom", "peruspaino": 1.2},
            {"numero": 6, "nimi": "Holiday Island", "ohjastaja": "Anders Eriksson", "peruspaino": 1.35},
            {"numero": 7, "nimi": "Sacrebleu", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.85},
            {"numero": 8, "nimi": "Uno", "ohjastaja": "Mats E Djuse", "peruspaino": 1.1},
            {"numero": 9, "nimi": "Whiskey Majo", "ohjastaja": "Marcus Lilius", "peruspaino": 0.75},
            {"numero": 10, "nimi": "Timotejs Gamble", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.0},
            {"numero": 11, "nimi": "Bear Victor", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.25},
            {"numero": 12, "nimi": "Lion Sisu", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.15},
            {"numero": 13, "nimi": "Jaguar Ima", "ohjastaja": "Fredrik Plassen", "peruspaino": 0.6},
            {"numero": 14, "nimi": "Flat Tire Grue", "ohjastaja": "Oskar Florhed", "peruspaino": 0.4},
            {"numero": 15, "nimi": "Vidar Burge", "ohjastaja": "Claes Sjöström", "peruspaino": 0.5},
        ]
    },
    9: {
        "nimi": "Lopp 9 - Tammer Pokal Kallblods-SM ston (V85-5, V4-2)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a_sm",
        "vihje": "<b>Daniel Berglund:</b> 1 Majblomster on keulasta vaikea voittaa.<br><b>Jens Sjödén - Tilastot:</b> Kallblods-SM ston on pelisuosikkien juhlaa (alkaen 2002). Ei skrällejä koskaan. 'Det är en god idé att spika i V85-5.'",
        "hevoset": [
            {"numero": 1, "nimi": "Majblomster", "ohjastaja": "Mats E Djuse", "peruspaino": 2.1},
            {"numero": 2, "nimi": "Prinsesse Ness Tjo", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.2},
            {"numero": 3, "nimi": "Tekno Tana", "ohjastaja": "Robert Skoglund", "peruspaino": 1.0},
            {"numero": 4, "nimi": "Hulte Alva", "ohjastaja": "Linda S Hedström", "peruspaino": 0.8},
            {"numero": 5, "nimi": "Guli Stina", "ohjastaja": "Ulf Ohlsson", "peruspaino": 0.5},
            {"numero": 6, "nimi": "Hög Decibel", "ohjastaja": "Stig Jarle Röste", "peruspaino": 0.4},
            {"numero": 7, "nimi": "Hulte Annika", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.7},
            {"numero": 8, "nimi": "Jonases Ninja", "ohjastaja": "Jan-Olov Åberg", "peruspaino": 0.5},
            {"numero": 9, "nimi": "Eldida", "ohjastaja": "Ida Eriksson", "peruspaino": 0.3},
            {"numero": 10, "nimi": "Rötungen", "ohjastaja": "Micael Melander", "peruspaino": 0.3},
            {"numero": 11, "nimi": "Saga Kiro", "ohjastaja": "Per Lennartsson", "peruspaino": 0.4},
            {"numero": 12, "nimi": "Ethel", "ohjastaja": "Henrik Svensson", "peruspaino": 0.4},
        ]
    },
    10: {
        "nimi": "Lopp 10 - STL Stodivisionen (V85-6, V4-3, DD-1)",
        "matka": "2640m Voltstart",
        "tyyppi": "tasaus",
        "vihje": "<b>Daniel Berglund:</b> Vaikea tammalähtö. 6 Kopparmärra, 4 Grove's Maple Poof, 8 Brionne.<br><b>Jens Sjödén - Tilastot:</b> Syysomgångin 170m loppusuora ja 2640m matka vaativat kestävyyttä.",
        "hevoset": [
            {"numero": 1, "nimi": "Sessan Of Man", "ohjastaja": "Henrik Svensson", "peruspaino": 0.5},
            {"numero": 2, "nimi": "Adora Liss", "ohjastaja": "Fredrik Plassen", "peruspaino": 0.6},
            {"numero": 3, "nimi": "Pure Jouline", "ohjastaja": "Linus Lönn", "peruspaino": 0.95},
            {"numero": 4, "nimi": "Grove's Maple Poof", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.25},
            {"numero": 5, "nimi": "Bohemian Maid", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.3},
            {"numero": 6, "nimi": "Kopparmärra", "ohjastaja": "Nathalie Blom", "peruspaino": 0.9},
            {"numero": 7, "nimi": "C'est Ma Course", "ohjastaja": "Lucas H Vikström", "peruspaino": 0.8},
            {"numero": 8, "nimi": "Brionne", "ohjastaja": "Rikard N Skoglund", "peruspaino": 1.25},
            {"numero": 9, "nimi": "Melina Havelock", "ohjastaja": "Carl Johan Jepson", "peruspaino": 0.85},
            {"numero": 10, "nimi": "Ajlexes Gourmand", "ohjastaja": "Tomas Pettersson", "peruspaino": 1.05},
            {"numero": 11, "nimi": "Global Empress", "ohjastaja": "Marcus Lilius", "peruspaino": 0.8},
            {"numero": 12, "nimi": "Danceinthedark F.", "ohjastaja": "Katrin K Frick", "peruspaino": 0.5},
            {"numero": 13, "nimi": "Rupie", "ohjastaja": "Mats E Djuse", "peruspaino": 0.9},
            {"numero": 14, "nimi": "Frida S.H.", "ohjastaja": "Örjan Kihlström", "peruspaino": 0.4},
            {"numero": 15, "nimi": "Kueen Simoni", "ohjastaja": "Claes Sjöström", "peruspaino": 0.6},
        ]
    },
    11: {
        "nimi": "Lopp 11 - STL Bronsdivisionen (V85-7, V4-4, DD-2)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a_brons",
        "vihje": "<b>Daniel Berglund:</b> 4 Mellby Mowgli, 3 Graces Bird, 10 Gosa Gosing.<br><b>Jens Sjödén - Tilastot:</b> Hopea/Pronssitasolla 2140a Hagmyrenissä skrällää todella harvoin (vain 2/20 skrälliä). Top-suosikit vahvoilla.",
        "hevoset": [
            {"numero": 1, "nimi": "Bruce Braylon", "ohjastaja": "Per Lennartsson", "peruspaino": 1.2},
            {"numero": 2, "nimi": "Pineapple", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.1},
            {"numero": 3, "nimi": "Graces Bird", "ohjastaja": "Fredrik Plassen", "peruspaino": 1.05},
            {"numero": 4, "nimi": "Mellby Mowgli", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.4},
            {"numero": 5, "nimi": "Ebbot Rice", "ohjastaja": "Linus Lönn", "peruspaino": 0.7},
            {"numero": 6, "nimi": "Jaguar Godiva", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.0},
            {"numero": 7, "nimi": "Don E.Star", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.5},
            {"numero": 8, "nimi": "Lucky Silver", "ohjastaja": "Mats E Djuse", "peruspaino": 1.0},
            {"numero": 9, "nimi": "Elvis T.C.B.", "ohjastaja": "Marcus Lilius", "peruspaino": 0.8},
            {"numero": 10, "nimi": "Gosa Gosing", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.85},
            {"numero": 11, "nimi": "Punchboard", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.6},
            {"numero": 12, "nimi": "Slivovitz Lover", "ohjastaja": "Claes Sjöström", "peruspaino": 0.4},
        ]
    }
}

# Liitetään peliprosentit
for lahto_id, hevoset in DATABANK.items():
    l_pelit = LIVE_PELIJAKAUMA.get(lahto_id, {})
    for h in hevoset["hevoset"]:
        h["peli_pct"] = l_pelit.get(h["numero"], 0)

# ==============================================================================
# 3. LASKENTAMOOTTORI (TILASTOLISIN KORJAUSKERROIN)
# ==============================================================================

def laske_painotettu_todennakoisyys(lahto_data: dict) -> list:
    hevoset = lahto_data["hevoset"]
    tyyppi = lahto_data["tyyppi"]
    
    korjatut_painot = []
    for h in hevoset:
        paino = h["peruspaino"]
        nro = h["numero"]
        peli = h["peli_pct"]
        
        # 1. SJÖDÉN SPÅRSTATISTIK (2140a: L5, L9, L11)
        if tyyppi in ["2140a", "2140a_sm", "2140a_brons"]:
            if nro in [4, 5]:
                paino *= 1.20  # Toppspår 4-5
            elif nro == 2:
                paino *= 0.85  # Överskattat spår 2
            elif nro >= 7:
                paino *= 0.80  # Radat 7-12 ottavat vain 28% voitoista
                
        # 2. SJÖDÉN ERITYISLÄHDÖT
        if tyyppi == "2140a_sm":  # L9 Kallblods-SM (Majblomster)
            if peli > 50:
                paino *= 1.45  # SM-suosikin tilastollinen dominanssi (ei skrällejä)
        
        elif tyyppi == "guld":  # L7 EJ's Guldsko (7 hevosta)
            if peli > 30:
                paino *= 1.30  # Ei skrällejä pienissä kultadivisioonissa
            elif peli < 5:
                paino *= 0.3  # Yllättäjät todella tiukilla
                
        elif tyyppi == "dubbelklass":  # L8 Dubbelklasslopp
            if peli < 10:
                paino *= 1.35  # Skrällihakuisuutta lisätty (40% skrällitoteutuma)
            elif peli > 30:
                paino *= 0.85  # Suosikkivoitot vain 20%
                
        korjatut_painot.append((nro, max(paino, 0.05)))
        
    return korjatut_painot

def simuloi_lahto_tilastoilla(lahto_data: dict, kierrokset: int = 10000) -> dict:
    painot_tiedot = laske_painotettu_todennakoisyys(lahto_data)
    numerot = [p[0] for p in painot_tiedot]
    painot = [p[1] for p in painot_tiedot]
    
    voitot = {num: 0 for num in numerot}
    for _ in range(kierrokset):
        voittaja = random.choices(numerot, weights=painot, k=1)[0]
        voitot[voittaja] += 1
        
    return {num: round((maara / kierrokset) * 100, 1) for num, maara in voitot.items()}

SIM_TULOKSET = {}
for lahto_id, lahto_data in DATABANK.items():
    SIM_TULOKSET[lahto_id] = simuloi_lahto_tilastoilla(lahto_data)

# ==============================================================================
# 4. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.set_page_config(page_title="Hagmyren V85 - Sjödén Simulaattori", layout="wide")

st.title("🏇 Hagmyren V85 - Live-Jakauma & Sjödén-Tilastosimulaattori")
st.caption("Monte Carlo + Jens Sjödén Tilastokorjaukset (170m upplopp, 2140a radat, SM-tilastot) + Live-vaihto")

# Live-vaihto yläpalkissa
m1, m2, m3 = st.columns(3)
m1.metric("Vaihto", LIVE_VAIHTOTIEDOT["vaihto"])
m2.metric("Jakosumma", LIVE_VAIHTOTIEDOT["jakosumma"])
m3.metric("Jackpot Extra", LIVE_VAIHTOTIEDOT["jackpot"])

tab1, tab2, tab3, tab4 = st.tabs(["📌 Lähdöt & Tilastoanalyysi", "📊 V85-Kokonaisuus", "🔥 V4-Peli", "🎯 Päivän Duo"])

# ------------------------------------------------------------------------------
# TAB 1: YKSITTÄISET LÄHDÖT
# ------------------------------------------------------------------------------
with tab1:
    valittu_lahto_nro = st.radio(
        "**Valitse Lähtö:**",
        options=list(DATABANK.keys()),
        format_func=lambda x: f"Lähtö {x}",
        horizontal=True
    )
    
    lahto = DATABANK[valittu_lahto_nro]
    sim = SIM_TULOKSET[valittu_lahto_nro]
    
    st.subheader(f"📌 {lahto['nimi']} ({lahto['matka']})")
    st.info(lahto["vihje"], icon="📊")
    
    hevoset_laskettu = []
    for h in lahto["hevoset"]:
        mc = sim.get(h["numero"], 0.0)
        peli = h["peli_pct"]
        ero = round(mc - peli, 1)
        hevoset_laskettu.append({**h, "mc": mc, "ero": ero})
    
    parhaat_pelihevoset = sorted(hevoset_laskettu, key=lambda x: x["ero"], reverse=True)[:3]
    
    st.markdown("### 🔥 **Parhaat Peliarvot (Sjödén Simulaatio vs. Live Peliprosentti)**")
    p1, p2, p3 = st.columns(3)
    for idx, col in enumerate([p1, p2, p3]):
        if idx < len(parhaat_pelihevoset):
            h = parhaat_pelihevoset[idx]
            with col:
                st.success(f"**#{h['numero']} {h['nimi']}**\n\n"
                           f"• Simulaatio (Sjödén): **{h['mc']}%**\n\n"
                           f"• Live Pelattu: **{h['peli_pct']}%**\n\n"
                           f"• Etumatka: **+{h['ero']}%**")

    st.divider()
    st.markdown("### 🏇 **Lähtöruudukko**")
    
    cols = st.columns(3)
    for idx, h in enumerate(hevoset_laskettu):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"#### **{h['numero']}. {h['nimi']}**")
                st.caption(f"🏎️ Ohjastaja: {h['ohjastaja']}")
                c1, c2 = st.columns(2)
                c1.metric("Tilastosim %", f"{h['mc']}%")
                c2.metric("Live Pelattu %", f"{h['peli_pct']}%", delta=f"{h['ero']:+.1f}%")
                st.progress(int(min(h['mc'], 100)))

# ------------------------------------------------------------------------------
# TAB 2: V85 KOKONAISUUS
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("📊 V85 Pelipaketti & Sjödén-Malli (Lähdöt 5-11)")
    
    v85_data = []
    for l_id in range(5, 12):
        l_info = DATABANK[l_id]
        l_sim = SIM_TULOKSET[l_id]
        for h in l_info["hevoset"]:
            mc = l_sim[h["numero"]]
            peli = h["peli_pct"]
            v85_data.append({
                "Lähtö": f"V85-{(l_id-4)} (Lopp {l_id})",
                "Nro": h["numero"],
                "Hevonen": h["nimi"],
                "Ohjastaja": h["ohjastaja"],
                "Sjödén Sim %": mc,
                "Live Peli %": peli,
                "Peliarvo Ero %": round(mc - peli, 1)
            })
            
    df_v85 = pd.DataFrame(v85_data)
    st.dataframe(df_v85, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB 3: V4-PELI
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("🔥 V4-Peli (Lähdöt 8–11)")
    
    for v4_leg, l_id in enumerate(range(8, 12), start=1):
        st.markdown(f"#### **V4-{v4_leg} / Lopp {l_id}**")
        l_info = DATABANK[l_id]
        l_sim = SIM_TULOKSET[l_id]
        
        l_hevoset = []
        for h in l_info["hevoset"]:
            mc = l_sim[h["numero"]]
            peli = h["peli_pct"]
            l_hevoset.append({
                "Nro": h["numero"],
                "Hevonen": h["nimi"],
                "Ohjastaja": h["ohjastaja"],
                "Sim %": mc,
                "Live Peli %": peli,
                "Ero %": round(mc - peli, 1)
            })
            
        df_leg = pd.DataFrame(l_hevoset).sort_values(by="Ero %", ascending=False)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            top_pick = df_leg.iloc[0]
            st.info(f"🏆 **V4-Pelihevonen:**\n\n"
                    f"**#{top_pick['Nro']} {top_pick['Hevonen']}**\n\n"
                    f"Sim: {top_pick['Sim %']}% | Live: {top_pick['Live Peli %']}%\n\n"
                    f"Etumatka: **+{top_pick['Ero %']}%**")
        with c2:
            st.dataframe(df_leg, use_container_width=True, hide_index=True)
        st.divider()

# ------------------------------------------------------------------------------
# TAB 4: PÄIVÄN DUO
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("🎯 Päivän Duo (Lähdöt 10 & 11)")
    
    dd1_sim = SIM_TULOKSET[10]
    dd2_sim = SIM_TULOKSET[11]
    
    dd_yhdistelmat = []
    
    for h1 in DATABANK[10]["hevoset"]:
        p1_mc = dd1_sim[h1["numero"]]
        p1_peli = h1["peli_pct"]
        
        for h2 in DATABANK[11]["hevoset"]:
            p2_mc = dd2_sim[h2["numero"]]
            p2_peli = h2["peli_pct"]
            
            yhdistelma_mc = (p1_mc / 100) * (p2_mc / 100) * 100
            yhdistelma_peli = (p1_peli / 100) * (p2_peli / 100) * 100
            ero = yhdistelma_mc - yhdistelma_peli
            
            dd_yhdistelmat.append({
                "Yhdistelmä": f"DD-1: #{h1['numero']} {h1['nimi']}  x  DD-2: #{h2['numero']} {h2['nimi']}",
                "Sjödén Todennäköisyys %": round(yhdistelma_mc, 2),
                "Live Todennäköisyys %": round(yhdistelma_peli, 2),
                "Peliarvo (Ero %)": round(ero, 2)
            })
            
    df_dd = pd.DataFrame(dd_yhdistelmat).sort_values(by="Peliarvo (Ero %)", ascending=False)
    
    st.markdown("### 🥇 **DD Parhaat peliyhdistelmät**")
    st.dataframe(df_dd.head(10), use_container_width=True, hide_index=True)
