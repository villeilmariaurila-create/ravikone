import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="Köysikujalla", layout="wide")
st.title("🏇 Köysikujalla — ATG Ravit & Live-kertoimet")

@st.cache_data(ttl=30)
def fetch_atg_json(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        st.error(f"Virhe haettaessa dataa: {e}")
    return None

selected_date = st.date_input("Valitse päivämäärä:", date.today())
date_str = selected_date.strftime("%Y-%m-%d")

# Käytetään suoraan päiväkalenterin rajapintaa, joka palauttaa kyseisen päivän radat ja lähdöt
url = f"https://www.atg.se/services/racinginfo/v1/calendar/day/{date_str}"
data = fetch_atg_json(url)

track_options = {}

if data and isinstance(data, dict):
    # Kalenteri palauttaa radat "tracks"-listassa
    tracks = data.get("tracks", [])
    for t in tracks:
        t_name = t.get("name", "Tuntematon rata")
        t_id = t.get("id")
        races = t.get("races", [])
        if t_id and races:
            label = f"{t_name} ({len(races)} lähtöä)"
            track_options[label] = {
                "track_id": t_id,
                "races": races
            }

col1, col2 = st.columns([2, 2])

with col1:
    if track_options:
        selected_label = st.selectbox("Valitse rata:", list(track_options.keys()))
        selected_data = track_options[selected_label]
    else:
        st.selectbox("Valitse rata:", ["Ei raveja tälle päivälle"])
        selected_data = {"track_id": None, "races": []}

races_list = selected_data.get("races", [])

with col2:
    available_races = [f"Lähtö {r.get('raceNumber', i+1)}" for i, r in enumerate(races_list)]
    filter_option = st.selectbox("Suodata lähtöä:", ["Kaikki lähdöt"] + available_races)

st.markdown("---")

if not races_list:
    st.warning(f"Valitsemallesi päivälle ({selected_date.strftime('%d.%m.%Y')}) ei löytynyt ratoja tai lähtölistoja ATG:n kalenterista.")
else:
    race_rankings = {}

    for race in races_list:
        r_num = race.get("raceNumber", 1)
        runners_data = []
        total_pts_sum = 0
        
        for s in race.get("starts", []):
            s_num = s.get("number", 1)
            horse_name = s.get("horse", {}).get("name", f"Hevonen {s_num}")
            
            driver = s.get("driver", {})
            driver_name = f"{driver.get('firstName', '')} {driver.get('lastName', '')}".strip() or "Tuntematon"
            post_pos = s.get("postPosition", s_num)
            
            win_odds_raw = s.get("odds", {}).get("win")
            odds = float(win_odds_raw) / 100.0 if win_odds_raw else 0.0
            
            base_score = 30 if odds == 0 else max(5, min(50, int(50 - (odds * 1.2))))
            track_score = 6 if post_pos in [2, 3, 4, 5] else (3 if post_pos == 1 else -4)
            tot_pts = max(1, base_score + track_score)
            total_pts_sum += tot_pts
            
            runners_data.append({
                "Rata": s_num,
                "Hevonen": horse_name,
                "Ohjastaja": driver_name,
                "Paikka": post_pos,
                "Kerroin": odds,
                "Pisteet": tot_pts
            })
            
        df = pd.DataFrame(runners_data)
        if not df.empty and total_pts_sum > 0:
            df["Todennäköisyys %"] = (df["Pisteet"] / total_pts_sum) * 100
            df["Rajakerroin"] = df["Todennäköisyys %"].apply(lambda x: 100 / x if x > 0 else 0)
            df["EV"] = df.apply(lambda row: (row["Kerroin"] * (row["Todennäköisyys %"] / 100)) if row["Kerroin"] > 0 else 0, axis=1)
            df = df.sort_values(by="Pisteet", ascending=False).reset_index(drop=True)
            race_rankings[r_num] = df

    # --- PÄIVÄN DUO -SUOSITUS ---
    sorted_race_nums = sorted(race_rankings.keys())
    if len(sorted_race_nums) >= 2:
        duo_race1 = sorted_race_nums[-2]
        duo_race2 = sorted_race_nums[-1]
        
        df_d1 = race_rankings.get(duo_race1, pd.DataFrame())
        df_d2 = race_rankings.get(duo_race2, pd.DataFrame())
        
        if not df_d1.empty and not df_d2.empty:
            st.subheader("🎯 Päivän Duo -suositus (Mallin ykkösvalinnat)")
            d_col1, d_col2 = st.columns(2)
            
            with d_col1:
                top_h1 = df_d1.iloc[0]
                st.markdown(f"**Duo 1 (Lähtö {duo_race1})**")
                st.info(f"🐎 **{top_h1['Hevonen']}** (Rata {top_h1['Rata']})\n\nOhjastaja: {top_h1['Ohjastaja']} | Kerroin: {top_h1['Kerroin']:.2f}")
                
            with d_col2:
                top_h2 = df_d2.iloc[0]
                st.markdown(f"**Duo 2 (Lähtö {duo_race2})**")
                st.info(f"🐎 **{top_h2['Hevonen']}** (Rata {top_h2['Rata']})\n\nOhjastaja: {top_h2['Ohjastaja']} | Kerroin: {top_h2['Kerroin']:.2f}")
            st.markdown("---")

    # Suodatetaan ja näytetään lähdöt
    filtered_races = []
    for r in races_list:
        r_num = r.get("raceNumber", 1)
        if filter_option == "Kaikki lähdöt" or filter_option == f"Lähtö {r_num}":
            filtered_races.append(r)

    for race in filtered_races:
        r_num = race.get("raceNumber", 1)
        distance = race.get("distance", 2140)
        
        st.subheader(f"Lähtö {r_num} ({distance} m)")
        df = race_rankings.get(r_num, pd.DataFrame())
        
        if not df.empty:
            def highlight_ev(val):
                return 'background-color: #d4edda;' if val > 1.0 else ''

            st.dataframe(
                df.style.format({
                    "Kerroin": "{:.2f}",
                    "Todennäköisyys %": "{:.1f}%",
                    "Rajakerroin": "{:.2f}",
                    "EV": "{:.2f}"
                }).map(highlight_ev, subset=['EV']),
                use_container_width=True
            )
        else:
            st.info("Ei osallistujatietoja saatavilla tälle lähdölle.")
