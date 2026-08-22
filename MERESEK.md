# MÉRÉSEK — a mérendő tételek egységes nyilvántartása

> **Ez a fájl azért van, mert a MERNOKISAROKKOVEK §4 kimondja: „Teljesítmény-,
> memória- és versenyhelyzet-állítás CSAK méréssel." Nélküle ezek a tételek
> szétszóródnak a tervben, és a fázisterv írásakor egy részük némán kimarad.**
>
> **Utolsó frissítés:** 2026-08-22 (2. munkamenet, 7. kör — M12/M13 felvéve)
> **Belépési pont a projekthez:** `FOLYAMATBAN.md`
> **A döntések igazságforrása:** `NYITOTT_KERDESEK.md`

---

# ⚠ A FELHASZNÁLÓ KIEMELT UTASÍTÁSA (2026-08-22)

> ## AZ ELSŐ TÉNYLEGES ÉLES TESZTNÉL **MINDENT** MEG KELL MÉRNI.
>
> Szó szerint: *„igen, mindenképpen szeretném majd a teljes terhelést minden
> ponton lemérni majd, de ez már akkor lesz időszerű, ha már teljesen kész a
> project és mehet az éles teszt. ezt nagybetűvel írd is fel, hogy az első
> tényleges teszt esetén legyen mérve minden is!"*
>
> **Ez nem opcionális lépés a fázistervben, hanem SZÁLLÍTÁSI KAPU.**
> Az éles teszt nem indulhat el mérési terv nélkül, és nem zárható le
> „úgy tűnt, jól ment" alapon — csak számokkal.
>
> **A mérésnek KÜLÖN FÁZIST kell kapnia az `E1` fázistervben**, saját
> időkerettel. A mérés nem a fejlesztés melléktermeke.

---

## 0. Hogyan használd ezt a fájlt

- Minden tétel állapota: `[ ]` még nincs mérve · `[MÉRVE]` van száma és dátuma ·
  `[ELAVULT]` volt száma, de a rendszer azóta változott.
- **`[MÉRVE]` sorba KÖTELEZŐ beírni:** a számot, a mértékegységet, a gépet, a
  dátumot, és hogy MI VOLT A TERHELÉS. Szám kontextus nélkül nem mérés.
- **Ha egy tétel „rendben"-nek bizonyul, azt is írd be** (§11: a negatív eredményt
  is le kell írni) — különben a következő kör újra végigcsinálja.
- **Semmilyen teljesítmény- vagy adatvesztési vállalás nem tehető a
  felhasználónak vagy az ügyfélnek MÉRÉS ELŐTT.**

---

## 1. A LEGSZŰKÖSEBB ESET — és ez az ALAPÉRTELMEZÉS, nem szélső eset

**Miért ez az első tétel:** a felhasználó 2026-08-22-én kimondta, hogy *„a legtöbb
esetben a szerver egy olyan gép lesz, ami egyébként kliens is, tehát egy tényleges
használatban levő POS"* — nagyon kevés hely vesz külön szervergépet. Vagyis a
kombinált szerep nem kivétel, hanem a tipikus telepítés.

### `[ ]` M1 — Kombinált szerver + pénztárgép EGY J1900-on
Egyszerre fut ugyanazon a gépen:
- PostgreSQL,
- a Java szerver (GraalVM native image),
- a WPF pénztárgép-kliens teljes képernyőn,
- a másodkijelzős 720p videó (spec 20. pont),
- a kliens-oldali tranzakció-archívum írásai.

**Mit mérj:** RAM-csúcs és -átlag, CPU-telítettség, a pénztári művelet
válaszideje (tétel felütése → megjelenik), a videó képkockadobása, lemez
várakozási idő. **4 GB RAM mellett is**, mert a bázis egy része ennyi.

**Miért kritikus:** ha ez nem fér bele, nem egy funkció dől meg, hanem a
telepítési modell.

### `[ ]` M12 — **A LEGKRITIKUSABB MÉRÉS: a tartalék POS átveszi a szolgálatot**

**Miért ez a legfontosabb tétel az egész listán.** A tartalék szerver **mindig egy
dolgozó Windows POS** (2026-08-22-i tisztázás) — nem dedikált gép. Amikor átveszi
a szolgálatot, ugyanaz a J1900 hirtelen ezt viszi **egyszerre**:

- a saját WPF pénztárgép-kliensét, amin közben a pincér/pultos dolgozik,
- a PostgreSQL-t **teljes szerver-terheléssel** (nem csak replikaként),
- az összes többi Windows POS kiszolgálását,
- a vékonyklienseket (a példa szerint 2 tablet + 4 telefon),
- a KDS-t és a rendeléskijelzőt,
- a nyomtató-útvonaltervezést,
- és a többi gép visszatéréskori napló-lejátszását.

**És mindez a lehető legrosszabb pillanatban:** a szerver akkor esik ki, amikor a
hely dolgozik, nem hajnali 3-kor.

