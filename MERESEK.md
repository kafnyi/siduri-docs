# MÉRÉSEK — a mérendő tételek egységes nyilvántartása

> **Ez a fájl azért van, mert a MERNOKISAROKKOVEK §4 kimondja: „Teljesítmény-,
> memória- és versenyhelyzet-állítás CSAK méréssel." Nélküle ezek a tételek
> szétszóródnak a tervben, és a fázisterv írásakor egy részük némán kimarad.**
>
> **Utolsó frissítés:** 2026-08-23 (3. munkamenet — M15–M19 felvéve)
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
> **`[ÁTMINŐSÍTVE 2026-08-23]` Ez már NEM az alapértelmezés.** Az első ügyfélnél
> **5. gen. i5 a szerver**, tehát ez az eset ott nem áll fenn.
> **Az M1 mostantól az INGYENES EGYGÉPES SZINT padlója** — és pont az a szint
> vonzza a leggyengébb vasat. **Marad, de más okból.**
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
> **`[PONTOSÍTVA 2026-08-23]` A tartalék egy 3. GENERÁCIÓS i3 / 8 GB**, nem J1900
> — mert a J1900-asok tiszta kliensek maradnak. Ez **lényegesen valószínűbbé
> teszi a sikert**, de a mérés **marad kritikus**, mert a HA-terv ezen áll.
>
> ⚠️ **És ez a mérés dönti el, kell-e MÁSODIK i5.** Ha az i3 csúcsban egyszerre
> pénztárgép ÉS szerver nem bírja, akkor a második i5 nem kényelem, hanem
> követelmény. **Az M12 előtt ne vegyen az ügyfél semmit.**

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

### `[ ]` M14 — A telephelyi szerver webes admin felületet is kiszolgál
A hibrid webes architektúra (`gemini_cloud_spec_en.md` §2, R2) szerint **ugyanazt
a webes admin alkalmazást a telephely saját szervere is kiszolgálja**, hogy
internetkimaradáskor is elérhető legyen. Mivel a telephelyi szerver jellemzően
**egy dolgozó Windows POS J1900-on**, ez az M1 terheléséhez **még hozzáad**:
statikus fájlkiszolgálás + a riportokat/statisztikákat hajtó lekérdezések.

**Mit mérj:** a riport-lekérdezések hatása a pénztári válaszidőre, amíg a
manager a webes felületen dolgozik. **Ez a legvalószínűbb valós együttállás:**
a főnök a hátsó asztalnál riportot néz, miközben a pult dolgozik.

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

---

## 6. Fiskális eszköz és napló — a 2026-08-23-i körből

### `[ ]` M15 — **Elfogadja-e az adóügyi eszköz a NULLA összegű tételt?**
A gyártói protokoll szerint a nulla összegű tétel támogatott. Hogy az adott
firmware és a NAV-engedély is elfogadja-e, az **nem következik ebből**.

**Ez blokkoló mérés:** ha nem fogadja el, a teljes „ár nélküli módosító =
szövegsor" megoldás (G2.3) újratervezendő, és visszajön az elvetett kerülőút
kérdése.

**Mérés:** éles készüléken, nulla összegű tétel küldése, a hibakód és a kinyomott
bizonylat rögzítése. Ugyanebben a menetben: **negatív mennyiség**
(göngyölegvisszavétel) és **negatív ár** viselkedése.

### `[ ]` M16 — Melyik gyűjtőre mehet a DRS visszaváltási díj?
A 8 fix rekeszben nincs DRS-hely (G1). A TAM az egyetlen jelölt, de a TAM
„tárgyi adómentes", ami **nem azonos** az „áfa hatályán kívülivel".
**Ez elsősorban kérdés a gyártó és/vagy a NAV felé, másodsorban mérés** —
ha megengedett az AJT rekesz újrakiosztása, azt is ki kell próbálni.

### `[ ]` M17 — Nyomtatási válaszidő és a bizonylat teljes ciklusideje
Mivel a **kliens nyomtat** és a szerver nincs a kritikus úton (G7), a nyugta
kiadásának ideje gyakorlatilag a fiskális eszköz válaszidejétől függ.
**Mérendő:** egy átlagos (6 tételes) és egy nagy (25 tételes, módosítókkal,
szétrobbantott menüvel) bizonylat teljes ciklusa, a több parancsos küldés
darabolásával együtt. Ebből derül ki, hány tétel felett lassul érezhetően.

### `[ ]` M34 — **Kiolvasható és írható-e az eszköz valutaárfolyama?**

A G5.6 előírja, hogy a gép saját valutaárfolyam-beállítását **ki kell írni és
vissza kell olvasni**. A megvalósítás ezt feltételezi — **de a premissza
igazolatlan**, ugyanúgy, mint a P1 (az eszköz szerver nélkül is sorszámoz).

**Három dolog dőlhet el rosszul, és mindháromra más a válasz:**

| Amit mérni kell | Ha nemleges |
|-----------------|-------------|
| **Kiolvasható-e** a beállított árfolyam | Az egyeztetés nem építhető meg; marad a **vak kiírás**, ami pont az, ami ellen a visszaolvasás véd. Ekkor valutát csak **külön kockázatvállalással** szabad engedni |
| **Írható-e** programból | Az egyeztetés helyére **összevetés és tiltás** lép: olvasunk, és eltérésnél nem fogadunk el valutát. A beállítás a gép billentyűzetéről történik |
| **Ugyanúgy kerekít-e**, ahogy mi | A nyugta és a bizonylat forintösszege 1–2 Ft-tal eltérhet. Ez **nem** elhanyagolható: az A2 elv szerint nem záródhat le csendben |

