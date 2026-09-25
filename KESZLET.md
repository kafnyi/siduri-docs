# Siduri — készlet és receptúra (F5)

> **Státusz: az S1 (törzsadat) KÉSZ, az S2 munkában** *(2026-09-26)*. A fázisterv F5.1–F5.6
> és F5.8 pontja. A már eldöntött alapszabályok: `NYITOTT_KERDESEK` B16.4
> (a készlet egyenlege telephely-autoritatív, a felhő MOZGÁST küld, egyenleget
> soha nem ír felül), B16.10 (leltár = korrekciós mozgás fordulónapra), G2.2
> (a módosító a recepttől eltérés), I3 (bruttó + kötelező beszerzési áfa, az
> árrés nettó), G5.3 (egységköltség 6 tizedes, nem lebegőpontos), M12 (a készlet
> soha nem blokkol eladást; a kézi „elfogyott" igen).

## 1. A felhasználó döntései *(2026-09-26)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **Mikor von le az eladás** | a bizonylat **lezárásakor**, egy tranzakcióban; a **sztornó visszaírja** (ellen-mozgás, az eredeti költségen); a lezárás előtt törölt tétel nem von | a nyitott asztal fogyása csak fizetéskor látszik; ha a sztornózott ital valóban elfogyott, selejtként kell rögzíteni |
| **Készletcikk és receptúra** | külön **alapanyag**, **többszintű** recepttel (félkész termék is lehet összetevő) | kb. másfélszeres munka: körfigyelés, rekurzív levonás, a félkész előállítása |
| **Raktár és pult** | **a Pult most bevezetve**: gép → pult → raktár; a riport pult szerint is bont | kb. +30% munka |
| **Mértékegység** | anyagonként **egy alapegység** (g, ml, db) **+ csomag-átváltás** (karton = 24 db, hordó = 50 000 ml) | egy mező és egy átváltó a bevételezésen |

## 2. Alapértelmezett döntések *(felülbírálhatók — az áruk mellettük)*

| # | Döntés | Ára |
|---|---|---|
| K1 | Az **alapanyag telephelyenként** él, mint a termék | lánc-szintű közös anyaglista később, külön szelet |
| K2 | A **recept egy O3-mező** (a tételek listája egyben); a hozam külön mező | ha két oldal ugyanannak a receptnek két különböző sorát írja egyszerre, az egyik írás egészében veszít — a felület kiírja |
| K3 | A **félkész** anyagnál választható: **nem készletezett** (alap: eladáskor a saját receptjére bomlik, egészen az alapanyagig) vagy **készletezett** (ELŐÁLLÍTÁS mozgással készül, az eladás a félkészből von) | — |
| K4 | A recept **legfeljebb 5 szint** mély, és **kör nem lehet** — mindkét oldal ugyanazzal a közös kóddal ellenőrzi | — |
| K5 | **A mozgás a saját korabeli átlagárát rögzíti** → az árrés visszamenőleg is helyes (ez a C2/a nyitott második fele) | mozgásonként egy szám — semmi |
| K6 | A **mozgóátlagárat az adatbázis-trigger** számolja a mozgás beszúrásakor (egy hely, nem felejthető el); nettó, 6 tizedes. **Negatív bázis:** a nullán vagy mínuszban kiadott mennyiség az utolsó ismert bekerülési áron megy ki; a hiányt feltöltő bevételezés után az átlag = a bevételezés ára, és az anyag **„korrekcióból számolt átlag"** jelölést kap | — |
| K7 | **Telephelyenként egy „Fő raktár"**, azonosítója = a telephelyé — így a két oldal ütközés nélkül, egymástól függetlenül is létrehozhatja | — |
| K8 | A **gép → pult** hozzárendelés szinkronizált törzsadat: a telephely felküldi a gépeit, így a felhőből is kiosztható. **A pult-kliens nem változik** — a szerver a bizonylatot záró gépből tudja a pultot és a raktárat. Pult nélküli gép a Fő raktárból von | — |
| K9 | **Recept nélküli kiszerelés nem von** — a Ziggurat külön listában mutatja őket | amíg valaki nem nézi a listát, az a termék nincs készleten követve |
| K10 | A **levonó módosító** (G2.2) és az **allergének** (M5.a) a C1-gyel jönnek — ma nincs módosító | — |
| K11 | **Bevételezés:** bizonylatként (szállító és számlaszám szövegként, szállító-törzs nélkül); soronként bruttó összeg + beszerzési áfa (az anyagé, felülírható) → nettó egységköltség; alapegységben **vagy** csomagban | nincs szállító-nyilvántartás |
| K12 | **Leltár:** raktáranként, részleges is (csak a megszámolt anyag kap korrekciót); fordulónap = időpont; a leltárív mutatja a **kalkulált veszteség %**-ot (anyagonként megadható) a tényleges eltérés mellett. PDA és papír-ív később | — |
| K13 | **A felhő** a telephely mozgásait archívumként kapja meg (mint az eladásokat) — ebből mutat készletet és árrést; a felhőből indított mozgás **parancsként** megy le, a telephely könyveli | a felhős készletkép a szinkron késésével frissül |
| K14 | A **selejt** és a **személyzeti fogyasztás** mozgás (nem eladás), indokkal; az NTAK-kérdés (J7) nyitva marad | — |
| K15 | Az **„elfogyott"** jelző kiszerelésenként, telephelyi állapot (nem O3-törzsadat); a pult szürkén mutatja | pult-kliens változás (a K8 kivétele) |

## 3. Az adatmodell

**Törzsadat — mindkét oldal írja, O3, szinkron mindkét irányban** (egy közös,
leíró-alapú út: `k2` `TorzsLeirok`; egy új tábla egy leírás, nem új kód):

| Tábla | Mezők (mind O3) |
|---|---|
| `anyag` | név, típus (ALAPANYAG / FELKESZ), alapegység (G / ML / DB), csomagok, beszerzési áfa, készletezett, kalkulált veszteség %, aktív |
| `recept` *(azonosítója a tulajdonosé: kiszerelés vagy félkész anyag)* | hozam, tételek (`anyag = mennyiség` lista) |
| `raktar` | név, aktív |
| `pult` | név, eladási raktár, aktív |
| `eszkoz_pult` *(azonosítója a gépé)* | gép neve (csak olvasható, a telephelyé), pult |

**Mozgás — csak a telephely könyvel**: `keszlet_mozgas` (csak beszúrás; fajta:
ELADAS, SZTORNO, BEVETELEZES, ATADAS_KI/BE, SELEJT, SZEMELYZETI, ELOALLITAS_KI/BE,
LELTAR; mennyiség alapegységben, előjelesen; nettó egységköltség),
`keszlet_egyenleg` (raktár × anyag: mennyiség, átlagár, jelölések),
`keszlet_bizonylat` (a bevételezés, átadás, selejt, leltár fejléce).

## 4. Szeletek

| # | Szelet | Állapot |
|---|---|---|
| S1 | Törzsadat: a közös leíró-alapú út + anyag, recept, raktár, pult, gép→pult; Ziggurat-képernyők | ✅ `admin/1.22.0`, `szinkron/1.13.0`; 6 mutációs próba, mind megfogva; élő próba (HTTP) |
| S2 | Készletmotor a telephelyen: mozgás, egyenleg, átlagár; eladás levonása lezáráskor, sztornó; bevételezés, átadás, selejt, személyzeti, előállítás | — |
| S3 | Felhő: a mozgások archívuma, felhős készletkép, felhőből indított mozgás | — |
| S4 | Leltár | — |
| S5 | „Elfogyott" jelző (kassza + pult-kliens) | — |
| S6 | Pult a bizonylatban → pult szerinti riport; árrés-riport teljesítési módonként (F5.8) | — |
