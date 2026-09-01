# Siduri — Fázisterv (E1)

**Utolsó frissítés:** 2026-08-23 (első ügyfél megvan: étterem, teljes funkcionalitással)
**Előfeltétel:** a teljes specifikáció lezárva (`siduri_spec_hu.md`), 57 invariáns rögzítve.

---

## 0. Mi ez a dokumentum, és mi NEM

**Ami:** a munka **sorrendje**, a **függőségei**, és fázisonként a **kilépési
feltétel** — vagyis mikor mondhatjuk ki, hogy egy fázis kész.

**Ami NEM: naptár.** És ezt nem lustaságból nem adom meg.

> **A projekt átfutási idejét nem a fejlesztés határozza meg, hanem három külső
> kapu, és egyik lead time-ját sem ismerjük.** Amíg ezek nincsenek meg, minden
> dátum kitalált szám lenne — és pont az a fajta hamis kényelem, amit végig
> kerültünk. **A terv abban a pillanatban naptárrá válik, amint a kapuk
> átfutási ideje megvan.**

**Alapfeltevés (a felhasználótól):** **a csapatlétszám nem korlát.** Ezért a terv
**párhuzamos sávokra** épül, nem egyetlen szekvenciára. Ahol mégis sorrend van,
ott az **valós függőség**, nem kapacitáshiány.

---

## 1. A három kapu, ami a naptárat adja

| # | Kapu | Mit blokkol | Mikor kell elindítani | Lead time |
|---|------|-------------|----------------------|-----------|
| **K1** | **Gyártói kapcsolat + fizikai tesztkészülék** | A fiskális réteg **véglegesítését** (a fejlesztést nem) | **Ma** | `[ISMERETLEN]` — eddig egyetlen, szöveg nélküli e-mail |
| **K2** | **MTÜ Igazolás + NTAK validációs teszt** | Az **élesítést**. Enélkül egyetlen ügyfél sem indulhat | **Ma** | `[ISMERETLEN]` — meg kell kérdezni |
| **K3** | **Fizikai J1900 referenciagépek** | Az **M1–M9, M12–M14, M19 méréseket**, és ezen keresztül a HA-terv és a topológia igazolását | **Ma** | beszerzési idő, hetek |

**K3 két lépcsőben kell:**

| Lépcső | Mi | Mikor |
|--------|-----|------|
| **K3/a** | **Egy i5-osztályú gép** (szerver-oldal) + **egy J1900** (a leggyengébb kliens ellenőrzésére) + **egy Fiscat eszköz** (`iPalm` vagy `Neon+`, amilyen az ügyfélnél van). ⚠️ **Az ügyfél gépein fejleszteni és mérni NEM lehet** -- az egy élő étterem | Az F1 fázishoz -- ez a legkorábbi valós blokkoló |
| **K3/b** | **Teljes referencia-telepítés**: 3 Windows POS + 2 tablet + 4 telefon + KDS + rendeléskijelző | Az M12-höz, az F6 fázis előtt |

> **A K3/a beszerzése az egyetlen dolog, ami MA elindítható, kevés pénzbe kerül,
> és azonnal felszabadít.** Enélkül az F1 kilépési feltétele nem teljesíthető.

---

## 2. Miért ebben a sorrendben — kockázat-kioltás, nem funkciólista

A fázisok sorrendje **nem a funkciók fontossága szerint** áll, hanem aszerint,
**mi tudja megölni a projektet, és azt mikor derítjük ki.**

