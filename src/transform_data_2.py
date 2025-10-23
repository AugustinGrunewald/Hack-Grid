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



if __name__ == "__main__":
    # Exemple d'utilisation
    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    prix_path = os.path.join(data_folder, 'spot_prices_year.csv') # Utilise ton fichier annuel
    conso_path = os.path.join(data_folder, 'conso_september_2025.csv')
    df = fusionner_prix_conso(prix_path, conso_path)
    print(df)