from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.FestivalListItem])
def list_festivals(
    region: Optional[str] = None,
    month: Optional[str] = None,  # YYYY-MM
    db: Session = Depends(get_db),
):
    query = db.query(models.Festival)
    if region:
        query = query.filter(models.Festival.region == region)
    if month:
        query = query.filter(models.Festival.start_date.like(f"{month}%"))
    return query.order_by(models.Festival.start_date.asc()).all()


@router.get("/{content_id}", response_model=schemas.FestivalDetail)
def get_festival(content_id: str, db: Session = Depends(get_db)):
    festival = (
        db.query(models.Festival).filter(models.Festival.content_id == content_id).first()
    )
    if not festival:
        raise HTTPException(status_code=404, detail="축제 정보를 찾을 수 없습니다.")
    return festival
