from telegram import ReplyMarkup, ReplyKeyboardMarkup, KeyboardButton

from tg.globals import Texts


def markup_btns(type=None):
    if type == "main":
        btn = [
            [KeyboardButton("Sozlamalar"), KeyboardButton("Mening e'lonlarim")]
        ]
    elif type == "settings":
        btn = [
            ["Tilni o\'zgartirish"]
        ]
    elif type == "s_lang":
        btn = [
                [Texts['BTN_LANG'][1]], [Texts['BTN_LANG'][2]]
        ]
    else:
        btn = []
    return ReplyKeyboardMarkup(btn, one_time_keyboard=True, resize_keyboard=True)
