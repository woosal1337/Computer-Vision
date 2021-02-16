import cv2
import numpy as np


while True:
    try:
        cap = cv2.VideoCapture("http://192.168.43.87/capture")
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red color
        low_red = np.array([-20, 120, 255])
        high_red = np.array([75, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)

        red = cv2.bitwise_and(frame, frame, mask=red_mask)

        # Blue color
        low_blue = np.array([95,45,35])
        high_blue = np.array([110,255,255])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)

        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

        # Green color
        low_green = np.array([25, 52, 72])
        high_green = np.array([83, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)

        green = cv2.bitwise_and(frame, frame, mask=green_mask)




        cv2.imshow("Frame", frame)
        cv2.imshow("Red", red)
        cv2.imshow("Green", green)
        cv2.imshow("Blue", blue)

        def helloblue():
            print("Hello Blue!")

        def hellored():
            print("Hello Red!")

        def hellogreen():
            print("Hello Green!")

        b = cv2.countNonZero(blue_mask)
        r = cv2.countNonZero(red_mask)
        g = cv2.countNonZero(green_mask)

        if b >= r and b >= g:
            helloblue()
        elif r >= b and r >= g:
            hellored()
        elif g >= b and g >= r:
            hellogreen()



        key = cv2.waitKey(1)
        if key == 27:
            break

    except:
        continue