import json
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Päivän Duo Pro - Race Flow & Live Engine",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 Päivän Duo Pro: Bjerke 13.9.2026")
st.caption(
    "Juoksun kulku (Race Flow) + Varustebonukset + Live-EV Laskenta & Bookmarklet"
)

# ----------------- 1. ALUSTAVAT POHJATIEDOT (Bjerke Lähtö 11 & Lähtö 12) -----------------
pd1_raw = [
    {
        "Nro": 1,
        "Hevonen": "Moni Elite",
        "P_Oma_Base": 3.0,
        "P_Peli %": 3.5,
        "Kerroin": 22.0,
        "Kiihdytys": 3,
        "Keulahalu": False,
    },
    {
        "Nro": 2,
        "Hevonen": "Bully Pepper",
        "P_Oma_Base": 8.0,
        "P_Peli %": 7.0,
        "Kerroin": 12.0,
        "Kiihdytys": 4,
        "Keulahalu": False,
    },
    {
        "Nro": 3,
        "Hevonen": "Kaprizov",
        "P_Oma_Base": 42.0,
        "P_Peli %": 48.0,
        "Kerroin": 1.8,
        "Kiihdytys": 5,
        "Keulahalu": True,
    },
    {
        "Nro": 4,
        "Hevonen": "Onyx B.R.",
        "P_Oma_Base": 12.0,
        "P_Peli %": 10.0,
        "Kerroin": 8.0,
        "Kiihdytys": 4,
        "Keulahalu": False,
    },
    {
        "Nro": 5,
        "Hevonen": "Brostile R.",
        "P_Oma_Base": 2.0,
        "P_Peli %": 1.5,
        "Kerroin": 35.0,
        "Kiihdytys": 2,
        "Keulahalu": False,
    },
    {
        "Nro": 6,
        "Hevonen": "El Guerro S.B.",
        "P_Oma_Base": 10.0,
        "P_Peli %": 8.5,
        "Kerroin": 9.5,
        "Kiihdytys": 4,
        "Keulahalu": False,
    },
    {
        "Nro": 7,
        "Hevonen": "Fillip O'Brian",
        "P_Oma_Base": 1.0,
        "P_Peli %": 0.5,
        "Kerroin": 60.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 8,
        "Hevonen": "Megatron",
        "P_Oma_Base": 4.0,
        "P_Peli %": 3.0,
        "Kerroin": 25.0,
        "Kiihdytys": 3,
        "Keulahalu": False,
    },
    {
        "Nro": 9,
        "Hevonen": "Casanova Dream",
        "P_Oma_Base": 6.0,
        "P_Peli %": 5.0,
        "Kerroin": 15.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 10,
        "Hevonen": "Gemstone Aze",
        "P_Oma_Base": 7.0,
        "P_Peli %": 8.0,
        "Kerroin": 11.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 11,
        "Hevonen": "Maserati Salt",
        "P_Oma_Base": 3.0,
        "P_Peli %": 3.0,
        "Kerroin": 25.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 12,
        "Hevonen": "Fargas T.K.",
        "P_Oma_Base": 2.0,
        "P_Peli %": 2.0,
        "Kerroin": 30.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
]

pd2_raw = [
    {
        "Nro": 1,
        "Hevonen": "Lazy Lane",
        "P_Oma_Base": 2.0,
        "P_Peli %": 1.5,
        "Kerroin": 40.0,
        "Kiihdytys": 3,
        "Keulahalu": False,
    },
    {
        "Nro": 2,
        "Hevonen": "I.D. Diamant",
        "P_Oma_Base": 10.0,
        "P_Peli %": 8.0,
        "Kerroin": 11.0,
        "Kiihdytys": 4,
        "Keulahalu": False,
    },
    {
        "Nro": 3,
        "Hevonen": "Supreme Sund",
        "P_Oma_Base": 4.0,
        "P_Peli %": 3.0,
        "Kerroin": 25.0,
        "Kiihdytys": 2,
        "Keulahalu": False,
    },
    {
        "Nro": 4,
        "Hevonen": "Vicious",
        "P_Oma_Base": 5.0,
        "P_Peli %": 4.0,
        "Kerroin": 20.0,
        "Kiihdytys": 3,
        "Keulahalu": False,
    },
    {
        "Nro": 5,
        "Hevonen": "Kentucky Field",
        "P_Oma_Base": 3.0,
        "P_Peli %": 2.5,
        "Kerroin": 30.0,
        "Kiihdytys": 2,
        "Keulahalu": False,
    },
    {
        "Nro": 6,
        "Hevonen": "Genius",
        "P_Oma_Base": 14.0,
        "P_Peli %": 16.0,
        "Kerroin": 6.5,
        "Kiihdytys": 5,
        "Keulahalu": True,
    },
    {
        "Nro": 7,
        "Hevonen": "Burn",
        "P_Oma_Base": 2.0,
        "P_Peli %": 1.5,
        "Kerroin": 50.0,
        "Kiihdytys": 2,
        "Keulahalu": False,
    },
    {
        "Nro": 8,
        "Hevonen": "Moni U.S.A.",
        "P_Oma_Base": 6.0,
        "P_Peli %": 5.0,
        "Kerroin": 15.0,
        "Kiihdytys": 3,
        "Keulahalu": False,
    },
    {
        "Nro": 9,
        "Hevonen": "Coral Coger",
        "P_Oma_Base": 12.0,
        "P_Peli %": 14.0,
        "Kerroin": 7.5,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 10,
        "Hevonen": "Broker Artist",
        "P_Oma_Base": 5.0,
        "P_Peli %": 4.0,
        "Kerroin": 20.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 11,
        "Hevonen": "M.H. Hot Cash",
        "P_Oma_Base": 3.0,
        "P_Peli %": 2.5,
        "Kerroin": 30.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 12,
        "Hevonen": "Nelson Daytona",
        "P_Oma_Base": 8.0,
        "P_Peli %": 10.0,
        "Kerroin": 9.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 13,
        "Hevonen": "Fighter Kronos",
        "P_Oma_Base": 11.0,
        "P_Peli %": 13.0,
        "Kerroin": 8.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 14,
        "Hevonen": "I.D. Exceptional",
        "P_Oma_Base": 2.0,
        "P_Peli %": 2.0,
        "Kerroin": 40.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
    {
        "Nro": 15,
        "Hevonen": "Wishful Order",
        "P_Oma_Base": 13.0,
        "P_Peli %": 13.0,
        "Kerroin": 7.0,
        "Kiihdytys": 1,
        "Keulahalu": False,
    },
]

df_pd1 = pd.DataFrame(pd1_raw)
df_pd2 = pd.DataFrame(pd2_raw)

# ----------------- 2. VARUSTE- JA DYNAMISET ASETUKSET SIVUPALKISSA -----------------
st.sidebar.header("⚙️ Varustemuutokset & Suodatus")

kengat_pois_pd1 = st.sidebar.multiselect(
    "PD-1 Kengät pois (¢¢) [+15%]", df_pd1["Hevonen"].tolist()
)
jenkit_pd1 = st.sidebar.multiselect(
    "PD-1 Jenkkikärryt (J) [+10%]", df_pd1["Hevonen"].tolist()
)

kengat_pois_pd2 = st.sidebar.multiselect(
    "PD-2 Kengät pois (¢¢) [+15%]", df_pd2["Hevonen"].tolist()
)
jenkit_pd2 = st.sidebar.multiselect(
    "PD-2 Jenkkikärryt (J) [+10%]", df_pd2["Hevonen"].tolist()
)

min_ev = st.sidebar.slider("Minimi Odotusarvo (EV)", 0.8, 3.0, 1.1, step=0.05)


# ----------------- 3. DYNAMISET CORRECTION-FUNKTIOT -----------------
def laske_dynamiikka(df, kengat_list, jenkit_list):
    df_out = df.copy()
    df_out["P_Oma_Adj"] = df_out["P_Oma_Base"]

    for idx, row in df_out.iterrows():
        kerroin = 1.0
        if row["Hevonen"] in kengat_list:
            kerroin *= 1.15
        if row["Hevonen"] in jenkit_list:
            kerroin *= 1.10
        df_out.at[idx, "P_Oma_Adj"] *= kerroin

    df_out["Keula_Pisteet"] = (
        df_out["Kiihdytys"] * 2.0
        - (df_out["Nro"] * 0.2)
        + (df_out["Keulahalu"] * 3.0)
    )
    keula_nro = df_out.sort_values(by="Keula_Pisteet", ascending=False).iloc[0][
        "Nro"
    ]
    prassiriski = len(df_out[df_out["Kiihdytys"] >= 5]) >= 2

    for idx, row in df_out.iterrows():
        faktori = 1.0
        if row["Nro"] == keula_nro:
            faktori *= 0.90 if prassiriski else 1.25
        elif prassiriski and row["Nro"] > 8:
            faktori *= 1.20
        df_out.at[idx, "P_Oma_Adj"] *= faktori

    df_out["P_Oma_Final"] = (
        df_out["P_Oma_Adj"] / df_out["P_Oma_Adj"].sum()
    ) * 100
    return df_out, keula_nro, prassiriski


df_pd1_p, keula_1, prassi_1 = laske_dynamiikka(
    df_pd1, kengat_pois_pd1, jenkit_pd1
)
df_pd2_p, keula_2, prassi_2 = laske_dynamiikka(
    df_pd2, kengat_pois_pd2, jenkit_pd2
)

# ----------------- 4. LIVE-DATAN SYÖTTÖ BROWSER BOOKMARKLETILLA -----------------
st.subheader("📥 Veikkauksen Live-Datan Tuonti (Bookmarklet)")
raw_input = st.text_area(
    "Klikkaa 'Hae Duo Prosentit' -kirjanmerkkiä Veikkauksen sivulla ja liimaa data tähän:",
    height=80,
    placeholder="Liimaa leikepöydän JSON-muotoinen teksti tähän...",
)

# ----------------- 5. YHDISTELMIEN MOOTTORI & EV LASKENTA -----------------
T = 0.80  # Veikkauksen Päivän Duon palautusprosentti (80%)
yhdistelmat = []

for _, h1 in df_pd1_p.iterrows():
    for _, h2 in df_pd2_p.iterrows():
        p_oma_combo = (h1["P_Oma_Final"] / 100.0) * (h2["P_Oma_Final"] / 100.0)
        p_peli_combo = (h1["P_Peli %"] / 100.0) * (h2["P_Peli %"] / 100.0)

        est_pool_odds = T / p_peli_combo if p_peli_combo > 0 else 0
        bookie_odds = h1["Kerroin"] * h2["Kerroin"]

        ev_pool = p_oma_combo * est_pool_odds
        ev_bookie = p_oma_combo * bookie_odds

        yhdistelmat.append(
            {
                "Yhdistelmä": f"#{h1['Nro']} {h1['Hevonen']} × #{h2['Nro']} {h2['Hevonen']}",
                "PD1": f"#{h1['Nro']} {h1['Hevonen']}",
                "PD2": f"#{h2['Nro']} {h2['Hevonen']}",
                "Oma %": round(p_oma_combo * 100, 3),
                "Peli %": round(p_peli_combo * 100, 3),
                "Pool Kerroin": round(est_pool_odds, 1),
                "Bookie Kerroin": round(bookie_odds, 1),
                "EV (Pool)": round(ev_pool, 2),
                "EV (Bookie)": round(ev_bookie, 2),
            }
        )

df_duo = pd.DataFrame(yhdistelmat)

# ----------------- 6. VISUAALINEN NÄYTTÖ & SUODATETUT PARHAAT IDEAT -----------------
st.subheader(f"🔥 Ylikertoimiset Päivän Duo Yhdistelmät (EV >= {min_ev})")

ylikertoimet = df_duo[df_duo["EV (Pool)"] >= min_ev].sort_values(
    by="EV (Pool)", ascending=False
)

if not ylikertoimet.empty:
    st.dataframe(
        ylikertoimet[
            [
                "Yhdistelmä",
                "Oma %",
                "Peli %",
                "Pool Kerroin",
                "EV (Pool)",
                "EV (Bookie)",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Ei valitulla minimi EV-rajalla löytyviä yhdistelmiä.")

st.divider()

st.subheader("📊 Kaikki 180 Yhdistelmää Järjestettynä Odotusarvon Mukaiseen Järjestykseen")
st.dataframe(
    df_duo.sort_values(by="EV (Pool)", ascending=False),
    use_container_width=True,
    hide_index=True,
)

# ----------------- 7. TULOSTEN TARKISTUS -----------------
st.divider()
st.subheader("🏁 Merkitse Voittajat Lähdön Jälkeen")

c1, c2 = st.columns(2)
with c1:
    v1 = st.selectbox("PD-1 Voittaja (Lähtö 11)", df_pd1_p["Hevonen"])
with c2:
    v2 = st.selectbox("PD-2 Voittaja (Lähtö 12)", df_pd2_p["Hevonen"])

osuma_row = df_duo[
    (df_duo["PD1"].str.contains(v1)) & (df_duo["PD2"].str.contains(v2))
].iloc[0]

res1, res2, res3 = st.columns(3)
res1.metric("Osuma Yhdistelmä", osuma_row["Yhdistelmä"])
res2.metric("Poolikerroin", f"{osuma_row['Pool Kerroin']:.1f}")
res3.metric("Odotusarvo (EV)", f"{osuma_row['EV (Pool)']:.2f}")

if osuma_row["EV (Pool)"] >= min_ev:
    st.success("✅ TOTEUTUNUT DUO OLI YLIKERTOIMINAN TÄRPI!")
else:
    st.warning("⚠️ Toteutunut Duo oli alipelattu/alikertoiminen kohde.")
