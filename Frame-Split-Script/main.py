# 1. Listing all the files
# 2. Iterating through each and cutting each x/2 equation and saving all them into the directory edited

import cv2
from os import listdir
from os.path import isfile, join
from scipy import misc
import scipy.misc
import imageio

mypath = "img/"
editedPath = "edited/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
theImg = cv2.imread(f"{mypath}{onlyfiles[0]}")
height, width, layers = theImg.shape

widthCutoff = width // 2
s1 = theImg[:, :widthCutoff]
s2 = theImg[:, widthCutoff:]

i = 0
cv2.imwrite(f"edited/test1.png", s1)
cv2.imwrite(f"edited/test2.png", s2)

# imageCV = cv2.imread(f"img/{onlyfiles[0]}")
# cv2.imshow("image", imageCV)
# cv2.waitKey(0)
