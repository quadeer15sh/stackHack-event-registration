import cv2
import os
import base64
import numpy as np

def detect_image(img):
    cwd = os.getcwd()
    url = os.path.join(cwd,'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(url)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces)!=0:
        return len(faces)
    else:
        return 0

def cropped_image(img):
    cwd = os.getcwd()
    url = os.path.join(cwd,'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(url)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cropped = img[ y : y+h, x : x+w ]
    
    ret, frame_buff = cv2.imencode('.jpg', cropped) #could be png, update html as well
    frame_b64 = base64.b64encode(frame_buff)
 
    return frame_b64

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img