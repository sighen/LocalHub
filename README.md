# 지역 관광 커뮤니티 플랫폼

## 디렉토리 구조

```
project/
├── backend/                # A 담당 — FastAPI + SQLite
│   ├── app/
│   │   ├── main.py         # 엔트리포인트, 라우터 등록
│   │   ├── database.py     # DB 연결
│   │   ├── models.py       # SQLAlchemy 모델
│   │   ├── schemas.py      # Pydantic 스키마
│   │   └── routers/
│   │       ├── posts.py       # 게시글 CRUD (커뮤니티)
│   │       ├── comments.py    # 댓글 CRUD
│   │       ├── chat.py        # 챗봇 (OpenAI 연동 예정)
│   │       ├── locations.py   # 관광지/문화시설 등 조회
│   │       └── festivals.py   # 축제 조회
│   ├── requirements.txt
│   ├── .env.example
│   └── Procfile             # Render 배포용
│
└── frontend/                # B(메인/디자인) + C(기능/게시판) — Vue 3 SPA
    ├── src/
    │   ├── views/
    │   │   ├── MainView.vue             # B 담당
    │   │   ├── RecommendView.vue        # 관광지 추천
    │   │   ├── FestivalView.vue         # 축제
    │   │   ├── CommunityListView.vue    # 게시판 목록
    │   │   ├── CommunityDetailView.vue  # 게시글 상세
    │   │   └── CommunityWriteView.vue   # 글쓰기
    │   ├── components/
    │   │   └── ChatWidget.vue           # 챗봇 팝업
    │   ├── api/client.js                # axios 공통 설정
    │   └── router/index.js
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

- **백엔드 (Render)**: `backend/` 를 루트로 새 Web Service 생성 → Build Command `pip install -r requirements.txt`, Start Command는 `Procfile` 사용 → 환경변수(.env 내용)를 Render 대시보드에 등록
- **프론트엔드 (Netlify)**: `frontend/` 를 루트로 새 사이트 생성 → Build Command `npm run build`, Publish directory `dist` (netlify.toml에 이미 설정됨) → 환경변수 `VITE_API_BASE_URL`을 Render 백엔드 URL로 설정

## 현재 상태

- 커뮤니티(게시글/댓글) CRUD: API + 화면 기본 골격 완성 — 비밀번호 평문 대조 방식 (교육 목적)
- 챗봇: 엔드포인트/화면 뼈대만 존재, OpenAI 연동은 `backend/app/routers/chat.py` TODO 참고
- locations/festivals: 조회 API + 화면 뼈대 존재, TourAPI·비짓서울 동기화 배치는 별도 작성 필요
- 이 상태로 B, C는 각자 화면에 디자인/기능을 바로 이어서 작업 가능 (mock 데이터 대신 실제 빈 API를 호출하도록 이미 연결되어 있음)
