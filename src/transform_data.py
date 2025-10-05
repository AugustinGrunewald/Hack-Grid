import pandas as pd
import os
import matplotlib.pyplot as plt

def fusionner_prix_conso(prix_path, conso_path):
	# Charger les CSV avec parsing des dates (on assigne le type date-time au champ)
	df_conso = pd.read_csv(
		conso_path,
		sep=";",
		parse_dates=["Time"],
		date_parser=lambda x: pd.to_datetime(x, format="%d/%m/%Y %H:%M:%S")
		# On s'assure que le type de date sera compatible avec le prochain df
	)	
	
	df_prix = pd.read_csv(prix_path, parse_dates=['time'])
	df_prix["time"] = df_prix["time"].dt.tz_localize(None) #On enlève le fuseau horaire 
	#On fait un inner join sur la colonne date
	df = pd.merge(df_prix, df_conso, left_on='time', right_on='Time')
	df = df[["time", "spot_price", "Consumption (W)"]]
	df.columns = ["Date Hour", "Spot Prices (EUR)", "Consumption (W)"]
	#On peut renvoyer le df une fois qu'on a selectionné et renommé les bonnes colonnes
	return df

if __name__ == "__main__":
	# Exemple d'utilisation
	data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
	prix_path = os.path.join(data_folder, 'spot_prices_september_2025.csv')
	conso_path = os.path.join(data_folder, 'conso_september_2025.csv')
	df = fusionner_prix_conso(prix_path, conso_path)
	print(df)
