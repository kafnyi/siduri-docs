# Siduri — Asztaltérkép (F4 #1)

> **Státusz: a T1–T4 KÉSZ** *(2026-09-30)* — hátra a böngészős és a pulton végzett élő próba. Forrás: `siduri_spec_hu.md` §21.1
> („vizuális szerkesztő — rajzolható háttér, asztalok elhelyezése, alakja,
> testreszabása"), `UIUX_TERV.md` (az asztaltérkép a pult tájékozódó nézete),
> `HATRALEK.md` F4 #1.

## 0. Honnan indulunk

Az `asztal` tábla létezik (V18: szám, megnevezés, szabad szöveges `terulet`, férőhely,
aktív, sorrend), de **nincs írási útja** (csak tesztek szúrnak be), nincs helye a
térképen, és a pult egy gombrácsban mutatja. Nincs terem, nincs háttér, nincs jog.

## 1. A felhasználó döntései *(2026-09-30)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **Hol szerkeszthető** | **a Zigguratban ÉS a pulton is** | két szerkesztő (Vue és WPF) — nagyjából dupla felületi munka |
| **Elrendezés** | **szabad koordináták**, és teremenként egy **kapcsolóval rács nézet**: N×M rács, az asztalok mérete és a cellán belüli igazítás állítható; **termek és teremenként eltérő háttérkép mindkét nézetben** | a két nézet két helyet tárol asztalonként |
| **A pult asztalválasztója** | **térkép teremfülekkel** | új WPF-nézet; élő próba a pulton |

## 2. Alapértelmezett döntések *(felülbírálhatók — az áruk mellettük)*

| # | Döntés | Ára |
|---|---|---|
| D1 | **A terem új leíró törzstábla** (`terem`): név, sorrend, aktív, `elrendezes` (SZABAD / RACS), a terem logikai mérete (`szelesseg` × `magassag`, alap 1600 × 1000), a rács (`racs_oszlop` × `racs_sor`, alap 8 × 5), a rácsbeli asztalméret (`racs_meret`, a cella %-a, alap 80) és igazítás (`racs_igazitas`, 9 érték, alap KOZEP), `hatter` (a háttérkép lenyomata) | — |
| D2 | **Az asztal leíró törzstábla lesz** (O3, szinkron mindkét irányba): szám, megnevezés, terem, férőhely, alak (KEREK / SZOGLETES), szabad hely (`x`, `y`, `szelesseg`, `magassag`, `forgatas` 0–359), rácsbeli hely (`racs_oszlop`, `racs_sor`, `racs_szeles`, `racs_magas` cellában), sorrend, aktív. A régi `terulet` szövegből **terem** lesz (migráció) | O3 mezőnként: két egyidejű húzásnál az `x` és az `y` más-más íróé lehet — ritka, látszik, újrahúzással javul |
| D3 | **A koordináta a terem logikai egysége**, nem képpont: a kijelző a terem arányában skáláz — minden felbontáson ugyanúgy néz ki | — |
| D4 | **A rácsbeli méret és igazítás a teremé** (egy helyen állítható); asztalonként csak a kiterjedés (hány cellát foglal) | asztalonként eltérő méret rácsban csak cellaszámmal |
| D5 | **A két nézet együtt él**: az asztal mindkét helyét megőrzi, a váltás nem veszít adatot. Az el nem helyezett asztal (üres hely) egy sávban látszik, onnan húzható be. Rácsra váltáskor a szerkesztő felajánlja: „a szabad helyekből rácsba" | — |
| D6 | **A háttérkép tartalom-címzett** (SHA-256): PNG / JPEG / WebP, legfeljebb 2 MB; **SVG nem** (szkriptet hordozhat). A terem csak a lenyomatot hordozza (O3); a kép bájtjai külön mennek a szinkronnal (fel: a telephely küldi, amit ott töltöttek fel; le: a telephely elkéri, ami hiányzik). A pult lenyomat szerint gyorsítótáraz | két új szinkron-végpont |
| D7 | **Jog:** új `asztal.kezeles` (termek, asztalok, háttér) — az ÜZLETVEZETŐ sablonban. Olvasás a Zigguratban: `termek.megtekintes`; a pulton az asztalos eladás joga | — |
| D8 | **A pult szerkesztője** az asztalképernyő „Térkép szerkesztése" módja (`asztal.kezeles`): húzás (szabad) / cellába tétel (rács), új asztal, tulajdonságok, a terem beállításai, háttérkép fájlból. Az írás a kassza API-n megy, **ugyanazzal a leíró-íróval** (forrás: telephely, O3) | a kassza-szerződésbe két törzs-író végpont kerül (csak `terem` és `asztal`) |
| D9 | **A nyitott rendelésű asztal nem tűnik el**: helyben nem inaktiválható (409), és ha a felhőből inaktív lesz, a pult a rendelés lezárásáig mutatja | — |
| D10 | Az élő frissítés (más pincér nyitott asztalt) marad a mostani újratöltés; az eseménycsatornás frissítés **később** (`ESEMENYCSATORNA.md`) | a térkép a képernyőre lépéskor frissül |

## 3. Szeletek

| # | Szelet | Állapot |
|---|---|---|
| T1 | **Háttér**: `terem`, `asztal` leíróként, `kep`; migrációk mindkét oldalon; jog; kép-végpontok (admin, kassza); a kassza `/asztalok` a hellyel, `/termek`; a kép szinkronja | **kész** — V54 (a régi `terulet` teremmé vált), felhő V25; `admin/1.32.0`, `kassza/1.34.0`, `szinkron/1.23.0`; a foglalt asztalszám 409, a nyitott rendelésű asztal nem inaktiválható, és a felhőből inaktiváltan is látszik (D9); a kép a tartalma szerint típusos, SVG nem. 3 telephelyi + 2 felhős + 1 szinkron- + 2 k2-teszt, 11 mutációs próba. A pult törzs-író végpontjai a T4-be kerültek |
| T2 | **Ziggurat**: „Asztalok" lap — teremfülek, szerkesztő (húzás, rács kapcsoló, tulajdonságok, háttér feltöltése), közös elrendezés-számítás tesztekkel | **kész** — SVG-térkép (húzás, nyilak, rácsvonalak, háttér), rácsbeállítások a terem sávjában, „a szabad helyekből rácsba", az el nem helyezettek sávja, a kiválasztott asztal minden mezője (O3-nyommal); a közös szabály a `szerzodes/tesztvektorok/asztalterkep.json` (egész aritmetika) — a pult ugyanezt futtatja. ⚠️ Böngészős próba hátra |
| T3 | **Pult**: a térkép teremfülekkel (olvasás), az elrendezés-számítás C#-ban tesztekkel | **kész** — a Mag `Asztalterkep.Elrendezes` a közös vektoron (6 eset); a terem Viewboxban, a saját arányában, háttérképpel (lenyomat szerint gyorsítótárazva), forgatott és kerek asztalok, a foglaltság szövegesen is; az el nem helyezettek a régi gombsorban; régi kiszolgálónál minden ott. 186 pult-teszt. ⚠️ Élő próba a pulton hátra |
| T4 | **Pult**: a szerkesztő mód | **kész** — az asztalválasztó „Térkép szerkesztése" gombja (`asztal.kezeles`): húzás (a vászonhoz mért pozícióval, így az elforgatott asztal is jó irányba megy), új asztal és terem, adatok, forgatás, méret, alak, rácskiterjedés, levétel, megszüntetés; a terem rácsa, asztalmérete, igazítása és háttérképe. `kassza/1.35.0`: `POST/PUT /torzs/{terem\|asztal}`, `POST /kepek` — a Zigguratéval azonos író (O3). 1 telephelyi teszt, 2 mutációs próba. ⚠️ Élő próba a pulton hátra |
