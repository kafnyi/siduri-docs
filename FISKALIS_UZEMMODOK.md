# FISKÁLIS ÜZEMMÓDOK — a három eset, és az e-pénztárgépes integráció

> **Létrejött:** 2026-08-22, a felhasználó döntése alapján (a fiskális kérdéskör
> három esetre bontása), kiegészítve a kért utánajárással.
>
> **A döntések igazságforrása:** `NYITOTT_KERDESEK.md`. Ez a fájl a fiskális
> terület **részletes kifejtése** — ami itt döntés, az oda is be van vezetve.
>
> **`[?]` jelölés = igazolatlan, forrás nélküli állítás** (§13.5).
> Ebben a fájlban ez különösen fontos: a fiskális terület tele van olyan
> állítással, amit csak a gyártói dokumentációból vagy a NAV-tól lehet lezárni.

---

## 1. A HÁROM ÜZEMMÓD

**A felhasználó döntése (2026-08-22):** a rendszernek **három, egymástól élesen
elkülönülő fiskális üzemmódot** kell támogatnia. Ez nem konfigurációs
kapcsoló-halmaz, hanem **három különböző működési mód**, más kötelezettségekkel.

| | **1. mód — BELSŐ RENDSZER** | **2. mód — ONLINE PÉNZTÁRGÉP** | **3. mód — E-PÉNZTÁRGÉP** |
|---|---|---|---|
| Kapcsolat adóügyi eszközzel | **nincs** | soros / TCP, gyártói protokoll | gyártói protokoll (lásd 4.) |
| Ki állítja ki a jogi bizonylatot | **nem a Siduri** — külön pénztárgépen, kézzel átütve | az online pénztárgép | az e-pénztárgép |
| Nyugtanyomtatás | — | **kötelező, papír** | **alapból NEM**, csak vevői kérésre |
| Vevő azonosítása | — | — | **vevőkód / QR** |
| Offline korlát | nincs fiskális | `[?]` ellenőrizendő | **72 óra** (jogszabályi) |
| Státusz a tervben | **ÚJ, eddig nem szerepelt** | nagyrészt lefedve | **a legnagyobb munka** |

---

## 2. `[!]` 1. MÓD — a Siduri mint BELSŐ rendszer (adóügyi eszköz nélkül)

**A felhasználó leírása:** *„a Sidurit csak belső rendszernek használják, nincs
összekötve pénztárgéppel, vagy NAV-val, van egy különálló online pénztárgépük és
abba átütik manuálisan."*

Ez a **legegyszerűbb** eset technikailag — és **a legveszélyesebb jogilag**, ha
nem vigyázunk.

### `[!]` A csapda: a Siduri olyat nyomtathatna, ami NYUGTÁNAK LÁTSZIK

Ebben a módban a Siduri **nem állít ki jogi bizonylatot** — nincs rá joga és nincs
rá eszköze. Amit nyomtat, az **belső bizonylat**: rendelés-összesítő, előnyugta,
konyhai blokk.

**Ha ez a papír úgy néz ki, mint egy nyugta — összegekkel, ÁFA-bontással, dátummal —
akkor a vendég nyugtának fogja hinni**, és a személyzet is odaadhatja nyugta
helyett. Ez **nem UX-hiba, hanem adóügyi kockázat**, ami az ügyfelet érinti.

**KÖTELEZŐ SZABÁLY:**
- ebben a módban minden nyomtatott papíron **feltűnő, letiltha­tatlan jelölés**:
  **„NEM ADÓÜGYI BIZONYLAT"**;
- a felület sehol ne nevezze **nyugtának** azt, amit ebben a módban kiállít;
- **a sztornó fogalma is más:** itt nincs fiskális sztornó, csak belső javítás —
  a felületnek ezt is máshogy kell neveznie, különben a személyzet azt hiszi,
  hogy elintézte az adóügyi oldalt is.

### `[ ]` Nyitott kérdések ehhez a módhoz

