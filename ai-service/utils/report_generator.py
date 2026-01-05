from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_report(data):
    # Create reports folder if not exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/plant_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI-Driven Plant Health Report")
    y -= 40

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated on: {datetime.now()}")
    y -= 30

    c.drawString(50, y, f"Prediction: {data['prediction']}")
    y -= 20

    c.drawString(50, y, f"Confidence: {data['confidence']}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Explanation:")
    y -= 20

    c.setFont("Helvetica", 11)
    for reason in data["explanation"]:
        c.drawString(70, y, f"- {reason}")
        y -= 18

    y -= 20

    if data.get("plant_message"):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Plant Message:")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(70, y, data["plant_message"]["plant_message"])
        y -= 20

    c.showPage()
    c.save()

    return filename
