import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI & KERTOINVERTAILU (Unibet vs. Coolbet)
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Kerroinvertailutyökalu", layout="wide")

# CSS-tyyli taulukon solujen sisällön rivittämiseen
st.markdown(
    """
    
    """,
    unsafe_allow_html=True
)

st.title("🎯 V85 Alle 10% Pelatut Yllättäjät & Kerroinvertailu (Unibet / Coolbet)")
st.caption("Työkalu hakee V85-kohteista (lähdöt 5–12) parhaat alle 10% pelatut yllättäjät ja vertailee kiinteitä kertoimia (Unibet & www.coolbet.fi).")

# Taulukon data V85-kohteista (Lähdöt 5–12) sis. Unibet & Coolbet kertoimet
v85_yllattajat_data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Nro & Hevonen": "#3 Sign Of Times",
        "Pelitapa & Rata": "2140m Autostart (Rata 3)",
        "La-%": "7.5%",
        "Unibet": 14.50,
        "Coolbet": 15.00,
        "Sim %": 11.2,
        "Yllättäjän Perustelut": "Travronden ja Expressen nostavat tallin nousuvireen esiin. Sisärata (3) ja hyvät varustemuutokset puoltavat menestystä."
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Nro & Hevonen": "#8 Teknologen",
        "Pelitapa & Rata": "2140m Voltstart (Rata 8)",
        "La-%": "5.0%",
        "Unibet": 22.00,
        "Coolbet": 21.00,
        "Sim %": 8.9,
        "Yllättäjän Perustelut": "Travronden Spelin asiantuntijat pitävät tätä jättiyllättäjänä. Haastavasta volttiradasta huolimatta kyky riittää."
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Nro & Hevonen": "#11 Bear Victor",
        "Pelitapa & Rata": "2640m Autostart (Rata 11)",
        "La-%": "8.1%",
        "Unibet": 16.00,
        "Coolbet": 16.50,
        "Sim %": 10.5,
        "Yllättäjän Perustelut": "Pitkä matka ja takarivi vaativat tuuria, mutta jenkkikärryt tuovat lisätehoja voittotaistoon."
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Nro & Hevonen": "#10 Ajlexes Gourmand",
        "Pelitapa & Rata": "2640m Voltstart (Rata 10)",
        "La-%": "6.8%",
        "Unibet": 18.50,
        "Coolbet": 19.00,
        "Sim %": 9.4,
        "Yllättäjän Perustelut": "Tammojen pitkän matkan volttilähtö. Kokenut ohjastaja pystyy poimimaan lopussa tarvettavat selät."
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Nro & Hevonen": "#1 Bruce Braylon",
        "Pelitapa & Rata": "2140m Autostart (Rata 1)",
        "La-%": "9.2%",
        "Unibet": 11.00,
        "Coolbet": 12.00,
        "Sim %": 12.1,
        "Yllättäjän Perustelut": "Ykkösrata takaa sisäradan juoksun ja mahdollisuuden keulaan tai johtavan taakse. Fiksumpi raha herännyt."
    }
]

df_yllattajat = pd.DataFrame(v85_yllattajat_data)

# Näytetään päätaulukko Streamlitissa
st.dataframe(df_yllattajat, use_container_width=True, hide_index=True)

st.divider()
st.subheader("💡 Peliohjeet & Kerroinvertailu")
st.markdown(
    """
    * **Kerroinvertailu:** Taulukko näyttää rinnakkain **Unibetin** ja **Coolbetin** kiinteät voittajakertoimet, jotta voit poimia markkinan parhaan palautuksen.
    * **Yllättäjäkriteeri:** Kohteet on rajattu V85-lähtöihin 5–12, joissa hevosen peliprosentti on **alle 10%**, mutta simuloitu voittotodennäköisyys ja kiinteä kerroin antavat selvän ylikertoimen.
    * **Vinkki:** Voit tarkistaa reaaliaikaiset muutokset suoraan osoitteesta [Coolbet Ravit](https://www.coolbet.com/fi/ravit-hub).
    """
)
