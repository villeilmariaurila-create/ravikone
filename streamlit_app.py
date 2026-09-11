import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI & KERTOIMET
# ==============================================================================

st.set_page_config(
    page_title="V85 Yllättäjä- ja Kerroinvertailutyökalu", layout="wide"
)

# CSS-tyyli taulukon ja korttien parantamiseen
st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)

st.title("🎯 V85 Yllättäjäanalyysi & Prosenttivertailu")
st.caption(
    "Perjantain peliprosentit (klo 15.40) vs. lauantain päivittyneet arvot (Vain alle 10 % pelatut yllättäjät)."
)

# Datan määrittely - mukana vain alle 10 % lauantaina pelatut hevoset
v85_yllattajat_data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#3 Sign Of Times",
        "Rata & Tapa": "2140m Autostart (Rata 3)",
        "Pe-% (15.40)": "4.2%",
        "La-%": "1.0%",
        "Muutos": "-3.2%",
        "Unibet (Pe 15.40)": 14.50,
        "Coolbet (Pe 15.40)": 15.00,
        "Perustelut": "Travronden ja Expressen nostavat tallin nousuvireen esiin. Sisärata (3) ja hyvät varustemuutokset puoltavat menestystä.",
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Hevonen": "#11 Bear Victor",
        "Rata & Tapa": "2640m Autostart (Rata 11)",
        "Pe-% (15.40)": "3.5%",
        "La-%": "1.0%",
        "Muutos": "-2.5%",
        "Unibet (Pe 15.40)": 16.00,
        "Coolbet (Pe 15.40)": 16.50,
        "Perustelut": "Pitkä matka ja takarivi vaativat tuuria, mutta jenkkikärryt tuovat lisätehoja voittotaistoon.",
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Hevonen": "#10 Ajlexes Gourmand",
        "Rata & Tapa": "2640m Voltstart (Rata 10)",
        "Pe-% (15.40)": "4.0%",
        "La-%": "5.0%",
        "Muutos": "+1.0%",
        "Unibet (Pe 15.40)": 18.50,
        "Coolbet (Pe 15.40)": 19.00,
        "Perustelut": "Tammojen pitkän matkan volttilähtö. Kokenut ohjastaja pystyy poimimaan lopussa tarvittavat selät.",
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Hevonen": "#1 Bruce Braylon",
        "Rata & Tapa": "2140m Autostart (Rata 1)",
        "Pe-% (15.40)": "5.5%",
        "La-%": "4.0%",
        "Muutos": "-1.5%",
        "Unibet (Pe 15.40)": 11.00,
        "Coolbet (Pe 15.40)": 12.00,
        "Perustelut": "Ykkösrata takaa sisäradan juoksun ja mahdollisuuden keulaan tai johtavan taakse.",
    },
]

df_yllattajat = pd.DataFrame(v85_yllattajat_data)

# Näytetään päätaulukko Streamlitissa
st.dataframe(df_yllattajat, use_container_width=True, hide_index=True)

st.divider()

# Tarkemmat perustelut korteina
st.subheader("📖 Tarkemmat perustelut ja analyysit kohdekohtaisesti")

for item in v85_yllattajat_data:
    st.markdown(
        f"""
