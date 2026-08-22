# Siduri - Rendszer Specifikáció és Tervezet

> ## ⚠ EZ A FÁJL NEM AZ IGAZSÁGFORRÁS — MUTATÓ
>
> Ez a dokumentum a rendszer **eredeti terve**. Több pontja **elavult**: a
> 2026-08-22-i tervezési munkamenetben hozott döntések felülírják.
>
> **A kötelező érvényű döntések helye: [`NYITOTT_KERDESEK.md`](NYITOTT_KERDESEK.md).**
> (MERNOKISAROKKOVEK §2.4: egy igazságforrás, a többi csak mutató — és a mutató
> mondja ki, hogy mutató.)
>
> Az alábbi fejezeteknél `[MÓDOSÍTVA]` / `[NYITOTT]` jelölés került a szövegbe.
> **Ahol ilyet látsz, a `NYITOTT_KERDESEK.md`-t olvasd, ne ezt.**
>
> Az aktuális állapot és a folytatás: [`FOLYAMATBAN.md`](FOLYAMATBAN.md).

## Fogalomtár
* **POS (Point of Sale):** Fizikai, érintőképernyős vastagkliensek (AIO gépek) perifériákkal (terminál, nyomtató).
* **PDA:** Telefonos/tabletes vékonykliensek a pincérek kezében (rendelésfelvétel).
* **KIOSK:** Önkiszolgáló rendelő és fizető terminálok a vendégek számára.

## 1. Rendszer Koncepció
* **Célpiac:** Magyar KKV vendéglátás (12 millió Ft árbevétel feletti, NTAK köteles helyek). Fejlesztő: Siduri Systems.
* **Fő eladási érv (USP):** Offline-first architektúra (lokális hálózaton működő rendszer), amely ellenáll az internetkimaradásnak, utólagos felhőszinkronizációval.

## 2. Tervezett Technológiai Stack
* **Backend:** Java (Spring Boot) - lokális szerveren futtatva. (A J1900-as hardverkorlátok miatt kötelezően GraalVM Native Image-re fordítva, szigorú PostgreSQL memórialimitekkel).
  * `[MÓDOSÍTVA — B3]` **Megerősítve, hogy a GraalVM kényszer marad**: a J1900 **meglévő telepített bázis**. A bázis **VEGYES** — J1900 fut szerverként **és** POS kliensként is. Utóbbiból következik, hogy **a WPF kliens teljesítmény-költségvetése is szoros** (lásd 20. pont: 720p másodkijelzős videó egy Bay Trail iGPU-n). §4: ez **mérendő valós J1900-on**, nem becsülhető.
* **Adatbázis Archiválás (Purging):** A 64GB-os SSD kímélése érdekében a lokális szerver havonta automatikusan tömöríti/törli a felhőbe már szinkronizált, 30 napnál régebbi tranzakciós naplókat (Event Log) és lezárt nyugtákat.
  * `[NYITOTT — A3]` **A 30 napos purge ütközhet a számviteli megőrzési kötelezettséggel.** A megőrzési idő **nincs forrásból igazolva** (§13.5). Amíg nincs, erre építeni tilos.
* **Adatbázis:** PostgreSQL.
* **Asztali Kliens / Pénztárgép:** C# (WPF, modern .NET 8+) - `[MÓDOSÍTVA — A1]` **Kizárólag Windows 10 IoT Enterprise (LTSC).**
  * **A Linux-támogatás TÖRÖLVE.** A WPF nem fut Linuxon; az Avalonia UI-ra váltást megvizsgáltuk és elvetettük, mert nem lesz Linuxos POS. A konkrét LTSC-build és a `.NET Desktop Runtime` telepíthetősége telepítési tétel (D2).
* **Mobil / Pincér Kliens:** Flutter (esetleg webes UI).

## 3. Alapvető Funkciók (MVP)
* Lokális, hálózatfüggetlen működés belső wifin.
* NTAK adatszolgáltatás: Aszinkron üzenetsoron (Message Queue) keresztül. Ha az NTAK szerver nem elérhető, a POS azonnal lezárja a fizetést, a háttérfolyamat pedig később újrapróbálja.
* SoftPOS integráció bankkártyás fizetéshez.
* Kliensoldali QR-kódos asztali rendelés közvetlenül a helyi szerverre.

