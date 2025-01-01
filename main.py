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
from entity.models import BaseModel, PairRecord
from service.pair.pairservice import PairService

# CONFIG #
load_dotenv()
TOKEN = os.getenv("TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

pair_service = PairService()

WAITING_FOR_PAIR_CODE = 0

is_pair_code_received = False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Type /help to see how can i help you?"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here are the commands you can use:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/list - List of the files in the folder\n"
        "/add - Add a new pair to the database\n"
    )

async def handle_reply_list_pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_pair: List[PairRecord] = pair_service.find_all()
    if not list_pair:
        await update.message.reply_text("No pairs found.")
        return

    pair_list = '\n'.join([pair.code for pair in list_pair])
    await update.message.reply_text(pair_list)

async def add_pair_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_pair_code_received
    is_pair_code_received = False
    await update.message.reply_text("Please send me the pair code. /cancel to cancel")
    return WAITING_FOR_PAIR_CODE

async def receive_pair_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_pair_code_received
    if not is_pair_code_received:
        pair_code = update.message.text
        addNewPair(pair_code)
        is_pair_code_received = True
        await update.message.reply_text(f"Pair '{pair_code}' has been added.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_pair_code_received
    is_pair_code_received = False
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def addNewPair(code: str):
    pair = PairRecord(code=code)
    pair_service.add_entity(pair)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    my_logger.error(f"Error : {context.error}")

if __name__ == "__main__":
    BaseModel.metadata.create_all(engine)

    app = Application.builder().token(TOKEN).connect_timeout(60).pool_timeout(60).read_timeout(60).write_timeout(
        60).get_updates_read_timeout(10).build()

    add_pair_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_pair_command)],
        states={
            WAITING_FOR_PAIR_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_pair_code)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(add_pair_handler)
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", handle_reply_list_pair))

    my_logger.info("Bot is running..")
    app.run_polling(poll_interval=1)
