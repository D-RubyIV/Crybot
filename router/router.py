from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config.logger import my_logger
from config.state import START_ROUTES, WAITING_FOR_INPUT_PAIR_PRICE, WAITING_FOR_INPUT_PAIR_CODE, END_ROUTES
from constant.constant import Constants, KEYBOARD
from handler.pairhandlers import pair_service
from handler.signalhandler import SignalHandler
from service.signal.signalservice import SignalService

#
pair_code_received = ""
# Callback data
ONE, TWO, THREE, FOUR = range(4)

signal_service = SignalService()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    my_logger.info("User %s started the conversation.", user.first_name)
    reply_markup = InlineKeyboardMarkup(KEYBOARD.KEY_BOARD_START)
    await update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    my_logger.info("START OVER RELOAD")
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD.KEY_BOARD_START)
    await query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return START_ROUTES


# ====================== PAIR ====================== #
# ====================== PAIR ====================== #
# ====================== PAIR ====================== #
async def onHandleViewPair(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    my_logger.info("HANDLE VIEW PAIR")
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD.KEY_BOARD_PAIR_VIEW)
    await query.edit_message_text(
        text="Hệ thống/Niêm yết", reply_markup=reply_markup
    )
    return START_ROUTES


async def onHandleListPair(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyBoard = [
        [
            # InlineKeyboardButton(
            #     Constants.InlineKeyboardMarkup.PAIR.CHECK,
            #     callback_data=Constants.InlineKeyboardMarkup.PAIR.HANDLE_CHECK
            # ),
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.SIGNAL.VIEW,
                callback_data=Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_VIEW
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyBoard)
    await query.edit_message_text(
        text=f"Tổng số {len(pair_service.find_all())} cặp", reply_markup=reply_markup
    )
    return START_ROUTES


async def onHandleCheckPair(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.PAIR.CHECK,
                callback_data=Constants.InlineKeyboardMarkup.PAIR.HANDLE_CHECK
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Tổng số {len(pair_service.find_all())} cặp", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES


# ====================== PAIR ====================== #
# ====================== PAIR ====================== #
# ====================== PAIR ====================== #


# ====================== SIGNAL ====================== #
# ====================== SIGNAL ====================== #
# ====================== SIGNAL ====================== #
async def onHandleViewSignal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    my_logger.info("HANDLE VIEW SIGNAL")
    query = update.callback_query
    await query.answer()
    reply_markup = InlineKeyboardMarkup(KEYBOARD.KEY_BOARD_SIGNAL_VIEW)
    await query.edit_message_text(
        text="Hệ thống/Tín hiệu", reply_markup=reply_markup
    )
    return START_ROUTES


async def onHandleListSignal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    list_signal = signal_service.find_all()


    reply_markup = InlineKeyboardMarkup(KEYBOARD.KEY_BOARD_START)
    await query.edit_message_text(
        text=str(list_signal), reply_markup=reply_markup
    )
    return START_ROUTES


# ====================== SIGNAL ====================== #
# ====================== SIGNAL ====================== #
# ====================== SIGNAL ====================== #

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        WAITING_FOR_INPUT_PAIR_CODE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, SignalHandler.handle_receive_signal_pair_code),
        ],
        WAITING_FOR_INPUT_PAIR_PRICE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, SignalHandler.handle_receive_signal_pair_price),
        ],
        START_ROUTES: [
            # PAIR
            # pair - view
            CallbackQueryHandler(
                onHandleViewPair, pattern="^" + Constants.InlineKeyboardMarkup.PAIR.HANDLE_VIEW + "$"
            ),
            # pair - list
            CallbackQueryHandler(
                onHandleListPair, pattern="^" + Constants.InlineKeyboardMarkup.PAIR.HANDLE_LIST + "$"
            ),
            # pair - add
            CallbackQueryHandler(
                SignalHandler.handle_required_input_pair_code,
                pattern="^" + Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_CREATE + "$"
            ),

            # SIGNAL
            # signal - view
            CallbackQueryHandler(
                onHandleViewSignal,
                pattern="^" + Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_VIEW + "$"
            ),
            # signal - list
            CallbackQueryHandler(
                onHandleListSignal,
                pattern="^" + Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_LIST + "$"
            ),

        ],
        END_ROUTES: [
            CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
            CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
        ],
    },
    fallbacks=[CommandHandler("start", start)],
)
