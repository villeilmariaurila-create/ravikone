import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI & KERTOIMET (Pe-otusaika klo 15.40)
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Kerroinvertailutyökalu", layout="wide")

# CSS-tyyli taulukolle ja korteille
st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)

st.title("🎯 V85 Yllättäjäanalyysi & Prosenttivertailu")
st.caption("Perjantain peliprosentit (otettu klo 15.40) vs. markkinan tiedot.")

st.divider()

# Datan määrittely ilman painikkeita tai Coolbetia
v85_yllattajat_data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#3 Sign Of Times",
        "Rata & Tapa": "2140m Autostart (Rata 3)",
        "Pe-% (15.40)": "4.2%",
        "La-%": "Ei vielä avattu",
        "Muutos": "Odottaa lauantaita",
        "Unibet (Pe 15.40)": 14.50,
        "Unibet (La)": "Ei vielä avattu",
        "Perustelut": (
            "Travronden ja Expressen nostavat tallin nousuvireen esiin. Sisärata"
            " (3) ja hyvät varustemuutokset puoltavat menestystä."
        ),
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Hevonen": "#8 Teknologen",
        "Rata & Tapa": "2140m Voltstart (Rata 8)",
        "Pe-% (15.40)": "2.1%",
        "La-%": "Ei vielä avattu",
        "Muutos": "Odottaa lauantaita",
        "Unibet (Pe 15.40)": 22.00,
        "Unibet (La)": "Ei vielä avattu",
        "Perustelut": (
            "Travronden Spelin asiantuntijat pitävät tätä jättiyllättäjänä."
            " Haastavasta volttiradasta huolimatta kyky riittää."
        ),
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Hevonen": "#11 Bear Victor",
        "Rata & Tapa": "2640m Autostart (Rata 11)",
        "Pe-% (15.40)": "3.5%",
        "La-%": "Ei vielä avattu",
        "Muutos": "Odottaa lauantaita",
        "Unibet (Pe 15.40)": 16.00,
        "Unibet (La)": "Ei vielä avattu",
        "Perustelut": (
            "Pitkä matka ja takarivi vaativat tuuria, mutta jenkkikärryt tuovat"
            " lisätehoja voittotaistoon."
        ),
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Hevonen": "#10 Ajlexes Gourmand",
        "Rata & Tapa": "2640m Voltstart (Rata 10)",
        "Pe-% (15.40)": "4.0%",
        "La-%": "Ei vielä avattu",
        "Muutos": "Odottaa lauantaita",
        "Unibet (Pe 15.40)": 18.50,
        "Unibet (La)": "Ei vielä avattu",
        "Perustelut": (
            "Tammojen pitkän matkan volttilähtö. Kokenut ohjastaja pystyy"
            " poimimaan lopussa tarvettavat selät."
        ),
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Hevonen": "#1 Bruce Braylon",
        "Rata & Tapa": "2140m Autostart (Rata 1)",
        "Pe-% (15.40)": "5.5%",
        "La-%": "Ei vielä avattu",
        "Muutos": "Odottaa lauantaita",
        "Unibet (Pe 15.40)": 11.00,
        "Unibet (La)": "Ei vielä avattu",
        "Perustelut": (
            "Ykkösrata takaa sisäradan juoksun ja mahdollisuuden keulaan tai"
            " johtavan taakse. Fiksumpi raha herännyt."
        ),
    },
]

df_yllattajat = pd.DataFrame(v85_yllattajat_data)

# Näytetään päätaulukko Streamlitissa
st.dataframe(df_yllattajat, use_container_width=True, hide_index=True)

st.divider()

# Tarkemmat perustelut korteina
st.subheader("📖 Tarkemmat perustelut ja analyysit kohdekohtaisesti")

for item in v85_yllattajat_data:
  card_html = (
      "
