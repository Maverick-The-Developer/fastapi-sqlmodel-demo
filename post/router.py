from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_db
from post.models import PostCreate, PostListResponse, PostUpdate, Post
from post.service import deletePost, insertPost, selectAllPosts, selectOnePost, updatePost

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=Post, status_code=201)
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = insertPost(post, db)
    if db_post is None:
        raise HTTPException(status_code=400, detail="Something went wrong")
    return db_post


@router.get("", response_model=PostListResponse)
def get_posts(db: Session = Depends(get_db)):
    return selectAllPosts(db)


@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    db_post = selectOnePost(id, db)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = updatePost(id, post, db)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    result = deletePost(id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return True
