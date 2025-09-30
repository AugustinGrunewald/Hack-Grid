import requests
import pandas as pd
import xmltodict
from datetime import datetime, timedelta

def extract_prices(periodStart, periodEnd):
    print("Fetching live prices data from ENTSO-E API...")
    in_Domain = "10YFR-RTE------C"
    out_Domain = "10YFR-RTE------C"
    url = (
        f"https://web-api.tp.entsoe.eu/api?"
        f"documentType=A44&periodStart={periodStart}&periodEnd={periodEnd}"
        f"&out_Domain={out_Domain}&in_Domain={in_Domain}"
        f"&securityToken=YOUR_API_KEY"
    )
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f":danger: API returned status code {response.status_code}")
            return pd.DataFrame()
        # Convertir XML -> dict
        data = xmltodict.parse(response.content)
        # Naviguer dans la structure
        period = data["Publication_MarketDocument"]["TimeSeries"]["Period"]
        start_time = datetime.fromisoformat(period["timeInterval"]["start"].replace("Z", "+00:00"))
        resolution = period["resolution"]  # ex "PT15M"
        step = int(resolution.replace("PT", "").replace("M", ""))
        # Extraire les points
        points = period["Point"]
        if isinstance(points, dict):  # cas 1 seul point
            points = [points]
        times, prices = [], []
        for p in points:
            pos = int(p["position"])
            price = float(p["price.amount"])
            timestamp = start_time + timedelta(minutes=(pos - 1) * step)
            times.append(timestamp)
            prices.append(price)
        df = pd.DataFrame({"time": times, "price": prices})
        print(f":coche_blanche: Extracted {len(df)} price points")
        return df
    except Exception as e:
        print(f":x: Error processing price data: {e}")
        return pd.DataFrame()

def get_conso_in_31_jours():
    # date de début il y a 31 jours
    date_end = datetime.today().date()
    date_start = date_end - timedelta(days=31)
    # format ISO pour la requête
    start_str = date_start.isoformat()
    end_str = date_end.isoformat()
    
    # URL de base de l’API
    base_url = "https://data.enedis.fr/api/records/1.0/search/"
    base_url = "https://data.enedis.fr/api/explore/v2.1/catalog/datasets/conso-inf36-region/records"
    params = {
        "dataset": "conso-inf36-region",
        "q": "",  # pas de filtre général
        # on filtre sur le champ de date (nom hypothétique “date”) ; à ajuster selon la vraie structure
        "where": f"date >= '{start_str}' AND date <= '{end_str}'",
        "rows": 1000  # nombre de résultats max (à ajuster)
    }
    
    resp = requests.get(base_url, params=params)
    resp.raise_for_status()
    data = resp.json()
    
    # extraire les valeurs de consommation dans les “records”
    valeurs = []
    for rec in data.get("records", []):
        fields = rec.get("fields", {})
        # supposons que le champ de consommation s’appelle “conso” ou “volume” — à adapter
        if "conso" in fields:
            valeurs.append(fields["conso"])
        elif "volume" in fields:
            valeurs.append(fields["volume"])
    
    if not valeurs:
        return None
    
    # moyenne
    moyenne = sum(valeurs) / len(valeurs)
    return moyenne


if __name__ == "__main__":

    print("deuxième fonction")

    moyenne = get_conso_in_31_jours()
    if moyenne is None:
        print("Aucune donnée récupérée.")
    else:
        print(f"Consommation moyenne sur les 31 derniers jours : {moyenne:.2f}")
    
    print("première fonction")

    result = extract_prices("202401150000", "202401160000")
    print(f"API test: {'OK' if not result.empty else 'Échec (normal sans clé API)'}")
        