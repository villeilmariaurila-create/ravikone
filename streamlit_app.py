import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Hagmyren 12.9.2026", layout="wide")
st.title("🏇 Hagmyren (12.9.2026) — V4 (Lähtö 1-4) & V85 (Lähtö 5-12) Analyysi")

st.markdown("""
**Ohje:** 
1. Syötä jokaiseen lähtöön **hevoset ja vihjeet** ensimmäiseen kenttään.
2. Syötä Veikkauksen **peliprosentit (%)** omiin kenttiinsä.
3. Ohjelma näyttää V4- ja V85-pelien omat analyysitaulukot, vertaa mallin arvioita peliprosentteihin ja nostaa parhaat arvohevokset ja Duo-suosituksen esille!
""")

race_tabs = st.tabs([f"Lähtö {i}" for i in range(1, 13)])
race_data_results = {}

for i in range(1, 13):
    with race_tabs[i-1]:
        if i <= 4:
            st.info(f"📌 **Lähtö {i} — V4-peli (Kohteet 1–4)**")
        else:
            st.success(f"🔥 **Lähtö {i} — V85-peli (Kohteet {i-4}/8)**")
            
        col_a, col_b = st.columns([1.5, 1])
        
        with col_a:
            default_list = f"""1. Hevonen Yksi - Ohjastaja A (Kommentti: Vahva vire)
2. Hevonen Kaksi - Ohjastaja B (Kommentti: Paikka ulkona)"""
            raw_text = st.text_area(f"Lähtö {i} - Listat & Vihjeet:", default_list, height=130, key=f"race_input_{i}")
            
        with col_b:
            default_pct = "1. 30%\n2. 15%\n3. 10%"
            raw_pct = st.text_area(f"Lähtö {i} - Veikkaus Peliprosentit (%):", default_pct, height=130, key=f"pct_input_{i}")
            
        # Parsitaan peliprosentit
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
                    assigned_pct = pct_map.get(r_num, 5.0)
                    
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
            df["Pisteet"] = [max(10, 50 - (idx * 6)) for idx in range(len(df))]
            
            total_pts = df["Pisteet"].sum()
            df["Mallin To %"] = (df["Pisteet"] / total_pts) * 100
            df["Etu-indeksi"] = df["Mallin To %"] - df["Peliprosentti %"]
            
            df = df.sort_values(by="Etu-indeksi", ascending=False).reset_index(drop=True)
            race_data_results[i] = df
            
            st.markdown(f"**Lähdön {i} Vertailutaulukko (Malli vs Markkina):**")
            st.dataframe(df, use_container_width=True)
        else:
            st.info(f'Tarkista lähdön {i} syöte.')

st.markdown("---")
st.header("📊 V4 & V85 Yhteenveto & Parhaat Arvokohteet")

v4_results = {k: v for k, v in race_data_results.items() if k <= 4}
v85_results = {k: v for k, v in race_data_results.items() if k > 4}

col_v4, col_v85 = st.columns(2)

with col_v4:
    st.subheader("📌 V4 Peli-ikkuna (Lähdöt 1–4)")
    v4_top_bets = []
    for r_num, df in v4_results.items():
        if not df.empty and "Etu-indeksi" in df.columns:
            top = df.iloc[0]
            v4_top_bets.append({"Lähtö": r_num, "Hevonen": top["Hevonen"], "Etu%": top["Etu-indeksi"]})
    if v4_top_bets:
        st.dataframe(pd.DataFrame(v4_top_bets), use_container_width=True)
    else:
        st.info("Ei vielä dataa V4-lähdöille.")

with col_v85:
    st.subheader("🔥 V85 Peli-ikkuna (Lähdöt 5–12)")
    v85_top_bets = []
    for r_num, df in v85_results.items():
        if not df.empty and "Etu-indeksi" in df.columns:
            top = df.iloc[0]
            v85_top_bets.append({"Lähtö": r_num, "Hevonen": top["Hevonen"], "Etu%": top["Etu-indeksi"]})
    if v85_top_bets:
        st.dataframe(pd.DataFrame(v85_top_bets), use_container_width=True)
    else:
        st.info("Ei vielä dataa V85-lähdöille.")

st.markdown("---")

# Päivän Duo -suositus
active_races = sorted(race_data_results.keys())
if len(active_races) >= 2:
    d1, d2 = active_races[-2], active_races[-1]
    st.subheader(f"🎯 Päivän Duo -suositus (Lähdöt {d1} & {d2})")
    
    col1, col2 = st.columns(2)
    df1 = race_data_results.get(d1, pd.DataFrame())
    df2 = race_data_results.get(d2, pd.DataFrame())
    
    if not df1.empty and not df2.empty:
        top1 = df1.iloc[0]
        top2 = df2.iloc[0]
        
        with col1:
            st.info(f"**Duo Kohde 1 (Lähtö {d1})**\n\n🐎 **{top1['Hevonen']}** (Rata {top1['Rata']})\n\nPeliprosentti: {top1['Peliprosentti %']}% | Mallin arvio: {top1['Mallin To %']:.1f}%\n\n*Vihje:* {top1['Lisätiedot / Vihje']}")
        with col2:
            st.info(f"**Duo Kohde 2 (Lähtö {d2})**\n\n🐎 **{top2['Hevonen']}** (Rata {top2['Rata']})\n\nPeliprosentti: {top2['Peliprosentti %']}% | Mallin arvio: {top2['Mallin To %']:.1f}%\n\n*Vihje:* {top2['Lisätiedot / Vihje']}")
else:
    st.warning("Syötä tietoja vähintään kahteen viimeiseen lähtöön Duo-suositusta varten.")
