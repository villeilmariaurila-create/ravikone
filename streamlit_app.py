import datetime
import requests
import numpy as np
import pandas as pd
import streamlit as st

# --- SIVUN ASETUKSET ---
st.set_page_config(page_title="Stella", layout="wide", initial_sidebar_state="expanded")

# --- STELLA: MODERNISORITU & HYMYILEVÄ VISUAALINEN LOGO ---
st.markdown("""
    <style>
    .stella-logo-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 20px;
    }
    .stella-logo-icon {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        color: white;
        font-size: 32px;
        width: 58px;
        height: 58px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
    }
    .stella-logo-text {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -1px;
        line-height: 1;
    }
    .stella-logo-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.65rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    </style>
""", unsafe_allow_html=True)

# STELLAN LOGO
st.markdown("""
    <div class="stella-logo-container">
        <div class="stella-logo-icon">😊</div>
        <div>
            <div class="stella-logo-text">STELLA</div>
            <div class="stella-logo-subtitle">Realtime Quant Racing Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIVUPALKKI: VALIKKO ---
st.sidebar.markdown("### 📅 VALITSE RAVIPÄIVÄ & RATA")

selected_date = st.sidebar.date_input("Päivämäärä", datetime.date.today())

tracks_map = {
    "Umåker (SE)": "umåker",
    "Jägersro (SE)": "jägersro",
    "Solvalla (SE)": "solvalla",
    "Åby (SE)": "åby",
    "Bjerke (NO)": "bjerke",
    "Boden (SE)": "boden",
    "Bergsåker (SE)": "bergsåker",
    "Eskilstuna (SE)": "eskilstuna",
    "Vermo (FI)": "vermo",
    "Teivo (FI)": "teivo"
}

selected_track_name = st.sidebar.selectbox("Ravirata", list(tracks_map.keys()))
selected_track_code = tracks_map[selected_track_name]

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ SIMULAATION SÄÄTIMET")

spets_bias = st.sidebar.slider("Keulapainotus (Spets-kerroin)", 1.00, 1.30, 1.15, step=0.01)
n_simulations = st.sidebar.slider("Monte Carlo -kierrokset", 10000, 100000, 50000, step=10000)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 DATA-INTEGRAATIOT")
use_unibet = st.sidebar.toggle("Unibet-kertoimet", value=True)
use_travronden = st.sidebar.toggle("Travronden-kommentit", value=True)

# Google-haku integroituna
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 GOOGLE-LÄHTÖHAKU")
search_term = f"{selected_track_name} {selected_date.strftime('%d.%m.%Y')} vihjeet"
google_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
st.sidebar.markdown(f"🔗 [Google-haku: **{selected_track_name}**]({google_url})")

# --- SUORA REAALIAIKAINEN ATG API HAKURI ---
@st.cache_data(ttl=60) # Paivittyy minuutin välein tuoreilla prosenteilla
def fetch_real_atg_data(date_obj, track_keyword):
    date_str = date_obj.strftime("%Y-%m-%d")
    calendar_url = f"https://www.atg.se/services/racinginfo/v1/api/calendar/day/{date_str}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    rows = []
    try:
        res = requests.get(calendar_url, headers=headers, timeout=10)
        if res.status_code == 200:
            cal_data = res.json()
            
            # Etsitään oikea rata kalenterista
            target_track_id = None
            for track in cal_data.get('tracks', []):
                t_name = track.get('name', '').lower()
                if track_keyword in t_name:
                    target_track_id = track.get('id')
                    races = track.get('races', [])
                    
                    for race in races:
                        race_id = race.get('id')
                        race_no = race.get('number', 1)
                        kohde_str = f"Lähtö {race_no}"
                        
                        # Haetaan lähdön yksityiskohtaiset tiedot & hevoset
                        race_url = f"https://www.atg.se/services/racinginfo/v1/api/races/{race_id}"
                        r_res = requests.get(race_url, headers=headers, timeout=5)
                        
                        if r_res.status_code == 200:
                            race_detail = r_res.json()
                            starts = race_detail.get('starts', [])
                            
                            for start in starts:
                                h_name = start.get('horse', {}).get('name', 'Tuntematon')
                                h_no = start.get('number', 0)
                                
                                # Peliprosentti (pools / distribution)
                                pools = start.get('pools', {})
                                bet_pct = 0.0
                                
                                # Haetaan V75/V85/V65 tai Vinnare prosentti
                                for p_key in ['v85', 'v75', 'v65', 'v64', 'v86', 'vinnare']:
                                    if p_key in pools:
                                        bet_pct = pools[p_key].get('betDistribution', 0) / 100.0
                                        break
                                
                                if bet_pct <= 0:
                                    bet_pct = round(100.0 / len(starts), 2)
                                
                                # Kengitystiedot (Bonukset)
                                bonus = 1.00
                                shoe_info = start.get('horse', {}).get('shoes', {})
                                if shoe_info.get('front') == False and shoe_info.get('back') == False:
                                    bonus += 0.12 # Kengättä joka jalasta
                                elif shoe_info.get('front') == False or shoe_info.get('back') == False:
                                    bonus += 0.05
                                    
                                sulky_info = start.get('horse', {}).get('sulky', {})
                                if sulky_info.get('type', {}).get('text') == 'Amerikansk':
                                    bonus += 0.08 # Amerikankärryt

                                unibet_k = round(100.0 / bet_pct, 2) if bet_pct > 0 else 15.00
                                
                                rows.append({
                                    "Kohde": kohde_str,
                                    "Nro": h_no,
                                    "Hevonen": h_name,
                                    "Veikkaus_%": round(bet_pct, 2),
                                    "Unibet_K": unibet_k,
                                    "Bonus": bonus,
                                    "Travronden": f"ATG Data | Varustebonus: {bonus:.2f}"
                                })
                    break
    except Exception as e:
        st.error(f"Virhe haettaessa dataa: {e}")
        
    return pd.DataFrame(rows)

# HAKU AJO
df_raw = fetch_real_atg_data(selected_date, selected_track_code)

if df_raw.empty:
    st.warning(f"⚠️ Ei löydetty vahvistettuja lähtölistoja radalle **{selected_track_name}** päivämäärälle **{selected_date.strftime('%d.%m.%Y')}**. Tapahtuma ei välttämättä ole vielä auki ATG:ssä.")
else:
    st.success(f"📍 Rata: **{selected_track_name}** | 📅 Päivämäärä: **{selected_date.strftime('%d.%m.%Y')}** | 🏇 Oikeita hevosia haettu: **{len(df_raw)} kpl**")

# --- SIMULAATIOFUNKTIO ---
def run_simulation(df, n_sims, spets):
    df_calc = df.copy()
    df_calc['Raw_Score'] = df_calc['Veikkaus_%'] * df_calc['Bonus'] * spets
    df_calc['Prob'] = df_calc.groupby('Kohde')['Raw_Score'].transform(lambda x: x / x.sum())
    
    results = []
    for kohde, group in df_calc.groupby('Kohde'):
        probs = group['Prob'].values
        nros = group['Nro'].values
        
        draws = np.random.choice(nros, size=n_sims, p=probs)
        unique, counts = np.unique(draws, return_counts=True)
        win_counts = dict(zip(unique, counts))
        
        for idx, row in group.iterrows():
            wins = win_counts.get(row['Nro'], 0)
            sim_prob = wins / n_sims
            sim_pct = sim_prob * 100
            
            peli_pct = row['Veikkaus_%']
            unibet_k = row['Unibet_K']
            
            ev_pool = round(sim_pct / peli_pct, 2) if peli_pct > 0 else 0.00
            ev_unibet = round((sim_prob * unibet_k), 2)
            raja_k = round(100 / sim_pct, 2) if sim_pct > 0 else 999.00
            
            if ev_pool >= 1.20 or ev_unibet >= 1.20:
                tila = "🔥 HUIPPU EV+"
            elif ev_pool >= 1.05 or ev_unibet >= 1.05:
                tila = "✅ EV+"
            elif ev_pool >= 0.85:
                tila = "⚪ Neutraali"
            else:
                tila = "❌ Ylipelattu"

            results.append({
                "Kohde": row['Kohde'],
                "Nro": int(row['Nro']),
                "Hevonen": row['Hevonen'],
                "Veikkaus %": f"{row['Veikkaus_%']:.2f}%",
                "Simu %": f"{sim_pct:.2f}%",
                "Raja-K": f"{raja_k:.2f}",
                "EV-Pooli": f"{ev_pool:.2f}",
                "Unibet K": f"{unibet_k:.2f}",
                "EV-Unibet": f"{ev_unibet:.2f}",
                "Tila": tila,
                "Travronden": row['Travronden']
            })
            
    return pd.DataFrame(results)

# Ajonappi
if not df_raw.empty:
    if st.button("🚀 KÄYNNISTÄ SIMULAATIO", type="primary"):
        df_res = run_simulation(df_raw, n_simulations, spets_bias)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Simulaatioajot", f"{n_simulations:,}".replace(",", " "))
        col2.metric("Pooli EV+ kohteet", len(df_res[df_res["EV-Pooli"].astype(float) >= 1.05]))
        if use_unibet:
            col3.metric("Unibet ylikertoimet", len(df_res[df_res["EV-Unibet"].astype(float) >= 1.05]))
        else:
            col3.metric("Unibet-haku", "Pois päältä")
        
        st.markdown("---")
        
        unique_races = df_res["Kohde"].unique().tolist()
        tab_list = ["Kaikki Lähdöt"] + unique_races
        tabs = st.tabs(tab_list)
        
        with tabs[0]:
            cols = ["Kohde", "Nro", "Hevonen", "Veikkaus %", "Simu %", "Raja-K", "EV-Pooli"]
            if use_unibet:
                cols.extend(["Unibet K", "EV-Unibet"])
            cols.append("Tila")
            if use_travronden:
                cols.append("Travronden")
            st.dataframe(df_res[cols], use_container_width=True, height=500)

        for i, race_name in enumerate(unique_races, start=1):
            with tabs[i]:
                df_single = df_res[df_res["Kohde"] == race_name]
                cols_single = ["Nro", "Hevonen", "Veikkaus %", "Simu %", "Raja-K", "EV-Pooli"]
                if use_unibet:
                    cols_single.extend(["Unibet K", "EV-Unibet"])
                cols_single.append("Tila")
                if use_travronden:
                    cols_single.append("Travronden")
                st.dataframe(df_single[cols_single], use_container_width=True)
