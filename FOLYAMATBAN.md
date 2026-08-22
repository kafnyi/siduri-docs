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

**Utolsó frissítés:** 2026-08-22
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

**Ha a `siduri_spec_hu.md` / `siduri_superprompt_en.md` ellentmond a
`NYITOTT_KERDESEK.md`-nek, a `NYITOTT_KERDESEK.md` nyer.** A két spec fejlécében ez
ki van írva, és a felülírt bekezdések inline meg vannak jelölve.

---

## 1. Mi KÉSZ

Öt blokkoló döntés lezárva a 2026-08-22-i munkamenetben. **Mindegyik indoklással
együtt** olvasandó — indoklás nélkül a döntések nem tapadnak meg, és a következő
kör újratárgyalja őket.

| Tétel | Döntés | Hol (`fájl:sor`) |
|-------|--------|------------------|
| **A1** | WPF marad; **Windows 10 IoT Enterprise (LTSC) only**, Linux törölve | `NYITOTT_KERDESEK.md:22` |
| **A2** | **Szerver-autoritatív + degradált gyorseladás** a POS-on. Cache + append-only outbox, **nem** PG replika | `NYITOTT_KERDESEK.md:40` |
| **A2/a** | Kettős kieséskor a **nyitott asztalok nem elérhetők** → kézi újrafelütés | `NYITOTT_KERDESEK.md:77` |
| **B3** | J1900 **vegyes bázis** (szerver ÉS kliens) → **GraalVM kényszer marad**, plusz szoros WPF perf-költségvetés | `NYITOTT_KERDESEK.md:256` |
| **E2** | 2–3 fős csapat + AI → **B8 az első hét tétele**, nem opcionális | `NYITOTT_KERDESEK.md:494` |

Ezen felül: új **F) szakasz** hét tétellel (`NYITOTT_KERDESEK.md:523`), ami egyik
eredeti doksiban sem szerepelt.

---

## 2. A KÖVETKEZŐ TÉTEL

### 2.1 `[FELHASZNÁLÓI DÖNTÉST IGÉNYEL]` B1 — HA / failover

**Állapot:** a javaslat **meg van írva**, a felhasználó azt kérte, „beszéljük még át".
**Nincs elfogadva. Erre építeni tilos.**

- Javaslat: `NYITOTT_KERDESEK.md:190`
- Kapcsolt tétel, **együtt döntendő**: **A4** kétszintű failback → `NYITOTT_KERDESEK.md:160`
- Nyitott **üzleti** kérdés benne (nem mérnöki, §12): az Emergency Server a specben
  **eladási érvként** szerepel; ha kikerül az MVP-ből, az a **termék pozicionálását**
  érinti → `NYITOTT_KERDESEK.md:243`

**A javaslat öt pontja dióhéjban** (a részletek és az indoklás a fenti soron):
1. Az A2 döntés **átrendezte a B1 tétjét** — az Emergency Server már kényelmi
   funkció, nem katasztrófavédelem.
2. Mindkét spec **fogalmi csúszása**: az USP az *internetkimaradás* elleni védelem;
   az Emergency Server viszont *hardverhiba* ellen véd. Más esemény.
3. Javaslat: **HA ki az MVP-ből**, de az **epoch-mező be a protokollba** az 1. naptól.
4. A „szinkron replikáció, ami automatikusan aszinkronra vált" **csapda** (§5 néma
   kudarc): pont akkor írsz védtelenül, amikor azt hiszed, védve vagy.
5. **Kézi** failover, jogosultsághoz kötve (nem szerephez); a biztonsági háló az A2
   degradált módja.

### 2.2 `[BLOKKOLVA A B1 ÁLTAL]` E1 — fázisterv

**A fázisterv még nincs megírva.** → `NYITOTT_KERDESEK.md:467`

- **Megállapított tény:** nincs konkrét, névre szóló első fizető ügyfél.
- **Munkafeltételezés** (felülvizsgálandó, amint van ügyfél): kis bár / büfé, 1–2
  pénztár, pincér nélkül.
- **Miért a B1 után:** ha a HA kikerül az MVP-ből, az több hét különbség a tervben.

---

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

## 3.1 `[?]` MÉRÉST IGÉNYEL, nem becsülhető (§4)

- **Failover adatvesztési ablak** J1900-on → `NYITOTT_KERDESEK.md:231`
- **WPF kliens teljesítménye** J1900-on: 720p másodkijelzős videó + teljes képernyős
  POS UI, 4 GB RAM mellett → `NYITOTT_KERDESEK.md:256`
- **PostgreSQL memórialimitek** (`shared_buffers`, `work_mem`, `max_connections`)

Mindháromhoz **fizikai J1900 referenciagép kell** — beszerzési tétel, felvéve az
E3-hoz (`NYITOTT_KERDESEK.md:511`).
**Semmilyen teljesítmény- vagy adatvesztési vállalás nem tehető mérés előtt.**

---

## 4. Miért nem kódolunk még

A felhasználó explicit kérése: *„kódolni egyelőre nem kell, még csak tárgyaljuk át a
projectet és véssük kőbe a végleges, mindenre kiterjedő, nagyon pontos tervet."*

Ezen felül mérnöki okból is korai:
- két blokkoló döntés nyitva (B1, E1),
- öt igazolatlan premissza (3. szakasz),
- és **B8** — az API-szerződés helye — még nincs eldöntve
  (`NYITOTT_KERDESEK.md:331`), ami 2–3 fős, három nyelvű csapatnál az **első hét**
  tétele. Ha kód születik előtte, a varrat (§6) már szétcsúszott mire észrevesszük.

---

## 5. Repó- és git-állapot — FONTOS FIGYELMEZTETÉS

**Ez a munka NINCS biztonságban.**

- A `Siduri-Docs` submodule „remote"-ja egy **lokális útvonal ugyanezen a gépen**:
  `W:\Wurfel_Obsidian_Safe\Siduri\Siduri-Docs`.
- A **parent repónak egyáltalán nincs remote-ja.**
- **GitHub sehol nincs a képben.** A `git push` lefut, de **nem mentés**.

§10 („a részeredményt commitold ÉS pushold — az ephemer környezet bármikor
elmehet, és a távoli branch az egyetlen igazságforrás") **nem teljesül**: minden
példány egy gépen, egy meghajtón van. Ha ez nem tudatos döntés, **GitHub remote-ot
kell beállítani, mielőtt a terv tovább nő.**

**Branch:** `claude-coding` (submodule és parent egyaránt).

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
4. A soron következő munka: **B1 lezárása a felhasználóval** (2.1 szakasz), majd
   **E1 fázisterv** (2.2).

**Ha egy tétel eldől:** jelöld `[ELDÖNTVE — <döntés>]`-ként a
`NYITOTT_KERDESEK.md`-ben, **az indoklással együtt**, frissítsd a prioritási táblát
és ezt a fájlt — majd commitold. Sehol máshol ne vezess párhuzamos döntéslistát
(§2.4).
