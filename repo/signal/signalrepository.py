from sqlalchemy import and_

from entity.models import SignalRecord
from repo.base.baserepository import BaseRepository


class SignalRepository(BaseRepository):
    def __init__(self):
        super().__init__(domain=SignalRecord)

    def find_by_pair_code_and_price(self, price: float, pair_code: str):
        with super().get_session() as session:
            return session.query(SignalRecord).filter(
                and_(
                    SignalRecord.price == price,
                    SignalRecord.pair_record.code == pair_code
                )
            ).one_or_none()
