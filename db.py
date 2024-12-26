from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///book.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True # only for debugging purpose
)


def get_session():
    with Session(engine) as session:
        yield session