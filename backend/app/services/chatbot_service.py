import json
import logging
import os
from functools import lru_cache

from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.services.place_search_service import (
    SearchDictionary,
    load_search_dictionary,
    place_to_chat_place,
    places_for_openai,
    search_places,
    validate_search_condition,
)


logger = logging.getLogger(__name__)
DEFAULT_MODEL = "gpt-5-mini"


SEARCH_CONDITION_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "chat_search_condition",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "district_name": {"type": ["string", "null"]},
                "content_type_ids": {
                    "type": "array",
                    "items": {"type": "integer", "enum": [12, 14, 15, 28]},
                },
                "overview_keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": 5,
                },
                "event_date_from": {"type": ["string", "null"]},
                "event_date_to": {"type": ["string", "null"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": 5},
            },
            "required": [
                "district_name",
                "content_type_ids",
                "overview_keywords",
                "event_date_from",
                "event_date_to",
                "limit",
            ],
        },
    },
}


def resolve_chat_places(
    message: str,
    history: list[schemas.ChatHistoryTurn],
    db: Session,
) -> list[models.Place]:
    dictionary = load_search_dictionary()
    condition = extract_search_condition(message, dictionary, history)
    validated_condition = validate_search_condition(condition, dictionary)
    return search_places(db, validated_condition)


def _history_messages(history: list[schemas.ChatHistoryTurn]) -> list[dict]:
    # 이전 대화 문맥("거기", "그중에서 저렴한 곳은" 같은 후속 질문)을 이해할 수
    # 있도록 지난 대화를 그대로 이전 turn으로 끼워 넣는다. 최근 6턴(3번 왕복)만
    # 사용해 토큰/지연 시간이 계속 늘어나지 않게 한다.
    return [{"role": turn.role, "content": turn.content} for turn in history[-6:]]


def extract_search_condition(
    message: str,
    dictionary: SearchDictionary,
    history: list[schemas.ChatHistoryTurn] | None = None,
) -> schemas.ChatSearchCondition:
    client = _get_openai_client_or_503()
    model = _get_model()
    prompt_payload = dictionary.prompt_payload

    try:
        response = client.chat.completions.create(
            model=model,
            response_format=SEARCH_CONDITION_SCHEMA,
            # gpt-5-mini는 기본적으로 답하기 전에 안 보이는 "추론" 토큰을 쓰는
            # 추론 모델이라, 이 옵션 없이는 단순 JSON 추출에도 몇 초씩 걸린다.
            # reasoning_effort를 최소로 낮춰서 그 추론 단계를 사실상 꺼버린다.
            extra_body={"reasoning_effort": "minimal"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 LocalHub 관광 검색 조건 추출기다. "
                        "반드시 제공된 검색 사전 값만 사용하고 JSON만 반환한다. "
                        "SQL을 만들지 말고 새로운 지역명, 키워드, content_type_id를 만들지 마라. "
                        "이전 대화가 있다면 참고해서 '거기', '그중에서' 같은 후속 질문의 의미를 파악한다."
                    ),
                },
                *_history_messages(history or []),
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "message": message,
                            "dictionary": prompt_payload,
                            "rules": {
                                "district_name": "dictionary.district_name 중 하나 또는 null",
                                "content_type_ids": [12, 14, 15, 28],
                                "overview_keywords": "dictionary.overview_keywords 중 최대 5개",
                                "date_format": "YYYYMMDD 또는 null",
                                "limit": "1~5, 기본 5",
                            },
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            timeout=20,
        )
    except OpenAIError:
        logger.exception("OpenAI search condition call failed")
        raise HTTPException(status_code=502, detail="검색 조건 생성에 실패했습니다.")

    try:
        content = response.choices[0].message.content or "{}"
        return schemas.ChatSearchCondition.model_validate_json(content)
    except (IndexError, ValidationError, ValueError):
        logger.exception("Invalid OpenAI search condition response")
        raise HTTPException(status_code=502, detail="검색 조건 응답 형식이 올바르지 않습니다.")


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def stream_chat_answer(
    message: str,
    db_places: list[models.Place],
    history: list[schemas.ChatHistoryTurn] | None = None,
):
    """OpenAI 답변을 토큰 단위로 SSE 청크로 흘려보낸다.

    답변을 구조화된(JSON schema) 형식으로 한 번에 받으면 스트리밍 도중에는
    깨진 JSON 조각만 보이게 되므로, 이 호출만은 response_format 없이 평문으로
    받는다. 장소별 추천 이유는 DB 조회 결과만으로 결정하고(_default_reason),
    답변 스트림이 끝난 뒤 한 번에 함께 보낸다.
    """
    if not db_places:
        answer = "조건에 맞는 장소를 찾지 못했습니다. 지역이나 목적을 조금 다르게 알려주시면 다시 찾아드릴게요."
        yield _sse({"type": "chunk", "text": answer})
        yield _sse({"type": "done", "places": []})
        return

    places = [place_to_chat_place(place, _default_reason(place)) for place in db_places]

    try:
        client = _get_openai_client_or_503()
        model = _get_model()
        place_payload = places_for_openai(db_places)

        stream = client.chat.completions.create(
            model=model,
            # 여기도 마찬가지로 추론 단계를 꺼서, 스트리밍이 시작되기 전에
            # 안 보이는 "생각 중" 지연이 생기지 않게 한다.
            extra_body={"reasoning_effort": "minimal"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 LocalHub 장소 추천 답변 작성기다. "
                        "전달받은 DB 장소를 근거로 사용자 질문에 자연스러운 한국어로 답한다. "
                        "장소 이름을 새로 만들지 말고 전달받은 장소만 언급한다. "
                        "마크다운 없이 일반 문장으로 답한다. "
                        "이전 대화가 있다면 자연스럽게 이어서 답한다."
                    ),
                },
                *_history_messages(history or []),
                {
                    "role": "user",
                    "content": json.dumps(
                        {"message": message, "places": place_payload},
                        ensure_ascii=False,
                    ),
                },
            ],
            stream=True,
            timeout=20,
        )
        for event in stream:
            delta = event.choices[0].delta.content if event.choices else None
            if delta:
                yield _sse({"type": "chunk", "text": delta})
    except OpenAIError:
        logger.exception("OpenAI streaming final answer failed; using DB fallback answer")
        yield _sse({"type": "chunk", "text": "요청하신 조건에 맞는 장소를 찾아봤습니다."})

    yield _sse({"type": "done", "places": [place.model_dump() for place in places]})


def _default_reason(place: models.Place) -> str:
    if place.overview:
        return "장소 설명과 조건이 잘 맞아 추천할 만합니다."
    return "요청하신 조건으로 조회된 장소입니다."


@lru_cache(maxsize=1)
def _get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=20)


def _get_openai_client_or_503() -> OpenAI:
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    try:
        api_key.encode("ascii")
    except UnicodeEncodeError:
        api_key = ""
    if not api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY가 설정되어 있지 않습니다.")
    return _get_openai_client()


def _get_model() -> str:
    configured = (os.getenv("OPENAI_MODEL") or DEFAULT_MODEL).strip()
    return configured if configured == DEFAULT_MODEL else DEFAULT_MODEL
