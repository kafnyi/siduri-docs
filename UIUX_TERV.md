# UI/UX terv — POS, vékonykliens, KDS, kijelzők, admin

**Utolsó frissítés:** 2026-08-23
**Fázis:** F1-nel párhuzamos; a felület alakja **visszahat az API-ra**, ezért a kód előtt
**Forrás:** a feltöltött `UiUX/` skill-készlet + a specifikáció kényszerei

---

## 0. Mit adott a skill-készlet, és mit nem — őszintén

Átnéztem a hét skillt. **Nem minden része alkalmazható ránk, és ezt jobb kimondani,
mint úgy tenni, mintha többet kaptunk volna.**

| Rész | Használható? |
|------|--------------|
| **`ux-guidelines.csv`** (119 irányelv) | **IGEN** — érintés, visszajelzés, űrlap, akadálymentesség. Közvetlenül alkalmazható |
| **`stacks/wpf.csv`** (57) és **`stacks/flutter.csv`** (53) | **IGEN, és ez a legértékesebb** — konkrét megvalósítási szabályok, teljesítmény-tételekkel, ami a J1900 miatt kritikus |
| **`app-interface.csv`** (32) | Részben — mobil-app fókuszú, de az érintés/visszajelzés része áll |
| `colors.csv`, `typography.csv`, `motion.csv` | Részben — alapelvek igen, konkrét paletták nem |
| **`ui-reasoning.csv`** (192 termékprofil) | ⚠️ **NEM.** Végignéztem: **nincs benne POS, pénztár, érintőkasszás vagy vendéglátós kategória.** A 192 profil web/SaaS/landing-page termékekre szól (Financial Dashboard, NFT Platform, Newsletter…) |
| `banner-design`, `slides`, `brand`, `design` | Most nem — marketing- és prezentációs anyagokra valók. **A `brand` skill később, a Myth System arculatához** |

> **Ezért a stílus- és palettadöntéseket NEM lehet a készletből átvenni.** Azokat
> a **működési környezetből** vezetjük le (2. szakasz), és a készlet szabályait
> **ellenőrzésként** használjuk rá.

---

## 1. Miért nem másolható a webes UX ide

**Ez a szakasz a dokumentum legfontosabb része.** A szokásos UX-tanácsok jelentős
része **egy POS-on kifejezetten káros**, mert más a használati mód.

| Webes/SaaS alapfeltevés | A POS valósága |
|-------------------------|----------------|
| A felhasználó **felfedez** | A pénztáros **ugyanazt a 20 gombot nyomja napi 500-szor.** A felfedezhetőség az adminnak számít, a kasszának **nem** |
| Van **hover** | **NINCS.** Érintőképernyőn a hoverre épülő jelzés **hiba**, nem finomság |
| A felhasználó **ül és figyel** | **Áll, siet, vendég néz rá**, és zajos a környezet |
| A felhasználó **elolvassa** a párbeszédablakot | **Csúcsban nem.** Amit minden alkalommal kidob a rendszer, azt **elkattintják** — ezt már egyszer levezettük a 18+ figyelmeztetésnél |
| A kéz **tiszta és száraz** | **Zsíros, nedves, néha kesztyűs** |
| Az **esztétika** eladja a terméket | **A sebesség adja el.** Egy szép, de lassú kassza megbukik |
| **Megerősítés** véd a hibától | **A visszavonás véd.** A megerősítés csak reflexet nevel |

### 1.1 A négy vezérelv, ami ezekből következik

| # | Elv |
|---|-----|
| **U1** | **Sebesség > felfedezhetőség** — a kasszán. Az adminban fordítva |
| **U2** | **Hibamegelőzés > hibaüzenet.** Ami nem üthető félre, arról nem kell üzenetet írni |
| **U3** | **Visszavonás > megerősítés.** Megerősítés csak **visszafordíthatatlan ÉS ritka** műveletre. Ami gyakori, arra visszavonás jár |
| **U4** | **Az állapot legyen ambiens, ne felugró.** A tartós sáv és a piktogram nem kattintható el; a felugró ablak igen — és el is fogják *(N0.3)* |

