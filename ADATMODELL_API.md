# F1 alapok — adatmodell magja és API-szerződés

**Utolsó frissítés:** 2026-08-23
**Fázis:** F1.1–F1.7 (`FAZISTERV.md`)
**Miért itt és most:** ezek **szerkezetek, nem funkciók.** Utólag beletenni őket
annyi, mint utólag naplózni: elvileg lehet, gyakorlatilag újraírás.

---

## 0. Amit ez a dokumentum eldönt, és amit nem

**Eldönt:** kereszmetsző konvenciókat (azonosító, pénz, bérlő, idő, törlés),
az invariánsokat kikényszerítő szerkezeteket (számozás, epoch, outbox, hash-lánc),
a fő entitásokat és kapcsolataikat, és az API-szerződés szabályait.

**Nem dönt el:** minden entitás minden oszlopát. Az implementációkor jön, és
ha most leírnám, csak elavulna.

---

# I. RÉSZ — ADATMODELL

## 1. Azonosítók

### 1.1 `[DÖNTÉS]` Elsődleges kulcs: UUIDv7, `uuid` típusban

| Szempont | Miért ez |
|----------|----------|
| **A kliens offline hoz létre rekordot** | A degradált módban a POS **szerver nélkül** ír az outboxba. **Szerver által kiosztott sorszám itt nem működik** — a kliensnek magának kell azonosítót adnia |
| **Miért v7 és nem v4** | A v7 **időrendezett**. A véletlen v4 elsődleges kulcs a B-fa lapjait folyamatosan hasítja, és a gyorsítótár-találati arányt lerontja. **A J1900 korlátozott memóriáján ez nem elméleti** |
| **Miért `uuid` és nem `text`** | `uuid` = **16 bájt**, szöveges alak = 37. Indexméretben és lapszámban ez a különbség a szűkös gépen látszik |

**Szabály:** minden entitás elsődleges kulcsa `uuid` (v7), **a kliens is
kioszthatja.**

### 1.2 Az azonosító NEM a bizonylatszám

Két külön dolog, és soha nem keverendő:

| | Technikai azonosító | Bizonylatszám |
|---|---|---|
| Mi | `uuid` v7 | `xxxxxxyyyzzzzz` |
| Kinek | a rendszernek | embernek és hatóságnak |
| Ki adja | bárki (kliens is) | a **kiállító eszköz**, saját tartományból |
| Mikor | rekord létrehozásakor | bizonylat kiállításakor |
| Egyedi | globálisan | üzleti napon belül eszközönként |

### 1.3 `[ELDÖNTVE]` Vonalkód — NEM cikkszám

**Az ügyfél nem a leváltott rendszer cikkszámát akarja, hanem VONALKÓD-kezelést.**
A vonalkód-olvasó már ott van a gépeken; ha egyszer ott van, a kólát is le
lehessen csippantani.

**Ez más entitás, mint egy cikkszám, és másképp is kell modellezni:**

| # | Szabály |
|---|---------|
| a | **A vonalkód a KISZERELÉSHEZ tartozik, nem a termékhez.** A 0,33 és a 0,5 literes kóla **külön EAN** — ezért is jó, hogy a kiszerelés önálló gyermek entitás |
| b | **Egy kiszereléshez TÖBB vonalkód tartozhat** (más beszállító, régi és új csomagolás, gyűjtőcsomag) → **önálló `vonalkod` tábla, nem oszlop** |
| c | **Egyediség telephelyen belül**: egy vonalkód **pontosan egy** kiszerelésre mutathat, különben a beolvasás kétértelmű. Globálisan ugyanaz az EAN más bérlőnél természetesen létezhet |
| d | **Nem azonosító.** A rekord kulcsa továbbra is `uuid` v7 |
| e | **Leváltott rendszerből származó cikkszám NEM kell** |

#### 1.3.1 Beolvasási viselkedés

| Eset | Mi történik |
|------|-------------|
| **Ismert vonalkód** | A kiszerelés a kosárba kerül, mennyiség 1 |
| **Ismeretlen vonalkód** | **Nem hiba, hanem lehetőség:** „ismeretlen vonalkód — melyik termékhez tartozik?" → hozzárendelés meglévő kiszereléshez, **jogosultsághoz kötve**, auditnaplózva |

