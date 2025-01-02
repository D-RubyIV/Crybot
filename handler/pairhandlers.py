from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from service.pair.pairservice import PairService

pair_service = PairService()
WAITING_FOR_PAIR_CODE = 0

async def list_pairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pairs = pair_service.find_all()
    await update.message.reply_text(f"Total: {len(pairs)}" if pairs else "No pairs found.")

async def request_pair_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send pair code or /cancel to exit.")
    return WAITING_FOR_PAIR_CODE

async def receive_pair_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair_code = update.message.text
    pair = pair_service.find_by_code(code=pair_code)
    await update.message.reply_text(f"Pair '{pair_code}' {'exists' if pair else 'not exist'}.")
    return ConversationHandler.END