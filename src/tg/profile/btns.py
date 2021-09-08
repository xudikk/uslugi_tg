from telegram import ReplyMarkup, ReplyKeyboardMarkup, KeyboardButton


def markup_btns(type=None):
    print(type)
    if type == "main":
        print("Mana taypi", type)
        btn = [
            [KeyboardButton("Sozlamalar"), KeyboardButton("Mening e'lonlarim")]
        ]
    else:
        btn = []

    print("Buttonlar", btn)

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)
