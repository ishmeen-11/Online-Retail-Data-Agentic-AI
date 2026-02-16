#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import sys
import zipfile
import io
import requests

# Configuration
DATABASE_NAME = 'online_retail1'
USERNAME = 'surendarsinghgarewal'  # Change to your username
TABLE_NAME = 'transactions'
DATA_URL = 'https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip'

# Sheet names in the Excel file
SHEET_NAMES = ['Year 2009-2010', 'Year 2010-2011']

def print_header(text):
    """Print formatted section header"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)

def download_data():
    """Download and read BOTH sheets from Online Retail II Excel file"""
    print("\n📥 Step 1: Downloading Online Retail II dataset...")
    
    try:
        # Download the ZIP file
        print("   Downloading ZIP file from UCI...")
        response = requests.get(DATA_URL, timeout=60)
        response.raise_for_status()
        
        # Open ZIP file
        z = zipfile.ZipFile(io.BytesIO(response.content))
        
        # List all files in ZIP
        all_files = z.namelist()
        print(f"   Files in ZIP: {all_files}")
        
        # Find the Excel file
        excel_files = [f for f in all_files if f.endswith('.xlsx')]
        
        if len(excel_files) == 0:
            raise Exception("No Excel files found in ZIP!")
        
        # Use the first Excel file found
        excel_file = excel_files[0]
        print(f"\n   📊 Reading Excel file: {excel_file}")
        
        # Read BOTH sheets from the same Excel file
        dfs = []
        for sheet_name in SHEET_NAMES:
            print(f"\n   📄 Reading sheet: '{sheet_name}'")
            try:
                df_temp = pd.read_excel(z.open(excel_file), sheet_name=sheet_name)
                print(f"      Rows: {len(df_temp):,}")
                print(f"      Columns: {list(df_temp.columns)}")
                dfs.append(df_temp)
            except Exception as e:
                print(f"      ⚠️  Error reading sheet '{sheet_name}': {e}")
                print(f"      Available sheets might be different. Trying to list them...")
                
                # Try to read all sheets to see what's available
                xl_file = pd.ExcelFile(z.open(excel_file))
                print(f"      Available sheets: {xl_file.sheet_names}")
                raise
        
        # Combine both sheets
        print(f"\n   🔗 Combining {len(dfs)} sheets...")
        df = pd.concat(dfs, ignore_index=True)
        
        print(f"✅ Total rows after combining both sheets: {len(df):,}")
        print(f"   Columns: {list(df.columns)}")
        return df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def prepare_data(df):
    """Minimal preparation - just standardize column names, NO CLEANING"""
    print("\n📋 Step 2: Preparing data (NO CLEANING)...")
    print(f"   Total rows: {len(df):,}")
    
    # Only standardize column names if needed
    df.columns = df.columns.str.strip()
    
    # Rename columns with spaces to match our schema
    column_mapping = {
        'Customer ID': 'CustomerID',
        'Invoice': 'InvoiceNo',
        'Price': 'UnitPrice'
    }
    
    renamed = []
    for old, new in column_mapping.items():
        if old in df.columns:
            df = df.rename(columns={old: new})
            renamed.append(f"{old} → {new}")
    
    if renamed:
        print(f"   Renamed columns: {', '.join(renamed)}")
    
    print(f"   Final columns: {list(df.columns)}")
    print("   ⚠️  Note: Data contains NULLs, cancellations, and negatives (NOT cleaned)")
    
    return df

def create_database_engine():
    """Create SQLAlchemy engine for PostgreSQL"""
    print("\n💾 Step 3: Connecting to Postgres...")
    try:
        connection_string = f'postgresql://{USERNAME}@localhost:5432/{DATABASE_NAME}'
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"❌ Error creating database connection: {e}")
        sys.exit(1)

def load_to_postgres(df, engine):
    """Load RAW dataframe to PostgreSQL"""
    print("\n📤 Step 4: Loading RAW data to Postgres...")
    try:
        df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
        print(f"✅ Loaded {len(df):,} rows to '{TABLE_NAME}' table")
        print("   (Includes NULLs, cancellations, negative values)")
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_data():
    """Verify the loaded data"""
    print("\n✓ Step 5: Verifying data...")
    
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=USERNAME,
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        # Check row count
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        count = cursor.fetchone()[0]
        print(f"   Total rows: {count:,}")
        
        # Check date range
        cursor.execute(f'SELECT MIN("InvoiceDate"), MAX("InvoiceDate") FROM {TABLE_NAME}')
        try:
            min_date, max_date = cursor.fetchone()
            print(f"   Date range: {min_date} to {max_date}")
        except:
            print(f"   (Could not determine date range)")
        
        # Check table structure
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{TABLE_NAME}'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        print(f"\n   Table structure:")
        for col in columns:
            print(f"      - {col[0]}: {col[1]}")
        
        # Count NULL CustomerIDs
        cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME} WHERE "CustomerID" IS NULL')
        null_customers = cursor.fetchone()[0]
        print(f"\n   Rows with NULL CustomerID: {null_customers:,}")
        
        # Count cancelled orders
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE \"InvoiceNo\"::text LIKE 'C%'")
        cancelled = cursor.fetchone()[0]
        print(f"   Cancelled orders (Invoice starts with 'C'): {cancelled:,}")
        
        # Count negative quantities
        cursor.execute(f'SELECT COUNT(*) FROM {TABLE_NAME} WHERE "Quantity" < 0')
        negative_qty = cursor.fetchone()[0]
        print(f"   Negative quantities: {negative_qty:,}")
        
        # Stats on non-null CustomerIDs
        cursor.execute(f'SELECT COUNT(DISTINCT "CustomerID") FROM {TABLE_NAME} WHERE "CustomerID" IS NOT NULL')
        customers = cursor.fetchone()[0]
        print(f"\n   Unique customers (non-NULL): {customers:,}")
        
        cursor.execute(f'SELECT COUNT(DISTINCT "Country") FROM {TABLE_NAME}')
        countries = cursor.fetchone()[0]
        print(f"   Unique countries: {countries}")
        
        # Sample data
        cursor.execute(f'SELECT * FROM {TABLE_NAME} LIMIT 3')
        print(f"\n   Sample rows:")
        for row in cursor.fetchall():
            print(f"      {row[:5]}...")
        
        conn.close()
        return count
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main execution function"""
    print_header("ONLINE RETAIL II DATA LOADER - RAW DATA")
    print("Dataset: UCI Online Retail II (2009-2011)")
    print("Source: https://archive.ics.uci.edu/dataset/502/online+retail+ii")
    print(f"Sheets: {SHEET_NAMES}")
    print("Mode: NO CLEANING - Loading raw data as-is")
    
    # Execute pipeline
    df_raw = download_data()
    df_prepared = prepare_data(df_raw)
    engine = create_database_engine()
    success = load_to_postgres(df_prepared, engine)
    
    if success:
        row_count = verify_data()
        
        if row_count:
            print_header("✅ SETUP COMPLETE!")
            print("\nDatabase Details:")
            print(f"  Dataset: Online Retail II (UCI)")
            print(f"  Sheets loaded: {SHEET_NAMES}")
            print(f"  Mode: RAW DATA (no cleaning)")
            print(f"  Host: localhost")
            print(f"  Port: 5432")
            print(f"  Database: {DATABASE_NAME}")
            print(f"  User: {USERNAME}")
            print(f"  Table: {TABLE_NAME}")
            print(f"  Rows: {row_count:,}")
            print("\n⚠️  Contains: NULLs, cancellations, negative values")
            print("✨ Ready for n8n integration!")
        else:
            print_header("⚠️  SETUP COMPLETED WITH WARNINGS")
    else:
        print_header("❌ SETUP FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
