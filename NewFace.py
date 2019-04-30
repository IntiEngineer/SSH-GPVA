import os
import numpy as np
import cv2

# Set up file, directory, and path
dirBase = os.path.dirname(os.path.abspath(__file__)) # Master directory containing this file
dirImg = os.path.join(dirBase, "FacesForTrainer") # Master directory containing ALL images

newname = input("Who would you like to add?\n").replace(" ", "")

os.mkdir("FacesForTrainer/" + newname)
cap = cv2.VideoCapture(0)
count = 0

while True:
    # Get data from camera
    _, frame = cap.read()
    
    key = cv2.waitKey(1)
    
    cv2.imshow('Frame', frame) 
    
    if key == 32:
        cv2.imwrite("FacesForTrainer/" + newname + "/" + newname + str(count) + ".png",frame)
        count+=1
    
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()

print("Please run Training file.")