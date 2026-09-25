# Siduri — az eladási adatok felküldése a felhőbe

> **Státusz: TERV, JÓVÁHAGYÁSRA** *(2026-09-25, FOLYAMATBAN 7.0/a: „előbb terv,
> kód csak utána")*. A döntést igénylő pontok a **6. fejezetben**, mindegyik
> mellett a javaslat és az ára.

## 1. Miért — és mi NEM ez

| Cél | Forrás |
|---|---|
| **A felhő a jogi archívum** — a 8 éves megőrzést (Szvt. 169. §) a felhő teljesíti, nem a telephelyi gép | `NYITOTT_KERDESEK.md` A3 |
| **A helyi törlés csak POZITÍV BIZONYÍTÉK után** — nem elég „elküldtük", igazoltan meg kell lennie a felhőben | A3, §5 |
| **Riportok, statisztikák a Zigguratban** — a telephelyek fölött, a lánc szintjén is | B16.1, a hátralévő admin-tétel |
| **Felhős horgonyzás** — a biztonsági audit-lánc feje időnként felmegy, így egy visszamenőleges átírás kiderül | `CLAUDE.md`, „Mi lesz a felhő" |

**Amit ez NEM:**
* **Nem kétirányú.** Az eladás **telephely-autoritatív** (a felhő mennyiségi
  állapotra nem gazda) — a felhő csak **fogad és tárol**, soha nem ír vissza
  eladást. Nincs ütközésfeloldás, mert nincs második író.
* **Nem az NTAK-beküldés.** Az a telephely feladata, külön úton marad.
* **Nem a kliens-archívum.** A pénztárgép saját, csak olvasható archívuma
  (B10/b) bizonyíték a szerver felé; ez a szerver és a felhő közötti út.

## 2. Mi megy fel — önmagában értelmezhető egységként

**Az egység a lezárt bizonylat, a teljes környezetével.** Egy archivált
bizonylat, amihez a mai terméktörzs kell, nem archívum (A3/1).

| Rész | Telephelyi tábla | Megjegyzés |
|---|---|---|
| A bizonylat | `bizonylat` | Siduri- és adóügyi szám, üzleti nap, végösszeg, eszköz, epoch+számláló |
| A rendelés | `rendeles` | teljesítési mód, munkanap |
| A tételsorok | `tetelsor` | **az eladáskori** név, egységár, áfa, mennyiség (C2/a) — ezért önálló |
| Az áfa-bontás | `bizonylat_afa_csoport` | bruttó = nettó + áfa |
| A fizetések | `fizetes` | valutánál az árfolyammal |
| Egyéb tételek | `bizonylat_egyeb_tetel` | kedvezmény, szervizdíj, borravaló |
| Sztornó, tételtörlés | `tetelsor_torles`, sztornó-bizonylat | **új rekordként**, az eredeti érintetlen |
| Számlaadatok | a számla vevőadatai | ⚠️ személyes adat — lásd **D5** |
| Megosztás | `megosztas`, `megosztas_tetel` | a számlamegosztás nyoma |

**Külön, a nap szintjén:** a munkanap és a műszakok (nyitás/zárás, vakzárás
eredménye), a készpénzmozgások — ezek a napi egyeztetés részei (4.).

## 3. Hogyan — a csatorna

Ugyanaz a minta, amit a törzsadat-felküldés (`TORZSADAT_FELKULDES.md`) már
bizonyított, **külön végponttal**, mert a mennyiség más nagyságrend:

| # | Tulajdonság | Miért |
|---|---|---|
| a | **Helyi kimenő sor**, a lezárással **ugyanabban a tranzakcióban** | nincs olyan állapot, ahol a bizonylat megvan, de a felküldése elveszett |
| b | **Új végpont: `POST /szinkron/v1/eladasok`**, kötegben (pl. 200 bizonylat) | a hozzáférés-lekérdezés percenkénti köre ne hízzon meg |
| c | **Azonosító szerint idempotens**; tételenkénti kimenet (`ELFOGADVA`, `HIBAS_TETEL`) | újraküldés = ugyanaz a válasz; egy hibás tétel nem akasztja a sort |
| d | **Tartalomlenyomat** minden bizonylaton (a sorrendezett, kanonikus alakból) | a felhő ellenőrzi, és a napi egyeztetés ezt hasonlítja |
| e | **A felhőben CSAK BESZÚRHATÓ** táblák (trigger, mint a telephelyen) | az archívum szerkezetileg nem írható át (A3, „őrt igényel, nem kommentet") |
| f | **Kölcsönös TLS**, telephely-egyezés, mint a többi szinkronnál | — |

## 4. A pozitív bizonyíték — a napi egyeztetés

A „küldtük, nem jött hiba" **nem bizonyíték**. A nap lezárása után (napzárás)
a telephely egy **napi összesítőt** is felküld:

> *darabszám · végösszeg áfacsoportonként · fizetési módonként · a bizonylatok
> lenyomatainak rendezett lenyomata*

A felhő a **saját**, beérkezett bizonylataiból ugyanezt kiszámolja. Ha egyezik,
a napot **IGAZOLTnak** jelöli, és ezt visszaküldi. **A telephely helyi törlése
(30 nap / 20 forgalmas nap) csak IGAZOLT napra futhat** — egy nem egyező nap
örökre helyben marad, és a Zigguratban piros.

Ugyanitt megy fel **a biztonsági audit-lánc feje** (a nap utolsó elemének
lenyomata): a felhő eltárolja, így egy visszamenőleges átírás a telephelyen
kiderül (horgonyzás).

## 5. A felhőben

* **Bérlőnkénti séma** (mint minden más), havi partícionálással a
  bizonylat-táblákon — a 8 év nem lassíthatja a friss riportot.
* **Olvasás: a Zigguratban** riportok (napi forgalom, áfa- és fizetésmód-bontás,
  termék-toplista, lánc-összesítő) — **ez a következő szelet**, nem ez.
* **A külön mentés** a 8 éves archívumra (B17/e) — magyar adatközpont; a
  visszatöltés **kipróbálva**, nem csak megtervezve (A3/3).

**Nagyságrend:** egy forgalmas hely ~1 000 bizonylat/nap × ~2 KB ≈ 2 MB/nap
→ 8 év alatt ~6 GB telephelyenként, tömörítés nélkül. Nem akadály.

## 6. DÖNTÉST IGÉNYEL

| # | Kérdés | Javaslat | Ára |
|---|---|---|---|
| **D1** | **Mikor megy fel?** Folyamatosan (lezáráskor) vagy csak napzáráskor, egyben | **Folyamatosan**, + napzáráskor az egyeztetés | több, kisebb kérés; cserébe a Zigguratban **napközben is** látszik a forgalom, és egy gépkiesés legfeljebb perceket veszít el, nem egy napot |
| **D2** | **Mi az egyeztetés egysége?** | **A munkanap** (napzárás után) | egy nyitva felejtett nap nem igazolódik — de azt a napzárás-ütemező úgyis kényszerzárja |
| **D3** | **Kezdeti feltöltés** a már meglévő, helyben még meglévő napokra | **Igen**, a legrégebbitől, lassítva (éjjel) | egy J1900-on órákig tarthat; közben a pult nem lassulhat — ezért ütemezve |
| **D4** | **A helyi törlés** feltétele | **Csak IGAZOLT nap** törölhető; a nem igazolt örökre marad | egy tartósan hibás nap helyet foglal a telephelyi gépen — de ez a helyes irány (A3) |
| **D5** | **A számla vevőadatai** (név, cím, adószám) felmenjenek-e | **Igen** — a jogi archívum része, nélküle a számla nem értelmezhető | GDPR: a felhő adatkezelő lesz ezekre is → adatkezelési tájékoztató, törlési kérelemnél a 8 éves megőrzés az erősebb |
| **D6** | **Az audit-horgony** most, ugyanezzel? | **Igen**, a napi egyeztetéssel együtt | kis többletmunka; enélkül a lánc visszamenőleges átírása csak helyben derülne ki |
| **D7** | **Riportok** ugyanebben a szeletben? | **Nem** — előbb az adat biztonságosan fent legyen, a riport a következő szelet | a Ziggurat riportképernyője egy körrel később jön |

## 7. A sorrend, ha jóváhagyva

1. `szinkron/1.10.0`: `POST /eladasok`, `POST /napi-egyeztetes` — szerződés + napló.
2. Felhő: csak beszúrható táblák (V-migráció), elbírálás, egyeztetés, horgony.
3. Telephely: kimenő sor a lezárásnál (trigger + tranzakció), küldő, egyeztető,
   a helyi törlés feltételének átállítása IGAZOLT napra.
4. Kezdeti feltöltés, ütemezve.
5. Tesztek + mutációs próbák: *elveszett bizonylat → a nap nem igazolódik*,
   *átírt bizonylat → a lenyomat eltér*, *újraküldés → nincs kettőzés*,
   *nem igazolt nap → nem törlődik*.
6. Ziggurat: a telephely-lapon a napok egyeztetési állapota (igazolt / eltérő /
   függőben) — a riportok a következő szeletben.
