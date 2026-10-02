from urllib.parse import quote_plus


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={query}",

    "Flipkart":
        "https://www.flipkart.com/search?q={query}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={query}",

    "Swiggy":
        "https://www.swiggy.com/search?query={query}",

    "Zomato":
        "https://www.zomato.com/search?q={query}",

    "OYO":
        "https://www.oyorooms.com/search/?location={query}"
}


def search_link(
    platform: str,
    query: str
) -> str:

    template = PLATFORMS.get(
        platform
    )

    if not template:

        return "#"

    return template.format(
        query=quote_plus(query)
    )


def enrich(
    items: list[dict]
) -> list[dict]:

    for item in items:

        platform = item.get(
            "platform",
            "Amazon"
        )

        query = item.get(
            "query"
        ) or item.get(
            "name",
            ""
        )

        item["link"] = search_link(
            platform,
            query
        )

    return items