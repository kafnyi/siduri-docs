# FOLYAMATBAN — élő folytatási horgony

> **Ez a belépési pont.** Ha új munkamenetet kezdesz a Siduri projekten, **ezt
> olvasd el először**, és csak utána bármi mást.
>
> MERNOKISAROKKOVEK §10: „Vezess ÉLŐ folytatási horgonyt: mi kész, mi a következő
> tétel `fájl:sor`-ral, mi igényel felhasználói döntést, és mi a folytatás pontos
> parancsa. Aki elindít, beírja; aki lezárja, kiveszi."
>
> **A horgony frissítése a MUNKA RÉSZE, nem utómunka** (§10). Elavult horgony = §2.4
> döntési premissza-hiba: a következő kört egy nem létező hátralék hajszolására küldi.

**Utolsó frissítés:** 2026-08-23 (3. munkamenet — módosítók, menü, DRS, pénz, audit napló, nyomtatás, **NTAK RMS specifikáció elsődleges forrásból**)
**Fázis:** tervezés. **KÓDOLÁS MÉG NEM KEZDŐDÖTT EL, és nem is szabad elkezdeni** —
lásd „Miért nem kódolunk még".

> **A `fájl:sor` hivatkozásokról:** a sorszámok a 2026-08-22-i állapotra érvényesek,
> és a `NYITOTT_KERDESEK.md` **minden szerkesztésekor elcsúsznak**. Ha nem stimmel,
> **keress a tétel azonosítójára** (pl. `A2/a`, `B1`, `F3`) — az azonosítók stabilak,
> a sorszámok nem. Aki szerkeszti a fájlt, **frissítse itt a sorszámokat is** (§10:
> a horgony frissítése a munka része).

---

## 0. Fájltérkép — melyik fájl mit ér

| Fájl | Szerep | Megbízhatóság |
|------|--------|---------------|
| **`NYITOTT_KERDESEK.md`** | **AZ EGY IGAZSÁGFORRÁS a döntésekre** (§2.4) | Kötelező érvényű |
| `MERNOKISAROKKOVEK.md` | Projekt-független mérnöki szabálygyűjtemény | Kötelezően alkalmazandó |
| `siduri_spec_hu.md` | Az eredeti rendszerterv (magyar) | **Részben ELAVULT** — inline `[MÓDOSÍTVA]` / `[NYITOTT]` jelölésekkel |
| `gemini_cloud_spec_en.md` | A Gemini felhő-specifikációja — **bemeneti dokumentum**, a munkamenet ELŐTTI állapot | **Csak a fájl végén lévő ÖSSZEVETÉSSEL együtt használható** — egy pontja felülírva, egy biztonsági aggály |
| `siduri_superprompt_en.md` | Ugyanaz megaprompt formában (angol, Geminihez) | **Részben ELAVULT** — inline `[SUPERSEDED]` / `[OPEN]` jelölésekkel |
| `FOLYAMATBAN.md` | Ez a fájl — állapot és folytatás | Élő |
| **`MVP_DEFINICIO.md`** | **Mit jelent az „MVP"** ebben a projektben + az öt címke (`ALAP`/`MVP`/`v1`/`v2`/`VÍZIÓ`) | **Kötelező érvényű** — ha bárhol „MVP" szerepel, ezt kell alatta érteni |
| **`ELLENORZES_2_ADVERZARIALIS.md`** | **A 2. ellenőrző kör** — szkeptikus átvizsgálás; a feladat a CÁFOLAT volt | Élő; **hat teendő, egy súlyos strukturális lelet** |
| **`FISKALIS_UZEMMODOK.md`** | A három fiskális üzemmód + az e-pénztárgépes integráció utánajárása | Élő; **hat kérdés a NAV/gyártó felé** |
| **`ELLENORZES_1_TELJESSEG_JOGI.md`** | **Az 1. ellenőrző kör jelentése** — jogi megfelelés forrásokkal + teljességi vizsgálat | Élő; **négy lelet DÖNTÉST igényel** |
| **`MERESEK.md`** | **A mérendő tételek egységes nyilvántartása.** A felhasználó kiemelt utasítása: az első éles tesztnél MINDENT meg kell mérni | Élő — kötelezően frissítendő |
| `UiUX/` (mappa) | UI/UX skill-készlet (7 skill, köztük WPF és Flutter stack-adatok) | Eszköz, a design-fázisban használandó — lásd 0.2 |

**Ha a `siduri_spec_hu.md` / `siduri_superprompt_en.md` ellentmond a
`NYITOTT_KERDESEK.md`-nek, a `NYITOTT_KERDESEK.md` nyer.** A két spec fejlécében ez
ki van írva, és a felülírt bekezdések inline meg vannak jelölve.

---

## 0.1 A FELHASZNÁLÓVAL VALÓ KOMMUNIKÁCIÓ SZABÁLYAI — kötelező

Ezek a felhasználó explicit kérései. Nem stílus, hanem működési követelmény: ha
megszegjük, a felhasználó **nem tud dönteni**, és a döntés vagy elmarad, vagy
félreértésen alapul (§2.2: a hibás premissza a felhasználó döntésébe csatornázódik).

1. **SOHA ne hivatkozz csupasz tételazonosítóval** (`A2`, `B1`, `F3`, `§13.2`…)
   a felhasználónak írt szövegben. A felhasználó **nem tudja fejből**, mit
   jelentenek. **Mindig írd ki, MIRŐL SZÓL**, és az azonosító legfeljebb zárójeles
   utalás legyen utána.
   - ROSSZ: „az A2 miatt a B1 tétje átrendeződött”
   - JÓ: „mivel a pénztárgép a szerver nélkül is tud eladni (ez volt a korábbi
     döntés), a vészhelyzeti szerver kérdésének a tétje átrendeződött”
   - **A dokumentumokra ez NEM vonatkozik** — ott az azonosítók a horgonyok, és a
     §2.4 (egy igazságforrás) miatt kellenek. A szabály a **beszélgetésre** él.
     Ezért van mostantól minden döntéstáblában egy „Miről szól” oszlop is.

2. **Ha egy kérdés nem érthető, a felhasználó szólni fog — ilyenkor fejtsd ki
   bővebben, ne ismételd meg ugyanúgy.** Volt rá példa: egy ütemezési kérdés
   csupa azonosítóval volt feltéve, és emiatt megválaszolhatatlan volt.

3. **Döntéskéréskor mindig legyen ott, mi az ÁRA a választásnak** — ne csak a
   lehetőségek nevei. A felhasználó a következményre szavaz, nem a címkére.

4. **A dokumentáció és a beszélgetés nyelve magyar.** Formai megkötés nincs.

5. **`[!]` NE FINOMKODJ. A tények kimondása mindig előrébb való a kényelemnél.**
   A felhasználó explicit utasítása (2026-08-22), a 2. ellenőrző kör után:

   > *„nem probléma, ha fájó pontok kerültek elő, mert pontosan ez a lényege…
   > hogy most derüljenek ki a hibák és hiányosságok, amikor még »olcsón«
   > javíthatóak… Egy összeadás is akkor ad pontos, tiszta végeredményt, ha az
   > összeadandó számok ismertek! Többet árt egy kényelemből vagy kedvességből
   > elhallgatott infó, mint a kegyetlen valóság, mert míg utóbbira lehet
   > készülni és tenni ellene, az előbbi egyszer csak váratlanul megbosszulhatja
   > magát."*

   **Mit jelent ez a gyakorlatban:**
   - **Rossz hírt NEM tompítunk**, és nem temetünk jó hírek közé.
   - **Ha egy döntés nem bírja el a saját súlyát, azt ki kell mondani**, akkor is,
     ha a felhasználó hozta.
   - **A saját tévedéseimet ugyanolyan élesen jelentem**, mint a másokét (§12).
   - **A bizonytalanságot nem kerekítjük bizonyossággá** — `[?]` marad `[?]`.
   - **Ami nincs kész, az nincs kész** — nem „nagyrészt kész" (§5).

   **Ez nem stílus, hanem a MERNOKISAROKKOVEK működési feltétele:** a §2.2
   (ne csatornázz ellenőrizetlen premisszát a felhasználó döntésébe), a §5
   (a néma kudarc a legveszélyesebb hibaosztály) és a §12 (mondd ki, mit
   hagytál ki és miért) **mind erre épül.** Egy elhallgatott lelet ugyanolyan
   néma kudarc, mint egy hamis zöld pipa.

---

## 0.2 UI/UX skill-készlet — MEGVAN, a design-fázisban KÖTELEZŐEN használandó

**A felhasználó 2026-08-22-én feltöltötte** a `UiUX/` mappát a `siduri-docs` repóba
(master commit `e6d26a2`, a munkabranchre merge-elve). Explicit kérése:
**„majd kérlek használd, amikor design tervezéshez jutunk."**

**Hol van:** `siduri-docs/UiUX/.claude/skills/` — hét skill:
`ui-ux-pro-max` (a fő, adatvezérelt design-intelligencia), `design-system`,
`ui-styling`, `design`, `brand`, `banner-design`, `slides`.

**Miért közvetlenül releváns — ellenőrizve, nem feltételezve:** a
`ui-ux-pro-max/data/stacks/` mappában van **`wpf.csv`** ÉS **`flutter.csv`** —
pontosan a projekt két kliens-stackje (WPF asztali pénztárgép, Flutter mobil
kliensek). A `wpf.csv` 57 soros, hivatkozott (Microsoft Learn URL-ekkel) és
dátumozott (`Verified At: 2026-08-13`) irányelvlista, súlyossági szinttel.
Van `avalonia.csv` is, de azt az A1 döntés (WPF marad) szerint nem használjuk.

