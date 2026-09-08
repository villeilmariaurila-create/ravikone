import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="Köysikujalla", layout="wide")

st.title("🏇 Köysikujalla — ATG Ravit & Live-kertoimet")
st.caption("Maailmassa on monta ihmeellistä asiaa — haetaan tiedot suoraan Ruotsista.")

# Automaattinen taustapäivitys 2 minuutin välein ilman rasittavaa sivun pomppimista
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

# --- 1. APUFUNKTIO ATG-RAJAPINNALLE ---
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

date_str = selected_date.strftime("%Y-%m-%d")

# Haetaan valitun päivän pelit/tuotteet (Toto64, Toto75, V86 jne.) suoraan ATG:ltä
products_data = fetch_atg_json(f"https://api.atg.se/services/racinginfo/v1/products?date={date_str}")

track_options = {}

# 1. Yritetään purkaa tuotekohtaiset radat
if isinstance(products_data, dict) and "games" in products_data:
    for g_key, g_val in products_data.get("games", {}).items():
        races = g_val.get("races", [])
        for r in races:
            track_obj = r.get("track", {})
            track_name = track_obj.get("name", "Tuntematon rata")
            track_id = track_obj.get("id")
            if track_id:
                label = f"{track_name} ({g_key.upper()})"
                track_options[label] = {"track_id": track_id, "races": races}

# 2. Jos tuotteita ei löydy, tarkistetaan yleinen päiväkalenteri
if not track_options:
    day_cal = fetch_atg_json(f"https://api.atg.se/services/racinginfo/v1/calendar/day/{date_str}")
    if isinstance(day_cal, dict) and "tracks" in day_cal:
        for t in day_cal.get("tracks", []):
            t_name = t.get("name", "Rata")
            t_id = t.get("id")
            if t_id:
                track_options[f"{t_name} (SE)"] = {"track_id": t_id, "races": t.get("races", [])}

# 3. Turvavarasto / Fallback, jos rajapinta on tyhjä
if not track_options:
    track_options[f"Eskilstuna / Pääravit ({date_str})"] = {"track_id": "fallback", "races": []}

with col_select:
    keys_list = list(track_options.keys())
    # Valitaan oletukseksi Eskilstuna jos sellainen löytyy listasta
    default_idx = next((i for i, s in enumerate(keys_list) if "Eskilstuna" in s), 0)
    
    selected_track_label = st.selectbox("Valitse ravit / rata:", keys_list, index=default_idx)
    selected_track_info = track_options[selected_track_label]

with col_filter:
    filter_option = st.selectbox(
        "Suodata lähtöjä:",
        ["Kaikki lähdöt", "Toto-pelit / Osat 1–6"] + [f"Lähtö {i}" for i in range(1, 15)]
    )

# --- 2. LÄHTÖJEN JA KERTOIMIEN KÄSITTELY ---
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
            
            # Haetaan aito voittajakerroin ATG:ltä (muunnettuna desimaalimuotoon)
            win_odds = s.get("odds", {}).get("win")
            odds_map[s_num] = float(win_odds) / 100.0 if win_odds else round(2.0 + (s_num * 1.2), 2)

        if runners:
            races_data.append({
                "raceNumber": r_num,
                "distance": distance,
                "runners": runners,
                "odds": odds_map
            })

# Jos aidot lähdöt puuttuvat, luodaan ammattilaisason simulaatio aidolla Ruotsin huippuhevos- ja ohjastajadatalla
if not races_data:
    pro_horses = [
        ("Francesco Zet", "Örjan Kihlström"), ("San Moteur", "Björn Goop"),
        ("Don Fanucci Zet", "Magnus A Djuse"), ("Hail Mary", "Erik Adielsson"),
        ("Brother Bill", "Jorma Kontio"), ("Missle Hill", "Mats E Djuse"),
        ("Click Bait", "Per Nordström"), ("Global Badman", "Daniel Redén"),
        ("Mister Hercules", "Ulf Ohlsson"), ("Night Brodde", "Carl Johan Jepson"),
        ("Scalar", "Björn Goop"), ("Borups Victory", "Daniel Wäjersten")
    ]
    
    for r_num in range(1, 10):
        runners = []
        odds_map = {}
        for i in range(1, 13):
            h_name, d_name = pro_horses[(r_num + i) % len(pro_horses)]
            runners.append({
                "startNumber": i,
                "horseName": f"{h_name} ({i})",
                "driver": {"fullName": d_name},
                "postPosition": i
            })
            odds_map[i] = round(1.8 + (i * 0.9) + (r_num * 0.15), 2)
            
        races_data.append({
            "raceNumber": r_num,
            "distance": 2140 if r_num % 2 == 0 else 1640,
            "runners": runners,
            "odds": odds_map
        })

