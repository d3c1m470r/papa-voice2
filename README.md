# Papa's Voice Reader

Ez egy kiegészítő (add-on) az NVDA képernyőolvasó szoftverhez, amelynek célja, hogy segítse a látássérült felhasználókat a weboldalak és Facebook tartalmának intelligens felolvasásával.

## Főbb funkciók

- **Intelligens tartalomfelismerés**: Automatikusan felismeri, hogy a weboldal Facebook-e vagy híroldal, és ennek megfelelően optimalizált módszerrel olvassa fel a tartalmat
- **Facebook támogatás**: Kifejezetten Facebook bejegyzések felolvasására optimalizálva, kihagyja a hirdetéseket és csak a releváns tartalmat olvassa fel
- **Híroldalak támogatása**: Általános híroldalak és blogok fő tartalmának intelligens kinyerése
- **Magyar nyelv támogatás**: Teljes magyar nyelvi támogatás, beleértve a magyar hirdetések felismerését is
- **Egyszerű kezelés**: Csak egy billentyűkombináció (`Insert+J`) a tartalom felolvasásához

## Telepítés

A telepítéshez valószínűleg egy látó személy (családtag, barát) segítségére lesz szükség, mivel a fájlokat a megfelelő mappába kell másolni.

1.  A "Code" gombra kattintva válassza a "Download ZIP" opciót a projekt letöltéséhez.
2.  Csomagolja ki a letöltött `.zip` fájlt egy tetszőleges mappába.
3.  Indítsa el az NVDA-t a gépen.
4.  Nyomja le az **`Insert+N`** billentyűket az NVDA menü megnyitásához.
5.  A nyíl billentyűkkel navigáljon az `Eszközök` menüponthoz, majd azon belül a `Kiegészítők kezelése` opcióra.
6.  A megnyíló ablakban használja a `Tab` billentyűt, amíg el nem éri a `Kiegészítő-mappa megnyitása` gombot, majd nyomjon `Enter`-t.
7.  A felugró mappába másolja be a 2. pontban kicsomagolt **`papa-voice-reader`** mappát.
8.  Indítsa újra az NVDA-t.

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
- **Függőségek**: requests, readability-lxml, html2text, beautifulsoup4
- **Architektúra**: NVDA Global Plugin
- **Facebook támogatás**: DOM-alapú bejegyzés-felismerés, hirdetésszűrés
- **Tartalomkinyerés**: Readability algoritmus híroldalakhoz, egyedi parser Facebookhoz

### Fájlstruktúra

```
papa-voice-reader/          # NVDA kiegészítő mappa
├── addon/
│   ├── __init__.py         # Fő plugin kód
│   └── lib/                # Csomagolt függőségek
├── manifest.ini            # NVDA kiegészítő metaadatok
src/                        # Fejlesztési fájlok
├── extract_content.py      # Általános tartalomkinyerő
└── facebook_parser.py      # Facebook-specifikus parser
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

## Jövőbeli fejlesztések

- Több közösségi média platform támogatása (Instagram, Twitter/X)
- Jobb hibakezelés és felhasználói visszajelzések
- Tartalom mentése későbbi olvasáshoz
- Testreszabható tartalomszűrés

## Támogatás és közreműködés

Ez a projekt nyílt forráskódú és a közösség közreműködését várja. Ha hibát talál vagy javaslatot szeretne tenni, használja a GitHub Issues funkciót.
