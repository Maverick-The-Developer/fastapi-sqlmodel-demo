from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "database.sqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(bind=engine, autocommit=False, autoflush=False)
    try:
        yield db
    finally:
        db.close()