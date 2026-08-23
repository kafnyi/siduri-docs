# MI AZ MVP — pontos definíció és címkekészlet

> **Kérte:** a felhasználó, 2026-08-22: *„kérlek írd ki, hogy mit értesz/jelent
> MVP alatt, hogy ne téveszthessem el."*
>
> **Ez a fájl az egyetlen hely, ahol az „MVP" szó jelentése definiálva van.**
> Ha bárhol a tervben „MVP" szerepel, **ezt kell alatta érteni.**

---

## 0. `[ELDÖNTVE]` A LÉTSZÁM NEM KORLÁT — és ami ettől MÉGIS korlát marad

**A felhasználó döntése (2026-08-22):** *„amennyiben szükség van a későbbiekben a
csapat bővítésére, azt majd megoldom… a létszám nem lesz szűk keresztmetszet,
nem is kell vele úgy számolni."*

**Elfogadva. A 2. ellenőrző kör `A1` leletét (a terv mérete vs. a 2–3 fős csapat)
ezzel LEZÁRTNAK tekintem**, és a továbbiakban nem hozom fel.

### `[!]` DE: öt dolog akkor sem gyorsul, ha holnap tízen leszünk

Ez nem az `A1` újranyitása, hanem **tényközlés** — mert **ha ezekkel úgy
számolunk, mintha létszámmal megoldhatók lennének, a terv ütemezése hibás lesz.**

| Mi | Miért nem segít rajta a létszám |
|---|---|
| **1. Külső kapuk** — MTÜ-validáció, a NAV-engedély kérdése, gyártói NDA | **Sorbaállás egy másik szervezetnél.** Tíz fejlesztő sem gyorsítja a hatósági átfutást. |
| **2. Sorrendi függés** | Az MTÜ-validációhoz **működő NTAK-modul kell.** Nem lehet párhuzamosítani azzal, amitől függ. |
| **3. A hardver igazsága** | Ha a J1900 nem bírja a kombinált szerep+POS terhelést, **több ember sem old meg semmit** — a telepítési modell dől. |
| **4. Külső dokumentáció megérkezése** | A gyártói protokoll nélkül a fiskális modul **nem tervezhető**, akárhányan vagyunk. |
| **5. `[!]` A varrat-kockázat NŐ a létszámmal** | Több ember → több párhuzamos munka **három nyelven, hat repóban** → **több néma szétcsúszás** (§6). **A közös API-szerződés és a paritás-őr nem opcionális lesz, hanem sürgősebb.** |

**Az 5. pont a legfontosabb:** a nagyobb csapat **nem semlegesíti** a
szétcsúszást, hanem **felerősíti.** A módszertan (§6, §9) erre való — és
**érdemben előrébb kerül**, amint többen leszünk.

### `[!]` És egy fogalmi váltás, ami ebből következik

**Amíg a létszám volt a korlát, a fázisolás oka az volt, hogy „ennyi fér bele".
Most, hogy nem az, a fázisolás oka MÁS lett** — és ez **jobb ok:**

> **Nem azért fázisolunk, mert kevesen vagyunk, hanem hogy
> A LEHETŐ LEGHAMARABB MEGTUDJUK, HOL TÉVEDTÜNK.**

Ebből az következik, hogy **az MVP-t nem a legkisebb munkára kell szabni, hanem
a legtöbb TANULÁSRA egységnyi munkára.** Konkrétan az MVP-nek **el kell érnie
azt a négy dolgot, amit csak élesben lehet megtudni:**
1. **bírja-e a hardver** (a telepítési modell igazsága),
2. **átmegyünk-e az MTÜ-validáción** (a piacra lépés feltétele),
3. **működik-e a fiskális integráció valós eszközzel** (a legdrágább ismeretlen),
4. **használható-e egy valódi pult mögött** (amit terv nem tud megmondani).

---

## 1. AZ MVP DEFINÍCIÓJA

> ### Az MVP a LEGSZŰKEBB olyan szállítás, amit egy VALÓDI, FIZETŐ vendéglátóhely a TELJES napi működésére használni tud — jogszerűen, biztonságosan, a mi jelenlétünk nélkül.

**A definíció négy szava hordozza a jelentést:**

### „VALÓDI, FIZETŐ" — nem demó, nem pilot, nem baráti teszt
Ha csak akkor működik, ha mi ott vagyunk, vagy ha az ügyfél „elnézi", hogy
valami hiányzik → **nem MVP.**

### „TELJES napi működés" — a nap KÖRE záruljon be
Munkanap nyitás → eladás → fizetés → bizonylat → Műszak zárás → Munkanap zárás →
riport → adatszolgáltatás. **Ha a körből EGY lépés hiányzik, a hely nem tudja
használni** — mert nem lehet „a nap 80%-át" lezárni.

### „JOGSZERŰEN" — ez a legkeményebb feltétel, és NEM fokozatos
**A megfelelésnek nincs „MVP-változata".** Egy bizonylat vagy szabályos, vagy
nem. Egy adatszolgáltatás vagy megtörtént, vagy nem.
**Nem lehet azt mondani, hogy „az MVP-ben még nem küldünk NTAK-ot".**
→ **Ha a célszegmens NTAK-köteles, az MTÜ-igazolás az MVP RÉSZE.**
→ Ha a célszegmens nyugtaadásra kötelezett, a fiskális integráció **az MVP része.**