| # | Kockázat | Ha kiderül, mi omlik | Mikor derül ki ebben a tervben |
|---|----------|----------------------|-------------------------------|
| **R1** | **A P1 premissza hamis** — az adóügyi eszköz mégsem önállóan állítja ki és sorszámozza a bizonylatot | **A teljes degradált mód** (§6.2), és vele az USP fele | **F1 vége** — 3. hét, nem 6. hónap |
| **R2** | **J1900-on nem fér el szerver + POS egyszerre** | A teljes topológia és az árazás alsó szintje | **F1 vége** (M1) |
| **R3** | **A tartalék POS nem bírja az átvételt csúcson** (M12) | A teljes HA-terv | **F4 vége** (M13, az M12 olcsó előjátéka) |
| **R4** | **Nincs gyártói partnerkapcsolat** | A fiskális réteg lezárása | K1, folyamatos |
| **R5** | **A tanúsítás tovább tart, mint hittük** | Az élesítés | K2, folyamatos |
| ~~R6~~ | ~~Nincs névre szóló első ügyfél~~ | — | **MEGOLDVA: az első ügyfél egy étterem (§7)** |
| **R7** | **Az első ügyfél MINDENT használ** → nincs fokozatos szállítás, az F2–F8 mind kötelező, és **a pilot egy élő étterem** | Az élesítés csúszik, a tanulási ciklus hosszú | **Ismert, §7.2** |

> **A vezérelv: ami meg tudja ölni a tervet, azt a legolcsóbb pillanatban kell
> kideríteni.** Egy hamis P1-et a 3. héten megtudni kellemetlen; a 6. hónapban
> katasztrófa.

---

## 3. Sávok

| Sáv | Mi | Repó |
|-----|-----|------|
| **A — Telephelyi mag** | Backend + POS kliens | `siduri-backend-server`, `siduri-pos-client` |
| **B — Felhő** | Licenc, archívum, webes admin, statisztikák | `siduri-cloud-api` |
| **C — Vékonykliensek** | PDA, KDS, rendeléskijelző, standoló | `siduri-flutter-clients` |
| **D — Telepítés és üzemeltetés** | Frissítő, telepítő, ellenőrzőlista | `siduri-updater` |
| **E — Kapuk** | Gyártó, MTÜ/NTAK, hardver, könyvelő | *(nem fejlesztés)* |

**Minden sáv az API-szerződéstől függ** — ezért az az első dolog, ami elkészül.

---

## F0 — Kapunyitás `MA INDUL, VÉGIG FUT`

Nem fázis, hanem **folyamatosan futó sáv**. Nincs kilépési feltétele; a többi
fázis kilépési feltételei hivatkoznak rá.

| # | Feladat |
|---|---------|
| F0.1 | **Prior Cash: valódi kapcsolatfelvétel** — bemutatkozás, integrációs szándék, **partneri megállapodás**, és mindenekelőtt **fizikai tesztkészülék**. Kérdésekkel együtt: nulla összegű tétel, DRS-gyűjtő, AJT-rekesz újrakiosztása, a szolgáltatás hitelesítése/IP-korlátozása |
| F0.2 | **MTÜ / NTAK: a tanúsítási folyamat elindítása**, és mindenekelőtt **a lead time megkérdezése**. Plusz a négy nyitott kérdés (napi zárás utáni rendelésösszesítő, személyzeti fogyasztás, múltbeli zárási időbélyeg, utalvány-besorolás, szétbontott számla) |
| F0.3 | **Hardver: K3/a beszerzése** — 2 db J1900 + 1 adóügyi eszköz |
| F0.4 | **Könyvelői kérdéssor**: borravaló adózása, előleg áfakulcsa vegyes fogyasztásnál |
| F0.5 | **Első ügyfél / tervezőpartner keresése** — lásd §7, ez a legalábbecsültebb tétel |

---

## F1 — Csontváz és kockázat-kioltás

**Cél:** nem funkció, hanem **bizonyíték.** A fázis végén tudni fogjuk, hogy a
technológiai alap és a legfontosabb premissza áll-e.

### Mi épül

