# Siduri — Rendszerspecifikáció

**Termék:** Siduri — magyar vendéglátóipari POS és menedzsmentrendszer
**Fejlesztő:** Myth System *(a Siduri a Myth System harmadik terméke, a Garm és a Hermes mellett)*
**A dokumentum állapota:** teljes körű, aktuális specifikáció
**Utolsó frissítés:** 2026-08-23 (3. tervezési munkamenet lezárása után)

---

## 0. Hogyan olvasd ezt a dokumentumot

Ez a fájl **a teljes, aktuális rendszertervet** tartalmazza, emberi olvasásra
szánva. Minden eddigi döntés benne van.

**Amit ez a fájl NEM tartalmaz:** a döntések mögötti **indoklást**, az elvetett
alternatívákat, a vitákat és az önhelyesbítéseket. Azok a
[`NYITOTT_KERDESEK.md`](NYITOTT_KERDESEK.md) fájlban élnek, szakaszokra bontva
(A–L). Ha egy döntés **miértjét** keresed, oda menj.

**Kapcsolódó fájlok:**

| Fájl | Mire való |
|------|-----------|
| [`NYITOTT_KERDESEK.md`](NYITOTT_KERDESEK.md) | A döntések indoklása, az elvetett utak, a viták |
| [`FOLYAMATBAN.md`](FOLYAMATBAN.md) | Aktuális állapot, mi következik, mi nyitott |
| [`MERNOKISAROKKOVEK.md`](MERNOKISAROKKOVEK.md) | Mérnöki sarokkövek — a munkamódszer szabályai |
| [`MERESEK.md`](MERESEK.md) | Mérési kötelezettségek (M1–M18) |
| [`MVP_DEFINICIO.md`](MVP_DEFINICIO.md) | Mi az MVP, és mi nem |
| [`FISKALIS_UZEMMODOK.md`](FISKALIS_UZEMMODOK.md) | A három fiskális üzemmód részletei |
| [`ELLENORZES_1_TELJESSEG_JOGI.md`](ELLENORZES_1_TELJESSEG_JOGI.md) | 1. ellenőrző kör: teljesség és jogi megfelelés |
| [`ELLENORZES_2_ADVERZARIALIS.md`](ELLENORZES_2_ADVERZARIALIS.md) | 2. ellenőrző kör: adverzariális átvizsgálás |
| [`siduri_superprompt_en.md`](siduri_superprompt_en.md) | Ugyanez angolul, gépi feldolgozásra |

**Címkék a szövegben:**

| Címke | Jelentés |
|-------|----------|
| `ALAP` | Az architektúra alapja — nem opcionális, nem halasztható |
| `MVP` | Az első kiadható változat része |
| `v1` | Az MVP utáni első bővítési kör |
| `v2` | Későbbi bővítés |
| `VÍZIÓ` | Irány, nem ütemezett munka |
| `[NYITOTT]` | Még nincs eldöntve |
| `[IGAZOLANDÓ]` | Feltevés, amit forrásból ellenőrizni kell kódolás előtt |
| `[MÉRENDŐ]` | Számot csak méréssel lehet rá mondani |

---

## 1. Fogalomtár

### 1.1 Eszközök és szerepek

| Fogalom | Jelentés |
|---------|----------|
| **POS** | Fizikai, érintőképernyős **vastagkliens** (AIO gép) perifériákkal. Windows. |
| **Vékonykliens** | Telefon vagy tablet (Flutter) a pincér kezében. Rendelésfelvétel. |
| **KDS** | Konyhai kijelző rendszer. |
| **Rendeléskijelző** | Vevőhívó tábla („Készül" / „Átvehető"). |
| **Kioszk** | Önkiszolgáló rendelő és fizető terminál. |
| **Fő szerver** | A telephely autoritatív szervere. Jellemzően egy dolgozó POS gépen fut. |
| **Tartalék szerver** | Készenléti szerver, **mindig egy Windows POS vastagkliensen**. |
| **Tanú** | Olyan gép, amely szavazatot ad abban a kérdésben, elérhető-e a fő szerver. |
| **Felhő** | A Siduri központi platformja: licenc, archívum, webes admin, statisztikák. |

### 1.2 Idő- és napfogalmak

| Fogalom | Jelentés |
|---------|----------|
| **MUNKANAP** | A **telephely** üzleti napja. Nem naptári nap. Egy naptári dátumra több is nyitható. Felső határa **23 óra 45 perc**. |
| **MŰSZAK** | **Eszközönkénti** fogalom — az adott pénztárgép adóügyi munkanapja. Egy MUNKANAP-on belül több MŰSZAK lehet, gépenként és felhasználónként. |
| **NTAK tárgynap** | Az NTAK adatszolgáltatás napfogalma. **A nyitás dátumából származik**, tehát gyakorlatilag megegyezik a MUNKANAP-pal. **Nem naptári nap.** |
| **Naptári nap** | A falinaptár napja. Csak megjelenítésre és néhány jogi időbélyegre. |

### 1.3 Működési állapotok

| Fogalom | Jelentés |
|---------|----------|
| **Normál üzem** | A kliens eléri a szervert, minden integráció él. |
| **Csökkentett mód** | Gyűjtőfogalom két okra: **(a)** a kliens nem éri el a szervert (degradált / gyorseladás mód), **(b)** egy védett integráció ideiglenesen ki van kapcsolva. A személyzet egy mintát tanul meg, két alfajjal. |
| **Degradált mód** | A kliens nem éri el sem a fő, sem a tartalék szervert. Gyorseladás helyi outboxba. |
| **Vészhelyzeti mód** | A tartalék szerver átvette a szolgálatot. |
| **Árva tranzakció** | Olyan tranzakció, amely az egyik szerveren létezik, a másikon nem, mert a replikáció nem érte utol a kiesést. |

### 1.4 Termékfogalmak

| Fogalom | Jelentés |
|---------|----------|
| **Termék** | Eladható tétel. Kötelező főkategóriája, két áfakulcsa és NTAK-besorolása van. |
| **Kiszerelés** | A termék **gyermeke**: saját bruttó ára, saját receptmennyisége, saját térfogata/tömege. Pl. 0,3 l és 0,5 l csapolt sör. |
| **Módosító** | **Mindig eltérés vagy fontos egyedi kérés** az alapállapottól. Az alapállapot a receptúra. |
| **Módosítócsoport** | Módosítók halmaza `min` / `max` / `FreeLimit` szabályokkal. |
| **Menü (összetett termék)** | Termék, amely **menükomponensekből** áll; a nyugtán szétrobban a komponenseire. |
| **Receptúra (BOM)** | A termék alapanyag-összetétele. |

---

## 2. Termékkoncepció

* **Célpiac:** magyar KKV vendéglátás — NTAK-köteles helyek.
* **Fő eladási érv:** **offline-first** architektúra. A rendszer a telephelyi hálózaton működik, és **ellenáll az internetkimaradásnak**; a felhővel utólag szinkronizál.
* **Második eladási érv:** **magas rendelkezésre állás** — tartalék szerver a fő szerver hardverhibája ellen.

> **Fogalmi pontosítás, amit nem szabad összemosni:** az internetkimaradás elleni
> védelmet **a lokális szerver** adja. A tartalék szerver egy **másik, sokkal
> ritkább** esemény ellen véd: a lokális szerver hardverhibája ellen. A kettő
> összemosása a HA-t indokoltabbnak mutatja, mint amennyire az.

### 2.1 Üzleti modell

* **Egygépes, asztalkezelés nélküli használat: ingyenes.** Belépő szint.
* **Fizetős csomagok** a további funkciókra. A csomagok tartalmát az
  **integráció- és funkciónyilvántartás** (§19.5) írja le — ugyanaz a szerkezet,
  ami az integrációk osztályozását is adja.
* A támogatási platform már létezik, nem ennek a projektnek a része.

---

## 3. Tervezési alapelvek

Ezek nem stílusszabályok. Minden konkrét döntés visszavezethető rájuk, és
ütközés esetén ezek döntenek.

| # | Elv |
|---|-----|
| **A1** | **Egy igazságforrás.** Minden más fájl mutató, és a mutató mondja ki magáról, hogy mutató. |
| **A2** | **Néma kudarc nincs.** Ami elromlott, azt látni kell — a felhasználónak, a naplóban, vagy mindkettőben. Csendben elnyelt hiba tilos. |
| **A3** | **Ne mondjuk meg az ügyfélnek, mit akar.** Ahol valós üzleti oka lehet eltérni a számított értéktől, ott a számított érték **egyszeri kitöltő segédlet, soha nem élő hivatkozás**. |
| **A4** | **Másolás, nem hivatkozás.** Ha egy érték átvétele később csendben megváltoztatná a származtatottat, akkor másoljuk, ne hivatkozzuk. |
| **A5** | **A két hibairány nem egyenértékű.** Pl. a túl magas áfa pénzügyi hátrány, a túl alacsony jogsértés. A mechanizmus a **kisebb kár** felé dőljön. |
| **A6** | **A ritkán futó kód élesben hibázik először.** Ahol lehet, olyan utat válasszunk, ami gyakran fut. |
| **A7** | **Minden „ideiglenes" megkerülés állandósul**, hacsak nincs kikényszerített lejárata. |
| **A8** | **A megkerülés felajánlása a megkerülés megtanítása.** A rendszer soha ne kínálja fel magától a kikerülő utat. |
| **A9** | **A hardver adottság, nem választás.** A meglévő J1900-as bázis kényszer; erre kell tervezni, nem ellene. |
| **A10** | **Nincs AI-attribúció** semmilyen commitban, kódban, dokumentumban vagy bizonylaton. |

---

## 4. Technológiai stack és célhardver

### 4.1 Stack

| Réteg | Technológia | Megjegyzés |
|-------|-------------|------------|
| **Backend** | Java (Spring Boot), **GraalVM Native Image** | A natív fordítás **kényszer**, nem optimalizáció — a J1900-as memóriakorlát miatt |
| **Adatbázis** | PostgreSQL | Szigorú memórialimitekkel |
| **POS kliens** | C# / WPF, .NET 8+ | **Kizárólag Windows 10 IoT Enterprise (LTSC).** A Linux-támogatás törölve |
| **Mobil / vékonykliens** | Flutter | PDA, KDS, rendeléskijelző, standoló |
| **Frissítő** | C# önálló segédprogram | A Windows fájlzárolási problémáit kerüli meg |
| **Felhő** | Java vagy Node.js | Licenc, archívum, webes admin |

**Miért nem Avalonia:** megvizsgáltuk és elvetettük. A WPF nem fut Linuxon, de
nem is lesz Linuxos POS, tehát a váltás költsége nem térülne meg.

### 4.2 Célhardver `ALAP`

**A meglévő bázis Intel J1900 (Bay Trail), 64 GB SSD.** A bázis **vegyes**:
ugyanaz a géptípus fut **szerverként és POS kliensként is**.

Ebből következik:

* A GraalVM-kényszer marad.
* **A WPF kliens teljesítmény-költségvetése is szoros** — pl. a 720p-s másodkijelzős videó egy Bay Trail integrált GPU-n nem triviális.
* `[MÉRENDŐ]` **Minden teljesítményszám valós J1900-on mérendő, nem becsülhető** (`MERESEK.md` M1–M3, M12–M14).
* **A CMOS-elem 10+ éves gépeken halott vagy haldoklik.** Ez nem elméleti: a gép órája áramszünet után évekkel korábbi dátumra ugorhat. A rendszernek ezt túl kell élnie (§9.5).

---

## 5. Topológia és telepítési méretosztályok

### 5.1 A méretosztályok AJÁNLÁSOK, nem korlátok `ALAP`

**A szoftver semmilyen konfigurációt nem utasíthat el.** Ha az ügyfél a
kockázat ismeretében másképp dönt, elfogadjuk, és a
**kockázatvállalási nyilatkozat** (§24.4) rögzíti.

| Gépszám | Fő szerver | Tartalék szerver | Adóügyi eszköz |
|---------|-----------|------------------|----------------|
| **1 gép** | **a pénztárgép MAGA a szerver** | nincs | 1 |
| **2–3 gép** | POS-on | **opcionális** | ajánlás: gépenként |
| **4+ gép** | POS-on, vagy dedikált ha megengedheti | **kötelező ajánlás** | **kiemelten: legalább 2** |

**A „nincs tartalék szerver" elsőrangú konfiguráció, nem hibaállapot** — ott
átkapcsolást felajánlani sem szabad.

### 5.2 Szerepkiosztási szabályok `ALAP`

* **A tartalék szerver SOHA nem dedikált gép — mindig egy Windows POS vastagkliens.**
* A fő szerver **jellemzően szintén POS-on** fut; aki megengedheti, annál lehet dedikált gép.
* **Vékonykliens, KDS, rendeléskijelző egyik szerepet sem viheti.**
* Egy gépen futhat **szerver és kliens egyszerre** — támogatott konfiguráció.

**Négy következmény, amit ez okoz:**

1. A tartalék gép terhelése **a legrosszabb pillanatban** ugrik meg — amikor átvesz, épp csúcsidő van.
2. A szerepet vivő gépet **valaki kikapcsolhatja**, mert az számára „csak egy kassza".
3. **A szerver Windows Service kell legyen**, nem a pénztáros munkamenetében futó folyamat.
4. **A frissítés sorrendje kemény követelmény** a `siduri-updater` felé: a szerepeket hordozó gépek nem frissülhetnek egyszerre.

### 5.3 Kliens-felderítés

**mDNS** a telephelyi hálózaton, hogy a kliensek IP-változás után is megtalálják
a szervert. A szerepváltás (§7) mDNS-en keresztül propagálódik.

---

## 6. Szerver-autoritatív modell és degradált mód

### 6.1 Az alapmodell `ALAP`

**Minden megosztott, módosítható állapot a szerveren dől el:** asztalok,
rendelések, készlet, kedvezmények, műszakok, jogosultságok.

A POS gépen **gyorsítótár és tartós, csak-hozzáfűzhető outbox** van —
**nem PostgreSQL replika.** (A korábbi „helyi PostgreSQL replika" terv törölve.)

### 6.2 Degradált mód (gyorseladás) `MVP`

Ha a kliens **sem a fő, sem a tartalék** szervert nem éri el:

* **Gyorseladás lehetséges:** tétel → fizetés → nyomtatás.
* Az események a **helyi outboxba** kerülnek, és visszatéréskor lejátszásra.
* **A nyitott asztalok NEM elérhetők.** A pincér kézzel, gyorseladásként üti fel újra a fogyasztást.

**Miért nem elérhetők az asztalok:** ez tartja meg a *„nincs megosztott
módosítható állapot"* invariánst, amire az egész degradált mód épül. Ha két
gép egymástól függetlenül módosíthatná ugyanazt az asztalt, a visszatéréskori
összefésülés megoldhatatlan lenne.

**Mindhárom rész az MVP-ben van:** helyi napló, degradált felület, visszatéréskori egyeztetés.

`[IGAZOLANDÓ]` **Az egész degradált mód egy premisszán áll:** AEE-s gépnél a jogi
bizonylatot **maga az adóügyi eszköz** állítja ki és sorszámozza, tehát a szerver
kiesése nem akadálya a nyugtaadásnak. **Kódolás előtt igazolandó.**

### 6.3 Minden gép önállóan megy csökkentett módba `ALAP`

A csökkentett mód **gépenkénti állapot, nem a helyé.** Ha egy gép wifije
megkoccan, az a gép megy csökkentett módba, a többi zavartalanul dolgozik.

**Ennek jó mellékhatása van:** az egyeztető kód **gyakran fut** — nem évente
egyszer, éles katasztrófában először (A6 elv).

### 6.4 A degradált mód NTAK-oldala `MVP`

Az NTAK adatszolgáltatásnak **hivatalos útvonala van szolgáltatáskiesésre**:
a rendelésösszesítő `osszesitett` jelölője és az `osszesitettIndoklasa` mező.
Részletek: §11.6.

**Ebből követelmény:** a degradált módnak **okkódot kell rögzítenie**
(áramszünet / szerverkiesés / hálózatkiesés), hogy az indoklás automatikusan
kitölthető legyen.

### 6.5 Személyzeti üzenetek `MVP`

Három üzenet, „hálózat" szóhasználattal (nem „internet"):

1. **A szerver gyanús** — „Nem érjük el a kiszolgálót. Kérjük, ellenőrizze a kiszolgáló gépet és a hálózatot."
2. **Ez a gép a hibás** — „Ez a gép nem éri el a hálózatot. Ellenőrizze ennek a gépnek a hálózati kapcsolatát."
3. **Bizonytalan** — ha nem tudjuk eldönteni.

Plusz **külön, halkabb jelzés az internet hiányára**, ami **soha nem hibaállapot**
és **soha nem befolyásolja** a „szerver vagy én?" döntést.

---

## 7. Magas rendelkezésre állás

### 7.1 Alapdöntések `MVP`

