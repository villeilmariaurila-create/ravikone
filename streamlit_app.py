import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Ravianalyysi & Berglund-Malli",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Keulapainotettu Odotusarvo- ja Simulaatiotyökalu")
st.caption(
    "Färjestad – Mukana Daniel Berglundin vihjeet, keulapainotus ja Unibetin"
    " kertoimet."
)

# ----------------- SELITYSLAATIKKO KÄYTTÖLIITTYMÄSSÄ -----------------
with st.expander(
    "ℹ️ Miten Arvio % ja Keulapainotus lasketaan? (Klikkaa tästä)", expanded=False
):
    st.markdown(
        """
    **Laskentalogiikan selitys:**
    * **Arvio %**: Kuvaa hevosen lopullista, keulapaikalla, radan erityispiirteillä (lyhyt 177m loppusuora) ja asiantuntija-analyysillä korjattua voittotodennäköisyyttä. 
    * **Keulapainotus (Spets-bonus)**: Korottaa todennäköisyyttä niillä hevosilla, joilla on parhaat mahdollisuudet päästä tai hallita keulapaikkaa.
    * **Normalisointi**: Kohdekohtaiset prosentit lasketaan niin, että kunkin lähdön arvioiden summa on tasan 100 %.
    * **Odotusarvo (EV)**: Lasketaan kaavalla `(Arvio % / 100) * Paras Kerroin`. Yli 1.0 arvot kertovat positiivisesta odotusarvosta.
    """
    )

# ----------------- SIVUPALKIN ASETUKSET -----------------
st.sidebar.header("⚙️ Simulaation Asetukset")
panos_per_vihje = st.sidebar.number_input(
    "Panos per vihje (€)", min_value=1.0, value=10.0, step=1.0
)
osuma_raja_ev = st.sidebar.slider(
    "Suodata minimi EV-raja", 0.5, 2.0, 1.0, step=0.05
)
num_simulations = st.sidebar.selectbox(
    "Monte Carlo -simulaatiot", [1000, 5000, 10000, 50000], index=2
)