**A visszaolvasás mindhárom esetben kell.** A „kiírtam, tehát beállt"
feltételezés pontosan az a hiba, ami ellen ez az egész lépés véd — és a
következménye nem hibaüzenet, hanem **egy rossz papír a vendég kezében**.

**Mérés:** éles készüléken az árfolyam kiolvasása, beállítása, visszaolvasása,
majd egy valutás nyugta kinyomtatása — és a nyomtatott árfolyam összevetése
azzal, amit visszaolvastunk. Ugyanebben a menetben: mit csinál a gép, ha a
valutaösszeg forintértéke **nem** egész szám, és hogyan jelöli a **visszajárót**.

### `[ ]` M18 — Az audit napló KÉT ágának tényleges mérete
A becslés (G9.2): biztonsági ág ~150–300 rekord/nap/telephely, működési ág
~3000–5000. **A működési ág viszi a tárhelyet, nem a biztonsági.**
**Mérendő:** valós forgalom mellett a rekordszám, a tömörített méret, és a
hash-lánc írási költsége a biztonsági ágon.

### `[ ]` M19 — A replikációs slot WAL-felhalmozódása a 64 GB-os SSD-n
Egy leszakadt tartalék szerverhez tartozó replikációs slot miatt a fő szerver
korlátlanul őrzi a WAL-t. **Mérendő:** mekkora WAL keletkezik óránként valós
csúcsforgalom mellett, tehát **hány óra alatt telik meg a maradék hely**; és
mennyi ideig tart egy **teljes újraszinkronizálás** J1900 páron, ami a slot
érvénytelenedése után elkerülhetetlen. Ebből jön a lemezalapú korlát és a
riasztási küszöb konkrét értéke.

---

## Export és import `[ÚJ — 2026-08-25]`

### `[ ]` M20 — Az Excel-könyvtár natív képbe fordul-e, és lebegőpont nélkül olvas-e
**Ez a legkeményebb a háromból, mert két döntést is dönthet el.**
Az Apache POI erősen reflexió-alapú, a GraalVM natív fordítás pedig pont a
reflexiót nem szereti; a hibák **fordítás után, futásidőben** jelentkeznek.
**Mérendő:** (a) a `fastexcel` és a POI natív képbe illesztése — sikerül-e,
mekkora leíróval; (b) **ad-e az olvasó szöveges cellaértéket**, vagy csak
lebegőpontosat. Ha csak lebegőpontosat ad, **az a könyvtár alkalmatlan**, mert
az import határán megsértené az I1 invariánst *(EXPORT_IMPORT §4.2, §6)*.

### `[ ]` M21 — Húszezer soros export a telephelyi szerveren, POS mellett
Offline esetben a fájlt a telephelyi gép állítja elő, miközben szervert és
POS klienst is futtat. **Mérendő:** csúcsmemória és teljes idő folyamatos
írással, i3-on és J1900-on egyaránt. Ebből jön ki, kell-e sorszám-korlát vagy
háttérbe tett feladat — és ha igen, hol *(EXPORT_IMPORT §5)*.

### `[ ]` M22 — A PDF könyvtár natív képbe fordul-e, magyar ékezetekkel
Ugyanaz a szempont a másik formátumra, plusz a **beágyazott betűtípus**: az
ékezetes karakterek hiánya PDF-ben tipikusan **némán** jelentkezik, kihagyott
vagy dobozzá váló betűkkel. **Mérendő:** natív fordítás, és egy teljes magyar
karakterkészletű minta vizuális ellenőrzése *(EXPORT_IMPORT §6.3)*.

### `[ ]` M23 — A WebSocket-réteg natív képbe fordul-e, és bírja-e a 12 kapcsolatot
Az S1 döntés WebSocketre esett *(`ESEMENYCSATORNA.md`)*, de a GraalVM natív
fordítás viselkedése itt ugyanúgy ismeretlen, mint az Excel- és a PDF-könyvtárnál.
**A puszta keretrendszer-támogatás nem elég bizonyíték:** a natív kép hibái
**futásidőben** jelentkeznek, nem fordításkor.
**Mérendő:** (a) a csatorna natív képbe illesztése — sikerül-e, mekkora leíróval;
(b) **12 tartós kapcsolat** a telephelyi gépen, POS klienssel együtt futva —
memória, és a szívverés tartható-e másodperces ütemben csúcsterhelés alatt.
**Ha megbukik, a csatorna technológiája dől**, és vele a KDS meg a
rendeléskijelző ütemezése.

### `[x]` M24 — A számlamegosztás áfaeltérése `MÉRVE`

**Kérdés:** ha egy rendelést részekre osztunk, a részek áfájának összege
megegyezik-e az osztatlan bizonylatéval?

**Nem.** A visszaszámolás bizonylatonként kerekít, három bizonylat pedig
háromszor kerekít.

| Beállítás | Érték |
|-----------|-------|
| Esetek | 5 000 véletlen rendelés |
| Áfakulcsok | 2 (5% és 27%) |
| Részek | 2–4 |
| **Eltérő eset** | **3 338 / 5 000 (67%)** |
| **Legnagyobb eltérés** | **4 Ft** |

