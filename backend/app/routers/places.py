from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("/{content_id}", response_model=schemas.PlaceItem)
def get_place(content_id: str, db: Session = Depends(get_db)):
    place = (
        db.query(models.Place).filter(models.Place.content_id == content_id).first()
    )
    if not place:
        raise HTTPException(status_code=404, detail="장소 정보를 찾을 수 없습니다.")
    return place
