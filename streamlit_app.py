import numpy as np
import pandas as pd
import streamlit as st

# --- STREAMLIT-SIVUN ASETUKSET ---
st.set_page_config(page_title="Toto85 Quant Dashboard", layout="wide")

st.title("🐎 Toto85 - Täydellinen Voittosimulaattori & Quant Dashboard")
st.caption("Monte Carlo -pohjainen EV+ ja peliarvo-analysaattori (Tabbed Dashboard -versio)")

# --- SIVUPALKKI: SÄÄTIMET JA SYÖTTEET ---
st.sidebar.header("⚙️ Simulaation Säätimet")

# 1. Lähdön valinta simuloinnille
selected_target = st.sidebar.selectbox(
    "Simuloinnin kohde",
    ["Kaikki Lähdöt (V85-1 - V85-8)", "V85-1", "V85-2", "V85-3", "V85-4", "V85-5", "V85-6", "V85-7", "V85-8"]
)

# 2. Monte Carlo & Spets
n_simulations = st.sidebar.slider("Monte Carlo -kierrokset", 10000, 100000, 50000, step=10000)
spets_bias = st.sidebar.slider("Ratakohtainen Spets-lisäkerroin", 1.00, 1.30, 1.15, step=0.05)

st.sidebar.markdown("---")
st.sidebar.header("📥 Data-integraatiot")
use_unibet = st.sidebar.checkbox("Käytä Unibetin kiinteitä kertoimia", value=True)
use_travronden = st.sidebar.checkbox("Näytä Travronden-kommentit", value=True)

