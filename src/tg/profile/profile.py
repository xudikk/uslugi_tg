from tg.user_data import UserData
from .btns import markup_btns, inline_buttons
from ..globals import Texts
from tg.services import get_user_announce, delete_announce
from tg.profile.txt import TEXTS


class Profile(UserData):
    def __init__(self, bot, update, user_model):
        super().__init__(bot, update, user_model)

    def send_trans(self, txt):
        return TEXTS[txt][self.user_model['lang']]

    def received_message(self, msg, txt):
        user_state = self.user_data.get("state", 0)
        lang = self.user_model["lang"]

        if user_state == 0 or txt == TEXTS["BTN_BACK"][lang]:
            self.change_state({"state": 1})
            self.go_message(message=self.send_trans("TEXT_PROFILE"),
                            user_id=self.user.id,
                            reply_markup=markup_btns(type="main", lang=lang))

        elif user_state == 1 or user_state == 0:
            text_menu = TEXTS.get("menu_profile")
            if txt == text_menu["BTN_SET"][lang]:
                self.change_state({"state": 2})
                self.go_message(message=self.send_trans("text_set"),
                                user_id=self.user.id,
                                reply_markup=markup_btns(type="settings", lang=lang))
            elif txt == text_menu["BTN_ADDS"][lang]:
                self.change_state({"state": 2})
                user_announce = get_user_announce(self.user.id)
                text_adds = TEXTS.get("text_adds")
                if user_announce['item'] == None:
                    self.go_message(user_id=self.user.id,
                                    message=text_adds["no_adds"][lang])
                    self.clear_state(1)
                    self.go_message(message=TEXTS["TEXT_PROFILE"][lang],
                                    user_id=self.user.id,
                                    reply_markup=markup_btns(type="main", lang=lang))
                else:
                    announce = self.text_announce(user_announce['item'])
                    self.go_message(message=announce,
                                    user_id=self.user.id,
                                    reply_markup=inline_buttons("button", page=user_announce['meta'],
                                                                data=user_announce['item'], lang=lang))
                    self.go_message(message=TEXTS["back_menu"][lang],
                                    user_id=self.user.id,
                                    reply_markup=markup_btns(type="back", lang=lang))


                # bu yerda barcha shu foydalanuvchiga tegishli bo'lgan barcha elonlarni chiqaruvchi funksiya chaqiriladi
        elif user_state == 2:
            set_menu = TEXTS.get("menu_set")
            if txt == set_menu["change_lang"][lang]:
                self.clear_state(1)
                self.go_message(message=Texts["TEXT_LANG"],
                                user_id=self.user.id,
                                reply_markup=markup_btns(type="s_lang"))

    def inline_query(self, callback_data, message_id=None):
        lang = self.user_model['lang']
        user_state = self.user_data.get("state", 1)
        if user_state == 2:
            if callback_data[:4] == "page":
                call_data = callback_data.split("=")[1]
                user_announce = get_user_announce(self.user.id, call_data)
                announce = self.text_announce(user_announce['item'])
                self.edit_message(chat_id=self.user.id,
                                  message_id=message_id,
                                  message= announce,
                                  reply_markup=inline_buttons("button", page=user_announce['meta'], data=user_announce['item'], lang=lang))

            if callback_data[:6] == "delete":
                text = TEXTS.get("text_adds")
                call_data = callback_data.split("=")[1]
                delete = delete_announce(call_data)
                self.delete_message_user(chat_id=self.user.id,
                                         message_id= message_id)
                self.go_message(user_id=self.user.id,
                                message= text["del_add"][lang])
                user_announce = get_user_announce(self.user.id)
                if user_announce['item'] == None:
                    self.go_message(user_id=self.user.id,
                                    message=text["end_adds"][lang])
                    self.clear_state(1)
                    self.go_message(message=TEXTS["TEXT_PROFILE"][lang],
                                    user_id=self.user.id,
                                    reply_markup=markup_btns(type="main"))
                else:
                    announce = self.text_announce(user_announce['item'])

                    self.go_message(user_id=self.user.id,
                                    message= announce,
                                    reply_markup=inline_buttons("button", user_announce['meta'], data=user_announce['item'], lang=lang))







    def text_announce(self, data):
        lang = int(self.user_model["lang"])
        data_lang = "uz" if lang == 1 else "ru"
        text = TEXTS["message_adds"]
        result = f"""
        {text["emp"][lang]} : {data['fullname']}
        
{text["region"][lang]} : {data[f'region_{data_lang}']}

{text["work"][lang]} : {data[f'category_{data_lang}']}

{text["contact"][lang]} : {data['phone_number']}

{text["price"][lang]} : {data['price']}

{text["desc"][lang]} : {data['description']}
        """

        return result
