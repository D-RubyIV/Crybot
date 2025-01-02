from entity.models import PairRecord
from repo.pair.pairrepository import PairRepository
from service.base.baseservice import BaseService


class PairService(BaseService):
    def __init__(self):
        self.repo = PairRepository()
        super().__init__(self.repo, PairRecord)

    def sync_pairs_to_db(self, list_pair_code):
        with self.repo.get_session() as session:
            existing_codes = {code for code, in session.query(PairRecord.code).all()}
            data = [
                PairRecord(code=code)
                for code in list_pair_code if code not in existing_codes
            ]
            if data:
                session.add_all(data)
                session.commit()

    def find_by_code(self, code: str):
        return self.repo.find_by_code(code)
