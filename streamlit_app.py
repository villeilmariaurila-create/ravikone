import random
import streamlit as st
from typing import List, Dict, Any

# ==============================================================================
# 1. TIETOMALLI (AVDELNING 1 / LÄHTÖ 1)
# ==============================================================================

ravilahto: Dict[str, Any] = {
    "lahto": 1,
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
            "haastattelu": "Oli viimeksi erittäin hyvä eikä ollut väsynyt maalissa. Muoto on todella hyvä ja pystyy avaamaan. Kestää matkan ja odotan hyvää esitystä.",
            "vihjekommentti": "Toppikunnossa ja elää voimillaan. Paras pidemmällä matkalla. Yllätysvalmis.",
            "tilastot": {"voittoprosentti": 0.18, "keula_voittoprosentti": 0.67, "balanssi": "Avokenkä"}
        },
        {
            "numero": 2,
            "nimi": "Hip To Be Square",
            "ohjastaja": "Per Lennartsson",
            "valmentaja": "Per Lennartsson",
            "haastattelu": "Kova reissu derbykarsinnassa, mutta pärjäsi silti hyvin. Kaksi vakuuttavaa voittoa alla ennen sitä. Avaa hyvin, vahva ja nopea. Vihjevihjeen ykkönen.",
            "vihjekommentti": "Kestää raskaan reissun ja riittää enemmän kuin hyvin tähän luokkaan. Ykkösvihje.",
            "tilastot": {"voittoprosentti": 0.31, "keula_voittoprosentti": 1.00, "balanssi": "Avokenkä"}
        },
        {
            "numero": 3,
            "nimi": "Sign Of Times",
            "ohjastaja": "Linus Lönn",
            "valmentaja": "Lovisa Gunnarsson",
            "haastattelu": "Tuli viimeksi hieman liian kuumaksi, mutta kesti silti hyvin. Nyt ajetaan selkäjuoksu. Keulapaikalta tai selästä tehokas.",
            "vihjekommentti": "Kulutti liikaa voimia viimeksi. Nopea avaaja ja saa hyvän juoksun, mutta vastus on kova.",
            "tilastot": {"voittoprosentti": 0.16, "keula_voittoprosentti": 0.67, "balanssi": "Avokenkä etu"}
        },
        {
            "numero": 4,
            "nimi": "Geisha Road Grif",
            "ohjastaja": "Jorma Kontio",
            "valmentaja": "Sybille Tinter",
            "haastattelu": "Pitää erinomaista kuntoa. Lähtöpaikka on täydellinen ja tästä päästään keulaan. Todella hyvä tuntu hevosesta.",
            "vihjekommentti": "Esiintynyt vahvasti pitkään ja on huippukunnossa. Voitti keulasta aiemmin. Otettava vakavasti.",
            "tilastot": {"voittoprosentti": 0.17, "keula_voittoprosentti": 0.50, "balanssi": "Avokenkä"}
        },
        {
            "numero": 5,
            "nimi": "Macho Cabrio B.B.",
            "ohjastaja": "Peter G Norman",
            "valmentaja": "Peter G Norman",
            "haastattelu": "Kesti vauhdin hyvin finaalissa ja kehittyy koko ajan. Nyt kengät jalassa joka jalkaan. Kestää tehdä työtä.",
            "vihjekommentti": "Nostanut tasoaan huimasti. Ei ole ollut kolmea heikompi viime kisoissaan kovia vastaan. Kuuluu kärkitaistoon.",
            "tilastot": {"voittoprosentti": 0.25, "keula_voittoprosentti": 1.00, "balanssi": "Kengät"}
        },
        {
            "numero": 6,
            "nimi": "Henessi Kiev",
            "ohjastaja": "Oskar J Andersson",
            "valmentaja": "Oskar J Andersson",
            "haastattelu": "Pussiin jäi voimia viimeksi johtavan takana. On nopea avaaja ja latautuu keulaan, vaikka sisältä löytyy myös nopeita.",
            "vihjekommentti": "Voimat tallella maaliin asti viimeksi. Riittää luokassaan, mutta keulaan pääsy ulkoa on tiukassa. Haastaja.",
            "tilastot": {"voittoprosentti": 0.23, "keula_voittoprosentti": 0.33, "balanssi": "Avokenkä"}
        },
        {
            "numero": 7,
            "nimi": "Takter",
            "ohjastaja": "Hans G Eriksson",
            "valmentaja": "Veronica Eriksson",
            "haastattelu": "Gauppa virkistyi edelliseen starttiin ja oli todella hieno. Haastava paikka ja nousee ylempään luokkaan, tarvitsee tuuria.",
            "vihjekommentti": "Hieno kakkossija alla ja kunto kohdallaan. Kolipaikalta laukkariski tai laikkaantuminen ulkoradoille. Rahasijaa hakee.",
            "tilastot": {"voittoprosentti": 0.22, "keula_voittoprosentti": 0.75, "balanssi": "Kengät"}
        },
        {
            "numero": 8,
            "nimi": "Herkules A'lir",
            "ohjastaja": "Rikard N Skoglund",
            "valmentaja": "Daniel Wäjersten (Oskar Florhed)",
            "haastattelu": "Erittäin hyvä viimeksi utvåldigt om ledaren -paikalta. Elämänsä kunnossa, mutta kasirata heikentää mahdollisuuksia huomattavasti.",
            "vihjekommentti": "Vahva esitys toiselta ilman selkää viimeksi. Kunto riittää heittämällä, mutta lähtöpaikka on todella ilkeä. Juoksun onnistuessa korkealla.",
            "tilastot": {"voittoprosentti": 0.21, "keula_voittoprosentti": 0.00, "balanssi": "Avokenkä taka"}
        },
        {
            "numero": 9,
            "nimi": "Night Hawk",
            "ohjastaja": "Mats E Djuse",
            "valmentaja": "Jenny Pettersson",
            "haastattelu": "Kaksi hyvää starttia pitkän tauon jälkeen. Parantaa koko ajan. Riittää luokassaan ja ammutaan ilman kenkiä ensi kertaa meiltä.",
            "vihjekommentti": "Luokkahevonen, joka on saanut kaksi starttia kropatuksi pitkän tauon jälkeen. Ensi kertaa avokengässä valmentajaltaan. Vaarallinen haastaja.",
            "tilastot": {"voittoprosentti": 0.64, "keula_voittoprosentti": 0.50, "balanssi": "Avokenkä"}
        },
        {
            "numero": 10,
            "nimi": "Huchuy Qosqo",
            "ohjastaja": "Anders Eriksson",
            "valmentaja": "Anders Eriksson",
            "haastattelu": "Laukkasi viimeksi kun kuskilla oli kiire riisua tupsuja. Kunto on nouseva. Takarivistä ollaan yllättäjänä matkassa.",
            "vihjekommentti": "Huipputehoja löytyy, mutta laukkaillut tiheään. Ensimmäistä kertaa kengittä eteen - mielenkiintoinen muutos. Yllätysvalmis.",
            "tilastot": {"voittoprosentti": 0.31, "keula_voittoprosentti": 0.75, "balanssi": "Avokenkä etu"}
        }
    ]
}

