import pandas as pd
import os

def calcul_prix_client(prix_path, conso_path):
	# Charger les CSV
	df_prix = pd.read_csv(prix_path)
	df_conso = pd.read_csv(conso_path)

	# On suppose que les deux CSV ont une colonne 'heure' pour la jointure
	df = pd.merge(df_prix, df_conso, on='jour-heure')
	# Colonnes attendues: 'heure', 'prix' (euro/Kwh), 'conso' (Kwh)

	# Prix réel payé
	prix_total = (df['prix'] * df['conso']).sum()

	# Prix si tarif minimum toute la journée
	prix_min = df['prix'].min() * df['conso'].sum()

	return prix_total, prix_min

if __name__ == "__main__":
	# Exemple d'utilisation
	data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
	prix_path = os.path.join(data_folder, 'prix.csv')
	conso_path = os.path.join(data_folder, 'conso.csv')
	prix_total, prix_min = calcul_prix_client(prix_path, conso_path)
	print(f"Prix réel payé: {prix_total:.2f} €")
	print(f"Prix au tarif minimum: {prix_min:.2f} €")