# ----------------- V85 LÄHDÖT & BERGLUNDIN TIEDOT -----------------
vihjeet_data = [
    # --- V85-1 ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Perus_Arvio %": 50.0,
        "Keula_Bonus": 1.05,
        "Unibet": 2.65,
        "Perustelu": (
            "Ylipelattu jättisuosikki, tekee luultavasti työt ulkoa[cite: 4]."
        ),
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Perus_Arvio %": 9.0,
        "Keula_Bonus": 1.10,
        "Unibet": 5.00,
        "Perustelu": (
            "Berglundin spetsfavorit, barfota r/o ensimmäistä kertaa ja Mats E"
            " Djuse."
        ),
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Peliprosentti": 1.0,
        "Perus_Arvio %": 11.0,
        "Keula_Bonus": 1.05,
        "Unibet": 11.00,
        "Perustelu": "💥 Jättiyllättäjä: Vahva uusi regi, nopea ja tehokas[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Hola Que Tal",
        "Peliprosentti": 4.0,
        "Perus_Arvio %": 10.0,
        "Keula_Bonus": 1.00,
        "Unibet": 7.00,
        "Perustelu": "Hyvä lähtöpaikka, Jorma Kontio vahvistuksena[cite: 4].",
    },
    # --- V85-2 ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "Peliprosentti": 35.0,
        "Perus_Arvio %": 32.0,
        "Keula_Bonus": 1.20,
        "Unibet": 2.75,
        "Perustelu": "Suosikki, hakee aktiivisesti keulapaikkaa[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Skylight",
        "Peliprosentti": 15.0,
        "Perus_Arvio %": 25.0,
        "Keula_Bonus": 1.05,
        "Unibet": 2.75,
        "Perustelu": "Norjalainen huipputamma, vahva haastaja ulkoradoilta[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#10 Monkey Wine",
        "Peliprosentti": 5.0,
        "Perus_Arvio %": 22.0,
        "Keula_Bonus": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Wäjerstenin kova kiritykki[cite: 3, 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Panthere d’Inverne",
        "Peliprosentti": 4.0,
        "Perus_Arvio %": 21.0,
        "Keula_Bonus": 1.00,
        "Unibet": 9.75,
        "Perustelu": "💥 Yllättäjä: Kovan luokan tamma, revanssihaku[cite: 3, 5].",
    },
    # --- V85-3 ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "Peliprosentti": 10.0,
        "Perus_Arvio %": 30.0,
        "Keula_Bonus": 1.15,
        "Unibet": 6.75,
        "Perustelu": "Lugauerin tamma, Kontio rattaille, spetsideea[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Peliprosentti": 8.0,
        "Perus_Arvio %": 28.0,
        "Keula_Bonus": 1.10,
        "Unibet": 8.50,
        "Perustelu": "Kolmen voiton putki, Mats E Djuse, viihtyy Färjestadissa[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#10 Popup Pellini",
        "Peliprosentti": 3.0,
        "Perus_Arvio %": 22.0,
        "Keula_Bonus": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Ikäluokkakarsinnoissa karittu kovuus[cite: 3, 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "Peliprosentti": 12.0,
        "Perus_Arvio %": 20.0,
        "Keula_Bonus": 1.05,
        "Unibet": 4.00,
        "Perustelu": "Tasainen ja sitkeä nelivuotias[cite: 6].",
    },
    # --- V85-4 ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Peliprosentti": 33.0,
        "Perus_Arvio %": 42.0,
        "Keula_Bonus": 1.15,
        "Unibet": 2.20,
        "Perustelu": "Berglundin varma spik! Valtava kehitys ja hirmukunto[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Perus_Arvio %": 30.0,
        "Keula_Bonus": 1.05,
        "Unibet": 4.25,
        "Perustelu": "Tjomslandin huippuhevonen, mutta laukkahuolia[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "Peliprosentti": 10.0,
        "Perus_Arvio %": 18.0,
        "Keula_Bonus": 1.20,
        "Unibet": 6.25,
        "Perustelu": "Spetsfavorit nuoresta iästään huolimatta[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#6 Baias",
        "Peliprosentti": 5.0,
        "Perus_Arvio %": 10.0,
        "Keula_Bonus": 1.00,
        "Unibet": 10.50,
        "Perustelu": "💥 Yllättäjä: Aliarvostettu haastaja elittiin[cite: 3, 7, 11].",
    },
    # --- V85-5 ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "Peliprosentti": 15.0,
        "Perus_Arvio %": 45.0,
        "Keula_Bonus": 1.25,
        "Unibet": 3.35,
        "Perustelu": "Berglundin fräck spik! Ohittaa suosikin kiihdytyksessä[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Perus_Arvio %": 25.0,
        "Keula_Bonus": 0.85,
        "Unibet": 2.35,
        "Perustelu": "Jättisuosikki, mutta innerspår Färjestadissa on riski[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Paw Patrol V.S.",
        "Peliprosentti": 8.0,
        "Perus_Arvio %": 18.0,
        "Keula_Bonus": 1.05,
        "Unibet": 7.00,
        "Perustelu": "Reipas nousuvire, uusia varusteita[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#10 Miguel",
        "Peliprosentti": 5.0,
        "Perus_Arvio %": 12.0,
        "Keula_Bonus": 1.00,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä: Kihlström rattaille, luokkaa taustalla[cite: 3, 7].",
    },
    # --- V85-6 ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Perus_Arvio %": 40.0,
        "Keula_Bonus": 1.05,
        "Unibet": 2.20,
        "Perustelu": "Suosikki, mutta epävarma vire ja herkkä juoksunkululle[cite: 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "Peliprosentti": 1.0,
        "Perus_Arvio %": 32.0,
        "Keula_Bonus": 1.00,
        "Unibet": 15.00,
        "Perustelu": "💥 Jättiyllättäjä: Loistava haku pitkälle matkalle, barfota r/o[cite: 3, 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Peliprosentti": 10.0,
        "Perus_Arvio %": 28.0,
        "Keula_Bonus": 1.15,
        "Unibet": 7.00,
        "Perustelu": "Spetskandidaatti, karkasi viimeksi yllättäjärenkaassa[cite: 8].",
    },
    # --- V85-7 ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#3 Barack Face",
        "Peliprosentti": 15.0,
        "Perus_Arvio %": 38.0,
        "Keula_Bonus": 1.10,
        "Unibet": 5.75,
        "Perustelu": "Positiivinen vire, Adrian Kolgjini, hyvä lähtöpaikka[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Get A Wish",
        "Peliprosentti": 20.0,
        "Perus_Arvio %": 32.0,
        "Keula_Bonus": 1.10,
        "Unibet": 4.50,
        "Perustelu": "Rautainen kovuus Robert Berghin tallista[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Loxahatchee",
        "Peliprosentti": 8.0,
        "Perus_Arvio %": 30.0,
        "Keula_Bonus": 1.00,
        "Unibet": 6.25,
        "Perustelu": "💥 Yllättäjä: Jännittävä guld-debytantti, Mats E Djuse[cite: 3, 9].",
    },
    # --- V85-8 ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Perus_Arvio %": 45.0,
        "Keula_Bonus": 1.20,
        "Unibet": 3.00,
        "Perustelu": "Stayerloppetin suosikki, Mats E Djuse ja loistava keulasauma[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "Peliprosentti": 20.0,
        "Perus_Arvio %": 25.0,
        "Keula_Bonus": 1.00,
        "Unibet": 4.25,
        "Perustelu": "Vahva ja sitkeä fuxi pitkälle matkalle[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#12 King Okay",
        "Peliprosentti": 3.0,
        "Perus_Arvio %": 18.0,
        "Keula_Bonus": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Vahva loppuvetäjä ruotsalaisradoilla[cite: 3, 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#14 Southbeach Volo",
        "Peliprosentti": 2.0,
        "Perus_Arvio %": 12.0,
        "Keula_Bonus": 1.00,
        "Unibet": 17.50,
        "Perustelu": "💥 Yllättäjä: Yllätyshaku pitkään loppuvetoon[cite: 3, 10].",
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)

