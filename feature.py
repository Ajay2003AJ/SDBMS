import os
from flask import Flask, request, send_file, render_template
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
# feature.py (previously app.py inside the testing folder)

from flask import Blueprint

feature_bp = Blueprint('feature', __name__)

@feature_bp.route('/feature')
def feature_route():
    return 'This is the feature route.'

# Define the directory where PDF files will be saved
PDF_DIR = 'S:/testing'

# Define the path to your template PDF
TEMPLATE_PATH = 'C:/Outpass.pdf'

app = Flask(__name__)

# Route for displaying the form
@app.route('/')
def index():
    return render_template('od_certificate_form.html')

# Route for generating OD PDF
@app.route('/generate_od_pdf', methods=['POST'])
def generate_od_pdf():
    # Retrieve student details from the form
    name = request.form['name']
    Rollno = request.form['Rollno']
    dept = request.form['dept']
    year = request.form['year']
    sec = request.form['sec']
    Time = request.form['Time']
    reason = request.form['reason']
    
    # Read the existing PDF template
    template = PdfReader(TEMPLATE_PATH)

    # Create a new PDF writer
    output_path = os.path.join(PDF_DIR, 'od_certificate.pdf')
    output = PdfWriter()

    # Loop through each page of the template
    for page in template.pages:
        # Create a canvas to draw additional text
        packet = BytesIO()
        canvas_ = canvas.Canvas(packet, pagesize=letter)

        # Calculate center coordinates
        width, height = letter
        x_center = width / 2
        y_center = height / 2

        # Set font and size
        canvas_.setFont("Helvetica-Bold", 16)
        
        # Draw text centered on the page
        canvas_.drawString(x_center, y_center, f"Name: {name}")
        canvas_.drawString(x_center, y_center - 20, f"Rollno: {Rollno}")
        canvas_.drawString(x_center, y_center - 40, f"Department: {dept}")
        canvas_.drawString(x_center, y_center - 60, f"Year: {year}")
        canvas_.drawString(x_center, y_center - 80, f"Section: {sec}")
        canvas_.drawString(x_center, y_center - 100, f"Time: {Time}")
        canvas_.drawString(x_center, y_center - 120, f"Reason for OD: {reason}")

        # Save the canvas content to the packet
        canvas_.save()
        packet.seek(0)
        
        # Merge the canvas content with the existing page
        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])

        # Add the modified page to the new PDF writer
        output.add_page(page)

    # Write the new PDF file
    with open(output_path, 'wb') as f:
        output.write(f)

    # Serve the PDF file to the user
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
    app.run(debug=True, port=5001)  # Change port number if needed
