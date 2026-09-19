# `admin` (K2) — v1.0.0, első szelet: csak olvasás

**Kiadva: 2026-09-19.** A fájl: [`admin.yaml`](admin.yaml).

Az első szelet **kategóriafa + termeklista + egy termék a kiszerelésekkel**,
**írás nélkül.**

> ✅ **Az írást blokkoló kérdés 2026-09-19-én eldőlt** (`NYITOTT_KERDESEK.md`
> **O3**): mindkét hely írhat, az ütközést **mezőnkénti időbélyeg** oldja fel, a
> későbbi írás nyer, és a **vesztes érték az auditban és a felületen látható
> marad**. Az írás így a **következő szelet** (`admin/1.1.0`), aminek ezt a
> szabályt már a szerződésben is hordoznia kell: a válaszban benne kell lennie,
> **melyik mező mikor és honnan kapta az értékét**.

**A négy kikötés, amivel ez a szerződés megíródott — és hogy hol áll mindegyik:**

| # | Kikötés | Állapot az 1.0.0-ban |
|---|---------|----------------------|
| a | **Két megvalósítása lesz** — a felhő és a telephelyi szerver —, és **ugyanaz a szerződésteszt fut mindkettőn** | A szerződés mindkét kiszolgálót felsorolja, és a válasz `Siduri-Kiszolgalo` fejléce megmondja, melyik szolgált ki. **Amíg csak az egyik megvalósítás létezik, a teszt egy oldalon fut** — kimondva a szerződés leírásában |
| b | **A csak helyi funkciók külön útvonalcsoportban** | Még nincs ilyen végpont. **Üres csoportot nem adunk ki** |
| c | **Az export és az import a K2 része**, minden listás nézethez | Még nincs benne: a könyvtárválasztás nyitott (`EXPORT_IMPORT.md` §6.1, Apache POI kontra GraalVM). Az `osszesen` mező viszont **már most** benne van, mert az export a teljes szűrt eredményt adja majd, és ezt a felületnek előre ki kell írnia |
| d | **Az offline korlát a válaszban látszik** (30 nap) | Ebben a szeletben **nincs időkorlátos adat** — a törzsadat nem az. A kimutatásoknál kötelező lesz |

**Amit a szelet szerkezetileg rögzít**, mert utólag nem tehető bele: a telephely
megnevezése minden kérésen, a kiszolgáló megnevezése minden válaszban, a
**kurzoros** lapozás, és a pénz egész forintban.
