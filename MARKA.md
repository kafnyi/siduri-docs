# Siduri — márkaelemek

**A logó megérkezett** *(a `dev` ág `Siduri/` mappájában)*, és a korábbi becsült
színek helyére **mért értékek** kerültek.

| Fájl | Mi | Méret |
|------|----|-------|
| `Siduri-Logo.png` | A jel — az alak, felirat nélkül | 1129 × 1293 |
| `Siduri-FullLogo.png` | Jel + „SIDURI" felirat, függőleges | 1128 × 1608 |
| `Siduri-flat.png` | Vízszintes sáv, „SIDURI / By Myth Systems" | 3815 × 1024 |

---

## 1. ⚠️ Három dolog, amit a fájlokról tudni kell

### 1.1 A „vektoros" fájlok NEM vektorosak

Mindhárom `*-Vector.svg` **egyetlen `<image>` elem, beágyazott PNG-vel**. Nulla
`<path>`, nulla valódi görbe — a raszterkép egy SVG-borítékba csomagolva.

| Következmény | Miért számít |
|--------------|--------------|
| **Nem skálázódik** | Nagyításnál ugyanúgy pixeles, mint a PNG |
| **Nagyobb, mint a PNG** | A base64 ~33%-ot ad hozzá: a 1,5 MB-os PNG-ből 2,0 MB-os „SVG" lett |
| **Nem konvertálható XAML-be** | A WPF vektoros rajzot tudna használni; itt nincs mit konvertálni |
| **A kis méretű jel nem vezethető le** | Marad, hogy **meg kell rajzolni** |

> **Ha van igazi vektoros eredeti** (AI, EPS, PDF, vagy valódi path-okból álló
> SVG), az sokat érne. Ha nincs, az sem tragédia — de akkor a kisméretű jelet
> és a nyomtatóra valót külön kell megrajzolni, és ezt jobb most tudni.

### 1.2 A vízszintes logónak fekete kerete van

A `Siduri-flat.png` szélén `#000000` keret fut körbe. **Ez a márkaszínek között
nem szerepel**, és sötét felületen kifejezetten rosszul mutat. Valószínűleg
exportálási maradvány — érdemes keret nélkül is elmenteni.

### 1.3 Kisméretű jel továbbra sem létezik

A logó **hajszálvékony arany áramkörvonalakat** tartalmaz. 16 × 16 képponton
(böngészőfül, alkalmazásikon) ezek szürke pacává mosódnak; az adóügyi nyomtató
egyszínű, alacsony felbontású kimenetén szintén eltűnnek — **és a
bizonylatfejléc az, amit a vendég hazavisz.**

---

## 2. A mért márkaszínek

Nem becslés: a `Siduri-Logo.png` átlátszatlan képpontjaiból számolva.

| Szerep | Érték | Hol |
|--------|-------|-----|
| **Mélyzöld-kék** | `#194254` | Ruha, haj, felirat |
| **Arany** | `#C9A460` | Amfora, diadém, áramköri vonalak |

*(A korábbi becslésem `#1A4C5D` és `#C9A961` volt — az aranyon közel jártam, a
kéken nem: a valódi sötétebb és kevésbé kék.)*

---

## 3. A felület palettája

**A felület színei nem a logó színei, csak passzolnak hozzájuk.** A logó fehér
alapra készült arculati elem; a felület este, félhomályban, órákon át nézett
munkaeszköz.

**A jelforrás a `marka.json`**, az ellenőrzés az `eszkozok/marka_ellenoriz.py`.

### 3.1 Sötét téma — ez az alapértelmezés

| Token | Érték | |
|-------|-------|--|
| `hatter` | `#0E1D25` | Nem tiszta fekete: a `#000000` a rákerülő szöveget túlélesíti |
| `felulet` | `#152B35` | |
| `felulet_emelt` | `#1E3A47` | Párbeszédablak, kiemelt kártya |
| `keret` | `#2C4E5D` | |
| `szoveg` | `#E6EDF1` | Törtfehér, nem `#FFFFFF` — sötétben az vakít |
| `szoveg_halvany` | `#A7BDC8` | |
| `arany` | `#C9A460` | |
| `hiba` / `figyelmeztetes` / `siker` | `#F08A7A` / `#E8B860` / `#7DC49B` | |

### 3.2 Világos téma

