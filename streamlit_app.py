import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="V85 Odotusarvo- ja Simulaatiotyökalu (Kotirata Painotettu)",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 V85 Simulaatiotyökalu – Kotirata- ja Datapainotettu")
st.caption(
    "Färjestad – Mukana dynaaminen kotiradan hevosten lista, matemaattinen"
    " simulaatio ja Unibetin kertoimet."
)

# ----------------- KOTIRADAN HEVOSLISTA (FÄRJESTAD) -----------------
# Erillinen lista kotiradan hevosista, niiden arvioista ja perusteluista
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

# ----------------- SELITYSLAATIKKO KÄYTTÖLIITTYMÄSSÄ -----------------
with st.expander("ℹ️ Miten simulaatio ja kotiratapainotus toimivat?", expanded=False):
    st.markdown(
        """
    **Laskentalogiikka:**
    * **Data-Arvio %**: Pohjautuu markkinakertoimiin ja objektiiviseen todennäköisyysjakaumaan.
    * **Kotirata-Bonus**: Färjestadin kotiradalla kilpailevat hevoset saavat pienen paikallistuntemusbonuksen (erillisestä kotirata-listasta).
    * **Odotusarvo (EV)**: `(Lopullinen Arvio % / 100) * Paras Kerroin`. Yli 1.0 arvot nostavat esiin parhaat pelikohteet.
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

# ----------------- V85 LÄHDÖT & PÄÄDATAT -----------------
vihjeet_data = [
    # --- V85-1 ---
    {
        "Kohde": "V85-1",
        "Hevonen": "#2 Mohawk",
        "Peliprosentti": 62.0,
        "Data_Arvio %": 55.0,
        "Vihje_Paino": 1.02,
        "Unibet": 2.65,
        "Perustelu": "Selvä markkinasuosikki, Goopin tykki kotiradallaan[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#4 Global Grand Slam",
        "Peliprosentti": 6.0,
        "Data_Arvio %": 8.0,
        "Vihje_Paino": 1.05,
        "Unibet": 5.00,
        "Perustelu": "Nopea avaaja, barfota r/o ja Mats E Djuse.",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#6 Kilifi",
        "Peliprosentti": 1.0,
        "Data_Arvio %": 7.0,
        "Vihje_Paino": 1.02,
        "Unibet": 11.00,
        "Perustelu": "💥 Jättiyllättäjä: Matemaattisesti aliarvostettu uusi regi[cite: 4].",
    },
    {
        "Kohde": "V85-1",
        "Hevonen": "#3 Hola Que Tal",
        "Peliprosentti": 4.0,
        "Data_Arvio %": 6.0,
        "Vihje_Paino": 1.00,
        "Unibet": 7.00,
        "Perustelu": "Hyvä lähtöpaikka, Kontio ohjastaa[cite: 4].",
    },
    # --- V85-2 ---
    {
        "Kohde": "V85-2",
        "Hevonen": "#5 Nilla Lane",
        "Peliprosentti": 35.0,
        "Data_Arvio %": 34.0,
        "Vihje_Paino": 1.05,
        "Unibet": 2.75,
        "Perustelu": "Keulapsykologia puoltaa, mutta lievä ylipaino markkinassa[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#6 Skylight",
        "Peliprosentti": 15.0,
        "Data_Arvio %": 22.0,
        "Vihje_Paino": 1.02,
        "Unibet": 2.75,
        "Perustelu": "Norjalainen kovuus, hyvä vastapaino suosikille[cite: 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#10 Monkey Wine",
        "Peliprosentti": 5.0,
        "Data_Arvio %": 15.0,
        "Vihje_Paino": 1.02,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Wäjerstenin kiritykki hyvällä matemaattisella EV:llä[cite: 3, 5].",
    },
    {
        "Kohde": "V85-2",
        "Hevonen": "#9 Panthere d’Inverne",
        "Peliprosentti": 4.0,
        "Data_Arvio %": 14.0,
        "Vihje_Paino": 1.00,
        "Unibet": 9.75,
        "Perustelu": "💥 Yllättäjä: Vahva tamma, alipelattu marginaali[cite: 3, 5].",
    },
    # --- V85-3 ---
    {
        "Kohde": "V85-3",
        "Hevonen": "#3 Pelshin Boko",
        "Peliprosentti": 10.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 1.05,
        "Unibet": 6.75,
        "Perustelu": "Lugauerin tamma, Kontio rattaille, vahva arvio[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#6 Luck Is For Losers",
        "Peliprosentti": 8.0,
        "Data_Arvio %": 26.0,
        "Vihje_Paino": 1.02,
        "Unibet": 8.50,
        "Perustelu": "Viihtyy Färjestadissa, hyvä formi[cite: 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#10 Popup Pellini",
        "Peliprosentti": 3.0,
        "Data_Arvio %": 24.0,
        "Vihje_Paino": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Ikäluokkakarsintojen kovuus tuottaa tulosta[cite: 3, 6].",
    },
    {
        "Kohde": "V85-3",
        "Hevonen": "#7 Lotusorchide",
        "Peliprosentti": 12.0,
        "Data_Arvio %": 22.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.00,
        "Perustelu": "Tasainen suorittaja[cite: 6].",
    },
    # --- V85-4 ---
    {
        "Kohde": "V85-4",
        "Hevonen": "#3 Grisle Tore G.L.",
        "Peliprosentti": 33.0,
        "Data_Arvio %": 44.0,
        "Vihje_Paino": 1.05,
        "Unibet": 2.20,
        "Perustelu": "Vahva simulaatiopisteytys, selvä ykkönen tähän lähtöön[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#7 Tangen Bork",
        "Peliprosentti": 33.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 0.98,
        "Unibet": 4.25,
        "Perustelu": "Tjomslandin hevonen, mutta laukkariski painaa vähän vastaan[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#4 Gigant Tider",
        "Peliprosentti": 10.0,
        "Data_Arvio %": 18.0,
        "Vihje_Paino": 1.02,
        "Unibet": 6.25,
        "Perustelu": "Keulapotentiaali nostaa odotusarvoa[cite: 7, 11].",
    },
    {
        "Kohde": "V85-4",
        "Hevonen": "#6 Baias",
        "Peliprosentti": 5.0,
        "Data_Arvio %": 10.0,
        "Vihje_Paino": 1.00,
        "Unibet": 10.50,
        "Perustelu": "💥 Yllättäjä: Aliarvostettu eliittihevonen[cite: 3, 7, 11].",
    },
    # --- V85-5 ---
    {
        "Kohde": "V85-5",
        "Hevonen": "#5 Maverick K.W.",
        "Peliprosentti": 15.0,
        "Data_Arvio %": 42.0,
        "Vihje_Paino": 1.08,
        "Unibet": 3.35,
        "Perustelu": "Matemaattisesti erinomainen EV ja vahva keulasauma[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#1 Fedorov",
        "Peliprosentti": 57.0,
        "Data_Arvio %": 28.0,
        "Vihje_Paino": 0.95,
        "Unibet": 2.35,
        "Perustelu": "Ylipelattu suosikki sisäratahaasteiden vuoksi[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#6 Paw Patrol V.S.",
        "Peliprosentti": 8.0,
        "Data_Arvio %": 18.0,
        "Vihje_Paino": 1.00,
        "Unibet": 7.00,
        "Perustelu": "Nousuvireinen haastaja[cite: 7].",
    },
    {
        "Kohde": "V85-5",
        "Hevonen": "#10 Miguel",
        "Peliprosentti": 5.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.00,
        "Unibet": 15.00,
        "Perustelu": "💥 Yllättäjä: Kihlström ja kova taustaluokka[cite: 3, 7].",
    },
    # --- V85-6 ---
    {
        "Kohde": "V85-6",
        "Hevonen": "#4 Cold Blaze",
        "Peliprosentti": 59.0,
        "Data_Arvio %": 42.0,
        "Vihje_Paino": 0.98,
        "Unibet": 2.20,
        "Perustelu": "Markkinasuosikki, mutta selvästi ylipelattu simulaatioon nähden[cite: 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#8 Oliver Transs R.",
        "Peliprosentti": 1.0,
        "Data_Arvio %": 32.0,
        "Vihje_Paino": 1.05,
        "Unibet": 15.00,
        "Perustelu": "💥 Jättiyllättäjä: Loistava EV pitkälle matkalle barfotabalanssilla[cite: 3, 8].",
    },
    {
        "Kohde": "V85-6",
        "Hevonen": "#2 Mr Explosive H.H.",
        "Peliprosentti": 10.0,
        "Data_Arvio %": 26.0,
        "Vihje_Paino": 1.02,
        "Unibet": 7.00,
        "Perustelu": "Vahva ehdokas keulajuoksuun[cite: 8].",
    },
    # --- V85-7 ---
    {
        "Kohde": "V85-7",
        "Hevonen": "#3 Barack Face",
        "Peliprosentti": 15.0,
        "Data_Arvio %": 36.0,
        "Vihje_Paino": 1.02,
        "Unibet": 5.75,
        "Perustelu": "Tasainen ja nousukuntoinen guld-hevonen[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#4 Get A Wish",
        "Peliprosentti": 20.0,
        "Data_Arvio %": 34.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.50,
        "Perustelu": "Rautainen kovuus[cite: 9].",
    },
    {
        "Kohde": "V85-7",
        "Hevonen": "#9 Loxahatchee",
        "Peliprosentti": 8.0,
        "Data_Arvio %": 30.0,
        "Vihje_Paino": 1.02,
        "Unibet": 6.25,
        "Perustelu": "💥 Yllättäjä: Mielenkiintoinen debytantti isolla kertoimella[cite: 3, 9].",
    },
    # --- V85-8 ---
    {
        "Kohde": "V85-8",
        "Hevonen": "#6 Great Old Dance",
        "Peliprosentti": 38.0,
        "Data_Arvio %": 45.0,
        "Vihje_Paino": 1.05,
        "Unibet": 3.00,
        "Perustelu": "Stayerloppetin ykkössuokki simulaatiossa[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#15 Steady Express",
        "Peliprosentti": 20.0,
        "Data_Arvio %": 26.0,
        "Vihje_Paino": 1.00,
        "Unibet": 4.25,
        "Perustelu": "Vahva fuxi pitkälle matkalle[cite: 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#12 King Okay",
        "Peliprosentti": 3.0,
        "Data_Arvio %": 17.0,
        "Vihje_Paino": 1.00,
        "Unibet": 11.00,
        "Perustelu": "💥 Yllättäjä: Loistava loppuvetäjä kovassa vauhdissa[cite: 3, 10].",
    },
    {
        "Kohde": "V85-8",
        "Hevonen": "#14 Southbeach Volo",
        "Peliprosentti": 2.0,
        "Data_Arvio %": 12.0,
        "Vihje_Paino": 1.00,
        "Unibet": 17.50,
        "Perustelu": "💥 Yllättäjä: Aliarvostettu stayer-kirijä[cite: 3, 10].",
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)


# --- YHDISTETÄÄN KOTIRADAN BONUS LOGIIKKAAN ---
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

# Lasketaan lopullinen arvio % (Data-Arvio * Vihjepaino * Kotirata-Bonus)
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

# ----------------- NÄYTTÖ: KOTIRADAN HEVOSLISTA -----------------
st.subheader("🏠 Färjestadin Kotiradan Hevoset & Paikallisetu")
st.dataframe(df_kotirata, use_container_width=True, hide_index=True)

st.divider()

# ----------------- PÄÄNÄYTTÖ -----------------
st.subheader("📊 Datavetoiset Odotusarvot (EV) + Kotiratapainotus")
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

# 🔥 ALIPELATUT YLLÄTTÄJÄT LÄHDÖTTÄIN
st.subheader(
    "🔥 Matemaattisesti Alipelatut Yllättäjät (< 10 % Peliprosentti)"
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
