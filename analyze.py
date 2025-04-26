import pandas as pd
import os
import tempfile
import shutil
from datetime import datetime

try:
    # Create temporary directory and copy file
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'temp_excel.xlsx')
    shutil.copy2('bookreport_copy.xlsx', temp_file)
    
    # Read the Excel file
    df = pd.read_excel(temp_file)
    
    # Clean and standardize column names
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # Find the department column
    dept_col = next((col for col in df.columns if 'dept' in col or 'department' in col), None)
    if dept_col:
        # Rename and clean department column
        df = df.rename(columns={dept_col: 'department'})
        df['department'] = df['department'].astype(str).str.lower().str.strip()
        
        # Count books per department
        books_per_dept = df['department'].value_counts().sort_values()
        
        # Create output file
        output_file = 'department_book_counts.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write("DEPARTMENT BOOK COUNT REPORT\n")
            f.write("===========================\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write total books count
            f.write(f"Total number of books: {len(df)}\n")
            f.write(f"Total number of departments: {len(books_per_dept)}\n\n")
            
            # Write department-wise counts
            f.write("DEPARTMENT WISE BOOK COUNT:\n")
            f.write("--------------------------\n")
            for dept, count in books_per_dept.items():
                f.write(f"{dept.title():<25} : {count:>5} books\n")
            
            # Write summary
            f.write("\nSUMMARY:\n")
            f.write("--------\n")
            f.write(f"Department with minimum books: {books_per_dept.idxmin().title()} ({books_per_dept.min()} books)\n")
            f.write(f"Department with maximum books: {books_per_dept.idxmax().title()} ({books_per_dept.max()} books)\n")
        
        print(f"\nReport has been saved to: {output_file}")
    
    # Clean up
    os.remove(temp_file)
    os.rmdir(temp_dir)
    
except Exception as e:
    print(f"Error analyzing Excel file: {e}")
    # Clean up in case of error
    try:
        if 'temp_file' in locals() and os.path.exists(temp_file):
            os.remove(temp_file)
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    except:
        pass 