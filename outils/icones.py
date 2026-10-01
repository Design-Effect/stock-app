#!/usr/bin/env python3
"""Fabrique les icônes de l'app et le logo d'en-tête depuis le vrai logo Healthy Sounna.

Source : le logo haute définition du catalogue (`assets/brand/logo-hd.png` du dépôt
healthy-sounna-catalogue, 2480 x 1886, alpha), passé en argument.
Même traitement que `marketing/cession/preparer_logo.py` de ce dépôt :
  1. isoler l'hexagone HS par sa forme (pas de rognage fixe du liseré) ;
  2. reboucher en blanc le « H », qui est un trou transparent dans le pavé noir.

Usage : python3 outils/icones.py <chemin/vers/logo-hd.png>
"""
import sys

import numpy as np
from PIL import Image

CREME = (250, 246, 236, 255)   # --creme de l'app (#FAF6EC)


def contenu(a, seuil=10):
    ys, xs = np.nonzero(a[..., 3] > seuil)
    return ys.min(), ys.max(), xs.min(), xs.max()


def trous(transparent):
    """Zones transparentes non reliées au bord : les trous à reboucher."""
    dehors = np.zeros_like(transparent)
    dehors[0], dehors[-1], dehors[:, 0], dehors[:, -1] = (
        transparent[0], transparent[-1], transparent[:, 0], transparent[:, -1])
    while True:
        etendu = dehors.copy()
        for axe, d in ((0, 1), (0, -1), (1, 1), (1, -1)):
            etendu |= np.roll(dehors, d, axis=axe)
        etendu &= transparent
        if etendu.sum() == dehors.sum():
            return transparent & ~dehors
        dehors = etendu


def composante(masque, y, x):
    """Pixels de `masque` reliés au point (y, x) : diffusion en numpy pur."""
    zone = np.zeros_like(masque)
    zone[y, x] = True
    while True:
        etendu = zone.copy()
        for axe, d in ((0, 1), (0, -1), (1, 1), (1, -1)):
            etendu |= np.roll(zone, d, axis=axe)
        etendu &= masque
        if etendu.sum() == zone.sum():
            return zone
        zone = etendu


def hexagone(source):
    """L'hexagone HS isolé par sa forme : on part du premier pixel opaque de la
    colonne centrale (le haut de l'hexagone) et on garde ce qui y est relié.
    Un rognage fixe du liseré mangeait le haut de l'hexagone, qui commence à
    45 px du bord de la source (défaut vu le 01/10 sur la première icône)."""
    a = np.array(Image.open(source).convert("RGBA")).astype(np.int16)
    a = a[:int(a.shape[0] * 0.45)]
    opaque = a[..., 3] > 25
    x = a.shape[1] // 2
    y = int(np.argmax(opaque[:, x]))
    zone = composante(opaque, y + 2, x)
    ys, xs = np.nonzero(zone)
    haut = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()
    garde = zone[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    haut[~garde & (haut[..., 3] > 25)] = 0   # rien d'étranger à l'hexagone
    haut = np.pad(haut, ((4, 4), (4, 4), (0, 0)))
    creux = trous(haut[..., 3] < 25)
    haut[creux] = [255, 255, 255, 255]
    return Image.fromarray(haut.astype(np.uint8))


def icone(hexa, cote, part):
    """L'hexagone centré sur fond crème, sa plus grande dimension = part du côté."""
    fond = Image.new("RGBA", (cote, cote), CREME)
    echelle = cote * part / max(hexa.size)
    h = hexa.resize((round(hexa.width * echelle), round(hexa.height * echelle)), Image.LANCZOS)
    fond.alpha_composite(h, ((cote - h.width) // 2, (cote - h.height) // 2))
    return fond.convert("RGB")


if __name__ == "__main__":
    hexa = hexagone(sys.argv[1])
    icone(hexa, 192, 0.84).save("icon-192.png", optimize=True)
    icone(hexa, 512, 0.84).save("icon-512.png", optimize=True)
    # icône adaptable Android : tout doit tenir dans le cercle central de 80 %
    icone(hexa, 512, 0.58).save("icon-maskable-512.png", optimize=True)
    entete = hexa.resize((round(hexa.width * 144 / hexa.height), 144), Image.LANCZOS)
    entete.save("logo-hexagone.png", optimize=True)
    print("hexagone source", hexa.size, "-> icon-192, icon-512, icon-maskable-512, logo-hexagone",
          entete.size)
