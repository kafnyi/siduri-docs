# A törzsadat felküldése — a telephelyről a felhőbe

> **Állapot: az 1–3. darab KÉSZ** *(2026-09-24)*, élő próbán végigvíve. A
> 4–6. (írás-történet, előző/vesztes érték, felület) hátra van. Mindhárom
> döntési kérdés a javaslat szerint dőlt el (lásd 5.).
>
> **Miért most:** a Ziggurat böngészős átnézésekor kiderült, hogy az árnál nem
> látszik, **mi volt előtte**. Ennek utánajárva egy nagyobb hiány került elő:
> a telephelyen átírt törzsadat **soha nem jut fel a felhőbe**. Ez a terv azt
> írja le, hogyan jut fel — és csak erre épülhet rá a felhős ártörténet és az
> „előző / elveszett érték” kijelzése.

---

## 1. Mi a helyzet ma — mérve, nem feltételezve

| Mit | Telephely | Felhő |
|---|---|---|
| Törzsadat **írása** | ✅ ár (`TorzsadatIro.arat`) | ❌ **nincs írási útvonal** — sem végpont, sem feltöltés |
| Honnan kerül bele a törzsadat | a helyi kezelés | ❌ **sehonnan** — a fejlesztői bérlőben nulla termék van; az élő próba SQL-lel töltötte fel |
| Mezőeredet (`mezo_eredet`) | ✅ | ✅ tábla van, de nem ír bele senki |
| Ártörténet | ✅ `ar_tortenet`, trigger írja | ❌ nincs |
| A **vesztes** írás nyoma | ✅ audit-lánc, `AR_MODOSITAS_ELVESZETT` | ❌ nincs |
| Szinkron felfelé | lekérdezés, nyugta, hozzáférés-változás | — |
| Szinkron **felfelé, mezőérték** | ❌ **nincs** | — |

**Ebből három dolog következik, és egyik sem az előző ár kérdése:**

1. ⚠️ **A felhős Ziggurat csendben mást mutat, mint a telephelyi.** Egy
   telephelyen átírt ár a felhőben a régi értékkel látszik, és semmi nem jelzi.
   Ez néma kudarc (§5), ráadásul pont ott, ahol a tulajdonos otthonról néz rá.
2. ⚠️ **A „későbbi írás nyer” szabályt ma csak a telephely alkalmazza.** A felhő
   a telephelyi írásról nem tud, tehát nem is dönthet róla.
3. ⚠️ **Egy döntés teljesítetlen:** *„a teljes [ár]történet a felhőben áll”*
   (B16.5 kiegészítés). A felhőben nincs ártörténet.

---

## 2. A javaslat röviden

**A telephely minden törzsadat-írását egy kimenő sorba teszi, és a szokásos
lekérdezési körben felküldi. A felhő ugyanazzal a szabállyal dönt róla, mint a
telephely a lefelé érkező értékről: a későbbi írás nyer, a zárolt érték mindig
nyer. Minden kísérlet — a vesztes is — bekerül egy írás-történetbe, mindkét
oldalon ugyanabba az alakba.**

Egy mondatban az indok: **a lefelé menő irány már így működik**, és ez a
felfelé menő tükörképe. Nem új szabály, hanem ugyanaz a szabály a másik
oldalon is.

---

## 3. A részletek

### 3.1 Egy út a kezdeti feltöltésre és a módosításra

A felhőben ma **nincs** törzsadat, tehát az első lépés nem egy módosítás, hanem
a **teljes katalógus** feltöltése.

**Javaslat: ugyanaz az út.** Egy felküldött tétel mindig *(rekord, mező,
érték, mikor, honnan)*. A kezdeti feltöltés annyi, hogy a telephely **minden**
mezőt elküld; a módosítás, hogy csak a változottat.

