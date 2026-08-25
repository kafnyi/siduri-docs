# Szerződés-változásnapló

**Minden szerződésváltozás ide kerül, a kiadás előtt.** Nem utólagos
összefoglaló: ez az a hely, ahol a **szerződésgazda** jóváhagyása megjelenik.

**Formátum:** szerződés · verzió · dátum · a változás · **törő-e**.

---

## `kassza` (K1)

### v1.0.0 — 2026-08-25 — *első kiadás*

Az F1 fázis bizonyító szelete: egy termék → kosár → készpénzes fizetés →
nyomtatás valódi adóügyi eszközre.

**Végpontok:** termékek lekérdezése (változás-jelzővel), rendelés nyitása,
tétel felvétele, rendelés lezárása, adóügyi eredmény jelentése.

**Amit szerkezetileg rögzít, mert utólag nem tehető bele:**

| Mi | Miért az első kiadásban |
|----|------------------------|
| `Siduri-Epoch` fejléc minden íráson | A HA az F6-ban épül, de egy protokollmező felvétele később **minden kliens minden verzióját** érinti |
| `Idempotencia-Kulcs` minden íráson | A degradált módból való visszajátszás **definíció szerint ismétel** |
| `(epoch, szamlalo)` sorrend minden rekordon | A sorrendet nem a fali óra adja |
| Eszközönként elhatárolt bizonylatszám | Az ütközés így **szerkezetileg lehetetlen** |
| Külön, nullázható adóügyi bizonylatszám | Nem minden bizonylathoz tartozik, és soha nem a Siduri szám helyett áll |
| Összeg egész forint; egységköltség, mennyiség, árfolyam **szövegként** | Az I1 invariáns a protokollon is érvényes, vagy sehol |

**Kimondott hiányok, nem elfeledett részek:**

| Hiány | Mikor pótoljuk |
|-------|----------------|
| **Eszközregisztráció és kezelői bejelentkezés** — a szelet már hitelesített állapotból indul | **F2** |
| **Leküldő eseménycsatorna** (KDS, rendeléskijelző, asztaltérkép) | **F1-ben eldöntendő** *(SZERZODES §7, S1)* |
| **Az eszköz azonosságának mechanizmusa** — a kölcsönös TLS a javaslat, a döntés nyitva | *(SZERZODES S5)* |

---

## `admin` (K2)

*Még nincs kiadva.* A K2-nek **két megvalósítása lesz** — a felhő és a
telephelyi szerver —, és a szerződésteszt mindkettőn ugyanaz fut. Ez teszi a
§22.2 ígéretét gépi kényszerré.

---

## `szinkron` (K3)

*Még nincs kiadva.* A **legszigorúbb kompatibilitási kényszerű** szerződés: a
felhő és a telephely soha nem frissül egyszerre.
