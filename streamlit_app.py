import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Köysikujalla — 13 Lähdön Jäsentäjä", layout="wide")
st.title("🏇 Köysikujalla — 13 Lähtöä, Vihjeet & Peliprosentit")

st.markdown("""
**Ohje:** Liitä jokaiseen lähtöön omat tietosi (lähtölistat, vihjeet, kommentit ja peliprosentit/kertoimet). 
Ohjelma lukee tiedot, laskee pisteytyksen automaattisesti ja näyttää ne taulukoina sekä tekee Duo-suosituksen.
""")

# Luodaan välilehdet tai expanderit 13 lähdölle
race_tabs = st.tabs([f"Lähtö {i}" for i in range(1, 14)])

race_data_results = {}

for i in range(1, 14):
    with race_tabs[i-1]:
        st.subheader(f"Lähtö {i} - Tiedot")
        
        default_text = f"""Esimerkki muoto (muokkaa tai korvaa omillasi):
1. Hevonen Yksi - Ohjastaja A (Prosentti: 25%, Kerroin: 3.50, Kommentti: Loistavassa kunnossa)
2. Hevonen Kaksi - Ohjastaja B (Prosentti: 15%, Kerroin: 6.00, Kommentti: Ulkorata miinusta)"""
        
        raw_text = st.text_area(f"Liitä lähdön {i} tiedot tähän:", default_text, height=150, key=f"race_input_{i}")
        
        # Jäsennetään teksti
        lines = raw_text.strip().split("\n")
        runners = []
        for line in lines:
            if "." in line and "-" in line:
                try:
                    parts = line.split("-")
                    left = parts[0].strip()
                    right = parts[1].strip()
                    
                    num_part = left.split(".")[0].strip()
                    horse_name = left.split(".")[1].strip()
                    
                    driver = right.split("(")[0].strip()
                    details = right.split("(")[1].replace(")", "").strip() if "(" in right else "Ei lisätietoja"
                    
                    # Yritetään poimia prosentti tai kerroin tekstistä, jos sellainen on annettu
                    pct_match = re.search(r'(\d+)\s*%', details)
                    odds_match = re.search(r'([\d\.]+)', details)
                    
                    runners.append({
                        "Rata": int(num_part) if num_part.isdigit() else 1,
                        "Hevonen": horse_name,
                        "Ohjastaja": driver,
                        "Lisätiedot / Vihje": details
                    })
                except Exception:
                    continue
        
        if runners:
            df = pd.DataFrame(runners)
            # Yksinkertainen automaattinen pisteytys listan järjestyksen mukaan
            df["Pisteet"] = [max(10, 50 - (idx * 6)) for idx in range(len(df))]
            df = df.sort_values(by="Pisteet", ascending=False).reset_index(drop=True)
            race_data_results[i] = df
            
            st.markdown(f"**Lähdön {i} järjestetyt arviot:**")
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f'Ei kelvollisia rivejä lähdölle {i}. Käytä muotoa: `1. Nimi - Ohjastaja (Kommentti, Prosentti jne.)`')

st.markdown("---")
st.header("🎯 Päivän Duo -suositus (Lähdöt 12 & 13 tai viimeiset aktiiviset)")

# Etsitään lähdöt joissa on dataa
active_races = sorted(race_data_results.keys())

if len(active_races) >= 2:
    d1, d2 = active_races[-2], active_races[-1]
    
    col1, col2 = st.columns(2)
    df1 = race_data_results[d1]
    df2 = race_data_results[d2]
    
    if not df1.empty and not df2.empty:
        top1 = df1.iloc[0]
        top2 = df2.iloc[0]
        
        with col1:
            st.info(f"**Duo Kohde 1 (Lähtö {d1})**\n\n🐎 **{top1['Hevonen']}** (Rata {top1['Rata']})\n\nOhjastaja: {top1['Ohjastaja']}\n\n*Tiedot:* {top1['Lisätiedot / Vihje']}")
        with col2:
            st.info(f"**Duo Kohde 2 (Lähtö {d2})**\n\n🐎 **{top2['Hevonen']}** (Rata {top2['Rata']})\n\nOhjastaja: {top2['Ohjastaja']}\n\n*Tiedot:* {top2['Lisätiedot / Vihje']}")
else:
    st.warning("Syötä tietoja vähintään kahteen eri lähtöön, jotta Päivän Duo -suositus voidaan muodostaa.")
