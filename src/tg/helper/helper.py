from tg.globals import Texts
from tg.user_data import UserData


class Helper(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]

    def received_message(self, msg, txt):
        user_state = self.user_data.get("state", 0)
        if user_state == 0:
            self.go_message(message="ss", user_id=self.user.id)

    def inline_query(self, msg, txt):
        pass

