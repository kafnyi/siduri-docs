# ELLENŐRZÉS — 2. kör: ADVERZARIÁLIS

> **Kérte:** a felhasználó, 2026-08-22. Szó szerint: *„egy szkeptikus ellenőrzés a
> teljes tervre, hogy hol csúszhat félre, mi nem jó, mi hiányos, illetve az első
> ellenőrzés pontjai, csak sokkal szkeptikusabban."*
>
> **MÓDSZERTAN (MERNOKISAROKKOVEK §11):** ebben a körben **a feladat a CÁFOLAT,
> nem a megerősítés.** Bizonytalanságnál az alapértelmezés: **cáfolva.**
> Perspektíva-diverz lencsék: megvalósíthatóság / helyesség / megfelelés /
> üzemeltethetőség / üzleti életképesség.
>
> **KIEMELT CÉLPONT (§11):** **az ebben a munkamenetben hozott ~50 döntés** —
> mert a leletek többsége mindig a friss munkában van, nem a régiben.
> **Beleértve a SAJÁT javaslataimat is.**
>
> **Ez a hangnem szándékos.** Nem azt írom le, mi jó a tervben — azt az
> 1. kör megtette. Itt azt írom le, **hol dől el.**

---

# A1. A LEGSÚLYOSABB LELET: a terv nem 2–3 fős méretű, és senki nem mondta ki

## A tény

Vegyük végig, mi lett **elkötelezve** ebben a munkamenetben és korábban:

| Terület | Mit tartalmaz |
|---|---|
| Telephelyi szerver | Java, **GraalVM native** (lassú build, reflection-pokol), PostgreSQL-hangolás |
| POS kliens | WPF: asztaltérkép, számlabontás, fogások, kedvezmények, módosítók, másodkijelző, kioszk mód |
| Flutter kliensek | **négy alkalmazás**: PDA, KDS, rendeléskijelző, standoló |
| Frissítő | **szerepismerő, sorrendezett**, a failoverrel összehangolt |
| Felhő | API + **teljes webes admin**: raktár, receptúra, BI, több telephely, franchise, zárolás, távoli konfiguráció |
| Telephelyi HA | replikáció, failover, fencing, **tanú-séma**, **Munkanap-összefésülés** |
| Felhős HA | **3 csomópont**, szinkron, mentés, **bérlőnkénti visszaállítás** |
| Csökkentett mód | outbox + degradált felület + **visszatéréskori egyeztetés** — **mind az MVP-ben** |
| Archívumok | POS-onként **és** vékonykliensenként |
| Fiskális | **három üzemmód**, **két eszközgeneráció**, gyártófüggő protokollok |
| NTAK | integráció + **MTÜ-validáció** |
| Szimulátorok | fiskális eszköz, bankterminál, NTAK, ESC/POS |
| Mérés | önálló fázis, fizikai referenciahardverrel |

**Ez nem 2–3 fős projekt. Ez nagyságrendileg egy 15–30 ember-éves program.**

## `[!]` És van egy MINTÁZAT, ami ennél is aggasztóbb

**Végignéztem a munkamenet tizenhét körét: MINDEGYIK BŐVÍTETTE a scope-ot.
Egyetlen kör sem szűkítette.**

- A vészhelyzeti szerver bent maradt (az ajánlás ellenére).
- A csökkentett mód **mindhárom része** bekerült az MVP-be — **a vészhelyzeti
  szerver MELLETT**, amit ugyanaz a baj ellen véd.
- A felhő „licenc + mentés"-ből **teljes menedzsment-platform** lett.
- Megjelent a **franchise/lánc** szint.
- Megjelent a **három fiskális üzemmód**.
- Megjelent a **kockázatvállalási nyilatkozat aláírással és felhő-továbbítással**.
- Megjelentek a **szerkeszthető jogosultsági szintek**.
- Megjelent a **kliens-archívum**, majd a **vékonykliens-archívum**.

**Minden egyes bővítés ÖNMAGÁBAN védhető volt** — ezért nem tűnt fel.
**Együtt viszont a projekt már nem szállítható.**

## Mit javaslok — és ez nem funkciók törlése

**Nem azt mondom, hogy vegyünk ki dolgokat a TERMÉKBŐL.** Azt mondom, hogy
**a fázistervnek (`E1`) kíméletlenül szűknek kell lennie**, és a mostani
döntéslista **NEM az MVP, hanem a TERMÉK VÍZIÓJA.**

