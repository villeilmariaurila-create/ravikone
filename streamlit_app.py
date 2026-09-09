import random
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. HAGMYREN 12.9.2026 V85-DATAN ALUSTUS PDF-TIEDOSTON MUKAAN
# ==============================================================================

DATABANK = {
    5: {
        "nimi": "Lopp 5 - STL Klass I (V85-1, V5-2)",
        "matka": "2140m Autostart",
        "hevoset": [
            {"numero": 1, "nimi": "T.Wall's Notorius", "ohjastaja": "Jomar Blekkan", "peli_pct": 12, "paino": 1.1},
            {"numero": 2, "nimi": "Hip To Be Square", "ohjastaja": "Per Lennartsson", "peli_pct": 32, "paino": 1.45},
            {"numero": 3, "nimi": "Sign Of Times", "ohjastaja": "Tomas Pettersson", "peli_pct": 8, "paino": 0.95},
            {"numero": 4, "nimi": "Geisha Road Grif", "ohjastaja": "Jorma Kontio", "peli_pct": 10, "paino": 1.05},
            {"numero": 5, "nimi": "Macho Cabrio B.B.", "ohjastaja": "Peter G Norman", "peli_pct": 11, "paino": 1.10},
            {"numero": 6, "nimi": "Henessi Kiev", "ohjastaja": "Oskar J Andersson", "peli_pct": 6, "paino": 0.85},
            {"numero": 7, "nimi": "Takter", "ohjastaja": "Hans G Eriksson", "peli_pct": 3, "paino": 0.70},
            {"numero": 8, "nimi": "Herkules A'lir", "ohjastaja": "Rikard N Skoglund", "peli_pct": 14, "paino": 1.25},
            {"numero": 9, "nimi": "Night Hawk", "ohjastaja": "Mats E Djuse", "peli_pct": 4, "paino": 0.80},
            {"numero": 10, "nimi": "Huchuy Qosqo", "ohjastaja": "Anders Eriksson", "peli_pct": 2, "paino": 0.60},
            {"numero": 11, "nimi": "De Är Hon", "ohjastaja": "Ulf Ohlsson", "peli_pct": 1, "paino": 0.50},
            {"numero": 12, "nimi": "Sandsjöns Cantona", "ohjastaja": "Claes Sjöström", "peli_pct": 7, "paino": 0.90},
        ]
    },
    6: {
        "nimi": "Lopp 6 - STL Kallblodsdivisionen (V85-2)",
        "matka": "2140m Voltstart",
        "hevoset": [
            {"numero": 1, "nimi": "Fosshaug Frasse", "ohjastaja": "Michaela B Fransson", "peli_pct": 2, "paino": 0.5},
            {"numero": 2, "nimi": "Sangviks Lynet", "ohjastaja": "Ulf Ohlsson", "peli_pct": 10, "paino": 1.0},
            {"numero": 3, "nimi": "Andarnas Patron", "ohjastaja": "Rikard N Skoglund", "peli_pct": 5, "paino": 0.8},
            {"numero": 4, "nimi": "Silke Sjarmör", "ohjastaja": "Carl Johan Jepson", "peli_pct": 15, "paino": 1.2},
            {"numero": 5, "nimi": "Ellbert", "ohjastaja": "Mats E Djuse", "peli_pct": 18, "paino": 1.3},
            {"numero": 6, "nimi": "Guli Hektor", "ohjastaja": "Örjan Kihlström", "peli_pct": 4, "paino": 0.7},
            {"numero": 7, "nimi": "Tåga Ryker", "ohjastaja": "Ingvar Nyberg", "peli_pct": 2, "paino": 0.5},
            {"numero": 8, "nimi": "Teknologen", "ohjastaja": "Robert Skoglund", "peli_pct": 22, "paino": 1.4},
            {"numero": 9, "nimi": "Ava Modde", "ohjastaja": "Henrik Svensson", "peli_pct": 3, "paino": 0.6},
            {"numero": 10, "nimi": "Re Alkapital", "ohjastaja": "Joakim Eskilsson", "peli_pct": 4, "paino": 0.7},
            {"numero": 11, "nimi": "Mira Kiro", "ohjastaja": "Jorma Kontio", "peli_pct": 6, "paino": 0.85},
            {"numero": 12, "nimi": "Ersa Frej", "ohjastaja": "Nathalie Blom", "peli_pct": 1, "paino": 0.4},
            {"numero": 13, "nimi": "Klack Vidar", "ohjastaja": "Magnus A Djuse", "peli_pct": 3, "paino": 0.6},
            {"numero": 14, "nimi": "Blixen", "ohjastaja": "Jan-Olof Johansson", "peli_pct": 2, "paino": 0.5},
            {"numero": 15, "nimi": "Guli Em", "ohjastaja": "Marcus Lilius", "peli_pct": 3, "paino": 0.6},
        ]
    },
    7: {
        "nimi": "Lopp 7 - STL Gulddivisionen (V85-3)",
        "matka": "1640m Autostart",
        "hevoset": [
            {"numero": 1, "nimi": "Before Takeoff", "ohjastaja": "Örjan Kihlström", "peli_pct": 22, "paino": 1.25},
            {"numero": 2, "nimi": "Santos De Castella", "ohjastaja": "Marcus Lilius", "peli_pct": 5, "paino": 0.70},
            {"numero": 3, "nimi": "Romulus Tooma", "ohjastaja": "Peter G Norman", "peli_pct": 2, "paino": 0.50},
            {"numero": 4, "nimi": "Mizai", "ohjastaja": "Per Lennartsson", "peli_pct": 12, "paino": 1.00},
            {"numero": 5, "nimi": "Lando Mearas", "ohjastaja": "Magnus A Djuse", "peli_pct": 28, "paino": 1.35},
            {"numero": 6, "nimi": "Mellby Joker", "ohjastaja": "Mats E Djuse", "peli_pct": 21, "paino": 1.20},
            {"numero": 7, "nimi": "Jerka Sting", "ohjastaja": "Claes Sjöström", "peli_pct": 10, "paino": 0.95},
        ]
    },
    8: {
        "nimi": "Lopp 8 - STL Dubbelklasslopp (V85-4, V4-1, V5-1)",
        "matka": "2640m Autostart",
        "hevoset": [
            {"numero": 1, "nimi": "Napoleon Sisu", "ohjastaja": "Oskar J Andersson", "peli_pct": 5, "paino": 0.8},
            {"numero": 2, "nimi": "Ies Ingusmemory", "ohjastaja": "Magnus A Djuse", "peli_pct": 8, "paino": 0.95},
            {"numero": 3, "nimi": "Ytowns Ulrik", "ohjastaja": "Jorma Kontio", "peli_pct": 12, "paino": 1.1},
            {"numero": 4, "nimi": "Classique Launcher", "ohjastaja": "Olle Alsén", "peli_pct": 2, "paino": 0.5},
            {"numero": 5, "nimi": "Umpteen", "ohjastaja": "Nathalie Blom", "peli_pct": 15, "paino": 1.2},
            {"numero": 6, "nimi": "Holiday Island", "ohjastaja": "Anders Eriksson", "peli_pct": 20, "paino": 1.35},
            {"numero": 7, "nimi": "Sacrebleu", "ohjastaja": "Rikard N Skoglund", "peli_pct": 6, "paino": 0.85},
            {"numero": 8, "nimi": "Uno", "ohjastaja": "Mats E Djuse", "peli_pct": 7, "paino": 0.9},
            {"numero": 9, "nimi": "Whiskey Majo", "ohjastaja": "Marcus Lilius", "peli_pct": 4, "paino": 0.75},
            {"numero": 10, "nimi": "Timotejs Gamble", "ohjastaja": "Carl Johan Jepson", "peli_pct": 9, "paino": 1.0},
            {"numero": 11, "nimi": "Bear Victor", "ohjastaja": "Ulf Ohlsson", "peli_pct": 8, "paino": 0.95},
            {"numero": 12, "nimi": "Lion Sisu", "ohjastaja": "Örjan Kihlström", "peli_pct": 14, "paino": 1.15},
            {"numero": 13, "nimi": "Jaguar Ima", "ohjastaja": "Fredrik Plassen", "peli_pct": 3, "paino": 0.6},
            {"numero": 14, "nimi": "Flat Tire Grue", "ohjastaja": "Oskar Florhed", "peli_pct": 1, "paino": 0.4},
            {"numero": 15, "nimi": "Vidar Burge", "ohjastaja": "Claes Sjöström", "peli_pct": 2, "paino": 0.5},
        ]
    },
    9: {
        "nimi": "Lopp 9 - STL Kallblodsdivisionen Tammer Pokal (V85-5, V4-2)",
        "matka": "2140m Autostart",
        "hevoset": [
            {"numero": 1, "nimi": "Majblomster", "ohjastaja": "Mats E Djuse", "peli_pct": 48, "paino": 1.8},
            {"numero": 2, "nimi": "Prinsesse Ness Tjo", "ohjastaja": "Örjan Kihlström", "peli_pct": 16, "paino": 1.2},
            {"numero": 3, "nimi": "Tekno Tana", "ohjastaja": "Robert Skoglund", "peli_pct": 10, "paino": 1.0},
            {"numero": 4, "nimi": "Hulte Alva", "ohjastaja": "Linda S Hedström", "peli_pct": 7, "paino": 0.9},
            {"numero": 5, "nimi": "Guli Stina", "ohjastaja": "Ulf Ohlsson", "peli_pct": 3, "paino": 0.6},
            {"numero": 6, "nimi": "Hög Decibel", "ohjastaja": "Stig Jarle Röste", "peli_pct": 2, "paino": 0.5},
            {"numero": 7, "nimi": "Hulte Annika", "ohjastaja": "Magnus A Djuse", "peli_pct": 5, "paino": 0.8},
            {"numero": 8, "nimi": "Jonases Ninja", "ohjastaja": "Jan-Olov Åberg", "peli_pct": 3, "paino": 0.6},
            {"numero": 9, "nimi": "Eldida", "ohjastaja": "Ida Eriksson", "peli_pct": 1, "paino": 0.4},
            {"numero": 10, "nimi": "Rötungen", "ohjastaja": "Micael Melander", "peli_pct": 1, "paino": 0.4},
            {"numero": 11, "nimi": "Saga Kiro", "ohjastaja": "Per Lennartsson", "peli_pct": 2, "paino": 0.5},
            {"numero": 12, "nimi": "Ethel", "ohjastaja": "Henrik Svensson", "peli_pct": 2, "paino": 0.5},
        ]
    },
    10: {
        "nimi": "Lopp 10 - STL Stodivisionen (V85-6, V4-3, DD-1)",
        "matka": "2640m Voltstart",
        "hevoset": [
            {"numero": 1, "nimi": "Sessan Of Man", "ohjastaja": "Henrik Svensson", "peli_pct": 2, "paino": 0.5},
            {"numero": 2, "nimi": "Adora Liss", "ohjastaja": "Fredrik Plassen", "peli_pct": 3, "paino": 0.6},
            {"numero": 3, "nimi": "Pure Jouline", "ohjastaja": "Linus Lönn", "peli_pct": 8, "paino": 0.95},
            {"numero": 4, "nimi": "Grove's Maple Poof", "ohjastaja": "Ulf Ohlsson", "peli_pct": 12, "paino": 1.1},
            {"numero": 5, "nimi": "Bohemian Maid", "ohjastaja": "Magnus A Djuse", "peli_pct": 18, "paino": 1.3},
            {"numero": 6, "nimi": "Kopparmärra", "ohjastaja": "Nathalie Blom", "peli_pct": 4, "paino": 0.7},
            {"numero": 7, "nimi": "C'est Ma Course", "ohjastaja": "Lucas H Vikström", "peli_pct": 5, "paino": 0.8},
            {"numero": 8, "nimi": "Brionne", "ohjastaja": "Rikard N Skoglund", "peli_pct": 14, "paino": 1.2},
            {"numero": 9, "nimi": "Melina Havelock", "ohjastaja": "Carl Johan Jepson", "peli_pct": 6, "paino": 0.85},
            {"numero": 10, "nimi": "Ajlexes Gourmand", "ohjastaja": "Tomas Pettersson", "peli_pct": 10, "paino": 1.05},
            {"numero": 11, "nimi": "Global Empress", "ohjastaja": "Marcus Lilius", "peli_pct": 5, "paino": 0.8},
            {"numero": 12, "nimi": "Danceinthedark F.", "ohjastaja": "Katrin K Frick", "peli_pct": 2, "paino": 0.5},
            {"numero": 13, "nimi": "Rupie", "ohjastaja": "Mats E Djuse", "peli_pct": 7, "paino": 0.9},
            {"numero": 14, "nimi": "Frida S.H.", "ohjastaja": "Örjan Kihlström", "peli_pct": 1, "paino": 0.4},
            {"numero": 15, "nimi": "Kueen Simoni", "ohjastaja": "Claes Sjöström", "peli_pct": 3, "paino": 0.6},
        ]
    },
    11: {
        "nimi": "Lopp 11 - STL Bronsdivisionen (V85-7, V4-4, DD-2)",
        "matka": "2140m Autostart",
        "hevoset": [
            {"numero": 1, "nimi": "Bruce Braylon", "ohjastaja": "Per Lennartsson", "peli_pct": 16, "paino": 1.25},
            {"numero": 2, "nimi": "Pineapple", "ohjastaja": "Carl Johan Jepson", "peli_pct": 14, "paino": 1.15},
            {"numero": 3, "nimi": "Graces Bird", "ohjastaja": "Fredrik Plassen", "peli_pct": 6, "paino": 0.85},
            {"numero": 4, "nimi": "Mellby Mowgli", "ohjastaja": "Örjan Kihlström", "peli_pct": 22, "paino": 1.35},
            {"numero": 5, "nimi": "Ebbot Rice", "ohjastaja": "Linus Lönn", "peli_pct": 4, "paino": 0.70},
            {"numero": 6, "nimi": "Jaguar Godiva", "ohjastaja": "Ulf Ohlsson", "peli_pct": 10, "paino": 1.05},
            {"numero": 7, "nimi": "Don E.Star", "ohjastaja": "Oskar J Andersson", "peli_pct": 2, "paino": 0.50},
            {"numero": 8, "nimi": "Lucky Silver", "ohjastaja": "Mats E Djuse", "peli_pct": 12, "paino": 1.10},
            {"numero": 9, "nimi": "Elvis T.C.B.", "ohjastaja": "Marcus Lilius", "peli_pct": 5, "paino": 0.80},
            {"numero": 10, "nimi": "Gosa Gosing", "ohjastaja": "Rikard N Skoglund", "peli_pct": 5, "paino": 0.80},
            {"numero": 11, "nimi": "Punchboard", "ohjastaja": "Magnus A Djuse", "peli_pct": 3, "paino": 0.60},
            {"numero": 12, "nimi": "Slivovitz Lover", "ohjastaja": "Claes Sjöström", "peli_pct": 1, "paino": 0.40},
        ]
    }
}

