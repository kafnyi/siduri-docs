# Hardver-minimum — döntéselőkészítés

**Utolsó frissítés:** 2026-08-23
**Kérdés:** legyen-e a minimum 3. generációs i3 / 8 GB / 128 GB SSD a J1900 helyett?
**Állapot:** `[JAVASLAT — EGY KÉRDÉS MEGVÁLASZOLÁSÁRA VÁR]`

---

## 1. Rövid válasz

> **Igen, emeljük a minimumot. De két számot kell megadni, nem egyet — és a
> 3. generációs i3 valószínűleg rossz cél egy 2026-ban induló rendszerhez.**

---

## 2. Mit KÖLTÖTT ránk eddig a J1900

A J1900 nem egy paraméter volt a listán, hanem **a terv több pontját alakította.**
Érdemes látni, mennyi minden lóg rajta:

| Döntés | Miért így | Hol |
|--------|-----------|-----|
| **GraalVM natív image KÖTELEZŐ** | memóriakorlát | §4.1 |
| **Szoros WPF teljesítmény-költségvetés** | Bay Trail iGPU | §4.2 |
| **Semmi üveghatás, árnyék, textúra** | ugyanaz | UIUX K1 |
| **Termékkép most nem épül meg** | 20 kép egy rácson kétséges | UIUX 10.2 |
| **A webes admin csak statikus lehet** | a szerveroldali renderelés kizárva | WEBADMIN §2 |
| **Helyben 30 nap megőrzés, purge felhőbe** | 64 GB SSD | §24.2 |
| **WAL-felhalmozódás kritikus kockázat** | 64 GB SSD | §7.1, M19 |
| **Az M12 (tartalék POS átvesz csúcson) a legkockázatosabb mérés** | CPU + RAM | MERESEK |
| **9 mérés a 19-ből a J1900 miatt van** | | MERESEK |

> **Vagyis a kérdés nem az, hogy „gyorsabb legyen-e a gép", hanem hogy
> a terv fél tucat kompromisszumát meg akarjuk-e tartani.**

---

## 3. Mit hozna a váltás — nagyságrendek

*Közelítő értékek, nem mérés:*

| | **J1900** | **i3-3220** | **N100** *(2023-as)* |
|---|---|---|---|
| Év | 2013–14 | **2012–13** | **2023** |
| Magok | 4 (HT nélkül) | 2 mag / 4 szál | 4 |
| **Egyszálas teljesítmény** | ~700 | **~1700 (≈2,4×)** | **~1900 (≈2,7×)** |
| Többszálas | ~1900 | ~3400 | **~5600** |
| TDP | 10 W | **55 W** | **6 W** |
| RAM tipikusan | 4 GB *(max 8)* | 8 GB+ | 8–16 GB |
| Állapot | használt | **használt** | **új, garanciával** |

### ⚠️ 3.1 Az egyszálas teljesítmény a döntő, nem a magszám

**Ez a fontos rész.** A mi szűk keresztmetszeteink szinte mind egyszálasak:

| Terhelés | Miért egyszálas |
|----------|-----------------|
| **PostgreSQL lekérdezés** | egy lekérdezés jellemzően egy magon fut |
| **A WPF felületi szál** | egyetlen szál, és ha akad, a pénztáros látja |
| **Kérésfeldolgozás** | kérésenként egy szál |

**Tehát a ~2,4–2,7× egyszálas előny nagyjából ennyivel gyorsítja azt, ami
ténylegesen fáj.** A magszám-előny ehhez képest másodlagos.

### 3.2 A RAM valószínűleg fontosabb, mint a CPU

**4 GB-on ez fut egyszerre:** Windows 10 IoT LTSC (~1,5–2 GB) · PostgreSQL ·
a szerver · a POS kliens · **és néha egy böngésző, ha ott nyitják meg az admint**
*(WEBADMIN §4)*.

**Ez 4 GB-on szoros. 8 GB-on kényelmes.** A 4→8 GB önmagában többet ér, mint a
CPU-csere.

### 3.3 A 128 GB SSD közvetlenül old egy kockázatot

**A WAL-felhalmozódás** *(§7.1, M19)* **azért volt kritikus, mert 64 GB-on egy
leszakadt tartalék szerver napok alatt betölti a lemezt.** Kétszer annyi hely
**kétszer annyi időt ad** a felismerésre és a beavatkozásra. Nem szünteti meg a
kockázatot, de nagyságrendet változtat rajta.

---

## 4. ⚠️ De miért pont 2012-es hardver legyen egy 2026-os minimum?

