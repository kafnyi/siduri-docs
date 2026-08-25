# Siduri — Export és import

**Létrehozva:** 2026-08-25
**Kiváltó ok:** felhasználói igény — *„mindenhol, ahol lehet rá igény vagy
szükség, legyen exportálás Excelbe, ne csak PDF-be; a PDF export is maradjon.
Termékek, árak pont azok, amik Excel importért kiáltanak."*

> ⚠️ **Ez a fejezet egy valódi hiányt pótol.** A `siduri_spec_hu.md` eddigi
> változatában **az „export", „PDF", „Excel", „CSV" szavak egyszer sem
> szerepeltek.** Nem azért, mert eldöntöttük, hogy nem kell — hanem mert nem
> került szóba. Egy irodai adminfelületnél ez nem apró hiány.

---

## 1. Az alapelv: melyik formátum mire való

Nem az a kérdés, hogy „legyen-e mindkettő", hanem hogy **mit jelent a
felhasználónak a kettő különbsége.**

| Formátum | Mit jelent | Mire jó |
|----------|------------|---------|
| **PDF** | **Bizonyíték.** Lezárt, nem szerkeszthető, kinyomtatható, átadható | Napi zárás, műszakzárás, bizonylatmásolat, leltárív aláírásra, könyvelőnek átadott kimutatás |
| **XLSX** | **Nyersanyag.** Tovább dolgozol vele: szűröd, összeadod, grafikont csinálsz belőle | Terméklista, árlista, forgalmi bontás, készlet, receptúra, munkaidő, beszerzés |

### 1.1 `[DÖNTÉS]` Ahol MINDKETTŐ kell, ott mindkettő legyen

A legtöbb kimutatásnál **mindkét használat valós**: a könyvelő PDF-et kap
aláírva-lepecsételve, a tulajdonos ugyanazt Excelben nézi tovább. **Ez nem
pazarlás, hanem két különböző felhasználó.**

### 1.2 `[DÖNTÉS]` Ahol az XLSX ÁRT, ott nincs XLSX

**Egyetlen szabály, ami alól nincs kivétel:**

> **Ami bizonyítékként működik, abból nincs szerkeszthető export.**

| Nincs XLSX | Miért |
|-----------|-------|
| **Bizonylatmásolat (nyugta, számla)** | Egy Excelben átírt „nyugta" hamisítvány, amit mi adtunk a kezébe |
| **Napi zárás hivatalos példánya** | Ugyanez |
| **Audit napló biztonsági ága** | Hash-láncolt bizonyíték; egy szerkeszthető másolat pont a lánc értelmét venné el |

**Ez nem bizalmatlanság az ügyféllel szemben.** A dokumentum akkor is
bizonyíték, ha jóhiszeműen adják tovább — és egy Excel-táblázat **nem tud
bizonyíték lenni**, mert bárki átírhatja, és a másolatán nem látszik.

> **A működési auditág kurált nézetei viszont exportálhatók** — azok elemzésre
> valók, nem bizonyításra.

---

## 2. Export — hol legyen

### 2.1 `[DÖNTÉS]` Nem képernyőnként döntjük el, hanem szabályként

**Rossz megközelítés:** végigmenni a képernyőkön, és eldönteni, melyikre kerül
export gomb. Ez garantáltan hiányos lesz, és a hiányzó helyeket az ügyfél
találja meg, nem mi.

**Helyes megközelítés:**

> **Az adminfelület MINDEN listás/táblás nézetéhez jár export.** Nem funkció
> képernyőnként, hanem **egyetlen közös szolgáltatás**, amit minden táblanézet
> megkap.

**Következmény:** ha valaki új listás képernyőt épít, az exportot **nem kell
megírnia** — az jár hozzá. És **nem is felejtheti el.**

### 2.2 `[DÖNTÉS]` Az export azt adja, AMIT LÁTSZ

