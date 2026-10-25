import numpy as np
import pandas as pd
import streamlit as st

# --- SIVUN ASETUKSET ---
st.set_page_config(page_title="Stella Quant", layout="wide", initial_sidebar_state="expanded")

# Custom tyylittely visuaalisen ilmeen raikastamiseen
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 0px;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 25px;
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

# Otsikko
st.markdown('<div class="main-title">STELLA QUANT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Kvantitatiivinen V85-simulaattori & peliarvoanalysaattori</div>', unsafe_allow_html=True)

# --- SIVUPALKKI: SÄÄTIMET ---
st.sidebar.markdown("### ⚙️ SIMULAATION SÄÄTIMET")

# 1. Kohdelähdön valinta
selected_target = st.sidebar.selectbox(
    "Kohdelähtö",
    ["Kaikki Lähdöt (V85-1 - V85-8)", "V85-1", "V85-2", "V85-3", "V85-4", "V85-5", "V85-6", "V85-7", "V85-8"]
)

# 2. Keulapainotus & Monte Carlo
spets_bias = st.sidebar.slider("Keulapainotus (Spets-kerroin)", 1.00, 1.30, 1.15, step=0.01)
n_simulations = st.sidebar.slider("Monte Carlo -kierrokset", 10000, 100000, 50000, step=10000)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 AUTOMAATTISET HAUT & DATA")

# 3. Automaattihaut päälle/pois
use_unibet = st.sidebar.toggle("Hae Unibet-kertoimet", value=True)
use_travronden = st.sidebar.toggle("Hae Travronden-kommentit", value=True)

# 4. Google-haku integroituna (Aina päällä)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 GOOGLE-LÄHTÖHAKU")
search_term = f"{selected_target} vihjeet ravien" if selected_target != "Kaikki Lähdöt (V85-1 - V85-8)" else "V85 vihjeet ravien"
google_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"
st.sidebar.markdown(f"🔗 [Avaa Google-haku: **{search_term}**]({google_url})")

