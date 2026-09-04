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

### 4.1 ~~Új információ: az admint az i3-as ÉRINTŐN is használják~~ `[MEGDŐLT — lásd §13]`

> ⚠️ **Ez a szakasz téves feltevésen alapul, és a §13 megdönti.** Az admint
> túlnyomórészt **saját laptopról, a felhőből** használják; a pulti gépen csak
> a helyi beállításokat. Az alábbi okfejtés **csak az offline tartalék esetére**
> marad érvényes. Meghagyva, mert a tévedés maga is információ.

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

## 10. `[MEGVÁLASZOLVA]` A Myth System házi stackje — és mit igazol

**A Garm és a Hermes tényleges felépítése:**

| | **Garm** | **Hermes** | **Siduri (tervezett)** |
|---|---|---|---|
| Backend | **Java Spring Boot** | **Node.js** | **Java Spring Boot** |
| Adatbázis | **PostgreSQL** | **PostgreSQL** | **PostgreSQL** |
| Windows kliens | **Dart** *(Flutter desktop)* | **WPF** | **WPF** |
| Mobil | **Dart** | **Dart** | **Dart** *(Flutter)* |
| Web | — | **Node.js**, minimális *(videós)* |  ← **ez a kérdés** |

### 10.1 `[MEGERŐSÍTÉS]` A Siduri öt választásából NÉGY már illeszkedik

**Ez jó hír, és eddig nem tudtuk:**

| Választás | Házi illeszkedés |
|-----------|------------------|
| **Java Spring Boot** backend | ✅ **Ugyanaz, mint a Garm** |
| **PostgreSQL** | ✅ **Mindkettőnél ez van** |
| **WPF** Windows kliens | ✅ **Ugyanaz, mint a Hermes** |
| **Flutter / Dart** vékonykliens | ✅ **Mindkettőnél ez van** |
| Webes admin | ← **az egyetlen új felület** |

> **Vagyis nem egy idegen stacket építünk a ház mellé — a Siduri négy rétege
> már most illeszkedik.** Ez utólagos igazolása a korábbi döntéseknek.

### 10.2 `[ÚJ JELÖLT]` Flutter Web — most már komolyan felmerül

**A Dart erősen jelen van a házban**, és a Siduriban **már úgyis lesz Flutter**
*(PDA, KDS, rendeléskijelző)*. **Ez a legerősebb szervezeti érv, ami eddig
elkerülte a figyelmemet.**

| ✅ Mellette | ⛔ Ellene |
|---|---|
| **Nulla új nyelv** — a ház mély Dart-tudással bír | ⚠️ **CanvasKit: vászonra rajzol.** Nincs natív szövegkijelölés, gyenge akadálymentesség, nincs böngészős keresés az oldalon |
| **Egy nyelv az egész Siduri frontendre** a POS-on kívül | ⚠️ **Nehéz első betöltés** — a futtatókörnyezet + a köteg **egy 3. gen. i3-on érezhető** |
| **Közös widgetek, közös i18n, közös generált API-kliens** a PDA-val és a KDS-sel | ⚠️ **NAGY TÁBLÁKON GYENGE** — pont az, amiből az admin áll |
| Web + telepíthető alkalmazás **egy kódbázisból** | ⚠️ **Nagy memórialábnyom** azon a gépen, ahol a szerver is fut |
| A Garm bizonyítja, hogy Dart desktopon is megy | ⚠️ Nincs PrimeVue-szintű kész adatrács |

### 10.3 A két érv, ami eldönti

**Az 1. — a Flutter Web pont ott gyenge, ahol az admin nehéz.**

> Az admin **táblákból, űrlapokból és grafikonokból** áll. Ez a **legrosszabb
> eset** vászonra rajzoló megjelenítőnek, és **a legjobb eset** DOM-alapúnak.
> Egy 500 tételes terméktörzs görgetése egy 3. gen. i3-on **pontosan az a
> terhelés, amit a CanvasKit rosszul visel.**

~~**Ellenérv, amit meg kell vizsgálni:** *„az admint csak alkalmanként használják,
számít ez?"* — **De igen, mert nem így van.** Az ügyfélnél **naponta, a pulti
érintőn** fogják nyitogatni gyors dolgokra *(§9.10)*, és **néha a szervergépen.**~~