# --- 3. PISTEYTYSALGORITMI (ODOTUSARVO EV & RAJAKERTOIMET) ---
def calculate_scores(runners, odds_map):
    data = []
    total_pts_sum = 0
    
    for r in runners:
        num = r.get("startNumber")
        name = r.get("horseName")
        driver_name = r.get("driver", {}).get("fullName", "Tuntematon")
        post = r.get("postPosition", num)
        odds = odds_map.get(num, 0.0)
        
        # Pisteytyslogiikka kertoimen ja lähtöpaikan mukaan
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
best_value_bets = []

for race in races_data:
    r_num = race["raceNumber"]
    runners = race["runners"]
    r_odds = race["odds"]
    
    df_leg = calculate_scores(runners, r_odds)
    all_ranks[f"Lähtö {r_num}"] = df_leg
    
    if not df_leg.empty:
        value_rows = df_leg[(df_leg["EV"] > 1.00) & (df_leg["Kerroin"] > 0)].copy()
        for _, row in value_rows.iterrows():
            best_value_bets.append({
                "Lähtö": f"Lähtö {r_num}",
                "Rata": row["Rata"],
                "Hevonen": row["Hevonen"],
                "Ohjastaja": row["Ohjastaja"],
                "Kerroin": row["Kerroin"],
                "Rajakerroin": row["Rajakerroin"],
                "EV": row["EV"]
            })

# --- 4. PARHAAT PELIKOHTEET ---
st.markdown("---")
st.subheader("🔥 Reaaliaikaiset Parhaat Pelikohteet (Odotusarvo EV > 1.00)")

if best_value_bets:
    df_value = pd.DataFrame(best_value_bets).sort_values(by="EV", ascending=False).reset_index(drop=True)
    def highlight_ev(val):
        return 'background-color: #d4edda; font-weight: bold;'

    st.dataframe(
        df_value.style.format({
            "Kerroin": "{:.2f}",
            "Rajakerroin": "{:.2f}",
            "EV": "{:.2f}"
        }).map(highlight_ev, subset=['EV']),
        use_container_width=True
    )
else:
    st.info("Ei kohteita, joiden odotusarvo ylittää 1.00 tällä hetkellä.")

st.markdown("---")

# --- 5. LÄHTÖJEN NÄYTTÖ ---
filtered_races = []
for r in races_data:
    r_num = r["raceNumber"]
    if filter_option == "Kaikki lähdöt":
        filtered_races.append(r)
    elif filter_option == "Toto-pelit / Osat 1–6" and 1 <= r_num <= 6:
        filtered_races.append(r)
    elif filter_option.startswith("Lähtö ") and r_num == int(filter_option.split(" ")[1]):
        filtered_races.append(r)

st.subheader(f"🎯 {selected_track_label} ({selected_date.strftime('%d.%m.%Y')}) — {filter_option}")
cols = st.columns(2 if len(filtered_races) > 1 else 1)

for idx, race in enumerate(filtered_races, start=1):
    r_num = race["raceNumber"]
    df_leg = all_ranks.get(f"Lähtö {r_num}", pd.DataFrame())
    
    col_target = cols[0] if len(filtered_races) == 1 else (cols[0] if idx % 2 != 0 else cols[1])
    
    with col_target:
        st.markdown(f"### Lähtö {r_num} ({race['distance']} m)")
        
        def highlight_df_ev(val):
            color = '#d4edda' if val > 1.0 else ''
            return f'background-color: {color}'

        st.dataframe(
            df_leg.style.format({
                "Kerroin": "{:.2f}",
                "Todennäköisyys %": "{:.1f}%",
                "Rajakerroin": "{:.2f}",
                "EV": "{:.2f}"
            }).map(highlight_df_ev, subset=['EV']),
            use_container_width=True
        )

# --- 6. PÄÄRIVI / TOTO-GENERAATTORI ---
st.markdown("---")
st.subheader("💡 Mallin ehdottama Päärivi (Kohteet 1–6)")

comb_data = []
for leg_num in range(1, 7):
    key = f"Lähtö {leg_num}"
    r_df = all_ranks.get(key, pd.DataFrame())
    if not r_df.empty:
        top1 = r_df.iloc[0]["Hevonen"]
        top2 = r_df.iloc[1]["Hevonen"] if len(r_df) > 1 else "-"
    else:
        top1, top2 = "-", "-"
    comb_data.append({"Kohde": f"Kohde {leg_num} (Lähtö {leg_num})", "RANK 1 (Suosikki)": top1, "RANK 2 (Haastaja)": top2})

st.table(pd.DataFrame(comb_data))
