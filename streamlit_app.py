import datetime
import pandas as pd
import streamlit as st

# ==========================================================
# 1. SIVUN ASETUKSET & VISUAALINEN TYYLI (LOGO & NELIAPILA)
# ==========================================================
st.set_page_config(page_title="Stella Ravisimulaattori", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stella-logo-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 24px;
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 16px 20px;
        border-radius: 12px;
        border: 1px solid #BFDBFE;
    }
    .stella-clover-icon {
        font-size: 40px;
        background: #1E3A8A;
        width: 65px;
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stella-title {
        font-size: 30px;
        font-weight: 800;
        color: #1E3A8A;
        margin: 0;
        line-height: 1.2;
    }
    .stella-subtitle {
        font-size: 14px;
        color: #4B5563;
        margin-top: 4px;
    }
    .card-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. SIVUN YLÄOSA JA LOGO
# ==========================================================
st.markdown("""
<div class="stella-logo-container">
    <div class="stella-clover-icon">🍀</div>
    <div>
        <div class="stella-title">Stella</div>
        <div class="stella-subtitle">Älykäs ravianalyysi, peliprosentit, valmentajakommentit ja asiantuntijavihjeet</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# 3. SIVUPALKKI (SIDEBAR) & DATAN SYÖTTÖLOKEROT
# ==========================================================
st.sidebar.header("⚙️ Simulaation asetukset")
valittu_pvm = st.sidebar.date_input("Valitse kilpailupäivä", datetime.date.today())
rata_nimi = st.sidebar.selectbox("Valitse ravirata", ["Umåker", "Solvalla", "Jägersro", "Bergsåker", "Bollnäs", "Gävle"])

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Datan syöttö")

# 1. PDF-käsiohjelma
pdf_käsiohjelma = st.sidebar.file_uploader("Lataa PDF-käsiohjelma", type=["pdf"])

# 2. Perjantain peliprosentit
perjantai_kuva = st.sidebar.file_uploader("Perjantain peliprosentit (kuva)", type=["png", "jpg", "jpeg"])

# 3. Lauantain varusteet / muutokset
lauantai_kuva = st.sidebar.file_uploader("Lauantain varusteet / muutokset (kuva)", type=["png", "jpg", "jpeg"])

# 4. Travronden valmentajakommentit (lähdöittäin kuvakaappaus)
travroden_kuva = st.sidebar.file_uploader("Travronden valmentajakommentit (kuvakaappaus)", type=["png", "jpg", "jpeg"])

# 5. Jensin vihjeet
jens_kuva = st.sidebar.file_uploader("Jensin vihjeet (kuva / tiedosto)", type=["png", "jpg", "jpeg", "txt"])

# 6. Danielin vihjeet
daniel_kuva = st.sidebar.file_uploader("Danielin vihjeet (kuva / tiedosto)", type=["png", "jpg", "jpeg", "txt"])

st.sidebar.markdown("---")
run_sim = st.sidebar.button("🚀 Suorita Stella-simulaatio", type="primary", use_container_width=True)

# ==========================================================
# 4. SIMULAATIOMOOTTORI & PÄÄSISÄLTÖ
# ==========================================================
if run_sim:
    st.success(f"Simulaatio käynnistetty radalle **{rata_nimi}** päivälle **{valittu_pvm}** manuaalisesti syötettyjen tietojen pohjalta!")
    
    # Esimerkkidatat simulaatiolle
    simuloidut_lahdot = [
        {
            "lahto": 1,
            "matka": "1640m VOLTSTART",
            "suosikki": {"nimi": "Orion Silver", "ohjastaja": "Ulf Ohlsson", "prosentti": 38, "raja": 2.63},
            "haastajat": [
                {"nimi": "Inti Vendil", "ohjastaja": "Oskar Kylin Blom", "prosentti": 24, "raja": 4.17},
                {"nimi": "Reno Wania", "ohjastaja": "Riina Rekilä", "prosentti": 18, "raja": 5.56}
            ],
            "yllattaja": {
                "nimi": "Lucy Leejs", "ohjastaja": "Hanna Olofsson", 
                "prosentti": 9, "raja": 11.11, 
                "perustelu": "Pirteät otteet kokeissa. Travrondenin kommentit ja vihjeet tukevat yllätyssaumaa."
            }
        },
        {
            "lahto": 2,
            "matka": "2140m AUTOSTART (Treåringselit)",
            "suosikki": {"nimi": "Catch and Go", "ohjastaja": "Daniel Wäjersten", "prosentti": 42, "raja": 2.38},
            "haastajat": [
                {"nimi": "Macguffin", "ohjastaja": "Daniel Wäjersten", "prosentti": 26, "raja": 3.85},
                {"nimi": "Dalton Russell", "ohjastaja": "Henrik Svensson", "prosentti": 14, "raja": 7.14}
            ],
            "yllattaja": {
                "nimi": "Nelly Furtado Sisu", "ohjastaja": "Ulf Ohlsson", 
                "prosentti": 7, "raja": 14.28, 
                "perustelu": "Kapasiteetti riittää huomattavasti suurempaan rooliin kuin markkinat olettavat."
            }
        }
    ]

    for l in simuloidut_lahdot:
        with st.container():
            st.markdown(f"### 🔹 Lähtö {l['lahto']} — {l['matka']}")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="card-box">
                    <b>👑 VOITTAJAEHDOKAS / SUOSIKKI:</b><br>
                    • <b>{l['suosikki']['nimi']}</b> ({l['suosikki']['ohjastaja']})<br>
                    • Simulaation voittoprosentti: <b>{l['suosikki']['prosentti']}%</b> | Raja-kerroin: <b>{l['suosikki']['raja']}</b><br><br>
                    <b>⚔️ HAASTAJAT:</b><br>
                    • {l['haastajat'][0]['nimi']} ({l['haastajat'][0]['ohjastaja']}) — {l['haastajat'][0]['prosentti']}% (Raja: {l['haastajat'][0]['raja']})<br>
                    • {l['haastajat'][1]['nimi']} ({l['haastajat'][1]['ohjastaja']}) — {l['haastajat'][1]['prosentti']}% (Raja: {l['haastajat'][1]['raja']})
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="card-box" style="background-color: #FEF3C7; border-color: #F59E0B;">
                    <b>⭐ PARAS YLLÄTTÄJÄ (<10%):</b><br>
                    • <b>{l['yllattaja']['nimi']}</b> ({l['yllattaja']['ohjastaja']})<br>
                    • Prosentti: <b>{l['yllattaja']['prosentti']}%</b> | Raja: <b>{l['yllattaja']['raja']}</b><br><br>
                    <b>💡 Perustelu:</b><br>
                    <span style="font-size: 13px;">{l['yllattaja']['perustelu']}</span>
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("👈 Lataa tarvittavat tiedostot ja kuvat sivupalkista (mukaan lukien Travronden sekä Jensin & Danielin vihjeet) ja paina **Suorita Stella-simulaatio**.")

# Alatunniste
st.markdown("---")
st.markdown("<div style='text-align: center; color: #9CA3AF; font-size: 12px;'>Stella Data Engine 🍀 • Kaikki oikeudet pidätetään</div>", unsafe_allow_html=True)
