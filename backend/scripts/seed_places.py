import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

from app.database import Base, SessionLocal, engine
from app.models import Place

BASE_DIR = Path(__file__).resolve().parents[1]
SEED_DIR = BASE_DIR / "data" / "seed"

SEED_FILES = [
    ("관광지", SEED_DIR / "서울_관광지_detailCommon.json", 12),
    ("축제", SEED_DIR / "서울_축제공연행사_detailCommon.json", 15),
]

URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")
HREF_PATTERN = re.compile(r"href=[\"']([^\"']+)[\"']", re.IGNORECASE)


def blank_to_none(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def to_float(value: Any) -> float | None:
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: Any) -> int | None:
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_datetime(value: Any) -> datetime | None:
    value = blank_to_none(value)
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d%H%M%S")
    except ValueError:
        return None


def extract_district_name(addr1: str | None) -> str | None:
    addr1 = blank_to_none(addr1)
    if not addr1:
        return None
    for part in addr1.split():
        if part.endswith("구"):
            return part
    return None


def extract_homepage_url(homepage: str | None) -> str | None:
    homepage = blank_to_none(homepage)
    if not homepage:
        return None

    text = unescape(homepage)
    href_match = HREF_PATTERN.search(text)
    if href_match:
        return href_match.group(1).strip()

    url_match = URL_PATTERN.search(text)
    if url_match:
        return url_match.group(0).strip()

    return None


def load_items(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"{path}의 items가 배열이 아닙니다.")
    return items


def map_item(item: dict[str, Any], default_type_id: int) -> dict[str, Any]:
    addr1 = blank_to_none(item.get("addr1"))
    homepage = blank_to_none(item.get("homepage"))
    return {
        "content_id": blank_to_none(item.get("contentid")),
        "content_type_id": to_int(item.get("contenttypeid")) or default_type_id,
        "region": "서울",
        "title": blank_to_none(item.get("title")),
        "addr1": addr1,
        "addr2": blank_to_none(item.get("addr2")),
        "district_name": extract_district_name(addr1),
        "district_code": blank_to_none(item.get("lDongSignguCd")),
        "zipcode": blank_to_none(item.get("zipcode")),
        "longitude": to_float(item.get("mapx")),
        "latitude": to_float(item.get("mapy")),
        "image_url": blank_to_none(item.get("firstimage")),
        "thumbnail_url": blank_to_none(item.get("firstimage2")),
        "tel": blank_to_none(item.get("tel")),
        "tel_name": blank_to_none(item.get("telname")),
        "homepage": homepage,
        "homepage_url": extract_homepage_url(homepage),
        "overview": blank_to_none(item.get("overview")),
        "category_l1": blank_to_none(item.get("lclsSystm1")),
        "category_l2": blank_to_none(item.get("lclsSystm2")),
        "category_l3": blank_to_none(item.get("lclsSystm3")),
        "copyright_type": blank_to_none(item.get("cpyrhtDivCd")),
        "source_created_at": to_datetime(item.get("createdtime")),
        "source_modified_at": to_datetime(item.get("modifiedtime")),
    }


def should_update(existing: Place, incoming: dict[str, Any]) -> bool:
    incoming_modified = incoming.get("source_modified_at")
    if existing.source_modified_at is None:
        return True
    if incoming_modified is None:
        return False
    return incoming_modified > existing.source_modified_at


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    stats: dict[str, dict[str, int]] = {}

    try:
        for label, path, default_type_id in SEED_FILES:
            inserted = 0
            updated = 0
            for raw_item in load_items(path):
                data = map_item(raw_item, default_type_id)
                if not data["content_id"] or not data["title"]:
                    continue

                existing = (
                    db.query(Place)
                    .filter(Place.content_id == data["content_id"])
                    .first()
                )
                if existing is None:
                    db.add(Place(**data))
                    inserted += 1
                    continue

                if should_update(existing, data):
                    for key, value in data.items():
                        setattr(existing, key, value)
                    updated += 1

            stats[label] = {"inserted": inserted, "updated": updated}

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    verify_db = SessionLocal()
    try:
        total = verify_db.query(Place).count()
    finally:
        verify_db.close()

    for label in ("관광지", "축제"):
        print(f"{label} 신규: {stats[label]['inserted']}")
        print(f"{label} 업데이트: {stats[label]['updated']}")
    print(f"총 저장 데이터: {total}")


if __name__ == "__main__":
    seed()
