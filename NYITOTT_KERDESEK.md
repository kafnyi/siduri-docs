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
> **ÚJ (hetedik kör):** a szerepkiosztás tisztázva — **a tartalék MINDIG Windows POS-on van,
> soha nem dedikált gépen**; vékonykliens/KDS/kijelző egyiket sem viheti. Négy új
> következmény rögzítve (tartalék terhelése failovernél, a gép kikapcsolhatósága, Windows
> Service kényszer, frissítési sorrend).
> **ÚJ (nyolcadik kör):** a méret-lépcső **értékesítési ajánlás, nem kikényszerített
> korlát**; öt támogatott telepítési kombináció rögzítve. Élesen kimondva: a csökkentett
> mód **nem véd minden lépcsőn** — az „1 POS = szerver + sok vékonykliens" konfiguráció
> teljesen védtelen, nem „kicsit kevésbé védett".
> **ÚJ (kilencedik kör):** **B12** — kockázatvállalási nyilatkozat aláírással és felhőbe
> továbbítva (ELDÖNTVE); **B11** — a tanú-séma teljes terve megírva (JÓVÁHAGYÁSRA VÁR);
> TPM: mindkét ágra készülünk, az ellenőrzés folyamatban.
> **NYITVA maradt (egyik sem blokkolja a fázistervet):** B11 jóváhagyása, a TPM-ellenőrzés
> eredménye, a B12 jogi kérdése, a B1/c R2–R5 kitöltése.
> **A FÁZISTERV (E1) MOST MÁR MEGÍRHATÓ.**
>
> **ÚJ (tizenkettedik kör):** a bizonylatszám **végleges formátuma** rögzítve
> (`xxxxxxyyyzzzzz` — üzleti nap + eszköz + napi folyószám); ez **mindkét korábbi
> aggályomat megoldja** (kimerülés, rendezés). **HELYESBÍTÉS: az én érvem az adóügyi
> szám ütközéséről HIBÁS volt** — a napszámláló 4 jegyű, nem 3; a saját számozás
> viszont más okból továbbra is kötelező. **B14.7** — offline üzleti nap nyitása:
> a javasolt „+1 nap" szabály minden zárvatartási napon hamisan riasztana, helyette
> **monotonitás-védelem**. **ÚJ HÉZAG:** két gép offline, eltérő órával, két külön
> üzleti napot nyit. **B16** — távoli konfiguráció a felhőből (új tétel).
> A telefon az első verzióban nem fizettet és nem ad nyugtát.
>
> **A felhasználó két ELLENŐRZŐ KÖRT kért a jelenlegi tervekre** — lásd
> `FOLYAMATBAN.md` 2.1.c és 2.1.d szakasz.
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

> ### `[TISZTÁZVA 2026-08-22]` A „dedikált" szó pontosítása — a tartalék SOHA nem dedikált
>
> A fenti „dedikált gépként" megfogalmazás **pontatlan volt**, és a felhasználó
> tisztázta. A **helyes** szabály:
>
> | Szerep | Hol fut |
> |--------|---------|
> | **Fő szerver** | **Jellemzően egy Windows POS vastagkliensen.** Aki megengedheti magának, annál lehet **dedikált** gépen. |
> | **Tartalék (vészhelyzeti) szerver** | **MINDIG egy Windows POS vastagkliensen. SOHA nem dedikált gép** — ez csak vészhelyzeti szükségmegoldás, nem éri meg rá gépet venni. |
> | Vékonykliens (tablet, telefon), KDS, rendeléskijelző | **SOHA nem viheti egyik szerepet sem.** |
>
> **A felhasználó példája, szó szerint** (ezt tartsuk meg referencia-telepítésként):
> egy étteremben van **3 Windows POS** (vastagkliens), **2 tablet**, **4 telefon**
> (vékonykliensek), **1 KDS**, **1 rendeléskijelző**. Ekkor: az **egyik Windows POS
> a fő szerver**, a maradék kettő **egyike a tartalék szerver**. A vékonykliensek,
> a KDS és a rendeléskijelző egyiket sem viheti.

**`[!]` NÉGY KÖVETKEZMÉNY, amit ez a tisztázás azonnal teremt**

**(1) A tartalék gép terhelése a LEGROSSZABB pillanatban ugrik meg — és ezt eddig
senki nem nézte meg.** A tartalék egy **dolgozó pénztárgép**: közben a WPF kliens
fut rajta, a pénztáros ott üt fel. Amikor átveszi a szolgálatot, **ugyanaz a
J1900 hirtelen elkezdi kiszolgálni az összes többi kasszát, a vékonyklienseket, a
KDS-t, a nyomtató-útvonalakat — miközben tovább kell pénztárgépként is működnie.**

**És ez pontosan a legrosszabb pillanatban történik:** a szerver akkor esik ki,
amikor a hely dolgozik. **Ez a rendszer legkritikusabb mérése**, mert ha a
tartalék nem bírja, akkor a failover **rosszabbá teszi a helyzetet, nem jobbá** —
egy lassú, akadozó rendszer minden kasszán, egy gyors csökkentett mód helyett.
→ `MERESEK.md`, M12.

**(2) A szerepet vivő gépet valaki KIKAPCSOLHATJA.** Egy hátsó irodában álló
szervergéphez senki nem nyúl. Egy pultban álló pénztárgépet a záró műszak
**lekapcsol**, mert nem tudja, hogy az a szerver. Ez a hibaosztály **nem létezett
eddig, és nagyon olcsó megelőzni:**
- a szerepet vivő gép **láthatóan jelezze magán**, hogy ő a fő szerver / a
  tartalék (állandó, nem eltüntethető jelzés a felületen);
- **leállítás/újraindítás onnan figyelmeztetéssel és jogosultsághoz kötve**
  történjen, ne egy sima Windows-leállítással;
- a leállítás előtt mondja meg, **hány másik eszköz függ tőle éppen.**

**(3) A szerver NEM futhat a pénztáros munkamenetében — Windows Service kell.**
A pénztárgép teljes képernyős kioszk módban fut, felhasználói munkamenetben. Ha a
szerver ugyanabban a munkamenetben futna, akkor **egy kijelentkezés, egy
felhasználóváltás vagy egy képernyőzár megölné a szervert az egész helyen.**
Tehát: **a szerver és a replika Windows Service-ként fut**, a bejelentkezett
felhasználótól függetlenül. Ez a telepítési tétel (D2) kemény követelménye, és
egyben biztonsági kérdés is (a service fiókja ne legyen a pénztáros fiókja).

**(4) A FRISSÍTÉS sorrendje kritikussá vált — ez a `siduri-updater` repó
követelménye, ami eddig sehol nem szerepelt.** Ha a pénztárgép-klienst frissítjük
azon a gépen, ami egyben a szerver, akkor **a frissítés az egész helyet leállítja.**
A frissítőnek **ismernie kell a szerepeket** és sorrendben kell dolgoznia:
először a tartalékot, majd átkapcsolás, majd a régi főt, majd vissza. Ez nem
apró: a frissítő így **függ a failover-mechanizmustól**, tehát a kettőt együtt
kell tervezni.

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
| **2–3 gép** | A fő szerver egy POS-on (vagy dedikált gépen); a tartalék MINDIG egy POS-on | **Nem kötelező, de LEHETŐSÉGKÉNT fenntartva** |
| **4+ gép** | Ugyanaz | **KÖTELEZŐ** |