**Ezt ki kell mondanom, mert a kérdésben benne van egy rejtett feltevés.**

Ha **szabadon választhatunk** minimumot, akkor **a 3. generációs i3 furcsa hely
megállni:**

| # | Probléma |
|---|----------|
| a | **2012–13-as hardver.** Ma 12–13 éves. Egy most induló telepítésnél **elhasználódott alkatrészeket** veszünk — ventilátor, kondenzátor, SSD-kopás |
| b | **55 W TDP** a J1900 10 W-jához képest. **Ventilátoros, meleg, poros konyhai környezetben** — ez üzemeltetési kockázat, nem apróság |
| c | **Nincs garancia**, nincs beszerzési utánpótlás. Ha három év múlva kell egy csere, mit veszünk? |
| d | **Egy mai N100-as mini PC ÚJONNAN olcsóbb vagy hasonló árú**, **gyorsabb**, **6 W**, **ventilátor nélküli**, **garanciás**, és **8–16 GB RAM + NVMe** |

> **Vagyis: ha azért emelünk minimumot, hogy jobb legyen — akkor a használt
> 2012-es i3 helyett egy új, belépő szintű mai gép jobb választás, gyakran
> ugyanannyiért.**

---

## 5. `[JAVASLAT]` Két szám, nem egy

| | **TÁMOGATOTT MINIMUM** | **AJÁNLOTT / ÉRTÉKESÍTETT** |
|---|---|---|
| Mi ez | Amit **elfogadunk**, ha az ügyfélnek már megvan | Amit **új telepítéshez adunk el** |
| CPU | **3. gen. i3 osztály** *(vagy azzal egyenértékű)* | **N100 osztály vagy jobb** |
| RAM | **8 GB** | **8–16 GB** |
| Tároló | **128 GB SSD** | **256 GB NVMe** |
| Szerver-szerep | **csak ha nincs jobb** | **igen** |

**Miért működik ez jobban egy számnál:**

| # | Indok |
|---|-------|
| a | **A meglévő gépes ügyfelet nem zárjuk ki** — ha van elfogadható vasa, elfogadjuk |
| b | **Új telepítésnél nem adunk el 12 éves hardvert** — az a mi hírnevünk |
| c | **Illeszkedik a már meglévő mintánkba:** a méretosztályok is **ajánlások, nem korlátok** *(§5.1)*, és a kockázatvállalási nyilatkozat kezeli, ha az ügyfél mást akar |
| d | **A szerver-szerepre szigorúbb lehet a szabály, mint a kliensre.** Egy gyenge gép **kliensként** elmegy; **szerverként** az egész telephelyet lassítja |

---

## 6. Az üzleti oldal

### 6.1 A támogatási költség aszimmetriája — ez a fő érv

> **Egy gyenge vason futó ügyfél aránytalanul sok támogatást fogyaszt, és
> hardveres okból lassú rendszert SZOFTVERHIBAKÉNT jelent be.**

**És ezt nem lehet szoftverrel megjavítani.** Minden ilyen ügyfél:

* több támogatási jegyet generál *(→ Hermes-terhelés, §0.3.1)*,
* rosszabb szájhagyományt csinál,
* és **pont annál a szegmensnél**, ahol a legkevesebb bevétel van.

### 6.2 ⚠️ Az ingyenes belépő szint pont a legrosszabb vasat vonzza

**Ezt előre látni kell.** Az egygépes, ingyenes szint *(§2.1)* **azt az ügyfelet
vonzza, akinél a legrégebbi gép van** — és nála fut a szerver, a kliens és az
adatbázis **ugyanazon a gépen**, ami a legszűkösebb eset *(M1)*.

**Következmény:** az ingyenes szintre **minimum-ellenőrzés kell**, és ha a gép
nem éri el, **mondjuk meg előre, ne a rossz élmény után.**

### 6.3 Pozicionálás

Egy magasabb minimum **nem csak korlát, hanem üzenet is:** *„ez egy komoly
rendszer, nem egy böngészős kasszaalkalmazás"*. A vendéglátós piacon ez inkább
segít, mint árt — **feltéve, hogy a hardvert mi tudjuk szállítani**, tehát nem
az ügyfélnek kell megoldania.

---

## 7. `[FONTOS]` A visszafordíthatóság aszimmetrikus

| Irány | Költség |
|-------|---------|
| **Magasabb minimumot később EMELNI** | **olcsó** — egyszerűen nem adunk el régi vasra |
| **Alacsonyabb minimumra később VISSZALÉPNI** | ⚠️ **majdnem lehetetlen**, ha közben 8 GB-ra építettünk |

