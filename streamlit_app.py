import numpy as np
import pandas as pd
import streamlit as st

# --- STREAMLIT-SIVUN ASETUKSET ---
st.set_page_config(page_title="Toto85 Quant Simulaattori", layout="wide")

st.title("🐎 Toto85 - Täydellinen Voittosimulaattori & Quant Dashboard")
st.caption("Monte Carlo -pohjainen EV+ ja peliarvo-analysaattori (8 lähtöä / V85-1 – V85-8)")

# --- SIVUPALKKI: ASETUKSET ---
st.sidebar.header("⚙️ Simulaation Säätimet")
n_simulations = st.sidebar.slider("Monte Carlo -kierrokset", 10000, 100000, 50000, step=10000)
spets_bias = st.sidebar.slider("Ratakohtainen Spets-lisäkerroin", 1.00, 1.30, 1.15, step=0.05)

# --- KOKO V85-AINEISTO (LÄHDÖT V85-1 – V85-8) ---
data = [
    # =============== V85-1 ===============
    {"Kohde": "V85-1", "Nro": 3, "Hevonen": "Nilla Lane", "Veikkaus_%": 76.0, "Bonus": 1.18, "Perustelu": "Rautainen Pankki, spets & kengättä"},
    {"Kohde": "V85-1", "Nro": 1, "Hevonen": "Panthere d'Inverne", "Veikkaus_%": 10.0, "Bonus": 1.00, "Perustelu": "B-varmistus sisäradalta"},
    {"Kohde": "V85-1", "Nro": 2, "Hevonen": "Fantastica Doda", "Veikkaus_%": 6.0, "Bonus": 1.02, "Perustelu": "Keulasta selkään, C-yllättäjä"},

    # =============== V85-2 ===============
    {"Kohde": "V85-2", "Nro": 7, "Hevonen": "Hawk Eyed Girl", "Veikkaus_%": 23.0, "Bonus": 1.25, "Perustelu": "🔥 HUIPPU EV+ Spets & Barfota"},
    {"Kohde": "V85-2", "Nro": 2, "Hevonen": "Polly Vici", "Veikkaus_%": 28.0, "Bonus": 0.85, "Perustelu": "Ylipelattu suosikki"},
    {"Kohde": "V85-2", "Nro": 12, "Hevonen": "Call Me Ottilia", "Veikkaus_%": 4.0, "Bonus": 1.15, "Perustelu": "C-Yllättäjä rycktussar"},
    {"Kohde": "V85-2", "Nro": 9, "Hevonen": "Mahakala", "Veikkaus_%": 10.0, "Bonus": 1.08, "Perustelu": "EV+ Nousukuntoinen"},

    # =============== V85-3 ===============
    {"Kohde": "V85-3", "Nro": 3, "Hevonen": "Veritas", "Veikkaus_%": 39.0, "Bonus": 0.95, "Perustelu": "Pääsuosikki"},
    {"Kohde": "V85-3", "Nro": 6, "Hevonen": "Rip Wheeler", "Veikkaus_%": 5.0, "Bonus": 1.30, "Perustelu": "💣 VARUSTEPOMMI / Barfota runt om"},
    {"Kohde": "V85-3", "Nro": 1, "Hevonen": "Helan Går", "Veikkaus_%": 17.0, "Bonus": 1.10, "Perustelu": "A / EV+ Sisärata"},
    {"Kohde": "V85-3", "Nro": 2, "Hevonen": "Wiener Sängerknabe", "Veikkaus_%": 4.0, "Bonus": 1.15, "Perustelu": "Yllättäjä haku"},

    # =============== V85-4 ===============
    {"Kohde": "V85-4", "Nro": 12, "Hevonen": "Chat Room", "Veikkaus_%": 30.0, "Bonus": 1.05, "Perustelu": "Vahva suosikki"},
    {"Kohde": "V85-4", "Nro": 13, "Hevonen": "Barkley", "Veikkaus_%": 15.0, "Bonus": 1.20, "Perustelu": "A / EV+ Berglundin u-hevonen"},
    {"Kohde": "V85-4", "Nro": 1, "Hevonen": "Mister Navajo", "Veikkaus_%": 4.0, "Bonus": 1.12, "Perustelu": "EV+ Yllättäjä"},

    # =============== V85-5 ===============
    {"Kohde": "V85-5", "Nro": 1, "Hevonen": "Richmond", "Veikkaus_%": 25.0, "Bonus": 1.05, "Perustelu": "A-ryhmä"},
    {"Kohde": "V85-5", "Nro": 3, "Hevonen": "Elroy Face", "Veikkaus_%": 25.0, "Bonus": 1.12, "Perustelu": "A / Hienossa iskussa"},
    {"Kohde": "V85-5", "Nro": 12, "Hevonen": "Hard Rock", "Veikkaus_%": 16.0, "Bonus": 1.08, "Perustelu": "B-varmistus"},

    # =============== V85-6 ===============
    {"Kohde": "V85-6", "Nro": 7, "Hevonen": "Tvingens Calippo", "Veikkaus_%": 46.0, "Bonus": 1.02, "Perustelu": "Vahva suosikki"},
    {"Kohde": "V85-6", "Nro": 2, "Hevonen": "Datos Rainbow", "Veikkaus_%": 13.0, "Bonus": 1.22, "Perustelu": "🔥 HUIPPU EV+ Djuse / Redén"},
    {"Kohde": "V85-6", "Nro": 1, "Hevonen": "Wannabe Zaz", "Veikkaus_%": 14.0, "Bonus": 1.10, "Perustelu": "Spets-haku"},

    # =============== V85-7 ===============
    {"Kohde": "V85-7", "Nro": 3, "Hevonen": "Diva Ek", "Veikkaus_%": 51.0, "Bonus": 1.00, "Perustelu": "Kultadivisioonan keulapiikki"},
    {"Kohde": "V85-7", "Nro": 5, "Hevonen": "Kentucky River", "Veikkaus_%": 11.0, "Bonus": 1.25, "Perustelu": "🔥 HUIPPU EV+ Kirikone"},
    {"Kohde": "V85-7", "Nro": 12, "Hevonen": "A Fair Day", "Veikkaus_%": 24.0, "Bonus": 1.02, "Perustelu": "Luokkahevonen taka-alalta"},

    # =============== V85-8 ===============
    {"Kohde": "V85-8", "Nro": 6, "Hevonen": "Nickel Occagnes", "Veikkaus_%": 51.0, "Bonus": 1.00, "Perustelu": "Päätöslähdön suosikki"},
    {"Kohde": "V85-8", "Nro": 5, "Hevonen": "Gustav Simoni", "Veikkaus_%": 16.0, "Bonus": 1.20, "Perustelu": "EV+ Lövgrenin luokkamenijä"},
    {"Kohde": "V85-8", "Nro": 12, "Hevonen": "Black Fire", "Veikkaus_%": 4.0, "Bonus": 1.25, "Perustelu": "🔥 HUIPPU EV+ Jättiyllättäjä"}
]

