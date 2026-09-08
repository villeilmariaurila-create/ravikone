import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Hagmyren 12.9.2026", layout="wide")
st.title("🏇 Hagmyren (12.9.2026) — Lähtölistat, Vihjeet, V4 & V85 Analyysi")

st.markdown("""
**Ohje:** 
1. Liitä jokaiseen lähtöön **lähtölistat, ohjastajat ja vihjeet** ensimmäiseen tekstikenttään.
2. Liitä Veikkauksen **peliprosentit** (esim. `1. 25%`, `2. 10%` tai pelkkänä listana) alempana olevaan prosenttikenttään.
3. Ohjelma vertailee pisteitä ja peliprosentteja ja nostaa parhaat pelikohteet ja Duo-vihjeet etusivulle!
""")

race_tabs = st.tabs([f"Lähtö {i}" for i in range(1, 13)])
race_data_results = {}

for i in range(1, 13):
    with race_tabs[i-1]:
        if i <= 4:
            st.info(f"📌 **Lähtö {i} kuuluu V4-peliin (Lähdöt 1–4)**")
        else:
            st.success(f"🔥 **Lähtö {i} kuuluu V85-peliin (Lähdöt 5–12)**")
            
        col_a, col_b = st.columns([1.5, 1])
        
        with col_a:
            default_list = f"""Liitä tähän lähdön {i} hevoset ja vihjeet:
1. Hevonen Yksi - Ohjastaja A (Kommentti: Vahva vire)
2. Hevonen Kaksi - Ohjastaja B (Kommentti: Paikka ulkona)"""
            raw_text = st.text_area(f"Lähtö {i} - Listat & Vihjeet:", default_list, height=130, key=f"race_input_{i}")
            
        with col_b:
            default_pct = "1. 30%\n2. 15%\n3. 10%"
            raw_pct = st.text_area(f"Lähtö {i} - Peliprosentit (%):", default_pct, height=130, key=f"pct_input_{i}")
            
        # Parsitaan peliprosentit talteen sanakirjaan {rata: prosentti}
        pct_map = {}
        for p_line in raw_pct.strip().split("\n"):
            p_match = re.findall(r'(\d+)[^\d]+(\d+)', p_line)
            if p_match:
                r_num = int(p_match[0][0])
                r_pct = float(p_match[0][1])
                pct_map[r_num] = r_pct

        # Parsitaan hevoset
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
                    
                    r_num = int(num_part) if num_part.isdigit() else 1
                    assigned_pct = pct_map.get(r_num, 5.0) # Oletus 5% jos ei löydy
                    
                    runners.append({
                        "Rata": r_num,
                        "Hevonen": horse_name,
                        "Ohjastaja": driver,
                        "Peliprosentti %": assigned_pct,
                        "Lisätiedot / Vihje": details
                    })
                except Exception:
                    continue
        
        if runners:
            df = pd.DataFrame(runners)
            # Pisteytys listan järjestyksen mukaan
            df["Pisteet"] = [max(10, 50 - (idx * 6)) for idx in range(len(df))]
            
            # Lasketaan mallin oma arvioitu todennäköisyys
            total_pts = df["Pisteet"].sum()
            df["Mallin To %"] = (df["Pisteet"] / total_pts) * 100
            
            # Verrataan mallin todennäköisyyttä peliprosenttiin (Etu / EV-tyyppinen arvio)
            df["Etu-indeksi"] = df["Mallin To %"] - df["Peliprosentti %"]
            
            df = df.sort_values(by="Etu-indeksi", ascending=False).reset_index(drop=True)
            race_data_results[i] = df
            
            st.markdown(f"**Lähdön {i} Analyysi (Pisteet vs Peliprosentit):**")
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f'Tarkista lähdön {i} syöte.')

st.markdown("---")
st.header("🏆 Parhaat pelikohteet & Päivän Duo -suositus")

# Poimitaan parhaat pelikohteet (korkein etu-indeksi eri starteista)
all_value_bets = []
for r_num, df in race_data_results.items():
    if not df.empty:
        top_pick = df.iloc[0]
        all_value_bets.append({
            "Lähtö": r_num,
            "Hevonen": top_pick["Hevonen"],
            "Rata": top_pick["Rata"],
            "Etu": top_pick["Etu-indeksi"],
            "Peliprosentti": top_pick["Peliprosentti %"],
            "Mallin To%": top_pick["Mallin To %"]
        })

if all_value_bets:
    val_df = pd.DataFrame(all_value_bets).sort_values(by="Etu", ascending=False)
    st.subheader("💡 Parhaat arvohevokset (Mallin arvio ylittää peliprosentit selvästi)")
    st.dataframe(val_df.head(3), use_container_width=True)

st.markdown("---")

# Päivän Duo -suositus
active_races = sorted(race_data_results.keys())
if len(active_races) >= 2:
    d1, d2 = active_races[-2], active_races[-1]
    st.subheader(f"🎯 Päivän Duo -suositus (Lähdöt {d1} & {d2})")
    
    col1, col2 = st.columns(2)
    df1 = race_data_results[d1]
    df2 = race_data_results[d2]
    
    if not df1.empty and not df2.empty:
        top1 = df1.iloc[0]
        top2 = df2.iloc[0]
        
        with col1:
            st.info(f"**Duo Kohde 1 (Lähtö {d1})**\n\n🐎 **{top1['Hevonen']}** (Rata {top1['Rata']})\n\nPeliprosentti: {top1['Peliprosentti %']}% | Mallin arvio: {top1['Mallin To %']:.1f}%\n\n*Vihje:* {top1['Lisätiedot / Vihje']}")
        with col2:
            st.info(f"**Duo Kohde 2 (Lähtö {d2})**\n\n🐎 **{top2['Hevonen']}** (Rata {top2['Rata']})\n\nPeliprosentti: {top2['Peliprosentti %']}% | Mallin arvio: {top2['Mallin To %']:.1f}%\n\n*Vihje:* {top2['Lisätiedot / Vihje']}")
else:
    st.warning("Syötä tietoja vähintään kahteen viimeiseen lähtöön Duo-suositusta varten.")
