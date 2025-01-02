from service.pair.pairservice import PairService
from service.signal.signalservice import SignalService

def setup_services():
    pair_service = PairService()
    signal_service = SignalService()
    return pair_service, signal_service
