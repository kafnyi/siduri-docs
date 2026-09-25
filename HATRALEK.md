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

## ⚠️ ÉLESÍTÉST BLOKKOLÓ HIBA — JAVÍTVA *(2026-09-24)*

**A telephelyi szerver adatbázis-kapcsolatai nem kapták meg a telephelyet**
(`siduri.telephely_id`). A sorszintű elhatárolás ebből dönt, és ha nincs,
**egyetlen sort sem** enged át. Élesben az alkalmazás a `siduri_app` szereppel
fut — **minden elhatárolt tábla üresnek látszott volna** (eszköz, bizonylat,
jogosultság, napló).

Egyetlen teszt sem vette észre, mert fejlesztésben és tesztben a séma
tulajdonosa fut (mentesül), az elhatárolás tesztje pedig a saját kapcsolatán
kézzel állította be az értéket. **Javítva:** a kapcsolatkészlet minden
kapcsolatot a telepítés telephelyével nyit; új teszt az alkalmazás saját
kapcsolatait vizsgálja; élő próba `siduri_app`-ként: belépés, lista, árírás rendben.

⚠️ **A tanulság, általánosan:** ami csak élesben fut másként (szerep, jogosultság,
TLS, proxy), azt élesítés előtt **az éles beállítással** is ki kell próbálni. Egy
zöld tesztkészlet erről nem mond semmit.

## 6. F5 — Készlet és admin

**Webes admin:** ✅ elindult — K2 olvasás, árírás, **zárolás kikényszerítve**.
**Készlet:** **0** — raktár, recept, leltár: egyetlen tábla sem létezik.

✅ **Kész** *(2026-09-24)*: bejelentkezés és munkamenet (`admin/1.7.0`) · a
felhős második megvalósítás · felhasználó- és jogosultságkezelés, a jogok emberi
nevével (`admin/1.8.0`) · telephelyválasztó (`admin/1.9.0`) · teljes angol és
német felület · böngészős átnézés.

✅ **Kész még** *(2026-09-24)*: a Siduri kollégafiókjai (`admin/1.10.0`–`1.11.0`),
a termék neve és állapota O3-mal (`admin/1.12.0`, `szinkron/1.6.0`), új bérlő,
telephely és telepítési jegy (`admin/1.13.0`); *(2026-09-25)* áfakategóriák és
a termék áfájának írása (`admin/1.14.0`), tanúsítvány visszavonása
(`admin/1.15.0`), a kategóriafa szerkesztése O3-mal (`admin/1.16.0`,
`szinkron/1.8.0`), a Siduri-hozzáférés a pulthoz — a felhő, a telephely és a
Ziggurat oldala (`admin/1.17.0`, `szinkron/1.9.0`, `kassza/1.24.0`; a pult
rejtett belépése az 5/c-vel).

✅ **Kész még:** a termék felvétele, törlése és visszaállítása (`admin/1.21.0`,
`szinkron/1.12.0`, C2/b alapértelmezett döntései). **Hátra a termékből:**
kiszerelés felvétele meglévő termékhez, vonalkód-hozzárendelés, a valódi törlés
(döntés: most nincs).
✅ A riportok első szelete (`admin/1.20.0`, `RIPORTOK.md`) — 14
kimutatás, csak a felhőben. A **30 napos offline korlát kiírása** így továbbra
sem kell: a telephelyi szerver a riportokra 501-et ad.
✅ Az eladási adatok felküldése a felhőbe, napi egyeztetéssel
(`szinkron/1.10.0`, `ELADAS_FELKULDES.md` §8) — a riportok erre épülhetnek.
✅ Az XLSX-export minden listás nézetben (`admin/1.18.0`,
EXPORT_IMPORT 2.2/a). **Hátra belőle:** az M20/M21 mérés a telephelyi élesítés
előtt, a PDF (külön döntés) és az import (külön munka). **Még
döntés kell:** módosító- és menükezelés (C1), beállításszerkesztés. A kiszolgálótól jövő szövegek (hibaüzenetek, jogosultságnevek)
nyelvváltáskor magyarok maradnak.

