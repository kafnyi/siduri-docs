# Siduri — NTAK adatszolgáltatás (F3)

> **Státusz: az N1–N4 KÉSZ** *(2026-09-29)* — hátra a valódi TLS és az MTÜ validációs tesztje (§0). Forrás: **RMS Interfész
> leírás v1.06** (MTÜ) — <https://info.ntak.hu/media/uploads/docs/RMS_Interfesz_leiras_v106.pdf>,
> 2026-09-29-én letöltve és végigolvasva (C11/a teljesítve). A korábbi döntések:
> `siduri_spec_hu.md` §11, `NYITOTT_KERDESEK` H1–H6, J1–J9, K1–K3, C11,
> `FAZISTERV` F3.

## 0. ⚠️ Amit a felhasználónak kell elindítania — MOST

A tanúsítás (MTÜ Igazolás) **külső átfutás**, és **ez a leghosszabb út az élesig**.
A kód nélküle is megírható és hamis NTAK-szerveren tesztelhető, de **valódi
teszthez és élesítéshez** az MTÜ-nek kell:

| # | Lépés | Ki |
|---|---|---|
| 1 | **Csatlakozási adatlap** (RMS gyártó: MythSystem; fejlesztői/teszt IP-tartomány) → `dev.support@ntak.hu` | **a felhasználó** |
| 2 | Az MTÜ felveszi a teszt-RMS-t, tesztszolgáltatót és teszt üzletet ad | MTÜ |
| 3 | CSR a teszt üzletre (a Ziggurat generálja — N3) → e-mailben | a felhasználó |
| 4 | Információs csomag: tesztrendszer címe, VPN vagy IP-szűrés, **Swagger**, Postman referenciakliens, validációs tesztesetek | MTÜ |
| 5 | Validációs teszt az MTÜ tesztesetein, jegyzőkönyv | mi + a felhasználó |
| 6 | **Igazolás** és éles RMS-azonosító | MTÜ |

## 1. A felhasználó döntései *(2026-09-29)*

| Kérdés | Döntés | Ára |
|---|---|---|
| **A következő tömb** | **NTAK (F3)** | nagy tömb; a valódi teszt az MTÜ hozzáférésére vár |
| **Mi egy rendelésösszesítő** (M10.e) | **bizonylatonként**: 1 bizonylat = 1 összesítő; a sztornóbizonylat = SZTORNO összesítő az eredetire; megosztásnál minden rész külön, a tételek a rész arányában (törtszámú tételszámmal) | egy asztal több összesítőként jelenik meg; az MTÜ-nél megerősítendő |
| **Nem fizetett lezárás** | **indok szerint**: a vendégnek adott (távozott, ház vendége, panasz) **jelentve** — a tételek + ÁFA-kulcsonként 100%-os `EGYEB/KEDVEZMENY` sor, 0 Ft; a **SZEMELYZETI nem** (J7) | könyvelői/MTÜ megerősítés hátra (F0.4) |
| **K1.2 — a felhős tartalék** | **a felhő jelenti a zárt napot, 3 nap várakozással**: csak ha a telephely a tárgynap kezdete óta nem jelentkezett, és a tárgynap után 3 nap eltelt; a jelentett napot a szinkron leviszi | ha a hely 3 napnál tovább internet nélkül, nyitva működik, azok a napok elvesznek (a ZÁRVA visszafordíthatatlan); a zárt nap jelentése 3 napot késik |
| **A privát kulcs helye** | **a felhőben is**: a felhő generálja (kulcs + CSR), titkosítva tárolja, és szinkronnal leküldi a telephelyre; a felhő így tartalékként is küldhet (K1.2) | a kulcs két helyen él — egy felhős incidens aláírási képességet ad ki |

## 2. Amit a leírás maga eldönt *(korábbi nyitott kérdések)*

