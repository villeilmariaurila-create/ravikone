import os
import re
from datetime import datetime
import pandas as pd
import streamlit as st

try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

st.set_page_config(page_title="Hagmyren 12.9.2026", layout="wide")
st.title("🏇 Hagmyren (12.9.2026) — V85 Ravianalyysi & Seuranta")

st.markdown("""
**Ohje:** 
1. **Lähtö 1** on syötetty ja suomennettu valmiiksi.
2. Syötä muille lähdöille (2–8) ruotsinkieliset lähtölistat/kommentit sekä Veikkauksen peliprosentit.
3. Ohjelma kääntää ruotsinkieliset kommentit automaattisesti suomeksi ja laskee arvohevokset.
""")

# Ravitermien ruotsi-suomi sanakirja
SWEDISH_TROTTING_TERMS = {
    "barfota runt om": "kengittä joka puolelta",
    "barfota fram": "kengittä edestä",
    "barfota bak": "kengittä takaa",
    "skor runt om": "kengät jalassa",
    "med skor": "kengät jalassa",
    "spets": "keula / keulapaikka",
    "rygg ledaren": "keulavoittajan takana (2. sisällä)",
    "dödens": "kuolemanpaikka (2. ilman selkää)",
    "galopp": "laukka",
    "galopprisk": "laukkariski",
    "bra form": "hyvä vire",
    "toppform": "huippukunto",
    "tidig": "varhainen merkki",
    "halvstängt": "puolikiinteät laput",
    "helstängt": "kiinteät laput",
}

def translate_swedish_to_finnish(text):
    if not text or text == "Ei lisätietoja":
        return text

    translated = text
    for sv, fi in SWEDISH_TROTTING_TERMS.items():
        pattern = re.compile(re.escape(sv), re.IGNORECASE)
        translated = pattern.sub(fi, translated)

    if HAS_TRANSLATOR and len(translated.strip()) > 0:
        try:
            translated = GoogleTranslator(source='sv', target='fi').translate(translated)
        except Exception:
            pass

    return translated

def parse_horse_line(line):
    line = line.strip()
    if not line:
        return None

    match_num = re.match(r"^(\d+)[\.\s\-:]+(.*)", line)
    if not match_num:
        return None

    r_num = int(match_num.group(1))
    rest = match_num.group(2).strip()

    details = "Ei lisätietoja"
    driver_trainer = "Tuntematon"
    horse_name = rest

    if "(" in rest and ")" in rest:
        parts = rest.split("(", 1)
        horse_and_driver = parts[0].strip()
        details = parts[1].split(")")[0].strip()
        rest = horse_and_driver

    if "-" in rest:
        parts = rest.split("-", 1)
        horse_name = parts[0].strip()
        driver_trainer = parts[1].strip()

    translated_details = translate_swedish_to_finnish(details)

    return {
        "Rata": r_num,
        "Hevonen": horse_name,
        "Ohjastaja / Valmentaja": driver_trainer,
        "Lisätiedot / Kommentit (SUOMEKSI)": translated_details,
    }

# --- ESITÄYTETYT DATA-ARVOT LÄHDÖLLE 1 ---
DEFAULT_RACE_1_TEXT = """1. T.Wall's Notorius - Johan Brandel / Sofia Johansson (Kunto huipussaan, saa hyvän reissun sisäradalta. Yllättäjä.)
2. Hip To Be Square - Peter Lennartsson (Huippuvireessä, vahva ja nopea. Avaa lujaa. Varma suosikki.)
3. Sign Of Times - Claes Sjöström / Lovisa Gunnarsson (Nopea avaaja, mutta ajetaan selästä. Tufft motstånd.)
4. Geisha Road Grif - Jorma Kontio / Sybille Tinter (Huippukunnossa, keulaan päästessään vetää pitkään. Pakollinen merkki.)
5. Macho Cabrio B.B. - Peter G Norman (Kehittynyt hurjasti. Tällä kertaa kengät jalassa, mutta luotettava haastaja.)
6. Herkules A'lir - Rikard N Skoglund / Daniel Wäjersten (Elämänsä iskussa, haastava lähtöpaikka ulkona.)
7. Night Hawk - Magnus A Djuse / Jenny Pettersson (Luokkahaat, kengittä joka puolelta ekaa kertaa tähän talliin. Päähaastaja.)
8. Huchuy Qosqo - Anders Eriksson (Ensimmäistä kertaa kengittä edestä. Outsider ulkoradalta.)
11. De Är Hon - Viktor Lyck (Epävarma suorittaja, vaikea paikka takarivistä.)
12. Sandsjöns Cantona - Mats E Djuse / Kim Moberg (Kengittä takaa ja puolikiinteät laput ekaa kertaa. Jättiyllättäjä.)"""

