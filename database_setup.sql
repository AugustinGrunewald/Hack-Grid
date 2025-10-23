-- Hackgrid Database Setup
-- Run this script to create the necessary tables for the ETL pipeline
CREATE DATABSE prices_consumption_db;
-- Drop tables if they exist (for clean restart)
DROP TABLE IF EXISTS prices_consumption;

-- First table - consumption
CREATE TABLE prices_consumption (
    id SERIAL PRIMARY KEY,
    date_actual DATE,
    hour_actual TIME,  
    spot_price DECIMAL(4,2), -- Precision in cents 
    consumption DECIMAL(10,6), -- Value in Wh

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_prices_consumption ON prices_consumption_db(date_actual);

-- Verify tables were created
\dt

SELECT 'Database setup complete!' as status;