### „A MI JELENLÉTÜNK NÉLKÜL" — a támogathatóság is MVP-feltétel
Ha egy hiba felderítéséhez ki kell menni, **nem MVP, hanem pilot.**
→ minimális távoli diagnosztika **az MVP része.**

---

## 2. AMI AZ MVP-BŐL KIMARADHAT — és ami SOHA nem

### Kimaradhat: a SZEGMENS szűkítése
**Az MVP-t nem a funkciók megnyirbálásával kell kicsivé tenni, hanem azzal, hogy
KEVESEBBFÉLE HELYET szolgál ki.**

| Szűkítés | Példa |
|---|---|
| **Üzlettípus** | csak bár/büfé — asztaltérkép, számlabontás, fogások nélkül |
| **Eszközszám** | csak 1–2 Windows POS, vékonykliens nélkül |
| **Fiskális mód** | csak EGY mód (lásd `FISKALIS_UZEMMODOK.md`) |
| **Telepítés** | csak egyfajta topológia |
| **Lánc** | egy telephely, franchise-szint nélkül |

**Ez a helyes irány**, mert a kiszolgált hely számára a rendszer **teljes**
marad — csak kevesebb féle helyet szolgálunk ki.

### `[!]` SOHA nem maradhat ki: a jogi és adatvédelmi teljesség
- szabályos bizonylat, helyes adókulcs, hiánytalan adatszolgáltatás,
- a megőrzés biztosítása,
- az adat elvesztésének kizárása,
- audit ott, ahol pénzt vagy jogot érint.

**Ezek nem funkciók, hanem a szállíthatóság feltételei.**

---

## 3. A CÍMKEKÉSZLET — öt címke, nem négy

A 2. ellenőrző kör négy címkét javasolt (`MVP`/`v1`/`v2`/`vízió`).
**Ez hiányos volt: kell egy ötödik, és az a legfontosabb.**

| Címke | Jelentése | Példa a jelenlegi döntésekből |
|-------|-----------|-------------------------------|
| **`ALAP`** | **`[!]` NEM fázis, hanem ELŐFELTÉTEL.** Az első kódsortól helyesen kell lennie, akkor is, ha a rá épülő funkció csak v2-ben jön. **Utólag beépíteni = mindent átírni.** | pénz- és mennyiség-ábrázolás; idempotencia-kulcs minden írásra; epoch-mező; a bizonylatszám szerkezete; az eladáskori ár/adó/név tárolása; az audit gerince; a beállítás-séma |
| **`MVP`** | Az 1. szakasz definíciója szerint az első fizető telepítéshez kell | egy fiskális mód végig; Munkanap/Műszak; NTAK + MTÜ-igazolás (ha a szegmens köteles); alap riport; távoli diagnosztika |
| **`v1`** | Az első **teljes** kiadás — a termék, ahogy hirdetni akarjuk | asztaltérkép, számlabontás, PDA, KDS, raktár, receptúra, felhős admin |
| **`v2`** | Vállalt, de későbbi | franchise/lánc, BI-mélység, külső integrációk, kioszk, QR-rendelés |
| **`VÍZIÓ`** | **Irány, NEM kötelezettség.** Ha soha nem valósul meg, senki nem sérül | összetett archiválási optimalizáció, hűségprogram, többnyelvűség |

### `[!]` Miért az `ALAP` a legfontosabb címke

**Mert ez az egyetlen, amit NEM lehet elhalasztani.**
Az egész eddigi munkamenet legerősebb visszatérő érve ez volt: *„most olcsó,
később drága."* **Ezek a döntések nem fázisba tartoznak, hanem alá.**

**Ha egy döntést `ALAP`-nak címkézünk, az azt jelenti: a fázisterv nem
rendelkezhet róla — csak arról, hogy MIKOR épül rá funkció.**

---

## 4. Hogyan használjuk — három szabály

1. **Minden lezárt döntés PONTOSAN EGY címkét kap.** Ha nem egyértelmű,
   az azt jelenti, hogy a döntés **két különböző dolgot kever** → szét kell
   szedni.
2. **`[!]` Az `MVP` címkék összege legyen ELLENŐRIZHETŐ az 1. szakasz definíciója
   ellen:** be lehet-e zárni velük a napi kört, jogszerűen, jelenlét nélkül?
   **Ha nem, akkor vagy hiányzik egy MVP-tétel, vagy a szegmenst kell szűkíteni.**
3. **Az `ALAP` címkéket a fázisterv NEM ütemezi** — azok minden fázisban
   érvényesek, az első kódsortól.

---

## 5. `[ ]` Amit a definícióból következően EL KELL DÖNTENI

A definíció **nem alkalmazható**, amíg ezek nyitva vannak — mert a jogi
teljesség és a napi kör bezárása **szegmensfüggő:**

| # | Kérdés | Miért az MVP-t dönti el |
|---|--------|-------------------------|
| **1** | **Melyik SZEGMENS az MVP célja?** (bár/büfé, étterem, lánc) | Ebből következik, mi a „teljes napi kör" |
| **2** | **NTAK-köteles-e az a szegmens?** | Ha igen, **az MTÜ-igazolás az MVP része** — ez a leghosszabb átfutású tétel |
| **3** | **Melyik fiskális mód az MVP-ben?** | Mindhárom kiépítése nagyságrenddel több; egy is elég egy szegmenshez |
| **4** | **Van-e vékonykliens az MVP-ben?** | Eldönti, kell-e a Flutter-ág egyáltalán az első körben |

**Ez a négy kérdés a fázisterv (`E1`) első oldala.**