> **Az ismeretlen kód hozzárendelése a legértékesebb része a funkciónak.**
> Így a vonalkód-készlet **használat közben épül fel**, nem külön adatrögzítési
> projektként. Enélkül a funkció csak addig ér valamit, amíg valaki egyszer
> beviszi az összes kódot — vagyis soha.

#### 1.3.2 `[TERVEZÉSI KIKÖTÉS]` A HID-billentyűzet probléma

**A vonalkód-olvasók többsége billentyűzetként viselkedik** — begépeli a
számjegyeket és nyom egy Entert. A felületnek **meg kell tudnia különböztetni a
beolvasást attól, hogy valaki kézzel beírt egy számot.**

Szokásos megoldás: **időzítés** (az olvasó nagyságrenddel gyorsabban „gépel",
mint az ember), opcionálisan előtag-karakterrel megerősítve.

**Ezt a felület-tervezésbe kell venni**, nem utólag ráakasztani — mert
befolyásolja, hogy a POS-nak mikor van „fókuszban" a beviteli mező.

#### 1.3.3 `[NYITOTT — v2]` Mérleges vonalkód

A mérlegek által nyomtatott, **súlyt vagy árat magába kódoló** vonalkód
(jellemzően `2`-vel kezdődő EAN-13) valós minta a kiskereskedelemben.
**Étteremhez most nem kell, de a szerkezet ne zárja ki** — a vonalkód-feloldás
legyen bővíthető mintaillesztéssel.

---

## 2. Pénz

### 2.1 `[DÖNTÉS]` Két típus, semmi más

| Fogalom | Használat | PostgreSQL | Kód |
|---------|-----------|------------|-----|
| **Összeg** | eladási ár, sorösszeg, végösszeg, fizetés, kedvezmény | **`bigint`** — egész forint | saját `Penz` értéktípus, `long` belsővel |
| **Egységköltség** | beszerzési egységár, mozgóátlagár, receptmennyiség szorzata | **`numeric(18,6)`** | saját `Egysegkoltseg` értéktípus |

**`double`, `float`, `real` pénz közelében TILOS** — sem oszlopban, sem
kódban, sem API-ban, sem JSON-ban. *(I1)*

### 2.2 A `Penz` típus szabályai

* **Nincs implicit konverzió** számra és számból — csak explicit, nevesített művelet.
* **Nincs `Penz` × `Penz`.** Csak `Penz` × mennyiség és `Penz` ± `Penz`.
* **Az áfa-visszaszámolás nem a típus dolga**, hanem külön szolgáltatásé — mert **áfakulcs-csoportonként, bizonylatszinten** történik, nem soronként *(I3)*.
* **A kerekítés explicit művelet**, soha nem mellékhatás.

### 2.3 Valuta

**Az árak MINDIG forintban vannak.** A valuta csak a **fizetésnél** jelenik meg:

| Mező | Tartalom |
|------|----------|
| `osszeg_huf` | `bigint` — ez megy a könyvelésbe és a bizonylat összesítőjébe |
| `penznem` | `HUF` / `EUR` |
| `eredeti_osszeg` | `numeric(18,2)` — amit a vendég ténylegesen adott, ha nem HUF |
| `arfolyam` | `numeric(18,6)` — a **felhasznált** árfolyam, a bizonylat mellett tárolva |

**Nincs többvalutás árlista.** Ha később kell, az új döntés lesz, nem
mellékhatás.

---

## 3. Bérlő és telephely

**Minden üzleti táblán kötelező `telephely_id`.** Nem opcionális, nem
következtethető.

```
berlo (tenant)
  └── telephely (site)          ← MINDEN üzleti adat ide kötődik
        ├── eszkoz (device)
        ├── felhasznalo
        ├── termek, kategoria, …
        └── munkanap, bizonylat, …
```

| # | Szabály |
|---|---------|
| a | **Sorszintű szűrés adatbázis-szinten** (RLS vagy kikényszerített szűrő), nem csak az alkalmazásban. Egy elfelejtett `WHERE` **nem szivárogtathat át telephelyek között** |
| b | A **lánc/franchise** a bérlő szintjén él; a **zárolt központi értékek** öröklődnek lefelé |
| c | **Egy telepítés egy telephelyet szolgál ki.** A több telephely a felhő dolga *(§22.3)* |

### 3.1 `[DÖNTÉS]` A telephelyi és a felhős séma KÖZÖS magja

**Ugyanaz a mag-séma fut lokálisan és a felhőben**, a felhőben kiegészítésekkel
(több telephely, lánc, zárolás, archívum).

