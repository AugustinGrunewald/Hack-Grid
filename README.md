# Hack-Grid

## Description
Ce projet est une pipeline ETL (Extract, Transform, Load) implémentée en Python. La pipeline suit les étapes suivantes :

- Extraction des données via ##A COMPLETER##,
- Transforme les données pour ##A COMPLETER##
- Load les données sur une base de données SQL puis rend compte d'une analyse et optimisation via PowerBI

Ce projet est une démo de notre Proof-of-Concept.

## Structure du projet
Voici la structure des fichiers du projet:
```bash
demo/
│
├── data/                           # Data directory
│   ├── conso_septembre_2025.csv              # Fichier temporaire pour l'extraction des données de consommation utilisateur
│   ├── spot_prices_septembre_2025.csv              # Fichier temporaire pour l'extraction des données de prix spot
│
├── src/
│   ├── extract.py                  # Code for extracting data
│   ├── transform.py                # Code for transforming data
│   └── load.py                     # Code for loading data
│
├── README.md                       # Documentation du projet
├── requirements.txt                # Liste des dépendances Python
└── main.py                         # Point d'entrée pour la pipeline ETL
```
## Setup d'installation
#### Create PostgreSQL database
   ```bash
   # Connect to PostgreSQL
   psql -U your_username -d postgres
   
   # Create database
   CREATE DATABASE prices_consumption_db;
   
   # Exit and reconnect to new database
   \q
   psql -U your_username -d prices_consumption_db
   
   # Create tables
   \i database_setup.sql
   ```
