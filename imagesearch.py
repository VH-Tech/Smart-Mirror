import json
from urllib.request import urlopen
import json

with open('keys.json') as json_file:
    data = json.load(json_file)
    base_url=data['google_image_search_url']


def find_image(search_term):
    url_to_open = base_url + '&q=' + search_term.strip().replace(" ", "_") + "&searchType=image&imgSize=huge"
    print(url_to_open)
    url = urlopen(url_to_open).read()
    my_json = url.decode("utf-8")
    obj = json.loads(my_json)
    image = obj["items"][0]["image"]["thumbnailLink"]
    return image

