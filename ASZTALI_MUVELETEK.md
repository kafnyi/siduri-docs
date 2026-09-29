# Siduri — asztali műveletek (F2 #3 + a konyhai törlés)

> **Státusz: a szerver kész (A1–A3), a pult (A4) következik** *(2026-09-29)*. A nyolc művelet, amelyik a
> jogosultsági katalógusban megvan, de végpontja nincs (`JogosultsagSoprasTest`
> kivétellistája), és a konyhára már kiküldött tétel törlése (`KONYHA.md` 4.).

## 1. A felhasználó döntései *(2026-09-29)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **A következő tömb** | **asztali műveletek** | 3–4 szelet; az élő próba a felhasználóé |
| **A kiküldött tétel törlése** | **sztornó jegy + KDS** — „TÖRÖLVE" jegy az állomásra, a KDS-en a tétel áthúzva | egy új eseménytípus és jegyfajta |
| **Áthelyezés, összevonás** | **egész rendelés ÉS tételenként** | a tételenkénti átrakás a nyitott megosztással ütközne — ilyenkor tiltjuk |
| **Nem fizetett lezárás** | **most, indokkal** | a könyvelési kérdés (reprezentáció áfája, F0.4) és az NTAK-jelentés módja nyitva marad |

## 2. Amit a felderítés talált *(a kódban, javítandó)*

| # | Lelet | Mi lesz |
|---|---|---|
| L1 | **A tételtörlés semmit nem néz a rendelésen**: se nyitott megosztást, se verziót, se más pincér asztalát, se a 24 órát. A megosztás triggerei a tételsor változására NEM futnak — **egy megosztás közbeni törlés némán inkonzisztens megosztást hagy** | D1: közös írási kapu |
| L2 | A törölt tétel a KDS-jegyen megmarad (a jegy sorai nem szűrnek állapotra) | D4 |
| L3 | A nyitott árú felütésnek nincs jogellenőrzése — az egyetlen „árfelülírás-szerű" út | marad: a nyitott ár a termék tulajdonsága, nem felülírás; a kézi ár (D8) külön jog |

## 3. Alapértelmezett döntések *(felülbírálhatók — az áruk mellettük)*

| # | Döntés | Ára |
|---|---|---|
| D1 | **Minden rendelést módosító művelet ugyanazon a kapun megy át**: NYITOTT, **nincs nyitott megosztás** (`MEGOSZTAS_FOLYAMATBAN`, 409 — előbb vissza kell vonni), más pincér asztalához a jog, 24 óra, verzió. A törlésnél a verzió **nem kötelező** (egy adott tételsorra szól, nem ír felül csendben), de ha jön, ellenőrzött; minden írás lépteti | megosztás közben semmi nem módosítható |
| D2 | **Mennyiségmódosítás csak egyszerű tételen** (nem menü, nincs módosító- vagy kedvezménysora); a módosítós és a menü: törlés + újrafelütés | a „még egy ilyen burgert, ugyanígy" újrafelütés |
| D3 | **Növelés** a konyha előtt ugyanazon a soron, a felütéskori áron; **a konyha után növelni nem lehet** (új felütés kell: a konyhának új jegy kell). **Csökkentés** a konyha után = részleges törlés: `tetel.torles_kuldes_utan` + sztornóindok + TÖRÖLVE jegy a különbségről. Mindig kell a `tetel.mennyiseg_modositas` | — |
| D4 | **TÖRÖLVE jegy** az eredeti állomásra (nagy fejléc, asztal, tétel, mennyiség); a KDS-en az eredeti jegyen a tétel **áthúzva**, új **`JEGY_VALTOZOTT`** eseménnyel. A nyomtatási hiba ugyanúgy HIBA + újranyomtatás | új eseménytípus a szerződésben |
| D5 | **Áthelyezés**: egész rendelés **szabad** asztalra (foglaltra: összevonás, külön jog); a nyitott KDS-jegyek az új asztalszámot mutatják (`JEGY_VALTOZOTT`) | — |
| D6 | **Összevonás**: a forrás **minden** tétele (a törölteké és a törlési bejegyzéseké is, menüpéldánnyal, konyhai jeggyel) a célba kerül; a forrás **`OSSZEVONVA`** állapotú üres héj lesz (hova ment), a vendégszám összeadódik, a cél előnyugtája érvényét veszti, az aktuális fogás a nagyobb. Mindkét verzió kell. ⚠️ **A törléseknek is menniük kell**: a forrásnak soha nem lesz bizonylata, és a felhőbe a törlés a bizonylattal megy fel — ha maradna, az összevonás a törlések eltüntetésének útja lenne | — |
| D7 | **Tételenkénti átrakás** másik asztalra (ha szabad, ott új rendelés nyílik az átrakó nevén); a tétel a gyerekeivel, a menü egészben; egyszerű tételnél **részmennyiség** is (a sor kettéválik, ugyanazon az áron). Jog: `rendeles.athelyezes` (külön kód nincs) | a már kiküldött tétel jegye a régi asztalon marad — a konyha már főzi, a pincér viszi át |
| D8 | **Kézi ár** egyszerű tételen és nyitott árún (nem menükomponens, nem gyereksor); `ar.kezi_felulriras` + `ARFELULIRAS` indok, egyszeri felhatalmazással is; a sor **`arfelulirva`** jelölést kap, az eredeti ár a biztonsági auditban | a menü ára nem írható át (a szétosztás a listaárakra épül) |
| D9 | **Tételkedvezmény** = a tétel alatti **KEDVEZMENY sor** (mint a levonó módosítóé), százalék vagy fix, soronként egy (az új felülírja, a 0 leveszi); `kedvezmeny.tetel`, a küszöb fölött `kedvezmeny.kuszob_felett` + `KEDVEZMENY` indok. A végösszeg-kedvezmény a tételkedvezmények utáni összegre számol | menün nincs tételkedvezmény |
| D10 | **Nem fizetett lezárás**: a rendelés **`NEM_FIZETETT`** állapotú, **bizonylat nincs** (nem adóügyi esemény), a **készlet levonódik** (új mozgásfajta `NEM_FIZETETT`, ugyanazzal a robbantással, mint az eladás); `NEM_FIZETETT_LEZARAS` indok kötelező, magas kockázatú (egyszeri felhatalmazással is), biztonsági audit | **NTAK: nyitott** — az F3 előtt el kell dönteni, hogyan jelentendő (`NYITOTT_KERDESEK`, új pont) |
| D11 | **Műszakátadás**: az átadó megszámol (a vakzárás szabályai szerint), a műszak **ÁTADVA** jelöléssel zárul; a gép következő nyitása ezt az összeget **várja**, az átvevő maga számol, az **eltérés az ő nyitásán** látszik. Jog: `muszak.atadas` (a zárás joga helyett) | két számolás — ez a lényege |
| D12 | **Fióknyitás eladás nélkül**: a szerver engedélyez és auditál (`FIOKNYITAS` indok, magas kockázatú), **a pult nyitja** az adóügyi eszköz fiókját | ha az eszköz nem tud fiókot nyitni, a pult jelez |