**Mit mérj:** a pénztári művelet válaszideje a tartalék gépen ÉS a többi kasszán,
CPU- és RAM-telítettség, lemez várakozási idő, a vékonykliensek válaszideje,
a nyomtatás késleltetése. **Terhelés: a referencia-telepítés** (3 Windows POS +
2 tablet + 4 telefon + KDS + rendeléskijelző) **csúcsforgalommal.**

**Miért nem halasztható:** ha a tartalék nem bírja, akkor a failover **rosszabbá
teszi a helyzetet, nem jobbá** — egy akadozó rendszer minden kasszán, egy gyors,
csökkentett mód helyett. Ez nem finomhangolási kérdés, hanem azt dönti el,
**érdemes-e egyáltalán átkapcsolni.**

### `[ ]` M13 — A tartalék POS terhelése NORMÁL üzemben (csak replikaként)
Az M12 előtti, enyhébb eset: a gép pénztárgép, és közben folyamatosan fogadja a
replikációs folyamot. Ha már ez is elviszi a válaszidőt, az M12 értelmetlen.

### `[ ]` M2 — PostgreSQL memórialimitek
`shared_buffers`, `work_mem`, `max_connections`. **Mérendő paraméterek, nem
tippelendők** — és az M1 kombinált terhelés mellett, nem üres gépen.

### `[ ]` M3 — WPF kliens önmagában, Bay Trail integrált GPU-n
720p másodkijelzős videó + teljes képernyős érintőfelület + animációk.
Külön mérendő az M1-től, hogy tudjuk, mennyi a kliens saját költsége.

---

## 2. Magas rendelkezésre állás és replikáció

### `[ ]` M4 — Szinkron vs. aszinkron replikáció írási válaszideje J1900 PÁRON
**A terv jelenlegi munkafeltevése az aszinkron replikáció, azzal az indoklással,
hogy két J1900 között a szinkron vállalhatatlan. EZ JELENLEG ÉRVELÉS, NEM MÉRÉS.**
Amíg nincs szám, a döntés érvényben marad (a konzervatív irány), de tényként
kezelni tilos.

### `[ ]` M5 — A failovernél elveszthető tranzakciók száma
**Semmilyen adatvesztési vállalás nem tehető az ügyfél felé e nélkül.**
Tipikus pénztári terhelés mellett, valós J1900 páron, aszinkron replikációval.

### `[ ]` M6 — A billegés-védelem küszöbei (X visszaállás / Y idő)
A növekvő várakozás lépcsősora és a leállási határ **tapasztalati értékek**.
Kiindulás: 3 visszaállás / 1 óra. Valós üzemben felülvizsgálandó.

### `[ ]` M7 — Mennyi idő ténylegesen egy szerepcsere?
A kliensek újracsatlakozásától a kiszolgálás helyreálltáig. Ez határozza meg,
mekkora a fennakadás, amiről a felhasználónak beszélünk.

---

## 3. Kliens-oldali tárolás

### `[ ]` M8 — A tranzakció-archívum írásterhelése olcsó tárolón
SSD vagy eMMC, minden tranzakciónál lemezre szinkronizált hozzáfűzés.
**Különösen az M1 kombinált esetben**, ahol ugyanaz a lemez viszi a PostgreSQL-t.
Mit mérj: írási késleltetés, a pénztári művelet válaszidejére gyakorolt hatás,
és a tároló élettartam-terhelése (írt bájt / nap).

### `[ ]` M9 — Az archívum tényleges mérete valós terméktörzzsel
A tervben szereplő ~1,5–2 kB / nyugta és ~10 MB / kassza / 10 nap **BECSLÉS**,
explicit feltevésekből (4–5 tétel/nyugta, 500 nyugta/nap). Valós terméktörzs és
valós nyugtaprofil mellett újraszámolandó. 20 forgalmas napra vetítve.

---

## 4. Amit a fejlesztés közben is mérni kell (nem csak az éles teszten)

### `[ ]` M10 — GraalVM native image build ideje és a fejlesztési sebességre gyakorolt hatása
A native image kényszer a fejlesztési sebességet is érinti; a fázistervnek
be kell áraznia. Ez nem futásidejű, hanem fejlesztői ergonómia-mérés.

### `[ ]` M11 — A teljes teszt-suite futásideje terhelés alatt
§4: „terhelés alatt is futtasd a suite-ot" — két ingadozó teszt (ütköző
temp-fájlnév, egy ablakon mért kétirányú rate-limit) csak párhuzamos futtatással
jött elő korábbi projektben.

---

## 5. Nyitott: mihez kell fizikai hardver

**Mind az M1–M9 fizikai J1900 referenciagépet igényel, az M4/M5/M7/M13 pedig
KETTŐT — az M12 pedig a TELJES referencia-telepítést** (3 Windows POS + 2 tablet
+ 4 telefon + KDS + rendeléskijelző), mert csak így mérhető a valós átvételi
terhelés. Ez beszerzési és logisztikai tétel, nem fejlesztési — a
`NYITOTT_KERDESEK.md` `E3` tételéhez tartozik, és **hetekig tarthat**.
Érdemes a kódolással párhuzamosan elindítani.
