from tg.user_data import UserData
from .btns import markup_btns


class Profile(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def received_message(self, msg, txt):
        user_state = self.user_data.get("state",1)
        print(user_state)
        if user_state == 0:
            self.change_state({"state": 1})
            self.go_message(message="Profile bo'limlaridan birini tanlang!",
                            user_id=self.user.id,
                            reply_markup=markup_btns(type="main"))
        elif user_state == 1:
            print("aaaa")

    def inline_query(self, msg, txt):
        pass