**FIGYELEM — ezek MOST NEM aktív skillek a munkamenetben.** A `.claude/skills/`
mappa a `UiUX/` alatt van, nem egy repó gyökerében, ezért a Claude Code nem
tölti be automatikusan. **A design-fázis kezdetekor ezt rendezni kell:** vagy át
kell másolni/linkelni a megfelelő repó gyökerébe (`siduri-pos-client/.claude/skills/`,
`siduri-flutter-clients/.claude/skills/`), vagy közvetlenül adatként kell olvasni
a CSV-ket. **Ez egy elvégzendő tétel, nem automatikus.**

**Ütemezés:** a design-fázis a fázistervben (E1) fog helyet kapni. Addig ez a
szakasz az emlékeztető, hogy megvan és hogy KÖTELEZŐ elővenni — §2.4 szerint
enélkül a következő kör nulláról találná ki a design-irányelveket, miközben itt
egy dátumozott, hivatkozott készlet fekszik használatlanul.

---

## 1. Mi KÉSZ

**Hatvanhat döntés lezárva** (öt az 1., negyven a 2., huszonegy a 3. munkamenetben).
**Mindegyik indoklással együtt** olvasandó — indoklás nélkül a döntések nem tapadnak
meg, és a következő kör újratárgyalja őket.

