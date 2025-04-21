# Barcode Generation System

A Flask-based application for generating barcodes for library books organized by department.

## Features

- Generate barcodes for books from different departments
- Organize barcodes in a 5×10 grid layout
- Download barcodes as PDF (up to 100 pages)
- Display barcodes with text values underneath
- Department-specific barcode prefixes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/barcode-generation.git
cd barcode-generation
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Prepare your data:
   - Place your Excel file with book data as `bookreport_with_codes_final.xlsx`
   - Create a `department_codes.txt` file with department mappings

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open a browser and navigate to `http://127.0.0.1:5000`

3. Select a department from the dropdown menu

4. Click "Generate Barcodes" to create barcodes

5. View generated barcodes and click "Download" to get the PDF

## Department Codes

The system supports various departments with specific code prefixes:
- Chemistry: BBHCCHE
- Commerce: BBHCCOM 
- Computer Science: BBHCCSC
- Economics: BBHCECO
- English: BBHCENG
- Kannada: BBHCKAN
- Management: BBHCMAN
- Mathematics: BBHCMAT
- Physics: BBHCPHYS
- And more...

## File Structure

- `app.py`: Main Flask application
- `static/barcodes/`: Generated barcode images
- `static/pdfs/`: Generated PDF files
- `templates/`: HTML templates for the web interface
- `department_codes.txt`: Department code mappings
- `bookreport_copy.xlsx`: Excel data source for book information

## Requirements

- Python 3.6+
- Flask
- pandas
- python-barcode
- Pillow
- reportlab
- openpyxl 