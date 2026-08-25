# A webes admin technológiai választása — döntéselőkészítés

**Utolsó frissítés:** 2026-08-23
**Fázis:** F1 — mert az API-szerződés fogyasztója lesz
**Állapot:** `[JAVASLAT — DÖNTÉSRE VÁR]`

---

## 1. Mi a feladat pontosan

| # | Követelmény | Honnan |
|---|-------------|--------|
| R1 | **EGY alkalmazás, KÉT helyről kiszolgálva** — a felhőből **és** a telephelyi szerverről | §22.2 |
| R2 | **A telephelyi kiszolgáló egy J1900**, ami közben szerver ÉS gyakran POS kliens is | §4.2, M14 |
| R3 | **Offline is működik a telephelyi hálózaton** — semmilyen külső hívás | §22.2 |
| R4 | **Adatsűrű CRUD + riportok grafikonokkal** — terméktörzs, készlet, receptúra, statisztikák, beállítások, több telephely, felhasználók | §22.1 |
| R5 | **Beállítás-paritás a POS-szal** — mindent tudnia kell | §22.1/a |
| R6 | **HU + EN + DE** felületi szövegek | §25 |
| R7 | A közönség: **tulajdonos és üzletvezető, ülve, gondolkodva** | UIUX §3 |

---

## 2. `[DÖNTŐ SZŰRŐ]` Az R2 kizár két lehetőséget — mielőtt ízlésről beszélnénk

> **A telephelyi J1900-nak is ki kell szolgálnia ezt az alkalmazást, miközben
> PostgreSQL-t futtat, replikál, és gyakran pénztárgép is.**

| Modell | Mit kér a J1900-tól | Verdikt |
|--------|---------------------|---------|
| **Statikus fájlok** (SPA) | Fájlt küld a hálózatra. **Gyakorlatilag nulla CPU** | ✅ |
| **Szerveroldali renderelés** (Thymeleaf, JTE, htmx) | **Minden oldalletöltésnél sablont renderel** | ⛔ |
| **Blazor Server** | **Állandó WebSocket + szerveroldali UI-állapot MINDEN felhasználóra** | ⛔ |

**Ezért a szerveroldali renderelés és a Blazor Server kiesik** — nem ízlésből,
hanem mert **pont arra a gépre tenné a terhet, amiről már tudjuk, hogy szűkös**,
és amiről az M14 mérés külön szól.

*Megjegyzés a htmx-hez: vonzó, mert kevés JS — de **több szerver-körutat**
jelent, ami itt épp a rossz irány.*

> **Marad: statikusra fordított kliensalkalmazás.** Ezen belül két világ van.

---

## 3. A két maradó jelölt

### 3.1 Blazor WebAssembly (C#)

| | |
|---|---|
| ✅ | **Ugyanaz a nyelv, mint a POS kliens** — a csapat egy nyelvvel kevesebbet tart fejben |
| ✅ | Statikusan kiszolgálható |
| ✅ | Erős típusosság végig |
| ⚠️ | **A megosztás kevesebb, mint amennyinek látszik.** A backend **Java** — tehát szerveroldali kódmegosztás nincs. A POS **WPF**, aminek a nézetmodellje Blazorba **nem vihető át**. Ami valóban megosztható (pénztípusok, validáció), az **az OpenAPI-ból generált kliens** — és azt **bármelyik nyelv megkapja** |
| ⚠️ | **.NET futtatókörnyezet letöltése** az első betöltéskor. LAN-on nem gond, felhőből gyorsítótárazás után sem — de **nem nulla** |
| ⛔ | **Adatrács és grafikon ökoszisztéma jóval szűkebb**, mint JS-ben — az R4 pont ezekről szól |

### 3.2 JS/TS egyoldalas alkalmazás

| | |
|---|---|
| ✅ | **Messze a legjobb adatrács- és grafikon-kínálat** — az R4 magja |
| ✅ | Statikus build, apró fájlok |
| ✅ | **A legtöbb rendelkezésre álló minta és segédanyag** — ami ebben a projektben gyakorlati előny, mert **együtt írjuk a kódot** |
| ⚠️ | **Negyedik nyelv** a Java, C#, Dart mellé |
| ⚠️ | **Node build-lánc** és függőségkezelés — **ellátási lánc kockázat**, és offline csomagolási feladat |

