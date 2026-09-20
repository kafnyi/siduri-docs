# HÁTRALÉK — mi van még hátra, tételesen

**Készült:** 2026-09-20
**Mi ez:** **pillanatkép**, nem igazságforrás. A kötelező érvényű döntések a
`NYITOTT_KERDESEK.md`-ben, a fázisok tartalma a `FAZISTERV.md`-ben, a mérések a
`MERESEK.md`-ben élnek. **Ütközésnél azok nyernek, nem ez a fájl.**

> ⚠️ **Egy pillanatkép attól veszélyes, hogy megbízhatónak látszik, amikor már
> nem az.** Ezért a fejlécben dátum áll, és minden állítás mellett ott van,
> **honnan tudjuk** — kódból ellenőrizve, vagy a dokumentumból idézve.

---

## 0. Hol tartunk (2026-09-20, kódból ellenőrizve)

| | |
|---|---|
| **Repók** | 6 · commitok: docs 117 · backend 46 · kassza 35 · felhő 12 · flutter 4 · frissítő 3 |
| **Tesztek** | 196 (mag) + 330 (szerver) Java · 153 C# (kassza) · 9 (webes admin) |
| **Szerződések** | `kassza` **1.22.0** · `admin` **1.2.0** · `szinkron` (K3) **nincs kiadva** |
| **Adatbázis** | 23 migráció |
| **Kód nélküli repók** | `siduri-flutter-clients`, `siduri-updater` |

---

## 1. F0 — Kapunyitás *(külső átfutás, folyamatosan fut)*

| # | Tétel | Állapot | Mit blokkol |
|---|---|---|---|
| F0.1 | Prior Cash: kapcsolatfelvétel, partneri megállapodás, **fizikai tesztkészülék** | **NYITVA** | A fiskális réteg lezárása; `C10`, `L3`, `E3` |
| F0.2 | MTÜ / NTAK tanúsítás indítása + **lead time** | **NYITVA** | **Az F8 kapuja**, ismeretlen átfutással |
| F0.3 | Hardver: 2 × J1900 + 1 adóügyi eszköz | **NYITVA** | **13 mérés**, köztük az F1 és az F6 kilépési feltételei |
| F0.4 | Könyvelői kérdéssor (borravaló, előleg áfakulcsa) | **NYITVA** | `M9.d`, `N7.c`, `N7.d` |
| F0.5 | Első ügyfél | ✅ megvan (étterem) | — |

---

## 2. F1 — Csontváz *(szerkezet kész, bizonyíték nincs)*

**Kész:** szerződés és verziózás · pénztípusok · bizonylatszámozás · epoch-mező ·
outbox **írása** · audit két ág + hash-lánc · monoton óra.

**Hátra:**

| # | Tétel | Tény |
|---|---|---|
| F1.8 | A vékony szelet **valódi adóügyi eszközre** | Ma naplózó eszköz ír fájlba |
| F1.9 | Minden egy J1900-on, **GraalVM natív kép** | A `pom.xml`-ben **nulla** natív-kép nyom |
| Kapu | **P1 premissza** (A2: az AEE sorszámoz) | **Igazolatlan** |
| Kapu | **M1, M15, M17** | **Nincs mérve** (hardver) |

> **Az F1 formálisan NYITVA van**, miközben az F2 nagy része elkészült.

---

## 3. F2 — Az eladás magja *(a legkészebb fázis)*

**Kész:** terméktörzs · áfacsoportos visszaszámolás · gyorseladás, fizetési módok,
vegyes fizetés · számlamegosztás · kedvezmény · szervizdíj · borravaló · sztornó ·
munkanap, műszak, napzárás, **vakzárás**, címletbontás · jogosultság + söprési
teszt · audit · PIN/RFID · valuta és árfolyam.

**Hátra:**

| # | Tétel | Miért |
|---|---|---|
| 1 | Gyártóspecifikus fiskális illesztő | `F0.1` blokkolja |
| 2 | Eszközregisztráció | Éles telepítéshez kell |
| 3 | **Hét művelet végpont nélkül** | `ar.kezi_felulriras`, `kedvezmeny.tetel`, `tetel.mennyiseg_modositas`, `rendeles.athelyezes`, `rendeles.osszevonas`, `rendeles.nem_fizetett_lezaras`, `muszak.atadas`, `kassza.fiok_nyitas_eladas_nelkul` *(a söprési kivétellistáról)* |

