# Siduri — Nyitott kérdések és specifikációs hiányok

> **Státusz:** nyitott, kódolás előtti tisztázásra vár.
> **Forrás:** `siduri_spec_hu.md` + `siduri_superprompt_en.md` átolvasása (2026-08-22).
> **Utolsó frissítés:** 2026-08-22 — A1, A2, A2/a, B3, E2 eldöntve; B1+A4 javaslat megírva (döntésre vár); F) szakasz felvéve.
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

### `[ ]` A4 — Failback csak Szuperfiókkal
HU 17. / EN 17.: a Master visszaállítása csak Siduri Systems szuperfiókkal
történhet. De a helyzet definíció szerint az, hogy a hely offline / szerverhiba van
— **pont akkor nem érhető el a support.**

Kell egy offline útvonal: challenge-response kód telefonon, vagy helyi menedzser +
fizikai megerősítés.

#### `[JAVASLAT — DÖNTÉSRE VÁR]` Kétszintű failback
> **Státusz: NEM eldöntött.** A B1-gyel EGYÜTT dőljön el, mert ugyanaz a
> mechanizmus. Lásd a B1 alatti javaslatblokkot.

- **Normál visszaállás:** helyi menedzser, a lokális admin felületen, egy
  képernyővel, ami **konkrétan kiírja, hány tranzakció veszne el** (§5: néma
  csonkolás helyett szám — „nincs több" látszatot ne keltsünk).
- **Szuperfiók CSAK a veszélyes változathoz:** amikor a két adatbázis
  szétdivergált, és az egyiket felül kell írni.

Így a támogatás elérhetetlensége nem blokkolja a normál esetet, viszont a
visszafordíthatatlan műveletnél megmarad a négy szem.

---

## B) Architekturális döntések, amiket a spec nyitva hagy

### `[ ]` B1 — Split-brain 2 node-dal matematikailag nem oldható meg
Master + Emergency = 2 szavazó, **nincs kvórum**. Kell egy harmadik tanú (witness):
egy POS kliens, egy olcsó RPi, egy shared lock a felhőben — vagy **explicit emberi
failover** (a menedzser nyom egy gombot).

Kapcsolódó, külön eldöntendő: a PostgreSQL replikáció
- **aszinkron** → failovernél elveszik az utolsó néhány tranzakció, vagy
- **szinkron** → ha a Standby leáll, a Master is megáll.

Mindkettőnek üzleti következménye van; ki kell mondani, melyiket vállaljuk.

---

#### `[JAVASLAT — DÖNTÉSRE VÁR]` A 2026-08-22-i átbeszélés eredménye

> **Státusz: NEM eldöntött.** A felhasználó azt kérte, beszéljük még át. Az alábbi
> öt pont javaslat, nem döntés — **erre építeni nem szabad.**

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

**3. Javasolt scope-döntés:** a teljes HA (Emergency Server, replikáció, failover,
fencing, split-brain tesztelés) **kerüljön ki az MVP-ből**, DE az **epoch-mező
kerüljön be a protokollba az első naptól**, akkor is, ha egyelőre mindig `1`.
Most ingyen van; utólag beletenni azt jelenti, hogy minden kliens minden
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

**Állapot 2026-08-22 után:** A1, A2, A2/a, B3, E2 eldöntve. Maradt két blokkoló:

| # | Tétel | Státusz | Miért blokkoló |
|---|-------|---------|----------------|
| 1 | **B1** | `[ ]` **NYITVA** — javaslat megírva, döntésre vár | Failover: automatikus witness-szel vagy emberi megerősítéssel? Szinkron vagy aszinkron replikáció? Kikerül-e a HA az MVP-ből? |
| 2 | **E1** | `[ ]` **NYITVA** — a fázisterv még nincs megírva | Mi az MVP scope-ja? Enélkül nincs mihez mérni a haladást. **B1 után** írandó. |
| — | ~~A1~~ | `[ELDÖNTVE]` | WPF, Windows 10 IoT Enterprise LTSC only. |
| — | ~~A2~~ | `[ELDÖNTVE]` | Szerver-autoritatív + degradált gyorseladás. **Feltételes**: igazolatlan AEE-premisszán áll. |
| — | ~~A2/a~~ | `[ELDÖNTVE]` | Kettős kieséskor a nyitott asztalok nem elérhetők → kézi újrafelütés. |
| — | ~~B3~~ | `[ELDÖNTVE]` | J1900 vegyes bázis (szerver ÉS kliens) → GraalVM kényszer marad, plusz szoros WPF perf-költségvetés. |
| — | ~~E2~~ | `[ELDÖNTVE]` | 2–3 fős csapat + AI → B8 az első hét tétele. |

**Az A4 (failback) a B1-gyel EGYÜTT dőljön el** — ugyanaz a mechanizmus.

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
