# Siduri — Nyitott kérdések és specifikációs hiányok

> **Státusz:** nyitott, kódolás előtti tisztázásra vár.
> **Forrás:** `siduri_spec_hu.md` + `siduri_superprompt_en.md` átolvasása (2026-08-22).
> **Utolsó frissítés:** 2026-08-22 (2. munkamenet) — ÚJ döntések: B1/a (HA az MVP-ben marad),
> B1/b (a tartalék is J1900 → aszinkron a munkafeltevés), A2/b (a degradált mód mindhárom
> része az MVP-ben). Korábbról: A1, A2, A2/a, B3, E2 eldöntve; F) szakasz felvéve.
> **ÚJ (ugyanaznap, később):** B1/c eldöntve — kétlépcsős failover (gép ellenőriz, ember dönt).
> **ÚJ (ugyanaznap, harmadik kör):** A4 eldöntve — automatikus visszaállás 1 perc stabil
> kölcsönös láthatóság után; tiszta vs. kemény átvétel külön útvonal; minden gép önállóan
> megy csökkentett módba. Kimondva egy ÜTKÖZÉS: „automatikus visszaállás” + „nulla
> adatvesztés” teljes automatizmussal nem teljesíthető együtt — a kimentés automatikus,
> a könyvelés nem lehet az.
> **ÚJ (negyedik kör):** A4/b (billegés-védelem: növekvő várakozás + leállási határ),
> A4/c (azonnali szerepcsere), a személyzeti üzenetek jóváhagyva, és ÚJ tétel: **B9**
> — telepítési méretosztályok, ahol az egygépes helyen a pénztárgép maga a szerver.
> **ÚJ (ötödik kör):** B9/b tisztázva — a gépszám-szabály a TARTALÉK SZERVERRE vonatkozik
> (2–3 gépnél opcionális, 4+ gépnél kötelező). ÚJ tétel: **B10** — kliens-oldali
> tranzakció-archívum (az adatmennyiség nem akadály; az adatvédelem, a megőrzési idő és
> az írásterhelés az).
> **ÚJ (hatodik kör):** B10/a, B10/b, B10/c eldöntve. Kiemelt: **a szerver jellemzően egy
> dolgozó pénztárgép lesz**, nem irodai gép — ez átrendezi az adatvédelmi képet és a
> teljesítménymérés súlyát. Megőrzés: **20 FORGALMAS nap**. Új fájl: **`MERESEK.md`**.
> **NYITVA maradt:** a B1/b ellentmondása (dedikált-e a tartalék gép), van-e TPM a bázison,
> az R1 lépcsőnkénti alakjának jóváhagyása, a B1/c R2–R5 kitöltése, majd E1 (fázisterv).
> **Ez az EGY igazságforrás a nyitott döntésekre** (MERNOKISAROKKOVEK §2.4).
> Ha egy tétel eldől, ITT jelöld `[ELDÖNTVE — <döntés>]`-ként, ne máshol.
>
> **Jelölések:**
> `[ ]` nyitott · `[?]` igazolatlan premisszán alapul, ellenőrizni kell (§13.5) ·
> `[ELDÖNTVE]` lezárva.
>
> **FIGYELEM — doksi-drift (§2.4):** az eldöntött tételek egy része **változtatást
> ír elő a két spec-fájlban** (pl. A1 → a Linux-említés törlése). Amíg ezek nem
> futnak át, a specek ellentmondanak ennek a fájlnak. Az elvégzendők az adott
> tételnél „Következmény — elvégzendő" címszó alatt szerepelnek.

---

## A) Ellentmondások a két dokumentum között / önmagában

### `[ELDÖNTVE — WPF, Windows 10 IoT Enterprise LTSC only]` A1 — WPF ≠ Linux
Mindkét doksi azt írja, a POS kliens „Windows 10/11 **vagy** Linux" (HU 2., EN 2.),
a stack viszont WPF. **WPF nem fut Linuxon.** Vagy elesik a Linux, vagy **Avalonia
UI**-ra váltunk (XAML-alapú, WPF-hez nagyon közeli, cross-platform).

**Döntés (2026-08-22):** nem lesz Linuxos POS. A célplatform **Windows 10 IoT
Enterprise (LTSC)**, kizárólag. Marad a **WPF** — kitaposottabb a másodkijelző, a
kioszk mód és az érintéskezelés terén, mint az Avalonia.

**Következmény — elvégzendő:** a Linux-említést ki kell venni **mindkét specből**
(`siduri_spec_hu.md` 2., `siduri_superprompt_en.md` 2.), különben a doksi-drift
(§2.4) a következő kört egy nem létező platformtámogatás tervezésére küldi.

**Következmény — a .NET verzióra:** a spec „modern .NET 8+"-t ír. Windows 10 IoT
Enterprise LTSC-n ez működik, de a **konkrét LTSC build** és a `.NET Desktop
Runtime` telepíthetősége telepítési (D2) tétel, nem fejlesztési — rögzíteni kell,
melyik LTSC kiadásra célzunk.

### `[ELDÖNTVE — szerver-autoritatív + degradált gyorseladás]` A2 — Vastagkliens lokális PostgreSQL replikával
**A két dokumentum ellentmond egymásnak:**
- HU 17.: „Vastagkliensek: AIO PC-k **helyi PostgreSQL replikával**."
- EN 17.: csak az **Emergency Server** replikál; a POS kliensekről nincs szó.

Két teljesen különböző architektúra:
- **Ha a POS csak olvas a replikából** → mire jó? A UI-hoz elég egy in-memory cache.
- **Ha a POS a szerver halála után önállóan tud eladni** → az multi-master,
  konfliktusfeloldással, saját bizonylat-sorszám-tartománnyal.

**Ez a projekt legdrágább egyetlen döntése** — meghatározza az adatmodellt, a
szinkronizációt, a sorszámozást és a fiskális folyamatot.

---

**Döntés (2026-08-22) — az ÜZLETI követelmény felől:**
Ha a Master ÉS az Emergency Server is halott, a POS-nak **gyorseladást nyugtával**
kell tudnia — **asztalkezelés nélkül**.

Ebből következő architektúra: **szerver-autoritatív minden megosztott állapotra +
szigorúan szűkített degradált mód a vastagkliensen.**

- **Normál üzem:** minden megosztott állapot (asztalok, rendelések, készlet,
  kedvezmények, műszak) a szerveren dől el. A POS-on **cache** van, **nem**
  PostgreSQL replika.
- **Degradált üzem:** tétel → fizetés → nyomtatás, és a történtek egy lokális,
  **tartós, append-only outboxba** kerülnek, amit visszatéréskor lejátszunk.

**Miért ez, és miért NEM multi-master:** a multi-master költsége abból fakad, hogy
**megosztott, módosítható állapoton** kell konfliktust feloldani. A degradált
gyorseladásban nincs ilyen állapot — csak egyirányú eseményfolyam. A
konfliktusfeloldás problémája így nem megoldódik, hanem **nem keletkezik**.

