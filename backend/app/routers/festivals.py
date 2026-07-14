from calendar import monthrange
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


def normalize_festival_date(value: str) -> tuple[str, str]:
    normalized = value.replace("-", "")
    if len(normalized) == 6 and normalized.isdigit():
        year = int(normalized[:4])
        month = int(normalized[4:6])
        if month < 1 or month > 12:
            raise ValueError
        last_day = monthrange(year, month)[1]
        start = f"{year:04d}{month:02d}01"
        end = f"{year:04d}{month:02d}{last_day:02d}"
        return start, end

    if len(normalized) == 8 and normalized.isdigit():
        datetime.strptime(normalized, "%Y%m%d")
        datetime_value = normalized
        return datetime_value, datetime_value

    raise ValueError


@router.get("", response_model=schemas.PlaceListResponse)
def list_festivals(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    q: Optional[str] = None,
    district: Optional[str] = None,
    category: Optional[str] = None,
    date: Optional[str] = Query(
        None,
        description="Festival date filter. Supports YYYYMM, YYYYMMDD, YYYY-MM, YYYY-MM-DD.",
    ),
    db: Session = Depends(get_db),
):
    query = db.query(models.Place).filter(models.Place.content_type_id == 15)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Place.title.like(like)) | (models.Place.overview.like(like))
        )
    if district:
        query = query.filter(models.Place.district_name == district)
    if category:
        query = query.filter(models.Place.category_l3 == category)
    if date:
        try:
            start_date, end_date = normalize_festival_date(date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="date는 YYYYMM, YYYYMMDD, YYYY-MM, YYYY-MM-DD 형식이어야 합니다.",
            )
        query = query.filter(
            models.Place.event_start_date <= end_date,
            models.Place.event_end_date >= start_date,
        )

    total = query.count()
    items = (
        query.order_by(models.Place.source_modified_at.desc().nullslast())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return schemas.PlaceListResponse(items=items, page=page, size=size, total=total)
