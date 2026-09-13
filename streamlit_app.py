
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Päivän Duo - Automaattinen Simulaattori",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 Päivän Duo - Automaattinen EV-Simulaattori")
st.caption(
    "Järjestelmä laskee dynaamiset voittotodennäköisyydet ja tuottaa parhaat Duo-pelikohteet välittömästi."
)

# ----------------- 1. SUORAT KERTOIMET & BASE-DATA -----------------
# Kiinteät kertoimet Unibet / Bookie -kertoimien mukaisesti
pd1_data = [
    {
        "Nro": 1,
        "Hevonen": "Moni Elite",
        "P_Oma %": 3.5,
        "Unibet": 22.0,
        "Veikkaus %": 3.5,
    },
    {
        "Nro": 2,
        "Hevonen": "Bully Pepper",
        "P_Oma %": 8.5,
        "Unibet": 12.0,
        "Veikkaus %": 7.0,
    },
    {
        "Nro": 3,
        "Hevonen": "Kaprizov",
        "P_Oma %": 44.0,
        "Unibet": 1.85,
        "Veikkaus %": 48.0,
    },
    {
        "Nro": 4,
        "Hevonen": "Onyx B.R.",
        "P_Oma %": 11.5,
        "Unibet": 8.0,
        "Veikkaus %": 10.0,
    },
    {
        "Nro": 5,
        "Hevonen": "Brostile R.",
        "P_Oma %": 2.0,
        "Unibet": 35.0,
        "Veikkaus %": 1.5,
    },
    {
        "Nro": 6,
        "Hevonen": "El Guerro S.B.",
        "P_Oma %": 9.5,
        "Unibet": 9.5,
        "Veikkaus %": 8.5,
    },
    {
        "Nro": 7,
        "Hevonen": "Fillip O'Brian",
        "P_Oma %": 1.0,
        "Unibet": 60.0,
        "Veikkaus %": 0.5,
    },
    {
        "Nro": 8,
        "Hevonen": "Megatron",
        "P_Oma %": 4.0,
        "Unibet": 25.0,
        "Veikkaus %": 3.0,
    },
    {
        "Nro": 9,
        "Hevonen": "Casanova Dream",
        "P_Oma %": 5.5,
        "Unibet": 15.0,
        "Veikkaus %": 5.0,
    },
    {
        "Nro": 10,
        "Hevonen": "Gemstone Aze",
        "P_Oma %": 7.5,
        "Unibet": 11.0,
        "Veikkaus %": 8.0,
    },
    {
        "Nro": 11,
        "Hevonen": "Maserati Salt",
        "P_Oma %": 3.0,
        "Unibet": 25.0,
        "Veikkaus %": 3.0,
    },
    {
        "Nro": 12,
        "Hevonen": "Fargas T.K.",
        "P_Oma %": 2.0,
        "Unibet": 30.0,
        "Veikkaus %": 2.0,
    },
]

