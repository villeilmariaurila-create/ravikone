import random
import streamlit as st
from typing import List, Dict, Any

# ==============================================================================
# 1. LÄHTÖLISTA, TEHOT JA MARKKINAN PELIPROSENTIT (L5)
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
            "peliprosentti": 3,
            "kerroin_paino": 1.10,
            "haastattelu": "Oli erittäin hyvä viimeksi eikä väsynyt. Kestää matkan ja saa hyvän reissun sisältä.",
            "vihje": "Toppikunnossa ja elää voimillaan. Sisärataetukin mukana."
        },
        {
            "numero": 2,
            "nimi": "Hip To Be Square",
            "ohjastaja": "Per Lennartsson",
            "peliprosentti": 24,
            "kerroin_paino": 1.35,
            "haastattelu": "Kova reissu derbykarsinnassa, kaksi voittoa alla ennen sitä. Avaa lujaa ja on vahva.",
            "vihje": "Kestää raskaan reissun ja riittää luokassa. Tipsetta / Ykkösvihje."
        },
        {
            "numero": 3,
            "nimi": "Sign Of Times",
            "ohjastaja": "Linus Lönn",
            "peliprosentti": 1,
            "kerroin_paino": 0.85,
            "haastattelu": "Tuli viimeksi kuumaksi. Nyt ajetaan selkäjuoksu. Keulapaikalta tai selästä tehokas.",
            "vihje": "Nopea avaaja, mutta vastus on todella kova."
        },
        {
            "numero": 4,
            "nimi": "Geisha Road Grif",
            "ohjastaja": "Jorma Kontio",
            "peliprosentti": 4,
            "kerroin_paino": 1.20,
            "haastattelu": "Huippukunnossa. Lähtöpaikka on täydellinen ja tästä tähdätään keulaan.",
            "vihje": "Esiintynyt vahvasti pitkään. Keulasta erittäin vaarallinen."
        },
        {
            "numero": 5,
            "nimi": "Macho Cabrio B.B.",
            "ohjastaja": "Peter G Norman",
            "peliprosentti": 10,
            "kerroin_paino": 1.25,
            "haastattelu": "Kesti vauhdin hyvin finaalissa. Nyt kengät jalassa joka jalkaan. Kestää työnteon.",
            "vihje": "Nostanut tasoaan huimasti kovia vastaan. Kuuluu kärkitaistoon."
        },
        {
            "numero": 6,
            "nimi": "Henessi Kiev",
            "ohjastaja": "Oskar J Andersson",
            "peliprosentti": 5,
            "kerroin_paino": 0.90,
            "haastattelu": "Pussiin jäi voimia viimeksi. On nopea avaaja, mutta ulkoa on vaikea päästä keulaan.",
            "vihje": "Voimat tallella maaliin asti viimeksi. Haastava lähtöpaikka."
        },
        {
            "numero": 7,
            "nimi": "Takter",
            "ohjastaja": "Hans G Eriksson",
            "peliprosentti": 3,
            "kerroin_paino": 0.75,
            "haastattelu": "Oli todella hieno kakkonen. Haastava paikka ja nousee ylempään luokkaan.",
            "vihje": "Kunto kohdallaan, mutta paha paikka ja kovempi luokka."
        },
        {
            "numero": 8,
            "nimi": "Herkules A'lir",
            "ohjastaja": "Rikard N Skoglund",
            "peliprosentti": 12,
            "kerroin_paino": 0.95,
            "haastattelu": "Elämänsä kunnossa, mutta kasirata heikentää mahdollisuuksia huomattavasti.",
            "vihje": "Vahva esitys toiselta ilman selkää. Kunto riittää, paikka ei."
        },
        {
            "numero": 9,
            "nimi": "Night Hawk",
            "ohjastaja": "Mats E Djuse",
            "peliprosentti": 34,
            "kerroin_paino": 1.45,
            "haastattelu": "Parantaa koko ajan. Riittää luokassaan ja ammutaan ilman kenkiä ensi kertaa meiltä.",
            "vihje": "Luokkahevonen (64% voitoista). Ensi kertaa kengittä valmentajaltaan. Iso vaara."
        },
        {
            "numero": 10,
            "nimi": "Huchuy Qosqo",
            "ohjastaja": "Anders Eriksson",
            "peliprosentti": 1,
            "kerroin_paino": 1.05,
            "haastattelu": "Laukkasi tupsujen irrotukseen. Kunto nousee ja nyt riisutaan kengät edestä.",
            "vihje": "Huipputehoja löytyy. Ensimmäistä kertaa kengittä eteen - mielenkiintoinen."
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

st.set_page_config(page_title="Ravikone - Monte Carlo & Peliarvo", layout="centered")

st.title("🏇 Ravikone: Simulointi vs. Peliprosentit")
st.subheader(f"{ravilahto['nimi']} | Startti klo {ravilahto['aika']}")

st.divider()

# Ajo Monte Carlo
simulaation_tulokset = suorita_monte_carlo(ravilahto, kierrokset=10000)
jarjestetty_tulokset = sorted(simulaation_tulokset.items(), key=lambda x: x[1], reverse=True)
hevoset_dict = {h["numero"]: h for h in ravilahto["hevoset"]}

# ==============================================================================
# 4. VIDEO-ANALYYSI: JUOKSUN KULKU
# ==============================================================================

st.markdown("### 🎥 Animaatio- ja Juoksutapahtumat")

tab1, tab2, tab3, tab4 = st.tabs(["🚦 1. Kiihdytys", "↪️ 2. Ensimmäinen kaarre", "🚀 3. Takasuora & Iskut", "🏁 4. Loppusuora"])

with tab1:
    st.info("**0-300m:** Nro 4 Geisha Road Grif lataa keulaan. Nro 2 Hip To Be Square vastaa rinnalla. Nro 3 Sign Of Times hakeutuu sisäradalle.")
with tab2:
    st.info("**300m-1000m:** Nro 4 ottaa keulat. Nro 5 Macho Cabrio B.B. joutuu toiselle ilman selkää. Nro 9 Night Hawk kyttää 2-utv:ssä.")
with tab3:
    st.info("**1000m-400m:** Nro 9 Night Hawk hyökkää 3. radalle ilman kenkiä. Kengättömyys tuo selkeän lisäpykälän vauhtiin!")
with tab4:
    st.info("**Loppusuora:** Nro 9 Night Hawk rynnii vahvasti ohi väsyvän keulavaljakon ja voittaa lähdön!")

st.divider()

# ==============================================================================
# 5. VERTAILUTAULUKKO & PELIARVOT
# ==============================================================================

st.markdown("### 📊 Monte Carlo vs. Markkina (Peliprosentit L5)")

for num, arvio_prosentti in jarjestetty_tulokset:
    h = hevoset_dict[num]
    peli_prosentti = h["peliprosentti"]
    ero = arvio_prosentti - peli_prosentti
    
    # Määritetään peliarvomerkintä
    if ero >= 4.0:
        peliarvo_teksti = f"🔥 **LOISTAVA PELIARVO** (+{ero:.1f}%)"
    elif ero > 0:
        peliarvo_teksti = f"✅ **Pientä peliarvoa** (+{ero:.1f}%)"
    else:
        peliarvo_teksti = f"❌ **Ylipelattu** ({ero:.1f}%)"
        
    otsikko = f"Nro {h['numero']} {h['nimi']} — Arvio: **{arvio_prosentti:.1f}%** | Pelattu: **{peli_prosentti}%**"
    
    with st.expander(otsikko):
        st.write(peliarvo_teksti)
        st.write(f"**Ohjastaja:** {h['ohjastaja']} | **Valmentaja:** {h['valmentaja']}")
        st.write(f"**Valmentajan kommentti:** {h['haastattelu']}")
        st.write(f"**Vihje:** {h['vihje']}")
        
    st.progress(int(arvio_prosentti))
