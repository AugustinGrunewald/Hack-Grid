#!/usr/bin/env python3
"""
AirLife ETL Pipeline - Simple Version

This script runs the complete ETL pipeline:
1. Extract airport data from CSV and flight data from API
2. Clean and transform the data
3. Load the data into PostgreSQL database

Run with: python main.py
"""
token = 'b21fd0b5-a6b2-45b4-add3-70bb610259c5'
PeriodStart = '202412230000'
PeriodEnd = '202508152300'

from src.extract_data import extract_prices_concatenate
from src.transform_data_2 import fusionner_prix_conso
from src.load_data_2 import load_to_database
import os


def main():
    """Run the complete ETL pipeline"""
    print("🛫 Starting AirLife ETL Pipeline...")
    print("=" * 50)
    
    # Step 1: Extract data
    print("\n=== EXTRACTION ===")
    print("📥 Extracting data from sources...")
    
    # TODO: Call the extraction functions
    prices = extract_prices_concatenate(PeriodStart, PeriodEnd, token, 'Europe/Paris')
    # nous n'extrayons finalement que les prix SPOT
    
    # Uncomment the lines above once you've implemented the functions
    # print("⚠️  Extraction functions not yet implemented")
    
    # Step 2: Transform data
    print("\n=== TRANSFORMATION ===")
    print("🔄 Cleaning and transforming data...")
    
    # TODO: Call the transformation functions
    # clean_airports_data = clean_airports(airports)
    # clean_flights_data = clean_flights(flights)
    # final_airports, final_flights = combine_data(clean_airports_data, clean_flights_data)
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    fusionned_table = fusionner_prix_conso(os.path.join(data_folder, f'SPOT_prices_{PeriodStart}_{PeriodEnd}.csv'),conso_path = os.path.join(data_folder, 'conso_september_2025.csv'))
    
    # Step 3: Load data
    print("\n=== LOADING ===")
    print("💾 Loading data to database...")
    
    # TODO: Call the loading function
    load_to_database(prices_consumption_df=fusionned_table)
    
    # Step 4: Verify everything worked
    print("\n=== VERIFICATION ===")
    print("✅ Verifying data was loaded correctly...")
    
    # TODO: Call the verification function
    # verify_data()
    
    print("\n🎉 ETL Pipeline completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
