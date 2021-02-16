import cv2
import urllib.request
import numpy as np
import argparse
import pyautogui # This library provides press control buttons according to image process
import time
time.sleep(2)
pyautogui.FAILSAFE=0
pyautogui.PAUSE=False
lower_green = np.array([50,120,50])
upper_green = np.array([75,255,255])

lower_red = np.array([170,180,70])
upper_red = np.array([180,255,255])

lower_blue = np.array([90,150,70])
upper_blue = np.array([130,255,255])


kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

counter = np.array([0,0,0])

with urllib.request.urlopen(0) as stream:
    bytes = bytearray()
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            ap = argparse.ArgumentParser()
            args = vars(ap.parse_args())
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(image, (340, 220))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv = cv2.medianBlur(hsv,5)
            # Apply mask for red, green and blue color
            # Green
            mask_Green = cv2.inRange(hsv, lower_green, upper_green)
            maskOpen_Green = cv2.morphologyEx(mask_Green, cv2.MORPH_OPEN, kernelOpen)
            maskClose_Green = cv2.morphologyEx(maskOpen_Green, cv2.MORPH_CLOSE, kernelClose)
            # Red
            mask_Red = cv2.inRange(hsv, lower_red, upper_red)
            maskOpen_Red = cv2.morphologyEx(mask_Red, cv2.MORPH_OPEN, kernelOpen)
            maskClose_Red = cv2.morphologyEx(maskOpen_Red, cv2.MORPH_CLOSE, kernelClose)
            # Blue
            mask_Blue = cv2.inRange(hsv, lower_blue, upper_blue)
            maskOpen_Blue = cv2.morphologyEx(mask_Blue, cv2.MORPH_OPEN, kernelOpen)
            maskClose_Blue = cv2.morphologyEx(maskOpen_Blue, cv2.MORPH_CLOSE, kernelClose)

            conts_Green, h = cv2.findContours(maskClose_Green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for i in range(len(conts_Green)):
                x, y, w, h = cv2.boundingRect(conts_Green[i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if cv2.rectangle is not None:
                    if w > 30 and h > 30:
                        cv2.putText(img, "Green", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        counter[0]+=1


            conts_Red, h = cv2.findContours(maskClose_Red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for i in range(len(conts_Red)):
                x, y, w, h = cv2.boundingRect(conts_Red[i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if cv2.rectangle is not None:
                    if w > 30 and h > 30:
                        cv2.putText(img, "Red", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        counter[1]+=1


            conts_Blue, h = cv2.findContours(maskClose_Blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for i in range(len(conts_Blue)):
                x, y, w, h = cv2.boundingRect(conts_Blue[i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if cv2.rectangle is not None:
                    if w > 30 and h>30:
                        cv2.putText(img, "Blue", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                        counter[2]+=1


            if counter.sum()>6:
                result = np.where(counter == np.amax(counter))[0]
                try:
                    if result == 1:
                        pyautogui.press('s')
                        time.sleep(0.1)
                        print("S")
                    elif result==2:
                        pyautogui.press('left')
                        time.sleep(0.1)
                        print("B")
                    elif result==0:
                        pyautogui.press('right')
                        time.sleep(0.1)
                        print("G")
                    counter= np.array([0,0,0])
                except:
                    pass


            cv2.imshow("Green", maskClose_Green)
            cv2.imshow("Blue", maskClose_Blue)
            cv2.imshow("Red", maskClose_Red)
            cv2.imshow("cam", img)
            cv2.imshow("hsv",hsv)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    cv2.destroyAllWindows()