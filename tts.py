# You need to install pyaudio to run this example
# pip install pyaudio

# In this example, the websocket connection is opened with a text
# passed in the request. When the service responds with the synthesized
# audio, the pyaudio would play it in a blocking mode

from __future__ import print_function
from ibm_watson import TextToSpeechV1
from ibm_watson.websocket import SynthesizeCallback
import pyaudio
import json

# If service instance provides API key authentication

with open('keys.json') as json_file:
    data = json.load(json_file)
    to_url = data['watson_url']
    apikey = data['iam_apikey']

service = TextToSpeechV1(
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    url=to_url,
    iam_apikey=apikey)

# service = TextToSpeechV1(
#     ## url is optional, and defaults to the URL below. Use the correct URL for your region.
#     # url='https://stream.watsonplatform.net/text-to-speech/api,
#     username='YOUR SERVICE USERNAME',
#     password='YOUR SERVICE PASSWORD')

class Play(object):
    """
    Wrapper to play the audio in a blocking mode
    """
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 22050
        self.chunk = 1024
        self.pyaudio = None
        self.stream = None


    def start_streaming(self):
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self._open_stream()
        self._start_stream()

    def _open_stream(self):
        stream = self.pyaudio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk,
            start=False
        )
        return stream

    def _start_stream(self):
        self.stream.start_stream()

    def write_stream(self, audio_stream):
        self.stream.write(audio_stream)

    def complete_playing(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

class MySynthesizeCallback(SynthesizeCallback):
    def __init__(self):
        SynthesizeCallback.__init__(self)
        self.play = Play()

    def on_connected(self):
        print('Opening stream to play')
        self.play.start_streaming()

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_timing_information(self, timing_information):
        print(timing_information)

    def on_audio_stream(self, audio_stream):
        self.play.write_stream(audio_stream)

    def on_close(self):
        print('Completed synthesizing')
        self.play.complete_playing()

test_callback = MySynthesizeCallback()

# An example SSML text
SSML_sorry_text = """<speak version=\"1.0\">
        <emphasis> I am sorry, I know how it feels.</emphasis>
        </speak>"""

# Another example of SSML text
SSML_text = """
       Good morning sir how may i help?
   """


def speak(text):

    service.synthesize_using_websocket(text,
                                   test_callback,
                                   accept='audio/wav',
                                   voice="en-US_MichaelVoice"
                                  )

