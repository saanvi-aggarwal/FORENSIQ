from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_pdf_report(profile, insights):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("FORENSIQ - Investigation Analysis Report",
                  styles["Title"])
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph("Dataset Overview", styles["Heading2"])
    )

    data = [
        ["Metric", "Value"],
        ["Total Records", profile["total_rows"]],
        ["Total Columns", profile["total_columns"]],
        ["Duplicate Rows", profile["duplicate_rows"]],
        ["Missing Cells", profile["missing_cells"]]
    ]

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    content.append(table)

    content.append(Spacer(1, 20))

    content.append(
        Paragraph("Automated Observations", styles["Heading2"])
    )

    for insight in insights:
        content.append(
            Paragraph(f"- {insight}", styles["BodyText"])
        )
        content.append(Spacer(1, 8))

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Disclaimer: This report contains exploratory "
            "statistical observations only. It does not establish "
            "identity, guilt, causation or forensic conclusions.",
            styles["Italic"]
        )
    )

    document.build(content)

    buffer.seek(0)

    return buffer
