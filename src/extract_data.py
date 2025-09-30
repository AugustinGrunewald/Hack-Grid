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
    
    date_end = datetime.today().date()
    date_start = date_end - timedelta(days=31)
    # format ISO pour la requête
    start_str = date_start.isoformat()
    end_str = date_end.isoformat()

    
    # URL de base de l'API
    base_url = "https://data.enedis.fr/api/explore/v2.1/catalog/datasets/conso-inf36-region/records"
    params = {
        "dataset": "conso-inf36-region",
        "where": f"date >= '{start_str}' AND date <= '{end_str}'",
        "rows": 1000  # nombre de résultats max (à ajuster)
    }
    
    try:
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {resp.text}")
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    
    # extraire les valeurs de consommation dans les "records"
    valeurs = []
    records = data.get("records", [])
    print(f"Found {len(records)} records")
    
    if not records:
        print("No records found in API response")
        return None
    
    # Debug: print the first record to understand the structure
    if records:
        print("Sample record structure:")
        print(records[0])
    
    for rec in records:
        fields = rec.get("fields", {})
        # Chercher différents champs possibles pour la consommation
        consumption_fields = ["conso", "volume", "consommation", "value", "valeur"]
        found_value = None
        
        for field in consumption_fields:
            if field in fields:
                found_value = fields[field]
                break
        
        if found_value is not None:
            try:
                # Convertir en float si possible
                valeur = float(found_value)
                valeurs.append(valeur)
            except (ValueError, TypeError):
                print(f"Could not convert value to float: {found_value}")
                continue
    
    if not valeurs:
        print("No valid consumption values found")
        return None
    
    # moyenne
    moyenne = sum(valeurs) / len(valeurs)
    print(f"Calculated average from {len(valeurs)} values: {moyenne:.2f}")
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
        