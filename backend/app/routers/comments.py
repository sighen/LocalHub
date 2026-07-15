from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.profanity import contains_banned_word

router = APIRouter()


@router.get("/posts/{post_id}/comments", response_model=List[schemas.CommentItem])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .order_by(models.Comment.created_at.asc())
        .all()
    )


@router.post("/posts/{post_id}/comments", status_code=201)
def create_comment(post_id: int, payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if contains_banned_word(payload.content):
        raise HTTPException(status_code=400, detail="부적절한 표현이 포함되어 있어 등록할 수 없습니다.")

    comment = models.Comment(post_id=post_id, content=payload.content, password=payload.password)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"id": comment.id, "created_at": comment.created_at}


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, payload: schemas.CommentDelete, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if comment.password != payload.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")

    db.delete(comment)
    db.commit()
    return None
