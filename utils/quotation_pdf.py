from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import date


def generate_quotation(data: dict, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("<b>QUOTATION</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Header
    elements.append(Paragraph(
        f"Date: {date.today()}<br/>Customer: RFP Client",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # Product Table
    table_data = [["SKU", "Unit Price", "Qty", "Cost"]]

    for p in data["pricing"]["products"]:
        table_data.append([
            p["sku"],
            f"₹ {p['unit_price']}",
            p["quantity"],
            f"₹ {p['cost']}"
        ])

    table = Table(table_data, colWidths=[160, 80, 60, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    elements.append(Paragraph("<b>Product Pricing</b>", styles["Heading2"]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Cost Summary
    material = data["pricing"]["material_cost"]
    test = data["pricing"]["test_cost"]
    subtotal = material + test
    gst = round(subtotal * 0.18, 2)
    grand_total = subtotal + gst

    summary = f"""
    <b>Material Cost:</b> ₹ {material}<br/>
    <b>Test Cost:</b> ₹ {test}<br/>
    <b>Subtotal:</b> ₹ {subtotal}<br/>
    <b>GST (18%):</b> ₹ {gst}<br/>
    <b>Grand Total:</b> ₹ {grand_total}
    """

    elements.append(Paragraph("<b>Cost Summary</b>", styles["Heading2"]))
    elements.append(Paragraph(summary, styles["Normal"]))

    doc.build(elements)
