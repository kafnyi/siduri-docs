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

*Még nincs kiadva.* A K2-nek **két megvalósítása lesz** — a felhő és a
telephelyi szerver —, és a szerződésteszt mindkettőn ugyanaz fut. Ez teszi a
§22.2 ígéretét gépi kényszerré.

---

## `szinkron` (K3)

*Még nincs kiadva.* A **legszigorúbb kompatibilitási kényszerű** szerződés: a
felhő és a telephely soha nem frissül egyszerre.

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
