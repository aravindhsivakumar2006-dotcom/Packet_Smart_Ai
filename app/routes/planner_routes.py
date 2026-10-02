import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from app.config import MAX_IMAGE_BYTES

from app.database import get_db

from app.dependencies import get_current_user

from app.models import (
    RecommendationHistory,
    User
)

from app.schemas import (
    HomeRequest,
    PartyRequest
)

from app.services.gemini_service import generate

from app.services.platform_service import enrich


router = APIRouter(
    prefix="/api/planners",
    tags=["planners"]
)


def save_history(
    db,
    user,
    planner,
    request_data,
    result
):

    row = RecommendationHistory(

        user_id=user.id,

        planner=planner,

        request_json=json.dumps(
            request_data,
            ensure_ascii=False
        ),

        result_json=json.dumps(
            result,
            ensure_ascii=False
        )
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    return row.id


@router.post("/home")
def home(
    data: HomeRequest,
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    result, source = generate(
        "home",
        data.model_dump()
    )

    result["recommendations"] = enrich(
        result.get(
            "recommendations",
            []
        )
    )

    history_id = save_history(
        db,
        user,
        "home",
        data.model_dump(),
        result
    )

    return {

        "planner": "home",

        "source": source,

        "history_id": history_id,

        **result
    }


@router.post("/party")
def party(
    data: PartyRequest,
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    result, source = generate(
        "party",
        data.model_dump()
    )

    result["recommendations"] = enrich(
        result.get(
            "recommendations",
            []
        )
    )

    history_id = save_history(
        db,
        user,
        "party",
        data.model_dump(),
        result
    )

    return {

        "planner": "party",

        "source": source,

        "history_id": history_id,

        **result
    }


@router.post("/jewelry")
async def jewelry(

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(
        "Elegant"
    ),

    outfit_description: str = Form(
        ""
    ),

    outfit_image: UploadFile | None = File(
        None
    ),

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    if budget <= 0 or budget > 10_000_000:

        raise HTTPException(
            422,
            "Budget must be between ₹1 and ₹1,00,00,000"
        )

    if len(
        occasion.strip()
    ) < 2:

        raise HTTPException(
            422,
            "Please enter an occasion"
        )

    image_bytes = None

    mime_type = "image/jpeg"

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if (
            outfit_image.content_type
            not in allowed
        ):

            raise HTTPException(
                415,
                "Only JPG, PNG, and WEBP images are supported"
            )

        image_bytes = await outfit_image.read()

        if len(image_bytes) > MAX_IMAGE_BYTES:

            raise HTTPException(
                413,
                "Image must be 5 MB or smaller"
            )

        mime_type = (
            outfit_image.content_type
        )

    data = {

        "budget": budget,

        "occasion":
            occasion.strip(),

        "style":
            style.strip(),

        "outfit_description":
            outfit_description.strip()
    }

    result, source = generate(

        "jewelry",

        data,

        image_bytes,

        mime_type
    )

    result["recommendations"] = enrich(
        result.get(
            "recommendations",
            []
        )
    )

    history_id = save_history(

        db,

        user,

        "jewelry",

        data,

        result
    )

    return {

        "planner": "jewelry",

        "source": source,

        "history_id": history_id,

        **result
    }