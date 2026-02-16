from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import os

def generate_pdf():
    top_10_file = "top_10.json"
    if not os.path.exists(top_10_file):
        return None

    with open(top_10_file, "r") as f:
        top_10 = json.load(f)

    pdf_folder = "reports"
    os.makedirs(pdf_folder, exist_ok=True)
    pdf_path = os.path.join(pdf_folder, "Top10_Resume_Report.pdf")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "TalentRank AI - Top 10 Candidates Report")

    y = 700
    for idx, candidate in enumerate(top_10):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"{idx+1}. {candidate['name']} - Score: {candidate['match_score']}%")
        c.setFont("Helvetica", 11)
        c.drawString(60, y-15, f"Skills: {', '.join(candidate['skills'])}")
        c.drawString(60, y-30, f"Experience: {candidate['experience']} years")
        y -= 60

    c.save()
    return pdf_path