**Ebből fakad a fontos árnyalat:**

> **A teljesítmény-fegyelmet akkor is meg kell tartani, ha emelünk.**

A J1900 kényszere **jó döntéseket szült**: virtualizált listák, egész forint,
indexfegyelem, elrendezés-animáció tilalma, kevés függőség. **Ezek attól még
helyesek, hogy van hely.** Amelyik rendszer kap fejteret, **az elfogyasztja.**

**Ezért a javaslat: a szabályok maradnak, csak nem egy konkrét géptípushoz
kötve.** A „lean by design" tervezési elv, nem hardverbaleset.

---

## 8. Mi VÁLTOZNA a tervben, ha emelünk

| # | Tétel | Változás |
|---|-------|----------|
| a | **GraalVM natív image** | ⚠️ **KÖTELEZŐBŐL DÖNTÉSSÉ válna.** 8 GB-on a sima JVM is elfér. **Ez a legnagyobb fejlesztési könnyítés**: elmarad a reflexiós konfiguráció, a hosszú fordítás *(M10)* és a könyvtár-összeférhetetlenség. **De: a gyors indulás továbbra is érték** *(a szerver újraindul egy Windows-frissítés után szerviz közben)* → **M1 és M10 mérése után döntsük el, ne most** |
| b | **Termékkép** | Reálisabbá válik, de **továbbra is mérés után** *(M3)* |
| c | **Másodkijelzős videó** | Kockázata jelentősen csökken |
| d | **WAL / lemez** | Nagyságrenddel több mozgástér, **de a korlátozás szabálya marad** |
| e | **M12 (tartalék POS átvesz)** | **Sokkal valószínűbb, hogy sikerül** — de **a mérés marad**, mert a HA-terv ezen áll |
| f | **Webes admin** | A statikus-kiszolgálás döntése **NEM változik** — az továbbra is a helyes megoldás, csak nem élet-halál kérdés |
| g | **UI/UX korlátok** | ⚠️ **NEM változnak.** A 64 px-es célfelület nem a CPU miatt van, hanem az ujj miatt |

---

## 9. `[MEGVÁLASZOLVA]` A tényleges felállás — és egy helyesbítés

**Az ügyfél tényleges vasparkja:**

| Szerep | Gép |
|--------|-----|
| **Jelenlegi kliensek** | **i3** *(a jelenlegi rendszer ezen fut)* |
| **Valószínű lokális szerver** | ⭐ **5. generációs i5, 8 GB RAM, 128 GB SSD** |
| **Tartalék gépek** | **3 db J1900** — egy megszűnt üzletből, **szeretné felhasználni** |

### ⚠️ 9.1 HELYESBÍTÉS: nem mondtam, hogy a J1900-asok nem használhatók

**A megfogalmazásom félreérthető volt, és rossz következtetést okozott.**
Amit írtam, az az volt, hogy **a J1900 a TERVEZÉSI CÉLKÉNT** költséges — nem az,
hogy a gépek használhatatlanok.

> **A három J1900 KLIENSKÉNT használható. Szervernek nem kell — mert van jobb.**

| Szerep | J1900 alkalmas? |
|--------|-----------------|
| **POS kliens** | ✅ **Igen** — a felület amúgy is a szűkös géphez tervezett *(UIUX K1)*. `[MÉRENDŐ]` M3 |
| **Fő szerver** | ❌ Felesleges — **van i5** |
| **Tartalék szerver** | ⚠️ **Lehet, de átgondolandó** — lásd 9.3 |
| **Termékkép megjelenítése** | ⚠️ Mérés után *(M3)* |

**Egy őszinte üzemeltetési megjegyzés:** három, megszűnt üzletből maradt gép
**öreg, és el fog romlani.** Nem érv ellenük — **de a pótalkatrész kérdését most
kell feltenni, nem az első meghibásodáskor.** Ha nincs tartalék gép, egy elromlott
kassza **azonnali kiesés.**

### 9.2 Amit ez a TERVBEN megváltoztat

> **A szerver-oldali J1900-kényszer MEGSZŰNT. Ez a projekt egyik legnagyobb
> könnyítése eddig.**

