import cv2 
import numpy as np
import matplotlib.pyplot as plt
import time

from picamera import PiCamera
import picamera.array
from flask import Flask

ALLOWED_AREA = np.array([
    [[0, 0], [200, 0], [200, 240], [0, 240]]
])

DENIED_AREA = np.array([
    [[200, 0], [320, 0], [320, 240], [200, 240]]
])
ALLOWED_COLOR = (66, 183, 42)
DENIED_COLOR = (0, 0, 255)

picam = PiCamera()
picam.framerate = 10
picam.resolution = (320, 240)
picam.rotation = 180

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


def capture_image():
    raw_capture = picamera.array.PiRGBArray(picam)
    picam.capture(raw_capture, format='rgb', use_video_port=True)
    img = raw_capture.array.astype('uint8')
    return img

  
# Trained XML classifiers describes some features of some object we want to detect 
car_cascade = cv2.CascadeClassifier('cars.xml') 
  
def applyTransparentMask(frames):
    base = np.zeros(frames.shape, dtype='uint8')
    exit_mask = cv2.fillPoly(base, DENIED_AREA, (255, 255, 255))[:, :, 0]
    _img = np.zeros(frames.shape, frames.dtype)
    _img[:, :] = DENIED_COLOR
    mask = cv2.bitwise_and(_img, _img, mask=exit_mask)
    cv2.addWeighted(mask, 1, frames, 1, 0, frames)

isLastFrameDetected = False
# loop runs if capturing has been initialized. 
while True: 

    image = capture_image()
    # convert to gray scale 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    # apply a mask to allowed area to exclude that area from detection
    cv2.fillPoly(gray, ALLOWED_AREA, (255, 255, 255))
    # Detects cars of different sizes in the input image 
    cars = car_cascade.detectMultiScale(gray, 1.1, 1) 
    print(cars)
    if type(cars) is list and cars.size > 0 and isLastFrameDetected == False:
        start = time.time()
    elif type(cars) is tuple and cars.any() and isLastFrameDetected == True:
        elapsedTimeOnTrack = start - time.time()
        print(elapsedTimeOnTrack)
        isLastFrameDetected = False

    # To draw a rectangle in each cars 
    for (x,y,w,h) in cars: 
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2) 
  
    # apply red transparent mask on the denied area
    applyTransparentMask(image)
    # Display frames in a window  
    cv2.imshow('video2', image) 
      
    # Wait for Esc key to stop 
    if cv2.waitKey(33) == 27: 
        break
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()
picam.close()