**Ez nem hiba, és nem javítható el** anélkül, hogy vagy a részek összege ne
adná ki a rendelést, vagy valamelyik rész áfája ne a saját tartalmából jönne.
A kettő közül egyik sem cserélhető el erre.

**Következmény a riportra:** a napi összesítő nem feltételezheti, hogy a
bizonylatok áfájának összege megegyezik a rendelések áfájának összegével.
Aki ezt egyeztetni próbálja, forintokat fog keresni, amik nincsenek eltűnve.

**A mérés a tesztben él** (`SzamlamegosztasTest.az_afa_osszege_elterhet`), és
azt is ellenőrzi, hogy **legyen** eltérés: ha soha nem térne el, ez a
figyelmeztetés fölösleges lenne, és akkor törölni kellene, nem meghagyni
„biztos, ami biztos" alapon.

**Kiegészítés (2026-09-14): a teljes HTTP-úton is megjelent, valódi
bizonylatokkal.** Az eddigi mérés a magra futott; ez azt bizonyítja, hogy az
eltérés **a kiadott bizonylatokban** is ott van, nem csak a számításban:

| | |
|---|---|
| Rendelés | 1 200 Ft (27%) + 2 400 Ft (5%) + 750 Ft (27%) = **4 350 Ft** |
| Osztatlan bizonylat áfája | **529 Ft** (5%: 114 · 27%: 415) |
| Három rész áfájának összege | **528 Ft** (3 × 176) |
| **Eltérés** | **−1 Ft** |

A részek összege közben **pontosan kiadta** a rendelést (3 × 1 450 = 4 350 Ft) —
vagyis a pénz nem tűnt el, csak az áfabontás kerekedett másképp. **Pontosan ezt
a kettőt nem lehet egyszerre megtartani**, és a választás tudatos: a pénz
egyezzen, az áfa kerekedjen.

### `[x]` M33 — Az eszköz árfolyama: a kiírás önmagában **nem bizonyíték** `MÉRVE, JAVÍTVA`

**A kérdés, amit feltettem:** ha kiírjuk az árfolyamot az adóügyi eszközre, és a
gép nem tiltakozik, honnan tudjuk, hogy beállt?

**Sehonnan.** És ez nem elméleti: egy elutasított, egy csonkolt vagy egy másképp
kerekített érték **pontosan úgy néz ki, mint egy sikeres** — amíg a nyugta ki nem
jön. Akkor viszont már a vendég előtt állunk, egy olyan papírral, amin más
árfolyam szerepel, mint a bizonylatunkon.

**A mérés** hamis eszközzel készült, amit rá lehet venni a valós
meghibásodásokra. Az egyeztetés **visszaolvasás nélküli** változatával:

| Az eszköz viselkedése | Visszaolvasás nélkül | Visszaolvasással |
|-----------------------|----------------------|------------------|
| Elfogadja és beállítja | ✅ jó | ✅ jó |
| **Elfogadja, de elnyeli** | ✅ „sikeres" — **hamis** | ❌ tiltja a valutát |
| Nincs beállítva rajta semmi | ✅ „sikeres" — **hamis** | ✅ beállítja, ellenőrzi |
| Nem válaszol | kivétel a fizetés közepén | ❌ tiltja a valutát, **a forintos eladást nem** |

A visszaolvasást a kódból kivéve **két teszt azonnal pirosra vált** — vagyis nem
díszlet.

**Négy kimenet, négy teendő** (`ArfolyamSzinkron`): *egyezik* (nem írunk rá újra
— egy fölösleges beállítás is beállítás, és a gép naplójába bekerül),
*beállítva*, *eltér*, *nem használható*. Az utolsó kettőnél **valutát elfogadni
tilos** — de **csak a valutát**: egy néma árfolyam-beállítás nem állíthatja meg
a forintos eladást, mert a vendéglátóhely nem áll le, amiért az euró nem megy.

**Két ponton fut le, és ez nem kettőzés:**

| Hol | Mit véd | Miért nem elég a másik |
|-----|---------|------------------------|
| Az árfolyam betöltésekor | A **gomb** őszinteségét | A gép beállítását közben a saját billentyűzetéről is át lehet írni |
| A lezárás **előtt**, mindent megelőzve | A **bizonylatot** | A gombnál még nem tudjuk, mikor és mivel fizet a vendég |

**A sorrend a lényeg:** az egyeztetés a **legelső** lépés, még a szerveres
lezárás előtt. Fordítva egy kiadott, de kinyomtathatatlan bizonylat maradna
utána — bizonylatszámmal, a vendég előtt.

**Amit a gép mondott, felmegy a szerverre** (`bizonylat.adougyi_arfolyam`).
Enélkül utólag nem az lenne rögzítve, hogy a **gép** egyetértett, csak az, hogy
**mi** hittük. Eltérésnél a szerver **nem utasítja el** a jelentést — a nyomtatás
megtörtént, és az elutasítás azt jelentené, hogy a rendszer nem tud a papírról,
ami a vendég kezében van —, hanem **biztonsági auditba** írja
(`ADOUGYI_ARFOLYAM_ELTERES`). A **hiányzó** árfolyam ugyanolyan eltérés, mint a
rossz: a „nem tudjuk" nem azonos az „egyetértett"-tel.

