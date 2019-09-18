from __future__ import unicode_literals
import youtube_dl
from youtube import get_youtube
import os
from webpusher import push


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def play_music(music_name):
    yt_name = get_youtube(music_name)[0]
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + yt_name])

    os.rename('_-' + yt_name + '.wav', "music/" + music_name + ".wav")

    push("music", music_name)

