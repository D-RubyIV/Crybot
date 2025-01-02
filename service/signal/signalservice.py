from entity.models import SignalRecord
from repo.signal.signalrepository import SignalRepository
from service.base.baseservice import BaseService


class SignalService(BaseService):
    def __init__(self):
        self.repo = SignalRepository()
        super().__init__(self.repo, SignalRecord)

    def find_by_pair_code_and_price(self, price: float, pair_code):
        return self.repo.find_by_pair_code_and_price(price=price, pair_code=pair_code)