pd2_data = [
    {
        "Nro": 1,
        "Hevonen": "Lazy Lane",
        "P_Oma %": 2.0,
        "Unibet": 40.0,
        "Veikkaus %": 1.5,
    },
    {
        "Nro": 2,
        "Hevonen": "I.D. Diamant",
        "P_Oma %": 9.5,
        "Unibet": 11.0,
        "Veikkaus %": 8.0,
    },
    {
        "Nro": 3,
        "Hevonen": "Supreme Sund",
        "P_Oma %": 4.0,
        "Unibet": 25.0,
        "Veikkaus %": 3.0,
    },
    {
        "Nro": 4,
        "Hevonen": "Vicious",
        "P_Oma %": 5.0,
        "Unibet": 20.0,
        "Veikkaus %": 4.0,
    },
    {
        "Nro": 5,
        "Hevonen": "Kentucky Field",
        "P_Oma %": 3.0,
        "Unibet": 30.0,
        "Veikkaus %": 2.5,
    },
    {
        "Nro": 6,
        "Hevonen": "Genius",
        "P_Oma %": 15.0,
        "Unibet": 6.5,
        "Veikkaus %": 16.0,
    },
    {
        "Nro": 7,
        "Hevonen": "Burn",
        "P_Oma %": 2.0,
        "Unibet": 50.0,
        "Veikkaus %": 1.5,
    },
    {
        "Nro": 8,
        "Hevonen": "Moni U.S.A.",
        "P_Oma %": 6.0,
        "Unibet": 15.0,
        "Veikkaus %": 5.0,
    },
    {
        "Nro": 9,
        "Hevonen": "Coral Coger",
        "P_Oma %": 12.5,
        "Unibet": 7.5,
        "Veikkaus %": 14.0,
    },
    {
        "Nro": 10,
        "Hevonen": "Broker Artist",
        "P_Oma %": 5.0,
        "Unibet": 20.0,
        "Veikkaus %": 4.0,
    },
    {
        "Nro": 11,
        "Hevonen": "M.H. Hot Cash",
        "P_Oma %": 3.0,
        "Unibet": 30.0,
        "Veikkaus %": 2.5,
    },
    {
        "Nro": 12,
        "Hevonen": "Nelson Daytona",
        "P_Oma %": 8.5,
        "Unibet": 9.0,
        "Veikkaus %": 10.0,
    },
    {
        "Nro": 13,
        "Hevonen": "Fighter Kronos",
        "P_Oma %": 11.5,
        "Unibet": 8.0,
        "Veikkaus %": 13.0,
    },
    {
        "Nro": 14,
        "Hevonen": "I.D. Exceptional",
        "P_Oma %": 2.0,
        "Unibet": 40.0,
        "Veikkaus %": 2.0,
    },
    {
        "Nro": 15,
        "Hevonen": "Wishful Order",
        "P_Oma %": 13.5,
        "Unibet": 7.0,
        "Veikkaus %": 13.0,
    },
]

df1 = pd.DataFrame(pd1_data)
df2 = pd.DataFrame(pd2_data)

# ----------------- 2. AUTOMAATTINEN SIMULAATIO & EV-LASKENTA -----------------
T = 0.80  # Päivän Duon palautusprosentti (80%)
yhdistelmat = []

for _, h1 in df1.iterrows():
    for _, h2 in df2.iterrows():
        p_oma_combo = (h1["P_Oma %"] / 100.0) * (h2["P_Oma %"] / 100.0)
        p_peli_combo = (h1["Veikkaus %"] / 100.0) * (h2["Veikkaus %"] / 100.0)

        # Arvioitu kerroin ja Unibetin yhdistelmäkerroin
        pooli_kerroin = T / p_peli_combo if p_peli_combo > 0 else 0
        unibet_kerroin = h1["Unibet"] * h2["Unibet"]

        # Odotusarvo (EV)
        ev_pooli = p_oma_combo * pooli_kerroin
        ev_unibet = p_oma_combo * unibet_kerroin

        yhdistelmat.append(
            {
                "Yhdistelmä": f"#{h1['Nro']} {h1['Hevonen']} × #{h2['Nro']} {h2['Hevonen']}",
                "Todennäköisyys %": round(p_oma_combo * 100, 2),
                "Pooli Kerroin": round(pooli_kerroin, 1),
                "Unibet Kerroin": round(unibet_kerroin, 1),
                "EV (Pooli)": round(ev_pooli, 2),
                "EV (Unibet)": round(ev_unibet, 2),
            }
        )

df_yhdistelmat = pd.DataFrame(yhdistelmat)

# ----------------- 3. YKSINKERTAINEN NÄKYMÄ & TULOKSET -----------------
st.subheader("🔥 Pelattavat Ylikertoimet (EV >= 1.10)")

parhaat_ideat = df_yhdistelmat[df_yhdistelmat["EV (Pooli)"] >= 1.10].sort_values(
    by="EV (Pooli)", ascending=False
)

if not parhaat_ideat.empty:
    st.dataframe(
        parhaat_ideat[
            [
                "Yhdistelmä",
                "Todennäköisyys %",
                "Pooli Kerroin",
                "Unibet Kerroin",
                "EV (Pooli)",
                "EV (Unibet)",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Kierrokselta ei löydy minimirajan ylittäviä pelikohteita.")

st.divider()

st.subheader("📊 Kaikki Duo-Yhdistelmät (Odotusarvojärjestys)")
st.dataframe(
    df_yhdistelmat.sort_values(by="EV (Pooli)", ascending=False),
    use_container_width=True,
    hide_index=True,
)