| # | Tétel | Miért itt |
|---|-------|-----------|
| F1.1 | **API-szerződés (B8):** hol él, hogyan verziózzuk, ki a gazdája | **Minden sáv erre épül.** Kis csapatnál sem opcionális |
| F1.2 | **Pénztípusok** (egész forint / nagy pontosságú egységköltség), lebegőpont tiltva | I1–I2. Utólag átírni az egész rendszert érinti |
| F1.3 | **Bizonylat-számozás**: eszközönként elhatárolt tartomány, üzletinap-előtag, nullázható adóügyi mező | I13–I14. **Szerkezet, nem funkció** — utólag nem tehető bele |
| F1.4 | **Epoch (fencing) mező a protokollban** | A HA az F6-ban jön, **de a mező az első naptól kell** |
| F1.5 | **Helyi outbox** (csak-hozzáfűzhető, tartós) | A degradált mód és a nyomtatási szándékrögzítés is erre ül |
| F1.6 | **Audit napló csontváza**: két áram, csak-hozzáfűzhető, adatbázisszinten kikényszerítve, hash-lánc a biztonsági ágon, UUID-hivatkozás | I24–I25, I35. Utólag beépíteni ugyanaz, mint utólag naplózni |
| F1.7 | **Monoton óra + óraszinkron váz** | I15–I17 |
| F1.8 | **A legvékonyabb függőleges szelet:** egy termék → kosár → készpénzes fizetés → **nyomtatás VALÓDI adóügyi eszközre** |
| F1.9 | **Mindez EGY J1900-on**, szerver és kliens együtt, GraalVM natív image + PostgreSQL + WPF |

### Kilépési feltétel — éles, nem puha

| # | Feltétel |
|---|----------|
| ✅ | **A P1 premissza IGAZOLVA vagy MEGDŐLVE, írásban.** Az adóügyi eszköz szerver nélkül is kiállítja és sorszámozza a bizonylatot? |
| ✅ | **Egy valódi bizonylat, valódi eszközön, valódi J1900-on kinyomtatva** |
| ✅ | **M1 mérve** (kombinált szerver + pénztárgép egy gépen) |
| ✅ | **M15 mérve** (nulla összegű tétel — elfogadja-e a firmware) |
| ✅ | **M17 mérve** (nyomtatási ciklusidő) |
| ✅ | **Az API-szerződés létezik és verziózott** |

> **Elágazás:** ha **P1 hamis**, a degradált mód (§6.2) **újratervezendő**, az
> USP kommunikációja változik, és az F6 hatóköre más lesz. **Itt megállunk és
> újratervezünk** — nem megyünk tovább feltevésre.

---

## F2 — Az eladás magja `MVP`

**Cél:** egy **egygépes hely jogszerűen tudjon kereskedni.** Ez egyben az ingyenes
belépő szint terméke.

| Terület | Tartalom |
|---------|----------|
| **Terméktörzs** | Kategóriák (max 4 szint, alulról öröklődő áfa-alapérték) · **két áfamező másolás-szemantikával** · kemény kapu hiányos áfánál · kiszerelések · ártörténet · életciklus (aktív / inaktív / soft delete) |
| **Ár és pénz** | Bruttó alapú számolás · **áfakulcs-csoportonkénti visszaszámolás bizonylatszinten** · **az ár a sor létrehozásakor rögzül** (I42) · kerekítés csak a készpénzes részre · EUR |
| **Eladás** | Gyorseladás · fizetési módok · vegyes fizetés · **számlamegosztás** · kedvezmény (áfa-arányos szétosztással) · **szervizdíj áfakulcsonként bontva** · borravaló |
| **Bizonylat** | Sztornó vs. törlés · **számla–nyugta kölcsönös kizárás, mindkét útvonallal** · „NEM ADÓÜGYI BIZONYLAT" jelölés |
| **Nap** | MUNKANAP a 23:45-ös vágással, **abszolút alapon mérve** · MŰSZAK · automatikus napzárás az előfázissal és a kötelező szünettel · **vakzárás** · címletkalkulátor |
| **Fiskális** | Gyűjtőkiosztás · tételtípusok (áras / ár nélküli szövegsor / levonó külön úton) · a kliens nyomtat, a szándék **helyben** rögzül |
| **Jogosultság** | Szintek, szerkeszthetően · **sérthetetlen Siduri admin** · fix offline belépés · PIN + RFID |
| **Audit** | Mindkét áram élesben, indokkódokkal |

