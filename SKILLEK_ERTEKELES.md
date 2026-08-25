# A `skills` branch értékelése — 128 skill átnézve

**Utolsó frissítés:** 2026-08-23
**Szabály (a felhasználótól):** amit hasznosnak találok, azt használjuk; ami nem
jó, felesleges, **vagy ütközik a jelenlegi döntésekkel / az utasításaiddal**, azt nem.

---

## Összesítő

| Kategória | Db | Mi |
|-----------|----|----|
| ✅ **Használjuk** | **18** | A stackünkhöz és a munkamódszerünkhöz illik |
| 🟡 **Feltételesen** | **11** | Egy konkrét részhez, vagy egy még nyitott döntés után |
| ⛔ **ÜTKÖZIK a döntéseinkkel** | **13** | **Ezekre külön felhívom a figyelmet** |
| ❌ Rossz stack | ~32 | Más nyelv/keretrendszer |
| 🔷 Figma | 16 | Csak ha Figmát vezetünk be — **nem javaslom** |
| 📣 Üzleti / marketing | ~14 | Most nem, később hasznos lehet |
| ⚙️ Meta / egyéb | ~24 | Átfedő vagy nem releváns |

---

## ✅ 1. Használjuk — a stackünk

| Skill | Mire | Miért |
|-------|------|-------|
| **`java-architect`** · **`spring-boot-engineer`** | Backend | A telephelyi szerver és a felhő |
| **`csharp-developer`** · **`dotnet-core-expert`** | POS kliens | WPF / .NET 8 |
| **`flutter-expert`** | Vékonykliens, KDS, kijelzők | |
| **`postgres`** · **`postgres-pro`** · **`sql-pro`** | Adatbázis | |
| **`database-optimizer`** · **`database-patterns`** | Adatbázis | ⚠️ **Kiemelten fontos nálunk**: a J1900 memóriakorlátja miatt az indexméret és a lekérdezésterv nem elmélet, hanem üzemeltetési kérdés |
| **`websocket-engineer`** | Push réteg | Ezt választottuk *(API-szerződés §1)* |
| **`test-master`** · **`testing-strategies`** | Tesztelés | |

### ⭐ `api-contract-first` — ez a legjobb találat

> *„Hard gate before implementing any API endpoint. Requires a written, reviewed
> contract before any implementation code is written."*

**Ez szó szerint az F1.1 feladatunk**, és pontosan azzal az indokkal, amit mi is
leírtunk: *„egy még nem frissített POS-nak tovább kell tudnia eladni"*.
**Kapuként használjuk, nem tanácsadóként.**

---

## ✅ 2. Használjuk — módszertan

| Skill | Mire |
|-------|------|
| **`architecture-designer`** | ADR-ek — **eddig hiányzott.** A döntéseink indoklása a `NYITOTT_KERDESEK.md`-ben él, de **formális ADR-forma nélkül**. Kódoláskor ez hasznos lesz |
| **`code-reviewer`** | Kódfelülvizsgálat *(egyet választunk, lásd 3.)* |
| **`secure-code-guardian`** | Biztonsági kód-átnézés |
| **`debugging-wizard`** | |
| **`code-documenter`** | |
| **`monitoring-expert`** · **`sre-engineer`** | Üzemeltetés — **a Hermes-integrációhoz** *(§0.3.1)* |
| **`ops-investigate-alert`** · **`ops-oncall-log`** | ⚠️ **Közvetlenül a nyolc eszkalációs útvonalunkhoz** — ezek adják a riasztás-kezelés mintáit, amit eddig nem terveztünk meg |

### ⭐ `the-fool` — adverzariális gondolkodás

> *„Devil's advocate, pre-mortem, red team, audit evidence and assumptions."*

**Ez pontosan az, amit a két ellenőrző körben kézzel csináltunk** — és ami a
legtöbb hibát találta (a 25 órás munkanap ütközése, a WAL-felhalmozódás, az
`ADOTT_NAPON_ZARVA` csapda). **Strukturálva jobb, mint ad hoc.**

**Javaslat:** minden fázis kilépési feltétele elé egy `the-fool` kör.

### ⭐ `chaos-engineer` — a HA-teszteléshez

> *„Failure injection, game day exercises, runbooks, rollback procedures."*

