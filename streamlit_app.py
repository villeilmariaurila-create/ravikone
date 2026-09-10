import random
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. LIVE-PELIJAKAUMA & VAIHTO (LÄHDÖT 5-12 KUVAN MUKAAN)
# ==============================================================================

LIVE_PELIJAKAUMA = {
    1: {1: 15, 2: 30, 3: 10, 4: 5, 5: 20, 6: 20},
    2: {1: 8, 2: 12, 3: 40, 4: 10, 5: 15, 6: 15},
    3: {1: 25, 2: 25, 3: 20, 4: 10, 5: 10, 6: 10},
    4: {1: 5, 2: 15, 3: 10, 4: 35, 5: 20, 6: 15},
    5: {1: 3, 2: 25, 3: 1, 4: 5, 5: 10, 6: 4, 7: 2, 8: 11, 9: 35, 10: 1, 11: 1, 12: 1},
    6: {1: 2, 2: 9, 3: 1, 4: 28, 5: 6, 6: 4, 7: 1, 8: 28, 9: 1, 10: 2, 11: 4, 12: 1, 13: 8, 14: 1, 15: 5},
    7: {1: 43, 2: 1, 3: 2, 4: 9, 5: 13, 6: 25, 7: 8},
    8: {1: 2, 2: 3, 3: 12, 4: 1, 5: 3, 6: 35, 7: 2, 8: 15, 9: 2, 10: 3, 11: 1, 12: 14, 13: 3, 14: 1, 15: 2},
    9: {1: 68, 2: 16, 3: 5, 4: 2, 5: 1, 6: 1, 7: 3, 8: 2, 9: 1, 10: 0, 11: 1, 12: 0},
    10: {1: 1, 2: 1, 3: 3, 4: 9, 5: 7, 6: 26, 7: 2, 8: 20, 9: 5, 10: 6, 11: 0, 12: 2, 13: 15, 14: 1, 15: 1},
    11: {1: 5, 2: 6, 3: 3, 4: 52, 5: 2, 6: 6, 7: 1, 8: 12, 9: 1, 10: 8, 11: 2, 12: 1},
    12: {1: 2, 2: 24, 3: 2, 4: 1, 5: 2, 6: 2, 7: 7, 8: 39, 9: 2, 10: 3, 11: 1, 12: 15}
}

LIVE_VAIHTOTIEDOT = {
    "vaihto": "111 435 €",
    "jakosumma": "1 393 258 €",
    "jackpot": "1 320 826 €"
}

# ==============================================================================
# 2. DATA (LÄHDÖT 1-12 MUKAAN LUKIEN VARUSTE- JA KEULAOLETUKSET)
# ==============================================================================

