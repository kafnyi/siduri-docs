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

**Utolsó frissítés:** 2026-08-22 (2. munkamenet)
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
| `siduri_superprompt_en.md` | Ugyanaz megaprompt formában (angol, Geminihez) | **Részben ELAVULT** — inline `[SUPERSEDED]` / `[OPEN]` jelölésekkel |
| `FOLYAMATBAN.md` | Ez a fájl — állapot és folytatás | Élő |
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

**Huszonkét döntés lezárva** (öt az 1., tizenhét a 2. munkamenetben, mindkettő 2026-08-22).
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
| **B9 jellege** | *(ÚJ)* Kikényszerített-e a méret-lépcső | **Nem — ÉRTÉKESÍTÉSI AJÁNLÁS.** Ha kellene tartalék de nincs hova tenni, dedikált szervergépet ajánlunk (az nem POS, így egyetlen Windows POS is elláthatja a tartalék szerepet). Ha az ügyfél a kockázat ismeretében elutasítja, elfogadjuk. **A szoftver semmilyen konfigurációt nem utasíthat el** | `NYITOTT_KERDESEK.md`, keress: `A lépcső AJÁNLÁS` |
| **Szerepkiosztás** | *(ÚJ)* Melyik gép viheti a szerver-szerepet | **A tartalék MINDIG Windows POS vastagkliensen van, SOHA nem dedikált gépen.** A fő szerver jellemzően szintén POS-on; aki megengedheti, annál lehet dedikált. **Vékonykliens, KDS, rendeléskijelző egyiket sem viheti** | `NYITOTT_KERDESEK.md`, keress: `A „dedikált" szó pontosítása` |
| **B10/a** | *(ÚJ)* Adatvédelem a kliens-archívumban | **A szerver jellemzően egy dolgozó pénztárgép lesz**, nem irodai gép → a teljes adatbázis a pultban áll. A fizikai lopás ellen szoftverrel nem lehet teljesen védekezni — ezt ki kell mondani. Ellenszer: **adatminimalizálás** (tervezési szabály), lemeztitkosítás ha van TPM, fizikai rögzítés, és a felhőmentés mint egyetlen helyreállítási út lopás után | `NYITOTT_KERDESEK.md`, keress: `B10/a` |
| **B10/b** | *(ÚJ)* Kliens-archívum megőrzési ideje | **20 FORGALMAS üzleti nap**, nem 20 naptári nap — egy zárva töltött nap nem számít bele és nem öregít ki semmit. A licenc 10 napos türelmi idejével szándékosan nem közös érték. Nyugtázatlan adatot a megőrzés soha nem töröl | `NYITOTT_KERDESEK.md`, keress: `B10/b` |
| **B9/b** | *(ÚJ)* Mikor kötelező a tartalék szerver | **1 gép:** nincs. **2–3 gép:** opcionális. **4+ gép:** kötelező. Következmény: a „nincs tartalék szerver" elsőrangú konfiguráció, nem hibaállapot | `NYITOTT_KERDESEK.md`, keress: `B9/b` |
| **B9/a** | *(ÚJ)* Egygépes telepítés | **A pénztárgép MAGA a szerver.** Ezzel eldőlt a korábban nyitott kérdés is: igen, futhat egy gépen szerver ÉS kliens — támogatott konfiguráció | `NYITOTT_KERDESEK.md`, keress: `B9` |
| **Üzenetek** | *(ÚJ)* Személyzeti hibaüzenetek | **Három üzenet jóváhagyva** („hálózat", nem „internet"), plusz külön jelzés az internet hiányára | `NYITOTT_KERDESEK.md`, keress: `A személyzetnek szóló üzenetek` |
| **B3** | Minimum célhardver | J1900 **vegyes bázis** (szerver ÉS kliens) → **GraalVM kényszer marad**, plusz szoros WPF perf-költségvetés | `NYITOTT_KERDESEK.md:374` |
| **E2** | Ki fejleszti | 2–3 fős csapat + AI → **B8 (API-szerződés) az első hét tétele**, nem opcionális | `NYITOTT_KERDESEK.md:612` |

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

### 2.1 A FÁZISTERV MOST MÁR MEGÍRHATÓ

**Nincs több blokkoló döntés.** Ami nyitva maradt, az mind párhuzamosan
elintézhető a fázisterv írásával:

1. **`[ ]` Van-e TPM a meglévő J1900 bázison?** Hardveren ellenőrizhető tény, nem
   vélemény. Ha nincs, a felügyelet nélkül induló pénztárgépen a teljes
   lemeztitkosítás útvonala elesik, és marad az adatminimalizálás + fizikai
   rögzítés. → keress: `IGAZOLATLAN PREMISSZA (§13.5):`
2. **`[ ]` A tanú-séma lépcsőnkénti alakja** — megírva, jóváhagyásra vár.
   → keress: `A tanú-kérdés (R1) NEM oldódott meg`
3. **`[ ]` A kockázatvállalás rögzítése** — javaslat megírva, jóváhagyásra vár:
   a „nincs tartalék szerver" tény kerüljön be a konfigurációba (mikor, ki
   tájékoztatta), és az admin felület **állandóan** mutassa a hely védelmi
   szintjét. Indok: az informált kockázatvállalás csak akkor véd, ha **adat**, nem
   beszélgetés. → keress: `informált kockázatvállalás`
4. **`[ ]` Az árva tranzakciók elétárásának időzítése** — javaslat megírva.
   → keress: `A4/c`

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

### 2.2 `[MÁR CSAK RÉSZLETEK BLOKKOLJÁK]` E1 — fázisterv

**A fázisterv még nincs megírva.** → `NYITOTT_KERDESEK.md:585`

- **Megállapított tény:** nincs konkrét, névre szóló első fizető ügyfél.
- **Munkafeltételezés** (felülvizsgálandó, amint van ügyfél): kis bár / büfé, 1–2
  pénztár, pincér nélkül. **FIGYELEM:** ezt a munkafeltételezést a 2. munkamenet
  döntései feszítik — lásd 1.1 szakasz 1. pontja (minimum 2 dedikált gép).
- **Mi hiányzik még hozzá:** a 2.1 négy részletkérdése közül az 1. (egypénztáras
  hely) és a 3. (mikor cseréljünk szerepet) érdemben befolyásolja a scope-ot.
  A 2. és a 4. nem — azok a fázistervvel párhuzamosan is eldönthetők.

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
| **C11** | 24 órás NTAK limit, 18 órás riasztás | A 19. pont SLA-figyelmeztetése |
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
