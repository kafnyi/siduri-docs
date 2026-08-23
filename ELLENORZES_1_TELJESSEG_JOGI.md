# ELLENŐRZÉS — 1. kör: TELJESSÉGI és JOGI

> **Kérte:** a felhasználó, 2026-08-22. Szó szerint: *„hogy biztos mindent
> lezártunk-e, minden jó-e, nem maradt-e ki ötlet, amit még jónak vagy beleillőnek
> gondolsz, és mindenhol megfelelünk-e a magyar jogszabályi előírásoknak."*
>
> **Módszertan:** MERNOKISAROKKOVEK §11 (teljességi kritikus) és §13.5
> (jogi állítás CSAK forrással).
>
> **Ezt a kört egy MÁSODIK, adverzariális kör követi** — ott a feladat a cáfolat.
>
> **Állapot a kör indulásakor:** 85 lezárt döntés, **71 nyitott tétel**,
> **11 igazolatlan premissza**.

---

# I. RÉSZ — JOGI MEGFELELÉS, FORRÁSOKKAL

> **§13.5:** jogi állítás forrásmegjelölés nélkül nem használható, és **nem
> csatornázható a felhasználó döntésébe.** Ez a szakasz **kizárólag olyan
> állítást tartalmaz, amit forrásból ellenőriztem** — és ahol csak másodlagos
> forrásom van, azt kiírom.

## `[!] L1 — LEGSÚLYOSABB LELET: az online pénztárgépeknek DÁTUMOZOTT LEJÁRATA van`

### A tény

**2028. július 1-ig használható még az online pénztárgép.** Utána **csak
e-pénztárgép**. A vonatkozó jogszabály: **8/2025. (III. 31.) NGM rendelet** az
e-pénztárgépek forgalmazásáról, üzemeltetéséről, valamint az e-pénztárgépek és
az e-nyugta kiállításának követelményeiről. Az e-pénztárgépes szabályok
**2025. július 1-jén** léptek hatályba (57. § (2)); azóta a pénztárgép-használatra
kötelezett adózó **választhat** az online pénztárgép és a hardveralapú
e-pénztárgép között (3. § (2)).

