# Siduri — márkaelemek

> ⚠️ **Ez a fájl a logó SZÍNEIRŐL szól, nem tartalmazza a logót.** A logót
> képként kaptam meg a beszélgetésben; **fájlként nincs a birtokomban**, tehát
> nem tudtam berakni a repóba. A forrásfájl (lehetőleg **SVG** vagy a vektoros
> eredeti) beküldése után kerül ide, és akkor a lenti értékek is pontosíthatók.

---

## 1. ⚠️ A színek BECSLÉSEK

**A lenti hexadecimális értékeket szemre olvastam le a küldött képről.** Nem a
forrásfájlból származnak, tehát **nem hitelesek**. A képernyőn 1–2 egységnyi
eltérés nem látszik, **nyomdában és arculati anyagon viszont igen** — a
végleges értékeket a vektoros eredetiből kell kivenni.

| Szerep | Becsült érték | Hol jelenik meg a logón |
|--------|---------------|-------------------------|
| **Mélyzöld-kék (fő)** | `#1A4C5D` | A ruha, a haj, a „SIDURI" felirat |
| **Arany (kiegészítő)** | `#C9A961` | Az amfora, a diadém, az áramköri vonalak |
| **Világos arany** | `#D9B36B` | Az amfora világosabb töltése |
| **Alap** | `#FFFFFF` | A logó háttere |

---

## 2. Amit a színekről MÉRNI lehet — és amiből következik valami

A kontrasztarány nem ízlés kérdése: kiszámolható, és a
**WCAG 2.1 AA** küszöbei (normál szöveg **4,5:1**, nagy szöveg **3:1**)
eldöntik, mire használható egy szín.

| Páros | Arány | Ítélet |
|-------|-------|--------|
| Mélyzöld-kék **fehéren** | **9,39:1** | Bármire jó — ez a szövegszín |
| Fehér **mélyzöld-kéken** | **9,39:1** | Bármire jó — ez a fejléc |
| Arany **fehéren** | **2,25:1** | ⚠️ **Szövegre alkalmatlan**, nagy szövegre is |
| Arany **mélyzöld-kéken** | **4,17:1** | Normál szövegre kevés, **nagy szövegre jó** |

### Amit ebből ki kell mondani

**Az arany a Siduriban DÍSZ, nem információ.** Keret, elválasztó, kiemelt
felület széle, ikon egy sötét felületen — igen. Felirat fehér alapon, állapot
jelzése, hibaüzenet — **nem**. Nem stílusdöntés: 2,25:1 mellett a pult mögött
álló ember **rossz fényben nem olvassa el**.

Ha az aranynak mégis szöveget kell hordoznia fehér alapon, **sötétebb változat
kell hozzá** — `#8A6D2F` már **4,87:1**, tehát megfelel. Ez viszont már
**nem a logó aranya**, tehát külön tokenként kell léteznie, nem a márkaszín
„egy kicsit sötétebben" használataként.

---

## 3. `[NYITOTT]` Amit a forrásfájl fog eldönteni

| # | Kérdés | Miért nem tippelhető meg |
|---|--------|--------------------------|
| a | **A pontos színértékek** | Lásd fent |
| b | **Van-e egyszerűsített jel** kis méretre? | A logón **hajszálvékony arany áramkörvonalak** vannak. 16×16 képponton (böngészőfül, alkalmazásikon) ezek **szürke pacává mosódnak**. Kell egy külön, egyszerűsített változat — az nem levezethető a nagyból, azt meg kell rajzolni |
| c | **Sötét háttéren mi a viselkedés?** | A felület sötét témát is kap. Fehér háttérre rajzolt logót sötét felületre tenni pont akkor néz ki rosszul, amikor a legtöbbet nézik |
| d | **Egysoros változat?** | A POS fejlécében nincs függőleges hely egy alak + felirat kompozíciónak |
| e | **Nyomtatott bizonylaton?** | Az adóügyi nyomtató **egyszínű, alacsony felbontású**. A finom vonalak ott is eltűnnek — és a bizonylatfejléc az, amit a vendég a kezében visz haza |

---

## 3.5 A FELÜLET palettája — nem ugyanaz, mint a logóé

**A logó színei a logóé; az alkalmazásé csak PASSZOLJON hozzájuk.** Ez nem
engedmény, hanem szükségszerű: a logó fehér alapra készült arculati elem, a
felület pedig egy este, félhomályban, órákon át nézett munkaeszköz.

| # | Kikötés | Miért |
|---|---------|-------|
| a | **Sötét téma az ALAPÉRTELMEZÉS**, nem a világos | A Siduri legtöbb üzemórája este és éjjel telik. Egy világos felület a sötét teremben **fényforrás**, amibe a felszolgáló minden rendelésnél belenéz |
| b | **Semmi neon, semmi tiszta telített szín** nagy felületen | A telített kék-zöld és a tiszta fehér az, amitől négy óra után fáj a szem. A felületek **tompított, alacsony telítettségű** változatok |
| c | **A legvilágosabb felület se legyen tiszta fehér**, a legsötétebb se tiszta fekete | A `#FFFFFF` sötétben vakít; a `#000000` pedig a rá kerülő szöveget élesíti túl (halo-hatás). Törtfehér és mélyszürke a két véglet |
| d | **A kontrasztminimumok ettől NEM lazulnak** | „Kímélje a szemet" nem jelenti azt, hogy „olvashatatlan". A 4,5:1 továbbra is alsó határ — a tompítás a **telítettséget** viszi le, nem a kontrasztot |
| e | **A jelzőszínek (hiba, figyelmeztetés) maradnak erősek** | Amit észre KELL venni, azt észre kell venni. A tompítás a nyugalmi állapoté, nem a riasztásé |

> **Világos téma is kell**, mert nappali pultnál, ablak mellett a sötét felület
> tükröz. De **az alapértelmezés a sötét** — az a gyakoribb üzemmód.

---

## 4. Hova kerülnek ezek a színek

**Egyetlen közös jelforrás, mindhárom felületre** *(a `WEBADMIN_STACK.md` W2
nyitott kérdése)*. A webes admin (Vue), a POS kliens (WPF) és a vékonykliensek
(Flutter) **nem ugyanazt a fájlformátumot eszik**, tehát a közös forrás nem
lehet egyikük saját formátuma sem.

**Javaslat:** egy semleges `marka.json`, amiből mindhárom cél generál —
CSS egyéni tulajdonságokat, WPF `ResourceDictionary`-t, Dart konstansokat.
A generálás **fordítási lépés**, nem kézi másolás: a kézi másolás garantáltan
szétcsúszik, és a szétcsúszást senki nem veszi észre, mert mindegyik felület
külön-külön jól néz ki.

**Ez a javaslat addig nem valósul meg, amíg a színek becslések** — egy rossz
értéket három helyre generálni rosszabb, mint egy helyen tartani.
