import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Ravianalyysi & Tulosseuranta", page_icon="🏇", layout="wide"
)

# ----------------- SIVUPALKIN ASETUKSET -----------------
st.sidebar.header("⚙️ Pelin Asetukset")

# Valitaan pelimuoto
pelimuoto = st.sidebar.selectbox(
    "Valitse pelimuoto:",
    ["V75", "V86", "V65", "V64", "V5", "V4", "Päivän Duo"],
    index=0,
)

st.title(f"🏇 Ravianalyysi & Tulokset: {pelimuoto}")

# ----------------- DATA (Voit syöttää minkä tahansa pelin tiedot) -----------------
# Esimerkkidata (toimii kaikilla pelimuodoilla):
vihjeet_data = [
    {
        "Kohde": f"{pelimuoto}-1",
        "Hevonen": "#3 Graces Bird",
        "Peliprosentti": 7.0,
        "Unibet": 21.00,
        "Coolbet": 19.00,
        "Perustelu": "Kärkipaikalta huipputärppi.",
    },
    {
        "Kohde": f"{pelimuoto}-2",
        "Hevonen": "#2 Prinsesse Ness Tjo",
        "Peliprosentti": 12.0,
        "Unibet": 9.50,
        "Coolbet": 10.00,
        "Perustelu": "Kihlström ohjastajana, vahva loppuveto.",
    },
]

tulokset_data = [
    {"Kohde": f"{pelimuoto}-1", "Voittaja": "#3 Graces Bird", "Peli_pct": 9.23},
    {
        "Kohde": f"{pelimuoto}-2",
        "Voittaja": "#2 Prinsesse Ness Tjo",
        "Peli_pct": 12.53,
    },
]

df_vihjeet = pd.DataFrame(vihjeet_data)
df_tulokset = pd.DataFrame(tulokset_data)

# ----------------- LASKENTA & LOGIIKKA -----------------
if not df_vihjeet.empty:
    df_vihjeet["Paras Kerroin"] = df_vihjeet[["Unibet", "Coolbet"]].max(axis=1)

    # Tarkistetaan osumat automaattisesti kohde- ja hevosnumeron perusteella
    df_vihjeet["Voitti"] = df_vihjeet.apply(
        lambda r: any(
            (r["Kohde"] == t["Kohde"])
            and (r["Hevonen"].split()[0] in t["Voittaja"])
            for _, t in df_tulokset.iterrows()
        ),
        axis=1,
    )

    panos = 10.0
    kokonaispanos = len(df_vihjeet) * panos
    voittaneet = df_vihjeet[df_vihjeet["Voitti"]]
    palautus = (voittaneet["Paras Kerroin"] * panos).sum()
    roi = (palautus / kokonaispanos * 100) if kokonaispanos > 0 else 0

    # ----------------- KÄYTTÖLIITTYMÄ -----------------
    st.subheader(f"📊 {pelimuoto} Yhteenveto & ROI")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Vihjattujen määrä", f"{len(df_vihjeet)} kpl")
    m2.metric("Osuneet vihjeet", f"{len(voittaneet)} kpl")
    m3.metric(
        "Netto (10 € tasapanoksella)",
        f"{palautus:.2f} €",
        delta=f"{palautus - kokonaispanos:.2f} €",
    )
    m4.metric("Palautusprosentti (ROI)", f"{roi:.1f} %")

    st.divider()

    st.subheader("🎯 Osuneet Ideat")
    if not voittaneet.empty:
        for _, row in voittaneet.iterrows():
            st.success(
                f"**{row['Kohde']}**: {row['Hevonen']} | "
                f"Kerroin: **{row['Paras Kerroin']:.2f}** | "
                f"Peliosuus: {row['Peliprosentti']}%"
            )
            st.caption(f"Perustelu: {row['Perustelu']}")
    else:
        st.info("Ei osuneita vihjeitä tällä kierroksella.")

    st.divider()

    st.subheader("🏁 Lähtöjen Voittajat ja Vihjeiden Vertailu")
    taulukko = df_tulokset.merge(
        df_vihjeet[df_vihjeet["Voitti"]][
            ["Kohde", "Hevonen", "Paras Kerroin", "Perustelu"]
        ],
        on="Kohde",
        how="left",
    ).fillna("-")

    st.dataframe(taulukko, use_container_width=True, hide_index=True)
else:
    st.warning("Syötä vihjeet analysointia varten.")
