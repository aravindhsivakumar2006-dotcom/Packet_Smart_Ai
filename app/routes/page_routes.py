from fastapi import (
    APIRouter,
    Request
)

from fastapi.responses import HTMLResponse

from fastapi.templating import (
    Jinja2Templates
)

from app.config import TEMPLATES_DIR


router = APIRouter()


templates = Jinja2Templates(
    directory=str(
        TEMPLATES_DIR
    )
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def index(
    request: Request
):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        }
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        "register.html",
        {
            "request": request
        }
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request
):

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request
        }
    )


@router.get(
    "/planner/home",
    response_class=HTMLResponse
)
def home_page(
    request: Request
):

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request
        }
    )


@router.get(
    "/planner/party",
    response_class=HTMLResponse
)
def party_page(
    request: Request
):

    return templates.TemplateResponse(
        "party.html",
        {
            "request": request
        }
    )


@router.get(
    "/planner/jewelry",
    response_class=HTMLResponse
)
def jewelry_page(
    request: Request
):

    return templates.TemplateResponse(
        "jewelry.html",
        {
            "request": request
        }
    )


@router.get(
    "/history",
    response_class=HTMLResponse
)
def history_page(
    request: Request
):

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request
        }
    )