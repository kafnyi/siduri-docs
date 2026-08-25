# Jogosultság- és indokkód-katalógus

**Utolsó frissítés:** 2026-08-23
**Fázis:** F1 (adatmodell) — az audit napló (§18.4) és a jogosultsági rendszer (§18.1) hivatkozik rá

---

## 0. `[DÖNTÉS]` Nyelvhasználat a kódban

Ez itt dől el, mert a jogosultságkódok **adatbázisban és API-ban is megjelennek**,
tehát a döntés visszamenőleg drága.

> **Tartományi fogalmak MAGYARUL, technikai állványzat ANGOLUL.**

| Réteg | Nyelv | Példa |
|-------|-------|-------|
| **Tartomány** (entitás, mező, jogosultságkód, indokkód) | **magyar** | `bizonylat`, `munkanap`, `gyujto`, `targynap`, `eladas.gyorseladas` |
| **Technikai állványzat** (osztálynevek utótagjai, keretrendszer-fogalmak) | angol | `BizonylatRepository`, `MunkanapService` |

**Miért — és ez nem ízlés kérdése:**

| # | Indok |
|---|-------|
| a | **A tartomány magyar szabályozási tartomány.** A `gyűjtő`, `AP-szám`, `tárgynap`, `TAM`, `AJT` fogalmaknak **nincs pontos angol megfelelője** — a fordítás információt veszít |
| b | **Az NTAK interfész maga is magyar** (`rendelesOsszesitok`, `afaKategoria`, `helybenFogyasztott`). Angol belső név mellett minden határátlépésnél fordítani kellene |
| c | ⚠️ **Bizonyítottan hibaforrás.** **Mi magunk követtük el ezt a hibát:** az „NTAK tárgynap = naptári nap" tévedés (H1) **pontosan abból származott, hogy két különböző napfogalmat egyetlen angol szóra (`day`) képeztünk le a fejünkben.** A pontos magyar szó ezt a hibát nem engedte volna meg |

---

# I. RÉSZ — JOGOSULTSÁGOK

## 1. Működési szabályok

| # | Szabály |
|---|---------|
| 1.1 | **A katalógus ADAT, nem kód** — frissítéssel bővíthető, kliens-újratelepítés nélkül |
| 1.2 | **Új jogosultság a meglévő szerepeken alapból TILTOTT**, de **feltűnő jelzéssel**, hogy dönteni tudjanak róla *(A2 + A5 elv)* |
| 1.3 | **Az ügyfél maga hozhat létre és módosíthat SZEREPEKET**, nem csak egyedi kivételeket kap |
| 1.4 | **Egyedi kivétel** felülírhatja a szerepet, felhasználónként |
| 1.5 | **A Siduri admin szerep sérthetetlen** — nem módosítható, nem csökkenthető, jelszava nem írható át *(§18.2)* |
| 1.6 | **A `siduri.*` jogosultságok SOHA nem delegálhatók** — nem is jelennek meg az ügyfél admin felületén |
| 1.7 | **Minden jogosultságváltozás auditnaplózott, a biztonsági ágon** — ez felértékelődött, mert az olvasást nem naplózzuk *(§18.4)* |

## 2. `[ÚJ]` Jogosultság csökkentett módban

**Ez eddig sehol nem szerepelt, pedig naponta előfordul.**

Ha a kliens nem éri el a szervert, **honnan tudja, mit szabad a bejelentkezett
felhasználónak?**

| # | Szabály |
|---|---------|
| 2.1 | **A kliens gyorsítótárazza a jogosultsági halmazt**, és degradált módban ezt használja |
| 2.2 | **A `siduri.*` jogosultságok soha nem gyorsítótárazódnak** — helyben úgysem gyakorolja őket senki |
| 2.3 | **A jogosultság-változás visszakapcsoláskor érvényesül.** Ha valakitől elvettek egy jogot, amíg a gép offline volt, **a gép ezt nem tudhatta** — ez **elfogadott kockázat**, mert az alternatíva az, hogy offline senki nem tud dolgozni |
| 2.4 | **A gyorsítótár korlátozott érvényességű.** Ha a kliens N napja nem látta a szervert, a **magas kockázatú jogosultságok lejárnak** (sztornó, árfelülírás, kedvezmény küszöb felett) — a sima eladás soha |

## 3. `[ÚJ]` Egyszeri felhatalmazás (vezetői jóváhagyás)