**Miért:** ha a két séma elválik, **ugyanaz a néma szétcsúszás keletkezik, amit
a „EGY admin alkalmazás, két helyről kiszolgálva" döntéssel (§22.2) már egyszer
megöltünk.** Két séma két igazságot szül, és senki nem veszi észre.

**Ára:** a felhős séma nem lehet szabadon optimalizált a saját terhelésére. Ezt
elfogadjuk.

---

## 4. Idő és sorrend

### 4.1 `[DÖNTÉS]` Minden rekord HÁROM időadatot hordoz

| Mező | Típus | Mire |
|------|-------|------|
| `eszkoz_ido` | `timestamptz` | Az **eszköz** órája a keletkezéskor |
| `szerver_ido` | `timestamptz` | A **szerver** órája a befogadáskor *(offline keletkezésnél a szinkronizálás ideje)* |
| `sorszam` | **`(epoch, szamlalo)`** | **A SORRENDET EZ ADJA** |

> **A sorrendezés soha nem a faliórán múlik** *(I17)*. Nem azért, mert az óra
> pontatlan lehet — hanem mert **javíthatjuk**, és egy visszaugró óra
> megfordítaná az események sorrendjét.

### 4.2 `[DÖNTÉS]` A monoton sorszám = `(epoch, számláló)`

**Ez a HA-ból következik, és elegánsan old meg egy különben csúnya problémát.**

Ha a sorszám egyetlen szerverszintű számláló lenne, **átvételkor a tartalék
szerver számlálója nem ott folytatná**, ahol a fő abbahagyta — és a sorrend
összekeveredne.

**Megoldás:** a sorszám **pár**: az `epoch` (fencing-generáció, minden
szerepváltásnál nő) és azon belül egy számláló.

* **Lexikografikusan rendezhető** → a sorrend átvétel után is helyes.
* **A fencing és a sorrendezés ugyanaz a mechanizmus** — nem két külön dolog, amit szinkronban kell tartani.
* Egy régebbi epochú szervertől érkező rekord **azonnal felismerhető** — és a kliens is elutasíthatja *(F6.5)*.

### 4.3 A munkanap hossza

**Két méréssel**, és a vágást **a konzervatívabb dönti el** *(I15)*:

| Mérés | Mire |
|-------|------|
| Monoton (szerver felfelé számláló órája) | Elsődleges |
| Falióra-különbség (`zaras − nyitas`) | Ez megy az NTAK-ba, tehát ezt is figyelni kell |

---

## 5. Az invariánsokat kikényszerítő szerkezetek

### 5.1 Bizonylat-számozás

```
bizonylat_szamlalo
  telephely_id, eszkoz_szam, uzleti_nap   → utolso_folyoszam
  ELSŐDLEGES KULCS: (telephely_id, eszkoz_szam, uzleti_nap)
```

| # | Szabály |
|---|---------|
| a | **Eszközönként elhatárolt tartomány** → az ütközés **szerkezetileg lehetetlen**, nulla koordináció kell *(I13)* |
| b | **Az `uzleti_nap` az ÜZLETI nap dátuma, nem a naptári** |
| c | A **tartalék szerver átvételkor AZONNAL kiszolgálhat** — nem kell egyeztetnie |
| d | Az **adóügyi szám külön, NULLÁZHATÓ mező** a bizonylaton *(I14)* |
| e | **Új mező:** `nyomtato_eszkoz_id` — melyik adóügyi eszköz nyomtatta *(§8.3)* |

### 5.2 Outbox

```
outbox
  id (uuid v7), telephely_id, eszkoz_id
  sorszam (epoch, szamlalo)
  tipus, tartalom (jsonb), tartalom_hash
  allapot: LETREHOZVA | ELKULDVE | NYUGTAZOTT | HIBA
  probalkozasok, utolso_hiba
```

| # | Szabály |
|---|---------|
| a | **Csak hozzáfűzhető.** A rekord tartalma soha nem módosul, csak az állapota |
| b | **A nyomtatási szándék IDE kerül, a fiskális eszköz hívása ELŐTT** *(I26)* |
| c | **Nyugtázatlan rekordot a megőrzés soha nem töröl** *(§24.2)* |
| d | A visszajátszás **idempotens** — az `id` egyben az idempotencia-kulcs *(lásd II./6)* |

### 5.3 Audit — két áram