**Miért:** a lefelé menő iránynál ugyanezt döntöttük (S3: *„a tömeges átvitel
ugyanaz a végpont — egy ritkán futó második kódút évekig észrevétlenül
romolhatna el”*). A felfelé menő irányra ugyanez igaz, és a kezdeti feltöltés
pont az a kódút, ami telephelyenként **egyszer** fut.

⚠️ **A rekord létrehozása külön tételfajta**, mert egy új terméknél nincs mit
„mezőnként összevetni” — a felhő egyszerűen még nem tudja, hogy létezik.
Két fajta tehát: `LETREHOZAS` *(a teljes sor)* és `MEZO_ERTEK` *(egy mező)*.

### 3.2 Az időbélyeg nélküli mezők

Mezőeredetet ma **csak az ár** kap. A név, az áfa, a kategória, az állapot
időbélyeg nélkül él a telephelyen.

**Javaslat:** ezeknél a **telephely nyer**, mert ma **ő az egyetlen író** — a
felhőben nincs olyan felület, ami ezeket írná. Amikor a felhő is írhatja őket,
**azzal együtt** kapnak mezőeredetet, különben ugyanez a hiány nyílna újra.

**ÁRA:** addig a felhőből ezek nem szerkeszthetők. Ez ma is így van, tehát
nem veszítünk semmit — csak nem nyerünk.

### 3.3 Hol utazik: a lekérdezésben, nem külön úton

A felküldött tételek a **`/lekerdezes`** kérésében mennek fel, és a válasz
tételenként hozza a kimenetet.

**Miért:** a hozzáférés-változásoknál ugyanezt választottuk, és ugyanazért: ha
külön úton menne, a telephely a következő lekérdezésben egy olyan állapotot
kaphatna vissza, ami a saját, épp felküldött írását még nem tartalmazza.

### 3.4 A kimenő sor: nem lehet elfelejteni

A telephely a kimenő tételt **ugyanabban a tranzakcióban** írja a sorba, mint
magát a módosítást. Így nincs olyan állapot, ahol az ár átíródott, de a
felküldése elveszett.

* A tétel akkor törlődik a sorból, amikor a felhő **kimenetet adott rá**
  *(bármelyiket — az elutasítás is válasz)*.
* Minden tételnek saját azonosítója van, és a felhő megjegyzi, mit bírált már
  el. **Egy megismételt felküldés nem bírálódik el kétszer.**
* A sor **offline is gyűlik**, és kapcsolódáskor megy fel.

### 3.5 A felhő döntése: ugyanaz a szabály

| Eset | Kimenet | Mi történik a felhőben |
|---|---|---|
| A felküldött érték **későbbi**, mint ami a felhőben áll | **ELFOGADVA** | átíródik, mezőeredet: `telephely` |
| A felhőben **későbbi** érték áll | **ELAVULT** | nem íródik át, de **bekerül a történetbe vesztesként** |
| A mező **zárolt** | **ZAROLT** | nem íródik át, bekerül vesztesként |
| Nincs ilyen rekord, érvénytelen érték | **ELUTASITVA** | nem íródik át, kóddal |

⚠️ **Az ELAVULT és a ZAROLT a telephelyen már rendben van.** A felhő későbbi
értéke vagy zárolása úgyis lejön a szokásos úton, és a telephely a saját
szabálya szerint alkalmazza. A kimenet tehát nem parancs a telephelynek, hanem
**tájékoztatás** — a felületen ebből lesz az „elveszett” jelzés.

⚠️ **Nincs visszhang.** Egy elfogadott telephelyi írásból a felhő **nem**
készít lefelé menő változást ugyanannak a telephelynek. Ha készítene, az
azonos időbélyeg miatt a telephely a saját értékét **vesztesként naplózná** —
egy nem létező ütközést. *(Az ár ma telephelyenkénti adat, tehát más
telephelynek sem kell lemennie. A lánc-szintű közös árnál ez más lesz — az
külön szelet.)*

### 3.6 Az írás-történet — a vesztes is benne van

