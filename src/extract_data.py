import requests
import pandas as pd
import xmltodict
from datetime import datetime, timedelta
import pytz

token = 'b21fd0b5-a6b2-45b4-add3-70bb610259c5'
timezone = 'Europe/Paris'


def extract_prices_concatenate(periodStart, periodEnd, token, timezone):
    # Convert strings en datetime
    start = datetime.strptime(periodStart, "%Y%m%d%H%M")
    end   = datetime.strptime(periodEnd, "%Y%m%d%H%M")
    
    list_of_df = []
    current_start = start
    
    while current_start < end:
        # On peut demander au max 1 mois à la fois pour simplifier
        # Calcul de la fin du mois ou fin de la période
        next_month = (current_start.replace(day=1) + timedelta(days=32)).replace(day=1)
        current_end = min(next_month, end)
        
        # Format ENTSO-E YYYYMMDDHHMM
        start_str = current_start.strftime("%Y%m%d%H%M")
        end_str   = current_end.strftime("%Y%m%d%H%M")
        
        # Appel à ta fonction extract_prices
        df = extract_prices(start_str, end_str, token, timezone)
        list_of_df.append(df)
        
        # Avancer au prochain intervalle
        current_start = current_end
    
    # Concaténer tous les DataFrames
    df_concat = pd.concat(list_of_df, ignore_index=False)
    df_to_csv(df_concat,output_path="./data", start=periodStart, end=periodEnd)
    return df_concat



def extract_prices(periodStart, periodEnd, token, timezone):
    start = datetime.strptime(periodStart, "%Y%m%d%H%M")
    month = start.month
    print(f"Fetching live prices data from ENTSO-E API for the month {month}")
    true_periodEnd = periodEnd.replace('2300','2200') # pour contourner le problème de l'API ENTSOE
    in_Domain = "10YFR-RTE------C"
    out_Domain = "10YFR-RTE------C"
    url = (
        f"https://web-api.tp.entsoe.eu/api?securityToken={token}"
        f"&documentType=A44&processType=A01"
        f"&out_Domain={out_Domain}&in_Domain={in_Domain}&periodStart={periodStart}&periodEnd={true_periodEnd}"
    )
    try:
        response = requests.get(url=url,
                headers={'Content-Type': 'application/xml', 'SECURITY_TOKEN': token},
                verify=True)
        if response.status_code != 200:
            print(f":danger: API returned status code {response.status_code}")
            return pd.DataFrame()
        # Convertir XML -> dict
        r_json = xmltodict.parse(response.content)

        time_series = r_json['Publication_MarketDocument']['TimeSeries']
        list_of_df =[]
        for series in time_series:
            start_date = utc_to_local(series['Period']['timeInterval']['start'], timezone)
            # start_date = series['Period']['timeInterval']['start']
            # dt1 = datetime.fromisoformat(start_date.replace("Z", "+02:00"))
            end_date = utc_to_local(series['Period']['timeInterval']['end'], timezone)
            # end_date = series['Period']['timeInterval']['end']
            # dt2 = datetime.fromisoformat(end_date.replace("Z", "+02:00"))
            currency = series["currency_Unit.name"]

            dt = pd.date_range(
                start=start_date,
                end=end_date - timedelta(minutes=60),
                freq=f'{60}min'
                )
            # print(dt[0],dt[len(dt)-1])    
            prices_col = [float('nan')] * len(dt)

            for val in series['Period']['Point']:
                xml_pos = int(val['position'])
                price = float(val['price.amount'])
                prices_col[xml_pos-1] = price
            df_c = pd.DataFrame({
                f'spot_price': prices_col,
                f'currency_unit': [currency] * len(prices_col)
            }, index=pd.Index(dt, name='time'))
            list_of_df.append(df_c)
        df_total = pd.concat(df_c for df_c in list_of_df)
        return df_total
        # df_to_csv(df=df_total, output_path="./data", start=periodStart, end=periodEnd)
    # if not isinstance(time_series, list):
    #     time_series = [time_series]
    #     for val in series['Period']['Point']:
    #         xml_pos = int(val['position'])
    #     # Naviguer dans la structure
    #     period = data["Publication_MarketDocument"]["TimeSeries"]["Period"]
    #     start_time = datetime.fromisoformat(period["timeInterval"]["start"].replace("Z", "+00:00"))
    #     resolution = period["resolution"]  # ex "PT15M"
    #     step = int(resolution.replace("PT", "").replace("M", ""))
    #     # Extraire les points
    #     points = period["Point"]
    #     if isinstance(points, dict):  # cas 1 seul point
    #         points = [points]
    #     times, prices = [], []
    #     for p in points:
    #         pos = int(p["position"])
    #         price = float(p["price.amount"])
    #         timestamp = start_time + timedelta(minutes=(pos - 1) * step)
    #         times.append(timestamp)
    #         prices.append(price)
    #     df = pd.DataFrame({"time": times, "price": prices})
    #     print(f":coche_blanche: Extracted {len(df)} price points")
    except Exception as e:
        print(f":x: Error processing price data: {e}")

