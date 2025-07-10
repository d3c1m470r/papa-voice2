# Papa's Voice Reader

Ez egy kiegészítő (add-on) az NVDA képernyőolvasó szoftverhez, amelynek célja, hogy segítse a látássérült felhasználókat a weboldalak fő tartalmának intelligens felolvasásával.

## Telepítés

A telepítéshez valószínűleg egy látó személy (családtag, barát) segítségére lesz szükség, mivel a fájlokat a megfelelő mappába kell másolni.

1.  A "Code" gombra kattintva válassza a "Download ZIP" opciót a projekt letöltéséhez.
2.  Csomagolja ki a letöltött `.zip` fájlt egy tetszőleges mappába.
3.  Indítsa el az NVDA-t a gépen.
4.  Nyomja le az **`Insert+N`** billentyűket az NVDA menü megnyitásához.
5.  A nyíl billentyűkkel navigáljon az `Eszközök` menüponthoz, majd azon belül a `Kiegészítők kezelése` opcióra.
6.  A megnyíló ablakban használja a `Tab` billentyűt, amíg el nem éri a `Kiegészítő-mappa megnyitása` gombot, majd nyomjon `Enter`-t.
7.  A felugró mappába másolja be a 2. pontban kicsomagolt **`papa-voice-reader`** mappát.
8.  Indítsa újra az NVDA-t (lépjen ki az `Insert+Q` billentyűkkel, majd indítsa el újra).

## Hogyan Használja?

A kiegészítő egy egyszerű billentyűparanccsal működik.

### **A használat menete:**

Amikor egy olyan weboldalon van, amelynek a fő tartalmát szeretné felolvastatni (pl. egy hírportálon vagy egy blogon), tegye a következőket:

1.  Használja a **`Tab`** billentyűt a linkek közötti ugráláshoz, amíg meg nem találja az elolvasni kívánt cikket.
2.  Amikor a fókusz a megfelelő linken van, nyomja le a **`Insert+J`** billentyűkombinációt.

Ez a parancs arra utasítja a kiegészítőt, hogy nyissa meg a linket a háttérben, keresse meg a cikk lényegi tartalmát, és azt olvassa fel Önnek egy külön ablakban, mindenféle zavaró elem (reklámok, menük) nélkül.

### **Miért az `Insert+J`?**

Ezt az egyszerű, kétgombos parancsot azért választottuk, mert könnyen lenyomható, és nem ütközik az NVDA vagy a Windows alapértelmezett parancsaival. A cél az, hogy a szoftver használata önállóan, segítség nélkül is a lehető legegyszerűbb legyen.

## Tervek

-   [ ] **Facebook Optimalizáció**: A Facebook hírfolyam struktúrájának megértése és felolvasása.
-   [ ] **Telepítőcsomag Készítése**: A kiegészítő becsomagolása egy könnyen telepíthető `.nvda-addon` fájlba. 