**Standard pénztárgép-viselkedés, amit eddig nem specifikáltunk.**

A pincér sztornózni akar, de nincs joga. **Nem az a megoldás, hogy kilép és az
üzletvezető bejelentkezik** — az lassú, és a műszak is összekeveredne.

> **Az üzletvezető a helyszínen jóváhagyja az EGY műveletet a saját PIN-jével,
> anélkül hogy a munkamenet gazdát cserélne.**

| # | Szabály |
|---|---------|
| 3.1 | **A jóváhagyás EGY műveletre szól**, nem időablakra és nem munkamenetre |
| 3.2 | ⚠️ **Az audit MINDKÉT személyt rögzíti:** ki volt bejelentkezve **és** ki hagyta jóvá. **Ez nem opcionális** — enélkül a nyom hamis képet ad, és pont a felelősséget mossa el |
| 3.3 | **Jogosultságonként állítható, hogy engedélyezhető-e így** — van, amit nem szabad futtában jóváhagyni |
| 3.4 | **A `siduri.*` jogosultságok így SEM gyakorolhatók** |

## 4. A katalógus

**Jelölés:** ⚠️ = **indokkód kötelező** · 🔒 = **csak Siduri, nem delegálható**

### 4.1 Eladás

| Kód | Mit enged |
|-----|-----------|
| `eladas.gyorseladas` | Gyorseladás (asztal nélkül) |
| `eladas.asztalra` | Eladás asztalra |
| `eladas.fizetes.keszpenz` | Készpénzes fizetés |
| `eladas.fizetes.kartya` | Kártyás fizetés |
| `eladas.fizetes.utalvany` | Utalvány elfogadása |
| `eladas.fizetes.valuta` | Valuta elfogadása |
| `eladas.fizetes.vegyes` | Vegyes fizetés |
| `eladas.szamla_keres` | Számla kiállítása nyugta helyett |
| `eladas.szamlamegosztas` | Számla szétbontása |

### 4.2 Rendelés és asztal

| Kód | Mit enged |
|-----|-----------|
| `rendeles.megnyitas` | Asztal megnyitása |
| `rendeles.mas_pincer_asztala` | **Más pincér asztalának** megnyitása/módosítása |
| `rendeles.athelyezes` | Rendelés áthelyezése másik asztalra |
| `rendeles.osszevonas` | Asztalok összevonása |
| `rendeles.vendegszam_modositas` | Vendégszám módosítása |
| `rendeles.fogas_inditas` | Következő fogás indítása |
| `rendeles.nem_fizetett_lezaras` ⚠️ | Rendelés lezárása fizetés nélkül |

### 4.3 Tétel

| Kód | Mit enged |
|-----|-----------|
| `tetel.torles_kuldes_elott` | Tétel törlése, **mielőtt** a konyhára ment |
| `tetel.torles_kuldes_utan` ⚠️ | Tétel törlése, **miután** a konyhára ment |
| `tetel.mennyiseg_modositas` | Mennyiség módosítása |

> **A `tetel.torles_kuldes_utan` a legfontosabb visszaélési pont** — a
> törlési arány riport (§26) pontosan ezt méri, nem a nyers törlésszámot.

### 4.4 Ár és kedvezmény

| Kód | Mit enged |
|-----|-----------|
| `ar.kezi_felulriras` ⚠️ | Kézi árfelülírás |
| `kedvezmeny.tetel` | Tételszintű kedvezmény |
| `kedvezmeny.vegosszeg` | Végösszeg-kedvezmény |
| `kedvezmeny.kuszob_felett` ⚠️ | Kedvezmény a beállított küszöb fölött |
| `szervizdij.modositas` | Szervizdíj módosítása egy rendelésen |

### 4.5 Sztornó

| Kód | Mit enged |
|-----|-----------|
| `sztorno.bizonylat` ⚠️ | Lezárt bizonylat sztornózása |
| `sztorno.mas_muszakbol` ⚠️ | **Másik műszak** bizonylatának sztornózása |

### 4.6 Nap és műszak

| Kód | Mit enged |
|-----|-----------|
| `nap.nyitas` | Munkanap nyitása |
| `nap.zaras` | Munkanap zárása |
| `nap.kezi_zaras` | **Kézi** napzárás, ha automatikus van beállítva |
| `muszak.nyitas` / `muszak.zaras` | Saját műszak |
| `muszak.atadas` | Műszakátadás |
| `muszak.mas_felhasznaloe` | **Más felhasználó** műszakának zárása |
| `muszak.osszesito_lathato` | **A műszak összesítőinek megtekintése** |