```
audit_biztonsagi                    audit_mukodesi
  id, telephely_id                    id, telephely_id
  sorszam (epoch, szamlalo)           sorszam
  felhasznalo_id  (UUID!)             felhasznalo_id (UUID!)
  szerep_pillanatkep (jsonb)          entitas_tipus, entitas_id
  eszkoz_id                           esemeny, adat (jsonb)
  esemeny, elotte, utana (jsonb)      eszkoz_ido, szerver_ido
  indok_kod, indok_szoveg
  elozo_hash, sajat_hash            (nincs hash-lánc)
```

| # | Szabály |
|---|---------|
| a | **`BEFORE UPDATE` és `BEFORE DELETE` trigger, ami kivételt dob** — adatbázisszinten, nem alkalmazásban *(I24)* |
| b | **A felhasználó UUID-vel hivatkozva, soha nem szöveges névvel** *(I35)* |
| c | **A szerep PILLANATKÉP** — az akkori szerep, mert a jelenlegi hazudna |
| d | **A hash-lánc csak a biztonsági ágon** — napi 5000 soron pazarlás, napi 200-on ingyen |
| e | **Felhős horgonyzás:** a lánc aktuális hash-e időnként a felhőbe |
| f | A **működési ág** legyen **entitásonként hatékonyan lekérdezhető** (asztal, felhasználó, rendelés) → indexelési követelmény *(§18.4)* |

### 5.4 NTAK kimenő sor

**Külön tábla, nem az outbox** — más az ütem (15 perc), más az állapotgép, és
**van egy második, visszamenőleges folyamata** (a feldolgozási nyugta lekérdezése).

```
ntak_kimeno
  id, telephely_id, targynap
  tipus: RENDELESOSSZESITO | NAPIZARAS
  tartalom (jsonb)
  allapot: VARAKOZIK | ELKULDVE | NYUGTA_VAR | KESZ | ELUTASITVA
  feldolgozas_azonosito          ← a szinkron válaszból
  nyugta_lekerve, nyugta_eredmeny
  osszesitett, osszesitett_indok  ← a degradált mód útvonala
```

**Kikötés:** a sor **sorrendtartó és átfedésmentes** *(I19)*, és a
**nyugta-lekérdezés kötelező, 24 órán belül** *(I20)*.

---

## 6. Fő entitások

### 6.1 Termék

```
kategoria ──(szülő, max 4 szint)── kategoria
    │
    └── termek ──── kiszereles (gyermek: saját ár, térfogat, vonalkód)
          │
          ├── termek_ar_tortenet (mikortól meddig mennyi)
          ├── recept_tetel ──── anyag ──── allergen (opcionális)
          ├── termek_modosito_csoport (hozzárendelés, FELÜLÍRÁSOKKAL)
          └── menu_komponens ──── menu_komponens_opcio (termék + felár)
```

| # | Szabály |
|---|---------|
| a | **Két áfamező kötelezően kitöltve**, plusz `azonos_afa` jelölő. **A jelölő MÁSOL, nem hivatkozik** *(I4)* |
| b | **Kemény kapu:** hiányos áfa vagy hiányzó NTAK-kategória → **nem menthető** *(I5)* |
| c | **A kiszerelés hordozza az NTAK `mennyiseg` értékét** (0,33 stb.), nem a neve |
| d | **A hozzárendelés (`termek_modosito_csoport`) hordozza a felülírásokat** — pl. a `FreeLimit` ingyenes-választás módja |
| e | **Az allergén az ANYAGHOZ tartozik**, a termék listája **élő származtatás** — az egyetlen kivétel az A3/A4 elv alól *(I45)* |
| f | Életciklus: `aktiv` / `inaktiv` / `soft_delete` — **egyik sem rejt el a történetből** |

### 6.2 Rendelés és bizonylat

```
munkanap (telephely) ──── muszak (eszköz + felhasználó)
    │
    └── rendeles ──── rendeles_tetel ──── tetel_modosito
          │                  │
          │                  └── menu_peldany_id   ← a szétrobbantott menü csoportosítója
          │
          └── bizonylat ──── fizetes
```

**`rendeles`:** asztal, vendégszám, **teljesítési mód** (helyben / elvitel /
kiszállítás), **fogás-állapot** (melyik fogás ment már el), nyitás/zárás,
`targynap`.

**`rendeles_tetel` — az ELADÁSKORI állapot MÁSOLATA:**

