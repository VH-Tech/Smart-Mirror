#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.request import urlopen
import json
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

with open('keys.json') as json_file:
    data = json.load(json_file)
    youtube_key = data['youtube_v3']

DEVELOPER_KEY = youtube_key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options,
    part='id,snippet',
    maxResults=10
  ).execute()

  videos = []

  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append(search_result['id']['videoId'])

  return videos[0]


def get_youtube(term):
    try:
        ref = youtube_search(term)
        searchUrl = "https://www.googleapis.com/youtube/v3/videos?id=" + ref + "&key=" + DEVELOPER_KEY + "&part=contentDetails"
        response = urlopen(searchUrl).read()
        my_json = response.decode("utf-8")
        data = json.loads(my_json)
        all_data = data['items']
        contentDetails = all_data[0]['contentDetails']
        duration = contentDetails['duration']

        mins = int(duration[duration.index("PT") + len("PT"): duration.index("M")]) * 60
        secs = int(duration[duration.index("M") + len("M"): duration.index("S")])
        total_dur = mins + secs

        return ref, total_dur

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


