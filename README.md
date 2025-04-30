# SOKOBAN

## Description du projet

SOKOBAN est une implémentation du célèbre jeu de puzzle Sokoban, développé en Python. Le joueur contrôle un personnage qui doit pousser des objets (représentés par des gâteaux dans ce projet) vers des cibles spécifiques. L'objectif est de déplacer tous les objets vers leurs positions cibles tout en évitant de les bloquer contre les murs ou entre eux.

Ce projet propose une interface graphique intuitive réalisée avec Python et utilisant des images SVG pour une représentation claire et esthétique des éléments du jeu (personnages, murs, objets à déplacer).

## Fonctionnalités principales

- Interface graphique simple et intuitive.
- Différents niveaux jouables stockés dans un fichier spécifique.
- Mode joueur unique et mode comparaison (joueur vs bot).
- Intégration d'un solveur automatique pour résoudre les niveaux.

## Structure du projet

- `main.py` : Script principal pour exécuter le jeu.
- `menu.py` : Gestion du menu interactif.
- `solver.py` : Implémentation de l'algorithme de résolution automatique.
- `grid_utils.py` : Fonctions utilitaires pour gérer les grilles du jeu.
- `levels` : Fichier contenant les niveaux prédéfinis.
- `music` : Dossier avec les effets sonores et musiques de fond.
- Images SVG utilisées pour la représentation graphique (`oven.svg`, `black-forest.svg`, `open-mouth.svg`, `wall.svg`).

## Prérequis

- Python 3.x
- Modules Python requis (`pygame`, autres dans `requirements.txt` si disponible)

## Installation

Clonez le dépôt :

```bash
git clone https://github.com/yassineelaa/SOKOBAN.git
cd SOKOBAN
```

Installez les éventuelles dépendances (si un fichier requirements.txt est fourni) :

```bash
pip install -r requirements.txt
```

Si pygame n'est pas inclus :

```bash
pip install pygame
```

## Utilisation

Pour lancer le jeu, exécutez simplement :

```bash
python3 start.py
```

Un menu interactif apparaîtra et vous permettra de sélectionner le mode de jeu (Joueur unique, Joueur vs Bot).

### Commandes du jeu

| Action                   | Touche clavier |            |
| ------------------------ | -------------- | ---------- |
| Déplacements             | Flèches        |            |
| Réinitialiser le niveau  |                | **Escape** |
| Solveur automatique      | **S**          |            |
| Solveur enregistré       | **=**          |            |
| Enregistrer une solution | **R**          |            |
| Entrer des déplacements  | **I**          |            |
| Démarrer un combat       | **F**          |            |

Editez ces paramètres dans le fichier `config.yaml` pour les personnaliser.

## Captures d'écran

Des captures d'écran sont disponibles dans le dossier du projet (`screen.png`).


## Licence

Ce projet est disponible sous la licence MIT. Pour plus de détails, consultez le fichier `LICENSE` s'il existe, ou ajoutez-le selon votre choix.

## Ressources supplémentaires

Pour plus d'informations sur Sokoban et les techniques de résolution :

- [Sokoban Wikipedia](https://en.wikipedia.org/wiki/Sokoban)

Amusez-vous bien ! 🚀🧩