# ==============================================================================
# 2. MONTE CARLO -SIMULAATTORI
# ==============================================================================

def simuloi_lahto(hevoset: list, kierrokset: int = 10000) -> dict:
    numerot = [h["numero"] for h in hevoset]
    painot = [h["paino"] for h in hevoset]
    
    voitot = {num: 0 for num in numerot}
    for _ in range(kierrokset):
        voittaja = random.choices(numerot, weights=painot, k=1)[0]
        voitot[voittaja] += 1
        
    return {num: round((maara / kierrokset) * 100, 1) for num, maara in voitot.items()}

# Lasketaan simulaatio kaikille lähdöille
SIM_TULOKSET = {}
for lahto_id, lahto_data in DATABANK.items():
    SIM_TULOKSET[lahto_id] = simuloi_lahto(lahto_data["hevoset"])

# ==============================================================================
# 3. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.set_page_config(page_title="Hagmyren 12.9.2026 Ravisimulaattori", layout="wide")

st.title("🏇 Hagmyren 12.9.2026 - Mallinnus & Pelianalyysi")
st.caption("Aitojen lähtölistojen Monte Carlo -simulaatio vs. Markkinan peliprosentit")

tab1, tab2, tab3, tab4 = st.tabs(["📌 Lähtökohtaiset Ruudukot", "📊 V85-Kokonaisuus", "🔥 V4-Peli", "🎯 Päivän Duo"])