> ⚠️ `[MÉRENDŐ]` **A premissza igazolatlan** — lásd M34. Feltételezzük, hogy az
> eszköz árfolyam-beállítása kiolvasható és írható. Fizikai készülék nélkül ez
> nem dönthető el.

> **Amit ez a kör mellékesen kijavított:** az adóügyi port eddig a **WPF-es
> kasszaprojektben** élt, tehát Linuxon futó tesztprojektből elérhetetlen volt —
> vagyis a szabályai **nem voltak tesztelhetők**. Önálló, keretrendszer-független
> projektbe került (`Siduri.Pos.Adougyi`). **ÁRA:** egy projekttel több.
> **Cserébe:** a gyártóspecifikus illesztés is ide, egyetlen jól körülhatárolt
> körbe kerül majd — ami nem csak tervezési, hanem **jogi** követelmény is.

---

### `[x]` M32 — A valutás fizetést semmi nem kötötte valódi árfolyamhoz `MÉRVE, JAVÍTVA`

**Amit kerestem:** hol van az árfolyam forrása. **Sehol.** A szerződés `Fizetes`
alakja, a `ValutaOsszeg` és az `Arfolyam` séma kezdettől megvolt, a
`siduri.fizetes` tábla `valutanal_arfolyam_kell` megszorítása ki is követelte
őket — de **azt, hogy az árfolyam IGAZ-e, senki nem nézte meg**.

**A mérés:** a lezárás fizetésellenőrzése (`fizeteseketEllenoriz`) három dolgot
számolt — az összeg egyezését, a készpénzes kerekítést, és a több készpénzes sor
tilalmát. A valutáról **egyetlen sort sem**. Vagyis:

| Amit a kliens küldött | Amit a szerver csinált vele |
|-----------------------|-----------------------------|
| `arfolyam: 300,00` (a valós 395,50 helyett) | Elfogadta, a bizonylatra írta |
| `osszeg: 7000` egy 20 EUR-s soron (a valós 7910 helyett) | Elfogadta, a bizonylatra írta |
| `eladas.fizetes.valuta` jog nélkül | Elfogadta |

**Ez nem elméleti rés.** Az árfolyam a kasszavisszaélés legrövidebb útja: nem a
pénzt kell eltüntetni, csak rosszul átváltani. A jogosultság-katalógusban a
`eladas.fizetes.valuta` kód ott állt, a szerep-sablon helyesen osztotta ki —
**és a szerver soha nem kérdezte meg.** Ugyanaz a minta, mint a lezárás
kedvezmény-jogainál (M28): *ami nincs ellenőrizve, az nincs.*

**Amit a javítás után a szerver megkövetel:**

| Ellenőrzés | Hiba | Miért |
|------------|------|-------|
| Van érvényes árfolyam | `409 ARFOLYAM_NINCS` | Árfolyam nélkül nincs mit a bizonylatra írni |
| A kliens árfolyama **az** érvényes | `409 ARFOLYAM_ELTER` | Csendben nem cserélünk: a vendégnek már mondtak egy összeget |
| A forintösszeg = az átváltás eredménye | `422 VALUTA_ATVALTAS_ELTER` | Ez tartja a pénzt a helyén |
| Valutaadat csak valutás soron | `422 VALUTA_ADAT_NEM_VALUTAS_SORON` | Kártyás soron ott hagyott árfolyam vagy szándékos, vagy hiba |
| **Mind az öt** `eladas.fizetes.*` jog | `403` | Az elrejtett gomb nem jogosultság |

**A visszajáró mérése.** A valutás túlfizetés forintban megy vissza (G5.6), és
ez a fiókból **tényleg kimegy**. Ha a bizonylat csak annyit mondana, hogy „a
számlát valutából fizették", a `muszak_vart_keszpenz` ezzel az összeggel többet
várna:

| | Számla | Átvett | Bizonylatsorok | Fiók forintban |
|---|---|---|---|---|
| Naiv modell | 7 940 | 25 EUR | `VALUTA: 7 940` | 0 — **hamis** |
| Amit építettünk | 7 940 | 25 EUR (= 9 888 Ft) | `VALUTA: 9 888` + `KÉSZPÉNZ: −1 950` (ker. −2) | **−1 950 — igaz** |

A meglévő invariáns változatlanul áll: 9 888 + (−1 950) = 7 938 = 7 940 + (−2).
**Új fogalom nem kellett hozzá** — a negatív készpénzsor pontosan az, ami:
forint, ami elhagyja a fiókot.

**Kettős megvalósítás, differenciál-futtatás.** Az átváltás két nyelven él (a
kassza a pult előtt mondja meg a visszajárót, a szerver ellenőrzi). 500 azonos
generátorral előállított véletlen eset — 1–999 forintos, hat tizedesig random
árfolyam, két tizedes valutaösszeg — mindkét megvalósításon átfuttatva:
**nulla eltérés**. Ezen felül hét kézzel írt fizetési terv a közös
`valuta.json` vektorfájlban, amit a **kassza előállít** és a **szerver
elfogad** — egy megállapodás, a két végén ellenőrizve.

> ⚠️ `[NYITOTT]` **Az adóügyi eszköz saját árfolyam-beállítása.** A G5.6 azt is
> előírja, hogy a gép valutaárfolyamát **ki kell írni és vissza kell olvasni**.
> Az adóügyi illesztő még nincs kész, ezért ez **hiányzik** — és ez nem
> részlet: enélkül a nyugtán más árfolyam szerepelhet, mint a rendszerben.
> **Két árfolyam két papíron.**