---

## 2. Kemény korlátok

| # | Korlát | Következmény |
|---|--------|--------------|
| K1 | **J1900 / Bay Trail integrált GPU** | Kevés árnyék, kevés áttetszőség, **semmi üveghatás**. Az animáció rövid és ritka. `[MÉRENDŐ]` M3 |
| K2 | **Jellemzően 1024×768 vagy 1366×768 érintőkijelző** | **Szűkös hely.** Minden képernyőnek van hely-költségvetése (7. szakasz) |
| K3 | **A német szöveg 25–35%-kal hosszabb a magyarnál** | **Németül kell tesztelni, nem magyarul** *(§25)* |
| K4 | **Zsíros/nedves ujj, sietség** | Nagy célfelület, nagy térköz |
| K5 | **Zajos környezet** | **A hangjelzés nem elsődleges visszajelzés.** Vizuális az elsődleges *(§N3.c)* |
| K6 | **A vonalkód-olvasó billentyűzetként viselkedik** | **Fókuszkezelési kényszer** *(§1.3.2)* |
| K7 | **Vendég is látja a képernyőt** | Ami érzékeny (árrés, beszerzési ár), **az a kasszán ne legyen látható** |

---

## 3. Felület-leltár

| # | Felület | Eszköz | Használati mód |
|---|---------|--------|----------------|
| 1 | **POS — értékesítés** | Windows POS | Álló, gyors, ismétlődő |
| 2 | **POS — asztaltérkép** | Windows POS | Álló, tájékozódó |
| 3 | **POS — napi/műszak műveletek** | Windows POS | Ritka, pontos |
| 4 | **Vékonykliens — rendelésfelvétel** | telefon/tablet | Járkálva, egy kézzel |
| 5 | **KDS** | konyhai kijelző | **2 méterről, gőzben, kézmosás után** |
| 6 | **Rendeléskijelző** | TV | **5 méterről, vendég olvassa** |
| 7 | **Másodkijelző** | vendégoldali | Passzív, vendég olvassa |
| 8 | **Webes admin** | böngésző | **Ülve, gondolkodva** — itt a webes UX-szabályok ÉRVÉNYESEK |

> **A 8. felület más világ.** Ott a felfedezhetőség, a sűrűség és a
> billentyűzet-hatékonyság számít — **ne vigyük át rá a kassza szabályait**,
> és fordítva se.

---

## 4. Interakció-költségvetés a kritikus folyamatokra

**Számban kifejezett, ellenőrizhető cél.** Ha egy folyamat túllépi, az tervezési hiba.

| Folyamat | Cél (érintés) | Megjegyzés |
|----------|---------------|------------|
| Gyorseladás: 1 termék → készpénz → nyomtat | **≤ 4** | termék · fizetés · készpénz · pontos összeg |
| Termék asztalra ütése (kedvenc) | **≤ 2** | kategória nélkül, közvetlen gomb |
| Termék módosítóval | **≤ 4** | a módosító felugró **magától** jön, ha kötelező |
| Asztalnyitás → első tétel | **≤ 3** | |
| Számla kérése az asztalra | **≤ 3** | |
| Fizetés kártyával | **≤ 3** | az integrált terminál magától megkapja az összeget |
| Következő fogás indítása | **≤ 2** | |
| Műszakzárás vakzárással | **≤ 6** | címletkalkulátorral együtt |

**Két szabály ezekhez:**

* **A leggyakoribb termékek soha ne legyenek kategórián belül.** Kell egy „kedvencek" rács, amit az ügyfél állít.
* **A képernyők közötti váltás is számít érintésnek.** Négy érintés két képernyőváltással lassabb, mint hat egy képernyőn.

---

## 5. Érintés és méretezés

