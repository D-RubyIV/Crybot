from typing import TypeVar
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.pool import QueuePool

from config.config import settings
from config.logger import my_logger

T = TypeVar('T')

engine = create_engine(
    f"sqlite+pysqlite:///{settings.DBPATH}?check_same_thread=False",
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
    poolclass=QueuePool,
    echo=False,
    pool_pre_ping=True,
    connect_args={"timeout": 30}
)


print(f"DB Path: ", settings.DBPATH)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=engine
    )
)

def get_session_local() -> Session:
    db = SessionLocal()
    my_logger.info("------------------ SESSION OPEN ------------------")
    try:
        yield db
        db.commit()  # Commit sau khi hoàn tất các thao tác
    except SQLAlchemyError as e:
        my_logger.error("Database error occurred: %s", str(e))
        db.rollback()  # Rollback nếu có lỗi
        raise
    finally:
        db.close()  # Đảm bảo kết nối luôn đóng
        my_logger.info("------------------ SESSION CLOSED ------------------")