**Ez a kettő eddig nincs szétválasztva a doksikban, és ez a legveszélyesebb
állapot** — mert minden döntés úgy néz ki, mintha az MVP része lenne.

**Konkrét javaslat:** a `NYITOTT_KERDESEK.md` minden lezárt döntése kapjon
**egy címkét: `MVP` / `v1` / `v2` / `vízió`** — és **az MVP-címkék összegének
elférhetőnek kell lennie** 2–3 emberrel, egy belátható időn belül.
**Ha nem fér el, az a fázisterv első leletje lesz, nem a fejlesztésé.**

---

# A2. A TERV MÉLY AZ INFRASTRUKTÚRÁBAN ÉS ÜRES A TERMÉKBEN

## A tény, amit nehéz elhinni, amíg ki nem mondja valaki

**Tizenhét kör tervezés után NINCS TERMÉKMODELLÜNK.**

A `C1` tétel **változatlanul nyitva van**, és ezt tartalmazza:
- **módosítók és feltétek** (kötelező/opcionális választócsoportok, ár-delta),
- **menük / combók**,
- **a „kiszerelés" fogalma** — a spec hivatkozik rá, **sehol nincs definiálva**,
- **többszintű receptúra**,
- allergének, nyitott árú tételek,
- **súly szerinti termékek + mérleg** — sehol nem szerepel.

**Egy vendéglátó POS a módosítókon áll vagy bukik.** „Hamburger, hagyma nélkül,
extra sajttal, közepesen átsütve" — **erre jelenleg nulla terv van**, miközben
a failover-mechanizmusra ötven oldal.

## Miért történt ez, és miért fog megismétlődni

**Az infrastruktúra-kérdések ELÉGGÉ ÉRDEKESEK ahhoz, hogy elvigyék a
beszélgetést**, és mindegyiknek van egy „ha most nem döntjük el, később drága"
indoklása — ami **igaz is.** A termékmodell viszont **nem izgalmas**, és
látszólag ráér.

**De a termékmodell is „most olcsó, később drága":** a módosító-szerkezet
**a bizonylattételbe, a receptúrába, a nyomtatásba, a KDS-be, az NTAK-adatba és
az árrés-számításba is beleér.** Utólag beépíteni **ugyanolyan drága**, mint
egy idempotencia-kulcsot.

## `[!]` És egy konkrét, azonnal látható következmény

Az 1. kör leletje szerint **az NTAK RMS interfész-leírását a kódolás előtt kell
elolvasni**, mert **adatmodell-követelményeket ír elő.**
**Ugyanez igaz az e-nyugta sémára is.**

> **Vagyis: a termékmodellt nem lehet megtervezni a két külső séma ismerete
> nélkül — és a két külső sémát még senki nem olvasta el.**

**Ez a jelenlegi legnagyobb egyetlen hiányosság a tervben.**

---

# A3. `[!]` A LEGFOUNDÁLTABB DÖNTÉS MÉG MINDIG NINCS MEGHOZVA: a PÉNZ ÁBRÁZOLÁSA

Az `F2` tétel **nyitva van**, és ezt tartalmazza:
- **pénz: egész, minor-egység alapú** — soha nem lebegőpontos,
- **mennyiség: decimális** (3 dl, 0,42 kg),
- a **kerekítés egy nevesített helperen** menjen át, **dátumozva.**

**Ez a legolcsóbban eldönthető és a legdrágábban javítható döntés az egész
tervben** — és tizenhét kör alatt **egyszer sem került elő.**

**Miért kritikus, konkrétan:** a terv tartalmaz **arányos kedvezmény-elosztást
vegyes ÁFA mellett** (spec 13.), **5 Ft-os kerekítést**, **mozgó átlagárat**,
**árrés-számítást kalkulált veszteséggel**, és **EUR/HUF váltást**.
**Ez az öt együtt a rendszer legkockázatosabb számítása** — és ha az alaptípus
rossz, **mind az öt csendben hibázik.**

**`[!]` Javaslat: ezt a fázisterv ELŐTT döntsük el, ma.** Öt perc, és utána
minden más számítás rá épülhet.

---

# A4. AZ ÖNCÁFOLAT: hol tévedtem ÉN ebben a munkamenetben

**§11 szerint a saját friss munkám a legkockázatosabb.** Négy pont:

