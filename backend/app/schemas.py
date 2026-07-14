from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


# ---------- Posts ----------
class PostCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    password: str


class PostUpdate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    password: str


class PostDelete(BaseModel):
    password: str


class PostListItem(BaseModel):
    id: int
    title: str
    category: Optional[str]
    view_count: int
    comment_count: int
    created_at: datetime

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


# ---------- Chat ----------
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None


class ChatReference(BaseModel):
    type: str  # "location" | "post"
    id: str
    title: str


class ChatResponse(BaseModel):
    reply: str
    references: Optional[List[ChatReference]] = None


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
    restaurants: List[PlaceItem]
    lodgings: List[PlaceItem]


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
