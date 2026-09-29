# Siduri — konyha: fogások, konyhai jegy, KDS, előnyugta (F4)

> **Státusz: a K1 (szerver) és a K2 (Ziggurat) KÉSZ, a K3 (pult) következik** *(2026-09-29)*. Az eldöntött
> szabályok: `NYITOTT_KERDESEK` N4 (fogások), L1.2 (a nem fiskális nyomtató
> kiesése: átirányítás vagy kihagyás, a jegyet szóban kell pótolni),
> `ESEMENYCSATORNA.md` (WebSocket, szívverés, pótlás/újratöltés), `UIUX_TERV`
> (a KDS 2 méterről olvasható), a vékonykliens-repó szabálya (nem ő nyomtat,
> hanem a szerver).

## 1. A felhasználó döntései *(2026-09-29)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **A következő tömb** | **F4 konyha** — fogások, konyhai jegy, előnyugta, KDS | 4–5 szelet; a nyomtatót és a KDS-t élőben csak a felhasználó tudja kipróbálni |
| **A konyhai kiküldés formája** | **nyomtatott jegy ÉS KDS** — ugyanarra a „kiküldés" eseményre | a legnagyobb munka a három közül |
| **Előnyugta és „fizetésre vár"** | **most** — nem adóügyi nyomtatóra, „NEM ADÓÜGYI BIZONYLAT" felirattal; új tételnél magától visszavált | — |
| **Fogások** | **címke + kézi indítás** — az automatikus indítás alapból ki (N4.e) | — |
| **A KDS platformja** | **Flutter**, ahogy terveztük (`siduri-flutter-clients`) | új technológiai lánc a nulláról; a KDS a konyhai sor végén lesz kész |
| **Ki nyomtat** | **a telephelyi szerver**, hálózati ESC/POS nyomtatóra (9100-as port) | a pulthoz USB-vel kötött nyomtató nem megy |

## 2. Alapértelmezett döntések *(felülbírálhatók — az áruk mellettük)*

| # | Döntés | Ára |
|---|---|---|
| D1 | **Állomás** = egy konyhai (vagy bár) pont: neve, **nyomtatócíme** (ha nyomtat), **KDS-e**; egy állomás nyomtathat és kijelezhet is. Leíró-alapú törzsadat (`konyhai_allomas`) | — |
| D2 | **Az irányítás a termék kategóriája szerint**: a kategóriához állomás rendelhető (`allomas_kategoria`); ha nincs, a **legközelebbi szülőkategóriáé** érvényes, ha az sincs, az **alapértelmezett** állomásé; ha az sincs, a tétel nem megy sehova (pl. a pultos ital) | egy termék csak egy állomásra megy (a „leves a konyhára ÉS a salátapultra" nincs) |
| D3 | **Fogás**: a tételsoron 1–9 (üres = azonnal megy); a rendelésnek **aktuális fogása** van (1-ről indul). A kiküldés az aktuális fogásig mindent visz, ami még nem ment; a „Következő fogás" (`rendeles.fogas_inditas`) a következő **létező** fogásra lép, és kiküldi | — |
| D4 | **Kiküldés**: asztalnál **kézi „Konyhára" gomb**; **gyorseladásnál a lezáráskor magától** megy minden | gyorseladásnál a konyha csak a fizetés után kezd |
| D5 | **A nyomtatás a kérésben történik, rövid (3 mp) időkorláttal**; ha a nyomtató nem válaszol, a kiküldés **megtörténik** (a KDS-en látszik), a jegy **HIBA** állapotba kerül, a pult **hangosan jelzi** („szóban pótolni!"), és **újranyomtatható** | a lassú nyomtató 3 másodpercig tartja a pultot |
| D6 | **Előnyugta**: a pult **pultjához** rendelt előnyugta-állomás nyomtatójára megy (`pult.elonyugta_allomas_id`); „fizetésre vár" = van előnyugta, és azóta nem jött új tétel — **számolt állapot**, nem tárolt, így az „új tételnél visszavált" magától igaz | minden előnyugta új példányt nyomtat |
| D7 | **Kódlap**: ESC/POS, CP852 (közép-európai) — az ékezet a jegyen is magyar | a CP852-t nem ismerő nyomtató kérdőjelet nyomtat |
| D8 | **Események**: a kiküldés és az „elkészült" **eseményként tárolódik** (sorszámmal, a K2 csatornájához), így a KDS a lemaradást pótolni tudja (ESEMENYCSATORNA 5.2) | — |

## 3. Szeletek

| # | Szelet | Állapot |
|---|---|---|
| K1 | **Szerver**: állomások és irányítás, fogás a tételen, kiküldés (nyomtatással), következő fogás, előnyugta és „fizetésre vár", az események tárolása; `kassza/1.28.0`, `admin/1.30.0` | **kész** — 5 teszttel (rögzítő nyomtatóval), 8 mutációs próbával; `szinkron/1.20.0`, V47 / felhő V22 |
| K2 | **Ziggurat**: állomások, kategória-hozzárendelés, a pult előnyugta-nyomtatója | **kész** — „Konyha" lap, a pult részleteiben az előnyugta nyomtatója; hu/en/de |
| K3 | **Pult**: fogás a kosárban, „Konyhára", „Következő fogás", „Előnyugta", a nyomtatási hiba jelzése, „fizetésre vár" az asztalon | — |
| K4 | **Eseménycsatorna** (WebSocket, szívverés, pótlás) + a KDS állapot- és „elkészült" végpontja + a KDS párosítása | — |
| K5 | **Flutter KDS** (`siduri-flutter-clients`) | — |
