# Barcode Generation System

A web-based barcode generation system built with Flask for DR. B. B. HEGDE FIRST GRADE COLLEGE, KUNDAPURA.

## Features

- Generate multiple barcodes at once (up to 100)
- Custom prefix support for barcode numbers
- Preview generated barcodes in a grid layout
- Download all barcodes as a single PDF file
- Mobile-responsive design
- Clean and intuitive user interface

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd barcode-generation-system
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage

1. Enter the number of barcodes you want to generate (1-100)
2. Specify a prefix for the barcodes (optional)
3. Click "Generate Barcodes"
4. Preview the generated barcodes
5. Click "Download All" to get a PDF with all barcodes

## Dependencies

- Flask
- python-barcode
- Pillow
- reportlab

## Directory Structure

```
barcode-generation-system/
├── app.py
├── requirements.txt
├── static/
│   ├── barcodes/
│   └── images/
└── templates/
    ├── index.html
    └── result.html
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 