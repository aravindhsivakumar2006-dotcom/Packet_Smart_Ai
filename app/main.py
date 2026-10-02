from fastapi import FastAPI, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
import json, shutil

from.database import Base, engine, get_db
from.models import User, RecommendationHistory
from.auth import hash_password, verify_password, create_access_token
from.dependencies import get_current_user
from.services.gemini_service import generate_home_recommendations, generate_party_recommendations, generate_jewelry_recommendations

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="PocketSmart AI")
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        user = None
    return templates.TemplateResponse(request, "index.html", {"user": user})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {})

@app.post("/register")
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse(request, "register.html", {"error": "Username already exists"})
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(request, "register.html", {"error": "Email already exists"})
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(request, "login.html", {"error": "Invalid credentials"})
    token = create_access_token({"sub": user.username})
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400, samesite="lax")
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    history = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == user.id).order_by(RecommendationHistory.created_at.desc()).limit(10).all()
    return templates.TemplateResponse(request, "dashboard.html", {"user": user, "history": history})

@app.get("/home-planner", response_class=HTMLResponse)
async def home_planner_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse(request, "home_planner.html", {"user": user})

@app.post("/generate-home", response_class=HTMLResponse)
async def generate_home(request: Request, total_budget: float = Form(...), rooms: str = Form(...), preferences: str = Form(""), db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    result = generate_home_recommendations(total_budget, rooms, preferences)
    hist = RecommendationHistory(user_id=user.id, category="home", budget=total_budget, input_data=json.dumps({"rooms": rooms, "preferences": preferences}), result=json.dumps(result))
    db.add(hist)
    db.commit()
    return templates.TemplateResponse(request, "recommendations.html", {"user": user, "category": "Home Interior", "result": result, "budget": total_budget})

@app.get("/party-planner", response_class=HTMLResponse)
async def party_planner_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse(request, "party_planner.html", {"user": user})

@app.post("/generate-party", response_class=HTMLResponse)
async def generate_party(request: Request, total_budget: float = Form(...), guest_count: int = Form(...), event_type: str = Form(...), venue_type: str = Form(...), db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    result = generate_party_recommendations(total_budget, guest_count, event_type, venue_type)
    hist = RecommendationHistory(user_id=user.id, category="party", budget=total_budget, input_data=json.dumps({"guests": guest_count, "event_type": event_type, "venue": venue_type}), result=json.dumps(result))
    db.add(hist)
    db.commit()
    return templates.TemplateResponse(request, "recommendations.html", {"user": user, "category": "Party", "result": result, "budget": total_budget})

@app.get("/jewelry-planner", response_class=HTMLResponse)
async def jewelry_planner_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse(request, "jewelry_planner.html", {"user": user})

@app.post("/generate-jewelry", response_class=HTMLResponse)
async def generate_jewelry(request: Request, total_budget: float = Form(...), occasion: str = Form(...), style: str = Form(...), outfit_image: UploadFile = File(None), db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    image_info = ""
    if outfit_image and outfit_image.filename:
        file_path = UPLOAD_DIR / outfit_image.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(outfit_image.file, f)
        image_info = f"User uploaded outfit: {outfit_image.filename}"
    result = generate_jewelry_recommendations(total_budget, occasion, style, image_info)
    hist = RecommendationHistory(user_id=user.id, category="jewelry", budget=total_budget, input_data=json.dumps({"occasion": occasion, "style": style}), result=json.dumps(result))
    db.add(hist)
    db.commit()
    return templates.TemplateResponse(request, "jewelry_planner.html", {"user": user, "category": "Jewelry", "result": result, "budget": total_budget})

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = get_current_user(request, db)
    except:
        return RedirectResponse("/login", status_code=302)
    history = db.query(RecommendationHistory).filter(RecommendationHistory.user_id == user.id).order_by(RecommendationHistory.created_at.desc()).all()
    return templates.TemplateResponse(request, "history.html", {"user": user, "history": history})