# HOZZÁFÉRÉS — ki mit érhet el, és miért éppen úgy

**Készült:** 2026-09-23
**Mi ez:** a **kötelező érvényű** leírás arról, hogy a Siduriban hány különböző
felhasználó-populáció van, melyik hol él, ki szerkesztheti, és milyen szabály
korlátozza. A jogosultságkódok **katalógusa** nem itt van, hanem a
`JOGOSULTSAG_KATALOGUS.md`-ben — ez a dokumentum a **szerkezetről** szól.

> ⚠️ **Ez a fájl döntéseket rögzít, nem javaslatokat.** Ütközésnél a
> `NYITOTT_KERDESEK.md` nyer; ami ott nincs benne, arra ez a hiteles.

---

## 0. A termék neve

A webes admin felület neve **`Ziggurat`** *(angol írásmód, ez a hivatalos)*. A
magyar `zikkurat` alak **átirányítás**, nem önálló név. A **kódban** a
tartományi szókincs magyar marad — a terméknév angol, ahogy a `Siduri` is.

**Miért ez a név:** a Siduri a Gilgames-eposz kocsmárosnője; a zikkurat
mezopotámiai **lépcsős torony**. Ugyanaz a világ — és a lépcsős szerkezet
történetesen pontosan leírja azt, ami ebben a dokumentumban áll: **szintekbe
rendezett jogosultság**, és egy központ, ami a telephelyek fölött áll.

---

## 1. HÁROM populáció van, nem kettő

Ez a dokumentum legfontosabb mondata. A három nyilvántartás **külön** él, és a
szabályaik **nem ugyanazok**.

| | **① Pultos felhasználó** | **② Bérlői Ziggurat-fiók** | **③ Siduri kollégafiók** |
|---|---|---|---|
| **Ki ő** | pultos, pincér, üzletvezető a pult mögött | tulajdonos, irodista, könyvelő, területi vezető | a mi munkatársunk |
| **Hol él a rekordja** | **a felhőben** (gazda), a telephelyen másolat | a felhőben, a bérlő sémájában | a felhőben, a **bérlőkön kívül** (`kozos` séma) |
| **Mivel azonosít** | azonosító + PIN (vagy RFID) | felhasználónév + jelszó | felhasználónév + jelszó |
| **Hol lép be** | pult (telephelyi gép) | Ziggurat | Ziggurat |
| **Jogosultsági modell** | **szintezett szerepek** (hierarchia) | **felhasználónkénti jogok** + sablon | **jogkör** (élő) + egyedi kapcsolók |
| **Hatóköre** | üzletenként más szerep lehet | hatókörönként más jog lehet | bérlőkön átnyúló |
| **Ki szerkesztheti** | Ziggurat **és** pult | **csak** Ziggurat | csak Ziggurat (a Szuperadmin: csak adatbázisból) |
| **Offline** | működnie kell | nem értelmezhető | nem értelmezhető |

**Ugyanaz az ember lehet ① és ② is** — például egy kis helyen dolgozó
üzletvezető, aki reggel PIN-nel nyit műszakot, délután a böngészőben árat ír.
Ilyenkor a két fiók **összekapcsolható** (lásd §6).

> ⚠️ **AMI SZÓHASZNÁLAT, DE FONTOS:** a belső felületen az „adatbázis" szó egy
> **bérlőt** jelent. Technikailag **nem** külön adatbázis, hanem külön **séma**
> egy adatbázison belül (`B7` döntés). A dokumentáció a **bérlő** szót
> használja; a belső képernyőkön „cég / adatbázis" néven jelenhet meg.

---

## 2. ① A pultos felhasználók — szintezett hierarchia

### 2.1 A gazda a felhő

**DÖNTÉS (2026-09-22):** a pultos nyilvántartás **gazdája a felhő**. A
telephelyi szerveren **csak a saját üzlet** felhasználói élnek, **másolatként**,
hogy internet nélkül is legyen belépés a pult mögött.

**Miért:** enélkül nem lehet egy több üzletben dolgozó embert egy helyen
kezelni, és nem lehet egy üzlet gépéből globálisan intézkedni (§7).

