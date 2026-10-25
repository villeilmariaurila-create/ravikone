import datetime
import requests
import numpy as np
import pandas as pd
import streamlit as st

# --- SIVUN ASETUKSET ---
st.set_page_config(page_title="Stella", layout="wide", initial_sidebar_state="expanded")

# --- VISUAALINEN ILME & HYMYILEVÄ LOGO ---
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

# LOGO
st.markdown("""
    <div class="stella-logo-container">
        <div class="stella-logo-icon">😊</div>
        <div>
            <div class="stella-logo-text">STELLA</div>
            <div class="stella-logo-subtitle">Aito Faktapohjainen Quant Racing Engine</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIVUPALKKI ---
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

if st.sidebar.button("🔄 Päivitä kertoimet ja datat"):
    st.cache_data.clear()

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ SIMULAATION PARAMETRIT")

spets_bias = st.sidebar.slider("Keulapainotus (Spets-kerroin)", 1.00, 1.30, 1.15, step=0.01)
n_simulations = st.sidebar.slider("Monte Carlo -kierrokset", 10000, 100000, 50000, step=10000)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 DATA-INTEGRAATIOT")
use_unibet = st.sidebar.toggle("Unibet-kertoimet", value=True)
use_travronden = st.sidebar.toggle("Travronden-kommentit", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 GOOGLE-LÄHTÖHAKU")
search_term = f"{selected_track_name} {selected_date.strftime('%d.%m.%Y')} vihjeet"
google_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
st.sidebar.markdown(f"🔗 [Google-haku: **{selected_track_name}**]({google_url})")

# --- PUHDAS DATAHAKU ATG:N REALIAIKAISESTA RAJAPINNASTA ---
@st.cache_data(ttl=60)
def fetch_factual_atg_data(date_obj, track_keyword):
    date_str = date_obj.strftime("%Y-%m-%d")
    calendar_url = f"https://www.atg.se/services/racinginfo/v1/api/calendar/day/{date_str}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    rows = []
    try:
        res = requests.get(calendar_url, headers=headers, timeout=10)
        if res.status_code == 200:
            cal_data = res.json()
            
            for track in cal_data.get('tracks', []):
                t_name = track.get('name', '').lower()
                if track_keyword in t_name:
                    races = track.get('races', [])
                    
                    for race in races:
                        race_id = race.get('id')
                        race_no = int(race.get('number', 1))
                        kohde_str = f"Lähtö {race_no}"
                        
                        race_url = f"https://www.atg.se/services/racinginfo/v1/api/races/{race_id}"
                        r_res = requests.get(race_url, headers=headers, timeout=5)
                        
                        if r_res.status_code == 200:
                            race_detail = r_res.json()
                            starts = race_detail.get('starts', [])
                            pools = race_detail.get('pools', {})
                            
                            t_game_type = None
                            for g_key in ['v85', 'v75', 'v86', 'v65', 'v64', 'gs75', 'v4', 'v5']:
                                if g_key in pools:
                                    t_game_type = g_key.upper()
                                    break
                            
                            game_label = f"{t_game_type}" if t_game_type else "Voittaja"
                            
                            for start in starts:
                                # Poisjääneet hevoset suodatetaan
                                if start.get('scratched', False):
                                    continue

                                h_name = start.get('horse', {}).get('name', '')
                                h_no = int(start.get('number', 0))
                                start_pools = start.get('pools', {})
                                
                                bet_pct = 0.0
                                unibet_odds = None
                                
                                if t_game_type and t_game_type.lower() in start_pools:
                                    bet_pct = start_pools[t_game_type.lower()].get('betDistribution', 0) / 100.0
                                
                                if 'vinnare' in start_pools:
                                    odds_raw = start_pools['vinnare'].get('odds', 0) / 100.0
                                    if odds_raw > 0:
                                        unibet_odds = round(odds_raw, 2)
                                        if bet_pct <= 0:
                                            bet_pct = round(100.0 / odds_raw, 2)
                                
                                if bet_pct <= 0:
                                    bet_pct = round(100.0 / max(len(starts), 1), 2)
                                
                                bonus = 1.00
                                shoe_info = start.get('horse', {}).get('shoes', {})
                                if shoe_info.get('front') == False and shoe_info.get('back') == False:
                                    bonus += 0.12
                                elif shoe_info.get('front') == False or shoe_info.get('back') == False:
                                    bonus += 0.05
                                    
                                sulky_info = start.get('horse', {}).get('sulky', {})
                                if sulky_info.get('type', {}).get('text') == 'Amerikansk':
                                    bonus += 0.08

                                rows.append({
                                    "Race_No": race_no,
                                    "Kohde": kohde_str,
                                    "Pelimuoto": game_label,
                                    "Nro": h_no,
                                    "Hevonen": h_name,
                                    "Veikkaus_%": round(bet_pct, 2),
                                    "Unibet_K": unibet_odds if unibet_odds else "-",
                                    "Bonus": bonus,
                                    "Travronden": ""
                                })
                    break
    except Exception as e:
        st.error(f"Virhe datan haussa: {e}")
        
    return pd.DataFrame(rows)

# HAKU
df_raw = fetch_factual_atg_data(selected_date, selected_track_code)

if df_raw.empty:
    st.warning(f"⚠️ Ei vahvistettua dataa radalle **{selected_track_name}** päivämäärälle **{selected_date.strftime('%d.%m.%Y')}**.")
else:
    st.success(f"📍 Rata: **{selected_track_name}** | 📅 Päivämäärä: **{selected_date.strftime('%d.%m.%Y')}** | 🏇 Haetut hevoset: **{len(df_raw)} kpl**")

# --- TURVALLINEN MONTE CARLO -SIMULAATTORI ---
def run_simulation(df, n_sims, spets):
    df_calc = df.copy()
    
    # Lasketaan raakavoima
    df_calc['Raw_Score'] = df_calc['Veikkaus_%'] * df_calc['Bonus'] * spets
    
    results = []
    for kohde, group in df_calc.groupby('Kohde'):
        # Normalisoidaan todennäköisyydet ja varmistetaan, että summa on täsmälleen 1.0
        raw_scores = group['Raw_Score'].values.astype(float)
        tot_score = np.sum(raw_scores)
        
        if tot_score > 0:
            probs = raw_scores / tot_score
        else:
            probs = np.ones(len(raw_scores)) / len(raw_scores)
            
        # Varmistetaan float64 tarkkuus ja normaali summa
        probs = probs / np.sum(probs)
        nros = group['Nro'].values
        
        # Suoritetaan turvallinen Monte Carlo -arvonta
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
            
            if isinstance(unibet_k, (int, float)):
                ev_unibet = round((sim_prob * unibet_k), 2)
                unibet_k_str = f"{unibet_k:.2f}"
                ev_unibet_str = f"{ev_unibet:.2f}"
            else:
                ev_unibet = 0.00
                unibet_k_str = "-"
                ev_unibet_str = "-"
                
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
                "Race_No": row['Race_No'],
                "Kohde": row['Kohde'],
                "Pelimuoto": row['Pelimuoto'],
                "Nro": int(row['Nro']),
                "Hevonen": row['Hevonen'],
                "Peli %": f"{row['Veikkaus_%']:.2f}%",
                "Simu %": f"{sim_pct:.2f}%",
                "Raja-K": f"{raja_k:.2f}",
                "EV-Pooli": f"{ev_pool:.2f}",
                "Unibet K": unibet_k_str,
                "EV-Unibet": ev_unibet_str,
                "Tila": tila,
                "Travronden": row['Travronden']
            })
            
    df_res = pd.DataFrame(results)
    df_res = df_res.sort_values(by=["Race_No", "Nro"]).reset_index(drop=True)
    return df_res

# AJONAPPI
if not df_raw.empty:
    if st.button("🚀 KÄYNNISTÄ SIMULAATIO", type="primary"):
        df_res = run_simulation(df_raw, n_simulations, spets_bias)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Simulaatioajot", f"{n_simulations:,}".replace(",", " "))
        col2.metric("Pooli EV+ kohteet", len(df_res[df_res["EV-Pooli"].astype(float) >= 1.05]))
        if use_unibet:
            valid_unibet = df_res[df_res["EV-Unibet"] != "-"]
            col3.metric("Unibet ylikertoimet", len(valid_unibet[valid_unibet["EV-Unibet"].astype(float) >= 1.05]))
        else:
            col3.metric("Unibet-haku", "Pois päältä")
        
        st.markdown("---")
        
        sorted_race_numbers = sorted(df_res["Race_No"].unique())
        unique_races = [f"Lähtö {num}" for num in sorted_race_numbers]
        tab_list = ["Kaikki Lähdöt"] + unique_races
        tabs = st.tabs(tab_list)
        
        with tabs[0]:
            cols = ["Kohde", "Pelimuoto", "Nro", "Hevonen", "Peli %", "Simu %", "Raja-K", "EV-Pooli"]
            if use_unibet:
                cols.extend(["Unibet K", "EV-Unibet"])
            cols.append("Tila")
            if use_travronden:
                cols.append("Travronden")
            st.dataframe(df_res[cols], use_container_width=True, height=500)

        for i, race_name in enumerate(unique_races, start=1):
            with tabs[i]:
                df_single = df_res[df_res["Kohde"] == race_name]
                cols_single = ["Pelimuoto", "Nro", "Hevonen", "Peli %", "Simu %", "Raja-K", "EV-Pooli"]
                if use_unibet:
                    cols_single.extend(["Unibet K", "EV-Unibet"])
                cols_single.append("Tila")
                if use_travronden:
                    cols_single.append("Travronden")
                st.dataframe(df_single[cols_single], use_container_width=True)