> ⚠️ `[TUDATOS KORLÁT]` **A kassza egész eurót vesz át, érmét nem.** A pénzmag
> két tizedessel dolgozik, a *felület* kínál csak bankjegyet: a vendéglátóhelyek
> jellemzően az eurócentet sem felváltani, sem bankba vinni nem tudják. Ha egy
> hely mégis érmét fogad, az **felületi bővítés**, nem pénzszabály-változás.

---

### `[x]` M31 — Az asztalos rendelés szerkezete `MEGÉPÍTVE, MÉRÉS NÉLKÜL`

**Ez nem hibamérés**, hanem annak rögzítése, hogy az asztalos rendelés mely
döntései hol vannak kikényszerítve — és melyik kérdés maradt nyitva.

| Szabály | Hol kényszerül ki | Miért ott |
|---------|-------------------|-----------|
| Egy asztalon **egy** nyitott rendelés | **Egyedi index** (V18) | Egy alkalmazási ágat ki lehet felejteni, egy indexet nem |
| Két írás nem írja felül egymást | **Optimista zárolás** (`verzio`) | Két pincér egy asztalhoz nyúlhat; enélkül az egyik írása **csendben** veszne el |
| 24 óránál tovább nincs nyitva (H6.5) | A szolgáltatás kapujában | A beküldéskor már késő: a vendég elment |
| Más pincér asztala külön jog | `rendeles.mas_pincer_asztala` | Egy idegen asztalra ütött tétel **annak a pincérnek** az elszámolását rontja |

**Amit a zárolás tesztje bizonyít:** kikapcsolva (a `verzio = ?` feltétel
elhagyásával) a teszt **azonnal piros** — vagyis nem díszlet.

> ⚠️ `[NYITOTT]` **J6 — a rendelés átlépi a munkanap-határt.** A rendelés a
> **kezdő** üzleti naphoz tartozik, a bizonylat a **fizetés** napjára kerül. A
> `NYITOTT_KERDESEK.md` J6 szerint **nem tisztázott**, elfogad-e az NTAK egy
> tárgynapra napi zárás **után** beérkező rendelésösszesítőt. Egy 0–24-es
> helyen ez **mindennapos**. A szerkezet ezt már most kiszolgálja; a kérdés a
> beküldés megépítéséig halasztható, de **nem felejthető el**.

> ⚠️ `[MÉRENDŐ]` **Az asztallista válaszideje.** A `GET /asztalok` a
> vendéglátóhely leggyakoribb kérése — minden képernyőfrissítésnél lefut.
> Egy lekérdezésből jön (nem N+1), de a **tényleges** válaszidőt húsz asztalnál,
> J1900-as pultgépen kell megmérni *(F0.3 / M13 környéke)*.

---

### `[x]` M30 — A megosztás eredményét a KOPPINTÁSI SORREND befolyásolta `MÉRVE, JAVÍTVA`

**A súlyozott megosztás felületének építése előtt** néztem meg, mit küld
valójában a képernyő. A kiosztásokat egy `HashSet<int>`-ből olvasta ki,
**bejárási sorrendben**.

**Mérve, futtatva:**

```
csak hozzaadas:       1,2,3
torles utan ujra:     1,2,3
mas koppintassorrend: 3,1,2      ← a 3-ra koppintott eloszor
```

**Miért számít ez egyáltalán:** a maradék forint a **legnagyobb súlyú** részre
kerül, holtversenynél a listában **korábbira**. Egy 1 000 Ft-os sor három
részre osztva 334 / 333 / 333 — és hogy **ki kapja a 334-et**, azt az döntötte
el, melyik gombra koppintott a pincér **először**.

| | |
|---|---|
| Az eltérés mértéke | **1 Ft** részenként |
| Amit megsért | *„ugyanaz a bizonylat kétszer számolva ugyanazt adja"* |
| Kit érint | minden kliens, ami rendezetlenül küld — **a készülő Dart vékonyklienst is** |

**A javítás nem a képernyőn van.** A rendezés a **magba** került
(`Szamlamegosztas.Rendezve`), mert ez szabály, nem felületi részlet — és így
tesztelhető is: a WPF-projektnek ezen a gépen nincs futtatható tesztkészlete
(a `net8.0-windows` cél fordul Linuxon, de nem fut). A képernyő ugyanazt a
rendezett listát használja a **kijelzéshez és a küldéshez**, tehát a kiírt szám
és az elküldött terv nem tud elcsúszni egymástól.

**És a szerződés eddig hallgatott róla.** A `Kiosztas.suly` leírása most már
kimondja *(v1.17.0)*. Ez nem kozmetika: a szabály **megvolt a kódban**, de
sehol nem volt leírva, tehát minden új kliens újra beleszaladt volna.

**A megosztás a kliensen is megvan — 500 esetes differenciál-mérés.**

A megosztóképernyő mostantól **kiírja, ki mennyit fizet**, mielőtt a terv
elmegy. Súlyozott osztásnál ez nem kényelem: a „két adag neki, egy neked"
önmagában elvont szám, és a vendégek a **forintot** vitatják meg egymás közt.

