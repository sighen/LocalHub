import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest
from app.services.chatbot_service import resolve_chat_places, stream_chat_answer

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    # 검색 조건 추출 + DB 조회는 여기서 동기적으로 끝내서, 실패 시 평범한
    # HTTP 에러 응답으로 내려간다. 실제 답변 생성만 스트리밍으로 전환한다.
    try:
        db_places = resolve_chat_places(payload.message, payload.history, db)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Chat search failed")
        raise HTTPException(status_code=500, detail="챗봇 처리 중 오류가 발생했습니다.")

    return StreamingResponse(
        stream_chat_answer(payload.message, db_places, payload.history),
        media_type="text/event-stream",
    )
