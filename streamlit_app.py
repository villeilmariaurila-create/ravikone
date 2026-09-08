import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="Köysikujalla", layout="wide")

st.title("🏇 Köysikujalla — ATG Ravit & Live-kertoimet")
st.caption("Aitojen lähtölistojen haku suoraan ATG:n rajapinnasta")

# Automaattinen taustapäivitys 2 minuutin välein
st.markdown(
    """
    <script>
        setTimeout(function(){
            window.location.reload(1);
        }, 120000);
    </script>
    """,
    unsafe_allow_html=True
)

@st.cache_data(ttl=60)
def fetch_atg_json(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

col_date, col_select, col_filter = st.columns([1, 2, 1.5])

with col_date:
    selected_date = st.date_input("Valitse päivämäärä:", date.today())

date_str = selected_date.strftime("%Y-%m-	") # Korjattu oikeaan muotoon
date_str = selected_date.strftime("%Y-%m-%d")

# Haetaan päivän virallinen kalenteri ATG:ltä
calendar_data = fetch_atg_json(f"https://api.atg.se/services/racinginfo/v1/calendar/day/{date_str}")

track_options = {}

if isinstance(calendar_data, dict) and "tracks" in calendar_data:
    for t in calendar_data.get("tracks", []):
        t_name = t.get("name", "Tuntematon rata")
        t_id = t.get("id")
        country = t.get("countryCode", "SE")
        races = t.get("races", [])
        if t_id:
            track_options[f"{t_name} ({country})"] = {"track_id": t_id, "races": races}

with col_select:
    if track_options:
        selected_track_label = st.selectbox("Valitse ravit / rata:", list(track_options.keys()))
        selected_track_info = track_options[selected_track_label]
    else:
        st.selectbox("Valitse ravit / rata:", ["Ei raveja tälle päivälle"])
        selected_track_info = {"track_id": None, "races": []}

with col_filter:
    filter_option = st.selectbox(
        "Suodata lähtöjä:",
        ["Kaikki lähdöt"] + [f"Lähtö {i}" for i in range(1, 15)]
    )

# --- LÄHTÖJEN KÄSITTELY ---
races_data = []
raw_races = selected_track_info.get("races", [])

if raw_races:
    for r_idx, r in enumerate(raw_races, start=1):
        r_num = r.get("raceNumber", r_idx)
        distance = r.get("distance", 2140)
        
        runners = []
        odds_map = {}
        starts = r.get("starts", [])
        
        for s in starts:
            s_num = s.get("number", 1)
            h_name = s.get("horse", {}).get("name", f"Hevonen {s_num}")
            driver_data = s.get("driver", {})
            d_name = f"{driver_data.get('firstName', '')} {driver_data.get('lastName', '')}".strip()
            if not d_name:
                d_name = "Tuntematon"
                
            runners.append({
                "startNumber": s_num,
                "horseName": h_name,
                "driver": {"fullName": d_name},
                "postPosition": s.get("postPosition", s_num)
            })
            
            win_odds = s.get("odds", {}).get("win")
            odds_map[s_num] = float(win_odds) / 100.0 if win_odds else 0.0

        if runners:
            races_data.append({
                "raceNumber": r_num,
                "distance": distance,
                "runners": runners,
                "odds": odds_map
            })

if not races_data:
    st.warning(f"Valitsemallesi päivälle ({selected_date.strftime('%d.%m.%Y')}) tai radalle ei löytynyt virallisia lähtölistoja ATG:n järjestelmästä.")
else:
    # Laskenta- ja näyttöosuus
    def calculate_scores(runners, odds_map):
        data = []
        total_pts_sum = 0
        
        for r in runners:
            num = r.get("startNumber")
            name = r.get("horseName")
            driver_name = r.get("driver", {}).get("fullName", "Tuntematon")
            post = r.get("postPosition", num)
            odds = odds_map.get(num, 0.0)
            
            base_score = 30 if odds == 0 else max(5, min(48, int(50 - (odds * 1.4))))
            track_score = 8 if post in [2, 3, 4, 5] else (5 if post == 1 else (-5 if post in [7, 8, 11, 12] else 0))
            driver_score = 5
            
            tot_pts = max(1, base_score + track_score + driver_score)
            total_pts_sum += tot_pts
            
            data.append({
                "Rata": num,
                "Hevonen": name,
                "Ohjastaja": driver_name,
                "Kerroin": odds,
                "Pisteet": tot_pts
            })
        
        df = pd.DataFrame(data)
        if not df.empty and total_pts_sum > 0:
            df["Todennäköisyys %"] = (df["Pisteet"] / total_pts_sum) * 100
            df["Rajakerroin"] = df["Todennäköisyys %"].apply(lambda x: 100 / x if x > 0 else 0)
            df["EV"] = df.apply(lambda row: (row["Kerroin"] * (row["Todennäköisyys %"] / 100)) if row["Kerroin"] > 0 else 0, axis=1)
        
        return df.sort_values(by="Pisteet", ascending=False).reset_index(drop=True)

    all_ranks = {}
    for race in races_data:
        r_num = race["raceNumber"]
        all_ranks[f"Lähtö {r_num}"] = calculate_scores(race["runners"], race["odds"])

    filtered_races = [r for r in races_data if filter_option == "Kaikki lähdöt" or r["raceNumber"] == int(filter_option.split(" ")[1])]

    st.subheader(f"🎯 Valitut lähdöt")
    for race in filtered_races:
        r_num = race["raceNumber"]
        st.markdown(f"### Lähtö {r_num} ({race['distance']} m)")
        st.dataframe(all_ranks.get(f"Lähtö {r_num}", pd.DataFrame()), use_container_width=True)
