import PyPDF2
from fpdf import FPDF
import datetime
import tempfile
import os

def extract_text_from_pdf(pdf_file):
    """Extracts text strings from the uploaded blood report PDF."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
    except Exception as e:
        return f"Extraction Error: {str(e)}"

def create_pdf_report(narrative_text, history):
    """Compiles the final markdown analysis text into a professional PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="HEMO-ANALYST: AI CLINICAL REPORT SUMMARY", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 8, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d')} | Made by Keertiraj Singh", ln=True, align='C')
    pdf.ln(10)
    
    # Red Disclaimer Box
    pdf.set_fill_color(255, 230, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, txt="CRITICAL MEDICAL DISCLAIMER:", ln=True, fill=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 5, txt="This document is an AI-assisted text analysis and serves educational purposes only. It is NOT a medical diagnosis. Please verify all findings, scores, and supplement strategies with a certified professional doctor before taking action.", fill=True)
    pdf.ln(5)
    
    # Content Block
    pdf.set_font("Arial", size=11)
    clean_text = narrative_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=clean_text)
    
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, "HemoAnalyst_Final_Report.pdf")
    pdf.output(file_path)
    return file_path
