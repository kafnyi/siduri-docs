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

### 2.1/a Hogyan jut le — PILLANATKÉPKÉNT

A telephely a `POST /hozzaferes` végponton kéri le a saját pultos
felhasználóit *(`szinkron/1.2.0`)*. **Nem változásfolyam**, pedig a K3 többi
része az — mert egy elmaradt növekmény itt azt jelentené, hogy egy **visszavont
jog megmarad**.

* A telephely elküldi, milyen **verziót** ismer *(a tartalom lenyomatát)*; ha
  egyezik, nem jön adat.
* A **szerepek jogai már kibontva** érkeznek *(a szint szerinti örökléssel)* —
  a szabály **egy helyen**, a felhőben él.
* ⚠️ **A PIN nem megy le.** A felhő a személyt és a jogait tartja nyilván; a
  hitelesítés helyi marad.
* ⚠️ **A helyben létrehozott sorokhoz nem nyúlunk.** A telephelyi táblákon
  jelölés van *(`felho_gazdaju`)*; a szinkron csak a saját sorait kezeli.
  Ennélkül az első szinkron kitörölné a telepítéskor felvett felhasználókat —
  vagyis **kizárná a telephelyet saját magából**.
* ⚠️ **Aki kikerül a pillanatképből: LETILTVA, nem törölve.**
* ⚠️ **Ismeretlen jogosultságkód** *(régebbi telephely)*: a jog nem kerül be
  *(fehérlista)*, de a napló **kiírja** — különben a „nincs jogosultságod”
  válasz sehova nem mutatna.
* A telephely tárolja, **mikor frissült utoljára**. Egy néma másolat ugyanolyan
  „rendben” képet mutatna, mint egy friss — pedig lehet, hogy hetek óta nem
  frissült, és egy kilépett dolgozó még mindig be tud lépni a pult mögött.

**Az egyediség populációnként:** a telephelyi szerepnév és felhasználó-azonosító
eddig telephelyenként volt egyedi. A felhőből lejövő szerepek ugyanazokat a
bevett neveket hozzák *(„Pultos”, „Üzletvezető”)*, mint a helyben, sablonból
létrehozottak — ezért az egyediség **két körre** bomlott: a helyiek egymás
között, a felhősek egymás között.

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

**Ha egy szint új jogot kap, minden RANGBAN FELETTE ÁLLÓ is megkapja.**

⚠️ **SZIGORÚAN felette — nem „felette vagy azonos".** Egy szerep megkapja a
**saját** jogait, és minden **szigorúan gyengébb** szintű szerep jogát. Ha az
azonos szint is öröklődne, akkor **egy szinten minden szerep ugyanazt
jelentené** — pedig épp azért engedünk több szerepet egy szinten, hogy a
tényleges különbséget a **jogaik** adják, ne a rangsor. *(Ezt egy teszt fogta
meg: az azonos szintet is beszámító öröklés mellett két azonos szintű szerep
kibontott joga betű szerint megegyezett — vagyis a megkülönböztetésük
elveszett.)*

Két további kikötéssel, mert enélkül csendes lenne:

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

### 4.4/a DÖNTÉSEK a megvalósításhoz *(2026-09-24)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **Felhasználónév** | `siduri.<név>` — ugyanaz a forma, mint a bérlőknél | a `siduri` rövid név **bérlőnek végleg tiltott** |
| **Munka egy bérlő adatán** | **bérlőválasztó**, belépés után; a belépés **naplózódik**, indok nélkül | a naplóból nem derül ki, **miért** lépett be |
| **Az első kapcsolók** | idegen bérlőbe belépés · új bérlő regisztrálása · a hozzáférési napló megtekintése · kollégafiókok kezelése | — |
| **Második tényező** | **továbbra sincs** (lásd 4.5) | a 4.5 kockázata marad |
| **Jog a bérlő adatán** *(a megvalósításkor, kérdés nélkül)* | Szuperadmin és Manager: **minden**; bárki más: **csak olvas** (a `*.megtekintes` jogok) | egy nem vezető kolléga egy ügyfél árát sem javíthatja; ha kell, az **új kapcsoló** lesz, nem csendben kiszélesített olvasójog |
| **A jogkör és a kapcsoló élő** | minden kérésnél újraszámolódik — egy elvett kapcsoló a **nyitott** munkamenetet is azonnal kizárja a bérlőből | kérésenként egy-két plusz lekérdezés |

