from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from config.state import WAITING_FOR_INPUT_PAIR_PRICE, WAITING_FOR_INPUT_PAIR_CODE
from constant.constant import KEYBOARD
from context.contextmanager import ContextManager
from entity.models import SignalRecord
from service.pair.pairservice import PairService
from service.signal.signalservice import SignalService


class SignalHandler:
    pair_service = PairService()
    signal_service = SignalService()

    @staticmethod
    async def handle_receive_signal_pair_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
        pair_code_received = update.message.text
        pair_found = SignalHandler.pair_service.find_by_code(code=pair_code_received)
        if pair_found is not None:
            ContextManager(context).assign_user_context(key="pair_code_received", value=pair_code_received)
            await update.message.reply_text(f"Mã cặp '{pair_code_received}' đã được nhận. Vui lòng nhập giá.")
            return WAITING_FOR_INPUT_PAIR_PRICE
        else:
            await update.message.reply_text(f"Không tìm thấy cặp {pair_code_received}, hãy nhập lại mã")
            return WAITING_FOR_INPUT_PAIR_CODE

    @staticmethod
    async def handle_receive_signal_pair_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            price = float(update.message.text)
            pair_code_received = ContextManager(context).get_user_context("pair_code_received")
            if pair_code_received:
                pair = SignalHandler.pair_service.find_by_code(code=pair_code_received)
                if pair is not None:
                    SignalHandler.signal_service.add_entity(
                        SignalRecord(pair_record=pair, price=price, isAlerted=False)
                    )
                    await update.message.reply_text(
                        text=f"Signal đã được thêm cho cặp '{pair_code_received}' với giá {price}.",
                        reply_markup=InlineKeyboardMarkup(KEYBOARD.KEY_BOARD_SIGNAL_VIEW))
                else:
                    await update.message.reply_text(f"Không tìm thấy cặp {pair_code_received}, hãy nhập lại mã")
                    return WAITING_FOR_INPUT_PAIR_CODE
            else:
                await update.message.reply_text("Không có mã cặp. Vui lòng nhập mã cặp trước.")
                return WAITING_FOR_INPUT_PAIR_CODE
        except ValueError:
            await update.message.reply_text("Giá không hợp lệ. Vui lòng nhập một số hợp lệ.")
            return WAITING_FOR_INPUT_PAIR_PRICE
        return ConversationHandler.END

    @staticmethod
    async def handle_required_input_pair_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text="Vui lòng gửi mã cặp. /cancel để hủy bỏ")
        return WAITING_FOR_INPUT_PAIR_CODE
