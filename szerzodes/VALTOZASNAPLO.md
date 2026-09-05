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
