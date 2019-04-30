# Granny Pod Virtual Assistant
# Programmer: David Connolly
# Published: April 29, 2019
# Version: GPVA V1.0.0
#
# Code References:
# OpenCV Facial Recognition code is provided by CodingEntrepreneurs (www.youtube.com/user/CodingEntrepreneurs)
# IOT ngrok and Flask localhost software is provided by Nassir Mamlik (Netmedias on Youtube)
# Description:
# This program simultaneously both functions of the Granny Pod
# 
# Main Function 1: Front Door Facial Alert - Repeated camera scan on camera 1 (outdoor camera) and facial
# recognition of any identified faces with OpenCV. Upon facial recognition, the identified face
# will play this message through the speaker: "Attention. ____________ is at the door." Where the
# blank space is the name of the person identified. 
# 
# Main Function 2: Help Needed Message - If the SSH resident says: "Hey Google" or "Okay Google, then proceed
# say "I need help", "Help me", or "Please help", then the Google Home will respond by saying
# "Help is on the way". Then it will call the SSH resident's guardian's phone with a message saying
# "__________ is in need of help". A message will also be sent with a picture from the indoor camera (optional)
# and a text message saying "__________ is in need of help". 

# Privacy and Security
# All name and imagery data is handled by the different imported python libraries. Any data used by GPVA
# not handled by a library is solely handled by the Raspberry Pi and is subject to the internet
# security of the Pi. An internet connection is required for the GPVA, which may put the
# Raspberry Pi at risk. All images posted online are deleted 5 minutes after use. Images used for facial
# recognition training and previously sent pictures in the GPVA folder are retained. For Help Needed
# Message, the message containing the picture from indoors is transmitted over the internet and is stored
# unencrypted for 5 minutes on the internet cloud, before being deleted. This presents a security risk
# which is why this feature is optional and is activated with a flag in the settings section.

#Python library imports
from twilio.rest import Client # For sending texts over the internet
import requests                # For sending images online with POST requests
import numpy as np
import cv2                     # Computer vision library for 
import pickle                  # For storing face training
import time                    # For pausing all processing for a limited time
from gtts import gTTS          # Text to speech converter
import pygame                  # Software made for Raspi with audio player

# Settings
sendIndoorsPicture = True # For privacy reasons, the online
# unidentifiedPersonAlert = False # Feature not implemented is this version

# Presets =============================================================
# imgBB user credential values
imgBBAPIkey = 'YOUR imgBB API KEY HERE'

# Twilio user credential values at https://twilio.com/user/account
account_sid = "YOUR SID HERE"
auth_token = "YOUR TOKEN HERE"
# Phone number format: '+1ZZZ#######'
twilioPhNumber = 'YOUR TWILIO GIVEN PHONE NUMBER HERE'
targetPhNumber = 'YOUR DESTINATION GIVEN PHONE NUMBER HERE'

# Camera set-ups
outdoorCam = cv2.VideoCapture(0)
indoorCam = cv2.VideoCapture(1)

# Intitial sound mixer
pygame.mixer.init()

# Recognition presets
faceCascade = cv2.CascadeClassifier('/home/pi/Documents/.../CascadeData/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml') # Load training data
labels = {} # List for possible recognized faces
with open("labels.pickle", 'rb') as f: # Fill list with recognizable face names 
        oglabels = pickle.load(f)
        labels = {v:k for k,v in oglabels.items()}

# Main loop runs forever until esc button is pressed
while True :
    # Function 2: Help Needed Message ===================================
    status = open("GoogleHomeStatus.txt",'r')
    statusText = status.readline()
    status.close()
    
    if statusText == 'help' and sendIndoorsPicture == True : # Condition webhooks from IFTTT
        # Take picture of indoors
        _, frame1 = indoorCam.read()
        cv2.imwrite('indoorPicture.png', frame1)
        
        # Upload image of indoors online to imgBB with imgBB API for transmission
        # Set imgBB upload url with user credentials 
        url = 'https://api.imgbb.com/1/upload?key=' + imgBBAPIkey
        payload = {'image': open('indoorPicture.png', 'rb')}
        
        # Send image to imgBB and recieve returning url for how to access it 
        r = requests.post(url, files=payload)
        
        # Extract url
        r_dict = r.json()
        imageURL = r_dict['data']['url']
        
        # Apply user credentials
        client = Client(account_sid, auth_token)
        
        # Send message with picture
        message = client.messages.create(
                              body='Granny is in need of help!',
                              from_= twilioPhNumber,
                              media_url=imageURL,
                              to=targetPhNumber
                          )
        # Clear Google Home status
        status = open("GoogleHomeStatus.txt",'w')
        status.write('no')
        status.close()
    
    if statusText == 'help' and sendIndoorsPicture == False :
        # Apply user credentials
        client = Client(account_sid, auth_token)
        
        # Send message with picture
        message = client.messages.create(
                              body='Granny is in need of help!',
                              from_= twilioPhNumber,
                              to=targetPhNumber
                          )
        # Clear Google Home status
        status = open("GoogleHomeStatus.txt",'w')
        status.write('no')
        status.close()
        
        
    # Function 1: Front Door Facial Alert =================================
    # Get data from camera
    _, frame0 = outdoorCam.read()
    
    # Convert to greyscale
    grey = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
    
    # Use AI to identify and place a face area value
    faces = faceCascade.detectMultiScale(grey, scaleFactor = 1.5, minNeighbors = 5)
    
    # Determine the area where a face is
    # Region of Interest (ROI)
    for (x, y, w, h) in faces:
        # Add rectangle face overlay
        ROI = frame0[y:y+h, x:x+w]
        greyROI = grey[y:y+h, x:x+w]
        
        # Identify face
        id_, conf = recognizer.predict(greyROI)
        if conf >= 40:
            # Convert text to Google Voice and save to a file
            text = "Attention! " + labels[id_] + " is at the door."
            tts = gTTS(text, 'en-uk')
            tts.save('WhosAtTheDoor.mp3')
            
            # Play message off who's at the door
            pygame.mixer.music.load('WhosAtTheDoor.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True :
                continue
            
            # Pause program to allow for break in facial recognition
            time.sleep(20)
    
    # Press esc to exit program
    key = cv2.waitKey(1)
    if key == 27:
        break


outdoorCam.release()
indoorCam.release()
cv2.destroyAllWindows()