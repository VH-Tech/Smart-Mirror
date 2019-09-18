import feedparser
from webpusher import push
import json


with open('keys.json') as json_file:
    data = json.load(json_file)
    feed = data['rssfeeds'].split(",")

headlines = []


def get_news(count, feed):
    newsfeed = feedparser.parse(feed)
    title = []

    for i in range(count):
        entry = newsfeed.entries[i]
        title.append(entry.title)

    return title


for i in feed:
    headlines += get_news(4, i)

push("news", headlines)


