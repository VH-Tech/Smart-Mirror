
from webpusher import push
import datetime
import threading
import time

morning = ["Good morning!", "feeling sleepy?", "Good to see you back!"]
afternoon = ["Good Afternoon!" , "Whats up!?" , "How may I help?"]
evening = ["Good Evening!", "Whats up!?", "How may I help?"]
night = ["Good Night!", "See you tomorrow", "How may I help?"]


def check_time():
    current_time = datetime.datetime.now().hour
    if current_time <= 12:
        compliments = morning
        time_left_for_next = 12 - current_time
        return compliments, time_left_for_next

    elif current_time <= 16:
        compliments = afternoon
        time_left_for_next = 16 - current_time
        return compliments, time_left_for_next

    elif current_time <= 19:
        compliments = evening
        time_left_for_next = 20 - current_time
        return compliments, time_left_for_next

    else:
        compliments = night
        time_left_for_next = 24 - current_time
        return compliments, time_left_for_next


def do():

    (compliments, time_left_for_next) = check_time()
    push("compliments", compliments)


do()

