#!/usr/bin/env python3
"""A markapaletta kontrasztjainak ellenorzese.

MIERT VAN EZ: a "kimeli a szemet" es az "olvashato" ket kulon kovetelmeny, es
konnyu az elsot ugy teljesiteni, hogy a masodik elveszik. Ez a szkript minden
szin-hatter parost ujraszamol, es HANGOSAN elbukik, ha valamelyik a WCAG 2.1 AA
kuszob ala megy.

A szam nem izles kerdese: kiszamolhato, tehat ellenorizheto.
"""
import json
import pathlib
import sys

GYOKER = pathlib.Path(__file__).resolve().parent.parent
NORMAL_KUSZOB = 4.5   # WCAG 2.1 AA, normal szoveg
NAGY_KUSZOB = 3.0     # WCAG 2.1 AA, nagy szoveg


def luminancia(hexa):
    hexa = hexa.lstrip("#")

    def csatorna(ketjegy):
        c = int(ketjegy, 16) / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return (0.2126 * csatorna(hexa[0:2])
            + 0.7152 * csatorna(hexa[2:4])
            + 0.0722 * csatorna(hexa[4:6]))


def kontraszt(egyik, masik):
    a, b = luminancia(egyik), luminancia(masik)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def ellenoriz(marka):
    hibak = []
    sorok = []

    for tema in ("sotet", "vilagos"):
        p = marka[tema]
        hatterek = [("hatter", p["hatter"]), ("felulet", p["felulet"]),
                    ("felulet_emelt", p["felulet_emelt"])]
        elotertek = [("szoveg", p["szoveg"], NORMAL_KUSZOB),
                     ("szoveg_halvany", p["szoveg_halvany"], NORMAL_KUSZOB),
                     ("hiba", p["hiba"], NORMAL_KUSZOB),
                     ("figyelmeztetes", p["figyelmeztetes"], NORMAL_KUSZOB),
                     ("siker", p["siker"], NORMAL_KUSZOB)]

        # Az arany a SOTET temaban szovegre is jo; a vilagosban NEM - ott az
        # arany_szoveg token a helyes valasztas. A kulonbseg nem izles: 2,34:1.
        if tema == "sotet":
            elotertek.append(("arany", p["arany"], NORMAL_KUSZOB))
        else:
            elotertek.append(("arany_szoveg", p["arany_szoveg"], NORMAL_KUSZOB))

        for elonev, elo, kuszob in elotertek:
            for hattnev, hatt in hatterek:
                ertek = kontraszt(elo, hatt)
                jo = ertek >= kuszob
                sorok.append(f"  {tema:8} {elonev:16} / {hattnev:14} "
                             f"{ertek:5.2f}:1  {'OK' if jo else 'BUKIK'}")
                if not jo:
                    hibak.append(
                        f"{tema}.{elonev} a {tema}.{hattnev} felett {ertek:.2f}:1 "
                        f"(kell: {kuszob}:1)")

    # A markakek mint felulet - a fejlec ilyen.
    marka_kek = marka["marka"]["melyzoldkek"]
    feher = kontraszt("#FFFFFF", marka_kek)
    sorok.append(f"  markafelulet feher / melyzoldkek  {feher:5.2f}:1  "
                 f"{'OK' if feher >= NORMAL_KUSZOB else 'BUKIK'}")
    if feher < NORMAL_KUSZOB:
        hibak.append(f"feher a markakek felett {feher:.2f}:1")

    arany_kek = kontraszt(marka["marka"]["arany"], marka_kek)
    sorok.append(f"  markafelulet arany / melyzoldkek  {arany_kek:5.2f}:1  "
                 f"{'csak NAGY szoveg' if arany_kek < NORMAL_KUSZOB else 'OK'}")
    if arany_kek < NAGY_KUSZOB:
        hibak.append(f"arany a markakek felett {arany_kek:.2f}:1 - nagy szovegre sem eleg")

    return sorok, hibak


def main():
    marka = json.loads((GYOKER / "marka.json").read_text(encoding="utf-8"))
    sorok, hibak = ellenoriz(marka)
    print("\n".join(sorok))

    if hibak:
        print("\nELBUKOTT:", file=sys.stderr)
        for hiba in hibak:
            print(f"  - {hiba}", file=sys.stderr)
        print("\nA 'kimeli a szemet' nem jelenti azt, hogy 'olvashatatlan'. A "
              "tompitas a TELITETTSEGET viszi le, nem a kontrasztot.", file=sys.stderr)
        return 1

    print("\nMinden paros megfelel a WCAG 2.1 AA kuszobnek.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