A skill-készlet minimumai (**44pt iOS / 48dp Android / 24×24 CSS px WCAG**)
**telefonra, kézben tartva** szólnak. **Egy pultra állított kassza más eset.**

| Elem | Minimum | Cél |
|------|---------|-----|
| **Elsődleges akciógomb** (fizetés, termék) | **64 px** | **72–80 px** |
| Másodlagos gomb | 56 px | 64 px |
| Listaelem (tétel a kosárban) | 56 px | 64 px |
| Numerikus billentyűzet gombja | **72 px** | 80 px |
| **Térköz célfelületek között** | **12 px** | 16 px |
| **Veszélyes gomb** (sztornó, törlés) közelsége | **min. 24 px** minden mástól | és **vizuálisan elkülönítve** |

> **A veszélyes gomb távolságtartása nem esztétika, hanem hibamegelőzés (U2).**
> A sztornó soha ne legyen a „fizetés" mellett.

**Fitts törvénye a mi esetünkre:** a leggyakoribb akciók a **képernyő szélére
vagy sarkába** kerüljenek, mert ott a célfelület gyakorlatilag végtelen —
az ujj nem tud „túlmenni" rajta.

---

## 6. Tipográfia

| Szerep | Méret | Megjegyzés |
|--------|-------|------------|
| **Összeg a fizetőképernyőn** | **32–40 px** | A legfontosabb szám a képernyőn |
| Gombfelirat | **18–20 px** | 16 px már kicsi álló használatnál |
| Tételsor | 16–18 px | |
| Alapszöveg | **min. 16 px** | ez alá **soha** |
| Segédszöveg | min. 14 px | ritkán |
| **KDS** | **24–32 px** | 2 méterről olvasható |
| **Rendeléskijelző** | **60 px+** | 5 méterről olvasható |

| # | Szabály |
|---|---------|
| a | **Sorköz 1,4–1,5** — a készlet 1.5-öt ír, a sűrű listákon 1,4 elfogadható |
| b | **Számokhoz táblázatos (tabular) számalak**, hogy az összegek oszlopban álljanak |
| c | **A pénzösszeg soha nem tördelhető, és soha nem rövidül `…`-tal** |
| d | ⚠️ **Minden gombfeliratot NÉMET szöveggel kell tesztelni** *(K3)* |

---

## 7. Elrendezés-költségvetés — **1024×768 a TERVEZÉSI CÉL**

> **Az első ügyfél legkisebb gépe 1024×768.** Ez tehát **nem a legrosszabb eset,
> amit még elviselünk, hanem a tervezési alap.** Ami 1024×768-on működik, az
> 1366×768-on és felette is működni fog; fordítva nem.

**Ez szűkösebb, mint elsőre látszik.** Levonva az állapotsávot (48 px) marad
**720 px magasság** — abba kell férnie a kosárnak, az összegnek és a fizetés
gombnak.

```
1024 × 768
┌──────────────────────────────────────────────────┐
│ ÁLLAPOTSÁV — 48 px, csak ha VAN mit mondani      │ 0 v. 48
├───────────────────────────┬──────────────────────┤
│                           │ KOSÁR                │
│ TERMÉKRÁCS                │ virtualizált lista   │
│ 600 px (~59%)             │ 424 px (~41%)        │ 720
│                           │ ~7 tétel látszik     │
│ 4 oszlop × 140 px gomb    ├──────────────────────┤
│ vagy 3 × 190 px           │ ÖSSZEG — 88 px       │
│                           ├──────────────────────┤
│                           │ FIZETÉS — 96 px      │
└───────────────────────────┴──────────────────────┘
```

| # | Számított korlát |
|---|------------------|
| a | **Termékrács: 4 oszlop × 140 px** (12 px térközzel) **vagy 3 × 190 px.** Ötnél több oszlop 1024-en már 64 px alá viszi a gombot → **tilos** |
| b | **A kosárból ~7 tétel látszik** 64 px-es sorokkal. Egy 12 tételes asztalnál görgetni kell → **a görgetés ténye legyen látható**, ne meglepetés |
| c | **Az összeg (88 px) és a fizetés (96 px) FIX** — összesen 184 px a jobb oldal aljából. Ezt semmi nem eheti meg |
| d | **Kedvencek: az első sor mindig kedvencek**, kategóriaváltás nélkül elérhetően *(4. szakasz)* |

