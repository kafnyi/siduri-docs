# `szinkron` (K3) — v1.0.0, első szelet

**Kiadva: 2026-09-21.** A fájl: [`szinkron.yaml`](szinkron.yaml).

**A K3 a legszigorúbb kompatibilitási kényszerű szerződés**, mert **a felhő és a
telephely soha nem frissül egyszerre.** Legalább **két kiadási ciklusnyi**
visszafelé kompatibilitás kell.

## A három szabály, ami ebből következik

| # | Szabály |
|---|---------|
| a | **Ismeretlen mezőt figyelmen kívül kell hagyni**, nem hibának tekinteni |
| b | **Ismeretlen változás-típust a telephely NEM alkalmaz**, hanem `ELUTASITVA` nyugtáz (`ISMERETLEN_TIPUS`). Nem áll le, és nem is ugorja át csendben — a felhő így **megtudja**, hogy a telephely régebbi |
| c | **A sorszám monoton és telephelyenkénti.** Egy már alkalmazott sorszám újbóli megérkezése nem alkalmazódik újra |

## Amit a megíráskor el kellett dönteni — és mi lett belőle

| # | Kérdés | Döntés (2026-09-21) |
|---|--------|---------------------|
| **W3** | Törzsadat-szerkesztés offline telephely mellett | **Eldöntve az O3-ban**: mezőnkénti időbélyeg, a későbbi írás nyer. A szerződés ezért hordozza a `mezoeredet`-et minden változáson |
| **S3** | A tömeges átvitel alakja | **Ugyanaz a végpont, lapozva.** Az első feltöltés és a teljes újraszinkron annyit jelent, hogy a telephely kurzor nélkül kérdez. **Nincs második formátum** — egy ritkán futó második kódút évekig észrevétlenül romolhatna el |
| **Ütem** | Ki kezdeményez | **A telephely húz, időzítve, alkalmazkodó ütemmel.** A választ a felhő vezérli (`kovetkezoLekerdezesMp`): amíg van több változás, **nulla** — így egy csomóban érkező szerkesztés másodpercek alatt leér, nyitva tartott kapcsolat nélkül |
| **B16.8/5** | Nagy hatókörű árművelet védelme | **Késleltetett élesítés** (`ervenyesTol`) — egy feltört felhő-fiók nem tudja egy pillanat alatt kinullázni egy franchise összes árát |
| **Hitelesítés** | Mi védi a lefelé menő parancsot | **Kölcsönös TLS most**, és az `alairas` mező **már benne van** a szerződésben. A telephely ma még nem követeli meg — de a későbbi bekapcsolás így **nem törő változás** |

## Amit egy lekérdezés valójában csinál

**Három dolog egyszerre, ezért nincs belőle három végpont:**

1. a rá váró változások lekérése,
2. a **szívverés** (a felhő ebből tudja, él-e a telephely — licenc, eszköz-láthatóság),
3. az **óraállás** jelentése.

> ⚠️ **Az üres lekérdezés ezért nem pazarlás.** Az óraállás nélkül a mezőnkénti
> időbélyeg-feloldás (O3) vakon futna: a sorrendet két gép **fali órája** dönti
> el, és a küszöb fölötti eltérést jelezni kell (`oraElteresMp`).

## Két dolog, amit a szerződés kimond, és a megvalósításnak tartania kell

* **A telephely VALIDÁL, nem vakon alkalmaz** (B16.8/3). Egy olyan áfakulcs, ami
  a dátumozott adókulcs-táblában nem szerepel, **elutasítandó**.
* **Három állapot van, nem kettő:** `ATVETTE` / `ALKALMAZTA` / `ELUTASITVA`. Az
  „összes érintett eszköz alkalmazta" a **negyedik** — az a K1 oldalán dől el
  (egy pénztárgép lehet offline, és még a régi árral dolgozik), és **későbbi
  szelet**. A fogalom viszont már most rögzítve van, hogy a felület ne kettőt
  mutasson három helyett.

## Ami ebben a szeletben NINCS benne

* **Az eladási adatok felküldése** (8 éves archívum) — későbbi szelet.
* **A mennyiségi, futó állapot** (készlet, forgalom, kassza): kizárólag
  telephely-autoritatív, és **csak felfelé** áramlik (B16.4).
* **Megvalósítás: semmi.** Ez a szerződés — a kód a következő lépés.
