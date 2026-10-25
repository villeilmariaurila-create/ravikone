import datetime
import requests
import pandas as pd
import streamlit as st

# ==========================================
# 1. SIVUN ASETUKSET & VISUAALINEN ILME
# ==========================================
st.set_page_config(page_title="Stella Data Engine", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stella-logo-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 24px;
    }
    .stella-logo-icon {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        color: white;
        font-size: 34px;
        width: 60px;
        height: 60px;
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

# LOGO (😉)
st.markdown("""
    <div class="stella-logo-container">
        <div class="stella-logo-icon">😉</div>
        <div>
            <div class="stella-logo-text">STELLA</div>
            <div class="stella-logo-subtitle">Core Live Data Engine (Ruotsin Ravit)</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 2. VALIKOT (PÄIVÄMÄÄRÄ & RATA)
# ==========================================
st.sidebar.markdown("### 📅 VALITSE RAVIPÄIVÄ & RATA")

selected_date = st.sidebar.date_input("Päivämäärä", datetime.date.today())

tracks_map = {
    "Umåker (SE)": "um",
    "Jägersro (SE)": "jä",
    "Solvalla (SE)": "s",
    "Åby (SE)": "å",
    "Bjerke (NO)": "bj",
    "Boden (SE)": "bo",
    "Bergsåker (SE)": "b",
    "Eskilstuna (SE)": "e",
    "Vermo (FI)": "ve",
    "Teivo (FI)": "t"
}

selected_track_name = st.sidebar.selectbox("Ravirata", list(tracks_map.keys()))
selected_track_code = tracks_map[selected_track_name]

if st.sidebar.button("⚡ PÄIVITÄ LIVE-DATA NOW"):
    st.cache_data.clear()

# ==========================================
# 3. BOMMINVARMA LIVE DATA-HAKURI (ATG API)
# ==========================================
@st.cache_data(ttl=5)
def fetch_core_live_data(date_obj, track_code, track_name):
    date_str = date_obj.strftime("%Y-%m-%d")
    calendar_url = f"https://www.atg.se/services/racinginfo/v1/api/calendar/day/{date_str}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    rows = []
    try:
        res = requests.get(calendar_url, headers=headers, timeout=10)
        if res.status_code == 200:
            cal_data = res.json()
            
            # Etsitään haluttu rata
            target_races = []
            for track in cal_data.get('tracks', []):
                t_id = str(track.get('id', '')).lower()
                t_name = str(track.get('name', '')).lower()
                
                if track_code == t_id or track_code in t_name or track_name.split()[0].lower() in t_name:
                    target_races = track.get('races', [])
                    break
            
            for race in target_races:
                race_id = race.get('id')
                race_no = int(race.get('number', 1))
                kohde_str = f"Lähtö {race_no}"
                
                # Suora kutsu lähdön raakatilastoihin
                race_url = f"https://www.atg.se/services/racinginfo/v1/api/races/{race_id}"
                r_res = requests.get(race_url, headers=headers, timeout=5)
                
                if r_res.status_code == 200:
                    race_detail = r_res.json()
                    
                    # 1. JUOSTAVA MATKA JA LÄHTÖTAPA
                    distance = race_detail.get('distance', 0)
                    start_method_raw = race_detail.get('startMethod', '')
                    if start_method_raw.lower() in ['a', 'autostart']:
                        start_method = "Ryhmäajo (Auto)"
                    elif start_method_raw.lower() in ['v', 'voltstart']:
                        start_method = "Tasoitusajo (Voltti)"
                    else:
                        start_method = start_method_raw if start_method_raw else "Tuntematon"
                    
                    starts = race_detail.get('starts', [])
                    pools = race_detail.get('pools', {})
                    
                    # 2. TUNNISTETAAN T-PELI (GS75, V85, V75, V65, V64, V5, V4)
                    t_game_type = "-"
                    for g_key in ['gs75', 'v85', 'v75', 'v86', 'v65', 'v64', 'v5', 'v4']:
                        if g_key in pools:
                            t_game_type = g_key.upper()
                            break
                    
                    for start in starts:
                        if start.get('scratched', False):
                            continue

                        horse_data = start.get('horse', {})
                        h_name = horse_data.get('name', 'Tuntematon')
                        h_no = int(start.get('number', 0))
                        
                        start_pools = start.get('pools', {})
                        bet_pct_str = "-"
                        live_odds_str = "-"
                        
                        # 3. LUE LIVE-VOITTAJAKERROIN (Vinnare)
                        if 'vinnare' in start_pools:
                            v_info = start_pools['vinnare']
                            raw_o = v_info.get('odds', 0)
                            if raw_o > 0:
                                odds_val = raw_o / 100.0 if raw_o > 100 else float(raw_o)
                                live_odds_str = f"{odds_val:.2f}"
                        
                        # 4. LUE T-PELIN PROSENTTI
                        if t_game_type != "-" and t_game_type.lower() in start_pools:
                            t_pct = start_pools[t_game_type.lower()].get('betDistribution', 0) / 100.0
                            if t_pct > 0:
                                bet_pct_str = f"{t_pct:.2f}%"

                        rows.append({
                            "Race_No": race_no,
                            "Kohde": kohde_str,
                            "Matka": f"{distance} m",
                            "Lähtötapa": start_method,
                            "T-Peli": t_game_type,
                            "Nro": h_no,
                            "Hevonen": h_name,
                            "T-Peli %": bet_pct_str,
                            "Live Kerroin": live_odds_str
                        })
    except Exception as e:
        st.error(f"Virhe haettaessa dataa: {e}")
        
    return pd.DataFrame(rows)

# ==========================================
# 4. KÄYTTÖLIITTYMÄ NÄKYMÄ
# ==========================================
df_raw = fetch_core_live_data(selected_date, selected_track_code, selected_track_name)

if df_raw.empty:
    st.warning(f"⚠️ Ei saatu dataa radalle **{selected_track_name}** päivämäärälle **{selected_date.strftime('%d.%m.%Y')}**.")
else:
    st.success(f"📍 Rata: **{selected_track_name}** | 📅 Päivämäärä: **{selected_date.strftime('%d.%m.%Y')}** | 🏇 Haetut valjakot: **{len(df_raw)} kpl**")

    sorted_race_numbers = sorted(df_raw["Race_No"].unique())
    unique_races = [f"Lähtö {num}" for num in sorted_race_numbers]
    tab_list = ["Kaikki Lähdöt"] + unique_races
    tabs = st.tabs(tab_list)

    # KAIKKI LÄHDÖT
    with tabs[0]:
        cols = ["Kohde", "Matka", "Lähtötapa", "T-Peli", "Nro", "Hevonen", "T-Peli %", "Live Kerroin"]
        st.dataframe(df_raw[cols], use_container_width=True, height=550, hide_index=True)

    # LÄHDÖITTÄIN
    for i, race_name in enumerate(unique_races, start=1):
        with tabs[i]:
            df_single = df_raw[df_raw["Kohde"] == race_name].sort_values(by="Nro")
            
            # Näytetään lähdön perustiedot (Matka ja Lähtötapa) yläpalkissa
            if not df_single.empty:
                m_info = df_single.iloc[0]["Matka"]
                l_info = df_single.iloc[0]["Lähtötapa"]
                t_info = df_single.iloc[0]["T-Peli"]
                st.info(f"📏 Matka: **{m_info}** | 🚦 Lähtötapa: **{l_info}** | 🏆 Pelimuoto: **{t_info}**")
            
            cols_single = ["Nro", "Hevonen", "T-Peli %", "Live Kerroin"]
            st.dataframe(df_single[cols_single], use_container_width=True, hide_index=True)