## 4. Architektúra és Topológia
* **Topológiai beállítás:** A rendszer telepítéskor konfigurálható tisztán lokális (dedikált gép a szerver) VAGY tisztán felhős/távoli szerveres működésre.
* **Kliens Auto-discovery:** Szabványos mDNS (Multicast DNS) használata lokális hálózaton, hogy a kliensek IP-változás esetén is megtalálják a szervert.

## 5. Asztali Kliens (Pénztárgép) Felület és Beléptetés
* Teljes képernyős (kioszk mód) futtatás azonnali bejelentkező képernyővel.
* Felhasználók listázása vizuális azonosítást segítő avatárokkal és nevekkel. Csak PIN-kódot elfogadó jelszómező.
* Hardveres bejelentkezés támogatása: RFID / kártyaolvasó integráció.

## 6. Étterem (Asztaltérkép) Nézet
* Vizuális asztaltérkép szerkesztő: rajzolható háttér, asztalok elhelyezése és testreszabása.
* Asztalhoz rendelhető adatok: dedikált felszolgáló, törzsvendég profil, és asztal-szintű kedvezmények.
* Asztalonkénti jogosultságkezelés.

## 7. Rendelésfelvétel és Asztalkezelés
* Asztal megnyitásakor alapértelmezett vendégszám automatikus felajánlása.
* Rendelés rögzítése asztalra vagy specifikus vendéghez rendelve.
* Jobb oldali panel nézetei: felütés sorrendje, vendégenként, vagy fogásonként (összevont nézettel).
* Proforma (előnyugta) nyomtatása után 'fizetésre vár' státusz, új tétel esetén automatikus visszaváltás.
* Számlabontás: Proforma és fizetés bontása vendégenként vagy manuális tételes bontással.

## 8. Asztal- és Vendégkezelés (Haladó)
* Vendégek dinamikus hozzáadása/törlése (csak tételmentes vendég törölhető).
* Átültetés (Table/Guest transfer) meglévő fogyasztás esetén figyelmeztetéssel.
* Ideiglenes asztalok kezelése (térképen nem megjelenő, dinamikus asztalok fizetésig).
* Több helyiség/zóna kezelése térképes 'átjárókkal' (gombokkal).

## 9. Értékesítési Nézet (Gyors eladás és Asztal nézet)
* Egységes felület. Felső sáv: Kiszerelésválasztó, Sztornó, Sztornó Mind gombok.
* 'Védett' tételek státusza (üzletenként paraméterezhető).
* Elvitel (Takeaway) kezelés és Automata ÁFA-váltás: A rendszer a jogszabályoknak megfelelően a háttérben automatikusan módosítja a helyben fogyasztott ÁFA-kulcsot elvitelesre, fixen tartva a bruttó árat.
* Szintén granulárisan adható kedvezmény (teljes asztalra, vendégre, rendelésre, tételre).

## 10. Jogosultsági Rendszer
* Extrém granuláris jogkörök (gomb- és végpontszintű engedélyek).
* Felhasználói szintek (Role-ok) és egyedi kivételek (Overrides).
* Rendszergazdai (Siduri Systems Szuperfiók) beégetett profil a támogatáshoz.
* Helyi offline hitelesítés (hash alapján) és vizuális konnektivitás indikátor.

## 11. Nyomtatási és Blokk Kiosztási Rendszer (Routing)
* Célnyomtatók és példányszámok dinamikus, termékcsoport és helyszín/gép alapú útvonaltervezése (Routing).
* **Nyomtató Fallback (Katasztrófa útvonal):** Ha a konyhai blokknyomtató 5 mp-en belül nem válaszol, a rendszer a pultba küldi a blokkot "KONYHAI NYOMTATÓ HIBA" felirattal.

## 12. Hardver és Periféria Integrációk
* NAV-engedélyes adóügyi pénztárgépek integrációja (pl. Micra, CashCube).
* Hagyományos bankkártya terminálok összekötése (a SoftPOS mellett).
* Széleskörű hőnyomtató (ESC/POS szabvány) támogatás.

