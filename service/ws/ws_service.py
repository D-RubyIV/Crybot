import json, websocket
import threading
from typing import List

from config.logger import my_logger
from entity.models import SignalRecord
from service.signal.signalservice import SignalService

class MyWebSocket:
    ws = None
    signal_service = SignalService()
    current_assets = []

    ws_thread = None

    def get_list_assets(self) -> List[str]:
        list_signal_record: List[SignalRecord] = self.signal_service.find_all()
        list_assets = list(set([record.pair_record.code for record in list_signal_record]))
        return list_assets

    def on_message(self, ws, message):
        data = json.loads(message)
        symbol = data["data"]["s"]
        close = data["data"]["k"]["c"]
        print(f"S: {symbol} - C: {close} - TOTAL: {len(self.current_assets)}")

    def run_ws(self):
        self.current_assets = self.get_list_assets()
        my_logger.info("Websocket is running ...")
        if self.ws:
            self.stop_ws()  # Dừng websocket hiện tại trước khi mở lại

        streams = '/'.join([a.lower() + "@kline_1h" for a in self.current_assets])
        self.ws = websocket.WebSocketApp(
            f"wss://stream.binance.com:9443/stream?streams={streams}",
            on_message=self.on_message
        )

        # Khởi chạy WebSocket trong một luồng riêng biệt
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.start()

    def stop_ws(self):
        if self.ws:
            self.ws.close()
            my_logger.info("Websocket stopped")
        if self.ws_thread:
            self.ws_thread.join()  # Đảm bảo thread được đóng khi dừng WebSocket
