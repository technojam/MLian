from flask import *
import requests
from flask import redirect, url_for
import cv2
import numpy as np
import face_recognition
import os
# from main.py import register_feed()

app = Flask(__name__)

#################################START######################################################
#Login page code
def gen_frames():
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
    # def gen_frames():
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
                    case:ProfileMatched
                else:
                    y1,x2,y2,x1 = faceLocation
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,"profile Not Matched",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    case:ProfileNotMatched
                    
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + 
                    b'\r\n')

#####################################END######################################

#################################START######################################################
#Register page code

def register_feed():
    import os
    import cv2
    path = '/UserImage'
    cam = cv2.VideoCapture(0)
    name=input("Name: ")

    # cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        else:
            # cv2.imshow("test", frame)
            img_saved = cv2.imwrite(f"UserImage\image{img_counter}.jpeg", frame)

            if img_saved:
                imageSmall = cv2.resize(frame,(0,0),None,0.25,0.25)
                imageSmall = cv2.cvtColor(imageSmall,cv2.COLOR_BGR2RGB)
                facesCurrFrames = face_recognition.face_locations(imageSmall)
                encodeCurrFrame = face_recognition.face_encodings(imageSmall,facesCurrFrames)
                for encodeFace, faceLocation in zip(encodeCurrFrame,facesCurrFrames):
                    y1,x2,y2,x1 = faceLocation
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.putText(frame,"Your image saved",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) 
                img_counter += 1

            cam.release()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + 
                b'\r\n')

    # cam.release()

    # cv2.destroyAllWindows()


#####################################END######################################





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/login_cam')
def login_cam():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register_cam')
def register_cam():
    return Response(register_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
