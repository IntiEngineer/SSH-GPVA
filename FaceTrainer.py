import os
import numpy as np
import cv2
import pickle
from PIL import Image

# Set up file, directory, and path
dirBase = os.path.dirname(os.path.abspath(__file__)) # Master directory containing this file
dirImg = os.path.join(dirBase, "FacesForTrainer") # Master directory containing ALL images

faceCascade = cv2.CascadeClassifier('/home/pi/.../CascadeData/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

currentID = 0
labelIDs = {}
yLabels = []
xTrain = []

for root, dirs, files in os.walk(dirImg):
    # Scan each file within dirImg directory
    for file in files:
        # Make sure there are no empty folders!!!
        if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png"):
            # Set path for each image and determine the parent folder (person name) of each image
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "")
            print(label, path)
            if label in labelIDs:
                pass
            else:
                labelIDs[label] = currentID
                currentID += 1
                
            id_ = labelIDs[label]
            #print(labelIDs)
                
            #y_labels.append(label)
            
            # Convert each image to pixel numbers
            pilImage = Image.open(path).convert("L")
            imArray = np.array(pilImage, "uint8")
            # print(imArray)
            
            faces = faceCascade.detectMultiScale(imArray, scaleFactor = 1.5, minNeighbors = 5)            
            for (x, y, w, h) in faces:
                ROI = imArray[y:y+h, x:x+w]
                xTrain.append(ROI)
                yLabels.append(id_)
                
#print(xTrain)
#print(yLabels)

with open("labels.pickle", 'wb') as f:
    pickle.dump(labelIDs, f)
    
recognizer.train(xTrain, np.array(yLabels))
recognizer.save("trainer.yml")

print("Training successful!")