**ÁRA, kimondva:**
* a telephelyi szerver **elveszíti a teljes önállóságát** a felhasználók terén;
* új pultost offline **fel lehet venni** helyben, és később felmegy — de a
  nyilvántartás igazsága a felhőben van;
* ⚠️ **az ütközésfeloldás szabálya NEM a törzsadaté.** A mezőnkénti időbélyeg
  (`O3`, a későbbi írás nyer) egy árnál jó, egy **jogosultságnál veszélyes**:
  óraeltérés miatt egy visszavont jog „feltámadhatna". **A MEGVONÁS MINDIG
  NYER**, időbélyegtől függetlenül — ugyanaz az elv, mint a zárolásnál
  (`B16.3`).

### 2.2 A szintek

A pultos szerepek **erősségi sorba** rendezettek. A szint **szám**, és **egy
szinten több szerep is állhat** — így nem kell eldönteni értelmetlen
kérdéseket (*erősebb-e a könyvelő a pultfőnöknél?*).

| Szint | Ki | Megjegyzés |
|---|---|---|
| **0** | **Siduri rendszergazda** | mindenhez hozzáfér, **elvehetetlenül**; a hierarchia teteje |
| 1 | tulaj | |
| 2 | üzletvezető | |
| 3… | pultfőnök, pultos, … | egy szinten több szerep is lehet |

### 2.3 A hierarchia szabályai

1. **Felfelé semmi nem megengedő.** Az üzletvezető a tulajtól **nem vehet el**
   semmit.
2. **Azonos szinten igen.** Egy üzletvezető lefokozhat egy másik üzletvezetőt —
   de csak olyan jogot adhat/vehet el, **amivel maga is rendelkezik**.
3. **Maga fölé senkit nem emelhet**, legfeljebb a saját szintjére.
4. **A jelszóváltoztatás joga is hierarchikus** — az üzletvezető nem írhatja át
   a tulaj jelszavát.
5. **A szintet ÜZLETENKÉNT mérjük.** Aki Sopronban üzletvezető, Pécsett meg
   pultos, az Pécsett nem fokozhat le egy pécsi üzletvezetőt.

### 2.4 Öröklés felfelé

**Ha egy szint új jogot kap, minden felette álló is megkapja.**

Két kikötéssel, mert enélkül csendes lenne:

* ⚠️ **Számoljuk, ne másoljuk.** Az öröklés **levezetett** (lekérdezéskor
  számolt), nem bemásolt sorok. A másolás első ránézésre egyszerűbb, de egy
  későbbi módosításnál a másolatok ottmaradnak, és a rendszer olyan jogot ad,
  amit **senki nem lát sehol**.
* **Látszódjon, hogy örökölt.** A szerep képernyőjén meg kell jelennie, hogy egy
  jogot alacsonyabb szintről **örököl** — különben a „ki adta ezt neki?"
  kérdésre nincs válasz.

**KÖVETKEZMÉNY, kimondva:** ebben a modellben **nem lehet olyan jog, ami egy
alacsonyabb szintnek megvan, a magasabbnak meg nincs**. Vendéglátásban ez
rendben van. *(Ahol nem: pénzügyi rendszerek, ahol a jóváhagyó és a rögzítő
szándékosan külön ember — ezt az utat ezzel lezártuk.)*