**Mindkét oldalon ugyanaz a tábla**, `mezo_iras`: minden írási kísérlet egy
sor *(rekord, mező, érték, mikor, honnan, ki, indok, kimenet)*.

* **Csak beszúrható**, adatbázis-triggerrel — mint a jogosultság-napló. Egy
  átírható történet pont ott hazudna, ahol a legdrágább.
* A telephelyi `ar_tortenet` **marad**, amíg a kassza és a riportok abból
  olvasnak. Az új tábla nem váltja ki, hanem a **vesztes** írásokkal egészíti
  ki. *(Ma a vesztes csak az audit-lánc JSON-jában van, ami lekérdezésre
  alkalmatlan.)*
* **Miért mindkét oldalon ugyanaz:** a Ziggurat mindkét helyről kiszolgálható,
  és a két válasznak ugyanazt kell mondania. A közös szerződésteszt így
  mindkét megvalósításon ugyanazt követelheti meg.

### 3.7 Amit a Ziggurat mutat

Az admin-szerződés `Kiszereles` alakja két nem kötelező mezőt kap:

| Mező | Mit mond |
|---|---|
| `arElozo` | az előtte érvényes ár, mikor és honnan kapta |
| `arElveszett` | a **legutóbbi** vesztes írás, ha a mostani érték óta vagy közvetlenül előtte történt: mennyi lett volna, mikor, honnan, és **miért** veszített *(későbbi érték / zárolás)* |

A felületen az ár mellett:

> **2700 Ft** · 09. 24. 11:00 · felhő
> előtte: 2650 Ft
> ⚠️ **Nem lépett érvénybe:** 2500 Ft · 09. 24. 10:00 · telephely — egy későbbi
> módosítás felülírta

⚠️ **A „miért” nem elhagyható.** Egy puszta „elveszett” azt sugallná, hogy
hiba történt — pedig a szabály szerint működött. A tulajdonosnak azt kell
látnia, hogy **valaki később átírta**, nem azt, hogy a rendszer elnyelte.

---

## 4. Amit ez a terv NEM old meg, kimondva

* **A felhőben a múlt nem lesz meg.** Az írás-történet a bevezetés napjától
  gyűlik. A telephelyi `ar_tortenet` régebbi sorait **nem** töltjük fel
  *(ÁRA, ha mégis kell: egy egyszeri feltöltő lépés — de akkor a vesztesek
  ott is hiányoznak, mert a telephelyen csak az audit-láncban vannak)*.
* **A felhőből írás** — ár, név, áfa a felhős Zigguratból. Ez külön szelet; ez
  a terv csak azt biztosítja, hogy amikor elkészül, legyen mire írnia.
* **A lánc-szintű közös ár**, ami több telephelyre megy le.
* **Az óraeltérés** vállalt kockázat marad: a sorrendet két gép fali órája
  dönti el. A felhő a jelentett óraállásból az eltérést már most jelzi.

---

## 5. Döntést igénylő kérdések

### 5.1 Ellenőrizze-e a felhő, hogy az írónak AKKOR volt-e joga?

A hozzáférés-változásoknál eldöntöttük: *„késleltetéssel jogot szerezni nem
lehet”* — a felhő az offline tett változtatásnál megnézi, hogy a cselekvőnek
**akkor** megvolt-e a joga. Ugyanez itt: egy offline gépen egy olyan
alkalmazott is átírhat árat, akitől a felhőben időközben elvették a jogot.

| | Ellenőrzi | Nem ellenőrzi |
|---|---|---|
| Mit nyerünk | ugyanaz a szabály, mint a hozzáférésnél; a visszavont jog nem kiskapu | egyszerűbb; a telephely a saját másolata szerint már ellenőrzött |
| **ÁRA** | ha a felhő utólag elutasítja, a telephelyen **már élt** az ár — vissza kell állítani, és **az addigi eladások azon az áron maradnak** (a bizonylat nem módosítható) | egy megvont jogú ember offline árat írhat, és az a felhőben is érvényes lesz |
| Munka | kicsi: a „megvolt-e akkor” kiértékelés már megvan (jogosultság-napló) | nulla |

