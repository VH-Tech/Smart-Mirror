import houndify.houndify as hd
import json

with open('keys.json') as json_file:
    data = json.load(json_file)


clientId = data["clientId"]
clientKey = data["clientKey"]
userId = "test_user"
requestInfo = {
  "Latitude": data["Latitude"],
  "Longitude": data["Longitude"]
}

client = hd.TextHoundClient(clientId, clientKey, userId, requestInfo)


def hound(text):
    response = client.query(text)
    return response["AllResults"][0]["SpokenResponse"]

