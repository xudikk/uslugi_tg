import ast

from tg.globals import Texts
from tg.user_data import UserData
from tg import services
from telegram import ReplyKeyboardMarkup, ReplyMarkup
from telegram_bot_pagination import InlineKeyboardPaginator


class Helper(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]

    def received_message(self, msg, txt, text, chat_id):
        message_id = chat_id
        user_state = self.user_data.get("state", 0)
        category_id = self.user_data.get('data', 0)
        data_announce = self.user_data.get('announce', [])
        buttons = self.render_buttons(txt)
        reply_murkup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if user_state == 0:
            self.change_state({"state": 1})
            self.go_message(message=Texts['REGION'][txt], user_id=self.user.id, reply_markup=reply_murkup)
        if user_state == 1:
            self.change_state({'state':2})
            data = services.searchRegion(text)
            self.change_state({'data': data['id']})
            self.go_message(message=Texts['REGION_END'][txt], user_id=self.user.id, reply_markup=None)
        if user_state == 2:
            self.change_state({'state': 3})
            data = services.searchCategory(text)
            if data != None:
                self.go_message(message=Texts['SUMMA'][txt], user_id=self.user.id, reply_markup=None)
            else:
                self.change_state({'state': 2})
                self.go_message(message=Texts['REGION_END_NONE'][txt], user_id=self.user.id, reply_markup=None)
        if user_state == 3:
            if ('-' in text) and ('--' not in text) and ('$' not in text):
                text = text.split('-')
                dic = {}
                try:
                    dic['from'] = int(text[0])
                    dic['to'] = int(text[1])
                except:
                    self.change_state({'state': 3})
                    self.go_message(message=Texts['SUMMA_ERROR'][txt], user_id=self.user.id, reply_markup=None)
                data = services.searchAnnounceMoney(f"{dic['from']}_{int(dic['to'])}_{category_id}")
                if data == []:
                    self.go_message(message=Texts['SUMMA_NONE'][txt], user_id=self.user.id, reply_markup=None)
                else:
                    self.change_state({'state': 4})
                    self.change_state({'announce': str(data)})
                    paginator = InlineKeyboardPaginator(
                        len(data),
                        data_pattern='character#{page}'
                    )
                    TEXT = f"""👨‍✈ Xodim {data[0]['fullname']}\n\n📞 Telefon nomer {data[0]['phone_number']}\n\n💵 Ishlash narxi {data[0]['price_from']}-{data[0]['price_to']} so'm\n\n📰 Qo'shimcha malumotlari {data[0]['description']}"""
                    self.go_message(message=TEXT, user_id=self.user.id, reply_markup=paginator.markup)
            else:
                self.change_state({'state': 3})
                self.go_message(message=Texts['SUMMA_ERROR'][txt], user_id=self.user.id, reply_markup=None)
        if user_state == 4:
            self.inline_query(msg, text, ast.literal_eval(data_announce), message_id)


    def render_buttons(self, txt):
        response = services.getRegions()
        but = []
        button = []
        for data in response:
            but.append(data[f'name_{txt}'])
            if len(but) == 2:
                button.append(but)
                but = []
        if len(but) > 0:
            button.append(but)
            but = []
        return button

    def inline_query(self, msg, text, data, message_id):
        number = int(text.split('#')[1])
        if number != 0:
            TEXT = f"""👨‍✈ Xodim {data[number-1]['fullname']}\n\n📞 Telefon nomer {data[number-1]['phone_number']}\n\n💵 Ishlash narxi {data[number-1]['price_from']}-{data[number-1]['price_to']} so'm\n\n📰 Qo'shimcha malumotlari {data[number-1]['description']}"""
            paginator = InlineKeyboardPaginator(
                len(data),
                current_page=number,
                data_pattern='character#{page}'
            )
            self.edit_message(chat_id=self.user.id, message_id=message_id, message=TEXT, reply_markup=paginator.markup)
        else:
            pass


