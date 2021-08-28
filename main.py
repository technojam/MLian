# def register_feed():
import os
import cv2
path = '/UserImage'
cam = cv2.VideoCapture(0)
name=input("Name: ")

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    else:
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            # img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(name + ".jpg", frame)
            # print("{} written!".format(img_name))
            print("Image Captured! Proceed...")
            img_counter += 1

cam.release()

cv2.destroyAllWindows()