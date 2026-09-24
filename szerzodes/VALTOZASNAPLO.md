# Szerződés-változásnapló

**Minden szerződésváltozás ide kerül, a kiadás előtt.** Nem utólagos
összefoglaló: ez az a hely, ahol a **szerződésgazda** jóváhagyása megjelenik.

**Formátum:** szerződés · verzió · dátum · a változás · **törő-e**.

---

## `kassza` (K1)

### v1.0.0 — 2026-08-25 — *első kiadás*

Az F1 fázis bizonyító szelete: egy termék → kosár → készpénzes fizetés →
nyomtatás valódi adóügyi eszközre.

**Végpontok:** termékek lekérdezése (változás-jelzővel), rendelés nyitása,
tétel felvétele, rendelés lezárása, adóügyi eredmény jelentése.

**Amit szerkezetileg rögzít, mert utólag nem tehető bele:**

| Mi | Miért az első kiadásban |
|----|------------------------|
| `Siduri-Epoch` fejléc minden íráson | A HA az F6-ban épül, de egy protokollmező felvétele később **minden kliens minden verzióját** érinti |
| `Idempotencia-Kulcs` minden íráson | A degradált módból való visszajátszás **definíció szerint ismétel** |
| `(epoch, szamlalo)` sorrend minden rekordon | A sorrendet nem a fali óra adja |
| Eszközönként elhatárolt bizonylatszám | Az ütközés így **szerkezetileg lehetetlen** |
| Külön, nullázható adóügyi bizonylatszám | Nem minden bizonylathoz tartozik, és soha nem a Siduri szám helyett áll |
| Összeg egész forint; egységköltség, mennyiség, árfolyam **szövegként** | Az I1 invariáns a protokollon is érvényes, vagy sehol |

**Kimondott hiányok, nem elfeledett részek:**

| Hiány | Mikor pótoljuk |
|-------|----------------|
| **Eszközregisztráció és kezelői bejelentkezés** — a szelet már hitelesített állapotból indul | **F2** |
| **Leküldő eseménycsatorna** (KDS, rendeléskijelző, asztaltérkép) | **F1-ben eldöntendő** *(SZERZODES §7, S1)* |
| **Az eszköz azonosságának mechanizmusa** — a kölcsönös TLS a javaslat, a döntés nyitva | *(SZERZODES S5)* |

---

## `admin` (K2)

A K2-nek **két megvalósítása lesz** — a felhő és a telephelyi szerver —, és a
szerződésteszt mindkettőn ugyanaz fut. Ez teszi a §22.2 ígéretét gépi kényszerré.

### v1.13.0 — 2026-09-24 — *új bérlő, új telephely, telepítési jegy* `NEM TÖRŐ`

* **`POST /siduri/berlok`** — új bérlő, egy lépésben az első telephellyel és a
  **tulajdonosi** Ziggurat-fiókkal (a bérlői katalógus minden joga + abszolút
  jogosultságkezelés), meghívóval.
* **`GET/POST /siduri/berlok/{id}/telephelyek`** — a telephelyek (regisztrált-e,
  van-e élő jegy) és új telephely felvétele.
* **`POST /siduri/telephelyek/{id}/jegy`** — telepítési jegy: **24 óra**, egyszer
  használható, telephelyenként **legfeljebb egy él** (az új a régit
  érvényteleníti). **Csak a válaszban látszik**, levélben nem megy ki.
* Új kapcsoló: **`TELEPITESI_JEGY`**.

**Törő-e:** nem. Új végpontok, új felsorolás-érték (a felület az ismeretlen
kapcsolót figyelmen kívül hagyja).

### v1.12.0 — 2026-09-24 — *a termék neve és állapota szerkeszthető* `NEM TÖRŐ`

* **`PUT /termekek/{id}/megnevezes`** (jog: `termek.modositas`) és **`PUT
  /termekek/{id}/allapot`** (jog: `termek.inaktivalas`). Mezőnként külön, mint
  az ár: a vesztes írás tiszta 409 (`KESOBBI_ERTEK_ALL`), nem félsiker.
* A **`Termek`** új mezői: `megnevezesEredet/Elozo/Elveszett` és
  `allapotEredet/Elozo/Elveszett` — a szabály (O3) ugyanaz, mint az árnál, és a
  felület ugyanúgy köteles megmutatni, mi nem lépett érvénybe.
* A TOROLT (soft delete) állapotot az új végpont nem állítja és nem oldja fel
  (`TOROLT_TERMEK`, 409).

**Törő-e:** nem. Új végpontok és új, nem kötelező mezők.

### v1.11.0 — 2026-09-24 — *a kollégák kezelése, négy szem* `NEM TÖRŐ`

* **`/siduri/kollegak`** (lista, felvétel meghívóval), **`PATCH`** (letiltás,
  egyedi kapcsolók, jogkörök), **`/rang`** (Manager adása/elvétele),
  **`/meghivo`**.
* **`/siduri/jogkorok`** — a jogkör **élő**: az átírása azonnal hat minden
  viselőjére; a válasz megmondja, hány emberre (`viselok`).
* **`/siduri/kerelmek`** — a négy szem elv: egy Manager letiltása vagy
  rangjának elvétele egy másik Manager által **függő kérelem (202)**, amit egy
  **harmadik** Manager hagy jóvá. Kettőnél kevesebb Manager nem maradhat
  (`NEGY_SZEM`, 409) — ezt csak Szuperadmin teheti meg.
* A napló bejegyzésének új mezője: **`reszlet`**.

⚠️ **A burok itt is:** csak olyan kapcsolót adhat vagy vehet el — közvetlenül
vagy jogkörrel —, amivel maga is rendelkezik. A Szuperadmin rang a felületről
sosem adható és sosem vehető el.

**Törő-e:** nem. Új végpontok és egy új, nem kötelező mező.

### v1.10.0 — 2026-09-24 — *a Siduri kollégafiókjai* `NEM TÖRŐ`

Új címke, **`siduri`**: a belső kollégafiókok (HOZZAFERES.md §4). **Csak a
felhő valósítja meg**; a telephely 501-et ad.

* **`GET /siduri/berlok`** — a bérlőválasztó listája.
* **`PUT /siduri/munkamenet/berlo`** — belépés egy bérlő adataihoz. A
  kollégamunkamenet **bérlő nélkül indul**; amíg nem választott, a bérlői
  végpontok `NINCS_BERLO_VALASZTVA` 403-at adnak. A belépés **naplózódik**, a
  bérlő saját belépési naplójába is.
* **`GET /siduri/naplo`** — a kollégák belépései és bérlőbe lépései.
* A **`Munkamenet`** új mezője: **`kollega`** (rang, tényleges kapcsolók,
  választott bérlő). A bérlői fióknál hiányzik.

⚠️ **A bérlői adaton a kollégajog:** a Szuperadmin és a Manager mindent tehet,
minden más kolléga **csak olvas**.

**Törő-e:** nem. Új végpontok és egy új, nem kötelező válaszmező.

### v1.9.0 — 2026-09-24 — *telephelyválasztó* `NEM TÖRŐ`

A **`Munkamenet`** új mezője: **`telephelyek`** — a cég telephelyei, névvel. A
felület ebből kínál választót a fejlécben, ha egynél több van. Eddig a
telephely **a konfigurációból** jött, tehát a felhős Zigguratban egy többüzletes
bérlő csak egy üzletet látott.

⚠️ **A lista nem jogosultság:** egy telephely szerepelhet benne, és a kiszolgáló
ott mégis 403-at adhat — a jog telephelyenként áll.

**Törő-e:** nem. Új, nem kötelező válaszmező.

### v1.8.0 — 2026-09-24 — *a jogosultságok emberi neve* `NEM TÖRŐ`

Új végpont: **`GET /jogosultsagok`** — kód, terület, magyar megnevezés, és hogy
magas kockázatú-e. A felület eddig nyers kódot mutatott (`termek.ar_modositas`).

| Mi | Döntés | Miért |
|----|--------|-------|
| **Honnan jön** | egy **közös forrás** (`mag`), amit egy teszt a telephelyi adatbázis-katalógussal kódról kódra egyeztet | Egy új jog, ami csak az egyik helyre kerül be, a buildet buktatja el — nem a felület mutat csendben nyers kódot |
| **Mindkét oldal** | ugyanaz a válasz; a közös szerződésteszt követeli meg | A felhőben eddig katalógus sem volt |
| **A Siduri-kódok** | nincsenek a válaszban | A bérlőnek nincs velük dolga |
| **Ismeretlen kód** | a felület nyersen mutatja | Nem találunk ki rá nevet |

**Törő-e:** nem. Új végpont.

### v1.7.0 — 2026-09-24 — *bejelentkezés* `NEM TÖRŐ`

Eddig a Ziggurat fejlesztői kapcsolóval működött, élesben **minden kérés 401**
volt. A döntések: `siduri-docs/BEJELENTKEZES.md`.

| Mi | Döntés | Miért |
|----|--------|-------|
| **Munkamenet** | Szerveroldali, `HttpOnly` süti (`siduri_munkamenet`), **nem JWT** | Kijelentkezéskor, letiltáskor, jelszócserekor **azonnal** megszűnik — egy JWT a lejáratáig érvényes maradna, és egy letiltott dolgozó bent maradna |
| **Időkorlát** | 20 perc tétlenség, legfeljebb 12 óra | A felület visszaszámlál; a **„Maradok”** (`POST /munkamenet/frissites`) az oldal megzavarása nélkül nulláz |
| **`GET /munkamenet`** | az egyetlen hitelesített kérés, ami **nem** nulláz | Különben a visszaszámláló lekérdezése maga hosszabbítana, és a számláló hazudna |
| **Két kapu** | felhő: név + jelszó; telephely: pultos azonosító + PIN, **csak ha a felhő nem érhető el** | A gyenge PIN csak kimaradáskor nyitott; különben a telephely a felhős Zigguratra küld (`FELHORE`, `409 FELHO_ELERHETO`) |
| **Fékezés** | növekvő várakozás, `429` + `Retry-After` — **kizárás nincs** | A kizárás maga is támadás: bárki kizárhatna bárkit |
| **Meghívó, elfelejtett jelszó** | egyszer használható, lejáró jegy e-mailben; a meghívó linkje **soha** nincs a válaszban | Különben a meghívó maga állíthatná be a másik jelszavát |
| **Felhő alapcíme** | `ziggurat.mythsystem.hu` | A korábbi `admin.sidurisystems.hu` helyett |

⚠️ **A válaszok nem árulnak el semmit:** rossz név és rossz jelszó ugyanazt
kapja; az „elfelejtettem” mindig `202`; lejárt, felhasznált és nem létező jegy
ugyanazt a `410`-et.

**Törő-e:** nem. Új végpontok és egy új biztonsági séma; a `Bearer` séma
megmarad, de **csak fejlesztői kapcsolóval** él. Két indokolt lint-kivétel
került be (`.redocly.lint-ignore.yaml`).

### v1.6.0 — 2026-09-24 — *az előző és az elveszett ár* `NEM TÖRŐ`

Két új, nem kötelező mező a kiszerelésen: **`arElozo`** *(az előtte érvényes ár,
mikor és honnan)* és **`arElveszett`** *(a legutóbbi írás, ami nem lépett
érvénybe, és **miért**)*. A döntés: `siduri-docs/TORZSADAT_FELKULDES.md`.

