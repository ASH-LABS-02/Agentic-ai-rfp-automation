from fastapi import FastAPI, Query
import requests
import os
import uuid

from agents.master_agent import master_agent
from agents.pdf_agent import generate_bid_pdf

app = FastAPI(
    title="Agentic AI RFP System",
    version="1.0.0"
)


@app.post("/evaluate-tender")
async def evaluate_tender(
    tender_url: str = Query(..., description="Public URL of Tender PDF")
):
    """
    Fetch tender PDF from mock website URL,
    run agentic evaluation,
    generate professional bid PDF.
    """

    # ---------- CREATE STORAGE ----------
    os.makedirs("downloaded_tenders", exist_ok=True)

    # ---------- DOWNLOAD PDF ----------
    local_pdf_path = f"downloaded_tenders/tender_{uuid.uuid4().hex}.pdf"

    try:
        response = requests.get(tender_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        return {
            "error": "Failed to download tender PDF",
            "details": str(e)
        }

    with open(local_pdf_path, "wb") as f:
        f.write(response.content)

    # ---------- RUN AGENTIC PIPELINE ----------
    result = master_agent(local_pdf_path)

    # ---------- GENERATE BID PDF ----------
    pdf_path = generate_bid_pdf(result)
    result["quotation_pdf"] = pdf_path

    # ---------- META INFO (OPTIONAL, BUT IMPRESSIVE) ----------
    result["source_tender_url"] = tender_url
    result["downloaded_pdf_path"] = local_pdf_path

    return result