> ⚠️ **A `muszak.osszesito_lathato` a VAKZÁRÁS kapcsolója**, fordított logikával:
> **akinek NINCS meg, az vakzárást csinál.** Nem külön „vakzárás" jelző —
> egy jogosultság hiánya, ami magától hozza a helyes viselkedést.
>
> **Emlékeztető (§9.2/a):** a védelmet **kiütheti az adóügyi eszköz
> X-jelentése** — azt is korlátozni kell, különben látszatvédelem.

### 4.7 Kassza

| Kód | Mit enged |
|-----|-----------|
| `kassza.befizetes` / `kassza.kifizetes` | Készpénz be- és kifizetés |
| `kassza.folozes` | Kassza fölözése |
| `kassza.fiok_nyitas_eladas_nelkul` ⚠️ | Fiókynyitás eladás nélkül |
| `kassza.borravalo_kifizetes` | Borravaló kifizetése *(bizonylatolt készpénzmozgásként, §16.6)* |

### 4.8 Termékkatalógus

| Kód | Mit enged |
|-----|-----------|
| `termek.megtekintes` | Terméktörzs megtekintése |
| `termek.letrehozas` / `termek.modositas` | Termék létrehozása és módosítása |
| **`termek.ar_modositas`** | **Ár módosítása** — külön, mert érzékenyebb |
| **`termek.afa_modositas`** | **Áfakulcs módosítása** — még érzékenyebb |
| `termek.inaktivalas` / `termek.soft_delete` | Életciklus |
| `termek.vonalkod_hozzarendeles` | **Ismeretlen vonalkód hozzárendelése** *(§1.3.1)* |
| `kategoria.kezeles` · `modosito.kezeles` · `menu.kezeles` | Szerkezetek |

> **Az ár és az áfa azért külön jogosultság**, mert a hibairányuk nem
> egyenértékű: egy rossz terméknév kellemetlen, **egy rossz áfakulcs
> jogsértés** *(A5 elv)*.

### 4.9 Készlet

| Kód | Mit enged |
|-----|-----------|
| `keszlet.megtekintes` | Készletadatok |
| `keszlet.bevetelezes` | Bevételezés |
| `keszlet.raktarkozi_mozgas` | Raktárközi mozgás |
| `keszlet.selejt` | Selejtezés |
| `keszlet.szemelyzeti` | Személyzeti fogyasztás rögzítése |
| `keszlet.elfogyott_jelzo` | **„Elfogyott" jelző** be/ki *(§17.6/c)* |
| `keszlet.leltar_inditas` | Leltár indítása |
| `keszlet.leltar_rogzites` ⚠️ | **Leltári eredmény rögzítése** (korrekciós mozgás) |
| `recept.megtekintes` / `recept.szerkesztes` | Receptúra |

### 4.10 Riport

| Kód | Mit enged |
|-----|-----------|
| `riport.napi_forgalom` | Napi forgalmi riportok |
| **`riport.beszerzesi_arak`** | **Beszerzési árak** |
| **`riport.arres`** | **Árrés és food cost** |
| `riport.borravalo` | Borravaló-riport *(bérszámfejtéshez, §16.6)* |
| `riport.asztal_tortenet` | Asztaltörténet |
| **`riport.felhasznalo_tortenet`** | **Felhasználó-történet** |
| `riport.torlesi_arany` | Törlési arány riport |

> ⚠️ **A `riport.felhasznalo_tortenet` megnyitásakor jelenik meg a munkajogi
> figyelmeztetés** *(§18.4)* — **ott, ahol a funkciót használják**, nem egyszer
> a telepítéskor. Ez a nézet **munkavállalói megfigyelés**, akármilyen szépen
> néz ki.
>
> A **beszerzési ár és az árrés** azért külön jogosultság, mert **egy pincérnek
> nincs köze hozzá** — és mivel az olvasást nem naplózzuk *(§18.4)*, **a
> jogosultság az egyetlen védelem.**

### 4.11 Felhasználó és jogosultság