**Megvalósítva** *(2026-09-24, `admin/1.10.0`)*: belépés `siduri.<név>`-vel,
bérlőválasztó, a belépés a bérlő saját naplójába is bekerül, hozzáférési napló
(a sikertelen próbálkozás is, a nem létező kolléganévre is). **Még nincs:** a
kollégafiókok és jogkörök kezelése a felületről, a négy szem elv, az új bérlő
regisztrálása — addig kollégát és jogkört **adatbázisból** lehet felvenni.

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
* ⚠️ **Kapcsolat csak ZIGGURAT és PULTOS között értelmes.** Két pultos fiók
  összekapcsolása nem „ugyanaz az ember", hanem elgépelés — a csendes elfogadás
  később megfejthetetlen adatot hagyna.

**Aki szint nélküli, arra a pultos rangsor nem vonatkozik — sem célként, sem
cselekvőként.** A tipikus eset: egy **Ziggurat-fiók kezel pultos
felhasználókat**. Őt a **burok** köti *(csak azt adhatja és veheti el, amije
van)*. Enélkül a Ziggurat — ahol a személyzetet kezelik — **egyetlen pultos
fiókhoz sem nyúlhatna**, amint az kap egy szerepet. *(Élő próbán jött elő.)*

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

### 7.2 Offline szerkesztés — helyi érvény, felhős elbírálás

⚠️ **DÖNTÉS (2026-09-23).** A 3. darab óta a pultos nyilvántartás gazdája a
felhő, a telephelyi példány másolat. Ebből az következne, hogy a pultnál
**minden** felhasználó-szerkesztés hálózatot igényel — a globális is, a saját
üzletbeli is. **Ezt elvetettük.**

**Miért:** az egész rendszer alapígérete, hogy a telephely net nélkül is
dolgozik. A kassza megy, az eladás megy, a napzárás megy. Ha pont a
felhasználókezelés esik ki, akkor az a dolog romlik el, amit a legkevésbé
terveztünk elromlani hagyni. A valós eset: a pultfőnök **most** akar sztornó-jogot
adni egy alkalmazottnak, mert a műszakban kelleni fog — és a gép lehet, hogy csak
másnap lesz újra online.

**Amit NEM csinálunk: összefésülést.** A jogosultságon az összefésülés pont az,
amit a 3. darabnál jó okkal utasítottunk el: mezőnkénti időbélyeg mellett egy
visszavont jog **feléledhet**, és ez csendben történik. Helyette:

| Lépés | Mi történik |
|---|---|
| 1. | A változtatás **helyben azonnal él** — a műszak megy tovább |
| 2. | **Külön táblába** kerül, nem a pillanatkép soraiba. A pillanatkép-alkalmazó marad, ami ma: letöröl és újraír, óvatoskodás nélkül. A helyi változtatás **ráfekszik** a pillanatképre, amíg el nem bírálják |
| 3. | Kapcsolódáskor **felmegy**, és a felhő bírálja el |
| 4. | Elfogadva → felhős igazsággá válik. Elutasítva → helyben visszavonjuk, és **kiírjuk, kinél, mit, miért** |

✅ **A felhő oldala megvált** *(2026-09-23)*. **HÁROM kimenet van, nem kettő:**

| Kimenet | Mit jelent | Mi a teendő |
|---|---|---|
| **ELFOGADVA** | A cselekvőnek **akkor** megvolt a joga | semmi |
| **ELUTASITVA** | **Nem volt joga** hozzá — a cselekvőről szól | jogot kérni |
| **ELAVULT** | A központ **időközben döntött ugyanarról** — senkiről nem szól, csak sorrendről | megnézni, mi lett az új érték |

⚠️ **A második és a harmadik nem ugyanaz, és a felületnek külön kell mondania
őket.** Egy közös „nem sikerült" üzenet azt sugallná a pultfőnöknek, hogy
ő rontott el valamit — pedig a harmadik esetben csak megelőzték.

⚠️ **A köteg NEM mindent-vagy-semmit.** Ha a harmadik változtatás elbukik, az
első kettő **attól még jó volt**. Egy közös visszagörgetés azt üzenné, hogy a
napi munka egy hibás sor miatt elveszett — és a javítás előtt nem is derülne ki,
melyik volt az.

⚠️ **Egy elavult változtatás EGÉSZE elavul**, nem csak az ütköző kód. A művelet
a hatókör **teljes** halmazát állítja be; részlegesen alkalmazni annyit
jelentene, hogy egy olyan állapot áll elő, amit **soha senki nem akart** — sem a
pultfőnök, sem a központ.

