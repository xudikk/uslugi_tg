from tg.user_data import UserData


class Profile(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def received_message(self, msg, txt):
        self.go_message(message="profile keldi", user_id=self.user.id)

    def inline_query(self, msg, txt):
        pass