**Miért:** az O3 szabály kikötése, hogy a vesztes érték nem tűnik el, csak nem
érvényes — és hogy a felület **mutassa meg**, mi volt előtte. Eddig a felület
csak azt tudta, mikor és honnan jött a mostani érték.

⚠️ **Az `ok` három érték, és nem vonható össze:** `KESOBBI_ERTEK` *(valaki később
átírta — sorrend)*, `ELUTASITVA` *(az írónak nem volt joga — a felhő utasította
el)*, `ZAROLT` *(a központ zárolta — hatáskör)*. Egy közös „elveszett” azt
sugallná, hogy hiba történt.

**Törő-e:** nem. ÁRA: mindkét oldalon **írás-történet** kellett (`mezo_iras`,
csak beszúrható), és a múlt nincs meg — a mezők a bevezetés napjától telnek.

### v1.3.0 — 2026-09-22 — *a hibaválasz is megmondja, melyik oldal felelt* `NEM TÖRŐ`

A `Siduri-Szerzodes` és a `Siduri-Kiszolgalo` fejléc eddig csak a **sikeres**
válaszokon volt előírva. Mostantól a **hibaválaszokon is** (401, 403, 404, 422
és az általános hiba).

⚠️ **Ez a 403-nál nem kényelmi kérdés.** A két megvalósítás **külön
hozzáférés-nyilvántartásból** dolgozik *(2026-09-22 döntés)*, tehát ugyanaz a
felhasználó az egyik oldalon jogosult lehet, a másikon nem. A böngészőben a két
kiszolgálás **ugyanúgy néz ki** — a kiszolgáló megnevezése nélkül egy „nekem
ehhez van jogom" bejelentés megfejthetetlen.

A 403 leírása ezen kívül **kimondja a két gépi kód különbségét**:
`NINCS_JOGOSULTSAG` *(a felhasználónak kell jogot kapnia)* és `MASIK_TELEPHELY`
*(beállítási hiba — ezen semmilyen jogosultság nem segít)*. A kettő összevonása a
második esetben a **rossz helyre** küldi a keresést.

**Amit ez a kiadás javított még:** a `Siduri-Szerzodes` példája `admin/1.0.0`-n
állt, két kiadással a valóság mögött.

**Törő-e:** nem. Új válaszfejléc hozzáadása — a régi kliensek figyelmen kívül
hagyják. ÁRA: a **telephelyi** oldal eddig nem küldte a `Siduri-Kiszolgalo`-t a
hibaválaszokon; ezt pótolni kellett, és a **közös szerződésteszt mostantól
meg is követeli** mindkét megvalósításon.

### v1.2.0 — 2026-09-19 — *a zárolás láthatóvá válik* `NEM TÖRŐ`

**Új mező** minden kiszerelésen: `arZarolas` — ha jelen van, az árat egy
**magasabb szint** (lánc/franchise központ) zárolta, és a telephelyről nem
írható át. A 403-as válasz ezt eddig is tartalmazta *(1.1.0)*; ami hiányzott, az
a **read oldal**.

**Miért nem elég a 403:** a felület enélkül csak annyit tudna, hogy az írás
elbukott. A menedzser újra és újra próbálkozna, és azt hinné, elromlott a
rendszer. **„Ár: 1200 Ft — a központ állította be, zárolva"** — ez a különbség
(`NYITOTT_KERDESEK.md` **B16.3**).

**Amit a szerződés szövege is kimond:** a zárolás **nem ütközés, hanem
hatáskör** — időbélyegtől függetlenül nyer, tehát az O3 időbélyeg-szabálya
**nem alkalmazható rá**.

### v1.1.0 — 2026-09-19 — *az első írás: a kiszerelés ára* `NEM TÖRŐ`

**Új végpont:** `PUT /termekek/{id}/kiszerelesek/{id}/ar`. **Új mező** minden
kiszerelésen: `arEredet` — *mikor* és *melyik oldalról* (felhő/telephely) kapta
az árat. Additív változás, a meglévő olvasó hívókat nem töri.

**Amit a szerződés szövege is hordoz** (`NYITOTT_KERDESEK.md` **O3**):

