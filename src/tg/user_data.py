import re
import datetime
from telegram import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)

# from .models import Log
from .globals import Texts
from . import services


class UserData:
    def __init__(self, bot, update, user_model):
        self._bot = bot
        self.update = update
        self.user_model = user_model if user_model else {}

        if update.message:
            self.user = update.message.from_user
            self.query = None
        else:
            self.query = update.callback_query
            self.user = self.query.from_user

        try:
            self.log = services.get_user_log(self.user.id)
            if not self.log:
                raise Exception
        except Exception as e:
            self.log = services.create_log(user_id=self.user.id)

    @property
    def user_data(self):
        return self.log.get("messages", {})

    def change_state(self, *args, **kwargs):
        self.log["messages"].update(*args)
        self.log = services.change_log(self.user.id, log=self.log["messages"])

    def clear_state(self, state=0):
        # self.log.messages = {'state': state}
        # self.log.save()
        self.log['messages'] = {'state': state}
        self.log = services.change_log(self.user.id, log=self.log)

    def change_profile_language(self, user_id, lang_id):
        services.tgChangeLang(user_id, lang_id)

    def delete_message_user(self, chat_id, message_id):
        self._bot.delete_message(chat_id, message_id)

    def go_message(self, user_id, message, reply_markup=None):
        self._bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                               disable_web_page_preview=True)

    def go_message_md(self, user_id, message, reply_markup, delete=True):

        self._bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='Markdown',
                               disable_web_page_preview=True)

    def go_reply(self, user_id, message, reply_id):
        self._bot.send_message(chat_id=user_id, text=message, reply_to_message_id=reply_id, parse_mode='HTML',
                               disable_web_page_preview=True)

    def go_reply_video(self, user_id, message, reply_id):
        self._bot.send_video(chat_id=user_id, text=message, reply_to_message_id=reply_id, parse_mode='HTML')

    def edit_message(self, chat_id, message_id, message, reply_markup):
        try:
            self._bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=message,
                                        reply_markup=reply_markup,
                                        parse_mode='HTML')
        except Exception as e:
            print('ERROR edit message: ', str(e))

    def send_photo(self, user_id, photo, caption=None, reply_markup=None):
        self._bot.send_photo(user_id, photo=photo, caption=caption, reply_markup=reply_markup, parse_mode='HTML')

    def send_video(self, user_id, video, caption=None, reply_markup=None):
        self._bot.send_video(user_id, video=video, caption=caption, reply_markup=reply_markup, parse_mode='HTML')

    def send_audio(self, user_id, audio, caption=None, reply_markup=None):
        self._bot.send_audio(user_id, audio=audio, caption=caption, reply_markup=reply_markup, parse_mode='HTML')

    def send_document(self, user_id, document, caption=None, reply_markup=None):
        self._bot.send_document(user_id, document=document, caption=caption, reply_markup=reply_markup,
                                parse_mode='HTML')

    def send_voice(self, user_id, voice, caption=None, reply_markup=None):
        self._bot.send_voice(user_id, voice=voice, caption=caption, reply_markup=reply_markup, parse_mode='HTML')

    def answer_callback_query(self, query_id, txt):
        self._bot.answer_callback_query(callback_query_id=query_id, text=txt, show_alert=True)

    def get_list_region(self):
        region = services.getRegions()
        return region

    def find_region(self, region_name, region_id=None):
        region = services.searchRegion(region_name, region_id)
        return region

    def getDistric(self, region_id):
        districts = services.Districts(region_id)
        return districts

    def format_region_buttons(self, lang, regions):
        keyboards = []
        for region in regions:
            keyboards.append([region[f'name_{lang}']])

        keyboards.append([Texts['BTN_SEND_BACK'][lang], Texts['BTN_HOME'][lang]])

        return ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=True)

    def get_district(self, name):
        root = services.district_by_name(name)
        return root

    #
    # def getListCategory(self):
    #     category = services.getParentCategories()
    #     return category
    #
    # def findCategory(self, category_name, parent_id=None):
    #     category = services.searchCategory(category_name, parent_id)
    #     return category
    #
    # def getCategoryChilds(self, parent_id, cats):
    #     childs = services.getCategoryChild(parent_id, cats)
    #     return childs

    def formatCategoryButtons(self, lang, categories, is_parent=True, btn_back=True):
        keyboards = []
        for category in categories:
            keyboards.append([category[f'name_{lang}']])

        if is_parent:
            if btn_back:
                keyboards.append([Texts['BTN_SEND_BACK'][lang]])
        else:
            keyboards.append([Texts['BTN_SEND_BACK'][lang], Texts['BTN_SEND_DALE'][lang]])
        keyboards.append([Texts['BTN_HOME'][lang]])

        return ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=True)