| Mező | Miért másolat |
|------|---------------|
| `nev_eladaskor` | A termék neve változhat |
| `brutto_ar_eladaskor` | **Az ár a sor létrehozásakor rögzül és soha nem értékelődik újra** *(I42)* |
| `afa_kulcs_eladaskor` | Ugyanaz |
| `ntak_fokategoria`, `ntak_alkategoria` | A kategória átsorolható |
| `fogas_sorszam` | Melyik fogáshoz tartozik |
| `menu_peldany_id` | Ha menüből robbant szét, melyikből |

> **Ez a legfontosabb szerkezeti döntés a bizonylatban.** A tétel **nem
> hivatkozik** a termékre az árért — **másolatot tart**. Enélkül minden
> visszamenőleges riport hazudna, és a happy hour determinizmusa (§12.10)
> megvalósíthatatlan lenne.
>
> A `termek_id` **megmarad hivatkozásként** — de csak riportáláshoz és
> visszakereséshez, **soha nem az árért.**

**A menü a bizonylaton nem létezik önálló tételként** — csak a komponensei, közös
`menu_peldany_id`-vel, és egy fejléc-szövegsorral *(I8)*.

### 6.3 Jogosultság

```
felhasznalo ──── szerep ──── szerep_jogosultsag ──── jogosultsag (katalógus)
                   │
                   └── felhasznalo_jogosultsag_kivetel (egyedi eltérés)
```

| # | Szabály |
|---|---------|
| a | **A jogosultság-katalógus ADAT, nem kód** — bővíthető frissítéssel |
| b | **Új jogosultság a meglévő szerepeken alapból TILTOTT**, feltűnő jelzéssel *(§18.1)* |
| c | **A Siduri admin szerep sérthetetlen** — az ügyfél nem módosíthatja *(§18.2)* |
| d | A **vékonykliens fizetési joga** szerveroldali, az admin felületen **meg nem jelenő** jogosultság *(§21.2)* |

---

## 7. Korábbi nyitott kérdések — lezárva

**Mindkét korábbi kérdés megválaszolva** *(vonalkód: 1.3 · tartalomfordítás: 8)*.

**Új, ennél fontosabb nyitott tétel keletkezett belőlük:** lásd **§9 — az eCassa
megjegyzés.**

## 8. `[ELDÖNTVE]` Tartalomfordítás — MVP, de csak HU + EN

**Az első ügyfél KÉRI az angol terméknevet. A német nem prioritás.**

| Réteg | Nyelv | Címke |
|-------|-------|-------|
| **Szoftverszövegek** (gomb, hibaüzenet, riportfejléc) | **HU + EN + DE** — ez a mi munkánk, olcsó | `MVP` |
| **Tartalom** (terméknév, kategórianév, módosítónév, leírás, allergénszöveg) | **HU + EN kötelezően támogatva**, DE ugyanazon a szerkezeten később, fejlesztés nélkül | `MVP` |

**Ebből következik:** a **fordítástáblák az F2-be kerülnek**, nem `v1`-be.

```
forditas
  entitas_tipus, entitas_id, mezo, nyelv → szoveg
  ELSŐDLEGES KULCS: (entitas_tipus, entitas_id, mezo, nyelv)
```

| # | Szabály |
|---|---------|
| a | **Mezőnként opcionális, MAGYAR visszaeséssel.** Ha nincs angol név, a magyar jelenik meg |
| b | **Kényszeríteni tilos** — nincs mentési kapu hiányzó fordításra *(A3 elv)* |
| c | **DE: „hiányzó fordítások" lista** a webes adminban. Nem kapu, hanem **segédlet** — az ügyfél kéri az angolt, tehát látnia kell, hol tart |
| d | **Új nyelv = adat, nem fejlesztés.** A szerkezet nyelvfüggetlen |

### 8.1 Hol jelenik meg az angol név — és hol NEM

| Felület | Nyelv |
|---------|-------|
| **Fiskális nyugta** | **MAGYAR, mindig** — jogszabályi kötöttség. **Az angol név ide SOHA nem kerül** |
| Nem fiskális példány | választható |
| QR-os vendégoldal | a vendég nyelve |
| Másodkijelző (vendégtájékoztató) | választható |
| KDS, konyhai jegy | **magyar** — a konyha magyarul dolgozik |
| Riportok | a felhasználó nyelve |