| Kód | Mit enged |
|-----|-----------|
| `felhasznalo.megtekintes` · `felhasznalo.letrehozas` · `felhasznalo.modositas` | Felhasználókezelés |
| `felhasznalo.jelszo_csere_mase` | **Más** jelszavának/PIN-jének cseréje |
| `felhasznalo.soft_delete` | Kilépett dolgozó *(a napló érintetlen marad, §N0.2)* |
| `szerep.kezeles` | Szerepek létrehozása és módosítása |
| `jogosultsag.kiosztas` | Jogosultság adása és elvétele |

### 4.12 Beállítás

| Kód | Mit enged |
|-----|-----------|
| `beallitas.telephely` | Telephelyi alapadatok |
| `beallitas.nyitvatartas` | **Nyitvatartási minta** *(az NTAK zárva-nap jelzéshez, §11.7)* |
| `beallitas.automatikus_napzaras` | Tervezett napzárás időpontja és szünete |
| `beallitas.nyomtatas_routing` | Nyomtatási útvonalak |
| `beallitas.eszkoz` | Eszközbeállítások |
| `beallitas.drs` | **DRS terhelési szabály** *(helyben fogyasztásnál is terhelünk-e, §14.3)* |
| `beallitas.18plusz` | 18+ piktogram be/ki és termékbesorolás |

### 4.13 Integráció

| Kód | Mit enged |
|-----|-----------|
| `integracio.ugyfel_eszkoz` | **(B) osztály:** nyomtatók, KDS, kijelzők — **szabadon, lejárat nélkül** *(§19.1)* |
| `integracio.vedett.ideiglenes_kikapcsolas` ⚠️ | **(A) osztály:** bankkártya-terminál, adóügyi eszköz — **1 órás lejárattal**, csak ha Siduri delegálta |

### 4.14 🔒 Csak Siduri — soha nem delegálható

| Kód | Mit enged |
|-----|-----------|
| `siduri.nyers_audit` | **Nyers auditnapló** megtekintése *(§18.4)* |
| `siduri.arva_tranzakcio_feloldas` | **Árva tranzakció feloldása** *(M13)* |
| `siduri.tartos_integracio_kikapcsolas` | **Lejárat nélküli** integráció-kikapcsolás *(L2.3, 3. szint)* |
| `siduri.fiskalis_integracio_delegalas` | Annak engedélyezése, hogy az ügyfél kikapcsolhassa a **fiskális** integrációt *(§19.5)* |
| `siduri.nyomtatas_atiranyitas` | Nyomtatás átirányítása másik eszközre *(§19.6)* |
| `siduri.eszkoz_regisztracio` | Eszköz regisztrálása, eszközszám kiosztása *(§8.2)* |
| `siduri.vekonykliens_fizetes` | A vékonykliens fizetési képességének bekapcsolása *(§21.2)* |
| `siduri.licenc_kezeles` | Licenc és csomagszint |

---

## 5. Alapértelmezett szerepek — SABLONOK, nem kényszer

**Telepítéskor létrejönnek, az ügyfél szabadon átírja őket** *(1.3)*.

| Szerep | Mit kap nagyjából |
|--------|-------------------|
| **Pincér** | Eladás asztalra, rendeléskezelés, fogásindítás, tételtörlés **küldés előtt**. Saját műszak. **Nincs**: sztornó, árfelülírás, küszöb feletti kedvezmény, beszerzési ár |
| **Pultos** | Mint a pincér + gyorseladás. **Alapból nincs `muszak.osszesito_lathato`** → **vakzárás** |
| **Műszakfelelős** | + tételtörlés küldés után, sztornó, küszöb feletti kedvezmény, „elfogyott" jelző, más felhasználó műszakának zárása |
| **Üzletvezető** | + termékkatalógus, készlet, leltár, riportok (árréssel), felhasználókezelés, beállítások |
| **Tulajdonos** | Minden ügyféloldali jog |
| **Siduri admin** | Minden + a `siduri.*` kör. **Sérthetetlen** |

---

# II. RÉSZ — INDOKKÓDOK

## 6. Szabályok

| # | Szabály |
|---|---------|
| 6.1 | **Az indokkód LISTÁBÓL választott**, nem szabad szöveg — különben elemezhetetlen |
| 6.2 | **Minden listán van `EGYEB`, és ott a szabad szöveg KÖTELEZŐ** |
| 6.3 | **A lista ADAT** — az ügyfél bővítheti a sajátjaival, de **az alapkészletet nem törölheti** (különben a riportok összehasonlíthatatlanná válnának telephelyek között) |
| 6.4 | Az indok **a biztonsági auditágba** kerül *(§18.4)* |
| 6.5 | ⚠️ **Az indokkód nem mentesít.** Egy „PANASZKEZELÉS" kód nem teszi jogossá a műveletet — **nyomot hagy, nem felmentést ad** |

