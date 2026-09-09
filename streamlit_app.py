import random
import streamlit as st
from typing import List, Dict, Any

# ==============================================================================
# 1. TIETOMALLI (LÄHDÖT 1, 2 JA 3)
# ==============================================================================

ravilahtot: List[Dict[str, Any]] = [
    # --------------------------------------------------------------------------
    # LÄHTÖ 1
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
                "tilastot": {"voittoprosentti": 0.25, "keula_voittoprosentti": 0.80, "balanssi": "Kengät"}
            },
            {
                "numero": 2,
                "nimi": "Esimerkki Hevonen 2",
                "ohjastaja": "Kusk B",
                "tilastot": {"voittoprosentti": 0.13, "keula_voittoprosentti": 0.50, "balanssi": "Avokenkä"}
            }
        ]
    },

    # --------------------------------------------------------------------------
    # LÄHTÖ 2
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
                "tilastot": {"voittoprosentti": 0.22, "keula_voittoprosentti": 0.60, "balanssi": "Kengät"}
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
                "tilastot": {"voittoprosentti": 0.22, "keula_voittoprosentti": 0.57, "balanssi": "Kengät / Kokolaput"}
            },
            {
                "numero": 2,
                "nimi": "Romulus Tooma",
                "ohjastaja": "Peter G Norman",
                "tilastot": {"voittoprosentti": 0.13, "keula_voittoprosentti": 1.00, "balanssi": "Kengät / Puolilaput / Bike"}
            },
            {
                "numero": 3,
                "nimi": "Mizai",
                "ohjastaja": "Mats E Djuse",
                "tilastot": {"voittoprosentti": 0.27, "keula_voittoprosentti": 0.79, "balanssi": "Avokenkä / Kokolaput / Bike"}
            },
            {
                "numero": 4,
                "nimi": "Lando Mearas",
                "ohjastaja": "Magnus A Djuse",
                "tilastot": {"voittoprosentti": 0.39, "keula_voittoprosentti": 0.92, "balanssi": "Norjalaiset laput / Bike"}
            },
            {
                "numero": 5,
                "nimi": "Mellby Joker",
                "ohjastaja": "Daniel Wäjersten",
                "tilastot": {"voittoprosentti": 0.22, "keula_voittoprosentti": 0.50, "balanssi": "Kokolaput"}
            },
            {
                "numero": 6,
                "nimi": "Jerka Sting",
                "ohjastaja": "Claes Sjöström",
                "tilastot": {"voittoprosentti": 0.28, "keula_voittoprosentti": 0.75, "balanssi": "Kokolaput / Norskit / Bike"}
            }
        ]
    }
]

# ==============================================================================
# 2. LASKENTA JA SIMULAATTIORI (NUMEROPOHJAINEN)
# ==============================================================================

def laske_suorituskyky_indeksi(hevonen: Dict[str, Any]) -> float:
    """Laskee indeksin pelkästään hevosobjektin tilastoista."""
    stats = hevonen["tilastot"]
    
    perus_v_prosentti = stats.get("voittoprosentti", 0.10)
    keula_v_prosentti = stats.get("keula_voittoprosentti", 0.50)
    
    balanssi = stats.get("balanssi", "")
    bonus = 1.15 if "Avokenkä" in balanssi or "barfota" in balanssi.lower() else 1.0

    return (perus_v_prosentti * 0.4 + keula_v_prosentti * 0.4) * bonus * 100


def simuloita_lahto_numerolla(lahto_data: Dict[str, Any], simulaatioita: int = 10000) -> Dict[int, float]:
    """
    Simuloi voittajat käyttäen avaimena pelkkää hevosen NUMEROA (int).
    Palauttaa dictin: {hevosen_numero: voittoprosentti}
    """
    hevoset = lahto_data["hevoset"]
    
    # Haetaan pelkät numerot ja lasketaan niille indeksit
    numerot = [h["numero"] for h in hevoset]
    indeksit = [laske_suorituskyky_indeksi(h) for h in hevoset]
    
    summa_indeksi = sum(indeksit)
    todennakoisyydet = [i / summa_indeksi for i in indeksit]
    
    # Alustetaan laskuri numeroittain: {1: 0, 2: 0, 3: 0, ...}
    voittotilasto = {num: 0 for num in numerot}
    
    # Suoritetaan simulaatio
    for _ in range(simulaatioita):
        voittaja_numero = random.choices(numerot, weights=todennakoisyydet, k=1)[0]
        voittotilasto[voittaja_numero] += 1
        
    # Lasketaan tulokset prosenteiksi
    return {num: (maara / simulaatioita) * 100 for num, maara in voittotilasto.items()}

# ==============================================================================
# 3. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.title("Ravikone - Numero-pohjainen Simulaattori")

for lahto in ravilahtot:
    st.header(f"{lahto['nimi']} ({lahto['aika']})")
    st.caption(f"Matka: {lahto['matka']} | {lahto['lahtotapa']} | Palkinto: {lahto['palkinto']}")
    
    # Luodaan hakutaulukko: numero -> hevosen muut tiedot (nimet jne.)
    hevoset_dict = {h["numero"]: h for h in lahto["hevoset"]}
    
    # Ajetaan numeropohjainen simulaatio
    ennusteet_numerolla = simuloita_lahto_numerolla(lahto, simulaatioita=10000)
    
    # Järjestetään tulokset voittoprosentin mukaan suurimmasta pienimpään
    jarjestetty_tulokset = sorted(ennusteet_numerolla.items(), key=lambda x: x[1], reverse=True)
    
    # Tulostetaan tulokset
    for num, prosenti in jarjestetty_tulokset:
        hevonen = hevoset_dict[num]
        st.write(f"**Nro {num} {hevonen['nimi']}** ({hevonen['ohjastaja']}) — Voittomahdollisuus: **{prosenti:.1f}%**")
        st.progress(int(prosenti))
    
    st.divider()
