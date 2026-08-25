# `admin` (K2) — még nincs kiadva

**Ez a könyvtár szándékosan üres.** Nem felejtettük el: a K2 az F2-ben készül,
és **üres váz-szerződést kiadni rosszabb, mint nem kiadni** — mert azt a
fogyasztók elkezdenék használni.

**Amit már most tudunk róla, és a megírásakor kötelező:**

| # | Kikötés |
|---|---------|
| a | ⚠️ **Két megvalósítása lesz** — a felhő és a telephelyi szerver —, és **ugyanaz a szerződésteszt fut mindkettőn.** Ez teszi a §22.2-t („egy admin, két helyről kiszolgálva") ígéretből géppel ellenőrizhető kényszerré |
| b | **A csak helyi funkciók** *(eszközszerep, nyomtató-átirányítás, integráció ideiglenes tiltása)* **külön útvonalcsoportban**, mert ezeknek a felhőben nincs párjuk, és offline is működniük kell *(WEBADMIN_STACK §13.4)* |
| c | **Az export és az import a K2 része**, nem külön felület — minden listás nézethez jár *(EXPORT_IMPORT §2.1)* |
| d | **Az offline korlát a válaszban látszik:** a telephelyi kiszolgálás 30 napnál régebbi adatot nem tud adni, és **ezt meg kell mondania**, nem csendben rövidebb listát adni |
