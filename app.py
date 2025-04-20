from flask import Flask, render_template, request, send_file, url_for, send_from_directory, session, flash, redirect
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
import pandas as pd
import shutil
from typing import List, Dict, Tuple, Optional
import logging
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/barcodes'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Ensure the barcodes directory exists
BARCODES_DIR = os.path.join('static', 'barcodes')
os.makedirs(BARCODES_DIR, exist_ok=True)

class DepartmentManager:
    def __init__(self):
        self.departments = self._load_department_codes()
        self.excel_data = self._load_excel_data()
        # Add department aliases for common variations
        self.department_aliases = {
            'economy': 'economics',
            'econ': 'economics',
            'eco': 'economics',
            'comp': 'computer science',
            'computer': 'computer science',
            'cs': 'computer science',
            'comp sci': 'computer science',
            'physic': 'physics',
            'phys': 'physics',
            'math': 'mathematics',
            'maths': 'mathematics',
            'management studies': 'management',
            'mgmt': 'management',
            'dic': 'dictionary',
            'dict': 'dictionary',
            'eng': 'english',
            'pol': 'political science',
            'polsci': 'political science',
            'politics': 'political science',
            'political': 'political science',
            'gen sci': 'general science',
            'general': 'general science',
            'year': 'year book',
            'yb': 'year book',
            'compexam': 'competitive exam',
            'competitive': 'competitive exam',
            'phyedu': 'physical education',
            'physical edu': 'physical education',
            'pe': 'physical education',
            'encl': 'encyclopedia',
            'encyc': 'encyclopedia',
            'encyclo': 'encyclopedia',
            'research': 'research methodology',
            'rm': 'research methodology',
            'comm': 'commerce'
        }
    
    def _load_department_codes(self) -> Dict[str, str]:
        """Load department codes from file or use default mapping"""
        try:
            departments = {}
            with open('department_codes.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        code, name = line.strip().split(' - ')
                        departments[name.lower()] = code
            return departments
        except Exception as e:
            logger.error(f"Error loading department codes: {str(e)}")
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
    
    def _load_excel_data(self) -> pd.DataFrame:
        """Load and clean Excel data"""
        try:
            df = pd.read_excel('bookreport_copy.xlsx')
            # Clean and standardize column names
            df.columns = [col.strip().lower() for col in df.columns]
            # Remove rows with empty department or accession numbers
            df = df.dropna(subset=['department', 'accession number'])
            return df
        except Exception as e:
            logger.error(f"Error loading Excel data: {str(e)}")
            return pd.DataFrame()
    
    def find_matching_department(self, department: str) -> Optional[str]:
        """Find the best matching department name"""
        dept_lower = department.lower()
        
        # Check for exact match first
        if dept_lower in self.departments:
            return dept_lower
        
        # Check for alias match
        if dept_lower in self.department_aliases:
            alias_match = self.department_aliases[dept_lower]
            if alias_match in self.departments:
                logger.info(f"Matched department alias '{dept_lower}' to '{alias_match}'")
                return alias_match
        
        # Try partial match
        for dept in self.departments.keys():
            if dept_lower in dept or dept in dept_lower:
                logger.info(f"Partial match for '{dept_lower}': found '{dept}'")
                return dept
        
        return None
    
    def get_department_books(self, department: str) -> pd.DataFrame:
        """Get books for a specific department"""
        matching_dept = self.find_matching_department(department)
        if not matching_dept:
            logger.warning(f"No matching department found for '{department}'")
            return pd.DataFrame()
        
        logger.info(f"Found matching department: '{matching_dept}' for input '{department}'")
        filtered_df = self.excel_data[self.excel_data['department'].str.lower() == matching_dept]
        
        if filtered_df.empty:
            logger.warning(f"No books found for department: {matching_dept}")
        else:
            logger.info(f"Found {len(filtered_df)} books for department: {matching_dept}")
            
        return filtered_df

class BarcodeGenerator:
    def __init__(self):
        # Create barcodes directory if it doesn't exist
        self.barcodes_dir = os.path.join(os.getcwd(), 'static', 'barcodes')
        os.makedirs(self.barcodes_dir, exist_ok=True)
    
    def generate_barcode(self, data: str, filename: str, department_code: str) -> str:
        """Generate a barcode image with department code prefix"""
        try:
            # Combine department code and accession number
            barcode_data = f"{department_code}{data}"
            logger.info(f"Generating barcode for: {barcode_data}")
            
            # Create barcode instance
            barcode_class = barcode.get_barcode_class('code128')
            code128 = barcode_class(barcode_data, writer=ImageWriter())
            
            # Save directly to the final location with full path
            filepath = os.path.join(self.barcodes_dir, filename)
            logger.info(f"Saving barcode to: {filepath}")
            
            # Save with optimized settings for better barcode visibility
            options = {
                'module_height': 10.0,    # Barcode height
                'module_width': 0.2,      # Bar width
                'quiet_zone': 4.0,        # Quiet zone around barcode
                'write_text': False,      # Don't show text below barcode
                'background': 'white',    # White background
                'foreground': 'black',    # Black bars
                'dpi': 300                # High resolution
            }
            
            # Generate and save the barcode
            generated_filename = code128.save(
                os.path.splitext(filepath)[0],  # Remove .png extension as it's added automatically
                options
            )
            
            # Verify the file exists
            if not os.path.exists(generated_filename):
                raise Exception(f"Failed to generate barcode file: {generated_filename}")
            
            logger.info(f"Successfully generated barcode: {os.path.basename(generated_filename)}")
            return os.path.basename(generated_filename)
                
        except Exception as e:
            logger.error(f"Error generating barcode: {e}")
            raise

    def create_pdf(self, barcode_files: List[Tuple[str, str]], 
                  barcodes_per_row: int = 10, 
                  barcodes_per_column: int = 10,
                  max_pages: int = 35) -> str:
        """Create a PDF with barcodes arranged in a grid"""
        try:
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            c = canvas.Canvas(temp_pdf.name, pagesize=landscape(A3))
            
            page_width, page_height = landscape(A3)
            margin = 0.5 * inch
            barcode_width = (page_width - 2 * margin) / barcodes_per_row
            barcode_height = (page_height - 2 * margin) / barcodes_per_column
            
            current_row = 0
            current_column = 0
            current_page = 1
            
            for barcode_file, barcode_data in barcode_files:
                if current_page > max_pages:
                    logger.warning(f"Maximum number of pages ({max_pages}) reached. Some barcodes may not be included.")
                    break
                
                if current_column >= barcodes_per_row:
                    current_column = 0
                    current_row += 1
                
                if current_row >= barcodes_per_column:
                    c.showPage()
                    current_row = 0
                    current_column = 0
                    current_page += 1
                
                x = margin + (current_column * barcode_width)
                y = page_height - margin - ((current_row + 1) * barcode_height)
                
                img_path = os.path.join(self.barcodes_dir, barcode_file)
                if os.path.exists(img_path):
                    try:
                        # Calculate dimensions to maintain aspect ratio
                        img = Image.open(img_path)
                        img_w, img_h = img.size
                        aspect = img_w / float(img_h)
                        
                        # Calculate new dimensions - make room for text
                        new_w = barcode_width - 10
                        new_h = (new_w / aspect) * 0.85  # Reduce height to leave room for text
                        
                        if new_h > (barcode_height - 20) * 0.85:
                            new_h = (barcode_height - 20) * 0.85
                            new_w = new_h * aspect
                        
                        # Center the barcode
                        x_offset = (barcode_width - new_w) / 2
                        # Position barcode higher to make room for text
                        y_offset = (barcode_height - new_h) / 2 + 5
                        
                        c.drawImage(img_path, x + x_offset, y + y_offset, 
                                  width=new_w, height=new_h)
                        
                        # Add barcode text below the image
                        c.setFont("Helvetica", 8)
                        text_width = c.stringWidth(barcode_data, "Helvetica", 8)
                        text_x = x + (barcode_width - text_width) / 2
                        c.drawString(text_x, y + 5, barcode_data)
                        
                    except Exception as e:
                        logger.error(f"Error processing barcode image {barcode_file}: {e}")
                else:
                    logger.error(f"Barcode image not found: {img_path}")
                
                current_column += 1
            
            c.save()
            logger.info(f"PDF created with {current_page} pages containing {len(barcode_files)} barcodes")
            return temp_pdf.name
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            raise

# Initialize managers
department_manager = DepartmentManager()
barcode_generator = BarcodeGenerator()

def cleanup_old_barcodes():
    """Remove old barcode files from the static/barcodes directory"""
    try:
        barcodes_dir = os.path.join('static', 'barcodes')
        # Create directory if it doesn't exist
        os.makedirs(barcodes_dir, exist_ok=True)
        # Remove old files
        for file in os.listdir(barcodes_dir):
            if file.endswith('.png'):
                try:
                    os.remove(os.path.join(barcodes_dir, file))
                except Exception as e:
                    logger.error(f"Error removing file {file}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning up barcode files: {str(e)}")

@app.route('/')
def index():
    # Clean up old barcode files before starting new generation
    cleanup_old_barcodes()
    
    # Clear session data to prevent issues with previous departments
    session.clear()
    
    departments = department_manager.departments
    return render_template('index.html', departments=departments)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Clear any existing session data to prevent conflicts
        session.clear()
        
        selected_department = request.form.get('department')
        if not selected_department:
            flash('Please select a department', 'error')
            return redirect(url_for('index'))

        # Clean up old files before generating new ones
        cleanup_old_barcodes()

        # Get department books
        dept_books = department_manager.get_department_books(selected_department)
        
        if dept_books.empty:
            flash(f'No books found for department: {selected_department}', 'error')
            return redirect(url_for('index'))

        # Get department code
        department_code = department_manager.departments.get(selected_department.lower())
        if not department_code:
            flash(f'Invalid department code for: {selected_department}', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Generating barcodes for department: {selected_department} ({department_code})")
        
        # Create barcodes
        barcode_files = []
        for _, book in dept_books.iterrows():
            try:
                accession_number = str(book['accession number']).strip()
                if not accession_number:
                    continue

                # Generate barcode filename without extension (it's added by the library)
                base_filename = secure_filename(f"{department_code}{accession_number}")
                
                # Generate barcode
                barcode_filename = barcode_generator.generate_barcode(
                    accession_number, 
                    base_filename, 
                    department_code
                )
                
                # Store both the filename and the full barcode data
                barcode_data = f"{department_code}{accession_number}"
                barcode_files.append((barcode_filename, barcode_data))
                
            except Exception as e:
                logger.error(f"Error creating barcode for {accession_number}: {str(e)}")
                continue

        if not barcode_files:
            flash('No valid barcodes could be generated', 'error')
            return redirect(url_for('index'))

        logger.info(f"Successfully generated {len(barcode_files)} barcodes")
        
        # Generate a unique ID for this batch
        batch_id = str(uuid.uuid4())
        
        # Create PDF directly and save with department name
        safe_dept_name = secure_filename(selected_department.lower())
        pdf_filename = f"{safe_dept_name}_barcodes_{batch_id}.pdf"
        pdf_path = os.path.join(os.getcwd(), 'static', 'pdfs', pdf_filename)
        
        # Ensure PDF directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        # Create PDF with department name
        temp_pdf_path = barcode_generator.create_pdf(barcode_files, barcodes_per_row=10, barcodes_per_column=10, max_pages=35)
        shutil.copy(temp_pdf_path, pdf_path)
        
        # Store only what we need for the results page
        session['pdf_filename'] = pdf_filename
        session['selected_department'] = selected_department
        
        return render_template('result.html', 
                             barcodes=barcode_files, 
                             total_barcodes=len(barcode_files),
                             department=selected_department,
                             pdf_filename=pdf_filename)

    except Exception as e:
        logger.error(f"Error in generate function: {str(e)}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_pdf(filename):
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            logger.error(f"Invalid filename requested: {filename}")
            flash('Invalid file request', 'error')
            return redirect(url_for('index'))
            
        pdf_path = os.path.join(os.getcwd(), 'static', 'pdfs', filename)
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file not found: {pdf_path}")
            flash('PDF file could not be found. Please regenerate the barcodes.', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Downloading PDF: {filename}")
        
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
            
    except Exception as e:
        logger.error(f"Error in download route: {e}")
        flash(f'An error occurred while downloading: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)