> ⚠️ **Ez az ellenérv-cáfolat HAMIS volt — lásd §13.1.** Az admint laptopról,
> a felhőből használják. **Az 1. érv ezzel nagyrészt elesik**; a döntést a
> §13.2 öt böngésző-natív tulajdonsága viszi tovább. **A 2. érv változatlanul áll.**

**A 2. — a közös dizájnrendszer NEM igényel közös keretrendszert.**

> **A tervezési tokenek csak értékek.** Egy közös token-fájlból *(petrol, arany,
> méretek, sugarak)* **a Flutter ÉS a Vue is táplálkozhat.** Ugyanígy: **az
> OpenAPI-ból generált kliens Dartra ÉS TypeScriptre is elkészül.**
>
> **Tehát az egységes megjelenés és a közös szerződés megvan közös nyelv
> nélkül is** — a Flutter Web valódi többlete ezzel jóval kisebb, mint elsőre látszik.

### 10.4 `[ÉRV, AMI A JS-T OLCSÓBBÁ TESZI]` A JS/TS nem új a házban

**A Hermes web- és szerverrétege Node.js.** Tehát:

> **A JS/TS ökoszisztéma már bent van a házban.** Nem új nyelvet hozunk be,
> csak egy keretrendszert egy olyan ökoszisztémán belül, ami már fut.

**Ez érdemben gyengíti az „ötödik nyelv" ellenérvet** — ami a Flutter Web
legerősebb támasza volt.

### 10.5 `[ELVI MEGÁLLAPÍTÁS]` A ház már most elfogad felület-szerinti sokféleséget

**Nézzük meg, mit csinál a Myth System valójában:**

* Windows desktopon **Garm = Dart, Hermes = WPF** — **két különböző út, ugyanabban a házban**
* Backendben **Garm = Java, Hermes = Node** — **szintén kettő**

> **A ház tehát nem „egy nyelv mindenre" elven működik, hanem
> FELÜLETENKÉNT VÁLASZT.** A webes admin egy **harmadik felület, harmadik
> igényekkel** — egy webnatív keretrendszer választása **illeszkedik a ház
> meglévő filozófiájába**, nem sérti azt.

---

## 11. `[VÉGLEGES]` A javaslat marad: Vue 3 + TypeScript + Vite

**A Flutter Web komoly jelölt lett, és tisztességesen mérlegeltem — de veszít**,
két okból:

| # | Ok |
|---|-----|
| 1 | **Pont ott gyenge, ahol az admin nehéz** (nagy táblák), **pont azon a hardveren**, amink van *(3. gen. i3, néha a szervergép)* |
| 2 | **A szervezeti előnye nagyrészt megszerezhető nélküle is** — közös tokenek, közös OpenAPI-kliens *(10.3)* |

**És amit ezért feladunk, azt ki kell mondani:**

> ⚠️ **A Siduriban két frontend nyelv lesz: Dart** *(PDA, KDS, kijelzők)* **és
> TypeScript** *(webes admin)*, a WPF mellett. **Ez valós költség** — két
> komponenskészlet, két fordítási lánc.
>
> **Azért vállalható, mert két KÜLÖNBÖZŐ felületről van szó** — érintős POS-eszköz
> és adatsűrű asztali admin —, **amiknek amúgy sem lenne közös komponenskészletük.**

**Az eldöntő mondat:**

> **Egy rossz eszközválasztás teljesítményproblémáját nem lehet szorgalommal
> megjavítani. Egy második nyelvet viszont el lehet viselni.**

### 11.1 ~~Ha valami mégis a Flutter Web felé billentené~~ `[VISSZAVONVA — §13.3]`

**Egy feltétel van, ami újranyitná a kérdést:**

