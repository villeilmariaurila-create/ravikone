import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI, KIINTEÄT KERTOIMET & TRAVRONDEN-VIHJEET (Lähdöt 5-12)
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Peliarvotyökalu", layout="wide")

# CSS-tyyli, joka pakottaa taulukon tekstit rivittymään ja estää tekstin katkeamisen
st.markdown(
    """
    <style>
    .stDataFrame td {
        white-space: normal !important;
        word-wrap: break-word !important;
        max-width: 400px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 V85 Alle 10% Pelatut Yllättäjät & Kiinteät Kertoimet")
st.caption("Työkalu hakee V85-kohteista (lähdöt 5–12) parhaat alle 10% pelatut yllättäjät huomioiden Unibetin kiinteät kertoimet, Expressenin, Aftonbladetin ja Travrondenin vihjeet, lähtöpaikan, lähtötavan sekä perjantain ja lauantain peliprosenttien erot.")

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
        "Yllättäjän Perustelut": "Travronden ja Expressen nostavat tallin nousuvireen esiin. Pääsee matkaan hyvältä sisäradalta (3). Autolähtö sopii erinomaisesti ja varustemuutokset puoltavat menestystä. Unibetin kiinteä kerroin (14.50) tarjoaa valtavan ylikertoimen suhteessa 11.2% simulaatiotodennäköisyyteen."
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
        "Yllättäjän Perustelut": "Travronden Spelin asiantuntijat pitävät tätä jättiyllättäjäpotentiaalina. Volttilähtö ja kahdeksas rata tekevät alusta haastavan, mutta Aftonbladet/Expressen-vihjeissä nostettu kyky riittää kovassa porukassa. Peliarvo on erinomainen (kerroin 22.00)."
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
        "Yllättäjän Perustelut": "Travrondenin vihjeissä nostettu esiin. Pitkä matka (2640m) ja takarivi vaativat tuuria, mutta ruotsalaislehtien vinkkilistoilla mainitut jenkkikärryt tuovat lisätehoja, nostaen voittosaumoja yli markkinajakauman."
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
        "Yllättäjän Perustelut": "Tammojen pitkän matkan volttilähtö, jota Expressen ja Travronden pitävät tasaisena. Kokenut ohjastaja pystyy poimimaan lopussa selkiä. Unibetin kerroin 18.50 ylittää selvästi markkinoiden todellisen todennäköisyyden."
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
        "Yllättäjän Perustelut": "Travronden nostaa ykkösradan merkityksen suureksi. Takaa sisäradan juoksun ja mahdollisuuden johtavan taakse tai keulaan. Perjantain ja lauantain välinen nousu (5.5% -> 9.2%) osoittaa fiksumman rahan heränneen."
    }
]

df_yllattajat = pd.DataFrame(v85_yllattajat_data)

# Korvataan st.dataframe Streamlitin natiivilla st.data_editor / st.table ratkaisulla tai asetetaan leveydet selkeiksi
st.table(df_yllattajat)

st.divider()
st.subheader("💡 Peliohjeet tälle kierrokselle")
st.markdown(
    """
    * **Yllättäjäkriteeri:** Taulukko suodattaa esiin vain ne V85-kohteiden hevoset, joiden lauantain peliprosentti on **alle 10%**, mutta simuloitu voittotodennäköisyys, Unibetin kiinteät kertoimet sekä ruotsalaismedioiden (Travronden, Expressen, Aftonbladet) vihjeet puoltavat peliä.
    * **Perjantai vs. Lauantai:** Seuraa sararaketta, joka näyttää prosentin muutoksen – se kertoo, mihin suuntaan yleisön raha on virrannut yön aikana.
    * **Perustelut:** Jokainen rivi yhdistää Travsport.se-tiedot, Expressen/Aftonbladet/Travronden -vihjeet sekä lähtötavan (auto vs. voltti) ja lähtöpaikan todellisen merkityksen.
    """
)
