# main.py
# import the necessary packages
from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2
from timeit import default_timer as timer

app = Flask(__name__)
@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')
def gen(camera):
    while True:
        start = timer()
        frame = camera.get_frame_gpu()
        print("with GPU", timer()-start)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)
