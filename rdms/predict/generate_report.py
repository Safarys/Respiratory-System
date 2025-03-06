from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import os
from django.conf import settings

def generate_report(patient_name, age, symptoms, date, disease, confidence, severity, spectrogram_path):
    """Generates a PDF report for respiratory disease diagnosis, including spectrogram."""
    report_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(report_dir, exist_ok=True)  # Ensure directory exists

    report_filename = f"{patient_name.replace(' ', '_')}_report.pdf"
    report_path = os.path.join(report_dir, report_filename)
    
    c = canvas.Canvas(report_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 750, "Respiratory Disease Diagnosis Report")
    c.setFont("Helvetica", 12)
    
    # Patient Info
    c.drawString(50, 710, f"Patient Name: {patient_name}")
    c.drawString(50, 690, f"Age: {age}")
    c.drawString(50, 670, f"Symptoms: {symptoms}")
    c.drawString(50, 650, f"Date: {date}")

    # Prediction Results
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 620, "Diagnostic Results:")
    c.setFont("Helvetica", 12)
    c.drawString(50, 600, f"- Predicted Disease: {disease}")
    c.drawString(50, 580, f"- Confidence Score: {confidence:.2f}%")
    c.drawString(50, 560, f"- Severity Level: {severity}")

    # Add Spectrogram Image if available
    if os.path.exists(spectrogram_path):
        c.drawString(50, 530, "Spectrogram Analysis:")
        spectrogram_image = Image(spectrogram_path, width=400, height=150)
        spectrogram_image.drawOn(c, 50, 350)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, "Note: This is an AI-based prediction. Consult a doctor for further evaluation.")

    c.save()
    return report_path
