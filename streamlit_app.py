import random
import streamlit as st
from typing import List, Dict, Any

# ==============================================================================
# 1. LÄHTÖLISTA JA LÄHDEMATERIAALI (AVDELNING 1)
# ==============================================================================

ravilahto: Dict[str, Any] = {
    "nimi": "Avdelning 1",
    "aika": "16:00",
    "matka": "2140 m",
    "lahtotapa": "Ryhmäajo (Autostart)",
    "palkinto": "135 000 kr",
    "hevoset": [
        {
            "numero": 1,
            "nimi": "T.Wall's Notorius",
            "ohjastaja": "Örjan Kihlström",
            "valmentaja": "Sofia Johansson",
            "haastattelu": "Oli erittäin hyvä viimeksi eikä väsynyt. Kestää matkan ja saa hyvän reissun sisältä.",
            "vihje": "Toppikunnossa ja elää voimillaan. Sisärataetukin mukana.",
            "kerroin_paino": 1.10
        },
        {
            "numero": 2,
            "nimi": "Hip To Be Square",
            "ohjastaja": "Per Lennartsson",
            "valmentaja": "Per Lennartsson",
            "haastattelu": "Kova reissu derbykarsinnassa, kaksi voittoa alla ennen sitä. Avaa lujaa ja on vahva.",
            "vihje": "Kestää raskaan reissun ja riittää luokassa. Tipsetta / Ykkösvihje.",
            "kerroin_paino": 1.35
        },
        {
            "numero": 3,
            "nimi": "Sign Of Times",
            "ohjastaja": "Linus Lönn",
            "valmentaja": "Lovisa Gunnarsson",
            "haastattelu": "Tuli viimeksi kuumaksi. Nyt ajetaan selkäjuoksu. Keulapaikalta tai selästä tehokas.",
            "vihje": "Nopea avaaja, mutta vastus on todella kova.",
            "kerroin_paino": 0.85
        },
        {
            "numero": 4,
            "nimi": "Geisha Road Grif",
            "ohjastaja": "Jorma Kontio",
            "valmentaja": "Sybille Tinter",
            "haastattelu": "Huippukunnossa. Lähtöpaikka on täydellinen ja tästä tähdätään keulaan.",
            "vihje": "Esiintynyt vahvasti pitkään. Keulasta erittäin vaarallinen.",
            "kerroin_paino": 1.20
        },
        {
            "numero": 5,
            "nimi": "Macho Cabrio B.B.",
            "ohjastaja": "Peter G Norman",
            "valmentaja": "Peter G Norman",
            "haastattelu": "Kesti vauhdin hyvin finaalissa. Nyt kengät jalassa joka jalkaan. Kestää työnteon.",
            "vihje": "Nostanut tasoaan huimasti kovia vastaan. Kuuluu kärkitaistoon.",
            "kerroin_paino": 1.25
        },
        {
            "numero": 6,
            "nimi": "Henessi Kiev",
            "ohjastaja": "Oskar J Andersson",
            "valmentaja": "Oskar J Andersson",
            "haastattelu": "Pussiin jäi voimia viimeksi. On nopea avaaja, mutta ulkoa on vaikea päästä keulaan.",
            "vihje": "Voimat tallella maaliin asti viimeksi. Haastava lähtöpaikka.",
            "kerroin_paino": 0.90
        },
        {
            "numero": 7,
            "nimi": "Takter",
            "ohjastaja": "Hans G Eriksson",
            "valmentaja": "Veronica Eriksson",
            "haastattelu": "Oli todella hieno kakkonen. Haastava paikka ja nousee ylempään luokkaan.",
            "vihje": "Kunto kohdallaan, mutta paha paikka ja kovempi luokka.",
            "kerroin_paino": 0.75
        },
        {
            "numero": 8,
            "nimi": "Herkules A'lir",
            "ohjastaja": "Rikard N Skoglund",
            "valmentaja": "Daniel Wäjersten",
            "haastattelu": "Elämänsä kunnossa, mutta kasirata heikentää mahdollisuuksia huomattavasti.",
            "vihje": "Vahva esitys toiselta ilman selkää. Kunto riittää, paikka ei.",
            "kerroin_paino": 0.95
        },
        {
            "numero": 9,
            "nimi": "Night Hawk",
            "ohjastaja": "Mats E Djuse",
            "valmentaja": "Jenny Pettersson",
            "haastattelu": "Parantaa koko ajan. Riittää luokassaan ja ammutaan ilman kenkiä ensi kertaa meiltä.",
            "vihje": "Luokkahevonen (64% voitoista). Ensi kertaa kengittä valmentajaltaan. Iso vaara.",
            "kerroin_paino": 1.45
        },
        {
            "numero": 10,
            "nimi": "Huchuy Qosqo",
            "ohjastaja": "Anders Eriksson",
            "valmentaja": "Anders Eriksson",
            "haastattelu": "Laukkasi tupsujen irrotukseen. Kunto nousee ja nyt riisutaan kengät edestä.",
            "vihje": "Huipputehoja löytyy. Ensimmäistä kertaa kengittä eteen - mielenkiintoinen.",
            "kerroin_paino": 1.05
        }
    ]
}

# ==============================================================================
# 2. MONTE CARLO -SIMULAATTORI
# ==============================================================================