| Tétel | Miről szól | Döntés | Hol (`fájl:sor`) |
|-------|-----------|--------|------------------|
| **A1** | POS kliens platformja | WPF marad; **Windows 10 IoT Enterprise (LTSC) only**, Linux törölve | `NYITOTT_KERDESEK.md:25` |
| **A2** | A pénztárgép önállósága | **Szerver-autoritatív + degradált gyorseladás.** Cache + helyi, csak-hozzáfűzhető napló, **nem** PostgreSQL replika | `NYITOTT_KERDESEK.md:43` |
| **A2/a** | Nyitott asztalok kettős kieséskor | **Nem elérhetők** → a pincér kézzel, gyorseladásként üti fel újra | `NYITOTT_KERDESEK.md:80` |
| **A2/b** | *(ÚJ, 2. munkamenet)* A degradált mód ütemezése | **Mindhárom rész az MVP-ben**: helyi napló + degradált felület + visszatéréskori egyeztetés | `NYITOTT_KERDESEK.md:112` |
| **B1/a** | *(ÚJ, 2. munkamenet)* Vészhelyzeti szerver / HA scope | **BENNE MARAD az MVP-ben** — az ajánlással szemben, tudatosan | `NYITOTT_KERDESEK.md:228` |
| **B1/b** | *(ÚJ, 2. munkamenet)* A tartalék gép és a replikáció | A tartalék **szintén J1900**, dedikált. Munkafeltevés: **aszinkron** replikáció (a „szinkron kizárt" **még nincs mérve**). Az „automatikusan szinkronról aszinkronra váltó" ág **elvetve** | `NYITOTT_KERDESEK.md:253` |
| **B1/c** | *(ÚJ, 2. munkamenet)* Ki kapcsol át a tartalékra | **Kétlépcsős: a gép ellenőriz, az ember dönt.** Azonnali, látványos csökkentett-mód jelzés, ami megmondja mit ellenőrizzenek; átkapcsolás felajánlása csak 5 perc után; a gombot EMBER nyomja; és a gépnek fel kell ismernie, ha Ő esett ki a hálózatról | `NYITOTT_KERDESEK.md:281` |
| **A4** | *(ÚJ)* Ki állítja vissza a fő szervert | **AUTOMATIKUS**, ha a fő és a tartalék 1 percig stabilan látják egymást és beszélnek is. A régi „csak szuperfiókkal" szabály ELVETVE. **De:** az árva tranzakciók kimentése automatikus és kötelező, a KÖNYVELÉSÜK nem lehet automatikus | `NYITOTT_KERDESEK.md`, keress: `A4 — failback` |
| **A4/a** | *(ÚJ)* Átvételi útvonalak | **Tiszta vs. kemény átvétel külön útvonal.** Ha a régi fő él és a tartalék eléri, a tartalék az átvétel ELŐTT leszívja a nem replikált tranzakciókat → tényleg nulla veszteség | `NYITOTT_KERDESEK.md`, keress: `A4/a` |
| **B1/c K1** | *(ÚJ)* Mikor megy csökkentett módba egy gép | **Önállóan, azonnal**, ha nem éri el a szervert — akkor is, ha a többi gép működik. Gépenkénti állapot, nem a helyé | `NYITOTT_KERDESEK.md`, keress: `K1 —` |
| **A4/b** | *(ÚJ)* Billegés-védelem | **Növekvő várakozás** minden automatikus visszaállás után + **leállási határ**, ami után az automatika kikapcsol és hangosan szól | `NYITOTT_KERDESEK.md`, keress: `A4/b` |
| **A4/c** | *(ÚJ)* Mikor cseréljen szerepet | **Azonnal, ahogy stabil** — nincs csendes ablakra halasztás. A csúcsidő-terhelést a billegés-védelem zárja ki | `NYITOTT_KERDESEK.md`, keress: `A4/c` |
| **Fiskális módok** | *(ÚJ)* Hány üzemmód van | **Három:** belső rendszer / online pénztárgép / e-pénztárgép. Az 1. módban a papírt **„NEM ADÓÜGYI BIZONYLAT"** jelöléssel kell ellátni | `FISKALIS_UZEMMODOK.md` |
| **F4** | *(ÚJ)* A nap-fogalmak | **MUNKANAP** = a hely egészéé, max 25 óra (23:30 figyelmeztetés, 25 óra kényszerleállás), nem naptári nap. **MŰSZAK** = eszközönkénti, az adóügyi munkanap. ~~**NTAK tárgynap** = naptári nap~~ → **[H1: TÉVEDÉS volt, a tárgynap a NYITÁS dátumából származik]**; **[H2: a 25 órás határ ÜTKÖZIK az NTAK 24 órás kemény validációjával]** | `NYITOTT_KERDESEK.md`, keress: `H1 —` |
| **C3/a,b** | *(ÚJ)* ÁFA és NTAK a terméken | **Két adókulcs kötelezően kitöltve**, az azonosság **jelölőként** tárolva. Az NTAK-kategória **feltételesen** kötelező (van-e kulcs) | `NYITOTT_KERDESEK.md`, keress: `C3/a` |
| **C2/a,b** | *(ÚJ)* Ár-történet és termék-életciklus | A bizonylat az **eladáskori** árat, adót ÉS nevet tárolja. Három állapot: aktív / inaktív / **soft delete** — de egyik sem rejti el a **történetből** | `NYITOTT_KERDESEK.md`, keress: `C2/a` |
| **A3** | *(ÚJ)* Purge és megőrzés | **A felhő a jogi archívum** (8 év). A „tisztán lokális" topológia így önmagában nem elegendő | `NYITOTT_KERDESEK.md`, keress: `A3 — purge` |
| **B17** | *(ÚJ)* A felhő rendelkezésre állása | **Két fizikai szerver**, fő + másodlagos, automatikus átcsatornázással. **A telephelyi kézi megoldás indoklása NEM vihető át** — a felhőben mi uraljuk az infrastruktúrát | `NYITOTT_KERDESEK.md`, keress: `B17` |
| **F7/a** | *(ÚJ)* Jogosultsági szintek | **Az ügyfél maga is létrehozhat/módosíthat szinteket** (pl. „Pultfőnök"), nem csak egyedi kivételeket. Frissítéskor érkező ÚJ jogosultság a meglévő szinteken **alapból tiltott**, de feltűnő jelzéssel | `NYITOTT_KERDESEK.md`, keress: `F7/a` |
| **F7/b** | *(ÚJ)* A Siduri admin fiók | **Sérthetetlen** (az ügyfél nem módosíthatja, nem csökkentheti, nem írja át a jelszavát) + **fix offline belépés** kell. Javaslat: **telephelyenkénti** hitelesítő adattal, látható audittal | `NYITOTT_KERDESEK.md`, keress: `F7/b` |
| **B16.12** | *(ÚJ)* Egy admin felület vagy kettő | **EGY webes admin alkalmazás, KÉT helyről kiszolgálva** (felhő + a telephely saját szervere offline-ra). A felhő raktár/receptúra ugyanaz, mint a telephelyi. **Ez a §6 néma szétcsúszást a gyökerénél szünteti meg** | `NYITOTT_KERDESEK.md`, keress: `B16.12` |
| **B16.10** | *(ÚJ)* Leltár | Az **egyetlen jogos** készlet-„felülírás" — de **korrekciós mozgásként**, hogy az eltérés kimutatható maradjon. **Fordulónapi elszámolás**, nem a rögzítés időpontjához | `NYITOTT_KERDESEK.md`, keress: `B16.10` |
| **B16.11** | *(ÚJ)* Több telephely | **Alapmodell, nem franchise-funkció.** Minden kimutatás működjön egy üzletre, több kiválasztottra és a teljes csoportra | `NYITOTT_KERDESEK.md`, keress: `B16.11` |
| **B16.1** | *(ÚJ)* Mi a felhő szerepe | **Teljes menedzsment-platform**, nem kiegészítő: beállítás-paritás a POS-szal, raktár, alapanyag-mozgás, receptúrázás, statisztikák; **zárolható beállítások** (ár, láthatóság); **üzletlánc/franchise szintű központi értékek**; visszajelzés a leérkezésről; eszköz-láthatóság. **A legnagyobb scope-változás — önálló terméksáv a fázistervben** | `NYITOTT_KERDESEK.md`, keress: `B16` |
| **B14.4** | *(ÚJ)* A bizonylatszám formátuma | **`xxxxxxyyyzzzzz`** = üzleti nap dátuma (a szervertől) + eszközszám + napi folyószám. Pl. `26082200300347`. **Naponta újraindul → soha nem fogy el**, és a dátum-előtag miatt szám szerint időrendben áll. **Kikötés: az `xxxxxx` az ÜZLETI NAP, nem a naptári nap** | `NYITOTT_KERDESEK.md`, keress: `B14.4` |
| **B14 M2** | *(ÚJ)* Klónozás elleni védelem | A szerver adja ki az azonosítót és regisztráció nélkül nincs bizonylat — **de a klónt ez nem fogja meg.** Hiányzó darab: **hardveres ujjlenyomat + forgó hitelesítő adat**; két ujjlenyomat egy azonosítón → **mindkettő tiltva**, amíg ember fel nem oldja | `NYITOTT_KERDESEK.md`, keress: `M2 — az eszközazonosító` |
| **B14 M4** | *(ÚJ)* Előzmény visszakérése | A kliens **lekérheti a saját előzményét** a szervertől → gépcsere után az új gép feltölti magát. Három kikötéssel (hiányos lehet, hitelesítés+audit, explicit gépcsere) | `NYITOTT_KERDESEK.md`, keress: `M4 —` |
| **B15 hatóköre** | *(ÚJ)* Mit tud a telefon v1-ben | **Nem fizettet és nem ad nyugtát** — csak rendelést vesz fel és menedzsel. Később bővítendő; az előkészítés majdnem ingyen van, egyetlen kikötéssel: **az eszközszám-tér legyen KÖZÖS minden eszköztípusra** | `NYITOTT_KERDESEK.md`, keress: `B15` |
| **B14** | *(ÚJ)* Bizonylat-számozás | **Kétrétegű.** (1) SIDURI szám: minden kiállító eszköz **saját, elhatárolt tartományból** számoz → az ütközés szerkezetileg lehetetlen, nulla koordináció, és a tartalék átvételkor azonnal kiszolgálhat. (2) ADÓÜGYI szám: tároljuk a sztornóhoz, de nem lehet a mi azonosítónk — és **nullázható**, mert nem minden bizonylatnak van | `NYITOTT_KERDESEK.md`, keress: `B14` |
| **B15** | *(ÚJ)* Vékonykliens-archívum | **Igen, de minimális** — csak amit ő küldött, rövidebb megőrzéssel, adatvédelmi okból (a telefon a leggyakrabban elveszített eszköz) | `NYITOTT_KERDESEK.md`, keress: `B15` |
| **B13** | *(ÚJ)* Átvétel előtti begyűjtés | **Elfogadva, módosítva.** A B14 miatt már nem kell az első bizonylat előtt lefutnia → a tartalék azonnal kiszolgál, a begyűjtés párhuzamosan fut. Célja adat-teljesség és ellenőrzés | `NYITOTT_KERDESEK.md`, keress: `B13` |
| **B12** | *(ÚJ)* Kockázatvállalási nyilatkozat | **Alkalmazásban elérhető űrlap, érintőképernyős aláírással**, elmentve ÉS a fő felhőszerverre továbbítva, visszakereshetően, időbélyeggel, védve. A terv négy dolgot tesz hozzá: a szöveg verzióját is menteni kell; két időbélyeg, a mérvadó a felhőé; offline útvonal kell; és konfiguráció-változáskor ÚJ nyilatkozat | `NYITOTT_KERDESEK.md`, keress: `B12` |
| **TPM** | *(ÚJ)* Van-e a bázison | **MINDKÉT ágra készülünk** — a titkosítás konfigurációs képesség, és az admin felület kiírja, melyik ágon vagyunk. Az ellenőrzés a felhasználónál folyamatban | `NYITOTT_KERDESEK.md`, keress: `MINDKÉT ÁGRA készülünk` |
| **B9 jellege** | *(ÚJ)* Kikényszerített-e a méret-lépcső | **Nem — ÉRTÉKESÍTÉSI AJÁNLÁS.** Ha kellene tartalék de nincs hova tenni, dedikált szervergépet ajánlunk (az nem POS, így egyetlen Windows POS is elláthatja a tartalék szerepet). Ha az ügyfél a kockázat ismeretében elutasítja, elfogadjuk. **A szoftver semmilyen konfigurációt nem utasíthat el** | `NYITOTT_KERDESEK.md`, keress: `A lépcső AJÁNLÁS` |
| **Szerepkiosztás** | *(ÚJ)* Melyik gép viheti a szerver-szerepet | **A tartalék MINDIG Windows POS vastagkliensen van, SOHA nem dedikált gépen.** A fő szerver jellemzően szintén POS-on; aki megengedheti, annál lehet dedikált. **Vékonykliens, KDS, rendeléskijelző egyiket sem viheti** | `NYITOTT_KERDESEK.md`, keress: `A „dedikált" szó pontosítása` |
| **B10/a** | *(ÚJ)* Adatvédelem a kliens-archívumban | **A szerver jellemzően egy dolgozó pénztárgép lesz**, nem irodai gép → a teljes adatbázis a pultban áll. A fizikai lopás ellen szoftverrel nem lehet teljesen védekezni — ezt ki kell mondani. Ellenszer: **adatminimalizálás** (tervezési szabály), lemeztitkosítás ha van TPM, fizikai rögzítés, és a felhőmentés mint egyetlen helyreállítási út lopás után | `NYITOTT_KERDESEK.md`, keress: `B10/a` |
| **B10/b** | *(ÚJ)* Kliens-archívum megőrzési ideje | **20 FORGALMAS üzleti nap**, nem 20 naptári nap — egy zárva töltött nap nem számít bele és nem öregít ki semmit. A licenc 10 napos türelmi idejével szándékosan nem közös érték. Nyugtázatlan adatot a megőrzés soha nem töröl | `NYITOTT_KERDESEK.md`, keress: `B10/b` |
| **B9/b** | *(ÚJ)* Mikor kötelező a tartalék szerver | **1 gép:** nincs. **2–3 gép:** opcionális. **4+ gép:** kötelező. Következmény: a „nincs tartalék szerver" elsőrangú konfiguráció, nem hibaállapot | `NYITOTT_KERDESEK.md`, keress: `B9/b` |
| **B9/a** | *(ÚJ)* Egygépes telepítés | **A pénztárgép MAGA a szerver.** Ezzel eldőlt a korábban nyitott kérdés is: igen, futhat egy gépen szerver ÉS kliens — támogatott konfiguráció | `NYITOTT_KERDESEK.md`, keress: `B9` |
| **Üzenetek** | *(ÚJ)* Személyzeti hibaüzenetek | **Három üzenet jóváhagyva** („hálózat", nem „internet"), plusz külön jelzés az internet hiányára | `NYITOTT_KERDESEK.md`, keress: `A személyzetnek szóló üzenetek` |
| **B3** | Minimum célhardver | J1900 **vegyes bázis** (szerver ÉS kliens) → **GraalVM kényszer marad**, plusz szoros WPF perf-költségvetés | `NYITOTT_KERDESEK.md:374` |
| **E2** | Ki fejleszti | 2–3 fős csapat + AI → **B8 (API-szerződés) az első hét tétele**, nem opcionális | `NYITOTT_KERDESEK.md:612` |

| **G0** | *(ÚJ, 3. munkamenet)* A gyártói AEE protokolldokumentum | **JOGI KORLÁT.** Szerzői jogi nyilatkozattal védett, partneri megállapodás NINCS. **A tartalma semmilyen formában nem kerülhet a dokumentációba** — csak absztrakt leírás. Külön kockázat: nincs támogatási szerződés és nincs tesztkészülék → **a fiskális mérföldkő fizikai készülék nélkül nem zárható le** | `NYITOTT_KERDESEK.md`, keress: `G0` |
| **G1** | *(ÚJ)* A gyűjtőkiosztás 8 fix rekesze | **Kemény korlát.** Áfakulcs-készlet: 5 / 18 / 27 / TAM / AJT, más nem küldhető → **validáció a terméktörzs mentésénél**. **A szervizdíjnak saját, áfakulcsonkénti gyűjtői vannak** → nem olvasztható a termék tételébe *(a korábbi terv itt hibás volt)*. Szabad rekesz **nincs** | `NYITOTT_KERDESEK.md`, keress: `G1 —` |
| **G2.1** | *(ÚJ)* FreeLimit | A darabszám mellé **külön beállítás, MELYIK elemek ingyenesek**: **legdrágább / legolcsóbb / legelső**, akár termékenként. **Alapértelmezés: LEGELSŐ** | `NYITOTT_KERDESEK.md`, keress: `G2.1` |
| **G2.2** | *(ÚJ)* Módosító vs. receptúra | **Az alapállapot a RECEPTÚRA.** A módosító **mindig eltérés** → **mindig nyomtatjuk és mindig kimegy a KDS-re**, kivétel nincs. Ezzel megszűnik az „alapállapot vs. eltérés" nyomtatási logika. A levonó módosító **anyagra hivatkozik**, és be tud nyúlni a szülőtermék receptjébe | `NYITOTT_KERDESEK.md`, keress: `G2.2` |
| **G2.3** | *(ÚJ)* Ár nélküli módosító | **Szövegsor, nem tétel.** Az „1 Ft-os áthelyezés" **ELVETVE** (ártájékoztatási jogsértés, áfakulcs-váltás, mennyiséggel szorzódás). ⚠️ **Éles készüléken ellenőrizendő**, hogy a nulla összegű tétel átmegy-e | `NYITOTT_KERDESEK.md`, keress: `G2.3` |
| **G2.4** | *(ÚJ)* Levonó módosító fiskálisan | A negatív ár a protokollban **tételsztornó**, nem mínuszos tétel → **a levonó és a hozzáadó módosítónak KÜLÖN fiskális útja van**. A negatív mennyiség viszont **göngyölegvisszavétel** → a DRS-visszaváltás natívan megvan | `NYITOTT_KERDESEK.md`, keress: `G2.4` |
| **G3** | *(ÚJ)* Összetett menü | Termékjelző + **menükomponensek** (min/max, alap 1), felár a **komponens–termék párosításon**. **A menü a nyugtán SZÉTROBBAN** a komponenseire, az ár a listaárak arányában osztva, determinisztikusan. Kötelező, mert vegyes áfakulcs egy sorban nem küldhető, és az NTAK komponensenkénti kategóriát vár | `NYITOTT_KERDESEK.md`, keress: `G3 —` |
| **G4** | *(ÚJ)* DRS — kötelező visszaváltási díj | **Új terület, eddig nem szerepelt.** 50 Ft/db, egyutas 0,1–3 l ital-csomagolás, tej kivétel, **az áfa hatályán kívüli tétel**, elkülönítve a nyugtán. **A lelet: helyben fogyasztásnál nem terheljük a vendégre, elvitelnél igen** → ugyanaz a termék kétféleképp viselkedik. **A díj nem árbevétel.** Blokkoló: melyik gyűjtőre mehet | `NYITOTT_KERDESEK.md`, keress: `G4 —` |
| **G5** | *(ÚJ)* Pénz, kerekítés, valuta | **Bruttó alapú számolás**; a visszaszámolás **áfakulcs-csoportonként, bizonylatszinten**, nem soronként. **Két pénztípus**: egész forint (ár) és nagy pontosságú tizedes (egységköltség); lebegőpont sehol. Kerekítés csak készpénzre, **a készpénzes részre**. EUR: napnyitás előtti árfolyam, **a gépbe is ki kell írni**, visszajáró forintban | `NYITOTT_KERDESEK.md`, keress: `G5 —` |
| **G6** | *(ÚJ)* Nyelvek | HU + EN + DE kötelező. **Két külön feladat**: szoftverszöveg (teljes) és **tartalom** (az ügyfél adata, mezőnként opcionális, magyar visszaeséssel). **A fiskális nyugta magyar.** A felületet **német szövegekkel kell tesztelni** | `NYITOTT_KERDESEK.md`, keress: `G6 —` |
| **G7** | *(ÚJ)* Ki nyomtat | **A KLIENS**, vékonykliensnél a szerver. Az „előzetes szándékrögzítés a szerverre" **ELVETVE** — a szerver nem kerülhet minden nyomtatás kritikus útjába (késleltetés + a vészhelyzeti mód szerver nélkül is működjön). **Elfogadott kockázat.** Enyhítés: a szándék **helyben** rögzül, nulla hálózattal. **Nyitott: az adóügyi eszköz egyetlen géphez kötött — a szerver-HA ezen nem segít** | `NYITOTT_KERDESEK.md`, keress: `G7 —` |
| **G8** | *(ÚJ)* Óraszinkron | **A telephelyi szerver az óra**, a kliensek hozzá igazodnak (nem az internethez). Az adóügyi eszköz órája külön ellenőrzendő napnyitáskor. **Minden óraállítás auditnaplózott.** A sorrendezés monoton számlálón, nem a faliórán | `NYITOTT_KERDESEK.md`, keress: `G8 —` |
| **G9** | *(ÚJ)* Audit napló | **KÉT külön áram:** (A) biztonsági/számviteli — hash-lánccal, 8 év, ~200 rekord/nap; (B) működési (asztal- és felhasználó-történet) — lánc nélkül, 1 év, ~4000 rekord/nap. **A tárhelyet a (B) viszi, de az az ügyfélnek adott érték.** Helyben 30 nap. **A nyers auditot csak MI látjuk**, az ügyfél kurált, vizuális nézeteket kap. **Az olvasás nem naplózódik** — helyette jogosultság szabályoz. Munkajogi oldal: **csak figyelmeztetünk, sablont nem adunk** | `NYITOTT_KERDESEK.md`, keress: `G9 —` |
| **G10** | *(ÚJ)* Árazás | Áfaváltozáskor **a bruttó marad**. **NINCS külön elviteli bruttó ár** — az elvitelen elveszett ~21% haszon bele van kalkulálva. Következmény: **minden árrés-riport teljesítési módonként bontva**. **Kiszerelésnek az ügyfél ad árat, a rendszer nem számol**; a kiszerelés a termék **gyermeke**. Ártörténet a törzsben is | `NYITOTT_KERDESEK.md`, keress: `G10 —` |
| **G11** | *(ÚJ)* Általános tervezési elv | **„Ne próbáljuk megmondani, mit szeretne az ügyfél."** Ahol valós üzleti oka lehet eltérni a számított értéktől, ott a számított érték **egyszeri kitöltő segédlet, soha nem élő hivatkozás** — ugyanaz az elv, mint az áfánál (C3/a) és a FreeLimitnél | `NYITOTT_KERDESEK.md`, keress: `G11` |

Ezen felül: **F) szakasz** hét tétellel (`NYITOTT_KERDESEK.md:647`-től), ami egyik
eredeti doksiban sem szerepelt.

### 1.1 Amit a 2. munkamenet döntései EGYÜTT okoznak — árazandó, nem újranyitandó

Ez a három új döntés (HA az MVP-ben + aszinkron replikáció + teljes degradált mód)
külön-külön mind védhető, de **együtt** két olyan következményt szülnek, amit a
fázisterv (E1) írásakor NEVESÍTENI kell:

1. **Minden telepítés legalább 2 dedikált gép** (fő + tartalék szerver), plusz a
   pénztárgépek. Az E1 mostani munkafeltételezése („kis bár / büfé, 1–2 pénztár")
   mellett ez 2–3 gépes minimum-telepítést jelent. Ez az ügyfél beszerzési és
   árazási tétele. **Ez nem a B1/a újranyitása** — ha elfogadhatatlannak bizonyul,
   az az E1 célprofilját kérdőjelezi meg (kihez szólunk), nem a HA-döntést.

2. **`[FRISSÍTVE]` Egy incidens után HÁROM helyen lesz adat, ami nincs mind ugyanott:**
   a halott fő szerver lemezén (amit még nem replikált ki), a tartalék szerver
   adatbázisában, és a pénztárgépek helyi naplóiban. Ebből következik, hogy a
   **visszaállási procedúra az MVP legkockázatosabb egyetlen darabja**, és a
   hardver-/hibaszimulátor (D5) **nem opcionális** hozzá — kézzel nem
   reprodukálható.

   **Két utólagos enyhítés, ami időközben született, és a kockázatot ÉRDEMBEN
   csökkenti — de nem szünteti meg:**
   - **Tiszta átvételnél** (a régi fő él és a tartalék eléri) a tartalék az átvétel
     ELŐTT leszívja a nem replikált tranzakciókat, tehát **árva adat nem is
     keletkezik**. A három forrás kettőre csökken.
   - Mivel **minden gép önállóan megy csökkentett módba** egy egyszerű wifi-koccanásnál
     is, az egyeztető kód **gyakran fut** — nem évente egyszer, éles katasztrófában
     először. Gyakran futó kód = gyakran javított kód.

   Amit **nem** old meg egyik sem: a **kemény átvétel** (a régi fő tényleg halott)
   ágán az árva tranzakciók elkerülhetetlenek, és a könyvelésük emberhez kell,
   mert automatikus visszaimportálásuk duplikált adóügyi bizonylatot okozhat.

---

## 2. A KÖVETKEZŐ TÉTEL

### 2.0 `[!!]` NTAK RMS SPECIFIKÁCIÓ — két korábbi döntés MEGDŐLT

Az `RMS Interfész leírás v1.06` (az MTÜ hivatalos műszaki specifikációja)
átolvasása után **két rögzített tételünk hibásnak bizonyult**, és egyik sem apróság.

| # | Ami megdőlt | Mi az igazság | Mit érint |
|---|-------------|---------------|-----------|
| **H1** | „NTAK tárgynap = naptári nap" (F4) | **A tárgynap a NYITÁS dátumából származik** → gyakorlatilag a mi MUNKANAP-unk | F4, és a 2. ellenőrző kör „a nap-összevonás az NTAK tartalmát nem érinti" megállapítása |
| **H3** | „24 órás NTAK adatszolgáltatási limit" (C11 premissza) | **A rendelésösszesítő 15 PERCENKÉNT megy**, paraméterezhetően; a napi zárás legalább 24 óránként | a teljes offline/degradált NTAK-terv és a 19. pont SLA-figyelmeztetése |

És egy **ütközés, ami döntést igényel**:

| # | Ütközés | Javaslat |
|---|---------|----------|
| **H2** | A MUNKANAP felső határa **25 óra**; az NTAK napi zárás validációja `zaras − nyitas <= 24 óra`, **szinkron, Conflict** → egy 24 óránál hosszabb nap adatszolgáltatása **elutasításra kerül** | **A felső határ 24 óra alá:** figyelmeztetés 22 órakor, kényszerleállás 23 óra 30 percnél. Az időtartam **abszolút (UTC) alapon** számolva, mert az őszi óraátállítás éjszakáján a falióra egy órát hazudik |

A további új követelmények (mennyiségi egység, kerekítési kényszer, a nyitott
rendelés 24 órás korlátja, nyitvatartási naptár, változó ENUM-készletek):
`NYITOTT_KERDESEK.md`, **H) szakasz**.

### 2.0.2 `[+]` NTAK — második olvasat (J szakasz)

| # | Lelet |
|---|-------|
| **J1** | **Az NTAK-nak VAN hivatalos degradált-mód útvonala:** `osszesitett` + `osszesitettIndoklasa`, „csak szolgáltatáskiesés esetén, pl. áramszünet vagy rendszerkiesés", max 1 üzleti nap összevonva. **Nem kell saját megoldást kitalálni az A2 kiesésre.** Új követelmény: a degradált módnak **okkódot** kell rögzítenie. |
| **J2** | A `helybenFogyasztott` **rendelés-szintű** bool, „vegyes esetben helyben fogyasztást kell jelölni" — a mi tételszintű modellünk finomabb, a leképezés: bármely helyben fogyasztott tétel → igaz |
| **J3** | **A mennyiségi egység NEM validált** — a „0,33 l → LITER" csak útmutatás. A `DARAB` átmegy. **Két külön mező van:** `mennyisegiEgyseg` + `mennyiseg` (a kiszerelés, pl. 0,33) és külön `tetelszam` (a rendelt darabszám) → **két új NTAK-mező a terméktörzsben** |
| **J4** | **Az NTAK-kategorizálás az ÜGYFÉL feladata** — mi a környezetet adjuk. De a kemény kapu marad, mert a hiányzó kategória beküldés-elutasítást okoz, ami üzemeltetésileg a mi problémánk |
| **J5** | **MUNKANAP: 23:00 enyhe / 23:30 erős figyelmeztetés / 23:45 kényszerzárás.** Két fontosabb kiegészítés: **tilos előre állítani az órát nyitott nap közben** (különben a rögzített időtartam felfújódik és elutasítást okoz), és **kell tervezett napzárási időpont**, mert különben a kényszerzárás naponta 15 perccel korábbra vándorol és egy hónap alatt körbeér a csúcsidőbe |
| **J7** | A nyitott rendelés 24 órás korlátja csak a **beküldött** rendelésekre vonatkozik; személyzeti asztal és selejt kivétel — **feltéve, hogy tényleg nem NTAK-kötelesek (ellenőrizendő)** |
| **J8** | **HELYESBÍTÉS:** a zárva tartott nap bejelentése **a MI szoftverünk kötelezettsége**, nem az ügyfélé az NTAK portálon. Szó szerint: „Napi zárási üzenetet akkor is küldenie kell minden RMS szoftvernek, ha az adott tárgynapon zárva tartott a vendéglátó üzlet." → **kell nyitvatartási minta + rákérdezés** |
| **J9** | **Egész forint mindenütt** — az adóügyi eszköz törtet nem kezel, az NTAK igazítható. Technikailag is jobb: az egész egységár mennyiséggel pontosan szorzódik, tört egységárnál 3 db menü három sora nem adná ki a 3× menüárat |

### 2.0.3 `[+]` Automatikus napzárás, zárva tartott nap, nyomtatás-átirányítás (K szakasz)

| # | Tétel |
|---|-------|
| **K1** | **VESZÉLY elhárítva:** a „nem volt nyitva" jelzést TILOS 23:55-kor előre elküldeni. A spec szerint egy `ADOTT_NAPON_ZARVA` napi zárás után **arra a tárgynapra több napi zárás nem küldhető** — ha a hely 23:58-kor mégis kinyit, a valós forgalmuk napi zárása **véglegesen beküldhetetlen**. Helyette: **visszamenőleg**, a tárgynap biztos lezárulta után (pl. 01:00-kor), a nyitvatartási minta alapján. Nyitott javaslat: zárvatartás alatt (kikapcsolt szerver) **a felhő küldje** |
| **K2** | **A figyelmeztetéskori óraszinkron ütközött a J5.1-gyel.** Feloldás: napnyitás előtt **ellenőrzés + beállítás**, a 23:00/23:30 figyelmeztetéskor **csak ellenőrzés, beállítás soha**. Ennél is erősebb: **a munkanap hosszát monoton órán mérjük**, és a vágást a konzervatívabb érték dönti el |
| **K3** | **Automatikus napzárás elfogadva:** műszakok, majd munkanap, felhasználói tájékoztatással, kötelező szünettel a következő nyitásig (**a szünet MAGA a biztonsági tartalék**: 04:00 zárás + 10 perc → max 23:50 munkanap). Hat kiegészítés: előfázis, az elérhetetlen eszköz nem blokkolhat, a vendégasztalt nem zárjuk, konfiguráció-validáció a mentéskor, a szünet állítható (min. 5, alap 10), és a **23:45-ös vészfék megmarad** |
| **K4** | **Nyitvatartási minta bekerül** — ebből tudjuk, mikor kell „nincs nyitva" jelzést küldeni, és mikor kellett volna nyitva lenniük (ami nem ugyanaz, és nem automatizálható) |
| **K5** | **Nyomtatás átirányítása megvalósítható** (IP:port alapú kommunikáció), csak Siduri rendszergazda állíthatja. Öt kiegészítés: **telephelyen belülre keményen korlátozva** (más telephely eszköze más NTAK-regisztrációs szám), a LAN-ra nyitott gyártói szolgáltatás **biztonsági kitettség** (és lehet, hogy nem is támogatott — kérdés a gyártó felé), a bizonylat tárolja **melyik eszköz nyomtatta**, auditnapló, és a felhasználó lássa |

### 2.0.4 `[+]` Integráció-kikapcsolás és a fiskális szolgáltatás hálózati kitettsége (L szakasz)

| # | Tétel |
|---|-------|
| **L0** | **HELYESBÍTÉS + SÚLYOSBÍTÁS:** a gyártói szolgáltatás **nem localhost-korlátos** — portra figyel és nem nézi, honnan jött a kérés. Ezzel a nyomtatás-átirányítás **ingyen van** (nem kell semmit kinyitni), **de a kockázat már most fennáll**: a hálózaton bárki hitelesítés nélkül adóügyi parancsot küldhet. **Új, kötelező telepítési előfeltétel: a vendég-wifi és az üzemi hálózat szétválasztása** |
| **L2** | **A kikapcsolás gépenkénti, a lejárat 1 ÓRA** (nem napzárás — egy óra alatt nem tud normává válni, és az ismételt kikapcsolás maga a jelzés). Eszkalációs létra: üzletvezető 1 óra → 3 ismétlés után értesítés felénk → tartós kikapcsolás csak Siduri. **Lejáratkor ELŐBB önteszt, csak utána visszakapcsolás** — különben óránként valaki egy sikertelen fizetést eszik meg. **És egy új általános szabály: KÉT integrációosztály** — a választóvonal nem az integráció fajtája, hanem hogy hordoz-e jogi/pénzügyi következményt. A nyomtató, KDS az ügyfél eszköze, ő állítja szabadon, lejárat és eszkaláció nélkül (egy kikapcsolva felejtett konyhai nyomtató két percen belül kiderül; egy adóügyi eszköz napokig nem) |
| **L1** | **Integrációk ideiglenes kikapcsolása — új funkció.** Kétszintű jog: bekapcsolni csak mi, ideiglenesen kikapcsolni az általunk **integrációnként** felhatalmazott szerep. **Az NTAK és az audit napló soha nem kapcsolható ki** (nincs hozzájuk kézi tartalék). Öt kötelező korlát a „minden ideiglenes megkerülés állandósul" ellen: **kötelező lejárat**, kötelező indok, tartós jelzés minden gépen, **háttér-önteszt automatikus visszakapcsolással**, és napzárási jelentés. **A kikapcsolást SOHA nem ajánljuk fel** (a korábbi javaslatom elvetve: a megkerülés felajánlása a megkerülés megtanítása) — dedikált gomb a beállításokban, a hibaüzenet iránymutat („szóljon az üzletvezetőnek") de nem kínál kart, a hiba a jogosulthoz jut el, és tartós, elrejthetetlen sáv jelzi az állapotot **a teendővel együtt**, plusz kötelező nyugtázás napzáráskor. A fiskális integrációra szigorúbb szabályok, mert **ez a visszaélés kara** |