Ez egyben **eltérés** a fehérlista alapszabályától („az új jogosultság alapból
tiltott"): itt egy alacsony szinthez adott jog **automatikusan** felfelé
terjed. Ezért kell a látható jelölés.

---

## 3. ② A bérlői Ziggurat-fiókok — nincs szerepkör

**DÖNTÉS (2026-09-22):** a Ziggurat bérlői oldalán **nincs szintezés és nincs
szerepkör**. Felhasználónként állítjuk a jogokat, és legfeljebb **sablonok**
vannak.

**Miért:** az irodista, a könyvelő és a területi vezető nem rendezhető egy
sorba — a rangsor ott értelmetlen összehasonlításokat kényszerítene ki.

### 3.1 A sablon nem szerepkör

⚠️ **A sablon EGYSZER másolódik** a felhasználóra, onnantól a kettő
**független**. Ha később átírod a sablont, a **meglévő** felhasználók nem
változnak.

* Ez így helyes: a szerepkör élő kapcsolat lenne, a sablon nem.
* **A felületen ki kell írni**, különben mindenki azt hiszi, hogy visszamenőleg
  hat.
* **Van „visszaállítás sablon szerint" gomb** — ha egy felhasználó beállítása
  nagyon elment, egy kattintással vissza lehet vinni a sablon állapotára.

### 3.2 Itt nincs „lefokozás"

Szintek híján a „nem emelhet maga fölé" szabály értelmét veszti. Marad a másik:
**csak azt adhatod/veheted, amid van**. Ebből következik, hogy a bérlői
Ziggurat-oldalon **nincs lefokozás fogalma** — csak jogok hozzáadása és
elvétele. A felületet is így kell megfogalmazni.

---

## 4. ③ A Siduri kollégafiókok — jogkör, élő kapcsolattal

Ezek a fiókok **a bérlőkön kívül** élnek, és **minden bérlő minden adatához**
hozzáférhetnek (a jogkörüktől függően).

### 4.1 Jogkör — és ez MÁS, mint a bérlői sablon

| | **Jogkör** (belső, ③) | **Sablon** (bérlői, ②) |
|---|---|---|
| Kapcsolat | **élő**: a jogkör módosítása a viselőkre is hat | **egyszeri másolat** |
| Elvétel | a jogkör adta jogot **egyedileg nem lehet elvenni** — csak a jogkör módosításával vagy elvételével | bármi elvehető egyedileg |

⚠️ **Két különböző dolog, ezért két különböző szó.** A felületen belül
**jogkör**, a bérlőnél **sablon** — egy szó két jelentéssel garantáltan
félreértés lenne.

**A jogkörön FELÜL lehet egyedi jogot adni**; amit a jogkör ad, azt egyedileg
nem lehet elvenni.

### 4.2 A belső rangsor

| Rang | Hogyan kapható | Mit ér |
|---|---|---|
| **Szuperadmin** | ⚠️ **kizárólag adatbázisba írva** — a felületen nem osztható | mindenhez hozzáfér |
| **Manager** | a felületről osztható (ez a legmagasabb kiosztható) | mindenhez hozzáfér, egy fokkal a Szuperadmin alatt |
| minden más jogkör | a felületről osztható | a kapcsolói szerint |

A Szuperadmin és a Manager alatt a többi jogkör között **nincs rangsor**.

### 4.3 Minden képesség külön kapcsoló

Az adminisztratív lehetőségek **egyenként** kapcsolhatók — például:
idegen bérlőbe belépés · új bérlő regisztrálása · a Siduri-hozzáférések
naplójának megtekintése · stb. Kiosztani először a **Szuperadminok** tudnak,
később a **Managerek** (ez maga is egy kapcsoló, nem a rang neve).

### 4.4 Négy szem elv a Managereknél

* **Kettőnél kevesebb Manager nem lehet.**
* Egy Manager a másikat **csak egy harmadik beleegyezésével** törölheti.
* **Határeset:** ha **pontosan két** Manager van, akkor egyik sem törölheti a
  másikat (nincs harmadik) — ilyenkor csak **Szuperadmin** tudja.

⚠️ Ez **munkafolyamat, nem szabály**: kell hozzá egy *függőben lévő kérelem →
jóváhagyás → végrehajtás* lánc. Külön darab.

### 4.5 Amit NEM kapnak — és ennek ára van

**DÖNTÉS:** a belső kollégafiókokhoz **egyelőre nincs második tényező**, elég a
felhasználónév + jelszó.

> ⚠️ **VÁLLALT KOCKÁZAT:** egyetlen kiszivárgott kollégajelszó **az összes bérlő
> összes adata**, interneten elérhető felületen. Ezt a döntést tudatosan
> hoztuk, és **újra elő kell venni**, mielőtt élő bérlői adat kerül a felhőbe.

---

## 5. A közös szabályok — a „burok"

Ez a két szabály **mindhárom populációra** érvényes, ahol értelmezhető:

1. **Csak azt adhatod, amid van.** A kezelt jogok halmaza nem lehet nagyobb,
   mint a műveletet végzőé.
2. **Csak azt veheted el, amid van.** ⚠️ Ez a szabály a leggyakrabban
   felejtődik el, és **nem több joggal sül el, hanem bénítással**: enélkül egy
   szűk jogú adminisztrátor **kizárhatja a lánc vezetőjét**.

**Mikor mérünk:** a **művelet pillanatában**. Ha később elvesznek tőlem egy
jogot, a korábban általam kiosztott szerepek **megmaradnak** — a visszamenőleges
érvénytelenítés azt jelentené, hogy egy vezetőcsere után emberek tucatjai esnek
ki, anélkül hogy bárki hozzájuk nyúlt volna.

**Mihez képest:** a **tényleges** jogosultsághalmazhoz, **hatókörönként**.

**Ami ebből ingyen jön:** magamnak sem tudok többet adni — nem kell külön
szabály rá.

### 5.1 A felületen ne rejtsük el, amit nem adhat

**Látszódjon, de ne legyen választható, és mondja meg, miért.** A rejtés azt
üzeni, hogy „nincs ilyen szerep", és a felhasználó keresni fogja. Ugyanaz az
elv, mint a zárolt árnál (`B16.3`).

### 5.2 Kizárás elleni védelem — kóddal, nem szabályzattal

1. **Magadat nem tilthatod le**, és a saját utolsó felhasználókezelő jogodat nem
   veheted el magadtól.
2. **Az utolsó aktív, felhasználókezelő joggal bíró fiók** nem tiltható le és nem
   fosztható meg ettől a jogtól — **hatókörönként**. Enélkül a bérlő nem tud
   több embert felvenni, és nem érti, miért.

### 5.3 Személyre szabott eltérés — a felhasználó az erősebb

A szereptől/sablontól felhasználónként el lehet térni **mindkét irányba**:

* a szerep **engedné**, de a felhasználónál tiltva van → **tiltott**;
* a szerep **nem adja**, de a felhasználónál engedélyezve van → **engedett**.

*(A ③ jogkör ez alól kivétel: amit a jogkör ad, azt egyedileg nem lehet
elvenni — lásd §4.1.)*

### 5.4 „Törlés" = letiltás

**Fizikai törlés nincs, sehol.** A kilépett dolgozó letiltott állapotba kerül; a
napló és a korábbi adat érintetlen marad. **A felületen ne legyen „törlés"
gomb**, csak letiltás — különben a korábbi árváltozások mellől eltűnik, ki
csinálta.

### 5.5 Abszolút jogosultságkezelés — a kiskapu

Egy **felhasználói beállítás**, ami felmentést ad **mindkét** burok-szabály alól
*(a „csak azt adhatod, amid van" és a „nem emelhetsz magad fölé" alól is)*.

* A **0. szint** elvehetetlenül birtokolja, és **ő adhatja/veheti**.
* Az **1. szint** alapból megkapja, de **kikapcsolható**.
* **Magának senki nem tudja bekapcsolni** — a „csak azt adhatod, amid van"
  szabály ezt eleve kizárja.
* Aki rendelkezik vele, **koronát** kap az ikonjára — a felhasználólistában is,
  nem csak a saját lapján. Ez az **egyetlen** vizuális jel arról, kinél van a
  főkulcs.

---

## 6. A két fiók összekapcsolása (① ↔ ②)

* A Zigguratból lehet egy bérlői fiókhoz **pultos fiókot is létrehozni**,
  kapcsoltan.
* Pultos fiók **bérlői fiók nélkül is** létrehozható.
* ⚠️ **Letiltáskor a rendszer RÁKÉRDEZ**, hogy a kapcsolt másikat is tiltsa-e —
  **mindkét irányban**. **Nem dönt helyettünk, de nem is hallgat.**

**Ára:** a kapcsolatot valakinek be kell állítania, és a rendszer **nem** tiltja
le automatikusan a másikat — csak figyelmeztet.

---

## 7. Hatókör — típus + azonosító

A jogosultság hatóköre **nem csak telephely**:

| Típus | Mi ez |
|---|---|
| **telephely** | egy üzlet |
| **raktár** | adminisztratív készlethely, **gép nélkül** |
| **globális** | a bérlő egésze |

⚠️ **Ezt MOST drótozzuk be**, noha a raktár maga később épül meg — így a raktár
bevezetése **adat lesz, nem adatmodell-műtét**. Egy későbbi átállás minden
bérlő minden kiosztását érintené.

### 7.1 Globális szerkesztés a pultból

* **Új jogosultság:** globális felhasználószerkesztés.
* **Hálózatot igényel:** a globális oldal net nélkül **meg sem nyílik**, hanem
  megmondja, miért.
* **A globális lista nem tárolódik a gépen** — a szerkesztés idejére lekérjük,
  változáskor visszaküldjük.
* **Együzletes ügyfélnél nincs globális oldal** — fölösleges és zavaró lenne.
* **A leggyengébb szint számít:** globálisan csak azt teheti meg, amit **minden
  érintett üzletben** megtehetne.

---

## 8. A Siduri-hozzáférés a pulthoz

### 8.1 A kód

**7 számjegy: 4 forgó + 3 személyes.**

| Rész | Hossz | Tulajdonság |
|---|---|---|
| forgó | 4 | **globális**, havonta cserélődik; az **előző havi is érvényes** |
| személyes | 3 | **kollégánként állandó**, a naplóban ez azonosít |

**Miért így:**
* A kolléga **egy** dolgot tart fejben állandóan (a sajátját), és havonta egyet
  tanul — így a helyek nagy részét fejből lefedi.
* A teljes tér **10 millió** kombináció (a korábban tervezett 6 jegy egymilliója
  helyett).
* Egy **kilépő kolléga magától kiesik**, amint a forgó rész cserélődik.

**ÁRA, kimondva:**
* Az érvényességi ablakon belül **egy kód nyit minden ügyfelet**, és az előző
  havi elfogadása ezt **két hónapra** nyújtja.
* A **személyes rész nem forog**: aki egyszer ellesi, annak az véglegesen
  megvan.
* ⚠️ **Az attribúció visszafelé is működik:** ha valaki egy kolléga három
  számjegyét használja, a napló **azt a kollégát** mutatja. Az azonosítás ezért
  **gyengébb bizonyíték, mint amilyennek látszik** — egy későbbi vizsgálatnál ezt
  figyelembe kell venni.

### 8.2 A rejtett, néma belépés

* **Gesztus:** a bejelentkező képernyőn **3 érintés a logón 5 másodpercen
  belül**. Nincs rá semmilyen vizuális visszajelzés.
* **Néma beütés:** a számbillentyűzet **semmit nem jelez** — se csillag, se
  karakterszám, se billentyű-animáció.
* **Nincs enter:** a **hetedik** számjegynél magától indul. Ha nem stimmel,
  **nem történik semmi**.
* **10 másodperces ablak**, utána a lehetőség megszűnik.
* **Kikapcsol**, ha közben bárki felhasználót választ (akár ugyanazt).
* **A néma mód csak a Siduri-belépésre vonatkozik.** A pultos kollégák PIN-je
  marad a normál visszajelzéssel — ott a rejtettség nem cél, a visszajelzés
  hiánya csak hibázást szülne.

**A billentyűzet gombjai:** törlés (egy karakter), clear (teljes mező), enter.
Néma módban ezek is visszajelzés nélkül működnek — a **clear** az, amivel egy
elrontott beütést el lehet dobni **elküldés nélkül**.

> ⚠️ **Amit ez nem ad:** a gesztus **nem titok**, csak nincs kiírva. Aki egyszer
> látta egy támogatási munkamenetben, tudja. A valódi védelem a kód és a
> korlátozás. A rejtettség haszna az, hogy a fiók **nem jelenik meg a
> felhasználólistán** — tehát egy támadó nem is tudja meg, hogy létezik.

> ⚠️ **A SZERZŐDÉSBEN LE KELL ÍRNI**, hogy a szállító támogatási hozzáféréssel
> rendelkezik. Egy biztonsági átvizsgálásnál a **dokumentálatlan** rejtett
> belépés **hátsó kapunak** minősül — akkor is, ha jogos. Ha a szerződés
> kimondja, akkor csak a **képernyőről** van elrejtve, nem az ügyfél elől.

### 8.3 Próbálkozás-korlátozás — zárolás helyett növekvő várakozás

`1 → 2 → 4 → 8 → 16 → 32 → 64 → 128 → 256` másodperc, onnantól **marad 256** a
helyes belépésig.

**Miért nem zárolás:** a zárolás **ellenünk** fordulna — bárki elronthatná
ötször, és a fiók zárva lenne **pont akkor**, amikor ki kell mennünk javítani.
A növekvő várakozás lassítja a próbálkozót, de nem zár ki.

*(256 másodperc „pont egy cigi", ha a kolléga akkor ér oda, amikor rosszal
próbálkoznak.)*

### 8.4 A bérlő nem tilthatja le — de látja

* A támogatási hozzáférést a bérlő **nem tilthatja le**.
* **Látja**, mert a belépett felhasználó ki van írva — ott a Siduri-fiók is
  megjelenik.

### 8.5 A napló

**Amit rögzítünk:** hol, melyik gépen, **melyik kolléga** (a 3 számjegyből),
mikortól meddig.

* ⚠️ **Helyben írjuk, és felküldjük**, amikor van net. Offline gép nem tud
  jelenteni, ezért a Zigguratban látszania kell, **mikor jelentett utoljára** az
  a gép — különben egy néma gép „tisztának" néz ki, pedig csak nem szól.
* ⚠️ **A meglévő láncolt auditnaplóba kerül**, nem külön táblába. Aki belépett,
  az mindenhez hozzáfér — a saját nyomát is elfedhetné; a láncból a
  visszamenőleges törlés kiderül.
* **Időkorlát a munkamenetre**, hogy ne maradjanak örökké nyitott bejegyzések
  (ha a kolléga csak becsukja a gépet).
* A Zigguratban **külön képernyő**: szűrés, rendezés, keresés.

### 8.6 Későbbi irány

RFID vagy fizikai kulcs a Siduri-fiókhoz. ⚠️ Megjegyzés előre: az **olcsó
RFID-kártyák másolhatók** — ha ide eljutunk, **biztonsági kulcs (FIDO2)**
érdemesebb: ugyanaz a kezelői élmény, de nem klónozható.

---

## 9. Bejelentkezés a Zigguratba

* **Felhasználónév + jelszó.**
* A felhasználónév **tartalmazza a hovatartozást**: `<bérlő>.<név>` —
  például `kiskocsma.Pista`. Az előtag a **bérlő** (cég) rövid neve, **nem** a
  telephelyé.
* **E-mailes meghívó**: a felvett felhasználó a megadott címre kap regisztrációs
  levelet.
* **Levélküldés:** SMTP-n, a MythSystems domainjéhez tartozó feladócímmel.
  ⚠️ **Ára:** a kézbesíthetőséghez a domain levélbeállításait (SPF, DKIM, DMARC)
  be kell állítani — enélkül a meghívók **levélszemétbe** kerülnek, és ez nem a
  kódon fog múlni.
* **Jelszószabályok és az „elfelejtettem" út** a bejelentkezés-szelettel készül:
  minimum hossz **igen**, kötelező lejárat **nem** *(az bizonyítottan gyengébb
  jelszavakhoz vezet)*.

---

## 10. A felhasználó ikonja

Minimálisan testreszabható **emberke**, **deréktól fölfelé**.

| Jellemző | Választék |
|---|---|
| bőrszín | 3 |
| alak | 2 *(a „női/férfi" megjelenés)* |
| haj | 4: kopasz, rövid, vállig érő, hosszú |
| szemszín | 5: kék, zöld, barna, fekete, szürke |
| ruha | öltöny, ing, póló *(+ dressz a női alaknál)* |

* **Rétegezett, színezett vektorrajz**, kódban. 480 kombináció képként
  kezelhetetlen lenne — és így teljesül az is, hogy **futásidőben nincs külső
  hívás** (nincs letöltött ikonkészlet).
* ⚠️ **Az „alak" megjelenési beállítás, nem a dolgozó neme.** Ha a dolgozó
  nemeként tárolnánk, az **személyes adat** lenne, külön indoklási
  kötelezettséggel. Ugyanaz a képernyő, ugyanannyi választék, kevesebb
  kötelezettség.
* **Kezdőbetűs tartalék:** aki nem állít be semmit, annál a neve két betűje
  jelenik meg — különben negyven dolgozó egyformán nézne ki.
* **Korona** annak, akinél az abszolút jogosultságkezelés be van kapcsolva
  (§5.5).

### 10.1 A lista

* **Ábécésorrend**, és egy gomb, ami **csökkenőre** fordítja.
* **Betűre ugrás** fizikai billentyűzetnél: egy betű megnyomása az első olyan
  kezdőbetűs felhasználóra ugrik, ismételt megnyomás a következőre. Nyilakkal is
  léptethető.
* ⚠️ **Keresőmező is kell**, és az az elsődleges: a pultban jellemzően
  **érintőképernyő** van billentyűzet nélkül, ott a betűugrás nem működik.

---

## 11. Raktár és Pult — amit most rögzítünk

Ezek a fogalmak a **készlet** fázisához tartoznak, de két döntés **már most**
megszületett, mert a hozzáférési modellt érinti.

### 11.1 Pult

A **Pult** **logikai csoport**, amihez **több gép is tartozhat**. Nem azonos az
**eszközzel** *(amihez a bizonylatszámozás kötődik)*.

Egy telephelyen több Pult lehet; a Pult előre meghatározott **raktárakból**
vonja az árut.

### 11.2 Raktár

* **Adminisztratív elem, gép nélkül.** Alapanyagot, félkész vagy kész terméket
  tárol; az adminisztrációja a Zigguratban történik.
* Lehet maga a telephely is raktár — de **valahonnan mindenképpen vonni kell**.
* Lehet olyan raktár, ahonnan **nincs közvetlen értékesítés** *(csak más
  raktárakat tölt, vagy csak ide érkezik az áru)*.
* Később ide tartozik: leltár, részleltár, bevételezés, kivételezés,
  átvételezés, fogyás leírás, és a teljes körű, személyre szabható, letölthető
  statisztika.

### 11.3 ⚠️ A több telephelyet kiszolgáló raktár — DÖNTÉS: felosztott alraktár

Rögzítve van, hogy **a mennyiségi állapot kizárólag telephely-autoritatív**
(`B16.4`), mert egy futó egyenlegnek **nem lehet két gazdája**. Egy több
telephelyet kiszolgáló közös raktár ezt megszegné: két üzlet, rossz nettel,
ugyanabból a készletből — és hétfőn mínusz tizenhét üveg.

**A választott megoldás:** a közös raktár **adminisztratív szinten közös**, de
**telephelyenkénti alraktárakra** van osztva. A Pult **mindig a sajátjából**
von, offline is.

**Ára:** a „közös készlet" valójában **felosztott** készlet — a felosztást
valakinek intéznie kell.

*(Az elvetett utak: **felhő-autoritatív** közös raktár → net nélkül megáll a
pult; **nincs közös raktár** → csak átvételezéssel lehet áttolni.)*

---

## 12. A megvalósítás sorrendje

1. **A hozzáférési modell a felhőben** — szintek, hierarchia-szabályok, burok,
   személyre szabott eltérés, 0. szint, típus+azonosító hatókör.
2. **Bérlői Ziggurat-fiókok kezelése** — felhasználónkénti jogok, sablonok,
   sablon-visszaállítás.
3. **A pultos nyilvántartás átköltöztetése** a felhő gazdasága alá, telephelyi
   másolattal.
4. **Pultos fiókok kezelése a Zigguratról**, és az összekapcsolás (§6).
5. **Globális pultos szerkesztés a pultból** (§7.1).
6. **A Siduri-hozzáférés** (§8).
7. **A belső kollégafiókok** (§4), a négy szem elv munkafolyamatával.

---

## 13. Amit ez a dokumentum NEM old meg

| Hiány | Hol dől el |
|---|---|
| A jogosultságkódok **katalógusa** | `JOGOSULTSAG_KATALOGUS.md` |
| A készletkezelés (leltár, bevételezés, …) | a készlet fázisa |
| A raktár mint **entitás** | ugyanott — itt csak a **hatókör** dőlt el |
| A bejelentkezés (jelszókezelés, munkamenet) | a bejelentkezés-szelet |
| A **második tényező** a belső fiókokhoz | elhalasztva — §4.5, vállalt kockázat |
