from django.shortcuts import render

# Create your views here.
from telegram import ReplyKeyboardMarkup

from tg import services
from tg.announcer.announcer import Announcer
from tg.globals import Texts
from tg.helper.helper import Helper
from tg.profile.profile import Profile


def text_translate(message):
    try:
        result = message.encode('utf-8')
    except AttributeError:
        result = message
    return result


def go_message(context, user_id, message, reply_markup):
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                             disable_web_page_preview=True)


def sendMainMenu(context, user_id, lang):
    go_message(context, user_id, Texts['TEXT_HOME'][lang], ReplyKeyboardMarkup([
        [Texts['BTN_CREATE_AD'][lang], Texts['BTN_GET_EMP'][lang]],
        [Texts['BTN_PROFILE'][lang]]
    ], one_time_keyboard=True, resize_keyboard=True))


def sendLangMessage(context, user_id):
    go_message(context, user_id, Texts['TEXT_START'], ReplyKeyboardMarkup([
        [Texts['BTN_LANG'][1]], [Texts['BTN_LANG'][2]]], one_time_keyboard=True, resize_keyboard=True))


def start(update, context):
    user = update.message.from_user
    tg_model = services.get_user(user.id)
    if not tg_model:
        print("aa")
        tg_model = services.create_tg_user(user)
        print("bb")
    print(tg_model)
    if not tg_model.get('lang'):
        sendLangMessage(context, user.id)
        return 1
    else:
        sendMainMenu(context, user.id, tg_model.get('lang'))


def received_message(update, context):
    if not update.message:
        return start(update, context)
    try:
        msg = update.message.text.encode("utf-8")
    except:
        msg = update.message.text
    print(msg)
    user = update.message.from_user
    if msg == text_translate(Texts['BTN_LANG'][1]):
        print("A.2")
        services.tgChangeLang(user.id, 1)
        tg_model = services.get_user(user.id)
        sendMainMenu(context, user.id, tg_model['lang'])
        return 1
    elif msg == text_translate(Texts['BTN_LANG'][2]):
        print("A.3")
        services.tgChangeLang(user.id, 2)
        tg_model = services.get_user(user.id)
        sendMainMenu(context, user.id, tg_model['lang'])
        return 1

    if msg == text_translate(Texts['BTN_CREATE_AD'][1]) or msg == text_translate(Texts['BTN_CREATE_AD'][2]):
        tg_model = services.userChangeMenu(user.id, 1)

    elif msg == text_translate(Texts['BTN_GET_EMP'][1]) or msg == text_translate(Texts['BTN_GET_EMP'][2]):
        tg_model = services.userChangeMenu(user.id, 2)

    elif msg == text_translate(Texts['BTN_PROFILE'][1]) or msg == text_translate(Texts['BTN_PROFILE'][2]):
        tg_model = services.userChangeMenu(user.id, 3)
    else:
        tg_model = services.get_user(user.id)

    if tg_model.get("menu_log") == 1:
        root = Announcer(context.bot, update, tg_model)
        root.received_message(msg, update.message.text)
        return 1
    elif tg_model.get("menu_log") == 2:
        root = Helper(context.bot, update, tg_model)
        root.received_message(msg, update.message.text)
        return 1
    elif tg_model.get("menu_log") == 3:
        root = Profile(context.bot, update, tg_model)
        root.received_message(msg, update.message.text)
        return 1
    else:
        sendMainMenu(context, user.id, tg_model['lang'])
        return 1

def get_contact_value(update, context):
    pass


def inline_query(update, context):
    pass