### 2.0.5 `[+]` Külső felülvizsgálat (Gemini) — 17 tétel értékelve (M szakasz)

| Kategória | Db | Tételek |
|---|---|---|
| **Valódi hiányosság nálunk — beépítve** | 11 | számla/nyugta kizárás · utalványok (egycélú vs. többcélú) · NTAK-tanúsítvány lejárat · allergének · GDPR vendégadat-törlés · számlamegosztás · címletkalkulátor · negatív készlet · Windows Update · kártyaterminál internet-figyelmeztetés · **PostgreSQL WAL-felhalmozódás** |
| **Beépítve, de a javaslat korrigálva** | 5 | szervizdíj-plafon (nincs jogi felső határ, a kemény 15% sértené az A3 elvet) · 18+ figyelmeztetés (tételenkénti felugró = zaj; a felelősség nem hárul át) · audit UUID (a jogi premissza téves, a mechanizmus jó) · kártyás borravaló (a „szigorúan tilos" túl abszolút) · terminál-üzenet szövege (a javaslat kerülőutat ajánlott = A8 sértés) |
| **A javaslat JOBB a mi döntésünknél — módosítottunk** | 1 | **árva tranzakció feloldása kizárólag Siduri támogatói felületen** |

**A két legfontosabb lelet:**

- **PostgreSQL WAL:** egy leszakadt tartalék szerverhez tartozó replikációs slot miatt a fő szerver korlátlanul őrzi a WAL-t → betelik a 64 GB-os SSD → **a fő szerver megáll.** Nálunk kiemelten veszélyes, mert két, eddig külön kezelt tényt köt össze: a tartalék egy POS gép, és **azt valaki kikapcsolhatja** (§5.2). Új mérés: M19.
- **Windows Update:** a teljes HA-t a szerver hardverhibája ellen építettük, közben a **sokkal valószínűbb** esemény egy Windows-újraindítás csúcsidőben — és az teljesen megelőzhető. Kötelező telepítési ellenőrzőlista-tétel lett.

Részletes értékelés tételenként: `NYITOTT_KERDESEK.md`, **M) szakasz**.
A `siduri_spec_hu.md` és a `siduri_superprompt_en.md` frissítve; az invariánslista
30-ról **41 pontra** bővült.

