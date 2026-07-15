from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ---------- Posts ----------
class PostCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    password: str
    place_content_id: Optional[str] = None


class PostUpdate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    password: str
    place_content_id: Optional[str] = None


class PostDelete(BaseModel):
    password: str


class PostListItem(BaseModel):
    id: int
    title: str
    category: Optional[str]
    view_count: int
    comment_count: int
    created_at: datetime
    place_content_id: Optional[str] = None
    place_title: Optional[str] = None
    place_content_type_id: Optional[int] = None

    class Config:
        from_attributes = True


class PostDetail(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]
    view_count: int
    created_at: datetime
    updated_at: datetime
    place_content_id: Optional[str] = None
    place_title: Optional[str] = None
    place_content_type_id: Optional[int] = None

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[PostListItem]


# ---------- Comments ----------
class CommentCreate(BaseModel):
    content: str
    password: str


class CommentDelete(BaseModel):
    password: str


class CommentItem(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("message must not be blank")
        return stripped


class ChatSearchCondition(BaseModel):
    district_name: Optional[str] = None
    content_type_ids: List[int] = Field(default_factory=list)
    overview_keywords: List[str] = Field(default_factory=list)
    event_date_from: Optional[str] = None
    event_date_to: Optional[str] = None
    limit: int = Field(default=5, ge=1, le=5)


class AIRecommendation(BaseModel):
    content_id: str
    reason: str


class AIFinalAnswer(BaseModel):
    answer: str
    recommendations: List[AIRecommendation] = Field(default_factory=list)


class ChatPlace(BaseModel):
    content_id: str
    content_type_id: int
    title: str
    district_name: Optional[str] = None
    addr1: Optional[str] = None
    addr2: Optional[str] = None
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    overview: Optional[str] = None
    event_start_date: Optional[str] = None
    event_end_date: Optional[str] = None
    reason: str


class ChatResponse(BaseModel):
    answer: str
    places: List[ChatPlace] = Field(default_factory=list)


# ---------- Locations ----------
class LocationListItem(BaseModel):
    content_id: str
    title: str
    category: str
    region: Optional[str]
    address: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    image: Optional[str] = None

    class Config:
        from_attributes = True


class LocationDetail(BaseModel):
    content_id: str
    title: str
    category: str
    overview: Optional[str]
    address: Optional[str]
    tel: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    images: Optional[List[str]] = None

    class Config:
        from_attributes = True


class PlaceItem(BaseModel):
    content_id: str
    content_type_id: int
    title: str
    region: str
    addr1: Optional[str]
    addr2: Optional[str]
    district_name: Optional[str]
    zipcode: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    image_url: Optional[str]
    thumbnail_url: Optional[str]
    tel: Optional[str]
    tel_name: Optional[str]
    homepage_url: Optional[str]
    overview: Optional[str]
    category_l1: Optional[str]
    category_l2: Optional[str]
    category_l3: Optional[str]
    copyright_type: Optional[str]
    event_start_date: Optional[str]
    event_end_date: Optional[str]

    class Config:
        from_attributes = True


class PlaceListResponse(BaseModel):
    items: List[PlaceItem]
    page: int
    size: int
    total: int


class PlaceFacetValue(BaseModel):
    value: str
    count: int


class PlaceFacetsResponse(BaseModel):
    districts: List[PlaceFacetValue]
    tags: List[PlaceFacetValue]


class PlacePoint(BaseModel):
    content_id: str
    title: str
    district_name: Optional[str]
    category_l1: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        from_attributes = True


class NearbyPlacesResponse(BaseModel):
    festival: Optional[PlaceItem] = None
    attraction: Optional[PlaceItem] = None


# ---------- Festivals ----------
class FestivalListItem(BaseModel):
    content_id: str
    title: str
    region: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    summary: Optional[str]

    class Config:
        from_attributes = True


class FestivalDetail(FestivalListItem):
    overview: Optional[str]
    fee: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    images: Optional[List[str]] = None


# ---------- Weather ----------
class WeatherCurrent(BaseModel):
    temp: float
    icon: str
    status: str