## `[!]` A4.1 — Tévedtem: az NTAK-küldést IGENIS érinti az összefésülés

**Azt állítottam** (`F4/K2`), hogy a Munkanap-összefésülés az NTAK-ot nem
érinti, mert az NTAK egysége a **naptári tárgynap**, nem a Munkanap.

**A TARTALOMRA igaz. A KIVÁLTÁSRA NEM.**

Az `L4` lelet szerint a szoftver **„a nap lezárását követően"** küldi az adatot.
**Ha egy naptári dátumra több Munkanap esik, akkor több „nap lezárása" is
történik** — tehát:
- **melyik zárás váltja ki a küldést?**
- ha mindegyik → **többszörös küldés ugyanarra a tárgynapra**;
- ha csak az első → **a többi Munkanap forgalma kimarad**;
- ha az összefésülés után küldünk → **késhetünk a határidőből.**

**Ez az én elemzésem hibája volt, és pont az a fajta, ami ellen a módszertan
véd: egy megnyugtató állítást tettem ellenőrzés nélkül.**
**`[ ]` Ezt tisztázni kell az RMS interfész-leírásból.**

## `[!]` A4.2 — Lyuk a saját „előre kiosztott Munkanap-azonosító" ötletemben

Az ötlet: a szerver előre kiosztja a következő Munkanap azonosítóját, hogy
offline mindenki ugyanazt nyissa.

**A lyuk:** mi van, ha a szerver **kiosztja X-et**, majd **helyreáll**, és
**normál úton nyit egy MÁSIK Munkanapot (Y)** — miközben egy gép, ami közben
végig offline volt, **később X-et nyitja meg?**
**Megint két Munkanap van** — pontosan az, amit el akartam kerülni.

**Javítás:** az azonosító **egyszer használatos és érvényteleníthető** — amint a
szerver normál úton Munkanapot nyit, **a kiosztott azonosító elévül**, és a
visszatérő gép ezt **a visszacsatlakozáskor megtudja.** De **amíg offline, nem
tudhatja** → **a 3. réteg (átsorolás) ezt az esetet is kezelnie kell.**
**Az ötlet tehát csökkenti a gyakoriságot, de nem szünteti meg az esetet** —
ezt korábban túl magabiztosan fogalmaztam.

## A4.3 — A három csomópontos felhő ára pénz, és ezt nem árazta senki

Javasoltam a **3 szervert 2 helyett** — technikailag helyes, **de egy
bevétel előtti terméknél ez +50% infrastruktúra-költség**, határozatlan ideig.
**Ezt üzleti döntésként kellett volna felvetnem, nem mérnökiként.**

## A4.4 — A „nem adóügyi bizonylat" jelölésről nincs forrásom

Kimondtam, hogy az 1. módban a nyomtatott papírt kötelezően meg kell jelölni.
**Ez józan ész, de nem forrásolt jogi állítás** (§13.5).
**Vagy szerezzünk rá forrást, vagy fogalmazzuk át: „a felelősség csökkentése
érdekében javasolt", ne „kötelező".**

---

# A5. A TERV EGYETLEN LEGNAGYOBB, MÉG NYITOTT KOCKÁZATA

## Ha a bizonylat-számozás jogi kérdése rosszul dől el, HÁROM döntés omlik össze

Az `L5` lelet szerint a számviteli törvény **„sorszáma, vagy egyéb más
azonosítója"**-t ír — **de ezt másodlagos forrásból olvastam**, és kimondtam,
hogy könyvelői megerősítés kell.

**Amire ez a válasz épül, láncban:**
1. **eszközönkénti számtartomány** (`B14`) →
2. **a számláló a DÁTUMHOZ kötődik, nem a Munkanaphoz** (`F4/K1`) →
3. **az összefésülés mechanikusan megoldható**, mert nem kell számot átírni
   (`F4/K2`) →
4. **a tartalék szerver azonnal kiszolgálhat**, nem kell begyűjtésre várnia
   (`B13`).

> **Ha a válasz az, hogy EGYETLEN, globális, folytonos sorozat kell, akkor
> mind a négy megdől** — és visszatér a szerver-oldali központi számláló,
> az ütközés-kockázat, az összefésülés nehézsége és a blokkoló begyűjtés.