| # | Szabály |
|---|---------|
| e | **A kosár és az összeg SOHA nem tolódik el** attól, hogy megjelenik az állapotsáv — a sáv **helyet foglal, nem takar** |
| f | **Az összeg és a fizetés gomb fix helyen van.** Az izommemória a legértékesebb, amit egy pénztáros felépít — **elmozdítani bűn** |
| g | **A két oldal külön görgethető, de soha nem egyszerre** |
| h | **Nincs vízszintes görgetés sehol** |
| i | ⚠️ **A német szöveg + 1024 px a legszűkebb együttállás** — a gombfelirat-teszt (K3) **1024×768-on, németül** futtatandó, nem 1366-on magyarul |

## 8. Szín — a Siduri paletta a logóból

A logó megvan, tehát a paletta **nem nyitott kérdés többé.** Kimintáztam:

| Szerep a logóban | Érték | Kontraszt fehéren |
|------------------|-------|-------------------|
| **Mélykék / petróleum** — ruha, körvonal, felirat | **`#003544`** | **13,2 : 1** ✅ |
| **Arany / okker** — szegély, ékszer, mintázat | **`#B08442`** | **3,4 : 1** ⚠️ |
| Sötét olíva — amfora | `#303024` | *(dekoratív, UI-ban nem használjuk)* |
| Háttér | `#FFFFFF` / `#F8F8F8` | |

### 8.1 `[FONTOS]` Az arany szép, de NEM lehet akciószín

**Ezt ki kell mondanom, mielőtt beleépülne.**

| Mérés | Eredmény |
|-------|----------|
| `#B08442` fehéren | **3,37 : 1** → **megbukik a 4.5:1-en** |
| `#B08442` petrolon | **3,91 : 1** → **megbukik** |

> **Az arany a logóban tökéletes — de a POS-on nem lehet gombfelirat, nem lehet
> szöveg fehéren, és nem lehet elsődleges akciószín.** Nem stílusdöntés:
> **egy 1024×768-as érintőkijelzőn, oldalról nézve, zsíros ujjlenyomatokkal
> egyszerűen nem olvasható.**

**Megoldás — két aranyváltozat, szerep szerint szétválasztva:**

| Token | Érték | Kontraszt | Mire |
|-------|-------|-----------|------|
| `arany.marka` | **`#B08442`** | 3,4:1 | **Csak dekoráció**: logó, elválasztó, keret, nagy fejlécszám. **Szöveg SOHA** |
| `arany.szoveg` | **`#8A6A2E`** | **5,0 : 1** ✅ | Aranyszínű **szöveg** fehéren, ha kell |
| `arany.vilagos` | **`#D4A24A`** | **5,7 : 1** petrolon ✅ | **Sötét háttéren** — sáv, sötét mód, kiemelés |

### 8.2 Szemantikus szerepek

| Szerep | Érték | Kontraszt | Megjegyzés |
|--------|-------|-----------|------------|
| **Elsődleges akció** (fizetés) | **`#003544`** petrol | 13,2:1 | **A márka fő színe = a fő akció.** Nem az arany |
| **Alap felület** | `#FFFFFF` | — | |
| **Másodlagos felület** | `#F4F6F7` | — | halvány, petrol felé hajló szürke |
| **Szöveg** | `#003544` | 13,2:1 | ugyanaz, mint az elsődleges — egységes |
| **Halvány szöveg** | `#4A6B77` | 4,6:1 | épphogy megfelel; ennél halványabb nincs |
| **Veszély** (sztornó, törlés) | **`#B3261E`** | 6,5:1 | ⚠️ **A logóban NINCS piros — be kell hozni** |
| **Siker** | **`#1B6E3C`** | 6,3:1 | ⚠️ **Zöld sincs a logóban** |
| **Figyelem** (csökkentett mód) | **`#8A5A00`** borostyán | 5,9:1 | Elkülönül a veszélytől ÉS az aranytól |