### 2.0.6 `[+]` Felhasználói korrekciók + a külső felülvizsgálat 2. köre (N szakasz)

**Három korrekció az 1. kör tételeihez:**

| # | Korrekció |
|---|-----------|
| **N0.1** | **Allergének: CSAK lehetőség.** Nincs kötelező kitöltés, nincs kapu, **nincs figyelmeztetés a kihagyásra** — opcionális kiegészítő funkció, amit kevesen fognak használni. Egyetlen biztonsági kikötés marad: **vagy teljes a lista, vagy nincs** (részleges lista veszélyesebb az üresnél, mert teljesnek hiszik) |
| **N0.2** | **Kilépett dolgozó: soft delete, a napló és a korábbi adat érintetlen** — a visszaellenőrizhetőség jegyében. Jogilag is rendben: a jogi kötelezettséghez és jogi igények védelméhez szükséges adatkezelésre a törlési jog nem terjed ki |
| **N0.3** | **18+: piktogram a tételsoron, felugró ablak SEMMIKÉPP.** Az ügyfél állítja, kéri-e, és **ő adja meg, mely termékek 18+** — az energiaital példája mutatja, hogy ez változik, és ha mi szállítanánk a listát, minden jogszabály-változásnál mi lennénk a hibásak |

**A 2. kör 9 tétele — mind elfogadva, egy tárgyi tévedéssel:**

