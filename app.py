from flask import Flask, render_template, request, send_file, url_for, send_from_directory, session
import barcode
from barcode.writer import ImageWriter
import os
from werkzeug.utils import secure_filename
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import inch
from PIL import Image
import tempfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/barcodes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your-secret-key-here'  # Required for session

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class BarcodeGenerator:
    def generate_barcode(self, data, filename):
        code = barcode.get('code128', data, writer=ImageWriter())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        code.save(filepath)
        return f"{filename}.png"

    def create_pdf(self, barcode_files, barcodes_per_row=10, barcodes_per_column=10):
        # Create a temporary file for the PDF
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        # Use A3 landscape for better fitting of 10x10 grid
        c = canvas.Canvas(temp_pdf.name, pagesize=landscape(A3))
        
        # Calculate dimensions
        page_width, page_height = landscape(A3)
        margin = 0.5 * inch
        barcode_width = (page_width - 2 * margin) / barcodes_per_row
        barcode_height = (page_height - 2 * margin) / barcodes_per_column
        
        current_row = 0
        current_column = 0
        
        for barcode_file, data in barcode_files:
            # Start new page if needed
            if current_row >= barcodes_per_column:
                c.showPage()
                current_row = 0
                current_column = 0
            
            # Calculate position
            x = margin + (current_column * barcode_width)
            y = page_height - margin - ((current_row + 1) * barcode_height)
            
            # Draw barcode
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], barcode_file)
            # Leave some padding around the barcode
            padding = 5  # Reduced padding to fit more barcodes
            c.drawImage(img_path, x + padding, y + padding, 
                       width=barcode_width - (2 * padding), 
                       height=barcode_height - (2 * padding))
            
            # Update position
            current_column += 1
            if current_column >= barcodes_per_row:
                current_column = 0
                current_row += 1
        
        c.save()
        return temp_pdf.name

@app.route('/')
def index():
    # Clean up any existing barcode files
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if file.endswith('.png'):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        count = int(request.form.get('count', 1))
        prefix = request.form.get('prefix', 'BARCODE')
        
        if count < 1 or count > 100:  # Limit to 100 barcodes
            return "Please enter a number between 1 and 100", 400
        
        barcode_files = []
        generator = BarcodeGenerator()
        
        for i in range(1, count + 1):
            data = f"{prefix}{i}"
            filename = secure_filename(data)
            barcode_file = generator.generate_barcode(data, filename)
            barcode_files.append((barcode_file, data))
        
        # Store barcode files in session for download
        session['barcode_files'] = barcode_files
        
        return render_template('result.html', 
                             barcode_files=barcode_files,
                             count=count)
    except ValueError:
        return "Please enter a valid number", 400
    except Exception as e:
        return str(e), 500

@app.route('/download')
def download():
    try:
        barcode_files = session.get('barcode_files', [])
        if not barcode_files:
            return "No barcodes to download", 404
            
        # Generate PDF
        generator = BarcodeGenerator()
        pdf_path = generator.create_pdf(barcode_files)
        
        # Clean up individual barcode files after sending
        def cleanup():
            for barcode_file, _ in barcode_files:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], barcode_file)
                if os.path.exists(file_path):
                    os.remove(file_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='barcodes.pdf'
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)