import pandas as pd
import os
import matplotlib.pyplot as plt


def clean_spot_prices(df_prix):
    """Nettoie et met les prix dans le fuseau Europe/Paris"""
    df_prix['spot_price'] = df_prix['spot_price'].ffill()
    df_prix['time'] = pd.to_datetime(df_prix['time'], utc=True)
    df_prix['datetime'] = df_prix['time'].dt.tz_convert("Europe/Paris")
    return df_prix


def fusionner_prix_conso(prix_path, conso_path):
    # --- Chargement consommation ---
    df_conso = pd.read_csv(
        conso_path,
        sep=";",
        parse_dates=["Time"],
        dayfirst=True
    )
    df_conso.rename(columns={"Time": "datetime"}, inplace=True)
    df_conso["datetime"] = df_conso["datetime"].dt.tz_localize(
        "Europe/Paris", ambiguous="infer", nonexistent="shift_forward"
    )
    
    # Si le nom de la colonne conso diffère (ex: "Consumption (W)" ou "conso")
    conso_col = [c for c in df_conso.columns if "conso" in c.lower() or "consumption" in c.lower()][0]
    df_conso.rename(columns={conso_col: "Consumption (W)"}, inplace=True)
    
    # Ajoute jour et heure pour la jointure
    df_conso["day"] = df_conso["datetime"].dt.day
    df_conso["hour"] = df_conso["datetime"].dt.hour

    # --- Chargement prix ---
    df_prix = pd.read_csv(prix_path, parse_dates=["time"])
    df_prix = clean_spot_prices(df_prix)
    df_prix["day"] = df_prix["datetime"].dt.day
    df_prix["hour"] = df_prix["datetime"].dt.hour

    # --- Fusion (sur jour + heure) ---
    df_merged = pd.merge(
        df_prix,
        df_conso[["day", "hour", "Consumption (W)"]],
        on=["day", "hour"],
        how="left"
    )

    # --- Nettoyage final ---
    df_final = df_merged[["datetime", "spot_price", "Consumption (W)"]]
    df_final.columns = ["Date Hour", "Spot Prices (EUR)", "Consumption (W)"]

    return df_final

def fusionner_prix_conso_df(df_prix, df_conso):
    
    #On fait un premier traitement des prix
    df_prix = clean_spot_prices(df_prix)

    #La clé de jointure sera le jour et l'heure, mais sans le mois car on a pas la data conso
    df_prix['JoinKey'] = df_prix['time'].dt.strftime('%d-%H')

    # Gestion spéciale pour le jour 31 (remplacer par jour 30)
    is_day_31 = df_prix['time'].dt.day == 31
    if is_day_31.any():
        # Remplace '31-HH' par '30-HH' pour les lignes concernées
        df_prix.loc[is_day_31, 'JoinKey'] = df_prix['time'].dt.strftime('30-%H')
        

    # Créer une clé unique 'Jour_Heure' pour DF_CONSO
    df_conso['JoinKey'] = df_conso['Time'].dt.strftime('%d-%H')
    
    
    # Fusion des DataFrames sur la clé Jour-Heure
    df = pd.merge(
        df_prix, 
        df_conso[['JoinKey', 'Consumption (W)']], # Seules les colonnes nécessaires de conso
        on='JoinKey', 
        how='left'
    )
    
    # Nettoyage final des colonnes
    df = df[["time", "spot_price", "Consumption (W)"]]
    df.columns = ["Date Hour", "Spot Prices (EUR)", "Consumption (W)"]
    df = df.drop_duplicates(keep='first')
    return df

if __name__ == "__main__":
    # Exemple d'utilisation
    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    prix_path = os.path.join(data_folder, 'spot_prices_year.csv') # Utilise ton fichier annuel
    conso_path = os.path.join(data_folder, 'conso_september_2025.csv')
    df = fusionner_prix_conso(prix_path, conso_path)
    print(df)