| # | Tétel | Megjegyzés |
|---|-------|-----------|
| **N1** | **Vakzárás** — jogosultsághoz kötve | ⚠️ **Az adóügyi eszköz X-jelentése kiütné** — azt is jogosultsághoz kell kötni, különben látszatvédelem. És **a rögzítés után sem szabad visszamutatni az eltérést** |
| **N2** | **Sztornó/törlési anomália riport** a BI-ban, valós idejű riasztás nélkül | A mérőszám **állapot és idő szerint minősítendő**: a 10 másodperc múlva törölt tétel elgépelés; a jel a **konyhára már elküldött tétel törlése fizetés előtt** |
| **N3** | **Kasszafiók-állapotfigyelés** | `v2`. ⚠️ **Ha nincs szenzor, ne legyen bekapcsolható** — a csendben soha meg nem szólaló biztonsági funkció rosszabb a semminél |
| **N4** | **Fogások késleltetett küldése** — **a kör legfontosabb tétele** | Valódi hiány: nálunk csak **nézet** volt fogásonként, **küldési mechanizmus nem.** A KDS lássa a visszatartott fogásokat is |
| **N5** | **Mérleg és tára** | A mérleg szerepelt, a **tára és a folyamat nem** |
| **N6** | **Időszakos árazás determinizmusa** | **Egy általunk nyitva hagyott kétértelműség:** az ár a **sor létrehozásának** időbélyegéhez rögzül. Határeset, amit a javaslat kihagy: a **mennyiségnövelés új sort hoz létre** |
| **N7** | **Előleg és asztalfoglalás** | Eddig egyáltalán nem szerepelt. ⚠️ Nyitott: **milyen áfakulcson adózik az előleg** vegyes adómértékű jövőbeni fogyasztásnál |
| **N8** | **Kiszállítás mint harmadik teljesítési mód** | ⚠️ **TÁRGYI TÉVEDÉS a javaslatban:** „automatikusan 27%-kal rögzíti". Nálunk **kulcsot nem égetünk a kódba** — a kiszállítás az **elviteli áfamezőt** használja, bármi is legyen benne |
| **N9** | **Offline vészmentés (pendrive)** | `v2`. ⚠️ **A javaslat átugorja a lényeget: milyen KULCCSAL titkosítunk?** Ha a kulcs a tönkrement gépen van, a mentés használhatatlan. És **az ellenőrizetlen mentés nem mentés** |

Részletes értékelés: `NYITOTT_KERDESEK.md`, **N) szakasz**.
A két végleges dokumentum frissítve; az invariánslista **41-ről 49 pontra** bővült.

### 2.0.1 `[!]` A 3. munkamenetből MÉG NYITOTT tételek

Ezek a 2026-08-23-i körben felmerültek, de **még nincs rájuk válasz**. Amíg
nincs, a két végleges dokumentum (`siduri_spec_hu.md`, `siduri_superprompt_en.md`)
ezeken a pontokon feltételes marad.

| # | Nyitott kérdés | Kihez |
|---|---------------|-------|
| ~~N1~~ | ~~Beszerzési ár~~ -> **ELDÖNTVE (I3):** bruttó felvitel + kötelező beszerzési áfakulcs, az árrés és a food cost NETTÓ alapon | — |
| ~~N2~~ | ~~DRS~~ -> **ELDÖNTVE (I4):** alapban TERHELVE, üzletenként kikapcsolható helyben fogyasztásra | — |
| ~~N3~~ | ~~Óraszinkron küszöbök~~ -> **ÁTDOLGOZVA (I5):** először javítunk (NTP, majd az adóügyi eszköz órája); blokkolás csak 2 óránál nagyobb eltérésnél vagy dátumeltérésnél. A valódi veszély a halott CMOS-elem, nem a másodperces drift | — |
| ~~N4~~ | ~~Repók~~ -> **ELDÖNTVE (I1.1):** MINDIG privátok maradnak | — |
| ~~N5~~ | ~~Nyomtatás-átirányítás~~ -> **ELDÖNTVE (K5):** megépítjük, IP:port alapon, csak Siduri rendszergazda állíthatja, telephelyen belülre korlátozva. Eredetileg: **RÉSZBEN eldöntve (I2):** gépenként adóügyi eszköz az ajánlás, 4 géptől kiemelten legalább kettő. **Nyitva maradt:** megépítjük-e a nyomtatás átirányítását másik gép eszközére | felhasználó |
| ~~N6~~ | ~~DRS gyűjtője~~ -> **ELHALASZTVA (I6.1):** a beüzemelés része; előtte gyártói egyeztetés, mert lehet, hogy náluk már megoldott | később |
| N7 | **Újrakiosztható-e az AJT gyűjtő** (G1.3) | **gyártó** |
| N8 | **Nulla összegű tétel** — a munkafeltevés mostantól: **NEM fogadja el** (I6.2). A G2.3 szövegsoros megoldás ettől függetlenül helyes, sőt megerősítést nyer | **gyártó** |
| ~~N9~~ | ~~NTAK menükezelés~~ -> **MEGVÁLASZOLVA (H4):** van ETELCSOMAG/ITALCSOMAG, de csak főkategórián belül -> vegyes menüt kötelező szétbontani. A G3 döntés helyes | — |
| ~~N10~~ | ~~MUNKANAP felső határa~~ -> **ELDÖNTVE (J5):** 23:00 enyhe / 23:30 erős / 23:45 kényszerzárás, plusz tervezett napzárási időpont | — |
| **N12** | **J6:** elfogadja-e az NTAK, ha egy tárgynapra a napi zárás UTÁN még jön rendelésösszesítő (a munkanap-határon átnyúló nyitott asztal miatt)? 0-24-es helyen mindennapos | **NTAK / MTÜ** |
| **N13** | **J7:** NTAK-köteles-e a személyzeti fogyasztás és a selejt? Ettől függ, hogy rájuk is vonatkozik-e a 24 órás korlát | **NTAK / MTÜ** |
| **N14** | **K1.2:** zárvatartás alatt (kikapcsolt telephelyi szerver) **a felhő küldje** a napi zárásokat? | **felhasználó** |
| **N15** | **L0:** van-e a gyártói szolgáltatásnak bármilyen **hitelesítési, IP-korlátozási vagy figyelési-cím** beállítása? (a nem-localhost figyelés kérdése tárgytalan — már most bárhonnan fogad) | **gyártó** |
| **N16** | **K3.2:** elfogadja-e az NTAK a múltbeli (utolsó tevékenység szerinti) zárási időbélyeget, ha a szerver 24 óránál tovább volt halott? | **NTAK / MTÜ** |
| ~~N17~~ | ~~Kikapcsolás hatóköre~~ -> **ELDÖNTVE (L2):** gépenkénti; **1 órás lejárat** eszkalációs létrával; és **két integrációosztály** — védett (adóügyi, bankkártya, NTAK: Siduri kezeli) vs. ügyfél-eszköz (nyomtató, KDS: az üzletvezetőé, lejárat és gépezet nélkül) | — |
| **N18** | **M2.d:** milyen NTAK-besorolást kap a többcélú utalvány ELADÁSA? | **NTAK / MTÜ** |
| **N19** | **M10.e:** a szétbontott számla az NTAK-ban egy rendelésösszesítő több fizetési móddal, vagy több rendelésösszesítő? | **NTAK / MTÜ** |
| **N20** | **M9.d:** a borravaló adózása (borravaló vs. felszolgálási díj, készpénz vs. kártya) | **könyvelő / adótanácsadó** |
| **N21** | **N7.d:** milyen áfakulcson adózik az előleg vegyes adómértékű jövőbeni fogyasztásnál? | **könyvelő** |
| **N22** | **N7.c:** az előleg tényleg kimarad az NTAK-ból? | **NTAK / MTÜ** |
| **N11** | **H3 következménye:** a 15 perces NTAK-küldés miatt a kimenő NTAK-sor tartós, felügyelt sor kell legyen, és a feldolgozási nyugtákat is le kell kérdezni (24 órán belül). Új munkatétel a fázistervben | tervezés |


### 2.1 A KÖVETKEZŐ MUNKA — a 2. ellenőrző kör után

**Mindkét ellenőrző kör lezárult.** A 2. kör hat teendőt nevesített, és ezek
**a fázisterv (E1) ELŐTT vagy VELE PÁRHUZAMOSAN** indítandók:

| # | Teendő | Miért most | Ki |
|---|--------|-----------|-----|
| **1** | **`[ ]` A pénz- és mennyiség-ábrázolás eldöntése (`F2`)** | Öt perc, és minden számítás rá épül. **A legolcsóbban eldönthető és legdrágábban javítható döntés.** | döntés, azonnal |
| **2** | **`[ ]` Könyvelői megerősítés a bizonylat-számozásra** | **NÉGY döntés függ tőle** láncban. Egy mondat. | felhasználó |
| **3** | **`[ ]` A három külső kapu elindítása** — MTÜ-validáció, NAV-kérdés (kell-e engedély a szoftvernek), gyártói protokoll (NDA) | **Ezek uralják a határidőt, nem a fejlesztés.** Egyik sincs elindítva. | felhasználó |
| **4** | **`[ ]` Az RMS interfész-leírás és az e-nyugta séma elolvasása** | **A termékmodell nem tervezhető nélkülük.** Mindkettő nyilvános. | elvégezhető |
| **5** | **`[ ]` Néhány napos ELŐMÉRÉS valós J1900-on** | A legdrágább feltevés (kombinált szerver+POS) cáfolata, **mielőtt ráépítünk mindent.** Nem kell hozzá a Siduri. | hardver kell |
| **6** | **`[ ]` E1 — fázisterv, és az ELSŐ dolga: `MVP`/`v1`/`v2`/`vízió` címke MINDEN döntésre** | Enélkül a jelenlegi ~50 döntés **úgy néz ki, mintha mind MVP lenne.** | a fázisterv része |

