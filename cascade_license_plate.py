import cv2
import pytesseract
import datetime
import numpy as np
import csv
import pandas as pd
import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\samar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Load the pre-trained license plate cascade classifier
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

# Open a connection to the webcam (you may need to change the index based on your system)
cap = cv2.VideoCapture(1)

tList = []
tsList = []

flag = False

while True:
    
    custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 --oem 3 --psm 6'
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    frame = cv2.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    
    # Convert the frame to grayscale for license plate detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    _, thresh =  cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    #inverted = cv2.bitwise_not(eroded)
    
    #thresh = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    #dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 0)
    #dist = cv2.normalize(thresh, thresh, 0, 1.0, cv2.NORM_MINMAX)
    #dist = (dist * 255).astype("uint8")
    #frame = cv2.threshold(dist, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    #frame = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
    #kernel = np.ones((5, 5), np.uint8)
    #frame = cv2.dilate(frame, kernel, iterations=1)
    #frame = cv2.erode(frame, kernel, iterations=1)
    
    
    # Perform license plate detection
    plates = plate_cascade.detectMultiScale(eroded, scaleFactor=1.75, minNeighbors=5, minSize=(30, 30))
    
    # Draw rectangles around detected license plates
    for (x, y, w, h) in plates:
        k = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text1 = pytesseract.image_to_string(k,config=custom_config)
        desired_length = 10
        filtered_words = [word for word in text1.split() if len(word) == desired_length]
        tm = datetime.datetime.now()
        
        print(filtered_words)
        tList.append(filtered_words)
        
        
        #if len(text1) > 8:
            #print(text1)
            #tList.append(text1)
            #tsList.append(tm)
            
        if len(tList) == 2 and tList[0] == tList[1]:
            print("Done!")
            a = tList[0]
            b = [tm]
            dict = {'License-Plate': [a] , 'Time': b}
            df = pd.DataFrame(dict)
            df.to_csv('data1.csv')
            flag = True
            tList.clear()
            tsList.clear()
            
        #if len(tList) > 2 and tList[0] != tList[1]:
            #tList.clear()
            #tsList.clear()
            #print("Trying Again")
        
    # Display the result
    cv2.imshow('License Plate Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
