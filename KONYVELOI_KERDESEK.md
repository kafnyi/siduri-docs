# Kérdések a könyvelőnek / adótanácsadónak

**Tárgy:** vendéglátóipari POS-rendszer (Siduri) adójogi kérdései
**Készült:** 2026-08-23

---

## Hogyan használd ezt a dokumentumot

**Ez a lista úgy van felépítve, hogy egy gyenge válasz is hasznos legyen.**

Minden kérdésnél szerepel:

| Rész | Mire jó |
|------|---------|
| **Amit mi feltételezünk** | Ha a válasz csak annyi, hogy „igen, jó", az is használható |
| **Mire alapozzuk** | Ahol van elsődleges forrásunk, ott hivatkozzuk — így ellenőrizhető, hogy a válasz ezzel összhangban van-e |
| **Mi múlik rajta** | Ha a válasz bizonytalan, ebből látszik, mennyire kockázatos rá építeni |

> **A cél nem az, hogy a könyvelő megmondja a megoldást, hanem hogy
> MEGERŐSÍTSE vagy CÁFOLJA a mi álláspontunkat.** Ahol cáfol, ott kérjük az
> indoklást is — mert több helyen már utánanéztünk elsődleges forrásból, és ha
> eltérés van, azt fel kell oldani, nem elfogadni.

**Ami a legfontosabb: ha valamire nem tud biztosat mondani, azt mondja meg.**
Egy „nem tudom" használhatóbb, mint egy bizonytalan „szerintem igen" — mert az
elsőre tudunk NAV-állásfoglalást kérni, a másodikra nem.

---

## A) Az MI kérdéseink — ezekre nincs biztos válaszunk

### A1 — Borravaló adóztatása `FONTOS`

**A helyzet:** a rendszer külön kezeli a **készpénzes** és a **kártyás**
borravalót. A kártyás a cég bankszámlájára érkezik, a készpénzes a kasszában van.

**Amit mi feltételezünk:** a kettő adójogi kezelése **eltér**, és a kártyás
borravaló kifizetése a dolgozónak **valamilyen jövedelemként adózik**.

**Kérdések:**

1. Hogyan adózik a **készpénzes** borravaló, amit a vendég közvetlenül a dolgozónak ad?
2. Hogyan adózik a **kártyás** borravaló, ami a cég számlájára érkezik, majd a dolgozóhoz kerül?
3. Van-e különbség a **borravaló** és a **felszolgálási díj (szervizdíj)** között ebből a szempontból?
4. **Hogyan kell kifizetni** a kártyás borravalót ahhoz, hogy szabályos legyen — bérként, egyéb jövedelemként, vagy máshogy?
5. Milyen **nyilvántartást** kell vezetni hozzá?

**Mi múlik rajta:** a rendszer **felhasználónkénti borravaló-riportot** készít a
hó végi elszámoláshoz. Tudnunk kell, **milyen bontásban** és **milyen adattal**
hasznos ez a könyvelésnek.

---

### A2 — Előleg áfakulcsa vegyes fogyasztásnál `FONTOS`

**A helyzet:** egy társaság asztalt foglal, és hetekkel előre kifizet
pl. 50 000 Ft előleget. A tényleges fogyasztás **vegyes adómértékű** lesz:
étel **5%**, alkoholos ital **27%**.

**Amit mi feltételezünk:** az előleg átvétele **adófizetési kötelezettséget
keletkeztet a megfizetés napján**, és **előlegszámlát** kell kiállítani.

**Kérdések:**

1. **Milyen áfakulcson** kell az előleget leszámlázni, ha a jövőbeni fogyasztás adómértéke vegyes és előre nem ismert?
2. **Meg kell osztani** az előleget adómértékek szerint? Ha igen, **milyen arányban** — és ki határozza meg?
3. Vagy a feleknek **előre meg kell határozniuk**, mire szól az előleg?
4. A **végszámlán** hogyan kell az előleget beszámítani?
5. Mi történik a **fel nem használt** előleggel, ha a vendég nem jelenik meg?

**Mi múlik rajta:** hogy egyáltalán meg tudjuk-e építeni az előleg-funkciót
determinisztikusan, vagy minden esetben emberi döntés kell.

---

### A3 — Személyzeti fogyasztás és selejt `KÖZEPES`

**A helyzet:** a rendszer a **személyzeti fogyasztást (repi)** és a **selejtet**
**készletmozgásként** rögzíti, nem eladásként — a tiszta könyvelés érdekében.

**Kérdések:**

1. Helyes-e ez a kezelés, vagy valamelyiket **értékesítésként** kell kezelni?
2. A **személyzeti étkezés** természetbeni juttatásnak minősül-e, és ha igen, milyen adóvonzattal?
3. A **selejtről** milyen bizonylatot és nyilvántartást kell vezetni ahhoz, hogy elfogadható legyen?
4. Van-e olyan **mennyiségi vagy értékhatár**, ami fölött ez már kifogásolható?

