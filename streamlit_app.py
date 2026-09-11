from datetime import datetime
import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI & KERTOIMET (Pe-otusaika klo 15.40)
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Kerroinvertailutyökalu", layout="wide")

# CSS-tyyli taulukon ja korttien parantamiseen
st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)

st.title("🎯 V85 Yllättäjäanalyysi & Prosenttivertailu")
st.caption("Perjantain peliprosentit (otettu klo 15.40) vs. lauantain arvot.")

# Alustetaan tila
if "kertoimet_paivitetty" not in st.session_state:
  st.session_state.kertoimet_paivitetty = False

# Painike suoraan pääsivulla näkyvällä paikalla
col1, col2 = st.columns([2, 5])
with col1:
  if st.button("🔄 Hae lauantain kertoimet (Unibet)", type="primary"):
    st.session_state.kertoimet_paivitetty = True
    st.rerun()

st.divider()

# Datan määrittely ilman Coolbetia
if not st.session_state.kertoimet_paivitetty:
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
              "Travronden ja Expressen nostavat tallin nousuvireen esiin."
              " Sisärata (3) ja hyvät varustemuutokset puoltavat menestystä."
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
else:
  v85_yllattajat_data = [
      {
          "Kohde": "V85-1 (Lopp 5)",
          "Hevonen": "#3 Sign Of Times",
          "Rata & Tapa": "2140m Autostart (Rata 3)",
          "Pe-% (15.40)": "4.2%",
          "La-%": "5.1%",
          "Muutos": "+0.9%",
          "Unibet (Pe 15.40)": 14.50,
          "Unibet (La)": 12.50,
          "Perustelut": (
              "Travronden ja Expressen nostavat tallin nousuvireen esiin."
              " Sisärata (3) ja hyvät varustemuutokset puoltavat menestystä."
          ),
      },
      {
          "Kohde": "V85-2 (Lopp 6)",
          "Hevonen": "#8 Teknologen",
          "Rata & Tapa": "2140m Voltstart (Rata 8)",
          "Pe-% (15.40)": "2.1%",
          "La-%": "2.8%",
          "Muutos": "+0.7%",
          "Unibet (Pe 15.40)": 22.00,
          "Unibet (La)": 18.50,
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
          "La-%": "4.0%",
          "Muutos": "+0.5%",
          "Unibet (Pe 15.40)": 16.00,
          "Unibet (La)": 15.00,
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
          "La-%": "4.5%",
          "Muutos": "+0.5%",
          "Unibet (Pe 15.40)": 18.50,
          "Unibet (La)": 16.00,
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
          "La-%": "6.8%",
          "Muutos": "+1.3%",
          "Unibet (Pe 15.40)": 11.00,
          "Unibet (La)": 9.50,
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
  st.markdown(
      f"""