> ⚠️ **A veszély, siker és figyelem színt be KELLETT hoznom, mert a logóban
> nincs.** Egy logó két színnel megél; **egy POS nem** — ott a piros és a zöld
> jelentést hordoz, és **a jelentéshordozó szín nem lehet márkaszín.**
>
> **A borostyán tudatosan távol áll az aranytól** — különben a „figyelem"
> összekeveredne a dekorációval, és pont akkor nem tűnne fel, amikor kell.

### 8.3 A logó jellege a felületen

A logó **vékony vonalas, klasszikus, sok apró mintázattal.** Ebből három dolog
következik a UI-ra:

| # | Következmény |
|---|--------------|
| a | **A vékony vonal a márkajegy** → a felületen **1–2 px-es keretek**, nem vastag határok, nem tömör kitöltések mindenütt |
| b | ⚠️ **A finom mintázat NEM vihető át a felületre.** Bay Trail iGPU-n a textúra drága *(K1)*, és 1024×768-on olvashatatlan zaj. **A mintázat a bejelentkező képernyőn és a nyomtatott fejlécen él, a kasszafelületen nem** |
| c | **Bőséges fehér tér** — a logó is így épül fel. **Ez ütközik a képernyő szűkösségével**, tehát: fehér tér a bejelentkezésen és az adminban, **sűrűség a kasszán** |

### 8.4 Szabályok

| # | Szabály |
|---|---------|
| 8.a | **Kontraszt minimum 4.5:1** normál szövegre, 3:1 nagy szövegre *(WCAG AA)* |
| 8.b | ⚠️ **Színnel önmagában SOHA nem közlünk információt** — mindig ikon vagy szöveg is. Kritikus: egy vörös-zöld tévesztő pénztáros nem láthatja rosszul a csökkentett módot |
| 8.c | **Nyers hexa érték komponensben tilos** — csak szemantikus token |
| 8.d | **`arany.marka` szövegre soha** |

### 8.5 `[DÖNTÉS]` Világos vagy sötét?

**Világos az alapértelmezés, sötét választható — ESZKÖZÖNKÉNT, nem telephelyenként.**

**Miért eszközönként:** egy étteremben a **pult** világos térben áll, a **bár**
gyakran félhomályban — **ugyanazon a telephelyen.** Ez ugyanaz a mintázat, mint a
fiskális üzemmódnál *(§9.2)*: **ami eszközfüggő, azt eszközre kell kötni.**

*(A skill-készlet „Financial Dashboard → sötét alapértelmezés" ajánlása
képernyőre tapadó elemzői munkára szól, nem pultra állított kasszára.)*

### 8.6 `[SZABÁLY]` A letiltott gomb nem elég, ha csak halványabb

A készlet szerint „csökkentett átlátszóság + más kurzor". **Kurzor nincs.**
Ezért: a letiltott gomb **más kitöltést, csökkentett kontrasztot ÉS hiányzó
árnyékot** kap, és **megnyomásra megmondja, MIÉRT tiltott** — nem néma.

---

## 9. `[FONTOS]` Az állapot vizuális nyelve

**Ez a szakasz köti össze a specifikáció szétszórt jelzéseit egyetlen rendszerré.**
Eddig külön-külön határoztunk meg sávokat és jelzéseket; **egy pénztárosnak
EGY mintát kell megtanulnia.**

### 9.1 A négy állapotszint