**Mi múlik rajta:** két dolog. Egyrészt hogy a NAV felé kell-e bármit
jelentenünk. Másrészt hogy az NTAK felé kell-e — mert ha igen, akkor egy
**személyzeti asztal sem lehet 24 óránál tovább nyitva** (az NTAK ezt kemény
validációval korlátozza).

---

### A4 — Számla és nyugta ütközése `FONTOS`

**A helyzet:** ha a vendég **áfás számlát** kér, és a tranzakciót **az adóügyi
eszközön is lezárnánk**, ugyanaz az értékesítés **kétszer kerülne be a hatóság
felé** — egyszer a pénztárgép adatszolgáltatásán, egyszer az Online Számla
rendszeren.

**Amit mi feltételezünk — és amit így építünk meg:**

| Eset | Amit tervezünk |
|------|----------------|
| A vendég a fizetés **ELŐTT** kér számlát | A rendszer **nem küld semmit** az adóügyi eszközre; számlát állítunk ki |
| A vendég a **nyugta után** kér számlát | **A nyugtát SZTORNÓZZUK**, és utána állítjuk ki a számlát |

**Kérdések:**

1. **Helyes-e ez a két útvonal?**
2. Az utólagos számlaigénynél **tényleg sztornózni kell** a nyugtát, vagy van más szabályos út?
3. Ha nyugtát adtunk és utána számlát is, **hogyan kell dokumentálni** a kapcsolatot a kettő között?
4. A nem adóügyi eszközön nyomtatott, „NEM ADÓÜGYI BIZONYLAT" jelöléssel ellátott példány **adhat-e** a vendégnek, számla mellé?

**Mi múlik rajta:** ez **napi szintű** művelet minden étteremben. Ha rosszul
csináljuk, minden számlaigénynél kettős bevételjelentés keletkezik.

---

### A5 — Utalványok `KÖZEPES`

**A helyzet:** ajándékutalvány eladása és beváltása.

**Amit mi feltételezünk:** kétféle utalvány létezik, és **ellentétesen adóznak**:

| Típus | ÁFA az eladáskor | ÁFA a beváltáskor |
|-------|------------------|-------------------|
| **Egycélú** (a beváltáskori adómérték és a teljesítés helye eladáskor ismert) | adóztatandó | nincs |
| **Többcélú** (bármire beváltható, vegyes adómértékkel) | **áfa hatályán kívül** | ekkor keletkezik az adókötelezettség |

**Kérdések:**

1. **Helyes-e ez a megkülönböztetés?**
2. Egy **étterem saját ajándékutalványa**, ami bármire beváltható (étel + alkohol) — **többcélú**, ugye?
3. Az utalvány **eladását** hogyan kell bizonylatolni? Kell-e adóügyi bizonylat, és ha igen, **milyen adómértékkel** vagy gyűjtőn?
4. A **beváltást** hogyan? (Mi fizetési módként terveztük kezelni.)
5. A **kintlévő, be nem váltott** utalványok hogyan jelennek meg a könyvelésben?
6. Van-e **elévülési** szabály?

---

### A6 — Szervizdíj (felszolgálási díj) `KÖZEPES`

**A helyzet:** a rendszer a szervizdíjat **önálló tételként**, **áfakulcsonként
bontva** kezeli — mert az adóügyi eszköz gyűjtőkiosztásában a szervizdíjnak
**saját, áfakulcsonkénti rekeszei** vannak.

**Kérdések:**

1. **Helyes-e**, hogy a szervizdíj a mögötte lévő termékek áfakulcsát követi, áfakulcsonként bontva?
2. Van-e **jogszabályi felső határa** a szervizdíj mértékének? *(Mi úgy tudjuk, hogy nincs — a követelmény az előzetes ártájékoztatás. Kérjük megerősíteni.)*
3. Milyen **tájékoztatási kötelezettség** van (étlap, árlista, nyugta)?
4. A szervizdíj **kifizethető-e** a dolgozóknak, és ha igen, milyen adózással? *(Kapcsolódik az A1-hez.)*

---

## B) Amit MI már megnéztünk — csak megerősítést kérünk

> Ezekre **elsődleges forrásból** dolgoztunk. Ha a válasz eltér attól, amit
> alább írunk, **kérjük az indoklást és a jogszabályhelyet** — mert akkor
> valamelyikünk téved, és azt fel kell oldani.

### B1 — Helyben fogyasztás vs. elvitel áfakulcsa

**Amit mi tudunk:** az **5%-os** kulcs az **étkezőhelyi vendéglátáshoz** kötődik
(helyben fogyasztás). **Elvitel és kiszállítás esetén ez nem alkalmazható.**

**Kérdés:** megerősíti? És **pontosan mi számít „helyben fogyasztásnak"** abban
az esetben, ha a vendég az étteremben rendel, de elviszi?

**Mi múlik rajta:** a rendszerben **minden terméknek két áfakulcsa van**
(helyben / elvitel), és **a besorolás az ügyfél felelőssége.** Nem égetünk kulcsot
a kódba — de a helyes gyakorlatot tudnunk kell.

