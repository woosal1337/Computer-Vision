# 1. Listing all the files
# 2. Iterating through each and cutting each x/2 equation and saving all them into the directory edited

import cv2
from os import listdir
from os.path import isfile, join

mypath = "img/"
editedPath = "edited/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

z = 0

for i in range(len(onlyfiles)):
    theImg = cv2.imread(f"{mypath}{onlyfiles[i]}")
    height, width, layers = theImg.shape

    widthCutoff = width // 2
    s1 = theImg[:, :widthCutoff]
    s2 = theImg[:, widthCutoff:]


    cv2.imwrite(f"edited/test{z}.png", s1)
    z += 1

    cv2.imwrite(f"edited/test{z}.png", s2)
    z += 1

    print("Working on image number {}".format(i))

print("Finished!")