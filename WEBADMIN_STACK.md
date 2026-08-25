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

## 4. `[ELDÖNTENDŐ RÉSZLET]` Ha JS: melyik keretrendszer

| | **React** | **Svelte** | **Vue** | **Angular** |
|---|---|---|---|---|
| Adatrács, grafikon | **legjobb** | szűkebb | jó | jó |
| Kötegméret / futásidő | közepes | **legkisebb** | kicsi | **legnagyobb** |
| Döntéskényszer *(router, állapot)* | sok | kevés | kevés | **nincs — mindent hoz** |
| Elérhető minta és segédanyag | **legtöbb** | kevesebb | sok | sok |
| Kis csapatnak | jó | **jó** | **jó** | nehéz |

### ⚠️ Egy szempont, ami könnyen kimarad

**Az admint gyakran ugyanazon a J1900-on nyitják meg**, ahol a szerver és a POS
fut — mert **egy kis étteremben az az egyetlen gép.**

> **Tehát nem csak a KISZOLGÁLÁS terheli a J1900-at, hanem a BÖNGÉSZŐ is.**

Ez **a legkisebb futásidő felé húz** (Svelte), és **az Angular ellen szól**.

---

## 5. `[JAVASLAT]` React + TypeScript + Vite, statikus build

**Miért nem a Svelte, pedig könnyebb:** a 4. pont szerint a Svelte futásideje
kisebb — **de az R4 (adatrács + grafikon) a nehezebb feladat**, és ott a React
kínálata lényegesen erősebb. **A kötegméret-különbség LAN-on nem érzékelhető, a
hiányzó adatrács viszont hetekben mérhető.**

**Miért nem a Blazor, pedig egy nyelvvel kevesebb:** a nyelvi megosztás valódi
haszna kicsi *(3.1)*, a hiányzó adatrács- és grafikon-kínálat viszont pont az
R4-et érinti.

**Miért nem az Angular:** a J1900-as böngésző *(4.)* és a kis csapat.

### 5.1 Kikötések — ezek nélkül a javaslat nem áll

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

## 6. Amit NEM javaslok — és miért

| Megoldás | Miért nem |
|----------|-----------|
| **Szerveroldali renderelés Java-ban** (Thymeleaf, JTE) | **A J1900-ra teszi a renderelést** *(2.)*. Plusz: GraalVM natív image mellett a sablonmotorok **reflexiós konfigurációt** igényelnek — pluszmunka, nem megtakarítás |
| **htmx** | Kevesebb JS, **de több szerver-körút** — a szűk erőforrás itt épp a szerver |
| **Blazor Server** | **Állandó kapcsolat + szerveroldali UI-állapot minden felhasználóra.** A legrosszabb illeszkedés a J1900-hoz |
| **Két külön admin** (felhős + helyi) | ⛔ **Kifejezetten megtiltottuk** *(§22.2)* — a néma szétcsúszás forrása |
| **`shadcn`, `migrate-radix-to-base` skillek** | Csak akkor, ha React lesz — **és akkor is csak ha tényleg használjuk** *(SKILLEK §4)* |
| **Mobilalkalmazásként is** | Az admin **ülve, gondolkodva** használt felület *(R7)*. A mobil eset a vékonykliens, az **Flutter** |

---

## 7. Nyitott — ez dönti el a javaslatot

| # | Kérdés |
|---|--------|
| **W1** | **Milyen frontend tapasztalat van a csapatban?** ⚠️ **Ez erősebb szempont, mint bármelyik fenti technikai érv.** Egy ismert keretrendszer közepes illeszkedéssel gyorsabb, mint egy ismeretlen tökéletes |
| **W2** | **Van-e C# fronton tapasztalat?** Ha erős C# és gyenge JS a helyzet, a **Blazor WASM felülírja a javaslatot** — az adatrács-hátrány kisebb baj, mint egy ismeretlen nyelv |
| **W3** | **A Garm vagy a Hermes admin felülete milyen technológián van?** Ha van már működő, ismert stack, **erős érv mellette** — közös komponensek, közös tudás, és a Myth System alatt egységes kép |
