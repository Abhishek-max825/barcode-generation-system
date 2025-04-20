import pandas as pd
import os

excel_file = 'bookreport_with_codes_final.xlsx'

print(f"File exists: {os.path.exists(excel_file)}")
print(f"File size: {os.path.getsize(excel_file) if os.path.exists(excel_file) else 'N/A'}")
print(f"File permissions: {oct(os.stat(excel_file).st_mode)[-3:] if os.path.exists(excel_file) else 'N/A'}")

try:
    df = pd.read_excel(excel_file)
    print(f"\nSuccessfully read Excel file!")
    print(f"Number of rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
except Exception as e:
    print(f"\nError reading Excel file: {str(e)}") 