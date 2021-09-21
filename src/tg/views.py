from django.shortcuts import render

# Create your views here.
from telegram import ReplyKeyboardMarkup

from tg import services
from tg.announcer.announcer import Announcer
from tg.globals import Texts
from tg.helper.helper import Helper
from tg.profile.profile import Profile
from tg.profile.txt import TEXTS

from telegram_bot_pagination import InlineKeyboardPaginator

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
    if not (update.message or update.callback_query):
        return start(update, context)
    try:
        if update.callback_query:
            msg = update.callback_query.data.encode("utf-8")
        else:
            msg = update.message.text.encode("utf-8")
    except:
        if update.callback_query:
            msg = update.callback_query.data
        else:
            msg = update.message.text
    if not update.callback_query:
        user = update.message.from_user
    else:
        user = update.callback_query.from_user
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
        try:
            services.change_log(user.id, {"state": 0})
        except:
            pass
    elif msg == text_translate(Texts['BTN_GET_EMP'][1]) or msg == text_translate(Texts['BTN_GET_EMP'][2]):
        tg_model = services.userChangeMenu(user.id, 2)
        try:
            services.change_log(user.id, {"state": 0})
        except:
            pass

    elif msg == text_translate(Texts['BTN_PROFILE'][1]) or msg == text_translate(Texts['BTN_PROFILE'][2]):
        tg_model = services.userChangeMenu(user.id, 3)
        try:
            services.change_log(user.id, {"state": 0})
        except:
            pass
    else:
        tg_model = services.get_user(user.id)

    if tg_model.get("menu_log") == 1:
        root = Announcer(context.bot, update, tg_model)
        if update.message.text == None:
            if update.message.contact == None:
                text = update.message.location
            else:
                text = update.message.contact.phone_number
        else:
            text = update.message.text
        root.received_message(msg, text)
        return 1
    elif tg_model.get("menu_log") == 2:
        chat_id = None
        if not update.callback_query:
            chat_id = update.message.message_id
            text = update.message.text
        else:
            chat_id = update.callback_query.message.message_id
            text = update.callback_query.data
        root = Helper(context.bot, update, tg_model)
        root.received_message(msg, tg_model['lang'], text, chat_id)
        return 1
    elif tg_model.get("menu_log") == 3:
        root = Profile(context.bot, update, tg_model)
        text = update.message.text
        message_id = update.message.message_id
        contact = None
        if text == None:
            contact = update.message.contact.phone_number
        if text == TEXTS["menu_profile"]["BTN_TOP"][1] or text == TEXTS["menu_profile"]["BTN_TOP"][2]:
            sendMainMenu(context, user.id, tg_model['lang'])
        else:
            root.received_message(msg, text, message_id, contact)
        return 1
    else:
        sendMainMenu(context, user.id, tg_model['lang'])
        return 1

def get_contact_value(update, context):
    pass


def inline_query(update, context):
    tg_model = services.get_user(update.callback_query.from_user.id)
    message_id = update.callback_query.message.message_id

    if tg_model.get("menu_log") == 3:
        root = Profile(context.bot, update, tg_model)
        callback_data = update.callback_query.data
        print("tg_model", tg_model)
        root.inline_query(callback_data, message_id)

