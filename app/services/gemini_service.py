import json
from..config import settings

MOCK_HOME = [
    {"name": "IKEA HEMNES Ceiling Light", "platform": "IKEA", "price": 2499, "link": "https://www.ikea.com/in/en/search/?q=ceiling+light", "reason": "Energy efficient, perfect for living room"},
    {"name": "Amazon Basics Dining Table 4 Seater", "platform": "Amazon", "price": 8999, "link": "https://www.amazon.in/s?k=dining+table", "reason": "Compact and budget-friendly"},
    {"name": "Flipkart Smart LED Bulb Pack of 4", "platform": "Flipkart", "price": 1299, "link": "https://www.flipkart.com/search?q=led+bulb", "reason": "Color changing, smart control"},
    {"name": "IKEA MALM Bed Frame", "platform": "IKEA", "price": 12990, "link": "https://www.ikea.com/in/en/search/?q=bed", "reason": "Modern minimal design"}
]

MOCK_PARTY = [
    {"category": "Catering", "name": "Swiggy Party Feast Box", "platform": "Swiggy", "price": 5000, "details": "Veg + Non-veg combo for 20 people"},
    {"category": "Decoration", "name": "Zomato Balloon & Lights Setup", "platform": "Zomato", "price": 3000, "details": "Theme based decoration with lights"},
    {"category": "Venue", "name": "OYO Party Hall AC", "platform": "OYO", "price": 7000, "details": "AC hall with basic seating and sound"},
    {"category": "Entertainment", "name": "DJ + Photographer Combo", "platform": "Swiggy", "price": 4000, "details": "3 hour DJ and photography"}
]

MOCK_JEWELRY = [
    {"name": "Gold Plated Necklace Set", "platform": "Amazon", "price": 1999, "link": "https://www.amazon.in/s?k=gold+necklace", "style_match": "Perfect for wedding, matches red saree"},
    {"name": "Silver Jhumka Earrings", "platform": "Flipkart", "price": 899, "link": "https://www.flipkart.com/search?q=jhumka", "style_match": "Traditional look, matches saree"},
    {"name": "Kundan Choker Set", "platform": "Amazon", "price": 3499, "link": "https://www.amazon.in/s?k=kundan+choker", "style_match": "Royal look for engagement"},
]

def get_gemini_model():
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "test_key" or len(settings.GEMINI_API_KEY) < 20:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        print(f"Gemini init failed: {e}")
        return None

def generate_home_recommendations(budget: float, rooms: str, preferences: str):
    model = get_gemini_model()
    if model is None:
        per_item = budget / 4
        result = []
        for item in MOCK_HOME:
            result.append({**item, "allocated_budget": round(per_item,2)})
        total = sum([i['price'] for i in result])
        return {"budget": budget, "rooms": rooms, "preferences": preferences, "recommendations": result, "total_estimated": total, "saving_tip": f"You save Rs.{budget-total:.0f} with these picks! Ideal for {preferences}"}

    prompt = f"""
    You are PocketSmart AI Home Expert. User budget Rs.{budget}, Rooms: {rooms}, Preferences: {preferences}
    Recommend 4 products from IKEA, Amazon, Flipkart with name, platform, price (must be within budget), link (real search link), reason.
    Return ONLY JSON: {{"recommendations": [{{"name":..., "platform":..., "price":int, "link":..., "reason":...}}], "total_estimated":int, "saving_tip":...}}
    """
    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip().replace("```json","").replace("```","")
        return json.loads(text)
    except Exception as e:
        print(e)
        return {"budget": budget, "rooms": rooms, "preferences": preferences, "recommendations": MOCK_HOME, "total_estimated": 25787, "saving_tip": "Smart picks within budget"}

def generate_party_recommendations(budget: float, guests: int, event_type: str, venue_type: str):
    model = get_gemini_model()
    if model is None:
        return {"budget": budget, "guests": guests, "event_type": event_type, "venue_type": venue_type, "recommendations": MOCK_PARTY, "allocation": {"catering": budget*0.5, "decoration": budget*0.25, "venue": budget*0.15, "entertainment": budget*0.1}}

    prompt = f"Party budget Rs.{budget}, guests {guests}, event {event_type}, venue {venue_type}. Allocate budget and recommend. Return JSON with recommendations array having category, name, platform, price, details and allocation object."
    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip().replace("```json","").replace("```","")
        return json.loads(text)
    except:
        return {"budget": budget, "guests": guests, "event_type": event_type, "venue_type": venue_type, "recommendations": MOCK_PARTY, "allocation": {"catering": budget*0.5, "decoration": budget*0.3, "venue": budget*0.2}}

def generate_jewelry_recommendations(budget: float, occasion: str, style: str, image_info: str = ""):
    model = get_gemini_model()
    if model is None:
        return {"budget": budget, "occasion": occasion, "style": style, "recommendations": MOCK_JEWELRY, "style_tip": f"For {occasion}, go with {style} style. Outfit: {image_info}. These pieces match perfectly!"}

    prompt = f"Jewelry budget Rs.{budget}, occasion {occasion}, style {style}. Outfit info: {image_info}. Recommend jewelry. Return JSON."
    try:
        resp = model.generate_content(prompt)
        text = resp.text.strip().replace("```json","").replace("```","")
        return json.loads(text)
    except:
        return {"budget": budget, "occasion": occasion, "style": style, "recommendations": MOCK_JEWELRY, "style_tip": "Fallback styling tip"}