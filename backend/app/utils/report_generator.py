from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

from utils.report_management import ensure_reports_dir, unique_report_filename


def generate_pdf_report(data, reports_dir: str = "reports", filename: str | None = None):
    """Generate a PDF report and return the absolute/relative file path.

    - `reports_dir`: folder where PDFs are stored
    - `filename`: optional explicit filename; if not provided, a unique filename is generated
    """
    try:
        required_fields = ["prediction", "confidence", "explanation"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        ensure_reports_dir(reports_dir)

        if not filename:
            filename = unique_report_filename("plant_health_report")

        file_path = os.path.join(reports_dir, filename)

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Plant Health Report")
        y -= 40

        c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Prediction:")
        c.setFont("Helvetica", 11)
        c.drawString(150, y, str(data['prediction']))
        y -= 25

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Confidence:")
        c.setFont("Helvetica", 11)
        c.drawString(150, y, str(data['confidence']))
        y -= 35

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Explanation:")
        y -= 20

        c.setFont("Helvetica", 11)
        for reason in data["explanation"]:
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 11)
            c.drawString(70, y, f"- {reason}")
            y -= 18

        y -= 20

        if data.get("plant_message"):
            if y < 150:
                c.showPage()
                y = height - 50
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Plant Message:")
            y -= 20

            c.setFont("Helvetica", 11)
            plant_msg = data["plant_message"].get("plant_message", "")
            
            words = plant_msg.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                if c.stringWidth(test_line, "Helvetica", 11) < (width - 140):
                    line = test_line
                else:
                    c.drawString(70, y, line)
                    y -= 18
                    line = word + " "
                    if y < 100:
                        c.showPage()
                        y = height - 50
                        c.setFont("Helvetica", 11)
            if line:
                c.drawString(70, y, line)

        c.showPage()
        c.save()
        return file_path
    
    except Exception as e:
        raise Exception(f"Failed to generate PDF report: {str(e)}")