## 13. Pénzügyek, Számlázás, Kedvezmények és Fizetési Módok
* **ÁFÁ-s Számlázás:** Számlázz.hu / Billingo API, vagy adóügyi nyomtatón "Egyszerűsített számla".
* **Kedvezmények (Proporcionális elosztás):** Adóügyi nyomtatóhoz a végösszegi kedvezményt a rendszer ÁFA-kulcs arányosan osztja szét a tételeken (0 Ft-os tételek elkerülése).
* **Szervízdíj:** Dinamikusan megjelenő ÁFA tartalommal.
* **5 Ft-os Kerekítés és Visszajáró:** Készpénznél automatikus kerekítés, dinamikus visszajáró számítás. Vegyes (készpénz + kártya) fizetés kezelése, EUR/HUF váltás.
* **Törlés vs. Sztornó:** Nyitott tétel = Törölhető (Void). Lezárt, fizetett nyugta = Csak Sztornózható (negatív bizonylattal).
* **Fizetési Biztonság (Állapotgép):** Bankkártya fizetésnél Two-Phase Commit. Terminál timeout esetén UI megerősítés (Igen/Megszakítás). Összegmódosításnál megszakítás + újraküldés. Sztornónál automatikus Refund parancs. Nyomtatóhiba esetén függő tranzakció.

## 14. Napi Működés és Kasszaműveletek (Műszakok)
* Egy munkanapon belül több felhasználóhoz/géphez kötött műszak. Napi árfolyam kötelező megadása.
* **NTAK Napi Zárás:** Automatikus aszinkron forgalmi és ÁFA-összesítő beküldés napzáráskor.
* Készpénz ki/befizetések, kassza fölözése (skimming) bizonylattal. Műszakátadás változatlan kasszaállással (fölözés nélkül).
* **Borravaló elszámolása:** Készpénzes borravaló kivétele a műszak végén. Kártyás borravaló külön riportálva a könyvelésnek (nem módosítja a fizikai kasszát).
* Kassza eltérés naplózása nyitáskor (hiány/többlet regisztrálása).

## 15. Többraktáras Készletkezelés és Háttérrendszer
* Korlátlan raktár (Főraktár, Pult), raktárközi mozgások bizonylatolása.
* **Repi (Személyzeti) és Selejt:** Szigorúan Készletmozgásként (Inventory Adjustment) rögzítve, nem eladásként (NAV és NTAK megkerülése, tiszta könyvelés).
* **Bevételezés és Mozgó Átlagár:** Beszerzési egységár megadása alapján Árrés (Margin) kalkuláció.
* **Standolás (Leltár):** Rendszeres fizikai készletellenőrzés. Beállítható "Kalkulált veszteség %" (pl. 2% csapolási veszteség) a hiány tolerálására. Receptúrák (BOM) kezelése.

## 16. Hálózati Kommunikáció és Kliens Állapot
* Kliens oldali Exponential Backoff újracsatlakozási logika.
* **Versenyhelyzet védelem (Optimistic Locking):** Asztalszerkesztéseknél verziószám (versioning) ellenőrzi az ütközéseket.

## 17. Kliens Szerepkörök és Failover (High Availability) Stratégia
* ~~**Vastagkliensek:** AIO PC-k helyi PostgreSQL replikával.~~
  * `[MÓDOSÍTVA — A2]` **A „helyi PostgreSQL replika" TÖRÖLVE.** A rendszer **szerver-autoritatív**: minden megosztott állapot (asztalok, rendelések, készlet, kedvezmények, műszak) a szerveren dől el. A POS-on **cache + tartós, append-only outbox** van, **nem** PostgreSQL replika.
  * **Degradált mód:** ha a Master **és** az Emergency Server is halott, a POS **gyorseladást** tud végezni nyugtával (tétel → fizetés → nyomtatás), és az eseményeket az outboxba írja, amit visszatéréskor lejátszik.
  * `[MÓDOSÍTVA — A2/a]` **A nyitott asztalok ilyenkor NEM elérhetők** — a pincér kézzel, gyorseladásként üti fel újra a fogyasztást. Ez tartja meg a „nincs megosztott módosítható állapot" invariánst, amire az egész degradált mód épül.
  * `[?]` **FIGYELEM:** az egész degradált mód egy **igazolatlan premisszán** áll (AEE-s gépnél az adóügyi eszköz állítja ki és sorszámozza a jogi bizonylatot). Kódolás előtt igazolandó — ha hamis, ez a fejezet megdől.
