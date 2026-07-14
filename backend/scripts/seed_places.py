import json
import re
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any

from sqlalchemy import inspect, text

from app.database import Base, SessionLocal, engine
from app.models import Place

BASE_DIR = Path(__file__).resolve().parents[1]
SEED_DIR = BASE_DIR / "data" / "seed"

TARGET_TYPES = {
    12: "\uad00\uad11\uc9c0",
    15: "\ucd95\uc81c\uacf5\uc5f0\ud589\uc0ac",
    14: "\ubb38\ud654\uc2dc\uc124",
    28: "\ub808\ud3ec\uce20",
}

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
        if part.endswith("\uad6c"):
            return part
    return None


def extract_homepage_url(homepage: str | None) -> str | None:
    homepage = blank_to_none(homepage)
    if not homepage:
        return None

    text_value = unescape(homepage)
    href_match = HREF_PATTERN.search(text_value)
    if href_match:
        return href_match.group(1).strip()

    url_match = URL_PATTERN.search(text_value)
    if url_match:
        return url_match.group(0).strip()

    return None


def load_seed_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"{path} items must be a list.")
    return payload


def iter_seed_payloads() -> list[tuple[Path, dict[str, Any]]]:
    payloads = []
    for path in sorted(SEED_DIR.glob("*.json")):
        payload = load_seed_payload(path)
        content_type_id = to_int(payload.get("contentTypeId"))
        if content_type_id in TARGET_TYPES:
            payloads.append((path, payload))
    return payloads


def ensure_place_columns() -> None:
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("places")}
    required_text_columns = {
        "event_start_date": "ALTER TABLE places ADD COLUMN event_start_date VARCHAR",
        "event_end_date": "ALTER TABLE places ADD COLUMN event_end_date VARCHAR",
    }
    with engine.begin() as connection:
        for column_name, ddl in required_text_columns.items():
            if column_name not in columns:
                connection.execute(text(ddl))


def map_item(item: dict[str, Any], region: str, default_type_id: int) -> dict[str, Any]:
    content_type_id = to_int(item.get("contenttypeid")) or default_type_id
    addr1 = blank_to_none(item.get("addr1"))
    homepage = blank_to_none(item.get("homepage"))
    has_event_dates = "eventstartdate" in item or "eventenddate" in item
    event_start_date = None
    event_end_date = None
    if content_type_id == 15 and has_event_dates:
        event_start_date = blank_to_none(item.get("eventstartdate"))
        event_end_date = blank_to_none(item.get("eventenddate"))

    return {
        "content_id": blank_to_none(item.get("contentid")),
        "content_type_id": content_type_id,
        "region": blank_to_none(region) or "\uc11c\uc6b8",
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
        "event_start_date": event_start_date,
        "event_end_date": event_end_date,
        "_has_event_dates": has_event_dates,
    }


def should_update(
    existing: Place, incoming: dict[str, Any], has_event_dates: bool
) -> bool:
    incoming_modified = incoming.get("source_modified_at")
    if existing.source_modified_at is None and incoming_modified is not None:
        return True
    if (
        incoming_modified is not None
        and existing.source_modified_at is not None
        and incoming_modified > existing.source_modified_at
    ):
        return True

    if has_event_dates:
        return any(
            getattr(existing, key) != incoming.get(key)
            for key in ("event_start_date", "event_end_date")
        )
    return False


def seed() -> None:
    ensure_place_columns()
    db = SessionLocal()
    stats = {
        content_type_id: {"inserted": 0, "updated": 0}
        for content_type_id in TARGET_TYPES
    }

    try:
        for _path, payload in iter_seed_payloads():
            default_type_id = to_int(payload.get("contentTypeId"))
            region = payload.get("region")
            if default_type_id not in TARGET_TYPES:
                continue

            for raw_item in payload.get("items", []):
                data = map_item(raw_item, region, default_type_id)
                has_event_dates = data.pop("_has_event_dates")
                if not data["content_id"] or not data["title"]:
                    continue

                existing = (
                    db.query(Place)
                    .filter(Place.content_id == data["content_id"])
                    .first()
                )
                if existing is None:
                    db.add(Place(**data))
                    stats[data["content_type_id"]]["inserted"] += 1
                    continue

                if should_update(existing, data, has_event_dates):
                    for key, value in data.items():
                        if (
                            not has_event_dates
                            and key in ("event_start_date", "event_end_date")
                        ):
                            continue
                        setattr(existing, key, value)
                    stats[data["content_type_id"]]["updated"] += 1

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    verify_db = SessionLocal()
    try:
        total = verify_db.query(Place).count()
        saved_counts = {
            content_type_id: verify_db.query(Place)
            .filter(Place.content_type_id == content_type_id)
            .count()
            for content_type_id in TARGET_TYPES
        }
    finally:
        verify_db.close()

    for content_type_id, label in TARGET_TYPES.items():
        print(f"{label} \uc2e0\uaddc: {stats[content_type_id]['inserted']}")
        print(f"{label} \uc5c5\ub370\uc774\ud2b8: {stats[content_type_id]['updated']}")
        print(f"{label} \uc800\uc7a5 \uac1c\uc218: {saved_counts[content_type_id]}")
    print(f"\ucd1d \uc800\uc7a5 \uac1c\uc218: {total}")


if __name__ == "__main__":
    seed()
