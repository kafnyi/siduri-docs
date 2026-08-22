# Mérnöki sarokkövek — projekt-független szabálygyűjtemény

> Egy hosszú, több-repós adverzariális átvizsgálási munkamenet során kikristályosodott
> szabályok. Mindegyik mögött VALÓS hiba áll — ezért az indoklás („miért") a szabály
> része, nem díszítés. Indoklás nélkül a szabályok nem tapadnak meg, és a következő
> kör újra elköveti ugyanazt.
>
> Használat: másold be az új projekt `CLAUDE.md`-jébe (vagy egy hivatkozott
> `METHODOLOGY.md`-be), és told hozzá a projekt-specifikus részt külön szakaszban.

---

## 1. Az őrökről (tesztek, szkennerek, lintek)

### 1.1 „Az őr nem azt méri, amit véd" — ez a domináns hibaosztály
A leggyakoribb néma hiba nem a kódban van, hanem az őrben. Négy alakja:

- **Komment-kielégítés.** A forrás-alapú szabály illeszkedik egy KIKOMMENTELT sorra
  vagy egy kommentben idézett mintára. → **Forrás-alapú ellenőrzés KIZÁRÓLAG
  komment-mentesített kódon mérhet.** (Ez a szabály önmagában is buktatható: a
  komment-mentesítőnek ismernie kell a nyelv string-literáljait, escape-eit és a
  verbatim/raw string alakokat, különben rövidebb másolatot ad és az indexek
  elcsúsznak.)
- **Rossz kódút.** Az őr olyan függvényt hív, amit a védett bemenet SOSEM ér el.
  → **Mielőtt egy tesztet „a szerződés őrének" nevezel, kövesd végig, MELYIK
  KÓDÚTON érkezik az, amit véd.** Volt olyan tesztem, ami négy „védett" stringre
  mért egy olyan tölcséren, amit a javítás hozzá sem ért — triviálisan zöld volt.
- **Proxy, nem jelenség.** Az őr egy könnyen mérhető helyettesítőt mér a tényleges
  veszélyes alak helyett. → A mérce a JELENSÉG legyen. (Pl. nem „ki ír `X: Y`-t",
  hanem „feltételes fájlművelet + feltétel nélküli állapot-írás".)
- **Túl tág vagy túl szűk ablak.** Egy mohó regex a külső `try`-tól indul és elnyeli
  a keresett mintát; egy karakter-távolságra kötött szabály a többsoros alakot
  átengedi. → **Szerkezeti mérce (blokk, zárójel-mélység) a karakter-távolság
  helyett.**

### 1.2 Minden őrt MUTÁCIÓVAL kell hitelesíteni — TÖBBFÉLÉVEL
„Megírtam és szabotázzsal próbáltam" **önmagában NEM elég**, ha a szabotázs a saját
regexem képére készült. Minimum-készlet minden új szabályhoz:

1. a valódi, eredeti hiba visszaállítása,
2. a szabály KIKOMMENTELÉSE (nem törlése),
3. átnevezés / horgony elmozdítása (az őr ne essen NÉMÁRA — a padló fogja),
4. operandus-csere vagy sorrend-csere (nem csak törlés),
5. **negatív kontroll**: egy változtatás, aminek NEM szabad jeleznie.

Ha egy mutáció „nem kapta el", az kétféle lehet: (a) az őr hiányos → javítsd;
(b) a mutáció valóban ártalmatlan → **mondd ki, és írd le a korlátot**. Ne fabrikálj
olyan őrt, ami úgy tesz, mintha mérne valamit, amit elvileg sem tud.

### 1.3 Minden őr LEGYEN PADLÓS
`0 vizsgált elem = HIBA`, nem siker. Padló kell a **bejárt** ÉS a **ténylegesen
mért** halmazra is (a kettő külön szűkíthető). Egy elrontott regex, egy átnevezett
horgony vagy egy elgépelt útvonal enélkül néma zöldet ad.

Ugyanez a teszt-FUTTATÓRA is: legyen padló a lefuttatott ellenőrzések SZÁMÁRA.
Kimérve: egy `if (true) return;` a `check()`-ben `0 pass, 0 fail`-t ad **EXIT 0-val**.

### 1.4 A futtató maga is hazudhat — négy módon
- **Csonkolás:** egy `unref`-elt timer kiüríti az event-loopot → a suite a KÖZEPÉN
  áll le, 0-s kóddal, „zöld" kimenettel. Semmilyen `check()` nem foghatja meg (nem
  egy állítás bukik, hanem a MÉRÉS szakad félbe). → **process-szintű őr** minden
  futtatóra: a `summary()` lefutott-e.
- **Nem awaitolható export:** a suite bukásai elvesznek, és a végösszeg BITRE a
  baseline marad — a kézi összevetés sem fog rajta.
- **`check(név, Promise)` MINDIG igaz.** Egy Promise truthy. Tiltsd vagy detektáld.
- **Duplikált teszt-nevek:** két állítás egy néven → az egyik eltűnik a kimenetből.

### 1.5 Az ingadozó őr rosszabb a semminél
Ha az időzítés ingadozna, használj **szerkezeti** mércét. Ha muszáj időt mérni,
használj **arányt, ne abszolút küszöböt** — az arány gép-sebességtől független.

> Konkrét eset: egy DoS-plafon eltávolítása 0,15 → 2,12 ms-ot jelentett. Nincs olyan
> fix ms-küszöb, ami stabilan elválasztaná. Az „a munka NE skálázódjon a bemenet
> méretével" arány viszont igen: plafonnal 0,91–1,10, nélküle 12,68–14,25 → a 4-es
> léc mindkét sávtól 3-4× távol van.

### 1.6 A teszt a SZERZŐDÉST mérje, ne beégetett feliratot
Ha egy teszt egy megjelenítendő literálra (`"Host"`, `"When may we start: <ts>"`)
illeszt, akkor a JOGOS javítás töri el. A teszt tárgya a LEKÉPEZÉS: mérj a
szótárhoz / a másik oldalhoz / az invariánshoz. Ha egy javítás tesztet tör, előbb
kérdezd meg: a teszt a szerződést védte, vagy csak a tegnapi kimenetet?

### 1.7 Az őrt is fejleszteni kell, ha új hívási út születik
Az őr annyit ér, amennyit MÉR. Új hívási alak (új annotáció, új wrapper, új
esemény-út) → a mérőt bővíteni KELL, különben csendben vakká válik, miközben
„minden rendben"-t ír ki.

### 1.8 Az „ELLENŐRIZENDŐ" halmaz nem mérés, hanem HALASZTÁS
Ha egy ellenőrző kockázatot jelez, de a DÖNTÉST emberre bízza („126 elem
átnézendő"), a döntés el fog maradni, a zöld pipa pedig hamis biztonságot ad.
→ **Fordítsd meg a bizonyítási terhet:** allowlist INDOKLÁSSAL; ami nincs rajta,
az HIBA, `fájl:sor`-ral.

---

## 2. A premisszákról

### 2.1 A saját indoklásod premisszáját ugyanúgy igazold kódból, mint a leletet
Több körön át építettem hamis indoklásra („a támadó ezt nem tudja hamisítani",
„az áradat csak X típusú sort tud előállítani") — és a rájuk épített javítás
ROSSZABB lett a megelőzőnél. **Egy teherhordó komment tévedése ugyanolyan hiba,
mint a kódé: a következő kör abból dolgozik.**

### 2.2 A KOMMENT NEM BIZONYÍTÉK
A kód önmagában sosem igazolja a SZÁNDÉKOT: egy szándékos biztosíték és egy
félbehagyott bekötés azonosan néz ki. De a komment sem: kimérten volt olyan
kommentem, ami azt állította, hogy „ezt a tokent csak hitelesített staff kapja" —
miközben a hitelesítetlen végpont is kiadta.

**Mielőtt LELETKÉNT jelentesz valamit — és különösen mielőtt DÖNTÉST kérsz —,
ellenőrizd, hogy a viselkedés nem DOKUMENTÁLT, SZÁNDÉKOS döntés-e.** A hiba nem a
tévedés, hanem hogy döntést kérsz ellenőrizetlen premisszára: a hibás premissza így
a FELHASZNÁLÓ döntésébe csatornázódik.

Jelentés-forma, ha a viselkedés szándékos:
> „ez szándékos (forrás: `fájl:sor`), a körülötte lévő X viszont valódi hiány"

### 2.3 Az ügynökök/alvállalkozók leleteinek a PREMISSZÁJÁT is ellenőrizd
Egy ügynök javaslata épülhet nem létező mezőre, elavult API-ra vagy félreértett
adatfolyamra. Ráépítve néma no-op lesz. Ne vedd készpénznek a leletet, és főleg ne
az indoklását.

### 2.4 A DOKSI-DRIFT döntési premissza-hiba
Egy elavult „ez még nyitva van" / „ez blokkolt" bekezdés a következő kört egy nem
létező hátralék hajszolására küldi. Legyen EGY igazságforrás, a többi csak MUTATÓ
— és a mutató mondja ki, hogy mutató.

---

## 3. Példány helyett OSZTÁLY

### 3.1 Ha egy hibát megtaláltál, keresd meg a TESTVÉREIT
Determinisztikus grep/szkenner-sweep az egész kódbázison a hibaosztályra — nem
példányonként, hanem osztályonként EGYBEN. Egy loop-alapú keresés a testvéreket
körökön át adagolja; a sweep egyben zárja.

### 3.2 Ha egy fájlban KÉT precedens van ugyanarra, a JAVÍTOTTAT másold
Grep-elj a hibaosztály kommentjére, ne a legközelebbi kódra. Több körön át a
leletek TÖBBSÉGE az ELŐZŐ KÖR SAJÁT JAVÍTÁSAIBAN volt — a friss javítás a
legkockázatosabb kód, nem a régi.

### 3.3 A felmentést SORRA add, ne FÁJLRA
Az „ez a fájl rendben van" indoklás egy MÁSIK sorra volt igaz; a veszélyes alak
ugyanabban a fájlban túlélt.

### 3.4 Ha egy körben lefektetsz egy precedenst, a kör VÉGÉN nézd meg:
- a testvérek követik-e,
- mely korábbi INDOKLÁSOK haltak meg tőle.

> Konkrét eset: bevezettem, hogy a kikapcsolt takarító `skipped`-et írjon, ne `ok`-ot.
> Ugyanabban a hullámban egy másik takarító `ok`-ot írt olyasmire, ami 100%-ban
> elmaradt — szemben a saját, aznapi precedensemmel.

### 3.5 Ha egy képességnek TÖBB belépési pontja van, KÖZÖS helper döntsön
Különben a kapuk szétcsúsznak. Kimért eset: egy jogosultsági kapu két végponton,
csak az egyik kapuzva — és a lelet is csak az egyiket vizsgálta.

---

## 4. MÉRJ, ne érvelj

- **Teljesítmény-, memória- és versenyhelyzet-állítás CSAK méréssel.** „Ez lassú
  lehet" nem lelet; „348 kB bemenet → 3327 ms blokkolt CPU, 830 MB RSS" az.
- **A versenyhelyzetet VEGYES, PÁRHUZAMOS terhelés alatt mérd.** Egy „18/18 tiszta
  futás" állításom nem volt reprodukálható: vegyes párhuzamos terhelésen 1/9 bukás.
- **Terhelés alatt is futtasd a suite-ot.** Két ingadozó teszt (ütköző temp-fájlnév,
  egy ablakon mért kétirányú rate-limit) csak párhuzamos futtatással jött elő.
- **A javítás UTÁN is mérj.** A „javítottam" állítás bizonyítéka az ELŐTTE/UTÁNA
  szám, nem az, hogy a diff jól néz ki.
- **A kockázatbecslés is lehet hibás — bizonyíték nélkül ne vonj vissza javítást.**
  Egyszer „nem igazolható API + futásidejű összeomlás" indokkal visszavontam egy
  helyes javítást; MINDKÉT feltevés téves volt, és a visszavonás ára valós.

---

## 5. A NÉMA KUDARC osztálya

**A rendszer olyankor hazudik, amikor JÓL néz ki.** Ne csak hibát keress — keress
olyan SIKERT, amit semmi nem bizonyít.

- **Ami elmaradt vagy elromlott, azt NE jelentsd elvégzettnek.** Külön számláló és
  külön állapot annak, ami nem volt elvégezhető (`skipped` / `unreachable`), nem
  `ok`. A kikapcsolt komponens `skipped`-et írjon, ne hagyja bent az utolsó éles
  futás `ok`-ját (a rácson hetekig stale siker látszik).
- **A KUDARC OKÁT el kell juttatni a HÍVÓIG.** Egy „mindenre `null`" visszatérés a
  hívónál egyetlen, félrevezető üzenetté olvad: a titok-rotáció, a leállt szolgáltatás
  és a valóban törölt erőforrás megkülönböztethetetlen lesz. Gépi kód + a valódi ok
  megnevezése.
- **A JELZÉS HIÁNYA nem bizonyíték a sikerre.** Ha egy „elvégeztem" jelzőt csak EGY
  kódút állítja elő, akkor összeomlás/áramszünet esetén a hiánya sikernek olvasódik.
  → **POZITÍV bizonyíték** kell (a ténylegesen futó artefakt verziója, nem a várt).
- **A „ne csináljunk semmit" is lehet a ROSSZABB választás.** Egy érintetlenül
  hagyott sor HARMADIK, soha nem záruló állapotot csinálhat, ami egyetlen takarító
  kapuját sem éri el — és a benne lévő titok korlátlan ideig ott marad minden
  dumpban. Ha a művelet bizonyítottan lehetetlen, zárd le TERMINÁLISAN, indoklással.
- **Néma csonkolás.** Fix limit + nincs lapozó + a `total`-t senki nem olvassa =
  „nincs több" látszat. Írd ki, hány elem látszik hányból.
- **Ha egy vészfék bont, tegye SZABÁLYOSAN.** Egy nyers `socket.destroy()` RST-t
  küld, ami a peernél a MÁR MEGÉRKEZETT választ is eldobathatja → a hívó határidő
  nélkül lóg vagy értelmezhetetlen hibát kap. Graceful zárás + szabályos hibaválasz.
- **A felület ne kínáljon olyat, ami nem működik.** Írás-only kapcsoló, 404-et adó
  „Futtatás most" gomb, olyan mező, amit a mentés eldob — mind ugyanaz az osztály.

---

## 6. VARRATOK (modulok, szolgáltatások, repók között)

**A varraton a hiba nem a kódban van, hanem a KÖZÖTTÜK lévő feltevésben.** Az egyik
oldal küld valamit (mezőt, gépi kódot, figyelmeztetést), a másik eldobja — és a
rendszer közben ZÖLDET mutat.

- **Ne a hívást nézd, hanem hogy a VÁLASZ MINDEN ÁGA eljut-e a döntéshozóig.**
- **EXPLICIT felsorolás vs. AUTOMATIKUS szerializáció → néma szétcsúszás.** Ha egy
  DTO-t az egyik ág `serialize(obj)`-ként küld, a másik pedig mezőnként felsorolva,
  akkor minden ÚJ mező addig hiányzik a felsoroló ágból, amíg valaki oda is beírja —
  és a fordító SOHA nem jelzi, mert a hívó-oldali kód hibátlan.
  → **paritás-őr KÖTELEZŐ.**
- **Egy drót-formátumnak EGY írója és EGY olvasója legyen.** Ha kettő van, mérd a
  paritásukat automatán — semmilyen típus- vagy fordítási szabály nem köti össze őket,
  és egyik repó tesztjei sem látják a másikat. → **kereszt-repós szkenner.**
- **Ha egy szótárat (ok-kód, státusz, esemény-név) TÖBB fogyasztó olvas, és
  mindegyiknek van `default` ága, akkor a „van-e ág" mérce VACUOUS.** A mérce az
  legyen, hogy az AZONOS JELENTÉSŰ értékek AZONOS ágra jussanak — szemantikai
  családok szerint.
- **Timeout MINDEN kereszt-szolgáltatás hívásra.** Egy beragadt peer különben a
  hívó handlerjét percekig fogva tartja (DoS-amplifikáció).
- **A javítás MINDKÉT oldala kell.** Ha az egyik fél nem küldi és a másik nem
  olvassa, bármelyik felét egyedül javítva a hiba megmarad — és „javítottnak"
  fog látszani.
- **A séma ne mondjon ellent a saját kapujának.** (Kimért eset: kötelezővé tett
  mező, amit egy legitim hívó-osztály elvileg nem tud megadni → az teljesen ki volt
  zárva.)

---

## 7. Adat-integritás, sorrend, konkurencia

- **Foglalj ELŐBB, hozz létre UTÁNA.** Ha az egyediség-megszorítás a mellékhatás
  UTÁN érvényesül, két párhuzamos kérés MINDKETTŐ végigmegy → duplikált
  mellékhatások, amikből a „vesztes" takarítása mindig hiányos.
- **Vak `where: {id}` állapot-írás CAS nélkül = elveszett frissítés.** Állapot-váltás
  mindig `where: {id, status: <kiolvasott>}` + 0 sor esetén 409.
- **Read-modify-write tömbön (`[...spread]`) konkurensen elveszti az egyik írást.**
  Használj atomikus append-et.
- **A destruktív takarító előtt nézd meg a rá mutató idegen kulcsokat és azok
  `ON DELETE` szabályát.** Egy `SET NULL` némán elveszi a védett rekordok
  hovatartozását.
- **Séma-változás: a MIGRÁCIÓ ELŐBB, utána az app.** Írd is le a commitban.
- **Ne abuzálj meglévő oszlopot jelölőnek.** Ha az adat nem az, aminek az oszlop neve
  mondja, a következő olvasó félre lesz vezetve — inkább új oszlop, indoklással.
- **A jelölőt CSAK a művelet SIKERE után írd ki.** Különben egy újrapróbálást
  elnyelsz, és a művelet SOHA nem történik meg.

---

## 8. Idő és lokalizáció (ha érintett)

- **Minden drótra menő és drótról jövő dátum `InvariantCulture` / explicit formátum.**
  A `:` több platformon IDŐELVÁLASZTÓ-HELYŐRZŐ, amit a gép területi beállítása
  lecserél; a 12 órás minta délutánt délelőttre ír. Mindkettő NÉMÁN hibázik.
- **Ha egy időzóna-hibát javítasz, az ÍRÁS és az OLVASÁS ugyanazon az órán legyen.**
  Sweepelj MINDKÉT irányra — a fél-javítás nem-alapértelmezett gépen halmozódó
  eltolást ad.
- **Ha egy szerződés KÉT, egymástól függetlenül elállítható kapcsolón nyugszik,
  legyen INDULÁSI ÁLLÍTÁS, ami hangosan szól.** A fél-teljesülés néma csúszást ad.
- **Naiv időbélyeg-oszlopba soha ne írj offszetes/`Z`-s alakot** — az adatbázis az
  offszetet eldobja, és a fali óra elcsúszik.
- **Megjelenített szöveg SOHA nem alkalmas állapot-felismerésre.** A nyelv alatta
  megváltozhat → a helykitöltő-egyezés vagy a felirat-összehasonlítás csendben
  hamissá válik. Használj EXPLICIT állapot-jelzőt / nem fordítható kulcsot (`Tag`).
- **Ami a szervernek megy, azt SOHA ne fordítsd — csak a megjelenítését.**
- **Fordított felirat MELLÉ soha ne tegyél fix méretet** (garantált levágódás más
  nyelven). És a levágódásnál szinte sosem az elem szélessége a szűk keresztmetszet,
  hanem a CELLA-KORLÁT.
- **Ha egy felirat MEZŐ-INICIALIZÁLÓBAN oldódik fel, BEFAGY** az akkori nyelven a
  folyamat teljes életére. Kifejezés-testű property kell.

---

## 9. HARNESS-higiénia (mutáció, ügynökök, munkamenetek)

- **A mutációs visszaállítás NE `git checkout --` legyen, ha az alapállapot NINCS
  commitolva** — az a SAJÁT, még nem commitolt javítást dobja el. (Velem megtörtént:
  elvesztettem egy kész javítást.) → **fájl-másolat** snapshot.
- **Egy MEGÖLT (timeoutolt) mutációs futás BENT HAGYJA a mutációt**, és a következő
  futás baseline-je már a romlott kódot méri. → A visszaállítást KÜLÖN igazold
  (`diff` + `git status`), ne feltételezd.
- **Mutációt futtató ügynököket NE engedj párhuzamosan ugyanarra a repóra.** Az egyik
  a másik futás közbeni szabotázsát látja, és valós leletként jelenti.
- **A 0-leletes automata futás SOHA nem tiszta bizonyítvány.** Nézd meg a naplót
  (hány ügynök zárult le, olvastak-e egyáltalán fájlt). Egy jogosultság- vagy
  keret-hiba miatt bukott futás „sikeresnek ÉS száraznak" látszik — a két tünet
  együtt tökéletesen álcázza magát. Indíts PRÓBA-ügynököt előbb.
- **Ha egy keret négyszer bukott, ne az ötödiket próbáld** — válts arra, ami
  bizonyítottan működik.

---

## 10. Munkamenet-folytonosság

- **MIELŐTT hosszú folyamatot indítasz, ellenőrizd, nincs-e FÉLBESZAKADT.** Ha van,
  kérdezd meg, azt folytassuk-e. Egy 30 másodperces ellenőrzés helyett feltevésre
  cselekedni drága: nálam ez egy folytatható, 133 részeredményt tartalmazó futás
  eldobásához és 7 felesleges párhuzamos ügynökhöz vezetett.
- **Vezess ÉLŐ folytatási horgonyt** (pl. `FOLYAMATBAN.md`): mi kész, mi a
  következő tétel `fájl:sor`-ral, mi igényel felhasználói döntést, és mi a
  folytatás pontos parancsa. Aki elindít, beírja; aki lezárja, kiveszi.
- **A részeredményt COMMITOLD ÉS PUSHOLD** — az ephemer környezet bármikor
  elmehet, és a távoli branch az egyetlen igazságforrás.
- **A horgony frissítése a MUNKA RÉSZE**, nem utómunka. Elavult horgony = §2.4.

---

## 11. Átvizsgálási körök módszertana

- **A kört ELSŐSORBAN az ELŐZŐ KÖR DIFFJÉRE célozd.** Nyolc körön át igazolódott:
  a leletek többsége a friss javításokban van, és azon belül is a friss ŐRÖKBEN.
- **Loop-until-dry**, nem „N kör": ismeretlen méretű halmaznál a fix számláló a
  farkat levágja. K egymást követő üres kör után állj meg.
- **Adverzariális verifikáció:** minden leletre 2+ FÜGGETLEN szkeptikus, akiknek a
  feladata a CÁFOLAT, nem a megerősítés. Bizonytalanságnál alapértelmezés: cáfolva.
- **Perspektíva-diverz verifikáció**, ha egy lelet többféleképp lehet hamis
  (helyesség / biztonság / teljesítmény / reprodukálható-e) — a sokféleség olyat
  fog, amit a redundancia nem.
- **Teljességi kritikus a kör végén:** „mi maradt ki — nem futtatott metszet,
  ellenőrizetlen állítás, el nem olvasott forrás?"
- **Ne legyen NÉMA plafon.** Ha a kör korlátoz (top-N, mintavétel, nincs retry),
  írd ki, mi esett ki — a csendes csonkolás „mindent lefedtünk"-ként olvasódik.
- **A negatív eredményt is írd le.** „Ezt megnéztem és tiszta" ugyanolyan értékes,
  mint a lelet — nélküle a következő kör újra végigcsinálja.

---

## 12. Kommunikáció és szállítás

- **Commit-üzenet: tárgyilagos, a „MIÉRT"-tel.** Mi volt a hiba, mi a
  következménye, mit mér a hozzá írt őr, és mivel hitelesítetted. Ne csak azt,
  hogy mit írtál át.
- **Ha a saját javításod vagy őröd hibás volt, azt is írd bele.** A következő kör
  ebből dolgozik.
- **Számot csak MÉRÉS után írj le.**
- **Ha egy scope-ot nem tudtál elvégezni, mondd ki explicit, mit hagytál ki és
  miért** — a leszűkítés a felhasználó döntése, nem a tiéd.
- **Külön kérdezz, ne feltételezz TERMÉK-döntésben.** Ami viselkedés-változás a
  végfelhasználónak, az nem mérnöki hatáskör.

### Többgépes / többszerveres környezet
**MINDEN parancsblokk fölött tüntesd fel, MELYIK gépen kell futtatni.**
(pl. `▶ APP-SZERVER (hostname)`). Több hoszt esetén a félreértés drága.

### Deploy-ablak
Ha az élesítés automata láncot indít, legyen **TILTOTT ABLAK** (pl. munkanap
munkaidő), és a push ELŐTT ellenőrizd a helyi időt. Ha a tiltott ablakban vagy:
ne pusholj, EMLÉKEZTESD a felhasználót a szabályra, és kérj időzítést.

### Szerzőség / attribúció (vidd át, ha ugyanaz a jogosult)
Ha a projektben tilos az AI-eszközre utalás: **semmilyen szerzőtárs-jelölés,
session-hivatkozás, „AI-generated" jelölés vagy modell-azonosító** nem kerülhet
kódba, kommentbe, doksiba, **commit-üzenetbe**, PR-leírásba vagy CI-konfigba.
Commit-üzenet záró trailer NÉLKÜL.

---

## 13. Jogszabályi megfelelés és JOGHATÓSÁG

### 13.0 Aktuális hatókör (Siduri)
**A termék első körben KIZÁRÓLAG a magyar piacra készül.** Amíg ez így van, a
megfelelési kötelezettség a magyar jog: NAV (nyugta/számla, adóügyi eszközök),
NTAK, számviteli megőrzés, GDPR. **Más ország szabályát MOST NE implementáld** —
találgatásból írt külföldi adólogika nem megfelelés, hanem karbantartandó holt kód.

**De a későbbi bővítéskor az új célország MINDEN szabályát be kell tartani** — nem
csak azokat, amiknek van magyar megfelelőjük. Egy másik joghatóság tipikusan olyan
kötelezettséget is támaszt, amire itt nincs analógia (kötelező fiskális aláírás,
eltérő bizonylat-tartalom, eltérő megőrzési idő, eltérő adatvédelmi lokalizáció).
A „nálunk ez nincs, tehát ott sincs" a §2.1 hibája: igazolatlan premissza.

### 13.1 A joghatóság-függő szabály ADATVEZÉRELT, nem beégetett
ÁFA-kulcsok és a hozzájuk tartozó besorolás, kerekítési szabály (5 Ft), bizonylat
kötelező tartalma, megőrzési idő, adóhatósági végpontok és sémák, pénznem és
formátum, adószám-validáció — **mind konfiguráció, nem konstans a kódban**.

**Miért:** a beégetett `0.05` / `5 Ft` / `HUF` nem EGY hiba, hanem egy HIBAOSZTÁLY
(§3.1), ami szétszóródik a kódbázis egészén, és bővítéskor sweepelni kell. A
bővítés akkor legyen „új konfiguráció + új implementáció egy ismert varraton",
ne „keressük meg, hol van 27 leírva".

### 13.2 Minden joghatóság-függő döntés EGY belépési ponton menjen át
§3.5 alkalmazása: ÁFA-megállapítás, kerekítés, bizonylat-összeállítás, adóügyi
eszköz-vezérlés, hatósági adatszolgáltatás — mindegyikhez EGY nevesített helper /
interfész. Ha két hívási út dönt ugyanarról, szét fognak csúszni, és a fordító
soha nem jelzi.

### 13.3 A jogszabály DÁTUMOZOTT — a szabály-tábla verziózott legyen
Az ÁFA-kulcs, a küszöbértékek és a sémák változnak, és **visszamenőleg NEM
alkalmazhatók**. A szabály-tábla sora `érvényes-tól` / `érvényes-ig` kulccsal áll,
és a bizonylat mindig az **eseménykori** szabállyal képződik.

**Miért:** egy régi nyugta újranyomtatása, sztornója vagy riportálása a MAI
kulccsal adóhiba. Ez a §5 néma kudarca: nem omlik össze, csak évek múlva egy
ellenőrzésen derül ki.

### 13.4 A megfelelési kudarc NÉMA — ezért ŐR kell rá
A hibás ÁFA, a kimaradt adatszolgáltatás és a hiányos bizonylat-tartalom mind
„sikeresen" fut le. Ezért:
- **szkenner** a beégetett joghatóság-literálokra (adókulcs-számok, kerekítési
  konstansok, pénznem-kódok, hatósági URL-ek) a konfigurációs rétegen KÍVÜL,
  §1.3 szerint PADLÓSAN és §1.8 szerint indoklásos allowlisttel;
- **arany-minta tesztek** valós bizonylat-esetekre (vegyes ÁFA + arányos
  kedvezmény + kerekítés + elviteles váltás), a jogszabályra hivatkozó indoklással;
- a hatósági adatszolgáltatás **pozitív visszaigazolása** legyen az elvégzettség
  bizonyítéka (§5), ne a hibajelzés hiánya.

### 13.5 A jogi állítás is PREMISSZA — hivatkozás nélkül nem használható
„Ez így kötelező" / „ezt nem szabad" **forrásmegjelölés nélkül nem építhető be**,
és főleg nem csatornázható a felhasználó döntésébe (§2.2). A jogszabályhelyet vagy
a hatósági dokumentációt nevezd meg a kódban/doksiban, a hatályosság dátumával.
Ha nem tudod igazolni, **mondd ki, hogy nem tudod** — az ellenőrizetlen jogi
premisszára épített javítás rosszabb a hiánynál.

### 13.6 Bővítéskor: országonkénti MEGFELELÉSI MÁTRIX, nem diff
Új célországnál ne azt kérdezd, „mi tér el a magyartól", hanem vedd végig az adott
ország teljes követelménylistáját. A diff-alapú megközelítés definíció szerint
vak arra, aminek itt nincs párja — pont arra, ami a legdrágább.

---

## 14. Gyors ellenőrzőlista (minden javításhoz)

- [ ] A hibát MÉRTEM (előtte/utána szám), nem érveltem.
- [ ] Megkerestem a TESTVÉREIT (osztály, nem példány).
- [ ] Ellenőriztem, hogy nem SZÁNDÉKOS viselkedés-e (forrás megnevezve).
- [ ] A saját INDOKLÁSOM premisszáját kódból igazoltam.
- [ ] Írtam őrt, ami a JELENSÉGET méri, nem proxyt.
- [ ] Az őr komment-mentesített forráson mér, és PADLÓS.
- [ ] Az őrt 4+ KÜLÖNBÖZŐ mutációval hitelesítettem, negatív kontrollal.
- [ ] Ahol az őr elvileg sem elég, azt KIMONDTAM a kommentben.
- [ ] Ellenőriztem, hogy a javításom nem tört-e meglévő szerződést.
- [ ] A varrat MINDKÉT oldalát javítottam (ha varrat).
- [ ] A teljes suite lefutott, és a VÉGÖSSZEG változása magyarázható.
- [ ] Ha joghatóság-függő: NEM égettem be szabályt, EGY belépési ponton megy át,
      és DÁTUMOZOTT (§13.1–13.3).
- [ ] Jogi állítást csak FORRÁSSAL írtam le, vagy kimondtam, hogy nem igazolt (§13.5).
- [ ] A folytatási horgony frissítve; a munka commitolva ÉS pusholva.
