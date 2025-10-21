"""
Data Loading Module

This module handles loading cleaned data into PostgreSQL database:
- Load optimized/non optimized price and consumption data for each day
- Verify data was loaded correctly
"""
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2
import os
# from transform_data import fusionner_prix_conso
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

# connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Database connection configuration
# DATABASE_CONFIG = {
#     'username': 'grunewaldaugustin',
#     'password': '', 
#     'host': 'localhost',
#     'port': '5432',
#     'database': 'prices_consumption_db'
# }


def get_connection_string():
    """
    Build PostgreSQL connection string
    """
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def load_to_database(prices_consumption_df):
    """
    Load cleaned data into PostgreSQL database
    
    Args:
        prices_consumption_df (pandas.DataFrame): Cleaned prices (optimized & non optimized) and consumption (kWh) data 
    """
    print(" Loading data to PostgreSQL database...")
    
    # Create connection string using the function above
    connection_string = get_connection_string()
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(connection_string)
            
        # Use pandas to_sql method to insert data
        if not prices_consumption_df.empty:
            prices_consumption_df.to_sql('prices_consumption', engine, if_exists='replace', index=False)
            print(f"Loaded {len(prices_consumption_df)} days of data to database")
         
        # Parameters explanation:
        # - 'prices&consumption': table name in database
        # - engine: database connection
        # - if_exists='replace': replace table if it exists (use 'append' to add to existing data)
        # - index=False: don't include pandas row index as a column
        
        else:
            print("No prices & consumption data to load")

        
    except Exception as e:
        print(f"Error loading data to database: {e}")
        print("Make sure:")
        print("   - PostgreSQL is running")
        print("   - Database 'prices_consumption_db' exists") 
        print("   - Username and password are correct")
        print("   - Tables are created (run database_setup.sql)")


if __name__ == "__main__":
    """Test the loading functions"""
    print("Testing database loading functions...\n")

    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    prix_path = os.path.join(data_folder, 'spot_prices_september_2025.csv')
    conso_path = os.path.join(data_folder, 'conso_type.csv')

    # load_to_database(fusionner_prix_conso(prix_path, conso_path))