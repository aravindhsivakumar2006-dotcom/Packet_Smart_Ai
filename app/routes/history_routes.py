import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies import get_current_user

from app.models import (
    RecommendationHistory,
    User
)


router = APIRouter(
    prefix="/api/history",
    tags=["history"]
)


@router.get("")
def history(
    user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    rows = db.query(
        RecommendationHistory
    ).filter_by(
        user_id=user.id
    ).order_by(
        RecommendationHistory.created_at.desc()
    ).all()

    return [

        {

            "id": row.id,

            "planner":
                row.planner,

            "created_at":
                row.created_at.isoformat(),

            "request":
                json.loads(
                    row.request_json
                ),

            "result":
                json.loads(
                    row.result_json
                )

        }

        for row in rows
    ]


@router.get("/{history_id}")
def history_detail(

    history_id: int,

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    row = db.query(
        RecommendationHistory
    ).filter_by(

        id=history_id,

        user_id=user.id

    ).first()

    if not row:

        raise HTTPException(
            404,
            "History item not found"
        )

    return {

        "id": row.id,

        "planner":
            row.planner,

        "created_at":
            row.created_at.isoformat(),

        "request":
            json.loads(
                row.request_json
            ),

        "result":
            json.loads(
                row.result_json
            )
    }