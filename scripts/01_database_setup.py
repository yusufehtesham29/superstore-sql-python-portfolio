"""
============================================================================
FILE: 01_database_setup.py
PURPOSE: Load CSV data into SQLite database
AUTHOR: yusufehtesham29
============================================================================
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

print("="*80)
print("SUPERSTORE DATABASE SETUP")
print("="*80)

# ============================================================================
# STEP 1: Load CSV File
# ============================================================================
print("\n[1] Loading CSV file...")

csv_path = 'data/Sample - Superstore.csv'

# Check if file exists
if not os.path.exists(csv_path):
    print(f"❌ Error: File not found at {csv_path}")
    print("Please ensure the CSV file is in the data/ folder")
    exit(1)

# Read CSV file
df = pd.read_csv(csv_path, encoding='latin-1')
print(f"✅ CSV loaded successfully!")
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")

# ============================================================================
# STEP 2: Data Inspection and Cleaning
# ============================================================================
print("\n[2] Inspecting data...")

# Show column names
print(f"\nColumns in dataset:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")

# Check for missing values
missing_counts = df.isnull().sum()
if missing_counts.sum() > 0:
    print(f"\n⚠️  Missing values found:")
    for col, count in missing_counts[missing_counts > 0].items():
        print(f"   {col}: {count}")
else:
    print(f"\n✅ No missing values found")

# ============================================================================
# STEP 3: Data Type Conversion and Validation
# ============================================================================
print("\n[3] Preparing data for database...")

# Convert date columns to proper datetime format
# The CSV might have different date formats, so we handle that
if 'Order Date' in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
    
if 'Ship Date' in df.columns:
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=False)

# Standardize column names (remove spaces, lowercase)
# This makes SQL queries easier
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')

print(f"✅ Data prepared!")
print(f"\nStandardized column names:")
for col in df.columns:
    print(f"   - {col}")

# ============================================================================
# STEP 4: Create SQLite Database Connection
# ============================================================================
print("\n[4] Creating database connection...")

# Create database folder if it doesn't exist
os.makedirs('database', exist_ok=True)

# Connect to SQLite database (creates file if doesn't exist)
db_path = 'database/superstore.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"✅ Connected to database: {db_path}")

# ============================================================================
# STEP 5: Create Table Schema
# ============================================================================
print("\n[5] Creating table schema...")

# Read and execute the CREATE TABLE SQL script
with open('sql_queries/01_create_table.sql', 'r') as f:
    create_table_sql = f.read()

# Execute the SQL (split by semicolon in case of multiple statements)
for statement in create_table_sql.split(';'):
    if statement.strip():
        cursor.execute(statement)

conn.commit()
print(f"✅ Table 'superstore' created successfully!")

# ============================================================================
# STEP 6: Insert Data into Database
# ============================================================================
print("\n[6] Inserting data into database...")
print(f"   This may take a moment...")

# Insert DataFrame into SQLite table
# if_exists='replace' will drop and recreate the table
df.to_sql('superstore', conn, if_exists='replace', index=False)

print(f"✅ Data inserted successfully!")
print(f"   {len(df):,} rows inserted")

# ============================================================================
# STEP 7: Verify Data
# ============================================================================
print("\n[7] Verifying database...")

# Count rows in database
cursor.execute("SELECT COUNT(*) FROM superstore")
row_count = cursor.fetchone()[0]
print(f"   Total rows in database: {row_count:,}")

# Show sample data
cursor.execute("SELECT * FROM superstore LIMIT 3")
sample_rows = cursor.fetchall()
print(f"\n   Sample data (first 3 rows):")
print(f"   {sample_rows[0][:5]}...")  # Show first 5 columns only

# Get table info
cursor.execute("PRAGMA table_info(superstore)")
columns_info = cursor.fetchall()
print(f"\n   Table structure:")
print(f"   {'Column Name':<20} {'Data Type':<15}")
print(f"   {'-'*35}")
for col in columns_info:
    print(f"   {col[1]:<20} {col[2]:<15}")

# ============================================================================
# STEP 8: Create Indexes for Performance
# ============================================================================
print("\n[8] Creating indexes for better query performance...")

indexes = [
    "CREATE INDEX IF NOT EXISTS idx_order_date ON superstore(order_date)",
    "CREATE INDEX IF NOT EXISTS idx_customer_id ON superstore(customer_id)",
    "CREATE INDEX IF NOT EXISTS idx_category ON superstore(category)",
    "CREATE INDEX IF NOT EXISTS idx_region ON superstore(region)",
    "CREATE INDEX IF NOT EXISTS idx_product_id ON superstore(product_id)"
]

for idx_sql in indexes:
    cursor.execute(idx_sql)
    
conn.commit()
print(f"✅ Indexes created successfully!")

# ============================================================================
# STEP 9: Cleanup and Close
# ============================================================================
conn.close()
print("\n[9] Database connection closed")

print("\n" + "="*80)
print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
print("="*80)
print(f"\n📊 Summary:")
print(f"   Database file: {db_path}")
print(f"   Table name: superstore")
print(f"   Total records: {row_count:,}")
print(f"   Columns: {len(df.columns)}")
print(f"\n✅ You can now run SQL queries against the database!")
print(f"✅ Next step: Run SQL analysis queries (02_sql_analysis.py)")