| # | Tétel | Változás |
|---|-------|----------|
| a | **GraalVM natív image** | **Kötelezőből DÖNTÉSSÉ vált.** 5. gen. i5 + 8 GB mellett a sima JVM kényelmesen elfér. **A gyors indulás továbbra is érv mellette** — döntsük el **M1 és M10 után** |
| b | **PostgreSQL memórialimitek** | **Jelentősen lazulnak** |
| c | **A webes admin statikus kiszolgálása** | **A DÖNTÉS NEM VÁLTOZIK** — továbbra is ez a helyes. De **már nem élet-halál kérdés**, hanem jó mérnöki gyakorlat |
| d | **64 GB SSD korlát** | **128 GB** — a WAL-kockázat *(M19)* nagyságrenddel kap levegőt |
| e | **M14** *(a szerver webes admint is kiszolgál)* | Kockázata **jelentősen csökken** |
| f | **A kliens-oldali korlátok** | ⚠️ **MEGMARADNAK, ha J1900-as kliens is lesz.** Nincs üveghatás, nincs elrendezés-animáció, virtualizált listák — **ezek maradnak** |

### 9.3 `[ÚJ KÉRDÉS]` Mi legyen a tartalék szerver?

**Ez most jött elő, és nem triviális.** A szabályunk szerint **a tartalék szerver
mindig egy Windows POS vastagkliens** *(§5.2)*. De:

| Ha a tartalék… | Következmény |
|----------------|--------------|
| **i3 kliens** | ✅ Elfogadható — átvételkor mérsékelt visszaesés |
| **J1900 kliens** | ⚠️ **Az átvétel LEFOKOZÁS.** i5-ről J1900-ra váltva a telephely **érezhetően lassabb** lesz — pont csúcsban, mert a failover jellemzően akkor kell |
| **Egy második i5** | ✅ A legjobb, ha van |

> **Új szabály következik ebből:** **a tartalék szerver ne legyen érdemben
> gyengébb a főnél.** Ha mégis az, azt **az ügyfélnek tudnia kell előre** — mert
> a failover után nem hibát fog látni, hanem lassulást, és **azt a szoftverre
> fogja.**

**A kockázatvállalási nyilatkozat** *(§24.4)* **természetes helye ennek.**

### 9.4 `[MÓDOSUL]` Az M1 mérés szerepe

Az M1 *(kombinált szerver + pénztárgép EGY J1900-on)* eddig **„a legszűkösebb
eset, és ez az ALAPÉRTELMEZÉS"** volt.

**Ez az első ügyfélre már nem áll** — ott i5 a szerver.

**De az M1 NEM törlendő**, csak átminősül:

> **Az M1 mostantól nem az alapértelmezés, hanem az INGYENES EGYGÉPES SZINT
> padlója** *(§2.1)* — és pont az a szint vonzza a legrosszabb vasat *(6.2)*.

### 9.5 `[ÜTEMEZÉSI NYERESÉG]` A K3 kapu szűkül

A `K3/a` kapu eddig **„2 db J1900 + 1 adóügyi eszköz beszerzése"** volt.

**Most pontosabban tudjuk, mit kell venni:**

| # | Mire |
|---|------|
| a | **Egy i5-osztályú gép** — a szerver-oldal fejlesztéséhez és méréséhez |
| b | **Egy J1900** — **a leggyengébb kliens** ellenőrzésére, mert az ügyfélnél is lesz ilyen |
| c | **Egy Fiscat eszköz** — `iPalm` vagy `Neon+`, **amilyen az ügyfélnél van** |

⚠️ **Az ügyfél gépein fejleszteni és mérni NEM lehet** — az egy élő étterem.
**Saját teszthardver továbbra is kell**, csak most már tudjuk, pontosan milyen.

### 9.6 `[LEZÁRVA]` A teljes kép

| Kérdés | Válasz |
|--------|--------|
| Az i3 generációja és RAM-ja | **3. generáció, 8 GB** |
| Az 1024×768 melyik gépé | ⚠️ **MINDEGYIKÉ** — az i3-ak kijelzője is ugyanakkora |
| Van-e második i5 | **Nincs** *(az ügyfél meggyőzése folyamatban)* |
| Van-e tartalék a J1900-hoz | ✅ **Van** |
| Milyen gépek ezek | ⚠️ **MIND érintőképernyős POS** — a J1900-ak, az i3-ak **és az i5 is** |

### 9.7 `[DÖNTÉS]` Három szint, nem egy — a TERVEZÉSI CÉL az i3

**Az utasítás: „legyen a rendszer az i3-ra tervezve."** Ezt így bontom ki:

