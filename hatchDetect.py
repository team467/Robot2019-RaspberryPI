import numpy as np
import cv2
import math

def isHatch(frame):
    #cap = frame
    #cv2.VideoCapture("http://10.0.1.112:1181/stream.mjpg")
    #cap = cv2.VideoCapture(0)
    #20, 120, 120
    #50, 255, 255
    lower_yellow = np.array([20, 110, 110])
    upper_yellow = np.array([100, 255, 255])
    lower_grey = np.array([80, 90, 90])
    upper_grey = np.array([120, 130, 130])
    
    #hatch = False
    #check, frame = cap.read()
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur = cv2.blur(frame,(8, 8))
    mask1 = cv2.inRange(blur, lower_yellow, upper_yellow)
    mask2 = cv2.inRange(blur, lower_grey, upper_grey)
    mask = mask1 + mask2
    res = cv2.bitwise_and(frame, frame, mask = mask)
    #frcv2.imshow('hatch', res)
    #cv2.imshow('hatch detection', frame)
    (contours, a) = cv2.findContours(mask1, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    (contoursG, b) = cv2.findContours(mask2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    image = frame
    ci = 0 
    hatch = False
    for c in contours:
        ci = ci + 1
        area = cv2.contourArea(c)
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        if area > 300:
            for c2 in contoursG:
                areaG = cv2.contourArea(c2)
                rectG = cv2.boundingRect(c2)
                xG, yG, wG, hG = rectG
                if areaG > 100:
                    if xG > x and x+w > xG+wG and yG > y and y+h > yG+hG:
                        hatch = True
                        #cv2.imshow('hatch', res)
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
        
    return hatch

        #print(frame[60, 0])
        #if cv2.waitKey(25) & 0xFF == ord('e'):
           # cv2.destroyAllWindows()
           # break

#while True:
#    cap = cv2.VideoCapture("http://10.0.1.112:1181/stream.mjpg")
#    _, f = cap.read()
#    print(isHatch(f))
    
    
