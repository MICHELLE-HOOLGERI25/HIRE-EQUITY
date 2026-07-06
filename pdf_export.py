import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def generate_pdf_report(metadata, original_score, fixed_score, flagged_items, original_jd, fixed_jd):
    """
    Generates a beautifully styled, production-ready 3-page PDF report.
    Returns a bytes object of the PDF content.
    """
    buffer = io.BytesIO()
    
    # 0.5 inch margins = 36 points. Printable width = 612 - 72 = 540 points.
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles to avoid modifying existing defaults
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'), # Slate 900
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#64748B'), # Slate 500
        spaceAfter=20
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1E293B'), # Slate 800
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155') # Slate 700
    )
    
    body_bold = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    # Font style for tables
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    
    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )
    
    # Style for original/fixed JD side-by-side
    jd_compare_style = ParagraphStyle(
        'JdCompareStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    # Styles for scorecard headers (labels)
    score_label_orig = ParagraphStyle(
        'ScoreLabelOrig',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#E11D48'), # Red
        alignment=TA_CENTER
    )
    score_label_opt = ParagraphStyle(
        'ScoreLabelOpt',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#16A34A'), # Green
        alignment=TA_CENTER
    )
    score_label_boost = ParagraphStyle(
        'ScoreLabelBoost',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'), # Blue
        alignment=TA_CENTER
    )

    # Styles for scorecard values
    score_val_orig = ParagraphStyle(
        'ScoreValOrig',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#E11D48'), # Red
        alignment=TA_CENTER
    )
    score_val_opt = ParagraphStyle(
        'ScoreValOpt',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#16A34A'), # Green
        alignment=TA_CENTER
    )
    score_val_boost = ParagraphStyle(
        'ScoreValBoost',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor('#2563EB'), # Blue
        alignment=TA_CENTER
    )

    story = []
    
    # =========================================================================
    # PAGE 1: SUMMARY
    # =========================================================================
    
    # Header Banner Style
    story.append(Paragraph("HireEquity — Audit Report", title_style))
    date_str = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"AI-Powered Job Description Bias Audit & Optimization  |  Date: {date_str}", subtitle_style))
    
    # Metadata Box
    metadata_data = [
        [
            Paragraph("<b>Role Name:</b>", body_style), 
            Paragraph(metadata.get("role", "N/A"), body_bold),
            Paragraph("<b>Experience Level:</b>", body_style), 
            Paragraph(metadata.get("level", "N/A"), body_bold)
        ],
        [
            Paragraph("<b>Industry Domain:</b>", body_style), 
            Paragraph(metadata.get("domain", "N/A"), body_bold),
            Paragraph("<b>Report ID:</b>", body_style), 
            Paragraph(f"HE-{datetime.now().strftime('%Y%m%d%H%M')}", body_bold)
        ]
    ]
    metadata_table = Table(metadata_data, colWidths=[100, 170, 110, 160])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9')),
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("Executive Scorecard Summary", h1_style))
    
    # Compute stats
    improvement_val = fixed_score - original_score
    total_flags = len(flagged_items)
    
    # Score blocks table
    # We display big metrics visually in a clean table grid
    score_blocks = [
        [
            Paragraph("Original Score", score_label_orig),
            Paragraph("Optimized Score", score_label_opt),
            Paragraph("Score Boost", score_label_boost)
        ],
        [
            Paragraph(f"{original_score}<font size=14 color='#64748B'>/100</font>", score_val_orig),
            Paragraph(f"{fixed_score}<font size=14 color='#64748B'>/100</font>", score_val_opt),
            Paragraph(f"+{improvement_val}<font size=14 color='#64748B'> pts</font>", score_val_boost)
        ]
    ]
    
    score_table = Table(score_blocks, colWidths=[180, 180, 180])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('LINEAFTER', (0,0), (0,1), 1, colors.HexColor('#E2E8F0')),
        ('LINEAFTER', (1,0), (1,1), 1, colors.HexColor('#E2E8F0')),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 25))
    
    # Inclusivity insights
    story.append(Paragraph("Key Insights & Highlights", h1_style))
    
    inclusivity_details = f"""
    This audit analyzed the job description for potential exclusionary language across 5 major bias categories: Gender Bias, Age Bias, Ableism, Elitism, and Overly Restrictive requirements.
    <br/><br/>
    <b>Summary of Audit Findings:</b>
    <ul>
        <li>A total of <b>{total_flags}</b> bias-coded or restrictive phrase(s) were flagged by the dual-engine scan.</li>
        <li>The initial job description received an inclusivity rating of <b>{original_score}/100</b>, indicating opportunities to expand the talent pool.</li>
        <li>After applying the AI-Powered Auto-Rewriter, all flagged items were resolved, improving the overall score to <b>{fixed_score}/100</b>.</li>
        <li>This represents a net inclusivity boost of <b>{improvement_val}%</b>.</li>
    </ul>
    """
    story.append(Paragraph(inclusivity_details, body_style))
    story.append(Spacer(1, 20))
    
    # Disclaimer / Footer info
    disclaimer = """
    <i>Disclaimer: The Gaucher et al. model is a research-backed heuristic framework for checking language appeal. Lower score indicates masculine-skewed or restricted phrasing which has been shown to reduce applicant pool diversity. HireEquity optimizations do not guarantee legal compliance but rather aim to improve candidate pool inclusivity.</i>
    """
    story.append(Paragraph(disclaimer, ParagraphStyle('Disclaimer', parent=body_style, fontSize=8, leading=11, textColor=colors.HexColor('#94A3B8'))))
    
    # Page Break to Page 2
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: AUDIT DETAILS
    # =========================================================================
    story.append(Paragraph("Detailed Bias Audit & Category Breakdown", title_style))
    story.append(Paragraph("A granular view of specific flags identified during the scanning process.", subtitle_style))
    
    # Category counts for breakdown
    cat_counts = {}
    for f in flagged_items:
        cat = f.get("category", "General")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        
    story.append(Paragraph("Flags Found per Category", h1_style))
    
    # Category summary table
    cat_data = [[Paragraph("<b>Category</b>", table_cell_header), Paragraph("<b>Flag Count</b>", table_cell_header)]]
    for cat, count in cat_counts.items():
        cat_data.append([
            Paragraph(cat, table_cell_style),
            Paragraph(str(count), table_cell_style)
        ])
    if not cat_counts:
        cat_data.append([Paragraph("No flags found in any category", table_cell_style), Paragraph("0", table_cell_style)])
        
    cat_table = Table(cat_data, colWidths=[380, 160])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('PADDING', (0,1), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 20))
    
    # Flagged Phrases Table
    story.append(Paragraph("Flagged Phrases & Remediation Guide", h1_style))
    
    # Table Width breakdown: 90 + 100 + 70 + 280 = 540
    flag_table_headers = [
        Paragraph("<b>Phrase / Term</b>", table_cell_header),
        Paragraph("<b>Category</b>", table_cell_header),
        Paragraph("<b>Severity</b>", table_cell_header),
        Paragraph("<b>Suggested Alternative</b>", table_cell_header)
    ]
    
    flag_table_data = [flag_table_headers]
    
    for f in flagged_items:
        sev = f.get("severity", "moderate").upper()
        # Color-code severity label
        if sev == "CRITICAL":
            sev_txt = f"<font color='#E11D48'><b>{sev}</b></font>"
        elif sev == "MODERATE":
            sev_txt = f"<font color='#D97706'><b>{sev}</b></font>"
        else:
            sev_txt = f"<font color='#2563EB'><b>{sev}</b></font>"
            
        phrase = f.get("phrase", "")
        category = f.get("category", "General")
        suggestion = f.get("suggestion", "")
        
        flag_table_data.append([
            Paragraph(f"<b>{phrase}</b>", table_cell_style),
            Paragraph(category, table_cell_style),
            Paragraph(sev_txt, table_cell_style),
            Paragraph(suggestion, table_cell_style)
        ])
        
    if len(flagged_items) == 0:
        flag_table_data.append([
            Paragraph("No bias flags identified in this job description.", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("-", table_cell_style),
            Paragraph("Text is clean and inclusive.", table_cell_style)
        ])
        
    flag_table = Table(flag_table_data, colWidths=[100, 110, 70, 260])
    flag_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('PADDING', (0,1), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(flag_table)
    
    # Page Break to Page 3
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: JD COMPARISON
    # =========================================================================
    story.append(Paragraph("Job Description Optimization Comparison", title_style))
    story.append(Paragraph("A side-by-side view showing the changes made to achieve full inclusivity.", subtitle_style))
    
    # Prepare JDs for PDF display by replacing newlines with HTML linebreaks
    orig_formatted = original_jd.replace('\n', '<br/>')
    fixed_formatted = fixed_jd.replace('\n', '<br/>')
    
    compare_data = [
        [
            Paragraph("<b>Original Job Description</b>", table_cell_header),
            Paragraph("<b>Optimized Job Description (Clean)</b>", table_cell_header)
        ],
        [
            Paragraph(orig_formatted, jd_compare_style),
            Paragraph(fixed_formatted, jd_compare_style)
        ]
    ]
    
    # Width: 265 each = 530 total (leaves 10 points buffer)
    compare_table = Table(compare_data, colWidths=[265, 265])
    compare_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('LINEBEFORE', (1,0), (1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFF1F2'), colors.white]), # Light red background on original side could be simulated, but let's keep it simple
    ]))
    story.append(compare_table)
    
    # Build Document
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