Nappali pultnál, ablak mellett a sötét felület tükröz — ezért kell. De **az
alapértelmezés a sötét**, mert az a gyakoribb üzemmód.

| Token | Érték | |
|-------|-------|--|
| `hatter` | `#F4F1EC` | Törtfehér |
| `felulet` | `#FFFFFF` | |
| `szoveg` | `#194254` | A márkaszín |
| `szoveg_halvany` | `#4A6B7A` | |
| `arany` | `#C9A460` | **Csak dísz** — lásd lent |
| `arany_szoveg` | `#7D6330` | Ha aranynak szöveget kell hordoznia |
| `hiba` / `figyelmeztetes` / `siker` | `#A32E1C` / `#7A5600` / `#1E6B45` | |

---

## 4. Egy fordulat, amit a mérés hozott

**A sötét téma megmenti az aranyat.**

| Az arany… | Kontraszt | Ítélet |
|-----------|-----------|--------|
| világos felületen (`#FFFFFF`) | **2,34:1** | ⚠️ Szövegre alkalmatlan |
| világos háttéren (`#F4F1EC`) | **2,08:1** | ⚠️ Rosszabb |
| **sötét felületen** (`#152B35`) | **6,27:1** | ✅ Szövegre is jó |
| **sötét háttéren** (`#0E1D25`) | **7,34:1** | ✅ |

Korábban azt írtam: *„az arany a Siduriban dísz, nem információ."* **Ez a sötét
témában nem igaz** — ott az arany teljes értékű szövegszín. A megkötés csak a
világos témára marad érvényben, és ott is van megoldás: az `arany_szoveg`
(`#7D6330`, 5,68:1).

**Ez nem szerencse, hanem következmény:** az arany egy közepesen világos szín,
ezért sötét alapon működik, világoson nem. Aki világos alapból indul, azt az
arany végig akadályozza; aki sötétből, annak segít.

---

## 5. Amit a `marka_ellenoriz.py` betartat

Minden szín–háttér páros minden témában, **WCAG 2.1 AA** küszöbök szerint. A
szkript **hangosan elbukik**, ha valamelyik a küszöb alá megy.

> **Miért kell ez gép:** a „kíméli a szemet" és az „olvasható" két külön
> követelmény, és könnyű az elsőt úgy teljesíteni, hogy a második elvész. A
> tompítás a **telítettséget** viszi le, nem a kontrasztot — de ezt egy
> szemre végzett igazítás nem garantálja.

Jelenleg mind a **38 páros** megfelel.

---

## 6. `[NYITOTT]` Ami a fájlokból még hiányzik

| # | Kérdés | Miért nem tippelhető meg |
|---|--------|--------------------------|
| a | **Valódi vektoros eredeti** | Lásd §1.1 |
| b | **Kisméretű, egyszerűsített jel** (16–32 px) | A vékony vonalak eltűnnek; a nagyból nem vezethető le, meg kell rajzolni |
| c | **Egyszínű változat a bizonylatfejléchez** | Az adóügyi nyomtató egyszínű és alacsony felbontású |
| d | **Sötét háttérre szánt változat** | A jel fehér alapra készült; a felület alapértelmezésben sötét |
| e | **Keret nélküli vízszintes logó** | Lásd §1.2 |
| f | **A „By Myth Systems" alsorral mi a szabály?** | A POS fejlécében nincs rá hely; kell-e egyáltalán a terméken belül |

---

## 7. Hova kerülnek ezek

**Egy jelforrás, három cél** *(a `WEBADMIN_STACK.md` W2 nyitott kérdése —
ezzel lezárva)*. A `marka.json`-ból generálódik:

| Cél | Alak |
|-----|------|
| Webes admin (Vue) | CSS egyéni tulajdonságok |
| POS kliens (WPF) | `ResourceDictionary` |
| Vékonykliensek (Flutter) | Dart konstansok |

**A generálás fordítási lépés, nem kézi másolás.** A kézi másolás garantáltan
szétcsúszik, és a szétcsúszást senki nem veszi észre, mert mindegyik felület
külön-külön jól néz ki.

> **A logófájlok jelenleg a `dev` ágon vannak.** Ahhoz, hogy a POS kliens és a
> webes admin használni tudja őket, be kell kerülniük azokba a repókba is —
> ez ágkezelési döntés, ezért nem nyúltam hozzá.
