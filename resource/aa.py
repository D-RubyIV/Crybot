import os
from typing import List
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
from config.achemy import engine
from config.logger import my_logger
from entity.models import BaseModel, PairRecord, SignalRecord
from service.binance.binanceservice import get_binance_symbol_pairs
from service.pair.pairservice import PairService
from service.signal.signalservice import SignalService

# CONFIG #
load_dotenv()
TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

pair_service = PairService()
signal_service = SignalService()

WAITING_FOR_PAIR_CODE = 0
WAITING_FOR_CREATE_REPORT = 0
WAITING_FOR_PRICE = 1

pair_code_received = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Type /help to see how can I help you?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here are the commands you can use:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/list - List of the files in the folder\n"
        "/check - Check a pair in the database\n"
        "/signal - Add a new signal to the database\n"
    )

async def handle_reply_list_pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_pair: List[PairRecord] = pair_service.find_all()
    if not list_pair:
        await update.message.reply_text("No pairs found.")
        return
    pair_list = f"Total: {len(list_pair)}"
    await update.message.reply_text(pair_list)

def add_new_signal(price: float, pair_code):
    pair = pair_service.find_by_code(code=pair_code)
    signal = SignalRecord(pair_record=pair, price=price, isAlerted=False)
    signal_service.add_entity(signal)

async def receive_signal_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pair_code_received
    pair_code = update.message.text
    pair_exists = pair_service.find_by_code(code=pair_code)
    if pair_exists:
        pair_code_received = pair_code
        await update.message.reply_text(f"Pair '{pair_code}' exists. Please enter the price.")
        return WAITING_FOR_PRICE
    else:
        await update.message.reply_text(f"Pair '{pair_code}' does not exist.")
        return ConversationHandler.END

async def receive_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pair_code_received
    try:
        price = float(update.message.text)
        add_new_signal(price, pair_code_received)
        await update.message.reply_text(f"Signal added for pair '{pair_code_received}' at price {price}.")
    except ValueError:
        await update.message.reply_text("Invalid price. Please enter a valid number.")
        return WAITING_FOR_PRICE
    return ConversationHandler.END

async def required_input_pair_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send me the pair code. /cancel to cancel")
    return WAITING_FOR_PAIR_CODE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pair_code_received
    pair_code_received = None
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    my_logger.error(f"Error : {context.error}")

if __name__ == "__main__":
    BaseModel.metadata.create_all(engine)
    list_pair_code = get_binance_symbol_pairs()
    pair_service.sync_pairs_to_db(list_pair_code=list_pair_code)
    my_logger.info("Sync successfully")
    my_logger.info("Total: %s", len(pair_service.find_all()))

    app = Application.builder().token(TOKEN).connect_timeout(60).pool_timeout(60).read_timeout(60).write_timeout(
        60).get_updates_read_timeout(10).build()

    add_create_signal_handler = ConversationHandler(
        entry_points=[CommandHandler("signal", required_input_pair_code)],
        states={
            WAITING_FOR_PAIR_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_signal_code)],
            WAITING_FOR_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_price)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(add_create_signal_handler)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", handle_reply_list_pair))

    my_logger.info("Bot is running..")
    app.run_polling(poll_interval=1)
