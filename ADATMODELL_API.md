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

## 9. `[TÉVES RIASZTÁS — de két valós lelettel]` Az „eCassa" megjegyzés

**A felvetésem alaptalan volt.** Az „eCassa" itt az **e-pénztárgép** szinonimájaként
szerepelt, nem márkanévként. **Az első ügyfélnél Prior Cash Fiscat eszközök
vannak: `iPalm` és `Neon+` pénztárgépek, plusz adóügyi nyomtatók.**

> **A Fiscat / Prior Cash felkészülésünk tehát HELYES**, a K1 kapu a jó gyártó
> felé mutat, és a kapott gyűjtőkiosztás erre az eszközcsaládra vonatkozik.

*(A szakasz nem törölve, hanem helyesbítve — a téves riasztás is a történet része.)*

**A válaszban viszont két olyan tény szerepelt, ami VALÓDI tervezési
következménnyel jár.**

### 9.1 `[ÚJ]` Kétféle adóügyi eszköz ugyanazon a telephelyen

**Pénztárgép** (`iPalm`, `Neon+`) **és adóügyi nyomtató** — és a kettő **nem
ugyanúgy viselkedik**:

| | **Adóügyi nyomtató** | **Pénztárgép** |
|---|---|---|
| Saját kezelőfelület | nincs | **van** (billentyűzet, kijelző) |
| Önállóan üzemeltethető | nem | **IGEN** |
| A POS vezérli | mindig | általában |

> ⚠️ **Ebből következik egy kockázat, ami eddig sehol nem szerepelt: a
> pénztárgépen VALAKI ÜTHET SIDURIN KÍVÜL.**
>
> Ha a személyzet közvetlenül a pénztárgépen ad ki egy nyugtát, az **adóügyi
> bizonylat létrejön, de a Siduriban nincs róla nyom.** A készlet nem fogy, az
> NTAK-ba nem megy be, a riport hazudik — és **nem hibából, hanem mert az eszköz
> ezt fizikailag megengedi.**

**Ellenszer — és ez olcsó, mert a protokoll amúgy is kell:**

| # | Megoldás |
|---|----------|
| a | **Napnyitáskor és napzáráskor kiolvassuk az eszköz saját számlálóit** (forgalom, bizonylatszám), és **összevetjük a sajátunkkal** |
| b | **Eltérés esetén hangos jelzés** — nem csendes elnyelés *(A2 elv)*, és auditbejegyzés a biztonsági ágon |
| c | **Ez nem vád, hanem tény:** az eltérésnek lehet ártatlan oka (próbanyomtatás, szerviz). A rendszer **jelez, nem következtet** |
| d | Az adóügyi nyomtatónál ez a kockázat **nem áll fenn** — ott nincs mit ütni |

**Ez egyben ingyen adja a vakzárás (§9.2) egyik hiányzó darabját is:** ha a nap
végén a gép saját számlálója és a miénk eltér, az önmagában jelzés.

### 9.2 `[ÚJ — SCOPE-VÁLTOZÁS]` Az e-pénztárgép nem `v2`, hanem tervezett ügyféligény

Az ügyfél **apránként át akar állni e-pénztárgépre.**

**Két következménye van, és a második a fontosabb:**

| # | Következmény |
|---|--------------|
| a | **A 3. fiskális üzemmód** (e-pénztárgép, 8/2025. (III. 31.) NGM) **nem „későbbi irány", hanem ismert, tervezett igény.** A `v2` címke marad, de **a szerkezetnek az első naptól bírnia kell** |
| b | ⚠️ **„Apránként" = VEGYES ESZKÖZPARK.** Ugyanazon a telephelyen, **ugyanabban az időben** lesz online pénztárgép (AEE) **és** e-pénztárgép |

> **A fiskális üzemmód tehát ESZKÖZ-szintű tulajdonság, nem telephely-szintű.**
>
> A specifikáció eddig a három üzemmódot **telephely-szintű** fogalomként
> kezelte *(§10.1)*. **Ez hibás** — javítandó.

**Amit ez konkrétan megkövetel:**

| # | Követelmény |
|---|-------------|
| 9.2.1 | Az **eszköz** hordozza a fiskális üzemmódját, nem a telephely |
| 9.2.2 | **A bizonylat rögzíti, MELYIK üzemmódban keletkezett** — mert az „adóügyi szám" mező **más jelentésű** módonként: AEE-nél `Axxxxxxxxx/yyyy/zzzzz` papíron, e-pénztárgépnél **e-nyugta a Nyugtatárban**. A nullázható mező *(I14)* ezt szerkezetileg bírja, de a **jelentést tárolni kell** |
| 9.2.3 | **A fiskális adapter réteg üzemmódonként külön megvalósítás**, közös felület mögött — nem egyetlen elágazásokkal teli osztály |
| 9.2.4 | Az **átállás eszközönként történik**, nem telephelyenként — a beállítás és a migráció is így nézzen ki |
| 9.2.5 | **A napi zárás és a riportok vegyes eszközparkot is helyesen kell összesítsenek** |

**Ez jó hír abban az értelemben, hogy MOST derül ki**, amikor az adaptert még
meg sem írtuk. Ha az F3 után derülne ki, az adapter-réteg átírása lenne.