| Mi | Miért így |
|----|-----------|
| **Mezőeredet minden írható mezőn** | Az ütközést mezőnkénti időbélyeg oldja fel, a későbbi írás nyer. Enélkül a felület nem tudná megmutatni, hogy egy változtatás **már nem érvényes** |
| **`PUT`, nem `PATCH`, és nincs idempotencia-kulcs** | A kérés a **teljes új értéket** adja meg, tehát a megismétlése ugyanoda vezet. Összeadódó műveletnél („emeld 10%-kal") ez nem állna, és ott kulcs kellene |
| **A nulla érvényes, a negatív nem** | Ingyenes tétel létezik; **az ár nem sztornó** |
| **A zárolt érték 403** | A lánc-zárolás **nem ütközés, hanem hatáskör** — időbélyegtől függetlenül nyer (B16.3) |
| **A vesztes írás 409, nem csendes 200** | A felhasználó beírt egy árat, és az nem lett érvényes. Sikeres válasszal azt hinné, megtörtént — és a következő számlán szembesülne az ellenkezőjével. *(A kiadás napján, még a megvalósítás előtt egészült ki ezzel; fogyasztó addig nem épült rá.)* |

**A megtartott kockázat, kimondva:** a sorrendet **két gép fali órája** dönti el.
Ha a telephelyi gép órája siet, egy korábbi helyi írás legyőzhet egy későbbi
felhőset. A vesztes érték az **audit-láncban** marad, tehát látható — de a
felülírás automatikus.

### v1.0.0 — 2026-09-19 — *első kiadás: csak olvasó törzsadat*

**Végpontok:** kategóriafa, termeklista (kurzoros lapozás, szűrés, keresés), egy
termék a kiszereléseivel. **Írás nincs benne.**

**Amit szerkezetileg rögzít, mert utólag nem tehető bele:**

| Mi | Miért az első kiadásban |
|----|------------------------|
| `Siduri-Telephely` fejléc **minden** kérésen | A több telephely alapmodell (§22.3). Utólag felvenni minden hívót érintene |
| `Siduri-Kiszolgalo` fejléc **minden** válaszban (`felho` / `telephely`) | Két megvalósítás van, és a böngészőben ugyanaz az alkalmazás látszik. Enélkül egy „nem látom a tegnapi változtatásomat” bejelentésnél senki nem tudja, hol kezdje |
| **Kurzoros** lapozás, nem eltolás-alapú | Eltolással a beszúrás közbeni lapozás sorokat ismétel vagy ejt — és ezt a felhasználó nem jelenti be, mert észre sem veszi |
| `osszesen` a listaválaszban | Az export a **teljes szűrt eredményt** adja majd, és ezt a felületnek előre ki kell írnia (`EXPORT_IMPORT.md` §2.2) |
| Bruttó ár **egész forint**, áfakulcs **másolat**, nem hivatkozás | Az I1 invariáns a protokollon is érvényes; a hivatkozott áfakulcs csendes jogsértést okozna |

**Kimondott hiányok, nem elfeledett részek:**

| Hiány | Miért nincs benne |
|-------|-------------------|
| **Bejelentkezés és munkamenet** — a szelet hitelesített állapotból indul | A K2 későbbi szelete |
| **Írás** (ár, láthatóság, termék) | Előbb a `WEBADMIN_STACK.md` **W3** kérdését kell eldönteni: offline telephely mellett melyik az igazság forrása |
| **Export és import** — egyetlen közös szolgáltatásként minden listás nézethez | A könyvtárválasztás nyitott: az Apache POI és a GraalVM natív fordítás ütközik (`EXPORT_IMPORT.md` §6.1) |
| **Csak helyi funkciók** külön útvonalcsoportban | Még nincs ilyen végpont — **üres csoportot nem adunk ki** |

---

## `szinkron` (K3)

A **legszigorúbb kompatibilitási kényszerű** szerződés: a felhő és a telephely
soha nem frissül egyszerre. Legalább **két kiadási ciklusnyi** visszafelé
kompatibilitás.

### v1.6.0 — 2026-09-24 — *a név és az állapot mezőeredetet kap* `NEM TÖRŐ`

* A `MEZO_ERTEK` (le és fel) új táblája a **`termek`**, új mezői a
  **`megnevezes`** és az **`allapot`**, az értékük a **`szovegErtek`**-ben.
* A REKORD `termek` része új mezőt kap: **`mezoeredetek`** (a név és az
  állapot eredete). A felhő mezőnként dönt: csak a későbbi értéket veszi át.

⚠️ **A „telephely nyer" szabály e két mezőre megszűnt** — a felhő is írhatja
őket (TORZSADAT_FELKULDES §3.2 ígérete szerint: a mezőeredettel együtt).
Ahol nincs eredet (a bevezetés előtti adat), ott a régi szabály él tovább.

**Törő-e:** nem. Ismeretlen táblát/mezőt a régebbi telephely `ELUTASITVA`
nyugtáz — a felhő ebből tudja, hogy még nem alkalmazta.

### v1.5.0 — 2026-09-24 — *beszerzési ár, NTAK-kódok, mennyiség* `NEM TÖRŐ`

A `REKORD` tétel eddig nem hozta fel a termék **beszerzési árát és áfáját**, az
**NTAK-kódokat**, és a kiszerelés **mennyiségét**. A felhő a riportok és a
8 éves archívum helye — az árrés- és food cost-riport enélkül nem építhető.

A mennyiség **szövegként** utazik, mint a K1-ben: lebegőpontos érték a
mennyiség közelében sincs.

**Törő-e:** nem. Új, nem kötelező mezők. ⚠️ Egy régebbi telephely nem küldi
őket; a felhő ilyenkor üresen hagyja — a telephely frissítése után a következő
módosítással töltődnek fel.

### v1.4.0 — 2026-09-24 — *a telephelyi törzsadat felmegy a felhőbe* `NEM TÖRŐ`

**Eddig a telephelyen átírt törzsadat soha nem jutott fel.** A felhős Ziggurat
ezért csendben a régi árat mutatta, és a felhőbe **semmi** nem írt törzsadatot
— még a kezdeti katalógus sem jutott fel. A teljes döntés:
`siduri-docs/TORZSADAT_FELKULDES.md`.

| Mi | Döntés | Miért |
|----|--------|-------|
| **Hol megy fel** | A **`/lekerdezes`** kérésében (`felkuldes`), a kimenet a válaszban (`felkuldesElbiralasok`) | Ugyanaz a kör, mint a hozzáférésnél: a felhő döntése — például egy visszaállító érték — **ugyanabban a válaszban** lejöhet |
| **Két tételfajta** | `REKORD` *(teljes sor)* és `MEZO_ERTEK` *(egy mező)* | Egy új rekordnál nincs mit mezőnként összevetni. A **kezdeti feltöltés csupa `REKORD`**, ugyanazon az úton — nincs második formátum |
| **Időbélyeg nélküli mezők** | A **telephely nyer** | Ma ő az egyetlen írójuk. Ha a felhő is írhatja őket, azzal együtt kapnak mezőeredetet |
| **Az ár** | A mezőeredet szabálya, a `REKORD`-ban is | A későbbi írás nyer, a zárolt mindig nyer — ugyanaz, mint lefelé |
| **Az író joga** | A felhő **az írás idejére** nézve ellenőrzi | Mint a hozzáférésnél: késleltetéssel jogot szerezni nem lehet |
| **Kimenet** | **NÉGY**: `ELFOGADVA`, `ELUTASITVA`, `ELAVULT`, `ZAROLT` | A három nem-elfogadó **nem ugyanaz**: a cselekvőről, a sorrendről, illetve a hatáskörről szól |

⚠️ **Nincs visszhang.** Egy elfogadott telephelyi írásból a felhő **nem**
készít lefelé menő változást ugyanannak a telephelynek — az azonos időbélyeg
miatt a telephely a saját értékét vesztesnek látná.

⚠️ **Ami nem kap kimenetet, az nincs elbírálva**, nem elutasítva. A telephely
megtartja és újra küldi; az azonosító miatt a felhő egy már elbírált tételt nem
bírál el kétszer.

**Törő-e:** nem. Új, nem kötelező kérés- és válaszmező. Egy **régebbi felhő**
a `felkuldes` mezőt figyelmen kívül hagyja, és nem ad rá kimenetet — a tételek
ettől a telephely sorában maradnak, tehát **nem vesznek el**, csak várnak.

### v1.3.0 — 2026-09-23 — *a telephely kerdez: offline valtoztatasok elbiralasa* `NEM TÖRŐ`

**Ez az első hely, ahol a telephely kérdez valamit, amire a felhő nemet is
mondhat.** A K3 lefelé menő iránya **parancs**; a kapcsolat nélkül tett
hozzáférés-változtatás viszont **kérés**.

| Mi | Döntés | Miért |
|----|--------|-------|
| **Hol megy fel** | A **meglévő `/hozzaferes` körben**, nem külön úton | Így az elfogadott változtatás **már benne van** a visszakapott pillanatképben. Külön úton a telephely egy olyan állapotot alkalmazna, ami a saját, iménti változtatását még nem tartalmazza — és az a pillanatra **visszaállna** |
| **`tortent`** | **Amikor megtörtént**, nem amikor felkerült | A felhő **ehhez** az időponthoz méri, hogy a cselekvőnek volt-e joga. A két időpont különbsége napokban mérhető — és épp ez a szelet lényege |
| **`ertekek`** | A hatókör **teljes** kívánt halmaza, nem növekmény | A részleges alkalmazás olyan állapotot állítana elő, amit **soha senki nem akart** — sem a pultfőnök, sem a központ |
| **`eredmeny`** | **HÁROM érték**: `ELFOGADVA`, `ELUTASITVA`, `ELAVULT` | Az utolsó kettő **nem ugyanaz**: az egyik a cselekvőről szól *(nem volt joga)*, a másik senkiről, csak sorrendről |
| **`telephelyDarab`** | **Minden körben lejön** | A pultnak **kapcsolat nélkül is** tudnia kell, együzletes-e a bérlő — különben a globális menüpont offline vagy eltűnne, vagy egy hasznavehetetlen oldalra vinne |

⚠️ **Az elbírálás akkor is lejön, ha a pillanatkép változatlan.** Hogy
változott-e a tartalom, és hogy mi lett a felküldött változtatás sorsa, **két
külön kérdés** — egy elutasítás tipikusan épp **nem változtat semmin**, és épp azt
kell megtudnia a telephelynek.

### v1.2.0 — 2026-09-23 — *a pultos hozzáférés — PILLANATKÉPKÉNT* `NEM TÖRŐ`

**Egy új végpont:** `POST /hozzaferes`. A telephely lekéri a saját pultos
felhasználóit és a jogaikat.

⚠️ **SZÁNDÉKOSAN NEM VÁLTOZÁSFOLYAM**, pedig a K3 többi része az. Három okból:

| # | Ok |
|---|---|
| 1 | **Nincs összefésülés, tehát nincs mit elrontani.** Egy elmaradt vagy rosszul sorrendezett növekmény azt jelentené, hogy egy **visszavont jog megmarad**. A törzsadatnál ez ár-hiba; itt **biztonsági hiba** |
| 2 | **A megvonás mindig nyer** — ez a pillanatképből ingyen jön. A mezőnkénti időbélyeg (`O3`) itt **nem érvényes**: két gép fali órája dönthet arról, melyik ár nyer, de arról nem, ki mit láthat |
| 3 | **Kicsi.** Néhány tucat felhasználó és szerep; a teljes halmaz átvitele olcsóbb, mint a növekményes gépezet |

**A telephely elküldi, milyen verziót ismer** *(a tartalom lenyomatát)*; ha az
egyezik, a válasz `valtozott: false`, és nem visszünk át semmit.

⚠️ **A PIN SOHA NEM SZEREPEL BENNE.** A felhő a **személyt** és a **jogait**
tartja nyilván; a hitelesítés helyi marad. Egy interneten áthaladó PIN-nek nem
lenne mit keresnie ebben a rendszerben.

⚠️ **A SZEREPEK JOGAI MÁR KIBONTVA ÉRKEZNEK** — a szint szerinti örökléssel
együtt. A kibontást a **felhő** végzi, egy helyen: különben a két oldal ugyanazt
a szabályt számolná külön, és az eltérés **csendes** lenne — mindkettő
„működik”, csak mást enged.

### v1.1.0 — 2026-09-21 — *a kölcsönös TLS megvalósul: regisztrációs végpont* `NEM TÖRŐ`

**Egy új végpont:** `POST /regisztracio` — egyszer használható, lejáró **jeggyel**
kér tanúsítványt a telephely. Ez az **egyetlen** végpont kölcsönös TLS nélkül, és
nem kivétel a szabály alól, hanem a tyúk-tojás feloldása: a telephelynek még
nincs tanúsítványa, éppen itt kapja meg.

| Mi | Döntés | Ára |
|----|--------|-----|
| **Ki hitelesít** | **Saját hitelesítő (CA)**, és a felhő **ujjlenyomat-nyilvántartásból** oldja fel a telephelyet | A CA magánkulcsának őrzése a mi felelősségünk; aki megszerzi, tetszőleges telephelynek adhat ki tanúsítványt |
| **Visszavonás** | **A nyilvántartásban**, egy sor megjelölésével — azonnal hat | Ha a felhő adatbázisa nem elérhető, **egyetlen telephely sem tud szinkronizálni**. Vállalt: egy visszavonási lista (CRL/OCSP) frissessége offline telephely mellett amúgy sem garantálható |
| **Az azonosság forrása** | **A tanúsítvány, nem a kérés teste.** Ha a kettő eltér: **403** | A `telephely` mező a testben marad, de már csak **ellenőrzésre** szolgál |
| **Kiosztás** | **Automatikus regisztráció**: a kulcspár a telephelyen születik, csak a PKCS#10 kérés megy fel | A jegy átadása emberi fegyelem: a jegy **nem bizonyítja**, hogy a jogos telepítő áll a vonal másik végén — csak azt, hogy nála van |
| **Hol fut** | **Egy port (443), két állomásnév**: `admin.*` nyilvános hitelesítővel, kliens-tanúsítvány nélkül; `szinkron.*` a saját hitelesítőnkkel | A böngésző soha nem kap tanúsítvány-választó ablakot, és a telephelynek nem kell a 443-tól eltérő kimenő port — szigorú céges tűzfal mögött ez döntő. Cserébe kézzel írt Tomcat-konfiguráció, és egy elé kerülő fordított proxynak **át kell engednie** a TLS-t |

⚠️ **Amit a kölcsönös TLS NEM old meg:** egy TLS-t felbontó céges tűzfal
(SSL-inspection) mögött a kapcsolat **eltörik** — a proxy nem tudja felmutatni a
telephely kliens-tanúsítványát. Ilyen helyen kivételt kell kérni a
szinkron-állomásnévre. Ez a **telepítési ellenőrzőlistára** tartozik.

⚠️ **És amit a csatorna hitelesítése önmagában sem old meg:** aki a felhőt vagy a
kulcsot megszerzi, tetszőleges parancsot küldhet. Ezért marad a `alairas` mező a
szerződésben — a bekapcsolása külön szelet, kulcskezeléssel.

### v1.0.0 — 2026-09-21 — *első kiadás: lefelé törzsadat és zárolás, felfelé nyugta*

**Két végpont:** `POST /lekerdezes` *(változások + szívverés + óraállás)* és
`POST /nyugta`.

**A döntések, amiket ez a kiadás rögzít:**

| Mi | Döntés | Miért így |
|----|--------|-----------|
| **Ki kezdeményez** | **A telephely húz, időzítve, alkalmazkodó ütemmel** | A telephelyen nem kell bejövő portot nyitni. Az ütemet a **felhő** mondja meg (`kovetkezoLekerdezesMp`): amíg van több változás, **nulla** — így egy csomóban érkező szerkesztés másodpercek alatt leér, **nyitva tartott kapcsolat nélkül** |
| **A tömeges átvitel** (`S3`) | **Ugyanaz a végpont, lapozva** | Kurzor nélkül kérdezni = teljes újraszinkron. **Nincs második formátum**, mert egy ritkán futó kódút évekig észrevétlenül romolhatna el |
| **Nagy hatókörű árművelet** (`B16.8/5`) | **Késleltetett élesítés** (`ervenyesTol`) | Egy feltört felhő-fiók így nem tud egy pillanat alatt kinullázni egy franchise-t — marad idő észrevenni |
| **Hitelesítés** | **Kölcsönös TLS most; `alairas` mező már a szerződésben** | A bekapcsolása később **nem törő változás** — ebben a szerződésben az a legdrágább fajta |
| **Ismeretlen típus** | **`ELUTASITVA` + `ISMERETLEN_TIPUS`** | Nem áll le, és nem is hallgat: a felhő megtudja, hogy a telephely régebbi |
| **Nyugta** | **Három állapot**: `ATVETTE` / `ALKALMAZTA` / `ELUTASITVA` | Enélkül a felhő elvégzettnek mutatná azt, ami nem történt meg (`B16.5`) |

**Az óraállás nem kényelmi adat:** a törzsadat-ütközést mezőnkénti időbélyeg
oldja fel (`O3`), és a sorrendet **két gép fali órája** dönti el. A telephely
minden lekérdezésnél jelenti az óraállását, a felhő pedig visszaadja az eltérést
(`oraElteresMp`) — enélkül a feloldás **vakon futna**.

**Ami nincs benne, kimondva:** az eladási adatok felküldése (8 éves archívum), a
mennyiségi állapot (az kizárólag telephely-autoritatív, `B16.4`), és a
megvalósítás — ez egyelőre **csak szerződés**.

### v1.1.0 — 2026-08-26 — *eseménycsatorna borítéka* `NEM TÖRŐ`

**Új fájl:** `kassza/v1/esemenyek.yaml` — a leküldő eseménycsatorna üzenetalakjai.

**Miért most, amikor a csatorna csak az F5-ben épül meg:** ugyanaz az ok, amiért
az epoch mező az első naptól benne van a kérésekben. **Egy protokollmező
utólagos felvétele minden kliens minden verzióját érinti** — most ingyen van,
egy év múlva átállási terv.

| Mit rögzít | Miért |
|-----------|-------|
| Az esemény sorszáma **ugyanaz a `(epoch, számláló)` pár** | Nem új mechanizmus. A régebbi generációjú esemény azonnal felismerhető, és szerepváltás után nem kell külön „ürítsd a gyorsítótárat" üzenet |
| **Újracsatlakozás: `POTLAS` vagy `UJRATOLTES`** | Az `UJRATOLTES` nem hibajelzés. ⚠️ Csendben folytatni tilos: a kliens azt hinné, naprakész, holott lyuk van a történetében |
| **Szívverés, és 5 másodperces elavulási küszöb** | Egy TCP-kapcsolat percekig „nyitva" maradhat egy halott szerver felé |

**Nem törő változás:** új fájl, meglévő alak nem módosult.

### v1.2.0 — 2026-09-01 — *kiszerelés és teljesítési mód* ⚠️ `KIADÁS ELŐTTI MÓDOSÍTÁS`

> ⚠️ **Ez a változás TÖRŐ lenne, ha a `v1` már be lenne fagyva.** Nincs — még
> egyetlen kliens sem fordult rá élesben *(§4.2/b)*. **Ez az utolsó pillanat,
> amikor ilyet szabad**; az első éles telepítés napjától a §4.1 táblázata
> kivétel nélkül érvényes.

**Mi változott, és miért:**

| Változás | Miért |
|----------|-------|
| `ErtekesithetoTetel.bruttoEgysegar` → **`bruttoAr`** | Az értékesíthető egység mostantól a **kiszerelés**, nem a termék. A 0,5 l és a 0,3 l csapolt sör két külön egység, saját árral és vonalkóddal — de egy termék gyermekei. **Az ár a kiszerelésen él**; ha a terméken is ott maradna, két igazságforrás keletkezne, és előbb-utóbb eltérnének |
| `afaKategoria` → **`afaHelyben` + `afaElvitel`** | Két áfamező, **másolat-szemantikával**. Ha hivatkozás lenne, a helyben fogyasztás kulcsának csökkentése csendben lecsökkentené az elviteli áfát is — ami jogsértés. **A két hibairány nem egyenértékű:** a túl magas áfa pénzügyi hátrány, a túl alacsony jogsértés |
| **Új: `TeljesitesMod`** a rendelésnyitásban | E nélkül a második áfamező holt súly: nincs, ami eldöntse, melyiket kell használni. A **kiszállítás az elviteli** mezőt használja — áfakulcsot soha nem égetünk a kódba |
| `tetelAzonosito` **jelentése** pontosítva | Mostantól a kiszerelés azonosítója. Az alak nem változott, a jelentés igen — **és ez az a fajta változás, ami kiadás után szigorúan tilos**, mert a fordító nem veszi észre |

**Ami NEM változott:** nincs külön elviteli **bruttó** ár. Ha a hamburger 1500 és
elvitelre kérik, az 1500 marad; csak a kulcs más. Ebből következik, hogy **a
nettó árbevétel teljesítési módonként eltér**, tehát minden árrés-kimutatást
teljesítési módonként bontva kell számolni.

### v1.3.0 — 2026-09-01 — *kedvezmény, szervizdíj, borravaló* `NEM TÖRŐ`

**Új, mind elhagyható mező a lezárásban:** `kedvezmeny`, `szervizdijSzazalek`,
`borravalo`, `kedvezmenyIndokKod`, `kedvezmenyIndokSzoveg`, `megerositve`.
**A válaszban új:** `borravalo` és `egyebTetelek`.

| Szabály | Miért így |
|---------|-----------|
| **A kedvezmény áfakulcs-arányosan oszlik szét**, maradék nélkül | Ha nem így lenne, a különbözet nem tűnne el — **rossz gyűjtőre kerülne**, és azt az adóhatóság látja |
| **A kedvezmény és a szervizdíj ÖNÁLLÓ SOR, áfakulcsonként** | Az adóügyi gyűjtőkiosztásban a szervizdíjnak **saját, áfakulcsonkénti rekeszei** vannak. A termékbe olvasztva rossz rekeszbe kerülne |
| **A kedvezmény negatív, a szervizdíj pozitív** — adatbázis-kikötés | Ha felcserélődne, a végösszeg jó lenne, **a gyűjtők viszont nem** |
| **A borravaló nincs az áfacsoportokban** | A gyűjtőkiosztásban nincs borravaló-rekesz: a borravaló nem ellenérték egy szolgáltatásért. A végösszeg viszont tartalmazza |
| **A `megerositve` a SZÁNDÉKOT erősíti meg, nem az összeget** | Ezért külön mező, és nem az érték megismétlése |
| ⚠️ **Kemény 15%-os szervizdíj-plafon NINCS** | Nincs jogszabályi felső határ, és egy rendezvényhelyszín szerződéses szervizdíja lehet magasabb. Kemény korlát csak 100% felett, mert az bizonyosan mellényúlás |

⚠️ **Üzleti döntés, amit meg kell erősíteni:** a szervizdíj **a kedvezménnyel
csökkentett** alapra számolódik. Ez a védhető alapértelmezés — szolgáltatási
díjat azon összeg után szedni, amit a vendég ténylegesen fizet. **Ha az ügyfél
másképp akarja, az konfiguráció, és meg kell kérdezni, nem kitalálni.**

### v1.5.0 — 2026-09-23 — *pultos fiókok és a két fiók összekapcsolása* `NEM TÖRŐ`

**Három új végpont:** `GET /szerepek`, `PUT /felhasznalok/{id}/szerepek`,
`PUT /felhasznalok/{id}/kapcsolat`. A felvétel mostantól **fajtát** is kap
*(ZIGGURAT vagy PULTOS)*, és a felvett fiók **azonnal összekapcsolható** egy
másikkal.

| Mi | Döntés | Miért |
|----|--------|-------|
| **E-mail** | **Csak a ZIGGURAT-fióknál kötelező** | A pultos fiók nem a böngészőbe lép be; egy kötelező, de értelmetlen mező kitalált címekkel telne meg |
| **Szerepkör** | **Csak a pultos oldalon van** | A Ziggurat-fiókoknál felhasználónkénti jog áll — az irodista, a könyvelő és a területi vezető nem rendezhető egy sorba |
| **Kiosztás** | **KÉT korlát egyszerre**: szint és burok | A második nélkül az első megkerülhető lenne egy **azonos szintű**, de több jogot tartalmazó szereppel |
| **Sérthetetlen szerep** | **A felületről soha nem osztható** | A burok önmagában nem védené meg: egy bérlői adminisztrátor, akinek minden bérlői joga megvan, ki tudná osztani — és onnantól a saját nyilvántartásában lenne egy elvehetetlen főkulcs |
| **Kapcsolat** | **Csak ZIGGURAT és PULTOS között** | Két pultos fiók összekapcsolása nem „ugyanaz az ember", hanem elgépelés — és a csendes elfogadás később megfejthetetlen adatot hagyna |

⚠️ **A kapcsolat NEM von maga után automatikus letiltást.** Ha az egyiket
letiltják, a válasz `kapcsoltFigyelmeztetes` mezője szól róla, és a felület
**rákérdez** — mindkét irányban. A rendszer nem dönt helyettünk, de nem is hallgat.

⚠️ **AMI MA MÉG NEM TÖRTÉNIK MEG:** a pultos fiók **PIN nélkül** jön létre — azt a
pult mögött kell beállítani. A felhő a **személyt** és a **jogait** tartja nyilván;
a hitelesítés helyi marad.

### v1.4.0 — 2026-09-01 — *sztornó és a számla–nyugta kizárás* `NEM TÖRŐ`

**Új:** `BizonylatMod` (`ADOUGYI` / `SZAMLA`) a lezárásban és a válaszban,
`BizonylatTipus` (`NORMAL` / `SZTORNO`) a válaszban.

⚠️ **A kölcsönös kizárás nem kényelmi szabály.** Ha a vendég áfás számlát kap
**és** a tranzakciót a fiskális eszközön is lezárják, ugyanaz az értékesítés
**kétszer kerül be a hatóság felé** — egyszer a pénztárgép adatszolgáltatásán,
egyszer az Online Számla rendszeren. **Az eltérést az adóalanynak kell
magyaráznia.**

**Két útvonal, nem egy tiltás:**

| Útvonal | Mikor | Menete |
|---------|-------|--------|
| **A) Eleve számlás** | a vendég a fizetés ELŐTT kéri | `mod: SZAMLA` — a fiskális eszköz felé nem megy semmi; a papíron **„NEM ADÓÜGYI BIZONYLAT"** |
| **B) Utólagos** | a nyugta már kinyomtatva | **a nyugtát SZTORNÓZNI kell**, és csak utána állítható ki a számla |

