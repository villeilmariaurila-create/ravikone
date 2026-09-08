import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime

st.set_page_config(page_title="1 € V4 - Ravityökalu", layout="wide")

st.title("🏇 Pohjoismaiset Ravit — 1,00 € V4 Automaattityökalu")
st.caption("Automaattinen lähtölistojen haku, kerroinanalyysi ja 1,00 € V4-yhdistelmägeneraattori")

# --- 1. PÄIVÄMÄÄRÄN JA RAVIRADAN VALINTA ---
col_date, col_select = st.columns([1, 2])

with col_date:
    selected_date = st.date_input("Valitse päivämäärä:", date.today())

date_str = selected_date.strftime("%Y-%m-%d")

@st.cache_data(ttl=30)
def fetch_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

# Haetaan valitun päivämäärän kaikki ravikortit Veikkaukselta
cards_data = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/date/{date_str}")
if not cards_data or not cards_data.get("cards"):
    # Jos päivämäärähaku ei palauta, kokeillaan yleistä tänään-rajapintaa
    cards_data = fetch_json("https://www.veikkaus.fi/api/toto-info/v1/cards/today")

cards = cards_data.get("cards", []) if cards_data else []

if not cards:
    st.warning(f"Ei ravipäiviä tai kertoimia saatavilla valitulle päivälle ({date_str}). Kokeile toista päivämäärää kalenterista.")
    st.stop()

card_options = {}
for c in cards:
    track = c.get("trackName", "Tuntematon rada")
    country = c.get("country", "")
    card_id = c.get("cardId")
    label = f"{track} ({country}) — Kortti ID: {card_id}"
    card_options[label] = c

with col_select:
    selected_label = st.selectbox("Valitse ravit / rada:", list(card_options.keys()))

selected_card = card_options[selected_label]
card_id = selected_card.get("cardId")

# --- 2. LÄHTÖLISTOJEN JA KERTOIMIEN HAKU ---
card_detail = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/{card_id}")
races = card_detail.get("races", []) if card_detail else []

odds_data = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/odds/v1/card/{card_id}/VOITTAJA")
odds_by_race = {}
if odds_data and "odds" in odds_data:
    for item in odds_data.get("odds", []):
        r_num = item.get("raceNumber")
        if r_num not in odds_by_race:
            odds_by_race[r_num] = {}
        for runner_odds in item.get("runnerOdds", []):
            runner_num = runner_odds.get("runnerNumber")
            raw_odds = runner_odds.get("odds", 0) / 100.0
            odds_by_race[r_num][runner_num] = raw_odds

# --- 3. LASKENTA ALGORITMI ---
def calculate_scores(runners, odds_map):
    data = []
    total_pts_sum = 0
    
    for r in runners:
        num = r.get("startNumber")
        name = r.get("horseName", f"Hevonen {num}")
        driver = r.get("driver", {}).get("fullName", "Tuntematon")
        post = r.get("postPosition", num)
        
        odds = odds_map.get(num, 0.0)
        
        base_score = 30 if odds == 0 else max(5, min(48, int(50 - (odds * 1.5))))
        track_score = 8 if post in [2, 3, 4, 5] else (5 if post == 1 else (-5 if post in [7, 8] else 0))
        driver_score = 5
        
        tot_pts = max(1, base_score + track_score + driver_score)
        total_pts_sum += tot_pts
        
        data.append({
            "Rata": num,
            "Hevonen": name,
            "Ohjastaja": driver,
            "Kerroin": odds,
            "Pisteet": tot_pts
        })
    
    df = pd.DataFrame(data)
    if not df.empty and total_pts_sum > 0:
        df["Todennäköisyys %"] = (df["Pisteet"] / total_pts_sum) * 100
        df["Rajakerroin"] = df["Todennäköisyys %"].apply(lambda x: 100 / x if x > 0 else 0)
        df["EV"] = df.apply(lambda row: (row["Kerroin"] * (row["Todennäköisyys %"] / 100)) if row["Kerroin"] > 0 else 0, axis=1)
    
    return df.sort_values(by="Pisteet", ascending=False).reset_index(drop=True)

# --- 4. TULOSTUS KÄYTTÖLIITTYMÄÄN ---
st.subheader(f"🎯 {selected_card.get('trackName')} — Lähtökohtaiset Kertoimet ja Analyysi")

v4_ranks = {}
col1, col2 = st.columns(2)

# Näytetään 4 ensimmäistä lähtöä (tai V4-lähdöt)
target_races = races[:4]

for idx, race in enumerate(target_races, start=1):
    r_num = race.get("raceNumber")
    runners = race.get("runners", [])
    r_odds = odds_by_race.get(r_num, {})
    
    df_leg = calculate_scores(runners, r_odds)
    v4_ranks[f"V4-{idx}"] = df_leg
    
    with (col1 if idx <= 2 else col2):
        st.markdown(f"### Lähtö {r_num} ({race.get('distance', '')} m)")
        
        def highlight_ev(val):
            color = '#d4edda' if val > 1.0 else ''
            return f'background-color: {color}'

        st.dataframe(
            df_leg.style.format({
                "Kerroin": "{:.2f}",
                "Todennäköisyys %": "{:.1f}%",
                "Rajakerroin": "{:.2f}",
                "EV": "{:.2f}"
            }).map(highlight_ev, subset=['EV']),
            use_container_width=True
        )

# --- 5. 1,00 € V4 -GENERAATTORI ---
st.markdown("---")
st.subheader("💡 Mallin ehdottama 1,00 € V4 -Päärivi")

comb_data = []
for r_name, r_df in v4_ranks.items():
    if not r_df.empty:
        top1 = r_df.iloc[0]["Hevonen"]
        top2 = r_df.iloc[1]["Hevonen"] if len(r_df) > 1 else "-"
    else:
        top1, top2 = "-", "-"
    comb_data.append({"Kohde": r_name, "RANK 1 (Suosikki)": top1, "RANK 2 (Haastaja)": top2})

st.table(pd.DataFrame(comb_data))