# --- TOTO85-DATA (MUKANA TIKETIT, UNIBET JA TRAVRONDEN) ---
raw_data = [
    # =============== V85-1 ===============
    {"Kohde": "V85-1", "Nro": 3, "Hevonen": "Nilla Lane", "Veikkaus_%": 76.0, "Unibet_K": 1.77, "Bonus": 1.18, "Travronden": "Rautainen Pankki, spets & kengättä. Varma keulavoittaja."},
    {"Kohde": "V85-1", "Nro": 1, "Hevonen": "Panthere d'Inverne", "Veikkaus_%": 10.0, "Unibet_K": 9.13, "Bonus": 1.00, "Travronden": "B-varmistus sisäradalta, saa tarkan juoksun."},
    {"Kohde": "V85-1", "Nro": 2, "Hevonen": "Fantastica Doda", "Veikkaus_%": 6.0, "Unibet_K": 15.00, "Bonus": 1.02, "Travronden": "Keulasta selkään, C-yllättäjä haku."},

    # =============== V85-2 ===============
    {"Kohde": "V85-2", "Nro": 7, "Hevonen": "Hawk Eyed Girl", "Veikkaus_%": 23.0, "Unibet_K": 4.35, "Bonus": 1.25, "Travronden": "🔥 HUIPPU EV+ Spets & Barfota runt om. Päivän paras merkki."},
    {"Kohde": "V85-2", "Nro": 2, "Hevonen": "Polly Vici", "Veikkaus_%": 28.0, "Unibet_K": 3.80, "Bonus": 0.85, "Travronden": "Ylipelattu suosikki, laukkariski olemassa."},
    {"Kohde": "V85-2", "Nro": 12, "Hevonen": "Call Me Ottilia", "Veikkaus_%": 4.0, "Unibet_K": 18.50, "Bonus": 1.15, "Travronden": "C-Yllättäjä, rycktussar ensimmäistä kertaa."},
    {"Kohde": "V85-2", "Nro": 9, "Hevonen": "Mahakala", "Veikkaus_%": 10.0, "Unibet_K": 10.00, "Bonus": 1.08, "Travronden": "EV+ Nousukuntoinen, reissun onnistuessa kärkitaistossa."},

    # =============== V85-3 ===============
    {"Kohde": "V85-3", "Nro": 3, "Hevonen": "Veritas", "Veikkaus_%": 39.0, "Unibet_K": 2.75, "Bonus": 0.95, "Travronden": "Pääsuosikki, mutta kärsii hieman ylipeluusta."},
    {"Kohde": "V85-3", "Nro": 6, "Hevonen": "Rip Wheeler", "Veikkaus_%": 5.0, "Unibet_K": 20.00, "Bonus": 1.30, "Travronden": "💣 VARUSTEPOMMI / Barfota runt om & jännitysvarusteet."},
    {"Kohde": "V85-3", "Nro": 1, "Hevonen": "Helan Går", "Veikkaus_%": 17.0, "Unibet_K": 6.25, "Bonus": 1.10, "Travronden": "A / EV+ Sisärata takaa loistavan juoksun."},
    {"Kohde": "V85-3", "Nro": 2, "Hevonen": "Wiener Sängerknabe", "Veikkaus_%": 4.0, "Unibet_K": 22.00, "Bonus": 1.15, "Travronden": "Jättiyllättäjä haku, kykyjä parempi."},

    # =============== V85-4 ===============
    {"Kohde": "V85-4", "Nro": 12, "Hevonen": "Chat Room", "Veikkaus_%": 30.0, "Unibet_K": 3.25, "Bonus": 1.05, "Travronden": "Vahva suosikki taka-alalta."},
    {"Kohde": "V85-4", "Nro": 13, "Hevonen": "Barkley", "Veikkaus_%": 15.0, "Unibet_K": 7.14, "Bonus": 1.20, "Travronden": "A / EV+ Berglundin vihjaama u-hevonen."},
    {"Kohde": "V85-4", "Nro": 1, "Hevonen": "Mister Navajo", "Veikkaus_%": 4.0, "Unibet_K": 25.00, "Bonus": 1.12, "Travronden": "EV+ Yllättäjä paalulta."},

    # =============== V85-5 ===============
    {"Kohde": "V85-5", "Nro": 1, "Hevonen": "Richmond", "Veikkaus_%": 25.0, "Unibet_K": 4.00, "Bonus": 1.05, "Travronden": "A-ryhmän hevonen tulppa-paikalta."},
    {"Kohde": "V85-5", "Nro": 3, "Hevonen": "Elroy Face", "Veikkaus_%": 25.0, "Unibet_K": 13.64, "Bonus": 1.12, "Travronden": "A / Hienossa iskussa, kerroin aivan liian korkea Unibetilla!"},
    {"Kohde": "V85-5", "Nro": 12, "Hevonen": "Hard Rock", "Veikkaus_%": 16.0, "Unibet_K": 6.25, "Bonus": 1.08, "Travronden": "B-varmistus hyvällä kirillä."},

    # =============== V85-6 ===============
    {"Kohde": "V85-6", "Nro": 7, "Hevonen": "Tvingens Calippo", "Veikkaus_%": 46.0, "Unibet_K": 2.10, "Bonus": 1.02, "Travronden": "Vahva suosikki keulaan."},
    {"Kohde": "V85-6", "Nro": 2, "Hevonen": "Datos Rainbow", "Veikkaus_%": 13.0, "Unibet_K": 3.11, "Bonus": 1.22, "Travronden": "🔥 HUIPPU EV+ Djuse / Redén kaksikko."},
    {"Kohde": "V85-6", "Nro": 1, "Hevonen": "Wannabe Zaz", "Veikkaus_%": 14.0, "Unibet_K": 76.64, "Bonus": 1.10, "Travronden": "Spets-haku, jättikertoiminen yllättäjä."},

    # =============== V85-7 ===============
    {"Kohde": "V85-7", "Nro": 3, "Hevonen": "Diva Ek", "Veikkaus_%": 51.0, "Unibet_K": 4.37, "Bonus": 1.00, "Travronden": "Kultadivisioonan keulapiikki."},
    {"Kohde": "V85-7", "Nro": 5, "Hevonen": "Kentucky River", "Veikkaus_%": 11.0, "Unibet_K": 8.50, "Bonus": 1.25, "Travronden": "🔥 HUIPPU EV+ Kirikone, jos vauhti menee yli."},
    {"Kohde": "V85-7", "Nro": 12, "Hevonen": "A Fair Day", "Veikkaus_%": 24.0, "Unibet_K": 3.50, "Bonus": 1.02, "Travronden": "Luokkahevonen taka-alalta."},

    # =============== V85-8 ===============
    {"Kohde": "V85-8", "Nro": 6, "Hevonen": "Nickel Occagnes", "Veikkaus_%": 51.0, "Unibet_K": 1.95, "Bonus": 1.00, "Travronden": "Päätöslähdön selkeä suosikki."},
    {"Kohde": "V85-8", "Nro": 5, "Hevonen": "Gustav Simoni", "Veikkaus_%": 16.0, "Unibet_K": 6.67, "Bonus": 1.20, "Travronden": "EV+ Lövgrenin luokkamenijä."},
    {"Kohde": "V85-8", "Nro": 12, "Hevonen": "Black Fire", "Veikkaus_%": 4.0, "Unibet_K": 20.00, "Bonus": 1.25, "Travronden": "🔥 HUIPPU EV+ Jättiyllättäjä piippuhyllyltä."}
]