---

## 4. `[ÚJRAÉRTÉKELVE]` Két dolog megváltozott a korábbi javaslat óta

### 4.1 Új információ: az admint az i3-as ÉRINTŐN is használják

**Az első ügyfélnél nincs irodai gép** — minden gép 1024×768-as érintőképernyős
POS *(HARDVER_MINIMUM §9.10)*.

**Ebből következik, hogy a böngésző futásidejű költsége FELÉRTÉKELŐDIK:**

| Hol nyitják meg | Mi fut még ugyanazon a gépen |
|-----------------|------------------------------|
| Pulti i3-as POS | Windows + POS kliens |
| ⚠️ **Az i5-ös gépen** | **Windows + PostgreSQL + a SZERVER + POS kliens** |

> **Ha az admint a szervergépen nyitják meg — és fogják —, akkor a böngésző
> memóriája és CPU-ja abból a keretből megy el, amiből a telephely működik.**
> Ez a szempont a korábbi értékelésben alul volt súlyozva.

### 4.2 `[ÖNHELYESBÍTÉS]` Túlértékeltem a React adatrács-előnyét

**Korábban azt írtam, hogy a React adatrács-kínálata döntően erősebb. Ez így
pontatlan.**

> **A legjobb fejnélküli (headless) adatrács — a TanStack Table — nem
> React-specifikus: van React, Vue, Svelte, Solid és Angular illesztője is.**

**És nálunk pont fejnélküli kell**, mert:

* saját palettánk van *(petrol + arany, UIUX §8)*,
* **érintésbarát sormagasság** kell *(§9.10)*,
* és minden kész, stílusozott rács **átstílusozásra szorulna** — ami gyakran több munka, mint fejnélkülit felöltöztetni.

**Tehát az az érv, ami a korábbi ajánlásomat vitte, nagyrészt elesik.**

---

## 5. A jelöltek — teljes összevetés

*(A szerveroldali renderelés és a Blazor Server már a 2. pontban kiesett.)*