# --- LASKENTALOGIIKAN TOTEUTUS ---
df_vihjeet["Lopullinen Arvio %"] = (
    df_vihjeet["Perus_Arvio %"] * df_vihjeet["Keula_Bonus"]
)
df_vihjeet["Arvio %"] = df_vihjeet.groupby("Kohde").apply(
    lambda x: x["Lopullinen Arvio %"]
    / x["Lopullinen Arvio %"].sum()
    * 100
).reset_index(level=0, drop=True)

df_vihjeet["Paras Kerroin"] = df_vihjeet["Unibet"]
df_vihjeet["EV"] = (df_vihjeet["Arvio %"] / 100.0) * df_vihjeet[
    "Paras Kerroin"
]

# ----------------- MONTE CARLO SIMULAATIO -----------------
st.sidebar.subheader("🎲 Monte Carlo Ajo")
if st.sidebar.button("Aja Simulaatio"):
    sim_results = []
    kohde_groups = df_vihjeet.groupby("Kohde")
    for _ in range(num_simulations):
        row_win = []
        for kohde, group in kohde_groups:
            probs = group["Arvio %"].values / group["Arvio %"].sum()
            winner_idx = np.random.choice(len(group), p=probs)
            row_win.append(group.iloc[winner_idx]["EV"] >= osuma_raja_ev)
        sim_results.append(all(row_win))
    hit_rate = np.mean(sim_results) * 100
    st.sidebar.success(f"Simulaation osumatodennäköisyys: {hit_rate:.2f} %")

# ----------------- NÄYTTÖ -----------------
st.subheader("📊 Kaikki Kohteet & Keulapainotetut Odotusarvot (EV)")
st.dataframe(
    df_vihjeet[
        [
            "Kohde",
            "Hevonen",
            "Peliprosentti",
            "Arvio %",
            "Paras Kerroin",
            "EV",
            "Perustelu",
        ]
    ].sort_values(by="EV", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# 🔥 ALIPELATUT YLLÄTTÄJÄT LÄHDÖTTÄIN
st.subheader(
    "🔥 Alipelatut Yllättäjät Lähdöittäin (< 10 % Peliprosentti)"
)
df_surprises = df_vihjeet[df_vihjeet["Peliprosentti"] < 10.0]

for kohde in sorted(df_surprises["Kohde"].unique()):
    st.markdown(f"### 📌 {kohde}")
    sub_df = df_surprises[df_surprises["Kohde"] == kohde]
    st.dataframe(
        sub_df[
            [
                "Hevonen",
                "Peliprosentti",
                "Arvio %",
                "Paras Kerroin",
                "EV",
                "Perustelu",
            ]
        ].sort_values(by="EV", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
