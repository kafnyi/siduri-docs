# Siduri — riportok a Zigguratban

> **Státusz: az első szelet KÉSZ** *(2026-09-25, `admin/1.20.0`)*. Az alap az
> eladási archívum (`ELADAS_FELKULDES.md`).

## 1. A döntések *(a felhasználó, 2026-09-25)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **Mely riportok** | a napi forgalom, a termék-toplista, a törlések és sztornók, a borravaló, **és** „az eladások időrendi eloszlása, gépek, pultosok, pultok szerinti lebontások, minden opcionális kimutatás" | több képernyő — egy közös alakkal ez olcsó (2.) |
| **Hol fut** | **előbb csak a felhőben**, az archívumból | internetkimaradáskor nincs riport; a telephelyi Ziggurat 501-et ad |
| **Lánc-szint** | **igen**, telephely-oszloppal (`hatokor=osszes`) — csak azok a telephelyek, amelyekre a felhasználónak joga van | — |
| **Nem igazolt nap** | **mutatja, ELŐZETES jelöléssel**; az ELTÉRŐ nap külön figyelmeztetést kap | a jelölést érteni kell |

## 2. A megoldás

**Egy alak minden riportnak:** oszlopok (típussal), sorok, összesítő — ugyanaz,
amit az XLSX-export (`EXPORT_IMPORT.md` 2.2/a) vár. A felület **egyetlen
általános táblával** jelenít meg és exportál minden riportot; egy új riport a
kiszolgálón egy függvény, a felületen semmi.

| Kód | Riport | Jog |
|---|---|---|
| `NAPI_FORGALOM` | napi sorok: bizonylat, bruttó/nettó/áfa, borravaló, sztornó, kedvezmény, szervizdíj, egyeztetés | `riport.napi_forgalom` |
| `AFA_OSSZESITO` | áfakulcsonként — a könyvelőnek | 〃 |
| `FIZETESI_MODOK` | módonként, a valuta külön | 〃 |
| `TERMEK_TOPLISTA` | termékenként mennyiség és bevétel — a sztornózott bizonylat nélkül | 〃 |
| `ORANKENT`, `HET_NAPJAI` | időrendi eloszlás, **budapesti** idő szerint | 〃 |
| `GEPENKENT` | gépenként, fizetésimód-bontással | 〃 |
| `TELJESITESI_MOD` | helyben / elvitel / kiszállítás | 〃 |
| `KOSARERTEK` | kosárérték-sávok, átlagos tételszám | 〃 |
| `KEDVEZMENYEK` | kedvezmények típus és indok szerint, szervizdíj | 〃 |
| `TELEPHELYEK` | telephelyek összehasonlítása, igazolt/előzetes napokkal | 〃 |
| `PULTOSONKENT` | pultosonként — **munkavállalói adat** | `riport.felhasznalo_tortenet` |
| `TORLESEK` | tételtörlések (konyhára ment-e, mennyi idő után) és sztornók pultosonként | `riport.torlesi_arany` |
| `BORRAVALO` | naponként és pultosonként | `riport.borravalo` |
| `PULT_SZERINT` | a lezáráskori pult szerint *(1.26.0)* | `riport.napi_forgalom` |
| `ARRES` | árrés és food cost, nettó, termékenként × teljesítési módonként *(1.26.0, F5.8)* | `riport.arres` |

A munkavállalói riport a **munkajogi figyelmeztetéssel** jelenik meg, ott, ahol
használják (`JOGOSULTSAG_KATALOGUS.md` 4.10). A pultos és a gép neve az
**eladáskori** érték (`szinkron/1.11.0`) — a riport 8 év múlva is olvasható.

## 3. Amit ez a szelet NEM tud, kimondva

| Mi | Miért | Mikor |
|---|---|---|
| ~~Pult szerinti bontás~~ | **kész** (1.26.0, `KESZLET.md` S6) | — |
| ~~Árrés, food cost~~ | **kész** (1.26.0) — a bizonylatszintű kedvezmény nincs a tételekre osztva | — |
| **Riport a telephelyi szerveren** | döntés: előbb csak a felhőben | ha kell, külön szelet, 30 napos korláttal |
| **Nagy időszak gyorsan** | a számolás memóriában, a bizonylatok JSON-jából; az időszak legfeljebb 366 nap | ha lassú: előre összesített riport-vetület |
| **Régi telephely pultosa** | a `szinkron/1.11.0` előtti telephely nem küldi a kezelőt | „ismeretlen" sorként látszik |
| **PDF** | külön döntés (`EXPORT_IMPORT.md` 6.3) | — |

## 4. Bizonyíték

`FelhoRiportTest` (6): az összegek és a sztornó nettózása, az ELŐZETES nap, a
toplista a sztornózott nélkül, az órás bontás budapesti idő szerint, a
munkavállalói riport saját joga, a lánc-szint jogszűrése, a 366 napos korlát.
**Mutációs próba** (mind megfogva): toplista a sztornózottal · UTC idő ·
lánc jogszűrés nélkül · a pultos riport a napi joggal.