| # | Szabály |
|---|---------|
| a | **A szűrés érvényes rá.** Ha a képernyőn három hét adata van szűrve, az export is annyi |
| b | **A rendezés érvényes rá** |
| c | **Az oszlopválasztás érvényes rá** — ha a felhasználó elrejtett oszlopokat, azok nincsenek benne |
| d | **Az összesítő sorok ugyanazok** |

**Miért ez a szabály:** ha az export mást ad, mint a képernyő, a felhasználó
**egyszer** veszi észre — és onnantól egyiknek sem hisz.

**Kivétel, kimondva:** ha a képernyő lapozott (pl. 50 sor), az export **a teljes
szűrt eredményt** adja, nem az aktuális oldalt. Ezt **a felület mondja meg
előre**, ne meglepetés legyen: *„Exportálás — 4 312 sor."*

### 2.3 A tipikus helyek

| Terület | XLSX | PDF |
|---------|------|-----|
| Terméktörzs, árlista, kiszerelések | **igen** | igen |
| Kategóriák | **igen** | igen |
| Receptúra, kalkuláció | **igen** | igen |
| Készlet, leltár, mozgások | **igen** | **igen** — a leltárív aláírásra megy |
| Beszerzés, szállítói árak | **igen** | igen |
| Forgalmi kimutatások, árrés | **igen** | igen |
| Fizetési módok, gyűjtő-bontás | **igen** | igen |
| Műszakok, munkaidő | **igen** | igen |
| Felhasználók, szerepek, jogosultságok | **igen** | igen |
| Működési audit kurált nézetei | **igen** | igen |
| Vendégkör, törzsvendég | **igen** | igen |
| **Bizonylatmásolat** | **NEM** *(1.2)* | igen |
| **Napi zárás hivatalos példánya** | **NEM** *(1.2)* | igen |
| **Biztonsági audit ág** | **NEM** *(1.2)* | igen |

---

## 3. Import — ez egy sokkal komolyabb dolog

**Az export olvas. Az import ír — a törzsadatba.** A kettő nem ugyanaz a
kockázati osztály, és nem is szabad ugyanúgy kezelni.

Egy elrontott árlista-import **azonnal rossz áron ad el**, és a hibát a
pénztárnál veszik észre, nem a képernyőn.

### 3.1 `[DÖNTÉS]` Az EXPORT a sablon

> **Az import sablonja nem külön fájl, hanem maga az export.**

Letöltöd a terméklistát Excelbe → átírod, amit kell → visszatöltöd.
**Körbeér.**

**Miért ez a helyes:**

| # | Indok |
|---|-------|
| a | **Nincs külön sablon, ami elavul.** Egy külön karbantartott sablonfájl garantáltan szétcsúszik a valódi oszlopoktól |
| b | **A felhasználó nem tanul új formátumot** — azt tölti vissza, amit letöltött |
| c | **A technikai azonosító benne van**, tehát a párosítás egyértelmű, nem névegyezésen múlik |

### 3.2 `[DÖNTÉS]` Kötelező szárazfutás — közvetlen írás SOHA

**Az import mindig két lépés:**

```
1. Feltöltés  →  ellenőrzés  →  ELŐNÉZET (semmi nincs elmentve)
2. A felhasználó látja, mi történne  →  jóváhagyás  →  írás
```

**Az előnézetben soronként látszik:**

| Minősítés | Mit jelent | Mit mutatunk |
|-----------|------------|--------------|
| **ÚJ** | Ilyen tétel még nincs | Mi jönne létre |
| **MÓDOSUL** | Van, és változna | **Régi → új érték, mezőnként kiemelve** |
| **VÁLTOZATLAN** | Van, és ugyanaz | Külön nem zavarunk vele, csak a darabszám |
| **HIBÁS** | Nem menthető | **Miért — magyarul, sorszámmal és oszlopnévvel** |

**Összesítő a jóváhagyás előtt, konkrét számokkal:**