**Forrás:** [NAV — Az e-pénztárgépeké a jövő](https://nav.gov.hu/sajtoszoba/hirek/az-e-penztargepeke-a-jovo-ma-lepett-hatalyba-a-rendelet)
(szó szerint: *„2028. július 1-ig még használható az online pénztárgép"*),
[8/2025. (III. 31.) NGM rendelet](https://net.jogtar.hu/jogszabaly?docid=a2500008.ngm).

### Miért ez a legsúlyosabb lelet

**A terv teljes fiskális rétege (spec 12., C10, F3) a MAI online pénztárgépekre
épül** (Micra, CashCube, AEE-s eszközök, soros/TCP protokoll). Ennek a rétegnek
**ismert lejárati dátuma van.**

Egyszerű időszámítás, a terv jelenlegi állapotából:
- a kódolás **még el sem kezdődött** (2026-08),
- a fázisterv **még nincs megírva**,
- ha a termék 2027 folyamán élesedik, akkor a **fiskális integrációnak
  nagyjából egy éve van**, mielőtt a támogatott eszközosztály kifut.

### Amit ez a tervben MEGDÖNT

**A `C12` tétel (e-nyugta / NAV nyugtatár) jelenlegi kezelése HIBÁS.**
A `C12` így fogalmaz: *„Stratégiai kérdés: most tervezünk rá helyet a
bizonylat-modellben, vagy tudatosan későbbre toljuk?"* — és az igazolatlan
premisszák táblája szerint a feltevés az, hogy *„az e-nyugta iránnyal most nem
kell foglalkozni"*.

**Ez a feltevés cáfolva.** Nem stratégiai választás, hanem **dátumozott,
jogszabályban előírt átállás**, ami a termék várható élettartamán belül van.

### Amit NEM dönt meg

**Az MVP-t nem kell e-pénztárgépre építeni.** Az online pénztárgép **2028-ig
legális**, és a meglévő telepített bázis is azt használja. A lelet nem azt
mondja, hogy most kell átállni — hanem hogy **az átállásnak helye kell legyen az
architektúrában és a fázistervben**, nem „majd meglátjuk" státuszban.

### `[ ]` Amit javaslok

1. **A `C12` státusza `[?]`-ról `[!]`-ra változzon**, és kerüljön a fázisterv
   nevesített tételei közé — nem az MVP-be, hanem **dátumozott ütemezéssel**.
2. **A bizonylat-modell MOST kapjon helyet mindkét formátumnak** (lásd `L4`) —
   ez most néhány mező, később migráció.
3. **`[ ]` Üzleti döntés a felhasználónak:** a 2028-as határidő **értékesítési
   érv is lehet** (aki ma vásárol, annak úgyis váltania kell — a Siduri
   felkészülten várja), vagy **kockázat**, ha egy versenytárs előbb áll át.
   Ez termékpozicionálás, nem mérnöki kérdés (§12).

---

## `[!] L2 — Az A2 TEHERHORDÓ PREMISSZÁJA IGAZOLVA (a legfontosabb jó hír)`

### A premissza, ami eddig igazolatlan volt

A `FOLYAMATBAN.md` 3. szakasza szerint **ez az egyetlen olyan tétel, ahol MÁR
MEGHOZOTT DÖNTÉS áll igazolatlan premisszán**: hogy az adóügyi eszköz **maga
állítja ki és sorszámozza** a jogi bizonylatot, tehát a Siduri szerver kiesése
nem akadálya a szabályos nyugtaadásnak. Ha hamis, **az `A2` és `A2/a` egésze,
és rá épülve a csökkentett mód megdől.**

### A bizonyíték

A **8/2025. (III. 31.) NGM rendelet** 2. melléklet B) rész II. fejezet 6. pontja
szerint a bizonylatokat **az e-pénztárgép látja el egyedi sorszámmal**, a
`NY–AP/ASZ/AN/NS` szerkezet szerint (AP = az e-pénztárgép száma, ASZ = adószám,
AN = a nap sorszáma, NS = napi sorszámláló). **A NAV nem adja a sorszámot** —
csak az AP-számot osztja ki (49. §).

**Ugyanez a szerkezet a MAI eszközöknél is** — a felhasználó által megadott,
utánanézett formátum: `Axxxxxxxxx/yyyy/zzzzz` (AP-szám / zárás száma / napi
nyugtaszám). **Mindkét generációban a bizonylat sorszáma az ESZKÖZBEN képződik,
helyben.**

**Forrás:** [8/2025. (III. 31.) NGM rendelet](https://net.jogtar.hu/jogszabaly?docid=a2500008.ngm).

### Következmény

**Az `A2` (szerver-autoritatív + csökkentett gyorseladás) és az `A2/a` alatt
maradhat.** A premissza a jövőbeli eszközgenerációra bizonyítottan igaz, és a
jelenlegire a formátum szerkezete ugyanezt mutatja.

**`[ ]` Ami MÉG HIÁNYZIK a teljes igazoláshoz:** a **mai** AEE-s eszközökre
vonatkozó gyártói protokolldokumentáció (`E3` beszerzési tétel). A rendelet a
**jövőbeli** eszközt szabályozza; a mait a régi pénztárgép-rendelet és a
gyártói protokoll. **A premissza tehát ERŐSEN alátámasztott, de a mai
eszközökre még nem teljesen zárt.**

---

## `[!] L3 — ÚJ, EDDIG NEM ISMERT KORLÁT: az offline működés 72 ÓRÁRA korlátozott`

### A tény

A **8/2025. (III. 31.) NGM rendelet** 2. melléklet B) rész 16–18. pontja szerint:

- **„A hardveralapú e-pénztárgép alkalmas offline működésre, a felhőalapú
  e-pénztárgép NEM alkalmas offline működésre."**
- **„Az offline működés időtartama nem haladhatja meg a hetvenkettő órát."** (72 óra)
- Offline alatt az e-nyugtákat tárolni kell, és a kapcsolat visszatérése után
  **„haladéktalanul szükséges elküldeni"**.

**Forrás:** [8/2025. (III. 31.) NGM rendelet](https://net.jogtar.hu/jogszabaly?docid=a2500008.ngm).

### Miért ez a második legsúlyosabb lelet

**Két dolgot mond ki, amit a terv sehol nem tud:**

**(1) A felhőalapú e-pénztárgép offline NEM működik.** Ha a Siduri valaha
felhőalapú e-pénztárgép irányba menne, **az offline-first USP (a spec 1. pontja,
a termék egész eladási érve) MEGSZŰNIK.** → **Az átállásnál kizárólag
HARDVERALAPÚ e-pénztárgép jöhet szóba.** Ez most egy mondat a tervben; később
egy rossz beszállítói döntés.

**(2) A 72 órás plafon ütközik a terv több számával.** A terv jelenlegi
offline-feltevései:
- **10 napos licenc-türelmi idő** (spec 19.),
- **20 forgalmas napnyi kliens-archívum** (`B10/b`),
- „a hely offline is működik" — időkorlát megjelölése nélkül.

**A jövőbeli eszközgenerációnál a fiskális eszköz maga nem tűr 72 óránál többet.**
Tehát a „tetszőleges ideig offline" ígéret **a fiskális rétegen megbukik**, akkor
is, ha a Siduri szoftvere elvben elbírná.

### `[ ]` Amit javaslok

1. **A 72 órát fel kell venni ELSŐRANGÚ KORLÁTKÉNT** az offline-tervezésbe —
   nem a szoftver korlátja, hanem a jogszabályé.
2. **A `D6` (licenc-lejárat) 10 napos türelmi ideje FELÜLVIZSGÁLANDÓ ennek
   fényében.** Nem ütközik közvetlenül (más dolgot mér), de **a felhasználó
   felé kommunikált „meddig működünk offline" üzenetnek EGYETLEN, a
   legszigorúbb korlátot kell mondania**, nem hármat.
3. **`[!]` A csökkentett mód UI-jának ki kell írnia az offline időt** és
   figyelmeztetnie a közelgő korlátra — ugyanaz az elv, mint a 18 órás
   NTAK-riasztásnál.
4. **`[ ]` Ellenőrizendő:** a MAI online pénztárgépekre van-e hasonló offline
   plafon? A rendelet a jövőbeli eszközt szabályozza. **Ez a gyártói
   protokolldokumentációból (`E3`) derül ki** — és ha van, az **AZONNAL**
   érinti az MVP-t, nem csak 2028-at.

---

## `L4 — Az NTAK határidő: a terv olvasata PONTATLAN volt (enyhébb a valóság)`

### A tény

A **235/2019. (X. 15.) Korm. rendelet**:
- **8/A. § (6):** *„a vendéglátó szoftver automatikusan küldi… a tárgynapot
  követő 24 órán belül a tárgynapra vonatkozóan a napi adatszolgáltatás körébe
  tartozó… statisztikai jellegű adatokat"*
- **8/A. § (9):** *„Ha az adatszolgáltatás üzemzavar vagy üzemszünet miatt
  meghiúsul, az adatszolgáltatást az üzemzavar vagy üzemszünet elhárultát
  követő napon teljesíteni kell."*

**Forrás:** [235/2019. (X. 15.) Korm. rendelet](https://net.jogtar.hu/jogszabaly?docid=a1900235.kor),
[NTAK információs oldal](https://info.ntak.hu/adatszolgaltatas).

### Mit igazol és mit cáfol ez a `C11` premisszából

| A terv állítása | Ítélet |
|---|---|
| Van 24 órás adatszolgáltatási szabály | **IGAZOLT** — de „a **tárgynapot követő** 24 órán belül", nem „bármikori 24 órás visszaszámláló" |
| 18 óra offline után **jogsértés fenyeget** | **PONTATLAN** — üzemzavar esetén a határidő **az elhárulást KÖVETŐ NAP**, nem a 24. óra |

### Következmény a spec 19. pontjára (18 órás riasztás)

**A riasztás megtartandó, de az INDOKLÁSA és a SZÖVEGE hibás.**
Nem az van, hogy 24 óra offline = jogsértés. Az van, hogy **az üzemzavar
elhárulását követő napon pótolni kell** — ami sokkal engedékenyebb.

**Amit ez jelent:**
- **A riasztás NEM jogi visszaszámláló**, hanem **üzemeltetési figyelmeztetés**:
  „adatszolgáltatási hátralék halmozódik". Ez így is hasznos, sőt kell.
- **A szöveg viszont ne állítson jogsértést**, mert az **hamis jogi állítás
  lenne a végfelhasználó felé** (§13.5, és §5: a felület ne állítson olyat,
  ami nem igaz).
- **`[!]` És van egy ELLENKEZŐ IRÁNYÚ kockázat, amit a terv nem lát:** a valódi
  kötelezettség **az elhárulást követő napon** áll be — tehát ha a kapcsolat
  helyreáll, **a pótlásnak MEG KELL TÖRTÉNNIE**, nem elég, hogy „majd a
  sorbaállító elviszi". **Pozitív visszaigazolás kell rá** (§5), és ha a pótlás
  nem sikerült, **azt hangosan jelezni kell.**

---

## `L5 — Bizonylat-sorszámozás: az eszközönkénti tartomány VALÓSZÍNŰLEG megfelel`

### A tény

A **2000. évi C. törvény (számviteli törvény) 167. §** a bizonylat kötelező
alaki és tartalmi kellékei között ezt írja: **„a bizonylat megnevezése,
sorszáma, vagy egyéb más azonosítója"**.

A **168. §** szerint a nyugta és a számla **szigorú számadás alá tartozik**, és
a kibocsátónak **olyan nyilvántartást kell vezetnie, amely biztosítja azok
elszámoltatását**.

**Forrás:** [2000. évi C. törvény](https://net.jogtar.hu/jogszabaly?docid=a0000100.tv),
[Bizonylat — összefoglaló](https://hu.wikipedia.org/wiki/Bizonylat),
[Adó Online — Bizonylati elv, bizonylati fegyelem](https://ado.hu/szamvitel/bizonylati-elv-bizonylati-fegyelem/).

### Ítélet a `B14.5` nyitott jogi kérdésre

A `B14.5` azt kérdezte: megfelel-e a **több párhuzamos, eszközönkénti
számtartomány** a folyamatos sorszámozás követelményének?

**A törvény szövege „sorszáma, VAGY EGYÉB MÁS AZONOSÍTÓJA"-t mond** — tehát
**nem ír elő egyetlen, globális, folytonos sorozatot**; azonosíthatóságot ír elő.
A 168. § pedig **elszámoltathatóságot** követel, amit **előre elhatárolt,
nyilvántartott tartományok teljesítenek** — pontosan ez a `B14` séma.

### `[?]` DE — a bizalmi szintet ki kell mondani

- A **167–168. § szövegét másodlagos forrásokból** olvastam; a `net.jogtar.hu`
  teljes szövegét a hosszúsága miatt **nem tudtam a §-ig letölteni**. A
  megfogalmazás több független forrásban azonos, de **ez nem elsődleges idézet.**
- **Ez a kérdés a felhasználó könyvelőjének / adótanácsadójának egy mondatos
  megerősítésével lezárható**, és **így is javaslom lezárni** — nem azért, mert
  valószínűleg rossz, hanem mert **a hibás válasz ára az adatmodell átírása.**
- A **jogi bizonylat sorszámát amúgy is az adóügyi eszköz adja** (`L2`), tehát
  a mi számunk **belső azonosító** — ez tovább erősíti a megfelelést. **A kockázat
  ott van, ahol a Siduri MAGA a kiállító** (pl. saját számla, belső bizonylatok).

---

## `L6 — Megőrzési idő: 8 év — az A3 tétel EZZEL ELDÖNTHETŐ`

### A tény

A **2000. évi C. törvény 169. §** szerint a beszámolót és az azt alátámasztó
dokumentumokat, valamint **a könyvviteli elszámolást közvetlenül és közvetetten
alátámasztó számviteli bizonylatot legalább 8 évig** kell **olvasható formában,
a könyvelési feljegyzések hivatkozása alapján visszakereshető módon** megőrizni.

**Forrás:** [2000. évi C. törvény](https://net.jogtar.hu/jogszabaly?docid=a0000100.tv),
[Adó Online — Az iratőrzési kötelezettség](https://ado.hu/szamvitel/az-iratorzesi-kotelezettseg/),
[Adózóna — Számlák az irattárban](https://adozona.hu/adozas_rendje/Szamlak_az_irattarban__megorzesi_ido_selejt_BBD9JO).

### Ítélet az `A3` tételre (30 napos purge)

**Az `A3` aggály MEGALAPOZOTT.** A spec 2. pontja szerint a lokális szerver
**30 nap után törli** a felszinkronizált nyugtákat és eseménynaplót. A megőrzési
kötelezettség **8 év**.

**Ebből következik, amit az `A3` már sejtett:**

> **Ha a rendszer 30 nap után helyben törli a bizonylatokat, akkor a
> „tisztán lokális" topológia (spec 4.) NEM megfelelő önmagában** — mert nem
> marad hol a 8 évet teljesíteni. **A felhő (vagy más archívum) ekkor nem
> opcionális kényelem, hanem a megfelelés feltétele.**

### `[ ]` Amit el kell dönteni (a felhasználónak)

Három út, mindegyik vállalható, de **választani kell**:
1. **A felhő a jogi archívum** → a „tisztán lokális" topológiát vagy elvetjük,
   vagy csak olyan ügyfélnek adjuk, aki maga oldja meg az archiválást.
2. **Helyi hosszú távú archívum** (NAS, külső adathordozó, rendszeres export) →
   a purge marad, de az archiválás **kötelező telepítési elem**, nem opció.
3. **Nincs purge** → a 64 GB-os SSD-vel ez **mérendő**, nem feltételezhető
   (`MERESEK.md`).

**`[!]` Bármelyik is lesz: a purge SOHA nem törölhet olyat, aminek a
megőrzéséről nincs POZITÍV bizonyíték** (§5) — nem elég, hogy „felment a
felhőbe", igazoltan meg kell lennie ott.

---

## `L7 — Elviteles ÁFA: a „automata ÁFA-váltás" NEM egyszerű kapcsoló`

### A tény

A helyben fogyasztás **szolgáltatásnyújtás** (kedvezményes kulcs), az elvitel és
a kiszállítás **termékértékesítés** (általános kulcs). **A besorolás a vevő
fogyasztási szándékán múlik.**

**És ami a terv szempontjából fontos: az italoknál nem egységes.** A kedvezményes
kulcs a **helyben készített** italokra vonatkozik (kávé, tea, frissen facsart lé,
gépi üdítő); a **palackozott üdítő, ásványvíz és az alkoholos italok**
a magasabb kulcs alá esnek **helyben fogyasztás esetén is**.

Külön eset: ha a vendég **helyben fogyaszt, majd a maradékot elviteti**,
az a becsomagolt maradék **továbbra is az éttermi szolgáltatás része.**

**Forrás:** [NAV — Mikor alkalmazható a kedvezményes áfakulcs az étkezőhelyi vendéglátásban?](https://nav.gov.hu/print/ugyfeliranytu/nezzen-utana/tudjon_rola/Mikor_alkalmazhato_a_kedvezmenyes_afakulcs_az_etkezohelyi_vendeglatasban_),
[Adó Online — Kedvezményes áfakulcs az étkezőhelyi vendéglátásban](https://ado.hu/ado/kedvezmenyes-afakulcs-az-etkezohelyi-vendeglatasban/).

### Ítélet a spec 9. pontjára („Automata ÁFA-váltás")

A spec így fogalmaz: *„a rendszer a háttérben automatikusan módosítja a helyben
fogyasztott ÁFA-kulcsot elvitelesre"*, az angol változat pedig konkrét példát ad:
*„from local 5% to takeaway 27%"*.

**Ez a megfogalmazás egy SZÁMÍTÁST sugall, és az hibás lenne.** A helyes modell
**keresés, nem váltás**:

> **Minden terméknek KÉT, egymástól függetlenül megadott adókulcsa van** —
> egy helyben fogyasztásra, egy elvitelre —, és **mindkettő dátumozott**
> (§13.3). Az „elviteles = 27%" **nem szabály, hanem a leggyakoribb adat.**

**Miért nem mindegy:** egy sörnél **mindkét kulcs azonos** — ott nincs „váltás".
Ha a kód „elvitelnél emeld a kulcsot"-ként valósul meg, az **egy egész
termékosztályon hibázik**, és **csendben** — a nyugta szabályosnak látszik.

**`[!]` És a spec „a bruttó árat fixen tartva" kikötése ezzel együtt
veszélyes:** ha a kulcs nem változik, nincs mit fixen tartani; ha változik,
a nettó ár változik. **A `C3` alatt nyitva hagyott termékdöntés (bruttó vagy
nettó marad fix) ezért CSAK azokra a termékekre értelmes, ahol a két kulcs
tényleg eltér.** Ezt a szabályt ki kell mondani.

---

## `L8 — Amit NEM ellenőriztem (kimondva, §11: ne legyen néma plafon)`

Ez a kör **nem** terjedt ki az alábbiakra. Nem azért, mert rendben vannak, hanem
mert nem néztem meg — **ezek a 2. körben vagy külön veendők elő:**

- **5 Ft-os kerekítés** pontos szabálya és hatálya (spec 13.) — **nem ellenőriztem.**
- **A sztornó/visszáru** konkrét jogi és protokoll-szabályai (`C10`) — a gyártói
  protokoll nélkül nem is ellenőrizhető.
- **GDPR** részletei: adatfeldolgozói szerződés tartalma, tájékoztatási
  kötelezettség, törlési igény kezelése (`B7`, `B10/a`, `F7/b`).
- **A kockázatvállalási nyilatkozat** (`B12`) jogi ereje — érintőképernyős
  aláírás **nem** minősített elektronikus aláírás; hogy a felelősségkorlátozáshoz
  elég-e, **nem ellenőriztem.**
- **Munkaidő-nyilvántartás** (`C8`) jogszabályi követelményei.
- **Az NTAK adattartalma és sémaverziója** (`C11` másik fele) — regisztráció
  nélkül nem hozzáférhető.
- **A hazai pénztárgép-rendelet (mai eszközök)** — csak az ÚJ, e-pénztárgépes
  rendeletet olvastam.

---

# II. RÉSZ — TELJESSÉGI ELLENŐRZÉS

## T1 — Ami MOST derült ki, hogy hiányzik a tervből

### `[!] T1.1 — Nincs semmi az ÜZLETI NAP és a MŰSZAK pontos modelljéről`

A terv **négy** különböző napfogalmat használ, és **egyik sincs definiálva**:
1. a **logikai üzleti nap** (pl. 04:00–04:00) — az `F4` említi,
2. az **adóügyi eszköz munkanapja** (a bizonylatszámban: `yyyy`),
3. az **NTAK tárgynap** (`L4` szerint jogszabályi fogalom),
4. a **naptári nap** (a riportokban, a megőrzésnél).

**A `B14.4` döntés óta ez SÚLYOSABB, mint volt:** az üzleti nap dátuma
**bekerül a bizonylatszámba**, tehát a fogalom **elrontása bizonylatszámot ront
el**, ami nem javítható. **Kell egy nevesített, egyetlen definíció**, és a többi
fogalommal való leképezés **kiírva** — nem kikövetkeztetve.

### `[!] T1.2 — A pénztárgép-műszak és a személyzet MUNKAIDEJE összekeveredhet`

A `C8` jelzi, hogy nincs munkaidő-nyilvántartás. **Amit nem jelez:** a műszak
(14.) **kasszához kötött**, a munkaidő **emberhez**. Egy pincér **több
műszakban** is dolgozhat, és egy műszakot **több ember** is használhat.
Ha ez a két fogalom egy táblába kerül, **később nem lehet szétszedni.**

### `[ ] T1.3 — Sehol nincs szó a RENDELÉS ÉLETCIKLUSÁRÓL a konyha felé`

A KDS (23.) és a nyomtatás (11.) meg van említve, de **nincs állapotgép** arra,
hogy egy tétel mikor „elküldött", „készül", „kész", „kiadva", és **mi történik,
ha egy elküldött tételt sztornóznak.** A spec 9. pontja említ „védett" tételeket
(amit konyhai nyomtatás után nem lehet módosítani) — **ez implicit állapotgép,
kiírva nincs.**

### `[ ] T1.4 — Nincs szó a TÖBBSZINTŰ receptúráról a készletlevonás szempontjából`

A `C1` említi a többszintű BOM-ot mint hiányt. **Amit hozzáteszek:** ha egy
koktél félkész alapanyagot használ (pl. házi szirup), akkor **az eladás
pillanatában mit vonunk le** — a szirupot vagy az összetevőit? És **mikor**
készül a szirup (gyártási mozgás)? **Ez a mozgó átlagár számítását is érinti**
(spec 15., 25.), tehát az árrés-riport pontosságát.

### `[ ] T1.5 — Hiányzik: mi történik egy TERMÉK TÖRLÉSEKOR?`

Egy termék, amit már eladtak, **nem törölhető** — a régi bizonylatok hivatkoznak
rá. Kell **inaktiválás** (nem látszik, de a történet megmarad) és **explicit
szabály**, hogy a törlés tilos. Ez triviálisnak tűnik, és **pontosan ezért
szokott kimaradni**, aztán a riport üres nevekkel tele.

### `[ ] T1.6 — Nincs ÁRVÁLTOZÁS-TÖRTÉNET`

A `C2` említi az ár-verziózást mint hiányt. **Ami ehhez kell, és nincs kimondva:**
a bizonylatnak **az eladáskori árat és adókulcsot kell tárolnia**, nem
hivatkozást a termékre. Enélkül egy áremelés **visszamenőleg átírja a régi
riportokat** — és a `B16` (felhőből zárolt ár) után ez **még valószínűbb**,
mert az árat távolról is átírhatják.

### `[ ] T1.7 — A `siduri-updater` szerepe most már TÖBB, mint patcher`

A `B1/b` alatti 4. következmény kimondta: a frissítőnek **ismernie kell a
szerver-szerepeket** és sorrendben kell dolgoznia. **Ez a repó eredeti
leírásában nincs benne** (a superprompt szerint: „standalone offline patcher
utility overcoming Windows file lock issues"). **A leírását frissíteni kell**,
különben a repó gazdája a szűkebb feladatot fogja megvalósítani.

### `[ ] T1.8 — Nincs szó arról, hogyan indul el egy ÚJ TELEPHELY`

A `D2` a telepítést említi, de **nem az adatokkal való feltöltést**: honnan jön
az első terméklista, ÁFA-tábla, jogosultsági szintek? **Sablonból? Importból?
Egy másik telephelyről másolva** (ez lánc esetén kézenfekvő)? Ez **értékesítési
sebesség kérdése is** — ha egy telepítés két nap adatrögzítés, az drága.

## T2 — Ötletek, amiket a tervbe illőnek tartok (nem kértétek, de javaslom)

### `[JAVASLAT] T2.1 — „Miért nem működik?" gomb a POS-on`

Az `F5` (támogathatóság) tétel megoldásának legolcsóbb 20%-a: egy gomb, ami
**egy képernyőn** megmutatja az összes releváns állapotot (szerverkapcsolat,
utolsó sikeres szinkron, adóügyi eszköz, nyomtatók, internet, licenc,
adatszolgáltatási hátralék). **Ez ugyanaz az adathalmaz, amit a `B11.3/b`
öndiagnosztikai létra amúgy is összegyűjt** — csak mindig elérhetővé téve.
Majdnem ingyen van, és péntek este ez a különbség egy 5 perces és egy 45 perces
hívás között.

### `[JAVASLAT] T2.2 — „Csak olvasható" szerviz-mód`

Az `F7/b` szerviz-belépés **teljes jogú**. Sok támogatási eset viszont csak
*megnézést* igényel. Egy **olvasás-only szerviz-munkamenet** külön jogosultsággal
azt jelenti, hogy a hívások többsége **nem igényel írási hozzáférést az ügyfél
adataihoz** — ami az `F7/b` alatt kimondott adatvédelmi aggály legjobb enyhítése,
és értékesítési érv is.

### `[JAVASLAT] T2.3 — A bizonylat-újranyomtatás mint önálló, naplózott művelet`

Sehol nem szerepel, pedig **naponta használt funkció**, és **visszaélési
felület** (egy „másolat" nyugta odaadható másik vendégnek). Kell rá: külön
jogosultság, **feltűnő MÁSOLAT jelölés a papíron**, és **naplózás**.

### `[JAVASLAT] T2.4 — Terv a NULLADIK ügyfélre`

Az `E1` rögzíti: nincs névre szóló első fizető ügyfél. **Javaslom, hogy a
fázistervben legyen egy nevesített „nulladik telepítés"** — akár egy baráti hely,
akár egy szimulált üzem —, aminek **egyetlen célja a `MERESEK.md` teljes
lefuttatása** éles körülmények között, fizető ügyfél kockázata nélkül.
Ez a felhasználó „az első éles teszten mindent mérjünk" utasításának a
végrehajtható formája.

## T3 — Amit ELLENŐRIZTEM és RENDBEN VAN (§11: a negatív eredményt is le kell írni)

- **A `NYITOTT_KERDESEK.md` az egyetlen döntési igazságforrás**, és a többi fájl
  fejlécében ki van írva, hogy mutató. **A §2.4 szabály teljesül.**
- **Minden ebben a munkamenetben hozott döntés mellett ott az INDOKLÁS**, és
  ahol az ajánlással szemben született, ott ez **külön ki van mondva**. Egy
  következő kör nem fogja újratárgyalni őket tájékozatlanul.
- **A visszavont saját érveim** (az adóügyi szám ütközése; a tartomány
  kimerülése; a rendezés) **áthúzva bent maradtak**, nem törölve — a §12
  szabálya („ha a saját javításod hibás volt, azt is írd bele") teljesül.
- **A `MERESEK.md` minden teljesítmény-állítást összegyűjt**, és sehol a tervben
  nincs mérés nélküli szám. **§4 teljesül.**
- **A `gemini_cloud_spec_en.md` bemenetként, összevetéssel került be** — a
  felülírt pontja meg van jelölve, tehát nem fog doksi-driftet okozni.

---

# III. RÉSZ — ÖSSZEGZÉS ÉS AMIT KÉREK

## A négy lelet, ami DÖNTÉST igényel

| # | Lelet | Miért sürgős |
|---|-------|--------------|
| **1** | **2028. július 1. — az online pénztárgépek kifutnak** | A fiskális réteg lejárati dátuma a termék élettartamán belül van. A `C12` kezelése hibás: nem „stratégiai kérdés", hanem dátumozott kötelezettség. |
| **2** | **72 órás offline plafon** (e-pénztárgépnél), és **a felhőalapú offline egyáltalán nem működik** | Az offline-first USP-t korlátozza. Ellenőrizendő, hogy a MAI eszközökre van-e hasonló — ha igen, az MVP-t is érinti. |
| **3** | **Megőrzés 8 év vs. 30 napos purge** | A „tisztán lokális" topológia így nem megfelelő önmagában. Három út közül választani kell. |
| **4** | **Az elviteles ÁFA nem „váltás", hanem termékenkénti KÉT kulcs** | Ha számításként épül meg, egy egész termékosztályon (italok) csendben hibázik. |

## A jó hír

**Az `A2` teherhordó premisszája — hogy az adóügyi eszköz maga sorszámozza a
bizonylatot — IGAZOLVA van** a jövőbeli eszközgenerációra, és a maira a formátum
szerkezete ugyanezt mutatja. **Ez volt az egyetlen olyan tétel, ahol már meghozott
döntés állt igazolatlan premisszán.** A csökkentett mód alatt marad a talaj.

**És a `B14` eszközönkénti számozás valószínűleg jogilag is rendben van** —
a törvény „sorszáma, **vagy egyéb más azonosítója**"-t mond, nem egyetlen
globális sorozatot.

## Amit kérek a folytatáshoz

1. **`[ ]` Döntés a négy leletről** (fent).
2. **`[ ]` Egy mondat a könyvelőtől/adótanácsadótól** a `L5` (eszközönkénti
   számozás) és a `L6` (megőrzés) tárgyában — nem azért, mert valószínűleg
   rossz, hanem mert **a hibás válasz ára az adatmodell átírása.**
3. **`[ ]` A gyártói protokolldokumentáció beszerzésének elindítása** (`E3`) —
   ez blokkolja a `C10`, `F3` és a `L3` alatti „mai eszközök offline plafonja"
   kérdést, és **hetekig tarthat.**
