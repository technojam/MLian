from flask import Flask, render_template, request, Response
import requests
from flask import redirect, url_for
import cv2
import numpy as np
import face_recognition
import os

app = Flask(__name__)

path = 'UserImage'
images = []
classNames = []
myList = os.listdir(path) 

# print(myList)
for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
# print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList 

encodeListKnown = findEncodings(images)
# print('Encoding Complete')

cap = cv2.VideoCapture(0)
def gen_frames():
    while True:
        success, img = cap.read()
        if not success:
            break
        else:
            imageSmall = cv2.resize(img,(0,0),None,0.25,0.25)
            imageSmall = cv2.cvtColor(imageSmall,cv2.COLOR_BGR2RGB)
            
            facesCurrFrames = face_recognition.face_locations(imageSmall)
            encodeCurrFrame = face_recognition.face_encodings(imageSmall,facesCurrFrames)
            
            for encodeFace, faceLocation in zip(encodeCurrFrame,facesCurrFrames):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                facedistance = face_recognition.face_distance(encodeListKnown,encodeFace)
                #print(facedistance)
                matchIndex = np.argmin(facedistance)
                if matches[matchIndex]:
                    y1,x2,y2,x1 = faceLocation
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,"profile Matched",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                else:
                    y1,x2,y2,x1 = faceLocation
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,"profile Not Matched",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + 
                    b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/result.html',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

if __name__ == '__main__':
    app.run(debug=True)