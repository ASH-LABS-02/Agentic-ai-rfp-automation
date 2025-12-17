from utils.pdf_generator import generate_tender_pdf

def generate_bid_pdf(data: dict) -> str:
    """
    Wrapper agent for PDF generation
    """
    return generate_tender_pdf(
        data=data,
        output_path="generated_pdfs/Bid_Quotation.pdf"
    )
