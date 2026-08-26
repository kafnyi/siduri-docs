# Tesztvektorok — a pénzszabályok közös igazsága

**Miért van erre szükség:** ugyanazokat a pénzszabályokat **legalább három
nyelven** meg kell valósítani — Java a szerveren, C# a POS kliensen, Dart a
vékonyklienseken. **A kettőzés elkerülhetetlen**, mert a kliensnek a szerver
válasza előtt is ki kell írnia a sorösszeget, és a készpénzes kerekítést a
fizetőképernyőn kell mutatnia.

> **Amit a kettőzés ellen tenni lehet, az nem az, hogy ne kettőzzünk — hanem
> hogy MINDEGYIK megvalósítás UGYANARRA a vektorkészletre feleljen.**

**Ezek a fájlok a specifikáció, nem a megvalósítás lenyomata.** Kézzel
készültek a szabályokból; ha egy megvalósítás megbukik rajtuk, **a megvalósítás
a hibás**, nem a vektor. Új vektort csak akkor veszünk fel, ha a szabály
változik — és akkor a változásnaplóba is bekerül.

| Fájl | Mit rögzít |
|------|-----------|
| `kerekites.json` | Készpénzes kerekítés öt forintra, a különbözettel |
| `afa.json` | Áfa-visszaszámolás áfakulcs-csoportonként |
| `sorosszeg.json` | Sorösszeg egész darabszámmal és tört mennyiséggel |
