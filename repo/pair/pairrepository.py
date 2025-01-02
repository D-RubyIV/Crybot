from entity.models import PairRecord
from repo.base.baserepository import BaseRepository


class PairRepository(BaseRepository):
    def __init__(self):
        super().__init__(domain=PairRecord)

    def find_by_code(self, code: str):
        with super().get_session() as session:
            return session.query(PairRecord).filter(PairRecord.code == code).one_or_none()
