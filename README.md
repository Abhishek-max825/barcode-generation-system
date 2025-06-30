# 📊 Barcode Generation System

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A professional Flask-based application for generating library barcodes organized by department. This system streamlines inventory management for educational institutions by automating the barcode creation process with department-specific prefixes and comprehensive data management.

<div align="center">
  <img src="static/images/barcode_example.png" alt="Barcode Example" width="600"/>
  <p><i>Example of generated barcodes with 4×5 grid layout</i></p>
</div>

## ✨ Features

- **Department-Based Generation**: Create barcodes for specific academic departments
- **Industry-Standard Code128 Format**: Generate scanner-compatible barcodes
- **Customizable Layout**: Organized in a 4×5 grid layout for optimal viewing
- **High-Capacity PDF Export**: Download up to 1000 barcodes (100 pages)
- **Barcode Text Display**: Clear text values underneath each barcode
- **Departmental Prefixing**: Department-specific code prefixes (e.g., BBHCCOM for Commerce)
- **Excel Integration**: Import book data directly from Excel spreadsheets 
- **Smart Department Matching**: Intelligent fuzzy matching for department names with aliases
- **Barcode Value Column**: Automatic generation of barcode_value column in Excel files
- **Mobile-Responsive Interface**: Clean, intuitive web interface that works on any device
- **Efficient Processing**: Generate hundreds of barcodes in seconds
- **Data Validation**: Comprehensive error handling and data validation
- **Session Management**: Secure session handling for multiple users

## 🚀 Installation

### Prerequisites
- Python 3.6+
- Git
- Excel file with book data

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/barcode-generation.git
cd barcode-generation
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Prepare your data:
   - Place your Excel file with book data as `bookreport_copy.xlsx`
   - Create a `department_codes.txt` file with department mappings (see format below)
   - Run the barcode column generator: `python add_barcode_column.py`

5. Create required directories:
```bash
mkdir -p static/barcodes static/pdfs static/images
```

## 📝 Department Code Format

The `department_codes.txt` file should follow this format:
```
BBHCCHE - chemistry
BBHCCOM - commerce
BBHCCSC - computer science
BBHCECO - economics
...
```

## 🛠️ Utility Scripts

### Adding Barcode Value Column
To add a `barcode_value` column to your Excel file:
```bash
python add_barcode_column.py
```
This script will:
- Read your `bookreport_copy.xlsx` file
- Generate barcode values using department codes + accession numbers
- Create a new file `bookreport_copy_with_barcodes.xlsx`
- Validate data integrity and check for duplicates

### Excel File Analysis
To analyze your Excel file structure:
```bash
python examine_excel.py
```
This helps verify your data format and identify any issues.

## 🖥️ Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open a browser and navigate to `http://127.0.0.1:5000`

3. Select a department from the dropdown menu

4. Click "Generate Barcodes" to create barcodes

5. View generated barcodes and click "Download" to get the PDF

## 📋 Supported Departments

The system supports various departments with specific code prefixes and intelligent name matching:

| Department | Code Prefix | Aliases |
|------------|-------------|---------|
| Chemistry | BBHCCHE | chemistry |
| Commerce | BBHCCOM | commerce, comm |
| Computer Science | BBHCCSC | computer science, comp, computer, cs, comp sci |
| Economics | BBHCECO | economics, economy, econ, eco |
| English | BBHCENG | english, eng |
| General Science | BBHCGEN | general science, gen sci, general |
| Hindi | BBHCHIN | hindi |
| Kannada | BBHCKAN | kannada |
| Management | BBHCMAN | management, management studies, mgmt |
| Mathematics | BBHCMAT | mathematics, math, maths |
| Physical Education | BBHCPHY | physical education, phyedu, physical edu, pe |
| Physics | BBHCPHYS | physics, physic, phys |
| Political Science | BBHCPOL | political science, pol, polsci, politics, political |
| Research Methodology | BBHCRES | research methodology, research, rm |
| Sanskrit | BBHCSAN | sanskrit |
| Year Book | BBHCYEA | year book, year, yb |

## 📊 Data Structure

### Excel File Requirements
Your Excel file should contain these columns:
- `Accession Number`: Unique identifier for each book
- `Title`: Book title
- `Department`: Department name (will be matched intelligently)
- `Author`: Book author
- `barcode_value`: Generated automatically (format: {DepartmentCode}{AccessionNumber})

### Example Data
```
Accession Number | Title           | Department      | Author     | barcode_value
3               | Business Basics | commerce        | John Doe   | BBHCCOM3
6               | Management 101  | management      | Jane Smith | BBHCMAN6
```

## 🛠️ Technical Details

### Technologies Used
- **Flask**: Web framework for the application
- **python-barcode**: For generating Code128 barcodes
- **Pillow**: Image processing for barcode manipulation
- **ReportLab**: PDF generation with precise control
- **pandas**: Data handling and Excel integration
- **openpyxl**: Excel file reading
- **Bootstrap**: Responsive front-end styling
- **Werkzeug**: File handling and security

### Project Structure

```
barcode-generation/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore file
├── department_codes.txt            # Department code mappings
├── bookreport_copy.xlsx            # Excel data source
├── bookreport_copy_with_barcodes.xlsx  # Excel with barcode values
├── add_barcode_column.py           # Utility to add barcode column
├── examine_excel.py                # Excel file analyzer
├── analyze.py                      # Data analysis script
├── static/                         # Static assets
│   ├── barcodes/                   # Generated barcode images
│   ├── pdfs/                       # Generated PDF files
│   └── images/                     # UI images and icons
└── templates/                      # HTML templates
    ├── index.html                  # Department selection page
    └── result.html                 # Barcode display page
```

## ⚠️ Troubleshooting

### Common Issues

1. **Excel File Error**:
   - Ensure your Excel file is properly formatted with columns for department and accession number
   - Check that the file is not open in another program
   - Try saving as `.xlsx` format instead of `.xls`
   - Run `python examine_excel.py` to verify file structure

2. **Barcode Generation Failure**:
   - Verify department codes are correctly defined in `department_codes.txt`
   - Check that accession numbers contain valid characters
   - Ensure the static/barcodes directory has write permissions
   - Use the department aliases if exact names don't match

3. **PDF Download Issues**:
   - Check browser download settings
   - Verify static/pdfs directory has write permissions
   - For large departments, wait for the generation to complete
   - Check file size limits in your browser

4. **Department Not Found**:
   - Check spelling of department names
   - Use the aliases listed in the supported departments table
   - Verify the department exists in your Excel file

### Debug Mode

The application runs in debug mode by default. To disable it for production:
```python
# Change in app.py from:
app.run(debug=True)
# To:
app.run(debug=False, host='0.0.0.0')
```

## 🔧 Configuration

### Environment Variables
You can configure the application using environment variables:
- `FLASK_ENV`: Set to 'production' for production deployment
- `SECRET_KEY`: Custom secret key for session management
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

### Customization
- Modify `department_codes.txt` to add new departments
- Adjust PDF layout in `app.py` (barcodes_per_row, barcodes_per_column)
- Customize barcode appearance in the `BarcodeGenerator` class

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

For questions or support, please contact [abhishettyabhi267@gmail.com](mailto:abhishettyabhi267@gmail.com).

## 📈 Version History

### v2.0.0 (Current)
- Added barcode_value column generation
- Improved department name matching with aliases
- Enhanced error handling and validation
- Added utility scripts for data management
- Updated documentation and troubleshooting guide

### v1.0.0
- Initial release with basic barcode generation
- Department-based organization
- PDF export functionality 