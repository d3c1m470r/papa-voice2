# Papa's Voice Reader

Ez egy kiegészítő (add-on) az NVDA képernyőolvasó szoftverhez, amelynek célja, hogy segítse a látássérült felhasználókat a weboldalak és Facebook tartalmának intelligens felolvasásával.

## Főbb funkciók

- **Intelligens tartalomfelismerés**: Automatikusan felismeri, hogy a weboldal Facebook-e vagy híroldal, és ennek megfelelően optimalizált módszerrel olvassa fel a tartalmat
- **Facebook támogatás**: Kifejezetten Facebook bejegyzések felolvasására optimalizálva, kihagyja a hirdetéseket és csak a releváns tartalmat olvassa fel
- **Híroldalak támogatása**: Általános híroldalak és blogok fő tartalmának intelligens kinyerése
- **Magyar nyelv támogatás**: Teljes magyar nyelvi támogatás, beleértve a magyar hirdetések felismerését is
- **Egyszerű kezelés**: Csak egy billentyűkombináció (`Insert+J`) a tartalom felolvasásához

## Telepítés

**Telepíthető verzió (AJÁNLOTT):**

1.  Töltse le a **`papa-voice-reader.nvda-addon`** fájlt a projekt [GitHub oldaláról](https://github.com/d3c1m470r/papa-voice).
2.  Kattintson duplán a letöltött `.nvda-addon` fájlra.
3.  Az NVDA automatikusan megkérdezi, hogy telepíteni szeretné-e a kiegészítőt. Válassza az "Igen" opciót.
4.  Indítsa újra az NVDA-t amikor arra kéri.

## Használat

### Alapvető használat

1.  Nyisson meg egy weboldalt a böngészőjében (Firefox, Chrome, Edge).
2.  Navigáljon a címsorba, vagy kattintson egy linkre.
3.  Nyomja le az **`Insert+J`** billentyűket.
4.  A kiegészítő automatikusan felismeri a weboldal típusát és elkezdi felolvasni a főbb tartalmat.

### Támogatott weboldalak

- **Facebook**: Bejegyzések, státuszok, hírek (hirdetések kihagyásával)
- **Híroldalak**: 444.hu, index.hu, hvg.hu, és egyéb magyar és nemzetközi híroldalak
- **Blogok**: Általános blog bejegyzések
- **Cikkek**: Online újságcikkek és magazinok

### Billentyűkombináció megváltoztatása

A billentyűkombináció (`Insert+J`) megváltoztatható az NVDA beállításaiban:

1.  Nyomja le az `Insert+N` billentyűket.
2.  Válassza a `Beállítások` > `Beviteli parancsok...` menüpontot.
3.  Keresse meg a "Papa's Voice Reader" kategóriát.
4.  Jelölje ki a "readArticle" funkciót.
5.  Klikkeljen a "Hozzáadás" gombra és állítson be egy új billentyűkombinációt.

## Fejlesztési információk

### Technikai részletek

- **Alapnyelv**: Python 3
- **Függőségek**: requests, html2text, beautifulsoup4 (tisztán Python könyvtárak)
- **Architektúra**: NVDA Global Plugin
- **Facebook támogatás**: DOM-alapú bejegyzés-felismerés, hirdetésszűrés
- **Tartalomkinyerés**: Egyszerű heurisztika híroldalakhoz, egyedi parser Facebookhoz

### Fájlstruktúra

```
papa-voice-reader.nvda-addon          # Telepíthető kiegészítő csomag (Windows + Linux)
papa-voice-reader/                    # NVDA kiegészítő forrásmappa
├── addon/
│   ├── __init__.py                   # Fő plugin kód
│   └── lib/                          # Csomagolt függőségek
├── manifest.ini                      # NVDA kiegészítő metaadatok
src/                                  # Fejlesztési fájlok
├── extract_content.py                # Általános tartalomkinyerő
├── facebook_parser.py                # Facebook-specifikus parser
└── test_intelligent_parser.py       # Tesztfájl a funkcionalitás bemutatására
```

## Hibaelhárítás

### "No URL found" üzenet

- Ellenőrizze, hogy a böngésző címsorában van-e URL
- Próbáljon meg egy linkre kattintani, majd használni a funkciót
- Egyes webhelyek esetén frissítse az oldalt

### "Error reading content" üzenet

- Ellenőrizze az internetkapcsolatot
- Egyes weboldalak blokkolhatják az automatikus hozzáférést
- Próbáljon meg egy másik weboldalt

### Nincs felolvasás

- Ellenőrizze, hogy az NVDA be van-e kapcsolva
- Próbálja meg másik weboldallal
- Indítsa újra az NVDA-t

### Telepítési problémák

- **"Damaged or unsupported" hiba**: Győződjön meg róla, hogy a `papa-voice-reader.nvda-addon` fájlt tölti le (ne más fájlt vagy mappát)
- Győződjön meg róla, hogy az NVDA fut a telepítés során
- Próbálja meg adminisztrátori jogokkal futtatni az NVDA-t
- Ellenőrizze, hogy a letöltött fájl neve `.nvda-addon` végződéssel rendelkezik

## Jövőbeli fejlesztések

- Több közösségi média platform támogatása (Instagram, Twitter/X)
- Jobb hibakezelés és felhasználói visszajelzések
- Tartalom mentése későbbi olvasáshoz
- Testreszabható tartalomszűrés

## Támogatás és közreműködés

Ez a projekt nyílt forráskódú és a közösség közreműködését várja. Ha hibát talál vagy javaslatot szeretne tenni, használja a GitHub Issues funkciót.

**Fejlesztő kontakt**: Ez egy közösségi projekt, a GitHub-on keresztül lehet kapcsolatba lépni.

## Licenc

Ez a projekt az MIT licenc alatt áll, ami azt jelenti, hogy szabadon használható, módosítható és terjeszthető.
