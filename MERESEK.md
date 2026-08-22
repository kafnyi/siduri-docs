# MÉRÉSEK — a mérendő tételek egységes nyilvántartása

> **Ez a fájl azért van, mert a MERNOKISAROKKOVEK §4 kimondja: „Teljesítmény-,
> memória- és versenyhelyzet-állítás CSAK méréssel." Nélküle ezek a tételek
> szétszóródnak a tervben, és a fázisterv írásakor egy részük némán kimarad.**
>
> **Utolsó frissítés:** 2026-08-22 (2. munkamenet)
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

**Mind az M1–M9 fizikai J1900 referenciagépet igényel, az M4/M5/M7 pedig
KETTŐT.** Ez beszerzési és logisztikai tétel, nem fejlesztési — a
`NYITOTT_KERDESEK.md` `E3` tételéhez tartozik, és **hetekig tarthat**.
Érdemes a kódolással párhuzamosan elindítani.
