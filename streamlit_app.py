import datetime
import requests
import pandas as pd
import streamlit as st

# ==========================================
# 1. SIVUN ASETUKSET & VISUAALINEN TYYLI
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
            <div class="stella-logo-subtitle">Aito Live ATG Direct Integration</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if "winners" not in st.session_state:
    st.session_state["winners"] = {}

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
# 3. DIRECT ATG GAME & ODDS API INTEGRATION
# ==========================================
@st.cache_data(ttl=2)
def fetch_direct_atg_data(date_obj, track_code, track_name):
    date_str = date_obj.strftime("%Y-%m-%d")
    calendar_url = f"https://www.atg.se/services/racinginfo/v1/api/calendar/day/{date_str}"
    
    # Täydelliset selainotsakkeet Cloudflare-ohitukseen
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.atg.se/",
        "Origin": "https://www.atg.se"
    }
    
    rows = []
    try:
        session = requests.Session()
        res = session.get(calendar_url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            cal_data = res.json()
            
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
                
                # Haetaan lähdön yksityiskohdat ja pelilinkit
                race_url = f"https://www.atg.se/services/racinginfo/v1/api/races/{race_id}"
                r_res = session.get(race_url, headers=headers, timeout=5)
                
                if r_res.status_code == 200:
                    race_detail = r_res.json()
                    
                    distance = race_detail.get('distance', 0)
                    start_method_raw = str(race_detail.get('startMethod', ''))
                    if start_method_raw.lower() in ['a', 'autostart']:
                        start_method = "Ryhmäajo (Auto)"
                    elif start_method_raw.lower() in ['v', 'voltstart']:
                        start_method = "Tasoitusajo (Voltti)"
                    else:
                        start_method = start_method_raw if start_method_raw else "Tuntematon"
                    
                    starts = race_detail.get('starts', [])
                    games = race_detail.get('games', {})
                    
                    # Haetaan aktiivinen T-peli (esim. GS75, V85, V75)
                    active_t_game_id = None
                    t_game_label = "-"
                    
                    for g_type in ['gs75', 'v85', 'v75', 'v86', 'v65', 'v64', 'v5', 'v4']:
                        if g_type in games:
                            g_obj = games[g_type]
                            if isinstance(g_obj, dict):
                                active_t_game_id = g_obj.get('id')
                            elif isinstance(g_obj, list) and len(g_obj) > 0:
                                active_t_game_id = g_obj[0].get('id')
                            t_game_label = g_type.upper()
                            break
                    
                    # Jos T-pelin Game ID löytyi, haetaan sen tuoreet peliprosentit suoraan Game APIsta
                    game_distribution = {}
                    if active_t_game_id:
                        game_url = f"https://www.atg.se/services/racinginfo/v1/api/games/{active_t_game_id}"
                        g_res = session.get(game_url, headers=headers, timeout=5)
                        if g_res.status_code == 200:
                            g_data = g_res.json()
                            # Etsitään tämän lähdön kohde
                            for leg in g_data.get('races', []):
                                if leg.get('number') == race_no or leg.get('id') == race_id:
                                    for s_info in leg.get('starts', []):
                                        s_num = s_info.get('number')
                                        dist = s_info.get('betDistribution', 0)
                                        if dist > 0:
                                            game_distribution[s_num] = dist / 100.0 if dist > 100 else float(dist)

                    for start in starts:
                        if start.get('scratched', False):
                            continue

                        horse_data = start.get('horse', {})
                        h_name = horse_data.get('name', 'Tuntematon')
                        h_no = int(start.get('number', 0))
                        
                        start_pools = start.get('pools', {})
                        live_odds_val = None
                        
                        # 1. HAETAAN REALTIME V-ODDS (VOITTAJAKERROIN)
                        if 'vinnare' in start_pools:
                            v_data = start_pools['vinnare']
                            raw_o = v_data.get('odds', 0) or v_data.get('fixedOdds', 0)
                            if raw_o > 0:
                                live_odds_val = float(raw_o) / 100.0 if raw_o > 100 else float(raw_o)

                        # 2. PROSENTTI: Pelijakauma Game-APIsta TAI laskettu V-ODDS -kertoimesta
                        t_pct_val = game_distribution.get(h_no)
                        
                        if t_pct_val is None and live_odds_val and live_odds_val > 0:
                            t_pct_val = round((85.0 / live_odds_val), 2)

                        bet_pct_str = f"{t_pct_val:.2f}%" if t_pct_val is not None else "-"
                        odds_str = f"{live_odds_val:.2f}" if live_odds_val is not None else "-"

                        rows.append({
                            "Race_No": race_no,
                            "Kohde": kohde_str,
                            "Matka": f"{distance} m",
                            "Lähtötapa": start_method,
                            "T-Peli": t_game_label,
                            "Nro": h_no,
                            "Hevonen": h_name,
                            "T-Peli %": bet_pct_str,
                            "Live Kerroin": odds_str
                        })
    except Exception as e:
        st.error(f"Virhe haettaessa dataa: {e}")
        
    return pd.DataFrame(rows)

# ==========================================
# 4. KÄYTTÖLIITTYMÄ
# ==========================================
df_raw = fetch_direct_atg_data(selected_date, selected_track_code, selected_track_name)

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
        df_all = df_raw.copy()
        df_all["Tulos / Voittaja"] = df_all.apply(
            lambda r: "🏆 VOITTAJA" if st.session_state["winners"].get(r["Kohde"]) == r["Nro"] else "-", axis=1
        )
        cols = ["Kohde", "Matka", "Lähtötapa", "T-Peli", "Nro", "Hevonen", "T-Peli %", "Live Kerroin", "Tulos / Voittaja"]
        st.dataframe(df_all[cols], use_container_width=True, height=550, hide_index=True)

    # LÄHDÖITTÄIN
    for i, race_name in enumerate(unique_races, start=1):
        with tabs[i]:
            df_single = df_raw[df_raw["Kohde"] == race_name].sort_values(by="Nro").copy()
            
            if not df_single.empty:
                m_info = df_single.iloc[0]["Matka"]
                l_info = df_single.iloc[0]["Lähtötapa"]
                t_info = df_single.iloc[0]["T-Peli"]
                
                col_info, col_win = st.columns([2, 1])
                with col_info:
                    st.info(f"📏 Matka: **{m_info}** | 🚦 Lähtötapa: **{l_info}** | 🏆 Pelimuoto: **{t_info}**")
                
                with col_win:
                    horse_options = [0] + df_single["Nro"].tolist()
                    current_win = st.session_state["winners"].get(race_name, 0)
                    
                    selected_win = st.selectbox(
                        f"Merkitse voittaja ({race_name})",
                        options=horse_options,
                        format_func=lambda x: "Ei tulosta" if x == 0 else f"Nro {x} - {df_single[df_single['Nro']==x]['Hevonen'].values[0]}",
                        index=horse_options.index(current_win) if current_win in horse_options else 0,
                        key=f"win_select_{race_name}"
                    )
                    st.session_state["winners"][race_name] = selected_win

            df_single["Tulos / Voittaja"] = df_single["Nro"].apply(
                lambda nro: "🏆 VOITTAJA" if st.session_state["winners"].get(race_name) == nro else "-"
            )
            
            cols_single = ["Nro", "Hevonen", "T-Peli %", "Live Kerroin", "Tulos / Voittaja"]
            st.dataframe(df_single[cols_single], use_container_width=True, hide_index=True)
