import snowboydecoder
import sys
import signal
from pygame import mixer
import speech_recognition as sr
import pyaudio
import wave
from tts import speak
from youtube import get_youtube
from webpusher import push
import requests as rqst
from wiki import do_wiki as wiki
from imagesearch import find_image
from music import play_music,pause_music
#from compliments import do
from news import get_news
import threading
import time

search_music = ""
mixer.music.load("/home/pi/snowboy/resources/ding.wav")

def listen():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = "file.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("record0ing...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    r = sr.Recognizer()
    harvard = sr.AudioFile('file.wav')
    with harvard as source:
        audio = r.record(source)

    type(audio)
    text = r.recognize_google(audio)
    return text


class worker(threading.Thread):

    def run(self):
        t1 = threading.Thread(target=play_music(search_music))
        t1.start()
        got, dur = get_youtube(search_music)
        time.sleep(dur)


def action(text):
    if text.find("YouTube") != -1:
        search_term = text[text.index("play") + 4: text.index("on YouTube")]
        got, dur = get_youtube(search_term)
        list =[got , dur]
        speak("playing" + search_term + "on youtube")
        push("youtube", list)

    elif text.find("turn on lights") != -1:
        rqst.get("http://192.168.1.150:91/?socket=1On")
        speak("turning on lights")

    elif text.find("stop") != -1:
        pause_music()
        push("youtube","stop")
        speak("ok")

    elif text.find("turn off lights") != -1:
        rqst.get("http://192.168.1.150:91/?socket=1Off")
        speak("turning off lights")

    elif text.find("tell me something about") != -1:
        search_wiki = text[text.index("tell me something about") + len("tell me something about"):]
        got_wiki = wiki(search_wiki)
        push("wiki", got_wiki)
        speak(got_wiki)

    elif text.find("play") != 1:
        global search_music
        search_music = text[text.index("play") + len("play"):]

        speak("playing" + search_music)
        worker().start()

    elif text.find("show me a picture of") != 1:
        search_image = text[text.index("show me a picture of") + len("show me a picture of"):].replace(" ", "")
        print(search_image)
        push("images", find_image(search_image))
        speak("ok! heres how" + search_image + "looks ")


interrupted = False

def hotword_detected():
    mixer.music.play()
    text = listen()
    try:
        action(text)
    except:
        speak("Sorry I don't know that one!")
    

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop

detector.start(detected_callback=hotword_detected,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()