| Szint | Mikor | Megjelenés | Elkattintható? |
|-------|-------|------------|----------------|
| **Normál** | minden rendben | **nincs sáv** | — |
| **Tájékoztat** | nincs internet · fordítás hiányzik | **halk jelzés**, nem sáv | igen |
| **Figyelmeztet** | csökkentett mód · integráció kikapcsolva · 23:00 napzárás-figyelmeztetés | **tartós sáv, elrejthetetlen** | **NEM** |
| **Blokkol** | óra > 2 óra eltérés · 23:45 kényszerzárás · nincs hely az auditnak | **teljes képernyős, kiúttal** | **NEM** |

### 9.2 A sáv szabályai

| # | Szabály |
|---|---------|
| a | ⚠️ **A sáv a TEENDŐT mondja meg, ne csak az állapotot.** Nem „adóügyi integráció kikapcsolva", hanem **„…— a nyugtát a különálló pénztárgépen adja ki"** *(§19.4/d)* |
| b | **Helyet foglal, nem takar** — a kosár és az összeg nem ugrik el alatta |
| c | **Kiírja, mióta tart és meddig** *(§19.4/e)* |
| d | **Egyszerre több ok is lehet** → a sáv **összevon**, nem halmoz egymásra sávokat |
| e | **Az „internet nincs" SOHA nem figyelmeztetés-szintű**, mert az nem hibaállapot *(§6.5)* |

### 9.3 Kis, tartós jelzések

| Jelzés | Hol | Szabály |
|--------|-----|---------|
| **18+ piktogram** | a felütött tétel során | Ambiens, **soha nem felugró** *(N0.3)* |
| **Allergén gomb** | a terméken | **Csak ott, ahol VAN adat** *(N0.1)* |
| **„Elfogyott"** | a termékgombon | **Kiszürkíti** — ez a mínuszos készlettel ellentétben valós információ *(§17.6/c)* |
| **Visszatartott fogás** | a KDS-en | **„Jön, de még ne kezdd"** — elkülönítve *(§20.1/d)* |

---

## 10. Mozgás

| # | Szabály |
|---|---------|
| a | **A mozgás jelentést hordoz vagy nincs.** Díszítő animáció a POS-on tilos |
| b | **Időtartam 120–200 ms.** A 0 ms hiba (nincs visszajelzés), a 300 ms felett lassúnak érződik |
| c | ⚠️ **Szélesség/magasság SOHA nem animálódik** — csak áttetszőség és eltolás. Bay Trail iGPU-n az elrendezés-animáció akadozik |
| d | **A `prefers-reduced-motion` tiszteletben tartva** |
| e | **A nyomott állapot azonnali** (< 50 ms), különben a pénztáros kétszer nyom |

---

## 10.1 `[ELDÖNTVE]` Fizikai billentyűzet — van, ahol van

**Az első ügyfélnél vegyes: némelyik gépnél van fizikai billentyűzet, némelyiknél
nincs.** Ez nem opció, hanem kényszer.

> **A teljes eladási folyamatnak működnie kell billentyűzet NÉLKÜL is, és
> billentyűzettel is — de a billentyűzet SOHA nem előfeltétel.**

| # | Szabály |
|---|---------|
| a | **Minden funkció elérhető érintéssel.** Gyorsbillentyű nélkül is teljes a rendszer |
| b | **Ahol van billentyűzet, ott gyorsítson** — de a gyorsbillentyű **soha nem az egyetlen út** valamihez |
| c | ⚠️ **A billentyűzet-támogatás akkor is KÖTELEZŐ, ha nincs billentyűzet** — mert **a vonalkód-olvasó billentyűzetként viselkedik** *(K6)*. A fókuszkezelésnek működnie kell akkor is, ha ember sosem gépel |
| d | **A gyorsbillentyűk NEM jelennek meg a felületen** azokon a gépeken, ahol nincs billentyűzet — különben hazudik a felület |
| e | **Numerikus billentyűzet a képernyőn MINDIG van**, akkor is, ha fizikai is van. A pénztáros nem néz le |

## 10.2 `[ELŐKÉSZÍTVE, DE NEM ÉPÜL MEG]` Termékkép

**Kép most nem kell — de a szerkezetnek bírnia kell**, hogy később ne
adatmodell-változás legyen belőle.

