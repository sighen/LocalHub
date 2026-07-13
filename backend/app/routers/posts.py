from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.get("", response_model=schemas.PostListResponse)
def list_posts(
    category: Optional[str] = None,
    keyword: Optional[str] = None,
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


@router.post("", status_code=201)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(
        title=payload.title,
        content=payload.content,
        category=payload.category,
        password=payload.password,
    )
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

    post.title = payload.title
    post.content = payload.content
    post.category = payload.category
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