---

## 4. F3 — NTAK *(0% — a küldési logika egyetlen sora sem létezik)*

A sémában csak a kategória-mezők vannak (21 oszlop).

`F3.1` rendelésösszesítő · `F3.2` kimenő sor · `F3.3` feldolgozási nyugta ·
`F3.4` napi zárás · `F3.5` nyitvatartási minta · `F3.6` ENUM-ok konfigurációból ·
`F3.7` `osszesitett` degradált út · `F3.8` mennyiségi egység.

**Előtte eldöntendő:** `H2` (a 25 órás munkanapot az NTAK elutasítja) · `H6` (tíz
új követelmény) · `J6` · `K1.2` · `K3.2` · `A4.1` · **`C11/a`: az RMS Interfész
v1.06 letöltése és feldolgozása KÓDOLÁS ELŐTT.**

---

## 5. F4 — Vendéglátás *(részben)*

**Kész:** asztaltörzs, asztalnyitás, vendégszám, felszolgáló, optimista zárolás;
13 kasszaképernyő.

| # | Hátra | Tény |
|---|---|---|
| 1 | Asztaltérkép-szerkesztő | — |
| 2 | Fogások | sémában 5 nyom, kódban 1 |
| 3 | Módosítók | kódban **nulla** |
| 4 | Menük | kódban **nulla** |
| 5 | KDS, rendeléskijelző | kódban **nulla** |
| 6 | Előnyugta, „fizetésre vár" | kódban **nulla** |
| 7 | Vékonykliens (Flutter) | a repó **üres** |
| 8 | Nyomtatási routing, eszközszám-tartományok | — |
| 9 | **Eseménycsatorna** | az üzenetalakok a szerződésben megvannak, **kiszolgáló oldali megvalósítás nincs**; `M23` mérendő |

**Kapu:** **`M13`** — és ez a kapu az **F6** felé.

---

## 6. F5 — Készlet és admin

**Webes admin:** ✅ elindult — K2 olvasás, árírás, **zárolás kikényszerítve**.
**Készlet:** **0** — raktár, recept, leltár: egyetlen tábla sem létezik.

**Hátra az adminból:** bejelentkezés/munkamenet *(ma fejlesztői kapcsoló)* ·
**a felhős második megvalósítás** *(enélkül a szerződésteszt egy oldalon fut)* ·
export/import *(`M20`, `M22` — könyvtárválasztás nyitott)* · név/áfa/inaktiválás
írása · kategória-, módosító-, menükezelés · felhasználó- és jogosultságkezelés ·
beállításszerkesztés · riportok · **a 30 napos offline korlát kiírása** ·
böngészős átnézés.

**Hátra a készletből:** `F5.1`–`F5.6`, `F5.8`.

---

## 7. F6 — Magas rendelkezésre állás *(0 mechanizmus)*

A szerkezetek megvannak (epoch, outbox-írás, számozási tartományok), a
mechanizmus nem: `F6.1`–`F6.8`.

**Előtte:** `B1/c R1–R5` · `B11` (tanú-séma, jóváhagyásra vár) · `B14.7`.
**Kapu:** `M4`, `M5`, `M6`, `M7`, **`M12`**, `M13`, `M19` — mind hardveren.

---

## 8. F7 — Felhő *(0 kód)*

A `felho/` Maven-modul **nem létezik**; a K3 szerződés **nincs kiadva**.
`F7.1`–`F7.9`.

**Előtte:** **`B7` + `B17` együtt** (multi-tenancy és bővíthetőség) ·
**`B17/d` — a felhő MENTÉSE** *(kimondott hézag: a 8 éves archívumnak nincs
második példánya)* · `B17/b` · `B17/e` · **`B16.7`** (beállítás-paritás őre).

---

## 9. F8 — Élesítés

`F8.1` MTÜ-igazolás + validációs teszt · `F8.2` telepítési ellenőrzőlista ·
`F8.3` frissítési sorrend · `F8.4` pilot · `F8.5` **a teljes `MERESEK.md`
lefuttatása** · `F8.6` **átállási terv**.

---