# ------------------------------------------------------------------------------
# TAB 1: YKSITTÄISET LÄHDÖT (5-11)
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
    
    # Parhaat pelihevoset (Suurin ERO = Monte Carlo % - Peli %)
    hevoset_laskettu = []
    for h in lahto["hevoset"]:
        mc = sim.get(h["numero"], 0.0)
        peli = h["peli_pct"]
        ero = round(mc - peli, 1)
        hevoset_laskettu.append({**h, "mc": mc, "ero": ero})
    
    parhaat_pelihevoset = sorted(hevoset_laskettu, key=lambda x: x["ero"], reverse=True)[:3]
    
    # Nostetaan esiin parhaat pelihevoset
    st.markdown("### 🔥 **Lähdön Parhaat Pelihevoset (Overvalue)**")
    p1, p2, p3 = st.columns(3)
    for idx, col in enumerate([p1, p2, p3]):
        if idx < len(parhaat_pelihevoset):
            h = parhaat_pelihevoset[idx]
            with col:
                st.success(f"**#{h['numero']} {h['nimi']}**\n\n"
                           f"• Simulaatio: **{h['mc']}%**\n\n"
                           f"• Pelattu: **{h['peli_pct']}%**\n\n"
                           f"• Peliarvo (Ero): **+{h['ero']}%**")

    st.divider()
    st.markdown("### 🏇 **Hevoset Ruudukossa**")
    
    # Näytetään hevoset 3 sarakkeen ruudukossa
    cols = st.columns(3)
    for idx, h in enumerate(hevoset_laskettu):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"#### **{h['numero']}. {h['nimi']}**")
                st.caption(f"🏎️ Ohjastaja: {h['ohjastaja']}")
                c1, c2 = st.columns(2)
                c1.metric("Simulaatio", f"{h['mc']}%")
                c2.metric("Markkina", f"{h['peli_pct']}%", delta=f"{h['ero']:+.1f}%")
                st.progress(int(min(h['mc'], 100)))