DEFAULT_RACE_1_PCT = """1. 8%
2. 35%
3. 3%
4. 18%
5. 12%
6. 10%
7. 11%
8. 2%
11. 0.5%
12. 0.5%"""

race_tabs = st.tabs([f"Lähtö {i}" for i in range(1, 9)])
race_data_results = {}

for i in range(1, 9):
    with race_tabs[i - 1]:
        st.success(f"🔥 **Lähtö {i} — V85 Kohde {i}/8**")

        col_a, col_b = st.columns([1.5, 1])

        # Asetetaan Lähtö 1:lle valmiit pohjatiedot, muille lähdöille tyhjät/esimerkit
        if i == 1:
            initial_text = DEFAULT_RACE_1_TEXT
            initial_pct = DEFAULT_RACE_1_PCT
        else:
            initial_text = f"1. Hevonen Yksi - Ohjastaja A (Kommentti ruotsiksi)\n2. Hevonen Kaksi - Ohjastaja B (Kommentti)"
            initial_pct = "1. 30%\n2. 15%"

        with col_a:
            raw_text = st.text_area(
                f"Lähtö {i} - Lähtölista & Kommentit:",
                initial_text,
                height=220,
                key=f"race_input_{i}",
            )

        with col_b:
            raw_pct = st.text_area(
                f"Lähtö {i} - Veikkaus Peliprosentit (%):",
                initial_pct,
                height=220,
                key=f"pct_input_{i}",
            )

        # 1. Parsitaan peliprosentit
        pct_map = {}
        for p_line in raw_pct.strip().split("\n"):
            p_match = re.search(r"^(\d+)[\.\s:]+\s*(\d+(?:[\.,]\d+)?)", p_line.strip())
            if p_match:
                r_num = int(p_match.group(1))
                r_pct = float(p_match.group(2).replace(",", "."))
                pct_map[r_num] = r_pct

        # 2. Parsitaan hevoset ja käännetään
        lines = raw_text.strip().split("\n")
        runners = []
        for line in lines:
            parsed = parse_horse_line(line)
            if parsed:
                parsed["Peliprosentit %"] = pct_map.get(parsed["Rata"], 5.0)
                runners.append(parsed)

        if runners:
            df = pd.DataFrame(runners)
            
            # Pisteytysmalli
            df["Pisteet"] = [max(10, 50 - (idx * 4)) for idx in range(len(df))]
            total_pts = df["Pisteet"].sum()
            df["Mallin To %"] = (df["Pisteet"] / total_pts) * 100
            df["Etu-indeksi"] = df["Mallin To %"] - df["Peliprosentit %"]

            df = df.sort_values(by="Etu-indeksi", ascending=False).reset_index(drop=True)
            race_data_results[i] = df

            st.markdown(f"**Lähdön {i} Vertailutaulukko (Malli vs Markkina):**")

            def highlight_max(s):
                is_max = s == s.max()
                return ['background-color: rgba(46, 125, 50, 0.2)' if v else '' for v in is_max]

            styled_df = df.style.format({
                "Peliprosentit %": "{:.1f}%",
                "Mallin To %": "{:.1f}%",
                "Etu-indeksi": "{:+.1f}%"
            }).apply(highlight_max, subset=["Etu-indeksi"])

            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.info(f"Syötä lähdön {i} tiedot yllä oleviin kenttiin.")

st.markdown("---")
st.header("📊 V85 Yhteenveto & Parhaat Arvokohteet")

v85_top_bets = []
for r_num, df in race_data_results.items():
    if not df.empty and "Etu-indeksi" in df.columns:
        top = df.iloc[0]
        v85_top_bets.append({
            "Lähtö": r_num,
            "Hevonen": top["Hevonen"],
            "Rata": top["Rata"],
            "Peliprosentti %": top["Peliprosentit %"],
            "Mallin arvio %": round(top["Mallin To %"], 1),
            "Etu%": round(top["Etu-indeksi"], 1),
            "Vihje / Kommentti (FI)": top["Lisätiedot / Kommentit (SUOMEKSI)"]
        })

if v85_top_bets:
    summary_df = pd.DataFrame(v85_top_bets)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.subheader("📁 Tulosten seuranta")
    history_file = "v85_seuranta_historia.csv"

    if st.button("💾 Tallenna tämän kierroksen parhaat vedot seurantaan"):
        save_df = summary_df.copy()
        save_df.insert(0, "Pvm", datetime.now().strftime("%Y-%m-%d"))
        save_df["Tulos (Osuma=1, Huti=0)"] = ""

        if os.path.exists(history_file):
            old_df = pd.read_csv(history_file)
            combined_df = pd.concat([old_df, save_df], ignore_index=True)
            combined_df.to_csv(history_file, index=False)
        else:
            save_df.to_csv(history_file, index=False)

        st.success(f"Valinnat tallennettu tiedostoon '{history_file}'!")