# ==============================================================================
# 2. LASKENTA JA SIMULAATTORI (NUMEROPOHJAINEN)
# ==============================================================================

def laske_suorituskyky_indeksi(hevonen: Dict[str, Any]) -> float:
    """Laskee indeksin pelkästään hevosobjektin tilastoista."""
    stats = hevonen["tilastot"]
    
    perus_v_prosentti = stats.get("voittoprosentti", 0.10)
    keula_v_prosentti = stats.get("keula_voittoprosentti", 0.50)
    
    balanssi = stats.get("balanssi", "")
    bonus = 1.15 if "Avokenkä" in balanssi else 1.0

    return (perus_v_prosentti * 0.4 + keula_v_prosentti * 0.4) * bonus * 100


def simuloita_lahto_numerolla(lahto_data: Dict[str, Any], simulaatioita: int = 10000) -> Dict[int, float]:
    """Simuloi voittajat käyttäen avaimena pelkkää hevosen NUMEROA (int)."""
    hevoset = lahto_data["hevoset"]
    
    numerot = [h["numero"] for h in hevoset]
    indeksit = [laske_suorituskyky_indeksi(h) for h in hevoset]
    
    summa_indeksi = sum(indeksit)
    todennakoisyydet = [i / summa_indeksi for i in indeksit]
    
    voittotilasto = {num: 0 for num in numerot}
    
    for _ in range(simulaatioita):
        voittaja_numero = random.choices(numerot, weights=todennakoisyydet, k=1)[0]
        voittotilasto[voittaja_numero] += 1
        
    return {num: (maara / simulaatioita) * 100 for num, maara in voittotilasto.items()}

# ==============================================================================
# 3. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.title("Ravikone - Ennustemallinnus")

lahto = ravilahto
st.header(f"{lahto['nimi']} ({lahto['aika']})")
st.caption(f"Matka: {lahto['matka']} | {lahto['lahtotapa']} | Palkinto: {lahto['palkinto']}")

# Hakutaulukko numeroittain
hevoset_dict = {h["numero"]: h for h in lahto["hevoset"]}

# Ajetaan simulaatio
ennusteet_numerolla = simuloita_lahto_numerolla(lahto, simulaatioita=10000)
jarjestetty_tulokset = sorted(ennusteet_numerolla.items(), key=lambda x: x[1], reverse=True)

# Tulostus
for num, prosentti in jarjestetty_tulokset:
    hevonen = hevoset_dict[num]
    
    with st.expander(f"**Nro {num} {hevonen['nimi']}** ({hevonen['ohjastaja']}) — **{prosentti:.1f}%**"):
        st.write(f"**Valmentaja:** {hevonen['valmentaja']}")
        st.write(f"**Balanssi:** {hevonen['tilastot']['balanssi']}")
        st.write(f"**Valmentajan kommentti:** {hevonen['haastattelu']}")
        st.write(f"**Vihje:** {hevonen['vihjekommentti']}")
    st.progress(int(prosentti))
