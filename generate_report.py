"""
Generate comprehensive PDF report for disease detection
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os


def generate_pdf_report(image_path, disease_name, symptoms, causes, treatment,
                        prevention, pesticides, organic_solutions, confidence, output_path):

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=60, leftMargin=60,
        topMargin=60, bottomMargin=40
    )

    elements = []
    styles   = getSampleStyleSheet()

    # ── Styles ──────────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        'Title', parent=styles['Normal'],
        fontSize=22, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a4d2e'),
        alignment=TA_CENTER, spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        fontSize=11, fontName='Helvetica',
        textColor=colors.HexColor('#555555'),
        alignment=TA_CENTER, spaceAfter=20
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Normal'],
        fontSize=13, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=14, spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#333333'),
        leading=16, spaceAfter=4
    )
    label_style = ParagraphStyle(
        'Label', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a4d2e')
    )

    # ── Title ────────────────────────────────────────────────────────────────
    elements.append(Paragraph("Crop Disease Detection Report", title_style))
    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y  |  %I:%M %p')}",
        subtitle_style
    ))
    elements.append(HRFlowable(width="100%", thickness=2,
                                color=colors.HexColor('#40916c'), spaceAfter=16))

    # ── Report summary table ─────────────────────────────────────────────────
    conf_level = 'High' if confidence >= 80 else 'Medium' if confidence >= 60 else 'Low'
    summary_data = [
        [Paragraph('Disease Detected', label_style), Paragraph(str(disease_name), body_style)],
        [Paragraph('Confidence Score', label_style), Paragraph(f'{confidence:.1f}%', body_style)],
        [Paragraph('Confidence Level', label_style), Paragraph(conf_level, body_style)],
        [Paragraph('Analysis Status', label_style), Paragraph('Complete', body_style)],
    ]
    summary_table = Table(summary_data, colWidths=[2.2*inch, 4.3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#d8f3dc')),
        ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#f8fff9')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#b7e4c7')),
        ('TOPPADDING',    (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))

    # ── Leaf image ───────────────────────────────────────────────────────────
    if image_path and os.path.exists(image_path):
        elements.append(Paragraph("Analyzed Leaf Image", section_style))
        elements.append(HRFlowable(width="100%", thickness=1,
                                    color=colors.HexColor('#b7e4c7'), spaceAfter=8))
        img = Image(image_path, width=3.5*inch, height=2.6*inch)
        img.hAlign = 'LEFT'
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))

    # ── Helper to add a section ──────────────────────────────────────────────
    def add_section(heading, content):
        elements.append(Paragraph(heading, section_style))
        elements.append(HRFlowable(width="100%", thickness=1,
                                    color=colors.HexColor('#b7e4c7'), spaceAfter=6))
        # Replace bullet characters that may cause encoding issues
        safe_content = (content or 'N/A').replace('\u2022', '-').replace('\u2013', '-')
        elements.append(Paragraph(safe_content, body_style))
        elements.append(Spacer(1, 0.1*inch))

    # ── Disease sections ─────────────────────────────────────────────────────
    add_section("Symptoms",              symptoms)
    add_section("Causes",                causes)
    add_section("Treatment Methods",     treatment)
    add_section("Preventive Measures",   prevention)
    add_section("Recommended Pesticides", pesticides)
    add_section("Organic Solutions",     organic_solutions)

    # ── Footer note ──────────────────────────────────────────────────────────
    elements.append(Spacer(1, 0.3*inch))
    elements.append(HRFlowable(width="100%", thickness=1,
                                color=colors.HexColor('#b7e4c7'), spaceAfter=8))
    elements.append(Paragraph(
        "This report was generated automatically by the Crop Disease Detection System. "
        "Please consult an agricultural expert for professional advice.",
        ParagraphStyle('Footer', parent=styles['Normal'],
                       fontSize=8, textColor=colors.HexColor('#888888'),
                       alignment=TA_CENTER)
    ))

    doc.build(elements)
    return output_path