**A készlet** (`KESZLET.md`): az S1–S4 (törzsadat, készletmotor, felhős tükör és parancs, leltár) kész; hátra az S5 („elfogyott" — pult-kliens is) és az S6 (pult a bizonylatban + árrés).

---

## 7. F6 — Magas rendelkezésre állás *(0 mechanizmus)*

A szerkezetek megvannak (epoch, outbox-írás, számozási tartományok), a
mechanizmus nem: `F6.1`–`F6.8`.

**Előtte:** `B1/c R1–R5` · `B11` (tanú-séma, jóváhagyásra vár) · `B14.7`.
**Kapu:** `M4`, `M5`, `M6`, `M7`, **`M12`**, `M13`, `M19` — mind hardveren.

---

## 8. F7 — Felhő *(elindult)*

✅ **A `felho/` modul megvan** *(2026-09-21)*: a **K2 második megvalósítása**,
bérlőnkénti sémával (B7), és egy **közös `k2` modul**, amiből mindkét oldal
ugyanazokat az alakokat és ugyanazt a **szerződéstesztet** használja. A
modulhatárt ArchUnit őrzi.

**Amit ez megold:** a „egy admin, két helyről kiszolgálva" eddig **állítás**
volt; mostantól **gépi kényszer** — a közös teszt bizonyítottan elbukik, ha a
két oldal viselkedése eltér.

✅ **A felhő jogosultság-ellenőrzése megvan** *(2026-09-22)*. A felhő a **saját**
hozzáférés-nyilvántartásából dolgozik, **telephelyenkénti kiosztással**, és a válasz
ugyanaz, mint a telephelyi oldalon (`NINCS_JOGOSULTSAG`, 403). **A közös
szerződésteszt mostantól ezt is kérdezi mindkét megvalósításon** — a kapu tehát
gépi kényszer, nem szándék.

**Ára, kimondva:** **két felhasználó-nyilvántartás**. Akit a telephelyen
kirúgnak és ott letiltanak, annak a felhős hozzáférése **megmarad**, amíg ott is
le nem tiltják. Ez eljárási feladat, nem kódé: a kiléptető listán mindkét
helynek szerepelnie kell. Cserébe létezhet olyan központi kategóriafelelős vagy
tulajdonos, akinek **egyáltalán nincs** telephelyi fiókja.

**Ami ebből még hiányzik a felhőben:** írás (az ármódosítás ma csak a telephelyi
oldalon él) · ~~bejelentkezés~~ ✅ **kész** *(2026-09-24, `admin/1.7.0`, lásd
`BEJELENTKEZES.md`)* · a webes admin **böngészős átnézése** *(✅ 2026-09-23, a felhőn: hat felületi hiba javítva, lásd lent)*.
A **felhasználókezelés** külön fejezet lett — lásd lentebb.

### A hozzáférési modell — megtervezve, még nem megépítve *(2026-09-23)*

⚠️ **A teljes leírás: `HOZZAFERES.md`.** Ez itt csak a munkadarabok listája.

A döntések megszülettek: **három populáció** *(pultos · bérlői Ziggurat · Siduri
kolléga)*, a pultos nyilvántartás **gazdája a felhő**, a pultban **szintezett
hierarchia**, a bérlői Zigguratban **felhasználónkénti jog + sablon**, a hatókör
**típus + azonosító**, és a **burok** mindkét irányban *(csak azt adhatod és veheted
el, amid van)*.

⚠️ **A 2026-09-22-én megépített felhős táblák átszabásra szorulnak**: a bérlői
oldalra szerepkör-alapú modellt építettem, a döntés viszont felhasználónkénti
jogokat mond. Adatvesztés nincs *(sehol nem éles)*, de új migráció kell — a
Flyway a lefutott migrációt nem engedi visszamenőleg átírni. Ez a menet közbeni
döntéshozatal szokásos ára.

**A darabok, sorrendben:**

| # | Darab | Állapot |
|---|---|---|
| 1 | **A hozzáférési modell a felhőben** — szintek, hierarchia, burok, személyre szabott eltérés, 0. szint, típus+azonosító hatókör | ✅ **kész** *(2026-09-23)* |
| 2 | **Bérlői Ziggurat-fiókok kezelése** — jogok, sablonok, sablon-visszaállítás | ✅ **kész** *(`admin/1.4.0`)* |
| 3 | **A pultos nyilvántartás átköltöztetése** a felhő gazdasága alá, telephelyi másolattal | ✅ **kész** *(`szinkron/1.2.0`)* |
| 4 | **Pultos fiókok kezelése a Zigguratról** + a két fiók összekapcsolása | ✅ **kész** *(`admin/1.5.0`)* |
| 5/a | **A felhő oldala** — globális kiértékelés, jogosultság-napló, offline elbírálás | ✅ **kész** |
| 5/b | **A telephelyi szerver és a szerződések** — `szinkron/1.3.0`, `kassza/1.23.0`, offline tábla, felküldés, öt végpont | ✅ **kész** |
| 5/c | **A pult képernyője** — WPF, helyi lista és globális fül | hátra |
| 6 | **A Siduri-hozzáférés** — forgó kód, néma belépés, növekvő várakozás, láncolt napló | hátra |
| 7 | **Belső kollégafiókok** — jogkörök, kapcsolók, négy szem elv | hátra |

⚠️ **Amit a 4. darab NEM old meg:** a szerepjelölők közül csak a
**sérthetetlen** látszik eleve letiltva. A **szint** és a **burok** korlátját a
kiszolgáló dönti el, és a felület az elutasítás után **visszaolvassa** az
állapotot. Ez helyes, de **egy kattintásnyi kitérő**: a felhasználó előbb
próbálkozik, csak utána tudja meg, hogy nem lehet. Az előzetes jelöléshez a
szereplistának **felhasználónként** kellene megmondania, kiosztható-e —
vagyis **szerződésbővítés** *(ÁRA: egy újabb `admin` kisverzió, és a
szereplista a cselekvőtől is függne, tehát nem lenne gyorstárazható)*.

**Amit ez a kör ELHALASZTOTT, kimondva:** második tényező a belső fiókokhoz
*(vállalt kockázat: egy kiszivargó kollégajelszó = minden bérlő minden adata)* ·
a raktár mint **entitás** *(csak a hatókör dőlt el)* · a készletkezelés egésze ·
RFID/fizikai kulcs a Siduri-fiókhoz.

✅ **A 403 saját képernyőt kapott a webes adminban** *(2026-09-22)*. Két
különböző 403 van, és a képernyő **szétválasztja** őket: `NINCS_JOGOSULTSAG`
*(a felhasználónak kell jogot kapnia)* és `MASIK_TELEPHELY` *(beállítási hiba —
ezen semmilyen jogosultság nem segít)*.

A képernyő **kimondja, melyik kiszolgáló utasította el**, és azt is, hogy a két
oldal külön nyilvántartásból dolgozik — ennélkül a felhasználó azt hinné, hogy
a jogosultsága „eltűnt". Ehhez a **szerződést is bővíteni kellett**
(`admin/1.3.0`: a `Siduri-Kiszolgalo` fejléc mostantól a **hibaválaszokon is**
kötelező), és a telephelyi oldalon pótolni, mert eddig nem küldte. A közös
szerződésteszt mindkét megvalósításon megköveteli.

⚠️ **Amit ez a szelet NEM old meg:** a képernyő **böngészőben nincs
megnézve** — a döntési logikát teszt fedi, a típusok fordulnak, a kiszolgáló
oldala élőben ellenőrzött, de a **megjelenés** nem. *(2026-09-24: a felhasználókezelő
felület és a bejelentkezés elkészült, böngészőben átnézve.)*

✅ **Böngészőben átnézve** *(2026-09-23, felhő, fejlesztői bérlő)*: termékek,
felhasználók két füle, felhasználó lapja, kapcsolt fiók, felvétel, 403. Javítva:
a cím még „Siduri admin” volt · a keresőgomb felirata a helykitöltő szövege volt ·
dupla elválasztó e-mail nélkül · a 403 alatt ott maradt az „Új felhasználó” gomb ·
a kapcsolt fiók figyelmeztetése nem mondta meg, **ki** a másik (most hivatkozás;
ehhez a nézet az útvonalváltáskor újratölt, különben csak az URL változott volna).

⚠️ **Amit az átnézés talált, de NEM javított:**
* A jogosultságok **nyers kódként** látszanak (`termek.ar_modositas`). Emberi
  név a szerződésből kellene *(ÁRA: `admin` kisverzió)*; egy felületi fordítótábla
  csendben elcsúszna a kiszolgáló katalógusától.
* Az **angol és német** szöveg a felületnek csak ~12 kulcsát fedi — a többi
  magyarul jelenik meg nyelvváltás után is.
* A **401** még nyers hibakódot mutat (`NINCS_MUNKAMENET: …`) — a bejelentkezés
  képernyőjével együtt készül.
* ⚠️ **Az előző érték nem látszik az árnál.** A szabály szerint a mező mellett
  látszania kell, mikor, honnan **és mi volt előtte** — az első kettő megvan, a
  harmadikat a szerződés nem adja *(ÁRA: `admin` kisverzió)*. Enélkül egy
  elveszett átírás nyoma csak a naplóban van, a képernyőn nem.
* ✅ Az **áfa** olvasható kulcsként látszik (27%); a fejlesztői adat
  **kategóriafát** kap *(2026-09-25, a meglévő adatbázison is)*. ⚠️ Az `E_0` ma
  „0%”-ként jelenik meg — a pénztárgépen ez a TAM gyűjtő; az áfakategóriával
  javul.

✅ **A telephelyi szerverrel is átnézve** *(2026-09-23)*: termékek, zárolt és
szerkeszthető ár, eredet, a „csak a felhőben” magyarázat. Javítva: a magyarázat
a pultos fülön is a Ziggurat-fiókokról szólt · az árszerkesztő mezőinek nem volt
akadálymentes címkéje. ✅ **Az ár- és a névírás a felületről, a telephelyi
szerverrel élőben kipróbálva** *(2026-09-25)*.

✅ **A K3 szerződés kiadva ÉS megvalósítva** *(2026-09-21, `szinkron/1.0.0`)*:
lefelé törzsadat és zárolás, felfelé nyugta és állapot.

⚠️ **LELET (2026-09-24): a telephelyen átírt törzsadat NEM jut fel a felhőbe.**
A szinkron-szerződésben (és a kódban) felfelé csak lekérdezés, nyugta és
hozzáférés-változás megy — **mezőérték nem**. Következmények:

* A telephelyről kiszolgált Zigguratban átírt ár a felhős Zigguratban **a régi
  értékkel látszik tovább**, és semmi nem jelzi, hogy eltér. Ez néma kudarc.
* A „későbbi írás nyer” szabályt ma **csak a telephely** alkalmazza (a lefelé
  érkező értékre). A felhő a telephelyi írásról nem tud, tehát nem is dönthet.
* A döntés szerint *„a teljes [ár]történet a felhőben áll”* — **a felhőben
  nincs ártörténet**, és felküldés nélkül nem is lehetne.
* A „mi volt előtte / mi veszett el” kijelzése a felhőben emiatt **felküldés
  nélkül nem építhető meg**: a vesztes érték többnyire a telephelyen keletkezik.

**A terv: `TORZSADAT_FELKULDES.md`** — ✅ **mind a hat darab kész** *(2026-09-24,
`szinkron/1.4.0`, `admin/1.6.0`)*: a telephelyi írás és a kezdeti katalógus
felmegy, és a Ziggurat az ár mellett mutatja, mi volt előtte, és mi nem lépett
érvénybe — okkal.

✅ **Javítva** *(2026-09-24)*: hibás JSON-ra mindkét oldal **400**-at ad
(`HIBAS_KERES`), nem 500-at — a felhő is ugyanígy hibázott.
Közben kiderült, hogy a felhőben **egyáltalán nincs törzsadat-írás** — a kezdeti
feltöltést is ennek kell megoldania. Sorrend: felküldés → írás-történet mindkét
oldalon → előző/vesztes érték a szerződésben és a felületen.

**Élő próbán végigvitt út:** a felhőbe tett árváltozás a telephelyi
adatbázisban landolt (2400 → 2650 → 2790), a felhő **ALKALMAZTA** nyugtát
kapott, a mezőeredet a **felhőt** mondja, az ártörténet lezárta a régi sort, és
a leérkezett **zárolás után a közvetlen SQL-írás is elbukik** a telephelyen.

✅ **A kölcsönös TLS megvalósult** *(2026-09-21, `szinkron/1.1.0`)*: saját
hitelesítő, ujjlenyomat-nyilvántartás azonnali visszavonással, automatikus
regisztráció egyszer használható jeggyel, **egy port — két állomásnév**.

**Élő próbán végigvitt út:** valódi (openssl-lel készült) hitelesítő → jegy → CSR
→ kiállított tanúsítvány *(az alanynév a **jegyé**, nem a kérelmezőé)* → valódi TLS
1.3 kézfogás → `200`. **Ugyanazzal a tanúsítvánnyal, idegen telephellyel a
testben: `403`.** Tanúsítvány nélkül `401`, a jegy másodszorra `403`. Az
`admin.*` állomásnév ugyanazon a porton **nem kér** kliens-tanúsítványt.

**Hátra:** az aláírás bekapcsolása (a mező már a szerződésben, kulcskezelés kell
hozzá) · a tanúsítvány **megújítása** (ma kézi: új jegy kell; a szerver 30 nappal
a lejárat előtt figyelmeztet) · a jegyek **kiadási felülete** (ma SQL-sor) · az
eladási adatok felküldése (8 éves archívum) · a felhő jogosultság-ellenőrzése ·
`F7.1`–`F7.9` többi része.

✅ **A bérlői migrációs rés bezárva** *(2026-09-22)*. A rés: egy **új bérlői
migráció nem ért el a MÁR LÉTEZŐ bérlői sémákhoz**, mert a sémamigráció csak a
bérlő létrehozásakor futott. Élesben ez azt jelentette volna, hogy egy frissítés
után a **régi** bérlők csendben kiesnek, az újak meg működnek — elő is jött: egy
régebbi bérlő sémájából hiányzott a `valtozas` tábla, és a szinkron **500**-zal
állt meg.

**Mostantól induláskor minden nyilvántartott sémán lefut a migráció.** Egy bérlő
hibája nem állítja meg a többit — de azt a bérlőt **nem szolgáljuk ki** (`503`),
mert egy félig migrált séma vagy értelmetlen hibával áll meg, vagy lefut és
**hiányos adatot ad**.

**Ára:** az indulás lassul, mérve **kb. 50 ms bérlőnként**. Ma ez nem számít; ezer
bérlőnél percekben mérhető lesz, és akkor a már naprakész sémákat át kell ugrani.

**Az adatmodell 2026-09-21-én ELDŐLT** *(az E-kör első batchje)*:

| Tétel | Döntés | Ami vállalt kockázat maradt |
|---|---|---|
| `B7` | **Bérlőnként külön séma** | A migráció N sémán fut; a sémaváltás egyetlen belépési ponton, teszttel |
| `B17/b` | **Két gép, vállaltan aszinkron** | **Failovernél néhány másodperc írás elveszhet** — a `W4` vállalásnak ezt ki kell mondania; a veszteségablak `M5`-ként mérendő |
| `B17/d`, `B17/e` | **Külön mentési rendszer, magyar adatközpontban** | **Országos szintű esemény mindkét helyet érheti** — újranyitandó, ha nő az ügyfélkör |
| `B16.7` | **Egy beállítás-regiszter + padlós paritás-őr** | Minden új beállítás a regiszterbe kerül, nem a kódba |

---

## 9. F8 — Élesítés

`F8.1` MTÜ-igazolás + validációs teszt · `F8.2` telepítési ellenőrzőlista ·
`F8.3` frissítési sorrend · `F8.4` pilot · `F8.5` **a teljes `MERESEK.md`
lefuttatása** · `F8.6` **átállási terv**.

---

## 10. Kereszttételek

### 10.1 Döntések — kb. 95 nyitott tétel
**A 2026-09-21-i döntési kör (E) tizenhat tételt zárt le:**

| Kör | Eldöntve |
|---|---|
| 1. — a felhő adatmodellje | `B7` · `B17/b` · `B17/d` · `B17/e` · `B16.7` |
| 2. — munkanap és számozás | `K1` *(már teljesült a kódban)* · `F4/K2` · `B14.7` · `C3/c` |
| 3. — magas rendelkezésre állás | `B11` *(ezzel `R1`, `R2` is)* · `R3` · `R4` · `R5` · `B16.4` |
| 4. — üzemeltetés | `D3` · `D4` · `D5` · `D6` |

**A prioritástáblából NYITVA maradt — de ezek egyike sem a mi döntésünk:**

| Tétel | Kinek a kérdése |
|---|---|
| `C11/a` | **MTÜ** — az RMS Interfész v1.06 beszerzése, és hogy minden szoftververzió után kell-e újravalidálni |
| fiskális engedélykérdés | **NAV / gyártó** — kell-e engedély a mi szoftverünknek |
| `B14.5` | **Könyvelő / jogász** — megfelel-e az eszközönkénti számtartomány a folyamatos sorszámozásnak. **Ha nem, a bizonylatszámozás megdől** |
| `B12` | **Jogász** — mit ér az érintőképernyős aláírás |
| `B10` (TPM) | **A felhasználó** — van-e TPM a meglévő gépeken |
| `E1` | Elavult jelölés: a fázisterv **megvan**, a `[ ]` a hibás |

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
