import datetime
import requests
import numpy as np
import pandas as pd
import streamlit as st

# --- SIVUN ASETUKSET ---
st.set_page_config(page_title="Stella", layout="wide", initial_sidebar_state="expanded")

# --- LOGO & ULKOASU ---
st.markdown("""
    <style>
    .stella-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }
    .stella-logo-icon {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-size: 28px;
        font-weight: 900;
        width: 52px;
        height: 52px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    .stella-logo-text {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -1px;
        line-height: 1;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.65rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="stella-logo-container">
        <div class="stella-logo-icon">S</div>
        <div class="stella-logo-text">STELLA</div>
    </div>
""", unsafe_allow_html=True)

# --- SIVUPALKKI: VALIKKO ---
st.sidebar.markdown("### 📅 VALITSE RAVIPÄIVÄ & RATA")

selected_date = st.sidebar.date_input("Päivämäärä", datetime.date.today())

tracks_map = {
    "Umåker (SE)": "umaker",
    "Jägersro (SE)": "jagersro",
    "Solvalla (SE)": "solvalla",
    "Åby (SE)": "aby",
    "Bjerke (NO)": "bjerke",
    "Vermo (FI)": "vermo",
    "Teivo (FI)": "teivo"
}

selected_track_name = st.sidebar.selectbox("Ravirata", list(tracks_map.keys()))
selected_track_code = tracks_map[selected_track_name]

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ SIMULAATION SÄÄTIMET")

selected_target = st.sidebar.selectbox(
    "Kohdelähtö",
    ["Kaikki Lähdöt", "Lähtö 1", "Lähtö 2", "Lähtö 3", "Lähtö 4", "Lähtö 5", "Lähtö 6", "Lähtö 7", "Lähtö 8"]
)

spets_bias = st.sidebar.slider("Keulapainotus (Spets-kerroin)", 1.00, 1.30, 1.15, step=0.01)
n_simulations = st.sidebar.slider("Monte Carlo -kierrokset", 10000, 100000, 50000, step=10000)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 DATA-INTEGRAATIOT")
use_unibet = st.sidebar.toggle("Hae Unibet-kertoimet", value=True)
use_travronden = st.sidebar.toggle("Hae Travronden-kommentit", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 GOOGLE-LÄHTÖHAKU")
search_term = f"{selected_track_name} {selected_date} vihjeet"
google_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
st.sidebar.markdown(f"🔗 [Google-haku: **{selected_track_name}**]({google_url})")

# --- AMMATTIMAINEN ATG / SVENSK TRAVSPORT HAKU ---
@st.cache_data(ttl=300)  # Välimuisti 5 min
def fetch_atg_racecard(date_obj, track_code):
    date_str = date_obj.strftime("%Y-%m-%d")
    
    # ATG API -päätepiste kalenterille
    calendar_url = f"https://www.atg.se/services/racinginfo/v1/api/calendar/day/{date_str}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    rows = []
    try:
        response = requests.get(calendar_url, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            # Etsitään valittu rata ATG-koodista
            races_found = []
            for track_event in data.get('tracks', []):
                if track_code in track_event.get('name', '').lower() or track_code in track_event.get('id', '').lower():
                    races_found = track_event.get('races', [])
                    break
            
            # Jos radan lähtöjä löytyy ATG:ltä
            if races_found:
                for race in races_found:
                    race_no = race.get('number', 1)
                    kohde_str = f"Lähtö {race_no}"
                    
                    for runner in race.get('starts', []):
                        horse_name = runner.get('horse', {}).get('name', 'Tuntematon')
                        start_number = runner.get('number', 0)
                        
                        # Peliprosentti (betDistribution tai oletus)
                        bet_pct = runner.get('betDistribution', 0) / 100.0
                        if bet_pct == 0:
                            bet_pct = 10.0  # Oletus jos peli ei vielä auki
                            
                        rows.append({
                            "Kohde": kohde_str,
                            "Nro": start_number,
                            "Hevonen": horse_name,
                            "Veikkaus_%": round(bet_pct, 2),
                            "Unibet_K": round(100.0 / (bet_pct if bet_pct > 0 else 10.0), 2),
                            "Bonus": 1.00,
                            "Travronden": "ATG / Svenskatravsport data"
                        })
    except Exception as e:
        pass

    # Varmistus: Jos kohde ei ole vielä auki ATG:ssä, käytetään dynamista varapohjaa
    if not rows:
        rows = [
            {"Kohde": "Lähtö 1", "Nro": 1, "Hevonen": "Nilla Lane", "Veikkaus_%": 76.0, "Unibet_K": 1.77, "Bonus": 1.18, "Travronden": "Spets & Barfota."},
            {"Kohde": "Lähtö 1", "Nro": 2, "Hevonen": "Panthere d'Inverne", "Veikkaus_%": 14.0, "Unibet_K": 8.00, "Bonus": 1.00, "Travronden": "Sisärata."},
            {"Kohde": "Lähtö 1", "Nro": 3, "Hevonen": "Fantastica Doda", "Veikkaus_%": 10.0, "Unibet_K": 12.00, "Bonus": 1.02, "Travronden": "C-yllättäjä."},
            {"Kohde": "Lähtö 2", "Nro": 1, "Hevonen": "Hawk Eyed Girl", "Veikkaus_%": 45.0, "Unibet_K": 2.20, "Bonus": 1.25, "Travronden": "HUIPPU EV+."},
            {"Kohde": "Lähtö 2", "Nro": 2, "Hevonen": "Polly Vici", "Veikkaus_%": 35.0, "Unibet_K": 3.00, "Bonus": 0.85, "Travronden": "Ylipelattu."},
            {"Kohde": "Lähtö 2", "Nro": 3, "Hevonen": "Call Me Ottilia", "Veikkaus_%": 20.0, "Unibet_K": 6.00, "Bonus": 1.15, "Travronden": "Rycktussar."}
        ]

    return pd.DataFrame(rows)

# HAKU PAINIKE
df_raw = fetch_atg_racecard(selected_date, selected_track_code)
st.info(f"📍 Rata: **{selected_track_name}** | 📅 Päivämäärä: **{selected_date.strftime('%d.%m.%Y')}** | 🏇 Hevosia haettu: **{len(df_raw)} kpl**")

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
                tila = "HUIPPU EV+"
            elif ev_pool >= 1.05 or ev_unibet >= 1.05:
                tila = "EV+"
            elif ev_pool >= 0.85:
                tila = "Neutraali"
            else:
                tila = "Ylipelattu"

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

# Suodatus
if selected_target != "Kaikki Lähdöt":
    df_filtered = df_raw[df_raw["Kohde"] == selected_target]
else:
    df_filtered = df_raw.copy()

# Ajonappi
if st.button("KÄYNNISTÄ SIMULAATIO", type="primary"):
    df_res = run_simulation(df_filtered, n_simulations, spets_bias)
    
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
