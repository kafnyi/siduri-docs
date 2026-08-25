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

### 9.6 Nyitott — az ügyfélnél megkérdezendő

| # | Kérdés | Miért |
|---|--------|-------|
| **H1** | **Pontosan hányadik generációs az i3, és mennyi RAM van bennük?** | A kliens-költségvetéshez |
| **H2** | ⚠️ **Az 1024×768-as kijelző MELYIK gépé?** Ha csak a régi J1900-asoké, akkor **a jelenlegi i3-as kliensek nagyobb felbontásúak** — és a tervezési alap felülvizsgálandó | UIUX §7 |
| **H3** | **Van-e második i5, vagy melyik gép lesz a tartalék szerver?** | 9.3 |
| **H4** | **Van-e tartalék gép a 3 J1900-hoz?** | 9.1 |
| **H5** | **A J1900-asok érintőképernyős POS gépek, vagy sima számítógépek?** | Ha nem érintős, kliensnek sem jók a pultban |
