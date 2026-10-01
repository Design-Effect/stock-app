# Stock

Application web installable (PWA) pour tenir un inventaire de produits : recherche, quantités avec + et −, prix, marques, photos, ventes du jour et export. Elle fonctionne hors connexion une fois ouverte une première fois.

Les données restent sur l'appareil (stockage du navigateur). L'application n'envoie rien sur Internet.

## Installation sur téléphone

1. Ouvrir l'adresse de l'application dans Chrome (Android) ou Safari (iPhone).
2. Android : menu ⋮ puis « Installer l'application ». iPhone : bouton Partager puis « Sur l'écran d'accueil ».
3. L'icône apparaît comme une application ordinaire.

## Sauvegarde

Menu ☰ puis « Sauvegarde complète (JSON) » : à faire régulièrement, et à garder dans un endroit sûr (Drive, mail, messagerie). Pour retrouver ses données sur un autre téléphone : menu ☰ puis « Restaurer une sauvegarde ».

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html`, `app.js` | interface et logique |
| `data.js`, `photos.js`, `img/` | produits de départ et leurs photos |
| `sw.js`, `manifest.webmanifest`, `icon-*.png` | mode hors connexion et installation |
| `robots.txt` | demande aux moteurs de recherche de ne pas indexer |
