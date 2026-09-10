import streamlit as st

DATABANK = {
    5: {
        "nimi": "Lopp 5 - STL Klass I (V85-1)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a",
        "vihje": "Mats Djuse: 9 Night Hawk on avoimen lähdön ensihevonen. Huomioi myös 2 Hip To Be Square ja vaarallinen 1 T.Wall's Notorius.",
        "hevoset": [
            {"numero": 1, "nimi": "T.Wall's Notorius", "ohjastaja": "Jomar Blekkan", "peruspaino": 1.2},
            {"numero": 2, "nimi": "Hip To Be Square", "ohjastaja": "Per Lennartsson", "peruspaino": 1.3},
            {"numero": 3, "nimi": "Sign Of Times", "ohjastaja": "Tomas Pettersson", "peruspaino": 0.9},
            {"numero": 4, "nimi": "Geisha Road Grif", "ohjastaja": "Jorma Kontio", "peruspaino": 1.0},
            {"numero": 5, "nimi": "Macho Cabrio B.B.", "ohjastaja": "Peter G Norman", "peruspaino": 1.0},
            {"numero": 6, "nimi": "Henessi Kiev", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.8},
            {"numero": 7, "nimi": "Takter", "ohjastaja": "Hans G Eriksson", "peruspaino": 0.6},
            {"numero": 8, "nimi": "Herkules A'lir", "ohjastaja": "Rikard N Skoglund", "peruspaino": 1.0},
            {"numero": 9, "nimi": "Night Hawk", "ohjastaja": "Mats E Djuse", "peruspaino": 1.5},
            {"numero": 10, "nimi": "Huchuy Qosqo", "ohjastaja": "Anders Eriksson", "peruspaino": 0.5},
            {"numero": 11, "nimi": "De Är Hon", "ohjastaja": "Ulf Ohlsson", "peruspaino": 0.4},
            {"numero": 12, "nimi": "Sandsjöns Cantona", "ohjastaja": "Claes Sjöström", "peruspaino": 0.8},
        ]
    },
    6: {
        "nimi": "Lopp 6 - STL Kallblodsdivisionen (V85-2)",
        "matka": "2140m Voltstart",
        "tyyppi": "tasoitus",
        "vihje": "Mats Djuse: 4 Silke Sjarmör on norjalaisvierailijana mielenkiintoinen. Ajokki 5 Ellbert omaa hyvän päivänkunnon.",
        "hevoset": [
            {"numero": 1, "nimi": "Fosshaug Frasse", "ohjastaja": "Michaela B Fransson", "peruspaino": 0.6},
            {"numero": 2, "nimi": "Sangviks Lynet", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.1},
            {"numero": 3, "nimi": "Andarnas Patron", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.9},
            {"numero": 4, "nimi": "Silke Sjarmör", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.4},
            {"numero": 5, "nimi": "Ellbert", "ohjastaja": "Mats E Djuse", "peruspaino": 1.3},
            {"numero": 6, "nimi": "Guli Hektor", "ohjastaja": "Örjan Kihlström", "peruspaino": 0.8},
            {"numero": 7, "nimi": "Tåga Ryker", "ohjastaja": "Ingvar Nyberg", "peruspaino": 0.5},
            {"numero": 8, "nimi": "Teknologen", "ohjastaja": "Robert Skoglund", "peruspaino": 1.2},
            {"numero": 9, "nimi": "Ava Modde", "ohjastaja": "Henrik Svensson", "peruspaino": 0.6},
            {"numero": 10, "nimi": "Re Alkapital", "ohjastaja": "Joakim Eskilsson", "peruspaino": 0.6},
            {"numero": 11, "nimi": "Mira Kiro", "ohjastaja": "Jorma Kontio", "peruspaino": 0.7},
            {"numero": 12, "nimi": "Ersa Frej", "ohjastaja": "Nathalie Blom", "peruspaino": 0.3},
            {"numero": 13, "nimi": "Klack Vidar", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.4},
            {"numero": 14, "nimi": "Blixen", "ohjastaja": "Jan-Olof Johansson", "peruspaino": 0.4},
            {"numero": 15, "nimi": "Guli Em", "ohjastaja": "Marcus Lilius", "peruspaino": 0.4},
        ]
    },
    7: {
        "nimi": "Lopp 7 - STL Gulddivisionen EJ's Guldsko (V85-3)",
        "matka": "1640m Autostart",
        "tyyppi": "guld",
        "vihje": "Mats Djuse: 4 Mizai voi yllättää keulasta. Ajokki 6 Mellby Joker hakee hyvää sijoitusta.",
        "hevoset": [
            {"numero": 1, "nimi": "Before Takeoff", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.3},
            {"numero": 2, "nimi": "Santos De Castella", "ohjastaja": "Marcus Lilius", "peruspaino": 0.6},
            {"numero": 3, "nimi": "Romulus Tooma", "ohjastaja": "Peter G Norman", "peruspaino": 0.4},
            {"numero": 4, "nimi": "Mizai", "ohjastaja": "Per Lennartsson", "peruspaino": 1.4},
            {"numero": 5, "nimi": "Lando Mearas", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.1},
            {"numero": 6, "nimi": "Mellby Joker", "ohjastaja": "Mats E Djuse", "peruspaino": 1.25},
            {"numero": 7, "nimi": "Jerka Sting", "ohjastaja": "Claes Sjöström", "peruspaino": 0.85},
        ]
    },
    8: {
        "nimi": "Lopp 8 - STL Dubbelklasslopp (V85-4)",
        "matka": "2640m Autostart",
        "tyyppi": "dubbelklass",
        "vihje": "Mats Djuse: Todella avoin lähtö, varaa laajasti merkkejä. Ajokki 8 Uno omaa hyvän kapasiteetin.",
        "hevoset": [
            {"numero": 1, "nimi": "Napoleon Sisu", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.8},
            {"numero": 2, "nimi": "Ies Ingusmemory", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.0},
            {"numero": 3, "nimi": "Ytowns Ulrik", "ohjastaja": "Jorma Kontio", "peruspaino": 1.1},
            {"numero": 4, "nimi": "Classique Launcher", "ohjastaja": "Olle Alsén", "peruspaino": 0.5},
            {"numero": 5, "nimi": "Umpteen", "ohjastaja": "Nathalie Blom", "peruspaino": 1.0},
            {"numero": 6, "nimi": "Holiday Island", "ohjastaja": "Anders Eriksson", "peruspaino": 1.3},
            {"numero": 7, "nimi": "Sacrebleu", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.85},
            {"numero": 8, "nimi": "Uno", "ohjastaja": "Mats E Djuse", "peruspaino": 1.1},
            {"numero": 9, "nimi": "Whiskey Majo", "ohjastaja": "Marcus Lilius", "peruspaino": 0.75},
            {"numero": 10, "nimi": "Timotejs Gamble", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.0},
            {"numero": 11, "nimi": "Bear Victor", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.2},
            {"numero": 12, "nimi": "Lion Sisu", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.1},
            {"numero": 13, "nimi": "Jaguar Ima", "ohjastaja": "Fredrik Plassen", "peruspaino": 0.8},
            {"numero": 14, "nimi": "Flat Tire Grue", "ohjastaja": "Oskar Florhed", "peruspaino": 0.4},
            {"numero": 15, "nimi": "Vidar Burge", "ohjastaja": "Claes Sjöström", "peruspaino": 0.9},
        ]
    },
    9: {
        "nimi": "Lopp 9 - Tammer Pokal Kallblods-SM ston (V85-5)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a_sm",
        "vihje": "Mats Djuse: Ajokillani 1 Majblomster on kierroksen vahvimpia voittajaehdokkaita. Kovina haastajina 2 Prinsesse Ness Tjo ja 3 Tekno Tana.",
        "hevoset": [
            {"numero": 1, "nimi": "Majblomster", "ohjastaja": "Mats E Djuse", "peruspaino": 2.2},
            {"numero": 2, "nimi": "Prinsesse Ness Tjo", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.3},
            {"numero": 3, "nimi": "Tekno Tana", "ohjastaja": "Robert Skoglund", "peruspaino": 1.2},
            {"numero": 4, "nimi": "Hulte Alva", "ohjastaja": "Linda S Hedström", "peruspaino": 0.8},
            {"numero": 5, "nimi": "Guli Stina", "ohjastaja": "Ulf Ohlsson", "peruspaino": 0.5},
            {"numero": 6, "nimi": "Hög Decibel", "ohjastaja": "Stig Jarle Röste", "peruspaino": 0.4},
            {"numero": 7, "nimi": "Hulte Annika", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.7},
            {"numero": 8, "nimi": "Jonases Ninja", "ohjastaja": "Jan-Olov Åberg", "peruspaino": 0.5},
            {"numero": 9, "nimi": "Eldida", "ohjastaja": "Ida Eriksson", "peruspaino": 0.3},
            {"numero": 10, "nimi": "Rötungen", "ohjastaja": "Micael Melander", "peruspaino": 0.3},
            {"numero": 11, "nimi": "Saga Kiro", "ohjastaja": "Per Lennartsson", "peruspaino": 0.4},
            {"numero": 12, "nimi": "Ethel", "ohjastaja": "Henrik Svensson", "peruspaino": 0.4},
        ]
    },
    10: {
        "nimi": "Lopp 10 - STL Stodivisionen (V85-6)",
        "matka": "2640m Voltstart",
        "tyyppi": "tasaus",
        "vihje": "Mats Djuse: Ajokki 13 Rupie on hienossa kunnossa, mutta vaatii onnistumisen takamatkalta.",
        "hevoset": [
            {"numero": 1, "nimi": "Sessan Of Man", "ohjastaja": "Henrik Svensson", "peruspaino": 0.5},
            {"numero": 2, "nimi": "Adora Liss", "ohjastaja": "Fredrik Plassen", "peruspaino": 0.6},
            {"numero": 3, "nimi": "Pure Jouline", "ohjastaja": "Linus Lönn", "peruspaino": 0.95},
            {"numero": 4, "nimi": "Grove's Maple Poof", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.25},
            {"numero": 5, "nimi": "Bohemian Maid", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.3},
            {"numero": 6, "nimi": "Kopparmärra", "ohjastaja": "Nathalie Blom", "peruspaino": 1.1},
            {"numero": 7, "nimi": "C'est Ma Course", "ohjastaja": "Lucas H Vikström", "peruspaino": 0.8},
            {"numero": 8, "nimi": "Brionne", "ohjastaja": "Rikard N Skoglund", "peruspaino": 1.25},
            {"numero": 9, "nimi": "Melina Havelock", "ohjastaja": "Carl Johan Jepson", "peruspaino": 0.85},
            {"numero": 10, "nimi": "Ajlexes Gourmand", "ohjastaja": "Tomas Pettersson", "peruspaino": 1.05},
            {"numero": 11, "nimi": "Global Empress", "ohjastaja": "Marcus Lilius", "peruspaino": 0.8},
            {"numero": 12, "nimi": "Danceinthedark F.", "ohjastaja": "Katrin K Frick", "peruspaino": 0.7},
            {"numero": 13, "nimi": "Rupie", "ohjastaja": "Mats E Djuse", "peruspaino": 1.1},
            {"numero": 14, "nimi": "Frida S.H.", "ohjastaja": "Örjan Kihlström", "peruspaino": 0.4},
            {"numero": 15, "nimi": "Kueen Simoni", "ohjastaja": "Claes Sjöström", "peruspaino": 0.6},
        ]
    },
    11: {
        "nimi": "Lopp 11 - STL Bronsdivisionen (V85-7)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a_brons",
        "vihje": "Mats Djuse: Ajokillani 8 Lucky Silver on hyvää toivoa täynnä, mutta lähtöpaika on haastava.",
        "hevoset": [
            {"numero": 1, "nimi": "Bruce Braylon", "ohjastaja": "Per Lennartsson", "peruspaino": 1.2},
            {"numero": 2, "nimi": "Pineapple", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.1},
            {"numero": 3, "nimi": "Graces Bird", "ohjastaja": "Fredrik Plassen", "peruspaino": 1.2},
            {"numero": 4, "nimi": "Mellby Mowgli", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.4},
            {"numero": 5, "nimi": "Ebbot Rice", "ohjastaja": "Linus Lönn", "peruspaino": 0.7},
            {"numero": 6, "nimi": "Jaguar Godiva", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.0},
            {"numero": 7, "nimi": "Don E.Star", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.5},
            {"numero": 8, "nimi": "Lucky Silver", "ohjastaja": "Mats E Djuse", "peruspaino": 1.25},
            {"numero": 9, "nimi": "Elvis T.C.B.", "ohjastaja": "Marcus Lilius", "peruspaino": 0.8},
            {"numero": 10, "nimi": "Gosa Gosing", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.85},
            {"numero": 11, "nimi": "Punchboard", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.6},
            {"numero": 12, "nimi": "Slivovitz Lover", "ohjastaja": "Claes Sjöström", "peruspaino": 0.4},
        ]
    },
    12: {
        "nimi": "Lopp 12 - STL Silverdivisionen (V85-8)",
        "matka": "2140m Autostart",
        "tyyppi": "2140a",
        "vihje": "Mats Djuse: Ajokillani 12 X.O.Kemp on huippukunnossa, mutta ulkorata tuo omat haasteensa juoksuun.",
        "hevoset": [
            {"numero": 1, "nimi": "Lähtö12 Hevonen 1", "ohjastaja": "Ohjastaja 1", "peruspaino": 1.0},
            {"numero": 2, "nimi": "Crowe Motion", "ohjastaja": "Ohjastaja 2", "peruspaino": 1.2},
            {"numero": 3, "nimi": "Lähtö12 Hevonen 3", "ohjastaja": "Ohjastaja 3", "peruspaino": 0.8},
            {"numero": 4, "nimi": "Lähtö12 Hevonen 4", "ohjastaja": "Ohjastaja 4", "peruspaino": 0.6},
            {"numero": 5, "nimi": "Lähtö12 Hevonen 5", "ohjastaja": "Ohjastaja 5", "peruspaino": 1.1},
            {"numero": 6, "nimi": "Killer Rain", "ohjastaja": "Ohjastaja 6", "peruspaino": 1.3},
            {"numero": 7, "nimi": "Brilliant Kid", "ohjastaja": "Ohjastaja 7", "peruspaino": 1.0},
            {"numero": 8, "nimi": "Lähtö12 Hevonen 8", "ohjastaja": "Ohjastaja 8", "peruspaino": 0.4},
            {"numero": 9, "nimi": "Summermusic'nights", "ohjastaja": "Ohjastaja 9", "peruspaino": 0.9},
            {"numero": 10, "nimi": "Lähtö12 Hevonen 10", "ohjastaja": "Ohjastaja 10", "peruspaino": 0.5},
            {"numero": 11, "nimi": "Lähtö12 Hevonen 11", "ohjastaja": "Ohjastaja 11", "peruspaino": 0.4},
            {"numero": 12, "nimi": "X.O.Kemp", "ohjastaja": "Mats E Djuse", "peruspaino": 1.35},
        ]
    }
}

# Käyttöliittymäkomponentit, jotka piirtävät tiedot ruudulle
st.title("Ravikone - V85 Vihjeet ja Tiedot")
st.write("Tässä näytetään tallennetut lähdöt ja Mats Djusen vihjeet.")

for loppu_id, tiedot in DATABANK.items():
    st.subheader(tiedot["nimi"])
    st.write(f"**Matka:** {tiedot['matka']}")
    st.write(f"**Vihje:** {tiedot['vihje']}")
    
    st.write("**Hevoset:**")
    for hevonen in tiedot["hevoset"]:
        st.write(f"- #{hevonen['numero']} **{hevonen['nimi']}** (Ohjastaja: {hevonen['ohjastaja']})")
    
    st.divider()
