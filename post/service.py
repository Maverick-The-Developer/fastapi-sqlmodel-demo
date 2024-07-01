from sqlmodel import Session, insert, select, update, delete, desc, func
from post.models import PostCreate, PostListResponse, PostUpdate, Post


def insertPost(post: PostCreate, db: Session) -> Post | None:
    stmt = insert(Post).values(title=post.title, content=post.content)
    result = db.exec(stmt)
    db.commit()
    post_id = result.inserted_primary_key[0]
    newPost = db.exec(select(Post).where(Post.id == post_id)).one_or_none()
    return newPost


def selectAllPosts(db: Session) -> PostListResponse:
    total = db.scalar(select(func.count(Post.id)))
    posts: list[Post] = db.exec(select(Post).order_by(desc(Post.id))).all()
    return PostListResponse(posts=posts, total=total)


def selectOnePost(id: int, db: Session) -> Post | None:
    return db.exec(select(Post).where(Post.id == id)).one_or_none()


def updatePost(id: int, post: PostUpdate, db: Session) -> Post | None:
    db_post = db.exec(select(Post).where(Post.id == id)).one_or_none()
    if db_post is None:
        return None
    stmt = (
        update(Post).where(Post.id == id).values(title=post.title, content=post.content)
    )
    db.exec(stmt)
    db.commit()
    db.refresh(db_post)

    return db_post


def deletePost(id: int, db: Session) -> bool:
    db_post = db.exec(select(Post).where(Post.id == id)).one_or_none()
    if db_post is None:
        return False
    stmt = delete(Post).where(Post.id == id)
    db.exec(stmt)
    db.commit()
    return True
