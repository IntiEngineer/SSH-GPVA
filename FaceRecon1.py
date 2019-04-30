import numpy as np
import cv2
import pickle

faceCascade = cv2.CascadeClassifier('/home/pi/.../CascadeData/haarcascade_frontalface_alt2.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

labels = {}
with open("labels.pickle", 'rb') as f:
    oglabels = pickle.load(f)
    labels = {v:k for k,v in oglabels.items()}

outdoorCam = cv2.VideoCapture(0)

while True:
    # Get data from camera
    _, frame = outdoorCam.read()
    
    # Convert to greyscale
    grey = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    # Use AI to identify and place a face area value
    faces = faceCascade.detectMultiScale(grey, scaleFactor = 1.5, minNeighbors = 5)
    
    # Determine the area where a aface is
    # Region of Interest (ROI)
    for (x, y, w, h) in faces:
        # print(x,y,w,h)
        
        # Add rectangle face overlay
        ROI = frame[y:y+h, x:x+w]
        greyROI = grey[y:y+h, x:x+w]
        rectBGR = (235, 192, 198)
        rectStroke = (2)
        endX = x + w
        endY = y + h
        cv2.rectangle(frame, (x,y), (endX, endY), rectBGR, rectStroke)
        
        id_, conf = recognizer.predict(greyROI)
        if conf >= 50:
            #print(id_)
            print("Attention! " + labels[id_] + " is at the door!")
        
    # Show frame
    #cv2.imshow('Frame', frame) 
    #cv2.imshow('Frame1', grey)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
outdoorCam.release()
cv2.destroyAllWindows()