| Szint | Gép | Mit jelent |
|-------|-----|-----------|
| **TERVEZÉSI CÉL** | **3. gen. i3 / 8 GB** | **Erre optimalizálunk, és az elfogadási kritériumokat EZEN mérjük.** Kliensként ÉS szerverként |
| **TÁMOGATOTT ALSÓ HATÁR** | **J1900** | **Működnie kell**, lehet lassabb, és **funkciók kikapcsolva** (termékkép). Nem itt mérünk sikert |
| **FŐ SZERVER (adott)** | **5. gen. i5 / 8 GB / 128 GB** | **Fejtér, nem cél.** Nem tervezünk „lefelé" hozzá |

> **Miért az i3 a cél és nem az i5:** mert **nincs második i5, tehát a TARTALÉK
> SZERVER egy i3 lesz.** Átvétel után a telephelyet **egy i3 hajtja** — ha csak
> az i5-re terveznénk, a failover utáni állapot mérhetetlen lenne.
>
> **A szerverkód alsó határa tehát az i3, nem az i5.**

### 9.8 `[MEGNYUGTATÓ]` A „lefokozás" aggály feloldva

**A 9.3-ban riasztottam, hogy i5-ről J1900-ra átvenni lefokozás.**
**Ez így már nem áll fenn**, mert:

> **A tartalék szerver egy i3 legyen, nem J1900.** i5 → i3 **mérsékelt lépcső,
> nem szakadék** — és az i3 8 GB-tal önmagában is elfogadható szerver.

**Konkrét ajánlás:** **a tartalék szerepet az egyik i3-as POS vigye.** A
J1900-asok maradjanak tiszta kliensek.

### 9.9 `[ŐSZINTE VÁLASZ]` Kell-e a második i5?

**Nem kritikus, és ezt meg is mondom, mert nem a mi dolgunk fölösleges vasat
eladni.**

| | |
|---|---|
| **i5 fő + i3 tartalék** | ✅ **Működőképes felállás.** Az i3 8 GB-tal elbírja a szerverszerepet, és a failover utáni visszaesés mérsékelt |
| **Második i5** | ✅ Jobb — de **kényelem, nem szükséglet** |

**Amiért mégis érdemes lehet — de ez ELTÉRŐ érv:** nem a teljesítmény, hanem az,
hogy **a tartalék gép egyben dolgozó pénztárgép is** *(§5.2)*. Ha az i3 tartalék
csúcsban átvesz, akkor **ugyanaz a gép egyszerre pénztárgép ÉS szerver** — ez
pontosan az **M12** mérés tárgya. **Ha az M12 az i3-on megbukik, akkor a második
i5 nem luxus, hanem követelmény.**

> **Vagyis: a válasz a mérésen múlik, nem az érzésen. Az M12 előtt ne vegyen
> semmit.**

### 9.10 `[ÚJ LELET]` MINDEN gép érintőképernyős POS — a webes adminnak is

⚠️ **Ez egy korábbi állításomat cáfolja.** A UI/UX tervben azt írtam:

> *„A webes admin más világ — ülve, gondolkodva, ott a webes UX-szabályok
> érvényesek."*

**Ez részben téves ebben a telepítésben**, mert **nincs irodai gép.** Minden gép
egy 1024×768-as érintőképernyős POS a pultban.

**Tehát az admint valószínűleg így fogják használni:**

| Hol | Mire | Milyen gyakran |
|-----|------|----------------|
| **A pulti POS érintőképernyőjén** | gyors dolgok: ár, „elfogyott", egy termék felvitele | **naponta** |
| **Saját laptopról / otthonról** | valódi adminisztráció: receptúra, leltár, riportok | ritkábban |

**Ebből következő követelmény:**

> **A webes admin legyen HASZNÁLHATÓ 1024×768-as érintőképernyőn — de
> OPTIMALIZÁLVA asztali gépre.**

| # | Szabály |
|---|---------|
| a | ⚠️ **Semmi olyan művelet, ami CSAK hover-rel érhető el** — a táblázatsorok „lebegő" akciógombjai a leggyakoribb hiba |
| b | **A táblázatsorok érintésbarát magasságúak** (min. 44 px), akkor is, ha egérrel is használják |
| c | **A fő táblázatok elférnek 1024 px szélességben** vízszintes görgetés nélkül — vagy **kártyás nézetre váltanak** szűk módban |
| d | **Nem kell teljes POS-szintű célfelület-méret** (64 px) — az admin nem a sebességről szól. **De a 24 px-es webes minimum kevés érintőn** |
| e | **A hosszú űrlapok (termékfelvitel) érintésre is kitölthetők** — a numerikus mezőknél képernyő-billentyűzet |

*(Ez befolyásolja az adatrács-könyvtár választását is: **érintésbarát legyen**,
ne csak egérre tervezett.)*
