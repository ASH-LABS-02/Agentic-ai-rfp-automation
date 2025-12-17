import json
import re

from agents.sales_agent import sales_agent_extract_summary
from agents.technical_agent import technical_agent_match
from agents.pricing_agent import pricing_agent
from agents.justification_agent import justification_agent
from agents.confidence_agent import confidence_agent
from agents.pdf_agent import generate_bid_pdf


def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("Invalid JSON from LLM")
    return json.loads(match.group())


def master_agent(pdf_path: str):
    # -------- SALES AGENT --------
    sales_output = sales_agent_extract_summary(pdf_path)
    rfp_specs = extract_json(sales_output)

    # -------- TECHNICAL AGENT --------
    technical_recommendations = technical_agent_match(rfp_specs)

    # -------- PRICING AGENT --------
    pricing = pricing_agent(
        technical_recommendations,
        rfp_specs.get("test_requirements", [])
    )

    # -------- JUSTIFICATION AGENT --------
    justification = justification_agent(
        rfp_specs,
        technical_recommendations
    )

    # -------- CONFIDENCE AGENT --------
    confidence = confidence_agent(
        technical_recommendations,
        pricing
    )

    return {
        "rfp_summary": rfp_specs,
        "technical_recommendations": technical_recommendations,
        "pricing": pricing,
        "justification": justification,
        "confidence": confidence
    }
