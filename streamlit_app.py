import numpy as np
import pandas as pd
import streamlit as st

# --- STREAMLIT-SIVUN ASETUKSET ---
st.set_page_config(page_title="Solvalla V5 Voittokone", layout="wide")

st.title("🏇 Solvalla V5 - Täydellinen Voittosimulaattori")
st.caption("Fokus vain V5-kohteissa (Lähdöt L8, L9, L10, L11, L12) 100% oikeilla hevosilla.")

# --- KOKO V5-AINEISTO (Täsmälleen kuvakaappaustesi mukainen) ---
data = [
    # ==================== V5-1 / L8 (2140a - Oaks-karsinta 1) ====================
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#1 Fatal Attraction", "Veikkaus_%": 4.0, "Bonus": 1.00, "Perustelu": "Smyygaa sisäradalta tarkan reissun."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#2 I See Tail Lights", "Veikkaus_%": 37.0, "Bonus": 1.12, "Perustelu": "💥 LÄHDÖN SUOSIKKI! Hirmuisessa iskussa (1.10,9a alla)."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#3 Tidig Tooma", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Sisäradalta mukaan."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#4 Jula Donatella", "Veikkaus_%": 2.0, "Bonus": 1.06, "Perustelu": "Ekaa kertaa ilman etukenkiä (barfota fram)."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#5 Illicit Hooch", "Veikkaus_%": 1.0, "Bonus": 1.08, "Perustelu": "Barfota runt om & blinkers."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#6 Bo Katan", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Keskiradalta haastavaa."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#7 Mellby Orkide", "Veikkaus_%": 24.0, "Bonus": 1.18, "Perustelu": "💥 JÄTTI-VARUSTEBONUS! Redén riisuu kengät ekaa kertaa + Kihlström."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#8 Cruiser", "Veikkaus_%": 1.0, "Bonus": 1.02, "Perustelu": "Huippusuku, ulkorata rasittaa."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#9 Zeebreeze", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä vaikeaa."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#10 Procope", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Outsider."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#11 Navy Cut", "Veikkaus_%": 3.0, "Bonus": 1.02, "Perustelu": "Hyvä kiri alla."},
    {"Kohde": "V5-1", "Lähtö": "L8", "Hevonen": "#12 Klara Godiva", "Veikkaus_%": 0.0, "Bonus": 1.08, "Perustelu": "🔥 TAULUAAN PAREMPI! Laukkasi voiton sivu suun."},

    # ==================== V5-2 / L9 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#1 Coloneltomparker", "Veikkaus_%": 52.0, "Bonus": 1.15, "Perustelu": "💥 SELKEÄ KEULASUOSIKKI & VARMA! Vahva 2640m matkalla."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#2 Bravo Desoto", "Veikkaus_%": 2.0, "Bonus": 1.06, "Perustelu": "Första barfota fram, tarkan reissun saaja."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#3 Ulix Turner", "Veikkaus_%": 2.0, "Bonus": 1.10, "Perustelu": "🔥 SKRÄLLBUD! Jepson ratissa, barfota runt om."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#4 Reagan Boko", "Veikkaus_%": 6.0, "Bonus": 1.02, "Perustelu": "Tehnyt tasaisia esityksiä."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#5 Yardbird", "Veikkaus_%": 5.0, "Bonus": 1.00, "Perustelu": "Hyvässä kunnossa."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#6 Banzai Brodde", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Ulkoreunalta haastavaa."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#7 Zarajevo Games", "Veikkaus_%": 28.0, "Bonus": 1.12, "Perustelu": "💥 PÄÄHAASTAJA! Voittanut 5/8 startistaan."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#8 Vancouver Tile", "Veikkaus_%": 0.0, "Bonus": 1.02, "Perustelu": "Björn Goop ratissa, rata 8 haittaa."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#9 John McClane", "Veikkaus_%": 0.0, "Bonus": 1.08, "Perustelu": "Ekaa kertaa barfota runt om ja rycktussar."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#10 Wingait Stefan", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Voittanut 4/5, takarivi haittaa."},
    {"Kohde": "V5-2", "Lähtö": "L9", "Hevonen": "#11 Po Tay Toes", "Veikkaus_%": 3.0, "Bonus": 1.10, "Perustelu": "🔥 SPÄNNANDE UTMANARE! Voittanut 3/4 ja ekaa kertaa barfota fram."},

    # ==================== V5-3 / L10 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#1 In Fine Fettle", "Veikkaus_%": 4.0, "Bonus": 1.04, "Perustelu": "Kengättä edestä & jenkit."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#2 Thor Tooma", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Smyygaa sisällä."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#3 Bourbon Phantasy", "Veikkaus_%": 4.0, "Bonus": 1.10, "Perustelu": "🔥 Wäjerstenin oma valinta hyvältä paikalta."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#4 Kodiak Zet", "Veikkaus_%": 76.0, "Bonus": 1.20, "Perustelu": "💥 KOKO ILLAN PÄÄVARMA & GIGA-SUOSIKKI!"},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#5 Baby Love", "Veikkaus_%": 1.0, "Bonus": 1.12, "Perustelu": "Barfota runt om & jenkit ekaa kertaa."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#6 Neutron Star", "Veikkaus_%": 11.0, "Bonus": 1.06, "Perustelu": "💥 PÄÄHAASTAJA! Ilman etukenkiä sitkeä kuolemanpaikkajyrä."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#7 Crew Lane", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Haastava paikka."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#8 Bys Arigato", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Kaukana kärjestä."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#9 Prince of Euro", "Veikkaus_%": 1.0, "Bonus": 1.10, "Perustelu": "🔥 Luokkaa löytyy, ekaa kertaa barfota runt om."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#10 Pivot Caigoo", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takarivistä."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#11 First Festive Vir", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Takaa vaikeaa."},
    {"Kohde": "V5-3", "Lähtö": "L10", "Hevonen": "#12 Xanthis Lewis", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Kunto piikissä, paha paikka."},

    # ==================== V5-4 / L11 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#1 Mister Never Die", "Veikkaus_%": 3.0, "Bonus": 1.00, "Perustelu": "Sisäradalta hyvään asematilaan."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#2 Gilmore Rice", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Haastaa sisältä."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#3 One Express", "Veikkaus_%": 5.0, "Bonus": 1.04, "Perustelu": "Hyvältä paikalta ehtii kärkitaistoon."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#4 Payback River", "Veikkaus_%": 2.0, "Bonus": 1.00, "Perustelu": "Perussuorittaja."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#5 City Slicker", "Veikkaus_%": 52.0, "Bonus": 1.15, "Perustelu": "💥 LÄHDÖN VALTAISA PÄÄSUOSIKKI! Kihlström ratissa, hirmuinen luokka."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#6 No Hitter", "Veikkaus_%": 8.0, "Bonus": 1.06, "Perustelu": "Björn Goop ratissa, barfota fram."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#7 Napoleon Sisu", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Ulkoreunasta haastavaa."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#8 Tennessee H.C.", "Veikkaus_%": 4.0, "Bonus": 1.02, "Perustelu": "Per Lennartsson kyydissä."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#9 Evert Palema", "Veikkaus_%": 20.0, "Bonus": 1.08, "Perustelu": "🔥 VAHVA HAASTAJA! Takarivistä huolimatta kova vauhtikestävyys."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#10 Global History", "Veikkaus_%": 2.0, "Bonus": 1.02, "Perustelu": "Jepson puikoissa."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#11 Zicken Zacke Zack", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Jorma Kontio ratissa."},
    {"Kohde": "V5-4", "Lähtö": "L11", "Hevonen": "#12 Nordic Dancer", "Veikkaus_%": 0.0, "Bonus": 1.00, "Perustelu": "Paha lähtöpaikka 12."},

    # ==================== V5-5 / L12 (2640a - Kriterium-karsinta) ====================
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#1 Pure Games", "Veikkaus_%": 3.0, "Bonus": 1.10, "Perustelu": "🔥 SPETSBUD! Adrian Kolgjini lataa ykkösestä keulaan."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#2 Long Night Out", "Veikkaus_%": 1.0, "Bonus": 1.06, "Perustelu": "Björn Goop vahvisteena nappipaikalla."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#3 Nanda Devi Cut", "Veikkaus_%": 5.0, "Bonus": 1.15, "Perustelu": "💥 HUIPPUIDEANOSTO! Mats E Djuse puikoissa, ekaa kertaa rycktussar."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#4 Outer Space", "Veikkaus_%": 2.0, "Bonus": 1.02, "Perustelu": "Claes Sjöström ratissa."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#5 Källe", "Veikkaus_%": 1.0, "Bonus": 1.00, "Perustelu": "Ajoissa sisälle."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#6 Vulcan Tile", "Veikkaus_%": 2.0, "Bonus": 1.08, "Perustelu": "Ensimmäistä kertaa barfota runt om."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#7 Ready for Boarding", "Veikkaus_%": 2.0, "Bonus": 1.08, "Perustelu": "💥 E3-VOITTAJA ELOKUULTA! Luokkaa riittää yllätykseen."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#8 Pepper Creation", "Veikkaus_%": 4.0, "Bonus": 1.10, "Perustelu": "STARK OCH FORMSTOPPAD! Skoglund ratissa."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#9 Ideal Kronos", "Veikkaus_%": 9.0, "Bonus": 1.12, "Perustelu": "🔥 MAXADE ÄNDRINGAR! Kihlström + rycktussar & amerikansk vagn."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#10 Turner Ale", "Veikkaus_%": 3.0, "Bonus": 1.04, "Perustelu": "Daniel Wäjersten puikoissa, barfota bak."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#11 Intro", "Veikkaus_%": 35.0, "Bonus": 1.06, "Perustelu": "💥 LÄHDÖN SUOSIKKI! Magnus A Djuse ajamassa."},
    {"Kohde": "V5-5", "Lähtö": "L12", "Hevonen": "#12 Campitj", "Veikkaus_%": 12.0, "Bonus": 1.00, "Perustelu": "Haastava paikka 12."}
]

df = pd.DataFrame(data)

# 1. Suhteellisen todennäköisyyden laskenta V5-kohteissa
df['Painotettu_Osuus'] = df['Veikkaus_%'] * df['Bonus']
df['Arvioitu_Prob_%'] = df.groupby('Kohde')['Painotettu_Osuus'].transform(lambda x: (x / x.sum()) * 100 if x.sum() > 0 else 0)
df['Ero_%'] = df['Arvioitu_Prob_%'] - df['Veikkaus_%']

# --- SIMULAATIO ---
st.sidebar.header("⚙️ Simulaattorin Asetukset")
n_simulations = st.sidebar.slider("Simulaatiotoistojen määrä", min_value=1000, max_value=50000, value=10000, step=1000)
run_sim = st.sidebar.button("🎲 Suorita Lopullinen Simulaatio", type="primary")

if run_sim or 'sim_done' not in st.session_state:
    st.session_state['sim_done'] = True
    sim_results = {}
    for kohde, group in df.groupby('Kohde'):
        probs = group['Arvioitu_Prob_%'].values / 100.0
        probs = probs / probs.sum()
        winners = np.random.choice(group['Hevonen'].values, size=n_simulations, p=probs)
        unique, counts = np.unique(winners, return_counts=True)
        counts_dict = dict(zip(unique, counts))
        sim_results[kohde] = {h: (counts_dict.get(h, 0) / n_simulations) * 100 for h in group['Hevonen'].values}
    
    df['Simuloitu_Voitto_%'] = df.apply(lambda r: sim_results[r['Kohde']][r['Hevonen']], axis=1)

# --- YHTEENVETO ---
st.markdown("---")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("💥 V5-Pelin Varmimmat Pankit (Bankerit)")
    top_bankers = df.sort_values(by='Simuloitu_Voitto_%', ascending=False).groupby('Kohde').first().reset_index()
    top_bankers = top_bankers.sort_values(by='Simuloitu_Voitto_%', ascending=False).head(3)
    for _, r in top_bankers.iterrows():
        st.success(f"**[{r['Kohde']} / {r['Lähtö']}] {r['Hevonen']}** | Simuloitu voitto: **{r['Simuloitu_Voitto_%']:.1f}%** (Veikkaus: {r['Veikkaus_%']}%)")

with col_b:
    st.subheader("💣 V5-Pelin Kuumimmat Alipelatut Jätti-Ideat")
    top_underdogs = df[df['Veikkaus_%'] < 10.0].sort_values(by='Ero_%', ascending=False).head(3)
    for _, r in top_underdogs.iterrows():
        st.warning(f"🔥 **[{r['Kohde']} / {r['Lähtö']}] {r['Hevonen']}** | Pelattu: **{r['Veikkaus_%']:.1f}%** ➔ Simulaatio: **{r['Simuloitu_Voitto_%']:.1f}%** (+{r['Ero_%']:.1f}%)\n\n_{r['Perustelu']}_")

st.markdown("---")
st.header("📊 V5-Kohteet (Täysin Tarkistetut Lähdöt L8 – L12)")

tabs = st.tabs(["V5-1 (L8)", "V5-2 (L9)", "V5-3 (L10)", "V5-4 (L11)", "V5-5 (L12)"])
kohteet_list = ["V5-1", "V5-2", "V5-3", "V5-4", "V5-5"]

for tab, kohde_code in zip(tabs, kohteet_list):
    with tab:
        k_df = df[df['Kohde'] == kohde_code].sort_values(by='Simuloitu_Voitto_%', ascending=False)
        
        lahto_nimi = k_df['Lähtö'].iloc[0]
        st.subheader(f"Lähtö {lahto_nimi} ({kohde_code}) - Simulaatiotulokset")
        
        disp_df = k_df[['Hevonen', 'Veikkaus_%', 'Bonus', 'Simuloitu_Voitto_%', 'Ero_%']].copy()
        disp_df.columns = ['Hevonen', 'Veikkaus %', 'Varuste/H2H Kerroin', 'Simulaatio Voitto %', 'Peliarvo (Ero %)']
        
        st.dataframe(
            disp_df,
            column_config={
                "Veikkaus %": st.column_config.NumberColumn(format="%.1f %%"),
                "Varuste/H2H Kerroin": st.column_config.NumberColumn(format="%.2f"),
                "Simulaatio Voitto %": st.column_config.NumberColumn(format="%.1f %%"),
                "Peliarvo (Ero %)": st.column_config.NumberColumn(format="%+.1f %%"),
            },
            use_container_width=True
        )
        
        st.markdown("### 📝 Analysaattorin kommentit hevosittain:")
        for _, r in k_df.iterrows():
            badge = "🟢 **SUOSIKKI**" if r['Simuloitu_Voitto_%'] > 25 else ("🟡 **HAASTAJA**" if r['Simuloitu_Voitto_%'] > 8 else "⚪ **YLLÄTTÄJÄ**")
            st.markdown(f"{badge} **{r['Hevonen']}** (Simulaatio: **{r['Simuloitu_Voitto_%']:.1f}%** | Pelattu: {r['Veikkaus_%']:.1f}%): {r['Perustelu']}")
