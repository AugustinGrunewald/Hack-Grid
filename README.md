# Hack-Grid
ETL project - Ce ReadMe 

## Résumé de la startup
... à compléter ...

## Description de l'ETL
#### Step 1 - Extract
Récupérer les données de consommation -> data d'entreprises/particuliers 
Récupérer les prix du marchés

#### Step 2 - Transform
Nettoyer les données
Une transformation -> on trouve le prix de consommation sans optimisation (prix payé sur une journée)
Mettre en place l'optimisation -> prix de la batterie, achat de l'électricité à différent moment, comparer les prix pour une même quantité consommée

#### Step 3 - Load
Faire une BD -> chaque ligne correspond à un jour contenant le prix optimisé et non optimisé
