from tg.user_data import UserData
from telegram import ReplyKeyboardMarkup, KeyboardButton
from .btn import *
from .text import *
from tg.globals import Texts as globals
from tg import services
from tg.models import *
class Announcer(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return Texts[txt][self.user_model['lang']]


    def received_message(self, msg, txt):
        print(" ---------********", f"\n{self.user_data}")
        user_state = self.user_data.get("state", 0)
        print("state: ", user_state)
        lang = self.user_model["lang"]
        if user_state == 0:
            print(self.user.id)
            self.change_state({"state": 1})
            self.go_message(message=self.send_trans("work"), user_id=self.user.id, reply_markup=reply_markup(type=f"work_{lang}"))
        if user_state == 1:
            self.change_state({"state": 2, "work": txt})
            self.go_message(message=self.send_trans("category"), user_id=self.user.id, reply_markup=reply_markup(type=f"cat_{lang}"))
        if user_state == 2:
            if txt == "viloyat":
                self.change_state({"state": 3, "category": txt })
                self.go_message(message=self.send_trans("region"), user_id=self.user.id, reply_markup=reply_markup(type=f"region_{lang}"))
            else:
                self.change_state({"state": 3})
                location_keyboard = KeyboardButton(text="send location", request_location=True)
                self.go_message(message=self.send_trans("location"), user_id=self.user.id, reply_markup=ReplyKeyboardMarkup([[location_keyboard]], resize_keyboard=True))
        if user_state == 10:
            print(txt)
            print(self.user_data)

        if user_state == 3:
            self.change_state({"state": 4, "region": txt})
            self.go_message(message=self.send_trans("price"), user_id=self.user.id, reply_markup=None)
        if user_state == 4:
            if "-" in txt:
                txt = txt.split("-")
                json = {"from": txt[0], "to":txt[1]}
                self.change_state({"state": 5, "price": json})
                self.go_message(message=self.send_trans("FIO"), user_id=self.user.id, reply_markup=None)
            else:
                self.go_message(message=self.send_trans("price"), user_id=self.user.id, reply_markup=None)

        if user_state == 5:
            self.change_state({"state": 6, "fio": txt})
            contact_number = KeyboardButton(text="Contact", request_contact=True)
            self.go_message(message=self.send_trans("contact"), user_id=self.user.id, reply_markup=ReplyKeyboardMarkup([[contact_number]], resize_keyboard=True))
        if user_state == 6:
            self.change_state({"state": 7, "contact": txt})
            self.go_message(message=self.send_trans("description"), user_id=self.user.id, reply_markup=remove_button())
        if user_state == 7:
            self.change_state({"state": 8, "desc": txt})

            self.formation()
            print(self.user_data["work"])
            self.go_message(message=self.send_trans("footer"), user_id=self.user.id, reply_markup=reply_markup(type=f"info_{lang}"))
        elif user_state == 8:
            if txt == "✅ Xa":
                self.change_state({"state": 9})
                user_id = self.user.id
                user = self.user_data
                an = services.create_announce(user, user_id)
                print(an)
                self.go_message(message=self.send_trans("last"), user_id=self.user.id, reply_markup=reply_markup(type=f"footer_{lang}"))
            else:
                self.clear_state()
                self.go_message(message="xabar saqlanmadi", user_id=self.user.id)
                self.go_message(message=globals['TEXT_HOME'][lang], user_id=self.user.id, reply_markup=ReplyKeyboardMarkup([
                    [globals['BTN_CREATE_AD'][lang], globals['BTN_GET_EMP'][lang]],
                    [globals['BTN_PROFILE'][lang]]
                ], one_time_keyboard=True, resize_keyboard=True))
        elif user_state == 9:
            if txt == "Bosh sahifa":
                self.go_message(message=globals['TEXT_HOME'][lang], user_id=self.user.id, reply_markup=ReplyKeyboardMarkup([
                                    [globals['BTN_CREATE_AD'][lang], globals['BTN_GET_EMP'][lang]],
                                    [globals['BTN_PROFILE'][lang]] ], one_time_keyboard=True, resize_keyboard=True))
            else:
                self.change_state({"state": 1})
                self.go_message(message=self.send_trans("work"), user_id=self.user.id, reply_markup=reply_markup(type=f"work_{lang}"))

    # def get_contact_value(update, context):
    #     pass

    def inline_query(self, msg, txt):
        pass


    def formation(self):
        user = self.user_data
        result = f"""👨‍💼 Xodim: {user.get("fio")}
🌐 Hudud: {user.get("region")}
👷 Ish turi: {user.get("work")}
📞 Contact: {user.get("contact")}
💰 Narxi: {user.get("price")}
🔎 Ish xaqida: {user.get("desc")}
        """
        self.go_message(message=result, user_id=self.user.id)