**A B) a gyakoribb** — a vendég a nyugta láttán kéri a számlát.

**Hogyan van kikényszerítve, három rétegben:**

| Réteg | Mi |
|-------|-----|
| **Adatbázis** | Számlás módban adóügyi bizonylatszám **nem is létezhet** — nem tiltva van, hanem **a rossz állapot ábrázolhatatlan** |
| **Szerver** | Az adóügyi eredmény jelentése számlás bizonylatra **hangos hibát** ad, nem csendes semmit |
| **Kliens** | A számlás bizonylatból nem építhető adóügyi nyomtatási kérés |

### v1.5.0 — 2026-09-02 — *`Siduri-Felhasznalo` fejléc* ⚠️ `TÖRŐ, DE KIADÁS ELŐTT`

**Új, kötelező fejléc minden íráson:** `Siduri-Felhasznalo` — **aki a műveletet
kezdeményezi.**

> ⚠️ **Ez törő változás lenne, ha lenne éles kliens.** A §4.2/b szabály szerint
> a verzió akkor fagy be, amikor **az első kliens élesbe megy** — az még nem
> történt meg, tehát ez kiadás előtti módosítás. **Ez az utolsó pillanat, amikor
> ingyen van.**

**Miért nem naplózási kényelem:**

A jogosultsági modell elkészült — katalógus, szerepek, egyszeri felhatalmazás,
a `siduri.*` kör nem delegálhatósága —, és **semmi nem hívta.** Nem
mulasztásból: **a hívásnak nem volt hova megmondania, KI kezdeményezi.** A
kérés borítékja a telephelyet, az eszközt, a generációt és az idempotencia-
kulcsot hordozta; embert nem.

Ugyanebből következett, hogy az audit **„ki" mezője a legtöbb helyen üres**
volt. Egy audit, ami nem tudja, ki tette, nem audit.

| Ezután | Előtte |
|--------|--------|
| Minden művelet jogosultsághoz kötött | A modell megvolt, de nem érvényesült |
| Az audit tudja, ki tette | `null` a legtöbb bejegyzésben |
| A vezetői jóváhagyás **mindkét személyt** rögzíti | Nem volt kit rögzíteni |

**Hibakódok:** a hiányzó jogosultság `NINCS_JOGOSULTSAG` (403); a hiányzó
fejléc mostantól `HIBAS_KERES` (400) — korábban `BELSO_HIBA` (500) volt,
amiből a kliensfejlesztő annyit látott, hogy „elromlott a szerver".

### v1.6.0 — 2026-09-02 — *belépés-végpont* `NEM TÖRŐ`

**Új:** `POST /kassza/v1/belepes`.

**Miért csak most:** a v1.5.0 kötelezővé tette a `Siduri-Felhasznalo` fejlécet
— **de a kliensnek nem volt honnan megtudnia, kit írjon bele.** A hitelesítés a
szerveren megvolt, végpont nélkül. A protokoll így önmagában ellentmondott: a
kliens csak akkor tudott volna bármit csinálni, ha már tudja, ki ő.

> ⚠️ **Ez az egyetlen végpont, ami nem kér `Siduri-Felhasznalo` fejlécet** — és
> nem kivétel a szabály alól, hanem a szabály értelme: **itt derül ki, ki a
> felhasználó.** Ha ez a végpont is felhasználót kérne, a belépéshez már be
> kellene lépni.

