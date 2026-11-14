# Sujet 7 - Sélection d'actions sous budget

## Objectif
(1-2 phrases : ce que le programme calcule)

## Lancer le projet
    pip install matplotlib
    python selection.py

## Décisions
- Pourquoi `itertools.product` (toutes les sélections 0/1)
- Pourquoi un `set` pour les prérequis
- Pourquoi la clé (gain, -coût) pour départager

## Contraintes respectées
- Budget, prérequis, bénéfices positifs ou nuls

## Résultat de référence
Budget 10 : C, D, F, coût 9, bénéfice 15

## Limites
- Complexité O(n × 2^n), environ 15 actions maximum
- Bénéfices fictifs et additifs, aucun calendrier d'exécution