**Kilépési feltétel:** egy egygépes telephely **valós forgalmat tud bonyolítani**
jogszerű bizonylatokkal. *(NTAK nélkül még — az az F3.)*

---

## F3 — NTAK `MVP` · *párhuzamos az F2 második felével*

| # | Tétel |
|---|-------|
| F3.1 | **Rendelésösszesítő, 15 percenként**, paraméterezhető ütemmel |
| F3.2 | **Tartós, sorrendtartó, átfedésmentes kimenő sor** — ugyanolyan elsőrangú, mint a bizonylat-outbox |
| F3.3 | **Feldolgozási nyugta lekérdezése** 24 órán belül, tárolással *(új, önálló folyamat)* |
| F3.4 | **Napi zárás**, tárgynap a nyitás dátumából, `zaras − nyitas <= 24 óra` betartva |
| F3.5 | **Nyitvatartási minta** + **visszamenőleges** zárva/forgalom nélküli nap küldés *(soha nem előre — I18)* |
| F3.6 | **Kategóriák, egységek, áfakulcsok KONFIGURÁCIÓBÓL**, nem kódból (I-szabály: az ENUM változhat) |
| F3.7 | **`osszesitett` degradált útvonal** okkóddal |
| F3.8 | Mennyiségi egység + kiszerelési mennyiség a terméktörzsben |

**Kilépési feltétel:** **a validációs teszt sikeres.** *(A K2 kapu része.)*

---

## F4 — Vendéglátás `MVP`

| Terület | Tartalom |
|---------|----------|
| **Asztal** | Asztaltérkép-szerkesztő · asztalnyitás, vendégszám · felszolgáló · asztal-szintű kedvezmény · optimista zárolás |
| **Rendelés** | Nézetek (felütés / vendég / fogás) · előnyugta és „fizetésre vár" |
| **Fogások** | **Fogás-címke + „következő fogás indítása"** · a KDS lássa a visszatartottakat |
| **Módosítók** | Csoportok, `min`/`max`, **FreeLimit háromállású ingyenes-választással** · levonó módosító anyagra hivatkozva · **minden módosító nyomtatódik** |
| **Menü** | Menükomponensek, párosításonkénti felár, **szétrobbantás egész forintos arányosítással** |
| **KDS** | Állapotváltás, a rendeléskijelző triggerelése |
| **Vékonykliens** | Rendelésfelvétel · **fizetés megépítve, szerveroldali jogosultsággal kikapcsolva** · minimális archívum |
| **Több gép** | Eszközszám-tartományok élesben · nyomtatási routing teljes körben |

**Kilépési feltétel:**
✅ Asztalkiszolgálásos étterem működik ·
✅ **M13 mérve** (a tartalék POS terhelése normál üzemben, csak replikaként)

> **Az M13 KAPU az F6 felé.** Ha a replika-terhelés már normál üzemben elviszi a
> válaszidőt, akkor **az M12 értelmetlen, és a HA-tervet újra kell gondolni,
> mielőtt megépítjük.**

---

## F5 — Készlet és admin `MVP` · *párhuzamos az F4-gyel*

| # | Tétel |
|---|-------|
| F5.1 | Raktárak, raktárközi mozgás bizonylattal |
| F5.2 | Receptúra (BOM), **levonó módosító visszaírja a készletet** |
| F5.3 | Bevételezés, **bruttó + kötelező beszerzési áfakulcs**, **mozgóátlagár a negatív bázis külön kezelésével** |
| F5.4 | **A készlet soha nem blokkol eladást**; a kézi „elfogyott" jelző igen |
| F5.5 | Leltár korrekciós mozgásként, fordulónapi elszámolással, kalkulált veszteség %-kal |
| F5.6 | Selejt és személyzeti fogyasztás **készletmozgásként** |
| F5.7 | **Webes admin — EGY alkalmazás, a telephelyi szerverről is kiszolgálva** (30 napos offline korláttal, kiírva) |
| F5.8 | Árrés-riportok **nettó alapon, teljesítési módonként bontva** |

