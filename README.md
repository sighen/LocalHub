# 지역 관광 커뮤니티 플랫폼

## 디렉토리 구조

```
LocalHub/
├── backend/                        # FastAPI + SQLite
│   ├── app/
│   │   ├── main.py                 # 엔트리포인트, 라우터 등록, CORS
│   │   ├── database.py             # DB 연결/세션
│   │   ├── models.py               # SQLAlchemy 모델
│   │   ├── schemas.py              # Pydantic 스키마
│   │   ├── profanity.py            # 비속어 필터링
│   │   ├── routers/
│   │   │   ├── posts.py                # 게시글 CRUD (커뮤니티)
│   │   │   ├── comments.py             # 댓글 CRUD
│   │   │   ├── chat.py                 # 챗봇 API (스트리밍 응답)
│   │   │   ├── locations.py            # 관광지 조회
│   │   │   ├── cultural_facilities.py  # 문화시설 조회
│   │   │   ├── festivals.py            # 축제 조회
│   │   │   ├── leports.py              # 레포츠 조회
│   │   │   ├── places.py               # 장소 통합 검색
│   │   │   └── weather.py              # 날씨 조회
│   │   └── services/
│   │       ├── chatbot_service.py        # 챗봇 응답 생성/스트리밍 (OpenAI 연동)
│   │       └── place_search_service.py   # 장소 검색 로직
│   ├── data/
│   │   ├── localhub.db             # SQLite DB 파일
│   │   ├── place_search_dictionary.json
│   │   └── seed/                   # TourAPI 원본 시드 데이터(관광지/문화시설/레포츠/축제)
│   ├── scripts/
│   │   └── seed_places.py          # seed 데이터 DB 적재 스크립트
│   ├── requirements.txt
│   ├── .env.example
│   └── Procfile                    # Render 배포용
│
└── frontend/                       # Vue 3 SPA
    ├── src/
    │   ├── components/
    │   │   ├── home/                # 메인 화면 (Hero, 추천 스팟, 커뮤니티 하이라이트 등)
    │   │   ├── explore/             # 관광지 탐색 (지도/목록/필터/상세)
    │   │   ├── festivals/           # 축제 캘린더/목록/상세
    │   │   ├── community/           # 게시판 목록/글쓰기/상세/비밀번호 확인
    │   │   ├── chat/                # 챗봇 위젯
    │   │   ├── weather/             # 날씨 상세
    │   │   ├── layout/              # 네브바/푸터/커서 이펙트
    │   │   └── modals/              # 공용 토스트 알림
    │   ├── composables/             # API 연동 + 상태 로직 (usePosts, useChat, useFestivals 등)
    │   │   └── useRouter.js         # vue-router 없이 URL 기반으로 직접 구현한 경량 라우터
    │   ├── api/client.js            # axios 공통 설정
    │   ├── data/                    # 목데이터, 서울 구 경계 GeoJSON
    │   ├── utils/                   # 이미지 URL, 태그 라벨, confetti 등 유틸
    │   ├── App.vue
    │   └── main.js
    ├── netlify.toml
    └── .env.example
```

## 로컬 실행

### 백엔드
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 값 채우기
uvicorn app.main:app --reload
```
`http://localhost:8000/docs` 에서 Swagger로 API 확인 가능.

### 프론트엔드
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
`http://localhost:5173` 에서 확인.

## 배포

- **백엔드 (Render)**: 
- **프론트엔드 (Netlify)**: 

## 배포 완료

모든 기능 구현을 마치고 배포까지 완료한 상태

- 커뮤니티(게시글/댓글) CRUD: API + 화면 완성 — 비밀번호 평문 대조 방식
- 챗봇: `services/chatbot_service.py`에서 OpenAI(`gpt-5-mini`) 연동 및 응답 구현 완료
- locations/cultural_facilities/festivals/leports/places/weather: 조회 API + 화면 구현 완료, `backend/data/seed/`의 TourAPI 시드 데이터를 `scripts/seed_places.py`로 DB에 적재
- 날씨 정보 연동: 외부 날씨 API 연동 및 권역별 현재 날씨·여행 적합 여부 표시 구현 완료
- 커뮤니티 게시판 추가기능: 조회수 표시, 게시글 검색, 북마크, 좋아요, 이미지 첨부, 태그 기능 구현 완료
- 축제 캘린더: 권역별 축제 일정 캘린더 시각화 구현 완료
- 지도 시각화: API 기반 관광지·맛집 지도 핀 시각화 구현 완료