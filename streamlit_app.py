import random
import streamlit as st
from typing import List, Dict, Any

# ==============================================================================
# 1. TIETOMALLI (LÄHDÖT 1, 2 JA 3)
# ==============================================================================

ravilahtot: List[Dict[str, Any]] = [
    # --------------------------------------------------------------------------
    # LÄHTÖ 1 (Malli)
    # --------------------------------------------------------------------------
    {
        "lahto": 1,
        "nimi": "Lähtö 1 / Osagruppi 1",
        "aika": "15:58",
        "matka": "2140 m",
        "lahtotapa": "Ryhmäajo (Autostart)",
        "palkinto": "100 000 kr",
        "hevoset": [
            {
                "numero": 1,
                "nimi": "Esimerkki Hevonen 1",
                "ohjastaja": "Kusk A",
                "valmentaja": "Valmentaja A",
                "haastattelu": "Kaikki kunnossa, hyvät saumat keulasta.",
                "vihjekommentti": "Toimii hienosti matkalla, varma ehdokas.",
                "tilastot": {
                    "startit": "20 (5-3-2)",
                    "voittoprosentti": 0.25,
                    "keula_voittoprosentti": 0.80,
                    "balanssi": "Kengät"
                }
            },
            {
                "numero": 2,
                "nimi": "Esimerkki Hevonen 2",
                "ohjastaja": "Kusk B",
                "valmentaja": "Valmentaja B",
                "haastattelu": "Haastava paikka mutta kunnossa.",
                "vihjekommentti": "Tarvitsee vähän tuuria matkalla.",
                "tilastot": {
                    "startit": "15 (2-4-1)",
                    "voittoprosentti": 0.13,
                    "keula_voittoprosentti": 0.50,
                    "balanssi": "Avokenkä"
                }
            }
        ]
    },

    # --------------------------------------------------------------------------
    # LÄHTÖ 2 (Malli)
    # --------------------------------------------------------------------------
    {
        "lahto": 2,
        "nimi": "Lähtö 2 / Osagruppi 2",
        "aika": "16:20",
        "matka": "2140 m",
        "lahtotapa": "Tasoitusajo (Voltstart)",
        "palkinto": "110 000 kr",
        "hevoset": [
            {
                "numero": 1,
                "nimi": "Esimerkki Hevonen 3",
                "ohjastaja": "Kusk C",
                "valmentaja": "Valmentaja C",
                "haastattelu": "Vahva esitys alla, odotetaan kärkisijoitusta.",
                "vihjekommentti": "Perushevonen tässä lähdössä.",
                "tilastot": {
                    "startit": "18 (4-2-3)",
                    "voittoprosentti": 0.22,
                    "keula_voittoprosentti": 0.60,
                    "balanssi": "Kengät"
                }
            }
        ]
    },

    # --------------------------------------------------------------------------
    # LÄHTÖ 3
    # --------------------------------------------------------------------------
    {
        "lahto": 3,
        "nimi": "Lähtö 3 / Osagruppi 3",
        "aika": "16:44",
        "matka": "1640 m",
        "lahtotapa": "Ryhmäajo (Autostart)",
        "palkinto": "150 000 kr",
        "hevoset": [
            {
                "numero": 1,
                "nimi": "Before Takeoff",
                "ohjastaja": "Örjan Kihlström",
                "valmentaja": "Daniel Wäjersten",
                "haastattelu": "Sai viimeksi hienon juoksun Margaretas Pokalissa. Kaikki tuntuu sen jälkeen hyvältä ja tästä yritetään avata mahdollisimman nopeasti.",
                "vihjekommentti": "Kolme voittoa kuudesta startista lyhyellä matkalla Ruotsissa. Neljä toista sijaa seitsemästä startista syksyn aikana.",
                "tilastot": {
                    "startit": "32 (7-8-4)",
                    "voittoprosentti": 0.22,
                    "keula_voittoprosentti": 0.57,
                    "balanssi": "Kengät / Kokolaput"
                }
            },
            {
                "numero": 2,
                "nimi": "Romulus Tooma",
                "ohjastaja": "Peter G Norman",
                "valmentaja": "Peter G Norman",
                "haastattelu": "Toimi hyvin viimeksi ja lopetti valtavan nopeasti. Täällä hiivitään mukana ja katsotaan mihin se riittää.",
                "vihjekommentti": "Lähdön alhaisin voittoprosentti. Neljä toista sijaa parhaana tuloksena 21 startista Normanilla.",
                "tilastot": {
                    "startit": "38 (5-7-6)",
                    "voittoprosentti": 0.13,
                    "keula_voittoprosentti": 1.00,
                    "balanssi": "Kengät / Puolilaput / Bike"
                }
            },
            {
                "numero": 3,
                "nimi": "Mizai",
                "ohjastaja": "Mats E Djuse",
                "valmentaja": "Jan Ove Olsen",
                "haastattelu": "Meni maaliin voimat tallella ja alkaa päästä huikeaan kuntoon. Nyt on aika olla hyökkäävämpi.",
                "vihjekommentti": "15 voittoa 21 startista keulasta Ruotsissa (79 %). Voitti kultadivisioonan vuosi sitten.",
                "tilastot": {
                    "startit": "77 (21-9-9)",
                    "voittoprosentti": 0.27,
                    "keula_voittoprosentti": 0.79,
                    "balanssi": "Avokenkä / Kokolaput / Bike"
                }
            },
            {
                "numero": 4,
                "nimi": "Lando Mearas",
                "ohjastaja": "Magnus A Djuse",
                "valmentaja": "Daniel Wäjersten",
                "haastattelu": "Uskomattoman starttinopea tällaisilta paikoilta. Jos pääsee keulaan, vaikea voittaa.",
                "vihjekommentti": "11 voittoa 14:stä Ruotsin voitosta keulasta (92 %). Talli iskussa.",
                "tilastot": {
                    "startit": "36 (14-1-5)",
                    "voittoprosentti": 0.39,
                    "keula_voittoprosentti": 0.92,
                    "balanssi": "Norjalaiset laput / Bike"
                }
            },
            {
                "numero": 5,
                "nimi": "Mellby Joker",
                "ohjastaja": "Daniel Wäjersten",
                "valmentaja": "Daniel Wäjersten",
                "haastattelu": "Teki rajun latauksen Suomessa Don Fanucci Cetin jälkeen. Täältä vaikea päästä keulaan tai voittajaselkään.",
                "vihjekommentti": "3 voittoa 9 startista Mats E Djusen kanssa. Vaikea asema ulkoa.",
                "tilastot": {
                    "startit": "65 (14-10-13)",
                    "voittoprosentti": 0.22,
                    "keula_voittoprosentti": 0.50,
                    "balanssi": "Kokolaput"
                }
            },
            {
                "numero": 6,
                "nimi": "Jerka Sting",
                "ohjastaja": "Claes Sjöström",
                "valmentaja": "Claes Sjöström",
                "haastattelu": "Samoilla varusteilla kuin aiemmin, kunto hyvä.",
                "vihjekommentti": "Yksi voitto neljästä startista sprinterimatkalla. Yksi aiempi startti Hagmyrenissa, jonka voitti.",
                "tilastot": {
                    "startit": "69 (19-11-10)",
                    "voittoprosentti": 0.28,
                    "keula_voittoprosentti": 0.75,
                    "balanssi": "Kokolaput / Norskit / Bike"
                }
            }
        ]
    }
]