---

## F6 — Magas rendelkezésre állás és degradált mód `MVP`

> **Miért ilyen későn:** a HA egy olyan rendszert véd, aminek előbb léteznie kell,
> és az M12 a **teljes referencia-telepítést** igényli. **A szerkezetek viszont
> már az F1 óta bent vannak** (epoch, számozási tartományok, outbox) — itt a
> **mechanizmus** épül rájuk, nem az alap.

| # | Tétel |
|---|-------|
| F6.1 | **Outbox visszajátszás és visszatéréskori egyeztetés** |
| F6.2 | Replikáció · **WAL-slot lemezalapú korlátozása + hangos jelzés + a teljes újraszinkronizálás útja** |
| F6.3 | **Tanú-séma**, öndiagnózis-létra, a „ki esett ki" felismerés (**kölcsönös hitelesítéssel** — a belső hálózat nem megbízható) |
| F6.4 | **Kétlépcsős failover**, 5 perces ajánlat monoton időmérőn, lejáró ajánlattal, idempotens átvétellel |
| F6.5 | **Fencing kikényszerítése a KLIENSEN is** — régebbi epochú szerverrel tilos beszélni |
| F6.6 | **Automatikus visszaállás** 1 perc stabil kölcsönös láthatóság után, billegés-védelemmel |
| F6.7 | **Árva tranzakciók: karanténsor + Siduri támogatói feloldó felület** (az ügyfél látja, hogy van, de nem oldhatja fel) |
| F6.8 | Degradált mód teljes felülete és személyzeti üzenetei |

**Kilépési feltétel:** ✅ **M4, M5, M6, M7, M12, M13, M19 mérve** · ✅ **M12
sikeres** — a tartalék POS csúcsterhelés alatt átveszi a szolgálatot.

---

## F7 — Felhő `MVP` · *önálló sáv, korán indul*

| # | Tétel |
|---|-------|
| F7.1 | Licenc, heartbeat (10 nap), **hardveres ujjlenyomat**, két ujjlenyomat egy azonosítón → mindkettő tiltva |
| F7.2 | **Archívum (8 év)** + **audit hash-horgonyzás** |
| F7.3 | **Webes admin kiszolgálása** (ugyanaz az alkalmazás, mint az F5.7) |
| F7.4 | Több telephely, lánc/franchise, **zárolható beállítások**, visszajelzés a leérkezésről, eszköz-láthatóság |
| F7.5 | **Felhő HA:** két fizikai szerver, automatikus átcsatornázás, aktív-passzív írás |
| F7.6 | **Lejárat-figyelő**: NTAK-tanúsítvány, licenc, API-kulcsok — 60/30/14/7/1 nap |
| F7.7 | **Zárva tartás alatti NTAK-küldés**, ha a telephelyi szerver ki van kapcsolva |
| F7.8 | Kockázatvállalási nyilatkozat tárolása **SHA-256 lezárással** |
| F7.9 | **Támogatói felület**: árva tranzakciók, nyers audit, tartós integráció-kikapcsolás |

---

## F8 — Élesítés

| # | Tétel |
|---|-------|
| F8.1 | **MTÜ Igazolás + validációs teszt** *(K2)* |
| F8.2 | **Telepítési ellenőrzőlista élesben**: vendég-wifi szétválasztás · Windows Update újraindítás letiltva · TPM-ág megállapítva · fizikai rögzítés |
| F8.3 | **Frissítési sorrend** kikényszerítve (a szerepet vivő gépek nem frissülnek egyszerre) |
| F8.4 | **Pilot telephely**, felügyelt üzem |
| F8.5 | **AZ ELSŐ ÉLES TESZTEN MINDENT MÉRÜNK** — a teljes `MERESEK.md` |
| **F8.6** | **ÁTÁLLÁSI TERV** — adatmigráció, csendes időpont, visszaállási terv, **NTAK-váltás kettős jelentés nélkül**, felügyelt üzem. Részletek: **§7.4** |

