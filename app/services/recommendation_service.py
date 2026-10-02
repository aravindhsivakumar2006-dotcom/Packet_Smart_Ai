from app.services.platform_service import enrich


def _split_budget(
    budget: float,
    parts: list[tuple[str, float]]
) -> list[dict]:

    return [

        {
            "category": name,
            "amount": round(
                budget * percentage,
                2
            ),
            "percentage": round(
                percentage * 100
            )
        }

        for name, percentage in parts
    ]


def fallback_home(
    data: dict
) -> dict:

    budget = data["budget"]

    rooms = data["rooms"]

    allocations = _split_budget(
        budget,
        [
            ("Furniture", 0.38),
            ("Lighting", 0.18),
            ("Decor", 0.18),
            ("Storage", 0.16),
            ("Contingency", 0.10)
        ]
    )

    items = []

    for room in rooms:

        items.extend([

            {
                "name": f"{room} lighting",
                "category": "Lighting",
                "estimated_price":
                    round(
                        budget * 0.06,
                        2
                    ),
                "platform": "IKEA",
                "query": f"{room} lighting"
            },

            {
                "name": f"{room} decor set",
                "category": "Decor",
                "estimated_price":
                    round(
                        budget * 0.07,
                        2
                    ),
                "platform": "Amazon",
                "query": f"{room} decor"
            }

        ])

    return {

        "summary":
            f"A {data['style']} plan for "
            f"{', '.join(rooms)} with a total "
            f"budget of ₹{budget:,.0f}.",

        "budget": budget,

        "allocations": allocations,

        "recommendations":
            enrich(items[:8]),

        "tips": [

            "Compare dimensions before buying.",

            "Keep 10% as contingency.",

            "Check delivery and return policies."

        ]
    }


def fallback_party(
    data: dict
) -> dict:

    budget = data["budget"]

    guests = data["guests"]

    allocations = _split_budget(
        budget,
        [
            ("Food & Catering", 0.45),
            ("Venue", 0.20),
            ("Decoration", 0.15),
            ("Entertainment", 0.10),
            ("Contingency", 0.10)
        ]
    )

    per_guest = budget / guests

    items = enrich([

        {
            "name":
                f"{data['event_type']} catering package",

            "category": "Food",

            "estimated_price":
                round(
                    budget * 0.45,
                    2
                ),

            "platform": "Swiggy",

            "query":
                f"{data['event_type']} catering"
        },

        {
            "name":
                "Event decoration package",

            "category": "Decoration",

            "estimated_price":
                round(
                    budget * 0.15,
                    2
                ),

            "platform": "Amazon",

            "query":
                "party decoration"
        },

        {
            "name":
                "Nearby venue options",

            "category": "Venue",

            "estimated_price":
                round(
                    budget * 0.20,
                    2
                ),

            "platform": "OYO",

            "query":
                data.get(
                    "venue",
                    "event venue"
                )
        }

    ])

    return {

        "summary":
            f"{data['event_type']} plan for "
            f"{guests} guests at about "
            f"₹{per_guest:,.0f} per guest.",

        "budget": budget,

        "allocations": allocations,

        "recommendations": items,

        "tips": [

            "Confirm guest count before final booking.",

            "Ask vendors about taxes and service charges.",

            "Keep a contingency amount."

        ]
    }


def fallback_jewelry(
    data: dict
) -> dict:

    budget = data["budget"]

    allocations = _split_budget(
        budget,
        [
            ("Main piece", 0.55),
            ("Matching piece", 0.25),
            ("Optional accessory", 0.10),
            ("Contingency", 0.10)
        ]
    )

    items = enrich([

        {
            "name":
                f"{data['style']} necklace set",

            "category":
                "Necklace",

            "estimated_price":
                round(
                    budget * 0.55,
                    2
                ),

            "platform":
                "Amazon",

            "query":
                f"{data['style']} necklace "
                f"{data['occasion']}"
        },

        {
            "name":
                f"{data['style']} earrings",

            "category":
                "Earrings",

            "estimated_price":
                round(
                    budget * 0.25,
                    2
                ),

            "platform":
                "Flipkart",

            "query":
                f"{data['style']} earrings"
        },

        {
            "name":
                "Minimal matching bracelet",

            "category":
                "Bracelet",

            "estimated_price":
                round(
                    budget * 0.10,
                    2
                ),

            "platform":
                "Amazon",

            "query":
                "matching bracelet"
        }

    ])

    return {

        "summary":
            f"Jewelry suggestions for a "
            f"{data['occasion']} occasion, "
            f"using a {data['style']} direction.",

        "budget": budget,

        "allocations": allocations,

        "recommendations": items,

        "tips": [

            "Treat AI image matching as style guidance, "
            "not a guarantee of exact color matching.",

            "Verify material, size, seller rating "
            "and return policy before purchasing."

        ]
    }