**A `siduri_spec_hu.md` 17. pontja ezzel ELLENTMOND ennek a döntésnek**
(„helyi PostgreSQL replikával"). §2.4 szerint javítandó, különben a következő kör
egy nem létező architektúrát fog tervezni.

#### `[ELDÖNTVE — nem elérhetők, kézi újrafelütés]` A2/a — a NYITOTT asztalok a kiesés pillanatában
**Ez a döntés éle volt.** A nyitott rendelések a halott szerveren vannak, a
vendégek viszont ott ülnek és fizetni akarnak.

**Döntés (2026-08-22):** ha a Master kiesik **és az Emergency Server sem lép be
(vagy az is kiesik)**, a nyitott asztalok **nem elérhetők**. A pincér a
fogyasztást kézzel, gyorseladásként üti fel újra.

**Miért ez a helyes, a kényelmetlensége ellenére:** ez tartja meg a **„nincs
megosztott módosítható állapot"** invariánst, amire az egész A2 döntés épül. Ha a
POS cache-elhetné és lezárhatná a nyitott asztalokat, azzal visszajönne a
konfliktusfeloldás problémája (két POS ugyanazt az asztalt zárja le → dupla
nyugta), csak kisebb és alattomosabb felületen. A cserearány rossz: kényelmet
kapnánk egy olyan hibaosztályért, ami pénzügyi bizonylatot érint.

**Fontos, hogy ez a normál üzemben SOHA nem fordul elő:** ez a kettős
meghibásodás ága. Emergency Server működése mellett az asztalok elérhetők
maradnak — a kézi újrafelütés a legvégső tartalék.

**Következmény — elvégzendő:**
- A degradált módra váltáskor a UI **mondja meg explicit**, hogy a nyitott
  asztalok nem elérhetők, és mit kell tenni helyette (§5: a felület ne kínáljon
  olyat, ami nem működik — itt: ne úgy tegyen, mintha az asztalok ott lennének).
- **A proforma (7.) itt kap váratlan szerepet:** ha a pincér korábban nyomtatott
  előnyugtát, az a papír az egyetlen megmaradt nyoma a fogyasztásnak. Ezt az
  üzemeltetési dokumentációban ki kell mondani.
- Visszatéréskor a szerveren **ott maradnak a nyitott asztalok** a kiesés
  pillanatának állapotával, miközben a fogyasztás időközben gyorseladásként
  kiment. Ezeket **rendezni kell** (kézi lezárás indoklással), különben örökre
  nyitva lógnak és hamisítják a riportokat. Ez az A2 4. pontjának
  (reconciliation) része.

#### `[ELDÖNTVE — a degradált mód TELJES EGÉSZÉBEN az MVP-ben van]` A2/b — ütemezés

**Döntés (2026-08-22, 2. munkamenet):** a degradált gyorseladás mindhárom része az
MVP-be kerül, akkor is, hogy közben a vészhelyzeti szerver (B1/a) is az MVP-ben van:

1. **helyi tartós napló a pénztárgépen** (append-only outbox) — a pénztárgép a
   szerver nélkül is tud eladni, és az eseményeket kiírja magának;
2. **degradált felület** — a pénztáros LÁTJA, hogy korlátozott módban van, és ami
   nem működik, az láthatóan tiltva van (nem némán bukik el);
3. **visszatéréskori egyeztetés** (reconciliation) — a szerver visszatérésekor a
   helyi napló lejátszása, sorrenden kívüli és múltbeli időbélyegű eseményekkel.

**Miért kellett ezt külön eldönteni:** mert a vészhelyzeti szerver ugyanazt a bajt
(a fő szerver kiesését) már lefedi, tehát felmerült, hogy a degradált mód
megvalósítása halasztható, és MVP-ben elég lenne csak az, ami utólag drága
(idempotencia-kulcs minden írásra, szerver-autoritatív modell). A felhasználó a
**kétszeres védelmet** választotta.

**Amit ez ÁRAZ (a fázistervben, E1, be kell írni):** a 3. pont, a
visszatéréskori egyeztetés, **az MVP legkockázatosabb egyetlen darabja** — nem a
kódmennyiség miatt, hanem mert egy incidens után három helyen lesz adat, ami nincs
mind ugyanott (a halott master lemeze, a tartalék szerver adatbázisa, és a
pénztárgépek helyi naplói). Lásd a B1/c alatti „három igazságforrás" bekezdést.
Ehhez §1 szerint őr és §D5 szerint szimulátor kell — kézzel nem reprodukálható.

#### Amit ez a döntés maga után von (elvégzendő a tervben)
1. **Lokális tartós tár a POS-on** (nem PG replika). Mit cache-elünk: törzsadat,
   árak, ÁFA-szabályok (dátumozva, §13.3), jogosultságok, PIN-hash-ek,
   nyomtató-routing.
2. **Cache-elévülési politika.** Elavult áron eladni valós kockázat. Ki kell
   mondani: hány órás cache-ből szabad még eladni, és mi történik utána. A
   „megjelenített szöveg nem állapot" (§8) itt is él: explicit korjelző kell.
3. **Az outbox-lejátszás idempotens legyen** (F1). Kezelnie kell azt is, hogy a
   szerver egyes eseményeket még a halála ELŐTT megkapott.
4. **Visszatéréskori egyeztetés (reconciliation).** A szerver múltbeli
   időbélyegű, sorrenden kívüli eseményeket kap több POS-tól. A készlet
   negatívba mehet; az üzleti nap / műszak határa átléphetett a kiesés alatt.
   Ez valódi munka, a fázistervben nevesíteni kell.
5. **A módváltás küszöbe.** Honnan tudja a POS, hogy a szerver tényleg halott, és
   nem csak 3 másodpercig akadt a wifi? Túl korán vált → felesleges degradáció;
   túl későn → a pénztáros áll. Explicit küszöb + **kézi felülbírálás** +
   feltűnő UI-állapot kell.
6. **Ami degradált módban nem megy, azt LÁTHATÓAN tiltsuk le**, ne némán bukjon
   el (§5: „a felület ne kínáljon olyat, ami nem működik").
7. **NTAK és riportok:** a degradált módban kelt eladásoknak is el kell jutniuk
   az NTAK-ba — ugyanaz az outbox-minta (B2).

#### `[?]` Teherhordó, IGAZOLATLAN premissza (§2.2, §13.5)
Az egész degradált mód arra épül, hogy **AEE-s pénztárgépnél a jogi bizonylatot
maga az adóügyi eszköz állítja ki és sorszámozza**, tehát a Siduri szerver kiesése
nem akadálya a szabályos nyugtaadásnak — sem technikailag, sem jogilag.

**Ez NINCS forrásból igazolva.** Ha nem igaz, ez a döntés megdől, és vissza kell
térni a „(b) semmi — a hely megáll" ághoz. **Kódolás előtt igazolandó.**
Kapcsolódik: C10, C11, F3.

### `[?]` A3 — 30 napos purge vs. megőrzési kötelezettség
A lokális szerver 30 nap után törli a felszinkronizált nyugtákat és event logot
(HU 2., EN 2.). A számviteli megőrzés viszont több év → ebből az következne, hogy
**a felhő nem opcionális, hanem a jogi archívum**, ami ellentmond a 4. pontnak
(„tisztán lokális topológia") és magának az USP-nek.

**Igazolatlan premissza (§13.5):** a konkrét megőrzési időt (8 év?) NEM ellenőriztem
forrásból, emlékezetből írtam. **Döntés előtt jogszabályi forrás kell.**

Ha a kötelezettség fennáll, tisztázandó: tisztán lokális telepítésnél hova
archiválunk (NAS? külső adathordozó? egyáltalán ne purge-eljünk?).

### `[ELDÖNTVE — automatikus szerepcsere; a bizonylat-rendezés NEM automatikus]` A4 — failback

**A régi spec állítása (HU 17. / EN 17.): a Master visszaállítása csak Siduri
Systems szuperfiókkal történhet. Ez ELVETVE** — a helyzet definíció szerint az,
hogy a helyen szerverhiba van, tehát pont akkor nem érhető el a support.

**Döntés (2026-08-22, 2. munkamenet):** a visszaállás **AUTOMATIKUS**, ha a fő és a
tartalék szerver **1 percig stabilan látják egymást és tudnak is beszélgetni**.
Emberi gombnyomás nem kell hozzá.

**Miért BIZTONSÁGOS ez, miközben az automatikus ÁTkapcsolás nem volt az — a kettő
NEM szimmetrikus, és ez a döntés kulcsindoklása:**
- Az automatikus **átkapcsolás** pont akkor futna le, amikor a két gép **NEM tud
  beszélni** egymással. Ez a kétértelmű eset: a némaság jelentheti azt is, hogy
  „halott", és azt is, hogy „élek, csak nem érlek el". Innen származik a
  kétmasteres kockázat.
- Az automatikus **visszaállás** pont akkor fut le, amikor a két gép **TUD
  beszélni**. A kétértelműség eltűnt: két, egymással kommunikáló gép meg tud
  egyezni abban, ki a főnök, kvórum nélkül is.

Tehát az automatizálás itt nem ugyanaz a kockázat, mint ott. **A felhasználó
intuíciója helyes volt.**

---

#### `[!]` ÜTKÖZÉS, amit ki kell mondani: „automatikus visszaállás" + „nulla adatvesztés" nem teljesíthető EGYSZERRE

A felhasználó kérése az volt, hogy a visszaálláskor a két szerver beszélgessen, és
**a lehető legkevesebb, ha megoldható 0 adatvesztés** legyen. **Ezt a két
követelményt együtt, teljes automatizmussal nem lehet teljesíteni** — az alábbi ok
miatt, ami nem megvalósítási nehézség, hanem az adat alakjából következik.

**Az adat nem „lemaradt", hanem ELÁGAZOTT.** A kiesés alatt:
- a régi fő szerver lemezén ott vannak azok a tranzakciók, amiket **commitolt, de
  nem replikált ki** (ez az aszinkron replikáció vállalt ára, lásd B1/b),
- a tartalék eközben **saját tranzakciókat** vett fel, **saját bizonylat-sorszámokkal**,
  amik ütközhetnek azokkal a számokkal, amiket a régi fő már kiadott.

Ez **nem lemaradás, hanem villa (fork).** Két elágazott előzményt nem lehet
„összeszinkronizálni" — az adatbázis-replikáció erre az esetre azt írja elő, hogy a
régi fő szervert **vissza kell tekerni** az elágazás pontjáig, és onnan újra kell
építeni az aktuális főnökből. **A visszatekerés viszont pont azokat a
tranzakciókat dobja el, amiket a felhasználó meg akar őrizni.**

**A feloldás — és ez a döntés végleges alakja:**

| Lépés | Automatikus? | Miért |
|-------|--------------|-------|
| Stabilitás észlelése (1 perc kölcsönös láthatóság + tényleges kommunikáció) | **IGEN** | Mechanikus, nincs benne kétértelműség |
| Az árván maradt tranzakciók **KIMENTÉSE** a régi fő szerver lemezéről, mielőtt bármit visszatekernénk | **IGEN, és KÖTELEZŐ** | Ez az, ami a „nulla adatVESZTÉS"-t garantálja: az adat nem semmisül meg |
| A régi fő visszatekerése és újraépítése az aktuális főnökből | **IGEN** | Mechanikus |
| Szerepcsere vissza (a régi fő megint a fő) | **IGEN** | Mechanikus |
| A kimentett tranzakciók **KÖNYVELÉSE** az új idővonalon | **NEM — emberhez kell** | Lásd alább |

**Miért nem lehet a KÖNYVELÉS automatikus:** azok a tranzakciók **valódi eladások,
valódi kinyomtatott nyugtákkal, amiket valódi vendégek elvittek.** A bizonylat-
sorszámaik viszont **ütközhetnek** azokkal, amiket a tartalék időközben kiadott.
Ha automatikusan visszaimportálnánk őket, **duplikált adóügyi bizonylatot**
hoznánk létre. Az adóügyi bizonylat visszamenőleges átszámozása nem opció.

**Tehát a „nulla adatvesztés" ÍGY teljesül:** az adat **soha nem semmisül meg**
(kimentés kötelező, a visszatekerés ELŐTT), és **hangosan a felhasználó elé kerül**
rendezésre. Amit nem tudunk megígérni, az az, hogy a rendezés emberi közreműködés
nélkül megtörténik. **Néma eldobás és néma visszaimportálás egyaránt TILOS** (§5).

---

#### `[ELDÖNTVE]` A4/a — TISZTA és KEMÉNY átvétel: két külön útvonal

Ez a felhasználó „beszélgessenek egymással" kérésének a legerősebb formája, és
**előre hozza a hasznot az átvételre is**, nem csak a visszaállásra:

- **TISZTA átvétel** — a régi fő szerver ÉL és elérhető a tartalék felől (ez a
  B1/c R5 esete: a pénztárgépek nem érik el, de a tartalék igen). Ekkor a tartalék
  az átvétel ELŐTT **leszívja a fő szerver még nem replikált tranzakcióit**, majd
  megmondja neki, hogy álljon le. **Eredmény: TÉNYLEG nulla adatvesztés, és a
  visszaálláskor nincs mit rendezni.**
- **KEMÉNY átvétel** — a régi fő szerver tényleg halott vagy elérhetetlen a
  tartalék felől is. Ekkor az árva tranzakciók **elkerülhetetlenek**, és a fenti
  kimentés-és-elétárás útvonal lép életbe.

**Ezt a két utat a tervben KÜLÖN kell nevesíteni**, mert a felhasználónak tett
ígéret is különbözik: tiszta átvételnél nulla veszteség ígérhető, keményénél nem.
§13.5 / §4 analógia: ne ígérjünk olyat, ami csak az egyik ágon igaz.

---

#### `[ELDÖNTVE — növekvő várakozás + leállási határ]` A4/b — billegés-védelem

**Döntés (2026-08-22, 2. munkamenet):** kell védelem.
- **Növekvő várakozás:** minden automatikus visszaállás után **hosszabb** stabil
  időszakot kell látni a következőhöz (pl. 1 perc → 5 → 15 → …). A konkrét
  lépcsősor konfigurációs paraméter, nem beégetett konstans.
- **Leállási határ:** ha X visszaállás történt Y időn belül, az automatika
  **kikapcsol**, és **hangosan szól**, hogy emberi beavatkozás kell. Nem csendben
  áll le (§5: a jelzés hiánya nem bizonyíték a sikerre) — kiírja, hogy azért nem
  próbálkozik többet, mert billegést észlelt.
- **X és Y konkrét értéke `[ ]` MÉRENDŐ / tapasztalati** — nem tippelhető.
  Kiindulásnak 3 visszaállás / 1 óra, de ez felülvizsgálandó valós üzemben.

**Miért nem elég az 1 perc önmagában:** egy haldokló switch pont olyan mintát ad,
ami ezt átveri — perceken keresztül stabil, majd megszakad. A fix küszöb nem
különbözteti meg a „helyreállt" és a „még nem halt meg végleg" esetet.

#### `[TÖRTÉNETI — a fenti döntés váltotta ki]` A4/b eredeti felvetése

**Új kockázat, amit az automatikus visszaállás teremt.** Ha a két szerver közti
kapcsolat szakaszos (haldokló switch, rossz kábel), a következő hurok áll elő:
1 perc stabilitás → automatikus visszaállás a főre → a kapcsolat megint elmegy →
a pénztárgépek csökkentett módba mennek → 5 perc → ember átkapcsol a tartalékra →
a kapcsolat visszajön → 1 perc → automatikus visszaállás → ...

**Minden kör egy teljes szerepcsere**, aminek ára van (minden kliens újracsatlakozik,
és minden körben keletkezhetnek árva tranzakciók). **Javaslat:** az 1 perc mellé
(a) fokozatosan növekvő várakozás minden automatikus visszaállás után, és
(b) egy határ — ha X visszaállás történt Y időn belül, az automatika **kikapcsol**,
és hangosan szól, hogy emberi beavatkozás kell. **Döntésre vár.**

#### `[ELDÖNTVE — azonnal, ahogy stabil]` A4/c — mikor történjen a szerepcsere

**Döntés (2026-08-22, 2. munkamenet):** a szerepcsere **azonnal** megtörténik,
amint a stabilitási feltétel teljesül — nincs napi zárásra halasztás.
A javasolt „csendes ablakra halasztás" **elvetve**: kiszámíthatóbb, hogy a rendszer
mindig ugyanúgy viselkedik, mint hogy a napszaktól függjön.

**Ez jól illeszkedik az A4/b döntéshez:** első alkalommal azonnal (gyors
helyreállás), ismétlődésnél viszont a növekvő várakozás úgyis egyre később engedi
— tehát a „csúcsidőben állandóan cserélget" forgatókönyvet nem az időzítés,
hanem a billegés-védelem zárja ki. A két döntés együtt koherens.

**`[JAVASLAT — jóváhagyásra]` Egy finomítás, ami megőrzi ezt a döntést, de levesz
egy terhet a csúcsidőről:** a **szerepcsere** legyen azonnali (mechanikus, gyors,
a kliensek újracsatlakoznak), de az **árva tranzakciók elétárása** — a „7 tétel
rendezésre vár" képernyő — **ne ugorjon a pénztáros arcába csúcsidőben**. Az adat
kimentése akkor is azonnali és kötelező; csak a **rendezésre való felszólítás**
várhat a menedzserre, egy jelzéssel, ami nem tűnik el, amíg nem foglalkoztak vele.
Így a felhasználó döntése („azonnal") érvényesül ott, ahol számít, és nem
terheljük a pénztárost egy könyvelési feladattal a sor közepén.

#### `[TÖRTÉNETI]` A4/c eredeti felvetése

**A visszaállás NEM sürgős.** A tartalék szerver közben rendesen kiszolgál; a hely
működik. A szerepcsere viszont **minden kliens újracsatlakozását jelenti**, tehát
egy rövid fennakadást — pénteken 20:00-kor ez fölösleges zavar, hajnali zárás után
viszont ingyen van.

**Javaslat:** az automatika ismerje fel, hogy „vissza lehet állni", de a tényleges
szerepcserét **halassza a napi zárásra / egy csendes ablakra**, kivéve ha a
menedzser azonnal kéri. **Döntésre vár** — ez termékdöntés, nem mérnöki (§12).

---

## B) Architekturális döntések, amiket a spec nyitva hagy

### `[RÉSZBEN ELDÖNTVE]` B1 — Split-brain 2 node-dal matematikailag nem oldható meg
Master + Emergency = 2 szavazó, **nincs kvórum**. Kell egy harmadik tanú (witness):
egy POS kliens, egy olcsó RPi, egy shared lock a felhőben — vagy **explicit emberi
failover** (a menedzser nyom egy gombot).

Kapcsolódó, külön eldöntendő: a PostgreSQL replikáció
- **aszinkron** → failovernél elveszik az utolsó néhány tranzakció, vagy
- **szinkron** → ha a Standby leáll, a Master is megáll.

Mindkettőnek üzleti következménye van; ki kell mondani, melyiket vállaljuk.

---

#### A B1 három részkérdésre bomlik — a státuszuk KÜLÖNBÖZŐ

| Részkérdés | Státusz |
|------------|---------|
| **B1/a — Benne van-e a HA az MVP-ben?** | `[ELDÖNTVE — IGEN, benne marad]` (lásd alább) |
| **B1/b — Milyen gép a tartalék szerver, és ebből mi következik a replikációra?** | `[ELDÖNTVE — szintén J1900]` (lásd alább) |
| **B1/c — Ki vált át: ember vagy automatika?** | `[ELDÖNTVE — kétlépcsős: gép ellenőriz, ember dönt]` — hat végrehajtási részlet (R1–R6) nyitva |

---

#### `[ELDÖNTVE — a HA BENNE MARAD az MVP-ben]` B1/a — HA scope

**Döntés (2026-08-22, 2. munkamenet):** a teljes vészhelyzeti szerver gépezet
(PostgreSQL replikáció, failover, fencing, split-brain tesztelés) **az MVP része**.

**Fontos, hogy ez a döntés az AJÁNLÁSSAL SZEMBEN született, tudatosan.** Az
alábbi „JAVASLAT" blokk öt pontja azt ajánlotta, hogy a HA kerüljön ki az MVP-ből.
A felhasználó ezt ismerve döntött úgy, hogy maradjon benne. §12: ami
viselkedés-/termékdöntés, az nem mérnöki hatáskör — a javaslat érvei
**megmaradnak dokumentációként** (miért volt vitatható), de **nem újranyitandók**.

**KÖVETKEZMÉNY, amit a döntés pillanatában még nem néztünk végig — a fázistervben
(E1) be kell árazni, NEM a döntés újranyitása:**
minden telepítés **legalább 2 dedikált gépet** igényel (master + tartalék), plusz a
pénztárgépek. Az E1 jelenlegi munkafeltételezése („kis bár / büfé, 1–2 pénztár")
mellett ez azt jelenti, hogy a legkisebb hiteles telepítés **2–3 gép**, nem 1–2.
Ez beszerzési és árazási tétel az ügyfél oldalán. Ha az E1 fázisterv írásakor ez
elfogadhatatlannak bizonyul, az az **E1 munkafeltételezését** kérdőjelezi meg
(kihez szólunk), nem ezt a döntést.

**KÖVETKEZMÉNY a spec 17. fejezetére:** a `siduri_spec_hu.md` 17. és a
`siduri_superprompt_en.md` §17 `[NYITOTT — B1, A4]` / `[OPEN — B1, A4]` jelölései
**részben feloldhatók** — a „kerüljön ki az MVP-ből" javaslat ELVETVE. A jelölések
csak a B1/c (ki vált) és az A4 (failback) miatt maradnak.

#### `[ELDÖNTVE — a tartalék szerver is J1900]` B1/b — a tartalék gép és a replikáció

**Döntés (2026-08-22, 2. munkamenet):** a vészhelyzeti szerver **szintén J1900**,
a meglévő telepített bázisból, **dedikált** gépként (nem egy pénztárgép mellékállása).

> ### `[!]` FIGYELEM — ez a döntés ELLENTMONDANI LÁTSZIK egy későbbi kijelentésnek
>
> A felhasználó ugyanaznap, később ezt mondta:
> *„a legtöbb esetben a szerver egy olyan gép lesz, ami egyébként kliens is, tehát
> egy tényleges használatban levő POS. Nagyon kevés hely engedheti meg magának,
> hogy egy irodában tárolt külön szervergépet vegyen és tartson fenn."*
>
> Ha a **fő** szerver jellemzően egy dolgozó pénztárgép, akkor **ugyanez a
> gazdasági érv a tartalékra is áll** — egy hely, ami a fő szerverre sem vesz
> külön gépet, a tartalékra végképp nem fog.
>
> **Ezt NEM oldom fel találgatással (§2.2).** A két olvasat érdemben eltérő
> hardver-költségvetést jelent:
> - **dedikált tartalék:** a gép csak PostgreSQL replikát visz → van szabad
>   kapacitása;
> - **tartalék egy dolgozó POS-on:** ugyanaz a J1900 viszi a WPF klienst, a
>   másodkijelzős videót ÉS a PostgreSQL replikát — ez az M1-nél is szűkösebb eset.
>
> **`[ ]` TISZTÁZANDÓ a felhasználóval.** Amíg nincs tisztázva, a `MERESEK.md`
> M1 tétele **mindkét változatot** mérendőként tartja.

**Ebből következő MUNKAFELTEVÉS a replikációra — figyelem, ez MÉG NEM IGAZOLT (§4):**
két J1900 között a **szinkron** replikáció várhatóan vállalhatatlan, mert szinkron
módban minden írás megvárja a lassabbik gép lemezét, és a pénztári tranzakció-
válaszidő közvetlenül ettől függ. **Ezért a munkafeltevés: ASZINKRON replikáció.**

**De ezt tilos tényként kezelni.** §4: „teljesítmény-állítás CSAK méréssel". A
„szinkron kizárt" mondat jelenleg **érvelés, nem mérés**. Ami hiányzik hozzá:
egy valós J1900 páron mért írási válaszidő szinkron és aszinkron módban, tipikus
pénztári terhelés mellett. Amíg ez nincs meg:
- az aszinkron a **tervezési alapeset**, mert ez a konzervatív irány
  (aszinkronnál tudjuk, hogy adatot veszthetünk, és fel tudunk rá készülni;
  szinkronnál azt hinnénk, hogy nem — az a rosszabb tévedés),
- de **semmilyen számot nem írunk le** arról, hány tranzakció veszhet el.
  Ez `[ ]` MÉRENDŐ tétel marad, hardverfüggő (E3).

**A vonzó középút továbbra is CSAPDA — ez elvi alapon kimondható, mérés nélkül is.**
Az ötlet, hogy „legyen szinkron, de ha a tartalék leáll, váltson automatikusan
aszinkronra", pontosan a §5 néma kudarca: a mechanizmus, ami eldönti, hogy „a
tartalék halott", hálózati particiónál téved — és amikor téved, **pont akkor írsz
védtelenül, amikor azt hiszed, védve vagy**, és semmi nem szól. Rosszabb a
vállaltan aszinkronnál, mert hamis biztonságot ad. **Ezt az ágat elvetjük.**

#### `[ELDÖNTVE — kétlépcsős: gép ellenőriz, ember dönt]` B1/c — ki vált át

**Döntés (2026-08-22, 2. munkamenet).** Sem tisztán kézi, sem tisztán automatikus:
**kétlépcsős.** A gép gyűjti a bizonyítékot, az ember hozza a döntést.

**A folyamat, ahogy a felhasználó megfogalmazta:**

1. **Amint a pénztárgép elveszti a szerverkapcsolatot — BÁRMI miatt —, látványosan
   jelzi a csökkentett módot.** A jelzés **kattintható**, és a mögötte lévő
   képernyő megmondja, mit tegyen a személyzet: **ellenőrizze a szervergépet és az
   összes gép hálózatát.**
2. **Átkapcsolást a rendszer NEM ajánl fel azonnal.** Csak akkor, ha a **tanúk
   már több mint 5 perce** nem érik el a szervert.
3. **Az átkapcsolást ekkor is EMBER indítja**, gombnyomással.
4. **A pénztárgépnek fel kell ismernie, ha Ő esett ki a hálózatról**, és ilyenkor
   **erre kell figyelmeztetnie, nem a szerver hibájára.**

**Miért ez jobb, mint a felvázolt három lehetőség bármelyike:**
- **A gépnek nincs joga átkapcsolni**, tehát egy téves detektálás ELVILEG nem tud
  két fő szervert csinálni. A kétmasteres, összefésülhetetlen nyugtasorozat
  hibaosztálya nem megoldódik, hanem **nem keletkezik** — ugyanaz az érvelési alak,
  mint az A2-nél a konfliktusfeloldásnál.
- **Az embernek nem kell diagnosztizálnia**, csak dönteni. A tiszta kézi változat
  gyenge pontja pont az volt, hogy a pultostól várjuk el annak eldöntését, hogy a
  szerver halott-e — amire nincs se ideje, se eszköze. Itt a gép már megnézte.
- **Az 5 perces küszöb kiszűri a pillanatnyi akadásokat**, tehát nem lesz
  „minden wifi-koccanásra felugró átkapcsolás-ajánlat" (kapunyitási zaj).
- **A 4. pont a legértékesebb elem, és egyik felvázolt lehetőségben sem szerepelt.**
  Enélkül a legvalószínűbb hibaeset (egyetlen pénztárgép wifije elmegy) úgy
  jelenne meg, hogy „a szerver halott" — és a személyzet elrohanna újraindítani
  egy tökéletesen egészséges szervert, közben a többi gép zavartalanul dolgozik.
  Ez pontosan a §5 hibaosztálya megfordítva: a felület olyat állítana, ami nem igaz.

**A tiszta kézi változathoz képest mi az ára:** semmi. Szigorúan jobb.
**Az automatikushoz képest mi az ára:** hajnali 3-kor, ha senki nincs bent, a hely
csökkentett módban működik reggelig. Ezt a felhasználó vállalja; a hálót az adja,
hogy a pénztárgép csökkentett módban is tud eladni (A2/b).

---

##### `[ ]` A döntés VÉGREHAJTÁSI RÉSZLETEI — ezek külön eldöntendők

A döntés iránya megvan, de hat olyan részlet van, ami nélkül nem
implementálható, és mindegyik önállóan tud csendben elromlani. Ezek nem a
döntés újranyitása, hanem a kitöltése.

**R1 `[ ]` — Ki számít „tanúnak", és mit jelent, hogy „a tanúk nem érik el"?**
A megfogalmazás többes számú. Tisztázandó: minden pénztárgép tanú, vagy kijelölt
halmaz? Kell-e mindegyik egyetértése, többség, vagy elég N darab?
**Kritikus alesetek, amikre külön szabály kell:**
- **Egypénztáras telepítés.** Ekkor „a tanúk" = egyetlen gép, tehát nincs
  kereszt-ellenőrzés, és a 4. pont (felismerni, hogy én estem ki) elveszti a fő
  információforrását. **Az egész tanú-séma ilyenkor nullára degradálódik.**
  Ez nem elméleti: az MVP jelenlegi célprofilja pont ilyen hely.
- **Lekapcsolt gép némasága NEM bizonyíték.** Külön kell kezelni azt, hogy egy
  gép JELENTI, hogy nem éri el a szervert, attól, hogy egy gépet MI nem érünk el.
  Ha a kettő összemosódik, egy éjszakára lekapcsolt pénztárgép „szavazatként"
  fog számítani. Ez a §5 néma kudarca: a jelzés hiánya nem bizonyíték.

**R2 `[ ]` — MIBŐL ismeri fel a pénztárgép, hogy Ő esett ki?**
A felhasználó követelménye világos, a mechanizmus nem magától értetődő: egy
izolált gép definíció szerint nem tud senkitől megkérdezni semmit.
Rendelkezésre álló jelek, növekvő értékben:
- **saját hálózati interfész állapota** (kábel kihúzva, wifi lecsatlakozott) —
  olcsó és egyértelmű, DE a gyakori esetre nem tüzel (az AP-hoz csatlakozva
  vagyunk, csak az AP uplinkje halt meg);
- **elér-e BÁRMI mást** (alapértelmezett átjáró, nyomtató, konyhai kijelző);
- **eléri-e a TÖBBI pénztárgépet és a TARTALÉK szervert** — ez a legélesebb teszt:
  ha a tartalékot eléri, a fő szervert nem, akkor **nem én vagyok a hibás**.

**Ez egy ÚJ ARCHITEKTURÁLIS KÖVETELMÉNY, amit eddig egyik doksi sem tartalmazott:**
a jelenlegi kép csillag alakú (mindenki a szerverrel beszél). A gép-gép közti
elérhetőség-vizsgálathoz a pénztárgépeknek **egymást is látniuk kell**. Ennek ára
van: felderítés (mDNS már tervben van) ÉS kölcsönös hitelesítés, mert a LAN nem
megbízható (B6). Ezt a fázistervben nevesíteni kell.

**R3 `[ ]` — Az 5 perc: mihez képest, milyen órán, és lejár-e az ajánlat?**
- **Milyen órán:** a szerver elérhetetlen, tehát a pénztárgép saját óráján. Ezért
  **monoton időmérő** kell, nem fali óra — különben egy óraállítás vagy egy
  időzóna-váltás átugorja vagy befagyasztja a visszaszámlálást (§8, D4).
- **Az 5 perc jó szám-e:** két irányba is vitatható. Egy pénteki csúcsban 5 perc
  asztalkezelés nélkül sok. Ugyanakkor egy Windows-frissítés utáni újraindulás
  simán tarthat tovább 5 percnél — és ha valaki az 5. percben átkapcsol, a 6.
  percben visszatérő fő szerver miatt le kell futtatni a **visszaállítást**, ami a
  rendszer legdrágább művelete. **Javaslat: legyen konfigurálható, 5 perc az
  alapérték.**
- **AZ AJÁNLATNAK LE KELL JÁRNIA.** Ha a fő szerver a 7. percben visszatér, miközben
  az „átkapcsoljak?” ablak a képernyőn van, az ablaknak **magától és feltűnően
  vissza kell vonulnia**. Enélkül valaki 20 perccel később, egy már egészséges
  rendszeren nyomja meg, és fölöslegesen kikényszerít egy failovert. §5.

**R4 `[ ]` — Több gépen jelenik meg a gomb. Mi van, ha többen nyomják meg?**
Ha három pénztárgép mutatja az ajánlatot, három ember nyomhat rá. **Az átvételnek
idempotensnek kell lennie:** az első nyer, a többi „már átkapcsolva" választ kap,
nem hibát és nem második átvételt. Ez a F1 (idempotencia) mintája, itt vezérlési
műveletre alkalmazva.

**R5 `[ ]` — Mi van, ha a fő szerver ÉL, csak a pénztárgépek nem érik el?**
Ez a legkellemetlenebb ág: a tartalékot arra kérjük, vegye át a szolgálatot,
miközben a fő szerver él, és nyitott rendelések vannak nála.
- Az átvétel előtt a tartalék **próbálja meg megmondani a főnek, hogy álljon le.**
  Ha a fő hallja: tiszta, kockázatmentes átadás.
- Ha nem hallja: a tartalék az ember felhatalmazására akkor is átvesz — és
  **ekkor az epoch-mező (fencing) az egyetlen, ami megvéd.**
- **Ebből következik, hogy a fencinget a KLIENSNEK is ki kell kényszerítenie:**
  egy visszacsatlakozó pénztárgép, ami a nála ismertnél RÉGEBBI epochú szervert
  talál, **köteles megtagadni a kommunikációt**. §6: a javítás mindkét oldala kell —
  ha csak a szerver oldalon van fencing, a régi master a hozzá visszacsatlakozó
  klienseket még kiszolgálja.

**R6 `[ ]` — Ne ajánljuk fel azt, ami nem fog menni.**
Ha a **tartalék szerver maga sem elérhető vagy nem egészséges**, akkor
átkapcsolást **felajánlani sem szabad** — helyette azt kell kiírni, hogy mindkét
szerver elérhetetlen, és a csökkentett mód folytatódik. §5: „a felület ne kínáljon
olyat, ami nem működik".

##### `[ELDÖNTVE]` B1/c kiegészítések (2026-08-22, 2. munkamenet, második kör)

**K1 — MINDEN gép ÖNÁLLÓAN megy csökkentett módba.** Ha egy pénztárgép nem éri el a
szervert, **azonnal csökkentett módba vágja magát, akkor is, ha a többi gép
zavartalanul működik.** A csökkentett mód tehát **gépenkénti állapot**, nem a hely
állapota, és nem függ a tanú-szavazástól. (A tanú-szavazás CSAK az átkapcsolás
felajánlását vezérli, a saját módváltást nem.)

**Miért ez fontos, és mi a KÖVETKEZMÉNYE — ez váratlan JÓ hír:** ettől a helyi
napló + visszatéréskori egyeztetés **nem csak katasztrófánál fut le**, hanem
minden egyes wifi-koccanásnál egyetlen gépen. Vagyis a rendszer legkockázatosabb
darabja (az egyeztetés) **gyakran futó, tehát gyakran hibázó, tehát gyakran
javított kód lesz** — nem olyan, ami évente egyszer, éles katasztrófában fut
először. §1 szempontjából ez sokkal jobb, mint egy ritkán érintett ág.

Egyszerű alesete: ha csak EGY gép esett ki, de a szerver él, akkor a gép a
visszatéréskor **ugyanannak a szervernek** játssza le a naplóját. Nincs
szerepcsere, nincs epoch-váltás — ez a legegyszerűbb egyeztetési út, és ez lesz a
leggyakoribb.

**K2 — az R6 MEGERŐSÍTVE.** Átkapcsolás felajánlása előtt a rendszer **kérdezze meg
a tartalék szervert, hogy egyáltalán elérhető és egészséges-e.** Ha nem, az
átkapcsolást **felajánlani sem szabad**.

##### `[ELDÖNTVE — JÓVÁHAGYVA 2026-08-22]` A személyzetnek szóló üzenetek szövege

A felhasználó kérte a két üzenetet, a megfogalmazást rám bízta. **Három** üzenet
készült, nem kettő, mert a gép három érdemben különböző helyzetet tud
megkülönböztetni, és a §5 („a felület ne állítson olyat, ami nem igaz") szerint
nem szabad kettőbe gyömöszölni őket.

**A felhasználó 2026-08-22-én JÓVÁHAGYTA** mindhárom szöveget, a „hálózat"
szóhasználattal (nem „internet") együtt, plusz külön, nem keveredő jelzést az
internet hiányára.

**Ezek MINTASZÖVEGEK, nem végleges felirat.** A design-fázisban a UiUX
skill-készlettel (lásd `FOLYAMATBAN.md` 0.2) át kell nézni tipográfiára,
kontrasztra és érintőképernyős olvashatóságra. A TARTALOM viszont jóváhagyott,
azon érdemben ne változtasson a design-kör.

**(1) A SZERVER a gyanús** — ez a gép eléri a többi gépet és/vagy a tartalék
szervert, de a fő szervert nem:

> ### ⚠ NINCS KAPCSOLAT A SZERVERREL — CSÖKKENTETT MÓD
> **Eladni és nyugtát adni továbbra is tud.** Asztalkezelés most nem érhető el.
>
> **A hiba a szervergépen van, nem ezen a pénztárgépen.** Kérjük, ellenőrizze:
> 1. **Be van kapcsolva a szervergép?** Világít rajta a bekapcsolás-jelző?
> 2. **Be van dugva a hálózati kábele?** Villog a lámpa ott, ahol a kábel
>    csatlakozik a géphez?
> 3. **Ha be van kapcsolva és a kábel is rendben van: indítsa újra a szervergépet**
>    (nyomja meg a bekapcsológombot, várjon amíg leáll, majd kapcsolja vissza),
>    és **várjon 2–3 percet.**
>
> Ha 5 perc múlva sem áll helyre, a rendszer fel fogja ajánlani az átkapcsolást a
> tartalék szerverre.

**(2) EZ A GÉP a hibás** — nem ér el semmit, vagy rossz hálózaton van:

> ### ⚠ EZ A GÉP NEM ÉRI EL A HÁLÓZATOT — CSÖKKENTETT MÓD
> **Eladni és nyugtát adni továbbra is tud.** Asztalkezelés most nem érhető el.
>
> **A szerver valószínűleg rendben van — a hiba ezen a gépen van.
> NE indítsa újra a szervergépet.** Kérjük, ellenőrizze:
> 1. **Vezetékes gépnél:** be van dugva a hálózati kábel ebbe a gépbe? Villog a
>    lámpa a csatlakozónál?
> 2. **Wifis gépnél:** a **megfelelő** hálózathoz csatlakozik? Nem a **vendég-wifire**
>    kapcsolt véletlenül? (A helyes hálózat neve: `<konfigból>`)
> 3. Elég erős a wifi jel ezen a helyen?
> 4. Ha a fentiek rendben vannak: **indítsa újra EZT a gépet.**

**(3) BIZONYTALAN / az egész hálózat gyanús** — a gép semmit nem ér el, vagy
egypénztáras helyen nincs mihez viszonyítania:

> ### ⚠ NINCS HÁLÓZATI KAPCSOLAT — CSÖKKENTETT MÓD
> **Eladni és nyugtát adni továbbra is tud.** Asztalkezelés most nem érhető el.
>
> **A rendszer nem tudja megállapítani, hol a hiba.** Kérjük, ellenőrizze
> sorrendben:
> 1. **A hálózati eszközt (switch / router):** be van kapcsolva, világítanak rajta
>    a lámpák?
> 2. **A szervergépet:** be van kapcsolva, be van dugva a hálózati kábele?
> 3. **Ezt a gépet:** be van dugva a kábel, illetve a megfelelő wifihez csatlakozik?
> 4. Ha nem talál hibát, **indítsa újra a hálózati eszközt, majd a szervergépet**,
>    és várjon 3–5 percet.

**`[!]` SZAKMAI PONTOSÍTÁS a felhasználó megfogalmazásához:** a felhasználó azt
kérte, hogy az üzenet kérdezze meg, „kap-e internetet" a szervergép. **A lokális
szervernek a pénztárgépek kiszolgálásához NEM kell internet, csak helyi hálózat.**
Ha az üzenet „internetet" mond, a személyzet a szolgáltatót fogja hívni, miközben
a valódi hiba egy switch. Ezért a fenti szövegekben **„hálózati kábel" és
„hálózat"** szerepel, nem „internet".

**Az internet ettől függetlenül számít**, csak MÁSRA: az adóhatósági
adatszolgáltatáshoz és a felhőszinkronhoz. Ezért javasolt egy **külön, önálló
jelzés** az internet hiányára, ami **nem keveredik** a szerverkapcsolat
jelzésével — ez egyébként már körvonalazódik a 19. fejezet 18 órás
riasztásában (C11).

##### `[ ]` Amit a döntés MEGVALÓSÍTÁSA a felületen megkövetel (design-tétel)

A várakozási 5 perc **ne üres visszaszámlálás legyen**, hanem mutassa, mit
állapított meg közben a gép: „a te géped hálózata: rendben" / „másik 2 pénztárgép:
szintén nem éri el a szervert" / „tartalék szerver: elérhető". Így amikor
megjelenik az ajánlat, az ember **nem találgat**.

**És egy kockázat, amit ez a konstrukció TEREMT:** ha a gép „javasolja" az
átkapcsolást, a személyzetben kialakul a „nyomd meg a zöld gombot" reflex, és egy
idő után ellenőrzés nélkül fogják nyomni. **Ellenszer:** a megerősítő képernyő ne
egyszerű igen/nem legyen, hanem **mondja meg számmal a következményt** — hány
tranzakció veszhet el —, amint ezt megmértük (§4).

---

**A B1/c-vel EGYÜTT döntendő A4 (failback) TOVÁBBRA IS NYITVA.** A felhasználó a
„ki vált át" kérdésre válaszolt; a „ki és hogyan állítja vissza a fő szervert"
kérdésre még nem.

---

##### A döntéskor is érvényes ÚJ szempont: három igazságforrás egy incidens után

**ÚJ, a mostani döntések által teremtett helyzet: három igazságforrás egy incidens
után.** Mivel (a) a replikáció aszinkron, (b) a degradált gyorseladás teljes
egészében az MVP-ben van, és (c) a HA is az MVP-ben van, egy szerverhiba után
**három** helyen lesz adat, ami nincs mind ugyanott:
1. a halott master lemezén (amit még nem replikált ki),
2. a tartalék szerver adatbázisában (ami átvette a szolgálatot),
3. a pénztárgépek helyi naplóiban (amiket degradált módban írtak).

Ez nem hiba, hanem a három döntés együttes következménye — de azt jelenti, hogy a
**visszaállási (failback) procedúra az MVP legkockázatosabb egyetlen darabja**, és
a szimulátor (D5) nem opcionális hozzá. Az A4 (failback) ezért a B1/c-vel EGYÜTT
döntendő, ahogy eddig is.

---

#### `[TÖRTÉNETI — a HA scope kérdésében ELVETVE]` A 2026-08-22-i átbeszélés javaslata

> **Státusz: a 3. pontja (HA ki az MVP-ből) ELVETVE a B1/a döntéssel.** A blokk
> **megmarad**, mert az érvei a B1/c-hez és az E1 fázistervhez továbbra is
> relevánsak, és mert §12 szerint le kell írni, mit vetettünk el és miért.
> Az 1., 2. és 4. pont **továbbra is érvényes megállapítás**; az 5. pont a B1/c
> nyitott kérdésének egyik oldala.

**1. Az A2 döntés ÁTRENDEZTE a B1 tétjét — ez a legfontosabb megállapítás.**
Amíg az volt a kép, hogy a szerver halálakor a hely megáll, az Emergency Server
**létfenntartó berendezés** volt. Az A2 (degradált gyorseladás) után viszont
átminősült: már nem azt akadályozza meg, hogy a hely ne tudjon pénzt elfogadni,
hanem azt, hogy az **asztalkezelés** essen ki. Ez **kényelmi funkció, nem
katasztrófavédelem.**

**2. Fogalmi csúszás mindkét specben (§2.4):** az USP az **internetkimaradás**
elleni védelem (HU 1., EN 1.) — ezt már maga a lokális szerver megoldja. Az
Emergency Server viszont a **lokális szerver HARDVERHIBÁJA** ellen véd, ami
egy sokkal ritkább, teljesen más esemény. A két dolog összemosódik a doksiban,
és ettől a HA indokoltabbnak látszik, mint amennyire az.

**3. `[ELVETVE — lásd B1/a]` Javasolt scope-döntés:** ~~a teljes HA kerüljön ki az
MVP-ből~~. **A felhasználó ezt elvetette: a HA az MVP része.**
Ami ebből a pontból **ÉLETBEN MARAD és kötelező**: az **epoch-mező kerüljön be a
protokollba az első naptól**. Sőt, most már nem opcionális elővigyázatosság, hanem
**működési követelmény** — ha a failover tényleg megépül az MVP-ben, az epoch az a
mechanizmus, ami megakadályozza, hogy a visszatérő régi master még kiszolgáljon
klienseket (fencing). Utólag beletenni azt jelentené, hogy minden kliens minden
verziójával kompatibilitást kell kezelni (D3).

**4. A vonzó középút CSAPDA — ezt elvi alapon ki lehet mondani.**
Az ötlet, hogy „legyen szinkron replikáció, de ha a Standby leáll, automatikusan
váltson aszinkronra", pontosan a **§5 néma kudarca**. Az a mechanizmus, ami
eldönti, hogy „a Standby halott", hálózati particiónál tévedhet — és amikor
téved, **pont akkor írsz védtelenül, amikor azt hiszed, védve vagy**, és semmi
nem szól. Ez ROSSZABB a vállaltan aszinkronnál, mert hamis biztonságot ad.
Vagy igazi szinkron kemény megállással, vagy vállaltan aszinkron.

**5. Kézi vs. automatikus failover — az aszimmetria.**
A kézi ára: valaki észreveszi és megnyomja. Az automatikusé, ha a detektor téved:
két master, szétdivergált adat, és egy összefésülés, aminek **nincs helyes
megoldása** — két külön kiadott nyugtasorozat nem merge-elhető.
Valós ellenérv: 22:00-kor egy pultossal a „menedzser megnyom egy gombot"
jelentheti azt, hogy *senki*. Két válasz: (a) a failover **jogosultsághoz**
kötődjön, ne szerephez, hogy a pultos is megkaphassa; (b) az A2 degradált módja
**maga a biztonsági háló** — ha senki nem nyom gombot, a POS akkor is tud eladni.

#### `[ ]` MÉRENDŐ, nem becsülhető (§4)
A failovernél elveszthető tranzakciók száma **nincs megmérve**, és emlékezetből
vagy analógiából megadni tilos. Egy J1900-on, terhelt SSD-vel a replikációs
késés érdemben rosszabb lehet, mint modern gépen. **A felhasználó felé semmilyen
adatvesztési vállalás nem tehető valós J1900-on végzett mérés előtt.**

#### Az epoch-fencing valódi ára
Nem egy feature, hanem egy feature **plusz teszt-infrastruktúra**: epoch a
DB-ben, epoch minden kliens-handshake-ben, kliens-oldali perzisztencia, átvételi
procedúra, zárolási útvonal — és split-brain forgatókönyvet **kézzel nem lehet
megbízhatóan reprodukálni**, tehát szimulátor kell hozzá (D5).

#### `[ ]` NYITOTT ÜZLETI KÉRDÉS (nem mérnöki, §12)
Az Emergency Server a specben **eladási érvként** szerepel (HU 17., EN 17.). Ha
kikerül az MVP-ből, az a **termék pozicionálását** érinti, nem csak a fejlesztési
sorrendet. Ezt a felhasználónak kell eldöntenie.

### `[ ]` B2 — Mi konkrétan a „Message Queue"?
A spec aszinkron üzenetsort ír az NTAK-ra (HU 3., EN 3.), de nem nevezi meg.
J1900-on egy RabbitMQ/Kafka kizárt.

Reális: **transactional outbox tábla a PostgreSQL-ben + ütemezett poller.** Ugyanez
a minta kell a felhőszinkronra, a számlázásra és a licenc-heartbeatre is — érdemes
most rögzíteni, mert mindenhol visszajön.

### `[ELDÖNTVE — J1900 meglévő bázis, GraalVM kényszer marad]` B3 — Mi a valódi minimum célhardver?
A spec a J1900 miatt teszi **kötelezővé** a GraalVM Native Image-et (HU 2., EN 2.).
A Spring Boot + JPA/Hibernate + Flyway native image működik, de reflection-hint
pokol és lassú build.

**Döntés (2026-08-22):** a J1900 **meglévő telepített bázis**, kötelezően
támogatandó. A GraalVM Native Image kényszer tehát **marad**, és a fejlesztési
sebességre gyakorolt hatását a fázistervbe (E1) be kell árazni.

**Következmények, amiket ez azonnal maga után von:**
- **Native image-barát könyvtárválasztás az első naptól.** Utólag lecserélni egy
  reflection-nehéz függőséget nagyságrenddel drágább. Minden új függőségnél
  kritérium: van-e hivatalos GraalVM metadata (reachability-metadata repo).
- **A CI-ban a native build KÖTELEZŐEN fusson** — nem elég JVM-en zöldnek lenni.
  Ez a §1.1 „rossz kódút" hibaosztálya: a JVM-es teszt olyan úton mér, amit az
  éles native artefakt sosem jár be.
- **A native image csak a szerver indulási idejét és RSS-ét javítja**, a
  PostgreSQL memóriaigényét nem. A 4–8 GB RAM-on futó PG + Java + replikáció
  továbbra is szűkös → a PG memórialimitek (`shared_buffers`, `work_mem`,
  `max_connections`) mérendő, nem tippelendő paraméterek (§4).

**Pontosítás (2026-08-22): a bázis VEGYES** — J1900 fut **szerverként is és POS
kliensként is**. Ennek két, egymástól független következménye van:

**(1) A szerver oldalon** a GraalVM kényszer megerősítve, a fentiek szerint.

**(2) A POS kliens oldalon** — ez a spec sehol nem tárgyalja — a **WPF kliens
teljesítmény-költségvetése is szoros** egy Bay Trail iGPU-n. Konkrét kockázatok:
- a 20. pont **másodkijelzős videó 720p-ben**, párhuzamosan a teljes képernyős
  POS UI-jal,
- animációk / átmenetek egy 2013-as integrált GPU-n,
- a .NET Desktop Runtime + WPF memóriaigénye 4 GB RAM mellett, ha ugyanazon a
  gépen PG vagy más is fut.

**§4 szerint ez MÉRENDŐ, nem érvelendő.** Semmilyen teljesítmény-állítás nem
kerülhet a tervbe valós J1900-on végzett mérés nélkül. **Ehhez kell egy fizikai
referenciagép** — ez beszerzési/logisztikai tétel, felvéve az E3-hoz.

**`[ ]` NYITVA MARAD — pontosítandó:**
1. Konkrét RAM / SSD a meglévő bázison (a „64 GB SSD" és a „4–8 GB RAM" a specből
   jön, nem mérésből).
2. Az Emergency Server (17.) is J1900? Ha igen, a szinkron replikáció végképp
   kizárt (lásd B1).
3. Egy gépen futhat-e egyszerre szerver ÉS POS kliens? (Kis helyen ez a
   kézenfekvő telepítés, és ez a legszűkösebb eset.)

### `[ ]` B4 — Ki nyomtat: a szerver vagy a kliens?
A 11. pont szerverközpontú routingot ír le (a szerver 5 mp után átirányít). De a
nyugtanyomtató és a **fiskális nyomtató fizikailag a POS gépen lóg** (soros/USB).

Valószínű a hibrid: a szerver dönt az útvonalról, a kliens hajtja végre a saját
perifériáin és visszajelez. Le kell fektetni — az egész print alrendszer erre épül.

### `[ ]` B5 — SoftPOS = PSP-döntés, nem fejlesztési döntés
SoftPOS-hoz acquirer/PSP szerződés kell (SumUp, Barion, OTP, Global Payments…), és
az SDK jellemzően **Android-only** → tehát a kártyás fizetés a Flutter PDA-n fut,
nem a WPF POS-on.

**Architekturális következmény:** a 13. pont fizetési állapotgépe **elosztott** kell
legyen — a tranzakciót a szerver vezérli, a terminál lehet bármelyik eszköz.

Melyik PSP-vel számolunk?

### `[ ]` B6 — Kliens↔szerver biztonság (a spec egyáltalán nem tárgyalja)
A LAN nem megbízható (vendég wifi ugyanazon az AP-n). Szükséges:
- eszközregisztráció (enrollment), nem „aki a hálózaton van, az beszélhet";
- lokális TLS: self-signed CA → tanúsítványkiosztás és -megújítás megoldva;
- **a 4 jegyű PIN mindössze 10 000 kombináció** → rate limit + lockout kötelező;
- PIN hash (argon2/bcrypt), nem sima hash;
- API-szintű jogosultságellenőrzés, nem csak gomb-elrejtés a UI-on.

### `[ ]` B7 — Multi-tenancy a felhőben
Nincs specifikálva: schema-per-tenant / DB-per-tenant / row-level. GDPR: adatexport,
törlési igény, hol tárolunk (EU).

### `[ ]` B8 — Hol él az API-szerződés?
Három nyelv (Java / C# / Dart) fogyasztja ugyanazt az API-t. Kézzel szinkronban
tartva garantáltan szétcsúszik — ez a MERNOKISAROKKOVEK §6 varrat-hibaosztálya.

Javaslat: **6. repo, vagy a `Siduri-Docs`-ban egy `contracts/` mappa** (OpenAPI +
AsyncAPI a WebSocket eventekre), amiből generáljuk mindhárom kliens SDK-t, plusz
paritás-őr (§6).

### `[RÉSZBEN ELDÖNTVE]` B9 — Telepítési MÉRETOSZTÁLYOK (új tétel, 2026-08-22)

**Ez a tétel a 2. munkamenetben született, egyik eredeti doksiban sem szerepelt.**
Feloldja azt a feszültséget, amit a „vészhelyzeti szerver az MVP-ben marad"
döntés (B1/a) teremtett: nem kell MINDEN helyre két dedikált gép.

**A felhasználó döntése (2026-08-22) — gépszám szerinti lépcsők:**

| Gépszám a helyen | Topológia | Vészhelyzeti szerver |
|------------------|-----------|----------------------|
| **1 gép** | **Az egyetlen pénztárgép MAGA a szerver** (kombinált szerep) | Nincs — nincs második gép |
| **2–3 gép** | Külön szerver + pénztárgépek | **Nem kötelező, de LEHETŐSÉGKÉNT fenntartva** |
| **4+ gép** | Külön szerver + pénztárgépek | **KÖTELEZŐ** |

**`[ELDÖNTVE]` B9/a — az egygépes hely: a pénztárgép maga a szerver.**
A felhasználó indoklása: *„az egyetlen gép maga a szerver, így annak elérésével
nem lehet probléma."* Ez helyes — nincs hálózati ugrás, tehát a
szerver-elérhetetlenség hibaosztálya ott elvileg nem keletkezik, és az egész
tanú-kérdés (R1) tárgytalanná válik ezen a lépcsőn.

**KÖVETKEZMÉNYEK, amiket ez azonnal maga után von — ezek NEM a döntés
újranyitása, hanem az árazása:**

1. **A B3 3. nyitott kérdése ezzel ELDŐLT.** Ott az szerepelt nyitottként:
   *„Egy gépen futhat-e egyszerre szerver ÉS POS kliens?"* — **igen, és ez most már
   nem hipotézis, hanem TÁMOGATOTT TERMÉKKONFIGURÁCIÓ.**

2. **`[!]` Ez a rendszer legszűkösebb hardveres esete, és most kötelezővé vált.**
   Egy J1900-on egyszerre fut: PostgreSQL + a Java szerver (GraalVM native) + a
   WPF pénztárgép-kliens + a 20. pont szerinti 720p másodkijelzős videó, 4 GB RAM
   mellett. **§4: ez MÉRENDŐ, nem becsülhető**, és most nem „érdekes lenne
   megnézni", hanem **az MVP egyik szállítási feltétele**. Ha nem fér bele,
   vagy a lépcső dől meg, vagy a hardverkövetelmény.

3. **Az egygépes helyen nincs semmilyen hardverhiba-védelem.** Ha az a gép
   meghal, a hely megáll — a csökkentett mód sem segít, mert az is azon a gépen
   futna. **Ezt az értékesítési anyagban és a telepítési dokumentációban ki kell
   mondani**, nem elhallgatni (§5: a felület / a termék ne ígérjen olyat, ami nincs).
   Ezen a lépcsőn a védelem: **mentés és gyors csereberendezés** (D1), nem HA.

4. **A csökkentett gyorseladás (A2/b) haszna lépcsőnként MÁS.** Egygépes helyen
   közel nulla (ha a gép él, a szerver is él; ha nem él, semmi sem). 2+ gépes
   helyen viszont valódi. Ez nem ok a kivételére — úgyis megépül —, de a
   fázistervben és a marketingben pontosan kell fogalmazni.

**`[ELDÖNTVE — a TARTALÉK SZERVERRE vonatkozik]` B9/b**

**Tisztázva (2026-08-22):** a „2–3 gépnél nem kell, 4+ gépnél kötelező" szabály a
**vészhelyzeti (tartalék) szerverre** vonatkozik, nem a tanú-sémára.

**KÖVETKEZMÉNYEK, amiket ez maga után von:**

1. **A „nincs tartalék szerver" NEM hibaállapot, hanem elsőrangú konfiguráció.**
   A szoftvernek támogatnia kell, hogy egy helyen egyáltalán nincs tartalék.
   Ilyenkor **átkapcsolást felajánlani sem szabad** — ez ugyanaz a szabály, mint
   az R6 (ne kínáljunk olyat, ami nem működik), csak itt nem hiba miatt, hanem
   mert nincs is mire kapcsolni. A felület mondja meg őszintén: „ezen a helyen
   nincs tartalék szerver, a csökkentett mód a védelem".

2. **A tanú-kérdés (R1) NEM oldódott meg, csak élesebb lett.** Most már
   lépcsőnként kell megválaszolni:
   - **1 gép:** tárgytalan (a gép maga a szerver).
   - **2–3 gép, tartalék NÉLKÜL:** nincs mire átkapcsolni → tanú sem kell. A gép
     csak azt akarja tudni, ŐT vágták-e le — ehhez a többi gépet kérdezi meg.
   - **2–3 gép, tartalékkal:** a tartalék szerver a kézenfekvő tanú („te látod a
     főt?"), plusz a többi gép.
   - **4+ gép:** teljes, több tanús séma.
   **`[ ]` Ez így elfogadható-e, jóváhagyásra vár.**

3. **A csökkentett gyorseladás haszna ITT a legnagyobb.** A 2–3 gépes,
   tartalék nélküli helyen a szerver kiesésekor a csökkentett mód **az egyetlen**
   védelem — nem tartalék, nem másodlagos háló. Ez utólag igazolja azt a
   döntést, hogy a csökkentett mód teljes egészében az MVP-ben van (A2/b).

### `[ ]` B10 — Kliens-oldali TRANZAKCIÓ-ARCHÍVUM (új tétel, 2026-08-22)

**A felhasználó felvetése:** tárolják-e a pénztárgépek a saját tranzakcióikat
legalább 10 napig, hogy a szerver egy vészhelyzeti átkapcsolás után **le tudja
kérni és összevetni** őket — így biztosabban elkerülhető az adatvesztés.
Kérdése: **nem lenne túl sok adat?**

#### Az adatmennyiség — BECSLÉS, nem mérés (§4)

> **Ez számított nagyságrend explicit feltevésekből, NEM mért adat.** Valós
> terméktörzs és valós nyugtaprofil mellett újraszámolandó. A feltevések:
> nyugtánként ~4–5 tétel, tömör bináris/JSON alak, forgalmas kassza 500 nyugta/nap.

| Tétel | Becsült méret |
|-------|---------------|
| Egy nyugta feje (időbélyeg, sorszám, kassza, felhasználó, műszak, végösszeg, ÁFA-bontás, fizetési bontás) | ~0,3–0,5 kB |
| Egy tételsor (cikk, mennyiség, egységár, ÁFA-kulcs, kedvezmény, feltétek) | ~0,15–0,25 kB |
| **Egy teljes nyugta** (~4–5 tétellel) | **~1,5–2 kB** |
| **Egy forgalmas kassza napi forgalma** (500 nyugta) | **~1 MB / nap** |
| **10 nap, egy kasszán** | **~10 MB** |
| **10 nap, teljes eseménynaplóval** (nem csak lezárt nyugtákkal) — 5–10× szorzó | **~50–100 MB** |

**Válasz: NEM sok. A tárhely nem korlát** — még a bőkezű, teljes eseménynaplós
változat is elfér egy 64 GB-os SSD-n nagyságrendekkel. **Az akadály tehát nem a
méret, hanem három másik dolog** (lásd lent).

#### `[!]` A LEGFONTOSABB tervezési szabály, amit ez megkövetel

**A kliensen KÉT, egymástól szerkezetileg elkülönített dolog van, és
összekeverésük duplikált adóügyi bizonylatot okoz:**

| | **KIMENŐ SOR (outbox)** | **ARCHÍVUM** |
|---|---|---|
| Mit tartalmaz | Amit a szerver **még nem nyugtázott** | Amit ez a kassza **valaha kiadott**, nyugtázottat is |
| Mi történik vele | **Lejátszandó** a szerverre | **SOHA nem játszandó le automatikusan** |
| Mikor törlődik | Nyugtázás után | N nap után, időalapon |
| Szerepe | Az adat eljuttatása | **BIZONYÍTÉK** összevetéshez |

**Ha az archívumot bárhol vissza lehet játszani írásként, az pontosan azt a hibát
hozza vissza, ami ellen az egész felépítés véd: már lekönyvelt eladások
újrakönyvelését.** Az archívum legyen **szerkezetileg csak olvasható** —
ne csak konvencióból, hanem úgy, hogy a lejátszó kódút hozzá se férjen. §1 szerint
ez **őrt igényel**, nem kommentet.

#### Amit ez ténylegesen MEGVESZ — és ez valódi érték

1. **„Reméljük, nincs hiány" helyett „be tudjuk bizonyítani, mi hiányzik".**
   Egy kemény átvétel után a szerver meg tudja kérdezni: *„2-es kassza, mit adtál
   ki 19:40 és 20:15 között?"*, és összevetheti az adatbázissal. Ez pontosan a §5
   szerinti **pozitív bizonyíték**, szemben a „nem jött hibajelzés" alapú
   következtetéssel.

2. **Egy helyreállítási út, ami eddig NEM létezett.** Ha a halott fő szerver
   lemeze **olvashatatlan** (gyakran pont ezért halt meg), akkor az árva
   tranzakciókat onnan **nem lehet kimenteni** — az A4 kimentési útvonala ilyenkor
   üres kézzel tér vissza. **A kasszák archívuma viszont megvan.** Ez a
   „nulla adatvesztés" ígéretet olyan ágon is közelíti, ahol eddig semmi nem volt.

3. **Rutinszerű ellenőrzés, nem csak katasztrófánál.** Ugyanez az összevetés
   futtatható napi záráskor is: „minden kassza minden nyugtája megvan a
   szerveren?" Ez a §1 értelmében **állandóan futó őr**, nem ritkán érintett ág.

#### A három akadály — mindhárom megválaszolva (2026-08-22), de az első nagyobb lett

**`[ELDÖNTVE + KITERJESZTVE]` B10/a — Adatvédelem**

**A felhasználó válasza NEM csak a kliens-archívumot érinti, hanem az egész
adatvédelmi képet átrajzolja:**

> *„a legtöbb esetben a szerver egy olyan gép lesz, ami egyébként kliens is, tehát
> egy tényleges használatban levő POS. Nagyon kevés hely engedheti meg magának,
> hogy egy irodában tárolt külön szervergépet vegyen és tartson fenn."*

**Ez ELSŐRANGÚ TERVEZÉSI BEMENET, nem mellékmegjegyzés.** Amit átrendez:

1. **A kombinált szerver+kliens szerep nem az egygépes lépcső különlegessége,
   hanem az ÁLTALÁNOS eset minden lépcsőn.** Eddig a B9/a döntés csak az
   egygépes helyre mondta ki; most kiderül, hogy 3 gépes helyen is jellemzően
   az egyik POS lesz a szerver.
2. **Ezzel a legszűkösebb hardveres konfiguráció nem szélső eset, hanem az
   ALAPÉRTELMEZÉS** (lásd B9/a 2. következménye). A teljesítménymérés súlya
   ennek megfelelően nő.
3. **A teljes adatbázis fizikailag a pultban lesz**, nem egy zárt irodában.

**Amit ez az adatvédelemben jelent — őszintén:**

**A fizikai lopás ellen szoftverrel nem lehet teljesen védekezni.** Ha valaki
elviszi a pultból a gépet, elvitte a teljes adatbázist. Ezt ki kell mondani, nem
elhallgatni. Amit tenni lehet, és amit `[ ]` el kell dönteni:

- **Teljes lemeztitkosítás (BitLocker).** `[?]` **IGAZOLATLAN PREMISSZA (§13.5):**
  a felügyelet nélküli, áramszünet után magától induló POS-nak jelszó nélkül kell
  bootolnia, tehát a kulcsot a gépben tárolt **TPM**-hez kellene kötni. **A J1900
  korabeli alaplapokon gyakran NINCS TPM.** Ezt a meglévő bázison **ellenőrizni
  kell**, mielőtt bármit ígérünk — ha nincs TPM, ez az útvonal elesik, és marad a
  gyengébb, jelszó-alapú vagy alkalmazásszintű változat.
- **Adatminimalizálás.** Ez az, ami TPM nélkül is működik: a kliens-archívum
  **ne tartalmazzon személyes adatot, ha nem muszáj** — bizonylat-azonosító,
  időbélyeg, összegek, ÁFA-bontás, fizetési bontás igen; számlázási név/cím és
  törzsvendég-azonosító **csak tokenizálva vagy sehogy**. Kevesebb tárolt adat =
  kisebb kár lopáskor. **Ez tervezési szabály, nem konfiguráció.**
- **Fizikai rögzítés** (zárható ház, Kensington-zár) — **telepítési követelmény**,
  nem szoftver. A telepítési dokumentáció (D2) tétele.
- **A lopás nem csak szivárgás, hanem ADATVESZTÉS is.** Ha a szerverként is
  működő POS-t ellopják, a hely elveszti a teljes adatbázisát → a **felhőmentés
  (D1) itt nem kényelmi funkció, hanem az egyetlen helyreállítási út.**

**`[ ]` Külön eldöntendő, de már nem a B10 alatt:** ha a szerver egy pultban álló
POS, akkor a **Windows-fiókok, a képernyőzár és a fájlrendszer-jogosultságok** is
védelmi vonallá válnak — egy kioszk módból kilépő dolgozó máskülönben hozzáfér az
adatbázis-fájlokhoz. Ez a B6 (kliens↔szerver biztonság) kiterjesztése.

**`[ELDÖNTVE — 20 FORGALMAS nap, nem naptári nap]` B10/b — megőrzési idő**

**Döntés (2026-08-22):** a kliens-archívum **alapértelmezetten 20 napnyi
tranzakciót tart meg**, DE:

- **A megőrzés egysége a FORGALMAS ÜZLETI NAP, nem a naptári nap.** A rendszer a
  legutóbbi **20 olyan üzleti napot** tartja meg, amelyen **tényleges forgalom
  volt**. Egy zárva töltött nap nem számít bele és nem is öregít ki semmit.
- **Miért:** egy három hétre bezáró szezonális hely különben elveszítené a teljes
  archívumát anélkül, hogy egyetlen tranzakció is történt volna. A naptári alapú
  törlés itt pontosan azt semmisítené meg, amiért az archívum létezik.
- **A 10 nappal (licenc offline türelmi idő) SZÁNDÉKOSAN NEM közös érték.**
  A felhasználó megerősítette, hogy nem tervezte összekötni őket; a 20 nap
  mozgásteret hagy. **Két külön, konfigurálható paraméter**, soha nem egy
  konstans (§13.1 hibaosztálya).

**Amit ez megkövetel, és külön ki kell mondani:**
- **A „forgalmas nap" definíciója EGY helyen éljen**, és **ugyanaz legyen, mint a
  logikai üzleti nap** határa (pl. hajnali 04:00) — különben a takarító és a
  riportok más napokat számolnak, és a `[ ]` F4 (két-három párhuzamos
  napzárás-fogalom) hibaosztálya itt is előjön.
- **A NEM NYUGTÁZOTT adatot (a kimenő sort) a megőrzés SOHA nem törli**, kortól
  függetlenül. A megőrzés kizárólag az archívumra vonatkozik.
- **Ha a lemez tényleg megtelik**, az **riasztás**, nem néma takarítás. Nyugtázatlan
  adatot eldobni tilos (§5: ami elmaradt, azt ne jelentsük elvégzettnek).

**`[ELDÖNTVE — a nagy méréssel együtt]` B10/c — írásterhelés**

A felhasználó döntése: **az összes teljesítménymérés az első éles teszt idejére
van ütemezve**, amikor a rendszer kész. **Az írásterhelés is oda tartozik.**
A mérendő tételek egységes nyilvántartása: **`MERESEK.md`** — abban ez a tétel
nevesítve van.

**Kapcsolódik:** A2/b (csökkentett mód és a helyi napló), A4 (visszaállás és az
árva tranzakciók), F1 (idempotencia — az összevetéshez stabil azonosító kell
minden tranzakción), F3 (ki az igazságforrás: a Siduri vagy az adóügyi eszköz —
az archívum ehhez is bizonyítékot ad), A3 (megőrzési kötelezettség).

---

## C) Funkcionálisan hiányzó területek

### `[ ]` C1 — Termék/menü adatmodell
A spec a POS *folyamatait* írja le részletesen, de a **törzsadat-modell szinte
teljesen hiányzik**:
- modifierek és feltétek (kötelező/opcionális választócsoportok, ár-delta),
- menük / combók,
- a „kiszerelés" pontos definíciója (a 9. pont hivatkozik rá, de sehol nincs
  definiálva),
- többszintű receptúra / BOM (félkész termékek),
- allergének,
- nyitott árú tételek,
- **súly szerinti termékek + mérleg integráció** — utóbbi sehol nem szerepel.

### `[ ]` C2 — Árazás
Csak kedvezmények vannak. Hiányzik: happy hour / idősávos ár, zóna szerinti ár
(terasz vs. belső), ár-verziózás (mikortól érvényes), kuponok.

### `[ ]` C3 — `[RÉSZBEN ELDÖNTVE]` ÁFA-mátrix
A „mit égetünk be" kérdés **lezárva**: a MERNOKISAROKKOVEK §13.1–13.3 szerint az
ÁFA-kulcs és a hozzá tartozó besorolás adatvezérelt és dátumozott, soha nem
konstans a kódban.

**Nyitva marad a termékdöntés:** elviteles ÁFA-váltásnál a **bruttó** marad fix
(nettó nő) vagy a **nettó**? A spec 9. pontja bruttó-fixet ír, de érdemes lehet
üzletenként konfigurálhatóvá tenni.

### `[ ]` C4 — Foglaláskezelés (asztalfoglalás)
Egyáltalán nem szerepel egyik doksiban sem. Kell-e? (Tipikus v2 tétel, de dönteni
kell, mert az asztal-adatmodellt érinti.)

### `[ ]` C5 — KIOSK
Szerepel mindkét fogalomtárban, de **nincs saját fejezete és nincs repo hozzá**.
Flutter appként él a `siduri-flutter-clients` alatt?

### `[ ]` C6 — QR-kódos vendégrendelés
Egyetlen sor mindkét doksiban. Nyitott: vendég azonosítása, ki rendelhet melyik
asztalra (visszaélés), és a fizetés — **online fizetés → PSP → internet kell**, ami
ellentmond az offline-first USP-nek. Mi a viselkedés netkimaradáskor?

### `[ ]` C7 — Audit log
Az `event_log` említve van *tárolási* szempontból, de nincs definiálva mint audit:
ki, mit, mikor, **milyen indoklással** (sztornó-ok, kedvezmény-ok, manager
override).

Ellenőrzésnél és lopásgyanúnál ez a legfontosabb funkció, és most a legolcsóbb
beépíteni.

### `[ ]` C8 — Munkaidő-nyilvántartás
Műszak van (14.), de jelenlét/óraszám bérszámfejtéshez nincs. A kártyás borravaló
külön riportálása félig ide mutat.

### `[ ]` C9 — Hűségprogram / törzsvendég
A 6. pont hivatkozik „törzsvendég profilra", a 24. pont „CRM és hűségprogram
API-ra", de nincs adatmodell, és nincs eldöntve: beépített pontgyűjtés, vagy csak
külső integráció?

### `[ ]` C10 — Fiskális sztornó ≠ tetszőleges negatív nyugta
A 13. pont „teljesen új negatív fiskális nyugtát" ír. Az AEE-s gépeknek saját
sztornó/visszáru-szabályaik vannak (mit engednek, milyen hivatkozással) — ezt a
gyártói protokoll dönti el, nem mi. A tényleges protokolldokumentáció ismerete
nélkül ez a fejezet nem tervezhető meg.

### `[?]` C11 — NTAK részletek
Hiányzik: szoftver-regisztráció és tanúsítványkezelés (tárolás, megújítás, több
telephely / több szolgáltatóazonosító), a séma verziója.

**Igazolatlan premissza (§13.5):** a 19. pontban írt 24 órás limit és a 18 órás
riasztás **a spec állítása, nem verifikált tudás.** Hatályos NTAK-dokumentációval
ellenőrizendő, mielőtt bármi épül rá.

### `[ ]` C12 — e-nyugta / NAV nyugtatár
A spec kizárólag AEE-s pénztárgép-vezérlésben gondolkodik (12. pont). A NAV
e-nyugta irány teljesen kimarad mindkét doksiból.

Stratégiai kérdés: most tervezünk rá helyet a bizonylat-modellben (a §13.2 egy
belépési pont miatt olcsó), vagy tudatosan későbbre toljuk?

---

## D) Nem-funkcionális hiányok

### `[ ]` D1 — Backup / restore
A HA **nem** backup — a hibás vagy törölt adat szépen átreplikálódik a Standbyra.
Nyitott: napi mentés hova, mennyi idő a visszaállítás, és mi van, ha mindkét gép
megsemmisül (tűz, lopás)?

### `[ ]` D2 — Telepítés / üzembe helyezés
Hogyan települ a lokális szerver? Windows Service? Docker (J1900-on újabb
memória-teher)? Egy helyszíni telepítés hány óra, és mennyi belőle automatizálható?

### `[ ]` D3 — Verziókompatibilitás
POS v1.2 + szerver v1.4 → mi történik? Kell API-verziózás és „kötelező frissítés"
policy. A `siduri-updater` a *mechanizmust* adja, de a *szabályt* nem.

### `[ ]` D4 — Óraszinkron
Fiskális bizonylatnál kritikus. NTP honnan, ha nincs net? (A lokális szerver mint
időforrás + drift-figyelés.) Kapcsolódik a MERNOKISAROKKOVEK §8-hoz.

### `[ ]` D5 — Hardver-szimulátorok
Fiskális nyomtató, bankterminál, NTAK, ESC/POS — mind külső rendszer. **Ezek nélkül
nem lehet CI-t és automata tesztet építeni** (§1: az őr annyit ér, amennyit mér).

Ez egy komoly, külön betervezendő tétel (mock/simulator harness), ami egyik
doksiban sem szerepel.

### `[ ]` D6 — Licenc-lejárat viselkedése
10 nap grace után **mi történik?** (19. pont nem mondja meg.) Ha leáll a kassza, az
üzletileg és jogilag is vállalhatatlan: a vendéglős a mi hibánkból nem tud
bizonylatot adni.

Javaslat: fokozatos degradáció (banner → admin/riport funkciók zárolása), de **az
eladás sosem áll le**. Plusz hiányzik: alaplap-/hardvercsere → offline
újraaktiválási útvonal.

### `[ ]` D7 — Lokalizáció és pénznem
Magyar-only, vagy angol/német UI is (turisztikai helyek, külföldi személyzet)?
A QR-menü többnyelvű? Az EUR/HUF váltás a visszajárónál említve (14.) — teljes
multi-currency, vagy csak készpénzes EUR-elfogadás napi árfolyammal?

Ha többnyelvű: a MERNOKISAROKKOVEK §8 fordítási szabályai azonnal élesek.

---

## E) Scope és folyamat

### `[ ]` E1 — Mi az MVP valójában?
A 3. pont négy sort jelöl MVP-nek, de a maradék 22 fejezet nincs fázisokba sorolva.
Így ez egy több éves program.

Javaslat: **3 szintű fázisterv** — „első fizető ügyfél" → v1 → v2 —, és minden
fejezet kap egy címkét.

#### Megállapított tény (2026-08-22)
**Nincs konkrét, névre szóló első fizető ügyfél.**

Ez nem hiányosság, hanem **tervezési bemenet**, és explicit feltételezésként kell
kezelni (§2.1: a saját indoklásom premisszáját is igazolni kell). Következménye:
az MVP-t nem lehet egy valós ügyfél igényeire szabni, tehát **a legkisebb hiteles
egységre** kell szabni — az adja legelőbb a valós visszajelzést.

**Munkafeltételezés (felülvizsgálandó, amint van ügyfél):** a célprofil egy
**kis bár / büfé, 1–2 pénztárral, pincér nélkül** — gyorseladás, nyugta, műszak,
NTAK. Asztaltérkép, PDA, KDS, számlabontás **nincs** benne.

#### `[ ]` NYITVA — a fázisterv maga
A fázisterv **még nincs megírva**. Ez a következő nagy tétel: mind a 26 fejezet
kapjon címkét (MVP / v1 / v2), a fenti munkafeltételezés mentén.

**Függőség:** a B1 kimenetele érdemben befolyásolja (ha az Emergency Server
kikerül az MVP-ből, az több hét különbség), ezért **a B1 lezárása után** érdemes
megírni, ne előtte.

### `[ELDÖNTVE — kis csapat, 2–3 fő + AI-asszisztencia]` E2 — Ki fejleszti?
Egyedül, vagy csapat? Ez dönti el, hogy az 5 repót lehet-e párhuzamosan vinni, vagy
szigorúan szekvenciálisan kell.

**Döntés (2026-08-22):** 2–3 fős csapat, AI-asszisztenciával.

**Következmények:**
- **Repónkénti felelős lehetséges** → a repók párhuzamosan vihetők.
- **Ezért a B8 nem opcionális.** Ha három ember három repóban dolgozik három
  nyelven, a kézzel szinkronban tartott API-szerződés **garantáltan** szétcsúszik
  (§6). Az API-szerződés + generált SDK-k + paritás-őr az **első hét** tétele,
  nem „majd később".
- **A kereszt-repós szkennerek (§6) is előre kerülnek** — egyik repó tesztjei sem
  látják a másikat, tehát a varratot csak külön mérő eszköz védi.
- **§9 (harness-higiénia) élesedik:** párhuzamos ügynökök/fejlesztők ugyanarra a
  repóra mutációs futás alatt tilos; a részeredmény commitolva ÉS pusholva (§10).

### `[ ]` E3 — Hardver-beszerzés mint blokkoló
Nem fejlesztési, hanem **beszerzési** feladatok, amik hetekig tarthatnak, és amíg
nincsenek meg, a C10 / 12. fejezet nem tervezhető:
- Micra / CashCube protokolldokumentáció (NDA-hoz kötött),
- bankterminál-protokoll (NEXO vagy gyártóspecifikus),
- NTAK teszt-környezet regisztráció,
- PSP/acquirer szerződés a SoftPOS-hoz (lásd B5).

Érdemes ezeket a kódolással **párhuzamosan** elindítani.

---

## F) Kiegészítések — a 2026-08-22-i átbeszélésen felvett tételek

> Ezek nem szerepeltek az A–E listákban. Mindegyik **most olcsó, később drága**:
> mindegyik az adatmodellt vagy egy varratot érint, tehát utólag beépíteni
> az egész felületet átírja.

### `[ ]` F1 — Idempotencia-kulcs minden kliens-írásra
A spec csak egy félmondatot szán rá („védelem dupla felütés ellen", HU 17.).
Ingadozó wifin az **újraküldés a normális eset, nem a kivétel**: a kliens elküldi a
tételt, a válasz elveszik, a kliens újrapróbál — és a vendég két sört kap a
számlájára.

Ezt szerver-oldali „ügyeskedéssel" (időablak + hasonlóság) nem lehet megoldani,
mert a **legitim** dupla felütés (a vendég tényleg kért még egy sört) és a
hálózati duplikátum megkülönböztethetetlen. Egyetlen megoldás: **kliens-generált
idempotencia-kulcs**, amit a szerver egyediségi megszorítással érvényesít.

Kapcsolódik §7-hez: *foglalj előbb, hozz létre utána* — a kulcsot a mellékhatás
ELŐTT kell rögzíteni, különben két párhuzamos kérés mindkettő végigmegy.

Ez az API-szerződés (B8) része, tehát **mind a három kliensnyelvben** azonos
szemantikával kell megjelennie.

### `[ ]` F2 — Pénz- és mennyiség-reprezentáció (sehol nincs kimondva)
Egyik doksi sem mondja meg, milyen típusban él a pénz. Rögzítendő:
- **Pénz: egész, minor-unit alapú** (fillér vagy forint — el kell dönteni, a HUF-nál
  a fillér nem forgalmi, de az arányos kedvezmény-elosztás (13.) belső pontosságot
  igényel). Lebegőpontos SOHA.
- **Mennyiség: decimális, nem egész** — 3 dl, 0,42 kg (C1 súly szerinti termékek).
- A `mennyiség × egységár` **kerekítése egy nevesített helperen** menjen át (§13.2),
  és a szabály dátumozott legyen (§13.3).

**Miért most:** a beégetett kerekítés nem EGY hiba, hanem egy hibaosztály (§3.1),
ami szétszóródik a kódbázison. A 13. pont arányos kedvezmény-elosztása +
5 Ft-os kerekítés + vegyes ÁFA együtt a legkockázatosabb számítás az egész
rendszerben — erre §13.4 szerint **arany-minta teszt kell**, jogszabályi
hivatkozással.

### `[ ]` F3 — Ki az igazságforrás: a Siduri bizonylat-entitása vagy az AEE naplója?
A spec az adóügyi eszközt **perifériaként** kezeli (12.), de az AEE a **jogi
bizonylat kiállítója és sorszámozója**. A kettő szétcsúszhat:
- áramszünet nyomtatás közben,
- papírelakadás a fiskális parancs után,
- a Siduri elküldte a parancsot, de a választ nem kapta meg.

Ilyenkor **kiment a bizonylat vagy nem?** Ha a Siduri-oldali rekordot tekintjük
igazságnak, hamis nyugtát könyvelünk; ha az AEE-t, akkor az összes riport,
NTAK-küldés és készletmozgás a fiskális eszköz állapotától függ.

Ez tiszta §5 néma kudarc: **jól néz ki, és évek múlva egy ellenőrzésen derül ki.**
Kell egy explicit egyeztetési (reconciliation) folyamat és egy „függő tranzakció"
állapot, aminek a feloldása **pozitív bizonyítékon** áll (§5), nem a hibajelzés
hiányán.

Kapcsolódik: C10, B4, D5.

### `[ ]` F4 — Két, egymástól független „napi zárás"
A rendszerben **két** napzárás-fogalom él, és a spec nem köti össze őket:
- **NTAK napi zárás** (HU 14., EN 14.) — aszinkron forgalmi/ÁFA-összesítő,
- **az adóügyi eszköz saját napzárása** — a gyártói protokoll szabálya szerint.

Plusz egy harmadik: a **logikai üzleti nap** határa (pl. hajnali 04:00), ami a
műszakokat fogja össze.

§8 szabálya kimondottan erre való: *ha egy szerződés két, egymástól függetlenül
elállítható kapcsolón nyugszik, legyen INDULÁSI ÁLLÍTÁS, ami hangosan szól.*
A fél-teljesülés (az egyik lezárt, a másik nem) néma csúszást ad, amit senki nem
vesz észre, amíg a havi összesítő el nem tér.

### `[ ]` F5 — Támogathatóság / megfigyelhetőség (egyik doksiban sincs)
Péntek este 20:00-kor csörög a telefon: „nem megy a kassza". **Hogyan látja a
support, mi történt?** Jelenleg sehogy — ez a terv teljes vakfoltja.

Szükséges, és a fázistervben nevesítendő:
- strukturált naplózás + naplógyűjtés (mennyi ideig, hol, GDPR-kompatibilisen),
- **diagnosztikai csomag** egy gombra (verziók, konfiguráció, utolsó N esemény,
  periféria-állapot),
- távoli hozzáférés útvonala és annak **jogosultsági/audit szabálya** (a
  szuperfiók, 10. pont, itt lesz veszélyes),
- a §5 szerinti gépi hibakódok: a „minden null" visszatérés a hívónál
  megkülönböztethetetlenné teszi a titok-rotációt, a leállt szolgáltatást és a
  valóban hiányzó adatot.

KKV-nak eladott termékben ez nem „nice to have", hanem üzemeltetési alapkövetelmény.

### `[ ]` F6 — Demó / teszt üzemmód
Értékesítési bemutatóhoz és oktatáshoz kell, de **bizonyíthatóan lehetetlenné kell
tenni, hogy demó módból éles fiskális bizonylat menjen ki** — és fordítva, hogy
éles üzemben demó-bizonylat képződjön.

Ez §5 „a felület ne kínáljon olyat, ami nem működik" osztálya, fordítva: a felület
ne engedjen olyat, aminek adóügyi következménye van. Őr kell rá (§13.4), nem
csak konvenció.

### `[ ]` F7 — A jogosultsági modell konkrét alakja
A 10. pont „extrém granuláris, gomb- és végpontszintű" jogköröket ír. Ez önmagában
**figyelmeztető jel**: elnevezési séma és **egy** kikényszerítő helper nélkül a
kapuk garantáltan szétcsúsznak (§3.5 — kimért eset: egy jogosultsági kapu két
végponton, csak az egyik kapuzva).

Rögzítendő a kód előtt:
- a jogosultság-azonosítók **elnevezési sémája** és hol él a kanonikus lista
  (az API-szerződés része, B8),
- **egy** kikényszerítő belépési pont szerver-oldalon,
- a UI-elrejtés **nem** kikényszerítés (B6-tal átfedésben),
- a Role + Override feloldási sorrend egyértelmű szabálya (mi nyer ütközéskor),
- a szuperfiók (10.) hatóköre és auditálása (F5-tel átfedésben).

---

## Amit a kód előtt el kell dönteni (prioritás)

**Állapot a 2026-08-22-i 2. munkamenet után:** nyolc tétel eldöntve.
**EGYETLEN blokkoló maradt a fázisterv előtt: a B1/c.**

| # | Tétel | Státusz | Miért blokkoló |
|---|-------|---------|----------------|
| 1 | **B1/b ellentmondás** | `[ ]` **NYITVA — tisztázandó, nem találgatható** | A tartalék szerver **dedikált** gép, vagy — a „kevés hely vesz külön szervergépet" logika szerint — szintén egy dolgozó pénztárgép? A második esetben ugyanaz a J1900 viszi a WPF klienst, a másodkijelzős videót ÉS a PostgreSQL replikát. |
| 1b | **B10/a maradéka** | `[ ]` **NYITVA** | Van-e TPM a meglévő J1900 bázison? Enélkül a felügyelet nélkül induló POS-on a teljes lemeztitkosítás útvonala elesik, és marad az adatminimalizálás + fizikai rögzítés. |
| 1b | **R1 lépcsőnként** | `[ ]` **NYITVA** — jóváhagyásra | A tanú-séma lépcsőnkénti alakja a B9/b tisztázása után megírva; a felhasználó jóváhagyására vár. |
| 2 | **B1/c R2–R5** | `[ ]` **NYITVA** — R6 megerősítve; az R1 lépcsőnként megírva, jóváhagyásra vár | A kétlépcsős failover végrehajtási részletei: ki a tanú (és mi van egypénztáras helyen), miből ismeri fel a gép hogy Ő esett ki, az 5 perc paraméterezése és az ajánlat lejárata, több egyidejű gombnyomás, élő-de-elérhetetlen fő szerver, és hogy ne ajánljunk fel működésképtelen átkapcsolást. |
| 3 | **E1** | `[ ]` **NYITVA** — a fázisterv még nincs megírva | Mi az MVP scope-ja? Enélkül nincs mihez mérni a haladást. **Az A4 után** írandó. |
| — | ~~A1~~ | `[ELDÖNTVE]` | WPF, Windows 10 IoT Enterprise LTSC only. |
| — | ~~A2~~ | `[ELDÖNTVE]` | Szerver-autoritatív + degradált gyorseladás. **Feltételes**: igazolatlan AEE-premisszán áll. |
| — | ~~A2/a~~ | `[ELDÖNTVE]` | Kettős kieséskor a nyitott asztalok nem elérhetők → kézi újrafelütés. |
| — | ~~A2/b~~ | `[ELDÖNTVE]` | A degradált gyorseladás **mindhárom része** (helyi napló, degradált felület, visszatéréskori egyeztetés) az MVP-ben van. |
| — | ~~B1/a~~ | `[ELDÖNTVE]` | A vészhelyzeti szerver / HA **BENNE MARAD az MVP-ben** (az ajánlással szemben, tudatosan). Következmény: min. 2 dedikált gép telepítésenként → E1-ben árazandó. |
| — | ~~A4/b~~ | `[ELDÖNTVE]` | Billegés-védelem: **növekvő várakozás** minden visszaállás után + **leállási határ**, ami után az automatika kikapcsol és hangosan szól. A konkrét X/Y érték mérendő. |
| — | ~~A4/c~~ | `[ELDÖNTVE]` | A szerepcsere **azonnal** megtörténik, ahogy stabil — nincs csendes ablakra halasztás. A csúcsidő-terhelést a billegés-védelem zárja ki, nem az időzítés. |
| — | ~~B10/a~~ | `[ELDÖNTVE + KITERJESZTVE]` | **A szerver jellemzően egy dolgozó pénztárgép lesz** → a teljes adatbázis a pultban áll. A fizikai lopás ellen szoftverrel nem lehet teljesen védekezni; ki kell mondani. Amit tenni lehet: **adatminimalizálás** (tervezési szabály), lemeztitkosítás ha van TPM, fizikai rögzítés (telepítési tétel), és a felhőmentés mint EGYETLEN helyreállítási út lopás után. |
| — | ~~B10/b~~ | `[ELDÖNTVE]` | **20 FORGALMAS üzleti nap** megőrzése, nem 20 naptári nap — egy zárva töltött nap nem számít bele és nem is öregít ki semmit. A licenc 10 napos türelmi idejével **szándékosan nem közös érték**. A nyugtázatlan adatot a megőrzés soha nem törli. |
| — | ~~B10/c~~ | `[ELDÖNTVE]` | Az írásterhelés az első éles teszt nagy mérésének része → `MERESEK.md` M8. |
| — | ~~B9/b~~ | `[ELDÖNTVE]` | A gépszám-szabály a **TARTALÉK SZERVERRE** vonatkozik: 2–3 gépnél opcionális, 4+ gépnél kötelező. Következmény: a „nincs tartalék szerver" **elsőrangú konfiguráció**, nem hibaállapot — ott átkapcsolást felajánlani sem szabad. |
| — | ~~B9/a~~ | `[ELDÖNTVE]` | **Egygépes helyen a pénztárgép MAGA a szerver.** Ezzel a B3 nyitott kérdése (futhat-e egy gépen szerver és kliens) eldőlt: **igen, támogatott konfiguráció**. Következmény: ez a legszűkösebb hardveres eset, és ott nincs hardverhiba-védelem. |
| — | ~~Személyzeti üzenetek~~ | `[ELDÖNTVE]` | Három üzenet (a szerver gyanús / ez a gép a hibás / bizonytalan), „hálózat" szóhasználattal, plusz külön jelzés az internet hiányára. Tartalmilag jóváhagyva; a design-körben csak a megjelenés csiszolható. |
| — | ~~A4~~ | `[ELDÖNTVE]` | **A visszaállás AUTOMATIKUS**, ha a fő és a tartalék 1 percig stabilan látják egymást és beszélnek is. A régi spec „csak szuperfiókkal" szabálya ELVETVE. **DE:** az árva tranzakciók KIMENTÉSE kötelező és automatikus, a KÖNYVELÉSÜK viszont nem lehet automatikus (duplikált adóügyi bizonylat kockázata). |
| — | ~~A4/a~~ | `[ELDÖNTVE]` | **Tiszta vs. kemény átvétel** külön útvonal. Tiszta átvételnél (a régi fő él és elérhető a tartalék felől) a tartalék az átvétel ELŐTT leszívja a nem replikált tranzakciókat → tényleg nulla veszteség. Keményénél az árvák elkerülhetetlenek. |
| — | ~~B1/c K1~~ | `[ELDÖNTVE]` | **Minden gép ÖNÁLLÓAN megy csökkentett módba**, akkor is, ha a többi működik. A csökkentett mód gépenkénti állapot, nem a helyé. |
| — | ~~B1/c~~ | `[ELDÖNTVE]` | **Kétlépcsős failover:** a pénztárgép azonnal, látványosan jelzi a csökkentett módot és megmondja mit ellenőrizzenek; átkapcsolást csak 5 perc után ajánl fel; a gombot EMBER nyomja meg; és a gépnek fel kell ismernie, ha Ő esett ki a hálózatról. |
| — | ~~B1/b~~ | `[ELDÖNTVE]` | A tartalék szerver **szintén J1900**, dedikált. Munkafeltevés: **aszinkron** replikáció; a „szinkron kizárt" állítás **még nincs mérve** (§4). Az „automatikusan szinkronról aszinkronra váltó" ág **elvetve** (§5 néma kudarc). |
| — | ~~B3~~ | `[ELDÖNTVE]` | J1900 vegyes bázis (szerver ÉS kliens) → GraalVM kényszer marad, plusz szoros WPF perf-költségvetés. |
| — | ~~E2~~ | `[ELDÖNTVE]` | 2–3 fős csapat + AI → B8 az első hét tétele. |

**Az A4 (failback) a B1/c-vel EGYÜTT dőljön el** — ugyanaz a mechanizmus.

**Az epoch-mező (fencing) mostantól nem elővigyázatosság, hanem KÖVETELMÉNY**, mert
a failover ténylegesen megépül az MVP-ben. Lásd B1/a és a történeti javaslatblokk
3. pontja.

### Kódolás előtti, IGAZOLANDÓ premisszák (§13.5)
Ezekre **döntés nem építhető** forrás nélkül. Egyik sem verifikált tudás, mindegyik
a spec állítása vagy emlékezetből írt feltevés:

| Tétel | Az igazolatlan állítás | Mi dől meg, ha hamis |
|-------|------------------------|----------------------|
| **A2** | AEE-s gépnél a jogi bizonylatot maga az adóügyi eszköz állítja ki és sorszámozza → a szerver kiesése nem akadálya a nyugtaadásnak | A degradált mód egésze (A2) |
| **A3** | A számviteli megőrzési idő (8 év?) | A 30 napos purge és a „tisztán lokális" topológia egyszerre |
| **C10** | „Teljesen új negatív fiskális nyugta" sztornóra | A teljes sztornó-folyamat (13.) |
| **C11** | 24 órás NTAK adatszolgáltatási limit, 18 órás riasztás | A 19. pont SLA-figyelmeztetése |
| **C12** | Az e-nyugta iránnyal most nem kell foglalkozni | A bizonylat-modell alakja |