> *„412 termék változatlan · 38 ár módosul · 6 új termék · 3 sor hibás.
> A 38 áremelés átlagosan +4,2%. A legnagyobb: Dorothy IPA 1 490 → 2 490 Ft (+67%)."*

**A kiugró érték kiemelése nem díszítés.** Az elgépelt ár (1490 helyett 2490,
vagy 149 helyett 1490) **pont így vehető észre** — a jóváhagyás előtt, nem a
pénztárnál.

### 3.3 `[DÖNTÉS]` Az import NEM kerülőút a szabályok alól

> **Amit a felület nem enged, azt az import sem engedi.**

| # | Szabály |
|---|---------|
| a | **Hiányos áfa → a sor hibás.** A kemény kapu kapu marad, tömegesen is |
| b | **Az érvényesség ugyanaz a kód**, mint az egyesével szerkesztésé — nem egy második, lazább változat |
| c | **A jogosultság ugyanaz**, plusz egy külön jog az importra *(3.5)* |

**Ez a leggyakoribb csendes hiba az ilyen rendszerekben:** az import
megkerüli az érvényességi szabályokat, mert „gyorsabb úgy", és fél év múlva
kiderül, hogy a törzsadat fele nem felel meg a saját szabályainknak.

### 3.4 `[DÖNTÉS]` Kötegazonosító és visszavonhatóság

**Minden import egy azonosított köteg**, és a köteg **egészben visszavonható**.

| # | Szabály |
|---|---------|
| a | Az importált változások **kötegazonosítót kapnak** |
| b | **Az ár az ártörténetbe kerül** — tehát az előző ár nem vész el, a visszaállítás nem rekonstrukció |
| c | **A köteg visszavonása új esemény**, nem törlés — az audit mindkettőt látja |
| d | **Ugyanannak a fájlnak a kétszeri feltöltése nem duplikál** — a sor kulcsa (technikai azonosító, ennek hiányában vonalkód) dönt |

### 3.5 `[DÖNTÉS]` Jogosultság és audit

| # | Szabály |
|---|---------|
| a | **Az import külön jogosultság**, nem jár együtt a „terméket szerkeszthet" joggal. **A tömeges módosítás nem ugyanaz, mint az egyesével szerkesztés** |
| b | **A biztonsági auditágra megy** egy bejegyzés a kötegről: ki, mikor, milyen fájlból (**fájl-lenyomat**), hány sor, mi lett az eredmény |
| c | **A működési ágra** entitásonként a tényleges változás |
| d | **Küszöb feletti tömeges áremelés indokot kér** — ugyanaz az elv, mint a küszöb feletti kedvezménynél |

---

## 4. Az Excel csapdái, amik BIZTOSAN elő fognak jönni

Ez a szakasz nem elmélet. Ezek mindegyike **rutinszerűen tönkretesz** import
funkciókat, és mindegyik olcsón megelőzhető — ha előre tudunk róla.

### 4.1 ⚠️ A vonalkód — a legdurvább

**Az Excel a 13 jegyű EAN-kódot számnak látja.**

| Mi történik | Eredmény |
|-------------|----------|
| Megnyitod a fájlt Excelben | `5998200210014` → **`5,9982E+12`** a képernyőn |
| Elmented | A pontosság **elveszhet** a 15 jegyű határ közelében |
| Vezető nullás kód (`0123456789012`) | **A nulla eltűnik** |

**A megoldás, mindkét irányban:**

| Irány | Mit teszünk |
|-------|-------------|
| **Export** | A vonalkód oszlop **szövegként formázva** kerül a fájlba, nem számként |
| **Import** | **Szövegként olvassuk.** Ha mégis szám érkezik (tehát az Excel már elrontotta), azt **felismerjük és HIBÁNAK jelöljük** — nem csendben elfogadjuk, mert a „javításunk" rossz kódot gyártana |
| **Felület** | A hibaüzenet **megmondja, mit tegyen**: *„A vonalkód oszlop számmá alakult az Excelben. Formázd szövegként, vagy tölts le friss sablont."* |

