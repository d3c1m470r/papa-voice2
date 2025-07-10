# Papa's Voice Reader


Ez egy kiegészítő (add-on) az NVDA képernyőolvasó szoftverhez, melynek célja, hogy segítse a látássérült felhasználókat a weboldalak és közösségi média felületek (elsősorban híroldalak és a Facebook) fő tartalmának intelligens felolvasásával.

## Előfeltételek

Rendelkeznie kell a **[NVDA (NonVisual Desktop Access)](https://www.nvaccess.org/download/)** képernyőolvasóval a Windows gépén. Az NVDA egy ingyenes, nyílt forráskódú képernyőolvasó.

## Telepítés (Fejlesztői Változat)

Mivel a projekt aktív fejlesztés alatt áll, még nem áll rendelkezésre stabil, telepíthető csomag (`.nvda-addon`). A telepítés menete a következő:

1.  Klónozza vagy töltse le ezt a repository-t a Windows gépére.
2.  Nyissa meg az NVDA-t, majd az `NVDA+N` billentyűkombinációval a menüt.
3.  Navigáljon az `Eszközök` -> `Kiegészítők kezelése` menüponthoz.
4.  A Kiegészítő-kezelőben kattintson a `Kiegészítő-mappa megnyitása` gombra.
5.  Másolja be a **`papa-voice-reader`** mappát ebből a repository-ból a most megnyitott kiegészítő-mappába.
6.  Indítsa újra az NVDA-t az `NVDA+Q` billentyűvel (kilépés), majd indítsa el újra.

## Használat

-   Nyissa meg a böngészőjét és navigáljon egy tetszőleges híroldalra, blogra vagy más weboldalra.
-   Fókuszáljon a böngésző címsorára (pl. `Alt+D` billentyűvel), vagy a `Tab` billentyűvel navigáljon egy linkre az oldalon.
-   Nyomja meg a **`NVDA+SHIFT+U`** billentyűkombinációt.
-   A kiegészítő letölti a cikk tartalmát, eltávolítja a felesleges elemeket (reklámok, menük), és a tiszta szöveget egy felugró ablakban jeleníti meg, amit az NVDA felolvas.

## Tervek

-   [ ] **Facebook Optimalizáció**: A Facebook hírfolyam struktúrájának megértése és felolvasása.
-   [ ] **Telepítőcsomag Készítése**: A kiegészítő becsomagolása egy könnyen telepíthető `.nvda-addon` fájlba. 