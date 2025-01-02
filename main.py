import logging
import os

from telegram import Update
from telegram.ext import Application
from dotenv import load_dotenv
from config.logger import my_logger
from router.router import conv_handler
from service.binance.binanceservice import get_binance_symbol_pairs
from setup.setup import setup_services

load_dotenv()
TOKEN = os.getenv("TOKEN")
pair_service, signal_service = setup_services()
WAITING_FOR_PAIR_CODE = 0

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger("my_logger")

if __name__ == "__main__":
    pair_service.sync_pairs_to_db(get_binance_symbol_pairs())
    my_logger.info("Synced successfully. Total: %s", len(pair_service.find_all()))

    app = Application.builder().token(TOKEN).build()
    app.add_handler(conv_handler)
    my_logger.info("Bot running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=1)
