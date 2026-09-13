import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Päivän Duo - Simulaattori & Perustelut",
    page_icon="🏇",
    layout="wide",
)

st.title("🏇 Päivän Duo - Simulaation Lopputulos & Perustelut")
st.caption(
    "Bjerke 13.9.2026: Taso-erot, todennäköisimmät voittajat ja suurin pelillinen etu (EV)."
)

# ----------------- 1. SIMULAATION LÄHTÖDATA & PERUSTELUT -----------------
pd1_data = [
    {
        "Nro": 1,
        "Hevonen": "Moni Elite",
        "P_Oma %": 3.5,
        "Unibet": 22.0,
        "Veikkaus %": 3.5,
        "Perustelu": "Sisärata auttaa, mutta taso ei riitä aivan kärkeen.",
    },
    {
        "Nro": 2,
        "Hevonen": "Bully Pepper",
        "P_Oma %": 8.5,
        "Unibet": 12.0,
        "Veikkaus %": 7.0,
        "Perustelu": "Hyvä paikka, kykyjä yllätykseen jos keulassa pidetään vauhtia.",
    },
    {
        "Nro": 3,
        "Hevonen": "Kaprizov",
        "P_Oma %": 44.0,
        "Unibet": 1.85,
        "Veikkaus %": 48.0,
        "Perustelu": "Lähdön selkeä ykkössuosikki ja keulahahmo. Erittäin todennäköinen voittaja.",
    },
    {
        "Nro": 4,
        "Hevonen": "Onyx B.R.",
        "P_Oma %": 11.5,
        "Unibet": 8.0,
        "Veikkaus %": 10.0,
        "Perustelu": "Pääsee suosikin vanavedessä hyviin asemiin, ykköshaastaja.",
    },
    {
        "Nro": 5,
        "Hevonen": "Brostile R.",
        "P_Oma %": 2.0,
        "Unibet": 35.0,
        "Veikkaus %": 1.5,
        "Perustelu": "Ulkopuolelta vaikea päästä asemiin.",
    },
    {
        "Nro": 6,
        "Hevonen": "El Guerro S.B.",
        "P_Oma %": 9.5,
        "Unibet": 9.5,
        "Veikkaus %": 8.5,
        "Perustelu": "Vahva puristaja, hyötyy jos avauksessa ajetaan liian kovaa.",
    },
    {
        "Nro": 7,
        "Hevonen": "Fillip O'Brian",
        "P_Oma %": 1.0,
        "Unibet": 60.0,
        "Veikkaus %": 0.5,
        "Perustelu": "Ulkotorven paikka, ei riitä.",
    },
    {
        "Nro": 8,
        "Hevonen": "Megatron",
        "P_Oma %": 4.0,
        "Unibet": 25.0,
        "Veikkaus %": 3.0,
        "Perustelu": "Raskaat asemat luvassa.",
    },
    {
        "Nro": 9,
        "Hevonen": "Casanova Dream",
        "P_Oma %": 5.5,
        "Unibet": 15.0,
        "Veikkaus %": 5.0,
        "Perustelu": "Takarivin paikka vaatii tuureja matkan aikana.",
    },
    {
        "Nro": 10,
        "Hevonen": "Gemstone Aze",
        "P_Oma %": 7.5,
        "Unibet": 11.0,
        "Veikkaus %": 8.0,
        "Perustelu": "Vahva jakso, pystyy nousemaan raskaallakin juoksulla.",
    },
    {
        "Nro": 11,
        "Hevonen": "Maserati Salt",
        "P_Oma %": 3.0,
        "Unibet": 25.0,
        "Veikkaus %": 3.0,
        "Perustelu": "Takarivistä haastava tehtävä.",
    },
    {
        "Nro": 12,
        "Hevonen": "Fargas T.K.",
        "P_Oma %": 2.0,
        "Unibet": 30.0,
        "Veikkaus %": 2.0,
        "Perustelu": "Kapasiteetti ei riitä kärkeen.",
    },
]

