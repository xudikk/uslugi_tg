import requests as re

from src.settings import API_URL
from tg.models import Log


def create_tg_user(user):
    print("qwe")
    url = API_URL + f"user/"
    print("qwe")
    data = {
        "user_id": user.id,
        "user_name": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    response = re.post(url, data=data)
    print("postuser", response.json())
    return response.json()['item']


def get_user(user_id):
    url = API_URL + f"user/{user_id}/"
    response = re.get(url)
    print("getu", response)
    return response.json()['item']


def get_user_log(user_id):
    url = API_URL + f"log/{user_id}/"
    response = re.get(url)
    print("get", response)
    return response.json()['item']


def create_log(user_id):
    url = API_URL + f"log/{user_id}/"
    response = re.post(url, data={"user_id": user_id})
    print("post", response)
    return response.json()['item']


def change_log(user_id, log):
    url = API_URL + f"log/{user_id}/"
    response = re.put(url, data={"messages": log})
    print("post", response)
    return response.json()['item']


def tgChangeLang(user_id, lang):
    url = API_URL + f"user/{user_id}/"
    data = {
        "lang": lang
    }
    response = re.put(url, data=data)
    print("lang_put", response)
    return response.json()['item']


def userChangeMenu(user_id, menu):
    url = API_URL + f"user/{user_id}/"
    data = {
        "menu_log": menu
    }
    response = re.put(url, data=data)
    print("menu_put", response)
    return response.json()['item']
