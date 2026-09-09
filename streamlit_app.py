import random
import streamlit as st
from typing import Dict, List, Any

# ==============================================================================
# 1. DYNAMISEN DATAN ALUSTUS (8 LÄHTÖÄ x 16 HEVOSTA)
# ==============================================================================

def luo_lahdon_data(lahto_nro: int) -> Dict[str, Any]:
    """Generoi lähdölle 16 hevosen rungon turvallisilla oletusarvoilla."""
    hevoset = []
    
    # Esimerkkidataa lähdölle 1 (voidaan laajentaa/muokata)
    muotoillut_hevoset = {
        1: {"nimi": "T.Wall's Notorius", "ohjastaja": "Ö. Kihlström", "valmentaja": "S. Johansson", "paino": 1.10, "peliprosentti": 3},
        2: {"nimi": "Hip To Be Square", "ohjastaja": "P. Lennartsson", "valmentaja": "P. Lennartsson", "paino": 1.35, "peliprosentti": 24},
        3: {"nimi": "Sign Of Times", "ohjastaja": "L. Lönn", "valmentaja": "L. Gunnarsson", "paino": 0.85, "peliprosentti": 1},
        4: {"nimi": "Geisha Road Grif", "ohjastaja": "J. Kontio", "valmentaja": "S. Tinter", "paino": 1.20, "peliprosentti": 4},
        5: {"nimi": "Macho Cabrio B.B.", "ohjastaja": "P. G. Norman", "valmentaja": "P. G. Norman", "paino": 1.25, "peliprosentti": 10},
        6: {"nimi": "Henessi Kiev", "ohjastaja": "O. J. Andersson", "valmentaja": "O. J. Andersson", "paino": 0.90, "peliprosentti": 5},
        7: {"nimi": "Takter", "ohjastaja": "H. G. Eriksson", "valmentaja": "V. Eriksson", "paino": 0.75, "peliprosentti": 3},
        8: {"nimi": "Herkules A'lir", "ohjastaja": "R. N. Skoglund", "valmentaja": "D. Wäjersten", "paino": 0.95, "peliprosentti": 12},
        9: {"nimi": "Night Hawk", "ohjastaja": "M. E. Djuse", "valmentaja": "J. Pettersson", "paino": 1.45, "peliprosentti": 34},
        10: {"nimi": "Huchuy Qosqo", "ohjastaja": "A. Eriksson", "valmentaja": "A. Eriksson", "paino": 1.05, "peliprosentti": 1}
    }

    for i in range(1, 17):
        if lahto_nro == 1 and i in muotoillut_hevoset:
            h = muotoillut_hevoset[i]
            hevoset.append({
                "numero": i,
                "nimi": h["nimi"],
                "ohjastaja": h["ohjastaja"],
                "valmentaja": h["valmentaja"],
                "kerroin_paino": h["paino"],
                "peliprosentti": h["peliprosentti"]
            })
        else:
            # Oletusarvot muille lähdöille ja tyhjille paikoille
            hevoset.append({
                "numero": i,
                "nimi": f"Hevonen {i}",
                "ohjastaja": "Tuntematon",
                "valmentaja": "Tuntematon",
                "kerroin_paino": round(random.uniform(0.5, 1.5), 2),
                "peliprosentti": random.randint(1, 15)
            })

    return {
        "nimi": f"Lähtö {lahto_nro}",
        "matka": "2140 m",
        "hevoset": hevoset
    }

# Luodaan kaikkien 8 lähdön tiedot
lahdot: Dict[int, Dict[str, Any]] = {i: luo_lahdon_data(i) for i in range(1, 9)}

# ==============================================================================
# 2. MONTE CARLO -SIMULAATTORI
# ==============================================================================

def suorita_monte_carlo(lahto_data: Dict[str, Any], kierrokset: int = 10000) -> Dict[int, float]:
    hevoset = lahto_data["hevoset"]
    numerot = [h["numero"] for h in hevoset]
    painot = [h.get("kerroin_paino", 1.0) for h in hevoset]
    
    voitot = {num: 0 for num in numerot}
    
    for _ in range(kierrokset):
        voittaja = random.choices(numerot, weights=painot, k=1)[0]
        voitot[voittaja] += 1
        
    return {num: round((maara / kierrokset) * 100, 1) for num, maara in voitot.items()}

# ==============================================================================
# 3. STREAMLIT-KÄYTTÖLIITTYMÄ JA RUUTUDUKKO (GRID)
# ==============================================================================

st.set_page_config(page_title="Ravikone 8 Lähtöä Grid", layout="wide")

st.title("🏇 Ravikone: 8 Lähdön Ruudukkonäkymä (16 Hevosta)")
st.caption("Valitse lähtö ja tarkastele 16 hevosen suorituskykyä 4x4 ruudukossa.")

# Lähtövalikko (1 - 8)
valittu_lahto_nro = st.radio(
    "**Valitse Lähtö:**",
    options=list(range(1, 9)),
    format_func=lambda x: f"Lähtö {x}",
    horizontal=True
)

st.divider()

valittu_lahto = lahdot[valittu_lahto_nro]
mc_tulokset = suorita_monte_carlo(valittu_lahto, kierrokset=10000)

st.subheader(f"📌 {valittu_lahto['nimi']} — 16 Hevosen Ruudukko")

# Luodaan 4x4 ruudukko (4 riviä, jokaisessa 4 saraketta)
hevoset = valittu_lahto["hevoset"]

for rivi in range(4):
    cols = st.columns(4)
    for sarake in range(4):
        index = rivi * 4 + sarake
        if index < len(hevoset):
            h = hevoset[index]
            num = h.get("numero", index + 1)
            nimi = h.get("nimi", f"Hevonen {num}")
            ohjastaja = h.get("ohjastaja", "-")
            valmentaja = h.get("valmentaja", "-")
            peli_pct = h.get("peliprosentti", 0)
            mc_pct = mc_tulokset.get(num, 0.0)
            
            ero = mc_pct - peli_pct
            
            # Kortin luonti ja reunaväritys peliarvon mukaan
            with cols[sarake]:
                with st.container(border=True):
                    # Numero ja nimi
                    st.markdown(f"### **{num}. {nimi}**")
                    st.caption(f"🏇 {ohjastaja} | 🏋️ {valmentaja}")
                    
                    st.divider()
                    
                    # Prosentit rinnakkain
                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric("Monte Carlo", f"{mc_pct}%")
                    with c2:
                        st.metric("Pelattu L5", f"{peli_pct}%", delta=f"{ero:+.1f}%")
                    
                    # Pienikokoinen edistymispalkki
                    st.progress(int(min(mc_pct, 100)))
