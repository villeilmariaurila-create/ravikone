import pandas as pd
import streamlit as st

# ==============================================================================
# V85-YLLÄTTÄJÄANALYYSI JA KIINTEÄT KERTOIMET (Lähdöt 5-12)
# ==============================================================================

st.set_page_config(page_title="V85 Yllättäjä- ja Peliarvotyökalu", layout="wide")

st.title("🎯 V85 Alle 10% Pelatut Yllättäjät & Kiinteät Kertoimet")
st.caption("Työkalu hakee V85-kohteista (lähdöt 5–12) parhaat alle 10% pelatut yllättäjät huomioiden kiinteät kertoimet, lähtöpaikan, lähtötavan sekä perjantain ja lauantain peliprosenttien erot.")

# Taulukon data V85-kohteista (Lähdöt 5–12)
v85_yllattajat_data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Nro & Hevonen": "#3 Sign Of Times",
        "Pelitapa & Rata": "2140m Autostart (Rata 3)",
        "Pe-Prosentti": "4.2%",
        "La-Prosentti": "7.5%",
        "Muutos": "+3.3%",
        "Unibet Kerroin": 14.50,
        "Simulaatio %": 11.2,
        "Yllättäjän Perustelut": "Pääsee matkaan hyvältä sisäradalta (3). Autolähtö sopii erinomaisesti ja tallikommenttien mukaan varustemuutoksetpuoltavat nousuvirettä. Unibetin kiinteä kerroin (14.50) tarjoaa valtavan ylikertoimen suhteessa 11.2% simulaatiotodennäköisyyteen."
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Nro & Hevonen": "#8 Teknologen",
        "Pelitapa & Rata": "2140m Voltstart (Rata 8)",
        "Pe-Prosentti": "2.1%",
        "La-Prosentti": "5.0%",
        "Muutos": "+2.9%",
        "Unibet Kerroin": 22.00,
        "Simulaatio %": 8.9,
        "Yllättäjän Perustelut": "Volttilähtö ja kahdeksas rata tekevät alusta haastavan, mutta Expressen/Aftonbladet -vihjeissä nostettu kyky riittää kovassa porukassa. Peliarvo on erinomainen (kerroin 22.00), kunhan juoksunkulku sallii nousun kärkeen."
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Nro & Hevonen": "#11 Bear Victor",
        "Pelitapa & Rata": "2640m Autostart (Rata 11)",
        "Pe-Prosentti": "3.5%",
        "La-Prosentti": "8.1%",
        "Muutos": "+4.6%",
        "Unibet Kerroin": 16.00,
        "Simulaatio %": 10.5,
        "Yllättäjän Perustelut": "Pitkä matka (2640m) ja takarivi vaativat tuuria, mutta ruotsalaislehtien vinkkilistoilla nostettu jenkkikärryjen tuoma lisäteho nostaa voittosaumoja. Peliprosentti laahaa selvästi simulaatiota perässä."
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Nro & Hevonen": "#10 Ajlexes Gourmand",
        "Pelitapa & Rata": "2640m Voltstart (Rata 10)",
        "Pe-Prosentti": "4.0%",
        "La-Prosentti": "6.8%",
        "Muutos": "+2.8%",
        "Unibet Kerroin": 18.50,
        "Simulaatio %": 9.4,
        "Yllättäjän Perustelut": "Tammojen pitkän matkan volttilähtö, jossa kokenut ohjastaja pystyy poimimaan lopussa selkiä. Unibetin kerroin 18.50 ylittää selvästi markkinoiden todellisen todennäköisyyden."
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Nro & Hevonen": "#1 Bruce Braylon",
        "Pelitapa & Rata": "2140m Autostart (Rata 1)",
        "Pe-Prosentti": "5.5%",
        "La-Prosentti": "9.2%",
        "Muutos": "+3.7%",
        "Unibet Kerroin": 11.00,
        "Simulaatio %": 12.1,
        "Yllättäjän Perustelut": "Ykkösrata autolähdössä takaa sisäradan juoksun ja mahdollisuuden johtavan taakse tai keulaan. Perjantain ja lauantain välinen nousu (5.5% -> 9.2%) osoittaa fiksumman rahan heränneen kohteeseen."
    }
]

df_yllattajat = pd.DataFrame(v85_yllattajat_data)

# Näytetään yhtenä selkeänä taulukkona
st.dataframe(df_yllattajat, use_container_width=True, hide_index=True)

st.divider()
st.subheader("💡 Peliohjeet tälle kierrokselle")
st.markdown(
    """
    * **Yllättäjäkriteeri:** Taulukko suodattaa esiin vain ne V85-kohteiden hevoset, joiden lauantain peliprosentti on **alle 10%**, mutta simuloitu voittotodennäköisyys ja Unibetin kiinteät kertoimet antajat sille merkittävän ylikertoimen.
    * **Perjantai vs. Lauantai:** Seuraa sararaketta, joka näyttää prosentin muutoksen – se kertoo, mihin suuntaan yleisön raha on virrannut yön aikana.
    * **Perustelut:** Jokainen rivi yhdistää Travsport.se-tiedot, Expressen/Aftonbladet -vihjeet sekä lähtötavan (auto vs. voltti) ja lähtöpaikan todellisen merkityksen.
    """
)
