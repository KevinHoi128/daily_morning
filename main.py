from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
wedding_date = os.environ['WEDDING_DATE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

jpweather_id = os.environ["JPWEATHER_ID"]


def get_weather():
  url = "https://devapi.qweather.com/v7/weather/now?key=" + jpweather_id + "&location=101330101"
  res = requests.get(url).json()
  weather = "࿓現在溫度:" + res['now']['temp'] + "度, 體感溫度:" + res['now']['temp'] + "度, 會是" + res['now']['text'] + "天氣, 吹" + res['now']['windDir'] + "༄"
  return weather

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# def get_birthday():
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

def get_wedding_days():
  delta = today - datetime.strptime(wedding_date, "%Y-%m-%d")
  return delta.days

def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
    words = requests.get("https://api.uomg.com/api/rand.qinghua")
    return "❤" + words.content + "❤"
#   return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea = get_weather()
# "birthday_left":{"value":get_birthday()},
data = {"weather":{"value":wea, "color":get_random_color()},"love_days":{"value":get_count(), "color":get_random_color()}, "wedding_days":{"value":get_wedding_days(), "color":get_random_color()}, "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