**Ez a legmagasabb tétű, legolcsóbban tisztázható nyitott kérdés az egész
tervben.** Egy könyvelői mondat. **Ne a fázisterv után legyen meg.**

---

# A6. A KÜLSŐ KAPUK URALJÁK A HATÁRIDŐT, NEM A FEJLESZTÉS

Három külső, tőlünk **nem függő** kapu, mindegyik **sorbaállással**:

| Kapu | Állapot | Blokkol |
|---|---|---|
| **MTÜ-validáció (NTAK)** | **IGAZOLT, kötelező** | NTAK-köteles hely kiszolgálása = **a célpiac** |
| **Fiskális: kell-e engedély a szoftvernek?** | **`[?]` ismeretlen** | a 2. és 3. fiskális mód |
| **Gyártói protokolldokumentáció (NDA)** | nem indult el | sztornó, függő tranzakció, offline plafon |

**`[!]` A szkeptikus olvasat:** a „mikor lesz első fizető ügyfél" kérdésre a
választ **nem a fejlesztési sebesség adja meg, hanem ez a három sor.**
És **egyik sincs elindítva.**

**Ez a fázisterv legfontosabb bemenete, és ma nem tudjuk.**

---

# A7. AZ OFFLINE-FIRST USP OTT A LEGGYENGÉBB, AHOL A CÉLPIAC VAN

**Szkeptikus összegzés az eddigi döntésekből:**

| Telepítés | Mit ad az offline-first? |
|---|---|
| **1 Windows POS = szerver** (a legkisebb ügyfél) | **SEMMIT.** A gép halálakor minden áll — a csökkentett mód is azon a gépen futna |
| 2–3 POS, tartalék nélkül | a nem-szerver POS-ok tudnak eladni |
| Dedikált szerver + POS-ok | minden POS tud eladni — **itt működik igazán** |

**És 2028-tól** az e-pénztárgép **72 órás** offline plafonja **minden módban**
korlátoz.

> **Vagyis: az USP a legkisebb ügyfeleknél nem ad többet, mint bármelyik
> hagyományos, helyben telepített POS — miközben a marketing róluk szól.**

**Ez nem mérnöki hiba, hanem POZICIONÁLÁSI kockázat.** Ha egy versenytárs
rákérdez, nincs jó válasz — hacsak **most nem fogalmazzuk újra**, hogy az
offline-first **mire is véd** (internetkimaradás ✔, hálózati hiba ✔,
egyetlen gép hardverhibája ✘ az egygépes lépcsőn).

---

# A8. A TERV OLYAN TÁMOGATÁSI SZERVEZETRE ÉPÜL, AMI NEM LÉTEZIK

**Hányszor hivatkozik a terv a „support"-ra vagy egy elérhető emberre?**

