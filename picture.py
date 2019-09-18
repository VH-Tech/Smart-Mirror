from webpusher import push
import datetime
import cv2


def click_picture():
    cap = cv2.VideoCapture('rtsp://192.168.2.181')

    ret, frame = cap.read()
    stamp = datetime.datetime.now().strftime("%X").replace(':', '')
    cv2.imwrite("photos/" + stamp + '.png', frame)
    cv2.imshow('frame', frame)
    cap.release()
    push('image_clicked', "photos/" + stamp)


