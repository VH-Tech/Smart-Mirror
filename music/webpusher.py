import pusher
import json

with open('keys.json') as json_file:
  data = json.load(json_file)

pusher_client = pusher.Pusher(
  app_id=data['app_id'],
  key=data['key'],
  secret=data['secret'],
  cluster=data['cluster'],
  ssl=True
)


def push(event, message):
  pusher_client.trigger('my-channel', event, message)
