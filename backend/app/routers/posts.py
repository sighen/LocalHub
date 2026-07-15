from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.profanity import contains_banned_word

router = APIRouter()


def _apply_place_tag(post: models.Post, place_content_id: Optional[str], db: Session) -> None:
    if not place_content_id:
        post.place_content_id = None
        post.place_title = None
        post.place_content_type_id = None
        return

    place = db.query(models.Place).filter(models.Place.content_id == place_content_id).first()
    if not place:
        post.place_content_id = None
        post.place_title = None
        post.place_content_type_id = None
        return

    post.place_content_id = place.content_id
    post.place_title = place.title
    post.place_content_type_id = place.content_type_id


@router.get("", response_model=schemas.PostListResponse)
def list_posts(
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    place_content_id: Optional[str] = None,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(models.Post)
    if category:
        query = query.filter(models.Post.category == category)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(
            (models.Post.title.like(like)) | (models.Post.content.like(like))
        )
    if place_content_id:
        query = query.filter(models.Post.place_content_id == place_content_id)

    total = query.count()
    posts = (
        query.order_by(models.Post.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    items = []
    for p in posts:
        comment_count = (
            db.query(func.count(models.Comment.id))
            .filter(models.Comment.post_id == p.id)
            .scalar()
        )
        items.append(
            schemas.PostListItem(
                id=p.id,
                title=p.title,
                category=p.category,
                view_count=p.view_count,
                comment_count=comment_count,
                created_at=p.created_at,
                place_content_id=p.place_content_id,
                place_title=p.place_title,
                place_content_type_id=p.place_content_type_id,
            )
        )

    return schemas.PostListResponse(total=total, page=page, size=size, items=items)


@router.get("/{post_id}", response_model=schemas.PostDetail)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    post.view_count += 1
    db.commit()
    db.refresh(post)
    return post


@router.post("/{post_id}/verify-password", status_code=204)
def verify_post_password(post_id: int, payload: schemas.PostDelete, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    return None


@router.post("", status_code=201)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    if contains_banned_word(payload.title, payload.content):
        raise HTTPException(status_code=400, detail="부적절한 표현이 포함되어 있어 등록할 수 없습니다.")

    post = models.Post(
        title=payload.title,
        content=payload.content,
        category=payload.category,
        password=payload.password,
    )
    _apply_place_tag(post, payload.place_content_id, db)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id, "created_at": post.created_at}


@router.put("/{post_id}", response_model=schemas.PostDetail)
def update_post(post_id: int, payload: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")
    if contains_banned_word(payload.title, payload.content):
        raise HTTPException(status_code=400, detail="부적절한 표현이 포함되어 있어 등록할 수 없습니다.")

    post.title = payload.title
    post.content = payload.content
    post.category = payload.category
    _apply_place_tag(post, payload.place_content_id, db)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, payload: schemas.PostDelete, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(post)
    db.commit()
    return None
