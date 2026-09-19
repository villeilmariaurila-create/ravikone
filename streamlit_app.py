import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Odotusarvo- ja Simulaatiotyökalu (Päivitetyt Prosentit)",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Simulaatiotyökalu – Päivitetyt Peliprosentit & Kotirata")
st.caption(
    "Färjestad – Mukana tuoreet peliprosentit (L5-L12), Unibetin kertoimet ja"
    " kotirataetu."
)

# ----------------- KOTIRADAN HEVOSLISTA (FÄRJESTAD) -----------------
kotirata_hevostiedot = [
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Goopin valmennettava kilpailee kotiradallaan, iso etu.",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Vahva paikallistuntemus ja sopiva profiili Färjestadiin.",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Kotirata_Bonus": 1.03,
        "Perustelu": "Tottunut Färjestadin kurveihin ja olosuhteisiin.",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Kotirata_Bonus": 1.04,
        "Perustelu": "Kotiradan stayer-taituri, hyötyy radan profiilista.",
    },
]
df_kotirata = pd.DataFrame(kotirata_hevostiedot)

# ----------------- SELITYSLAATIKKO -----------------
with st.expander("ℹ️ Tietoa mallista ja prosenteista", expanded=False):
    st.markdown(
        """
    **Laskentalogiikka:**
    * **Peliprosentit**: Päivitetty suoraan tuoreimmasta pelijakaumasta (L5-L12).
    * **Kotirata-Bonus**: Färjestadin paikalliset hevoset saavat pienen paikallistuntemusbonuksen.
    * **Odotusarvo (EV)**: `(Lopullinen Arvio % / 100) * Paras Kerroin`. Yli 1.0 arvot osoittavat positiivisen odotusarvon.
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

# ----------------- V85 LÄHDÖT & PÄIVITETYT PROSENTIT (L5-L12) -----------------
vihjeet_data = [
    # --- V85-1 (L5) ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 61.0,
        "Data_Arvio %": 55.0,
        "Vihje_Paino": 1.02,
        "Unibet": 2.65,
        "Perustelu": "Edelleen jättisuosikki (61%), Goopin tykki kotiradallaan[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Global Grand Slam",
        "Peliprosentti": 9.0,
        "Data_Arvio %": 9.0,
        "Vihje_Paino": 1.05,
        "Unibet": 5.00,
        "Perustelu": "Noussut 9 prosenttiin, nopea avaaja barfota r/o.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Peliprosentti": 3.0,
        "Data_Arvio %": 7.0,
        "Vihje_Paino": 1.02,
        "Unibet": 11.00,
        "Perustelu": "💥 Jättiyllättäjä (3%): Matemaattisesti aliarvostettu uusi regi[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Hola Que Tal",
        "Peliprosentti": 5.0,
        "Data_Arvio %": 6.0,
        "Vihje_Paino": 1.00,
        "Unibet": 7.00,
        "Perustelu": "Hyvä lähtöpaikka, Kontio ohjastaa[cite: 4].",
    },
    # --- V85-2 (L6) ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "Peliprosentti": 50.0,
        "Data_Arvio %": 45.0,
        "Vihje_Paino": 1.05,
        "Unibet": 2.75,
        "Perustelu": "Pelattu nyt vahvasti (50%), selvä suosikki keulaan[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Skylight",
        "Peliprosentti": 26.0,
        "Data_Arvio %": 25.0,
        "Vihje_Paino": 1.02,
        "Unibet": 2.75,
        "Perustelu": "Noussut 26 prosenttiin, norjalainen kovuus[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#10 Monkey Wine",
        "Peliprosentti": 6.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.02,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä (6%): Wäjerstenin kiritykki hyvällä EV:llä[cite: 3, 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Panthere d’Inverne",
        "Peliprosentti": 4.0,
        "Data_Arvio %": 10.0,
        "Vihje_Paino": 1.00,
        "Unibet": 9.75,
        "Perustelu": "💥 Yllättäjä (4%): Vahva tamma, pysyy hyvänä haastajana[cite: 3, 5].",
    },
    # --- V85-3 (L7) ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "Peliprosentti": 23.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 1.05,
        "Unibet": 6.75,
        "Perustelu": "Kerännyt reilusti peliä (23%), Kontio rattaille[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Peliprosentti": 18.0,
        "Data_Arvio %": 24.0,
        "Vihje_Paino": 1.02,
        "Unibet": 8.50,
        "Perustelu": "Viihtyy Färjestadissa, nostettu 18 prosenttiin[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#10 Popup Pellini",
        "Peliprosentti": 6.0,
        "Data_Arvio %": 20.0,
        "Vihje_Paino": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä (6%): Ikäluokkakarsintojen kovuus tuottaa tulosta[cite: 3, 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "Peliprosentti": 24.0,
        "Data_Arvio %": 20.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.00,
        "Perustelu": "Noussut suosikiksi (24%), tasainen suorittaja[cite: 6].",
    },
    # --- V85-4 (L8) ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Peliprosentti": 38.0,
        "Data_Arvio %": 42.0,
        "Vihje_Paino": 1.05,
        "Unibet": 2.20,
        "Perustelu": "Peliosuus noussut 38 prosenttiin, selvä suosikki kylmäverisissä[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 29.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 0.98,
        "Unibet": 4.25,
        "Perustelu": "Pivenlaskua (29%), Tjomslandin hevonen hakee revanssia[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "Peliprosentti": 17.0,
        "Data_Arvio %": 18.0,
        "Vihje_Paino": 1.02,
        "Unibet": 6.25,
        "Perustelu": "Noussut 17 prosenttiin, vahva keulapotentiaali[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#6 Baias",
        "Peliprosentti": 4.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.00,
        "Unibet": 10.50,
        "Perustelu": "💥 Yllättäjä (4%): Aliarvostettu eliittihevonen[cite: 3, 7, 11].",
    },
    # --- V85-5 (L9) ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 50.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 0.95,
        "Unibet": 2.35,
        "Perustelu": "Jättisuosikki (50%), mutta edelleen riskialtis sisäradalta[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "Peliprosentti": 25.0,
        "Data_Arvio %": 38.0,
        "Vihje_Paino": 1.08,
        "Unibet": 3.35,
        "Perustelu": "Vahvassa nosteessa (25%), erinomainen EV keulajuoksulla[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Paw Patrol V.S.",
        "Peliprosentti": 6.0,
        "Data_Arvio %": 18.0,
        "Vihje_Paino": 1.00,
        "Unibet": 7.00,
        "Perustelu": "💥 Yllättäjä (6%): Nousuvireinen haastaja hyvällä kertoimella[cite: 3, 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#10 Miguel",
        "Peliprosentti": 6.0,
        "Data_Arvio %": 14.0,
        "Vihje_Paino": 1.00,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä (6%): Kihlström ja kova taustaluokka[cite: 3, 7].",
    },
    # --- V85-6 (L10) ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 64.0,
        "Data_Arvio %": 45.0,
        "Vihje_Paino": 0.98,
        "Unibet": 2.20,
        "Perustelu": "Ylipelattu suosikki (64%), simulaation mukaan haavoittuva[cite: 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "Peliprosentti": 3.0,
        "Data_Arvio %": 25.0,
        "Vihje_Paino": 1.05,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä (3%): Loistava haku barfotabalanssilla suosikin varjossa[cite: 3, 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Peliprosentti": 7.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.02,
        "Unibet": 7.00,
        "Perustelu": "Vahva ehdokas keulajuoksuun ja yllätysvalmiudessa[cite: 8].",
    },
    # --- V85-7 (L11) ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#5 Bright Star U.S.",
        "Peliprosentti": 25.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.00,
        "Unibet": 5.75,
        "Perustelu": "Noussut suosikiksi (25%), mutta haasteellinen paikka[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Get A Wish",
        "Peliprosentti": 20.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.50,
        "Perustelu": "Vakaa ja rautainen kovuus (20%)[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Loxahatchee",
        "Peliprosentti": 19.0,
        "Data_Arvio %": 25.0,
        "Vihje_Paino": 1.02,
        "Unibet": 6.25,
        "Perustelu": "Vahvassa nosteessa (19%), Mats E Djuse guld-debyytissä[cite: 3, 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#3 Barack Face",
        "Peliprosentti": 6.0,
        "Data_Arvio %": 15.0,
        "Vihje_Paino": 1.02,
        "Unibet": 5.75,
        "Perustelu": "💥 Yllättäjä (6%): Aliarvostettu huippuhevonen, erinomainen EV[cite: 3, 9].",
    },
    # --- V85-8 (L12) ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 36.0,
        "Data_Arvio %": 40.0,
        "Vihje_Paino": 1.05,
        "Unibet": 3.00,
        "Perustelu": "Stayerloppetin selvä suosikki (36%), Djuse puikoissa[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "Peliprosentti": 23.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.25,
        "Perustelu": "Vahva ja pelattu fuxi pitkälle matkalle (23%)[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#2 Mr Carnation",
        "Peliprosentti": 18.0,
        "Data_Arvio %": 20.0,
        "Vihje_Paino": 1.00,
        "Unibet": 5.75,
        "Perustelu": "Vahva haastaja stayer-matkalle (18%)[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#12 King Okay",
        "Peliprosentti": 1.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Jättiyllättäjä (1%): Loistava loppuvetäjä minimaalisella peliprosentilla[cite: 3, 10].",
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)


# --- KOTIRATABONUS LOGIIKKA ---
def get_kotirata_bonus(kohde, hevonen):
    match = df_kotirata[
        (df_kotirata["Kohde"] == kohde) & (df_kotirata["Hevonen"] == hevonen)
    ]
    if not match.empty:
        return match.iloc[0]["Kotirata_Bonus"]
    return 1.00


df_vihjeet["Kotirata_Bonus"] = df_vihjeet.apply(
    lambda row: get_kotirata_bonus(row["Kohde"], row["Hevonen"]), axis=1
)

df_vihjeet["Lopullinen Arvio %"] = (
    df_vihjeet["Data_Arvio %"]
    * df_vihjeet["Vihje_Paino"]
    * df_vihjeet["Kotirata_Bonus"]
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

# ----------------- NÄYTÖT -----------------
st.subheader("🏠 Färjestadin Kotiradan Hevoset & Paikallisetu")
st.dataframe(df_kotirata, use_container_width=True, hide_index=True)

st.divider()

st.subheader("📊 Päivitetyt Odotusarvot (EV) tuoreilla prosenteilla")
st.dataframe(
    df_vihjeet[
        [
            "Kohde",
            "Hevonen",
            "Peliprosentti",
            "Arvio %",
            "Paras Kerroin",
            "EV",
            "Kotirata_Bonus",
            "Perustelu",
        ]
    ].sort_values(by="EV", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("🔥 Alipelatut Yllättäjät (< 10 % Peliprosentti)")
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