## 10. Kereszttételek

### 10.1 Döntések — kb. 95 nyitott tétel
A saját prioritástábla szerinti legsürgősebbek: `C11/a` · fiskális
engedélykérdés · `B17/d` · `F4/K2` · `C3/c` · `B14.7` · `B16.4` · `B16.7` ·
`B7` + lánc-szint · `B14.5` · `B11` · `B10` (TPM) · `B12` · `B1/c R1–R5` · `E1`.

### 10.2 Nyolc igazolatlan premissza — ezekre építeni TILOS
`A2` · `A3` · `C10` · `C12` · `B12` · **`B14.5`** *(ha egyetlen sorozat kell, a
bizonylatszámozás megdől)* · `B10` · `N7.c`.

### 10.3 Mérések — 36-ból 23 nincs mérve
**13 fizikai hardvert igényel** (`M1`–`M9`, `M12`–`M14`, `M19`), és az `M12` a
**teljes referencia-telepítést**. Részben mérve: `M25`, `M31`.

### 10.4 Jogi és könyvelői kérdések
Sorszámozás megfelelősége (`B14.5`) · a 8 éves megőrzés helye (`L6`) ·
érintőképernyős aláírás (`B12`) · kártyás borravaló (`M9.d`) · előleg áfakulcsa
(`N7.d`) · DRS-díj gyűjtője (`G4.d`) · vevőkód mint személyes adat · kell-e
engedély a mi szoftverünknek.

### 10.5 Márka — öt nyitott elem
Vektoros eredeti · kisméretű jel (16–32 px) · egyszínű bizonylatfejléc-változat ·
sötét hátterű változat · a „By Myth Systems" alsor szabálya.

### 10.6 Dokumentációs adósság
**Elavult jelölések**, amiket javítani kell: `L1.4/v5` *(az `L2.1` megválaszolta)* ·
`B16/b`, `B16/c` *(az `O3` megválaszolta)* · `B3` (2)–(3) · `B1/c R6` · `E1`
*(„a fázisterv nincs megírva" — pedig megvan)*.

> **Miért nem kozmetika:** egy elavult `[ ]` ugyanúgy néz ki, mint egy valódi
> nyitott kérdés, és a következő olvasó **újra eldönti, ami már el van döntve.**

---

## 11. A kritikus út

```
K3/a hardver ──► F1 kapu ──► [P1 elágazás] ──► F2 ──► F3 ──► K2 tanúsítás ──► F8
                                                 ├──► F4 ──► [M13] ──► F6
                                                 └──► F5
F7 (felhő) ─── önálló sáv ───► az F5.7-nél találkozik
```

**A kritikus úton három dolog van, és egyik sem kód:** a hardver, a tanúsítás, a
gyártói kapcsolat. **Ezen a hármon több munka nem gyorsít.**

---

## 12. Mi mehet külső függőség nélkül — és mi az ára

| Irány | Mit ad | Ára |
|---|---|---|
| **A)** A webes admin folytatása | Élesíti a jogosultsági kivételeket; innen jön a felhasználó- és beállításkezelés | Az export/importnál **megáll** a könyvtárválasztásnál (`M20`, `M22`) |
| **B)** A `felho/` modul váza + a **K2 második megvalósítása** | **Ez élesíti a szerződéstesztet** — ma egy oldalon fut, ami nem paritásbizonyíték | Előbb **`B7` + `B17` együtt** eldöntendő, különben az adatmodellt kétszer írjuk |
| **C)** F4-maradék a kasszán (módosítók, menük, fogások) | Az első ügyfél egy étterem: **ezek nélkül nem tud kereskedni** | Nagy felületi munka; a KDS-hez az eseménycsatorna is kell |
| **D)** NTAK-váz | A leghosszabb külső átfutás előkészítése | **Blokkolja az RMS v1.06** (`C11/a`) — enélkül találgatás |
| **E)** Döntési kör a 15 prioritásos kérdésre | Több későbbi átírást előz meg, mint amennyi kódot most írnánk | Nem termel működő funkciót |

**Javaslat:** **E → B → C.** A `B7` + `B17` és a `B16.4` / `B16.7` pont azt az
adatmodellt érinti, amit a felhőben megírnánk — utólag ez a legdrágább átírás.
