# Az eseménycsatorna `[S1 — ELDÖNTVE]`

**Létrehozva:** 2026-08-26
**Mit dönt el:** hogyan jut el a szerver felől érkező változás a kliensekhez.

---

## 1. Mi a valódi kérdés — és mi nem

**Nem az, hogy „melyik technológia a modernebb".** Négy konkrét képernyő van,
aminek magától kell frissülnie:

| Képernyő | Mit kell megtudnia | Mi történik, ha késve tudja meg |
|----------|--------------------|---------------------------------|
| **KDS (konyhai kijelző)** | Új tétel érkezett a konyhára | ⚠️ **A szakács nem kezdi el az ételt.** Ez azonnal vendégidő |
| **Rendeléskijelző** | Egy rendelés elkészült | A vendég áll a pultnál, és nem tudja, mikor mehet |
| **Asztaltérkép** | Egy asztalhoz hozzáütöttek | Két pincér ugyanarra az asztalra dolgozik |
| **POS állapotsáv** | Csökkentett mód, integráció tiltva | A pénztáros olyan műveletet kezd, ami nem fog sikerülni |

**A kérdés tehát: mennyi késleltetés elfogadható, és mi történik, ha a csatorna
elszakad.** A második a fontosabb.

---

## 2. `[ELV]` A csatorna soha nem az igazság egyetlen forrása

**Ezt a döntés előtt kell kimondani, mert bármelyik technológiánál érvényes:**

> **Egy elveszett esemény némán rossz képernyőt hagy maga után, és a szakács a
> rossz képernyőről főz.**

Ebből három kötelező tulajdonság következik:

| # | Követelmény | Miért |
|---|-------------|-------|
| a | **Teljes állapot mindig lekérdezhető** — kérés-válasz úton, a csatornától függetlenül | Ez az, amire vissza lehet esni |
| b | **Minden esemény sorszámozott** a már meglévő `(epoch, számláló)` párral | Így a kliens tudja, hogy lemaradt, és nem kell találgatnia |
| c | ⚠️ **A kliens LÁTHATÓAN jelzi, ha a csatorna elavult** | **Egy némán elavult KDS rosszabb, mint egy láthatóan leszakadt.** Ha nincs kapcsolat, azt látni kell — nem elhinni, hogy nincs új rendelés |

**A (c) a legfontosabb, és a legkönnyebb elfelejteni.** Egy TCP-kapcsolat percekig
„nyitva" maradhat egy halott szerver felé; a kliens nem tudja meg magától.

---

## 3. A négy jelölt

| | WebSocket | SSE | Hosszú lekérdezés | Lekérdezés |
|---|---|---|---|---|
| **Irány** | kétirányú | csak szerver→kliens | csak szerver→kliens | csak kliens kér |
| **Késleltetés** | ezredmásodperc | ezredmásodperc | ezredmásodperc | a periódus fele, átlagban |
| **Kapcsolatok száma** *(12 kliens)* | 12 tartós | 12 tartós | 12 függő kérés | 12 × periódusonként |
| **.NET kliens** | **beépített** (`ClientWebSocket`) | ⚠️ **nincs beépített kliens** — kézzel kell értelmezni a folyamot | beépített | beépített |
| **Dart / Flutter** | **beépített** | csomagból | beépített | beépített |
| **Böngésző** | **beépített** | **beépített** (`EventSource`) | beépített | beépített |
| **GraalVM natív kép** | `[MÉRENDŐ]` | `[MÉRENDŐ]` | egyszerűbb | triviális |
| **Újracsatlakozás** | kézzel | **beépített** (`EventSource` újrapróbál) | kézzel | nem kérdés |

---

## 4. `[DÖNTÉS]` WebSocket

**Két ok dönti el, és egyik sem az, hogy „ez a modern".**

### 4.1 A .NET-ben nincs beépített SSE-kliens

**Ez a legkonkrétabb különbség.** A POS kliens C#/WPF. WebSocketre van beépített
osztály; SSE-re **nincs** — a folyamot kézzel kellene darabolni, az
újracsatlakozást és a `Last-Event-ID` kezelést magunknak megírni.

> **Vagyis az SSE „egyszerűbb" volta pont a mi legfontosabb kliensünkön nem
> érvényesül** — ott éppen ellenkezőleg: több kézzel írt kód kell hozzá, és
> minden kézzel írt protokollkezelés hibaforrás.

### 4.2 A KDS-nek visszafelé is beszélnie kell

A szakács a KDS-en jelzi, hogy egy tétel **elkészült**. Ez ugyanannak a
párbeszédnek a része, nem külön ügy.

SSE mellett ez külön kérés-válasz hívás lenne — ami **működne**, de akkor két
külön csatorna állapotát kellene együtt tartani, és a hibakezelés kétfelé ágazna.

### 4.3 Amit ezzel vállalunk — kimondva

