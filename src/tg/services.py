import requests as re

from src.settings import API_URL
from tg.models import Log
import json


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
    response = re.put(url, data={"messages": json.dumps(log)})
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
    print('url', url)
    data = {
        "menu_log": menu
    }
    response = re.put(url, data=data)
    print("menu_put", response)
    return response.json()['item']


def getRegions():
    url = API_URL + f"g/regions/"
    response = re.get(url)
    response = response.json()['items']
    return response


def getCategory():
    url = API_URL + f"g/category/"
    response = re.get(url)
    print("respone ctg", response.json)
    return response.json()['items']


def searchCategory(category_name):
    url = API_URL + f"g/category/{category_name}"
    response = re.get(url)
    try:
        response = response.json()['item']
    except:
        response = None
    return response


def searchRegion(region_name, region_id=None):
    url = API_URL + f"g/regions/{region_name}"
    response = re.get(url)
    return response.json()['item']


def Districts(region_id):
    pass


def district_by_name(name):
    pass
