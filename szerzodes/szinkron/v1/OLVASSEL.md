# `szinkron` (K3) — még nincs kiadva

**Ez a könyvtár szándékosan üres.**

**A K3 a legszigorúbb kompatibilitási kényszerű szerződés**, mert **a felhő és
a telephely soha nem frissül egyszerre.** Legalább **két kiadási ciklusnyi**
visszafelé kompatibilitás kell.

**Amit a megírásakor el kell dönteni:**

| # | Kérdés |
|---|--------|
| **S3** | A **tömeges átvitel** alakja: a napi szinkron nem ugyanaz, mint egy rendelés felküldése. Lehet, hogy külön formátum kell |
| **W3** | ⚠️ **Törzsadat-szerkesztés offline telephely mellett** — a tulajdonos laptopról árat ír át a felhőben, miközben az étterem internete áll. **Melyik az igazság forrása, és mi történik ütközésnél?** Ezt a K3 megírása ELŐTT kell eldönteni, mert a szerződés alakját határozza meg *(WEBADMIN_STACK §14)* |
