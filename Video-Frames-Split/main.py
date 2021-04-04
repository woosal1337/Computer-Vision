import cv2
import numpy as np

cap = cv2.VideoCapture("video.mp4")

if not cap.isOpened():
    print("There has happened an error while opening the specified video file.")

i = 0

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:
        i += 1

        cv2.imshow("Frame", frame)
        cv2.imwrite(f"frames/frame{i}.png", frame)

        if cv2.waitKey(25) == ord("q"):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
