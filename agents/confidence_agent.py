def confidence_agent(technical_recommendations: list, pricing: dict) -> str:
    """
    Determines bid confidence based on:
    - Average technical match %
    - Whether pricing is complete
    """

    if not technical_recommendations:
        return "LOW"

    # ---- Technical confidence ----
    avg_match = sum(
        r.get("spec_match_percent", 0)
        for r in technical_recommendations
    ) / len(technical_recommendations)

    # ---- Pricing confidence ----
    has_material_cost = pricing.get("material_cost", 0) > 0

    # ---- Decision logic ----
    if avg_match >= 85 and has_material_cost:
        return "HIGH"

    if avg_match >= 65:
        return "MEDIUM"

    return "LOW"
