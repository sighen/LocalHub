# LocalHub SEOUL (Vue 3 버전)

원본 단일 HTML(Vue CDN + 인라인 스크립트) 파일을 **Vite + Vue 3 (Composition API, `<script setup>`)** 기반의
컴포넌트 구조 프로젝트로 변환한 버전입니다.

## 기술 스택
- Vue 3 (`<script setup>`, Composition API)
- Vite
- Tailwind CSS (원본 CDN 방식 → PostCSS 빌드 방식으로 전환)
- Leaflet (npm 패키지로 전환, CDN 스크립트 제거)
- Font Awesome (CDN 유지)

## 실행 방법
```bash
npm install
npm run dev       # http://localhost:5173
npm run build      # 프로덕션 빌드 (dist/)
npm run preview    # 빌드 결과 미리보기
```

## 폴더 구조
```
src/
├── App.vue                     # 탭 전환 + 전역 모달 오케스트레이션
├── main.js                     # 앱 진입점
├── style.css                   # Tailwind 지시문 + 커스텀 스타일(스크롤바, fade-in)
├── data/
│   └── mockData.js             # 이벤트/명소/에디터코스/게시글 목업 데이터
├── composables/
│   ├── useToast.js             # 전역 안내 팝업 (싱글턴)
│   ├── useWeather.js           # 실시간 서울 날씨(Open-Meteo API)
│   ├── useEvents.js            # 캘린더/이벤트 상태 (싱글턴, 홈-캘린더모달 공유)
│   ├── useMap.js                # Leaflet 지도 초기화/모달 상태
│   ├── usePosts.js              # 게시판 CRUD + localStorage 저장
│   └── useChat.js               # AI 챗봇 위젯 로직
└── components/
    ├── layout/                  # NavBar, FooterBar
    ├── home/                    # 홈 탭 (히어로, 이벤트, 명소, 에디터코스, SNS 등)
    ├── community/                # 익명 게시판 + 읽기/쓰기/비밀번호 모달
    ├── modals/                   # 캘린더/지도/토스트 전역 모달
    └── chat/                     # 플로팅 AI 챗봇
```

## 원본 대비 주요 변경 사항

1. **컴포넌트 분리**: 하나의 거대한 `<div id="app">` + 단일 `setup()` 구조를 기능 단위 SFC로 분리했습니다.
2. **상태 공유 패턴**: `selectedDate`(이벤트/캘린더), 토스트 알림처럼 여러 컴포넌트가 공유해야 하는 상태는
   composable 내부를 모듈 스코프 싱글턴으로 만들어 어디서 `useEvents()` / `useToast()`를 호출해도 같은 상태를 참조하도록 했습니다.
   더 큰 앱으로 확장한다면 Pinia 스토어로 옮기는 것을 권장합니다.
3. **`v-model` 기반 폼**: 게시글 작성/수정 폼과 비밀번호 입력은 Vue 3.4의 `defineModel()`을 사용해
   부모-자식 간 양방향 바인딩을 명시적으로 표현했습니다.
4. **Leaflet npm 패키지화**: CDN `<script>` 대신 `import L from 'leaflet'`로 전환했습니다.
5. **AI 챗봇 보안 처리**: 원본은 Google AI Studio 캔버스 전용 환경에서 API 키가 자동 주입되는 것을 전제로
   프론트에서 직접 Gemini API를 호출했습니다. 이는 일반 배포 환경에서는 API 키가 그대로 노출되는 심각한
   보안 문제가 되므로, `src/composables/useChat.js`는 여러분의 백엔드(BFF) 프록시(`VITE_CHAT_API_URL`,
   기본값 `/api/chat`)를 호출하도록 바꿨습니다. 백엔드에서 실제 OpenAI/Gemini 등 LLM API 키를 관리하고
   `{ prompt, system }`을 받아 `{ reply: "..." }` 형태로 응답하는 엔드포인트를 구현해주시면 됩니다.
6. **게시글 저장소**: 원본과 동일하게 `localStorage` 기반으로 유지했습니다 (실서비스 전환 시 REST API로 교체 권장).
7. **잘못된 `v-slot:default` 제거**: 원본 HTML에 실수로 들어간 `v-slot:default v-if="..."` (일반 `<div>`/`<p>`에는
   `v-slot`이 유효하지 않음) 속성은 삭제하고 `v-if`만 남겼습니다.

## 다음 단계 제안
- 상태 관리가 더 커지면 Pinia 도입
- 게시판 API를 실제 백엔드(REST/OpenAPI 스펙)로 교체
- 챗봇 프록시 백엔드 구현 (Node/Express, FastAPI 등) 후 `.env`의 `VITE_CHAT_API_URL` 연결
- Vue Router 도입 시 `currentTab` 상태를 라우팅으로 전환 가능