#### `[LEZÁRVA — a felhasználó döntése]` A 2. kör `A1` leletje: méret vs. csapat

**A felhasználó döntése (2026-08-22):** a létszám **nem** korlát — ha bővíteni
kell, azt megoldja. **Az `A1` lelet ezzel lezárva, nem hozzuk fel újra.**

**`[!]` DE öt dolog akkor sem gyorsul a létszámtól**, és ha ezekkel úgy
számolunk, mintha igen, **az ütemezés hibás lesz:** (1) a külső kapuk
sorbaállása, (2) a sorrendi függések (az MTÜ-validációhoz működő modul kell),
(3) a hardver igazsága, (4) a külső dokumentáció megérkezése, és
**(5) a varrat-kockázat, ami NŐ a létszámmal** — több ember, három nyelv, hat
repó → **több néma szétcsúszás.** Az API-szerződés és a paritás-őr ettől
**sürgősebb lesz, nem kevésbé.** → `MVP_DEFINICIO.md` 0. szakasz.

**`[!]` És egy fogalmi váltás:** amíg a létszám volt a korlát, azért fázisoltunk,
mert „ennyi fér bele". Most **más okból fázisolunk, és ez jobb ok:**
**hogy a lehető leghamarabb megtudjuk, hol tévedtünk.** Ebből az következik,
hogy **az MVP-t nem a legkisebb munkára kell szabni, hanem a legtöbb tanulásra
egységnyi munkára.**

#### `[!]` A második: nincs TERMÉKMODELL

**Tizenhét kör után a `C1` változatlanul nyitva:** módosítók, feltétek, menük,
„kiszerelés" (a spec hivatkozik rá, sehol nincs definiálva), többszintű
receptúra, allergének, súly szerinti termékek + mérleg.

**Egy vendéglátó POS a módosítókon áll vagy bukik** — „hamburger hagyma nélkül,
extra sajttal" —, és **erre nulla terv van**, miközben a failoverre ötven oldal.
**És a termékmodell sem tervezhető meg a két külső séma (NTAK RMS, e-nyugta)
elolvasása előtt** → lásd a 4. teendőt.

### 2.1.0 `[!]` Amit a fázisterv írásakor NEM szabad elfelejteni

**A csökkentett mód NEM véd minden telepítésen.** Ez a legkönnyebben
félreérthető pont az egész tervben:

| Telepítés | Ha a fő szerver meghal (tartalék nélkül) |
|-----------|-------------------------------------------|
| 1 Windows POS = szerver, mellé vékonykliensek | **SEMMILYEN védelem — a hely megáll** |
| 2+ Windows POS, egyikük a szerver | a többi POS csökkentett módban eladhat |
| Dedikált szerver + N Windows POS | **minden POS eladhat — itt a legnagyobb a haszon** |

Az „1 POS + sok vékonykliens" nem „kicsit kevésbé védett", hanem **teljesen
védtelen** — a rajta futó csökkentett mód is meghal a géppel együtt. Az
értékesítési beszélgetésben pontosan ezt kell mondani.

### 2.1.1 `[ ]` A kétlépcsős failover kitöltési kérdései (R1–R5; az R6 megerősítve)

Nem irány-, hanem részletkérdések. Mindegyik önállóan tud csendben elromlani.
→ `NYITOTT_KERDESEK.md`, keress az `R1` … `R6` jelölésekre.

1. **R1 — ki a „tanú"**, és mi van egypénztáras helyen (lásd fent, 1. pont). Plusz:
   egy lekapcsolt gép némasága NEM bizonyíték — külön kell kezelni azt, hogy egy gép
   JELENTI, hogy nem éri el a szervert, attól, hogy MI nem érjük el a gépet.
2. **R2 — miből ismeri fel a gép, hogy Ő esett ki?** Ez **új architekturális
   követelmény**: a pénztárgépeknek egymást és a tartalék szervert is látniuk kell
   (eddig csillag-topológia volt, mindenki csak a szerverrel beszélt). Felderítés
   + **kölcsönös hitelesítés** kell hozzá, mert a belső hálózat nem megbízható.
3. **R3 — az 5 perc:** monoton időmérőn (nem fali órán), konfigurálhatóan, és
   **az ajánlatnak le kell járnia**, ha közben visszatér a fő szerver.
4. **R4 — több gép mutatja a gombot** → az átvétel legyen idempotens, az első nyer.
5. **R5 — a fő szerver ÉL, csak nem érik el.** Innen két dolog: a fencinget a
   **kliensnek is** ki kell kényszerítenie (régebbi epochú szerverrel tilos
   beszélni), ÉS ez a „tiszta átvétel" esete, ahol tényleg nulla veszteség érhető el.
6. **R6 — `[MEGERŐSÍTVE]`** ha a tartalék sem egészséges, átkapcsolást felajánlani
   sem szabad.