## 4. Szeletek

| # | Szelet | Állapot |
|---|---|---|
| A1 | **Szerver**: közös írási kapu (L1), mennyiségmódosítás, konyhai törlés (TÖRÖLVE jegy, `JEGY_VALTOZOTT`) | **kész** — `kassza/1.31.0`, V48; a konyha utáni csökkentés a törlési mutatóban és a felhőben is; 10 mutációs próba |
| A2 | **Szerver**: áthelyezés, összevonás, tételenkénti átrakás | **kész** — `kassza/1.32.0`, V49 (`OSSZEVONVA`); a kettévágott, már kiküldött sor a konyhai jegyen is kettéválik (a konyha ugyanannyit készít); 3 végponti teszt, 7 mutációs próba |
| A3 | **Szerver**: kézi ár, tételkedvezmény, nem fizetett lezárás, műszakátadás, fióknyitás | **kész** — `kassza/1.33.0`, V50–V51 (a készletrobbantás közös függvényben); a sweep-teszt „végpont nélküli" listája kiürült; 11 mutációs próba |
| A4 | **Pult**: mindez a kosárban és az asztalnál | — |
| A5 | **KDS**: a `JEGY_VALTOZOTT`, az áthúzott tétel | — |

## 5. Kimondott hiányok *(a szerver után)*

| Hiány | Ára, ha marad |
|---|---|
| **A nem fizetett lezárás a felhős riportban nem látszik** — nincs bizonylat, ami felmenne; ma csak a biztonsági audit és a készletmozgás (`NEM_FIZETETT`) őrzi | a „gyanús minta" nézet (N2.c) ezt még nem tudja összevetni; egy felküldési szelet kell hozzá |
| **NTAK: a nem fizetett rendelés jelentése** | az F3 előtt el kell dönteni (a térítésmentes átadás jelentendő-e, és hogyan) |
| **Az átrakott, már kiküldött tétel jegye a régi asztalon marad** (D7) | a pincér tudja, a konyha a régi asztalszámot látja |
| **A kézi ár és a tételkedvezmény riportja** (hány tétel, ki, mennyi) | a jelzők felmennek (`arfelulirva`, KEDVEZMENY sor) — a riport még nincs megírva |