| # | Előkészítés |
|---|-------------|
| a | **`kep_azonosito` mező a terméken és a kiszerelésen**, üresen. **Most nem használjuk** |
| b | **A képek a felhőben tárolódnak**, a telephely gyorsítótáraz. ⚠️ **A 64 GB-os SSD-be nem fér bele korlátlan kép** *(§24.2)* — a gyorsítótár méretkorlátos |
| c | ⚠️ **A termékgomb elrendezése NE változzon meg attól, hogy kap képet.** A gomb már most fenntartja a helyet — különben a bekapcsolás **átrendezi a rácsot, és megöli az izommemóriát** *(7.f)* |
| d | **A képes rács külön mérés** *(K1, M3)*: 4×5 = 20 kép egy Bay Trail iGPU-n **nem triviális.** Bekapcsolás előtt mérni kell |
| e | **A képes mód eszközönként kapcsolható**, mint a sötét mód *(8.5)* — a pult lehet képes, a bár szöveges |

## 11. Komponens-döntések

| Komponens | Döntés |
|-----------|--------|
| **Termékgomb** | Név + ár. **Kép opcionális**, mert a képes rács a J1900-on drága, és a gyakorlott pénztáros a helyre emlékszik, nem a képre |
| **Kosár tétele** | Név · mennyiség · sorösszeg. A módosítók **alatta, kisebben, behúzva** |
| **Numerikus billentyűzet** | **Elsőrangú komponens** — mennyiség, ár, PIN, átvett készpénz. Mindig ugyanaz az elrendezés |
| **Módosító-felugró** | **Magától jön, ha kötelező** (`min ≥ 1`). Nem kell megkeresni |
| **Menü-felugró** | Komponensenként lépteti végig, **amíg mind ki nincs töltve** *(§13.4)* |
| **Megerősítés** | **Csak visszafordíthatatlan ÉS ritka műveletre.** És **számmal mondja meg a következményt**, ne igen/nem legyen *(a „nyomd meg a zöldet" reflex ellen)* |
| **Visszavonás** | Gyakori műveletekre, néhány másodperces ablakkal |
| **Üres állapot** | **Soha nem üres képernyő** — mondja meg, mi a következő lépés |

---

## 12. Stack-szabályok *(a skill-készletből, ránk szűrve)*

### 12.1 WPF — a J1900 miatt kritikus tételek

| # | Szabály | Miért nálunk |
|---|---------|--------------|
| a | **`VirtualizingStackPanel` minden hosszú listára** | Egy 800 tételes terméklista **egyszerre nem létezhet** a memóriában |
| b | **`Freeze()` minden `Freezable`-re** (ecsetek, geometriák) | A változáskövetés elhagyása mérhető Bay Trailen |
| c | **`async` minden hosszú műveletre**, `Task.Run` a CPU-igényesre | A fiskális eszköz válasza **másodperces** lehet — az UI szál nem várhat rá |
| d | **`Dispatcher` minden UI-frissítéshez** | |
| e | **`DispatcherUnhandledException` kezelve** | ⚠️ **A WPF alapértelmezett összeomlás-ablaka egy kasszán elfogadhatatlan.** Naplózni és kezelni kell |
| f | **MVVM, `INotifyPropertyChanged`, `ObservableCollection`, `ICommand`** | Szerkezeti alap |
| g | **`AutomationProperties` beállítva, teljes billentyűzet-elérés** | Nem elvi: **a vonalkód-olvasó billentyűzet** *(K6)* |

### 12.2 Flutter — vékonykliens, KDS, kijelzők

| # | Szabály |
|---|---------|
| a | **`ListView.builder`** minden listára · **kulcsok** az állapottal bíró elemekre |
| b | **`const` widgetek**, minimális újraépítési hatókör, **`RepaintBoundary`** a gyakran változó részekre *(KDS-időzítők!)* |
| c | **Vezérlők és feliratkozások eldobása** (`dispose`) — a KDS **napokig fut megszakítás nélkül**, ott a szivárgás halálos |
| d | **Betöltési ÉS hibaállapot mindkettő kezelve** |
| e | **`PopScope`** az Android vissza-gombra — **a rendelésfelvétel közepén a vissza nem dobhatja el a kosarat** |
| f | **`Semantics`**, nagy betűméret támogatása (`TextScaler`) |

---

## 13. Anti-minták — amit soha

| # | Tilos | Miért |
|---|-------|-------|
| 1 | **Hoverre épülő jelzés** | Érintőképernyőn nem létezik |
| 2 | **Felugró ablak gyakori műveletre** | Reflexszerűen elkattintják *(U3, N0.3)* |
| 3 | **A fizetés gomb elmozdítása** | Az izommemória a legértékesebb eszköz |
| 4 | **Szélesség/magasság animálása** | Bay Trail iGPU-n akadozik |
| 5 | **Csak színnel közölt információ** | Színtévesztés + WCAG |
| 6 | **Néma sikertelenség** | *(A2 elv, I29)* |
| 7 | **Beszerzési ár vagy árrés a kasszán** | A vendég is látja *(K7)* |
| 8 | **Vízszintes görgetés** | |
| 9 | **12 px alatti szöveg** | |
| 10 | **Hangjelzés mint egyetlen visszajelzés** | Zajos környezet *(K5)* |
| 11 | **Emoji ikon helyett** | A készlet külön kiemeli; és a betűkészletfüggés kiszámíthatatlan |
| 12 | **Üveghatás, erős árnyék, elmosás** | *(K1)* |

---

## 14. Elfogadási kritériumok — mérhetően

| # | Kritérium |
|---|-----------|
| 1 | **Minden kritikus folyamat a 4. szakasz érintés-költségvetésén belül** |
| 2 | **Minden gombfelirat kifér NÉMET szöveggel**, 1366×768-on és 1024×768-on |
| 3 | **Minden célfelület ≥ az 5. szakasz minimuma**, térközzel |
| 4 | **Kontraszt ≥ 4.5:1** minden szövegre |
| 5 | **Minden információ elérhető szín nélkül is** |
| 6 | **A fizetés gomb és az összeg pozíciója változatlan** minden állapotban |
| 7 | **Nincs 200 ms-nál hosszabb animáció**, és nincs elrendezés-animáció |
| 8 | **A teljes eladási folyamat elvégezhető billentyűzetről** *(vonalkód-olvasó)* |
| 9 | **A KDS 2 méterről, a rendeléskijelző 5 méterről olvasható** |
| 10 | ⚠️ **Mindezt valós J1900-on, valós érintőkijelzőn** — nem fejlesztői gépen |

---

## 15. Nyitott kérdések

| # | Kérdés |
|---|--------|
| ~~D1~~ | ~~Márkapaletta~~ → **MEGVAN, a logóból kimintázva (8. szakasz).** Petrol `#003544` + arany `#B08442`, plusz a **behozott** veszély/siker/figyelem szín. A Myth System **cégarculata** külön kérdés marad |
| ~~D2~~ | ~~Termékkép?~~ → **MOST NEM, de előkészítve (10.2).** Mező üresen, hely fenntartva, felhős tárolás, méréshez kötött bekapcsolás |
| ~~D3~~ | ~~Fizikai billentyűzet?~~ → **VEGYES (10.1).** Van, ahol van. A rendszer billentyűzet nélkül is teljes, de a billentyűzet-támogatás a vonalkód-olvasó miatt kötelező |
| ~~D4~~ | ~~Felbontás?~~ → **1024×768 a legkisebb gépen → EZ A TERVEZÉSI CÉL (7. szakasz)**, nem a tűrt legrosszabb eset |
| **D5** | **A Myth System CÉGARCULATA** — a Siduri terméképe megvan; a cég szintű arculat (Garm, Hermes, Siduri együtt) külön kör, a `brand` skillel |
