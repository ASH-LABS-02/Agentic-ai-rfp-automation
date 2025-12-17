from utils.openai_client import ask_llm

def justification_agent(rfp_summary: dict, technical_recommendations: list):
    """
    Generates human-readable justification for each selected SKU
    """
    justifications = {}

    for rec in technical_recommendations:
        sku = rec["sku"]

        prompt = f"""
You are a senior electrical tender engineer.

Explain WHY the below SKU is suitable for the RFP.
Use bullet points.
Focus on voltage, standards, cross section, application.
Do NOT mention AI.

RFP:
{rfp_summary}

SKU:
{sku}
"""

        response = ask_llm(
            "You explain technical tender decisions clearly.",
            prompt
        )

        justifications[sku] = response

    return justifications
