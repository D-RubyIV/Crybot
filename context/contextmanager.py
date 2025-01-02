from telegram.ext import ContextTypes


class ContextManager:
    def __init__(self, context: ContextTypes.DEFAULT_TYPE):
        self.context = context

    def assign_user_context(self, key: str, value: any):
        self.context.user_data[key] = value

    def get_user_context(self, key: str):
        return self.context.user_data.get(key)

    def assign_chat_context(self, key: str, value: any):
        self.context.chat_data[key] = value

    def get_chat_context(self, key: str):
        return self.context.chat_data.get(key)

    def assign_bot_context(self, key: str, value: any):
        self.context.bot_data[key] = value

    def assign_bot_context(self, key: str, value: any):
        self.context.bot_data[key] = value