**`[ELDÖNTVE 2026-09-24]` Ellenőrzi** — és az elutasításnál a felület mondja ki, hogy a
közben történt eladások a régi szabály szerint rendben vannak. A hozzáférésnél
ugyanezt a szigort választottuk, és egy ár pénzügyileg nem kisebb tét.

### 5.2 Az első szelet mit fedjen le?

**`[ELDÖNTVE 2026-09-24]`** A **teljes katalógus** kezdeti feltöltése *(kategória, termék,
kiszerelés, vonalkód)*, és a módosításoknál **csak az ár**, mert ma csak azt
lehet a telephelyen szerkeszteni. **ÁRA:** a név/áfa/állapot szerkesztése, ha
a telephelyen elkészül, a kimenő sorba is be kell kötni — ezt a telephelyi
szerkesztés elkészülésénél kötelező pontként kell felvenni.

### 5.3 Automatikus-e a kezdeti feltöltés?

**`[ELDÖNTVE 2026-09-24]` Igen**, az első sikeres kapcsolódáskor, magától. **ÁRA:** egy
nagy katalógusnál az első kör hosszabb — ezért a feltöltés **lapozva** megy,
körönként legfeljebb néhány száz tétel, ahogy a lefelé menő irány is.

---

## 6. A darabok, sorrendben

| # | Darab | Érinti |
|---|---|---|
| 1 | **Szinkron-kisverzió** *(`szinkron/1.4.0`)*: felküldött tételek a lekérdezésben, kimenet tételenként | docs |
| 2 | **Telephely:** kimenő sor (migráció), bekötés az árírásba, kezdeti feltöltés, felküldés | backend `szerver` |
| 3 | **Felhő:** elbírálás, beírás, visszhang nélkül | backend `felho` |
| 4 | **Írás-történet** mindkét oldalon (két migráció) | backend |
| 5 | **Admin-kisverzió** *(`admin/1.6.0`)*: `arElozo`, `arElveszett` | docs, backend |
| 6 | **A Ziggurat** kijelzése | ez a felület |

Az 1–3. darab **önmagában is értékes**: megszünteti, hogy a felhős Ziggurat
csendben mást mutat. A 4–6. erre épül.

### 6.1 Az 1–3. darab — ami megépült *(2026-09-24)*

✅ `szinkron/1.4.0` · felhő: elbíráló + V6 (idempotencia) · telephely: V28
(kimenő sor, triggerek, kezdeti feltöltés) + felküldés a körben.

**Élő próba, két valódi kiszolgálóval** *(a fejlesztői adatbázisok másolatán)*:

| Lépés | Eredmény |
|---|---|
| Első kör | a teljes katalógus felment (5 termék, 5 kiszerelés), a felhős Ziggurat ugyanazt mutatja |
| Ár átírása a telephelyen, a felhő által **nem ismert** íróval | helyben azonnal 850, a felhő `ELUTASITVA` / `NINCS_ILYEN_FELHASZNALO`, **13 mp-en belül visszaállt 820-ra** |
| Jog kiosztása a felhőben → lejön → az író átírja | 880 mindkét oldalon, eredet: `telephely`; **visszhang nincs** |

⚠️ **Amit a próba NEM fedett, és csak teszt védi:** a `ZAROLT` és az
`ELAVULT` kimenet, a megvonás előtti jóhiszemű írás, az újraküldés.

⚠️ **Két ismert korlát:**
* Ha egy rekord a kötegen **túli** új kategóriára hivatkozik, a felhő
  `HIBAS_TETEL`-lel utasítja el; a rekord a következő módosításakor megy fel
  újra. Ritka, de nem nulla.
* A telephely a **beszerzési árat** és a termék NTAK-kódjait **nem** küldi fel —
  a felhős táblában nincs helyük. A felhős árrés-riport előtt pótolni kell.
