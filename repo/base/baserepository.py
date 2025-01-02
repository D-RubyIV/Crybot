from sqlalchemy.orm import Session
from typing import Type, TypeVar, List, Generic, Any

from config.achemy import SessionLocal, get_session_local
from config.logger import my_logger
from entity.models import BaseModel

T = TypeVar('T', bound=BaseModel)




class BaseRepository(Generic[T]):
    def __init__(self, domain: Type[T]):
        self.domain = domain
        self.db = SessionLocal

    def get_session(self) -> Session:
        my_logger.info(f"GET SESSION FROM : {self.domain.__name__}", )
        return next(get_session_local())

    def find_all(self) -> List[T]:
        with self.get_session() as session:
            return session.query(self.domain).all()

    def find_by_id(self, entity_id: int) -> T:
        with self.get_session() as session:
            return session.query(self.domain).filter_by(id=entity_id).first()

    def add(self, entity: T):
        with self.get_session() as session:
            session.add(entity)
            session.commit()
            return entity

    def add_all(self, entity_list: List[T]):
        with self.get_session() as session:
            session.add_all(entity_list)
            session.commit()
        return entity_list

    def update_by_id(self, entity_id: int, entity: T):
        with self.get_session() as session:
            entity_to_update = session.query(self.domain).filter_by(id=entity_id).first()
            if entity_to_update:
                for key, value in entity.__dict__.items():
                    if key != "_sa_instance_state":
                        setattr(entity_to_update, key, value)
                session.commit()

    def update(self, entity: T) -> None:
        with self.get_session() as session:
            session.commit()

    def delete(self, entity: T) -> None:
        with self.get_session() as session:
            session.delete(entity)
            session.commit()

    def update_field_for_all(self, field_name: str, new_value: Any) -> None:
        """
        Cập nhật giá trị của một trường cho toàn bộ bản ghi của model.
        :param field_name: Tên của cột cần cập nhật.
        :param new_value: Giá trị mới sẽ được đặt cho cột.
        """
        with self.get_session() as session:
            session.query(self.domain).update(
                {field_name: new_value}, synchronize_session=False
            )
            session.commit()