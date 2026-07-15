import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas


VALID_CONTENT_TYPE_IDS = {12, 14, 15, 28}
DATE_RE = re.compile(r"^\d{8}$")
DICTIONARY_PATH = Path(__file__).resolve().parents[2] / "data" / "place_search_dictionary.json"


@dataclass(frozen=True)
class SearchDictionary:
    content_type_ids: set[int]
    district_names: set[str]
    overview_keywords: set[str]
    prompt_payload: dict


@lru_cache(maxsize=1)
def load_search_dictionary() -> SearchDictionary:
    try:
        raw = json.loads(DICTIONARY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="검색 사전 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="검색 사전 JSON 형식이 올바르지 않습니다.")

    try:
        content_type = raw["content_type"]
        district_names = set(raw["district_name"])
        overview_keywords = set(raw["overview"]["keywords"])
    except (KeyError, TypeError):
        raise HTTPException(status_code=500, detail="검색 사전 구조가 올바르지 않습니다.")

    content_type_ids = {int(key) for key in content_type.keys()} & VALID_CONTENT_TYPE_IDS
    prompt_payload = {
        "content_type": {
            key: {
                "name": value.get("name"),
                "aliases": value.get("aliases", []),
            }
            for key, value in content_type.items()
            if int(key) in content_type_ids
        },
        "district_name": sorted(district_names),
        "overview_keywords": sorted(overview_keywords),
    }
    return SearchDictionary(
        content_type_ids=content_type_ids,
        district_names=district_names,
        overview_keywords=overview_keywords,
        prompt_payload=prompt_payload,
    )


def validate_search_condition(
    condition: schemas.ChatSearchCondition,
    dictionary: SearchDictionary,
) -> schemas.ChatSearchCondition:
    district_name = condition.district_name
    if district_name not in dictionary.district_names:
        district_name = None

    content_type_ids = []
    seen_type_ids = set()
    for content_type_id in condition.content_type_ids:
        if content_type_id in dictionary.content_type_ids and content_type_id not in seen_type_ids:
            content_type_ids.append(content_type_id)
            seen_type_ids.add(content_type_id)

    overview_keywords = []
    seen_keywords = set()
    for keyword in condition.overview_keywords:
        if keyword in dictionary.overview_keywords and keyword not in seen_keywords:
            overview_keywords.append(keyword)
            seen_keywords.add(keyword)
        if len(overview_keywords) >= 5:
            break

    event_date_from = _valid_date_or_none(condition.event_date_from)
    event_date_to = _valid_date_or_none(condition.event_date_to)
    if event_date_from and event_date_to and event_date_from > event_date_to:
        event_date_from, event_date_to = event_date_to, event_date_from

    limit = max(1, min(condition.limit, 5))
    return schemas.ChatSearchCondition(
        district_name=district_name,
        content_type_ids=content_type_ids,
        overview_keywords=overview_keywords,
        event_date_from=event_date_from,
        event_date_to=event_date_to,
        limit=limit,
    )


def search_places(
    db: Session,
    condition: schemas.ChatSearchCondition,
) -> list[models.Place]:
    fallback_steps = [
        (condition.district_name, condition.content_type_ids, condition.overview_keywords),
        (condition.district_name, [], condition.overview_keywords),
        (None, condition.content_type_ids, condition.overview_keywords),
        (None, [], condition.overview_keywords),
        (condition.district_name, condition.content_type_ids, []),
        (condition.district_name, [], []),
        (None, condition.content_type_ids, []),
    ]

    for district_name, content_type_ids, keywords in fallback_steps:
        places = _run_place_query(
            db=db,
            district_name=district_name,
            content_type_ids=content_type_ids,
            keywords=keywords,
            event_date_from=condition.event_date_from,
            event_date_to=condition.event_date_to,
            limit=condition.limit,
        )
        if places:
            return places
    return []


def place_to_chat_place(place: models.Place, reason: str) -> schemas.ChatPlace:
    return schemas.ChatPlace(
        content_id=place.content_id,
        content_type_id=place.content_type_id,
        title=place.title,
        district_name=place.district_name,
        addr1=place.addr1,
        addr2=place.addr2,
        image_url=place.image_url,
        thumbnail_url=place.thumbnail_url,
        overview=place.overview,
        event_start_date=place.event_start_date,
        event_end_date=place.event_end_date,
        reason=reason,
    )


def places_for_openai(places: Iterable[models.Place]) -> list[dict]:
    payload = []
    for place in places:
        overview = place.overview or ""
        payload.append(
            {
                "content_id": place.content_id,
                "content_type_id": place.content_type_id,
                "title": place.title,
                "district_name": place.district_name,
                "addr1": place.addr1,
                "addr2": place.addr2,
                "overview": overview[:700],
                "image_url": place.image_url,
                "event_start_date": place.event_start_date,
                "event_end_date": place.event_end_date,
            }
        )
    return payload


def _run_place_query(
    db: Session,
    district_name: str | None,
    content_type_ids: list[int],
    keywords: list[str],
    event_date_from: str | None,
    event_date_to: str | None,
    limit: int,
) -> list[models.Place]:
    query = db.query(models.Place)
    if district_name:
        query = query.filter(models.Place.district_name == district_name)
    if content_type_ids:
        query = query.filter(models.Place.content_type_id.in_(content_type_ids))
    if keywords:
        keyword_filters = []
        for keyword in keywords:
            pattern = f"%{keyword}%"
            keyword_filters.append(models.Place.overview.ilike(pattern))
            keyword_filters.append(models.Place.title.ilike(pattern))
        query = query.filter(or_(*keyword_filters))
    if event_date_from or event_date_to:
        start_date = event_date_from or event_date_to
        end_date = event_date_to or event_date_from
        query = query.filter(
            models.Place.event_start_date.isnot(None),
            models.Place.event_end_date.isnot(None),
            models.Place.event_start_date <= end_date,
            models.Place.event_end_date >= start_date,
        )

    # Fetch a modest candidate pool, then score in Python. This keeps the SQL simple and
    # prevents model-generated data from influencing query construction.
    candidates = query.limit(80).all()
    scored = [(_score_place(place, keywords), place) for place in candidates]
    scored.sort(key=lambda item: (-item[0], item[1].title or "", item[1].content_id))
    return [place for _, place in scored[:limit]]


def _score_place(place: models.Place, keywords: list[str]) -> int:
    if not keywords:
        return 0
    title = place.title or ""
    overview = place.overview or ""
    score = 0
    for keyword in keywords:
        lowered_keyword = keyword.lower()
        if lowered_keyword in title.lower():
            score += 2
        if lowered_keyword in overview.lower():
            score += 1
    return score


def _valid_date_or_none(value: str | None) -> str | None:
    if not value:
        return None
    return value if DATE_RE.match(value) else None