| | **Vue 3** | **React** | **Svelte 5** | **Angular** | **Blazor WASM** |
|---|---|---|---|---|---|
| **Futásidejű költség gyenge gépen** | **kicsi** | közepes | **legkisebb** | nagy | ⛔ **legnagyobb** |
| **Első betöltés i3-on** | gyors | gyors | **leggyorsabb** | lassabb | ⛔ **.NET futtatókörnyezet + WASM fordítás** |
| **Memórialábnyom** | kicsi | közepes | **legkisebb** | nagy | ⛔ nagy |
| **Fejnélküli adatrács** | ✅ TanStack | ✅ TanStack | ✅ TanStack | ✅ TanStack | ⚠️ nincs egyenértékű |
| **Kész, teljes adatrács** | ✅ **PrimeVue DataTable** *(ingyenes, teljes, témázható)* | sok | kevesebb | AG Grid, Material | MudBlazor, Radzen |
| **Hivatalos útválasztó + állapot** | ✅ **Vue Router + Pinia** | ❌ külön csomagok | ✅ SvelteKit | ✅ beépítve | ✅ beépítve |
| **Függőségszám** | **kevés** | **legtöbb** | kevés | legkevesebb *(de a keret óriási)* | kevés |
| **TypeScript minőség** | **nagyon jó** | jó | jó | **legjobb** | *(C#)* |
| **Stabilitás / kevés törés** | ✅ **3.0 óta stabil** | sok mintaváltás | ⚠️ **az 5-ös „runes" valódi paradigmaváltás volt** | ✅ **nagyon stabil** | stabil |
| **Grafikon** | ECharts / Chart.js | legtöbb | ECharts | ECharts | szűkebb |
| **Nyelvi többlet** | JS/TS | JS/TS | JS/TS | JS/TS | **nincs — C#** |

---

## 6. `[VÉGLEGES JAVASLAT]` Vue 3 + TypeScript + Vite

**A korábbi React-javaslatomat visszavonom.** Nem azért, mert a React rossz — hanem
mert a két érv, ami vitte, **megváltozott vagy tévesnek bizonyult** *(4.1, 4.2)*.

### 6.1 Miért a Vue — négy ok, súly szerint

| # | Indok |
|---|-------|
| **1** | ⭐ **Kicsi futásidő gyenge gépen.** Az admin egy 3. gen. i3-on, sőt gyakran **a szervergépen** fut *(4.1)*. A Vue reaktivitása fordítási időben optimalizált, a memórialábnyoma kicsi |
| **2** | ⭐ **Hivatalos, összetartozó eszközkészlet.** Vue Router + Pinia + vue-i18n — **egy csapattól, egy verziórenddel.** Reactnál ugyanez 4–5 független csomag, mindegyik saját ütemben törik. **A „kevés függőség" kikötésünk** *(5.1/c)* **itt válik valósággá** |
| **3** | ⭐ **PrimeVue DataTable**: ingyenes, teljes *(virtuális görgetés, szűrés, rendezés, soron belüli szerkesztés)*, **és „unstyled" módban a mi tokenjeinkkel öltöztethető** — pont az, amit a paletta és az érintésbarát sorok igényelnek |
| **4** | ⭐ **Demonstráltan stabil.** A 3.0 óta nem volt paradigmaváltás. **Ez egy évtizedig futó rendszer** — a kevés törés itt többet ér, mint az ökoszisztéma mérete |

### 6.2 Miért nem a Svelte, pedig a futásideje kisebb

**Ez volt a legszorosabb döntés.** A Svelte technikailag a legkönnyebb.

**De: a Svelte 5 „runes" bevezetése valódi paradigmaváltás volt**, migrációval.
**Egy évtizedes életciklusú rendszernél a demonstrált törés valós kockázat** —
és a Vue futásidő-hátránya a Sveltéhez képest **ezen a feladaton nem érzékelhető**
*(egy admin CRUD nem animációs motor)*.

**A kész adatrács is ide húz:** a PrimeVue DataTable-nek nincs Svelte-megfelelője.

### 6.3 Miért nem a React

| # | Indok |
|---|-------|
| a | **Nagyobb futásidejű költség** azon a gépen, ahol a telephely is fut *(4.1)* |
| b | **A legtöbb függőség** — útválasztó, állapot, űrlap, i18n mind külön, külön ütemben törik. **Ütközik a „kevés függőség" kikötéssel** |
| c | ⚠️ **Az adatrács-előnye nagyrészt elesett** *(4.2)* — a TanStack fejnélküli és univerzális |

*A React nem rossz választás — csak ezen a hardveren és ezekkel a kikötésekkel
a Vue jobb.*

### 6.4 Miért nem az Angular

Kiváló TypeScript és stabilitás, **de a legnagyobb futásidejű költség** —
és a 4.1 pont pont ezt bünteti. Egy 3. gen. i3-on nem indokolt.

### 6.5 Miért nem a Blazor WASM

| # | Indok |
|---|-------|
| a | ⛔ **A .NET futtatókörnyezet letöltése + WASM fordítás egy 3. gen. i3-on érezhetően lassú első betöltés** |
| b | ⛔ **A legnagyobb memórialábnyom** — pont azon a 8 GB-os gépen, ahol PostgreSQL és a szerver is fut |
| c | ⚠️ **A nyelvi megosztás kevesebb, mint amennyinek látszik:** a backend **Java**, a POS **WPF**. Ami valóban megosztható, az **az OpenAPI-ból generált kliens** — és azt bármelyik nyelv megkapja |

---

## 7. A javasolt konkrét összeállítás

| Réteg | Választás | Miért |
|-------|-----------|-------|
| Keretrendszer | **Vue 3** *(Composition API, `<script setup>`)* | 6.1 |
| Nyelv | **TypeScript, szigorú módban** | A pénz és az áfa itt is átmegy |
| Fordító | **Vite** | Statikus build |
| Útválasztó | **Vue Router** | hivatalos |
| Állapot | **Pinia** | hivatalos |
| Nyelvek | **vue-i18n** — HU / EN / DE | §25 |
| **Adatrács** | **PrimeVue DataTable**, *unstyled* módban a mi tokenjeinkkel | 6.1/3 |
| **Grafikon** | **ECharts** | Sűrű adatra a legerősebb, keretrendszer-független |
| Stílus | **Saját tokenek** a logóból *(UIUX §8)* | Nincs idegen dizájnrendszer |

**Kilenc csomag. Ennél lényegesen több indoklást igényel** *(5.1/c)*.

## 8. Kikötések — ezek nélkül a javaslat nem áll

| # | Kikötés |
|---|---------|
| a | ⚠️ **SEMMILYEN külső hívás futásidőben.** Nincs CDN, **nincs Google Fonts**, nincs külső ikonkészlet. **Minden becsomagolva** — mert a telephelyi szervernek nincs internete *(R3)* |
| b | ⚠️ **A háttérrendszer címe futásidejű konfiguráció, nem build-időben beégetve.** Ugyanaz a köteg mutasson a felhőre **vagy** a telephelyi szerverre. **Ez ugyanaz a szabály, mint §0.3.3** — most a webre alkalmazva |
| c | **Kevés függőség.** Minden csomag ellátási lánc kockázat **és** offline csomagolási feladat. Adatrács + grafikon + útválasztó + űrlap — **ennél lényegesen több indoklást igényel** |
| d | **TypeScript, szigorú módban** — a pénz és az áfa itt is átmegy, és a lebegőpont tilalma *(I1)* a fronton is él |
| e | **A pénz a fronton is egész forint.** JSON-ban `1500`, nem `1500.0` *(API §9/1)* |
| f | **A grafikonkönyvtár külön döntés** — a `dataviz` szempontok szerint, és **a paletta a logóból jön** *(UIUX §8)* |
| g | **Offline korlát kiírva:** a telephelyről kiszolgált admin **30 napnál régebbi adatot nem mutat** — ezt a felület mondja meg, ne csendes üres eredmény legyen *(§22.2)* |

---

## 9. Amit NEM javaslok — és miért

| Megoldás | Miért nem |
|----------|-----------|
| **Szerveroldali renderelés Java-ban** (Thymeleaf, JTE) | **A J1900-ra teszi a renderelést** *(2.)*. Plusz: GraalVM natív image mellett a sablonmotorok **reflexiós konfigurációt** igényelnek — pluszmunka, nem megtakarítás |
| **htmx** | Kevesebb JS, **de több szerver-körút** — a szűk erőforrás itt épp a szerver |
| **Blazor Server** | **Állandó kapcsolat + szerveroldali UI-állapot minden felhasználóra.** A legrosszabb illeszkedés a J1900-hoz |
| **Két külön admin** (felhős + helyi) | ⛔ **Kifejezetten megtiltottuk** *(§22.2)* — a néma szétcsúszás forrása |
| **`shadcn`, `migrate-radix-to-base` skillek** | Csak akkor, ha React lesz — **és akkor is csak ha tényleg használjuk** *(SKILLEK §4)* |
| **Mobilalkalmazásként is** | Az admin **ülve, gondolkodva** használt felület *(R7)*. A mobil eset a vékonykliens, az **Flutter** |

---

## 10. Nyitott

**A csapat tapasztalati szintje kifejezetten NEM szempont** — a felhasználó
utasítása szerint a kérdés az, mi a legjobb választás.

| # | Ami még nyitott |
|---|-----------------|
| **W1** | **A Garm és a Hermes admin felülete milyen technológián van?** Nem a tudás miatt, hanem mert **közös komponenskészlet és egységes megjelenés** a Myth System alatt valós érték. Ha az egyik már Vue, az megerősíti a javaslatot; ha React, azt mérlegelni kell |
| **W2** | **Az adatrács végleges kiválasztása** — a PrimeVue DataTable a javaslat, de az érintésbarát sormagasság és a mi tokenjeink **kipróbálandók**, mielőtt véglegesítjük |
