#!/usr/bin/env python3
"""
Convert PROJECT_SUMMARY.md to PDF
"""

import os

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    
    # Read markdown file
    with open('PROJECT_SUMMARY.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create PDF
    pdf_filename = 'PROJECT_SUMMARY.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2e5c8a'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )
    
    # Parse markdown and add to PDF
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            title = line.replace('# ', '')
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 0.2*inch))
        elif line.startswith('## '):
            heading = line.replace('## ', '')
            elements.append(Paragraph(heading, heading_style))
        elif line.startswith('### '):
            subheading = line.replace('### ', '')
            elements.append(Paragraph(f"<b>{subheading}</b>", normal_style))
        elif line.startswith('- '):
            bullet = line.replace('- ', '• ')
            elements.append(Paragraph(bullet, normal_style))
        elif line.startswith('```'):
            continue
        elif line.strip() == '':
            elements.append(Spacer(1, 0.1*inch))
        else:
            if line.strip():
                elements.append(Paragraph(line, normal_style))
    
    # Build PDF
    doc.build(elements)
    print(f"✅ PDF created: {pdf_filename}")
    print(f"📁 Location: {os.path.abspath(pdf_filename)}")
    
except ImportError:
    print("❌ reportlab not installed")
    print("Install with: pip install reportlab")
    print("\nAlternatively, you can:")
    print("1. Open PROJECT_SUMMARY.md in any text editor")
    print("2. Copy all content")
    print("3. Paste into Word/Google Docs")
    print("4. Export as PDF")
