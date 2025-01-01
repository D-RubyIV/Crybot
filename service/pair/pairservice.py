from entity.models import PairRecord
from repo.pair.pairrepository import PairRepository
from service.base.baseservice import BaseService


class PairService(BaseService):
    def __init__(self):
        self.repo = PairRepository()
        super().__init__(self.repo, PairRecord)