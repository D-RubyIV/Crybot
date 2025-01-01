from entity.models import PairRecord
from repo.base.baserepository import BaseRepository


class PairRepository(BaseRepository):
    def __init__(self):
        super().__init__(domain=PairRecord)