**Erre konkrét szükségünk van, és eddig nem volt rá terv.** Az M12 mérés (*a
tartalék POS átveszi a szolgálatot csúcson*) **pontosan egy game day**. És a
`FOLYAMATBAN.md` már rögzítette, hogy a failover-kód **ritkán futó kód, tehát
élesben hibázik először** *(A6 elv)* — **a hibainjektálás ez ellen a legjobb
eszköz.**

---

## 🟡 3. Feltételesen

| Skill | Feltétel |
|-------|----------|
| `api-designer` · `backend-api-design` · `api-endpoint-creator` | **Átfedik az `api-contract-first`-öt.** Egy kapu elég — a többi zaj. **Csak az `api-contract-first`-öt tartjuk** |
| `code-review-skill` · `security-reviewer` · `security-checklist` | **Átfedés** a `code-reviewer` + `secure-code-guardian` párossal. **Kettőnél több kódfelülvizsgáló skill kioltja egymást** |
| `ui-ux-pro-max` · `ui-styling` · `design-system` · `design-intelligence` | **Már használtuk**, részlegesen *(UIUX_TERV §0)*. A `ui-reasoning` adata ránk nem áll |
| `brand` | **A Myth System CÉGarculatához** — a Siduri terméképe már megvan a logóból |
| `playwright-expert` · `browser-qa` | **Csak a webes adminhoz.** A POS-t nem böngésző futtatja |
| `legacy-modernizer` · `spec-miner` | **Az átálláshoz** *(F8.6)* — a leváltott rendszer adatszerkezetének megértéséhez |
| `cloud-architect` · `devops-engineer` | **Csak a felhő oldalra**, mértékkel — lásd 4. |

---

## ⛔ 4. ÜTKÖZIK a döntéseinkkel — ezeket NE

**Ez a szakasz az, amire külön kérted, hogy figyeljek.**

| Skill | Mivel ütközik | Miért káros, nem csak felesleges |
|-------|---------------|----------------------------------|
| **`microservices-architect`** | **Monolitot építünk EGY J1900-ra** | ⚠️ **Aktívan káros.** Szolgáltatás-szétvágás, hálózati határok, elosztott tranzakciók — mindegyik **memóriát és késleltetést tesz oda, ahol pont abból nincs.** A mi „elosztottságunk" két gép, nem tucat szolgáltatás |
| **`graphql-architect`** | **REST + JSON-t választottunk** *(API §1)* | A választás indoklása is megvan: három különböző kliens, és a hibakereshetőség többet ér a bájtoknál |
| **`react-native-expert`** | **Flutter** | |
| **`mysql`** | **PostgreSQL** | A replikációs slot, a WAL-korlátozás, az RLS mind Postgres-specifikus döntés |
| **`kubernetes-specialist`** | **Két fizikai felhőszerver + Windows Service egy étteremben** | ⚠️ A konténer-orkesztráció **egy egészen más üzemeltetési modellt feltételez**, mint amit a §22.4-ben eldöntöttünk |
| **`terraform-*`** *(6 skill: best-practices, engineer, module-creator, review, security-audit, service-scaffold)* | Ugyanaz | **Hat skill ugyanarra**, olyan infrastruktúrára, amink nincs |
| **`shadcn`** · **`migrate-radix-to-base`** | React komponenskönyvtár | **A webes admin frontend stackje MÉG NINCS ELDÖNTVE** *(lásd 8.)*. Ha nem React lesz, ezek zaj |
| ⚠️ **`using-superpowers`** | **A munkamódszerünkkel ÉS az utasításaiddal** | *„requires Skill tool invocation before ANY response including clarifying questions"* — **ez minden válasz elé ceremóniát tenne**, beleértve a tisztázó kérdéseket. **Közvetlenül ütközik** azzal, ahogy dolgozunk, és a „ne használj semmitmondó hivatkozásokat, írd ki pontosan" elvárásoddal |

---

## 🔷 5. Figma (16 skill) — nem javaslom

`figma-code-connect` · `figma-create-new-file` · `figma-design-to-code` ·
`figma-generate-design` · `figma-generate-diagram` · `figma-generate-library` ·
`figma-implement-motion` · `figma-swiftui` · `figma-use` · `figma-use-figjam` ·
`figma-use-motion` · `figma-use-slides` · `skill-sets/figma/*` (2) ·
`design-workflow`

**Nem azért nem, mert rosszak** — hanem mert:

| # | Indok |
|---|-------|
| a | **Új eszközfüggőség** egy olyan projektben, ahol már van három külső kapu |
| b | ⚠️ **A POS-felület valódi kényszerei nem pixelkérdések.** A 64 px-es célfelület, a német szöveghossz, a Bay Trail iGPU és a zsíros ujj — **ezeket Figmában nem lehet ellenőrizni, csak valós J1900-on** *(elfogadási kritérium 10.)* |
| c | A `figma-swiftui` iOS-re való — **nálunk nincs iOS natív** |

**Ha később mégis kell** (pl. az ügyfélnek prezentálandó látvány), akkor a
`figma-generate-design` és a `figma-design-to-code` a két értelmes belépő.

---

## ❌ 6. Rossz stack — nem használjuk

`django-expert` · `django-storages-s3` · `fastapi-expert` · `python-pro` ·
`pandas-pro` · `rails-expert` · `laravel-specialist` · `php-pro` ·
`wordpress-pro` · `shopify-expert` · `golang-pro` · `rust-engineer` ·
`cpp-pro` · `kotlin-best-practices` · `kotlin-specialist` · `swift-expert` ·
`salesforce-developer` · `game-developer` · `embedded-systems` ·
`spark-engineer` · `ml-pipeline` · `fine-tuning-expert` · `rag-architect` ·
`nestjs-expert` · `cli-developer` · `atlassian-mcp` *(Jira/Confluence — **nekünk Hermes van**)*

---

## 📣 7. Üzleti / marketing — most nem, később igen

`investor-materials` · `investor-outreach` · `market-research` ·
`competitive-teardown` · `idea-validation` · `startup-pipeline` ·
`content-engine` · `article-writing` · `slides` · `banner-design` ·
`brainstorm` · `deep-research` · `web-to-prd` · `theme-factory`

**Kettő közülük később valóban hasznos lehet:** a `competitive-teardown` és a
`market-research` — **de a termék eladásához, nem a megépítéséhez.** Most a
figyelmet elvinnék.

---

## 8. `[ÚJ NYITOTT DÖNTÉS]` A webes admin frontend stackje

**`[MEGVÁLASZOLVA 2026-08-23]` A javaslat: Vue 3 + TypeScript + Vite**
*(részletes indoklás: `WEBADMIN_STACK.md`)*.

**Ebből következik a skill-választás:**

| Skill | Verdikt |
|-------|---------|
| **`vue-expert`** *(vagy `vue-expert-js`)* | ✅ **EZ az egy frontend skill, ami bekerül** |
| **`typescript-pro`** | 🟡 Feltételesen — ha a `vue-expert` nem fedi le |
| `react-expert` · `nextjs-developer` · `angular-architect` · `shadcn` · `migrate-radix-to-base` | ⛔ **Tárgytalan** |
| `javascript-pro` | ⛔ TypeScriptet írunk |
| `js-security-audit` | 🟡 Feltételesen, egy biztonsági kör erejéig |

A specifikáció annyit mond, hogy **EGY webes admin alkalmazás van, két helyről
kiszolgálva** *(§22.2)* — **a technológiáját nem.**

**Ez F1-es döntés**, mert az API-szerződés fogyasztója lesz.

| # | Szempont |
|---|----------|
| a | ⚠️ **A telephelyi szerver is kiszolgálja** — J1900-on. **Kiszolgálás szempontjából statikus fájlok a legolcsóbbak** |
| b | A backend Java → **egy Java-alapú szerveroldali renderelés kísértése** csábító, de a J1900-on drágább, mint statikus fájlt adni |
| c | **A csapat ismerete dönt**, nem a divat |

**Amint eldől, egy — és csak egy — frontend skill kerül be.**

---

## 9. Javaslat — ennyit telepítsünk, ne többet

> **A skillek nem ingyen vannak: egymást zavarják, és a sok átfedő tanácsadó
> kioltja egymást.** Ezért szűk lista:

**Mag (11):**
`api-contract-first` · `java-architect` · `spring-boot-engineer` ·
`csharp-developer` · `dotnet-core-expert` · `flutter-expert` · `postgres-pro` ·
`database-optimizer` · `websocket-engineer` · `test-master` ·
`architecture-designer`

**Minőség és üzemeltetés (5):**
`the-fool` · `chaos-engineer` · `code-reviewer` · `secure-code-guardian` ·
`ops-investigate-alert`

**Amikor odaérünk (4):**
`playwright-expert` *(webes admin)* · `brand` *(Myth System cégarculat)* ·
`spec-miner` *(átállás)* · **`vue-expert`** *(eldőlt — lásd 8.)*

**Összesen: 20 skill a 128-ból.**
