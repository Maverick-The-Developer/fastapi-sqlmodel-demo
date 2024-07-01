from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables, engine
from post.router import router as post_router


@asynccontextmanager
async def lifeSpan(app: FastAPI):
    # on startup
    print("#" * 20, "Server is starting", "#" * 20)
    print("=" * 20, "Creating Table if NOT Exists", "=" * 20)
    create_db_and_tables()
    yield
    # on shutdown
    print("#" * 20, "Server is going DOWN", "#" * 20)
    if engine:
        engine.dispose()


app = FastAPI(lifespan=lifeSpan)

app.include_router(post_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