| Kérdés | A leírás szerint |
|---|---|
| **J6** — mehet-e rendelésösszesítő a napi zárás után? | Igen, **de a következő tárgynapra**: „a rendelés tárgynapja minden esetben a rendelés lezárásakor aktuálisan nyitott nap tárgynapja" — tehát nincs ütközés |
| A 7 napos visszamenőleges korlát | az `uzenetKuldesIdeje` legfeljebb 7 napos lehet — egy hétnél hosszabb kiesés után az **újraküldendő** üzenet nem küldhető változatlanul (ritka; riasztás) |
| Kerekítés | `KEREKITES` fizetési mód, értéke **fizetendő − fizetett** (a példa szerint: KP 1165, KEREKITES −2, végösszeg 1163) |
| Borravaló | `EGYEB/BORRAVALO` tétel (`E_0`) a rendelésben **és** `osszesBorravalo` a napi zárásban |
| Aláírás | **JWS RS256, leválasztott (üres) payload**: `x-jws-signature: <fejléc>..<aláírás>`, a törzs a HTTP body; `x-certificate`: a PEM tanúsítvány BASE64-ben; **kölcsönös TLS ugyanazzal a tanúsítvánnyal** |
| Rendelésazonosító | **UUID v4** — a mi azonosítóink v7-esek, ezért saját v4-et adunk és megőrzünk |

## 3. Alapértelmezett döntések *(felülbírálhatók — az áruk mellettük)*