> **Ez a leggyakoribb félreértés-forrás:** hogy „a rendszer angolul is tud", az
> **nem jelenti azt, hogy a nyugta angol lehet.** Az adóügyi bizonylat nyelve
> kötött.

## 9. `[!!] ÚJ, FONTOS` — az „eCassa" megjegyzés

Az ügyfél megjegyzésében szerepel, hogy a vonalkód-olvasó **„az eCassa rendszer
miatt"** van a gépeken.

> **Az eCassa egy magyar online pénztárgép-márka. Ha az első ügyfélnek eCassa
> adóügyi eszköze van, akkor a teljes fiskális integrációs előkészületünk
> ROSSZ GYÁRTÓRA irányult.**

Eddig a **Fiscat / Prior Cash** illesztő-protokollra készültünk — az a
dokumentum, amit kaptunk, és amiért a partnerkapcsolatot építjük (K1).

**Ez közvetlenül érinti:**

| # | Mit |
|---|-----|
| a | **K1 kapu** — lehet, hogy más gyártóval kell kapcsolatba lépni, vagy MINDKETTŐVEL |
| b | **F1 kilépési feltétele** — „valódi bizonylat valódi eszközön": **melyik eszközön?** |
| c | **A gyűjtőkiosztás** (§10.3) — a kapott 8 rekeszes kiosztás **eszközspecifikus lehet** |
| d | **A nulla összegű tétel és a DRS-gyűjtő kérdései** — más gyártónál más a válasz |

**AZONNALI TEENDŐ — ez a D7 döntési pont legfontosabb kérdése:**

> **Pontosan milyen adóügyi eszköz van az első ügyfélnél? Gyártó, típus,
> és melyik cég szervizeli?**

*Lehetséges, hogy a Prior Cash több márkát is forgalmaz és az illesztő közös —
de erre **feltevést építeni tilos**, mert az egész F1 fázis erre az egy eszközre
épül.*

---

# II. RÉSZ — API-SZERZŐDÉS

## 1. `[DÖNTÉS]` Stílus: REST + JSON, mellette WebSocket

