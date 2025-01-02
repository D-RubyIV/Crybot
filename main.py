import os
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv
from config.logger import my_logger
from service.binance.binanceservice import get_binance_symbol_pairs
from setup.setup import setup_services
from handler.commonhandlers import start, help_command, cancel
from handler.pairhandlers import list_pairs, request_pair_code, receive_pair_code

load_dotenv()
TOKEN = os.getenv("TOKEN")
pair_service, signal_service = setup_services()
WAITING_FOR_PAIR_CODE = 0

if __name__ == "__main__":
    pair_service.sync_pairs_to_db(get_binance_symbol_pairs())
    my_logger.info("Synced successfully. Total: %s", len(pair_service.find_all()))

    app = Application.builder().token(TOKEN).build()

    pair_handler = ConversationHandler(
        entry_points=[CommandHandler("signal", request_pair_code), CommandHandler("check", request_pair_code)],
        states={WAITING_FOR_PAIR_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_pair_code)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(pair_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_pairs))

    my_logger.info("Bot running...")
    app.run_polling(poll_interval=1)