| # | Döntés | Ára |
|---|---|---|
| D1 | **A telephelyi szerver küld** (ELADAS_FELKULDES), a felhő csak tartalék (N4) | kikapcsolt szerver alatt a felhő lép be — addig az N4-ig senki |
| D2 | **Tartós kimenő sor**: összesítőnként egy sor (saját v4-azonosítóval, a bizonylathoz kötve), üzenetenként egy sor (a **pontos elküldött törzzsel**, hogy az `UJRA_KULDENDO` bájtra azonosan mehessen) | két tábla, nem egy (az ADATMODELL_API §5.4 egytáblás terve helyett) |
| D3 | **Ütem**: 15 percenként (paraméter), legfeljebb **500 tétel** üzenetenként, sorszám szerinti sorrendben; a napi zárás a nap összesítői UTÁN | — |
| D4 | **Ellenőrzés**: a beküldés után ≥2 perccel, aztán az ütemmel, amíg BEFOGADVA; a hibás összesítő **HIBAS** a hibakulccsal, a Zigguratban látszik és (a törzsadat javítása után) **újraépíthető és újraküldhető**; `UJRA_KULDENDO` → ugyanaz a törzs | — |
| D5 | **Napi zárás**: a munkanap zárásakor (NORMAL_NAP vagy FORGALOM_NELKULI_NAP); a nyitvatartási minta nélkül a **zárva tartott nap** csak **utólag**: az a naptári nap, amelyen munkanap nem nyílt és ami már elmúlt, `ADOTT_NAPON_ZARVA` — napi feladat 01:00-kor és indításkor (K1) | nyitvatartási minta nélkül nem kérdezünk rá („elfelejtettetek nyitni?") — a K1.c későbbre marad |
| D6 | **Degradált (`osszesitett`)**: nem használjuk — a mi rendszerünk kiesés alatt is tételesen rögzít, a késve küldött összesítő NORMAL marad; a mező mindig `false` | ha kézi (papír) rögzítés kell valaha, akkor kerül elő |
| D7 | **Leképezés**: tétel = a tételsor (`TETEL`, `MENU_KOMPONENS`, `MODOSITO` a szülő kiszerelésének kategóriájával); `KEDVEZMENY` sor és a bizonylat kedvezménye → `EGYEB/KEDVEZMENY`; szervizdíj → `EGYEB/SZERVIZDIJ` (ÁFA-kulcsonként, ahogy a bizonylaton áll); `mennyiseg` = a kiszerelés mennyisége, `tetelszam` = a tételsor mennyisége; `helybenFogyasztott` = nem ELVITEL/KISZALLITAS | — |
| D8 | **Konfiguráció**: RMS-azonosító, alap-URL (teszt/éles), ütem — alkalmazás-beállítás; adószám és üzlet-regisztrációs szám — telephelyenként (Ziggurat); a kulcs a konfigurációs titokkal titkosítva mindkét oldalon | — |
| D9 | **Az NTAK-küldés nem kapcsolható ki** (L1.2) — de a telephely `ntak_koteles` jelzője alapján nem köteles helyen nem keletkezik sor | — |

## 4. Szeletek

| # | Szelet | Állapot |
|---|---|---|
| N1 | **Üzenetépítő** a közös `k2` modulban (bizonylat → összesítő, sztornó, megosztás-rész, nem fizetett, napi zárás) + **JWS aláíró** + tesztek | **kész** — `k2/Ntak`, `NtakKulcs` (AES-GCM kulcstárolás, közös); 10 teszt, 6 mutációs próba |
| N2 | **Telephelyi küldés**: táblák, sorba állítás (lezárás, sztornó, nem fizetett, napzárás, zárt napok), küldő és ellenőrző ütem, kölcsönös TLS, hamis NTAK-szerver a tesztekhez | **kész** — V52 (`ntak_osszesito`, `ntak_napzaras`, `ntak_uzenet`); a KÉSZÜLETLEN (pl. kategória nélküli) összesítő minden körben újraépül, és a nap napzárása megvárja; UJRA_KULDENDO bájtra azonos; a ZÁRVA csak az elmúlt napra, 6:00 után, nyitott nap nélkül; 9 teszt aláírás-ellenőrző hamis NTAK-kal, 9 mutációs próba. ⚠️ A valódi TLS-kapcsolatot csak az MTÜ tesztrendszere tudja igazolni |
| N3 | **Felhő + Ziggurat**: NTAK-adatok, kulcs + CSR generálása, tanúsítvány feltöltése és lejárata, szinkron le; a telephelyi Zigguratban a küldés állapota, hibák, újraküldés | **kész** — felhő: bérlői V23 (`ntak_beallitas`, KÉT kulcshely: az érvényes és a függő CSR-é — a megújítás nem állítja le a küldést), RSA 4096 + CSR (`CN=<a regszám számjegyei>`), a tanúsítvány csak a függő kulcsra, erre az üzletre, élőként; más regszám = a tanúsítvány és a kulcs eldobva; `admin/1.31.0`, `szinkron/1.21.0` (a kulcs nyersen, a kölcsönös TLS-en; a telephely a SAJÁT titkával tárolja, és csak tanúsítványváltáskor írja át). Telephely: `/ntak` olvasásra, `/ntak/sor`, a HIBAS újraépítése (a többi 409); jog `beallitas.telephely`. Ziggurat: NTAK-lap (60 nappal a lejárat előtt szól). 5 felhős + 2 új telephelyi teszt, 13 mutációs próba (N3) + 11 (N4), összesen 39. ⚠️ Élesítéshez: `SIDURI_NTAK_TITOK` a felhőn ÉS `siduri.ntak.titok` a telephelyen — üresen a felhő nem készít CSR-t (503), a telephely nem tárol kulcsot (a naplóban hibaként) |
| N4 | **Felhős tartalék** (K1.2): zárt nap jelentése, ha a telephely hallgat | **kész** — az NTAK-kliens a közös `k2`-ben; felhő: bérlői V24 (`ntak_felho_zarva`, a törzs bájtra pontosan), óránkénti kör (`siduri.ntak.tartalek`), ellenőrzés, UJRA_KULDENDO; `szinkron/1.22.0` (`felhoZarvaNapok`); telephely: V53 (`ntak_napzaras.felhobol`) — a jelentett napra nem küld, a visszavontat maga jelenti, és ha itt munkanap volt, hangosan naplóz. 5 felhős + 1 telephelyi teszt, 11 mutációs próba |