Ha az admin **mégsem** lenne táblanehéz — pl. ha a valódi adminisztráció
teljesen átkerülne egy külön eszközre, és a webfelület **csak néhány gyors
művelet** maradna *(ár, „elfogyott", egy termék)* — **akkor a Flutter Web
egyértelműen nyerne**, mert a nehéz része esne ki.

**Ezt érdemes az első ügyfélnél megfigyelni**, és **v2-ben újraértékelni.**

---

## 12. Nyitott

**A csapat tapasztalati szintje kifejezetten NEM szempont** — a kérdés az, mi a
legjobb választás.

| # | Ami még nyitott |
|---|-----------------|
| **W1** | **Az adatrács végleges kiválasztása** — a PrimeVue DataTable a javaslat, de az **érintésbarát sormagasság** és a mi tokenjeink **kipróbálandók**, mielőtt véglegesítjük |
| ~~**W2**~~ | ~~**Közös token-fájl formátuma** a Flutter és a Vue felé *(10.3)*~~ → **LEZÁRVA:** `marka.json` a jelforrás, `eszkozok/marka_ellenoriz.py` a kapu. Lásd `MARKA.md` §7 |

---

## 13. `[ÖNHELYESBÍTÉS — AZ ÉRVEM MEGDŐLT]` Az admint laptopról, a felhőből használják

**Új információ a felhasználótól (2026-08-25):**

> „A legtöbben valószínűleg egy saját laptopról fogják a webes felületen
> használni az admin oldalt, amit meg a felhő lát majd el. A kliensen használat
> ritka lesz, ott inkább csak a helyi beállításokat fogják nyomkodni."

### 13.1 Mit dönt ez meg — pontosan

**A §4.1 és a §10.3 első érvének a magja hamis volt.**

A §10.3-ban a Flutter Webet elsősorban azzal buktattam meg, hogy a CanvasKit
vászonra rajzol, és ez **pont a mi gyenge vasunkon, pont a táblanehéz admin
képernyőkön** fáj. Amikor felmerült az ellenérv, hogy „az admint úgyis csak
ritkán nyitják meg", azt **azzal ütöttem el, hogy naponta megnyitják a pulti
érintőképernyőn.**

**Ez nem így van.** Az admin elsődleges helye a **saját laptop**, és a
kiszolgálója a **felhő**. A pulti gépen a rendszeres használat a **helyi
beállítások**, ami nem táblanehéz.

**Ezt nem szépítem: nem gyengült az érvem, hanem megszűnt.** A „gyenge vas +
nagy tábla" együttállás, amire épült, az esetek túlnyomó részében nem áll fenn.

### 13.2 Újrafuttatva a döntés, a helyes tényekkel

Ami ezzel a **Flutter Web javára** változott:

| # | Változás |
|---|----------|
| a | **A teljesítményérv nagyrészt elesik.** Egy laptop nem egy 3. generációs i3-as pultgép; a CanvasKit ott elbírja a táblát |
| b | **A helyi felület kicsi lett** — a beállítások néhány űrlap, nem adatrács. A CanvasKit gyenge oldala itt alig érintett |

Ami viszont **ugyanezzel a lépéssel a Vue javára erősödött** — és ezt korábban
alulsúlyoztam:

| # | Tulajdonság | Miért számít MOST jobban |
|---|-------------|--------------------------|
| 1 | **Szövegkijelölés és másolás** | Az admin átkerült egy **irodai** felületre. A tulajdonos és a **könyvelő** ki fogja jelölni a számokat, és **be fogja illeszteni Excelbe.** A CanvasKit vászonra rajzol: a kijelölés ott legjobb esetben is utánzat |
| 2 | **Ctrl+F, a böngésző saját keresése** | Egy 400 soros terméklistában ez az első reflex. Vásznon **nem működik** — nem lassan, hanem sehogy |
| 3 | **Nyomtatás és PDF** | Kimutatást nyomtatnak. A vászon-alapú oldal nyomtatása rossz, és nem javítható ki |
| 4 | **Jelszókezelő, könyvjelző, új lap, vissza gomb** | Saját laptopon a felhasználó **a böngészőjét használja**, nem a mi alkalmazásunkat. A jelszókezelő vászon-beviteli mezőt nem tölt ki. Két lapon összehasonlítani két kimutatást természetes igény |
| 5 | **Első betöltés mérete** | A felhőből, **interneten** érkezik, nem LAN-ról. A CanvasKit futásideje másfél–két megabájt az alkalmazás előtt; egy Vite-os csomag ennek töredéke |

### 13.3 `[VÁLTOZATLAN KÖVETKEZTETÉS, ÚJ INDOKLÁSSAL]`

**A javaslat marad a Vue 3 + TypeScript + Vite — de nem azért, amiért eddig.**

> **Az admin nem „egy kezelőpanel a mi vasunkon" lett, hanem egy irodai
> webalkalmazás valaki más laptopján.** Az irodai webalkalmazásnál pedig a
> böngésző natív viselkedése — kijelölés, másolás, keresés, nyomtatás,
> könyvjelző, jelszókezelő — **nem részletkérdés, hanem maga a termék.**

**Ez a korábbinál erősebb indoklás**, mert nem egy mérésre váró
teljesítménysejtésen áll, hanem öt olyan tulajdonságon, ami a Flutter Webben
**szerkezetileg** hiányzik, nem hangolással.

**A §11.1-ben rögzített újranyitási feltételt ezzel visszavonom.** Az ott
megnevezett eset — „ha az admin mégsem lenne táblanehéz, a Flutter Web
egyértelműen nyerne" — **részben bekövetkezett**, és **mégsem billenti át**,
mert a döntés súlypontja közben átkerült a teljesítményről a böngésző-natív
viselkedésre. Ha ezt akkor tudom, a §11.1-et eleve nem így fogalmazom meg.

### 13.4 `[TERVEZÉSI KÖVETKEZMÉNY]` A funkciók megoszlása a két kiszolgálás között

A §22.2 („egy admin alkalmazás, két helyről kiszolgálva") **áll**, de a
laptop-elsőség után **meg kell húzni benne egy vonalat**, amit eddig nem
húztunk meg:

| Funkciócsoport | Hol él | Miért |
|----------------|--------|-------|
| **Törzsadat, receptúra, kimutatás, jogosultság** | **Ugyanaz a kód, két helyről kiszolgálva** — normál esetben a felhőből, offline a telephelyi szerverről | Ezek **mindkét helyen léteznek**, tehát fennáll a néma szétcsúszás veszélye. Ez ellen csak a közös kód véd |
| **Helyi beállítás** — eszközszerep, nyomtató-átirányítás, adóügyi eszköz párosítása, integráció ideiglenes tiltása | **Kizárólag a telephelyi szerverről** | Ezeknek a felhőben **nincs párja**, tehát nincs mitől szétcsúszniuk. És **működniük kell akkor is, amikor nincs internet** — épp ilyenkor van rájuk szükség |

**Következmény az M14 mérésre:** a telephelyi szerver **nem a napi
adminisztrációt szolgálja ki**, hanem a helyi beállításokat és az offline
tartalékot. **Az M14 terhelési feltevését ennek megfelelően lejjebb kell
venni** — de a mérést nem törölni, mert az offline eset továbbra is valós.

### 13.5 `[ÚJ KOCKÁZAT]` A felhő üzemeltetési kritikussá vált

Eddig a felhő szerepe **licenc, archívum, statisztika, NTAK-tartalék** volt —
vagyis a napi kereskedés **nem függött tőle**.

**A laptop-elsőségű adminnal a felhő bekerül a napi munkába:** az árat, a
menüt, az új terméket ott viszik fel. **Ha a felhő áll, a törzsadat-karbantartás
áll.** Az eladás nem — az továbbra is telephelyi —, de a kettő nem ugyanaz.

**Ez nem érv a döntés ellen**, hanem egy **rendelkezésre állási követelmény**,
amit ki kell mondani, mielőtt ígéretet teszünk rá.

---

## 14. Nyitott — bővítve

| # | Ami még nyitott |
|---|-----------------|
| **W1** | Az adatrács végleges kiválasztása — PrimeVue DataTable, érintésbarát sormagassággal, a mi tokenjeinkkel, **kipróbálás után** |
| ~~**W2**~~ | ~~A közös token-fájl formátuma a Flutter és a Vue felé~~ → lezárva, `MARKA.md` §7 |
| **W3** | **`[ÚJ]` Törzsadat-szerkesztés offline telephely mellett.** A tulajdonos otthon, laptopról árat ír át a felhőben, miközben az étterem internete áll. **Melyik az igazság forrása, és mi történik ütközésnél?** Ez a laptop-elsőségből következik, és **el kell dönteni, mielőtt a szinkron megépül** |
| **W4** | **`[ÚJ]` A felhő rendelkezésre állási vállalása** a törzsadat-karbantartásra *(13.5)* |
