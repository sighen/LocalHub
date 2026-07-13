import os

from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest):
    """
    TODO(C):
    1. payload.message에서 intent 분류 (관광지 추천 / 축제 일정 / 맛집 / 게시글 검색 등)
    2. intent에 맞는 locations/festivals/posts 데이터 조회
    3. 조회 결과를 컨텍스트로 넣어 OpenAI API 호출 후 자연어 응답 생성
    4. 관련 장소/게시글이 있으면 references로 함께 반환
    지금은 프론트 개발이 막히지 않도록 더미 응답을 반환합니다.
    """
    if not OPENAI_API_KEY:
        # 키 미설정 상태에서도 프론트 개발이 진행될 수 있도록 더미 응답 유지
        pass

    return ChatResponse(
        reply=f"'{payload.message}'에 대한 답변입니다. (더미 응답 — OpenAI 연동 예정)",
        references=[],
    )