- challenge–response szerviz-belépés → **valaki generálja a felhőben**;
- a szuperfiókos műveletek → **valaki jóváhagyja**;
- a hibás átkapcsolás feloldása („mindkét eszköz tiltva, amíg ember fel nem
  oldja") → **valaki feloldja**;
- a diagnosztikai csomag, a péntek esti hívás (`F5`) → **valaki felveszi**;
- az árva tranzakciók rendezése → **valaki elvégzi**.

**A csapat 2–3 fő.** **Nincs terv arra, ki veszi fel a telefont pénteken
22:00-kor** — és **a rendszer több biztonsági mechanizmusa MŰKÖDÉSKÉPTELEN
nélküle.**

**`[!]` Ez nem „majd megoldjuk" kategória:** a `B12` kockázatvállalási
nyilatkozattól kezdve a fiskális felelősségi határokig **a termék jogi és
üzleti felépítése feltételezi, hogy van kit hívni.**

**`[ ]` A támogatási modell (elérhetőség, válaszidő, ki, mennyiért) a
fázisterv része kell legyen, nem utómunka.**

---

# A9. A MÉRÉST A VÉGÉRE TETTÜK — ÉS EZ ROSSZ, EGY PONTON

**A felhasználó utasítása:** *„az első tényleges teszt esetén legyen mérve
minden is."* **Ez a TELJES mérési suite-ra helyes.**

**De három döntés MA is FOGADÁS a teljesítményre**, és mindhárom
**architekturális**, nem finomhangolási:

1. **A kombinált szerver + POS egy J1900-on az ALAPÉRTELMEZETT telepítés** (`M1`).
2. **A tartalék POS átveszi a teljes terhelést** — csúcsidőben (`M12`).
3. **Ugyanaz a gép szolgálja ki a webes admint is** (`M14`).

> **Ha bármelyik megbukik, nem egy funkciót kell javítani, hanem a
> TELEPÍTÉSI MODELLT eldobni — miután minden megépült.**

**`[!]` Ezért tisztelettel, de határozottan nem értek egyet azzal, hogy MINDEN
mérés a végére kerüljön.** Javaslat:

> **Egy néhány napos, eldobható ELŐMÉRÉS, MOST**, a fázisterv előtt:
> egy valós J1900, rajta PostgreSQL + egy üres Java szolgáltatás + egy WPF ablak
> + egy 720p videó a másodkijelzőn, és egy szintetikus terhelés.
>
> **Nem a Siduri kell hozzá** — csak a hardver és fél hét munka.
> **Ez a legolcsóbb módja annak, hogy a legdrágább feltevésünket még azelőtt
> megcáfoljuk, hogy ráépítenénk mindent.**

---

# A10. RÖVIDEN: AMI TELJESEN ÉRINTETLEN MARADT

Tizenhét kör után **ezekhez senki nem nyúlt**, pedig több közülük **blokkoló
vagy szerződéses átfutású:**

| Tétel | Miért fáj |
|---|---|
| **`B4` — ki nyomtat, a szerver vagy a kliens?** | **A teljes nyomtatási alrendszer erre épül.** Alapkérdés, nincs eldöntve. |
| **`B5` — melyik fizetési szolgáltató (SoftPOS)?** | **Szerződés, átfutási idővel.** És eldönti, melyik eszközön van a kártyás fizetés. |
| **`B2` — mi a konkrét üzenetsor?** | Javaslat volt (outbox-tábla), **döntés nem.** |
| **`C1` — termékmodell** | Lásd `A2`. **A legnagyobb hiány.** |
| **`D5` — szimulátorok** | **Enélkül nincs automata teszt** a fiskális, banki és NTAK ágra — vagyis a legkockázatosabb részekre. |
| **`D4` — óraszinkron** | A bizonylatszám dátumot tartalmaz. **Az óra most már bizonylat-helyesség kérdése.** |
| **`D3` — verziókompatibilitás** | POS v1.2 + szerver v1.4. És **az MTÜ-igazolás verzióhoz kötött** — újravalidálás kell-e? |
| **`C7` — audit log** | A terv **tucatnyi helyen hivatkozik auditra** — de maga az audit nincs megtervezve. |
| **`D7` — nyelv és pénznem** | EUR-elfogadás említve; **multi-currency vagy sem, nincs eldöntve.** |

---

# ÖSSZEGZÉS — a hat dolog, amit ebből tenni kell

| # | Mit | Miért most |
|---|-----|-----------|
| **1** | **Döntsük el a pénz- és mennyiség-ábrázolást** (`F2`) | Öt perc, és minden számítás rá épül. **Ma megtehető.** |
| **2** | **Szerezzünk könyvelői megerősítést a bizonylat-számozásra** | Egy mondat, és **négy döntés függ tőle** (`A5`). |
| **3** | **Indítsuk el a három külső kaput** (MTÜ, NAV-kérdés, gyártói NDA) | **Ezek uralják a határidőt**, nem a fejlesztés (`A6`). |
| **4** | **Olvassuk el az RMS interfész-leírást és az e-nyugta sémát** | **A termékmodell nem tervezhető nélkülük** (`A2`). |
| **5** | **Egy néhány napos ELŐMÉRÉS valós J1900-on** | A legdrágább feltevés cáfolata, mielőtt ráépítünk (`A9`). |
| **6** | **A fázisterv első dolga: MVP / v1 / v2 / vízió címke MINDEN döntésre** | Enélkül a mostani lista **úgy néz ki, mintha mind MVP lenne** (`A1`). |

## És egy mondat, amit ki kell mondani

**A terv MINŐSÉGE magas.** A döntések indokoltak, a premisszák jelölve vannak, a
hibáinkat visszavontuk, a jogi állítások forrásoltak. **Ez ritka.**

**A terv MÉRETE viszont nem illeszkedik a csapathoz** — és ezt eddig
**egyetlen dokumentum sem mondta ki.** A fázisterv nem „a következő tétel"
lesz, hanem **az a pont, ahol ez a feszültség eldől.**
