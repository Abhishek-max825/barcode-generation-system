import pandas as pd
import os
from typing import Dict

def load_department_codes() -> Dict[str, str]:
    """Load department codes from file"""
    try:
        departments = {}
        with open('department_codes.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    code, name = line.strip().split(' - ')
                    departments[name.lower()] = code
        return departments
    except Exception as e:
        print(f"Error loading department codes: {str(e)}")
        return {
            "chemistry": "BBHCCHE",
            "commerce": "BBHCCOM",
            "competitive exam": "BBHCCOMP",
            "computer science": "BBHCCSC",
            "dictionary": "BBHCDIC",
            "economics": "BBHCECO",
            "encyclopedia": "BBHCENC",
            "english": "BBHCENG",
            "general science": "BBHCGEN",
            "hindi": "BBHCHIN",
            "kannada": "BBHCKAN",
            "management": "BBHCMAN",
            "mathematics": "BBHCMAT",
            "physical education": "BBHCPHY",
            "physics": "BBHCPHYS",
            "political science": "BBHCPOL",
            "research methodology": "BBHCRES",
            "sanskrit": "BBHCSAN",
            "year book": "BBHCYEA"
        }

def add_barcode_column():
    """Add barcode_value column to the Excel file"""
    try:
        # Load department codes
        department_codes = load_department_codes()
        print(f"Loaded {len(department_codes)} department codes")
        
        # Read the Excel file
        print("Reading Excel file...")
        df = pd.read_excel('bookreport_copy.xlsx')
        print(f"Original file has {len(df)} rows and {len(df.columns)} columns")
        print(f"Original columns: {df.columns.tolist()}")
        
        # Clean column names
        df.columns = [col.strip().lower() for col in df.columns]
        print(f"Cleaned column names: {df.columns.tolist()}")
        
        # Check if required columns exist
        required_columns = ['department', 'accession number']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Missing required columns: {missing_columns}")
            print(f"Available columns: {df.columns.tolist()}")
            return
        
        # Remove rows with empty department or accession numbers
        original_count = len(df)
        df = df.dropna(subset=['department', 'accession number'])
        print(f"Removed {original_count - len(df)} rows with missing data")
        
        # Create barcode_value column
        barcode_values = []
        for _, row in df.iterrows():
            department = str(row['department']).strip().lower()
            accession_number = str(row['accession number']).strip()
            
            # Find matching department code
            department_code = None
            for dept_name, code in department_codes.items():
                if department == dept_name or dept_name in department or department in dept_name:
                    department_code = code
                    break
            
            if department_code:
                barcode_value = f"{department_code}{accession_number}"
            else:
                barcode_value = f"UNKNOWN{accession_number}"
                print(f"Warning: No department code found for '{department}'")
            
            barcode_values.append(barcode_value)
        
        # Add the new column
        df['barcode_value'] = barcode_values
        
        # Save the updated file
        output_filename = 'bookreport_copy_with_barcodes.xlsx'
        df.to_excel(output_filename, index=False)
        
        print(f"\nSuccessfully added barcode_value column!")
        print(f"Updated file saved as: {output_filename}")
        print(f"Total rows: {len(df)}")
        print(f"New columns: {df.columns.tolist()}")
        
        # Show sample of the new column
        print(f"\nSample barcode values:")
        print(df[['department', 'accession number', 'barcode_value']].head(10))
        
        # Show unique barcode values count
        unique_barcodes = df['barcode_value'].nunique()
        total_barcodes = len(df)
        print(f"\nUnique barcode values: {unique_barcodes}/{total_barcodes}")
        
        if unique_barcodes < total_barcodes:
            print("Warning: Some barcode values are duplicated!")
            duplicates = df[df.duplicated(subset=['barcode_value'], keep=False)]
            print(f"Duplicate barcode values: {len(duplicates)}")
            print(duplicates[['department', 'accession number', 'barcode_value']].head())
        
    except Exception as e:
        print(f"Error processing Excel file: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_barcode_column() 