* A HA **benne marad az MVP-ben** — tudatosan, az ellenkező ajánlással szemben.
* A tartalék gép **szintén J1900**.
* Munkafeltevés: **aszinkron replikáció**. `[MÉRENDŐ]` A „szinkron kizárt" állítás **még nincs mérve** (`MERESEK.md` M4).
* Az „automatikusan szinkronról aszinkronra váltó" ág **elvetve** (néma kudarc, A2 elv).
* **Az epoch-mező (fencing) KÖVETELMÉNY**, az első naptól benne a protokollban.
* **`[ALAP]` A replikációs slot WAL-felhalmozódása ellen kötelező védelem.**
  Egy leszakadt készenléti szerverhez tartozó replikációs slot miatt a fő szerver
  **korlátlanul őrzi a WAL-t** → **betelik a lemez** → **a FŐ SZERVER MEGÁLL.**
  64 GB-os SSD-n ez napok kérdése.

  **Nálunk kiemelten veszélyes**, mert két, eddig külön kezelt tényt köt össze:
  a tartalék szerver **egy POS gép**, és **„a szerepet vivő gépet valaki
  kikapcsolhatja, mert az számára csak egy kassza"** (§5.2). A napokig leszakadt
  készenléti szerver tehát **nem széleset, hanem egy már dokumentált kockázat
  kiszámítható következménye.**

  | # | Megoldás |
  |---|----------|
  | a | **A korlát LEMEZ alapú, nem idő alapú** — a valódi korlát a hely. A slot által megőrizhető WAL méretét korlátozni kell; a határ átlépésekor a slot érvénytelenedik |
  | b | **Következmény, amit ki kell mondani:** az érvénytelenített slot után a tartalék **nem tud növekményesen felzárkózni** — **teljes újraszinkronizálás** kell. J1900-on nehéz művelet, **csúcsidőn kívülre** tervezendő |
  | c | **Hangosan kell szólnia** (A2 elv), nem csendes slot-eldobás |
  | d | **Riasztás a küszöb ELŐTT is:** a büdzsé felénél már figyelmeztetés — ne a leállás legyen az első jelzés |
  | e | `[MÉRENDŐ]` A WAL-méret kölcsönhatása a 30 napos purge-dzsel és a 64 GB-os SSD-vel |

### 7.2 Kétlépcsős failover `MVP`

**A gép ellenőriz, az ember dönt.**

1. A pénztárgép **azonnal, látványosan** jelzi a csökkentett módot, és megmondja, mit ellenőrizzenek.
2. A gépnek **fel kell ismernie, ha Ő esett ki** a hálózatról — nem a szerver.
3. **Átkapcsolást csak 5 perc után ajánl fel**, és csak akkor, ha a tanúk sem érik el a szervert.
4. **A gombot EMBER nyomja meg.**

### 7.3 Tanú-séma `MVP`

Két node-dal a split-brain matematikailag nem oldható meg. Ezért **tanúkat**
kérdezünk: a telephely többi gépe szavaz arról, elérik-e a fő szervert.

**Öndiagnózis-létra a kliensen, ebben a sorrendben:**

1. Elérem-e a saját hálózati interfészemet?
2. Elérem-e az alapértelmezett átjárót?
3. Elérik-e a tanúk a szervert?
4. **Utolsó fokként:** van-e internet — **publikus** címre, HTTPS-sel (nem ICMP), két külön jellel (névfeloldás + elérés). **Ez soha nem befolyásolja a „szerver vagy én?" döntést**, csak külön, megcímkézett sorban jelenik meg.

### 7.4 Átvételi útvonalak `MVP`

| Útvonal | Mikor | Adatvesztés |
|---------|-------|-------------|
| **Tiszta átvétel** | A régi fő szerver él és a tartalék eléri | **Nulla** — a tartalék az átvétel ELŐTT leszívja a nem replikált tranzakciókat |
| **Kemény átvétel** | A régi fő tényleg halott | **Árva tranzakciók elkerülhetetlenek** |

**Átvétel előtti begyűjtés a kliensektől:** a tartalék begyűjti a kliensek
outboxában lévő, még nyugtázatlan adatot. **Ez nem blokkolja az első bizonylatot** —
a kétrétegű számozás (§8) miatt a tartalék azonnal kiszolgálhat, a begyűjtés
párhuzamosan fut. Célja **adat-teljesség és ellenőrzés**, nem ütközés-megelőzés.

### 7.5 Visszaállás (failback) `MVP`

* **AUTOMATIKUS**, ha a fő és a tartalék **1 percig stabilan látják egymást és beszélnek is.**
* A régi „csak szuperfiókkal" szabály **elvetve**.
* **Az árva tranzakciók KIMENTÉSE automatikus és kötelező.**
* **A KÖNYVELÉSÜK viszont nem lehet automatikus** — duplikált adóügyi bizonylat kockázata miatt emberi döntés kell.
**Az árva tranzakciók feloldása KIZÁRÓLAG Siduri támogatói felületen történik.**
Az ügyféltől ezt a feladatot **teljesen elvesszük** — a duplikált adóügyi
bizonylat jogi következmény, a feloldáshoz **az adóügyi eszköz saját naplóját
kell keresztbe olvasni**, és ez szakértelem, nem gombnyomás. Ritka esemény
(csak kemény átvétel után), tehát a támogatói bevonás nem skálázódik rosszul.
Ugyanaz az eszkalációs minta, mint a nyers auditnál (§18.4) és a tartós
integráció-kikapcsolásnál (§19.4).

**Két kikötés:**

| # | Kikötés |
|---|---------|
| a | **A feloldatlan árva tranzakció NEM blokkolhatja az üzletmenetet** — karanténsorba kerül, a hely tovább dolgozik |
| b | **Az ügyfél LÁSSA, hogy van feloldatlan tétel**, akkor is, ha nem tud vele mit kezdeni (A2 elv). Csak a **feloldást** vesszük el, a **tudást** nem |
* **Szerepcsere azonnal, ahogy stabil** — nincs csendes ablakra halasztás.

### 7.6 Billegés-védelem `MVP`

**Növekvő várakozás** minden automatikus visszaállás után, plusz **leállási
határ**, ami után az automatika kikapcsol és **hangosan szól**.
`[MÉRENDŐ]` A küszöbök (X visszaállás / Y idő) mérésből jönnek (`MERESEK.md` M6).

### 7.7 Amit a HA NEM old meg `ALAP`

> **A szerver-HA nem véd az adóügyi eszköz ellen.** Ha a telephelyen egyetlen
> adóügyi eszköz van, és az a gép hal meg, amelyikre kötve van, a nyitott
> asztalokat sehol nem lehet lezárni. A duplikált szerver ezen semmit nem segít.

Ellenszer: **gépenkénti adóügyi eszköz ajánlása**, 4 géptől kiemelten legalább
kettő, plusz **nyomtatás-átirányítás** (§19.6).

---

## 8. Bizonylat-számozás

### 8.1 Kétrétegű számozás `ALAP`

| Réteg | Formátum | Ki adja | Nullázható |
|-------|----------|---------|------------|
| **SIDURI szám** | `xxxxxxyyyzzzzz` | mi | nem |
| **ADÓÜGYI szám** | `Axxxxxxxxx/yyyy/zzzzz` | az adóügyi eszköz | **igen** |

**A SIDURI szám felépítése:** `xxxxxx` = az **ÜZLETI NAP** dátuma (nem a naptári!),
`yyy` = eszközszám, `zzzzz` = napi folyószám.
Példa: `26082200300347`.

**Miért így:**

* **Naponta újraindul → soha nem fogy el.**
* **A dátum-előtag miatt szám szerint időrendben áll.**
* **Minden kiállító eszköz saját, elhatárolt tartományból számoz** (a 2-es kassza `002…`) → **az ütközés szerkezetileg lehetetlen**, nulla koordináció kell, és **a tartalék szerver átvételkor AZONNAL kiszolgálhat.**

**Miért nem lehet az adóügyi szám a mi azonosítónk:**

* **Csak a nyomtatás UTÁN érkezik** — addig a bizonylatnak nem lenne azonosítója, és nyomtatási hiba esetén soha nem is lesz.
* Nem mi vezéreljük.
* **Nem minden bizonylatnak van** — előnyugtának, raktármozgásnak, készpénzmozgásnak soha.

Az adóügyi számot **tároljuk a bizonylat mellett**, mert a sztornóhoz kell.

### 8.2 Eszközazonosítás és klónvédelem `MVP`

* Az eszközszám-tér **KÖZÖS minden eszköztípusra** (POS, vékonykliens, kioszk) — így a vékonykliens későbbi bővítése nem töri meg a számozást.
* A szerver adja ki az azonosítót, és **regisztráció nélkül nincs bizonylat**.
* **Ez önmagában nem fogja meg a klónt.** Hiányzó darab: **hardveres ujjlenyomat + forgó hitelesítő adat**. Két ujjlenyomat egy azonosítón → **mindkettő tiltva**, amíg ember fel nem oldja.
* **A gépcsere explicit, engedélyezett művelet**, nem véletlen mellékhatás.

### 8.3 Az adóügyi eszköz azonosítása a bizonylaton `MVP`

**A bizonylat tárolja, MELYIK adóügyi eszköz nyomtatta.** Nyomtatás-átirányítás
(§19.6) esetén a SIDURI szám a **kiállító** gépé, az adóügyi szám a **nyomtató**
eszközé — a két réteg szándékosan szétválik, és utólag tudni kell, miért.

---

## 9. Nap-fogalmak, napzárás, óra

### 9.1 MUNKANAP `ALAP`

A **telephely** üzleti napja. Nem naptári nap; egy dátumra több is nyitható.

| Küszöb | Viselkedés |
|--------|-----------|
| **23:00** | Enyhe figyelmeztetés |
| **23:30** | Erős figyelmeztetés |
| **23:45** | **Kíméletlen kényszerzárás** — nem mehet tovább |

**Miért 23:45 és nem 24 óra:** az NTAK napi zárás validációja
`zarasIdopontja − nyitasIdopontja <= 24 óra`, **szinkron, `Conflict` hibakulccsal** —
a 24 óránál hosszabb nap adatszolgáltatása **azonnal elutasításra kerül**.
A 15 perc tartalék.

> ⚠️ **Az időtartamot ABSZOLÚT (UTC) alapon kell számolni, soha nem faliórán.**
> Az őszi óraátállítás éjszakáján egy 06:00 → 06:00 „nap" faliórán 24 óra,
> valójában **25**. Ez a leggyakoribb módja annak, hogy évente egyszer
> elutasítást kapjunk.

**A mérés monoton órán történik** (a szerver visszaállíthatatlan, felfelé
számláló óráján), és a vágási döntést a monoton és a faliórás érték közül a
**konzervatívabb** (nagyobb eltelt idő) hozza. Szerver-újraindulás nullázza a
monoton órát — ilyenkor visszaesünk a faliórára, és ezt jelezni kell.

### 9.2 MŰSZAK `ALAP`

**Eszközönkénti** fogalom — az adott pénztárgép adóügyi munkanapja. Egy
MUNKANAP-on belül több MŰSZAK lehet, gépenként és felhasználónként.

* Készpénz ki- és befizetés, kassza fölözése **bizonylattal**.
* Műszakátadás **változatlan kasszaállással** (fölözés nélkül) is lehetséges.
* **Kassza-eltérés naplózása nyitáskor** (hiány / többlet regisztrálása).
#### Vakzárás (blind close) `v1`

**Jogosultsághoz kötött.** Akire vonatkozik, az **nem látja a
műszakinformációkat** (bevétel, eladási statisztika, várt kasszatartalom).
Záráskor a címletkalkulátoron **beírja a ténylegesen megszámolt készpénzt**, és a
gép **csak a rögzítés után** naplózza az eltérést, a biztonsági auditágba, ahol
kizárólag a vezetőség látja.

**Indok:** ha a pultos záráskor látja az elvárt összeget, a többletet **eltehetiI
úgy, hogy a gép nem mutat eltérést.**

| # | Kikötés |
|---|---------|
| a | ⚠️ **AZ ADÓÜGYI ESZKÖZ X-JELENTÉSE KIÜTI A VAKZÁRÁST.** A pénztárgép maga is kinyomtatja a napi forgalmat — ha a pultos ezt lefuttathatja, **kiszámolja az elvárt kasszatartalmat.** Az X-jelentés futtatását **is jogosultsághoz kell kötni**; ha az adott készülék ezt nem engedi, **ki kell mondani az ügyfélnek, hogy a védelem részleges** |
| b | **A rögzítés UTÁN sem szabad visszamutatni az eltérést.** Egy „eltérés: +5 000" visszajelzésből a pultos **megtanulta a várt számot a következő alkalomra.** A visszajelzés csak annyi lehet: „rögzítve" |
| c | **Alapból kikapcsolva, felhasználónként bekapcsolható** — lassítja a zárást és bizalmatlanságot jelez, tehát üzleti döntés |

* **Beépített címletkalkulátor** a műszakzáráshoz: szorzós számláló
  (20 000 × 4, 10 000 × 3, …) a készpénz összesítéséhez. `v1`
  **A címletbontás mentődjön el a műszakzárás rekordjában**, ne csak a végösszeg —
  egy kasszaeltérésnél a címletszerkezet gyakran megmondja, mi történt
  (egy hiányzó 20 000-es nem centizés, hanem egy darab bankjegy).

### 9.3 Automatikus napzárás `MVP`

Az ügyfél által állítható, **tervezett napzárási időpont** (pl. 04:00).

**Menete:**

1. **Előfázis, 5 perccel a zárás előtt:** új rendelés nyitása és új fizetés indítása letiltva; a folyamatban lévők befejezhetők.
2. **Az eszközök MŰSZAK-jának zárása.**
3. **A MUNKANAP zárása.**
4. Közben a felhasználók tájékoztatása: *„automatikus napzárás folyamatban, kis türelmet"*.

**Kötelező szünet a zárás és a következő nyitás között:** állítható,
**minimum 5 perc, alapértelmezés 10 perc.**

> **A szünet MAGA a biztonsági tartalék.** 04:00 zárás + 10 perc → a munkanap
> matematikailag legfeljebb **23 óra 50 perc** lehet. Nem kell külön őrszem a
> 24 órás korlát betartására: a konfiguráció szerkezetéből következik.

**Négy kötelező kiegészítés:**

| # | Szabály | Miért |
|---|---------|-------|
| a | **A MUNKANAP zárása nem függhet attól, hogy minden eszköz műszakja lezárult.** Az elérhetetlen eszközt megjelöljük, és a következő bekapcsolásakor zárjuk | Egy éjszakára kikapcsolt POS 04:00-kor nem érhető el. Ha ez blokkolna, az automatika soha nem futna le |
| b | **A nyitott VENDÉGASZTALOKAT az automatika nem zárja le** — átlépnek a határon | A vendég egy számlát kap, nem kettőt |
| c | **Konfiguráció-validáció mentéskor**, és a felület **írja ki a számított maximumot**: „napzárás 04:00, újranyitás 04:10 → a munkanap legfeljebb 23:50" | Rejtett számítás ne legyen |
| d | **A 23:45-ös kényszerzárás megmarad vészféknek**, akkor is, ha az automatika be van kapcsolva | Az automatika elmaradhat: állt a szerver, akadt egy eszköz |

**Kézi zárás:** külön engedélyezhető. Ha megtörtént, az automatikának nincs dolga.

**Miért kell a tervezett napzárás egy 0–24-es helynek:** ha csak a kényszerzárásra
hagyatkoznak, a napzárás **naponta 15 perccel korábbra vándorol** — négy nap
alatt egy órát, egy hónap alatt körbeér, és előbb-utóbb **szombat este 22:00-kor,
csúcsban** csap le.

### 9.4 A munkanap-határon átnyúló nyitott rendelés `MVP`

A rendelés **átlép a határon**, és ahhoz a tárgynaphoz tartozik, **amelyikben
elkezdődött** — összhangban azzal, hogy a tárgynap a nyitás dátumából származik.

`[NYITOTT]` **Elfogadja-e az NTAK, ha egy tárgynapra már beérkezett a napi zárás,
és utána még jön arra a tárgynapra rendelésösszesítő?** A specifikációban erre
nincs sem tiltás, sem engedély. 0–24-es helyen ez **mindennapos**, tehát
megkérdezendő.

### 9.5 Óraszinkron `ALAP`

**Időforrás-sorrend a telephelyen:**

1. **NTP**, ha van internet.
2. **Az adóügyi eszköz órája** — az AEE a saját mobilhálózatán szinkronizál, tehát **internet nélkül is ez a legmegbízhatóbb óra a helyszínen.**
3. **A telephelyi szerver a kliensek felé.** A kliensek **hozzá** igazodnak, nem az internethez — így a telephely offline is önmagával konzisztens.

**Először javítunk, csak utána panaszkodunk:**

| Eltérés | Válasz |
|---------|--------|
| **< 2 perc** | **Csendben javítjuk.** Nincs üzenet |
| **2–15 perc** | Javítjuk, ha van forrás. Ha nincs: **nem blokkoló** figyelmeztetés + auditbejegyzés |
| **> 15 perc** | **Feltűnő, nyugtázandó** figyelmeztetés — **továbbra sem blokkol** |
| **> 2 óra, vagy eltérő DÁTUM** | **Az EGYETLEN blokkoló eset.** Egygombos kiút: „óra beállítása az adóügyi eszközről" |

**Mikor állítunk órát, és mikor csak ellenőrzünk:**

| Mikor | Mit |
|-------|-----|
| **Napnyitás előtt** | **Ellenőrzés + BEÁLLÍTÁS** |
| **23:00 / 23:30 figyelmeztetéskor** | **CSAK ELLENŐRZÉS. Beállítás soha** |

> **TILOS előre állítani az órát nyitott üzleti nap közben.** A
> `nyitasIdopontja` és a `zarasIdopontja` is a mi óránkról jön, tehát az abszolút
> elcsúszás kiesik a különbségből — **kivéve, ha menet közben javítunk**. Egy
> csendes, 12 perces előre-korrekció egy 23:40-es napból 23:52-t csinálna.
> Visszafelé állítás sem megengedett, mert az a sorrendet keverné.

**A valódi veszély ezen a hardveren nem a másodperces drift, hanem a halott
CMOS-elem** — „a gép szerint 2014 van", minden áramszünet után.

**Minden óraállítás auditnaplózott esemény**, a régi és az új értékkel.
**A sorrendezés soha nem a faliórán múlik** — azt monoton számláló adja.

---

## 10. Fiskális működés

### 10.1 A három üzemmód `ALAP`

| # | Üzemmód | Mit ad ki | Megjegyzés |
|---|---------|-----------|------------|
| **1** | **Belső rendszer** (nincs adóügyi eszköz) | A papírra **„NEM ADÓÜGYI BIZONYLAT"** jelölést kell tenni — **kötelező elem** | Nyugtaadási kötelezettséget nem vált ki |
| **2** | **Online pénztárgép (AEE)** | Adóügyi nyugta, adóügyi számmal | A jelenlegi fő cél |
| **3** | **e-pénztárgép** (8/2025. (III. 31.) NGM rendelet) | e-nyugta, Nyugtatár | Későbbi irány |