df_raw = pd.DataFrame(data)

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
            ev_pool = round(sim_pct / peli_pct, 2) if peli_pct > 0 else 0
            raja_k = round(100 / sim_pct, 2) if sim_pct > 0 else 999.0
            
            if ev_pool >= 1.20:
                tila = "🔥 HUIPPU EV+"
            elif ev_pool >= 1.05:
                tila = "✅ EV+"
            elif ev_pool >= 0.85:
                tila = "⚪ Neutraali"
            else:
                tila = "❌ Ylipelattu"

            results.append({
                "Kohde": row['Kohde'],
                "Nro": row['Nro'],
                "Hevonen": row['Hevonen'],
                "Veikkaus %": f"{row['Veikkaus_%']:.1f}%",
                "Simuloitu %": f"{sim_pct:.1f}%",
                "Raja-Kerroin": raja_k,
                "EV-Pooli": ev_pool,
                "Tila": tila,
                "Perustelu": row['Perustelu']
            })
            
    return pd.DataFrame(results)

# --- AJO PAINIKE JA TULOSTUS ---
if st.button("🚀 AJA MONTE CARLO -SIMULAATIO", type="primary"):
    df_res = run_monte_carlo(df_raw, n_simulations, spets_bias)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Simuloidut kierrokset", f"{n_simulations:,}".replace(",", " "))
    col2.metric("Löydetyt EV+ Kohteet", len(df_res[df_res["EV-Pooli"] >= 1.05]))
    col3.metric("Löydetyt Jätti-EV+ Kohteet", len(df_res[df_res["EV-Pooli"] >= 1.20]))
    
    st.markdown("---")
    st.subheader("📊 Simulaation Tulokset Lähdöittäin")
    
    st.dataframe(
        df_res.style.highlight_max(axis=0, subset=["EV-Pooli"], color="#d4edda"),
        use_container_width=True,
        height=600
    )