### 4.2 ⚠️ A lebegőpont pont itt lép be a rendszerbe

**Az XLSX a számokat lebegőpontosan tárolja.** Tehát az import **pontosan az a
határ**, ahol az I1 invariáns *(„lebegőpontos szám a pénz közelében sehol")*
megsérülhetne.

| # | Szabály |
|---|---------|
| a | **A pénz- és egységköltség-cellákat szövegként olvassuk**, és `BigDecimal`-lá **szövegből** alakítjuk |
| b | **`double` a beolvasási útvonalon sehol** — az ArchUnit szabály ezt a fordításnál elkapja |
| c | Ha az olvasó könyvtár csak lebegőpontos értéket ad vissza, **az a könyvtár alkalmatlan** *(6. fejezet)* |

> **A már meglévő ArchUnit szabály itt fogja először valóban megfogni a
> kezünket** — és ez a helyes viselkedés. Ha az import kódja megbukik rajta, a
> válasz nem a szabály lazítása, hanem másik olvasási mód.

### 4.3 A többi, sorrendben gyakoriság szerint

| # | Csapda | Kezelés |
|---|--------|---------|
| a | **A felhasználó átrendezi vagy átnevezi az oszlopokat** | **Fejléc szerint azonosítunk, nem pozíció szerint.** Ismeretlen oszlop → figyelmeztetés, nem hiba. Hiányzó kötelező oszlop → az egész fájl elutasítva, névvel megmondva |
| b | **Több munkalap** | **Nevesített munkalapot olvasunk**, nem „az elsőt" |
| c | **Rejtett vagy szűrt sorok** | **Minden sort olvasunk** — a rejtettség megjelenítési állapot, nem adat. Az előnézet a teljes darabszámot mutatja, így kiderül, ha többet hozott, mint hitte |
| d | **Egyesített cellák** | Felismerve, hibaüzenettel — nem próbáljuk kitalálni a szándékot |
| e | **Ezres elválasztó, nem törhető szóköz beillesztett értékben** | Beolvasáskor normalizálva, de **az előnézet az értelmezett értéket mutatja**, hogy látható legyen |
| f | **Automatikus dátumkonverzió** *(„1-2" → január 2.)* | A szöveges oszlopok szövegként exportálva; importnál a váratlan dátumtípus hiba |
| g | **A régi `.xls` formátum** | **Nem támogatjuk.** A hibaüzenet megmondja: mentsd `.xlsx`-ként |

### 4.4 `[DÖNTÉS]` CSV — csak bemenetként, és csak kimondva

**Az XLSX az elsődleges formátum mindkét irányban.**

**A CSV-t importnál elfogadjuk**, mert a szállítói árlisták gyakran így
érkeznek — **de kimondva, nem kitalálva:**

| # | Szabály |
|---|---------|
| a | **Az elválasztót és a kódolást a felhasználó választja ki**, alapértelmezés a magyar Excel szokása (pontosvessző, UTF-8), de **felismerve és felajánlva** |
| b | **A tizedesvessző/tizedespont kérdését kimondjuk**, nem tippeljük — ez a CSV egyetlen legnagyobb csendes hibaforrása |
| c | **Exportnál CSV nincs.** Ha valakinek CSV kell, az XLSX-et menti annak. Nem gyártunk saját CSV-értelmezési problémákat |

---

## 5. Hol fut — és milyen vason

| Eset | Hol keletkezik a fájl |
|------|----------------------|
| **Normál** — laptop, felhő | **A felhőben** |
| **Offline** — telephelyi kiszolgálás | **A telephelyi szerveren** |

**Ebből következik két kötelező tulajdonság:**

| # | Követelmény |
|---|-------------|
| a | **Közös kód.** Ugyanaz az export/import motor fut mindkét helyen — különben a néma szétcsúszás, amit a §22.2 döntéssel már megöltünk |
| b | **Folyamatos írás/olvasás (streaming), nem memóriában összeállítás.** Egy 20 000 soros forgalmi export **nem foglalhat 20 000 sornyi memóriát** egy J1900-on, ami közben szervert és POS-t is futtat |

**Az offline korlát itt is él:** a telephelyi kiszolgálás **30 napnál régebbi
adatot nem tud exportálni** *(§24.2)*, és **ezt meg kell mondania**, nem
csendben rövidebb fájlt adni.

---

## 6. `[NYITOTT — DÖNTÉST IGÉNYEL]` Könyvtárválasztás, és egy valós ütközés

### 6.1 ⚠️ Az Apache POI és a GraalVM natív fordítás ütközik

**A Java-világ alapértelmezett Excel-könyvtára az Apache POI.** Nagy tudású,
kiforrott — **és erősen reflexió-alapú.**

> **A GraalVM natív fordítás pont a reflexiót nem szereti.** A POI natív képbe
> illesztése ismerten körülményes: kiterjedt elérhetőségi leírót igényel, és a
> hibák **fordítás után, futásidőben** jelentkeznek.

**Ez valódi ütközés a saját stack-döntésünkkel**, nem elméleti aggály.

### 6.2 A javaslat: könnyű, folyamatos írású könyvtár

| Jelölt | Mellette | Ellene |
|--------|----------|--------|
| **`fastexcel` (dhatim)** — **javaslat** | Kis felület, folyamatos írás és olvasás, kevés reflexió → **natív képbe jóval jobban illik**. A memóriaigénye töredéke | Kevesebbet tud: **nincs diagram, korlátozott formázás** |
| **Apache POI (SXSSF)** | Mindent tud | **A natív fordítás kockázata**; nagyobb memória |

**Miért elég a kevesebb tudás:** amit exportálunk, az **adat, nem
dokumentum**. Fejléc, oszlopszélesség, szám- és szövegformátum, fagyasztott
fejlécsor, automatikus szűrő — ennyi kell. **Diagramot a felhasználó csinál
magának, az az Excel dolga, nem a miénk.**

### 6.3 `[NYITOTT]` A PDF könyvtár még nincs eldöntve

Ugyanaz a szempont áll rá: **natív képbe illeszthetőség**, és a magyar
karakterkészlet helyes kezelése beágyazott betűtípussal.

**Ez külön döntés, külön mérés** — nem intézhető el mellékesen.

---

## 7. Mérési kötelezettségek

| # | Mérés | Miért blokkoló |
|---|-------|----------------|
| **M20** | **Az Excel-könyvtár natív képbe fordul-e**, és a beolvasás ad-e szöveges cellaértéket lebegőpont nélkül | Ha nem, az egész formátumválasztás dől — és vele az I1 invariáns az import határán |
| **M21** | **20 000 soros export memóriaigénye és ideje a telephelyi szerveren**, POS-szal együtt futva | Az offline kiszolgálás valós terhelése |
| **M22** | **A PDF könyvtár natív képbe fordul-e**, magyar ékezetekkel, beágyazott betűtípussal | Ugyanaz, a másik formátumra |

---

## 8. Nyitott kérdések

| # | Kérdés |
|---|--------|
| **E1** | **Ütemezett export?** *(pl. minden hónap 5-én a könyvelőnek e-mailben.)* Valós igény, de **kimenő e-mail-küldés a rendszerből** önálló döntés — nem csúsztatjuk be egy export funkció mellé |
| **E2** | **Több telephely exportja egy fájlba** — telephelyenként külön munkalap, vagy egy tábla telephely-oszloppal? A lánc-nézetnél merül fel |
| **E3** | **Az import ütemezhető-e** *(szállítói árlista automatikus beolvasása)*? **Az álláspontom: NEM, v1-ben.** A szárazfutás emberi jóváhagyást igényel, és **egy automatikus árlista-import emberi szem nélkül pontosan az a funkció, ami egy éjszaka alatt tönkretesz egy árlistát** |
