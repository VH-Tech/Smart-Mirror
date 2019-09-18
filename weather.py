import json
from urllib.request import urlopen
from webpusher import push

with open('keys.json') as json_file:
    data = json.load(json_file)
    darksky_url=data['darksky_url']


def get_weather():
    url_to_open = darksky_url
    url = urlopen(url_to_open).read()
    my_json = url.decode("utf-8")
    obj = json.loads(my_json)
    weather = obj["currently"]
    return weather


def calc_weather():
    weather = get_weather()
    icon = weather["icon"]
    temperature = weather['temperature']
    to_push = icon.replace("-", "_").upper()
    push("weather", [to_push, temperature])
    print(to_push)

calc_weather()