# --- DATASETTI ---
raw_data = [
    # =============== V85-1 ===============
    {"Kohde": "V85-1", "Nro": 3, "Hevonen": "Nilla Lane", "Veikkaus_%": 76.0, "Unibet_K": 1.77, "Bonus": 1.18, "Travronden": "Rautainen Pankki, spets & kengättä."},
    {"Kohde": "V85-1", "Nro": 1, "Hevonen": "Panthere d'Inverne", "Veikkaus_%": 10.0, "Unibet_K": 9.13, "Bonus": 1.00, "Travronden": "B-varmistus sisäradalta."},
    {"Kohde": "V85-1", "Nro": 2, "Hevonen": "Fantastica Doda", "Veikkaus_%": 6.0, "Unibet_K": 15.00, "Bonus": 1.02, "Travronden": "Keulasta selkään, C-yllättäjä."},

    # =============== V85-2 ===============
    {"Kohde": "V85-2", "Nro": 7, "Hevonen": "Hawk Eyed Girl", "Veikkaus_%": 23.0, "Unibet_K": 4.35, "Bonus": 1.25, "Travronden": "HUIPPU EV+ Spets & Barfota runt om."},
    {"Kohde": "V85-2", "Nro": 2, "Hevonen": "Polly Vici", "Veikkaus_%": 28.0, "Unibet_K": 3.80, "Bonus": 0.85, "Travronden": "Ylipelattu suosikki, laukkariski."},
    {"Kohde": "V85-2", "Nro": 12, "Hevonen": "Call Me Ottilia", "Veikkaus_%": 4.0, "Unibet_K": 18.50, "Bonus": 1.15, "Travronden": "C-Yllättäjä, rycktussar peliin."},
    {"Kohde": "V85-2", "Nro": 9, "Hevonen": "Mahakala", "Veikkaus_%": 10.0, "Unibet_K": 10.00, "Bonus": 1.08, "Travronden": "EV+ Nousukuntoinen."},

    # =============== V85-3 ===============
    {"Kohde": "V85-3", "Nro": 3, "Hevonen": "Veritas", "Veikkaus_%": 39.0, "Unibet_K": 2.75, "Bonus": 0.95, "Travronden": "Pääsuosikki, lievästi ylipelattu."},
    {"Kohde": "V85-3", "Nro": 6, "Hevonen": "Rip Wheeler", "Veikkaus_%": 5.0, "Unibet_K": 20.00, "Bonus": 1.30, "Travronden": "VARUSTEPOMMI / Barfota runt om."},
    {"Kohde": "V85-3", "Nro": 1, "Hevonen": "Helan Går", "Veikkaus_%": 17.0, "Unibet_K": 6.25, "Bonus": 1.10, "Travronden": "A / EV+ Sisärata."},
    {"Kohde": "V85-3", "Nro": 2, "Hevonen": "Wiener Sängerknabe", "Veikkaus_%": 4.0, "Unibet_K": 22.00, "Bonus": 1.15, "Travronden": "Jättiyllättäjä haku."},

    # =============== V85-4 ===============
    {"Kohde": "V85-4", "Nro": 12, "Hevonen": "Chat Room", "Veikkaus_%": 30.0, "Unibet_K": 3.25, "Bonus": 1.05, "Travronden": "Vahva suosikki taka-alalta."},
    {"Kohde": "V85-4", "Nro": 13, "Hevonen": "Barkley", "Veikkaus_%": 15.0, "Unibet_K": 7.14, "Bonus": 1.20, "Travronden": "A / EV+ Berglundin u-hevonen."},
    {"Kohde": "V85-4", "Nro": 1, "Hevonen": "Mister Navajo", "Veikkaus_%": 4.0, "Unibet_K": 25.00, "Bonus": 1.12, "Travronden": "EV+ Yllättäjä paalulta."},

    # =============== V85-5 ===============
    {"Kohde": "V85-5", "Nro": 1, "Hevonen": "Richmond", "Veikkaus_%": 25.0, "Unibet_K": 4.00, "Bonus": 1.05, "Travronden": "A-ryhmän hevonen tulppa-paikalta."},
    {"Kohde": "V85-5", "Nro": 3, "Hevonen": "Elroy Face", "Veikkaus_%": 25.0, "Unibet_K": 13.64, "Bonus": 1.12, "Travronden": "A / Hienossa iskussa."},
    {"Kohde": "V85-5", "Nro": 12, "Hevonen": "Hard Rock", "Veikkaus_%": 16.0, "Unibet_K": 6.25, "Bonus": 1.08, "Travronden": "B-varmistus hyvällä kirillä."},

    # =============== V85-6 ===============
    {"Kohde": "V85-6", "Nro": 7, "Hevonen": "Tvingens Calippo", "Veikkaus_%": 46.0, "Unibet_K": 2.10, "Bonus": 1.02, "Travronden": "Vahva suosikki keulaan."},
    {"Kohde": "V85-6", "Nro": 2, "Hevonen": "Datos Rainbow", "Veikkaus_%": 13.0, "Unibet_K": 3.11, "Bonus": 1.22, "Travronden": "HUIPPU EV+ Djuse / Redén."},
    {"Kohde": "V85-6", "Nro": 1, "Hevonen": "Wannabe Zaz", "Veikkaus_%": 14.0, "Unibet_K": 76.64, "Bonus": 1.10, "Travronden": "Spets-haku."},

    # =============== V85-7 ===============
    {"Kohde": "V85-7", "Nro": 3, "Hevonen": "Diva Ek", "Veikkaus_%": 51.0, "Unibet_K": 4.37, "Bonus": 1.00, "Travronden": "Keulapiikki."},
    {"Kohde": "V85-7", "Nro": 5, "Hevonen": "Kentucky River", "Veikkaus_%": 11.0, "Unibet_K": 8.50, "Bonus": 1.25, "Travronden": "HUIPPU EV+ Kirikone."},
    {"Kohde": "V85-7", "Nro": 12, "Hevonen": "A Fair Day", "Veikkaus_%": 24.0, "Unibet_K": 3.50, "Bonus": 1.02, "Travronden": "Luokkahevonen taka-alalta."},

    # =============== V85-8 ===============
    {"Kohde": "V85-8", "Nro": 6, "Hevonen": "Nickel Occagnes", "Veikkaus_%": 51.0, "Unibet_K": 1.95, "Bonus": 1.00, "Travronden": "Päätöslähdön suosikki."},
    {"Kohde": "V85-8", "Nro": 5, "Hevonen": "Gustav Simoni", "Veikkaus_%": 16.0, "Unibet_K": 6.67, "Bonus": 1.20, "Travronden": "EV+ Lövgrenin luokkamenijä."},
    {"Kohde": "V85-8", "Nro": 12, "Hevonen": "Black Fire", "Veikkaus_%": 4.0, "Unibet_K": 20.00, "Bonus": 1.25, "Travronden": "HUIPPU EV+ Jättiyllättäjä."}
]

df_raw = pd.DataFrame(raw_data)

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

# Suodatus kohdelähdön mukaan
if selected_target != "Kaikki Lähdöt (V85-1 - V85-8)":
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
    
    tabs = st.tabs(["Kaikki Lähdöt", "V85-1", "V85-2", "V85-3", "V85-4", "V85-5", "V85-6", "V85-7", "V85-8"])
    
    with tabs[0]:
        cols = ["Kohde", "Nro", "Hevonen", "Veikkaus %", "Simu %", "Raja-K", "EV-Pooli"]
        if use_unibet:
            cols.extend(["Unibet K", "EV-Unibet"])
        cols.append("Tila")
        if use_travronden:
            cols.append("Travronden")
        st.dataframe(df_res[cols], use_container_width=True, height=500)

    for i in range(1, 9):
        target_name = f"V85-{i}"
        with tabs[i]:
            df_single = df_res[df_res["Kohde"] == target_name]
            if df_single.empty:
                st.info(f"Valitse sivupalkista '{target_name}' tai 'Kaikki Lähdöt'.")
            else:
                cols_single = ["Nro", "Hevonen", "Veikkaus %", "Simu %", "Raja-K", "EV-Pooli"]
                if use_unibet:
                    cols_single.extend(["Unibet K", "EV-Unibet"])
                cols_single.append("Tila")
                if use_travronden:
                    cols_single.append("Travronden")
                st.dataframe(df_single[cols_single], use_container_width=True)
