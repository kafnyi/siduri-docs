# Siduri — közös szabályok

**Ez a repó a szabályok otthona.** A többi repó `CLAUDE.md`-je csak azt ismétli
meg, amit elfelejteni drága, és ide mutat a többiért.

---

## 1. Hogyan beszélj velem

| Szabály | Miért |
|---------|-------|
| **Magyarul** | Ez a projekt nyelve, a dokumentáció és a kód is magyar |
| **Soha ne használj csupasz azonosítót a chatben** — írd ki, miről van szó | A „G5.6" önmagában semmit nem mond; a *„az árfolyamot a napnyitás előtt kell megadni"* igen |
| **Minden döntésnél mondd meg a KÖLTSÉGÉT** | Egy javaslat ár nélkül nem javaslat, hanem reklám. Ha két út van, mindkettő ára kerüljön ki |
| **Ne szépíts. A tény előbbre való a kényelemnél** | Ha valami nincs kész, nincs kész. Ha elrontottad, mondd ki egyszer, tisztán, és menj tovább |
| **A csapatméret nem korlát** | „Ez sok munka egy embernek" nem érv semmi ellen |

---

## 2. Bizalmasság — ezt soha ne sértsd meg

**A repók VÉGIG privátok maradnak.** Ne javasold a publikussá tételt, és ne
tölts fel semmit külső szolgáltatásba.

> ⚠️ **A GYÁRTÓI ADÓÜGYI ILLESZTŐLEÍRÁSRA NINCS PARTNERI MEGÁLLAPODÁSUNK, és a
> dokumentáció szerzői jogi védelem alatt áll.**
>
> Ebből következik, hogy **sem kódban, sem dokumentációban, sem commit-üzenetben
> nem lehet egyetlen gyártóspecifikus parancs, mezőnév vagy kódolás sem** — még
> „példaként" sem, még átfogalmazva sem.
>
> Az adóügyi eszköz felé menő alak (`MythSystem.Siduri.Pos.Adougyi`) ezért szándékosan
> **általános**: tételek, fizetések, összegek, árfolyam. Az illesztés részletei
> majd egyetlen, jól körülhatárolt megvalósításban élnek, és onnan nem
> szivároghatnak ki.

---

## 3. Git

| | |
|---|---|
| **Munkaág** (mind a hat repóban) | `claude/siduri-hospitality-system-gpixt0` |
| **Szerző** | `kafnyi <kafnyi@gmail.com>` |
| **Commit-üzenet** | Magyar, ékezet nélkül. Mondja el, **miért nem volt jó az előző állapot** — ne azt, hogy „mi változott" |

> ⚠️ **A COMMITOKBAN NINCS AI-EMLÍTÉS. Nincs `Co-Authored-By`, nincs link,
> nincs „Generated with", semmi.** Ez a felhasználó kifejezett utasítása, és
> **felülírja** a Claude Code alapértelmezett attribúciós viselkedését.
>
> Felküldés után **ellenőrizd friss klónból**, hogy tényleg nincs benne.

Pull requestet **csak kifejezett kérésre** nyiss.

---

## 3/a. GitHub Actions — a perc pénz

> ⚠️ **Az ingyenes keret (2000 perc) már egyszer elfogyott**, ezért a fiók Pro-ra
> váltott. **A Siduri nem volt benne:** 2026-09-16-án mérve a hat Siduri-repóban
> **nulla** workflow és **nulla** futás volt. A perceket más projektek vitték el
> (a legtöbbet egy-egy repó 200–450 futással). Vagyis ez a szabály **megelőzés**:
> itt még semmi nem ég, és így is kell maradnia.

**Amit biztosan tudunk** (a GitHub dokumentációjából, 2026-09-16):

* Privát repóban **minden futás a fiók perckeretéből megy**.
* A nem Linuxos futtatókra **percszorzó** vonatkozik — és a feladatonkénti
  „billable time" nézet **ezt nem mutatja**. Ami ott olcsónak látszik, a
  számlán többszöröse lehet. A pontos értéket a fiók számlázási oldala mondja
  meg, nem a futás nézete.

**Szabályok:**