> ### `[ELDÖNTVE 2026-08-22]` A lépcső AJÁNLÁS, nem kikényszerített korlát
>
> **A hézag feloldva.** A gépszám-lépcső **értékesítési ajánlás**, nem olyan
> szabály, amit a szoftver kikényszerít. A felhasználó döntése:
>
> - **Ha egy helynek kellene tartalék, de nincs hova tenni** (csak egy Windows POS
>   van, és az a fő szerver), akkor **már az ajánlatban dedikált szervergépet
>   javaslunk.** A dedikált szerver **nem üzemel POS-ként**, így ha van mellette
>   akár egyetlen Windows POS, az el tudja látni a tartalék szerepet.
> - **Ha az ügyfél ezt a kockázat ismeretében elutasítja** (pl. „nekem elég egy
>   POS szervernek, mellé 10 vékonykliens"), **elfogadjuk a döntését.**
>   Marad a csökkentett mód, tartalék nélkül.
> - **Fordítva ugyanígy:** ha egy 2 POS-os hely kéri a tartalékot, **megcsináljuk**,
>   akkor is, ha a lépcső szerint nem lenne kötelező.
>
> **Mérnöki következmény: a szoftver SEMMILYEN konfigurációt nem utasíthat el.**
> Támogatnia kell: tartalék nélküli és tartalékos működést, POS-on futó és
> dedikált gépen futó fő szervert, tetszőleges vékonykliens-számmal. A lépcső az
> ajánlatban él, nem a kódban.

#### `[!]` De az „informált kockázatvállalás" csak akkor ér valamit, ha BIZONYÍTÉK van rá

A felhasználó megfogalmazása — *„az ügyfél elfogadta a kockázatot, minden
információ tudatában"* — **jogilag és üzletileg is csak akkor véd, ha rögzítve
van.** §5 hibaosztálya, megfordítva: **a panasz hiánya nem bizonyíték a
tájékoztatásra.** Amikor a hely két napra megáll, és azt mondják, hogy „nekünk
ezt senki nem mondta", egy nyolc hónappal korábbi értékesítési beszélgetés
semmit nem ér.

**`[JAVASLAT — jóváhagyásra]` Ezért a kockázatvállalás legyen ADAT, ne beszélgetés:**
- **A telepítés rögzítse a konfigurációban**, hogy ezen a helyen **nincs tartalék
  szerver**, mikor, és **ki tájékoztatta** az ügyfelet erről.
- **Az adminisztrációs felület állandóan mutassa a hely védelmi szintjét**
  („ezen a helyen nincs tartalék szerver — szerverhiba esetén a védelem: a
  csökkentett mód, illetve mentésből visszaállítás"). **Ne legyen elrejtve** egy
  beállítási almenüben.
- Ez egyben **támogatási eszköz** is: pénteken este a support első kérdése az,
  hogy „mi van ezen a helyen telepítve" — és ez legyen egy lekérdezés, ne egy
  telefonhívás.

#### `[!]` FONTOS PONTOSÍTÁS: a csökkentett mód NEM véd minden lépcsőn

Ezt élesen ki kell mondani, mert a „marad a csökkentett mód" mondat **nem
mindenhol igaz.** A csökkentett gyorseladás csak azokat a Windows POS gépeket
védi, **amelyek NEM a szerverek.**

| Telepítés | Mi történik, ha a fő szerver meghal (tartalék nélkül) |
|-----------|------------------------------------------------------|
| **1 Windows POS = szerver**, mellé vékonykliensek | **SEMMILYEN védelem.** A gép halott, tehát a rajta futó csökkentett mód is halott. A vékonykliensek terv szerint leállnak. **A hely megáll.** |
| **2+ Windows POS**, egyikük a szerver | A többi POS csökkentett módban **eladhat**. A vékonykliensek leállnak. |
| **Dedikált szerver + N Windows POS** | **MINDEN POS csökkentett módban eladhat** — egy POS sem vész el a szerverrel együtt. **Itt a legnagyobb a csökkentett mód haszna.** |

**Ez az értékesítési beszélgetés lényege:** a „1 POS + sok vékonykliens"
konfiguráció nem „kicsit kevésbé védett", hanem **teljesen védtelen**. Ha az
ügyfél ezt vállalja, rendben — de pontosan ezt kell elmondani neki, nem azt,
hogy „marad a csökkentett mód".

#### A támogatott telepítési kombinációk — a konfigurációs modellnek MINDET vinnie kell

| # | Fő szerver | Tartalék | Csökkentett mód haszna |
|---|-----------|----------|------------------------|
| **A** | egyetlen Windows POS-on | nincs (nincs hova) | **nulla** |
| **B** | egy Windows POS-on | másik Windows POS-on | a többi POS védve |
| **C** | egy Windows POS-on | nincs (ügyfél elutasította) | a többi POS védve |
| **D** | **dedikált gépen** (nem POS) | egy Windows POS-on | **minden POS védve** |
| **E** | **dedikált gépen** (nem POS) | nincs (ügyfél elutasította) | **minden POS védve** |

**A dedikált szerver teljesítményprofilja MÁS** (nem viszi a WPF klienst és a
másodkijelzős videót), tehát a `MERESEK.md` M1 tétele **nem érvényes rá** — az a
kombinált esetet méri. A dedikált eset enyhébb, de attól még mérendő.

**`[ELDÖNTVE]` B9/a — az egygépes hely: a pénztárgép maga a szerver.****`[ELDÖNTVE]` B9/a — az egygépes hely: a pénztárgép maga a szerver.**
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

- **Teljes lemeztitkosítás (BitLocker).** `[ELDÖNTVE — MINDKÉT ÁGRA készülünk]`
  A felhasználó (2026-08-22): *„egyelőre még nem tudom megmondani, készüljünk fel
  mindkét alternatívára, de a napokban ezt majd ellenőrzöm és pontosítom."*
  **Tehát a terv nem feltételezhet TPM-et, de nem is zárhatja ki:** a
  titkosítás legyen **konfigurációs képesség**, amit a telepítő a gépen talált
  adottságok szerint kapcsol be, és az admin felület **írja ki, melyik ágon
  vagyunk** („ezen a gépen a lemez titkosítva / NINCS titkosítva"). §5: ne
  hallgassuk el, ha nincs védelem.
  `[?]` **IGAZOLATLAN PREMISSZA (§13.5), ellenőrzés alatt:**
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

### `[ELDÖNTVE — kétrétegű számozás]` B14 — BIZONYLAT-SZÁMOZÁS

> **A felhasználó döntése és pontosítása (2026-08-22).** Ez a tétel egyik eredeti
> doksiban sem szerepelt, és **a rendszer egyik legmeghatározóbb szerkezeti
> döntése** — az adatmodellt, a szinkronizációt és a sztornót egyaránt érinti.

#### B14.1 A két, egymástól FÜGGETLEN szám

| | **SIDURI bizonylatszám** | **ADÓÜGYI ESZKÖZ száma** |
|---|---|---|
| Ki adja | **Mi** — a kiállító eszköz, saját, elhatárolt tartományból | **Az adóügyi nyomtató**, a saját szabályai szerint |
| Alakja | eszközazonosító-előtag + folyószám (pl. a 2-es kassza: `002xxxxx`) | `A12345678/123/1234` |
| Mikor keletkezik | **a bizonylat létrehozásakor**, azonnal, helyben | **csak a nyomtatás után**, válaszként |
| Mire jó | **ez a mi elsődleges azonosítónk** mindenre | **a sztornóhoz KELL** — enélkül nem hivatkozható |
| Mi van, ha nincs | nem fordulhat elő | **gyakran nincs** — lásd B14.4 |

**Az adóügyi szám formátuma** (a felhasználó **javított** megadása, 2026-08-22):
`Axxxxxxxxx/yyyy/zzzzz` — `A` fix karakter, `xxxxxxxxx` az **AP-szám** (a nyomtató
NAV-os azonosítója), `yyyy` a **zárás száma / munkanap-azonosító**, `zzzzz` a
**nyugta száma** az adott nyomtatón, az adott munkanapon.

---

#### `[!]` HELYESBÍTÉS — az ÉN korábbi érvem volt HIBÁS (§2.1)

**Egy előző körben azt írtam, hogy a munkanap-számláló 3 jegyű, tehát ~2,7 év
után körbefordul és ütközést okozhat. EZ TÉVEDÉS VOLT.** A felhasználó
utánanézett és pontosított: a számláló **4 jegyű**.

**Számolva a helyes formátummal:** 4 jegy = 9999 zárás; napi egy zárással
**~27 év** üzem. Napi 99 999 nyugta egy nyomtatón. **Gyakorlati ütközés nincs.**

**Ez §2.1 tanpéldája: a saját indoklásom premisszáját ugyanúgy igazolni kellett
volna, mint a leletet.** Egy megadott formátumot vettem készpénznek, számoltam
belőle, és a számítás — bár aritmetikailag helyes volt — **rossz bemenetre
épült**, tehát a következtetés hamis. A hiba nem a számolásban volt, hanem
abban, hogy nem kérdeztem vissza a formátumra.

**Mi dől meg, és mi NEM dől meg ettől:**

| Érv arra, hogy ne az adóügyi szám legyen a mi azonosítónk | Állapot |
|---|---|
| ~~1. A napszámláló körbefordul → ütközés~~ | **MEGDŐLT.** Nincs gyakorlati ütközés. |
| 2. Nem mi vezéreljük (csere, szerviz, memóriatörlés a tudtunk nélkül) | **Áll** — de önmagában gyenge érv |
| **3. Az adóügyi szám CSAK A NYOMTATÁS UTÁN érkezik** | **ÁLL, és mindvégig ez volt a teherhordó érv** |

**A 3. érv egymaga is elég, és nem függött a formátumtól:** a bizonylat **létezik
a nyomtatás előtt is** — tételei vannak, fizetés történt rá. Saját azonosító
nélkül a nyomtatás pillanatáig **nincs mivel hivatkozni rá**, és ha a nyomtatás
elbukik, **soha nem is lesz.** Épp a „függő tranzakció" állapot válna
kezelhetetlenné. **A saját számozás tehát továbbra is kötelező** — csak nem azért,
amiért én először írtam.

**Egy maradék, apró megjegyzés:** a formátum **nem végtelen** (a 9999. zárás után
a viselkedés a gyártói protokoll kérdése). 27 év távlatában ez nem tervezési
kockázat, de a protokolldokumentáció áttekintésekor **egy sor erejéig nézzük meg**,
mi történik a határon — ne feltevés maradjon.

#### B14.3 `[ELFOGADVA]` Eszközönként elhatárolt saját tartomány — miért JÓ ötlet

A felhasználó javaslata: minden kiállító eszköz **saját, egymást nem metsző
számtartományból** dolgozik (2-es kassza: `002…`, 4-es kassza: `004…`).

**Ez a legerősebb megoldás, és nem csak könnyítés — hibaosztályt szüntet meg:**

1. **Az ütközés SZERKEZETILEG lehetetlen**, nem „protokollal megelőzött".
   Nincs mit elrontani.
2. **Nulla koordináció.** Az eszköz **örökké tud offline bizonylatot kiállítani**,
   anélkül hogy bárkitől engedélyt kérne. A csökkentett mód így nem kivétel a
   számozás szempontjából, hanem **ugyanaz, mint a normál üzem.**
3. **`[!]` A B13 ÁTVÉTELI ELJÁRÁS EGYSZERŰBB ÉS GYORSABB LESZ TŐLE.**
   Korábban azt írtam, hogy a begyűjtésnek **az első bizonylat kiadása ELŐTT**
   kell lefutnia, különben sorszám-ütközés keletkezik. **Eszközönkénti
   tartománnyal ez a kényszer MEGSZŰNIK**, mert a tartalék szerver **soha nem
   ad ki bizonylatszámot** — azt mindig a kassza teszi.
   **Következmény: a tartalék AZONNAL kiszolgálhat, és a begyűjtés
   PÁRHUZAMOSAN futhat.** Az átvétel nem áll meg a begyűjtés miatt → rövidebb
   kiesés. **A begyűjtés célja adat-teljesség marad, nem ütközés-megelőzés.**
4. **Levesz egy forró, sorosított írási utat a szerverről** (a központi
   számláló). A felhasználó megérzése, hogy ez könnyíti a terhelést, **helyes.**
5. **Visszakereséskor azonnal látszik, melyik kassza állította ki.**

#### B14.4 `[ELDÖNTVE]` A SIDURI bizonylatszám VÉGLEGES FORMÁTUMA

**A felhasználó megadása (2026-08-22):** `xxxxxxyyyzzzzz`

| Rész | Jegyek | Jelentés |
|------|--------|----------|
| `xxxxxx` | 6 | **az ÜZLETI NAP dátuma** — **a szerver közli** |
| `yyy` | 3 | **az eszköz sorszáma** (pl. 003) |
| `zzzzz` | 5 | **a bizonylat sorszáma** azon az eszközön, azon az üzleti napon |

**Példa:** `26082200300347` — a 2026-08-22-i üzleti nap, 3-as eszköz, 347. bizonylat.

##### `[!]` Ez a formátum MEGOLDJA az általam felvetett két problémát

**1. A kimerülés-aggály TÁRGYTALAN.** Korábban azt számoltam, hogy 5 jegyű
folyószám (100 000) egy forgalmas kasszán **egy éven belül elfogyna.** Ez a
formátum viszont **naponta és eszközönként újraindul** → 99 999 bizonylat / eszköz
/ nap. **Ez soha nem fogy el.** A `[!]` M1 módosítási igényem **visszavonva.**

**2. A rendezés-aggály is TÁRGYTALAN.** Korábban jeleztem, hogy eszközönkénti
tartománnyal a bizonylatok **nem rendeződnek időrendbe** szám szerint.
A dátum-előtaggal **rendeződnek** — a szám szerinti sorrend egyben időrend is.

##### `[!]` DE: az `xxxxxx` az ÜZLETI NAP, NEM a naptári nap

**Ezt a specifikációban élesen ki kell mondani, különben némán elromlik.**
Ha az üzleti nap 04:00-tól 04:00-ig tart, akkor egy **augusztus 23-án hajnali
2:30-kor** kiállított nyugta **az augusztus 22-i üzleti naphoz tartozik**, tehát
a száma `260822…`-vel kezdődik, nem `260823…`-mal.

**Aki ezt `DateTime.Now.Date`-ként implementálja, annak minden éjszakai helyen
csendben elcsúszik a számozás** — és csak a havi összesítőnél derül ki. Ez a §8
hibaosztálya. **Az üzleti nap értékét EGY nevesített helper adja**, sehol máshol
ne számolódjon.

**Jó mellékhatás:** mivel a bizonylatszám magában hordozza az üzleti napot, és azt
**a szerver közli**, ez **egyetlen igazságforrássá teszi az üzleti nap fogalmát** —
ami közvetlenül enyhíti az `F4` alatt jelzett bajt (három párhuzamos
„napzárás"-fogalom él a tervben).

##### `[ ]` Két apró, olcsó megfontolás — döntsd el, nem sürgős

- **Kétjegyű év.** `260822` 2099-ig működik. Nem gyakorlati kockázat, de a
  **négyjegyű év két karakterbe kerül** (`2026082200300347`), és ez az a fajta
  döntés, amit utólag már nem lehet olcsón megváltoztatni. **Ajánlom, de nem
  erőltetem** — a te döntésed.
- **Megjelenítés csoportosítva.** 14 jegyet az ember nem tud felolvasni telefonba.
  **Tároljuk egyben, de MUTASSUK tagolva:** `260822-003-00347`. A tagolás legyen
  **csak megjelenítés**, sose kerüljön a drótra vagy az adatbázisba (§8).

##### `[ELDÖNTVE + MÓDOSÍTVA]` M2 — az eszközazonosító egyedisége és a KLÓNOZÁS

**A felhasználó válasza:** normál regisztrációnál a **szerver adja ki** az
eszközazonosítót; másolható ugyan, de akkor az **adatokkal együtt** másolódik,
illetve egy friss gépnek **először szerver-szinkron kell**, addig nem enged tovább.

**A „szerver adja ki" és a „szinkron nélkül nem enged tovább" HELYES és
KÖTELEZŐ — de önmagában NEM elég.** Ez a maradék rés:

> Klónozom a 003-as gépet. A klón **érvényes azonosítót ÉS érvényes hitelesítő
> adatokat visz magával.** Mindkettő le tud szinkronizálni — mert mindkettő
> **ugyanannak** a gépnek látszik. Aztán **mindkettő bizonylatot ad ki
> `…003…` előtaggal, ugyanazon az üzleti napon, a saját helyi számlálójából**
> → **duplikált bizonylatszám.**
>
> A „szinkron kell" szabály ezt **nem fogja meg**, mert a klón simán szinkronizál.
> **A hiányzó darab: a szervernek meg kell tudnia KÜLÖNBÖZTETNI a klónt az
> eredetitől.**

**Ellenszer — és a jó hír, hogy MINDKÉT eleme MÁR A TERVBEN VAN:**

1. **Hardveres ujjlenyomat.** A 19. fejezet **már tervez** hardveres
   ujjlenyomatot a licenceléshez (alaplap/CPU/MAC). **Ugyanazt használjuk itt.**
   Ha egy ismert eszközazonosító **más ujjlenyomatról** jelentkezik be, az vagy
   **gépcsere** (engedélyhez kötött művelet), vagy **klón**.
2. **Forgó hitelesítő adat.** Minden sikeres kapcsolódáskor a szerver **új
   titkot ad**, a régi érvénytelen. Ha később valaki a **régi** titkot mutatja
   be, **abból tudni, hogy két példány van** — ez a lopott-token felismerés
   szokásos mintája.

**A kemény szabály:** ha a szerver **ugyanazt az eszközazonosítót két különböző
ujjlenyomatról** látja, **MINDKETTŐT letiltja a bizonylat-kiállításból**, amíg
ember fel nem oldja. **Nem választ magától** — nem tudhatja, melyik az eredeti,
és a rossz választás duplikált adóügyi bizonylatot okoz.

**Pontosítás a „szinkron nélkül nem enged tovább" szabályhoz** — ez fontos, mert
különben ellentmond az offline-first alapelvnek:

| Eszköz állapota | Mit tehet szerver nélkül |
|-----------------|--------------------------|
| **Soha nem regisztrált** (friss vagy klónozott telepítés) | **SEMMIT** — nem adhat ki bizonylatot. Ez a helyes és szükséges kapu |
| **Már sikeresen regisztrált** | **Mindent, amit a csökkentett mód enged** — offline is dolgozhat |

##### `[ELFOGADVA]` M4 — a kliens visszakérheti a saját előzményeit a szervertől

**A felhasználó ötlete:** a kliensek kérhessenek vissza adatot a szervertől a
saját előzményükről, így **gépcsere után az új gép szinkronizál, és feltölti az
adatbázisát a kiesett gép adataival.**

**Jó, és pontosan a gépcsere-hézagot zárja be**, amit az M2-nél nyitva hagytam.
**Három kikötéssel:**

1. **`[!]` A visszatöltött archívum LEHET, HOGY HIÁNYOSABB, mint az eredeti volt.**
   A szerver csak azt tudja visszaadni, amit **megkapott** — épp azok a
   tranzakciók hiányozhatnak belőle, amiket a régi gép nem tudott felküldeni.
   **Ezért a visszatöltött archívumot MEG KELL JELÖLNI** („szerverről
   visszaállítva, dátum; nem feltétlenül tartalmazza azt, amit a szerver sosem
   kapott meg"). §5: ne tegyünk úgy, mintha teljes lenne.
2. **`[!]` Ez ADATKIADÁSI csatorna → biztonsági kapu kell rá.** Egy kliens
   **kizárólag a SAJÁT** előzményét kérheti le, **csak sikeres regisztráció
   után**, hitelesítetten, és **a lekérést naplózni kell** (audit).
3. **A gépcsere legyen EXPLICIT, engedélyezett művelet** („ez a gép a 003-as
   eszközt váltja fel"), ne automatikus felismerés. Különben egy idegen gép
   pusztán azzal, hogy 003-nak vallja magát, **letöltheti a teljes előzményt.**

#### `[RÉSZBEN ELFOGADVA — a szabály módosítást igényel]` B14.7 — ÜZLETI NAP NYITÁSA OFFLINE, óra-ellenőrzéssel

**A felhasználó felvetése (2026-08-22):** ha a szerver nem elérhető, és úgy
nyitnának üzleti napot az egyik gépen, akkor a kliens **az utolsó lezárt üzleti
nap dátumához hozzáad 1 napot**, és összeveti a rendszerórával; ha nem egyezik,
jelzi, hogy nincs szerverkapcsolat és **valószínűleg rossz az időbeállítás.**

**A felvetés lényege HELYES, és fontos**, mert az üzleti nap dátuma **bekerül a
bizonylatszámba** — tehát egy rossz óra **rossz számokat gyárt**, amiket utólag
nem lehet átírni. A konkrét szabály viszont **módosítást igényel.**

##### `[!]` A javasolt szabály hibája: minden zárvatartási napon FALSE ALARM

Az „utolsó lezárt nap + 1 nap" szabály **azt feltételezi, hogy az üzleti napok
folytonosak.** De egy hétfőn és kedden zárva tartó hely szerdán nyit:
- utolsó lezárt nap = vasárnap, +1 nap = **hétfő**,
- a rendszeróra viszont **szerdát** mond.

**A szabály hibát jelezne — pedig minden rendben van.** És ez **nem ritka eset**:
zárvatartási nap, szabadság, felújítás, szezonális működés mind ide tartozik.
Egy ellenőrzés, ami rendszeresen ok nélkül riaszt, **egy hét alatt megtanulják
figyelmen kívül hagyni** — onnantól nem véd semmit (§1.5: az ingadozó őr rosszabb
a semminél).

##### A helyes megfogalmazás: nem dátum-aritmetika, hanem MONOTONITÁS

Az igazi védendő tulajdonság **nem az, hogy „+1 nap"**, hanem hogy
**az üzleti nap értéke SOHA ne menjen visszafelé és soha ne ismétlődjön** —
mert **abból keletkezik duplikált bizonylatszám.**

**Javasolt szabály, három ággal — a két irány NEM egyformán veszélyes:**

| Amit az óra mond | Megítélés | Teendő |
|------------------|-----------|--------|
| **≤ a gép által VALAHA használt legmagasabb üzleti nap** | **VESZÉLYES** — ebből duplikált bizonylatszám lesz | **KEMÉNY TILTÁS.** Ne lehessen üzleti napot nyitni. Ez az egyetlen ág, ahol megállunk |
| **> az utolsó, de „ésszerű" távolságon belül** (pl. ≤ 30 nap) | **NORMÁL** — zárvatartás, szabadság, szezon | **Engedjük**, jelzés nélkül |
| **> az utolsó, de irreálisan messze** (pl. > 30 nap, vagy múltbeli év) | **GYANÚS** — de lehet valós (szezonális hely télen zár) | **FIGYELMEZTETÉS + megerősítés**, ne tiltás |

**Miért aszimmetrikus:** az órát **visszaállítani** duplikált bizonylatszámot
csinál — ez adóügyi hiba, és **szándékos csalás eszköze is lehet.**
Az órát **előreállítani** hézagot csinál — kellemetlen, de nem sorszám-ütközés.
Ezért az egyik hard stop, a másik figyelmeztetés.

**`[!]` A „valaha használt legmagasabb üzleti nap" a gépen TÁROLVA legyen**, ne
az utolsó lezárt napból számoljuk. Így az óra visszaállítása **nem tudja
becsapni** — pontosan ez a lényeg.

##### Két olcsó, független ellenőrzési pont, ami MÁR RENDELKEZÉSRE ÁLL

Ha a szerver nem elérhető, a gép nincs egyedül:

1. **A többi Siduri-eszköz** — a **tanú-séma** (B11) újrahasznosítható erre.
   Ha egy másik pénztárgép elérhető, meg lehet kérdezni tőle, ő milyen üzleti
   napon áll. **Két gép egyeztetése sokkal erősebb, mint egy gép órája.**
2. **Az adóügyi eszköz saját napszámlálója.** Az eszköz tudja, hányadik
   munkanapon áll, **függetlenül a Windows órájától.** Ez egy teljesen
   független referencia — és épp arra való.

##### `[!]` ÚJ HÉZAG, amit ez a forgatókönyv feltár: két gép, két külön üzleti nap

**Ez eddig sehol nem szerepelt.** Ha a szerver halott és **két pénztárgép
egymástól függetlenül nyit üzleti napot**, és **az óráik eltérnek** (az egyik
azt hiszi, 22-e van, a másik 23-a), akkor:

- a két gép **különböző üzleti nap alatt** ad ki bizonylatokat,
- visszatéréskor a szerver **két, egyszerre nyitott üzleti napot** lát,
- a napi zárás, a forgalmi összesítő és az adóhatósági adatszolgáltatás
  mind **kettéhasad** — és a bizonylatszámok már ki vannak nyomtatva, tehát
  **nem javíthatók.**

**Kell rá szabály.** Javaslat, döntésre:
- **az offline nyitott üzleti nap kapjon „ideiglenes" jelölést**, és
  visszatéréskor a szerver **egyeztesse össze** őket;
- **a nyitás előtt a gép KÖTELEZŐEN kérdezze meg a tanúkat** (fenti 1. pont) —
  ha bármelyik másik gép már nyitott üzleti napot, **azt vegye át**, ne nyisson
  újat a saját órája alapján. **Ez a legolcsóbb és leghatásosabb ellenszer.**

#### B14.5 `[?]` JOGI KÉRDÉS, amit NEM tudok megválaszolni (§13.5)

**A számviteli és adójogi előírások jellemzően folyamatos, kihagyás és ismétlés
nélküli sorszámozást követelnek a bizonylatoktól.** Hogy ez **egyetlen, globális
sorozatot** ír-e elő, vagy **több párhuzamos, előre elhatárolt tartomány is
megfelel** (ami az általános gyakorlat), azt **forrás nélkül nem állítom.**

**Enyhítő körülmény, ami valószínűleg megoldja:** a mi számunk **belső
azonosító**, nem a jogi bizonylat sorszáma — azt az adóügyi eszköz adja.
**De ez nem minden bizonylatra igaz:** ahol **a Siduri maga a kiállító**
(pl. számla saját kiállítása, egyes belső bizonylatok), ott a szabály élesben él.

**→ Az ELSŐ ELLENŐRZŐ KÖR (jogi) kiemelt tétele.** Ha kiderül, hogy egyetlen
sorozat kell, ez a döntés megdől, és a hatása nagy.

#### B14.6 Amit az adóügyi számmal tenni kell

- **Tároljuk a bizonylat mellett**, teljes egészében, ahogy az eszköz visszaadta
  (ne bontsuk szét visszaépíthetetlenül) — **a sztornóhoz kell.**
- **`[!]` NULLÁZHATÓ mező.** **Nem minden Siduri-bizonylatnak van adóügyi száma:**
  előnyugta, raktármozgás, készpénz ki-/befizetés, selejt, személyzeti fogyasztás
  — ezek soha nem érintik az adóügyi eszközt. **Minden kód, ami feltételezi, hogy
  létezik, el fog hasalni.** A séma és a felület is számoljon a hiányával.
- **Ha a nyomtatás elbukott, a bizonylatnak NINCS adóügyi száma** — tehát
  **fiskálisan nem is állították ki**, tehát **nem is sztornózható** a szokásos
  úton. Ez **külön feloldási útvonal** (F3 függő tranzakció), nem sztornó.
- **A saját számunk és az adóügyi szám párosítása legyen KÖTELEZŐEN naplózva**,
  mert ez a kapocs a mi rendszerünk és a jogi bizonylat között — és az
  ellenőrzésnél ez az, amit kérni fognak.

---

### `[JAVASLAT — ELFOGADÁSRA AJÁNLOM]` B13 — ÁTVÉTEL ELŐTTI BEGYŰJTÉS a kliensektől

> **A felhasználó ötlete (2026-08-22).** Amikor a tartalék átveszi a szolgálatot,
> kérdezze le az összes klienstől az utolsó szinkron óta (plusz egy átfedő ablak)
> keletkezett tranzakciókat. Az átfedés validál, az azon túli rész pedig
> **bepótolja azt, ami eddig csak a fő szerveren létezett.**

#### `[!]` Ez az ötlet TÖBBET old meg, mint amire szánva volt

Az árva tranzakciók problémája **nem attól volt nehéz, hogy hiányzik az adat** —
az adat mindig megvolt valahol. **Attól volt nehéz, hogy a BIZONYLAT-SORSZÁMOK
ÜTKÖZNEK.** Ha a fő szerver kiadta az 1001–1015 sorszámokat, de csak 1010-ig
replikált, akkor a tartalék azt hiszi, 1011 következik — és ha ő is kiad egy
1011-est, két különböző eladás kap azonos sorszámot. **Ezt utólag nem lehet
helyrehozni**, mert a papír már a vendégnél van.

**A felhasználó ötlete pontosan ezt előzi meg — DE CSAK EGY FELTÉTELLEL:**

> ### `[FELÜLÍRVA a B14 döntéssel — lásd alább]` A begyűjtésnek az ELSŐ bizonylat kiadása ELŐTT kell lefutnia.
>
> Ha a begyűjtés a takeover **része**, és a tartalék **csak utána** kezd
> bizonylatot kiadni, akkor megtanulja a valódi legmagasabb sorszámot, és
> **1016-tal folytatja, nem 1011-gyel. Ütközés SOHA nem keletkezik.**
>
> Ha a begyűjtés a kiszolgálás megkezdése UTÁN futna, az ötlet **nem javít,
> hanem ront**: pontosan azokat az ütköző rekordokat importálná be, amiket a
> tartalék időközben már kiosztott.

> ### `[!]` FELÜLÍRVA — a B14 (eszközönkénti számtartomány) döntés eltörölte ezt a kényszert
>
> A fenti okfejtés **azt feltételezte, hogy a SZERVER osztja a bizonylatszámot.**
> A B14 döntés szerint viszont **minden kiállító eszköz a saját, elhatárolt
> tartományából számoz** — tehát **a tartalék szerver soha nem ad ki
> bizonylatszámot**, és **ütközés szerkezetileg nem keletkezhet.**
>
> **Új szabály: a tartalék AZONNAL kiszolgálhat, a begyűjtés PÁRHUZAMOSAN fut.**
> Az átvétel nem áll meg a begyűjtés miatt → **rövidebb kiesés.**
>
> **A begyűjtés célja megmarad, csak megváltozik:** nem ütközés-megelőzés, hanem
> **adat-teljesség és ellenőrzés** (az átfedő szakasz összevetése). Ettől
> **kevésbé időkritikus, de nem kevésbé fontos.**

**Ezzel a nehéz probléma könnyű problémává válik:** ütközés nélkül az árva
tranzakciók behozatala **közönséges, idempotens adatimport**, nem
összefésülhetetlen elágazás. A `A4` alatti „a könyvelésük nem lehet automatikus"
korlát **nagyrészt feloldódik** — a maradék az, amit a kliensek nem láttak
(lásd lent).

#### Mit gyűjt be, és mit NEM

**BEGYŰJTHETŐ — és ez a lényeg, mert ez az árva tranzakciók zöme:**
minden kliens-eredetű írás: eladás, rendelés, fizetés, sztornó, készpénzmozgás.
Ezek mind valamelyik kliensen keletkeztek, tehát a kliens archívumában megvannak.

**NEM gyűjthető be — ezt ki kell mondani, különben hamis biztonságot ad:**

| Mi marad ki | Miért | Súlyosság |
|-------------|-------|-----------|
| **Szerver-eredetű adat** — napi zárás összesítők, adóhatósági beküldés állapota, felhőszinkron vízjelek, ütemezett feladatok eredménye | A kliens sosem látta ezeket | Kicsi darab, de **nem nulla** — az egyeztetés nem tűnik el, csak összezsugorodik |
| **Egy olyan kliens adata, ami az átvételkor szintén halott** (pl. közös áramkör esett ki) | Nem tudjuk lekérdezni **abban a pillanatban** | **Nem végleges veszteség**, ha a begyűjtés **megismételhető**, amikor az a gép visszatér — lásd lent |
| ~~Vékonykliens (telefon, tablet) adata~~ | **`[ELDÖNTVE 2026-08-22]` A vékonykliensek IS vezetnek archívumot** — lásd B15 | Megoldva |

#### Három módosítás, amit javaslok az ötlethez

**1. `[!]` A begyűjtés az ELSŐ bizonylat kiadása ELŐTT fusson** — lásd fent.
Ez nem finomítás, hanem a feltétel, amitől az ötlet működik.

**2. Az ablak ne fix 5 perc legyen, hanem KLIENSENKÉNT SZÁMÍTOTT.**
A fix 5 perc feltételezi, hogy a replikációs lemaradás 5 percnél kisebb volt.
**Egy terhelt J1900-on ez nem garantált** — épp azért választottunk aszinkron
replikációt, mert a lemaradást nem tudjuk előre. Ha a lemaradás 8 perc volt, egy
5 perces ablak **némán kihagy 3 percnyi adatot.** §5.

**Robusztus változat:** a tartalék minden kliensnek megmondja, **mi az utolsó
tranzakciója, amit ő ismer** — a kliens pedig **mindent visszaküld, ami azután
jött**, plusz egy átfedő darabot. Így az ablak **automatikusan pontos**, akármekkora
volt a lemaradás, és **a felhasználó átfedés-ötlete megmarad**, mert az az
értékes rész.

**3. Időkorlát + explicit „hiányos" állapot, ne várakozás.**
Ha egy kliens nem válaszol N másodpercen belül, **a hely nem állhat meg miatta.**
A tartalék vegye át a szolgálatot, de **jegyezze fel és LÁTHATÓAN írja ki**, hogy
melyik géptől nem sikerült begyűjteni, tehát **az egyeztetés hiányos**. §5:
a jelzés hiánya nem bizonyíték a sikerre.
**És a begyűjtés legyen MEGISMÉTELHETŐ**, ne egyszeri: amikor a hiányzó gép
visszatér, automatikusan fusson le rá is.

#### Miért BIZTONSÁGOS az átfedés — és miért értékes

**Biztonságos**, mert minden kliens-írás egyedi azonosítót visz (F1). Egy már
meglévő tranzakció újbóli beküldése **no-op**, nem duplikátum. Az átfedésnek
tehát nincs ára.

**Értékes**, mert **ellenőrzést** ad: az átfedő szakaszban a tartaléknak és a
kliensnek **ugyanazt kell látnia**. Ha eltérnek, az **hiba jele** — és ilyenkor
**meg kell állni és szólni**, nem továbbmenni. Ez pontosan §5 pozitív
bizonyítéka: nem azt feltételezzük, hogy stimmel, hanem ellenőrizzük.

#### `[?]` Egy premissza, ami az egészet EGYSZERŰBBÉ tenné, ha igaz

Ha igaz az `A2` alatti (még **igazolatlan**) feltevés, hogy **az adóügyi eszköz
maga állítja ki és sorszámozza a jogi bizonylatot**, akkor **a sorszám-ütközés
problémája NEM IS LÉTEZIK**: minden kassza adóügyi eszköze a saját számlálóját
vezeti, helyben, és az túléli a szerver halálát.

**Ekkor a begyűjtés célja már nem az ütközés megelőzése, hanem pusztán az
adat-teljesség** — továbbra is hasznos, de nem kritikus időzítésű.

**Ez erősen indokolja, hogy azt a premisszát MIELŐBB igazoljuk**, mert két
érdemben különböző takeover-eljárást ír elő. Felvéve az első ellenőrzési kör
tételei közé.

#### `[ ]` Biztonsági megjegyzés

A begyűjtés **beviteli csatorna**: egy feltört vagy hamisított kliens
**kitalált eladásokat** adhatna be az átvételi ablakban. Ellenszer: az
eszközregisztráció (B6), a kliens kulcsával aláírt tételek, és — ha az adóügyi
eszköz a sorszámozó — az adóügyi eszköz naplójával való összevetés (F3).

#### Összegzés: mennyire jó az ötlet?

**Nagyon jó, és az egyik legértékesebb hozzájárulás ebben a tervezési körben.**
Nem apró javítás: **a terv legkockázatosabb darabját zsugorítja össze.**
Az egyeztetés nem tűnik el (a szerver-eredetű adat és az elérhetetlen gépek
miatt), de **a nehéz része — az összefésülhetetlen sorszám-elágazás — megszűnik**,
feltéve, hogy a begyűjtés az első bizonylat előtt fut le.

---

### `[ELDÖNTVE — igen, de minimális]` B15 — VÉKONYKLIENS-ARCHÍVUM

**Döntés (2026-08-22):** a vékonykliensek (telefon, tablet) **is vezetnek helyi
archívumot**, de **jóval kisebbet, mint a pénztárgépek** — a felhasználó
megfogalmazásában: *„nem kell olyan combosat, mint a POS-oknak."*

**Miért kellett egyáltalán:** a B13 begyűjtés **csak azt éri el, ami valamelyik
eszköz archívumában van.** Egy telefonról feladott, a fő szerver által nyugtázott,
de nem replikált rendelés enélkül **sehol máshol nem létezne** — se a tartalékon,
se egy POS-on.

#### Mi legyen benne, és mi NE

| | Pénztárgép (POS) | **Vékonykliens** |
|---|---|---|
| Mit tárol | mindent, amit ez a gép kiállított | **csak amit EZ az eszköz küldött** (rendelés, ha fizetést vesz fel, akkor az is) |
| Megőrzés | **20 forgalmas nap** | **`[JAVASLAT]` minden, ami még nincs nyugtázva + egy rövid átfedő farok** (pl. az aktuális üzleti nap, vagy 2–3 forgalmas nap) |
| Tartalom | teljes bizonylat | **azonosító, időbélyeg, tételsorok, célasztal** — a visszajátszáshoz és az összevetéshez szükséges minimum |

#### `[!]` Miért JAVASLOM a rövidebb megőrzést — adatvédelmi indok, nem takarékosság

**A telefon a leggyakrabban elveszített és ellopott eszköz** az egész
rendszerben. Egy pult mögé csavarozott pénztárgép ritkán tűnik el; **egy pincér
telefonja hetente elhagyható.** Ugyanaz az elv, mint a B10/a-nál:
**minél kevesebb adat van rajta, annál kisebb a kár.**

**És a rövid megőrzés elég is a célra:** a helyreállítási ablak **percekben**
mérhető, nem napokban — a telefon úgyis gyakran újracsatlakozik. Amit meg kell
őriznie, az **a még nem nyugtázott adat** (az kortól függetlenül soha nem
törölhető) **plusz egy rövid átfedés** a B13 ellenőrzéséhez. Ennél többet
tárolni **kockázatot vinne fel egy zsebben hordott eszközre, haszon nélkül.**

#### Amit ez maga után von

- A vékonykliensek is **azonosítottak és regisztráltak** kell legyenek (B6),
  hogy a begyűjtés hitelesíthető legyen.
- **`[ELDÖNTVE 2026-08-22]` Az ELSŐ verzióban a telefon NEM fizettet és NEM ad
  nyugtát** — csak rendelést vesz fel és menedzsel. **Később bővítendő**, tehát
  elő kell készíteni.
  **Jó hír: az előkészítés majdnem ingyen van**, mert a B14 formátum eleve
  eszközfüggetlen. **Egyetlen kikötés, ami MOST olcsó és később drága:**
  az eszközszám-tér (`yyy`) legyen **KÖZÖS minden eszköztípusra** — ne külön
  „POS-számok" és külön „telefon-számok". Ha most szétválasztjuk, a bővítéskor
  migrálni kell; ha most közös, akkor a telefon egyszerűen kap egy számot.
- Elveszett/ellopott eszköznél kell **távoli visszavonás** (a regisztráció
  érvénytelenítése), különben egy elhagyott telefon örökre legitim kliens marad.
  Ez a B6 kiterjesztése.

---

### `[ ]` B16 — TÁVOLI KONFIGURÁCIÓ A FELHŐBŐL (új tétel, 2026-08-22)

**A felhasználó egy mellékmondatban új képességet nevezett meg**, ami egyik
eredeti doksiban sem szerepelt így: *„a szerver esetén a központi felhővel való
kommunikációhoz, amiből majd az online felületen látja az ügyfél a saját adatait
és tud beállításokat végezni távolról."*

A specifikáció 18. fejezete „felhő platformot tenant- és licenckezelésre" ír —
**a helyszín TÁVOLI KONFIGURÁLÁSA ennél lényegesen többet jelent**, és külön
tervezést igényel.

#### Miért nem apró kiegészítés

1. **`[!]` Ez KÉTIRÁNYÚVÁ teszi a felhő-kapcsolatot.** Eddig a felhő
   **fogadó** oldal volt (adatszinkron, licenc-életjel, adatszolgáltatás
   biztonsági másolata). Most **utasítást is küld lefelé.** Ez teljesen más
   biztonsági és megbízhatósági osztály.
2. **`[!]` Ütközés a helyi beállítással.** Az ügyfél a felhőben átír egy árat,
   miközben a helyi menedzser ugyanazt a terméket a helyi felületen módosítja.
   **Melyik nyer?** A rendszer szerver-autoritatív a LOKÁLIS állapotra — most
   viszont egy MÁSODIK autoritás jelent meg. **Szabály kell rá**, különben ez a
   §6 varrat-hibaosztálya: mindkét oldal „sikeresen" ír, és csendben szétcsúsznak.
3. **`[!]` Offline sorbaállás.** Ha a helyszín offline, a felhőben elvégzett
   beállítás **nem érkezik meg.** Az ügyfél viszont a felhőben azt látja, hogy
   megtörtént. **Ez §5 néma kudarca**, csak a felhasználó felé fordítva:
   a felület olyat mutat elvégzettként, ami nem történt meg.
   → **Kell egy állapot: „a helyszín még nem vette át"**, láthatóan.
4. **`[!]` Biztonsági célpont.** Egy távoli csatorna, ami **meg tudja változtatni
   egy pénztárgép konfigurációját** (árak, ÁFA-hozzárendelés, jogosultságok),
   a rendszer egyik legértékesebb támadási felülete. Kell hozzá: erős
   hitelesítés, **jogosultsághoz kötés**, és **teljes audit** — ki, mikor, mit
   írt át távolról (F5, F7).
5. **Mit szabad egyáltalán távolról átírni?** Nem mindegy. Egy termék ára: igen.
   Egy ÁFA-kulcs hozzárendelés: **veszélyes** (adóügyi következménye van, §13).
   Egy adóügyi eszköz beállítása: **valószínűleg nem.** **Explicit, szűk
   listát kell definiálni**, nem „mindent, ami a helyi admin felületen megy".

#### `[ ]` Eldöntendő

- Mely beállítások írhatók át távolról (szűk, nevesített lista)?
- Ütközéskor mi nyer — a felhő, a helyi, vagy „az újabb"? És **hogyan látja
  bárki, hogy volt ütközés?**
- Offline helyszínnél a sorbaállított változtatás **meddig érvényes**, és mi
  történik, ha közben helyben is módosult?

**Kapcsolódik:** B7 (multi-tenancy), B6 (biztonság), F5 (támogathatóság),
F7 (jogosultsági modell), 18. és 19. fejezet.

---

### `[JAVASLAT — JÓVÁHAGYÁSRA VÁR]` B11 — A TANÚ-SÉMA részletes terve

> **Státusz:** a felhasználó kérte, hogy írjam le a tervet, majd elolvassa és
> jóváhagyja. **Amíg nincs jóváhagyva, erre építeni nem szabad.**

#### B11.0 A séma SOHA nem dönt — csak bizonyítékot gyűjt

**Ez a legfontosabb tervezési tulajdonsága, és ez teszi olcsóvá és
kockázatmentessé.** Mivel az átkapcsolást mindig ember indítja (B1/c), a
tanú-sémának **nem kell elosztott konszenzus-protokollnak lennie.** Nem szavaz,
nem választ vezetőt, nem oszt zárolást. **Csak kitölt egy képernyőt.**

**Következmény:** ha a tanú-sémában hiba van, annak az eredménye egy
**rosszabbul tájékozott ember**, nem két fő szerver és nem szétdivergált
nyugtasorozat. Ezért nem kell hozzá az a hibatűrő gépezet (lease, fencing,
kvórum), ami az automatikus failoverhez kellene.

#### B11.1 Két külön kérdés, ugyanazzal a mechanizmussal

| | Kérdés | Mit dönt el |
|---|--------|-------------|
| **Q1** | Én estem ki, vagy a szerver halott? | **Melyik személyzeti üzenet jelenjen meg** (a három közül) |
| **Q2** | Tényleg 5+ perce elérhetetlen a szerver, több nézőpontból? | **Felajánljuk-e az átkapcsolást** |

#### B11.2 Ki lehet tanú

**Tanú = olyan Siduri-eszköz, ami (a) hálózati tápról megy, (b) a nyitvatartás
alatt elvárhatóan folyamatosan bekapcsolva van, és (c) telepítéskor tanúnak van
konfigurálva.**

| Eszköz | Tanú? | Miért |
|--------|-------|-------|
| Windows POS vastagkliens | **IGEN** | Mindig bekapcsolva, vezetékes vagy stabil wifi, a mi szoftverünk fut rajta |
| Tartalék szerver (ami egy POS) | **IGEN, és a legerősebb** | Ha ő látja a főt, akkor a fő él |
| KDS | **IGEN** | Hálózati tápról megy, folyamatosan bekapcsolva, és WebSocketen beszél a szerverrel — tehát TUDJA, eléri-e |
| Rendeléskijelző | **IGEN** | Ugyanaz |
| Tablet, telefon (vékonykliens) | **NEM** | Zsebben van, alszik, lemerül. A némasága semmit nem jelent. Legfeljebb **gyenge pozitív jel**: ha elérem, a hálózatom legalább részben él |

#### B11.3 A LEGFONTOSABB SZABÁLY: a némaság NEM szavazat

| Amit a tanú tesz | Mit ér |
|------------------|--------|
| **Válaszol**, és azt mondja: „én sem érem el a szervert" | **Bizonyíték**, hogy a szerver halott |
| **Válaszol**, és azt mondja: „én elérem a szervert" | **Bizonyíték**, hogy a szerver ÉL, és a hiba köztem és a szerver között van |
| **Nem válaszol** | **SEMMIT nem ér.** Lehet lekapcsolva, lehet ugyanazon szakadás mögött, mint én |

**Miért kell ezt külön kimondani:** ez pontosan a §5 hibaosztálya. Ha a némaság
szavazatnak számítana, egy éjszakára lekapcsolt pénztárgép „szavazna" a szerver
halála mellett, és a rendszer egy egészséges szerverről állítaná, hogy halott.

#### `[JAVASLAT — a felhasználó felvetése + módosítás]` B11.3/b — ÖNDIAGNOSZTIKAI LÉTRA

> **A felhasználó felvetése (2026-08-22):** legyen internet-ellenőrzés (pl. ping egy
> erre a célra fenntartott szerverre), illetve nézze meg a gép, hogy az IP-címe és
> az alhálózata egyezik-e a többiekével és a szerverével — ha nem változott semmi
> a saját hálózatában, akkor a probléma nem vele van.

**Az alhálózat- és változás-vizsgálat ötlete ERŐS, az internet-ping GYENGE.**
Az alábbi létra megtartja az erős részt és a helyére teszi a gyengét.

##### A létra — olcsóbbtól a drágábbig, informatívtól a kevésbé informatívig

| # | Vizsgálat | Mit bizonyít | Költség |
|---|-----------|--------------|---------|
| **1** | **Él-e a saját hálózati kapcsolat?** (kábel bedugva / wifi csatlakozva) | Ha NEM: **egyértelműen én vagyok a hibás.** Azonnali, biztos válasz | nulla |
| **2** | **Változott-e a hálózati identitásom** az utolsó sikeres szerver-kapcsolat óta? IP, alhálózati maszk, átjáró IP-je, **az átjáró MAC-címe**, wifinél az **SSID ÉS a BSSID** (a konkrét hozzáférési pont MAC-je) | **Ez a legerősebb egyetlen jel.** Ha az azonosságom megváltozott, **nálam történt valami** — másik hálózatra kerültem, más AP-hoz kapcsolódtam, más IP-t kaptam | nulla hálózati forgalom |
| **3** | **Elérem-e a saját alapértelmezett átjárómat?** | A kapcsolatom és az IP-beállításom **működik** — tehát a hiba nem a saját kábelemnél/wifimnél van | egy csomag, helyi |
| **4** | **Elérem-e a többi Siduri-eszközt?** (a tanú-séma) | **EZ adja meg a valódi választ:** én vagyok-e, vagy a szerver | kicsi, helyi |
| **5** | **Van-e internetem?** (utolsó fok, két külön jel: névfeloldás + HTTPS-elérés egy közismert publikus címre) | **A „szerver vagy én?" kérdésre NEM válaszol** — de kiegészítő információ, amikor minden más elhasalt, és külön célra (adóhatósági adatszolgáltatás) amúgy is kell | kicsi, nincs saját függőség |

##### `[ELDÖNTVE 2026-08-22]` Az internet-ellenőrzés BENT MARAD — utolsó fokként

**A felhasználó pontosítása feloldotta a fő kifogásomat:** nem saját, általunk
üzemeltetett végpontra gondolt, hanem egy **közismert publikus címre** (pl. Google),
és **utolsó ellenőrzési pontnak**, amikor már minden más elhasalt.

**Így elfogadom**, mert a két legsúlyosabb ellenvetésem elesik: nincs új
üzemeltetési függőségünk, és nem az első, hanem az **utolsó** fok, tehát nem
uralja a diagnózist. A megmaradó kifogások (gyenge korreláció, félrevezethet)
azzal kezelhetők, hogy **külön, megcímkézett sorban jelenik meg**, és **soha nem
befolyásolja a „szerver vagy én?" döntést.**

**Három gyakorlati kikötés:**
1. **Ne ICMP ping legyen.** Sok hálózaton tiltott, és egy tiltott ping
   „nincs internet"-nek látszik. Helyette **egy kicsi HTTPS-kérés** egy
   közismert, magas rendelkezésre állású címre.
2. **Bontsuk KÉT jelre: névfeloldás és elérés.** „A DNS nem működik" és „nincs
   útvonal" **két különböző hiba**, két különböző teendővel — és a
   szétválasztásuk ingyen van, mert úgyis egymás után történik.
3. **A „nincs internet" SOHA ne legyen hibaállapot.** Ez az offline-first
   rendszer **normál üzeme** egy szolgáltatói kimaradás alatt, és van olyan
   helyszín, ahol a kimenő forgalom szándékosan tiltott. Tájékoztató sor,
   nem riasztás — a riasztás az adóhatósági határidőhöz tartozik (19. fejezet),
   nem ehhez.

##### Miért NEM szabad az internet-ellenőrzést a DIAGNÓZISBA keverni (az eredeti érvelés)

1. **Mindkét irányban gyenge a korreláció.** Lehet internetem és mégsem érem el a
   szervert (rossz alhálózat, vendég-wifi, 4G-stick). És **lehet, hogy nincs
   internetem, miközben minden tökéletesen működik** — ez az offline-first
   rendszer NORMÁL állapota egy szolgáltatói kimaradás alatt.
2. **`[!]` Aktívan félrevezethet.** Ha az internet megy, a személyzet arra jut,
   hogy „a hálózat rendben van" — miközben a valódi hiba egy switch.
   Ha nem megy, **a szolgáltatót fogják hívni** — pontosan az a hibaosztály,
   ami miatt a személyzeti üzenetekből kivettük az „internet" szót (B12 alatti
   szakmai pontosítás).
3. ~~**Új üzemeltetési függőség.**~~ **`[TÁRGYTALAN]`** — a felhasználó
   publikus címre gondolt, nem sajátra. Ez a kifogás elesett.
4. **Az átjáró jobb próba nála**, és ingyen van: helyi, gyors, nem függ tőlünk.

##### Amit viszont MEGTARTUNK az internet-ellenőrzésből

**Külön, egyértelműen megcímkézett sorként** jelenjen meg — mert az internetnek
**van** jelentősége, csak **másra**: az adóhatósági adatszolgáltatásra és a
felhőszinkronra. Ez amúgy is külön jelzést kapott (lásd a személyzeti üzenetek
alatti pontosítást és a 19. fejezet 18 órás riasztását). **Így nem vész el, de
nem is szennyezi a szerver-diagnózist.**

##### `[!]` A legértékesebb elem, ami ebből az ötletből következik: MI VÁLTOZOTT

A 2. pont nem csak igen/nem választ tud adni — **meg tudja mondani, MI változott.**
A gép minden sikeres szerver-kapcsolatkor **elmenti a működő hálózati
azonosságát**, és kieséskor összeveti.

Egy olyan képernyő, ami azt írja ki, hogy:

> *„Utoljára 19:42-kor beszéltél a szerverrel. Azóta ez a gép átkapcsolt a
> `Bar-AP` hozzáférési pontról a `Terasz-AP`-ra, és új IP-címet kapott egy másik
> alhálózaton."*

**nagyságrendekkel többet ér, mint bármilyen ping-eredmény** — mert nem csak azt
mondja meg, hogy baj van, hanem **hogy mi történt.** Ez egyben a támogatás
(F5) eszköze is: ez a néhány sor pontosan az, amit péntek este telefonon
kérdezgetni kellene.

**Ez a `MERESEK.md`-be nem tartozik** — nem mérés, hanem naplózás és
összehasonlítás, elhanyagolható költséggel.

#### B11.4 A döntési menet — amit a pénztárgép lefuttat

**0. lépés — Öndiagnosztika (B11.3/b létra 1–3. foka), hálózati forgalom nélkül vagy
majdnem anélkül.**
- **Nincs kapcsolat** (kábel kihúzva / wifi lecsatlakozott) → **ÉN estem ki**,
  azonnal, kérdezősködés nélkül. → **(2)-es üzenet.**
- **Megváltozott a hálózati azonosságom** (IP, alhálózat, átjáró MAC, SSID/BSSID)
  → **erős jel, hogy nálam történt valami.** → **(2)-es üzenet**, és **írja ki,
  MI változott.**
- **Nem érem el a saját átjárómat** → **ÉN estem ki.** → **(2)-es üzenet.**

**1. lépés — Egyáltalán a hálózaton vagyok?**
- Nem érek el SEMMIT (se Siduri-eszközt, se az alapértelmezett átjárót)
  → **ÉN estem ki.** → **(2)-es üzenet**, és a visszaszámláló **NEM indul**.
- Elérek legalább egy Siduri-eszközt → tovább.

**2. lépés — Mit mondanak a tanúk?**
- **Bármelyik tanú azt mondja: „én elérem a szervert"** → **a szerver ÉL.**
  → **(2)-es üzenet változata** („a szerver rendben van, a hiba a te géped és a
  szerver között van"). A visszaszámláló **NEM indul**.
- **Minden válaszoló tanú azt mondja: „én sem érem el"** → **a szerver halott.**
  → **(1)-es üzenet**, és a visszaszámláló **INDUL**.
- **Elérek eszközöket, de egyik sem tanú** (pl. csak telefonokat), **vagy
  egyetlen tanú sem válaszol** → **BIZONYTALAN.** → **(3)-as üzenet**, és a
  visszaszámláló **indul** (mert a szerver tényleg lehet halott), de a
  megerősítő képernyő **kiírja, hogy nem volt kereszt-ellenőrzés.**

**3. lépés — Átkapcsolás felajánlása.** MIND a négynek teljesülnie kell:
1. van egyáltalán konfigurált tartalék szerver *(ha nincs → soha nem ajánlunk)*,
2. a tartalék **válaszol és egészségesnek jelenti magát** (R6),
3. eltelt az 5 perc (monoton időmérőn, R3),
4. **legalább egy rajtam kívüli tanú** is megerősíti, hogy nem éri el a
   szervert — **kivéve**, ha nincs más tanú (lásd a degenerált esetet lent),
   ekkor ezt a megerősítő képernyő explicit kiírja.

#### B11.5 Telepítési kombinációnként

| Telepítés | Tanúk | Mi működik |
|-----------|-------|-----------|
| **1 Windows POS = szerver** | — | A kérdés fel sem merül: nincs hálózati ugrás a szerverig |
| **2+ POS, egyikük szerver, NINCS tartalék** | a többi POS, KDS, kijelző | Csak a **Q1** él (kinek a hibája). Átkapcsolást **soha nem ajánlunk** — nincs mire |
| **2+ POS, egyikük szerver, VAN tartalék** | a többi POS + **a tartalék** + KDS, kijelző | A **teljes séma**. A tartalék a legerősebb tanú |
| **Dedikált szerver + 2+ POS + tartalék** | az összes POS + a tartalék + KDS, kijelző | A legjobb eset: sok, egymástól független tanú |
| **`[!]` Dedikált szerver + 1 POS, és a tartalék ezen az EGY POS-on van** | KDS/kijelző, ha van; különben **SENKI** | **Degenerált eset.** A POS-nak magának kell döntenie. Ez nem baj, mert **az ember úgyis megerősíti** — de a megerősítő képernyőnek **ki kell írnia, hogy nem volt független megerősítés** |

#### B11.6 Mit üzennek egymásnak a tanúk

**Nagyon keveset — és szándékosan semmilyen üzleti adatot.** Egy állapotcsomag:
- ki vagyok (eszközazonosító), mi a szerepem,
- **mikor beszéltem utoljára sikeresen a fő szerverrel**,
- elérem-e most a fő szervert / a tartalékot,
- mennyi ideje vagyok csökkentett módban.

Ettől olcsó (elhanyagolható hálózati és processzorterhelés) és **kicsi a
biztonsági felülete**.

#### B11.7 `[!]` Biztonsági követelmény, ami ebből következik

**A tanú-üzeneteket hitelesíteni KELL.** Enélkül bárki, aki a vendég-wifire
felcsatlakozik, tanúnak adhatja ki magát és **hazudhat** („én sem érem el a
szervert") — hogy kikényszerítsen egy átkapcsolás-ajánlatot.

**A kár korlátozott**, mert ember úgyis megerősíti — de zaklató vektor, és
pontosan az a fajta, ami éles helyzetben tetézi a bajt. Ez a B6
(eszközregisztráció + kölcsönös hitelesítés) hatálya alá tartozik: **a tanú-séma
nem külön biztonsági rendszert igényel, hanem a meglévő eszközregisztrációt
használja.**

#### B11.8 Mi történik, ha a tanúk tartósan ellentmondanak egymásnak?

Nem kell feloldani — **nem szavazás.** Ilyenkor a **(3)-as, bizonytalan** üzenet
jelenik meg, és a képernyő **nyersen felsorolja a tényeket**: melyik gép mit lát,
mikor beszélt utoljára a szerverrel. **Az ember lát olyat, amit a gép nem** — ez
volt az egész kétlépcsős konstrukció alapgondolata (B1/c).

---

### `[ELDÖNTVE — kell, aláírással és felhőbe továbbítva]` B12 — Kockázatvállalási nyilatkozat

**A felhasználó kérése (2026-08-22):** legyen egy **alkalmazásban elérhető
űrlap**, amit a végén egy kijelölt mezőben **alá kell írni**; a rendszer
**elmenti**, és **továbbítja a fő felhőszerverre**, hogy meglegyen és
**visszakereshető** legyen — **időbélyegekkel, hitelesítve és védve.**

#### Amit ebből technikailag meg tudunk csinálni

1. **Aláírás érintőképernyőn.** A pénztárgép érintőképernyős, ez természetes.
2. **`[!]` A SZÖVEG VERZIÓJÁT is el kell menteni, nem csak azt, hogy aláírták.**
   Két év múlva a nyilatkozat szövege más lesz. Ha csak azt tároljuk, hogy „X
   aláírta", akkor **nem tudjuk bizonyítani, MIT írt alá.** Ezért a mentett
   csomag tartalmazza a **pontos, akkor érvényes szöveget**, nem hivatkozást rá.
3. **A csomag tartalma:** a telephely azonosítója; a nyilatkozat teljes szövege
   és verziószáma; **az aláíráskori TELJES konfiguráció** (mely gépek, milyen
   szereppel, van-e tartalék); az aláíró neve és beosztása; az aláírás képe;
   a bejelentkezett felhasználó; az eszköz ujjlenyomata.
4. **Ujjlenyomat (hash) és lánc.** Az egész csomagról készül egy lenyomat, és
   minden új nyilatkozat **az előzőhöz láncolódik** — így egy dokumentum utólagos
   eltüntetése vagy átírása kimutatható.
5. **`[!]` KÉT időbélyeg, és a MÉRVADÓ a felhőé.** A helyi gép órája az ügyfél
   gépének órája — **nem megbízható** (átállítható, elcsúszhat, lásd D4). Ezért
   tároljuk **mindkettőt**: amit a helyi gép állít, és amit a **felhő ad
   érkezéskor** — és **a felhőé a mérvadó.**
6. **`[!]` OFFLINE ÚTVONAL KELL.** Egy friss telepítésen **gyakran még nincs
   internet** — épp azt állítjuk be. Tehát a nyilatkozat a **kimenő sorba** kerül,
   megváltoztathatatlanul, és akkor megy fel, amikor lesz kapcsolat.
   **Amíg a felhő nem igazolta vissza, az admin felület írja ki, hogy
   „helyben rögzítve, a felhő még nem igazolta vissza"** — §5: pozitív
   bizonyíték kell, nem a hibajelzés hiánya.
7. **Védelem:** nyugalmi állapotban titkosítva (amennyire a B10/a keretei
   engedik), és a **kliens eszközkulcsával aláírva**, hogy a felhő igazolni tudja
   az eredetét.

#### `[!]` Amit a felhasználó nem említett, de nélküle az egész elavul

**Ha a konfiguráció később megváltozik, a régi nyilatkozat MÁR NEM A VALÓSÁGRÓL
SZÓL.** Ha az ügyfél fél év múlva vesz egy negyedik pénztárgépet, vagy leszereli
a tartalékot, akkor van egy aláírt papírunk egy olyan felállásról, ami már nem
létezik — **ami rosszabb a semminél, mert hamis biztonságot ad.**

**Ezért:** a rendszer **vesse össze a jelenlegi konfigurációt az utoljára aláírt
állapottal**, és ha eltér, **kérjen új nyilatkozatot**, illetve jelezze az admin
felületen, hogy az aktuális felállásra **nincs érvényes kockázatvállalás.**

#### `[?]` IGAZOLATLAN JOGI PREMISSZA (§13.5) — ezt NEM tudom igazolni

**Egy érintőképernyőn rajzolt aláírás NEM minősített elektronikus aláírás.**
Amit a fenti csomag ad, az **erős bizonyíték**, nem minősített aláírás.

**Hogy ez a konkrét jogi célra (felelősségkorlátozás) elegendő-e, azt NEM tudom
megmondani, és nem is fogom megtippelni.** Ez jogi kérdés, forrás kell hozzá.
**A tervezett jogi ellenőrzési kör tétele.** Amíg nincs igazolva, a rendszer
építhető (a bizonyíték-érték magától is hasznos), de **semmilyen jogi hatást nem
állíthatunk róla** sem a doksiban, sem az ügyfélnek.

#### `[ ]` Adatvédelmi következmény

A nyilatkozat **személyes adatot tartalmaz** (aláíró neve, aláírásképe), és
**a mi felhőnkbe kerül.** Ettől Siduri Systems adatkezelővé válik erre az adatra.
Kell hozzá: megőrzési szabály, tájékoztató, és illeszkednie kell a B7
(felhő-adatvédelem) tételhez.

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
| 1 | **B14.7 — két gép, két üzleti nap offline** | `[ ]` **ÚJ HÉZAG, döntést igényel** | Ha a szerver halott és két pénztárgép egymástól függetlenül nyit üzleti napot eltérő órával, **kettéhasad a napi zárás és az adatszolgáltatás** — és a bizonylatszámok már ki vannak nyomtatva. Javasolt ellenszer: nyitás előtt kötelezően kérdezze meg a tanúkat. |
| 2 | **B16 — távoli konfiguráció a felhőből** | `[ ]` **ÚJ TÉTEL** | Kétirányúvá teszi a felhő-kapcsolatot. Eldöntendő: mit szabad távolról átírni, mi nyer ütközéskor, és hogyan látszik, hogy egy offline helyszín még nem vette át a változtatást. |
| 3 | **B14.5 — jogi kérdés** | `[?]` **A JOGI KÖR KIEMELT TÉTELE** | Megfelel-e a több párhuzamos számtartomány a folyamatos sorszámozás követelményének? Forrás nélkül nem állítható. Ha egyetlen sorozat kell, a B14 megdől. |
| 4 | **B11 — tanú-séma** | `[ ]` **JÓVÁHAGYÁSRA VÁR** | A séma SOHA nem dönt, csak bizonyítékot gyűjt — ezért nem kell hozzá elosztott konszenzus. |
| 2 | **TPM-ellenőrzés** | `[FOLYAMATBAN]` — a felhasználó a napokban ellenőrzi | Addig **mindkét ágra készülünk**: a titkosítás konfigurációs képesség, és az admin felület kiírja, melyik ágon vagyunk. **Nem blokkolja a fázistervet.** |
| 3 | **B12 jogi kérdése** | `[?]` **IGAZOLATLAN, jogi kör tétele** | Az érintőképernyős aláírás nem minősített elektronikus aláírás. Hogy a felelősségkorlátozáshoz elég-e, forrás nélkül nem állítható. |
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
| — | ~~B14.4~~ | `[ELDÖNTVE]` | **A SIDURI bizonylatszám formátuma: `xxxxxxyyyzzzzz`** — üzleti nap dátuma (a szervertől) + eszközszám + napi folyószám. Ez **megoldja mindkét korábbi aggályomat**: naponta újraindul, tehát soha nem fogy el; és a dátum-előtag miatt szám szerint időrendben áll. **Kikötés:** az `xxxxxx` az ÜZLETI NAP, nem a naptári nap — aki `DateTime.Now.Date`-ként írja meg, annak minden éjszakai helyen csendben elcsúszik a számozás. |
| — | ~~B14 M2~~ | `[ELDÖNTVE, kiegészítve]` | A szerver adja ki az azonosítót és regisztráció nélkül nincs bizonylat — **helyes, de a klónt nem fogja meg**, mert a klón érvényes hitelesítéssel szinkronizál. **Hiányzó darab: hardveres ujjlenyomat (már tervben van a licencelésnél) + forgó hitelesítő adat.** Ha egy azonosító két ujjlenyomatról jelentkezik, **mindkettő tiltva**, amíg ember fel nem oldja. |
| — | ~~B14 M4~~ | `[ELFOGADVA]` | **A kliens visszakérheti a saját előzményét a szervertől** → gépcsere után az új gép feltölti magát. Három kikötés: a visszatöltött archívum **hiányosabb lehet** (meg kell jelölni), adatkiadási csatorna (hitelesítés + audit), és a gépcsere **explicit, engedélyezett művelet** legyen. |
| — | ~~Adóügyi szám~~ | `[HELYESBÍTVE]` | **Az ÉN érvem volt hibás:** a napszámláló 4 jegyű (~27 év), nem 3 (~2,7 év) — **gyakorlati ütközés nincs.** A saját számozás viszont **továbbra is kötelező**, mert a teherhordó érv más volt: az adóügyi szám csak a NYOMTATÁS UTÁN érkezik, tehát nélküle a bizonylatnak addig nincs azonosítója, és nyomtatási hiba esetén soha nem is lesz. |
| — | ~~B14~~ | `[ELDÖNTVE]` | **Kétrétegű bizonylat-számozás.** (1) SIDURI szám: minden kiállító eszköz **saját, elhatárolt tartományból** számoz (2-es kassza: `002…`) → az ütközés **szerkezetileg lehetetlen**, nulla koordináció kell, és **a tartalék szerver átvételkor AZONNAL kiszolgálhat**. (2) ADÓÜGYI szám (`A12345678/123/1234`): **tároljuk a bizonylat mellett** (a sztornóhoz kell), de **nem lehet a mi azonosítónk** — nem mi vezéreljük, a 3 jegyű napszámláló ~2,7 év után körbefordulhat, és **csak a nyomtatás UTÁN érkezik**, tehát nélküle a bizonylatnak a nyomtatásig nem is lenne azonosítója. **Nullázható mező** — előnyugtának, raktármozgásnak, készpénzmozgásnak soha nincs. |
| — | ~~B15~~ | `[ELDÖNTVE]` | **A vékonykliensek is vezetnek archívumot, de minimálisat**: csak amit ők küldtek, és **rövidebb megőrzéssel** (nyugtázatlan + rövid átfedő farok) — adatvédelmi okból, mert a telefon a leggyakrabban elveszített eszköz. |
| — | ~~Internet-ellenőrzés~~ | `[ELDÖNTVE]` | **Bent marad, de UTOLSÓ fokként** és publikus címre (nem sajátra). Külön, megcímkézett sorban; **soha nem befolyásolja a „szerver vagy én?" döntést**. HTTPS, ne ICMP; két külön jel (névfeloldás + elérés); és a „nincs internet" **soha nem hibaállapot**. |
| — | ~~B13~~ | `[ELFOGADVA, módosítva]` | Átvétel előtti begyűjtés a kliensektől. **A B14 miatt már nem kell az első bizonylat előtt lefutnia** — a tartalék azonnal kiszolgálhat, a begyűjtés párhuzamosan fut. Célja: **adat-teljesség és ellenőrzés**, nem ütközés-megelőzés. |
| — | ~~B12~~ | `[ELDÖNTVE]` | **Kockázatvállalási nyilatkozat**: alkalmazásban elérhető űrlap, érintőképernyős aláírással, elmentve ÉS a fő felhőszerverre továbbítva, visszakereshetően, időbélyeggel, védve. Négy dolog, amit a terv hozzátesz: (1) a SZÖVEG VERZIÓJÁT is menteni kell, nem csak azt hogy aláírták; (2) KÉT időbélyeg, és a MÉRVADÓ a felhőé, mert a helyi óra az ügyfél gépéé; (3) offline útvonal, mert friss telepítésen gyakran nincs internet — és amíg a felhő nem igazolta vissza, ezt ki kell írni; (4) **konfiguráció-eltérés esetén ÚJ nyilatkozat kell**, különben egy már nem létező felállásról van aláírt papírunk. |
| — | ~~B9 lépcső jellege~~ | `[ELDÖNTVE]` | **A gépszám-lépcső ÉRTÉKESÍTÉSI AJÁNLÁS, nem kikényszerített korlát.** Ha kellene tartalék de nincs hova tenni → dedikált szervergépet ajánlunk (az nem POS, így egyetlen Windows POS is elláthatja a tartalék szerepet). Ha az ügyfél a kockázat ismeretében elutasítja, elfogadjuk. Fordítva is: 2 POS-os hely kérésére megcsináljuk. **A szoftver semmilyen konfigurációt nem utasíthat el.** |
| — | ~~B1/b pontosítás~~ | `[ELDÖNTVE]` | **A tartalék szerver SOHA nem dedikált gép — mindig egy Windows POS vastagkliens.** A fő szerver jellemzően szintén POS-on van, de aki megengedheti, annál lehet dedikált. Vékonykliens / KDS / rendeléskijelző egyik szerepet sem viheti. Négy következmény: a tartalék terhelése a legrosszabb pillanatban ugrik meg; a szerepet vivő gépet valaki kikapcsolhatja; a szerver Windows Service kell legyen, nem a pénztáros munkamenetében; és a frissítés sorrendje a `siduri-updater` kemény követelménye lett. |
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
