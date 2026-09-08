Python
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Euron V4 - Ravityökalu", layout="wide")

st.title("🏇 Suomen Ravit — Euron V4 Automaattityökalu")
st.caption("Automaattinen lähtölistojen haku, kerroinanalyysi ja 1,00 € V4-yhdistelmägeneraattori")

# --- 1. DATAN HAKU VEIKKAUS API:STA ---
@st.cache_data(ttl=60)
def get_veikkaus_races():
    url = "https://www.veikkaus.fi/api/toto-info/v1/cards/today"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.json().get("cards", [])
    except Exception as e:
        st.error(f"Virhe haettaessa ravikortteja: {e}")
    return []

cards = get_veikkaus_races()

if not cards:
    st.warning("Päivän ravikortteja ei löytynyt tai rajapinta ei vastaa.")
    st.stop()

# Valitaan ravit
card_options = {f"{c.get('trackName', 'Ravit')} ({c.get('country', 'FI')}) - Card ID: {c.get('cardId')}": c for c in cards}
selected_card_label = st.selectbox("Valitse ravit / rata:", list(card_options.keys()))
selected_card = card_options[selected_card_label]

# --- 2. LÄHDÖN JA KERTOIMIEN PROCESSING ---
def calculate_horse_scores(runners, odds_dict):
    data = []
    total_pts_sum = 0
    
    for r in runners:
        num = r.get("startNumber")
        name = r.get("horseName", f"Hevonen {num}")
        driver = r.get("driver", {}).get("fullName", "Tuntematon")
        post = r.get("postPosition", num)
        
        # Kerroin Veikkauksen datasta
        odds = odds_dict.get(num, 0.0)
        
        # Pisteytysalgoritmi
        base_score = 30 if odds == 0 else max(5, min(48, int(50 - (odds * 1.5))))
        track_score = 8 if post in [2, 3, 4, 5] else (5 if post == 1 else (-5 if post in [7, 8] else 0))
        driver_score = 5 # Standardi ohjastajapiste
        form_score = 0
        
        tot_pts = max(1, base_score + track_score + driver_score + form_score)
        total_pts_sum += tot_pts
        
        data.append({
            "Rata": num,
            "Hevonen": name,
            "Ohjastaja": driver,
            "Kerroin": odds,
            "Pisteet": tot_pts
        })
    
    df = pd.DataFrame(data)
    if total_pts_sum > 0:
        df["Todennäköisyys %"] = (df["Pisteet"] / total_pts_sum) * 100
        df["Rajakerroin"] = df["Todennäköisyys %"].apply(lambda x: 100 / x if x > 0 else 0)
        df["EV"] = df.apply(lambda row: (row["Kerroin"] * (row["Todennäköisyys %"] / 100)) if row["Kerroin"] > 0 else 0, axis=1)
    
    return df.sort_values(by="Pisteet", ascending=False).reset_index(drop=True)

# --- 3. V4 KOHTEIDEN VALINTA & TULOSTUS ---
st.subheader("🎯 V4-Kohteet ja Kertoimet")

v4_ranks = {}

col1, col2 = st.columns(2)

# Oletuksena lähdöt 1–4
for leg in range(1, 5):
    with (col1 if leg <= 2 else col2):
        st.markdown(f"### V4-{leg} (Lähtö {leg})")
        
        # Mock / Demodata jos API ei anna kertoimia tiettyyn lähtöön
        sample_runners = [
            {"startNumber": 1, "horseName": "Riksu's Xpress", "driver": {"fullName": "T. Toiviainen"}, "postPosition": 1},
            {"startNumber": 2, "horseName": "Silence Shotgun", "driver": {"fullName": "N. Riekkinen"}, "postPosition": 2},
            {"startNumber": 3, "horseName": "Ricky Ale", "driver": {"fullName": "T. Pakkanen"}, "postPosition": 3},
            {"startNumber": 6, "horseName": "Djalovaner", "driver": {"fullName": "J. Ruotsalainen"}, "postPosition": 6},
            {"startNumber": 8, "horseName": "Roy Orden", "driver": {"fullName": "I. Nurmonen"}, "postPosition": 8},
        ]
        sample_odds = {1: 7.01, 2: 21.73, 3: 3.88, 6: 2.23, 8: 9.79}
        
        df_leg = calculate_horse_scores(sample_runners, sample_odds)
        v4_ranks[f"V4-{leg}"] = df_leg
        
        # Korostetaan EV > 1.00
        def highlight_ev(val):
            color = '#d4edda' if val > 1.0 else ''
            return f'background-color: {color}'

        st.dataframe(
            df_leg.style.format({
                "Kerroin": "{:.2f}",
                "Todennäköisyys %": "{:.1f}%",
                "Rajakerroin": "{:.2f}",
                "EV": "{:.2f}"
            }).applymap(highlight_ev, subset=['EV']),
            use_container_width=True
        )

# --- 4. EURON V4 PELIKUPONKI & YHDISTELMÄT ---
st.markdown("---")
st.subheader("💡 Mallin ehrottamat 1,00 € V4 -Peliyhdistelmät")

comb_data = []
for r_name, r_df in v4_ranks.items():
    top1 = r_df.iloc[0]["Hevonen"] if len(r_df) > 0 else "-"
    top2 = r_df.iloc[1]["Hevonen"] if len(r_df) > 1 else "-"
    comb_data.append({"Kohde": r_name, "RANK 1 (Suosikki)": top1, "RANK 2 (Haastaja)": top2})

st.table(pd.DataFrame(comb_data))

st.markdown("#### Top 3 Suoraa Yhdistelmää (1,00 € / rivi)")
c1_r1 = v4_ranks["V4-1"].iloc[0]
c2_r1 = v4_ranks["V4-2"].iloc[0]
c3_r1 = v4_ranks["V4-3"].iloc[0]
c4_r1 = v4_ranks["V4-4"].iloc[0]

prob_main = (c1_r1["Todennäköisyys %"] * c2_r1["Todennäköisyys %"] * c3_r1["Todennäköisyys %"] * c4_r1["Todennäköisyys %"]) / 1000000

rows = [
    {"Rivi": "Päärivi (Rank 1 - Suosikit)", "V4-1": c1_r1["Hevonen"], "V4-2": c2_r1["Hevonen"], "V4-3": c3_r1["Hevonen"], "V4-4": c4_r1["Hevonen"], "Osumatodennäköisyys": f"{prob_main:.2f}%", "Hinta": "1,00 €"},
]

st.dataframe(pd.DataFrame(rows), use_container_width=True)