---

## 4. Kritikus út

```
K3/a hardver ──► F1 ──► [P1 elágazás] ──► F2 ──► F3 ──► K2 tanúsítás ──► F8 élesítés
                                             │
                                             ├──► F4 ──► [M13 kapu] ──► F6
                                             └──► F5
F7 (felhő) ──────────────────────── önálló sáv, az F5.7-nél találkozik ─────►
K1 gyártó ─────────────────────── a fiskális réteg lezárásáig fut ─────────►
```

**A kritikus úton három dolog van, és egyik sem kód:**

| # | Elem | Miért kritikus |
|---|------|----------------|
| 1 | **K3/a hardver** | Az F1 kilépési feltétele mérésekhez kötött |
| 2 | **K2 tanúsítás** | Az élesítés kapuja, ismeretlen lead time-mal |
| 3 | **K1 gyártói kapcsolat** | A fiskális réteg lezárásának kapuja |

> **Ha holnap kétszer annyian dolgoznánk rajta, a projekt nem lenne feleannyi
> idő** — mert a kritikus úton külső átfutási idők állnak. **Ezért kell a K1–K3-at
> ma elindítani, nem akkor, amikor odaérünk.**

---

## 5. Amit ma el lehet kezdeni, nulla külső függőséggel

| # | Feladat | Sáv |
|---|---------|-----|
| 1 | **API-szerződés** (F1.1) — hol él, verziózás, gazda | A |
| 2 | **Adatmodell**: pénztípusok, bizonylat-számozás, epoch, audit-váz | A |
| 3 | **Felhő alapok**: licenc, archívum-séma, hitelesítés | B |
| 4 | **UI/UX kör** a `UiUX/` skill-készlettel — **német szövegekkel tesztelve** | A, C |
| 5 | **Telepítési ellenőrzőlista** megírása | D |
| 6 | **Kapulevelek megírása és elküldése** (F0.1, F0.2, F0.4) | E |

---

## 6. Amit tudatosan NEM viszünk az MVP-be

| Terület | Címke | Miért |
|---------|-------|-------|
| e-pénztárgép (3. fiskális üzemmód) | `v2` | Az AEE-s út a jelenlegi cél |
| DRS visszaváltás (göngyölegvisszavétel) | `v1/v2` | A hely nem kötelezett visszaváltóhely lenni |
| Utalványok | `v1` | Nem blokkolja a kereskedést |
| Előleg / asztalfoglalás | `v1` | Ugyanaz |
| Allergének | `v1` | **Opcionális kiegészítő funkció**, kevesen használják |
| 18+ piktogram | `v1` | Ugyanaz |
| Mérleg és tára | `v1` | Szűk termékkör |
| Kioszk, QR-rendelés, rendeléskijelző | `v1/v2` | Nem a kereskedés magja |
| Kiszállítás mint teljesítési mód | `v1` | Az elviteli áfamező már megvan |
| Kasszafiók-szenzor | `v2` | Hardverfüggő, kicsi érték |
| Offline pendrive-mentés | `v2` | Szűk célcsoport *(kivéve, ha fesztivál a célpiac — akkor `v1`)* |
| Nyomtatás-átirányítás másik eszközre | `v1` | Az „gépenként egy eszköz" ajánlás ezt ritkává teszi |
| Külső API (kiszállító platformok, CRM) | `v2` | — |

---

## 7. Az első ügyfél — ami eldőlt, és ami ettől nehezebb lett

> **Az első ügyfél egy ÉTTEREM, aki gyakorlatilag MINDEN tervezett megoldást
> használni fog.**

### 7.1 Amit ez megold

A korábbi legnagyobb kockázat — *„nincs névre szóló első fizető ügyfél, tehát az
MVP-definíció egy fogadás"* — **megszűnt.** A hatókör mostantól **tény**, nem
feltevés. A **D6 döntési pont tárgytalan.**

### 7.2 Amit ez elront — és ezt ki kell mondani

**Megszűnt a fokozatos szállítás lehetősége.**

