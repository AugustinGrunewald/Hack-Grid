# Hack-Grid

## Description
Ce projet est une pipeline ETL (Extract, Transform, Load) implémentée en Python. La pipeline suit les étapes suivantes :

- Extraction des données via un fichier csv et une API,
- Transforme les données pour créer un dataframe avec 3 colonnes utilisable pour le loadd,
- Load les données sur une base de données SQL puis rend compte d'une analyse et optimisation via PowerBI

Ce projet est une démo de notre Proof-of-Concept.

## Structure du projet
Voici la structure des fichiers du projet:
```bash
demo/
│
├── data/                           # Data directory
│   ├── conso_septembre_2025.csv              # Fichier de consommation d'un proche du groupe à partir duquel on génère la consommation utilisateur
│   
├── src/
│   ├── extract.py                  # Code for extracting data
│   ├── transform.py                # Code for transforming data
│   └── load.py                     # Code for loading data
│
├── README.md                       # Documentation du projet
├── .env                            # Configuration des variables d'environnement pour la base SQL
├── .gitignore                       # Liste des fichiers que le git doit ignorer
├── database_setup.sql              # Fichier pour configurer la database SQL
├── requirements.txt                # Liste des dépendances Python
├── Hack-Grid.pbi                   # PowerBI démontrons l'optimisation
└── main.py                         # Point d'entrée pour la pipeline ETL
```
## Setup d'installation
   ```bash
   # Cloner le repo
   git clone git@github.com:AugustinGrunewald/Hack-Grid.git

   # Installer les packages nécessaires
   pip install -r requirements.txt
   
   # Connect to PostgreSQL
   psql -U your_username -d postgres
   
   # Create database
   CREATE DATABASE prices_consumption_db;
   
   # Exit and reconnect to new database
   \q
   psql -U your_username -d prices_consumption_db
   
   # Create tables
   \i database_setup.sql

   # Exécuter le main
   python main.py
   ```
