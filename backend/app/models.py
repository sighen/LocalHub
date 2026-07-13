from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    password = Column(String, nullable=False)  # 평문 저장 — 교육 목적 의도된 설계
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    content = Column(Text, nullable=False)
    password = Column(String, nullable=False)  # 평문 저장 — 교육 목적 의도된 설계
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="comments")


class Location(Base):
    """관광지/문화시설/레포츠/숙박/쇼핑/음식 — TourAPI + 비짓서울 동기화 데이터"""

    __tablename__ = "locations"

    content_id = Column(String, primary_key=True)
    source = Column(String, nullable=False)  # 'tourapi' | 'visitseoul'
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    region = Column(String, nullable=True)
    address = Column(String, nullable=True)
    overview = Column(Text, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    tel = Column(String, nullable=True)
    images = Column(JSON, nullable=True)  # URL 리스트


class Festival(Base):
    __tablename__ = "festivals"

    content_id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    title = Column(String, nullable=False)
    region = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    overview = Column(Text, nullable=True)
    summary = Column(String, nullable=True)
    fee = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    images = Column(JSON, nullable=True)