df_raw = pd.DataFrame(raw_data)

# --- SIMULAATIOFUNKTIO ---
def run_monte_carlo(df, n_sims, spets):
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
            
            # Odotusarvot (EV)
            ev_pool = round(sim_pct / peli_pct, 2) if peli_pct > 0 else 0.00
            ev_unibet = round((sim_prob * unibet_k), 2)
            raja_k = round(100 / sim_pct, 2) if sim_pct > 0 else 999.00
            
            # Tila
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

# --- SUODATETAN KOHTEET VALINNAN MUKAAN ---
if selected_target != "Kaikki Lähdöt (V85-1 - V85-8)":
    df_filtered = df_raw[df_raw["Kohde"] == selected_target]
else:
    df_filtered = df_raw.copy()

# --- AJO PAINIKE ---
if st.button(f"🚀 AJA SIMULAATIO: {selected_target.upper()}", type="primary"):
    df_res = run_monte_carlo(df_filtered, n_simulations, spets_bias)
    
    # Metriikat
    col1, col2, col3 = st.columns(3)
    col1.metric("Simuloidut kierrokset", f"{n_simulations:,}".replace(",", " "))
    col2.metric("EV+ Kohteet (Pooli ≥ 1.05)", len(df_res[df_res["EV-Pooli"].astype(float) >= 1.05]))
    col3.metric("Unibet Ylikertoimet (EV ≥ 1.05)", len(df_res[df_res["EV-Unibet"].astype(float) >= 1.05]))
    
    st.markdown("---")
    
    # --- TABBED DASHBOARD LAYOUT (VÄLILEHDET) ---
    tab_names = ["📋 Kaikki Lähdöt", "V85-1", "V85-2", "V85-3", "V85-4", "V85-5", "V85-6", "V85-7", "V85-8"]
    tabs = st.tabs(tab_names)
    
    # TAB 0: KAIKKI LÄHDÖT YHTEENSA
    with tabs[0]:
        st.subheader("📊 Koko Kierroksen Yhteenveto")
        
        # Sarakkeiden valinta kytkimien mukaan
        cols_to_show = ["Kohde", "Nro", "Hevonen", "Veikkaus %", "Simu %", "Raja-K", "EV-Pooli"]
        if use_unibet:
            cols_to_show.extend(["Unibet K", "EV-Unibet"])
        cols_to_show.append("Tila")
        if use_travronden:
            cols_to_show.append("Travronden")
            
        st.dataframe(df_res[cols_to_show], use_container_width=True, height=500)

    # TABS 1-8: YKSITTÄISET LÄHDÖT
    for i in range(1, 9):
        target_name = f"V85-{i}"
        with tabs[i]:
            st.subheader(f"🐎 Lähtö {target_name}")
            df_single = df_res[df_res["Kohde"] == target_name]
            
            if df_single.empty:
                st.info(f"Aja simulaatio 'Kaikki Lähdöt' tai valitse sivupalkista {target_name}.")
            else:
                cols_single = ["Nro", "Hevonen", "Veikkaus %", "Simu %", "Raja-K", "EV-Pooli"]
                if use_unibet:
                    cols_single.extend(["Unibet K", "EV-Unibet"])
                cols_single.append("Tila")
                if use_travronden:
                    cols_single.append("Travronden")
                    
                st.dataframe(df_single[cols_single], use_container_width=True)
