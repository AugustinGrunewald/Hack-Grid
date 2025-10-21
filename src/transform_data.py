import pandas as pd
import os
import matplotlib.pyplot as plt

def clean_spot_prices(df_prix):
    # On remplace les valeurs NaN par la dernière valeur connue
    df_prix['spot_price'] = df_prix['spot_price'].ffill()	
    # On convertit tout en UTC +02, dans le format compatible avec les consos
    df_prix['time'] = pd.to_datetime(df_prix['time'], utc=True)    
    df_prix = df_prix.drop_duplicates(keep='first')
    df_prix['time'] = df_prix['time'] + pd.Timedelta(hours=2)
    return df_prix


def fusionner_prix_conso(prix_path, conso_path):
    # On charge les df:
    df_conso = pd.read_csv(
        conso_path,
        sep=";",
        parse_dates=["Time"],
        date_format="%d/%m/%Y %H:%M:%S" 
    )
    df_prix = pd.read_csv(prix_path, parse_dates=['time'])
    
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