from telegram import InlineKeyboardButton


class Constants:
    class InlineKeyboardMarkup:
        START = "Start"

        class PAIR:
            VIEW = "Cặp niêm yết"
            LIST = "Danh sách cặp"
            CHECK = "Kiểm tra cặp"

            HANDLE_VIEW = "#P001"
            HANDLE_LIST = "#P002"
            HANDLE_CHECK = "#P003"

        class SIGNAL:
            VIEW = "Tín hiệu"
            LIST = "Danh sách tín hiệu"
            CREATE = "Thêm tín hiệu"
            UPDATE = "Sửa tín hiệu"
            DELETE = "Xóa tín hiệu"

            HANDLE_VIEW = "#S001"
            HANDLE_LIST = "#S002"
            HANDLE_CREATE = "#S003"
            HANDLE_UPDATE = "#S004"
            HANDLE_DELETE = "#S005"

class KEYBOARD:
    KEY_BOARD_START = [
        [
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.PAIR.VIEW,
                callback_data=Constants.InlineKeyboardMarkup.PAIR.HANDLE_VIEW
            ),
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.SIGNAL.VIEW,
                callback_data=Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_VIEW
            ),
        ]
    ]
    KEY_BOARD_PAIR_VIEW = [
        [
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.PAIR.LIST,
                callback_data=Constants.InlineKeyboardMarkup.PAIR.HANDLE_LIST
            ),
            # InlineKeyboardButton(
            #     Constants.InlineKeyboardMarkup.PAIR.CHECK,
            #     callback_data=Constants.InlineKeyboardMarkup.PAIR.HANDLE_CHECK
            # ),
        ]
    ]
    KEY_BOARD_SIGNAL_VIEW = [
        [
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.PAIR.LIST,
                callback_data=Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_LIST
            ),
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.SIGNAL.CREATE,
                callback_data=Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_CREATE
            ),
        ],
        [
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.SIGNAL.UPDATE,
                callback_data=Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_UPDATE
            ),
            InlineKeyboardButton(
                Constants.InlineKeyboardMarkup.SIGNAL.DELETE,
                callback_data=Constants.InlineKeyboardMarkup.SIGNAL.HANDLE_DELETE
            ),
        ],
    ]
