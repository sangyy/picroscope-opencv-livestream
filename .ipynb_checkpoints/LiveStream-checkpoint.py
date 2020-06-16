from flask import Flask, Response
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import io

class Camera(object):
    def __init__(self):
        self.cam = PiCamera()
        self.cam.resolution = (640, 480)
        self.rawCapture = PiRGBArray(self.cam, size=(640,480))

    def get_frame(self):
        for frame in self.cam.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            cv2.imwrite('blah.jpg',image)
            self.rawCapture.truncate(0)
            return open('blah.jpg', 'rb').read()

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.route('/')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
