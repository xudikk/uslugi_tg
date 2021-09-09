from tg.user_data import UserData
from .btns import markup_btns
from ..globals import Texts


class Profile(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        print("ASD", txt)
        return Texts[txt][self.user_model['lang']]

    def received_message(self, msg, txt):
        user_state = self.user_data.get("state", 0)
        print(self.user_data)
        if user_state == 0:
            self.change_state({"state": 1})
            self.go_message(message="Profile bo'limlaridan birini tanlang!",
                            user_id=self.user.id,
                            reply_markup=markup_btns(type="main"))
        elif user_state == 1 or user_state == 0:
            if txt == "Sozlamalar":
                self.change_state({"state": 2})
                self.go_message(message="Kerakli sozlamalarni tanlang",
                                user_id=self.user.id,
                                reply_markup=markup_btns(type="settings"))
            elif txt == "Mening e'lonlarim":
                self.clear_state(1)
                self.go_message(message="Bu qism hali tayyor emas",
                                user_id=self.user.id)
                # bu yerda barcha shu foydalanuvchiga tegishli bo'lgan barcha elonlarni chiqaruvchi funksiya chaqiriladi
        elif user_state == 2:
            if txt == "Tilni o\'zgartirish":
                self.clear_state(1)
                self.go_message(message=Texts["TEXT_LANG"],
                                user_id=self.user.id,
                                reply_markup=markup_btns(type="s_lang"))

    def inline_query(self, msg, txt):
        # inline profileda edit qismi uchun kerak bo'ladi

        pass