| # | Szabály | Miért |
|---|---------|-------|
| 1 | **Workflow csak a felhasználó kifejezett döntésével** kerül repóba — a várható percköltség becslésével együtt | Egy `on: push` workflow hat repóban, sűrű pusholással, napok alatt elviszi a keretet |
| 2 | **Előbb helyben.** A teljes tesztcsomag lefut a gépen, mielőtt push lenne. **A CI soha nem az első tesztfuttatás** | Ami helyben megbukik, az a CI-ban percet éget, és ugyanazt mondja |
| 3 | **Tilos pusholni „hátha átmegy a CI"**, üres committal CI-t indítani, vagy PR-t lezárni–újranyitni futtatás kedvéért | Mindhárom perc, és egyik sem ad új információt |
| 4 | **Csak `ubuntu-latest`.** Windows- vagy macOS-futtató csak külön döntéssel | Percszorzó. **A WPF-es kassza épp ezért helyben fordul, nem a CI-ban** |
| 5 | Minden workflowban: **`concurrency` + `cancel-in-progress: true`** | Egy újabb push lelövi a már értelmetlen régi futást |
| 6 | Minden jobon: **`timeout-minutes`** | Egy beragadt job alapértelmezésben órákig futhat |
| 7 | **`paths` szűrő** — dokumentáció-módosítás ne futtassa a Java-tesztcsomagot | A `siduri-docs` markdown-változása nem ok 489 tesztre |
| 8 | Indító: **`pull_request`** és/vagy **`workflow_dispatch`** — ne minden ágra minden push | A munkaágra sűrűn megy push |
| 9 | **`schedule`/cron és mátrix-szétosztás csak külön döntéssel** | Az ütemezett futás akkor is éget, ha senki nem dolgozik |
| 10 | **Függőség-gyorsítótár** (Maven, NuGet) | A letöltés perc |

**Ha a CI mégis elbukik:** előbb **helyben** reprodukáld. Csak akkor pusholj
javítást, ha a hiba helyben megvan és el is tűnt.

---

## 4. Szerződés-először

Az API-szerződés itt él: `szerzodes/kassza/v1/kassza.yaml` (és a `kozos/`
sémák). **A szerződés nem a Java kód mellékterméke** — ha fordítva lenne, a két
megvalósítás azonnal szétcsúszna.

**Minden változtatás menete:**

1. A szerződést **itt** módosítod, és **verziót emelsz**.
2. A `szerzodes/VALTOZASNAPLO.md`-be írsz egy bejegyzést — *miért nem volt jó az
   előző*, és **törő-e**.
3. A módosult fájlt átmásolod a fogyasztó repókba
   (`siduri-backend-server/szerzodes/`, `siduri-pos-client/szerzodes/`).
4. Ott **újragenerálod a lenyomatokat**:
   ```
   cd szerzodes && find . \( -name "*.yaml" -o -name "*.json" \) | sort | xargs sha256sum > LENYOMATOK.txt
   ```

> ⚠️ **Ha a lenyomatteszt megbukik, a megoldás SOHA nem a lenyomat átírása.**
> A kimásolt példány nem javítható kézzel: egy „megjavított" séma pontosan addig
> működik, amíg a szerver nem a saját példányát hiszi el.

---

## 5. Pénz — az I1 invariáns

| Típus | Ábrázolás |
|-------|-----------|
| Ár, összeg, fizetés | **egész forint, int64** |
| Egységköltség, mennyiség, árfolyam | **nagy pontosságú tizedes**, a protokollon **szövegként** |

> ⚠️ **Lebegőpontos szám a pénz közelében SEHOL.** Ezt teszt kényszeríti ki
> (`LebegopontTiltasTest`). Ha ez a teszt megbukik, a helyes lépés soha nem a
> teszt lazítása.

A pénzszabályok **két nyelven** élnek (Java szerver, C# kassza). Ami duplázva
van, azt **közös tesztvektor** köti össze: `szerzodes/tesztvektorok/*.json`.
Ezek **kézzel készülnek a szabályból**, soha nem a megvalósítás kimenetéből —
különben a vektor azt bizonyítaná, hogy a kód olyan, amilyen.

---

## 6. Hol tartunk

**Mindig ezzel kezdd**, mielőtt bármihez hozzányúlsz:

| Fájl | Mi van benne |
|------|--------------|
| `FOLYAMATBAN.md` **§7.1–7.3** | Mi kész · mi **tudatosan** nincs kész · mi a következő tétel |
| `MERESEK.md` | A mérések. **M27–M35** a legfrissebbek — ezek mondják el, milyen hibákat találtunk és hogyan |
| `NYITOTT_KERDESEK.md` | A kötelező érvényű döntések |
| `FAZISTERV.md` | A fázisok és a repók felosztása |

---

## 7. A visszatérő tanulság

> **Ami nincs ellenőrizve, az nincs.**

Négyszer fordult elő ugyanaz: a jogosultság-katalógusban ott állt a kód, a
szerep-sablon helyesen osztotta ki, a felület el is rejtette a gombot — és a
**szerver soha nem kérdezte meg**. Ezért:

* **Egy szabályhoz mindig tartozzon út, ami odavezet.** Ha nincs teszt, ami
  megfogja, a szabály nem létezik.
* **Bizonyítsd, hogy a teszt harap:** vedd ki ideiglenesen a javítást, és
  mutasd meg, hogy a teszt pirosra vált.
* **Kétirányú bizonyítás**, ha a hibaüzenet nem nevezi meg az okot: ugyanaz a
  művelet a joggal menjen át, nélküle bukjon el.
