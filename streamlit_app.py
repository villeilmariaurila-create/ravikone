import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="Köysikujalla", layout="wide")

st.title("🏇 Köysikujalla")
st.caption("Maailmassa on monta ihmeellistä asiaa")

# Automaattinen sivun päivitys 2 minuutin (120 s) välein
st.empty()
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

# --- 1. PÄIVÄMÄÄRÄN JA RADOJEN HAKU ---
col_date, col_select, col_filter = st.columns([1, 2, 1.5])

with col_date:
    selected_date = st.date_input("Valitse päivämäärä:", date.today())

# Veikkauksen API hyväksyy muodon YYYYMMDD sekä YYYY-MM-DD
date_str_nodash = selected_date.strftime("%Y%m%d")
date_str_dash = selected_date.strftime("%Y-%m-%d")

@st.cache_data(ttl=120)
def fetch_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

# Haetaan kortit useammalla eri API-osoitevaihtoehdolla
cards = []
cards_data = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/date/{date_str_nodash}")
if isinstance(cards_data, dict) and cards_data.get("cards"):
    cards = cards_data.get("cards", [])

if not cards:
    cards_data = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/date/{date_str_dash}")
    if isinstance(cards_data, dict) and cards_data.get("cards"):
        cards = cards_data.get("cards", [])

if not cards and selected_date == date.today():
    today_cards = fetch_json("https://www.veikkaus.fi/api/toto-info/v1/cards/today")
    if isinstance(today_cards, dict):
        cards = today_cards.get("cards", [])

card_options = {}
if cards:
    for c in cards:
        track = c.get("trackName", "Tuntematon rada")
        country = c.get("country", "FI")
        card_id = c.get("cardId")
        label = f"{track} ({country}) — Kortti: {card_id}"
        card_options[label] = c

with col_select:
    if card_options:
        selected_label = st.selectbox("Valitse ravit / rada:", list(card_options.keys()))
        selected_card = card_options[selected_label]
    else:
        st.warning(f"Ei aktiivisia ravikohteita saatavilla valitulle päivälle ({selected_date.strftime('%d.%m.%Y')}).")
        selected_card = None

with col_filter:
    filter_option = st.selectbox(
        "Suodata lähtöjä:",
        ["Kaikki lähdöt", "V4 (Lähdöt 1–4)", "V85 / V86 (Lähdöt 5–12)"] + [f"Lähtö {i}" for i in range(1, 14)]
    )

if not selected_card:
    st.info("💡 Kokeile valita kalenterista tämä päivä tai tuleva päivä, jolle lähtölistat on jo julkaistu.")
    st.stop()

card_id = selected_card.get("cardId")

# --- 2. LÄHTÖLISTOJEN JA KERTOIMIEN HAKU ---
card_detail = fetch_json(f"https://www.veikkaus.fi/api/toto-info/v1/cards/{card_id}")
races = card_detail.get("races", []) if isinstance(card_detail, dict) else []

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

# --- 3. PISTEYTYSALGORITMI ---
def calculate_scores(runners, odds_map):
    data = []
    total_pts_sum = 0
    
    for r in runners:
        num = r.get("startNumber")
        name = r.get("horseName", f"Hevonen {num}")
        
        driver_info = r.get("driver", {})
        driver_name = driver_info.get("fullName") or f"{driver_info.get('firstName', '')} {driver_info.get('lastName', '')}".strip()
        if not driver_name:
            driver_name = "Tuntematon"
            
        post = r.get("postPosition", num)
        odds = odds_map.get(num, 0.0)
        
        # Sovittu pisteytyslogiikka
        base_score = 30 if odds == 0 else max(5, min(48, int(50 - (odds * 1.5))))
        track_score = 8 if post in [2, 3, 4, 5] else (5 if post == 1 else (-5 if post in [7, 8] else 0))
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

# Lasketan pisteytykset kaikille lähdöille
all_ranks = {}
best_value_bets = []

for race in races:
    r_num = race.get("raceNumber")
    runners = race.get("runners", [])
    r_odds = odds_by_race.get(r_num, {})
    
    df_leg = calculate_scores(runners, r_odds)
    all_ranks[f"Lähtö {r_num}"] = df_leg
    
    # Poimitaan parhaat pelikohteet (EV > 1.00 ja Kerroin > 0)
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

# --- 4. REAALIAIKAISET PARHAAT PELIKOHTEET -LAATIKKO ---
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

# --- 5. SUODATETUT LÄHDÖT ---
filtered_races = []
for r in races:
    r_num = r.get("raceNumber")
    if filter_option == "Kaikki lähdöt":
        filtered_races.append(r)
    elif filter_option == "V4 (Lähdöt 1–4)" and 1 <= r_num <= 4:
        filtered_races.append(r)
    elif filter_option == "V85 / V86 (Lähdöt 5–12)" and 5 <= r_num <= 12:
        filtered_races.append(r)
    elif filter_option.startswith("Lähtö ") and r_num == int(filter_option.split(" ")[1]):
        filtered_races.append(r)

# --- 6. TULOSTUS KÄYTTÖLIITTYMÄÄN ---
st.subheader(f"🎯 {selected_card.get('trackName')} — {filter_option}")

cols = st.columns(2 if len(filtered_races) > 1 else 1)

for idx, race in enumerate(filtered_races, start=1):
    r_num = race.get("raceNumber")
    df_leg = all_ranks.get(f"Lähtö {r_num}", pd.DataFrame())
    
    col_target = cols[0] if len(filtered_races) == 1 else (cols[0] if idx % 2 != 0 else cols[1])
    
    with col_target:
        v4_tag = " [V4-kohde]" if 1 <= r_num <= 4 else ""
        v85_tag = " [V85/V86-kohde]" if 5 <= r_num <= 12 else ""
        
        st.markdown(f"### Lähtö {r_num} ({race.get('distance', 2140)} m){v4_tag}{v85_tag}")
        
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

# --- 7. 1,00 € V4-GENERAATTORI ---
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