def utc_to_local(utc_date_str, timezone):
    """
    Convertit une date UTC string ISO en datetime localisé (timezone donnée).
    """
    tz = pytz.timezone(timezone)
    utc_dt = datetime.strptime(utc_date_str, '%Y-%m-%dT%H:%MZ').replace(tzinfo=pytz.utc)
    # print(type(utc_dt.astimezone(tz)))
    return utc_dt.astimezone(tz)


# def get_conso_in_31_jours():
    
#     date_end = datetime.today().date()
#     date_start = date_end - timedelta(days=31)
#     # format ISO pour la requête
#     start_str = date_start.isoformat()
#     end_str = date_end.isoformat()

    
#     # URL de base de l'API
#     base_url = "https://data.enedis.fr/api/explore/v2.1/catalog/datasets/conso-inf36-region/records"
#     params = {
#         "dataset": "conso-inf36-region",
#         "where": f"date >= '{start_str}' AND date <= '{end_str}'",
#         "rows": 1000  # nombre de résultats max (à ajuster)
#     }
    
#     try:
#         resp = requests.get(base_url, params=params)
#         resp.raise_for_status()
#         data = resp.json()
#     except requests.exceptions.HTTPError as e:
#         print(f"HTTP Error: {e}")
#         print(f"Response content: {resp.text}")
#         return None
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return None
    
#     # extraire les valeurs de consommation dans les "records"
#     valeurs = []
#     records = data.get("records", [])
#     print(f"Found {len(records)} records")
    
#     if not records:
#         print("No records found in API response")
#         return None
    
#     # Debug: print the first record to understand the structure
#     if records:
#         print("Sample record structure:")
#         print(records[0])
    
#     for rec in records:
#         fields = rec.get("fields", {})
#         # Chercher différents champs possibles pour la consommation
#         consumption_fields = ["conso", "volume", "consommation", "value", "valeur"]
#         found_value = None
        
#         for field in consumption_fields:
#             if field in fields:
#                 found_value = fields[field]
#                 break
        
#         if found_value is not None:
#             try:
#                 # Convertir en float si possible
#                 valeur = float(found_value)
#                 valeurs.append(valeur)
#             except (ValueError, TypeError):
#                 print(f"Could not convert value to float: {found_value}")
#                 continue
    
#     if not valeurs:
#         print("No valid consumption values found")
#         return None
    
#     # moyenne
#     moyenne = sum(valeurs) / len(valeurs)
#     print(f"Calculated average from {len(valeurs)} values: {moyenne:.2f}")
#     return moyenne

def df_to_csv(df, output_path, start, end):
    """
    Sauvegarde le DataFrame au format CSV.
    """
    name = f"SPOT_prices_{start}_{end}"
    filepath = f"{output_path}/{name}.csv"
    df.to_csv(filepath)
    print(f"[INFO] Fichier CSV enregistré : {filepath}")

if __name__ == "__main__":

    # print("deuxième fonction")

    # moyenne = get_conso_in_31_jours()
    # if moyenne is None:
    #     print("Aucune donnée récupérée.")
    # else:
    #     print(f"Consommation moyenne sur les 31 derniers jours : {moyenne:.2f}")
    
    print("première fonction")

    result = extract_prices_concatenate("202501100000", "202509152300", token, timezone)

    # print(f"API test: {'OK' if not result.empty else 'Échec'}")

        