def suorita_monte_carlo(lahto: Dict[str, Any], kierrokset: int = 10000) -> Dict[int, float]:
    hevoset = lahto["hevoset"]
    numerot = [h["numero"] for h in hevoset]
    painot = [h["kerroin_paino"] for h in hevoset]
    
    voitot = {num: 0 for num in numerot}
    
    for _ in range(kierrokset):
        voittaja = random.choices(numerot, weights=painot, k=1)[0]
        voitot[voittaja] += 1
        
    return {num: (maara / kierrokset) * 100 for num, maara in voitot.items()}

# ==============================================================================
# 3. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.set_page_config(page_title="Ravikone - Monte Carlo & Juoksun Kulku", layout="centered")

st.title("🏇 Ravikone: Monte Carlo & Juoksutapahtumat")
st.subheader(f"{ravilahto['nimi']} | Startti klo {ravilahto['aika']}")
st.caption(f"📏 Matka: {ravilahto['matka']} | {ravilahto['lahtotapa']} | 💰 Palkinto: {ravilahto['palkinto']}")

st.divider()

# Ajo Monte Carlo
simulaation_tulokset = suorita_monte_carlo(ravilahto, kierrokset=10000)
jarjestetty_tulokset = sorted(simulaation_tulokset.items(), key=lambda x: x[1], reverse=True)
hevoset_dict = {h["numero"]: h for h in ravilahto["hevoset"]}

# Suosikkinäyttö
top1_num = jarjestetty_tulokset[0][0]
top1 = hevoset_dict[top1_num]

st.success(f"🏆 **SIMULAATION VOITTAJASUOSIKKI:** Nro {top1['numero']} **{top1['nimi']}** ({jarjestetty_tulokset[0][1]:.1f}%)")

# ==============================================================================
# 4. VIDEO-ANALYYSI: JUOKSUN KULKU (TAKTIKKA & ANIMAATIO-ANALYYSI)
# ==============================================================================

st.markdown("### 🎥 Video-Animaatio & Juoksun Kulku")

tab1, tab2, tab3, tab4 = st.tabs(["🚦 1. Kiihdytys", "↪️ 2. Ensimmäinen kaarre", "🚀 3. Takasuora & Iskut", "🏁 4. Loppusuora"])

with tab1:
    st.markdown("#### 🚦 Lähtö ja Kiihdytys (0 - 300m)")
    st.info(
        "**Ratamestarin havainto:**\n"
        "* **Nro 4 Geisha Road Grif** (Jorma Kontio) lataa rajusti keskeltä rataa.\n"
        "* **Nro 2 Hip To Be Square** pystyy vastaamaan sisältä ja pyrkii estämään 4:n pääsyn eteen.\n"
        "* **Nro 3 Sign Of Times** ottaa lyhyen latauksen jälkeen nopeasti paikan 2:n takaa sisäradalla (Rygg Ledare)."
    )

with tab2:
    st.markdown("#### ↪️ Asemat Kaarteessa (300m - 1000m)")
    st.info(
        "**Asemat muotoutuvat:**\n"
        "* **Keulapaikka (1-rata):** Nro 4 Geisha Road Grif pääsee Kontion ajamana keulaan 400m kohdalla.\n"
        "* **Toinen ilman selkää (2-rata):** Nro 5 Macho Cabrio B.B. joutuu tekemään työt kuolemanpaikalla.\n"
        "* **Takarivi:** Nro 9 Night Hawk hiipii Mats E Djusen kanssatoisessa ulkoparissa (2-utv) valmiina iskemään."
    )

with tab3:
    st.markdown("#### 🚀 Ratkaisut Takasuoralla (1000m - 400m kv)")
    st.info(
        "**Vauhti kiihtyy:**\n"
        "* Tempo pysyy tasaisen kovana. Nro 5 alkaa painaa keulahevosta (Nro 4).\n"
        "* **Isot liikkeet:** Nro 9 Night Hawk lähtee heittämällä kolmannelle radalle 600 m ennen maalia. Ensimmäistä kertaa ilman kenkiä juokseva Night Hawk liikkuu erittäin tuoreen näköisesti!"
    )

with tab4:
    st.markdown("#### 🏁 Loppusuoran Taistelu (400m - Maali)")
    st.info(
        "**Ratkaisu:**\n"
        "* Keulassa ollut Nro 4 taipuu hivenen kovasta temposta.\n"
        "* **Nro 2 Hip To Be Square** löytää tilaa vapaalle radalle ja haastaa keulan.\n"
        "* Ulkorataa pitkin uljaasti tykittävä **Nro 9 Night Hawk** tulee kuitenkin kengättä ylivoimaisella vauhdilla ohi muista ja ratkaisee lähdön varmasti!"
    )

st.divider()

# ==============================================================================
# 5. KAIKKIEN HEVOSTEN SIMULAATIOTULOKSET
# ==============================================================================

st.markdown("### 📊 Kaikkien hevosten voittotodennäköisyydet (10 000 simulaatiota)")

for num, prosentti in jarjestetty_tulokset:
    h = hevoset_dict[num]
    
    otsikko = f"Nro {h['numero']} {h['nimi']} ({h['ohjastaja']}) — {prosentti:.1f}%"
    
    with st.expander(otsikko):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Valmentaja:** {h['valmentaja']}")
            st.write(f"**Vihje:** {h['vihje']}")
        with col2:
            st.write(f"**Valmentajan kommentti:** {h['haastattelu']}")
            
    st.progress(int(prosentti))
