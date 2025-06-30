import pandas as pd
import os

excel_file = 'bookreport_copy.xlsx'

print(f"File exists: {os.path.exists(excel_file)}")
print(f"File size: {os.path.getsize(excel_file) if os.path.exists(excel_file) else 'N/A'}")

try:
    df = pd.read_excel(excel_file)
    print(f"\nSuccessfully read Excel file!")
    print(f"Number of rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Show first few rows to understand the data structure
    print(f"\nFirst 3 rows:")
    print(df.head(3))
    
    # Show data types
    print(f"\nData types:")
    print(df.dtypes)
    
    # Check for any unique identifiers
    print(f"\nChecking for potential unique identifiers:")
    for col in df.columns:
        unique_count = df[col].nunique()
        total_count = len(df)
        print(f"{col}: {unique_count}/{total_count} unique values")
        
except Exception as e:
    print(f"\nError reading Excel file: {str(e)}") 