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
> **ÚJ (tizenhetedik kör):** **`[!]` C11/a — MTÜ-IGAZOLÁS KELL az NTAK-adatszolgáltatáshoz**
> (igazolt lelet; a célpiac NTAK-köteles, tehát ez belépési feltétel — de az
> interfész-leírás nyilvános, tehát azonnal elkezdhető). **HELYESBÍTÉS: a felhasználó
> feltevése, hogy a felhasználó kézzel is beküldheti a napi adatot, NEM igazolt.**
> **C3/a helyesbítés — az ÉN javaslatom volt hibás**, az adókulcs-másolás a helyes.
> **F4/K2** — négyrétegű terv a Munkanap-összefésülésre. **C3/c** — kategória-alapértékek.
>
> **ÚJ (tizenhatodik kör — nagy blokk):** **Fiskális üzemmódok** három esetre bontva
> (új fájl: `FISKALIS_UZEMMODOK.md`, benne a kért e-pénztárgépes utánajárás
> eredményével). **F4** — mind a négy nap-fogalom definiálva, **három új
> következménnyel** (bizonylatszám-ütközés; a 25 órás leállás ütközik a csökkentett
> móddal; a Műszak = fiskális napzárás). **C3/a-b** — ÁFA és NTAK a terméken.
> **C2/a-b** — árváltozás-történet és a termék életciklusa (soft delete).
> **A3** — a felhő a jogi archívum. **B17** — a felhő saját rendelkezésre állása.
>
> **ÚJ (tizenötödik kör):** **F7/a** — szerkeszthető jogosultsági szintek (a frissítéskor
> érkező ÚJ jogosultságok alapból tiltottak, de feltűnő jelzéssel). **F7/b** — a Siduri
> admin fiók sérthetetlen + fix offline belépés; javaslat: telephelyenkénti hitelesítő
> adattal, hogy egy kiszivárgás ne érintsen minden ügyfelet.
>
> **ÚJ (tizennegyedik kör):** **Leltár** — az egyetlen jogos készlet-„felülírás", de
> korrekciós mozgásként megvalósítva, fordulónapi elszámolással. **Több telephely
> alapmodellként** (nem csak franchise). **A felhő raktár/receptúra = a telephelyi
> adminfelület** → egy webes admin, két helyről kiszolgálva. **ÚJ FÁJL:**
> `gemini_cloud_spec_en.md` — a Gemini felhő-specifikációja bemenetként, teljes
> összevetéssel: egy pontja (felhő-szuperfiókos failback-engedélyezés) **FELÜLÍRVA**,
> egy pontja (globálisan szinkronizált szuperfiók-jelszó) **biztonsági aggály**.
>
> **ÚJ (tizenharmadik kör):** **B16 kibővítve** — a felhő **teljes menedzsment-platform**
> (beállítás-paritás, raktár, receptúra, statisztika, **zárolható értékek**,
> **üzletlánc/franchise szint**). Ez ÚJ hierarchia-szintet vezet be a telephely fölé, és
> **a B7 multi-tenancy döntést magához köti**. Kiemelt új megállapítás: **a törzsadat lehet
> felhő-autoritatív, a KÉSZLET nem** — az futó egyenleg, aminek nem lehet két gazdája.
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

### `[ELDÖNTVE — a felhő a jogi archívum]` A3 — purge és megőrzés

**Döntés (2026-08-22), az 1. ellenőrző kör `L6` lelete után:** az adatok
**a felhős szerveren** tárolódnak hosszú távon. A 8 éves megőrzési
kötelezettséget (számviteli tv. 169. §) tehát **a felhő teljesíti**, nem a
telephelyi gép.

**Ez egyben a `L6` alatt felvázolt három út közül az elsőt választja**, és
következik belőle:
- **`[!]` A „tisztán lokális" topológia (spec 4.) önmagában NEM elegendő** egy
  megfelelést igénylő ügyfélnek. Vagy nem adjuk ilyen formában, vagy az ügyfél
  saját archiválási megoldást vállal — **és ezt a `B12` kockázatvállalási
  nyilatkozatban rögzíteni kell.**
- **`[!]` A purge SOHA nem törölhet olyat, aminek a megőrzéséről nincs POZITÍV
  BIZONYÍTÉK** (§5). Nem elég, hogy „elküldtük" — **igazoltan meg kell lennie
  a felhőben**, mielőtt a helyi példány törlődik.

#### `[ ] KÉSŐBBI TERV` — összetett archiválási folyamat a felhőben

**A felhasználó jelezte (2026-08-22), előre, hogy ne felejtsük el:** szeretne egy
**összetett, akár túloptimalizált archiválási folyamatot** is a felhőben, hogy
**a szerver tárhelyét se pazaroljuk feleslegesen.**

**`[KÉSŐBBI FÁZIS]` — most nem tervezzük meg**, de **három dolgot most olcsó
nem elrontani**, és később drága javítani:

1. **A bizonylat legyen ÖNMAGÁBAN ÉRTELMEZHETŐ** (lásd `C2/a`: az eladáskori
   név, ár, adókulcs benne van). **Egy archivált bizonylat, aminek a
   megértéséhez a mai terméktörzs kell, nem archiválható önállóan** — és pont
   az kell, hogy 8 év múlva is olvasható legyen, „a könyvelési feljegyzések
   hivatkozása alapján visszakereshető módon" (169. §).
2. **A tömörítés/hidegtárolás NE veszítsen felbontást.** Egy „napi összesítővé
   tömörített" archívum **nem teljesíti** a bizonylat-szintű megőrzést.
   Az összesítés **riport**, nem archívum.
3. **A visszatöltés menete legyen kipróbálva, ne csak megtervezve.** Egy
   archívum, amiből még soha nem állítottunk vissza, **nem archívum, hanem
   remény** (§5: pozitív bizonyíték).

**`[ ]` Felvéve a fázistervbe (`E1`) későbbi tételként.**
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

### `[RÉSZBEN ELDÖNTVE]` B17 — A FELHŐ SAJÁT RENDELKEZÉSRE ÁLLÁSA (új tétel, 2026-08-22)

**A felhasználó döntése:** a felhő is **két fizikai szerver** ugyanazzal a
szoftverrel — egy **fő** és egy **másodlagos**. **Minden adat mindkét helyen
meg kell legyen.** A fő szerver **terhelés függvényében megoszthassa a
feladatokat** és **automatikusan átcsatornázhassa a forgalmat** a másodlagosra,
**hogy a mi oldalunkról ne lehessen kimaradás.** A **folyamatos szinkron
elengedhetetlen**, és **a bővíthetőség a mi oldalunkon is fontos.**

#### `[!]` A LEGFONTOSABB, amit ki kell mondani: NE MÁSOLJUK IDE A TELEPHELYI MEGOLDÁST

A telephelyen **kézi átkapcsolást** választottunk, mert **két gép nem tud
többségi szavazást tartani**, és a hálózati szakadás megkülönböztethetetlen a
géphaláltól.

**A felhőben ez NEM így van, és ez FONTOS különbség:**

| | Telephely | **Felhő** |
|---|---|---|
| Ki uralja az infrastruktúrát | az ügyfél | **mi** |
| Lehet-e harmadik szavazó | nehezen (lekapcsolják a gépeket) | **igen, olcsón** |
| Van-e menedzselt adatbázis-szolgáltatás automatikus átvétellel | nincs | **igen** |
| Lehet-e terheléselosztó előtte | nem életszerű | **igen** |

**Tehát a felhőben az AUTOMATIKUS átvétel nem ugyanaz a kockázat**, mint a
telephelyen — ott azért volt veszélyes, mert nem tudtunk kvórumot építeni.
**Itt tudunk.** A telephelyi döntés indoklása **nem vihető át**, és nem is szabad
átvinni (§2.1: a premisszát itt is igazolni kell, nem analógiából venni).

#### `[!]` DE: az „aktív-aktív, mindkettőn minden adat, folyamatos szinkron" a LEGNEHEZEBB konfiguráció

A kérés három eleme **együtt** a legnehezebb elosztott rendszer:
1. **minden adat mindkét helyen** +
2. **terhelésmegosztás** (tehát mindkettő dolgozik) +
3. **folyamatos szinkron**

**Ha ez azt jelenti, hogy MINDKÉT szerver ÍR**, akkor **konfliktusfeloldás
kell** — ugyanaz a probléma, amit a telephelyen `A2`-vel szándékosan
elkerültünk. Két helyen egyszerre módosított árlista, két helyre egyszerre
felküldött bizonylat: **nincs rá általános jó válasz.**

#### `[JAVASLAT — döntésre]` A kérés teljesíthető, de bontsuk szét ÍRÁSRA és OLVASÁSRA

> - **ÍRÁS: egy helyen.** Egy szerver fogadja az írásokat, a másik forró
>   tartalék, **automatikus átvétellel** (ezt a felhőben biztonságosan meg
>   tudjuk csinálni, lásd fent). **Konfliktus nem keletkezhet.**
> - **OLVASÁS: mindkettőn.** A riportok, statisztikák, grafikonok, a webes
>   felület böngészése — **ez a terhelés túlnyomó része** — elosztható.
>
> **Ez teljesíti a felhasználó célját** („ne lehessen a mi oldalunkról
> kimaradás", „terhelés függvényében ossza meg a feladatokat"), **anélkül hogy
> megfizetnénk az aktív-aktív írás árát.**

**`[ ]` Döntést igényel.** Ha a felhasználó ragaszkodik az írás megosztásához is,
az **vállalható**, de akkor **nevesíteni kell a konfliktusfeloldási szabályt**
minden írható adatfajtára — ez érdemi munka és kockázat.

#### `[!]` A „folyamatos szinkron" ugyanaz a csapda, mint a telephelyen

A `B1/b`-nél már kimondtuk: **a „szinkron, ami baj esetén automatikusan
aszinkronra vált" a legrosszabb választás**, mert pont akkor írsz védtelenül,
amikor azt hiszed, védve vagy. **Ez a felhőben is ugyanúgy igaz.**
**Vagy vállaltan szinkron** (a másodlagos kiesése lassítja/megállítja a főt),
**vagy vállaltan aszinkron** (failovernél veszhet néhány másodperc) —
**a néma átváltás tilos.**

#### `[!]` Bővíthetőség: ez ELDÖNTI a `B7` multi-tenancy kérdést

A felhasználó külön kiemelte a bővíthetőséget. **Ez összeér a `B7`-tel, ami még
nyitva van, és a `B16.2` lánc-hierarchiával.**

**`[JAVASLAT]` A természetes bővítési út a BÉRLŐ SZERINTI szétosztás
(sharding):** ha a kapacitás elfogy, **új szervert állítunk be, és bérlőket
mozgatunk rá** — nem az egy adatbázist próbáljuk nagyobbra hizlalni.

**Egyetlen kikötéssel, ami MOST olcsó és később drága:**
> **Egy LÁNC (franchise / többtelephelyes tulajdonos) MINDIG EGY szétosztási
> egységen belül maradjon.**
>
> Enélkül a lánc-szintű összesített lekérdezés — ami a `B16.11` szerint
> **alapkövetelmény** — **két adatbázison átívelő lekérdezéssé válik**, ami
> nagyságrenddel drágább és lassabb.

**`[ ]` A `B7` és a `B17` bővíthetőség EGYÜTT döntendő.**

#### `[ ]` Ami még nyitva marad

#### `[JAVASLAT]` B17/b — szinkron vagy aszinkron? — és miért NEM ugyanaz a kérdés, mint a telephelyen

**`[!]` A telephelyi érvelés itt NEM érvényes, és ezt fontos kimondani.**

A telephelyen azért esett ki a szinkron replikáció, mert **minden írás
megvárná a lassabbik gép lemezét, és ez közvetlenül a PÉNZTÁRI VÁLASZIDŐT
rontaná** — a pénztáros áll, a sor nő.

**A felhőben ez nem így van:**

> **A pénztárgép NEM a felhőbe ír.** A pénztárgép a **telephelyi** szerverbe ír.
> A felhő **kötegelt szinkront** kap és a **webes admin felületet** szolgálja ki.
>
> **Mindkettő tűr néhány ezredmásodperc többletet.** Egy pincér sem áll tőle.

**Tehát a szinkron replikáció a felhőben MEGFIZETHETŐ**, miközben a telephelyen
nem volt az. Ugyanaz a technika, **más a költsége, mert más a hívó.**

##### `[!]` DE két szerverrel a szinkron csapdába visz — hárommal nem

| Felállás | Adatvesztés failovernél | Mi történik, ha egy gép kiesik |
|----------|-------------------------|--------------------------------|
| **2 gép, aszinkron** | van (néhány másodperc) | a másik átveszi, működik |
| **2 gép, szinkron** | **nincs** | **`[!]` A MÁSIK IS MEGÁLL** — mert nincs kitől visszaigazolást kapni |
| **3 gép, többségi visszaigazolás** | **nincs** | **működik tovább** — kettő még mindig többség |

**A felhasználó célja — *„ne lehessen a mi oldalunkról kimaradás"* — két géppel
és szinkron replikációval NEM teljesíthető**, mert a másodlagos kiesése
megállítaná az elsődlegest is. **Három géppel viszont mindkettő teljesül
egyszerre: nulla adatvesztés ÉS nincs kimaradás.**

**Ez pontosan az a „harmadik szavazó", amit a telephelyen nem tudtunk
megvalósítani** (mert az ügyfél gépeit lekapcsolják) — **a felhőben viszont
ez rajtunk múlik, tehát megtehetjük.**

