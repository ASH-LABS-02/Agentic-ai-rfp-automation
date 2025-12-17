import pdfplumber
from utils.openai_client import ask_llm

def sales_agent_extract_summary(pdf_path: str) -> str:
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:5]:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    prompt = f"""
You are a B2B Sales Agent analysing an RFP.

Extract ONLY the following fields and return STRICT JSON:
- product_family
- voltage_grade
- standard
- cores
- cross_section_sqmm
- test_requirements

Document text:
{text}
"""

    return ask_llm(
        "You extract structured technical requirements from RFPs.",
        prompt
    )
