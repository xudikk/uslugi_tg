from tg.globals import Texts
from tg.user_data import UserData
from tg import services
from telegram import ReplyKeyboardMarkup, ReplyMarkup

class Helper(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]

    def received_message(self, msg, txt, text):
        user_state = self.user_data.get("state", 0)
        buttons = self.render_buttons(txt)
        reply_murkup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if user_state == 0:
            self.change_state({"state": 1})
            self.go_message(message="Viloyatlardan birini tanlang", user_id=self.user.id, reply_markup=reply_murkup)
        if user_state == 1:
            print('data', text)
            data = services.searchRegion(text)

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

    def inline_query(self, msg, txt):
        pass

