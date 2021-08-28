# Team MLian
## Automatic Age verification System
---
 ### Info: 

This project verifies the identity of the user using facial recognition technology.
__________________________
 ### Features:
1. New users can register with their details and their face-id. Their image will be saved using webcam.
2. Old users can login by getting their face image verified only. The image they registered with previously will be used for verfication.
3. If verified, the system will allow the user to proceed.
__________________________
### Use Cases
1. Age verification system can be used for age restricted spaces, ie. alcoholic stores and heavy drugs stores.
2. Basic facial recognition and face-id registration features can be used for personnel restricted spaces, ie. banks, special corporate spaces, government organisations etc.
3. Applications with user restricted access.
__________________________
### Technologies Used
1. Frontend - HTML, CSS
2. Framework - [Flask](https://flask.palletsprojects.com/en/2.0.x/)
3. Facial Recognition - [Dlib](http://dlib.net/), [OpenCV](https://docs.opencv.org/master/).
__________________________
### How To Run It
1. Installing dependencies

    `pip install -r requirements.txt` 

2. Running

    `flask run`

- When you run `flask run` on the terminal, a local host link should appear. Open this link in your browser to view the project.

- Ensure you have installed Desktop developement with C++ componenets using Visual Studio Installer and CMake to install dlib and face_recognition.

## Demo: https://mlian.herokuapp.com/

