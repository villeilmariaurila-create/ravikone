import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Yllättäjä- ja Kerroinvertailutyökalu", layout="wide"
)

st.title("🎯 V85 Yllättäjäanalyysi & Prosenttivertailu")
st.caption(
    "Automaattinen suodatus: Näytetään vain valjakot, joiden lauantain peliprosentti on enintään 10 %."
)

kaikki_data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#3 Sign Of Times",
        "Rata & Tapa": "2140m Autostart (Rata 3)",
        "Pe-% (15.40)": "4.2%",
        "La-%": "1.0%",
        "Muutos": "-3.2%",
        "Unibet Kerroin": 14.50,
        "Coolbet Kerroin": 15.00,
        "Perustelut": "Travronden ja Expressen nostavat tallin nousuvireen esiin. Sisärata (3) ja hyvät varustemuutokset puoltavat menestystä.",
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Hevonen": "#8 Teknologen",
        "Rata & Tapa": "2140m Voltstart (Rata 8)",
        "Pe-% (15.40)": "2.1%",
        "La-%": "32.0%",
        "Muutos": "+29.9%",
        "Unibet Kerroin": 3.20,
        "Coolbet Kerroin": 3.10,
        "Perustelut": "Peli-intressi heräsi voimakkaasti lauantaina. Suosikiksi noussut valjakko rajautuu pois yllättäjälistalta.",
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Hevonen": "#11 Bear Victor",
        "Rata & Tapa": "2640m Autostart (Rata 11)",
        "Pe-% (15.40)": "3.5%",
        "La-%": "1.0%",
        "Muutos": "-2.5%",
        "Unibet Kerroin": 16.00,
        "Coolbet Kerroin": 16.50,
        "Perustelut": "Pitkä matka ja takarivi vaativat tuuria, mutta jenkkikärryt tuovat lisätehoja voittotaistoon.",
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Hevonen": "#10 Ajlexes Gourmand",
        "Rata & Tapa": "2640m Voltstart (Rata 10)",
        "Pe-% (15.40)": "4.0%",
        "La-%": "5.0%",
        "Muutos": "+1.0%",
        "Unibet Kerroin": 18.50,
        "Coolbet Kerroin": 19.00,
        "Perustelut": "Tammojen pitkän matkan volttilähtö. Kokenut ohjastaja pystyy poimimaan lopussa tarvittavat selät.",
    },
    {
        "Kohde": "V85-7 (Lopp 11)",
        "Hevonen": "#1 Bruce Braylon",
        "Rata & Tapa": "2140m Autostart (Rata 1)",
        "Pe-% (15.40)": "5.5%",
        "La-%": "4.0%",
        "Muutos": "-1.5%",
        "Unibet Kerroin": 11.00,
        "Coolbet Kerroin": 12.00,
        "Perustelut": "Ykkösrata takaa sisäradan juoksun ja mahdollisuuden keulaan tai johtavan taakse.",
    },
]

yllattajat_filtratty = [
    item
    for item in kaikki_data
    if float(item["La-%"].replace("%", "").strip()) <= 10.0
]

df_yllattajat = pd.DataFrame(yllattajat_filtratty)

st.dataframe(df_yllattajat, use_container_width=True, hide_index=True)

st.divider()

st.subheader("📖 Suodatettujen yllättäjien analyysit")

for item in yllattajat_filtratty:
    with st.container(border=True):
        st.subheader(f"{item['Kohde']} - {item['Hevonen']}")
        st.write(f"Rata ja tapa: {item['Rata & Tapa']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Lauantain peliprosentti",
                value=item["La-%"],
                delta=item["Muutos"],
            )
        with col2:
            st.write(f"Perjantain prosentti: {item['Pe-% (15.40)']}")
            st.write(f"Unibet kerroin: {item['Unibet Kerroin']}")
        with col3:
            st.write(f"Coolbet kerroin: {item['Coolbet Kerroin']}")

        st.write(f"Analyysi: {item['Perustelut']}")

st.divider()
st.subheader("💡 Ohjeet ja huomiot")
st.markdown("* Automaattisuodatus poistaa yli 10 % pelatut valjakot.")
st.markdown("* Käytössä Streamlitin omat komponentit ilman pitkiä tekstimuotoiluja.")