**A válasz visszaadja a jogosultsághalmazt**, hogy a felület ne kínáljon fel
olyat, ami úgyis elutasításba futna. **Ez nem jelenti azt, hogy a döntés a
kliensé:** minden művelet a szerveren is ellenőrződik. Két helyen két döntés
lenne; itt egy döntés van és egy előzetes jelzés.

| Válaszmező | Miért van ott |
|------------|---------------|
| `pinCsereKotelezo` | A felvételkor adott PIN-t a felvevő **ismeri**. Amíg nem cserélik, a „ki nyomta meg" kérdésre a válasz nem az, akire hivatkoznánk |
| `jogosultsagok` | A `siduri.*` kör **soha** nem kerül bele — helyben úgysem gyakorolja senki, viszont a kliens lemezén fölösleges támadási felület |
| `magasKockazatu` | Ezek a kliensen **lejárnak**, ha régen látta a szervert. A sima eladás soha — az alternatíva az, hogy egy hálózati hiba megállítja a kereskedést |

**A hibaválaszok szándékosan egyformák:** a nem létező felhasználó, a rossz PIN
és a rossz **alakú** PIN mind `401`, ugyanazzal a szöveggel. Külön üzenet
megmondaná a próbálgatónak, melyik felén jár a feladatnak.

### v1.7.0 — 2026-09-04 — *kezelőlista a belépőképernyőnek* `NEM TÖRŐ`

**Új:** `GET /kassza/v1/kezelok`.

**Miért csak most:** a v1.6.0 megadta a belépést, de a kliensnek **nem volt
honnan megtudnia, kiket kínáljon fel**. Kártyás belépésnél ez nem gond — kártya
nélkül viszont a belépőképernyő üres listát mutatott volna.

**Csak akik be tudnak lépni:** aktív felhasználók, akiknek van beállított
PIN-jük. Aki nincs köztük, azt felkínálni csak arra lenne jó, hogy valaki hiába
próbálkozzon vele.

> ⚠️ **Ez a lista a személyzet nevét adja vissza hitelesítés nélkül.** Tudatos:
> ugyanezek a nevek a kioszk képernyőjén amúgy is ott vannak, és a belépéshez
> PIN kell. Amit **nem** ad vissza: jogosultságot, szerepet, kártyát — semmit,
> ami a próbálgatást segítené. Egy teszt őrzi, hogy a válaszban **pontosan két
> mező** van.

**A zároltak benne maradnak.** Aki zárolva van, arról a saját belépési
kísérletekor kap értelmes üzenetet; a listából kihagyva csak annyit látna, hogy
„eltűntem", és a támogatás keresné, mi történt.

### v1.8.0 — 2026-09-07 — *nap- és műszakvégpontok* `NEM TÖRŐ`

**Új:** `POST /kassza/v1/nap/nyitas`, `GET /kassza/v1/nap/allapot`,
`POST /kassza/v1/nap/zaras`, `POST /kassza/v1/muszak/nyitas`,
`POST /kassza/v1/muszak/zaras`.

**Miért csak most:** a v1.7.0-val a kliens **be tudott lépni, de nem tudott
eladni.** A szerver minden eladást nyitott naphoz és nyitott műszakhoz köt — a
szerződésben viszont nem volt végpont, amivel a napot vagy a műszakot ki
lehetett volna nyitni. Ugyanaz a hiba, mint a v1.6.0-nál: a szabály megvolt, a
teljesítéséhez vezető út nem.

**A `GET /nap/allapot` nem kényelmi végpont.** A kliens indulásakor azt kell
megtudnia, *hol tart a telephely* — nyitva van-e a nap, jár-e a saját műszaka,
mennyi van hátra a kényszerzárásig. E nélkül a felület vagy fölöslegesen kérne
nyitást, vagy hagyná a kezelőt eladni olyan napra, amit rég le kellett volna
zárni.

| Válaszmező | Miért van ott |
|------------|---------------|
| `hosszPerc` | A nyitás óta eltelt idő, a **konzervatívabb** mérés szerint (monoton és fali óra közül a nagyobb). Ha a kettő elcsúszik, a szigorúbbat hisszük el |
| `szint` | `NINCS` / `ENYHE` / `EROS` / `KENYSZER`. A kezelő **előre** lássa, hogy a kassza mikor áll meg, ne akkor derüljön ki, amikor sor áll a pult előtt |
| `csakFaliora` | Szerver-újraindítás után a mérés visszaesik a fali órára. **Ezt ki kell írni:** egy órajavítás onnantól észrevétlenül elmozdítja a hosszt |

**A küszöbök eltelt időtartamok, nem óraidők.** A „23:45" nem este negyed
tizenkettőt jelent, hanem huszonhárom óra negyvenöt percet a *nyitás* óta. Egy
délben nyitó helyen a kényszerzárás másnap délelőtt van — és ez a helyes
viselkedés, nem hiba.

> ⚠️ **A vakzárás nem kérés-mező.** A `MuszakZarasValasz`-ban a `vartKeszpenz`,
> `szamoltKeszpenz` és `elteres` mezők **hiányoznak** a válaszból, ha a záró
> kezelőnek nincs `muszak.osszesito_lathato` joga — nem nullák, nem nullázottak,
> **nincsenek ott.** Ha kérés-mező lenne, a kliens hazudhatna róla; ha a válasz
> csak elrejtené, a hálózaton akkor is átmenne. Így a szerver **nem is állítja
> elő** azt, amit nem szabad látnia.
>
> A `vakzaras: true` jelzi a kliensnek, hogy ne várjon összeget. A záró kezelő
> így megszámolja a kasszát anélkül, hogy tudná, mennyit *kellene* találnia — az
> eltérést a műszakösszesítőt látó vezető nézi meg utólag.

**A napzárás nem kér összeget.** A nap zárása a műszakok zárásából adódik; ha
külön összeget kérne, két igazság lenne ugyanarról a pénzről.

### v1.9.0 — 2026-09-07 — *az idempotencia a nap- és műszakírásokra is* ⚠️ `TÖRŐ, DE KIADÁS ELŐTT`

**Változás:** a `nap/nyitas`, `nap/zaras`, `muszak/nyitas` és `muszak/zaras`
mostantól **kötelezően** kéri az `Idempotencia-Kulcs` fejlécet. A
`GET /nap/allapot` nem — az nem ír semmit.

> ⚠️ **Ez a v1.8.0 hibájának javítása, néhány órával a v1.8.0 után.** A v1.8.0
> nem törlődik és nem íródik át: két repó hordozza kimásolva, lenyomatokkal, és
> egy csendben átírt verziószám pont azt a bizalmat mossa el, amiért a
> lenyomatok egyáltalán léteznek.

**A szabály az ELSŐ kiadás óta ki van írva.** A v1.0.0 táblázata így szól:
*„`Idempotencia-Kulcs` minden íráson — a degradált módból való visszajátszás
definíció szerint ismétel."* A v1.8.0 négy írást vett fel, és **egyiken sem**
volt ott. Nem új felismerés kellett hozzá, csak az, hogy a meglévő szabályt
alkalmazzuk arra, amit épp írunk.

**A kár konkrét lett volna, nem elvi:**

| Mikor | Mi történt volna | Mit lát a kezelő |
|-------|------------------|------------------|
| Műszaknyitás, a **válasz** vész el | Az újraküldés `409 MAR_VAN_NYITOTT_MUSZAK` | Hibaüzenet egy művelet után, ami **sikerült** — és nincs meg a műszak azonosítója, tehát zárni sem tud |
| Műszakzárás, a válasz vész el | Az újraküldés `409` | A leszámolt készpénz **már rögzült**, a kezelő mégis újraszámol — és a második szám lesz a hivatalos |
| Napnyitás, a válasz vész el | Az újraküldés `409 MAR_VAN_NYITOTT_NAP` | A kassza indulása látszik hibának |

**Ez pont a rossz hálózaton fáj**, vagyis ott, ahol a Siduri dolgozik. Egy jó
vonalon a válasz nem szokott elveszni — és épp ezért nem derült volna ki a
fejlesztésnél, csak élesben.

**Egy teszt őrzi**, és a teszt bizonyítottan megfogja: a javítás nélkül
`MAR_VAN_NYITOTT_MUSZAK`-ra bukik. Egy második teszt azt is őrzi, hogy ugyanaz a
kulcs **más művelethez** hangos `409 IDEMPOTENCIA_KULCS_UTKOZES` — a csendes
elfogadás azt hitetné a klienssel, hogy a második művelet is lefutott.

### v1.10.0 — 2026-09-14 — *sztornó, tételtörlés, indokkódok* `NEM TÖRŐ`

**Új:** `GET /kassza/v1/indokok/{keszlet}`,
`POST /kassza/v1/rendelesek/{rendeles}/tetelek/{tetelsor}/torles`,
`POST /kassza/v1/bizonylatok/{bizonylat}/sztorno`.

**Miért csak most — harmadszor ugyanaz a minta.** A sztornó szolgáltatásrétege
készen állt, teszttel együtt. Végpont nélkül viszont **a kassza egyetlen rossz
nyugtát sem tudott volna visszavonni.** Előbb a belépés volt így, aztán a nap- és
műszaknyitás, most a sztornó: a szabály megvolt, a teljesítéséhez vezető út nem.

> **Ez a harmadik eset, és ezért nem véletlen.** A szolgáltatásréteg tesztjei
> saját magukat hívják, nem a HTTP-felületet — így egy teljesen kész szolgáltatás
> is maradhat elérhetetlen anélkül, hogy bármi pirosra váltana. A védelem nem
> több teszt, hanem **más fajta**: olyan, ami a kliens útján megy végig.

**A törlés és a sztornó nem ugyanaz**, és a különbség nem szóhasználat:

| | Törlés | Sztornó |
|---|--------|---------|
| Mit érint | **Nyitott** rendelés tételsorát | **Lezárt**, fizetett bizonylatot |
| Keletkezik bizonylat? | Nem | **Igen — negatív bizonylat** |
| Kell az adóügyi szám? | Nem | **Igen, az eredetié** |

Ha a kettőt összemosnánk, a lezárt bizonylat „törölhetővé" válna — pontosan az a
kár, amivel egy műszakot nyugtaadás nélkül le lehet vezetni.

**Az indokkód-végpont nem kényelmi tétel.** A szerver kötelező indokkódot kér, és
**csak a telephelyen érvényeset** fogad el — a kliensnek viszont nem volt honnan
megtudnia, melyek ezek. Kódba égetni nem lehet: az alapkészlet mellé bármelyik
telephely felvehet sajátot.

> ⚠️ **A készlet NEVE nem választható KÓD.** A `SZTORNO` a készlet neve; a
> választható kódok a `VENDEG_ELALLT`, `TEVES_FELUTES`, `MINOSEGI_KIFOGAS`,
> `KONYHAI_HIBA`, `ARHIBA`, `SZAMLAIGENY`, `EGYEB`. **Ezt a hibát a végpont
> tesztjének írása közben magam követtem el** — ami pontosan azt mutatja, miért
> nem lehet a kliensre bízni, hogy kitalálja.

**Küldés után kötelező az indok, előtte nem.** Küldés előtt a törlés a normális
munka része; a kötelező indok ott csak arra tanítaná meg a kezelőt, hogy gépiesen
ugyanazt válassza — és akkor a kód semmit nem érne ott sem, ahol számít.