# ------------------------------------------------------------------------------
# TAB 2: V85-KOKONAISUUS
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("📊 V85 Pelipaketti & Vertailu (Lähdöt 5-11)")
    
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
                "Simulaatio %": mc,
                "Peliprosentti %": peli,
                "Ero %": round(mc - peli, 1)
            })
            
    df_v85 = pd.DataFrame(v85_data)
    
    # Puhdas taulukkonäkymä ilman matplotlib-muotoilua
    st.dataframe(
        df_v85,
        use_container_width=True,
        hide_index=True
    )

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
                "Peli %": peli,
                "Ero %": round(mc - peli, 1)
            })
            
        df_leg = pd.DataFrame(l_hevoset).sort_values(by="Ero %", ascending=False)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            top_pick = df_leg.iloc[0]
            st.info(f"🏆 **Paras V4-Pelihevonen:**\n\n"
                    f"**#{top_pick['Nro']} {top_pick['Hevonen']}**\n\n"
                    f"Sim: {top_pick['Sim %']}% | Peli: {top_pick['Peli %']}%\n\n"
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
                "Simulaatio Todennäköisyys %": round(yhdistelma_mc, 2),
                "Pelattu Todennäköisyys %": round(yhdistelma_peli, 2),
                "Peliarvo (Ero %)": round(ero, 2)
            })
            
    df_dd = pd.DataFrame(dd_yhdistelmat).sort_values(by="Peliarvo (Ero %)", ascending=False)
    
    st.markdown("### 🥇 **Päivän Duon Parhaat Peliyhdistelmät**")
    # Puhdas taulukkonäkymä ilman matplotlib-muotoilua
    st.dataframe(
        df_dd.head(10),
        use_container_width=True,
        hide_index=True
    )