Eddig volt egy olcsó út: az egygépes, asztalkezelés nélküli szint önmagában
szállítható termék, amivel korán élesbe lehet menni és tanulni. **Egy étterem
ezzel nem tud mit kezdeni.** Ott az első éles nap az, amikor **egyszerre** kell
működnie az asztalkezelésnek, a fogásoknak, a módosítóknak, a menüknek, a
KDS-nek, a készletnek, a receptúrának, a több gépnek, a fiskális rétegnek, az
NTAK-nak és a felhős adminnak.

**Négy konkrét következmény:**

| # | Következmény |
|---|--------------|
| 7.2.a | **Az F2–F8 mind kötelező** az első élesítés előtt. Semmi nem halasztható |
| 7.2.b | **A HA nem opció, hanem kötelező.** Egy éttermi telepítés jellemzően 4+ gép → a saját méretosztály-szabályunk szerint a **tartalék szerver kötelező ajánlás** (§5.1) |
| 7.2.c | **A tanulási ciklus hosszabb lett.** Az első visszajelzés nem az F2 után jön, hanem az F8-ban |
| 7.2.d | **A pilot egy ÉLŐ étterem** — ott nem lehet kísérletezni szerviz közben |

### 7.3 A fázisok sorrendje ettől NEM változik — de a jelentése igen

**Fontos, hogy ezt ne értsük félre:** attól, hogy mindent szállítani kell,
**a kockázat-kioltó sorrend nem lesz értéktelen — sőt.**

> **Az „szállítható" és a „megépítendő" nem ugyanaz.** Az F1 továbbra is a
> legkockázatosabb premisszát oltja ki 3 hét alatt 6 hónap helyett; az M13 kapu
> továbbra is megmenti a HA-terv újraépítését. **Csak a „kimehetünk vele élesbe"
> pont csúszik a végére.**

**Egy változás viszont van:** az **F4 (vendéglátás)** és az **F5 (készlet)**
korábban „párhuzamos, ha jut rá kapacitás" volt. **Most mindkettő kritikus úton
van**, és az F5.7 (webes admin) is, mert az étterem a receptúrát és a készletet
az első naptól használni fogja.

### 7.4 `[ÚJ, KÖTELEZŐ FÁZISELEM]` F8.6 — Átállási terv

**Egy működő éttermet nem lehet péntek este átkapcsolni egy új
kasszarendszerre.** Ez nem fejlesztési, hanem üzemeltetési feladat, és **eddig
egyáltalán nem szerepelt a tervben.**

| # | Elem | Miért |
|---|------|-------|
| 7.4.a | **Adatmigráció** a jelenlegi rendszerből: terméktörzs, árak, kategóriák, receptúra, készlet-nyitóérték | A terméktörzs kézi felvitele egy étteremben napok |
| 7.4.b | **Az átállás időpontja: csendes időszak** — hétfő reggel, vagy zárás utáni nap. **Soha nem forgalmas nap** | — |
| 7.4.c | **Visszaállási terv:** ha az első nap nem megy, mihez nyúlnak? **A régi rendszernek elérhetőnek kell maradnia**, amíg az új nem bizonyított | Enélkül az első hiba üzletbezárás |
| 7.4.d | ⚠️ **NTAK-átállás: a régi és az új szoftver EGYSZERRE nem jelenthet ugyanarról a forgalomról.** A váltás pillanatát pontosan meg kell határozni, és az NTAK-oldali szoftverregisztrációt hozzá kell igazítani | **Kettős adatszolgáltatás keletkezne** |
| 7.4.e | **Fiskális eszköz:** melyik eszközük van, és a gyártói szoftver telepíthető-e rá — **ezt az F1 előtt tudnunk kell**, mert ez határozza meg, milyen készüléken mérünk | A K1/K3 kaput konkretizálja |
| 7.4.f | **Felügyelt üzem:** az első napokban fizikai jelenlét a helyszínen | — |

### 7.5 Amit az ügyféltől MOST meg kell kérdezni