**Vezetői jóváhagyás a sztornóhoz:** ha a kezdeményezőnek nincs sztornójoga, nem
kell kilépnie és az üzletvezetőnek belépnie — az lassú, és a műszak is
összekeveredne. Az üzletvezető a helyszínen jóváhagyja az **egy** műveletet
(`felhatalmazas` mező), és az auditba **mindkét személy** bekerül.

### v1.11.0 — 2026-09-14 — *PIN-csere, vezetői jóváhagyás, készpénzmozgás* `NEM TÖRŐ`

**Új:** `POST /kassza/v1/pin`, `POST /kassza/v1/felhatalmazas`,
`POST /kassza/v1/kassza/mozgas`.

**Ezeket már nem egyesével találtuk meg.** A sztornó volt a harmadik olyan
szolgáltatás, ami készen állt, de HTTP-felület nélkül elérhetetlen volt. Három
után **rendszeres átvizsgálás** jött: minden állapotot változtató
szolgáltatásműveletre rákérdeztünk, hívja-e vezérlő. Négy további rést adott,
ebből három ez a három végpont. *(A negyedik a számlamegosztás.)*

> ⚠️ **A PIN-csere hiánya ZSÁKUTCA volt.** A belépés válasza kötelező cserét
> jelezhet, és a felület ilyenkor **semmit nem engedhet** a cseréig — cserélni
> viszont nem lehetett. **Egy újonnan felvett kezelő egyáltalán nem tudott
> dolgozni.**

**A jelenlegi PIN-t is kérjük a cseréhez.** Nem formaság: a munkamenet egy
nyitva hagyott kassza előtt is él, és akkor bárki átírhatná a bejelentkezett
kezelő PIN-jét — vagyis **kizárhatná a saját gépéből**, és a nevében
dolgozhatna tovább.