| # | Költség | Hogyan kezeljük |
|---|---------|-----------------|
| a | **Az újracsatlakozás a mi dolgunk** | Egyetlen közös kliensoldali réteg, nem képernyőnként megírva |
| b | **Állapotos kapcsolat a szerveren** | 12 kapcsolat egy telephelyen — ez nem terhelés, ez könyvelés |
| c | **A GraalVM natív kép viselkedése ismeretlen** | **M23 mérés, blokkoló** *(6. fejezet)* |

---

## 5. `[DÖNTÉS]` A csatorna szabályai

### 5.1 Az esemény sorszáma ugyanaz a `(epoch, számláló)` pár

**Nem új mechanizmus.** Ugyanaz, ami a rekordok sorrendjét és a fencinget adja.

Ebből ingyen jön három dolog:

| # | Következmény |
|---|--------------|
| a | A kliens **pontosan tudja, hol tart**, és mit kért utoljára |
| b | **A régebbi generációjú esemény azonnal felismerhető** — egy leszakadt, majd visszatért régi szerver eseményeit a kliens eldobja |
| c | **A szerepváltás után nem kell külön „ürítsd a gyorsítótárat" üzenet** — az epoch változása maga az üzenet |

### 5.2 Újracsatlakozás: a szerver dönt, hogy pótol vagy újraküld

```
kliens:  "nálam (5, 1203) az utolsó"
szerver: → POTLAS      + a hiányzó események     (ha még megvannak)
         → UJRATOLTES  + "kérd le a teljes állapotot"  (ha túl régi)
```

**Az `UJRATOLTES` nem hibajelzés, hanem normális válasz.** A szerver véges
pufferben tartja az eseményeket; ha a kliens ennél régebbi, a teljes állapot
lekérése **olcsóbb és biztosabb**, mint órákat visszajátszani.

> ⚠️ **Ami tilos: csendben folytatni onnan, ahol a szerver tud.** A kliens ilyenkor
> azt hinné, hogy naprakész, holott lyuk van a történetében.

### 5.3 Szívverés — a néma szakadás ellen

| # | Szabály |
|---|---------|
| a | **A szerver másodpercenként küld szívverést** a csatornán |
| b | ⚠️ **Ha a kliens 5 másodpercig nem kap semmit, a csatornát elavultnak tekinti** — nem várja meg a TCP időtúllépését, ami percekig is eltarthat |
| c | **Az elavult csatorna LÁTSZIK a felületen** — a KDS és a rendeléskijelző jelzi, hogy amit mutat, nem friss |
| d | Az újracsatlakozás **növekvő várakozással** próbálkozik, de a **felső korlát 5 másodperc** — egy konyhai kijelző nem várhat percet |

**Az (b) küszöb miért ilyen szoros:** egy csúcsforgalmú konyhán öt másodperc
alatt nem történik semmi visszafordíthatatlan, öt *perc* alatt viszont
kiszolgálatlan asztalok keletkeznek.

### 5.4 A csatorna nem hitelesít külön

Ugyanaz az eszközazonosság és munkamenet, mint a kérés-válasz úton. **Nincs
külön token a csatornához** — egy második hitelesítési út egy második
hibalehetőség, és semmivel nem véd jobban.

---

## 6. Mérési kötelezettség

| # | Mérés | Miért blokkoló |
|---|-------|----------------|
| **M23** | **A WebSocket-réteg natív képbe fordul-e**, és bírja-e a 12 tartós kapcsolatot a telephelyi gépen, POS-szal együtt futva | Ha nem fordul, a csatorna technológiája dől — és vele a KDS és a rendeléskijelző ütemezése. **A puszta keretrendszer-támogatás nem elég bizonyíték**, mert a natív kép hibái futásidőben jelentkeznek |

---

## 7. Mikor épül meg

**A döntés most kell, a megvalósítás nem.**

| Mi | Mikor | Miért ekkor |
|----|-------|-------------|
| **A boríték a szerződésben** *(esemény-azonosító, sorszám, epoch, típus)* | **most, F1** | Ugyanaz az ok, amiért az epoch mező az első naptól benne van: egy protokollmező utólagos felvétele **minden kliens minden verzióját** érinti |
| **A szerveroldali csatorna** | F5, a KDS-sel együtt | Előbb nincs kinek küldeni |
| **M23 mérés** | amint van referenciagép | Ha megbukik, a döntés újranyílik — és jobb, ha az F5 előtt derül ki |

---

## 8. Amit NEM döntöttünk el

| # | Nyitott |
|---|---------|
| **E1** | **Az esemény tartalma: teljes objektum vagy csak azonosító?** A „csak azonosító + kérdezd le" kisebb csomag és egyszerűbb érvénytelenítés, de **több kérés**. A KDS-nél a teljes objektum valószínűleg jobb; ezt az F5-ben, valós adaton kell eldönteni |
| **E2** | **Az eseménypuffer mérete** — ez dönti el, mikor jön `UJRATOLTES` az `POTLAS` helyett. Mérés kérdése, nem elvé |
