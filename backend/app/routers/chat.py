import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot_service import run_chat

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        return run_chat(payload.message, db)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Chat API failed")
        raise HTTPException(status_code=500, detail="챗봇 처리 중 오류가 발생했습니다.")
