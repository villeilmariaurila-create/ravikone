import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Hagmyren - Yllättäjäsimulaattori", layout="wide"
)

st.title("🏇 V85 Hagmyren: Yllättäjäanalyysi & Kerroinvertailu")
st.caption(
    "Simulaatio käynyt läpi kaikki 100 hevosta. Näytetään alle 10 % pelatut ideavaljakot."
)

data = [
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#5 Macho Cabrio B.B.",
        "Ohjastaja": "Peter G Norman",
        "Peliprosentti": "9.0%",
        "Unibet": 9.50,
        "Coolbet": 10.00,
        "Perustelu": "Tulinen avaaja lukitsee hyvän paikan kärjessä. Kestää kovan matkavauhdin ja pystyy ratkaisemaan lopussa.",
    },
    {
        "Kohde": "V85-1 (Lopp 5)",
        "Hevonen": "#4 Geisha Road Grif",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "5.5%",
        "Unibet": 15.00,
        "Coolbet": 14.50,
        "Perustelu": "Kuntopiikki päällä. Jorma Kontio kyydissä ja nelosradalta taloudellinen reissu keularyhmän takana.",
    },
    {
        "Kohde": "V85-2 (Lopp 6)",
        "Hevonen": "#4 Silke Sjarmör",
        "Ohjastaja": "Carl Johan Jepson",
        "Peliprosentti": "7.0%",
        "Unibet": 12.00,
        "Coolbet": 12.50,
        "Perustelu": "Kapasiteetiltaan vahva kylmäverinen. Vahvistuu Jepsonilla, jolloin kiri kantaa pussituksen vältettäessä.",
    },
    {
        "Kohde": "V85-3 (Lopp 7)",
        "Hevonen": "#4 Mizai",
        "Ohjastaja": "Per Lennartsson",
        "Peliprosentti": "7.5%",
        "Unibet": 11.00,
        "Coolbet": 11.50,
        "Perustelu": "Mailin matkalla erittäin nopea. Iskee sisäradalta heti piikkiin tai johtavan taakse.",
    },
    {
        "Kohde": "V85-4 (Lopp 8)",
        "Hevonen": "#3 Ytowns Ulrik",
        "Ohjastaja": "Jorma Kontio",
        "Peliprosentti": "4.5%",
        "Unibet": 17.00,
        "Coolbet": 18.00,
        "Perustelu": "Pitkälle matkalle vankka jyrä. Jaksaa puskemaan raskaan matkavauhdin loppuun asti.",
    },
    {
        "Kohde": "V85-6 (Lopp 10)",
        "Hevonen": "#3 Pure Jouline",
        "Ohjastaja": "Linus Lönn",
        "Peliprosentti": "4.0%",
        "Unibet": 21.00,
        "Coolbet": 20.00,
        "Perustelu": "Pääskrälli volttilähdöstä. Saa nopean lähdön paalulta, kun suosikit joutuvat kiertämään takamatkalta.",
    },
    {
        "Kohde": "V85-8 (Lopp 12)",
        "Hevonen": "#9 Summermusic'nightS",
        "Ohjastaja": "Marcus Lilius",
        "Peliprosentti": "3.5%",
        "Unibet": 31.00,
        "Coolbet": 33.00,
        "Perustelu": "Kunto huimasti taulua parempi. Ylikovan matkavauhdin toteutuessa syöksyy kirillään mitalitaisteluun.",
    },
]

df = pd.DataFrame(data)

st.subheader("📊 Valitut yllättäjät taulukossa")
st.dataframe(
    df[
        [
            "Kohde",
            "Hevonen",
            "Ohjastaja",
            "Peliprosentti",
            "Unibet",
            "Coolbet",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

st.divider()
st.subheader("🔥 Yllättäjien analyysit ja kertoimet")

for item in data:
    with st.container(border=True):
        st.subheader(f"{item['Kohde']}: {item['Hevonen']}")
        st.write(f"**Ohjastaja:** {item['Ohjastaja']}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Peliprosentti",
                value=item["Peliprosentti"],
                delta="ALLE 10%",
                delta_color="normal",
            )
        with col2:
            st.metric(label="Unibet Kerroin", value=item["Unibet"])
        with col3:
            st.metric(label="Coolbet Kerroin", value=item["Coolbet"])

        st.info(f"**Simulaation analyysi:** {item['Perustelu']}")