| | |
|---|---|
| Véletlen esetek | **500** (2–5 rész, 1–5 sor, 0–5 súlyok) |
| Összehasonlítva | részenkénti végösszeg **és az elutasítások** |
| **Eltérés** | **0** — a 441 sikeres eset és mind az **59 elutasítás** is egyezik |

A 10 kézzel írt vektor *(`megosztas.json`)* rögzíti a nehéz eseteket. **Az
egyiket a vektor fogta meg, nem a kód:** a „súlyozás több soron egyszerre"
esetnél elszámoltam a 2. részt (1 500-at írtam 2 000 helyett), és a
megvalósítás mondta meg, hogy tévedek.

---

### `[x]` M29 — A C# kliens SOHA nem fordult le, és a pénzszabályok egyezése feltevés volt `MÉRVE`

**A környezet megváltozott, és ez a legfontosabb sor ebben a bejegyzésben:**
a .NET SDK telepíthető ebbe a környezetbe (`dotnet-install.sh --channel 8.0`),
és a WPF-kliens is fordul rajta a `-p:EnableWindowsTargeting=true` kapcsolóval.
**Eddig minden C# munka fordítás nélkül készült** — a helyettesítő ellenőrzés
(XAML-jólformáltság, kötésnevek, zárójel-egyensúly) hasznos volt, de nem az.

**Amit az első fordítás azonnal kiadott — két, régóta bent ülő hiba:**

| Hol | Mi | Miért nem látszott |
|-----|----|--------------------|
| `KozosVektorokTeszt.cs` | Egy teszt **metódus neve** (`Sorosszeg`) elfedte az azonos nevű **osztályt**, amit hívni akart | Csak a fordító látja |
| `FizetestervTeszt.cs` | xUnit-elemzői hiba (`Where` az `Assert.Single` előtt), és a projekt **hibává** minősíti a figyelmeztetéseket | Csak a fordító látja |

**Vagyis a kliens tesztkészlete soha nem futott le.** Ez azt is jelenti, hogy
egy ott ülő, kész ellenőrzés — *„minden szerződésfájl szerepel a
lenyomatjegyzékben"* — **némán állt**. Amikor végre lefutott, azonnal igazat
mondott: a `tesztvektorok/*.json` fájlok **nem** voltak a jegyzékben, tehát egy
kézzel átírt vektor észrevétlen maradt volna.

> ⚠️ **A tanulság nem az, hogy a tesztek jók.** Az, hogy **egy teszt, ami nem
> fut, pontosan annyit ér, mint a hiánya** — de közben azt az érzést kelti,
> hogy a terület le van fedve. Ez rosszabb, mint ha ott sem lenne.

**A pénzszabályok egyezése: 500 esetes differenciál-mérés.**