Részletek: [`FISKALIS_UZEMMODOK.md`](FISKALIS_UZEMMODOK.md).

### 10.2 Nem írunk saját adóügyi szoftvert `ALAP`

**Kimondott döntés:** *nem tervezünk NAV-os adóügyi nyomtatóhoz szoftvert írni,
sem most, sem később.* **Meglévő gyártói szoftverrel integrálunk.**

**Ebből következő korlátok:**

* A gyártói illesztő-protokoll dokumentáció **szerzői jogvédett**, és **partneri megállapodás nincs** — eddig egyetlen, szöveg nélküli e-mailes válasz érkezett.
* **A dokumentáció tartalma semmilyen formában nem kerülhet publikus anyagba** — sem idézet, sem parancstáblázat, sem „átfogalmazva, de felismerhetően". **A repók mindig privátok maradnak.**
* A gyártóspecifikus illesztő **elkülönített modulban** él, hogy bármikor kiemelhető legyen.
* **Nincs támogatási szerződés, nincs értesítés firmware-változásról, és nincs tesztkészülék.**

> **Ütemezési kapu:** haladunk a fejlesztéssel, **de a fiskális réteg
> VÉGLEGESÍTÉSE előtt be kell várni a gyártói kapcsolatfelvételt és a fizikai
> tesztkészüléket.** A fiskális mérföldkő készülék nélkül nem zárható le.

### 10.3 A gyűjtőkiosztás kemény korlát `ALAP`

A kapott kiosztás **8 fix rekesz, egy sem szabad**:

| # | Gyűjtő | Adójel |
|---|--------|--------|
| 1 | Termék 5% | A00 |
| 2 | Termék 18% | B00 |
| 3 | Termék 27% | C00 |
| 4 | Szervizdíj 5% | A00 |
| 5 | **TAM** | E00 |
| 6 | Szervizdíj 18% | B00 |
| 7 | Szervizdíj 27% | C00 |
| 8 | **AJT** | D00 |

**Következmények:**

1. **Az áfakulcs-készlet kötött: 5 / 18 / 27 / TAM / AJT.** Semmi más nem küldhető. **A validációt a terméktörzs mentésénél kell megfogni**, nem nyomtatáskor — ott már késő.
2. **A szervizdíjnak saját, áfakulcsonkénti gyűjtői vannak.** A szervizdíjat **nem szabad a termék tételébe olvasztani**, és **áfakulcsonként bontva** kell számolni, nem egyetlen záró összegként.
3. **Az AJT (adójegyes termék) vendéglátásban gyakorlatilag használatlan** — ez az egyetlen esélyes szabad rekesz, ha a gyártó megengedi az újrakiosztást. `[NYITOTT]`
4. Bármi új igény (pl. DRS visszaváltási díj) csak meglévő rekesz terhére fér be.

**Megerősítés két független forrásból:** az NTAK `afaKategoria` értékkészlete
`A_5`, `B_18`, `C_27`, `D_AJT`, `E_0` — **betűről betűre ugyanaz.**

### 10.4 Tételtípusok a fiskális rétegben `MVP`

