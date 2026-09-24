# Bejelentkezés a Zigguratba

> **Állapot: TERV, döntésre vár** *(2026-09-24)*. Kód még nem készült.
>
> **Miért most:** a Ziggurat ma fejlesztői kapcsolóval működik (a „token” maga
> a felhasználó azonosítója), élesben **minden kérés 401**. Bejelentkezés nélkül
> a felület nem élesíthető. A keret már eldőlt (`HOZZAFERES.md` §9); ez a
> dokumentum a **hiányzó döntéseket** és a megvalósítás darabjait írja le.

---

## 1. Ami már eldőlt, és amire építünk

| Mi | Döntés / meglévő | Hol |
|---|---|---|
| Azonosítás a Zigguratban | **felhasználónév + jelszó** | `HOZZAFERES.md` §9 |
| A felhasználónév | `<bérlő>.<név>`, pl. `kiskocsma.Pista` — az előtag a **bérlő** rövid neve | §9, `kozos.berlo.rovid_nev` |
| Új felhasználó | **e-mailes meghívó**, SMTP, a MythSystems feladócímével | §9 |
| Jelszószabály | **minimumhossz: igen**, kötelező lejárat: **nem** | §9 |
| Második tényező | a belső kollégafiókokhoz **egyelőre nincs** — vállalt kockázat | §4.5 |
| Pultos belépés | azonosító + PIN, **PBKDF2 + bors**, **növekvő várakozás**, belépési napló | telephelyi szerver, `mag.BelepesiKorlat` |
| A felhő natív képe | **nem kényszer** — ott az Argon2id is használható, új függőség nélkül (a BouncyCastle már bent van) | O1 |

---

## 2. A javaslat röviden

* **A felhőben:** jelszó **Argon2id** lenyomattal, a bejelentkezés után
  **szerveroldali munkamenet** egy `HttpOnly` sütiben. Kijelentkezéskor,
  letiltáskor és jelszócserekor a munkamenet **azonnal megszűnik**.
* **A telephelyről kiszolgált Zigguratban:** a **pultos azonosító + PIN** léptet
  be, a meglévő, fékezett úton — mert a telephely a Ziggurat-jelszavakat nem
  ismeri, és ne is ismerje *(lásd 5.1)*.
* **Meghívó és elfelejtett jelszó:** egyszer használható, lejáró jegy,
  e-mailben. A jegyből **csak a lenyomata** kerül az adatbázisba.
* **A felület:** saját bejelentkező képernyő, és a 401 végre nem nyers hibakód.

---

## 3. A részletek

### 3.1 A jelszó

* **Argon2id**, OWASP-paraméterekkel (19 MiB memória, 2 iteráció, 1 szál) — a
  paraméterek a lenyomat mellett tárolódnak, így később emelhetők anélkül, hogy
  mindenkinek új jelszó kellene.
* **Minimumhossz** *(5.3)*, felső határ 128 karakter *(a hash-számítás így nem
  lehet túlterheléses támadás eszköze)*.
* **Tiltólista:** a leggyakoribb jelszavak és a felhasználó saját neve /
  felhasználóneve. Helyi lista, **külső hívás nélkül**.
* Kötelező lejárat **nincs** *(eldöntve)*. Csere csak kérésre vagy gyanú esetén.

### 3.2 A próbálgatás fékezése

* **Fiókonként növekvő várakozás** — ugyanaz a `BelepesiKorlat`, mint a pultnál.
  **Kizárás nincs**, mert a kizárás maga is támadás: bárki kizárhatna bárkit,
  aki a felhasználónevét ismeri.
* **A válasz nem árulja el, létezik-e a felhasználó:** rossz név és rossz jelszó
  ugyanazt a választ kapja, ugyanannyi idő alatt *(nem létező névnél is lefut
  egy ál-lenyomatolás)*.
* Minden kísérlet a belépési naplóba kerül: ki, mikor, honnan (IP), sikerült-e.

### 3.3 A munkamenet

* **Szerveroldali, átlátszatlan azonosító** *(nem JWT)*: 32 bájt véletlen, a
  sütiben az érték, az adatbázisban **csak a lenyomata**. Egy ellopott
  adatbázis-mentésből így nem lesz használható munkamenet.
* **Süti:** `HttpOnly` *(a böngészőben futó kód nem látja — egy XSS nem viszi
  el)*, `Secure`, `SameSite=Strict`.
* **Visszavonás azonnal:** kijelentkezés, **letiltás**, jelszócsere → a
  felhasználó minden munkamenete megszűnik. Ez a fő ok, amiért nem JWT: egy
  aláírt tokent a lejáratáig nem lehet visszavonni, és egy letiltott dolgozó
  addig bent maradna.
* **Hol él:** a felhőben a **közös sémában** (`kozos`), mert a sütiből kell
  kiderülnie, **melyik bérlőé** — a bérlő sémáját csak ezután tudjuk kiválasztani.
* Időkorlát *(5.2)*: tétlenségi és abszolút is.

### 3.4 A telephelyről kiszolgált Ziggurat

A Ziggurat két helyről szolgálható ki, és a telephelyi azért van, hogy
**internetkimaradáskor is működjön**. A telephelyen a pultos nyilvántartás
másolata él, PIN-nel — a Ziggurat-fiókok jelszava **nincs** ott.

**Javaslat:** a telephelyi Zigguratba **pultos azonosító + PIN** léptet be, a
meglévő úton *(fékezés, napló)*. A munkamenet ugyanúgy süti, a telephelyi
adatbázisban. A felület a `Siduri-Kiszolgalo` fejlécből tudja, melyik
bejelentkező mezőt mutassa.