* **Vékonykliensek:** Mobil/PDA (Flutter), szerverhiba esetén automatikus leállás (védelem dupla felütés ellen).
* **Emergency Server (Vészhelyzeti Szerver):** Dedikált Standby PC, amely Master hiba esetén átveszi az irányítást (mDNS). Szigorú Split-brain védelem és Master Lockout mechanizmus. A visszaállás csak Szuperfiókkal történhet.
  * `[NYITOTT — B1, A4]` **Az egész HA-fejezet DÖNTÉSRE VÁR.** Megírt, de még el nem fogadott javaslat: a HA **kerüljön ki az MVP-ből** (az A2 degradált módja után az Emergency Server már kényelmi funkció, nem katasztrófavédelem), viszont az **epoch-mező kerüljön be a protokollba az első naptól**. Továbbá: aszinkron replikáció, **kézi** failover (jogosultsághoz kötve, nem szerephez), és **kétszintű failback** — helyi menedzser a normál esetre, Szuperfiók csak divergált adatok felülírásához.
  * **Fogalmi csúszás, amit ez a fejezet elkövet:** az USP (1. pont) az **internetkimaradás** elleni védelem, amit már a lokális szerver megold. Az Emergency Server viszont a **lokális szerver hardverhibája** ellen véd — másik, sokkal ritkább esemény. A kettő összemosása miatt látszik a HA indokoltabbnak, mint amennyire az.

## 18. Menedzsment Interfészek (Online és Offline)
* Operatív (POS) és Adminisztrációs (Raktár/BOM/Statisztika) rétegek. Az adminisztráció internetkimaradás esetén is elérhető lokális weben. 

## 19. Licenckezelés és Jogosultság (DRM)
* Felhőből kezelt hardveres ujjlenyomat (Fingerprinting) alapú licencelés.
* **Heartbeat:** 10 napos Offline türelmi idő.
* **NTAK SLA Figyelmeztetés:** 18 óra offline állapot után kritikus piros riasztás a 24 órás kötelező adatszolgáltatási limit miatt.

## 20. Másodkijelző (Vendégtájékoztató)
* Rendelés, borravaló felület és idle állapotban videó/kép lejátszása (automata konvertálással 720p/1024x768).

## 21. Vevőhívó (Order Ready Board)
* Különálló, arculatosítható alkalmazás (Smart TV/Android) WebSocket kommunikációval ("Készül" / "Átvehető").

## 22. Standoló / Készletellenőrző Alkalmazás
* PDA modul vonalkódolvasással, illetve weben generálható papíralapú standívek és utólagos felrögzítés.

## 23. Konyhai Kijelző Rendszer (KDS)
* Érintőképernyős (Android/Windows) kijelző, drag-and-drop státuszváltással (triggereli a vevőhívót).

## 24. Külső Integrációk (REST API)
* Foodora / Wolt natív KDS és POS integráció. CRM és hűségprogram API.

## 25. Fejlett Analitika és Riportolás (BI)
* Dinamikus grafikonok a felhőben. 
* **Valós Árrés (Margin):** Beszerzési átlagáron alapul, dinamikus "Kalkulált veszteség %" csúszkával kiegészítve a tiszta profit modellezéséhez.

## 26. Speciális Termékkezelés (DRS és Repohár)
* **DRS (REpont):** ÁFA-körön kívüli, nem kedvezményezhető fix +50 Ft (kötelezően a szülőtermékhez kötve).
* **Repohár (Token):** Képes termékként (pozitív) és visszaváltásként (negatív tétel, készpénzkiadási tranzakció) működni.