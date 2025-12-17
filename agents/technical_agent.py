import json

with open("data/product_specs.json", encoding="utf-8") as f:
    PRODUCT_DB = json.load(f)


def normalize_sizes(values):
    """Convert list of sizes to integers safely"""
    cleaned = []
    for v in values:
        try:
            cleaned.append(int(float(v)))
        except Exception:
            pass
    return cleaned


def calculate_spec_match(product: dict, rfp: dict) -> float:
    score = 0
    total = 6  # Increased weight for better differentiation

    # ---------- PRODUCT FAMILY ----------
    pf = rfp.get("product_family", "").lower()
    if "cable" in pf:
        score += 1

    # ---------- VOLTAGE ----------
    if product.get("voltage_grade") and rfp.get("voltage_grade"):
        if product["voltage_grade"] in rfp["voltage_grade"]:
            score += 1

    # ---------- STANDARD (ANY MATCH) ----------
    rfp_standards = rfp.get("standard", [])
    if isinstance(rfp_standards, list):
        if any(product.get("standard", "") in s for s in rfp_standards):
            score += 1

    # ---------- CROSS SECTION (EXACT OR NEAR MATCH) ----------
    product_size = product.get("cross_section_sqmm")
    rfp_sizes = normalize_sizes(rfp.get("cross_section_sqmm", []))

    if product_size in rfp_sizes:
        score += 2  # exact size match (strong)
    elif any(abs(product_size - s) <= 10 for s in rfp_sizes):
        score += 1  # near match (fallback)

    # ---------- CORES ----------
    if isinstance(rfp.get("cores"), int):
        if product.get("cores") == rfp["cores"]:
            score += 1

    return round((score / total) * 100, 2)


def technical_agent_match(rfp_specs: dict):
    results = []

    for product in PRODUCT_DB:
        if "sku" not in product:
            continue

        score = calculate_spec_match(product, rfp_specs)

        if score >= 30:  # realistic enterprise threshold
            results.append({
                "sku": product["sku"],
                "spec_match_percent": score
            })

    results.sort(key=lambda x: x["spec_match_percent"], reverse=True)
    return results[:3]
