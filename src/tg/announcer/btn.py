from telegram import  ReplyKeyboardMarkup, ReplyKeyboardRemove
from tg import services

def reply_markup(type=None):
    type = type.split('_')
    if type[0] == "region":
        response = services.getRegions()
        but = []
        button = []
        for cat in response:
            but.append(cat[f"name_{type[1]}"])
            if len(but) == 2:
                button.append(but)
                but = []
        if len(but) > 0:
            button.append(but)
            but =[]
        status = ['◀️ ortga',]
        button.append(status)
        complaint = ReplyKeyboardMarkup(button,  resize_keyboard=True, one_time_keyboard=True)
        return complaint
    elif type[0] == "cat":
        btn = ReplyKeyboardMarkup([["viloyat", "lokatsiya"]], resize_keyboard=True)

    elif type[0] == 'work':
        response = services.getCategory()
        but = []
        button = []
        for cat in response:
            but.append(cat[f"name_{type[1]}"])
            if len(but) == 2:
                button.append(but)
                but = []
        if len(but) > 0:
            button.append(but)
            but = []
        status = ['◀️ ortga']
        button.append(status)
        complaint = ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True)
        return complaint
    elif type[0] == 'footer':
        btn = ReplyKeyboardMarkup([["elon qo'shish", "Bosh sahifa"]], resize_keyboard=True)
    elif type[0] == "back":
        btn = ReplyKeyboardMarkup([['◀️Ortga']], resize_keyboard=True)
    elif type[0] == "info":
        btn = ReplyKeyboardMarkup([["✅ Xa", "❌ Yo'q"]], resize_keyboard=True)
    else:
        btn = []
    return btn

def remove_button():
    markup = ReplyKeyboardRemove(selective=False)
    return markup

# def generateButtons(type=None, category):
#     but = []
#     button = []
#     for cat in category:
#         but.append(cat.name)
#         button.append(but)
#         but = []
#     status = ReplyKeyboardMarkup([
#         ['◀️ ortga',]
#         ],  resize_keyboard=True)
#     complaint = ReplyKeyboardMarkup(button,  resize_keyboard=True)
