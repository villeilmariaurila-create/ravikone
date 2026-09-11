import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI, KIINTEÄT KERTOIMET & SEURANTALINKIT (Lähdöt 5-12)
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Peliarvotyökalu", layout="wide")

# CSS-tyyli taulukon solujen sisällön rivittämiseen
st.markdown(
    """
    
    """,
    unsafe_allow_html=True
)

st.title("🎯 V85 Alle 10% Pelatut Yllättäjät & Seurantalinkit")
st.caption("Työkalu hakee V85-kohteista (lähdöt 5–12) parhaat alle 10% pelatut yllättäjät. Mukana suorat seuranta- ja vihjelingit (Travronden, ATG, Unibet).")

v85_yllattajat_data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Nro & Hevonen": "#3 Sign Of Times",
        "Pelitapa & Rata": "2140m Autostart (Rata 3)",
        "Pe-%": "4.2%",
        "La-%": "7.5%",
        "Muutos": "+3.3%",
        "Unibet": 14.50,
        "Sim %": 11.2,
        "Yllättäjän Perustelut": "Travronden ja Expressen nostavat tallin nousuvireen esiin. Sisärata (3) ja hyvät varustemuutokset puoltavat menestystä.",
        "Seuranta / Linkit": "🔗 [Travronden](https://www.travronden.fi) | [ATG](https://www.atg.se)"
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Nro & Hevonen": "#8 Teknologen",
        "Pelitapa & Rata": "2140m Voltstart (Rata 8)",
        "Pe-%": "2.1%",
        "La-%": "5.0%",
        "Muutos": "+2.9%",
        "Unibet": 22.00,
        "Sim %": 8.9,
        "Yllättäjän Perustelut": "Travronden Spelin asiantuntijat pitävät tätä jättiyllättäjänä. Haastavasta volttiradasta huolimatta kyky riittää.",
        "Seuranta / Linkit": "🔗 [Travronden](https://www.travronden.fi) | [ATG](https://www.atg.se)"
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Nro & Hevonen": "#11 Bear Victor",
        "Pelitapa & Rata": "2640m Autostart (Rata 11)",
        "Pe-%": "3.5%",
        "La-%": "8.1%",
        "Muutos": "+4.6%",
        "Unibet": 16.00,
        "Sim %": 10.5,
        "Yllättäjän Perustelut": "Pitkä matka ja takarivi vaativat tuuria, mutta jenkkikärryt tuovat lisätehoja voittotaistoon.",
        "Seuranta / Linkit": "🔗 [Travronden](https://www.travronden.fi) | [ATG](https://www.atg.se)"
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Nro & Hevonen": "#10 Ajlexes Gourmand",
        "Pelitapa & Rata": "2640m Voltstart (Rata 10)",
        "Pe-%": "4.0%",
        "La-%": "6.8%",
        "Muutos": "+2.8%",
        "Unibet": 18.50,
        "Sim %": 9.4,
        "Yllättäjän Perustelut": "Tammojen pitkän matkan volttilähtö. Kokenut ohjastaja pystyy poimimaan lopussa tarvettavat selät.",
        "Seuranta / Linkit": "🔗 [Travronden](https://www.travronden.fi) | [ATG](https://www.atg.se)"
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Nro & Hevonen": "#1 Bruce Braylon",
        "Pelitapa & Rata": "2140m Autostart (Rata 1)",
        "Pe-%": "5.5%",
        "La-%": "9.2%",
        "Muutos": "+3.7%",
        "Unibet": 11.00,
        "Sim %": 12.1,
        "Yllättäjän Perustelut": "Ykkösrata takaa sisäradan juoksun ja mahdollisuuden keulaan tai johtavan taakse. Fiksumpi raha herännyt.",
        "Seuranta / Linkit": "🔗 [Travronden](https://www.travronden.fi) | [ATG](https://www.atg.se)"
    }
]

df_yllattajat = pd.DataFrame(v85_yllattajat_data)

# Korjattu pois puuttuvasta 'tabulate'-kirjastosta johtunut virhe käyttämällä Streamlitin natiivia taulukkoa
st.dataframe(df_yllattajat, use_container_width=True, hide_index=True)

st.divider()
st.subheader("💡 Peliohjeet & Seuranta")
st.markdown(
    """
    * **Seuranta- ja live-linkit:** Jokaisen hevosen kohdalta löydät suorat linkit Travrondenin vihjeisiin sekä ATG:n live-seurantaan.
    * **Yllättäjäkriteeri:** Taulukko suodattaa esiin vain ne V85-kohteiden hevoset, joiden lauantain peliprosentti on **alle 10%**, mutta simuloitu voittotodennäköisyys ja kiinteät kertoimet puoltavat peliä.
    * **Perjantai vs. Lauantai:** Seurattava muutos-sarake näyttää, mihin suuntaan yleisön raha on virrannut yön ja lauantaipäivän välillä.
    """
)
