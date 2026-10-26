from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def report_text(record):
    result = record['result']
    error_message = record['error_message'] if 'error_message' in record.keys() else None
    explanation = {'MATCH': 'The calculated SHA-256 hash matches the stored reference.', 'MISMATCH': 'The calculated SHA-256 hash differs from the stored reference.', 'REFERENCE_NOT_FOUND': 'No registered reference was available for this verification.'}.get(result, error_message or 'The verification could not be completed.')
    return '\n'.join(['SECUREDOC VERIFICATION REPORT', f"Report identifier: {record['id']}", f"Document name: {record['document_name']}", f"Verification date: {record['verified_at']}", 'Hash algorithm: SHA-256', f"Reference hash: {record['reference_hash'] or 'Not available'}", f"Calculated hash: {record['calculated_hash'] or 'Not available'}", f"Verification result: {result}", f"Explanation: {explanation}", '', 'Limitation: This local reference should be protected; SQLite alone is not tamper-proof.'])

def report_pdf(record):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=.65*inch, leftMargin=.65*inch, topMargin=.6*inch, bottomMargin=.6*inch)
    styles = getSampleStyleSheet(); styles.add(ParagraphStyle(name='Mono', parent=styles['BodyText'], fontName='Courier', fontSize=8, leading=11))
    color = colors.HexColor('#16734b') if record['result'] == 'MATCH' else colors.HexColor('#b42318')
    story = [Paragraph('SecureDoc', styles['Title']), Paragraph('Verification report', styles['Heading2']), Spacer(1, 14)]
    rows = [['Report identifier', str(record['id'])], ['Document', record['document_name']], ['Verified at', record['verified_at']], ['Algorithm', 'SHA-256'], ['Reference hash', record['reference_hash'] or 'Not available'], ['Calculated hash', record['calculated_hash'] or 'Not available'], ['Result', record['result']]]
    table = Table([[Paragraph(str(a), styles['BodyText']), Paragraph(str(b), styles['Mono'] if 'hash' in a.lower() else styles['BodyText'])] for a,b in rows], colWidths=[1.5*inch, 5.7*inch])
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.HexColor('#d8e0eb')),('BACKGROUND',(0,0),(0,-1),colors.HexColor('#f3f6fa')),('TEXTCOLOR',(1,6),(1,6),color),('FONTNAME',(1,6),(1,6),'Helvetica-Bold'),('VALIGN',(0,0),(-1,-1),'TOP'),('PADDING',(0,0),(-1,-1),8)]))
    story += [table, Spacer(1, 18), Paragraph('This report reflects a content comparison against the locally stored reference. A matching hash does not establish authorship, and SQLite alone is not tamper-proof.', styles['BodyText'])]
    doc.build(story); return output.getvalue()