Plusz egy **design-tétel**: az 5 perc ne üres visszaszámlálás legyen, hanem mutassa,
mit állapított meg közben a gép; és a megerősítő képernyő számmal mondja meg a
következményt, ne egyszerű igen/nem legyen (különben kialakul a „nyomd meg a zöld
gombot" reflex).

### 2.2 `[KÉSZ]` E1 — fázisterv

**A fázisterv megírva: [`FAZISTERV.md`](FAZISTERV.md).**

Amit rögzít: nyolc fázis (F0–F8), öt párhuzamos sáv, fázisonkénti **éles kilépési
feltétel**, **kritikus út** és **hat döntési pont**, ahol megállunk és
újratervezünk.

**Amit tudatosan NEM ad meg: naptárat.** Az átfutási időt **három külső kapu**
határozza meg (gyártói kapcsolat + tesztkészülék · MTÜ tanúsítás · fizikai J1900
referenciagépek), és **egyik lead time-ját sem ismerjük.** A terv abban a
pillanatban válik naptárrá, amint ezek megvannak — addig minden dátum kitalált
szám lenne.

**A terv szervezőelve nem a funkciók fontossága, hanem a kockázat-kioltás:**
ami meg tudja ölni a projektet, azt a legolcsóbb pillanatban kell kideríteni.
Ezért az **F1 kilépési feltétele nem funkció, hanem bizonyíték** — a P1 premissza
(az adóügyi eszköz önállóan állítja ki és sorszámozza a bizonylatot) **igazolva
vagy megdöntve, írásban**, valódi eszközön, valódi J1900-on. Egy hamis P1-et a
3. héten megtudni kellemetlen; a 6. hónapban katasztrófa.

**Három dolog van a kritikus úton, és egyik sem kód:** a hardverbeszerzés, a
tanúsítás és a gyártói kapcsolat. **Ezért a csapatlétszám növelése nem rövidíti
arányosan a projektet** — a K1–K3 kapukat ma kell elindítani, nem akkor, amikor
odaérünk.

**AZ ELSŐ ÜGYFÉL MEGVAN: egy ÉTTEREM, aki gyakorlatilag minden tervezett
megoldást használni fog.** Ezzel a korábbi legnagyobb kockázat (nincs névre
szóló ügyfél, az MVP-definíció fogadás) **megszűnt** — a hatókör tény.

**Cserébe megszűnt a fokozatos szállítás lehetősége.** Az egygépes szint, mint
korán élesíthető termék, egy étteremnek használhatatlan: ott az első éles napon
**egyszerre** kell működnie az asztalkezelésnek, fogásoknak, módosítóknak,
menüknek, KDS-nek, készletnek, receptúrának, több gépnek, a fiskális rétegnek,
az NTAK-nak és a felhős adminnak. **Az F2–F8 mind kötelező**, a HA nem opció
(4+ gép), és **a pilot egy ÉLŐ étterem** — ott nem lehet kísérletezni szerviz
közben.

**A kockázat-kioltó sorrend ettől NEM lesz értéktelen** — az F1 továbbra is
3 hét alatt oltja ki a legveszélyesebb premisszát 6 hónap helyett, és az M13
kapu továbbra is megmenti a HA-terv újraépítését. **Csak a „kimehetünk élesbe"
pont csúszik a végére.**

**Új kötelező fáziselem: F8.6 — átállási terv.** Egy működő éttermet nem lehet
péntek este átkapcsolni. Adatmigráció, csendes időpont, **visszaállási terv**, és
⚠️ **NTAK-váltás kettős jelentés nélkül** — a régi és az új szoftver egyszerre
nem jelenthet ugyanarról a forgalomról.

**Új döntési pont: D7, még az F1 ELŐTT** — az ügyfél tényleges felállásának
felmérése (milyen adóügyi eszköz, hány gép, milyen hardver, mit váltanak le).
**Ez konkretizálja a K1 és K3 kaput.** A kérdéssor: `FAZISTERV.md` §7.5.

### 2.3 Ami a B1/c-től FÜGGETLENÜL már most elkezdhető (tervezésként, nem kódként)

Ezek egyik nyitott döntéstől sem függenek, és mind a nyolc lezárt döntés
következménye — a fázisterv úgyis mindet tartalmazni fogja:

- **B8 — hol él az API-szerződés** (`NYITOTT_KERDESEK.md:449`). Az E2 döntés
  (2–3 fő, három nyelv) miatt ez az „első hét" tétele. Új szempont az 5. szakaszból:
  a Siduri-Docs csak doksinak van szánva, tehát a `contracts/` mappa ide nem fér
  bele → vagy 6. repó, vagy a kikötés lazítása.
- **F1 — idempotencia-kulcs minden kliens-írásra** (`NYITOTT_KERDESEK.md:647`).
  Az A2/b döntés (teljes degradált mód) után ez már nem javaslat, hanem
  **következmény**: helyi napló lejátszása idempotencia nélkül duplikált tételt ad.
- **Epoch-mező (fencing) a protokollban.** A B1/a döntés (HA az MVP-ben) után ez
  nem elővigyázatosság, hanem **működési követelmény** — ez akadályozza meg, hogy a
  visszatérő régi fő szerver még kiszolgáljon klienseket.
- **F2 — pénz- és mennyiség-reprezentáció.** Minden számítás alapja, semmitől nem függ.

## 3. `[?]` IGAZOLATLAN PREMISSZÁK — erre döntést építeni TILOS (§13.5)

**Ez a szakasz a legfontosabb az új munkamenet számára.** Egyik állítás sem
verifikált tudás; mindegyik a spec állítása vagy emlékezetből írt feltevés.
§2.2: *„a hiba nem a tévedés, hanem hogy döntést kérsz ellenőrizetlen premisszára."*

| Tétel | Az igazolatlan állítás | Mi dől meg, ha hamis |
|-------|------------------------|----------------------|
| **A2** | AEE-s gépnél a jogi bizonylatot maga az adóügyi eszköz állítja ki és sorszámozza | **A már meghozott A2 döntés egésze** |
| **A3** | A számviteli megőrzési idő (8 év?) | A 30 napos purge és a „tisztán lokális" topológia egyszerre |
| **C10** | „Teljesen új negatív fiskális nyugta" sztornóra | A teljes sztornó-folyamat (13. fejezet) |
| ~~**C11**~~ | ~~24 órás NTAK limit~~ → **IGAZOLVA HAMIS: 15 PERC** (H3) | A 19. pont SLA-figyelmeztetése újraírandó |
| **C12** | Az e-nyugta iránnyal most nem kell foglalkozni | A bizonylat-modell alakja |

Az **A2** külön figyelmet érdemel: ez az egyetlen olyan tétel, ahol **már meghozott
döntés** áll igazolatlan premisszán. Ha az igazolás cáfolja, az A2-t és az A2/a-t
újra kell nyitni.

## 3.1 `[?]` MÉRÉST IGÉNYEL — a teljes lista átköltözött a `MERESEK.md`-be

**A mérendő tételek külön fájlba kerültek: `MERESEK.md`.** Itt csak a mutató és a
két legfontosabb tudnivaló marad (§2.4: egy igazságforrás, a többi mutató — és a
mutató mondja ki, hogy mutató).

> ### ⚠ A FELHASZNÁLÓ KIEMELT UTASÍTÁSA (2026-08-22)
> **AZ ELSŐ TÉNYLEGES ÉLES TESZTNÉL MINDENT MEG KELL MÉRNI.**
> Ez nem opcionális lépés, hanem **szállítási kapu**. A mérésnek **külön fázist
> kell kapnia** a fázistervben (E1), saját időkerettel — a mérés nem a fejlesztés
> mellékterméke. Az éles teszt nem zárható le „úgy tűnt, jól ment" alapon.

**A legfontosabb egyetlen tétel** (`MERESEK.md`, **M12**): **a tartalék POS
átveszi a szolgálatot.** A tartalék mindig egy dolgozó pénztárgép, tehát átvételkor
ugyanaz a J1900 viszi a saját kasszáját ÉS az egész hely kiszolgálását — a lehető
legrosszabb pillanatban, mert a szerver akkor esik ki, amikor a hely dolgozik.
**Ha a tartalék nem bírja, a failover rosszabbá teszi a helyzetet, nem jobbá.**
Ez azt dönti el, érdemes-e egyáltalán átkapcsolni.

Közvetlenül utána (M1): **a kombinált szerver + pénztárgép egy J1900-on** — a
felhasználó kimondta, hogy *„a legtöbb esetben a szerver egy olyan gép lesz, ami
egyébként kliens is"*, tehát ez **nem szélső eset, hanem az alapértelmezett
telepítés.** Ha ez nem fér bele a hardverbe, nem egy funkció dől meg, hanem a
telepítési modell.

**Mind a mérésekhez fizikai J1900 referenciagép kell**, a replikációsokhoz
**kettő** — beszerzési tétel, hetekig tarthat, érdemes a kódolással
párhuzamosan elindítani.

## 4. Miért nem kódolunk még

A felhasználó explicit kérése: *„kódolni egyelőre nem kell, még csak tárgyaljuk át a
projectet és véssük kőbe a végleges, mindenre kiterjedő, nagyon pontos tervet."*

Ezen felül mérnöki okból is korai:
- egy blokkoló döntés nyitva (B1/c — ki vált át a tartalék szerverre, és a vele
  együtt döntendő A4 visszaállítás), és csak utána írható meg a fázisterv (E1),
- öt igazolatlan premissza (3. szakasz) — köztük EGY olyan, amin **már meghozott
  döntés** áll,
- és **B8** — az API-szerződés helye — még nincs eldöntve
  (`NYITOTT_KERDESEK.md:449`), ami 2–3 fős, három nyelvű csapatnál az **első hét**
  tétele. Ha kód születik előtte, a varrat (§6) már szétcsúszott mire észrevesszük.

---

## 5. Repó- és git-állapot

> **JAVÍTVA (2026-08-22, 2. munkamenet).** Ez a szakasz korábban azt állította, hogy
> „a munka NINCS biztonságban", a remote egy lokális `W:\...` útvonal, és a branch
> `claude-coding`. **Mindhárom állítás elavult** — §2.4 (doksi-drift): egy elavult
> „ez blokkolt" bekezdés a következő kört egy nem létező hátralék hajszolására küldi.

**Tényleges állapot (mérve, nem feltételezve — `git remote -v`, `git branch`):**

| Repó | GitHub remote | Tartalom |
|------|---------------|----------|
| `kafnyi/siduri-docs` | ✔ | 5 doksi + üres README |
| `kafnyi/siduri-backend-server` | ✔ | csak README (üres) |
| `kafnyi/siduri-pos-client` | ✔ | csak README (üres) |
| `kafnyi/siduri-flutter-clients` | ✔ | csak README (üres) |
| `kafnyi/siduri-updater` | ✔ | csak README (üres) |
| `kafnyi/siduri-cloud-api` | ✔ | csak README (üres) |

**Munkabranch mind a 6 repóban:** `claude/siduri-hospitality-system-gpixt0`
(a `master` az alapértelmezett branch). §10 tehát **teljesül**: a távoli branch az
igazságforrás, a környezet ephemer, ezért minden részeredmény commitolva ÉS
pusholva megy.

**A `Siduri-Docs` szerepe (a felhasználó kikötése, 2026-08-22):** **kizárólag**
dokumentáció-tárolás. Kód nem kerül bele. Ide jön a teljes projekt-dokumentáció,
és ide jönnek az AI-munkamenet saját, mindig naprakész állapot-doksijai
(ez a fájl + a `NYITOTT_KERDESEK.md`) — utóbbiakra nincs formai vagy nyelvi
megkötés, az egyetlen követelmény, hogy **soha ne maradjanak le a valóságtól**,
akkor sem, ha a tényleges terv-dokumentáció épp lemaradt.

**Nyitott következmény:** a **B8** (hol él az API-szerződés) javaslata „6. repo VAGY
a `Siduri-Docs`-ban egy `contracts/` mappa" volt. Mivel a Docs csak doksinak van
szánva, ez a `contracts/` ág **most gyengébb** — vagy 6. repót nyitunk, vagy a Docs
kikötését lazítjuk. Eldöntendő a B8-nál.

**Munkamenet-szabály (§10):** hosszú folyamat indítása előtt ellenőrizd, nincs-e
félbeszakadt — és ha van, kérdezd meg, azt folytassuk-e.

**Attribúció (§12) — ELDÖNTVE:** a MERNOKISAROKKOVEK §12 attribúciós szabálya
**vonatkozik erre a projektre**. Semmilyen AI-utalás nem kerülhet kódba, kommentbe,
doksiba, **commit-üzenetbe**, PR-leírásba vagy CI-konfigba. **Commit-üzenet záró
trailer nélkül.**

---

## 6. A folytatás pontos módja

Új munkamenet indításakor, ebben a sorrendben:

1. Olvasd el ezt a fájlt (kész).
2. Olvasd el a `MERNOKISAROKKOVEK.md`-t — a szabályok kötelezőek, és az indoklás
   („miért") a szabály része, nem díszítés.
3. Olvasd el a `NYITOTT_KERDESEK.md`-t. A két spec-fájlt **csak ezután**, és a
   `[MÓDOSÍTVA]` / `[SUPERSEDED]` jelöléseket komolyan véve.
4. **Olvasd el a 0.1 szakaszt** (kommunikációs szabályok) — ha ezt kihagyod, a
   felhasználó nem tud dönteni, mert csupasz azonosítókkal fogsz kérdezni.
5. A soron következő munka: **B1/c lezárása a felhasználóval** — ki vált át a
   tartalék szerverre, amikor a fő meghal, és vele együtt az A4 (ki és hogyan
   állítja vissza a fő szervert) — a 2.1 szakasz szerint. Majd **E1 fázisterv**
   (2.2). Ami közben a döntéstől függetlenül vihető: 2.3 szakasz.

**Ha egy tétel eldől:** jelöld `[ELDÖNTVE — <döntés>]`-ként a
`NYITOTT_KERDESEK.md`-ben, **az indoklással együtt**, frissítsd a prioritási táblát
és ezt a fájlt — majd commitold. Sehol máshol ne vezess párhuzamos döntéslistát
(§2.4).
