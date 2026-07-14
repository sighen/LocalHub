from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=schemas.PlaceListResponse)
def list_locations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    q: Optional[str] = None,
    district: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Place).filter(models.Place.content_type_id == 12)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Place.title.like(like)) | (models.Place.overview.like(like))
        )
    if district:
        query = query.filter(models.Place.district_name == district)
    if category:
        query = query.filter(models.Place.category_l3 == category)

    total = query.count()
    items = (
        query.order_by(models.Place.title.asc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return schemas.PlaceListResponse(items=items, page=page, size=size, total=total)