DATABANK = {
    1: {
        "nimi": "Lopp 1 - P21-Lopp (Voittajapeli)", "matka": "2140m Autostart", "tyyppi": "2140a",
        "vihje": "<b>Varustemuutokset:</b> Hevosella 2 laput vaihdettu avoimiin. Keulaolettamus: Hevonen 2.",
        "keula_nro": 2,
        "hevoset": [
            {"numero": 1, "nimi": "Lähtö1 Hevonen 1", "ohjastaja": "Ohjastaja A", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Lähtö1 Hevonen 2", "ohjastaja": "Ohjastaja B", "peruspaino": 1.4, "varuste_muutos": "⚠️ Kengät pois / Sekki muutettu"},
            {"numero": 3, "nimi": "Lähtö1 Hevonen 3", "ohjastaja": "Ohjastaja C", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Lähtö1 Hevonen 4", "ohjastaja": "Ohjastaja D", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Lähtö1 Hevonen 5", "ohjastaja": "Ohjastaja E", "peruspaino": 1.2, "varuste_muutos": "⚠️ Amerikkalaiset kärryt"},
            {"numero": 6, "nimi": "Lähtö1 Hevonen 6", "ohjastaja": "Ohjastaja F", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
        ]
    },
    2: {
        "nimi": "Lopp 2 - Svensk Travsports Unghästserie (Voittajapeli)", "matka": "2140m Voltstart", "tyyppi": "tasoitus",
        "vihje": "<b>Varustemuutokset:</b> Nuorten lähtö. Keulaolettamus: Hevonen 3.",
        "keula_nro": 3,
        "hevoset": [
            {"numero": 1, "nimi": "Lähtö2 Hevonen 1", "ohjastaja": "Ohjastaja A", "peruspaino": 0.7, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Lähtö2 Hevonen 2", "ohjastaja": "Ohjastaja B", "peruspaino": 0.9, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Lähtö2 Hevonen 3", "ohjastaja": "Ohjastaja C", "peruspaino": 1.6, "varuste_muutos": "⚠️ Sekki vaihdettu avoimeksi"},
            {"numero": 4, "nimi": "Lähtö2 Hevonen 4", "ohjastaja": "Ohjastaja D", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Lähtö2 Hevonen 5", "ohjastaja": "Ohjastaja E", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Lähtö2 Hevonen 6", "ohjastaja": "Ohjastaja F", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
        ]
    },
    3: {
        "nimi": "Lopp 3 - Breddlopp (Voittajapeli)", "matka": "1640m Autostart", "tyyppi": "2140a",
        "vihje": "<b>Varustemuutokset:</b> Autolähtö sprintti. Keulaolettamus: Hevonen 1.",
        "keula_nro": 1,
        "hevoset": [
            {"numero": 1, "nimi": "Lähtö3 Hevonen 1", "ohjastaja": "Ohjastaja A", "peruspaino": 1.3, "varuste_muutos": "⚠️ Amerikkalaiset kärryt"},
            {"numero": 2, "nimi": "Lähtö3 Hevonen 2", "ohjastaja": "Ohjastaja B", "peruspaino": 1.3, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Lähtö3 Hevonen 3", "ohjastaja": "Ohjastaja C", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Lähtö3 Hevonen 4", "ohjastaja": "Ohjastaja D", "peruspaino": 0.7, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Lähtö3 Hevonen 5", "ohjastaja": "Ohjastaja E", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Lähtö3 Hevonen 6", "ohjastaja": "Ohjastaja F", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
        ]
    },
    4: {
        "nimi": "Lopp 4 - Amatörlopp (Voittajapeli)", "matka": "2140m Autostart", "tyyppi": "2140a",
        "vihje": "<b>Varustemuutokset:</b> Amatöörilähtö. Keulaolettamus: Hevonen 4.",
        "keula_nro": 4,
        "hevoset": [
            {"numero": 1, "nimi": "Lähtö4 Hevonen 1", "ohjastaja": "Ohjastaja A", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Lähtö4 Hevonen 2", "ohjastaja": "Ohjastaja B", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Lähtö4 Hevonen 3", "ohjastaja": "Ohjastaja C", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Lähtö4 Hevonen 4", "ohjastaja": "Ohjastaja D", "peruspaino": 1.5, "varuste_muutos": "⚠️ Kengät pois"},
            {"numero": 5, "nimi": "Lähtö4 Hevonen 5", "ohjastaja": "Ohjastaja E", "peruspaino": 1.2, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Lähtö4 Hevonen 6", "ohjastaja": "Ohjastaja F", "peruspaino": 0.9, "varuste_muutos": "Normaali"},
        ]
    },
    5: {
        "nimi": "Lopp 5 - STL Klass I (V85-1)", "matka": "2140m Autostart", "tyyppi": "2140a",
        "vihje": "<b>Mats Djuse:</b> 9 Night Hawk suosikki. <b>Varusteet:</b> 2 Hip To Be Square ja 9 Night Hawk kilpailevat amerikanvankkureilla. Keulaolettamus: Hevonen 2.",
        "keula_nro": 2,
        "hevoset": [
            {"numero": 1, "nimi": "T.Wall's Notorius", "ohjastaja": "Jomar Blekkan", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Hip To Be Square", "ohjastaja": "Per Lennartsson", "peruspaino": 1.4, "varuste_muutos": "⚠️ Amerikkalaiset kärryt"},
            {"numero": 3, "nimi": "Sign Of Times", "ohjastaja": "Tomas Pettersson", "peruspaino": 0.9, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Geisha Road Grif", "ohjastaja": "Jorma Kontio", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Macho Cabrio B.B.", "ohjastaja": "Peter G Norman", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Henessi Kiev", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "Takter", "ohjastaja": "Hans G Eriksson", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "Herkules A'lir", "ohjastaja": "Rikard N Skoglund", "peruspaino": 1.2, "varuste_muutos": "Normaali"},
            {"numero": 9, "nimi": "Night Hawk", "ohjastaja": "Mats E Djuse", "peruspaino": 1.25, "varuste_muutos": "⚠️ Amerikkalaiset kärryt + Kengät pois"},
            {"numero": 10, "nimi": "Huchuy Qosqo", "ohjastaja": "Anders Eriksson", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "De Är Hon", "ohjastaja": "Ulf Ohlsson", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 12, "nimi": "Sandsjöns Cantona", "ohjastaja": "Claes Sjöström", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
        ]
    },
    6: {
        "nimi": "Lopp 6 - STL Kallblodsdivisionen (V85-2)", "matka": "2140m Voltstart", "tyyppi": "tasoitus",
        "vihje": "<b>Mats Djuse:</b> 4 Silke Sjarmör & 5 Ellbert. Keulaolettamus: Hevonen 4.",
        "keula_nro": 4,
        "hevoset": [
            {"numero": 1, "nimi": "Fosshaug Frasse", "ohjastaja": "Michaela B Fransson", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Sangviks Lynet", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Andarnas Patron", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.9, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Silke Sjarmör", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.2, "varuste_muutos": "⚠️ Kengät pois"},
            {"numero": 5, "nimi": "Ellbert", "ohjastaja": "Mats E Djuse", "peruspaino": 1.3, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Guli Hektor", "ohjastaja": "Örjan Kihlström", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "Tåga Ryker", "ohjastaja": "Ingvar Nyberg", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "Teknologen", "ohjastaja": "Robert Skoglund", "peruspaino": 1.5, "varuste_muutos": "⚠️ Sekki vaihdettu"},
            {"numero": 9, "nimi": "Ava Modde", "ohjastaja": "Henrik Svensson", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 10, "nimi": "Re Alkapital", "ohjastaja": "Joakim Eskilsson", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "Mira Kiro", "ohjastaja": "Jorma Kontio", "peruspaino": 0.7, "varuste_muutos": "Normaali"},
            {"numero": 12, "nimi": "Ersa Frej", "ohjastaja": "Nathalie Blom", "peruspaino": 0.3, "varuste_muutos": "Normaali"},
            {"numero": 13, "nimi": "Klack Vidar", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 14, "nimi": "Blixen", "ohjastaja": "Jan-Olof Johansson", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 15, "nimi": "Guli Em", "ohjastaja": "Marcus Lilius", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
        ]
    },
    7: {
        "nimi": "Lopp 7 - STL Gulddivisionen EJ's Guldsko (V85-3)", "matka": "1640m Autostart", "tyyppi": "guld",
        "vihje": "<b>Mats Djuse:</b> 4 Mizai keulapotentiaali. Keulaolettamus: Hevonen 4.",
        "keula_nro": 4,
        "hevoset": [
            {"numero": 1, "nimi": "Before Takeoff", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.45, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Santos De Castella", "ohjastaja": "Marcus Lilius", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Romulus Tooma", "ohjastaja": "Peter G Norman", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Mizai", "ohjastaja": "Per Lennartsson", "peruspaino": 1.0, "varuste_muutos": "⚠️ Amerikkalaiset kärryt"},
            {"numero": 5, "nimi": "Lando Mearas", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.25, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Mellby Joker", "ohjastaja": "Mats E Djuse", "peruspaino": 1.15, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "Jerka Sting", "ohjastaja": "Claes Sjöström", "peruspaino": 0.85, "varuste_muutos": "Normaali"},
        ]
    },
    8: {
        "nimi": "Lopp 8 - STL Dubbelklasslopp (V85-4)", "matka": "2640m Autostart", "tyyppi": "dubbelklass",
        "vihje": "<b>Mats Djuse:</b> 8 Uno. Keulaolettamus: Hevonen 6.",
        "keula_nro": 6,
        "hevoset": [
            {"numero": 1, "nimi": "Napoleon Sisu", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Ies Ingusmemory", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.95, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Ytowns Ulrik", "ohjastaja": "Jorma Kontio", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Classique Launcher", "ohjastaja": "Olle Alsén", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Umpteen", "ohjastaja": "Nathalie Blom", "peruspaino": 1.2, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Holiday Island", "ohjastaja": "Anders Eriksson", "peruspaino": 1.35, "varuste_muutos": "⚠️ Kengät pois"},
            {"numero": 7, "nimi": "Sacrebleu", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.85, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "Uno", "ohjastaja": "Mats E Djuse", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 9, "nimi": "Whiskey Majo", "ohjastaja": "Marcus Lilius", "peruspaino": 0.75, "varuste_muutos": "Normaali"},
            {"numero": 10, "nimi": "Timotejs Gamble", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "Bear Victor", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.25, "varuste_muutos": "⚠️ Amerikkalaiset kärryt"},
            {"numero": 12, "nimi": "Lion Sisu", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.15, "varuste_muutos": "Normaali"},
            {"numero": 13, "nimi": "Jaguar Ima", "ohjastaja": "Fredrik Plassen", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 14, "nimi": "Flat Tire Grue", "ohjastaja": "Oskar Florhed", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 15, "nimi": "Vidar Burge", "ohjastaja": "Claes Sjöström", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
        ]
    },
    9: {
        "nimi": "Lopp 9 - Tammer Pokal Kallblods-SM ston (V85-5)", "matka": "2140m Autostart", "tyyppi": "2140a_sm",
        "vihje": "<b>Mats Djuse:</b> 1 Majblomster keulapaikalta vahvoilla. Keulaolettamus: Hevonen 1.",
        "keula_nro": 1,
        "hevoset": [
            {"numero": 1, "nimi": "Majblomster", "ohjastaja": "Mats E Djuse", "peruspaino": 2.1, "varuste_muutos": "⚠️ Amerikkalaiset kärryt + Kengät pois"},
            {"numero": 2, "nimi": "Prinsesse Ness Tjo", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.2, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Tekno Tana", "ohjastaja": "Robert Skoglund", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Hulte Alva", "ohjastaja": "Linda S Hedström", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Guli Stina", "ohjastaja": "Ulf Ohlsson", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Hög Decibel", "ohjastaja": "Stig Jarle Röste", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "Hulte Annika", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.7, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "Jonases Ninja", "ohjastaja": "Jan-Olov Åberg", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 9, "nimi": "Eldida", "ohjastaja": "Ida Eriksson", "peruspaino": 0.3, "varuste_muutos": "Normaali"},
            {"numero": 10, "nimi": "Rötungen", "ohjastaja": "Micael Melander", "peruspaino": 0.3, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "Saga Kiro", "ohjastaja": "Per Lennartsson", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 12, "nimi": "Ethel", "ohjastaja": "Henrik Svensson", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
        ]
    },
    10: {
        "nimi": "Lopp 10 - STL Stodivisionen (V85-6)", "matka": "2640m Voltstart", "tyyppi": "tasaus",
        "vihje": "<b>Mats Djuse:</b> 13 Rupie. Keulaolettamus: Hevonen 4.",
        "keula_nro": 4,
        "hevoset": [
            {"numero": 1, "nimi": "Sessan Of Man", "ohjastaja": "Henrik Svensson", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Adora Liss", "ohjastaja": "Fredrik Plassen", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Pure Jouline", "ohjastaja": "Linus Lönn", "peruspaino": 0.95, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Grove's Maple Poof", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.25, "varuste_muutos": "⚠️ Kengät pois"},
            {"numero": 5, "nimi": "Bohemian Maid", "ohjastaja": "Magnus A Djuse", "peruspaino": 1.3, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Kopparmärra", "ohjastaja": "Nathalie Blom", "peruspaino": 0.9, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "C'est Ma Course", "ohjastaja": "Lucas H Vikström", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "Brionne", "ohjastaja": "Rikard N Skoglund", "peruspaino": 1.25, "varuste_muutos": "Normaali"},
            {"numero": 9, "nimi": "Melina Havelock", "ohjastaja": "Carl Johan Jepson", "peruspaino": 0.85, "varuste_muutos": "Normaali"},
            {"numero": 10, "nimi": "Ajlexes Gourmand", "ohjastaja": "Tomas Pettersson", "peruspaino": 1.05, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "Global Empress", "ohjastaja": "Marcus Lilius", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 12, "nimi": "Danceinthedark F.", "ohjastaja": "Katrin K Frick", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 13, "nimi": "Rupie", "ohjastaja": "Mats E Djuse", "peruspaino": 0.9, "varuste_muutos": "⚠️ Amerikkalaiset kärryt"},
            {"numero": 14, "nimi": "Frida S.H.", "ohjastaja": "Örjan Kihlström", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 15, "nimi": "Kueen Simoni", "ohjastaja": "Claes Sjöström", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
        ]
    },
    11: {
        "nimi": "Lopp 11 - STL Bronsdivisionen (V85-7)", "matka": "2140m Autostart", "tyyppi": "2140a_brons",
        "vihje": "<b>Mats Djuse:</b> 8 Lucky Silver. Keulaolettamus: Hevonen 4.",
        "keula_nro": 4,
        "hevoset": [
            {"numero": 1, "nimi": "Bruce Braylon", "ohjastaja": "Per Lennartsson", "peruspaino": 1.2, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Pineapple", "ohjastaja": "Carl Johan Jepson", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Graces Bird", "ohjastaja": "Fredrik Plassen", "peruspaino": 1.05, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Mellby Mowgli", "ohjastaja": "Örjan Kihlström", "peruspaino": 1.4, "varuste_muutos": "⚠️ Kengät pois + Amerikkalaiset kärryt"},
            {"numero": 5, "nimi": "Ebbot Rice", "ohjastaja": "Linus Lönn", "peruspaino": 0.7, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Jaguar Godiva", "ohjastaja": "Ulf Ohlsson", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "Don E.Star", "ohjastaja": "Oskar J Andersson", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "Lucky Silver", "ohjastaja": "Mats E Djuse", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 9, "nimi": "Elvis T.C.B.", "ohjastaja": "Marcus Lilius", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 10, "nimi": "Gosa Gosing", "ohjastaja": "Rikard N Skoglund", "peruspaino": 0.85, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "Punchboard", "ohjastaja": "Magnus A Djuse", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 12, "nimi": "Slivovitz Lover", "ohjastaja": "Claes Sjöström", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
        ]
    },
    12: {
        "nimi": "Lopp 12 - STL Silverdivisionen (V85-8)", "matka": "2140m Autostart", "tyyppi": "2140a",
        "vihje": "<b>Mats Djuse:</b> 12 X.O.Kemp. Keulaolettamus: Hevonen 8.",
        "keula_nro": 8,
        "hevoset": [
            {"numero": 1, "nimi": "Lähtö12 Hevonen 1", "ohjastaja": "Ohjastaja 1", "peruspaino": 1.0, "varuste_muutos": "Normaali"},
            {"numero": 2, "nimi": "Crowe Motion", "ohjastaja": "Ohjastaja 2", "peruspaino": 1.2, "varuste_muutos": "Normaali"},
            {"numero": 3, "nimi": "Lähtö12 Hevonen 3", "ohjastaja": "Ohjastaja 3", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 4, "nimi": "Lähtö12 Hevonen 4", "ohjastaja": "Ohjastaja 4", "peruspaino": 0.6, "varuste_muutos": "Normaali"},
            {"numero": 5, "nimi": "Lähtö12 Hevonen 5", "ohjastaja": "Ohjastaja 5", "peruspaino": 1.1, "varuste_muutos": "Normaali"},
            {"numero": 6, "nimi": "Killer Rain", "ohjastaja": "Ohjastaja 6", "peruspaino": 0.7, "varuste_muutos": "Normaali"},
            {"numero": 7, "nimi": "Brilliant Kid", "ohjastaja": "Ohjastaja 7", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 8, "nimi": "X.O.Kemp (8)", "ohjastaja": "Mats E Djuse", "peruspaino": 1.35, "varuste_muutos": "⚠️ Amerikkalaiset kärryt + Kengät pois"},
            {"numero": 9, "nimi": "Summermusic'nights", "ohjastaja": "Ohjastaja 9", "peruspaino": 0.8, "varuste_muutos": "Normaali"},
            {"numero": 10, "nimi": "Lähtö12 Hevonen 10", "ohjastaja": "Ohjastaja 10", "peruspaino": 0.5, "varuste_muutos": "Normaali"},
            {"numero": 11, "nimi": "Lähtö12 Hevonen 11", "ohjastaja": "Ohjastaja 11", "peruspaino": 0.4, "varuste_muutos": "Normaali"},
            {"numero": 12, "nimi": "Lähtö12 Hevonen 12", "ohjastaja": "Ohjastaja 12", "peruspaino": 0.9, "varuste_muutos": "Normaali"},
        ]
    }
}

# Liitetään peliprosentit
for lahto_id, hevoset in DATABANK.items():
    l_pelit = LIVE_PELIJAKAUMA.get(lahto_id, {})
    for h in hevoset["hevoset"]:
        h["peli_pct"] = l_pelit.get(h["numero"], 0)

# ==============================================================================
# 3. SIMULAATIOT & VARUSTE-/KEULAMUUTOSTEN HUOMIOINTI
# ==============================================================================

def laske_painotettu_todennakoisyys(lahto_data: dict) -> list:
    hevoset = lahto_data["hevoset"]
    tyyppi = lahto_data["tyyppi"]
    keula_nro = lahto_data.get("keula_nro")
    
    korjatut_painot = []
    for h in hevoset:
        paino = h["peruspaino"]
        nro = h["numero"]
        peli = h["peli_pct"]
        muutos = h["varuste_muutos"]
        
        # Varustemuutosten vaikutus simulaatioon
        if "Kengät pois" in muutos:
            paino *= 1.15
        if "Amerikkalaiset kärryt" in muutos:
            paino *= 1.12
        if "Sekki" in muutos:
            paino *= 1.05
            
        # Keulahevosen 5% lisäpaino / etu
        if nro == keula_nro:
            paino *= 1.05
        
        if tyyppi in ["2140a", "2140a_sm", "2140a_brons"]:
            if nro in [4, 5]:
                paino *= 1.20
            elif nro == 2:
                paino *= 0.85
            elif nro >= 7:
                paino *= 0.80
                
        if tyyppi == "2140a_sm":
            if peli > 50:
                paino *= 1.45
        elif tyyppi == "guld":
            if peli > 30:
                paino *= 1.30
            elif peli < 5:
                paino *= 0.3
        elif tyyppi == "dubbelklass":
            if peli < 10:
                paino *= 1.35
            elif peli > 30:
                paino *= 0.85
                
        korjatut_painot.append((nro, max(paino, 0.05)))
        
    return korjatut_painot

def simuloi_lahto_tilastoilla(lahto_data: dict, kierrokset: int = 10000) -> dict:
    painot_tiedot = laske_painotettu_todennakoisyys(lahto_data)
    numerot = [p[0] for p in painot_tiedot]
    painot = [p[1] for p in painot_tiedot]
    
    voitot = {num: 0 for num in numerot}
    for _ in range(kierrokset):
        voittaja = random.choices(numerot, weights=painot, k=1)[0]
        voitot[voittaja] += 1
        
    return {num: round((maara / kierrokset) * 100, 1) for num, maara in voitot.items()}

SIM_TULOKSET = {}
KAIKKI_PELIARVOT = []

for lahto_id, lahto_data in DATABANK.items():
    sim_res = simuloi_lahto_tilastoilla(lahto_data)
    SIM_TULOKSET[lahto_id] = sim_res
    
    for h in lahto_data["hevoset"]:
        mc = sim_res[h["numero"]]
        peli = h["peli_pct"]
        ero = round(mc - peli, 1)
        
        KAIKKI_PELIARVOT.append({
            "lahto": lahto_id,
            "v85_leg": (lahto_id - 4) if lahto_id >= 5 else None,
            "nro": h["numero"],
            "nimi": h["nimi"],
            "ohjastaja": h["ohjastaja"],
            "varuste": h["varuste_muutos"],
            "sim": mc,
            "peli": peli,
            "ero": ero
        })

TOP_TARPIT_V85 = sorted([p for p in KAIKKI_PELIARVOT if p["lahto"] >= 5], key=lambda x: x["ero"], reverse=True)[:5]
TOP_TARPIT_VOITTAJA = sorted([p for p in KAIKKI_PELIARVOT if p["lahto"] <= 4], key=lambda x: x["ero"], reverse=True)[:4]

# ==============================================================================
# 4. STREAMLIT-KÄYTTÖLIITTYMÄ
# ==============================================================================

st.set_page_config(page_title="Hagmyren Live - Varustemuutokset & Keulaetu", layout="wide")

st.title("🏇 Hagmyren Ravioohjelma - Varuste- ja Keula-analyysaattori")
st.caption("Päivitetty simulaatio: Huomioi varustemuutokset (kengät pois, amerikkalaiset kärryt) sekä keulahevosen 5% lisäpaino.")

m1, m2, m3 = st.columns(3)
m1.metric("Vaihto", LIVE_VAIHTOTIEDOT["vaihto"])
m2.metric("Jakosumma", LIVE_VAIHTOTIEDOT["jakosumma"])
m3.metric("Jackpot Extra", LIVE_VAIHTOTIEDOT["jackpot"])

tab_v85, tab_voittaja, tab_lahdot, tab_kokonais, tab_v4, tab_dd = st.tabs([
    "🏆 V85 Yhteenveto & 200€ Systeemi",
    "🎯 Voittaja-peli (Lähdöt 1–4)",
    "📌 Lähdöt 1–12 Analyysi",
    "📊 Koko Ravipäivä",
    "🔥 V4-Peli",
    "🎯 Päivän Duo"
])

# ------------------------------------------------------------------------------
# TAB V85: SYSTEEMI (Lähdöt 5-12)
# ------------------------------------------------------------------------------
with tab_v85:
    st.subheader("🎯 V85 Parhaat Peliarvot (Huomioiden Varusteet & Keulat)")
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    
    for idx in range(4):
        tarp = TOP_TARPIT_V85[idx]
        with cols[idx]:
            st.success(
                f"**V85-{tarp['v85_leg']} (Lopp {tarp['lahto']})**\n\n"
                f"### **#{tarp['nro']} {tarp['nimi']}**\n\n"
                f"• Simulaatio: **{tarp['sim']}%**\n\n"
                f"• Live-pelattu: **{tarp['peli']}%**\n\n"
                f"• Peliarvo: **+{tarp['ero']}%**"
            )

    st.divider()
    st.subheader("💰 200 € V85-Tavoitesysteemi (Lähdöt 5–12)")
    
    SYSTEEMI_200E = [
        {"leg": "V85-1 (L5)", "varmat_ja_merkit": "**9 Night Hawk** (Amerik. kärryt + kengät pois), 2 Hip To Be Square", "syu": "2 merkkiä"},
        {"leg": "V85-2 (L6)", "varmat_ja_merkit": "**8 Teknologen**, 5 Ellbert, 4 Silke Sjarmör, 2 Sangviks Lynet", "syu": "4 merkkiä"},
        {"leg": "V85-3 (L7)", "varmat_ja_merkit": "🔒 **1 Before Takeoff** (Varma)", "syu": "1 merkki (Spiki)"},
        {"leg": "V85-4 (L8)", "varmat_ja_merkit": "**6 Holiday Island**, **11 Bear Victor**, **8 Uno**, 12 Lion Sisu, 3 Ytowns Ulrik", "syu": "5 merkkiä"},
        {"leg": "V85-5 (L9)", "varmat_ja_merkit": "🔒 **1 Majblomster** (Keulapaikka + varusteet, varma)", "syu": "1 merkki (Spiki)"},
        {"leg": "V85-6 (L10)", "varmat_ja_merkit": "**5 Bohemian Maid**, **8 Brionne**, 4 Grove's Maple Poof, 10 Ajlexes Gourmand", "syu": "4 merkkiä"},
        {"leg": "V85-7 (L11)", "varmat_ja_merkit": "**4 Mellby Mowgli** (Kengät pois + amerik. kärryt), 1 Bruce Braylon", "syu": "2 merkkiä"},
        {"leg": "V85-8 (L12)", "varmat_ja_merkit": "**8 X.O.Kemp**, 2 Crowe Motion", "syu": "2 merkkiä"}
    ]
    st.table(pd.DataFrame(SYSTEEMI_200E))

# ------------------------------------------------------------------------------
# TAB VOITTAJA: LÄHDÖT 1-4
# ------------------------------------------------------------------------------
with tab_voittaja:
    st.subheader("🎯 Parhaat Voittaja-Pelikohteet (Lähdöt 1–4)")
    st.write("Simuloidut arvot huomioivat nyt varustemuutokset ja keulaedun.")
    
    c1, c2 = st.columns(2)
    for idx, tarp in enumerate(TOP_TARPIT_VOITTAJA):
        target_col = c1 if idx % 2 == 0 else c2
        with target_col:
            st.info(
                f"### **Lähtö {tarp['lahto']} - #{tarp['nro']} {tarp['nimi']}**\n\n"
                f"• Simulaation Voitto-%: **{tarp['sim']}%**\n\n"
                f"• Peliprosentti: **{tarp['peli']}%**\n\n"
                f"• **Peliarvo-Ero: +{tarp['ero']}%**"
            )

# ------------------------------------------------------------------------------
# TAB LÄHDÖT 1-12
# ------------------------------------------------------------------------------
with tab_lahdot:
    valittu_lahto_nro = st.radio(
        "**Valitse Lähtö:**",
        options=list(DATABANK.keys()),
        format_func=lambda x: f"Lähtö {x}" + (f" (V85-{(x-4)})" if x >= 5 else " (Voittajapeli)"),
        horizontal=True
    )
    
    lahto = DATABANK[valittu_lahto_nro]
    sim = SIM_TULOKSET[valittu_lahto_nro]
    keula_nro = lahto.get("keula_nro")
    
    st.subheader(f"📌 {lahto['nimi']} ({lahto['matka']})")
    st.info(lahto["vihje"], icon="📊")
    st.warning(f"💨 **Oletettu Keulahevonen tässä lähdössä:** #{keula_nro} (saa +5% painoarvon simulaatioon)", icon="⚡")
    
    hevoset_laskettu = []
    for h in lahto["hevoset"]:
        mc = sim.get(h["numero"], 0.0)
        peli = h["peli_pct"]
        ero = round(mc - peli, 1)
        hevoset_laskettu.append({
            **h, 
            "mc": mc, 
            "ero": ero,
            "varuste": h.get("varuste_muutos", "Normaali")
        })
    
    parhaat_pelihevoset = sorted(hevoset_laskettu, key=lambda x: x["ero"], reverse=True)[:3]
    
    st.markdown("### 🔥 **Parhaat Peliarvot (Simulaatio vs. Peliprosentti)**")
    p1, p2, p3 = st.columns(3)
    for idx, col in enumerate([p1, p2, p3]):
        if idx < len(parhaat_pelihevoset):
            h = parhaat_pelihevoset[idx]
            with col:
                st.success(f"**#{h['numero']} {h['nimi']}**\n\n"
                           f"• Varusteet: {h['varuste']}\n\n"
                           f"• Simulaatio: **{h['mc']}%**\n\n"
                           f"• Live Pelattu: **{h['peli_pct']}%**\n\n"
                           f"• Etumatka: **+{h['ero']}%**")

    st.divider()
    st.markdown("### 🏇 **Lähtöruudukko & Varustemuutokset**")
    
    cols = st.columns(3)
    for idx, h in enumerate(hevoset_laskettu):
        with cols[idx % 3]:
            with st.container(border=True):
                is_keula = " (KEULA)" if h['numero'] == keula_nro else ""
                st.markdown(f"#### **{h['numero']}. {h['nimi']}**{is_keula}")
                st.caption(f"🏎️ {h['ohjastaja']}")
                st.text(f"Varusteet: {h['varuste']}")
                c1, c2 = st.columns(2)
                c1.metric("Simulaatio %", f"{h['mc']}%")
                c2.metric("Pelattu %", f"{h['peli_pct']}%", delta=f"{h['ero']:+.1f}%")
                st.progress(int(min(h['mc'], 100)))

# ------------------------------------------------------------------------------
# TAB KOKO RAVIPÄIVÄ (1-12)
# ------------------------------------------------------------------------------
with tab_kokonais:
    st.subheader("📊 Kaikkien Lähdöistä (1–12) Päivitetyt Simulaatiotulokset")
    
    kaikki_data = []
    for l_id in range(1, 13):
        l_info = DATABANK[l_id]
        l_sim = SIM_TULOKSET[l_id]
        for h in l_info["hevoset"]:
            mc = l_sim[h["numero"]]
            peli = h["peli_pct"]
            kaikki_data.append({
                "Lähtö": f"Lopp {l_id}" + (f" (V85-{l_id-4})" if l_id >= 5 else ""),
                "Nro": h["numero"],
                "Hevonen": h["nimi"],
                "Varustemuutos": h["varuste_muutos"],
                "Simulaatio %": mc,
                "Live Peli %": peli,
                "Peliarvo (Ero %)": round(mc - peli, 1)
            })
            
    df_kaikki = pd.DataFrame(kaikki_data)
    st.dataframe(df_kaikki, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# TAB V4 & DD
# ------------------------------------------------------------------------------
with tab_v4:
    st.subheader("🔥 V4-Peli (Lähdöt 9–12)")
    for v4_leg, l_id in enumerate(range(9, 13), start=1):
        st.markdown(f"#### **V4-{v4_leg} / Lopp {l_id}**")
        l_info = DATABANK[l_id]
        l_sim = SIM_TULOKSET[l_id]
        
        l_hevoset = []
        for h in l_info["hevoset"]:
            mc = l_sim[h["numero"]]
            peli = h["peli_pct"]
            l_hevoset.append({
                "Nro": h["numero"], "Hevonen": h["nimi"], "Varuste": h["varuste_muutos"],
                "Sim %": mc, "Live Peli %": peli, "Ero %": round(mc - peli, 1)
            })
        df_leg = pd.DataFrame(l_hevoset).sort_values(by="Ero %", ascending=False)
        st.dataframe(df_leg, use_container_width=True, hide_index=True)

with tab_dd:
    st.subheader("🎯 Päivän Duo (Lähdöt 11 & 12)")
    dd1_sim = SIM_TULOKSET[11]
    dd2_sim = SIM_TULOKSET[12]
    
    dd_yhdistelmat = []
    for h1 in DATABANK[11]["hevoset"]:
        for h2 in DATABANK[12]["hevoset"]:
            yhdistelma_mc = (dd1_sim[h1["numero"]] / 100) * (dd2_sim[h2["numero"]] / 100) * 100
            yhdistelma_peli = (h1["peli_pct"] / 100) * (h2["peli_pct"] / 100) * 100
            dd_yhdistelmat.append({
                "Yhdistelmä": f"DD-1: #{h1['numero']} {h1['nimi']}  x  DD-2: #{h2['numero']} {h2['nimi']}",
                "Sim Todennäköisyys %": round(yhdistelma_mc, 2),
                "Live Todennäköisyys %": round(yhdistelma_peli, 2),
                "Peliarvo Ero %": round(yhdistelma_mc - yhdistelma_peli, 2)
            })
            
    st.dataframe(pd.DataFrame(dd_yhdistelmat).sort_values(by="Peliarvo Ero %", ascending=False).head(10), use_container_width=True, hide_index=True)