⚠️ **AMIT NEM BÍRÁLUNK EL IDŐBEN: A RANGSORT.** A **szint** szerinti korlátot a
**mai** állapot szerint nézzük, mert **szinttörténetet nem vezetünk** — a napló
jogosultságokat rögzít, nem rangokat. Tudatos szűkítés: a rang **jelen idejű**
tulajdonság *(„van-e most állása ehhez")*, míg a jogosultság konkrét
felhatalmazás, amit **el lehetett veszíteni**. **ÁRA:** egy időközben
**lefokozott** pultfőnök jóhiszemű változtatása elbukhat. Látható és
megmagyarázható elutasítás, és megismételheti az, akinek most van hozzá állása.

⚠️ **Ez nem összefésülés, hanem jóváhagyásra váró kérés.** Az összefésülés egy
soron két értéket ütköztet; itt egyetlen kérés vár elbírálásra. A második nem
igényel algoritmust — és nincs benne az a hiba, hogy a helyi írás csendben
felülír egy központi megvonást.

**Hol él:** ⚠️ **a telephelyi szerveren, nem a pultban.** „Offline" azt jelenti,
hogy a **boltnak** nincs internete; a pult és a telephelyi szerver között megy a
hálózat, különben a kassza sem működne. A pultban tehát **nulla offline gépezet**
kell. Mellékhaszon: ugyanez jár a **telephelyről kiszolgált Zigguratnak** is,
ingyen.

#### A szabály két fele

⚠️ **A „legfrissebb döntés nyer" önmagában lyukas**, és pont az offline-ban
maradás lenne a kiskapu: aki offline van, a **saját jogának megvonását** is
felülírhatná azzal, hogy később cselekszik. Ezért:

| Mit | Ki dönt | Miért |
|---|---|---|
| **A jogosultság ÉRTÉKE** *(van-e X-nek sztornó-joga)* | **a legfrissebb döntés** | Két írás ütközik ugyanarra; a későbbi tud többet |
| **A CSELEKVŐ joga** *(oszthatta-e egyáltalán)* | **a felhő, a változtatás IDŐPONTJÁRA nézve** | Késleltetéssel jogot szerezni nem lehet |

A második nem szigorúbb, hanem **igazságosabb**: ha a pultfőnök 09:00-kor
osztott, és a központ 10:00-kor vette el a jogát, a 09:00-s osztás **érvényes
marad**. Csak a 10:00 **utáni** cselekvés bukik el. Ehhez kell a §7.3 naplója.

#### Három aszimmetria, ami korlátban tartja

1. ⚠️ **Kifelé mindig, befelé soha.** Letiltani offline **mindig** lehet, és
   azonnal él. **Visszaengedni offline nem lehet:** ha a pillanatkép szerint
   valaki le van tiltva, azt helyben nem lehet feloldani. Szándékosan nem
   szimmetrikus — kijuttatni valakit sürgős lehet, beengedni sosem az.
2. ⚠️ **A hatalmi jogok offline nem oszthatók.** Az **üzleti** jogok mehetnek
   (sztornó, árengedmény, napzárás); a rendszer **fölötti** hatalom nem. A
   lista *(2026-09-23 döntés)*:

   | Kód | Miért nem osztható offline |
   |---|---|
   | `jogosultsag.kiosztas` | Aki ezt offline megkapja, onnantól **bármit** adhat — a rés ki tudja tágítani önmagát |
   | `szerep.kezeles` | Ugyanaz, egy lépéssel odébb: a szerep jogain keresztül |
   | `felhasznalo.globalis` | A helyi rés **minden üzletre** kiterjedne |
   | `felhasznalo.jelszo_csere_mase` | **Nem üzleti művelet, hanem egy út befelé**: aki megkapja, bárki fiókjába beléphet, és onnantól az illető jogaival dolgozik — a burok megkerülése személycserével |

   ⚠️ **A négy közös vonása:** egyik sem egy **üzleti** műveletet enged meg,
   hanem azt, hogy valaki **több jogot szerezzen**, mint amennyi az elbíráláskor
   számon kérhető rajta. Ezért nem elegénségi kérdés, hogy offline eljárhat-e
   velük: a felhős elbírálás **utólag** törli őket, de amit közben csináltak velük,
   az megmarad.
3. **Elévülés NINCS** — kimondott döntés. A licenc **10 napos offline türelmi
   ideje** már korlátozza az ablakot; egy második, szűkebb korlát csak annyit
   érne el, hogy a 8. napon a képernyő érthetetlenül megtagadná a munkát. *(A
   dokumentum egyébként is tiltja az ilyen számok összecsatolását — lásd
   `NYITOTT_KERDESEK.md` B10/b.)*

#### ⚠️ Amit ez NEM old meg — és kód nem is fogja

> Kedden 10:00-kor a központ elveszi Kovács sztornó-jogát, mert gyanús. A bolt
> kedd óta offline. Kedden 14:00-kor a pultfőnök — aki **nem tudhat** a központ
> döntéséről — visszaadja neki. Kovács kedd délutántól szerda reggelig
> **sztornóz**. Szerdán a gép online lesz, a felhő elutasítja a változtatást, a
> jog eltűnik. **A sztornók viszont megtörténtek.**

Ez a maradékkockázat, és **kizárólag az offline ablak hosszával** csökkenthető.
Az audit-lánc rögzíti őket, tehát **észrevehető** — csak nem megelőzhető.
Vállaljuk, kimondva.

---

### 7.3 A jogosultság-napló — ki, mikor, kinek, mit

✅ **Megépült** *(2026-09-23)*.

⚠️ **Eddig erre a kérdésre senki nem tudott válaszolni.** A megvonás egyszerűen
egy törölt sor volt: se időbélyeg, se nyom. Egy olyan rendszerben, aminek a
lényege, hogy megmondja, mi történt, a jogosultság-nyilvántartás volt az
egyetlen hely **történet nélkül**. Ezért az O3 mezőeredet-kötelezettség *(„látszania
kell, mikor és honnan kapta a mostani értékét")* a jogosultságokra
**teljesíthetetlen** volt.

⚠️ **A TÉNYLEGES HATÁST naplózzuk, nem a táblaműveletet.** Egy szerep kiosztása
egyetlen sor, de az örökléssel tíz jogosultságot hozhat magával — és a kérdés
sosem az, hogy melyik sor változott, hanem hogy **mit tud mostantól**. A
táblaműveletet naplózva minden kérdésnél újra ki kellene számolni az öröklést a
**múltbeli** állapotra; így egy indexelt keresés elég.

* Ebből következik, hogy egy **letiltás az összes jogot elvesztettként**
  naplózza. Ez nem zaj, hanem a valóság: a letiltott halmaza üres. Cserébe az
  elbírálónak **nincs külön ága** a letiltásra.
* A **hatástalan művelet nem kerül bele.** Egy „mentés" gomb, ami ugyanazt menti
  újra, nem történés — és ha bekerülne, a napló pont azoknál hízna
  használhatatlanná, akiknél a legtöbbet kattintanak.
* ⚠️ **Csak beszúrható**, adatbázis-szintű triggerrel. Egy napló, amit át lehet
  írni, nem napló — és épp az elbírálásnál lenne a legdrágább: az időpont,
  amihez mérünk, hamisítható lenne.
* Rögzítjük, hogy a döntés a **felhőben** vagy a **telephelyen** született. Egy
  offline tett változtatás elavult jogállás szerint született, és az elbírálás
  kiindulópontja épp ez a tény.

⚠️ **A „megvolt-e neki AKKOR?" kérdésre a MAI állapotból indulunk visszafelé**,
nem a bejegyzésekből előre. Ha csak a bejegyzéseket néznénk, minden korábban
kiosztott jog úgy látszana, mintha soha nem létezett volna — vagyis **a napló
bevezetése maga törölné el mindenki múltját**.

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
3. ✅ **A pultos nyilvántartás átköltöztetése** a felhő gazdasága alá, telephelyi
   másolattal — **kész** *(2026-09-23)*, lásd §2.1/a.
4. ✅ **Pultos fiókok kezelése a Zigguratról**, és az összekapcsolás (§6) —
   **kész** *(2026-09-23, `admin/1.5.0`)*.
5. **Globális pultos szerkesztés a pultból** (§7.1) — **három részre bomlott**,
   mert a pultban **egyáltalán nincs felhasználókezelő képernyő**, és a
   kassza-szerződésben sincs mihez beszélnie:
   * ✅ **5/a — a felhő oldala: KÉSZ** *(2026-09-23)*. Globális kiértékelés
     *(leggyengébb szint, metszet-burok)*, **jogosultság-napló** (§7.3) és az
     **offline elbírálás** (§7.2).
   * **5/b — a telephelyi szerver és a szerződések.** A pulti felhasználókezelés
     végpontjai, az offline átfedő tábla és a felküldés.
   * **5/c — a pult képernyője.** WPF, a helyi lista és a globális fül.
6. **A Siduri-hozzáférés** (§8).
7. **A belső kollégafiókok** (§4), a négy szem elv munkafolyamatával.
   * ✅ **7/a — belépés, bérlőválasztó, napló: KÉSZ** *(2026-09-24, `admin/1.10.0`)*.
   * **7/b — kollégafiókok és jogkörök kezelése**, a négy szem elvvel.
   * **7/c — új bérlő regisztrálása.**

---

## 13. Amit ez a dokumentum NEM old meg

| Hiány | Hol dől el |
|---|---|
| A jogosultságkódok **katalógusa** | `JOGOSULTSAG_KATALOGUS.md` |
| A készletkezelés (leltár, bevételezés, …) | a készlet fázisa |
| A raktár mint **entitás** | ugyanott — itt csak a **hatókör** dőlt el |
| A bejelentkezés (jelszókezelés, munkamenet) | a bejelentkezés-szelet |
| A **második tényező** a belső fiókokhoz | elhalasztva — §4.5, vállalt kockázat |
