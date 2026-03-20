"""
Generate comprehensive PDF report for disease detection
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os

def generate_pdf_report(image_path, disease_name, symptoms, causes, treatment, prevention, 
                       pesticides, organic_solutions, confidence, output_path):
    """
    Generate a comprehensive PDF report with all disease information
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a4d2e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d6a4f'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leading=16
    )
    
    # Title
    title = Paragraph("🌿 Crop Disease Detection Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Report Info Table
    report_data = [
        ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['Detection Accuracy:', f'{confidence}%'],
        ['Confidence Level:', 'High' if confidence >= 70 else 'Medium' if confidence >= 50 else 'Low'],
        ['Status:', 'Analysis Complete']
    ]
    
    report_table = Table(report_data, colWidths=[2*inch, 4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#d8f3dc')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#40916c'))
    ]))
    elements.append(report_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Uploaded Image
    if os.path.exists(image_path):
        elements.append(Paragraph("📸 Analyzed Image", heading_style))
        img = Image(image_path, width=4*inch, height=3*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))
    
    # Detection Result
    elements.append(Paragraph(f"🔍 Detected Disease: {disease_name}", heading_style))
    
    # Accuracy Box
    accuracy_data = [
        ['Model Accuracy:', f'{confidence}%'],
        ['Confidence Level:', 'High' if confidence >= 70 else 'Medium' if confidence >= 50 else 'Low'],
        ['Reliability:', 'Reliable' if confidence >= 60 else 'Moderate']
    ]
    
    accuracy_table = Table(accuracy_data, colWidths=[2*inch, 4*inch])
    accuracy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ffc107'))
    ]))
    elements.append(accuracy_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Symptoms
    elements.append(Paragraph("🩺 Symptoms", heading_style))
    elements.append(Paragraph(symptoms, normal_style))
    
    # Causes
    elements.append(Paragraph("🔬 Causes", heading_style))
    elements.append(Paragraph(causes, normal_style))
    
    # Treatment
    elements.append(Paragraph("💊 Treatment Methods", heading_style))
    elements.append(Paragraph(treatment, normal_style))
    
    # Prevention
    elements.append(Paragraph("🛡️ Preventive Measures", heading_style))
    elements.append(Paragraph(prevention, normal_style))
    
    # Pesticides
    elements.append(Paragraph("🧪 Recommended Pesticides", heading_style))
    elements.append(Paragraph(pesticides, normal_style))
    
    # Organic Solutions
    elements.append(Paragraph("🌱 Organic Solutions", heading_style))
    elements.append(Paragraph(organic_solutions, normal_style))
    
    # Build PDF
    doc.build(elements)
    return output_path
