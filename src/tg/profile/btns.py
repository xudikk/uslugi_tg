from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tg.profile.txt import TEXTS
from tg.globals import Texts


def markup_btns(type=None, lang=1):
    if type == "main":
        text = TEXTS.get("menu_profile")
        btn = [
            [KeyboardButton(text["BTN_SET"][lang]), KeyboardButton(text["BTN_ADDS"][lang])],
            [KeyboardButton(text["BTN_TOP"][lang])]
        ]
    elif type == "settings":
        text = TEXTS.get("menu_set")
        btn = [
            [text["change_lang"][lang]],
            [TEXTS["BTN_BACK"][lang]]
        ]
    elif type == "s_lang":
        btn = [
                [Texts['BTN_LANG'][1]], [Texts['BTN_LANG'][2]]
        ]
    elif type == "back":
        btn = [
            [KeyboardButton(TEXTS["BTN_BACK"][lang])]
        ]
    else:
        btn = []
    return ReplyKeyboardMarkup(btn, one_time_keyboard=True, resize_keyboard=True)


def inline_buttons(type=None, page=None, data=None, lang=1):
    if type == "button":
        text = TEXTS["inline_btn"]
        btn = [
            [InlineKeyboardButton(text["BTN_BACK"][lang],
                                  callback_data=f"page={page['previous'] if page['previous'] != None else 1}"),
             InlineKeyboardButton(f"{page['page_num']}/{page['count']}", callback_data="None"),
             InlineKeyboardButton(text["BTN_NEXT"][lang], callback_data=f"page={page['page_num']+1}")],
            [InlineKeyboardButton(text["BTN_DEL"][lang], callback_data=f"delete={data['id']}"),
             InlineKeyboardButton(text["BTN_EDIT"][lang], callback_data=f"edit={data['id']}")]
        ]

    return InlineKeyboardMarkup(btn)

