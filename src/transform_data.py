import pandas as pd
import os


def fusionner_prix_conso(prix_path, conso_path):
	# Charger les CSV avec parsing des dates
	df_prix = pd.read_csv(prix_path, parse_dates=['time'])
	df_conso = pd.read_csv(conso_path, parse_dates=['temps'])

	# Fusionner sur les colonnes de temps
	df = pd.merge(df_prix, df_conso, left_on='time', right_on='temps')
	# Supprimer la colonne 'temps'
	df = df.drop(columns=['temps'])
	return df

if __name__ == "__main__":
	# Exemple d'utilisation
	data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
	prix_path = os.path.join(data_folder, 'day_ahead_prices_example.csv')
	conso_path = os.path.join(data_folder, 'consommation_electricite_deux_jours.csv')
	df_fusion = fusionner_prix_conso(prix_path, conso_path)
	print(df_fusion)

