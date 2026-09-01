# Siduri — Az API-szerződés `[F1.1 / B8]`

**Létrehozva:** 2026-08-25
**Mit dönt el:** hol él a szerződés, hogyan verziózzuk, ki a gazdája, és mi
számít törésnek.

> **Ez az első dolog, ami elkészül, mert minden sáv erre épül** *(FÁZISTERV §3)*.
> Nem azért, mert érdekes, hanem mert **utólag ráhúzni egy szerződést négy
> különböző nyelven írt kliensre nem javítás, hanem újraírás.**

---

## 1. Nem egy szerződés van, hanem három

Ez a felismerés a szerkezetet is eldönti.

| # | Szerződés | Kik beszélnek | Ki valósítja meg |
|---|-----------|---------------|------------------|
| **K1** | **Kasszaprotokoll** | POS kliens (C#/WPF), PDA, KDS, rendeléskijelző, standoló (Dart) ↔ telephelyi szerver | **csak a telephelyi szerver** |
| **K2** | **Adminprotokoll** | Webes admin (Vue/TS) ↔ szerver | ⚠️ **KÉT megvalósítás: a felhő ÉS a telephelyi szerver** |
| **K3** | **Szinkronprotokoll** | Telephelyi szerver ↔ felhő | gép–gép, emberi felület nélkül |

### 1.1 ⚠️ A K2 a legfontosabb felismerés

A §22.2 kimondja: **„egy admin alkalmazás, két helyről kiszolgálva"**, és
megindokolja: két külön adminfelület **némán szétcsúszna.**

**Eddig ez ígéret volt. A K2-vel gépi kényszer lesz belőle:**

> **Ha az admin alkalmazás EGYETLEN generált kliensre fordul, és mindkét
> szervernek UGYANAZT a szerződést kell teljesítenie, akkor a szétcsúszás nem
> lassan derül ki egy ügyfélnél, hanem AZONNAL, egy szerződésteszt bukásaként.**

**Ez a különbség egy elv és egy invariáns között.** Az elvet be lehet tartani;
az invariánst nem lehet megsérteni.

### 1.2 Miért nem egy nagy szerződés

Mert **más a változási ütemük és más a kompatibilitási kényszerük**:

| | Ki frissül együtt | Mennyire tűr eltérést |
|---|---|---|
| **K1** | A telephely gépei, a frissítővel, egyszerre | **Kevéssé** — de a gördülő frissítés alatt órákig eltérhetnek |
| **K2** | A böngésző a betöltéskor mindig friss | **Alig kell tűrnie** |
| **K3** | ⚠️ **A felhő és a telephely SOHA nem frissül egyszerre** | **Erősen** — ez a legszigorúbb |

Egyetlen szerződésben a legszigorúbb kényszer húzná magával a másik kettőt.

---

## 2. `[DÖNTÉS]` Hol él — és miért pont ott

> **A három szerződés a `siduri-docs` repóban él, a `szerzodes/` könyvtárban.**

### 2.1 A döntő érv: körkörös függés

Ez nem kényelmi kérdés. Nézzük meg, mi történik a másik két lehetőséggel:

| Ha a szerződés a… | Mi lesz belőle |
|---|---|
| **…gyártó repójában él** | A `siduri-pos-client` függ a `siduri-backend-server`-től. A K2-nél viszont **két gyártó van** — a felhő és a telephely —, tehát vagy önkényesen kijelölünk egyet, vagy **körkörös függés keletkezik** |
| **…külön repóban él** | Hetedik repó, hat helyett. **Nem kérünk rá engedélyt egy elkerülhető dologért** |

> **A `siduri-docs` az egyetlen csúcs, amitől mind a hat repó függhet anélkül,
> hogy kör keletkezne.** Ez gráfelméleti tulajdonság, nem ízlés.

### 2.2 ⚠️ Ez módosítja a §30 szabályát — kimondva, nem csendben

A §30 azt írja: **„`siduri-docs` — dokumentáció, kód SOHA nem kerül bele."**

**Ezt módosítani javaslom, pontosítással:**

> **Kód soha. Szerződés igen.**

**Indoklás:** a szabály célja az volt, hogy **megvalósítás** ne keveredjen a
dokumentációba. **A szerződés nem megvalósítás, hanem specifikáció** — pont az
a fajta dolog, amiért a docs repó létezik. Az, hogy **kódot lehet belőle
generálni**, nem teszi kóddá; az adatbázisséma-leírásból is lehet.

**Amit a szabály továbbra is tilt, és ez él:** a `siduri-docs` **nem tartalmaz
generált klienst, megvalósítást, tesztet vagy build-konfigurációt.** Csak a
szerződésfájlokat és a hozzájuk tartozó változásnaplót.

### 2.3 A könyvtárszerkezet

```
siduri-docs/
  szerzodes/
    kassza/      v1/  kassza.yaml        (K1)
    admin/       v1/  admin.yaml         (K2)
    szinkron/    v1/  szinkron.yaml      (K3)
    kozos/            penz.yaml, ido.yaml, hiba.yaml, azonosito.yaml
    VALTOZASNAPLO.md
```

**A `kozos/` azért van, hogy a pénz, az idő és a hibaformátum leírása
mindhárom szerződésben ugyanaz legyen** — ne három, lassan széttartó változat.

---

## 3. `[DÖNTÉS]` Ki a gazdája

**A gazda nem repó, hanem szerep** — mert a K2-nek két megvalósítója van, és
egy repó nem tud dönteni.

| Szerep | Ki | Mit tesz |
|--------|-----|---------|
| **Szerződésgazda** | **Egy megnevezett személy** *(kezdetben: a telephelyi szerver vezetője)* | Minden szerződésváltozást ő hagy jóvá. **Nem technikai jog, hanem felelősség** |
| **Javaslattevő** | Bárki | Módosítást bárki javasolhat, a szokásos átnézési folyamattal |

**Egyetlen kikötés, ami nélkül a szerep üres:**

> **Szerződésváltozás nem mehet be ugyanabban a változtatásban, mint a
> megvalósítása.** Előbb a szerződés, külön, láthatóan. Utána a kód.

**Miért:** ha a kettő együtt megy, a szerződés **a megvalósítás
mellékterméke** lesz, és a jóváhagyás formalitássá válik — pontosan az, amit
el akarunk kerülni.

---

## 4. `[DÖNTÉS]` Verziózás

### 4.1 Fő verzió az útvonalban, additív változás azon belül

```
/kassza/v1/rendeles
/admin/v1/termek
/szinkron/v1/koteg
```

| Változás | Megengedett `v1`-en belül? |
|----------|---------------------------|
| **Új végpont** | igen |
| **Új, nem kötelező mező a válaszban** | igen |
| **Új, nem kötelező mező a kérésben** | igen |
| **Új felsorolás-érték** | ⚠️ **igen — de csak a 4.2 szabállyal együtt** |
| Mező törlése vagy átnevezése | **nem** → új fő verzió |
| Mező kötelezővé tétele | **nem** |
| Típus szűkítése, korlát szigorítása | **nem** |
| Mező jelentésének megváltoztatása | **nem** — és ez a legalattomosabb |

### 4.2 ⚠️ Az ismeretlen felsorolás-értéket TŰRNI kell — de nem elnyelni

**Új felsorolás-érték hozzáadása egy szigorú kliensnek törés.** Ezt nem úgy
oldjuk meg, hogy soha nem adunk hozzá, hanem szabállyal:

| # | Szabály |
|---|---------|
| a | **Minden kliens köteles az ismeretlen felsorolás-értéket beolvasni** — nem eshet el rajta a válasz feldolgozása |
| b | ⚠️ **De nem kezelheti úgy, mintha értené.** Az ismeretlen érték: `ISMERETLEN`, és a rá épülő művelet **hangosan elutasítva** |
| c | **Kijelzésnél megmutatjuk a nyers értéket**, nem üres helyet — a támogatás így tudja megmondani, mi történt |

**Miért ez a helyes:** egy ismeretlen fizetési mód vagy bizonylattípus
**csendes elnyelése** rossz összeget vagy rossz gyűjtőt eredményez. A hangos
elutasítás kellemetlen; a néma félreértés kimutathatatlan.

### 4.2/b ⚠️ `[ÚJ SZABÁLY]` Mikor fagy be egy verzió

**A 4.1 táblázata azt írja le, mi engedhető meg egy KIADOTT verzión. Volt egy
hiányzó mondat, ami nélkül a szabály használhatatlanul szigorú lett volna:**

> **Egy szerződésverzió akkor fagy be, amikor az ELSŐ kliens élesben ráfordul.**
> Addig módosítható — de **minden módosítás bekerül a változásnaplóba**, a
> „miért" indoklással.

**Miért kell ez kimondva:** e nélkül minden fejlesztés közbeni finomítás új fő
verziót igényelne, és három hét alatt `v7`-nél tartanánk anélkül, hogy egyetlen
kliens is létezne. **A verziószám akkor ér valamit, ha valakinek fáj, ha nő** —
ha nem fáj senkinek, csak zaj.

**A határ éles, és nem mozgatható:** az első éles telepítés napjától a 4.1
táblázat kivétel nélkül érvényes. **A „még csak egy ügyfél van" nem mentesség** —
az az egy ügyfél is elad, és az ő kliense is elromlik.

### 4.3 Két fő verzió egyszerre — mennyi ideig

| Szerződés | Meddig kell a régit is kiszolgálni |
|-----------|-----------------------------------|
| **K1** | **Legalább egy teljes kiadási ciklus.** A gördülő frissítés alatt a gépek órákig eltérnek, és **egy offline PDA napokig** |
| **K2** | A böngésző mindig friss klienst tölt — **de a nyitva felejtett lap nem.** A verzióeltérést a felület **kimondja**, és újratöltésre kér |
| **K3** | ⚠️ **Legalább két kiadási ciklus.** A felhő és a telephely soha nem frissül egyszerre |

### 4.4 A válasz megmondja, milyen szerződéssel szolgálták ki

**Minden válasz fejlécében:** a szerződés neve és pontos verziója.

**Miért:** egy „néha rosszul viselkedik" hibabejelentésnél az első kérdés az,
hogy **melyik oldal melyik verziót futtatja.** Ha ez nem látszik, ez a kérdés
órákba kerül.

---

## 5. `[DÖNTÉS]` Hogyan jut el a fogyasztókhoz

### 5.1 Kimásolt, rögzített példány — nem almodul

**Minden fogyasztó repó a saját fájában tartja a szerződés másolatát**, a
felhasznált verzióval együtt, és **a folyamatos beépítés ellenőrzi a
lenyomatát.**

| Lehetőség | Miért nem |
|-----------|-----------|
| **Git almodul** | A C# és a Dart eszközlánc mellett ez rendszeres súrlódás; és **az almodul-mutató frissítését pont olyan könnyű elfelejteni**, mint a másolatét — csak nehezebb észrevenni |
| **Csomagtárból** | Három nyelvhez három csomagtár. **Aránytalan** |

**A kimásolt példány szabálya:**

| # | Szabály |
|---|---------|
| a | A fogyasztó **megnevezi a verziót**, amire fordít |
| b | A folyamatos beépítés **összeveti a lenyomatot** a kiadott szerződéssel — **eltérésnél megbukik** |
| c | **A generált klienst nem tartjuk verziókövetésben**, hanem építéskor generáljuk. Ami generált, az ne legyen kézzel javítható |

### 5.2 A generálás iránya

| Repó | Nyelv | Mit generálunk |
|------|-------|----------------|
| `siduri-backend-server` | Java | ⚠️ **Kiszolgáló-oldali illesztő** — a szerződésből, nem fordítva |
| `siduri-cloud-api` | Java | Ugyanaz, a K2 és K3 rá eső részére |
| `siduri-pos-client` | C# | Kliens |
| `siduri-flutter-clients` | Dart | Kliens |
| *webes admin* | TypeScript | Kliens |

> ⚠️ **Szerződés-először, nem kód-először.** A szerződés nem a Java kód
> mellékterméke. Ha fordítva lenne, a K2 két megvalósítása azonnal szétcsúszna
> — mert akkor **az egyik szerver kódja lenne az igazság**, és a másik csak
> követné.

### 5.3 Szerződésteszt — ez teszi valóságossá az egészet

| # | Teszt | Mit bizonyít |
|---|-------|--------------|
| a | **Mindkét K2-megvalósítás ugyanazt a szerződéstesztet futtatja** | A felhő és a telephely tényleg ugyanazt tudja *(§22.2)* |
| b | **Kompatibilitási ellenőrzés a kiadott előző verzióval szemben** | Törő változás nem mehet ki fő verzió emelése nélkül. **Gépi, nem emberi éberség** |
| c | **A generált kliensek lefordulnak** mindhárom nyelven | A szerződés nem csak Javában értelmes |

---

## 6. `[DÖNTÉS]` Amit a szerződésnek szerkezetileg ki kell kényszerítenie

Ez a rész nem stílus. **Ezek az invariánsok a határon is érvényesek, vagy
sehol.**

### 6.1 ⚠️ Pénz a dróton

| Fogalom | Hogyan megy át | Miért |
|---------|----------------|-------|
| **Összeg** | **egész szám** (JSON `number`, tizedes nélkül) | Egész forint, a `2^53` határ alatt bőven. A JSON-szám itt biztonságos |
| **Egységköltség, mennyiség, árfolyam** | ⚠️ **SZÖVEG** — `"2.500000"` | **A JSON-szám lebegőpontosként olvasódna be** a legtöbb elemzőben. Szövegként pontos |
| **Pénznem** | csak fizetésnél, önálló mező | Az árlista mindig forint |

> **Ez az I1 invariáns kiterjesztése a protokollra.** A `double` tiltása a
> kódban semmit nem ér, ha az adat lebegőpontosként lép be a rendszerbe.

### 6.2 Idő és sorrend

| Mező | Kötelező | Miért |
|------|----------|-------|
| `eszkoz_ido` | igen | Az eszköz órája a keletkezéskor |
| `szerver_ido` | a válaszban | A befogadás ideje |
| `sorszam` = `(epoch, szamlalo)` | ⚠️ **igen, MINDEN íráson** | **A sorrendet ez adja, nem a fali óra** |

### 6.3 ⚠️ Az epoch az első naptól benne van

**A magas rendelkezésre állás az F6-ban épül meg — de az `epoch` mező a
protokollban az első naptól kötelező** *(F1.4)*.

| # | Szabály |
|---|---------|
| a | **Minden írási kérés hordozza a kliens által ismert epochot** |
| b | **A szerver a régebbi epochú kérést elutasítja**, nevesített hibával |
| c | **A kliens a régebbi epochú választ elutasítja** *(F6.5)* |

**Miért az első naptól:** egy mező felvétele a protokollba később **minden
kliens minden verzióját érinti.** Most ingyen van; egy év múlva átállási terv.

### 6.4 Idempotencia

| # | Szabály |
|---|---------|
| a | **Minden állapotváltoztató kérés hordoz idempotencia-kulcsot** — ez az outbox rekord azonosítója |
| b | **A megismételt kulcs ugyanazt a választ adja**, nem hibát és nem második hatást |
| c | **A kulcs érvényességi ideje kimondott**, nem örök |

**Miért kötelező, nem választható:** a degradált módból való visszajátszás
**definíció szerint ismétel.** Ha az idempotencia opció lenne, azt pont az a
kliens hagyná ki, amelyik offline üzemel.

### 6.5 A hibaformátum mindhárom szerződésben ugyanaz

| Mező | Tartalom |
|------|----------|
| `kod` | **gépi kód**, stabil, verziózott — erre ágazik el a kliens |
| `uzenet` | **magyar szöveg a kezelőnek**, tényt közöl |
| `azonosito` | **nyomkövetési azonosító** — ez köti össze a képernyőt a naplóval |
| `reszletek` | mezőnkénti hibák, ha van |

> ⚠️ **A `kod` soha nem a `uzenet` szövegéből származik.** Aki szövegre ágazik
> el, annak a következő fordítás töri el a logikáját.

---

## 7. `[ELDÖNTVE — S1]` A leküldő csatorna: WebSocket

> **Részletes indoklás: `ESEMENYCSATORNA.md`.** Itt csak az, ami a szerződést
> érinti.

**A döntés: WebSocket**, és nem azért, mert ez a modern.

| # | Ok |
|---|-----|
| a | ⚠️ **A .NET-ben nincs beépített SSE-kliens.** A POS kliens C#/WPF: WebSocketre van beépített osztály, SSE-re nincs — a folyamot, az újracsatlakozást és a `Last-Event-ID` kezelést kézzel kellene megírni. **Az SSE „egyszerűbb" volta pont a legfontosabb kliensünkön nem érvényesül** |
| b | **A KDS-nek visszafelé is beszélnie kell** — a szakács ott jelzi, hogy egy tétel elkészült. SSE mellett ez külön hívás lenne, és két csatorna állapotát kellene együtt tartani |

**A boríték MOST kerül a szerződésbe** *(`szerzodes/kassza/v1/esemenyek.yaml`)*,
**a megvalósítás az F5-ben** épül meg a KDS-sel együtt. Ugyanaz az ok, amiért az
epoch mező az első naptól benne van: egy protokollmező utólagos felvétele
**minden kliens minden verzióját** érinti.

### 7.1 Amit a szerződés rögzít

| # | Szabály |
|---|---------|
| a | **Az esemény sorszáma ugyanaz a `(epoch, számláló)` pár** — nem új mechanizmus. Így a régebbi generációjú esemény azonnal felismerhető és eldobható, és szerepváltás után nem kell külön „ürítsd a gyorsítótárat" üzenet |
| b | **Újracsatlakozáskor a szerver dönt:** `POTLAS` vagy `UJRATOLTES`. **Az `UJRATOLTES` nem hibajelzés**, hanem normális válasz — véges pufferből nem lehet órákat visszajátszani. ⚠️ **Csendben folytatni tilos**: a kliens azt hinné, naprakész, holott lyuk van a történetében |
| c | **Másodperces szívverés, és a kliens 5 másodperc után elavultnak tekinti a csatornát** — nem várja meg a TCP időtúllépését, ami percekig is eltarthat |
| d | ⚠️ **Az elavult csatorna LÁTSZIK a felületen.** Egy némán elavult KDS rosszabb, mint egy láthatóan leszakadt: az elsőnél a szakács elhiszi, hogy nincs új rendelés |
| e | **A csatorna nem hitelesít külön** — ugyanaz az eszközazonosság és munkamenet. Egy második hitelesítési út egy második hibalehetőség |

**Blokkoló mérés: M23** — a WebSocket-réteg natív képbe fordul-e, és bírja-e a
12 tartós kapcsolatot a telephelyi gépen. **A puszta keretrendszer-támogatás nem
elég bizonyíték**, mert a natív kép hibái futásidőben jelentkeznek.

---

## 8. Nyitott

| # | Kérdés |
|---|--------|
| ~~**S1**~~ | ~~A leküldő csatorna technológiája~~ — **ELDÖNTVE: WebSocket** *(7. fejezet, `ESEMENYCSATORNA.md`)* |
| **S2** | **A kompatibilitási ellenőrzés eszköze** — melyik nyílt eszköz ismeri fel megbízhatóan a törő változást OpenAPI 3.1-en |
| **S3** | **A K3 tömeges átvitelének alakja** — a napi szinkron nem ugyanaz, mint egy rendelés felküldése; lehet, hogy külön formátum kell |
| **S4** | **A szerződésgazda megnevezése** — ez személyi döntés, nem technikai |
| **S5** | ⚠️ **Az eszköz azonosságának mechanizmusa.** A **kölcsönös TLS** a javaslat: egy LAN-on egy másolható jelszó kevés egy olyan géptől, ami **bizonylatot állíthat ki**. Az ára valós — tanúsítvány-kiosztás és -megújítás a telepítéskor és a telepítés élettartama alatt. **Amíg nincs döntés, a megvalósítás nem kezdődhet el** |
| **S6** | **Eszközregisztráció és kezelői bejelentkezés a K1-ben.** Az F1 bizonyító szelete már hitelesített állapotból indul — **ez kimondott hiány, F2-ben pótlandó**, nem elfeledett rész |