Ez konkretizálja a K1 és K3 kaput, és részben az F1-et is:

| # | Kérdés | Mit befolyásol |
|---|--------|----------------|
| ~~1~~ | ~~Milyen adóügyi eszközük van?~~ -> **MEGVÁLASZOLVA: Prior Cash Fiscat `iPalm` és `Neon+` pénztárgépek + adóügyi nyomtatók.** A K1 kapu a jó gyártó felé mutat. **Két új lelet:** a pénztárgépen lehet Siduri nélkül is ütni (egyeztetés kell), és az ügyfél apránként e-pénztárgépre áll át, tehát **a fiskális üzemmód ESZKÖZ-szintű, nem telephely-szintű** | rendezve |
| 2 | **Hány gép, milyen szerepben?** Pénztár, pincér-eszköz, konyha, iroda | A topológia és a HA-méretosztály |
| 3 | **Milyen hardveren futnak most?** J1900, vagy más | K3 — ha nem J1900, a mérési alap változik |
| 4 | **Milyen rendszert váltanak le?** | Adatmigráció, NTAK-átállás |
| 5 | **Van-e már NTAK-adatszolgáltatásuk, milyen szoftverrel?** | 7.4.d — a kettős jelentés elkerülése |
| 6 | **Használnak-e receptúrát és készletet ma?** | Van-e migrálható adat, vagy nulláról indul |
| 7 | **Hány terméket kell felvinni?** | Az adatmigráció mérete |
| 8 | **Vendég-wifi és üzemi hálózat szét van választva?** | Kötelező telepítési előfeltétel (§10.6) |
| 9 | **Mikor van a legcsendesebb időszakuk?** | Az átállás időzítése |


## 8. Döntési pontok — hol állunk meg és tervezünk újra

| # | Mikor | Mit döntünk |
|---|-------|-------------|
| **D1** | **F1 vége** | **P1 igaz vagy hamis?** Ha hamis: a degradált mód és az USP újratervezése |
| **D2** | **F1 vége** | **M1 eredménye:** elbírja-e a J1900 a szerver + POS párost? Ha nem, a topológia és az árazás alsó szintje változik |
| **D3** | **F4 vége** | **M13 eredménye:** van-e értelme az M12-nek? Ha nincs, **a HA-terv újragondolása az F6 MEGÉPÍTÉSE ELŐTT** |
| **D4** | **K2 válasza megjön** | A tanúsítás lead time-ja alapján **a terv naptárrá válik**, és eldől, kell-e átcsoportosítani |
| **D5** | **K1 válasza megjön** | Ha nincs partnerkapcsolat, eldöntendő: várunk, vagy más gyártóval is felvesszük a kapcsolatot |
| ~~D6~~ | — | ~~Van-e tervezőpartner?~~ **TÁRGYTALAN — az első ügyfél megvan (§7)** |
| **D7** | **F1 ELŐTT** | **Az ügyfél tényleges felállása** (§7.5): milyen adóügyi eszköz, hány gép, milyen hardver, mit váltanak le. **Ez konkretizálja a K1 és K3 kaput** |

---

## 9. Fázisonkénti kilépési feltételek — összefoglaló

| Fázis | Kilépési feltétel |
|-------|-------------------|
| **F1** | P1 eldöntve írásban · valódi bizonylat valódi eszközön valódi J1900-on · M1, M15, M17 mérve · API-szerződés él |
| **F2** | Egygépes hely jogszerűen kereskedik |
| **F3** | **NTAK validációs teszt sikeres** |
| **F4** | Asztalkiszolgálásos étterem működik · **M13 mérve** |
| **F5** | Készlet, receptúra, leltár, webes admin él |
| **F6** | **M12 sikeres** — a tartalék POS csúcson átvesz · M4, M5, M6, M7, M19 mérve |
| **F7** | Licenc, archívum, admin, felhő-HA, lejárat-figyelő él |
| **F8** | **MTÜ Igazolás megvan** · pilot fut · a teljes mérési lista lezárva |