1. **`[ ]` NTAK ebben a módban?** Ha a hely NTAK-köteles, az adatszolgáltatásnak
   akkor is meg kell történnie. **Ki küldi — a Siduri vagy a különálló
   pénztárgép?** Ha mindkettő, **kétszer küldjük ugyanazt.** Ha egyik sem,
   elmarad. **Ezt tisztázni kell**, és ez az egyik legvalószínűbb néma hiba.
2. **`[ ]` A kézi átütés miatt a Siduri forgalma és a pénztárgép forgalma
   szétcsúszhat** (elgépelés, kihagyás). Kell-e összevető riport
   („a Siduri szerint X, a pénztárgép napi zárása szerint Y")? **Javaslom, hogy
   igen** — olcsó, és ez az egyetlen kontroll ebben a módban.
3. **`[ ]` A készlet ettől függetlenül fogy** a Siduriban. Ez rendben van, de
   az **árrés-riport a Siduri árain alapul**, nem azon, amit a pénztárgépbe
   ütöttek. **Az eltérés lehetőségét ki kell mondani a riporton.**

---

## 3. 2. MÓD — online pénztárgép (a jelenlegi terv fő ága)

Ezt a terv nagyrészt lefedi. Amit **ehhez a körhöz** hozzáteszek:

- **`[!]` Dátumozott lejárata van: 2028. július 1.** Lásd
  `ELLENORZES_1_TELJESSEG_JOGI.md` L1. Utána csak e-pénztárgép.
- **`[ ]` Van-e offline plafon a MAI eszközökön?** A 72 órás korlát a
  8/2025. NGM rendeletben az **e-pénztárgépre** vonatkozik. A mai eszközökre
  **nem ellenőriztem**, és **ha van, az azonnal érinti az MVP-t.**
  → a gyártói protokolldokumentációból derül ki (`E3`).

---

## 4. `[!]` 3. MÓD — e-pénztárgép: AMIT AZ UTÁNAJÁRÁS KIDERÍTETT

> A felhasználó kérte: *„nézz utána, hogy hogyan lehet megoldani az integrációt
> pontosan, mik a feltételei."* Ez a szakasz az eredmény.
> **Minden állítás mellett ott a forrás vagy a `[?]` jelölés.**

### 4.1 Engedélytípusok — a Gemini-prompt állítása HELYES

A **hardveralapú** e-pénztárgép forgalmazási engedélyszáma **`B` + három
számjegy** (pl. `B123`); a **felhőalapú** engedélyszáma **`C` + három számjegy**
(pl. `C014`).

**Forrás:** [8/2025. (III. 31.) NGM rendelet](https://net.jogtar.hu/jogszabaly?docid=a2500008.ngm),
[Hardveralapú e-pénztárgépek — HePG](https://hepg.hu/),
[Felhőalapú e-pénztárgép — FePG](https://fepg.hu/).

### 4.2 `[!]` A LEGFONTOSABB: az architektúra alakja NEM változik

A hardveralapú e-pénztárgép **külső számítógépet vagy POS-rendszert igényel** a
működéséhez — **nem önálló kassza, hanem lényegében adóügyi
nyomtató/egység, amit külső szoftver vezérel.** Az első engedélyezett
hardveralapú eszköz a **Fiscat Super eFP**, ami pontosan így működik.

**Forrás:** [HePG — hardveralapú e-pénztárgépek](https://hepg.hu/).

**Ez nagyon jó hír a tervnek:** az integráció **ugyanaz a forma**, mint ma
(a Siduri vezérli az adóügyi eszközt) — **nem kell új architektúrát tervezni**,
csak új protokoll-implementációt egy meglévő absztrakció mögé.

### 4.3 `[!]` HELYESBÍTÉS a Gemini-prompthoz: a NAV sémái NEM a mi interfészünk

A Gemini-prompt azt írja, hogy az e-pénztárgéphez *„a hivatalos NAV fejlesztői
protokollok (GitHubon elérhető XSD sémák)"* használatával integrálunk.
**Ez félreértés.**

A NAV nyilvános fejlesztői anyaga (`nav-gov-hu/eRECEIPT` repó) **két
kapcsolatot ír le:**
1. **e-pénztárgép ↔ NAV** (az eszköz küldi az e-nyugtát a Nyugtatárba),
2. **vevői alkalmazás ↔ NAV** (a vevő lekéri a nyugtáját).

**Amit NEM ír le: a külső szoftver ↔ e-pénztárgép kapcsolatot.**
**Forrás:** [NAV — GitHubon az e-pénztárgépek fejlesztői dokumentációja](https://nav.gov.hu/ado/egyeb/GitHubon_az_e-penztargepek_fejlesztoi_dokumentacioja),
[nav-gov-hu/eRECEIPT](https://github.com/nav-gov-hu/eRECEIPT).

**Következmény, ami a fázistervet érinti:**
> **A mi interfészünk az eszközzel továbbra is GYÁRTÓFÜGGŐ**, ugyanúgy, mint ma
> az AEE-s eszközöknél. **Tehát az `E3` beszerzési tétel (gyártói
> protokolldokumentáció, NDA) NEM szűnik meg 2028-cal — átkerül az
> e-pénztárgép-gyártókra.**

**Amiért a NAV sémáit ettől függetlenül ismerni kell:** azok írják le, **mi kerül
bele az e-nyugtába** (mezők, ÁFA-besorolás, kötelező tartalom). A mi
adatmodellünknek **elő kell tudnia állítani mindent, amit az eszköz kérni fog** —
tehát a séma **a mi adatmodellünk követelménylistája**, még ha nem is a mi
drótformátumunk.

### 4.4 `[?]` NYITOTT ÉS FONTOS: kell-e a MI szoftverünknek engedély?

**Ezt NEM tudtam eldönteni**, és **nem is fogom megtippelni.**

- A **hardveralapú eszköz** engedélyköteles (B-engedély), és azt a **gyártó**
  szerzi meg.
- **Hogy a hozzá kapcsolódó külső POS-szoftvernek kell-e bármilyen tanúsítás,
  bejelentés vagy „igazolt kompatibilitás", az a nyilvános anyagokból nem derül ki.**

**Miért ez a legnagyobb nyitott kockázat ebben a modulban:** ha kiderül, hogy
igen, az **hetekben-hónapokban mérhető** átfutás és **pénz** — és a fázistervbe
be kell árazni. Ha nem, akkor csak a gyártói kompatibilitás-igazolás kell.

**`[ ]` Teendő: közvetlen kérdés a NAV-hoz ÉS egy engedélyezett gyártóhoz
(pl. a Fiscat forgalmazójához).** Ez az `E3` beszerzési tétel része, és
**korán indítandó.**

### 4.5 `[!]` Felelősségi határok — kereskedelmi kockázat, nem mérnöki

A HePG-anyag külön kiemeli: *„a több különálló elemből felépülő rendszerben a
felelősségi határok is könnyen elmosódhatnak"* — hiba esetén a hardver
forgalmazója a szoftverfejlesztőre mutat, a szoftverfejlesztő a hardverre.

**Ez ránk fog mutatni.** A vendéglős szemében a „Siduri nem ad nyugtát" —
függetlenül attól, hogy az eszköz hibázott. **Két következmény:**
1. **Diagnosztika kell**, ami bizonyítja, melyik oldal hibázott (`F5`):
   mit küldtünk, mit válaszolt az eszköz, mikor. **Enélkül nem lehet vitát nyerni.**
2. **A szerződésben és az értékesítésnél tisztázni kell a határt** — ez nem
   mérnöki döntés (§12).

### 4.6 Papír nyugta: NEM kötelező — igazolva

A NAV kérdés-válasz oldala szerint papírt **csak akkor kötelező nyomtatni, ha a
vevő kifejezetten kér papíralapú másolatot.**

**Forrás:** [NAV — E-pénztárgép-üzemeltetés, kérdések és válaszok](https://nav.gov.hu/ado/enyugta/kerdesek-es-valaszok/e-penztargep-uzemeltetes).

**A felhasználó döntése ezzel összhangban:** *„a nyugtanyomtatás az ügyfélnek
első körben opcionális… az alap legyen az, hogy ha egy bármilyen alkalmas hőfejes
nyomtató be van állítva, mint blokknyomtató, akkor azon jöjjön a gépből a nyugta."*

**`[!]` Egy pontosítás, ami fontos lehet:** ha a papírt **a mi hőnyomtatónk**
állítja elő (nem az adóügyi eszköz), akkor tisztázandó, hogy **az a papír
jogilag minek minősül** — „papíralapú másolat"-e a NAV szerinti értelemben, vagy
csak tájékoztató. **`[?]` Ezt nem ellenőriztem, és a különbség lényeges:**
ha csak tájékoztató, akkor ugyanaz a jelölési kötelezettség, mint az 1. módban.
**→ a NAV-hoz intézett kérdés része legyen.**

### 4.7 A vevőkód / QR — a felhasználó döntése és amit hozzáteszek

**Döntés:** a vásárló egy **QR felmutatásával** kérheti magához rendelni a
nyugtát a NAV rendszerében; ezt **géphez kötött QR-olvasóval** oldjuk meg
hardveresen, **de a szoftveres oldalt is le kell fedni.**

**Amit ehhez hozzáteszek:**

1. **`[!]` A fordított irány is kell.** A vevőnek nem mindig van alkalmazása
   felmutatható kóddal. **A mi másodkijelzőnkön (spec 20.) meg kell tudni
   jeleníteni egy QR-t**, amit a vendég beolvas. A másodkijelző **már tervben
   van** — ez majdnem ingyen van, ha most számolunk vele.
2. **`[ ]` A vevőkód SZEMÉLYES ADAT-e?** Egy azonosító, ami egy konkrét
   vásárlót köt egy vásárláshoz. **Ha eltároljuk, adatvédelmi tétel lesz**
   (`B7`, `B10/a`). **Javaslat: NE tároljuk** — továbbítsuk az eszköznek és
   felejtsük el. Ha mégis kell (pl. hibakereséshez), akkor rövid megőrzéssel
   és indoklással.
3. **`[ ]` Mi történik, ha a beolvasás nem sikerül** (karcos telefonkijelző,
   rossz fény)? Kell **kézi bevitel** és **kihagyás** út is — és a kihagyás
   **ne blokkolja a fizetést.** §5: a felület ne álljon meg olyanon, ami nem
   kötelező.
4. **`[ ]` A QR-olvasó ugyanaz az eszköz, mint a vonalkódolvasó?** Ha igen, a
   szoftvernek **meg kell tudnia különböztetni**, hogy egy termék vonalkódját
   vagy egy vevőkódot olvasott-e be — különben a vevőkód „ismeretlen termék"
   hibát fog adni a kosárban. **Ez egy konkrét, könnyen kihagyható hiba.**

### 4.8 `[!]` A 72 óra és a KÉTFÉLE „offline"

**A felhasználó döntése:** *„48 óra offline lét után erősen jelezni kell, hogy nem
csak a rendszer szempontja, de az ügyfél jogi kötelezettsége, hogy 24 órán belül
hozza online állapotba a gépet."*

**Elfogadva.** Két kiegészítéssel:

**(1) `[!]` A 3. módban KÉTFÉLE „offline" van, és a kettő NEM ugyanaz:**

| Mi hiányzik | Kit érint | Következmény |
|---|---|---|
| **A helyi hálózat / a Siduri szerver** | a Siduri | csökkentett mód — **az adóügyi eszköz ettől még dolgozhat** |
| **Az INTERNET** | **az adóügyi eszköz** | **72 óra után az eszköz megáll** — a Siduri ettől függetlenül tökéletesen működhet |

**A két állapotot külön kell mérni és külön kell kijelezni.** Ez összecseng
azzal a korábbi döntéssel, hogy az internet-jelzés önálló sorban van, és nem
keveredik a szerver-diagnózissal. **Itt viszont már nem kényelmi kérdés:
a rossz jelzés miatt a személyzet a rossz dolgot fogja javítani, miközben
ketyeg a 72 óra.**

**(2) `[!]` A visszaszámlálót AZ ESZKÖZTŐL kérdezzük, ne mi számoljuk.**
A 72 órát **az eszköz tartja nyilván**, és **az eszköz fog megállni.** Ha mi
a saját óránkból számolunk, a két számláló elcsúszhat (óraállítás, eszközcsere,
szerviz), és **pont akkor mutatunk 40 órát, amikor az eszköz már a 71-nél tart.**
§5: pozitív bizonyíték kell, nem a saját becslésünk.

### 4.9 `[!]` Amit a 3. mód a TERV EGÉSZÉBEN megváltoztat

1. **A „nyugta" fogalma kettéválik:** van **e-nyugta** (az eszköz állítja ki,
   a Nyugtatárba megy, alapból papír nélkül) és van **papíralapú másolat**
   (opcionális). A bizonylat-modellnek **mindkettőt** kezelnie kell, és a
   „kinyomtattuk-e" **nem azonos** azzal, hogy „kiállítottuk-e".
2. **A fiskális azonosító formátuma MÁS:** `NY–AP/ASZ/AN/NS` az e-pénztárgépnél,
   szemben a mai `Axxxxxxxxx/yyyy/zzzzz`-vel.
   → **`[!]` A fiskális azonosító mezőt SOHA ne kössük egyetlen formátumhoz** —
   se validációval, se szétbontással. **Tároljuk szövegként, ahogy az eszköz
   visszaadta**, és a szétbontás legyen külön, formátum-tudatos réteg.
3. **A sztornó menete is más lesz** — az eredeti **e-nyugta azonosítójára**
   hivatkozó fordító művelet. `[?]` A pontos menetet a gyártói protokoll adja
   (`C10`).

---

## 5. A MODUL SZERKEZETE — amit a három mód megkövetel

**Egy nevesített absztrakció mögé kerül mind a három** (§3.5: ha egy képességnek
több belépési pontja van, közös helper döntsön):

| Implementáció | Mit csinál |
|---|---|
| **Belső mód** | nem hív adóügyi eszközt; a bizonylat „nem adóügyi" jelöléssel készül |
| **Online pénztárgép** | gyártói protokoll, papír kötelező |
| **E-pénztárgép** | gyártói protokoll, e-nyugta, vevőkód, papír opcionális |

**`[!]` Amit a pénztáros lát, mind a három módban UGYANAZ kell legyen** — a
különbség a háttérben van. **Kivéve ott, ahol a különbségnek látszania KELL**
(nem adóügyi jelölés az 1. módban; vevőkód-kérés a 3. módban). Ez a kettő nem
mond ellent egymásnak: az **alapfolyamat** azonos, a **jogilag jelentős
eltérések** viszont láthatók.

### `[!]` És ebből következik egy őr-követelmény (§13.4)

A módváltás **adóügyi következményű**. Kell rá **szkenner/őr**, ami méri, hogy
- egyik módban sem hívódik meg a másik mód kódútja,
- a „nem adóügyi" jelölés **nem hagyható el** az 1. módban,
- **a demó/teszt mód (`F6`) és az éles mód nem keveredhet** egyik fiskális
  módban sem.

---

## 6. `[ ]` AMIT MEG KELL KÉRDEZNI — a NAV-tól és egy gyártótól

Ezek **nem eldönthetők nyilvános anyagból**, és **korán indítandók**, mert
átfutási idejük van:

| # | Kérdés | Kinek | Mi múlik rajta |
|---|--------|-------|----------------|
| 1 | **Kell-e a külső POS-szoftvernek engedély/tanúsítás/bejelentés** az e-pénztárgéphez? | NAV **és** gyártó | Hetek-hónapok és pénz a fázistervben |
| 2 | A POS ↔ e-pénztárgép **protokoll dokumentációja** | gyártó (NDA?) | A teljes 3. mód nem tervezhető nélküle |
| 3 | Van-e **offline plafon a MAI online pénztárgépeken** is? | gyártó | Ha igen, **AZONNAL érinti az MVP-t** |
| 4 | A **saját hőnyugtánk** minek minősül a 3. módban — „papíralapú másolat" vagy tájékoztató? | NAV | Jelölési kötelezettség |
| 5 | Sztornó/visszáru pontos menete mindkét eszközgenerációnál | gyártó | `C10` teljes egészében |
| 6 | Az **1. módban** ki teljesíti az NTAK-adatszolgáltatást? | NAV / NTAK | Néma elmaradás vagy dupla küldés |