Aki mindkét fiókkal rendelkezik *(a 4. darab óta összekapcsolhatók)*, az
kapcsolat nélkül a pultos fiókjával lép be. **Akinek csak Ziggurat-fiókja van**
*(irodista, könyvelő)*, az kapcsolat nélkül **nem** lép be — ezt a képernyő
kimondja, nem hallgatja el.

### 3.5 Meghívó és elfelejtett jelszó

* **Egyszer használható jegy**, 32 bájt véletlen; az adatbázisban a lenyomata.
  Meghívó: **72 óra**, jelszó-visszaállítás: **1 óra**.
* A „elfelejtettem” válasza **mindig ugyanaz** *(„ha létezik ilyen fiók, levelet
  küldtünk”)* — különben a felhasználónevek listázhatók lennének.
* **Levélküldés:** SMTP-n, beállításból. **Ha nincs beállítva, a meghívás nem
  sikerül, és ezt kimondja** — nem tesz úgy, mintha elment volna.
  Fejlesztésben a link a naplóba kerül.
* ⚠️ **A meghívó linkje NEM jelenik meg a meghívónak.** Ha megjelenne, a
  meghívó maga állíthatná be a másik jelszavát, és utána az ő nevében
  dolgozhatna — a napló pedig a meghívottat mutatná.

### 3.6 A felület

* **Bejelentkező képernyő**, felhőben név + jelszó, telephelyen azonosító + PIN.
* **A 401 saját képernyőt kap**: átirányít a bejelentkezésre, és utána vissza
  oda, ahol a felhasználó volt.
* **Kijelentkezés** gomb a fejlécben, a bejelentkezett felhasználó nevével.
* A `localStorage`-os fejlesztői token **megszűnik** a felületen; a fejlesztői
  kapcsoló a háttérben tesztelésre megmarad.

---

## 4. Amit ez a terv NEM old meg, kimondva

* **Második tényező** — vállalt kockázat, a belső fiókoknál a legnagyobb.
* **A Siduri kollégafiókok** belépése (`HOZZAFERES.md` §4) — a 7. darab.
* **A telephelyválasztó:** ma a telephely a konfigurációból jön. Több üzletes
  bérlőnél a felhős Zigguratban választani kell majd — külön darab.
* **A levél kézbesíthetősége** (SPF, DKIM, DMARC) — üzemeltetési feladat, nem kód.
* **Egy négyjegyű PIN a böngészőben gyenge** — tízezer lehetőség. A telephelyi
  Ziggurat csak a helyi hálózaton érhető el, és a fékezés ugyanaz, mint a
  pultnál; de ezt vállalni kell, ha az 5.1-ben az „a” út nyer.

---

## 5. Döntést igénylő kérdések

### 5.1 Hogyan lépnek be a telephelyről kiszolgált Zigguratba?

| | a) Pultos azonosító + PIN | b) A Ziggurat-jelszavak a telephelyre is lemennek | c) Csak kapcsolattal |
|---|---|---|---|
| Kapcsolat nélkül | működik — pultos fiókkal | működik — mindenkinek | **nem működik** |
| **ÁRA** | aki csak Ziggurat-fiókkal bír, offline nem lép be; a PIN gyengébb egy jelszónál | **a bérlő összes jelszó-lenyomata ott van egy kocsmai gépen**: ha elviszik, offline próbálgatható; szinkron-bővítés | a telephelyi Ziggurat értelmét veszti — pont kimaradáskor esik ki |
| Munka | kicsi — a PIN-es út megvan | közepes | kicsi |

**Javaslat: a)**.

### 5.2 Meddig él egy munkamenet?

**Javaslat:** **60 perc tétlenség** után lejár, és **legfeljebb 12 óra** — utána
újra be kell lépni. **ÁRA:** aki egész nap nyitva tartja, naponta egyszer-kétszer
újra belép. Rövidebb tétlenségi idő (15 perc) biztonságosabb egy közös gépen, de
a munka közben is kiléptetne.

### 5.3 Mekkora a minimális jelszóhossz?

| | 8 | **12** | 15 |
|---|---|---|---|
| Mit mond róla a szabvány | a régi NIST-minimum | közbülső | a NIST 800-63B **újabb** változata ennyit ír elő, ha a jelszó az egyetlen tényező |
| **ÁRA** | gyenge — és nálunk nincs második tényező | kompromisszum | a felhasználók egy része bosszankodni fog, és felírja |

**Javaslat: 12**, a tiltólistával együtt. Mivel második tényező nincs, a 8 kevés.

---

## 6. A darabok, sorrendben

| # | Darab | Érinti |
|---|---|---|
| 1 | **Szerződés** *(`admin/1.7.0`)*: bejelentkezés, kijelentkezés, „ki vagyok”, meghívó elfogadása, elfelejtett jelszó; a biztonsági séma süti | docs |
| 2 | **Felhő:** jelszó-lenyomat, munkamenet-tábla, fékezés, napló, meghívó- és visszaállító jegy, levélküldő (SMTP, fejlesztésben napló) | backend `felho` |
| 3 | **Telephely:** PIN-es bejelentkezés a Zigguratba, munkamenet | backend `szerver` |
| 4 | **A Ziggurat:** bejelentkező képernyő, 401-képernyő, kijelentkezés, meghívó- és visszaállító oldal | ez a felület |
| 5 | **Élő próba** mindkét kiszolgálóval, böngészőben | — |
