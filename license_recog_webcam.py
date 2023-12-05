# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 19:47:32 2023

@author: samar
"""

from ultralytics import YOLO
import cv2
import math 
import pytesseract
import datetime
import numpy as np
import csv
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\samar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("license_plate.pt")

# object classes
classNames = ["license-plate","car"]

while True:
    success, img = cap.read()
    results = model(img, stream=True)
    img = cv2.resize(img, None, fx=1.15, fy=1.15, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.convertScaleAbs(img, 50, 1)
    thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 0)
    dist = cv2.normalize(thresh, thresh, 0, 1.0, cv2.NORM_MINMAX)
    dist = (dist * 255).astype("uint8")
    dist = cv2.threshold(dist, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    img = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
    #kernel = np.ones((11, 11), np.uint8)
    #img = cv2.dilate(img, kernel, iterations=1)
    #img = cv2.erode(img, kernel, iterations=1)
    custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 --psm 6'
    
    # coordinates
    for r in results:
        boxes = r.boxes
        tList = []
        tsList = []
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            k= cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            
            text1 = pytesseract.image_to_string(k,config=custom_config)
            #print(text1)
            #print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            tm = datetime.datetime.now()
            tList.append(text1)
            tsList.append(tm)
            
            # confidence
            #confidence = math.ceil((box.conf[0]*100))/100
            #print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            #print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls] ,org, font, fontScale, color, thickness)
            
        if len(tList) == 2 and tList[0] == tList[1]:
            print("Done!")
            a = tList[0]
            b = tsList[0]
            dict = {'License-Plate': tList , 'Time': tsList}
            df = pd.DataFrame(dict)
            df.to_csv('data1.csv')
            
        if len(tList) > 2 and tList[0] != tList[1]:
            tList.clear()
            tsList.clear()
            print("Trying Again")
            
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()