## 7. Készletek

### 7.1 Sztornó és tételtörlés küldés után

| Kód | Jelentés |
|-----|----------|
| `VENDEG_ELALLT` | A vendég meggondolta magát |
| `TEVES_FELUTES` | Rossz tétel |
| `MINOSEGI_KIFOGAS` | A vendég visszaküldte |
| `KONYHAI_HIBA` | A konyha rontotta el |
| `ARHIBA` | Rossz ár került rá |
| `EGYEB` | *(szabad szöveg kötelező)* |

### 7.2 Küszöb feletti kedvezmény

`TORZSVENDEG` · `PANASZKEZELES` · `MARKETING_AKCIO` · `VEZETOI_DONTES` · `EGYEB`

### 7.3 Kézi árfelülírás

`EGYEDI_MEGALLAPODAS` · `RENDEZVENY_AR` · `ARHIBA_JAVITAS` · `EGYEB`

### 7.4 Leltári rögzítés

| Kód | Jelentés |
|-----|----------|
| `FIZIKAI_ELTERES` | A számlálás mást mutatott |
| `KORABBI_ROGZITESI_HIBA` | Elmaradt vagy hibás korábbi rögzítés |
| `ROMLAS_TORES` | Romlás, törés |
| `LOPASGYANU` | **Külön kód**, mert ez a riportban máshogy kezelendő |
| `EGYEB` | *(szabad szöveg kötelező)* |

### 7.5 Fiókynyitás eladás nélkül

`VALTOPENZ` · `TEVEDES` · `ELLENORZES` · `EGYEB`

### 7.6 Nem fizetett lezárás

| Kód | Jelentés |
|-----|----------|
| `VENDEG_TAVOZOTT_FIZETES_NELKUL` | Távozott fizetés nélkül |
| `HAZ_VENDEGE` | A ház vendége |
| `PANASZ_ELENGEDES` | Panasz miatt elengedve |
| `SZEMELYZETI` | Személyzeti fogyasztás |
| `EGYEB` | *(szabad szöveg kötelező)* |

### 7.7 Integráció ideiglenes kikapcsolása

`NINCS_HALOZAT` · `ESZKOZ_MEGHIBASODAS` · `KABEL_SZAKADAS` · `ESZKOZ_NEM_VALASZOL` · `EGYEB`

### 7.8 Óraállítás

`AUTOMATIKUS_SZINKRON` · `KEZI_JAVITAS` · `CMOS_ELEM_HIBA` · `EGYEB`

### 7.9 `[KÜLÖNLEGES]` Degradált mód — ez az NTAK-ba MEGY

| Kód | NTAK-jelentés |
|-----|---------------|
| `ARAMSZUNET` | áramszünet |
| `RENDSZERKIESES` | rendszerkiesés |
| `HALOZATKIESES` | hálózatkiesés |

> **Ez az egyetlen indokkód-készlet, ami elhagyja a rendszert:** ez tölti ki az
> NTAK `osszesitettIndoklasa` mezőjét *(§11.6)*. Ezért **a szövegének a
> hatóság felé is értelmesnek kell lennie** — nem belső rövidítés.

---

## 8. Amit ez a katalógus MOST old meg

| # | Korábban nyitott | Most |
|---|------------------|------|
| a | „küszöb feletti kedvezmény indokot igényel" — **milyen indokot?** | 7.2 |
| b | „a vakzárás jogosultsághoz kötött" — **melyikhez?** | `muszak.osszesito_lathato`, fordított logikával |
| c | „a fiskális integráció kikapcsolása nem delegálható alapból" — **hogyan?** | `siduri.fiskalis_integracio_delegalas` |
| d | „az olvasás nem naplózódik, helyette jogosultság szabályoz" — **milyen bontásban?** | 4.10, külön az árrés és a beszerzési ár |
| e | **Jogosultság offline?** *(eddig sehol)* | 2. szakasz |
| f | **Vezetői jóváhagyás kilépés nélkül?** *(eddig sehol)* | 3. szakasz — **és az audit MINDKÉT személyt rögzíti** |
