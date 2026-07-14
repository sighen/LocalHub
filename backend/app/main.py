from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import (
    chat,
    comments,
    cultural_facilities,
    festivals,
    leports,
    locations,
    places,
    posts,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="지역 관광 커뮤니티 플랫폼 API")

# 개발 중에는 전체 허용, 배포 시 Netlify 도메인으로 제한 권장
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router, prefix="/api/posts", tags=["community-posts"])
app.include_router(comments.router, prefix="/api", tags=["community-comments"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(locations.router, prefix="/api/locations", tags=["locations"])
app.include_router(festivals.router, prefix="/api/festivals", tags=["festivals"])
app.include_router(
    cultural_facilities.router,
    prefix="/api/cultural-facilities",
    tags=["cultural-facilities"],
)
app.include_router(leports.router, prefix="/api/leports", tags=["leports"])
app.include_router(places.router, prefix="/api/places", tags=["places"])


@app.get("/")
def health_check():
    return {"status": "ok"}