pd2_data = [
    {
        "Nro": 1,
        "Hevonen": "Lazy Lane",
        "P_Oma %": 2.0,
        "Unibet": 40.0,
        "Veikkaus %": 1.5,
        "Perustelu": "Arvoituksellinen kunto.",
    },
    {
        "Nro": 2,
        "Hevonen": "I.D. Diamant",
        "P_Oma %": 9.5,
        "Unibet": 11.0,
        "Veikkaus %": 8.0,
        "Perustelu": "Oma kärkipaikka tai hyvä selkäjuoksu luvassa.",
    },
    {
        "Nro": 3,
        "Hevonen": "Supreme Sund",
        "P_Oma %": 4.0,
        "Unibet": 25.0,
        "Veikkaus %": 3.0,
        "Perustelu": "Tasainen suorittaja.",
    },
    {
        "Nro": 4,
        "Hevonen": "Vicious",
        "P_Oma %": 5.0,
        "Unibet": 20.0,
        "Veikkaus %": 4.0,
        "Perustelu": "Sopivalla juoksulla pystyy sijoittumaan.",
    },
    {
        "Nro": 5,
        "Hevonen": "Kentucky Field",
        "P_Oma %": 3.0,
        "Unibet": 30.0,
        "Veikkaus %": 2.5,
        "Perustelu": "Sektorin ulkopuolella.",
    },
    {
        "Nro": 6,
        "Hevonen": "Genius",
        "P_Oma %": 15.0,
        "Unibet": 6.5,
        "Veikkaus %": 16.0,
        "Perustelu": "Erittäin nopea avaaja, todennäköinen keulahevonen ja lähdön suosikki.",
    },
    {
        "Nro": 7,
        "Hevonen": "Burn",
        "P_Oma %": 2.0,
        "Unibet": 50.0,
        "Veikkaus %": 1.5,
        "Perustelu": "Häntäpään hevosia.",
    },
    {
        "Nro": 8,
        "Hevonen": "Moni U.S.A.",
        "P_Oma %": 6.0,
        "Unibet": 15.0,
        "Veikkaus %": 5.0,
        "Perustelu": "Ulkopuolelta paha kiihdytys.",
    },
    {
        "Nro": 9,
        "Hevonen": "Coral Coger",
        "P_Oma %": 12.5,
        "Unibet": 7.5,
        "Veikkaus %": 14.0,
        "Perustelu": "Kunto huipussaan, kova loppuveto takarivistä.",
    },
    {
        "Nro": 10,
        "Hevonen": "Broker Artist",
        "P_Oma %": 5.0,
        "Unibet": 20.0,
        "Veikkaus %": 4.0,
        "Perustelu": "Sopisi yllättäjäksi jos kärki vetää ylikovaa.",
    },
    {
        "Nro": 11,
        "Hevonen": "M.H. Hot Cash",
        "P_Oma %": 3.0,
        "Unibet": 30.0,
        "Veikkaus %": 2.5,
        "Perustelu": "Vaikeat asemat.",
    },
    {
        "Nro": 12,
        "Hevonen": "Nelson Daytona",
        "P_Oma %": 8.5,
        "Unibet": 9.0,
        "Veikkaus %": 10.0,
        "Perustelu": "Nousukuntoinen haastaja.",
    },
    {
        "Nro": 13,
        "Hevonen": "Fighter Kronos",
        "P_Oma %": 11.5,
        "Unibet": 8.0,
        "Veikkaus %": 13.0,
        "Perustelu": "Erittäin vahva esitys viimeksi, taistelee voitosta.",
    },
    {
        "Nro": 14,
        "Hevonen": "I.D. Exceptional",
        "P_Oma %": 2.0,
        "Unibet": 40.0,
        "Veikkaus %": 2.0,
        "Perustelu": "Ulkopaikka verottaa mahdollista menestystä.",
    },
    {
        "Nro": 15,
        "Hevonen": "Wishful Order",
        "P_Oma %": 13.5,
        "Unibet": 7.0,
        "Veikkaus %": 13.0,
        "Perustelu": "Matka sopii ja kunto rautaa. Kierroksen paras pelikohde suosikkiparin muodossa.",
    },
]

df1 = pd.DataFrame(pd1_data)
df2 = pd.DataFrame(pd2_data)

# ----------------- 2. SIMULAATION LASKENTA -----------------
T = 0.80  # Veikkauksen palautusprosentti
yhdistelmat = []

for _, h1 in df1.iterrows():
    for _, h2 in df2.iterrows():
        p_oma_combo = (h1["P_Oma %"] / 100.0) * (h2["P_Oma %"] / 100.0)
        p_peli_combo = (h1["Veikkaus %"] / 100.0) * (h2["Veikkaus %"] / 100.0)

        pooli_kerroin = T / p_peli_combo if p_peli_combo > 0 else 0
        unibet_kerroin = h1["Unibet"] * h2["Unibet"]

        ev_pooli = p_oma_combo * pooli_kerroin
        ev_unibet = p_oma_combo * unibet_kerroin

        yhdistelmat.append(
            {
                "Yhdistelmä": f"#{h1['Nro']} {h1['Hevonen']} × #{h2['Nro']} {h2['Hevonen']}",
                "Todennäköisyys %": round(p_oma_combo * 100, 2),
                "Pooli Kerroin": round(pooli_kerroin, 1),
                "EV (Pooli)": round(ev_pooli, 2),
                "Perustelu": f"PD1: {h1['Perustelu']} | PD2: {h2['Perustelu']}",
            }
        )

df_yhdistelmat = pd.DataFrame(yhdistelmat)

# ----------------- 3. TULOSTEN NÄYTTÖ -----------------
st.subheader("🏆 Simulaation Voittaja-Arviot Lähdöittäin")

col1, col2 = st.columns(2)
with col1:
    st.write("**PD-1 (Lähtö 11) Voittajasuosikki:**")
    v1 = df1.sort_values(by="P_Oma %", ascending=False).iloc[0]
    st.success(
        f"**#{v1['Nro']} {v1['Hevonen']}** ({v1['P_Oma %']} %)\n\n*Perustelu:* {v1['Perustelu']}"
    )

with col2:
    st.write("**PD-2 (Lähtö 12) Voittajasuosikki:**")
    v2 = df2.sort_values(by="P_Oma %", ascending=False).iloc[0]
    st.success(
        f"**#{v2['Nro']} {v2['Hevonen']}** ({v2['P_Oma %']} %)\n\n*Perustelu:* {v2['Perustelu']}"
    )

st.divider()

st.subheader("🔥 Parhaat Pelikohteet Odotusarvon Perusteella (EV >= 1.10)")
parhaat = df_yhdistelmat[df_yhdistelmat["EV (Pooli)"] >= 1.10].sort_values(
    by="EV (Pooli)", ascending=False
)
st.dataframe(
    parhaat[["Yhdistelmä", "Todennäköisyys %", "Pooli Kerroin", "EV (Pooli)"]],
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("📋 Kaikkien Yhdistelmien Analyysi & Perustelut")
st.dataframe(
    df_yhdistelmat.sort_values(by="EV (Pooli)", ascending=False)[
        ["Yhdistelmä", "Todennäköisyys %", "Pooli Kerroin", "EV (Pooli)", "Perustelu"]
    ],
    use_container_width=True,
    hide_index=True,
)
