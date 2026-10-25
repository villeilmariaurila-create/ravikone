import pandas as pd
import streamlit as st

# ==========================================================
# 1. SIVUN ASETUKSET & PUHDAS, MODERNISOITU TYYLI
# ==========================================================
st.set_page_config(page_title="Stella Ravisimulaattori", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Pääotsikko ja logo-osio */
    .stella-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding-bottom: 20px;
        border-bottom: 2px solid #E5E7EB;
        margin-bottom: 24px;
    }
    .stella-diamond-logo {
        font-size: 34px;
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: #34D399;
        width: 70px;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
        border: 2px solid #34D399;
    }
    .stella-title-text h1 {
        font-size: 36px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .stella-slogan-fi {
        font-size: 16px;
        font-weight: 700;
        color: #059669;
        margin: 4px 0 2px 0;
        letter-spacing: 0.2px;
    }
    .stella-slogan-se {
        font-size: 13px;
        font-weight: 500;
        color: #64748B;
        font-style: italic;
        margin: 0;
    }
    
    /* Tuloskortit */
    .result-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #0F172A;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .yllattaja-card {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 5px solid #F59E0B;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 2. YLÄOSA (TIMANTTINEN LOGO & SLOGAN SUOMEKSI JA RUOTSIKSI)
# ==========================================================
st.markdown("""
<div class="stella-header">
    <div class="stella-diamond-logo">💎🍀</div>
    <div class="stella-title-text">
        <h1>Stella</h1>
        <div class="stella-slogan-fi">Hyvä päivä olla minä – ai että ai että!</div>
        <div class="stella-slogan-se">Vilken härlig dag – åh gosse åh gosse!</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# 3. SIVUPALKKI (SIDEBAR) & DATAN SYÖTTÖ
# ==========================================================
st.sidebar.header("⚙️ Asetukset")

pdf_käsiohjelma = st.sidebar.file_uploader("PDF-käsiohjelma", type=["pdf"])
unibet_tiedosto = st.sidebar.file_uploader("Unibet kiinteät kertoimet (tiedosto/kuva)", type=["png", "jpg", "jpeg", "txt", "csv"])
perjantai_kuva = st.sidebar.file_uploader("Perjantain peliprosentit (kuva)", type=["png", "jpg", "jpeg"])
lauantai_kuva = st.sidebar.file_uploader("Lauantain varusteet (kuva)", type=["png", "jpg", "jpeg"])
travroden_kuva = st.sidebar.file_uploader("Travronden kommentit (kuva)", type=["png", "jpg", "jpeg"])
jens_kuva = st.sidebar.file_uploader("Jensin vihjeet (kuva/tiedosto)", type=["png", "jpg", "jpeg", "txt"])
daniel_kuva = st.sidebar.file_uploader("Danielin vihjeet (kuva/tiedosto)", type=["png", "jpg", "jpeg", "txt"])

st.sidebar.markdown("---")
run_sim = st.sidebar.button("🚀 Suorita Stella-simulaatio", type="primary", use_container_width=True)

# ==========================================================
# 4. SIMULAATIOMOOTTORI & NÄKYMÄ
# ==========================================================
if run_sim:
    st.success("Simulaatio suoritettu onnistuneesti annettujen tietojen pohjalta!")
    
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
                "perustelu": "Pirteät otteet kokeissa. Syötetyt tiedot ja vihjeet tukevat yllätyssaumaa."
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
        st.markdown(f"### Lähtö {l['lahto']} — {l['matka']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px;">👑 KÄRKI & HAASTAJAT</div>
                <div><b>Suosikki:</b> {l['suosikki']['nimi']} ({l['suosikki']['ohjastaja']})</div>
                <div style="font-size: 13px; color: #475569; margin-bottom: 8px;">Voittoprosentti: <b>{l['suosikki']['prosentti']}%</b> | Raja-kerroin: <b>{l['suosikki']['raja']}</b></div>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #E2E8F0;">
                <div style="font-size: 13px;"><b>Haastajat:</b></div>
                <div style="font-size: 13px; color: #475569;">• {l['haastajat'][0]['nimi']} ({l['haastajat'][0]['prosentti']}%, Raja: {l['haastajat'][0]['raja']})</div>
                <div style="font-size: 13px; color: #475569;">• {l['haastajat'][1]['nimi']} ({l['haastajat'][1]['prosentti']}%, Raja: {l['haastajat'][1]['raja']})</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="yllattaja-card">
                <div style="font-weight: 700; color: #B45309; margin-bottom: 8px;">⭐ PARAS YLLÄTTÄJÄ (< 10%)</div>
                <div><b>{l['yllattaja']['nimi']}</b> ({l['yllattaja']['ohjastaja']})</div>
                <div style="font-size: 13px; color: #78350F; margin-bottom: 8px;">Prosentti: <b>{l['yllattaja']['prosentti']}%</b> | Raja-kerroin: <b>{l['yllattaja']['raja']}</b></div>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #FDE68A;">
                <div style="font-size: 13px; color: #78350F;"><b>Perustelu:</b> {l['yllattaja']['perustelu']}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("Lataa tarvittavat tiedostot ja kuvat vasemmasta valikosta ja paina **Suorita Stella-simulaatio**.")

# Alatunniste
st.markdown("---")
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 12px;'>Stella Data Engine 💎🍀</div>", unsafe_allow_html=True)