**`[JAVASLAT — döntésre]` Három csomópont, többségi visszaigazolással.**
A felhasználó megfogalmazása („két fizikai szerver… a későbbiekben akár több")
ezzel nem ütközik — csak a harmadik gép **előbb** kell, mint gondoltuk.

**Ha mégis pontosan kettő marad:** akkor **vállaltan aszinkron**, a
veszteségablak kimondva — és **soha nem szabad automatikusan szinkronról
aszinkronra váltani** (ez a `B1/b`-nél már lefektetett szabály, itt is él).

#### `[JAVASLAT]` B17/c — földrajzi elhelyezés

| | Egy adatközpont | **Két, egymáshoz KÖZELI adatközpont** | Távoli régiók |
|---|---|---|---|
| Túléli-e a tűz/áramszünet/víz esetet | **NEM** | **igen** | igen |
| Szinkron replikáció késleltetése | elhanyagolható | **néhány ms — vállalható** | tíz-száz ms |

**`[ELDÖNTVE 2026-08-22]`** A felhasználó: **legalább két külön adatközpont**,
de **első körben kizárólag magyarországi** adatközpontok jöhetnek szóba.

**Ez jó választás, és két okból KEDVEZ a terveknek:**
- **GDPR: rendben** — Magyarország EU-n belül van, tehát a `B7` adatlokalizációs
  aggálya megoldva, külön intézkedés nélkül.
- **`[!]` A két magyar adatközpont közti késleltetés kicsi** → **a szinkron
  replikáció még kényelmesebben megfizethető**, mint amivel számoltam.
  **Ez tovább ERŐSÍTI a három csomópontos, szinkron javaslatot** (`B17/b`).

**`[ ]` Egy maradék kockázat, amit ki kell mondani, nem elhallgatni:** két
azonos országban lévő adatközpont **ugyanazon az országos áramhálózaton,
ugyanabban a joghatóságban és ugyanabban a régióban** van. Egy országos szintű
esemény **mindkettőt érintheti.** Ez **vállalható** kockázat egy induló
terméknél — de **később, nagyobb ügyfélkörnél felülvizsgálandó**, és
**a jogi archívum** (lásd `B17/e`) esetében **már most megfontolandó** egy
harmadik, országon kívüli (de EU-n belüli) példány.

**`[!]` Kimondandó, mert könnyű elsiklani fölötte:** a „két fizikai szerver
ugyanabban a szobában" **nem katasztrófavédelem** — egyetlen tűz, egyetlen
elázás, egyetlen áramügy mindkettőt viszi. **Ha már két gépet veszünk, tegyük
őket két helyre**, különben a pénz nagy részét kidobtuk.

#### `[!] [ÚJ HÉZAG — a legkomolyabb ezek közül]` B17/d — A FELHŐ MENTÉSE

**A replikáció NEM mentés.** A `D1` tétel ezt a telephelyre már kimondta:
*„a hibás vagy törölt adat szépen átreplikálódik."* **A felhőre eddig nem
mondtuk ki — pedig ott MINDEN ügyfél adata egy helyen van.**

##### Mi ellen véd a replikáció, és mi ellen NEM

| Esemény | Replikáció | Mentés |
|---------|-----------|--------|
| Meghal egy szerver | **véd** | nem kell hozzá |
| Valaki **letöröl** valamit | **NEM véd** — átreplikálódik azonnal | **véd** |
| Hibás migráció / szoftverhiba adatot ront | **NEM véd** | **véd** |
| Zsarolóvírus, feltört fiók | **NEM véd** | **csak ha a mentést nem éri el** |

##### `[!]` Négy követelmény, ami nélkül a mentés látszat

1. **Időbeli visszaállítási pontok** (point-in-time), nem csak „a tegnapi
   állapot". Egy hibás migráció **percek alatt** ront el mindent.
2. **`[!]` A mentés MÁS hozzáférési úton legyen, MÁS jogosultsággal.** Ha az a
   fiók, ami a szervereket kezeli, **törölni is tudja a mentéseket**, akkor egy
   feltört fiók ellen **a mentés nem véd.** Ez nem elméleti — ez a zsarolóvírus
   első lépése.
3. **Írás-egyszer / módosíthatatlan megőrzés** egy ideig — hogy a mentést **utólag
   se lehessen elrontani**, még jogosultsággal se.
4. **A visszaállítást KI KELL PRÓBÁLNI, rendszeresen.** §5: *„a jelzés hiánya nem
   bizonyíték a sikerre."* **Egy mentés, amiből még soha nem állítottunk vissza,
   nem mentés, hanem remény.**

##### `[!]` A valós igény nem a teljes visszaállítás, hanem az EGY BÉRLŐÉ

**Ez a legfontosabb tervezési következmény, és könnyű kihagyni.**

A gyakorlatban **nem** az lesz, hogy „elveszett az egész felhő". Hanem az, hogy
**„a Kék Rák étterem menedzsere letörölte a teljes terméklistát"**.

**Ha a mentésből csak a TELJES adatbázist tudjuk visszaállítani, akkor egy ügyfél
hibájának javításához MINDEN MÁS ÜGYFÉL friss adatát is visszaforgatnánk** — ami
sokkal nagyobb kár, mint az eredeti baj. **Tehát a mentésnek
BÉRLŐNKÉNTI visszaállítást kell támogatnia.**

**Ez visszahat a `B7` multi-tenancy döntésre:** a **bérlő szerinti szétosztás**
(amit a `B17` bővíthetőség miatt már javasoltunk) **ezt is olcsóbbá teszi** —
egy bérlő adatai egy helyen vannak, tehát külön menthetők és visszaállíthatók.
**Két független érv ugyanarra a döntésre.**

##### `[!]` És egy megnyugtató, illetve egy nyugtalanító megállapítás

**Megnyugtató:** a rendszer **offline-first**, tehát **minden telephely önmaga is
részleges mentés.** Egy felhő-katasztrófa után a **friss** adat nagyrészt
visszaszedhető a telephelyekről (a szerverekről és a pénztárgép-archívumokból).
**A sitek nem állnak meg egy felhőkimaradástól** — ez az architektúra ingyen
kapott haszna.

**Nyugtalanító:** **ez a 8 ÉVES ARCHÍVUMRA NEM IGAZ.** Az `A3` döntés szerint a
telephely 30 nap után purge-öl, és **a hosszú távú megőrzést a felhő teljesíti.**

> **Tehát a 8 éves jogi archívum az EGYETLEN adat az egész rendszerben, aminek
> SEHOL NINCS második példánya a felhőn kívül.**
>
> **Ez a legpótolhatatlanabb adat, amink van** — és jogszabályi kötelezettség
> áll rajta. **A legerősebb védelmet ez érdemli**, nem az operatív adatbázis.

#### `[RÉSZBEN ELDÖNTVE]` B17/e — külön archívum, DE ne cold storage

**A felhasználó válasza (2026-08-22):** *„jó lenne egy külön archívum megoldás
is, bár a felhős szervereket terveztem erre használni a gyorsabb
visszakereshetőség okán, de látom az előnyét, viszont a hátrányát is, hogy a
régi adatok visszanyerése akár jelentősen több idő lehet."*

**Az aggály jogos — de a kettő nem zárja ki egymást.** Itt egy fogalmi
összemosás van, amit érdemes szétszedni:

| Amit szét kell választani | Ez a lényeg |
|---|---|
| **Hol tárolódik** (gyors online tár ⟷ lassú hideg tár) | **ez adja a visszakeresési sebességet** |
| **Milyen mentési rendszer védi** (közös az operatívval ⟷ külön) | **ez adja a pótolhatatlanság elleni védelmet** |

**A kettő FÜGGETLEN.** A javaslatom **nem** az volt, hogy tegyük hideg tárba —
hanem hogy **külön MENTÉSI rendszere legyen.**

**`[JAVASLAT]` A megoldás, ami mindkettőt hozza:**
> A jogi archívum **maradjon ONLINE, gyorsan kereshetően** — a felhős
> szervereken, ahogy a felhasználó tervezte. **A visszakeresés gyors marad.**
>
> **De legyen SAJÁT, az operatívtól elkülönített mentése:** más hozzáférési út,
> más jogosultság, hosszabb megőrzés, módosíthatatlan példányok.
>
> **Így a gyors visszakeresés és a pótolhatatlanság elleni védelem NEM
> egymás rovására megy.**

**Amiért ez fontos:** a 8 éves archívum **az egyetlen adat, aminek nincs
második példánya a felhőn kívül**. Ha ugyanaz a mentési rendszer és ugyanaz a
jogosultság védi, mint az operatív adatokat, akkor **egy feltört fiók vagy egy
elrontott migráció mindkettőt viszi egyszerre.**

**`[ ]` Ami ebből eldöntendő:** a hosszú távú megőrzésű, módosíthatatlan
mentés **hol legyen** — a két magyar adatközpont valamelyikében, vagy
(a fenti országos kockázat miatt) **egy harmadik, EU-n belüli helyen?**

#### `[ ]` Ami még nyitva marad

| Tétel | Kérdés |
|-------|--------|
| **B17/a** | `[ELFOGADVA]` Írás egy helyen, automatikus átvétellel; olvasás megosztva. |
| **B17/b** | **2 gép aszinkronnal, vagy 3 gép szinkronnal?** (javaslat: 3) |
| **B17/c** | Két/három **EU-n belüli, közeli** adatközpont — **ne egy szobában.** |
| **B17/d** | A mentés négy követelménye + **bérlőnkénti visszaállítás**. |
| **B17/e** | **Külön mentési rendszer a 8 éves jogi archívumnak?** (javaslat: igen) |

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

### `[RÉSZBEN ELDÖNTVE]` B16 — A FELHŐ MINT TELJES MENEDZSMENT-PLATFORM (új tétel, 2026-08-22)

> **`[!]` EZ A LEGNAGYOBB SCOPE-VÁLTOZÁS AZ EGÉSZ TERVEZÉSI MUNKAMENETBEN.**
> A felhasználó kimondta, hogy a felhő nem kiegészítő, hanem **teljes értékű
> menedzsment-platform** — és ez a specifikáció 18. fejezetéhez képest
> **nagyságrenddel több.**

#### B16.1 Amit a felhasználó kimondott (2026-08-22)

1. **`[ELDÖNTVE]` Teljes beállítás-paritás:** *„a felhőn minden beállításnak
   elérhetőnek kell lennie, aminek a POS-on is."* Kevés kivétel lesz, azok
   később tisztázandók.
2. **`[ELDÖNTVE]` A felhő funkciói:** raktárkezelés, alapanyag-mozgás,
   receptúrázás, kimutatások, grafikonok, diagramok, **minden elképzelhető
   statisztika és üzletmenedzsment.**
3. **`[ELDÖNTVE]` A kommunikáció kétirányú**, és **kifejezetten védettnek kell lennie.**
4. **`[ELDÖNTVE]` ZÁROLHATÓ beállítások:** a felhőben zárolható egy érték
   (kiemelten **termékárak** és **termék-láthatóságok**), és akkor
   **a POS-on nem írható át.**
5. **`[ELDÖNTVE]` ÜZLETLÁNC / FRANCHISE:** zárolható **központi** értékek több
   üzletre (pl. a franchise árlistája minden üzletben fix, csak a felhőben
   állítható).
6. **`[ELDÖNTVE]` Visszajelzés:** látszódjon, hogy a módosítás **lement-e** a gépekre.
7. **`[ELDÖNTVE]` Eszköz-láthatóság:** melyik eszköz **mikor kommunikált utoljára**,
   **meg van-e nyitva.**

#### B16.2 `[!]` Ez egy ÚJ HIERARCHIA-SZINTET vezet be, ami eddig nem létezett

A terv eddigi modellje: **felhő → bérlő (tenant) → telephely → eszköz.**
A franchise/üzletlánc **egy új szintet szúr be**: **lánc / csoport**, a
telephely FÖLÉ.

**Ez nem egy jelölő mező, hanem öröklődési hierarchia**, és három dolgot érint:

- **az adatmodellt:** minden beállítás-értéknek tudnia kell, **melyik szinten
  definiálták**, és **zárolt-e ott**;
- **a jogosultsági modellt (F7):** ki szerkeszthet melyik szinten;
- **`[!]` a multi-tenancy kérdését (B7), ami MÉG NYITVA VAN** — és ez a
  követelmény érdemben szűkíti a lehetséges válaszokat. Egy lánc **több
  telephelyet átfogó lekérdezéseket** akar (összesített statisztika, közös
  árlista); ez a telephelyenként külön adatbázis irányt drágábbá teszi.
  **A B7-et ezzel együtt kell eldönteni, nem külön.**

#### B16.3 `[JAVASLAT]` A beállítás-öröklődés konkrét alakja

**Most olcsó, utólag az egész felületet átírja.** Javaslat:

Minden beállítás-érték két dolgot hordoz: **melyik szinten definiálták**
(lánc / telephely / eszköz), és **zárolt-e azon a szinten**.

**Feloldás:** a legspecifikusabb **nem zárolt** szint értéke nyer.
Egy **zárolt** magasabb szint **minden alacsonyabbat felülír**.

**`[!]` És egy kikötés, ami nélkül a helyi menedzser azt hiszi, elromlott a
rendszer:** a felületnek **nem elég a HATÁLYOS értéket mutatnia — a FORRÁSÁT is
mutatnia kell.**

> „Ár: 1 200 Ft — **a központ állította be, zárolva**"
> szemben azzal, hogy „Ár: 1 200 Ft".

Enélkül a helyi menedzser újra és újra próbálná átírni, és nem értené, miért nem
sikerül. §5: a felület ne kínáljon olyat, ami nem működik — itt: **ha nem
szerkeszthető, azt MONDJA MEG, ne csak visszautasítsa.**

**`[!]` A zárolást a TELEPHELYI SZERVERNEK is ki kell kényszerítenie**, nem csak
a felhőnek. Ha csak a felhő felülete rejti el, akkor a helyi admin felület, egy
importálás vagy egy közvetlen adatbázis-írás megkerüli. Ez a terv máshol már
lefektetett szabálya (a UI-elrejtés nem kikényszerítés, B6/F7) — itt is él.

#### B16.4 `[!]` A LEGFONTOSABB HATÁROVONAL: BEÁLLÍTÁS vs. MENNYISÉGI ÁLLAPOT

**Ez az az egy dolog, amit szerintem MOST kell eldönteni, mert utólag
katasztrofális.**

A felsorolásban két, gyökeresen különböző dolog keveredik:

| | **Törzsadat / beállítás** | **Mennyiségi, futó állapot** |
|---|---|---|
| Példa | ár, láthatóság, receptúra, termékadat, jogosultság | **készletszint**, eladások, pénztárállás |
| Természete | **érték, amit felülírsz** | **egyenleg, ami mozgásokból áll össze** |
| Lehet-e két írója | igen, ha van feloldási szabály (fent) | **NEM. SOHA.** |

**Miért nem lehet a készletnek két gazdája:** az ár egy érték — ha két helyről
írják, a feloldási szabály eldönti, melyik nyer, és kész. **A készlet viszont
nem érték, hanem egy futó egyenleg**, amit a telephelyen percenként csökkentenek
az eladások. Ha a felhő „felülírja" a készletet 40-re, miközben a telephelyen
közben 3 fogyott, **az a 3 eltűnik** — és nem is derül ki, mert az eredmény
hihetőnek látszik. Ez §7 klasszikus elveszett-frissítése, csak két rendszer között.

**JAVASOLT SZABÁLY:**

> - **Törzsadat és beállítás:** lehet **felhő-autoritatív**, zárolással,
>   a fenti öröklődés szerint. ✔
> - **Mennyiségi, futó állapot** (készlet, forgalom, kassza): **KIZÁRÓLAG
>   telephely-autoritatív**, és **csak felfelé** áramlik.
> - **A felhő KEZDEMÉNYEZHET készletmozgást** (bevételezés, selejtezés,
>   raktárközi mozgás) — de az **MOZGÁSKÉNT megy le**, amit a telephely
>   könyvel el, **nem egyenleg-felülírásként.**
>
> Egy mondatban: **a felhő küldhet „vegyél fel 20 darabot"-ot, de soha nem
> küldhet „a készlet mostantól 40"-et.**

#### B16.5 `[ELFOGADVA + kiegészítés]` Visszajelzés: lement-e a módosítás

A felhasználó kérése helyes és §5-konform. Amit hozzáteszek:

- **Három állapot kell, nem kettő:** *elküldve* / *a telephely átvette* /
  **`[!]` az összes érintett eszköz alkalmazta.** A második és a harmadik nem
  ugyanaz: a telephelyi szerver megkaphatta, miközben egy pénztárgép offline volt
  és még a régi árral dolgozik.
- **Offline telephelynél a felhő NE mutassa elvégzettnek.** Ez a §5 néma kudarca,
  a felhasználó felé fordítva: a felület olyat mutatna késznek, ami nem történt meg.
- **`[ ]` Meddig él a sorbaállított változtatás?** Ha egy telephely három hétig
  offline (szezonális zárás), és közben háromszor módosult ugyanaz az ár —
  **mind a három lemenjen sorban, vagy csak a végállapot?** A végállapot a
  helyes, de akkor **az audit naplóban a köztes lépéseknek meg kell maradniuk.**
- **`[ ]` Mi van, ha közben HELYBEN is módosult** egy nem zárolt érték? Ez az
  ütközés, amire szabály kell.

#### B16.6 `[ELFOGADVA + FONTOS KORLÁT]` Eszköz-láthatóság a felhőben

A kérés jó és olcsó. **De van egy korlát, amit ki kell írni a felületre,
különben rendszeresen félrevezet:**

> **`[!]` A felhő tudása a TELEPHELY kapcsolatán át jön.** Ha a telephely
> internetkapcsolata megszakad, a felhő **egyetlen eszközről sem tud semmit** —
> de a képernyőn ez úgy fog kinézni, mintha **mind a 8 eszköz halott lenne.**
>
> **A felületnek meg kell különböztetnie:** „ez az eszköz nem elérhető"
> ⟷ **„a telephely offline, tehát nem tudom, mi van az eszközökkel".**
> A kettő összemosása pánikot okoz egy olyan helyzetben, ahol valójában csak a
> szolgáltató van kint. §5: a jelzés hiánya nem bizonyíték.

**Továbbá:** az „utoljára kommunikált" időbélyeg **önmagában értelmezhetetlen.**
3 perce = rendben; 3 órája nyitvatartási időben = baj. **Adjunk mellé
értelmezést** (rendben / késik / nem elérhető), a várt életjel-gyakoriság
alapján — ne a felhasználóra hagyjuk a fejszámolást.

#### B16.7 `[!]` PARITÁS-KÖVETELMÉNY — ez a §6 varrat-hibaosztálya, és GARANTÁLTAN elromlik

*„A felhőn minden beállításnak elérhetőnek kell lennie, aminek a POS-on is."*

**Ez a kimondottan legveszélyesebb fajta követelmény**, mert:
- **két külön felület**, két külön repóban, **két külön nyelven** írva
  (helyi admin: a backend-szerver; felhő: a felhő-API),
- **semmilyen fordító nem köti össze őket**,
- **minden új beállítás**, amit valaki hozzáad a POS-hoz, **némán hiányozni fog
  a felhőből**, amíg valaki oda is beírja — és **senki nem fogja észrevenni**,
  amíg egy ügyfél nem keresi.

Ez szó szerint a MERNOKISAROKKOVEK §6 kimért esete: *„EXPLICIT felsorolás vs.
AUTOMATIKUS szerializáció → néma szétcsúszás… paritás-őr KÖTELEZŐ."*

**JAVASLAT — és ez a B8 (hol él az API-szerződés) tételt élesíti:**
a beállítások **EGY helyen legyenek definiálva** (nevesített séma/regiszter:
azonosító, típus, szint, zárolható-e, alapérték, érvényességi szabály), és
**mindkét felület EBBŐL épüljön** — generálva vagy adatvezérelten.
Plusz **automatikus paritás-őr**, ami padlós (§1.3): ha 0 beállítást vizsgált,
az HIBA, nem siker.

**Ha ez nem így épül, a paritás-követelmény teljesítése kézi munkává válik, és
a §6 szerint garantáltan szétcsúszik.**

#### B16.8 `[ ]` Biztonság — konkrétan, mert „védett legyen" önmagában nem terv

A lefelé menő csatorna **árat, ÁFA-hozzárendelést, láthatóságot és
jogosultságot** tud átírni **egy egész láncon**. Ez a rendszer legértékesebb
támadási felülete. Amit a tervbe javaslok:

1. **Kölcsönös hitelesítés**, és **minden parancs aláírva** — a telephely
   ellenőrizze az eredetet, ne csak a csatornát.
2. **Idempotens parancsok** — az újraküldés ne alkalmazza kétszer (F1 mintája).
3. **`[!]` A telephely VALIDÁLJON, ne vakon alkalmazzon.** Egy felhőből érkező
   ÁFA-hozzárendelés, ami nem szerepel a **dátumozott** adókulcs-táblában (§13.3),
   **elutasítandó a telephelyen** — nem alkalmazandó. A bizalom nem mentesít az
   ellenőrzés alól.
4. **Teljes audit:** ki, mikor, mit írt át távolról, melyik telephelyre.
   Ez F5 és F7 hatálya.
5. **`[ ]` Nagy hatókörű változtatás külön védelmet érdemel.** Egy feltört
   felhő-fiók **egy egész franchise árait nullázhatja.** Megfontolandó:
   négy szem elve lánc-szintű ár-műveletnél, vagy késleltetett/értesített
   élesítés. **Eldöntendő.**

#### B16.9 `[!]` Következmény a FÁZISTERVRE (E1)

**A felhő ezzel nem „az 5. repó", hanem önálló terméksáv.** Raktárkezelés,
receptúrázás, statisztika, lánc-kezelés, zárolható öröklődés, kétirányú
konfiguráció — ez a mennyiség **külön fázisolást igényel**, és érdemben
befolyásolja, mi fér bele az első kiadásba.

**Külön kérdés, amit az E1-nél fel kell tenni:** a felhő raktár- és
receptúra-funkciói **ugyanazok**, mint a telephelyi adminfelületé, csak máshol —
vagy **mások**? Ha ugyanazok, akkor **egyszer építjük meg és két helyen
jelenítjük meg** (a B16.7 séma-alapú megközelítése ezt támogatja). Ha mások,
akkor kétszer építjük. **Ez hetekben mérhető különbség.**

#### `[ELDÖNTVE]` B16.10 — A LELTÁR: az EGYETLEN jogos „felülírás", és hogyan legyen mégis mozgás

**A felhasználó kiegészítése (2026-08-22):** kell egy **dedikált Leltár funkció**,
ami **igenis felül tudja írni a készletet** — mert **ez a szerepe**: megadják, hogy
egy adott időpontban ténylegesen mennyi van az alapanyagból.

**Igaza van, és ez NEM mond ellent a B16.4 szabálynak** — ha jól építjük meg.

##### A megoldás: a leltár sem egyenleget ír felül, hanem KORREKCIÓS MOZGÁST hoz létre

| Rossz megvalósítás | Helyes megvalósítás |
|---|---|
| `készlet = 40` | `megszámolva: 40; a rendszer szerint 43; **korrekciós mozgás: −3**, ok: leltár` |
| Az előzmény eltűnik | **Az előzmény megmarad, az eltérés látszik és riportálható** |
| Nem derül ki, mennyi volt a hiány | **Pont a hiány a leltár EREDMÉNYE** — ez az egész értelme |

**Ez ugyanazt éri el, amit a felhasználó kér** (a megszámolt mennyiség lesz az új
készlet), **de közben megmarad az, amiért az egész készletmodell mozgás-alapú:**
az eltérés **kimutatható, riportálható, és a „Kalkulált veszteség %"-hoz
(spec 15./25.) hozzámérhető.** Egy néma felülírásnál épp az az adat veszne el,
amiért leltározunk.

##### `[!]` IDŐZÍTÉSI CSAPDA — ez a leltár klasszikus, néma hibája

**A megszámolás ideje és a rögzítés ideje NEM ugyanaz.** A pultos 22:00-kor
megszámolja, de csak 23:30-kor viszi be a gépbe — miközben a bár tovább árul.

- Ha a rendszer az eltérést **a rögzítés pillanatának** készletéhez méri, akkor
  **az 1,5 óra alatt eladott mennyiséget hiányként könyveli el**, majd a
  korrekcióval **kitörli az időközbeni eladásokat a készletből.**
- **Ez §7 elveszett-frissítése**, és **teljesen hihetőnek látszik** — a szám
  „stimmel", csak rossz.

**Kötelező szabály:** a leltárnak **saját, megadott FORDULÓNAPJA/időpontja** van,
és az eltérés **az AKKORI készlethez** számolódik, nem a rögzítéséhez. A
fordulónap és a rögzítés között történt mozgások **a korrekció után is
érvényesek maradnak.**

##### Hol futhat a leltár

**A korrekciós mozgást a TELEPHELY könyveli el** (B16.4: a mennyiségi állapot
telephely-autoritatív). A **felhőből kezdeményezhető és rögzíthető** — a webes
felület úgyis közös (lásd `gemini_cloud_spec_en.md` R2) —, de a könyvelés a
telephelyen történik, mozgásként.

##### Amit ez maga után von

- **Jogosultság:** a leltári korrekció **készletet és így árrést módosít** —
  lopásgyanúnál pont ez a művelet a gyanús. **Jogosuláshoz kötve, teljes
  audittal, indoklással** (C7).
- **Részleges leltár** (csak egy raktár, csak egy termékcsoport) legyen
  lehetséges — a nem leltározott tételekhez **ne keletkezzen korrekció**.
  Néma nullázás tilos.
- Kapcsolódik: spec 15. (standolás, kalkulált veszteség %), 22. (standoló app),
  25. (valós árrés).

#### `[ELDŐNTVE]` B16.11 — TÖBB TELEPHELY, nem csak franchise

**A felhasználó pontosítása:** a több üzlet **nem csak franchise-kérdés** — lehet
olyan ügyfél, akinek **három különálló üzlete** van, és **egy felületen** akarja
kezelni őket.

**Következmény:** a hierarchia **nem „franchise-funkció", hanem alapmodell.**
A lánc/csoport szint akkor is létezik, ha nincs franchise — csak akkor
egyszerűen „ennek a tulajdonosnak a három üzlete".

**És a statisztika hatóköre ezzel érdemben bővül** (a felhasználó kiemelte):
minden kimutatásnak, lekérdezésnek és menedzsment-funkciónak működnie kell
- **egy üzletre**,
- **több, kiválasztott üzletre**,
- **a teljes csoportra / franchise-ra.**

**`[!]` Ez nem „egy szűrő a riportokon".** Az összesítés **több telephely
adatainak összefésülését** jelenti, ami:
- **eltérő árakkal** (ha nem zárolt), **eltérő ÁFA-időszakokkal**, **eltérő
  nyitvatartással és üzleti nap-határral** dolgozó helyeket ad össze;
- **`[!]` és pont ezért kell a „mit jelent az összeg" kérdést eldönteni**:
  két üzlet „napi forgalma" nem adható össze naivan, ha az egyik üzleti napja
  04:00-kor, a másiké 06:00-kor fordul.
- **`[ ]` Eldöntendő:** a csoportos riport **közös üzleti nap** szerint
  összesít, vagy **telephelyenkénti üzleti nap** szerint, és a kettő
  különbsége **látszódjon-e** a riporton.

**Ez megerősíti, hogy a B7 (multi-tenancy) döntést ezzel EGYÜTT kell meghozni**,
és hogy a több telephelyet átfogó lekérdezés **alapkövetelmény**, nem extra.

#### `[ELDÖNTVE]` B16.12 — A felhő raktár/receptúra = a telephelyi adminfelület

**A felhasználó megerősítette:** *„A felhő raktár- és receptúra-funkciói ugyanazok,
mint a telephelyi adminfelületé, csak máshol megjelenítve."*

**Ez a legjobb hír a paritás-problémára (B16.7)**, és a Gemini-dokumentum
(`gemini_cloud_spec_en.md` §2) konkrét architektúrát is ad hozzá:

> **EGY webes adminisztrációs alkalmazás, KÉT helyről kiszolgálva** — a
> felhő-portálról, és internetkimaradáskor a telephely saját szerveréről.

**Miért ez a legfontosabb következménye:** a §6 szerinti néma szétcsúszás
**gyökerénél szűnik meg** — nincs két felület, amit szinkronban kellene tartani.
Ami marad: a **két backend** (telephelyi szerver / felhő-API) paritása, és épp
erre való a `B16.7` egységes beállítás-séma + paritás-őr.

**→ Ez érdemben csökkenti a fázisterv (E1) egyik legnagyobb tételét: nem kétszer
építjük meg a raktár- és receptúrakezelést.**

#### `[ ]` Ami NYITVA marad ebből

| Tétel | Kérdés |
|-------|--------|
| **B16/a** | Mely beállítások NEM lesznek elérhetők a felhőből? (a felhasználó szerint „kevés kivétel", később tisztázandó) |
| **B16/b** | Ütközés: nem zárolt érték, amit közben helyben is módosítottak — mi nyer? |
| **B16/c** | Sorbaállított változtatás hosszú offline után: csak a végállapot menjen le? |
| **B16/d** | Nagy hatókörű (lánc-szintű) változtatás kap-e extra védelmet? |
| ~~**B16/e**~~ | **`[MEGVÁLASZOLVA]` Azonosak** — egy webes admin alkalmazás, két helyről kiszolgálva. Lásd B16.12. |
| **B16/f** | Csoportos riport: **közös** üzleti nap szerint összesít, vagy **telephelyenkénti** szerint — és látszódjon-e a különbség? |
| **B7** | **A multi-tenancy modellt ezzel EGYÜTT kell eldönteni** — a lánc-szintű összesített lekérdezés igénye szűkíti a lehetőségeket |

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

### `[ELDÖNTVE]` C2/a — ÁRVÁLTOZÁS-TÖRTÉNET: a bizonylat az ELADÁSKORI árat és ÁFÁ-t tárolja

**Döntés (2026-08-22):** a bizonylat **az eladás pillanatában érvényes árat és
adókulcsot tárolja**, nem hivatkozást a termékre.

**Miért kellett kimondani:** enélkül egy áremelés **visszamenőleg átírná a régi
riportokat** — a tavalyi forgalom a mai árakon jelenne meg. És a
`B16` (felhőből, akár láncszinten zárolt ár) után ez **még valószínűbb**, mert
az árat távolról, tömegesen is át lehet írni.

**Amit ez konkrétan jelent:**
- a bizonylattétel tárolja: **a termék azonosítóját ÉS a nevét ÉS az egységárat
  ÉS az adókulcsot ÉS a kedvezményt** — mind az akkori állapot szerint;
- **a NÉV is** — különben egy átnevezett termék visszamenőleg átírja a régi
  nyugták olvasatát;
- ugyanez a szabály él a **receptúrára és a beszerzési átlagárra** is, ha az
  árrés-riportnak visszamenőleg is helyesnek kell lennie. **`[ ]` Ez utóbbi
  külön eldöntendő** — az árrés visszamenőleges pontossága drágább, mint az
  eladási áré.

### `[ELDÖNTVE]` C2/b — TERMÉK ÉLETCIKLUS: inaktiválás, soft delete, és a törlés tilalma

**Döntés (2026-08-22):** egy **már eladott terméket nem szabad törölni** — de az
**inaktiváláson felül** kell egy **soft delete** alternatíva is arra az esetre,
*„ha ténylegesen rossz terméket csináltak és nem akarják javítani."*

#### A három állapot, és mi a különbség

| Állapot | Mikor | Látszik az eladási felületen | Látszik a történetben / riportban |
|---------|-------|------------------------------|-----------------------------------|
| **Aktív** | normál | igen | igen |
| **Inaktív** | szezonális, átmenetileg nem árulják | **nem** | **igen** — és **visszakapcsolható** |
| **Soft-deleted** | elrontott termék, nem javítják | **nem** | **igen** — de **nem szánják visszahozni** |

**`[!]` A LEGFONTOSABB SZABÁLY, ami mindkettőre igaz:**
> **Sem az inaktiválás, sem a soft delete NEM rejtheti el a terméket a
> TÖRTÉNETBŐL.** Egy régi nyugta, riport vagy készletmozgás **továbbra is meg
> kell mutassa**, mit adtak el. Ha a soft delete kiveszi a riportokból,
> **a tavalyi forgalom megváltozik** — ami ugyanaz a hibaosztály, mint a
> `C2/a`-nál.

**A soft delete tehát az ELÉRHETŐSÉGET szünteti meg, nem a TÉNYT.**

#### `[ ]` Amit még el kell dönteni

1. **`[JAVASLAT]` Ha egy termék SOHA nem szerepelt egyetlen bizonylaton vagy
   készletmozgáson sem, akkor legyen ténylegesen TÖRÖLHETŐ.** Ez a tiszta
   megoldás az „elgépeltem, újra létrehozom" esetre — nem hagy szemetet.
   **A kapu: bármilyen felhasználás után már csak soft delete.**
2. **`[ ]` Visszavonható-e a soft delete?** Javaslom: igen, de **külön
   jogosultsághoz kötve** — különben a soft delete és az inaktiválás
   megkülönböztethetetlenné válik a gyakorlatban.
3. **`[ ]` Mi történik, ha a soft-deleted termék szerepel egy RECEPTÚRÁBAN vagy
   egy MENÜBEN?** Néma törés lenne, ha a menü egyik eleme eltűnik.
   **Ellenőrzés kell a művelet előtt**, felsorolva, hol használják.
4. **`[ ]` A vonalkód / gyorsgomb felszabadul-e?** Ha egy soft-deleted termék
   megtartja a vonalkódját, az új termék nem kaphatja meg. Ha felszabadul,
   a régi bizonylatok vonalkód szerinti visszakeresése félrevezet.
   **Eldöntendő** — javaslom: **a vonalkód szabaduljon fel**, mert az fizikai
   azonosító, és a visszakeresés úgyis a bizonylatszámon megy.

### `[ ]` C2 — Árazás
Csak kedvezmények vannak. Hiányzik: happy hour / idősávos ár, zóna szerinti ár
(terasz vs. belső), ár-verziózás (mikortól érvényes), kuponok.

### `[ELDÖNTVE]` C3/a — ÁFA A TERMÉKEN: két kulcs, kötelező kitöltés, NTAK-kategória

**A felhasználó döntése (2026-08-22) — és a felelősség tisztázása:**

> *„az áfa megadása a termékekhez az ügyfél felelőssége, és mi ezért garanciát
> nem is vállalunk, mi csak a lehetőséget kell biztosítsuk."*

**Ez helyes és fontos határkijelölés.** A rendszer **eszközt ad**, nem
adótanácsot. Az 1. ellenőrző kör `L7` leletében leírt jogi finomságok
(helyben készített ital vs. palackozott, a vevő fogyasztási szándéka) **nem a
szoftver feladatai** — de **a szoftvernek lehetővé kell tennie, hogy az ügyfél
helyesen állítsa be őket.** Ezért:

#### Amit a rendszer biztosít

1. **Termékenként KÉT adókulcs megadható:** egy **helyben fogyasztásra**, egy
   **elvitelre**.
2. **Megjelölhető, hogy az elviteles adókulcs MEGEGYEZIK a helyben
   fogyasztásossal** — ekkor a rendszer „másolja" az adókört.
3. **`[!]` BIZTONSÁGI KAPU:** **termék NEM hozható létre adókulcs nélkül**, és
   **akkor sem, ha az egyik adókulcs (pl. az elviteles) hiányzik.**
   **Csak teljesen kitöltött adóadatokkal engedjük létrehozni.**

#### `[!]` HELYESBÍTÉS — az ÉN javaslatom volt HIBÁS, a felhasználóé a helyes

**Azt javasoltam, hogy a „megegyezik" JELÖLŐKÉNT tárolódjon, ne másolt
értékként** — azzal az indoklással, hogy különben a helyben fogyasztásos kulcs
átírásakor az elviteles csendben a régin marad.

**A felhasználó ellenérve erősebb, és elfogadom:**

> Ha az elviteles adókulcs **HIVATKOZÁS**, akkor amikor az ügyfél a helyben
> fogyasztásos kulcsot lejjebb viszi (mert a könyvelő szólt), **az elviteles
> is némán lejjebb megy vele.** A pizza eddig 27% volt mindkét módon; a helyben
> fogyasztásos 18-ra változik; **és az elviteles is 18 lesz — ami súlyos
> szabálysértés.**

**A két hibairány NEM egyenrangú, és ez a döntő érv:**

| Hibairány | Következmény |
|---|---|
| **Túl MAGAS adókulcsot alkalmazunk** | pénzügyi hátrány az ügyfélnek, **de nem jogsértés** |
| **Túl ALACSONY adókulcsot alkalmazunk** | **adóhiány → jogsértés, bírság** |

**Egy hivatkozás-alapú modell épp a veszélyes irányba hibázik automatikusan.**
Egy másolat-alapú modell a biztonságos irányba (marad a régi, magasabb érték,
amíg valaki hozzá nem nyúl). **§13-as gondolkodás: ahol a két hibairány ára
eltér, a mechanizmus a kisebb kár felé dőljön.**

#### `[ELDÖNTVE]` A felhasználó által megadott, elfogadott működés

1. Az ügyfél beírja a **helyben fogyasztásos** adókulcsot.
2. Bepipálja: **„az adókulcsok megegyeznek"** → a rendszer **MÁSOLJA** az
   értéket, és **így menti** (két önálló érték).
3. **Betöltéskor**: ha a két érték egyezik, a jelölő **bepipálva** jelenik meg,
   és az elviteles mező **csak olvasható**, amíg ki nem veszik a pipát.
4. **`[!]` Ha az ügyfél SZERKESZTI a helyben fogyasztásos kulcsot, a jelölő
   AUTOMATIKUSAN kiugrik**, és az elviteles mező **írhatóvá válik, a KORÁBBI
   értékkel.** → **a régi, magasabb érték marad, amíg nem nyúlnak hozzá.**
5. Ha újra egyezővé akarja tenni, **újra bepipálhatja — de meg kell erősítenie.**

**Ez a viselkedés a §5 szellemében is helyes:** a rendszer nem dönt csendben
olyasmiben, aminek adóügyi következménye van — **hanem odaadja a döntést, és
láthatóvá teszi, hogy döntés történt.**

#### `[JAVASLAT]` Az „elviteles alapból a legmagasabb kulcs" ötlethez

A felhasználó felvetette, hogy **az elviteles adókulcs alapból 27% legyen**, és
manuálisan vagy jelölővel lehessen átírni.

**Az elv helyes** (a biztonságos irányba dőljünk), **de a konkrét szám nem
kerülhet a kódba.** §13.1: a beégetett `27` nem egy hiba, hanem egy hibaosztály,
és az adókulcsok változnak.

**Javaslat ugyanarra a célra, beégetés nélkül:**
> Az elviteles adókulcs **alapértelmezése az adott napon érvényes
> adókulcs-táblából a LEGMAGASABB kulcs** — nem a beégetett 27.
>
> Ugyanaz a védelem, de **dátumozott és adatvezérelt** (§13.1, §13.3), tehát egy
> jogszabályváltozás nem igényel kódmódosítást.

**`[ ]` Eldöntendő:** ez az alapértelmezés **előre ki legyen töltve** (az ügyfél
felülírhatja), vagy **üresen hagyva** (és a kapu úgyis kikényszeríti a
kitöltést)? Az előbbi kényelmesebb, az utóbbi kevésbé csábít a
gondolkodás nélküli mentésre. **Javaslom az előre kitöltést**, mert a kapu
(`C3/a` 3. pont) úgyis megvéd a hiánytól, és a magas kulcs a biztonságos irány.

#### `[ ]` Kapcsolódó, még eldöntendő

- **`[ ]` Mi történik a MEGLÉVŐ termékekkel, ha később új kötelező adómező
  jelenik meg?** A kapu csak az újakra hat. A régiek migrációja kell — és amíg
  nincs kitöltve, **jelezni kell**, nem csendben elengedni.
- **`[ ]` Az `L7` szerinti „bruttó ár fix marad" kikötés (spec 9.) CSAK ott
  értelmes, ahol a két kulcs tényleg eltér.** Ahol azonos (pl. alkohol),
  ott nincs mit fixen tartani. Ezt a szabályt ki kell mondani, különben a
  megvalósítás egy nem létező esetre készül.

### `[JAVASLAT — támogatom, két kikötéssel]` C3/c — TERMÉKKATEGÓRIÁK és öröklött adó-alapértékek

**A felhasználó felvetése (2026-08-22):** a termékeket **kötelező főkategóriába
sorolni**, az **alkategória (vagy alkategóriák) opcionális**; és **a fő- és
alkategóriákon is megadható alap adókulcs**, amit az új termék **első körben
örököl**, de **manuálisan és/vagy utólag felülírható.**

**Támogatom.** Két okból jó:
1. **A gyakorlati hibát szünteti meg**, amiért az egész adókapu (`C3/a`) kell:
   a kézzel, terméknént beírt adókulcsnál előbb-utóbb elgépel valaki. A
   kategória-alapérték **a helyes értéket teszi az alapértelmezetté.**
2. **Gyorsítja a telepítést** — ez az `1. ellenőrző kör` `T1.8` leletéhez
   kapcsolódik (hogyan indul el egy új telephely adatokkal). Egy 400 tételes
   itallap felvitele kategória-alapértékekkel nagyságrenddel gyorsabb.

#### `[!]` 1. KIKÖTÉS — az öröklés MÁSOLÁS legyen, ne élő hivatkozás

**Pontosan ugyanaz az érv, amit a felhasználó a `C3/a`-nál helyesen felhozott,
és amiben nekem igaza lett:**

> Ha a kategória adókulcsa **élő hivatkozás**, akkor egy kategória-szintű
> módosítás **egyszerre, csendben átír több száz terméket** — és ha lefelé
> mozdul, az **jogsértés minden érintett terméken egyszerre.**

**Tehát: a kategória adókulcsa ALAPÉRTELMEZÉS a létrehozás pillanatában, és
onnantól a termék saját, önálló értéke.**

**`[JAVASLAT]` Ha a kategória alapértéke később változik**, a rendszer **ne
írjon át semmit magától**, hanem **ajánljon fel egy áttekintett tömeges
frissítést**: „ennek a kategóriának 137 terméke a régi kulcson áll —
átnézed?", listával és egyenkénti kipipálással. **Soha ne néma tömeges írás.**

#### `[ELDÖNTVE — ALULRÓL FELFELÉ öröklés; az ÉN javaslatom volt rosszabb]` 2. kikötés

**Azt javasoltam, hogy adó-alapértéket csak a FŐkategória adhasson**, mert több
alkategóriánál nem tudni, melyik nyer.

**A felhasználó ellenpéldája megcáfolta:**

> Főkategória: **Italok** → 1. szintű alkategória: **Üdítők** → 2. szintű
> alkategóriák: **„helyben készült italok"** és **„dobozos üdítők"**.
>
> A limonádé (helyben készült) **más adókulcs alá eshet**, mint a dobozos üdítő
> fix magasabb kulcsa. **A „Italok" főkategória szintjén ez nem is
> megadható** — ott nincs egyetlen helyes érték.

**A felhasználónak igaza van, és az érv általánosítható:**
> **Minél mélyebb a kategória, annál PONTOSABBAN tudja, mi a helyes adókulcs.**
> A főkategória a leggyengébb hely az adó-alapértéknek, nem a legerősebb.

**ELFOGADOTT SZABÁLY — öröklés ALULRÓL FELFELÉ:**
a rendszer a **legmélyebb alkategóriától indul**, és **felfelé halad** az első
olyan szintig, ami megadja az értéket; **legvégül a főkategóriáig.**

##### `[!]` Amit a mélységi öröklés MEGKÖVETEL — négy pontosítás

**(1) A kategóriaszerkezet FA legyen, ne CÍMKE-halmaz.**
Az „alulról felfelé" **csak akkor egyértelmű**, ha a terméknek **EGY útvonala
van** a fában (Italok → Üdítők → dobozos üdítők). Ha egy termék **egyszerre
több, egymással nem rokon kategóriában** is lehetne (pl. „Üdítők" ÉS „Akciós"
ÉS „Nyári kínálat"), akkor **két azonos mélységű ág is adhatna eltérő
adókulcsot** — és nincs sorrend köztük.

**`[ELDÖNTVE 2026-08-22]`** A felhasználó megerősítette: **egy termék CSAK EGY
legalsó kategóriában szerepelhet, egyenesen — nem lehet több azonos rangú
kategória eleme.** Tehát **szigorú fa, egyetlen útvonallal**, és az alulról
felfelé öröklés **teljesen egyértelmű.**

**Ha később mégis kell csoportosítás promócióhoz vagy navigációhoz**, az legyen
**külön „címke" fogalom, adó-jelentés nélkül** — hogy ne bontsa meg ezt az
egyértelműséget.

**(2) A hiányzó értékek KÜLÖN-KÜLÖN öröklődnek.**
Ha a legmélyebb alkategória **csak a helyben fogyasztásos** kulcsot adja meg, az
elviteleset nem, akkor **az elviteleshez tovább kell menni felfelé** — nem az
van, hogy „az első szint, ami bármit ad, mindkettőt adja".
Enélkül az elviteles üresen maradna, a kapu (`C3/a`) blokkolná a mentést, és a
felhasználó nem értené, miért.

**(3) A létrehozáskor LÁTSZÓDJON, HONNAN jött az érték.**
„27% — örökölve innen: *dobozos üdítők*". Így a felvivő **azonnal látja, ha rossz
kategóriába tette**, és nem utólag, egy adóellenőrzésen. Ugyanaz az elv, mint a
felhőből zárolt áraknál (`B16.3`): **az érték mellett a forrása is látszik.**

**(4) `[!]` Ha egy terméket KÉSŐBB áthelyeznek másik kategóriába, az adókulcsa
NEM változik.** Mert másolat, nem hivatkozás (1. kikötés). **Ezt ki kell írni a
felületre**, különben mindenki azt hiszi, hogy újraöröklődik — és pont az
újraöröklődés lenne a veszélyes irány.
**Javaslat:** áthelyezéskor a rendszer **kérdezze meg**: „az új kategória
alapértéke X — átvegyük?" — döntéssel, ne automatikusan.

**(5) A fa legyen véges és körmentes.** Egy kategória ne lehessen a saját őse
(ez fa-szerkesztőkben klasszikus hibaforrás), és **a mélységnek legyen ésszerű
korlátja** (javaslat: 3–4 szint) — különben az öröklési lánc kibogozhatatlan
lesz, és a felület is használhatatlan.

#### `[!]` 3. FIGYELMEZTETÉS — a Siduri-kategória NEM azonos az NTAK-kategóriával

Két különböző taxonómia, két különböző célra:

| | **Siduri fő-/alkategória** | **NTAK fő-/alkategória** |
|---|---|---|
| Kié | a miénk / az ügyfélé | **az NTAK-é**, jogszabályi lista |
| Mire jó | felület, gyorsgombok, riport, adó-alapérték | **adatszolgáltatás** |
| Változtathatja az ügyfél | igen | **nem** |

**Ha a kettőt egy mezőbe tesszük, mindkettő elromlik:** vagy az ügyfél nem
tudja úgy csoportosítani a felületet, ahogy neki jó, vagy elrontja az
adatszolgáltatást. **Két külön mező kell.**

**`[JAVASLAT]` Ami viszont hasznos és olcsó:** a **Siduri-kategórián is
megadható legyen egy NTAK-kategória alapértelmezés** — ugyanazzal a
másolás-nem-hivatkozás szabállyal. Így az „Üdítők" kategóriába felvett új
termék automatikusan a helyes NTAK-besorolást kapja, **és ez pont azt a
kritikus pillanatot enyhíti** (`C3/b` 1. pont), amikor egy hely utólag válik
NTAK-kötelessé.

### `[ELDÖNTVE]` C3/b — NTAK-KATEGÓRIA a terméken: feltételesen kötelező

**A felhasználó döntése:** az NTAK fő- és alkategória **kiválasztását biztosítani
kell a termékekhez**, de:

| A hely állapota | Az NTAK-kategória |
|---|---|
| **Nincs NTAK-kulcs beillesztve** (nem NTAK-köteles) | **NEM kötelező**, és **ne is figyelmeztessünk** rá |
| **Van NTAK-kulcs** (integrálva van) | **kötelező** — vagy legalábbis **erősen figyelmeztetünk** a kötelezettségre |

**Ez jó tervezés:** a rendszer **abból következtet, amit tud** (van-e kulcs),
nem kérdezget feleslegesen. §5 fordítottja: ne zaklassunk olyasmivel, ami az
adott helyen nem értelmezhető.

#### `[ ]` Amit ez megkövetel

1. **`[!]` A kulcs beillesztésének PILLANATA a kritikus.** Amikor egy hely
   utólag NTAK-kötelessé válik és beteszi a kulcsot, **az összes MEGLÉVŐ terméke
   kategória nélkül áll.** Kell rá:
   - **tömeges kitöltő felület** (kategória hozzárendelése termékcsoportokhoz),
   - **és egy le nem tűnő jelzés**, amíg van kategória nélküli, forgalmazott termék.
   **Enélkül az adatszolgáltatás hiányos lesz, és az csendben történik.**
2. **`[ ]` Kötelező vagy csak figyelmeztetés?** A felhasználó a kettő közül
   nem választott („vagy legyen kötelező… vagy erősen figyelmeztessük").
   **Javaslom: figyelmeztetés a termék mentésekor, DE kemény tiltás az
   ÉRTÉKESÍTÉSRE** — kategória nélküli terméket ne lehessen eladni olyan
   helyen, ami NTAK-integrált. Így a rögzítés nem akad meg, de hiányos adat
   nem kerül forgalomba. **Döntést igényel.**
3. **Az NTAK-kategórialista ADATVEZÉRELT és VERZIÓZOTT legyen** (§13.1, §13.3) —
   a lista változhat, és **kódkiadás nélkül frissíthetőnek kell lennie.**

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

### `[!] [ÚJ, IGAZOLT LELET]` C11/a — AZ NTAK-HOZ MTÜ-IGAZOLÁS KELL A SZOFTVERNEK

> **Ez a 2. legsúlyosabb lelet az egész átvizsgálásban** (az online pénztárgépek
> 2028-as kifutása után), és **eddig sehol nem szerepelt a tervben.**

#### A tény

> **„az adatszolgáltatásra kizárólag az NTAK-kal kommunikálni képes, az MTÜ által
> kiállított Igazolással rendelkező vendéglátó szoftverek használhatóak."**

A folyamat: a szoftvergyártó megkapja az **RMS Interfész leírást**, felkészül,
majd **validációs tesztet** kell teljesítenie. Sikeres teszt után az **MTÜ
Igazolást állít ki**, felveszi a szoftvert az NTAK RMS-adatbázisába, és kiadja az
**éles környezeti azonosítót**. A tesztkörnyezethez **telephelyenkénti NTAK RMS
(teszt) tanúsítvány** kell, és a beküldött üzeneteket **elektronikusan alá kell
írni.**

**Forrás:** [NTAK — Vendéglátás információs oldal](https://info.ntak.hu/vendeglatas),
[RMS Interfész leírás v1.06 (PDF)](https://info.ntak.hu/media/uploads/docs/RMS_Interfesz_leiras_v106.pdf),
[NTAK Vendéglátás szakmodul felhasználói útmutató](https://info.ntak.hu/media/uploads/docs/ntak_vendeglatas_szakmodul_felhasznaloi_utmutato.pdf).

#### `[!]` Miért ez súlyos a terv szempontjából

**A célpiac definíció szerint NTAK-köteles.** A `siduri_spec_hu.md` 1. pontja
szó szerint: *„Magyar KKV vendéglátás (12 millió Ft árbevétel feletti, **NTAK
köteles** helyek)."*

> **Tehát: MTÜ-igazolás nélkül a Siduri a saját megcélzott piacát jogszerűen
> nem tudja kiszolgálni.** Ez nem „jó lenne", hanem **belépési feltétel.**

**Ez egy KAPU a fázistervben, átfutási idővel** — nem egy fejlesztési feladat,
amit párhuzamosan el lehet végezni. A validációs teszthez **kész, működő
adatszolgáltatásra van szükség**, tehát a sorrend kötött:
adatmodell → NTAK-modul → tesztkörnyezet → validációs teszt → Igazolás → **csak
ezután élesíthető NTAK-köteles helyen.**

#### Amiért ez mégis JOBB hír, mint a fiskális oldal

| | **NTAK (MTÜ)** | **Fiskális eszköz (gyártó)** |
|---|---|---|
| Van-e nyilvános interfész-leírás | **IGEN** — az RMS Interfész leírás **letölthető** | `[?]` valószínűleg NDA-hoz kötött |
| Van-e tesztkörnyezet | **IGEN**, nevesítve | `[?]` gyártófüggő |
| Ki a partner | **egy** szervezet (MTÜ) | **gyártónként külön** |

**Tehát az NTAK-integráció MOST elkezdhető** — a specifikáció a kezünkben van,
nem kell hozzá senkivel szerződni előbb. **Ez a `E3` beszerzési tétel egyik
darabját azonnal kiveszi a blokkolók közül.**

#### `[ ]` Amit ez azonnal megkövetel

1. **`[ ]` Az RMS Interfész leírás v1.06 letöltése és feldolgozása** — ez a
   **konkrét adatmodell-követelmény** az értékesítési adatokra. **Ez befolyásolja
   a termék-, kategória- és bizonylat-modellt**, tehát **a kódolás előtt kell
   elolvasni**, nem közben.
2. **`[!]` Tanúsítványkezelés mint FUNKCIÓ.** Telephelyenkénti tanúsítvány +
   üzenetaláírás → **kiadás, tárolás, megújítás, lejárat-figyelés, több
   telephely.** Ez a `C11` eredeti „tanúsítványkezelés" aggálya, **most már
   igazoltan.** És a `B10/a` fényében: **a tanúsítvány privát kulcsa egy
   pult mögött álló gépen lesz** — védeni kell.
3. **`[ ]` A validációs teszt a FÁZISTERV nevesített mérföldköve legyen**, saját
   időkerettel, mint a mérési fázis.
4. **`[ ]` Az MTÜ-igazolás VERZIÓHOZ kötött** — „a kiállítás napján érvényes
   követelményeknek való megfelelést igazolja". **Kérdés: minden szoftververzió
   után újra kell-e validálni?** Ez a `D3` (verziókompatibilitás) és a
   `siduri-updater` szempontjából is fontos. **Utánajárandó.**

#### `[!]` HELYESBÍTÉS a felhasználó feltevéséhez

A felhasználó (2026-08-22) így fogalmazott: *„az NTAK adatszolgáltatást minden
esetben vagy a szoftware **vagy a felhasználó végzi az NTAK felületén**."*

| Állítás | Ítélet |
|---|---|
| A pénztárgép nem küld az NTAK-nak | **IGAZ** — a pénztárgép a NAV felé küld forgalmi adatot; az NTAK statisztikai adatot kap, azt a szoftver küldi |
| A napi adatszolgáltatást a szoftver végzi | **IGAZ**, és **automatikusan**, a nap lezárása után |
| A felhasználó kézzel is beküldheti az NTAK felületén | **`[!]` NEM IGAZOLT — a forrás szerint erre nincs mód.** A napi adatszolgáltatásra **kizárólag MTÜ-igazolással rendelkező szoftver** használható. Az NTAK online felületén a **regisztrációs adatok** (nyitvatartás, üzlettípus) módosíthatók, nem a napi forgalmi adat |

**Miért fontos ez a különbség:** ha lenne kézi út, akkor az `1. fiskális mód`
(Siduri mint belső rendszer, adóügyi eszköz nélkül) esetén az ügyfél maga
megoldhatná. **Így viszont nem.** Ebből következik:

> **Az `1. módban` (belső rendszer) egy NTAK-köteles hely számára az
> adatszolgáltatást is A SIDURINAK kell teljesítenie** — vagy a hely
> **egy másik, igazolt szoftvert is használ** mellette.
> **Ez az 1. mód alatt nyitva hagyott kérdést megválaszolja.**

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

### `[ELDÖNTVE — mind a négy nap definiálva]` F4 — A NAP-FOGALMAK

> **A felhasználó definíciói (2026-08-22).** Ez lezárja az `F4` tételt és az
> 1. ellenőrző kör `T1.1` leletét is: eddig **négy nap-fogalom élt a tervben,
> egyik sem definiálva.**

| Fogalom | Definíció | Kihez tartozik |
|---------|-----------|----------------|
| **MUNKANAP** (üzleti nap) | A rendszerben nyitott Munkanap **nyitásától a lezárásáig** tartó, **legfeljebb 25 órás** intervallum. **Nem naptári nap**, lehet eltolódás. **Ugyanarra a dátumra több Munkanap is nyitható.** | **A HELY EGÉSZE** — minden eszközre közösen |
| **MŰSZAK** (adóügyi munkanap) | Az adóügyi eszköz saját munkanapja. **Minden eszköz külön Műszakot nyit** a Munkanapon belül, zárhatja és nyithat újat. | **ESZKÖZÖNKÉNT** |
| **NTAK TÁRGYNAP** | Az adott értékesítés **naptári napja**. | jogszabályi fogalom |
| **NAPTÁRI NAP** | 00:00 – 23:59. | — |

#### A Munkanap időzítése

- **23 óra 30 perc** eltelte után **figyelmeztetés**: a Munkanapot 24 óránként
  le kell zárni.
- **1 óra türelmi idő.**
- **25 óra letelte után MINDEN GÉP MEGÁLL** — nincs értékesítés, amíg új
  Munkanapot nem nyitnak.

#### Miért jó ez a modell

**A Munkanap a helyé, a Műszak az eszközé** — és ez tisztán megoldja azt, ami
eddig kavarodás volt: „egy Munkanapon több Műszak" kérdése **szerkezetileg**
oldódik meg, nem szabállyal.

---

#### `[!]` HÁROM KÖVETKEZMÉNY, amit ez a definíció TEREMT

##### `[!] K1 — A BIZONYLATSZÁM ÜTKÖZIK, ha egy dátumra több Munkanap esik`

**A felhasználó maga jelezte:** *„lehet több munkanapot is nyitni ugyanarra a
dátumra is, ezt is le kell majd kezelni valahogy a nyugtaszámokat illetően."*

**A probléma pontosan:** a bizonylatszám `xxxxxxyyyzzzzz`, ahol `xxxxxx` a
**dátum**. Ha a folyószám (`zzzzz`) **Munkanaponként** indul újra, és **két
Munkanap ugyanarra a dátumra esik**, akkor a 3-as eszköz **mindkét Munkanapon
kiadja a `26082200300001`-et** → **duplikált bizonylatszám.**

**JAVASOLT MEGOLDÁS — a legegyszerűbb, ami működik:**

> **A folyószám ne MUNKANAPONKÉNT induljon újra, hanem DÁTUMONKÉNT.**
> A számláló kulcsa: **(eszköz, dátum-előtag)** — nem (eszköz, Munkanap).
>
> Ha egy dátumra második Munkanap nyílik, a számláló **egyszerűen folytatódik**
> ott, ahol az első abbahagyta. **Ütközés nem keletkezhet**, a formátum nem
> változik, és a napi 99 999-es keret **több Munkanapra is bőven elég.**
>
> **Melyik Munkanaphoz tartozott a bizonylat, az KÜLÖN MEZŐ** — nem a
> sorszámból olvassuk ki. (Amúgy sem lenne szabad: §8, a megjelenített/származtatott
> érték nem alkalmas állapot-felismerésre.)

**Ez a legkisebb változtatás, ami a problémát megszünteti** — nem szabállyal
kezeli, hanem **nem engedi keletkezni.** `[ ]` **Jóváhagyásra vár.**

##### `[ELDÖNTVE + TERV]` K2 — A MUNKANAP OFFLINE NYITÁSA ÉS ÖSSZEFÉSÜLÉSE

**A felhasználó pontosítása (2026-08-22):** a Munkanapot **bármelyik gépen meg
lehet nyitni**, de **a szerver tartja számon**, és **ő kommunikálja a kliensek
felé.** Kiesésnél ez a szerep a tartalék szerverre száll. **Marad a nehéz eset:
mi van, ha minden offline** — és akkor akár **öt Munkanap** is nyílhat ugyanarra
a dátumra, amiket **össze kell hozni.**

> **A felhasználó kérése:** *„ennek a megoldására nagyban számítok a
> segítségedre és ha van esetleg egy konkrét, pontos ötleted, azt mondd."*
> Az alábbi a javaslatom, **négy rétegben**. A lényeg: **három réteg megelőzi a
> problémát, és csak a negyedik javít** — mert az összefésülést nem megoldani
> kell, hanem **nem engedni keletkezni.**

---

###### `[!]` ELŐSZÖR A JÓ HÍR: az összefésülés MÁR MOST sokkal kisebb probléma, mint amilyennek látszik

**Három dolog, ami NEM sérül egy összefésüléskor** — és ezek a legdrágábbak
lennének:

| | Miért nem sérül |
|---|---|
| **A bizonylatszámok** | A `K1` döntés óta a szám a **DÁTUMHOZ** kötődik, **nem a Munkanaphoz.** Egy bizonylat átsorolása másik Munkanap alá **nem változtat egyetlen kinyomtatott számot sem.** |
| **A fiskális oldal** | A Z-jelentések a **MŰSZAKHOZ** tartoznak, ami **eszközönkénti** — és a modell szerint **egy Munkanapon több Műszak is normális.** Az adóügyi eszközön **semmit nem kell összefésülni.** |
| **Az NTAK-adatszolgáltatás** | Az NTAK egysége a **tárgynap = naptári nap**, nem a Munkanap. **Az összefésülés az NTAK-küldést nem érinti.** |

**Vagyis az összefésülés kizárólag a BELSŐ riportokat érinti** — a Munkanapra
vetített forgalmat, a műszakegyeztetést, a napi zárást. **Egyetlen külső,
jogilag kötött rendszer sem függ tőle.**

**Ez nem szerencse, hanem a `K1` döntés hozadéka** — érdemes látni, hogy a
döntések itt összeértek.

---

###### 1. RÉTEG — MEGELŐZÉS: a szerver ELŐRE kiosztja a következő Munkanap azonosítóját

**Ez a legerősebb és a legolcsóbb elem, és eddig nem merült fel.**

> Amíg a szerver **egészséges**, minden eszköznek **előre odaadja a KÖVETKEZŐ
> Munkanap azonosítóját** — egy generált azonosítót, dátum nélkül.
>
> Ha később a szerver kiesik, és egy eszköznek Munkanapot kell nyitnia,
> **azt az előre kapott azonosítót használja.**
>
> **Mivel MINDEN eszköz UGYANAZT az azonosítót kapta, mindegyik UGYANAZT a
> Munkanapot nyitja meg — akkor is, ha egymást sem látják.**
> **Nincs mit összefésülni.**

**Miért működik teljes hálózati összeomlásnál is:** az azonosítót **még a baj
előtt** kapták meg. Nem kell hozzá kommunikáció a nyitás pillanatában.

**Mi kell hozzá:** egy mező az eszköz helyi tárában, és a szerver adja hozzá
minden szinkronhoz. **Gyakorlatilag ingyen van.**

**Mikor NEM elég:** ha egy eszköz **nem volt online**, amikor az azonosítót
kiosztották (pl. most hozták be). Akkor nincs tokene → a 2. réteg lép.

###### 2. RÉTEG — MEGELŐZÉS: kérdezd meg a tanúkat nyitás előtt

**Ez már el van döntve** (`B14.7`), itt csak megerősítem és élesítem:

> **A Munkanap offline nyitása ELŐTT a gép kötelezően megkérdezi az elérhető
> tanúkat** (a többi Windows POS, a tartalék szerver, KDS, kijelző):
> **„van nálad nyitott Munkanap?"**
>
> - **Ha bárkinél van → ÁTVESZI azt**, nem nyit újat.
> - Ha senkinél sincs, de van előre kapott azonosítója → azt használja (1. réteg).
> - Ha egyik sem → **csak ekkor** nyit sajátot.

**Az 1. és 2. réteg együtt lefedi a reális esetek túlnyomó részét.** Több
Munkanap **csak akkor** keletkezik, ha a gépek **egymást sem látják** ÉS
**nem volt előre kiosztott azonosítójuk** — ez már ritka együttállás.

###### 3. RÉTEG — JAVÍTÁS: automatikus átsorolás, KIZÁRÓLAG azonos dátumon belül

Ha mégis több Munkanap keletkezett **ugyanarra a dátumra**, a szerver
visszatéréskor **automatikusan összevonja őket.** A művelet:

1. **Túlélő kiválasztása:** a **legkorábban nyitott** Munkanap marad meg.
2. **Átsorolás:** a többi Munkanap **összes bizonylata és eseménye** a túlélő alá
   kerül. **Egyetlen bizonylatszám sem változik** (lásd fent).
3. **Időhatárok:** a túlélő nyitása a **legkorábbi**, zárása a **legkésőbbi**.
4. **Továbbmutató nyom:** a beolvasztott Munkanapok **nem tűnnek el**, hanem
   „beolvasztva ide: X" állapotot kapnak. **Ez kritikus**, mert:
5. **Késve érkező eszköz:** ha egy gép csak napokkal később csatlakozik vissza,
   az ő bizonylatai egy **már beolvasztott** Munkanapra hivatkoznak — a
   továbbmutató nyom alapján **automatikusan a túlélő alá kerülnek.**
   Enélkül ezek árván maradnának.
6. **Naplózás:** az összevonás **auditált esemény** — mit, mibe, mikor, hány
   bizonylattal.

**`[!]` Két szabály, ami nélkül a saját rendszerünk utasítaná el a javítást:**

- **A 25 órás korlát a NYITÁSRA vonatkozik, nem az összefésült Munkanapra.**
  Ha az egyik gép 06:00-kor, a másik 20:00-kor nyitott, az összevont Munkanap
  **hosszabb lehet 25 óránál** — ez **utólagos tény**, nem szabálysértés.
  Az érvényesítés ne bukjon el rajta.
- **Az összevont Munkanap „összevont" jelölést kap**, és **a menedzsernek
  látnia kell**, mielőtt lezárja. **A rendszer az adatot rendbe teszi
  automatikusan, de a TÉNYT nem hallgatja el** (§5).

###### 4. RÉTEG — ESZKALÁCIÓ: eltérő DÁTUM nem összefésülhető

**`[!]` Ha a Munkanapok DÁTUMA eltér** (mert az egyik gép órája rossz volt),
**az NEM összefésülési feladat.**

**Miért:** a **dátum benne van a kinyomtatott bizonylatszámban.** Két különböző
dátum-előtaggal kiadott bizonylatot **nem lehet egy dátum alá vonni** — a papír
már a vendégnél van.

**Ez tehát óra-incidens**, aminek a feloldása:
- **emberi**, dokumentált, indoklással;
- a rendszer **kilistázza pontosan**, melyik gép melyik dátumon mit adott ki;
- és **ez a legerősebb érv a `B14.7` óra-monotonitás védelem mellett** — mert
  az ilyen incidenst **meg kell előzni**, javítani már nem lehet rendesen.

---

###### Összefoglalva: a négy réteg együtt

| Réteg | Mit tesz | Költség |
|-------|----------|---------|
| **1. Előre kiosztott azonosító** | **megelőzi** — mindenki ugyanazt nyitja | **elhanyagolható** |
| **2. Tanúk megkérdezése** | **megelőzi** — átveszi a meglévőt | már eldöntött mechanizmus |
| **3. Automatikus átsorolás** | **javít**, azonos dátumon belül | közepes, de mechanikus |
| **4. Emberi feloldás** | eltérő dátum — óra-incidens | ritka, dokumentált |

**A lényeg: a felhasználó félelme („lehet 5 Munkanap is, amiket egybe kell
hozni") jogos, DE az 1. és 2. réteggel ez az eset nagyrészt meg sem történik** —
és amikor mégis, a 3. réteg **mechanikus**, mert a `K1` döntés miatt
**egyetlen kinyomtatott számhoz sem kell hozzányúlni.**

**`[ ] Jóváhagyásra vár.**

##### `[!] K3 — A MŰSZAK = adóügyi napzárás, tehát a fiskális napszámláló GYORSABBAN fogy`

Ha a **Műszak** az adóügyi eszköz munkanapja, akkor **a Műszak lezárása fiskális
napzárást (Z-jelentést) vált ki** az eszközön — nem csak Siduri-oldali könyvelés.
**Ezt ki kell mondani**, mert különben valaki „csak egy Siduri-státuszváltásnak"
fogja megvalósítani.

**És van egy számszerű következménye:** a fiskális azonosítóban a napszámláló
4 jegyű (9999 zárás). Korábban **napi egy zárással ~27 évet** számoltam.
**Ha egy hely naponta 3 Műszakot zár, az ~9 év.** Nem riasztó, de
**nem is 27** — és a szám a tervben szerepel, tehát pontosítom.

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

### `[ELDÖNTVE]` F7/a — SZERKESZTHETŐ JOGOSULTSÁGI SZINTEK (2026-08-22)

**A felhasználó döntése:** az egyedi, felhasználónkénti jogkörök **mellett** az
ügyfél **maga is létrehozhat és módosíthat jogosultsági SZINTEKET** — ne csak az
általunk előre megadottak létezzenek.

**Indoklás a felhasználótól:** ha kell egy „Pultfőnök" szint, azt az ügyfél
csinálja meg egyszer, ahelyett hogy **hat pultosnak külön-külön** kellene egyedi
jogkört állítani.

**Ez helyes**, és megszünteti azt a hibaosztályt, hogy hat, kézzel beállított
jogkör közül **ötben lesz ugyanaz, a hatodikban véletlenül nem** — és senki nem
veszi észre.

#### `[!]` A frissítési csapda, amit ez teremt — ez a legfontosabb következmény

**Kiadunk egy új verziót, ami bevezet egy ÚJ jogosultságot** (mert új funkció
került a rendszerbe). **Mi legyen ez az új jogosultság az ügyfél SAJÁT,
korábban létrehozott „Pultfőnök" szintjén?**

- **Ha alapból ENGEDÉLYEZETT:** egy frissítés **csendben jogot ad** olyan
  embereknek, akiknek az ügyfél sosem adta meg. (Például: a pultosok hirtelen
  sztornózhatnak.) **Ez elfogadhatatlan.**
- **Ha alapból TILTOTT** (a helyes választás): az új funkció **némán nem
  működik** azoknak, akiknek működnie kellene, és a támogatás azt fogja hallani,
  hogy „a frissítés után elromlott".

**Döntés: TILTOTT alapból** — a biztonságos irány —, **DE ez önmagában nem elég**
(§5: néma kudarc). **Kötelező mellé:**
- a frissítés után az admin felület **feltűnően jelezze**: „a frissítés N új
  jogosultságot vezetett be, egyik szint sem kapta meg — nézd át";
- a lista legyen **egy kattintással elérhető és tömegesen kiosztható**;
- **amíg át nem nézték, a jelzés ne tűnjön el.**

**Ugyanez vonatkozik az ÁLTALUNK szállított alapszintekre:** ha az ügyfél
módosított egy általunk adott szintet, egy frissítés **NEM írhatja felül némán**
a módosítását. Vagy másolatként szerkeszti (a mi szintjeink sablonok), vagy a
módosított szint „testreszabott" jelölést kap, és a frissítés **nem nyúl hozzá**,
csak jelzi az eltérést.

#### `[ ]` Amit a szerkeszthető szintek még megkövetelnek

- **`[!]` Jogosultság-emelés önmagának.** Aki szerkesztheti a szinteket,
  **bármit megadhat magának** — ez tervezési szinten privilégium-emelés.
  Szabály kell rá: **nem adhatsz olyan jogot, amivel te magad nem
  rendelkezel**, vagy a szint-szerkesztés joga szigorúan szűk körhöz kötött.
  **Eldöntendő, melyik.**
- **Feloldási sorrend** szint és egyedi kivétel között (ez az `F7` eredeti
  nyitott kérdése) — szerkeszthető szintekkel **élesebb**: mi nyer, ha a szint
  tilt, de az egyedi kivétel enged?
- **Szint törlése**, amihez felhasználók vannak rendelve — mi történik velük?
  (Néma jogvesztés tilos.)
- **Több telephely / lánc (B16.2):** a szint **lánc-szinten** definiálódik és
  öröklődik lefelé, vagy telephelyenként külön? **Zárolható-e?**
  Ez ugyanaz a hierarchia-kérdés, mint az áraknál.

### `[ELDÖNTVE]` F7/b — A SIDURI ADMIN FIÓK sérthetetlensége és az OFFLINE BELÉPÉS

#### A követelmény, ahogy a felhasználó megfogalmazta (2026-08-22)

1. **A Siduri admin felhasználó „szent és sérthetetlen":** az ügyfél
   **nem módosíthatja**, **nem csökkentheti a jogkörét**, **nem változtathat
   rajta jelszót.**
2. **Kell egy FIX belépési lehetőség**, mert *„ha nincs internet vagy
   szerverkapcsolat egy gépen, amit javítanunk kell, akkor is be kell tudni
   lépni, mégha egy frissítés előtti jelszóval is."*

**A felhasználó a biztonsági aggályt (lásd `gemini_cloud_spec_en.md` R4)
megértette, és ennek ismeretében tartja fenn a követelményt.** A követelmény
tehát adott; a kérdés már csak az, **hogyan valósítjuk meg a legkevesebb
kockázattal.**

#### `[JAVASLAT]` Ugyanez a képesség, TELEPHELYENKÉNTI hitelesítő adattal

**A követelmény minden szava teljesíthető úgy is, hogy NE egyetlen közös titok
legyen minden ügyfél gépén.** A különbség nem a funkcióban van, hanem a
kompromittálódás hatósugarában:

| | Globális, közös jelszó | **Telephelyenkénti hitelesítő adat** |
|---|---|---|
| Offline belépés | ✔ | ✔ |
| Régi jelszóval is működik | ✔ | ✔ |
| Nem kell hozzá internet | ✔ | ✔ |
| **Egy kiszivárgás hatása** | **MINDEN ügyfél, minden gépe** | **egy telephely** |
| Rotálható a többi érintése nélkül | ✘ | ✔ |

**Konkrétan:** telepítéskor minden telephely **saját** szerviz-hitelesítő adatot
kap. Online állapotban ez cserélhető, de **a régi addig érvényes marad, amíg az
új visszaigazoltan meg nem érkezett** — így teljesül a felhasználó kikötése,
hogy „mégha egy frissítés előtti jelszóval is" be lehessen lépni.

**Még erősebb változat, ha később belefér — challenge–response:** a gép kiír egy
kódot, a support a felhőből generál rá **időkorlátos** választ. Ekkor a gépen
**semmilyen újrafelhasználható titok nem pihen.** Offline is működik (telefonon
bediktálható). **Ennek a hátránya**, hogy a support oldalán kell hozzá elérhető
generátor — ha az nem megy, nincs belépés. **Ezért javaslom a kettőt együtt:**
challenge–response az elsődleges út, telephelyenkénti fix hitelesítő adat a
végső tartalék.

#### Kötelező kísérő intézkedések — ezek nélkül a fix belépés nyílt hátsó ajtó

1. **Sebességkorlát és zárolás.** Fix hitelesítő adat egy **fizikailag
   hozzáférhető** gépen: próbálgatás elleni védelem nélkül idő kérdése a betörés.
2. **`[!]` TELJES, TÖRÖLHETETLEN AUDIT, ami az ÜGYFÉL SZÁMÁRA IS LÁTHATÓ.**
   Ez a legfontosabb enyhítés, és nem csak technikai: **egy szerviz-belépés,
   amit a tulajdonos utólag lát a naplóban, gyökeresen más dolog, mint egy
   rejtett hátsó ajtó.** Rögzítendő: mikor, melyik gépen, ki, milyen jogcímen,
   és **mit csinált**.
3. **A belépés legyen látható a gépen is**, amíg tart (pl. állandó sáv:
   „szerviz-hozzáférés aktív"). Ne lehessen észrevétlenül bent ülni.
4. **Időkorlát:** a szerviz-munkamenet magától záruljon le.

#### `[!]` Egy következmény, amit ki kell mondani — nem mérnöki, hanem szerződéses

A „sérthetetlen, korlátozhatatlan jogkörű" szolgáltatói fiók azt jelenti, hogy
**a Siduri Systems állandó, az ügyfél által nem korlátozható hozzáféréssel
rendelkezik minden ügyfél teljes üzleti és személyes adatához.**

**Ez tényként rögzítendő, nem elhallgatandó:**
- **adatvédelmi szempontból** ez adatfeldolgozói (esetenként adatkezelői)
  viszonyt keletkeztet, amit **a szerződésben és az adatkezelési tájékoztatóban
  szerepeltetni kell** — kapcsolódik `B7`-hez és `B10/a`-hoz;
- **`[?]` hogy ehhez pontosan mi szükséges jogilag, azt NEM tudom forrás nélkül
  megmondani** (§13.5) — **a jogi ellenőrzési kör tétele**;
- **üzletileg** ez egy nagyobb ügyfélnél (lánc, franchise) **kérdés lesz az
  értékesítési tárgyaláson** — jobb felkészülten válaszolni rá, mint
  meglepődni. A 2. pont (látható audit) itt a legjobb érv.

#### `[!]` A sérthetetlenséget a KÓDBAN kell kikényszeríteni, nem a felületen

Ha csak a felület nem kínálja fel a szerkesztést, akkor **egy importálás, egy
API-hívás vagy egy közvetlen adatbázis-írás megkerüli.** A szabály:
**a szolgáltatói fiók módosítására, jogkörcsökkentésére és törlésére irányuló
kérés a szerveren utasítódjon el**, minden belépési ponton, **egy közös
kikényszerítő helyen** (§3.5) — és a kísérlet **naplózódjon**, mert az önmagában
is jelzés.

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
| 1 | **`[!]` C11/a — MTÜ-igazolás az NTAK-hoz** | **IGAZOLT LELET, kapu a fázistervben** | **Az NTAK-adatszolgáltatásra kizárólag MTÜ-igazolással rendelkező szoftver használható**, validációs teszt után. A célpiac definíció szerint NTAK-köteles → **igazolás nélkül a Siduri a saját piacát nem tudja kiszolgálni.** JÓ HÍR: az interfész-leírás **nyilvános és letölthető**, tesztkörnyezet van → **azonnal elkezdhető.** |
| 2 | **Fiskális: kell-e engedély a MI szoftverünknek?** | `[?]` **NEM eldönthető nyilvános anyagból** | Ha igen, hetekben-hónapokban és pénzben mérhető. Közvetlen kérdés a NAV-hoz és egy gyártóhoz — **korán indítandó**. Lásd `FISKALIS_UZEMMODOK.md` 4.4. |
| 3 | **B17/a — a felhő írás-modellje** | `[ELFOGADVA a javaslat]` | Írás egy helyen automatikus átvétellel, olvasás megosztva. Marad nyitva: szinkron vagy aszinkron a két felhős szerver között, és földrajzi elhelyezés. |
| 4 | **B17/d — a felhő MENTÉSE** | `[ ]` **ÚJ HÉZAG** | A replikáció NEM mentés: a törölt vagy elrontott adat átreplikálódik. A telephelyre ezt már kimondtuk (`D1`), a felhőre nem — pedig ott MINDEN ügyfél adata egy helyen van. |
| 5 | **F4/K2 — a Munkanap-összefésülés terve** | `[ ]` **JÓVÁHAGYÁSRA VÁR** | Négyrétegű javaslat: (1) a szerver előre kiosztja a következő Munkanap azonosítóját → mindenki ugyanazt nyitja, **nincs mit összefésülni**; (2) tanúk megkérdezése; (3) automatikus átsorolás azonos dátumon belül; (4) eltérő dátum → emberi feloldás. |
| 6 | **C3/c — kategória-alapértékek** | `[ ]` **JÓVÁHAGYÁSRA VÁR** | Támogatom, két kikötéssel: az öröklés **másolás legyen, ne élő hivatkozás**; és több alkategóriánál meg kell mondani, melyik nyer (javaslat: csak a főkategória adhat adó-alapértéket). |
| 6 | **B14.7 — két gép, két üzleti nap offline** | `[ ]` **hézag, döntést igényel** | Ha a szerver halott és két pénztárgép egymástól függetlenül nyit üzleti napot eltérő órával, **kettéhasad a napi zárás és az adatszolgáltatás** — és a bizonylatszámok már ki vannak nyomtatva. Javasolt ellenszer: nyitás előtt kötelezően kérdezze meg a tanúkat. |
| 2 | **B16.4 — beállítás vs. mennyiségi állapot** | `[ ]` **A LEGFONTOSABB MOST ELDÖNTENDŐ** | A felhő lehet autoritatív a **törzsadatra** (ár, láthatóság, receptúra) — de a **készlet futó egyenleg**, aminek nem lehet két gazdája. Javaslat: a felhő küldhet „vegyél fel 20 darabot"-ot, de soha nem „a készlet mostantól 40"-et. Utólag katasztrofális. |
| 3 | **B16.7 — beállítás-paritás őre** | `[ ]` **DÖNTÉST IGÉNYEL** | „A felhőn minden beállítás legyen, ami a POS-on" — két felület, két repó, két nyelv, semmilyen fordító nem köti össze őket. §6 szerint **garantáltan szétcsúszik**, hacsak a beállítások nem EGY sémából épülnek, paritás-őrrel. Élesíti a B8-at. |
| 4 | **B7 + a lánc-szint** | `[ ]` **EGYÜTT döntendő** | A franchise egy ÚJ hierarchia-szintet vezet be a telephely fölé, és a lánc-szintű összesített lekérdezés igénye érdemben szűkíti a multi-tenancy lehetőségeit. |
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
| — | ~~C3/a HELYESBÍTÉS~~ | `[ELDÖNTVE — a felhasználónak volt igaza]` | Az adókulcs-„megegyezik" **MÁSOLAT legyen, ne hivatkozás** — az én jelölő-javaslatom hibás volt. Indok: egy hivatkozás a helyben fogyasztásos kulcs csökkentésekor **az elvitelest is némán lecsökkentené**, ami adóhiány. A két hibairány ára nem egyenlő: túl magas kulcs pénzügyi hátrány, túl alacsony **jogsértés** — a mechanizmus a kisebb kár felé dőljön. |
| — | ~~F4/K1~~ | `[ELFOGADVA]` | A bizonylatszám-számláló kulcsa **(eszköz, dátum)**, nem (eszköz, Munkanap). Egy dátumra nyíló második Munkanap folytatja a számozást; a Munkanap külön mező. **Mellékhaszon: ettől lett az összefésülés mechanikusan megoldható.** |
| — | ~~Fiskális üzemmódok~~ | `[ELDÖNTVE]` | **Három üzemmód:** (1) belső rendszer adóügyi eszköz nélkül, (2) online pénztárgép, (3) e-pénztárgép. Részletek: **`FISKALIS_UZEMMODOK.md`**. Az 1. módban `[!]` a nyomtatott papírt **„NEM ADÓÜGYI BIZONYLAT"** jelöléssel kell ellátni, különben nyugtának néz ki. |
| — | ~~F4~~ | `[ELDÖNTVE]` | **Mind a négy nap-fogalom definiálva.** MUNKANAP = a HELYÉ, max 25 óra (23:30-nál figyelmeztetés, 25 óránál kényszerleállás), nem naptári nap, egy dátumra több is nyitható. MŰSZAK = az ESZKÖZÉ, az adóügyi munkanap. ~~NTAK tárgynap = naptári nap.~~ **[H1 HELYESBÍTÉS: TÉVEDÉS — az NTAK tárgynap a NYITÁS dátumából származik, tehát a MUNKANAP-pal esik egybe.]** **[H2: a 25 órás felső határ ÜTKÖZIK az NTAK 24 órás kemény validációjával — döntést igényel.]** |
| — | ~~C3/a~~ | `[ELDÖNTVE]` | **Termékenként két adókulcs** (helyben / elvitel), megjelölhető az azonosság, és **termék nem hozható létre hiányos adóadattal**. Az adó megadása az ügyfél felelőssége. **Kikötés:** az „azonos" JELÖLŐKÉNT tárolandó, ne másolt értékként, különben a helyben fogyasztásos kulcs átírásakor az elviteles csendben a régin marad. |
| — | ~~C3/b~~ | `[ELDÖNTVE]` | **NTAK-kategória feltételesen kötelező:** nincs NTAK-kulcs → nem kell és nem is figyelmeztetünk; van kulcs → kötelező vagy erős figyelmeztetés. **Kritikus pillanat:** amikor egy hely utólag illeszt be kulcsot, minden meglévő terméke kategória nélkül áll. |
| — | ~~C2/a~~ | `[ELDÖNTVE]` | **A bizonylat az ELADÁSKORI árat, adókulcsot ÉS NEVET tárolja**, nem hivatkozást — különben egy áremelés vagy átnevezés visszamenőleg átírja a régi riportokat. |
| — | ~~C2/b~~ | `[ELDÖNTVE]` | **Három állapot:** aktív / inaktív (szezonális, visszakapcsolható) / **soft delete** (elrontott termék). **Egyik sem rejtheti el a terméket a TÖRTÉNETBŐL** — csak az elérhetőséget szünteti meg. Javaslat: soha nem használt termék legyen ténylegesen törölhető. |
| — | ~~A3~~ | `[ELDÖNTVE]` | **A felhő a jogi archívum** — a 8 éves megőrzést a felhő teljesíti. Következmény: a „tisztán lokális" topológia önmagában nem elegendő, és ezt a kockázatvállalási nyilatkozatban rögzíteni kell. Későbbi tervként felvéve az összetett felhős archiválás. |
| — | ~~B17~~ | `[RÉSZBEN ELDÖNTVE]` | **A felhő is két fizikai szerver**, fő + másodlagos, minden adat mindkettőn, terhelésmegosztás, automatikus átcsatornázás. **Fontos:** a telephelyi „kézi átkapcsolás" indoklása **NEM vihető át** ide — a felhőben mi uraljuk az infrastruktúrát, tehát az automatikus átvétel biztonságosan megépíthető. |
| — | ~~F7/a~~ | `[ELDÖNTVE]` | **Szerkeszthető jogosultsági SZINTEK** — az ügyfél maga hozhat létre szintet (pl. „Pultfőnök"), nem csak egyedi kivételeket. **Frissítési csapda felvéve:** egy új verzió új jogosultságai a meglévő, testreszabott szinteken **alapból TILTOTTAK**, de a felület **feltűnően jelezze**, hogy N új jogosultság érkezett és át kell nézni — különben az új funkció némán nem működik. |
| — | ~~F7/b~~ | `[ELDÖNTVE]` | **A Siduri admin fiók sérthetetlen** (nem módosítható, jogköre nem csökkenthető, jelszava nem írható át az ügyfél által), és **van fix offline belépési lehetőség** — a felhasználó a biztonsági aggály ismeretében tartja fenn. **Javaslat a megvalósításra:** ugyanez a képesség **telephelyenkénti** hitelesítő adattal (egy kiszivárgás egy telephelyet érint, nem mindet), challenge–response elsődleges úttal. Kötelező kísérők: sebességkorlát, **az ügyfél számára is látható, törölhetetlen audit**, látható jelzés a gépen, időkorlát. |
| — | ~~B16.10~~ | `[ELDÖNTVE]` | **Leltár — az egyetlen jogos „felülírás", de mégis MOZGÁSKÉNT.** A megszámolt mennyiség és a rendszer szerinti eltérése **korrekciós mozgásként** könyvelődik, nem néma felülírásként — így az eltérés kimutatható marad, ami a leltár egész értelme. **Időzítési csapda:** az eltérést a **fordulónapi** készlethez kell mérni, nem a rögzítéséhez, különben a közben eladott mennyiséget hiányként könyveli és kitörli az időközbeni eladásokat. |
| — | ~~B16.11~~ | `[ELDÖNTVE]` | **A több telephely nem franchise-funkció, hanem ALAPMODELL** — lehet olyan tulajdonos, akinek 3 különálló üzlete van. Minden kimutatásnak működnie kell egy üzletre, több kiválasztottra, és a teljes csoportra. |
| — | ~~B16.12~~ | `[ELDÖNTVE]` | **A felhő raktár/receptúra = a telephelyi adminfelület**, csak máshol megjelenítve → **EGY webes admin alkalmazás, KÉT helyről kiszolgálva.** Ez a §6 néma szétcsúszást a gyökerénél szünteti meg, és érdemben csökkenti a fázisterv egyik legnagyobb tételét. |
| — | ~~B16.1~~ | `[ELDÖNTVE]` | **A felhő teljes menedzsment-platform**, nem kiegészítő: teljes beállítás-paritás a POS-szal, raktárkezelés, alapanyag-mozgás, receptúrázás, statisztikák; **zárolható beállítások** (kiemelten ár és láthatóság); **üzletlánc/franchise szintű zárolható központi értékek**; visszajelzés a módosítás leérkezéséről; eszköz-láthatóság (mikor kommunikált utoljára, meg van-e nyitva). **Ez a legnagyobb scope-változás az egész munkamenetben, és önálló terméksávot jelent a fázistervben.** |
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
| ~~**C11**~~ | ~~24 órás NTAK adatszolgáltatási limit, 18 órás riasztás~~ | **[H3: IGAZOLVA, HOGY HAMIS.** A rendelésösszesítő **15 percenként** megy (paraméterezhetően), a napi zárás legalább 24 óránként. A 19. pont SLA-figyelmeztetése újraírandó.**]** |
| **C12** | Az e-nyugta iránnyal most nem kell foglalkozni | A bizonylat-modell alakja |

---

## G) A 2026-08-23-i kör — módosítók, menü, DRS, pénz, audit napló, nyomtatás

Ez a kör három bemenetből dolgozott: a feltöltött **gyűjtőkiosztás**, a feltöltött
**gyártói AEE illesztő-protokoll** (lásd G0 — jogi korlát), és a **DRS**
elsődleges forrásokból végzett kutatása.

### `[JOGI KORLÁT — KÖTELEZŐ BETARTANI]` G0 — A gyártói protokolldokumentum nem publikálható

A kapott illesztő-protokoll PDF **kifejezett szerzői jogi nyilatkozatot hordoz**:
a kiadó kizárólagos tulajdona, írásbeli engedély nélkül másolása és terjesztése
tilos. Partneri megállapodás **nincs** — eddig egyetlen, szöveg nélküli e-mailes
válasz érkezett egy integrációs megkeresésre.

**Ebből következő, kötelező szabályok:**

| # | Szabály |
|---|---------|
| G0.1 | A dokumentum tartalma **semmilyen formában nem kerülhet a dokumentációba** — sem idézet, sem parancstáblázat, sem „átfogalmazva, de felismerhetően". |
| G0.2 | A dokumentációban a fiskális illesztés **csak absztrakt szinten** írható le: „a fiskális adapter a gyártó helyi szolgáltatásával kommunikál; a konkrét parancskészletet a gyártó zárt dokumentációja írja le". Portszám, parancsnevek, mezőnevek, hibakódok **nem**. |
| G0.3 | A protokoll részletei **kizárólag a fejlesztéshez** használhatók. |
| G0.4 | A gyártóspecifikus illesztő **elkülönített modulban** éljen, a többi kódtól tisztán elválasztva, hogy bármikor kiemelhető legyen. |
| G0.5 | **NYITOTT KOCKÁZAT:** a megvalósított illesztőkód szükségszerűen tartalmazni fogja a parancsneveket. Ha bármelyik repó valaha publikussá válik, a modult ki kell emelni. **Eldöntendő: a repók privátok maradnak-e.** |

**Járulékos, nem jogi kockázat, amit ki kell mondani:** partneri megállapodás
nélkül olyan termékhez illesztünk, amihez **nincs támogatási szerződésünk, nincs
tesztkészülékünk és nincs értesítésünk a firmware-változásokról**. A fiskális
mérföldkő ezért **fizikai tesztkészülék nélkül nem zárható le** — ez ütemezési
korlát, nem fejlesztési feladat.

### `[ELDÖNTVE]` G1 — A gyűjtőkiosztás 8 fix rekesze kemény korlát

A kapott kiosztás: **Termék 5% / 18% / 27%**, **Szervizdíj 5% / 18% / 27%**,
**TAM**, **AJT** — összesen 8, **egy sem szabad**.

| # | Következmény |
|---|--------------|
| G1.1 | Az áfakulcs-készlet kötött: **5 / 18 / 27 / TAM / AJT**. Más nem küldhető. A validációt a **terméktörzs mentésénél** kell megfogni, nem nyomtatáskor — ott már késő. |
| G1.2 | **A szervizdíjnak saját, áfakulcsonkénti gyűjtői vannak.** A szervizdíjat tehát **nem szabad** a termék tételébe olvasztani, és **áfakulcsonként bontva** kell számolni, nem egyetlen záró összegként. *A korábbi tervben ez rosszul szerepelt — javítandó.* |
| G1.3 | Az **AJT** (adójegyes termék) vendéglátásban gyakorlatilag használatlan → ez az egyetlen esélyes szabad rekesz, ha a gyártó megengedi az újrakiosztást. **Kérdés a gyártó felé.** |
| G1.4 | Bármi új igény (pl. DRS visszaváltási díj, G4) csak meglévő rekesz terhére fér be. |

### `[ELDŐLT — a felhasználó jobb megoldást adott]` G2 — Módosítók

#### G2.1 — FreeLimit (ingyenes választások száma)

Csoportszintű mező: hány elem választható ingyen, mielőtt a többi fizetőssé válik.
Független a `min`/`max`-tól.

**DÖNTÉS:** a `FreeLimit` mellé **külön beállítás, hogy MELYIK elemek ingyenesek**,
három lehetőséggel: **legdrágább / legolcsóbb / legelső**.
**Alapértelmezés: LEGELSŐ** (a választás sorrendje szerint).
Az ügyfél állítja be, akár termékenként.

*Az eredeti javaslat (fix „legdrágább" logika, kapcsolóval) elvetve — a
háromállású, ügyfél által vezérelt változat jobb: nem mi döntjük el helyette,
mi az üzletpolitikája.*

#### G2.2 — A módosító MINDIG eltérés (ez a kör legfontosabb egyszerűsítése)

**DÖNTÉS:** az alapállapot a **receptúra**. A ketchup a hamburger receptjének
része, nem módosító. Aki „ketchup nélkül" opciót akar, **levonó módosítót** csinál rá.

**Miért ez a jó modell:** nem kell minden receptúra-tételt egyesével automatikus
módosítóvá alakítani, és **megszűnik az „alapállapot vs. eltérés" megkülönböztetés
a nyomtatási logikában**.

**Ebből következő, egyszerű szabály:**

> **Ami módosítóként a sorra kerül, az MINDIG eltérés vagy fontos egyedi kérés →
> MINDIG nyomtatjuk és MINDIG megjelenítjük a KDS-en.** Kivétel nincs.

**Járulékos következmények, amiket a modellbe kell tenni:**

| # | Következmény |
|---|--------------|
| G2.2.a | A **levonó módosítónak be kell tudnia nyúlni a szülőtermék receptjébe.** Nem elég, hogy „saját receptje van" — ki kell tudnia venni egy összetevőt a szülő levonásából. |
| G2.2.b | A levonó módosító **ANYAGRA (összetevőre) hivatkozzon, ne konkrét receptsorra.** Így egyetlen „Ketchup nélkül" módosító minden olyan terméken működik, aminek a receptjében ketchup van; ahol nincs, ott nem csinál semmit (beállításkor érdemes figyelmeztetni). |
| G2.2.c | A `default` (előre bejelölt) jelző **megmarad**, de **csak előválasztásra** — a kötelező választású csoportoknál (pl. „milyen köret?") gyorsít. **A nyomtatásra nincs hatása:** ami a soron van, az nyomtatódik. |
| G2.2.d | A levonó módosító **visszaírja a készletet** — ez a lényege. |

#### G2.3 — Ár nélküli módosító = szövegsor, nem tétel

A gyártói protokoll a tételsorhoz **szöveges kiegészítő mezőket** kínál. Az ár
nélküli módosító oda való: megjelenik a termék alatt, de **nem tétel** — nincs ára,
áfája, gyűjtője.

**Szabály:** *ár nélküli módosító = szövegsor; áras módosító = önálló tétel.*
Harmadik eset nincs.

**Ezzel a korábban felmerült „0 Ft-os módosító legyen 1 Ft, és vonjunk le 1 Ft-ot
a termék árából" megoldás ELVETVE**, mert:

- több 0 Ft-os módosítónál halmozódik → a nyugtán nem az étlapi ár szerepel
  (**ártájékoztatási jogsértés**, akkor is, ha a végösszeg stimmel);
- áfakulcsot vált, ha a termék és a módosító más kulcson van;
- mennyiséggel szorzódik;
- a százalékos kedvezmény alapját elrontja.

⚠️ **MÉRENDŐ:** a protokoll szerint a nulla összegű tétel támogatott, de hogy az
adott firmware és a NAV-engedély elfogadja-e, azt **éles készüléken kell
ellenőrizni** → `MERESEK.md`.

#### G2.4 — Levonó módosító: külön fiskális útvonal

A protokollban a **negatív ár nem „mínusz forintos tétel", hanem tételsztornó**.
Egy „sajt nélkül −100 Ft" módosító tehát **nem küldhető negatív árú eladási
sorként**. Két járható út: a kedvezmény-mechanizmuson keresztül, vagy a termék
árába építve.

**Tervezési következmény:** a **levonó és a hozzáadó módosítónak külön útja van a
fiskális rétegben.** Ezt most kell szétválasztani a modellben.

Ugyanitt jó hír: a **negatív mennyiség a protokollban göngyölegvisszavétel** —
a DRS-visszaváltás (G4) natívan támogatott, nem kell kerülőút.

### `[ELDÖNTVE]` G3 — Összetett menü

**Szerkezet:** terméken „ez menü" jelző + **menükomponensek**; komponensenként
`min`/`max` (alapértelmezés pontosan 1) és választható termékek; a rendszer
automatikusan felugrik, amíg minden komponens ki nincs töltve.

| # | Döntés |
|---|--------|
| G3.1 | **Felár a komponens–termék PÁROSÍTÁSON**, nem a komponensen. („ital: üdítő +0, frissen facsart +390") |
| G3.2 | A menükomponens **külön entitás**, nem módosítócsoport — az opciói **termékek**, saját recepttel, készlettel, áfakulccsal, NTAK-kategóriával. |
| G3.3 | **A menü a nyugtán SZÉTROBBAN a komponenseire.** A menü neve fejléc-szövegsor, alatta a komponensek, mindegyik a saját áfakulcsán. |
| G3.4 | Az ár szétosztása **a komponensek egyedi listaárainak arányában**, a kerekítési maradék a legnagyobb komponensre. **Determinisztikus** — két azonos menü mindig ugyanazokat a számokat adja. |

**Miért kötelező a szétrobbantás:** vegyes áfakulcsú menü (5%-os étel + 27%-os
palackos üdítő) egyetlen fiskális sorként **nem küldhető**, mert két gyűjtőre kell
mennie. Ezen felül az NTAK komponensenkénti kategóriát vár, a készlet pedig
komponensenkénti receptet fogyaszt.

⚠️ **ELLENŐRIZENDŐ:** az NTAK-specifikáció ír-e elő külön menükezelést. A nyilvános
NTAK vendéglátás útmutatók ezt nem részletezik egyértelműen — **hivatalosan
megkérdezendő**.

### `[ÚJ TERÜLET — a tervben eddig nem szerepelt]` G4 — DRS (kötelező visszaváltási díj)

Kutatva elsődleges és szakmai forrásokból (NAV adózási kérdés 2023-11;
450/2023. (X. 4.) Korm. rendelet; kamarai és szakmai összefoglalók).

#### G4.1 — Tényállás

| Tétel | Tartalom |
|-------|----------|
| Összeg | **darabonként egységesen 50 Ft**, nem újrahasználható (egyutas) csomagolásra |
| Termékkör | **0,1–3 liter** űrtartalmú, fogyasztásra kész vagy koncentrátum italtermék csomagolása — üveg, fém, műanyag |
| Kivétel | **tej és tejtartalmú italtermék** |
| Áfa | **NEM része az értékesítés adóalapjának** — nem 0%, nem áfamentes, hanem **az áfa hatályán kívüli tétel**. A nyugtán/számlán **a termék árától elkülönítve** kell feltüntetni. |
| Visszaváltáskor | **az adóalap nem csökkenthető** a díjjal |
| Újrahasználható csomagolás | **más szabály**: az áfatörvény általános betétdíj-szabályai, a díj **benne van** az adóalapban |
| Visszaváltóhely | a vendéglátóhelynek **nem kötelező** üzemeltetnie; önkéntes csatlakozás |

#### G4.2 — A minket leginkább érintő szabály

> **Helyben fogyasztásnál, ha a csomagolás a vendéglátóhelyen marad, a
> visszaváltási díjat nem terheljük a vendégre. Elvitelnél, amikor a palack a
> vendéggel távozik, fel kell számítani, külön tételként, az áfa hatályán kívül.**

Vagyis **ugyanaz a termék két különbözőképpen viselkedik ugyanazon a napon,
ugyanazon a gépen** — kizárólag a teljesítési módtól függően.

#### G4.3 — Teendők

| # | Teendő | Címke |
|---|--------|-------|
| G4.a | Terméktörzs: **`DRS-köteles csomagolás`** jelző + **`csomagolástípus`** (egyutas / újrahasználható) — a kettő áfakezelése eltér | MVP |
| G4.b | A díj összege **központi, verziózott paraméter** (most 50 Ft), **nem konstans a kódban**; a régi bizonylatok a régi értéket őrzik | MVP |
| G4.c | A felszámítás **a teljesítési módhoz kötött, nem a termékhez**. Teljesítési mód váltásakor (helyben → elvitel) **utólag hozzáadható/levehető a nyitott rendelésen**, auditnaplózva | MVP |
| G4.d | **Külön nyugtasor a termék alatt, saját gyűjtőn.** ⚠️ A 8 fix rekeszben nincs DRS-hely; a TAM az egyetlen jelölt, **de a TAM „tárgyi adómentes", ami nem azonos az „áfa hatályán kívülivel"** → **kérdés a gyártó / NAV felé** | blokkoló |
| G4.e | **A díj NEM árbevétel** — átfutó tétel. A forgalmi riportokból, a jutalékalapból és a napi zárás forgalmi számából **ki kell venni** | MVP |
| G4.f | Visszavétel (a vendég hozza a palackot, kap 50 Ft-ot): a protokollban natívan támogatott, **de a hely nem kötelezett visszaváltóhely lenni** → **nem MVP**, opcionális funkció | v1/v2 |
| G4.g | **DRS-egyenleg** (beszerzésen kifizetett vs. visszaváltással visszakapott) | v2 |

### `[ELDÖNTVE]` G5 — Pénz, kerekítés, valuta

| # | Döntés |
|---|--------|
| G5.1 | **Bruttó alapú számolás.** Ha az árlistán 1500 van, akkor 1500 az igazság; a nettó és az áfa ebből származik. |
| G5.2 | **A visszaszámolás áfakulcs-csoportonként, bizonylatszinten történik**, nem soronként — mert a pénztárgép is így számol, és a soronkénti kerekítés garantáltan 1–2 Ft eltérést szül a mi összesítőnk és a gép nyugtája között. |
| G5.3 | **Két pénztípus:** *ár/összeg* = **egész forint (int64)**; *egységköltség* (beszerzési egységár, mozgóátlagár, receptösszetevő) = **nagy pontosságú tizedes (6 tizedes)**. Lebegőpontos szám pénz közelében **sehol**. |
| G5.4 | **Kerekítés csak készpénznél, 5 Ft-ra.** Vegyes fizetésnél **a készpénzes részre** vonatkozik, nem a végösszegre. |
| G5.5 | **A kerekítést mi számoljuk, elküldjük, és a gép válaszát összevetjük.** Eltérés esetén a bizonylat **nem záródhat le csendben** — hiba, kezelői beavatkozással. |
| G5.6 | **EUR:** árfolyam napnyitás előtt megadva, felülírásig érvényes. **A pénztárgép saját valutaárfolyam-beállítását is ki kell írni és vissza kell olvasni.** A bizonylat **tárolja a felhasznált árfolyamot**. Ha napnyitáskor nincs árfolyam: **az előzőt viszi tovább feltűnő figyelmeztetéssel, nem blokkol**. **Visszajáró forintban.** Csak készpénzre. |

### `[ELDÖNTVE]` G6 — Nyelvek

Magyar + angol + német **kötelező**; szomszédos nyelvek később.

| # | Döntés |
|---|--------|
| G6.1 | **Két külön feladat:** (1) **szoftverszövegek** — teljes körű, mindhárom nyelven; (2) **tartalom** (terméknév, kategórianév, módosítónév, allergén) — **az ügyfél adata**, mezőnként opcionális, **magyar visszaesési értékkel**. Kényszeríteni tilos, mert akkor nem tölti fel a törzset. |
| G6.2 | **A fiskális nyugta magyar** — jogszabályi kötöttség. A többnyelvűség a nem fiskális példányon, a QR-os vendégoldalon, az e-nyugta megjelenítésén és a kijelzőkön él. |
| G6.3 | **A POS-felületet német szövegekkel kell tesztelni**, nem magyarral: a német átlagosan 25–35%-kal hosszabb, és a J1900-as gépek kis felbontású érintőképernyőjén tördel. **Elfogadási kritérium a UiUX körben.** |

### `[ELDÖNTVE — a felhasználó döntése, kockázatvállalással]` G7 — Ki nyomtat

**A KLIENS nyomtat** (nála van az adóügyi eszköz és a nyomtató). **Kivétel: a
vékonykliens** — helyette a szerver.

**Az „előzetes szándékrögzítés a szerverre" javaslat ELVETVE.** Indoklás
(a felhasználóé, elfogadva): ha a gép meghal, úgyis támogatás kell; ha
feléleszthető, magától szinkronizál; ha nem, munkatárs jelzi és pótoljuk.
Cserébe **a szerver nem kerül minden nyomtatás kritikus útjába** — ez a döntő
érv, mert (a) akadozó szervernél minden nyugta várna, és (b) **szerver nélkül a
vészhelyzeti mód sem működne**.

*Pontosítás a rend kedvéért: az eredeti javaslat nem folyamatos kliens-szerver
csevegést jelentett, hanem bizonylatonként egy írást — a hálózati terhelés érve
tehát nem áll. A **késleltetés** és a **vészhelyzeti mód** érve viszont áll, és
önmagában elég.*

| # | Döntés / teendő |
|---|-----------------|
| G7.1 | **Elfogadott kockázat:** ha a kliens kinyomtat, majd meghal a jelzés előtt, a pénztárgépben van egy lezárt adóügyi bizonylat, amiről a rendszer nem tud. Feloldás: **támogatói úton, az adóügyi eszköz saját naplójából.** |
| G7.2 | **Enyhítés, ami nem sérti a döntést:** a kliens a nyomtatási szándékot **HELYBEN** rögzítse (ugyanabba a helyi outboxba, ami degradált módban amúgy is működik) a gép hívása előtt. Költsége: **egy helyi lemezírás, nulla hálózat, nulla szerverfüggés.** Áramszünet/összeomlás után (a tipikus eset) a bizonyíték megvan; fizikailag megsemmisült gépnél úgyis támogatás kell. |
| G7.3 | **Nyitott, külön kérdés:** az adóügyi eszköz **egyetlen géphez** van kötve. Ha az a gép meghal, a nyitott asztalokat sehol nem lehet lezárni — **a szerver-HA ezen nem segít.** Teendő: (a) 4+ gépes helyre **legalább 2 adóügyi eszköz** ajánlása, (b) **a nyomtatási feladat átirányítása másik gép eszközére**. |
| G7.4 | **A vékonykliens nem vehet fel fizetést**: a képesség megépül, de kikapcsolva. **Ne fordítási kapcsoló legyen**, hanem **szerveroldali, az admin felületen meg nem jelenő jogosultság**, amit a kliens minden fizetési kísérletnél megkérdez — így helyi fájl átírásával nem oldható fel, és a bekapcsolás **auditnaplózható**. |

### `[ELDÖNTVE]` G8 — Óraszinkron

| # | Döntés |
|---|--------|
| G8.1 | **A telephelyen a szerver az óra.** A kliensek hozzá szinkronizálnak, **nem az internethez** → a telephely offline is önmagával konzisztens. A szerver, ha van net, NTP-hez igazodik és **rögzíti az elcsúszást**. |
| G8.2 | **Az adóügyi eszköz órája külön** — napnyitáskor összehasonlítandó. Javaslat: **30 mp felett figyelmeztetés, 5 perc felett a napnyitás blokkolva.** *(Jóváhagyásra vár.)* |
| G8.3 | **Minden óraállítás auditnaplózott**, régi és új értékkel. |
| G8.4 | **A sorrendezés soha nem a faliórán múlik** — monoton növekvő számláló adja; a faliórát csak megjelenítésre és jogi időbélyegre használjuk. |

### `[ELDÖNTVE]` G9 — Audit napló

#### G9.1 — Alapelvek

- **Csak hozzáfűzhető** — nincs `UPDATE`, nincs `DELETE`, adatbázisszinten kikényszerítve.
- **Hash-lánc** a biztonsági/számviteli ágon: minden rekord tartalmazza az előző hash-ét → utólagos átírás vagy kivágás matematikailag kimutatható.
- **Felhős horgonyzás:** a lánc aktuális hash-e időnként felmegy a felhőbe. Enélkül a lánc nem véd az ellen, ha valaki az **egész adatbázist** korábbi állapotra állítja vissza.
- **A Siduri admin sem törölheti.** Purge csak kor alapján, felhős archívumba.
- Rekordtartalom: **ki** (felhasználó + eszköz + **az akkori** szerepe), **mikor** (eszközóra + szerveróra + monoton sorszám), **mi**, **hol**, **mi volt előtte / utána**, és ahol kötelező: **miért** (indokkód + szabad szöveg).

#### G9.2 — KÉT KÜLÖN ÁRAM (a tárhely-aggály nyomán)

A felhasználó jogosan kérdőjelezte meg, megéri-e mindent naplózni. A válasz:
**nem egy napló van, hanem kettő, eltérő garanciával és költséggel.**

| | **(A) Biztonsági / számviteli audit** | **(B) Működési eseménynapló** |
|---|---|---|
| Mi kerül bele | sztornó, kedvezmény, árfelülírás, jogosultság, beállítás, napnyitás/-zárás, átállás, leltári felülírás, óraállítás, fiókynyitás eladás nélkül | tételfelvitel, asztalmozgás, rendelésállapot — az **asztaltörténet / felhasználó-történet** nézetek forrása |
| Hash-lánc | **igen** | nem (felesleges és lassít) |
| Megőrzés | **8 év** (felhőben) | **1 év** (felhőben) |
| Helyi megőrzés | **30 nap** | **30 nap** |
| Nagyságrend / telephely / nap | ~150–300 rekord | ~3000–5000 rekord |
| Éves méret / telephely | néhány tíz MB | ~0,5 GB |

**A hangsúlyos lelet:** a tárhelyet **nem a biztonsági események viszik el, hanem
az asztaltörténet-nézet** — de az az ügyfélnek adott érték, tehát megéri.
A hash-lánc viszont csak az (A) ágon indokolt: napi 5000 soron pazarlás és lassít,
napi 200-on ingyen van.
**Valós mérés:** `MERESEK.md`.

#### G9.3 — Hozzáférés

| # | Döntés |
|---|--------|
| G9.3.a | **A nyers auditot CSAK MI látjuk.** Az ügyfél nem kap nyers adatbázissor-nézetet. Kért adatokat kiküldünk. |
| G9.3.b | Az ügyfél **kurált, vizuális nézeteket** kap, célzottan elhelyezve: **asztaltörténet** (egy asztalra kattintva, az adott munkanapra), **felhasználó-történet** („bejelentkezett, felütött a 3-as asztalra 1 gyrost, kilépett"). Szép, könnyen érthető megjelenítés, nem száraz lista. |
| G9.3.c | **Technikai következmény:** a napló legyen **entitásonként (asztal, felhasználó, rendelés) hatékonyan lekérdezhető** → indexelési követelmény. Kell **esemény → emberi mondat** sablonkészlet, **többnyelvűen**. |
| G9.3.d | **Az olvasás NEM naplózódik.** Helyette a **jogosultsági beállítások** szabják meg, ki mit láthat. Következmény: a **jogosultságváltozás naplózása felértékelődik**. |

#### G9.4 — Munkajogi figyelmeztetés

**DÖNTÉS: csak figyelmeztetünk, sablont NEM adunk.** Indok (a felhasználóé,
elfogadva): ez a munkáltató kötelezettsége, és egy elavuló sablonért minket
hibáztatnának.

**Kiegészítés:** a figyelmeztetés **ott jelenjen meg, ahol a funkciót használják**
(a felhasználó-történet megnyitásakor), **ne csak egyszer a telepítéskor** — mert
a felhasználó-történet nézet **munkavállalói megfigyelés**, függetlenül attól,
milyen szépen néz ki.

#### G9.5 — Ha nem lehet kiírni

**Enyhe változat:** előre lefoglalt helyi vésztartalék-pufferbe ír, feltűnő
riasztás, és amint lehet, összefésül. Ha a vésztartalék is betelik, **akkor** áll meg.

*Megjegyzés a listáról: a felhasználó fenntartja, hogy a naplózandó események
listája szűkíthető lehet. **Később átnézzük** — kivenni megírt naplózási tételt
könnyebb, mint utólag újat írni.*

### `[ELDÖNTVE]` G10 — Árazás

| # | Döntés |
|---|--------|
| G10.1 | **Áfakulcs-változáskor a BRUTTÓ marad** (1500 marad 1500). A nettó árbevétel változik, az árlista nem. **Következmény, amit ki kell írni a felületen:** egy áfakulcs-változás **azonnal átírja a haszonkulcsot**. |
| G10.2 | **NINCS külön elviteli bruttó ár.** Ha a hamburger 1500 és elvitelre kérik, az ügyfél elesik ~21%-nyi haszontól — **ez így működik Magyarországon, és bele van kalkulálva**. Csak a **két áfakulcs** van külön, a **bruttó ár egy**. |
| G10.3 | **Következmény G10.2-ből:** mivel a bruttó azonos, de az áfa eltér, **a nettó árbevétel teljesítési módonként más** → minden **árrés- és food cost-riportot teljesítési módonként bontva** kell számolni, sosem vegyített bruttón. Kell egy riport, ami megmutatja, **mennyibe kerül az elviteles arány** a tulajdonosnak. |
| G10.4 | **Kiszerelések: az ügyfél ad árat, a rendszer NEM számol.** A 0,5 l csapolt sör 1000 Ft, a 0,3 l **nem 600, hanem amennyit az ügyfél mond** (pl. 750). Súly/térfogat szerinti árazás **is** legyen, de csak ahol kérik. |
| G10.5 | **A kiszerelés a termék gyermeke**, nem külön termék: közös név, kategória, áfakulcs, NTAK-kategória; **saját bruttó ár és saját receptmennyiség**. Riportban együtt is, külön is látszik. |
| G10.6 | **Ártörténet a terméktörzsben is** (mikortól meddig mennyi volt) — a bizonylat eladáskori árán felül. Enélkül a „miért esett a márciusi árrés" kérdésre nincs válasz. |

### `[ÁLTALÁNOS TERVEZÉSI ELV — a felhasználó fogalmazta meg]` G11

> **„Ne próbáljuk megmondani, hogy mit szeretne az ügyfél. Hagyjuk, hogy olyan
> szabadon és pontosan állíthassa be a termékeit és a kiszereléseit, ahogy szeretné."**

Ez ugyanaz az elv, mint az áfa **másolás-nem-hivatkozás** döntésénél (C3/a) és a
`FreeLimit` háromállású beállításánál (G2.1). Általánosítva:

**Ahol az ügyfélnek valós üzleti oka lehet eltérni a számított értéktől, ott a
számított érték legyen EGYSZERI KITÖLTŐ SEGÉDLET, soha ne élő hivatkozás.**

---

## H) NTAK RMS interfész — elsődleges forrásból igazolva (2026-08-23)

Forrás: **NTAK Vendéglátás szakrendszer, RMS Interfész leírás v1.06 (MTÜ, 2024.06.10)**,
`https://info.ntak.hu/media/uploads/docs/RMS_Interfesz_leiras_v106.pdf`.
Ez a hivatalos műszaki specifikáció, nem másodlagos összefoglaló.

### `[HELYESBÍTÉS — a korábbi F4 döntésünk HIBÁS volt]` H1 — Az NTAK tárgynap NEM naptári nap

Az F4-ben azt rögzítettük, hogy **„NTAK tárgynap = naptári nap"**. **Ez tévedés.**
A specifikáció szó szerint:

> „A tárgynap az aktuálisan nyitott nap nyitásának dátumával megegyező dátum érték."
> „Naptári napon átnyúló tárgynap esetén **a nyitás időpontjából származtatott nap**."

**Vagyis az NTAK tárgynap a MI MUNKANAP-fogalmunkkal esik egybe, nem a naptári nappal.**
Egy hétfő 06:00 → kedd 03:00 üzleti nap **egyetlen tárgynap: hétfő.**

**Ez jó hír** — nem kell két fogalmat egymásra képezni —, **de két korábbi
következtetést érvénytelenít**:
- az F4 „NTAK tárgynap = naptári nap" sora **törlendő**;
- a 2. ellenőrző körben tett „a munkanap-összevonás az NTAK tartalmát nem érinti,
  csak a küldés kiváltóját" megállapítás **újraértékelendő** — a tartalmat is érinti,
  mert a tárgynap maga az üzleti naptól függ.

### `[ÜTKÖZÉS — DÖNTÉST IGÉNYEL]` H2 — A 25 órás MUNKANAP-ot az NTAK ELUTASÍTJA

A napi zárás üzenet validációja szó szerint:

> `zarasIdopontja – nyitasIdopontja <= 24 óra` — **Szinkron**, hibakulcs: **Conflict**

Ez **szinkron validáció**, tehát az üzenet **azonnal visszautasításra kerül**, nem
utólag jelződik. A szöveges indoklás: „legalább 24 óránként szükséges a napi zárás
elvégzése […] ezáltal az adott tárgynap nyitvatartására vonatkozó nyitás és zárás
időpontok között nem telhet el több, mint 24 óra."

**A mi MUNKANAP-unk felső határa 25 óra** (23:30-nál figyelmeztetés, 25 óránál
kényszerleállás). **Egy 24 óránál hosszabb munkanap NTAK-adatszolgáltatása
elutasításra kerülne.**

**Két megoldási irány, mindkettőnek ára van:**

| Opció | Mit jelent | Ár |
|-------|-----------|-----|
| **(a) A MUNKANAP felső határa 24 óra alá** — javaslat: **figyelmeztetés 22 órakor, kényszerleállás 23 óra 30 percnél** | A két fogalom pontosan egybeesik, nincs külön logika | 1,5 óra „tartalék" elveszik — de a gyakorlatban egyetlen hely sem tart nyitva 23 órát egyhuzamban |
| **(b) 25 óra marad, de 24 óránál közbenső NTAK-zárást küldünk** | A spec engedi: „Lehetséges egy tárgynapra több normál […] napizárás üzenet beküldése, így kezelhető a napközi zárás funkciója is" (az időszakok nem lehetnek átfedők) | Külön, ritkán futó kódág — pont az a fajta, ami élesben először hibázik |

**Javaslatom: (a).** Egyszerűbb, nincs ritkán futó ág, és a tartalék nem hiányzik.

⚠️ **A nyári időszámítás miatt az időtartamot ABSZOLÚT (UTC) alapon kell számolni,
soha nem faliórán.** Az őszi óraátállítás éjszakáján egy 06:00 → 06:00 „napnak"
faliórán 24 óra, valójában **25**. A specifikáció RFC 3339 időbélyeggel dolgozik
(eltolással), tehát abszolút pillanatokat hasonlít. **Ez a leggyakoribb módja
annak, hogy évente egyszer elutasítást kapjunk.**

### `[HELYESBÍTÉS — a C11 premissza HAMIS]` H3 — Az adatküldés 15 PERCES, nem napi

A §13.5 igazolatlan premisszái között szerepelt: *„24 órás NTAK adatszolgáltatási
limit, 18 órás riasztás"*. **A specifikáció ezt cáfolja:**

> „A gyártóknak fel kell készíteniük a szoftvereiket arra, hogy az adatküldési
> gyakoriság **paraméterezhető** legyen. Az aktuálisan meghatározott adatküldési
> gyakoriság: **15 perc**."

**Két külön üzenettípus, két külön ütem:**

| Üzenet | Mikor |
|--------|-------|
| **Rendelésösszesítő** (forgalmi adat) | **15 percenként**, az előző küldés óta rögzített rendelések. **Az érték paraméterezhető kell legyen** — nem éghet a kódba. |
| **Napi zárás** | az üzleti nap zárásakor, **de legalább 24 óránként** |

**Ez érdemben megváltoztatja az offline/degradált tervet.** Eddig úgy számoltunk,
hogy van egy napunk a beküldésre. Valójában **egy hosszabb internetkimaradás alatt
15 percenként keletkezik egy elmaradt küldés**, amit sorba kell állítani és a
visszatéréskor **sorrendben, átfedés nélkül** pótolni. A kimenő NTAK-sor tehát
ugyanolyan elsőrangú, tartós, felügyelt sor kell legyen, mint a bizonylat-outbox.

**Járulékos kötelezettség:** minden beküldésre szinkron válaszban érkezik egy
feldolgozási azonosító, és **a feldolgozás eredményét le KELL kérdezni** —
a specifikáció szerint a beküldéstől számított **24 órán belül**, legkésőbb
**1 hónapon belül**, mert utána már nem elérhető. Ez egy **második, visszamenőleges
folyamat**, ami eddig a tervben egyáltalán nem szerepelt: a beküldés nem elég,
a nyugtázást is be kell gyűjteni és eltárolni.

### `[MEGERŐSÍTVE — a G3 döntés helyes, most már forrással]` H4 — Menükezelés az NTAK-ban

**Van** csomag-kategória, de **csak főkategórián belül**:

| Főkategória | Csomag-alkategória |
|---|---|
| Étel | `ETELCSOMAG` — ételcsomag |
| Étel | `FOETEL_KORETTEL` — főétel körettel |
| Helyben készített alkoholmentes ital | `ITALCSOMAG` |
| Nem helyben készített alkoholmentes ital | `ITALCSOMAG` |
| Alkoholos ital | `ITALCSOMAG` |

**Nincs vegyes (étel + ital) csomagkategória.** Egy klasszikus menü
(hamburger + krumpli + kóla) tehát **nem sorolható be egyetlen kategóriába** →
**kötelezően szét kell bontani a komponenseire.**

**A G3 döntés (a menü a nyugtán szétrobban) így két, egymástól független okból is
kényszer:** a fiskális gyűjtő-korlát miatt (vegyes áfakulcs), és az NTAK
kategóriakészlete miatt.

**Amit ez hozzátesz:** *tisztán ételből álló* menü **elvileg** mehetne egyetlen
`ETELCSOMAG` tételként. **Nem élünk vele** — egységesen bontunk, mert (1) a
készletlevonás komponensenkénti receptet igényel, (2) a riportokban látni akarjuk
mi fogy, (3) egyetlen kódág jobb, mint kettő.

### `[MEGERŐSÍTVE]` H5 — Az NTAK ÁFA-értékkészlete pontosan egyezik a gyűjtő-betűkkel

`afaKategoria` értékkészlet: **`A_5`, `B_18`, `C_27`, `D_AJT`, `E_0`**.

Ez **betűről betűre** ugyanaz, mint a pénztárgép gyűjtőkiosztásának adójelei
(A00 / B00 / C00 / D00 / E00). **Két, egymástól független forrás igazolja a
G1.1 döntést:** a rendszer adókulcs-készlete kötött, öt érték, semmi más.

*Egy különbség a szóhasználatban:* a gyűjtőnél az „E" **TAM**, az NTAK-nál
**`E_0`**. Ugyanaz a rekesz, más elnevezés — a DRS visszaváltási díj (G4)
NTAK-oldalon ide, `E_0`-ra kerülne.

### `[ÚJ KÖVETELMÉNYEK]` H6 — Amit a specifikáció még előír, és a tervben nem szerepelt

| # | Követelmény | Következmény |
|---|-------------|--------------|
| H6.1 | **Mennyiségi egység** értékkészlet: `DARAB`, `LITER`, `KILOGRAMM`, `EGYSEG`, `ADAG`. Szó szerint: *„egy 0,33 literes dobozos üdítő esetén a LITER használandó, nem a DARAB"* | **Minden terméknek kell NTAK mennyiségi egysége**, és palackos/dobozos italnál ez **térfogat**. Ez közvetlenül a kiszerelés-modellhez (G10.5) kapcsolódik: **a kiszerelésnek ismernie kell a térfogatát**, nem elég a neve. |
| H6.2 | `tetelOsszesito` **egész szám**, = tételszám × bruttó egységár, **kereskedői kerekítéssel**, és **a tételösszesítők összegének ki kell adnia a rendelés végösszegét** | **Kemény korlát a menü-szétosztásra (G3.4):** a kerekített komponens-összegeknek **pontosan** ki kell adniuk a menü árát. A „maradék a legnagyobb komponensre" szabály ezt teljesíti — de mostantól nem elegánsság, hanem **előírás**. |
| H6.3 | `bruttoEgysegar` **double** (tört is lehet), `tetelOsszesito` **int** | **A menü-szétosztás így tisztán megoldható:** tört egységár + egész sorösszeg. Nem kell trükközni. |
| H6.4 | `megnevezes` **max 255 karakter**, kötelező, nem üres | Terméknév-hossz validáció a törzsben. |
| H6.5 | **`rendelesVege – rendelesKezdete <= 24 óra`**, szinkron, Conflict | **Egy rendelés (asztal) nem lehet 24 óránál tovább nyitva.** A tervben eddig nem volt felső korlát a nyitott asztalra. Kell figyelmeztetés és kezelés. |
| H6.6 | A `tetelszam`, `tetelOsszesito` és `rendelesVegosszege` **v1.05 óta lehet negatív** | A sztornó és a göngyölegvisszavétel NTAK-oldalon kezelhető. |
| H6.7 | **Az ENUM-értékkészletek a jövőben változhatnak**, a szoftvert fel kell készíteni rá | **Az NTAK kategóriák, mennyiségi egységek és áfakulcsok NEM éghetnek a kódba** — konfigurációból, frissíthetően kell jönniük, és a frissítés nem járhat kliens-újratelepítéssel. |
| H6.8 | Önálló NTAK tételkategóriák: `EGYEB/SZERVIZDIJ`, `EGYEB/BORRAVALO`, `EGYEB/KISZALLITASI_DIJ`, `EGYEB/KEDVEZMENY`, `EGYEB/KORNYEZETBARAT_CSOMAGOLAS`, `EGYEB/MUANYAG_CSOMAGOLAS`, `EGYEB/NEM_VENDEGLATAS` | **A kedvezmény, a borravaló és a szervizdíj az NTAK-ban ÖNÁLLÓ TÉTEL, nem a végösszeg módosítója.** Ez egybevág a gyűjtő-lelettel (G1.2), ahol a szervizdíjnak saját gyűjtői vannak. **A csomagolási kategóriák a DRS/csomagolási díjak valószínű helye.** |
| H6.9 | A napi zárás tartalmaz **`osszesBorravalo`** mezőt | A borravalót nap szinten is összesítenünk kell. |
| H6.10 | Zárva tartott napra **is kell** napi zárást küldeni (`ADOTT_NAPON_ZARVA`), és forgalom nélküli napra is (`FORGALOM_NELKULI_NAP`) | **A rendszernek tudnia kell, mikor van zárva a hely** → nyitvatartási naptár kell, és **a zárva töltött napokról is megy üzenet**. Ez eddig nem szerepelt a tervben. |

---

## I) A 2026-08-23-i kör második fele — válaszok és egy önhelyesbítés

### `[ELDÖNTVE]` I1 — Prior Cash: haladunk, de a véglegesítés a kapcsolatra vár

| # | Döntés |
|---|--------|
| I1.1 | **A repók MINDIG privátok maradnak.** Ezzel a G0.5 nyitott kockázat lezárva: a gyártóspecifikus illesztő maradhat a fő repóban, elkülönített modulban. |
| I1.2 | A kapott dokumentum **fejlesztési irányként** használható, hogy a munka ne álljon. **A dokumentációba továbbra sem kerülhet pontos vagy felismerhető leirat belőle** (G0.1–G0.3 változatlanul él). |
| I1.3 | **A partneri kapcsolatfelvétel, egyeztetés és megállapodás tervben van.** Kapuszabály: **a fiskális réteg VÉGLEGESÍTÉSE előtt be kell várni a kapcsolatot** — addig haladunk, de nem zárjuk le. |
| I1.4 | *Az ügyfél jelzése szerint a kapott dokumentum régi lehet* → a jelenlegi leletek (nulla összegű tétel, DRS-gyűjtő) **egy elavult verzióra épülhetnek**, és az egyeztetésen újra kell kérdezni őket. |

### `[ELDÖNTVE]` I2 — Adóügyi eszköz: gépenként, 4 géptől legalább kettő

| # | Döntés |
|---|--------|
| I2.1 | **Értékesítési ajánlás: gépenként adóügyi eszköz / pénztárgép.** Üzletileg is ez az irány. |
| I2.2 | **4 géptől kezdve KIEMELTEN, erősen ajánlunk legalább kettőt.** |
| I2.3 | Ez ugyanaz a logika, mint a tartalék szervernél (B9): **ajánlás, nem kikényszerítés**; ha az ügyfél a kockázat ismeretében elutasítja, elfogadjuk, és a kockázatvállalási nyilatkozat (B12) rögzíti. |
| I2.4 | *Nyitva maradt:* megépítjük-e a **nyomtatás átirányítását másik gép eszközére** (G7.3). Ha gépenként van eszköz, ez ritkább eset — de a „4 gép / 2 eszköz" felállásban pont ez a kérdés. |

### `[ELDÖNTVE]` I3 — Beszerzési ár

**Bruttó felvitel + KÖTELEZŐ beszerzési áfakulcs; az árrés és a food cost NETTÓ
alapon számol.** Mindkét érték tárolva, a felületen mindkettő látszik.

Indok: a beszerzés áfája levonható, tehát nem költség. Bruttó alapú árrés
**21–27%-kal hamis** számot adna — és az a rendszer legfontosabb üzleti riportja.

### `[ELDÖNTVE — módosítva]` I4 — DRS: alapban terhelve, kikapcsolható

**A G4.c döntés MÓDOSUL.** Az eredeti terv a jogszabályi lehetőséget tette
alapértelmezéssé (helyben fogyasztásnál nem terheljük). **A gyakorlat mást mutat:**

> Van olyan eset — és **ez a gyakoribb** —, hogy helyben fogyasztásnál is kiadják
> az üveget, de **nem veszik vissza**, vagy egyáltalán nem kezelik a visszaváltást.

| # | Döntés |
|---|--------|
| I4.1 | **Alapértelmezés: a visszaváltási díj TERHELVE van**, teljesítési módtól függetlenül. |
| I4.2 | **Beállítási opció (üzletenként):** „helyben fogyasztásnál ne terhelődjön a vendégre". Kikapcsolva alapból. |
| I4.3 | A jogi háttér (G4.1–G4.2) változatlan: a mentesség **lehetőség**, nem kötelezettség — akkor él, ha a csomagolás a vendéglátóhelyen marad. Aki nem veszi vissza, annak terhelnie kell. |
| I4.4 | **A beállítás állapotát a bizonylat mellett rögzíteni kell** — utólag tudni kell, milyen szabály szerint készült. |
| I4.5 | **Ez megint a G11 elv esete:** nem mi döntjük el, mi az üzletmenete — a biztonságosabb (terhelt) irány az alapértelmezés, és aki tudatosan másképp működik, átállítja. |

### `[ÖNHELYESBÍTÉS — a javaslatom rossz ALAKÚ volt, nem csak szigorú]` I5 — Óraszinkron küszöbök

Az eredeti javaslat (**30 mp figyelmeztetés / 5 perc a napnyitás blokkolása**)
jogos kifogást kapott. Átgondolva **nem a küszöb volt a hiba, hanem a szerkezet**:
a blokkolást tettem elsődleges eszközzé, holott **a drift helyes válasza a
JAVÍTÁS, nem a leállítás.**

#### I5.1 — Miért számít egyáltalán az óra

| Ok | Mekkora eltérésnél fáj |
|----|------------------------|
| **NTAK szinkron validáció:** `nyitasIdopontja <= sysDate`, `zarasIdopontja <= sysDate`, hibakulcs **Future** → **ha a mi óránk ELŐRE jár az NTAK szerveréhez képest, az üzenet elutasításra kerül** | ismeretlen tűrés; előre járó óránál akár percek |
| **A bizonylat időbélyege jogi elem** — ellenőrzésnél láthatóan rossz idő probléma | perc szinten kozmetikai, óra szinten valós |
| **Üzleti nap besorolása** — rossz napra kerül a tranzakció | órák |
| **Sorrendezés** | **soha** — azt monoton számláló adja (G8.4), nem a falióra |

#### I5.2 — A valódi veszély ezen a hardveren, amit az eredeti javaslat NEM kezelt

**A J1900-as gépek 10+ évesek. A CMOS-elemük halott vagy haldoklik.**
Ez nem „30 másodperc elcsúszás" — ez **„a gép szerint 2014 van"**, minden
áramszünet után. Ez a bázison **be fog következni**, nem hipotézis.

A rendszernek ezt kell túlélnie, nem a másodperces driftet. **Ez fontosabb, mint
az egész küszöbkérdés**, és az eredeti javaslatból hiányzott.

#### I5.3 — Az átdolgozott terv

**Először javítunk, csak utána panaszkodunk, és blokkolni szinte soha nem kell.**

**Időforrás-sorrend a telephelyen:**
1. **NTP**, ha van internet
2. **az adóügyi eszköz órája** — az AEE a saját mobilhálózatán szinkronizál, tehát
   **internet nélkül is ez a legmegbízhatóbb óra a helyszínen**
3. a telephelyi szerver, a kliensek felé (G8.1 változatlan)

| Eltérés | Válasz |
|---------|--------|
| **< 2 perc** | **Csendben javítjuk.** Nincs üzenet. |
| **2–15 perc** | Javítjuk, ha van forrás. Ha nincs: **nem blokkoló** figyelmeztetés a napnyitó képernyőn + auditbejegyzés. |
| **> 15 perc** | **Feltűnő, nyugtázandó** figyelmeztetés — de **továbbra sem blokkol**. |
| **> 2 óra, vagy eltérő DÁTUM** | **Az EGYETLEN blokkoló eset** — itt már az üzleti nap besorolása és a bizonylat dátuma is hibás lenne, ami valós jogi hiba. **És itt is kell egy egygombos kiút: „óra beállítása az adóügyi eszközről".** |

**Amit ezzel megnyerünk:** reggel 6-kor senki nem áll meg egy 5 perces eltérés
miatt, viszont a „2014 van" eset — ami tényleg megtörténik — nem megy át csendben.

*(A G8.2 sora ezzel felülírva.)*

### `[TISZTÁZVA — nem a mi feladatunk MOST]` I6 — A DRS gyűjtője és a nulla összegű tétel

| # | Állapot |
|---|---------|
| I6.1 | **A DRS gyűjtőjének kiválasztása KÉSŐBBI kérdés** — a tényleges beüzemelés része (a DRS-termék felvitele és az áfájának kiválasztása). Előtte a gyártóval egyeztetni kell: **elképzelhető, hogy náluk ez már megoldott**, és a kapott dokumentum régi. |
| I6.2 | **A nulla összegű tétel: a gyártóra vár.** Az ügyfél tudomása szerint **hiába szerepel a protokollban, a készülék nem fogadja el.** → Az M15 mérés marad, de a **munkafeltevés mostantól: NEM fogadja el.** A G2.3 („ár nélküli módosító = szövegsor") **így is helyes marad**, sőt megerősítést nyer: a szövegsoros út **nem is küld tételt**, tehát a nulla összeg kérdése fel sem merül. |

---

## J) NTAK — második olvasat és a 2026-08-23-i kör harmadik fele

### `[NAGY LELET]` J1 — Az NTAK-nak VAN hivatalos degradált-mód útvonala

`rendelesOsszesitok.osszesitett` (bool) + `osszesitettIndoklasa`. A specifikáció
megjegyzése szó szerint:

> „Annak jelölésére szolgál, ha adott rendelésösszesítő egy hosszabb időszak
> (**max 1 üzleti nap**) értékesítéseit összevontan tartalmazza.
> **Csak szolgáltatáskiesés esetén használható, pl áramszünet, vagy rendszerkiesés.**
> Normál adatszolgáltatás esetén hamis értékkel kell küldeni."

**Ez pontosan a mi degradált / gyorseladás módunk esete (A2).** Az NTAK tehát
nem hogy engedi, hanem **nevesített mezőt ad rá**. Következmények:

| # | Következmény |
|---|--------------|
| J1.1 | **Nem kell saját megoldást kitalálni** a kiesés alatti forgalom pótlására — az összevont beküldés a hivatalos út. |
| J1.2 | **Az összevonás felső határa 1 üzleti nap** → egy 1 napnál hosszabb kiesés nem oldható meg egyetlen összevont üzenettel; napokra kell bontani. |
| J1.3 | **Kell indoklás szöveg** (`osszesitettIndoklasa`) → a degradált módnak **okkódot kell rögzítenie** (áramszünet / szerverkiesés / hálózatkiesés), hogy ez automatikusan kitölthető legyen. Ez új követelmény a degradált mód felé. |
| J1.4 | Normál üzemben a mező kötelezően **hamis** — nem lehet „biztos ami biztos" alapon mindig igazra állítani. |

### `[ELTÉRÉS A MODELLÜNKTŐL]` J2 — A „helyben fogyasztott" NTAK-ban RENDELÉS-szintű

`helybenFogyasztott` **bool, a rendelésösszesítőn**, nem tételenként.
Megjegyzés: **„Vegyes esetben helyben fogyasztást kell jelölni."**

A mi modellünk **finomabb**: a teljesítési mód tételenként értelmezett (ettől függ
az áfakulcs és a DRS terhelése). Ez nem ütközés, csak leképezés:

> **Szabály:** a rendelés `helybenFogyasztott` értéke **igaz**, ha a rendelésben
> **legalább egy** helyben fogyasztott tétel van. Csak a teljesen elviteles
> rendelés kap hamisat.

Az áfakulcs tételenként megy (`afaKategoria` tételszintű mező), tehát a vegyes
rendelés áfája helyesen jelenik meg attól, hogy a jelölő rendelésszintű.

### `[HELYESBÍTÉS — a felhasználónak igaza van]` J3 — A mennyiségi egység NEM validált

A `mennyisegiEgyseg` mezőnél a „0,33 literes dobozos üdítőnél LITER használandó,
nem DARAB" **Megjegyzés (útmutatás), nem validáció.** A mező validációi kizárólag:
`NotNull` és `Enum`. **A `DARAB` tehát átmegy** — az interfész nem utasítja el.

Vagyis: **technikailag elfogadott, de a specifikáció útmutatásával ellentétes.**
A felhasználó emléke („elfogadták a darabot is") **helyes**.

**Amit ez tervezésileg jelent — és ez a lényegesebb rész:** két külön mező van,
amit eddig egynek kezeltünk:

| Mező | Jelentés | Példa: 2 db 0,33 l-es dobozos üdítő |
|------|----------|--------------------------------------|
| `mennyisegiEgyseg` | a termék mértékegysége | `LITER` |
| `mennyiseg` | **a termék saját kiszerelése** (>0, <>0) | `0.33` |
| `tetelszam` | **hány darabot rendeltek** | `2` |

**A terméktörzsben tehát KÉT új NTAK-mező kell:** mennyiségi egység **és**
kiszerelési mennyiség. Ez pontosan illeszkedik a G10.5 kiszerelés-modellhez —
a kiszerelés hordozza a térfogatot.

**Döntés:** a rendszer **támogatja mindkettőt**, az ajánlott (specifikáció szerinti)
értéket **felkínálja**, de **az ügyfél dönt** — G11 elv.

### `[ELDÖNTVE]` J4 — Az NTAK-kategorizálás az ÜGYFÉL feladata

**A termékek és menütételek NTAK fő-/alkategóriájának pontos beállítása az ügyfélé.**
Mi a környezetet és a lehetőséget teremtjük meg hozzá.

**Két kikötés, ami ettől függetlenül a MI felelősségünk:**

| # | Kikötés |
|---|---------|
| J4.1 | **Kemény kapu marad** (C3/b): NTAK-kategória nélkül a termék nem menthető, ha a hely NTAK-köteles. Nem azért, mert mi akarjuk megmondani a kategóriát, hanem mert **a hiányzó kategóriával a beküldés elutasításra kerül**, és az üzemeltetésileg a MI problémánk lesz. |
| J4.2 | **A menükomponensek is kapnak saját NTAK-kategóriát** — a G3 szétbontás miatt minden komponens önálló tétel, tehát önálló kategóriát igényel. |

### `[ELDÖNTVE]` J5 — A MUNKANAP hossza

| Küszöb | Viselkedés |
|--------|-----------|
| **23:00** | **Enyhe** figyelmeztetés |
| **23:30** | **Erős** figyelmeztetés |
| **23:45** | **Kíméletlen kényszerzárás** — nem mehet tovább |

Az abszolút (UTC) alapú számolás (H2) változatlanul él.

**Két kiegészítés, ami a küszöbnél fontosabb:**

| # | Kiegészítés |
|---|-------------|
| J5.1 | **TILOS előre állítani az órát nyitott üzleti nap közben.** A `nyitasIdopontja` és a `zarasIdopontja` is a mi óránkról jön, tehát az abszolút elcsúszás kiesik a különbségből — **kivéve, ha menet közben javítunk**. Az I5 szerinti csendes, 15 percig terjedő előre-korrekció **felfújná a rögzített időtartamot** és elutasítást okozna. **Az óra-korrekció a napnyitáskor történik, nyitott nap közben soha** (visszafelé állítás sem, mert az meg a sorrendet keverné). |
| J5.2 | **Kell TERVEZETT napzárási időpont** (üzletenként állítható, pl. 05:00). Enélkül egy 0–24-es helynél a kényszerzárás **naponta 15 perccel korábbra vándorol** — négy nap alatt egy órát, egy hónap alatt körbeér, és **előbb-utóbb szombat este 22:00-kor, csúcsban fog lecsapni.** A tervezett zárással a határ mindig ugyanabban a csendes órában van, és a kényszerzárás soha nem lép működésbe. **Ez a valódi megoldás a 0–24-es helyre, nem a küszöb nagysága.** |

**Miért 23:45 és nem 23:55 — a „kieső idő" félreértése:**
a zárás után **azonnal nyílik az új nap**, tehát nem esik ki 15 perc üzemidő.
Kiesés = a zárási művelet hossza, ami mindkét küszöbnél ugyanannyi. A különbség
éves szinten: 0–24-es helyen kb. **369 vs. 366 napciklus**, azaz **3 extra zárás
évente**. A biztonság tehát gyakorlatilag ingyen van, egy elutasított NTAK-beküldés
visszamenőleges javítása viszont nem.

### `[NYITOTT — 0–24-es helyeknél MINDENNAPOS]` J6 — Mi történik a nyitott asztallal a munkanap-határon?

Egy 0–24-es helyen a kényszerzárás pillanatában **ülnek vendégek nyitott
asztaloknál**. A rendelést nem lehet lezárni (nem kértek számlát), és nem lehet
kettévágni (a vendég egy számlát kap).

**Javaslat:** a rendelés **átlép a határon**, és ahhoz a tárgynaphoz tartozik,
**amelyikben elkezdődött** — összhangban azzal, hogy a tárgynap a nyitás
dátumából származik (H1). Az `rendelesVege − rendelesKezdete <= 24 óra` korlát
(H6.5) továbbra is köti.

⚠️ **Amit ellenőrizni kell:** elfogadja-e az NTAK, ha egy tárgynapra már beérkezett
a napi zárás, és **utána** még jön arra a tárgynapra rendelésösszesítő. A
specifikációban erre nem találtam kifejezett tiltást, de **nem is találtam
engedélyt**. → megkérdezendő, mert 0–24-es helyen ez nem élhelyzet, hanem
mindennapos.

### `[ELDÖNTVE]` J7 — A nyitott rendelés 24 órás korlátja csak a beküldöttekre vonatkozik

**Vendégasztal:** valóban nem lehet 24 óránál tovább nyitva.
**Személyzeti asztal / selejt:** lehet, mert **nem kerül NTAK-beküldésre.**

⚠️ **Feltétel, amit igazolni kell:** hogy a személyzeti fogyasztás és a selejt
tényleg nem NTAK-köteles. Az NTAK ismer `EGYEB / NEM_VENDEGLATAS` tételkategóriát,
a rendelésbesorolás értékkészlete viszont csak `NORMAL / SZTORNO / HELYESBITO` —
**„nem forgalmi" rendelés-besorolás nincs.** Ha kiderül, hogy a személyzeti
fogyasztást is jelenteni kell, a 24 órás korlát rájuk is vonatkozik.
→ **megkérdezendő.**

**Ettől függetlenül kell egy belső korlát**: egy hetek óta nyitott személyzeti
asztal üzemeltetési hiba. Javaslat: figyelmeztetés a napnyitáskor minden olyan
nem-vendég rendelésre, ami régebbi az előző munkanapnál.

### `[HELYESBÍTÉS — ez NEM az ügyfél feladata]` J8 — A zárva tartott nap bejelentése a MI szoftverünk kötelezettsége

A felhasználó álláspontja az volt, hogy a nyitvatartást az ügyfél állítja be az
NTAK oldalán, ehhez nekünk nincs közünk. **A specifikáció ezt egyértelműen
cáfolja** — szó szerint:

> „**Napi zárási üzenetet akkor is küldenie kell minden RMS szoftvernek**, ha az
> adott tárgynapon zárva tartott a vendéglátó üzlet. Ekkor **adott napon zárva**
> besorolású napi zárás üzenetet kell küldeni, mely esetben a nyitás és zárás adat
> megadására nincs szükség […] Abban az esetben is kell napi zárás üzenetet
> küldeni, ha a nyitvatartás során nem került beküldésre rendelésösszesítő.
> Ekkor a napi zárás üzenetben meg kell jelölni, hogy **forgalom nélküli napot**
> zárt a vendéglátó üzlet."

Ez **az RMS szoftverre** kimondott kötelezettség, nem az NTAK portálra.
**„A napi zárás üzeneteket minden tárgynapra vonatkozóan be kell küldeni."**

**Ebből következően tudnunk kell, mikor van zárva** — máskülönben nem tudjuk
megkülönböztetni a „zárva volt" és a „elfelejtettek napot nyitni" esetet, pedig
az egyik `ADOTT_NAPON_ZARVA`, a másik hiba.

**Javaslat (a legkisebb súrlódású megoldás):**

1. **Nyitvatartási minta** (heti séma + kivételnapok/ünnepek) — egyszer beállítva magától megy.
2. **Rákérdezés**, ha egy tárgynapra nem nyílt nap és nincs is rá szabály: a következő napnyitáskor egy kérdés — „tegnap zárva voltatok?" — és a válasz alapján megy a `ADOTT_NAPON_ZARVA` vagy `FORGALOM_NELKULI_NAP`.

*Ha az NTAK portál kínál kézi utat a zárva tartott napok bejelentésére, az
elméletben kiváltja — de azt az ügyfélnek minden egyes zárva töltött napra
kézzel meg kellene tennie. Ezt senki nem fogja megbízhatóan csinálni,
és a hiányzó napi zárás a MI szoftverünkre nézve mulasztás.*

### `[ELDÖNTVE — a felhasználó döntése felülírja a korábbit]` J9 — Egész forint mindenütt

A H6.3 lelet az volt, hogy a `bruttoEgysegar` tört is lehet, tehát a menü-szétosztás
tört egységárral megoldható. **A döntés ezzel szemben:**

> **Az adóügyi eszköz forintban törtet nem kezel, csak egész számot. Az NTAK
> viszont igazítható hozzá, amíg az összeg stimmel. Ezért az EGÉSZ FORINT
> a meghatározó, és legyen egységes mindenütt.**

**Ez helyes, és nem csak egységesség kérdése — technikailag is jobb:**
az egész egységár **mennyiséggel pontosan szorzódik**. Tört egységár + egész
sorösszeg esetén 3 db menünél soronként kerekítenénk, és a három sor összege
**nem feltétlenül adná ki a 3× menüárat** — pont azt a szabályt sértenénk meg,
amit a H6.2 kötelezővé tesz.

**Menü-szétosztás véglegesítve:** a komponensek **egész forintos egységárat**
kapnak, a listaárak arányában, a kerekítési maradék a legnagyobb komponensre.
Az egységárak összege pontosan a menü ára → tetszőleges mennyiséggel felszorozva
is pontos marad.
