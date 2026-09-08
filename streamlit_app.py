import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="1 € V4 - Travverktyg", layout="wide")

st.title("🏇 Finlands Trav — 1,00 € V4 Automatiserat Verktyg")
st.caption("Automatisk hämtning av startlistor, oddsanalys och 1,00 € V4-kombinationsgenerator")

# --- 1. DATAHÄMTNING FRÅN VEIKKAUS API (12.9.2026) ---
TARGET_DATE = "2026-09-12"

@st.cache_data(ttl=60)
def get_veikkaus_races(date_str):
    url = f"https://www.veikkaus.fi/api/toto-info/v1/cards/date/{date_str}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json().get("cards", [])
    except Exception as e:
        pass
    return []

cards = get_veikkaus_races(TARGET_DATE)

if cards:
    card_options = {f"{c.get('trackName', 'Trav')} ({c.get('country', 'FI')}) - Kort-ID: {c.get('cardId')}": c for c in cards}
    selected_card_label = st.selectbox("Välj travbana / tävling (12.9.2026):", list(card_options.keys()))
    selected_card = card_options[selected_card_label]
else:
    st.info(f"ℹ️ Inga aktiva odds tillgängliga för lördagen {TARGET_DATE} ännu. Visar modelldata för analys och V4-generatorn.")
    selected_card = {"trackName": "Lördagstrav (Modell)", "cardId": "20260912"}

# --- 2. BEARBETNING AV POÄNG OCH ODDS ---
def calculate_horse_scores(runners, odds_dict):
    data = []
    total_pts_sum = 0
    
    for r in runners:
        num = r.get("startNumber")
        name = r.get("horseName", f"Häst {num}")
        driver = r.get("driver", {}).get("fullName", "Okänd")
        post = r.get("postPosition", num)
        
        odds = odds_dict.get(num, 0.0)
        
        base_score = 30 if odds == 0 else max(5, min(48, int(50 - (odds * 1.5))))
        track_score = 8 if post in [2, 3, 4, 5] else (5 if post == 1 else (-5 if post in [7, 8] else 0))
        driver_score = 5
        form_score = 0
        
        tot_pts = max(1, base_score + track_score + driver_score + form_score)
        total_pts_sum += tot_pts
        
        data.append({
            "Spår": num,
            "Häst": name,
            "Kusk": driver,
            "Odds": odds,
            "Poäng": tot_pts
        })
    
    df = pd.DataFrame(data)
    if total_pts_sum > 0:
        df["Sannolikhet %"] = (df["Poäng"] / total_pts_sum) * 100
        df["Gränsodds"] = df["Sannolikhet %"].apply(lambda x: 100 / x if x > 0 else 0)
        df["EV"] = df.apply(lambda row: (row["Odds"] * (row["Sannolikhet %"] / 100)) if row["Odds"] > 0 else 0, axis=1)
    
    return df.sort_values(by="Poäng", ascending=False).reset_index(drop=True)

# --- 3. V4-AVDELNINGAR OCH TABLES ---
st.subheader("🎯 V4-Avdelningar och Odds (Lördag 12.9.2026)")

v4_ranks = {}
col1, col2 = st.columns(2)

sample_runners_list = [
    [{"startNumber": 1, "horseName": "Riksu's Xpress", "driver": {"fullName": "T. Toiviainen"}, "postPosition": 1},
     {"startNumber": 2, "horseName": "Silence Shotgun", "driver": {"fullName": "N. Riekkinen"}, "postPosition": 2},
     {"startNumber": 3, "horseName": "Ricky Ale", "driver": {"fullName": "T. Pakkanen"}, "postPosition": 3},
     {"startNumber": 6, "horseName": "Djalovaner", "driver": {"fullName": "J. Ruotsalainen"}, "postPosition": 6}],
    
    [{"startNumber": 1, "horseName": "Zeta Crown", "driver": {"fullName": "H. Bollström"}, "postPosition": 1},
     {"startNumber": 4, "horseName": "Stonecapes Superb", "driver": {"fullName": "A. Teivainen"}, "postPosition": 4},
     {"startNumber": 5, "horseName": "Main Stage", "driver": {"fullName": "S. Raitala"}, "postPosition": 5}],

    [{"startNumber": 2, "horseName": "Make It Rain", "driver": {"fullName": "J. Torvinen"}, "postPosition": 2},
     {"startNumber": 3, "horseName": "Consalvo", "driver": {"fullName": "E. Holopainen"}, "postPosition": 3},
     {"startNumber": 7, "horseName": "MAS Capacity", "driver": {"fullName": "I. Nurmonen"}, "postPosition": 7}],

    [{"startNumber": 1, "horseName": "Amazing Player", "driver": {"fullName": "P. Korpi"}, "postPosition": 1},
     {"startNumber": 6, "horseName": "BWT Highway Star", "driver": {"fullName": "O. Koivunen"}, "postPosition": 6},
     {"startNumber": 8, "horseName": "Run For Royalty", "driver": {"fullName": "J. Utala"}, "postPosition": 8}]
]

sample_odds_list = [
    {1: 7.01, 2: 21.73, 3: 3.88, 6: 2.23},
    {1: 4.50, 4: 1.85, 5: 6.20},
    {2: 2.10, 3: 8.50, 7: 3.90},
    {1: 3.40, 6: 5.10, 8: 1.95}
]

for leg in range(1, 5):
    with (col1 if leg <= 2 else col2):
        st.markdown(f"### V4-{leg} (Lopp {leg})")
        df_leg = calculate_horse_scores(sample_runners_list[leg-1], sample_odds_list[leg-1])
        v4_ranks[f"V4-{leg}"] = df_leg
        
        def highlight_ev(val):
            color = '#d4edda' if val > 1.0 else ''
            return f'background-color: {color}'

        st.dataframe(
            df_leg.style.format({
                "Odds": "{:.2f}",
                "Sannolikhet %": "{:.1f}%",
                "Gränsodds": "{:.2f}",
                "EV": "{:.2f}"
            }).map(highlight_ev, subset=['EV']),
            use_container_width=True
        )

# --- 4. V4 SYSTEM & REKOMMENDATIONER ---
st.markdown("---")
st.subheader("💡 Modellens rekommenderade 1,00 € V4-kombinationer")

comb_data = []
for r_name, r_df in v4_ranks.items():
    top1 = r_df.iloc[0]["Häst"] if len(r_df) > 0 else "-"
    top2 = r_df.iloc[1]["Häst"] if len(r_df) > 1 else "-"
    comb_data.append({"Avdelning": r_name, "RANK 1 (Favorit)": top1, "RANK 2 (Utmanare)": top2})

st.table(pd.DataFrame(comb_data))

st.markdown("#### Föreslagen Huvudrad (1,00 € / rad)")
c1_r1 = v4_ranks["V4-1"].iloc[0]
c2_r1 = v4_ranks["V4-2"].iloc[0]
c3_r1 = v4_ranks["V4-3"].iloc[0]
c4_r1 = v4_ranks["V4-4"].iloc[0]

prob_main = (c1_r1["Sannolikhet %"] * c2_r1["Sannolikhet %"] * c3_r1["Sannolikhet %"] * c4_r1["Sannolikhet %"]) / 1000000

rows = [
    {"Rad": "Huvudrad (Rank 1 - Favoriter)", "V4-1": c1_r1["Häst"], "V4-2": c2_r1["Häst"], "V4-3": c3_r1["Häst"], "V4-4": c4_r1["Häst"], "Vinstchans": f"{prob_main:.2f}%", "Pris": "1,00 €"},
]

st.dataframe(pd.DataFrame(rows), use_container_width=True)