> ⚠️ **Az ellenőrzésre beütött PIN-en NEM fut a gyengeség-vizsgálat.** Egy
> elgépelés simán lehet gyenge alakú („0000"), és ha a gyengeség-kivétel
> felszállna, az ilyen elgépelés **más választ adna**, mint egy sima rossz PIN —
> megmondaná a próbálgatónak, melyik bemeneteket veszi egyáltalán figyelembe a
> rendszer. Ezt a hibát a végpont **első változata elkövette**, és a teszt fogta
> meg: minden érvénytelen alak ugyanazt a `401`-et kapja. Az **új** PIN-t
> viszont továbbra is szigorúan vizsgáljuk.

**A jóváhagyónak is PIN-t kell ütnie.** Enélkül a kérő egyszerűen beírhatná a
vezetője azonosítóját, és **saját magát hatalmazná fel** — a jóváhagyás pont
annyit érne, mint a hiánya. Önmagát senki nem hagyhatja jóvá: akkor a jóváhagyás
egy plusz gombnyomás lenne, nem második ember.

**A készpénzmozgás előjelét a szerver adja a típusból**, a kérésben csak pozitív
szám lehet. Így a kliens nem tud „negatív befizetést" küldeni, ami a várt
kasszatartalmat csendben elrontaná. **A jog a mozgás típusához tartozik**, nem a
„készpénzmozgás" fogalmához: a váltópénz betétele napi munka, a fölözés már a
trezor felé mozgat pénzt.

### v1.12.0 — 2026-09-14 — *számlamegosztás* `NEM TÖRŐ`

**Új:** `POST`, `GET` és `DELETE` a
`/kassza/v1/rendelesek/{rendeles}/megosztas` úton, valamint
`POST /kassza/v1/rendelesek/{rendeles}/megosztas/{resz}/lezaras`.

**A negyedik — és utolsó — rés**, amit a rendszeres átvizsgálás talált. A
`MegosztasSzolgaltatas` készen állt, végpont nélkül.

**Két lépés, és a szétválasztás szándékos.** Előbb megosztjuk a rendelést —
ekkor még senki nem fizetett —, azután a részek egyenként fizetnek. Egy
lépésben nem menne: az asztalnál a második vendég akkor is elmehet a mosdóba,
amikor az első már fizetne.

**A `LezarasKeres` séma kiemelve.** A rendelés lezárásának kérésalakja eddig
**beágyazva** élt a végpontban; a részfizetésnek ugyanaz kell. Két helyre
bemásolva biztosan szétcsúszott volna — most egy nevesített séma, amire
mindkét út hivatkozik. *(A kiemelés a meglévő alakot bitre megtartotta: a
kötelező mezők, az összes mező és az `additionalProperties: false` változatlan.)*

> ⚠️ **A részek áfájának összege nem feltétlenül egyezik az osztatlan
> bizonylatéval.** Nem hiba: a visszaszámolás bizonylatonként kerekít, és három
> bizonylat háromszor kerekít. **Élesben megmérve** (`MERESEK.md`, M24): egy
> 4 350 Ft-os rendelés osztatlan áfája 529 Ft, három részre osztva 528 Ft —
> **−1 Ft**. A részek összege közben *pontosan* kiadta a rendelést.
>
> **Ezt a kettőt nem lehet egyszerre megtartani**, és a választás tudatos: a
> pénz egyezzen, az áfa kerekedjen. Aki a napi összesítőben a kettőt
> egyeztetni próbálja, forintokat fog keresni, amik nincsenek eltűnve.

**Kiosztatlan tétel nem maradhat.** Ha maradhatna, a részek összege kevesebb
lenne, mint a rendelés, és a különbözet csendben eltűnne. A szerver `422`-vel
utasítja el.

**A megosztás csak addig vonható vissza, amíg egyetlen rész sem fizetett.** Egy
kiadott bizonylat a vendég kezében van, és az nem érvénytelenedik attól, hogy mi
átrendeznénk a maradékot. Onnantól a sztornó az út.

**A `GET` nem kényelmi végpont:** megmondja, melyik rész fizetett már. Enélkül a
felület a kezelő emlékezetéből dolgozna, és egy megszakadt műszak után **két
résznek is fizettetne**.

### v1.13.0 — 2026-09-14 — *a megosztás állapota a részek összegét is adja* ⚠️ `TÖRŐ, DE KIADÁS ELŐTT`

**Változás:** a `GET /kassza/v1/rendelesek/{rendeles}/megosztas` válaszában a
`fizetett: [bool]` tömb helyén `reszek: [{sorszam, osszeg, fizetett}]` áll.

> ⚠️ **Ez a v1.12.0 hiányának pótlása, órákkal a v1.12.0 után** — ahogy a
> v1.8.0 → v1.9.0-nál is. A v1.12.0 nem íródik át: két repó hordozza kimásolva,
> lenyomatokkal.

**A hiányt a kliens bekötése találta meg**, nem kódolvasás. A képernyő
összeállt, aztán jött a kérdés: *mi történik, ha a kliens újraindul, miközben
egy megosztott számla fele még nem fizetett?* A válasz az volt, hogy **semmi
sem folytatható**: a kliens megtudta volna, hány rész van és melyik fizetett —
azt nem, hogy **mennyit kell kérni**.

**Márpedig pont ez a megosztás értelme:** a vendégek nem egyszerre fizetnek. Ha
a folytatáshoz a kliens memóriájára lenne szükség, a megosztás csak addig
működne, amíg senki nem zárja be az alkalmazást — és a pult mögött ez nem
elfogadható feltétel.

**Az összeg a rész saját soraiból adódik**, nem tárolt végösszegből: így nem tud
elcsúszni attól, amiből a bizonylat készül.

**Élesben végigpróbálva:** egy három soros, 4 350 Ft-os rendelés két részre
osztva (a harmadik soron ketten osztoznak) → 1 575 + 2 775 = 4 350 Ft; az első
rész fizet; **a kliens „újraindul"**; a maradék **kizárólag az állapot-végpontból**
kifizethető volt.

---

### v1.14.0 — 2026-09-14 — *régebbi bizonylat megkeresése, és a sztornó helyre kerül* ⚠️ `TÖRŐ, DE KIADÁS ELŐTT`

**Miért nem volt jó az előző:** a kasszán **nem lehetett megtalálni egy
korábbi bizonylatot**. A sztornó végpontja bizonylat-**azonosítót** kér — azt
viszont csak az a kliens ismerte, amelyik az eladást maga zárta le. A másnap
visszatérő vendég a kezében tartotta a nyugtát, a pincér a számot be tudta
volna ütni, de **nem volt hova**. A szabály megvolt, az odavezető út nem.

**Új végpontok:**

| Végpont | Jog | Miért így |
|---------|-----|-----------|
| `GET /bizonylatok/szam/{siduriBizonylatszam}` | **nincs riportjog** | Aki a számot be tudja ütni, az a papírt is látja. A riportjog ott védene, ahol nincs mit védeni |
| `GET /bizonylatok` | `riport.napi_forgalom` | A **teljes nap** végigböngészése forgalmi adat, akkor is, ha sztornózni akarnak belőle |

Mindkettő **fejlécet** ad (`BizonylatFejlec`), nem teljes bizonylatot: szám,
idő, végösszeg, állapot. Amit nem küldünk el, azt nem is kell védeni.

**A törő rész — a sztornó helye megváltozott.** A sztornó eddig az **eredeti**
bizonylat üzleti napjára és **eredeti** műszakjába került. **Mérve, élő
szerveren**, három seb, mindhárom néma *(MERESEK.md M27)*:

1. A már elszámolt, **lezárt** műszak várt készpénze **visszamenőleg
   megváltozott**: 1 200 Ft → −1 200 Ft. Egy átadott kassza száma módosult az
   átadás után.
2. A bizonylatszám **előtagja maga az üzleti nap** (`yyMMdd`), tehát egy **ma**
   kiadott bizonylat egy **már lejelentett nap** számsorát toldotta meg.
3. A pénz **ma** jön ki a fiókból, a hiánya viszont tegnapra könyvelődött — a
   különbözetet a mai műszak vállán keresték volna.

**Amit a kliensnek tudnia kell:**

- a válaszban kapott sztornó száma **mai előtagot** visel, nem az eredetiét —
  a kettőt ne hasonlítsa össze;
- **nyitott műszak nélkül** a sztornó `409 NINCS_NYITOTT_MUSZAK`: csukott
  fiókból nem jön ki pénz;
- az eredeti bizonylat üzleti napja és műszakja **változatlan marad**.

**Más műszak bizonylatához külön jog kell** (`sztorno.mas_muszakbol`) a
`sztorno.bizonylat` mellett. ⚠️ **Ez a jog a katalógusban eddig is ott volt, az
ÜZLETVEZETŐ sablonjában is — de a kód sehol nem hivatkozott rá.** Egy
műszakfelelős a saját mai nyugtáját és a tegnap estit *ugyanazzal az egy
joggal* vonhatta vissza. Ami nincs ellenőrizve, az nincs.

**Új hibakód:** `TOBB_JOGOSULTSAG_HIANYZIK` (403). A helyszíni jóváhagyás
**egy** jogot pótol, nem kettőt: egyetlen kódra szól, és egyszer használható
fel. Ha a kezelőnek mindkét jog hiányzik, a kliens **ne kérjen jóváhagyást** —
a vezető odaállna, jóváhagyná, és a művelet a második kapun mégis elhasalna,
már elhasznált jóváhagyással.

---

### v1.15.0 — 2026-09-14 — *a lezárás végre ellenőrzi a jogosultságokat* ⚠️ `TÖRŐ, DE KIADÁS ELŐTT`

**Miért nem volt jó az előző:** a `POST /rendelesek/{r}/lezaras` **egyetlen
jogosultságot sem nézett meg**. A kódok léteztek, a szerep-sablonok helyesen
osztották ki őket — a kód viszont soha nem kérdezte meg. Ez a
jogosultság-söprés *(FOLYAMATBAN.md §7.3)* eredménye: **84 katalóguskódból 69
volt ellenőrizetlen**, és ebből öt **élő kódútra** vonatkozott.

**Amit ez a gyakorlatban jelentett:** bárki, aki egyáltalán el tudott adni,
adhatott **tetszőleges végösszeg-kedvezményt** — a vendégtől teljes ár, a gépbe
kedvezmény, a különbözet a zsebbe. Ez a kasszavisszaélés legrégebbi formája.

**A lezárás négy jogosultsága:**

| Jog | Mikor kell | Miért |
|-----|-----------|-------|
| `kedvezmeny.vegosszeg` | bármilyen kedvezménynél | Itt válhat szét a vendég által fizetett és a gépbe ütött összeg |
| `kedvezmeny.kuszob_felett` | a telephelyi küszöb felett | A küszöb pont az a határ, ami fölött vezetőnek kell látnia |
| `szervizdij.modositas` | nem nulla szervizdíjnál | A felszolgálói jutalék alapja |
| `eladas.szamla_keres` | `SZAMLA` módnál | Más adóügyi út, más bizonylat |

**A sima lezáráshoz továbbra sem kell külön jog.** Ezek csak akkor lépnek
életbe, ha a kérés tartalmazza őket.

**Új mező — `felhatalmazas` a `LezarasKeres`-en.** A pincér az asztalnál áll;
nem az a megoldás, hogy kilép és az üzletvezető bejelentkezik. ⚠️ **De egy
jóváhagyás EGY jogot pótol, nem kettőt:** egyetlen kódra szól és egyszer
használható fel. Ha két jog hiányzik (küszöb feletti kedvezménynél tipikusan
mindkettő), a szerver `TOBB_JOGOSULTSAG_HIANYZIK` kódú **403**-at ad, **a
jóváhagyást pedig nem használja el** — a kliensnek ilyenkor **nem szabad**
jóváhagyást kérnie.

**⚠️ A küszöb mostantól a FIX összegű kedvezményre is vonatkozik.** Eddig csak
a százalékos alakot nézte, tehát egy 10 000 Ft-os számlára adott **9 999 Ft-os
„fix" kedvezmény — vagyis 99,99%** — indok és külön jog nélkül átment. A küszöb
egyetlen legördülő-választással megkerülhető volt. A fix összeget mostantól a
**kedvezmény előtti alaphoz** arányítjuk.

**Új készpénzmozgás-típus: `BORRAVALO_KIVET`.** Az adatbázis ezt a típust a V9
óta ismeri, és a `kassza.borravalo_kifizetes` jog is ki volt osztva — **a kód
viszont soha nem állította elő**. A készpénzes borravalót így egy sima
`KIFIZETES`-ként vitték ki, a `kassza.kifizetes` joggal. A kettő nem ugyanaz: a
beszerzésre kivitt pénz a **vállalkozásé**, a borravaló a **személyzeté**. Más
felelősség — és a borravaló-riport is csak így tud külön számot mondani.

---

### v1.16.0 — 2026-09-14 — *kedvezmény-felület a kasszán, és a telephelyi küszöbök lekérdezhetők*

**Miért nem volt jó az előző:** a v1.15.0 óta a szerver helyesen ellenőrzi a
lezárás négy jogosultságát — a POS-kliensnek viszont **nem volt** kedvezmény-,
szervizdíj- és számlaigény-felülete. A szabály megvolt, a hozzá vezető út nem;
ugyanaz a minta, mint a sztornónál és a nap-/műszaknyitásnál.

**Új végpont — `GET /beallitasok`:**

| | |
|---|---|
| Mit ad | `kedvezmenyIndokSzazalek`, `szervizdijMegerositesSzazalek` |
| Jogosultság | **nincs** — ez nem forgalmi adat, hanem a telephely szabálya |

⚠️ **Miért kell egyáltalán:** a kassza a kedvezmény beütésekor — **a kérés
elküldése előtt** — meg akarja mondani a kezelőnek, hogy kell-e indok és
vezetői jóváhagyás. Kódba égetve ezek egy hónap múlva mást mutatnának, mint
amit a szerver elfogad, és a kezelő a **szerver elutasításából** tudná meg,
a vendég előtt.

**A `Szazalek` protokoll-alakja külön a megjelenítési alaktól.** A magyar
szövegbe való `10,00%` jel a szerződés mintáján (`^[0-9]{1,3}\.[0-9]{2}$`)
elbukik. Ezt a **saját tesztem fogta meg** az első futáson; a mintát mostantól
külön állítás is őrzi.

**Új közös tesztvektorok: `kedvezmeny.json` (8 eset).** A kassza a
fizetőképernyőn **kiírja a fizetendőt**, mielőtt a szerver válasza megérkezne.
Ha a két számítás egy forintban eltér, a szerver a lezárást *„a fizetés nem
egyezik"* hibával utasítja el — a vendég előtt, készpénzzel a kézben. A
vektorok az egyetlen dolog, ami a két megvalósítást együtt tartja.

**A vektorfájlok mostantól a lenyomatjegyzékben is benne vannak.** Eddig csak a
`*.yaml` szerepelt, tehát egy **kézzel átírt tesztvektor észrevétlen maradt**
volna — pont az, ami a két nyelv egyezését bizonyítja. A kliens tesztje ezt
mindvégig ellenőrizte; csak soha nem futott le *(lásd `MERESEK.md` M29)*.

---

### v1.17.0 — 2026-09-15 — *a kiosztások sorrendje kimondva* ⚠️ `NEM TÖRŐ`

**Nincs új mező és nincs viselkedésváltozás** — egy **kimondatlan szabály**
került a szerződésbe, mert kliensoldali hibát okozott.

A `Kiosztas.suly` leírása mostantól kimondja: **a kiosztások sorrendje
számít**. A maradék forint a legnagyobb súlyú részre kerül, holtversenynél a
listában **korábbira** — tehát ugyanaz a terv más sorrendben más összeget ad.

**Miért kellett ezt leírni:** a POS-kliens a kezelő **koppintási sorrendjében**
küldte a kiosztásokat *(mérve: `MERESEK.md` M30)*. Ha a pincér a 3. részre
koppintott először, a maradék oda került, nem az 1.-re — ugyanaz a felállás más
kézmozdulattal más forintot adott. A kliens ezt javította; a szerződés eddig
**nem figyelmeztetett rá**, tehát a készülő Dart vékonykliens pontosan
ugyanabba futott volna bele.

**A kliensnek soronként, rész szerint növekvően kell küldenie.**

**Új közös tesztvektorok: `megosztas.json` (10 eset)** — súlyozott osztás,
maradék a nagyobb súlyra, nulla súly, vegyes arányok több soron, nem bontható
kategória. A megosztóképernyő mostantól **kiírja, ki mennyit fizet**, mielőtt a
terv elmegy; a számot ugyanaz a szabály adja, amit a szerver futtat.

---

### v1.18.0 — 2026-09-15 — *asztalos rendelés* ⚠️ `NEM TÖRŐ`

**A gyorseladás és az asztalos rendelés két külön folyamat**, és a katalógusban
két külön jog állt rajtuk (`eladas.gyorseladas`, `eladas.asztalra`) — csak
eddig egyik sem volt megépítve. A különbség nem a felület:

| | Gyorseladás (pult) | Asztalos rendelés |
|---|---|---|
| Hol él a kosár | a **kliensnél** | a **szerveren** |
| Meddig | másodpercek | **órák** |
| Ki nyúl hozzá | egy kezelő | **több kezelő, több gépről** |
| Gépvesztéskor | a vendég újra elmondja | **a vendég nincs ott** |

**Új végpontok:**

| Végpont | Mire |
|---------|------|
| `GET /asztalok` | Az asztalok **és a rajtuk álló nyitott rendelés** — egy lekérdezésből |
| `GET /rendelesek/{r}` | Egy nyitott rendelés tartalma **és a verziója** |
| `POST /rendelesek/{r}/vendegszam` | A vendégszám módosítása |

**Bővült:** `POST /rendelesek` (asztal, vendégszám), `POST .../tetelek`
(**verzió**), és a `Rendeles` válasz (vendégszám, verzió).

**⚠️ Optimista zárolás.** Két pincér ugyanahhoz az asztalhoz nyúlhat
egyszerre; zárolás nélkül az egyik írása **csendben** felülírná a másikét. Az
írás a látott **verzióval** megy; ha a szerveren azóta változott, a válasz
`409 RENDELES_MEGVALTOZOTT` — a kliensnek frissítenie kell, és **meg kell
mutatnia, mi került rá**.

**⚠️ Egy asztalon egy nyitott rendelés.** Nem alkalmazási ellenőrzés, hanem
**egyedi index**: egy ágat ki lehet felejteni, egy indexet nem. Két nyitott
rendelés ugyanazon az asztalon azt jelentené, hogy a vendég két számlát kap ott,
ahol egyet kért.

**⚠️ A 24 órás korlát (H6.5) érvényesítve.** Efölött a rendelés nem bővíthető
(`409 RENDELES_TUL_REGI`), és **22 óra fölött a válasz figyelmeztetést hoz** — a
korlátba beleütközni a legrosszabb pillanat: a vendég fizetni akar, és a kassza
nemet mond.

**A `rendeles.mas_pincer_asztala` és a `rendeles.vendegszam_modositas` is
ellenőrzött** — újabb kettő a söprés listájáról.

---

### v1.19.0 — 2026-09-15 — *árfolyamforrás és valutás fizetés* ⚠️ `TÖRŐ, DE KIADÁS ELŐTT`

**Mi hiányzott eddig:** nem a valuta, hanem a **forrása**. A `Fizetes` alak, a
`ValutaOsszeg` és az `Arfolyam` séma kezdettől megvolt, az adatbázis-megszorítás
ki is követelte őket — **árfolyamforrás viszont sehol nem volt a rendszerben**.
Így a kliens bármilyen árfolyamot küldhetett, és a szerver elfogadta: a
pénztáros elveszi a húsz eurót, a bizonylatra pedig az az összeg kerül, amit a
kliens állított. **Az árfolyam a kasszavisszaélés legrövidebb útja — nem a pénzt
kell eltüntetni, csak rosszul átváltani.**

**Új végpontok:**

| Végpont | Mire |
|---------|------|
| `GET /arfolyamok` | Az érvényes árfolyamok, a **régiség jelzésével** |
| `POST /arfolyamok` | Árfolyam rögzítése — saját, **magas kockázatú** joggal (`arfolyam.megadas`) |

**Új jogosultság:** `arfolyam.megadas`. **Szándékosan nem az kapja meg, aki a
valutát elfogadja** (`eladas.fizetes.valuta`): aki beállíthatja az árfolyamot,
az dönti el, mennyit ér a vendég húsz eurója.

**⚠️ A lezárás mostantól a FIZETÉSI MÓDOK JOGAIT is megkérdezi.** Mind az öt
`eladas.fizetes.*` kód ott állt a katalógusban, a szerep-sablonok helyesen
osztották ki őket, és a kassza el is rejtette a gombot — a **szerver** viszont
bármit elfogadott. **Egy elrejtett gomb nem jogosultság:** a kérést nem a gomb
küldi el, hanem a kliens. Ez a törő rész: aki eddig minden módon fizettethetett,
annak most a megfelelő jog kell hozzá.

**⚠️ A valutás soron az árfolyam kötelező, és a szerver ÖSSZEVETI** a
telephelyen érvényessel (`409 ARFOLYAM_ELTER`). **Csendben nem cserélünk
árfolyamot:** a vendégnek már mondtak egy összeget. A forintösszegnek az
átváltás eredményének kell lennie (`422 VALUTA_ATVALTAS_ELTER`), és
valutaadat csak valutás soron állhat (`422 VALUTA_ADAT_NEM_VALUTAS_SORON`).

**⚠️ A VISSZAJÁRÓ NEGATÍV KÉSZPÉNZSOR.** Forintban megy vissza (G5.6), tehát a
bizonylaton ott áll, ahol a pénz ténylegesen kimegy a fiókból. Egy 7940 Ft-os
számlára adott 25 EUR 395,50-es árfolyamon 9888 Ft; a visszajáró 1948, öt
forintra kerekítve 1950 → a készpénzsor **−1950**, kerekítési különbözete −2.
Az összeg így is stimmel: 9888 + (−1950) = 7938 = 7940 + (−2). **Enélkül a
műszakelszámolás pont ennyivel többet várna a fiókban.** Ebből következik, hogy
egy valutás fizetés két sort ad — de **nem lesz vegyes fizetés**: a vegyesség és
a módonkénti jog csak a **pozitív** sorokból számolódik.

**Új közös tesztvektor:** `valuta.json` — az átváltás és a fizetési terv. A
kassza **előállítja** a sorokat, a szerver **elfogadja** őket; a vektor egy
megállapodást ellenőriz a két végén.

**Ami továbbra sem kész (G5.6):** az adóügyi eszköz **saját**
valutaárfolyam-beállítását ki kell írni és vissza kell olvasni. Az adóügyi
illesztő még nincs kész, ezért ez hiányzik — és ez nem részlet: **két árfolyam
két papíron**.

---

### v1.20.0 — 2026-09-15 — *az adóügyi eszköz árfolyama a bizonylat mellé* ⚠️ `NEM TÖRŐ`

**A G5.6 maradék fele.** Az árfolyamforrás (v1.19.0) megmondja, mivel számol a
rendszer — **a nyugtát viszont az eszköz írja, a SAJÁT beállításával**. Ha a
kettő eltér, **két árfolyam kerül két papírra** ugyanarra a fizetésre, és utólag
nem lehet megmondani, melyik volt az igaz.

**Bővült:** a `POST /bizonylatok/{id}/adougyi-eredmeny` kérése egy opcionális
`eszkozArfolyam` mezővel. Nem törő: a mező elhagyható.

**⚠️ A KIÍRÁS ÖNMAGÁBAN NEM BIZONYÍTÉK.** A kliens a nyomtatás **előtt**
egyezteti a gép árfolyamát — kiírás után **kötelező visszaolvasás** —, és
eltéréskor **el sem indítja a lezárást**: bizonylat se szülessen, amit nem lehet
kinyomtatni. Egy elutasított, egy csonkolt vagy egy másképp kerekített érték
pontosan úgy néz ki, mint egy sikeres, amíg a nyugta ki nem jön.

**Amit a mező hordoz:** amit a gép a **visszaolvasáskor** mondott. Enélkül
utólag nem az lenne rögzítve, hogy a **gép** egyetértett, csak az, hogy a
**kliens** hitte.

**Eltérésnél a szerver NEM utasítja el a jelentést.** A nyomtatás megtörtént; az
elutasítás azt jelentené, hogy a rendszer nem tud a papírról, ami a vendég
kezében van — és a kliens örökké újrapróbálkozna. Az eltérés **biztonsági
auditba** kerül (`ADOUGYI_ARFOLYAM_ELTERES`), a rögzítés pedig marad. A
**hiányzó** árfolyam ugyanolyan eltérés, mint a rossz: a „nem tudjuk" nem azonos
az „egyetértett"-tel.

**A tiltás csak a valutára szól.** Egy néma árfolyam-beállítás nem állíthatja meg
a forintos eladást.

**⚠️ A premissza igazolatlan** (`MERESEK.md` M34): feltételezzük, hogy az eszköz
árfolyam-beállítása kiolvasható és írható. Fizikai készülék nélkül ez nem
dönthető el.

---

### v1.21.0 — 2026-09-16 — *a napzárás automatikája kiderül a kasszának* ⚠️ `NEM TÖRŐ`

**Bővült:** a `Beallitasok` alak egy `automatikusNapzaras` jelzővel.

**Miért kell.** A `nap.kezi_zaras` **feltételes** jog: a katalógus pontosan azt
mondja, hogy „kézi napzárás, **ha automatikus van beállítva**". Ahol nincs
tervezett zárás, ott a kézi zárás a **rendes üzemmód**, és a műszakfelelősnek is
mennie kell.

**⚠️ A felület ezt eddig SZIGORÚBBAN vette, mint a szerver** — minden
napzárásnál megkövetelte a `nap.kezi_zaras`-t, tehát pont a **kézzel záró**
helyeken rejtette el a gombot attól, akinek az a napi munkája. A szerver
viszont egyáltalán nem kérdezte. **Mindkét oldal rosszul csinálta, ellentétes
irányban.** A jelző nélkül a kassza nem tudja eldönteni, melyik eset áll fenn.

**A szigorúbb felület is hiba, nem óvatosság:** egy szótlanul hiányzó gomb azt
üzeni a kezelőnek, hogy ő rontott el valamit.

---

### v1.22.1 — 2026-09-21 — *a `nullable` javítása: 3.0-ás alak egy 3.1-es szerződésben* `NEM TÖRŐ`

**Két mező** (`ArfolyamAllapot.beallitotta`, `ArfolyamAllapot.figyelmeztetes`)
`nullable: true`-val volt jelölve. **Ez az OpenAPI 3.0 alakja, és a 3.1-ben nem
létezik** — a szerződés viszont `openapi: 3.1.0`.

> ⚠️ **Miért nem kozmetika:** az ellenőrzők és a generátorok a `nullable`-t
> 3.1-ben **csendben eldobják**. A generált kliens így **nem nullázhatónak**
> hitte volna a mezőt, miközben a szerver `null`-t küld — a hiba **a kliensnél,
> futásidőben** jött volna elő, és nem a szerződésben látszott volna.

**A javítás:** `type: [string, "null"]`. **Az alak nem változott** — a szerver
eddig is `null`-t küldött ezekre a mezőkre; csak eddig **nem volt leírva**, hogy
szabad.

**Hogyan derült ki:** a K3 szerződés kiadásakor futott le először a teljes
szerződés-ellenőrzés mindhárom fájlra. **Addig a hiba benne volt, és semmi nem
szólt** — a K1 ellenőrzését soha nem futtatta senki, mert folyamatos beépítés
nincs *(`CLAUDE.md` 3/a: az Actions perce pénz)*.

**Ezzel együtt:** két `no-ambiguous-paths` figyelmeztetés **nevesített
kivételre** került (`.redocly.lint-ignore.yaml`), indoklással és a vállalt
kockázattal — nem a szabály kikapcsolásával.

### v1.22.0 — 2026-09-17 — *a `csakFaliora` végre azt jelenti, amit mond* ⚠️ `NEM TÖRŐ`

**Az alak nem változott**, a `NapAllapot.csakFaliora` **jelentése** igen — ezért
verzióemelés.

**Mi volt a baj.** A leírás eddig azt állította, hogy a mérés „szerver-újraindítás
után" esik vissza a fali órára. **Ez nem volt igaz.** A szerver a monoton
számlálók nyers különbségét mérésnek hitte, ha a mostani érték nem volt kisebb a
nyitáskorinál — azt viszont nem nézte, hogy **ugyanaz az óra** mérte-e a kettőt.
Egy újraindítás után ezért a jelzés **tévesen elmaradhatott**; egy tartalék
szerver vagy másik gép nagyobb számlálójával pedig egy nyolcórás nap napokig
tartónak látszott, és a vészfék **szolgálat közben** zárt.

**Mostantól** a mező akkor igaz, ha a nap nyitását **más monoton óra** mérte,
mint ami most fut: újraindult szerver, másik gép, tartalék szerver.

**⚠️ Ami a felületen látszani fog:** a figyelmeztetés **gyakrabban** jelenik meg —
minden szerver-újraindulás után, a nyitott nap hátralévő részében. Ez nem
regresszió, hanem az, amit a mező mindig is állított magáról. Egy elvesztett, de
érvényes mérés a fali órára esik vissza, és ezt jelezzük; egy tévesen elhitt
mérés viszont hamis vészzárást okozhat, és azt senki nem jelezné.
### v1.23.0 — 2026-09-23 — *személyzetkezelés a pult mögül* `NEM TÖRŐ`

Öt új végpont a `/szemelyzet` alatt: lista, szereplista, szerepek, egyedi
jogosultságok, letiltás.

⚠️ **NEM AZONOS A `/kezelok` LISTÁVAL.** Az a belépőképernyő listája: nevet
ad, hitelesítés nélkül, és szándékosan **semmi mást** — se szerepet, se jogot,
se kártyát. Ez itt a személyzet **kezelése**, jogosultsághoz kötve. A két lista
összevonása azt jelentené, hogy a belépőképernyő hitelesítés nélkül adna ki
jogosultsági adatot.

| Mi | Döntés | Miért |
|----|--------|-------|
| **Minden írás** | **Elbírálásra vár** (`varakozo: true`) | A változtatás helyben azonnal él, de a felhő mondja ki a végső szót (`HOZZAFERES.md` §7.2). A pultfőnöknek **tudnia kell**, hogy amit lát, az még nem végleges |
| **`masolatFrissitve`** | **Minden listában benne van** | Egy néma másolat ugyanolyan „rendben" képet mutat, mint egy friss — pedig lehet, hogy hetek óta nem frissült, és egy kilépett dolgozó még mindig be tud lépni |
| **`sorsuk`** | A helyi változtatások **sorsa** felhasználónként | A változtatás kedden történt, a válasz szerdán érkezik — esetleg **más műszakban**. Ha nem látszik, a változtatás úgy vesz el, hogy senki nem tud meg róla |
| **`kioszthato`** | Szerepenként, **előre** | A felület így nem kényszerül próbálkozásra. De a védelem nem itt van: **az elrejtett gomb nem jogosultság** |
| **`egyuzletes`** | A válaszban | Egyetlen telephely esetén a globális oldal **meg sem jelenik** (§7.1). A telephely **eltárolja**, mert a pultnak kapcsolat nélkül is tudnia kell |
| **Hatalmi jog** | **422 már itt**, nem a felhő válaszára várva | A felhő is megtagadná, de a válasza **órákkal később** érkezik — és addig a pultfőnök azt hinné, elintézte. **Az első nem-et ott kell kimondani, ahol a gomb van** |

⚠️ **A letiltás kapcsolat nélkül is megy; a visszaengedés SOHA.** Szándékosan nem
szimmetrikus: kijuttatni valakit **sürgős** lehet, épp a kapcsolat nélküli
órákban; beengedni sosem az.
