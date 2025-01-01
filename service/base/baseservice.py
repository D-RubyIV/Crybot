from typing import TypeVar, Generic, Type, List, Any

from entity.models import BaseModel
from repo.base.baserepository import BaseRepository

R = TypeVar("R", bound=BaseRepository)
T = TypeVar("T", bound=BaseModel)

class BaseService(Generic[R, T]):
    def __init__(self, repo: Type[R], entity: Type[T]):
        self.repo = repo
        self.entity = entity()

    def self_commit(self):
        with self.repo.get_session() as session:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def add_all_entity(self, list_entity) -> T:
        return self.repo.add_all(list_entity)

    def add_entity(self, entity) -> T:
        return self.repo.add(entity)

    def get_entity(self) -> T:
        return self.entity

    def find_all(self) -> List[T]:
        return self.repo.find_all()

    def update_by_id(self, entity) -> T:
        return self.repo.update_by_id(entity.id, entity)

    def update(self) -> T:
        return self.repo.update(self.entity)

    def delete(self):
        return self.repo.delete(self.entity)

    def update_field_for_all(self, field_name: str, new_value: Any) -> None:
        self.repo.update_field_for_all(field_name, new_value)