---

### B2 — Kiszállítás áfakulcsa

**Amit mi tudunk:** a kiszállítás **nem** étkezőhelyi vendéglátás, tehát az
elviteli kulcs alkalmazandó, nem az 5%.

**Kérdés:** megerősíti? Van-e olyan eset, amikor kiszállításnál mégis 5%?

---

### B3 — DRS (kötelező visszaváltási díj)

**Amit mi tudunk** — NAV 2023-11 adózási kérdés és 450/2023. (X. 4.) Korm.
rendelet alapján:

| Állítás |
|---------|
| A díj **darabonként 50 Ft**, egyutas 0,1–3 literes italcsomagolásra |
| **Tej és tejtartalmú italtermék kivétel** |
| A díj **NEM része az értékesítés adóalapjának** — az **áfa hatályán kívüli** tétel |
| A nyugtán **a termék árától elkülönítve** kell feltüntetni |
| Visszaváltáskor **az adóalap nem csökkenthető** a díjjal |
| **Újrahasználható** csomagolásnál MÁS a szabály: a betétdíj **benne van** az adóalapban |
| **A díj nem árbevétel** — átfutó tétel |

**Kérdések:**

1. Megerősíti a fentieket?
2. **A könyvelésben hogyan jelenik meg** a kifizetett és a visszakapott visszaváltási díj?
3. **Melyik pénztárgép-gyűjtőre** kerülhet? A rendelkezésre álló gyűjtők: 5% / 18% / 27% / **TAM** / **AJT**. **A TAM „tárgyi adómentes", ami nem azonos az „áfa hatályán kívülivel"** — elfogadható-e mégis, vagy más megoldás kell?

**A 3. kérdés a legfontosabb**, és lehet, hogy inkább a pénztárgép-forgalmazónak vagy a NAV-nak szól.

---

### B4 — Kerekítés vegyes fizetésnél

**Amit mi tudunk:** az 5 forintra kerekítés **csak a készpénzes fizetésre**
vonatkozik, és vegyes fizetésnél **a készpénzes részre**, nem a végösszegre.

*Példa:* 1 234 Ft-os számla, 1 000 Ft kártyával + 234 Ft készpénzzel → a
készpénzes rész **235 Ft**.

**Kérdés:** helyes ez a példa?

---

### B5 — Megőrzési idő

**Amit mi tudunk:** a számviteli bizonylatokat **8 évig** kell megőrizni.

**Kérdések:**

1. Megerősíti a 8 évet?
2. **Pontosan mely dokumentumokra** vonatkozik: nyugta, számla, napi zárás, pénztárjelentés, készletbizonylat?
3. **Mikortól** számít a 8 év?
4. Elfogadható-e, ha ezek **kizárólag elektronikusan**, felhőben tároltak?
5. Van-e **eltérő megőrzési idő** bármelyikre?

**Mi múlik rajta:** a rendszer **helyben 30 napot** őriz, minden mást felhőben.
Ha valamire hosszabb vagy szigorúbb szabály vonatkozik, azt tudnunk kell.

---

### B6 — Valuta (EUR) elfogadása

**Amit mi tudunk:** az árfolyamot előre meg kell adni és közölni kell; a
visszajáró forintban adható.

**Kérdések:**

1. Milyen **árfolyamot** kell alkalmazni, és mennyi ideig érvényes?
2. Kell-e az árfolyamot **a nyugtán** feltüntetni?
3. Van-e **közzétételi kötelezettség** (kiírás a vendégtérben)?
4. A visszajáró **adható-e forintban**, vagy valutában kell?

---

## C) Amit érdemes megkérdezni, mert az ügyfelet érinti

### C1 — Az első ügyfél átállása

Az első telephely **jelenleg is működik**, tehát **rendszert vált**.

**Kérdések:**

1. Az **NTAK-adatszolgáltatás** szempontjából mi a helyes átállási eljárás? A régi és az új szoftver **egyszerre** nem jelenthet ugyanarról a forgalomról.
2. Van-e olyan **fordulónap**, amihez az átállást igazítani kell (hó-, negyedév-, évforduló)?
3. A **készlet nyitóértékét** hogyan kell megállapítani és dokumentálni az átálláskor?
4. A régi rendszer adatait **meddig és milyen formában** kell megőrizni az átállás után?

---

## D) Ha valamire nem tud választ adni

Ezekre **NAV-állásfoglalást** vagy a **pénztárgép-forgalmazó** véleményét kérjük:

| # | Kérdés | Kihez |
|---|--------|-------|
| 1 | A DRS visszaváltási díj gyűjtője az adóügyi eszközön (B3/3) | forgalmazó / NAV |
| 2 | Az előleg áfakulcsa vegyes fogyasztásnál (A2) | NAV |
| 3 | Az utólagos számlaigény kezelése kiadott nyugta után (A4/2) | NAV |
| 4 | A többcélú utalvány bizonylatolása pénztárgépen (A5/3) | forgalmazó / NAV |
