import pandas as pd
import re

PRICES = pd.read_csv("data/pricing.csv").fillna("")

PRICES["type"] = PRICES["type"].astype(str)
PRICES["sku"] = PRICES["sku"].astype(str)
PRICES["name"] = PRICES["name"].astype(str)


def to_python_type(value):
    if hasattr(value, "item"):
        return value.item()
    return value


def extract_size_from_sku(sku: str):
    match = re.search(r"-(\d+)$", sku)
    return int(match.group(1)) if match else None


def pricing_agent(recommendations, tests):
    material_cost = 0
    test_cost = 0
    products = []
    quantity = 1000  # meters

    # ---------- PRODUCT COST ----------
    for rec in recommendations:
        sku = rec["sku"]
        size = extract_size_from_sku(sku)

        row = PRICES[
            (PRICES["type"] == "PRODUCT") &
            (PRICES["sku"] == sku)
        ]

        # fallback: size-only
        if row.empty and size:
            row = PRICES[
                (PRICES["type"] == "PRODUCT") &
                (PRICES["sku"].str.endswith(f"-{size}"))
            ]

        if not row.empty:
            unit_price = to_python_type(row.iloc[0]["price"])
            cost = unit_price * quantity

            material_cost += cost

            products.append({
                "sku": sku,
                "unit_price": unit_price,
                "quantity": quantity,
                "cost": cost,
                "pricing_note": "Exact / nearest SKU pricing"
            })

    # ---------- TEST COST ----------
    for test in tests:
        test_lower = test.lower()

        row = PRICES[
            (PRICES["type"] == "TEST") &
            (PRICES["name"].str.lower().str.contains(test_lower, regex=False))
        ]

        if not row.empty:
            test_cost += to_python_type(row.iloc[0]["price"])

    return {
        "products": products,
        "material_cost": material_cost,
        "test_cost": test_cost,
        "total_cost": material_cost + test_cost
    }
