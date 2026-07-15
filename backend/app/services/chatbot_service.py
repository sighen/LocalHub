import json
import logging
import os
from functools import lru_cache
from typing import Any

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


FINAL_ANSWER_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "chat_final_answer",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "answer": {"type": "string"},
                "recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "content_id": {"type": "string"},
                            "reason": {"type": "string"},
                        },
                        "required": ["content_id", "reason"],
                    },
                },
            },
            "required": ["answer", "recommendations"],
        },
    },
}


def run_chat(message: str, db: Session) -> schemas.ChatResponse:
    dictionary = load_search_dictionary()
    condition = extract_search_condition(message, dictionary)
    validated_condition = validate_search_condition(condition, dictionary)
    db_places = search_places(db, validated_condition)

    final_answer = build_final_answer(message, db_places)
    return combine_answer_with_db_places(final_answer, db_places)


def extract_search_condition(
    message: str,
    dictionary: SearchDictionary,
) -> schemas.ChatSearchCondition:
    client = _get_openai_client_or_503()
    model = _get_model()
    prompt_payload = dictionary.prompt_payload

    try:
        response = client.chat.completions.create(
            model=model,
            response_format=SEARCH_CONDITION_SCHEMA,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 LocalHub 관광 검색 조건 추출기다. "
                        "반드시 제공된 검색 사전 값만 사용하고 JSON만 반환한다. "
                        "SQL을 만들지 말고 새로운 지역명, 키워드, content_type_id를 만들지 마라."
                    ),
                },
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


def build_final_answer(
    message: str,
    db_places: list[models.Place],
) -> schemas.AIFinalAnswer:
    if not db_places:
        return schemas.AIFinalAnswer(
            answer="조건에 맞는 장소를 찾지 못했습니다. 지역이나 목적을 조금 다르게 알려주시면 다시 찾아드릴게요.",
            recommendations=[],
        )

    client = _get_openai_client_or_503()
    model = _get_model()
    place_payload = places_for_openai(db_places)

    try:
        response = client.chat.completions.create(
            model=model,
            response_format=FINAL_ANSWER_SCHEMA,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "너는 LocalHub 장소 추천 답변 작성기다. "
                        "반드시 전달받은 DB 장소만 사용한다. content_id를 수정하거나 새로 만들지 않는다. "
                        "답변과 각 장소 추천 이유만 자연스러운 한국어로 작성한다."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "message": message,
                            "places": place_payload,
                        },
                        ensure_ascii=False,
                    ),
                },
            ],
            timeout=20,
        )
        content = response.choices[0].message.content or "{}"
        return schemas.AIFinalAnswer.model_validate_json(content)
    except (OpenAIError, IndexError, ValidationError, ValueError):
        logger.exception("OpenAI final answer failed; using DB fallback answer")
        return _fallback_final_answer(message, db_places)


def combine_answer_with_db_places(
    ai_answer: schemas.AIFinalAnswer,
    db_places: list[models.Place],
) -> schemas.ChatResponse:
    places_by_id = {place.content_id: place for place in db_places}
    reasons_by_id: dict[str, str] = {}
    for recommendation in ai_answer.recommendations:
        if recommendation.content_id in places_by_id and recommendation.content_id not in reasons_by_id:
            reasons_by_id[recommendation.content_id] = recommendation.reason

    selected_places = []
    if reasons_by_id:
        for place in db_places:
            if place.content_id in reasons_by_id:
                selected_places.append(place_to_chat_place(place, reasons_by_id[place.content_id]))
    else:
        for place in db_places:
            selected_places.append(place_to_chat_place(place, _default_reason(place)))

    return schemas.ChatResponse(answer=ai_answer.answer, places=selected_places)


def _fallback_final_answer(message: str, db_places: list[models.Place]) -> schemas.AIFinalAnswer:
    if not db_places:
        return schemas.AIFinalAnswer(
            answer="조건에 맞는 장소를 찾지 못했습니다. 다른 지역이나 목적을 알려주시면 다시 찾아드릴게요.",
            recommendations=[],
        )
    return schemas.AIFinalAnswer(
        answer="요청하신 조건에 맞는 장소를 찾아봤습니다.",
        recommendations=[
            schemas.AIRecommendation(content_id=place.content_id, reason=_default_reason(place))
            for place in db_places
        ],
    )


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