A kedvezményszámítás mostantól **két nyelven** él (Java szerver, C# kassza),
mert a kassza a fizetőképernyőn kiírja a fizetendőt, mielőtt a szerver válasza
megérkezne. Az eltérés ára nem elméleti: a szerver *„a fizetés nem egyezik"*
hibával utasítja el a lezárást — a vendég előtt, készpénzzel a kézben.

| | |
|---|---|
| Véletlen esetek | **500** (1–4 áfakulcs, százalékos/fix/nincs kedvezmény, 0–100% szervizdíj, borravaló) |
| Összehasonlítva | áfacsoportonkénti bruttó, áruk összege, végösszeg |
| **Eltérés** | **0** |

A 8 kézzel írt közös vektor *(`kedvezmeny.json`)* a nehéz eseteket rögzíti — a
maradék szétosztását, a holtverseny feloldását, a szervizdíj alapját, a nem
bontható kategóriát —, a 500 véletlen eset pedig azt mutatja, hogy a két
megvalósítás **nem csak a kiválasztott pontokon** egyezik.

> ⚠️ `[MÉRENDŐ]` **A WPF-felület továbbra sem FUT itt, csak fordul.** A
> képernyők tényleges viselkedését — fókusz, érintés, kiosztás a J1900-on —
> csak valódi gépen lehet megnézni *(F0.3)*.

---

### `[x]` M28 — A lezárás egyetlen jogosultságot sem ellenőrzött `SÖPRÉSSEL TALÁLVA, JAVÍTVA`

**Ez nem mérés volt, hanem söprés** — az M27 tanulságából született új köri
ellenőrzés első éles futása: *melyik katalóguskódot nem ellenőrzi soha a kód.*

| | |
|---|---|
| Katalóguskódok | **84** |
| Soha nem ellenőrzött | **69** |
| Ebből még meg nem épült funkció | 64 — ez rendben van |
| **Élő kódútra vonatkozó** | **5** |

**Az öt, és amit engedett:**

| Jogosultság | Mit engedett bárkinek |
|-------------|----------------------|
| `kedvezmeny.vegosszeg` | Tetszőleges végösszeg-kedvezmény — **a vendégtől teljes ár, a gépbe kedvezmény** |
| `kedvezmeny.kuszob_felett` | A küszöb feletti kedvezményt is, vezetői rálátás nélkül |
| `szervizdij.modositas` | A szervizdíj átírását — a felszolgálói jutalék alapját |
| `eladas.szamla_keres` | Nyugta helyett számlát, más adóügyi úton |
| `kassza.borravalo_kifizetes` | *(közvetve)* a borravaló kivételét a `kassza.kifizetes` joggal |

⚠️ **A `rendelestLezar` szó szerint nulla jogosultság-ellenőrzést tartalmazott.**
Nem rossz feltétel volt benne, nem elavult kód — **nem volt ott semmi**.

**Két további lelet a javítás közben:**

1. **A küszöb megkerülhető volt egy legördülő-választással.** A
   küszöbvizsgálat csak a **százalékos** kedvezményt nézte. Egy 10 000 Ft-os
   számlára adott **9 999 Ft-os „fix" kedvezmény — 99,99%** — indok és külön
   jog nélkül átment. A fix összeget mostantól a kedvezmény előtti alaphoz
   arányítjuk.
2. **A `BORRAVALO_KIVET` mozgástípus fél kézzel volt megépítve.** Az
   adatbázis a V9 óta ismerte *(„SOHA NEM LEHET NYOMKÖVETHETETLEN FIÓKKIVÉT")*,
   az indokkód és a jogosultság is létezett — **a kód viszont soha nem
   állította elő**. A tervező szándéka megvolt, a huzal hiányzott.

**⚠️ Ami ezt enyhíti, és ami nem.** A POS-kliensnek **nincs** kedvezmény-,
szervizdíj- vagy számlaigény-felülete, tehát **ezen a kasszán** a négy lezárási
jog nem volt elérhető. A rés az **API-felületen** volt valódi: bármely más
kliens, egy vékonykliens, vagy egy közvetlen hívás kihasználhatta volna. **Ez
nem menti a hibát** — a szerver nem építhet arra, hogy a saját kliense jól
viselkedik.

> ⚠️ **A söprés a következő körben is fusson.** A maradék ellenőrizetlen kódok
> között most nincs ilyen súlyú — a legközelebb figyelendők: `kedvezmeny.tetel`
> és `ar.kezi_felulriras`, amint a tételszintű kedvezmény, illetve a kézi
> árfelülírás megépül. **A jog ellenőrzését a funkcióval EGYÜTT kell megírni,
> nem utána.**

---

### `[x]` M27 — A sztornó a lezárt napra és a lezárt műszakba került `MÉRVE, JAVÍTVA`

**Ez sem terv szerinti mérés volt:** a *régebbi bizonylatok sztornózása*
építése előtt azt akartam ellenőrizni, **biztonságos-e egyáltalán** egy tegnapi
nyugtát visszavonni. Nem volt az.

A sztornó az **eredeti** bizonylat üzleti napját és **eredeti** műszakját
örökölte. Élő szerveren mérve:

```
   eredeti üzleti napja : 2026-10-24
   sztornó üzleti napja : 2026-10-24
   a NYITOTT nap        : 2026-10-25
   a sztornó műszakja   : … állapota: LEZART
   ⚠️ A SZTORNÓ A LEZÁRT MŰSZAKBA KERÜLT.
   Az 1. műszak várt készpénze MOST: -1200 Ft
   A záráskor rögzített várt érték : 1200 Ft
   ⚠️⚠️ A LEZÁRT MŰSZAK SZÁMA VISSZAMENŐLEG MEGVÁLTOZOTT.
```

**Három seb, és mindhárom néma volt:**

| # | Mi történt | Miért súlyos |
|---|-----------|--------------|
| 1 | A **lezárt** műszak várt készpénze 1 200 → −1 200 Ft | Egy elszámolt, **átadott** kassza száma módosult az átadás **után**. Aki aláírta, már nem azt írta alá, ami ott van |
| 2 | A bizonylatszám a lezárt nap sorozatából folytatódott | A szám előtagja **maga az üzleti nap** (`yyMMdd`): egy **ma** kiadott bizonylat egy **már lejelentett nap** számsorát toldotta meg |
| 3 | A pénz **ma** jött ki a fiókból, a hiánya tegnapra könyvelődött | A mai kassza bevétele többet mutat, mint ami benne van — és a különbözetet a **mai** műszakon keresik |

**És egy negyedik, amit csak a javítás közben talált meg a számolás.** A várt
készpénz adatbázisfüggvénye **kihagyta** a sztornózott bizonylatokat
(`b.allapot <> 'SZTORNOZOTT'`), miközben a sztornó **saját negatív
fizetéssorai** ugyanabban a műszakban voltak. Két külön mechanizmus ugyanarra
a visszavonásra. A régi és az új képlet valós sorokon összevetve:

| Eset | Régi képlet | Helyes |
|------|------------|--------|
| 1 000 Ft-os nyugta saját műszakban sztornózva | **−1 000 Ft** | **0 Ft** |
| 1 270 Ft-os nyugta saját műszakban sztornózva | **−1 270 Ft** | **0 Ft** |

Vagyis a kihagyás nem is a lezárt napnál kezdett el hazudni, hanem **már
ugyanabban a műszakban is**: a fiók mínuszban állt egy olyan visszavonás után,
ami után pontosan ott kellett volna lennie, ahol azelőtt.

**A javítás nem kivételez, hanem összead.** A sztornó önálló bizonylat,
negatív fizetéssorokkal, abban a műszakban, ahol a pénz **ténylegesen** kijön
a fiókból *(V17 migráció)*:

| | 1. műszak | 2. műszak |
|---|---|---|
| Ugyanabban a műszakban visszavonva | +1 200 − 1 200 = **0 Ft** | — |
| Másnap visszavonva | **+1 200 Ft** *(ennyi volt a fiókban záráskor)* | **−1 200 Ft** *(ennyi megy ki ma)* |

**Miért nem fogta meg teszt — harmadszor ugyanaz a minta.** 384 zöld teszt
futott, és a sztornó-fixek után **egyetlen sem lett piros**. A sztornó tesztjei
azt nézték, **keletkezik-e** negatív bizonylat, azt nem, hogy **hova**. A
javítást megelőzően megírt nyolc új teszt közül **öt azonnal piros lett** a
régi kóddal — vagyis nem az volt a baj, hogy nehéz mérni, hanem hogy senki nem
nézett oda.

**Egy negyedik lelet, ugyanebből a körből:** a `sztorno.mas_muszakbol`
jogosultság a katalógusban **létezett**, az ÜZLETVEZETŐ sablonjában **benne
volt** — és a kód **sehol nem hivatkozott rá**. Egy műszakfelelős a saját mai
nyugtáját és a tegnap estit ugyanazzal az **egy** joggal vonhatta vissza. A
megadott jog nem az, amit érvényesítünk: **ami nincs ellenőrizve, az nincs.**

> ⚠️ **Tanulság a következő körre:** a jogosultságkódok katalógusa és a kódban
> ténylegesen ellenőrzött kódok halmaza **eltérhet**, és az eltérés néma. Egy
> teszt bizonyítja, hogy minden *hivatkozott* kód létezik a katalógusban — a
> fordított irányt (**minden katalóguskódot ellenőriz-e valaki**) semmi nem
> bizonyítja. Ezt a söprést is fel kell venni a köri ellenőrzésbe.

---

### `[x]` M26 — A készpénzmozgás előjelének hiánya `MÉRVE, JAVÍTVA`

**Nem terv szerinti mérés volt:** a készpénzmozgás képernyőjének bekötésekor
derült ki, hogy **a szerver nem tette rá az előjelet** a mozgás összegére.

A várt kasszatartalom **egyetlen összegzésből** áll
(`sum(keszpenzmozgas.osszeg)`), típusonkénti ágazás nélkül — a tábla kommentje
ezt ki is mondja. Ehhez az kell, hogy az előjel a **tárolt** értékben legyen.
Nem volt benne.

| | |
|---|---|
| Nyitó készpénz | 100 000 Ft |
| Váltópénz +5 000 · Befizetés +10 000 · Kifizetés −2 500 · Fölözés −50 000 | |
| **Helyes várt kasszatartalom** | **62 500 Ft** |
| **Amit a hibás kód adott** | **167 500 Ft** |
| **Eltérés** | **105 000 Ft** — pontosan a kifizetés és a fölözés kétszerese |

**Miért nem fogta meg teszt:** a szolgáltatásréteg tesztje maga küldte az
előjelet (`Penz.forint(-15_000)`), vagyis **a saját feltevését ellenőrizte**.
Az új HTTP-végpont viszont — a szerződés szerint helyesen — pozitív összeget
adott tovább, és ott bukott ki.

**A javítás ott van, ahol minden hívó átmegy:** a szolgáltatásban. Ha minden
hívó maga előjelezne, az ágazás annyi helyen lenne, ahányan hívják, és **egy
elfelejtett ág csendben hamis számot adna.** Pontosan ez történt.

**A regressziós teszt bizonyítottan fog:** a javítás nélkül 62 500 helyett
167 500 jön ki.

### `[~]` M25 — A PIN-lenyomatolás költsége `RÉSZBEN MÉRVE`

**Kérdés:** hány iterációt bír el a PBKDF2 úgy, hogy a belépés a pult mögött ne
legyen érezhetően lassú?

**Mérve** (Intel Xeon @ 2,8 GHz, PBKDF2-HMAC-SHA512, legjobb az 5 futásból):

| Iteráció | Idő |
|----------|-----|
| 10 000 | 16,8 ms |
| 50 000 | 69,3 ms |
| 100 000 | 120,4 ms |
| **210 000** *(OWASP ajánlás)* | **250,2 ms** |
| 400 000 | 473,2 ms |

**A választott érték: 60 000** (≈83 ms ezen a gépen).

**Miért nem az OWASP 210 000-e:** a célgép a **J1900**, ami ennél a Xeonnál
becslés szerint 3–4-szer lassabb — vagyis az OWASP-érték ott **közel egy
másodperc belépésenként**. Egy műszakkezdésnél, öt ember után ez fél perc
állás a pultnál.

**És miért fér ez bele:** mert a PIN kulcstere **tízezer**. Az iterációszám
emelése a támadónak percekben, a kezelőnek másodpercekben számít:

| Iteráció | 10 000 tipp végigfuttatása |
|----------|---------------------------|
| 60 000 | ~8 perc |
| 210 000 | ~42 perc |

**Egyik sem védelem.** A PIN-t nem a KDF védi, hanem a **bors** — a szerveren
tartott kulcs, ami nincs az adatbázisban. Ahol egy paraméter másodrendű, ott a
kisebb üzemeltetési kockázat nyer.

> ⚠️ `[MÉRENDŐ]` **A J1900-as szám becslés, nem mérés.** A tényleges értéket a
> K3/a hardver megérkezésekor kell megmérni *(F0.3)*. Ha ott a 60 000 is
> 500 ms fölött van, lejjebb kell vinni — és akkor azt is ki kell mondani,
> hogy a KDF ott már tényleg csak formaság.
