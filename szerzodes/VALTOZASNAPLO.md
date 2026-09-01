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

### v1.1.0 — 2026-08-26 — *eseménycsatorna borítéka* `NEM TÖRŐ`

**Új fájl:** `kassza/v1/esemenyek.yaml` — a leküldő eseménycsatorna üzenetalakjai.

**Miért most, amikor a csatorna csak az F5-ben épül meg:** ugyanaz az ok, amiért
az epoch mező az első naptól benne van a kérésekben. **Egy protokollmező
utólagos felvétele minden kliens minden verzióját érinti** — most ingyen van,
egy év múlva átállási terv.

| Mit rögzít | Miért |
|-----------|-------|
| Az esemény sorszáma **ugyanaz a `(epoch, számláló)` pár** | Nem új mechanizmus. A régebbi generációjú esemény azonnal felismerhető, és szerepváltás után nem kell külön „ürítsd a gyorsítótárat" üzenet |
| **Újracsatlakozás: `POTLAS` vagy `UJRATOLTES`** | Az `UJRATOLTES` nem hibajelzés. ⚠️ Csendben folytatni tilos: a kliens azt hinné, naprakész, holott lyuk van a történetében |
| **Szívverés, és 5 másodperces elavulási küszöb** | Egy TCP-kapcsolat percekig „nyitva" maradhat egy halott szerver felé |

**Nem törő változás:** új fájl, meglévő alak nem módosult.
