from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.LocationListItem])
def list_locations(
    category: Optional[str] = None,
    region: Optional[str] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Location)
    if category:
        query = query.filter(models.Location.category == category)
    if region:
        query = query.filter(models.Location.region == region)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            (models.Location.title.like(like)) | (models.Location.overview.like(like))
        )

    results = []
    for loc in query.all():
        image = loc.images[0] if loc.images else None
        results.append(
            schemas.LocationListItem(
                content_id=loc.content_id,
                title=loc.title,
                category=loc.category,
                region=loc.region,
                address=loc.address,
                lat=loc.lat,
                lng=loc.lng,
                image=image,
            )
        )
    return results


@router.get("/{content_id}", response_model=schemas.LocationDetail)
def get_location(content_id: str, db: Session = Depends(get_db)):
    loc = db.query(models.Location).filter(models.Location.content_id == content_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return loc