| Réteg | Mi | Miért |
|-------|-----|-------|
| **Parancs és lekérdezés** | **REST + JSON HTTPS-en** | Három különböző kliens (C# WPF, Flutter, böngésző). **Univerzális, hibakereshető**, és a mi forgalmi nagyságrendünkön (percenként néhány száz kérés, nem másodpercenként ezrek) a JSON-feldolgozás költsége nem szűk keresztmetszet |
| **Kitolás (push)** | **WebSocket** | Rendelésállapot, KDS, rendeléskijelző, asztalfrissítés, **csökkentett-mód jelzés**. Lekérdezgetéssel ez a J1900-at feleslegesen terhelné |

**Miért nem gRPC:** a böngészős admin `grpc-web` réteget igényelne, a Flutter web
esetet bonyolítja, és a nyerhető sávszélesség itt nem szűkös. **A hibakereshetőség
többet ér, mint a bájtok.** *(Ha később egy útvonalon mégis szűkös lesz, az
pontszerű döntés, nem az egész szerződés.)*

## 2. `[DÖNTÉS]` Hol él a szerződés

**Az `siduri-backend-server` repóban, dedikált útvonalon, OpenAPI-ként**, és
**verziózott artefaktumként publikálva**, amit a többi repó fogyaszt.

| Alternatíva | Miért nem |
|-------------|-----------|
| `siduri-docs` | **Kód soha nem kerül oda** — ez repószabály |
| Külön 6. repó | Ceremónia egy szerződésért, ami egyetlen gazdához tartozik |

**Szabály:** a szerződés gazdája a backend, **de a változtatás a kliens-oldali
gazdák jóváhagyásával megy.** Egy szerződés, egy gazda, több érdekelt.

## 3. `[DÖNTÉS]` Verziózás és visszafelé kompatibilitás

* **Fő verzió az útvonalban:** `/v1/…`
* **Kisebb változás csak ADDITÍV** — új opcionális mező igen; mező eltávolítása vagy jelentésváltozása **soha**.

> **KEMÉNY KÖVETELMÉNY: egy még nem frissített POS-nak TOVÁBB KELL TUDNIA
> ELADNI.**

Ez nem elvi elegancia, hanem a saját üzemeltetési szabályunkból következik:
**a szerepet vivő gépek nem frissülhetnek egyszerre** *(§5.2)*, tehát **a
telephelyen mindig lesz vegyes verziójú állapot.** A szervernek **az előző fő
verziót is ki kell szolgálnia** a kiadási ablak alatt.

## 4. `[DÖNTÉS]` Hitelesítés — két réteg

| Réteg | Ki | Hogyan |
|-------|-----|--------|
| **Eszköz** | a gép | **hardveres ujjlenyomat + forgó hitelesítő adat**. Regisztráció nélkül nincs bizonylat *(§8.2)* |
| **Felhasználó** | az ember | A kérésben utazó felhasználói azonosság (PIN/RFID belépés után) |

**Miért két réteg:** a **bizonylat az eszközhöz** kötődik (számozási tartomány,
adóügyi eszköz), a **felelősség az emberhez** (audit). A kettő nem ugyanaz, és
összemosni azt jelentené, hogy egy műszakváltás után nem tudjuk, ki mit tett.

**Két ujjlenyomat egy eszközazonosítón → MINDKETTŐ tiltva**, amíg ember fel nem
oldja *(§8.2)*.

## 5. `[DÖNTÉS]` A cím SOHA nem ég a kliensbe

A felhő (`api.siduri.mythsystem.com`) és a Hermes címe **konfigurációból jön,
távolról frissíthetően**; a beépített alapértelmezés **csak visszaesés**.
*(§0.3.3 — közvetlenül a mostani domainköltözés tanulsága.)*

A **telephelyi** szervert a kliens **mDNS-sel** találja meg *(§5.3)*.

## 6. `[DÖNTÉS]` Idempotencia — nem opció

> **Minden módosító hívás idempotencia-kulcsot hordoz, és a kulcs a kliens által
> kiosztott `uuid` v7.**

**Miért kötelező:** az outbox **visszajátszik**. Degradált módból visszatérve
ugyanaz az esemény **többször is megérkezhet** — hálózati újrapróbálkozásból,
kettős szinkronból, vagy azért, mert a kliens nem kapta meg a nyugtázást.

**Idempotencia nélkül a degradált mód duplikált bizonylatokat gyárt** — pontosan
azt a kárt, ami ellen az egész árva-tranzakció kezelés épült.

**Szabály:** a szerver az ismert kulcsra **ugyanazt a választ adja vissza**, nem
hibát és nem új rekordot.

## 7. Az outbox-visszajátszás szerződése

A visszajátszó végpont **köteg**et fogad, és minden elem hordozza:

| Mező | Miért |
|------|-------|
| `id` (uuid v7) | idempotencia-kulcs |
| `sorszam` (epoch, számláló) | **az eredeti sorrend**, nem az érkezési |
| `eszkoz_ido` | az eredeti keletkezés ideje |
| `tartalom_hash` | sértetlenség-ellenőrzés |

**A szerver a sorrendet a `sorszam` szerint dolgozza fel, nem az érkezés
szerint** — különben a visszajátszás összekeverné a történetet.

## 8. Hibakezelés

| # | Szabály |
|---|---------|
| a | **Néma kudarc nincs** *(I29)*. Minden hiba **gépi kóddal** és **embernek szóló szöveggel** tér vissza |
| b | A hibakód **stabil és katalogizált** — a felület fordítja, nem a szerver szövegét mutatja |
| c | **Elkülönítve: „nem sikerült" vs. „nem tudom, sikerült-e".** A második a veszélyes eset (nyomtatás, kártyás fizetés), és **soha nem kezelhető úgy, mint az első** |
| d | A **validációs hibák mezőszinten** térnek vissza, hogy a felület oda tudja tenni, ahol keletkeztek |

## 9. `[SZABÁLY]` Amit az API SOHA nem tesz

| # | Tilalom |
|---|---------|
| 1 | **Nem küld lebegőpontos számot pénzként.** JSON-ban is egész szám, nem `1500.0` |
| 2 | **Nem ad vissza árat a termékről a bizonylathoz** — a bizonylat a saját másolatát hordozza |
| 3 | **Nem enged áfakulcsot az öt engedélyezetten kívül** *(I6)* |
| 4 | **Nem enged menüt egyetlen tételként** *(I8)* |
| 5 | **Nem enged törlést auditrekordon** *(I24–I25)* |
| 6 | **Nem fogad el bizonylatot regisztrálatlan eszköztől** |
| 7 | **Nem ad vissza más telephely adatát** — sorszintű szűréssel kikényszerítve |
