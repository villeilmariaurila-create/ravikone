const ravilahtot = [
  // ==========================================
  // LÄHTÖ 1
  // ==========================================
  {
    lahto: 1,
    nimi: "Lähtö 1 / Osagruppi 1",
    aika: "15:58",
    matka: "2140 m",
    lahtotapa: "Ryhmäajo (Autostart)",
    palkinto: "100 000 kr",
    hevoset: [
      {
        numero: 1,
        nimi: "Esimerkki Hevonen 1",
        ohjastaja: "Esimerkki Kusk",
        valmentaja: "Esimerkki Valmentaja",
        haastattelu: "Tuntui hyvältä viimeksi ja lähtöpaikka on ihanteellinen.",
        vihjekommentti: "Avaa nopeasti, mahdoton ohitettava keulasta.",
        tilastot: {
          startit: "20 (5-3-2)",
          voittoprosentti: "25%",
          keula: "5 (4-1-0)"
        }
      }
    ]
  },

  // ==========================================
  // LÄHTÖ 2
  // ==========================================
  {
    lahto: 2,
    nimi: "Lähtö 2 / Osagruppi 2",
    aika: "16:20",
    matka: "2140 m",
    lahtotapa: "Tasoitusajo (Voltstart)",
    palkinto: "110 000 kr",
    hevoset: [
      {
        numero: 1,
        nimi: "Esimerkki Hevonen 2",
        ohjastaja: "Esimerkki Kusk",
        valmentaja: "Esimerkki Valmentaja",
        haastattelu: "Hyvässä kunnossa, juoksun onnistuessa voi mennä pitkälle.",
        vihjekommentti: "Tasaista suorittamista, vaatii hieman tuuria matkalla.",
        tilastot: {
          startit: "15 (3-2-1)",
          voittoprosentti: "20%",
          keula: "2 (1-1-0)"
        }
      }
    ]
  },

  // ==========================================
  // LÄHTÖ 3
  // ==========================================
  {
    lahto: 3,
    nimi: "Lähtö 3 / Osagruppi 3",
    aika: "16:44",
    matka: "1640 m",
    lahtotapa: "Ryhmäajo (Autostart)",
    palkinto: "150 000 kr",
    hevoset: [
      {
        numero: 1,
        nimi: "Before Takeoff",
        ohjastaja: "Örjan Kihlström",
        valmentaja: "Daniel Wäjersten",
        haastattelu: "Sai viimeksi hienon juoksun Margaretas Pokalissa ja viimeisessä kurvissa näytti siltä, että se voisi yltää kolmen parhaan joukkoon. Viimeisellä matkalla ei kuitenkaan ollut aivan parasta potkua potkussa. Kaikki tuntuu sen jälkeen hyvältä, ja tästä lähtökohdasta on vain yritettävä avata niin nopeasti kuin mahdollista. Jatkamme luultavasti kokolapuilla (helstängt) eikä muitakaan muutoksia ole tulossa, sanoo Oskar Florhed Daniel Wäjerstenin tallista.",
        vihjekommentti: "Kolme voittoa kuudesta startista lyhyellä matkalla Ruotsissa. Neljä toista sijaa seitsemästä startista syksyn aikana. Toinen Örjan Kihlströmin kanssa, ensimmäisessä sijoittumaton. Keulapaikka on epävarma, mutta aikainen merkki silti.",
        tilastot: {
          startit: "32 (7-8-4)",
          voittoprosentti: "22%",
          keula: "7 (4-3-0)",
          balanssi: "Kengät / Kokolaput"
        }
      },
      {
        numero: 2,
        nimi: "Romulus Tooma",
        ohjastaja: "Peter G Norman",
        valmentaja: "Peter G Norman",
        haastattelu: "Hän toimi hyvin viimeksi ja lopetti valtavan nopeasti. Olin lisäksi erittäin tyytyväinen siihen, miltä hevonen tuntui. Täällä on sama taktiikka: hiivitään mukana ja jatketaan kunnon rakentamista. Ajetaan sitten lopussa ja katsotaan mihin se riittää. Jatketaan edelleen kengät jalassa, jenkkikärryillä ja puolilapuilla (halvstängt), sanoo Peter G Norman.",
        vihjekommentti: "Lähdön alhaisin voittoprosentti. Neljä toista sijaa parhaana tuloksena 21 startista Peter G Normanilla. Sijoittunut kolmen joukkoon neljässä kuudesta startista lyhyellä matkalla, yksi voitto. Positiivinen viimeksi, yllätyshaastaja sijasta.",
        tilastot: {
          startit: "38 (5-7-6)",
          voittoprosentti: "13%",
          keula: "1 (1-0-0)",
          balanssi: "Kengät / Puolilaput / Bike"
        }
      },
      {
        numero: 3,
        nimi: "Mizai",
        ohjastaja: "Mats E Djuse",
        valmentaja: "Jan Ove Olsen",
        haastattelu: "Hän tuli maaliin voimat tallella viimeksi ja alkaa päästä huikeaan kuntoon. Mats oli myös erittäin tyytyväinen hevosen tuntiin. Olemme ajaneet hänellä melko nätisti jonkin aikaa, mutta nyt on aika olla hyökkäävämpi. Hän osaa avata erittäin nopeasti, mutta mukana on useita muitakin nopeita avaajia. Vastus on kovaa, mutta hän on voittanut kovia hevosia aiemminkin. Rata 4 Hagmyrenilla on varmaan paras paikka sillä radalla. Täällä ei vain riisuta kenkiä ja uskota voittoon, mutta hän on yksi useista, jotka voisivat sen tehdä. Varusteet tapissaan taas: kengittä joka puolelta, jenkkikärryt ja kokolaput, sanoo Jan Ove Olsen.",
        vihjekommentti: "15 voittoa 21 startista keulasta Ruotsissa (19 yritystä). Kuusi voittoa 35 lähdössä V75/V85-tasolla. Voitti kultadivisioonan vuosi sitten, kunto nousussa, ehkä keulaan tässä? Mahdollinen.",
        tilastot: {
          startit: "77 (21-9-9)",
          voittoprosentti: "27%",
          keula: "19 (15-4-0)",
          balanssi: "Avokenkä / Kokolaput / Bike"
        }
      },
      {
        numero: 4,
        nimi: "Lando Mearas",
        ohjastaja: "Magnus A Djuse",
        valmentaja: "Daniel Wäjersten",
        haastattelu: "Hän tuli maaliin kaikkia voimia säästyen viimeksi, mikä voi olla hyvä asia tällä kertaa. Hän on uskomattoman starttinopea tällaisilta paikoilta ja Magnus saanee hänet täyteen vauhtiin ensimmäisellä matkalla. Jos pääsevät keulaan, heitä on vaikea voittaa, ja tähän minulla on paras tuntu kolmesta hevosestamme lähtöpaikat huomioiden. Vedettävät laput (norsken) jäivät vetämättä viimeksi ja jatkamme niillä sekä samalla balanssilla ja varusteilla, sanoo Oskar Florhed Daniel Wäjerstenin tallista.",
        vihjekommentti: "11 voittoa 14:stä Ruotsin voitosta keulasta (12 yritystä). 13 voittoa 14:stä keskimatkalla, ei yhtään voittoa kolmesta startista lyhyellä matkalla. Kolme voittoa yhdeksästä syysstartista, talli iskussa. Mielenkiintoinen idea!",
        tilastot: {
          startit: "36 (14-1-5)",
          voittoprosentti: "39%",
          keula: "12 (11-0-1)",
          balanssi: "Norjalaiset laput / Bike"
        }
      },
      {
        numero: 5,
        nimi: "Mellby Joker",
        ohjastaja: "Daniel Wäjersten",
        valmentaja: "Daniel Wäjersten",
        haastattelu: "Hän teki rajun latauksen viimeksi Suomessa ja oli uskomattoman hyvä toisena Don Fanucci Cetin jälkeen. Hevonen on kaikkein paras keulasta tai voittajaselästä (2. ulkoa/sisältä), mutta täältä on vaikea päästä kumpaankaan paikkaan. Toivotaan nättiä juoksua ja katsotaan mihin se riittää. Muutoksia ei ole suunniteltu, sanoo Oskar Florhed Daniel Wäjerstenin tallista.",
        vihjekommentti: "Kolme voittoa yhdeksästä startista Mats E Djusen kanssa, neljä voittoa 21 startista lyhyellä matkalla. Vaikea päästä keulaan tai voittajaselkään täältä, peruutetaan luultavasti ja toivotaan kovaa matkavauhtia. Ei täysin ulkona.",
        tilastot: {
          startit: "65 (14-10-13)",
          voittoprosentti: "22%",
          keula: "18 (9-4-4)",
          balanssi: "Kokolaput"
        }
      },
      {
        numero: 6,
        nimi: "Jerka Sting",
        ohjastaja: "Claes Sjöström",
        valmentaja: "Claes Sjöström",
        haastattelu: "",
        vihjekommentti: "Yksi voitto neljästä startista sprinterimatkalla. Yksi aiempi startti Hagmyrenissa, jonka voitti. Kuusi voittoa 19 syysstartista, yhdeksän voittoa 12 yrityksestä keulasta. Nyt varmasti taka-alalta, yllättäjä.",
        tilastot: {
          startit: "69 (19-11-10)",
          voittoprosentti: "28%",
          keula: "12 (9-2-1)",
          balanssi: "Kokolaput / Norskit / Bike"
        }
      }
    ]
  }
];
