import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="Köysikujalla", layout="wide")

st.title("🏇 Köysikujalla")
st.caption("Automaattinen lähtölistojen haku, kerroinanalyysi ja 1,00 € V4/V85-yhdistelmägeneraattori")

# --- 1. PÄIVÄMÄÄRÄN JA RAVIRADAN VALINTA ---
col_date, col_select = st.columns([1, 2])

with col_date:
    selected_date = st.date_input("Valitse päivämäärä:", date.today())

date_str = selected_date.strftime("%Y-%m-%d")

@st.cache_data(ttl=60)
def fetch_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

# Haetaan Veikkaukselta päivän kortit
cards_data = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/date/{date_str}")
cards = cards_data.get("cards", []) if isinstance(cards_data, dict) else []

card_options = {
    "🇸🇪 Hagmyren (Ruotsi Mallinnus - Lähdöt 1-13)": "MOCK_HAGMYREN"
}

if cards:
    for c in cards:
        track = c.get("trackName", "Tuntematon rada")
        country = c.get("country", "")
        card_id = c.get("cardId")
        label = f"{track} ({country}) — Kortti ID: {card_id}"
        card_options[label] = c

with col_select:
    selected_label = st.selectbox("Valitse ravit / rada:", list(card_options.keys()))

selected_card = card_options[selected_label]

# --- 2. APUFUNKTIOT JA MALLIDATA ---
def calculate_scores(runners, odds_map):
    data = []
    total_pts_sum = 0
    
    for r in runners:
        num = r.get("startNumber")
        name = r.get("horseName", f"Hevonen {num}")
        driver = r.get("driver", {}).get("fullName", "Tuntematon")
        post = r.get("postPosition", num)
        
        odds = odds_map.get(num, 0.0)
        
        # Pisteytyslogiikka
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

# Generoidaan Ruotsin Hagmyren Mallipohja Lähdöille 1-13
def get_mock_races():
    mock_races = []
    horse_names = [
        ["Haylee Eagra", "Memory of China", "Freja Hammering", "Whysoserious", "Hervey Island", "Joyful Godiva", "Gaya Vendil", "Cocktail Spirit", "Green Dream", "Teaberry", "Sanna Tooma", "Happy Girl"],
        ["Zeta Crown", "Stonecapes Superb", "Main Stage", "Global Dazzle", "Quick Trot", "Speedy Boy", "Iron Lady"],
        ["Make It Rain", "Consalvo", "MAS Capacity", "Ranch Kelly", "Next Direction", "Polara"],
        ["Amazing Player", "BWT Highway Star", "Run For Royalty", "Willow Pride", "Hierro Boko"],
        ["Callela Ikaros", "Atupem", "Vixus", "Parvelan Retu", "Evartti", "Stallone"],
        ["Jokivarren Kunkku", "Lissun Eerikki", "Välähdys", "Kukkarosuon Kurko", "Nyland"],
        ["Vixeli", "Hissun Turbo", "Tähen Toivomus", "Veeran Poika", "Kartier"],
        ["Aatami", "Vilju", "Humiro", "Pyöriäisen May", "Sipori"],
        ["Tango Vartti", "Suvelan Unelma", "Vesmeus", "Profin Toivo", "Sarkren Vappu"],
        ["Core", "Mascate Match", "Graceful Swamp", "Cameron Evo", "Hotshot Luca"],
        ["Workout Wonder", "Chief Beyalke", "Sobel Conway", "Dundee", "Tito C.A."],
        ["Express Duo", "Bret Boko", "Seabiscuit", "Tumble Dust", "One Too Many"],
        ["Fiolation", "Sahara One", "T.X. All In", "Shadow Of Brisbane", "Midnight Hour"]
    ]
    
    for r in range(1, 14):
        h_list = horse_names[(r - 1) % len(horse_names)]
        runners = []
        odds_map = {}
        for idx, h_name in enumerate(h_list, start=1):
            runners.append({
                "startNumber": idx,
                "horseName": h_name,
                "driver": {"fullName": f"Kuskipojat {idx}"},
                "postPosition": idx
            })
            odds_map[idx] = round(2.0 + (idx * 1.8), 2)
        
        mock_races.append({
            "raceNumber": r,
            "distance": 1640 if r % 2 != 0 else 2140,
            "runners": runners,
            "odds": odds_map
        })
    return mock_races

# --- 3. DATAN PROSESSINTI & TULOSTUS ---
if selected_card == "MOCK_HAGMYREN":
    st.info("ℹ️ Näytetään Ruotsi Hagmyren mallinnus (Lähdöt 1–13, V4 & V85/V86).")
    races_data = get_mock_races()
    track_title = "Hagmyren (Ruotsi Mallinnus)"
else:
    card_id = selected_card.get("cardId")
    card_detail = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/{card_id}")
    raw_races = card_detail.get("races", []) if isinstance(card_detail, dict) else []
    
    odds_data = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/odds/v1/card/{card_id}/VOITTAJA")
    odds_by_race = {}
    if isinstance(odds_data, dict) and "odds" in odds_data:
        for item in odds_data.get("odds", []):
            r_num = item.get("raceNumber")
            if r_num not in odds_by_race:
                odds_by_race[r_num] = {}
            for runner_odds in item.get("runnerOdds", []):
                runner_num = runner_odds.get("runnerNumber")
                odds_by_race[r_num][runner_num] = runner_odds.get("odds", 0) / 100.0
                
    races_data = []
    for r in raw_races:
        r_num = r.get("raceNumber")
        races_data.append({
            "raceNumber": r_num,
            "distance": r.get("distance", 2140),
            "runners": r.get("runners", []),
            "odds": odds_by_race.get(r_num, {})
        })
    track_title = selected_card.get('trackName', 'Ravit')

st.subheader(f"🎯 {track_title} — Lähdöt 1–13 Kertoimet & Pisteytys")

all_ranks = {}
cols = st.columns(2)

for idx, race in enumerate(races_data, start=1):
    r_num = race["raceNumber"]
    runners = race["runners"]
    r_odds = race["odds"]
    
    df_leg = calculate_scores(runners, r_odds)
    all_ranks[f"Lähtö {r_num}"] = df_leg
    
    with (cols[0] if idx % 2 != 0 else cols[1]):
        # Merkitään erikseen V4 ja V85/V86 kohteet
        v4_tag = " [V4-kohde]" if 1 <= r_num <= 4 else ""
        v85_tag = " [V85/V86-kohde]" if 5 <= r_num <= 12 else ""
        
        st.markdown(f"### Lähtö {r_num} ({race['distance']} m){v4_tag}{v85_tag}")
        
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

# --- 4. 1,00 € V4-GENERAATTORI ---
st.markdown("---")
st.subheader("💡 Mallin ehdottama 1,00 € V4 -Päärivi (Lähdöt 1–4)")

comb_data = []
for leg_num in range(1, 5):
    key = f"Lähtö {leg_num}"
    r_df = all_ranks.get(key, pd.DataFrame())
    if not r_df.empty:
        top1 = r_df.iloc[0]["Hevonen"]
        top2 = r_df.iloc[1]["Hevonen"] if len(r_df) > 1 else "-"
    else:
        top1, top2 = "-", "-"
    comb_data.append({"Kohde": f"V4-{leg_num} (Lähtö {leg_num})", "RANK 1 (Suosikki)": top1, "RANK 2 (Haastaja)": top2})

st.table(pd.DataFrame(comb_data))
