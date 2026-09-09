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
            "kerroin_paino": 1.10  # Hyvä paikka + vire
        },
        {
            "numero": 2,
            "nimi": "Hip To Be Square",
            "ohjastaja": "Per Lennartsson",
            "valmentaja": "Per Lennartsson",
            "haastattelu": "Kova reissu derbykarsinnassa, kaksi voittoa alla ennen sitä. Avaa lujaa ja on vahva.",
            "vihje": "Kestää raskaan reissun ja riittää luokassa. Tipsetta / Ykkösvihje.",
            "kerroin_paino": 1.35  # Ykkösvihje + huippupaikka
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
            "kerroin_paino": 1.20  # Keulahuomio + Kontio
        },
        {
            "numero": 5,
            "nimi": "Macho Cabrio B.B.",
            "ohjastaja": "Peter G Norman",
            "valmentaja": "Peter G Norman",
            "haastattelu": "Kesti vauhdin hyvin finaalissa. Nyt kengät jalassa joka jalkaan. Kestää työnteon.",
            "vihje": "Nostanut tasoaan huimasti kovia vastaan. Kuuluu kärkitaistoon.",
            "kerroin_paino": 1.25  # Vahva luokka
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
            "kerroin_paino": 0.95  # Kova hevostaso, paha paikka
        },
        {
            "numero": 9,
            "nimi": "Night Hawk",
            "ohjastaja": "Mats E Djuse",
            "valmentaja": "Jenny Pettersson",
            "haastattelu": "Parantaa koko ajan. Riittää luokassaan ja ammutaan ilman kenkiä ensi kertaa meiltä.",
            "vihje": "Luokkahevonen (64% voitoista). Ensi kertaa kengittä valmentajaltaan. Iso vaara.",
            "kerroin_paino": 1.45  # Suurin suosikki: Huikea voittoprosentti + kenkäriisunta
        },
        {
            "numero": 10,
            "nimi": "Huchuy Qosqo",
            "ohjastaja": "Anders Eriksson",
            "valmentaja": "Anders Eriksson",
            "haastattelu": "Laukkasi tupsujen irrotukseen. Kunto nousee ja nyt riisutaan kengät edestä.",
            "vihje": "Huipputehoja löytyy. Ensimmäistä kertaa kengittä eteen - mielenkiintoinen.",
            "kerroin_paino": 1.05  # Yllättäjä / Kenkäriisunta
        }
    ]
}

# ==============================================================================
# 2. MONTE CARLO -SIMULAATTORI
# ==============================================================================

def suorita_monte_carlo(lahto: Dict[str, Any], kierrokset: int = 10000) -> Dict[int, float]:
    """Suorittaa Monte Carlo -simulaation hevosten painotettujen tehojen perusteella."""
    hevoset = lahto["hevoset"]
    numerot = [h["numero"] for h in hevoset]
    painot = [h["kerroin_paino"] for h in hevoset]
    
    # Alustetaan voittolaskuri
    voitot = {num: 0 for num in numerot}
    
    # Arvotaan voittaja 'kierrokset'-määrän verran
    for _ in range(kierrokset):
        voittaja = random.choices(numerot, weights=painot, k=1)[0]
        voitot[voittaja] += 1
        
    # Muutetaan tulokset prosenteiksi
    return {num: (maara / kierrokset) * 100 for num, maara in voitot.items()}

# ==============================================================================
# 3. HELPOSTI LUETTAVA STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.set_page_config(page_title="Ravikone - Monte Carlo", layout="centered")

st.title("🏇 Ravikone: Monte Carlo -Ennuste")
st.subheader(f"{ravilahto['nimi']} | Startti klo {ravilahto['aika']}")
st.caption(f"📏 Matka: {ravilahto['matka']} | {ravilahto['lahtotapa']} | 💰 Palkinto: {ravilahto['palkinto']}")

st.divider()

# Suoritetaan simulaatio
simulaation_tulokset = suorita_monte_carlo(ravilahto, kierrokset=10000)

# Järjestetään hevoset parhaasta heikoimpaan voittotodennäköisyyden mukaan
jarjestetty_tulokset = sorted(simulaation_tulokset.items(), key=lambda x: x[1], reverse=True)
hevoset_dict = {h["numero"]: h for h in ravilahto["hevoset"]}

# Näytetään top 3 selkeänä yhteenvetona
top1_num = jarjestetty_tulokset[0][0]
top1 = hevoset_dict[top1_num]

st.success(f"🏆 **SUURIN VOITTAJASUOSIKKI:** Nro {top1['numero']} **{top1['nimi']}** ({jarjestetty_tulokset[0][1]:.1f}%)")

st.markdown("### 📊 Kaikkien hevosten voittotodennäköisyydet (10 000 simulaatiota)")

# Tulostetaan jokainen hevonen selkeänä korttina
for num, prosentti in jarjestetty_tulokset:
    h = hevoset_dict[num]
    
    # Kortin otsikkorivi
    otsikko = f"Nro {h['numero']} {h['nimi']} ({h['ohjastaja']}) — {prosentti:.1f}%"
    
    with st.expander(otsikko):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Valmentaja:** {h['valmentaja']}")
            st.write(f"**Vihje:** {h['vihje']}")
        with col2:
            st.write(f"**Valmentajan kommentti:** {h['haastattelu']}")
            
    # Visuaalinen edistymispalkki
    st.progress(int(prosentti))
