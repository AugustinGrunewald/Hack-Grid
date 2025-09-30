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



if __name__ == "__main__":
    
    # Test fonction réelle (échouera sans API key)
    result = extract_prices("202401150000", "202401160000")
    print(f"API test: {'OK' if not result.empty else 'Échec (normal sans clé API)'}")
        