# ==============================================================================
# 2. MALLINNOSTO / SIMULAATTORI (Monte Carlo Simulation)
# ==============================================================================

def laske_suorituskyky_indeksi(hevonen: Dict[str, Any]) -> float:
    """
    Laskee hevoselle painotetun tasoluvun perustilastojen pohjalta.
    Korjattu muuttujien nimet (poistettu %-merkit).
    """
    stats = hevonen["tilastot"]
    
    perus_v_prosentti = stats.get("voittoprosentti", 0.10)
    keula_v_prosentti = stats.get("keula_voittoprosentti", 0.50)
    
    # Tarkistetaan varuste- ja balanssietu
    balanssi = stats.get("balanssi", "")
    bonus = 1.15 if "Avokenkä" in balanssi or "barfota" in balanssi.lower() else 1.0

    indeksi = (perus_v_prosentti * 0.4 + keula_v_prosentti * 0.4) * bonus * 100
    return indeksi

def simuloita_lahto(lahto_data: Dict[str, Any], simulaatioita: int = 10000) -> Dict[str, float]:
    """
    Simuloi tietyn lähdön voittajaa Monte Carlo -menetelmällä.
    """
    hevoset = lahto_data["hevoset"]
    indeksit = [laske_suorituskyky_indeksi(h) for h in hevoset]
    summa_indeksi = sum(indeksit)
    
    # Lasketaan todennäköisyysjakauma
    todennakoisyydet = [i / summa_indeksi for i in indeksit]
    
    voittotilasto = {h["nimi"]: 0 for h in hevoset}
    
    # Suoritetaan simulaatio
    for _ in range(simulaatioita):
        voittaja = random.choices(hevoset, weights=todennakoisyydet, k=1)[0]
        voittotilasto[voittaja["nimi"]] += 1
        
    # Muunnetaan simulaatiotulokset prosenteiksi
    tulos_prosentteina = {nimi: (maara / simulaatioita) * 100 for nimi, maara in voittotilasto.items()}
    return tulos_prosentteina

# ==============================================================================
# 3. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.title("Ravikone - Ennustemallinnus")
st.write("Mallinnetut voittotodennäköisyydet lähtökohtaisille lähdöille.")

for lahto in ravilahtot:
    st.header(f"{lahto['nimi']} ({lahto['aika']})")
    st.caption(f"Matka: {lahto['matka']} | {lahto['lahtotapa']} | Palkinto: {lahto['palkinto']}")
    
    ennusteet = simuloita_lahto(lahto, simulaatioita=10000)
    jarjestetty = sorted(ennusteet.items(), key=lambda x: x[1], reverse=True)
    
    for nimi, prosenti in jarjestetty:
        hevonen_info = next(h for h in lahto["hevoset"] if h["nimi"] == nimi)
        st.write(f"**Nro {hevonen_info['numero']} {nimi}** - Voittomahdollisuus: **{prosenti:.1f}%**")
        st.progress(int(prosenti))
    
    st.divider()
