# 📊 Barcode Generation System

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A professional Flask-based application for generating library barcodes organized by department. This system streamlines inventory management for educational institutions by automating the barcode creation process with department-specific prefixes.

<div align="center">
  <img src="static/images/barcode_example.png" alt="Barcode Example" width="600"/>
  <p><i>Example of generated barcodes with 5×10 grid layout</i></p>
</div>

## ✨ Features

- **Department-Based Generation**: Create barcodes for specific academic departments
- **Industry-Standard Code128 Format**: Generate scanner-compatible barcodes
- **Customizable Layout**: Organized in a 5×10 grid layout for optimal viewing
- **High-Capacity PDF Export**: Download up to 1000 barcodes (100 pages)
- **Barcode Text Display**: Clear text values underneath each barcode
- **Departmental Prefixing**: Department-specific code prefixes (e.g., BBHCCOM for Commerce)
- **Excel Integration**: Import book data directly from Excel spreadsheets 
- **Mobile-Responsive Interface**: Clean, intuitive web interface that works on any device
- **Efficient Processing**: Generate hundreds of barcodes in seconds

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
   - Place your Excel file with book data as `bookreport_with_codes_final.xlsx`
   - Create a copy named `bookreport_copy.xlsx` for the application to use
   - Create a `department_codes.txt` file with department mappings (see format below)

5. Create required directories:
```bash
mkdir -p static/barcodes static/pdfs
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

The system supports various departments with specific code prefixes:

| Department | Code Prefix | Description |
|------------|-------------|-------------|
| Chemistry | BBHCCHE | Chemistry department books |
| Commerce | BBHCCOM | Commerce and business books |
| Computer Science | BBHCCSC | Computer Science and IT books |
| Economics | BBHCECO | Economics books |
| English | BBHCENG | English literature and language books |
| Kannada | BBHCKAN | Kannada literature and language books |
| Management | BBHCMAN | Business management books |
| Mathematics | BBHCMAT | Mathematics books |
| Physics | BBHCPHYS | Physics books |
| Political Science | BBHCPOL | Political science books |
| Research Methodology | BBHCRES | Research methodology books |
| Sanskrit | BBHCSAN | Sanskrit books |
| Year Book | BBHCYEA | Annual publications |

## 🛠️ Technical Details

### Technologies Used
- **Flask**: Web framework for the application
- **python-barcode**: For generating Code128 barcodes
- **Pillow**: Image processing for barcode manipulation
- **ReportLab**: PDF generation with precise control
- **pandas**: Data handling and Excel integration
- **openpyxl**: Excel file reading
- **Bootstrap**: Responsive front-end styling

### Project Structure

```
barcode-generation/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore file
├── department_codes.txt    # Department code mappings
├── bookreport_copy.xlsx    # Excel data source
├── static/                 # Static assets
│   ├── barcodes/           # Generated barcode images
│   ├── pdfs/               # Generated PDF files
│   └── images/             # UI images and icons
└── templates/              # HTML templates
    ├── index.html          # Department selection page
    └── result.html         # Barcode display page
```

## ⚠️ Troubleshooting

### Common Issues

1. **Excel File Error**:
   - Ensure your Excel file is properly formatted with columns for department and accession number
   - Check that the file is not open in another program
   - Try saving as `.xlsx` format instead of `.xls`

2. **Barcode Generation Failure**:
   - Verify department codes are correctly defined
   - Check that accession numbers contain valid characters
   - Ensure the static/barcodes directory has write permissions

3. **PDF Download Issues**:
   - Check browser download settings
   - Verify static/pdfs directory has write permissions
   - For large departments, wait for the generation to complete

### Debug Mode

The application runs in debug mode by default. To disable it for production:
```python
# Change in app.py from:
app.run(debug=True)
# To:
app.run(debug=False, host='0.0.0.0')
```

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