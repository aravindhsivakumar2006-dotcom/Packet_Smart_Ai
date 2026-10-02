from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Cookie
)

from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    hash_password,
    verify_password
)

from app.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from app.database import get_db

from app.models import User

from app.schemas import (
    LoginRequest,
    RegisterRequest
)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    email = data.email.strip().lower()

    existing = db.query(User).filter(
        User.email == email
    ).first()

    if existing:

        raise HTTPException(
            409,
            "An account with this email already exists"
        )

    user = User(
        email=email,
        password_hash=hash_password(
            data.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    token = create_access_token(
        user.id
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {

        "message":
            "Registration successful",

        "user": {
            "id": user.id,
            "email": user.email
        }
    }


@router.post("/login")
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email ==
        data.email.strip().lower()
    ).first()

    if (
        not user
        or not verify_password(
            data.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            401,
            "Invalid email or password"
        )

    token = create_access_token(
        user.id
    )

    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return {

        "message":
            "Login successful",

        "user": {
            "id": user.id,
            "email": user.email
        }
    }


@router.post("/logout")
def logout(
    response: Response
):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message": "Logged out"
    }


@router.get("/me")
def me(
    access_token: str | None = Cookie(
        default=None
    ),
    db: Session = Depends(get_db)
):

    if not access_token:

        raise HTTPException(
            401,
            "Not logged in"
        )

    from app.auth import (
        decode_access_token
    )

    try:

        user_id = decode_access_token(
            access_token
        )

    except Exception:

        raise HTTPException(
            401,
            "Invalid session"
        )

    user = db.get(
        User,
        user_id
    )

    if not user:

        raise HTTPException(
            401,
            "User not found"
        )

    return {
        "id": user.id,
        "email": user.email
    }