| Eset | Kezelés |
|------|---------|
| **Áras módosító** | **Önálló tétel**, saját áfakulcson |
| **Ár nélküli módosító** | **Szövegsor a termék alatt** — nem tétel, nincs ára, áfája, gyűjtője |
| **Levonó módosító** (pl. „sajt nélkül −100") | **NEM küldhető negatív árú eladási sorként** — a protokollban a negatív ár *tételsztornó*. Kedvezmény-mechanizmuson keresztül, vagy a termék árába építve |
| **Göngyölegvisszavétel** | Negatív mennyiség — a protokoll natívan támogatja |
| **Végösszegi kedvezmény** | **ÁFA-kulcs arányosan szétosztva** a tételeken |

`[IGAZOLANDÓ]` **A nulla összegű tétel.** A protokoll szerint támogatott, de az
ügyfél tudomása szerint **a készülék nem fogadja el**. **Munkafeltevés: nem
fogadja el.** A szövegsoros megoldás ettől függetlenül helyes — ha nem küldünk
tételt, a nulla összeg kérdése fel sem merül. (`MERESEK.md` M15)

### 10.5 Sztornó és törlés `MVP`

* **Nyitott tétel** = törölhető (void).
* **Lezárt, fizetett nyugta** = **csak sztornózható**, negatív bizonylattal.
* Sztornóhoz **kell az eredeti adóügyi szám** — ezért tároljuk (§8.1).

`[IGAZOLANDÓ]` A „teljesen új negatív fiskális nyugta" mechanizmus.

### 10.6 A gyártói szolgáltatás hálózati kitettsége `ALAP`

**A gyártói szolgáltatás portra figyel, és NEM vizsgálja, hogy a kérés
localhostról vagy kívülről érkezett-e.**

**Ebből két dolog következik:**

1. **A nyomtatás-átirányítás (§19.6) technikailag ingyen van** — nem kell semmit „kinyitni".
2. **De a kockázat MÁR MOST fennáll:** a telephelyi hálózaton **bárki, bármilyen eszközről, hitelesítés nélkül adóügyi parancsot küldhet** a pénztárgépre — bizonylatot nyithat, tételt vehet fel, sztornózhat. **Ha a vendég-wifi és az üzemi hálózat nincs szétválasztva, ezt egy vendég is megteheti a telefonjáról.**

> **Kötelező telepítési előfeltétel: a vendég-wifi és az üzemi hálózat fizikai
> vagy VLAN-szintű szétválasztása.** Nem ajánlás. A telepítési ellenőrzőlistán
> kötelező tétel; ha az ügyfél nem teljesíti, az a kockázatvállalási nyilatkozat
> tárgya.

Amit még tehetünk: tűzfalszabály a saját gépeinken, ami a szolgáltatás portját
csak az ismert gépekre engedi. Ez nem oldja meg a gyökeret, de szűkíti.

`[NYITOTT]` Van-e a szolgáltatásnak **bármilyen hitelesítési, IP-korlátozási vagy
figyelési-cím beállítása** — kérdés a gyártó felé.

---

## 11. NTAK adatszolgáltatás

Forrás: **NTAK Vendéglátás — RMS Interfész leírás v1.06** (MTÜ, 2024.06.10),
a hivatalos műszaki specifikáció.

### 11.1 Alapfogalmak `ALAP`

* **Tárgynap:** *„az aktuálisan nyitott nap nyitásának dátumával megegyező dátum érték"*; naptári napon átnyúló esetben **a nyitás időpontjából származtatott nap.** Tehát **gyakorlatilag a MUNKANAP** — nem naptári nap.
* **Két üzenettípus:** rendelésösszesítő (forgalmi adat) és napi zárás.

### 11.2 Küldési ütem `ALAP`

| Üzenet | Mikor |
|--------|-------|
| **Rendelésösszesítő** | **15 percenként** az előző küldés óta rögzített rendelések. **Az érték paraméterezhető kell legyen** — nem éghet a kódba |
| **Napi zárás** | Az üzleti nap zárásakor, **de legalább 24 óránként** |

> **Ez érdemben megváltoztatja az offline tervet.** Egy hosszabb
> internetkimaradás alatt **15 percenként keletkezik egy elmaradt küldés**, amit
> sorba kell állítani és a visszatéréskor **sorrendben, átfedés nélkül** pótolni.
> A kimenő NTAK-sor ugyanolyan elsőrangú, tartós, felügyelt sor kell legyen,
> mint a bizonylat-outbox.

### 11.3 A feldolgozási nyugta lekérdezése `MVP`

Minden beküldésre **szinkron válaszban érkezik egy feldolgozási azonosító**, és
**a feldolgozás eredményét le KELL kérdezni** — a beküldéstől számított
**24 órán belül**, legkésőbb **1 hónapon belül**, mert utána már nem elérhető.

**A beküldés nem elég: a nyugtát is be kell gyűjteni és eltárolni.** Ez egy
második, visszamenőleges folyamat.

### 11.4 Kemény validációk, amiket be kell tartani `ALAP`

| Validáció | Típus | Következmény |
|-----------|-------|--------------|
| `zarasIdopontja − nyitasIdopontja <= 24 óra` | **szinkron**, `Conflict` | A napi zárás elutasítva → innen a 23:45-ös munkanap-korlát (§9.1) |
| `rendelesVege − rendelesKezdete <= 24 óra` | **szinkron**, `Conflict` | **Egy nyitott rendelés nem lehet 24 óránál tovább nyitva** |
| `nyitasIdopontja <= sysDate`, `zarasIdopontja <= sysDate` | szinkron, `Future` | **Ha az óránk előre jár, az üzenet elutasításra kerül** |
| `nyitasIdopontja >= előző zarasIdopontja` | aszinkron | Nem lehet átfedő időszak |
| ADOTT_NAPON_ZARVA után nincs több napi zárás arra a tárgynapra | aszinkron, `UniqueConstraint` | **Lásd §11.7 — visszafordíthatatlan** |
| A tételösszesítők összegének ki kell adnia a rendelés végösszegét | — | **Kemény korlát a menü-szétosztásra** (§13.4) |

**A 24 órás rendeléskorlát csak a BEKÜLDÖTT rendelésekre vonatkozik.**
Személyzeti asztal és selejt kivétel, mert nem megy beküldésre.
`[IGAZOLANDÓ]` Az NTAK ismer `EGYEB / NEM_VENDEGLATAS` tételkategóriát, de a
rendelésbesorolás értékkészlete csak `NORMAL / SZTORNO / HELYESBITO` —
**„nem forgalmi" besorolás nincs.** Ha kiderül, hogy a személyzeti fogyasztást
is jelenteni kell, a korlát rájuk is vonatkozik.

**Belső korlát ettől függetlenül kell:** egy hetek óta nyitott személyzeti asztal
üzemeltetési hiba → figyelmeztetés napnyitáskor minden nem-vendég rendelésre,
ami régebbi az előző munkanapnál.

### 11.5 Tételszintű mezők `ALAP`

| Mező | Tartalom |
|------|----------|
| `megnevezes` | max 255 karakter, kötelező, nem üres |
| `fokategoria` / `alkategoria` | Szabványos értékkészletből (§11.8) |
| `afaKategoria` | `A_5` / `B_18` / `C_27` / `D_AJT` / `E_0` |
| `bruttoEgysegar` | tört is lehet — **de mi egész forintot küldünk** (§15.2) |
| `mennyisegiEgyseg` | `DARAB` / `LITER` / `KILOGRAMM` / `EGYSEG` / `ADAG` |
| `mennyiseg` | **a termék saját kiszerelése** (pl. 0,33) |
| `tetelszam` | **hány darabot rendeltek** (pl. 2) |
| `tetelOsszesito` | **egész szám**, tételszám × bruttó egységár, kereskedői kerekítéssel |

**A `mennyiseg` és a `tetelszam` két külön dolog.** 2 db 0,33 l-es dobozos üdítő:
`mennyisegiEgyseg = LITER`, `mennyiseg = 0.33`, `tetelszam = 2`.

**Ebből a terméktörzsben KÉT NTAK-mező kell:** mennyiségi egység **és**
kiszerelési mennyiség. Ez pontosan illeszkedik a kiszerelés-modellhez (§12.4).

> A specifikáció **útmutatása** szerint egy 0,33 literes dobozos üdítőnél a
> `LITER` használandó, nem a `DARAB`. **Ez azonban Megjegyzés, nem validáció** —
> a mező validációi kizárólag `NotNull` és `Enum`, tehát **a `DARAB` átmegy.**
> A rendszer **támogatja mindkettőt**, az ajánlott értéket **felkínálja**, de
> **az ügyfél dönt** (A3 elv).

**Rendelésszintű mezők:** `helybenFogyasztott` (bool — **„vegyes esetben helyben
fogyasztást kell jelölni"**), `rendelesBesorolasa` (`NORMAL` / `SZTORNO` /
`HELYESBITO`), `osszesitett` + `osszesitettIndoklasa`.

**A `helybenFogyasztott` leképezése:** a mi modellünk finomabb (tételenkénti
teljesítési mód). Szabály: **igaz, ha a rendelésben legalább egy helyben
fogyasztott tétel van**; csak a teljesen elviteles rendelés kap hamisat. Az
áfakulcs tételenként megy, tehát a vegyes rendelés helyesen jelenik meg.

### 11.6 Degradált mód az NTAK-ban `MVP`

`osszesitett` (bool) + `osszesitettIndoklasa`. A specifikáció szerint:

> *„Annak jelölésére szolgál, ha adott rendelésösszesítő egy hosszabb időszak
> (max 1 üzleti nap) értékesítéseit összevontan tartalmazza. Csak
> szolgáltatáskiesés esetén használható, pl áramszünet, vagy rendszerkiesés.
> Normál adatszolgáltatás esetén hamis értékkel kell küldeni."*

**Ez pontosan a mi degradált módunk esete.** Nem kell saját megoldást kitalálni.

| # | Következmény |
|---|--------------|
| a | **Az összevonás felső határa 1 üzleti nap** — hosszabb kiesést napokra kell bontani |
| b | **Kell indoklás szöveg** → a degradált módnak **okkódot kell rögzítenie** |
| c | Normál üzemben a mező kötelezően **hamis** — „biztos ami biztos" alapon mindig igazra állítani tilos |

### 11.7 Zárva tartott és forgalom nélküli nap `MVP`

**Ez a MI szoftverünk kötelezettsége, nem az ügyfélé az NTAK portálon.**
A specifikáció szó szerint:

> *„Napi zárási üzenetet akkor is küldenie kell minden RMS szoftvernek, ha az
> adott tárgynapon zárva tartott a vendéglátó üzlet. […] Abban az esetben is kell
> napi zárás üzenetet küldeni, ha a nyitvatartás során nem került beküldésre
> rendelésösszesítő. […] A napi zárás üzeneteket minden tárgynapra vonatkozóan
> be kell küldeni."*

> ### ⚠️ VESZÉLY: a „nem volt nyitva" jelzést TILOS ELŐRE küldeni
>
> A validáció: *„Azon tárgynapra, melyre már van beküldve ADOTT_NAPON_ZARVA
> napi zárás, azon tárgynapokra nem lehet további napi zárás üzeneteket
> beküldeni."*
>
> Ha 23:55-kor elküldenénk, és a hely 23:58-kor mégis kinyit, **azt a tárgynapot
> véglegesen lezártuk** — a valós forgalmuk napi zárása többé nem küldhető be.
> **Nem visszavonható.** És ez nem elméleti eset: a 23:55 pont az az időpont,
> amikor egy szórakozóhely vagy éjszakai büfé kinyit.

**A helyes megoldás — visszamenőleg küldünk, nem előre:**

| # | Szabály |
|---|---------|
| a | A `ADOTT_NAPON_ZARVA` / `FORGALOM_NELKULI_NAP` üzenet **csak akkor mehet ki, ha a tárgynap már biztosan lezárult** |
| b | **Napi feladat** (javaslat: 01:00) végigveszi a lezáratlan tárgynapokat, és a **nyitvatartási minta** alapján küldi a helyes besorolást |
| c | **Ha a minta szerint nyitva kellett volna lenniük, de nem nyílt nap:** ez **kérdés**, nem automatizmus — a következő napnyitáskor: *„tegnap zárva voltatok, vagy elfelejtettek napot nyitni?"* |
| d | **Szerverindításkor pótolni kell** minden hiányzó tárgynap-zárást |
| e | **Zárvatartás alatt (kikapcsolt telephelyi szerver) A FELHŐ küldi.** A telephelyi szerver a tulajdonos, amíg online van; a felhő akkor lép be, ha a minta szerint zárva van a hely **és** a szerver X órája nem jelentkezett. A duplikációt a `UniqueConstraint` visszadobja |

**Nyitvatartási minta** (heti séma + kivételnapok/ünnepek), a webes felületen
állítható. Kettős haszna: ebből tudjuk, mikor kell automatikusan jelezni, és
mikor kellett volna nyitva lenniük — ami nem ugyanaz, és nem automatizálható.

### 11.8 Kategóriakészlet `ALAP`

| Főkategória | Alkategóriák |
|-------------|--------------|
| **Étel** (`ETEL`) | reggeli, szendvics, előétel, leves, főétel, köret, savanyúság/saláta, kóstoló, péksütemény, desszert, snack, **főétel körettel**, **ételcsomag**, egyéb |
| **Helyben készített alkoholmentes ital** (`ALKMENTESITAL_HELYBEN`) | víz, limonádé/szörp/frissen facsart, alkoholmentes koktél, tea/forrócsoki/tejalapú, **italcsomag**, kávé |
| **Nem helyben készített alkoholmentes ital** (`ALKMENTESITAL_NEM_HELYBEN`) | víz, rostos üdítő, szénsavas üdítő, szénsavmentes üdítő, **italcsomag** |
| **Alkoholos ital** (`ALKOHOLOSITAL`) | koktél/kevert ital, likőr, párlat, sör, bor, pezsgő, **italcsomag** |
| **Egyéb** (`EGYEB`) | egyéb, **szervizdíj**, **borravaló**, kiszállítási díj, nem vendéglátás, környezetbarát csomagolás, műanyag csomagolás, **kedvezmény** |

**Két fontos következmény:**

1. **A kedvezmény, a borravaló és a szervizdíj az NTAK-ban ÖNÁLLÓ TÉTEL**, nem a végösszeg módosítója. Ez egybevág a gyűjtő-lelettel (§10.3), ahol a szervizdíjnak saját gyűjtői vannak.
2. **Csomagkategória csak főkategórián belül létezik.** Vegyes (étel + ital) csomagkategória **nincs** → a klasszikus menü **kötelezően szétbontandó** (§13.4).

**Az ENUM-értékkészletek a jövőben változhatnak**, a szoftvert fel kell készíteni
rá. **Az NTAK kategóriák, mennyiségi egységek és áfakulcsok NEM éghetnek a
kódba** — konfigurációból, frissíthetően kell jönniük, kliens-újratelepítés
nélkül.

### 11.9 Ki állítja be a kategóriákat `MVP`

**A termékek és menütételek NTAK fő- és alkategóriájának pontos beállítása az
ÜGYFÉL feladata.** Mi a környezetet és a lehetőséget teremtjük meg hozzá.

**Két dolog ettől függetlenül a mi felelősségünk:**

1. **Kemény kapu marad:** NTAK-kategória nélkül a termék nem menthető, ha a hely NTAK-köteles. Nem azért, mert mi akarjuk megmondani a kategóriát, hanem mert **a hiányzó kategóriával a beküldés elutasításra kerül**, és az üzemeltetésileg a mi problémánk lesz.
2. **A menükomponensek is kapnak saját NTAK-kategóriát** — a szétbontás miatt önálló tételek.

### 11.10 Tanúsítás `ALAP`

**MTÜ Igazolás** és **validációs teszt** kell az élesítés előtt, telephelyenkénti
tanúsítványokkal és üzenet-aláírással. **Ez külső kapu, ami dominálja az
ütemtervet** — nem fejlesztési feladat, hanem átfutási idő.

**Kell tanúsítvány-lejárat figyelés — a FELHŐBEN, nem a telephelyi szerveren.**
Ha a telephelyi szerver az, ami áll, akkor pont nem tud riasztani.
Erősödő riasztás: **60 / 30 / 14 / 7 / 1 nap**; az utolsó kettő **felénk is megy**,
nem csak az ügyfélnek. Új tanúsítványt igényelni átfutási idő.
**Ugyanez a lejárat-figyelő szolgálja ki az összes többi hitelesítő adatot** is
(licenc, számlázó API-kulcs, felhős tanúsítványok) — egy közös mechanizmus
olcsóbb, mint három külön.

---

## 12. Termékkatalógus

### 12.1 Kategóriastruktúra `MVP`

* **Maximum 4 kategóriaszint, a főkategóriát is beleértve.**
* **A főkategória kötelező**, az alkategóriák opcionálisak.
* **Az áfa-alapértelmezés bármely szinten megadható, és lefelé öröklődik** — a mélyebb szint felülírhatja.

**Miért alulról öröklődik:** a mélyebb kategória gyakran pontosabban tudja a
helyes kulcsot. Példa: *Italok → Üdítők → helyben készült / dobozos* — a
levélszinten dől el az áfakulcs, nem a főkategórián.

### 12.2 ÁFA a terméken `ALAP`

* **Két áfamező kötelezően kitöltve:** helyben fogyasztás és elvitel.
* **„Ugyanaz" jelölő** — a másolás pillanatában másol, **nem hivatkozik** (A4 elv).
* **Ha a helyben fogyasztás kulcsát megváltoztatják, a jelölő automatikusan kikapcsol** és az elviteli érték változatlan marad.
* **Kemény kapu: nincs termék hiányos áfa-adatokkal.** Mentés nem lehetséges.
* Alapértelmezés: **27%** (A5 elv — a biztonságosabb irány).

**Miért másolás és nem hivatkozás:** ha hivatkozás lenne, a helyben fogyasztás
kulcsának csökkentése **csendben lecsökkentené az elviteli áfát is** — ami
komoly jogsértés. **A két hibairány nem egyenértékű**: a túl magas áfa
pénzügyi hátrány, a túl alacsony jogsértés.

**Az áfa besorolása az ügyfél felelőssége** — mi a lehetőséget adjuk hozzá.

### 12.3 Árazás a terméken `ALAP`

* **A bruttó ár az igazság.** Ha az árlistán 1500 van, akkor 1500; a nettó és az áfa ebből származik.
* **Áfakulcs-változáskor a BRUTTÓ marad** (1500 marad 1500). A nettó árbevétel változik, az árlista nem. **A felület írja ki, hogy ez azonnal átírja a haszonkulcsot.**
* **NINCS külön elviteli bruttó ár.** Ha a hamburger 1500 és elvitelre kérik, az ügyfél elesik ~21%-nyi haszontól — **ez így működik Magyarországon, és bele van kalkulálva.** Csak a **két áfakulcs** van külön.

**Következmény, ami ebből esik ki:** mivel a bruttó azonos, de az áfa eltér,
**a nettó árbevétel teljesítési módonként más** → **minden árrés- és food
cost-riportot teljesítési módonként bontva kell számolni**, sosem vegyített
bruttón. Kell egy riport, ami megmutatja, **mennyibe kerül a tulajdonosnak az
elviteles arány.**

### 12.4 Kiszerelések `MVP`

**A kiszerelés a termék GYERMEKE, nem külön termék.**

| Öröklődik | Saját |
|-----------|-------|
| név(törzs), kategória, áfakulcsok, NTAK-kategória | **bruttó ár**, receptmennyiség, **térfogat/tömeg**, vonalkód |

> **A rendszer NEM számol árat.** A 0,5 l csapolt sör 1000 Ft, a 0,3 l **nem 600,
> hanem amennyit az ügyfél mond** (pl. 750). Súly/térfogat szerinti árazás **is**
> legyen, de csak ahol kérik. (A3 elv)

**A kiszerelés térfogata/tömege az NTAK `mennyiseg` mezőt tölti** (§11.5) —
tehát nem csak a nevében kell szerepelnie.

**Megjelenítés a POS-on:** 2–3 kiszerelésnél külön gombok (leggyorsabb),
többnél felugró — konfigurálható.

### 12.5 Ártörténet `ALAP`

* **A bizonylat az ELADÁSKORI árat, áfát ÉS nevet tárolja** — nem hivatkozást a termékre.
* **A terméktörzsben is legyen ártörténet** (mikortól meddig mennyi volt). Enélkül a „miért esett a márciusi árrés" kérdésre nincs válasz.

### 12.6 Termék-életciklus `ALAP`

Három állapot: **aktív / inaktív / soft delete**.
**Egyik sem rejti el a TÖRTÉNETBŐL.** Fizikai törlés nincs.

### 12.7 Beszerzési ár és árrés `MVP`

* **Bruttó felvitel** (ahogy a vendéglős a szállítólevelet olvassa).
* **KÖTELEZŐ beszerzési áfakulcs.**
* **Az árrés és a food cost NETTÓ alapon számol.** Mindkét érték tárolva, a felületen mindkettő látszik.

**Miért:** a beszerzés áfája levonható, tehát nem költség. Bruttó alapú árrés
**21–27%-kal hamis** számot adna — és ez a rendszer legfontosabb üzleti riportja.

### 12.8 Allergének `v1` — opcionális kiegészítő funkció

**Kizárólag lehetőséget adunk. Nem kötelező, nincs kapu, és a kihagyásra
SEMMILYEN figyelmeztetés nem jár.** Ez egy kiegészítő funkció, amit kevesen
fognak használni, és így is kezeljük.

| # | Szabály |
|---|---------|
| a | **Az allergén az ALAPANYAGHOZ tartozik.** A termék listája a **receptúrából származtatott** és **élő** — receptmódosításkor magától frissül. A módosítók is beleszámítanak (extra sajt → tej) |
| b | **Kézi felülírás lehetséges** — keresztszennyeződés és készen vásárolt termék miatt kell |
| c | **POS-on „Allergén infó" gomb**, kérésre az előnyugtára is nyomtatható |
| d | **Nincs kötelező kitöltés, nincs mentési kapu, nincs emlékeztető** |

> **Egyetlen biztonsági kikötés, ami nem kényszer és nem kerül semmibe: vagy
> teljes a lista, vagy nincs.** Az „Allergén infó" gomb **csak ott jelenjen meg,
> ahol van adat**, és **részleges lista soha ne látszódjon teljesként** — egy
> félig kitöltött lista veszélyesebb az üresnél, mert teljesnek hiszik.

*A tájékoztatási kötelezettség (1169/2011/EU) az ügyfélé, és attól nem szűnik
meg, hogy a funkciónkat nem használja. Ezért ezt **nem szabad megfelelési
eszközként értékesíteni** — csak kényelmi funkcióként.*

### 12.9 Korhatáros (18+) termékek `v1` — emlékeztető piktogram

**Felugró ablak SEMMIKÉPP.** A jelzés egy **emlékeztető piktogram a felütött
tételek listájában**, a tételsoron — POS-on és vékonykliensen egyaránt.

| # | Szabály |
|---|---------|
| a | **Az ügyfél állítja, kéri-e egyáltalán** a piktogramot |
| b | **Az ügyfél adja meg, mely termékek 18+**, nem mi. A nyilvántartás az ő dolga: az energiaital sokáig nem volt korhoz kötve, most már az — és ez később is változhat. Ha mi szállítanánk a listát, minden jogszabály-változásnál mi lennénk a hibásak egy elavult alapértelmezésért (A3 elv) |
| c | A jelző **kategóriaszinten öröklődhet**, terméken felülírva |
| d | **Nem hárít át jogi felelősséget a pultosra.** Emlékeztető, nem bizonyíték |

> **Miért jobb a felugró ablaknál:** a piktogram **ambiens és tartós** — ott van,
> amíg a rendelés nyitva, nem szakítja meg a munkát, és **nem lehet
> elkattintani.** A felugró ablak pont azért értéktelen, mert elkattintható —
> és el is fogják.

### 12.10 Időszakos árazás és az ár rögzülése `ALAP`

> **Az ár a TÉTEL KOSÁRBA TÉTELÉNEK időbélyegéhez van kötve. Soha nem az asztal
> nyitási idejéhez és soha nem a fizetés idejéhez.**

Így a 17:50-kor felütött sör akciós, a 18:05-ös teljes áras — **ugyanazon a
nyugtán**, és ez így helyes.

| # | Szabály |
|---|---------|
| a | **Általánosítva a happy houron túl:** az ár a **sor létrehozásakor rögzül, és soha nem értékelődik újra.** Egy menet közbeni általános árváltozás sem írja át visszamenőleg a már felütött sorokat — ugyanaz az elv, mint az áfánál (A4: másolás, nem hivatkozás) |
| b | ⚠️ **Határeset: meglévő sor MENNYISÉGÉNEK növelése.** Egy soron nem lehet kétféle ár. **A mennyiségnövelés ÚJ SORT hoz létre az aktuális áron** (vagy rákérdez) — enélkül a modell ábrázolhatatlan állapotba kerül |
| c | Az időszakos kedvezmény az NTAK-ban **önálló tétel** (`EGYEB / KEDVEZMENY`), tehát a nyugtán is megkülönböztethető |

### 12.11 Kiszállítás mint harmadik teljesítési mód `v1`

A teljesítési mód **három** értéket vehet fel: **helyben fogyasztás / elvitel /
kiszállítás.**

| # | Szabály |
|---|---------|
| a | **A kiszállítás az ELVITELI áfamezőt használja** — bármi is legyen benne. **Kulcsot nem égetünk a kódba**, az áfa besorolása az ügyfél felelőssége (§12.2, A3 elv). *(Az 5%-os kulcs az étkezőhelyi vendéglátáshoz, azaz a helyben fogyasztáshoz kötődik; a kiszállítás nem az — de ezt az ügyfél állítja be, nem mi kényszerítjük.)* |
| b | **A kiszállítási díj önálló sor**, `EGYEB / KISZALLITASI_DIJ` NTAK-kategóriával |
| c | **`helybenFogyasztott = false`** az NTAK felé |
| d | **DRS: a csomagolás biztosan a vendéggel távozik** → a visszaváltási díj terhelendő (§14.3 alapértelmezése ezt fedi) |
| e | A külső kiszállító platformokról érkező rendelések **automatikusan kiszállítás módba** kerülnek |

---

## 13. Módosítók és menük

### 13.1 Az alapszabály `ALAP`

> **Az alapállapot a RECEPTÚRA. A módosító MINDIG eltérés vagy fontos egyedi
> kérés → MINDIG nyomtatjuk és MINDIG megjelenítjük a KDS-en. Kivétel nincs.**

A ketchup a hamburger receptjének része, nem módosító. Aki „ketchup nélkül"
opciót akar, **levonó módosítót** csinál rá. Így nem kell minden receptúra-tételt
egyesével automatikus módosítóvá alakítani, és **megszűnik az „alapállapot vs.
eltérés" megkülönböztetés a nyomtatási logikában.**

**Az „előre bejelölt" (`default`) jelző megmarad, de CSAK előválasztásra** — a
kötelező választású csoportoknál (pl. „milyen köret?") gyorsít.
**A nyomtatásra nincs hatása: ami a soron van, az nyomtatódik.**

### 13.2 Levonó módosító `MVP`

* **Be tud nyúlni a szülőtermék receptjébe** — nem elég, hogy saját receptje van, ki kell tudnia venni egy összetevőt a szülő levonásából.
* **ANYAGRA (összetevőre) hivatkozik, nem konkrét receptsorra.** Így egyetlen „Ketchup nélkül" módosító minden olyan terméken működik, aminek a receptjében ketchup van; ahol nincs, ott nem csinál semmit (beállításkor érdemes figyelmeztetni).
* **Visszaírja a készletet** — ez a lényege.
* **Külön fiskális útvonala van** a hozzáadó módosítóhoz képest (§10.4).

### 13.3 Módosítócsoport `MVP`

| Mező | Jelentés |
|------|----------|
| `min` / `max` | **hányat kell / lehet** választani |
| `FreeLimit` | **hányat lehet INGYEN** választani, mielőtt a többi fizetőssé válik |
| **Ingyenes-választás módja** | **legdrágább / legolcsóbb / LEGELSŐ** — **alapértelmezés: LEGELSŐ** |
| Mennyiség módosítónként | Konfigurálható, maximummal |

`min`/`max` és `FreeLimit` **egymástól függetlenül** állítható
(pl. `min=0, max=8, FreeLimit=3`).

**Az ingyenes-választás módját az ügyfél állítja, akár termékenként.**
A csoport adja az alapot, a termék–csoport hozzárendelés felülírhatja.

**A módosítók a készlettől függetlenül választhatók** — a készlethiány nem
tiltja le a módosítót.

### 13.4 Összetett menü `MVP`

**Szerkezet:** terméken „ez menü" jelző + **menükomponensek**; komponensenként
`min`/`max` (alapértelmezés pontosan 1) és választható **termékek**; a rendszer
automatikusan felugrik, amíg minden komponens ki nincs töltve.

| # | Döntés |
|---|--------|
| a | **Felár a komponens–termék PÁROSÍTÁSON**, nem a komponensen („ital: üdítő +0, frissen facsart +390") |
| b | **A menükomponens külön entitás**, nem módosítócsoport — az opciói **termékek**, saját recepttel, készlettel, áfakulccsal, NTAK-kategóriával |
| c | **A menü a nyugtán SZÉTROBBAN a komponenseire.** A menü neve fejléc-szövegsor, alatta a komponensek, mindegyik a saját áfakulcsán |
| d | Az ár szétosztása **a komponensek egyedi listaárainak arányában**, a kerekítési maradék a **legnagyobb komponensre**. **Determinisztikus** |

**Miért kötelező a szétbontás — három független ok:**

1. **Fiskálisan:** vegyes áfakulcsú menü (5%-os étel + 27%-os palackos üdítő) egyetlen sorként nem küldhető, mert két gyűjtőre kell mennie.
2. **NTAK:** nincs vegyes csomagkategória (§11.8).
3. **Készlet:** minden komponens a saját receptjét fogyasztja.

**A komponensek EGÉSZ FORINTOS egységárat kapnak** (§15.2) — így tetszőleges
darabszámmal felszorozva is pontos marad az összeg, és teljesül az NTAK
követelménye, hogy a tételösszesítők összege adja a rendelés végösszegét.

**Példa:** menü 2490 Ft; hamburger listaár 1990 (5%), üdítő 690 (27%).
Arány 1990 : 690 → hamburger 1849, üdítő 641. Összeg **2490**. ✔
3 db menü: 5547 + 1923 = **7470** = 2490 × 3. ✔

*Elvileg egy tisztán ételből álló menü mehetne egyetlen `ETELCSOMAG` tételként.
**Nem élünk vele** — egységesen bontunk: egy kódág jobb, mint kettő.*

---

## 14. DRS — kötelező visszaváltási díj

### 14.1 Tényállás `ALAP`

| Tétel | Tartalom |
|-------|----------|
| **Összeg** | **darabonként egységesen 50 Ft**, nem újrahasználható (egyutas) csomagolásra |
| **Termékkör** | **0,1–3 liter**, fogyasztásra kész vagy koncentrátum italtermék csomagolása — üveg, fém, műanyag |
| **Kivétel** | **tej és tejtartalmú italtermék** |
| **ÁFA** | **NEM része az értékesítés adóalapjának** — az **áfa hatályán kívüli** tétel. A nyugtán **a termék árától elkülönítve** kell feltüntetni |
| **Visszaváltáskor** | **az adóalap nem csökkenthető** a díjjal |
| **Újrahasználható csomagolás** | **más szabály:** az áfatörvény általános betétdíj-szabályai — a díj **benne van** az adóalapban |
| **Visszaváltóhely** | a vendéglátóhelynek **nem kötelező** üzemeltetnie; önkéntes csatlakozás |

Jogszabályi háttér: 450/2023. (X. 4.) Korm. rendelet; NAV 2023-11 adózási kérdés.

### 14.2 A vendéglátásra vonatkozó szabály

Helyben fogyasztásnál, **ha a csomagolás a vendéglátóhelyen marad**, a
visszaváltási díj **nem terhelendő a vendégre**. Elvitelnél, amikor a palack a
vendéggel távozik, **fel kell számítani**, külön tételként, az áfa hatályán kívül.

### 14.3 A mi megoldásunk `MVP`

> **Alapértelmezés: a visszaváltási díj TERHELVE van, teljesítési módtól
> függetlenül.** Beállítási opció üzletenként: *„helyben fogyasztásnál ne
> terhelődjön a vendégre"* — alapból kikapcsolva.

**Miért így:** a gyakorlat az, hogy **helyben fogyasztásnál is kiadják az üveget,
de nem veszik vissza**, vagy egyáltalán nem kezelik a visszaváltást — **és ez a
gyakoribb eset.** A mentesség lehetőség, nem kötelezettség. (A3 + A5 elv)

**A beállítás állapotát a bizonylat mellett rögzíteni kell** — utólag tudni kell,
milyen szabály szerint készült.

### 14.4 Teendők

| # | Teendő | Címke |
|---|--------|-------|
| a | Terméktörzs: **`DRS-köteles csomagolás`** jelző + **`csomagolástípus`** (egyutas / újrahasználható) — a kettő áfakezelése eltér | `MVP` |
| b | A díj összege **központi, verziózott paraméter** (most 50 Ft), **nem konstans a kódban**; a régi bizonylatok a régi értéket őrzik | `MVP` |
| c | A felszámítás a **teljesítési módhoz** kötött. A mód váltásakor **utólag hozzáadható/levehető a nyitott rendelésen**, auditnaplózva | `MVP` |
| d | **Külön nyugtasor a termék alatt, saját gyűjtőn** | `MVP` |
| e | **A díj NEM árbevétel** — átfutó tétel. A forgalmi riportokból, a jutalékalapból és a napi zárás forgalmi számából **ki kell venni** | `MVP` |
| f | Visszavétel (a vendég hozza a palackot): a protokoll natívan támogatja (negatív mennyiség), **de a hely nem kötelezett visszaváltóhely lenni** | `v1/v2` |
| g | **DRS-egyenleg** (beszerzésen kifizetett vs. visszaváltással visszakapott) | `v2` |

`[NYITOTT]` **Melyik gyűjtőre mehet a visszaváltási díj.** A 8 fix rekeszben
nincs DRS-hely; a TAM az egyetlen jelölt, **de a TAM „tárgyi adómentes", ami nem
azonos az „áfa hatályán kívülivel"**. NTAK-oldalon `E_0` a valószínű hely.
**Ez a tényleges beüzemelés része lesz** — előtte gyártói egyeztetés, mert lehet,
hogy náluk már megoldott.

### 14.5 Repohár `v1`

Standard termékként kezelve (+ érték); a **visszavétel** (− érték) automatikusan
**készpénz-kifizetési tranzakciót** indít a fiókból, hogy a kasszaegyenleg pontos
maradjon.

---

## 15. Pénz, kerekítés, valuta

### 15.1 Bruttó alapú számolás `ALAP`

**Ha az árlistán 1500 van, akkor 1500 az igazság**; a nettó és az áfa ebből
származik.

> **A visszaszámolás ÁFAKULCS-CSOPORTONKÉNT, BIZONYLATSZINTEN történik, nem
> soronként** — mert a pénztárgép is így számol, és a soronkénti kerekítés
> garantáltan 1–2 Ft eltérést szül a mi összesítőnk és a gép nyugtája között.

### 15.2 Pénz-ábrázolás `ALAP`

| Típus | Használat | Tárolás |
|-------|-----------|---------|
| **Ár / összeg** | eladási ár, sorösszeg, végösszeg, fizetés | **egész forint (int64)** |
| **Egységköltség** | beszerzési egységár, mozgóátlagár, receptösszetevő | **nagy pontosságú tizedes (6 tizedes)** |

**Lebegőpontos szám pénz közelében SEHOL.**

> **Egész forint mindenütt.** Az adóügyi eszköz forintban törtet nem kezel, az
> NTAK viszont igazítható hozzá, amíg az összeg stimmel — **ezért az egész forint
> a meghatározó, és egységes.**
>
> Technikailag is jobb: **az egész egységár mennyiséggel pontosan szorzódik.**
> Tört egységár + egész sorösszeg esetén 3 db menünél soronként kerekítenénk, és
> a három sor összege nem feltétlenül adná ki a 3× menüárat — pont az NTAK
> követelményét sértenénk meg.

A nagy pontosságú egységköltség azért kell, mert **1 gramm liszt ára valóban
tört forint**, és egészre kerekítve egy 200 adagos recept költsége
nagyságrendekkel elcsúszik.

### 15.3 Kerekítés `ALAP`

* **Csak készpénzes fizetésnél, 5 Ft-ra.**
* **Vegyes fizetésnél a KÉSZPÉNZES RÉSZRE** vonatkozik, nem a végösszegre. 1234 Ft-ból 1000 kártya + 234 készpénz → a készpénzes rész **235**.
* **Mi számoljuk, elküldjük, és a gép válaszát összevetjük.** Eltérés esetén a bizonylat **nem záródhat le csendben** — hiba, kezelői beavatkozással (A2 elv).

### 15.4 Valuta (EUR) `MVP`

* **Árfolyam a napnyitás előtt megadva, felülírásig érvényes.**
* **A pénztárgép saját valutaárfolyam-beállítását is ki kell írni és vissza kell olvasni** — különben a nyugtán más árfolyam szerepel, mint a rendszerben.
* **A bizonylat tárolja a felhasznált árfolyamot.**
* **Ha napnyitáskor nincs árfolyam:** az előzőt viszi tovább **feltűnő figyelmeztetéssel**, **nem blokkol**. (Reggel 6-kor senki nem fog árfolyamot keresgélni; a blokkolás azt eredményezné, hogy kikapcsolják a valutaelfogadást.)
* **Visszajáró forintban.**
* **Csak készpénzre.** Kártyás valutát a terminál kezel.

---

## 16. Fizetés, kedvezmény, szervizdíj, borravaló

### 16.1 Fizetési biztonság — állapotgép `ALAP`

* **Bankkártya-fizetésnél két fázisú véglegesítés (two-phase commit).**
* **Terminál-timeout esetén UI-megerősítés** (Igen / Megszakítás) — soha nem automatikus feltételezés.
* **Összegmódosításnál** megszakítás + újraküldés.
* **Sztornónál automatikus refund parancs.**
* **Nyomtatóhiba esetén függő tranzakció** — nem néma elnyelés.
* **Internet-figyelmeztetés a kártyás fizetés ELŐTT:** a meglévő internet-jelző
  (§6.5) össze van kötve a fizetési folyamattal, hogy a személyzet a fizetés
  megkezdése előtt tudja meg, ne egy 45 másodperces időtúllépés után.
  **A szöveg tényt közöl, nem ír elő megoldást:** *„Nincs külső internetkapcsolat.
  A kártyaterminál valószínűleg nem fog működni."* — **kerülőutat felajánlani
  tilos** (A8 elv, §19.5).

### 16.2 Ki nyomtat `ALAP`

**A KLIENS nyomtat**, mert nála van az adóügyi eszköz és a nyomtató.
**Kivétel: a vékonykliens** — helyette a szerver.

**Az „előzetes szándékrögzítés a szerverre" ELVETVE**, két okból:
a szerver nem kerülhet minden nyomtatás kritikus útjába (akadozó szervernél
minden nyugta várna), és **szerver nélkül a vészhelyzeti mód sem működne**.

**Elfogadott kockázat:** ha a kliens kinyomtat, majd meghal a jelzés előtt, a
pénztárgépben van egy lezárt adóügyi bizonylat, amiről a rendszer nem tud.
**Feloldás: támogatói úton, az adóügyi eszköz saját naplójából.**

**Enyhítés, ami nem sérti a döntést:** a kliens a nyomtatási szándékot
**HELYBEN** rögzíti (ugyanabba a helyi outboxba, ami degradált módban amúgy is
működik) a gép hívása előtt. **Költsége: egy helyi lemezírás, nulla hálózat,
nulla szerverfüggés.** Áramszünet/összeomlás után — a tipikus eset — a bizonyíték
megvan; fizikailag megsemmisült gépnél úgyis támogatás kell.

### 16.3 Fizetési módok `MVP`

* Készpénz (kerekítéssel), bankkártya (integrált vagy kézi), utalvány, valuta.
* **Vegyes fizetés** támogatott.
* **Nyugta opcionális nyomtatása** hőnyomtatón, ahol nem kötelező.
* **QR-kódos vevőkód** a digitális bizonylathoz.

### 16.4 Kedvezmény `MVP`

* **Végösszegi kedvezmény ÁFA-kulcs arányosan szétosztva a tételeken** — így nem keletkezik rossz gyűjtőre kerülő összeg.
* Kedvezmény adható tételre, asztalra, végösszegre.
* **Küszöb feletti kedvezmény indokot igényel**, és auditnaplózott (§18.4).
* **Az NTAK-ban a kedvezmény önálló tétel** (`EGYEB / KEDVEZMENY`).

### 16.5 Szervizdíj `MVP`

* **Áfakulcsonként bontva számolandó**, mert a fiskális gyűjtőkiosztásban **saját, áfakulcsonkénti rekeszei vannak** (§10.3).
* **Nem olvasztható a termék tételébe.**
* **Az NTAK-ban is önálló tétel** (`EGYEB / SZERVIZDIJ`).
* **Elgépelés-védelem:** **puha megerősítés konfigurálható küszöb felett**
  („Biztosan 25%? Ez szokatlanul magas."), alapértelmezett küszöb 15%; **kemény
  korlát csak abszurd értéknél** (100% felett), mert az bizonyosan mellényúlás.
  **Kemény 15%-os plafont NEM teszünk** — nincs jogszabályi felső határ, és az
  sértené az A3 elvet (egy rendezvényhelyszín szerződéses szervizdíja lehet magasabb).
* **Valós jogi követelmény:** a szervizdíj mértékét **előzetesen közölni kell**
  (ártájékoztatás). A rendszer támogassa az árlistán/étlapon megjelenő szöveget.

### 16.6 Borravaló `MVP`

* **Készpénzes borravaló:** kivétel a műszak végén.
* **Kártyás borravaló:** külön riportálva a könyvelésnek, **nem módosítja a fizikai kasszát**.
* **Az NTAK napi zárás tartalmaz `osszesBorravalo` mezőt** → nap szinten is összesíteni kell.
* **Az NTAK-ban önálló tétel** (`EGYEB / BORRAVALO`).
* **Felhasználónkénti borravaló-riport** a felhős admin felületen, a hó végi
  bérszámfejtéshez. `MVP`
* **Miért nem mehet a fiókból:** ha a kártyás borravalót a műszak végén készpénzben
  veszik ki a fiókból, **a fizikai kassza hiányba kerül** a záráskori elváráshoz
  képest. **A szabály: soha nem lehet nyomkövetetlen fiókkivét.** Ha az ügyfél
  mégis készpénzben fizeti ki, az **önálló, bizonylatolt készpénzmozgás**, nem
  néma fiókcsökkentés.
* `[IGAZOLANDÓ]` **A borravaló adózása** (borravaló vs. felszolgálási díj, készpénz
  vs. kártya) nem triviális — könyvelői/adótanácsadói kérdés. A tervezési
  következmény (felhasználónkénti riport) mindkét kimenetel mellett ugyanaz.

### 16.7 Számlázás és a nyugta–számla kizárás `ALAP`

ÁFÁ-s számla: Számlázz.hu / Billingo API, **vagy** adóügyi nyomtatón
„Egyszerűsített számla".

> **Kölcsönös kizárás — kötelező.** Ha a vendég áfás számlát kap ÉS a tranzakciót
> a fiskális eszközön is lezárják, ugyanaz az értékesítés **kétszer kerül be a
> hatóság felé** — egyszer a pénztárgép adatszolgáltatásán, egyszer az Online
> Számla rendszeren. A bevétel felfújva jelenik meg, és az eltérést az
> adóalanynak kell magyaráznia.

**Két külön útvonal kell, nem egy tiltás:**

| Útvonal | Mikor | Menete |
|---------|-------|--------|
| **A) Eleve számlás** | A vendég a fizetés ELŐTT kéri | A kosár **számlás módba** kapcsol → **a fiskális eszköz felé nem megy semmi**; amit papíron kiadunk, azon **„NEM ADÓÜGYI BIZONYLAT"** |
| **B) Utólagos számlaigény** | A nyugta már kinyomtatva | **A nyugtát SZTORNÓZNI kell**, és csak utána állítható ki a számla |

**A B) a gyakoribb** — a vendég a nyugta láttán kéri a számlát.

| # | Kikötés |
|---|---------|
| a | **Szoftveres reteszelés:** számlás módban a fiskális adapter hívása **szerkezetileg lehetetlen**, nem csak letiltva |
| b | A bizonylat **tárolja, melyik útvonalon készült** |
| c | **Az NTAK felé mindkét útvonal ugyanúgy jelentendő** — az NTAK a forgalomtól függ, nem a bizonylat típusától |

### 16.8 Utalványok `v1`

**Kétféle utalvány van, ellentétes adókezeléssel** (áfatörvény, az uniós
utalvány-irányelv átültetése):

| Típus | Mi az | ÁFA ELADÁSKOR | ÁFA BEVÁLTÁSKOR |
|-------|-------|---------------|-----------------|
| **Egycélú** | A beváltáskori adómérték és a teljesítés helye **már eladáskor ismert** (pl. „1 db pizza") | **Adóztatandó** | nincs újabb |
| **Többcélú** | Bármire beváltható, vegyes adómértékkel (klasszikus ajándékutalvány) | **Áfa hatályán kívül** | **Ekkor keletkezik az adófizetési kötelezettség** |

**Egyetlen „Utalvány" terméktípus NEM elég** — kell **`utalvány` jelző +
`utalványtípus`** a terméktörzsben.

| # | Teendő |
|---|--------|
| a | **Többcélú eladása áfa hatályán kívül** → **ugyanaz a gyűjtő-probléma, mint a DRS-nél** (§10.3): nincs szabad rekesz. **A kérdés összevonva a DRS-kérdéssel** a gyártó/NAV felé |
| b | **A beváltás FIZETÉSI MÓD, nem termék.** A beváltott tételek normál módon adóznak és jelentendők |
| c | `[IGAZOLANDÓ]` Az NTAK-besorolás a többcélú utalvány ELADÁSÁRA — valószínűleg `EGYEB / NEM_VENDEGLATAS`, de forrásból ellenőrizendő |
| d | **Kintlévő utalványok nyilvántartása** (kiadott / beváltott / lejárt) — kötelezettség a mérlegben. `v2` |

### 16.9 Számlamegosztás (split bill) `MVP`

**Két megosztási mód van:**

| Mód | Mit csinál | Nehézség |
|-----|-----------|----------|
| **Egyenlő bontás (n felé)** | A teljes számlát n részre osztja | **Kerekítés** + az áfa és a szervizdíj arányos hozzárendelése |
| **Tételes bontás (ki mit evett)** | Mindenki a saját tételeit fizeti | A **megosztott tételt** (egy üveg bor négyüknek) tovább kell bontani |

| # | Szabály |
|---|---------|
| a | **Determinisztikus maradékelosztás:** 10 000 / 3 → 3 333 + 3 333 + **3 334**. Ugyanaz a bontás mindig ugyanazt adja |
| b | **A bontás ÁFAKULCSONKÉNT történik, nem a végösszegen.** Vegyes kosárnál minden résznek arányos áfaszerkezetet kell kapnia — különben a gyűjtőkre rossz összeg megy |
| c | **A szervizdíj ugyanígy arányosodik**, áfakulcsonként (§16.5) |
| d | **Minden rész ÖNÁLLÓ bizonylat, saját SIDURI számmal** — a napi folyószámos séma ezt kezeli (§8.1) |
| e | `[IGAZOLANDÓ]` Az NTAK-ban egy szétbontott számla **egy** rendelésösszesítő több fizetési móddal, vagy **több** rendelésösszesítő? A bizonylatonkénti bontás a valószínűbb |

### 16.10 Előleg és asztalfoglalás `v1`

| # | Elem |
|---|------|
| a | **Az előleg átvétele ELŐLEGSZÁMLÁT igényel** — a megfizetés napján adófizetési kötelezettség keletkezik |
| b | **„Előleg beszámítása" FIZETÉSI MÓD** a fizetési felületen, legfeljebb a végösszeg erejéig. A maradékot normál módon fizetik, majd **VÉGSZÁMLA** készül |
| c | `[IGAZOLANDÓ]` **Az előleg nem megy az NTAK-ba** (nincs konkrét fogyasztás); a fogyasztás napján a teljes összeg jelentendő, és az előleg fizetési mód |
| d | ⚠️ `[KÉRDÉS a könyvelőnek]` **Milyen áfakulcson adózik az előleg**, ha vegyes adómértékű jövőbeni fogyasztásra veszik fel (5%-os étel + 27%-os ital)? Meg kell osztani, vagy a feleknek meg kell határozniuk. **Ugyanaz a probléma, mint a vegyes menünél** (§13.4) |
| e | **Fel nem használt előleg** (nem jelennek meg) — önálló számviteli esemény. `v2` |

---

## 17. Készlet, receptúra, beszerzés

### 17.1 Raktárak `MVP`

* **Korlátlan raktár** (Főraktár, Pult, …), **raktárközi mozgások bizonylatolva**.
* **Receptúrák (BOM)** kezelése, összetevőkkel és mennyiségekkel.

### 17.2 Bevételezés és mozgóátlagár `MVP`

* Beszerzési egységár megadása → **mozgóátlagár** karbantartása.
* **Bruttó felvitel + kötelező beszerzési áfakulcs; az árrés nettón** (§12.7).
* **Árrés (margin) kalkuláció**, teljesítési módonként bontva (§12.3).

### 17.3 Személyzeti fogyasztás és selejt `MVP`

**Szigorúan KÉSZLETMOZGÁSKÉNT rögzítve, nem eladásként** — tiszta könyvelés.

`[IGAZOLANDÓ]` Hogy ezek tényleg nem NTAK-kötelesek. Az NTAK ismer
`EGYEB / NEM_VENDEGLATAS` tételkategóriát, de a rendelésbesorolás értékkészlete
csak `NORMAL / SZTORNO / HELYESBITO`. Ha kiderül, hogy jelenteni kell, a 24 órás
rendeléskorlát (§11.4) rájuk is vonatkozik.

### 17.4 Leltár (standolás) `MVP`

* **Az EGYETLEN jogos készlet-„felülírás"** — de **korrekciós mozgásként**, hogy az eltérés kimutatható maradjon. A készletszám soha nem íródik felül nyom nélkül.
* **Fordulónapi elszámolás**, nem a rögzítés időpontjához.
* **Beállítható „kalkulált veszteség %"** (pl. 2% csapolási veszteség) a hiány tolerálására.
* **A leltári felülírás indokot igényel** és auditnaplózott.
* PDA-modul vonalkódolvasással; **papíralapú standív** generálható és utólag felrögzíthető.

### 17.5 Módosítók és készlet `MVP`

* **A módosítók a készlettől függetlenül választhatók** — készlethiány nem tiltja le őket.
* **A levonó módosító visszaírja a készletet** (§13.2).

### 17.6 A készlet SOHA nem blokkolhat eladást `ALAP`

> **A készlet állapota SOHA nem blokkolhatja a POS értékesítést.** Ha egy
> bevételezés elmaradt és a szoftveres készlet nullát mutat, a vendégnek akkor is
> ki kell adni a fizikailag meglévő terméket.

| # | Szabály |
|---|---------|
| a | **A mínuszos készlet a pultos felé láthatatlan** — neki a készlettel nincs dolga. A menedzsment felé a felhős admin **egyértelmű piros jelzéssel** mutatja |
| b | **A későbbi bevételezés a mínuszt automatikusan feltölti** |
| c | **A „mínuszos készlet" és az „elfogyott" KÉT KÜLÖN dolog.** A mínusz adathiba → nem látszik a pultosnak. Az **„elfogyott" kézi jelző**, amit a személyzet állít be, és **igenis kiszürkíti a gombot** — az valós információ a vendég felé |
| d | ⚠️ **Numerikus csapda: a mozgóátlagár negatív készleten.** Ha a készlet −5 és bevételezünk 10-et új áron, a mozgóátlag-számítás **negatív bázison értelmetlen eredményt ad**, és onnantól minden árrésszám hibás. A negatív bázist **külön kell kezelni** (a negatív rész az utolsó ismert bekerülési áron), és **jelezni kell**, hogy az adott tétel átlagára korrekcióból származik |

---

## 18. Jogosultságok és audit

### 18.1 Jogosultsági szintek `MVP`

* **Az ügyfél maga is létrehozhat és módosíthat SZINTEKET** (pl. „Pultfőnök"), nem csak egyedi kivételeket kap.
* **Frissítéskor érkező ÚJ jogosultság a meglévő szinteken alapból TILTOTT**, de **feltűnő jelzéssel** — hogy tudjanak róla dönteni (A2 + A5 elv).
* Asztalonkénti jogosultságkezelés.
* **Kilépett dolgozó: soft delete.** A felhasználó nem jelenik meg a listákban és
  nem tud belépni, **de a napló és minden korábbi adat érintetlen marad** — pont
  a későbbi visszaellenőrizhetőség jegyében. A név feloldható marad.
  *(Ez jogilag is rendben van: a jogi kötelezettség teljesítéséhez és jogi
  igények védelméhez szükséges adatkezelésre a törlési jog nem terjed ki.)*

### 18.2 A Siduri admin fiók `ALAP`

**Sérthetetlen:**

* Az ügyfél **nem módosíthatja**, **nem csökkentheti a jogait**, **nem írhatja át a jelszavát**.
* **Fix offline belépés kell** — akkor is, ha a jelszót a frissítés előtt cserélték.
* Javaslat: **telephelyenkénti hitelesítő adat**, **látható audittal**.

### 18.3 Belépés `MVP`

* Teljes képernyős kioszk mód, azonnali bejelentkező képernyővel.
* Felhasználók listázása **avatárokkal és nevekkel**; **csak PIN-t elfogadó** jelszómező.
* **Hardveres belépés:** RFID / NFC kártyaolvasó.

### 18.4 Audit napló `ALAP`

#### Alapelvek

* **Csak hozzáfűzhető** — nincs `UPDATE`, nincs `DELETE`, **adatbázisszinten kikényszerítve**.
* **Hash-lánc** a biztonsági ágon: minden rekord tartalmazza az előző hash-ét → az utólagos átírás vagy kivágás **matematikailag kimutatható**.
* **Felhős horgonyzás:** a lánc aktuális hash-e időnként felmegy a felhőbe. Enélkül a lánc nem véd az ellen, ha valaki **az egész adatbázist** korábbi állapotra állítja vissza.
* **A Siduri admin sem törölheti.** Purge csak kor alapján, felhős archívumba.

#### Rekordtartalom

**Ki** (felhasználó + eszköz + **az akkori** szerepe) · **mikor** (eszközóra +
szerveróra + monoton sorszám) · **mi** · **hol** · **mi volt előtte / utána** ·
és ahol kötelező: **miért** (indokkód + szabad szöveg).

* **A naplórekord a felhasználót KIZÁRÓLAG belső UUID-vel hivatkozza, soha nem
  sima szöveges névvel.** Három okból, amiből kettő nem is adatvédelmi:
  helyes normalizálás; **a hash-lánc túléli a névváltozást** (különben egy
  névváltozás után vagy elavult nevünk lenne, vagy egy megváltoztathatatlan
  rekordot kellene átírni — ami a láncot törné); és **pszeudonimizálási kar**
  marad a kezünkben, ha egy konkrét ügy megkívánja (a **megjelenítő réteget**
  cseréljük, a lánc érintetlen).
  **A szerep viszont PILLANATKÉP marad** (az akkori szerep), mert a jelenlegi
  hazudna. Tehát: **azonosság = UUID (hivatkozás), szerep = pillanatkép (másolat).**

#### KÉT külön áram

| | **(A) Biztonsági / számviteli** | **(B) Működési** |
|---|---|---|
| **Mi kerül bele** | sztornó, kedvezmény, árfelülírás, jogosultság, beállítás, nap-/műszaknyitás és -zárás, átállás, leltári felülírás, óraállítás, fiókynyitás eladás nélkül, integráció ki-/bekapcsolás, kockázatvállalási nyilatkozat | tételfelvitel, asztalmozgás, rendelésállapot — **az asztaltörténet és a felhasználó-történet forrása** |
| **Hash-lánc** | **igen** | nem |
| **Megőrzés** | **8 év** (felhőben) | **1 év** (felhőben) |
| **Helyi megőrzés** | **30 nap** | **30 nap** |
| **Nagyságrend / telephely / nap** | ~150–300 rekord | ~3000–5000 rekord |
| **Éves méret / telephely** | néhány tíz MB | ~0,5 GB |

> **A tárhelyet nem a biztonsági események viszik el, hanem az
> asztaltörténet-nézet** — de az az ügyfélnek adott érték, tehát megéri.
> A hash-lánc viszont csak az (A) ágon indokolt: napi 5000 soron pazarlás és
> lassít, napi 200-on ingyen van. `[MÉRENDŐ]` `MERESEK.md` M18.

#### Indoklást igénylő események

Bizonylat-sztornó · konyhára már elküldött tétel törlése · küszöb feletti
kedvezmény · kézi árfelülírás · leltári felülírás · fiókynyitás eladás nélkül ·
„nem fizetett" lezárás · **integráció ideiglenes kikapcsolása**.

#### Hozzáférés

* **A nyers auditot CSAK MI látjuk.** Az ügyfél nem kap nyers adatbázissor-nézetet; a kért adatokat kiküldjük.
* **Az ügyfél kurált, vizuális nézeteket kap**, célzottan elhelyezve:
  * **asztaltörténet** — egy asztalra kattintva, az adott munkanapra;
  * **felhasználó-történet** — *„bejelentkezett, felütött a 3-as asztalra 1 gyrost, kilépett"*.
  * Szép, könnyen érthető megjelenítés, nem száraz lista.
* **Technikai következmény:** a napló legyen **entitásonként** (asztal, felhasználó, rendelés) hatékonyan lekérdezhető → **indexelési követelmény**. Kell **esemény → emberi mondat** sablonkészlet, **mindhárom nyelven**.
* **Az OLVASÁS nem naplózódik.** Helyette a **jogosultsági beállítások** szabják meg, ki mit láthat. **Következmény: a jogosultságváltozás naplózása felértékelődik** — az lesz az egyetlen nyom arról, ki mihez fért hozzá.

#### Munkajogi figyelmeztetés

**Csak figyelmeztetünk, sablont NEM adunk.** Ez a munkáltató kötelezettsége, és
egy elavuló sablonért minket hibáztatnának.

**A figyelmeztetés ott jelenjen meg, ahol a funkciót használják** (a
felhasználó-történet megnyitásakor), **ne csak egyszer a telepítéskor** — mert az
a nézet **munkavállalói megfigyelés**, függetlenül attól, milyen szépen néz ki.

#### Ha nem lehet kiírni

**Enyhe változat:** előre lefoglalt helyi vésztartalék-pufferbe ír, feltűnő
riasztás, és amint lehet, összefésül. Ha a vésztartalék is betelik, **akkor** áll meg.

---

## 19. Integrációk

### 19.1 Két integrációosztály `ALAP`

> **A választóvonal nem az, hogy melyik integrációról van szó, hanem hogy
> hordoz-e JOGI vagy PÉNZÜGYI következményt.**

| | **A) Védett integrációk** | **B) Ügyfél-eszközök** |
|---|---|---|
| **Mik** | adóügyi eszköz, bankkártya-terminál, NTAK | nyomtatók, KDS, rendeléskijelző |
| **Következmény** | jogi / pénzügyi | tisztán működési |
| **Bekapcsolás** | **csak Siduri** | **az üzletvezető** |
| **Kikapcsolás** | delegált jog, **1 órás lejárattal** | **szabadon, lejárat nélkül** |
| **Beállítás** (cím, hozzárendelés, áthelyezés) | Siduri | **az üzletvezető** |
| **Eszkaláció, felhős értesítés** | igen | nem |
| **Audit** | biztonsági ág | működési ág |

**Miért nem kapja meg a (B) osztály a gépezetet:** egy kikapcsolva felejtett
konyhai nyomtató **két percen belül kiderül** — a szakács szól, hogy nem jön a
jegy. **Önjavító hiba.** Egy kikapcsolva felejtett adóügyi eszköz viszont
**napokig észrevétlen maradhat**, mert a pénz közben folyik.

### 19.2 Ideiglenes kikapcsolás — mit old meg `MVP`

Egy integrált periféria kiesése ma **az egész eladási folyamatot megbénítja**,
holott létezik kézi tartalék:

* Nincs internet a gépen → a bankkártyás fizetés nem megy át, **de van kézzel üthető terminál.**
* Kábelszakadás / elromlott adóügyi nyomtató → **minden nyugta megszakad**, holott van egy önálló pénztárgép, amit tudnának ütni.

**Hatókör: gépenkénti** (az integráció természetes hatókörét követve). Ha az
egyik kassza terminálja halott, a többi zavartalanul dolgozik.

### 19.3 Mit jelent a kikapcsolás integrációnként

| Integráció | Mit jelent | Mi vész el |
|------------|------------|------------|
| **Bankkártya-terminál** | A „Bankkártya" fizetési mód **kézi módra vált** | **A terminál engedélyezési adatai** (jóváhagyási kód, maszkolt kártyaszám, terminálazonosító). A napzárási egyeztetés **kézivé válik**. A bizonylatot meg kell jelölni: **„kézi kártyás fizetés"** |
| **Adóügyi eszköz** | **A jogi bizonylatot egy általunk nem vezérelt eszköz adja ki.** Az adóügyi szám mezője üres marad; amit mi nyomtatunk: **„NEM ADÓÜGYI BIZONYLAT"** | **Kettős munka** — mindkét rendszerbe be kell ütni; az összegek egyezését nem tudjuk ellenőrizni |
| **Nem fiskális nyomtató / KDS** | Átirányítás vagy kihagyás | A konyhai jegy |
| **NTAK** | **SOHA nem kapcsolható ki** | — |
| **Audit napló** | **SOHA nem kapcsolható ki** | — |

**Az NTAK azért kivétel, mert nincs hozzá kézi tartalék** — az adatszolgáltatás
sorba áll és elviseli az offline időt. A kikapcsolása nem áthidalás lenne,
hanem elmaradt adatszolgáltatás.

### 19.4 A kikapcsolás szabályai `MVP`

**A funkció bukási módja, hogy minden „ideiglenes" megkerülés állandósul (A7).**
Ezért:

| # | Szabály |
|---|---------|
| a | **Kötelező lejárat: 1 óra.** Nincs „amíg valaki vissza nem kapcsolja" |
| b | **Kötelező indok** (okkód + szabad szöveg), a **biztonsági** auditágban |
| c | **Tartós, elrejthetetlen sáv** az érintett gépen, amíg aktív. Nem ikon, nem eltüntethető értesítés |
| d | **A sáv a TEENDŐT is mondja meg**, ne csak az állapotot: *„Adóügyi integráció ideiglenesen kikapcsolva — a nyugtát a különálló pénztárgépen adja ki."* |
| e | **A sáv írja ki, mióta van kikapcsolva és mikor jár le** |
| f | **Az üzletvezetői és a felhős áttekintőben** minden telephely és gép kikapcsolt integrációja egy helyen látszik |
| g | **Napzáráskor kötelező nyugtázás**, ha bármelyik **védett** integráció ki volt kapcsolva. **Összevontan** — egy tétel eszközönként és integrációnként, a ciklusok számával és összesített idővel, nem ciklusonként egy bejegyzés |

**Eszkalációs létra:**

| Szint | Ki | Meddig | Mi történik |
|-------|-----|--------|-------------|
| **1. Ideiglenes** | üzletvezető (ha Siduri delegálta) | **1 óra**, ismételhető | indok, audit, tartós sáv |
| **2. Ismétlődés** | — | **3 ismétlés után** | **automatikus értesítés felénk** — ez már valós hiba |
| **3. Tartós** | **kizárólag Siduri** | lejárat nélkül | dokumentáltan; a fiskálisnál a **kockázatvállalási nyilatkozathoz** kötve |

**A lejáratkor ELŐBB tesztelünk, csak utána kapcsolunk vissza:**

1. **Önteszt lefut** — a folyamatban lévő tranzakciók befejezése után, **soha nem közben**.
2. **Sikeres** → **csendben visszakapcsol**, a sáv eltűnik.
3. **Sikertelen** → az integráció **visszakapcsolt állapotba kerül**, **de a sáv azonnal „DÖNTÉST IGÉNYEL" állapotba vált**, és az üzletvezető értesítést kap.

**Miért kell a teszt:** vak visszakapcsolásnál **óránként egyszer valaki egy
sikertelen fizetést vagy megszakadt nyugtát eszik meg** — egy esti műszakban
hatszor. A súrlódás (újra kell kapcsolni) így is megmarad, de nem a pultos
fizeti meg az árát.

**Az állapot és a lejárat szerveroldalon, eszközönként tárolódik** — egy POS
újraindulása nem kapcsolhatja vissza csendben egy törött eszközre, és nem is
hosszabbíthatja meg magától a kikapcsolást.

### 19.5 A kikapcsolást SOHA nem ajánljuk fel `ALAP`

> **A megkerülés felajánlása a megkerülés megtanítása** (A8 elv).

* **Dedikált gomb a beállítások között.** Nincs felugró ajánlat.
* **A hibaüzenet iránymutat, de nem kínál kart:** *„A bankkártya-terminál nem elérhető. Szóljon az üzletvezetőnek."*
* **Az ismétlődő hiba a JOGOSULTHOZ jusson el, ne a pulthoz** — az üzletvezetői és felhős riasztási felületen, nem felugró ablakként a kasszán.

**Az adóügyi integrációra szigorúbb szabályok**, mert **a kikapcsolása pontosan
az a kar, amivel egy műszakot nyugtaadás nélkül le lehet vezetni**:

| # | Szabály |
|---|---------|
| a | A kikapcsolás joga **alapból NEM delegálható** — telephelyenként, kifejezetten mi engedélyezzük |
| b | **Azonnali értesítés a felhőbe**, nem napzáráskor |
| c | **Külön riport:** mennyi forgalom keletkezett, amíg ki volt kapcsolva |
| d | A delegálás **a kockázatvállalási nyilatkozathoz kötve** |

*Maga a helyzet jogszerű — egy különálló pénztárgépen kiadott nyugta érvényes
nyugta. A kockázat nem jogi, hanem visszaélési.*

### 19.6 Nyomtatás átirányítása másik gép adóügyi eszközére `v1`

**Megvalósítható**, mert az adóügyi eszközzel a kommunikáció **IP:port alapú**.
**Csak Siduri rendszergazda állíthatja**, mert problémaforrás.

| # | Kikötés |
|---|---------|
| a | **Telephelyen belülre KEMÉNYEN korlátozva, szerveroldalon kikényszerítve** — nem admin-fegyelemre bízva. Másik telephely eszközére nyomtatni **más NTAK-regisztrációs számot és esetleg más adóalanyt** jelentene: súlyos szabálysértés |
| b | **A bizonylatnak tárolnia kell, MELYIK adóügyi eszköz nyomtatta** (§8.3) |
| c | **Az átirányítás beállítása és minden átirányított nyomtatás auditnaplózott** |
| d | **A felhasználónak látszania kell**, hogy máshol nyomtat — különben a pult mellett várja a papírt |

### 19.7 Integráció-nyilvántartás `ALAP`

Minden integrációra rögzítve: **a neve · az OSZTÁLYA (A vagy B) · bekapcsolható-e
ezen a telephelyen · kikapcsolható-e ideiglenesen · ki által · mi a tartalék
viselkedés · mi vész el vele · a maximális időtartam · a hatóköre (gépenkénti
vagy telephelyi).**

**Ez nem konfigurációs apróság, hanem terméktulajdonság-katalógus** — és ugyanez
a nyilvántartás szolgálja ki a **fizetős csomagokat és licencszinteket** (§2.1).

### 19.8 Hardver és periféria `MVP`

* NAV-engedélyes adóügyi pénztárgépek integrációja gyártói szoftveren keresztül.
* Hagyományos bankkártya-terminálok (a SoftPOS mellett) — **ugyanaz az elv: integrálunk, nem írunk sajátot.**
* Széleskörű **hőnyomtató (ESC/POS)** támogatás.
* Vonalkódolvasó, RFID/NFC olvasó.
* **Mérleg és tára** `v1`: **`súlyra mért` kapcsoló a terméktörzsben**; felütéskor
  a gép a mérlegről veszi az adatot. **„Tára" gomb** az edény/csomagolás súlyának
  levonására. **A mérleg hitelesített kell legyen** (mérésügyi követelmény, ha a
  mérés határozza meg a fogyasztói árat) — **az ügyfél kötelezettsége**, mi
  jelezzük. **(B) osztályú ügyféleszköz** (§19.1). **Ha nem válaszol, kézi
  bevitelre esünk vissza — soha nem blokkolunk** (§17.6).
* **Kasszafiók-állapotfigyelés** `v2`: ahol a hardver mikrokapcsolója támogatja,
  az üzletvezető engedélyezheti. ⚠️ **A szenzor gyakran nincs vagy nincs bekötve
  — a funkciónak magától fel kell ismernie, hogy érkezik-e jel, és ha soha nem,
  akkor NE legyen bekapcsolható.** Egy csendben soha meg nem szólaló biztonsági
  funkció **rosszabb a semminél**, mert hamis biztonságérzetet ad (A2 elv).
  A küszöb **konfigurálható, 2–3 perces alapértékkel** (60 másodperc kevés:
  csúcson a fiók jogosan marad nyitva vendégek között), a jelzés **elsősorban
  vizuális** — hangos helyen a hangjelzés értéktelen.

### 19.9 Külső API `v2`

* **Foodora / Wolt** natív KDS- és POS-integráció.
* **CRM és hűségprogram API.**
* Nyilvános REST API.

---

## 20. Nyomtatás és routing

* **Blokk-kiosztás (routing):** melyik terméktípus melyik nyomtatóra vagy KDS-re megy.
* **Előnyugta (proforma) nyomtatása után „fizetésre vár" státusz**; új tétel esetén automatikus visszaváltás.
* **Ami módosítóként a soron van, az MINDIG nyomtatódik és MINDIG kimegy a KDS-re** (§13.1).
* **Az ár nélküli módosító szövegsor a termék alatt**, nem tétel.
* **A menü fejléc-szövegsorként jelenik meg, alatta a komponensek** (§13.4).
* **A fiskális nyugta magyar** — jogszabályi kötöttség (§25).

### 20.1 Fogások késleltetett küldése `MVP`

Ha a vendég egyszerre rendel levest, főételt és desszertet, és mindhárom
egyszerre megy a konyhára, **a főétel kihűl, mire a leves elfogy.**

| # | Szabály |
|---|---------|
| a | **Fogás-címke a tételsoron** (1., 2., 3. fogás vagy előétel/főétel/desszert) |
| b | **Küldéskor csak az aktuális fogás megy** a KDS-re/nyomtatóra |
| c | **„Következő fogás indítása" gomb** — POS-on **és** vékonykliensen |
| d | **A KDS lássa a VISSZATARTOTT fogásokat is**, elkülönítve („jön, de még ne kezdd") — különben a konyha nem tud előre tervezni |
| e | **Opcionális automatikus indítás:** a következő fogás magától elindul N perccel azután, hogy az előzőt késznek jelölték. **Alapból kikapcsolva** |
| f | **Nem kivétel a §13.1 nyomtatási szabálya alól:** a fogás-állapot a **továbbítást** kapuzza, nem a módosító-szabályt. Ha egy fogás elmegy, **minden módosítója vele megy** |

---

## 21. Kliensek

### 21.1 POS (vastagkliens) `MVP`

* Teljes képernyős kioszk mód, azonnali bejelentkezés (§18.3).
* **Étterem (asztaltérkép) nézet:** vizuális szerkesztő — rajzolható háttér, asztalok elhelyezése, alakja, testreszabása.
* **Asztalhoz rendelhető:** dedikált felszolgáló, törzsvendég-profil, asztal-szintű kedvezmény.
* **Rendelésfelvétel:** asztalra vagy konkrét vendéghez rendelve; alapértelmezett vendégszám automatikus felajánlása.
* **Jobb oldali panel nézetei:** felütés sorrendje / vendégenként / fogásonként (összevont nézettel).
* **Értékesítési nézet:** gyors eladás és asztal nézet.
* **Egygépes, asztalkezelés nélküli mód** — az ingyenes belépő szint (§2.1).
* **Versenyhelyzet-védelem:** optimista zárolás verziószámmal az asztalszerkesztéseknél.
* **Újracsatlakozás:** exponenciálisan növekvő várakozás, **leállási határral**.

### 21.2 Vékonykliens (PDA) `MVP`

* Rendelésfelvétel és -kezelés.
* **v1-ben NEM fizettet és NEM ad nyugtát.**
* **A fizetési képesség MEGÉPÜL, de kikapcsolva.** **Nem fordítási kapcsoló**, hanem **szerveroldali, az admin felületen meg nem jelenő jogosultság**, amit a kliens minden fizetési kísérletnél megkérdez — így helyi fájl átírásával nem oldható fel, és a **bekapcsolás auditnaplózható**.
* **Szerverhiba esetén automatikus leállás** — védelem a dupla felütés ellen.
* **Minimális archívum:** csak amit ő küldött, **rövidebb megőrzéssel** — adatvédelmi okból, mert a telefon a leggyakrabban elveszített eszköz.
* **Az eszközszám-tér KÖZÖS** minden eszköztípussal (§8.2).

### 21.3 KDS `MVP`

Érintőképernyős (Android / Windows) kijelző, **drag-and-drop státuszváltással**,
ami **triggereli a vevőhívót**.
**Minden módosító megjelenik rajta** (§13.1).

### 21.4 Rendeléskijelző (vevőhívó) `v1`

Különálló, **arculatosítható** alkalmazás (Smart TV / Android),
**WebSocket** kommunikációval: „Készül" / „Átvehető".

### 21.5 Másodkijelző (vendégtájékoztató) `v1`

Rendelés és borravaló felület; **idle állapotban videó/kép lejátszása**,
automatikus konvertálással (720p / 1024×768).
`[MÉRENDŐ]` Bay Trail integrált GPU-n ez nem triviális (`MERESEK.md` M3).

### 21.6 Kioszk `v2`

Önkiszolgáló rendelő és fizető terminál.

### 21.7 Standoló alkalmazás `v1`

PDA-modul vonalkódolvasással; **weben generálható papíralapú standív** és
utólagos felrögzítés.

### 21.8 QR-kódos asztali rendelés `v2`

Vendégoldali rendelés **közvetlenül a helyi szerverre**.

---

## 22. Felhő

### 22.1 A felhő szerepe `ALAP`

**Teljes menedzsment-platform, nem kiegészítő.** Ez a legnagyobb
scope-változás a projektben, és **önálló terméksáv a fázistervben.**

| # | Terület |
|---|---------|
| a | **Beállítás-paritás a POS-szal** — a felhőnek MINDEN POS-beállítást ismernie kell |
| b | **Raktár, alapanyag-mozgás, receptúrázás** — ugyanaz, mint a telephelyi admin |
| c | **Riportok, grafikonok, statisztikák** |
| d | **Leltár** — dedikált funkció, ami felülírhatja a készletet (korrekciós mozgásként, §17.4) |
| e | **Zárolható beállítások** (ár, láthatóság) — a lánc/franchise központ zárolhat értékeket |
| f | **Üzletlánc / franchise szintű központi értékek**, öröklődéssel |
| g | **Visszajelzés arról, hogy a változás leérkezett-e a gépekre** |
| h | **Eszköz-láthatóság** — melyik gép él, mikor jelentkezett |
| i | **Kétirányú, kifejezetten védett szinkron** |

### 22.2 Egy admin felület, két helyről kiszolgálva `ALAP`

> **EGY webes admin alkalmazás van, KÉT helyről kiszolgálva:** a felhőből, és
> offline esetén **a telephely saját szerveréről**.

**Ez szünteti meg a gyökerénél a néma szétcsúszás veszélyét** — ha két külön
adminfelület lenne, azok idővel különböző dolgokat tudnának, és senki nem venné
észre.

**A felhő raktár/receptúra ugyanaz, mint a telephelyi.**

`[MÉRENDŐ]` A telephelyi szerver webes admint is kiszolgál — a J1900-on ennek
terhelése mérendő (`MERESEK.md` M14).

**Offline korlát:** a telephelyi kiszolgálás **30 napnál régebbi adatot nem tud
mutatni** (a helyi megőrzés miatt, §24.2). Ezt a felület mondja meg, ne csendben
üres eredményt adjon.

### 22.3 Több telephely `ALAP`

**Alapmodell, nem franchise-funkció.** Minden kimutatás működjön:

* egy üzletre,
* több kiválasztottra,
* a teljes csoportra.

Nem-franchise tulajdonos is kaphat több telephelyet.

### 22.4 A felhő rendelkezésre állása `MVP`

* **Két fizikai szerver**, fő + másodlagos, **automatikus átcsatornázással** és terheléselosztással.
* **A telephelyi „kézi átkapcsolás" indoklása NEM vihető át:** a telephelyen azért kézi, mert nem uraljuk az infrastruktúrát és nem tudjuk a hálózat állapotát. **A felhőben mi uraljuk** — ott az automatika indokolt.
* **Aktív-passzív írás, aktív-aktív olvasás.**

### 22.5 A felhő mint archívum `ALAP`

**A felhő a jogi archívum** (8 év). A helyi purge (30 nap) csak azért
megengedhető, mert a felhő őrzi. **Ebből következik, hogy a „tisztán lokális"
topológia önmagában nem elegendő** NTAK-köteles helyen.

### 22.6 A felhő mint NTAK-küldő zárvatartás alatt `MVP`

Lásd §11.7/e.

---

## 23. Licenc és jogosultság (DRM)

* **Felhőből kezelt, hardveres ujjlenyomat alapú** licencelés.
* **Heartbeat: 10 napos offline türelmi idő.**
* **A licenc türelmi ideje és a kliens-archívum megőrzési ideje SZÁNDÉKOSAN nem közös érték** — két különböző dolog, nem szabad összekötni őket.
* **Két ujjlenyomat egy azonosítón → mindkettő tiltva**, amíg ember fel nem oldja (§8.2).
* **Licencszintek / fizetős csomagok:** az integráció- és funkciónyilvántartás (§19.7) írja le.

> **A korábbi „NTAK SLA figyelmeztetés 18 óra offline után, a 24 órás limit
> miatt" szabály ÉRVÉNYTELEN** — az adatküldés 15 perces (§11.2). A figyelmeztetés
> logikáját újra kell írni: nem a 24 órás limithez, hanem **a felhalmozódott,
> beküldetlen 15 perces csomagok számához és korához** kell kötni.

---

## 24. Biztonság, adatvédelem, üzemeltetés

### 24.1 Fizikai kockázat `ALAP`

**A szerver jellemzően egy dolgozó pénztárgép** — a teljes adatbázis a pultban
áll, nem egy zárt szerverszobában.

**A fizikai lopás ellen szoftverrel nem lehet teljesen védekezni; ezt ki kell
mondani.** Amit tenni lehet:

| # | Ellenszer |
|---|-----------|
| a | **Adatminimalizálás** — tervezési szabály: ne tároljunk olyat, amire nincs szükség |
| b | **Lemeztitkosítás, ha van TPM.** `[NYITOTT]` A bázison van-e TPM — **mindkét ágra készülünk**, a titkosítás konfigurációs képesség, és az admin felület kiírja, melyik ágon vagyunk |
| c | **Fizikai rögzítés** — telepítési tétel |
| d | **A felhőmentés az EGYETLEN helyreállítási út lopás után** |

### 24.2 Kliens-oldali archívum `MVP`

* **20 FORGALMAS üzleti nap** megőrzése — **nem 20 naptári nap.** Egy zárva töltött nap nem számít bele és nem is öregít ki semmit.
* **A nyugtázatlan adatot a megőrzés SOHA nem törli.**
* **Vékonykliensnél rövidebb** (§21.2).
* **A kliens visszakérheti a saját előzményét a szervertől** → gépcsere után az új gép feltölti magát. Három kikötéssel: a visszatöltött archívum **hiányosabb lehet** (meg kell jelölni), **hitelesített, auditált adatkiadási csatornán** megy, és a **gépcsere explicit, engedélyezett művelet.**
* `[MÉRENDŐ]` Az írásterhelés olcsó tárolón és a tényleges méret (`MERESEK.md` M8, M9).

### 24.3 Hálózat `ALAP`

* **A vendég-wifi és az üzemi hálózat szétválasztása KÖTELEZŐ TELEPÍTÉSI ELŐFELTÉTEL** (§10.6).
* **Kliens↔szerver kommunikáció titkosítva és hitelesítve** — a régi spec ezt egyáltalán nem tárgyalta.
* Tűzfalszabály az adóügyi szolgáltatás portjára.

### 24.4 Kockázatvállalási nyilatkozat `MVP`

Alkalmazásban elérhető űrlap, **érintőképernyős aláírással**, elmentve **ÉS a fő
felhőszerverre továbbítva**, visszakereshetően, időbélyeggel, védve.

**Négy kikötés:**

| # | Kikötés |
|---|---------|
| a | **A SZÖVEG VERZIÓJÁT is menteni kell**, nem csak azt, hogy aláírták |
| b | **KÉT időbélyeg**, és a **mérvadó a felhőé** — a helyi óra az ügyfél gépéé |
| c | **Offline útvonal kell**, mert friss telepítésen gyakran nincs internet — és amíg a felhő nem igazolta vissza, ezt ki kell írni |
| d | **Konfiguráció-eltérés esetén ÚJ nyilatkozat kell**, különben egy már nem létező felállásról van aláírt papírunk |
| e | **Kriptográfiai lezárás:** a **teljes szöveg + dátum + a KONFIGURÁCIÓS ÁLLAPOT** összefűzve, **SHA-256 lenyomattal**, az aláírással együtt a felhőbe. Ez nemcsak azt bizonyítja, melyik szöveget írták alá, hanem hogy **pontosan az a csomag nem változott utólag**, és **hozzáköti az aláírást ahhoz a konkrét konfigurációhoz**, amit elutasítottak. ⚠️ **Őszinte korlát: egy érintőképernyős aláírás + SHA-256 NEM minősített elektronikus aláírás.** Ez bizonyíték, nem eIDAS-megfelelés — és nem is szabad annak beállítani |

**Mikor kell:** ha az ügyfél a kockázat ismeretében elutasítja a tartalék
szervert, a második adóügyi eszközt, vagy a hálózat szétválasztását; és a
fiskális integráció ideiglenes kikapcsolásának delegálásához.

### 24.5 Frissítés `MVP`

* Önálló offline patcher (`siduri-updater`), ami a Windows fájlzárolási problémáit kerüli meg.
* **A frissítés SORRENDJE kemény követelmény:** a szerepeket hordozó gépek (fő és tartalék szerver) nem frissülhetnek egyszerre.
* **Frissítéskor érkező új jogosultság alapból tiltott, feltűnő jelzéssel** (§18.1).

### 24.6 Windows Update a szerepet vivő gépen `ALAP`

> **A teljes HA-rendszert a szerver HARDVERHIBÁJA ellen építettük. Közben a
> sokkal valószínűbb esemény az, hogy a Windows Update szombat este 20:00-kor
> újraindítja a szerverként dolgozó pénztárgépet — és ez teljesen megelőzhető.**

Rosszabb: a failoverünk **kézi** (5 perc után ember nyom gombot). Egy
Windows-újraindítás tehát **5+ perc csökkentett módot és egy emberi döntést**
okoz, csúcsidőben, feleslegesen.

| # | Teendő |
|---|--------|
| a | **A telepítés kötelezően letiltja az automatikus újraindítást** — Windows 10 IoT Enterprise LTSC-n házirenddel/beállítással megtehető (halasztás + aktív órák + újraindítás-tiltás) |
| b | **KÖTELEZŐ TELEPÍTÉSI ELLENŐRZŐLISTA-TÉTEL**, ugyanabban az osztályban, mint a vendég-wifi szétválasztása (§10.6) |
| c | **Az updater ELLENŐRZI a beállítást**, és ha valaki visszaállította, **jelez — a felhőbe is** |
| d | A frissítési sorrend kemény követelménye (§5.2) **kiterjed az operációs rendszerre is**, nem csak a mi szoftverünkre |

### 24.7 Törzsvendég-adatok törlése (GDPR) `v1`

| # | Szabály |
|---|---------|
| a | **Egygombos anonimizálás** a törzsvendég-profilra. A statisztikák sértetlenek maradnak (a fogyasztási adat a profil-azonosítóhoz kötött, nem a névhez) |
| b | **Nem elég a nevet átírni.** Ki kell terjednie a **telefonszámra, e-mailre, címre, hűségkártya-számra**, és — a legkockázatosabb — a **szabad szöveges megjegyzésekre.** Oda írja a személyzet, hogy „a piros autós fickó", ami önmagában újraazonosít |
| c | **A BIZONYLATOKAT nem érintheti.** A számla nevet és címet hordoz, és **8 évig kötelezően megőrzendő** — **a törlési jog nem írja felül a jogszabályi megőrzési kötelezettséget.** A törlés a **CRM-profilra** vonatkozik, nem a számviteli bizonylatra |

### 24.8 Offline vészmentés (pendrive) `v2`

**A forgatókönyv:** több napig internet nélkül működő telephelyen (fesztivál,
rossz lefedettség, hosszabb szolgáltatáskiesés) a felhőmentés áll. Ha ekkor
fizikailag tönkremegy a fő szerver SSD-je, **a köztes napok adata elvész.**

> **A célcsoport szűkebb, mint elsőre látszik: ha VAN tartalék szerver, az
> SSD-hiba már fedve van** (replika). A pendrive pontosan ott számít, ahol
> **nincs tartalék szerver ÉS napokig nincs internet** — vagyis az egygépes,
> kisméretű telepítéseknél. **Érdekes következmény: a legolcsóbb szintnek van rá
> a legnagyobb szüksége.**

**Menete:** ha a gépben van egy dedikált pendrive (azonosító kulcsfájllal),
a rendszer napzáráskor **titkosított adatbázis-dumpot** ír rá.

| # | Kikötés |
|---|---------|
| a | ⚠️ **MILYEN KULCCSAL titkosítunk?** Ha a kulcs azon a gépen van, ami tönkrement, **a mentés használhatatlan.** A kulcsnak **nálunk kell lennie** (felhőben letétbe helyezve) vagy a telephely licenc-hitelesítőjéből származtathatónak. **Ez a funkció lényege** |
| b | ⚠️ **A gépben hagyott pendrive maga is fizikai kockázat** — a teljes adatbázis, őrizetlenül, egy közönség előtt álló gépben (§24.1). **Ezért a titkosítás nem opció, hanem a funkció feltétele** |
| c | ⚠️ **Az ellenőrizetlen mentés nem mentés.** Az olcsó pendrive-ok csendben hibáznak: **vissza kell olvasni, ellenőrzőösszeget képezni, és az eredményt jelenteni** — különben hamis biztonságérzetet adunk (A2 elv) |
| d | **Napzárás + állítható időköz** — egy 4 napos fesztiválon a napi egy mentés akár egy teljes napot veszíthet. `[MÉRENDŐ]` a dump ideje J1900-on |
| e | **A visszatöltési utat is tesztelni kell**, nem csak a mentést. A nem tesztelt visszaállítás mítosz |

---

## 25. Nyelvek és lokalizáció

**Magyar + angol + német KÖTELEZŐ**; szomszédos nyelvek (szlovák, román, szerb,
horvát) később.

> **Két külön feladat, amit nem szabad összekeverni:**

| | **(1) Szoftverszövegek** | **(2) Tartalom** |
|---|---|---|
| Mi | gombfelirat, hibaüzenet, riportfejléc | terméknév, kategórianév, módosítónév, allergénszöveg |
| Kié | **a miénk** | **az ÜGYFÉL adata**, telephelyenként újra |
| Hogyan | **teljes körű**, mindhárom nyelven | **mezőnként opcionális, MAGYAR visszaesési értékkel** |

**A tartalomfordítást kényszeríteni TILOS** — akkor nem töltik fel a terméktörzset.

**A fiskális nyugta MAGYAR** — jogszabályi kötöttség. A többnyelvűség a nem
fiskális példányon, a QR-os vendégoldalon, az e-nyugta megjelenítésén és a
kijelzőkön él.

> **A POS-felületet NÉMET szövegekkel kell tesztelni, nem magyarral.** A német
> átlagosan 25–35%-kal hosszabb, az angol rövidebb — a J1900-as gépek kis
> felbontású érintőképernyőjén a német tördel. **Elfogadási kritérium a UiUX
> körben.**

Ha (1) és (2) rendesen fel van építve, egy új nyelv **csak fordítási költség**,
fejlesztési nem.

---

## 26. Riportok és analitika

* **Dinamikus grafikonok a felhőben.**
* **Valós árrés:** a beszerzés **mozgóátlagárán**, **nettó alapon** (§12.7), **teljesítési módonként bontva** (§12.3).
* **Dinamikus „kalkulált veszteség %" csúszka** a tiszta profit modellezéséhez.
* **Elviteles arány költsége** — mennyibe kerül a tulajdonosnak a takeaway (§12.3).
* **DRS a forgalmi számokból KIVÉVE** — átfutó tétel, nem árbevétel (§14.4/e).
* **Integráció nélkül keletkezett forgalom** — külön riport (§19.5/c).
* **Sztornó- és törlési anomália riport** `v1`: dedikált mutató a felhős BI-ban,
  **utólagos elemzésre — valós idejű riasztás NINCS**, mert az téves
  gyanúsítgatást szülne.

  | # | A mérőszám helyes definíciója |
  |---|------------------------------|
  | a | **Nem a nyers törlésszám a jel, hanem az ARÁNY** — a saját forgalmához és az **összehasonlítható műszakot dolgozó társakhoz** viszonyítva. Egy pénteki csúcsműszak abszolút értékben mindig több törlést hoz |
  | b | ⚠️ **Állapot és idő szerint minősítve.** A felütés után 10 másodperccel törölt tétel **elgépelés**. A visszaélés mintája szűkebb: **a konyhára MÁR ELKÜLDÖTT tétel törlése, FIZETÉS ELŐTT.** Mindent egy kalap alá véve a mutató használhatatlan |
  | c | **Kombinált nézet:** magas törlési arány **ÉS** sok „nem fizetett" lezárás **ÉS** sok küszöb feletti kedvezmény **ugyanattól a személytől** — ez a jel. Egy közös „figyelemfelhívó" nézet többet ér három külön grafikonnál |
* **Asztaltörténet és felhasználó-történet** — kurált, vizuális nézetek a működési auditágból (§18.4).
* Franchise/lánc szinten: egy üzletre, több kiválasztottra, a teljes csoportra (§22.3).

---

## 27. MVP és ütemezés

Részletek: [`MVP_DEFINICIO.md`](MVP_DEFINICIO.md).

### 27.1 Az MVP magja

Offline-first telephelyi működés · szerver-autoritatív modell · **teljes
degradált mód** · **HA tartalék szerverrel** · kétrétegű bizonylat-számozás ·
fiskális integráció (2. üzemmód) · **teljes NTAK adatszolgáltatás** ·
termékkatalógus módosítókkal és menükkel · készlet és receptúra · jogosultságok
és audit napló · alap felhő (licenc, archívum, admin).

### 27.2 Amit az ütemterv NEM tud lerövidíteni `ALAP`

**A csapatlétszám nem korlát. A külső kapuk azok:**

| Kapu | Mit blokkol |
|------|-------------|
| **MTÜ Igazolás + NTAK validációs teszt** | Az élesítést |
| **Gyártói kapcsolatfelvétel + fizikai tesztkészülék** | A fiskális réteg véglegesítését |
| **Fizikai J1900 referenciagépek** (2 db, illetve a teljes referencia-telepítés) | Az M1–M9, M12–M14 méréseket |

**Ezek átfutási idők, nem fejlesztési feladatok.** A fázistervnek ezekre kell
épülnie, nem fordítva.

### 27.3 Az első hét tétele

**Az API-szerződés helye** (`B8`) — hol él, hogyan verziózzuk, ki a gazdája.
Kis csapatnál sem opcionális.

---

## 28. Nyitott kérdések és igazolandó premisszák

### 28.1 Igazolandó premisszák — döntés nem építhető rájuk forrás nélkül

| # | Az igazolatlan állítás | Mi dől meg, ha hamis |
|---|------------------------|----------------------|
| **P1** | AEE-s gépnél a jogi bizonylatot maga az adóügyi eszköz állítja ki és sorszámozza → a szerver kiesése nem akadálya a nyugtaadásnak | **A degradált mód egésze** (§6.2) |
| **P2** | „Teljesen új negatív fiskális nyugta" sztornóra | A teljes sztornó-folyamat (§10.5) |
| **P3** | Az e-nyugta iránnyal most nem kell foglalkozni | A bizonylat-modell alakja |
| **P4** | A személyzeti fogyasztás és a selejt nem NTAK-köteles | A 24 órás rendeléskorlát rájuk is vonatkozna (§11.4) |

*(A korábbi „24 órás NTAK limit" premissza IGAZOLVA HAMIS — 15 perc, §11.2.
A „számviteli megőrzési idő" premissza rendezve: 8 év, felhős archívummal.)*

### 28.2 Nyitott kérdések — külső félhez

| # | Kérdés | Kihez |
|---|--------|-------|
| **K1** | Elfogadja-e a firmware a **nulla összegű tételt**? (munkafeltevés: nem) | gyártó |
| **K2** | **Melyik gyűjtőre mehet a DRS visszaváltási díj?** Újrakiosztható-e az **AJT** rekesz? | gyártó / NAV |
| **K3** | Van-e a gyártói szolgáltatásnak **hitelesítési, IP-korlátozási vagy figyelési-cím** beállítása? | gyártó |
| **K4** | Elfogadja-e az NTAK a **napi zárás UTÁNI rendelésösszesítőt** ugyanarra a tárgynapra? (0–24-es helyen mindennapos) | NTAK / MTÜ |
| **K5** | **NTAK-köteles-e a személyzeti fogyasztás és a selejt?** | NTAK / MTÜ |
| **K6** | Elfogadja-e az NTAK a **múltbeli (utolsó tevékenység szerinti) zárási időbélyeget**, ha a szerver 24 óránál tovább volt halott? | NTAK / MTÜ |

### 28.3 Nyitott kérdések — belső

| # | Kérdés |
|---|--------|
| **B1** | Van-e TPM a meglévő bázison (§24.1/b) — mindkét ágra készülünk |
| **B2** | A „Message Queue" konkrét megvalósítása |
| **B3** | Multi-tenancy modellje a felhőben |
| **B4** | SoftPOS = PSP-döntés, nem fejlesztési döntés |

---

## 29. Mérési kötelezettségek

**Az első éles teszten MINDENT MÉRÜNK.** Teljes lista: [`MERESEK.md`](MERESEK.md).

| # | Mérés | Miért kritikus |
|---|-------|----------------|
| **M1** | Kombinált szerver + pénztárgép EGY J1900-on | A legszűkösebb eset, és **ez az alapértelmezés** |
| **M4** | Szinkron vs. aszinkron replikáció írási válaszideje J1900 páron | A „szinkron kizárt" állítás nincs igazolva |
| **M5** | A failovernél elveszthető tranzakciók száma | Az árva tranzakciók nagyságrendje |
| **M12** | **A LEGKRITIKUSABB: a tartalék POS átveszi a szolgálatot** csúcsterhelés alatt | Az egész HA-terv ezen áll |
| **M13** | A tartalék POS terhelése normál üzemben (csak replikaként) | Ha már ez is elviszi a válaszidőt, az M12 értelmetlen |
| **M14** | A telephelyi szerver webes admint is kiszolgál | §22.2 |
| **M15** | **Elfogadja-e az eszköz a nulla összegű tételt** | §10.4 — blokkoló |
| **M16** | Melyik gyűjtőre mehet a DRS | §14.4 |
| **M17** | Nyomtatási válaszidő és a bizonylat teljes ciklusideje | Hány tétel felett lassul érezhetően |
| **M18** | Az audit napló két ágának tényleges mérete | §18.4 |

**Fizikai hardver kell hozzá:** M1–M9 egy J1900-at, M4/M5/M7/M13 **kettőt**,
**az M12 a TELJES referencia-telepítést** (3 Windows POS + 2 tablet + 4 telefon +
KDS + rendeléskijelző).

---

## 30. Repók

| # | Repó | Tartalom |
|---|------|----------|
| 1 | `siduri-backend-server` | Java / Spring Boot / GraalVM — telephelyi fő és tartalék szerver, PostgreSQL |
| 2 | `siduri-pos-client` | C# / WPF — POS kliens, fiskális és hardveres integrációk |
| 3 | `siduri-flutter-clients` | Flutter workspace — PDA, KDS, rendeléskijelző, standoló |
| 4 | `siduri-updater` | C# — önálló offline patcher |
| 5 | `siduri-cloud-api` | Felhő: licenc, archívum, webes admin, NTAK-tartalék |
| 6 | `siduri-docs` | **Dokumentáció — kód SOHA nem kerül bele** |

**A repók MINDIG privátok maradnak** (§10.2).

---

## 31. Munkamódszer

Részletek: [`MERNOKISAROKKOVEK.md`](MERNOKISAROKKOVEK.md). A legfontosabbak:

| # | Szabály |
|---|---------|
| 1 | **Egy igazságforrás**; minden más mutató, és a mutató mondja ki, hogy mutató |
| 2 | **Soha ne szépítsünk.** Többet árt egy kényelemből elhallgatott információ, mint a kegyetlen valóság |
| 3 | **Minden döntéshez tartozik a KÖLTSÉGE is**, nem csak az előnye |
| 4 | **Nincs semmitmondó hivatkozás** — mindig ki kell írni, miről van szó |
| 5 | **Az elvetett alternatívát nem töröljük, hanem áthúzva megtartjuk** az indoklással |
| 6 | **A saját tévedést helyesbítjük, nem elfedjük** |
| 7 | **Nincs AI-attribúció** semmilyen artefaktumban |

---

## 32. Invariánsok — amiket soha nem szabad megsérteni

Gyors összefoglaló. Ezek megsértése **hiba, nem kompromisszum.**

| # | Invariáns |
|---|-----------|
| I1 | Pénzhez soha nem használunk lebegőpontos számot |
| I2 | Minden ár és összeg egész forint; nagy pontosságú tizedes csak egységköltségre |
| I3 | Az áfa-visszaszámolás áfakulcs-csoportonként, bizonylatszinten történik, soha nem soronként |
| I4 | A termék két áfamezője **másolat, nem hivatkozás** |
| I5 | Termék nem menthető hiányos áfával vagy hiányzó NTAK-kategóriával |
| I6 | Öt áfakategória létezik: 5 / 18 / 27 / TAM(0) / AJT |
| I7 | A szervizdíj önálló sor, áfakulcsonként bontva, soha nem a termékbe olvasztva |
| I8 | A vegyes áfakulcsú menü mindig szétrobban komponensekre |
| I9 | A menükomponensek egységára egész forint, és pontosan kiadja a menü árát |
| I10 | Az ár nélküli módosító szövegsor, soha nem tétel |
| I11 | A levonó módosítót soha nem küldjük negatív árú eladási sorként |
| I12 | Minden módosító, ami a soron van, nyomtatódik és kimegy a KDS-re |
| I13 | A SIDURI bizonylatszám eszközönként elhatárolt tartományból jön |
| I14 | Az adóügyi szám soha nem a mi azonosítónk, és nullázható |
| I15 | A munkanap hossza abszolút (UTC) alapon számolódik, a monoton és a faliórás érték közül a konzervatívabbal |
| I16 | Nyitott munkanap közben az órát soha nem állítjuk |
| I17 | A sorrendezés soha nem a faliórán múlik |
| I18 | `ADOTT_NAPON_ZARVA` soha nem megy ki a tárgynap biztos lezárulta előtt |
| I19 | A kimenő NTAK-sor tartós, sorrendtartó és átfedésmentes |
| I20 | Minden NTAK-beküldés feldolgozási nyugtáját lekérdezzük és eltároljuk |
| I21 | Az NTAK és az audit napló soha nem kapcsolható ki |
| I22 | Minden ideiglenes integráció-kikapcsolásnak 1 órás, kikényszerített lejárata van |
| I23 | A rendszer soha nem ajánlja fel magától a megkerülést |
| I24 | Az audit napló csak hozzáfűzhető, adatbázisszinten kikényszerítve |
| I25 | Auditrekordot még a Siduri admin fiók sem törölhet |
| I26 | A nyomtatási szándék helyben rögzül, mielőtt az adóügyi eszközt hívnánk |
| I27 | A nyomtatás-átirányítás telephelyen belülre korlátozott, szerveroldalon kikényszerítve |
| I28 | A szoftver soha nem utasítja el az ügyfél választott konfigurációját |
| I29 | Hibát soha nem nyelünk el csendben |
| I30 | Semmilyen artefaktumban nincs AI-attribúció |
| I31 | Számlás módban a fiskális adapter hívása szerkezetileg lehetetlen; utólagos számlaigénynél a nyugtát előbb sztornózni kell |
| I32 | A többcélú utalvány eladása áfa hatályán kívüli; a beváltás fizetési mód, nem termék |
| I33 | Az allergénlista a receptúrából ÉLŐ módon származtatott, nem másolat — ez az egyetlen kivétel az A3/A4 elv alól |
| I34 | A készlet soha nem blokkol eladást; csak a kézi „elfogyott" jelző szürkíti ki a gombot |
| I35 | Az auditrekord a felhasználót UUID-vel hivatkozza, soha nem szöveges névvel; a szerep pillanatkép |
| I36 | A kártyás borravaló soha nem nyomkövetetlen fiókkivét |
| I37 | A számlamegosztás áfakulcsonként arányosít, soha nem a végösszegen |
| I38 | Árva tranzakciót csak Siduri oldhat fel — de az ügyfél látja, hogy van feloldatlan tétel |
| I39 | A replikációs slot WAL-felhalmozódása lemez alapon korlátozott, és a korlát elérése hangos |
| I40 | A szerepet vivő gépen az automatikus Windows-újraindítás tiltott, és ezt ellenőrizzük |
| I41 | A GDPR-törlés a CRM-profilt érinti; a számviteli bizonylatot soha |
| I42 | Az ár a sor létrehozásakor rögzül, és soha nem értékelődik újra; a mennyiségnövelés új sort hoz létre |
| I43 | A kiszállítás az elviteli áfamezőt használja; áfakulcsot soha nem égetünk a kódba |
| I44 | Vakzárásnál a rögzítés után sem mutatjuk vissza az eltérést |
| I45 | Az allergénfunkció opcionális, de részleges lista soha nem látszódhat teljesként |
| I46 | A 18+ jelzés piktogram a tételsoron, soha nem felugró ablak |
| I47 | Kilépett dolgozó soft delete; a napló és a korábbi adat érintetlen marad |
| I48 | Offline vészmentésnél a titkosító kulcs soha nem csak a mentett gépen él, és a mentést vissza kell olvasni |
| I49 | Egy biztonsági funkció, ami csendben nem működik (hiányzó szenzor, ellenőrizetlen mentés), tiltott — hamis biztonságérzetet ad |
