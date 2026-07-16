from datetime import date
from math import atan2, cos, radians, sin, sqrt
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()

# 관광지 추천 페이지의 카테고리 탭 → TourAPI contentTypeId
CATEGORY_CONTENT_TYPE = {
    "관광지": 12,
    "문화시설": 14,
    "레포츠": 28,
}

EXPLORE_CONTENT_TYPES = tuple(CATEGORY_CONTENT_TYPE.values())
FESTIVAL_CONTENT_TYPE = 15

MAX_POINTS = 2000


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius_km = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * earth_radius_km * atan2(sqrt(a), sqrt(1 - a))


def _filtered_query(
    db: Session,
    type: str,
    q: Optional[str] = None,
    district: Optional[List[str]] = None,
    tag: Optional[str] = None,
):
    content_type_id = CATEGORY_CONTENT_TYPE.get(type)
    if content_type_id is None:
        raise HTTPException(status_code=400, detail="지원하지 않는 카테고리입니다.")

    query = db.query(models.Place).filter(models.Place.content_type_id == content_type_id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Place.title.like(like)) | (models.Place.overview.like(like))
        )
    if district:
        query = query.filter(models.Place.district_name.in_(district))
    if tag:
        query = query.filter(models.Place.category_l1 == tag)
    return query


@router.get("", response_model=schemas.PlaceListResponse)
def list_locations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    q: Optional[str] = None,
    type: str = Query("관광지", description="관광지 | 문화시설 | 레포츠"),
    district: Optional[List[str]] = Query(None, description="복수 선택 가능 (예: 강남구, 마포구)"),
    tag: Optional[str] = None,
    sort: str = Query("title", description="title | latest"),
    db: Session = Depends(get_db),
):
    query = _filtered_query(db, type, q, district, tag)

    total = query.count()
    if sort == "latest":
        query = query.order_by(models.Place.source_modified_at.desc().nullslast())
    else:
        query = query.order_by(models.Place.title.asc())

    items = query.offset((page - 1) * size).limit(size).all()
    return schemas.PlaceListResponse(items=items, page=page, size=size, total=total)


@router.get("/points", response_model=List[schemas.PlacePoint])
def list_location_points(
    q: Optional[str] = None,
    type: str = Query("관광지", description="관광지 | 문화시설 | 레포츠"),
    district: Optional[List[str]] = Query(None, description="복수 선택 가능 (예: 강남구, 마포구)"),
    tag: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """지도에 모든 핀을 한 번에 찍기 위한 경량 엔드포인트 (페이지네이션 없음)."""
    query = _filtered_query(db, type, q, district, tag)
    query = query.filter(models.Place.latitude.isnot(None), models.Place.longitude.isnot(None))
    return query.order_by(models.Place.title.asc()).limit(MAX_POINTS).all()


@router.get("/facets", response_model=schemas.PlaceFacetsResponse)
def get_location_facets(
    type: str = Query("관광지", description="관광지 | 문화시설 | 레포츠"),
    db: Session = Depends(get_db),
):
    content_type_id = CATEGORY_CONTENT_TYPE.get(type)
    if content_type_id is None:
        raise HTTPException(status_code=400, detail="지원하지 않는 카테고리입니다.")

    base = db.query(models.Place).filter(models.Place.content_type_id == content_type_id)

    district_rows = (
        base.with_entities(models.Place.district_name, func.count(models.Place.id))
        .filter(models.Place.district_name.isnot(None))
        .group_by(models.Place.district_name)
        .order_by(models.Place.district_name.asc())
        .all()
    )
    tag_rows = (
        base.with_entities(models.Place.category_l1, func.count(models.Place.id))
        .filter(models.Place.category_l1.isnot(None))
        .group_by(models.Place.category_l1)
        .order_by(models.Place.category_l1.asc())
        .all()
    )

    return schemas.PlaceFacetsResponse(
        districts=[schemas.PlaceFacetValue(value=v, count=c) for v, c in district_rows],
        tags=[schemas.PlaceFacetValue(value=v, count=c) for v, c in tag_rows],
    )


@router.get("/{content_id}", response_model=schemas.PlaceItem)
def get_location(content_id: str, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.content_id == content_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
    return place


@router.get("/{content_id}/nearby", response_model=schemas.NearbyPlacesResponse)
def get_nearby_places(content_id: str, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.content_id == content_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")

    def nearest_of(content_type_ids, ongoing_only=False):
        if place.latitude is None or place.longitude is None:
            return None
        query = db.query(models.Place).filter(
            models.Place.content_type_id.in_(content_type_ids),
            models.Place.content_id != content_id,
            models.Place.latitude.isnot(None),
            models.Place.longitude.isnot(None),
        )
        if ongoing_only:
            today = date.today().strftime("%Y%m%d")
            query = query.filter(
                models.Place.event_start_date.isnot(None),
                models.Place.event_end_date.isnot(None),
                models.Place.event_start_date <= today,
                models.Place.event_end_date >= today,
            )
        candidates = query.all()
        if not candidates:
            return None
        return min(
            candidates,
            key=lambda c: _haversine_km(place.latitude, place.longitude, c.latitude, c.longitude),
        )

    return schemas.NearbyPlacesResponse(
        festival=nearest_of([FESTIVAL_CONTENT_TYPE], ongoing_only=True),
        attraction=nearest_of(EXPLORE_CONTENT_TYPES),
    )
