import streamlit as st
import pandas as pd

st.set_page_config(page_title="Köysikujalla — Travronden Tulkki", layout="wide")
st.title("🏇 Köysikujalla — Travronden Listat & Vihjeet")

st.markdown("""
**Ohje:** Koska Travronden vaatii kirjautumisen suojatulle sivustolleen, helpoin ja varmin tapa on kopioida haluamasi lähdön tiedot tai vihjeteksti suoraan sivustolta ja liittää se tähän kenttään. Ohjelma lukee tiedot automaattisesti!
""")

# Malliteksti havainnollistamaan muotoa
default_data = """Lähtö 1:
1. Hail Mary - Erik Adielsson (Vihje: Todella vahva suosikki, luottohevonen)
2. Don Fanucci Zet - Magnus A Djuse (Vihje: Haastaa tosissaan)
3. Brother Bill - Jorma Kontio (Vihje: Ulkoradalta yllätysvalmis)
4. Missle Hill - Mats E Djuse (Vihje: Tasainen suorittaja)"""

raw_text = st.text_area("Liitä Travrondenin starttilista / vihjeet tähän:", default_data, height=200)

if st.button("Jäsennä tiedot, laske pisteet ja tee Duo-suositus"):
    lines = raw_text.strip().split("\n")
    current_race = 1
    races_dict = {}
    
    runners = []
    for line in lines:
        if "Lähtö" in line:
            if runners:
                races_dict[current_race] = runners
                runners = []
            # Poimitaan lähdön numero jos mahdollista
            import re
            found_num = re.findall(r'\d+', line)
            if found_num:
                current_race = int(found_num[0])
        elif "." in line and "-" in line:
            try:
                parts = line.split("-")
                left = parts[0].strip()
                right = parts[1].strip()
                
                num_part = left.split(".")[0].strip()
                horse_name = left.split(".")[1].strip()
                
                driver = right.split("(")[0].strip()
                hint = right.split("(")[1].replace(")", "").strip() if "(" in right else "Ei erillistä vihjettä"
                
                runners.append({
                    "Rata": int(num_part),
                    "Hevonen": horse_name,
                    "Ohjastaja": driver,
                    "Vihje / Kommentti": hint
                })
            except Exception:
                continue
    if runners:
        races_dict[current_race] = runners

    if races_dict:
        st.success("Tiedot jäsennetty onnistuneesti!")
        
        # Näytetään jokainen lähtö taulukoina
        all_dfs = {}
        for r_num, r_list in races_dict.items():
            st.subheader(f"Lähtö {r_num}")
            df = pd.DataFrame(r_list)
            # Tehdään yksinkertainen pisteytys listan järjestyksen mukaan
            df["Pisteet"] = [max(10, 50 - (i * 8)) for i in range(len(df))]
            df = df.sort_values(by="Pisteet", ascending=False).reset_index(drop=True)
            all_dfs[r_num] = df
            
            st.dataframe(df, use_container_width=True)
            
        # Päivän Duo -suositus kahden viimeisen tai kahden ensimmäisen lähdön perusteella
        race_keys = sorted(all_dfs.keys())
        if len(race_keys) >= 2:
            d1, d2 = race_keys[-2], race_keys[-1]
            st.markdown("---")
            st.subheader("🎯 Päivän Duo -suositus (Travronden-datan pohjalta)")
            
            col1, col2 = st.columns(2)
            top1 = all_dfs[d1].iloc[0]
            top2 = all_dfs[d2].iloc[0]
            
            with col1:
                st.info(f"**Duo Kohde 1 (Lähtö {d1})**\n\n🐎 **{top1['Hevonen']}** (Rata {top1['Rata']})\n\nOhjastaja: {top1['Ohjastaja']}\n\n*Kommentti:* {top1['Vihje / Kommentti']}")
            with col2:
                st.info(f"**Duo Kohde 2 (Lähtö {d2})**\n\n🐎 **{top2['Hevonen']}** (Rata {top2['Rata']})\n\nOhjastaja: {top2['Ohjastaja']}\n\n*Kommentti:* {top2['Vihje / Kommentti']}")
    else:
                st.warning("Tarkista syötteen muoto. Varmista että riveissä on muoto: `1. Hevonen - Ohjastaja (Vihje: ...)`")
